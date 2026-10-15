from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
import re,json,hashlib,shutil
out=Path('complete-master-audit');out.mkdir(exist_ok=True);paths=json.loads(Path('responsive-header-audit/changed-header-pages.json').read_text(encoding='utf-8-sig'))+['considerations.html']
with ThreadPoolExecutor(max_workers=12) as pool:sources=dict(zip(paths,pool.map(lambda n:Path(n).read_bytes().decode('utf-8'),paths)))
rows=[]
for name,s in sources.items():
 h=re.search(r'<header\b[^>]*id="dd-header".*?</header>',s,re.S);assert h,name
 rows.append({'page':name,'header':h[0],'outsideHash':hashlib.sha256((s[:h.start()]+'<HEADER/>'+s[h.end():]).encode()).hexdigest(),'sourceHash':hashlib.sha256(s.encode()).hexdigest()})
(out/'before-headers.json').write_text(json.dumps(rows),encoding='utf-8')
for n in ['buy-a-home.html','life-changes.html','assets/buy-with-dominique.css','assets/navigation-v22.js','assets/responsive-navigation.css','sitemap.xml','considerations.html']:
 shutil.copy2(n,out/('before-'+Path(n).name))
class Text(HTMLParser):
 def __init__(self):super().__init__();self.words=[]
 def handle_data(self,x):
  if x.strip():self.words.append(x.strip())
s=sources['buy-a-home.html'];m=re.search(r'<main\b.*?</main>',s,re.S)[0];parser=Text();parser.feed(m)
inventory={'exactMainText':parser.words,'headings':re.findall(r'<h[123][^>]*>(.*?)</h[123]>',m,re.S),'links':re.findall(r'<a\b[^>]*href="([^"]+)"',m),'wheelSteps':re.findall(r'<li class="dd-buy-step".*?<span>(.*?)</span>',m,re.S),'wheelIconPaths':re.findall(r'<li class="dd-buy-step".*?</li>',m,re.S),'mapVectors':re.findall(r'<div class="dd-buy-map">.*?</svg>',m,re.S),'charts':re.findall(r'<figure class="dd-buy-chart".*?</figure>',m,re.S),'mainHash':hashlib.sha256(m.encode()).hexdigest(),'interactions':'Static diagram, static CSS charts, static vector maps; consultation anchor and global contact workflow. No map or wheel interaction exists to preserve.'}
(out/'buy-before-inventory.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8');print('Recorded all 352 headers and full Buy content inventory. Baseline copied.')
