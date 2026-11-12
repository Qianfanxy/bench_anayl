"""Round 2 — efficiency analyses on the audited master table (out/runs.csv).

All problems are treated as one flat set of equal units: no grouping by platform, category or
source folder. Because models cover different numbers of problems, every comparison is either
(a) problem-matched (pairwise, on the problems both models did) or (b) a two-way additive model
with one effect per model and one per problem, with uncertainty from resampling problems.

Writes CSV tables under <out_dir>/tables and a generated <out_dir>/report.md.

Usage: python3 -I analyze.py <out_dir> [score_tolerance=3] [bootstrap_reps=2000]
"""
import itertools
import os
import sys

import numpy as np
import pandas as pd

OUT = sys.argv[1]
DELTA = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0   # score gap treated as judge noise
REPS = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
TAB = os.path.join(OUT, "tables")
os.makedirs(TAB, exist_ok=True)
rng = np.random.default_rng(20261111)

runs = pd.read_csv(os.path.join(OUT, "runs.csv"), keep_default_na=False, na_values=[""])
NEW_PROTOCOL = "v2_no_screenshot_direct"
runs["protocol"] = NEW_PROTOCOL
old_path = os.path.join(OUT, "runs_old.csv")
HAS_OLD = os.path.exists(old_path) and os.environ.get("EFF_NEW_ONLY") != "1"
if HAS_OLD:
    old = pd.read_csv(old_path, keep_default_na=False, na_values=[""])
    old = old[old.model.isin(set(runs.model))]          # only models that also exist in this batch
    runs = pd.concat([runs, old], ignore_index=True)
    runs["needs_review"] = runs.needs_review.fillna(False)
    runs["hit_time_limit"] = runs.hit_time_limit.fillna(False)
# comparisons "on the same problem" are only made between runs under the same protocol
runs["cell"] = runs.problem + " @ " + runs.protocol
rq_path = os.path.join(OUT, "review_queue.csv")
rq = pd.read_csv(rq_path) if os.path.exists(rq_path) else pd.DataFrame()

# --------------------------------------------------------------------------- inclusion sets
# Human verdicts (review_queue.csv) are the only route to excluding a finished, measured run
# from the primary set, apart from records whose measured object is demonstrably not the final
# artifact / not a finished run.
for col in ["exclude_tokens", "exclude_time", "exclude_quality"]:
    runs[col] = False
if len(rq):
    for col in ["exclude_tokens", "exclude_time", "exclude_quality"]:
        if col in rq:
            ids = rq.loc[rq[col].astype(str).str.lower().isin(["1", "true", "yes", "y"]), "task_id"]
            runs.loc[runs.task_id.isin(ids), col] = True

fin = runs.lifecycle.eq("finished")
q_ok = fin & runs.quality_validity.isin(["ok", "caveat:multiple_score_revisions"]) & ~runs.exclude_quality
t_ok = fin & ~runs.tokens_validity.str.startswith("unusable") & ~runs.exclude_tokens
d_ok = fin & ~runs.time_validity.str.startswith("unusable") & ~runs.exclude_time
artifact_uncertain = runs.outcome_class.isin(["checker_error_no_frames", "failed_unknown"])
runs["g0_pass"] = runs.g0_pass.astype(str)

SETS = {
    # finished runs; partial token counts kept as lower bounds; model-caused failures kept
    "primary": dict(q=q_ok & ~artifact_uncertain, tok=t_ok, dur=d_ok),
    # everything that has a number, including still-running snapshots
    "all_measurable": dict(q=runs.score_total.notna(), tok=runs.tokens_scored_file.notna(), dur=runs.duration_s.notna()),
    # single-attempt runs with complete token accounting that ended on their own
    "strict_clean": dict(
        q=q_ok & ~artifact_uncertain,
        tok=t_ok & runs.tokens_validity.eq("ok") & runs.n_trajectory_files.le(1) & ~runs.hit_time_limit.astype(bool),
        dur=d_ok & runs.time_validity.eq("ok")),
}
# "tokens" = tokens spent by attempts that worked on the judged file (the cost of the judged result);
# "tokens_all_attempts" = what summary.csv reports, including restarts that ran on another file.
COSTS = {"tokens": ("tokens_scored_file", "tok"), "tokens_all_attempts": ("total_tokens", "tok"),
         "output_tokens": ("output_tokens_scored_file", "tok"),
         "time": ("duration_s", "dur"), "tool_calls": ("tool_calls", "tok")}


