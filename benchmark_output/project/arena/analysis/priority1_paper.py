"""Reproducible, version-audited Arena / Rubric descriptive analysis.
Run: python arena/analysis/priority1_paper.py. Aggregated paper figures; derived from priority1.py audit. All inputs are local snapshots.
"""
from pathlib import Path
import collections as C
import csv, hashlib, html, itertools, json, math, sqlite3
import numpy as np
from scipy.stats import kendalltau
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'results_eval/priority1_paper'
OUT.mkdir(exist_ok=True)
SEED=20261108
BOOT=10000
EXCLUDED='6case-case-004'
RVS=['participant-88da474b00f1bfba176ba284','participant-c387d1e86a8b70b0f54324a7']
RL={RVS[0]:'R1',RVS[1]:'R2'}
MODELS=['model_claude_opus55_direct','model_de5fc4c9cdb841e8','model_claude_fable51_login','model_glm_53_flash_cc','model_kimi_k3_cc','model_gemini_31_pro_cc']
LABELS=dict(zip(MODELS,['Opus','GPT','Fable','GLM','Kimi','Gemini']))
COLORS=['#4055a8','#1a927c','#bc7a25','#8f66b5','#d06980','#83909a']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':180})

def readcsv(p):
    return list(csv.DictReader(open(p,encoding='utf-8-sig')))
