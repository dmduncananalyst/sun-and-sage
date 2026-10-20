"""Local-only Chrome review. External requests are blocked; no forms are submitted."""
from functools import partial
import argparse
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
import json
from pathlib import Path
import threading
from urllib.parse import urlsplit
from .site import ROOT,CONFIG,local_url

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--source',action='store_true');parser.add_argument('--english-only',action='store_true');args=parser.parse_args()
    from playwright.sync_api import sync_playwright
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT if args.source else ROOT/'dist')))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    origin=f'http://127.0.0.1:{server.server_port}'
    results=[];paid_attempts=[];errors=[]
    review=ROOT/'.translation-state'/('source-browser-review' if args.source else 'browser-review');review.mkdir(exist_ok=True,parents=True)
    try:
        with sync_playwright() as driver:
            browser=driver.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
            for width in [1440,390]:
                for lang in (['en'] if args.english_only else CONFIG['languages']):
                    context=browser.new_context(viewport={'width':width,'height':960},reduced_motion='reduce')
                    def route(request):
                        url=request.request.url
                        if 'googleapis.com' in url and any(part in url for part in ['translate','speech']):paid_attempts.append(url)
                        if urlsplit(url).hostname in {'127.0.0.1','localhost'}:request.continue_()
                        else:request.abort()
                    context.route('**/*',route)
                    page=context.new_page()
                    page.on('pageerror',lambda error:errors.append(str(error)))
                    for path in ['index.html','blog.html','contact.html','blog-401k-matters.html']:
                        response=page.goto(origin+local_url(path,lang),wait_until='domcontentloaded',timeout=60000)
                        page.wait_for_timeout(500)
                        actual=page.evaluate('''() => ({language:document.documentElement.lang,direction:document.documentElement.dir,canonical:document.querySelector('link[rel="canonical"]')?.href,alternates:document.querySelectorAll('link[hreflang]').length,options:document.querySelector('#dd-language')?.options.length,overflow:document.documentElement.scrollWidth>innerWidth+2,title:document.title,mainText:document.querySelector('main')?.innerText.slice(0,200)})''')
                        checks={'status':response.status==200,'language':actual['language']==lang,'direction':actual['direction']==('rtl' if lang in CONFIG['rtl'] else 'ltr'),'canonical':actual['canonical']==CONFIG['origin']+local_url(path,lang),'hreflang':actual['alternates']==11,'selector':actual['options']==10,'no_horizontal_overflow':not actual['overflow'],'header_styles_loaded':page.locator('header').first.evaluate('(h)=>h.getBoundingClientRect().height<300')}
                        if path=='contact.html' and lang!='en':
                            validation=page.evaluate('''() => {const field=document.querySelector('input[required]');if(!field)return true;field.value='';field.checkValidity();return field.validationMessage===window.dommydomTranslateSaved('Please fill out this field.')}''')
                            checks['translated_validation']=validation
                        if width==390 and path=='index.html':
                            toggle=page.locator('.dd-menu-toggle')
                            toggle.click();checks['mobile_menu_opens']=toggle.get_attribute('aria-expanded')=='true'
                            toggle.click();checks['mobile_menu_closes']=toggle.get_attribute('aria-expanded')=='false'
                        results.append({'width':width,'language':lang,'page':path,'checks':checks,'title':actual['title']})
                        if path=='index.html' and lang in {'en','es','fa','ar','zh-CN'}:page.screenshot(path=str(review/f'{lang}-{width}.png'),full_page=False)
                    # Switch from the current blog article to English; explicit selector choice must win.
                    page.select_option('#dd-language','en')
                    page.wait_for_url(origin+'/blog-401k-matters.html',timeout=15000)
                    context.close()
                    print(f'Browser review: {lang} at {width}px complete',flush=True)
            browser.close()
    finally:server.shutdown();server.server_close()
    report={'local_only':True,'actual_source_website':args.source,'pages_checked':len(results),'checks':results,'paid_api_attempts':paid_attempts,'javascript_errors':sorted(set(errors)),'screenshots_directory':str(review.relative_to(ROOT))}
    report_path=ROOT/'multilingual'/('source-browser-review.json' if args.source else 'browser-review.json')
    if args.english_only:
        report_path=report_path.with_name(report_path.stem+'-english-recheck.json')
    report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    failures=[r for r in results if not all(r['checks'].values())]
    print(json.dumps({'pages_checked':len(results),'failed_pages':len(failures),'paid_api_attempts':len(paid_attempts),'javascript_errors':len(set(errors))},indent=2))
    if failures or paid_attempts:raise RuntimeError('Browser review found issues; see browser-review.json')

if __name__=='__main__':main()
