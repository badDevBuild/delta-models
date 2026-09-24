import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { Assembly,disposeModel } from './assembly.js';
import { LatestModelLoader } from './model-loader.js';
import {formatMeasure,setModelWireframe} from './view-options.js';
import {loadGameGuides,renderGameGuide} from './game-guide.js';
import './style.css';

const $=id=>document.getElementById(id);
const downloadBase=(import.meta.env.VITE_DOWNLOAD_BASE_URL||'').replace(/\/$/,'');
const stage=$('viewer'), reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
const scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(33,1,.01,100);
const loader=new LatestModelLoader();
let renderer,controls,environmentTarget,assembly,catalog,currentModel,loadSerial=0,cameraTween=null,currentView='perspective',lastTime=performance.now();
let ready=false,disposedModels=0,resizeObserver;
let wireframe=false;
const variantGroupNames={barrel:'前端长度',stock:'尾部样式'};
const variantValueNames={short:'基础短款',long:'配件长款'};

function textElement(tag,className,text){const element=document.createElement(tag);if(className)element.className=className;element.textContent=text;return element;}
function normalizeEntry(entry,index){return {...entry,id:String(entry.id),name:entry.name||String(entry.id).toUpperCase(),index,model:entry.model||`/models/${entry.id}.glb`,preview:entry.preview||`/previews/${entry.id}.png`,downloads:entry.downloads||{}};}
function showLoading(title,message,failed=false){$('loading').hidden=false;$('loading').classList.toggle('error',failed);$('load-title').textContent=title;$('load-message').textContent=message;$('load-progress').hidden=failed;$('load-progress').removeAttribute('value');$('retry').hidden=!failed;}
function setReady(value){ready=value;for(const id of ['explode','assemble','autorotate','view-perspective','view-side','view-top','zoom-in','zoom-out','reset-view','wireframe'])$(id).disabled=!value;if(!value){$('detach').disabled=true;$('isolate').disabled=true;}updateModelNavigation();}
function updateLink(id,path){const link=$(id);if(path){link.href=downloadBase&&path.startsWith('/downloads/')?`${downloadBase}/${path.slice('/downloads/'.length)}`:path;link.removeAttribute('aria-disabled');link.removeAttribute('tabindex');}else{link.removeAttribute('href');link.setAttribute('aria-disabled','true');link.tabIndex=-1;}}

function filterCatalog(){
  if(!catalog)return;
  const query=$('catalog-search').value.trim().toLocaleLowerCase(),category=$('catalog-category').value;
  let visible=0;
  for(const entry of catalog.models){
    const card=$('catalog').querySelector(`[data-model="${entry.id}"]`);
    const matches=(!query||`${entry.name} ${entry.category} ${entry.id}`.toLocaleLowerCase().includes(query))&&(category==='all'||entry.category===category);
    card.hidden=!matches;if(matches)visible++;
  }
  $('catalog-matches').textContent=`${visible} / ${catalog.models.length} 款`;
  $('catalog-empty').hidden=visible>0;
  updateModelNavigation();
}
function visibleModels(){return catalog?.models.filter(entry=>!$('catalog').querySelector(`[data-model="${entry.id}"]`)?.hidden)||[];}
function updateModelNavigation(){const multiple=ready&&visibleModels().length>1;$('previous-model').disabled=$('next-model').disabled=!multiple;}
function navigateModel(step){
  const models=visibleModels();if(models.length<2)return;
  const index=models.findIndex(entry=>entry.id===currentModel?.id);
  const next=index<0?(step>0?0:models.length-1):(index+step+models.length)%models.length;
  loadModel(models[next]);
  $('catalog').querySelector(`[data-model="${models[next].id}"]`)?.scrollIntoView({block:'nearest',inline:'nearest'});
}
$('catalog-search').addEventListener('input',()=>{$('catalog-filter-note').hidden=true;filterCatalog();});
function changeCatalogFilter(){
  const note=$('catalog-filter-note');note.hidden=true;note.textContent='';
  filterCatalog();
  if(!visibleModels().length&&$('catalog-search').value){
    $('catalog-search').value='';
    note.textContent='当前条件没有匹配的搜索词，已清除搜索。';note.hidden=false;
    filterCatalog();
  }
  const selected=visibleModels().find(entry=>entry.id===currentModel?.id);
  if(!selected&&visibleModels().length)loadModel(visibleModels()[0]);
  else if(selected)commitUrl(selected,'push');
}
$('catalog-category').addEventListener('change',changeCatalogFilter);
$('previous-model').onclick=()=>navigateModel(-1);
$('next-model').onclick=()=>navigateModel(1);

