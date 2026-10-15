exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 pg=b.new_page();pg.route('https://**/*',lambda r:r.abort())
 for path,sel in [('seller-questions.html','.loanHubGrid'),('life-changes.html','.loanHubGrid'),('considerations.html','.considerations-grid')]:
  for w in [390,1440]:
   pg.set_viewport_size({'width':w,'height':1000});pg.goto(f'http://127.0.0.1:{s.server_port}/'+path,wait_until='domcontentloaded')
   print(path,w,pg.locator(sel).evaluate('e=>({columns:getComputedStyle(e).gridTemplateColumns,overflow:document.documentElement.scrollWidth>innerWidth})'),flush=True)
 b.close()
s.shutdown()
