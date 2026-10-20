const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const source=fs.readFileSync('assets/multilingual.js','utf8');
function boot(language,catalog){
  let observer,assignments=[],writes=0;
  const element=()=>({nodeType:1,childNodes:[],attributes:{},append(){},add(){},addEventListener(name,fn){this[name]=fn},matches(){return false},hasAttribute(name){return name in this.attributes},getAttribute(name){return this.attributes[name]},setAttribute(name,value){this.attributes[name]=value}});
  const text={nodeType:3,parentElement:{closest(){return false}},value:'Dominique',get textContent(){return this.value},set textContent(value){writes++;this.value=value}};
  const body=element();body.childNodes=[text];
  let select;
  const cfg={language,path:'blog-new.html',languages:{en:'English',es:'Español',fa:'فارسی',hy:'Հայերեն','zh-CN':'简体中文',ko:'한국어',tl:'Tagalog',te:'తెలుగు',ru:'Русский',ar:'العربية'}};
  const document={body,getElementById(){return {textContent:JSON.stringify(cfg)}},querySelector(){return {insertAdjacentElement(){}}},createElement(tag){const el=element();if(tag==='select')select=el;return el}};
  const context={document,window:{DOMMYDOM_TRANSLATIONS:catalog},Node:{TEXT_NODE:3,ELEMENT_NODE:1},Option:function(name,value){this.name=name;this.value=value},MutationObserver:class{constructor(fn){observer=fn}observe(){}},localStorage:{getItem(){return language},setItem(){}},location:{search:'',hash:'',assign(value){assignments.push(value)},replace(value){assignments.push(value)}},URLSearchParams};
  vm.runInNewContext(source,context);
  return {text,select,get writes(){return writes},observer,assignments};
}
const unchanged=boot('es',{Dominique:'Dominique'});
assert.equal(unchanged.writes,0,'unchanged proper names must not trigger an observer loop');
unchanged.observer([{type:'characterData',target:unchanged.text}]);
assert.equal(unchanged.writes,0);
const translated=boot('es',{Dominique:'Traducido'});
assert.equal(translated.text.textContent,'Traducido');
translated.observer([{type:'characterData',target:translated.text}]);
assert.equal(translated.writes,1,'translated nodes must not be repeatedly rewritten');
for(const language of ['en','es','fa','hy','zh-CN','ko','tl','te','ru','ar']){
  const view=boot('es',{});view.select.value=language;view.select.change();
  assert.equal(view.assignments[0],(language==='en'?'/':'/'+language+'/')+'blog-new.html');
}
assert(!source.includes('fetch('),'static locale runtime must not request translations');
let Processor;
vm.runInNewContext(fs.readFileSync('assets/multilingual-pcm.js','utf8'),{AudioWorkletProcessor:class{constructor(){this.port={postMessage:buffer=>{const samples=new Int16Array(buffer);assert.equal(samples[0],32767);assert.equal(samples[1],-32768)}}}},registerProcessor(name,type){Processor=type}});
const processor=new Processor();const frame=new Float32Array(1600);frame[0]=2;frame[1]=-2;assert.equal(processor.process([[frame]]),true);
console.log('Browser runtime checks passed: ten language routes, stable mutations, no paid browsing calls, bounded PCM encoding.');
