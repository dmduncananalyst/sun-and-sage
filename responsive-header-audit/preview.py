import sys,os,json,threading,functools,http.server
from pathlib import Path
sys.path.insert(0,os.path.join(os.environ['TEMP'],'dommydom-browser-tools-complete'))
from playwright.sync_api import sync_playwright
root=Path.cwd();out=root/'responsive-header-audit'
class Q(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
class S(http.server.ThreadingHTTPServer):
 request_queue_size=128
 def handle_error(self,*a):pass
s=S(('127.0.0.1',0),functools.partial(Q,directory=str(root)));threading.Thread(target=s.serve_forever,daemon=True).start();results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for touch,cases in [(False,[(1280,900),(1366,900),(1440,1000),(1920,1080)]),(True,[(320,720),(375,812),(390,844),(430,932),(650,900),(680,900),(768,1024),(900,1000),(1024,768)])]:
  ctx=b.new_context(viewport={'width':cases[0][0],'height':cases[0][1]},has_touch=touch,is_mobile=touch,device_scale_factor=1);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();errors=[];pg.on('pageerror',lambda e:errors.append(str(e)));pg.goto(f'http://127.0.0.1:{s.server_port}/index.html',wait_until='domcontentloaded');pg.evaluate('document.fonts.ready')
  for w,h in cases:
   pg.set_viewport_size({'width':w,'height':h});pg.wait_for_timeout(180);pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()');pg.mouse.move(0,h-1)
   d=pg.locator('#dd-header').evaluate('''h=>({compact:h.classList.contains('is-compact'),height:h.offsetHeight,overflow:document.documentElement.scrollWidth>innerWidth,contactVisible:!!h.querySelector('.dd-contact-strip').getClientRects().length,navVisible:!!h.querySelector('nav').getClientRects().length,children:[...h.children].map(e=>({class:e.className,rect:e.getBoundingClientRect().toJSON()}))})''');d.update(width=w,errors=list(errors));print(json.dumps(d),flush=True);results.append(d);pg.screenshot(path=str(out/f'{w}-closed.png'))
   if d['compact']:
    pg.locator('.dd-menu-toggle').tap();pg.screenshot(path=str(out/f'{w}-menu.png'));pg.locator('.dd-buyers>a').tap();pg.screenshot(path=str(out/f'{w}-buy.png'));pg.locator('.dd-menu-toggle').tap()
   else:
    for label,selector in [('buy','.dd-buyers'),('design','#dd-navigation>.dd-group:nth-of-type(4)'),('life','#dd-navigation>.dd-group:nth-of-type(5)'),('sell','#dd-navigation>.dd-group:nth-of-type(2)'),('management','#dd-navigation>.dd-group:nth-of-type(3)'),('contact','#dd-navigation>.dd-group:nth-of-type(6)')]:
     pg.locator(selector+'>a').hover();pg.screenshot(path=str(out/f'{w}-{label}.png'));pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()');pg.mouse.move(0,h-1)
   for label in ['neighborhoods','search']:
    a=pg.locator('.dd-'+label+'>button').first
    if touch:a.tap()
    else:a.hover()
    pg.screenshot(path=str(out/f'{w}-{label}.png'))
    if touch:pg.locator('.dd-'+label+' .dd-feature-close').tap()
    else:pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()');pg.mouse.move(0,h-1)
  ctx.close()
 b.close()
s.shutdown();(out/'preview-metrics.json').write_text(json.dumps(results,indent=2))