def writecsv(name,rows):
    if not rows: return
    with open(OUT/name,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ci(values,ratio=False):
    a=np.asarray(values,dtype=float)
    rng=np.random.default_rng(SEED)
    ix=rng.integers(0,len(a),(BOOT,len(a)))
    if ratio:
        samples=a[ix].sum(axis=1)
        z=np.divide(samples[:,0],samples[:,1],out=np.full(BOOT,np.nan),where=samples[:,1]!=0)
        point=a[:,0].sum()/a[:,1].sum() if a[:,1].sum() else np.nan
    else:
        z=np.nanmean(a[ix],axis=1);point=float(np.nanmean(a))
    lo,hi=np.nanpercentile(z,[2.5,97.5])
    return {'estimate':float(point),'lo':float(lo),'hi':float(hi),'n_tasks':len(a)}
def savefig(fig,name):
    fig.savefig(OUT/(name+'.png'),bbox_inches='tight')
    fig.savefig(OUT/(name+'.pdf'),bbox_inches='tight')
    plt.close(fig)
def summarize_metrics(rows):
    return {'tau_b':ci([r['tau_b'] for r in rows]),
            'top1_set_hit':ci([r['top1_set_hit'] for r in rows]),
            'top1_unique_hit':ci([r['top1_unique_hit'] for r in rows]),
            'direct_pair_agreement':ci([[r['direct_agree'],r['direct_decisive']] for r in rows],True),
            'direct_agree':sum(r['direct_agree'] for r in rows),
            'direct_decisive':sum(r['direct_decisive'] for r in rows),
            'direct_score_ties':sum(r['direct_score_ties'] for r in rows),
            'top1_set_hits':sum(r['top1_set_hit'] for r in rows),
            'top1_unique_hits':sum(r['top1_unique_hit'] for r in rows),
            'rubric_top_tied_tasks':sum(r['rubric_top_tied'] for r in rows)}

manifest=readcsv(ROOT/'deliver-20261103/manifest.csv')
index=readcsv(ROOT/'results_eval/资产清单-索引.csv')
IX={r['run_id']:r for r in index}
MAN={(r['round']+'-'+r['case_id'],r['model_id']):r for r in manifest}
S=json.load(open(ROOT/'arena/sorting.json'))['sessions']
con=sqlite3.connect('file:'+str(ROOT/'arena/arena.sqlite3')+'?mode=ro',uri=True)
A={(case,m):json.loads(body) for case,m,body in con.execute('select case_id,model_id,body from candidates')}
DBS={id:(json.loads(state),revision) for id,state,revision in con.execute('select id,state,revision from incremental_sort_sessions')}
for session in S:
    for candidate in session['models']:
        assert candidate['candidate_id']==A[session['case_id'],candidate['model_id']]['id']
versions=C.defaultdict(set)
for session in S:
    for candidate in session['models']:
        versions[candidate['candidate_id']].add(candidate['version'])
assert all(len(v)==1 for v in versions.values())
snapshot_diff=[]
for s in S:
    state,rev=DBS[s['session_id']]
    if state['status']!=s['status'] or rev!=s['revision']:
        snapshot_diff.append({'session_id':s['session_id'],'case_id':s['case_id'],'reviewer':RL.get(s['reviewer_id'],s['reviewer_id'][-6:]),'export_status':s['status'],'export_revision':s['revision'],'sqlite_status':state['status'],'sqlite_revision':rev})
writecsv('snapshot_differences.csv',snapshot_diff)

# Validate same candidate run, exact score record, score value and delivered image multiset.
version_rows=[];verified=set();DB={}
for (case,m),a in sorted(A.items()):
    r=MAN[case,m];same=a['run_id']==r['run_id'];score_ok=False;images_ok=False
    if same:
        dbpath=IX[r['run_id']]['round_db']
        if dbpath not in DB: DB[dbpath]=sqlite3.connect('file:'+dbpath+'?mode=ro',uri=True)
        sc=DB[dbpath].execute('select run_id,method,cc_total from scale_scores where id=?',(a['cc_score_id'],)).fetchone()
        score_ok=bool(sc and sc[0]==a['run_id'] and sc[1]=='fixed_v4' and float(sc[2])==float(a['cc_score'])==float(r['score_total']))
        fp=Path(IX[r['run_id']]['frames_dir'])
        images_ok=sorted(sha(p) for p in fp.glob('*.png'))==sorted(im['sha256'] for im in a['images'])
    ok=same and score_ok and images_ok
    if ok: verified.add((case,m))
    version_rows.append({'case_id':case,'title':a['title'],'model':LABELS[m],'arena_run_id':a['run_id'],'index_run_id':r['run_id'],'arena_cc_score':a['cc_score'],'index_score':r['score_total'],'same_run':same,'score_record_verified':score_ok,'image_hashes_verified':images_ok,'strict_eligible':ok and case!=EXCLUDED,'excluded_chat_bot_case':case==EXCLUDED,'arena_url':a['workspace_url'],'index_url':IX[r['run_id']]['copy_figma_url']})
assert len(verified)==169
writecsv('version_audit.csv',version_rows)
strict_cases={case for case,_ in A if case!=EXCLUDED and all((case,m) in verified for m in MODELS)}
complete=[s for s in S if s['status']=='complete' and s['case_id']!=EXCLUDED]
assert len(complete)==42
assert all(len(s['ranking'])==6 and set(s['ranking'])==set(MODELS) for s in complete)
# Use the latest complete session if future snapshots contain repeated rounds.
latest={}
for s in complete:
    k=(s['reviewer_id'],s['case_id'])
    if k not in latest or s['round']>latest[k]['round']:latest[k]=s
complete=list(latest.values())
SS={rv:sorted([s for s in complete if s['reviewer_id']==rv],key=lambda s:s['case_id']) for rv in RVS}
common=sorted(set(s['case_id'] for s in SS[RVS[0]]) & set(s['case_id'] for s in SS[RVS[1]]))

rank_rows=[];rank_stats=[]
for scope in ['all_completed','common_tasks']:
    for rv in RVS:
        ss=[s for s in SS[rv] if scope=='all_completed' or s['case_id'] in common]
        for m in MODELS:
            ranks=[s['ranking'].index(m)+1 for s in ss];v=ci(ranks)
            rank_stats.append({'scope':scope,'reviewer':RL[rv],'model':LABELS[m],'mean_rank':v['estimate'],'ci_lo':v['lo'],'ci_hi':v['hi'],'n_tasks':len(ss),'first_count':ranks.count(1),'last_count':ranks.count(6)})
for s in complete:
    for m in MODELS:rank_rows.append({'case_id':s['case_id'],'title':A[s['case_id'],m]['title'],'reviewer':RL[s['reviewer_id']],'model':LABELS[m],'rank':s['ranking'].index(m)+1,'arena_run_id':A[s['case_id'],m]['run_id'],'score':A[s['case_id'],m]['cc_score'],'strict_case':s['case_id'] in strict_cases})
writecsv('expert_rankings.csv',rank_rows);writecsv('expert_rank_summary.csv',rank_stats)

# Paired reviewer analysis on exactly the same tasks.
inter=[]
for case in common:
    s1=next(s for s in SS[RVS[0]] if s['case_id']==case);s2=next(s for s in SS[RVS[1]] if s['case_id']==case)
    r1=[s1['ranking'].index(m)+1 for m in MODELS];r2=[s2['ranking'].index(m)+1 for m in MODELS]
    agree=sum((r1[i]-r1[j])*(r2[i]-r2[j])>0 for i,j in itertools.combinations(range(6),2))
    inter.append({'case_id':case,'title':A[case,MODELS[0]]['title'],'tau_b':float(kendalltau(r1,r2).statistic),'top1_same':int(s1['ranking'][0]==s2['ranking'][0]),'rank_implied_pair_agree':agree,'rank_implied_pairs':15,'R1_top':LABELS[s1['ranking'][0]],'R2_top':LABELS[s2['ranking'][0]]})
writecsv('inter_reviewer_by_task.csv',inter)
inter_summary={'tau_b':ci([r['tau_b'] for r in inter]),'top1_agreement':ci([r['top1_same'] for r in inter]),'top1_same':sum(r['top1_same'] for r in inter),'rank_implied_pair_agreement':ci([[r['rank_implied_pair_agree'],15] for r in inter],True)}

# Direct evidence: one active, latest decisive vote per unordered model pair per session.
# Incomplete sessions are exported as a secondary, non-ranking evidence set.
vote_audit=[];session_votes={};duplicate_counts=C.Counter();conflict_count=0
for s in S:
    if s['case_id']==EXCLUDED:continue
    active={}
    for v in sorted(s['actual_vote_records'],key=lambda v:(v.get('created_at',''),v['id'])):
        if not v.get('active') or v.get('outcome')!='win' or not v.get('winner'):continue
        k=tuple(sorted((v['a'],v['b'])))
        if k in active:
            duplicate_counts['repeated_active_pair']+=1
            duplicate_counts['conflicting_repeated_pair']+=int(active[k]['winner']!=v['winner'])
        active[k]=v
    session_votes[s['session_id']]=list(active.values())
    for v in active.values():
        winner=v['winner'];loser=v['b'] if winner==v['a'] else v['a'];case=s['case_id']
        delta=float(A[case,winner]['cc_score'])-float(A[case,loser]['cc_score'])
        conflict=False
        if s['status']=='complete':conflict=s['ranking'].index(winner)>s['ranking'].index(loser);conflict_count+=int(conflict)
        vote_audit.append({'case_id':case,'reviewer':RL.get(s['reviewer_id'],s['reviewer_id'][-6:]),'session_status':s['status'],'vote_id':v['id'],'winner':LABELS[winner],'loser':LABELS[loser],'score_margin':delta,'auto_tie':delta==0,'auto_agrees':delta>0,'strict_pair':(case,winner) in verified and (case,loser) in verified,'strict_case':case in strict_cases,'rank_conflict':conflict})
assert conflict_count==0
writecsv('direct_votes.csv',vote_audit)

agreement_rows=[];agreement={}
for scope in ['strict_matched','arena_embedded_sensitivity']:
    agreement[scope]={}
    for rv in RVS:
        ss=[s for s in SS[rv] if scope!='strict_matched' or s['case_id'] in strict_cases]
        rows=[]
        for s in ss:
            case=s['case_id'];scores=[float(A[case,m]['cc_score']) for m in s['ranking']];top=max(scores)
            vs=session_votes[s['session_id']];deltas=[]
            for v in vs:
                loser=v['b'] if v['winner']==v['a'] else v['a']
                deltas.append(float(A[case,v['winner']]['cc_score'])-float(A[case,loser]['cc_score']))
            r={'scope':scope,'reviewer':RL[rv],'case_id':case,'title':A[case,MODELS[0]]['title'],'tau_b':float(kendalltau(range(6,0,-1),scores).statistic),'top1_set_hit':int(scores[0]==top),'top1_unique_hit':int(scores[0]==top and scores.count(top)==1),'rubric_top_tied':int(scores.count(top)>1),'human_top':LABELS[s['ranking'][0]],'rubric_top_set':';'.join(LABELS[s['ranking'][i]] for i,z in enumerate(scores) if z==top),'direct_agree':sum(d>0 for d in deltas),'direct_decisive':sum(d!=0 for d in deltas),'direct_score_ties':sum(d==0 for d in deltas)}
            rows.append(r)
        agreement_rows+=rows;agreement[scope][RL[rv]]=summarize_metrics(rows)
writecsv('rubric_agreement_by_task.csv',agreement_rows)
# SQLite-only completed-session sensitivity to the snapshot discrepancy.
sqlite_sensitivity={}
for rv in RVS:
    rows=[r for r in agreement_rows if r['scope']=='strict_matched' and r['reviewer']==RL[rv] and any(s['case_id']==r['case_id'] and DBS[s['session_id']][0]['status']=='complete' for s in SS[rv])]
    sqlite_sensitivity[RL[rv]]=summarize_metrics(rows)

# Exploratory, post-hoc check: remove the two aggregate extremes.
middle_models=[m for m in MODELS if LABELS[m] not in ['Opus','Gemini']]
middle={}
for rv in RVS:
    ss=[s for s in SS[rv] if s['case_id'] in strict_cases]
    taus=[];counts=[]
    for session in ss:
        order=[m for m in session['ranking'] if m in middle_models]
        scores=[float(A[session['case_id'],m]['cc_score']) for m in order]
        taus.append(float(kendalltau(range(4,0,-1),scores).statistic))
        ds=[]
        for vote in session_votes[session['session_id']]:
            if vote['a'] not in middle_models or vote['b'] not in middle_models:continue
            loser=vote['b'] if vote['winner']==vote['a'] else vote['a']
            ds.append(float(A[session['case_id'],vote['winner']]['cc_score'])-float(A[session['case_id'],loser]['cc_score']))
        counts.append([sum(d>0 for d in ds),sum(d!=0 for d in ds)])
    middle[RL[rv]]={'tau_b':ci(taus),'direct_pair_agreement':ci(counts,True),'direct_agree':sum(c[0] for c in counts),'direct_decisive':sum(c[1] for c in counts)}
paired_rank_preferences={}
for rv in RVS:
    ss=[s for s in SS[rv] if s['case_id'] in common]
    paired_rank_preferences[RL[rv]]=ci([s['ranking'].index(MODELS[1])-s['ranking'].index(MODELS[3]) for s in ss])

summary={'middle_four_posthoc':middle,'paired_GPT_minus_GLM_rank':paired_rank_preferences,'seed':SEED,'bootstrap_replicates':BOOT,'bootstrap_unit':'task, within reviewer; paired shared tasks for human-human; conditional on these reviewers','excluded_case':EXCLUDED,'source':'sorting.json authoritative for session/ranking/vote; SQLite authoritative for candidate identity only','sorting_status':dict(C.Counter(s['status'] for s in S)),'sqlite_status':dict(C.Counter(st['status'] for st,rev in DBS.values())),'snapshot_differences':snapshot_diff,'versions':{'candidates':len(A),'verified_same_run_score_and_images':len(verified),'run_mismatches':sum(not r['same_run'] for r in version_rows),'strict_cases':len(strict_cases),'strict_case_ids':sorted(strict_cases)},'n_completed':{RL[rv]:len(SS[rv]) for rv in RVS},'n_common':len(common),'expert_rank_summary':rank_stats,'inter_reviewer':inter_summary,'rubric_agreement':agreement,'sqlite_completed_sensitivity':sqlite_sensitivity,'duplicate_active_votes':dict(duplicate_counts),'completed_rank_vote_conflicts':conflict_count,'inputs':{str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'arena/sorting.json',ROOT/'arena/arena.sqlite3',ROOT/'deliver-20261103/manifest.csv',ROOT/'results_eval/资产清单-索引.csv']}}
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))


