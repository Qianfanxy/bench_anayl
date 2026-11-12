"""Behaviour & failure, step 2: code the judge's evidence into concrete failure manifestations.

Input: out/item_evidence.csv (from failure_collect.py). Only evidence for items that LOST points is
coded (score < max); a sentence in a full-score evidence that says "no overlap" would otherwise
match. A match is dropped when a negation (没有 / 未见 / 无 / 不存在 / 避免 / 未出现) sits within
six characters before it.

Modes:
  code      -> out/failure_codes.csv (run x item x manifestation), prints coverage
  validate  -> random matched snippets per manifestation + random uncoded lost-point evidence
  report    -> tables R_9_*: prevalence by model, manifestation x item, link to behaviour/product

Usage: .venv/bin/python failure_taxonomy.py out code|validate|report
"""
import os
import random
import re
import sys

import numpy as np
import pandas as pd

OUT, MODE = sys.argv[1], sys.argv[2]
TAB = os.path.join(OUT, "tables")
pd.set_option("display.width", 240)

# manifestation -> (group, pattern). Patterns are matched on the raw evidence text.
TAX = {
    # --- catastrophic / completeness
    "screen_clipped_or_empty": ("completeness", r"画板高度|只露出|只剩页头|只有页头|仅有页头|主体(全|为)?空|全空|整屏|空页|页面缺失|主流程不可见|主体内容.{0,6}(缺失|不可见|被裁切)"),
    "black_or_unreadable_screen": ("completeness", r"全黑|黑底上.{0,8}(看不清|不可见|难以辨认)|纯黑背景|近乎不可见"),
    "content_missing": ("completeness", r"(没有|无|缺少|缺失|未绘制|没画|未画出|不存在)(任何)?(输入框|表单|搜索框|按钮|加入购物车|结算|支付|步骤条|进度条|开关|步进器|图表|列表|卡片)|(关键|核心)(控件|内容|模块).{0,4}(缺失|不存在|全部缺失)"),
    "purpose_unclear": ("comprehension", r"(判断|推断).{0,10}(页面)?用途|无法明确.{0,6}(主要对象|用途)|只能大致猜测|不易判断(这是|页面)|难以判断.{0,6}(页面|是)|需要?结合.{0,10}才能(推断|判断)"),
    # --- controls degenerate
    "text_only_controls": ("controls", r"纯文字|纯文本|只是.{0,6}文字|仅为文字|文字描述|描述文字|占位稿|线框|没有(按钮|卡片|容器)?外形|无法识别为可(点击|操作)|不像可点|不像按钮|同样式的白色文字|与正文(同样式|无区别|无差异)"),
    "placeholder_icons": ("controls", r"方块占位|占位(方块|色块|图标|符号)|色块(代替|占位|充当)|图标.{0,6}(占位|方块|缺失|没有|未绘制|为空|是色块)|没有图标|无图标|emoji|纯色(圆|方|块)|圆点代替"),
    "unlabeled_controls": ("controls", r"没有标签|无标签|缺少标签|缺少字段名|没有字段名|字段名缺失|无法得知要输入|输入要求无法"),
    "icon_ambiguous_semantics": ("controls", r"(依赖|依靠|结合|靠).{0,8}(文字|标题|旁边|上下文).{0,8}(才能|理解|判断|区分)|不够直观|含义(模糊|不明)|无法联想|难以区分|不能区分含义"),
    # --- layout defects
    "overlap": ("layout", r"重叠|叠压|压在|压住|遮住|遮挡|覆盖(在|了)|叠在|盖住|互相挤压|相互压|交叠"),
    "overflow_clipping": ("layout", r"溢出|超出(画布|画板|父级|容器|边界|屏幕)|裁切|被截|截断|截成|右侧被裁|出画|越界"),
    "misalignment_spacing": ("layout", r"不齐|错位|未对齐|没有对齐|对齐(混乱|不一)|间距(失衡|不一|混乱|过小|过大|不等|偏松)|贴住|贴边|挤在|拥挤|挤压|紧贴|过于靠近|留白不足|内边距(不足|过小|不一)"),
    "empty_space": ("layout", r"空白|空洞|空泛|空隙|留空|大片空|大面积空|空荡"),
    "size_proportion": ("layout", r"比例失当|比例失调|尺寸不协调|尺寸(过小|过大|不一)|字号(过小|偏小|过大)|过宽|过窄|偏小|偏细|太小"),
    # --- state & navigation
    "no_current_state": ("state", r"没有.{0,10}(当前|选中|高亮|激活)|无.{0,8}(当前|选中|高亮)态?|未选中|都未选中|选中态.{0,6}(缺失|没有|不明|不可辨|一致)|未(标出|标注|显示)当前|看不出(所处|当前)|当前(位置|步骤|项).{0,6}(无法|不明|不清|无从)|始终高亮|都是同一|同色同字重"),
    "missing_navigation": ("state", r"没有底部导航|无底部导航|缺少(底部)?导航|导航(缺失|时有时无)|没有(返回|出口)|出口(不可|缺失|不明)|下一步.{0,4}(无从|不明|无法|靠猜)|去向.{0,4}(靠猜|不明)"),
    "input_feedback_missing": ("state", r"未提示|无法确认.{0,10}(选中|提交|付款|用哪|会用)|无法核对|不显示.{0,10}(金额|数量|手续费)"),
    # --- hierarchy & typography
    "flat_hierarchy": ("hierarchy", r"同字号|同字重|同一字号|同一号|同样(字号|大小|样式|粗细)|层级(缺失|扁平|不清|不足|单一)|主次(不分|难辨|难分|无别|缺失)|没有(主次|层级)|等距排列|扁平"),
    "weak_emphasis": ("hierarchy", r"主操作.{0,6}(过弱|不突出|缺失|无差异|与正文)|强调(过弱|不足|不当|对象不当|方式异常)|重点(不突出|无法突出|表达不足)|淹没|争抢|同等突出|同色同(样式|权重)|强调程度(接近|分散)|危险操作.{0,8}(缺少区分|同色|未区分|没有区分)|不够中立"),
    "readability_contrast": ("hierarchy", r"对比(度)?(不足|过低|偏低)|可读性(差|不足|受损)|难以阅读|辨识(受损|困难)|看不清|不可读|浅灰.{0,6}(难|不)|偏淡|难以辨认|过度弱化|主次倒置"),
    # --- color usage
    "accent_color_overused": ("color", r"强调(色)?(过多|过度|面积过大|失效|反而最弱)|两种强调色并存|抢眼|抢占注意"),
    "semantic_color_misuse": ("color", r"语义色|(涨|跌|下跌|上涨).{0,8}(绿|红|白)|(成功|警告|错误|禁用)状态.{0,8}(没有|缺失|未|无)|用色.{0,4}(冲突|误导|不当)|状态色缺失|误判"),
    # --- consistency
    "inconsistent_across_screens": ("consistency", r"不一致|不统一|不稳定|时有时无|位置(不固定|变动|不稳)|风格(突兀|冲突|不一)|各(屏|页)(不同|各异)|规则(不统一|不一)|(样式|结构|写法).{0,4}(不同|各异|冲突)|框架(偏离|失效|不稳|稳定性不足)|无法沿用"),
    "misgrouping": ("consistency", r"归组|分组(不明|混杂|不清|不当|略混)|游离|错组|混排|归属.{0,4}(不明|不清|混杂|牵强)|粒度(偏粗|不当)|混在一组|混进"),
    "sequence_disorder": ("consistency", r"顺序(略绕|不合理|颠倒)|阅读.{0,4}(中断|受阻)|需要?回看|滞后|较靠后|衔接(断裂|断开)"),
    # --- logic & content
    "logic_data_error": ("logic", r"矛盾|不符|冲突|错误|错放|不合理|自相|不自洽|计算(有误|错误)|价格(相同|重复)|完全相同|重复(的|出现)|同名同价|全部重复|缺少「|拼写|乱码|占位(文本|文案)|lorem|placeholder"),
    # --- file structure (judge reads the layer summary)
    "flat_layers_default_names": ("structure", r"默认名|「Frame」|「Rectangle」|Frame \d|Rectangle \d|嵌套.{0,4}(1|一)层|平铺|合成单个|单个文本节点|没有.{0,6}(容器|子级|分组)|缺少.{0,6}(容器|子级结构)|无法按功能区域|不能按功能"),
}
NEG = re.compile(r"(没有|未见|无明显|不存在|避免了?|未出现|不见|没出现|无任何)$")
RX = {k: re.compile(p) for k, (g, p) in TAX.items()}


