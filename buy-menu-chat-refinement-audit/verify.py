exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'buy-menu-chat-refinement-audit';results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in [320,375,390,430,600,650,744,768,820,834,1024,1180,1280,1366,1440,1920]:
  ctx=b.new_context(viewport={'width':w,'height':1000 if w>=600 else 844},has_touch=w<1200);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();errors=[];pg.on('pageerror',lambda e:errors.append(str(e)));pg.goto(f'http://127.0.0.1:{s.server_port}/buy-a-home.html',wait_until='domcontentloaded');pg.wait_for_timeout(150);assert pg.locator('.dd-buy-location').count()==0
  a=pg.locator('#dd-header a.dd-search');assert a.count()==1 and a.get_attribute('aria-haspopup') is None and a.get_attribute('href')=='search.html';assert pg.locator('#dd-header .dd-search .dd-panel').count()==0
  d=pg.locator('.dd-buy-benefits').evaluate('e=>({items:[...e.querySelectorAll("article")].map(a=>{let s=a.querySelector("svg").getBoundingClientRect(),h=a.querySelector("h3").getBoundingClientRect();return {icon:s.toJSON(),heading:h.toJSON(),aligned:Math.abs(s.y+s.height/2-h.y-h.height/2)<1}}),overflow:document.documentElement.scrollWidth>innerWidth})');assert not d['overflow'] and all(x['aligned'] for x in d['items']),(w,d)
  assert pg.locator('#sun-conversation img,#sun-conversation .sunConversation__brand').count()==0
  pg.screenshot(path=str(out/f'buy-{w}.png'),full_page=True)
  if w in [390,768,1024,1440]:
   pg.locator('.dd-buy-benefits').screenshot(path=str(out/f'benefits-{w}.png'));pg.locator('.dd-buy-reach').screenshot(path=str(out/f'maps-{w}.png'))
   pg.evaluate('scrollTo({top:0,behavior:"instant"})')
   if w==390:pg.locator('.dd-menu-toggle').tap();pg.screenshot(path=str(out/'sage-menu-390.png'));pg.keyboard.press('Escape')
   trigger=pg.locator('[data-sun-conversation-open]').first;trigger.scroll_into_view_if_needed();trigger.click();dialog=pg.locator('#sun-conversation');assert dialog.is_visible();assert dialog.locator('img').count()==0;pg.screenshot(path=str(out/f'chat-{w}.png'));dialog.locator('.sunConversation__close').click();assert not dialog.is_visible()
  if w==1440:
   pg.evaluate('scrollTo({top:0,behavior:"instant"})');a.hover();pg.wait_for_timeout(80);assert pg.locator('#dd-header .is-open').count()==0
  a.click();pg.wait_for_url('**/search.html');assert not errors,errors;d.update(width=w,errors=errors);results.append(d);ctx.close();print('Passed',w,flush=True)
 # Inline and nested chat implementations share the same logo-free template.
 for name in ['contact.html','life-changes/marriage.html','buyer-consultation.html']:
  pg=b.new_page(viewport={'width':768,'height':1024});pg.route('https://**/*',lambda r:r.abort());pg.goto(f'http://127.0.0.1:{s.server_port}/{name}',wait_until='domcontentloaded');assert pg.locator('#sun-conversation img,.sunConversation__brand').count()==0;pg.close()
 b.close()
s.shutdown();(out/'results.json').write_text(json.dumps(results,indent=2));print('All responsive, alignment, direct Search and chat-logo checks passed.')
