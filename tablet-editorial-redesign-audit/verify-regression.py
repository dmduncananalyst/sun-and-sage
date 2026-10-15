exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
from PIL import Image,ImageChops
out=root/'tablet-editorial-redesign-audit';old=(out/'before-tablet-language.css').read_text(encoding='utf-8')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h in [(390,844),(430,932),(1280,900),(1440,1000)]:
  shots=[]
  for phase in ['before','after']:
   ctx=b.new_context(viewport={'width':w,'height':h},has_touch=w<1200);ctx.route('https://**/*',lambda r:r.abort())
   if phase=='before':ctx.route('**/tablet-language.css*',lambda r:r.fulfill(body=old,content_type='text/css'))
   pg=ctx.new_page();pg.goto(f'http://127.0.0.1:{s.server_port}/about.html',wait_until='domcontentloaded');pg.wait_for_timeout(500)
   assert pg.locator('link[href*="tablet-language.css?v=20261015-folio"]').count()==1
   if w<600:pg.locator('.dd-menu-toggle').tap();pg.wait_for_timeout(300);pg.screenshot(path=str(out/f'{phase}-{w}-phone.png'));shots.append(out/f'{phase}-{w}-phone.png')
   else:pg.locator('.dd-interior>a').hover();pg.wait_for_timeout(300);assert pg.locator('.dd-interior>.dd-panel').is_visible();pg.screenshot(path=str(out/f'{phase}-{w}-desktop.png'));shots.append(out/f'{phase}-{w}-desktop.png')
   assert not pg.evaluate('document.documentElement.scrollWidth>innerWidth');ctx.close()
  assert ImageChops.difference(Image.open(shots[0]),Image.open(shots[1])).getbbox() is None,(w,'Desktop/phone pixels changed')
 b.close()
s.shutdown();print('Desktop and phone before/after screenshots are pixel-identical at all four requested widths. Versioned CSS is loaded.')
