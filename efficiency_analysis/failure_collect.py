"""Behaviour & failure, step 1: collect per-item scores and the judge's evidence text.

Writes out/item_evidence.csv (one row per run x rubric item) and prints points lost by item.
Usage: .venv/bin/python failure_collect.py out
"""
import csv
import json
import os
import sqlite3
import sys

import pandas as pd

OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
NEW = os.path.join(HERE, "..", "new_output-246-29x4-13x10")
OLD = os.path.join(HERE, "..", "benchmark_output")
MAX = {k: 3 for k in ["B1", "B2", "B3", "B4", "B5", "D1", "D2", "D3", "D4"]}
DIM = {"A": "用户体验", "B": "信息组织", "G": "可交付性", "D": "布局质量", "E": "一致性", "F": "视觉表达"}

R = pd.read_csv(os.path.join(OUT, "reliable_runs.csv"), low_memory=False)
src = pd.read_csv(os.path.join(OUT, "runs.csv"), low_memory=False).set_index("task_id").source_folder
idx = {r["run_id"]: r for r in csv.DictReader(open(os.path.join(OLD, "metadata/portable_run_index.csv"), encoding="utf-8-sig"))}
rows, dbs = [], {}
for _, r in R.iterrows():
    if r.protocol == "v2":
        p = os.path.join(NEW, src[r.task_id], r.task_id, "score.json")
        if not os.path.exists(p):
            continue
        j = json.load(open(p))
        vals, ev, g0 = j.get("values", {}), j.get("evidence", {}), j.get("g0_reason", "")
    else:
        db = os.path.join(OLD, idx[r.task_id]["round_db"])
        con = dbs.setdefault(db, sqlite3.connect(f"file:{db}?immutable=1", uri=True))
        q = con.execute("select cc_values,evidence,g0_reason from scale_scores where run_id=? and status='已完成'", (r.task_id,)).fetchone()
        if not q:
            continue
        vals, ev, g0 = json.loads(q[0]), (json.loads(q[1]) if q[1] else {}), q[2]
    for k, v in vals.items():
        e = ev.get(k) if isinstance(ev, dict) else None
        if isinstance(e, dict):
            e = e.get("evidence") or e.get("text") or json.dumps(e, ensure_ascii=False)
        rows.append(dict(task_id=r.task_id, model=r.model, problem=r.problem, protocol=r.protocol,
                         g0=str(r.g0_pass) == "True", item=k, dimension=DIM.get(k[0], k[0]), score=v, max=MAX.get(k, 2),
                         evidence=e or "", g0_reason=g0 or ""))
E = pd.DataFrame(rows)
E["lost"] = E["max"] - E.score
E.to_csv(os.path.join(OUT, "item_evidence.csv"), index=False)
print(len(E), "item records,", E.task_id.nunique(), "runs; evidence present:", round((E.evidence.str.len() > 0).mean(), 3))
print(E.groupby("protocol").evidence.apply(lambda s: round((s.str.len() > 0).mean(), 2)).to_dict())
g = E[E.g0].groupby(["dimension", "item"]).agg(n=("score", "size"), max=("max", "first"), mean=("score", "mean"),
                                               lost=("lost", "sum"), zero_rate=("score", lambda s: (s == 0).mean()))
g["lost_share"] = g.lost / (g.n * g["max"])
g = g.sort_values("lost_share", ascending=False)
g.to_csv(os.path.join(OUT, "tables", "R_9_points_lost_by_item.csv"))
pd.set_option("display.width", 200)
print(g.round(2).to_string())
print("\nevidence length:", E.evidence.str.len().describe().round(0).to_dict())
