"""Build the arena hand-off package: manifest + frozen frames for every final (case, model) cell.

Read-only over run directories; later dirs in each round override earlier ones only when they
have a scored run (same rule as the process.md reports).
"""
import csv, hashlib, json, re, shutil, sqlite3, struct, sys
from datetime import datetime
from pathlib import Path

B = Path("/mnt/afs/huangxinyue/bench-runs")
S = Path("/mnt/afs/gaoyongyong/code/rate_website_figma-sft-cc-tap-benchmark-design/storage/benchmarks")
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "/mnt/afs/huangxinyue/projects/benchmark-design/deliver-20261103")
ROUNDS = {
    "3case": [S / "3case-7models-v4-20261028", B / "3case-rerun1-gemini"],
    "6case": [B / "6case-6models-v4-20261030"] + [B / f"6case-rerun1-{n}" for n in ("glm", "fable", "gemini", "kimi", "gpt")] + [B / "6case-rerun2-gemini", B / "6case-rerun3-gpt"],
    "10case": [B / "10case-6models-v4-20261101"] + [B / f"10case-rerun1-{n}" for n in ("gemini", "kimi", "gpt")]
              + [B / f"10case-rerun2-{n}" for n in ("gpt", "opus", "fable", "glm", "kimi")] + [B / f"10case-rerun3-{n}" for n in ("gpt", "kimi", "opus3")],
    "web10": [B / "web10-main-v4-20261102", B / "web10-gemini-v4-20261102", B / "web10-gpt-v4-20261102", B / "web10-rerun1-fable", B / "web10-rerun1-kimi"],
}
TITLE_FIX = {("6case", "case-001"): "StockWave", ("6case", "case-002"): "Nectar", ("6case", "case-003"): "Stylish",
             ("6case", "case-004"): "Chat Bot AI", ("6case", "case-005"): "FinX", ("6case", "case-006"): "Fruit Hub"}  # display names used in reports
ITEMS = ["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4", "B5", "G1", "G2", "D1", "D2", "D3", "D4", "E1", "E2", "F1", "F2", "F3", "F4", "F5"]
slug = lambda s: re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
ts = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp() if s else None


def png_size(p):
    with open(p, "rb") as f:
        h = f.read(24)
    return struct.unpack(">II", h[16:24]) if h[:8] == b"\x89PNG\r\n\x1a\n" else (None, None)


def jload(p):
    try:
        return json.loads(Path(p).read_text())
    except Exception:
        return None


cells, cases, models = {}, {}, {}
for rnd, dirs in ROUNDS.items():
    base = dirs[0].name
    for d in dirs:
        if not (d / "ui-eval.sqlite3").exists():
            print("skip (no db)", d); continue
        plan, ds = jload(d / "plan.json"), jload(d / "dataset.json")
        for m in plan["models"]:
            models[m["id"]] = {"model_id": m["id"], "name": m["name"], "provider": m.get("provider"), "api_model": m.get("model_id"), "generation_mode": m.get("generation_mode")}
        for c in ds["cases"]:
            cases.setdefault((rnd, c["case_id"]), {"round": rnd, "case_id": c["case_id"], "title": TITLE_FIX.get((rnd, c["case_id"]), c["title"]), "source_figma_url": c["source_figma_url"], "source_file_key": c["source_file_key"], "source_query": c["source_query"]})
        db = sqlite3.connect(f"file:{d}/ui-eval.sqlite3?mode=ro", uri=True)
        tests = {r[1]: r[0] for r in db.execute("select id,title from tests")}
        for a in plan["assignments"]:
            tid = tests.get(f"{plan['id']}/{a['assignment_id']}")
            if not tid: continue
            runs = db.execute("select id,status,run_dir,figma_url,started_at,finished_at,error,turn_count from runs where test_id=? order by started_at", (tid,)).fetchall()
            if not runs: continue
            sc = {}
            for r in db.execute("select run_id,id,total,g0_pass,g0_reason,cc_values,evidence,image_manifest,image_paths,eval_model_id,method,updated_at from scale_scores "
                                "where test_id=? and status='已完成' and total is not null and method='fixed_v4' order by updated_at", (tid,)):
                sc[r[0]] = r
            scored = [r for r in runs if r[0] in sc]
            run = scored[-1] if scored else runs[-1]
            key = (rnd, a["case_id"], a["model_id"])
            prev = cells.get(key)
            s = sc.get(run[0])
            off = d / "offline-judge" / "result.json"
            if not s and off.exists():  # user-approved out-of-band judge (trace not verified), same rubric/judge
                o = jload(off)
                if o["run_id"] == run[0] and o["plan_hash"] == plan["content_hash"]:
                    s = (o["run_id"], "offline-judge", o["total"], int(o["g0_pass"]), o["g0_reason"], json.dumps(o["cc_values"]),
                         json.dumps(o["evidence"], ensure_ascii=False), json.dumps(o["image_manifest"]), json.dumps(o["image_paths"]), o["judge"], "fixed_v4", o["at"])
                    scored = [run]
            if prev and prev["score_total"] is not None and not s:
                continue  # never replace a scored cell by an unscored rerun
            cells[key] = {"score_source": "offline-judge（推理轨迹未核验，用户批准）" if s and s[1] == "offline-judge" else "platform","round": rnd, "case_id": a["case_id"], "model_id": a["model_id"], "source_round_dir": str(d), "is_rerun": d.name != base,
                          "test_id": tid, "run_id": run[0], "run_status": run[1], "run_dir": run[2], "figma_url": run[3], "started_at": run[4], "finished_at": run[5],
                          "minutes": round((ts(run[5]) - ts(run[4])) / 60, 1) if run[4] and run[5] else None, "turns": run[7], "attempts_in_dir": len(runs),
                          "error": (run[6] or "").strip()[:300], "score_row": s,
                          "score_total": s[2] if s else None}

