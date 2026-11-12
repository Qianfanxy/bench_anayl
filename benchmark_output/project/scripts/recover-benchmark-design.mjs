import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { BenchmarkApiResources, canRetryResourceScore, isBenchmarkTransportError } from "../server/benchmark_api_resources.mjs";
import { benchmarkDeliveryEvidence, benchmarkNeedsFrameRecovery } from "../server/benchmark_health.mjs";
import { snapshotRubric, verifySeal } from "../server/benchmark_protocol.mjs";

const storage = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../storage/benchmark-design");
const plan = JSON.parse(fs.readFileSync(path.join(storage, "recovery-plan.json")));
const manifest = JSON.parse(fs.readFileSync(path.join(storage, "inputs.json")));
const rubric = snapshotRubric();
const job = JSON.parse(fs.readFileSync(path.join(storage, "gpu/job.json")));
const execFileAsync = promisify(execFile);
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const log = (message) => console.log(`${new Date().toISOString()} ${message}`);
const write = (name, value) => {
  const file = path.join(storage, name);
  fs.writeFileSync(file + ".tmp", JSON.stringify(value, null, 2) + "\n", { mode: 0o600 });
  fs.renameSync(file + ".tmp", file);
};
const rubricFile = path.join(storage, "rubric.json");
if (fs.existsSync(rubricFile) && verifySeal(JSON.parse(fs.readFileSync(rubricFile))).content_hash !== rubric.content_hash) {
  throw new Error("Archive the superseded rubric before explicitly changing the official scoring version");
}
write("rubric.json", rubric);
write("scoring-policy.json", { method: rubric.method, rubric_hash: rubric.content_hash, question_count: rubric.questions.length,
  max: rubric.max, judge_model_id: "model_claude_opus55_direct", superseded_methods: ["fixed20"],
  note: "User selected fixed_v4; fixed20 scores are historical and excluded from official results" });
const request = async (route, body, timeout = 30000) => {
  const response = await fetch("http://127.0.0.1:18174" + route, {
    method: body === undefined ? "GET" : "POST", headers: { "content-type": "application/json", connection: "close" },
    ...(body === undefined ? {} : { body: JSON.stringify(body) }), signal: AbortSignal.timeout(timeout),
  });
  const value = await response.json();
  if (!response.ok || value.ok === false) throw new Error(`${route}: ${value.message || response.status}`);
  return value;
};

let scheduler = null;
let schedulerChecked = 0;
let gpuReady = false;
let gpuError = "";
const scoresSubmitted = new Set();
const generationBatches = new Map();
const firstPass = new Map([...plan.retained, ...plan.candidates].map((row) => [row.test_id, row]));
const apiResources = new BenchmarkApiResources();
const frameRecoveryAttempted = new Map();
let frameRecoveryBusy = false;

function recoverVerifiedFrames(state) {
  if (frameRecoveryBusy) return;
  for (const run of state.runs) {
    if (!firstPass.has(run.test_id) || !run.run_dir || Date.now() - (frameRecoveryAttempted.get(run.id) || 0) < 300000) continue;
    const artifact = path.join(run.run_dir, "benchmark-artifact.json");
    const layers = path.join(run.run_dir, "benchmark-layers.json");
    if (!fs.existsSync(artifact) || !fs.existsSync(layers)) continue;
    const delivery = benchmarkDeliveryEvidence(null, JSON.parse(fs.readFileSync(artifact)));
    const manifest = path.join(run.run_dir, "figma-frames/frames.json");
    const frames = fs.existsSync(manifest) ? JSON.parse(fs.readFileSync(manifest)) : [];
    const ready = frames.length > 0 && frames.every((frame) => fs.existsSync(path.join(run.run_dir, "figma-frames", frame.file)));
    if (!benchmarkNeedsFrameRecovery(run, delivery, ready)) continue;
    frameRecoveryAttempted.set(run.id, Date.now());
    frameRecoveryBusy = true;
    log(`${run.id}: recover verified design screenshots independently of trajectory conversion status`);
    execFileAsync("python", ["scripts/recover-benchmark-frames.py", "--run-id", run.id],
      { timeout: 380000, maxBuffer: 1024 * 1024 }).then(({ stdout }) => {
      const result = JSON.parse(stdout.trim().split("\n").at(-1));
      log(`${run.id}: screenshot recovery ${result.ok ? `ready (${result.frames} frames)` : "deferred; original artifact preserved"}`);
    }).catch((error) => log(`${run.id}: screenshot recovery deferred (${error.message.slice(0, 180)})`))
      .finally(() => { frameRecoveryBusy = false; });
    return;
  }
}

