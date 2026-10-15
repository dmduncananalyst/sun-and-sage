exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'contact-final-audit'
import re
before=(out/'before-contact.html').read_text(encoding='utf-8');after=Path('contact.html').read_text(encoding='utf-8');old=re.search(r'<main\b[^>]*>([\s\S]*?)</main>',before)[1];assert after.count(old)==1
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h in [(390,844),(768,1024),(1024,768),(1440,1000)]:
  ctx=b.new_context(viewport={'width':w,'height':h},has_touch=w<1200);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/contact.html',wait_until='domcontentloaded');pg.wait_for_timeout(250);pg.evaluate('document.documentElement.style.scrollBehavior="auto"');cards=pg.locator('.dd-contact-cards');assert cards.locator('.consideration-card').count()==3
  assert cards.locator('img').evaluate_all('es=>es.every(e=>e.complete&&e.naturalWidth>0)');assert not pg.evaluate('document.documentElement.scrollWidth>innerWidth');cards.screenshot(path=str(out/f'{w}-cards.png'));pg.screenshot(path=str(out/f'{w}-contact.png'),full_page=True)
  pg.evaluate('window.scrollTo({top:0,behavior:"instant"})')
  if w<600:pg.locator('.dd-menu-toggle').tap()
  a=pg.locator('.dd-contact>a');a.tap() if w<1200 else a.hover();pg.wait_for_timeout(80);panel=pg.locator('.dd-contact>.dd-panel');assert panel.is_visible();assert panel.locator('a').all_text_contents()==['Contact','Reviews'];pg.screenshot(path=str(out/f'{w}-contact-menu.png'))
  pg.goto(f'http://127.0.0.1:{s.server_port}/considerations.html',wait_until='domcontentloaded');pg.wait_for_timeout(100);pg.locator('.consideration-card[href="seller-questions.html"]').screenshot(path=str(out/f'{w}-selling.png'));ctx.close()
 b.close()
s.shutdown();print('Original Contact section preserved exactly; cards, exact photos, two-link menu and overflow checks passed at four widths.')
