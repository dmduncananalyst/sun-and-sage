exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
import ast,re
out=root/'english-restoration-audit';module=ast.parse((out/'test-chats.py').read_text(encoding='utf-8-sig'));runner=next(ast.literal_eval(n.value) for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='runner' for t in n.targets));results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w in [834,390]:
  ctx=b.new_context(viewport={'width':w,'height':1000},has_touch=True);ctx.route('https://**/*',lambda r:r.abort());ctx.route('https://api-na2.hsforms.com/submissions/**',lambda r:r.fulfill(status=200,content_type='application/json',body='{}'));pg=ctx.new_page()
  for n in ['index.html','contact.html','buyer-consultation.html','seller-consultation.html','sell-free-home-valuation.html','interior-design.html','life-changes/marriage.html']:
   pg.goto(f'http://127.0.0.1:{s.server_port}/'+n,wait_until='domcontentloaded');pg.wait_for_function('!!document.querySelector("#sun-conversation")');pg.evaluate('document.querySelector("main [data-sun-conversation-open=true]").click()')
   if n=='contact.html':pg.screenshot(path=str(out/f'english-chat-{w}.png'))
   pg.locator('.sunConversation__close').evaluate('(e)=>e.click()');pg.evaluate(runner,{});pg.wait_for_function('!!document.querySelector(".sunConversation__done")');results.append({'page':n,'width':w,'status':'pass'})
  ctx.close()
 b.close()
s.shutdown();(out/'touch-chat-results.json').write_text(json.dumps(results,indent=2));print('PASS',len(results),'touch chat flows with mocked submissions')
