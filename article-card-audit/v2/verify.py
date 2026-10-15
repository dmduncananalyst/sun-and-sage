import sys, os, json, threading, http.server, functools
from pathlib import Path
sys.path.insert(0, os.path.join(os.environ['TEMP'], 'dommydom-browser-tools-complete'))
from playwright.sync_api import sync_playwright

root = Path.cwd()
out = root / 'article-card-audit/v2'
baseline = '--before' in sys.argv
quick = '--quick' in sys.argv
class Quiet(http.server.SimpleHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    def log_message(self, *args): pass
class LocalServer(http.server.ThreadingHTTPServer):
    request_queue_size = 128
    def handle_error(self, request, client_address): pass
server = LocalServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
threading.Thread(target=server.serve_forever, daemon=True).start()
pages = [root/'blog.html', root/'life-changes/marriage.html'] if baseline or quick else [p for p in root.rglob('*.html') if 'final-static-answer' in p.read_text(encoding='utf-8') and p.name != 'questions.html']
widths = [1440,390] if baseline else [1440,1280,1024,768,390]
results = []
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe', headless=True)
    context = browser.new_context(viewport={'width':1440,'height':1000}, device_scale_factor=1)
    context.route('https://**/*', lambda r:r.abort())
    if baseline:
        for name in ['75e3427875dcf211','295473f8529b44f9','ad2a85f2e8cb67b7']:
            css = (out/(name+'-before.css')).read_text()
            context.route('**/'+name+'.css', lambda r, request, css=css:r.fulfill(body=css,content_type='text/css'))
    page = context.new_page()
    for path in pages:
        for width in widths:
            page.set_viewport_size({'width':width,'height':1000})
            page.goto(f'http://127.0.0.1:{server.server_port}/'+path.relative_to(root).as_posix(), wait_until='load')
            page.evaluate('''async()=>{
                const imgs=[...document.querySelectorAll('.loanHubGrid img')];
                imgs.slice(0,6).forEach(i=>i.loading='eager');
                await Promise.race([Promise.all(imgs.slice(0,6).map(i=>i.decode().catch(()=>{}))),new Promise(r=>setTimeout(r,2000))]);
                await document.fonts.ready;
            }''')
            page.wait_for_timeout(300)
            data = page.evaluate('''()=>({overflow:document.documentElement.scrollWidth>innerWidth,
              cards:[...document.querySelectorAll('.loanHubGrid > .loanHubItem:has(> .ss18-card-photo):has(> .loanLearn)')].map(c=>{
                const r=c.getBoundingClientRect(),s=getComputedStyle(c),body=c.querySelector('.final-static-answer'),ex=c.querySelector('.final-static-answer-copy'),link=c.querySelector('.loanLearn a'),f=c.querySelector('.loanLearn'),h=c.querySelector('h2'),im=c.querySelector('img');
                const es=getComputedStyle(ex),hs=getComputedStyle(h),ls=link.getBoundingClientRect(),fs=getComputedStyle(f),ir=im?.getBoundingClientRect();
                return {top:r.top,bottom:r.bottom,height:r.height,width:r.width,linkBottom:ls.bottom,blank:ls.top-ex.getBoundingClientRect().bottom,
                 frame:[s.borderTopWidth,s.borderRightWidth,s.borderBottomWidth,s.borderLeftWidth],color:s.borderTopColor,footer:fs.backgroundColor,footerRule:fs.borderTopColor,
                 clamp:es.webkitLineClamp,excerptHeight:ex.clientHeight,excerptLineHeight:es.lineHeight,headline:h.textContent,headlineClipped:h.scrollHeight>h.clientHeight+1||hs.overflow==='hidden',
                 href:link.getAttribute('href'),linkVisible:ls.width>0&&ls.height>0,imageLoaded:!im||im.complete&&im.naturalWidth>0,imageSrc:im?.getAttribute('src'),imageFit:im&&getComputedStyle(im).objectFit,imageRatio:ir&&ir.width/ir.height,
                 rowRule:getComputedStyle(c.parentElement).gridAutoRows,bodyFlex:getComputedStyle(body).flexGrow};
              })})''')
            rows = {}
            for card in data['cards']:
                rows.setdefault(round(card['top']), []).append(card)
            data['aligned'] = all(max(c['bottom'] for c in row)-min(c['bottom'] for c in row)<2 and max(c['linkBottom'] for c in row)-min(c['linkBottom'] for c in row)<2 for row in rows.values())
            data.update(page=path.relative_to(root).as_posix(),width=width,columns=max(map(len,rows.values())))
            if path.name in ['blog.html','marriage.html']:
                link = page.locator('.loanHubGrid .loanLearn a').first
                link.click(trial=True)
                link.focus()
                data['focusOutline'] = link.evaluate('a=>getComputedStyle(a).outlineStyle')
                if not baseline and width in [1440,390]:
                    target=link.get_attribute('href')
                    link.click()
                    page.wait_for_load_state('domcontentloaded')
                    data['clickDestinationCorrect'] = page.url.endswith(target)
                    page.go_back(wait_until='load')
                    page.wait_for_timeout(300)
                page.evaluate('document.activeElement?.blur()')
                page.locator('.loanHubGrid').evaluate('(g,w)=>window.scrollTo(0,g.getBoundingClientRect().top+scrollY-(w>820?180:20))',width)
                page.screenshot(path=str(out/f'{path.stem}-{"before" if baseline else "after"}-{width}.png'))
            results.append(data)
            (out/('before.json' if baseline else 'results-quick.json' if quick else 'results.json')).write_text(json.dumps(results,indent=2))
            print(path.relative_to(root),width,'aligned',data['aligned'],'overflow',data['overflow'],'max gap',round(max(c['blank'] for c in data['cards'])),'headline clips',sum(c['headlineClipped'] for c in data['cards']),flush=True)
    page.close()
    context.close()
    browser.close()
server.shutdown()
