exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'translation-audit'/'final';out.mkdir(exist_ok=True);results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h in [(768,1024),(820,1180),(834,1194),(1024,768),(1180,820),(1280,900),(1440,1000),(390,844),(430,932)]:
  ctx=b.new_context(viewport={'width':w,'height':h},has_touch=w<1200);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.goto(f'http://127.0.0.1:{s.server_port}/about.html',wait_until='domcontentloaded');pg.wait_for_timeout(900);pg.evaluate('document.documentElement.style.scrollBehavior="auto"')
  d=pg.locator('#dd-header').evaluate('h=>({overflow:document.documentElement.scrollWidth>innerWidth,height:h.offsetHeight,tools:[...h.querySelector(".dd-header-tools").children].map(e=>({class:e.className,left:e.getBoundingClientRect().left,right:e.getBoundingClientRect().right})),navWidth:h.querySelector("nav").clientWidth,navScroll:h.querySelector("nav").scrollWidth})');results.append({'width':w,**d});print(w,d,flush=True);assert not d['overflow'],d;assert all(d['tools'][i]['right']<=d['tools'][i+1]['left'] for i in range(2)),d
  assert all(t['left']>=0 and t['right']<=w for t in d['tools']),d;pg.screenshot(path=str(out/f'after-{w}-closed.png'))
  if w<600:pg.locator('.dd-menu-toggle').tap();pg.screenshot(path=str(out/f'after-{w}-phone-open.png'));pg.keyboard.press('Escape')
  for label in ['Buy','Interior Design','Sell']:
   if w<600:break
   a=pg.locator('#dd-navigation>.dd-group>a').filter(has_text=label).first
   a.tap() if w<1200 else a.hover();pg.wait_for_timeout(220);assert a.locator('..').locator(':scope>.dd-panel').is_visible();
   if 600<=w<1200:assert pg.locator('.dd-contact>a').evaluate('e=>e.getBoundingClientRect().bottom<=innerHeight'),(w,label,'Contact offscreen')
   pg.screenshot(path=str(out/f'after-{w}-{label.replace(" ","-")}.png'));pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()');pg.mouse.move(0,h-1)
  a=pg.locator('.dd-language-trigger');a.tap() if w<1200 else a.hover();pg.wait_for_timeout(100);assert pg.locator('.dd-language-panel').is_visible();assert pg.locator('.dd-language-options button').count()==11;pg.screenshot(path=str(out/f'{w}-language-menu.png'))
  pg.locator('.dd-language-options button[lang="es"]').click();pg.wait_for_timeout(250);assert pg.locator('.dd-language-status').text_content();assert pg.locator('h1').first.text_content()=='About Dominique Duncan-Nelson';assert pg.evaluate('document.documentElement.lang')=='en';assert not errs,errs;ctx.close()
 b.close()
s.shutdown();(out/'navigation-results.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print('Navigation, language controls, native error fallback passed. No Google calls made.')
