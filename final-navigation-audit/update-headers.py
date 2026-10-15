from pathlib import Path
from html.parser import HTMLParser
import re,html,json,hashlib
class Node:
 def __init__(self,tag='',attrs=None,children=None):self.tag=tag;self.attrs=dict(attrs or []);self.children=list(children or [])
 def text(self):return ''.join(c.text() if isinstance(c,Node) else c for c in self.children)
 def render(self):
  attrs=''.join(' '+k+('="'+html.escape(str(v),quote=True)+'"' if v is not None else '') for k,v in self.attrs.items())
  return '<'+self.tag+attrs+'>'+''.join(c.render() if isinstance(c,Node) else html.escape(c,quote=False) for c in self.children)+'</'+self.tag+'>'
 def find(self,cls):
  if cls in self.attrs.get('class','').split():return self
  return next((r for c in self.children if isinstance(c,Node) for r in [c.find(cls)] if r),None)
 def links(self):
  return ([self] if self.tag=='a' else [])+[a for c in self.children if isinstance(c,Node) for a in c.links()]
class Parse(HTMLParser):
 def __init__(self,s):super().__init__(convert_charrefs=True);self.root=Node();self.stack=[self.root];self.feed(s)
 def handle_starttag(self,t,a):n=Node(t,a);self.stack[-1].children.append(n);self.stack.append(n)
 def handle_endtag(self,t):self.stack.pop()
 def handle_data(self,d):self.stack[-1].children.append(d)
def anchor(href,label):return Node('a',[('href',href)],[label])
def wrap(label,href,content,extra=''):
 return Node('div',[('class','ss22-group'+(' '+extra if extra else ''))],[Node('a',[('class','ss22-top'),('href',href),('aria-haspopup','true'),('aria-expanded','false')],[label]),Node('div',[('class','ss22-panel')],[content])])
root=Path('.');out=root/'final-navigation-audit';records=[];mapping={}
for p in root.rglob('*.html'):
 raw=p.read_bytes();s=raw.decode('utf-8');match=re.search(r'<header\b[^>]*id="ss22-header"[^>]*>.*?</header>',s,re.S)
 if not match:continue
 old=match[0];nm=re.search(r'<nav\b(?=[^>]*id="ss22-navigation")[^>]*>.*?</nav>',old,re.S);nav=Parse(nm[0]).root.children[0];items=[c for c in nav.children if isinstance(c,Node)]
 groups={next(c for c in g.children if isinstance(c,Node) and c.tag in ['button','a']).text():g for g in items if g.tag=='div'}
 direct={g.text():g for g in items if g.tag=='a'};consider=groups['Considerations'].links();search=groups['Search'].links();oldlinks=[(a.attrs['href'],a.text()) for a in nav.links()]
 buy=groups['Buyers'].find('ss22-panel-content');buy_sections=[c for c in buy.children if isinstance(c,Node) and c.tag=='section'];bylabel={a.text():a for a in consider};buy_sections[0].children.extend([bylabel['Buying'],bylabel['Financing']]);buy_sections[1].children.extend(search[1:])
 sell=groups['Sellers'].find('ss22-panel-content');sell.children.append(bylabel['Selling']);design=groups['Interior Design'].find('ss22-panel-content');design.children.append(bylabel['Design'])
 prefix=direct['About'].attrs['href'][:-len('about.html')];prop=direct['Property Management'];pm=Node('div',[('class','ss22-panel-content')],[anchor(prop.attrs['href'],prop.text()),bylabel['Rental Ownership']]);design_href=prefix+'interior-design.html';design.children.insert(0,anchor(design_href,'Interior Design'))
 life=groups['Life Changes'];life_anchor=next(c for c in life.children if isinstance(c,Node) and c.tag=='a');life_anchor.attrs['class']='ss22-top';life_anchor.attrs['aria-haspopup']='true';life_anchor.attrs['aria-expanded']='false'
 contact=groups['Contact'].find('ss22-panel-content')
 nav.children=[direct['Home'],direct['About'],wrap('Buy',buy.links()[0].attrs['href'],buy,'ss22-buyers'),wrap('Sell',sell.links()[0].attrs['href'],sell),wrap('Property Management',prop.attrs['href'],pm),wrap('Interior Design',design_href,design),life,direct['Blog'],wrap('Contact',contact.links()[0].attrs['href'],contact)]
 searchhref=search[0].attrs['href'];feature='<a class="ss22-header-search" href="'+html.escape(searchhref,quote=True)+'"><svg aria-hidden="true" focusable="false" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/></svg><span>Search</span></a>'
 newheader=old.replace(nm[0],nav.render()).replace('</header>',feature+'</header>')
 script=re.search(r'<script[^>]*src="([^"]*navigation-v22\.js)"',s)[1];css_href=script.replace('navigation-v22.js','responsive-navigation.css');css='<link rel="stylesheet" href="'+html.escape(css_href,quote=True)+'" data-dommydom-navigation="final"/>'
 new=s[:match.start()]+newheader+s[match.end():];new=new.replace('</head>',css+'</head>',1)
 outside=s[:match.start()]+'<HEADER/>'+s[match.end():]
 records.append({'page':str(p),'oldHeader':old,'outsideHash':hashlib.sha256(outside.encode()).hexdigest(),'oldLinks':oldlinks,'searchHref':searchhref,'cssLink':css,'oldHTMLHash':hashlib.sha256(raw).hexdigest()})
 for a in consider:mapping[a.text()]={'url':a.attrs['href'].removeprefix(prefix),'newCategory':{'Buying':'Buy','Financing':'Buy','Selling':'Sell','Design':'Interior Design','Rental Ownership':'Property Management'}[a.text()]}
 p.write_bytes(new.encode('utf-8'))
(out/'headers-before.json').write_text(json.dumps(records,indent=2),encoding='utf-8');(out/'considerations-map.json').write_text(json.dumps(mapping,indent=2),encoding='utf-8');print('Updated headers',len(records));print(json.dumps(mapping,indent=2))
