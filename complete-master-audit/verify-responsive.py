exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'complete-master-audit';widths=[320,375,390,430,600,650,744,768,820,834,1024,1180,1280,1366,1440,1920];expected=['Home','About','Buy','Sell','Property Management','Interior Design','Life Changes','Considerations','Blog','Contact'];results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in widths:
  ctx=b.new_context(viewport={'width':w,'height':1000 if w>=600 else 844},has_touch=w<1200,device_scale_factor=1);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();errors=[];pg.on('pageerror',lambda e:errors.append(str(e)));case={'width':w,'pages':{}}
  for file,label in [('index.html','home'),('considerations.html','considerations'),('life-changes.html','life'),('buy-a-home.html','buy')]:
   pg.goto(f'http://127.0.0.1:{s.server_port}/{file}',wait_until='domcontentloaded');pg.evaluate('document.fonts.ready');pg.wait_for_timeout(150)
   d=pg.locator('#dd-header').evaluate('''h=>({compact:h.classList.contains('is-compact'),rail:h.classList.contains('has-nav-rail'),navVisible:!!h.querySelector('nav').getClientRects().length,menuVisible:!!h.querySelector('.dd-menu-toggle').getClientRects().length,overflow:document.documentElement.scrollWidth>innerWidth,labels:[...h.querySelector('nav').children].filter(e=>e.matches('a,.dd-group')).map(e=>(e.matches('a')?e:e.querySelector('a')).textContent),direct:[...h.querySelectorAll('nav>a')].filter(a=>['Life Changes','Considerations'].includes(a.textContent)).map(a=>({text:a.textContent,hasPopup:a.hasAttribute('aria-haspopup'),expanded:a.hasAttribute('aria-expanded'),controls:a.hasAttribute('aria-controls')}))})''')
   assert d['labels']==expected and len(d['direct'])==2,(w,file,d);assert all(not x['hasPopup'] and not x['expanded'] and not x['controls'] for x in d['direct']);assert d['compact']==(w<600) and d['menuVisible']==(w<600) and d['navVisible']==(w>=600);assert not d['overflow'],(w,file)
   if label in ['considerations','life']:
    pg.locator('main img').evaluate_all("aa=>Promise.all(aa.map(a=>{a.loading='eager';return a.decode()}))");d['photos']=pg.locator('main img').evaluate_all('aa=>aa.map(i=>({src:i.getAttribute("src"),loaded:i.naturalWidth>0,rect:i.getBoundingClientRect().toJSON(),fit:getComputedStyle(i).objectFit}))');assert all(x['loaded'] for x in d['photos'])
    if label=='life':
     assert len(d['photos'])==7;assert len([i for i in d['photos'] if 'images/life-changes/' in i['src']])==5;assert all(abs(i['rect']['width']/i['rect']['height']-1.5)<.01 for i in d['photos']),d['photos']
     if w in [390,768,1440]:pg.locator('.loanHubItem').filter(has=pg.locator('h2',has_text='Empty Nest')).screenshot(path=str(out/f'empty-nest-card-{w}.png'));pg.evaluate('scrollTo(0,0)')
   if label=='buy':
    d['buy']=pg.locator('main').evaluate('''m=>({stages:[...m.querySelectorAll('.dd-buy-step span')].map(e=>e.textContent),charts:m.querySelectorAll('.dd-buy-chart').length,maps:m.querySelectorAll('.dd-buy-map svg').length,bitmapImages:m.querySelectorAll('img').length,barRatios:[...m.querySelectorAll('.dd-buy-bar-fill')].map(e=>({expected:parseFloat(e.style.height)/100,actual:e.offsetHeight/e.parentElement.offsetHeight})),text:m.innerText})''');assert len(d['buy']['stages'])==8 and d['buy']['charts']==2 and d['buy']['maps']==4 and d['buy']['bitmapImages']==0;assert all(abs(v['expected']-v['actual'])<.008 for v in d['buy']['barRatios'])
   pg.evaluate('scrollTo(0,0)');pg.screenshot(path=str(out/f'{label}-{w}.png'),full_page=label!='home')
   if label=='buy' and w in [390,768,1024,1440]:
    for selector,section in [('.dd-buy-overview','top'),('.dd-buy-statistics','middle'),('.dd-buy-reach','maps'),('.ss49-button-row','bottom')]:
     pg.locator(selector).evaluate('e=>e.scrollIntoView({block:"start"})');pg.screenshot(path=str(out/f'buy-{section}-{w}.png'))
   case['pages'][label]=d
  assert not errors,errors;case['errors']=errors;results.append(case);(out/'responsive-results.json').write_text(json.dumps(results,indent=2),encoding='utf-8');ctx.close();print('Passed four pages at',w,flush=True)
 b.close()
s.shutdown();print('All 64 page-and-width checks passed.')
