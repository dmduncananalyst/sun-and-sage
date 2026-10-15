from pathlib import Path
import json
p=Path('english-restoration-audit');a=json.loads((p/'before-navigation.json').read_text());b=json.loads((p/'after-navigation.json').read_text());diff=[]
for old,new in zip(a,b):
 assert not new['language'],new['width']
 for x,y in zip(old['nav'],new['nav']):
  for k in x['css']:
   if k=='fontFamily' and 600<=old['width']<1200:continue
   if x['css'][k]!=y['css'][k]:diff.append((old['width'],x['text'],k,x['css'][k],y['css'][k]))
  if x['rect']!=y['rect']:diff.append((old['width'],x['text'],'rect',x['rect'],y['rect']))
 print(new['width'],new['neighborhoodFont'],{x['css']['fontFamily'] for x in new['nav']})
print('Differences except intended font:',json.dumps(diff)[:5000])