def subset(set_name, cost=None, need_score=True):
    s = SETS[set_name]
    m = pd.Series(True, index=runs.index)
    if need_score:
        m &= s["q"]
    if cost:
        col, key = COSTS[cost]
        m &= s[key] & runs[col].notna() & (runs[col] > 0)
    return runs[m].copy()


models = sorted(runs.model.unique())
for c_ in ["tool_calls", "tool_errors", "tool_calls_answered"]:
    if c_ not in runs:
        runs[c_] = np.nan
problems = sorted(runs.problem.unique())
lines = []


def md(text=""):
    lines.append(text)


def md_table(df, floatfmt="{:.2f}"):
    df = df.copy()
    for c in df.columns:
        if pd.api.types.is_float_dtype(df[c]):
            df[c] = df[c].map(lambda v: "" if pd.isna(v) else floatfmt.format(v))
    md("| " + " | ".join(str(c) for c in df.columns) + " |")
    md("|" + "|".join("---" for _ in df.columns) + "|")
    for _, row in df.iterrows():
        md("| " + " | ".join(str(v) for v in row.values) + " |")
    md()


def save(df, name, index=False):
    df.to_csv(os.path.join(TAB, name), index=index)


# --------------------------------------------------------------------------- 0. coverage & audit
md("# Efficiency analysis report (generated)")
md()
md(f"Records: {len(runs)} (model x problem x protocol), {len(problems)} problems, {len(models)} models"
   + (f"; {int((runs.protocol != NEW_PROTOCOL).sum())} records come from the earlier package. " if HAS_OLD else ". ") +
   f"Problems are a flat set; no categories are used. Score tolerance for 'same quality': {DELTA:g} points.")
md()
md("## 0. Coverage and data audit")
md()
cov = runs.groupby(["model", "protocol"]).agg(
    records=("task_id", "size"),
    problems=("problem", "nunique"),
    finished=("lifecycle", lambda s: int((s == "finished").sum())),
    scored=("score_total", lambda s: int(s.notna().sum())),
    tokens_ok=("tokens_validity", lambda s: int((s == "ok").sum())),
    tokens_partial=("tokens_validity", lambda s: int((s == "caveat:partial_lower_bound").sum())),
    hit_time_limit=("hit_time_limit", lambda s: int(s.astype(bool).sum())),
    multi_attempt=("n_trajectory_files", lambda s: int((s > 1).sum())),
    checker_failed=("outcome_class", lambda s: int(s.isin(["delivered_checker_error", "checker_error_no_frames"]).sum())),
    needs_review=("needs_review", lambda s: int(s.astype(bool).sum())),
).reset_index()
save(cov, "0_coverage_by_model.csv")
md_table(cov)
sizes = {k: {c: int(v[c].sum()) for c in ("q", "tok", "dur")} for k, v in SETS.items()}
md("Inclusion sets (records with usable quality / tokens / time): " +
   "; ".join(f"**{k}** {v['q']}/{v['tok']}/{v['dur']}" for k, v in sizes.items()))
md()
oth = runs[fin & runs.tokens_other_files.notna() & (runs.tokens_other_files > 0)]
md(f"Restarts that ran on a different Figma file than the judged one: {len(oth)} runs; in those runs a median "
   f"{(oth.tokens_other_files / oth.total_tokens).median():.0%} of the reported tokens were spent on the non-judged file "
   f"(max {(oth.tokens_other_files / oth.total_tokens).max():.0%}). The primary token cost excludes that share.")
md()
nb = runs[fin & (runs.protocol == NEW_PROTOCOL)]
eff = pd.crosstab(nb.model, nb.requested_effort.fillna("no trajectory")).reset_index()
save(eff, "0_reasoning_effort_by_model.csv")
md("Requested reasoning effort recorded in the trajectories of the judged attempts (`not_set` = no effort control was sent; `not_set|low` = attempts of the same run differ):")
md()
md_table(eff)
for col in ["outcome_class", "quality_validity", "tokens_validity", "time_validity", "trajectory_validity"]:
    vc = runs[col].value_counts()
    md(f"- `{col}`: " + ", ".join(f"{k} {v}" for k, v in vc.items()))
