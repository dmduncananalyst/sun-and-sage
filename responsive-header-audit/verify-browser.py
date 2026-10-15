import sys,os,json,threading,functools,http.server
from pathlib import Path
sys.path.insert(0,os.path.join(os.environ['TEMP'],'dommydom-browser-tools-complete'))
from playwright.sync_api import sync_playwright
root=Path.cwd();out=root/'responsive-header-audit'
class Q(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
class S(http.server.ThreadingHTTPServer):
 request_queue_size=128
 def handle_error(self,*a):pass
s=S(('127.0.0.1',0),functools.partial(Q,directory=str(root)));threading.Thread(target=s.serve_forever,daemon=True).start();results=json.loads((out/'browser-results.json').read_text()) if (out/'browser-results.json').exists() else []
cases=[(1280,900),(1366,900),(1440,1000),(1920,1080),(320,720),(375,812),(390,844),(430,932),(650,900),(680,900),(768,1024),(900,1000),(1024,768)]
pages=['index.html','buy-a-home.html','sell-a-home.html','life-changes/marriage.html','buy-winnetka.html','blog.html'];labels=['Home','About','Buy','Sell','Property Management','Interior Design','Life Changes','Blog','Contact']
geom='''e=>{const r=e.getBoundingClientRect();return r.width>0&&r.left>=-1&&r.right<=innerWidth+1&&r.top>=-1&&r.bottom<=innerHeight+1&&e.scrollWidth<=e.clientWidth+1}'''
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for page in pages:
  for touch in [False,True]:
   sizes=[x for x in cases if (x[0]<1280)==touch];ctx=b.new_context(viewport={'width':sizes[0][0],'height':sizes[0][1]},has_touch=touch,is_mobile=touch,device_scale_factor=1);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();errors=[];pg.on('pageerror',lambda e:errors.append(str(e)));pg.goto(f'http://127.0.0.1:{s.server_port}/'+page,wait_until='domcontentloaded');pg.evaluate('document.fonts.ready');pg.wait_for_timeout(150)
   for w,h in sizes:
    if any(x['page']==page and x['width']==w and not x['failures'] and abs(x['headerHeight']-(137 if w>=1280 else 116 if w==320 else 132))<=1 for x in results):continue
    results=[x for x in results if not(x['page']==page and x['width']==w)]
    pg.set_viewport_size({'width':w,'height':h});pg.wait_for_timeout(90);pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()');pg.mouse.move(0,h-1)
    d=pg.evaluate('''()=>{const h=document.querySelector('#dd-header'),n=h.querySelector('nav'),cats=[...n.children].filter(e=>e.matches('a,.dd-group')),as=cats.map(e=>e.matches('a')?e:e.querySelector(':scope>a')),rs=as.map(e=>e.getBoundingClientRect()),brand=h.querySelector('.dd-brand').getBoundingClientRect(),rise=h.querySelector('.dd-rise').getBoundingClientRect(),ts=[...h.querySelectorAll('.dd-feature-trigger,.dd-menu-toggle')].filter(e=>e.getClientRects().length).map(e=>e.getBoundingClientRect()),compact=h.classList.contains('is-compact');return {compact,headerHeight:h.offsetHeight,labels:as.map(e=>e.textContent.trim()),gridBands:getComputedStyle(h).gridTemplateRows.split(' ').length,brandingSeparate:brand.right+15<=rise.left,brandingSameBand:Math.abs((brand.top+brand.height/2)-(rise.top+rise.height/2))<2,controlsSeparate:ts.every((r,i)=>r.height>=44&&r.left>=0&&r.right<=innerWidth&&(!i||r.left-ts[i-1].right>=11)),controlsOneBand:ts.every(r=>Math.abs(r.top-ts[0].top)<2),noPageOverflow:document.documentElement.scrollWidth<=innerWidth,contactVisible:!!h.querySelector('.dd-contact-strip').getClientRects().length,oneNavRow:rs.every((r,i)=>Math.abs(r.top-rs[0].top)<2&&(!i||r.left-rs[i-1].right>=21)),noIndicators:as.concat([...h.querySelectorAll('.dd-feature-trigger')]).every(a=>['::before','::after'].every(p=>['none','normal','""'].includes(getComputedStyle(a,p).content))),signatureWidth:brand.width,riseWidth:rise.width,navFont:parseFloat(getComputedStyle(as[0]).fontSize)}}''');d.update(page=page,width=w);d['exactLabels']=d.pop('labels')==labels
    if page=='index.html':pg.screenshot(path=str(out/f'{w}-closed.png'))
    opened=[];bounded=[];transfer=[];flyout=[]
    if d['compact']:
     pg.locator('.dd-menu-toggle').tap();n=pg.locator('#dd-navigation');d['openMenuBounded']=n.evaluate(geom);d['menuWidthControlled']=n.bounding_box()['width']<=481;d['contactsInsideMenu']=n.locator('.dd-contact-strip a').count()==3 and n.locator('.dd-contact-strip').is_visible();d['contactsTouchTargets']=n.locator('.dd-contact-strip a').evaluate_all('as=>as.every(a=>a.getBoundingClientRect().height>=44)');d['onlyNineInitially']=n.locator(':scope>.dd-group>.dd-panel:visible').count()==0;d['utilityVisibleWithoutScrolling']=n.locator('.dd-contact-strip').evaluate('e=>e.getBoundingClientRect().bottom<=innerHeight');d['backgroundLocked']=pg.evaluate("getComputedStyle(document.body).overflow==='hidden'")
     if page=='index.html':pg.screenshot(path=str(out/f'{w}-menu.png'))
    for group in pg.locator('#dd-navigation>.dd-group').all():
     a=group.locator(':scope>a');panel=group.locator(':scope>.dd-panel');name=a.text_content().strip()
     if touch:a.tap()
     else:a.hover()
     opened.append(panel.is_visible());bounded.append(pg.locator('#dd-navigation').evaluate(geom) if d['compact'] else panel.evaluate(geom))
     if d['compact']:
      d['inlineKeepsCategories']=pg.locator('#dd-navigation>a').first.is_visible() and pg.locator('#dd-navigation>.dd-group').last.is_visible()
      if name=='Buy':d['mobileBuyNotArticleDump']=panel.locator('a:visible').count()<=7
     elif name=='Buy':
      d['smallBuy']=panel.bounding_box()['width']<=260 and panel.bounding_box()['height']<230
      for j,f in enumerate(group.locator('.dd-flyout').all()):
       a.hover();f.locator(':scope>a').hover();fp=f.locator(':scope>.dd-flyout-panel');flyout.append(fp.is_visible() and fp.evaluate(geom));fp.locator('a').first.hover();transfer.append(fp.is_visible())
       if page=='index.html':pg.screenshot(path=str(out/f'{w}-buy-flyout-{j}.png'))
       pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()');pg.wait_for_timeout(20)
      a.hover()
     if page=='index.html':pg.screenshot(path=str(out/(str(w)+'-'+{'Buy':'buy','Sell':'sell','Property Management':'management','Interior Design':'design','Life Changes':'life','Contact':'contact'}[name]+'.png')))
     if d['compact']:a.tap()
     else:panel.locator('a:visible').first.hover();pg.wait_for_timeout(50);transfer.append(panel.is_visible());pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()');pg.wait_for_timeout(20)
    if d['compact']:pg.locator('.dd-menu-toggle').tap()
    for name in ['neighborhoods','search']:
     group=pg.locator('.dd-'+name);a=group.locator(':scope>button');panel=group.locator(':scope>.dd-panel')
     if touch:a.tap()
     else:a.locator('svg').hover();opened.append(panel.is_visible());a.locator('span').hover()
     opened.append(panel.is_visible());bounded.append(panel.evaluate(geom))
     if name=='neighborhoods':d['all30Cities']=panel.locator('a').count()==30;panel.locator('a').last.scroll_into_view_if_needed();d['lastCityReachable']=panel.locator('a').last.is_visible();panel.evaluate('p=>p.scrollTop=0')
     else:d['searchOptionUnchanged']=panel.locator('a').text_content().strip()=='Personalized Home Search'
     if not touch:panel.locator('a').first.hover();pg.wait_for_timeout(80);transfer.append(panel.is_visible())
     if page=='index.html':pg.screenshot(path=str(out/f'{w}-{name}.png'))
     if touch:panel.locator('.dd-feature-close').tap()
     else:pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()');pg.mouse.move(0,h-1);pg.wait_for_timeout(20)
    pg.wait_for_timeout(20);d['allDropdownsOpen']=all(opened);d['panelsBounded']=all(bounded);d['hoverTransfer']=all(transfer);d['desktopFlyouts']=all(flyout);d['bodyRestored']=pg.evaluate("getComputedStyle(document.body).overflow!=='hidden'&&!document.querySelector('main').inert");d['errors']=list(errors)
    checks=['exactLabels','brandingSeparate','brandingSameBand','controlsSeparate','controlsOneBand','noPageOverflow','noIndicators','all30Cities','lastCityReachable','searchOptionUnchanged','allDropdownsOpen','panelsBounded','hoverTransfer','desktopFlyouts','bodyRestored']+(['openMenuBounded','menuWidthControlled','contactsInsideMenu','contactsTouchTargets','onlyNineInitially','utilityVisibleWithoutScrolling','backgroundLocked','inlineKeepsCategories','mobileBuyNotArticleDump'] if d['compact'] else ['oneNavRow','smallBuy']);d['failures']=[k for k in checks if not d.get(k)]+(['bands'] if d['gridBands']!=2 else [])+(['headerTooTall'] if d['headerHeight']>145 else [])+(['closedContactPlacement'] if d['contactVisible']==d['compact'] else [])+(['scriptErrors'] if errors else [])+(['inconsistentHeaderProportions'] if abs(d['headerHeight']-(137 if w>=1280 else 116 if w==320 else 132))>1 else []);results.append(d);(out/'browser-results.json').write_text(json.dumps(results,indent=2));print(json.dumps({'page':page,'width':w,'compact':d['compact'],'height':d['headerHeight'],'failures':d['failures']}),flush=True)
   ctx.close()
 b.close()
s.shutdown()
