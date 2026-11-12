"""Reliable-set efficiency findings.

Step 1 selects the records whose numbers can be trusted (rules below, each with a count).
Step 2 computes the findings on that set, with the wider set as a sensitivity check.
Writes out/reliable_runs.csv, out/findings.json and out/tables/R_*.csv.

A record is RELIABLE when all of these hold:
  R1 the run finished
  R2 the judged score is of the final artifact (not a mid-run snapshot, not a crashed check with no frames)
  R3 its cost can be attributed to the judged file exactly (single attempt, or per-attempt usage adds up)
  R4 the token count is verified against the trajectory: characters-per-input-token within
     [0.6, 1.6] x the median of that model+protocol. This replaces the harness's own
     "partial" label, which is kept only when the trajectory confirms a real gap.
  R5 the run is not materially hit by infrastructure failures (<=2 infra-failed calls and <5% of calls)
  R6 a trajectory exists (needed for R4 and R5)
None of the rules looks at how large the cost is.

Usage: .venv/bin/python findings.py out [bootstrap_reps=2000]
"""
import json
import os
import sys

import numpy as np
import pandas as pd

OUT = sys.argv[1]
REPS = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
TAB = os.path.join(OUT, "tables")
os.makedirs(TAB, exist_ok=True)
rng = np.random.default_rng(7)
F = {}  # findings


def load():
    n = pd.read_csv(os.path.join(OUT, "runs.csv"), keep_default_na=False, na_values=[""], low_memory=False)
    n["protocol"] = "v2"
    o = pd.read_csv(os.path.join(OUT, "runs_old.csv"), keep_default_na=False, na_values=[""])
    o["protocol"] = "v1"
    o = o[o.model.isin(set(n.model))]
    r = pd.concat([n, o], ignore_index=True)
    r["g0"] = r.g0_pass.astype(str).eq("True")
    for c in ["tool_errors_infra", "tool_calls_answered", "carry_chars_total"]:
        r[c] = pd.to_numeric(r[c], errors="coerce")
    return r


r = load()
r["cpt"] = r.carry_chars_total / r.input_tokens
ref = r[r.tokens_validity.eq("ok") & r.cpt.notna()].groupby(["model", "protocol"]).cpt.median().rename("cpt_ref")
r = r.join(ref, on=["model", "protocol"])
r["cpt_rel"] = r.cpt / r.cpt_ref

rules = {
    "R1 finished": r.lifecycle.eq("finished"),
    "R2 score is of the final artifact": r.quality_validity.isin(["ok", "caveat:multiple_score_revisions"])
    & ~r.outcome_class.isin(["checker_error_no_frames", "failed_unknown", "no_score"]),
    "R3 cost attributable to judged file": r.token_split_method.fillna("single_attempt").isin(
        ["single_attempt", "exact_per_attempt_usage"]) & r.tokens_scored_file.notna(),
    "R4 token count verified by trajectory": r.cpt_rel.between(0.6, 1.6),
    "R5 no material infra failures": (r.tool_errors_infra.fillna(0) <= 2)
    & (r.tool_errors_infra.fillna(0) < 0.05 * r.tool_calls_answered.fillna(1e9)),
    "R6 trajectory available": r.trajectory_validity.eq("ok"),
}
ok = pd.Series(True, index=r.index)
audit = []
for name, m in rules.items():
    audit.append({"rule": name, "fail_this_rule": int((~m).sum()), "newly_excluded": int((ok & ~m).sum())})
    ok &= m
    audit[-1]["remaining"] = int(ok.sum())
