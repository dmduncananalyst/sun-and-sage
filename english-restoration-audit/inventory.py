from pathlib import Path
import re,json,collections
paths=json.loads(Path('english-restoration-audit/pages.json').read_text()); cs=[];scripts=collections.Counter()
for n in paths:
 s=Path(n).read_text(encoding='utf-8');m=re.search(r'<script[^>]*id="dominiqueConversationConfig"[^>]*>(.*?)</script>',s,re.S)
 if m:cs.append({'page':n,'cfg':json.loads(m.group(1))})
 for src in re.findall(r'<script[^>]*src="([^"]+)"',s):
  if any(x in src.lower() for x in ['chat','conversation','hubspot','contact']):scripts[src]+=1
Path('english-restoration-audit/chat-inventory.json').write_text(json.dumps(cs,indent=2),encoding='utf-8')
print('Chat pages:',len(cs),'Unique configs:',len({json.dumps(x['cfg'],sort_keys=True) for x in cs}));print(dict(scripts));print(json.dumps(cs[0],indent=2)[:3000])
