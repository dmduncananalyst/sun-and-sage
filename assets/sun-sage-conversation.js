
(() => {
  const cfgNode = document.getElementById('sunSageConversationConfig');
  if (!cfgNode) return;
  let cfg;
  try { cfg = JSON.parse(cfgNode.textContent); } catch (e) { return; }

  const normalizedText = el => (el?.textContent || '').replace(/\s+/g,' ').trim().replace(/\s*→\s*$/,'').trim();

  function makeTrigger(existing){
    let trigger = existing;
    if (!trigger) {
      const target = document.querySelector(cfg.target || 'main');
      if (!target) return null;
      const wrap = document.createElement('div');
      wrap.className = 'sunInlineAction';
      if (cfg.line) {
        const p = document.createElement('p');
        p.className = 'sunInlineAction__line';
        p.textContent = cfg.line;
        wrap.appendChild(p);
      }
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'sunInlineAction__button';
      btn.textContent = cfg.button;
      wrap.appendChild(btn);
      target.appendChild(wrap);
      trigger = btn;
    } else {
      trigger.classList.add('sunInlineAction__button');
      trigger.textContent = cfg.button;
      if (trigger.tagName === 'A') trigger.setAttribute('href','#');
      trigger.removeAttribute('target');
    }
    trigger.setAttribute('data-sun-conversation-open','true');
    return trigger;
  }

  if (Array.isArray(cfg.hideSelectors)) cfg.hideSelectors.forEach(sel => document.querySelectorAll(sel).forEach(el => el.setAttribute('data-sun-replaced','true')));

  let reused = [];
  if (Array.isArray(cfg.reuseTexts) && cfg.reuseTexts.length) {
    const candidates = [...document.querySelectorAll('main a, main button')];
    reused = candidates.filter(el => cfg.reuseTexts.includes(normalizedText(el)));
  }
  if (reused.length) reused.forEach(el => makeTrigger(el));
  else makeTrigger(null);

  const dialog = document.createElement('dialog');
  dialog.className = 'sunConversation';
  dialog.setAttribute('aria-labelledby','sunConversationTitle');
  const assetPrefix = cfg.assetPrefix || 'assets/';
  dialog.innerHTML = `
    <div class="sunConversation__inner">
      <div class="sunConversation__top">
        <div class="sunConversation__brand"><img src="${assetPrefix}sun-sage-key.png" alt=""><span>SUN AND SAGE</span></div>
        <button class="sunConversation__close" type="button" aria-label="Close">×</button>
      </div>
      <h2 class="sunConversation__title" id="sunConversationTitle">Let’s Work Through This Together</h2>
      <p class="sunConversation__intro"></p>
      <div class="sunConversation__stage" aria-live="polite"></div>
    </div>`;
  document.body.appendChild(dialog);

  const intro = dialog.querySelector('.sunConversation__intro');
  const stage = dialog.querySelector('.sunConversation__stage');
  const close = dialog.querySelector('.sunConversation__close');
  const answers = {};
  const history = [];
  let index = 0;

  function stepApplies(step){
    if (!step.when) return true;
    return Object.entries(step.when).every(([k,v]) => {
      const actual = answers[k];
      if (Array.isArray(v)) return v.includes(actual);
      return actual === v;
    });
  }
  function nextIndex(from){
    let i = from + 1;
    while (i < cfg.steps.length && !stepApplies(cfg.steps[i])) i++;
    return i;
  }
  function prevIndex(){
    return history.length ? history.pop() : 0;
  }

  function render(){
    intro.textContent = cfg.intro || '';
    intro.hidden = !intro.textContent.trim();
    if (index >= cfg.steps.length) return renderContact();
    const step = cfg.steps[index];
    if (!stepApplies(step)) { index = nextIndex(index); return render(); }
    stage.innerHTML = '';
    const q = document.createElement('h3');
    q.className = 'sunConversation__question';
    q.textContent = step.prompt;
    stage.appendChild(q);
    const choices = document.createElement('div');
    choices.className = 'sunConversation__choices';
    (step.options || []).forEach(optRaw => {
      const opt = typeof optRaw === 'string' ? {label:optRaw,value:optRaw} : optRaw;
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'sunConversation__choice';
      b.textContent = opt.label;
      b.addEventListener('click', () => {
        // Clear answers from later steps if the visitor changed direction.
        const stepPos = cfg.steps.indexOf(step);
        cfg.steps.slice(stepPos + 1).forEach(s => { delete answers[s.key]; delete answers[s.key + '__label']; });
        answers[step.key] = opt.value ?? opt.label;
        answers[step.key + '__label'] = opt.label;
        if (opt.end) { dialog.close(); return; }
        history.push(index);
        index = nextIndex(index);
        render();
      });
      choices.appendChild(b);
    });
    stage.appendChild(choices);
    if (history.length) {
      const nav = document.createElement('div'); nav.className='sunConversation__nav';
      const back = document.createElement('button'); back.type='button'; back.className='sunConversation__back'; back.textContent='← Back';
      back.addEventListener('click',()=>{ index=prevIndex(); render(); }); nav.appendChild(back); stage.appendChild(nav);
    }
  }

  function renderSoftEnd(){
    stage.innerHTML = `<div class="sunConversation__done"><h3>No problem.</h3><p>Keep exploring. This will still be here if you want to pick it back up.</p><button type="button" class="sunConversation__return">Back to the page</button></div>`;
    stage.querySelector('.sunConversation__return').addEventListener('click',()=>dialog.close());
  }

  function renderContact(){
    stage.innerHTML = '';
    if (cfg.contactHeading) { const q = document.createElement('h3'); q.className='sunConversation__question'; q.textContent = cfg.contactHeading; stage.appendChild(q); }
    const form = document.createElement('form'); form.className='sunConversation__fields';
    form.innerHTML = `
      <label class="sunConversation__label">What’s your first name?<input class="sunConversation__input" name="firstName" autocomplete="given-name" required></label>
      <label class="sunConversation__label">${cfg.emailLabel || 'What’s the best email for Dominique to reach you?'}<input class="sunConversation__input" name="email" type="email" autocomplete="email" required></label>
      <label class="sunConversation__label">Phone number, if you want Dominique to call or text you.<input class="sunConversation__input" name="phone" type="tel" autocomplete="tel"></label>
      <button class="sunConversation__submit" type="submit">${cfg.submitText || 'Send This to Dominique'}</button>
      <p class="sunConversation__status" role="status" aria-live="polite"></p>`;
    stage.appendChild(form);
    if (history.length) {
      const nav = document.createElement('div'); nav.className='sunConversation__nav';
      const back = document.createElement('button'); back.type='button'; back.className='sunConversation__back'; back.textContent='← Back';
      back.addEventListener('click',()=>{ index=prevIndex(); render(); }); nav.appendChild(back); stage.appendChild(nav);
    }
    form.addEventListener('submit', submitConversation);
  }

  async function submitConversation(event){
    event.preventDefault();
    const form = event.currentTarget;
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const button = form.querySelector('.sunConversation__submit');
    const status = form.querySelector('.sunConversation__status');
    button.disabled = true; button.textContent = 'Sending…'; status.textContent='';
    const responseLines = (cfg.steps || []).map(step => {
      const label = answers[step.key+'__label'];
      return label ? `${step.prompt} ${label}` : '';
    }).filter(Boolean);
    const message = [
      `Page: ${document.title}`,
      `CTA: ${cfg.button}`,
      ...responseLines
    ].join('\n');
    const cookie = document.cookie.match(/(?:^|;\s*)hubspotutk=([^;]+)/)?.[1];
    const fields = [
      {name:'firstname',value:String(data.get('firstName')||'')},
      {name:'email',value:String(data.get('email')||'')},
      {name:'phone',value:String(data.get('phone')||'')},
      {name:'message',value:message},
    ].filter(f=>f.value);
    try{
      const endpoint='https://api-na2.hsforms.com/submissions/v3/integration/submit/247079925/da6d1bd8-d7e9-4ff5-91a3-efa6c8abadfc';
      const res=await fetch(endpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({fields,context:{...(cookie?{hutk:cookie}:{}),pageUri:location.href,pageName:document.title}})});
      if(!res.ok) throw new Error('Submission failed');
      stage.innerHTML = `<div class="sunConversation__done"><h3>Got it.</h3><p>${cfg.thankYou || 'Dominique has what you shared and can follow up from here.'}</p><button type="button" class="sunConversation__return">Back to the page</button></div>`;
      stage.querySelector('.sunConversation__return').addEventListener('click',()=>dialog.close());
    }catch(e){
      button.disabled=false; button.textContent=cfg.submitText || 'Send This to Dominique';
      status.textContent='That did not go through. Please try again.';
    }
  }

  document.addEventListener('click', e => {
    const trigger = e.target.closest?.('[data-sun-conversation-open="true"]');
    if (!trigger) return;
    e.preventDefault();
    Object.keys(answers).forEach(k=>delete answers[k]); history.splice(0); index=0; render();
    if (typeof dialog.showModal === 'function') dialog.showModal();
  });
  close.addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close()});
})();