async function updateApiResources(state) {
  const scores = (await request(`/api/scale-scores?method=${rubric.method}`)).scores || [];
  for (const score of scores) apiResources.observeFailure(score.eval_model_id, score.error, score.updated_at);
  for (const run of state.runs) apiResources.observeFailure(run.model_id, run.error, run.finished_at);
  const keyFile = path.join(storage, "private/model_api_keys.json");
  const keys = fs.existsSync(keyFile) ? JSON.parse(fs.readFileSync(keyFile)) : {};
  const judgeWasReady = apiResources.available("model_claude_opus55_direct");
  const models = state.models.filter((model) => model.id !== "model_local_a282d9c9a73446c8");
  const snapshot = await apiResources.check(models, (model) => keys[model.id] || process.env[model.api_key_env] || "");
  write("api-resource-status.json", { updated_at: new Date().toISOString(), models: snapshot });
  if (!judgeWasReady && apiResources.available("model_claude_opus55_direct")) {
    for (const score of scores.filter(canRetryResourceScore)) scoresSubmitted.delete(score.run_id);
    log(`Judge API connection restored; quota-interrupted scores can resume with ${rubric.method}`);
  }
}

async function updateGpu(state) {
  if (Date.now() - schedulerChecked < 60000) return;
  schedulerChecked = Date.now();
  try {
    const { stdout } = await execFileAsync("sco", ["acp", "jobs", "describe", job.name,
      "--workspace-name", "design", "-o", "json"], { timeout: 30000, maxBuffer: 1024 * 1024 });
    const result = JSON.parse(stdout);
    scheduler = { job: result.name, state: result.state, checked_at: new Date().toISOString() };
    if (["FAILED", "STOPPED", "CANCELLED"].includes(result.state)) gpuError = `本轮 GPU 作业 ${result.name}: ${result.state}`;
    if (gpuReady || gpuError) return;
    const expectedFile = path.join(storage, "private/model-local-a282d9c9a73446c8.json");
    const expected = JSON.parse(fs.readFileSync(expectedFile));
    const response = await fetch("http://127.0.0.1:18013/v1/models", { signal: AbortSignal.timeout(5000) });
    const models = await response.json();
    if (!response.ok || !models.data?.some((row) => row.id === expected.checkpoint)) return;
    const resumedBatch = state.eval_batches.find((row) => row.id === generationBatches.get("task1"));
    if (resumedBatch && expected.enabled && expected.last_test_ok) {
      gpuReady = true;
      log("Resumed the already validated checkpoint batch; no duplicate inference probes during generation");
      return;
    }
    await request("/api/models/model_local_a282d9c9a73446c8/runtime/test", {}, 300000);
    const validated = JSON.parse(fs.readFileSync(expectedFile));
    if (!validated.last_test_ok) return;
    write("private/model-local-a282d9c9a73446c8.json", { ...validated, enabled: true });
    gpuReady = true;
    log("GPU exact checkpoint and native probes passed; schedule it at the next free generation slot");
  } catch { /* An unallocated or loading worker is a resource wait, not a failed model. */ }
}

async function submitGeneration(group, state) {
  const selected = plan.candidates.filter((row) => row.task === group.task);
  const ids = selected.map((row) => row.test_id);
  for (const row of selected) {
    const saved = state.tests.find((test) => test.id === row.test_id);
    const original = group.tests.find((item) => item.question === row.question);
    if (!saved || saved.query !== original.query || saved.base_figma_url !== original.figma_url || saved.model_id !== group.model_id) {
      throw new Error(`Input changed: ${group.task}/${row.question}`);
    }
  }
  const name = `${plan.tag}/${group.task}`;
  let batch = state.eval_batches.find((row) => row.name === name);
  if (!batch) batch = await request("/api/eval-batches", {
    name, model_id: group.model_id, test_ids: ids, generation_mode: "cc", concurrency: 1,
    reviewer_id: "gyy", reviewer_name: "gyy", young_mode: 0,
  });
  generationBatches.set(group.task, batch.id);
  write("recovery-submissions.json", { updated_at: new Date().toISOString(),
    groups: [...generationBatches].map(([task, batch_id]) => ({ task, batch_id })) });
  log(`${group.task}: recovery batch ${batch.id}; ${ids.length} verified empty files, queries unchanged`);
}

