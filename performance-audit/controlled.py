import sys,json,threading,http.server,functools,subprocess,asyncio,time
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'.codex-tools'))
from playwright.async_api import async_playwright
root=Path.cwd()
class Quiet(http.server.SimpleHTTPRequestHandler):
 protocol_version='HTTP/1.1'
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start()
names=sys.argv[1:] or ['index.html','first-time-your-offer.html','blog.html','portfolio.html']
originals={n:subprocess.check_output(['git','show','HEAD:'+n],cwd=root).decode('utf-8') for n in names+['assets/photo-navigation-ready.js']}
async def run():
 results=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
  for width in [1440,390]:
   for name in names*int(__import__('os').environ.get('DOMMYDOM_AUDIT_REPEATS','1')):
    for phase in ['before','after']:
     context=await browser.new_context(viewport={'width':width,'height':1000 if width==1440 else 844})
     await context.route('https://**/*',lambda route:route.abort())
     if phase=='before':
      await context.route('**/'+name,lambda route,request,n=name:route.fulfill(body=originals[n],content_type='text/html'))
      await context.route('**/assets/photo-navigation-ready.js',lambda route:route.fulfill(body=originals['assets/photo-navigation-ready.js'],content_type='application/javascript'))
     page=await context.new_page();cdp=await context.new_cdp_session(page);await cdp.send('Network.enable');await cdp.send('Network.emulateNetworkConditions',{'offline':False,'latency':80,'downloadThroughput':3_000_000,'uploadThroughput':1_000_000})
     await page.add_init_script("window.auditCLS=0;window.auditLCP=0;window.auditFCPFont=null;new PerformanceObserver(l=>l.getEntries().forEach(e=>{if(e.name==='first-contentful-paint'){const h=document.querySelector('main h1');window.auditFCPFont=h?getComputedStyle(h).font:null}})).observe({type:'paint',buffered:true});new PerformanceObserver(l=>l.getEntries().forEach(e=>{if(!e.hadRecentInput)window.auditCLS+=e.value})).observe({type:'layout-shift',buffered:true});new PerformanceObserver(l=>l.getEntries().forEach(e=>window.auditLCP=e.startTime)).observe({type:'largest-contentful-paint',buffered:true})")
     await page.goto(f'http://127.0.0.1:{server.server_port}/'+name,wait_until='load',timeout=90000);await page.wait_for_timeout(500)
     r=await page.evaluate("() => ({font_at_first_paint:window.auditFCPFont,font_after_load:document.querySelector('main h1')?getComputedStyle(document.querySelector('main h1')).font:null,load_ms:performance.getEntriesByType('navigation')[0].loadEventEnd,fcp_ms:performance.getEntriesByName('first-contentful-paint')[0]?.startTime,lcp_ms:window.auditLCP,cls:window.auditCLS,css_requests:performance.getEntriesByType('resource').filter(r=>r.name.includes('.css')).length,bytes:performance.getEntriesByType('resource').reduce((s,r)=>s+r.transferSize,0)})")
     results.append({'phase':phase,'page':name,'width':width,**r});print(phase,width,name,round(r['load_ms']),r['css_requests'],round(r['bytes']/1e6,2),flush=True);await context.close()
  # Isolate the old navigation wait with deliberately slow destination images.
  for phase in ['before','after']:
   context=await browser.new_context(viewport={'width':1440,'height':1000});await context.route('https://**/*',lambda route:route.abort())
   if phase=='before':await context.route('**/assets/photo-navigation-ready.js',lambda route:route.fulfill(body=originals['assets/photo-navigation-ready.js'],content_type='application/javascript'))
   page=await context.new_page();await page.goto(f'http://127.0.0.1:{server.server_port}/first-time-your-offer.html',wait_until='load')
   async def slow_image(route):
    await asyncio.sleep(3)
    try:await route.continue_()
    except Exception:pass
   await context.route(re.compile(r'\.(png|jpg|jpeg|webp)(\?.*)?$'),slow_image)
   start=time.monotonic()
   await page.locator('#ss22-navigation a[href="blog.html"]').click(no_wait_after=True)
   await page.wait_for_url('**/blog.html',wait_until='commit',timeout=60000)
   results.append({'phase':phase,'test':'slow destination images','commit_ms':(time.monotonic()-start)*1000});print(results[-1],flush=True);await context.close()
  await browser.close()
 (root/'performance-audit'/('controlled-repeat.json' if sys.argv[1:] else 'controlled-performance.json')).write_text(json.dumps(results,indent=2),encoding='utf-8')
import re
asyncio.run(run());server.shutdown()