def code_text(text):
    found = {}
    for k, rx in RX.items():
        hits = []
        for m in rx.finditer(text):
            pre = text[max(0, m.start() - 6):m.start()]
            if NEG.search(pre):
                continue
            hits.append(m.group(0))
        if hits:
            found[k] = hits
    return found


E = pd.read_csv(os.path.join(OUT, "item_evidence.csv"), low_memory=False)
E["evidence"] = E.evidence.fillna("").astype(str)
L = E[(E.lost > 0) & (E.evidence.str.len() > 0)].copy()

if MODE in ("code", "validate"):
    rows, uncoded = [], []
    for _, r in L.iterrows():
        f = code_text(r.evidence)
        if not f:
            uncoded.append(r)
        for k, hits in f.items():
            rows.append(dict(task_id=r.task_id, model=r.model, problem=r.problem, protocol=r.protocol, g0=r.g0,
                             item=r["item"], dimension=r.dimension, lost=r.lost, score=r.score, max=r["max"],
                             manifestation=k, group=TAX[k][0], n_hits=len(hits), first_hit=hits[0]))
    C = pd.DataFrame(rows)
    if MODE == "code":
        C.to_csv(os.path.join(OUT, "failure_codes.csv"), index=False)
        cov = 1 - len(uncoded) / len(L)
        print(f"lost-point item records {len(L)}, coded {cov:.1%}; manifestations per coded record {C.groupby(['task_id','item']).size().mean():.2f}")
        print(C.groupby(["group", "manifestation"]).agg(records=("task_id", "size"), runs=("task_id", "nunique"),
                                                        points=("lost", "sum")).sort_values("records", ascending=False).to_string())
        print("\nuncoded lost-point records by item:")
        U = pd.DataFrame(uncoded)
        print((U.groupby("item").size() / L.groupby("item").size()).round(2).sort_values(ascending=False).to_string())
    else:
        random.seed(5)
        for k in TAX:
            sub = C[C.manifestation == k]
            print(f"\n## {k} ({TAX[k][0]}) — {len(sub)} records")
            for _, r in sub.sample(min(6, len(sub)), random_state=1).iterrows():
                ev = L[(L.task_id == r.task_id) & (L["item"] == r["item"])].evidence.iloc[0]
                i = ev.find(r.first_hit)
                print(f"  [{r['item']} -{r.lost} {r.model[:10]}] …{ev[max(0, i - 45):i + 55]}…")
        print(f"\n## UNCODED lost-point evidence ({len(uncoded)})")
        for r in random.sample(uncoded, min(25, len(uncoded))):
            print(f"  [{r['item']} -{r.lost} {r.model[:10]}] {r.evidence[:150]}")
    sys.exit()

