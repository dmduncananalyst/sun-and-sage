(() => {
  const PORTAL_ID = '247079925';
  const WEBSITE_FORM_ID = 'da6d1bd8-d7e9-4ff5-91a3-efa6c8abadfc';
  const VALUATION_FORM_ID = '219b1eb8-6a36-48c8-aec4-c930e48ce833';

  function hubspotEndpoint(formId){
    return `https://api-na2.hsforms.com/submissions/v3/integration/submit/${PORTAL_ID}/${formId}`;
  }
  function cookieValue(){
    return document.cookie.match(/(?:^|;\s*)hubspotutk=([^;]+)/)?.[1] || '';
  }
  async function submit(formId, fields){
    const hutk = cookieValue();
    const response = await fetch(hubspotEndpoint(formId), {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({
        fields: fields.filter(field => String(field.value || '').trim()),
        context: {
          ...(hutk ? {hutk} : {}),
          pageUri: location.href,
          pageName: document.title
        }
      })
    });
    if(!response.ok) throw new Error('HubSpot rejected the submission.');
  }

  // Contact page -> Website Conversation form.
  document.querySelectorAll('.contactPageForm').forEach(form => {
    form.addEventListener('submit', async event => {
      event.preventDefault();
      event.stopImmediatePropagation();
      if(!form.reportValidity()) return;
      const data = new FormData(form);
      const button = form.querySelector('button[type="submit"],button:not([type])');
      const original = button?.innerHTML;
      let status = form.querySelector('.hubspotFormStatus');
      if(!status){ status=document.createElement('p'); status.className='hubspotFormStatus'; status.setAttribute('role','status'); status.setAttribute('aria-live','polite'); form.appendChild(status); }
      status.textContent='';
      if(button){ button.disabled=true; button.textContent='Sending…'; }
      try{
        await submit(WEBSITE_FORM_ID,[
          {name:'firstname', value:String(data.get('name')||'')},
          {name:'email', value:String(data.get('email')||'')},
          {name:'phone', value:String(data.get('phone')||'')},
          {name:'message', value:String(data.get('message')||'')}
        ]);
        window.sunSageShowConfirmation?.(form);
        form.reset();
        if(button){ button.textContent='Thank you, Dominique will follow up'; button.disabled=true; }
      }catch(error){
        status.textContent='Your message could not be sent. Please try again.';
        if(button){ button.innerHTML=original; button.disabled=false; }
      }
    }, true);
  });


  // Regional guide request -> Website Conversation form. All regional details are bundled into Message.
  document.querySelectorAll('.regionRequestForm').forEach(form => {
    form.addEventListener('submit', async event => {
      event.preventDefault();
      event.stopImmediatePropagation();
      if(!form.reportValidity()) return;
      const data = new FormData(form);
      const button = form.querySelector('button[type="submit"],button:not([type])');
      const original = button?.innerHTML;
      let status = form.querySelector('.hubspotFormStatus');
      if(!status){ status=document.createElement('p'); status.className='hubspotFormStatus'; status.setAttribute('role','status'); status.setAttribute('aria-live','polite'); form.appendChild(status); }
      status.textContent='';
      if(button){ button.disabled=true; button.textContent='Sending…'; }
      const details = [
        `Region: ${form.dataset.region || ''}`,
        data.get('city') ? `Preferred community: ${data.get('city')}` : '',
        data.get('budget') ? `Budget: ${data.get('budget')}` : '',
        data.get('timing') ? `Timing: ${data.get('timing')}` : '',
        data.get('message') ? `What matters most: ${data.get('message')}` : ''
      ].filter(Boolean).join('\n');
      try{
        await submit(WEBSITE_FORM_ID,[
          {name:'firstname', value:String(data.get('name')||'')},
          {name:'email', value:String(data.get('email')||'')},
          {name:'phone', value:String(data.get('phone')||'')},
          {name:'message', value:details || `Region: ${form.dataset.region || ''}`}
        ]);
        window.sunSageShowConfirmation?.(form);
        form.reset();
        if(button){ button.textContent='Thank you, Dominique will follow up'; button.disabled=true; }
      }catch(error){
        status.textContent='Your request could not be sent. Please try again.';
        if(button){ button.innerHTML=original; button.disabled=false; }
      }
    }, true);
  });

  // One dedicated Home Valuation form -> Home Valuation HubSpot form.
  document.querySelectorAll('.homeValuationForm').forEach(form => {
    form.addEventListener('submit', async event => {
      event.preventDefault();
      event.stopImmediatePropagation();
      if(!form.reportValidity()) return;
      const data = new FormData(form);
      const button = form.querySelector('button[type="submit"],button:not([type])');
      const original = button?.innerHTML;
      let status = form.querySelector('.hubspotFormStatus');
      if(!status){ status=document.createElement('p'); status.className='hubspotFormStatus'; status.setAttribute('role','status'); status.setAttribute('aria-live','polite'); form.appendChild(status); }
      status.textContent='';
      if(button){ button.disabled=true; button.textContent='Sending…'; }
      try{
        await submit(VALUATION_FORM_ID,[
          {name:'firstname', value:String(data.get('name')||'')},
          {name:'address', value:String(data.get('address')||'')},
          {name:'email', value:String(data.get('email')||'')},
          {name:'phone', value:String(data.get('phone')||'')}
        ]);
        window.sunSageShowConfirmation?.(form);
        form.reset();
        if(button){ button.textContent='Thank you, Dominique will follow up'; button.disabled=true; }
      }catch(error){
        status.textContent='Your home valuation request could not be sent. Please try again.';
        if(button){ button.innerHTML=original; button.disabled=false; }
      }
    }, true);
  });
})();
