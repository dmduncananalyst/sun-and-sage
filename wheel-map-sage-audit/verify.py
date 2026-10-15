exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'wheel-map-sage-audit';results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in [320,390,650,768,1024,1440,1920]:
  ctx=b.new_context(viewport={'width':w,'height':1000 if w>=600 else 844},has_touch=w<1200);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/buy-a-home.html',wait_until='domcontentloaded');pg.wait_for_timeout(150)
  d=pg.locator('.dd-buy-wheel').evaluate('''e=>{let r=e.getBoundingClientRect();return {size:r.width,steps:[...e.querySelectorAll('.dd-buy-step')].map(a=>{let i=a.querySelector('svg').getBoundingClientRect(),t=a.querySelector('span').getBoundingClientRect();return {text:a.textContent.trim(),distance:Math.hypot(i.x+i.width/2-r.x-r.width/2,i.y+i.height/2-r.y-r.height/2),gap:t.y-i.bottom,centerOffset:(i.x+i.width/2)-(t.x+t.width/2),bottom:t.bottom-r.y}})}}''');expected=d['size']*(.35 if w<=650 else .4);assert all(abs(x['distance']-expected)<1 and abs(x['centerOffset'])<1 for x in d['steps']),(w,d);assert max(x['gap'] for x in d['steps'])-min(x['gap'] for x in d['steps'])<1
  assert not pg.evaluate('document.documentElement.scrollWidth>innerWidth');pg.locator('.dd-buy-wheel').screenshot(path=str(out/f'wheel-{w}.png'));pg.locator('.dd-buy-reach').screenshot(path=str(out/f'maps-{w}.png'))
  pg.evaluate('scrollTo({top:0,behavior:"instant"})');a=pg.locator('.dd-neighborhoods>button').first
  if w<1200:a.tap()
  else:a.hover()
  panel=pg.locator('.dd-neighborhoods>.dd-panel');assert panel.is_visible();assert panel.evaluate('e=>getComputedStyle(e).backgroundColor')=='rgb(72, 83, 62)';assert panel.locator('.dd-panel-content>a').count()==30;assert panel.locator('.dd-panel-content>a').first.evaluate('e=>getComputedStyle(e).color')=='rgb(243, 234, 220)';pg.screenshot(path=str(out/f'neighborhoods-{w}.png'));pg.keyboard.press('Escape');assert not panel.is_visible();results.append({'width':w,**d});ctx.close();print('Passed',w,flush=True)
 b.close()
s.shutdown();(out/'results.json').write_text(json.dumps(results,indent=2));print('All wheel, map and sage Neighborhoods checks passed.')
