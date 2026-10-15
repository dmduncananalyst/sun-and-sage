import sys,os,json,threading,http.server,functools,hashlib
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
s=S(('127.0.0.1',0),functools.partial(Q,directory=str(root)));threading.Thread(target=s.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{s.server_port}/';checks={}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True);ctx=b.new_context(viewport={'width':768,'height':1024},is_mobile=True,has_touch=True);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.goto(base+'buy-winnetka.html',wait_until='load');pg.wait_for_function('document.querySelector("link[href*=responsive-navigation]")?.sheet')
 toggle=pg.locator('.ss22-menu-toggle');toggle.click();toggle.focus();pg.keyboard.press('Shift+Tab');checks['focusWrapsBack']=pg.locator('#ss22-navigation .ss22-menu-column').last.locator(':scope>.ss22-group').last.locator('button.ss22-top').evaluate('e=>e===document.activeElement');pg.keyboard.press('Tab');checks['focusWrapsForward']=toggle.evaluate('e=>e===document.activeElement')
 pg.locator('.ss22-menu-backdrop').click(position={'x':2,'y':600});checks['outsideClickCloses']=toggle.get_attribute('aria-expanded')=='false';checks['outsideRestoresFocus']=toggle.evaluate('e=>e===document.activeElement')
 pg.evaluate('scrollTo({top:90,behavior:"instant"})');pg.wait_for_timeout(100);toggle.click();pg.wait_for_timeout(100);before=pg.evaluate('scrollY');checks['openBodyOverflow']=pg.evaluate('getComputedStyle(document.body).overflow');pg.mouse.wheel(0,500);pg.wait_for_timeout(150);checks['pageDoesNotScrollBehindMenu']=pg.evaluate('scrollY')==before
 pg.set_viewport_size({'width':1024,'height':768});pg.wait_for_timeout(150);checks['rotationClearsOpenState']=toggle.get_attribute('aria-expanded')=='false' and pg.evaluate('getComputedStyle(document.body).overflow')!='hidden'
 toggle.click();pg.locator('.ss22-buyers > button.ss22-top').click();links=pg.locator('.ss22-buyers .ss22-panel a');checks['submenuTouchTargets']=links.evaluate_all('as=>as.every(a=>a.getBoundingClientRect().height>=44)');link=pg.locator('.ss22-buyers a[href="buy-sun-valley.html"]');link.focus();link.press('Enter');pg.wait_for_url('**/buy-sun-valley.html');checks['submenuLinkNavigates']=pg.locator('main[data-city-page="Sun Valley"]').count()==1
 pg.wait_for_function('document.querySelector("link[href*=responsive-navigation]")?.sheet');checks['destinationMenuClosed']=pg.locator('.ss22-menu-toggle').get_attribute('aria-expanded')=='false';pg.locator('.cityHeroAction').click();checks['chatStillOpens']=pg.locator('#sun-conversation').is_visible();pg.locator('.sunConversation__close').click()
 for w,h,name in [(1366,1024,'ipad-pro-landscape'),(1280,800,'small-laptop')]:
  pg.set_viewport_size({'width':w,'height':h});pg.goto(base+'buy-winnetka.html',wait_until='load');pg.wait_for_function('document.querySelector("link[href*=responsive-navigation]")?.sheet');pg.locator('.ss22-menu-toggle').click();pg.screenshot(path=str(out/(name+'-menu.png')));checks[name+'-brandingFits']=pg.evaluate('()=>{const h=document.querySelector("#ss22-header"),b=h.querySelector(".ss22-brand").getBoundingClientRect(),r=h.querySelector(".ss22-rise").getBoundingClientRect(),t=h.querySelector(".ss22-menu-toggle").getBoundingClientRect();return b.right<r.left&&r.right<t.left&&t.right<=innerWidth;}')
 pg.close();ctx.close();b.close()
manifest=json.loads((out/'html-before.json').read_text());changed=[p for p,d in manifest.items() if hashlib.sha256((root/p).read_bytes()).hexdigest()!=d];checks['allHTMLUnchanged']=not changed;checks['htmlCount']=len(manifest)
(out/'interaction-checks.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2));s.shutdown()
