from pathlib import Path
import re,json,hashlib,urllib.parse
exec(Path('final-navigation-audit/update-headers.py').read_text(encoding='utf-8-sig').split("root=Path('.')")[0])
out=Path('responsive-header-audit');records=json.loads((out/'headers-before.json').read_text());issues=[];routes=set();exists={};labels=['Home','About','Buy','Sell','Property Management','Interior Design','Life Changes','Blog','Contact']
for r in records:
 p=Path(r['page']);s=p.read_bytes().decode();hm=re.search(r'<header\b[^>]*id="dd-header"[^>]*>.*?</header>',s,re.S)
 if not hm:issues.append([r['page'],'missing new header']);continue
 if hashlib.sha256((s[:hm.start()]+'<HEADER/>'+s[hm.end():]).encode()).hexdigest()!=r['outsideHash']:issues.append([r['page'],'non-header change'])
 old=Parse(r['oldHeader']).root;new=Parse(hm[0]).root;before=[(a.attrs.get('href'),a.text()) for a in old.links()];after=[(a.attrs.get('href'),a.text()) for a in new.links()]
 if before!=after:issues.append([r['page'],'link URL or display name changed'])
 if re.findall(r'<img\b[^>]*src="([^"]+)"',r['oldHeader'])!=re.findall(r'<img\b[^>]*src="([^"]+)"',hm[0]):issues.append([r['page'],'branding asset changed'])
 nav=new.find('dd-nav');actual=[n.text() if n.tag=='a' else n.children[0].text() for n in nav.children if isinstance(n,Node)]
 if actual!=labels:issues.append([r['page'],'wrong primary labels'])
 if len(new.find('dd-neighborhoods').links())!=30:issues.append([r['page'],'city links lost'])
 base=re.search(r'<base[^>]*href="([^"]+)"',s);url='https://local/'+r['page'].replace('\\','/');baseurl=urllib.parse.urljoin(url,base[1]) if base else url
 for href,label in after:
  u=urllib.parse.urlparse(urllib.parse.urljoin(baseurl,href))
  if u.netloc!='local':continue
  route=urllib.parse.unquote(u.path).lstrip('/');routes.add(route)
  if route not in exists:exists[route]=Path(route).is_file()
  if not exists[route]:issues.append([r['page'],'broken destination',href,route])
 # Verify that compact Buy's direct landing pages retain all resources shown in desktop flyouts.
 if r['page']=='index.html':
  buy=new.find('dd-buyers');coverage=[]
  for group in [n for n in buy.find('dd-panel-content').children if isinstance(n,Node) and n.tag=='div']:
   parent=group.children[0].attrs['href'];landing=Path(parent).read_text(encoding='utf-8');targets=[a.attrs['href'] for a in group.links()[1:]]
   for target in targets:
    if target==parent or target=='first-time-homebuyer-programs.html':continue
    coverage.append({'group':group.children[0].text(),'article':target,'linkedFromExistingLanding':bool(re.search(r'href="'+re.escape(target)+'"',landing))})
  if not all(x['linkedFromExistingLanding'] for x in coverage):issues.append(['index.html','mobile resource landing coverage missing'])
hero_before=(out/'before/home-hero-fit.js').read_text(encoding='utf-8-sig');hero_now=Path('assets/home-hero-fit.js').read_text(encoding='utf-8-sig');hero_ok=hero_now==hero_before.replace("getElementById('ss22-header')","getElementById('dd-header')")
if not hero_ok:issues.append(['hero helper','more than header selector changed'])
result={'livePages':len(records),'allPageBodiesAndHeadMetadataBytePreserved':not any('non-header' in str(i) for i in issues),'allOriginalHeaderLinksAndNamesPreserved':not any('link URL' in str(i) for i in issues),'neighborhoods':30,'distinctHeaderPageDestinations':len(routes),'brokenRoutes':sorted(k for k,v in exists.items() if not v),'heroAlgorithmUnchangedOnlyHeaderSelectorUpdated':hero_ok,'mobileBuyerLandingCoverage':coverage,'issues':issues};(out/'source-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='mobileBuyerLandingCoverage'},indent=2))
