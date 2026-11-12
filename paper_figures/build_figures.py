"""Reproduce the Figma benchmark figure set with Matplotlib and NumPy."""
import csv
import hashlib
import importlib.util
import json
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.patches import Patch
import numpy as np
from PIL import Image

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent / "benchmark_output/project"
ARENA = ROOT / "arena"
DB = ARENA / "arena.sqlite3"
MANIFEST = ROOT / "deliver-20261103/manifest.csv"
spec = importlib.util.spec_from_file_location("arena_elo", ARENA / "analysis/arena_elo.py")
elo = importlib.util.module_from_spec(spec)
sys.dont_write_bytecode = True
spec.loader.exec_module(elo)
db = sqlite3.connect(DB.as_uri() + "?mode=ro&immutable=1", uri=True)
candidates = {
    (case, model): json.loads(body)
    for case, model, body in db.execute("select case_id,model_id,body from candidates")
}
cases = sorted({case for case, _ in candidates})
aliases = {
    "Opus 5.5（三方A）": "Opus 5.5 (A)", "gpt-6-astra": "GPT-6 Astra",
    "Fable 5.1": "Fable 5.1", "GLM-5.3 Flash": "GLM-5.3 Flash",
    "Kimi K3": "Kimi K3", "Gemini 3.5 Flash": "Gemini 3.5 Flash",
}
names = {model: aliases[x["model_name"]] for (_, model), x in candidates.items()}
scores = {key: float(x["cc_score"]) for key, x in candidates.items()}
titles = {case: x["title"] for (case, _), x in candidates.items()}
assert len(candidates) == len(cases) * len(names) == 174
assert {x["cc_method"] for x in candidates.values()} == {"fixed_v4"}

sessions = {
    sid: (case, reviewer, json.loads(state))
    for sid, case, reviewer, state in db.execute(
        "select id,case_id,reviewer_id,state from incremental_sort_sessions")
}
expert_votes = {}
for sid, a, b, winner, outcome, active, pair in db.execute(
    "select session_id,a,b,winner,outcome,active,pair_id "
    "from incremental_sort_votes order by created_at,ballot_id"
):
    case, reviewer, _ = sessions[sid]
    if active and outcome == "win" and case != elo.EXCLUDED and reviewer in elo.EXPERTS:
        loser = b if winner == a else a
        assert winner in (a, b) and winner != loser
        expert_votes[sid, tuple(sorted((a, b)))] = case, reviewer, winner, loser, pair
votes = list(expert_votes.values())
matched = sorted({v[0] for v in votes})
assert len(matched) == 28 and set(matched) == set(cases) - {elo.EXCLUDED}
rating = elo.summarize([v[:4] for v in votes], sorted(names))
models = [r["model"] for r in rating["leaderboard"]]
n = len(matched)

INK, MUTED, GRID = "#192D39", "#506472", "#DCE5E9"
BLUE, TEAL, COPPER = "#255D85", "#137568", "#A0442D"
DIVERGE = LinearSegmentedColormap.from_list("difference", [COPPER, "#FAF7F2", "#196F93"])
SEQUENCE = LinearSegmentedColormap.from_list("proficiency", ["#F1F6F7", "#164E72"])
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "text.color": INK,
    "axes.labelcolor": INK, "axes.edgecolor": GRID, "xtick.color": MUTED,
    "ytick.color": MUTED, "axes.titleweight": "bold", "pdf.fonttype": 42,
    "svg.fonttype": "none", "axes.spines.top": False, "axes.spines.right": False,
})

def page(width, height, title, subtitle):
    fig = plt.figure(figsize=(width, height), facecolor="white")
    fig.text(.055, .94, title, fontsize=19, weight="bold", va="top")
    fig.text(.055, .873, subtitle, fontsize=9.5, color=MUTED, va="top")
    return fig

def foot(fig, value):
    fig.text(.055, .038, value, fontsize=8, color=MUTED, va="bottom", linespacing=1.5)

def label(ax, title):
    ax.set_title(title, loc="left", fontsize=11.5, pad=12)

def chart_axis(ax, direction):
    ax.set_axisbelow(True)
    if direction != "none":
        ax.grid(axis=direction, color=GRID, linewidth=.7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0)

def colorbar(fig, ax, image, legend, ticks, extend="neither"):
    cb = fig.colorbar(image, cax=ax, orientation="horizontal", ticks=ticks, extend=extend)
    cb.outline.set_visible(False)
    cb.ax.tick_params(length=0, labelsize=8, pad=2)
    cb.ax.set_title(legend, loc="left", fontsize=8, pad=5, color=MUTED)

