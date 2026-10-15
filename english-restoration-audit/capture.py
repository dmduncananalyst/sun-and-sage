exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'english-restoration-audit'; phase=sys.argv[1]; data=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in [768,820,834,1024,1180,1440,390]:
  ctx=b.new_context(viewport={'width':w,'height':1024},has_touch=w<1200);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/index.html');pg.wait_for_timeout(400)
  d=pg.evaluate('''()=>({width:innerWidth,styles:[...document.styleSheets].map(s=>s.href).filter(Boolean),nav:[...document.querySelectorAll('#dd-navigation>a,#dd-navigation>.dd-group>a')].map(e=>({text:e.textContent,rect:e.getBoundingClientRect().toJSON(),css:Object.fromEntries(['fontFamily','fontSize','lineHeight','padding','margin','color','background','border','letterSpacing'].map(k=>[k,getComputedStyle(e)[k]]))})),neighborhoodFont:getComputedStyle(document.querySelector('.dd-neighborhoods .dd-panel a')).fontFamily,language:!!document.querySelector('.dd-language')})''');data.append(d)
  pg.screenshot(path=str(out/f'{phase}-{w}-closed.png'))
  if 600<=w<1200:
   pg.locator('.dd-interior>a').tap();pg.screenshot(path=str(out/f'{phase}-{w}-expanded.png'))
  ctx.close()
 b.close()
(out/f'{phase}-navigation.json').write_text(json.dumps(data,indent=2));s.shutdown()