md()

# --------------------------------------------------------------------------- 1. per-model description
md("## 1. Per-model outcome and cost (primary set, unmatched — descriptive only)")
md()
rows = []
for m in models:
    a = runs[(runs.model == m) & fin]
    s = subset("primary", "tokens")
    s = s[s.model == m]
    d = subset("primary", "time", need_score=False)
    d = d[d.model == m]
    rows.append({
        "model": m, "finished": len(a),
        "delivered_or_checker_err": int(a.outcome_class.isin(["delivered", "delivered_checker_error"]).sum()),
        "g0_fail": int(((a.g0_pass.astype(str) == "False") & a.score_total.notna()).sum()),
        "n_scored": len(s),
        "score_mean": s.score_total.mean(), "score_median": s.score_total.median(),
        "tokens_M_median": s.tokens_scored_file.median() / 1e6, "tokens_M_mean": s.tokens_scored_file.mean() / 1e6,
        "tokens_M_p25": s.tokens_scored_file.quantile(.25) / 1e6, "tokens_M_p75": s.tokens_scored_file.quantile(.75) / 1e6,
        "max_over_min_tokens": s.tokens_scored_file.max() / s.tokens_scored_file.min() if len(s) else np.nan,
        "all_attempt_tokens_M_median": s.total_tokens.median() / 1e6,
        "minutes_median": d.duration_s.median() / 60,
        "tool_calls_median": s.tool_calls.median(),
        "tool_error_rate": s.tool_errors.sum() / s.tool_calls_answered.sum() if s.tool_calls_answered.sum() else np.nan,
    })
desc = pd.DataFrame(rows).sort_values("tokens_M_median")
save(desc, "1_model_description.csv")
md_table(desc)
md("These rows mix different problem sets per model, so they are not a ranking. Use sections 2-3.")
md()

# --------------------------------------------------------------------------- 2. two-way additive model


def fit_effects(df, ycol, log=False):
    """Least squares y ~ model + problem on an unbalanced table. Returns model effects, centred
    so that the mean effect over models is zero (identifiable when the design is connected)."""
    ms = sorted(df.model.unique())
    ps = sorted(df.problem.unique())
    mi = {m: i for i, m in enumerate(ms)}
    pi = {p: i for i, p in enumerate(ps)}
    y = df[ycol].to_numpy(float)
    if log:
        y = np.log(y)
    X = np.zeros((len(df), len(ms) + len(ps) + 1))
    X[np.arange(len(df)), df.model.map(mi).to_numpy()] = 1
    X[np.arange(len(df)), len(ms) + df.problem.map(pi).to_numpy()] = 1
    # one shift for the earlier protocol, shared by all models (zero column if only one protocol)
    X[:, -1] = (df.protocol != NEW_PROTOCOL).to_numpy(float)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    eff = beta[:len(ms)]
    eff = eff - eff.mean()
    out = pd.Series(eff, index=ms)
    out["__old_protocol__"] = beta[-1]
    return out


def boot_effects(df, ycol, log=False, reps=REPS):
    point = fit_effects(df, ycol, log)
    ps = sorted(df.problem.unique())
    groups = {p: g for p, g in df.groupby("problem")}
    draws = []
    for _ in range(reps):
        pick = rng.choice(ps, size=len(ps), replace=True)
        parts = []
        for j, p in enumerate(pick):
            g = groups[p].copy()
            g["problem"] = f"{p}#{j}"
            parts.append(g)
        b = pd.concat(parts, ignore_index=True)
        if b.model.nunique() < df.model.nunique() or b.protocol.nunique() < df.protocol.nunique():
            continue
        try:
            draws.append(fit_effects(b, ycol, log).reindex(point.index))
        except np.linalg.LinAlgError:
            continue
    D = pd.DataFrame(draws)
    return point, D.quantile(0.025), D.quantile(0.975)


md("## 2. Problem-adjusted model effects (score and cost)")
md()
md("Additive model `y ~ model + problem`, fitted on all usable records, so a model that only ran "
   "13 problems is compared on those problems' own difficulty. Cost effects are multiplicative "
   "(x geometric mean of models); 95% intervals resample problems.")