def numeric_cells(ax, values, image, fmt):
    for (y, x), value in np.ndenumerate(values):
        red, green, blue, _ = image.cmap(image.norm(value))
        dark = .2126 * red + .7152 * green + .0722 * blue < .51
        ax.text(x, y, fmt(value), ha="center", va="center", color="white" if dark else INK,
                fontsize=8, weight="bold")

figures = []
stats = {"arena_sha256": hashlib.sha256(DB.read_bytes()).hexdigest(), "elo": rating}

# Figure 1: human preference and rubric quality on the same tasks.
rng = np.random.default_rng(20261111)
matrix = np.array([[scores[c, m] for m in models] for c in matched])
draws = rng.integers(n, size=(4000, n))
boot = matrix[draws].mean(axis=1)
ci = np.percentile(boot, [2.5, 97.5], axis=0).T
means = matrix.mean(axis=0)
stats["vlm_mean_28"] = {names[m]: [means[i], *ci[i]] for i, m in enumerate(models)}
stats["vlm_paired_differences"] = {}
for i in range(len(models) - 1):
    stats["vlm_paired_differences"][f"{names[models[i]]} vs {names[models[i+1]]}"] = [
        means[i] - means[i+1], *np.percentile(boot[:, i] - boot[:, i+1], [2.5, 97.5])
    ]
fig = page(10.5, 5.0, "Overall benchmark performance",
           f"Six models on {n} shared Figma tasks  ·  {len(votes)} decisive pairwise votes from two designers")
for index, (box, points, bounds, title, axis, col, limits) in enumerate([
    ([.205, .215, .327, .54], [r["elo"] for r in rating["leaderboard"]],
     [r["ci95"] for r in rating["leaderboard"]], "A   Human preference", "Bradley–Terry Elo", TEAL, (500, 1790)),
    ([.61, .215, .32, .54], means, ci, "B   VLM rubric score", "Mean score (out of 53)", BLUE, (25, 54)),
]):
    ax = fig.add_axes(box)
    label(ax, title)
    y = np.arange(len(models))
    points, bounds = np.array(points), np.array(bounds)
    ax.hlines(y, bounds[:, 0], bounds[:, 1], color=col, alpha=.65, linewidth=2.0)
    ax.scatter(points, y, color=col, s=40, zorder=3, edgecolors="white", linewidths=.6)
    for pos, (_, hi), value in zip(y, bounds, points):
        ax.annotate(f"{value:.0f}" if index == 0 else f"{value:.1f}", (hi, pos),
                    xytext=(7, 0), textcoords="offset points", va="center", color=col, weight="bold")
    ax.set(ylim=(len(models)-.5, -.5), xlim=limits, xlabel=axis)
    ax.set_yticks(y, [names[m] for m in models] if index == 0 else [])
    if index == 0:
        ax.set_xticks([600, 900, 1200, 1500, 1700])
    chart_axis(ax, "x")
foot(fig, "Lines show 95% task-bootstrap intervals, conditional on the observed designer panel.\n"
          "Chat Bot AI is excluded from both panels because the GPT-6 Astra output was incomplete.")
figures.append(("fig1_overall_performance", fig))

# Figure 2: each cell prints the raw score and encodes its difference from the task median.
batches = ["3case", "6case", "10case", "web10"]
ordered = sorted(cases, key=lambda c: (batches.index(c.split("-")[0]), c))
raw = np.array([[scores[c, m] for c in ordered] for m in models])
median = np.median(raw, axis=0)
delta = raw - median
fig = page(12.3, 6.7, "Model performance varies across tasks",
           "Numbers show raw VLM scores. Color shows each model’s score relative to the median on that task.")
ax = fig.add_axes([.165, .512, .785, .25])
img = ax.imshow(delta, cmap=DIVERGE, norm=TwoSlopeNorm(0, vmin=-16, vmax=16), aspect="auto")
ax.set_yticks(range(len(models)), [names[m] for m in models])
ax.set_xticks([])
ax.tick_params(length=0)
for x in np.arange(-.5, 29, 1):
    ax.axvline(x, color="white", linewidth=.6)
for y in np.arange(-.5, 6, 1):
    ax.axhline(y, color="white", linewidth=.6)
for (y, x), value in np.ndenumerate(raw):
    ax.text(x, y, f"{value:.0f}", ha="center", va="center", fontsize=7.5,
            color="white" if abs(delta[y, x]) > 10 else INK, weight="bold")
