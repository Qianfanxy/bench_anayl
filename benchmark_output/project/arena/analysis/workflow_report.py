"""Build the first-pass workflow report and a local evidence review workbench."""
from pathlib import Path
import csv,json,html,collections as C,hashlib,zipfile
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch,FancyBboxPatch
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'results_eval/workflow_analysis'
s=json.load(open(OUT/'summary.json'));bundles=json.load(open(OUT/'workflow_evidence.json'));events=pd.read_csv(OUT/'workflow_units.csv').fillna('');runs=pd.read_csv(OUT/'run_workflows.csv');profiles=pd.read_csv(OUT/'model_workflow_profiles.csv');N=len(runs)
LABELS={'O':'任务与环境理解','P':'资源与设计系统准备','C':'界面构建与修改','I':'交互与状态实现','V':'产物验证','D':'交付声明','U':'待判定'}
COLORS={'O':'#6e8eaf','P':'#a68cbb','C':'#348c90','I':'#d29a55','V':'#bb6e78','D':'#60776d','U':'#d6dbe1'}
ORDER=['Opus','GPT','Fable','GLM','Kimi','Gemini']
# Per-run organization patterns, distinct from outcome quality.
org=[]
for b in bundles:
 rr=b['meta'];es=[e for e in b['events'] if e['success']];cs=[i for i,e in enumerate(es) if 'C' in e['labels'].split(';')];first=min(cs) if cs else len(es)
 z=dict(run_id=rr['run_id'],case_id=rr['case_id'],model=rr['model'],preconstruction_orientation=any('O' in e['labels'].split(';') for e in es[:first]),preconstruction_preparation=any('P' in e['labels'].split(';') for e in es[:first]),preconstruction_units=first,UI_units=sum('C' in e['labels'].split(';') for e in es),bundled_UI_interaction=any('C' in e['labels'].split(';') and 'I' in e['labels'].split(';') for e in es),standalone_interaction=any(e['primary']=='I' for e in es),readback_interaction_properties=any('interaction_property_readback' in e['subtypes'] for e in es),api_probe=any('api_schema_probe' in e['subtypes'] for e in es),declared_revision=any('declared_revision' in e['subtypes'] for e in es),mixed_work_units=sum(len(e['labels'].split(';'))>1 for e in es))
 org.append(z)
pd.DataFrame(org).to_csv(OUT/'workflow_organization.csv',index=False,encoding='utf-8-sig')
orgdf=pd.DataFrame(org)
# Preserve targeted analyst samples as an audit trail, not an independent reliability estimate.
samples=[]
for model in ORDER:
 for case in ['10case-case-001','web10-case-001']:
  x=events[(events.model==model)&(events.case_id==case)&events.success]
  for stage in ['P','C','I','V']:
   a=x[x.primary==stage]
   if len(a):
    rr=a.iloc[0].to_dict();rr['review_scope']='Targeted analyst examination of purpose cues; not blinded independent full-code validation';samples.append(rr)
