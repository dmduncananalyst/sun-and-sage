from pathlib import Path
import json,re
out=Path('responsive-arrival-audit');out.mkdir(exist_ok=True)
start='''<script data-dd-arrival="mode">(()=>{const w=innerWidth,h=document.currentScript.parentElement;if(w<1200){h.classList.add(w<600?'is-compact':'is-tablet');document.body.classList.toggle('dd-tablet-navigation',w>=600);}})();</script>'''
end='''<script data-dd-arrival="layout">(()=>{if(innerWidth>=1200)return;const h=document.currentScript.parentElement,n=h.querySelector('#dd-navigation'),t=h.querySelector('.dd-header-tools'),b=h.querySelector('.dd-menu-toggle'),c=h.querySelector('.dd-contact-strip');if(t&&b)t.append(b);if(innerWidth<600&&n&&c)n.append(c);document.documentElement.style.setProperty('--dd-header-bottom',Math.max(0,h.getBoundingClientRect().bottom)+'px');})();</script>'''
paths=json.loads(Path('english-restoration-audit/pages.json').read_text())
for name in paths:
 p=Path(name);s=p.read_bytes().decode();m=re.search(r'<header\b[^>]*id="dd-header"[^>]*>',s);assert m,name
 close=s.index('</header>',m.end());s=s[:close]+end+s[close:];s=s[:m.end()]+start+s[m.end():];p.write_bytes(s.encode())
(out/'change.json').write_text(json.dumps({'pages':len(paths),'change':'Initialize responsive header classes and control placement synchronously during parsing, before deferred navigation setup. Desktop path is a no-op.'},indent=2))
print('Applied arrival initialization to',len(paths),'pages')
