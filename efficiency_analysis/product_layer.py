"""Product layer: what the delivered Figma file actually contains, from its layer snapshot.

One snapshot per run: the judged revision's `benchmark-layers.json` (this batch) or the run's own
snapshot (earlier package). Each snapshot lists the product screens ("boards") with node, depth,
instance, text and image counts, the six most frequent node types, and the first six layer names.
The judge reads this same summary when it scores G1 and G2, so those two items are only checked
for consistency, never used as evidence.

Writes out/product_runs.csv, out/product_boards.csv and out/tables/R_8_*.csv.
Usage: .venv/bin/python product_layer.py out [reps]
"""
import glob
import json
import os
import re
import sys

import numpy as np
import pandas as pd

OUT = sys.argv[1]
REPS = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
TAB = os.path.join(OUT, "tables")
HERE = os.path.dirname(os.path.abspath(__file__))
NEW = os.path.join(HERE, "..", "new_output-246-29x4-13x10")
NEWL = os.path.join(HERE, "..", "distributed-246-layers-only", "layers-only")
OLD = os.path.join(HERE, "..", "benchmark_output")
rng = np.random.default_rng(23)
pd.set_option("display.width", 240)

R = pd.read_csv(os.path.join(OUT, "reliable_runs.csv"), low_memory=False)
src = pd.read_csv(os.path.join(OUT, "runs.csv"), low_memory=False).set_index("task_id").source_folder
idx = pd.read_csv(os.path.join(OLD, "metadata/portable_run_index.csv"), encoding="utf-8-sig").set_index("run_id")

DEFAULT_NAME = re.compile(r"^(Frame|Rectangle|Ellipse|Group|Vector|Text|Line|Polygon|Star|Component|Instance|Union|"
                          r"Subtract|Section|Image|Auto layout)( \d+)?$")


def snapshot(r):
    if r.protocol == "v2":
        s = os.path.join(NEW, src[r.task_id], r.task_id, "score.json")
        rev = (json.load(open(s)).get("candidate") or {}).get("revision") if os.path.exists(s) else None
        f = os.path.join(NEWL, f"{r.task_id}-{rev}__benchmark-layers.json")
    else:
        f = os.path.join(OLD, os.path.dirname(os.path.dirname(idx.loc[r.task_id, "trajectory_path"])), "benchmark-layers.json")
    return json.load(open(f)) if os.path.exists(f) else None


boards, missing = [], []
for _, r in R.iterrows():
    snap = snapshot(r)
    if not snap:
        missing.append(r.task_id)
        continue
    for k, b in enumerate(snap.get("boards") or []):
        types = {}
        for t in b.get("types") or []:
            m = re.match(r"(.+?)×(\d+)$", t)
            if m:
                types[m.group(1)] = int(m.group(2))
        names = b.get("names") or []
        boards.append(dict(task_id=r.task_id, model=r.model, problem=r.problem, protocol=r.protocol, board=k,
                           nodes=b.get("nodes") or 0, max_depth=b.get("max_depth") or 0,
                           instances=b.get("instances") or 0, texts=b.get("texts") or 0, images=b.get("images") or 0,
                           types_listed=sum(types.values()), n_types_listed=len(types),
                           frame_listed=types.get("frame", 0), rectangle_listed=types.get("rectangle", 0),
                           vector_listed=types.get("vector", 0), group_listed=types.get("group", 0),
                           ellipse_listed=types.get("ellipse", 0),
                           names_listed=len(names), default_names=sum(bool(DEFAULT_NAME.match(n)) for n in names)))
B = pd.DataFrame(boards)
B.to_csv(os.path.join(OUT, "product_boards.csv"), index=False)
print(f"reliable runs {len(R)}, with snapshot {B.task_id.nunique()}, missing {len(missing)}; screens {len(B)}")
print("screens with 0 nodes:", int((B.nodes == 0).sum()))
cov = B.types_listed / B.nodes.replace(0, np.nan)
print("share of nodes covered by the six listed types: median %.2f, p10 %.2f" % (cov.median(), cov.quantile(.1)))

