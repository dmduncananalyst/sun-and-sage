exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'dark-sage-map-audit'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h in [(390,844),(768,1024),(1440,1000)]:
  ctx=b.new_context(viewport={'width':w,'height':h},has_touch=w<1200);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/buy-a-home.html',wait_until='domcontentloaded');pg.wait_for_timeout(200);pg.evaluate('document.documentElement.style.scrollBehavior="auto"')
  maps=pg.locator('.dd-buy-reach-grid');maps.screenshot(path=str(out/f'{w}-maps.png'))
  for i in [2,3]:
   d=pg.locator('.dd-buy-map').nth(i).evaluate('e=>{let r=e.getBoundingClientRect(),t=e.querySelector("strong").getBoundingClientRect();return [Math.abs(t.x+t.width/2-r.x-r.width/2),Math.abs(t.y+t.height/2-r.y-r.height/2)]}');assert max(d)<1,d
  pg.evaluate('window.scrollTo({top:0,behavior:"instant"})');pg.wait_for_timeout(100)
  if w<600:pg.locator('.dd-menu-toggle').tap();target=pg.locator('#dd-navigation')
  else:
   a=pg.locator('.dd-buyers>a');a.tap() if w<1200 else a.hover();target=pg.locator('.dd-buyers>.dd-panel')
  assert target.evaluate('e=>getComputedStyle(e).backgroundColor')=='rgb(82, 107, 96)';pg.screenshot(path=str(out/f'{w}-menu.png'));pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()');pg.mouse.move(0,h-1)
  a=pg.locator('.dd-neighborhoods>button');a.tap() if w<1200 else a.hover();target=pg.locator('.dd-neighborhoods>.dd-panel');assert target.evaluate('e=>getComputedStyle(e).backgroundColor')=='rgb(82, 107, 96)';pg.screenshot(path=str(out/f'{w}-neighborhoods.png'));assert not pg.evaluate('document.documentElement.scrollWidth>innerWidth');ctx.close()
 b.close()
s.shutdown();print('Passed desktop, tablet, phone: consistent dark sage, centered Local/#1, no horizontal overflow.')
