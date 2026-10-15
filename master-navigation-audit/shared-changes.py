from pathlib import Path
p=Path('assets/navigation-v22.js');s=p.read_text(encoding='utf-8')
a=s.index('function fits()');b=s.index('// Keep parent destinations',a)
s=s[:a]+'''function layout(){
 const next=innerWidth<600;if(next!==compact)closeAll();compact=next;
 header.classList.toggle('is-compact',compact);header.classList.toggle('is-tablet',!compact&&innerWidth<1200);
 if(compact){if(contacts.parentElement!==nav)nav.append(contacts);}else if(contacts.parentElement!==header)header.insertBefore(contacts,nav);
 position();groups.filter(g=>g.classList.contains('is-open')).forEach(place);
 const rail=!compact&&nav.scrollWidth>nav.clientWidth+1;header.classList.toggle('has-nav-rail',rail);
 nav.setAttribute('aria-label',rail?'Main navigation — swipe or scroll horizontally for more links':'Main navigation');
}
''' +s[b:]
# Search is again an actual compact feature dropdown.
s=s.replace(":g.matches('.dd-buyers')?252",":g.matches('.dd-search')?246:g.matches('.dd-buyers')?252")
# Keep position attached when a tablet rail is scrolled.
s=s.replace("const current=new URL(location.href);", "nav.addEventListener('scroll',()=>{if(!compact)groups.filter(g=>g.classList.contains('is-open')).forEach(place);},{passive:true});\nconst current=new URL(location.href);")
p.write_text(s,encoding='utf-8')
p=Path('assets/responsive-navigation.css');s=p.read_text(encoding='utf-8');s=s.replace("grid-template-areas:'brand rise contacts tools' 'nav nav nav nav';grid-template-columns:230px 114px minmax(260px,1fr) auto", "grid-template-areas:'brand rise tools contacts' 'nav nav nav nav';grid-template-columns:230px 114px minmax(200px,1fr) auto")
s=s.replace('@media(max-width:1279px){#dd-header:not(.is-compact){visibility:hidden;}}','')
s+='''
/* Tablets keep visible navigation. Only phones use the existing MENU panel. */
#dd-header:not(.is-compact) .dd-header-tools{justify-self:center;}
#dd-header:not(.is-compact) .dd-contact-strip{justify-self:end;}
@media(min-width:600px) and (max-width:1199px){
 #dd-header{grid-template-areas:'brand rise' 'tools contacts' 'nav nav';grid-template-columns:minmax(0,1fr) auto;gap:0 20px;padding:6px var(--dd-gutter) 0;}
 #dd-header .dd-brand{width:224px;}
 #dd-header .dd-rise{justify-self:end;}
 #dd-header:not(.is-compact) .dd-header-tools{justify-self:start;justify-content:flex-start;gap:28px;min-height:44px;}
 #dd-header .dd-contact-strip{font-size:14px;column-gap:18px;}
 #dd-header .dd-contact-strip a:last-child{font-size:13px;}
}
#dd-header:not(.is-compact) #dd-navigation{justify-content:safe center;gap:clamp(18px,1.8vw,28px);overflow-x:auto;overscroll-behavior-x:contain;scrollbar-width:thin;scrollbar-color:#89927e #f0f1eb;}
#dd-header.has-nav-rail #dd-navigation{justify-content:flex-start;padding-bottom:8px;}
#dd-header.has-nav-rail #dd-navigation::after{content:'Swipe for more';display:flex;align-items:center;flex:none;font:11px/1.4 Arial,sans-serif;color:var(--dd-sage);padding-right:8px;}
@media(min-width:600px) and (max-width:1279px){#dd-navigation>a,#dd-navigation>.dd-group>a{font-size:13px;letter-spacing:.025em;}#dd-header .dd-panel a{min-height:44px;}}
'''
p.write_text(s,encoding='utf-8')
p=Path('assets/editorial-layout.css')
with p.open('a',encoding='utf-8') as f:f.write('''
/* Considerations reuses the editorial card palette, framing, and typography. */
html body.ss18 main#main#main#main#main .considerations-grid{display:grid!important;grid-template-columns:repeat(6,minmax(0,1fr));gap:24px;align-items:stretch;}
html body.ss18 main#main#main#main#main .consideration-card{grid-column:span 2;display:flex;flex-direction:column;min-width:0;margin:0;padding:0;border:3px solid #48533e;background:#fff;color:#343c32;text-decoration:none;box-shadow:none;transform:none;}
html body.ss18 main#main#main#main#main .consideration-card:nth-child(4){grid-column:2/span 2;}
html body.ss18 main#main#main#main#main .consideration-photo{display:block;position:relative;aspect-ratio:3/2;overflow:hidden;}
html body.ss18 main#main#main#main#main .consideration-photo img{position:absolute!important;inset:0!important;display:block!important;width:100%!important;max-width:none!important;height:100%!important;max-height:none!important;margin:0!important;padding:0!important;object-fit:cover!important;}
html body.ss18 main#main#main#main#main .consideration-card h2{margin:0;padding:18px 20px;border-top:2px solid #48533e;font:400 24px/1.35 Arial,sans-serif;text-align:center;color:#343c32;}
html body.ss18 main#main#main#main#main .consideration-card p{margin:0;padding:16px 20px;border-top:2px solid #48533e;font:400 16px/1.8 Arial,sans-serif;text-align:center;color:#343c32;}
html body.ss18 main#main#main#main#main .consideration-more{display:flex;justify-content:center;align-items:center;min-height:52px;margin-top:auto;padding:12px 20px;border-top:2px solid #48533e;font:500 12px/1.5 Arial,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#48533e;text-decoration:underline;text-underline-offset:5px;}
html body.ss18 main#main#main#main#main .consideration-card:hover{color:#343c32;background:#fff;box-shadow:none;transform:none;}
html body.ss18 main#main#main#main#main .consideration-card:focus-visible{outline:2px solid #48533e;outline-offset:4px;}
@media(min-width:601px) and (max-width:1100px){html body.ss18 main#main#main#main#main .considerations-grid{grid-template-columns:repeat(4,minmax(0,1fr));}html body.ss18 main#main#main#main#main .consideration-card:nth-child(4){grid-column:span 2;}html body.ss18 main#main#main#main#main .consideration-card:last-child{grid-column:2/span 2;}}
@media(max-width:600px){html body.ss18 main#main#main#main#main .considerations-grid{grid-template-columns:minmax(0,1fr);}html body.ss18 main#main#main#main#main .consideration-card,html body.ss18 main#main#main#main#main .consideration-card:nth-child(4){grid-column:auto;}}
''')
print('Updated shared responsive navigation and Considerations styles.')