ax.axvline(18.5, color=INK, linewidth=1.2)
for left, right, platform in [(-.5, 18.5, "Mobile · 19 tasks"), (18.5, 28.5, "Web · 10 tasks")]:
    ax.plot([left+.13, right-.13], [1.035]*2, transform=ax.get_xaxis_transform(),
            color=GRID, clip_on=False, linewidth=1.5)
    ax.text((left+right)/2, 1.067, platform, transform=ax.get_xaxis_transform(),
            ha="center", va="bottom", color=MUTED, weight="bold")
task_ax = fig.add_axes([.165, .395, .785, .089])
task_ax.scatter(range(len(ordered)), median, s=12, color=BLUE, zorder=3)
task_ax.axvline(18.5, color=INK, linewidth=1.2)
task_ax.set(xlim=(-.5, 28.5), ylim=(32, 52))
task_ax.set_yticks([35, 45])
task_ax.set_ylabel("Task\nmedian", rotation=0, labelpad=25, va="center", fontsize=8)
task_ax.set_xticks(range(len(ordered)), [titles[c] for c in ordered], rotation=60, ha="right", rotation_mode="anchor")
task_ax.tick_params(axis="x", labelsize=7.4, pad=5)
chart_axis(task_ax, "y")
colorbar(fig, fig.add_axes([.165, .081, .22, .016]), img,
         "VLM points from the task median", [-16, -8, 0, 8, 16], extend="both")
foot(fig, "All 29 Arena tasks, including Chat Bot AI and the recorded 0 for Gemini on ABM Developer Portfolio.")
figures.append(("fig2_task_heterogeneity", fig))

# Figure 3: observed direct vote agreement and rank agreement on complete sessions.
margins = [(case, scores[case, w] - scores[case, l]) for case, _, w, l, _ in votes]
bin_specs = [(1, 2), (3, 5), (6, 9), (10, np.inf)]
counts = np.zeros((n, len(bin_specs), 2), dtype=int)
index = {c: i for i, c in enumerate(matched)}
for case, margin in margins:
    for j, (lo, hi) in enumerate(bin_specs):
        if lo <= abs(margin) <= hi:
            counts[index[case], j, int(margin > 0)] += 1
totals = counts.sum(axis=0)
accuracy = totals[:, 1] / totals.sum(axis=1)
sim = counts[draws].sum(axis=1)
den = sim.sum(axis=2)
intervals = np.nanpercentile(np.divide(sim[:, :, 1], den, where=den > 0,
                                        out=np.full(den.shape, np.nan)), [2.5, 97.5], axis=0)
rank_tau = defaultdict(list)
for case, reviewer, state in sessions.values():
    if case in matched and reviewer in elo.EXPERTS and state["status"] == "complete":
        human = {m: -i for i, m in enumerate(state["ranking"])}
        assert set(human) == set(models)
        rank_tau[case].append(elo.tau(human, {m: scores[case, m] for m in models}, models))
case_tau = sorted((np.mean(values), c, len(values)) for c, values in rank_tau.items())
summary = [int(totals[:, 1].sum()), int(totals.sum()), sum(m == 0 for _, m in margins)]
stats.update(agreement_counts=summary, agreement_by_bin=totals.tolist(),
             mean_task_tau=float(np.mean([r[0] for r in case_tau])), tau_tasks=len(case_tau))
fig = page(10.7, 5.35, "Where VLM scores agree with designers",
           f"{summary[0]}/{summary[1]} decisive votes agreed with the VLM ({summary[0]/summary[1]:.1%})  ·  "
           f"{summary[2]} votes with tied VLM scores excluded from panel A")
ax = fig.add_axes([.105, .23, .355, .54])
label(ax, "A   Agreement by VLM score gap")
p = np.arange(len(accuracy))
ax.vlines(p, *intervals, color=TEAL, linewidth=1.7)
ax.scatter(p, accuracy, color=TEAL, zorder=3, s=41)
for j, v in enumerate(accuracy):
    ax.annotate(f"{v:.0%}", (j, v), xytext=(9, -3), textcoords="offset points", color=TEAL, weight="bold")
ax.set_xticks(p, [f"{name}\n$n$ = {count}" for name, count in
                  zip(["1–2", "3–5", "6–9", "≥10"], totals.sum(axis=1))])
ax.set(xlim=(-.4, 3.6), ylim=(.25, 1.04), ylabel="Agreement with the human vote",
       xlabel="Absolute score gap (points)")
ax.set_yticks([.25, .5, .75, 1], ["25%", "50%", "75%", "100%"])
chart_axis(ax, "y")
ax = fig.add_axes([.575, .23, .375, .54])
label(ax, f"B   Ranking agreement across {len(case_tau)} tasks")
for j, (tau, case, reviewers) in enumerate(case_tau):
    ax.scatter(j, tau, color=BLUE if reviewers == 2 else "white", edgecolor=BLUE, s=26, zorder=3)
