import json,csv,collections as C,itertools as I,statistics as st
from scipy.stats import kendalltau,spearmanr
B='/mnt/afs_design/huangxinyue/projects/benchmark-design/'
S=json.load(open(B+'arena/sorting.json'))['sessions']
M=list(csv.DictReader(open(B+'deliver-20261103/manifest.csv',encoding='utf-8-sig')))
print('manifest rounds',C.Counter(r['round'] for r in M))
NM={r['model_id']:r['model_name'] for r in M}
rub={(f"{r['round']}-{r['case_id']}",r['model_id']):float(r['score_total']) for r in M}
title={f"{r['round']}-{r['case_id']}":r['title'] for r in M}
comp=[s for s in S if s['status']=='complete']
R1='participant-88da474b00f1bfba176ba284'; R2='participant-c387d1e86a8b70b0f54324a7'
def rk(s): return {m:i+1 for i,m in enumerate(s['ranking'])}
models=sorted({m['model_id'] for m in S[0]['models']}); print('extra in manifest:',{(NM[k],k) for k in NM if k not in models})
for rv in (R1,R2):
  ss=[s for s in comp if s['reviewer_id']==rv]
  print('\nreviewer',rv[-6:],len(ss),'cases')
  for m in sorted(models,key=lambda m:st.mean(rk(s)[m] for s in ss)):
    rs=[rk(s)[m] for s in ss]; print(f"  {NM[m]:22s} mean rank {st.mean(rs):.2f}  #1 x{rs.count(1)}  #6 x{rs.count(6)}")
# inter-reviewer
by=C.defaultdict(dict)
for s in comp: by[s['case_id']][s['reviewer_id']]=s
taus=[]
for c,d in sorted(by.items()):
  if R1 in d and R2 in d:
    a=rk(d[R1]);b=rk(d[R2]); t=kendalltau([a[m] for m in models],[b[m] for m in models])[0]; taus.append(t)
    print(f"  {c:16s} {title.get(c,'?'):18s} tau={t:+.2f} top1 same={d[R1]['ranking'][0]==d[R2]['ranking'][0]}")
print('inter-reviewer mean tau',round(st.mean(taus),3),'n',len(taus))
# rubric vs arena
print('\nmissing rubric keys',[ (s['case_id'],m) for s in comp for m in models if (s['case_id'],m) not in rub][:5])
for rv in (R1,R2):
  ts=[];top=0;n=0
  for s in comp:
    if s['reviewer_id']!=rv: continue
    a=rk(s); x=[-a[m] for m in models]; y=[rub[(s['case_id'],m)] for m in models]
    ts.append(kendalltau(x,y)[0]); n+=1
    best=max(y); top+= y[models.index(s['ranking'][0])]==best
  print(rv[-6:],'rubric-vs-arena per-case mean tau',round(st.mean(ts),3),'rubric top1 == arena top1',top,'/',n)
# model level
for rv in (R1,):
  ss=[s for s in comp if s['reviewer_id']==rv]; cs={s['case_id'] for s in ss}
  ar={m:st.mean(rk(s)[m] for s in ss) for m in models}
  ru={m:st.mean(rub[(c,m)] for c in cs) for m in models}
  print('model-level (R1 cases)',[(NM[m],round(ar[m],2),round(ru[m],1)) for m in sorted(models,key=ar.get)])
  print('spearman model-level',spearmanr([-ar[m] for m in models],[ru[m] for m in models]))
