"""Case study audit for the five lowest per-task tau values in the strict analysis.
Uses the frozen source_evidence.json exported from candidate-specific score IDs.
Reproduces figures/tables/report; raw trajectory paths retained as evidence anchors.
"""
from pathlib import Path
import collections as C
import csv,hashlib,html,itertools,json,os,shutil,sqlite3,zipfile
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'results_eval/disagreement_analysis';OUT.mkdir(exist_ok=True)
D=json.load(open(OUT/'source_evidence.json'))
S=json.load(open(ROOT/'arena/sorting.json'))['sessions']
CDB=sqlite3.connect('file:'+str(ROOT/'arena/arena.sqlite3')+'?mode=ro',uri=True);CDB.row_factory=sqlite3.Row
MODELS=['model_claude_opus55_direct','model_de5fc4c9cdb841e8','model_claude_fable51_login','model_glm_53_flash_cc','model_kimi_k3_cc','model_gemini_31_pro_cc']
ML=dict(zip(MODELS,['Opus','GPT','Fable','GLM','Kimi','Gemini']))
RV={'participant-88da474b00f1bfba176ba284':'R1','participant-c387d1e86a8b70b0f54324a7':'R2'}
A='model_de5fc4c9cdb841e8';F='model_claude_fable51_login';O='model_claude_opus55_direct';K='model_kimi_k3_cc';G='model_glm_53_flash_cc';E='model_gemini_31_pro_cc'
Q=json.load(open(ROOT/'benchmarks/rubrics/fixed-v4.json'))['questions'];MAX={q['key']:q.get('max',2) for q in Q};assert sum(MAX.values())==53

