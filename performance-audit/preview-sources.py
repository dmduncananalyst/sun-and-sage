import sys,threading,http.server,functools
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'.codex-tools'))
from playwright.sync_api import sync_playwright
root=Path.cwd()
class Quiet(http.server.SimpleHTTPRequestHandler):
 protocol_version='HTTP/1.1'
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for width in [1440,390]:
  context=browser.new_context(viewport={'width':width,'height':1000 if width==1440 else 844});context.route('https://**/*',lambda route:route.abort());page=context.new_page()
  page.goto(f'http://127.0.0.1:{server.server_port}/first-time-your-offer.html',wait_until='load');section=page.locator('.source-reference-links').first;section.scroll_into_view_if_needed();section.locator('a').first.focus();section.screenshot(path=str(root/'performance-audit'/f'sources-{width}.png'));context.close()
 browser.close()
server.shutdown()
