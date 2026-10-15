exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'navigation-language-final-audit'/'final';out.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h in [(768,1024),(820,1180),(834,1194),(1024,768),(1180,820),(1440,1000),(390,844)]:
  ctx=b.new_context(viewport={'width':w,'height':h},has_touch=w<1200);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/about.html',wait_until='domcontentloaded');pg.wait_for_timeout(600);assert pg.locator('link[href*="tablet-language.css?v=20261015-navigation-language-v2"]').count()==1;assert not pg.evaluate('document.documentElement.scrollWidth>innerWidth');pg.screenshot(path=str(out/f'after-{w}-closed.png'))
  if 600<=w<1200:pg.locator('.dd-interior>a').tap();pg.wait_for_timeout(220);pg.screenshot(path=str(out/f'after-{w}-expanded.png'));pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()')
  a=pg.locator('.dd-language-trigger');a.tap() if w<1200 else a.hover();pg.wait_for_timeout(200);assert pg.locator('.dd-language-panel').evaluate('e=>e.getBoundingClientRect().height<350');assert pg.locator('.dd-language-options button').evaluate_all('es=>es.every(e=>getComputedStyle(e).textAlign==="left")');assert pg.locator('.dd-language-panel details').count()==0;pg.screenshot(path=str(out/f'after-{w}-language.png'));assert pg.locator('script[src*="google-translation.js?v=20261015-compact"]').count()==1;pg.locator('.dd-language-notice-link').click();assert pg.locator('.dd-translation-legal').is_visible();pg.locator('.dd-translation-legal button').click();assert not pg.locator('.dd-translation-legal').is_visible();ctx.close()
 b.close()
s.shutdown();print('Captured verified after screenshots at all requested tablet sizes plus desktop and phone.')
