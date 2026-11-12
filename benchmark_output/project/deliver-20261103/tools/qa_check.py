"""Pre-review QA over manifest.json: zero/G0, frame list vs brief, blank/cropped images, outliers, run anomalies."""
import json, re, statistics as st, collections
from pathlib import Path
from PIL import Image
import numpy as np
D = Path(__file__).resolve().parent.parent
man = json.loads((D / "manifest.json").read_text())
rows = man["items"]

def brief_frames(r):
    p = D / "requirements" / r["round"] / f"{r['case_id']}-{re.sub(r'[^A-Za-z0-9]+','-',r['title']).strip('-').lower()}.md"
    t = p.read_text()
    names = []
    for ln in t.splitlines():
        s = ln.strip()
        if re.fullmatch(r"\d{2}_[A-Za-z0-9_]+", s) and s not in names: names.append(s)
    m = re.search(r"exactly the (\d+) frames|exactly (\d+) frames", t)
    return names, (int(m.group(1) or m.group(2)) if m else None)

def img_stats(path):
    im = Image.open(path).convert("L"); w, h = im.size
    a = np.asarray(im.resize((max(1, w // 8), max(1, h // 8))), dtype=np.float32)
    hist = np.bincount((a // 8).astype(int).ravel(), minlength=32) / a.size
    return w, h, float(a.std()), float(hist.max())

model_mean = collections.defaultdict(list)
for r in rows: model_mean[r["model_name"]].append(r["score_total"])
model_mean = {k: (st.mean(v), st.pstdev(v)) for k, v in model_mean.items()}
case_scores = collections.defaultdict(list)
for r in rows: case_scores[(r["round"], r["case_id"])].append(r["score_total"])

issues = []
def add(r, kind, sev, detail): issues.append({"round": r["round"], "case": r["title"], "model": r["model_name"], "score": r["score_total"], "kind": kind, "severity": sev, "detail": detail, "run_id": r["run_id"], "copy": r["copy_figma_url"]})

for r in rows:
    if not r["g0_pass"] or r["score_total"] == 0:
        add(r, "G0 未通过 / 0 分", "高", r["g0_reason"])
    names, n = brief_frames(r)
    labels = [f["label"] for f in r["frames"]]
    dup = [l for l, c in collections.Counter(labels).items() if c > 1]
    if dup: add(r, "画板重名/重复交付", "高", f"{len(labels)} 张截图，重复：{dup[:5]}")
    if names:
        miss = [x for x in names if x not in labels]
        extra = [x for x in dict.fromkeys(labels) if x not in names]
        if miss: add(r, "缺少需求里的屏", "高" if len(miss) >= 2 or len(miss) == len(names) else "中", f"需求 {len(names)} 屏，缺 {miss}")
        if extra: add(r, "多出需求外的画板", "低", f"{extra[:6]}")
    for f in r["frames"]:
        w, h, sd, dom = img_stats(D / f["file"])
        if sd < 6 or dom > 0.93: add(r, "截图接近空白/纯色", "高", f"{f['label']}（灰度标准差 {sd:.1f}，单色占比 {dom:.0%}）")
        elif dom > 0.8: add(r, "截图大面积单色", "低", f"{f['label']}（单色占比 {dom:.0%}）")
        if h / w > 12: add(r, "截图异常细长", "低", f"{f['label']} {w}×{h}")
    for n_ in r["workspace_top_level"]:
        pass
    mm, ms = model_mean[r["model_name"]]
    if r["score_total"] and r["score_total"] < mm - 2.2 * ms: add(r, "分数明显低于该模型平均", "中", f"{r['score_total']}，该模型均分 {mm:.1f}±{ms:.1f}")
    cs = [x for x in case_scores[(r["round"], r["case_id"])] if x]
    if r["score_total"] and len(cs) > 3 and r["score_total"] < st.median(cs) - 12: add(r, "分数比同题中位数低 12 分以上", "中", f"{r['score_total']}，同题中位数 {st.median(cs)}")
    s = sum(r["items"].values())
    if r["g0_pass"] and s != r["score_total"]: add(r, "子项和≠总分", "中", f"子项和 {s}，总分 {r['score_total']}")
    if r["minutes"] is not None and r["minutes"] < 5: add(r, "推理时间过短", "中", f"{r['minutes']} 分钟，{r['turns']} 轮")
    if r["error"]: add(r, "run 带报错", "低", r["error"][:160])
    ev = " ".join(r["item_evidence"].values()) + " " + (r["g0_reason"] or "")
    hits = [k for k in ("全白", "空白屏", "无法打开", "打不开", "未加载", "加载失败", "缺图", "截图缺失") if k in ev]
    if hits: add(r, "判官依据提到截图问题", "中", "、".join(hits))

order = {"高": 0, "中": 1, "低": 2}
issues.sort(key=lambda x: (order[x["severity"]], x["round"], x["case"], x["model"]))
(D / "qa").mkdir(exist_ok=True)
(D / "qa" / "qa-issues.json").write_text(json.dumps(issues, ensure_ascii=False, indent=1))
c = collections.Counter((i["severity"], i["kind"]) for i in issues)
for k, v in sorted(c.items(), key=lambda kv: order[kv[0][0]]): print(k, v)
print("cells with 高:", len({(i['round'], i['case'], i['model']) for i in issues if i['severity'] == '高'}))
for i in issues:
    if i["severity"] != "低": print(i["severity"], i["round"], i["case"], i["model"], i["score"], i["kind"], "|", str(i["detail"])[:150])
