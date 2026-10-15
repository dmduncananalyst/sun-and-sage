import sys,os,threading,functools,http.server,json
from pathlib import Path
sys.path.insert(0,os.path.join(os.environ['TEMP'],'dommydom-browser-tools-complete'))
from playwright.sync_api import sync_playwright
root=Path.cwd();out=root/'final-navigation-audit'
class Q(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Q,directory=str(root)));threading.Thread(target=s.serve_forever,daemon=True).start()
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h,t in [(1920,1080,False),(1440,1000,False),(1280,800,False),(1024,768,True),(820,1180,True),(768,1024,True),(600,900,True),(390,844,True),(320,720,True)]:
  c=b.new_context(viewport={'width':w,'height':h},has_touch=t,is_mobile=t);c.route('https://**/*',lambda r:r.abort());pg=c.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/index.html',wait_until='domcontentloaded');pg.evaluate('document.fonts.ready');pg.wait_for_timeout(350)
  print(w,pg.evaluate('''()=>{const h=document.querySelector('#ss22-header');return {compact:h.classList.contains('ss22-compact-nav'),height:h.offsetHeight,children:[...h.children].map(e=>({cls:e.className,rect:e.getBoundingClientRect().toJSON()})),overflow:document.documentElement.scrollWidth>innerWidth}}'''),flush=True)
  pg.screenshot(path=str(out/f'{w}-closed.png'))
  if pg.locator('#ss22-header').evaluate('e=>e.classList.contains("ss22-compact-nav")'):pg.locator('.ss22-menu-toggle').click();pg.screenshot(path=str(out/f'{w}-menu.png'));pg.locator('.ss22-buyers>a').click()
  elif t:pg.locator('.ss22-buyers>a').tap()
  else:pg.locator('.ss22-buyers>a').hover()
  pg.screenshot(path=str(out/f'{w}-buy.png'));c.close()
 b.close()
s.shutdown()
