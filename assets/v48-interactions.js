(() => {
  /* Real browser-back behavior with a useful direct-entry fallback. */
  document.querySelectorAll('[data-smart-back]').forEach(link => {
    link.addEventListener('click', event => {
      let hasUsefulReferrer = false;
      try {
        hasUsefulReferrer = Boolean(document.referrer) && new URL(document.referrer).origin === location.origin;
      } catch (_) {}
      if (hasUsefulReferrer && history.length > 1) {
        event.preventDefault();
        history.back();
      }
    });
  });

  /* Region city focus: every city remains visible in the index; only its profile is shown. */
  document.querySelectorAll('.valleyCatalogue').forEach(catalogue => {
    const links = [...catalogue.querySelectorAll('.cityIndex a')];
    const cards = [...catalogue.querySelectorAll('.cityEntry')];
    if (!links.length || !cards.length) return;
    const activate = id => {
      links.forEach(link => {
        const active = link.getAttribute('href') === `#${id}`;
        link.classList.toggle('active', active);
        link.setAttribute('aria-current', active ? 'true' : 'false');
      });
      cards.forEach(card => card.classList.toggle('active', card.id === id));
    };
    activate((location.hash || links[0].getAttribute('href')).slice(1));
    links.forEach(link => {
      const id = link.getAttribute('href').slice(1);
      ['pointerenter', 'focus'].forEach(type => link.addEventListener(type, () => activate(id)));
      link.addEventListener('click', event => {
        event.preventDefault();
        activate(id);
        history.replaceState(null, '', `#${id}`);
      });
    });
  });

  /* Flip cards also work by tap and keyboard, not only by hover. */
  document.querySelectorAll('.qaFlip').forEach(card => {
    card.addEventListener('click', () => card.classList.toggle('is-flipped'));
    card.addEventListener('keydown', event => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        card.classList.toggle('is-flipped');
      }
    });
  });

  /* Review salon: no carousel, no arrows, one original review selected at a time. */
  const reviewButtons = [...document.querySelectorAll('[data-review-target]')];
  const reviewImages = [...document.querySelectorAll('.reviewStage img')];
  reviewButtons.forEach(button => button.addEventListener('click', () => {
    const target = button.dataset.reviewTarget;
    reviewButtons.forEach(item => item.classList.toggle('active', item === button));
    reviewImages.forEach(image => image.classList.toggle('active', image.id === target));
  }));

  /* The home-value reading follows hover/focus as well as click. */
  document.querySelectorAll('.factorWheel [data-factor]').forEach(button => {
    const selectFactor = () => button.click();
    button.addEventListener('pointerenter', selectFactor);
    button.addEventListener('focus', selectFactor);
  });

  /* Every "Ready for your next step" invitation opens the form in place. */
  document.querySelectorAll('.footerNextStep a, .servicePageClose a').forEach(link => {
    link.addEventListener('click', event => {
      const dialog = document.querySelector('.contactFormModal');
      if (!dialog || typeof dialog.showModal !== 'function') return;
      event.preventDefault();
      event.stopImmediatePropagation();
      document.querySelectorAll('details[open]').forEach(detail => detail.removeAttribute('open'));
      if (!dialog.open) dialog.showModal();
    }, true);
  });
})();
