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
s=S(('127.0.0.1',0),functools.partial(Q,directory=str(root)));threading.Thread(target=s.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{s.server_port}/';results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h,touch in [(1440,1000,False),(1366,900,False),(1024,768,True),(768,1024,True),(390,844,True),(320,720,True)]:
  ctx=b.new_context(viewport={'width':w,'height':h},has_touch=touch,is_mobile=touch);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.goto(base+'life-changes/marriage/buying-a-home-together-when-one-spouse-already-owns-property.html',wait_until='domcontentloaded');pg.evaluate('document.fonts.ready');pg.wait_for_timeout(100);d={'width':w};compact=pg.locator('#dd-header').evaluate('e=>e.classList.contains("is-compact")')
  n=pg.locator('.dd-neighborhoods');nt=n.locator(':scope>button');np=n.locator('.dd-panel')
  if touch:nt.tap()
  else:nt.hover()
  d['firstHoverOrTapShowsCities']=np.is_visible();dest=np.locator('a').filter(has_text='Winnetka');dest.click();pg.wait_for_url('**/buy-winnetka.html');d['cityDirectFromNested']=pg.locator('h1').is_visible()
  st=pg.locator('.dd-search>button');sp=pg.locator('.dd-search>.dd-panel')
  if touch:st.tap()
  else:st.hover()
  d['firstHoverOrTapShowsSearch']=sp.is_visible();sp.locator('a').click();pg.wait_for_url('**/search.html');d['existingSearchWorks']=pg.locator('input[aria-label="Minimum price"]').is_visible() and pg.locator('select[name="city"]').is_visible()
  pg.goto(base+'index.html',wait_until='domcontentloaded');pg.evaluate('document.fonts.ready')
  if compact:
   if touch:pg.locator('.dd-menu-toggle').tap()
   else:pg.locator('.dd-menu-toggle').click()
  a=pg.locator('.dd-buyers>a')
  if touch or compact:a.click()
  else:a.hover()
  f=pg.locator('.dd-flyout').last
  if not compact:
   if touch:f.locator(':scope>a').tap()
   else:f.locator(':scope>a').hover()
  (f.locator(':scope>a') if compact else f.locator('.dd-flyout-panel>a').first).click();pg.wait_for_url('**/buyer-questions.html');d['formerBuyingRouteWorks']=pg.locator('h1').text_content().strip()=='Buying'
  pg.goto(base+'index.html',wait_until='domcontentloaded');pg.evaluate('document.fonts.ready')
  if touch or compact:
   n=pg.locator('.dd-neighborhoods');n.locator(':scope>button').click() if not touch else n.locator(':scope>button').tap();np=n.locator('.dd-panel');d['backgroundLocked']=pg.evaluate("getComputedStyle(document.body).overflow==='hidden'");start=pg.evaluate('scrollY');np.locator('a').last.scroll_into_view_if_needed();d['panelScrollDoesNotMovePage']=pg.evaluate('scrollY')==start
   pg.locator('.dd-search>button').tap();d['switchClosesPrevious']=not np.is_visible() and pg.locator('.dd-search>.dd-panel').is_visible();pg.keyboard.press('Escape');pg.wait_for_timeout(20);d['escapeRestoresFocus']=pg.locator('.dd-search>button').evaluate('e=>e===document.activeElement');d['scrollRestored']=pg.evaluate("getComputedStyle(document.body).overflow!=='hidden'&&!document.querySelector('main').inert")
   pg.locator('.dd-search>button').tap();pg.set_viewport_size({'width':1280,'height':800});pg.wait_for_timeout(100);d['resizeClosesAndUnlocks']=not pg.locator('.dd-search>.dd-panel').is_visible() and pg.evaluate("getComputedStyle(document.body).overflow!=='hidden'")
  else:
   pg.locator('.dd-search>button').focus();d['keyboardOpensSearch']=pg.locator('.dd-search>.dd-panel').is_visible();pg.keyboard.press('Escape');d['escapeClosesSearch']=not pg.locator('.dd-search>.dd-panel').is_visible();pg.locator('.dd-neighborhoods>button').focus();d['keyboardOpensCities']=pg.locator('.dd-neighborhoods>.dd-panel').is_visible();pg.keyboard.press('Escape');pg.locator('.dd-buyers>a').focus();pg.locator('.dd-flyout').first.locator(':scope>a').focus();d['keyboardOpensFlyout']=pg.locator('.dd-flyout').first.locator('.dd-flyout-panel').is_visible();pg.keyboard.press('Escape');d['flyoutEscapeReturnsFocus']=pg.locator('.dd-flyout').first.locator(':scope>a').evaluate('e=>e===document.activeElement');pg.keyboard.press('Escape');pg.locator('.dd-search>button').hover();pg.evaluate('window.scrollTo(0,250)');pg.wait_for_timeout(100);d['offscreenTriggerClosesDropdown']=not pg.locator('.dd-search>.dd-panel').is_visible();pg.evaluate('window.scrollTo(0,0)');pg.locator('.dd-buyers>a').click();pg.wait_for_url('**/buy-a-home.html#top');d['primaryBuyStillNavigates']=True
  d['passed']=all(v for k,v in d.items() if k!='width');results.append(d);(out/'interaction-results.json').write_text(json.dumps(results,indent=2));print(json.dumps(d),flush=True);ctx.close()
 b.close()
s.shutdown()
