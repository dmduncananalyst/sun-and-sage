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
s=S(('127.0.0.1',0),functools.partial(Q,directory=str(root)));threading.Thread(target=s.serve_forever,daemon=True).start()
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True);pg=b.new_page(viewport={'width':1024,'height':1200});pg.route('https://**/*',lambda r:r.abort());pg.goto(f'http://127.0.0.1:{s.server_port}/life-changes/death.html',wait_until='load');pg.evaluate('document.fonts.ready')
 pg.evaluate('async()=>{const imgs=[...document.querySelectorAll(".loanHubGrid img")].slice(0,3);imgs.forEach(i=>i.loading="eager");await Promise.race([Promise.all(imgs.map(i=>i.decode().catch(()=>{}))),new Promise(r=>setTimeout(r,2500))]);}')
 card=pg.locator('.loanHubItem').first;h=card.evaluate('c=>c.getBoundingClientRect().height');pg.set_viewport_size({'width':1024,'height':round(h+215)});card.evaluate('c=>scrollTo(0,c.getBoundingClientRect().top+scrollY-180)');pg.screenshot(path=str(out/'long-excerpts-death-1024.png'));pg.close();b.close()
s.shutdown()
