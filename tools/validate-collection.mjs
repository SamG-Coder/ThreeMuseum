import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {EXHIBITS} from '../src/world/layout.js';
import {COLLECTION} from '../src/world/collection.js';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const report=[];const loader=new GLTFLoader();
for(const entry of EXHIBITS){
 const bytes=await fs.readFile(path.join(root,'public/models',entry.id+'.glb'));
 assert.equal(bytes.readUInt32LE(0),0x46546c67);
 const jsonLength=bytes.readUInt32LE(12);
 const document=JSON.parse(bytes.subarray(20,20+jsonLength).toString());
 assert.ok(!document.extensionsRequired?.some(x=>/draco|basisu|meshopt/i.test(x)),`${entry.id}: unsupported compression`);
 assert.ok((document.buffers??[]).every(b=>!b.uri),`${entry.id}: external buffer`);
 assert.ok((document.images??[]).every(i=>i.bufferView!==undefined),`${entry.id}: external texture`);
 assert.ok(COLLECTION[entry.id],`${entry.id}: missing visitor interpretation`);
 const gltf=await loader.parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
 gltf.scene.updateMatrixWorld(true);
 const box=new THREE.Box3().setFromObject(gltf.scene);
 const [w,h,d]=entry.envelope;
 assert.ok(box.min.x>=-w/2-.02 && box.max.x<=w/2+.02 && box.min.y>=-.02 && box.max.y<=h+.02 && box.min.z>=-d/2-.02 && box.max.z<=d/2+.02,`${entry.id}: exported bounds exceed envelope`);
 let triangles=0,meshes=0;let clearance=Infinity;
 gltf.scene.traverse(obj=>{
  if(!obj.isMesh)return;
  meshes++;const g=obj.geometry;const pos=g.attributes.position;
  assert.ok(g.attributes.color,`${entry.id}: missing portable vertex colours`);
  triangles+=(g.index?.count??pos.count)/3;
  for(let i=0;i<pos.count;i++)assert.ok([pos.getX(i),pos.getY(i),pos.getZ(i)].every(Number.isFinite));
  if(entry.id==='D01'){
   const count=g.index?.count??pos.count;const p=[new THREE.Vector3(),new THREE.Vector3(),new THREE.Vector3()];
   for(let k=0;k<count;k+=3){
    for(let j=0;j<3;j++)p[j].fromBufferAttribute(pos,g.index?g.index.getX(k+j):k+j).applyMatrix4(obj.matrixWorld);
    if(Math.min(...p.map(v=>v.z))<=3.5 && Math.max(...p.map(v=>v.z))>=-3.5)clearance=Math.min(clearance,...p.map(v=>v.y+entry.position[1]));
   }
  }
 });
 if(entry.id==='D01')assert.ok(clearance>=2.8,`D01 passage clearance ${clearance}m`);
 report.push({id:entry.id,bytes:bytes.length,meshes,triangles,bounds:{min:box.min.toArray(),max:box.max.toArray()},...(Number.isFinite(clearance)?{passageClearanceM:clearance}:{})});
}
const result={count:report.length,bytes:report.reduce((n,e)=>n+e.bytes,0),triangles:report.reduce((n,e)=>n+e.triangles,0),exhibits:report};
await fs.writeFile(path.join(root,'docs/validation/glb-collection.json'),JSON.stringify(result,null,2)+'\n');
if(process.argv.includes('--install')){
 const file=path.join(root,'public/exhibits.json');const manifest=JSON.parse(await fs.readFile(file,'utf8'));
 manifest.note='Original interpretive collection. Paths relative to public/. See docs/COLLECTION_CREDITS.md.';
 for(const entry of manifest.exhibits)entry.url=`models/${entry.id}.glb`;
 await fs.writeFile(file,JSON.stringify(manifest,null,2)+'\n');
}
console.log(JSON.stringify({validated:result.count,totalMB:result.bytes/1e6,triangles:result.triangles,sauropodClearanceM:report.find(e=>e.id==='D01').passageClearanceM,installed:process.argv.includes('--install')},null,2));
