(()=>{'use strict';
document.querySelectorAll('.loanFlip').forEach(card=>{
 const toggle=()=>{const active=card.classList.toggle('ss21-flipped');card.setAttribute('aria-pressed',String(active));card.setAttribute('aria-label',active?'Show question':'Show answer')};
 card.addEventListener('click',toggle);
 card.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();toggle()}});
});
})();
