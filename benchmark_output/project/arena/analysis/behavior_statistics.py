"""Exploratory behavior associations; run after behavior_analysis.py. No causal claims."""
from pathlib import Path
import collections as C,csv,json,math,html,zipfile
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'results_eval/behavior_analysis'
pd.set_option('display.max_columns',30)
f=pd.read_csv(OUT/'features.csv');main=f[f.strict_case].copy().reset_index(drop=True)
FEATURES=[('screen_coverage','Final-screen screenshot coverage','最终屏幕截图覆盖率',False),('recheck_coverage','Screenshot–edit–same-screen recheck','截图—修改—同屏复查覆盖率',False),('script_error_rate','Script error rate','脚本报错率',False),('audit_read_calls','Read-only structural audits','只读结构/文本验收调用数',True),('instance_write_share','Instance / clone script share','实例化/克隆脚本占比',False),('prewrite_inspection_calls','Inspections before first write','首次写入前检查调用数',True),('screenshot_calls','Successful screenshot calls','成功截图调用数',True),('minutes','Run duration','运行时长',True)]
def design(d,effort=False,model=False):
 z=[np.ones((len(d),1)),pd.get_dummies(d.case_id,drop_first=True,dtype=float).values]
 if model:z.append(pd.get_dummies(d.model,drop_first=True,dtype=float).values)
 if effort:z.append(np.log1p(d.total_calls.values)[:,None])
 return np.column_stack(z)
def fit(d,key,trans,outcome,adjust='full'):
 dd=d[np.isfinite(d[key])].copy();v=dd[key].to_numpy(float);v=np.log1p(v) if trans else v
 if np.std(v)<1e-10:return None
 x=(v-v.mean())/v.std();y=dd[outcome].to_numpy(float)
 if outcome=='expert_rank':y=7-y
 Z=design(dd,effort=adjust=='full',model=adjust in ['full','model']);X=np.column_stack([Z,x]);rank=np.linalg.matrix_rank(X)
 if rank<np.linalg.matrix_rank(Z)+1:return None
 inv=np.linalg.pinv(X.T@X);beta=inv@X.T@y;u=y-X@beta;clusters=dd.case_id.to_numpy();group=np.unique(clusters);meat=np.zeros((X.shape[1],X.shape[1]))
 for g in group:
  mask=clusters==g;sc=X[mask].T@u[mask];meat+=np.outer(sc,sc)
 correction=len(group)/(len(group)-1)*(len(dd)-1)/(len(dd)-rank)
 cov=correction*inv@meat@inv;se=math.sqrt(max(cov[-1,-1],0));t=beta[-1]/se if se else np.nan;p=2*stats.t.sf(abs(t),len(group)-1);crit=stats.t.ppf(.975,len(group)-1)
 # Fraction of feature variance remaining after controls (identifiability diagnostic).
 xr=x-Z@np.linalg.lstsq(Z,x,rcond=None)[0]
 return dict(feature=key,outcome=outcome,adjustment=adjust,beta=float(beta[-1]),se=se,lo=float(beta[-1]-crit*se),hi=float(beta[-1]+crit*se),p=float(p),n=len(dd),tasks=len(group),residual_feature_variance=float(np.mean(xr*xr)),feature_mean=float(v.mean()),feature_sd=float(v.std()),rank=int(rank))
rows=[]
for k,en,zh,tr in FEATURES:
 for out in ['expert_rank','rubric_score']:
  for adj in ['task','model','full']:
   rr=fit(main,k,tr,out,adj)
   if rr:rr.update(label=en,label_zh=zh,log1p=tr);rows.append(rr)
# Benjamini–Hochberg across all 16 main fully adjusted exploratory associations.
full=[r for r in rows if r['adjustment']=='full']
primary=[r for r in rows if r['adjustment']=='model']
for family in [primary,full]:
 ix=np.argsort([r['p'] for r in family]);prev=1.
 for j in range(len(ix)-1,-1,-1):
  i=int(ix[j]);prev=min(prev,family[i]['p']*len(ix)/(j+1));family[i]['q']=prev
