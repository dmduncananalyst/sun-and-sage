import sys,os,threading,http.server,functools,json
from pathlib import Path
sys.path.insert(0,os.path.join(os.environ['TEMP'],'dommydom-browser-tools-complete'))
from playwright.sync_api import sync_playwright
class Q(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Q,directory=str(Path.cwd())));threading.Thread(target=s.serve_forever,daemon=True).start()
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True);pg=b.new_page();pg.route('https://**/*',lambda r:r.abort())
 for path in ['blog.html','life-changes/marriage.html']:
  for w in [1440,390]:
   pg.set_viewport_size({'width':w,'height':1000});pg.goto(f'http://127.0.0.1:{s.server_port}/'+path,wait_until='load')
   styles=pg.locator('.loanLearn a').evaluate_all('as=>as.map(a=>[getComputedStyle(a).borderBottomColor,getComputedStyle(a).borderBottomWidth])');assert all(x==['rgb(72, 83, 62)','1px'] for x in styles),styles
   print(path,w,'all',len(styles),'underlines sage, 1px',flush=True)
 pg.close();b.close()
s.shutdown()