function renderCatalog(){
  $('catalog').replaceChildren();
  for(const entry of catalog.models){
    const card=document.createElement('button');card.className='catalog-card';card.dataset.model=entry.id;card.setAttribute('aria-label',`查看 ${entry.name} ${entry.category||'装饰模型'}`);card.setAttribute('aria-pressed','false');
    card.append(textElement('span','card-name',entry.name));
    const image=document.createElement('img');image.src=entry.preview;image.alt='';image.loading='lazy';image.decoding='async';image.onerror=()=>image.classList.add('image-missing');card.append(image,textElement('span','card-category',entry.category||'外观装饰模型'));
    card.addEventListener('click',()=>loadModel(entry));$('catalog').append(card);
  }
  $('model-total').textContent=String(catalog.models.length).padStart(2,'0');
  $('catalog-category').replaceChildren();
  for(const category of ['all',...[...new Set(catalog.models.map(entry=>entry.category))].filter(Boolean)]){
    const option=textElement('option','',category==='all'?'全部类别':category);option.value=category;$('catalog-category').append(option);
  }
  const requestedCategory=new URLSearchParams(location.search).get('category');
  if([...$('catalog-category').options].some(option=>option.value===requestedCategory))$('catalog-category').value=requestedCategory;
  filterCatalog();
}
function renderEntry(entry){
  for(const card of $('catalog').children){const active=card.dataset.model===entry.id;card.classList.toggle('active',active);card.setAttribute('aria-pressed',String(active));}
  $('model-name').textContent=$('stage-word').textContent=entry.name;
  $('model-category').textContent=entry.category||'外观装饰模型';
  $('model-index').textContent=String(entry.index+1).padStart(2,'0');
  const printed=entry.status?.physical?.state==='passed'?'已实机验证':'未实机打印';
  $('model-size').textContent=entry.lengthMm?`数字模型约 ${formatMeasure(Number(entry.lengthMm)/10)} 厘米 · 非功能性 · ${printed}`:`非功能性缩比模型 · ${printed}`;
  $('model-description').textContent=entry.description||`${entry.name} 外观模型。旋转查看轮廓，选择组件探索细节。`;
  $('model-note').hidden=!entry.note;$('model-note').textContent=entry.note||'';
  renderGameGuide(entry.id);
  updateLink('download-print',entry.downloads?.print);updateLink('download-blend',entry.downloads?.blend);
  updateLink('download-sliced',entry.downloads?.sliced);$('download-sliced').hidden=!entry.downloads?.sliced;
  document.title=`${entry.name} · DELTA MODELS 模型收藏馆`;
  updateModelNavigation();
}
function commitUrl(entry,mode){
  if(mode==='none')return;
  const url=new URL(location.href);
  url.searchParams.delete('batch');
  const category=$('catalog-category').value;
  if(category==='all')url.searchParams.delete('category');else url.searchParams.set('category',category);
  url.searchParams.set('model',entry.id);
  if(mode==='push'&&url.href!==location.href)history.pushState({},'',url);
  else if(mode==='replace')history.replaceState({},'',url);
}
async function loadModel(entry,{historyMode='push'}={}){
  const serial=++loadSerial;currentModel=entry;setReady(false);cameraTween=null;renderEntry(entry);
  if(assembly){assembly.dispose();assembly=null;disposedModels++;renderer?.renderLists.dispose();}
  $('parts-list').replaceChildren();$('parts-count').textContent='—';$('variants').replaceChildren();$('variants-section').hidden=true;$('selection-chip').hidden=true;$('explode').value='0';$('explode-value').textContent='0%';$('component-info').textContent='点击模型或列表选择组件。';wireframe=false;$('wireframe').setAttribute('aria-pressed','false');$('wireframe').textContent='△ 显示三角网格';
  showLoading(`正在载入 ${entry.name}`,'仅加载当前展品，准备几何与材质。');
  let gltf;
  try{
    gltf=await loader.load(entry.model,({received,percent})=>{
      if(serial!==loadSerial)return;
      if(percent!==null){$('load-progress').value=percent;$('load-message').textContent=`已载入 ${Math.round(percent)}% · ${(received/1e6).toFixed(1)} MB`;}
      else $('load-message').textContent=`已接收 ${(received/1e6).toFixed(1)} MB`;
    });
    if(!gltf||serial!==loadSerial)return;
    assembly=new Assembly(gltf.scene);scene.add(assembly.wrapper);setReady(true);$('loading').hidden=true;
    renderVariants();renderAssembly();resize();resetView(true);
    commitUrl(entry,historyMode);
  }catch(error){
    if(serial!==loadSerial||error.name==='AbortError')return;
    if(gltf&&!assembly)disposeModel(gltf.scene);
    setReady(false);showLoading(`${entry.name} 暂时无法显示`,'模型文件可能尚未生成或请求失败。可重试，或选择其他展品。',true);console.error(error);
  }
}

