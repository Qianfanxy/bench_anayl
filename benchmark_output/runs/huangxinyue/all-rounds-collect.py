import json, sqlite3, sys
from pathlib import Path
B = Path("/mnt/afs/huangxinyue/bench-runs"); S = Path("/mnt/afs/gaoyongyong/code/rate_website_figma-sft-cc-tap-benchmark-design/storage/benchmarks")
ROUNDS = {
 "3case": [S / "3case-7models-v4-20261028"],
 "6case": [B / "6case-6models-v4-20261030"] + [B / f"6case-rerun1-{n}" for n in ("glm", "fable", "gemini", "kimi", "gpt")],
 "10case": [B / "10case-6models-v4-20261101"] + [B / f"10case-rerun1-{n}" for n in ("gemini", "kimi", "gpt")] + [B / f"10case-rerun2-{n}" for n in ("gpt", "opus", "fable", "glm", "kimi")],
 "web10": [B / "web10-main-v4-20261102", B / "web10-gemini-v4-20261102", B / "web10-gpt-v4-20261102"],
}
out = {}
for rnd, dirs in ROUNDS.items():
    cells, names, cases = {}, {}, {}
    for d in dirs:
        if not (d / "ui-eval.sqlite3").exists(): continue
        plan = json.loads((d / "plan.json").read_text())
        names.update({m["id"]: m["name"] for m in plan["models"]})
        for c in json.loads((d / "dataset.json").read_text())["cases"]: cases.setdefault(c["case_id"], c["title"])
        db = sqlite3.connect(f"file:{d}/ui-eval.sqlite3?mode=ro", uri=True)
        tests = {r[1]: r[0] for r in db.execute("select id,title from tests")}
        for a in plan["assignments"]:
            tid = tests.get(f"{plan['id']}/{a['assignment_id']}")
            if not tid: continue
            runs = db.execute("select id,status,started_at,finished_at,error,figma_url from runs where test_id=? order by started_at", (tid,)).fetchall()
            if not runs: continue
            sc = {r[0]: r[1] for r in db.execute("select run_id,total from scale_scores where test_id=? and status='已完成' and total is not null order by updated_at", (tid,))}
            scored = [r for r in runs if r[0] in sc]; r = scored[-1] if scored else runs[-1]
            from datetime import datetime
            t = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp() if s else None
            mins = (t(r[3]) - t(r[2])) / 60 if r[3] and r[2] else None
            cells[f"{a['model_id']}|{a['case_id']}"] = {"round_dir": d.name, "status": r[1], "score": sc.get(r[0]), "error": (r[4] or "").strip()[:220],
                "mins": mins, "url": r[5], "attempts": len(runs)}
    out[rnd] = {"names": names, "cases": cases, "cells": cells}
json.dump(out, open("all.json", "w"), ensure_ascii=False, indent=1)
for rnd, v in out.items():
    print(rnd, len(v["names"]), "models", len(v["cases"]), "cases", len(v["cells"]), "cells", sum(c["score"] is not None for c in v["cells"].values()), "scored")
    print("  ", v["names"])
