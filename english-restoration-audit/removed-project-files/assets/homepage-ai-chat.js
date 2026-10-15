/* Adds an optional real AI conversation inside the existing homepage dialog. */
(()=>{'use strict';
let cfg,englishUI,session=null,messages=[],lang='en',pending=false;
const base=new URL('.',document.baseURI),home=!!document.querySelector('main.ss22-home');if(!home)return;
Promise.all([fetch(new URL('assets/translation-config.json',base)).then(r=>r.json()),fetch(new URL('assets/homepage-chat-ui.json',base)).then(r=>r.json())]).then(([c,u])=>{cfg=c;englishUI=u}).catch(()=>{});
function endpoint(path){return new URL(path,cfg.chatEndpoint.endsWith('/')?cfg.chatEndpoint:cfg.chatEndpoint+'/')}
function ui(){return window.DommyDomHomepage?.pack?.ui||englishUI}
let currentDialog;
window.DommyDomAI={open({dialog,stage,intro,trigger,details,activeCTA}){
 const state=window.DommyDomHomepage;lang=state?.language||'en';cfg=state?.config||cfg;if(!cfg?.chatEndpoint||!cfg.verifiedChatLanguages?.includes(lang)||!ui())return false;
 const strings=ui();currentDialog=dialog;session=null;messages=[];pending=false;dialog.lang=lang;dialog.dir=['fa','ar'].includes(lang)?'rtl':'ltr';dialog.querySelector('.sunConversation__title').textContent=strings.title;dialog.querySelector('.sunConversation__close').setAttribute('aria-label',strings.close);intro.hidden=true;stage.replaceChildren();
 const log=document.createElement('div');log.className='dd-home-ai-log';log.setAttribute('role','log');log.setAttribute('aria-live','polite');const form=document.createElement('form');form.className='dd-home-ai-form';form.noValidate=true;const input=document.createElement('textarea');input.maxLength=2000;input.rows=2;input.placeholder=strings.placeholder;input.setAttribute('aria-label',strings.message);const send=document.createElement('button');send.type='submit';send.textContent=strings.send;form.append(input,send);const status=document.createElement('p');status.className='dd-home-ai-status';status.setAttribute('role','status');const consent=document.createElement('p');consent.className='dd-home-ai-status';consent.textContent=strings.consent;const lead=document.createElement('button');lead.type='button';lead.className='dd-home-ai-lead';lead.textContent=strings.sendInquiry;lead.hidden=true;stage.append(log,form,status,consent,lead);consent.hidden=true;
 function bubble(role,text){const p=document.createElement('p');p.className='dd-home-ai-message';p.dataset.role=role;p.dir=dialog.dir;p.textContent=text;log.append(p);log.scrollTop=log.scrollHeight;}
 bubble('assistant',strings.welcome);
 form.addEventListener('submit',async e=>{e.preventDefault();const text=input.value.trim();if(pending)return;if(!text){status.textContent=strings.required;return;}pending=true;send.disabled=true;status.textContent=strings.thinking;const oldValue=input.value;input.value='';bubble('user',text);
 try{const r=await fetch(endpoint('chat'),{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({language:lang,session,message:text,context:{page:'index.html',cta:activeCTA||'',details:details||[]}}),signal:AbortSignal.timeout(30000)});if(!r.ok)throw Error();const data=await r.json();if(typeof data.reply!=='string'||!data.session)throw Error();session=data.session;bubble('assistant',data.reply);messages.push({role:'user',text},{role:'assistant',text:data.reply});lead.hidden=!data.leadReady;consent.hidden=!data.leadReady;status.textContent='';}catch{status.textContent=strings.unavailable;input.value=oldValue;}finally{pending=false;send.disabled=false;input.focus();}});
 lead.addEventListener('click',async()=>{if(!session||pending)return;lead.disabled=true;try{const r=await fetch(endpoint('lead'),{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session,language:lang,consent:true}),signal:AbortSignal.timeout(20000)});if(!r.ok)throw Error();const data=await r.json();if(data.delivered!==true)throw Error();status.textContent=strings.leadSent;lead.hidden=true;consent.hidden=true;}catch{status.textContent=strings.leadFailed;lead.disabled=false;}});
 return true;
}};
document.addEventListener('dd-home-language',()=>{session=null;messages=[];if(currentDialog?.open)currentDialog.close();});
})();
