import sys, os, json, threading, functools, http.server, hashlib
from pathlib import Path
sys.path.insert(0, os.path.join(os.environ['TEMP'], 'dommydom-browser-tools-complete'))
from playwright.sync_api import sync_playwright
root=Path.cwd();out=root/'article-card-audit/v2'
class Quiet(http.server.SimpleHTTPRequestHandler):
    protocol_version='HTTP/1.1'
    def log_message(self,*args):pass
class Server(http.server.ThreadingHTTPServer):
    request_queue_size=128
    def handle_error(self,*args):pass
server=Server(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/'
results={}
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
    for mode in ['before','after']:
        context=browser.new_context(viewport={'width':1440,'height':1000},device_scale_factor=1)
        context.route('https://**/*',lambda r:r.abort())
        if mode=='before':
            for name in ['75e3427875dcf211','295473f8529b44f9','ad2a85f2e8cb67b7']:
                css=(out/(name+'-before.css')).read_text()
                context.route('**/'+name+'.css',lambda r,request,css=css:r.fulfill(body=css,content_type='text/css'))
        page=context.new_page();records=[]
        for path in ['blog.html','life-changes/marriage.html']:
            for width in [1440,390]:
                page.set_viewport_size({'width':width,'height':1000})
                page.goto(base+path,wait_until='load')
                page.evaluate('document.fonts.ready')
                page.wait_for_timeout(350)
                info=page.evaluate('''()=>({text:document.querySelector('.loanHubGrid').textContent,
                  titles:[...document.querySelectorAll('.loanHubGrid h2')].map(h=>h.textContent),
                  links:[...document.querySelectorAll('.loanHubGrid a')].map(a=>a.getAttribute('href')),
                  images:[...document.querySelectorAll('.loanHubGrid img')].map(i=>({src:i.getAttribute('src'),srcset:i.getAttribute('srcset'),fit:getComputedStyle(i).objectFit,ratio:i.clientWidth/i.clientHeight})),
                  metadata:[...document.querySelectorAll('meta,link[rel="canonical"]')].map(e=>e.outerHTML)})''')
                if mode=='after':
                    link=page.locator('.loanHubGrid .loanLearn a').first
                    target=link.get_attribute('href');link.focus();link.press('Enter')
                    page.wait_for_load_state('domcontentloaded')
                    info['keyboardDestinationCorrect']=page.url.endswith(target)
                    page.go_back(wait_until='load')
                    page.wait_for_timeout(350)
                    index=3
                    row_height=page.locator('.loanHubGrid > .loanHubItem').nth(index).evaluate('c=>c.getBoundingClientRect().height')
                    page.set_viewport_size({'width':width,'height':round(row_height)+(204 if width>820 else 44)})
                    page.locator('.loanHubGrid > .loanHubItem').nth(index).evaluate('(c,w)=>window.scrollTo(0,c.getBoundingClientRect().top+scrollY-(w>820?180:20))',width)
                    page.evaluate('async()=>{const images=[...document.querySelectorAll(".loanHubGrid img")].slice(0,6);images.forEach(i=>i.loading="eager");await Promise.race([Promise.all(images.map(i=>i.decode().catch(()=>{}))),new Promise(r=>setTimeout(r,2000))]);}')
                    page.screenshot(path=str(out/f'{Path(path).stem}-after-{width}-row2.png'))
                records.append({'page':path,'width':width,**info})
        if mode=='after':
            unrelated=[]
            for path in ['index.html','buy-sun-valley.html','questions.html','blog-what-its-like-to-live-in-granada-hills.html','life-changes/marriage/should-we-buy-a-house-before-or-after-getting-married.html']:
                page.goto(base+path,wait_until='domcontentloaded')
                matches=page.locator('.loanHubGrid > .loanHubItem:has(> .ss18-card-photo):has(> .loanLearn)').count()
                unrelated.append({'page':path,'newFrameMatches':matches})
            results['unrelated']=unrelated
        results[mode]=records
        page.close();context.close()
    browser.close()
checks=[]
for before,after in zip(results['before'],results['after']):
    checks.append({'page':after['page'],'width':after['width'],
        'contentAndLinksUnchanged':all(before[k]==after[k] for k in ['text','titles','links','metadata']),
        'imageSourcesFitAndRatioUnchanged':all(a['src']==b['src'] and a['srcset']==b['srcset'] and a['fit']==b['fit'] and abs(a['ratio']-b['ratio'])<.005 for a,b in zip(before['images'],after['images'])),
        'keyboardDestinationCorrect':after['keyboardDestinationCorrect']})
results['checks']=checks
(out/'preservation.json').write_text(json.dumps(results,indent=2))
print(json.dumps(checks,indent=2),flush=True)
server.shutdown()
