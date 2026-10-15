import sys,os,threading,http.server,functools,json
from pathlib import Path
sys.path.insert(0,os.path.join(os.environ['TEMP'],'dommydom-browser-tools-complete'))
from playwright.sync_api import sync_playwright
class Q(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Q,directory=str(Path.cwd())));threading.Thread(target=s.serve_forever,daemon=True).start()
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True);pg=b.new_page(viewport={'width':1920,'height':1000});pg.route('https://**/*',lambda r:r.abort());pg.goto(f'http://127.0.0.1:{s.server_port}/life-changes.html',wait_until='load')
 print(json.dumps(pg.locator('.loanHubItem').nth(5).evaluate('''c=>{const e=c.querySelector('.final-static-answer-copy'),body=e.parentElement;const st=getComputedStyle(e);function walk(rs){return [...rs].flatMap(r=>r.styleSheet?walk(r.styleSheet.cssRules):r.cssRules?[r,...walk(r.cssRules)]:[r])};return {rect:e.getBoundingClientRect().toJSON(),width:st.width,maxWidth:st.maxWidth,minWidth:st.minWidth,justifySelf:st.justifySelf,gridColumn:st.gridColumn,columns:getComputedStyle(body).gridTemplateColumns,body:body.getBoundingClientRect().toJSON(),matches:[...document.styleSheets].flatMap(s=>{try{return walk(s.cssRules)}catch{return []}}).filter(r=>r.selectorText&&e.matches(r.selectorText)&&/width|grid-column|justify-self/.test(r.style.cssText)).map(r=>r.cssText)}}'''),indent=2),flush=True)
 pg.close();b.close()
s.shutdown()