ax.axhline(0, color=MUTED, linewidth=.9)
ax.axhline(stats["mean_task_tau"], color=BLUE, linestyle="--", linewidth=.9)
ax.text(.03, stats["mean_task_tau"]+.035, f"Task mean {stats['mean_task_tau']:.2f}",
        transform=ax.get_yaxis_transform(), fontsize=8, color=BLUE)
ax.set(xlim=(-1, len(case_tau)), ylim=(-.2, 1.07), xlabel="Tasks, sorted by agreement", ylabel="Kendall’s τ-b")
ax.set_xticks([])
ax.annotate(titles[case_tau[0][1]], (0, case_tau[0][0]), xytext=(8, 7),
            textcoords="offset points", color=MUTED, fontsize=8)
chart_axis(ax, "y")
foot(fig, "A  Intervals resample tasks. Votes contribute equally within each score-gap bin.\n"
          "B  Each dot averages available complete designer rankings for one task (filled: two; open: one).")
figures.append(("fig3_human_vlm_agreement", fig))

# Figure 4: strongest VLM reversal shared by both designers, with original screenshots.
shared_pairs = defaultdict(dict)
for case, reviewer, winner, loser, pair in votes:
    shared_pairs[case, winner, loser][reviewer] = pair
gap, case, winner, loser = min(
    (scores[c, w] - scores[c, l], c, w, l)
    for (c, w, l), review in shared_pairs.items() if len(review) == 2
)
assert gap < 0
plans = []
choices = []
for reviewer, pair in sorted(shared_pairs[case, winner, loser].items()):
    left, right = db.execute(
        "select left_model_id,right_model_id from incremental_sort_requests where pair_id=?",
        (pair,)).fetchone()
    plan = json.loads(db.execute(
        "select body from pair_screen_plans where reviewer_id=? and pair_id=?",
        (reviewer, pair)).fetchone()[0])
    by_id = dict(db.execute(
        "select slot_id,choice from pair_screen_votes where reviewer_id=? and pair_id=?",
        (reviewer, pair)))
    plans.append({s["name"]: {left: s["A"], right: s["B"]} for s in plan})
    choices.append({s["name"]: {"A": left, "B": right}.get(by_id.get(s["id"]), by_id.get(s["id"]))
                    for s in plan})
assert plans[0] == plans[1]
slots = list(plans[0])
shown = slots[:3]
stats["example"] = {"task": case, "human_winner": names[winner], "human_loser": names[loser],
                    "vlm_margin": gap, "shown_slots": shown}
fig = page(10.8, 7.2, f"A closer look at a disagreement · {titles[case]}",
           f"Both designers preferred {names[winner]} overall. The VLM favored {names[loser]} "
           f"({scores[case, loser]:.0f} vs. {scores[case, winner]:.0f} out of 53).")
ax = fig.add_axes([.17, .709, .77, .073])
ax.set_title("A   Recorded judgments across all screens", loc="left", pad=11, fontsize=11.5)
prefs = {winner: (TEAL, names[winner]), loser: (COPPER, names[loser]),
         "tie": ("#C8D2D8", "Tie"), "unable": ("#F2F5F7", "Unable"),
         None: ("#F2F5F7", "No vote")}
for i, review in enumerate(choices):
    for j, slot in enumerate(slots):
        ax.barh(i, .96, height=.83, left=j-.48, color=prefs[review[slot]][0])
ax.set(ylim=(1.5, -.5), xlim=(-.5, len(slots)-.5))
ax.set_yticks([0, 1], ["Designer 1", "Designer 2"])
ax.set_xticks(range(len(slots)), [s.split("_")[0] for s in slots])
chart_axis(ax, "none")
seen = set(v for review in choices for v in review.values())
fig.legend(handles=[Patch(color=col, label=name) for k, (col, name) in prefs.items() if k in seen],
           loc="center left", bbox_to_anchor=(.161, .65), frameon=False, ncol=len(seen),
           fontsize=8, handlelength=1.1)
