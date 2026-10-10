/* Sun and Sage journal: self-contained navigation and budget controls. */
(()=>{
  const progress=document.querySelector('.reading-progress span');
  if(progress){const update=()=>{const d=Math.max(1,document.documentElement.scrollHeight-innerHeight);progress.style.width=Math.min(100,Math.max(0,100*scrollY/d))+'%';};addEventListener('scroll',update,{passive:true});update();}
  const income=document.querySelector('#monthly-income');
  const fields=[...document.querySelectorAll('.category-input')];
  if(!income||!fields.length)return;
  const initial=[income,...fields].map(e=>e.defaultValue);
  const money=n=>new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0}).format(n);
  const read=el=>Math.max(0,Number(el.value)||0);
  const update=()=>{
    const total=fields.reduce((n,el)=>n+read(el),0), net=read(income),remain=net-total;
    const text=(id,value)=>{const el=document.getElementById(id);if(el)el.textContent=value;};
    text('remaining-amount',money(remain));text('assigned-amount',money(total));
    text('savings-amount',money(read(document.querySelector('[name="savings"]')||{value:0})));
    text('budget-feedback',remain===0?'Every dollar has a purpose.':remain>0?'Give the remaining dollars a job.':'Your assignments exceed your income.');
    const stack=document.querySelector('#stackbar');if(stack){stack.textContent='';fields.forEach((field,i)=>{const part=document.createElement('span');part.style.width=(total?100*read(field)/total:0)+'%';part.style.backgroundColor=['#c8a579','#8c9b86','#6e827a','#a0b29d','#a07d65','#e0cda9','#6a726a','#b89b85'][i%8];part.title=field.getAttribute('aria-label')+': '+money(read(field));stack.appendChild(part);});}
    const list=document.querySelector('#budget-breakdown');if(list){list.textContent='';fields.forEach(field=>{const row=document.createElement('div');const name=document.createElement('span');name.textContent=field.getAttribute('aria-label')?.replace(/ amount$/,'')||field.name;const sum=document.createElement('strong');sum.textContent=money(read(field));row.append(name,sum);list.appendChild(row);});}
  };
  [income,...fields].forEach(el=>el.addEventListener('input',update));
  document.querySelector('#reset-budget')?.addEventListener('click',()=>{[income,...fields].forEach((el,i)=>el.value=initial[i]);update();});
  update();
})();