for r in rows:r.setdefault('q',None)
pd.DataFrame(rows).to_csv(OUT/'associations.csv',index=False,encoding='utf-8-sig')
# Robustness: model+task only, exclude infrastructure-blocked runs, and leave-one-model-out.
sens=[]
for k,en,zh,tr in FEATURES:
 for out in ['expert_rank','rubric_score']:
  for label,dd in [('no_infrastructure_block',main[~main.infra_blocked]),('no_observed_terminal_error',main[~main.terminal_is_error])]+[('without_'+m,main[main.model!=m]) for m in sorted(main.model.unique())]:
   rr=fit(dd,k,tr,out,'model')
   if rr:rr['sample']=label;sens.append(rr)
pd.DataFrame(sens).to_csv(OUT/'sensitivity.csv',index=False,encoding='utf-8-sig')
# Within-model cross-task correlations are descriptive, with no task difficulty control.
corr=[]
for model,d in main.groupby('model'):
 for k,en,zh,tr in FEATURES:
  for out in ['expert_rank','rubric_score']:
   v=d[k].values;y=7-d[out].values if out=='expert_rank' else d[out].values
   if np.std(v)>1e-10:corr.append(dict(model=model,feature=k,outcome=out,rho=float(stats.spearmanr(v,y).statistic),n=len(d)))
pd.DataFrame(corr).to_csv(OUT/'within_model_correlations.csv',index=False,encoding='utf-8-sig')
# Error recovery is conditioned on having errors; assess separately to avoid inventing 100% recovery for error-free runs.
rec=[]
for out in ['expert_rank','rubric_score']:
 rr=fit(main[main.script_errors>0],'recovery_next3_rate',False,out,'full')
 if rr:rec.append(rr)
pd.DataFrame(rec).to_csv(OUT/'conditional_error_recovery.csv',index=False,encoding='utf-8-sig')
model_summary=main.groupby('model').agg(runs=('run_id','count'),screen_coverage=('screen_coverage','mean'),recheck_coverage=('recheck_coverage','mean'),error_rate=('script_error_rate','mean'),screenshots=('screenshot_calls','mean'),calls=('total_calls','mean'),minutes=('minutes','median'))
model_summary.to_csv(OUT/'model_behavior_summary.csv',encoding='utf-8-sig')
summary={'scope':{'extracted_runs':len(f),'matched_runs':len(main),'matched_tasks':main.case_id.nunique(),'models':6,'excluded_entire_case':'6case-case-004','rubric_all_local_secondary_runs':len(f)},'estimator':'Primary: one behavior at a time, standardized over matched sample (log1p for counts/duration); task and model fixed effects. Effort sensitivity additionally conditions on log1p(total tool calls), which may be a mediator and changes the estimand; CR1 task-cluster sandwich SE, t intervals with task clusters minus one df. Expert outcome is 7-minus-mean-expert-rank (higher better).','multiplicity':'BH correction across 16 task+model adjusted primary exploratory behavior/outcome associations; effort sensitivity corrected in a separate 16-test family. Conditional recovery and sensitivities are separate exploratory checks.','features':FEATURES,'task_model_adjusted':primary,'effort_adjusted_sensitivity':full,'conditional_error_recovery':rec,'sensitivity_caveat':'Leave-one-model-out and no-infrastructure runs are descriptive robustness checks, not independent replications. Fixed effects remove mean differences, not all difficulty or capability confounding.','source_quality':json.load(open(OUT/'extraction_summary.json')),'raw_behavior_definitions':{'screen_coverage':'Fraction of required final-named screens with at least one successful screenshot targeting a final root frame ID. Whole-page/composite screenshots do not count; old/replaced IDs do not count. Denominator from full delivered requirement text, not truncated artifact brief.','recheck_coverage':'Fraction of required final screens with a successful screenshot, an intervening successful mutation script after receiving its result, and a later successful screenshot of the same final frame ID. The mutation may affect another screen; this is an observable sequence, not proof of visual repair.','script_error_rate':'Observed error results / use_figma calls. Detect explicit is_error/success=false and error prefixes; not all logical failures or rendering problems.','audit_read_calls':'Successful use_figma script without detected mutation, containing a node traversal and text/reaction/name/count inspection. Does not prove correctness or full acceptance.','instance_write_share':'Fraction of successful mutation scripts syntactically containing createInstance or clone. Code presence is not executed instance count, supplied-media reuse, or semantic fidelity.','prewrite_inspection_calls':'Metadata or non-mutating use_figma calls before the first mutation script. Does not prove understanding of requirements.','recovery_next3_rate':'Among script errors, fraction followed by a successful mutation within the next three tool calls. The successful operation may be unrelated to the error.'}}
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print(pd.DataFrame(full)[['feature','outcome','beta','lo','hi','p','q','residual_feature_variance']].to_string(index=False),flush=True)

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'pdf.fonttype':42,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'text.color':'#263648','axes.labelcolor':'#263648','savefig.dpi':220})
BLUE='#315a8c';TEAL='#178577';GRAY='#a4adb8';ORANGE='#be813b'
def save(fig,name):
 for ext in ['png','pdf','svg']:fig.savefig(OUT/(name+'.'+ext),bbox_inches='tight',facecolor='white')
 plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(12,5),sharey=True)
