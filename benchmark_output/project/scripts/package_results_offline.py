"""Package local analysis, all selected runs, referenced historical evidence and score DBs.
Excludes private agent/account configuration. Writes an immutable archive and portable preparation tools.
"""
from pathlib import Path
import os,re,csv,json,hashlib,shutil,sqlite3,tarfile,time,collections as C,importlib.metadata,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1];EXPORT=ROOT/'offline_exports';STAMP='20261109'
BUNDLE=EXPORT/('benchmark-design-offline-'+STAMP);BUNDLE.mkdir(exist_ok=True)
PROJECT=BUNDLE/'project';PROJECT.mkdir(exist_ok=True);META=BUNDLE/'metadata';META.mkdir(exist_ok=True);TOOLS=BUNDLE/'tools';TOOLS.mkdir(exist_ok=True)
rows=list(csv.DictReader(open(ROOT/'results_eval/资产清单-索引.csv',encoding='utf-8-sig')))
HUANG=Path('/mnt/afs_design/huangxinyue/bench-runs')
GAO=Path('/mnt/afs_design/gaoyongyong/code/rate_website_figma-sft-cc-tap-benchmark-design/storage/benchmarks')
PATH_MAP=[(str(ROOT),'project'),(str(HUANG),'runs/huangxinyue'),(str(GAO),'runs/gaoyongyong')]
MAN=[];EXCLUDED=[];MISSING=[];DBCOUNT=0
BANNED_DIRS={'claude-config','private','.git','.aws','.codex','node_modules','__pycache__','.venv','venv'}
BANNED_FILES={'copy-accounts.json','server.json','compatibility-proxy-config.json','compatibility-proxy.json','figma-mcp.json','.env','.env.local'}
def forbidden(p):return p.name in BANNED_FILES or any(s in BANNED_DIRS for s in p.parts) or p.name.endswith(('-wal','-shm','.pid','.lock','.pyc'))
def dest(p):
 p=Path(p)
 for prefix,rel in PATH_MAP:
  try:return BUNDLE/rel/p.relative_to(prefix)
  except ValueError:pass
 raise ValueError('Unmapped source '+str(p))
def copy_file(p,q=None):
 global DBCOUNT
 p=Path(p);q=Path(q) if q else dest(p)
 if forbidden(p):EXCLUDED.append(dict(source=str(p),reason='private configuration, runtime cache, or database sidecar'));return
 if not p.exists():MISSING.append(dict(source=str(p),reason='referenced file missing'));return
 if q.exists() and p.suffix not in ['.sqlite3','.sqlite','.db'] and q.stat().st_size==p.stat().st_size:
  MAN.append(dict(source=str(p),bundle_path=str(q.relative_to(BUNDLE)),bytes=q.stat().st_size,action='copy'));return
 q.parent.mkdir(parents=True,exist_ok=True)
 action='copy'
 if p.suffix in ['.sqlite3','.sqlite','.db']:
  with tempfile.TemporaryDirectory(prefix='benchmark-sqlite-',dir='/tmp') as td:
   snapshot=Path(td)/'snapshot.sqlite3';local_source=Path(td)/'source.sqlite3'
   # Read raw DB+WAL without creating a shared-memory file beside the original DB.
   # Require stable source metadata across the copy, then let local SQLite apply WAL.
   def signature():
    return [(str(x),x.stat().st_size,x.stat().st_mtime_ns) for x in [p,Path(str(p)+'-wal')] if x.exists()]
   for attempt in range(3):
    before=signature();shutil.copy2(p,local_source)
    source_wal=Path(str(p)+'-wal');local_wal=Path(str(local_source)+'-wal')
    if source_wal.exists():shutil.copy2(source_wal,local_wal)
    elif local_wal.exists():local_wal.unlink()
    if before==signature():break
   else:raise RuntimeError('Source DB changed during snapshot: '+str(p))
   with sqlite3.connect('file:'+str(local_source)+'?mode=ro',uri=True) as a:
    with sqlite3.connect(str(snapshot)) as b:a.backup(b);b.execute('PRAGMA journal_mode=DELETE')
   with sqlite3.connect('file:'+str(snapshot)+'?mode=ro',uri=True) as b:
    assert b.execute('PRAGMA quick_check').fetchone()[0]=='ok'
   shutil.copy2(snapshot,q)
  action='consistent_sqlite_backup';DBCOUNT+=1
 else:shutil.copy2(p,q)
 MAN.append(dict(source=str(p),bundle_path=str(q.relative_to(BUNDLE)),bytes=q.stat().st_size,action=action))
