from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import json,re
out=Path('complete-master-audit');out.mkdir(exist_ok=True)
paths=json.loads(Path('responsive-header-audit/changed-header-pages.json').read_text(encoding='utf-8-sig'))+['considerations.html'];root=Path.cwd()
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.base='';self.images=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='base':self.base=a.get('href','')
  if tag in ['img','source']:
   if a.get('src'):self.images.append((tag,a['src'],a.get('alt','')))
   for part in a.get('srcset','').split(','):
    if part.strip():self.images.append(('srcset',part.strip().split()[0],a.get('alt','')))
with ThreadPoolExecutor(max_workers=12) as pool:sources=dict(zip(paths,pool.map(lambda n:Path(n).read_text(encoding='utf-8'),paths)))
refs={};external=[]
for n,s in sources.items():
 p=Parser();p.feed(s);base=Path(n).parent/p.base
 for kind,url,alt in p.images:
  if url.startswith(('http:','https:','data:','//')):external.append({'page':n,'src':url[:200]});continue
  dest=(base/unquote(urlsplit(url).path)).resolve();refs.setdefault(str(dest),[]).append({'page':n,'src':url,'alt':alt,'kind':kind})
 def dummy():pass
bad=[]
def check(name):
 p=Path(name)
 if not p.exists():return 'missing'
 if not p.stat().st_size:return 'empty'
 if p.suffix.lower() not in ['.svg','.mp4','.webm']:
  try:
   with Image.open(p) as im:im.verify()
  except Exception as e:return str(e)
 return None
with ThreadPoolExecutor(max_workers=12) as pool:
 for name,error in zip(refs,pool.map(check,refs)):
  if error:bad.append({'file':str(Path(name).relative_to(root)),'error':error,'references':refs[name]})
report={'pages':len(paths),'uniqueAssets':len(refs),'references':sum(map(len,refs.values())),'bad':bad,'external':external};(out/'final-image-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='external'},indent=2)[:1500])