for ax,out,title in zip(axes,['expert_rank','rubric_score'],['Expert preference','Rubric score']):
 for i,(k,en,zh,tr) in enumerate(FEATURES):
  r=next(r for r in primary if r['feature']==k and r['outcome']==out);col=(TEAL if out=='expert_rank' else BLUE) if r['q']<.05 else GRAY
  ax.errorbar(r['beta'],i,xerr=[[r['beta']-r['lo']],[r['hi']-r['beta']]],fmt='o',color=col,capsize=3)
 ax.axvline(0,color='#7d8895',ls='--',lw=1);ax.set_yticks(range(len(FEATURES)),[v[1] for v in FEATURES]);ax.set_title(title,loc='left',fontweight='bold');ax.grid(axis='x',alpha=.15);ax.set_xlabel('Higher preference (rank points) per 1 SD' if out=='expert_rank' else 'Rubric points per 1 SD')
axes[0].invert_yaxis();fig.suptitle('Observable behaviors after task and model adjustment',x=.025,ha='left',fontweight='bold',y=1.02);save(fig,'fig1_adjusted_associations')

fig,axes=plt.subplots(1,2,figsize=(12,4.9),sharey=True)
for ax,out in zip(axes,['expert_rank','rubric_score']):
 for i,(k,en,zh,tr) in enumerate(FEATURES):
  for j,(adj,col) in enumerate([('task',ORANGE),('model',TEAL)]):
   r=next(r for r in rows if r['feature']==k and r['outcome']==out and r['adjustment']==adj)
   ax.errorbar(r['beta'],i+(j-.5)*.16,xerr=[[r['beta']-r['lo']],[r['hi']-r['beta']]],fmt='o',color=col,capsize=2,ms=4,label=('Task-adjusted only' if adj=='task' else '+ Model adjustment') if i==0 else None)
 ax.set_yticks(range(len(FEATURES)),[v[1] for v in FEATURES]);ax.axvline(0,color=GRAY,ls='--',lw=1);ax.grid(axis='x',alpha=.12);ax.set_title('Expert preference' if out=='expert_rank' else 'Rubric score',loc='left');ax.set_xlabel('Outcome change per 1 SD')
axes[0].invert_yaxis();axes[1].legend(fontsize=8,loc='lower right');fig.suptitle('Between-model patterns do not establish within-model benefits',x=.025,ha='left',fontweight='bold',y=1.02);save(fig,'fig2_confounding_check')

fig,axes=plt.subplots(1,3,figsize=(11,3.6),sharey=True)
ms=['Opus','GPT','Fable','GLM','Kimi','Gemini']
for ax,k,title in zip(axes,['screen_coverage','recheck_coverage','error_rate'],['Final-screen screenshot coverage','Screenshot–edit–recheck coverage','Script error rate']):
 vals=[model_summary.loc[m,k] for m in ms];ax.barh(range(6),vals,color=TEAL if k!='error_rate' else ORANGE,alpha=.8)
 for j,x in enumerate(vals):ax.text(x+.02,j,f'{x:.0%}',va='center',fontsize=9)
 ax.set_yticks(range(6),ms);ax.set_xlim(0,1.18);ax.set_xticks([0,.5,1],['0','50%','100%']);ax.set_title(title,fontsize=10,loc='left');ax.grid(axis='x',alpha=.1)
axes[0].invert_yaxis();fig.suptitle('Execution profiles across matched tasks (descriptive)',x=.025,ha='left',fontweight='bold',y=1.04);save(fig,'fig3_model_profiles')
