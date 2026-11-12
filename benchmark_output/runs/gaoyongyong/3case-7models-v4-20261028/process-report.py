#!/usr/bin/env python3
"""Refresh process.md for this benchmark run from `bench status` every few minutes."""
import json, os, subprocess, sys, time
from datetime import datetime, timezone, timedelta
from pathlib import Path

RUN = Path(__file__).resolve().parent
REPO = RUN.parents[2]
NODE = "/mnt/afs/gaoyongyong/.nvm/versions/node/v22.23.2/bin/node"
OUT, STATE = RUN / "process.md", RUN / "process-state.json"
INTERVAL = int(os.environ.get("PROCESS_INTERVAL", "300"))
CST = timezone(timedelta(hours=8))
CASES = {"case-001": "Balance", "case-002": "Paradise Invest", "case-003": "Foodgo"}
ACCOUNTS = json.loads((RUN / "runtime-policy.json").read_text()).get("model_accounts", {})

SETUP = """## 准备阶段记录
- 10-28 06:21 导入 3 题（query 沿用上次 benchmark-design 原文，仅换 URL），计划 3×7=21，fixed-v4（22 题/53 分），判官 Opus 5.5
- 10-28 06:22 3 个源模板只读检查通过：00/01/02/04 齐全，无 03
- 10-28 06:40 修复 Figma 新界面导致的复制失败（ProfileButton、"Duplicate to your drafts"）；一条未实际点击的 ambiguous 记录核对 drafts 后重置
- 10-28 07:00 enterprise_weizheng 浏览器登录失效 → 运行策略 r2：Gemini 改用 enterprise_huangxinyue
- 10-28 08:52 21 份独立副本全部就绪并验证（写权限、页面结构与源一致）
- 10-28 08:54 后端 :18194 启动（review 飞书注册因无权限跳过），监督器开始推理与评分
"""


def now():
    return datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")


def status():
    out = subprocess.run([NODE, "scripts/bench.mjs", "status", "--dir", str(RUN)], cwd=REPO,
                         capture_output=True, text=True, timeout=180)
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
    lines = [f"# 3case-7models-v4-20261028 进度", "",
             f"最后更新：{now()}（每 {INTERVAL // 60} 分钟自动刷新）", "",
             f"**已评分 {s['scored']}/{s['total']}** · 推理中 {s['active']} · 有产物 {s['design_present']} · "
             f"无交付 {s['no_delivery']} · 评分失败 {s['judge_failures']} · 阶段 `{s['phase']}`"
             + (" · **全部结束**" if s.get("finished") else ""), "",
             "## 结果矩阵", "", "| 模型 | Figma 账号 | 可用 | " + " | ".join(CASES.values()) + " | 均分 |",
             "|---|---|---|" + "---|" * len(CASES) + "---|"]
    for m in models:
        res = s["resources"].get(m, {})
        ok = "✅" if res.get("available") else ("❌ " + (str(res.get("http_status") or "") or "超时") if res else "—")
        scores = [by[f"{m}|{c}"]["score_total"] for c in CASES if by.get(f"{m}|{c}", {}).get("score_total") is not None]
        avg = f"{sum(scores) / len(scores):.1f}（n={len(scores)}）" if scores else "—"
        lines.append(f"| {names[m]} | {ACCOUNTS.get(m, '').replace('enterprise_', '')} | {ok} | "
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
    lines += ["", "## 副本链接", "", "| 模型 | " + " | ".join(CASES.values()) + " |", "|---|" + "---|" * len(CASES)]
    for m in models:
        lines.append(f"| {names[m]} | " + " | ".join(
            f"[副本]({by[f'{m}|{c}']['target_figma_url']})" if by.get(f"{m}|{c}", {}).get("target_figma_url") else "—" for c in CASES) + " |")
    lines += ["", "## 事件日志（最新在前）", ""] + [f"- {e}" for e in reversed(events[-80:])]
    lines += ["", SETUP]
    return "\n".join(lines) + "\n"


def main():
    state = json.loads(STATE.read_text()) if STATE.exists() else {"cells": {}, "events": [], "resources": {}}
    while True:
        try:
            # Scoring needs the read-only trace audit; rescore runs that failed only for lack of it.
            rescore = subprocess.run([NODE, str(RUN / "audit-rescore.mjs")], cwd=REPO, capture_output=True, text=True, timeout=600)
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
                return
        except Exception as error:  # keep refreshing; record the failure in the report header
            with OUT.open("a") as f:
                f.write(f"\n> {now()} 刷新失败：{str(error)[:200]}\n")
        if "--once" in sys.argv:
            return
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
