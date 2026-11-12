"""Round 1 — build the audited master table for efficiency analysis.

Reads one benchmark batch directory (summary.csv, task-metrics.csv, scoring-results.csv and
the per-run folders) and writes, under <out_dir>:

  runs.csv            one row per model x task record, with raw metrics, trajectory-derived
                      behaviour features, PER-METRIC validity labels and review flags
  attempts.csv        one row per trajectory file (a run may have several attempts)
  tool_errors.csv     one row per failed tool call, with an automatic cause guess
  error_signatures.csv  failed-call messages grouped by signature (for taxonomy review)
  review_queue.csv    runs flagged needs_review, with empty verdict columns for a human;
                      verdicts already filled in are preserved when the script is re-run

Principles (from anay_skills.md):
  * nothing is deleted here; rows are labelled, and validity is per metric, not per run
  * detection (needs_review) is separate from exclusion (a human verdict in review_queue.csv)
  * model-caused inefficiency stays in; only evidence of external contamination can exclude

Usage: python3 -I build_master.py <batch_dir> <out_dir>
"""
import collections
import csv
import glob
import hashlib
import json
import math
import os
import re
import statistics
import sys

BATCH = sys.argv[1]
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)

# shared parsing code lives next to this file; -I keeps the script directory off sys.path
import importlib.util
_spec = importlib.util.spec_from_file_location("trajfeat", os.path.join(os.path.dirname(os.path.abspath(__file__)), "trajfeat.py"))
_tf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_tf)
globals().update({k: v for k, v in vars(_tf).items() if not k.startswith("__")})

# --------------------------------------------------------------------------- load batch

summary = read_csv(os.path.join(BATCH, "summary.csv"))
tm = {r["id"]: r for r in read_csv(os.path.join(BATCH, "task-metrics.csv"))}
sr = collections.defaultdict(list)
for r in read_csv(os.path.join(BATCH, "scoring-results.csv")):
    sr[r["task_id"]].append(r)

runs, attempts, tool_errors = [], [], []

