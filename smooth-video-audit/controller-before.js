(() => {
  'use strict';
  const video = document.getElementById('home-introduction-video');
  const hero = video?.closest('.videoHero');
  if (!hero) return;
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  // About .55s of the original footage faces the camera. This short opening
  // beat makes that shot last about one second after the doors finish opening.
  const revealBeat = reducedMotion ? 0 : 450;
  let opening = false;
  let finished = false;
  let holdingOpeningShot = false;
  let mediaFailed = false;
  document.documentElement.classList.remove('preview-loading');
  document.documentElement.style.visibility = 'visible';
  video.defaultMuted = true;
  video.muted = true;
  video.loop = true;
  video.playsInline = true;
  // The controller starts playback after the reveal; native autoplay must not
  // spend the opening shot behind closed doors while scripts/styles load.
  video.autoplay = false;
  video.pause();
  const playButton = document.createElement('button');
  playButton.type = 'button';
  playButton.textContent = 'Play video';
  playButton.setAttribute('aria-label', 'Play Dominique’s introduction video');
  playButton.hidden = true;
  playButton.style.cssText = 'position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:20;padding:14px 22px;border:1px solid #fff;background:#41372b;color:#fff;font:16px Arial,sans-serif;cursor:pointer;';
  hero.append(playButton);
  function showPlayButton() {
    if ((!finished || holdingOpeningShot) && !video.error && !mediaFailed) return;
    if (!video.paused && video.readyState >= 2) return;
    playButton.hidden = false;
    video.controls = true;
    if (video.error || mediaFailed) playButton.textContent = 'Open video';
  }
  playButton.addEventListener('click', () => {
    if (video.error || mediaFailed) {
      const source = video.currentSrc || video.querySelector('source:not([media])')?.src;
      if (source) window.open(source, '_blank', 'noopener');
    } else requestPlayback();
  });

  function finish() {
    if (finished) return;
    finished = true;
    holdingOpeningShot = true;
    hero.classList.add('ss23-doors-finished');
    setTimeout(() => {
      holdingOpeningShot = false;
      requestPlayback();
    }, revealBeat);
  }
  function reveal() {
    if (opening || video.seeking || (video.readyState < 2 && !video.error && !mediaFailed)) return;
    if (video.currentTime > .05 && !video.error) {
      video.currentTime = 0;
      return; // The seeked event resumes preparation at the opening shot.
    }
    opening = true;
    video.pause();
    hero.classList.add('ss23-opening');
    if (reducedMotion) finish();
    else setTimeout(finish, 1250); // Fallback if animationend is unavailable.
  }
  function requestPlayback() {
    // Source failures may occur before this deferred controller attaches.
    if (video.networkState === video.NETWORK_NO_SOURCE) mediaFailed = true;
    if (!finished) {
      reveal();
      if (mediaFailed) showPlayButton();
      return;
    }
    if (holdingOpeningShot || document.hidden || !video.paused || video.error || mediaFailed) return;
    try {
      const playing = video.play();
      playing?.catch(() => {
        if (video.paused) showPlayButton();
      });
    } catch (_) {
      showPlayButton();
    }
  }
  video.addEventListener('playing', () => {
    video.controls = false;
    playButton.hidden = true;
  });
  video.addEventListener('loadeddata', requestPlayback);
  video.addEventListener('canplay', requestPlayback);
  video.addEventListener('seeked', requestPlayback);
  video.addEventListener('pause', () => {
    if (!video.controls) requestPlayback();
  });
  function mediaError() {
    mediaFailed = true;
    reveal();
    showPlayButton();
  }
  video.addEventListener('error', mediaError);
  // With multiple sources, browsers can report failures on each source rather
  // than on the video. Reveal the existing poster if every eligible source fails.
  const failedSources = new Set();
  const sources = [...video.querySelectorAll('source[src]')];
  sources.forEach(source => source.addEventListener('error', () => {
    failedSources.add(source);
    const eligible = sources.filter(item => !item.media || matchMedia(item.media).matches);
    if (eligible.every(item => failedSources.has(item))) mediaError();
  }));
  document.addEventListener('visibilitychange', requestPlayback);
  window.addEventListener('pageshow', requestPlayback);
  document.addEventListener('pointerdown', requestPlayback, {passive: true});
  document.addEventListener('keydown', requestPlayback);
  hero.querySelector('.doors > div:last-child')?.addEventListener('animationend', event => {
    if (event.animationName === 'rightOpen') finish();
  });

  // Prepare the decoded opening shot without hiding or delaying the page.
  requestPlayback();
  setTimeout(requestPlayback, 1000);
  setTimeout(showPlayButton, 1800);
})();