# ------------------------------------------------------------------ report
C = pd.read_csv(os.path.join(OUT, "failure_codes.csv"), low_memory=False)
runs = E.drop_duplicates("task_id")[["task_id", "model", "protocol", "g0"]]
# which items cost points, by model (share of available points lost), G0-pass runs
P = E[E.g0].groupby(["model", "item"]).apply(lambda d: d.lost.sum() / d["max"].sum()).unstack()
P.to_csv(os.path.join(TAB, "R_9_lost_share_model_x_item.csv"))
dim = E[E.g0].groupby(["model", "dimension"]).apply(lambda d: d.lost.sum() / d["max"].sum()).unstack()
print("== share of available points lost, by dimension (G0-pass runs)\n", dim.round(2).to_string())
dim.to_csv(os.path.join(TAB, "R_9_lost_share_model_x_dimension.csv"))

# prevalence: share of runs in which the manifestation appears at least once
pres = C.drop_duplicates(["task_id", "manifestation"]).groupby(["model", "manifestation"]).size().unstack(fill_value=0)
pres = pres.div(runs.groupby("model").size(), axis=0)
pres.to_csv(os.path.join(TAB, "R_9_manifestation_prevalence_by_model.csv"))
overall = C.drop_duplicates(["task_id", "manifestation"]).groupby("manifestation").size() / len(runs)
print("\n== share of runs showing each manifestation (all models)\n", overall.sort_values(ascending=False).round(2).to_string())
print("\n== by model\n", pres.T.round(2).to_string())

# points attributed: a lost-point record with k manifestations gives lost/k to each
C["pts"] = C.lost / C.groupby(["task_id", "item"]).manifestation.transform("size")
mi = C.groupby(["manifestation", "item"]).pts.sum().unstack(fill_value=0)
mi.to_csv(os.path.join(TAB, "R_9_points_manifestation_x_item.csv"))
tot = C.groupby("manifestation").pts.sum().sort_values(ascending=False)
tot.to_csv(os.path.join(TAB, "R_9_points_by_manifestation.csv"))
print("\n== points lost attributed to each manifestation (all items)\n", tot.round(0).to_string())

