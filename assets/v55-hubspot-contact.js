(() => {
  const portalId = '247079925';
  const formId = '9f964a9c-2d5d-4238-a4bb-421002fa0ed6';
  const endpoint = `https://api-na2.hsforms.com/submissions/v3/integration/submit/${portalId}/${formId}`;

  const splitName = value => {
    const parts = value.trim().split(/\s+/);
    return {
      firstName: parts.shift() || '',
      lastName: parts.join(' ') || '(not provided)'
    };
  };

  document.querySelectorAll('.contactModalForm').forEach(form => {
    form.addEventListener('submit', async event => {
      event.preventDefault();
      event.stopImmediatePropagation();
      if (!form.reportValidity()) return;

      const data = new FormData(form);
      const name = splitName(String(data.get('name') || ''));
      const source = String(data.get('source') || '').replace(
        'AI Chat (Claude, ChatGPT, etc)',
        'AI Chat (Claude, ChatGPT, etc.)'
      );
      const button = form.querySelector('button[type="submit"]');
      const originalButton = button?.innerHTML;
      const status = document.createElement('p');
      status.className = 'hubspotFormStatus';
      status.setAttribute('role', 'status');
      status.setAttribute('aria-live', 'polite');

      form.querySelector('.hubspotFormStatus')?.remove();
      if (button) {
        button.disabled = true;
        button.textContent = 'Sending…';
      }

      const cookie = document.cookie.match(/(?:^|;\s*)hubspotutk=([^;]+)/)?.[1];
      const fields = [
        { name: 'firstname', value: name.firstName },
        { name: 'lastname', value: name.lastName },
        { name: 'email', value: String(data.get('email') || '') },
        { name: 'phone', value: String(data.get('phone') || '') },
        { name: 'message', value: String(data.get('message') || '') },
        { name: 'how_can_dominique_help', value: String(data.get('service') || '') },
        { name: 'how_did_you_find_us', value: source }
      ].filter(field => field.value);

      try {
        const response = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            fields,
            context: {
              ...(cookie ? { hutk: cookie } : {}),
              pageUri: location.href,
              pageName: document.title
            }
          })
        });

        if (!response.ok) throw new Error('HubSpot rejected the submission.');

        form.reset();
        if (button) {
          button.textContent = 'Thank you, Dominique will follow up';
          button.disabled = true;
        }
      } catch (error) {
        status.textContent = 'Your message could not be sent. Please try again.';
        form.appendChild(status);
        if (button) {
          button.innerHTML = originalButton;
          button.disabled = false;
        }
      }
    }, true);
  });
})();

(() => {
  const portalId = '247079925';
  const formId = '39e25c59-3606-482e-b999-01eaa236b90c';
  const endpoint = `https://api-na2.hsforms.com/submissions/v3/integration/submit/${portalId}/${formId}`;

  const splitName = value => {
    const parts = value.trim().split(/\s+/);
    return {
      firstName: parts.shift() || '',
      lastName: parts.join(' ') || '(not provided)'
    };
  };

  document.querySelectorAll('.regionRequestForm').forEach(form => {
    form.addEventListener('submit', async event => {
      event.preventDefault();
      event.stopImmediatePropagation();
      if (!form.reportValidity()) return;

      const data = new FormData(form);
      const name = splitName(String(data.get('name') || ''));
      const source = String(data.get('source') || '').replace(
        'AI Chat (Claude, ChatGPT, etc)',
        'AI Chat (Claude, ChatGPT, etc.)'
      );
      const button = form.querySelector('button[type="submit"]');
      const originalButton = button?.innerHTML;
      let status = form.querySelector('.hubspotFormStatus');
      if (!status) {
        status = document.createElement('p');
        status.className = 'hubspotFormStatus';
        status.setAttribute('role', 'status');
        status.setAttribute('aria-live', 'polite');
        form.appendChild(status);
      }
      status.textContent = '';
      if (button) {
        button.disabled = true;
        button.textContent = 'Sending…';
      }

      const cookie = document.cookie.match(/(?:^|;\s*)hubspotutk=([^;]+)/)?.[1];
      const fields = [
        { name: 'firstname', value: name.firstName },
        { name: 'lastname', value: name.lastName },
        { name: 'email', value: String(data.get('email') || '') },
        { name: 'phone', value: String(data.get('phone') || '') },
        { name: 'message', value: String(data.get('message') || '') },
        { name: 'how_did_you_find_us', value: source },
        { name: 'property_search_city', value: String(data.get('city') || '') },
        { name: 'valley_region', value: String(form.dataset.region || '') },
        { name: 'home_buying_budget', value: String(data.get('budget') || '') },
        { name: 'moving_timelin', value: String(data.get('timing') || '') }
      ].filter(field => field.value);

      try {
        const response = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            fields,
            context: {
              ...(cookie ? { hutk: cookie } : {}),
              pageUri: location.href,
              pageName: document.title
            }
          })
        });
        if (!response.ok) throw new Error('HubSpot rejected the submission.');

        form.reset();
        if (button) {
          button.textContent = 'Thank you, Dominique will follow up';
          button.disabled = true;
        }
      } catch (error) {
        status.textContent = 'Your property request could not be sent. Please try again.';
        if (button) {
          button.innerHTML = originalButton;
          button.disabled = false;
        }
      }
    }, true);
  });
})();

