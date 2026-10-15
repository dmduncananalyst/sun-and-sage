exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'complete-master-audit'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in [1440,768,390]:
  pg=b.new_page(viewport={'width':w,'height':1000});pg.route('https://**/*',lambda r:r.abort());pg.goto(f'http://127.0.0.1:{s.server_port}/buy-a-home.html',wait_until='domcontentloaded');pg.wait_for_timeout(150);pg.screenshot(path=str(out/f'before-buy-{w}.png'),full_page=True);pg.close()
 b.close()
s.shutdown();print('Captured desktop, iPad and phone Buy before screenshots.')
