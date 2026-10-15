import sys,os,json,re,time,threading,functools,http.server
from pathlib import Path
sys.path.insert(0,os.path.join(os.environ['TEMP'],'dommydom-browser-tools-complete'))
from playwright.sync_api import sync_playwright
root=Path.cwd();source=(root/'index.html').read_text(encoding='utf-8');brand=re.search(r'<a[^>]*class="ss22-brand".*?</a>',source,re.S)[0];logo=re.search(r'src="([^"]+)"',brand)[1]
class Q(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
 def do_GET(self):
  if self.path.split('?')[0].lstrip('/')==logo:time.sleep(3)
  super().do_GET()
class S(http.server.ThreadingHTTPServer):
 def handle_error(self,*a):pass
s=S(('127.0.0.1',0),functools.partial(Q,directory=str(root)));threading.Thread(target=s.serve_forever,daemon=True).start();results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,touch in [(1440,False),(390,True)]:
  ctx=b.new_context(viewport={'width':w,'height':900},has_touch=touch,is_mobile=touch);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/index.html',wait_until='domcontentloaded');early=pg.evaluate("document.readyState!=='complete'");a=pg.locator('.ss22-neighborhoods>button')
  if touch:a.tap()
  else:a.hover()
  before=pg.locator('.ss22-neighborhoods>.ss22-panel').is_visible();pg.wait_for_load_state('load');pg.wait_for_timeout(100);after=pg.locator('.ss22-neighborhoods>.ss22-panel').is_visible();d={'width':w,'openedBeforeLoadCompleted':early,'openInitially':before,'stillOpenAfterLoad':after,'passed':early and before and after};results.append(d);print(json.dumps(d),flush=True);ctx.close()
 b.close()
s.shutdown();(root/'header-hover-audit/late-load-results.json').write_text(json.dumps(results,indent=2))
