import sys,os,json,threading,functools,http.server
from pathlib import Path
sys.path.insert(0,os.path.join(os.environ['TEMP'],'dommydom-browser-tools-complete'))
from playwright.sync_api import sync_playwright
root=Path.cwd();out=root/'header-hover-audit'
class Q(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
class S(http.server.ThreadingHTTPServer):
 request_queue_size=128
 def handle_error(self,*a):pass
s=S(('127.0.0.1',0),functools.partial(Q,directory=str(root)));threading.Thread(target=s.serve_forever,daemon=True).start();results=json.loads((out/'browser-results.json').read_text()) if (out/'browser-results.json').exists() else []
cases=[(1440,1000,False),(1280,800,False),(1024,768,True),(820,1180,True),(768,1024,True),(390,844,True),(320,720,True)]
pages=['index.html','buy-winnetka.html','life-changes/marriage/buying-a-home-together-when-one-spouse-already-owns-property.html','life-changes/divorce.html','blog/can-the-dodgers-do-a-threepeat-2026.html']
labels=['Home','About','Buy','Sell','Property Management','Interior Design','Life Changes','Blog','Contact']
geometry='''p=>{const r=p.getBoundingClientRect();return r.width>0&&r.left>=-1&&r.right<=innerWidth+1&&r.top>=-1&&r.bottom<=innerHeight+1&&p.scrollWidth<=p.clientWidth+1}'''
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for page in pages:
  for w,h,touch in cases:
   if any(x['page']==page and x['width']==w and not x['failures'] for x in results):continue
   ctx=b.new_context(viewport={'width':w,'height':h},has_touch=touch,is_mobile=touch,device_scale_factor=1);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();errors=[];pg.on('pageerror',lambda e:errors.append(str(e)));pg.goto(f'http://127.0.0.1:{s.server_port}/'+page,wait_until='domcontentloaded');pg.evaluate('document.fonts.ready');pg.wait_for_timeout(100)
   d=pg.evaluate('''()=>{const h=document.querySelector('#ss22-header'),n=h.querySelector('nav'),items=[...n.children].filter(e=>!e.matches('button')),rs=items.map(e=>(e.matches('a')?e:e.querySelector(':scope>a')).getBoundingClientRect()),tools=h.querySelectorAll('.ss22-feature-trigger'),ts=[...tools].map(e=>e.getBoundingClientRect());return {compact:h.classList.contains('ss22-compact-nav'),labels:items.map(e=>(e.matches('a')?e:e.querySelector(':scope>a')).textContent.trim()),oneRow:rs.every((r,i)=>Math.abs(r.top-rs[0].top)<2&&(!i||r.left-rs[i-1].right>=10)),controlsVisible:[...tools].every(e=>e.getClientRects().length&&e.textContent.trim()&&e.querySelector('svg')),controlsDoNotOverlap:ts[0].right<=ts[1].left,brandingVisible:!!h.querySelector('.ss22-brand').getClientRects().length&&!!h.querySelector('.ss22-rise').getClientRects().length,searchAfterNeighborhoods:tools[0].textContent.trim()==='Neighborhoods'&&tools[1].textContent.trim()==='Search',noPageOverflow:document.documentElement.scrollWidth<=innerWidth,noIndicators:[...h.querySelectorAll('a,button')].every(a=>['::before','::after'].every(p=>['none','normal','""'].includes(getComputedStyle(a,p).content)))}}''');d.update(page=page,width=w);d['exactLabels']=d.pop('labels')==labels
   opened=[];contained=[];transfer=[];flyoutok=[]
   # Feature controls must work independently of the main MENU.
   for name in ['neighborhoods','search']:
    group=pg.locator('.ss22-'+name);a=group.locator(':scope>button').first;panel=group.locator(':scope>.ss22-panel')
    if touch:a.tap()
    else:
     a.locator('svg').hover();opened.append(panel.is_visible());a.locator('span').hover()
    opened.append(panel.is_visible());contained.append(panel.evaluate(geometry))
    if name=='neighborhoods':
     d['neighborhoodCount']=panel.locator('a').count();d['allCitiesDirect']=panel.locator('a').evaluate_all('as=>as.every(a=>a.getAttribute("href")&&!a.getAttribute("href").startsWith("#"))');panel.locator('a').last.scroll_into_view_if_needed();d['lastCityReachable']=panel.locator('a').last.is_visible();panel.evaluate('p=>p.scrollTop=0')
    else:d['actualSearchOption']=panel.locator('a').count()==1 and panel.locator('a').inner_text()=='Personalized Home Search'
    if not touch:panel.locator('a').first.hover();pg.wait_for_timeout(300);transfer.append(panel.is_visible())
    if page=='index.html':pg.screenshot(path=str(out/f'{w}-{name}.png'))
    if touch:
     d[name+'LocksBackground']=pg.evaluate("getComputedStyle(document.body).overflow==='hidden'");panel.locator('.ss22-feature-close').tap();pg.wait_for_timeout(10)
    else:pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()');pg.wait_for_timeout(30);pg.mouse.move(0,h-1)
   if d['compact']:pg.locator('.ss22-menu-toggle').click()
   for i,group in enumerate(pg.locator('#ss22-navigation>.ss22-group').all()):
    a=group.locator(':scope>a');panel=group.locator(':scope>.ss22-panel');name=a.text_content().strip()
    if touch:a.tap()
    else:a.hover()
    opened.append(panel.is_visible());contained.append(pg.locator('#ss22-navigation').evaluate(geometry) if d['compact'] else panel.evaluate(geometry))
    if name=='Buy':
     d['buyHasFiveEntries']=panel.locator('.ss22-panel-content').evaluate('e=>e.children.length===5');d['buyHasNoCities']=panel.locator('a[href*="buy-winnetka"]').count()==0;d['compactBuyPanel']=d['compact'] or panel.bounding_box()['width']<300 and panel.bounding_box()['height']<240
     for j,f in enumerate(group.locator('.ss22-flyout').all()):
      if d['compact']:flyoutok.append(f.locator('.ss22-flyout-panel').is_visible());continue
      if not touch:a.hover()
      if not panel.is_visible():
       if touch:a.tap()
       else:a.hover()
      if touch:f.locator(':scope>a').tap()
      else:f.locator(':scope>a').hover()
      fp=f.locator(':scope>.ss22-flyout-panel');flyoutok.append(fp.is_visible() and fp.evaluate(geometry))
      if not touch:fp.locator('a').first.hover();pg.wait_for_timeout(50);transfer.append(fp.is_visible())
      if page=='index.html':pg.screenshot(path=str(out/f'{w}-buy-flyout-{j}.png'))
      pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()');pg.wait_for_timeout(30)
    if not panel.is_visible():
     if touch:a.tap()
     else:a.hover()
    if page=='index.html':pg.screenshot(path=str(out/(f'{w}-'+{'Buy':'buy','Sell':'sell','Property Management':'management','Interior Design':'design','Life Changes':'life','Contact':'contact'}[name]+'.png')))
    if not touch:
     panel.locator('a').first.hover();pg.wait_for_timeout(60);transfer.append(panel.is_visible());pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()');pg.wait_for_timeout(30)
    elif d['compact']:pg.locator('.ss22-nav-back').click()
    else:pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()');pg.wait_for_timeout(30)
   if d['compact']:pg.locator('.ss22-menu-toggle').click()
   pg.wait_for_timeout(20);d['allDropdownsOpen']=all(opened);d['panelsStayInViewport']=all(contained);d['hoverTransfer']=all(transfer);d['buyGroupsWork']=all(flyoutok);d['bodyRestored']=pg.evaluate("getComputedStyle(document.body).overflow!=='hidden'&&!document.querySelector('main').inert");d['errors']=errors
   required=['exactLabels','controlsVisible','controlsDoNotOverlap','brandingVisible','searchAfterNeighborhoods','noPageOverflow','noIndicators','allCitiesDirect','lastCityReachable','actualSearchOption','buyHasFiveEntries','buyHasNoCities','compactBuyPanel','allDropdownsOpen','panelsStayInViewport','hoverTransfer','buyGroupsWork','bodyRestored']+(['neighborhoodsLocksBackground','searchLocksBackground'] if touch else [])+([] if d['compact'] else ['oneRow'])
   d['failures']=[k for k in required if not d.get(k)]+(['cityCount'] if d['neighborhoodCount']!=30 else [])+(['scriptErrors'] if errors else []);results.append(d);(out/'browser-results.json').write_text(json.dumps(results,indent=2));print(json.dumps(d),flush=True);ctx.close()
 b.close()
s.shutdown()
