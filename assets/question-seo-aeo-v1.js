(function(){
  function send(name,params){try{if(typeof window.gtag==='function')window.gtag('event',name,params||{});}catch(e){}}
  document.addEventListener('click',function(e){
    var a=e.target.closest('a'); if(!a)return;
    var href=a.getAttribute('href')||'';
    if(a.hasAttribute('data-qseo-consultation')) send('select_consultation',{destination_url:a.href,page_location:location.href});
    if(a.hasAttribute('data-qseo-related')) send('view_related_article',{destination_url:a.href,page_location:location.href});
    if(href.indexOf('tel:')===0) send('click_to_call',{destination_url:href,page_location:location.href});
    if(href.indexOf('mailto:')===0) send('click_email',{destination_url:href,page_location:location.href});
  },false);
  /* HubSpot emits this message only after a form is submitted successfully. */
  window.addEventListener('message',function(event){
    var d=event && event.data;
    if(!d || d.type!=='hsFormCallback') return;
    if(d.eventName==='onFormSubmitted') send('generate_lead',{form_id:d.id||'',page_location:location.href});
  },false);
})();
