(()=>{'use strict';
 const video=document.getElementById('home-introduction-video');if(!video)return;
 const hero=video.closest('.videoHero');if(!hero)return;
 let started=false,opening=false,finished=false;
 document.documentElement.classList.remove('preview-loading');document.documentElement.style.visibility='visible';
 video.muted=true;video.loop=true;video.playsInline=true;
 function finish(){if(finished)return;finished=true;hero.classList.add('ss23-doors-finished');}
 function reveal(){if(opening)return;opening=true;hero.classList.add('ss23-opening');if(matchMedia('(prefers-reduced-motion: reduce)').matches){finish();return;}setTimeout(finish,1250);}
 hero.querySelector('.doors>div:last-child')?.addEventListener('animationend',event=>{if(event.animationName==='rightOpen')finish();});
 async function start(){if(started)return;started=true;try{await video.play();if(video.requestVideoFrameCallback){let shown=false;const show=()=>{if(shown)return;shown=true;reveal();};video.requestVideoFrameCallback(show);setTimeout(show,700);}else requestAnimationFrame(()=>requestAnimationFrame(reveal));}catch(e){video.controls=true;video.setAttribute('aria-label','Play Dominique’s introduction video');reveal();}}
 if(video.readyState>=2)start();else{video.addEventListener('loadeddata',start,{once:true});video.addEventListener('canplay',start,{once:true});video.addEventListener('error',start,{once:true});setTimeout(start,3000);try{video.load()}catch(e){start();}}
 document.addEventListener('visibilitychange',()=>{if(!document.hidden&&started&&video.paused&&!video.controls)video.play().catch(()=>{});});
})();
