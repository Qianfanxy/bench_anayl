"""Process layer: HOW each model builds the design, from the Plugin API code of its write calls.

For every reliable run, every write call (build / revise / wire) is scanned for Figma operations.
Counts are static: a helper or loop that creates 20 nodes counts once, so the measures describe
the construction METHOD a model uses, not how many nodes it produced. Calls whose code the harness
elided are skipped.

Modes:
  extract   -> out/design_ops_runs.csv, out/design_ops_calls.csv, prints per-model profiles
  validate  -> prints random matches per operation, with context, for manual checking
  test      -> tests the hypotheses fixed in design_ops_hypotheses.md

Usage: .venv/bin/python design_ops.py out extract|validate|test [reps]
"""
import collections
import glob
import importlib.util
import json
import os
import random
import re
import sys

import numpy as np
import pandas as pd

OUT, MODE = sys.argv[1], sys.argv[2]
REPS = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("tf", os.path.join(HERE, "trajfeat.py"))
tf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tf)
NEW = os.path.join(HERE, "..", "new_output-246-29x4-13x10")
OLD = os.path.join(HERE, "..", "benchmark_output")

OPS = {  # operation -> pattern (counted per occurrence)
    "instance": r"\.createInstance\s*\(|importComponent(?:Set)?ByKeyAsync\s*\(",
    "own_component": r"figma\.createComponent(?:FromNode)?\s*\(|combineAsVariants\s*\(",
    "clone": r"\.clone\s*\(\s*\)",
    "frame": r"figma\.create(?:Frame|AutoLayout|Section)\s*\(",
    "primitive": r"figma\.create(?:Rectangle|Ellipse|Line|Vector|Polygon|Star)\s*\(|createNodeFromSvg\s*\(",
    "text": r"figma\.createText\s*\(",
    "group": r"figma\.(?:group|union|subtract|flatten)\s*\(",
    "autolayout": r"layoutMode\s*=(?!=)\s*(?![\"'`]NONE)",
    "naming": r"\.name\s*=(?!=)",
    "instance_override": r"\.setProperties\s*\(|\.swapComponent\s*\(|\.mainComponent\s*=(?!=)",
    "style_or_variable": r"setBoundVariable|(?:text|fill|stroke|effect)StyleId|set(?:Text|Fill|Stroke|Effect)StyleIdAsync",
    "image": r"[\"'`]IMAGE[\"'`]|imageHash|createImage",
    "text_edit": r"\.characters\s*=(?!=)",
}
OPS = {k: re.compile(v) for k, v in OPS.items()}
CREATE = ["instance", "own_component", "clone", "frame", "primitive", "text"]


def run_files(R):
    """(task_id, protocol, model, problem, path) for every trajectory counted in the run's cost."""
    att = pd.read_csv(os.path.join(OUT, "attempts.csv"), low_memory=False)
    att = att[att.counted_in_run_totals.astype(str).eq("True")]
    nb = pd.read_csv(os.path.join(OUT, "runs.csv"), low_memory=False).set_index("task_id").source_folder
    idx = {r["run_id"]: r["trajectory_path"] for r in
           pd.read_csv(os.path.join(OLD, "metadata/portable_run_index.csv"), encoding="utf-8-sig").to_dict("records")}
    for _, r in R.iterrows():
        if r.protocol == "v2":
            for f in att[att.task_id == r.task_id].trajectory_file:
                yield r.task_id, r.protocol, r.model, r.problem, os.path.join(NEW, nb[r.task_id], r.task_id, f)
        else:
            yield r.task_id, r.protocol, r.model, r.problem, os.path.join(OLD, idx[r.task_id])


def write_calls(path):
    with open(path) as fh:
        rec = json.loads([l for l in fh if l.strip()][-1])
    for m in tf.normalize_messages(rec.get("messages") or []):
        for tc in m.get("tool_calls") or []:
            fn = tc.get("function") or {}
            a = fn.get("arguments")
            if isinstance(a, str):
                try:
                    a = json.loads(a)
                except ValueError:
                    continue
            if not isinstance(a, dict) or "code" not in a:
                continue
            cat = tf.classify_call(fn.get("name"), a)[0]
            if cat not in ("construct", "modify", "prototype"):
                continue
            code = a.get("code") or ""
            yield cat, code, tf.ELIDED_MARK in code


R = pd.read_csv(os.path.join(OUT, "reliable_runs.csv"), low_memory=False)

