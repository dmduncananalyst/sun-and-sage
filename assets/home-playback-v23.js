(()=>{'use strict';
 const video=document.querySelector('#home-introduction-video');if(!video)return;
 const hero=video.closest('.videoHero');if(!hero)return;
 let revealed=false,started=false,fallback=0;
 document.documentElement.classList.remove('preview-loading');document.documentElement.style.visibility='visible';
 video.muted=true;video.loop=true;video.playsInline=true;
 function play(){if(started)return;started=true;video.play().catch(()=>{video.controls=true;video.setAttribute('aria-label','Play Dominique’s introduction video')});setTimeout(()=>hero.classList.add('ss23-doors-finished'),160)}
 function reveal(){if(revealed)return;revealed=true;if(fallback){clearTimeout(fallback);fallback=0;}hero.classList.add('ss23-opening');if(matchMedia('(prefers-reduced-motion: reduce)').matches){hero.classList.add('ss23-doors-finished');play();return;}setTimeout(play,1180)}
 function ready(){requestAnimationFrame(()=>requestAnimationFrame(reveal))}
 if(video.readyState>=3) ready(); else {video.addEventListener('canplay',ready,{once:true});video.addEventListener('loadeddata',ready,{once:true});fallback=setTimeout(ready,2200);try{video.load()}catch(e){}}
 video.addEventListener('error',()=>{if(fallback)clearTimeout(fallback);reveal();video.controls=true},{once:true});
 document.addEventListener('visibilitychange',()=>{if(!document.hidden&&started&&video.paused&&!video.controls)video.play().catch(()=>{})});
})();