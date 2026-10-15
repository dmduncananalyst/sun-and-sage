import sys,os,json,threading,http.server,functools
from pathlib import Path
sys.path.insert(0,os.path.join(os.environ['TEMP'],'dommydom-browser-tools-complete'))
from playwright.sync_api import sync_playwright
root=Path.cwd();out=root/'article-card-audit'
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
pages=[root/'life-changes/marriage.html']
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 print('browser ready',flush=True)
 page=browser.new_page()
 page.route('https://**/*',lambda r:r.abort())
 for path in pages:
  for width in [1440,390]:
   page.set_viewport_size({'width':width,'height':1000})
   page.goto(f'http://127.0.0.1:{server.server_port}/'+path.relative_to(root).as_posix(),wait_until='domcontentloaded')
   page.locator('.loanHubGrid').first.wait_for()
   page.evaluate('async()=>{for(const img of document.querySelectorAll(".loanHubGrid img")){img.loading="eager";}await Promise.race([Promise.all([...document.querySelectorAll(".loanHubGrid img")].map(i=>i.decode().catch(()=>{}))),new Promise(r=>setTimeout(r,1500))]);await document.fonts.ready;}')
   page.wait_for_timeout(350)
   data=page.evaluate('''()=>{const grids=[...document.querySelectorAll('.loanHubGrid')].filter(g=>g.querySelector(':scope > .loanHubItem > .final-static-answer'));return {overflow:document.documentElement.scrollWidth>innerWidth,grids:grids.map(g=>({rows:getComputedStyle(g).gridAutoRows,cards:[...g.querySelectorAll(':scope > .loanHubItem')].map(c=>{const r=c.getBoundingClientRect(),a=c.querySelector('.loanLearn a'),p=c.querySelector('.final-static-answer-copy'),im=c.querySelector('img');const ar=a?.getBoundingClientRect();return {top:r.top,bottom:r.bottom,height:r.height,width:r.width,linkBottom:ar?.bottom,linkVisible:!!ar&&ar.height>0,href:a?.getAttribute('href'),blank:ar&&p?ar.top-p.getBoundingClientRect().bottom:null,clipped:[...c.querySelectorAll('h2,p')].some(t=>t.scrollHeight>t.clientHeight+1),image:!im||im.complete&&im.naturalWidth>0}})}))}}''')
   for g in data['grids']:
    rows={}
    for c in g['cards']:rows.setdefault(round(c['top']),[]).append(c)
    g['aligned']=all(max(c['bottom'] for c in row)-min(c['bottom'] for c in row)<2 and max(c['linkBottom'] or 0 for c in row)-min(c['linkBottom'] or 0 for c in row)<2 for row in rows.values())
   data.update(page=path.relative_to(root).as_posix(),width=width)
   results.append(data)
   print(data['page'],width,'overflow',data['overflow'],'grids',len(data['grids']),'aligned',all(g['aligned'] for g in data['grids']),flush=True)
   if path.name=='marriage.html' and width in [1440,390]:
    page.locator('.loanHubGrid').screenshot(path=str(out/f'marriage-{width}.png'))
    page.locator('.loanHubGrid .loanLearn a').first.click(trial=True)
    page.locator('.loanHubGrid').evaluate('g=>window.scrollTo(0,g.getBoundingClientRect().top+scrollY-20)')
    page.screenshot(path=str(out/f'marriage-viewport-{width}.png'))
 (out/'marriage-final.json').write_text(json.dumps(results,indent=2))
 page.close()
 browser.close()
(out/'marriage-final.json').write_text(json.dumps(results,indent=2))
server.shutdown()



