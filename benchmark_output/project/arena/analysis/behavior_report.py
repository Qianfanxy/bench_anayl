"""Build the behavior-analysis report after extraction and statistics."""
from pathlib import Path
import json,csv,html,zipfile,hashlib
import pandas as pd
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'results_eval/behavior_analysis'
d=json.load(open(OUT/'summary.json'));f=pd.read_csv(OUT/'features.csv');r=pd.read_csv(OUT/'associations.csv');s=pd.read_csv(OUT/'sensitivity.csv');m=pd.read_csv(OUT/'model_behavior_summary.csv')
primary=r[r.adjustment=='model'];small=primary[primary.outcome=='expert_rank'];E=html.escape

def table(headers,rows):return '<table><thead><tr>'+''.join('<th>'+E(str(x))+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+E(str(x))+'</td>' for x in rr)+'</tr>' for rr in rows)+'</tbody></table>'
def fmt(x):return f"{x.beta:+.3f} [{x.lo:+.3f}, {x.hi:+.3f}]"
parts=['''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>可观察工作行为与设计结果</title><style>body{max-width:1200px;margin:36px auto;padding:24px;font:16px/1.8 system-ui,sans-serif;color:#263648}h1,h2,h3{line-height:1.35}h2{margin-top:40px}table{border-collapse:collapse;width:100%;font-size:14px}td,th{border-bottom:1px solid #dfe5eb;padding:10px;text-align:left}th{background:#eef3f8}img{width:100%}figure{margin:26px 0}figcaption{font-size:13px;color:#526071}a{color:#315a8c}.note{padding:16px;background:#eef6f5;border-left:4px solid #178577}.draft{padding:16px;background:#fbf8f3;border-left:4px solid #be813b}code{background:#f2f4f7}</style><h1>可观察工作行为与设计结果</h1><p>2026年11月8日本地快照分析。问题是行为与结果的关联，而非模型的心理动机或行为的因果作用。按版本匹配的专家偏好和Rubric分数分别分析，图表不展示评审身份或人数。</p><div class="note">主要发现：只控制任务时，截图覆盖、同屏复查与专家偏好存在正向关联；加入模型固定效应后，关联显著减弱。8项行为×2种结果的16项主要探索性检验，均未通过BH多重比较校正（最小q=0.202）。因此，现有数据支持“不同模型有不同执行方式”，但不足以证明某一计数行为独立提升质量。未检出不等于没有作用。</div>''']
parts.append('<h2>范围与轨迹质量核查</h2>')
parts.append(table(['集合','范围','用途'],[['工具行为提取','168个run，28题×6模型','140个run使用完整stream-json运行日志；28个GPT使用标准化轨迹'],['严格版本匹配主分析','144个run，24题×6模型','继承同run、原始评分记录、分数和交付图SHA256的联合核验；仅将这些run与人评连接'],['排除','Chat Bot AI整题、Qwen','旧GPT持续排除，且避免旧候选影响整题相对排序；Qwen不在Arena且只有3题'],['非严格题目','其余4题只留行为描述','未将当前run轨迹接到不同版本的人评；不混入主要回归']]))
parts.append('<p>多数GLM轨迹的metadata标为subagent/compaction_merged，故不能先假定轨迹完整。本轮逐条解析完整日志后，140个有日志的run，其工具调用ID集合与当前导出轨迹对齐，调用数量相等，所选事件均有结果记录；这消除了当前快照的工具计数差异疑虑，但不保证所有内部上下文和推理都完整。报告只测工具事件及代码，不推断私有思维质量。</p><p>benchmark-artifact.json中的brief存在截断，若从它统计需求屏幕数，会把Furniro的9屏误记为5屏。本轮分母统一从完整交付需求文档提取，并核对同题各模型完全一致。<a href="source_quality.csv">来源审计</a> · <a href="features.csv">逐run行为特征</a> · <a href="tool_event_audit.csv">工具事件索引</a>。</p>')
parts.append('<h2>什么被测量，什么没有被证明</h2>')
parts.append(table(['指标','可观察定义','解释限制'],[
['最终屏幕截图覆盖率','需求屏幕中，最终根frame ID至少成功截图一次的比例','全页拼图和后来被替换的ID不计；成功调用不等于模型识别了问题'],
['截图—修改—同屏复查覆盖率','同一最终根frame先成功截图，收到结果后有成功修改脚本，再成功截同一frame','中间修改可能作用于其他屏幕；这是可观察时序，不是修复成功率'],
['脚本报错率','use_figma调用中，明确错误结果的比例','不涵盖布局不可读、语义遗漏或返回值中的所有逻辑失败'],
['只读结构/文本验收次数','无识别到的修改操作，且遍历节点并读取文本/连线/名称/数量的成功脚本','正则代理，可能漏检；局部查询不等于全局验收'],
['实例化/克隆脚本占比','成功修改脚本中含createInstance或clone代码的比例','代码存在不等于实际调用次数，更不等于正确复用给定素材'],
['首次写入前检查次数','首次修改前的metadata或只读use_figma调用次数','不等于理解需求，也可能反映工具使用困难'],
['成功截图调用数、运行时长','可见截图事件数、索引记录分钟数','次数含同屏重复和组件截图；时间受接口延迟、报错和预算影响'],
['报错后的短期恢复，补充分析','有报错的run中，下一3个工具调用内出现成功修改的报错比例','不证明解决了原错误；未报错run不人为赋100%恢复率']]))
parts.append('<h2>主结果：先控制任务，再控制模型差异</h2>')
parts.append('<p>每项行为单独拟合结果=行为+任务固定效应+模型固定效应。专家结果取7−平均专家名次，值越大越好。计数和时长先log1p，再与比例指标一样标准化；系数对应行为增加1个样本标准差的结果变化。不是8个行为同时入模。95%区间使用按任务聚类的CR1 sandwich标准误和t(23)近似，只有24个任务簇，属于探索性区间。</p>')
rr=[]
for k,en,zh,tr in d['features']:
 a=r[(r.feature==k)&(r.outcome=='expert_rank')&(r.adjustment=='task')].iloc[0]
 b=r[(r.feature==k)&(r.outcome=='expert_rank')&(r.adjustment=='model')].iloc[0]
 rr.append([zh,fmt(a),fmt(b),f'{b.q:.3f}'])
