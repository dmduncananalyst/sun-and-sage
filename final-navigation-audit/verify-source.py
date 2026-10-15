from pathlib import Path
import json,re,hashlib,urllib.parse
root=Path.cwd();out=root/'final-navigation-audit'
exec((out/'update-headers.py').read_text(encoding='utf-8-sig').split("root=Path('.')")[0])
records=[r for r in json.loads((out/'headers-before.json').read_text()) if 'audit' not in r['page']];issues=[];urls=set();original_broken=set()
labels=['Home','About','Buy','Sell','Property Management','Interior Design','Life Changes','Blog','Contact']
for record in records:
 p=root/record['page'];s=p.read_bytes().decode();header=re.search(r'<header\b[^>]*id="ss22-header"[^>]*>.*?</header>',s,re.S)
 outside=s[:header.start()]+'<HEADER/>'+s[header.end():];outside=outside.replace(record['cssLink'],'',1)
 if hashlib.sha256(outside.encode()).hexdigest()!=record['outsideHash']:issues.append([str(p),'content outside header changed'])
 nav=Parse(re.search(r'<nav\b(?=[^>]*id="ss22-navigation")[^>]*>.*?</nav>',header[0],re.S)[0]).root.children[0]
 actual=[n.text() if n.tag=='a' else next(c.text() for c in n.children if isinstance(c,Node) and c.tag=='a') for n in nav.children if isinstance(n,Node)]
 if actual!=labels:issues.append([str(p),'wrong labels'])
 links=[a.attrs['href'] for a in nav.links()]+[record['searchHref']]
 if not set(h for h,t in record['oldLinks']).issubset(links):issues.append([str(p),'lost original links'])
 base=re.search(r'<base[^>]*href="([^"]+)"',s);pageurl='https://local/'+record['page'].replace('\\','/');baseurl=urllib.parse.urljoin(pageurl,base[1]) if base else pageurl
 def resolve(h):
  u=urllib.parse.urljoin(baseurl,h);parsed=urllib.parse.urlparse(u)
  return urllib.parse.unquote(parsed.path).lstrip('/') if parsed.netloc=='local' else None
 for h in links:
  path=resolve(h)
  if path and not (root/path).is_file():issues.append([record['page'],'missing destination',h,path])
  if path:urls.add(path)
 for h,t in record['oldLinks']:
  path=resolve(h)
  if path and not (root/path).is_file():original_broken.add(path)
articlemap={}
for label,m in json.loads((out/'considerations-map.json').read_text()).items():
 s=(root/m['url']).read_text(encoding='utf-8');articles=sorted(set(re.findall(r'href="([^"]+)"[^>]*>\s*Read More',s,re.I)))
 articlemap[label]={'landing':m['url'],'category':m['newCategory'],'articles':articles}
 for h in articles:
  if not (root/h.split('#')[0]).is_file():issues.append([m['url'],'missing article',h])
result={'pages':len(records),'allPageContentOutsideHeaderPreserved':not any('content outside' in str(i) for i in issues),'distinctHeaderDestinations':len(urls),'originalBrokenURLs':sorted(original_broken),'issues':issues,'formerConsiderations':articlemap}
(out/'source-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='formerConsiderations'},indent=2))

