exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True);pg=b.new_page(viewport={'width':768,'height':1024});pg.route('https://**/*',lambda r:r.abort());pg.goto(f'http://127.0.0.1:{s.server_port}/interior-design.html',wait_until='domcontentloaded');print(pg.locator('body *').evaluate_all('es=>es.filter(e=>e.getBoundingClientRect().right>769&&getComputedStyle(e).position!=="fixed").map(e=>({tag:e.tagName,cls:e.className,x:e.getBoundingClientRect().x,w:e.getBoundingClientRect().width})).slice(0,15)'));b.close()
s.shutdown()
