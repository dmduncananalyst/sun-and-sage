/* Measure the retained current header; door dimensions are the uploaded ZIP's CSS. */
(()=>{const header=document.getElementById('ss22-header');if(!header)return;const update=()=>document.documentElement.style.setProperty('--ss-header-height',header.getBoundingClientRect().height+'px');update();new ResizeObserver(update).observe(header);})();
