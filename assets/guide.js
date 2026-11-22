(() => {
  'use strict';
  const dialog = document.getElementById('guide-request');
  const openButton = document.getElementById('guide-open');
  const form = dialog.querySelector('.hs-form-frame');
  const confirmation = document.getElementById('guide-confirmation');

  openButton.addEventListener('click', () => dialog.showModal());
  dialog.querySelector('.guide-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => openButton.focus());

  window.addEventListener('hs-form-event:on-submission:success', event => {
    if (event.detail?.formId !== form.dataset.formId) return;
    confirmation.hidden = false;
  });
})();