# Average judgments within a task first. Task is the resampling and weighting unit.
def taskmean(rows, key):
    g=C.defaultdict(list)
    for r in rows:g[r['case_id']].append(float(r[key]))
    return {c:float(np.mean(v)) for c,v in g.items()}
def metric_summary(rows):
    result={}
    for key in ['tau_b','top1_set_hit','top1_unique_hit']:
        vals=taskmean(rows,key);result[key]=ci(list(vals.values()))
    rr=[dict(r,rate=r['direct_agree']/r['direct_decisive']) for r in rows if r['direct_decisive']]
    result['direct_pair_agreement']=ci(list(taskmean(rr,'rate').values()))
    result['pooled_direct_counts']={'agree':sum(r['direct_agree'] for r in rows),'decisive':sum(r['direct_decisive'] for r in rows),'auto_ties':sum(r['direct_score_ties'] for r in rows)}
    return result
strict_rows=[r for r in agreement_rows if r['scope']=='strict_matched']
ext_rows=[r for r in agreement_rows if r['scope']=='arena_embedded_sensitivity']
rank_group=C.defaultdict(list)
for s in complete:
    rank_group[s['case_id']].append([s['ranking'].index(m)+1 for m in MODELS])
cases=sorted(rank_group,key=lambda c:({'3case':0,'6case':1,'10case':2,'web10':3}[c.split('-case')[0]],c))
rank_matrix=np.array([np.mean(rank_group[c],axis=0) for c in cases])
rank_summary=[]
for i,m in enumerate(MODELS):
    v=ci(rank_matrix[:,i]);wins=[np.mean([a[i]==1 for a in rank_group[c]]) for c in cases]
    rank_summary.append(dict(model=LABELS[m],mean_rank=v['estimate'],ci_lo=v['lo'],ci_hi=v['hi'],first_choice_share=float(np.mean(wins)),n_tasks=len(cases)))
