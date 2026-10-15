exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for name in ['blog','about']:
  for w,h in [(1440,900),(768,1024),(390,844)]:
   ctx=b.new_context(viewport={'width':w,'height':h},has_touch=w<1280);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/{name}.html',wait_until='domcontentloaded');pg.wait_for_timeout(250)
   if w<1280:pg.locator('.dd-menu-toggle').tap()
   a=pg.locator('#dd-navigation>a[aria-current="page"],#dd-navigation>.dd-group>a[aria-current="page"]').first
   d=a.evaluate('a=>({text:a.textContent,color:getComputedStyle(a).color,opacity:getComputedStyle(a).opacity,visibility:getComputedStyle(a).visibility,width:a.getBoundingClientRect().width})');assert d['color']!='rgb(255, 255, 255)' and d['opacity']=='1' and d['visibility']=='visible' and d['width']>0,d
   d.update(page=name,width=w);results.append(d)
   if name in ['blog','about']:pg.screenshot(path=str(out/f'current-label-{name}-{w}.png'))
   ctx.close()
 b.close()
s.shutdown();(out/'current-label-results.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(json.dumps(results))

