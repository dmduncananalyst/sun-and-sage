from pathlib import Path
import json,re,html,hashlib
from urllib.parse import unquote,urlsplit
from playwright.sync_api import sync_playwright
from multilingual.site import CONFIG,document_spans,strip_integration,key

root=Path(__file__).resolve().parent;out=root/'october21-review'
records=json.loads((out/'articles.json').read_text(encoding='utf-8'))
cache=json.loads((root/'multilingual/translations.json').read_text(encoding='utf-8'))
results=[];errors=[];paid=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
 for width in (390,1440):
  for lang in CONFIG['languages']:
   context=browser.new_context(viewport={'width':width,'height':1000})
   def route(r):
    if 'translation.googleapis.com' in r.request.url:paid.append(r.request.url)
    r.continue_() if r.request.url.startswith('file:') else r.abort()
   context.route('**/*',route);page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
   prefix='' if lang=='en' else lang+'/'
   for record in records:
    source=(root/prefix/record['file']).read_text(encoding='utf-8')
    english=(root/record['file']).read_text(encoding='utf-8')
    if lang!='en':
     for a,b,text,attribute in document_spans(strip_integration(english)):
      assert html.escape(cache[key(text,lang)],quote=attribute) in source,(lang,record['file'],text)
    assert source.count('hreflang=')==11
    page.goto((root/prefix/record['file']).as_uri(),wait_until='load')
    expected_title=record['title'] if lang=='en' else cache[key(record['title'],lang)]
    assert page.locator('h1').count()==1 and page.locator('h1').inner_text()==expected_title
    assert page.locator('main article > section:not(#references)').count()==7
    assert page.locator('#references a').count()==4
    assert page.locator('html').get_attribute('lang')==lang
    assert page.locator('html').get_attribute('dir')==('rtl' if lang in CONFIG['rtl'] else 'ltr')
    assert page.locator('#dd-language option').count()==10
    assert page.locator('#dd-language').input_value()==lang
    assert page.locator('link[rel=canonical]').get_attribute('href')==CONFIG['origin']+'/'+prefix+record['file']
    schema=json.loads(page.locator('script[type="application/ld+json"]').inner_text())
    assert schema['inLanguage']==lang and schema['headline']==expected_title
    assert schema['datePublished']=='2026-10-21'
    image=page.locator('main figure img');image.evaluate('(i)=>i.decode()')
    assert image.evaluate('(i)=>getComputedStyle(i).objectFit')=='contain'
    assert image.get_attribute('src')=='assets/blogs/'+record['photo']
    assert hashlib.sha256((root/'assets/blogs'/record['photo']).read_bytes()).hexdigest()==record['photo_sha256']
    assert page.locator('main').evaluate('(e)=>e.scrollWidth<=e.clientWidth+1')
    assert CONFIG['origin']+'/'+prefix+record['file'] in (root/f'sitemap-{lang}.xml').read_text(encoding='utf-8')
    for href in page.locator('main a').evaluate_all('(aa)=>aa.map(a=>a.getAttribute("href"))'):
     if not href.startswith(('http','#','mailto:','tel:')):assert (root/unquote(urlsplit(href).path)).exists(),href
    page.screenshot(path=str(out/f'{lang}-{record["slug"]}-{width}.png'))
    results.append({'language':lang,'width':width,'article':record['file'],'complete_saved_translation':True,'photo':True,'seo':True})
   for record in records:
    page.goto((root/prefix/'blog.html').as_uri(),wait_until='load')
    card=page.locator(f'[data-october21="{record["slug"]}"]');assert card.count()==1
    assert card.locator('.loanLearn a').get_attribute('href')==prefix+record['file']
    photo=card.locator('img');photo.scroll_into_view_if_needed();photo.evaluate('(i)=>i.decode()')
    assert photo.evaluate('(i)=>getComputedStyle(i).objectFit')=='cover'
    card.locator('.loanLearn a').click();assert page.locator('h1').inner_text()==(record['title'] if lang=='en' else cache[key(record['title'],lang)])
   if lang!='en':
    page.locator('#dd-language').click();page.locator('#dd-language-menu [data-language="en"]').click()
    page.wait_for_url((root/records[-1]['file']).as_uri())
    assert page.locator('h1').inner_text()==records[-1]['title']
   context.close();print('Passed:',width,lang,flush=True)
 browser.close()
assert not paid and not errors,(paid,errors)
(out/'translation-results.json').write_text(json.dumps({'cases':results,'javascript_errors':errors,'paid_browser_requests':paid,'local_only':True},indent=2),encoding='utf-8')
print('Passed 60 article browser cases, all translated cards and English switching; zero paid browser requests or JavaScript errors.')