for s in summary:
    tid = s["task_id"]
    d = os.path.join(BATCH, s["cohort"], tid)
    t = tm.get(tid, {})
    metrics = load_json(os.path.join(d, "inference-metrics.json")) or {}
    meta = load_json(os.path.join(d, "meta.json")) or {}
    score = load_json(os.path.join(d, "score.json")) or {}
    screen = load_json(os.path.join(d, "screen-count-check.json")) or {}

    row = {
        "task_id": tid, "problem": s["title"], "model": s["model_name"], "model_id": s["model_id"],
        "source_folder": s["cohort"],  # provenance only; never used as an analysis factor
        "harness_status": s["inference_status"], "failure_category": s["failure_category"],
        "failure_reason": t.get("failure_reason", ""),
        "termination_reason": t.get("termination_reason", ""),
        "started_at": s["started_at"], "finished_at": s["inference_finished_at"],
        "timeout_seconds": num(t.get("inference_timeout_seconds")),
        "duration_s": num(s["inference_duration_seconds"]),
        "current_attempt_duration_s": num(t.get("current_attempt_duration_seconds")),
        "continuation_count": num(t.get("continuation_count")),
        "input_tokens": num(s["input_tokens"]), "output_tokens": num(s["output_tokens"]),
        "total_tokens": num(s["total_tokens"]),
        "token_usage_status": s["token_usage_status"],
        "expected_frames": num(s["expected_frames"]), "actual_frames": num(s["actual_frames"]),
        "white_screen_check_status": t.get("white_screen_check_status", ""),
        "white_screen_count": num(t.get("white_screen_count")),
        "account": t.get("account", ""), "actual_account": t.get("actual_account", ""),
        "score_status": s["score_status"], "score_total": num(s["score_total"]),
        "g0_pass": s["g0_pass"],
        "n_score_revisions_other": len(meta.get("other_score_revisions") or []),
        "judge_model": score.get("judge_model", ""), "rubric_hash": (score.get("rubric_hash") or "")[:12],
        "score_trace_status": score.get("trace_status", ""),
        "score_candidate_inference_status": (score.get("candidate") or {}).get("inference_status", ""),
        "score_candidate_finished_at": (score.get("candidate") or {}).get("finished_at", ""),
        "score_candidate_actual_frames": (score.get("candidate") or {}).get("actual", ""),
        "screen_check_expected": screen.get("expected", ""), "screen_check_actual": screen.get("actual", ""),
        "screen_check_passed": screen.get("passed", ""),
        # first-attempt metrics file (NOT the run total when a run has several attempts)
        "mfile_input_tokens": metrics.get("input_tokens"), "mfile_output_tokens": metrics.get("output_tokens"),
        "mfile_cached_input_tokens": metrics.get("cached_input_tokens"),
        "mfile_cache_creation_tokens": metrics.get("cache_creation_input_tokens"),
        "mfile_duration_s": metrics.get("inference_duration_seconds"),
        "mfile_api_calls": metrics.get("api_usage_calls"),
        "mfile_api_unknown_calls": metrics.get("api_usage_unknown_calls"),
        "mfile_token_usage_status": metrics.get("token_usage_status"),
        "mfile_token_source": metrics.get("token_usage_source"),
    }
    for k, v in (score.get("values") or {}).items():
        row[f"rubric_{k}"] = v

    # ---- trajectories (all attempts)
    files = sorted(glob.glob(os.path.join(d, "trajectory*.jsonl")), key=os.path.getmtime)
    seen_ids = set()
    agg = collections.Counter()
    a_rows = []
    for f in files:
        arow, erows, ids = parse_attempt(f)
        overlap = len(ids & seen_ids) / len(ids) if ids else 0.0
        arow["call_id_overlap_with_earlier"] = round(overlap, 3)
        seen_ids |= ids
        arow.update({"task_id": tid, "problem": s["title"], "model": s["model_name"]})
        a_rows.append(arow)
        for e in erows:
            e.update({"task_id": tid, "problem": s["title"], "model": s["model_name"]})
            tool_errors.append(e)
    # The judged artifact lives in one Figma file. Restarts sometimes ran on a fresh copy, so only
    # attempts that worked on the judged file are part of the cost of the judged result.
    scored_key = (score.get("candidate") or {}).get("file_key") or ""
    for a in a_rows:
        a["on_scored_file"] = (a.get("file_key") == scored_key) if scored_key else ""
    keep = [a for a in a_rows if a["on_scored_file"] is True] if scored_key else list(a_rows)
    if scored_key and not keep:
        keep = list(a_rows)           # judged file not among packaged trajectories: keep all, flag below
    for a in a_rows:
        a["counted_in_run_totals"] = a in keep
    for a in keep:
        for k in SUM_FIELDS:
            agg[k] += a.get(k) or 0
    # Split the run's reported tokens between attempts. Output usage per attempt is reliable; input
    # usage inside a trajectory omits cache reads for some API formats, so when it does not add up
    # to the reported input total, input is apportioned by each attempt's context size instead.
    tot_in, tot_out = num(s["input_tokens"]), num(s["output_tokens"])
    u_in = sum(a.get("usage_input_tokens") or 0 for a in a_rows)
    u_out = sum(a.get("usage_output_tokens") or 0 for a in a_rows)
    carry_all = sum(a.get("carry_chars_total") or 0 for a in a_rows)
    exact_in = bool(tot_in and u_in and abs(u_in - tot_in) / tot_in < 0.02)
    for a in a_rows:
        ao = a.get("usage_output_tokens") or 0
        a["est_output_tokens"] = (tot_out * ao / u_out) if (tot_out and u_out) else ""
        if tot_in is None:
            a["est_input_tokens"] = ""
        elif exact_in:
            a["est_input_tokens"] = a.get("usage_input_tokens") or 0
        elif carry_all:
            a["est_input_tokens"] = tot_in * (a.get("carry_chars_total") or 0) / carry_all
        else:
            a["est_input_tokens"] = ""
    split_ok = bool(a_rows) and all(a["est_input_tokens"] != "" and a["est_output_tokens"] != "" for a in a_rows)
    if split_ok:
        row["tokens_scored_file"] = sum(a["est_input_tokens"] + a["est_output_tokens"] for a in keep)
        row["output_tokens_scored_file"] = sum(a["est_output_tokens"] for a in keep)
    else:
        row["tokens_scored_file"] = num(s["total_tokens"]) if len(a_rows) <= 1 else None
        row["output_tokens_scored_file"] = tot_out if len(a_rows) <= 1 else None
    row["token_split_method"] = ("single_attempt" if len(a_rows) <= 1 else
                                 "exact_per_attempt_usage" if exact_in else
                                 "input_apportioned_by_context_size" if split_ok else "not_possible")
    row["scored_file_key"] = scored_key
    row["n_attempts_other_file"] = len(a_rows) - len(keep)
    row["scored_file_in_trajectories"] = (any(a["on_scored_file"] is True for a in a_rows) if scored_key else "")
    attempts.extend(a_rows)

    row["n_trajectory_files"] = len(files)
    row["n_attempts_counted"] = len(keep)
    row["attempt_kinds"] = "+".join(a["attempt_kind"] for a in a_rows)
    row["file_keys_in_attempts"] = "|".join(sorted({a.get("file_key", "") for a in a_rows if a.get("file_key")}))
    row["traj_usage_input_sum"] = u_in if a_rows else None
    row["traj_usage_output_sum"] = u_out if a_rows else None
    row["requested_effort"] = "|".join(sorted({str(a.get("requested_effort")) for a in keep})) if keep else ""
    row["enable_thinking"] = "|".join(sorted({str(a.get("enable_thinking")) for a in a_rows})) if a_rows else ""
    row["api_model"] = "|".join(sorted({str(a.get("api_model")) for a in a_rows})) if a_rows else ""
    row["api_format"] = "|".join(sorted({str(a.get("api_format")) for a in a_rows})) if a_rows else ""
    row["traj_final_status"] = a_rows[-1].get("traj_status", "") if a_rows else ""
    row["ended_with_text_answer"] = a_rows[-1].get("ended_with_text_answer", "") if a_rows else ""
    row["max_error_streak"] = max((a.get("max_error_streak") or 0 for a in a_rows), default="")
    row["largest_result_chars"] = max((a.get("largest_result_chars") or 0 for a in a_rows), default="")
    for k in SUM_FIELDS:
        row[k] = agg[k] if keep else ""
    runs.append(row)

