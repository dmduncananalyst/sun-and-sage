exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'complete-master-audit';results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in [1440,1024,768,390,320]:
  pg=b.new_page(viewport={'width':w,'height':1000});pg.route('https://**/*',lambda r:r.abort());pg.goto(f'http://127.0.0.1:{s.server_port}/buy-a-home.html',wait_until='domcontentloaded');pg.wait_for_timeout(200);d=pg.locator('main').evaluate('m=>({overflow:document.documentElement.scrollWidth>innerWidth,chart:m.querySelector(".dd-buy-chart").getBoundingClientRect().toJSON(),wheel:m.querySelector(".dd-buy-wheel").getBoundingClientRect().toJSON(),bars:[...m.querySelectorAll(".dd-buy-bar-fill")].map(e=>({style:e.style.height,height:e.offsetHeight,parent:e.parentElement.offsetHeight}))})');results.append({'width':w,**d});pg.screenshot(path=str(out/f'probe-buy-{w}.png'),full_page=True);pg.close()
 b.close()
s.shutdown();(out/'probe-results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results))