async function scoreReady(state) {
  if (!apiResources.available("model_claude_opus55_direct")) return;
  const jobs = (await request("/api/scale-jobs")).jobs || [];
  if (jobs.some((job) => ["运行中", "排队中"].includes(job.status))) return;
  const existing = (await request(`/api/scale-scores?method=${rubric.method}`)).scores || [];
  const latest = new Map();
  for (const run of state.runs) if (firstPass.has(run.test_id) && (!latest.has(run.test_id)
      || run.started_at > latest.get(run.test_id).started_at)) latest.set(run.test_id, run);
  const targets = [...latest.values()].filter((run) => run.run_dir && !scoresSubmitted.has(run.id)
    && !existing.some((score) => score.run_id === run.id && !canRetryResourceScore(score)));
  const ready = targets.filter((run) => {
    const file = path.join(run.run_dir, "figma-frames/frames.json");
    const layers = path.join(run.run_dir, "benchmark-layers.json");
    if (!fs.existsSync(file) || !fs.existsSync(layers) || ["运行中", "补图中", "已暂停", "停止中"].includes(run.status)) return false;
    const frames = JSON.parse(fs.readFileSync(file));
    return frames.length && frames.every((frame) => fs.existsSync(path.join(run.run_dir, "figma-frames", frame.file)));
  });
  if (!ready.length) return;
  const job = await request("/api/scale-jobs", { name: `${plan.tag} · ${rubric.name}`, method: rubric.method,
    prompt_template: rubric.prompt_template, eval_model_id: "model_claude_opus55_direct",
    run_ids: ready.map((run) => run.id), concurrency: 1, fetch_frames: false });
  for (const run of ready) scoresSubmitted.add(run.id);
  log(`${rubric.method} judge queued ${ready.length} existing designs (${job.id}); no Figma or design regeneration`);
}

