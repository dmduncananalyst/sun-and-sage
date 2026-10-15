from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageChops
from urllib.parse import unquote,urlsplit
from html.parser import HTMLParser
import re,json,hashlib
out=Path('complete-master-audit');rows=json.loads((out/'before-headers.json').read_text(encoding='utf-8'))
with ThreadPoolExecutor(max_workers=12) as pool:sources=dict(zip([r['page'] for r in rows],pool.map(lambda r:Path(r['page']).read_bytes().decode(),rows)))
class H(HTMLParser):
 def __init__(self):super().__init__();self.level=0;self.navlevel=0;self.labels=[];self.current=None;self.text=[];self.links=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='nav':self.navlevel=1;self.level=0
  elif self.navlevel:
   if t in ['div','a']:self.level+=1
   if t=='a' and self.level==1:self.current=a;self.text=[]
 def handle_data(self,d):
  if self.current is not None:self.text.append(d)
 def handle_endtag(self,t):
  if self.navlevel:
   if t=='a' and self.current is not None:self.links.append((self.current,''.join(self.text)));self.current=None
   if t in ['div','a']:self.level-=1
   if t=='nav':self.navlevel=0
expected=['Home','About','Buy','Sell','Property Management','Interior Design','Life Changes','Considerations','Blog','Contact'];broken=[]
for row in rows:
 name=row['page'];s=sources[name];m=re.search(r'<header\b[^>]*id="dd-header".*?</header>',s,re.S);h=m[0]
 for label,file in [('Life Changes','life-changes.html'),('Considerations','considerations.html')]:
  a=re.search(r'<nav.*?</nav>',h,re.S)[0];assert re.search(r'<a href="[^"]*'+re.escape(file)+r'">'+label+'</a>',a),name
  assert not re.search(r'<a[^>]*(?:aria-haspopup|aria-expanded|dd-top)[^>]*>'+label+'</a>',h),name
 assert '>Marriage</a>' not in h and '>Growing Family</a>' not in h,name
 if name!='life-changes.html':assert hashlib.sha256((s[:m.start()]+'<HEADER/>'+s[m.end():]).encode()).hexdigest()==row['outsideHash'],name
 base=re.search(r'<base[^>]*href="([^"]+)"',s);base_dir=Path(name).parent/(base[1] if base else '')
 for href in re.findall(r'href="([^"]+)"',h):
  if href.startswith(('https:','http:','mailto:','tel:','#')):continue
  if not (base_dir/unquote(urlsplit(href).path)).resolve().exists():broken.append([name,href])
 assert re.findall(r'href="((?:tel:|mailto:)[^"]+)"',h)==re.findall(r'href="((?:tel:|mailto:)[^"]+)"',row['header']),name
assert not broken,broken
# Life Changes differs only in five image tags, plus its authorized header.
old=(out/'before-life-changes.html').read_bytes().decode('utf-8');new=sources['life-changes.html'];normalize=lambda s:re.sub(r'<img\b[^>]*>','<IMAGE/>',re.sub(r'<header\b[^>]*id="dd-header".*?</header>','<HEADER/>',s.replace('\r\n','\n'),count=1,flags=re.S))
assert normalize(old)==normalize(new)
a=re.findall(r'<main.*?</main>',old,re.S)[0];b=re.findall(r'<main.*?</main>',new,re.S)[0];oldimgs=re.findall(r'<img\b[^>]*>',a);newimgs=re.findall(r'<img\b[^>]*>',b);assert len(oldimgs)==len(newimgs)==7;assert sum(x!=y for x,y in zip(oldimgs,newimgs))==5;assert oldimgs[:2]==newimgs[:2]
mapping=json.loads((out/'life-changes-photo-map.json').read_text())
for c in mapping:
 original=Image.open(c['source']).convert('RGB');final=Image.open(c['image']).convert('RGB');assert original.size==final.size and ImageChops.difference(original,final).getbbox() is None
 assert f'<h2>{c["title"]}</h2>' in b and c['url'] in b
# Buy main is byte-identical: every heading, word, icon, map vector, graph, value and CTA remains.
oldbuy=(out/'before-buy-a-home.html').read_bytes().decode('utf-8');newbuy=sources['buy-a-home.html'];main=lambda s:re.search(r'<main\b.*?</main>',s,re.S)[0];assert main(oldbuy)==main(newbuy)
assert Path('sitemap.xml').read_bytes()==(out/'before-sitemap.xml').read_bytes()
report={'headersUpdated':len(rows),'otherPageContentAndMetadataUnchanged':len(rows)-1,'lifeChangesContentUnchangedExceptFiveImageTags':True,'marriageAndGrowingFamilyPhotosUnchanged':True,'newLifePhotosPixelIdenticalToSuppliedOriginals':True,'buyEntireMainHtmlUnchanged':True,'sitemapUnchanged':True,'brokenHeaderDestinations':broken,'considerationsMapping':json.loads(Path('master-navigation-audit/category-photo-map.json').read_text()),'lifeChangesMapping':mapping}
(out/'source-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('Source preservation passed for all 352 pages; five lossless photo replacements; Buy entire DOM and content unchanged; sitemap unchanged.')