pd.DataFrame(samples).to_csv(OUT/'targeted_review_samples.csv',index=False,encoding='utf-8-sig')
revision_log=[{'issue':'Output-object serialization mistaken for document mutation','example':'Investment Wallet component inspectors in Fable/Kimi/Gemini','decision':'Ignore property assignments to locally declared ordinary object literals; keep node-creation and edit operations.'},{'issue':'Reference screenshot mistaken for final product verification','example':'Investment Wallet early screenshots of source components','decision':'Before product construction, unresolved-reference screenshot maps to preparation; screenshot of known final screen maps to verification.'},{'issue':'Mixed work unit forced into one stage','example':'Investment Wallet GPT construction script','decision':'Keep P+C+I multi-labels; use one primary label only for reduced timeline visualization.'},{'issue':'API schema probe mistaken for user-screen construction','example':'Furniro GLM temporary reaction-schema frames','decision':'Code environment/API adaptation separately, with an orthogonal probe tag.'},{'issue':'Stored helper code mistaken for rendered UI','example':'Furniro drawing utilities and component preparation','decision':'Use explicit preparation purpose, not merely the presence of createFrame text.'},{'issue':'Compaction summary mistaken for final handoff','example':'Merged/subagent trajectory formats','decision':'Use the full selected log when available; require a visible response after the final tool result.'}]
(OUT/'coding_revision_log.json').write_text(json.dumps(revision_log,ensure_ascii=False,indent=2))
# Diagram shows a selected frequent backbone and observed return edge, not an imposed universal order.
t={(r['source'],r['target']):r['runs'] for r in s['top_transitions']};alltrans=pd.read_csv(OUT/'transitions.csv');t.update({(r.source,r.target):r.runs for _,r in alltrans.iterrows()})
prev={r['stage']:r['runs_with_successful_evidence'] for r in s['stage_prevalence']}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'pdf.fonttype':42,'svg.fonttype':'none','savefig.dpi':200})
fig,ax=plt.subplots(figsize=(13,4.7));ax.set_xlim(-.15,11.8);ax.set_ylim(-.2,4.3);ax.axis('off')
positions={'O':(.1,2.05),'P':(2.45,2.05),'C':(4.8,2.05),'V':(7.15,2.05),'D':(9.5,2.05),'I':(6.0,.15)}
names={'O':'Context & constraints','P':'Resources & system','C':'UI construction','V':'Verification','D':'Handoff statement','I':'Interaction & states'}
for st,(x,y) in positions.items():
 ax.add_patch(FancyBboxPatch((x,y),1.9,.72,boxstyle='round,pad=0.06',facecolor=COLORS[st],edgecolor='white'))
 ax.text(x+.95,y+.43,names[st],ha='center',va='center',fontsize=9,color='white',fontweight='bold');ax.text(x+.95,y+.17,f'{prev[st]}/{N} runs',ha='center',va='center',fontsize=9,color='white')
for a,b in [('O','P'),('P','C'),('C','V'),('V','D')]:
 x,y=positions[a];xx,yy=positions[b];ax.add_patch(FancyArrowPatch((x+1.97,y+.36),(xx-.06,yy+.36),arrowstyle='-|>',mutation_scale=12,color='#6b7785',lw=1.6));ax.text((x+1.9+xx)/2,y+.66,f'{t.get((a,b),0)/N:.0%}',ha='center',fontsize=9,color='#526071')
ax.add_patch(FancyArrowPatch((8.1,2.84),(5.75,2.84),connectionstyle='arc3,rad=.45',arrowstyle='-|>',mutation_scale=13,color=COLORS['V'],lw=2));ax.text(6.92,3.7,f'Verification → UI return: {t.get(("V","C"),0)/N:.0%} of runs',ha='center',fontsize=10,color=COLORS['V'])
for a,b,start,end,tx,ty in [('C','I',(5.75,1.99),(6.4,.93),5.25,1.3),('I','V',(7.65,.93),(8.1,1.99),8.15,1.3)]:
 ax.add_patch(FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=12,color='#8f7b66',lw=1.5));ax.text(tx,ty,f'{t.get((a,b),0)/N:.0%}',ha='center',fontsize=9,color='#526071')
ax.set_title('A shared scaffold with recurrent construction–verification loops',loc='left',fontweight='bold',pad=10)
fig.text(.065,.015,'Initial rule-assisted coding. Edge labels: share of runs with adjacent primary stages, not transition probabilities. Mixed-stage calls remain multi-labelled.',fontsize=8,color='#667085')
for ext in ['png','pdf','svg']:fig.savefig(OUT/('fig0_common_workflow.'+ext),bbox_inches='tight',facecolor='white')
plt.close(fig)