# --------------------------------------------------------------------------- audit labels

by_problem = collections.defaultdict(list)
for r in runs:
    by_problem[r["problem"]].append(r)


def median(vals):
    vals = [v for v in vals if v is not None]
    return statistics.median(vals) if vals else None


def task_tok(r):
    return r["tokens_scored_file"] if r.get("tokens_scored_file") is not None else r["total_tokens"]


problem_median_tokens = {p: median([task_tok(r) for r in rs if r["harness_status"] in ("success", "failed")])
                         for p, rs in by_problem.items()}
problem_median_dur = {p: median([r["duration_s"] for r in rs]) for p, rs in by_problem.items()}
tok_sorted = sorted(task_tok(r) for r in runs if task_tok(r))
dur_sorted = sorted(r["duration_s"] for r in runs if r["duration_s"])
p95_tok = tok_sorted[int(0.95 * (len(tok_sorted) - 1))] if tok_sorted else None
p95_dur = dur_sorted[int(0.95 * (len(dur_sorted) - 1))] if dur_sorted else None

# chars-per-token consistency: reported input tokens vs what the trajectory text implies
ratios = collections.defaultdict(list)
for r in runs:
    if r["carry_chars_total"] and r["input_tokens"] and r["harness_status"] in ("success", "failed"):
        r["carry_chars_per_input_token"] = round(r["carry_chars_total"] / r["input_tokens"], 3)
        ratios[r["model"]].append(r["carry_chars_per_input_token"])
    else:
        r["carry_chars_per_input_token"] = ""
model_ratio_med = {m: statistics.median(v) for m, v in ratios.items() if v}

