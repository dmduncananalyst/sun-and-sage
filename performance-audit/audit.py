import sys, json, re
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'.codex-tools'))
from bs4 import BeautifulSoup
root=Path.cwd(); rows=[]; refs=[]; media={}
paths=list(root.glob('*.html'))+list(root.glob('blog/*.html'))+list(root.glob('life-changes/**/*.html'))+list(root.glob('design-questions/*.html'))+list(root.glob('short-term-rental-questions/*.html'))
for path in sorted(paths):
 soup=BeautifulSoup(path.read_bytes(),'html.parser')
 rows.append({'page':path.relative_to(root).as_posix(),'stylesheets':len(soup.select('link[rel="stylesheet"]')),'images':len(soup.select('img')),'eager_images':len(soup.select('img:not([loading="lazy"])'))})
 for heading in soup.find_all(re.compile('^h[1-6]$')):
  if re.match(r'^(sources|resources|references)\b',heading.get_text(' ',strip=True),re.I):
   container=heading.parent
   refs.append({'page':path.relative_to(root).as_posix(),'heading':heading.get_text(' ',strip=True),'html':str(container),'links':[{'name':a.get_text(' ',strip=True),'url':a.get('href')} for a in container.select('a')]})
 base=soup.find('base',href=True);asset_base=(path.parent/base['href']).resolve() if base else path.parent
 for tag in soup.select('img[src], source[src], video[src]'):
  local=(asset_base/tag['src'].split('?')[0]).resolve()
  if local.is_file(): media[str(local.relative_to(root))]={'bytes':local.stat().st_size,'path':str(local.relative_to(root))}
result={'pages':rows,'references':refs,'largest_referenced_media': sorted(media.values(),key=lambda x:x['bytes'],reverse=True)[:25]}
(root/'performance-audit/inventory.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('Pages:',len(rows),'Reference sections:',len(refs),'Links:',sum(len(r['links']) for r in refs))
print('Unique references:',json.dumps(sorted({(a['name'],a['url']) for r in refs for a in r['links']}),indent=2))
print('Unlinked sections:',json.dumps([r for r in refs if not r['links']],indent=2))
print('Largest media:',json.dumps(result['largest_referenced_media'][:8],indent=2))
