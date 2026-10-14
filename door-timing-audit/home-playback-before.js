(() => {
  'use strict';
  const video = document.getElementById('home-introduction-video');
  const hero = video?.closest('.videoHero');
  if (!hero) return;
  let opening = false;
  let finished = false;
  document.documentElement.classList.remove('preview-loading');
  document.documentElement.style.visibility = 'visible';
  video.defaultMuted = true;
  video.muted = true;
  video.loop = true;
  video.playsInline = true;
  video.autoplay = true;
  const playButton = document.createElement('button');
  playButton.type = 'button';
  playButton.textContent = 'Play video';
  playButton.setAttribute('aria-label', 'Play Dominique’s introduction video');
  playButton.hidden = true;
  playButton.style.cssText = 'position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:20;padding:14px 22px;border:1px solid #fff;background:#41372b;color:#fff;font:16px Arial,sans-serif;cursor:pointer;';
  hero.append(playButton);
  function showPlayButton() {
    if (!video.paused && video.readyState >= 2) return;
    playButton.hidden = false;
    video.controls = true;
    if (video.error) playButton.textContent = 'Open video';
  }
  playButton.addEventListener('click', () => {
    if (video.error) {
      const source = video.currentSrc || video.querySelector('source:not([media])')?.src;
      if (source) window.open(source, '_blank', 'noopener');
    } else requestPlayback();
  });

  function finish() {
    if (finished) return;
    finished = true;
    hero.classList.add('ss23-doors-finished');
  }
  function reveal() {
    if (opening) return;
    opening = true;
    hero.classList.add('ss23-opening');
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) finish();
    else setTimeout(finish, 1250);
  }
  function requestPlayback() {
    if (!video.paused || video.error) return;
    try {
      const playing = video.play();
      playing?.catch(() => {
        // A browser that requires a user gesture still needs a working Play button.
        if (video.paused) showPlayButton();
      });
    } catch (_) {
      showPlayButton();
    }
  }
  video.addEventListener('playing', () => {
    video.controls = false;
    playButton.hidden = true;
    reveal();
  });
  video.addEventListener('loadeddata', requestPlayback);
  video.addEventListener('canplay', requestPlayback);
  video.addEventListener('pause', () => {
    if (!video.controls) requestPlayback();
  });
  video.addEventListener('error', showPlayButton);
  document.addEventListener('visibilitychange', requestPlayback);
  window.addEventListener('pageshow', requestPlayback);
  // Retry within a real gesture when browser autoplay policy blocked the first attempt.
  document.addEventListener('pointerdown', requestPlayback, {passive: true});
  document.addEventListener('keydown', requestPlayback);
  hero.querySelector('.doors > div:last-child')?.addEventListener('animationend', event => {
    if (event.animationName === 'rightOpen') finish();
  });

  // Start now. Reloading the media here would abort the native autoplay request.
  requestPlayback();
  // Door timing is independent of buffering and an unresolved play promise.
  setTimeout(reveal, 150);
  setTimeout(requestPlayback, 1000);
  // Embedded previews may leave play() pending without rejecting it.
  setTimeout(showPlayButton, 1800);
})();