function renderVariants(){
  $('variants').replaceChildren();const groups=new Map();
  for(const part of assembly.parts.values())if(part.config.group){if(!groups.has(part.config.group))groups.set(part.config.group,[]);groups.get(part.config.group).push(part);}
  for(const [name,options] of groups){
    const label=textElement('label','variant-row',variantGroupNames[name]||name);const select=document.createElement('select');select.dataset.variant=name;select.setAttribute('aria-label',variantGroupNames[name]||name);
    for(const part of options){const option=textElement('option','',variantValueNames[part.config.value]||part.label);option.value=part.config.value;select.append(option);}select.value=assembly.groups.get(name);select.onchange=()=>{assembly.setVariant(name,select.value);renderAssembly();fitCurrent();};label.append(select);$('variants').append(label);
  }
  for(const part of assembly.parts.values())if(part.config.optional){
    const label=textElement('label','variant-row',part.label),checkbox=document.createElement('input');checkbox.type='checkbox';checkbox.dataset.optional=part.id;checkbox.checked=assembly.options.has(part.id);checkbox.onchange=()=>{assembly.setOptional(part.id,checkbox.checked);renderAssembly();fitCurrent();};label.append(checkbox);$('variants').append(label);
  }
  $('variants-section').hidden=!$('variants').children.length;
}
function renderAssembly(){
  if(!assembly)return;
  const focusRow=document.activeElement?.closest?.('[data-part]');
  const focusPart=focusRow?.dataset.part;
  const focusEye=document.activeElement?.classList.contains('eye-button');
  $('parts-list').replaceChildren();let index=0;
  for(const [id,part] of assembly.parts){
    if(!assembly.enabled(id))continue;
    const row=textElement('div',`part-row${assembly.selected===id?' selected':''}${!part.object.visible?' invisible':''}`,'');row.dataset.part=id;
    const button=document.createElement('button');button.className='part-button';button.setAttribute('aria-pressed',String(assembly.selected===id));button.append(textElement('span','index',String(++index).padStart(2,'0')),textElement('span','',part.label));
    if(assembly.detached.has(id))button.append(textElement('span','part-detached','已取下'));
    button.onclick=()=>selectPart(id);row.append(button);
    const eye=textElement('button','eye-button',assembly.hidden.has(id)?'○':'◉');eye.setAttribute('aria-label',`${assembly.hidden.has(id)?'显示':'隐藏'}${part.label}`);eye.setAttribute('aria-pressed',String(!assembly.hidden.has(id)));eye.onclick=()=>{assembly.toggleHidden(id);renderAssembly();};row.append(eye);$('parts-list').append(row);
  }
  $('parts-count').textContent=`${index} 组`;
  const selected=assembly.parts.get(assembly.selected);$('selection-chip').hidden=!selected;$('selected-name').textContent=selected?.label||'';
  $('detach').disabled=$('isolate').disabled=!selected;$('detach').textContent=assembly.detached.has(assembly.selected)?'装回组件':'取下组件';$('isolate').textContent=assembly.isolated?'查看全部':'单独查看';
  $('component-info').textContent=selected?(selected.description||`${selected.label} · 外观装饰组件，可取下或单独查看。`):'点击模型或列表选择组件。';
  $('explode').value=Math.round(assembly.explosion*100);$('explode-value').textContent=`${Math.round(assembly.explosion*100)}%`;
  if(focusPart){
    const row=[...$('parts-list').children].find(element=>element.dataset.part===focusPart)||$('parts-list').firstElementChild;
    row?.querySelector(focusEye?'.eye-button':'.part-button')?.focus({preventScroll:true});
  }
}
function stopAutoRotate(){if(!controls)return;controls.autoRotate=false;$('autorotate').setAttribute('aria-pressed','false');}
function selectPart(id){if(!assembly)return;stopAutoRotate();const wasIsolated=assembly.isolated;assembly.select(id);renderAssembly();if(wasIsolated)fitCurrent();}
function setView(name){currentView=name;for(const value of ['perspective','side','top']){$('view-'+value).classList.toggle('active',name===value);$('view-'+value).setAttribute('aria-pressed',String(name===value));}}
function moveCamera(position,target,instant=false){if(instant||reduced){camera.position.copy(position);controls.target.copy(target);controls.update();cameraTween=null;}else cameraTween={from:camera.position.clone(),to:position.clone(),fromTarget:controls.target.clone(),target:target.clone(),start:performance.now()};}
function fittedCamera(direction){
  let bounds=assembly?.visibleBounds();
  if(!bounds||bounds.isEmpty())bounds=new THREE.Box3(new THREE.Vector3(-1.5,-.6,-.3),new THREE.Vector3(1.5,.6,.3));
  const center=bounds.getCenter(new THREE.Vector3());
  const forward=direction.clone().normalize(),right=new THREE.Vector3().crossVectors(camera.up,forward).normalize(),up=new THREE.Vector3().crossVectors(forward,right).normalize();
  if(right.lengthSq()<.001){right.set(1,0,0);up.crossVectors(forward,right).normalize();}
  const halfY=Math.tan(THREE.MathUtils.degToRad(camera.fov*.5)),halfX=halfY*camera.aspect;let distance=.7;
  for(const x of [bounds.min.x,bounds.max.x])for(const y of [bounds.min.y,bounds.max.y])for(const z of [bounds.min.z,bounds.max.z]){
    const p=new THREE.Vector3(x,y,z).sub(center),depth=p.dot(forward);
    distance=Math.max(distance,depth+Math.abs(p.dot(right))/halfX*1.23,depth+Math.abs(p.dot(up))/halfY*1.23);
  }
  return {position:center.clone().addScaledVector(forward,distance),target:center};
}
function fitCurrent(instant=false){if(!controls)return;const direction=camera.position.clone().sub(controls.target).normalize();const frame=fittedCamera(direction);moveCamera(frame.position,frame.target,instant);}
function resetView(instant=false){if(!controls)return;stopAutoRotate();const frame=fittedCamera(new THREE.Vector3(-.20,.18,.96));moveCamera(frame.position,frame.target,instant);setView('perspective');}
function zoom(factor){if(!ready)return;cameraTween=null;camera.position.sub(controls.target).multiplyScalar(factor).add(controls.target);controls.update();}
function resize(){if(!renderer)return;const rect=stage.getBoundingClientRect();if(!rect.width||!rect.height)return;const changed=Math.abs(camera.aspect-rect.width/rect.height)>.07;camera.aspect=rect.width/rect.height;camera.updateProjectionMatrix();renderer.setSize(rect.width,rect.height);if(ready&&changed)fitCurrent(true);}