(() => {
  const portalId = '247079925';
  const formId = 'b7fffa9e-1693-4f3a-837c-3f15e93eaaa5';
  const endpoint = `https://api-na2.hsforms.com/submissions/v3/integration/submit/${portalId}/${formId}`;
  const dialog = document.querySelector('.propertyRequest');
  const form = dialog?.querySelector('.requestDetails');
  if (!dialog || !form) return;

  form.addEventListener('submit', async event => {
    event.preventDefault();
    event.stopImmediatePropagation();
    if (!form.reportValidity()) return;

    const data = new FormData(form);
    const criteria = dialog.querySelector('.requestCriteria')?.textContent
      .split('•')
      .map(value => value.trim())
      .filter(Boolean) || [];
    const source = String(data.get('source') || '').replace(
      'AI Chat (Claude, ChatGPT, etc)',
      'AI Chat (Claude, ChatGPT, etc.)'
    );
    const button = form.querySelector('.requestSend');
    const originalButton = button?.textContent;
    let status = form.querySelector('.hubspotFormStatus');
    if (!status) {
      status = document.createElement('p');
      status.className = 'hubspotFormStatus';
      status.setAttribute('role', 'status');
      status.setAttribute('aria-live', 'polite');
      form.appendChild(status);
    }
    status.textContent = '';
    if (button) {
      button.disabled = true;
      button.textContent = 'Sending…';
    }

    const cookie = document.cookie.match(/(?:^|;\s*)hubspotutk=([^;]+)/)?.[1];
    const fields = [
      { name: 'firstname', value: String(data.get('firstName') || '') },
      { name: 'lastname', value: String(data.get('lastName') || '') },
      { name: 'email', value: String(data.get('email') || '') },
      { name: 'phone', value: String(data.get('phone') || '') },
      { name: 'preferred_contact_method', value: String(data.get('contactMethod') || '') },
      { name: 'how_did_you_find_us', value: source },
      { name: 'property_search_city', value: criteria[0] || '' },
      { name: 'minimum_home_price', value: criteria[1] || '' },
      { name: 'maximum_home_price', value: criteria[2] || '' },
      { name: 'desired_property_type', value: criteria[3] || '' }
    ].filter(field => field.value);

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          fields,
          context: {
            ...(cookie ? { hutk: cookie } : {}),
            pageUri: location.href,
            pageName: document.title
          }
        })
      });
      if (!response.ok) throw new Error('HubSpot rejected the submission.');

      form.reset();
      form.hidden = true;
      dialog.querySelector('.requestThanks').hidden = false;
    } catch (error) {
      status.textContent = 'Your property request could not be sent. Please try again.';
      if (button) {
        button.disabled = false;
        button.textContent = originalButton;
      }
    }
  }, true);
})();

