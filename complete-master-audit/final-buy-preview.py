exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'complete-master-audit';results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in [390,744,768,820,834,1024,1440]:
  pg=b.new_page(viewport={'width':w,'height':1000 if w>=600 else 844});pg.route('https://**/*',lambda r:r.abort());pg.goto(f'http://127.0.0.1:{s.server_port}/buy-a-home.html',wait_until='domcontentloaded');pg.wait_for_timeout(150);pg.evaluate('document.documentElement.style.scrollBehavior="auto"');assert not pg.evaluate('document.documentElement.scrollWidth>innerWidth');pg.screenshot(path=str(out/f'buy-{w}.png'),full_page=True)
  if w in [390,768,1024,1440]:
   for selector,section in [('.dd-buy-overview','top'),('.dd-buy-statistics','middle'),('.dd-buy-reach','maps'),('.ss49-button-row','bottom')]:
    pg.locator(selector).evaluate('e=>e.scrollIntoView({block:"start",behavior:"instant"})');pg.wait_for_timeout(70);pg.screenshot(path=str(out/f'buy-{section}-{w}.png'))
   for selector,section in [('.dd-buy-wheel','wheel'),('.dd-buy-statistics','charts'),('.dd-buy-reach','reach')]:
    pg.locator(selector).screenshot(path=str(out/f'buy-detail-{section}-{w}.png'))
  results.append({'width':w,'overflow':False,'benefitsColumns':pg.locator('.dd-buy-benefits').evaluate('e=>getComputedStyle(e).gridTemplateColumns')});pg.close()
 b.close()
s.shutdown();(out/'final-buy-refinement-results.json').write_text(json.dumps(results,indent=2));print('Final Buy views recaptured with settled section positions and tablet benefit rows.')
