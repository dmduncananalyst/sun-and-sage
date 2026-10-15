from pathlib import Path
import re,json
out=Path('interior-design-final-audit');out.mkdir(exist_ok=True)
for n in ['interior-design.html','assets/navigation-v22.js','assets/responsive-navigation.css']: (out/('before-'+Path(n).name)).write_bytes(Path(n).read_bytes())
paths=json.loads(Path('responsive-header-audit/changed-header-pages.json').read_text(encoding='utf-8-sig'))+['considerations.html']
for name in dict.fromkeys(paths):
 p=Path(name);s=p.read_bytes().decode('utf-8');pat=r'<div class="dd-group"><a class="dd-top" href="([^"]*interior-design.html)"[^>]*>Interior Design</a><div class="dd-panel"><div class="dd-panel-content">[\s\S]*?</div></div></div>'
 s,n=re.subn(pat,r'<div class="dd-group dd-interior"><a class="dd-top" href="\1" aria-haspopup="true" aria-expanded="false">Interior Design</a><div class="dd-panel"><div class="dd-panel-content"><a href="\1">Interior Design</a><a href="portfolio.html">Portfolio</a></div></div></div>',s);assert n==1,name;p.write_bytes(s.encode('utf-8'))
p=Path('assets/navigation-v22.js');s=p.read_text(encoding='utf-8').replace('!g.matches(".dd-contact")','!g.matches(".dd-contact,.dd-interior")');p.write_text(s,encoding='utf-8')
p=Path('assets/responsive-navigation.css');s=p.read_text(encoding='utf-8');s+='''
/* Interior Design shares the compact, centered two-link disclosure. */
#dd-header:not(.is-compact) #dd-navigation>.dd-interior>.dd-panel{left:var(--dd-panel-left);width:var(--dd-panel-width);max-width:calc(100vw - 32px);padding:12px 20px;}
#dd-header:not(.is-compact) #dd-navigation>.dd-interior>.dd-panel>.dd-panel-content{width:100%;margin:0;}
#dd-header:not(.is-compact) #dd-navigation>.dd-interior>.dd-panel a{justify-content:center;text-align:center;}
''';p.write_text(s,encoding='utf-8')
p=Path('interior-design.html');s=p.read_bytes().decode('utf-8');cards=[]
for key,title in [('residential','Residential Design'),('commercial','Commercial Design')]:
 section=re.search(r'<section[^>]*id="'+key+r'"[\s\S]*?</section>',s)[0];img=re.search(r'<img[^>]+>',section)[0];src=re.search(r'src="([^"]+)"',img)[1];alt=re.search(r'alt="([^"]+)"',img)[1]
 cards.append(f'<a class="dd-design-card" href="{key}-design.html"><span class="dd-design-card-photo"><img src="{src}" alt="{alt}" width="1400" height="933" decoding="async"/></span><h2>{title}</h2><span class="dd-design-card-link">Explore {title}</span></a>')
section='<section class="dd-design-paths" aria-label="Explore design services">'+''.join(cards)+'</section>'
s=s.replace('<nav aria-label="Interior Design sections"',section+'\n<nav aria-label="Interior Design sections"',1)
portfolio=Path('portfolio.html').read_text(encoding='utf-8');projects=re.findall(r'<a class="portfolioParentCard"[\s\S]*?</a>',portfolio)[:3];tiles=[]
for project in projects:
 href=re.search(r'href="([^"]+)"',project)[1];src=re.search(r'<img[^>]+src="([^"]+)"',project)[1];name=re.search(r'<span class="ddn-portfolio-name">([^<]+)',project)[1]
 tiles.append(f'<a class="dd-design-project" href="{href}"><figure><img src="{src}" alt="{name}" loading="lazy" decoding="async"/></figure><span class="dd-design-project-caption"><span>{name}</span><span class="dd-design-project-action">View Project <span aria-hidden="true">?</span></span></span></a>')
