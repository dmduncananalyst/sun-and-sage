exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
checks=json.loads((out/'hover-style-results.json').read_text()) if (out/'hover-style-results.json').exists() else []
flychecks=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True);ctx=b.new_context(viewport={'width':1280,'height':900});ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/index.html',wait_until='domcontentloaded');pg.evaluate('document.fonts.ready')
 for w,h in [(1280,900),(1366,900),(1440,1000),(1920,1080)]:
  pg.set_viewport_size({'width':w,'height':h});pg.wait_for_timeout(100)
  for group in pg.locator('#dd-navigation>.dd-group,.dd-feature').all():
   a=group.locator(':scope>a,:scope>button').first;name=a.text_content().strip()
   if any(x['width']==w and x['category']==name and x['passed'] and x['hoverTransfer'] for x in checks):continue
   checks=[x for x in checks if not(x['width']==w and x['category']==name)];a.hover();pg.wait_for_timeout(300);panel=group.locator(':scope>.dd-panel');d=a.evaluate('''a=>{const cs=getComputedStyle(a);return {background:cs.backgroundColor,color:cs.color,shadow:cs.boxShadow,transform:cs.transform}}''');d.update(width=w,category=name,open=panel.is_visible());d['flush']=panel.evaluate('p=>Math.abs(p.getBoundingClientRect().top-p.parentElement.querySelector(":scope>a,:scope>button").getBoundingClientRect().bottom)<=1');d['passed']=d['open'] and d['flush'] and d['background']=='rgba(0, 0, 0, 0)' and d['color']=='rgb(72, 83, 62)' and d['shadow']=='none' and d['transform']=='none';checks.append(d);label={'Buy':'buy','Sell':'sell','Property Management':'management','Interior Design':'design','Life Changes':'life','Contact':'contact','Neighborhoods':'neighborhoods','Search':'search'}[name];pg.screenshot(path=str(out/f'{w}-{label}.png'));panel.locator('a:visible').first.hover();d['hoverTransfer']=panel.is_visible();pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()');pg.mouse.move(0,h-1)
  for j,f in enumerate(pg.locator('.dd-flyout').all()):
   pg.locator('.dd-buyers>a').hover();f.locator(':scope>a').hover();fp=f.locator(':scope>.dd-flyout-panel');fp.locator('a:visible').first.hover();pg.wait_for_timeout(80);valid=fp.is_visible() and fp.evaluate('e=>{const r=e.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth&&r.bottom<=innerHeight&&r.top>=0}');flychecks.append({'width':w,'group':j,'passed':valid});pg.screenshot(path=str(out/f'{w}-buy-flyout-{j}.png'));pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()');pg.wait_for_timeout(30)
  print('Verified final hover styles',w,flush=True)
 ctx.close();b.close()
s.shutdown();(out/'hover-style-results.json').write_text(json.dumps(checks,indent=2));(out/'final-flyout-results.json').write_text(json.dumps(flychecks,indent=2));print('Final hover checks:',len(checks),'passed:',all(x['passed'] and x['hoverTransfer'] for x in checks),flush=True)
