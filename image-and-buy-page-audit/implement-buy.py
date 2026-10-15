from pathlib import Path
import re,math,json
from PIL import Image,ImageDraw
out=Path('image-and-buy-page-audit');p=Path('buy-a-home.html');s=p.read_text(encoding='utf-8');(out/'buy-before.html').write_text(s,encoding='utf-8')
# Convert the original map silhouettes into inline vector outlines; text is live HTML.
source=Image.open('assets/buy-with-dominique-reach-approved-clean.lossless.webp').convert('RGB')
boxes=[(65,425,435,710),(475,420,705,700),(780,450,1010,710),(1025,490,1360,700)]
def silhouette(box):
 im=source.crop(box);im.thumbnail((220,180));w,h=im.size;pix=im.load();mask={(x,y) for y in range(h) for x in range(w) if max(pix[x,y])-min(pix[x,y])>8 and 70<sum(pix[x,y])/3<180}
 # Fill holes (including lettering) using exterior flood fill.
 exterior=set();stack=[(x,y) for x in range(w) for y in [0,h-1]]+[(x,y) for y in range(h) for x in [0,w-1]]
 while stack:
  x,y=stack.pop()
  if (x,y) in mask or (x,y) in exterior or not(0<=x<w and 0<=y<h):continue
  exterior.add((x,y));stack.extend([(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
 filled={(x,y) for y in range(h) for x in range(w) if (x,y) not in exterior}
 # Compact horizontal runs form a resolution-independent vector silhouette.
 runs=[]
 for y in range(h):
  x=0
  while x<w:
   if (x,y) not in filled:x+=1;continue
   start=x
   while x<w and (x,y) in filled:x+=1
   runs.append(f'M{start} {y}h{x-start}v1H{start}z')
 return f'<svg viewBox="0 0 {w} {h}" aria-hidden="true" focusable="false"><path fill="currentColor" d="{"".join(runs)}"/></svg>'
icons={
'Budget':'<rect x="5" y="2" width="14" height="20" rx="1"/><path d="M8 6h8M8 11h1m3 0h1m3 0h1M8 15h1m3 0h1m3 0h1M8 19h1m3 0h1m3 0h1"/>',
'Preapproval':'<path d="M6 2h9l4 4v15H6zM14 2v5h5M9 11h6M9 15l2 2 5-5"/>',
'Wish List':'<path d="m2 11 10-9 10 9M5 9v13h14V9"/><path d="M12 17s-5-3-3-5c1-1 3 0 3 0s2-1 3 0c2 2-3 5-3 5z"/>',
'Neighborhoods':'<path d="M12 22s8-9 8-14a8 8 0 0 0-16 0c0 5 8 14 8 14z"/><circle cx="12" cy="8" r="2"/>',
'Tours':'<circle cx="12" cy="6" r="3"/><circle cx="4" cy="9" r="2"/><circle cx="20" cy="9" r="2"/><path d="M7 22v-7a5 5 0 0 1 10 0v7M1 22v-6a3 3 0 0 1 5-2m12 0a3 3 0 0 1 5 2v6"/>',
'Offer':'<path d="M5 2h12v6M5 2v20h12v-5M8 6h5M8 10h4m-1 7 8-8 3 3-8 8-4 1z"/>',
'Escrow':'<path d="m2 10 5-6 5 2 5-2 5 6-5 8-5 3-5-3zM7 4l5 5 4-2m-4 2-4 4 6 6M2 10l7 8m13-8-7 9"/>',
'Keys':'<circle cx="16" cy="7" r="5"/><path d="m12 11-10 10 3 1 2-3 3-1-1-3 5-5"/>'}
def icon(label):return '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'+icons[label]+'</svg>'
steps=[]
for i,label in enumerate(icons):
 angle=2*math.pi*i/8;left=50+41*math.sin(angle);top=50-41*math.cos(angle);steps.append(f'<li class="dd-buy-step" style="left:{left:.3f}%;top:{top:.3f}%">{icon(label)}<span>{label}</span></li>')
intro='Buying a home is a big step — and you don’t have to do it alone. Dominique guides you through each step of the process with local expertise and the support of Rise Real Estate, so you can move forward with confidence.'
benefits=[('Neighborhoods','Local Expertise','In-depth knowledge of our communities.'),('Tours','Clear Guidance','Straightforward advice at every step.'),('Wish List','Trusted Network','The strength of Rise Real Estate.')]
benefit=''.join('<article>'+icon(i)+'<div><h3>'+t+'</h3><p>'+d+'</p></div></article>' for i,t,d in benefits)
def chart(title,values,maximum):
 bars=''.join(f'<div class="dd-buy-bar"><strong>{value}</strong><span class="dd-buy-bar-fill" style="height:{num/maximum*100:.2f}%"></span><span class="dd-buy-bar-label">{label}</span></div>' for label,value,num in values)
 summary='; '.join(label+': '+value for label,value,num in values)
 return f'<figure class="dd-buy-chart" aria-label="{title}: {summary}"><figcaption>{title}</figcaption><div class="dd-buy-chart-plot"><div class="dd-buy-axis"><span>{maximum:,}</span><span>{maximum//2:,}</span><span>0</span></div><div class="dd-buy-bars">{bars}</div></div></figure>'
stats=chart('Rise Sales Activity',[('2023 Homes Sold','300+',300),('Sales Last 12 Months','404',404),('Total Sales','1,333',1333)],1400)+chart('Client Trust',[('Five-Star Reviews','600+',600),('Team Reviews','1,016',1016),('Average Price','$903K',903)],1200)
reach=[]
for box,value,name,desc in zip(boxes,['Thousands','HQ','#1','Local'],['','California','Los Angeles','San Fernando Valley'],['Families Assisted','Los Angeles Headquarters','Real Estate Team in Los Angeles','San Fernando Valley Buyer Guidance']):
 reach.append(f'<article><span class="dd-buy-map-name">{name}</span><div class="dd-buy-map">{silhouette(box)}<strong>{value}</strong></div><h3>{desc}</h3></article>')
main='''<main class="dd-buy-page" id="top"><section class="dd-buy-overview"><div class="dd-buy-intro"><span class="dd-buy-eyebrow">The Buying Process</span><h1>Buy With<br/><span>Dominique</span></h1><p class="dd-buy-subhead">Expert guidance. A brighter next chapter.</p><p>'''+intro+'''</p></div><div class="dd-buy-wheel"><div class="dd-buy-wheel-center"><span>A Smoother<br/>Path Home</span></div><ol>'''+''.join(steps)+'''</ol></div><div class="dd-buy-benefits">'''+benefit+'''</div></section><section class="dd-buy-statistics" aria-label="Rise sales activity and client trust">'''+stats+'''<div class="dd-buy-location"><span class="dd-buy-eyebrow">01</span><h2>Buy With<br/>Dominique</h2><p>San Fernando<br/>Valley +<br/>Los Angeles</p></div><p class="dd-buy-stat-footer">Local Expertise / Stronger Opportunities / A Brighter Tomorrow</p></section><section class="dd-buy-reach"><div class="dd-buy-reach-heading"><div><span class="dd-buy-eyebrow">04</span><h2>Rise Real Estate Reach</h2></div><p class="dd-buy-eyebrow">Backed by a broader network</p></div><div class="dd-buy-reach-grid">'''+''.join(reach)+'''</div></section><div class="ss49-button-row"><section class="bottom-cta"><h2>Ready to start your search?</h2><p>Work one-on-one with Dominique for clear guidance, local perspective, and a smoother buying experience from planning to keys.</p><a href="buyer-consultation.html">Buy With Dominique</a></section></div></main>'''
s=re.sub(r'<main\b.*?</main>',lambda m:main,s,count=1,flags=re.S);s=s.replace('</head>','<link rel="stylesheet" href="assets/buy-with-dominique.css"/>\n</head>',1);p.write_text(s,encoding='utf-8')
p=Path('assets/navigation-v22.js');s=p.read_text(encoding='utf-8');s=s.replace("const available=vw-16-Math.max(16,r.left);width=Math.min(width,vw-32);if(available>=220||g.matches('.dd-feature'))width=Math.min(width,Math.max(180,available));const left=Math.max(16,Math.min(r.left,vw-width-16));", "const centered=g.matches('.dd-neighborhoods')&&vw>=1200,available=vw-16-Math.max(16,r.left);width=Math.min(width,vw-32);if(!centered&&(available>=220||g.matches('.dd-feature')))width=Math.min(width,Math.max(180,available));const desired=centered?r.left+r.width/2-width/2:r.left,left=Math.max(16,Math.min(desired,vw-width-16));");p.write_text(s,encoding='utf-8');print('Rebuilt Buy page as live HTML/CSS/vector content; centered large-screen Neighborhoods.')
