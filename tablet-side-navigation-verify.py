exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'tablet-side-navigation-audit';out.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h in [(768,1024),(820,1180),(834,1194),(1024,768),(1180,820)]:
  pg=b.new_page(viewport={'width':w,'height':h},has_touch=True);pg.route('https://**/*',lambda r:r.abort());pg.goto(f'http://127.0.0.1:{s.server_port}/interior-design.html',wait_until='domcontentloaded');pg.wait_for_timeout(150)
  d=pg.locator('#dd-navigation').evaluate('e=>({client:e.clientWidth,scroll:e.scrollWidth,links:[...e.querySelectorAll(":scope>a,:scope>.dd-group>a")].map(a=>({text:a.textContent,x:a.getBoundingClientRect().left,right:a.getBoundingClientRect().right,bottom:a.getBoundingClientRect().bottom})),body:document.documentElement.scrollWidth})');print(w,d,flush=True);assert d['body']==w,d;assert d['scroll']<=d['client'];assert len(d['links'])==10;assert all(a['x']>=0 and a['right']<=200 and a['bottom']<=h for a in d['links']);pg.screenshot(path=str(out/f'{w}-navigation.png'))
  pg.locator('.dd-interior>a').tap();pg.screenshot(path=str(out/f'{w}-dropdown.png'));assert pg.locator('.dd-interior>.dd-panel').is_visible();pg.close()
 b.close()
s.shutdown()
