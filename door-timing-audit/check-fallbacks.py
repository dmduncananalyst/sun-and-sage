import sys,json,threading,http.server,functools,asyncio
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'.door-test-tools'))
from playwright.async_api import async_playwright
root=Path.cwd();audit=root/'door-timing-audit'
class Quiet(http.server.SimpleHTTPRequestHandler):
 protocol_version='HTTP/1.1'
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
async def run():
 results=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
  for width in [1440,390]:
   for mode in ['reveal-preview','blocked-playback','animation-event-fallback','media-error','loop']:
    context=await browser.new_context(viewport={'width':width,'height':1000 if width==1440 else 844},is_mobile=width==390,has_touch=width==390);await context.route('https://**/*',lambda route:route.abort())
    if mode=='blocked-playback':await context.add_init_script("const native=HTMLMediaElement.prototype.play;let attempts=0;HTMLMediaElement.prototype.play=function(){return ++attempts===1?Promise.reject(new DOMException('Test autoplay block','NotAllowedError')):native.call(this)}")
    if mode=='animation-event-fallback':await context.add_init_script("document.addEventListener('animationend',e=>{if(e.animationName==='rightOpen')e.stopImmediatePropagation()},true)")
    if mode=='media-error':await context.route('**/videos/home-introduction-*.mp4',lambda route:route.abort())
    page=await context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));await page.goto(base+'index.html',wait_until='domcontentloaded');await page.wait_for_function("document.querySelector('.videoHero').classList.contains('ss23-doors-finished')")
    if mode=='reveal-preview':
     state=await page.locator('#home-introduction-video').evaluate('v=>({time:v.currentTime,paused:v.paused})');await page.locator('.videoHero').screenshot(path=str(audit/f'reveal-facing-{width}.png'));passed=state['time']<=.05 and state['paused']
    elif mode=='blocked-playback':
     button=page.get_by_role('button',name='Play Dominique’s introduction video');await button.wait_for(state='visible');await button.click();await page.wait_for_function("!document.querySelector('#home-introduction-video').paused");passed=True
    elif mode=='media-error':
     button=page.get_by_role('button',name='Play Dominique’s introduction video');passed=await button.is_visible() and await button.inner_text()=='Open video'
    elif mode=='loop':
     await page.wait_for_function("!document.querySelector('#home-introduction-video').paused");await page.wait_for_timeout(11000);state=await page.locator('#home-introduction-video').evaluate('v=>({time:v.currentTime,paused:v.paused,loop:v.loop,rate:v.playbackRate})');passed=not state['paused'] and state['loop'] and state['rate']==1 and state['time']<5
    else:
     await page.wait_for_function("!document.querySelector('#home-introduction-video').paused");passed=True
    results.append({'width':width,'test':mode,'pass':passed and not errors,'errors':errors});print(results[-1],flush=True);await context.close()
  await browser.close()
 (audit/'edge-checks.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
asyncio.run(run());server.shutdown()
