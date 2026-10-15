import sys,os,json,threading,functools,http.server
from pathlib import Path
sys.path.insert(0,os.path.join(os.environ['TEMP'],'dommydom-browser-tools-complete'))
from playwright.sync_api import sync_playwright
root=Path.cwd();out=root/'final-navigation-audit'
class Q(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
class S(http.server.ThreadingHTTPServer):
 request_queue_size=128
 def handle_error(self,*a):pass
s=S(('127.0.0.1',0),functools.partial(Q,directory=str(root)));threading.Thread(target=s.serve_forever,daemon=True).start()
cases=[(1920,1080,False),(1440,1000,False),(1280,800,False),(1024,768,True),(820,1180,True),(768,1024,True),(600,900,True),(390,844,True),(320,720,True)]
pages=['index.html','buy-winnetka.html','sell-a-home.html','life-changes/marriage.html','buyer-questions.html','blog/can-the-dodgers-do-a-threepeat-2026.html'];results=[]
labels=['Home','About','Buy','Sell','Property Management','Interior Design','Life Changes','Blog','Contact']
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for path in pages:
  for w,h,touch in cases:
   ctx=b.new_context(viewport={'width':w,'height':h},has_touch=touch,is_mobile=touch,device_scale_factor=1);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();errors=[];pg.on('pageerror',lambda e:errors.append(str(e)))
   pg.goto(f'http://127.0.0.1:{s.server_port}/'+path,wait_until='domcontentloaded');pg.wait_for_function('document.querySelector("link[data-dommydom-navigation]")?.sheet');pg.evaluate('document.fonts.ready');pg.wait_for_timeout(80)
   d=pg.evaluate('''()=>{const h=document.querySelector('#ss22-header'),n=h.querySelector('nav'),s=h.querySelector('.ss22-header-search'),b=h.querySelector('.ss22-brand'),sr=s.getBoundingClientRect(),br=b.getBoundingClientRect();const links=[...n.children].filter(e=>!e.matches('button')).map(e=>e.matches('a')?e:e.querySelector(':scope>a'));return {compact:h.classList.contains('ss22-compact-nav'),labels:links.map(a=>a.textContent.trim()),noPageOverflow:document.documentElement.scrollWidth<=innerWidth,searchSeparate:!n.contains(s)&&s.textContent.trim()==='Search'&&!!s.querySelector('svg'),searchAligned:sr.left>=br.right&&sr.top<br.bottom&&sr.bottom>br.top,searchTouchTarget:sr.height>=44,headerHeight:h.offsetHeight,singleRow:links.every(a=>Math.abs(a.getBoundingClientRect().top-links[0].getBoundingClientRect().top)<2),readableFont:links.every(a=>parseFloat(getComputedStyle(a).fontSize)>=12),noIndicators:links.every(a=>['::before','::after'].every(p=>['none','normal','""'].includes(getComputedStyle(a,p).content)))}}''');d.update(page=path,width=w);d['exactLabels']=d.pop('labels')==labels
   if path=='index.html':pg.screenshot(path=str(out/f'{w}-closed.png'))
   if d['compact']:
    pg.locator('.ss22-menu-toggle').click();d['bodyLocked']=pg.evaluate("getComputedStyle(document.body).overflow==='hidden'")
    d['singleFlow']=pg.locator('#ss22-navigation').evaluate('''n=>{const rs=[...n.children].filter(e=>e.matches('a,.ss22-group')).map(e=>e.getBoundingClientRect());return rs.every((r,i)=>r.height>=44&&(!i||r.top>=rs[i-1].bottom-1))}''')
    if path=='index.html':pg.screenshot(path=str(out/f'{w}-menu.png'))
   allopen=[];transfer=[]
   for group in pg.locator('#ss22-navigation>.ss22-group').all():
    a=group.locator(':scope>a');panel=group.locator('.ss22-panel')
    if touch:a.tap()
    else:a.hover()
    allopen.append(panel.is_visible() and a.get_attribute('aria-expanded')=='true')
    if not touch:
     panel.locator('a').first.hover();pg.wait_for_timeout(20);transfer.append(panel.is_visible())
    if path=='index.html' and group.evaluate('e=>e.classList.contains("ss22-buyers")'):pg.screenshot(path=str(out/f'{w}-buy.png'))
    if d['compact']:
     if group.evaluate('e=>e.classList.contains("ss22-buyers")'):d['submenuScrolls']=pg.locator('#ss22-navigation').evaluate('n=>n.scrollHeight>n.clientHeight||n.getBoundingClientRect().bottom<=innerHeight')
     pg.locator('.ss22-nav-back').click()
    else:pg.keyboard.press('Escape')
   d['everySubmenuOpens']=all(allopen);d['hoverTransfer']=all(transfer)
   if d['compact']:
    pg.keyboard.press('Escape');pg.wait_for_timeout(20);d['closedAndUnlocked']=pg.locator('.ss22-menu-toggle').get_attribute('aria-expanded')=='false' and pg.evaluate("getComputedStyle(document.body).overflow!=='hidden'");d['focusReturned']=pg.locator('.ss22-menu-toggle').evaluate('e=>e===document.activeElement');d['inertRestored']=pg.locator('main').evaluate('e=>!e.inert')
   d['errors']=errors
   required=['exactLabels','noPageOverflow','searchSeparate','searchAligned','searchTouchTarget','noIndicators','everySubmenuOpens','hoverTransfer']+(['bodyLocked','singleFlow','closedAndUnlocked','focusReturned','inertRestored','submenuScrolls'] if d['compact'] else ['singleRow','readableFont'])
   d['failures']=[k for k in required if not d.get(k)];results.append(d);print(json.dumps(d),flush=True);(out/'browser-results.json').write_text(json.dumps(results,indent=2));ctx.close()
 b.close()
s.shutdown()
