(()=>{'use strict';
 const video=document.querySelector('#home-introduction-video');if(!video)return;
 const hero=video.closest('.videoHero');let started=false;
 document.documentElement.classList.remove('preview-loading');
 document.documentElement.style.visibility='visible';
 video.muted=true;video.loop=true;video.playsInline=true;
 function play(){if(started)return;started=true;hero.classList.add('ss23-doors-finished');video.play().catch(()=>{video.controls=true;video.setAttribute('aria-label','Play Dominique’s introduction video')})}
 function reveal(){hero.classList.add('ss23-opening');if(matchMedia('(prefers-reduced-motion: reduce)').matches){play();return}setTimeout(play,1250)}
 if(video.readyState>=2)reveal();else{video.addEventListener('loadeddata',reveal,{once:true});video.addEventListener('error',()=>{hero.classList.add('ss23-doors-finished');video.controls=true},{once:true})}
 // Resume at the existing position after tab suspension; never reset the timeline.
 document.addEventListener('visibilitychange',()=>{if(!document.hidden&&started&&video.paused&&!video.controls)video.play().catch(()=>{video.controls=true})});
})();