$('retry').onclick=()=>currentModel?loadModel(currentModel):init();
$('explode').oninput=event=>{if(!assembly)return;stopAutoRotate();assembly.setExplosion(Number(event.target.value)/100);renderAssembly();fitCurrent();};
$('assemble').onclick=()=>{if(!assembly)return;assembly.reset();stopAutoRotate();renderVariants();renderAssembly();resetView();};
$('detach').onclick=()=>{stopAutoRotate();assembly?.toggleDetached();renderAssembly();fitCurrent();};
$('isolate').onclick=()=>{stopAutoRotate();assembly?.toggleIsolate();renderAssembly();fitCurrent();};
$('clear-selection').onclick=()=>selectPart(null);
$('view-perspective').onclick=()=>resetView();
$('view-side').onclick=()=>{stopAutoRotate();const frame=fittedCamera(new THREE.Vector3(0,0,1));moveCamera(frame.position,frame.target);setView('side');};
$('view-top').onclick=()=>{stopAutoRotate();const frame=fittedCamera(new THREE.Vector3(0,1,.001));moveCamera(frame.position,frame.target);setView('top');};
$('wireframe').onclick=()=>{
  if(!ready||!assembly)return;
  wireframe=!wireframe;setModelWireframe(assembly,wireframe);
  $('wireframe').setAttribute('aria-pressed',String(wireframe));
  $('wireframe').textContent=wireframe?'◼ 恢复实体外观':'△ 显示三角网格';
};
$('zoom-in').onclick=()=>zoom(.8);$('zoom-out').onclick=()=>zoom(1.25);$('reset-view').onclick=()=>resetView();
$('autorotate').onclick=()=>{controls.autoRotate=!controls.autoRotate;$('autorotate').setAttribute('aria-pressed',String(controls.autoRotate));};
const raycaster=new THREE.Raycaster(),pointer=new THREE.Vector2();let pointerDown=null;
stage.addEventListener('pointerdown',e=>{pointerDown={x:e.clientX,y:e.clientY,id:e.pointerId,type:e.pointerType};});
stage.addEventListener('pointerup',e=>{
  if(!ready||!pointerDown||pointerDown.id!==e.pointerId||Math.hypot(e.clientX-pointerDown.x,e.clientY-pointerDown.y)>(pointerDown.type==='touch'?12:5))return;
  pointerDown=null;const rect=stage.getBoundingClientRect();pointer.set((e.clientX-rect.left)/rect.width*2-1,-(e.clientY-rect.top)/rect.height*2+1);raycaster.setFromCamera(pointer,camera);
  const roots=[...assembly.parts.values()].filter(p=>p.object.visible).map(p=>p.object);const hit=raycaster.intersectObjects(roots,true)[0];if(!hit)return;
  let object=hit.object;while(object&&(object.isMesh||assembly.parts.get(object.name.slice(5))?.object!==object))object=object.parent;if(object)selectPart(object.name.slice(5));
});
stage.addEventListener('pointercancel',()=>pointerDown=null);
stage.addEventListener('keydown',e=>{if(e.key==='+'||e.key==='='){e.preventDefault();zoom(.85);}if(e.key==='-'){e.preventDefault();zoom(1.18);}if(e.key.toLowerCase()==='r')resetView();if(e.key==='Escape')selectPart(null);});

