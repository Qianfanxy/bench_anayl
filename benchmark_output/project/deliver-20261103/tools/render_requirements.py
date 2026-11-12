"""raw/<file_key>.json -> <round>/<case_id>-<title>.md (full 00 task text + 01 foundations text, top-to-bottom order)."""
import json, re
from pathlib import Path
D = Path(__file__).resolve().parent.parent
meta = json.loads((D / "manifest.json").read_text())["meta"]
slug = lambda s: re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
index = []
for c in meta["cases"]:
    raw = json.loads((D / "requirements/raw" / f"{c['source_file_key']}.json").read_text())
    lines = [f"# {c['title']}（{c['round']} / {c['case_id']}）", "", f"- 原始模板（只读）：{c['source_figma_url']}", "- 模型收到的提示词：", "", "```", c["source_query"], "```", ""]
    total = 0
    for p in raw["pages"]:
        lines += [f"## {p['page_name']}", ""]
        for t in p["texts"]:
            s = t["text"].strip()
            if s: lines += [s, ""]; total += len(s)
    out = D / "requirements" / c["round"] / f"{c['case_id']}-{slug(c['title'])}.md"
    out.parent.mkdir(parents=True, exist_ok=True); out.write_text("\n".join(lines))
    index.append((c["round"], c["case_id"], c["title"], total, str(out.relative_to(D))))
for i in index: print(*i, sep="\t")
