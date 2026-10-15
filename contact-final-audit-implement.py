from pathlib import Path
import re,json
out=Path('contact-final-audit');out.mkdir(exist_ok=True)
for n in ['contact.html','considerations.html','assets/editorial-layout.css','assets/navigation-v22.js','assets/responsive-navigation.css']:
 q=out/('before-'+Path(n).name);q.write_bytes(Path(n).read_bytes())
paths=json.loads(Path('responsive-header-audit/changed-header-pages.json').read_text(encoding='utf-8-sig'))+['considerations.html']
for name in dict.fromkeys(paths):
 p=Path(name);s=p.read_bytes().decode('utf-8')
 s,n=re.subn(r'(<div class="dd-group"><a class="dd-top" href="[^"]*interior-design.html"[^>]*>Interior Design</a><div class="dd-panel"><div class="dd-panel-content">)([\s\S]*?)(</div></div></div>)',lambda m:m[1]+re.sub(r'<a[^>]*>Design</a>','',m[2])+m[3],s);assert n==1,name
 s,n=re.subn(r'<div class="dd-group"><a class="dd-top" href="([^"]*contact.html)"[^>]*>Contact</a><div class="dd-panel"><div class="dd-panel-content">[\s\S]*?</div></div></div>',r'<div class="dd-group dd-contact"><a class="dd-top" href="\1" aria-haspopup="true" aria-expanded="false">Contact</a><div class="dd-panel"><div class="dd-panel-content"><a href="\1">Contact</a><a href="reviews.html">Reviews</a></div></div></div>',s);assert n==1,name
 p.write_bytes(s.encode('utf-8'))
p=Path('contact.html');s=p.read_bytes().decode('utf-8');cards=[]
for title,button,page in [('Free Home Evaluation','Request Free Evaluation','sell-free-home-valuation.html'),('Buyer Consultation','Schedule Consultation','buyer-consultation.html'),('Seller Consultation','Schedule Consultation','seller-consultation.html')]:
 source=Path(page).read_text(encoding='utf-8');main=re.search(r'<main\b[\s\S]*?</main>',source)[0];img=re.search(r'<img[^>]+>',main)[0];src=re.search(r'src="([^"]+)"',img)[1];alt=re.search(r'alt="([^"]+)"',img)[1]
 cards.append(f'<a class="consideration-card" href="{page}"><span class="consideration-photo"><img src="{src}" alt="{alt}" width="1400" height="933" loading="eager" decoding="async"/></span><h2>{title.upper()}</h2><span class="consideration-more">{button}</span></a>')
s=re.sub(r'(<main\b[^>]*>)',lambda m:m[1]+'<section class="dd-contact-cards" aria-label="Contact services"><div class="considerations-grid">'+''.join(cards)+'</div></section>',s,count=1)
if 'href="assets/editorial-layout.css' not in s:s=s.replace('</head>','<link rel="stylesheet" href="assets/editorial-layout.css"/></head>')
p.write_bytes(s.encode('utf-8'))
p=Path('assets/editorial-layout.css');s=p.read_text(encoding='utf-8');s+='''
/* Keep the Selling portrait's head inside the established landscape frame. */
html body.ss18 main#main#main#main#main.considerations-page .consideration-card[href="seller-questions.html"] img{object-position:center top!important;}
/* Contact cards reuse the established editorial card component above the existing page. */
html body.ss18 main#main#main#main#main.final-contact .dd-contact-cards{width:100%;max-width:1448px;margin:0 auto;padding:40px 24px 24px;}
html body.ss18 main#main#main#main#main.final-contact .consideration-card h2{font-size:21px!important;}
html body.ss18 main#main#main#main#main.final-contact .consideration-photo img{object-position:center top!important;}
@media(min-width:601px) and (max-width:1100px){html body.ss18 main#main#main#main#main.final-contact .consideration-card:last-child{grid-column:2/span 2;}}
''';p.write_text(s,encoding='utf-8')
p=Path('assets/navigation-v22.js');s=p.read_text(encoding='utf-8');s=s.replace('if(primary.includes(g)){','if(primary.includes(g)&&!g.matches(".dd-contact")){',1);p.write_text(s,encoding='utf-8')
p=Path('assets/responsive-navigation.css');s=p.read_text(encoding='utf-8');s+='''
/* Contact has two compact destinations, centered beneath its own label. */
#dd-header:not(.is-compact) #dd-navigation>.dd-contact>.dd-panel{left:var(--dd-panel-left);width:var(--dd-panel-width);max-width:calc(100vw - 32px);padding:12px 20px;}
#dd-header:not(.is-compact) #dd-navigation>.dd-contact>.dd-panel>.dd-panel-content{width:100%;margin:0;}
#dd-header:not(.is-compact) #dd-navigation>.dd-contact>.dd-panel a{justify-content:center;text-align:center;}
''';p.write_text(s,encoding='utf-8');print('Updated navigation on',len(set(paths)),'pages; added exact-source Contact cards and top-aligned Selling image.')
