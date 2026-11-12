"""Bring the earlier 29-problem package (benchmark_output) onto the same token definition as the
246-record batch, so the two can sit in one table.

Token definition used for both: every prompt token of every model request is counted once
(fresh + cache-read + cache-write), plus all output tokens, for the run that produced the judged
file. Providers report cached tokens two ways (inside input_tokens, or beside it); this script
detects which per run from the per-request usage and normalises.

Writes <out_dir>/runs_old.csv (same key columns as runs.csv, protocol = "v1_screenshot_cc").

Usage: python3 -I build_old.py <benchmark_output_dir> <out_dir>
"""
import collections
import csv
import json
import os
import sqlite3
import sys

PKG, OUT = sys.argv[1], sys.argv[2]
import importlib.util
_spec = importlib.util.spec_from_file_location("trajfeat", os.path.join(os.path.dirname(os.path.abspath(__file__)), "trajfeat.py"))
tf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tf)
tool_errors = []
TIME_LIMIT = 5400.0


def connect(path):
    return sqlite3.connect(f"file:{os.path.join(PKG, path)}?immutable=1", uri=True)


index = list(csv.DictReader(open(os.path.join(PKG, "metadata/portable_run_index.csv"), encoding="utf-8-sig")))
scores, run_status = {}, {}
for db in sorted({r["round_db"] for r in index}):
    con = connect(db)
    for rid, status, total, g0, method, judge, vals in con.execute(
            "select run_id,status,total,g0_pass,method,eval_model_id,cc_values from scale_scores order by updated_at"):
        scores[rid] = dict(status=status, total=total, g0=g0, method=method, judge=judge,
                           items=json.loads(vals) if vals else {})
    for rid, status, started, finished, turns in con.execute("select id,status,started_at,finished_at,turn_count from runs"):
        run_status[rid] = dict(status=status, started=started, finished=finished)

rows = []
for r in index:
    rid = r["run_id"]
    row = {"task_id": rid, "problem": r["title"], "model": r["model"], "protocol": "v1_screenshot_cc",
           "source_folder": "old:" + r["round"], "lifecycle": "finished", "n_trajectory_files": 1,
           "n_attempts_other_file": 0, "exclude_note": ""}
    con = connect(r["trace_sqlite"])
    cols = {c[1] for c in con.execute("pragma table_info(sessions)")}
    sessions = con.execute("select summary_json, started_at, updated_at from sessions").fetchall()
    tables = {t[0] for t in con.execute("select name from sqlite_master where type='table'")}
    prompt = out = 0
    n_req = n_no_usage = n_cached = n_inclusive = 0
    raw_in = raw_read = raw_create = 0
    api_models = collections.Counter()
    if "records" in tables:
        per = []
        for (p,) in con.execute("select payload_json from records order by record_index"):
            j = json.loads(p)
            rec = j.get("record", j)
            body = (rec.get("response") or {}).get("body") or {}
            u = body.get("usage") if isinstance(body, dict) else None
            n_req += 1
            m = ((rec.get("request") or {}).get("body") or {}).get("model")
            if m:
                api_models[m] += 1
            if not u:
                n_no_usage += 1
                continue
            i = u.get("input_tokens") or 0
            rd = u.get("cache_read_input_tokens") or 0
            cr = u.get("cache_creation_input_tokens") or 0
            per.append((i, rd, cr, u.get("output_tokens") or 0))
            if rd + cr > 0:
                n_cached += 1
                n_inclusive += int(i >= rd + cr)
        # a provider is "inclusive" if its input_tokens already contains the cached part
        inclusive = n_cached > 0 and n_inclusive / n_cached >= 0.9
        for i, rd, cr, o in per:
            prompt += i if inclusive else i + rd + cr
            out += o
            raw_in += i
            raw_read += rd
            raw_create += cr
        row["cache_reporting"] = "inside_input_tokens" if inclusive else ("beside_input_tokens" if n_cached else "no_cache_reported")
    else:  # direct runner: one summary with OpenAI-style totals (input already includes cached)
        for sj, _, _ in sessions:
            s = json.loads(sj)
            prompt += s.get("input_tokens") or 0
            out += s.get("output_tokens") or 0
            n_req += s.get("turn_count") or 0
            api_models[s.get("model")] += 1
        row["cache_reporting"] = "summary_only_inside_input_tokens"
    summ = [json.loads(s[0]) for s in sessions if s[0]]
    dur = sum((s.get("duration_ms") or 0) for s in summ) / 1000.0
    if sessions:   # wall clock of the session; the summary's duration_ms can be request time only
        from datetime import datetime
        f = lambda t: datetime.fromisoformat(t.replace("Z", "+00:00"))
        dur = max(dur, sum((f(s[2]) - f(s[1])).total_seconds() for s in sessions))
    sc = scores.get(rid, {})
    scored = sc.get("status") == "已完成" and sc.get("total") is not None
    rs = run_status.get(rid, {})
    hit = dur >= 0.98 * TIME_LIMIT
    row.update({
        "harness_status": rs.get("status", ""), "outcome_class": "delivered" if scored else "no_score",
        "input_tokens": prompt, "output_tokens": out, "total_tokens": prompt + out,
        "tokens_scored_file": prompt + out, "output_tokens_scored_file": out, "tokens_other_files": 0,
        "trace_summary_total_tokens": sum((s.get("total_tokens") or 0) for s in summ),
        "raw_input_tokens": raw_in, "raw_cache_read": raw_read, "raw_cache_create": raw_create,
        "duration_s": round(dur, 3), "hit_time_limit": hit, "budget_multiple": round(dur / TIME_LIMIT, 2),
        "assistant_turns": n_req, "api_requests_without_usage": n_no_usage,
        "api_model": "|".join(k for k in api_models if k), "n_sessions": len(sessions),
        "score_total": sc.get("total") if scored else "", "g0_pass": bool(sc.get("g0")) if scored else "",
        "judge_model": sc.get("judge", ""), "score_method": sc.get("method", ""),
        "requested_effort": "not_set",
        **({f"rubric_{k}": v for k, v in sc.get("items", {}).items()} if scored else {}),
        "quality_validity": "ok" if scored else "unusable:no_score",
        "tokens_validity": ("unusable:missing" if not prompt else
                            "caveat:partial_lower_bound" if n_no_usage else "ok"),
        "time_validity": "caveat:censored_at_time_limit" if hit else "ok",
        "trajectory_validity": "ok",
        "needs_review": False, "review_flags": "", "infra_incidents": "",
    })
    # behaviour features from the trajectory, with the same parser as the new batch
    tp = os.path.join(PKG, r["trajectory_path"])
    if os.path.exists(tp):
        arow, erows, _ = tf.parse_attempt(tp)
        for k in tf.SUM_FIELDS + ["max_error_streak", "largest_result_chars", "ended_with_text_answer"]:
            if k != "assistant_turns":
                row[k] = arow.get(k, "")
        row["trajectory_turns"] = arow.get("assistant_turns", "")
        for e in erows:
            e.update({"task_id": rid, "problem": r["title"], "model": r["model"]})
            tool_errors.append(e)
        if not arow.get("tool_calls"):
            row["trajectory_validity"] = "unusable:no_tool_calls_parsed"
    else:
        row["trajectory_validity"] = "unusable:no_trajectory"
    rows.append(row)