writecsv('paper_expert_rank_summary.csv',rank_summary)
writecsv('paper_task_ranks.csv',[dict(case_id=c,title=A[c,MODELS[0]]['title'],**{LABELS[m]:float(rank_matrix[j,i]) for i,m in enumerate(MODELS)}) for j,c in enumerate(cases)])
strict_summary=metric_summary(strict_rows);expanded_summary=metric_summary(ext_rows)
shared_strict=set(common)&strict_cases
shared_auto=metric_summary([r for r in strict_rows if r['case_id'] in shared_strict])
shared_inter=[r for r in inter if r['case_id'] in shared_strict]
shared_human={'tau_b':ci([r['tau_b'] for r in shared_inter]),'top1_set_hit':ci([r['top1_same'] for r in shared_inter]),'rank_implied_pair_agreement':ci([r['rank_implied_pair_agree']/15 for r in shared_inter])}
# A post-hoc subset is not evidence of a prespecified hypothesis.
mid_rows=[]
for s in complete:
    if s['case_id'] not in strict_cases:continue
    case=s['case_id'];order=[m for m in s['ranking'] if m in middle_models]
    scores=[float(A[case,m]['cc_score']) for m in order];ds=[]
    for v in session_votes[s['session_id']]:
        if v['a'] not in middle_models or v['b'] not in middle_models:continue
        loser=v['b'] if v['winner']==v['a'] else v['a']
        ds.append(float(A[case,v['winner']]['cc_score'])-float(A[case,loser]['cc_score']))
    mid_rows.append(dict(case_id=case,tau_b=float(kendalltau(range(4,0,-1),scores).statistic),direct_agree=sum(d>0 for d in ds),direct_decisive=sum(d!=0 for d in ds),direct_score_ties=sum(d==0 for d in ds),top1_set_hit=int(scores[0]==max(scores)),top1_unique_hit=int(scores[0]==max(scores) and scores.count(max(scores))==1)))
mid_summary=metric_summary(mid_rows)
paired_drops={}
for key in ['tau_b']:
    a=taskmean(strict_rows,key);b=taskmean(mid_rows,key);paired_drops[key]=ci([a[c]-b[c] for c in a])
# A shared case cluster bootstrap, preserving all judgments for the selected task.
finx='6case-case-005'
sql_rows=[r for r in strict_rows if any(s['case_id']==r['case_id'] and RL[s['reviewer_id']]==r['reviewer'] and DBS[s['session_id']][0]['status']=='complete' for s in complete)]
sql_summary=metric_summary(sql_rows)
comparisons=[]
for i,m in enumerate(MODELS[1:],1):
    v=ci(rank_matrix[:,i]-rank_matrix[:,0]);comparisons.append(dict(comparison=LABELS[m]+' minus Opus',**v))
writecsv('paper_paired_rank_differences.csv',comparisons)

# Export per-task aggregate metrics with no expert identifiers.
bytask=[]
for c in sorted(strict_cases):
    rr=[r for r in strict_rows if r['case_id']==c]
    bytask.append(dict(case_id=c,title=A[c,MODELS[0]]['title'],tau_b=float(np.mean([r['tau_b'] for r in rr])),top1_set_hit=float(np.mean([r['top1_set_hit'] for r in rr])),direct_pair_agreement=float(np.mean([r['direct_agree']/r['direct_decisive'] for r in rr])),direct_votes=sum(r['direct_decisive'] for r in rr),auto_ties=sum(r['direct_score_ties'] for r in rr)))
writecsv('paper_agreement_by_task.csv',bytask)
paper_summary={'estimand':'Equal task weights; within each task, mean of available complete expert judgments. Not a consensus ranking. Bootstrap resamples whole tasks and is conditional on the observed expert panel.','rankings':rank_summary,'strict':strict_summary,'expanded_sensitivity':expanded_summary,'sqlite_complete_sensitivity':sql_summary,'human_human_all_overlap':inter_summary,'matched_overlap':{'n_tasks':len(shared_strict),'human_human':shared_human,'rubric_human':shared_auto},'middle_four_posthoc':mid_summary,'all_minus_middle_paired':paired_drops,'coverage':{'human_tasks':len(cases),'strict_tasks':len(strict_cases),'human_overlap_tasks':len(common),'strict_overlap_tasks':len(shared_strict)},'methods':{'experts':len(RVS),'completed_sessions':len(complete),'per_expert_completed_tasks':summary['n_completed'],'version_verification':'same run + original score record + score value + full screenshot SHA256 multiset','bootstrap':BOOT,'seed':SEED,'excluded_entire_case':EXCLUDED,'source':'sorting.json; SQLite for candidate/score identity; snapshot sensitivity also reported','snapshot_discrepancies':snapshot_diff},'input_sha256':summary['inputs']}
(OUT/'paper_summary.json').write_text(json.dumps(paper_summary,ensure_ascii=False,indent=2))