if MODE == "validate":
    random.seed(3)
    hits = collections.defaultdict(list)
    for tid, proto, model, prob, path in run_files(R):
        for cat, code, elided in write_calls(path):
            if elided:
                continue
            for op, pat in OPS.items():
                for mm in pat.finditer(code):
                    hits[op].append((model, re.sub(r"\s+", " ", code[max(0, mm.start() - 70): mm.end() + 50])))
    for op, h in hits.items():
        print(f"\n## {op}  ({len(h)} matches)")
        for model, ctx in random.sample(h, min(6, len(h))):
            print(f"  [{model[:14]}] ...{ctx}...")
    sys.exit()

if MODE == "extract":
    calls, runs = [], []
    for tid, proto, model, prob, path in run_files(R):
        for k, (cat, code, elided) in enumerate(write_calls(path)):
            row = dict(task_id=tid, protocol=proto, model=model, problem=prob, file=os.path.basename(path),
                       k=k, category=cat, elided=elided, code_chars=len(code))
            for op, pat in OPS.items():
                row[op] = 0 if elided else len(pat.findall(code))
            calls.append(row)
    C = pd.DataFrame(calls)
    C.to_csv(os.path.join(OUT, "design_ops_calls.csv"), index=False)
    ok = C[~C.elided]
    g = ok.groupby("task_id")
    D = g[list(OPS)].sum()
    D["write_calls"] = g.size()
    D["elided_write_calls"] = C.groupby("task_id").elided.sum().reindex(D.index).fillna(0)
    for op in OPS:  # presence share: robustness version that ignores how often an op repeats in one call
        D[f"has_{op}"] = (ok[op] > 0).groupby(ok.task_id).mean()
    creations = D[CREATE].sum(axis=1).replace(0, np.nan)
    D["reuse_ratio"] = D.instance / (D.instance + D.primitive + D.frame).replace(0, np.nan)
    D["own_components"] = (D.own_component > 0).astype(float)
    D["clone_ratio"] = D.clone / creations
    D["autolayout_ratio"] = D.autolayout / D.frame.replace(0, np.nan)
    D["naming_ratio"] = D.naming / creations
    D["primitive_share"] = D.primitive / creations
    D["text_share"] = D.text / creations
    D["frame_share"] = D.frame / creations
    D["instance_share"] = D.instance / creations
    D = D.join(R.set_index("task_id")[["model", "problem", "protocol", "score_total", "g0_pass"]
                                      + [c for c in R if c.startswith("rubric_")]])
    D.reset_index().to_csv(os.path.join(OUT, "design_ops_runs.csv"), index=False)
    pd.set_option("display.width", 250)
    prof = D.groupby(["model", "protocol"])[["write_calls", "instance_share", "frame_share", "primitive_share", "text_share",
                                             "clone_ratio", "reuse_ratio", "own_components", "autolayout_ratio",
                                             "naming_ratio"]].median()
    prof["runs"] = D.groupby(["model", "protocol"]).size()
    prof["elided_share"] = (D.groupby(["model", "protocol"]).elided_write_calls.sum()
                            / (D.groupby(["model", "protocol"]).write_calls.sum() + D.groupby(["model", "protocol"]).elided_write_calls.sum()))
    prof.to_csv(os.path.join(OUT, "tables", "R_7_construction_profile.csv"))
    print(prof.round(2).to_string())
    sys.exit()

