import sys,os,json,threading,functools,http.server,re,html
from pathlib import Path
sys.path.insert(0,os.path.join(os.environ['TEMP'],'dommydom-browser-tools-complete'))
from playwright.sync_api import sync_playwright
root=Path.cwd();out=root/'navigation-audit'
class Q(http.server.SimpleHTTPRequestHandler):
 protocol_version='HTTP/1.1'
 def log_message(self,*a):pass
class S(http.server.ThreadingHTTPServer):
 request_queue_size=128
 def handle_error(self,*a):pass
s=S(('127.0.0.1',0),functools.partial(Q,directory=str(root)));threading.Thread(target=s.serve_forever,daemon=True).start();rs=[]
cases=[('desktop',1440,1000,False),('ipad-portrait',768,1024,True),('ipad-landscape',1024,768,True),('phone',390,844,True)]
if '--all' in sys.argv:cases=[('desktop-wide',1920,1080,False),('desktop',1440,1000,False),('laptop',1366,768,False),('small-laptop',1280,800,False),('ipad-portrait',768,1024,True),('ipad-air-portrait',820,1180,True),('ipad-landscape',1024,768,True),('ipad-air-landscape',1180,820,True),('ipad-pro-landscape',1366,1024,True),('phone',390,844,True),('phone-small',320,720,True)]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for path in (['blog/can-the-dodgers-do-a-threepeat-2026.html'] if '--variant' in sys.argv else ['buy-winnetka.html','blog.html','index.html'] if '--all' in sys.argv else ['buy-winnetka.html']):
  src=(root/path).read_text(encoding='utf-8');markup=re.search(r'<nav\b(?=[^>]*\bid="ss22-navigation")[^>]*>(.*?)</nav>',src,re.S)[1];expected=re.findall(r'<a\b[^>]*href="([^"]+)"',markup)
  for name,w,h,touch in cases:
   ctx=b.new_context(viewport={'width':w,'height':h},has_touch=touch,is_mobile=touch,device_scale_factor=1);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();errors=[];pg.on('pageerror',lambda e:errors.append(str(e)))
   pg.goto(f'http://127.0.0.1:{s.server_port}/'+path,wait_until='domcontentloaded');pg.wait_for_function('document.querySelector("link[href*=responsive-navigation]")?.sheet');pg.evaluate('document.fonts.ready');pg.wait_for_timeout(250)
   data=pg.evaluate('''()=>{const h=document.querySelector('#ss22-header'),n=h.querySelector('nav'),t=h.querySelector('.ss22-menu-toggle');return {compact:h.classList.contains('ss22-compact-nav'),toggleVisible:!!t.getClientRects().length,headerHeight:h.getBoundingClientRect().height,pageOverflow:document.documentElement.scrollWidth>innerWidth,links:[...n.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'))}}''');data.update(page=path,case=name,width=w,height=h);data['linksPreserved']=data.pop('links')==expected
   if data['compact']:
    start=pg.evaluate('scrollY');pg.locator('.ss22-menu-toggle').click();pg.wait_for_timeout(100)
    data.update(pg.evaluate('''()=>{const n=document.querySelector('#ss22-navigation'),g=n.querySelector('.ss22-menu-grid'),r=n.getBoundingClientRect(),h=document.querySelector('#ss22-header').getBoundingClientRect();return {columns:getComputedStyle(g).gridTemplateColumns.split(' ').length,navTop:r.top,headerBottom:h.bottom,navBottom:r.bottom,navOverflow:n.scrollWidth>n.clientWidth,panelVisible:!!n.getClientRects().length}}'''))
    if path=='buy-winnetka.html':pg.screenshot(path=str(out/(name+'-menu.png')))
    expanded=[]
    for group in pg.locator('#ss22-navigation .ss22-group').all():
     trigger=group.locator(':scope > button.ss22-top,:scope > a').first;trigger.click();panel=group.locator('.ss22-panel');expanded.append(panel.is_visible() and trigger.get_attribute('aria-expanded')=='true')
     if path=='buy-winnetka.html' and group.evaluate('g=>g.classList.contains("ss22-buyers")'):pg.screenshot(path=str(out/(name+'-buyers.png')))
     trigger.click()
    data['everyCategoryExpands']=all(expanded);data['allLinkTouchTargets']=pg.locator('#ss22-navigation .ss22-menu-column>a').evaluate_all('as=>as.every(a=>a.getBoundingClientRect().height>=44)')
    pg.keyboard.press('Escape');pg.wait_for_timeout(50);data['closed']=pg.locator('.ss22-menu-toggle').get_attribute('aria-expanded')=='false';data['scrollRestored']=pg.evaluate('scrollY')==start;data['focusReturned']=pg.locator('.ss22-menu-toggle').evaluate('e=>e===document.activeElement');data['bodyUnlocked']=pg.evaluate('getComputedStyle(document.body).overflow')!='hidden';data['mainRestored']=pg.locator('main').evaluate('m=>!m.inert')
   else:
    data['singleDesktopRow']=pg.locator('#ss22-navigation').evaluate('n=>{const rs=[...n.children].map(e=>(e.matches("a")?e:e.querySelector(":scope>a,:scope>button"))?.getBoundingClientRect()).filter(Boolean);return Math.max(...rs.map(r=>r.top))-Math.min(...rs.map(r=>r.top))<2&&n.scrollWidth<=n.clientWidth+1}')
    group=pg.locator('#ss22-navigation .ss22-group').first;group.hover();pg.wait_for_timeout(250);data['desktopDropdown']=group.locator('.ss22-panel').is_visible();pg.keyboard.press('Escape')
    if path=='buy-winnetka.html':pg.screenshot(path=str(out/(name+'-header.png')))
   data['errors']=errors;rs.append(data);print(json.dumps(data),flush=True);(out/('variant-results.json' if '--variant' in sys.argv else 'results.json' if '--all' in sys.argv else 'quick.json')).write_text(json.dumps(rs,indent=2));ctx.close()
 b.close()
s.shutdown()
