from pathlib import Path
import re,json,urllib.parse
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
root=Path.cwd();paths=json.loads(Path('responsive-header-audit/changed-header-pages.json').read_text(encoding='utf-8-sig'))+['considerations.html'];seen=set();refs=set();missing=[]
with ThreadPoolExecutor(max_workers=12) as pool:sources=dict(zip(paths,pool.map(lambda n:Path(n).read_text(encoding='utf-8'),paths)))
def resolve(base,url):
 if url.startswith(('http:','https:','data:','//','#')):return None
 u=urllib.parse.unquote(url.split('?')[0].split('#')[0]);return (root/u.lstrip('/') if u.startswith('/') else base/u).resolve()
def css(s,base):
 for url in re.findall(r'url\(\s*[\"\']?([^\"\')\s]+)',s):
  p=resolve(base,url)
  if not p:continue
  if p.suffix.lower()=='.css':load(p)
  elif p.suffix.lower() in ['.jpg','.jpeg','.webp','.png','.svg','.gif','.avif']:refs.add(p)
 for url in re.findall(r'@import\s+[\"\']([^\"\']+)',s):
  p=resolve(base,url)
  if p:load(p)
def load(p):
 if p in seen:return
 seen.add(p)
 if p.exists():css(p.read_text(encoding='utf-8',errors='replace'),p.parent)
for n,s in sources.items():
 base=Path(n).parent;bm=re.search(r'<base[^>]*href="([^"]+)"',s)
 if bm:base/=bm[1]
 for tag in re.findall(r'<link\b[^>]*>',s):
  if 'stylesheet' in tag:
   m=re.search(r'href="([^"]+)"',tag)
   if m:
    p=resolve(base,m[1])
    if p:load(p)
 css(' '.join(re.findall(r'<style[^>]*>(.*?)</style>',s,re.S)),base)
for p in refs:
 if not p.exists() or not p.stat().st_size:missing.append(str(p.relative_to(root)))
 elif p.suffix.lower()!='.svg':
  try:
   with Image.open(p) as im:im.verify()
  except Exception:missing.append(str(p.relative_to(root)))
report={'stylesheets':len(seen),'cssImageFiles':len(refs),'bad':missing};Path('image-and-buy-page-audit/css-image-audit.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
