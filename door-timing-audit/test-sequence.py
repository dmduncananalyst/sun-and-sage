import sys,json,threading,http.server,functools,asyncio,base64,hashlib
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'.door-test-tools'))
from playwright.async_api import async_playwright
from PIL import Image,ImageDraw
root=Path.cwd();audit=root/'door-timing-audit'
class Quiet(http.server.SimpleHTTPRequestHandler):
 protocol_version='HTTP/1.1'
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
recorder=r"""
window.doorAudit={events:[],samples:[],frames:[],finishedAt:null};
const audit=window.doorAudit;
function state(){const v=document.getElementById('home-introduction-video'),h=v?.closest('.videoHero'),d=h?.querySelector('.doors>div:last-child');if(!v)return null;return {wall:performance.now(),media:v.currentTime,paused:v.paused,rate:v.playbackRate,ready:v.readyState,opening:h.classList.contains('ss23-opening'),finished:h.classList.contains('ss23-doors-finished'),transform:d?getComputedStyle(d).transform:null,animation:d?getComputedStyle(d).animation:null};}
function capture(label){const v=document.getElementById('home-introduction-video');if(!v||v.readyState<2)return;const c=document.createElement('canvas');c.width=320;c.height=180;c.getContext('2d').drawImage(v,0,0,320,180);audit.frames.push({label,...state(),png:c.toDataURL('image/png').split(',')[1]});}
setInterval(()=>{const s=state();if(s){audit.samples.push(s);if(s.finished&&audit.finishedAt===null){audit.finishedAt=s.wall;capture('doors fully open');for(const delay of [250,500,900,1100,1600,2400])setTimeout(()=>capture('reveal + '+delay+'ms'),delay)}}},40);
for(const name of ['loadeddata','playing','pause','seeked','waiting','error'])document.addEventListener(name,e=>{if(e.target.id==='home-introduction-video')audit.events.push({name,...state()})},true);
for(const name of ['animationstart','animationend'])document.addEventListener(name,e=>{if(e.animationName==='rightOpen')audit.events.push({name,animationName:e.animationName,...state()})},true);
"""
async def run():
 results=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
  cases=[('before',1440,'normal'),('before',390,'normal'),('after',1440,'normal'),('after',390,'normal'),('after',1440,'slow-media'),('after',390,'slow-media'),('after',1440,'reduced-motion'),('after',390,'reduced-motion')]
  for phase,width,mode in (cases if len(sys.argv)==1 else [c for c in cases if c[0]=='after']):
   context=await browser.new_context(viewport={'width':width,'height':1000 if width==1440 else 844},is_mobile=width==390,has_touch=width==390,reduced_motion='reduce' if mode=='reduced-motion' else 'no-preference')
   await context.route('https://**/*',lambda route:route.abort())
   if phase=='before':
    await context.route('**/index.html',lambda route:route.fulfill(body=(audit/'index-before.html').read_bytes(),content_type='text/html'))
    await context.route('**/home-playback-v23.js*',lambda route:route.fulfill(body=(audit/'home-playback-before.js').read_bytes(),content_type='application/javascript'))
   if mode=='slow-media':
    async def slow(route):await asyncio.sleep(3);await route.continue_()
    await context.route('**/videos/home-introduction-*.mp4',slow)
   page=await context.new_page();errors=[];page.on('pageerror',lambda error:errors.append(str(error)));await page.add_init_script(recorder)
   await page.goto(base+'index.html',wait_until='domcontentloaded',timeout=60000)
   await page.wait_for_function('window.doorAudit.finishedAt!==null',timeout=20000)
   await page.wait_for_timeout(3200)
   data=await page.evaluate("() => ({...window.doorAudit,source:document.querySelector('#home-introduction-video').currentSrc,load:performance.getEntriesByType('navigation')[0].toJSON(),fcp:performance.getEntriesByName('first-contentful-paint')[0]?.startTime,quality:{frames:document.querySelector('video').getVideoPlaybackQuality().totalVideoFrames,dropped:document.querySelector('video').getVideoPlaybackQuality().droppedVideoFrames},video: {media:document.querySelector('video').currentTime,paused:document.querySelector('video').paused,rate:document.querySelector('video').playbackRate},header:document.querySelector('#ss22-header').getBoundingClientRect().toJSON()})")
   key=f'{phase}-{width}-{mode}';frames=[]
   for frame in data['frames']:
    file=audit/f'{key}-{frame["label"].replace(" ","-")}.png';file.write_bytes(base64.b64decode(frame.pop('png')));frame['file']=file.name
    tile=Image.new('RGB',(320,220),'white');tile.paste(Image.open(file).convert('RGB'),(0,0));ImageDraw.Draw(tile).text((7,186),f'{frame["label"]}: video {frame["media"]:.2f}s',fill='black');frames.append(tile)
   sheet=Image.new('RGB',(320*len(frames),220),'white')
   for i,tile in enumerate(frames):sheet.paste(tile,(320*i,0))
   sheet.save(audit/f'{key}-sequence.jpg')
   await page.locator('.videoHero').screenshot(path=str(audit/f'{key}-hero.png'))
   result={'phase':phase,'width':width,'mode':mode,'errors':errors,**data};results.append(result)
   print(key,'finish at',round(data['finishedAt']),'frame at finish',data['frames'][0]['media'] if data['frames'] else None,'play events',[(e['name'],round(e['wall'])) for e in data['events'] if e['name']=='playing'],'errors',errors,flush=True)
   await context.close()
  await browser.close()
 (audit/('browser-sequences-final.json' if len(sys.argv)>1 else 'browser-sequences.json')).write_text(json.dumps(results,indent=2),encoding='utf-8')
asyncio.run(run());server.shutdown()
