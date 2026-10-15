exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'wheel-map-sage-audit'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in [390,768,1440]:
  pg=b.new_page(viewport={'width':w,'height':1000});pg.route('https://**/*',lambda r:r.abort());pg.goto(f'http://127.0.0.1:{s.server_port}/buy-a-home.html',wait_until='domcontentloaded');pg.locator('.dd-buy-reach').screenshot(path=str(out/f'maps-{w}.png'));fonts=pg.locator('.dd-buy-map strong').evaluate_all('aa=>aa.map(a=>getComputedStyle(a).fontSize)');assert fonts==['22px','18px','28px','28px'],fonts;pg.close()
 b.close()
s.shutdown();print('Final map label sizes verified: 22px, 18px, 28px, 28px.')
