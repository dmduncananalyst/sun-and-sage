(()=>{'use strict';
const header=document.querySelector('#ss22-header');if(!header)return;
const nav=header.querySelector('.ss22-nav'),toggle=header.querySelector('.ss22-menu-toggle'),groups=[...nav.querySelectorAll('.ss22-group')];
const desktop=()=>matchMedia('(min-width:1280px)').matches;let closeTimer,suppressFocus=false;
function closeGroup(group){group.classList.remove('is-open');group.querySelectorAll(':scope>button').forEach(b=>b.setAttribute('aria-expanded','false'))}
function place(group){if(!desktop())return;const content=group.querySelector('.ss22-panel-content'),anchor=group.querySelector(':scope>a,:scope>button'),width=content.getBoundingClientRect().width;const left=Math.max(24,Math.min(anchor.getBoundingClientRect().left,document.documentElement.clientWidth-width-32));content.style.setProperty('--panel-start',left+'px')}
function open(group){clearTimeout(closeTimer);groups.forEach(g=>{if(g!==group)closeGroup(g)});group.classList.add('is-open');group.querySelectorAll(':scope>button').forEach(b=>b.setAttribute('aria-expanded','true'));place(group)}
function close(){clearTimeout(closeTimer);groups.forEach(closeGroup)}
function closeMobile(){header.classList.remove('menu-is-open');toggle.setAttribute('aria-expanded','false');toggle.textContent='Menu'}
toggle.addEventListener('click',()=>{const active=!header.classList.contains('menu-is-open');close();header.classList.toggle('menu-is-open',active);toggle.setAttribute('aria-expanded',String(active));toggle.textContent=active?'Close':'Menu'});
groups.forEach((g,i)=>{const panel=g.querySelector('.ss22-panel');panel.id='ss22-dropdown-'+i;g.querySelectorAll(':scope>button').forEach(b=>{b.setAttribute('aria-controls',panel.id);b.addEventListener('click',()=>g.classList.contains('is-open')?closeGroup(g):open(g))});g.addEventListener('pointerenter',e=>{if(desktop()&&e.pointerType!=='touch')open(g)});g.addEventListener('pointerleave',e=>{if(desktop()&&e.pointerType!=='touch')closeTimer=setTimeout(()=>{if(!g.matches(':hover')&&!g.contains(document.activeElement))closeGroup(g)},320)});panel.addEventListener('pointerenter',()=>clearTimeout(closeTimer));g.addEventListener('focusin',()=>{if(desktop()&&!suppressFocus)open(g)});g.addEventListener('focusout',()=>setTimeout(()=>{if(desktop()&&!g.contains(document.activeElement)&&!g.matches(':hover'))closeGroup(g)},0))});
nav.querySelectorAll(':scope>a').forEach(a=>a.addEventListener('pointerenter',()=>{if(desktop())close()}));
document.addEventListener('click',e=>{if(!header.contains(e.target)){close();closeMobile()}});
document.addEventListener('keydown',e=>{if(e.key!=='Escape')return;const group=groups.find(g=>g.contains(document.activeElement));close();closeMobile();suppressFocus=true;(desktop()?group?.querySelector(':scope>button,:scope>a'):toggle)?.focus();queueMicrotask(()=>suppressFocus=false)});
window.addEventListener('resize',()=>{close();closeMobile();document.documentElement.style.setProperty('--ss-header-height',header.offsetHeight+'px')});
document.documentElement.style.setProperty('--ss-header-height',header.offsetHeight+'px');
const current=(location.pathname.split('/').pop()||'index.html');nav.querySelectorAll('a[href]').forEach(a=>{if(a.getAttribute('href').split('/').pop()===current)a.setAttribute('aria-current','page')});

/* v34: mobile Life Changes uses its label, not a separate Open button. */
const mobileLifeQuery=matchMedia('(max-width:1279px)');
const lifeGroup=groups.find(g=>{const a=g.querySelector(':scope>a');return a&&/life-changes\.html$/.test(a.getAttribute('href')||'')});
if(lifeGroup){
 const label=lifeGroup.querySelector(':scope>a'),panel=lifeGroup.querySelector('.ss22-panel');
 const syncLife=()=>{
   if(mobileLifeQuery.matches){label.setAttribute('role','button');label.setAttribute('aria-controls',panel.id);label.setAttribute('aria-expanded',String(lifeGroup.classList.contains('is-open')))}
   else{label.removeAttribute('role');label.removeAttribute('aria-controls');label.removeAttribute('aria-expanded')}
 };
 label.addEventListener('click',e=>{if(!mobileLifeQuery.matches)return;e.preventDefault();lifeGroup.classList.contains('is-open')?closeGroup(lifeGroup):open(lifeGroup);syncLife()});
 label.addEventListener('keydown',e=>{if(mobileLifeQuery.matches&&e.key===' '){e.preventDefault();label.click()}});
 new MutationObserver(syncLife).observe(lifeGroup,{attributes:true,attributeFilter:['class']});
 mobileLifeQuery.addEventListener('change',syncLife);syncLife();
}
})();
