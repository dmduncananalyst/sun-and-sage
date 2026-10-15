exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'consultation-spacing-audit';out.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in [390,768,1440]:
  pg=b.new_page(viewport={'width':w,'height':900});pg.route('https://**/*',lambda r:r.abort())
  for kind in ['buyer','seller']:
   pg.goto(f'http://127.0.0.1:{s.server_port}/{kind}-consultation.html',wait_until='domcontentloaded');pg.evaluate('document.documentElement.style.scrollBehavior="auto"');a=pg.locator(f'.dd-{kind}-consultation-action>a');gap=pg.evaluate('''()=>{let a=document.querySelector('[class$="-consultation-action"]>a'),f=document.querySelector('body>footer');return f.getBoundingClientRect().top-a.getBoundingClientRect().bottom}''');assert 24<=gap<=64,gap
   a.evaluate('e=>window.scrollTo({top:e.getBoundingClientRect().top+scrollY-350,behavior:"instant"})');pg.wait_for_timeout(100);pg.screenshot(path=str(out/f'{kind}-{w}.png'));print(kind,w,'button-to-footer gap:',gap,flush=True)
  pg.close()
 b.close()
s.shutdown()

