/* Targeted display audit. No content removal, no Portfolio changes, no network calls. */
(() => {
 'use strict';
 const untouched = '.ss22-portfolio,.homePortfolioVideos,.ss23-project,.portfolioParentCard,.ss22-service-hero';
 function color(value){
   const m=(value||'').match(/rgba?\(([^)]+)\)/);if(!m)return null;
   const n=m[1].split(/[\s,\/]+/).filter(Boolean).map(Number);return n.length>=3?[n[0],n[1],n[2],n.length>3?n[3]:1]:null;
 }
 function luminance(c){return c.slice(0,3).map(n=>{n/=255;return n<=.04045?n/12.92:Math.pow((n+.055)/1.055,2.4)}).reduce((s,n,i)=>s+n*[.2126,.7152,.0722][i],0)}
 function contrast(a,b){const x=luminance(a),y=luminance(b);return(Math.max(x,y)+.05)/(Math.min(x,y)+.05)}
 function background(el){
   const layers=[];let opacity=1;
   for(let node=el;node&&node.nodeType===1;node=node.parentElement){
     const st=getComputedStyle(node);
     if(st.backgroundImage!=='none')return null; // Do not guess text colors over photos/gradients.
     const c=color(st.backgroundColor);if(c&&c[3]>0){layers.push(c);opacity*=1-c[3];if(opacity<.01)break}
   }
   let result=[248,247,243];
   for(let i=layers.length-1;i>=0;i--){const c=layers[i];result=result.map((v,k)=>c[k]*c[3]+v*(1-c[3]))}
   return result;
 }
 function review(){
   document.querySelectorAll('#main p,#main h1,#main h2,#main h3,#main h4,#main span,#main small,#main figcaption,#main a,#main button,#main strong,.sunConversation h3,.sunConversation p,.sunConversation button').forEach(el=>{
     if(el.closest(untouched)||el.querySelector('svg')||!el.getClientRects().length)return;
     if(![...el.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))return;
     const st=getComputedStyle(el);if(st.visibility==='hidden'||Number(st.opacity)===0)return;
     const fg=color(st.color),bg=background(el);if(!fg||!bg)return;
     const threshold=parseFloat(st.fontSize)>=24?3:4.5;
     if(contrast(fg,bg)>=threshold)return;
     const white=[255,255,255],ink=[48,56,46];
     el.classList.add(contrast(white,bg)>contrast(ink,bg)?'v27-readable-on-dark':'v27-readable-on-light');
   });
 }
 function finish(){
   review();
   if(document.querySelector('main [data-sun-conversation-open="true"]')){
     document.querySelectorAll('footer .ss22-footer-action').forEach(el=>el.hidden=true);
   }
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',finish,{once:true});else finish();
 window.addEventListener('load',finish,{once:true});
 // Chat choices are inserted on demand, so check those after the visitor selects one.
 document.addEventListener('click',e=>{if(e.target.closest('.sunConversation,[data-sun-conversation-open]'))requestAnimationFrame(review)});
 window.addEventListener('resize',()=>{clearTimeout(window.__v27Review);window.__v27Review=setTimeout(review,120)});
})();
