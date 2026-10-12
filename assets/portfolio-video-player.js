(()=>{
 const links=[...document.querySelectorAll('a.portfolioVideoThumb')];
 if(!links.length)return;
 const dialog=document.createElement('dialog');dialog.id='portfolioVideoDialog';dialog.setAttribute('aria-label','Portfolio video player');
 const close=document.createElement('button');close.type='button';close.className='portfolioVideoClose';close.setAttribute('aria-label','Close video');close.textContent='×';
 const player=document.createElement('video');player.controls=true;player.playsInline=true;player.preload='metadata';
 dialog.append(close,player);document.body.append(dialog);
 let trigger=null;
 function stop(){player.pause();player.removeAttribute('src');player.load();if(trigger)trigger.focus();}
 close.addEventListener('click',()=>dialog.close());
 dialog.addEventListener('close',stop);
 dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
 for(const link of links)link.addEventListener('click',e=>{
  if(typeof dialog.showModal!=='function')return;
  e.preventDefault();trigger=link;player.src=link.href;player.poster=link.querySelector('img').src;player.setAttribute('aria-label',link.getAttribute('aria-label'));dialog.showModal();player.play().catch(()=>{});
 });
})();
