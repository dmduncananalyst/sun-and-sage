"""Property-search and HubSpot payload checks; intercept every submission locally."""
import json,threading
from functools import partial
from http.server import ThreadingHTTPServer
from .audit_review import QuietHandler
from .site import ROOT,pages

def main():
    from playwright.sync_api import sync_playwright
    paths=[p for p in pages() if 'data-sun-conversation-form' in (ROOT/p).read_text(encoding='utf-8')]
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
    results=[];payloads=[]
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
            context=browser.new_context()
            def route(r):
                if 'hsforms.com/submissions/' in r.request.url:
                    payloads.append({'url':r.request.url,'payload':r.request.post_data_json});r.fulfill(status=200,content_type='application/json',body='{}')
                elif r.request.url.startswith(origin):r.continue_()
                else:r.abort()
            context.route('**/*',route);page=context.new_page();page.on('pageerror',lambda e:print('Browser error:',e,flush=True))
            for path in paths:
                page.goto(origin+'/'+path,wait_until='domcontentloaded')
                form=page.locator('[data-sun-conversation-form]').first
                city=form.locator('[name="city"]');city.select_option('')
                form.evaluate('(f)=>f.requestSubmit()')
                assert page.locator('#sun-conversation[open]').count()==0,path
                options=city.locator('option').evaluate_all('(o)=>o.filter(x=>x.value).map(x=>x.value)');city.select_option(options[0])
                form.locator('[name="minPrice"]').fill('900000');form.locator('[name="maxPrice"]').fill('500000')
                form.evaluate('(f)=>f.requestSubmit()');assert form.locator('[name="maxPrice"]').evaluate('(f)=>f.validity.customError'),(path,form.evaluate('(f)=>[...f.elements].map(e=>({name:e.name,value:e.value,valid:e.checkValidity(),message:e.validationMessage}))'))
                form.locator('[name="maxPrice"]').fill('1500000');form.evaluate('(f)=>f.requestSubmit()')
                assert page.locator('#sun-conversation[open]').count()==1,path
                if path in ['index.html','buy-sylmar.html']:
                    for _ in range(15):
                        choice=page.locator('.sunConversation__choice')
                        if choice.count():choice.first.click();continue
                        if page.locator('.sunConversation__contact').count():break
                        fields=page.locator('.sunConversation__stage input:visible,.sunConversation__stage textarea:visible')
                        if fields.count():
                            for field in fields.all():field.fill('Local audit test')
                            page.locator('.sunConversation__stage button[type="submit"]').click();continue
                        break
                    form2=page.locator('#sun-conversation form').last
                    for field in form2.locator('input,textarea').all():
                        if not field.is_visible():continue
                        kind=field.get_attribute('type');name=field.get_attribute('name')
                        value='dommydom-local-review@example.invalid' if kind=='email' else '8185550100' if kind=='tel' else 'Local audit test'
                        if kind not in ['checkbox','radio','hidden']:field.fill(value)
                    form2.evaluate('(f)=>f.requestSubmit()');page.wait_for_timeout(100)
                    assert payloads and '900000' in json.dumps(payloads[-1]),path
                results.append({'page':path,'blank_city_rejected':True,'reversed_prices_rejected':True,'corrected_range_accepted':True,'conversation_opened':True})
            browser.close()
    finally:server.shutdown()
    report={'local_only':True,'search_forms_checked':len(results),'results':results,'intercepted_hubspot_payloads':payloads,'external_submissions_sent':0,'live_crm_receipt_verified':False,'crm_blocker':'No authenticated HubSpot account connection is available to inspect received submissions.'}
    (ROOT/'multilingual/form-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'forms_checked':len(results),'payloads_verified':len(payloads),'external_submissions_sent':0},indent=2))

if __name__=='__main__':main()
