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
  // Size the closed selector to its selected label, keeping the chevron nearby.
  if(typeof getComputedStyle==='function'){
    const measure=document.createElement('canvas').getContext?.('2d');
    if(measure){
      const sizeSelector=()=>{measure.font=getComputedStyle(select).font;select.style.setProperty('--dd-language-width',Math.ceil(measure.measureText(select.selectedOptions[0].textContent).width)+20+'px')};
      sizeSelector();window.addEventListener('resize',()=>requestAnimationFrame(sizeSelector));document.fonts?.ready.then(()=>requestAnimationFrame(sizeSelector));
    }
  }
  if(toolbar&&!toolbar.contains(select)){const search=toolbar.querySelector('.dd-search');if(search)search.insertAdjacentElement('afterend',select.parentElement);else toolbar.append(select.parentElement)}
  function destination(code){
    const root=new URL(cfg.rootPrefix||('../'.repeat(cfg.path.split('/').length-1+(cfg.language==='en'?0:1))||'./'),location.href);
    const path=(code==='en'?'':code+'/')+(cfg.path==='index.html'&&location.protocol!=='file:'?'':cfg.path);
    return new URL(path||'./',root).href+location.search+location.hash;
  }
  select.addEventListener('change',()=>{try{localStorage.setItem('dommydom-language',select.value)}catch{}location.assign(destination(select.value))});
  // The open list has its own width, independent of the compact closed label.
  // Native select popups in embedded browsers can clip the other language names.
  if(typeof HTMLSelectElement!=='undefined'&&select instanceof HTMLSelectElement){
    const menu=document.createElement('div');menu.id='dd-language-menu';menu.hidden=true;
    menu.setAttribute('role','listbox');menu.setAttribute('aria-label',select.getAttribute('aria-label'));
    menu.setAttribute('translate','no');document.body.append(menu);
    select.setAttribute('aria-controls',menu.id);select.setAttribute('aria-expanded','false');
    const options=[];
    function closeMenu(restore=false){menu.hidden=true;select.setAttribute('aria-expanded','false');if(restore)select.focus({preventScroll:true})}
    for(const [code,name] of Object.entries(cfg.languages)){
      const option=document.createElement('button');option.type='button';option.tabIndex=-1;
      option.textContent=name;option.dataset.language=code;option.setAttribute('role','option');
      option.setAttribute('lang',code);option.setAttribute('dir','auto');
      option.setAttribute('aria-selected',String(code===cfg.language));
      option.addEventListener('click',()=>{closeMenu();select.value=code;select.dispatchEvent(new Event('change',{bubbles:true}))});
      menu.append(option);options.push(option);
    }
    function positionMenu(){
      const anchor=select.getBoundingClientRect(),vw=document.documentElement.clientWidth,vh=innerHeight;
      menu.style.maxHeight=(vh-16)+'px';
      const width=menu.getBoundingClientRect().width,height=menu.scrollHeight+2;
      const below=vh-anchor.bottom-8,above=anchor.top-8,down=below>=height||below>=above;
      const space=Math.max(48,down?below:above);
      menu.style.maxHeight=space+'px';
      menu.style.left=Math.max(8,Math.min(anchor.left,vw-width-8))+'px';
      menu.style.top=(down?anchor.bottom+4:Math.max(8,anchor.top-Math.min(height,space)-4))+'px';
    }
    function openMenu(){menu.hidden=false;select.setAttribute('aria-expanded','true');positionMenu();(options.find(o=>o.dataset.language===select.value)||options[0]).focus({preventScroll:true})}
    select.addEventListener('pointerdown',event=>{if(event.button!==0)return;event.preventDefault();menu.hidden?openMenu():closeMenu(true)});
    select.addEventListener('click',event=>event.preventDefault());
    select.addEventListener('keydown',event=>{if(['ArrowDown','ArrowUp',' ','Enter'].includes(event.key)){event.preventDefault();openMenu()}else if(event.key==='Escape')closeMenu(true)});
    menu.addEventListener('keydown',event=>{
      const index=options.indexOf(document.activeElement);
      if(['ArrowDown','ArrowUp','Home','End'].includes(event.key)){
        event.preventDefault();const next=event.key==='Home'?0:event.key==='End'?options.length-1:(index+(event.key==='ArrowDown'?1:-1)+options.length)%options.length;
        options[next].focus();
      }else if(event.key==='Escape'){event.preventDefault();closeMenu(true)}
      else if(event.key==='Tab')closeMenu(true);
    });
    document.addEventListener('pointerdown',event=>{if(!menu.hidden&&!menu.contains(event.target)&&event.target!==select)closeMenu()});
    window.addEventListener('resize',()=>{if(!menu.hidden)requestAnimationFrame(positionMenu)});
    window.addEventListener('scroll',()=>closeMenu(),{passive:true});
  }
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
