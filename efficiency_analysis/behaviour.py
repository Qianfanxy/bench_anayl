"""Does what a model DOES during inference relate to the quality it delivers?

Behaviour is measured per run from the trajectory: how many calls of each kind, how the input
context is occupied, how often it errs and repeats itself. Then three questions:
  Q1 model fingerprints  - what each model characteristically does
  Q2 between models      - do models that behave a certain way score higher? (n = 10 models)
  Q3 within a model      - when a run deviates from that model's own habit, does the score move?
Q3 cannot separate cause from effect: a run going badly also produces more retries.

Usage: .venv/bin/python behaviour.py out [reps=1000]
"""
import json
import os
import sys

import numpy as np
import pandas as pd

OUT = sys.argv[1]
REPS = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
TAB = os.path.join(OUT, "tables")
rng = np.random.default_rng(11)
R = pd.read_csv(os.path.join(OUT, "reliable_runs_cost.csv"), low_memory=False)
R = R[(R.tool_calls > 0) & R.score_total.notna()].copy()
E = pd.read_csv(os.path.join(TAB, "R_1_model_effects_reliable.csv"), index_col=0)
F = json.load(open(os.path.join(OUT, "findings.json")))

CATS = ["inspect", "construct", "modify", "prototype", "verify"]
R["calls_write"] = R[[f"calls_{c}" for c in ["construct", "modify", "prototype"]]].sum(axis=1)
R["real_errors"] = R.tool_errors - R.tool_errors_intentional.fillna(0)
M = {  # behaviour measures, all per-run and scale-free
    "read_share": R.calls_inspect / R.tool_calls,
    "revise_share": R.calls_modify / R.tool_calls,
    "build_share": R.calls_construct / R.tool_calls,
    "revise_per_build": R.calls_modify / R.calls_construct.replace(0, np.nan),
    "reads_per_write": R.calls_inspect / R.calls_write.replace(0, np.nan),
    "ctx_read_share": R.carry_chars_inspect / R.carry_chars_total,
    "ctx_write_share": (R.carry_chars_construct + R.carry_chars_modify) / R.carry_chars_total,
    "error_rate": R.real_errors / R.tool_calls_answered,
    "repeat_error_rate": R.same_error_repeats / R.tool_calls_answered,
    "duplicate_call_rate": R.duplicate_calls / R.tool_calls,
    "delete_rate": R.calls_with_delete / R.tool_calls,
    "calls_per_turn": R.tool_calls / R.assistant_turns,
    "chars_per_call": R.carry_chars_total / R.tool_calls,
}
for k, v in M.items():
    R[k] = v.replace([np.inf, -np.inf], np.nan)
KEYS = list(M)


def two_way(df, y):
    """Residual of y after removing model, problem and protocol means (least squares)."""
    ms, ps = sorted(df.model.unique()), sorted(df.problem.unique())
    X = np.zeros((len(df), len(ms) + len(ps) + 1))
    X[np.arange(len(df)), df.model.map({m: i for i, m in enumerate(ms)}).to_numpy()] = 1
    X[np.arange(len(df)), len(ms) + df.problem.map({p: i for i, p in enumerate(ps)}).to_numpy()] = 1
    X[:, -1] = (df.protocol == "v1").to_numpy(float)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    eff = pd.Series(beta[:len(ms)] - beta[:len(ms)].mean(), index=ms)
    return y - X @ beta, eff


def spear(a, b):
    a, b = pd.Series(a), pd.Series(b)
    k = a.notna() & b.notna()
    return float(a[k].rank().corr(b[k].rank())) if k.sum() > 3 else np.nan


# ---------------------------------------------------------------- Q1 fingerprints
fp = R.groupby(["model", "protocol"])[KEYS].median().round(3)
fp["runs"] = R.groupby(["model", "protocol"]).size()
fp.to_csv(os.path.join(TAB, "R_5_behaviour_fingerprint.csv"))
pd.set_option("display.width", 250)
print("== per-model behaviour (median run)\n", fp.to_string())

