"""Read tool calls/results from both trajectory formats and full stream-json logs."""
import json,re
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
  t['result_text']=result[0] if result else ''
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

