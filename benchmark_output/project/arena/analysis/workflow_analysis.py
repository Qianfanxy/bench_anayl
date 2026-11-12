"""First-pass, multi-label workflow coding across all six-model task trajectories.
Labels describe observable work units, never inferred reasoning quality. Rule-assisted coding requires review.
Run: MPLCONFIGDIR=/tmp/benchmark-mpl python arena/analysis/workflow_analysis.py
"""
from pathlib import Path
import csv,json,re,collections as C,hashlib,html,zipfile,math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch,FancyBboxPatch,Patch
from trajectory_io import normalize,log_messages,texts,MUT
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'results_eval/workflow_analysis';OUT.mkdir(exist_ok=True)
MODELS={'Opus 5.5（三方A）':'Opus','gpt-6-astra':'GPT','Fable 5.1':'Fable','GLM-5.3 Flash':'GLM','Kimi K3':'Kimi','Gemini 3.5 Flash':'Gemini'}
ORDER=['Opus','GPT','Fable','GLM','Kimi','Gemini']
STAGES=['O','P','C','I','V','D','U']
LABELS={'O':'Orient / inspect constraints','P':'Prepare resources / system','C':'Construct / modify UI','I':'Implement interactions','V':'Verify artifact','D':'Declare handoff','U':'Unresolved'}
ZH={'O':'任务与环境理解','P':'资源与设计系统准备','C':'界面构建与修改','I':'交互与状态实现','V':'产物验证','D':'交付声明','U':'待判定'}
COLORS={'O':'#6e8eaf','P':'#a68cbb','C':'#348c90','I':'#d29a55','V':'#bb6e78','D':'#60776d','U':'#d6dbe1'}
R=list(csv.DictReader(open(ROOT/'results_eval/资产清单-索引.csv',encoding='utf-8-sig')))
VA={r['arena_run_id']:r for r in csv.DictReader(open(ROOT/'results_eval/priority1_paper/version_audit.csv',encoding='utf-8-sig'))}
STRICT_CASES={c for c in {v['case_id'] for v in VA.values()} if sum(v['case_id']==c and v['strict_eligible']=='True' for v in VA.values())==6}
B=pd.read_csv(ROOT/'results_eval/behavior_analysis/features.csv');B={r.run_id:r.to_dict() for _,r in B.iterrows()}