preview='<section class="dd-design-portfolio" aria-labelledby="dd-design-portfolio-title"><header><h2 id="dd-design-portfolio-title">Portfolio</h2><a href="portfolio.html" class="dd-design-view-all">View Portfolio <span aria-hidden="true">?</span></a></header><div class="dd-design-editorial">'+''.join(tiles)+'</div></section>'
s=s.replace('<section aria-labelledby="design-action-title"',preview+'\n<section aria-labelledby="design-action-title"',1)
s=s.replace('</head>','<link rel="stylesheet" href="assets/interior-design-preview.css"/></head>');p.write_bytes(s.encode('utf-8'))
css='''/* Interior Design additions, isolated from all existing sections. */
html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-paths{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px;max-width:1280px;margin:32px auto;padding:0 32px;}
html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-card{display:flex;flex-direction:column;min-width:0;border:3px solid #48533e;background:#fff;text-decoration:none;box-shadow:none;transform:none;}
html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-card-photo{display:block;aspect-ratio:3/2;overflow:hidden;}
html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-card img{display:block!important;position:static!important;width:100%!important;height:100%!important;max-height:none!important;object-fit:cover!important;margin:0!important;}
html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-card h2{font:400 24px/1.35 Arial!important;margin:0!important;padding:18px 16px!important;border-top:2px solid #48533e;}
html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-card-link{display:block;padding:16px;text-align:center;border-top:2px solid #48533e;font:500 12px/1.5 Arial;letter-spacing:.08em;text-transform:uppercase;text-decoration:underline;text-underline-offset:5px;}
html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-portfolio{max-width:1280px;margin:40px auto;padding:32px;background:#f4f1eb;border-top:1px solid #c8c3b7;border-bottom:1px solid #c8c3b7;}
html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-portfolio>header{display:flex;align-items:center;justify-content:space-between;gap:24px;margin-bottom:24px;}
html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-portfolio h2{font:400 clamp(30px,3vw,44px)/1.2 Arial!important;text-align:left!important;margin:0!important;}
html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-view-all{font:500 13px/1.5 Arial;letter-spacing:.06em;text-decoration:underline;text-underline-offset:6px;white-space:nowrap;}
html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-editorial{display:grid;grid-template-columns:1.5fr 1fr;grid-template-rows:repeat(2,minmax(0,1fr));gap:24px 32px;}
html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-project{display:flex;flex-direction:column;min-width:0;color:#343c32;text-decoration:none;background:transparent;box-shadow:none;transform:none;}
html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-project:first-child{grid-row:span 2;}
html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-project figure{position:relative;flex:1;min-height:0;aspect-ratio:2/1;margin:0!important;overflow:hidden;}
html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-project:first-child figure{aspect-ratio:auto;}
html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-project img{position:absolute!important;inset:0!important;display:block!important;width:100%!important;height:100%!important;max-height:none!important;object-fit:cover!important;object-position:center!important;margin:0!important;}
html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-project-caption{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:14px 0 0;font:400 20px/1.35 Arial;}
html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-project-action{font:500 11px/1.5 Arial;letter-spacing:.05em;white-space:nowrap;text-decoration:underline;text-underline-offset:4px;}
html:root body.ss18 main#main#main.interior-overview-v43 :is(.dd-design-card,.dd-design-project,.dd-design-view-all):focus-visible{outline:2px solid #68705e;outline-offset:5px;}
@media(max-width:800px){html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-editorial{grid-template-columns:1fr 1fr;grid-template-rows:auto auto;gap:24px;}html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-project:first-child{grid-column:span 2;grid-row:auto;}html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-project:first-child figure{aspect-ratio:3/2;}html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-project figure{aspect-ratio:3/2;}html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-project-caption{display:block;font-size:18px;}html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-project-action{display:block;margin-top:8px;}}
@media(max-width:600px){html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-paths{grid-template-columns:1fr;gap:24px;padding:0 20px;margin:24px auto;}html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-portfolio{padding:24px 20px;margin:24px 0;}html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-editorial{gap:20px 16px;}html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-project:not(:first-child) .dd-design-project-caption{font-size:16px;}html:root body.ss18 main#main#main.interior-overview-v43 .dd-design-portfolio>header{gap:12px;}}
'''
Path('assets/interior-design-preview.css').write_text(css,encoding='utf-8');print('Implemented Interior Design cards, authentic project preview, and two-link centered dropdown across 352 headers.')
