import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { benchmarkDesignTarget } from "../server/benchmark_design.mjs";
import { assertFreshBenchmarkAssignment, assertFreshBenchmarkSnapshot } from "../server/benchmark_fixture.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const storage = path.join(root, "storage/benchmark-design");
const tag = "benchmark-design-fresh-20261026";
const raw = fs.readFileSync(path.join(storage, "inputs.json"));
const manifest = JSON.parse(raw);
const preflight = JSON.parse(fs.readFileSync(path.join(storage, "fresh-preflight-20261026.json")));
if (preflight.manifest_sha256 !== crypto.createHash("sha256").update(raw).digest("hex") || preflight.files.length !== 21) {
  throw new Error("Complete read-only checks for the current 21 inputs before submitting");
}
for (const group of manifest.groups) for (const item of group.tests) {
  const target = benchmarkDesignTarget(item.query, item.figma_url);
  assertFreshBenchmarkAssignment(manifest, target, item.query, group.model_id);
  assertFreshBenchmarkSnapshot(preflight.files.find((row) => row.file_key === target.fileKey)?.snapshot, target);
}

const execFileAsync = promisify(execFile);
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const log = (text) => console.log(`${new Date().toISOString()} ${text}`);
const write = (name, value) => {
  const file = path.join(storage, name);
  fs.writeFileSync(file + ".tmp", JSON.stringify(value, null, 2) + "\n", { mode: 0o600 });
  fs.renameSync(file + ".tmp", file);
};
const request = async (route, body, timeout = 30000) => {
  const response = await fetch("http://127.0.0.1:18174" + route, {
    method: body === undefined ? "GET" : "POST", headers: { "content-type": "application/json" },
    ...(body === undefined ? {} : { body: JSON.stringify(body) }), signal: AbortSignal.timeout(timeout),
  });
  const value = await response.json();
  if (!response.ok || value.ok === false) throw new Error(`${route}: ${value.message || response.status}`);
  return value;
};

let checkpointState = "等待 GPU / 模型服务";
let checkpointError = "";
let scheduler = null;
let schedulerChecked = 0;
let progressBusy = false;
const gpuGroup = manifest.groups[0];
const gpuConfigFile = path.join(storage, "private/model-local-a282d9c9a73446c8.json");
const gpuJob = JSON.parse(fs.readFileSync(path.join(storage, "gpu/job.json")));
const terminal = new Set(["FAILED", "STOPPED", "CANCELLED", "COMPLETED", "SUCCEEDED"]);
const batches = new Map();

async function updateProgress() {
  if (progressBusy) return false;
  progressBusy = true;
  try {
    const state = await request("/api/bootstrap");
    if (Date.now() - schedulerChecked > 60000) {
      schedulerChecked = Date.now();
      try {
        const { stdout } = await execFileAsync("sco", ["acp", "jobs", "describe", gpuJob.name,
          "--workspace-name", "design", "-o", "json"], { timeout: 30000, maxBuffer: 1024 * 1024 });
        const job = JSON.parse(stdout);
        scheduler = { job: job.name, state: job.state, checked_at: new Date().toISOString() };
      } catch { log("GPU scheduler check temporarily unavailable"); }
    }
    const groups = manifest.groups.map((group) => {
      const batch = state.eval_batches.find((row) => row.name === `${tag}/${group.task}`);
      const runs = batch ? state.runs.filter((run) => run.batch_id === batch.id) : [];
      return { task: group.task, model: group.model_name, test_count: 3, batch_id: batch?.id || null,
        status: batch?.status || (group.task === "task1" ? checkpointState : "待提交"),
        ...(group.task === "task1" && checkpointError ? { error: checkpointError } : {}),
        runs: runs.map((run) => ({ id: run.id, test_id: run.test_id, status: run.status,
          model_started: Boolean(run.run_dir),
          error: run.error || "", frames_error: run.frames_error || "", started_at: run.started_at,
          finished_at: run.finished_at, figma_url: run.figma_url })) };
    });
    write("progress.json", { updated_at: new Date().toISOString(), tag, total_tests: 21, models: 7,
      query_modified: false, submitted_batches: groups.filter((group) => group.batch_id).length,
      gpu_scheduler: scheduler, groups });
    const gpu = groups[0];
    if (gpu.status === "已完成" && gpu.runs.length === 3 && gpu.runs.every((run) => run.model_started)) write("gpu/release.json", { finished_at: new Date().toISOString(), batch_id: gpu.batch_id });
    return groups.every((group) => group.batch_id && group.status === "已完成");
  } finally { progressBusy = false; }
}