md()
eff_tables, proto_rows = {}, {}
for set_name in SETS:
    out = pd.DataFrame(index=models + ["__old_protocol__"])
    s = subset(set_name)
    if s.model.nunique() > 1:
        p, lo, hi = boot_effects(s, "score_total")
        out["score_effect"], out["score_lo"], out["score_hi"] = p, lo, hi
        out["n_score"] = s.groupby("model").size()
    for cost in ["tokens", "tokens_all_attempts", "time", "output_tokens", "tool_calls"]:
        c = subset(set_name, cost, need_score=False)
        if c.model.nunique() > 1:
            p, lo, hi = boot_effects(c, COSTS[cost][0], log=True)
            out[f"{cost}_x"], out[f"{cost}_x_lo"], out[f"{cost}_x_hi"] = np.exp(p), np.exp(lo), np.exp(hi)
            out[f"n_{cost}"] = c.groupby("model").size()
    proto_rows[set_name] = out.loc["__old_protocol__"] if "__old_protocol__" in out.index else None
    out = out.drop(index="__old_protocol__", errors="ignore")
    out = out.reset_index().rename(columns={"index": "model"})
    eff_tables[set_name] = out
    save(out, f"2_model_effects_{set_name}.csv")
prim = eff_tables["primary"].sort_values("tokens_x")
show = prim[["model", "n_score", "score_effect", "score_lo", "score_hi", "tokens_x", "tokens_x_lo", "tokens_x_hi",
             "time_x", "time_x_lo", "time_x_hi", "tool_calls_x"]]
md_table(show)
if HAS_OLD:
    pr = proto_rows["primary"]
    md("**Protocol shift** (earlier package: screenshot self-check required, Claude Code harness; this batch: screenshots "
       "forbidden, direct runner). Estimated as one common shift, identified because the four 42-problem models fix each "
       "problem's level under the new protocol and the six other models were run under both protocols on different problems. "
       "It assumes the shift is the same for every model and that models do not interact with problems:")
    md()
    md(f"- score: {pr.score_effect:+.1f} points under the earlier protocol (95% {pr.score_lo:+.1f} to {pr.score_hi:+.1f})")
    md(f"- tokens: x{pr.tokens_x:.2f} (95% {pr.tokens_x_lo:.2f} to {pr.tokens_x_hi:.2f}); time: x{pr.time_x:.2f} "
       f"(95% {pr.time_x_lo:.2f} to {pr.time_x_hi:.2f})")
    md()
    pd.DataFrame(proto_rows).T.to_csv(os.path.join(TAB, "2_protocol_shift.csv"))

# --------------------------------------------------------------------------- 3. matched pairs
md("## 3. Problem-matched pairwise comparison (primary set)")
md()
s = subset("primary", "tokens")
piv_s = s.pivot_table(index="cell", columns="model", values="score_total", aggfunc="first")
piv_c = s.pivot_table(index="cell", columns="model", values="tokens_scored_file", aggfunc="first")
rows = []
for a, b in itertools.combinations(models, 2):
    if a not in piv_s or b not in piv_s:
        continue
    common = piv_s[[a, b]].dropna().index.intersection(piv_c[[a, b]].dropna().index)
    if len(common) < 5:
        continue
    ds = piv_s.loc[common, a] - piv_s.loc[common, b]
    lr = np.log(piv_c.loc[common, a] / piv_c.loc[common, b])
    cheaper_not_worse = int(((lr < 0) & (ds >= -DELTA)).sum())
    costlier_not_better = int(((lr > 0) & (ds <= DELTA)).sum())
    rows.append({"model_a": a, "model_b": b, "n_common": len(common),
                 "median_score_diff_a_minus_b": ds.median(),
                 "a_higher_score": int((ds > DELTA).sum()), "b_higher_score": int((ds < -DELTA).sum()),
                 "median_token_ratio_a_over_b": float(np.exp(lr.median())),
                 "a_cheaper_on": int((lr < 0).sum()),
                 "a_cheaper_and_not_worse": cheaper_not_worse,
                 "a_costlier_and_not_better": costlier_not_better})