# ---------------------------------------------------------------- Q2 between models
rows = []
for k in KEYS:
    d = R[R[k].notna()]
    _, eff = two_way(d, d[k].to_numpy(float))
    rows.append({"behaviour": k, "spearman_with_score": spear(eff, E.score.reindex(eff.index)),
                 "spearman_with_tokens": spear(eff, E.tokens.reindex(eff.index)),
                 "spearman_with_cost": spear(eff, E.cost.reindex(eff.index)),
                 "models": len(eff)})
    E[f"b_{k}"] = eff
between = pd.DataFrame(rows).sort_values("spearman_with_score")
between.to_csv(os.path.join(TAB, "R_5_between_model_correlates.csv"), index=False)
print("\n== between models (n=10, Spearman; adjusted for problem and protocol)\n", between.round(2).to_string(index=False))
E.to_csv(os.path.join(TAB, "R_1_model_effects_reliable.csv"))

# ---------------------------------------------------------------- Q3 within model and problem
sr, _ = two_way(R, R.score_total.to_numpy(float))
R["score_resid2"] = sr
rows = []
for k in KEYS:
    d = R[R[k].notna()]
    br, _ = two_way(d, np.log(d[k].to_numpy(float) + 1e-6) if d[k].min() > 0 else d[k].to_numpy(float))
    s2, _ = two_way(d, d.score_total.to_numpy(float))
    r = spear(br, s2)
    # bootstrap over problems
    bs = []
    groups = {p: g.index for p, g in d.groupby("problem")}
    ps = list(groups)
    for _ in range(REPS):
        idx = np.concatenate([groups[p] for p in rng.choice(ps, len(ps))])
        dd = d.loc[idx]
        if dd.model.nunique() < 3:
            continue
        b2, _ = two_way(dd, np.log(dd[k].to_numpy(float) + 1e-6) if dd[k].min() > 0 else dd[k].to_numpy(float))
        s3, _ = two_way(dd, dd.score_total.to_numpy(float))
        bs.append(spear(b2, s3))
    rows.append({"behaviour": k, "n": len(d), "partial_spearman_with_score": r,
                 "lo": float(np.nanquantile(bs, .025)), "hi": float(np.nanquantile(bs, .975))})
within = pd.DataFrame(rows).sort_values("partial_spearman_with_score")
within.to_csv(os.path.join(TAB, "R_5_within_model_correlates.csv"), index=False)
print("\n== within model+problem (does a run that deviates from habit score differently?)\n", within.round(2).to_string(index=False))

# ---------------------------------------------------------------- screenshots: only where allowed
v1 = R[(R.protocol == "v1") & R.calls_verify.notna()]
out = {}
if len(v1) > 30:
    vr, veff = two_way(v1, np.log1p(v1.calls_verify.to_numpy(float)))
    s1, _ = two_way(v1, v1.score_total.to_numpy(float))
    out["screenshot_within_r"] = spear(vr, s1)
    out["screenshot_between_r"] = spear(veff, E.score.reindex(veff.index))
    out["screenshot_share_of_calls_by_model"] = (v1.groupby("model").calls_verify.sum() / v1.groupby("model").tool_calls.sum()).round(3).to_dict()
F.update({"behaviour_" + k: v for k, v in out.items()})
F["behaviour_between_top3"] = {m: {k: float(E.loc[m, f"b_{k}"]) for k in ["read_share", "revise_share", "reads_per_write", "error_rate"]}
                               for m in ["Opus 5.5（三方A）", "Sonnet 5.5", "gpt-6-astra", "DeepSeek V4 Flash", "Gemini 3.5 Flash"]}
json.dump(F, open(os.path.join(OUT, "findings.json"), "w"), indent=1, ensure_ascii=False)
print("\n== screenshots (earlier protocol only)", json.dumps(out, ensure_ascii=False, indent=1))
R.to_csv(os.path.join(OUT, "reliable_runs_behaviour.csv"), index=False)
