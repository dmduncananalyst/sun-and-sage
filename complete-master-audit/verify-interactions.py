exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'complete-master-audit';results=[];menu_names=['Buy','Sell','Property Management','Interior Design','Contact']
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in [1280,1366,1440,1920]:
  pg=b.new_page(viewport={'width':w,'height':1000});pg.route('https://**/*',lambda r:r.abort());pg.goto(f'http://127.0.0.1:{s.server_port}/index.html',wait_until='domcontentloaded');pg.wait_for_timeout(200)
  for label in menu_names+['Neighborhoods','Search']:
   if label in menu_names:a=pg.locator('#dd-navigation>.dd-group>a').filter(has_text=label)
   else:a=pg.locator('.dd-'+label.lower()+'>button').first
   a.hover();pg.wait_for_timeout(50);panel=a.locator('..').locator(':scope>.dd-panel');assert panel.is_visible();r=a.bounding_box();q=panel.bounding_box();desired=r['x']+r['width']/2-q['width']/2;expected=max(16,min(desired,w-q['width']-16));assert abs(q['x']-expected)<1 and abs(q['y']-r['y']-r['height'])<1,(w,label,r,q);assert q['height']<500 and q['x']>=15 and q['x']+q['width']<=w-15
   panel.locator('.dd-panel-content a').first.hover();pg.wait_for_timeout(100);assert panel.is_visible();pg.screenshot(path=str(out/f'open-{label.replace(" ","-")}-{w}.png'));results.append({'width':w,'label':label,'trigger':r,'panel':q,'centered':abs(q['x']-desired)<1,'edgeClamped':abs(q['x']-desired)>=1});pg.keyboard.press('Escape');assert not panel.is_visible();pg.evaluate('document.activeElement?.blur()');pg.mouse.move(0,950);pg.wait_for_timeout(40)
  for label,dest in [('Life Changes','life-changes.html'),('Considerations','considerations.html')]:
   a=pg.locator('#dd-navigation>a').filter(has_text=label);a.hover();pg.wait_for_timeout(70);assert pg.locator('#dd-header .is-open').count()==0;assert a.get_attribute('aria-haspopup') is None and a.get_attribute('aria-expanded') is None;a.click();pg.wait_for_url('**/'+dest);pg.go_back(wait_until='domcontentloaded');pg.wait_for_timeout(150)
  # Keyboard focus and Escape preserve the true Search disclosure.
  a=pg.locator('.dd-search>button').first;a.focus();assert a.get_attribute('aria-expanded')=='true';pg.keyboard.press('Escape');assert a.get_attribute('aria-expanded')=='false';pg.close();print('Passed all dropdowns and direct links:',w,flush=True)
 for w in [320,375,390,430,744,768,820,834,1024,1180]:
  ctx=b.new_context(viewport={'width':w,'height':1024 if w>=600 else 844},has_touch=True);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/life-changes/marriage.html',wait_until='domcontentloaded');pg.wait_for_timeout(150)
  for label,dest in [('Life Changes','life-changes.html'),('Considerations','considerations.html')]:
   if w<600:pg.locator('.dd-menu-toggle').tap()
   a=pg.locator('#dd-navigation>a').filter(has_text=label);a.scroll_into_view_if_needed();a.tap();pg.wait_for_url('**/'+dest);assert pg.locator('main h1').first.is_visible();pg.go_back(wait_until='domcontentloaded');pg.wait_for_timeout(150)
  if w<600:
   pg.locator('.dd-menu-toggle').tap();pg.screenshot(path=str(out/f'phone-menu-{w}.png'));pg.locator('#dd-navigation>.dd-group>a').filter(has_text='Buy').tap();assert pg.locator('.dd-buyers>.dd-panel').is_visible();pg.screenshot(path=str(out/f'phone-menu-buy-{w}.png'));assert pg.evaluate('getComputedStyle(document.body).overflow')=='hidden';pg.keyboard.press('Escape');assert pg.locator('.dd-menu-toggle').get_attribute('aria-expanded')=='false'
  else:
   # The last item remains reachable along the tablet rail.
   a=pg.locator('#dd-navigation>.dd-group>a').filter(has_text='Contact');a.scroll_into_view_if_needed();a.tap();assert a.get_attribute('aria-expanded')=='true';pg.screenshot(path=str(out/f'tablet-rail-end-{w}.png'));pg.keyboard.press('Escape');pg.locator('#dd-navigation').evaluate('n=>n.scrollLeft=0')
   a=pg.locator('#dd-navigation>.dd-group>a').filter(has_text='Interior Design');a.scroll_into_view_if_needed();a.tap();assert a.get_attribute('aria-expanded')=='true';pg.keyboard.press('Escape')
  pg.evaluate('scrollTo(0,0)');pg.locator('.dd-search>button').first.tap();assert pg.locator('.dd-search>.dd-panel').is_visible();pg.locator('.dd-search .dd-panel-content>a').tap();pg.wait_for_url('**/search.html');pg.locator('.dd-neighborhoods>button').first.tap();assert pg.locator('.dd-neighborhoods .dd-panel-content>a').count()==30;pg.locator('.dd-neighborhoods .dd-panel-content>a').filter(has_text='Winnetka').tap();pg.wait_for_url('**/buy-winnetka.html');ctx.close();print('Passed touch navigation:',w,flush=True)
 # Original category-to-article journey; all links remain actual existing destinations.
 pg=b.new_page(viewport={'width':1440,'height':1000});pg.route('https://**/*',lambda r:r.abort());pg.goto(f'http://127.0.0.1:{s.server_port}/considerations.html',wait_until='domcontentloaded');pg.locator('.consideration-card').first.click();pg.wait_for_url('**/buyer-questions.html');pg.screenshot(path=str(out/'existing-category.png'));pg.locator('.ss18-card-photo').first.click();pg.wait_for_load_state('domcontentloaded');assert 'buyer-question-' in pg.url;pg.screenshot(path=str(out/'existing-article.png'));pg.close();b.close()
s.shutdown();(out/'dropdown-interaction-results.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print('All hover, direct-link, keyboard, touch, nested-path and existing article-flow checks passed.')
