(()=>{'use strict';
const header=document.querySelector('#dd-header');if(!header)return;
const nav=header.querySelector('#dd-navigation'),toggle=header.querySelector('.dd-menu-toggle');if(!nav||!toggle)return;
const contacts=header.querySelector('.dd-contact-strip'),tools=header.querySelector('.dd-header-tools');tools.append(toggle);
const items=[...nav.children],primary=items.filter(e=>e.matches('.dd-group')),features=[...header.querySelectorAll('.dd-feature')],groups=[...primary,...features],flyouts=[...nav.querySelectorAll('.dd-flyout')],fine=matchMedia('(hover:hover) and (pointer:fine)'),inertState=new Map();
let compact=false,pointer='mouse',lastWidth=innerWidth,suppressFocus=false;const timers=new Map();
const backdrop=document.createElement('div');backdrop.className='dd-menu-backdrop';backdrop.hidden=true;backdrop.setAttribute('aria-hidden','true');document.body.appendChild(backdrop);
const trigger=g=>g.querySelector(':scope>a,:scope>button'),panel=g=>g.querySelector(':scope>.dd-panel,:scope>.dd-flyout-panel');
function cancel(g){clearTimeout(timers.get(g));timers.delete(g);}
function close(g){cancel(g);g.classList.remove('is-open');if(compact&&flyouts.includes(g))trigger(g).removeAttribute('aria-expanded');else trigger(g).setAttribute('aria-expanded','false');if(primary.includes(g))g.querySelectorAll('.dd-flyout').forEach(close);}
function syncOverlay(){const locked=header.classList.contains('menu-is-open')||header.classList.contains('feature-is-open');backdrop.hidden=!locked;if(locked){document.querySelectorAll('body>main,body>footer').forEach(e=>{if(!inertState.has(e))inertState.set(e,e.inert);e.inert=true;});}else{inertState.forEach((v,e)=>e.inert=v);inertState.clear();}}
function closeAll(restore=false){const feature=features.find(g=>g.classList.contains('is-open')),menu=header.classList.contains('menu-is-open');groups.forEach(close);flyouts.forEach(close);header.classList.remove('menu-is-open','feature-is-open');toggle.setAttribute('aria-expanded','false');toggle.textContent='Menu';syncOverlay();if(restore){suppressFocus=true;(feature?trigger(feature):menu?toggle:null)?.focus({preventScroll:true});queueMicrotask(()=>suppressFocus=false);}}
function position(){const root=document.documentElement,gutter=parseFloat(getComputedStyle(header).paddingLeft),width=Math.min(480,root.clientWidth-2*gutter);root.style.setProperty('--dd-header-bottom',Math.max(0,header.getBoundingClientRect().bottom)+'px');root.style.setProperty('--dd-menu-width',width+'px');root.style.setProperty('--dd-menu-left',Math.max(gutter,root.clientWidth-gutter-width)+'px');}
function place(g){if(compact&&primary.includes(g))return;const p=panel(g),r=trigger(g).getBoundingClientRect(),vw=document.documentElement.clientWidth;
 let width=g.matches('.dd-neighborhoods')?(vw>1100?720:vw>600?610:vw-32):g.matches('.dd-search')?246:g.matches('.dd-buyers')?252:272;
 // Anchor each dropdown to its own label; only constrain it at the viewport edge.
 const centered=g.matches('.dd-neighborhoods')&&vw>=1200,available=vw-16-Math.max(16,r.left);width=Math.min(width,vw-32);if(!centered&&(available>=220||g.matches('.dd-feature')))width=Math.min(width,Math.max(180,available));const desired=centered?r.left+r.width/2-width/2:r.left,left=Math.max(16,Math.min(desired,vw-width-16));
 p.style.setProperty('--dd-panel-left',left+'px');p.style.setProperty('--dd-panel-top',Math.max(0,r.bottom)+'px');p.style.setProperty('--dd-panel-width',width+'px');p.style.removeProperty('--dd-panel-height');}
function placeFlyout(g){if(compact)return;const p=panel(g),r=trigger(g).getBoundingClientRect(),parent=g.closest('.dd-panel').getBoundingClientRect(),vw=document.documentElement.clientWidth,width=Math.min(360,vw-32),height=Math.max(100,innerHeight-Math.max(12,parent.top)-16);
 let left=parent.right-1;if(left+width>vw-16)left=parent.left-width+1;left=Math.max(16,Math.min(left,vw-width-16));
 p.style.setProperty('--dd-panel-width',width+'px');p.style.setProperty('--dd-panel-height',height+'px');p.style.setProperty('--dd-panel-left',left+'px');
 const actual=Math.min(p.scrollHeight+2,height),top=Math.max(Math.max(12,parent.top),Math.min(r.top,innerHeight-actual-16));p.style.setProperty('--dd-panel-top',top+'px');}
function openGroup(g){cancel(g);if(g.classList.contains('is-open'))return;
 if(features.includes(g)){closeAll();if(compact||pointer==='touch'||!fine.matches)header.classList.add('feature-is-open');}
 else{groups.filter(x=>x!==g).forEach(close);header.classList.remove('feature-is-open');}
 g.classList.add('is-open');trigger(g).setAttribute('aria-expanded','true');if(!(compact&&primary.includes(g)))place(g);syncOverlay();}
function openFlyout(g){if(compact)return;flyouts.filter(x=>x!==g).forEach(close);cancel(g);g.classList.add('is-open');trigger(g).setAttribute('aria-expanded','true');placeFlyout(g);}
function openMenu(){if(!compact)return;closeAll();position();header.classList.add('menu-is-open');toggle.setAttribute('aria-expanded','true');toggle.textContent='Close';nav.scrollTop=0;syncOverlay();}
// Fit the utility composition and the navigation, with space beyond their text widths.
function layout(){
 const next=innerWidth<600;if(next!==compact)closeAll();compact=next;
 header.classList.toggle('is-compact',compact);header.classList.toggle('is-tablet',!compact&&innerWidth<1200);
 if(compact){if(contacts.parentElement!==nav)nav.append(contacts);}else if(contacts.parentElement!==header)header.insertBefore(contacts,nav);
 position();groups.filter(g=>g.classList.contains('is-open')).forEach(place);
 const rail=!compact&&nav.scrollWidth>nav.clientWidth+1;header.classList.toggle('has-nav-rail',rail);header.classList.toggle('nav-at-end',nav.scrollLeft+nav.clientWidth>=nav.scrollWidth-1);
 nav.setAttribute('aria-label',rail?'Main navigation — swipe or scroll horizontally for more links':'Main navigation');
}
// Keep parent destinations explicit in inline menus, and avoid a second nested accordion.
primary.forEach(g=>{const a=trigger(g),content=g.querySelector('.dd-panel-content');if(![...content.children].some(c=>c.matches('a')&&c.getAttribute('href')===a.getAttribute('href'))){const overview=a.cloneNode(true);overview.className='dd-parent-link';overview.removeAttribute('aria-haspopup');overview.removeAttribute('aria-expanded');content.prepend(overview);}});
const program=nav.querySelector('a[href$="first-time-homebuyer-programs.html"]');if(program){const link=program.cloneNode(true);link.className='dd-mobile-program';nav.querySelector('.dd-buyers>.dd-panel>.dd-panel-content').append(link);}
header.addEventListener('pointerdown',e=>pointer=e.pointerType);toggle.addEventListener('click',()=>header.classList.contains('menu-is-open')?closeAll(true):openMenu());
function bind(g,i,fly=false){const a=trigger(g),p=panel(g);p.id='dd-dropdown-'+i;a.setAttribute('aria-controls',p.id);a.setAttribute('aria-haspopup','true');a.setAttribute('aria-expanded','false');const open=()=>fly?openFlyout(g):openGroup(g);
 g.addEventListener('pointerenter',e=>{if(e.pointerType!=='touch'&&(!compact||features.includes(g)))open();});g.addEventListener('pointerleave',e=>{if(e.pointerType==='touch')return;timers.set(g,setTimeout(()=>{if(!g.matches(':hover')&&!g.contains(document.activeElement)){close(g);if(features.includes(g)){if(!features.some(x=>x.classList.contains('is-open')))header.classList.remove('feature-is-open');syncOverlay();}}},260));});p.addEventListener('pointerenter',()=>cancel(g));
 a.addEventListener('click',e=>{if(compact&&fly)return;if(compact&&primary.includes(g)){e.preventDefault();g.classList.contains('is-open')?close(g):open();return;}if(a.matches('button')){e.preventDefault();g.classList.contains('is-open')?closeAll(true):open();}else if((compact||pointer==='touch'||!fine.matches)&&!g.classList.contains('is-open')){e.preventDefault();open();}});
 a.addEventListener('keydown',e=>{if(e.key==='ArrowDown'||e.key===' '&&a.matches('a')){e.preventDefault();open();p.querySelector('a')?.focus();}});
 g.addEventListener('focusin',()=>{if(!suppressFocus&&pointer!=='touch'&&(!compact||features.includes(g))&&!g.classList.contains('is-open'))open();});
 g.addEventListener('focusout',()=>setTimeout(()=>{if(!g.contains(document.activeElement)&&!g.matches(':hover')&&(!compact||features.includes(g))){close(g);if(features.includes(g)){if(!features.some(x=>x.classList.contains('is-open')))header.classList.remove('feature-is-open');syncOverlay();}}},0));}
groups.forEach((g,i)=>bind(g,i));flyouts.forEach((g,i)=>bind(g,'buy-'+i,true));
features.forEach(g=>{const b=document.createElement('button');b.type='button';b.className='dd-feature-close';b.textContent='Close';b.setAttribute('aria-label','Close '+trigger(g).textContent.trim()+' menu');b.addEventListener('click',()=>closeAll(true));panel(g).prepend(b);});
items.filter(e=>e.matches('a')).forEach(a=>a.addEventListener('pointerenter',()=>{if(!compact)closeAll();}));
header.addEventListener('click',e=>{if(!e.defaultPrevented&&e.target.closest('.dd-panel a,#dd-navigation>a,.dd-contact-strip a'))closeAll();});backdrop.addEventListener('click',()=>closeAll(true));document.addEventListener('click',e=>{if(!header.contains(e.target))closeAll();});
document.addEventListener('keydown',e=>{pointer='keyboard';if(e.key==='Escape'){const f=flyouts.find(g=>g.classList.contains('is-open'));if(f&&!compact){close(f);suppressFocus=true;trigger(f).focus({preventScroll:true});queueMicrotask(()=>suppressFocus=false);return;}const g=groups.find(g=>g.classList.contains('is-open')),overlay=!backdrop.hidden;closeAll(overlay);if(!overlay&&g){suppressFocus=true;trigger(g).focus({preventScroll:true});queueMicrotask(()=>suppressFocus=false);}return;}
 if(e.key==='Tab'&&!backdrop.hidden){const active=features.find(g=>g.classList.contains('is-open')),els=active?[trigger(active),...panel(active).querySelectorAll('a[href],button')]:[toggle,...nav.querySelectorAll('a[href],button')];const visible=els.filter(el=>el.getClientRects().length&&!el.disabled);if(visible.length){e.preventDefault();const current=visible.indexOf(document.activeElement),next=current<0?(e.shiftKey?visible.length-1:0):(current+(e.shiftKey?-1:1)+visible.length)%visible.length;visible[next].focus({preventScroll:true});}}});
function reposition(){position();const active=groups.find(g=>g.classList.contains('is-open'));if(active&&!compact&&trigger(active).getBoundingClientRect().bottom<=0){closeAll();return;}groups.filter(g=>g.classList.contains('is-open')).forEach(place);flyouts.filter(g=>g.classList.contains('is-open')).forEach(placeFlyout);}
window.addEventListener('resize',()=>{if(innerWidth!==lastWidth){lastWidth=innerWidth;closeAll();layout();}else reposition();});window.addEventListener('scroll',reposition,{passive:true});window.addEventListener('pageshow',e=>{if(e.persisted)closeAll();layout();});document.querySelector('link[data-dommydom-navigation]')?.addEventListener('load',layout);document.fonts.ready.then(layout);new ResizeObserver(position).observe(header);
nav.addEventListener('scroll',()=>{header.classList.toggle('nav-at-end',nav.scrollLeft+nav.clientWidth>=nav.scrollWidth-1);if(!compact)groups.filter(g=>g.classList.contains('is-open')).forEach(place);},{passive:true});
const current=new URL(location.href);header.querySelectorAll('a[href]').forEach(a=>{const url=new URL(a.href);if(url.pathname===current.pathname&&!url.hash)a.setAttribute('aria-current','page');});layout();
})();
