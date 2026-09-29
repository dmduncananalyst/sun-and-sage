(()=>{'use strict';
 const links=[...document.querySelectorAll('[data-ss23-lightbox]')];if(!links.length)return;
 const dialog=document.createElement('dialog');dialog.className='ss23-lightbox';dialog.setAttribute('aria-label','Project photograph');
 dialog.innerHTML='<button type="button" aria-label="Close photograph">Close</button><img alt="">';document.body.append(dialog);
 const close=()=>dialog.close();dialog.querySelector('button').addEventListener('click',close);dialog.addEventListener('click',e=>{if(e.target===dialog)close()});
 links.forEach(a=>a.addEventListener('click',e=>{e.preventDefault();const image=dialog.querySelector('img');image.src=a.href;image.alt=a.querySelector('img').alt;dialog.showModal()}));
})();