pairs = pd.DataFrame(rows)
save(pairs, "3_pairwise_matched.csv")
if len(pairs):
    md(f"{len(pairs)} model pairs with >=5 common problems (full table: tables/3_pairwise_matched.csv). "
       "Largest cost gaps without a quality gain:")
    md()
    top = pairs.assign(gap=lambda d: np.abs(np.log(d.median_token_ratio_a_over_b))).sort_values("gap", ascending=False).head(12)
    md_table(top.drop(columns="gap"))

# --------------------------------------------------------------------------- 4. Pareto per problem
md("## 4. Per-problem cost-quality Pareto frontier")
md()


def pareto(df, costcol, delta):
    """Frontier membership within one problem. With delta>0 a point is only dominated if another
    is cheaper AND better by more than delta or equal-within-delta and >=20% cheaper."""
    res = {}
    recs = df[["model", costcol, "score_total"]].to_numpy()
    for m, c, q in recs:
        dominated = False
        for m2, c2, q2 in recs:
            if m2 == m:
                continue
            if delta == 0:
                if c2 <= c and q2 >= q and (c2 < c or q2 > q):
                    dominated = True
            else:
                if c2 <= 0.8 * c and q2 >= q - delta:
                    dominated = True
                elif c2 <= c and q2 > q + delta:
                    dominated = True
            if dominated:
                break
        res[m] = not dominated
    return res


rows = []
for set_name in SETS:
    for cost in ["tokens", "time"]:
        s = subset(set_name, cost)
        for delta in (0.0, DELTA):
            tally = {m: [0, 0] for m in models}
            for p, g in s.groupby("cell"):
                if len(g) < 3:
                    continue
                fr = pareto(g, COSTS[cost][0], delta)
                for m, on in fr.items():
                    tally[m][1] += 1
                    tally[m][0] += int(on)
            for m, (on, n) in tally.items():
                rows.append({"set": set_name, "cost": cost, "score_tolerance": delta, "model": m,
                             "on_frontier": on, "problems": n, "frontier_rate": on / n if n else np.nan})
par = pd.DataFrame(rows)
save(par, "4_pareto_frontier.csv")
p1 = par[(par.set == "primary")].pivot_table(index="model", columns=["cost", "score_tolerance"], values="frontier_rate")
p1.columns = [f"{c}_tol{t:g}" for c, t in p1.columns]
p1["problems"] = par[(par.set == "primary") & (par.cost == "tokens") & (par.score_tolerance == 0)].set_index("model").problems
p1 = p1.reset_index().sort_values("tokens_tol0", ascending=False)
md("Share of problems on which each model is not dominated. `tol0` is strict dominance; "
   f"`tol{DELTA:g}` only counts domination by a model that is >=20% cheaper at no worse than -{DELTA:g} points, "
   f"or cheaper and better by more than {DELTA:g}. A frontier is an observed set from single runs, not a guarantee.")
md()
md_table(p1)

# --------------------------------------------------------------------------- 5. does more cost buy more quality?
md("## 5. Cost vs quality relationship")
md()


def spearman(x, y):
    rx, ry = pd.Series(x).rank(), pd.Series(y).rank()
    if rx.std() == 0 or ry.std() == 0:
        return np.nan
    return float(np.corrcoef(rx, ry)[0, 1])


rows = []
for set_name in SETS:
    for cost in ["tokens", "time", "tool_calls"]:
        s = subset(set_name, cost)
        for p, g in s.groupby("cell"):
            if len(g) >= 4:
                rows.append({"set": set_name, "cost": cost, "problem": p, "n_models": len(g),
                             "spearman": spearman(g[COSTS[cost][0]], g.score_total)})
sp = pd.DataFrame(rows)
save(sp, "5_per_problem_spearman.csv")
agg = (sp.assign(many=lambda d: np.where(d.n_models >= 8, ">=8 models", "4-7 models"))
         .groupby(["set", "cost", "many"]).spearman
         .agg(problems="count", median="median", share_negative=lambda v: float((v < 0).mean()),
              p25=lambda v: v.quantile(.25), p75=lambda v: v.quantile(.75)).reset_index())
save(agg, "5_spearman_summary.csv")
md("Across models within the same problem (Spearman between cost and score), summarised over problems. "
   "Problems with only 4 models give very coarse correlations and are shown separately.")
