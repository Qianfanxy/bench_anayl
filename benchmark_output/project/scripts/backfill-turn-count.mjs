// 一次性回填 runs.turn_count（轨迹顶层 total_steps）。跑完即弃。
import fs from "node:fs";
import path from "node:path";
import { DatabaseSync } from "node:sqlite";
const db = new DatabaseSync("storage/ui-eval.sqlite3");
const cols = db.prepare("PRAGMA table_info(runs)").all().map((r) => r.name);
if (!cols.includes("turn_count")) db.exec("ALTER TABLE runs ADD COLUMN turn_count INTEGER NOT NULL DEFAULT 0");
let done = 0, skipped = 0;
for (const row of db.prepare("SELECT id, run_dir FROM runs WHERE run_dir != '' AND turn_count = 0").all()) {
  const p = [path.join(row.run_dir, "task-000001", "trajectory.jsonl"), path.join(row.run_dir, "trajectory.jsonl")]
    .find(fs.existsSync);
  if (!p) { skipped += 1; continue; }
  try {
    const first = fs.readFileSync(p, "utf8").split(/\r?\n/).find(Boolean);
    const steps = Number(JSON.parse(first)?.total_steps) || 0;
    if (steps > 0) { db.prepare("UPDATE runs SET turn_count=? WHERE id=?").run(steps, row.id); done += 1; }
    else skipped += 1;
  } catch { skipped += 1; }
}
console.log(`回填 ${done} 条，跳过（无轨迹/解析失败/0 轮） ${skipped} 条`);
