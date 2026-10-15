exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 pg=b.new_page(viewport={'width':1440,'height':900});pg.route('https://**/*',lambda r:r.abort())
 pg.goto(f'http://127.0.0.1:{s.server_port}/blog.html');pg.wait_for_timeout(300)
 print(pg.locator('#dd-navigation>a').evaluate_all('(aa)=>aa.map(a=>({text:a.textContent,style:a.getAttribute("style"),color:getComputedStyle(a).color,opacity:getComputedStyle(a).opacity,visibility:getComputedStyle(a).visibility,fill:getComputedStyle(a).webkitTextFillColor}))'))
 print(pg.evaluate('''()=>{let a=document.querySelector('#dd-navigation>a[aria-current]'),out=[];function walk(rs){for(let r of rs){if(r.selectorText){try{if(a.matches(r.selectorText))out.push(r.cssText)}catch{}}else if(r.cssRules)walk(r.cssRules)}}for(let s of document.styleSheets){try{walk(s.cssRules)}catch{}}return out}'''))
 b.close()
s.shutdown()
