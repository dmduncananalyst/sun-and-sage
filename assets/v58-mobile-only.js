(() => {
  const mobile = window.matchMedia('(max-width:800px)');

  const menuButton = document.querySelector('.menuButton');
  const mobileNav = document.querySelector('.mobileNavTree');
  if (menuButton && mobileNav) {
    menuButton.textContent = 'Menu';
    menuButton.setAttribute('aria-label', 'Open menu');
    menuButton.setAttribute('aria-expanded', 'false');
    const backdrop = document.createElement('button');
    backdrop.className = 'v58-menu-backdrop';
    backdrop.type = 'button';
    backdrop.setAttribute('aria-label', 'Close menu');
    document.body.append(backdrop);
    const menuTitle = document.createElement('span');
    menuTitle.className = 'v58-menu-title';
    menuTitle.textContent = 'Navigation';
    const closeButton = document.createElement('button');
    closeButton.className = 'v58-menu-close';
    closeButton.type = 'button';
    closeButton.setAttribute('aria-label', 'Close menu');
    closeButton.textContent = '×';
    mobileNav.prepend(menuTitle, closeButton);
    mobileNav.querySelectorAll('summary').forEach(summary => {
      const arrow = summary.querySelector(':scope > b');
      if (!arrow) return;
      arrow.setAttribute('role', 'button');
      arrow.setAttribute('tabindex', '0');
      arrow.setAttribute('aria-label', 'Toggle submenu');
    });
    const setMenu = open => {
      document.body.classList.toggle('v58-menu-open', open);
      mobileNav.classList.toggle('open', open);
      menuButton.setAttribute('aria-expanded', String(open));
      menuButton.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    };
    menuButton.addEventListener('click', event => {
      event.stopImmediatePropagation();
      setMenu(!document.body.classList.contains('v58-menu-open'));
    }, true);
    backdrop.addEventListener('click', () => setMenu(false));
    closeButton.addEventListener('click', () => setMenu(false));
    /* Give each control its own action. This avoids conflicts with the
       website's older delegated mobile-menu listener. */
    mobileNav.querySelectorAll('a[href]').forEach(link => {
      link.addEventListener('click', event => {
        const href = link.getAttribute('href');
        if (!href || href.startsWith('#') || href.startsWith('javascript:')) return;
        event.preventDefault();
        event.stopImmediatePropagation();
        window.location.assign(link.href);
      }, true);
    });
    mobileNav.querySelectorAll('summary > b').forEach(arrow => {
      const toggleSubmenu = event => {
        event.preventDefault();
        event.stopImmediatePropagation();
        const details = arrow.closest('details');
        if (!details) return;
        details.open = !details.open;
        arrow.setAttribute('aria-expanded', String(details.open));
      };
      arrow.addEventListener('click', toggleSubmenu, true);
      arrow.addEventListener('keydown', event => {
        if (event.key === 'Enter' || event.key === ' ') toggleSubmenu(event);
      }, true);
    });
    document.addEventListener('keydown', event => { if (event.key === 'Escape') setMenu(false); });
  }
  /* Valley guide cities stay in-page; no city-on-city modal. */
  const cityIndex = document.querySelector('.cityIndex');
  if (cityIndex && document.querySelector('.cityEntry') && !document.querySelector('.v80-city-hint')) {
    const hint = document.createElement('p');
    hint.className = 'v80-city-hint';
    hint.textContent = 'Hover over or select a city to explore its details.';
    cityIndex.before(hint);
  }

  /* Footer phone confirmation prompt removed by request. */
})();
