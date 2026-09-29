/* Mobile-only framing for the existing landscape introduction video.
   Keep its subject in view while filling the portrait hero. No scroll commands,
   resizing on playback, or changes to the video timeline/desktop presentation. */
(() => {
  'use strict';
  const video = document.getElementById('home-introduction-video');
  if (!video) return;
  const mobile = window.matchMedia('(max-width:760px), (max-width:1023px) and (orientation:landscape) and (pointer:coarse)');
  const focus = [[0, .365], [2, .365], [4, .50], [6, .55], [10.667, .55]];
  let frame = 0;

  function updateFraming() {
    if (!mobile.matches) {
      video.style.removeProperty('--ss36-video-focus');
      return;
    }
    if (!video.videoWidth || !video.videoHeight || !video.clientHeight) return;
    const visibleFraction = video.clientWidth / (video.clientHeight * video.videoWidth / video.videoHeight);
    if (visibleFraction >= 1) {
      video.style.setProperty('--ss36-video-focus', '50%');
      return;
    }
    const time = video.currentTime;
    let target = focus[focus.length - 1][1];
    for (let i = 1; i < focus.length; i++) {
      if (time <= focus[i][0]) {
        const [start, from] = focus[i - 1];
        const [end, to] = focus[i];
        const progress = Math.max(0, Math.min(1, (time - start) / (end - start)));
        const eased = progress * progress * (3 - 2 * progress);
        target = from + (to - from) * eased;
        break;
      }
    }
    const position = 100 * (target - visibleFraction / 2) / (1 - visibleFraction);
    video.style.setProperty('--ss36-video-focus', Math.max(0, Math.min(100, position)).toFixed(3) + '%');
  }

  function tick() {
    frame = 0;
    updateFraming();
    if (mobile.matches && !video.paused && !document.hidden) frame = requestAnimationFrame(tick);
  }
  function refresh() {
    if (frame) cancelAnimationFrame(frame);
    frame = 0;
    tick();
  }
  ['loadedmetadata', 'playing', 'pause', 'seeked'].forEach(event => video.addEventListener(event, refresh));
  window.addEventListener('resize', refresh, {passive:true});
  document.addEventListener('visibilitychange', refresh);
  if (mobile.addEventListener) mobile.addEventListener('change', refresh);
  else mobile.addListener(refresh);
  refresh();
})();
