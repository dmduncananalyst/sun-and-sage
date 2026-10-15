import sys,os,json,re,hashlib,threading,functools,http.server
from pathlib import Path
sys.path.insert(0,os.path.join(os.environ['TEMP'],'dommydom-browser-tools-complete'))
from playwright.sync_api import sync_playwright
root=Path.cwd();out=root/'responsive-header-audit';records=[]
for name in json.loads((root/'header-hover-audit/changed-header-pages.json').read_text()):
 s=(root/name).read_bytes().decode();h=re.search(r'<header\b[^>]*id="ss22-header"[^>]*>.*?</header>',s,re.S);records.append({'page':name,'oldHeader':h[0],'outsideHash':hashlib.sha256((s[:h.start()]+'<HEADER/>'+s[h.end():]).encode()).hexdigest()})
(out/'headers-before.json').write_text(json.dumps(records,indent=2));print('Saved',len(records),'live header baselines.',flush=True)
class Q(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
class S(http.server.ThreadingHTTPServer):
 def handle_error(self,*a):pass
s=S(('127.0.0.1',0),functools.partial(Q,directory=str(root)));threading.Thread(target=s.serve_forever,daemon=True).start()
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h,touch in [(650,900,False),(1366,900,False),(390,844,True),(768,1024,True)]:
  c=b.new_context(viewport={'width':w,'height':h},has_touch=touch,is_mobile=touch);c.route('https://**/*',lambda r:r.abort());pg=c.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/index.html',wait_until='domcontentloaded');pg.evaluate('document.fonts.ready');pg.wait_for_timeout(150);pg.screenshot(path=str(out/'before'/f'{w}-closed.png'))
  if w in [390,768]:pg.locator('.ss22-menu-toggle').tap();pg.screenshot(path=str(out/'before'/f'{w}-menu.png'))
  print('Captured before',w,flush=True);c.close()
 b.close()
s.shutdown()