ekeys = ["task_id", "problem", "model", "trajectory_file", "call_index", "tool", "call_category",
         "auto_cause", "auto_kind", "signature", "message_head"]
with open(os.path.join(OUT, "tool_errors_old.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=ekeys, extrasaction="ignore")
    w.writeheader()
    w.writerows(tool_errors)

keys = []
for r in rows:
    for k in r:
        if k not in keys:
            keys.append(k)
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "runs_old.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=keys)
    w.writeheader()
    w.writerows(rows)

c = collections.Counter
print("old runs:", len(rows), " scored:", sum(1 for r in rows if r["score_total"] != ""))
print("cache reporting by model:")
for k, v in sorted(c((r["model"], r["cache_reporting"]) for r in rows).items()):
    print(f"  {v:3d}  {k}")
print("tokens_validity:", dict(c(r["tokens_validity"] for r in rows)))
print("hit time limit:", sum(r["hit_time_limit"] for r in rows), " multi-session:", sum(r["n_sessions"] > 1 for r in rows))
print("trace summary total / normalised total (median by model):")
by = collections.defaultdict(list)
for r in rows:
    if r["total_tokens"] and r["trace_summary_total_tokens"]:
        by[r["model"]].append(r["trace_summary_total_tokens"] / r["total_tokens"])
for m, v in by.items():
    v.sort()
    print(f"  {m}: median {v[len(v)//2]:.2f}  range {v[0]:.2f}-{v[-1]:.2f}")
print("api models:", dict(c((r["model"], r["api_model"]) for r in rows)))
print("trajectory_validity:", dict(c(r["trajectory_validity"] for r in rows)))
print("failed tool calls:", len(tool_errors), dict(c((e["auto_cause"], e["auto_kind"]) for e in tool_errors).most_common(12)))
print("top unknown:", c(e["signature"] for e in tool_errors if e["auto_cause"] == "unknown").most_common(12))
mm = [(r["assistant_turns"], r["trajectory_turns"]) for r in rows if r.get("trajectory_turns") not in ("", None)]
print("api requests == trajectory turns:", sum(a == b for a, b in mm), "of", len(mm))
