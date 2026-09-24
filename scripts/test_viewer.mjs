import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {GLTFLoader} from '../web/node_modules/three/examples/jsm/loaders/GLTFLoader.js';
import {Vector3} from '../web/node_modules/three/build/three.module.js';
import {Assembly} from '../web/src/assembly.js';
import {LatestModelLoader} from '../web/src/model-loader.js';

const project=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const requested=process.argv.slice(2);
const registry=JSON.parse(await readFile(path.join(project,'config/models.json'),'utf8'));
const modelPaths=requested.length?requested:registry.models.map(({id})=>path.join(project,'web/public/models',`${id}.glb`));
const checks=[];
const record=(name,data={})=>checks.push({name,passed:true,...data});
const binary=async file=>{const data=await readFile(file);return data.buffer.slice(data.byteOffset,data.byteOffset+data.byteLength);};
const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));

for(const file of modelPaths){
  const id=path.basename(file,'.glb'),buffer=await binary(file);
  const gltf=await new GLTFLoader().parseAsync(buffer,'');
  if(['uzi','thompson'].includes(id)){
    const walnut=[];
    gltf.scene.traverse(o=>{if(o.isMesh)for(const m of [].concat(o.material))if(m.name.includes('Warm walnut'))walnut.push(m);});
    assert(walnut.length>0,`${id} must retain its wood material`);
    for(const m of walnut)assert(m.map||(m.color.r>m.color.g&&m.color.g>m.color.b&&m.color.r<.5),`${id} wood cannot fall back to white when procedural Blender nodes are exported`);
    record(`${id}: wood has a portable texture or brown PBR fallback`);
  }
  const beforeColors=[];gltf.scene.traverse(o=>{if(o.isMesh)for(const m of [].concat(o.material))if(m.color)beforeColors.push(m.color.toArray());});
  const model=new Assembly(gltf.scene);
  assert(model.parts.size>=2,`${id} needs multiple logical parts`);assert(model.meshCount>0);assert(model.triangleCount>100);
  const partRoots=new Set([...model.parts.values()].map(part=>part.object));
  for(const part of model.parts.values()){
    assert(!part.object.isMesh,`${id}/${part.id} is an EMPTY/group, never a surfaces mesh`);
    let ancestor=part.object.parent;while(ancestor){assert(!partRoots.has(ancestor),`${id}/${part.id} cannot be nested in another assembly part`);ancestor=ancestor.parent;}
  }
  try{
    const manifest=JSON.parse(await readFile(path.join(project,'assets',id,'manifest.json'),'utf8'));
    assert.deepEqual([...model.parts.keys()].sort(),manifest.parts.map(p=>p.id.replace(/^part_/,'')).sort(),`${id} component IDs must match the authoritative Blender manifest`);
    record(`${id}: non-nested group roots match authoritative Blender manifest`,{parts:model.parts.size});
  }catch(error){if(error.code!=='ENOENT'||!requested.length)throw error;}
  const box=model.visibleBounds(),size=box.getSize(new Vector3());
  assert(Math.abs(Math.max(size.x,size.y,size.z)-3)<1e-5,`${id} default bounds must normalize to 3`);
  const afterColors=[];gltf.scene.traverse(o=>{if(o.isMesh)for(const m of [].concat(o.material))if(m.color)afterColors.push(m.color.toArray());});
  assert.deepEqual(afterColors,beforeColors,`${id} original material colors are preserved`);
  record(`${id}: real GLB hierarchy, normalization and colors`,{parts:model.parts.size,meshes:model.meshCount,triangles:model.triangleCount});

  const enabled=[...model.parts.keys()].filter(key=>model.enabled(key));
  const chosen=enabled.find(key=>/magazine|grip|stock|slide/.test(key))||enabled.at(-1);
  const part=model.parts.get(chosen),origin=part.origin.clone(),worldOrigin=part.object.getWorldPosition(new Vector3());
  model.select(chosen);assert.equal(model.selected,chosen);
  model.toggleDetached();model.update(1,true);assert(part.object.position.distanceTo(origin)>0,`${id} detach changes actual transform`);
  const worldOffset=part.object.getWorldPosition(new Vector3()).sub(worldOrigin);
  assert(worldOffset.distanceTo(part.direction.clone().multiplyScalar(.8))<1e-8,`${id} export unit/parent transforms preserve intended world movement`);
  model.toggleDetached();model.update(1,true);assert(part.object.position.distanceTo(origin)<1e-10,`${id} reattach restores actual transform`);
  model.toggleHidden(chosen);assert.equal(part.object.visible,false);model.toggleHidden(chosen);assert.equal(part.object.visible,true);
  model.toggleIsolate();assert.equal([...model.parts.values()].filter(p=>p.object.visible).length,1);assert(part.object.visible);
  model.toggleIsolate();assert.equal([...model.parts.values()].filter(p=>p.object.visible).length,enabled.length);
  model.setExplosion(1);model.update(1,true);assert(part.object.position.distanceTo(origin)>0);assert(!model.visibleBounds().isEmpty());
  record(`${id}: selection, detach/reattach, hide, isolate and explosion mutate real scene`);

  const defaults=[...model.parts].map(([key,p])=>[key,p.config.defaultVisible]);
  for(const [group,defaultValue] of model.groups){
    const variants=[...model.parts.values()].filter(p=>p.config.group===group);
    for(const variant of variants){model.setVariant(group,variant.config.value);assert.equal(variants.filter(p=>model.enabled(p.id)).length,1);assert(model.enabled(variant.id));}
    model.setVariant(group,defaultValue);
  }
  for(const [key,p] of model.parts)if(p.config.optional){model.setOptional(key,true);assert(model.enabled(key));model.setOptional(key,false);assert(!model.enabled(key));}
  model.reset();model.update(1,true);assert.equal(model.explosion,0);assert.equal(model.selected,null);assert.equal(model.hidden.size,0);assert.equal(model.detached.size,0);
  for(const [key,p] of model.parts){assert(p.object.position.distanceTo(p.origin)<1e-10);assert.equal(model.enabled(key),defaults.find(([n])=>n===key)[1],`${id}/${key} reset restores default visibility`);}
  record(`${id}: mutually exclusive variants, optional attachments and full reset`);

  const geometries=new Set(),materials=new Set();let disposedGeometry=0,disposedMaterial=0;
  model.root.traverse(o=>{if(o.geometry)geometries.add(o.geometry);for(const m of [].concat(o.material||[]))materials.add(m);});
  for(const geometry of geometries)geometry.addEventListener('dispose',()=>disposedGeometry++);
  for(const material of materials)material.addEventListener('dispose',()=>disposedMaterial++);
  const disposed=model.dispose();assert.equal(disposedGeometry,geometries.size);assert.equal(disposedMaterial,materials.size);assert.equal(model.wrapper.parent,null);
  record(`${id}: all model geometry/material dispose events observed`,disposed);
}