(() => {
  const portalId = '247079925';
  const formId = '3a3caedf-8f1d-47f9-a485-5904d87d9f2e';
  const endpoint = `https://api-na2.hsforms.com/submissions/v3/integration/submit/${portalId}/${formId}`;

  const splitName = value => {
    const parts = value.trim().split(/\s+/);
    return {
      firstName: parts.shift() || '',
      lastName: parts.join(' ') || '(not provided)'
    };
  };

  document.querySelectorAll('.contactPageForm').forEach(form => {
    form.addEventListener('submit', async event => {
      event.preventDefault();
      event.stopImmediatePropagation();
      if (!form.reportValidity()) return;

      const data = new FormData(form);
      const name = splitName(String(data.get('name') || ''));
      const source = String(data.get('source') || '').replace(
        'AI Chat (Claude, ChatGPT, etc)',
        'AI Chat (Claude, ChatGPT, etc.)'
      );
      const button = form.querySelector('button[type="submit"], button:not([type])');
      const originalButton = button?.innerHTML;
      let status = form.querySelector('.hubspotFormStatus');
      if (!status) {
        status = document.createElement('p');
        status.className = 'hubspotFormStatus';
        status.setAttribute('role', 'status');
        status.setAttribute('aria-live', 'polite');
        form.appendChild(status);
      }
      status.textContent = '';
      if (button) {
        button.disabled = true;
        button.textContent = 'Sending…';
      }

      const cookie = document.cookie.match(/(?:^|;\s*)hubspotutk=([^;]+)/)?.[1];
      const fields = [
        { name: 'firstname', value: name.firstName },
        { name: 'lastname', value: name.lastName },
        { name: 'email', value: String(data.get('email') || '') },
        { name: 'phone', value: String(data.get('phone') || '') },
        { name: 'message', value: String(data.get('message') || '') },
        { name: 'how_did_you_find_us', value: source }
      ].filter(field => field.value);

      try {
        const response = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            fields,
            context: {
              ...(cookie ? { hutk: cookie } : {}),
              pageUri: location.href,
              pageName: document.title
            }
          })
        });
        if (!response.ok) throw new Error('HubSpot rejected the submission.');

        form.reset();
        if (button) {
          button.textContent = 'Thank you, Dominique will follow up';
          button.disabled = true;
        }
      } catch (error) {
        status.textContent = 'Your message could not be sent. Please try again.';
        if (button) {
          button.innerHTML = originalButton;
          button.disabled = false;
        }
      }
    }, true);
  });
})();

(() => {
  const portalId = '247079925';
  const formId = '612b67da-7ecf-49c2-8f0a-21f356fbf66b';
  const endpoint = `https://api-na2.hsforms.com/submissions/v3/integration/submit/${portalId}/${formId}`;
  const propertyForm = document.querySelector('.miniLeadForm');
  const contactForm = document.querySelector('.evaluationContactForm');
  if (!propertyForm || !contactForm) return;

  const splitName = value => {
    const parts = value.trim().split(/\s+/);
    return {
      firstName: parts.shift() || '',
      lastName: parts.join(' ') || '(not provided)'
    };
  };

  const timelineValues = {
    'Exploring my options': 'Just exploring',
    'Within three months': '0–3 months',
    'Within six months': '3–6 months',
    'Not sure yet': 'Just exploring'
  };

  contactForm.addEventListener('submit', async event => {
    event.preventDefault();
    event.stopImmediatePropagation();
    if (!propertyForm.reportValidity() || !contactForm.reportValidity()) return;

    const property = new FormData(propertyForm);
    const contact = new FormData(contactForm);
    const name = splitName(String(contact.get('name') || ''));
    const source = String(contact.get('source') || '').replace(
      'AI Chat (Claude, ChatGPT, etc)',
      'AI Chat (Claude, ChatGPT, etc.)'
    );
    const timing = String(property.get('timing') || '');
    const button = contactForm.querySelector('button[type="submit"]');
    const originalButton = button?.innerHTML;
    let status = contactForm.querySelector('.hubspotFormStatus');
    if (!status) {
      status = document.createElement('p');
      status.className = 'hubspotFormStatus full';
      status.setAttribute('role', 'status');
      status.setAttribute('aria-live', 'polite');
      contactForm.appendChild(status);
    }
    status.textContent = '';
    if (button) {
      button.disabled = true;
      button.textContent = 'Sending…';
    }

    const cookie = document.cookie.match(/(?:^|;\s*)hubspotutk=([^;]+)/)?.[1];
    const fields = [
      { name: 'firstname', value: name.firstName },
      { name: 'lastname', value: name.lastName },
      { name: 'email', value: String(contact.get('email') || '') },
      { name: 'phone', value: String(contact.get('phone') || '') },
      { name: 'address', value: String(property.get('address') || '') },
      { name: 'city', value: String(property.get('city') || '') },
      { name: 'selling_timeline', value: timelineValues[timing] || timing },
      { name: 'message', value: String(contact.get('message') || '') },
      { name: 'how_did_you_find_us', value: source }
    ].filter(field => field.value);

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          fields,
          context: {
            ...(cookie ? { hutk: cookie } : {}),
            pageUri: location.href,
            pageName: document.title
          }
        })
      });
      if (!response.ok) throw new Error('HubSpot rejected the submission.');

      propertyForm.reset();
      contactForm.reset();
      if (button) {
        button.textContent = 'Thank you, Dominique will follow up';
        button.disabled = true;
      }
    } catch (error) {
      status.textContent = 'Your evaluation request could not be sent. Please try again.';
      if (button) {
        button.innerHTML = originalButton;
        button.disabled = false;
      }
    }
  }, true);
})();
