exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
phase=sys.argv[1];out=root/'tablet-editorial-redesign-audit';out.mkdir(exist_ok=True);records=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h in [(768,1024),(820,1180),(834,1194),(1024,768),(1180,820)]:
  ctx=b.new_context(viewport={'width':w,'height':h},has_touch=True);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/about.html',wait_until='domcontentloaded');pg.wait_for_timeout(700)
  d=pg.evaluate('''()=>({styles:[...document.styleSheets].map(s=>s.href).filter(Boolean),scripts:[...document.scripts].map(s=>s.src).filter(Boolean),nav:{background:getComputedStyle(document.querySelector('#dd-navigation')).background,padding:getComputedStyle(document.querySelector('#dd-navigation')).padding},overflow:document.documentElement.scrollWidth>innerWidth})''');assert any('tablet-language.css' in x for x in d['styles']);assert any('navigation-v22.js' in x for x in d['scripts']);assert not d['overflow'];records.append({'width':w,**d});pg.screenshot(path=str(out/f'{phase}-{w}-closed.png'))
  for label in ['Buy','Interior Design','Sell']:
   a=pg.locator('#dd-navigation>.dd-group>a').filter(has_text=label).first;a.tap();pg.wait_for_timeout(220);panel=a.locator('..').locator(':scope>.dd-panel');assert panel.is_visible();assert panel.evaluate('e=>getComputedStyle(e).position')=='static';assert pg.locator('#dd-navigation').evaluate('e=>e.scrollWidth<=e.clientWidth');pg.screenshot(path=str(out/f'{phase}-{w}-{label.replace(" ","-")}.png'));pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()')
  ctx.close()
 b.close()
s.shutdown();(out/f'{phase}-loaded-assets.json').write_text(json.dumps(records,indent=2),encoding='utf-8');print(phase,'screenshots captured; loaded shared CSS/JS verified at five widths.')
