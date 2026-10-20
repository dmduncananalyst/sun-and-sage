class DommyDomPCM extends AudioWorkletProcessor {
  constructor(){super();this.samples=new Int16Array(1600);this.offset=0}
  process(inputs){
    const input=inputs[0]?.[0];if(!input)return true;
    for(const value of input){this.samples[this.offset++]=Math.round(Math.max(-1,Math.min(1,value))*(value<0?32768:32767));if(this.offset===this.samples.length){this.port.postMessage(this.samples.buffer,[this.samples.buffer]);this.samples=new Int16Array(1600);this.offset=0}}
    return true;
  }
}
registerProcessor('dommydom-pcm',DommyDomPCM);
