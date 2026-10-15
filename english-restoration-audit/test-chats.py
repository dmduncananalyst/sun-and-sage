exec(open('responsive-header-audit/preview.py',encoding='utf-8-sig').read().split('with sync_playwright()')[0])
out=root/'english-restoration-audit';inventory=json.loads((out/'chat-inventory.json').read_text());results=[];payloads=[];seen=set();failures=[];branch_count=0
runner=r'''({targetKey=null,targetOption=0,prereqs={},submit=true})=>{
 const cfg=JSON.parse(document.querySelector('#dominiqueConversationConfig').textContent), d=document.querySelector('#sun-conversation'), triggers=[...document.querySelectorAll('main [data-sun-conversation-open="true"]')];
 if(!triggers.length)throw Error('No chat trigger');
 const originalIntro=cfg.intro||'';
 triggers[0].click();if(!d.open)throw Error('Dialog failed to open');
 if(!d.querySelector('.sunConversation__intro').textContent.startsWith(originalIntro))throw Error('Greeting changed');
 let visited=[],ended=false;
 for(let i=0;i<35;i++){
  const stage=d.querySelector('.sunConversation__stage');if(stage.querySelector('[name=firstName]'))break;
  const q=stage.querySelector('h3')?.textContent,step=cfg.steps.find(x=>x.prompt===q),key=step?.key||'referralSource';visited.push(key);
  const choices=[...stage.querySelectorAll('.sunConversation__choice')];
  if(choices.length){
   let ix=0;
   if(key===targetKey)ix=targetOption;
   else if(prereqs[key]!==undefined){let v=prereqs[key];if(Array.isArray(v))v=v[0];ix=(step?.options||[]).findIndex(o=>(typeof o==='string'?o:o.value??o.label)===v);if(ix<0)ix=0;}
   else{ix=(step?.options||[]).findIndex(o=>typeof o==='string'||!o.end);if(ix<0)ix=0;}
   choices[ix].click();if(!d.open){ended=true;break;}
  }else{const input=stage.querySelector('input,textarea');if(!input)throw Error('No response controls: '+q);input.value='Local verification only';stage.querySelector('form').requestSubmit();}
 }
 if(targetKey&&!visited.includes(targetKey))return {unreached:targetKey,visited};
 if(ended)return {ended:true,visited};
 const form=d.querySelector('.sunConversation__stage form');if(!form?.querySelector('[name=firstName]'))throw Error('No final lead collection');
 form.querySelector('[name=firstName]').value='Local QA';form.querySelector('[name=email]').value='qa@example.invalid';form.querySelector('[name=phone]').value='5550100000';
 if(submit)form.requestSubmit();return {visited,triggers:triggers.length};
}'''
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True);ctx=b.new_context(viewport={'width':1440,'height':1000});ctx.route('https://**/*',lambda r:r.abort())
 state={'error':False}
 def hub(r):
  payloads.append({'url':r.request.url,'data':r.request.post_data_json});r.fulfill(status=500 if state['error'] else 200,content_type='application/json',body='{}')
 ctx.route('https://api-na2.hsforms.com/submissions/**',hub)
 ctx.route('**/*',lambda r:r.abort() if r.request.resource_type in ['image','media','font'] else r.fallback())
 pg=ctx.new_page();pg.set_default_timeout(6000)
 for idx,item in enumerate(inventory):
  n=item['page'];cfg=item['cfg']
  try:
   pg.goto(f'http://127.0.0.1:{s.server_port}/'+n.replace('\\','/'),wait_until='domcontentloaded');pg.wait_for_function('!!document.querySelector("#sun-conversation")')
   assert not pg.locator('.dd-language,.dd-translation-notice,.dd-homepage-language-notice').count()
   # Exercise every original trigger, including multiple actions on a page.
   trigger_count=pg.locator('main [data-sun-conversation-open="true"]').count()
   for t in range(trigger_count):
    pg.locator('main [data-sun-conversation-open="true"]').nth(t).evaluate('(e)=>e.click()');assert pg.locator('#sun-conversation').evaluate('(d)=>d.open');pg.locator('.sunConversation__close').evaluate('(e)=>e.click()')
   res=pg.evaluate(runner,{});pg.wait_for_function('!!document.querySelector(".sunConversation__done")');assert payloads[-1]['data']['fields'][0]['value']=='Local QA'
   fields={f['name']:f['value'] for f in payloads[-1]['data']['fields']};assert 'How did you find our website?' in fields['message'];assert payloads[-1]['data']['context']['pageName']==pg.title()
   pg.locator('.sunConversation__return').evaluate('(e)=>e.click()');assert not pg.locator('#sun-conversation').evaluate('(d)=>d.open')
   key=json.dumps(cfg,sort_keys=True)
   if key not in seen:
    seen.add(key)
    for step in cfg['steps']:
     for oi,opt in enumerate(step.get('options',[])):
      res=pg.evaluate(runner,{'targetKey':step['key'],'targetOption':oi,'prereqs':step.get('when',{})})
      if res.get('unreached'):raise Exception('Branch not reached '+str(res))
      if not res.get('ended'):pg.wait_for_function('!!document.querySelector(".sunConversation__done")');pg.locator('.sunConversation__return').evaluate('(e)=>e.click()')
      branch_count+=1
   results.append({'page':n,'triggers':trigger_count,'status':'pass'})
  except Exception as e:failures.append({'page':n,'error':str(e)});print('FAIL',n,str(e)[:250],flush=True)
  if idx%25==0:print('Verified',idx+1,'pages;',branch_count,'option paths',flush=True)
 # Shared submission failure/retry handling.
 state['error']=True;pg.evaluate(runner,{});pg.wait_for_function('document.querySelector(".sunConversation__status")?.textContent.includes("Please try again")');assert pg.locator('.sunConversation__submit').is_enabled();state['error']=False;pg.locator('.sunConversation__stage form').evaluate('(f)=>f.requestSubmit()');pg.wait_for_function('!!document.querySelector(".sunConversation__done")')
 b.close()
s.shutdown();(out/'chat-results.json').write_text(json.dumps({'pages':results,'failures':failures,'uniqueConfigurations':len(seen),'optionPaths':branch_count,'interceptedSubmissions':len(payloads),'failureAndRetry':'pass','realLeadsSent':0},indent=2));print('DONE',len(results),'pages',len(failures),'failures',branch_count,'branches',len(payloads),'intercepted submissions',flush=True)
