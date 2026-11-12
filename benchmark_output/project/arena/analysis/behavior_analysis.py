"""Observable process/outcome associations. Local snapshots only; no model reasoning is interpreted.
Run MPLCONFIGDIR=/tmp/benchmark-mpl python arena/analysis/behavior_analysis.py
"""
from pathlib import Path
import csv,json,re,collections as C,hashlib,math,html,zipfile
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'results_eval/behavior_analysis';OUT.mkdir(exist_ok=True)
R=list(csv.DictReader(open(ROOT/'results_eval/资产清单-索引.csv',encoding='utf-8-sig')))
AUD=list(csv.DictReader(open(ROOT/'results_eval/priority1_paper/version_audit.csv',encoding='utf-8-sig')))
STRICT={r['case_id'] for r in AUD if r['strict_eligible']=='True'}
STRICT={c for c in STRICT if sum(r['case_id']==c and r['strict_eligible']=='True' for r in AUD)==6}
MODEL={'Fable 5.1':'Fable','Opus 5.5（三方A）':'Opus','gpt-6-astra':'GPT','Gemini 3.5 Flash':'Gemini','GLM-5.3 Flash':'GLM','Kimi K3':'Kimi'}
S=json.load(open(ROOT/'arena/sorting.json'))['sessions']
A=C.defaultdict(list)
for s in S:
 if s['status']=='complete' and s['case_id']!='6case-case-004':
  for m in s['models']:A[m['candidate_id']].append(s['ranking'].index(m['model_id'])+1)
