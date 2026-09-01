
(()=>{
  // Image fallback: if any remote/local image fails, show an actual local portfolio photo instead of alt text.
  const fallback='assets/projects/sun-lit-modern/photo-48.jpg';
  document.querySelectorAll('img').forEach(img=>{
    img.addEventListener('error',()=>{
      if(img.dataset.fallbackDone)return;
      img.dataset.fallbackDone='1';
      img.src=fallback;
    });
  });

  // Mobile before/after slider: explicit pointer/touch support in addition to native range input.
  const range=document.querySelector('.compareFrame input[type=range]');
  if(range){
    const frame=range.closest('.compareFrame');
    const apply=v=>{
      const n=Math.max(+range.min||0,Math.min(+range.max||100,v)); range.value=n;
      const pct=(n-(+range.min||0))/((+range.max||100)-(+range.min||0))*100;
      const top=frame.querySelector('.compareTop'), handle=frame.querySelector('.compareHandle');
      if(top) top.style.right=(100-pct)+'%'; if(handle) handle.style.left=pct+'%';
    };
    const setFromX=x=>{const r=frame.getBoundingClientRect(); const pct=(x-r.left)/r.width; apply((+range.min||0)+pct*((+range.max||100)-(+range.min||0)));};
    range.addEventListener('pointerdown',e=>{range.setPointerCapture?.(e.pointerId);setFromX(e.clientX)});
    range.addEventListener('pointermove',e=>{if(e.buttons||e.pointerType==='touch')setFromX(e.clientX)});
    range.addEventListener('input',()=>apply(+range.value));
    apply(+range.value);
  }
})();
