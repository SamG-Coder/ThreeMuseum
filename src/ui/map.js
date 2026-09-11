import {ROOMS,EXHIBITS,RAMP,DECK} from '../world/layout.js';
/** One map projection for the HUD and the full-screen visitor map. */
export function drawMuseumMap(canvas, state, colliders, detailed=false){
 const ctx=canvas.getContext('2d'),W=canvas.width,H=canvas.height;
 const scale=Math.min((W-24)/88,(H-30)/98), ox=W/2,oz=12+48*scale;
 const X=x=>ox+x*scale,Z=z=>oz+z*scale;
 ctx.clearRect(0,0,W,H);ctx.fillStyle='#edeadf';ctx.fillRect(0,0,W,H);
 ctx.fillStyle='#dddacf';ctx.fillRect(X(-38),Z(-43),76*scale,72*scale);
 for(const r of ROOMS){const[x1,x2,z1,z2]=r.bounds;ctx.fillStyle=r.color+'70';ctx.fillRect(X(x1),Z(z1),(x2-x1)*scale,(z2-z1)*scale);}
 ctx.fillStyle='#ba98693b';ctx.fillRect(X(RAMP.x1),Z(-36),(RAMP.x2-RAMP.x1)*scale,42*scale);
 const[x1,x2,z1,z2]=DECK.bounds;ctx.fillRect(X(x1),Z(z1),(x2-x1)*scale,(z2-z1)*scale);
 ctx.fillStyle='#293c39';
 for(const b of colliders){if(b.min[1]>1.8||b.max[1]<=.06||b.id==='site-boundary'||b.id==='ramp-side')continue;
  ctx.fillRect(X(b.min[0]),Z(b.min[2]),Math.max(.6,(b.max[0]-b.min[0])*scale),Math.max(.6,(b.max[2]-b.min[2])*scale));}
 for(const e of EXHIBITS){ctx.strokeStyle='#8b683d';ctx.lineWidth=.65;ctx.strokeRect(X(e.position[0]-e.envelope[0]/2),Z(e.position[2]-e.envelope[2]/2),e.envelope[0]*scale,e.envelope[2]*scale);
  if(detailed){ctx.font=`600 ${Math.max(9,scale*1.2)}px system-ui`;ctx.textAlign='center';ctx.fillStyle='#354139';ctx.fillText(e.id,X(e.position[0]),Z(e.position[2])+3);}}
 if(state){const px=X(state.x),pz=Z(state.z);ctx.save();ctx.translate(px,pz);ctx.rotate(-state.yaw);ctx.fillStyle='#c27c32';ctx.beginPath();ctx.moveTo(0,-12);ctx.lineTo(-6,5);ctx.lineTo(6,5);ctx.closePath();ctx.fill();ctx.restore();ctx.beginPath();ctx.arc(px,pz,3,0,Math.PI*2);ctx.fillStyle='#fff9e6';ctx.fill();}
 if(detailed){ctx.textAlign='left';ctx.font='600 12px system-ui';ctx.fillStyle='#354139';ctx.fillText('N ↑',14,24);ctx.fillText('Original design · metres',14,H-12);}
}
