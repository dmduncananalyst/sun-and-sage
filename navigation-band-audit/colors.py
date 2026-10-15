exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True);pg=b.new_page();pg.route('https://**/*',lambda r:r.abort());pg.goto(f'http://127.0.0.1:{s.server_port}/index.html');print(pg.locator('a,footer').evaluate_all('es=>es.map(e=>({text:e.textContent.trim().slice(0,65),bg:getComputedStyle(e).backgroundColor})).filter(e=>e.bg!=="rgba(0, 0, 0, 0)").slice(-35)'));b.close()
s.shutdown()
