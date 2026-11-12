#!/usr/bin/env python3
"""Merged progress for 6case-6models-v4-20261030 plus its rerun1 rounds; refreshes every 5 minutes."""
import json, os as _os
NODE22_ENV = {**_os.environ, "PATH": "/mnt/afs/gaoyongyong/.nvm/versions/node/v22.23.2/bin:" + _os.environ.get("PATH", "")}
import json, os, sqlite3, subprocess, sys, time
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE = Path("/mnt/afs/huangxinyue/bench-runs")
MAIN = BASE / "6case-6models-v4-20261030"
RERUNS = {**{n: BASE / f"6case-rerun1-{n}" for n in ("glm", "fable", "gemini", "kimi", "gpt")}, "r2-gemini": BASE / "6case-rerun2-gemini", "r3-gpt": BASE / "6case-rerun3-gpt"}  # later rounds override
OUT = BASE / "6case-process.md"
CASES = {"case-001": "StockWave", "case-002": "Nectar", "case-003": "Stylish", "case-004": "Chat Bot AI", "case-005": "FinX", "case-006": "Fruit Hub"}
CST = timezone(timedelta(hours=8))
REPO = "/mnt/afs/gaoyongyong/code/rate_website_figma-sft-cc-tap-benchmark-design"
NODE = "/mnt/afs/gaoyongyong/.nvm/versions/node/v22.23.2/bin/node"
ACTIVE = ("运行中", "已暂停", "停止中", "补图中")


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp() if s else None


def load(round_dir):
    """Latest run + finished score per (model, case) for one round."""
    plan = json.loads((round_dir / "plan.json").read_text())
    inputs = json.loads((round_dir / "inputs.json").read_text())
    accounts = json.loads((round_dir / "copy-accounts.json").read_text())["accounts"]
    db = sqlite3.connect(f"file:{round_dir}/ui-eval.sqlite3?mode=ro", uri=True)
    tests = {r[0]: r[1] for r in db.execute("select id, title from tests")}
    runs = db.execute("select id, test_id, status, started_at, finished_at, error, figma_url from runs").fetchall()
    scores = {r[0]: r[1] for r in db.execute("select run_id, total from scale_scores where status='已完成' and total is not null")}
    by_assignment = {t["assignment_id"]: t for g in inputs["groups"] for t in g["tests"]}
    cells = {}
    for a in plan["assignments"]:
        test_ids = [k for k, v in tests.items() if v == f"{plan['id']}/{a['assignment_id']}"]
        mine = sorted((r for r in runs if r[1] in test_ids), key=lambda r: r[3] or "")
        target = by_assignment[a["assignment_id"]]["figma_url"]
        cell = {"target": target, "account": accounts.get(target.rstrip("/").split("/")[-1], "?").replace("enterprise_", ""),
                "attempts": len(mine), "run": None, "score": None}
        if mine:
            r = mine[-1]
            scored = [x for x in mine if x[0] in scores]
            cell["run"] = {"id": r[0], "status": r[2], "start": ts(r[3]), "end": ts(r[4]), "error": (r[5] or "").strip()}
            if scored:
                cell["score"] = scores[scored[-1][0]]
        cells[(a["model_id"], a["case_id"])] = cell
    return plan, cells


def label(cell, now):
    if cell["score"] is not None:
        return f"✅ {cell['score']}/53"
    r = cell["run"]
    if not r:
        return "⏸ 未开始"
    if r["status"] in ACTIVE:
        mins = (now - r["start"]) / 60 if r["start"] else 0
        return f"🟢 {'补图' if r['status'] == '补图中' else '推理'}中 {mins:.0f}m"
    if r["status"] == "生成失败":
        return "❌ 推理失败"
    return "🔍 待核验/评分"