for r in runs:
    hs = r["harness_status"]
    fc = r["failure_category"]
    timeout = r["timeout_seconds"] or 5400.0
    has_tokens = r["total_tokens"] is not None
    has_time = r["duration_s"] is not None
    scored = r["score_status"] == "completed" and r["score_total"] is not None
    cont = r["continuation_count"] or 0
    multi = r["n_trajectory_files"] > 1 or cont > 0

    # 1. lifecycle
    if hs in ("pending", "preparing_copy", "deferred"):
        life = "not_run"
    elif hs == "running":
        life = "in_progress"
    else:
        life = "finished"
    r["lifecycle"] = life

    # 2. what a harness "failed" actually means
    if hs == "success":
        outcome = "delivered"
    elif hs != "failed":
        outcome = life
    elif fc == "white_screen_check":
        no_frames = (r["actual_frames"] or 0) == 0
        outcome = "checker_error_no_frames" if no_frames else "delivered_checker_error"
    elif fc == "blank_screen":
        outcome = "blank_output"
    elif fc == "screen_count":
        outcome = "screen_count_mismatch"
    elif fc == "inference_timeout":
        outcome = "timeout_partial"
    else:
        outcome = "failed_unknown"
    r["outcome_class"] = outcome

    hit_limit = (r["termination_reason"] == "inference_time_limit" or fc == "inference_timeout"
                 or (has_time and r["duration_s"] >= 0.98 * timeout))
    r["hit_time_limit"] = hit_limit
    r["budget_multiple"] = round(r["duration_s"] / timeout, 2) if has_time else ""

    # 3. per-metric validity (ok / caveat:<why> / unusable:<why>)
    if not scored:
        q = "unusable:no_score" if life == "finished" else f"unusable:{life}"
    elif life == "in_progress":
        q = "caveat:scored_while_still_running"
    elif r["n_score_revisions_other"]:
        q = "caveat:multiple_score_revisions"
    else:
        q = "ok"
    r["quality_validity"] = q

    if not has_tokens:
        tk = "unusable:missing"
    elif life == "in_progress":
        tk = "unusable:in_progress"
    elif r["tokens_scored_file"] is None:
        tk = "caveat:cannot_separate_other_file_attempts"
    elif r["token_usage_status"] == "partial":
        tk = "caveat:partial_lower_bound"
    elif r["token_usage_status"] != "reported":
        tk = f"caveat:{r['token_usage_status'] or 'status_missing'}"
    else:
        tk = "ok"
    r["tokens_validity"] = tk

    if not has_time:
        tv = "unusable:missing" if life == "finished" else f"unusable:{life}"
    elif r["n_attempts_other_file"]:
        tv = "caveat:includes_attempts_on_other_file"
    elif hit_limit:
        tv = "caveat:censored_at_time_limit"
    elif multi:
        tv = "caveat:summed_over_attempts"
    else:
        tv = "ok"
    r["time_validity"] = tv

    od_ = (abs(r["traj_usage_output_sum"] - r["output_tokens"]) / r["output_tokens"]
           if (r["output_tokens"] and r["traj_usage_output_sum"]) else 0)
    r["trajectory_validity"] = ("unusable:no_trajectory" if not r["n_trajectory_files"] else
                                "caveat:judged_file_not_in_packaged_trajectories" if r["scored_file_in_trajectories"] is False else
                                "caveat:trajectory_incomplete" if od_ > 0.10 else "ok")
    r["tokens_other_files"] = (r["total_tokens"] - r["tokens_scored_file"]
                               if (has_tokens and r["tokens_scored_file"] is not None) else "")

    # 4. infrastructure incidents (evidence, not verdicts)
    inc = []
    if outcome in ("delivered_checker_error", "checker_error_no_frames"):
        inc.append("screen_checker_failed")
    if r["account"] and r["actual_account"] and r["account"] != r["actual_account"]:
        inc.append("account_switched")
    if "restart" in r["attempt_kinds"] or "resume" in r["attempt_kinds"]:
        inc.append("batch_restart_or_resume")
    if cont > 0 or "continuation" in r["attempt_kinds"]:
        inc.append("continued_after_time_limit")
    if r["tool_errors_infra"]:
        inc.append(f"infra_tool_errors={r['tool_errors_infra']}")
    if r["n_attempts_other_file"]:
        inc.append("restart_ran_on_a_different_file")
    r["infra_incidents"] = ";".join(inc)

    # 5. exploratory review flags (thresholds only locate cases; they never delete)
    fl = []
    pm = problem_median_tokens.get(r["problem"])
    if has_tokens and pm and task_tok(r) > 3 * pm:
        fl.append("tokens_gt_3x_problem_median")
    if has_tokens and p95_tok and task_tok(r) >= p95_tok:
        fl.append("tokens_top5pct")
    if has_time and p95_dur and r["duration_s"] >= p95_dur:
        fl.append("duration_top5pct")
    if r["tool_calls_answered"] and r["tool_calls_answered"] >= 10 and r["tool_errors"] / r["tool_calls_answered"] > 0.3:
        fl.append("tool_error_rate_gt_30pct")
    if r["max_error_streak"] != "" and r["max_error_streak"] >= 5:
        fl.append("error_streak_ge_5")
    if r["tool_errors_infra"]:
        fl.append("infra_tool_errors")
    if r["tool_errors_unknown"] and r["tool_errors_unknown"] >= 3:
        fl.append("unclassified_tool_errors")
    if hit_limit:
        fl.append("hit_time_limit")
    if outcome in ("checker_error_no_frames", "failed_unknown"):
        fl.append(outcome)
    if q.startswith("caveat"):
        fl.append(q.split(":")[1])
    if scored and r["g0_pass"] == "False":
        fl.append("g0_fail_score_zero")
    # Informational only: the usage block inside a trajectory excludes cache reads for some API
    # formats, while summary.csv counts every prompt token once, so the two legitimately differ.
    if has_tokens and r["traj_usage_input_sum"] and r["input_tokens"]:
        r["traj_usage_input_over_summary_input"] = round(r["traj_usage_input_sum"] / r["input_tokens"], 3)
    else:
        r["traj_usage_input_over_summary_input"] = ""
    # Output tokens have no cache ambiguity, so a gap here means attempts are missing or double counted.
    if r["output_tokens"] and r["traj_usage_output_sum"]:
        od = abs(r["traj_usage_output_sum"] - r["output_tokens"]) / r["output_tokens"]
        r["traj_vs_summary_output_token_diff"] = round(od, 3)
        if od > 0.10:
            fl.append("summary_output_tokens_ne_trajectory_sum")
    else:
        r["traj_vs_summary_output_token_diff"] = ""
    mr = model_ratio_med.get(r["model"])
    if r["carry_chars_per_input_token"] != "" and mr:
        ratio = r["carry_chars_per_input_token"] / mr
        if ratio > 2 or ratio < 0.5:
            fl.append("token_count_inconsistent_with_trajectory_text")
    if r["n_attempts_other_file"]:
        fl.append("restart_ran_on_a_different_file")
    if r["trajectory_validity"].startswith("caveat"):
        fl.append(r["trajectory_validity"].split(":")[1])
    r["review_flags"] = ";".join(fl)
    r["needs_review"] = bool(fl)

    # 6. automatic first-pass audit status (a human verdict in review_queue.csv overrides it)
    if life != "finished":
        st = "excluded_not_finished"
    elif not r["needs_review"]:
        st = "clean"
    else:
        st = "flagged_pending_review"
    r["audit_status_auto"] = st

