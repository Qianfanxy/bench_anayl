"""Pre-review sanity checks over manifest.json + frames/. Read-only. Prints findings as JSON lines + summary."""
import json, re, hashlib, statistics as st, collections, sys
from pathlib import Path
from PIL import Image
import numpy as np
D = Path(__file__).resolve().parent.parent
m = json.loads((D / "manifest.json").read_text()); items = m["items"]
req = {}
for c in m["meta"]["cases"]:
    p = next((D / "requirements" / c["round"]).glob(c["case_id"] + "-*.md"))
    names = []
    for ln in p.read_text().splitlines():
        s = ln.strip()
        if re.fullmatch(r"\d{2}_[A-Za-z0-9_]+", s) and s not in names: names.append(s)
    req[(c["round"], c["case_id"])] = names
F = []
def flag(r, kind, sev, detail): F.append({"round": r["round"], "case": r["title"], "model": r["model_name"], "kind": kind, "sev": sev, "detail": detail})
by_model = collections.defaultdict(list)
for r in items: by_model[(r["round"], r["model_name"])].append(r["score_total"])
model_all = collections.defaultdict(list)
for r in items: model_all[r["model_name"]].append(r["score_total"])
case_scores = collections.defaultdict(list)
for r in items: case_scores[(r["round"], r["case_id"])].append(r["score_total"])
IDENT = re.compile(r"claude|anthropic|opus|fable|sonnet|gpt|openai|gemini|google ai|kimi|moonshot|glm|zhipu|qwen", re.I)
for r in items:
    exp = req[(r["round"], r["case_id"])]
    labels = [f["label"] for f in r["frames"]]
    # completeness
    miss = [n for n in exp if n not in labels]
    extra = [l for l in labels if exp and l not in exp]
    dup = [l for l, k in collections.Counter(labels).items() if k > 1]
    if miss: flag(r, "缺少规定画板", "high" if len(miss) > len(exp) / 3 else "mid", miss)
    if extra: flag(r, "画板名不在需求清单", "low", extra)
    if dup: flag(r, "画板重复（同名多份）", "mid", dup)
    if not exp: flag(r, "需求里没解析出画板清单", "info", "")
    # score
    if r["score_total"] == 0 or not r["g0_pass"]: flag(r, "G0 未通过 / 0 分", "high", r["g0_reason"])
    peers = [x for x in model_all[r["model_name"]] if x]
    mu, sd = st.mean(peers), st.pstdev(peers)
    if r["score_total"] and sd and (mu - r["score_total"]) / sd > 2: flag(r, "明显低于该模型平时水平", "mid", f"{r['score_total']} vs 均值 {mu:.1f}±{sd:.1f}")
    cs = [x for x in case_scores[(r["round"], r["case_id"])] if x is not None]
    if r["score_total"] and r["score_total"] - st.median(cs) <= -10: flag(r, "比同题其他模型中位数低 10 分以上", "mid", f"{r['score_total']} vs 中位 {st.median(cs)}")
    isum = sum(r["items"].values())
    if r["g0_pass"] and isum != r["score_total"]: flag(r, "子项和≠总分", "high", f"{isum} vs {r['score_total']}")
    if r["minutes"] is not None and r["minutes"] < 8: flag(r, "推理用时很短", "low", f"{r['minutes']} 分钟")
    # identity leakage in layer names
    leak = [n["name"] for n in r["workspace_top_level"] if IDENT.search(n["name"])]
    if leak: flag(r, "画板名疑似含模型/厂商名", "high", leak)
    # image checks
    hashes = collections.Counter(f["sha256"] for f in r["frames"])
    if any(k > 1 for k in hashes.values()): flag(r, "多张截图完全相同", "mid", [f["label"] for f in r["frames"] if hashes[f["sha256"]] > 1])
    blank, odd = [], []
    for f in r["frames"]:
        im = Image.open(D / f["file"]).convert("L"); w, h = im.size
        a = np.asarray(im.resize((max(1, w // 8), max(1, h // 8))), dtype=np.float32)
        if a.std() < 6: blank.append(f"{f['label']}(std {a.std():.1f})")
        mobile = r["round"] != "web10"
        if mobile and not (360 <= w <= 440): odd.append(f"{f['label']} {w}×{h}")
        if not mobile and not (1200 <= w <= 1920): odd.append(f"{f['label']} {w}×{h}")
        # large empty bottom area (content cut / overflow) : last 25% nearly uniform while top has content
        if h > 600:
            bot = a[int(a.shape[0] * 0.75):]; 
            if bot.std() < 2 and a.std() > 15: odd.append(f"{f['label']} 底部 1/4 空白")
    if blank: flag(r, "截图几乎空白", "high", blank)
    if odd: flag(r, "画板尺寸/版式异常", "low", odd)
sev = {"high": 0, "mid": 1, "low": 2, "info": 3}
F.sort(key=lambda x: (sev[x["sev"]], x["kind"], x["round"], x["case"]))
(D / "check-findings.json").write_text(json.dumps(F, ensure_ascii=False, indent=1))
c = collections.Counter((x["sev"], x["kind"]) for x in F)
for (s, k), n in sorted(c.items(), key=lambda kv: (sev[kv[0][0]], -kv[1])): print(s, k, n)
