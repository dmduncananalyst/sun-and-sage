import sys,json,threading,http.server,functools,asyncio
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'.smooth-video-tools'))
from playwright.async_api import async_playwright
root=Path.cwd();audit=root/'smooth-video-audit'
class Quiet(http.server.SimpleHTTPRequestHandler):
 protocol_version='HTTP/1.1'
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
record=r"""
window.smoothAudit={playCalls:0,pauseCalls:0,seekWrites:0,rateWrites:0,events:[],samples:[]};
const a=window.smoothAudit,p=HTMLMediaElement.prototype,play=p.play,pause=p.pause;
p.play=function(){if(this.id==='home-introduction-video')a.playCalls++;return play.apply(this,arguments)};
p.pause=function(){if(this.id==='home-introduction-video')a.pauseCalls++;return pause.apply(this,arguments)};
for(const [key,count] of [['currentTime','seekWrites'],['playbackRate','rateWrites']]){const d=Object.getOwnPropertyDescriptor(p,key);Object.defineProperty(p,key,{...d,set(value){if(this.id==='home-introduction-video')a[count]++;d.set.call(this,value)}})}
function state(){const v=document.getElementById('home-introduction-video');if(!v)return null;const h=v.closest('.videoHero');return {wall:performance.now(),media:v.currentTime,paused:v.paused,rate:v.playbackRate,opening:h.classList.contains('ss23-opening'),finished:h.classList.contains('ss23-doors-finished')};}
setInterval(()=>{const s=state();if(s)a.samples.push(s)},50);
for(const name of ['playing','pause','waiting','seeking','seeked','ended','error'])document.addEventListener(name,e=>{if(e.target.id==='home-introduction-video')a.events.push({name,...state()})},true);
for(const name of ['animationstart','animationend'])document.addEventListener(name,e=>{if(e.animationName==='rightOpen')a.events.push({name,...state()})},true);
"""
async def run():
 results=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
  for width in [1440,390]:
   for mode in ['normal-loop','slow-media','blocked-autoplay','media-error','reduced-motion','manual-pause']:
    context=await browser.new_context(viewport={'width':width,'height':1000 if width==1440 else 844},is_mobile=width==390,has_touch=width==390,reduced_motion='reduce' if mode=='reduced-motion' else 'no-preference');await context.route('https://**/*',lambda route:route.abort());await context.add_init_script(record)
    if mode=='slow-media':
     async def slow(route):await asyncio.sleep(3);await route.continue_()
     await context.route('**/videos/home-introduction-*.mp4',slow)
    if mode=='blocked-autoplay':await context.add_init_script("const native=HTMLMediaElement.prototype.play;let attempts=0;HTMLMediaElement.prototype.play=function(){if(this.id==='home-introduction-video'&&++attempts===1){window.smoothAudit.playCalls++;return Promise.reject(new DOMException('Test autoplay block','NotAllowedError'))}return native.apply(this,arguments)}")
    if mode=='media-error':await context.route('**/videos/home-introduction-*.mp4',lambda route:route.abort())
    page=await context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));await page.goto(base+'index.html',wait_until='domcontentloaded',timeout=60000)
    if mode=='blocked-autoplay':
     button=page.get_by_role('button',name='Play Dominique’s introduction video');await button.wait_for(state='visible');await page.wait_for_timeout(400);await button.click()
    if mode=='media-error':
     await page.wait_for_function("document.querySelector('.videoHero').classList.contains('ss23-doors-finished')");await page.get_by_role('button',name='Play Dominique’s introduction video').wait_for(state='visible');await page.wait_for_timeout(200)
    else:
     await page.wait_for_function("window.smoothAudit.events.some(e=>e.name==='playing')");await page.wait_for_timeout(11000 if mode=='normal-loop' else 2500)
    if mode=='manual-pause':
     await page.locator('#home-introduction-video').evaluate('v=>v.pause()');await page.wait_for_timeout(750)
    data=await page.evaluate("() => ({...window.smoothAudit,source:document.querySelector('#home-introduction-video').currentSrc,paused:document.querySelector('#home-introduction-video').paused,media:document.querySelector('#home-introduction-video').currentTime,loop:document.querySelector('#home-introduction-video').loop,rate:document.querySelector('#home-introduction-video').playbackRate,doorsFinished:document.querySelector('.videoHero').classList.contains('ss23-doors-finished'),fallbackLabel:document.querySelector('.videoHero>button')?.textContent,quality:{frames:document.querySelector('#home-introduction-video').getVideoPlaybackQuality().totalVideoFrames,dropped:document.querySelector('#home-introduction-video').getVideoPlaybackQuality().droppedVideoFrames}})")
    playing=next((e for e in data['events'] if e['name']=='playing'),None);pauses=[e for e in data['events'] if e['name']=='pause' and playing and e['wall']>playing['wall']]
    passed=not errors and data['seekWrites']==0 and data['rateWrites']==0 and data['doorsFinished'] and data['rate']==1
    if mode=='manual-pause':passed=passed and data['paused'] and data['playCalls']==1 and data['pauseCalls']==1
    elif mode=='media-error':passed=passed and data['fallbackLabel']=='Open video' and data['pauseCalls']==0
    else:passed=passed and not data['paused'] and not pauses and data['pauseCalls']==0 and data['playCalls']==(2 if mode=='blocked-autoplay' else 1)
    if mode=='normal-loop':passed=passed and data['loop'] and 0<data['media']<5
    result={'width':width,'mode':mode,'pass':passed,'errors':errors,**data};results.append(result)
    print(width,mode,'pass',passed,'play calls',data['playCalls'],'pause calls',data['pauseCalls'],'seek writes',data['seekWrites'],'errors',errors,flush=True);await context.close()
  await browser.close()
 (audit/'browser-checks.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
asyncio.run(run());server.shutdown()
