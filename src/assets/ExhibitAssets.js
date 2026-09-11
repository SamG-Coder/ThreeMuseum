import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {EXHIBITS} from '../world/layout.js';
const finiteVector=(v)=>Array.isArray(v)&&v.length===3&&v.every(Number.isFinite);
export function validateEntry(e){
 if(!e||typeof e.id!=='string'||!EXHIBITS.some(x=>x.id===e.id))throw new Error('Unknown exhibit ID.');
 if(e.url!==null&&e.url!==undefined&&(typeof e.url!=='string'||/^\s*(javascript|data):/i.test(e.url)))throw new Error('An exhibit URL must be a relative path or an HTTP(S) URL.');
 for(const k of['offset','rotation'])if(e[k]!==undefined&&!finiteVector(e[k]))throw new Error(`${e.id}: ${k} must have three finite numbers.`);
 if(e.scale!==undefined&&(!Number.isFinite(e.scale)||e.scale<=0))throw new Error(`${e.id}: scale must be positive.`);
 return e;
}
function disposeObject(root){const geometries=new Set(),materials=new Set(),textures=new Set();root.traverse(o=>{if(o.geometry)geometries.add(o.geometry);const list=Array.isArray(o.material)?o.material:[o.material];for(const m of list){if(!m)continue;materials.add(m);for(const v of Object.values(m))if(v?.isTexture)textures.add(v);}});for(const g of geometries)g.dispose();for(const t of textures){if(t.source?.data?.close)t.source.data.close();t.dispose();}for(const m of materials)m.dispose();}
export class ExhibitAssets{
 constructor(anchors,notify){this.anchors=anchors;this.notify=notify;this.entries=new Map(EXHIBITS.map(e=>[e.id,structuredClone(e)]));this.loaded=new Map();this.pending=new Map();this.loader=new GLTFLoader();this.mixers=new Map();}
 async readManifest(){try{
  const r=await fetch('./public/exhibits.json');if(!r.ok)throw new Error(`Manifest HTTP ${r.status}`);const j=await r.json();if(!Array.isArray(j.exhibits))throw new Error('Expected an exhibits array.');
  for(const item of j.exhibits){validateEntry(item);const e=this.entries.get(item.id);for(const k of['url','offset','rotation','scale'])if(item[k]!==undefined)e[k]=item[k];}
  // Sequential loads keep memory and compile spikes bounded during installation.
  for(const e of this.entries.values())if(e.url){try{await this.load(e.id,new URL(e.url,new URL('./public/',location.href)).href);}catch{/* One broken asset must not prevent the remaining gallery from loading. */}}
 }catch(err){this.notify(`Asset manifest: ${err.message}`);}}
 async load(id,url,localFileName=null){
  if(!this.entries.has(id))throw new Error('Unknown exhibit ID.');const ticket=Symbol();this.pending.set(id,ticket);
  try{const gltf=await this.loader.loadAsync(url);if(this.pending.get(id)!==ticket){disposeObject(gltf.scene);return;}
   this.remove(id);const root=new THREE.Group();root.name='Exhibit_'+id;root.add(gltf.scene);root.traverse(o=>{if(o.isMesh){o.castShadow=true;o.receiveShadow=true;}});this.anchors.get(id).add(root);this.loaded.set(id,root);
   if(localFileName)this.entries.get(id).url='models/'+localFileName;
   this.apply(id);if(gltf.animations.length){const mixer=new THREE.AnimationMixer(gltf.scene);for(const clip of gltf.animations)mixer.clipAction(clip).play();this.mixers.set(id,mixer);}
   const warning=this.checkEnvelope(id);this.notify(warning||`${id} installed${localFileName?' for this session. Copy the GLB into public/models to keep it.':'.'}`);
  }catch(err){this.notify(`${id} could not load: ${err.message}. Use a self-contained, uncompressed GLB.`);throw err;}
 }
 async loadFile(id,file){if(!file.name.toLowerCase().endsWith('.glb'))throw new Error('Choose a self-contained .glb file.');if(file.size>128*1024*1024)throw new Error('This preview accepts GLB files up to 128 MB. Optimise the model first.');const url=URL.createObjectURL(file);try{await this.load(id,url,file.name);}finally{URL.revokeObjectURL(url);}}
 remove(id){this.pending.delete(id);const root=this.loaded.get(id);if(root){root.removeFromParent();disposeObject(root);this.loaded.delete(id);}const m=this.mixers.get(id);if(m){m.stopAllAction();m.uncacheRoot(m.getRoot());this.mixers.delete(id);}}
 apply(id){const e=this.entries.get(id);validateEntry(e);const root=this.loaded.get(id);if(!root)return;root.position.set(...e.offset);root.rotation.set(...e.rotation.map(THREE.MathUtils.degToRad));root.scale.setScalar(e.scale);root.updateMatrixWorld(true);}
 checkEnvelope(id){const root=this.loaded.get(id);if(!root)return'';const e=this.entries.get(id);root.updateWorldMatrix(true,true);const box=new THREE.Box3().setFromObject(root),p=e.position,[w,h,d]=e.envelope;const eps=.03;
  return box.min.x<p[0]-w/2-eps||box.max.x>p[0]+w/2+eps||box.min.y<p[1]-eps||box.max.y>p[1]+h+eps||box.min.z<p[2]-d/2-eps||box.max.z>p[2]+d/2+eps?`${id}: the model extends outside its reserved envelope. Adjust offset, rotation or scale; the walkway must stay clear.`:'';
 }
 fit(id){const root=this.loaded.get(id);if(!root)return;const e=this.entries.get(id);e.offset=[0,0,0];e.rotation=[0,0,0];e.scale=1;this.apply(id);
  root.updateWorldMatrix(true,true);const b=new THREE.Box3().setFromObject(root),s=b.getSize(new THREE.Vector3()),c=b.getCenter(new THREE.Vector3()),p=e.position;
  if(Math.min(s.x,s.y,s.z)<1e-7){this.notify('Cannot fit a degenerate model.');return;}
  e.scale=.94*Math.min(...e.envelope.map((v,i)=>v/[s.x,s.y,s.z][i]));e.offset=[-(c.x-p[0])*e.scale,-(b.min.y-p[1])*e.scale,-(c.z-p[2])*e.scale];this.apply(id);this.notify('Uniform fit applied. This changes presentation scale; verify real-world specimen scale yourself.');
 }
 update(dt){for(const m of this.mixers.values())m.update(Math.min(dt,.05));}
 export(){return{version:1,units:'metres',note:'Position/envelope are defined in src/world/layout.js. Place referenced GLB files under public/models.',exhibits:[...this.entries.values()].map(e=>({id:e.id,title:e.title,position:e.position,envelope:e.envelope,url:e.url,offset:e.offset,rotation:e.rotation,scale:e.scale}))};}
}