g = B[B.nodes > 0].groupby("task_id")
P = pd.DataFrame({
    "screens": B.groupby("task_id").size(),
    "empty_screens": B.groupby("task_id").nodes.apply(lambda s: int((s == 0).sum())),
    "nodes_per_screen": g.nodes.median(),
    "max_depth": g.max_depth.median(),
    "instances_per_screen": g.instances.median(),
    "texts_per_screen": g.texts.median(),
    "images_per_screen": g.images.median(),
    "instance_node_share": g.instances.sum() / g.nodes.sum(),
    "text_node_share": g.texts.sum() / g.nodes.sum(),
    "frame_share_lb": g.frame_listed.sum() / g.nodes.sum(),
    "rectangle_share_lb": g.rectangle_listed.sum() / g.nodes.sum(),
    "vector_share_lb": g.vector_listed.sum() / g.nodes.sum(),
    "group_share_lb": g.group_listed.sum() / g.nodes.sum(),
    "default_name_share": g.default_names.sum() / g.names_listed.sum().replace(0, np.nan),
}).reset_index()
P = P.merge(R[["task_id", "model", "problem", "protocol", "score_total", "g0_pass"] + [c for c in R if c.startswith("rubric_")]],
            on="task_id")
P.to_csv(os.path.join(OUT, "product_runs.csv"), index=False)

# ---------------------------------------------------------------- 1. what was delivered
D = P.groupby(["model", "protocol"]).agg(
    runs=("task_id", "size"), nodes_per_screen=("nodes_per_screen", "median"), max_depth=("max_depth", "median"),
    instance_node_share=("instance_node_share", "median"), instances_per_screen=("instances_per_screen", "median"),
    text_node_share=("text_node_share", "median"), images_per_screen=("images_per_screen", "median"),
    vector_share_lb=("vector_share_lb", "median"), rectangle_share_lb=("rectangle_share_lb", "median"),
    group_share_lb=("group_share_lb", "median"), default_name_share=("default_name_share", "median"),
    empty_screens=("empty_screens", "sum"))
D.to_csv(os.path.join(TAB, "R_8_delivered_structure.csv"))
print("\n== delivered structure (median run)\n", D.round(2).to_string())


SPEC = {"unit": "model"}  # "model" = as pre-registered (one protocol shift); "model_protocol" = one mean per model x batch


def resid(df, y):
    key = df.model if SPEC["unit"] == "model" else df.model + " @ " + df.protocol
    ms, ps = sorted(key.unique()), sorted(df.problem.unique())
    X = np.zeros((len(df), len(ms) + len(ps) + 1))
    X[np.arange(len(df)), key.map({m: i for i, m in enumerate(ms)}).to_numpy()] = 1
    X[np.arange(len(df)), len(ms) + df.problem.map({p: i for i, p in enumerate(ps)}).to_numpy()] = 1
    X[:, -1] = (df.protocol == "v1").to_numpy(float) if SPEC["unit"] == "model" else 0.0
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    return y - X @ b, pd.Series(b[:len(ms)] - b[:len(ms)].mean(), index=ms)


def prs(df, x, y):
    a, _ = resid(df, df[x].to_numpy(float))
    b, _ = resid(df, df[y].to_numpy(float))
    return float(pd.Series(a).rank().corr(pd.Series(b).rank()))


def boot(df, x, y, sign=1):
    d = df[df[x].notna() & df[y].notna()].reset_index(drop=True)
    r0 = prs(d, x, y)
    groups = {p: gg.index.to_numpy() for p, gg in d.groupby("problem")}
    ps = list(groups)
    bs = []
    for _ in range(REPS):
        ii = np.concatenate([groups[p] for p in rng.choice(ps, len(ps))])
        v = prs(d.loc[ii].reset_index(drop=True), x, y)
        if not np.isnan(v):
            bs.append(v)
    bs = np.array(bs)
    return dict(n=len(d), r=r0, lo=float(np.quantile(bs, .025)), hi=float(np.quantile(bs, .975)),
                p_one_sided=float(np.mean(bs * sign <= 0)))


