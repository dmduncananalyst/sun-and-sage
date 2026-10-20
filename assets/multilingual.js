/* Static catalogs only. Browsing and language switching never contact a paid API. */
(() => {
  'use strict';
  const node=document.getElementById('dommydom-locale');
  if(!node)return;
  const cfg=JSON.parse(node.textContent),catalog=window.DOMMYDOM_TRANSLATIONS||{};
  const t=value=>catalog[value]||value;
  window.dommydomLanguage=cfg.language;
  window.dommydomTranslateSaved=t;
  const wrap=document.createElement('div');wrap.className='dd-language-selector';
  const label=document.createElement('label');label.htmlFor='dd-language';label.textContent=t('Language');
  const select=document.createElement('select');select.id='dd-language';
  for(const [code,name] of Object.entries(cfg.languages)){const option=new Option(name,code);option.selected=code===cfg.language;select.add(option)}
  select.addEventListener('change',()=>{try{localStorage.setItem('dommydom-language',select.value)}catch{}location.assign((select.value==='en'?'/':'/'+select.value+'/')+(cfg.path==='index.html'?'':cfg.path)+location.search+location.hash)});
  wrap.append(label,select);(document.querySelector('header')||document.body).insertAdjacentElement('afterend',wrap);
  // Apply a saved preference on subsequent English visits. Explicit locale links win.
  try{
    const saved=localStorage.getItem('dommydom-language');
    if(cfg.language==='en'&&saved&&saved!=='en'&&cfg.languages[saved]&&!new URLSearchParams(location.search).has('language')){
      location.replace('/'+saved+'/'+(cfg.path==='index.html'?'':cfg.path)+location.search+location.hash);return;
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
    localize(document.body);
    new MutationObserver(records=>{for(const r of records){if(r.type==='characterData')localize(r.target);else if(r.type==='attributes')localize(r.target);else for(const n of r.addedNodes)localize(n)}}).observe(document.body,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:['aria-label','title','placeholder','alt']});
  }
})();