def writecsv(name,rows):
 if not rows:return
 with open(OUT/name,'w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def clean(s,n=320):
 s=re.sub(r'https?://[^\s"<>]+','[URL]',s);s=re.sub(r'[\w.+-]+@[\w.-]+','[EMAIL]',s)
 return s[:n]
def has(s,p):return bool(re.search(p,s,re.I))
def mutates_node(code):
 # Ignore assignments to ordinary output objects used in read-only inspectors.
 strong=has(code,r'figma\.create(?:Frame|Text|Component|Rectangle|Vector|Variable|Style|NodeFromSvg)|\.(?:createInstance|clone|appendChild|insertChild|remove|resize|setReactionsAsync|setBoundVariable)\s*\(')
 if strong:return True
 plain=set(re.findall(r'(?:const|let|var)\s+(\w+)\s*=\s*\{',code))
 assignments=re.findall(r'\b([A-Za-z_$][\w$]*)\.(?:characters|fills|strokes|reactions|layoutMode|x|y|name|fontSize|cornerRadius|clipsContent|overflowDirection|scrollBehavior)\s*=(?!=)',code)
 return any(v not in plain for v in assignments)


inventory=[];all_events=[];runs=[];bundles=[]
for r in R:
 if r['model'] not in MODELS:continue
 case=r['round']+'-'+r['case_id'];excluded=case=='6case-case-004' and r['model']=='gpt-6-astra'
 p=Path(r['trajectory_path']);exists=p.exists() and p.stat().st_size>0
 inventory.append(dict(case_id=case,title=r['title'],model=MODELS[r['model']],run_id=r['run_id'],trajectory_path=str(p),trajectory_exists=exists,trace_format=r['trajectory_source'],run_log=r['run_log'],included=not excluded and exists,exclusion='Chat Bot AI GPT: quarantined per user; no replacement human/trajectory alignment asserted' if excluded else '',arena_version_match=VA.get(r['run_id'],{}).get('same_run','False'),strict_quality_eligible=(case in STRICT_CASES and VA.get(r['run_id'],{}).get('strict_eligible')=='True')))
 if excluded or not exists:continue
 d=json.load(open(p));calls=normalize(d.get('messages',[]));source='trajectory';terminal={};source_path=str(p);selected_messages=d.get('messages',[])
 if r['run_log'] and Path(r['run_log']).exists():
  msgs,bad,terminal=log_messages(r['run_log']);lc=normalize(msgs)
  if {t['id'] for t in calls}<={t['id'] for t in lc}:calls=lc;source='run.log';source_path=r['run_log'];selected_messages=msgs
 artifact=json.load(open(Path(r['run_dir'])/'benchmark-artifact.json'))
 pages=artifact.get('pages',[]);page_ids={n['id']:n['name'] for n in pages}
 roots={n['id']:n['name'] for n in artifact.get('workspace',{}).get('children',[]) if n.get('type')=='FRAME' and re.match(r'^\d\d[_ ·-]',n['name'])}
 req=next((ROOT/'deliver-20261103/requirements'/r['round']).glob(r['case_id']+'-*.md'))
 expected=sorted(set(re.findall(r'^\s*(\d\d_[A-Za-z][A-Za-z0-9_]+)\s*$',req.read_text(),re.M)))
 # Classify purpose using code/visible tool description and structural context. Keep overlapping purposes.
 firstwrite=next((t['index'] for t in calls if t['write']),len(calls));firstC=None;events=[]
 for t in calls:
  name=t['name'];code=t['code'];t['write']=bool('use_figma' in name and mutates_node(code));desc=str(t['args'].get('description',''));hint=desc.lower();node=t['node'];after=firstC is not None;labs=set();why=[];sub=[]
  orientation=has(hint,r'brief|start here|foundations|requirements|task text|design rules|任务|需求|规范')
  prep=has(hint,r'media|assets?|resources?|components?|design system|tokens?|styles?|素材|组件|设计系统|变量|样式')
  verify=has(hint,r'audit|verif|validat|check|inspect.*(?:screen|workspace)|read.?back|assert|missing|duplicate|验收|核查|验证|检查|回读|查重|核对')
  if 'whoami' in name:labs.add('O');why.append('account/environment tool')
  elif 'get_metadata' in name or 'get_design_context' in name:
   if node in roots:labs.add('V');why.append('read final screen metadata')
   elif after and verify:labs.add('V');why.append('post-build inspection intent')
   elif prep or (node in page_ids and has(page_ids[node],r'components|media')):labs.add('P');why.append('reference resource structure')
   else:labs.add('O');why.append('reference/document inspection')
  elif t['screenshot']:
   if node in roots:labs.add('V');why.append('screenshot targets final named screen');sub.append('visual_final_screen')
   elif not after:labs.add('P');why.append('reference screenshot before product construction');sub.append('reference_visual')
   else:labs.add('V');why.append('post-construction screenshot, target scope unresolved');sub.append('visual_other_scope')
  elif 'use_figma' in name:
   if has(hint,r'permission.{0,12}(?:test|probe)|write.permission test|权限.{0,6}测试|测试.{0,6}权限'):
    labs.add('O');why.append('environment permission probe, not product construction');sub.append('permission_probe')
   elif t['write']:
    actual_prep=has(code,r'figma\.create(?:Component|Variable|TextStyle|PaintStyle|EffectStyle)|\.createVariable\s*\(')
    interact=has(code,r'\.(?:reactions|overflowDirection|scrollBehavior|prototypeStartNode|flowStartingPoints)\s*=(?!=)|setReactionsAsync\s*\(')
    screen_literal=any(re.search(r'[\x22\x27`]'+re.escape(s)+r'[\x22\x27`]',code) for s in expected)
    screen_intent=has(hint,r'screens?|onboarding|checkout|\bhome\b|屏幕|画板|(?:build|create|construct).{0,35}\bpages?\b|(?:构建|创建|绘制).{0,20}页面')
    ui_create=has(code,r'figma\.create(?:Frame|Text|Rectangle|Vector|NodeFromSvg)|\.createInstance\s*\(|\.clone\s*\(')
    pure_interaction=interact and not ui_create and not actual_prep
    pure_prep=((actual_prep or prep or (not after and has(hint,r'helper|utilities|utility|辅助|工具函数')) or (not after and not ui_create)) and not screen_literal and not screen_intent and not pure_interaction)
    if actual_prep or pure_prep:labs.add('P');why.append('component/token/style preparation code or intent')
    if not pure_interaction and not pure_prep:labs.add('C');why.append('UI construction/modification code')
    if interact:
     labs.add('I');why.append('prototype/scroll/state property write')
     if has(code,r'\.reactions\s*=(?!=)|setReactionsAsync\s*\('):sub.append('prototype_write')
     if has(code,r'\.(?:overflowDirection|scrollBehavior)\s*=(?!=)'):sub.append('scroll_property_write')
    if verify and has(code,r'findAll|findOne|getNodeById|\.children'):sub.append('mixed_write_and_inspection')
    if has(code,r'\.remove\s*\('):sub.append('deletion_or_cleanup')
    if has(code,r'setCurrentPageAsync|loadAllPagesAsync'):sub.append('explicit_page_context')
   else:
    if orientation:labs.add('O');why.append('brief/constraint inspection intent')
    if prep:labs.add('P');why.append('resource/system inspection intent')
    scope_workspace=has(hint,r'workspace|screen|屏幕|工作区') or any(n in code for n in roots)
    if after and (verify or scope_workspace):labs.add('V');why.append('post-build structural/readback inspection');sub.append('structural_readback')
    if not labs:
     labs.add('V' if after else 'O');why.append('phase-based fallback for unclassified read-only script');sub.append('fallback')
    if 'V' in labs and has(code,r'\.reactions|overflowDirection|scrollBehavior'):sub.append('interaction_property_readback')
  explicit_screen_build=has(hint,r'(?:build|create|implement|construct|rebuild|complete|render).{0,45}(?:\d\d_|\bscreens?\b|\bframes?\b|\bpages\b|\blanding page\b|\b(?:home|shop|product|checkout|wallet) page\b)|(?:构建|创建|绘制|重建|实现).{0,20}(?:\d\d_|屏幕|页面|画板)')
  api_probe=has(hint,r'probe.{0,25}(?:schema|reactions?|api)|(?:api|schema|capability).{0,20}(?:test|probe)|API.{0,12}测试')
  declared_preparation=(prep or has(hint,r'(?:copy|clone).{0,35}(?:assets?|media|components?)|(?:prepare|install|store|define).{0,35}(?:helpers?|utilities|script logic)|辅助函数|准备脚本')) and not explicit_screen_build
  if 'use_figma' in name and api_probe and not explicit_screen_build:
   labs={'O'};why.append('API capability/schema probe, not a user-screen build');sub.append('api_schema_probe')
  elif 'use_figma' in name and declared_preparation:
   labs.discard('C');labs.discard('V');labs.add('P');why.append('explicit resource/system/helper preparation intent')
  if not labs:labs.add('U');why.append('unsupported tool/purpose')
  # Recovery is an orthogonal context, not a fabricated design phase.
  repair=has(hint,r'\bfix\b|repair|retry|rebuild|correct|resolve|patch|修复|重试|重建|纠正|调整')
  recent_error=any(u['error'] for u in calls[max(0,t['index']-3):t['index']])
  if repair:sub.append('declared_revision')
  if recent_error:sub.append('within_three_calls_after_error')
  if 'C' in labs and t['success'] and firstC is None:firstC=t['index']
  # Primary label is only for sequence visualization; multi-label record remains authoritative.
  primary=('V' if t['screenshot'] and 'V' in labs else 'P' if t['screenshot'] else 'C' if 'C' in labs else 'I' if 'I' in labs else 'P' if 'P' in labs else 'V' if 'V' in labs else 'O' if 'O' in labs else 'U')
  ambiguous=len(labs)>1 or 'fallback' in sub or 'visual_other_scope' in sub
  ev=dict(case_id=case,title=r['title'],model=MODELS[r['model']],run_id=r['run_id'],source=source,source_path=source_path,message_index=t['message'],call_index=t['index'],tool_call_id=t['id'],tool=name,mutation=t['write'],description=clean(desc),labels=';'.join(s for s in STAGES if s in labs),primary=primary,subtypes=';'.join(sub),success=t['success'],error=t['error'],review_required=ambiguous,rule_evidence='; '.join(why),final_screen_name=roots.get(node,''),result_message_index=t['result_message'],code_excerpt=clean(code,650),error_excerpt=clean(t['result_text'],220) if t['error'] else '')
  assert primary in labs
  events.append(ev)
 # The final visible delivery statement is a separate work unit, not an artifact-quality verdict.
 final='';final_index=None
 last_result=max((t['result_message'] for t in calls if t['result_message'] is not None),default=-1)
 for mi in range(len(selected_messages)-1,last_result,-1):
  mm=selected_messages[mi]
  if mm.get('role')=='assistant' and not mm.get('tool_calls') and not any(isinstance(b,dict) and b.get('type')=='tool_use' for b in mm.get('content',[]) if isinstance(mm.get('content'),list)):
   tx=texts(mm.get('content',''))
   if tx.strip():final=tx;final_index=mi;break
 handoff=bool(re.search(r'figma\.com/(?:design|file)/',final) and has(final,r'workspace|工作区|交付|page.{0,6}id|页面'))
 if handoff:
  events.append(dict(case_id=case,title=r['title'],model=MODELS[r['model']],run_id=r['run_id'],source=source+'_final_visible_response',source_path=source_path,message_index=final_index,call_index=len(calls),tool_call_id='',tool='final_visible_response',mutation=False,description='Delivery statement with Figma link and workspace context',labels='D',primary='D',subtypes='handoff_statement_only',success=True,error=False,review_required=False,rule_evidence='visible final response; not independent completion verification',final_screen_name='',result_message_index=None,code_excerpt='',error_excerpt=''))
 all_events.extend(events)
 good=[e for e in events if e['success']];compressed=[]
 for e in good:
  if not compressed or compressed[-1]!=e['primary']:compressed.append(e['primary'])
 pc=[i for i,e in enumerate(good) if 'C' in e['labels'].split(';')];pv=[i for i,e in enumerate(good) if 'V' in e['labels'].split(';')]
 postV=[i for i in pv if pc and i>min(pc)]
 pattern='no_observed_product_construction' if not pc else 'no_postconstruction_verification' if not postV else 'interleaved_build_verify' if any(min(pc)<i<max(pc) for i in postV) else 'build_then_verify'
 rr=dict(case_id=case,title=r['title'],model=MODELS[r['model']],run_id=r['run_id'],source=source,source_path=source_path,trajectory_path=str(p),call_count=len(calls),coded_units=len(events),ambiguous_units=sum(e['review_required'] for e in events),error_calls=sum(t['error'] for t in calls),pattern=pattern,compressed_sequence='→'.join(compressed),handoff_statement=handoff,terminal_result_observed=bool(terminal),terminal_is_error=bool(terminal.get('is_error')),terminal_reason=terminal.get('terminal_reason','unobserved'),strict_quality_eligible=(case in STRICT_CASES and VA.get(r['run_id'],{}).get('strict_eligible')=='True'),rubric_score=float(r['score_total']),expert_rank=(B.get(r['run_id'],{}).get('expert_rank',None) if B.get(r['run_id'],{}).get('expert_rank',None) is not None and np.isfinite(B.get(r['run_id'],{}).get('expert_rank',np.nan)) else None))
 for st in STAGES:
  ids=[i for i,e in enumerate(events) if st in e['labels'].split(';')]
  rr[st+'_attempted_units']=len(ids);rr[st+'_successful_units']=sum(events[i]['success'] for i in ids)
  rr[st+'_first_relative_position']=min(ids)/max(len(events)-1,1) if ids else None
 runs.append(rr);bundles.append(dict(meta=rr,events=events))
writecsv('trajectory_inventory.csv',inventory);writecsv('workflow_units.csv',all_events);writecsv('run_workflows.csv',runs)
(OUT/'workflow_evidence.json').write_text(json.dumps(bundles,ensure_ascii=False))
print('Located',len(inventory),'coded',len(runs),'units',len(all_events),flush=True)

# Corpus-level summaries, with run-level prevalence rather than counting tool calls as participants.
trans=C.Counter();pres=C.Counter();co=C.Counter()
for rr,b in zip(runs,bundles):
 seq=rr['compressed_sequence'].split('→');trans.update(set(zip(seq,seq[1:])))
 pres.update({st for e in b['events'] if e['success'] for st in e['labels'].split(';')})
 for e in b['events']:
  if e['success']:co.update(__import__('itertools').combinations(e['labels'].split(';'),2))
prevalence=[dict(stage=s,label=LABELS[s],label_zh=ZH[s],runs_with_successful_evidence=pres[s],runs=len(runs),share=pres[s]/len(runs)) for s in STAGES]
writecsv('stage_prevalence.csv',prevalence)
writecsv('transitions.csv',[dict(source=a,target=b,runs=n,share=n/len(runs)) for (a,b),n in trans.most_common()])
profiles=[]
for m in ORDER:
 rs=[r for r in runs if r['model']==m];z=dict(model=m,runs=len(rs))
 for st in STAGES:
  z[st+'_coverage']=sum(r[st+'_successful_units']>0 for r in rs)/len(rs);z[st+'_mean_units']=float(np.mean([r[st+'_successful_units'] for r in rs]))
 for pat in ['interleaved_build_verify','build_then_verify','no_postconstruction_verification']:z[pat]=sum(r['pattern']==pat for r in rs)
 profiles.append(z)
writecsv('model_workflow_profiles.csv',profiles)
summary={'status':'First-pass rule-assisted multi-label workflow coding; not a fully human-validated taxonomy or saturation claim. Outcomes are not used to assign workflow labels.','target_cells':len(inventory),'found_nonempty_trajectories':sum(r['trajectory_exists'] for r in inventory),'coded_runs':len(runs),'excluded_cells':[r for r in inventory if not r['included']],'coded_units':len(all_events),'ambiguous_units':sum(e['review_required'] for e in all_events),'stage_prevalence':prevalence,'patterns':dict(C.Counter(r['pattern'] for r in runs)),'sources':dict(C.Counter(r['source'] for r in runs)),'strict_quality_runs':sum(r['strict_quality_eligible'] for r in runs),'model_profiles':profiles,'top_transitions':[dict(source=a,target=b,runs=n) for (a,b),n in trans.most_common(20)],'limitations':['A unit is a tool call or final handoff statement; one unit can implement multiple stages.','Descriptions indicate declared purpose; code patterns do not prove all branches executed or goals were met.','Primary-stage sequences are visualization reductions; multi-label evidence is authoritative.','Call order is not wall time or token effort; batched calls may be concurrent.','Post-error operations and declared repairs are orthogonal tags, not evidence of successful defect repair.','Full logs and current trajectory call sets are checked; screenshots captured at reference pages do not automatically count as final artifact verification.','Excluded Chat Bot AI GPT is quarantined; no inference that the indexed updated trace aligns with replacement human judgments.']}
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'pdf.fonttype':42,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':200})
def save(fig,name):
 for ext in ['png','pdf','svg']:fig.savefig(OUT/(name+'.'+ext),bbox_inches='tight',facecolor='white')
 plt.close(fig)
# A transition matrix avoids inventing a universal linear pipeline.
fig,ax=plt.subplots(figsize=(7.5,6));mat=np.array([[trans[a,b]/len(runs) for b in STAGES[:6]] for a in STAGES[:6]])
im=ax.imshow(mat,vmin=0,vmax=1,cmap='Blues')
for i in range(6):
 for j in range(6):ax.text(j,i,f'{mat[i,j]:.0%}',ha='center',va='center',color='white' if mat[i,j]>.55 else '#263648')
ax.set_xticks(range(6),[LABELS[s].split(' / ')[0] for s in STAGES[:6]],rotation=35,ha='right',fontsize=9);ax.set_yticks(range(6),[LABELS[s].split(' / ')[0] for s in STAGES[:6]],fontsize=9);ax.set_xlabel('Next distinct primary stage');ax.set_ylabel('Previous primary stage');ax.set_title('Observed workflow transitions (initial coding)',loc='left',fontweight='bold',pad=14);fig.colorbar(im,ax=ax,label='Share of runs containing transition');save(fig,'fig1_workflow_transitions')
# All-run timelines normalized by observable unit index, not elapsed time.
fig,axes=plt.subplots(1,6,figsize=(15.8,9.5),sharex=True)
from matplotlib.colors import ListedColormap
cmap=ListedColormap([COLORS[s] for s in STAGES]);stage_ix={s:i for i,s in enumerate(STAGES)}
for ax,m in zip(axes,ORDER):
 bs=sorted([b for b in bundles if b['meta']['model']==m],key=lambda b:({'3case':0,'6case':1,'10case':2,'web10':3}[b['meta']['case_id'].split('-case')[0]],b['meta']['case_id']))
 z=np.array([[stage_ix[b['events'][min(int(x*len(b['events'])),len(b['events'])-1)]['primary']] for x in np.linspace(0,.999,120)] for b in bs])
 ax.imshow(z,aspect='auto',cmap=cmap,vmin=-.5,vmax=6.5,interpolation='nearest');ax.set_title(m,fontweight='bold');ax.set_yticks(range(len(bs)),[b['meta']['case_id'].replace('-case-','-') for b in bs],fontsize=6);ax.set_xticks([0,59,119],['0','50','100']);ax.set_xlabel('Relative unit index (%)',fontsize=8)
fig.suptitle('Workflow paths across the trajectory corpus',x=.03,ha='left',fontweight='bold');fig.legend(handles=[Patch(facecolor=COLORS[s],label=LABELS[s]) for s in STAGES],loc='lower center',ncol=4,bbox_to_anchor=(.5,-.025),fontsize=9,frameon=False);fig.tight_layout(rect=[0,.04,1,.97]);save(fig,'fig2_all_run_timelines')
fig,ax=plt.subplots(figsize=(9.3,3.8));z=np.array([[p[s+'_coverage'] for s in STAGES[:6]] for p in profiles]);im=ax.imshow(z,vmin=0,vmax=1,cmap='YlGnBu',aspect='auto')
for i,j in __import__('itertools').product(range(6),range(6)):ax.text(j,i,f'{z[i,j]:.0%}',ha='center',va='center',color='white' if z[i,j]>.65 else '#263648')
ax.set_xticks(range(6),[LABELS[s].split(' / ')[0] for s in STAGES[:6]],rotation=20,ha='right',fontsize=9);ax.set_yticks(range(6),ORDER);ax.set_title('Stage coverage by model (successful observable evidence)',loc='left',fontweight='bold',pad=12);save(fig,'fig3_stage_coverage')
print(json.dumps({'prevalence':prevalence,'patterns':summary['patterns'],'ambiguous':summary['ambiguous_units'],'top_transitions':summary['top_transitions']},ensure_ascii=False,indent=2))
