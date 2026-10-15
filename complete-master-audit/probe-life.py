exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'complete-master-audit'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True);pg=b.new_page(viewport={'width':1440,'height':1000});pg.route('https://**/*',lambda r:r.abort());pg.goto(f'http://127.0.0.1:{s.server_port}/life-changes.html',wait_until='domcontentloaded');pg.locator('main img').evaluate_all("aa=>Promise.all(aa.map(a=>{a.loading='eager';return a.decode()}))");pg.screenshot(path=str(out/'probe-life-1440.png'),full_page=True);print(pg.locator('main img[src*="images/life-changes"]').evaluate_all('aa=>aa.map(i=>({src:i.getAttribute("src"),fit:getComputedStyle(i).objectFit,rect:i.getBoundingClientRect().toJSON(),frame:i.parentElement.getBoundingClientRect().toJSON()}))'));b.close()
s.shutdown()
