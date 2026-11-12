// User-approved (2026-11-05) out-of-band judge for run_debad9d401bc448c: same judge, rubric, prompt builder,
// image preparation and parser as server/benchmark_judge.mjs#runBenchmarkJudge, minus assertJudgeBenchmarkTrace
// (trace is needs_review: runner crashed on a screenshot download after the 12-screen delivery).
// Writes only into this folder; never touches ui-eval.sqlite3 or trace-integrity-audit.json.
import fs from "node:fs"; import path from "node:path"; import { execFile } from "node:child_process";
import { promisify } from "node:util"; import { createHash } from "node:crypto"; import { DatabaseSync } from "node:sqlite";
const repo = "/mnt/afs/gaoyongyong/code/rate_website_figma-sft-cc-tap-benchmark-design";
const imp = (p) => import(path.join(repo, p));
const { loadSuite } = await imp("server/benchmark_suite.mjs");
const { benchmarkEvidenceImages } = await imp("server/benchmark_evidence.mjs");
const { buildFixed20Prompt, normalizeFixed20Config, parseFixed20Result, fixed20Total } = await imp("server/fixed20_scale.mjs");
const { getScaleMethod } = await imp("server/fixed_scales/index.mjs");
const { buildImageManifest, renderImageBlock, EVAL_TIMEOUT_MS } = await imp("server/cc_evaluation.mjs");
const { generateCriteriaText } = await imp("server/criteria_generation.mjs");
const { MAX_IMAGE_BYTES, callDirectModelVision, imageMediaType } = await imp("server/model_text.mjs");
const { parseClaudeJson, extractClaudeResult } = await imp("server/claude_result.mjs");
const exec = promisify(execFile), sha = (t) => createHash("sha256").update(t).digest("hex");
const dir = path.resolve(import.meta.dirname, ".."), out = import.meta.dirname, runId = process.argv[2];
const python = "/mnt/afs/gaoyongyong/code/rate_website_figma-sft-cc-tap/storage/standalone-original-20261025/venv/bin/python";
if (fs.existsSync(path.join(out, "result.json"))) throw Error("result.json exists; inspect before another paid request");
const suite = loadSuite(dir), db = new DatabaseSync(path.join(dir, "ui-eval.sqlite3"), { readOnly: true });
const run = db.prepare("SELECT * FROM runs WHERE id=?").get(runId); if (!run) throw Error("run not found");
const def = getScaleMethod(suite.rubric.method);
if (!def || def.key !== "fixed_v4" || def.max !== suite.rubric.max) throw Error("rubric drift");
const model = suite.plan.judge, key = JSON.parse(fs.readFileSync(path.join(dir, "private/model_api_keys.json")))[model.id];
if (model.connection_mode !== "direct" || !key) throw Error("judge config unavailable");
const original = benchmarkEvidenceImages(run), folder = path.join(out, "images"); fs.mkdirSync(folder, { recursive: true, mode: 0o700 });
const input = path.join(folder, "input.json"); fs.writeFileSync(input, JSON.stringify(original.images, null, 2), { mode: 0o600 });
const prepared = JSON.parse((await exec(python, [path.join(repo, "server/benchmark_images.py"), "--manifest", input, "--output", folder], { timeout: 300000, maxBuffer: 4e6 })).stdout);
if (prepared.length !== original.total) throw Error("image preparation lost screens");
const layers = JSON.parse(fs.readFileSync(path.join(run.run_dir, "benchmark-layers.json")));
if (layers.board_count !== original.total) throw Error("layer summary does not cover all screens");
const config = normalizeFixed20Config({ prompt_template: suite.rubric.prompt_template }, def);
const prompt = buildFixed20Prompt(config.prompt_template, { query: run.query, imageBlock: renderImageBlock(prepared, original.total),
  layerSummary: layers, criteriaSummary: null, questions: def.questions, layerLabel: def.layer_label, layerHints: def.layer_hints });
fs.writeFileSync(path.join(out, "prompt.txt"), prompt, { mode: 0o600 });
let bytes = 0; const images = prepared.map((i) => { const b = fs.readFileSync(i.path); bytes += b.length; if (bytes > MAX_IMAGE_BYTES) throw Error("too large"); return { data: b.toString("base64"), media_type: imageMediaType(i.path) }; });
let output, result, parsed;
for (let attempt = 0; attempt < 3; attempt++) {
  output = await generateCriteriaText((text, timeoutMs) => callDirectModelVision(model, key, text, images, { timeoutMs }), prompt, { attempts: 2, timeoutMs: EVAL_TIMEOUT_MS });
  parsed = parseClaudeJson(output); result = parseFixed20Result(parsed, def.questions);
  if (!result.parse_error && typeof parsed?.g0?.pass === "boolean") break;
  if (attempt === 2) throw Error("incomplete judge output: " + (result.parse_error || "missing G0"));
}
const res = { kind: "offline-judge/fixed_v4", approved_by: "huangxinyue 2026-11-05", trace_verified: false,
  trace_status: "needs_review (runner ConnectError on screenshot asset download after delivery)",
  run_id: run.id, plan_hash: suite.plan.content_hash, rubric_hash: suite.rubric.content_hash, judge: model.id, api_model: model.model_id,
  prompt_sha256: sha(prompt), image_count: prepared.length, image_paths: prepared.map((i) => i.path), image_manifest: buildImageManifest(prepared),
  images: prepared.map((i) => ({ path: i.path, sha256: sha(fs.readFileSync(i.path)) })),
  cc_values: result.values, evidence: result.evidence, g0_pass: result.g0_pass, g0_reason: result.g0_reason,
  total: fixed20Total(result.values, result.g0_pass, def.questions), raw_output: String(extractClaudeResult(output)).slice(0, 200000), at: new Date().toISOString() };
fs.writeFileSync(path.join(out, "result.json"), JSON.stringify(res, null, 1), { mode: 0o600 });
console.log(JSON.stringify({ total: res.total, g0_pass: res.g0_pass, g0_reason: res.g0_reason, images: res.image_count }));
