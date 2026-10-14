import sys,json,re
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'.codex-tools'))
from bs4 import BeautifulSoup
root=Path.cwd(); originals=json.loads((root/'performance-audit/original-invariants.json').read_text()); failures=[]; counts=[]; refs=0; links=0
for page,before in originals.items():
 path=root/page;soup=BeautifulSoup(path.read_bytes(),'html.parser')
 if (soup.main.get_text() if soup.main else '')!=before['main_text']:failures.append([page,'article text changed'])
 if [str(n) for n in soup.select('meta,title,script[type="application/ld+json"]')]!=before['metadata']:failures.append([page,'metadata changed'])
 if str(soup.select_one('#ss22-navigation'))!=before['nav']:failures.append([page,'navigation changed'])
 base=soup.find('base',href=True);asset_base=(path.parent/base['href']).resolve() if base else path.parent
 counts.append({'page':page,'stylesheets':len(soup.select('link[rel="stylesheet"]')),'eager_images':len(soup.select('img:not([loading="lazy"])'))})
 for tag in soup.select('link[rel="stylesheet"],script[src]'):
  url=tag.get('href',tag.get('src'))
  if not url.startswith(('http','//')) and not (asset_base/url.split('?')[0]).is_file():failures.append([page,'missing asset',url])
 for image in soup.select('img[srcset],link[imagesrcset]'):
  url=image.get('srcset',image.get('imagesrcset',''))
  if '.performance.webp' in url:
   from urllib.parse import unquote
   if not (asset_base/unquote(url)).is_file():failures.append([page,'missing lossless image',url])
 for section in soup.select('.source-reference-links'):
  refs+=1
  for li in section.select('li'):
   if not li.select_one('a[href]'):failures.append([page,'unlinked source',li.get_text()])
  for a in section.select('a[href]'):
   links+=1;url=a['href']
   if not url.startswith(('http','//')) and not (asset_base/url).is_file():failures.append([page,'missing internal source',url])
result={'checked_pages':len(originals),'reference_sections':refs,'source_links':links,'failures':failures,'counts':counts}
(root/'performance-audit/static-verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('Pages',len(originals),'Sections',refs,'Links',links,'Failures',len(failures));print(failures[:20])
