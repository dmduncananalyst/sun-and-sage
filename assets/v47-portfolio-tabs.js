(() => {
  const tabSets = document.querySelectorAll('[data-portfolio-tabs]');

  tabSets.forEach((tabSet) => {
    const tabs = Array.from(tabSet.querySelectorAll('[role="tab"]'));
    const panels = Array.from(tabSet.querySelectorAll('[role="tabpanel"]'));

    const loadGallery = (panel) => {
      const gallery = panel.querySelector('[data-job-gallery]');
      if (!gallery || gallery.dataset.loaded === 'true') return;

      const slug = gallery.dataset.job;
      const count = Number(gallery.dataset.count || 0);
      const skipped = new Set((gallery.dataset.skip || '').split(',').map(Number).filter(Boolean));
      const title = gallery.dataset.title || 'Interior design project';
      const fragment = document.createDocumentFragment();

      for (let index = 1; index <= count; index += 1) {
        if (skipped.has(index)) continue;
        const figure = document.createElement('figure');
        const image = document.createElement('img');
        image.src = `assets/portfolio-jobs/${slug}/photo-${String(index).padStart(2, '0')}.webp`;
        image.alt = `${title} project photograph ${index}`;
        image.loading = index <= 3 ? 'eager' : 'lazy';
        image.decoding = 'async';
        figure.appendChild(image);
        fragment.appendChild(figure);
      }

      gallery.appendChild(fragment);
      gallery.dataset.loaded = 'true';
    };

    const activate = (tab, updateHash = true) => {
      const panelId = tab.getAttribute('aria-controls');
      tabs.forEach((item) => {
        const active = item === tab;
        item.setAttribute('aria-selected', String(active));
        item.tabIndex = active ? 0 : -1;
      });
      panels.forEach((panel) => {
        const active = panel.id === panelId;
        panel.hidden = !active;
        if (active) loadGallery(panel);
      });
      if (updateHash && history.replaceState) history.replaceState(null, '', `#${tab.dataset.job}`);
    };

    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => activate(tab));
      tab.addEventListener('keydown', (event) => {
        if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
        event.preventDefault();
        let next = index;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = tabs.length - 1;
        tabs[next].focus();
        activate(tabs[next]);
      });
    });

    const requested = location.hash.replace('#', '');
    const initial = tabs.find((tab) => tab.dataset.job === requested) || tabs[0];
    if (initial) activate(initial, false);
  });
})();