async function prepareCheckpoint() {
  const expected = JSON.parse(fs.readFileSync(gpuConfigFile)).checkpoint;
  while (true) {
    if (scheduler && terminal.has(scheduler.state)) throw new Error(`GPU job ${gpuJob.name} ended with ${scheduler.state}`);
    try {
      const response = await fetch("http://127.0.0.1:18013/v1/models", { signal: AbortSignal.timeout(5000) });
      const value = await response.json();
      if (response.ok && value.data?.some((model) => model.id === expected)) break;
    } catch { /* Wait for this benchmark's own GPU worker. */ }
    await sleep(15000);
  }
  checkpointState = "模型服务就绪，连接测试中";
  await request(`/api/models/${gpuGroup.model_id}/runtime/test`, {}, 300000);
  const config = JSON.parse(fs.readFileSync(gpuConfigFile));
  if (!config.last_test_ok) throw new Error("Checkpoint connection probes failed");
  write("private/model-local-a282d9c9a73446c8.json", { ...config, enabled: true });
  log("task1: exact checkpoint identity and native connection probes passed");
}

async function submit(group) {
  const state = await request("/api/bootstrap");
  const tests = group.tests.map((item) => {
    const saved = state.tests.find((test) => test.title === `${tag}/${group.task}/${item.question}`);
    if (!saved || saved.query !== item.query || saved.base_figma_url !== item.figma_url
        || saved.model_id !== group.model_id) throw new Error(`Stored input mismatch: ${group.task}/${item.question}`);
    return saved.id;
  });
  const name = `${tag}/${group.task}`;
  let dataset = state.datasets.find((row) => row.name === name);
  if (!dataset) dataset = await request("/api/datasets", { name, test_ids: tests });
  else if (JSON.stringify([...dataset.test_ids].sort()) !== JSON.stringify([...tests].sort())) throw new Error(`Dataset mismatch: ${name}`);
  let batch = state.eval_batches.find((row) => row.name === name);
  const generationMode = group.task === "task7" ? "direct" : "cc";
  if (batch && (batch.model_id !== group.model_id || batch.generation_mode !== generationMode
      || JSON.stringify([...batch.test_ids].sort()) !== JSON.stringify([...tests].sort()))) throw new Error(`Batch mismatch: ${name}`);
  if (!batch) batch = await request("/api/eval-batches", { name, model_id: group.model_id,
    dataset_id: dataset.id, generation_mode: generationMode, concurrency: 1, young_mode: 0,
    reviewer_id: "gyy", reviewer_name: "gyy" });
  batches.set(group.task, batch.id);
  write("submission-state.json", { tag, updated_at: new Date().toISOString(), total_tests: 21,
    batches: [...batches].map(([task, batch_id]) => ({ task, batch_id })) });
  log(`${group.task}: submitted ${batch.id}, ${group.model_name}, 3 verbatim queries`);
}

let monitor;
try {
  monitor = setInterval(() => updateProgress().catch((error) => log(`Progress check: ${error.message}`)), 15000);
  await updateProgress();
  for (const group of manifest.groups.slice(1)) await submit(group);
  await updateProgress();
  try {
    await prepareCheckpoint();
    await submit(gpuGroup);
  } catch (error) {
    checkpointState = "GPU / 模型服务失败，3 条任务尚未启动";
    checkpointError = error.message;
    write("gpu/error.json", { at: new Date().toISOString(), message: checkpointError });
    // Keep recording the other six groups even when the checkpoint fails.
    log(checkpointError);
  }
  while (true) {
    if (await updateProgress()) break;
    if (checkpointError) {
      const progress = JSON.parse(fs.readFileSync(path.join(storage, "progress.json")));
      if (progress.groups.slice(1).every((group) => group.status === "已完成")) throw new Error(checkpointError);
    }
    await sleep(15000);
  }
  const progress = JSON.parse(fs.readFileSync(path.join(storage, "progress.json")));
  const started = progress.groups.flatMap((group) => group.runs).filter((run) => run.model_started).length;
  write("generation-complete.json", { finished_at: new Date().toISOString(), tests: 21, batches: 7,
    model_started: started, phase: "generation_finished", evaluation_complete: false });
  log("Generation phase ended; output verification and judge scores determine evaluation completion");
} catch (error) {
  write("supervisor-error.json", { at: new Date().toISOString(), message: error.message });
  log(`Supervisor stopped: ${error.message}`);
  process.exitCode = 1;
} finally { clearInterval(monitor); }