md()
md_table(agg[agg.set == "primary"].drop(columns="set"))


def gamma_fit(df, costcol):
    ms = sorted(df.model.unique())
    ps = sorted(df.problem.unique())
    X = np.zeros((len(df), len(ms) + len(ps) + 2))
    X[np.arange(len(df)), df.model.map({m: i for i, m in enumerate(ms)}).to_numpy()] = 1
    X[np.arange(len(df)), len(ms) + df.problem.map({p: i for i, p in enumerate(ps)}).to_numpy()] = 1
    X[:, -2] = (df.protocol != NEW_PROTOCOL).to_numpy(float)
    X[:, -1] = np.log(df[costcol].to_numpy(float))
    beta, *_ = np.linalg.lstsq(X, df.score_total.to_numpy(float), rcond=None)
    return beta[-1]


def gamma_boot(df, costcol, reps=REPS):
    point = gamma_fit(df, costcol)
    ps = sorted(df.problem.unique())
    groups = {p: g for p, g in df.groupby("problem")}
    draws = []
    for _ in range(reps):
        pick = rng.choice(ps, size=len(ps), replace=True)
        parts = []
        for j, p in enumerate(pick):
            g = groups[p].copy()
            g["problem"] = f"{p}#{j}"
            parts.append(g)
        draws.append(gamma_fit(pd.concat(parts, ignore_index=True), costcol))
    return point, float(np.quantile(draws, .025)), float(np.quantile(draws, .975))


