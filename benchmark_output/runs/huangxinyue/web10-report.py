#!/usr/bin/env python3
"""Merged progress for the web10 round (web10-main + web10-gemini sub-rounds); refreshes every 5 minutes."""
import json, os, sqlite3, subprocess, sys, time
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE = Path("/mnt/afs/huangxinyue/bench-runs")
ROUNDS = {"main": BASE / "web10-main-v4-20261102", "gemini": BASE / "web10-gemini-v4-20261102", "gpt": BASE / "web10-gpt-v4-20261102", "r1-fable": BASE / "web10-rerun1-fable", "r1-kimi": BASE / "web10-rerun1-kimi"}  # later rounds override earlier cells
OUT = BASE / "web10-process.md"
CST = timezone(timedelta(hours=8))
REPO = "/mnt/afs/gaoyongyong/code/rate_website_figma-sft-cc-tap-benchmark-design"
NODE = "/mnt/afs/gaoyongyong/.nvm/versions/node/v22.23.2/bin/node"
NODE22_ENV = {**os.environ, "PATH": "/mnt/afs/gaoyongyong/.nvm/versions/node/v22.23.2/bin:" + os.environ.get("PATH", "")}
ACTIVE = ("运行中", "已暂停", "停止中", "补图中")
ORDER = ["model_de5fc4c9cdb841e8", "model_claude_opus55_direct", "model_claude_fable51_login",
         "model_glm_53_flash_cc", "model_gemini_31_pro_cc", "model_kimi_k3_cc"]
TIMEOUT_MIN = 89.5  # CC runs are cut at 90 min, direct (GPT) at 95


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp() if s else None


def load(round_dir):
    plan = json.loads((round_dir / "plan.json").read_text())
    inputs = json.loads((round_dir / "inputs.json").read_text())
    accounts = json.loads((round_dir / "copy-accounts.json").read_text())["accounts"]
    cases = {c["case_id"]: c["title"] for c in json.loads((round_dir / "dataset.json").read_text())["cases"]}
    db = sqlite3.connect(f"file:{round_dir}/ui-eval.sqlite3?mode=ro", uri=True)
    tests = {r[0]: r[1] for r in db.execute("select id, title from tests")}
    runs = db.execute("select id, test_id, status, started_at, finished_at, error, exit_code from runs").fetchall()
    scores = {r[0]: r[1] for r in db.execute("select run_id, total from scale_scores where status='已完成' and total is not null")}
    by_assignment = {t["assignment_id"]: t for g in inputs["groups"] for t in g["tests"]}
    cells = {}
    for a in plan["assignments"]:
        test_ids = [k for k, v in tests.items() if v == f"{plan['id']}/{a['assignment_id']}"]
        mine = sorted((r for r in runs if r[1] in test_ids), key=lambda r: r[3] or "")
        target = by_assignment[a["assignment_id"]]["figma_url"]
        cell = {"target": target, "account": accounts.get(target.rstrip("/").split("/")[-1], "?").replace("enterprise_", ""),
                "run": None, "score": None}
        if mine:
            r = mine[-1]
            cell["run"] = {"id": r[0], "status": r[2], "start": ts(r[3]), "end": ts(r[4]), "error": (r[5] or "").strip()}
            scored = [x for x in mine if x[0] in scores]
            if scored:
                cell["score"] = scores[scored[-1][0]]
        cells[(a["model_id"], a["case_id"])] = cell
    return {m["id"]: m["name"] for m in plan["models"]}, cases, cells


def minutes(cell, now):
    r = cell["run"]
    return ((r["end"] or now) - r["start"]) / 60 if r and r["start"] else None


def label(cell, now):
    r = cell["run"]
    timed_out = r and r["status"] not in ACTIVE and (minutes(cell, now) or 0) >= TIMEOUT_MIN
    if cell["score"] is not None:
        return f"✅ {cell['score']}/53" + (" ⏱" if timed_out else "")
    if not r:
        return "⏸ 未开始"
    if r["status"] in ACTIVE:
        return f"🟢 {'补图' if r['status'] == '补图中' else '推理'}中 {minutes(cell, now):.0f}m"
    if r["status"] == "生成失败" and not timed_out:
        return "❌ 推理失败"
    return "🔍 待核验/评分" + (" ⏱" if timed_out else "")