rows, missing = [], []
for key in sorted(cells, key=lambda k: (list(ROUNDS).index(k[0]), k[1], k[2])):
    c = cells[key]; rnd, cid, mid = key
    case = cases[(rnd, cid)]
    rd = Path(c["run_dir"]) if c["run_dir"] else None
    art = jload(rd / "benchmark-artifact.json") if rd else None
    inp = jload(rd / "benchmark-input.json") if rd else None
    s = c.pop("score_row")
    frames = []
    if s:
        manifest, paths = json.loads(s[7] or "[]"), json.loads(s[8] or "[]")
        dest = OUT / "frames" / rnd / f"{cid}-{slug(case['title'])}" / slug(models[mid]["name"])
        dest.mkdir(parents=True, exist_ok=True)
        for i, (m, p) in enumerate(zip(manifest, paths), 1):
            src = Path(p)
            if not src.exists():
                missing.append(str(src)); continue
            name = f"{i:02d}_{slug(m['label'])}.png"
            shutil.copy2(src, dest / name)
            w, h = png_size(dest / name)
            frames.append({"index": i, "label": m["label"], "node_id": m["file_name"].removesuffix(".png").replace("-", ":"),
                           "file": str((dest / name).relative_to(OUT)), "width": w, "height": h,
                           "sha256": hashlib.sha256((dest / name).read_bytes()).hexdigest()})
    ws = (art or {}).get("workspace") or {}
    rows.append({
        **{k: case[k] for k in ("round", "case_id", "title", "source_figma_url")},
        "model_id": mid, "model_name": models[mid]["name"],
        "account": ((inp or {}).get("runtime") or {}).get("account_identity"),
        "copy_figma_url": c["figma_url"] or (inp or {}).get("target", {}).get("url"),
        "copy_file_key": (art or {}).get("file_key") or (inp or {}).get("target", {}).get("fileKey"),
        "workspace_page_id": ws.get("id"), "workspace_page_name": ws.get("name"),
        "workspace_top_level": [{"id": n["id"], "name": n["name"], "type": n["type"]} for n in ws.get("children", [])],
        **{k: c[k] for k in ("is_rerun", "source_round_dir", "test_id", "run_id", "run_status", "run_dir", "started_at", "finished_at", "minutes", "turns", "error")},
        "score_total": s[2] if s else None, "score_source": c.get("score_source", "platform"), "score_max": 53, "rubric": "fixed_v4", "judge_model_id": s[9] if s else None, "score_id": s[1] if s else None,
        "g0_pass": bool(s[3]) if s else None, "g0_reason": s[4] if s else None,
        "items": json.loads(s[5]) if s else {}, "item_evidence": json.loads(s[6] or "{}") if s else {},
        "frames": frames, "frame_count": len(frames),
    })

meta = {"generated_at": datetime.now().astimezone().isoformat(timespec="seconds"), "rubric": "fixed_v4 (22 items, max 53, G0 gate)", "judge": "Opus 5.5",
        "rounds": {r: [str(d) for d in ds] for r, ds in ROUNDS.items()}, "selection_rule": "per (round, case, model): last scored fixed_v4 run; later rerun dirs override earlier ones only if scored",
        "models": list(models.values()), "cases": list(cases.values()), "cell_count": len(rows),
        "scored": sum(r["score_total"] is not None for r in rows), "frame_count": sum(r["frame_count"] for r in rows)}
(OUT / "manifest.json").write_text(json.dumps({"meta": meta, "items": rows}, ensure_ascii=False, indent=1))
with open(OUT / "manifest.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["round", "case_id", "title", "model_name", "model_id", "account", "score_total", "g0_pass", *ITEMS, "frame_count", "copy_figma_url",
                "workspace_page_id", "is_rerun", "run_id", "minutes", "frames_dir", "source_figma_url", "g0_reason", "score_source"])
    for r in rows:
        w.writerow([r["round"], r["case_id"], r["title"], r["model_name"], r["model_id"], r["account"], r["score_total"], r["g0_pass"],
                    *[r["items"].get(k, "") for k in ITEMS], r["frame_count"], r["copy_figma_url"], r["workspace_page_id"], r["is_rerun"], r["run_id"], r["minutes"],
                    str(Path(r["frames"][0]["file"]).parent) if r["frames"] else "", r["source_figma_url"], r["g0_reason"], r["score_source"]])
with open(OUT / "frames-sha256.txt", "w") as f:
    for r in rows:
        for fr in r["frames"]:
            f.write(f"{fr['sha256']}  {fr['file']}\n")
print(json.dumps({k: meta[k] for k in ("cell_count", "scored", "frame_count")}), "missing frames:", len(missing))
for r in rows:
    if r["score_total"] is None or not r["frames"] or not r["workspace_page_id"]:
        print("CHECK", r["round"], r["title"], r["model_name"], r["score_total"], r["frame_count"], r["workspace_page_id"], r["run_status"])
for m in missing[:10]: print("missing", m)