async function progress(state) {
  const scores = (await request(`/api/scale-scores?method=${rubric.method}`)).scores || [];
  const groups = manifest.groups.map((group) => ({ task: group.task, model: group.model_name,
    batch_id: generationBatches.get(group.task) || null,
    status: state.eval_batches.find((batch) => batch.id === generationBatches.get(group.task))?.status
      || (group.task !== "task1" && !apiResources.available(group.model_id) ? "等待模型 API 资源恢复" : "")
      || (group.task === "task1" && !gpuReady ? gpuError || "等待 GPU / 模型服务" : "已有产物或等待恢复调度"),
    runs: group.tests.map((question) => {
      const test = state.tests.find((row) => row.title === `benchmark-design-fresh-20261026/${group.task}/${question.question}`);
      const attempts = state.runs.filter((row) => row.test_id === test.id).sort((a, b) => b.started_at.localeCompare(a.started_at));
      const run = attempts[0];
      const score = scores.find((row) => row.run_id === run?.id && row.is_baseline !== 0 && row.status === "已完成");
      const first = firstPass.get(test.id);
      const receipt = run?.run_dir && path.join(run.run_dir, "benchmark-delivery.json");
      const artifact = run?.run_dir && path.join(run.run_dir, "benchmark-artifact.json");
      const delivery = receipt && fs.existsSync(receipt) ? JSON.parse(fs.readFileSync(receipt))
        : artifact && fs.existsSync(artifact) ? benchmarkDeliveryEvidence(null, JSON.parse(fs.readFileSync(artifact))) : null;
      const resourceFile = run?.run_dir && path.join(run.run_dir, "benchmark-infrastructure.json");
      const infrastructure = resourceFile && fs.existsSync(resourceFile) ? JSON.parse(fs.readFileSync(resourceFile)) : null;
      return { question: question.question, test_id: test.id, id: run?.id, status: run?.status,
        model_started: Boolean(run?.run_dir), attempt_count: attempts.length, error: run?.error || "",
        delivery, infrastructure,
        first_pass: { id: first.original_run_id, status: first.original_status,
          quota_errors: first.evidence.quota_errors, design_present: first.evidence.design_present },
        score_status: score ? "已完成" : scores.find((row) => row.run_id === run?.id)?.status || "尚未评分",
        score: score?.total ?? null, g0_pass: score?.g0_pass ?? null };
    }) }));
  const logical = groups.flatMap((group) => group.runs);
  const completedScores = logical.filter((row) => row.score_status === "已完成").length;
  const output = { updated_at: new Date().toISOString(), tag: plan.tag, phase: completedScores === 21 ? "evaluation_finished" : "recovering",
    total_tests: 21, models: 7, scoring_method: rubric.method, rubric_hash: rubric.content_hash,
    score_max: rubric.max, question_count: rubric.questions.length, superseded_methods: ["fixed20"],
    query_modified: false, retained_designs: plan.retained.length, empty_retries: plan.candidates.length,
    attempt_count: state.runs.length, model_started_cases: logical.filter((run) => run.model_started).length,
    design_present_cases: logical.filter((run) => run.delivery?.design_present).length,
    scores_completed: completedScores, gpu_scheduler: scheduler, gpu_error: gpuError,
    api_resources: apiResources.snapshot(),
    judge_status: apiResources.available("model_claude_opus55_direct") ? "可用" : "等待模型 API 资源恢复", groups };
  write("progress.json", output);
  const gpuBatch = state.eval_batches.find((row) => row.id === generationBatches.get("task1"));
  if (gpuBatch?.status === "已完成") write("gpu/release.json", { batch_id: gpuBatch.id, finished_at: new Date().toISOString() });
  if (completedScores === 21) write("complete.json", { finished_at: new Date().toISOString(), tests: 21,
    scores_completed: 21, phase: "evaluation_finished", scoring_method: rubric.method, rubric_hash: rubric.content_hash,
    score_max: rubric.max, question_count: rubric.questions.length,
    note: "Official fixed_v4 scores assess delivered artifacts; superseded fixed20 scores and infrastructure-interrupted first attempts remain historical" });
  return completedScores === 21;
}

try {
  while (true) {
    try {
      let state = await request("/api/bootstrap");
      for (const group of manifest.groups) {
        const batch = state.eval_batches.find((row) => row.name === `${plan.tag}/${group.task}`);
        if (batch) generationBatches.set(group.task, batch.id);
      }
      await updateApiResources(state);
      recoverVerifiedFrames(state);
      await scoreReady(state);
      await updateGpu(state);
      const active = state.eval_batches.some((row) => [...generationBatches.values()].includes(row.id)
        && ["排队中", "运行中", "已暂停"].includes(row.status));
      if (!active) {
        const pending = manifest.groups.filter((group) => plan.candidates.some((row) => row.task === group.task)
          && !generationBatches.has(group.task));
        const next = (gpuReady && pending.find((group) => group.task === "task1"))
          || pending.find((group) => group.task !== "task1" && apiResources.available(group.model_id));
        if (next) await submitGeneration(next, state);
      }
      state = await request("/api/bootstrap");
      const finished = await progress(state);
      fs.rmSync(path.join(storage, "recovery-error.json"), { force: true });
      if (finished) break;
    } catch (error) {
      if (!isBenchmarkTransportError(error)) throw error;
      const detail = { at: new Date().toISOString(), message: error.message, cause: error.cause?.code, retryable: true };
      write("recovery-error.json", detail);
      fs.appendFileSync(path.join(storage, "recovery-transport-errors.jsonl"), JSON.stringify(detail) + "\n", { mode: 0o600 });
      // Never blindly repeat a POST after an ambiguous response. The next
      // iteration reconciles existing batches and score jobs from the server.
      log(`Benchmark API transport interrupted; reconcile saved batches after 15s (${error.cause?.code || error.name})`);
    }
    await sleep(15000);
  }
  log("All 21 logical cases have actual judge results; original attempts and resource attribution retained");
} catch (error) {
  write("recovery-error.json", { at: new Date().toISOString(), message: error.message });
  log(`Recovery supervisor error: ${error.message}`);
  process.exitCode = 1;
}