# Restrained, reusable paper style. No identities or panel-size encodings in plots.
plt.rcParams.update({'font.size':10,'axes.titlesize':11,'axes.labelsize':10,'pdf.fonttype':42,'ps.fonttype':42,'figure.facecolor':'white','axes.facecolor':'white','axes.edgecolor':'#aeb7c2','text.color':'#263648','axes.labelcolor':'#263648','xtick.color':'#526071','ytick.color':'#263648','savefig.dpi':220})
BLUE='#315a8c';TEAL='#178577';ORANGE='#be813b';GRAY='#7d8895'
def savepaper(fig,name):
    fig.savefig(OUT/(name+'.png'),bbox_inches='tight',facecolor='white')
    fig.savefig(OUT/(name+'.pdf'),bbox_inches='tight',facecolor='white')
    fig.savefig(OUT/(name+'.svg'),bbox_inches='tight',facecolor='white')
    plt.close(fig)
def err(ax,v,y,color=BLUE,marker='o',label=None):
    ax.errorbar(v['estimate'],y,xerr=[[max(0,v['estimate']-v['lo'])],[max(0,v['hi']-v['estimate'])]],fmt=marker,color=color,capsize=3,ms=6,lw=1.5,label=label,zorder=3)

fig,ax=plt.subplots(figsize=(6.6,3.8))
order=sorted(range(6),key=lambda i:rank_summary[i]['mean_rank'])
for y,i in enumerate(order):
    r=rank_summary[i];err(ax,dict(estimate=r['mean_rank'],lo=r['ci_lo'],hi=r['ci_hi']),y,COLORS[i]);ax.text(1.02,y,f"{r['mean_rank']:.2f}",va='center',ha='left',fontsize=10,transform=ax.get_yaxis_transform())
ax.set_yticks(range(6),[rank_summary[i]['model'] for i in order]);ax.invert_yaxis();ax.set_xlim(.8,6.3);ax.set_xticks(range(1,7));ax.set_xlabel('Mean expert rank  (lower is better)');ax.set_title('Expert preference across design tasks',loc='left',fontweight='bold',pad=15);ax.grid(axis='x',alpha=.16);ax.text(0,-.25,'28 tasks · equal task weights · 95% task-bootstrap intervals',transform=ax.transAxes,color=GRAY,fontsize=9);savepaper(fig,'fig1_expert_ranking')

fig,ax=plt.subplots(figsize=(13.4,4.3));z=rank_matrix.T
im=ax.imshow(z,vmin=1,vmax=6,cmap='viridis_r',aspect='auto')
for i,j in itertools.product(range(6),range(len(cases))):
    val=z[i,j];ax.text(j,i,f'{val:g}',ha='center',va='center',fontsize=7,color='#17202a' if val<2.5 else 'white')
labels=[A[c,MODELS[0]]['title'].replace('Deniz Arslan 3D Portfolio','3D Portfolio').replace('ABM Developer Portfolio','ABM Portfolio') for c in cases]
ax.set_xticks(range(len(cases)),labels,rotation=55,ha='right',fontsize=8);ax.set_yticks(range(6),[LABELS[m] for m in MODELS]);ax.set_title('Task-level expert preference',loc='left',fontweight='bold',pad=12)
for j in range(1,len(cases)):
    if cases[j].split('-case')[0]!=cases[j-1].split('-case')[0]:ax.axvline(j-.5,color='white',lw=2)
cb=fig.colorbar(im,ax=ax,fraction=.022,pad=.018);cb.set_label('Mean rank');cb.set_ticks(range(1,7));savepaper(fig,'fig2_task_rank_heatmap')

# Put the three main agreement estimands on their own panels; no false common baseline.
fig,axes=plt.subplots(1,3,figsize=(11.5,3.1))
for ax,key,title in zip(axes,['tau_b','top1_set_hit','direct_pair_agreement'],['(a) Ordering agreement','(b) Best-design selection','(c) Direct-vote agreement']):
    v=strict_summary[key];err(ax,v,0,TEAL);ax.text(v['estimate'],.28,f"{v['estimate']:.3f}" if key=='tau_b' else f"{100*v['estimate']:.1f}%",ha='center',fontsize=18,fontweight='bold',color=TEAL)
    ax.text(.5,-.33,f"95% CI [{v['lo']:.3f}, {v['hi']:.3f}]",transform=ax.transAxes,ha='center',fontsize=9,color=GRAY)
    ax.set_ylim(-.35,.65);ax.set_yticks([]);ax.set_xlim(-1,1) if key=='tau_b' else ax.set_xlim(0,1)
    ax.set_title(title,loc='left',pad=13);ax.grid(axis='x',alpha=.16)
    if key=='tau_b':ax.axvline(0,color='#ccd2da',ls='--',lw=1);ax.set_xlabel('Kendall tau-b')
    elif key=='top1_set_hit':ax.set_xlabel('Expert choice in rubric top-score set')
    else:ax.set_xlabel('Agreement on observed decisive votes')
fig.suptitle('Rubric–expert alignment on verified versions',x=.06,ha='left',fontweight='bold',y=1.05);fig.subplots_adjust(wspace=.35,bottom=.26);savepaper(fig,'fig3_rubric_alignment')

fig,axes=plt.subplots(1,2,figsize=(10,3.5))
for ax,key,title in zip(axes,['tau_b','top1_set_hit'],['Ordering agreement','Top-choice agreement']):
    for j,(label,data,color) in enumerate([('Expert–expert',shared_human,GRAY),('Rubric–expert',shared_auto,TEAL)]):
        v=data[key];err(ax,v,j,color);ax.text(1.03,j,f"{v['estimate']:.3f}",va='center',fontsize=10,transform=ax.get_yaxis_transform())
    ax.set_yticks([0,1],['Expert–expert','Rubric–expert']);ax.set_xlim(0,1);ax.set_ylim(1.5,-.6);ax.set_title(title,loc='left');ax.grid(axis='x',alpha=.16);ax.set_xlabel('Kendall tau-b' if key=='tau_b' else 'Agreement rate')