for spec in ["model", "model_protocol"]:
    SPEC["unit"] = spec
    tag = "" if spec == "model" else "_by_batch"
    print(f"\n################ adjustment: {spec}")
    # ---------------------------------------------------------------- 2. does the process layer match the product?
    O = pd.read_csv(os.path.join(OUT, "design_ops_runs.csv"), low_memory=False)
    J = P.merge(O[["task_id", "instance_share", "reuse_ratio", "primitive_share", "text_share", "autolayout_ratio",
                   "frame_share", "naming_ratio"]], on="task_id")
    pairs = [("instance_share", "instance_node_share", "instances: code share vs file share"),
             ("reuse_ratio", "instance_node_share", "reuse ratio (code) vs instance share (file)"),
             ("text_share", "text_node_share", "text layers: code share vs file share"),
             ("primitive_share", "vector_share_lb", "primitive shapes (code) vs vector nodes (file)"),
             ("autolayout_ratio", "max_depth", "auto-layout (code) vs nesting depth (file)"),
             ("naming_ratio", "default_name_share", "naming (code) vs default names (file), expect negative")]
    rows = []
    for a, b, lab in pairs:
        d = J[J[a].notna() & J[b].notna()]
        raw = float(d[a].rank().corr(d[b].rank()))
        _, ea = resid(d.reset_index(drop=True), d[a].to_numpy(float))
        _, eb = resid(d.reset_index(drop=True), d[b].to_numpy(float))
        rows.append(dict(check=lab, n=len(d), across_runs=raw, within_model_task=prs(d.reset_index(drop=True), a, b),
                         between_models=float(ea.rank().corr(eb.rank()))))
    V = pd.DataFrame(rows)
    V.to_csv(os.path.join(TAB, f"R_8_process_vs_product{tag}.csv"), index=False)
    print("\n== process layer (code) vs product layer (file), Spearman\n", V.round(2).to_string(index=False))

    # ---------------------------------------------------------------- 3. consistency check: judge vs the summary it reads
    Q = P[P.g0_pass.astype(str).eq("True")]
    cc = [("default_name_share", "rubric_G1", -1), ("max_depth", "rubric_G2", 1), ("instance_node_share", "rubric_G2", 1)]
    C = pd.DataFrame([dict(measure=a, item=b, **boot(Q, a, b, s)) for a, b, s in cc])
    C.to_csv(os.path.join(TAB, f"R_8_judge_consistency{tag}.csv"), index=False)
    print("\n== consistency (judge reads these fields for G1/G2; not evidence)\n", C.round(3).to_string(index=False))

    # ---------------------------------------------------------------- 4. pre-registered tests
    H = [("P1a", "instance_node_share", "rubric_E1", 1), ("P1b", "instance_node_share", "rubric_E2", 1),
         ("P1c", "instance_node_share", "rubric_B4", 1), ("P2", "images_per_screen", "rubric_F5", 1),
         ("P3", "nodes_per_screen", "rubric_D4", 1)]
    T = pd.DataFrame([dict(hypothesis=h, measure=a, item=b.replace("rubric_", ""), expected="+" if s > 0 else "-", **boot(Q, a, b, s))
                      for h, a, b, s in H])
    order = T.p_one_sided.sort_values().index
    run, holm = 0.0, {}
    for k, i in enumerate(order):
        run = max(run, min(1.0, (len(T) - k) * T.loc[i, "p_one_sided"]))
        holm[i] = run
    T["p_holm"] = pd.Series(holm)
    T["supported"] = T.p_holm < 0.05
    # between models, descriptive
    _, es = resid(Q.reset_index(drop=True), Q.score_total.to_numpy(float))
    for c in ["instance_node_share", "images_per_screen", "nodes_per_screen"]:
        _, ec = resid(Q.reset_index(drop=True), Q[c].to_numpy(float))
        T.loc[T.measure == c, "between_models_vs_total"] = float(ec.rank().corr(es.rank()))
    for i, r in T.iterrows():
        _, ec = resid(Q.reset_index(drop=True), Q[r.measure].to_numpy(float))
        _, ei = resid(Q.reset_index(drop=True), Q[f"rubric_{r['item']}"].to_numpy(float))
        T.loc[i, "between_models_vs_item"] = float(ec.rank().corr(ei.rank()))
    T.to_csv(os.path.join(TAB, f"R_8_hypothesis_tests{tag}.csv"), index=False)
    print("\n== pre-registered product-layer tests\n", T.round(3).to_string(index=False))
