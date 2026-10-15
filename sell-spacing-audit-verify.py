exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'sell-spacing-audit';out.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in [390,768,1440]:
  pg=b.new_page(viewport={'width':w,'height':1000});pg.route('https://**/*',lambda r:r.abort());pg.goto(f'http://127.0.0.1:{s.server_port}/sell-a-home.html',wait_until='domcontentloaded');pg.evaluate('document.documentElement.style.scrollBehavior="auto"');d=pg.evaluate('''()=>{let a=document.querySelector('.ss23-invitation>a').getBoundingClientRect(),h=document.querySelector('.ss23-invitation h2').getBoundingClientRect(),r=document.querySelector('.ss24-reviews>.v4-button').getBoundingClientRect(),f=document.querySelector('#dd-site-footer').getBoundingClientRect();return {footerGap:f.top-a.bottom,reviewGap:h.top-r.bottom,overflow:document.documentElement.scrollWidth>innerWidth}}''');assert 48<=d['footerGap']<=64,d;assert d['reviewGap']<100,d;assert not d['overflow'];pg.locator('.ss23-invitation').evaluate('e=>window.scrollTo({top:e.getBoundingClientRect().top+scrollY-200,behavior:"instant"})');pg.wait_for_timeout(100);pg.screenshot(path=str(out/f'{w}.png'));print(w,d,flush=True);pg.close()
 b.close()
s.shutdown()
