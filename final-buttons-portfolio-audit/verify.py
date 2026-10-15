exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'final-buttons-portfolio-audit'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h in [(390,844),(768,1024),(1440,1000)]:
  ctx=b.new_context(viewport={'width':w,'height':h});ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page()
  for name in ['contact.html','interior-design.html','sell-free-home-valuation.html','buyer-consultation.html','seller-consultation.html']:
   pg.goto(f'http://127.0.0.1:{s.server_port}/{name}',wait_until='domcontentloaded');pg.wait_for_timeout(150);pg.evaluate('document.documentElement.style.scrollBehavior="auto"');assert not pg.evaluate('document.documentElement.scrollWidth>innerWidth')
   if name=='contact.html':
    assert not pg.locator('#sun-conversation').is_visible();assert pg.locator('.v7-service-guide a').get_attribute('href')=='questions.html';pg.locator('.dd-contact-action').screenshot(path=str(out/f'{w}-contact-button.png'));pg.locator('.dd-contact-action>a').click();assert pg.locator('#sun-conversation').is_visible();pg.screenshot(path=str(out/f'{w}-chat-open.png'));pg.keyboard.press('Escape');assert not pg.locator('#sun-conversation').is_visible()
   elif name=='interior-design.html':
    el=pg.locator('.dd-design-portfolio');el.scroll_into_view_if_needed();pg.wait_for_timeout(800);rects=el.locator('figure').evaluate_all('es=>es.map(e=>({w:e.getBoundingClientRect().width,h:e.getBoundingClientRect().height}))');assert max(r['w'] for r in rects)-min(r['w'] for r in rects)<1;assert max(r['h'] for r in rects)-min(r['h'] for r in rects)<1;el.screenshot(path=str(out/f'{w}-portfolio.png'));assert pg.locator('.ss43-primary-action').text_content()=='Design with Dominique'
   elif name=='sell-free-home-valuation.html':assert pg.locator('.dd-evaluation-action>a').text_content()=='Schedule Evaluation';pg.locator('.dd-evaluation-action').screenshot(path=str(out/f'{w}-evaluation.png'))
   else:assert pg.locator('.ss24-consultation-caption>a').text_content()=='Schedule Consultation'
  ctx.close()
 b.close()
s.shutdown();print('Passed desktop, iPad and phone: equal image dimensions, correct labels, closed Contact chat, click to open and Escape to close.')
