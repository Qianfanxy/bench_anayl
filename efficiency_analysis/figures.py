"""Publication figures for the efficiency analysis (reliable set).

Reads out/reliable_runs.csv, out/all_runs_labelled.csv, out/findings.json, out/tables/R_*.csv.
Writes vector PDF + 600-dpi PNG to <out>/figures.

Usage: .venv/bin/python figures.py out
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

OUT = sys.argv[1]
FIG = os.path.join(OUT, "figures")
os.makedirs(FIG, exist_ok=True)

INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#8a897f", "#e6e5e0"
BLUE, ORANGE, AQUA, YELLOW, NEUTRAL = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#b9b8b0"
plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 7.5, "axes.labelsize": 8, "axes.titlesize": 8.5, "xtick.labelsize": 7, "ytick.labelsize": 7,
    "legend.fontsize": 7, "axes.edgecolor": MUTED, "axes.linewidth": 0.6, "axes.labelcolor": INK,
    "xtick.color": INK2, "ytick.color": INK2, "text.color": INK, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.major.size": 2.5, "ytick.major.size": 2.5, "axes.spines.top": False, "axes.spines.right": False,
    "pdf.fonttype": 42, "ps.fonttype": 42, "savefig.bbox": "tight", "savefig.pad_inches": 0.03,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True, "legend.frameon": False,
})
SHORT = {"Opus 5.5（三方A）": "Opus 5.5"}
nm = lambda m: SHORT.get(m, m)


def save(fig, name):
    fig.savefig(os.path.join(FIG, name + ".pdf"))
    fig.savefig(os.path.join(FIG, name + ".png"), dpi=600)
    plt.close(fig)


def panel(ax, letter, title):
    ax.set_title(f"({letter}) {title}", loc="left", pad=6, fontweight="bold")


F = json.load(open(os.path.join(OUT, "findings.json")))
E = pd.read_csv(os.path.join(OUT, "tables", "R_1_model_effects_reliable.csv"), index_col=0)
R = pd.read_csv(os.path.join(OUT, "reliable_runs.csv"), low_memory=False)
A = pd.read_csv(os.path.join(OUT, "all_runs_labelled.csv"), low_memory=False)
Bh = pd.read_csv(os.path.join(OUT, "tables", "R_3_behaviour.csv"))
order = E.sort_values("tokens").index.tolist()

# ------------------------------------------------------------------ Fig 1: cost-quality plane
PANELS = [("tokens", "Tokens per task", "a"), ("cost", "API list price per task", "b"), ("time", "Wall-clock time per task", "c")]
OFF = {
    "tokens": {"gpt-6-astra": (-6, 6), "GPT 6.1 Sol": (7, -7), "Gemini 3.5 Flash": (7, 1), "Sonnet 5.5": (6, 7),
               "Opus 5.5（三方A）": (6, 7), "GLM-5.3 Flash": (6, 8), "Kimi K3": (-8, -9), "Fable 5.1": (3, -12),
               "Qwen 3.8 Max": (7, -3), "DeepSeek V4 Flash": (-6, 3)},
    "cost": {"gpt-6-astra": (0, 10), "GPT 6.1 Sol": (0, -11), "Gemini 3.5 Flash": (7, 1), "Sonnet 5.5": (7, 2),
             "Opus 5.5（三方A）": (6, 7), "GLM-5.3 Flash": (6, 6), "Kimi K3": (-7, -8), "Fable 5.1": (-6, 6),
             "Qwen 3.8 Max": (6, -7), "DeepSeek V4 Flash": (-6, 3)},
    "time": {"gpt-6-astra": (-6, 1), "GPT 6.1 Sol": (-7, -6), "Gemini 3.5 Flash": (7, 1), "Sonnet 5.5": (0, 10),
             "Opus 5.5（三方A）": (6, 7), "GLM-5.3 Flash": (6, 5), "Kimi K3": (-8, -4), "Fable 5.1": (2, -11),
             "Qwen 3.8 Max": (0, -11), "DeepSeek V4 Flash": (-6, 3)},
}
fig, axes = plt.subplots(1, 3, figsize=(7.1, 2.75), sharey=True, gridspec_kw={"wspace": 0.07})
for ax, (cost, lab, letter) in zip(axes, PANELS):
    def front(c, sc):
        return pd.Series([not (((c <= c[m]) & (sc >= sc[m]) & ((c < c[m]) | (sc > sc[m]))).any()) for m in c.index], index=c.index)
    on = front(E[cost], E.score)
    fr = E[on].sort_values(cost)
    xs, ys = [fr[cost].iloc[0]], [fr.score.iloc[0]]
    for i in range(1, len(fr)):
        xs += [fr[cost].iloc[i], fr[cost].iloc[i]]
        ys += [fr.score.iloc[i - 1], fr.score.iloc[i]]
    xs.append(20)
    ys.append(fr.score.iloc[-1])
    ax.plot(xs, ys, color=BLUE, lw=1.2, alpha=0.5, zorder=2, solid_joinstyle="round")
    ax.axhline(0, color=MUTED, lw=0.6, zorder=1)
    ax.axvline(1, color=MUTED, lw=0.6, zorder=1)
    for m in E.index:
        c = BLUE if on[m] else NEUTRAL
        ax.errorbar(E.loc[m, cost], E.loc[m, "score"],
                    xerr=[[E.loc[m, cost] - E.loc[m, cost + "_lo"]], [E.loc[m, cost + "_hi"] - E.loc[m, cost]]],
                    yerr=[[E.loc[m, "score"] - E.loc[m, "score_lo"]], [E.loc[m, "score_hi"] - E.loc[m, "score"]]],
                    fmt="none", ecolor=c, elinewidth=0.8, alpha=0.7, zorder=3)
        ax.scatter(E.loc[m, cost], E.loc[m, "score"], s=30, color=c, edgecolor="white", linewidth=1.0, zorder=4)
        dx, dy = OFF[cost][m]
        ax.annotate(nm(m), (E.loc[m, cost], E.loc[m, "score"]), xytext=(dx, dy), textcoords="offset points",
                    ha="left" if dx > 3 else "right" if dx < -3 else "center", va="center",
                    fontsize=6.3, color=INK if on[m] else INK2, zorder=5)
    ax.set_xscale("log")
    ax.set_xlim(0.07, 20)
    ax.set_xticks([0.125, 0.5, 2, 8])
    ax.set_xticklabels(["1/8×", "1/2×", "2×", "8×"])
    ax.minorticks_off()
    ax.set_xlabel(lab + "\n(× mean model, log scale)")
    ax.set_ylim(-19, 12)
    panel(ax, letter, {"tokens": "Token cost", "cost": "Money cost", "time": "Time cost"}[cost])
axes[0].set_ylabel("Design quality vs. mean model\n(points on the 53-point rubric)")
axes[0].legend(handles=[Line2D([], [], marker="o", ls="-", color=BLUE, mec="white", ms=5.5, lw=1.2, label="Pareto frontier"),
                        Line2D([], [], marker="o", ls="", color=NEUTRAL, mec="white", ms=5.5, label="Dominated")],
               loc="lower left", handletextpad=0.5, borderaxespad=0.2, labelspacing=0.3)
save(fig, "fig1_cost_quality")

# ------------------------------------------------------------------ Fig 2: dispersion of token use
fig, ax = plt.subplots(figsize=(3.4, 3.3))
rng = np.random.default_rng(3)
rows = order[::-1]
for i, m in enumerate(rows):
    for proto, kw in [("v2", dict(color=BLUE, edgecolor="white", linewidth=0.4)),
                      ("v1", dict(facecolor="white", edgecolor=ORANGE, linewidth=0.7))]:
        d = R[(R.model == m) & (R.protocol == proto)]
        if len(d):
            ax.scatter(d.tokens_scored_file / 1e6, i + rng.uniform(-0.2, 0.2, len(d)) + (0.0 if proto == "v2" else 0.0),
                       s=9, alpha=0.85, zorder=3, **kw)
    for proto in ["v2", "v1"]:
        d = R[(R.model == m) & (R.protocol == proto)]
        if len(d):
            med = d.tokens_scored_file.median() / 1e6
            ax.plot([med, med], [i - 0.36, i + 0.36], color=BLUE if proto == "v2" else ORANGE, lw=1.6, zorder=4,
                    solid_capstyle="round")
ax.set_yticks(range(len(rows)))
ax.set_yticklabels([nm(m) for m in rows])
ax.set_xscale("log")
ax.set_xlim(0.04, 40)
ax.set_xticks([0.1, 1, 10])
ax.set_xticklabels(["0.1M", "1M", "10M"])
ax.set_xlabel("Tokens per run (log scale)")
ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", length=0)
ax.legend(handles=[Line2D([], [], marker="o", ls="", color=BLUE, mec="white", ms=4.5, label="No-screenshot protocol"),
                   Line2D([], [], marker="o", ls="", mfc="white", mec=ORANGE, ms=4.5, label="Screenshot protocol"),
                   Line2D([], [], color=INK2, lw=1.6, label="Median")],
          loc="upper center", bbox_to_anchor=(0.42, 1.13), ncol=3, columnspacing=1.0, handletextpad=0.3)
save(fig, "fig2_token_dispersion")

# ------------------------------------------------------------------ Fig 3: more tokens != better; turns vs context
fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.9), gridspec_kw={"wspace": 0.3})
ax = axes[0]
x = R.logtok_resid / np.log(2)
y = R.score_resid
g = R.g0_pass.astype(str).eq("True")
ax.scatter(x[g], y[g], s=9, color=BLUE, alpha=0.5, edgecolor="none", zorder=3)
ax.scatter(x[~g], y[~g], s=14, marker="x", color=ORANGE, linewidth=0.9, zorder=4)
slope = np.polyfit(x, y, 1)
xx = np.linspace(-3, 3, 50)
gm = pd.read_csv(os.path.join(OUT, "tables", "R_2_cost_quality_slope.csv"))
g0 = gm[(gm.set == "reliable") & (gm.scores == "all")].iloc[0]
ax.fill_between(xx, g0.lo * xx, g0.hi * xx, color=INK, alpha=0.08, lw=0, zorder=2)
ax.plot(xx, g0.points_per_doubling * xx, color=INK, lw=1.4, zorder=5)
ax.set_xlim(-3, 3)
ax.set_ylim(-45, 22)
ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
ax.set_xticklabels(["1/8×", "1/4×", "1/2×", "1×", "2×", "4×", "8×"])
ax.set_xlabel("Tokens relative to expectation\nfor that model and task")
ax.set_ylabel("Quality relative to expectation (points)")
ax.text(0.03, 0.05, (f"Doubling tokens: {g0.points_per_doubling:+.1f} points\n(95% CI {g0.lo:+.1f} to {g0.hi:+.1f}),  n = {int(g0.n)}").replace("-", "−"),
        transform=ax.transAxes, fontsize=6.8, color=INK2, va="bottom")
ax.legend(handles=[Line2D([], [], marker="o", ls="", color=BLUE, alpha=0.6, mec="none", ms=4.5, label="Passed usability gate"),
                   Line2D([], [], marker="x", ls="", color=ORANGE, ms=4.5, mew=0.9, label="Failed gate (score 0)")],
          loc="upper left", handletextpad=0.3, borderaxespad=0.1)
panel(ax, "a", "Extra tokens do not buy quality")

ax = axes[1]
for tot in [0.125, 0.25, 0.5, 1, 2, 4, 8]:
    xs = np.array([0.2, 12])
    ax.plot(xs, tot / xs, color=GRID, lw=0.7, zorder=1)
    xt = np.sqrt(tot * 9.0) if tot >= 1 else None
for tot, (tx, ty) in {8: (3.3, 8 / 3.3), 2: (5.6, 2 / 5.6), 0.5: (1.9, 0.5 / 1.9)}.items():
    lab = {8: "8× tokens", 2: "2×", 0.5: "1/2×", 0.125: "1/8×"}[tot]
    ax.text(tx * 1.04, ty * 1.04, lab, fontsize=6, color=MUTED, rotation=-43, ha="center", va="center", zorder=1,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.6))
OFF2 = {"gpt-6-astra": (0, -10), "GPT 6.1 Sol": (7, 2), "Gemini 3.5 Flash": (-7, -4), "Sonnet 5.5": (-7, 4),
        "Opus 5.5（三方A）": (-7, 4), "GLM-5.3 Flash": (0, -11), "Kimi K3": (7, 5), "Fable 5.1": (7, 3),
        "Qwen 3.8 Max": (0, -11), "DeepSeek V4 Flash": (-2, 10)}
for m in E.index:
    ax.errorbar(E.loc[m, "turns"], E.loc[m, "tok_per_turn"],
                xerr=[[E.loc[m, "turns"] - E.loc[m, "turns_lo"]], [E.loc[m, "turns_hi"] - E.loc[m, "turns"]]],
                yerr=[[E.loc[m, "tok_per_turn"] - E.loc[m, "tok_per_turn_lo"]], [E.loc[m, "tok_per_turn_hi"] - E.loc[m, "tok_per_turn"]]],
                fmt="none", ecolor=BLUE, elinewidth=0.8, alpha=0.6, zorder=3)
    ax.scatter(E.loc[m, "turns"], E.loc[m, "tok_per_turn"], s=34, color=BLUE, edgecolor="white", linewidth=1.0, zorder=4)
    dx, dy = OFF2[m]
    ax.annotate(nm(m), (E.loc[m, "turns"], E.loc[m, "tok_per_turn"]), xytext=(dx, dy), textcoords="offset points",
                ha="left" if dx > 3 else "right" if dx < -3 else "center", va="center", fontsize=6.8, zorder=5)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(0.2, 9)
ax.set_ylim(0.2, 4)
ax.set_xticks([0.5, 1, 2, 4, 8])
ax.set_xticklabels(["1/2×", "1×", "2×", "4×", "8×"])
ax.set_yticks([0.25, 0.5, 1, 2, 4])
ax.set_yticklabels(["1/4×", "1/2×", "1×", "2×", "4×"])
ax.minorticks_off()
ax.grid(False)
ax.set_xlabel("Model turns per task (× mean model)")
ax.set_ylabel("Tokens per turn (× mean model)")
panel(ax, "b", "Two routes to a large token bill")
save(fig, "fig3_tokens_vs_quality_and_turns")

# ------------------------------------------------------------------ Fig 4: where the context goes + failed calls
B2 = Bh[Bh.protocol == "v2"].set_index("model").reindex(order)
segs = [("ctx_inspect", "Reading file state", BLUE), ("ctx_construct", "Building", ORANGE), ("ctx_modify", "Revising", AQUA),
        ("rest", "Other tool traffic", YELLOW), ("ctx_fixed_prompt", "Fixed prompt and tool schemas", NEUTRAL)]
B2["rest"] = 1 - B2[["ctx_inspect", "ctx_construct", "ctx_modify", "ctx_fixed_prompt"]].sum(axis=1)
fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.75), gridspec_kw={"width_ratios": [2.15, 1], "wspace": 0.1})
ax = axes[0]
ypos = np.arange(len(order))[::-1]
left = np.zeros(len(order))
for col, lab, c in segs:
    v = B2[col].to_numpy() * 100
    ax.barh(ypos, v, left=left, height=0.62, color=c, edgecolor="white", linewidth=1.2, label=lab)
    for yy, l, w in zip(ypos, left, v):
        if w >= 9:
            ax.text(l + w / 2, yy, f"{w:.0f}", ha="center", va="center", fontsize=6.3,
                    color="white" if c in (BLUE, ORANGE) else INK)
    left += v
ax.set_yticks(ypos)
ax.set_yticklabels([nm(m) for m in order])
ax.set_xlim(0, 100)
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(["0", "25", "50", "75", "100%"])
ax.set_xlabel("Share of input context, weighted by how often it is re-sent")
ax.grid(False)
ax.tick_params(axis="y", length=0)
for s in ["left", "bottom"]:
    ax.spines[s].set_visible(False)
ax.tick_params(axis="x", length=0)
ax.legend(loc="lower center", bbox_to_anchor=(0.42, 1.09), ncol=3, columnspacing=1.1, handlelength=1.0, handletextpad=0.4)
panel(ax, "a", "What fills the input context")
ax = axes[1]
v = B2.error_rate.to_numpy() * 100
ax.hlines(ypos, 0, v, color=BLUE, lw=1.6, zorder=2)
ax.scatter(v, ypos, s=26, color=BLUE, edgecolor="white", linewidth=1.0, zorder=3)
for yy, w in zip(ypos, v):
    ax.text(w + 1.2, yy, f"{w:.0f}%", va="center", fontsize=6.6, color=INK2)
ax.set_yticks(ypos)
ax.set_yticklabels([])
ax.set_ylim(axes[0].get_ylim())
ax.set_xlim(0, 34)
ax.set_xticks([0, 10, 20, 30])
ax.set_xticklabels(["0", "10", "20", "30%"])
ax.set_xlabel("Tool calls that fail")
ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
panel(ax, "b", "Failed tool calls")
save(fig, "fig4_context_and_errors")

# ------------------------------------------------------------------ Fig 5: what models do during inference
BW = pd.read_csv(os.path.join(OUT, "tables", "R_5_within_model_correlates.csv"))
E5 = pd.read_csv(os.path.join(OUT, "tables", "R_1_model_effects_reliable.csv"), index_col=0)
T6 = pd.read_csv(os.path.join(OUT, "tables", "R_6_time_output_by_category.csv"))
fig = plt.figure(figsize=(7.1, 3.0))
gs = fig.add_gridspec(1, 3, width_ratios=[1.05, 0.8, 0.82], wspace=0.16)
CATC = [("inspect", "Read file state", BLUE), ("construct", "Build", ORANGE), ("modify", "Revise", AQUA),
        ("prototype", "Wire prototype", YELLOW), ("verify", "Screenshot check", "#6250d6"), ("rest", "Other", NEUTRAL)]

ax = fig.add_subplot(gs[0])
v2b = Bh[Bh.protocol == "v2"].set_index("model")
mods = [m for m in E5.sort_values("score", ascending=False).index if m in v2b.index]
yy = np.arange(len(mods))[::-1]
left = np.zeros(len(mods))
v2b["calls_rest_share"] = 1 - v2b[[f"calls_{c}_share" for c in ["inspect", "construct", "modify", "prototype", "verify"]]].sum(axis=1)
for key, lab, c in CATC:
    v = v2b.loc[mods, f"calls_{key}_share"].to_numpy() * 100
    ax.barh(yy, v, left=left, height=0.64, color=c, edgecolor="white", linewidth=1.0, label=lab)
    for y_, l_, w_ in zip(yy, left, v):
        if w_ >= 14:
            ax.text(l_ + w_ / 2, y_, f"{w_:.0f}", ha="center", va="center", fontsize=5.9,
                    color="white" if c in (BLUE, ORANGE, "#6250d6") else INK)
    left += v
for y_, m in zip(yy, mods):
    ax.text(101.5, y_, f"{v2b.loc[m, 'calls_median']:.0f}", va="center", fontsize=6.0, color=INK2)
ax.text(101.5, len(mods) - 0.35, "calls", fontsize=5.8, color=MUTED, va="bottom")
ax.set_yticks(yy)
ax.set_yticklabels([nm(m) for m in mods], fontsize=6.6)
ax.set_xlim(0, 100)
ax.set_xticks([0, 50, 100])
ax.set_xticklabels(["0", "50", "100%"])
ax.set_xlabel("Share of tool calls (no-screenshot protocol)")
ax.grid(False)
ax.tick_params(axis="y", length=0)
for sp in ["left"]:
    ax.spines[sp].set_visible(False)
panel(ax, "a", "What models call")

ax = fig.add_subplot(gs[1])
T6 = T6.assign(cat=T6.category.where(T6.category.isin(["inspect", "construct", "modify", "prototype", "verify"]), "rest"))
tt = T6.groupby(["model", "cat"]).share_of_time.sum().unstack(fill_value=0)
mods6 = [m for m in mods if m in tt.index]
yy6 = np.array([yy[mods.index(m)] for m in mods6])
for y_, m in zip(yy, mods):
    if m not in tt.index:
        ax.text(2, y_, "not timed (this batch only)", va="center", fontsize=5.9, color=MUTED)
left = np.zeros(len(mods6))
for key, lab, c in CATC:
    v = tt.loc[mods6, key].to_numpy() * 100 if key in tt else np.zeros(len(mods6))
    ax.barh(yy6, v, left=left, height=0.64, color=c, edgecolor="white", linewidth=1.0)
    for y_, l_, w_ in zip(yy6, left, v):
        if w_ >= 14:
            ax.text(l_ + w_ / 2, y_, f"{w_:.0f}", ha="center", va="center", fontsize=5.9,
                    color="white" if c in (BLUE, ORANGE, "#6250d6") else INK)
    left += v
ax.set_yticks(yy)
ax.set_yticklabels([])
ax.set_ylim(fig.axes[0].get_ylim())
ax.set_xlim(0, 100)
ax.set_xticks([0, 50, 100])
ax.set_xticklabels(["0", "50", "100%"])
ax.set_xlabel("Share of wall-clock time\n(screenshot protocol)")
ax.grid(False)
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
panel(ax, "b", "Where time goes")
handles = [Patch(facecolor=c, edgecolor="white", label=lab) for _, lab, c in CATC]
fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.40, 0.955), ncol=6, handlelength=1.0,
           handletextpad=0.35, columnspacing=0.9, fontsize=6.4)

ax = fig.add_subplot(gs[2])
LAB = {"revise_share": "Revising share of calls", "revise_per_build": "Revisions per build call",
       "ctx_write_share": "Context on build/revise", "delete_rate": "Calls that delete",
       "error_rate": "Failed-call rate", "calls_per_turn": "Calls per turn", "repeat_error_rate": "Same error repeated",
       "build_share": "Building share of calls", "read_share": "Reading share of calls",
       "reads_per_write": "Reads per write", "ctx_read_share": "Context on reading", "duplicate_call_rate": "Duplicate calls"}
BW = BW[BW.behaviour.isin(LAB)].sort_values("partial_spearman_with_score")
yy = np.arange(len(BW))
sig = ((BW.lo > 0) | (BW.hi < 0)).to_numpy()
col = [BLUE if s_ else NEUTRAL for s_ in sig]
ax.hlines(yy, BW.lo, BW.hi, color=col, lw=1.6, zorder=3)
ax.scatter(BW.partial_spearman_with_score, yy, s=20, color=col, edgecolor="white", linewidth=0.9, zorder=4)
ax.axvline(0, color=MUTED, lw=0.8, zorder=2)
ax.set_yticks(yy)
ax.yaxis.tick_right()
ax.set_yticklabels([LAB[b_] for b_ in BW.behaviour], fontsize=6.3)
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_xlabel("Correlation with quality, 95% CI\n(within model and task)")
ax.set_xlim(-0.4, 0.4)
ax.set_xticks([-0.3, 0, 0.3])
ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", length=0)
panel(ax, "c", "Behaviour vs. quality")
save(fig, "fig5_behaviour")

# ------------------------------------------------------------------ Fig 6: how models build (process layer)
DO = pd.read_csv(os.path.join(OUT, "design_ops_runs.csv"), low_memory=False)
HT = pd.read_csv(os.path.join(OUT, "tables", "R_7_hypothesis_tests.csv"))
E6 = pd.read_csv(os.path.join(OUT, "tables", "R_1_model_effects_reliable.csv"), index_col=0)
v2o = DO[DO.protocol == "v2"]
ops = [("instance", "Instance of a component", BLUE), ("clone", "Duplicate a node", "#6250d6"),
       ("own_component", "Define own component", AQUA), ("frame", "New container frame", ORANGE),
       ("text", "New text layer", YELLOW), ("primitive", "Primitive shape / SVG", NEUTRAL)]
tot6 = v2o.groupby("model")[[o for o, _, _ in ops]].sum()
comp6 = tot6.div(tot6.sum(axis=1), axis=0)
mods = [m for m in E6.sort_values("score", ascending=False).index if m in comp6.index]
fig = plt.figure(figsize=(7.1, 3.0))
gs = fig.add_gridspec(1, 3, width_ratios=[1.15, 0.55, 1.0], wspace=0.12)
ax = fig.add_subplot(gs[0])
yy = np.arange(len(mods))[::-1]
left = np.zeros(len(mods))
for key, lab, c in ops:
    v = comp6.loc[mods, key].to_numpy() * 100
    ax.barh(yy, v, left=left, height=0.64, color=c, edgecolor="white", linewidth=1.0, label=lab)
    for y_, l_, w_ in zip(yy, left, v):
        if w_ >= 13:
            ax.text(l_ + w_ / 2, y_, f"{w_:.0f}", ha="center", va="center", fontsize=5.9,
                    color="white" if c in (BLUE, ORANGE, "#6250d6") else INK)
    left += v
ax.set_yticks(yy)
ax.set_yticklabels([nm(m) for m in mods], fontsize=6.6)
ax.set_xlim(0, 100)
ax.set_xticks([0, 50, 100])
ax.set_xticklabels(["0", "50", "100%"])
ax.set_xlabel("Share of node-creating operations in code")
ax.grid(False)
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
panel(ax, "a", "How models create nodes")
fig.legend(handles=[Patch(facecolor=c, edgecolor="white", label=lab) for _, lab, c in ops], loc="lower center",
           bbox_to_anchor=(0.36, 0.955), ncol=3, handlelength=1.0, handletextpad=0.35, columnspacing=0.9, fontsize=6.3)

ax = fig.add_subplot(gs[1])
al = v2o.groupby("model").apply(lambda d: d.autolayout.sum() / max(d.frame.sum(), 1)).reindex(mods)
ax.hlines(yy, 0, al.to_numpy(), color=BLUE, lw=1.6, zorder=2)
ax.scatter(al.to_numpy(), yy, s=24, color=BLUE, edgecolor="white", linewidth=1.0, zorder=3)
for y_, v_ in zip(yy, al.to_numpy()):
    ax.text(v_ + 0.06, y_, f"{v_:.2f}", va="center", fontsize=6.0, color=INK2)
ax.set_yticks(yy)
ax.set_yticklabels([])
ax.set_ylim(fig.axes[0].get_ylim())
ax.set_xlim(0, 1.45)
ax.set_xticks([0, 0.5, 1.0])
ax.set_xlabel("Auto-layout settings\nper new frame")
ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
panel(ax, "b", "Auto-layout")

ax = fig.add_subplot(gs[2])
ML = {"reuse_ratio": "Component reuse", "own_components": "Own components", "clone_ratio": "Duplication",
      "autolayout_ratio": "Auto-layout", "naming_ratio": "Layer naming", "primitive_share": "Primitive shapes"}
IL = {"E1": "consistent controls", "E2": "consistent pages", "B4": "clear icons", "D1": "control alignment",
      "D2": "component spacing", "G2": "layer hierarchy", "G1": "layer names", "F5": "overall polish"}
HT = HT.iloc[::-1].reset_index(drop=True)
yy = np.arange(len(HT))
col = [BLUE if s_ else (ORANGE if (r_ * (1 if e_ == "+" else -1) < 0 and (lo_ > 0 or hi_ < 0)) else NEUTRAL)
       for s_, r_, e_, lo_, hi_ in zip(HT.supported, HT.r, HT.expected, HT.lo, HT.hi)]
ax.hlines(yy, HT.lo, HT.hi, color=col, lw=1.6, zorder=3)
ax.scatter(HT.r, yy, s=20, color=col, edgecolor="white", linewidth=0.9, zorder=4)
ax.axvline(0, color=MUTED, lw=0.8, zorder=2)
ax.set_yticks(yy)
ax.yaxis.tick_right()
ax.set_yticklabels([f"{ML[m]}: {IL[i]} ({'+' if e == '+' else '−'})" for m, i, e in zip(HT.measure, HT.item, HT.expected)], fontsize=6.1)
ax.legend(handles=[Line2D([], [], marker="o", color=BLUE, mec="white", ms=5, lw=1.6, label="Supported (Holm)"),
                   Line2D([], [], marker="o", color=ORANGE, mec="white", ms=5, lw=1.6, label="Opposite sign"),
                   Line2D([], [], marker="o", color=NEUTRAL, mec="white", ms=5, lw=1.6, label="Not supported")],
          loc="lower left", bbox_to_anchor=(0.0, 1.09), ncol=3, fontsize=5.9, handlelength=1.3, handletextpad=0.35,
          columnspacing=0.8, borderaxespad=0.0)
ax.set_xlim(-0.4, 0.45)
ax.set_xticks([-0.3, 0, 0.3])
ax.set_xlabel("Correlation with rubric item, 95% CI\n(within model and task)")
ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)
panel(ax, "c", "Pre-registered tests")
save(fig, "fig6_construction")

# ------------------------------------------------------------------ Fig 7: what the delivered file contains (product layer)
PR = pd.read_csv(os.path.join(OUT, "product_runs.csv"), low_memory=False)
PB = pd.read_csv(os.path.join(OUT, "product_boards.csv"), low_memory=False)
PT = pd.read_csv(os.path.join(OUT, "tables", "R_8_hypothesis_tests_by_batch.csv"))
E7 = pd.read_csv(os.path.join(OUT, "tables", "R_1_model_effects_reliable.csv"), index_col=0)
b2 = PB[(PB.protocol == "v2") & (PB.nodes > 0)]
per = b2.groupby("model")[["nodes", "instances", "texts", "max_depth"]].mean()
per["other"] = per.nodes - per.instances - per.texts
mods = [m for m in E7.sort_values("score", ascending=False).index if m in per.index]
fig = plt.figure(figsize=(7.1, 2.95))
gs = fig.add_gridspec(1, 3, width_ratios=[1.15, 0.95, 1.0], wspace=0.5)
ax = fig.add_subplot(gs[0])
yy = np.arange(len(mods))[::-1]
left = np.zeros(len(mods))
for key, lab, c in [("instances", "Component instances", BLUE), ("texts", "Text layers", YELLOW), ("other", "Frames, shapes, images", NEUTRAL)]:
    v = per.loc[mods, key].to_numpy()
    ax.barh(yy, v, left=left, height=0.64, color=c, edgecolor="white", linewidth=1.0, label=lab)
    left += v
for y_, m in zip(yy, mods):
    ax.text(left[list(mods).index(m)] + 0.8, y_, f"depth {per.loc[m, 'max_depth']:.1f}", va="center", fontsize=5.9, color=INK2)
ax.set_yticks(yy)
ax.set_yticklabels([nm(m) for m in mods], fontsize=6.6)
ax.set_xlim(0, 52)
ax.set_xlabel("Layers per screen (mean)\n(instance contents not counted)")
ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
ax.legend(loc="lower center", bbox_to_anchor=(0.45, 1.09), ncol=3, fontsize=6.0, handlelength=1.0, handletextpad=0.3, columnspacing=0.7)
panel(ax, "a", "What the file contains")

ax = fig.add_subplot(gs[1])
v2r = PR[(PR.protocol == "v2") & PR.g0_pass.astype(str).eq("True")]
jit = np.random.default_rng(4)
ax.scatter(v2r.instance_node_share * 100, v2r.max_depth + jit.uniform(-0.18, 0.18, len(v2r)), s=9, color=BLUE, alpha=0.55,
           edgecolor="none", zorder=3)
z = np.polyfit(v2r.instance_node_share * 100, v2r.max_depth, 1)
xx = np.linspace(0, 100, 20)
ax.plot(xx, np.polyval(z, xx), color=INK, lw=1.2, zorder=4)
ax.set_xlim(0, 100)
ax.set_ylim(-0.3, 9)
ax.set_xlabel("Instance share of layers (%)")
ax.set_ylabel("Nesting depth in the snapshot")
ax.text(0.97, 0.95, "Depth vs. G2 score:\nr = +0.60 within model", transform=ax.transAxes, ha="right", va="top",
        fontsize=6.3, color=INK2)
panel(ax, "b", "Instances hide depth")

ax = fig.add_subplot(gs[2])
IL7 = {"E1": "consistent controls", "E2": "consistent pages", "B4": "clear icons", "F5": "overall polish", "D4": "no empty space"}
ML7 = {"instance_node_share": "Instance share", "images_per_screen": "Images per screen", "nodes_per_screen": "Layers per screen"}
PT = PT.iloc[::-1].reset_index(drop=True)
yy = np.arange(len(PT))
col = [BLUE if s_ else NEUTRAL for s_ in PT.supported]
ax.hlines(yy, PT.lo, PT.hi, color=col, lw=1.6, zorder=3)
ax.scatter(PT.r, yy, s=20, color=col, edgecolor="white", linewidth=0.9, zorder=4)
ax.axvline(0, color=MUTED, lw=0.8, zorder=2)
ax.set_yticks(yy)
ax.yaxis.tick_right()
ax.set_yticklabels([f"{ML7[m]}: {IL7[i]} (+)" for m, i in zip(PT.measure, PT["item"])], fontsize=6.1)
ax.set_xlim(-0.35, 0.35)
ax.set_xticks([-0.3, 0, 0.3])
ax.set_xlabel("Correlation with rubric item, 95% CI\n(within model and task)")
ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)
panel(ax, "c", "Pre-registered tests")
save(fig, "fig7_product")

# ------------------------------------------------------------------ Fig 8: failure modes (sub-dimensions -> manifestations)
DIM_ORDER = ["用户体验", "布局质量", "信息组织", "一致性", "可交付性", "视觉表达"]
DIM_EN = {"用户体验": "Usability", "布局质量": "Layout", "信息组织": "Information", "一致性": "Consistency",
          "可交付性": "Deliverability", "视觉表达": "Visual"}
DIM_COLOR = {"用户体验": BLUE, "布局质量": ORANGE, "信息组织": AQUA, "一致性": YELLOW,
             "可交付性": "#e87ba4", "视觉表达": "#008300"}
D8 = pd.read_csv(os.path.join(OUT, "tables", "R_9_lost_share_model_x_dimension.csv"), index_col=0)[DIM_ORDER]
M8 = pd.read_csv(os.path.join(OUT, "tables", "R_9_points_by_manifestation.csv"), index_col=0).iloc[:, 0]
MI8 = pd.read_csv(os.path.join(OUT, "tables", "R_9_points_manifestation_x_item.csv"), index_col=0)
E8 = pd.read_csv(os.path.join(OUT, "tables", "R_1_model_effects_reliable.csv"), index_col=0)

MLAB = {"overlap": "Elements overlap", "overflow_clipping": "Content overflows / is clipped",
        "logic_data_error": "Data or logic inconsistent", "empty_space": "Large meaningless empty space",
        "misalignment_spacing": "Misaligned / uneven spacing", "flat_layers_default_names": "Flat layers, default names",
        "inconsistent_across_screens": "Inconsistent across screens", "placeholder_icons": "Placeholder-looking icons",
        "icon_ambiguous_semantics": "Icon meaning unclear", "no_current_state": "No current-state indicator",
        "weak_emphasis": "Primary action not emphasised", "content_missing": "Expected element missing",
        "screen_clipped_or_empty": "Screen clipped or empty", "readability_contrast": "Low text contrast",
        "size_proportion": "Control proportions off", "misgrouping": "Content grouped incorrectly",
        "text_only_controls": "Controls are bare text", "sequence_disorder": "Reading order disrupted",
        "unlabeled_controls": "Controls lack a label", "purpose_unclear": "Screen purpose unclear",
        "missing_navigation": "Navigation missing", "flat_hierarchy": "No text-size hierarchy",
        "semantic_color_misuse": "Wrong state color used", "accent_color_overused": "Accent color overused",
        "input_feedback_missing": "No confirmation feedback", "black_or_unreadable_screen": "Screen unreadably dark"}
ITEM_TXT = {"A1": "page purpose", "A2": "current state", "A3": "finding core content", "A4": "control affordance",
            "B1": "grouping", "B2": "reading order", "B3": "logic/data", "B4": "icon clarity", "B5": "action emphasis",
            "G1": "layer names", "G2": "layer hierarchy", "D1": "control alignment", "D2": "component spacing",
            "D3": "page structure", "D4": "empty space", "E1": "control consistency", "E2": "page consistency",
            "F1": "type hierarchy", "F2": "accent color", "F3": "state color", "F4": "neutral color", "F5": "polish"}

fig = plt.figure(figsize=(7.1, 6.1))
gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.55], hspace=0.62)

ax = fig.add_subplot(gs[0])
order = D8.sum(axis=1).sort_values().index
yy = np.arange(len(order))[::-1]
left = np.zeros(len(order))
for d in DIM_ORDER:
    v = D8.loc[order, d].to_numpy() * 100
    ax.barh(yy, v, left=left, height=0.64, color=DIM_COLOR[d], edgecolor="white", linewidth=1.0, label=DIM_EN[d])
    left += v
ax.set_yticks(yy)
ax.set_yticklabels([nm(m) for m in order], fontsize=6.8)
ax.set_xlim(0, left.max() * 1.08)
ax.set_xlabel("Points lost, as % of points available per dimension (summed across dimensions)")
ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
ax.legend(loc="lower center", bbox_to_anchor=(0.46, 1.1), ncol=6, fontsize=6.0, handlelength=1.0, handletextpad=0.3, columnspacing=0.7)
panel(ax, "a", "Where each model loses points")

ax = fig.add_subplot(gs[1])
top = M8.sort_values(ascending=False).head(14)
yy2 = np.arange(len(top))[::-1]
ax.barh(yy2, top.to_numpy(), height=0.6, color=BLUE, edgecolor="white", linewidth=1.0, zorder=3)
for y_, k, v in zip(yy2, top.index, top.to_numpy()):
    top_items = MI8.loc[k].sort_values(ascending=False)
    top_items = top_items[top_items > 0].head(3)
    lab = " / ".join(ITEM_TXT.get(i, i) for i in top_items.index)
    ax.text(v + 8, y_, lab, va="center", fontsize=6.1, color=INK2)
ax.set_yticks(yy2)
ax.set_yticklabels([MLAB.get(k, k) for k in top.index], fontsize=6.6)
ax.set_xlim(0, 620)
ax.set_xlabel("Points lost across all runs  —  labels show which rubric sub-items it mostly comes from")
ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
panel(ax, "b", "The concrete failure behind each lost point")
save(fig, "fig8_failure_modes")

# ------------------------------------------------------------------ Fig S1: reliability audit
aud = pd.read_csv(os.path.join(OUT, "tables", "R_0_reliability_rules.csv"))
labels = ["Run finished", "Score is of the final file", "Cost attributable to judged file",
          "Token count matches trajectory", "No material infrastructure failures", "Trajectory available"]
fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.5), gridspec_kw={"width_ratios": [1.25, 1], "wspace": 0.75})
ax = axes[0]
yy = np.arange(len(aud) + 1)[::-1]
vals = [F["n_total"]] + aud.remaining.tolist()
ax.barh(yy, vals, height=0.6, color=[NEUTRAL] + [BLUE] * len(aud), edgecolor="white", linewidth=1.2)
for y_, v_, d_ in zip(yy, vals, [None] + aud.newly_excluded.tolist()):
    ax.text(v_ + 6, y_, f"{v_}" + (f"  (−{d_})" if d_ else ""), va="center", fontsize=6.8, color=INK2)
ax.set_yticks(yy)
ax.set_yticklabels(["All records"] + labels)
ax.set_xlim(0, 500)
ax.set_xlabel("Records remaining after each rule")
ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", length=0)
panel(ax, "a", "Reliability rules, applied in order")
ax = axes[1]
cnt = A.groupby("model").agg(total=("reliable", "size"), ok=("reliable", "sum")).reindex(order)
yp = np.arange(len(order))[::-1]
ax.barh(yp, cnt.total, height=0.6, color=GRID, edgecolor="white", linewidth=1.2, label="Excluded")
ax.barh(yp, cnt.ok, height=0.6, color=BLUE, edgecolor="white", linewidth=1.2, label="Reliable")
for y_, a_, b_ in zip(yp, cnt.ok, cnt.total):
    ax.text(b_ + 1, y_, f"{a_}/{b_}", va="center", fontsize=6.6, color=INK2)
ax.set_yticks(yp)
ax.set_yticklabels([nm(m) for m in order])
ax.set_xlim(0, 52)
ax.set_xlabel("Records per model")
ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", length=0)
ax.legend(loc="lower center", bbox_to_anchor=(0.45, 1.1), ncol=2, handlelength=1.0, handletextpad=0.4, columnspacing=1.0)
panel(ax, "b", "Coverage by model")
save(fig, "figS1_reliability_audit")
print("wrote", sorted(os.listdir(FIG)))