def render():
    now = time.time()
    plan, cells = load(MAIN)
    names = {m["id"]: m["name"] for m in plan["models"]}
    source = {k: "main" for k in cells}
    for n, d in RERUNS.items():
        if (d / "ui-eval.sqlite3").exists():
            _, rc = load(d)
            for k, v in rc.items():
                cells[k] = v; source[k] = n
    lines = [f"# 6 题 × 6 模型 汇总进度（含补跑）", "",
             f"最后更新：{datetime.now(CST):%Y-%m-%d %H:%M:%S}（每 5 分钟自动刷新）", "",
             "标 🔁 的格子来自补跑轮次（用户 10-31 提供的新副本），已替换原轮次结果。", "", "## 结果矩阵", "",
             "| 模型 | " + " | ".join(CASES.values()) + " | 均分 |", "|---|" + "---|" * (len(CASES) + 1)]
    scored_total = 0
    for m in names:
        row, vals = [], []
        for c in CASES:
            cell = cells[(m, c)]
            row.append(("🔁 " if source[(m, c)] != "main" else "") + label(cell, now))
            if cell["score"] is not None:
                vals.append(cell["score"]); scored_total += 1
        avg = f"{sum(vals) / len(vals):.1f}（n={len(vals)}）" if vals else "—"
        lines.append(f"| {names[m]} | " + " | ".join(row) + f" | {avg} |")
    lines.insert(4, f"**已出分 {scored_total}/36**")
    lines.insert(5, "")
    lines += ["", "## 补跑明细", "", "| 模型 | 题目 | 账号 | 状态 | 推理时长 | 新副本 | 备注 |", "|---|---|---|---|---|---|---|"]
    for k, cell in cells.items():
        if source[k] == "main":
            continue
        r = cell["run"]
        dur = f"{((r['end'] or now) - r['start']) / 60:.0f}m" if r and r["start"] else "—"
        err = (r["error"][:80] if r and cell["score"] is None else "")
        lines.append(f"| {names[k[0]]} | {CASES[k[1]]} | {cell['account']} | {label(cell, now)} | {dur} | [打开]({cell['target']}) | {err} |")
    issues = [f"- {names[k[0]]} × {CASES[k[1]]}（{'补跑' if source[k] != 'main' else '原轮次'}）：{c['run']['error'][:140]}"
              for k, c in cells.items() if c["score"] is None and c["run"] and c["run"]["status"] not in ACTIVE and c["run"]["error"]]
    lines += ["", "## 未出分且有报错", ""] + (issues or ["- 无"])
    stage_b = (BASE / "rerun1-stage-b.log").read_text().strip() if (BASE / "rerun1-stage-b.log").exists() else ""
    lines += ["", "## 说明", "",
              "- 11-02 修复 Fable × FinX：平台截图环节竞态导致画板 19:183 的原始响应文件被覆盖（截图本身正确），经用户同意只读重截 10 张、凭据核对通过后重新评分 → 35/53；旧截图备份在原轮次 trace-finalization/TEST-021-figma-frames.bak-20261101",
              "- 原轮次目录：`/mnt/afs/huangxinyue/bench-runs/6case-6models-v4-20261030/`（自身明细见其 process.md）",
              "- 补跑目录：`/mnt/afs/huangxinyue/bench-runs/6case-rerun1-{glm,fable,gemini,kimi,gpt}/`",
              f"- 第二批（Kimi、GPT）：{'已启动 ' + stage_b.splitlines()[0] if stage_b else '等待 Fable、Gemini 补跑结束后自动启动'}",
              "- 原轮次的原副本自动重启已停用；自动新建副本的重试未开启，失败题列出后由用户提供新副本。"]
    OUT.write_text("\n".join(lines) + "\n")


def alive(pid_file):
    try:
        os.kill(int(pid_file.read_text().strip()), 0)
        return True
    except (OSError, ValueError):
        return False


def nudge():
    """Reruns' supervisors exit before the trace audit lands; audit, rescore and restart them."""
    for d in RERUNS.values():
        if not (d / "ui-eval.sqlite3").exists():
            continue
        _, cells = load(d)
        pending = [c for c in cells.values() if c["run"] and c["score"] is None and c["run"]["status"] not in ACTIVE]
        if not pending:
            continue
        subprocess.run([NODE, str(d / "audit-rescore.mjs")], cwd=REPO, capture_output=True, env=NODE22_ENV, timeout=600)
        if not alive(d / "supervisor.pid"):
            subprocess.run([NODE, "scripts/bench.mjs", "run", "--dir", str(d), "--background"], cwd=REPO, capture_output=True, env=NODE22_ENV, timeout=180)


if __name__ == "__main__":
    while True:
        try:
            if "--once" not in sys.argv:
                nudge()
            render()
        except Exception as error:  # keep refreshing through transient DB states
            OUT.with_suffix(".err").write_text(f"{datetime.now(CST)} {error!r}\n")
        if "--once" in sys.argv:
            break
        time.sleep(300)
