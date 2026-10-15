import sys, os, json, threading, functools, http.server, hashlib
from pathlib import Path
sys.path.insert(0,os.path.join(os.environ['TEMP'],'dommydom-browser-tools-complete'))
from playwright.sync_api import sync_playwright
root=Path.cwd();out=root/'design-corrections-audit'
class Quiet(http.server.SimpleHTTPRequestHandler):
    protocol_version='HTTP/1.1'
    def log_message(self,*args):pass
class Server(http.server.ThreadingHTTPServer):
    request_queue_size=128
    def handle_error(self,*args):pass
server=Server(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/';results=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
    context=browser.new_context(viewport={'width':1440,'height':1000})
    context.route('https://**/*',lambda r:r.abort())
    page=context.new_page()
    for path in ['blog.html','life-changes/marriage.html','life-changes/growing-family.html','life-changes/empty-nest.html','buy-winnetka.html','buy-sun-valley.html']:
        for width in [1440,390]:
            page.set_viewport_size({'width':width,'height':1000})
            page.goto(base+path,wait_until='load');page.wait_for_timeout(250)
            data={'page':path,'width':width}
            link=page.locator('.loanHubGrid .loanLearn a').first
            if link.count():
                target=link.get_attribute('href');link.click(trial=True);link.focus()
                data['focusVisible']=link.evaluate('a=>getComputedStyle(a).outlineStyle')=='solid'
                link.press('Enter');page.wait_for_load_state('domcontentloaded')
                data['readMoreNavigation']=page.url.endswith(target)
                page.go_back(wait_until='load')
            if width==390:
                toggle=page.locator('.ss22-menu-toggle');toggle.click()
                data['mobileMenuOpens']=toggle.get_attribute('aria-expanded')=='true'
                page.keyboard.press('Escape')
                data['mobileMenuCloses']=toggle.get_attribute('aria-expanded')=='false'
            else:
                group=page.locator('#ss22-navigation .ss22-group').first
                group.hover();data['desktopDropdownVisible']=group.locator('.ss22-panel').is_visible()
                page.mouse.move(0,0)
            trigger=page.locator('main [data-sun-conversation-open="true"]').first
            if trigger.count():
                trigger.click();dialog=page.locator('#sun-conversation')
                data['chatOpens']=dialog.is_visible()
                choices=dialog.locator('.sunConversation__choice')
                data['chatChoicesVisible']=choices.count()>0 and choices.first.is_visible()
                if choices.count():choices.first.click()
                dialog.locator('.sunConversation__close').click()
                data['chatCloses']=not dialog.is_visible()
            if path.startswith('buy-'):
                data['searchFieldsPreserved']=page.locator('.searchBar :is(input,select)').count()==4
                data['citySelected']=page.locator('.searchBar select[name="city"]').input_value()
            results.append(data);print(json.dumps(data),flush=True)
    page.close();context.close();browser.close()
manifest=json.loads((out/'html-sha256-before.json').read_text())
changed=[path for path,digest in manifest.items() if hashlib.sha256((root/path).read_bytes()).hexdigest()!=digest]
(out/'functionality.json').write_text(json.dumps({'checks':results,'changedHTML':changed,'htmlFilesVerified':len(manifest)},indent=2))
server.shutdown()
