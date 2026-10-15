exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'ipad-cards-date-audit'
selectors=['.loanHubGrid','.considerations-grid','.ss22-services-grid','.ss22-project-grid','.homePortfolioVideosGrid','.portfolioParentGrid','.dd-design-paths','.dd-design-editorial','.ss43-detail-grid','.ss43-process-grid','.ss34-platform-grid','.ss24-review-grid','.ss24-consultation-topics','.ss21-fact-grid','.ss-city-card-grid','.ss23-regions','.estateRoutes','.f4-breakdown','.ss24-roadmap','.ss24-eligibility','.ss90-eval-grid','.dd-buy-benefits','.dd-buy-reach-grid','.v12-pm-service-list','.v4-stats','.v4-ranks','.sageStatRail','.ss22-city-highlights','.ss22-platform-stats','.ss22-print-gallery','.ss23-awards>div']
inventory=json.load(open(out/'before-grids.json'))
paths=[]
for p in inventory:
 if any(g['cls'] and any('.'+g['cls'].split()[0]==sel for sel in selectors) for g in p['grids']):paths.append(p['page'])
failures=[];results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 pg=b.new_page(viewport={'width':1024,'height':1000});pg.route('https://**/*',lambda r:r.abort())
 for index,path in enumerate(paths):
  pg.goto(f'http://127.0.0.1:{s.server_port}/'+path,wait_until='domcontentloaded')
  for w in [600,768,820,1024,1180]:
   pg.set_viewport_size({'width':w,'height':1000})
   data=pg.locator('main').evaluate_all('''(ms,sels)=>ms.flatMap(m=>[...m.querySelectorAll(sels.join(','))].filter(e=>e.children.length>1&&e.getClientRects().length).map(e=>({cls:e.className,columns:getComputedStyle(e).gridTemplateColumns.split(' ').length,width:e.clientWidth,scroll:e.scrollWidth})))''',selectors)
   for d in data:
    if d['columns']!=2 or d['scroll']>d['width']+2:failures.append({'page':path,'width':w,**d})
   results.append({'page':path,'width':w,'grids':data})
  if path in ['seller-questions.html','life-changes.html','considerations.html','buyer-questions.html','blog.html']:
   pg.set_viewport_size({'width':1024,'height':1000});pg.screenshot(path=str(out/(Path(path).stem+'-1024.png')))
  if index%10==0:print('Checked',index+1,'of',len(paths),'card pages',flush=True)
 b.close()
s.shutdown();(out/'after-grids.json').write_text(json.dumps(results,indent=2));(out/'failures.json').write_text(json.dumps(failures,indent=2));print('TOTAL',len(results),'FAILURES',json.dumps(failures),flush=True)
