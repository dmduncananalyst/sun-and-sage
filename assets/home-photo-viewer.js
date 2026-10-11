(()=>{
 const dialog=document.querySelector('.ddn-photo-viewer');
 if(!dialog)return;
 const enlarged=dialog.querySelector('img'),caption=dialog.querySelector('.ddn-photo-viewer-caption');
 let trigger,previousOverflow='';
 document.querySelectorAll('.ddn-photo-open').forEach(button=>button.addEventListener('click',()=>{
  const photo=button.querySelector('img');trigger=button;
  enlarged.src=photo.currentSrc||photo.src;enlarged.alt=photo.alt;
  caption.textContent=button.closest('.ss22-service-card').querySelector('h3').textContent;
  previousOverflow=document.body.style.overflow;document.body.style.overflow='hidden';dialog.showModal();
  dialog.querySelector('.ddn-photo-close').focus();
 }));
 dialog.querySelector('.ddn-photo-close').addEventListener('click',()=>dialog.close());
 dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close()});
 dialog.addEventListener('close',()=>{document.body.style.overflow=previousOverflow;if(trigger)trigger.focus()});
})();
