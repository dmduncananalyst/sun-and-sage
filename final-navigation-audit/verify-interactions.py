import sys,os,json,threading,functools,http.server
from pathlib import Path
sys.path.insert(0,os.path.join(os.environ['TEMP'],'dommydom-browser-tools-complete'))
from playwright.sync_api import sync_playwright
root=Path.cwd();out=root/'final-navigation-audit'
class Q(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Q,directory=str(root)));threading.Thread(target=s.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{s.server_port}/';results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h,t in [(1440,1000,False),(1024,768,True),(768,1024,True),(390,844,True)]:
  ctx=b.new_context(viewport={'width':w,'height':h},has_touch=t,is_mobile=t);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.goto(base+'blog/can-the-dodgers-do-a-threepeat-2026.html',wait_until='domcontentloaded');pg.evaluate('document.fonts.ready');d={'width':w}
  pg.locator('.ss22-header-search').click();pg.wait_for_url('**/search.html');d['searchPageWorks']=pg.locator('input[aria-label="Minimum price"]').is_visible() and pg.locator('input[aria-label="Maximum price"]').is_visible()
  pg.goto(base+'index.html',wait_until='domcontentloaded');pg.evaluate('document.fonts.ready');compact=pg.locator('#ss22-header').evaluate('e=>e.classList.contains("ss22-compact-nav")')
  if compact:pg.locator('.ss22-menu-toggle').click()
  if t:pg.locator('.ss22-buyers>a').tap()
  else:pg.locator('.ss22-buyers>a').hover()
  pg.locator('.ss22-buyers .ss22-panel a').get_by_text('Buying',exact=True).click();pg.wait_for_url('**/buyer-questions.html');d['formerBuyingReachable']=pg.locator('h1').inner_text().strip()=='Buying'
  if compact:
   pg.locator('.ss22-menu-toggle').click();pg.keyboard.press('Shift+Tab');d['focusTrapBack']=pg.locator('.ss22-header-search').evaluate('e=>e===document.activeElement');pg.keyboard.press('Tab');d['focusTrapForward']=pg.locator('.ss22-menu-toggle').evaluate('e=>e===document.activeElement')
   pg.locator('.ss22-menu-backdrop').click(position={'x':5,'y':max(5,h-pg.locator('#ss22-header').bounding_box()['height']-10)});d['backdropCloses']=pg.locator('.ss22-menu-toggle').get_attribute('aria-expanded')=='false'
   pg.locator('.ss22-menu-toggle').click();start=pg.evaluate('scrollY');pg.mouse.wheel(0,500);pg.wait_for_timeout(100);d['backgroundDoesNotScroll']=pg.evaluate('scrollY')==start
   pg.set_viewport_size({'width':1440,'height':1000});pg.wait_for_timeout(100);d['resizeUnlocks']=pg.evaluate("getComputedStyle(document.body).overflow!=='hidden'&&!document.querySelector('#ss22-header').classList.contains('menu-is-open')")
  else:
   a=pg.locator('.ss22-buyers>a');a.focus();d['keyboardFocusOpens']=pg.locator('.ss22-buyers .ss22-panel').is_visible();pg.keyboard.press('Escape');d['escapeCloses']=not pg.locator('.ss22-buyers .ss22-panel').is_visible()
   pg.locator('.ss22-buyers>a').click();pg.wait_for_url('**/buy-a-home.html#top');d['primaryCategoryNavigates']=True
  d['passed']=all(v for k,v in d.items() if k!='width');results.append(d);print(json.dumps(d),flush=True);ctx.close()
 b.close()
s.shutdown();(out/'interaction-results.json').write_text(json.dumps(results,indent=2))
