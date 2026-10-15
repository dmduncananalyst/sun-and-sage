exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'home-portfolio-photo-audit';out.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in [390,768,1024,1440]:
  pg=b.new_page(viewport={'width':w,'height':1000});pg.route('https://**/*',lambda r:r.abort());pg.goto(f'http://127.0.0.1:{s.server_port}/index.html',wait_until='domcontentloaded');pg.evaluate('document.documentElement.style.scrollBehavior="auto"');grid=pg.locator('.ss22-project-grid');grid.scroll_into_view_if_needed();pg.wait_for_timeout(600)
  d=grid.locator('.ss22-project').evaluate_all('es=>es.map(e=>{let i=e.querySelector("img"),s=e.querySelector("span"),r=i.getBoundingClientRect(),t=s.getBoundingClientRect();return {loaded:i.complete&&i.naturalWidth>0,gap:t.top-r.bottom,w:r.width,h:r.height}})');assert all(a['loaded'] and a['gap']>=-1 for a in d),d;grid.screenshot(path=str(out/f'{w}.png'));pg.close()
 b.close()
s.shutdown();print('Verified all four photos load with captions below images at desktop, tablet and phone widths.')
