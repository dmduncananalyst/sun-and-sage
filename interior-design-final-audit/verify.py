exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'interior-design-final-audit'
import re
old=re.search(r'<main\b[\s\S]*?</main>',(out/'before-interior-design.html').read_text(encoding='utf-8'))[0];new=re.search(r'<main\b[\s\S]*?</main>',Path('interior-design.html').read_text(encoding='utf-8'))[0]
for chunk in re.findall(r'<section\b[\s\S]*?</section>',old):assert chunk in new,'Existing section changed'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h in [(390,844),(768,1024),(1024,768),(1440,1000)]:
  ctx=b.new_context(viewport={'width':w,'height':h},has_touch=w<1200);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/interior-design.html',wait_until='domcontentloaded');pg.wait_for_timeout(200);pg.evaluate('document.documentElement.style.scrollBehavior="auto"')
  for selector,kind in [('.dd-design-paths','cards'),('.dd-design-portfolio','portfolio')]:
   el=pg.locator(selector);el.scroll_into_view_if_needed();pg.wait_for_timeout(1000);assert el.locator('img').evaluate_all('es=>es.every(e=>e.complete&&e.naturalWidth>0)');el.screenshot(path=str(out/f'{w}-{kind}.png'))
  assert not pg.evaluate('document.documentElement.scrollWidth>innerWidth');pg.screenshot(path=str(out/f'{w}-full.png'),full_page=True);pg.evaluate('window.scrollTo({top:0,behavior:"instant"})')
  if w<600:pg.locator('.dd-menu-toggle').tap()
  a=pg.locator('.dd-interior>a');a.tap() if w<1200 else a.hover();pg.wait_for_timeout(80);panel=pg.locator('.dd-interior>.dd-panel');assert panel.is_visible();assert panel.locator('a').all_text_contents()==['Interior Design','Portfolio']
  if w>=600:
   d=pg.locator('.dd-interior').evaluate('e=>{let a=e.querySelector("a").getBoundingClientRect(),p=e.querySelector(".dd-panel").getBoundingClientRect();return Math.abs(a.x+a.width/2-p.x-p.width/2)}');assert d<1,d
  pg.screenshot(path=str(out/f'{w}-dropdown.png'));ctx.close()
 b.close()
s.shutdown();print('Passed four widths; original sections intact, all new photos decoded, dropdown centered and exact two links.')

