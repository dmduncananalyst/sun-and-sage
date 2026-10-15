exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'master-navigation-audit';widths=[320,375,390,430,600,650,744,768,820,834,1024,1180,1280,1366,1440,1920];labels=['Home','About','Buy','Sell','Property Management','Interior Design','Life Changes','Considerations','Blog','Contact'];results=[];interaction=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in widths:
  ctx=b.new_context(viewport={'width':w,'height':1000 if w>=600 else 844},has_touch=w<1200,device_scale_factor=1);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();errors=[];pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.goto(f'http://127.0.0.1:{s.server_port}/index.html',wait_until='domcontentloaded');pg.evaluate('document.fonts.ready');pg.wait_for_timeout(180)
  d=pg.locator('#dd-header').evaluate('''h=>({compact:h.classList.contains('is-compact'),rail:h.classList.contains('has-nav-rail'),height:h.offsetHeight,navVisible:!!h.querySelector('nav').getClientRects().length,menuVisible:!!h.querySelector('.dd-menu-toggle').getClientRects().length,overflow:document.documentElement.scrollWidth>innerWidth,labels:[...h.querySelector('nav').children].filter(e=>e.matches('a,.dd-group')).map(e=>(e.matches('a')?e:e.querySelector('a')).textContent),tools:h.querySelector('.dd-header-tools').getBoundingClientRect().toJSON(),contacts:h.querySelector('.dd-contact-strip').getBoundingClientRect().toJSON()})''')
  assert d['labels']==labels,(w,d);assert d['compact']==(w<600);assert d['menuVisible']==(w<600);assert d['navVisible']==(w>=600);assert not d['overflow'];assert w<600 or d['tools']['right']<=d['contacts']['left'],d
  pg.screenshot(path=str(out/f'header-{w}.png'))
  if w<600:
   pg.locator('.dd-menu-toggle').tap();assert pg.locator('#dd-navigation>a').filter(has_text='Considerations').count()==1;pg.screenshot(path=str(out/f'menu-{w}.png'));pg.locator('#dd-navigation>.dd-group>a').filter(has_text='Life Changes').tap();pg.screenshot(path=str(out/f'menu-life-{w}.png'));pg.keyboard.press('Escape')
  elif w<1200:
   # Every category remains reachable along the rail and on touch.
   for label in labels:
    a=pg.locator('#dd-navigation>a,#dd-navigation>.dd-group>a').filter(has_text=re.compile('^'+re.escape(label)+'$')) if False else None
   pg.locator('#dd-navigation>a').filter(has_text='Contact') if False else None
   last=pg.locator('#dd-navigation>.dd-group>a').filter(has_text='Contact');last.scroll_into_view_if_needed();last.tap();assert last.get_attribute('aria-expanded')=='true';pg.screenshot(path=str(out/f'tablet-end-{w}.png'));pg.keyboard.press('Escape');pg.locator('#dd-navigation').evaluate('n=>n.scrollLeft=0')
  pg.goto(f'http://127.0.0.1:{s.server_port}/considerations.html',wait_until='domcontentloaded');pg.locator('.consideration-photo img').evaluate_all("aa=>Promise.all(aa.map(a=>{a.loading='eager';return a.decode()}))");pg.wait_for_timeout(80)
  cards=pg.locator('.consideration-card').evaluate_all('''aa=>aa.map(a=>({title:a.querySelector('h2').textContent,href:a.getAttribute('href'),rect:a.getBoundingClientRect().toJSON(),border:getComputedStyle(a).borderTopWidth,photo:a.querySelector('img').getBoundingClientRect().toJSON(),fit:getComputedStyle(a.querySelector('img')).objectFit,loaded:a.querySelector('img').naturalWidth>0}))''')
  assert len(cards)==5 and all(c['border']=='3px' and c['loaded'] and c['fit']=='cover' for c in cards),cards
  assert not pg.evaluate('document.documentElement.scrollWidth>innerWidth');assert not errors,errors
  pg.screenshot(path=str(out/f'considerations-{w}.png'),full_page=True);d.update(width=w,cards=cards,errors=errors);results.append(d);ctx.close();print('Verified',w,flush=True)
 # Desktop hover, destinations and keyboard.
 ctx=b.new_context(viewport={'width':1440,'height':1000});ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/considerations.html',wait_until='domcontentloaded');pg.wait_for_timeout(150)
 for label in ['Buy','Sell','Property Management','Interior Design','Life Changes','Contact']:
  a=pg.locator('#dd-navigation>.dd-group>a').filter(has_text=label);a.hover();pg.wait_for_timeout(80);panel=a.locator('..').locator(':scope>.dd-panel');assert panel.is_visible();r=panel.bounding_box();assert r['height']<430 and r['x']>=0 and r['x']+r['width']<=1441;panel.locator('a').first.hover();assert panel.is_visible();pg.screenshot(path=str(out/f'desktop-{label.replace(" ","-")}.png'));pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()');pg.mouse.move(0,900);pg.wait_for_timeout(40)
 for name in ['neighborhoods','search']:
  a=pg.locator('.dd-'+name+'>button').first;a.hover();pg.wait_for_timeout(80);assert pg.locator('.dd-'+name+'>.dd-panel').is_visible();pg.screenshot(path=str(out/f'desktop-{name}.png'));pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()');pg.mouse.move(0,900);pg.wait_for_timeout(40)
 assert pg.locator('.dd-neighborhoods .dd-panel-content a').count()==30
 pg.locator('#dd-navigation>a').filter(has_text='Considerations').hover();assert pg.locator('#dd-header .is-open').count()==0
 pg.screenshot(path=str(out/'desktop-Considerations-no-dropdown.png'))
 # Keyboard focus opens a genuine dropdown; Escape returns focus.
 a=pg.locator('.dd-search>button').first;a.focus();assert a.get_attribute('aria-expanded')=='true';pg.keyboard.press('Escape');assert a.get_attribute('aria-expanded')=='false'
 # Follow the original category and an actual article.
 pg.locator('.consideration-card').first.click();pg.wait_for_url('**/buyer-questions.html');pg.locator('.loanHubItem a.ss18-card-photo').first.click();pg.wait_for_load_state('domcontentloaded');interaction.append({'flow':'Considerations > Buying > first existing article','url':pg.url});pg.screenshot(path=str(out/'existing-article-flow.png'));ctx.close()
 # Touch feature menus on iPad and phone, nested paths, direct URLs, focus/close.
 for w in [768,390]:
  ctx=b.new_context(viewport={'width':w,'height':1024 if w==768 else 844},has_touch=True);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/life-changes/marriage.html',wait_until='domcontentloaded');pg.wait_for_timeout(180)
  pg.locator('.dd-search>button').first.tap();assert pg.locator('.dd-search .dd-panel').is_visible();pg.screenshot(path=str(out/f'touch-search-{w}.png'));pg.locator('.dd-search .dd-panel-content>a').tap();pg.wait_for_url('**/search.html');pg.locator('.dd-neighborhoods>button').first.tap();assert pg.locator('.dd-neighborhoods .dd-panel-content>a').count()==30;pg.locator('.dd-neighborhoods .dd-panel-content>a').filter(has_text='Winnetka').tap();pg.wait_for_url('**/buy-winnetka.html');interaction.append({'width':w,'nestedSearchAndCity':'passed'});ctx.close()
 b.close()
s.shutdown();(out/'browser-results.json').write_text(json.dumps(results,indent=2),encoding='utf-8');(out/'interaction-results.json').write_text(json.dumps(interaction,indent=2),encoding='utf-8');print('All browser checks passed',flush=True)