r["reliable"] = ok
aud = pd.DataFrame(audit)
aud.to_csv(os.path.join(TAB, "R_0_reliability_rules.csv"), index=False)
print(aud.to_string(index=False))
cov = r.groupby(["model", "protocol"]).agg(records=("reliable", "size"), reliable=("reliable", "sum")).unstack(fill_value=0)
cov.columns = [f"{a}_{b}" for a, b in cov.columns]
cov.to_csv(os.path.join(TAB, "R_0_reliable_coverage.csv"))
print(cov.to_string())
r.to_csv(os.path.join(OUT, "all_runs_labelled.csv"), index=False)
R = r[r.reliable].copy()
R.to_csv(os.path.join(OUT, "reliable_runs.csv"), index=False)
# wider set: everything finished + scored + with a token number (lower bounds and estimates included)
W = r[rules["R1 finished"] & rules["R2 score is of the final artifact"] & r.tokens_scored_file.notna()].copy()
F["n_total"], F["n_reliable"], F["n_wide"] = len(r), len(R), len(W)
F["partial_label_total"] = int(r.tokens_validity.eq("caveat:partial_lower_bound").sum())
F["partial_label_confirmed_ok"] = int((r.tokens_validity.eq("caveat:partial_lower_bound") & rules["R4 token count verified by trajectory"]).sum())

# selection check: are excluded runs systematically more expensive?
sel = W.assign(ltok=np.log(W.tokens_scored_file))
sel["lt_adj"] = sel.ltok - sel.groupby(["model", "protocol"]).ltok.transform("mean")
F["excluded_vs_kept_token_ratio_within_model"] = float(np.exp(sel[~sel.reliable].lt_adj.mean() - sel[sel.reliable].lt_adj.mean()))
print("excluded/kept token ratio within model+protocol:", round(F["excluded_vs_kept_token_ratio_within_model"], 2))

# ------------------------------------------------------------------ model: y ~ model + problem + protocol


def design(df, extra=None):
    ms, ps = sorted(df.model.unique()), sorted(df.problem.unique())
    X = np.zeros((len(df), len(ms) + len(ps) + 1 + (0 if extra is None else extra.shape[1])))
    X[np.arange(len(df)), df.model.map({m: i for i, m in enumerate(ms)}).to_numpy()] = 1
    X[np.arange(len(df)), len(ms) + df.problem.map({p: i for i, p in enumerate(ps)}).to_numpy()] = 1
    X[:, len(ms) + len(ps)] = (df.protocol == "v1").to_numpy(float)
    if extra is not None:
        X[:, len(ms) + len(ps) + 1:] = extra
    return X, ms, ps


def fit(df, y, extra=None):
    X, ms, ps = design(df, extra)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    eff = pd.Series(beta[:len(ms)] - beta[:len(ms)].mean(), index=ms)
    return eff, beta[len(ms) + len(ps)], beta[len(ms) + len(ps) + 1:], y - X @ beta


def boot(df, yfun, extra_fun=None, reps=REPS):
    """Resample problems (the sampling unit). Returns point estimates and 95% intervals."""
    e0, p0, x0, _ = fit(df, yfun(df), None if extra_fun is None else extra_fun(df))
    groups = {p: g for p, g in df.groupby("problem")}
    ps = list(groups)
    E, P, Xs = [], [], []
    for _ in range(reps):
        parts = []
        for j, p in enumerate(rng.choice(ps, len(ps))):
            g = groups[p].copy()
            g["problem"] = f"{p}#{j}"
            parts.append(g)
        b = pd.concat(parts, ignore_index=True)
        if b.model.nunique() < df.model.nunique() or b.protocol.nunique() < df.protocol.nunique():
            continue
        e, p_, x, _ = fit(b, yfun(b), None if extra_fun is None else extra_fun(b))
        E.append(e.reindex(e0.index))
        P.append(p_)
        Xs.append(x)
    E = pd.DataFrame(E)
    q = lambda a: (float(np.quantile(a, .025)), float(np.quantile(a, .975)))
    return e0, E.quantile(.025), E.quantile(.975), (p0, *q(P)), [(x0[i], *q([x[i] for x in Xs])) for i in range(len(x0))], E


