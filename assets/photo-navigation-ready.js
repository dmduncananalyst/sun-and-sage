/* Warm the next page's first photos without hiding or covering either page. */
(() => {
  'use strict';
  const pages = new Map();
  const heldImages = [];
  const eligible = anchor => {
    if (!anchor || anchor.target === '_blank' || anchor.hasAttribute('download') || anchor.hasAttribute('data-chat')) return null;
    let url;
    try { url = new URL(anchor.href, location.href); } catch (_) { return null; }
    if (url.origin !== location.origin || url.hash || url.href === location.href || !(/\.html$/.test(url.pathname) || url.pathname.endsWith('/'))) return null;
    return url;
  };
  const warm = (url, urgent = false) => {
    if (pages.has(url.href)) return pages.get(url.href);
    const job = fetch(url.href, {credentials: 'same-origin', cache: 'default'})
      .then(response => { if (!response.ok) throw new Error('Page unavailable'); return response.text(); })
      .then(markup => {
        const doc = new DOMParser().parseFromString(markup, 'text/html');
        const base = doc.querySelector('base[href]');
        const baseURL = base ? new URL(base.getAttribute('href'), url.href) : url;
        const cards = [...doc.querySelectorAll('.loanHubItem img[src], [class*="card"] img[src], [class*="Card"] img[src], .ss22-project img[src], .ss18-project img[src], .ss23-project img[src], .propertyCollageHero img[src]')];
        const sources = [...new Set([...cards, ...doc.querySelectorAll('main img[src]')].filter((i, n) => cards.includes(i) || n < cards.length + 6).map(i => new URL(i.getAttribute('src'), baseURL).href))];
        return Promise.all(sources.map(src => new Promise(resolve => {
          const image = new Image();
          image.fetchPriority = urgent ? 'high' : 'low';
          image.onload = () => image.decode().catch(() => {}).then(resolve);
          image.onerror = resolve;
          heldImages.push(image);
          if (heldImages.length > 60) heldImages.shift();
          image.src = src;
        })));
      }).catch(() => {});
    pages.set(url.href, job);
    if (pages.size > 10) pages.delete(pages.keys().next().value);
    return job;
  };
  let hoverTimer;
  document.addEventListener('pointerover', event => {
    const url = eligible(event.target.closest('a[href]'));
    clearTimeout(hoverTimer);
    if (url) hoverTimer = setTimeout(() => warm(url), 100);
  }, {passive: true});
  document.addEventListener('pointerdown', event => {
    const url = eligible(event.target.closest('a[href]'));
    if (url) warm(url, true);
  }, {passive: true});
  let navigation = 0;
  document.addEventListener('click', event => {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const anchor = event.target.closest('a[href]');
    const url = eligible(anchor);
    if (!url) return;
    event.preventDefault();
    const ticket = ++navigation;
    // The existing page remains fully visible and interactive while photos warm.
    warm(url, true).then(() => {
      if (ticket === navigation) location.assign(url.href);
    });
  });
})();
