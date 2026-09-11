import * as THREE from 'three';
import {COLLECTION} from './world/collection.js';

/** Opt-in, reproducible camera edit. Uses the real museum and the real visitor dialogs. */
export function createDirector(api){
 const {camera,world,assets,data,visitor}=api;
 // Exhibit captions replace the physical reading plaques during the camera edit.
 world.root.traverse(o=>{if(o.userData.exhibit)o.visible=false;});
 const style=document.createElement('style');
 style.textContent=`body.director #welcome,body.director header,body.director #edition,body.director #location-card,body.director #mini-map,body.director #controls,body.director #crosshair,body.director #touch-controls,body.director #interact-prompt,body.director #toast,body.director .scrim{display:none!important}
 .director-caption{position:fixed;bottom:0;left:0;right:0;padding:24px 44px 28px;background:linear-gradient(transparent,rgba(10,25,24,.96));pointer-events:none;z-index:20}
 .director-caption small{font:11px Arial;letter-spacing:3px;color:#d6bb87}.director-caption h1{font:34px Georgia;margin:9px 0 7px;color:#f4eddd;letter-spacing:0}.director-caption p{font:15px Arial;color:#e0e5dc;margin:0;line-height:1.5}.director-brand{position:fixed;top:25px;left:44px;font:12px Arial;letter-spacing:4px;color:#f4eddd;text-shadow:0 1px 5px #000;z-index:20}
 body.director dialog{max-height:78vh;margin-top:28px}body.director .director-progress{position:fixed;bottom:0;left:0;height:3px;background:#d6bb87;z-index:30}`;
 document.head.append(style);document.body.classList.add('director');
 const caption=document.createElement('div');caption.className='director-caption';document.body.append(caption);
 const brand=document.createElement('div');brand.className='director-brand';brand.textContent="M³  /  THREE MUSEUM  /  DIRECTOR’S CUT";document.body.append(brand);
 const progress=document.createElement('div');progress.className='director-progress';document.body.append(progress);
 const shots=[];
 const add=(duration,title,detail,from,to,target,extra={})=>shots.push({duration,title,detail,from,to,target,...extra});
 add(6,'Small worlds. Deep time.','A walkable natural-history museum built with Three.js + Blender MCP.',[16,5.8,43],[8,4.6,39],[-4,3,10]);
 add(6,'Eleven spaces. One connected museum.','Roof-off architect view reveals the galleries, cases and circulation.',[53,66,57],[42,62,65],[0,0,-8],{roof:false});
 add(5,'Take the long view','A continuous ramp climbs 2.4 metres to the Deep Time overlook.',[-35.8,2.8,-25],[-35.8,3.8,-34],[-21,2,-19]);
 for(const e of data.exhibits){
  const root=assets.loaded.get(e.id);root.updateWorldMatrix(true,true);
  const box=new THREE.Box3().setFromObject(root),centre=box.getCenter(new THREE.Vector3());
  const from=[e.view[0],e.view[1]+1.62,e.view[2]];
  if(e.id==='D09')from[1]=4.02;
  const delta=new THREE.Vector3(from[0]-centre.x,0,from[2]-centre.z).normalize();
  if(e.kind==='table'){
   from[0]=centre.x+delta.x*2;from[2]=centre.z+delta.z*2;from[1]=box.max.y+1.7;
  }
  if(e.id==='D02')from.splice(0,3,-5.6,4.2,-10.5);
  if(e.id==='D08')from[1]=5;
  if(e.id==='B16'){from[0]=centre.x;from[1]=centre.y;from[2]=centre.z+2.8;}
  const tangent=new THREE.Vector3(-delta.z,0,delta.x);
  const amount=e.kind==='wall'?.18:.42;
  const to=[from[0]+tangent.x*amount,from[1]+.08,from[2]+tangent.z*amount];
  const target=centre.toArray();
  add(['D01','F01','B09'].includes(e.id)?4:2.3,COLLECTION[e.id]?.[0]||e.subject,
   `${e.id} / ${e.subject}${e.id==='F01'?' · Smithsonian Institution · CC0': ' · Original interpretive model'}`,from,to,target,{id:e.id,fov:['D01','D02'].includes(e.id)?78:60});
 }
 add(4,'Find your next discovery','The map offers direct room destinations and a measured design atlas.',[0,2,20],[0,2,20],[0,2,0],{dialog:'mapDialog'});
 add(4,'Make yourself comfortable','Field of view, walking speed, sensitivity, eye height and graphics controls.',[0,2,20],[0,2,20],[0,2,0],{dialog:'settingsDialog'});
 add(5,'A museum you can keep building','Preview GLBs, adjust transforms, fit envelopes and export the installation manifest.',[-17.5,2,-16],[-17.5,2,-16],[-24,3,-16],{dialog:'installDialog',argument:'D01',guides:true});
 add(4,'Read the evidence','Visitor cards describe each installation and distinguish original studies from CC0 source material.',[7.3,2,-34.4],[7.3,2,-34.4],[13,1.7,-34.4],{dialog:'showExhibit',argument:data.exhibits.find(e=>e.id==='F01')});
 add(3,'Room to pause','A quiet theatre and visitor lounge complete the journey.',[25,2,-27],[26,2,-29],[29.5,2.6,-42.56]);
 add(3,'Built for exploring','Keyboard, mouse, drag-to-look and touch controls. Collision-aware walking throughout.',[-24,2,17],[-25,2,19],[-29,2,28]);
 add(6,'Open the doors. Make it yours.','github.com/SamG-Coder/ThreeMuseum  ·  MIT code + original assets  ·  CC0 Triceratops',[45,60,62],[52,65,55],[0,0,-8],{roof:false});
 let start=null,current=-1;const total=shots.reduce((a,s)=>a+s.duration,0);
 function paint(seconds){
  let index=0,local=seconds;while(index<shots.length-1&&local>=shots[index].duration)local-=shots[index++].duration;
  const s=shots[index],u=THREE.MathUtils.clamp(local/s.duration,0,1),t=u*u*(3-2*u);
  if(current!==index){
   api.closeDialog();visitor.active=false;world.helpers.visible=!!s.guides;world.roof.visible=s.roof!==false;
   caption.replaceChildren();const k=document.createElement('small'),h=document.createElement('h1'),p=document.createElement('p');
   k.textContent=`${String(index+1).padStart(2,'0')} / THE COLLECTION EDITION`;h.textContent=s.title;p.textContent=s.detail;caption.append(k,h,p);
   if(s.dialog)api[s.dialog](s.argument);
   camera.fov=s.fov||60;camera.updateProjectionMatrix();current=index;
  }
  camera.position.fromArray(s.from).lerp(new THREE.Vector3(...s.to),t);camera.lookAt(...s.target);
  const sorted=data.lights.toSorted((a,b)=>new THREE.Vector3(...a.position).distanceToSquared(camera.position)-new THREE.Vector3(...b.position).distanceToSquared(camera.position));
  api.fillLights.forEach((l,i)=>{l.position.set(...sorted[i].position);l.intensity=sorted[i].power;});
  progress.style.width=`${Math.min(seconds/total,1)*100}%`;
 }
 const play=document.createElement('button');play.textContent="Play director’s cut";play.style.cssText='position:fixed;right:30px;top:20px;z-index:40';document.body.append(play);
 window.__DIRECTOR__={total,shots,ready:true,done:false,start(){play.hidden=true;window.__DIRECTOR__.done=false;start=performance.now();},seek(seconds){play.hidden=true;start=null;paint(seconds);}};
 play.onclick=()=>window.__DIRECTOR__.start();
 paint(0);
 return now=>{if(start!==null){const seconds=(now-start)/1000;paint(Math.min(seconds,total));if(seconds>=total){window.__DIRECTOR__.done=true;start=null;}}};
}