parts.append(table(['行为','仅控制任务：专家偏好系数 [95% CI]','再控制模型：专家偏好系数 [95% CI]','校正后q'],rr))
parts.append('<figure><img src="fig2_confounding_check.png"><figcaption>Behavior–outcome associations before and after model adjustment. Each coefficient is estimated separately with task fixed effects; green additionally includes model fixed effects. Outcomes are oriented so that larger values indicate better results. Error bars are 95% task-cluster CR1 t intervals. Differences between specifications are descriptive and do not identify a causal pathway.</figcaption></figure>')
parts.append('<p>最清楚的变化是截图覆盖：与专家偏好的关联从+0.732降到+0.003；同屏复查从+0.384降到+0.205，后者区间为[-0.088,0.499]。这不支持把跨模型正相关直接解释成“让同一个模型多做这些步骤就会提升质量”。加入模型效应也会消去稳定的执行策略差异，因此并非证明这些行为没有价值。</p>')
parts.append('<figure><img src="fig1_adjusted_associations.png"><figcaption>Task- and model-adjusted associations for eight observable behaviors, estimated one at a time. Expert preference is 7 minus task-level mean expert rank. Counts and duration are log1p-transformed; all predictors are standardized. Gray indicates BH q≥0.05 in the 16-test exploratory family; confidence intervals themselves are nominal 95% intervals, not multiplicity-adjusted simultaneous intervals.</figcaption></figure>')
parts.append(table(['行为','Rubric分数系数 [95% CI]','p','BH q'],[[x.label_zh,fmt(x),f'{x.p:.4f}',f'{x.q:.3f}'] for _,x in primary[primary.outcome=='rubric_score'].iterrows()]))
parts.append('<p>截图覆盖与Rubric的调整后系数为−1.399，名义p=0.0127，但BH q=0.202，没有通过多重比较校正。不把这个负号解释为“截图有害”，也不选择性省略该结果。评分维度、触发检查的缺陷、运行选择等均可能解释此关联。</p>')
parts.append('<h2>执行画像是描述，不是成功配方</h2><figure><img src="fig3_model_profiles.png"><figcaption>Mean execution profiles across the same 24 version-matched tasks per model. These are descriptive protocol observations, not estimates of the causal effect of checking. Same-screen recheck requires a final frame ID; changed IDs and page-level screenshots are not counted.</figcaption></figure>')
parts.append(table(['模型','最终屏幕截图覆盖','同屏复查覆盖','脚本报错率','平均截图次数','中位运行分钟'],[[x.model,f'{x.screen_coverage:.1%}',f'{x.recheck_coverage:.1%}',f'{x.error_rate:.1%}',f'{x.screenshots:.1f}',f'{x.minutes:.1f}'] for _,x in m.iterrows()]))
parts.append('<p>Opus最终屏幕截图覆盖100%、同屏复查覆盖32.1%、脚本报错率11.1%；Fable复查覆盖78.5%，Kimi为66.6%，但二者专家总体排名并不优于Opus。不能据此说复查有害；它说明“复查更多”可能同时反映初稿问题更多或执行策略不同。Gemini在当前定义下未出现最终frame的同屏复查序列，不代表所有形式的检查都不存在。</p>')
parts.append('<h2>结合具体轨迹：验收针对什么，比调用次数更具体</h2>')
parts.append(table(['案例','已观察到的证据','对后续行为标注的启发'],[
['Fruit Hub · GLM','最终屏幕覆盖100%、同屏复查60%，但交付含两套同名屏幕；旧ID查询假阴性后重建，最终只核对新建ID','应检查整个交付集合的数量、唯一性及旧版本清理，而非只验证新节点存在'],
['Furniro · Gemini','9屏仅3屏有最终根frame截图；Blog没有被截查，交付Blog文字/图片明显裁切；代码中确有素材实例化','应覆盖风险屏幕并验证内容可读；有文本节点和实例化API不等于呈现正确'],
['Investment Wallet · Kimi','最终屏幕覆盖100%、同屏复查100%，但滚动作用域包含本应固定的背景/栏/操作层；静止截图及文本核对未记录滚动到中底部验证','应检查交互状态和滚动层级；截图—修改—截图的闭环仍可能漏掉运行时问题'],
['Workout Class/Investment Wallet · Gemini','原始运行结果同时记录stop_reason=refusal、terminal_reason=api_error，工具错误后没有正常后续执行','不能把缺少恢复步骤一律归为模型没有修复意愿；单独做排除终止错误的敏感性分析']]))
parts.append('<p>这些案例来自已选择的问题样本，不能当作全体run的缺陷发生率，也不能代替回归证据。它们提出更具体的可检验指标：全局唯一性验收、需求项到实现的映射、滚动/覆盖态验收，以及修复是否消除了原缺陷。详细逐例材料见<a href="../模型行为深挖/index.html">已有行为深挖</a>；本报告不将其中Chat Bot AI案例纳入统计。</p>')
parts.append('<h2>稳健性与额外分析</h2>')
parts.append('<p>另计算了：加入log1p总工具调用数的努力程度敏感性；排除infrastructure_blocked；排除观测到的terminal is_error；逐个去掉一个模型；以及每个模型内跨题的Spearman描述。加入总调用数会改变“更多行为”的含义，总调用数本身也可能是执行行为的结果，因此它不是主要控制项，不能靠它断言因果。所有结果完整导出，避免只挑有利设定。</p>')
rec=d['conditional_error_recovery'];parts.append(table(['结果','有报错run的短期恢复系数 [95% CI]','n'],[[x['outcome'],f"{x['beta']:+.3f} [{x['lo']:+.3f}, {x['hi']:+.3f}]",x['n']] for x in rec]))
parts.append('<p>恢复指标在139个有报错的匹配run中也未提供清楚的独立关联证据；这仍只是“后续写入成功”，不是原问题修复完成。恢复分析独立列为补充探索，不混用主要16检验的q。</p>')
parts.append('<h2>可写进论文的表述</h2><div class="draft"><p>We examined observable tool-use behaviors on 144 version-matched design runs spanning 24 tasks and six model configurations. Screenshot coverage and same-screen rechecking were positively associated with expert preference in task-adjusted analyses (0.732 and 0.384 preference-rank points per standard deviation, respectively). These associations weakened after accounting for model fixed effects (0.003 and 0.205), and none of the 16 primary behavior–outcome tests survived Benjamini–Hochberg correction. Thus, cross-model process differences should not be interpreted as evidence that increasing the frequency of a behavior improves an individual model’s output.</p><p>Qualitative trajectory audits further show that procedural coverage need not imply effective verification: complete screenshot coverage can coexist with duplicated deliverables or incorrect scrolling structure. These cases motivate measuring what is verified and whether a detected defect is resolved, rather than relying solely on tool-call counts. These observations are exploratory and do not establish a causal benefit of verification.</p></div>')
parts.append('<h2>下一步最值得补的证据</h2><p>将“检查质量”标注为可回放的证据链：目标需求或缺陷→检查对象→工具或截图证据→针对性修改→相同缺陷复查结果。对全部匹配run按统一规则标注，保留未知状态和双人复核，再分析与结果的关联。不能只在已知低分案例中找问题。若要证明行为有效，需要同模型、同任务、同预算的随机化流程干预，例如强制最终全局唯一性验收或滚动状态验收；单凭当前观察数据不能替代这种实验。</p>')
parts.append('<h2>复现、限制和文件</h2><ul><li>主样本的每个任务×模型只有一个最终采用的run；包含不等次数的补跑，因此存在选择偏差，不是同模型同任务的随机对照。</li><li>专家偏好来自现有2位评审，覆盖不均；按题内平均连接产物，不以会话数扩大样本量。图中不展示身份或人数。区间固定当前模型和评审面板，不能外推专家总体或所有模型。</li><li>固定效应消除题目和模型的平均差异，不能控制特定模型在特定任务上的难度、初稿质量和隐藏失败。仅24个任务簇，聚类区间为近似；未显著可能来自小样本、量测误差、行为饱和或有限变异。</li><li>每个行为分开估计，不能解释成控制了其他所有行为。8项×2结果的主要16检验统一BH校正，不把补充探索算作独立验证。</li><li>源码方法检测是代理，不证明脚本分支执行、素材语义正确或修复成功。最终ID覆盖忽略旧ID、全页拼图及没有独立根frame的状态；对模型工作流可能产生不同测量偏差。</li><li>工具错误不等于设计错误；API/安全终止不等于模型自主放弃。GPT没有run.log，终止结果不完整观察，不将缺失当正常完成。</li></ul><p>运行顺序：<code>python arena/analysis/behavior_analysis.py</code> → <code>python arena/analysis/behavior_statistics.py</code> → <code>python arena/analysis/behavior_report.py</code>。</p><p><a href="features.csv">逐run行为与结果</a> · <a href="associations.csv">全部回归与校正</a> · <a href="sensitivity.csv">敏感性分析</a> · <a href="conditional_error_recovery.csv">条件错误恢复</a> · <a href="summary.json">口径与结果JSON</a> · <a href="tool_event_audit.csv">可回溯工具事件</a></p></html>')
(OUT/'报告.html').write_text(''.join(parts))
inputs=[ROOT/'results_eval/资产清单-索引.csv',ROOT/'results_eval/priority1_paper/version_audit.csv',ROOT/'arena/sorting.json']
(OUT/'input_sha256.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},indent=2))
with zipfile.ZipFile(OUT/'工作行为与设计结果.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in OUT.iterdir():
  if p.suffix in ['html','png','pdf','svg','csv','json'] and p.name!='tool_event_audit.csv':z.write(p,p.name)
 for p in [ROOT/'arena/analysis/behavior_analysis.py',ROOT/'arena/analysis/behavior_statistics.py',ROOT/'arena/analysis/behavior_report.py']:z.write(p,'scripts/'+p.name)
print('Report, captions, aggregate plots, audit tables and reproducible package written.')