def effects(df, tag):
    out = pd.DataFrame(index=sorted(df.model.unique()))
    draws = {}
    for name, yfun, logged in [("score", lambda d: d.score_total.to_numpy(float), False),
                               ("tokens", lambda d: np.log(d.tokens_scored_file.to_numpy(float)), True),
                               ("time", lambda d: np.log(d.duration_s.to_numpy(float)), True),
                               ("turns", lambda d: np.log(d.assistant_turns.to_numpy(float)), True),
                               ("tok_per_turn", lambda d: np.log((d.tokens_scored_file / d.assistant_turns).to_numpy(float)), True),
                               ("cost", lambda d: np.log(d.cost_list.to_numpy(float)), True)]:
        if name == "cost" and ("cost_list" not in df or df.cost_list.isna().any()):
            continue
        d = df[df.duration_s.notna() & (df.duration_s > 0) & (df.assistant_turns > 0)] if name != "score" else df
        e, lo, hi, proto, _, E = boot(d, yfun)
        tr = np.exp if logged else (lambda v: v)
        out[name], out[name + "_lo"], out[name + "_hi"] = tr(e), tr(lo), tr(hi)
        F[f"{tag}_protocol_{name}"] = [float(tr(v)) for v in proto]
        draws[name] = E
    out["n"] = df.groupby("model").size()
    out.to_csv(os.path.join(TAB, f"R_1_model_effects_{tag}.csv"))
    return out, draws


cost_path = os.path.join(OUT, "reliable_runs_cost.csv")
if os.path.exists(cost_path):
    cc = pd.read_csv(cost_path, low_memory=False)[["task_id", "cost_list", "output_share_of_cost"]]
    for d in (R, W):
        d.drop(columns=[c for c in ("cost_list", "output_share_of_cost") if c in d], inplace=True)
    R = R.merge(cc, on="task_id", how="left")
    W = W.merge(cc, on="task_id", how="left")

effR, drawsR = effects(R, "reliable")
effW, _ = effects(W, "wide")
print(effR.round(2).sort_values("tokens").to_string())
print("protocol v1 vs v2 (reliable): score", np.round(F["reliable_protocol_score"], 2), "tokens x", np.round(F["reliable_protocol_tokens"], 2),
      "time x", np.round(F["reliable_protocol_time"], 2))
F["rank_corr_reliable_vs_wide_tokens"] = float(effR.tokens.rank().corr(effW.tokens.rank()))
F["rank_corr_reliable_vs_wide_score"] = float(effR.score.rank().corr(effW.score.rank()))
F["max_log2_change_tokens_wide"] = float(np.abs(np.log2(effW.tokens / effR.tokens)).max())
F["max_score_change_wide"] = float((effW.score - effR.score).abs().max())
F["token_spread_between_models"] = float(effR.tokens.max() / effR.tokens.min())

# Pareto frontier on adjusted effects + how often each model is on it across bootstrap draws
def frontier(cost, score):
    on = []
    for m in cost.index:
        dom = ((cost <= cost[m]) & (score >= score[m]) & ((cost < cost[m]) | (score > score[m]))).any()
        on.append(not dom)
    return pd.Series(on, index=cost.index)


effR["on_frontier"] = frontier(effR.tokens, effR.score)
if "cost" in effR:
    effR["on_frontier_cost"] = frontier(effR.cost, effR.score)
    nn = min(len(drawsR["cost"]), len(drawsR["score"]))
    effR["frontier_prob_cost"] = sum(frontier(np.exp(drawsR["cost"].iloc[i]), drawsR["score"].iloc[i]).astype(int) for i in range(nn)) / nn
    F["cost_spread_between_models"] = float(effR.cost.max() / effR.cost.min())
    F["rank_change_tokens_to_cost"] = {m: int(effR.tokens.rank()[m] - effR.cost.rank()[m]) for m in effR.index}
    F["output_share_of_cost_median"] = float(R.output_share_of_cost.median())
n = min(len(drawsR["tokens"]), len(drawsR["score"]))
freq = sum(frontier(np.exp(drawsR["tokens"].iloc[i]), drawsR["score"].iloc[i]).astype(int) for i in range(n)) / n
effR["frontier_prob"] = freq
effR.to_csv(os.path.join(TAB, "R_1_model_effects_reliable.csv"))
print(effR[["score", "tokens", "on_frontier", "frontier_prob"]].round(2).sort_values("tokens").to_string())

