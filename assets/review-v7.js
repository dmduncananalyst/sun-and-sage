(()=>{
 const box=document.querySelector('[data-v7-down-payment]');if(!box)return;
 const price=box.querySelector('[name=illustrationPrice]'),percent=box.querySelector('[name=illustrationDown]');
 const money=n=>new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0}).format(n);
 function update(){
  const amount=Number(price.value),pct=Number(percent.value),valid=Number.isFinite(amount)&&amount>0&&amount<=100000000&&Number.isFinite(pct)&&pct>=0&&pct<=40;
  box.querySelector('.v7-chart-error').textContent=valid?'':'Enter a purchase price between $1 and $100,000,000.';
  price.setAttribute('aria-invalid',String(!valid));
  box.querySelector('[data-v7-percent]').textContent=pct+'%';
  box.querySelector('[data-v7-donut-value]').textContent=pct+'%';
  box.querySelector('.v7-donut').style.setProperty('--down',pct+'%');
  box.querySelector('[data-v7-cash]').textContent=valid?money(amount*pct/100):'—';
  box.querySelector('[data-v7-loan]').textContent=valid?money(amount*(1-pct/100)):'—';
  box.querySelectorAll('[data-v7-set-down]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.v7SetDown)===pct)));
 }
 box.querySelectorAll('[data-v7-set-down]').forEach(b=>b.addEventListener('click',()=>{percent.value=b.dataset.v7SetDown;update()}));
 price.addEventListener('input',update);percent.addEventListener('input',update);update();
})();
