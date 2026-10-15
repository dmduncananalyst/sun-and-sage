from pathlib import Path
import re,json,hashlib,shutil
from PIL import Image
out=Path('master-navigation-audit');paths=json.loads(Path('responsive-header-audit/changed-header-pages.json').read_text(encoding='utf-8-sig'))
before=json.loads((out/'before.json').read_text(encoding='utf-8'))
for row in before:
 p=Path(row['page']);s=p.read_bytes().decode('utf-8');h=row['header'];prefix='../'*len(Path(row['page']).parts[:-1])
 def link(file,label):return f'<a href="{prefix}{file}">{label}</a>'
 # Replace only the Buy panel with a modest set of actual direct destinations.
 start=h.index('<div class="dd-group dd-buyers">');end=h.index('<div class="dd-group">',start+20)
 buy='<div class="dd-group dd-buyers"><a class="dd-top" href="'+prefix+'buy-a-home.html#top" aria-haspopup="true" aria-expanded="false">Buy</a><div class="dd-panel"><div class="dd-panel-content">'+''.join(link(f,l) for f,l in [('buy-a-home.html#top','Buy With Dominique'),('first-time-buyers.html','First-Time Homebuyers'),('buyer-consultation.html','Buyer Consultation')])+'</div></div></div>'
 h=h[:start]+buy+h[end:]
 h=h.replace(link('blog.html','Blog'),link('considerations.html','Considerations')+link('blog.html','Blog'),1)
 pat=r'<a class="dd-search dd-feature-trigger" href="([^"]+)">(.*?)</a>'
 m=re.search(pat,h);assert m,row['page']
 search='<div class="dd-feature dd-search"><button class="dd-feature-trigger" type="button" aria-haspopup="true" aria-expanded="false">'+m[2]+'</button><div class="dd-panel"><div class="dd-panel-content"><a href="'+m[1]+'">Personalized Home Search</a></div></div></div>'
 h=h[:m.start()]+search+h[m.end():]
 p.write_bytes(s.replace(row['header'],h,1).encode('utf-8'))
# Preserve incoming originals and create named web assets.
imgdir=Path('assets/images/considerations');imgdir.mkdir(parents=True,exist_ok=True)
categories=[('Buying','buyer-questions.html',5,'family-viewing-home','Family exploring a bright living room together'),('Selling','seller-questions.html',4,'preparing-home','Woman reviewing materials in a furnished living room'),('Financing','homebuyer-financing-questions.html',1,'home-financing','Couple reviewing financial documents at home'),('Design','design-questions.html',2,'interior-design-planning','Couple considering interior plans and material samples'),('Rental Ownership','short-term-rental-questions.html',3,'rental-travel','Couple exploring a neighborhood while traveling')]
cards=[];mapping=[]
for title,url,num,stem,alt in categories:
 source=next(Path('.').glob(f'ChatGPT*-{num}.png'));image=Image.open(source).convert('RGB');image.thumbnail((1400,1400));dest=imgdir/(stem+'.webp');image.save(dest,'WEBP',quality=90,method=6)
 page=Path(url).read_text(encoding='utf-8');desc=re.search(r'<section class="loanHubHero[^>]*>.*?<p>(.*?)</p>',page,re.S)[1]
 cards.append(f'<a class="consideration-card" href="{url}"><span class="consideration-photo"><img src="{dest.as_posix()}" alt="{alt}" width="{image.width}" height="{image.height}" loading="{"eager" if num==5 else "lazy"}" decoding="async"/></span><h2>{title}</h2><p>{desc}</p><span class="consideration-more">Read More</span></a>')
 mapping.append({'title':title,'url':url,'description':desc,'source':source.name,'image':dest.as_posix(),'alt':alt})
s=Path('buyer-questions.html').read_text(encoding='utf-8')
s=re.sub(r'<main\b.*?</main>','<main class="loanHubPage v27-review considerations-page" id="main"><section class="loanHubHero v27-title-block"><h1>Considerations</h1></section><section class="loanHubGridWrap full-card-panel" aria-label="Considerations categories"><div class="considerations-grid">'+''.join(cards)+'</div></section></main>',s,count=1,flags=re.S)
s=s.replace('https://dommydom.com/buyer-questions.html','https://dommydom.com/considerations.html')
s=re.sub(r'<title>.*?</title>','<title>Dominique Duncan-Nelson | Considerations</title>',s,count=1,flags=re.S)
description='Explore buying, selling, financing, design, and rental ownership with Dominique Duncan-Nelson.'
s=re.sub(r'(<meta\b[^>]*content=")[^"]*("[^>]*(?:name="description"|property="og:description"|name="twitter:description")[^>]*>)',lambda m:m[1]+description+m[2],s)
s=s.replace('Dominique Duncan-Nelson | Buying','Dominique Duncan-Nelson | Considerations')
# Update WebPage structured metadata without touching other schema types.
def schema(m):
 try:d=json.loads(m[1])
 except:return m[0]
 if d.get('@type')=='WebPage':d.update(name='Dominique Duncan-Nelson | Considerations',description=description,url='https://dommydom.com/considerations.html')
 return '<script type="application/ld+json">'+json.dumps(d,ensure_ascii=False)+'</script>'
s=re.sub(r'<script type="application/ld\+json">(.*?)</script>',schema,s,flags=re.S)
Path('considerations.html').write_text(s,encoding='utf-8')
p=Path('sitemap.xml');s=p.read_text(encoding='utf-8');assert 'https://dommydom.com/considerations.html' not in s;s=s.replace('</urlset>','<url><loc>https://dommydom.com/considerations.html</loc></url>\n</urlset>');p.write_text(s,encoding='utf-8')
(out/'category-photo-map.json').write_text(json.dumps(mapping,indent=2),encoding='utf-8')
print('Updated',len(paths),'headers; created Considerations, five optimized photos, and sitemap entry.')
