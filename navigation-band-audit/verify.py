exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'navigation-band-audit'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h in [(320,740),(390,844),(768,1024),(1024,768),(1280,900),(1440,1000),(1920,1080)]:
  touch=w<1200;ctx=b.new_context(viewport={'width':w,'height':h},has_touch=touch,device_scale_factor=1);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.goto(f'http://127.0.0.1:{s.server_port}/about.html',wait_until='domcontentloaded');pg.wait_for_timeout(200)
  assert pg.locator('.dd-search').get_attribute('href')=='search.html'
  assert pg.locator('.dd-search .dd-panel').count()==0
  assert not pg.evaluate('document.documentElement.scrollWidth>innerWidth')
  if w<600:
   pg.locator('.dd-menu-toggle').tap();pg.locator('.dd-buyers>a').tap();pg.screenshot(path=str(out/f'{w}-menu.png'));pg.locator('.dd-menu-toggle').tap()
  else:
   for i in range(pg.locator('#dd-navigation>.dd-group').count()):
    g=pg.locator('#dd-navigation>.dd-group').nth(i);a=g.locator(':scope>a');a.scroll_into_view_if_needed()
    if touch:a.tap()
    else:a.hover()
    pg.wait_for_timeout(70);panel=g.locator(':scope>.dd-panel');assert panel.is_visible()
    d=panel.evaluate('e=>({x:e.getBoundingClientRect().x,width:e.getBoundingClientRect().width,top:e.getBoundingClientRect().top,bottom:e.getBoundingClientRect().bottom,navBottom:document.querySelector("#dd-navigation").getBoundingClientRect().bottom,color:getComputedStyle(e).backgroundColor,links:[...e.querySelectorAll("a")].filter(a=>a.getClientRects().length).map(a=>({text:a.textContent.trim(),x:a.getBoundingClientRect().x,right:a.getBoundingClientRect().right}))})')
    assert abs(d['x'])<1 and abs(d['width']-w)<1 and abs(d['top']-d['navBottom'])<1,d
    assert all(x['x']>=0 and x['right']<=w for x in d['links'])
    if not touch:panel.locator('a').first.hover();pg.wait_for_timeout(300);assert panel.is_visible()
    pg.screenshot(path=str(out/f'{w}-group-{i}.png'));results.append(dict(viewport=w,group=i,**d));pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()');pg.mouse.move(0,h-1);pg.wait_for_timeout(50)
  a=pg.locator('.dd-neighborhoods>button')
  if touch:a.tap()
  else:a.hover()
  pg.wait_for_timeout(80);panel=pg.locator('.dd-neighborhoods>.dd-panel');assert panel.is_visible();assert panel.locator('.dd-panel-content>a').count()==30
  assert panel.evaluate('e=>getComputedStyle(e).backgroundColor')=='rgb(72, 83, 62)'
  pg.screenshot(path=str(out/f'{w}-neighborhoods.png'));assert not errs,errs;ctx.close()
 b.close()
(out/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8');s.shutdown();print('Passed seven widths; all five bands, hover transfer, touch, phone menu, and 30 Neighborhoods links.')

