from pathlib import Path
import re,json,hashlib,html
exec(Path('final-navigation-audit/update-headers.py').read_text(encoding='utf-8-sig').split("root=Path('.')")[0])
root=Path('.');out=root/'header-hover-audit';records=[]
files=json.loads(Path('final-navigation-audit/changed-header-pages.json').read_text())
def article_links(name,prefix):
 s=(root/name).read_text(encoding='utf-8');p=Parse(re.search(r'<main\b.*?</main>',s,re.S)[0]);links=[]
 # Existing card headings and Read More URLs, in their existing order.
 for a in re.findall(r'<article\b.*?</article>',s,re.S):
  title=re.search(r'<h2\b[^>]*>(.*?)</h2>',a,re.S);href=re.search(r'<a\b[^>]*href="([^"]+)"[^>]*>\s*Read More\s*</a>',a,re.S)
  if title and href:links.append(anchor(prefix+href[1],html.unescape(re.sub('<[^>]*>','',title[1]))))
 return links
def flyout(label,href,links):return Node('div',[('class','ss22-flyout')],[Node('a',[('class','ss22-flyout-trigger'),('href',href),('aria-haspopup','true'),('aria-expanded','false')],[label]),Node('div',[('class','ss22-flyout-panel')],links)])
def feature(name,svg,links,cls):
 return '<div class="ss22-feature '+cls+'"><button class="ss22-feature-trigger" type="button" aria-haspopup="true" aria-expanded="false">'+svg+'<span>'+name+'</span></button><div class="ss22-panel"><div class="ss22-panel-content">'+''.join(a.render() for a in links)+'</div></div></div>'
icon='<svg aria-hidden="true" focusable="false" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
house=icon+'<path d="m3 10 9-7 9 7M5 9v12h14V9M9 21v-8h6v8"/></svg>';glass=icon+'<circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/></svg>'
for filename in files:
 p=root/filename;s=p.read_bytes().decode();hm=re.search(r'<header\b[^>]*id="ss22-header"[^>]*>.*?</header>',s,re.S);old=hm[0];nm=re.search(r'<nav\b(?=[^>]*id="ss22-navigation")[^>]*>.*?</nav>',old,re.S);nav=Parse(nm[0]).root.children[0];buy=nav.find('ss22-buyers');content=buy.find('ss22-panel-content');sections=[n for n in content.children if isinstance(n,Node) and n.tag=='section'];basic=sections[0].links();cities=sections[1].links();prefix=basic[1].attrs['href'][:-len('first-time-buyers.html')]
 oldlinks=Parse(nm[0]).root.links();search=re.search(r'<a class="ss22-header-search".*?</a>',old,re.S)
 oldsearch=Parse(search[0]).root.links()[0];searchhref=oldsearch.attrs['href']
 process=basic[2:7];finance=[basic[9],basic[7]]+article_links('homebuyer-financing-questions.html',prefix);resources=[basic[8]]+article_links('buyer-questions.html',prefix)
 content.children=[basic[0],anchor(basic[1].attrs['href'],'First-Time Homebuyers'),flyout('Buying Process',basic[1].attrs['href'],process),flyout('Financing',basic[9].attrs['href'],finance),flyout('Buyer Resources',basic[8].attrs['href'],resources)]
 # Remove only exact duplicate overview rows from the two already long panels.
 for n in nav.children:
  if not isinstance(n,Node) or n.tag!='div' or n is buy:continue
  top=next(c for c in n.children if isinstance(c,Node) and c.tag=='a');panel=n.find('ss22-panel-content')
  if top.text() in ['Interior Design','Life Changes']:
   panel.children=[c for c in panel.children if not(isinstance(c,Node) and c.tag=='a' and c.attrs.get('href')==top.attrs['href'])]
 tools='<div class="ss22-header-tools">'+feature('Neighborhoods',house,cities,'ss22-neighborhoods')+feature('Search',glass,[anchor(searchhref,'Personalized Home Search')],'ss22-search')+'</div>'
 new=old.replace(nm[0],nav.render()).replace(search[0],tools);updated=s[:hm.start()]+new+s[hm.end():];p.write_bytes(updated.encode())
 records.append({'page':filename,'oldHeader':old,'outsideHash':hashlib.sha256((s[:hm.start()]+'<HEADER/>'+s[hm.end():]).encode()).hexdigest(),'oldLinks':[(a.attrs['href'],a.text()) for a in oldlinks]+[(searchhref,'Search')],'neighborhoods':[(a.attrs['href'],a.text()) for a in cities]})
(out/'headers-before.json').write_text(json.dumps(records,indent=2),encoding='utf-8');(out/'neighborhoods.json').write_text(json.dumps([{'url':a.attrs['href'].removeprefix(prefix),'label':a.text()} for a in cities],indent=2),encoding='utf-8');print('Updated',len(records),'live headers; neighborhoods',len(cities),'finance',len(finance),'resources',len(resources))
