from pathlib import Path
import json,re,html,xml.etree.ElementTree as ET
from urllib.parse import unquote,urlsplit
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parent;out=root/'october21-review'
records=json.loads((out/'articles.json').read_text())
results=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
    for width in (390,768,1440):
        context=browser.new_context(viewport={'width':width,'height':1000})
        context.route('**/*',lambda route:route.continue_() if route.request.url.startswith('file:') else route.abort())
        page=context.new_page()
        for r in records:
            page.goto((root/r['file']).as_uri(),wait_until='load')
            assert page.locator('h1').count()==1
            assert page.locator('h1').inner_text()==r['title']
            sections=page.locator('main article > section:not(#references)')
            assert sections.count()==7
            for i,(heading,text) in enumerate(r['sections']):
                assert sections.nth(i).locator('p').inner_text()==text
                if heading:assert sections.nth(i).locator('h2').inner_text()==heading
            assert page.title()==r['title']
            assert page.locator('meta[name=description]').get_attribute('content')==r['description']
            assert page.locator('link[rel=canonical]').get_attribute('href')=='https://dommydom.com/'+r['file']
            schema=json.loads(page.locator('script[type="application/ld+json"]').inner_text())
            assert schema['datePublished']=='2026-10-21'
            assert page.locator('#references a').count()==4
            assert page.locator('main').evaluate('(e)=>e.scrollWidth<=e.clientWidth+1')
            for href in page.locator('main a').evaluate_all('(aa)=>aa.map(a=>a.getAttribute("href"))'):
                if not href.startswith(('http','#','tel:','mailto:')):assert (root/unquote(urlsplit(href).path)).exists(),href
            photos=page.locator('main figure img')
            assert photos.count()==1
            photos.evaluate('(i)=>i.decode()')
            assert photos.get_attribute('src')=='assets/blogs/'+r['photo']
            assert photos.get_attribute('alt')==r['photo_alt']
            assert photos.evaluate('(i)=>i.complete && i.naturalWidth>0')
            assert photos.evaluate('(i)=>getComputedStyle(i).objectFit')=='contain'
            assert photos.evaluate('(i)=>Math.abs(i.clientWidth/i.clientHeight-i.naturalWidth/i.naturalHeight)<0.02')
            assert schema['image']['url']==page.locator('meta[property="og:image"]').get_attribute('content')
            assert schema['image']['width']==r['photo_width']
            page.screenshot(path=str(out/f'{r["slug"]}-top-{width}.png'))
            page.screenshot(path=str(out/f'{r["slug"]}-{width}.png'),full_page=True)
            results.append({'page':r['file'],'width':width,'content_exact':True,'metadata':True,'local_links':True,'photo':photos.count()>0})
        page.goto((root/'blog.html').as_uri(),wait_until='load')
        for r in records:
            card=page.locator(f'[data-october21="{r["slug"]}"]')
            assert card.count()==1
            assert card.locator('h2').inner_text()==r['title']
            link=card.locator('.loanLearn a');assert link.get_attribute('href')==r['file']
            assert card.locator('img').count()==1
            card.locator('img').scroll_into_view_if_needed()
            card.locator('img').evaluate('(i)=>i.decode()')
            assert card.locator('img').evaluate('(i)=>i.complete && i.naturalWidth>0')
            assert card.locator('img').get_attribute('src')=='assets/blogs/'+r['photo']
            assert card.locator('img').evaluate('(i)=>getComputedStyle(i).objectFit')=='cover',card.locator('img').evaluate('(i)=>i.outerHTML')
            assert card.locator('img').evaluate('(i)=>Math.abs(i.getBoundingClientRect().height-i.parentElement.clientHeight)<2 && Math.abs(i.getBoundingClientRect().width-i.parentElement.clientWidth)<2')
            card.screenshot(path=str(out/f'{r["slug"]}-card-{width}.png'))
            link.click();assert page.locator('h1').inner_text()==r['title']
            page.goto((root/'blog.html').as_uri(),wait_until='load')
        page.screenshot(path=str(out/f'archive-{width}.png'))
        context.close()
    browser.close()
tree=ET.parse(root/'sitemap-en.xml');ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls=[n.text for n in tree.findall('.//s:loc',ns)]
for r in records:assert urls.count('https://dommydom.com/'+r['file'])==1
(out/'local-results.json').write_text(json.dumps(results,indent=2))
print('Passed: exact article text, headings, metadata, structured data, source counts, internal links, archive navigation and sitemap; 390, 768, 1440 pixels.')
