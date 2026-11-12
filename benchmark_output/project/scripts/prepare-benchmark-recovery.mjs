import fs from "node:fs";
import path from "node:path";
import { DatabaseSync } from "node:sqlite";
import { fileURLToPath } from "node:url";
import { benchmarkDeliveryEvidence } from "../server/benchmark_health.mjs";
import { assertFreshBenchmarkSnapshot } from "../server/benchmark_fixture.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../storage/benchmark-design");
const manifest = JSON.parse(fs.readFileSync(path.join(root, "inputs.json")));
const artifacts = JSON.parse(fs.readFileSync(path.join(root, "artifact-audit-20261026.json"))).files;
const audits = JSON.parse(fs.readFileSync(path.join(root, "failure-attribution-20261026.json")));
const db = new DatabaseSync(path.join(root, "ui-eval.sqlite3"), { readOnly: true });
const candidates = [];
const retained = [];
for (const group of manifest.groups) for (const task of group.tests) {
  const test = db.prepare("SELECT * FROM tests WHERE title=?").get(`benchmark-design-fresh-20261026/${group.task}/${task.question}`);
  if (!test || test.query !== task.query || test.model_id !== group.model_id) throw new Error("Fresh input changed");
  const run = db.prepare("SELECT * FROM runs WHERE test_id=? ORDER BY started_at DESC LIMIT 1").get(test.id);
  const snapshot = artifacts.find((row) => row.file_key === task.file_key)?.snapshot;
  if (!snapshot) throw new Error(`Missing live artifact inspection: ${test.id}`);
  const original = audits.find((row) => row.id === run.id);
  const trajectory = run.run_dir && path.join(run.run_dir, "task-000001/trajectory.jsonl");
  const record = trajectory && fs.existsSync(trajectory) ? JSON.parse(fs.readFileSync(trajectory, "utf8").split("\n")[0]) : null;
  const evidence = { ...benchmarkDeliveryEvidence(record, snapshot), quota_errors: original?.quota_errors || 0,
    infrastructure_blocked: Boolean(original?.quota_errors), first_pass_status: run.status, first_pass_error: run.error };
  if (run.run_dir) {
    fs.writeFileSync(path.join(run.run_dir, "benchmark-delivery.json"), JSON.stringify(evidence, null, 2) + "\n", { mode: 0o600 });
  }
  const item = { task: group.task, question: task.question, test_id: test.id, model_id: group.model_id,
    model_name: group.model_name, original_run_id: run.id, original_status: run.status, file_key: task.file_key,
    evidence, generation_mode: group.task === "task7" ? "direct" : "cc" };
  if (!evidence.design_present && (!run.run_dir || evidence.infrastructure_blocked)) {
    assertFreshBenchmarkSnapshot(snapshot, { fileKey: task.file_key });
    candidates.push(item);
  } else retained.push(item);
}
db.close();
const plan = { created_at: new Date().toISOString(), tag: "benchmark-design-repair-20261026",
  query_modified: false, figma_content_deleted: false, candidates, retained };
fs.writeFileSync(path.join(root, "recovery-plan.json"), JSON.stringify(plan, null, 2) + "\n", { mode: 0o600 });
console.log(JSON.stringify({ safe_empty_retries: candidates.length, retained_designs: retained.length,
  retained_frame_count: retained.reduce((n, row) => n + row.evidence.frame_count, 0), query_modified: false }));
