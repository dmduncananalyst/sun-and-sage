exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'dropdown-blog-refinement-audit';results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in [390,650,744,768,820,834,1024,1180,1280,1440]:
  ctx=b.new_context(viewport={'width':w,'height':1000},has_touch=w<1200);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();errors=[];pg.on('pageerror',lambda e:errors.append(str(e)));pg.goto(f'http://127.0.0.1:{s.server_port}/blog.html',wait_until='domcontentloaded');pg.wait_for_timeout(180)
  d=pg.locator('.loanHubGrid').evaluate('g=>({columns:getComputedStyle(g).gridTemplateColumns.split(" ").length,width:g.offsetWidth,overflow:document.documentElement.scrollWidth>innerWidth})');assert d['columns']==(1 if w<=600 else 2 if w<1200 else 3),(w,d);assert not d['overflow'];pg.screenshot(path=str(out/f'blog-{w}.png'));d['width']=w
  if w in [768,1024,1440]:
   for name in ['neighborhoods','search']:
    a=pg.locator('.dd-'+name+'>button').first
    if w<1200:a.tap()
    else:a.hover()
    pg.wait_for_timeout(80);r=a.bounding_box();panel=pg.locator('.dd-'+name+'>.dd-panel');q=panel.bounding_box();assert abs(q['x']-r['x'])<1 and abs(q['y']-r['y']-r['height'])<1,(w,name,r,q);assert q['x']+q['width']<=w-15
    if w==1440:panel.locator('.dd-panel-content>a').first.hover();assert panel.is_visible()
    pg.screenshot(path=str(out/f'{name}-{w}.png'));pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()');pg.mouse.move(0,950);pg.wait_for_timeout(40)
  if w==1440:
   for label in ['Buy','Sell','Property Management','Interior Design','Life Changes','Contact']:
    a=pg.locator('#dd-navigation>.dd-group>a').filter(has_text=label);a.hover();q=a.locator('..').locator(':scope>.dd-panel').bounding_box();r=a.bounding_box();assert abs(q['y']-r['y']-r['height'])<1 and q['x']+q['width']<=w-15;pg.screenshot(path=str(out/f'menu-{label.replace(" ","-")}.png'));pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()');pg.mouse.move(0,950);pg.wait_for_timeout(40)
  if w==768:
   assert 'Swipe' not in pg.locator('#dd-header').evaluate('h=>getComputedStyle(h,"::after").content');pg.locator('#dd-navigation').evaluate('n=>n.scrollLeft=n.scrollWidth');pg.wait_for_timeout(80);assert pg.locator('#dd-header').evaluate('h=>h.classList.contains("nav-at-end")');pg.screenshot(path=str(out/'tablet-end-768.png'))
  assert not errors,errors;d['errors']=errors;results.append(d);ctx.close();print('Verified',w,flush=True)
 b.close()
s.shutdown();(out/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
