# Layout stress fixtures only. These are not translations and produce no translated-page screenshots.
exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
fixtures={'es':'Información completa sobre la vivienda y las decisiones de propiedad. ','zh-CN':'完整的住房信息和房产规划。','fa':'اطلاعات کامل درباره خانه و برنامه‌ریزی خرید ملک. ','hy':'Ամբողջական տեղեկություններ տան և անշարժ գույքի վերաբերյալ։ '}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in [390,834,1440]:
  pg=b.new_page(viewport={'width':w,'height':1000});pg.route('https://**/*',lambda r:r.abort())
  for lang,text in fixtures.items():
   pg.goto(f'http://127.0.0.1:{s.server_port}/considerations.html',wait_until='domcontentloaded');pg.evaluate('''([lang,text])=>{document.documentElement.classList.add('dd-translated');const m=document.querySelector('main');m.dir=lang==='fa'?'rtl':'ltr';m.querySelectorAll('.consideration-card h2').forEach(e=>e.textContent=text.repeat(2));m.querySelectorAll('.consideration-card p').forEach(e=>e.textContent=text.repeat(8));}''',[lang,text]);assert not pg.evaluate('document.documentElement.scrollWidth>innerWidth'),(w,lang);assert pg.locator('.consideration-card p,.consideration-card h2').evaluate_all('es=>es.every(e=>e.scrollHeight<=e.clientHeight+2&&getComputedStyle(e).textOverflow!=="ellipsis")'),(w,lang)
  pg.close()
 b.close()
s.shutdown();print('12 layout-only stress cases passed: full card text wraps at readable sizes. Fixtures are not Google translation output.')
