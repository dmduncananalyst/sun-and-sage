exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'ipad-uniform-type-audit';results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in [768,820,834,1024,1180,1440,390]:
  ctx=b.new_context(viewport={'width':w,'height':1024},has_touch=w<1200);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/considerations.html',wait_until='domcontentloaded');pg.wait_for_timeout(200)
  def styles():return pg.locator('#dd-navigation a').evaluate_all('''es=>es.map(e=>({label:e.textContent.trim(),font:getComputedStyle(e).fontFamily,size:getComputedStyle(e).fontSize,weight:getComputedStyle(e).fontWeight,line:getComputedStyle(e).lineHeight,spacing:getComputedStyle(e).letterSpacing,case:getComputedStyle(e).textTransform}))''')
  d=styles()
  if 600<=w<1200:
   assert len({tuple(x[k] for k in ['font','size','weight','line','spacing','case']) for x in d})==1,d
   assert d[0]['size']=='13px'
   pg.screenshot(path=str(out/f'{w}-closed.png'))
   pg.locator('#dd-navigation>.dd-group').filter(has=pg.locator('a[href="sell-a-home.html"]')).locator(':scope >a').tap()
   pg.wait_for_timeout(450);pg.screenshot(path=str(out/f'{w}-sell-open.png'))
   assert pg.locator('#dd-navigation .is-open .dd-panel').is_visible()
  else:
   old=json.loads((root/'english-restoration-audit/after-navigation.json').read_text());old=next(x for x in old if x['width']==w)
   roots=pg.locator('#dd-navigation>a,#dd-navigation>.dd-group>a').evaluate_all('es=>es.map(e=>({fontFamily:getComputedStyle(e).fontFamily,fontSize:getComputedStyle(e).fontSize,lineHeight:getComputedStyle(e).lineHeight}))')
   for x,y in zip(roots,old['nav']):
    for k in x:assert x[k]==y['css'][k]
  results.append({'width':w,'labels':d,'status':'pass'});print('PASS',w,flush=True);ctx.close()
 b.close()
s.shutdown();(out/'results.json').write_text(json.dumps(results,indent=2))

