(()=>{'use strict';
const header=document.querySelector('.ss-header');if(!header)return;
const menu=header.querySelector('.ss-menu-toggle'),groups=[...header.querySelectorAll('.ss-nav-group')];
const desktop=()=>matchMedia('(min-width:1181px)').matches;let suppressFocus=false;
function closeGroup(g){g.classList.remove('ss-open');g.querySelectorAll(':scope>button').forEach(b=>b.setAttribute('aria-expanded','false'))}
function openGroup(g){groups.forEach(x=>{if(x!==g)closeGroup(x)});g.classList.add('ss-open');g.querySelectorAll(':scope>button').forEach(b=>b.setAttribute('aria-expanded','true'))}
function closeAll(){groups.forEach(closeGroup);header.classList.remove('ss-menu-open');menu.setAttribute('aria-expanded','false');menu.textContent='Menu'}
menu.addEventListener('click',()=>{const open=!header.classList.contains('ss-menu-open');closeAll();header.classList.toggle('ss-menu-open',open);menu.setAttribute('aria-expanded',String(open));menu.textContent=open?'Close':'Menu'});
groups.forEach((g,i)=>{
 const dropdown=g.querySelector('.ss-dropdown');dropdown.id='ss-menu-'+i;
 g.querySelectorAll(':scope>button').forEach(btn=>{btn.setAttribute('aria-controls',dropdown.id);btn.addEventListener('click',()=>{if(g.classList.contains('ss-open'))closeGroup(g);else openGroup(g)})});
 g.addEventListener('pointerenter',e=>{if(desktop()&&e.pointerType!=='touch')openGroup(g)});
 g.addEventListener('pointerleave',e=>{if(desktop()&&e.pointerType!=='touch'&&!g.contains(document.activeElement))closeGroup(g)});
 g.addEventListener('focusin',()=>{if(desktop()&&!suppressFocus)openGroup(g)});
 g.addEventListener('focusout',()=>setTimeout(()=>{if(desktop()&&!g.contains(document.activeElement)&&!g.matches(':hover'))closeGroup(g)},0));
});
document.addEventListener('click',e=>{if(!header.contains(e.target))closeAll()});
document.addEventListener('keydown',e=>{if(e.key!=='Escape')return;const g=groups.find(x=>x.contains(document.activeElement));closeAll();suppressFocus=true;if(g&&desktop())g.querySelector(':scope>button,:scope>a')?.focus();else if(!desktop())menu.focus();queueMicrotask(()=>suppressFocus=false)});
function size(){groups.forEach(g=>g.querySelector('.ss-dropdown').style.setProperty('--ss-dropdown-space',Math.max(0,document.documentElement.clientWidth-g.getBoundingClientRect().left-16)+'px'))}
size();window.addEventListener('resize',()=>{closeAll();size()});document.fonts?.ready.then(size);
const current=location.pathname.split('/').pop()||'index.html';header.querySelectorAll('a[href]').forEach(a=>{if(a.getAttribute('href').split('/').pop()===current)a.setAttribute('aria-current','page')});
})();
