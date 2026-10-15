exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'editorial-sidebar-final';out.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h in [(768,1024),(820,1180),(834,1194),(1024,768),(1180,820)]:
  pg=b.new_page(viewport={'width':w,'height':h},has_touch=True);pg.route('https://**/*',lambda r:r.abort());pg.goto(f'http://127.0.0.1:{s.server_port}/considerations.html',wait_until='domcontentloaded')
  pg.wait_for_timeout(900);pg.screenshot(path=str(out/f'{w}-closed.png'))
  assert pg.locator('#dd-navigation').evaluate('e=>e.scrollWidth<=e.clientWidth')
  for label in ['Sell','Interior Design']:
   a=pg.locator('#dd-navigation>.dd-group>a').filter(has_text=label).first;a.tap();pg.wait_for_timeout(220);group=a.locator('..');panel=group.locator(':scope>.dd-panel');assert panel.is_visible();d=group.evaluate('e=>{let a=e.querySelector("a").getBoundingClientRect(),p=e.querySelector(".dd-panel").getBoundingClientRect(),n=e.nextElementSibling.getBoundingClientRect();return {gap:p.top-a.bottom,x:p.x,right:p.right,next:n.top,bottom:p.bottom}}');assert abs(d['gap'])<=3 and d['x']>=0 and d['right']<=200 and d['next']>=d['bottom']-1,d;assert pg.locator('#dd-navigation').evaluate('e=>e.scrollWidth<=e.clientWidth');pg.screenshot(path=str(out/f'{w}-{label.replace(" ","-")}.png'));pg.keyboard.press('Escape');pg.evaluate('document.activeElement?.blur()')
  pg.close()
 b.close()
s.shutdown();print('Both submenus expand directly below their labels at all five tablet widths, without covering content or horizontal scrolling.')



