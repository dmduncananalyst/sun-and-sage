exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
checks=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h,touch in [(650,900,False),(390,844,True)]:
  ctx=b.new_context(viewport={'width':w,'height':h},has_touch=touch,is_mobile=touch);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/index.html',wait_until='domcontentloaded');pg.evaluate('document.fonts.ready');pg.wait_for_timeout(150);pg.locator('.dd-menu-toggle').click();d={'width':w,'mouseViewport':not touch};pg.keyboard.press('Tab');d['menuTabStartsAtHome']=pg.locator('#dd-navigation>a').first.evaluate('e=>e===document.activeElement');pg.keyboard.press('Shift+Tab');d['reverseReturnsToClose']=pg.locator('.dd-menu-toggle').evaluate('e=>e===document.activeElement');pg.keyboard.press('Shift+Tab');d['reverseWrapsToContact']=pg.locator('.dd-contact-strip a').last.evaluate('e=>e===document.activeElement');pg.keyboard.press('Tab');d['forwardWrapsToClose']=pg.locator('.dd-menu-toggle').evaluate('e=>e===document.activeElement');a=pg.locator('.dd-buyers>a');a.focus();pg.keyboard.press('Enter');d['enterExpandsInline']=pg.locator('.dd-buyers>.dd-panel').is_visible() and pg.locator('#dd-navigation>a').first.is_visible();pg.keyboard.press('Escape');d['escapeClosesAndRestoresFocus']=pg.locator('.dd-menu-toggle').get_attribute('aria-expanded')=='false' and pg.locator('.dd-menu-toggle').evaluate('e=>e===document.activeElement');pg.evaluate('document.activeElement.blur()')
  for name in ['neighborhoods','search']:
   a=pg.locator('.dd-'+name+'>button').first
   if touch:a.tap()
   else:a.hover()
   panel=pg.locator('.dd-'+name+'>.dd-panel');d[name+'OpensWithoutMouseClick']=panel.is_visible();pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()');pg.mouse.move(0,h-1);pg.wait_for_timeout(30)
  d['passed']=all(v for k,v in d.items() if k not in ['width','mouseViewport']);checks.append(d);print(json.dumps(d),flush=True);ctx.close()
 # Additional page screenshots show the identical repaired proportions beyond the homepage.
 for page in ['buy-a-home.html','life-changes/marriage.html','buy-winnetka.html','sell-a-home.html','blog.html']:
  ctx=b.new_context(viewport={'width':1366,'height':900});ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/'+page,wait_until='domcontentloaded');pg.evaluate('document.fonts.ready');pg.wait_for_timeout(100);pg.screenshot(path=str(out/('page-'+page.replace('/','-').replace('.html','')+'-1366.png')));ctx.close()
 b.close()
s.shutdown();(out/'keyboard-and-mouse-results.json').write_text(json.dumps(checks,indent=2))
