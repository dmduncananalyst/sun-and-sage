(()=>{'use strict';
 const links=[...document.querySelectorAll('[data-ss23-lightbox]')];if(!links.length)return;
 const dialog=document.createElement('dialog');dialog.className='ss23-lightbox';dialog.setAttribute('aria-label','Project photograph viewer');
 dialog.innerHTML='<button type="button" class="ss23-lightbox-close" aria-label="Close photograph viewer">Close</button><button type="button" class="ss23-lightbox-prev" aria-label="Previous photograph">‹</button><img alt=""><button type="button" class="ss23-lightbox-next" aria-label="Next photograph">›</button><div class="ss23-lightbox-count" aria-live="polite"></div>';
 document.body.append(dialog);
 const img=dialog.querySelector('img'), closeBtn=dialog.querySelector('.ss23-lightbox-close'), prevBtn=dialog.querySelector('.ss23-lightbox-prev'), nextBtn=dialog.querySelector('.ss23-lightbox-next'), count=dialog.querySelector('.ss23-lightbox-count');
 let group=[],current=0,touchX=null;
 function buildGroup(a){const gallery=a.closest('[data-job-gallery]')||a.closest('.jobPanel')||document;group=[...gallery.querySelectorAll('[data-ss23-lightbox]')];current=Math.max(0,group.indexOf(a));}
 function show(i){if(!group.length)return;current=(i+group.length)%group.length;const a=group[current];img.src=a.href;img.alt=a.querySelector('img')?.alt||'Project photograph';count.textContent=(current+1)+' / '+group.length;}
 function close(){dialog.close();img.removeAttribute('src');}
 closeBtn.addEventListener('click',close);prevBtn.addEventListener('click',()=>show(current-1));nextBtn.addEventListener('click',()=>show(current+1));
 dialog.addEventListener('click',e=>{if(e.target===dialog)close()});
 links.forEach(a=>a.addEventListener('click',e=>{e.preventDefault();buildGroup(a);show(current);dialog.showModal()}));
 document.addEventListener('keydown',e=>{if(!dialog.open)return;if(e.key==='ArrowLeft'){e.preventDefault();show(current-1)}else if(e.key==='ArrowRight'){e.preventDefault();show(current+1)}else if(e.key==='Escape'){close()}});
 dialog.addEventListener('touchstart',e=>{touchX=e.changedTouches[0]?.clientX??null},{passive:true});
 dialog.addEventListener('touchend',e=>{if(touchX==null)return;const dx=(e.changedTouches[0]?.clientX??touchX)-touchX;touchX=null;if(Math.abs(dx)>45)show(current+(dx<0?1:-1))},{passive:true});
})();