# one table with every count side by side, so "how often" and "how costly" can be compared directly
summary = pd.DataFrame({
    "records": C.groupby("manifestation").size(),                                   # item-evidence hits, not deduped
    "runs": C.drop_duplicates(["task_id", "manifestation"]).groupby("manifestation").size(),  # runs showing it >=1x
    "n_hits_total": C.groupby("manifestation").n_hits.sum(),                         # regex matches, incl. repeats within one sentence
    "points_raw_sum": C.groupby("manifestation").lost.sum(),                         # NOT fair-split: double-counts co-occurring tags
    "points_fair_split": tot,                                                        # fair-split across co-occurring tags in the same item
})
summary["prevalence"] = (summary.runs / len(runs)).round(3)
summary["points_per_run_shown"] = (summary.points_fair_split / summary.runs).round(2)
summary["records_per_run_shown"] = (summary.records / summary.runs).round(2)
summary = summary.sort_values("points_fair_split", ascending=False)
summary.to_csv(os.path.join(TAB, "R_9_manifestation_summary.csv"))
print("\n== combined: occurrence vs points side by side\n", summary.round(2).to_string())
print("\n== top items per manifestation\n")
for k in tot.index:
    top = mi.loc[k].sort_values(ascending=False).head(3)
    print(f"  {k:32s} " + ", ".join(f"{i} {v:.0f}" for i, v in top.items()))

# link to process/product measures (within model, problem, protocol)
try:
    O = pd.read_csv(os.path.join(OUT, "design_ops_runs.csv"), low_memory=False)[["task_id", "reuse_ratio", "autolayout_ratio", "text_share", "primitive_share"]]
    Q = pd.read_csv(os.path.join(OUT, "product_runs.csv"), low_memory=False)[["task_id", "instance_node_share", "max_depth", "nodes_per_screen", "text_node_share"]]
    B = pd.read_csv(os.path.join(OUT, "reliable_runs_behaviour.csv"), low_memory=False)[["task_id", "tool_errors_model", "assistant_turns", "hit_time_limit", "duration_s", "problem"]]
    X = runs.merge(O, on="task_id", how="left").merge(Q, on="task_id", how="left").merge(B, on="task_id", how="left")
    flags = C.drop_duplicates(["task_id", "manifestation"]).assign(v=1).pivot(index="task_id", columns="manifestation", values="v").reindex(X.task_id).fillna(0)
    X = X.set_index("task_id").join(flags)
    X = X[X.g0]

    def resid(df, y):
        key = df.model + "@" + df.protocol
        ms, ps = sorted(key.unique()), sorted(df.problem.unique())
        M = np.zeros((len(df), len(ms) + len(ps)))
        M[np.arange(len(df)), key.map({m: i for i, m in enumerate(ms)}).to_numpy()] = 1
        M[np.arange(len(df)), len(ms) + df.problem.map({p: i for i, p in enumerate(ps)}).to_numpy()] = 1
        b, *_ = np.linalg.lstsq(M, y, rcond=None)
        return y - M @ b

    pairs = [("text_only_controls", "instance_node_share", "-"), ("text_only_controls", "text_node_share", "+"),
             ("placeholder_icons", "instance_node_share", "-"), ("placeholder_icons", "reuse_ratio", "-"),
             ("overlap", "autolayout_ratio", "-"), ("misalignment_spacing", "autolayout_ratio", "-"),
             ("flat_layers_default_names", "max_depth", "-"), ("flat_layers_default_names", "autolayout_ratio", "-"),
             ("screen_clipped_or_empty", "hit_time_limit", "+"), ("content_missing", "hit_time_limit", "+"),
             ("empty_space", "nodes_per_screen", "-"), ("logic_data_error", "assistant_turns", "+")]
    rows = []
    for f, m, exp in pairs:
        d = X[X[f].notna() & X[m].notna()].reset_index()
        d[m] = d[m].astype(float)
        a = resid(d, d[f].to_numpy(float))
        b = resid(d, d[m].to_numpy(float))
        rows.append(dict(manifestation=f, measure=m, expected=exp, n=len(d), prevalence=round(d[f].mean(), 2),
                         partial_spearman=round(float(pd.Series(a).rank().corr(pd.Series(b).rank())), 3),
                         raw_spearman=round(float(d[f].rank().corr(d[m].rank())), 3)))
    LK = pd.DataFrame(rows)
    LK.to_csv(os.path.join(TAB, "R_9_manifestation_vs_behaviour.csv"), index=False)
    print("\n== manifestation vs process/product measure (exploratory; partial = within model x batch and problem)\n", LK.to_string(index=False))
except FileNotFoundError as e:
    print("link step skipped:", e)