if MODE == "test":
    from math import isnan
    D = pd.read_csv(os.path.join(OUT, "design_ops_runs.csv"), low_memory=False)
    D = D[D.g0_pass.astype(str).eq("True")].copy()
    rng = np.random.default_rng(17)
    H = [("H1a", "reuse_ratio", "E1", 1), ("H1b", "reuse_ratio", "E2", 1), ("H1c", "reuse_ratio", "B4", 1),
         ("H2", "own_components", "E1", 1), ("H3", "clone_ratio", "E2", 1),
         ("H4a", "autolayout_ratio", "D1", 1), ("H4b", "autolayout_ratio", "D2", 1), ("H4c", "autolayout_ratio", "G2", 1),
         ("H5", "naming_ratio", "G1", 1), ("H6a", "primitive_share", "B4", -1), ("H6b", "primitive_share", "F5", -1)]

    def resid(df, y):
        ms, ps = sorted(df.model.unique()), sorted(df.problem.unique())
        X = np.zeros((len(df), len(ms) + len(ps) + 1))
        X[np.arange(len(df)), df.model.map({m: i for i, m in enumerate(ms)}).to_numpy()] = 1
        X[np.arange(len(df)), len(ms) + df.problem.map({p: i for i, p in enumerate(ps)}).to_numpy()] = 1
        X[:, -1] = (df.protocol == "v1").to_numpy(float)
        b, *_ = np.linalg.lstsq(X, y, rcond=None)
        return y - X @ b

    def prs(df, x, y):
        a = pd.Series(resid(df, df[x].to_numpy(float)))
        b = pd.Series(resid(df, df[y].to_numpy(float)))
        return float(a.rank().corr(b.rank()))

    rows = []
    for hid, x, item, sign in H:
        y = f"rubric_{item}"
        d = D[D[x].notna() & D[y].notna()].reset_index(drop=True)
        r0 = prs(d, x, y)
        groups = {p: g.index.to_numpy() for p, g in d.groupby("problem")}
        ps = list(groups)
        bs = []
        for _ in range(REPS):
            idx = np.concatenate([groups[p] for p in rng.choice(ps, len(ps))])
            bs.append(prs(d.loc[idx].reset_index(drop=True), x, y))
        bs = np.array([v for v in bs if not isnan(v)])
        p_one = float(np.mean(bs * sign <= 0))  # one-sided, in the predicted direction
        rows.append(dict(hypothesis=hid, measure=x, item=item, expected="+" if sign > 0 else "-", n=len(d),
                         r=r0, lo=float(np.quantile(bs, .025)), hi=float(np.quantile(bs, .975)), p_one_sided=p_one))
    T = pd.DataFrame(rows)
    order = T.p_one_sided.sort_values().index
    m = len(T)
    holm, running = {}, 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * T.loc[i, "p_one_sided"]))
        holm[i] = running
    T["p_holm"] = pd.Series(holm)
    T["supported"] = (T.p_holm < 0.05)
    T.to_csv(os.path.join(OUT, "tables", "R_7_hypothesis_tests.csv"), index=False)
    pd.set_option("display.width", 220)
    print(T.round(3).to_string(index=False))

if MODE == "test":
    # robustness: presence-based versions of the two non-null results (not part of the 11 tests)
    rob = []
    for hid, x, item in [("H4c", "has_autolayout", "G2"), ("H5", "has_naming", "G1"), ("H4a", "has_autolayout", "D1")]:
        d = D[D[x].notna() & D[f"rubric_{item}"].notna()].reset_index(drop=True)
        rob.append(dict(hypothesis=hid, measure=x, item=item, r=prs(d, x, f"rubric_{item}"), n=len(d)))
    rob = pd.DataFrame(rob)
    rob.to_csv(os.path.join(OUT, "tables", "R_7_robustness_presence.csv"), index=False)
    print("\n== robustness (presence share instead of occurrence ratio)\n", rob.round(3).to_string(index=False))

    # between models (n = 10): descriptive only
    def effects(df, col):
        ms, ps = sorted(df.model.unique()), sorted(df.problem.unique())
        X = np.zeros((len(df), len(ms) + len(ps) + 1))
        X[np.arange(len(df)), df.model.map({m: i for i, m in enumerate(ms)}).to_numpy()] = 1
        X[np.arange(len(df)), len(ms) + df.problem.map({p: i for i, p in enumerate(ps)}).to_numpy()] = 1
        X[:, -1] = (df.protocol == "v1").to_numpy(float)
        b, *_ = np.linalg.lstsq(X, df[col].to_numpy(float), rcond=None)
        return pd.Series(b[:len(ms)] - b[:len(ms)].mean(), index=ms)
    meas = ["reuse_ratio", "own_components", "instance_share", "frame_share", "primitive_share", "text_share", "clone_ratio",
            "autolayout_ratio", "naming_ratio"]
    eff = pd.DataFrame({c: effects(D[D[c].notna()], c) for c in meas + ["score_total"]
                        + [f"rubric_{k}" for k in ["E1", "E2", "B4", "D1", "D2", "G1", "G2", "F5"]]})
    eff.to_csv(os.path.join(OUT, "tables", "R_7_model_effects_strategy.csv"))
    bt = []
    for hid, x, item, sign in H:
        bt.append(dict(hypothesis=hid, measure=x, item=item, between_model_spearman=float(eff[x].rank().corr(eff[f"rubric_{item}"].rank()))))
    for x in meas:
        bt.append(dict(hypothesis="-", measure=x, item="total score", between_model_spearman=float(eff[x].rank().corr(eff.score_total.rank()))))
    bt = pd.DataFrame(bt)
    bt.to_csv(os.path.join(OUT, "tables", "R_7_between_model.csv"), index=False)
    print("\n== between models (10 points, descriptive)\n", bt.round(2).to_string(index=False))