fig.suptitle('Agreement on the same verified task subset',x=.05,ha='left',fontweight='bold',y=1.04);fig.tight_layout(w_pad=3);savepaper(fig,'fig4_shared_task_consistency')

fig,ax=plt.subplots(figsize=(8.6,7.0));rr=sorted(bytask,key=lambda r:r['tau_b'])
for y,r in enumerate(rr):
    color=TEAL if r['case_id'].startswith('web10') else BLUE
    ax.plot([0,r['tau_b']],[y,y],color=color,alpha=.35,lw=2);ax.scatter(r['tau_b'],y,color=color,s=30,zorder=3);ax.text(1.04,y,f"{r['tau_b']:.2f}",va='center',fontsize=8)
ax.set_yticks(range(len(rr)),[r['title'].replace('Deniz Arslan 3D Portfolio','3D Portfolio') for r in rr],fontsize=9);ax.set_xlim(-1,1.16);ax.set_xticks([-1,-.5,0,.5,1]);ax.axvline(0,color='#9ba6b2',lw=.8);ax.axvline(strict_summary['tau_b']['estimate'],color=ORANGE,ls='--',lw=1);ax.invert_yaxis();ax.set_xlabel('Task-level mean Kendall tau-b');ax.set_title('Agreement varies across tasks',loc='left',fontweight='bold',pad=14);ax.scatter([],[],color=BLUE,label='Mobile');ax.scatter([],[],color=TEAL,label='Web');ax.legend(loc='lower left',frameon=False);ax.grid(axis='x',alpha=.1);savepaper(fig,'fig5_task_alignment')

fig,axes=plt.subplots(1,2,figsize=(10.2,3.6))
for ax,key,title in zip(axes,['tau_b','direct_pair_agreement'],['Ordering agreement','Direct-vote agreement']):
    for y,(lab,data,col) in enumerate([('All six models',strict_summary,TEAL),('Middle four models',mid_summary,ORANGE)]):
        v=data[key];err(ax,v,y,col);ax.text(1.03,y,f"{v['estimate']:.3f}",va='center',fontsize=10,transform=ax.get_yaxis_transform())
    ax.set_yticks([0,1],['All six models','Middle four models']);ax.set_ylim(1.5,-.6);ax.set_xlim(-.2 if key=='tau_b' else 0,1);ax.grid(axis='x',alpha=.16);ax.set_title(title,loc='left');ax.set_xlabel('Kendall tau-b' if key=='tau_b' else 'Agreement rate')
fig.suptitle('Exploratory sensitivity to model separation',x=.05,ha='left',fontweight='bold',y=1.04);fig.tight_layout(w_pad=3);savepaper(fig,'fig6_middle_model_sensitivity')
print(json.dumps(paper_summary,ensure_ascii=False,indent=2))

# Report and captions keep study design transparent; figures aggregate judgments.
def htable(headers,rows):
    return '<table><thead><tr>'+''.join('<th>'+html.escape(str(x))+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(str(x))+'</td>' for x in r)+'</tr>' for r in rows)+'</tbody></table>'
def fnum(v,percent=False):
    if percent:return f"{v['estimate']*100:.1f}% [{v['lo']*100:.1f}%, {v['hi']*100:.1f}%]"
    return f"{v['estimate']:.3f} [{v['lo']:.3f}, {v['hi']:.3f}]"
