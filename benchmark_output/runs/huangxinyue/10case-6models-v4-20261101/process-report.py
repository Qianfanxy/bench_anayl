#!/usr/bin/env python3
"""Refresh process.md for this benchmark run from `bench status` every few minutes."""
import json, os as _os
NODE22_ENV = {**_os.environ, "PATH": "/mnt/afs/gaoyongyong/.nvm/versions/node/v22.23.2/bin:" + _os.environ.get("PATH", "")}
import json, os, subprocess, sys, time
from datetime import datetime, timezone, timedelta
from pathlib import Path

RUN = Path(__file__).resolve().parent
REPO = Path("/mnt/afs/gaoyongyong/code/rate_website_figma-sft-cc-tap-benchmark-design")
NODE = "/mnt/afs/gaoyongyong/.nvm/versions/node/v22.23.2/bin/node"
OUT, STATE = RUN / "process.md", RUN / "process-state.json"
INTERVAL = int(os.environ.get("PROCESS_INTERVAL", "300"))
CST = timezone(timedelta(hours=8))
CASES = {"case-001": "Investment Wallet", "case-002": "Travelin", "case-003": "Stock Trading", "case-004": "Meet", "case-005": "Expenio", "case-006": "Payment Wallet", "case-007": "Vulcan Invest", "case-008": "Fitness App", "case-009": "Workout Class", "case-010": "Budget"}
COPY_ACCOUNTS = json.loads((RUN / "copy-accounts.json").read_text())["accounts"]
ACCOUNTS = json.loads((RUN / "runtime-policy.json").read_text()).get("model_accounts", {})

SETUP = """## 准备阶段记录
- 11-01 导入 10 题（Investment Wallet/Travelin/Stock Trading/Meet/Expenio/Payment Wallet/Vulcan Invest/Fitness App/Workout Class/Budget），query 与上轮同一模板；10 个源文件只读预检通过（00/01/02/04 均有内容）
- 计划 10×6=60（Opus/Fable/GLM/Gemini/Kimi/GPT），fixed-v4，判官 Opus 5.5；绑定 1101_data_test.md 的 60 个预分发副本
- 每模型固定一个账号：GPT→hejiatong，Opus→zuohaosheng，Fable→gaoyongyong，GLM→zhengyaozhi，Gemini→panzhengyuan，Kimi→huangxinyue；每账号同时 1 个任务，总并发 6
- 自动重试关闭（含原副本自动重启）；失败题按约定从源文件复制新副本后重跑
"""


def now():
    return datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")


def status():
    out = subprocess.run([NODE, "scripts/bench.mjs", "status", "--dir", str(RUN)], cwd=REPO,
                         capture_output=True, env=NODE22_ENV, text=True, timeout=180)
    if out.returncode:
        raise RuntimeError(out.stderr.strip()[-300:])
    return json.loads(out.stdout)


def cell(row):
    gen, score = row.get("generation_status") or "未开始", row.get("score_total")
    if score is not None:
        return f"✅ {score}/{row.get('score_max', 53)}" + ("" if row.get("g0_pass") in (None, True, "通过") else " (G0✗)")
    if row.get("score_error"):
        return "⚠️ 评分失败"
    if row.get("score_status") in ("评分中", "排队中", "运行中"):
        return "⚖️ 评分中"
    return {"尚未启动": "⏸ 未开始", "运行中": "🟢 推理中", "排队中": "⏳ 排队", "补图中": "📸 截图取证",
            "等待评分": "🔍 待评分", "已完成": "🔍 待评分", "失败": "❌ 失败"}.get(gen, gen)


def key(row):
    return f"{row['model_id']}|{row['case_id']}"