function animate(time){
  const delta=Math.min((time-lastTime)/1000,.1);lastTime=time;
  if(cameraTween){const amount=Math.min((time-cameraTween.start)/450,1),ease=1-(1-amount)**3;camera.position.lerpVectors(cameraTween.from,cameraTween.to,ease);controls.target.lerpVectors(cameraTween.fromTarget,cameraTween.target,ease);if(amount===1)cameraTween=null;}
  assembly?.update(delta,reduced);controls.update(delta);renderer.render(scene,camera);
}
function initRenderer(){
  renderer=new THREE.WebGLRenderer({antialias:true,alpha:true,powerPreference:'high-performance'});renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=.7;stage.append(renderer.domElement);
  const generator=new THREE.PMREMGenerator(renderer),room=new RoomEnvironment();environmentTarget=generator.fromScene(room,.04);scene.environment=environmentTarget.texture;room.dispose();generator.dispose();
  scene.add(new THREE.HemisphereLight(0xe5eddb,0x293126,.15));
  const key=new THREE.DirectionalLight(0xf3f2dc,1.5);key.position.set(-1.5,4,3);scene.add(key);
  const rim=new THREE.DirectionalLight(0xadbdcb,1.6);rim.position.set(1,2,-4);scene.add(rim);
  const fill=new THREE.DirectionalLight(0xc8d2b4,.1);fill.position.set(3,.2,3);scene.add(fill);
  controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.dampingFactor=.085;controls.minDistance=.3;controls.maxDistance=30;controls.autoRotateSpeed=.65;controls.addEventListener('start',()=>{cameraTween=null;stopAutoRotate();setView('custom');});controls.listenToKeyEvents(stage);
  resizeObserver=new ResizeObserver(resize);resizeObserver.observe(stage);resetView(true);resize();renderer.setAnimationLoop(animate);
  renderer.domElement.addEventListener('webglcontextlost',event=>{event.preventDefault();setReady(false);showLoading('三维上下文暂时中断','请重新载入页面以恢复模型。',true);$('retry').onclick=()=>location.reload();});
}
async function init(){
  setReady(false);
  try{if(!renderer)initRenderer();}catch(error){showLoading('浏览器无法启动三维渲染','请使用支持 WebGL 2 的浏览器，并启用图形加速。',true);console.error(error);return;}
  const guidesReady=loadGameGuides().then(()=>{if(currentModel)renderGameGuide(currentModel.id);}).catch(error=>console.warn('游戏指南暂时无法读取',error));
  try{
    const response=await fetch('/catalog.json');if(!response.ok)throw new Error(`目录 HTTP ${response.status}`);const data=await response.json();
    if(!Array.isArray(data.models)||!data.models.length||data.models.some(e=>!e.id)||new Set(data.models.map(e=>e.id)).size!==data.models.length)throw new Error('目录缺少有效且唯一的模型编号。');
    catalog={...data,models:data.models.map(normalizeEntry)};renderCatalog();
    const requested=new URLSearchParams(location.search).get('model');
    const filtered=visibleModels();
    await loadModel(filtered.find(e=>e.id===requested)||filtered[0]||catalog.models.find(e=>e.id==='m7')||catalog.models[0],{historyMode:'replace'});
    if(location.hash==='#game-guide'){
      await guidesReady;
      if(!$('game-guide').hidden)requestAnimationFrame(()=>$('game-guide').scrollIntoView({block:'start'}));
    }
  }catch(error){showLoading('展品目录暂时无法读取','请检查网络或本地预览服务，然后重试。',true);console.error(error);}
}

