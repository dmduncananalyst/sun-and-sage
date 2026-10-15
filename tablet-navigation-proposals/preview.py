exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'tablet-navigation-proposals'
base='''#dd-header #dd-navigation{overflow:visible!important;scrollbar-width:none!important;}#dd-header.has-nav-rail::after{display:none!important;}#dd-header #dd-navigation>a,#dd-header #dd-navigation>.dd-group>a{font-size:14px!important;letter-spacing:.035em!important;min-height:44px!important;white-space:normal!important;}'''
css={
'directory':base+'''#dd-header #dd-navigation{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:0 32px!important;justify-content:stretch!important;align-items:start!important;padding:14px 0!important;}#dd-header #dd-navigation>a,#dd-header #dd-navigation>.dd-group>a{border-bottom:1px solid #d8dbd0!important;}''',
'sidebar':base+'''#dd-header #dd-navigation{display:flex!important;flex-direction:column!important;align-items:stretch!important;justify-content:flex-start!important;position:fixed!important;left:0!important;top:130px!important;bottom:0!important;width:202px!important;padding:18px!important;gap:0!important;background:#f4f1eb!important;border-right:1px solid #d8dbd0!important;overflow-y:auto!important;}html:root body.ss18 main#main#main#main#main#main,html:root body.ss18 footer#dd-site-footer#dd-site-footer#dd-site-footer{margin-left:202px!important;width:calc(100% - 202px)!important;}#dd-header{padding-bottom:10px!important;}#dd-header #dd-navigation>a,#dd-header #dd-navigation>.dd-group>a{border-bottom:1px solid #d8dbd0!important;}'''
}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h in [(768,1024),(820,1180),(834,1194),(1024,768),(1180,820)]:
  for name,style in css.items():
   pg=b.new_page(viewport={'width':w,'height':h},has_touch=True);pg.route('https://**/*',lambda r:r.abort());pg.goto(f'http://127.0.0.1:{s.server_port}/interior-design.html',wait_until='domcontentloaded');pg.add_style_tag(content=style + ('html:root body.ss18 footer#dd-site-footer{display:none!important;}html:root body.ss18 main#main#main#main#main#main{min-width:0!important;max-width:calc(100% - 202px)!important;}' if name=='sidebar' else ''));pg.wait_for_timeout(150);assert pg.locator('#dd-navigation>a,#dd-navigation>.dd-group').count()==10;assert not pg.evaluate('document.documentElement.scrollWidth>innerWidth');pg.screenshot(path=str(out/f'{name}-{w}.png'));pg.close()
 b.close()
s.shutdown()
for name,style in css.items():(out/(name+'.css')).write_text(style,encoding='utf-8')
print('Created two isolated visual proposals at all five requested iPad widths. Live tablet navigation unchanged.')
