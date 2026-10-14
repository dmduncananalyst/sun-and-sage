import sys,json,threading,http.server,functools
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'.codex-tools'))
from playwright.sync_api import sync_playwright
root=Path.cwd()
class Quiet(http.server.SimpleHTTPRequestHandler):
 protocol_version='HTTP/1.1'
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/';results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for width in [1440,390]:
  context=browser.new_context(viewport={'width':width,'height':1000 if width==1440 else 844});context.route('https://**/*',lambda route:route.fulfill(body='<title>Source destination test</title>',content_type='text/html') if route.request.resource_type=='document' else route.abort())
  page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(base+'first-time-your-offer.html',wait_until='load')
  for source in page.locator('.source-reference-links a[href]').all():
   expected=source.get_attribute('href')
   with page.expect_popup() as event:source.click()
   popup=event.value;popup.wait_for_load_state();results.append({'width':width,'test':'source click','url':expected,'pass':popup.url==expected});popup.close()
  source=page.locator('.source-reference-links a[href]').first;source.hover();results.append({'width':width,'test':'source hover','pass':source.evaluate("e=>getComputedStyle(e).textDecorationThickness")=='2px'})
  for destination in ['blog.html','index.html']:
   if width<800:page.locator('.ss22-menu-toggle').click()
   page.locator('#ss22-navigation a[href="'+destination+'"]').click();page.wait_for_url('**/'+destination);results.append({'width':width,'test':'navigation '+destination,'pass':True})
  if width<800:page.locator('.ss22-menu-toggle').click()
  group=page.locator('.ss22-group').filter(has=page.locator('a[href="portfolio.html"]'));group.locator(':scope > .ss22-top').hover() if width>=1280 else group.locator(':scope > .ss22-top').click();results.append({'width':width,'test':'dropdown','pass':group.locator(':scope > .ss22-top').get_attribute('aria-expanded')=='true'})
  group.locator('a[href="portfolio.html"]').click();page.wait_for_url('**/portfolio.html')
  page.locator('a.portfolioVideoThumb').first.click();dialog=page.locator('#portfolioVideoDialog');results.append({'width':width,'test':'portfolio video dialog','pass':dialog.evaluate('e=>e.open')});dialog.locator('.portfolioVideoClose').click();results.append({'width':width,'test':'portfolio video close','pass':not dialog.evaluate('e=>e.open')})
  page.goto(base+'index.html',wait_until='load');page.wait_for_timeout(2000);results.append({'width':width,'test':'home video playback','pass':page.locator('#home-introduction-video').evaluate('v=>!v.paused && v.readyState>=2')})
  trigger=page.locator('.sunInlineAction__button').first
  if trigger.count():
   trigger.click();chat=page.locator('#sun-conversation');results.append({'width':width,'test':'chat opens','pass':chat.is_visible()});chat.locator('.sunConversation__close').click();results.append({'width':width,'test':'chat closes','pass':not chat.is_visible()})
  else:results.append({'width':width,'test':'chat opens','pass':False,'reason':'trigger missing'})
  page.goto(base+'blog-why-budgeting-matters.html',wait_until='load');field=page.locator('[data-budget-field="income"]')
  if field.count():
   old=page.locator('#budget-balance').inner_text();field.fill('9999');results.append({'width':width,'test':'budget calculator','pass':page.locator('#budget-balance').inner_text()!=old})
  results.append({'width':width,'test':'runtime errors','pass':not errors,'errors':errors});context.close()
 browser.close()
(root/'performance-audit/interactions.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(json.dumps(results,indent=2));server.shutdown()
