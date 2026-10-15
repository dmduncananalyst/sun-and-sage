exec(open('header-hover-audit/verify-browser.py',encoding='utf-8').read().split('with sync_playwright()')[0])
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for i in range(3):
  ctx=b.new_context(viewport={'width':1024,'height':768},has_touch=True,is_mobile=True);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();pg.add_init_script('''window.navEvents=[];const remove=DOMTokenList.prototype.remove;DOMTokenList.prototype.remove=function(...args){const old=this.value;const result=remove.apply(this,args);if(old.includes('is-open')&&!this.value.includes('is-open'))window.navEvents.push({old,args,stack:new Error().stack,time:performance.now(),ready:document.readyState});return result;};''');pg.goto(f'http://127.0.0.1:{s.server_port}/life-changes/divorce.html',wait_until='domcontentloaded');pg.evaluate('document.fonts.ready');pg.wait_for_timeout(100);pg.locator('.ss22-neighborhoods>button').tap();pg.wait_for_timeout(800);print(i,pg.evaluate('''()=>({open:document.querySelector('.ss22-neighborhoods').classList.contains('is-open'),header:document.querySelector('#ss22-header').className,events:window.navEvents,scrollY})'''),flush=True);ctx.close()
 b.close()
s.shutdown()