# --------------------------------------------------------------------------- write


def write_csv(path, rows, first=()):
    keys = list(first)
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in keys})


LEAD = ["task_id", "problem", "model", "harness_status", "outcome_class", "lifecycle", "audit_status_auto",
        "quality_validity", "tokens_validity", "time_validity", "trajectory_validity",
        "needs_review", "review_flags", "infra_incidents",
        "score_total", "g0_pass", "tokens_scored_file", "tokens_other_files", "total_tokens", "input_tokens", "output_tokens", "duration_s",
        "budget_multiple", "hit_time_limit", "tool_calls", "tool_errors", "tool_errors_model",
        "tool_errors_infra", "tool_errors_unknown", "assistant_turns", "requested_effort"]
write_csv(os.path.join(OUT, "runs.csv"), runs, LEAD)
for a in attempts:
    a.pop("mtime", None)
write_csv(os.path.join(OUT, "attempts.csv"), attempts,
          ["task_id", "problem", "model", "trajectory_file", "attempt_kind", "on_scored_file", "counted_in_run_totals",
           "est_input_tokens", "est_output_tokens", "requested_effort",
           "call_id_overlap_with_earlier", "traj_status", "total_steps", "usage_input_tokens",
           "usage_output_tokens", "file_key", "tool_calls", "tool_errors"])
