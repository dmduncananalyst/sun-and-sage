"""Exercise the audit's nineteen formerly broken URLs in a real browser."""
import json,threading
from http.server import ThreadingHTTPServer
from functools import partial
from .audit_review import QuietHandler
from .site import ROOT

SLUGS='401k-matters california-condo-crisis-sb326-2026 california-proposition-19-homeowners chatsworth-home-prices-2026 dia-de-los-muertos-san-fernando-valley-2026 fall-farmers-markets-san-fernando-valley-2026 film-crew-rental having-children-in-your-40s how-to-stage-a-living-room is-it-time-for-divorce lake-balboa-park-japanese-garden-fall-guide living-in-chatsworth los-angeles-short-term-rental-rules-2026 northridge-housing-market-2026 porter-ranch-housing-market thoughtful-home-staging-presentation two-one-rate-buydown what-its-like-to-live-in-granada-hills why-budgeting-matters'.split()

def main():
    from playwright.sync_api import sync_playwright
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';results=[]
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
            context=browser.new_context();context.route('**/*',lambda r:r.continue_() if r.request.url.startswith(origin) or r.request.url.startswith('file:') else r.abort());page=context.new_page()
            for protocol in ['http','file']:
                for slug in SLUGS:
                    start=(ROOT/'blog'/f'{slug}.html').as_uri() if protocol=='file' else origin+'/blog/'+slug+'.html'
                    expected=(ROOT/f'blog-{slug}.html').as_uri() if protocol=='file' else origin+'/blog-'+slug+'.html'
                    page.goto(start+'?audit=local#main',wait_until='domcontentloaded');page.wait_for_url(expected+'?audit=local#main')
                    assert page.locator('h1').count()==1,(protocol,slug)
                    results.append({'protocol':protocol,'slug':slug,'local_redirect_and_query_fragment_preserved':True})
            browser.close()
    finally:server.shutdown()
    (ROOT/'multilingual/redirect-review.json').write_text(json.dumps({'local_only':True,'browser_routes_checked':len(results),'results':results},indent=2)+'\n',encoding='utf-8');print('Passed:',len(results),'legacy blog redirect browser checks')

if __name__=='__main__':main()
