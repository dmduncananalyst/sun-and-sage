exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'footer-consistency-audit'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in [390,768,1440]:
  pg=b.new_page(viewport={'width':w,'height':1000});pg.route('https://**/*',lambda r:r.abort());reference=None
  for n in ['index.html','buyer-consultation.html','seller-consultation.html','contact.html','interior-design.html','blog.html','life-changes/marriage.html','portfolio.html']:
   pg.goto(f'http://127.0.0.1:{s.server_port}/{n}',wait_until='domcontentloaded');pg.evaluate('document.documentElement.style.scrollBehavior="auto"');f=pg.locator('#dd-site-footer');f.scroll_into_view_if_needed();pg.wait_for_timeout(70)
   d=f.evaluate('e=>{let g=e.querySelector(".footerGrid"),c=e.querySelector(".cityLinks"),l=e.querySelector(".legal");return [getComputedStyle(e).backgroundColor,e.offsetHeight,g.offsetHeight,getComputedStyle(g).gridTemplateColumns,c.offsetHeight,l.offsetHeight]}')
   if reference is None:reference=d;print('REFERENCE',w,pg.locator('#dd-site-footer .legal').evaluate('e=>({height:getComputedStyle(e).height,min:getComputedStyle(e).minHeight,padding:getComputedStyle(e).padding,children:[...e.children].map(c=>[c.tagName,c.offsetWidth,c.offsetHeight])})'),flush=True)
   
   if d!=reference: print(n,pg.locator("#dd-site-footer .legal>*").evaluate_all("es=>es.map(e=>({tag:e.tagName,cls:e.className,w:e.offsetWidth,h:e.offsetHeight,margin:getComputedStyle(e).margin,padding:getComputedStyle(e).padding,display:getComputedStyle(e).display,flex:getComputedStyle(e).flex}))"),flush=True)
   assert d==reference,(w,n,reference,d)
   assert f.locator('.cityLinks a').count()==26;assert f.locator('img').evaluate_all('es=>es.every(e=>e.complete&&e.naturalWidth>0)');assert not pg.evaluate('document.documentElement.scrollWidth>innerWidth')
   if n in ['index.html','seller-consultation.html']:f.screenshot(path=str(out/f'{w}-{n[:-5]}.png'))
  print('Matched eight page layouts at',w,flush=True);pg.close()
 b.close()
s.shutdown()
