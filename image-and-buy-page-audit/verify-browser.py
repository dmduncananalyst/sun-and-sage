exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'image-and-buy-page-audit';results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in [320,390,768,1024,1440,1920]:
  ctx=b.new_context(viewport={'width':w,'height':1000 if w>=600 else 844},has_touch=w<1200);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();errors=[];pg.on('pageerror',lambda e:errors.append(str(e)));pg.goto(f'http://127.0.0.1:{s.server_port}/buy-a-home.html',wait_until='domcontentloaded');pg.wait_for_timeout(180)
  d=pg.locator('.dd-buy-page').evaluate('m=>({overflow:document.documentElement.scrollWidth>innerWidth,text:m.innerText,h1:getComputedStyle(m.querySelector("h1")).fontSize,images:m.querySelectorAll("img").length,charts:m.querySelectorAll(".dd-buy-chart").length,steps:m.querySelectorAll(".dd-buy-step").length})');assert not d['overflow'],w;assert d['images']==0 and d['charts']==2 and d['steps']==8;assert '1,333' in d['text'] and '$903K' in d['text'];pg.screenshot(path=str(out/f'buy-{w}.png'),full_page=True);pg.locator('.dd-buy-overview').screenshot(path=str(out/f'buy-process-{w}.png'))
  if w>=1200:
   pg.evaluate('scrollTo(0,0)');a=pg.locator('.dd-neighborhoods>button').first;a.hover();q=pg.locator('.dd-neighborhoods>.dd-panel').bounding_box();r=a.bounding_box();assert abs(q['x']+q['width']/2-r['x']-r['width']/2)<1;pg.screenshot(path=str(out/f'neighborhoods-centered-{w}.png'));pg.keyboard.press('Escape')
  d.update(width=w,errors=errors);assert not errors;results.append(d);ctx.close();print('Verified Buy',w,flush=True)
 import json
 assert not json.loads((out/'browser-image-decode.json').read_text())['failed']
 # Inspect named fixes in the actual category card and article layouts.
 pages=['life-changes/marriage.html','life-changes/marriage/what-if-my-husband-already-owns-a-house-before-marriage.html','short-term-rental-questions.html','short-term-rental-questions/someone-to-look-after-house-while-away.html']
 for name in pages:
  pg=b.new_page(viewport={'width':1440,'height':1000});pg.route('https://**/*',lambda r:r.abort());pg.goto(f'http://127.0.0.1:{s.server_port}/{name}',wait_until='domcontentloaded');key='article-batch-02/article-09.webp' if 'marriage' in name else 'photo-3.lossless.webp';im=pg.locator('main img').filter() if False else pg.locator('main img[src*="'+key+'"]');assert im.count()==1;im.scroll_into_view_if_needed();im.evaluate('i=>i.decode()');assert im.evaluate('i=>i.naturalWidth>0');pg.screenshot(path=str(out/('fixed-'+Path(name).stem+'.png')));pg.close()
 b.close()
s.shutdown();(out/'browser-layout-results.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print('All image decode, layout and centered-menu checks passed.')
