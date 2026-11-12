from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];bad=[];n=0
for row in json.load(open(ROOT/'metadata/checksums.json')):
 p=ROOT/row['path'];n+=1
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:bad.append(row['path'])
print('Checked',n,'files; failures',len(bad))
for x in bad:print(x)
sys.exit(bool(bad))
