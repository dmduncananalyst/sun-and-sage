/* Optional, bounded document prefetch. Navigation never waits for downloads. */
(() => {
  'use strict';
  const connection = navigator.connection;
  if (connection && (connection.saveData || /(^|-)2g$/.test(connection.effectiveType))) return;
  const warmed = new Set();
  let timer;
  function warm(anchor) {
    if (!anchor || anchor.target === '_blank' || anchor.hasAttribute('download') || anchor.hasAttribute('data-chat')) return;
    let url;
    try { url = new URL(anchor.href, location.href); } catch (_) { return; }
    if (url.origin !== location.origin || url.hash || url.href === location.href ||
        !(/\.html$/.test(url.pathname) || url.pathname.endsWith('/')) ||
        warmed.has(url.href) || warmed.size >= 4) return;
    warmed.add(url.href);
    const link = document.createElement('link');
    link.rel = 'prefetch';
    link.as = 'document';
    link.href = url.href;
    document.head.append(link);
  }
  document.addEventListener('pointerover', event => {
    if (event.pointerType !== 'mouse') return;
    clearTimeout(timer);
    const anchor = event.target.closest('a[href]');
    timer = setTimeout(() => warm(anchor), 150);
  }, {passive: true});
  document.addEventListener('pointerout', () => clearTimeout(timer), {passive: true});
  document.addEventListener('focusin', event => warm(event.target.closest('a[href]')));
})();
