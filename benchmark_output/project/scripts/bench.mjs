#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { execFile, spawn } from "node:child_process";
import { promisify } from "node:util";
import { assertFreshBenchmarkSnapshot } from "../server/benchmark_fixture.mjs";
import { BENCHMARK_RUBRIC_ID, bindCopies, canonical, cleanModel, createDataset, createPlan, figmaKey, fingerprint, makeResultRows, snapshotRubric, verifySeal } from "../server/benchmark_protocol.mjs";
import { openFigmaCopyProvider, provisionCopies, saveJson } from "../server/benchmark_copies.mjs";
import { assertBackend, createBenchmarkClient, loadSuite, prepareSuite } from "../server/benchmark_suite.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const execFileAsync = promisify(execFile);
const read = (file) => JSON.parse(fs.readFileSync(file, "utf8"));
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
function argumentsOf(argv) {
  const options = {};
  for (let i = 0; i < argv.length; i++) {
    const name = argv[i];
    if (!name.startsWith("--")) throw new Error(`Unknown argument ${name}`);
    if (["--background", "--once"].includes(name)) options[name.slice(2)] = true;
    else { if (!argv[i + 1] || argv[i + 1].startsWith("--")) throw new Error(`${name} requires a value`); options[name.slice(2)] = argv[++i]; }
  }
  return options;
}
function immutable(file, value) {
  if (fs.existsSync(file)) {
    const existing = verifySeal(read(file));
    if (existing.content_hash !== value.content_hash) throw new Error(`${file} is immutable; use a new dataset/run directory`);
    return existing;
  }
  saveJson(file, value); return value;
}
async function rowsFrom(file) {
  const extension = path.extname(file).toLowerCase();
  if ([".csv", ".xlsx"].includes(extension)) {
    const { stdout } = await execFileAsync("python", [path.join(root, "scripts/bench_table.py"), "read", "--input", path.resolve(file)], { maxBuffer: 64 * 1024 * 1024 });
    return JSON.parse(stdout);
  }
  if ([".txt", ".jsonl"].includes(extension)) return fs.readFileSync(file, "utf8").split(/\r?\n/).filter(Boolean).map((line) => extension === ".jsonl" ? JSON.parse(line) : line);
  const value = read(file);
  return value.cases || value.rows || value.copies || value;
}
function lease(file) {
  fs.mkdirSync(path.dirname(file), { recursive: true, mode: 0o700 });
  if (fs.existsSync(file)) {
    const owner = read(file);
    try { process.kill(owner.pid, 0); throw new Error(`Workflow is already running (PID ${owner.pid})`); }
    catch (error) { if (error.code !== "ESRCH") throw error; fs.unlinkSync(file); }
  }
  fs.writeFileSync(file, JSON.stringify({ pid: process.pid }), { flag: "wx", mode: 0o600 });
  return () => { if (fs.existsSync(file) && read(file).pid === process.pid) fs.unlinkSync(file); };
}
function apiFor(directory, options) { return options.api || (fs.existsSync(path.join(directory, "server.json")) ? read(path.join(directory, "server.json")).api : "http://127.0.0.1:18184"); }
async function inspectFile(url, options) {
  if (!options["mcp-config"]) throw new Error("copy requires --mcp-config for read-only source and copy verification");
  const { stdout } = await execFileAsync(options.python || "python", [path.join(root, "server/benchmark_fixture.py"),
    "--mcp-config", path.resolve(options["mcp-config"]), "--file-key", figmaKey(url)], { timeout: 180000, maxBuffer: 1024 * 1024 });
  return JSON.parse(stdout);
}
async function exportSuite(suite, call, output) {
  await assertBackend(suite, call);
  const state = await call("/api/bootstrap"); const scores = (await call(`/api/scale-scores?method=${suite.rubric.method}`)).scores;
  const rows = makeResultRows(suite.dataset, suite.plan, suite.execution, state, scores, suite.rubric);
  for (const row of rows) {
    const run = state.runs.find((r) => r.id === row.run_id);
    const receipt = run?.run_dir && path.join(run.run_dir, "benchmark-delivery.json");
    const delivery = receipt && fs.existsSync(receipt) ? read(receipt) : null;
    Object.assign(row, { design_present: delivery?.design_present ?? null, delivery_state: delivery?.artifact_state || "unverified",
      product_frame_count: delivery?.frame_count ?? null, missing_required_names: (delivery?.missing_screens || []).join("; "),
      infrastructure_blocked: delivery?.infrastructure_blocked ?? null });
  }
  const common = suite.dataset.cases.map((c) => c.case_id).filter((id) => suite.plan.models.every((m) => rows.some((r) => r.case_id === id && r.model_id === m.id && r.score_total !== null)));
  const mean = (items) => items.length ? Math.round(items.reduce((sum, r) => sum + r.score_total, 0) / items.length * 100) / 100 : null;
  const summary = suite.plan.models.map((model) => {
    const modelRows = rows.filter((r) => r.model_id === model.id); const scored = modelRows.filter((r) => r.score_total !== null);
    return { model_id: model.id, model_name: model.name || model.id, total: modelRows.length, scored: scored.length,
      mean_score: mean(scored), common_case_count: common.length, common_case_mean: mean(scored.filter((r) => common.includes(r.case_id))),
      scoring_method: suite.rubric.method, score_max: suite.rubric.max, g0_passed: scored.filter((r) => r.g0_pass).length };
  });
  fs.mkdirSync(output, { recursive: true, mode: 0o700 });
  const testIds = new Set(rows.map((r) => r.test_id));
  const attempts = state.runs.filter((r) => testIds.has(r.test_id)).map((r) => Object.fromEntries(
    ["id", "test_id", "model_id", "status", "query", "figma_url", "run_dir", "error", "frames_error", "started_at", "finished_at"].map((k) => [k, r[k] ?? null])));
  saveJson(path.join(output, "dataset.json"), suite.dataset);
  saveJson(path.join(output, "rubric.json"), suite.rubric);
  saveJson(path.join(output, "results.json"), { exported_at: new Date().toISOString(), dataset_hash: suite.dataset.content_hash,
    rubric_hash: suite.rubric.content_hash, plan: suite.plan, execution: suite.execution, rows, attempts,
    scores: scores.filter((s) => testIds.has(s.test_id)), summary });
  saveJson(path.join(output, "summary.json"), summary);
  for (const [name, records] of [["cases", suite.dataset.cases], ["results", rows], ["summary", summary]]) {
    const json = path.join(output, `${name}-table.json`); saveJson(json, records);
    for (const extension of ["csv", "xlsx"]) await execFileAsync("python", [path.join(root, "scripts/bench_table.py"), "write", "--input", json, "--output", path.join(output, `${name}.${extension}`)]);
  }
  return { cases: suite.dataset.cases.length, models: suite.plan.models.length, results: rows.length,
    scored: rows.filter((r) => r.score_total !== null).length, common_case_count: common.length, output };
}

