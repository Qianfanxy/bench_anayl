#!/usr/bin/env python3
"""Per-cell asset index for the 29-case / 177-cell benchmark delivery.

Reads deliver-20261103/manifest.json + qa/qa-issues.json, resolves every cell's
raw assets on this machine (/mnt/afs -> /mnt/afs_design), writes 资产清单-索引.csv.
Usage: python3 scripts/build_asset_index.py
"""
import csv, glob, json, os
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DELIVER = ROOT / "deliver-20261103"
OUT = ROOT / "资产清单-索引.csv"
fix = lambda p: (p or "").replace("/mnt/afs/", "/mnt/afs_design/", 1)
size = lambda p: os.path.getsize(p) if p and os.path.isfile(p) else 0

items = json.load(open(DELIVER / "manifest.json"))["items"]
qa = defaultdict(list)
for q in json.load(open(DELIVER / "qa" / "qa-issues.json")):
    qa[q["run_id"]].append(f'[{q["severity"]}]{q["kind"]}')

rows = []
for i in items:
    d = fix(i["run_dir"])
    traj, src = f"{d}/task-000001/trajectory.jsonl", "task"
    if not size(traj):
        rec = [p for p in glob.glob(f"{d}/trace-recovery/**/trajectory.jsonl", recursive=True) if size(p)]
        traj, src = (rec[0], "trace-recovery") if rec else ("", "missing")
    steps = ""
    if traj:
        with open(traj) as f:
            steps = json.loads(f.readline()).get("total_steps", "")
    frames = str(DELIVER / os.path.dirname(i["frames"][0]["file"])) if i.get("frames") else ""
    rows.append({
        "round": i["round"], "case_id": i["case_id"], "title": i["title"], "model": i["model_name"],
        "score_total": i["score_total"], "g0_pass": i["g0_pass"], "score_source": i["score_source"],
        "is_rerun": i["is_rerun"], "run_id": i["run_id"], "minutes": i["minutes"], "turns": i["turns"],
        "trajectory_source": src, "trajectory_steps": steps, "trajectory_mb": round(size(traj) / 1e6, 2),
        "trajectory_path": traj,
        "trace_sqlite": f"{d}/task-000001/trace.sqlite3",
        "run_log": f"{d}/task-000001/run.log" if size(f"{d}/task-000001/run.log") else "",
        "run_dir": d, "round_db": fix(i["source_round_dir"]) + "/ui-eval.sqlite3",
        "frame_count": i["frame_count"], "frames_dir": frames, "account": i["account"], "copy_figma_url": i["copy_figma_url"],
        "source_figma_url": i["source_figma_url"],
        "qa_flags": "; ".join(sorted(set(qa.get(i["run_id"], [])))),
    })

with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)
print(f"{len(rows)} rows -> {OUT}")
