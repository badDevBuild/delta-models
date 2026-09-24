import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { disposeModel } from './assembly.js';

export class LatestModelLoader {
  constructor({fetcher=(...args)=>globalThis.fetch(...args),parser=new GLTFLoader()}={}) {this.fetcher=fetcher;this.parser=parser;this.serial=0;this.controller=null;}
  cancel() {this.serial++;this.controller?.abort();}
  async load(url,onProgress=()=>{}) {
    this.cancel();
    const serial=this.serial;
    const controller=new AbortController();this.controller=controller;
    const response=await this.fetcher(url,{signal:controller.signal});
    if(!response.ok) throw new Error(`模型请求失败（HTTP ${response.status}）`);
    const total=Number(response.headers.get('content-length'))||0;
    let data;
    if(response.body?.getReader) {
      const reader=response.body.getReader(),chunks=[];let received=0;
      while(true) {
        const {done,value}=await reader.read();if(done)break;
        chunks.push(value);received+=value.byteLength;
        if(serial===this.serial)onProgress({received,total,percent:total?Math.min(100,received/total*100):null});
      }
      const bytes=new Uint8Array(received);let offset=0;
      for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.byteLength;}
      data=bytes.buffer;
    } else data=await response.arrayBuffer();
    if(serial!==this.serial)return null;
    const base=new URL('.',new URL(url,globalThis.location?.href||'http://localhost/')).href;
    const gltf=await this.parser.parseAsync(data,base);
    if(serial!==this.serial){disposeModel(gltf.scene);return null;}
    onProgress({received:data.byteLength,total:data.byteLength,percent:100});
    return gltf;
  }
}
