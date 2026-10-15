exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for source,w,h in [('blog.html',1440,900),('about.html',768,1024),('life-changes/marriage.html',390,844)]:
  ctx=b.new_context(viewport={'width':w,'height':h},has_touch=w<1280);ctx.route('https://**/*',lambda r:r.abort());pg=ctx.new_page();errors=[];pg.on('pageerror',lambda e:errors.append(str(e)));pg.goto(f'http://127.0.0.1:{s.server_port}/{source}',wait_until='domcontentloaded');pg.wait_for_timeout(200)
  a=pg.locator('#dd-header a.dd-search');assert a.count()==1;assert a.get_attribute('aria-haspopup') is None;assert pg.locator('#dd-header .dd-search .dd-panel').count()==0
  if w==1440:a.hover();pg.wait_for_timeout(300);assert pg.locator('#dd-header .is-open').count()==0
  pg.screenshot(path=str(out/f'direct-search-{w}.png'))
  if w<1280:a.tap()
  else:a.click()
  pg.wait_for_url('**/search.html');assert not errors,errors
  results.append({'width':w,'source':source,'destination':pg.url,'errors':errors});ctx.close()
 b.close()
s.shutdown();(out/'direct-search-results.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(json.dumps(results))
