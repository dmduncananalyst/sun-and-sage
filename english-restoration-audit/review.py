from pathlib import Path
import json,re
out=Path('english-restoration-audit'); forms=[]
for n in json.loads((out/'pages.json').read_text()):
 s=Path(n).read_text(encoding='utf-8')
 for tag in re.findall(r'<form\b[^>]*>',s,re.I):
  if any(c in tag for c in ['contactPageForm','regionRequestForm','homeValuationForm']):forms.append({'page':n,'tag':tag})
(out/'legacy-forms.json').write_text(json.dumps(forms,indent=2));print('Active legacy forms:',len(forms))
if Path('english-restore-inspect.py').exists():Path('english-restore-inspect.py').rename(out/'inspect.py')
widths=[768,820,834,1024,1180,1440,390]
s='<!doctype html><html lang="en"><meta charset="utf-8"><title>English restoration verification</title><style>body{font:16px/1.6 Arial;background:#f8f7f3;color:#343c32;margin:32px}section{margin:32px 0}div{display:grid;grid-template-columns:1fr 1fr;gap:24px}img{width:100%;height:auto;border:1px solid #ccc}figure{margin:0}a{color:#48533e}</style><h1>English restoration verification</h1><p>Before and after: sidebar preserved; tablet main font family corrected. Language controls removed. Screenshots show actual local browser renders; moving homepage video frames naturally differ.</p>'
for w in widths:
 for mode in ['closed','expanded'] if 600<=w<1200 else ['closed']:
  s+=f'<section><h2>{w}px — {mode}</h2><div>'+''.join(f'<figure><figcaption>{p.title()}</figcaption><a href="{p}-{w}-{mode}.png"><img src="{p}-{w}-{mode}.png"></a></figure>' for p in ['before','after'])+'</div></section>'
s+='<h2>Original English chats</h2><div>'+''.join(f'<figure><figcaption>{w}px</figcaption><img src="english-chat-{w}.png"></figure>' for w in [834,390])+'</div></html>'
(out/'review.html').write_text(s,encoding='utf-8')
