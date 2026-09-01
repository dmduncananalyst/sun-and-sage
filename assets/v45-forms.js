(()=>{
  const email='dominique@therise.group';
  const openEmail=(subject,lines)=>{
    location.href='mailto:'+email+'?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(lines.filter(Boolean).join('\n'));
  };

  document.querySelectorAll('.consultationForm,.contactPageForm').forEach(form=>{
    form.addEventListener('submit',event=>{
      event.preventDefault();
      if(!form.reportValidity())return;
      const d=new FormData(form),topic=form.dataset.topic||'Website contact';
      openEmail(topic+' request',[
        'Request: '+topic,
        'Name: '+d.get('name'),
        'Email: '+d.get('email'),
        'Phone: '+(d.get('phone')||'Not provided'),
        'How they found Dominique: '+d.get('source'),
        'Message: '+(d.get('message')||'Not provided')
      ]);
    });
  });

  const firstStep=document.querySelector('.miniLeadForm');
  const dialog=document.querySelector('.evaluationContactDialog');
  if(firstStep&&dialog){
    firstStep.addEventListener('submit',event=>{
      event.preventDefault();
      if(!firstStep.reportValidity())return;
      dialog.showModal();
    });
    dialog.querySelector('.dialogClose')?.addEventListener('click',()=>dialog.close());
    dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close()});
    dialog.querySelector('.evaluationContactForm')?.addEventListener('submit',event=>{
      event.preventDefault();
      const form=event.currentTarget;
      if(!form.reportValidity())return;
      const property=new FormData(firstStep),contact=new FormData(form);
      openEmail('Free home evaluation request',[
        'Request: Free home evaluation',
        'Property address: '+property.get('address'),
        'City: '+property.get('city'),
        'Timing: '+property.get('timing'),
        'Name: '+contact.get('name'),
        'Email: '+contact.get('email'),
        'Phone: '+(contact.get('phone')||'Not provided'),
        'How they found Dominique: '+contact.get('source'),
        'Property notes: '+(contact.get('message')||'Not provided')
      ]);
    });
  }
})();

/* v54 shared mobile navigation and portfolio photograph viewer. */
(()=>{
  const mobile=()=>matchMedia('(max-width:800px)').matches;
  if(!/\/(index\.html)?$/.test(location.pathname)){
    const header=document.querySelector('body>header,header.siteHeader,header');
    if(header&&!document.querySelector('.mobileBackControl')){
      const back=document.createElement('button');
      back.type='button';
      back.className='mobileBackControl';
      back.innerHTML='<span aria-hidden="true">←</span> Back';
      back.addEventListener('click',()=>{if(history.length>1)history.back();else location.href='index.html'});
      header.insertAdjacentElement('afterend',back);
    }
  }

  const gallerySelector='.jobGallery,.projectGallery';
  const imageSelector='.jobGallery img,.projectGallery img';
  const galleries=[...document.querySelectorAll(gallerySelector)];
  if(!galleries.length)return;

  galleries.forEach(gallery=>{
    if(gallery.previousElementSibling?.classList.contains('portfolioZoomInstruction'))return;
    const note=document.createElement('p');
    note.className='portfolioZoomInstruction';
    note.textContent='Select any photograph to view it larger.';
    gallery.insertAdjacentElement('beforebegin',note);
  });

  const viewer=document.createElement('div');
  viewer.className='portfolioLightbox';
  viewer.setAttribute('role','dialog');
  viewer.setAttribute('aria-modal','true');
  viewer.setAttribute('aria-label','Enlarged portfolio photograph');
  viewer.innerHTML='<div class="portfolioLightboxStage"><img alt=""/><button class="portfolioLightboxClose" type="button" aria-label="Close enlarged photograph">×</button></div>';
  document.body.appendChild(viewer);
  const large=viewer.querySelector('img');
  const close=viewer.querySelector('button');
  const images=()=>[...document.querySelectorAll(imageSelector)];
  const markImages=()=>images().forEach(img=>{
    img.classList.add('portfolioZoomTarget');
    if(img.parentElement?.classList.contains('portfolioZoomFrame'))return;
    const frame=document.createElement('span');
    frame.className='portfolioZoomFrame';
    img.parentNode.insertBefore(frame,img);
    frame.appendChild(img);
    const label=document.createElement('span');
    label.className='portfolioZoomLabel';
    label.textContent='View larger';
    frame.appendChild(label);
  });
  const show=img=>{
    large.src=img.currentSrc||img.src; large.alt=img.alt||'Portfolio photograph';
    viewer.classList.add('isOpen');
    document.body.classList.add('portfolioLightboxOpen');
    close.focus();
  };
  const hide=()=>{
    viewer.classList.remove('isOpen');
    document.body.classList.remove('portfolioLightboxOpen');
  };
  markImages();
  new MutationObserver(markImages).observe(document.body,{childList:true,subtree:true});
  document.addEventListener('click',event=>{
    const frame=event.target.closest?.('.portfolioZoomFrame');
    const img=frame?.querySelector('img');
    if(!img)return;
    event.preventDefault();
    show(img);
  });
  close.addEventListener('click',hide);
})();
