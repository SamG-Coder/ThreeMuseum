import * as THREE from 'three';
import {makeMaterials,canvasTexture} from './materials.js';

function geometryFor(p){
 const[w,h,d]=p.size;let g;
 if(p.kind==='ramp'){
  const{x1,x2,z1,z2,y1,y2}=p,v=[x1,y1,z1,x2,y1,z1,x2,y2,z2,x1,y2,z2,x1,y1-.2,z1,x2,y1-.2,z1,x2,y2-.2,z2,x1,y2-.2,z2];
  g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(v,3));g.setIndex([0,1,2,0,2,3,4,7,6,4,6,5,0,4,5,0,5,1,3,2,6,3,6,7,0,3,7,0,7,4,1,5,6,1,6,2]);
  g.setAttribute('uv',new THREE.Float32BufferAttribute([0,0,w,0,w,(z1-z2),0,z1-z2,0,0,w,0,w,z1-z2,0,z1-z2],2));g.computeVertexNormals();return g;
 }
 if(p.kind==='beam'){
  const a=new THREE.Vector3(...p.position),b=new THREE.Vector3(...p.end),dir=b.clone().sub(a);g=new THREE.CylinderGeometry(w,w,dir.length(),6,1);
  const q=new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0),dir.normalize());g.applyMatrix4(new THREE.Matrix4().compose(a.add(b).multiplyScalar(.5),q,new THREE.Vector3(1,1,1)));return g;
 }
 if(p.kind==='cylinder')g=new THREE.CylinderGeometry(w/2,w/2,h,20);
 else{
  g=new THREE.BoxGeometry(w,h,d);
  // World-unit texture density instead of stretching one wood pattern over the entire hall.
  const uv=g.getAttribute('uv');for(let i=0;i<uv.count;i++){const side=Math.floor(i/4);let uw=side<2?d:w,vh=side===2||side===3?d:h;uv.setXY(i,uv.getX(i)*uw*.5,uv.getY(i)*vh*.5);}
 }
 if(p.yaw)g.rotateY(p.yaw);g.translate(...p.position);return g;
}
function mergeStatic(list){
 const geos=list.map(g=>g.index?g.toNonIndexed():g);const total=geos.reduce((n,g)=>n+g.getAttribute('position').count,0),merged=new THREE.BufferGeometry();
 for(const[name,size]of[['position',3],['normal',3],['uv',2]]){const out=new Float32Array(total*size);let off=0;for(const g of geos){const a=g.getAttribute(name);if(a)out.set(a.array,off);off+=g.getAttribute('position').count*size;}merged.setAttribute(name,new THREE.BufferAttribute(out,size));}
 merged.computeBoundingSphere();for(const g of new Set([...list,...geos]))g.dispose();return merged;
}
function wrap(c,text,maxWidth){const words=text.split(' '),lines=[];let line='';for(const word of words){const t=line?line+' '+word:word;if(c.measureText(t).width>maxWidth&&line){lines.push(line);line=word;}else line=t;}if(line)lines.push(line);return lines;}
export function makePanel(p){
 const styles={dark:['#222c2e','#f0e9d9','#c2a075'],bronze:['#252b2b','#e5cca7','#bc9562'],light:['#ede7d7','#303b39','#71786c'],green:['#203d37','#e3eedb','#95bdaa'],purple:['#302e3d','#f1ebf4','#c1afcf'],screen:['#172527','#d5dfd7','#819d92']};
 const[bg,fg,accent]=styles[p.style]||styles.dark;const aspect=p.width/p.height;
 const tex=canvasTexture(1024,Math.max(128,Math.round(1024/aspect)),(c,w,h)=>{
  c.fillStyle=bg;c.fillRect(0,0,w,h);c.fillStyle=accent;c.fillRect(0,0,Math.max(5,w*.009),h);
  let size=Math.min(h*.34,w*.075);c.font=`500 ${size}px Arial`;let lines=wrap(c,p.title,w*.88);while(lines.length>2&&size>12){size*=.88;c.font=`500 ${size}px Arial`;lines=wrap(c,p.title,w*.88);}
  c.fillStyle=fg;c.textBaseline='middle';const start=h*.39-(lines.length-1)*size*.52;lines.forEach((l,i)=>c.fillText(l,w*.055,start+i*size*1.08));
  c.font=`400 ${Math.min(h*.12,w*.028)}px Arial`;c.fillStyle=accent;c.fillText(p.subtitle,w*.057,h*.83,w*.89);
 });
 const mesh=new THREE.Mesh(new THREE.PlaneGeometry(p.width,p.height),new THREE.MeshBasicMaterial({map:tex,side:THREE.DoubleSide}));mesh.position.set(...p.position);mesh.rotation.y=p.yaw||0;mesh.name=p.id;mesh.userData.exhibit=p.exhibit;return mesh;
}
export function renderArchitecture(data){
 const root=new THREE.Group();root.name='ThreeMuseum_Architecture';const roof=new THREE.Group();roof.name='Ceilings_and_roofs';root.add(roof);
 const materials=makeMaterials(),groups=new Map();
 // Separate glass panes so transparent surfaces can be sorted by camera distance.
 for(const p of data.pieces){const key=`${p.material}|${p.section==='roof'?'roof':'body'}${p.material==='glass'?'|'+p.id:''}`;if(!groups.has(key))groups.set(key,[]);groups.get(key).push(geometryFor(p));}
 let triangles=0;
 for(const[key,list]of groups){const[mat,section]=key.split('|'),geo=mergeStatic(list),mesh=new THREE.Mesh(geo,materials[mat]);mesh.name=`Architecture_${mat}_${section}`;mesh.castShadow=!['glass','skylight','light'].includes(mat);mesh.receiveShadow=!['glass','skylight','light'].includes(mat);triangles+=geo.getAttribute('position').count/3;(section==='roof'?roof:root).add(mesh);}
 const signs=new THREE.Group();signs.name='Wayfinding_and_labels';for(const p of data.panels)signs.add(makePanel(p));root.add(signs);
 // Deliberate soft contact decals, not claimed as GI or ray-traced shadows.
 const contactTexture=canvasTexture(128,128,(c,w,h)=>{const g=c.createRadialGradient(w/2,h/2,10,w/2,h/2,w/2);g.addColorStop(0,'rgba(15,22,17,.33)');g.addColorStop(.6,'rgba(15,22,17,.12)');g.addColorStop(1,'rgba(15,22,17,0)');c.fillStyle=g;c.fillRect(0,0,w,h);});
 const contactMat=new THREE.MeshBasicMaterial({map:contactTexture,transparent:true,depthWrite:false,toneMapped:false});
 for(const e of data.exhibits){if(e.kind==='wall'||e.kind==='suspended')continue;const p=new THREE.Mesh(new THREE.PlaneGeometry(e.envelope[0]+2,e.envelope[2]+2),contactMat);p.rotation.x=-Math.PI/2;p.position.set(e.position[0],e.id==='D09'?2.405:.035,e.position[2]);root.add(p);}
 // Exhibit envelopes appear only in installation mode. Nothing fills an empty visitor bay.
 const helpers=new THREE.Group();helpers.name='Exhibit_envelopes';helpers.visible=false;
 const anchors=new Map();
 for(const e of data.exhibits){
  const group=new THREE.Group();group.position.set(...e.position);group.name=e.id;group.userData={id:e.id,envelope:e.envelope,subject:e.subject};anchors.set(e.id,group);root.add(group);
  const g=new THREE.EdgesGeometry(new THREE.BoxGeometry(...e.envelope)),mesh=new THREE.LineSegments(g,new THREE.LineBasicMaterial({color:'#c79e62',transparent:true,opacity:.85}));mesh.position.set(e.position[0],e.position[1]+e.envelope[1]/2,e.position[2]);helpers.add(mesh);
  const plate=makePanel({id:'helper-'+e.id,title:e.id,subtitle:`${e.envelope.join(' × ')} m`,position:[e.position[0],e.position[1]+e.envelope[1]+.35,e.position[2]],width:Math.min(e.envelope[0],2.7),height:.65,style:'dark'});helpers.add(plate);
 }
 root.add(helpers);return{root,roof,helpers,anchors,materials,triangles,signs};
}