def writecsv(name,rows):
 if not rows:return
 with open(OUT/name,'w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def h(x):return html.escape(str(x))
def table(headers,rows):return '<table><thead><tr>'+''.join('<th>'+h(x)+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+h(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table>'
def img(name,caption):return f'<figure><a href="{name}.png"><img src="{name}.png"></a><figcaption>{h(caption)}</figcaption></figure>'
def txt(p):return Path(p).read_text()
def getcode(msg):
 out=[]
 for tc in msg.get('tool_calls',[]):
  f=tc.get('function',{});a=f.get('arguments',{});a=json.loads(a) if isinstance(a,str) else a
  if 'code' in a:out.append(a['code'])
 return '\n'.join(out)

audited={(r['case_id'],r['model']) for r in csv.DictReader(open(ROOT/'results_eval/priority1_analysis/version_audit.csv',encoding='utf-8-sig')) if r['strict_eligible']=='True'}
selection=list(csv.DictReader(open(ROOT/'results_eval/priority1_analysis/rubric_agreement_by_task.csv',encoding='utf-8-sig')))
mins={}
for r in selection:
 if r['scope']!='strict_matched':continue
 if r['case_id'] not in mins or float(r['tau_b'])<float(mins[r['case_id']]['tau_b']):mins[r['case_id']]=r
selected=sorted(mins.values(),key=lambda r:float(r['tau_b']))[:5]
assert set(r['case_id'] for r in selected)==set(D)
writecsv('case_selection.csv',[{'case_id':r['case_id'],'title':r['title'],'reviewer_at_minimum':r['reviewer'],'minimum_tau_b':r['tau_b'],'selection_rule':'lowest minimum strict-matched task-reviewer tau; five unique tasks, post-hoc'} for r in selected])

# Verify score provenance again and export all 22 item scores + judge rationale.
items=[];traces={};images=[];version=[]
for ca,mods in D.items():
 for m,z in mods.items():
  assert (ca,ML[m]) in audited
  a=z['candidate'];ix=z['index'];assert a['run_id']==ix['run_id']==z['manifest']['run_id']
  db=sqlite3.connect('file:'+ix['round_db']+'?mode=ro',uri=True);db.row_factory=sqlite3.Row;rec=db.execute('select * from scale_scores where id=?',(z['score_id'],)).fetchone()
  assert rec['run_id']==a['run_id'] and rec['method']=='fixed_v4' and float(rec['cc_total'])==a['cc_score']==sum(z['scores'].values())
  for q in Q:
   key=q['key'];items.append({'case_id':ca,'title':a['title'],'model':ML[m],'run_id':a['run_id'],'score_id':z['score_id'],'item':key,'dimension':q['dimension'],'item_max':MAX[key],'score':z['scores'][key],'judge_rationale':z['evidence'][key]})
  traces[ca,m]=json.load(open(ix['trajectory_path']))['messages']
  for file in Path(ix['frames_dir']).glob('*.png'):
   digest=hashlib.sha256(file.read_bytes()).hexdigest();assert digest in {im['sha256'] for im in a['images']}
   im=Image.open(file);images.append({'case_id':ca,'model':ML[m],'file':str(file),'width':im.width,'height':im.height,'sha256':digest})
  version.append({'case_id':ca,'model':ML[m],'run_id':a['run_id'],'score_id':z['score_id'],'score':a['cc_score'],'url':a['workspace_url'],'trajectory_path':ix['trajectory_path'],'trajectory_sha256':hashlib.sha256(Path(ix['trajectory_path']).read_bytes()).hexdigest()})
writecsv('rubric_items.csv',items);writecsv('versions.csv',version);writecsv('image_dimensions.csv',images)

requirements=[]
for ca,mods in D.items():
    r=next(iter(mods.values()))['manifest'];rn=r['round'];cid=r['case_id']
    files=list((ROOT/'deliver-20261103/requirements'/rn).glob(cid+'-*.md'))
    assert len(files)==1
    raw=files[0].read_text()
    (OUT/(ca+'-requirement.txt')).write_text(raw)
    for lineno,line in enumerate(raw.splitlines(),1):
        if (ca=='3case-case-002' and any(t in line for t in ['Gold 30%','1,000,240','0182128'])) or (ca=='6case-case-005' and any(t in line for t in ['No 1 design','09_Exchange_Stock','• Keypad:','• Side:','• Actions: filter'])):
            requirements.append({'case_id':ca,'source_file':str(files[0].relative_to(ROOT)),'line':lineno,'text':line})
writecsv('requirement_anchors.csv',requirements)

# Actual direct pair evidence; incomplete sessions remain labelled and never replace rankings.
direct=[];screen_rows=[];notes=[]
for session in S:
 ca=session['case_id']
 if ca not in D:continue
 for vote in session['actual_vote_records']:
  if not vote.get('active') or vote['outcome']!='win':continue
  win=vote['winner'];lose=vote['b'] if win==vote['a'] else vote['a'];pair=vote['pair_id']
  direct.append({'case_id':ca,'reviewer':RV.get(session['reviewer_id'],session['reviewer_id'][-6:]),'session_status':session['status'],'pair_id':pair,'winner':ML[win],'loser':ML[lose],'winner_score':D[ca][win]['candidate']['cc_score'],'loser_score':D[ca][lose]['candidate']['cc_score']})
  req=CDB.execute('select left_model_id,right_model_id from incremental_sort_requests where pair_id=?',(pair,)).fetchone()
  if not req:continue
  pr=CDB.execute('select body from pair_screen_plans where pair_id=? and reviewer_id=?',(pair,session['reviewer_id'])).fetchone();slots={x['id']:x for x in json.loads(pr[0])} if pr else {}
  for row in CDB.execute('select * from pair_screen_votes where pair_id=? and reviewer_id=?',(pair,session['reviewer_id'])):
   model=req[0] if row['choice']=='A' else req[1] if row['choice']=='B' else None
   screen_rows.append({'case_id':ca,'reviewer':RV.get(session['reviewer_id'],session['reviewer_id'][-6:]),'pair_id':pair,'left_model':ML[req[0]],'right_model':ML[req[1]],'screen':slots.get(row['slot_id'],{}).get('name',row['slot_id']),'choice':row['choice'],'selected_model':ML[model] if model else row['choice'],'comment':row['comment']})
 for tab in ['ballots','pair_screen_votes']:
  for row in CDB.execute(f"select t.* from {tab} t join pairs p on p.id=t.pair_id where p.case_id=? and t.reviewer_id=? and trim(t.comment)!=''",(ca,session['reviewer_id'])):
   notes.append({'case_id':ca,'reviewer':RV.get(session['reviewer_id'],session['reviewer_id'][-6:]),'session_status':session['status'],'source_table':tab,'pair_id':row['pair_id'],'comment':row['comment']})
writecsv('direct_pair_evidence.csv',direct);writecsv('screen_vote_evidence.csv',screen_rows);writecsv('expert_comments.csv',notes)

# Tool execution evidence only: no model private reasoning exported.
anchors=[]
def anchor(ca,m,i,kind,excerpt):
 assert i<len(traces[ca,m]);message=traces[ca,m][i]
 anchors.append({'case_id':ca,'model':ML[m],'run_id':D[ca][m]['candidate']['run_id'],'trajectory_path':D[ca][m]['index']['trajectory_path'],'message_index_zero_based':i,'role':message['role'],'evidence_type':kind,'excerpt':excerpt})
for ca,m,i,term,span in [
 ('6case-case-005',E,34,'const f9 =',6000),
 ('6case-case-005',A,26,"screen('09_Exchange_Stock'",3500),
 ('3case-case-002',F,29,'function createAccount',3400),
 ('3case-case-002',A,18,'Enter a valid email',500),
 ('6case-case-003',A,24,"['Go to cart'",450),
 ('6case-case-003',A,36,"txt(10,'Go to cart'",220),
 ('web10-case-006',F,98,"const ph2=",550),
]:
 code=getcode(traces[ca,m][i]);pos=code.find(term);assert pos>=0;anchor(ca,m,i,'tool_call_code',code[pos:pos+span])
for ca,m,i,term,span in [('6case-case-003',A,67,'7:150',680),('6case-case-003',K,62,'09 done',100),('6case-case-003',K,80,'11 done',100),('6case-case-006',G,156,'10:24: NULL',300),('6case-case-006',G,158,'hits: 0',40)]:
 content=traces[ca,m][i]['content'];pos=content.find(term);assert pos>=0;anchor(ca,m,i,'tool_result',content[pos:pos+span])
(OUT/'trace_anchors.json').write_text(json.dumps(anchors,ensure_ascii=False,indent=2))

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':180})
# Human ranks and automatic scores, with both reviewers kept separate.
fig,axes=plt.subplots(1,5,figsize=(17,4.5),sharey=True)
ranktable=[]
for ax,r in zip(axes,selected):
 ca=r['case_id'];sessions=[s for s in S if s['case_id']==ca and s['status']=='complete']
 vals=[D[ca][m]['candidate']['cc_score'] for m in MODELS]
 # Average ranks preserve automatic score ties.
 from scipy.stats import rankdata
 auto=rankdata(-np.array(vals),method='average')
 for j,s in enumerate(sessions):
  hr=[s['ranking'].index(m)+1 for m in MODELS]
  ax.plot(hr,range(6),'o',color=['#3654a4','#cf873f'][j],label=RV[s['reviewer_id']])
  for k,m in enumerate(MODELS):ranktable.append({'case_id':ca,'title':r['title'],'reviewer':RV[s['reviewer_id']],'model':ML[m],'human_rank':hr[k],'rubric_score':vals[k],'rubric_tied_rank':auto[k]})
 ax.plot(auto,range(6),'x',color='#333333',label='Rubric rank')
 ax.set_title(r['title']+'\nmin tau='+f"{float(r['tau_b']):.3f}",fontsize=10);ax.set_xlim(.5,6.5);ax.set_xticks([1,2,3,4,5,6]);ax.grid(axis='x',alpha=.2);ax.set_xlabel('Rank (1 = best)')
axes[0].set_yticks(range(6),[ML[m] for m in MODELS]);axes[0].invert_yaxis();from matplotlib.lines import Line2D
axes[-1].legend(handles=[Line2D([],[],marker='o',ls='',color='#3654a4',label='R1'),Line2D([],[],marker='o',ls='',color='#cf873f',label='R2'),Line2D([],[],marker='x',ls='',color='#333333',label='Rubric rank')],fontsize=8,loc='lower right');fig.suptitle('Five lowest-agreement tasks from the strict version-matched analysis',y=1.03);fig.tight_layout()
for ext in ['png','pdf']:fig.savefig(OUT/('01_case_rank_reversals.'+ext),bbox_inches='tight')
plt.close(fig);writecsv('case_rankings.csv',ranktable)
# Item-group decomposition of actually observed human-preferred pairs.
pairs=[('6case-case-005',A,O),('3case-case-002',F,A),('6case-case-003',K,A),('6case-case-006',F,K),('web10-case-006',F,A)]
dims=['A','B','G','D','E','F'];dimnames=['UX /8','Information /15','Handoff /4','Layout /12','Consistency /4','Visual /10']
z=[];decomp=[]
for ca,w,l in pairs:
 assert any(r['case_id']==ca and r['session_status']=='complete' and r['winner']==ML[w] and r['loser']==ML[l] for r in direct)
 ds=[sum(v for q,v in D[ca][w]['scores'].items() if q.startswith(k))-sum(v for q,v in D[ca][l]['scores'].items() if q.startswith(k)) for k in dims];z.append(ds)
 decomp.append({'case_id':ca,'human_preferred':ML[w],'other':ML[l],'total_margin':sum(ds),**dict(zip(dims,ds))})
fig,ax=plt.subplots(figsize=(10,4.4));im=ax.imshow(z,vmin=-5,vmax=5,cmap='RdBu',aspect='auto')
for i,j in itertools.product(range(5),range(6)):ax.text(j,i,f'{z[i][j]:+d}',ha='center',va='center')
ax.set_xticks(range(6),dimnames);ax.set_yticks(range(5),[next(iter(D[ca].values()))['candidate']['title']+'\n'+ML[w]+' > '+ML[l] for ca,w,l in pairs]);ax.set_title('Rubric points: human-preferred artifact minus alternative\nAll five pairs were directly voted; group weights are unequal');fig.colorbar(im,ax=ax,label='Point difference');fig.tight_layout()
for ext in ['png','pdf']:fig.savefig(OUT/('02_rubric_decomposition.'+ext),bbox_inches='tight')
plt.close(fig);writecsv('rubric_decomposition.csv',decomp)
# Comparison images copied from exact-hash matched delivered PNGs. Entire frames fit the tile.
configs=[('03_finx_screens','6case-case-005',[A,O,E],['07','09'],350,770),('04_paradise_screens','3case-case-002',[F,A,K],['04','03-create-account-error'],350,770),('05_stylish_screens','6case-case-003',[K,A,F],['09','11'],350,770),('06_octom_screens','web10-case-006',[F,O,A],['01','02'],620,490)]
for name,ca,models,nums,w,hh in configs:
 canvas=Image.new('RGB',(3*w,len(nums)*(hh+65)),'#e7e9ef');draw=ImageDraw.Draw(canvas)
 for row,num in enumerate(nums):
  for col,m in enumerate(models):
   files=sorted(Path(D[ca][m]['index']['frames_dir']).glob('*.png'));p=next(p for p in files if p.stem.split('_',1)[1].startswith(num));im=Image.open(p).convert('RGB');size=im.size;im.thumbnail((w-12,hh));x=col*w+6;y=row*(hh+65)
   canvas.paste(im,(x,y+59));draw.text((x,y+4),ML[m],fill='#141c28');draw.text((x,y+20),p.stem,fill='#141c28');draw.text((x,y+36),f'{size[0]} x {size[1]} pixels',fill='#141c28')
 canvas.save(OUT/(name+'.png'))

# Evidence-based narratives. Interpretations explicitly separated from observed behavior.
CASE_TEXT={
'6case-case-005':{
 'heading':'FinX：总体排序接近反向，且能定位到判分目标与任务约束的冲突',
 'observed':'R1排序为GPT > Fable > Opus > GLM > Kimi > Gemini；自动分数却为Opus44、Gemini40、GPT39、Kimi36、Fable35、GLM33。GPT胜Opus是直接投票；逐屏为GPT 9胜、1平、0负。Fable胜Opus也是直接投票，但逐屏4胜4负2平，不能把最终偏好说成逐屏多数自动决定。当前快照没有文字备注，因此不知道评审偏好的具体理由。',
 'rubric':'GPT比Opus少5分，差额分解为A −1、B 0、G −2、D −1、E 0、F −1。G1/G2占2分差，显示自动总分还评价图层交付性；实际屏幕投票不能证明专家评价了图层。更关键的是，GPT的A3=0，理由为09没有确认按钮；Gemini的A3=2，但同一09屏实际连数字键盘、Buy/Sell、换向控件都缺失。这里不是简单的“专家忽略功能”，而是分项锚点没有一致地覆盖相同屏幕缺陷。',
 'trace':'GPT的轨迹与交付图有键盘、Buy/Sell、FROM/TO等内容；Gemini messages[34]仅构建两张股票卡及底部导航，[35]返回创建成功。简报明确要求09含键盘与Buy/Sell，却没有列出提交按钮；还指定“Buy、AAPL→SPOT”和“No 1 design for E-bank…”文案，这些又出现在GPT的负面评分理由中。存档判分提示未包含156.50或该文案原文。',
 'conclusion':'强证据：需求覆盖遗漏与通用可用性扣分没有被一致处理。可讨论：任务符合性与产品合理性是不同评价对象，固定简报自身的设计选择可能被转化为模型扣分。不能认定缺提交按钮的可用性批评一定错误，也不能把这解释为全部5分差或R1偏好GPT的原因。',
 'figure':'03_finx_screens'},
'3case-case-002':{
 'heading':'Paradise Invest：两位专家重复选择Fable，分项却奖励GPT的布局与可用性',
 'observed':'两位专家都将Fable排第2；GPT分别第3、第5。两人均有Fable胜GPT的直接票。对应逐屏分别为Fable 10胜1平0负，以及7胜3平1负；这不是单一评审的一次偶然选择。没有文字备注，不应声称专家亲述“更精致”。',
 'rubric':'Fable40，GPT45。A为6比8，D为8比11；F1至F5逐项完全相同，F5均1/2。分数差来自可用性和布局，而不是自动评分给Fable更高美学分但权重不足。截图可见Fable确有错误提示离邮箱较远、姓名密码清空等局部问题，故不能直接认定Rubric错误。',
 'trace':'Fable轨迹messages[29]创建Empty/Filled/Error三态，后续多轮修复平台壳与点击热点；交付图仍保留局部对齐和错误态问题。GPT也确实建立三态及原型。另有任务约束污染：B3理由以Gold30%低于Silver60%、历史金额大于当前资产、两银行同掩码账号为问题；但这些数字在需求原文163、165、175行被明确指定。两模型B3均1，因此这一问题不能解释Fable/GPT的5分反转。',
 'conclusion':'强证据：两位专家的重复偏好未被当前细粒度总分复现；视觉综合项在这一对产物上没有区分度。待验证：专家重视的整体风格、空间节奏或观感未被现有分档充分捕捉。不能从没有备注的投票推断专家心理。',
 'figure':'04_paradise_screens'},
'6case-case-003':{
 'heading':'Stylish：专家备注与轨迹共同确认“可见范围不等”，但不是全部分歧的解释',
 'observed':'R2把Kimi排第2、GPT第5，直接选Kimi胜GPT；对应逐屏Kimi7胜、GPT2胜、6平。R2在Home明确写“有内容但是因为画板大小限制有点显示不全”；比较Fable时又写“a又看不到了”和“左边又是没什么内容的”。R1却把GPT排第4、Kimi第5，所以该具体偏好不代表评审共识。',
 'rubric':'Kimi31、GPT36。GPT的A3=0，判官同样指出Product Detail首屏看不到购买按钮；Kimi A3=1。然而GPT在D1/D3/D4和G2等项目累计得分更高，抵消了主操作定位问题。可见分歧并非判官完全没发现裁切，而是总分的补偿结构保留了GPT优势。',
 'trace':'GPT messages[24]把Go to cart、Buy Now放在滚动内容y=1020；[36]有对应原型链接；[67]回读Home和Product Detail含684px高的VERTICAL滚动容器。Kimi工具结果[62]显示Home画板高2116，[80]显示Product Detail高1468；Fable导出Home高2500。三者交付截图分别是视口首屏与完整长画板，不是等价覆盖。只能确认内容在图层与代码里，未实测原型滚动是否可靠。',
 'conclusion':'强证据：设计呈现方式和截图覆盖范围会进入专家判断与自动评分；应区分“未生成”和“在首屏之外”。强证据：总分可以用其他分项抵消已发现的关键可见性缺陷。待验证：统一视口/长页证据后，模型偏好是否改变；尚未做反事实重评。',
 'figure':'05_stylish_screens'},
'6case-case-006':{
 'heading':'Fruit Hub：自动同分压缩了中间排序，重复交付又阻碍了评审',
 'observed':'R1排序为Opus > GPT > Fable > GLM > Kimi > Gemini；GPT、Kimi、Gemini自动同为44分，Fable42、GLM41。R1直接选Fable胜Kimi，逐屏Fable8胜1平1负；这属于分数反转。另一个评审R2停在paused-unable，备注“本来只有10个画板？a组现在有20个…不知道怎么比”，不得将该未完成会话当完整排序。',
 'rubric':'GLM的图单与G0都明确看到20屏；G0说明“20屏均可读取，主流程完整”，G1仅1/2并指出成对同名。自动评价不是没看到重复，而是允许这一稿继续评分并得到41分。截图可继续工作，与人能否进行无歧义的配对比较，是不同条件。自动44分的三模型在专家完整排序中分别位于2、5、6，说明相同总分不表示专家判断相近。',
 'trace':'GLM messages[156]查询原10节点均NULL，[158]全局搜索hits:0；随后重建。最终快照与评分图单同时保留旧新两套，每套01–10。该轨迹与最终状态不一致，支持工具状态异常/重建残留的描述，不能确定底层原因，也不能直接归为模型无故重复生成。Fable实际只有10个正式画板，导出顺序异常；“有两套内容”的另一条备注尚未得到完整双套屏幕证据支持。',
 'conclusion':'强证据：可评分性与可比较性不同；需要单独记录重复版本和无法判断，而不是把它们混入纯视觉质量。强证据：整数分项求和可能压缩中间产物差异。不能断言去重后R2会完成排序、也不能断言重复造成R1的具体名次。',
 'figure':None},
'web10-case-006':{
 'heading':'Octom：专家选择Fable，判官也认可其精致度，却在其他维度累计扣分',
 'observed':'R1排序Fable > GPT > Opus > GLM > Kimi > Gemini。Fable43、GPT48、Opus50。Fable胜GPT有直接票，逐屏Fable4胜、GPT1胜、1平；Fable相对Opus的优势这里只能由最终排序推导，没有这两者的直接票。没有文字备注。',
 'rubric':'Fable和Opus的F5均2/2，判官分别评价“精致的SaaS视觉”“整体协调精致”。Fable对Opus的7分差来自A −1、B −1、D −3、E −1、F −1，G相同。扣分包括Timeline今天位置矛盾、全部星期标S、状态同为Active却用不同颜色、Files右栏空白。不是判官没有发现Fable的视觉优点，而是该优点在顶档2分内无法进一步增加。',
 'trace':'Fable messages[98]增加Phase progress卡，写入3 tasks/62%等自定数据；[99]工具确认成功。这说明丰富完成度可能伴随额外数据和更多可被批评的细节。截图也能看到Fable较完整的页头与阶段汇总，但没有专家理由能证明这些导致其胜出。',
 'conclusion':'强证据：综合视觉顶档饱和与其他维度累计扣分共存，能够产生整体偏好反转。待验证：专家是否更重视整体完成感/构图，而对局部语义一致性容忍度更高；需回访或针对性重新标注。不能据单例建议按这些偏好重新拟合权重。',
 'figure':'06_octom_screens'}
}
(OUT/'case_findings.json').write_text(json.dumps(CASE_TEXT,ensure_ascii=False,indent=2))

parts=['''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>五个最大分歧案例的证据分析</title><style>body{font:16px/1.8 system-ui,sans-serif;max-width:1200px;margin:40px auto;padding:0 24px;color:#25303d}h1,h2{line-height:1.4}h2{margin-top:42px}table{border-collapse:collapse;width:100%;font-size:13px}td,th{border:1px solid #dce1e8;padding:8px;text-align:left;vertical-align:top}th{background:#edf1f7}figure{margin:25px 0}img{max-width:100%}figcaption,small{font-size:13px;color:#667085}a{color:#235ac1}.note{padding:12px;background:#edf3fb}details{border:1px solid #dce1e8;padding:10px;margin:12px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px}code{background:#eff1f5}</style><h1>五个最大分歧案例的证据分析</h1><p>选取严格版本匹配分析中，每题最低的“评审×题目”τ-b排序前五个不同任务。属于按结果选择的事后案例研究，不估计问题的总体发生率，也不作因果推断。Chat Bot AI整题继续排除。</p><p class="note">证据分三层：①实际投票、文字备注与可核验产物；②自动评分自己的理由和分数差分解；③对偏好原因的解释假设。FinX、Paradise Invest和Octom没有文字备注，不能把视觉分析冒充专家亲述。</p>''']
parts.append(table(['任务','最低τ-b','评审','完整排序数','文字备注'],[[r['title'],f"{float(r['tau_b']):.3f}",r['reviewer'],sum(s['case_id']==r['case_id'] and s['status']=='complete' for s in S),len([n for n in notes if n['case_id']==r['case_id']])] for r in selected]))
parts.append(img('01_case_rank_reversals','图1：人评名次与自动评分名次，自动同分采用平均名次。R1/R2分别呈现，未合并成共识。'))
parts.append(img('02_rubric_decomposition','图2：实际直接投票中，人更偏好的产物相对另一产物的自动分数差。分组满分不同，总分53；这只是原始加和分解，不是重新拟合权重。'))
for r in selected:
 ca=r['case_id'];t=CASE_TEXT[ca];parts.append('<h2>'+h(t['heading'])+'</h2>')
 for label,key in [('实际分歧与专家证据','observed'),('Rubric分项','rubric'),('轨迹与需求核对','trace'),('论文发现与边界','conclusion')]:parts.append('<p><strong>'+label+'：</strong>'+h(t[key])+'</p>')
 if t['figure']:parts.append(img(t['figure'],'交付截图来自同run且哈希匹配的版本；每张图按整幅适配缩略图，原始像素尺寸见标签。长图与视口图的缩略比例不同，不能据此比较字号大小。'))
 parts.append('<details><summary>该题六模型的22项评分与判官理由</summary>')
 for m in MODELS:
  z=D[ca][m];parts.append('<h3>'+h(ML[m])+' · '+str(z['candidate']['cc_score'])+'分</h3><p><a href="'+h(z['candidate']['workspace_url'])+'">打开该版本Figma交付</a></p>')
  parts.append(table(['项','分数','判官理由'],[[q['key']+' '+q['dimension'],f"{z['scores'][q['key']]}/{MAX[q['key']]}",z['evidence'][q['key']]] for q in Q]))
 parts.append('</details>')
 ca_anchors=[a for a in anchors if a['case_id']==ca]
 parts.append('<details><summary>原始轨迹证据定位（messages从0计）</summary>')
 for a in ca_anchors:parts.append('<p>'+h(a['model'])+' · '+h(a['run_id'])+' · messages['+str(a['message_index_zero_based'])+']</p><pre>'+h(a['trajectory_path']+'\n'+a['excerpt'])+'</pre>')
 parts.append('</details>')

parts.append('''<h2>可以放进论文的发现</h2><ol><li><strong>统一观察范围是解释一致性的前提。</strong>Stylish的专家备注、评分理由和轨迹共同表明，视口截图与完整长画板展示了不同范围的内容；缺失与首屏外内容需要分开编码。尚不能声称统一截图会提高一致性，需要反事实重评。</li><li><strong>发现关键缺陷不保证总分保留其影响。</strong>Stylish的自动评分已将GPT主操作定位评0分，但其他分项优势使总分仍高于专家更喜欢的Kimi。这是可直接复算的补偿效应。</li><li><strong>任务符合性与通用产品合理性会发生冲突。</strong>FinX/Paradise中被批评的部分字段是简报固定数据；这需要在评价对象中明确区分。不能把全部通用可用性批评简单归为判官错误。</li><li><strong>综合视觉分档在局部样本中缺乏区分度。</strong>Octom的Fable与Opus均获F5满分，却有7分总差且人偏好逆转；Paradise的Fable/GPT视觉F1–F5完全相同。这支持检查量表分辨率，不证明应按本组样本调权。</li><li><strong>可交付、可评分与可比较是不同条件。</strong>Fruit Hub的20屏重复被判官识别并放行，但另一评审因其无法比较而暂停。基础设施/状态恢复问题应与视觉质量及模型失败分开标注。</li></ol><h2>仍不能写成确定结论的内容</h2><p>不能宣称专家总是偏好浅色、丰富页面或特定风格；不能声称Rubric系统性压低Fable；不能把没有文字理由的偏好解释成确定的心理机制；不能把按最大分歧挑出的五题当作整体发生率；不能把图层代码里存在的内容等同于原型已经实际可用；不能把另一位评审的备注直接当作R1排序的原因。</p><h2>下一步可验证实验</h2><p>对Stylish统一视口与完整内容证据后重新盲评；对FinX/Paradise向判官补充简报并要求区分固定输入与模型新增错误；对Octom/Paradise让专家补充偏好理由，并分开标注整体视觉与局部功能；对Fruit Hub指定唯一正式版本后重做比较。所有重新评价应作为新实验，不覆盖原始分数。</p><h2>文件与复现</h2><p>运行<code>python arena/analysis/disagreement_cases.py</code>。<a href="case_findings.json">逐例结论</a>、<a href="rubric_items.csv">660项原始评分及理由</a>、<a href="screen_vote_evidence.csv">逐屏投票</a>、<a href="expert_comments.csv">备注</a>、<a href="trace_anchors.json">轨迹定位</a>、<a href="versions.csv">30个产物版本</a>、<a href="requirement_anchors.csv">需求原文定位</a>。图1、图2均另有PDF。source_evidence.json按Arena候选的精确score_id从原始库导出，并在脚本中重新核验。</p></html>''')
(OUT/'报告.html').write_text(''.join(parts))
assert len(items)==5*6*22
assert not any(r['case_id']=='6case-case-004' for r in items)
assert len(version)==30
with zipfile.ZipFile(ROOT/'results_eval/最大分歧案例分析.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(OUT.iterdir()):
  if p.is_file():z.write(p,'disagreement_analysis/'+p.name)
 z.write(Path(__file__),'disagreement_cases.py')
print(json.dumps({'cases':[r['title'] for r in selected],'artifacts':len(version),'score_items':len(items),'direct_votes':len(direct),'screen_votes':len(screen_rows),'notes':len(notes),'trace_anchors':len(anchors)},ensure_ascii=False))
