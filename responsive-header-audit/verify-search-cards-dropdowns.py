exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h in [(1440,1000),(768,1024),(390,844)]:
  ctx=b.new_context(viewport={'width':w,'height':h},has_touch=w<1280);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/search.html',wait_until='domcontentloaded');pg.wait_for_timeout(250);pg.locator('.ss23-regions img').evaluate_all("aa=>Promise.all(aa.map(a=>{a.loading='eager';return a.decode()}))");pg.locator('.ss23-regions').scroll_into_view_if_needed();pg.screenshot(path=str(out/f'search-cards-corrected-{w}.png'))
  d=pg.locator('.v30-region-card').evaluate_all('aa=>aa.map(a=>{let m=a.querySelector(".v30-region-media").getBoundingClientRect(),i=a.querySelector("img").getBoundingClientRect();return {card:a.getBoundingClientRect().toJSON(),media:m.toJSON(),image:i.toJSON(),fit:getComputedStyle(a.querySelector("img")).objectFit}})');assert all(abs(x['media']['width']-x['image']['width'])<1 and abs(x['media']['height']-x['image']['height'])<1 and x['fit']=='cover' for x in d),d
  pg.locator('.ss23-regions').screenshot(path=str(out/f'search-cards-detail-{w}.png'));pg.evaluate('scrollTo(0,0)')
  if w<1280:pg.locator('.dd-menu-toggle').tap()
  for label in ['Interior Design','Life Changes']:
   a=pg.locator('#dd-navigation>.dd-group>a').filter(has_text=label);g=a.locator('..')
   if w<1280:a.tap()
   else:a.hover()
   pg.wait_for_timeout(100);overview=g.locator('.dd-panel-content>a').first;assert overview.text_content()==label;assert overview.is_visible();pg.screenshot(path=str(out/f'dropdown-{label.replace(" ","-")}-{w}.png'))
   if w<1280:a.tap()
   else:pg.keyboard.press('Escape');pg.mouse.move(0,h-1);pg.evaluate('document.activeElement?.blur()')
  results.append({'width':w,'cards':d,'dropdowns':'passed'});ctx.close()
 b.close()
s.shutdown();(out/'search-cards-dropdown-results.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print('Passed cards and dropdowns at desktop, tablet, phone widths.')