def render(s, events):
    rows = s["rows"]
    models = list(dict.fromkeys(r["model_id"] for r in rows))
    by = {key(r): r for r in rows}
    names = {r["model_id"]: r["model_name"] for r in rows}
    lines = [f"# 10case-6models-v4-20261101 进度", "",
             f"最后更新：{now()}（每 {INTERVAL // 60} 分钟自动刷新）", "",
             f"**已评分 {s['scored']}/{s['total']}** · 推理中 {s['active']} · 有产物 {s['design_present']} · "
             f"无交付 {s['no_delivery']} · 评分失败 {s['judge_failures']} · 阶段 `{s['phase']}`"
             + (" · **全部结束**" if s.get("finished") else ""), "",
             "## 结果矩阵", "", "| 模型 | 可用 | " + " | ".join(CASES.values()) + " | 均分 |",
             "|---|---|" + "---|" * len(CASES) + "---|"]
    for m in models:
        res = s["resources"].get(m, {})
        ok = "✅" if res.get("available") else ("❌ " + (str(res.get("http_status") or "") or "超时") if res else "—")
        scores = [by[f"{m}|{c}"]["score_total"] for c in CASES if by.get(f"{m}|{c}", {}).get("score_total") is not None]
        avg = f"{sum(scores) / len(scores):.1f}（n={len(scores)}）" if scores else "—"
        lines.append(f"| {names[m]} | {ok} | "
                     + " | ".join(cell(by[f'{m}|{c}']) if f"{m}|{c}" in by else "—" for c in CASES) + f" | {avg} |")
    problems = [r for r in rows if r.get("generation_error") or r.get("score_error")]
    unavailable = {m: r for m, r in s["resources"].items() if not r.get("available")}
    if problems or unavailable or s.get("evidence_errors"):
        lines += ["", "## 当前问题", ""]
        for m, r in unavailable.items():
            lines.append(f"- **{names.get(m, m)}** 不可用：{(r.get('error') or '')[:160]}")
        for r in problems:
            lines.append(f"- {r['model_name']} × {CASES[r['case_id']]}：{(r.get('generation_error') or r.get('score_error'))[:200]}")
        for run, err in (s.get("evidence_errors") or {}).items():
            lines.append(f"- 取证 {run}：{err[:160]}")
    lines += ["", "## 副本链接（链接文字为副本所在账号）", "", "| 模型 | " + " | ".join(CASES.values()) + " |", "|---|" + "---|" * len(CASES)]
    for m in models:
        lines.append(f"| {names[m]} | " + " | ".join(
            f"[{COPY_ACCOUNTS.get(by[f'{m}|{c}']['target_figma_url'].rstrip('/').split('/')[-1], '?').replace('enterprise_', '')}]({by[f'{m}|{c}']['target_figma_url']})" if by.get(f"{m}|{c}", {}).get("target_figma_url") else "—" for c in CASES) + " |")
    lines += ["", "## 事件日志（最新在前）", ""] + [f"- {e}" for e in reversed(events[-80:])]
    lines += ["", SETUP]
    return "\n".join(lines) + "\n"


def main():
    state = json.loads(STATE.read_text()) if STATE.exists() else {"cells": {}, "events": [], "resources": {}}
    while True:
        try:
            # Scoring needs the read-only trace audit; rescore runs that failed only for lack of it.
            rescore = subprocess.run([NODE, str(RUN / "audit-rescore.mjs")], cwd=REPO, capture_output=True, env=NODE22_ENV, text=True, timeout=600)
            if rescore.returncode == 0 and '"rescored":["' in rescore.stdout:
                state["events"].append(f"{now()} 审计后重新提交评分：{rescore.stdout.strip()[-200:]}")
            elif rescore.returncode:
                state["events"].append(f"{now()} 审计/补评分失败：{rescore.stderr.strip()[-160:]}")
            s = status()
            names = {r["model_id"]: r["model_name"] for r in s["rows"]}
            for r in s["rows"]:
                c = cell(r)
                if state["cells"].get(key(r)) != c:
                    if key(r) in state["cells"] or c not in ("未开始",):
                        state["events"].append(f"{now()} {r['model_name']} × {CASES[r['case_id']]}：{state['cells'].get(key(r), '未开始')} → {c}")
                    state["cells"][key(r)] = c
            for m, r in s["resources"].items():
                avail = bool(r.get("available"))
                if state["resources"].get(m) != avail:
                    state["events"].append(f"{now()} {names.get(m, m)} 资源{'可用' if avail else '不可用：' + (r.get('error') or '')[:80]}")
                    state["resources"][m] = avail
            OUT.write_text(render(s, state["events"]))
            STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1))
            if s.get("finished"):
                if s.get("judge_failures") and not state.get("final_audit_done"):
                    # The supervisor exits once the matrix is finished; audit once more and restart it so late scores land.
                    state["final_audit_done"] = True
                    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1))
                    subprocess.run([NODE, "scripts/bench.mjs", "run", "--dir", str(RUN), "--background"], cwd=REPO, capture_output=True, env=NODE22_ENV, timeout=180)
                else:
                    return
        except Exception as error:  # keep refreshing; record the failure in the report header
            with OUT.open("a") as f:
                f.write(f"\n> {now()} 刷新失败：{str(error)[:200]}\n")
        if "--once" in sys.argv:
            return
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
