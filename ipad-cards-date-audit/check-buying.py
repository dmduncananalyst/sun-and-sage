exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 pg=b.new_page();pg.route('https://**/*',lambda r:r.abort())
 for w in [600,650,744,767,768,820,1024,1180]:
  pg.set_viewport_size({'width':w,'height':1000});pg.goto(f'http://127.0.0.1:{s.server_port}/buy-a-home.html',wait_until='domcontentloaded')
  d=pg.locator('.dd-buy-benefits').evaluate('e=>({columns:getComputedStyle(e).gridTemplateColumns.split(" ").length,width:e.clientWidth,scroll:e.scrollWidth})')
  assert d['columns']==2 and d['scroll']<=d['width']+2,(w,d)
 print('Buying cards pass all eight tablet widths.',flush=True)
 b.close()
s.shutdown()
