(() => {
  'use strict';
  const video = document.getElementById('home-introduction-video');
  const hero = video?.closest('.videoHero');
  if (!hero) return;
  let opening = false;
  let finished = false;
  let started = false;
  let playPending = false;
  let needsGesture = false;
  let mediaFailed = false;
  const videoCandidates = [...new Set([
    ...[...video.querySelectorAll('source[src]')].filter(s => !s.media || matchMedia(s.media).matches).map(s => s.src),
    new URL('assets/videos/home-introduction.mp4', document.baseURI).href
  ])];
  let candidateIndex = 0;
  function loadCandidate() {
    mediaFailed = false;
    started = false;
    playPending = false;
    needsGesture = false;
    video.src = videoCandidates[candidateIndex];
    video.load();
    requestPlayback();
  }
  document.documentElement.classList.remove('preview-loading');
  document.documentElement.style.visibility = 'visible';
  video.defaultMuted = true;
  video.muted = true;
  video.loop = true;
  video.playsInline = true;
  // A single controller-owned start coordinates the doors with actual playback.
  video.autoplay = false;
  const playButton = document.createElement('button');
  playButton.type = 'button';
  playButton.textContent = 'Play video';
  playButton.setAttribute('aria-label', 'Play Dominique’s introduction video');
  playButton.hidden = true;
  playButton.style.cssText = 'position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:20;padding:14px 22px;border:1px solid #fff;background:#41372b;color:#fff;font:16px Arial,sans-serif;cursor:pointer;';
  hero.append(playButton);

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
    else setTimeout(finish, 1250); // Retained animation-event fallback only.
  }
  function showPlayButton() {
    playButton.hidden = false;
    video.controls = true;
    playButton.textContent = 'Play video';
    // Keep the existing poster and manual control accessible if autoplay fails.
    reveal();
  }
  function mediaError() {
    if (candidateIndex < videoCandidates.length - 1) {
      candidateIndex++;
      loadCandidate();
      return;
    }
    mediaFailed = true;
    showPlayButton();
  }
  function requestPlayback(userGesture = false) {
    if (video.error || mediaFailed) {
      mediaError();
      return;
    }
    if (started || playPending || (needsGesture && !userGesture)) return;
    if (!video.paused) {
      started = true;
      reveal();
      return;
    }
    playPending = true;
    const rejected = () => {
      playPending = false;
      needsGesture = true;
      showPlayButton();
    };
    try {
      const playing = video.play();
      if (playing?.then) playing.then(() => { playPending = false; }, rejected);
      else playPending = false;
    } catch (_) {
      rejected();
    }
  }
  playButton.addEventListener('click', () => {
    if (video.error || mediaFailed) {
      candidateIndex = 0;
      loadCandidate();
    } else requestPlayback(true);
  });
  video.addEventListener('playing', () => {
    started = true;
    playPending = false;
    needsGesture = false;
    video.controls = false;
    playButton.hidden = true;
    reveal();
  });
  video.addEventListener('error', mediaError);
  hero.querySelector('.doors > div:last-child')?.addEventListener('animationend', event => {
    if (event.animationName === 'rightOpen') finish();
  });
  // No pause, seek, reveal hold, playback-rate change, or automatic restart.
  window.addEventListener('pageshow', event => {
    if (event.persisted && video.paused) { started = false; requestPlayback(); }
  });
  loadCandidate();
})();
