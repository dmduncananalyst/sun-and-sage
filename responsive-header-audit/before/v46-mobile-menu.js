/* Restore the page's previous scroll state after either touch navigation closes. */
(()=>{
 const header=document.querySelector('#ss22-header');if(!header)return;
 let locked=false,previousOverflow='',previousPriority='';
 const sync=()=>{
  const open=header.classList.contains('menu-is-open')||header.classList.contains('feature-is-open');
  document.documentElement.classList.toggle('ss22-navigation-open',open);
  if(open&&!locked){previousOverflow=document.body.style.getPropertyValue('overflow');previousPriority=document.body.style.getPropertyPriority('overflow');document.body.style.setProperty('overflow','hidden','important');locked=true;}
  else if(!open&&locked){if(previousOverflow)document.body.style.setProperty('overflow',previousOverflow,previousPriority);else document.body.style.removeProperty('overflow');locked=false;}
 };
 new MutationObserver(sync).observe(header,{attributes:true,attributeFilter:['class']});sync();
})();