rows = []
for set_name in SETS:
    for cost in ["tokens", "time", "tool_calls"]:
        for label, filt in [("all scored", None), ("G0-pass only", "g0")]:
            s = subset(set_name, cost)
            if filt:
                s = s[s.g0_pass.astype(str) == "True"]
            if len(s) < 30:
                continue
            g, lo, hi = gamma_boot(s, COSTS[cost][0], reps=max(300, REPS // 4))
            rows.append({"set": set_name, "cost": cost, "scores": label, "n": len(s),
                         "gamma_points_per_log_cost": g, "ci_lo": lo, "ci_hi": hi,
                         "points_per_doubling": g * np.log(2)})
gam = pd.DataFrame(rows)
save(gam, "5_fixed_effects_gamma.csv")
md("Within-model, within-problem association `score ~ model + problem + gamma*log(cost)`. "
   "gamma is an association, not the effect of spending more: runs that go badly also retry more.")
md()
md_table(gam[gam.set == "primary"].drop(columns="set"))

# --------------------------------------------------------------------------- 6. where does the cost go?
md("## 6. Execution behaviour (where resources go)")
md()
s = subset("primary", "tokens", need_score=False)
s = s[s.tool_calls.notna() & (s.tool_calls > 0)].copy()
s["proto"] = np.where(s.protocol == NEW_PROTOCOL, "v2", "v1")
for c_ in ["calls_verify", "carry_chars_verify", "carry_chars_harness_reminders", "tool_errors_intentional"]:
    s[c_] = s[c_].fillna(0) if c_ in s else 0
cats = ["setup", "inspect", "construct", "modify", "prototype", "verify", "other_tool"]
beh = s.groupby(["model", "proto"]).agg(
    runs=("task_id", "size"),
    turns_med=("assistant_turns", "median"),
    calls_med=("tool_calls", "median"),
    inspect_share=("calls_inspect", "sum"), construct_share=("calls_construct", "sum"),
    modify_share=("calls_modify", "sum"), prototype_share=("calls_prototype", "sum"),
    verify_share=("calls_verify", "sum"),
    calls_total=("tool_calls", "sum"), answered=("tool_calls_answered", "sum"),
    errors=("tool_errors", "sum"), err_model=("tool_errors_model", "sum"),
    err_infra=("tool_errors_infra", "sum"), err_unknown=("tool_errors_unknown", "sum"),
    err_intentional=("tool_errors_intentional", "sum"),
    same_error_repeats=("same_error_repeats", "sum"), duplicate_calls=("duplicate_calls", "sum"),
    calls_with_delete=("calls_with_delete", "sum"),
    post_build_inspect=("post_build_inspect_calls", "sum"),
    max_streak_med=("max_error_streak", "median"),
).reset_index()
for c in ["inspect", "construct", "modify", "prototype", "verify"]:
    beh[f"{c}_share"] = beh[f"{c}_share"] / beh.calls_total
beh["error_rate"] = beh.errors / beh.answered
beh["model_err_share"] = beh.err_model / beh.errors.replace(0, np.nan)
beh["infra_err_share"] = beh.err_infra / beh.errors.replace(0, np.nan)
beh["unknown_err_share"] = beh.err_unknown / beh.errors.replace(0, np.nan)
beh["intentional_throw_share"] = beh.err_intentional / beh.errors.replace(0, np.nan)
beh["infra_errors_per_run"] = beh.err_infra / beh.runs
beh["repeat_same_error_per_run"] = beh.same_error_repeats / beh.runs
beh["duplicate_calls_per_run"] = beh.duplicate_calls / beh.runs
beh["delete_calls_per_run"] = beh.calls_with_delete / beh.runs
beh["post_build_inspect_per_run"] = beh.post_build_inspect / beh.runs
save(beh, "6_behaviour_by_model.csv")
md("Tool-call mix and error behaviour per model (labels are descriptive; no category is 'waste' by itself):")
md()
md("`v1` = earlier package (screenshots required), `v2` = this batch (screenshots forbidden). `verify` = get_screenshot calls. "
   "Error shares are of failed calls; `intentional_throw` = the model threw an Error on purpose to print data.")
md()
md_table(beh[["model", "proto", "runs", "turns_med", "calls_med", "inspect_share", "construct_share", "modify_share",
              "prototype_share", "verify_share", "error_rate", "model_err_share", "infra_err_share", "unknown_err_share", "intentional_throw_share",
              "repeat_same_error_per_run", "duplicate_calls_per_run", "delete_calls_per_run"]])

inf = s.assign(any_infra=s.tool_errors_infra > 0).groupby(["model", "proto"]).agg(
    runs=("task_id", "size"), runs_with_infra_errors=("any_infra", "sum"),
    infra_errors=("tool_errors_infra", "sum"), calls=("tool_calls_answered", "sum")).reset_index()
inf["infra_errors_per_100_calls"] = 100 * inf.infra_errors / inf.calls
save(inf, "6_infra_errors_by_model.csv")
md("Infrastructure-caused failed calls (quota circuit breaker, tool timeouts, transport). These are not the model's "
   "doing, and the retries they trigger inflate tokens and time:")
md()
md_table(inf)
carry_cols = [f"carry_chars_{c}" for c in cats] + ["carry_chars_assistant_text", "carry_chars_fixed_prompt",
                                                    "carry_chars_harness_reminders"]
cc = s.groupby(["model", "proto"])[carry_cols + ["carry_chars_total"]].sum()
share = cc[carry_cols].div(cc.carry_chars_total, axis=0)
share.columns = [c.replace("carry_chars_", "") for c in share.columns]
share = share.reset_index()
save(share, "6_context_occupancy_by_model.csv")
md("Context occupancy: every message is re-sent on each later model request, so its characters are weighted by "
   "the number of later requests that contain it. This is where *input* tokens come from (shares sum to 1). "
   "`fixed_prompt` is the system prompt + tool schemas, paid once per turn.")
md()
md_table(share)

chk = s[(s.carry_chars_total > 0) & (s.input_tokens > 0)]
r_all = spearman(chk.carry_chars_total, chk.input_tokens)
ratio = (chk.carry_chars_total / chk.input_tokens).groupby([chk.model, chk.proto]).agg(["median", "min", "max", "count"]).reset_index()
ratio.columns = ["model", "proto", "chars_per_input_token_median", "min", "max", "runs"]
save(ratio, "6_chars_per_token_check.csv")
md(f"Validation of that attribution: Spearman between trajectory-implied context size and reported input tokens = "
   f"**{r_all:.2f}** over {len(chk)} runs. Per-model characters per reported input token (a stable ratio means the "
   "token counts and the trajectory agree; outliers are flagged in the review queue):")
md()
md_table(ratio)

# what distinguishes expensive runs: within-problem, within-model association with log tokens
feat = {"assistant_turns": "turns", "calls_verify": "screenshot calls", "tool_errors": "tool errors", "same_error_repeats": "same error repeated",
        "duplicate_calls": "duplicate calls", "calls_inspect": "inspect calls", "calls_construct": "construct calls",
        "calls_modify": "modify calls", "calls_with_delete": "calls that delete", "largest_result_chars": "largest tool result"}
rows = []
for col, label in feat.items():
    d = s[["model", "problem", "proto", "tokens_scored_file", col]].dropna()
    d = d.assign(model=d.model + "/" + d.proto, problem=d.problem + "/" + d.proto)
    d = d[d.tokens_scored_file > 0]
    lt = np.log(d.tokens_scored_file)
    x = np.log1p(d[col].astype(float))
    # remove model and problem means (two-way demeaning, one pass each is enough for a descriptive r)
    for key in ("model", "problem"):
        lt = lt - lt.groupby(d[key]).transform("mean")
        x = x - x.groupby(d[key]).transform("mean")
    rows.append({"feature": label, "partial_spearman_with_log_tokens": spearman(x, lt), "n": len(d)})
drv = pd.DataFrame(rows).sort_values("partial_spearman_with_log_tokens", ascending=False)
save(drv, "6_token_drivers.csv")
md("What moves with token use after removing model and problem averages:")
md()
md_table(drv)

# --------------------------------------------------------------------------- 7. sensitivity
md("## 7. Robustness of the conclusions")
md()
rows = []
for cost in ["tokens", "time"]:
    base = eff_tables["primary"].set_index("model")[f"{cost}_x"]
    for set_name in SETS:
        cur = eff_tables[set_name].set_index("model")
        if f"{cost}_x" not in cur:
            continue
        both = pd.concat([base, cur[f"{cost}_x"]], axis=1, keys=["base", "cur"]).dropna()
        rows.append({"cost": cost, "set": set_name, "models": len(both),
                     "rank_corr_with_primary": spearman(both.base, both.cur),
                     "max_abs_log2_change": float(np.abs(np.log2(both.cur / both.base)).max())})
base_s = eff_tables["primary"].set_index("model")["score_effect"]
for set_name in SETS:
    cur = eff_tables[set_name].set_index("model")
    if "score_effect" in cur:
        both = pd.concat([base_s, cur.score_effect], axis=1, keys=["base", "cur"]).dropna()
        rows.append({"cost": "score", "set": set_name, "models": len(both),
                     "rank_corr_with_primary": spearman(both.base, both.cur),
                     "max_abs_log2_change": float(np.abs(both.cur - both.base).max())})
sens = pd.DataFrame(rows)
save(sens, "7_sensitivity_model_effects.csv")
md("Model effects re-estimated under each inclusion set (for `score` the last column is the largest change in points; "
   "for costs it is the largest change in log2 units, i.e. 1.0 = a factor of two):")
md()
md_table(sens)
md("Cost-quality slope (gamma) under each set and cost measure:")
md()
g7 = gam[gam.scores == "all scored"].assign(lo_per_doubling=lambda d: d.ci_lo * np.log(2), hi_per_doubling=lambda d: d.ci_hi * np.log(2))
md_table(g7[["set", "cost", "n", "points_per_doubling", "lo_per_doubling", "hi_per_doubling"]])
tok_time = subset("primary", "tokens", need_score=False)
tok_time = tok_time[tok_time.duration_s.notna()]
md(f"Tokens vs wall-clock time across runs: Spearman {spearman(tok_time.tokens_scored_file, tok_time.duration_s):.2f} "
   f"(n={len(tok_time)}); they are related but not interchangeable, so both are reported.")
md()

# judge repeatability, if the scoring log holds more than one completed score per record
sr_path = os.path.join(os.path.dirname(OUT.rstrip("/")), "..")
md("## 8. Open items the data cannot settle")
md()
md("- Single run per model x problem: run-to-run variance is unobserved, so small differences are not evidence.")
md(f"- Judge noise is not estimated here; the {DELTA:g}-point tolerance is a placeholder until repeat judgings or human ratings exist.")
md("- Progress curves (cost vs verified progress) need intermediate file states or the trace database; "
   "trajectories alone only support call-level proxies.")
md()

with open(os.path.join(OUT, "report.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))
print("\n".join(lines))