write_csv(os.path.join(OUT, "tool_errors.csv"), tool_errors,
          ["task_id", "problem", "model", "trajectory_file", "call_index", "tool", "call_category",
           "auto_cause", "auto_kind", "signature", "message_head"])

sig = collections.defaultdict(lambda: {"count": 0, "runs": set(), "models": collections.Counter(), "example": ""})
for e in tool_errors:
    k = (e["auto_cause"], e["auto_kind"], e["signature"])
    sig[k]["count"] += 1
    sig[k]["runs"].add(e["task_id"])
    sig[k]["models"][e["model"]] += 1
    sig[k]["example"] = sig[k]["example"] or e["message_head"]
sig_rows = [{"auto_cause": k[0], "auto_kind": k[1], "signature": k[2], "count": v["count"],
             "n_runs": len(v["runs"]),
             "models": "; ".join(f"{m}={c}" for m, c in v["models"].most_common()),
             "example": v["example"]}
            for k, v in sorted(sig.items(), key=lambda kv: -kv[1]["count"])]
write_csv(os.path.join(OUT, "error_signatures.csv"), sig_rows)

# review queue: keep any human verdicts that already exist
rq_path = os.path.join(OUT, "review_queue.csv")
old = {}
if os.path.exists(rq_path):
    for r in read_csv(rq_path):
        old[r["task_id"]] = r
HUMAN = ["verdict_cause", "exclude_tokens", "exclude_time", "exclude_quality", "reviewer", "review_notes"]
rq = []
for r in runs:
    if not r["needs_review"]:
        continue
    q = {k: r.get(k) for k in ["task_id", "problem", "model", "outcome_class", "review_flags", "infra_incidents",
                               "score_total", "tokens_scored_file", "tokens_other_files", "total_tokens", "duration_s", "budget_multiple", "tool_calls",
                               "tool_errors", "tool_errors_model", "tool_errors_infra", "tool_errors_unknown",
                               "max_error_streak", "attempt_kinds"]}
    pm = problem_median_tokens.get(r["problem"])
    q["tokens_x_problem_median"] = round(task_tok(r) / pm, 2) if (pm and task_tok(r)) else ""
    for h in HUMAN:
        q[h] = old.get(r["task_id"], {}).get(h, "")
    rq.append(q)
rq.sort(key=lambda q: -(q["tokens_x_problem_median"] or 0))
write_csv(rq_path, rq)

# --------------------------------------------------------------------------- console summary
c = collections.Counter
print(f"runs: {len(runs)}   problems: {len(by_problem)}   models: {len({r['model'] for r in runs})}")
print("trajectory files:", len(attempts), "  failed tool calls:", len(tool_errors))
for col in ["lifecycle", "outcome_class", "quality_validity", "tokens_validity", "time_validity",
            "trajectory_validity", "audit_status_auto", "requested_effort", "attempt_kinds"]:
    print(f"\n[{col}]")
    for k, v in c(r[col] for r in runs).most_common():
        print(f"  {v:4d}  {k}")
print("\n[review flags]")
for k, v in c(f for r in runs for f in r["review_flags"].split(";") if f).most_common():
    print(f"  {v:4d}  {k}")
print("\n[infra incidents]")
for k, v in c(re.sub(r"=\d+", "", f) for r in runs for f in r["infra_incidents"].split(";") if f).most_common():
    print(f"  {v:4d}  {k}")
print("\n[tool error auto cause/kind]")
for k, v in c((e["auto_cause"], e["auto_kind"]) for e in tool_errors).most_common():
    print(f"  {v:5d}  {k}")
print("\n[top unknown signatures]")
for s_ in [s for s in sig_rows if s["auto_cause"] == "unknown"][:25]:
    print(f"  {s_['count']:4d}  {s_['signature']}")
