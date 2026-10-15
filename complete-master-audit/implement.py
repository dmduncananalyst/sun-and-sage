from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import re,json
out=Path('complete-master-audit');rows=json.loads((out/'before-headers.json').read_text(encoding='utf-8'))
def update(r):
 p=Path(r['page']);s=p.read_bytes().decode('utf-8');h=r['header'];pat=r'<div class="dd-group"><a\b[^>]*href="([^"]*life-changes.html)"[^>]*>Life Changes</a><div class="dd-panel"><div class="dd-panel-content">.*?</div></div></div>'
 h,n=re.subn(pat,lambda m:'<a href="'+m[1]+'">Life Changes</a>',h,count=1,flags=re.S);assert n==1,r['page'];s=s.replace(r['header'],h,1);p.write_bytes(s.encode());return r['page']
with ThreadPoolExecutor(max_workers=8) as pool:changed=list(pool.map(update,rows))
p=Path('assets/navigation-v22.js');s=p.read_text(encoding='utf-8');a=s.index(' const centered=');b=s.index('\n p.style.setProperty',a);s=s[:a]+''' width=Math.min(width,vw-32);const desired=r.left+r.width/2-width/2,left=Math.max(16,Math.min(desired,vw-width-16));'''+s[b:];p.write_text(s,encoding='utf-8')
p=Path('assets/responsive-navigation.css');s=p.read_text(encoding='utf-8');s+='''
/* These ordinary page links have no disclosure treatment. */
#dd-navigation>a:is([href$="life-changes.html"],[href$="considerations.html"]):hover{text-decoration:none;}
''';p.write_text(s,encoding='utf-8')
imgdir=Path('assets/images/life-changes');imgdir.mkdir(parents=True,exist_ok=True)
mapping=[('Relocation','Relocation.png','relocation-family','life-changes/relocation.html','Younger family arriving in their new home with moving boxes'),('Empty Nest','empty-nest.png','empty-nest-dining-table','life-changes/empty-nest.html','Two adults sitting together at a large dining table surrounded by empty chairs'),('Retirement','Retirement.png','retirement-couple','life-changes/retirement.html','Older couple relaxing together at home beside a window'),('Divorce','Divorce.png','divorce-home','life-changes/divorce.html','Two adults taking time apart in a quiet living room'),('Death of a Loved One','death-of-a-loved-one.png','remembering-loved-one','life-changes/death.html','Couple comforting each other at home beside a family photograph')]
life=Path('life-changes.html');s=life.read_text(encoding='utf-8');photos=[]
for title,source,stem,url,alt in mapping:
 im=Image.open(source);dest=imgdir/(stem+'.webp');im.save(dest,'WEBP',lossless=True,method=6)
 found=[0]
 def card(m):
  article=m[0]
  if '<h2>'+title+'</h2>' not in article:return article
  found[0]+=1;tag=re.search(r'<img\b[^>]*>',article)[0];newtag=re.sub(r'src="[^"]*"','src="'+dest.as_posix()+'"',tag);newtag=re.sub(r'alt="[^"]*"','alt="'+alt+'"',newtag);newtag=re.sub(r'width="\d+"','width="'+str(im.width)+'"',newtag);newtag=re.sub(r'height="\d+"','height="'+str(im.height)+'"',newtag)
  return article.replace(tag,newtag,1)
 s=re.sub(r'<article class="loanHubItem">.*?</article>',card,s,flags=re.S);assert found[0]==1,title;photos.append({'title':title,'source':source,'image':dest.as_posix(),'url':url,'alt':alt,'dimensions':[im.width,im.height]})
life.write_text(s,encoding='utf-8');(out/'life-changes-photo-map.json').write_text(json.dumps(photos,indent=2),encoding='utf-8')
p=Path('complete-master-baseline.py');p.replace(out/'capture-baseline.py')
print('Life Changes is direct in',len(changed),'headers; all genuine dropdowns centered; five supplied photos applied losslessly.')