def copy_tree(p,q=None):
 p=Path(p);q=Path(q) if q else dest(p)
 if forbidden(p):EXCLUDED.append(dict(source=str(p),reason='private or cache directory'));return
 if not p.exists():MISSING.append(dict(source=str(p),reason='referenced directory missing'));return
 for child in sorted(p.iterdir()):
  if child.is_dir():copy_tree(child,q/child.name)
  elif child.is_file():copy_file(child,q/child.name)
# All local analysis files, aliases materialized for portable HTML browsing.
for name in ['results_eval','deliver-20261103','arena','benchmarks','docs']:
 copy_tree(ROOT/name)
(ROOT/'scripts').mkdir(exist_ok=True)
for p in sorted((ROOT/'scripts').iterdir()):
 if p.is_file() and p.suffix in ['.py','.mjs','.js','.sh']:copy_file(p)
for p in sorted(ROOT.glob('*.md')):copy_file(p)
for name in ['package.json','package-lock.json']:
 if (ROOT/name).exists():copy_file(ROOT/name)
# Locate run references in analysis files, in addition to all 177 selected rows.
run_dirs={Path(r['run_dir']) for r in rows}
pat=re.compile(r'/mnt/(?:afs_design|afs)/[^\s\"\'<>`\\,;]*?/runs/TEST-\d+_\d+')
for p in (ROOT/'results_eval').rglob('*'):
 if p.is_file() and p.suffix.lower() in ['.json','.jsonl','.csv','.html','.txt','.md','.js','.py']:
  for m in pat.finditer(p.read_text(errors='replace')):
   z=Path(m.group().replace('/mnt/afs/','/mnt/afs_design/'))
   if z.is_dir():run_dirs.add(z)
for i,p in enumerate(sorted(run_dirs)):
 copy_tree(p)
 if (i+1)%20==0:print(json.dumps({'phase':'runs','done':i+1,'total':len(run_dirs),'files':len(MAN)},ensure_ascii=False),flush=True)
# The score DBs and round inputs that resolve every adopted run.
round_dirs={Path(r['round_db']).parent for r in rows}
for p in sorted(round_dirs):
 for name in ['ui-eval.sqlite3','plan.json','dataset.json','rubric.json','inputs.json','timing.json','process.md','process-report.py','gpt-adapter.log','complete.json']:
  if (p/name).exists():copy_file(p/name)
 if (p/'offline-judge').exists():copy_tree(p/'offline-judge')
for p in sorted(HUANG.iterdir()):
 if p.is_file() and p.suffix in ['.md','.py']:copy_file(p)
# Map every Arena candidate image to locally available original bytes, without substituting versions.
hashes={}
for m in MAN:
 if Path(m['bundle_path']).suffix.lower() in ['.png','.jpg','.jpeg','.webp']:
  p=BUNDLE/m['bundle_path'];h=hashlib.sha256(p.read_bytes()).hexdigest();hashes.setdefault(h,p)
with sqlite3.connect(str(PROJECT/'arena/arena.sqlite3')) as c:candidates=[json.loads(x[0]) for x in c.execute('select body from candidates')]
image_rows=[]
for c in candidates:
 for ix,im in enumerate(c['images']):
  src=hashes.get(im['sha256']);target=PROJECT/'arena'/im['file']
  if src and not target.exists():
   target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,target)
   MAN.append(dict(source=str(src.relative_to(BUNDLE)),bundle_path=str(target.relative_to(BUNDLE)),bytes=target.stat().st_size,action='arena_image_reconstructed_by_exact_sha256'))
  image_rows.append(dict(candidate_id=c['id'],case_id=c['case_id'],run_id=c['run_id'],image_index=ix,sha256=im['sha256'],bundle_path=str(target.relative_to(BUNDLE)),available=src is not None))
# A readable mapping and immutable copies are kept; preparation changes only extracted project text.
(META/'path_map.json').write_text(json.dumps([dict(original_prefix=a,bundle_prefix=b) for a,b in PATH_MAP],ensure_ascii=False,indent=2))
for name,data in [('file_inventory.csv',MAN),('excluded_files.csv',EXCLUDED),('missing_references.csv',MISSING),('arena_image_inventory.csv',image_rows)]:
 with open(META/name,'w',encoding='utf-8-sig',newline='') as f:
  keys=list(data[0]) if data else ['source','reason'];w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(data)
run_index=[]
for r in rows:
 run_index.append(dict(round=r['round'],case_id=r['case_id'],title=r['title'],model=r['model'],run_id=r['run_id'],trajectory_path=str(dest(r['trajectory_path']).relative_to(BUNDLE)),trace_sqlite=str(dest(r['trace_sqlite']).relative_to(BUNDLE)),run_log=str(dest(r['run_log']).relative_to(BUNDLE)) if r['run_log'] else '',round_db=str(dest(r['round_db']).relative_to(BUNDLE)),frames_dir=str(dest(r['frames_dir']).relative_to(BUNDLE)),copy_figma_url=r['copy_figma_url']))
