/* Authenticated adapter for the existing contact interface. No calls run on page load.
   The deployed identity integration supplies getToken; credentials are never embedded. */
window.DommyDomCommunications=class {
  constructor({api,room,getToken,language='en',onEvent=()=>{}}){
    const url=new URL(api);if(url.protocol!=='https:')throw new Error('HTTPS required');
    Object.assign(this,{api:api.replace(/\/$/,''),room,getToken,language,onEvent});
  }
  async request(path,body){
    const response=await fetch(this.api+path,{method:body?'POST':'GET',headers:{Authorization:'Bearer '+await this.getToken(),'Content-Type':'application/json'},...(body?{body:JSON.stringify(body)}:{})});
    if(!response.ok)throw new Error('Communication service unavailable ('+response.status+')');return response.json();
  }
  send(text,id=crypto.randomUUID()){return this.request('/rooms/'+this.room+'/messages',{id,text,language:this.language})}
  history(){return this.request('/rooms/'+this.room+'/messages')}
  preference(language){this.language=language;return this.request('/rooms/'+this.room+'/language',{language})}
  async speak(id){const result=await this.request('/rooms/'+this.room+'/messages/'+id+'/speak',{});if(result.audio)return this.play(result.audio);if(result.text&&!this.browserVoice(result.text,result.locale))this.onEvent({type:'captions-only',text:result.text});return result}
  async play(audio){const player=new Audio('data:audio/mp3;base64,'+audio);try{await player.play()}catch{this.onEvent({type:'playback-permission-required',player})}}
  browserVoice(text,locale){const voice=speechSynthesis.getVoices().find(v=>v.lang===locale);if(!voice)return false;const utterance=new SpeechSynthesisUtterance(text);utterance.voice=voice;speechSynthesis.speak(utterance);return true}
  async capture(onChunk){
    this.stream=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true,noiseSuppression:true,channelCount:1}});
    this.context=new AudioContext({sampleRate:16000});await this.context.resume();
    if(this.context.sampleRate!==16000){await this.stop();throw new Error('16kHz microphone capture unavailable')}
    await this.context.audioWorklet.addModule('/assets/multilingual-pcm.js');
    this.input=this.context.createMediaStreamSource(this.stream);this.processor=new AudioWorkletNode(this.context,'dommydom-pcm');
    this.processor.port.onmessage=e=>onChunk(e.data);this.input.connect(this.processor);this.processor.connect(this.context.destination);
  }
  async startCall(){
    const token=await this.getToken();this.socket=new WebSocket(this.api.replace(/^https:/,'wss:')+'/rooms/'+this.room+'/call');
    await new Promise((resolve,reject)=>{this.socket.onopen=resolve;this.socket.onerror=reject});
    this.socket.send(JSON.stringify({token}));
    this.socket.onmessage=event=>{const data=JSON.parse(event.data);this.onEvent(data);if(data.type==='audio'&&data.audio)this.play(data.audio);if((data.type==='audio-unavailable'||data.fallback)&&data.text)this.browserVoice(data.text,data.locale);if(data.type==='segment-ended')this.stop()};
    this.socket.onclose=()=>this.stop();
    try{await this.capture(buffer=>{if(this.socket?.readyState===WebSocket.OPEN&&this.socket.bufferedAmount<64000)this.socket.send(buffer);else this.onEvent({type:'network-delay'})})}catch(error){await this.stop();throw error}
  }
  async startRecording(){this.chunks=[];this.recordedBytes=0;await this.capture(buffer=>{if(this.recordedBytes+buffer.byteLength>1920000)return;this.chunks.push(new Uint8Array(buffer));this.recordedBytes+=buffer.byteLength});this.timer=setTimeout(()=>this.stop(),60000)}
  async sendRecording(id=crypto.randomUUID()){
    await this.stop();const bytes=new Uint8Array(this.recordedBytes);let offset=0;for(const chunk of this.chunks){bytes.set(chunk,offset);offset+=chunk.length}
    let binary='';for(let i=0;i<bytes.length;i+=8192)binary+=String.fromCharCode(...bytes.subarray(i,i+8192));
    return this.request('/rooms/'+this.room+'/voice',{id,language:this.language,pcm_base64:btoa(binary)});
  }
  async stop(){clearTimeout(this.timer);this.stream?.getTracks().forEach(track=>track.stop());this.processor?.disconnect();this.input?.disconnect();if(this.context&&this.context.state!=='closed')await this.context.close();if(this.socket&&this.socket.readyState<2)this.socket.close()}
  mount(target=document.querySelector('.contactPageForm')?.parentElement){
    if(!target)throw new Error('Contact interface unavailable');
    const t=window.dommydomTranslateSaved||((text)=>text);
    const panel=document.createElement('section');panel.className='dd-communications';
    const heading=document.createElement('h3');heading.textContent=t('Messages and voice');
    const log=document.createElement('div');log.setAttribute('aria-live','polite');log.className='dd-communication-status';
    const input=document.createElement('textarea');input.setAttribute('aria-label',t('Your message'));input.maxLength=10000;
    const status=document.createElement('p');status.setAttribute('role','status');
    const button=(label,action)=>{const item=document.createElement('button');item.type='button';item.textContent=t(label);item.addEventListener('click',async()=>{item.disabled=true;status.textContent='';try{await action()}catch{status.textContent=t('Communication unavailable. Please try again.')}finally{item.disabled=false}});return item};
    const render=async()=>{const history=await this.history();log.replaceChildren();for(const item of history.messages.reverse()){const row=document.createElement('p');const text=item.translations?.[this.language]||item.original;row.textContent=new Date(item.created).toLocaleString()+' — '+text;const original=document.createElement('details');const summary=document.createElement('summary');summary.textContent=t('Original message');const copy=document.createElement('p');copy.textContent=item.original;original.append(summary,copy);row.append(original,button('Listen',()=>this.speak(item.id)));log.append(row)}};
    const prior=this.onEvent;
    this.onEvent=event=>{prior(event);if(event.text)status.textContent=event.text;if(event.type==='error')status.textContent=t('Voice translation unavailable.');if(event.type==='segment-ended')status.textContent=t('Call segment ended. Select Start translated call to continue.')};
    const language=document.createElement('select');language.setAttribute('aria-label',t('Language'));
    const names={en:'English',es:'Español',fa:'فارسی',hy:'Հայերեն','zh-CN':'简体中文',ko:'한국어',tl:'Tagalog',te:'తెలుగు',ru:'Русский',ar:'العربية'};
    for(const [code,name]of Object.entries(names))language.add(new Option(name,code,code===this.language,code===this.language));
    language.addEventListener('change',async()=>{try{await this.preference(language.value);await render()}catch{status.textContent=t('Language preference could not be saved.')}});
    panel.append(heading,language,log,input,button('Send message',async()=>{await this.send(input.value);input.value='';await render()}),button('Refresh messages',render),button('Record voice message',()=>this.startRecording()),button('Send voice message',async()=>{await this.sendRecording();await render()}),button('Start translated call',()=>this.startCall()),button('Stop',()=>this.stop()),status);
    target.append(panel);render().catch(()=>{status.textContent=t('Sign in to view your messages.')});return panel;
  }
};
