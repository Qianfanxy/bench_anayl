"""Reproducible, version-audited Arena / Rubric descriptive analysis.
Run: python arena/analysis/priority1.py. All inputs are local snapshots.
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
OUT=ROOT/'results_eval/priority1_analysis'
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

# Figure 1: equal-task comparisons alongside full coverage.
fig,axes=plt.subplots(1,2,figsize=(12,4.6),sharey=True)
for ax,scope,title in zip(axes,['all_completed','common_tasks'],['All completed tasks (unequal coverage)','Same 14 tasks (paired comparison)']):
    for j,rv in enumerate(RVS):
        rs=[next(r for r in rank_stats if r['scope']==scope and r['reviewer']==RL[rv] and r['model']==LABELS[m]) for m in MODELS]
        y=np.arange(6)+(j-.5)*.18;v=np.array([r['mean_rank'] for r in rs]);lo=np.array([r['ci_lo'] for r in rs]);hi=np.array([r['ci_hi'] for r in rs])
        ax.errorbar(v,y,xerr=[v-lo,hi-v],fmt='o' if j==0 else 's',color=['#4055a8','#d27d38'][j],capsize=3,label=f'{RL[rv]} (n={rs[0]["n_tasks"]})')
    ax.set_yticks(range(6),[LABELS[m] for m in MODELS]);ax.set_xlim(.7,6.2);ax.set_xlabel('Mean human rank (lower is better)');ax.set_title(title);ax.grid(axis='x',alpha=.2);ax.legend(fontsize=9)
axes[0].invert_yaxis();fig.suptitle('Expert rankings with 95% task-bootstrap intervals',y=1.03)
savefig(fig,'01_expert_rankings')

# Figure 2: full model-by-task heatmap, common source ordering across reviewers.
cases=sorted({s['case_id'] for s in complete},key=lambda c:({'3case':0,'6case':1,'10case':2,'web10':3}[c.split('-case')[0]],c))
fig,axes=plt.subplots(2,1,figsize=(15,5.6),sharex=True)
for ax,rv in zip(axes,RVS):
    z=np.full((6,len(cases)),np.nan)
    for s in SS[rv]:
        for i,m in enumerate(MODELS):z[i,cases.index(s['case_id'])]=s['ranking'].index(m)+1
    cmap=plt.colormaps['viridis_r'].copy();cmap.set_bad('#eeeeee');ax.imshow(z,vmin=1,vmax=6,cmap=cmap,aspect='auto')
    for i,j in itertools.product(range(6),range(len(cases))):
        if not np.isnan(z[i,j]):ax.text(j,i,str(int(z[i,j])),ha='center',va='center',fontsize=8,color='black' if z[i,j]<=2 else 'white')
    ax.set_yticks(range(6),[LABELS[m] for m in MODELS]);ax.set_ylabel(RL[rv]);ax.set_title(f'{RL[rv]}: {len(SS[rv])} completed tasks',loc='left',fontsize=10)
axes[1].set_xticks(range(len(cases)),[A[c,MODELS[0]]['title'] for c in cases],rotation=65,ha='right',fontsize=8)
fig.suptitle('Per-task human rankings | 1 = best, 6 = worst; gray = uncompleted',y=1.02)
fig.tight_layout();savefig(fig,'02_rank_heatmap')

# Figure 3: paired human-human consistency.
fig,axes=plt.subplots(1,2,figsize=(12,4.4),gridspec_kw={'width_ratios':[1.7,1]})
rs=sorted(inter,key=lambda r:r['tau_b']);ys=np.arange(len(rs));axes[0].barh(ys,[r['tau_b'] for r in rs],color=['#4055a8' if r['top1_same'] else '#c18a46' for r in rs]);axes[0].set_yticks(ys,[r['title'] for r in rs],fontsize=8);axes[0].axvline(inter_summary['tau_b']['estimate'],ls='--',color='#25303d',lw=1);axes[0].set_xlim(-1,1);axes[0].set_xlabel('Kendall tau-b');axes[0].set_title('14 common tasks (orange: different top choice)')
items=[('Mean tau-b',inter_summary['tau_b']),('Top-1 agreement',inter_summary['top1_agreement']),('Rank-implied pair agreement',inter_summary['rank_implied_pair_agreement'])]
for j,(lab,v) in enumerate(items):
    axes[1].errorbar(v['estimate'],j,xerr=[[v['estimate']-v['lo']],[v['hi']-v['estimate']]],fmt='o',color='#4055a8',capsize=4)
    axes[1].text(v['estimate'],j+.18,f'{v["estimate"]:.3f} [{v["lo"]:.3f}, {v["hi"]:.3f}]',ha='center',fontsize=8)
axes[1].set_yticks(range(3),[a for a,b in items]);axes[1].set_xlim(0,1.05);axes[1].set_ylim(-.5,2.6);axes[1].invert_yaxis();axes[1].set_title('95% task-bootstrap intervals');axes[1].grid(axis='x',alpha=.2)
fig.tight_layout();savefig(fig,'03_inter_reviewer')

# Figure 4: strict main result and embedded-score sensitivity.
fig,axes=plt.subplots(1,3,figsize=(14,4.2))
for ax,key,title in zip(axes,['tau_b','top1_set_hit','direct_pair_agreement'],['Task-mean Kendall tau-b','Top-1 in rubric best-score set','Direct-vote agreement (auto ties excluded)']):
    for j,rv in enumerate(RVS):
        for k,scope in enumerate(agreement):
            v=agreement[scope][RL[rv]][key];y=j+(k-.5)*.22
            ax.errorbar(v['estimate'],y,xerr=[[v['estimate']-v['lo']],[v['hi']-v['estimate']]],fmt='o' if k==0 else 's',color=['#4055a8','#c18a46'][k],capsize=4,label=['Strict matched versions','Arena embedded scores'][k] if j==0 else None)
    ax.set_yticks([0,1],['R1','R2']);ax.set_xlim(0,1.03);ax.set_ylim(1.5,-.5);ax.set_title(title,fontsize=10);ax.grid(axis='x',alpha=.2)
axes[0].legend(loc='lower left',fontsize=8);fig.suptitle('Rubric vs. expert judgments | 95% task-cluster bootstrap intervals',y=1.03)
fig.tight_layout();savefig(fig,'04_rubric_agreement')

# Figure 5: per-task agreement exposes variation hidden in global means.
fig,ax=plt.subplots(figsize=(11,4.5))
for j,rv in enumerate(RVS):
    rs=[r for r in agreement_rows if r['scope']=='arena_embedded_sensitivity' and r['reviewer']==RL[rv]]
    for r in rs:
        x=cases.index(r['case_id'])+(j-.5)*.16
        ax.scatter(x,r['tau_b'],marker='o' if j==0 else 's',facecolors=['#4055a8','#c18a46'][j] if r['case_id'] in strict_cases else 'none',edgecolors=['#4055a8','#c18a46'][j],s=45)
    ax.scatter([],[],marker='o' if j==0 else 's',color=['#4055a8','#c18a46'][j],label=RL[rv])
ax.axhline(0,color='#aaaaaa',lw=1);ax.set_ylim(-1,1.08);ax.set_xticks(range(len(cases)),[A[c,MODELS[0]]['title'] for c in cases],rotation=65,ha='right',fontsize=8);ax.set_ylabel('Kendall tau-b');ax.set_title('Agreement varies across tasks | hollow: unresolved version, sensitivity only');ax.legend();fig.tight_layout();savefig(fig,'05_agreement_by_task')

# Figure 6: predeclared main result versus post-hoc middle-model check.
fig,axes=plt.subplots(1,2,figsize=(11,3.8))
for ax,key,title in zip(axes,['tau_b','direct_pair_agreement'],['Kendall tau-b','Direct-vote agreement']):
    for j,rv in enumerate(['R1','R2']):
        for k,v in enumerate([agreement['strict_matched'][rv][key],middle[rv][key]]):
            ax.errorbar(v['estimate'],j+(k-.5)*.22,xerr=[[v['estimate']-v['lo']],[v['hi']-v['estimate']]],fmt='o' if k==0 else 's',capsize=4,color=['#4055a8','#c18a46'][k],label=['All 6 models (main)','Middle 4 models (post-hoc)'][k] if j==0 else None)
    ax.set_yticks([0,1],['R1 (24 tasks)','R2 (12 tasks)']);ax.set_xlim(-.25 if key=='tau_b' else 0,1.03);ax.set_ylim(1.5,-.5);ax.set_title(title);ax.grid(axis='x',alpha=.2)
    if key=='tau_b':ax.axvline(0,color='#999999',ls='--',lw=1)
axes[0].legend(fontsize=8,loc='lower left');fig.suptitle('Exploratory sensitivity: agreement weakens among middle-ranked models',y=1.04);fig.tight_layout();savefig(fig,'06_middle_model_sensitivity')

# A self-contained local report; figures also exported as PNG and PDF.
def fmt(v):return f'{v["estimate"]:.3f} [{v["lo"]:.3f}, {v["hi"]:.3f}]'
def table(headers,rows):return '<table><thead><tr>'+''.join('<th>'+html.escape(str(x))+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(str(x))+'</td>' for x in r)+'</tr>' for r in rows)+'</tbody></table>'
def fig(name,caption):return f'<figure><img src="{name}.png"><figcaption>{caption}</figcaption></figure>'
parts=['''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>专家排名与自动评价一致性分析</title><style>body{font:16px/1.75 system-ui,sans-serif;max-width:1200px;margin:40px auto;padding:0 24px;color:#25303d}h1,h2{line-height:1.3}h2{margin-top:40px}table{border-collapse:collapse;width:100%;font-size:14px}td,th{border:1px solid #dce1e8;padding:9px;text-align:left}th{background:#edf1f7}img{width:100%}figure{margin:24px 0}figcaption,small{color:#667085;font-size:14px}.note{padding:14px;background:#eff5fc;border-left:4px solid #4055a8}code{background:#f0f2f6;padding:2px 5px}</style><h1>专家排名与自动评价一致性分析</h1><p>范围：本地 2026 年 11 月 8 日可用快照。分析任务是专家排名、评审间一致性，以及 Rubric 与专家判断的一致性。Chat Bot AI 整题的人评会话均排除，避免旧 GPT 版本参与或影响排序；不对更新后的 GPT 产物作评价。</p>''']
parts.append('<h2>版本核查与分析范围</h2><p>采用 sorting.json 的排序与投票。SQLite 的 FinX 会话少两张后续投票（导出末票为 2026-11-06 10:16:48 UTC），因此导出有42个完整会话，SQLite有41个；资产清单中“SQLite比导出新”的判断与逐票证据不符。另一处状态差异属于已排除的 Chat Bot AI。候选身份与候选内自动分数取SQLite，再与交付索引、原始评分库逐条校验。</p>')
parts.append(table(['集合','范围','用途'],[['专家评价集','R1 28题；R2 14题；共同14题；6模型','独立呈现专家排序与共同题比较'],['严格版本匹配主分析',f'{len(strict_cases)}个全模型版本均已核实的题目','Rubric主结果；同时核对run、原始score_id/分数与全部参评截图SHA256'],['扩展敏感性分析','额外纳入4道Gemini版本未在本地查到的题目','仅使用Arena候选中记录的cc_score，不冒充已复核原始评分'],['排除','Chat Bot AI整题，含其他模型的该题投票','避免旧GPT参与产生的间接排序影响']]))
parts.append('<p>174个Arena候选中169个通过同run、原始fixed_v4评分记录、数值与截图哈希联合核验。另5个run不同：Chat Bot AI×GPT已排除；Balance、Budget、Foodieland、ABM×Gemini只进入扩展敏感性分析。Qwen仅有3题且不在Arena，故不进入本报告。</p>')
parts.append('<h2>专家排名</h2>'+fig('01_expert_rankings','图1：平均名次及95%按题bootstrap区间。左图题集不同；跨评审比较应看右图共同14题。')+fig('02_rank_heatmap','图2：逐题名次。灰色代表未完成排序，不代表模型失败。'))
parts.append(table(['题集','评审','模型','平均名次 [95% CI]','第一名次数'],[[r['scope'],r['reviewer'],r['model'],f'{r["mean_rank"]:.2f} [{r["ci_lo"]:.2f}, {r["ci_hi"]:.2f}]',f'{r["first_count"]}/{r["n_tasks"]}'] for r in rank_stats]))
parts.append('<h2>评审间一致性</h2>'+fig('03_inter_reviewer','图3：只比较共同14题；排序隐含的15对关系不是15张直接投票。'))
parts.append(table(['指标','估计 [95% CI]'],[['平均Kendall τ-b',fmt(inter_summary['tau_b'])],['Top-1一致率',fmt(inter_summary['top1_agreement'])],['排序隐含两两一致率',fmt(inter_summary['rank_implied_pair_agreement'])]]))
parts.append('<h2>Rubric 与人评一致性</h2>'+fig('04_rubric_agreement','图4：实心圆为严格匹配主结果，方块为包含Arena内嵌分数的敏感性分析。全部区间按题重采样，固定现有评审。')+fig('05_agreement_by_task','图5：各题一致性；空心点仅作敏感性分析。'))
parts.append(table(['集合','评审','题数','τ-b [95% CI]','Top-1集合命中','唯一Top-1命中','直接票一致率 [95% CI]','自动同分票'],[[scope,rv,v['tau_b']['n_tasks'],fmt(v['tau_b']),f'{v["top1_set_hits"]}/{v["tau_b"]["n_tasks"]}',f'{v["top1_unique_hits"]}/{v["tau_b"]["n_tasks"]}',f'{v["direct_agree"]}/{v["direct_decisive"]}; '+fmt(v['direct_pair_agreement']),v['direct_score_ties']] for scope,d in agreement.items() for rv,v in d.items()]))
parts.append('<h2>探索性敏感性分析</h2><p>移除总体两端的Opus与Gemini，仅保留GPT、Fable、GLM、Kimi。此集合由本次结果选择，属于事后探索，不作为预先指定的主检验。</p>')
parts.append(fig('06_middle_model_sensitivity','图6：移除总体两端模型后的事后探索，提示总体一致性不能直接外推到相近产物的细分能力。'))
parts.append(table(['评审','中间4模型τ-b [95% CI]','中间4模型直接票一致率 [95% CI]'],[[rv,fmt(v['tau_b']),f'{v["direct_agree"]}/{v["direct_decisive"]}; '+fmt(v['direct_pair_agreement'])] for rv,v in middle.items()]))
parts.append('<p>快照敏感性：只保留SQLite也标记完成的严格匹配会话时，R1样本降为23题，τ-b为'+fmt(sqlite_sensitivity['R1']['tau_b'])+'；R2不变。这一处理剔除了FinX，不能用来替代较新导出的主结果。</p>')
parts.append('<h2>可写进论文的结论及边界</h2><ol><li>在当前两位专家完成的题目上，Opus的平均名次最低；共同题比较用于核验该结果是否受覆盖范围影响。这里描述的是产物及运行配置组合，不是跨设置的模型固有能力。</li><li>专家之间存在正向但不完全一致的排序关系。人评有独立信息，且现有结果不足以称为“多专家共识”。</li><li>在严格版本匹配样本中，Rubric与专家判断呈正向一致；排序、选优和实际投票三个粒度提供互补证据。</li><li>总体一致性不能保证每题一致；图5及逐题表用于挑选低一致案例。Top-1集合命中允许自动并列最高，必须同时报告唯一最高命中。</li><li>版本不明样本与快照选择的敏感性结果单独报告，避免把版本差异解释为评估器差异。</li></ol><p>不应宣称：自动评价已经替代专家；Rubric比专家更接近真值；一次总体相关系数证明细粒度量表有效；模型间所有差异均统计显著；把两评审42个会话当作42道独立题；把自适应比较票一致率解释为均匀抽样全部模型对的一致率。</p>')
parts.append('<h2>论文结果表述草稿</h2><p>在两位专家共同完成的14道任务上，Opus均取得最低平均名次（分别为1.29与1.21），且各被选为11道任务的首选。专家对整体排序具有正向但不完全一致的判断，平均Kendall τ-b为0.524（95%按题bootstrap区间[0.419, 0.638]），首选一致率为9/14。两位专家对GPT与GLM的相对位置存在差异：共同题平均名次在R1为2.29与3.79，在R2为3.79与2.86。因此排名应按评审呈现，不能将现有数据概括为单一专家共识。</p><p>在产物版本、原始评分记录及截图哈希均一致的样本中，Rubric与R1、R2的逐题平均τ-b分别为0.677[0.583, 0.756]（24题）与0.629[0.521, 0.725]（12题）。排除自动同分后的实际胜负票一致率分别为81.7%[76.6%, 86.2%]与78.8%[71.2%, 85.0%]。专家首选落入自动最高分集合的比例分别为18/24与10/12；若要求唯一最高分，分别为17/24与10/12。这些结果支持自动评价捕捉总体相对质量，但不能证明自动评价可以替代专家判断。</p><p>事后移除总体排名两端的Opus和Gemini后，中间四模型的排序一致性下降到0.434[0.314, 0.560]与0.168[-0.158, 0.466]。该探索性结果提示，总体一致性部分依赖于差异较大的模型区分，对相近质量产物的细分仍需更多专家及任务验证。</p>')
parts.append('<h2>统计口径与限制</h2><ul><li>Bootstrap为10,000次，种子20261108。专家平均名次、逐题τ和Top-1按题重采样；直接票按题聚类重采样分子分母后计算比率。95%区间为百分位区间，非同时置信区间，不用于宣称已通过多重比较显著性检验。</li><li>评审间分析仅共同题；直接票只用完整排序会话的实际active胜负票，一会话内同一模型对保留时间最后的一票。完整排序中未发现保留票与最终排名矛盾。</li><li>未完成会话不用于排名或主一致性估计；其有效投票另存direct_votes.csv供后续检查。存在2次同一会话模型对重复且结果冲突，来自未完成会话，不能把暂停环路直接解释成专家偏好循环。</li><li>报告的是对当前两位评审和当前任务集的条件结果，不外推到专家总体；只有14个共同题，区间不确定性应保留。</li><li>Arena候选固定模型与账号的映射可能影响匿名性；截图、Figma原型及评审访问方式可能影响观察范围。现有记录不足以量化该偏差。</li><li>交付使用补跑后版本，且模型预算与运行路径不同；排名不等同于统一预算下单次成功率或模型纯能力。</li></ul>')
parts.append('<h2>复现与数据文件</h2><p>运行 <code>python arena/analysis/priority1.py</code>。输入快照SHA256、全部统计和区间见 <a href="summary.json">summary.json</a>；版本核验见 <a href="version_audit.csv">version_audit.csv</a>；排序明细见 <a href="expert_rankings.csv">expert_rankings.csv</a>；逐题一致性见 <a href="rubric_agreement_by_task.csv">rubric_agreement_by_task.csv</a>；原始有效票见 <a href="direct_votes.csv">direct_votes.csv</a>。所有图另有同名PDF可用于论文排版。</p></html>')
(OUT/'报告.html').write_text(''.join(parts))
print(json.dumps({'verified':len(verified),'strict_cases':len(strict_cases),'n_completed':summary['n_completed'],'inter':inter_summary,'agreement':agreement,'sqlite_sensitivity':sqlite_sensitivity,'duplicates':dict(duplicate_counts)},ensure_ascii=False,indent=2))
