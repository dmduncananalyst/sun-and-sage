exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'ipad-buy-life-layout-audit';results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in [768,820,834,1024,1180,1440,390]:
  ctx=b.new_context(viewport={'width':w,'height':1024},has_touch=w<1200);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page()
  for n in ['buy-a-home.html','life-changes.html']:
   pg.goto(f'http://127.0.0.1:{s.server_port}/'+n,wait_until='domcontentloaded');pg.wait_for_timeout(180)
   if n.startswith('buy'):
    d=pg.locator('.dd-buy-intro h1 span').evaluate('''e=>{let r=document.createRange();r.selectNodeContents(e);return {lines:r.getClientRects().length,width:r.getBoundingClientRect().width,available:e.closest('.dd-buy-intro').clientWidth,text:e.textContent}}''')
    if 600<=w<1200:assert d['lines']==1 and d['width']<=d['available']+1,d
   else:
    d=pg.locator('.loanHubGrid').evaluate('''e=>({columns:getComputedStyle(e).gridTemplateColumns.split(' ').length,cards:e.querySelectorAll('article').length,overflow:document.documentElement.scrollWidth>innerWidth})''')
    if 600<=w<1200:assert d['columns']==2 and not d['overflow'],d
   pg.screenshot(path=str(out/f'{w}-{n}.png'));results.append({'width':w,'page':n,**d})
  ctx.close();print('PASS',w,flush=True)
 b.close()
s.shutdown();(out/'results.json').write_text(json.dumps(results,indent=2))
