import sys,json,threading,time,http.server,functools
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'.codex-tools'))
from playwright.sync_api import sync_playwright
root=Path.cwd(); phase=sys.argv[1]
handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(root))
class Quiet(handler.func):
 protocol_version='HTTP/1.1'
 def log_message(self,*args): pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for width,height in [(1440,1000),(390,844)]:
  context=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1)
  context.route('https://**/*',lambda route:route.abort())
  for name in ['index.html','first-time-your-offer.html','blog.html','blog-california-proposition-19-homeowners.html','portfolio.html','life-changes/retirement/should-i-downsize-when-i-retire.html']:
   page=context.new_page(); errors=[]; page.on('pageerror',lambda err:errors.append(str(err)))
   page.add_init_script("window.auditCLS=0;new PerformanceObserver(l=>l.getEntries().forEach(e=>{if(!e.hadRecentInput)window.auditCLS+=e.value})).observe({type:'layout-shift',buffered:true})")
   page.goto(f'http://127.0.0.1:{server.server_port}/'+name,wait_until='load');page.wait_for_timeout(1500)
   metrics=page.evaluate("""() => ({cls:window.auditCLS, timing:performance.getEntriesByType('navigation')[0].toJSON(),resources:performance.getEntriesByType('resource').map(r=>({name:r.name,bytes:r.transferSize,duration:r.duration})), overflow:document.documentElement.scrollWidth>innerWidth, geometry:[...document.querySelectorAll('header,main,main h1,main figure,footer')].map(e=>({tag:e.tagName,cls:e.className,rect:JSON.stringify(e.getBoundingClientRect().toJSON()),font:getComputedStyle(e).font})),refs:[...document.querySelectorAll('main a')].filter(a=>a.closest('.blogReferences,.ss4711-sources,.article-sources,.sources,.resources')).map(a=>({text:a.textContent,underline:getComputedStyle(a).textDecorationLine}))})""")
   page.screenshot(path=str(root/'performance-audit'/f'{phase}-{width}-{name.replace("/","_")}.png'))
   results.append({'page':name,'width':width,'errors':errors,**metrics});page.close()
  page=context.new_page();page.goto(f'http://127.0.0.1:{server.server_port}/first-time-your-offer.html',wait_until='load')
  if width<800: page.locator('.ss22-menu-toggle').click();page.wait_for_timeout(250)
  start=time.monotonic();page.locator('#ss22-navigation a[href="blog.html"]').click(force=True);page.wait_for_url('**/blog.html',timeout=30000)
  results.append({'navigation':'offer to blog','width':width,'milliseconds':(time.monotonic()-start)*1000});context.close()
 browser.close()
(root/'performance-audit'/f'{phase}-browser.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps([{'page':r.get('page',r.get('navigation')),'width':r['width'],'load_ms':r.get('timing',{}).get('loadEventEnd'),'cls':r.get('cls'),'errors':r.get('errors'),'nav_ms':r.get('milliseconds')} for r in results],indent=2))
server.shutdown()

