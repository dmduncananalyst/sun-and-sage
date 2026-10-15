exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'ipad-cards-date-audit';out.mkdir(exist_ok=True)
results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 pg=b.new_page(viewport={'width':1024,'height':900});pg.route('https://**/*',lambda r:r.abort())
 paths=list(root.glob('*.html'))+[p for p in (root/'life-changes').glob('*.html')]
 for path in paths:
  pg.goto(f'http://127.0.0.1:{s.server_port}/'+path.relative_to(root).as_posix(),wait_until='domcontentloaded')
  data=pg.locator('main').evaluate_all('''ms=>ms.flatMap(m=>[...m.querySelectorAll('*')].filter(e=>getComputedStyle(e).display==='grid'&&e.children.length>1).map(e=>({tag:e.tagName,cls:e.className,cols:getComputedStyle(e).gridTemplateColumns,children:[...e.children].slice(0,4).map(c=>({tag:c.tagName,cls:c.className,title:c.querySelector('h2,h3')?.textContent?.trim().slice(0,90)}))})))''')
  if data:results.append({'page':path.relative_to(root).as_posix(),'grids':data})
 b.close()
s.shutdown();(out/'before-grids.json').write_text(json.dumps(results,indent=2));print(json.dumps(results))