with open(META/'portable_run_index.csv','w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(run_index[0]));w.writeheader();w.writerows(run_index)
requirements=[]
for name in ['numpy','scipy','matplotlib','pandas','Pillow']:
 try:requirements.append(name+'=='+importlib.metadata.version(name))
 except importlib.metadata.PackageNotFoundError:requirements.append(name)
(BUNDLE/'requirements-analysis.txt').write_text('\n'.join(requirements)+'\n')
prepare='''"""After extraction: python tools/prepare_local.py. Raw run evidence is never rewritten."""
from pathlib import Path
import json,shutil
ROOT=Path(__file__).resolve().parents[1]
maps=json.load(open(ROOT/'metadata/path_map.json'))
pairs=[]
for m in maps:
 target=(ROOT/m['bundle_prefix']).as_posix();pairs.append((m['original_prefix'],target));pairs.append((m['original_prefix'].replace('/mnt/afs_design/','/mnt/afs/'),target))
pairs.sort(key=lambda x:len(x[0]),reverse=True)
count=0
for p in (ROOT/'project').rglob('*'):
 if not p.is_file() or p.suffix.lower() not in {'.json','.jsonl','.csv','.html','.md','.txt','.py','.js','.mjs','.sh'}:continue
 try:old=p.read_text(encoding='utf-8')
 except (UnicodeError,OSError):continue
 new=old
 for a,b in pairs:new=new.replace(a,b)
 if new!=old:
  backup=ROOT/'metadata/original_project_text'/p.relative_to(ROOT/'project')
  if not backup.exists():backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,backup)
  p.write_text(new,encoding='utf-8');count+=1
print(f'Updated {count} project text files for {ROOT}. Raw runs untouched; original text backups in metadata/original_project_text.')
'''
(TOOLS/'prepare_local.py').write_text(prepare)
verify='''from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];bad=[];n=0
for row in json.load(open(ROOT/'metadata/checksums.json')):
 p=ROOT/row['path'];n+=1
 if not p.is_file() or hashlib.file_digest(open(p,'rb'),'sha256').hexdigest()!=row['sha256']:bad.append(row['path'])
print('Checked',n,'files; failures',len(bad))
for x in bad:print(x)
sys.exit(bool(bad))
'''.replace("hashlib.file_digest(open(p,'rb'),'sha256').hexdigest()","hashlib.sha256(p.read_bytes()).hexdigest()")
(TOOLS/'verify_bundle.py').write_text(verify)
missing_images=sum(not x['available'] for x in image_rows)
summary={'created_date':'2026-11-09 Asia/Shanghai','indexed_runs':len(rows),'included_run_directories':len(run_dirs),'historical_extra_runs':len(run_dirs)-len(rows),'round_databases':len(round_dirs),'sqlite_consistent_backups':DBCOUNT,'indexed_trajectories_present':sum(dest(r['trajectory_path']).exists() for r in rows),'indexed_trace_databases_present':sum(dest(r['trace_sqlite']).exists() for r in rows),'indexed_logs_present':sum(bool(r['run_log']) and dest(r['run_log']).exists() for r in rows),'arena_candidates':len(candidates),'arena_images_total':len(image_rows),'arena_images_available':len(image_rows)-missing_images,'arena_images_missing':missing_images,'missing_local_references':len(MISSING),'private_config_paths_excluded':len(EXCLUDED),'figma_native_files':0,'cloud_figma_files':'URLs retained; no native .fig files available locally; no claim that PNG/layer snapshots replace editable originals.','exclusion_policy':'Chat Bot AI old GPT remains excluded from analyses, but historical raw evidence is archived without deleting it.'}
(META/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
readme=f'''离线评测工作包 2026-11-09

解压后先打开 START.html，或直接打开 project/results_eval 下的各报告 HTML。

内容
- results_eval 的全部原始文件与已生成分析、图表、证据；两个目录别名已实体化。
- 全部177个索引运行，加报告引用的1个历史运行；原始trajectory、trace抓包、media图片、完整run.log（存在的148份）、运行快照、交付图和判官输入。
- 27个轮次的评分数据库、题目/输入/量表配置，Arena数据库与排序快照、交付包及29题需求。
- 分析脚本、量表、过程文档、依赖版本、相对路径索引及逐文件SHA256。

本地工作步骤
1. 解压。先执行 python tools/verify_bundle.py 核对原始包文件。
2. 如需运行脚本或让报告中的服务器绝对路径指向本机，执行 python tools/prepare_local.py。
   它只转换 project 内文本里的已知原始路径；raw runs 不改写。修改前的文本另存 metadata/original_project_text。
   转换后 checksums.json 不再对应被修改的工作文本，这是预期现象；原始压缩包和备份保留不变。
3. 使用 Python 3.10+，按 requirements-analysis.txt 安装依赖。HTML浏览与数据读取可离线；包内不含Python环境和依赖wheel。
4. 从 project 目录运行 arena/analysis 下脚本。示例：python arena/analysis/workflow_analysis.py。
   本地只分析数据，不启动Figma/模型接口。云端Figma链接仍需网络及原有访问权限。

路径
project/：原项目结构；runs/huangxinyue/、runs/gaoyongyong/：原始运行及评分数据。
metadata/portable_run_index.csv：无需改路径即可读的相对路径索引。
metadata/file_inventory.csv：来源、包内路径、大小与打包动作。
metadata/path_map.json：服务器路径与本地目录的映射。

数据库
所有SQLite库使用在线backup接口生成一致性快照并通过quick_check；WAL内容已合入。
不复制-wal/-shm和写锁文件。快照数据库字节哈希可能与源库不同，属于正常情况。

边界与缺口
- Arena的{missing_images}张历史候选图在现有本地资产中找不到精确SHA256匹配；见metadata/arena_image_inventory.csv。没有用别的版本替代。
- 本地没有原生.fig副本；Figma作答/模板URL、图层快照、媒体与截图均已保留，不能据此声称原生可编辑文件可离线打开。
- 4个历史Arena Gemini run的原始轨迹本地仍未知；不虚构补齐，版本差异见已有资产清单。
- Chat Bot AI旧GPT仅作为历史证据保留，分析排除规则不变。
- 按资产清单排除claude-config、private、账号/代理/MCP服务器配置、运行缓存和锁，不含登录凭据目录。
- 工作包是完整的私有研究材料，包含原始运行日志与人评数据库；不是为匿名公开发布整理的数据集。
'''
(BUNDLE/'README.txt').write_text(readme)
(BUNDLE/'START.html').write_text('''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>离线评测工作包</title><style>body{font:17px/1.9 system-ui;max-width:900px;margin:50px auto;padding:24px;color:#263648}a{color:#315a8c}</style><h1>离线评测工作包</h1><p>先读<a href="README.txt">本地使用说明</a>，再查看分析与原始数据。原始轨迹和数据库随包保存。</p><ul><li><a href="project/results_eval/workflow_analysis/报告.html">共同工作流分析</a> · <a href="project/results_eval/workflow_analysis/review.html">轨迹证据查看器</a></li><li><a href="project/results_eval/priority1_paper/报告.html">专家排名与评价一致性</a></li><li><a href="project/results_eval/behavior_analysis/报告.html">工作行为与设计结果</a></li><li><a href="project/results_eval/模型行为深挖/index.html">模型行为案例深挖</a></li><li><a href="project/results_eval/全部模型全部题-交付导航.html">全部交付链接</a></li><li><a href="project/results_eval/资产清单.md">原资产清单</a></li><li><a href="metadata/portable_run_index.csv">相对路径运行索引</a></li><li><a href="metadata/summary.json">打包范围与缺口</a></li></ul></html>''')
# Hash everything except the checksum index itself, including raw evidence and helpers.
checks=[]
for p in sorted(BUNDLE.rglob('*')):
 if p.is_file():checks.append(dict(path=str(p.relative_to(BUNDLE)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(META/'checksums.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
print(json.dumps({'phase':'archive','files':len(checks)+1,'bytes':sum(x['bytes'] for x in checks),'summary':summary},ensure_ascii=False),flush=True)
archive=EXPORT/(BUNDLE.name+'.tar.gz')
with tarfile.open(archive,'w:gz',compresslevel=4) as t:t.add(BUNDLE,arcname=BUNDLE.name)
# Stream every member to verify compressed payload checksums, not just the tar headers.
expected={BUNDLE.name+'/'+c['path']:c for c in checks};seen=set()
with tarfile.open(archive,'r:gz') as t:
 for member in t:
  if not member.isfile():continue
  seen.add(member.name)
  if member.name not in expected:continue
  h=hashlib.sha256();f=t.extractfile(member)
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
  assert h.hexdigest()==expected[member.name]['sha256'],member.name
assert set(expected)<=seen
h=hashlib.sha256()
with open(archive,'rb') as f:
 for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
sha=h.hexdigest();(EXPORT/(archive.name+'.sha256')).write_text(sha+'  '+archive.name+'\n')
(EXPORT/(BUNDLE.name+'-summary.json')).write_text(json.dumps(dict(summary,archive=str(archive),archive_bytes=archive.stat().st_size,sha256=sha,verified_files=len(checks)),ensure_ascii=False,indent=2))
print(json.dumps({'phase':'complete','archive':str(archive),'archive_bytes':archive.stat().st_size,'sha256':sha,'verified_files':len(checks)},ensure_ascii=False),flush=True)
