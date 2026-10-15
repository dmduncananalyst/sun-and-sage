# Browser transport-contract tests only: the echo response below is NOT translation.
exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 ctx=b.new_context(viewport={'width':834,'height':1194},has_touch=True);sent=[]
 ctx.route('https://**/*',lambda r:r.abort())
 ctx.route('**/assets/translation-config.json',lambda r:r.fulfill(json={'endpoint':f'http://127.0.0.1:{s.server_port}/translate-contract-only'}))
 def echo(route):
  data=route.request.post_data_json;sent.extend(data['texts']);route.fulfill(json={'translations':data['texts']})
 ctx.route('**/translate-contract-only',echo);pg=ctx.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/considerations.html',wait_until='domcontentloaded');pg.wait_for_timeout(200)
 pg.evaluate('let i=document.createElement("input");i.id="privacy-contract";i.value="PRIVATE-VISITOR-123";document.querySelector("main").append(i)')
 original=pg.locator('main').inner_text();pg.locator('.dd-language-trigger').tap();pg.locator('.dd-language-options button[lang="fa"]').click();pg.wait_for_function('document.documentElement.lang==="fa"');assert pg.locator('main').get_attribute('dir')=='rtl';assert not any('PRIVATE-VISITOR' in t for t in sent);assert pg.locator('#privacy-contract').input_value()=='PRIVATE-VISITOR-123'
 pg.goto(f'http://127.0.0.1:{s.server_port}/buyer-consultation.html',wait_until='domcontentloaded');pg.wait_for_function('document.documentElement.lang==="fa"');assert pg.locator('main').get_attribute('dir')=='rtl';pg.locator('.dd-language-trigger').tap();pg.locator('.dd-language-options button[lang="en"]').click();pg.wait_for_function('document.documentElement.lang==="en"');assert pg.locator('main').get_attribute('dir') is None;assert pg.locator('.dd-translation-credit').is_hidden()
 pg.locator('.dd-language-trigger').focus();pg.keyboard.press('ArrowDown');assert pg.locator('.dd-language-panel').is_visible();pg.keyboard.press('Escape');assert not pg.locator('.dd-language-panel').is_visible();ctx.close()
 ctx=b.new_context(viewport={'width':390,'height':844},locale='es-ES');ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/about.html',wait_until='domcontentloaded');pg.wait_for_timeout(150);assert pg.locator('.dd-translation-notice').get_attribute('lang')=='es';assert pg.evaluate('document.documentElement.lang')=='en';pg.locator('.dd-translation-notice button').last.click();pg.reload(wait_until='domcontentloaded');assert pg.locator('.dd-translation-notice').count()==0;ctx.close();b.close()
s.shutdown();print('Transport-contract checks passed: same-page state, persisted language across consultation link, RTL restoration, input exclusion, Escape and native invitation dismissal. Echo transport is NOT Google translation.')
