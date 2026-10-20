/* Static catalogs only. Browsing and language switching never contact a paid API. */
(() => {
  'use strict';
  const node=document.getElementById('dommydom-locale');
  if(!node)return;
  const cfg=JSON.parse(node.textContent),catalog=window.DOMMYDOM_TRANSLATIONS||{};
  const t=value=>catalog[value]||value;
  window.dommydomLanguage=cfg.language;
  window.dommydomTranslateSaved=t;
  let select=document.getElementById('dd-language');
  if(!select){
    const wrap=document.createElement('div');wrap.className='dd-language-selector';
    select=document.createElement('select');select.id='dd-language';
    select.setAttribute('aria-label',t('Language'));
    const globe=document.createElement('span');globe.textContent='🌐';globe.setAttribute('aria-hidden','true');
    for(const [code,name] of Object.entries(cfg.languages)){const option=new Option(name,code);option.selected=code===cfg.language;select.add(option)}
    wrap.append(globe,select);(document.querySelector('.dd-header-tools')||document.querySelector('header')||document.body).append(wrap);
  }
  const toolbar=document.querySelector('.dd-header-tools');
  if(toolbar&&!toolbar.contains(select)){const search=toolbar.querySelector('.dd-search');if(search)search.insertAdjacentElement('afterend',select.parentElement);else toolbar.append(select.parentElement)}
  function destination(code){
    const root=new URL(cfg.rootPrefix||('../'.repeat(cfg.path.split('/').length-1+(cfg.language==='en'?0:1))||'./'),location.href);
    const path=(code==='en'?'':code+'/')+(cfg.path==='index.html'&&location.protocol!=='file:'?'':cfg.path);
    return new URL(path||'./',root).href+location.search+location.hash;
  }
  select.addEventListener('change',()=>{try{localStorage.setItem('dommydom-language',select.value)}catch{}location.assign(destination(select.value))});
  // Apply a saved preference on subsequent English visits. Explicit locale links win.
  try{
    const saved=localStorage.getItem('dommydom-language');
    if(cfg.language==='en'&&saved&&saved!=='en'&&cfg.languages[saved]&&!new URLSearchParams(location.search).has('language')){
      location.replace(destination(saved));return;
    }
    localStorage.setItem('dommydom-language',cfg.language);
  }catch{}
  function localize(root){
    if(root.nodeType===Node.TEXT_NODE){
      if(root.parentElement?.closest('script,style,code,pre,[translate=no],input,textarea'))return;
      const text=root.textContent,trim=text.trim();if(catalog[trim]&&catalog[trim]!==trim)root.textContent=text.replace(trim,catalog[trim]);return;
    }
    if(root.nodeType!==Node.ELEMENT_NODE)return;
    if(root.matches('script,style,code,pre,[translate=no]'))return;
    for(const name of ['aria-label','title','placeholder','alt'])if(root.hasAttribute(name)){const value=root.getAttribute(name);if(catalog[value]&&catalog[value]!==value)root.setAttribute(name,catalog[value])}
    if(root.matches('input,textarea'))return;
    for(const child of root.childNodes)localize(child);
  }
  if(cfg.language!=='en'){
    document.addEventListener('invalid',event=>{
      const field=event.target,validity=field.validity;if(!validity||validity.customError)return;
      const message=validity.valueMissing?'Please fill out this field.':validity.typeMismatch&&field.type==='email'?'Please enter a valid email address.':validity.patternMismatch?'Please match the requested format.':validity.rangeOverflow||validity.rangeUnderflow?'Please enter a value in the allowed range.':'Please check this value.';
      field.setCustomValidity(t(message));
    },true);
    document.addEventListener('input',event=>{if(event.target.setCustomValidity)event.target.setCustomValidity('')},true);
    localize(document.body);
    new MutationObserver(records=>{for(const r of records){if(r.type==='characterData')localize(r.target);else if(r.type==='attributes')localize(r.target);else for(const n of r.addedNodes)localize(n)}}).observe(document.body,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:['aria-label','title','placeholder','alt']});
  }
})();
