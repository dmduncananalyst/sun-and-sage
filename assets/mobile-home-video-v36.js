/* v52: steady mobile framing. Keep Dominique fully visible without per-frame panning/jumps. */
(() => {
  'use strict';
  const video = document.getElementById('home-introduction-video');
  if (!video) return;
  const mobile = window.matchMedia('(max-width:760px), (max-width:1023px) and (orientation:landscape) and (pointer:coarse)');
  function apply() {
    if (mobile.matches) video.style.setProperty('--ss36-video-focus', '34%');
    else video.style.removeProperty('--ss36-video-focus');
  }
  window.addEventListener('resize', apply, {passive:true});
  if (mobile.addEventListener) mobile.addEventListener('change', apply); else mobile.addListener(apply);
  apply();
})();