fig.text(.055, .592, "B   First three screens in brief order", fontsize=11.5, weight="bold")
for j, slot in enumerate(shown):
    x = .11 + j * .277
    fig.text(x + .105, .542, slot.replace("_", " "), weight="bold", ha="center", fontsize=9)
    for k, model in enumerate([winner, loser]):
        image = candidates[case, model]["images"][plans[0][slot][model]]
        path = ARENA / image["file"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == image["sha256"]
        with Image.open(path) as file:
            img = file.convert("RGB")
            img.thumbnail((350, 760), Image.Resampling.LANCZOS)
        ax = fig.add_axes([x + .106*k, .13, .1, .375])
        ax.imshow(img)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color(GRID)
        fig.text(x + .05 + .106*k, .106, names[model], ha="center", fontsize=8,
                 weight="bold", color=prefs[model][0])
foot(fig, "Post-hoc illustration selected by the largest opposing VLM margin among pairs with two agreeing designers.\n"
          "Screens shown at a common scale. Colored cells record the original screen votes.")
figures.append(("fig4_disagreement_case", fig))

# Figure S1: item-level scores from the delivery package, with a common-task G0 filter.
rubric = json.loads((ROOT / "benchmarks/rubrics/fixed-v4.json").read_text())
groups = defaultdict(list)
for question in rubric["questions"]:
    groups[question["key"][0]].append((question["key"], question.get("max", 2)))
dimensions = ["Usability", "Information\norganization", "Deliverability",
              "Layout", "Consistency", "Visual\nexpression"]
item_groups = [groups[key] for key in "ABGDEF"]
maxima = [sum(v for _, v in g) for g in item_groups]
assert sum(maxima) == 53 and sum(map(len, item_groups)) == 22
with MANIFEST.open(encoding="utf-8-sig") as source:
    delivery = defaultdict(dict)
    for row in csv.DictReader(source):
        if row["model_name"] in aliases:
            delivery[row["round"] + "-" + row["case_id"]][aliases[row["model_name"]]] = row
assert all(len(v) == 6 for v in delivery.values())
proficiency = []
for rows in delivery.values():
    if any(row["g0_pass"] != "True" for row in rows.values()):
        continue
    task = []
    for model in models:
        row = rows[names[model]]
        subtotals = [sum(int(row[k]) for k, _ in g) for g in item_groups]
        assert sum(subtotals) == int(row["score_total"])
        task.append(np.array(subtotals) / maxima * 100)
    proficiency.append(task)
absolute = np.mean(proficiency, axis=0)
gap = absolute - absolute.mean(axis=0)
relative = gap - gap.mean(axis=1, keepdims=True)
stats["rubric_delivery"] = {"tasks": len(proficiency), "absolute": absolute.tolist(),
                            "relative": relative.tolist()}
fig = page(12.0, 5.1, "Design capabilities by rubric dimension",
           f"{len(proficiency)} common tasks passing G0 for all six models  ·  Delivery-package rubric scores")
for start, title, matrix, cmap, lo, hi, fmt in [
    (.184, "A   Mean share of available points", absolute, SEQUENCE, 0, 100, lambda x: f"{x:.1f}"),
    (.604, "B   Relative strengths after centering", relative, DIVERGE, -12, 12, lambda x: f"{x:+.1f}"),
]:
    ax = fig.add_axes([start, .295, .35, .39])
    label(ax, title)
    img = ax.imshow(matrix, cmap=cmap, vmin=lo, vmax=hi, aspect="auto", interpolation="nearest")
    ax.set_yticks(range(6), [names[m] for m in models] if start < .2 else [])
    ax.set_xticks(range(6), dimensions, fontsize=7.3)
    ax.tick_params(length=0, pad=5)
    numeric_cells(ax, matrix, img, fmt)
    for x in np.arange(-.5, 6, 1):
        ax.axvline(x, color="white", linewidth=1)
    for y in np.arange(-.5, 6, 1):
        ax.axhline(y, color="white", linewidth=1)
    colorbar(fig, fig.add_axes([start, .13, .2, .02]), img,
             "Percent of dimension maximum" if lo == 0 else "Residual (percentage points)",
             [0, 25, 50, 75, 100] if lo == 0 else [-12, -6, 0, 6, 12])
foot(fig, "Panel B subtracts both the dimension mean and the model’s average gap across dimensions. Tasks are equally weighted.\n"
          "The delivery package includes a different Chat Bot AI run for GPT-6 Astra, scored offline.")
figures.append(("figS1_rubric_dimensions", fig))

with PdfPages(OUT / "figma_benchmark_figures.pdf", metadata={
    "Title": "Figma benchmark figures", "Subject": "Benchmark results and evaluation agreement",
}) as pdf:
    for name, fig in figures:
        pdf.savefig(fig)
        fig.savefig(OUT / (name + ".svg"))
        fig.savefig(OUT / (name + ".png"), dpi=300)
        plt.close(fig)
(OUT / "figure_statistics.json").write_text(json.dumps(stats, indent=2, ensure_ascii=False) + "\n")
