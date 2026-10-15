exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'responsive-arrival-audit';results=[];source=(root/'assets/navigation-v22.js').read_text(encoding='utf-8')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in [390,768,820,834,1024,1180,1440]:
  ctx=b.new_context(viewport={'width':w,'height':1024},has_touch=w<1200);ctx.route('https://**/*',lambda r:r.abort());ctx.route('**/assets/navigation-v22.js',lambda r:r.fulfill(content_type='application/javascript',body='setTimeout(()=>{'+source+';window.__navFinished=true},2000);'))
  pg=ctx.new_page()
  for page in ['index.html','contact.html','interior-design.html']:
   pg.goto(f'http://127.0.0.1:{s.server_port}/'+page,wait_until='domcontentloaded');pg.wait_for_timeout(100)
   script='''()=>({header:document.querySelector('#dd-header').getBoundingClientRect().toJSON(),items:[...document.querySelectorAll('#dd-navigation>a,#dd-navigation>.dd-group>a,.dd-menu-toggle,.dd-header-tools')].map(e=>({rect:e.getBoundingClientRect().toJSON(),size:getComputedStyle(e).fontSize})),mode:document.querySelector('#dd-header').className})'''
   early=pg.evaluate(script)
   if page=='index.html':pg.screenshot(path=str(out/f'{w}-arrival.png'))
   pg.wait_for_function('window.__navFinished===true');late=pg.evaluate(script)
   if w<1200:
    assert early['header']==late['header'],(w,page,'header moved')
    for a,z in zip(early['items'],late['items']):
     assert a['size']==z['size'],(w,page,'font changed')
     assert all(abs(a['rect'][k]-z['rect'][k])<0.5 for k in a['rect']),(w,page,'menu moved')
   else:
    baseline=next(x for x in json.loads((root/'english-restoration-audit/after-navigation.json').read_text()) if x['width']==1440)
    for a,z in zip(late['items'][:10],baseline['nav']):assert a['size']==z['css']['fontSize']
   if page=='index.html':pg.screenshot(path=str(out/f'{w}-ready.png'))
   results.append({'width':w,'page':page,'stableHeaderAndMenu':True})
  print('PASS stable arrival',w,flush=True);ctx.close()
 b.close()
s.shutdown();(out/'results.json').write_text(json.dumps(results,indent=2))