export async function main(argv = process.argv.slice(2)) {
  const [command = "help", ...rest] = argv; const options = argumentsOf(rest);
  if (command === "help") {
    console.log("bench import|plan|copy|bind|start|prepare|run|status|export|rubric\nSee docs/benchmark-workflow.md for inputs, isolation and examples."); return;
  }
  if (command === "rubric") {
    const rubric = snapshotRubric();
    if (options.output) immutable(path.resolve(options.output), rubric);
    console.log(JSON.stringify({ id: rubric.id, hash: rubric.content_hash, max: rubric.max, questions: rubric.questions.length })); return;
  }
  if (!options.dir) throw new Error("Provide --dir for an isolated benchmark directory");
  const directory = path.resolve(options.dir); const at = (name) => path.join(directory, name);
  if (command === "import") {
    if (!options.input || !options.id) throw new Error("import requires --input and --id");
    const template = fs.readFileSync(options.template || path.join(root, "benchmarks/templates/initial-design.zh.txt"), "utf8");
    const imported = path.extname(options.input).toLowerCase() === ".json" ? read(options.input) : null;
    if (imported?.kind === "dataset" && imported.id !== options.id) throw new Error("Use the original dataset id when reimporting its sealed manifest");
    const dataset = immutable(at("dataset.json"), imported?.kind === "dataset" ? verifySeal(imported)
      : createDataset(await rowsFrom(options.input), { id: options.id, template }));
    console.log(JSON.stringify({ dataset: dataset.id, cases: dataset.cases.length, hash: dataset.content_hash })); return;
  }
  if (command === "plan") {
    if (!options.models || !options.id) throw new Error("plan requires --models and --id");
    const specification = read(options.models); const raw = specification.models || specification;
    const source = options["models-api"] ? await createBenchmarkClient(options["models-api"])("/api/bootstrap") : { models: [] };
    const resolve = (model) => {
      const value = cleanModel(model); const existing = source.models.find((m) => m.id === value.id);
      const complete = { ...(existing ? cleanModel(existing) : {}), ...value };
      if (!complete.model_id || !complete.connection_mode) throw new Error(`Full configuration needed for ${value.id}; pass --models-api to resolve existing model ids`);
      return complete;
    };
    const models = raw.map(resolve);
    const judgeRef = specification.judge || options.judge || "model_claude_opus55_direct";
    const judge = resolve(typeof judgeRef === "string" ? models.find((m) => m.id === judgeRef) || judgeRef : judgeRef);
    const rubric = immutable(at("rubric.json"), read(path.join(root, `benchmarks/rubrics/${BENCHMARK_RUBRIC_ID}.json`)));
    const plan = immutable(at("plan.json"), createPlan(verifySeal(read(at("dataset.json"))), models, rubric, { id: options.id, judge }));
    console.log(JSON.stringify({ plan: plan.id, cases: plan.case_count, models: plan.models.length, assignments: plan.assignment_count })); return;
  }
  if (command === "copy") {
    if (!options["browser-config"]) throw new Error("copy requires --browser-config");
    const dataset = verifySeal(read(at("dataset.json"))); const plan = verifySeal(read(at("plan.json")));
    const release = lease(at("copies.lock")); let provider;
    try {
      const sourceFile = at("sources-preflight.json");
      const preflight = fs.existsSync(sourceFile) ? read(sourceFile) : { dataset_hash: dataset.content_hash, files: Object.create(null) };
      if (preflight.dataset_hash !== dataset.content_hash) throw new Error("Source preflight belongs to a different dataset");
      for (const item of dataset.cases) if (!Object.hasOwn(preflight.files, item.case_id)) {
        const snapshot = await inspectFile(item.source_figma_url, options);
        assertFreshBenchmarkSnapshot(snapshot, { fileKey: item.source_file_key }, { requiredPages: dataset.required_pages });
        preflight.files[item.case_id] = snapshot; saveJson(sourceFile, preflight);
      }
      provider = await openFigmaCopyProvider(read(options["browser-config"]));
      const verifyCopy = provider.verifyCopy.bind(provider);
      provider.verifyCopy = async (record) => {
        await verifyCopy(record);
        const snapshot = await inspectFile(record.target_figma_url, options);
        assertFreshBenchmarkSnapshot(snapshot, { fileKey: figmaKey(record.target_figma_url) }, { requiredPages: dataset.required_pages });
        const original = preflight.files[record.case_id];
        const counts = (pages) => pages.filter((p) => !/^03\s*[·.\-—]/.test(p.name)).map((p) => [p.name, p.child_count]).sort();
        if (canonical(counts(snapshot.pages)) !== canonical(counts(original.pages))) throw new Error("Copied reference pages differ from the original template");
        saveJson(at(`copy-preflight/${record.assignment_id}.json`), snapshot);
      };
      const journal = await provisionCopies(dataset, plan, at("copies.json"), provider, { limit: Number(options.limit || Infinity), log: (value) => console.log(JSON.stringify(value)) });
      const ready = journal.copies.filter((c) => c.status === "ready");
      if (ready.length === plan.assignment_count) immutable(at("inputs.json"), bindCopies(dataset, plan, ready));
      console.log(JSON.stringify({ ready: ready.length, total: plan.assignment_count, originals_modified: false }));
    } finally { try { if (provider) await provider.close(); } finally { release(); } }
    return;
  }
  if (command === "bind") {
    if (!options.input) throw new Error("bind requires --input with already provisioned copy mappings");
    const result = immutable(at("inputs.json"), bindCopies(read(at("dataset.json")), read(at("plan.json")), await rowsFrom(options.input)));
    console.log(JSON.stringify({ bound: result.groups.reduce((n, g) => n + g.tests.length, 0) })); return;
  }
  if (command === "status" && !fs.existsSync(at("inputs.json"))) {
    const plan = fs.existsSync(at("plan.json")) ? read(at("plan.json")) : null;
    const copies = fs.existsSync(at("copies.json")) ? read(at("copies.json")).copies : [];
    console.log(JSON.stringify({ phase: "awaiting_plan_or_copies", total: plan?.assignment_count || 0,
      copies_ready: copies.filter((c) => c.status === "ready").length }, null, 2)); return;
  }
  const suite = loadSuite(directory);
  if (command === "start") {
    if (!options["runtime-config"]) throw new Error("start requires --runtime-config with installed runner and Figma account paths");
    const port = Number(options.port || (fs.existsSync(at("server.json")) ? new URL(read(at("server.json")).api).port : 18184)); const api = `http://127.0.0.1:${port}`;
    const pidFile = at("server.pid");
    if (fs.existsSync(pidFile)) {
      const pid = Number(fs.readFileSync(pidFile));
      try { process.kill(pid, 0); await assertBackend(suite, createBenchmarkClient(api)); console.log(JSON.stringify({ api, pid, already_running: true })); return; }
      catch (error) { if (error.code !== "ESRCH") throw error; }
    }
    const occupied = await fetch(`${api}/api/health`, { signal: AbortSignal.timeout(1000) }).then(() => true).catch(() => false);
    if (occupied) throw new Error("Benchmark port is already in use; choose another --port");
    const credentialsFile = options.credentials || path.join(root, "storage/benchmark-design/private/model_api_keys.json");
    if (fs.existsSync(credentialsFile)) {
      const keys = read(credentialsFile); const ids = new Set([...suite.plan.models.map((m) => m.id), suite.plan.judge.id]);
      saveJson(at("private/model_api_keys.json"), Object.fromEntries(Object.entries(keys).filter(([id]) => ids.has(id))));
    }
    const log = fs.openSync(at("server.log"), "a", 0o600);
    const child = spawn(process.execPath, [path.join(root, "scripts/start-benchmark-design.mjs"), "--runtime-config", path.resolve(options["runtime-config"]), "--storage-root", directory, "--port", String(port)],
      { cwd: root, detached: true, stdio: ["ignore", log, log], env: { ...process.env, UI_EVAL_BENCHMARK_RECOVERY: "1" } });
    child.unref(); fs.closeSync(log); fs.writeFileSync(pidFile, String(child.pid)); saveJson(at("server.json"), { api, pid: child.pid });
    for (let i = 0; i < 60; i++) { try { await assertBackend(suite, createBenchmarkClient(api)); console.log(JSON.stringify({ api, pid: child.pid })); return; } catch { await sleep(500); } }
    throw new Error("Benchmark server did not become ready; inspect its isolated server.log");
  }
  const api = apiFor(directory, options); const call = createBenchmarkClient(api);
  if (command === "prepare") { await prepareSuite(suite, call); console.log(JSON.stringify({ imported: suite.plan.assignment_count })); return; }
  if (command === "run") {
    if (fs.existsSync(at("supervisor.pid"))) {
      const pid = Number(fs.readFileSync(at("supervisor.pid")));
      if (!Number.isInteger(pid) || pid < 1) throw new Error("Invalid supervisor PID file");
      try {
        process.kill(pid, 0);
        const args = fs.readFileSync(`/proc/${pid}/cmdline`, "utf8").split("\0");
        if (!args.includes(path.join(root, "scripts/run-benchmark-suite.mjs")) || !args.includes(directory)) throw new Error("Supervisor PID belongs to another process");
        console.log(JSON.stringify({ supervisor_pid: pid, already_running: true })); return;
      } catch (error) { if (error.code !== "ESRCH") throw error; }
    }
    await prepareSuite(suite, call);
    const args = [path.join(root, "scripts/run-benchmark-suite.mjs"), "--dir", directory, "--api", api];
    if (options.once) args.push("--once");
    if (options.background) {
      const log = fs.openSync(at("supervisor.log"), "a", 0o600);
      const child = spawn(process.execPath, args, { cwd: root, detached: true, stdio: ["ignore", log, log] });
      child.unref(); fs.closeSync(log); console.log(JSON.stringify({ supervisor_pid: child.pid, total: suite.plan.assignment_count }));
    } else { const child = spawn(process.execPath, args, { cwd: root, stdio: "inherit" }); await new Promise((resolve) => child.once("close", (code) => { process.exitCode = code; resolve(); })); }
    return;
  }
  if (command === "status") { console.log(JSON.stringify(fs.existsSync(at("progress.json")) ? read(at("progress.json")) : { total: suite.plan.assignment_count, phase: "not_started" }, null, 2)); return; }
  if (command === "export") { console.log(JSON.stringify(await exportSuite(suite, call, path.resolve(options.output || at("exports"))))); return; }
  throw new Error(`Unknown command: ${command}`);
}
if (process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url) main().catch((error) => { console.error(error.message); process.exitCode = 1; });
