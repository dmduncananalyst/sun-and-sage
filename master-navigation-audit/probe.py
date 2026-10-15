exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'master-navigation-audit'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in [600,744,768,1024,1280,1440,390]:
  ctx=b.new_context(viewport={'width':w,'height':1000},has_touch=w<1200);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();errors=[];pg.on('pageerror',lambda e:errors.append(str(e)));pg.goto(f'http://127.0.0.1:{s.server_port}/about.html',wait_until='domcontentloaded');pg.wait_for_timeout(250)
  d=pg.locator('#dd-header').evaluate('h=>({height:h.offsetHeight,compact:h.classList.contains("is-compact"),rail:h.classList.contains("has-nav-rail"),overflow:document.documentElement.scrollWidth>innerWidth,nav: [...h.querySelector("nav").children].filter(e=>e.matches("a,.dd-group")).map(e=>({text:(e.matches("a")?e:e.querySelector("a")).textContent,rect:e.getBoundingClientRect().toJSON()})),zones:[...h.children].map(e=>({class:e.className,rect:e.getBoundingClientRect().toJSON()}))})');d.update(width=w,errors=errors);results.append(d);pg.screenshot(path=str(out/f'probe-{w}.png'));ctx.close()
 b.close()
s.shutdown();(out/'probe.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(json.dumps([{k:v for k,v in d.items() if k not in ['nav','zones']} for d in results]))
