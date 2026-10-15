from pathlib import Path
import json,re,hashlib,urllib.parse,xml.etree.ElementTree as ET
out=Path('master-navigation-audit');before=json.loads((out/'before.json').read_text(encoding='utf-8'));report={'pages':len(before),'outsideHeadersUnchanged':True,'headerLinksValid':True,'originalCategoryContentUnchanged':True};bad=[];names=['Home','About','Buy','Sell','Property Management','Interior Design','Life Changes','Considerations','Blog','Contact']
from concurrent.futures import ThreadPoolExecutor
page_names=[r['page'] for r in before]+['considerations.html']
with ThreadPoolExecutor(max_workers=12) as pool:sources=dict(zip(page_names,pool.map(lambda n:Path(n).read_bytes().decode('utf-8'),page_names)))
for r in before:
 p=Path(r['page']);s=sources[r['page']];m=re.search(r'<header\b[^>]*id="dd-header".*?</header>',s,re.S);assert m
 assert hashlib.sha256((s[:m.start()]+'<HEADER/>'+s[m.end():]).encode()).hexdigest()==r['outsideHash'],r['page']
 base=re.search(r'<base[^>]*href="([^"]+)"',s);base_dir=(p.parent/base[1]) if base else p.parent
 h=m[0];assert h.count('>Considerations</a>')==1 and 'class="dd-flyout"' not in h,(r['page'],h.count('>Considerations</a>'))
 for href in re.findall(r'href="([^"]+)"',h):
  if href.startswith(('http:','https:','tel:','mailto:','#')):continue
  dest=(base_dir/urllib.parse.unquote(href.split('#')[0])).resolve()
  if not dest.exists():bad.append((str(p),href))
 assert sorted(re.findall(r'href="((?:tel:|mailto:)[^"]+)"',h))==sorted(re.findall(r'href="((?:tel:|mailto:)[^"]+)"',r['header']))
 assert re.findall(r'<img[^>]+src="([^"]+)"',h)==re.findall(r'<img[^>]+src="([^"]+)"',r['header'])
assert not bad,bad
mapping=json.loads((out/'category-photo-map.json').read_text());landing=Path('considerations.html').read_text(encoding='utf-8')
for c in mapping:
 assert f'<h2>{c["title"]}</h2>' in landing and c['description'] in landing and Path(c['url']).exists() and Path(c['image']).exists()
old=ET.fromstring((out/'before-sitemap.xml').read_text(encoding='utf-8'));new=ET.fromstring(Path('sitemap.xml').read_text(encoding='utf-8'));ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
oldurls=[x.text for x in old.findall('.//s:loc',ns)];newurls=[x.text for x in new.findall('.//s:loc',ns)];assert set(oldurls)<=set(newurls);assert newurls.count('https://dommydom.com/considerations.html')==1;assert len(newurls)-len(oldurls)==1
report.update(sitemapOriginalUrls=len(oldurls),sitemapNewUrls=len(newurls),categories=mapping,brokenHeaderLinks=bad)
# Verify removed header destinations retain crawlable incoming links elsewhere.
removed=set()
for r in before:
 page_source=sources[r['page']];base=re.search(r'<base[^>]*href="([^"]+)"',page_source);base_dir=(Path(r['page']).parent/base[1]) if base else Path(r['page']).parent
 oldh=r['header'];newh=re.search(r'<header\b[^>]*id="dd-header".*?</header>',sources[r['page']],re.S)[0]
 def dests(h):return {str((base_dir/urllib.parse.unquote(x.split('#')[0])).resolve()) for x in re.findall(r'href="([^"]+)"',h) if not x.startswith(('http','tel:','mailto:','#'))}
 removed|=dests(oldh)-dests(newh)
incoming={x:[] for x in removed}
for r in before+[{'page':'considerations.html'}]:
 p=Path(r['page']);s=sources[r['page']];base=re.search(r'<base[^>]*href="([^"]+)"',s);base_dir=(p.parent/base[1]) if base else p.parent;s=re.sub(r'<header\b[^>]*id="dd-header".*?</header>','',s,count=1,flags=re.S)
 for href in re.findall(r'href="([^"]+)"',s):
  if href.startswith(('http','tel:','mailto:','#')):continue
  dest=str((base_dir/urllib.parse.unquote(href.split('#')[0])).resolve())
  if dest in incoming and dest!=str(p.resolve()):incoming[dest].append(str(p))
assert all(incoming.values()),[k for k,v in incoming.items() if not v]
report['removedMenuDestinationsStillLinked']={Path(k).name:len(v) for k,v in incoming.items()}
(out/'source-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('Preserved all',len(before),'page bodies, SEO/AEO metadata, logos, contact links and original sitemap URLs. All header destinations exist. Removed menu links retain contextual incoming links.')