def table(headers,rows):return '<table><thead><tr>'+''.join('<th>'+html.escape(str(x))+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(str(x))+'</td>' for x in rr)+'</tr>' for rr in rows)+'</tbody></table>'
parts=['''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Figma设计任务的共同工作流与执行差异</title><style>body{font:16px/1.8 system-ui,sans-serif;color:#263648;max-width:1200px;padding:24px;margin:28px auto}h1,h2,h3{line-height:1.4}h2{margin-top:38px}table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:10px;border-bottom:1px solid #dfe5eb;text-align:left}th{background:#eef3f8}a{color:#315a8c}img{width:100%}figure{margin:25px 0}figcaption{font-size:13px;color:#526071}.note{border-left:4px solid #348c90;background:#eef6f5;padding:16px}code{background:#f2f4f7}li{margin:7px 0}</style><h1>Figma设计任务的共同工作流与执行差异</h1><p>第一轮全量轨迹梳理，2026年11月8日。先归纳“在约束下制作可编辑、可复用、可持续操作的Figma文件”的工作过程，再比较各模型在这个共同结构中的组织方式。以下是规则辅助的初稿，不冒充全量人工验证或已经达到理论饱和的工作流分类。</p>''']
parts.append(f'<div class="note">29×6=174个候选格子均找到非空轨迹；按用户要求隔离Chat Bot AI×GPT，实际编码173条轨迹、{s["coded_units"]:,}个工具调用/交付声明单元。保留同一调用的多个功能标签，并把错误、重试、清理、API适配作为跨阶段标签。<a href="review.html">逐条工作流与证据查看器</a>。</div>')
parts.append('<h2>任务一：共同工作流是什么</h2><p>共同骨架可概括为：建立任务与资源上下文，构建界面及交互，通过多种检查返回修改，最后形成交付声明。真实路径不是所有模型都依次完整经过的六步流水线；组件准备可能贯穿构建，交互可以嵌入同一构建脚本，验证也可能触发资源检查或重建。</p><figure><img src="fig0_common_workflow.png"><figcaption>Shared scaffold from first-pass trajectory coding. Nodes indicate observable work purposes, not independently certified task completion. The diagram displays selected frequent primary-stage transitions; the full transition matrix includes additional returns and branches. Multi-purpose calls retain all labels in the evidence table.</figcaption></figure>')
codebook=[['O','任务与环境理解','账号核验、任务/规范读取、文档结构检查、工具权限或API能力探测','读取不等于理解；API探测不等于构建用户屏幕'],['P','资源与设计系统准备','素材/基础组件定位，变量、样式、业务组件、绘图辅助设施的准备','组件创建代码存在不代表实际复用正确；可与C/I重叠'],['C','界面构建与修改','屏幕组装、内容填充、布局调整、对已有界面的修改','成功脚本不等于设计正确；同一调用可构建多个屏幕'],['I','交互与状态实现','原型连接、滚动/固定层设置和交互相关状态写入','配置属性不等于经过真实交互验收，不能认为交互完整可用'],['V','产物验证','最终屏幕截图，或构建后的结构、文本、原型属性回读','局部检查、参考组件截图和完整交付验收必须区分'],['D','交付声明','最后工具结果之后，含文件链接和Workspace上下文的可见答复','是声明，不是独立确认交付完成；没有识别到也不等于没有交付']]
parts.append(table(['编码','功能阶段','可观察证据','边界'],codebook))
parts.append(table(['阶段','有成功调用/可见声明证据的运行','占173条'],[[LABELS[p['stage']],p['runs_with_successful_evidence'],f"{p['share']:.1%}"] for p in s['stage_prevalence'] if p['stage']!='U']))
parts.append('<p>上述共性部分来自统一提示词：基准明确要求读取任务、规范、组件与素材，并要求构建、截图和交付。因此不能把阶段普遍出现本身写成“自主涌现的最佳工作流”。更值得分析的是：同样的要求如何被组织为不同的执行路径，以及各阶段实际检查的对象和标准。</p>')
pat=s['patterns'];parts.append(table(['观察到的组织方式','运行数','判定方式'],[['构建与验证交错',pat.get('interleaved_build_verify',0),'成功界面构建之后、最后一次成功界面修改之前，出现验证单元'],['构建后再验证',pat.get('build_then_verify',0),'识别到的产物验证只出现在最后一次成功界面修改之后'],['未观察到构建后的产物验证',pat.get('no_postconstruction_verification',0),'不解释成模型从未进行任何形式的检查']]))
parts.append(f'<p>另有{int(orgdf.bundled_UI_interaction.sum())}/{N}条轨迹在同一成功调用中同时出现界面构建与交互相关设置。把每个调用强行分到一个阶段，会把这些实现误读为“缺少交互步骤”。第一次界面构建前，{int(orgdf.preconstruction_orientation.sum())}条已有任务/环境证据，{int(orgdf.preconstruction_preparation.sum())}条已有资源/准备证据；这只是可见调用顺序，不是对模型内部计划的推断。</p>')
parts.append('<figure><img src="fig1_workflow_transitions.png"><figcaption>Run-level prevalence of adjacent distinct primary-stage transitions after unsuccessful calls are excluded and consecutive equal labels are collapsed. Cells are not row-normalized probabilities and can sum above 100%; one run may contain several transitions. Tool-call ordering does not resolve concurrency inside batches.</figcaption></figure>')
parts.append('<h2>任务二：在共同结构中比较执行方式</h2><p>这一轮先比较路径，不用分数定义工作流类别。质量数据只留在已核实同版本的144个run上；不把四个不匹配Gemini版本的当前轨迹接到历史Arena评分，也不使用Chat Bot AI整题的人评推导质量关系。</p>')
rows=[]
for _,p in profiles.iterrows():
 o=orgdf[orgdf.model==p.model];rr=runs[runs.model==p.model]
 rows.append([p.model,int(p.runs),int(p.interleaved_build_verify),int(p.build_then_verify),f'{o.preconstruction_units.median():.0f}',f'{o.UI_units.median():.0f}',f'{o.bundled_UI_interaction.mean():.0%}',f'{o.api_probe.mean():.0%}'])
