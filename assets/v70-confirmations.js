(() => {
  if (window.sunSageShowConfirmation) return;

  const dialog=document.createElement('dialog');
  dialog.className='v70SubmissionConfirm';
  dialog.innerHTML=`
    <button type="button" class="v70ConfirmClose" aria-label="Close">×</button>
    <span class="v70ConfirmEyebrow">Request received</span>
    <h2 class="v70ConfirmTitle">Thank you.</h2>
    <p class="v70ConfirmContext"></p>
    <div class="v70ConfirmThanks">
      <p>Dominique will follow up personally.</p>
      <button type="button" class="v70ConfirmDone">Close</button>
    </div>`;
  document.body.appendChild(dialog);

  const close=()=>dialog.close();
  dialog.querySelector('.v70ConfirmClose').addEventListener('click',close);
  dialog.querySelector('.v70ConfirmDone').addEventListener('click',close);
  dialog.addEventListener('click',e=>{if(e.target===dialog)close()});

  const contentFor=form=>{
    if(form.classList.contains('regionRequestForm')){
      const region=form.dataset.region || 'San Fernando Valley';
      return ['HOME SEARCH REQUEST', `Dominique received your ${region} home search request.`, 'Dominique will follow up with homes shaped around your priorities.'];
    }
    if(form.classList.contains('evaluationContactForm')){
      return ['HOME EVALUATION REQUEST', 'Your home evaluation request has been received.', 'Dominique will review the property details and follow up personally.'];
    }
    if(form.classList.contains('contactPageForm')){
      return ['MESSAGE RECEIVED', 'Your message has been sent to Dominique.', 'Dominique will follow up personally.'];
    }
    if(form.classList.contains('contactModalForm')){
      const service=form.querySelector('[name="service"]')?.value || '';
      if(service==='Buy a Home') return ['BUYER CONSULTATION', 'Your buyer consultation request has been received.', 'Dominique will follow up personally about your home search.'];
      if(service==='Sell a Home') return ['SELLER CONSULTATION', 'Your seller consultation request has been received.', 'Dominique will follow up personally about your selling plans.'];
      if(service==='Interior Design') return ['INTERIOR DESIGN', 'Your interior design inquiry has been received.', 'Dominique will follow up personally about your project.'];
      if(service==='Property Management') return ['PROPERTY MANAGEMENT', 'Your property management inquiry has been received.', 'Dominique will follow up personally about your property.'];
      return ['REQUEST RECEIVED','Your request has been received.','Dominique will follow up personally.'];
    }
    return ['REQUEST RECEIVED','Your request has been received.','Dominique will follow up personally.'];
  };

  window.sunSageShowConfirmation=form=>{
    const [eyebrow,context,followup]=contentFor(form);
    dialog.querySelector('.v70ConfirmEyebrow').textContent=eyebrow;
    dialog.querySelector('.v70ConfirmTitle').textContent='Thank you.';
    dialog.querySelector('.v70ConfirmContext').textContent=context;
    dialog.querySelector('.v70ConfirmThanks p').textContent=followup;
    if(!dialog.open) dialog.showModal();
  };
})();