def render():
    now = time.time()
    names, cases, cells = {}, {}, {}
    for d in ROUNDS.values():
        n, c, cl = load(d)
        names.update(n); cases.update(c); cells.update(cl)
    models = [m for m in ORDER if m in names]
    cases = dict(sorted(cases.items()))
    scored = sum(1 for c in cells.values() if c["score"] is not None)
    running = sum(1 for c in cells.values() if c["run"] and c["run"]["status"] in ACTIVE)
    L = ["# 网站 10 题 × 6 模型 进度（web10）", "",
         f"最后更新：{datetime.now(CST):%Y-%m-%d %H:%M:%S}（每 5 分钟自动刷新）", "",
         f"**已出分 {scored}/60 · 推理中 {running}**", "",
         "⏱ = 推理跑满时限（90 分钟，GPT 95 分钟）被中断，已有设计照常评分。", "", "## 结果矩阵", "",
         "| 模型 | " + " | ".join(cases.values()) + " | 均分 |", "|---|" + "---|" * (len(cases) + 1)]
    for m in models:
        vals = [cells[(m, c)]["score"] for c in cases if cells[(m, c)]["score"] is not None]
        avg = f"{sum(vals) / len(vals):.1f}（n={len(vals)}）" if vals else "—"
        L.append(f"| {names[m]} | " + " | ".join(label(cells[(m, c)], now) for c in cases) + f" | {avg} |")
    L += ["", "## 每题明细", "", "| 模型 | 题目 | 账号 | 状态 | 推理时长 | 副本 |", "|---|---|---|---|---|---|"]
    for m in models:
        for c in cases:
            cell = cells[(m, c)]; mins = minutes(cell, now)
            L.append(f"| {names[m]} | {cases[c]} | {cell['account']} | {label(cell, now)} | {f'{mins:.0f}m' if mins is not None else '—'} | [打开]({cell['target']}) |")
    issues = [f"- {names[k[0]]} × {cases[k[1]]}（{c['account']}）：{c['run']['error'][:160]}"
              for k, c in cells.items() if c["score"] is None and c["run"] and c["run"]["status"] not in ACTIVE and c["run"]["error"]]
    L += ["", "## 未出分且有报错（需要新副本的会在这里列出）", ""] + (issues or ["- 无"])
    L += ["", "## 说明", "",
          "- 题目与副本：`/mnt/afs/huangxinyue/projects/benchmark-design/1102_data_add.md`（用户 11-02 预分发的 60 个副本，10 个源文件只读预检通过：00/01/02/04 齐全）",
          "- query 与之前各轮同一模板；fixed-v4 评分，判官 Opus 5.5",
          "- 每个副本在它所在的账号上跑：GPT→panzhengyuan（原为 hejiatong），Opus→zuohaosheng，Fable→gaoyongyong，GLM→zhengyaozhi，Gemini→panzhengyuan，Kimi→huangxinyue；每账号同时 1 个任务",
          "- 拆成三个子轮次：`web10-main-v4-20261102`（5 个模型，11-02 03:11 开始）和 `web10-gemini-v4-20261102`（Gemini，03:11 开始）、`web10-gpt-v4-20261102`（GPT，同在 panzhengyuan，排在 Gemini 后面）",
          "- 11-03 补跑：Fable × Foodieland（`web10-rerun1-fable`，gaoyongyong）、Kimi × Shop.co（`web10-rerun1-kimi`，huangxinyue，排在 10case Kimi 补跑之后），新副本来自 1103_data.md",
          "- 自动重试关闭：失败题列出后由用户提供新副本",
          "- GPT 换账号（11-02）：hejiatong 的 Figma 额度仍然耗尽，GPT × Furniro 刚开始写入就被拒、55 秒后结束，于是本轮把 hejiatong 标为不可用。用户把 GPT 的 10 题重新复制到 panzhengyuan（`1102_data_add_gpt.md`），放在子轮次 `web10-gpt-v4-20261102` 里，等 Gemini 的 10 题跑完后自动开始；矩阵里 GPT 一行取自这个子轮次。hejiatong 上原来那 10 个 GPT 副本不再使用",
          "- 本轮起 Figma 工具单次调用有 120 秒时限（11-02 修复截图卡死），不会再因一次卡死白等 30 分钟",
          "- 开跑前已停止 6case/10case 原轮次对旧副本的重复截图（它们一直在消耗 hejiatong 的 Figma 额度）"]
    OUT.write_text("\n".join(L) + "\n")
    os.chmod(OUT, 0o600)


def alive(pidfile):
    try:
        os.kill(int(pidfile.read_text().split()[0]), 0)
        return True
    except Exception:
        return False


def nudge():
    """Late trace audits: rescore and keep the supervisors alive until every cell is settled."""
    for d in ROUNDS.values():
        if not (d / "audit-rescore.mjs").exists():
            continue
        subprocess.run([NODE, str(d / "audit-rescore.mjs")], cwd=REPO, capture_output=True, env=NODE22_ENV, timeout=600)
        # only revive rounds that have already started (staged rounds must wait for their own trigger)
        has_runs = sqlite3.connect(f"file:{d}/ui-eval.sqlite3?mode=ro", uri=True).execute("select count(*) from runs").fetchone()[0]
        if has_runs and not alive(d / "supervisor.pid"):
            subprocess.run([NODE, "scripts/bench.mjs", "run", "--dir", str(d), "--background"], cwd=REPO, capture_output=True, env=NODE22_ENV, timeout=180)


if __name__ == "__main__":
    while True:
        try:
            if "--once" not in sys.argv:
                nudge()
            render()
        except Exception as error:
            OUT.with_suffix(".err").write_text(f"{datetime.now(CST)} {error!r}\n")
        if "--once" in sys.argv:
            break
        time.sleep(300)
