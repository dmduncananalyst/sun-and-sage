import sys, os, json, threading, functools, http.server
from pathlib import Path
sys.path.insert(0, os.path.join(os.environ['TEMP'], 'dommydom-browser-tools-complete'))
from playwright.sync_api import sync_playwright

root=Path.cwd();out=root/'design-corrections-audit'
before='--before' in sys.argv;quick='--quick' in sys.argv
recheck='--recheck-cards' in sys.argv
hub='--recheck-hub' in sys.argv
class Quiet(http.server.SimpleHTTPRequestHandler):
    protocol_version='HTTP/1.1'
    def log_message(self,*args):pass
class Server(http.server.ThreadingHTTPServer):
    request_queue_size=128
    def handle_error(self,*args):pass
server=Server(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/'
cards=[p for p in root.rglob('*.html') if 'final-static-answer' in p.read_text(encoding='utf-8') and p.name!='questions.html']
cities=[p for p in root.glob('buy-*.html') if 'data-city-page=' in p.read_text(encoding='utf-8')]
pages=[root/p for p in ['blog.html','life-changes/marriage.html','buy-winnetka.html','buy-sun-valley.html']] if quick or before else cards+cities
if recheck:pages=cards
if hub:pages=[root/'life-changes.html']
widths=[1440,390] if before else [1440,768,390] if quick else [1920,1440,1280,1024,768,390,320]
results=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
    context=browser.new_context(viewport={'width':1440,'height':1000},device_scale_factor=1)
    context.route('https://**/*',lambda r:r.abort())
    if before:
        for name in ['75e3427875dcf211','295473f8529b44f9','ad2a85f2e8cb67b7']:
            css=(out/'before'/(name+'.css')).read_text()
            context.route('**/'+name+'.css',lambda r,request,css=css:r.fulfill(body=css,content_type='text/css'))
    page=context.new_page()
    for path in pages:
        is_city=path in cities
        for width in widths:
            page.set_viewport_size({'width':width,'height':1000})
            page.goto(base+path.relative_to(root).as_posix(),wait_until='load')
            page.evaluate('document.fonts.ready')
            page.wait_for_timeout(180)
            common=page.evaluate('''()=>({overflow:document.documentElement.scrollWidth>innerWidth,
             pageText:document.querySelector('main').textContent,
             metadata:[...document.querySelectorAll('meta,link[rel="canonical"],script[type="application/ld+json"]')].map(e=>e.outerHTML),
             links:[...document.querySelectorAll('main a')].map(a=>a.getAttribute('href'))})''')
            if is_city:
                data=page.evaluate('''()=>{const g=document.querySelector('.ss21-fact-grid');return {kind:'city',columns:getComputedStyle(g).gridTemplateColumns,
                 panels:[...g.children].map(c=>{const r=c.getBoundingClientRect(),s=getComputedStyle(c),children=[...c.children];return {top:r.top,bottom:r.bottom,height:r.height,width:r.width,background:s.backgroundColor,border:s.borderTopWidth,borderColor:s.borderTopColor,
                 alignment:children.map(e=>getComputedStyle(e).textAlign),lefts:children.map(e=>e.getBoundingClientRect().left),
                 clipped:children.some(e=>e.scrollHeight>e.clientHeight+1||e.scrollWidth>e.clientWidth+1),text:c.textContent};})}}''')
            else:
                data=page.evaluate('''()=>({kind:'cards',cards:[...document.querySelectorAll('.loanHubGrid>.loanHubItem:has(>.ss18-card-photo):has(>.loanLearn)')].map(c=>{
                 const r=c.getBoundingClientRect(),s=getComputedStyle(c),b=c.querySelector('.final-static-answer'),ex=c.querySelector('.final-static-answer-copy'),h=c.querySelector('h2'),t=c.querySelector('.topic'),f=c.querySelector('.loanLearn'),a=f.querySelector('a'),im=c.querySelector('img');
                 const br=b.getBoundingClientRect(),er=ex.getBoundingClientRect(),hr=h.getBoundingClientRect(),tr=t.getBoundingClientRect(),fr=f.getBoundingClientRect(),ar=a.getBoundingClientRect(),ir=im.getBoundingClientRect();
                 const ps=[...ex.querySelectorAll('p')].filter(e=>e.getClientRects().length);const last=ps.at(-1)?.getBoundingClientRect();
                 const rule=e=>{const x=e.getBoundingClientRect(),st=getComputedStyle(e);return {left:x.left,right:x.right,top:x.top,width:st.borderTopWidth,color:st.borderTopColor};};
                 return {top:r.top,bottom:r.bottom,height:r.height,width:r.width,left:r.left,right:r.right,
                  frame:[s.borderTopWidth,s.borderRightWidth,s.borderBottomWidth,s.borderLeftWidth],color:s.borderTopColor,
                  rules:[rule(b),rule(ex),rule(f)],titleTop:hr.top,titleBottom:hr.bottom,categoryTop:tr.top,excerptTop:er.top,footerTop:fr.top,linkBottom:ar.bottom,
                  gap:fr.top-(last?.bottom||er.bottom),text:ex.textContent,title:h.textContent,href:a.getAttribute('href'),
                  clipped:[h,t,...ps].some(e=>e.scrollHeight>e.clientHeight+1||e.scrollWidth>e.clientWidth+1),clamp:getComputedStyle(ex).webkitLineClamp,
                  linkVisible:ar.width>0&&ar.height>0,bodyFlex:getComputedStyle(b).flexGrow,rowRule:getComputedStyle(c.parentElement).gridAutoRows,
                  image:{src:im.getAttribute('src'),srcset:im.getAttribute('srcset'),fit:getComputedStyle(im).objectFit,ratio:ir.width/ir.height,top:ir.top,bottom:ir.bottom,loaded:im.complete&&im.naturalWidth>0}};
                })})''')
                rows={}
                for c in data['cards']:rows.setdefault(round(c['top']),[]).append(c)
                data['columns']=max(map(len,rows.values()))
                data['aligned']=all(all(max(c[k] for c in row)-min(c[k] for c in row)<2 for k in ['bottom','categoryTop','titleTop','excerptTop','footerTop','linkBottom']) for row in rows.values())
                data['fullWidthRules']=all(all(abs(rule['left']-(c['left']+float(c['frame'][0][:-2])))<1 and abs(rule['right']-(c['right']-float(c['frame'][0][:-2])))<1 for rule in c['rules']) for c in data['cards'])
            data.update(common,page=path.relative_to(root).as_posix(),width=width)
            records=data.get('cards',data.get('panels',[]))
            print(data['page'],width,data['kind'],'overflow',data['overflow'],'clipped',sum(c['clipped'] for c in records),'aligned',data.get('aligned'),'full rules',data.get('fullWidthRules'),flush=True)
            key=path.name in ['blog.html','marriage.html','growing-family.html','empty-nest.html','buy-winnetka.html','buy-sun-valley.html']
            if key and (width in [1440,390] or path.name in ['blog.html','buy-winnetka.html']):
                selector='.ss21-facts' if is_city else '.loanHubGrid'
                page.locator(selector).evaluate('(g,args)=>window.scrollTo(0,g.getBoundingClientRect().top+scrollY-(args.width>820?(args.city?240:180):20))',{'width':width,'city':is_city})
                page.evaluate('async()=>{const imgs=[...document.images].filter(i=>{const r=i.getBoundingClientRect();return r.top<innerHeight&&r.bottom>0});await Promise.race([Promise.all(imgs.map(i=>i.decode().catch(()=>{}))),new Promise(r=>setTimeout(r,1500))]);}')
                page.screenshot(path=str(out/f'{path.stem}-{"before" if before else "after"}-{width}.png'))
            results.append(data)
            (out/('before.json' if before else 'quick.json' if quick else 'hub-final.json' if hub else 'cards-final.json' if recheck else 'results.json')).write_text(json.dumps(results,indent=2))
    page.close();context.close();browser.close()
server.shutdown()
