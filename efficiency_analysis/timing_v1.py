"""Where TIME and OUTPUT tokens go, per behaviour category (earlier package only).

The earlier package keeps every model request with its end timestamp, generation time and
output tokens; this batch's trajectories have no timestamps. For each request:
  generation time  = the request's own duration            -> charged to the calls it emits
  tool time        = gap until the next request starts      -> charged to the calls it emitted
  output tokens    = the request's output usage             -> charged to the calls it emits
A request that emits several calls splits its time and tokens equally among them; a request with
no tool call is charged to "text_only_turn". Tool time also contains harness overhead.

Writes out/tables/R_6_time_output_by_category.csv and out/v1_request_timeline.csv.
Usage: .venv/bin/python timing_v1.py ../benchmark_output out
"""
import collections
import csv
import importlib.util
import json
import os
import sqlite3
import sys
from datetime import datetime

import pandas as pd

PKG, OUT = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("tf", os.path.join(os.path.dirname(os.path.abspath(__file__)), "trajfeat.py"))
tf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tf)
ts = lambda t: datetime.fromisoformat(t.replace("Z", "+00:00")).timestamp()
R = pd.read_csv(os.path.join(OUT, "reliable_runs.csv"), low_memory=False)
keep = set(R[R.protocol == "v1"].task_id)
index = [r for r in csv.DictReader(open(os.path.join(PKG, "metadata/portable_run_index.csv"), encoding="utf-8-sig"))
         if r["run_id"] in keep]


def set_ptr(obj, path, value):
    parts = [p for p in path.split("/") if p]
    for p in parts[:-1]:
        obj = obj[int(p)] if isinstance(obj, list) else obj.setdefault(p, {})
    last = parts[-1]
    if isinstance(obj, list):
        i = int(last)
        while len(obj) <= i:
            obj.append(None)
        obj[i] = value
    else:
        obj[last] = value


def requests_tap(con):
    blobs = {h: p for h, p in con.execute("select hash, payload_json from record_blobs")}
    out = []
    for (p,) in con.execute("select payload_json from records order by record_index"):
        j = json.loads(p)
        rec = j.get("record", j)
        for ref in (j.get("__claude_tap_compact_record__") or {}).get("refs", []):
            if ref["path"].startswith("/response") and ref["hash"] in blobs:
                set_ptr(rec, ref["path"], json.loads(blobs[ref["hash"]]))
        body = (rec.get("response") or {}).get("body") or {}
        content = body.get("content") if isinstance(body, dict) else None
        calls = [(b.get("name"), b.get("input")) for b in (content or []) if isinstance(b, dict) and b.get("type") == "tool_use"]
        u = (body.get("usage") or {}) if isinstance(body, dict) else {}
        end = ts(rec["timestamp"])
        out.append(dict(end=end, start=end - (rec.get("duration_ms") or 0) / 1000, gen=(rec.get("duration_ms") or 0) / 1000,
                        out_tok=u.get("output_tokens") or 0, calls=calls, has_content=content is not None))
    return out


def requests_direct(con):
    ev = con.execute("select turn, timestamp, type, payload_json from direct_events order by event_index").fetchall()
    by = collections.defaultdict(list)
    for turn, t, typ, p in ev:
        by[turn].append((ts(t), typ, json.loads(p)))
    out = []
    for turn in sorted(by):
        e = by[turn]
        tim = next((x for x in e if x[1] == "api_timing"), None)
        if not tim:
            continue
        calls = [(x[2].get("tool"), x[2].get("input")) for x in e if x[1] == "tool_use"]
        out.append(dict(end=tim[0], start=tim[0] - tim[2]["duration_ms"] / 1000, gen=tim[2]["duration_ms"] / 1000,
                        out_tok=tim[2].get("output_tokens") or 0, calls=calls, has_content=True))
    return out


rows, timeline = [], []
for r in index:
    con = sqlite3.connect(f"file:{os.path.join(PKG, r['trace_sqlite'])}?immutable=1", uri=True)
    tables = {t[0] for t in con.execute("select name from sqlite_master where type='table'")}
    reqs = requests_tap(con) if "records" in tables else requests_direct(con)
    reqs = [q for q in reqs if q["has_content"]]
    reqs.sort(key=lambda q: q["end"])
    agg = collections.defaultdict(lambda: collections.Counter())
    for i, q in enumerate(reqs):
        nxt = reqs[i + 1]["start"] if i + 1 < len(reqs) else None
        tool_t = max(0.0, nxt - q["end"]) if nxt else 0.0
        cats = [tf.classify_call(n, a)[0] for n, a in q["calls"]] or ["text_only_turn"]
        for c in cats:
            agg[c]["gen_s"] += q["gen"] / len(cats)
            agg[c]["tool_s"] += tool_t / len(cats)
            agg[c]["out_tok"] += q["out_tok"] / len(cats)
            agg[c]["calls"] += 1 if c != "text_only_turn" else 0
        timeline.append(dict(task_id=r["run_id"], model=r["model"], i=i, start=q["start"] - reqs[0]["start"],
                             gen=q["gen"], tool=tool_t, out_tok=q["out_tok"], cats="+".join(cats)))
    for c, v in agg.items():
        rows.append(dict(task_id=r["run_id"], model=r["model"], problem=r["title"], category=c, **v))
D = pd.DataFrame(rows).fillna(0)
pd.DataFrame(timeline).to_csv(os.path.join(OUT, "v1_request_timeline.csv"), index=False)
D.to_csv(os.path.join(OUT, "v1_time_output_by_run_category.csv"), index=False)
T = D.groupby(["model", "category"])[["gen_s", "tool_s", "out_tok", "calls"]].sum()
tot = D.groupby("model")[["gen_s", "tool_s", "out_tok"]].sum()
T["share_of_time"] = (T.gen_s + T.tool_s) / (tot.gen_s + tot.tool_s).reindex(T.index.get_level_values(0)).to_numpy()
T["share_of_output"] = T.out_tok / tot.out_tok.reindex(T.index.get_level_values(0)).to_numpy()
T["tool_s_per_call"] = T.tool_s / T.calls.replace(0, float("nan"))
T["gen_s_per_call"] = T.gen_s / T.calls.replace(0, float("nan"))
T.reset_index().to_csv(os.path.join(TAB := os.path.join(OUT, "tables"), "R_6_time_output_by_category.csv"), index=False)
split = tot.assign(gen_share=tot.gen_s / (tot.gen_s + tot.tool_s), runs=D.groupby("model").task_id.nunique())
split.to_csv(os.path.join(TAB, "R_6_generation_vs_tool_time.csv"))
pd.set_option("display.width", 220)
print(split.round(3).to_string())
print(T[["share_of_time", "share_of_output", "gen_s_per_call", "tool_s_per_call", "calls"]].astype(float).round(3).to_string())
# check against wall clock
w = R.set_index("task_id").duration_s
chk = D.groupby("task_id")[["gen_s", "tool_s"]].sum().sum(axis=1) / w.reindex(D.task_id.unique())
print("measured (gen+tool) / wall clock: median %.2f  range %.2f-%.2f" % (chk.median(), chk.min(), chk.max()))