BYRUN={r['arena_run_id']:r for r in AUD if r['strict_eligible']=='True'}
import sqlite3
con=sqlite3.connect('file:'+str(ROOT/'arena/arena.sqlite3')+'?mode=ro',uri=True)
RUNRANK={run:float(np.mean(A[id])) for id,run in con.execute('select id,run_id from candidates') if A[id]}
def writecsv(name,rows):
 if not rows:return
 with open(OUT/name,'w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def texts(x):
 if isinstance(x,str):return x
 if isinstance(x,list):return '\n'.join(texts(v) for v in x if not isinstance(v,dict) or v.get('type') not in ['image','image_url','thinking','reasoning'])
 if isinstance(x,dict):return texts(x.get('text',x.get('content','')))
 return ''
def args(x):
 if isinstance(x,str):
  try:return json.loads(x)
  except Exception:return {}
 return x if isinstance(x,dict) else {}
ERR=re.compile(r'(?:^|\n)(?:Error:|TypeError:|ReferenceError:|SyntaxError:|Input validation error:)|tool.*(?:quota|limit).*reached|rate.limit|exceeded.*quota|MCP.*limit',re.I)
MUT=re.compile(r'figma\.create(?:Frame|Text|Component|Rectangle|Vector|Variable|Style|NodeFromSvg)|\.createInstance\s*\(|\.(?:appendChild|insertChild|remove|resize|setReactionsAsync|setBoundVariable)\s*\(|\.(?:characters|fills|strokes|reactions|layoutMode|x|y|name|fontSize|cornerRadius|clipsContent|overflowDirection)\s*=(?!=)')

def normalize(messages):
 calls=[];seen=set();results={}
 for ix,m in enumerate(messages):
  for t in m.get('tool_calls',[]) or []:
   f=t.get('function',{});id=t.get('id')
   if id and id not in seen:calls.append(dict(id=id,name=f.get('name',''),args=args(f.get('arguments',{})),message=ix));seen.add(id)
  blocks=m.get('content',[])
  if isinstance(blocks,list):
   for b in blocks:
    if not isinstance(b,dict):continue
    if b.get('type')=='tool_use':
     id=b.get('id')
     if id and id not in seen:calls.append(dict(id=id,name=b.get('name',''),args=args(b.get('input',{})),message=ix));seen.add(id)
    elif b.get('type')=='tool_result':results[b.get('tool_use_id')]=(texts(b.get('content','')),b.get('is_error',False),ix)
  if m.get('role')=='tool':results[m.get('tool_call_id')]=(texts(m.get('content','')),m.get('success') is False,ix)
 for i,t in enumerate(calls):
  result=results.get(t['id']);t['index']=i;t['result_observed']=result is not None
  t['error']=bool(result and (result[1] or ERR.search(result[0])))
  t['success']=bool(result and not t['error']);t['result_message']=result[2] if result else None
  t['code']=str(t['args'].get('code',t['args'].get('script','')))
  t['write']=bool('use_figma' in t['name'] and MUT.search(t['code']))
  t['screenshot']='get_screenshot' in t['name'];t['node']=str(t['args'].get('nodeId',t['args'].get('node_id',''))).replace('-',':')
 return calls

def log_messages(path):
 messages=[];bad=0;uuids=set();terminal={}
 with open(path,errors='replace') as f:
  for line in f:
   if not line.startswith('{'):continue
   try:d=json.loads(line)
   except Exception:bad+=1;continue
   if d.get('type')=='result':terminal={k:d.get(k) for k in ['is_error','stop_reason','terminal_reason','safety_stops']}
   if d.get('type') not in ['assistant','user'] or not isinstance(d.get('message'),dict):continue
   uid=d.get('uuid')
   if uid and uid in uuids:continue
   if uid:uuids.add(uid)
   messages.append(d['message'])
 return messages,bad,terminal

features=[];events=[];quality=[]
for r in R:
 if r['model'] not in MODEL or (r['round']=='6case' and r['case_id']=='case-004'):continue
 case=r['round']+'-'+r['case_id'];d=json.load(open(r['trajectory_path']));tcalls=normalize(d.get('messages',[]));source='trajectory';calls=tcalls;bad=0;logn=0;terminal={}
 if r['run_log'] and Path(r['run_log']).exists():
  msgs,bad,terminal=log_messages(r['run_log']);lcalls=normalize(msgs);logn=len(lcalls)
  # Prefer the full harness stream if its call ID coverage contains the trajectory's IDs.
  if len(lcalls)>=len(tcalls) and {t['id'] for t in tcalls}<={t['id'] for t in lcalls}:calls=lcalls;source='run.log'
  elif len(lcalls)>len(tcalls):
   calls=lcalls;source='run.log_non_nested';
 artifact=json.load(open(Path(r['run_dir'])/'benchmark-artifact.json'))
 screens=[n for n in artifact.get('workspace',{}).get('children',[]) if n['type']=='FRAME' and re.match(r'^\d{2}[_ ·-]',n['name'])]
 requirement_file=next((ROOT/'deliver-20261103/requirements'/r['round']).glob(r['case_id']+'-*.md'))
 expected=sorted(set(re.findall(r'^\s*(\d{2}_[A-Za-z][A-Za-z0-9_]+)\s*$',requirement_file.read_text(),re.M)))
 if not expected:expected=sorted({n['name'] for n in screens})
 screen_map={n['id']:n['name'] for n in screens};screen_names=set(expected)
 shot=[t for t in calls if t['screenshot'] and t['success']]
 verified={screen_map[t['node']] for t in shot if t['node'] in screen_map and screen_map[t['node']] in screen_names}
 repeat=set();firstshot={}
 for t in shot:
  node=t['node']
  if node in firstshot and any(u['write'] and u['success'] and firstshot[node]['result_message'] is not None and u['message']>firstshot[node]['result_message'] and u['result_message'] is not None and u['result_message']<t['message'] for u in calls):
   if node in screen_map and screen_map[node] in screen_names:repeat.add(screen_map[node])
  firstshot[node]=t
 script=[t for t in calls if 'use_figma' in t['name']];writes=[t for t in calls if t['write'] and t['success']]
 er=[t for t in script if t['error']];recovery=sum(any(u['write'] and u['success'] for u in calls[t['index']+1:t['index']+4]) for t in er)
 instance=[t for t in writes if re.search(r'\.createInstance\s*\(|\.clone\s*\(',t['code'])]
 audit=[t for t in script if t['success'] and not t['write'] and re.search(r'findAll|findOne|\.children',t['code']) and re.search(r'characters|reactions|missing|duplicate|\.length|\.name',t['code'])]
 firstwrite=next((t['index'] for t in calls if t['write']),len(calls));inspect=sum(t['index']<firstwrite and ('get_metadata' in t['name'] or ('use_figma' in t['name'] and not t['write'])) for t in calls)
 f=dict(case_id=case,title=r['title'],model=MODEL[r['model']],run_id=r['run_id'],rubric_score=float(r['score_total']),expert_rank=RUNRANK.get(r['run_id'],float('nan')),strict_case=case in STRICT,source=source,terminal_result_observed=bool(terminal),terminal_is_error=bool(terminal.get('is_error')),terminal_reason=terminal.get('terminal_reason','unobserved'),terminal_stop_reason=terminal.get('stop_reason','unobserved'),trajectory_agent_role=d.get('metadata',{}).get('agent_role','unspecified'),total_calls=len(calls),trajectory_calls=len(tcalls),log_calls=logn,missing_results=sum(not t['result_observed'] for t in calls),script_calls=len(script),successful_writes=len(writes),screenshot_calls=len(shot),expected_screens=len(expected),final_screen_count=len(screens),duplicate_screens=len(screens)-len({n['name'] for n in screens}),screen_coverage=len(verified)/max(len(expected),1),recheck_coverage=len(repeat)/max(len(expected),1),script_error_rate=len(er)/max(len(script),1),script_errors=len(er),recovery_next3_rate=recovery/len(er) if er else float('nan'),instance_write_share=len(instance)/max(len(writes),1),audit_read_calls=len(audit),prewrite_inspection_calls=inspect,minutes=float(r['minutes']),is_rerun=r['is_rerun']=='True',infra_blocked=json.load(open(Path(r['run_dir'])/'benchmark-delivery.json')).get('infrastructure_blocked',False),last_script_error=bool(script and script[-1]['error']))
 features.append(f)
 for t in calls:
  events.append(dict(run_id=r['run_id'],case_id=case,model=MODEL[r['model']],source=source,call_index=t['index'],message_index=t['message'],tool=t['name'],tool_call_id=t['id'],result_observed=t['result_observed'],success=t['success'],error=t['error'],write=t['write'],screenshot=t['screenshot'],node_id=t['node'],final_screen_name=screen_map.get(t['node'],'')))
 quality.append(dict(run_id=r['run_id'],model=MODEL[r['model']],source=source,trajectory_calls=len(tcalls),log_calls=logn,selected_calls=len(calls),missing_results=f['missing_results'],trajectory_agent_role=f['trajectory_agent_role'],malformed_log_lines=bad))
writecsv('features.csv',features);writecsv('tool_event_audit.csv',events);writecsv('source_quality.csv',quality)
print('FEATURES',len(features),'strict',sum(f['strict_case'] for f in features),'sources',dict(C.Counter(f['source'] for f in features)),flush=True)
(OUT/'extraction_summary.json').write_text(json.dumps({'n_runs':len(features),'n_events':len(events),'sources':dict(C.Counter(f['source'] for f in features)),'role_counts':dict(C.Counter(f['trajectory_agent_role'] for f in features))},indent=2))