// Exercise the production request/race module with bytes from an actual GLB.
const bytes=await binary(modelPaths[0]);
const pending=[];
const fetcher=async(url,{signal})=>{
  if(url.includes('slow'))await new Promise((resolve,reject)=>{const timer=setTimeout(resolve,40);signal.addEventListener('abort',()=>{clearTimeout(timer);reject(new DOMException('aborted','AbortError'));},{once:true});});
  return new Response(bytes.slice(0),{status:200,headers:{'content-length':String(bytes.byteLength)}});
};
const loading=new LatestModelLoader({fetcher});let progress=0;
pending.push(loading.load('http://localhost/slow.glb').catch(e=>e.name));
const winner=await loading.load('http://localhost/fast.glb',p=>progress=p.percent);
assert.equal(await pending[0],'AbortError');assert(winner.scene);assert.equal(progress,100);
const winningModel=new Assembly(winner.scene);winningModel.dispose();record('latest request aborts prior network transfer; actual winning GLB parsed; progress reaches 100');

let parsedOld,wasDisposed=0,releaseOld;
const parser={parseAsync:async(data,base)=>{const result=await new GLTFLoader().parseAsync(data,base);if(!parsedOld){parsedOld=result;result.scene.traverse(o=>{o.geometry?.addEventListener('dispose',()=>wasDisposed++);});await new Promise(resolve=>releaseOld=resolve);}return result;}};
const racing=new LatestModelLoader({fetcher,parser});const old=racing.load('http://localhost/old.glb');
while(!releaseOld)await delay(1);
const fresh=await racing.load('http://localhost/new.glb');releaseOld();assert.equal(await old,null);assert(wasDisposed>0);new Assembly(fresh.scene).dispose();record('out-of-order GLB parsing cannot replace current asset; stale geometry disposed');

const missing=new LatestModelLoader({fetcher:async()=>new Response('missing',{status:404})});await assert.rejects(missing.load('http://localhost/no.glb'),/404/);record('HTTP failure propagates to recoverable UI path');
const output=path.join(project,'output/viewer-validation.json');await mkdir(path.dirname(output),{recursive:true});await writeFile(output,JSON.stringify({checkedAt:new Date().toISOString(),scope:'Node tests on real GLBs and the production Assembly/LatestModelLoader modules; no browser/WebGL claim',passed:true,models:modelPaths.map(p=>path.basename(p)),checks},null,2)+'\n');
console.log(JSON.stringify({passed:true,checks:checks.length,models:modelPaths.map(p=>path.basename(p)),output},null,2));
