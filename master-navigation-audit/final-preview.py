exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'master-navigation-audit'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in [390,768,834,1024,1440]:
  ctx=b.new_context(viewport={'width':w,'height':1000},has_touch=w<1200);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/considerations.html',wait_until='domcontentloaded');pg.locator('.consideration-photo img').evaluate_all("aa=>Promise.all(aa.map(a=>{a.loading='eager';return a.decode()}))");assert pg.locator('.consideration-card h2').first.evaluate('a=>getComputedStyle(a).fontSize')=='24px';pg.screenshot(path=str(out/f'considerations-{w}.png'),full_page=True);pg.locator('.considerations-grid').screenshot(path=str(out/f'cards-detail-{w}.png'));ctx.close()
 for name in ['design-questions/best-accent-wall-colors.html','life-changes/marriage.html']:
  pg=b.new_page(viewport={'width':768,'height':1024});pg.route('https://**/*',lambda r:r.abort());pg.goto(f'http://127.0.0.1:{s.server_port}/{name}',wait_until='domcontentloaded');a=pg.locator('#dd-navigation>a').filter(has_text='Considerations');assert a.count()==1;assert a.get_attribute('href')=='considerations.html';a.click();pg.wait_for_url('**/considerations.html');pg.close()
 b.close()
s.shutdown();print('Final card typography and nested base-URL links verified.')
