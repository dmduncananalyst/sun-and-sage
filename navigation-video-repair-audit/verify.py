exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'navigation-video-repair-audit'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,fail in [(1440,False),(768,False),(390,False),(1440,True),(390,True)]:
  ctx=b.new_context(viewport={'width':w,'height':900},has_touch=w<1200);ctx.route('https://**/*',lambda r:r.abort())
  if fail:ctx.route('**/*-web.mp4',lambda r:r.abort());ctx.route('**/*-mobile.mp4',lambda r:r.abort())
  pg=ctx.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/index.html',wait_until='domcontentloaded');pg.wait_for_function('(()=>{const v=document.querySelector("#home-introduction-video");return v.currentTime>0.3&&!v.paused})()',timeout=20000)
  d=pg.locator('#home-introduction-video').evaluate('v=>({src:v.currentSrc,time:v.currentTime,error:v.error?.code})');assert not d.get('error');assert ('home-introduction.mp4' in d['src'])==fail
  assert pg.locator('#dd-navigation>.dd-group').filter(has_text='Property Management').count()==0
  assert pg.locator('#dd-navigation>a[href="property-management.html"]').count()==1
  assert pg.locator('.dd-buyers .dd-panel a[href="buyer-consultation.html"]').count()==0
  assert 'Open video' not in pg.locator('.videoHero').inner_text()
  pg.screenshot(path=str(out/f'{w}-video-{fail}.png'));print(w,fail,d,flush=True);ctx.close()
 b.close()
s.shutdown()
