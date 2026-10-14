import sys,threading,http.server,functools,json
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'.door-test-tools'))
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
root=Path.cwd()
class Quiet(http.server.SimpleHTTPRequestHandler):
 protocol_version='HTTP/1.1'
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 page=browser.new_page(viewport={'width':960,'height':600});page.route('**/',lambda route:route.fulfill(body='<html><body></body></html>',content_type='text/html'));page.goto(base)
 results=[]
 for name in ['home-introduction.mp4','home-introduction-web.mp4','home-introduction-mobile.mp4']:
  page.evaluate("name=>{document.body.innerHTML='';const v=document.createElement('video');v.muted=true;v.preload='auto';v.src='assets/videos/'+name;v.style.cssText='width:640px;height:420px;object-fit:contain;background:white';document.body.append(v)}",name)
  page.wait_for_function('document.querySelector("video").readyState>=2');v=page.locator('video');results.append(page.evaluate("name=>({name,duration:document.querySelector('video').duration,width:document.querySelector('video').videoWidth,height:document.querySelector('video').videoHeight})",name))
  frames=[]
  page.evaluate('document.querySelector("video").play()')
  for t in [0,.4,.8,1.2,1.6,2,2.5,3,4]:
   page.wait_for_function('t=>document.querySelector("video").currentTime>=t',arg=t)
   actual=page.evaluate('document.querySelector("video").currentTime')
   file=root/'door-timing-audit'/f'{name}-{t}.png';v.screenshot(path=str(file));frame=Image.open(file).convert('RGB');frame.thumbnail((320,210));tile=Image.new('RGB',(320,240),'white');tile.paste(frame,(0,0));ImageDraw.Draw(tile).text((8,215),f'{name}: {actual:.2f}s',fill='black');frames.append(tile)
  print(name,page.evaluate('document.querySelector("video").getVideoPlaybackQuality().toJSON()' if False else 'JSON.stringify(document.querySelector("video").getVideoPlaybackQuality())'),flush=True)
  page.evaluate('document.querySelector("video").pause()')
  sheet=Image.new('RGB',(960,720),'white')
  for i,frame in enumerate(frames):sheet.paste(frame,((i%3)*320,(i//3)*240))
  sheet.save(root/'door-timing-audit'/f'{name}-playing-frames.jpg')
 (root/'door-timing-audit/video-metadata.json').write_text(json.dumps(results,indent=2));print(results)
 browser.close()
server.shutdown()
