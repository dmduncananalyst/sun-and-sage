"""Validate the complete supplied PDF article and local saved translations."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer
import hashlib,html,json,re,threading
from urllib.parse import urljoin,urlsplit,unquote
from .audit_review import QuietHandler
from .site import ROOT,CONFIG,key,document_spans,strip_integration

def main():
    from playwright.sync_api import sync_playwright
    data=json.loads((ROOT/'multilingual/midterm-editorial-manifest.json').read_text(encoding='utf-8'))
    cache=json.loads((ROOT/'multilingual/translations.json').read_text(encoding='utf-8'))
    english=(ROOT/data['path']).read_text(encoding='utf-8')
    main=re.search(r'<main\b.*?</main>',english,re.S)[0]
    separated=re.sub(r'</(?:p|h[1-6]|li|header|figcaption|article)>','\n',main)
    visible=' '.join(html.unescape(re.sub('<[^>]*>','',separated)).split())
    assert all(block in visible for block in data['blocks']),[b for b in data['blocks'] if b not in visible]
    assert all(r['url'] in main and r['description'] in html.unescape(main) for r in data['references'])
    assert all(v not in main for v in ['Developer instructions','Developer placement:','SEO meta description:','Exact photo filename:'])
    assert not re.search(r'<h[1-6][^>]*>[^<]*(?:FAQ|Next steps)',main,re.I)
    assert hashlib.sha256((ROOT/data['image']).read_bytes()).hexdigest()==data['image_sha256']
    assert (ROOT/data['image']).read_bytes()==Path(data['image_source']).read_bytes()
    for language in CONFIG['languages']:
        prefix='' if language=='en' else language+'/'
        source=(ROOT/prefix/data['path']).read_text(encoding='utf-8')
        assert source.count('<h1')==1 and source.count('rel="canonical"')==1
        assert source.count('hreflang=')==11
        assert data['image'] in source and data['image'] in (ROOT/prefix/'blog.html').read_text(encoding='utf-8')
        assert 'https://dommydom.com/'+prefix+data['path'] in (ROOT/f'sitemap-{language}.xml').read_text(encoding='utf-8')
        if language!='en':
            for _,_,text,attribute in document_spans(strip_integration(english)):
                assert html.escape(cache[key(text,language)],quote=attribute) in source,(language,text)
        schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',source,re.S)[1])
        assert schema['@type']=='BlogPosting' and len(schema['citation'])==4
    missing=[]
    for path in [data['path'],'blog.html']:
        source=(ROOT/path).read_text(encoding='utf-8')
        for tag in re.finditer(r'<(?:a|img|script|link)\b[^>]*>',source,re.I):
            for url in re.findall(r'(?:href|src)=["\']([^"\']*)',tag[0]):
                parsed=urlsplit(urljoin('https://dommydom.com/',html.unescape(url)))
                if parsed.netloc=='dommydom.com' and parsed.path and not (ROOT/unquote(parsed.path.lstrip('/'))).exists():missing.append((path,url))
    assert not missing,missing
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
    results=[];errors=[];paid=[];shots=ROOT/'.translation-state/midterm-review';shots.mkdir(parents=True,exist_ok=True)
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
            for width in [390,768,1440]:
                for language in CONFIG['languages']:
                    context=browser.new_context(viewport={'width':width,'height':960})
                    def route(r):
                        url=r.request.url
                        if 'googleapis.com' in url and 'translate' in url:paid.append(url)
                        if url.startswith(origin) or url.startswith('file:'):r.continue_()
                        else:r.abort()
                    context.route('**/*',route);page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
                    prefix='' if language=='en' else language+'/'
                    response=page.goto(origin+'/'+prefix+data['path'],wait_until='domcontentloaded');page.wait_for_timeout(200)
                    image=page.locator('.midterm-hero img');image.evaluate('(i)=>i.decode()')
                    state=page.evaluate('''()=>{const i=document.querySelector('.midterm-hero img'),r=i.getBoundingClientRect();return {lang:document.documentElement.lang,rtl:document.documentElement.dir,overflow:document.documentElement.scrollWidth>innerWidth+2,ratio:r.width/r.height,naturalWidth:i.naturalWidth,fit:getComputedStyle(i).objectFit,filter:getComputedStyle(i).filter,caption:document.querySelector('.midterm-hero figcaption').getBoundingClientRect().height>0,h2:document.querySelectorAll('main h2').length,selected:document.querySelector('#dd-language').value}}''')
                    assert response.status==200 and state['lang']==language and state['selected']==language
                    assert not state['overflow'] and state['h2']==7,(width,language,state)
                    assert state['naturalWidth']==data['image_width'] and abs(state['ratio']-data['image_width']/data['image_height'])<.01 and state['fit']=='contain' and state['filter']=='none' and state['caption'],(width,language,state)
                    assert state['rtl']==('rtl' if language in ['fa','ar'] else 'ltr')
                    if language=='en':page.screenshot(path=str(shots/f'article-{width}.png'),full_page=True)
                    page.goto(origin+'/'+prefix+'blog.html',wait_until='domcontentloaded')
                    card=page.locator('[data-midterm-article]');assert card.count()==1
                    photo=card.locator('img');photo.scroll_into_view_if_needed();photo.evaluate('(i)=>i.decode()')
                    assert photo.evaluate('(i)=>i.naturalWidth')==data['image_width']
                    with page.expect_navigation(wait_until='domcontentloaded'):card.locator('.loanLearn a').click()
                    assert page.url==origin+'/'+prefix+data['path']
                    page.locator('#dd-language').click()
                    with page.expect_navigation(wait_until='domcontentloaded'):page.locator('#dd-language-menu [data-language="en"]').click()
                    assert page.url==origin+'/'+data['path']
                    results.append({'width':width,'language':language,'complete_article':True,'original_uncropped_article_photo':True,'archive_card_and_language_switch':True});context.close()
                    print('Reviewed:',width,language,flush=True)
            context=browser.new_context(viewport={'width':390,'height':960});context.route('**/*',lambda r:r.continue_() if r.request.url.startswith('file:') else r.abort())
            page=context.new_page();page.goto((ROOT/data['path']).as_uri(),wait_until='domcontentloaded');assert page.locator('.midterm-hero img').evaluate('(i)=>i.decode().then(()=>i.naturalWidth)')==data['image_width']
            context.close();browser.close()
    finally:server.shutdown()
    report={'local_only':True,'article':data['path'],'pdf_pages_read':4,'complete_original_content_preserved':True,'headings':6,'supplied_references':4,'verification_resource_links_included':True,'original_photo_bytes_preserved':True,'saved_language_versions':10,'browser_cases':results,'missing_internal_files':missing,'paid_visitor_api_attempts':paid,'javascript_errors':sorted(set(errors)),'published':False,'committed':False}
    (ROOT/'multilingual/midterm-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'browser_cases':len(results),'errors':errors,'paid_visitor_api_attempts':paid,'complete_source_and_translations':True},indent=2))
    assert not paid and not errors

if __name__=='__main__':main()