figs=[
('fig1_expert_ranking','专家偏好排名，建议正文','Expert preference over 28 design tasks. Ranks are averaged across available complete judgments within each task and then equally across tasks. Error bars show 95% percentile intervals from 10,000 task-cluster bootstrap samples, conditional on the observed expert panel. Lower is better. These are descriptive aggregate ranks, not a single consensus ordering.'),
('fig2_task_rank_heatmap','逐题排名，建议附录','Task-level mean expert ranks. Each cell aggregates the available complete rankings for the same task; tasks use the same six candidate models. The excluded Chat Bot AI task is omitted. Color indicates relative preference within a task, not an absolute quality score.'),
('fig3_rubric_alignment','自动评价的一致性，建议正文','Rubric–expert alignment on 24 tasks with matched candidate run IDs, original fixed_v4 score records, score values, and delivered screenshot hashes. Metrics are averaged within task before equal-task aggregation. Top-choice set hit permits tied rubric maxima; strict unique-top hit is 70.8%. Direct-vote agreement uses observed active decisive comparisons and excludes automatic-score ties. Error bars are 95% task-cluster bootstrap intervals conditional on the observed expert panel.'),
('fig4_shared_task_consistency','相同题集的一致性参照，建议附录','Expert–expert consistency and rubric–expert alignment on the same 12 verified tasks. Expert–expert top-choice agreement compares selections directly; rubric top-choice set hit allows automatic-score ties (none at the maximum in this subset). Intervals resample tasks. Human agreement is a reference, not a ceiling or ground-truth accuracy; the two comparisons are dependent and do not establish that the rubric is superior to experts.'),
('fig5_task_alignment','各题一致性，建议附录','Task-level mean Kendall tau-b on verified versions. The dashed line marks the equal-task aggregate. Colors distinguish mobile and web tasks descriptively. Per-task values expose heterogeneity but do not provide a causal explanation. FinX uses the later completed sorting export; the database-complete-only sensitivity excludes it.'),
('fig6_middle_model_sensitivity','相近模型区分能力，建议正文或讨论','Post-hoc sensitivity analysis on the same 24 verified tasks. Removing the aggregate extremes (Opus and Gemini) reduces agreement among the remaining GPT, Fable, GLM, and Kimi candidates. Both ranks and automatic ties are recalculated within the subset; direct-vote comparisons are restricted to pairs observed in the original adaptive protocol. Error bars are task-cluster bootstrap intervals. This is an exploratory analysis, not a prespecified confirmatory test.')]
parts=['''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>专家排名与评价一致性 论文分析</title><style>body{font:16px/1.8 system-ui,sans-serif;color:#263648;max-width:1120px;padding:24px;margin:24px auto}h1,h2,h3{line-height:1.35}h2{margin-top:42px}table{border-collapse:collapse;width:100%;font-size:14px}th,td{padding:10px;border-bottom:1px solid #dfe5eb;text-align:left}th{background:#eef3f8}img{width:100%}figure{margin:26px 0}figcaption{font-size:13px;color:#526071}.note{background:#eef6f5;border-left:4px solid #178577;padding:16px}code{background:#f2f4f7}a{color:#315a8c}.draft{border-left:3px solid #be813b;padding:10px 18px;background:#fbf8f3}</style><h1>专家排名与评价一致性 论文分析</h1><p>基于本地评测快照的第一优先级分析，整理于2026年11月8日。图表汇总专家判断，不显示评审身份、逐人曲线或评审人数；方法说明保留真实采样设计。本报告使用任务等权口径，不能与先前按会话或按单个评审报告的数字直接混用。</p>''']
parts.append('<div class="note">主要结果：Opus的汇总平均名次最低，为1.38；严格版本匹配样本中，Rubric与专家判断的τ-b为0.649、首选集合命中率75.0%、实际胜负票一致率79.5%。移除总体排名两端后，τ-b降至0.371，提示对相近质量产物的区分需要单独检验。</div>')
parts.append('<h2>版本核验与样本</h2>')
parts.append(htable(['分析集合','范围','处理'],[['专家独立评价','28题，6模型','按题内可用的完整排序求平均，每题等权；不是42道独立题'],['严格匹配主分析','24题，144个候选','同时核验run、原始score_id/方法/分数、全部交付图SHA256'],['人评重叠题','14题；其中严格匹配12题','评审间一致性只在相同任务、相同候选上计算'],['排除','Chat Bot AI整题','旧GPT不参与任何主结果或敏感性分析；暂不以更新产物替换旧人评'],['扩展敏感性','28题','增加Balance、Budget、Foodieland、ABM；仅使用Arena内嵌分数，不能冒充原始评分记录已核实']]))
parts.append('<p>174个Arena候选中，169个通过同run、原始评分和交付图哈希联合核验。5个版本不一致候选中，Chat Bot AI×GPT连同该题全部排序排除，避免旧候选影响其他模型的相对位置；其余4道题从严格主分析移除。Qwen只有3题且未参加Arena，不参与六模型比较。<a href="version_audit.csv">逐候选版本核验</a>。</p>')
parts.append('<p>快照核对发现FinX在sorting.json中已完成，而SQLite停在较早revision；主分析采用较新的完成排序导出。仅采用SQLite也标为完成的题目时，严格样本为23题，τ-b为'+fnum(sql_summary['tau_b'])+'。这一差异不应隐藏，见<a href="snapshot_differences.csv">快照差异表</a>。</p>')
parts.append('<h2>专家排名</h2>')
parts.append(htable(['模型简称','平均名次','95%任务bootstrap区间'],[[r['model'],f"{r['mean_rank']:.2f}",f"[{r['ci_lo']:.2f}, {r['ci_hi']:.2f}]"] for r in rank_summary]))
parts.append('<p>模型简称对应原始配置：Opus 5.5（三方A）、gpt-6-astra、Fable 5.1、GLM-5.3 Flash、Kimi K3、Gemini 3.5 Flash。模型名必须在投稿前核实是否匿名代号。当前交付包含不同次数补跑，结果描述的是本次交付产物及运行配置，不代表统一预算下的单次成功率。</p>')
parts.append('<h2>一致性统计</h2>')
rows=[]
for label,key,pct in [('Rubric–expert排序','tau_b',False),('Rubric–expert首选集合命中','top1_set_hit',True),('Rubric–expert唯一最高分命中','top1_unique_hit',True),('Rubric–expert直接票一致率','direct_pair_agreement',True)]:rows.append([label,'严格24题',fnum(strict_summary[key],pct)])
rows.extend([['Expert–expert排序','全部14个重叠题',fnum(inter_summary['tau_b'])],['Expert–expert首选一致','全部14个重叠题',fnum(inter_summary['top1_agreement'],True)],['Expert–expert排序','相同严格12题',fnum(shared_human['tau_b'])],['Rubric–expert排序','相同严格12题',fnum(shared_auto['tau_b'])]])
parts.append(htable(['指标','题集','估计与95%区间'],rows))
parts.append('<p>主直接票一致率79.5%是先在每个完整判断中计算，再在题内、题间平均。将所有票直接相加会得到268/332=80.7%，这只是票数加权的次要描述；19张自动同分票单独计数，不伪装为胜负。自适应比较协议并非均匀抽样所有模型对，因此该指标不应外推为任意随机模型对的准确率。</p>')
parts.append('<h2>图表与英文图注</h2><p>正文建议保留图1、图3、图6；图2、图4、图5放附录。使用点与置信区间替代仅柱状均值，避免雷达图。任务级热力图帮助发现异质性，不把42次会话当作42道任务。</p>')
for name,title,cap in figs:
    parts.append(f'<h3>{html.escape(title)}</h3><figure><img src="{name}.png"><figcaption>{html.escape(cap)}</figcaption></figure><p><a href="{name}.pdf">PDF矢量图</a> · <a href="{name}.svg">SVG可编辑图</a> · <a href="{name}.png">PNG</a></p>')
