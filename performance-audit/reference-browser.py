import sys,json,threading,http.server,functools,asyncio
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'.codex-tools'))
from playwright.async_api import async_playwright
root=Path.cwd()
class Quiet(http.server.SimpleHTTPRequestHandler):
 protocol_version='HTTP/1.1'
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start()
refs=sorted({r['page'] for r in json.loads((root/'performance-audit/inventory.json').read_text())['references']})
async def run():
 results=[];sem=asyncio.Semaphore(3)
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
  for width in [1440,390]:
   context=await browser.new_context(viewport={'width':width,'height':1000 if width==1440 else 844});await context.route('https://**/*',lambda route:route.abort())
   # Media is unnecessary for checking source links; detailed visual tests load it separately.
   cache={}
   async def local_resource(route):
    from urllib.parse import urlparse,unquote
    req=route.request
    if req.url.startswith('https://') or req.resource_type in ['image','media','script','font']: await route.abort();return
    file=root/unquote(urlparse(req.url).path).lstrip('/')
    if not file.is_file(): await route.fulfill(status=404,body='');return
    if file not in cache:cache[file]=file.read_bytes()
    await route.fulfill(body=cache[file],content_type='text/css' if file.suffix=='.css' else 'text/html')
   await context.route('**/*',local_resource)
   async def check(name):
    async with sem:
     page=await context.new_page()
     try:
      await page.goto(f'http://127.0.0.1:{server.server_port}/'+name,wait_until='load',timeout=60000)
      items=await page.locator('.source-reference-links a[href]').evaluate_all("els => els.map(a=>({name:a.textContent,url:a.href,underline:getComputedStyle(a).textDecorationLine,color:getComputedStyle(a).color,width:a.getBoundingClientRect().width,visible:a.getBoundingClientRect().height>0}))")
      first=page.locator('.source-reference-links a[href]').first;await first.focus()
      focus=await first.evaluate("a=>({visible:a.matches(':focus-visible'),style:getComputedStyle(a).outlineStyle,width:getComputedStyle(a).outlineWidth})")
      result={'page':name,'width':width,'links':items,'focus':focus,'pass':bool(items) and all(a['visible'] and a['width']>0 and 'underline' in a['underline'] for a in items) and focus['style']!='none' and focus['width']!='0px'}
     except Exception as e:result={'page':name,'width':width,'pass':False,'error':str(e)}
     results.append(result);await page.close()
   await asyncio.gather(*(check(name) for name in refs));await context.close();print(width,'checked',len(refs),'pages',flush=True)
  await browser.close()
 (root/'performance-audit/reference-browser.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
 print('Failures:',json.dumps([r for r in results if not r['pass']],indent=2),flush=True)
asyncio.run(run());server.shutdown()

