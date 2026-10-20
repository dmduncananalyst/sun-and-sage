"""Review the real checkout, including Explorer file URLs; never send form data."""
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import html,json,re,threading,zipfile,hashlib
from urllib.parse import urljoin,urlsplit,unquote
from .site import ROOT,CONFIG,pages

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass

def main():
    from playwright.sync_api import sync_playwright
    manifest=json.loads((ROOT/'multilingual/october-editorial-manifest.json').read_text(encoding='utf-8'))
    listing=pages();results=[];errors=[];paid=[];missing=[]
    for path in listing:
        source=(ROOT/path).read_text(encoding='utf-8')
        base=re.search(r'<base\b[^>]*href=["\']([^"\']*)',source,re.I)
        origin=urljoin('https://dommydom.com/'+path,base[1]) if base else 'https://dommydom.com/'+path
        for match in re.finditer(r'<(?:a|img|script|link|source)\b[^>]*',source,re.I):
            for attr,value in re.findall(r'\b(href|src)=["\']([^"\']*)',match[0],re.I):
                target=urlsplit(urljoin(origin,html.unescape(value)))
                if target.netloc!='dommydom.com' or not target.path or value.startswith('#'):continue
                local=ROOT/unquote(target.path.lstrip('/'))
                if not local.exists():missing.append({'page':path,'url':value})
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    origin=f'http://127.0.0.1:{server.server_port}'
    shots=ROOT/'.translation-state/october-review';shots.mkdir(parents=True,exist_ok=True)
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
            for protocol in ['file','http']:
                for language in CONFIG['languages']:
                    context=browser.new_context(viewport={'width':1440,'height':960})
                    def route(r):
                        url=r.request.url
                        if 'googleapis.com' in url and any(x in url for x in ['translate','speech']):paid.append(url)
                        if url.startswith('file:') or urlsplit(url).hostname=='127.0.0.1':r.continue_()
                        else:r.abort()
                    context.route('**/*',route);page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
                    address=(ROOT/'index.html').as_uri() if protocol=='file' else origin+'/index.html'
                    page.goto(address,wait_until='domcontentloaded')
                    with page.expect_navigation(wait_until='domcontentloaded'):page.select_option('#dd-language',language)
                    page.wait_for_function('(lang)=>document.documentElement.lang===lang',arg=language)
                    state=page.evaluate('''()=>({language:document.documentElement.lang,order:!!document.querySelector('.dd-search + .dd-language-selector'),globe:!!document.querySelector('.dd-language-selector svg'),label:document.querySelector('.dd-language-selector').innerText,loaded:typeof window.dommydomTranslateSaved==='function'&&document.querySelector('header').getBoundingClientRect().height<300,text:document.querySelector('main').innerText.slice(0,150)})''')
                    results.append({'protocol':protocol,'language':language,'checks':{'language':state['language']==language,'beside_search':state['order'],'globe':state['globe'],'runtime_loaded':state['loaded'],'no_visible_language_label':'Language' not in state['label']},'main_text':state['text']})
                    context.close()
            for width in [320,390,768,1024,1440]:
                context=browser.new_context(viewport={'width':width,'height':960})
                context.route('**/*',lambda r:r.continue_() if urlsplit(r.request.url).hostname=='127.0.0.1' else r.abort())
                page=context.new_page()
                for path in ['index.html','blog.html']+[a['path'] for a in manifest['articles']]:
                    page.goto(origin+'/'+path,wait_until='domcontentloaded');page.wait_for_timeout(150)
                    for image in page.locator('.loanHubItem>.ss18-card-photo img,.dommydom-new-blog .ss4711-photo img').all():
                        image.scroll_into_view_if_needed();image.evaluate('(i)=>i.decode()')
                    page.evaluate('scrollTo(0,0)')
                    state=page.evaluate('''()=>({overflow:document.documentElement.scrollWidth>innerWidth+2,select:document.querySelector('#dd-language').getBoundingClientRect().toJSON(),images:[...document.querySelectorAll('.dommydom-new-blog .ss4711-photo img,[data-editorial-batch] img')].map(i=>({loaded:i.complete&&i.naturalWidth===1800,fit:getComputedStyle(i).objectFit,expected:i.closest('[data-editorial-batch]')?'cover':'contain',filter:getComputedStyle(i).filter}))})''')
                    fits=page.locator('.loanHubItem:not([data-editorial-batch])>.ss18-card-photo img,.blogCard figure img,.blog-card figure img').evaluate_all('(images)=>images.map(i=>getComputedStyle(i).objectFit)')
                    results.append({'width':width,'page':path,'checks':{'no_overflow':not state['overflow'],'selector_visible':state['select']['x']>=0 and state['select']['right']<=width,'quality_photos_and_requested_card_fill':all(i['loaded'] and i['fit']==i['expected'] and i['filter']=='none' for i in state['images']),'existing_card_photos_uncropped':all(f=='contain' for f in fits)},'image_states':state['images']})
                    if path in ['index.html','blog.html',manifest['articles'][0]['path']]:page.screenshot(path=str(shots/f'{width}-{path}.png'),full_page=True)
                context.close()
            browser.close()
    finally:server.shutdown()
    with zipfile.ZipFile('C:/Users/Owner/Downloads/dommydom_six_blog_photos.zip') as archive:
        hashes={a['image']:hashlib.sha256((ROOT/a['image']).read_bytes()).hexdigest()==hashlib.sha256(archive.read(next(n for n in archive.namelist() if n.endswith('/'+a['image'].split('/')[-1]) or n==a['image'].split('/')[-1]))).hexdigest() for a in manifest['articles']}
    report={'local_only':True,'checks':results,'missing_internal_files':missing,'original_photo_bytes_preserved':hashes,'paid_api_attempts':paid,'javascript_errors':sorted(set(errors))}
    (ROOT/'multilingual/october-audit-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    failures=[r for r in results if not all(r['checks'].values())]
    print(json.dumps({'cases':len(results),'failures':failures,'missing_internal_files':missing,'photo_hashes_match':all(hashes.values()),'paid_api_attempts':paid,'javascript_errors':sorted(set(errors))},ensure_ascii=False,indent=2))
    if failures or missing or paid or not all(hashes.values()):raise RuntimeError('Audit review requires corrections')

if __name__=='__main__':main()