parts.append('<h2>可用于论文的发现</h2>')
parts.append(htable(['发现','证据','可写范围'],[['专家独立评价区分产物质量','Opus平均名次1.38；其余依次为GPT 2.77、Fable 3.39、GLM 3.55、Kimi 4.14、Gemini 5.77','描述本次任务、现有专家面板和交付配置；Fable与GLM的接近均值不能写成已证明显著优劣'],['自动评价捕捉总体相对差异','严格样本τ-b 0.649 [0.559,0.725]；直接票一致率79.5% [74.7%,83.8%]','支持正向一致性；不等于替代专家，也不证明每个Rubric维度有效'],['排序与选优是不同能力','首选集合命中75.0%，唯一最高命中70.8%','必须报告自动并列；75%不是独立的18/24二项试验次数，因为先进行了题内判断平均'],['相近产物仍难细分','中间四模型τ-b 0.371 [0.236,0.501]；全六减中四配对差0.278 [0.163,0.391]；直接票一致率降至66.7%','明确事后探索；子集来自当前数据，不能写为预注册验证或因果机制'],['不同任务的一致性不均匀','FinX -0.067、Fruit Hub 0.298、Octom 0.414','说明需逐题诊断；FinX同时存在快照状态差异，不能直接归因于量表设计']]))
parts.append('<h2>英文结果段落草稿</h2><div class="draft"><p>We report expert preferences independently of rubric-based evaluation. Averaging complete expert rankings within each task and assigning equal weight to tasks, Opus obtains the lowest mean rank (1.38; 95% task-bootstrap CI [1.16, 1.61]) across 28 design tasks. These aggregate ranks summarize the observed judgments rather than asserting a unanimous consensus.</p><p>On 24 tasks whose candidate runs, original rubric score records, and delivered screenshot hashes were verified, rubric scores exhibit positive alignment with expert preferences: mean Kendall’s tau-b is 0.649 (95% CI [0.559, 0.725]). The expert-preferred design belongs to the rubric’s highest-score set in 75.0% of task-weighted judgments; requiring a unique highest score reduces this rate to 70.8%. Agreement on observed decisive pairwise comparisons is 79.5% (95% CI [74.7%, 83.8%]), excluding automatic-score ties. These results support rubric-based evaluation as a complementary scalable measure, without establishing equivalence to expert judgment.</p><p>In an exploratory post-hoc analysis, removing the aggregate ranking extremes reduces ordering agreement among the remaining four models from 0.649 to 0.371, a paired task-level decrease of 0.278 (95% CI [0.163, 0.391]). Direct-vote agreement decreases from 79.5% to 66.7%. Thus, aggregate alignment does not by itself establish reliable discrimination among closer-performing candidates.</p></div>')
parts.append('<h2>方法与必须保留的限制</h2><p>本地完整排序来自2位评审，分别覆盖28题和14题，共42个完整会话、28道不同题；二者重叠14题。不能用汇总图省略这些方法事实，也不能把“专家偏好”改称具有广泛代表性的“专家共识”。图中不编码人数或身份，方法与限制章节如实披露采样范围。</p><ul><li>任务内先平均可用判断，任务间等权；部分任务只有较少判断，因此整体结果仍受覆盖方式影响。置信区间固定现有专家面板，只重采样任务，不能推广为专家总体的不确定性。</li><li>10,000次百分位任务聚类bootstrap，固定随机种子20261108。同题的判断和票一起保留。区间不是同时区间，不进行未经说明的模型两两显著性结论。</li><li>τ-b保留自动分数并列，不人为打破同分；参见<a href="https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kendalltau.html">SciPy Kendall tau-b定义</a>。</li><li>完整排序内每个无序模型对只保留最后一张active胜负票；暂停会话不混入主排序和一致性。保留票与完整排名没有矛盾。排序隐含15对关系不等于15次直接人评。</li><li>人评不是量表校准后的真值；人评间相关不能当作自动评价性能上限。共同子集中的自动–人评相关高于人评间相关，不证明自动评价优于专家。</li><li>专家可能通过Figma账号信息推断模型，不能宣称已验证严格双盲。当前运行预算、补跑选择和模型接入路径不同，结果限定为现有评测设置。</li><li>版本核验以当前本地快照为准，不代表后台已同步或链接当前可访问。扩展4题仅作敏感性分析；Chat Bot AI整题持续排除。</li></ul>')
parts.append('<h2>敏感性分析</h2>')
parts.append(htable(['设置','τ-b','首选集合命中','直接票一致率'],[[label,fnum(v['tau_b']),fnum(v['top1_set_hit'],True),fnum(v['direct_pair_agreement'],True)] for label,v in [('严格匹配24题',strict_summary),('扩展Arena内嵌分数28题',expanded_summary),('SQLite也完成23题',sql_summary),('中间四模型，事后探索24题',mid_summary)]]))
parts.append('<h2>复现与文件</h2><p>运行<code>python arena/analysis/priority1_paper.py</code>。输入快照哈希、抽样口径和数值见<a href="paper_summary.json">paper_summary.json</a>；<a href="paper_expert_rank_summary.csv">排名统计</a>、<a href="paper_agreement_by_task.csv">逐题一致性</a>、<a href="paper_task_ranks.csv">任务级汇总名次</a>。原始审计文件留在分析目录，不作为图版中的评审身份展示。</p></html>')
(OUT/'报告.html').write_text(''.join(parts))
# Shareable figure package includes aggregate data and full methods, not raw panel identifiers.
import zipfile
with zipfile.ZipFile(OUT/'论文图表与结果.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name,_,_ in figs:
        for suffix in ['png','pdf','svg']:z.write(OUT/(name+'.'+suffix),name+'.'+suffix)
    for name in ['报告.html','paper_expert_rank_summary.csv','paper_task_ranks.csv','paper_agreement_by_task.csv','paper_paired_rank_differences.csv']:z.write(OUT/name,name)
print('Report and aggregate figure package written.')
