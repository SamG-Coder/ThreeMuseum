import {PLAYER_SPAWN} from '../world/layout.js';
/** Museum walking, not FPS combat: no mandatory head bob, jumping, stamina or camera roll. */
export class VisitorController{
 constructor(camera,canvas,navigation){
  this.camera=camera;this.canvas=canvas;this.navigation=navigation;
  this.state={x:PLAYER_SPAWN[0],y:0,z:PLAYER_SPAWN[2],yaw:0,pitch:0};
  this.keys=new Set();this.active=false;this.eyeHeight=1.62;this.sensitivity=.002;this.walkSpeed=2.2;this.touchMove={x:0,y:0};this.distance=0;
  window.addEventListener('keydown',e=>{if(/INPUT|SELECT|TEXTAREA/.test(document.activeElement?.tagName||''))return;if(this.active&&['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Space'].includes(e.code))e.preventDefault();this.keys.add(e.code);});
  window.addEventListener('keyup',e=>this.keys.delete(e.code));
  window.addEventListener('blur',()=>this.clearInput());
  document.addEventListener('visibilitychange',()=>this.clearInput());
  document.addEventListener('pointerlockchange',()=>{this.drag=null;this.clearInput();});
  document.addEventListener('mousemove',e=>{if(this.active&&document.pointerLockElement===canvas)this.look(e.movementX,e.movementY);});
  canvas.addEventListener('pointerdown',e=>{if(this.active&&document.pointerLockElement!==canvas){this.drag={x:e.clientX,y:e.clientY,id:e.pointerId};canvas.setPointerCapture(e.pointerId);}});
  canvas.addEventListener('pointermove',e=>{if(this.active&&this.drag?.id===e.pointerId){this.look(e.clientX-this.drag.x,e.clientY-this.drag.y);this.drag={x:e.clientX,y:e.clientY,id:e.pointerId};}});
  canvas.addEventListener('pointerup',()=>this.drag=null);canvas.addEventListener('pointercancel',()=>this.drag=null);
  this.updateCamera();
 }
 clearInput(){this.keys.clear();this.touchMove.x=this.touchMove.y=0;this.drag=null;}
 look(dx,dy){this.state.yaw-=dx*this.sensitivity;this.state.pitch=Math.max(-1.42,Math.min(1.42,this.state.pitch-dy*this.sensitivity));}
 async lock(){try{await this.canvas.requestPointerLock?.();}catch{/* Drag-to-look and keyboard look remain available. */}}
 teleport(p,yaw=0){if(!this.navigation.safePosition(p))return false;[this.state.x,this.state.y,this.state.z]=p;this.state.yaw=yaw;this.state.pitch=0;this.clearInput();this.updateCamera();return true;}
 update(dt){if(!this.active)return;
  dt=Math.min(dt,.05);const k=this.keys;
  let forward=(k.has('KeyW')?1:0)-(k.has('KeyS')?1:0)-this.touchMove.y;
  let right=(k.has('KeyD')?1:0)-(k.has('KeyA')?1:0)+this.touchMove.x;
  const len=Math.hypot(forward,right);if(len>1){forward/=len;right/=len;}
  if(k.has('ArrowLeft'))this.state.yaw+=dt*1.6;if(k.has('ArrowRight'))this.state.yaw-=dt*1.6;
  if(k.has('ArrowUp'))this.state.pitch=Math.min(1.42,this.state.pitch+dt);if(k.has('ArrowDown'))this.state.pitch=Math.max(-1.42,this.state.pitch-dt);
  const speed=k.has('ShiftLeft')||k.has('ShiftRight')?this.walkSpeed*1.75:this.walkSpeed;
  const dx=(-Math.sin(this.state.yaw)*forward+Math.cos(this.state.yaw)*right)*dt*speed;
  const dz=(-Math.cos(this.state.yaw)*forward-Math.sin(this.state.yaw)*right)*dt*speed;
  const oldX=this.state.x,oldZ=this.state.z;this.navigation.move(this.state,dx,dz);
  this.distance+=Math.hypot(this.state.x-oldX,this.state.z-oldZ);this.updateCamera();
 }
 updateCamera(){this.camera.position.set(this.state.x,this.state.y+this.eyeHeight,this.state.z);this.camera.rotation.order='YXZ';this.camera.rotation.set(this.state.pitch,this.state.yaw,0);}
}