parts.append(table(['模型','轨迹数','交错构建/验证','构建后验证','首次界面构建前单元数中位数','界面构建/修改单元数中位数','构建/交互同调用占比','有API适配探测占比'],rows))
parts.append('<p>这些数量受脚本颗粒度影响：一次大脚本可以完成多屏，多次调用也可能只完成一个组件。不能把调用多解释为投入更多，也不能把交错循环多解释为质量更好。模型内任务差异和同任务不同模型的对照，都需要保留。</p><figure><img src="fig2_all_run_timelines.png"><figcaption>All 173 workflow paths, grouped by model and task. The horizontal axis is relative observable work-unit index, not elapsed time, tokens, or cognitive effort. Colors show the reduced primary label; mixed-stage records remain available in the evidence workbench. A missing GPT Chat Bot AI row is excluded by design.</figcaption></figure><figure><img src="fig3_stage_coverage.png"><figcaption>Observed stage coverage by model. Coverage means at least one successful tool call with the corresponding functional code, or a visible final handoff statement. It does not establish completion, correct resource use, or effective verification.</figcaption></figure>')
parts.append('<h2>同一任务的初步对照：Investment Wallet</h2>')
parts.append(table(['模型','可回溯片段','目前可支持的组织方式判断'],[['Opus','工具调用3检查组件/素材；24构建Wallet；25截图；43写原型连接','资源与系统准备、屏幕构建、视觉检查和连接实现可以区分；不凭这一例推断所有任务一致'],['GPT','调用2集中读取任务/规范/资源；调用3同时包含P+C+I；调用4单独接原型；随后截图回读','存在把多屏和共享组件集中构建的方式，不能按一次调用只计一个阶段'],['Kimi','调用9开始Wallet，随后重建和截图；调用31接原型；后续还回到布局修正','构建与验收多次交错；但静态截图与文本检查不等于滚动状态已正确验证'],['Gemini','调用16创建Wallet；后续分别构建屏幕；末尾原型脚本报错，运行记录API终止','应区分分段构建、晚期连接和外部终止；不能把没有后续修复一律解释为主动放弃']]))
parts.append('<p>调用序号从0计，依据当前所选完整日志/轨迹；可在<a href="review.html">证据查看器</a>按模型和题目定位。定向抽查覆盖六模型的Investment Wallet与Furniro，记录保留于<a href="targeted_review_samples.csv">抽查样本</a>；这不是独立双标，也不是全量分类准确率估计。</p>')
parts.append('<h2>质量差异下一步应落在哪些阶段</h2>')
parts.append(table(['共同阶段','需要编码的差异','已有案例为何值得检验'],[['任务/资源理解','是否把需求、资源和实现位置建立可核对映射','读取过素材目录不保证使用正确；“读了”与“落实了”应分开'],['构建与恢复','局部修复是否保持全局数量、唯一性和对象身份','GLM Fruit Hub有检查与重建，最终仍留下两套屏幕'],['交互实现与验收','是否区分视口、滚动内容、固定操作层和覆盖态','Kimi Investment Wallet有全屏截图和反复修正，仍存在滚动层级问题'],['最终验收','核对的是新建局部还是整个交付集合；是否覆盖风险屏幕','Furniro Blog没有被截查；节点存在不能证明内容可读'],['交付声明','声明的范围与实际验收证据是否一致','D阶段只说明说出了交付入口，不是完成证明']]))
parts.append('<p>这些是待统一编码的差异轴，不是已经证实的成功原因。此前8项行为计数的相关性分析仍保留，作为阶段分析后的辅助证据；这里不继续通过增加指标寻找显著性。</p>')
parts.append('<h2>编码审计与下一步</h2>')
parts.append(f'<p>当前{int(s["ambiguous_units"]):,}/{int(s["coded_units"]):,}个单元被标记为需复核，原因包括多功能重叠、只读目的兜底判断或截图目标范围不清；其余单元也没有全部人工确认。所有行保留run、来源文件、message索引、工具调用ID、描述、规则依据和代码片段。工作流标签在连接质量结果之前生成，但本轮分析者已知部分既往案例结果，不能称作完全盲法。</p>')
parts.append('<ol><li>先复核多标签和兜底单元，修正编码规范；尤其区分资源组件准备与业务屏幕构建、API探测与真实交互。</li><li>将连续调用合并为有共同目标的工作段，例如“完成首页”或“修复滚动层级”，避免脚本颗粒度支配比较。</li><li>在每个共同阶段增加“检查对象、判断标准、发现的问题、针对性修复、复查结果”编码；保留未知和无法验证。</li><li>最后在同题、同版本产物上比较阶段执行差异，结合模型内跨题变化；不能把模型身份或单个问题案例当作因果解释。</li></ol>')
parts.append('<h2>复现与文件</h2><p><code>python arena/analysis/workflow_analysis.py</code> → <code>python arena/analysis/workflow_report.py</code>。<a href="trajectory_inventory.csv">174格轨迹定位表</a> · <a href="workflow_units.csv">功能单元编码</a> · <a href="run_workflows.csv">逐run工作流</a> · <a href="coding_revision_log.json">规则修订记录</a> · <a href="summary.json">统计口径</a> · <a href="review.html">证据查看器</a>。</p></html>')
(OUT/'报告.html').write_text(''.join(parts))
# The evidence browser is embedded, so it also works when opened as a local file.
DATA=json.dumps(bundles,ensure_ascii=False,allow_nan=False).replace('</','<\\/')
viewer='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>工作流证据查看器</title><style>body{font:14px/1.7 system-ui,sans-serif;background:#f6f8fb;color:#263648;max-width:1200px;margin:25px auto;padding:20px}select,input,button{font:inherit;padding:8px;margin:5px;border:1px solid #c7d0db;border-radius:5px}article{background:white;border:1px solid #dfe5eb;border-radius:7px;padding:14px;margin:12px 0}.tag{display:inline-block;padding:2px 8px;margin-right:5px;background:#e8f0f5;border-radius:4px}.err{color:#af4444}.muted{color:#64748b;font-size:12px}code,pre{font:12px/1.6 ui-monospace,monospace;white-space:pre-wrap;word-break:break-all}h1{font-size:25px}#meta{background:#eaf2f5;padding:14px;word-break:break-all}summary{cursor:pointer}a{color:#315a8c}</style><h1>工作流证据查看器</h1><p>规则辅助初稿。标签描述调用的工作目的，不代表阶段完成或修复成功。代码为片段；完整内容按来源文件、message索引与tool_call_id回溯。未包含模型私有推理。</p><select id="model"></select><select id="run"></select><select id="stage"><option value="">全部功能阶段</option><option>O</option><option>P</option><option>C</option><option>I</option><option>V</option><option>D</option></select><label><input type="checkbox" id="amb">仅看需复核单元</label><label><input type="checkbox" id="err">仅看工具报错</label><p><a href="报告.html">返回分析报告</a></p><div id="meta"></div><div id="events"></div><script type="application/json" id="data">__DATA__</script><script>const bs=JSON.parse(document.querySelector('#data').textContent),M=document.querySelector('#model'),R=document.querySelector('#run'),S=document.querySelector('#stage'),A=document.querySelector('#amb'),E=document.querySelector('#err');const zh={O:'任务与环境',P:'资源与系统',C:'界面构建',I:'交互实现',V:'产物验证',D:'交付声明',U:'待判定'};function esc(x){return String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}for(const m of ['Opus','GPT','Fable','GLM','Kimi','Gemini'])M.add(new Option(m,m));function fill(){R.innerHTML='';bs.filter(b=>b.meta.model===M.value).forEach(b=>R.add(new Option(b.meta.case_id+' · '+b.meta.title,b.meta.run_id)));render()}function render(){const b=bs.find(b=>b.meta.run_id===R.value);if(!b)return;const x=b.meta;document.querySelector('#meta').innerHTML='<b>'+esc(x.model+' · '+x.title)+'</b><br>'+esc(x.run_id)+' · '+esc(x.pattern)+'<br><span class="muted">来源：'+esc(x.source_path)+'<br>轨迹：'+esc(x.trajectory_path)+'<br>主序列（已压缩成功调用）：'+esc(x.compressed_sequence)+'<br>严格质量连接：'+esc(x.strict_quality_eligible)+'</span>';const es=b.events.filter(e=>(!S.value||e.labels.split(';').includes(S.value))&&(!A.checked||e.review_required)&&(!E.checked||e.error));document.querySelector('#events').innerHTML='<p>显示 '+es.length+' / '+b.events.length+' 个单元</p>'+es.map(e=>'<article><div>'+e.labels.split(';').map(l=>'<span class="tag">'+esc(l+' '+zh[l])+'</span>').join('')+'<span class="'+(e.error?'err':'muted')+'">'+(e.error?'工具报错':e.success?'成功结果/可见声明':'结果缺失')+(e.review_required?' · 需复核':'')+'</span></div><b>#'+esc(e.call_index)+' '+esc(e.description||e.tool)+'</b><div class="muted">'+esc(e.rule_evidence)+'<br>附加标签：'+esc(e.subtypes)+'<br>message['+esc(e.message_index)+'] · '+esc(e.tool_call_id)+' · '+esc(e.tool)+(e.final_screen_name?' · '+esc(e.final_screen_name):'')+'</div><details><summary>代码片段与错误摘要</summary><pre>'+esc(e.code_excerpt||'此单元无脚本代码。')+'</pre><pre class="err">'+esc(e.error_excerpt)+'</pre></details></article>').join('')}M.onchange=fill;[R,S,A,E].forEach(e=>e.onchange=render);const want=new URLSearchParams(location.search).get('run');if(want){const b=bs.find(b=>b.meta.run_id===want);if(b)M.value=b.meta.model}fill();if(want){R.value=want;render()}</script></html>'''
(OUT/'review.html').write_text(viewer.replace('__DATA__',DATA))
# Save source snapshots/hashes for reproducibility; no private configs or raw log bodies are copied.
inputs=[ROOT/'results_eval/资产清单-索引.csv',ROOT/'results_eval/priority1_paper/version_audit.csv',ROOT/'arena/sorting.json']
(OUT/'input_sha256.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},indent=2))
with zipfile.ZipFile(OUT/'共同工作流第一轮分析.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in OUT.iterdir():
  if p.suffix in ['html','json','csv','png','pdf','svg']:z.write(p,p.name)
 for p in [ROOT/'arena/analysis/workflow_analysis.py',ROOT/'arena/analysis/workflow_report.py',ROOT/'arena/analysis/trajectory_io.py']:z.write(p,'scripts/'+p.name)
print('Workflow report, evidence workbench, diagram and review queue written.')
