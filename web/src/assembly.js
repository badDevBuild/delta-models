import * as THREE from 'three';

const semanticDirections = {
  receiver:[0,.09,.05], body:[0,.09,.05], frame:[0,.06,.02],
  handguard:[-.67,.04,0], stock:[.85,.1,0], buttstock:[.85,.1,0],
  grip:[.24,-.65,.08], magazine:[-.06,-.82,0],
  barrel:[-1.05,.07,0], barrel_short:[-1.05,.07,0], barrel_long:[-1.05,.07,0],
  sights:[0,.65,0], optic:[.08,.88,0], scope:[.08,.88,0], foregrip:[-.48,-.66,0],
  slide:[0,.57,0], pump:[-.55,-.38,.14], tube:[-.55,-.36,-.18],
};

function isTrue(value, fallback = true) {
  if(value === undefined || value === null) return fallback;
  return ![false, 0, 'false', '0'].includes(value);
}

export function partConfiguration(id, data) {
  const variant = data.variant;
  let group = null, value = null;
  if(variant && typeof variant === 'object') {
    group = variant.group || null; value = variant.value || id;
  } else if(typeof variant === 'string' && variant.includes(':')) {
    [group,value] = variant.split(':',2);
  } else if(['short','long'].includes(variant) || ['barrel_short','barrel_long'].includes(id)) {
    group = 'barrel'; value = variant === 'short' || variant === 'long' ? variant : id.split('_').at(-1);
  }
  const fallback = !['barrel_long','optic','foregrip'].includes(id);
  const defaultVisible = isTrue(data.default_visible,fallback);
  return {group, value, defaultVisible, optional:!group && !defaultVisible};
}

export function disposeModel(root) {
  if(!root) return {geometries:0,materials:0,textures:0};
  const geometries = new Set(), materials = new Set(), textures = new Set(), images = new Set();
  root.traverse(object => {
    if(object.geometry) geometries.add(object.geometry);
    for(const material of Array.isArray(object.material) ? object.material : [object.material]) {
      if(!material) continue;
      materials.add(material);
      for(const value of Object.values(material)) if(value?.isTexture) textures.add(value);
    }
    object.skeleton?.dispose();
  });
  geometries.forEach(value => value.dispose());
  textures.forEach(texture => {
    const candidates = Array.isArray(texture.image) ? texture.image : [texture.image];
    for(const item of candidates) if(item?.close && !images.has(item)){item.close();images.add(item);}
    texture.dispose();
  });
  materials.forEach(value => value.dispose());
  root.removeFromParent();
  return {geometries:geometries.size,materials:materials.size,textures:textures.size};
}

