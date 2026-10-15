import sys,os,threading,http.server,functools,json
from pathlib import Path
sys.path.insert(0,os.path.join(os.environ['TEMP'],'dommydom-browser-tools-complete'))
from playwright.sync_api import sync_playwright
root=Path.cwd();out=root/'design-corrections-audit'
class Q(http.server.SimpleHTTPRequestHandler):
 protocol_version='HTTP/1.1'
 def log_message(self,*a):pass
class S(http.server.ThreadingHTTPServer):
 request_queue_size=128
 def handle_error(self,*a):pass
s=S(('127.0.0.1',0),functools.partial(Q,directory=str(root)));threading.Thread(target=s.serve_forever,daemon=True).start();rs=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True);ctx=b.new_context();ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page()
 for name in ['marriage','growing-family','empty-nest']:
  for w in [1440,390]:
   pg.set_viewport_size({'width':w,'height':1000});pg.goto(f'http://127.0.0.1:{s.server_port}/life-changes/{name}.html',wait_until='load');pg.locator('main [data-sun-conversation-open="true"]').first.click();d=pg.locator('#sun-conversation')
   data=d.locator('.sunConversation__stage').evaluate('s=>({interactive:[...s.querySelectorAll("input,textarea,button,select")].some(e=>e.getClientRects().length&&!e.disabled),fields:[...s.querySelectorAll("input,textarea")].map(e=>e.name),text:s.textContent})')
   data.update(page=f'life-changes/{name}.html',width=w);rs.append(data);d.locator('.sunConversation__close').click();print(name,w,data['interactive'],data['fields'],flush=True)
 pg.close();ctx.close();b.close()
(out/'chat-stages.json').write_text(json.dumps(rs,indent=2));s.shutdown()
