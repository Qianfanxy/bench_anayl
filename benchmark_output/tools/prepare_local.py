"""After extraction: python tools/prepare_local.py. Raw run evidence is never rewritten."""
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
