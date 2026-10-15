exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True);pg=b.new_page();pg.route('https://**/*',lambda r:r.abort());pg.goto(f'http://127.0.0.1:{s.server_port}/index.html',wait_until='domcontentloaded');pg.wait_for_timeout(3000);print(pg.locator('#home-introduction-video').evaluate('v=>({src:v.currentSrc,error:v.error&&{code:v.error.code,message:v.error.message},state:v.readyState,time:v.currentTime,paused:v.paused})'));b.close()
s.shutdown()