# ------------------------------------------------------------------ does spending more buy quality?
res = []
for tag, df in [("reliable", R), ("wide", W)]:
    for label, d in [("all", df), ("g0_pass", df[df.g0])]:
        _, _, _, _, x, _ = boot(d, lambda b: b.score_total.to_numpy(float),
                                lambda b: np.log(b.tokens_scored_file.to_numpy(float))[:, None], reps=max(500, REPS // 2))
        g, lo, hi = x[0]
        res.append({"set": tag, "scores": label, "n": len(d), "points_per_doubling": g * np.log(2),
                    "lo": lo * np.log(2), "hi": hi * np.log(2)})
for label, col in [("cost_all", "cost_list")]:
    if col in R and R[col].notna().all():
        _, _, _, _, x, _ = boot(R, lambda b: b.score_total.to_numpy(float),
                                lambda b: np.log(b[col].to_numpy(float))[:, None], reps=max(500, REPS // 2))
        g, lo, hi = x[0]
        res.append({"set": "reliable", "scores": label, "n": len(R), "points_per_doubling": g * np.log(2),
                    "lo": lo * np.log(2), "hi": hi * np.log(2)})
gam = pd.DataFrame(res)
gam.to_csv(os.path.join(TAB, "R_2_cost_quality_slope.csv"), index=False)
print(gam.round(2).to_string(index=False))
# residuals for the figure
_, _, _, rs = fit(R, R.score_total.to_numpy(float))
_, _, _, rt = fit(R, np.log(R.tokens_scored_file.to_numpy(float)))
R["score_resid"], R["logtok_resid"] = rs, rt
F["resid_corr_score_tokens"] = float(np.corrcoef(rs, rt)[0, 1])
# between-model relation
F["between_model_spearman_score_tokens"] = float(effR.score.rank().corr(effR.tokens.rank()))

# ------------------------------------------------------------------ variance of log tokens
lt = np.log(R.tokens_scored_file)
tot = ((lt - lt.mean()) ** 2).sum()
def r2(cols):
    d = pd.get_dummies(R[cols].astype(str), drop_first=False).to_numpy(float)
    b, *_ = np.linalg.lstsq(d, lt.to_numpy(), rcond=None)
    return 1 - ((lt.to_numpy() - d @ b) ** 2).sum() / tot
F["var_share_model_only"] = float(r2(["model"]))
F["var_share_problem_only"] = float(r2(["problem"]))
F["var_share_model_problem_protocol"] = float(r2(["model", "problem", "protocol"]))
# same problem, different models; same model, different problems
v2 = R[R.protocol == "v2"]
gp = v2.groupby("problem").tokens_scored_file.agg(["max", "min", "size"])
gp = gp[gp["size"] >= 4]
F["same_problem_max_over_min_median"] = float((gp["max"] / gp["min"]).median())
F["same_problem_max_over_min_max"] = float((gp["max"] / gp["min"]).max())
gm = R.groupby(["model", "protocol"]).tokens_scored_file.agg(["max", "min", "size"])
gm = gm[gm["size"] >= 5]
F["same_model_max_over_min_median"] = float((gm["max"] / gm["min"]).median())
# turns vs per-turn context: which one separates models?
a, b = np.log(effR.turns), np.log(effR.tok_per_turn)
F["model_token_gap_share_from_turns"] = float(np.cov(a, a + b)[0, 1] / np.var(a + b, ddof=1))
F["corr_logtokens_logturns_within"] = float(np.corrcoef(rt, fit(R, np.log(R.assistant_turns.clip(lower=1).to_numpy(float)))[3])[0, 1])

# ------------------------------------------------------------------ behaviour (reliable set)
cats = ["inspect", "construct", "modify", "prototype", "verify"]
B = R[R.tool_calls > 0].copy()
g = B.groupby(["model", "protocol"])
beh = pd.DataFrame({"runs": g.size(), "turns_median": g.assistant_turns.median(), "calls_median": g.tool_calls.median(),
                    "tokens_M_median": g.tokens_scored_file.median() / 1e6})
for c in cats:
    beh[f"calls_{c}_share"] = g[f"calls_{c}"].sum() / g.tool_calls.sum()
real_err = g.tool_errors.sum() - g.tool_errors_intentional.sum()
beh["error_rate"] = real_err / g.tool_calls_answered.sum()
beh["model_caused_share_of_errors"] = g.tool_errors_model.sum() / real_err
beh["same_error_repeats_per_run"] = g.same_error_repeats.sum() / g.size()
beh["duplicate_calls_per_run"] = g.duplicate_calls.sum() / g.size()
occ = ["inspect", "construct", "modify", "prototype", "verify", "setup", "other_tool"]
tot_c = g.carry_chars_total.sum()
for c in occ:
    beh[f"ctx_{c}"] = g[f"carry_chars_{c}"].sum() / tot_c
beh["ctx_fixed_prompt"] = (g.carry_chars_fixed_prompt.sum() + g.carry_chars_harness_reminders.sum()) / tot_c
beh["ctx_assistant_text"] = g.carry_chars_assistant_text.sum() / tot_c
beh.to_csv(os.path.join(TAB, "R_3_behaviour.csv"))
print(beh.round(2).to_string())

# drivers of tokens within model+problem
drv = []
for col, label in [("assistant_turns", "turns"), ("calls_construct", "construct calls"), ("calls_modify", "modify calls"),
                   ("calls_inspect", "inspect calls"), ("tool_errors_model", "model-caused errors"),
                   ("same_error_repeats", "same error repeated"), ("duplicate_calls", "duplicate calls"),
                   ("calls_with_delete", "calls that delete"), ("largest_result_chars", "largest tool result")]:
    x = fit(B, np.log1p(B[col].fillna(0).to_numpy(float)))[3]
    y = fit(B, np.log(B.tokens_scored_file.to_numpy(float)))[3]
    drv.append({"feature": label, "partial_r": float(pd.Series(x).rank().corr(pd.Series(y).rank()))})
drv = pd.DataFrame(drv).sort_values("partial_r", ascending=False)
drv.to_csv(os.path.join(TAB, "R_3_token_drivers.csv"), index=False)
print(drv.round(2).to_string(index=False))

# errors: does failing more cost more / score less, within model+problem?
er = fit(B, np.log1p((B.tool_errors_model).fillna(0).to_numpy(float)))[3]
F["partial_r_model_errors_vs_score"] = float(np.corrcoef(er, fit(B, B.score_total.to_numpy(float))[3])[0, 1])

# ------------------------------------------------------------------ reasoning-effort check (v2 only, models with both settings)
E = R[(R.protocol == "v2") & R.requested_effort.isin(["low", "not_set"])].copy()
mix = E.groupby("model").requested_effort.nunique()
E = E[E.model.isin(mix[mix > 1].index)]
if len(E) > 20:
    ind = (E.requested_effort == "low").to_numpy(float)[:, None]
    for name, y in [("tokens", np.log(E.tokens_scored_file.to_numpy(float))), ("score", E.score_total.to_numpy(float))]:
        X, ms, ps = design(E, ind)
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        F[f"effort_low_vs_notset_{name}"] = float(np.exp(beta[-1]) if name == "tokens" else beta[-1])
    F["effort_check_n"] = len(E)
    F["effort_check_models"] = sorted(E.model.unique())
    print("effort low vs not_set:", F["effort_low_vs_notset_tokens"], F["effort_low_vs_notset_score"], len(E), F["effort_check_models"])

# G0 failures
F["g0_fail_n"] = int((~R.g0).sum())
F["g0_fail_by_model"] = R[~R.g0].groupby("model").size().to_dict()
F["g0_fail_token_ratio_vs_pass_within_model_problem"] = float(np.exp(R.loc[~R.g0, "logtok_resid"].mean() - R.loc[R.g0, "logtok_resid"].mean()))

R.to_csv(os.path.join(OUT, "reliable_runs.csv"), index=False)
json.dump(F, open(os.path.join(OUT, "findings.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps(F, indent=1, ensure_ascii=False))