// Read-only diagnostics report actual scene/camera state for acceptance tests.
window.deltaSix={snapshot:()=>({ready,model:currentModel?.id,loadSerial,disposedModels,view:currentView,camera:camera.position.toArray(),target:controls?.target.toArray(),assembly:assembly?.snapshot(),lighting:renderer?{exposure:renderer.toneMappingExposure,lights:scene.children.filter(o=>o.isLight).map(o=>({type:o.type,intensity:o.intensity}))}:null,memory:renderer?{...renderer.info.memory}:null,render:renderer?{...renderer.info.render}:null})};
window.addEventListener('popstate',()=>{
  if(!catalog)return;
  const params=new URLSearchParams(location.search);
  $('catalog-search').value='';
  $('catalog-filter-note').hidden=true;
  const category=params.get('category');
  $('catalog-category').value=[...$('catalog-category').options].some(option=>option.value===category)?category:'all';
  filterCatalog();
  const target=visibleModels().find(entry=>entry.id===params.get('model'))||visibleModels()[0]||catalog.models[0];
  if(target&&target.id!==currentModel?.id)loadModel(target,{historyMode:'none'});
});
window.addEventListener('pagehide',()=>{loader.cancel();renderer?.setAnimationLoop(null);assembly?.dispose();controls?.dispose();resizeObserver?.disconnect();environmentTarget?.dispose();renderer?.dispose();},{once:true});
init();
