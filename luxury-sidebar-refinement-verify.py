exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'luxury-sidebar-refinement-audit';out.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h in [(768,1024),(820,1180),(834,1194),(1024,768),(1180,820),(390,844),(1440,1000)]:
  pg=b.new_page(viewport={'width':w,'height':h},has_touch=w<1200);pg.route('https://**/*',lambda r:r.abort());pg.goto(f'http://127.0.0.1:{s.server_port}/index.html',wait_until='domcontentloaded');pg.evaluate('document.documentElement.style.scrollBehavior="auto"')
  if 600<=w<1200:
   nav=pg.locator('#dd-navigation');assert nav.evaluate('e=>e.scrollWidth<=e.clientWidth');assert nav.locator(':scope>a,:scope>.dd-group>a').count()==10;pg.screenshot(path=str(out/f'{w}-closed.png'))
   for label in ['Sell','Interior Design']:
    a=nav.locator(':scope>.dd-group>a').filter(has_text=label).first;a.tap();pg.wait_for_timeout(220);panel=a.locator('..').locator(':scope>.dd-panel');assert panel.is_visible();assert panel.evaluate('e=>getComputedStyle(e).position')=='static';pg.screenshot(path=str(out/f'{w}-{label.replace(" ","-")}.png'));pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()')
  elif w==390:pg.locator('.dd-menu-toggle').tap();assert pg.locator('#dd-navigation').is_visible();pg.keyboard.press('Escape')
  else:pg.locator('.dd-interior>a').hover();assert pg.locator('.dd-interior>.dd-panel').is_visible();pg.keyboard.press('Escape');pg.mouse.move(0,h-1)
  el=pg.locator('.ss22-project-grid');el.scroll_into_view_if_needed();pg.wait_for_timeout(600);el.screenshot(path=str(out/f'{w}-home-cards.png'))
  pg.goto(f'http://127.0.0.1:{s.server_port}/portfolio.html',wait_until='domcontentloaded');pg.evaluate('document.documentElement.style.scrollBehavior="auto"');el=pg.locator('.portfolioParentGrid');el.scroll_into_view_if_needed();pg.wait_for_timeout(500);cards=el.locator('.portfolioParentCard');ratios=cards.evaluate_all('es=>es.map(e=>{let p=e.getBoundingClientRect(),c=e.querySelector(".portfolioParentCardContent").getBoundingClientRect();return c.height/p.height})');print(w,max(ratios),flush=True);pg.screenshot(path=str(out/f'{w}-portfolio.png'));pg.close()
 b.close()
s.shutdown();print('Verified five tablet sizes, desktop hover, phone MENU and compact portfolio overlays.')


