exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in [390,768,820,834,1024,1180,1440]:
  pg=b.new_page(viewport={'width':w,'height':1000},has_touch=w<1200);pg.route('https://**/*',lambda r:r.abort())
  for n in ['index.html','buy-a-home.html','contact.html']:
   pg.goto(f'http://127.0.0.1:{s.server_port}/{n}',wait_until='domcontentloaded');pg.wait_for_timeout(80)
   assert not pg.evaluate('document.documentElement.scrollWidth>innerWidth'),(w,n)
  if w==390:pg.locator('.dd-menu-toggle').tap();assert pg.locator('#dd-navigation').is_visible()
  if w==1440:pg.locator('.dd-interior>a').hover();assert pg.locator('.dd-interior>.dd-panel').is_visible()
  pg.close()
 b.close()
s.shutdown();print('Homepage, Buy and Contact passed seven widths; desktop hover and phone MENU retained.')
