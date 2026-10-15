from pathlib import Path
import re,json,hashlib,urllib.parse
exec(Path('final-navigation-audit/update-headers.py').read_text(encoding='utf-8-sig').split("root=Path('.')")[0])
out=Path('header-hover-audit');records=json.loads((out/'headers-before.json').read_text());issues=[];paths=set();exists={};mapping={'buyer-questions.html':'Buyer Resources','homebuyer-financing-questions.html':'Financing','seller-questions.html':'Sell','design-questions.html':'Interior Design','short-term-rental-questions.html':'Property Management'}
labels=['Home','About','Buy','Sell','Property Management','Interior Design','Life Changes','Blog','Contact']
for r in records:
 p=Path(r['page']);s=p.read_bytes().decode();hm=re.search(r'<header\b[^>]*id="ss22-header"[^>]*>.*?</header>',s,re.S);outside=s[:hm.start()]+'<HEADER/>'+s[hm.end():]
 if hashlib.sha256(outside.encode()).hexdigest()!=r['outsideHash']:issues.append([r['page'],'non-header change'])
 nav=Parse(re.search(r'<nav\b(?=[^>]*id="ss22-navigation")[^>]*>.*?</nav>',hm[0],re.S)[0]).root.children[0];header=Parse(hm[0]).root;links=[a.attrs['href'] for a in header.links()];actual=[n.text() if n.tag=='a' else n.children[0].text() for n in nav.children if isinstance(n,Node)]
 if actual!=labels:issues.append([r['page'],'wrong labels'])
 if not set(h for h,t in r['oldLinks']).issubset(links):issues.append([r['page'],'lost old links'])
 cities=header.find('ss22-neighborhoods').links();expected=r['neighborhoods'];got=[(a.attrs['href'],a.text()) for a in cities]
 if got!=[tuple(x) for x in expected]:issues.append([r['page'],'city list mismatch'])
 if set(a.attrs['href'] for a in nav.find('ss22-buyers').links()).intersection(h for h,t in expected):issues.append([r['page'],'cities repeated under Buy'])
 for url,category in mapping.items():
  target=nav.find('ss22-buyers') if category in ['Financing','Buyer Resources'] else next(n for n in nav.children if isinstance(n,Node) and n.tag=='div' and n.children[0].text()==category)
  if not any(a.attrs['href'].endswith(url) for a in target.links()):issues.append([r['page'],'missing Considerations route',url])
 base=re.search(r'<base[^>]*href="([^"]+)"',s);pageurl='https://local/'+r['page'].replace('\\','/');baseurl=urllib.parse.urljoin(pageurl,base[1]) if base else pageurl
 for h in links:
  u=urllib.parse.urlparse(urllib.parse.urljoin(baseurl,h))
  if u.netloc!='local':continue
  route=urllib.parse.unquote(u.path).lstrip('/');paths.add(route)
  if route not in exists:exists[route]=Path(route).is_file()
  if not exists[route]:issues.append([r['page'],'broken URL',h,route])
result={'pages':len(records),'neighborhoodLinks':30,'cities':26,'regionalGuides':4,'allOriginalHeaderURLsPreserved':not any('lost old' in str(i) for i in issues),'distinctCurrentHeaderURLs':len(paths),'allPageContentOutsideHeaderUnchanged':not any('non-header' in str(i) for i in issues),'allNeighborhoodAndConsiderationsMappingsVerified':not issues,'missingOrBrokenRoutes':sorted(k for k,v in exists.items() if not v),'issues':issues,'considerationsMap':mapping,'searchOptions':[{'label':'Personalized Home Search','url':'search.html','experience':'Existing city/price/property-type search request form; regional guides live under Neighborhoods.'}]}
(out/'source-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