export class Assembly {
  constructor(root) {
    this.root = root;
    this.wrapper = new THREE.Group();
    this.wrapper.name = 'display_normalization';
    this.wrapper.add(root);
    this.parts = new Map();
    this.groups = new Map();
    this.options = new Set();
    this.hidden = new Set();
    this.detached = new Set();
    this.selected = null;
    this.isolated = false;
    this.explosion = 0;
    this.meshCount = 0;
    this.triangleCount = 0;
    root.updateMatrixWorld(true);
    root.traverse(object => {
      if(object.isMesh) {
        this.meshCount++;
        this.triangleCount += (object.geometry.index?.count || object.geometry.attributes.position?.count || 0)/3;
      }
      if(object.isMesh || !object.name.startsWith('part_')) return;
      // A glTF mesh with several materials can become a THREE.Group. It still
      // belongs to its containing EMPTY, even when its Blender mesh name starts part_.
      let owner=object.parent;
      while(owner){if(this.parts.get(owner.name.slice(5))?.object===owner)return;owner=owner.parent;}
      const id = object.name.slice(5);
      if(this.parts.has(id)) throw new Error(`组件名称重复：${id}`);
      let meshes=0;
      object.traverse(child => {if(child.isMesh) meshes++;});
      if(!meshes) throw new Error(`组件没有几何体：${id}`);
      const bounds = new THREE.Box3().setFromObject(object);
      const dimensions = bounds.getSize(new THREE.Vector3());
      if(bounds.isEmpty() || ![...bounds.min,...bounds.max].every(Number.isFinite) || dimensions.toArray().some(n=>n<=0)) throw new Error(`组件尺寸无效：${id}`);
      const config = partConfiguration(id, object.userData);
      const part = {id,object,label:object.userData.label || id,description:object.userData.description || '',config,origin:object.position.clone(),target:object.position.clone(),materials:[]};
      this.parts.set(id,part);
    });
    if(!this.parts.size) throw new Error('模型没有 part_ 命名的外观组件。');
    for(const part of this.parts.values()) {
      let ancestor=part.object.parent;
      while(ancestor){if([...this.parts.values()].some(other=>other.object===ancestor))throw new Error(`逻辑组件不能嵌套：${part.id}`);ancestor=ancestor.parent;}
    }
    // Every part needs independent highlight materials; geometry and textures remain shared.
    const originalMaterials = new Set();
    for(const part of this.parts.values()) {
      const clones = new Map();
      part.object.traverse(object => {
        if(!object.isMesh) return;
        const clone = material => {
          originalMaterials.add(material);
          if(!clones.has(material)) {
            const copy=material.clone();
            copy.envMapIntensity=.35;
            clones.set(material,copy);
            part.materials.push({material:copy,emissive:copy.emissive?.clone(),intensity:copy.emissiveIntensity});
          }
          return clones.get(material);
        };
        object.material=Array.isArray(object.material) ? object.material.map(clone) : clone(object.material);
      });
    }
    const stillUsed=new Set();root.traverse(o=>{for(const m of [].concat(o.material||[]))stillUsed.add(m);});
    for(const material of originalMaterials) if(!stillUsed.has(material)) material.dispose();
    this.reset();
    const baseBounds = new THREE.Box3();
    for(const part of this.parts.values()) if(this.enabled(part.id)) baseBounds.union(new THREE.Box3().setFromObject(part.object));
    if(baseBounds.isEmpty()) throw new Error('模型没有默认显示组件。');
    const size = baseBounds.getSize(new THREE.Vector3());
    const center = baseBounds.getCenter(new THREE.Vector3());
    this.scale=3/Math.max(...size.toArray());
    this.wrapper.scale.setScalar(this.scale);
    this.wrapper.position.copy(center).multiplyScalar(-this.scale);
    this.wrapper.updateMatrixWorld(true);
    for(const [id,part] of this.parts) {
      part.baseBounds=new THREE.Box3().setFromObject(part.object);
      const ownDirection=part.object.userData.explode_direction;
      if(Array.isArray(ownDirection)&&ownDirection.length===3&&ownDirection.every(Number.isFinite)) part.direction=new THREE.Vector3(...ownDirection);
      else if(semanticDirections[id]) part.direction=new THREE.Vector3(...semanticDirections[id]);
      else {
        part.direction=part.baseBounds.getCenter(new THREE.Vector3());
        part.direction.multiplyScalar(.7);
        if(part.direction.length()<.25) part.direction.set(0,.4,.3);
      }
      // Convert a normalized world offset into the actual parent coordinates, including glTF unit transforms.
      const inverseLinear=new THREE.Matrix3().setFromMatrix4(part.object.parent.matrixWorld).invert();
      part.localDirection=part.direction.clone().applyMatrix3(inverseLinear);
    }
  }
  reset() {
    this.explosion=0;this.selected=null;this.isolated=false;this.hidden.clear();this.detached.clear();this.groups.clear();this.options.clear();
    for(const part of this.parts.values()) {
      const c=part.config;
      if(c.group && (c.defaultVisible || !this.groups.has(c.group))) this.groups.set(c.group,c.value);
      if(c.optional && c.defaultVisible) this.options.add(part.id);
      part.object.position.copy(part.origin);
      part.target.copy(part.origin);
    }
    this.sync();
  }
  enabled(id) {
    const c=this.parts.get(id)?.config;
    return !!c && (c.group ? this.groups.get(c.group)===c.value : c.optional ? this.options.has(id) : true);
  }
  setVariant(group,value) {
    if(![...this.parts.values()].some(p=>p.config.group===group&&p.config.value===value)) return false;
    this.groups.set(group,value);this.sync();return true;
  }
  setOptional(id,enabled) {if(!this.parts.get(id)?.config.optional)return false;enabled?this.options.add(id):this.options.delete(id);this.sync();return true;}
  select(id) {this.selected=this.parts.has(id)&&this.enabled(id)?id:null;this.isolated=false;this.sync();}
  toggleHidden(id) {if(!this.parts.has(id))return;this.hidden.has(id)?this.hidden.delete(id):this.hidden.add(id);this.sync();}
  toggleDetached(id=this.selected) {if(!this.parts.has(id))return;this.detached.has(id)?this.detached.delete(id):this.detached.add(id);this.sync();}
  toggleIsolate() {if(!this.selected)return;this.isolated=!this.isolated;this.hidden.delete(this.selected);this.sync();}
  setExplosion(amount) {this.explosion=THREE.MathUtils.clamp(Number(amount)||0,0,1);this.isolated=false;this.sync();}
  sync() {
    if(this.selected&&!this.enabled(this.selected)){this.selected=null;this.isolated=false;}
    for(const [id,part] of this.parts) {
      part.object.visible=this.enabled(id)&&!this.hidden.has(id)&&(!this.isolated||id===this.selected);
      if(part.localDirection)part.target.copy(part.origin).addScaledVector(part.localDirection,this.explosion+(this.detached.has(id)?.8:0));
      for(const {material,emissive,intensity} of part.materials) {
        if(!material.emissive)continue;
        material.emissive.copy(emissive);
        material.emissiveIntensity=intensity;
        if(id===this.selected){material.emissive.lerp(new THREE.Color(0x9dbb64),.23);material.emissiveIntensity=Math.max(.25,intensity||0);}
      }
    }
  }
  update(delta,immediate=false) {
    const ratio=immediate?1:1-Math.exp(-Math.min(delta,.1)*10);
    for(const part of this.parts.values())part.object.position.lerp(part.target,ratio);
    this.wrapper.updateMatrixWorld(true);
  }
  visibleBounds(targetPositions=true) {
    const box=new THREE.Box3();
    this.wrapper.updateMatrixWorld(true);
    for(const [id,part] of this.parts) {
      if(!part.object.visible)continue;
      const partBounds=targetPositions&&part.baseBounds?part.baseBounds.clone().translate(part.direction.clone().multiplyScalar(this.explosion+(this.detached.has(id)?.8:0))):new THREE.Box3().setFromObject(part.object);
      box.union(partBounds);
    }
    return box;
  }
  snapshot() {
    return {selected:this.selected,isolated:this.isolated,explosion:this.explosion,groups:Object.fromEntries(this.groups),options:[...this.options],hidden:[...this.hidden],detached:[...this.detached],parts:[...this.parts].map(([id,p])=>({id,label:p.label,enabled:this.enabled(id),visible:p.object.visible,position:p.object.position.toArray(),target:p.target.toArray()})),meshes:this.meshCount,triangles:this.triangleCount};
  }
  dispose() {return disposeModel(this.wrapper);}
}
