import sys,os,json,threading,functools,http.server
from pathlib import Path
sys.path.insert(0,os.path.join(os.environ['TEMP'],'dommydom-browser-tools-complete'))
from playwright.sync_api import sync_playwright
root=Path.cwd();out=root/'header-hover-audit'
class Q(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
class S(http.server.ThreadingHTTPServer):
 request_queue_size=128
 def handle_error(self,*a):pass
s=S(('127.0.0.1',0),functools.partial(Q,directory=str(root)));threading.Thread(target=s.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{s.server_port}/';results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h,touch in [(1440,1000,False),(1024,768,True),(768,1024,True),(390,844,True),(320,720,True)]:
  ctx=b.new_context(viewport={'width':w,'height':h},has_touch=touch,is_mobile=touch);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.goto(base+'life-changes/marriage/buying-a-home-together-when-one-spouse-already-owns-property.html',wait_until='domcontentloaded');pg.evaluate('document.fonts.ready');pg.wait_for_timeout(100);d={'width':w};compact=pg.locator('#ss22-header').evaluate('e=>e.classList.contains("ss22-compact-nav")')
  n=pg.locator('.ss22-neighborhoods');nt=n.locator(':scope>button');np=n.locator('.ss22-panel')
  if touch:nt.tap()
  else:nt.hover()
  d['firstHoverOrTapShowsCities']=np.is_visible();dest=np.locator('a').filter(has_text='Winnetka');dest.click();pg.wait_for_url('**/buy-winnetka.html');d['cityDirectFromNested']=pg.locator('h1').is_visible()
  st=pg.locator('.ss22-search>button');sp=pg.locator('.ss22-search>.ss22-panel')
  if touch:st.tap()
  else:st.hover()
  d['firstHoverOrTapShowsSearch']=sp.is_visible();sp.locator('a').click();pg.wait_for_url('**/search.html');d['existingSearchWorks']=pg.locator('input[aria-label="Minimum price"]').is_visible() and pg.locator('select[name="city"]').is_visible()
  pg.goto(base+'index.html',wait_until='domcontentloaded');pg.evaluate('document.fonts.ready')
  if compact:pg.locator('.ss22-menu-toggle').click()
  a=pg.locator('.ss22-buyers>a')
  if touch:a.tap()
  else:a.hover()
  f=pg.locator('.ss22-flyout').last
  if not compact:
   if touch:f.locator(':scope>a').tap()
   else:f.locator(':scope>a').hover()
  f.locator('.ss22-flyout-panel>a').first.click();pg.wait_for_url('**/buyer-questions.html');d['formerBuyingRouteWorks']=pg.locator('h1').text_content().strip()=='Buying'
  pg.goto(base+'index.html',wait_until='domcontentloaded');pg.evaluate('document.fonts.ready')
  if touch:
   n=pg.locator('.ss22-neighborhoods');n.locator(':scope>button').tap();np=n.locator('.ss22-panel');d['backgroundLocked']=pg.evaluate("getComputedStyle(document.body).overflow==='hidden'");start=pg.evaluate('scrollY');np.locator('a').last.scroll_into_view_if_needed();d['panelScrollDoesNotMovePage']=pg.evaluate('scrollY')==start
   pg.locator('.ss22-search>button').tap();d['switchClosesPrevious']=not np.is_visible() and pg.locator('.ss22-search>.ss22-panel').is_visible();pg.keyboard.press('Escape');pg.wait_for_timeout(20);d['escapeRestoresFocus']=pg.locator('.ss22-search>button').evaluate('e=>e===document.activeElement');d['scrollRestored']=pg.evaluate("getComputedStyle(document.body).overflow!=='hidden'&&!document.querySelector('main').inert")
   pg.locator('.ss22-search>button').tap();pg.set_viewport_size({'width':1280,'height':800});pg.wait_for_timeout(100);d['resizeClosesAndUnlocks']=not pg.locator('.ss22-search>.ss22-panel').is_visible() and pg.evaluate("getComputedStyle(document.body).overflow!=='hidden'")
  else:
   pg.locator('.ss22-search>button').focus();d['keyboardOpensSearch']=pg.locator('.ss22-search>.ss22-panel').is_visible();pg.keyboard.press('Escape');d['escapeClosesSearch']=not pg.locator('.ss22-search>.ss22-panel').is_visible();pg.locator('.ss22-neighborhoods>button').focus();d['keyboardOpensCities']=pg.locator('.ss22-neighborhoods>.ss22-panel').is_visible();pg.keyboard.press('Escape');pg.locator('.ss22-buyers>a').focus();pg.locator('.ss22-flyout').first.locator(':scope>a').focus();d['keyboardOpensFlyout']=pg.locator('.ss22-flyout').first.locator('.ss22-flyout-panel').is_visible();pg.keyboard.press('Escape');d['flyoutEscapeReturnsFocus']=pg.locator('.ss22-flyout').first.locator(':scope>a').evaluate('e=>e===document.activeElement');pg.keyboard.press('Escape');pg.locator('.ss22-search>button').hover();pg.evaluate('window.scrollTo(0,250)');pg.wait_for_timeout(100);d['offscreenTriggerClosesDropdown']=not pg.locator('.ss22-search>.ss22-panel').is_visible();pg.evaluate('window.scrollTo(0,0)');pg.locator('.ss22-buyers>a').click();pg.wait_for_url('**/buy-a-home.html#top');d['primaryBuyStillNavigates']=True
  d['passed']=all(v for k,v in d.items() if k!='width');results.append(d);(out/'interaction-results.json').write_text(json.dumps(results,indent=2));print(json.dumps(d),flush=True);ctx.close()
 b.close()
s.shutdown()
