
(() => {
  const cfgNode = document.getElementById('sunSageConversationConfig');
  if (!cfgNode) return;
  let cfg;
  try { cfg = JSON.parse(cfgNode.textContent); } catch (e) { return; }
  cfg.steps = cfg.steps || [];
  cfg.steps = cfg.steps.filter(step => step.key !== 'referralSource');
  cfg.steps.push({key:'referralSource',prompt:'How did you find our website?',options:['Google','AI (ChatGPT, Claude, Gemini, etc.)','Instagram','Other']});

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
    trigger.setAttribute('aria-controls','sun-conversation');
    trigger.setAttribute('aria-haspopup',cfg.inline ? 'false' : 'dialog');
    return trigger;
  }

  if (Array.isArray(cfg.hideSelectors)) cfg.hideSelectors.forEach(sel => document.querySelectorAll(sel).forEach(el => el.setAttribute('data-sun-replaced','true')));

  let reused = [];
  if (Array.isArray(cfg.reuseTexts) && cfg.reuseTexts.length) {
    const candidates = [...document.querySelectorAll('main a, main button')];
    reused = candidates.filter(el => cfg.reuseTexts.includes(normalizedText(el)));
  }
  if (!cfg.inline) {
    if (reused.length) reused.forEach(el => makeTrigger(el));
    else if (!document.querySelector('main [data-sun-conversation-open="true"]')) makeTrigger(null);
  }

  // v39: the city-page action belongs after the page content on mobile.
  // A placeholder restores the original desktop layout when the viewport grows.
  const cityMain = document.querySelector('main[data-city-page]');
  if (cityMain && !cfg.inline) {
    const cityActions = [...cityMain.querySelectorAll('[data-sun-conversation-open="true"]')];
    if (cityActions.length) {
      const mobile = window.matchMedia('(max-width: 800px)');
      const placements = cityActions.map(action => {
        const placeholder = document.createComment('city CTA desktop position');
        action.before(placeholder);
        return {action, placeholder};
      });
      const bottom = document.createElement('section');
      bottom.className = 'sunInlineAction v39-city-cta';
      bottom.setAttribute('aria-label', 'Home search in ' + cityMain.dataset.cityPage);
      function placeCityAction() {
        if (mobile.matches) {
          cityMain.appendChild(bottom);
          placements.forEach(({action}) => bottom.appendChild(action));
        } else {
          placements.forEach(({action, placeholder}) => placeholder.after(action));
          bottom.remove();
        }
      }
      placeCityAction();
      if (mobile.addEventListener) mobile.addEventListener('change', placeCityAction);
      else mobile.addListener(placeCityAction);
    }
  }

  const dialog = document.createElement(cfg.inline ? 'section' : 'dialog');
  dialog.id = 'sun-conversation';
  dialog.className = 'sunConversation' + (cfg.inline ? ' sunConversation--inline' : '');
  dialog.setAttribute('aria-labelledby','sunConversationTitle');
  const assetPrefix = cfg.assetPrefix || 'assets/';
  const isSensitivePage = /\/life-changes\/(death|divorce)\//.test(location.pathname);
  const conversationTitle = cfg.title || (isSensitivePage ? 'Share Your Plans' : (cfg.button || 'Work With Dominique'));
  dialog.innerHTML = `
    <div class="sunConversation__inner">
      <div class="sunConversation__top">
        <div class="sunConversation__brand"><img src="${assetPrefix}sun-sage-key.png" alt=""><span>SUN AND SAGE</span></div>
        <button class="sunConversation__close" type="button" aria-label="Close">×</button>
      </div>
      <h2 class="sunConversation__title" id="sunConversationTitle">${conversationTitle}</h2>
      <p class="sunConversation__intro"></p>
      <div class="sunConversation__stage" aria-live="polite"></div>
    </div>`;
  (cfg.inline ? document.querySelector(cfg.target) || document.body : document.body).appendChild(dialog);

  const intro = dialog.querySelector('.sunConversation__intro');
  const stage = dialog.querySelector('.sunConversation__stage');
  const close = dialog.querySelector('.sunConversation__close');
  const answers = {};
  const history = [];
  let entryDetails = [];
  let activeCTA = cfg.button;
  let index = 0;
  function closeConversation(){
    if(cfg.inline){Object.keys(answers).forEach(k=>delete answers[k]);history.splice(0);index=0;render();}
    else dialog.close();
  }
  function advance(step, value){
    const stepPos=cfg.steps.indexOf(step);
    cfg.steps.slice(stepPos+1).forEach(s=>{delete answers[s.key];delete answers[s.key+'__label']});
    answers[step.key]=value;answers[step.key+'__label']=value;
    history.push(index);index=nextIndex(index);render();
  }

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
    intro.textContent = [cfg.intro || '', ...entryDetails].filter(Boolean).join(' · ');
    intro.hidden = !intro.textContent.trim();
    if (index >= cfg.steps.length) return renderContact();
    const step = cfg.steps[index];
    if (!stepApplies(step)) { index = nextIndex(index); return render(); }
    stage.innerHTML = '';
    const q = document.createElement('h3');
    q.className = 'sunConversation__question';
    q.textContent = step.prompt;
    stage.appendChild(q);
    if (step.type === 'text') {
      const form=document.createElement('form');form.className='sunConversation__fields';
      const input=document.createElement(step.multiline?'textarea':'input');
      input.className='sunConversation__input';input.name=step.key;input.required=step.required!==false;
      input.placeholder=step.placeholder||'';input.setAttribute('aria-label',step.prompt);
      input.maxLength=step.multiline?2000:300;
      input.value=answers[step.key]||'';
      if(step.multiline)input.rows=4;
      const submit=document.createElement('button');submit.type='submit';submit.className='sunConversation__submit';submit.textContent='Continue';
      form.append(input,submit);stage.appendChild(form);
      form.addEventListener('submit',e=>{e.preventDefault();if(form.reportValidity())advance(step,input.value.trim())});
      if(history.length){const back=document.createElement('button');back.type='button';back.className='sunConversation__back';back.textContent='Edit previous answer';back.addEventListener('click',()=>{index=prevIndex();render()});stage.appendChild(back)}
      return;
    }
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
        if (opt.end) { closeConversation(); return; }
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
    stage.querySelector('.sunConversation__return').addEventListener('click',closeConversation);
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
      `CTA: ${activeCTA}`,
      ...entryDetails,
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
      stage.innerHTML = `<div class="sunConversation__done"><h3>Thank you.</h3><p>Dominique will follow up with you shortly.</p><button type="button" class="sunConversation__return">Back to the page</button></div>`;
      stage.querySelector('.sunConversation__return').textContent=cfg.inline?'Send Another Message':'Back to the page';
      stage.querySelector('.sunConversation__return').addEventListener('click',closeConversation);
    }catch(e){
      button.disabled=false; button.textContent=cfg.submitText || 'Send This to Dominique';
      status.textContent='That did not go through. Please try again.';
    }
  }

  function openConversation(trigger, details = []) {
    entryDetails = details;
    activeCTA = trigger?.dataset.sunConversationLabel || normalizedText(trigger) || cfg.button;
    Object.keys(answers).forEach(k=>delete answers[k]); history.splice(0); index=0; render();
    if (cfg.inline) {
      dialog.scrollIntoView({block:'center'});
      dialog.querySelector('.sunConversation__choice,.sunConversation__input')?.focus({preventScroll:true});
    } else if (typeof dialog.showModal === 'function') dialog.showModal();
  }
  // Explicit chat triggers take precedence over older contact-form handlers.
  document.addEventListener('click', e => {
    const trigger = e.target.closest?.('[data-sun-conversation-open="true"]');
    if (!trigger) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    openConversation(trigger);
  }, true);
  document.addEventListener('submit', e => {
    const form = e.target.closest?.('[data-sun-conversation-form]');
    if (!form) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    const details = [...form.querySelectorAll('input,select,textarea')].map(field => {
      const label = field.closest('label')?.querySelector('span')?.textContent.trim() || field.name;
      return field.value.trim() ? `${label}: ${field.value.trim()}` : '';
    }).filter(Boolean);
    openConversation(e.submitter || form.querySelector('button[type="submit"],button'), details);
  }, true);
  close.addEventListener('click',closeConversation);
  if(!cfg.inline) dialog.addEventListener('click',e=>{if(e.target===dialog)closeConversation()});
  if(cfg.inline) render();
})();
