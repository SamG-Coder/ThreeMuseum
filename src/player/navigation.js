import {RAMP,DECK,BOUNDS} from '../world/layout.js';
export const BODY_RADIUS=.28;
export const BODY_HEIGHT=1.72;
export const MAX_STEP=.18;
const clamp=(n,a,b)=>Math.min(b,Math.max(a,n));
/** Vertical cylinder versus an axis-aligned solid. Rendering meshes never drive collision. */
export function intersectsSolid(x,y,z,b,radius=BODY_RADIUS,height=BODY_HEIGHT){
 if(y+.025>=b.max[1] || y+height<=b.min[1]+.015)return false;
 const cx=clamp(x,b.min[0],b.max[0]),cz=clamp(z,b.min[2],b.max[2]);
 return (x-cx)**2+(z-cz)**2 < radius*radius-1e-9;
}
export function groundHeight(x,z,previousY=0){
 let h=0;
 if(x>=RAMP.x1-.001&&x<=RAMP.x2+.001){
  for(const s of RAMP.segments){if(z<=s.z1+.001&&z>=s.z2-.001){const t=clamp((s.z1-z)/(s.z1-s.z2),0,1),v=s.y1+(s.y2-s.y1)*t;if(v<=previousY+MAX_STEP)h=Math.max(h,v);}}
 }
 const [x1,x2,z1,z2]=DECK.bounds;
 if(x>=x1&&x<=x2&&z>=z1&&z<=z2&&DECK.y<=previousY+MAX_STEP)h=Math.max(h,DECK.y);
 return h;
}
export class NavigationWorld{
 constructor(colliders){this.colliders=colliders;this.grid=new Map();this.cellSize=4;
  for(const b of colliders)for(let x=Math.floor((b.min[0]-BODY_RADIUS)/4);x<=Math.floor((b.max[0]+BODY_RADIUS)/4);x++)for(let z=Math.floor((b.min[2]-BODY_RADIUS)/4);z<=Math.floor((b.max[2]+BODY_RADIUS)/4);z++){const key=`${x},${z}`;if(!this.grid.has(key))this.grid.set(key,[]);this.grid.get(key).push(b);}
 }
 candidates(x,z){return this.grid.get(`${Math.floor(x/4)},${Math.floor(z/4)}`)||[];}
 blocked(x,y,z){return this.candidates(x,z).some(b=>intersectsSolid(x,y,z,b));}
 /** Displacement subdivision prevents wall tunnelling even after a long frame; X/Z separation gives wall sliding. */
 move(state,dx,dz){
  if(![state.x,state.y,state.z,dx,dz].every(Number.isFinite))throw new TypeError('Movement coordinates must be finite.');
  const steps=Math.max(1,Math.ceil(Math.hypot(dx,dz)/.09));dx/=steps;dz/=steps;
  for(let i=0;i<steps;i++){
   for(const [axis,d]of[['x',dx],['z',dz]]){
    const x=state.x+(axis==='x'?d:0),z=state.z+(axis==='z'?d:0),y=groundHeight(x,z,state.y);
    if(!this.blocked(x,y,z)){state.x=x;state.z=z;state.y=y;}
   }
  }
  return state;
 }
 safePosition(p){return Array.isArray(p)&&p.length===3&&p.every(Number.isFinite)&&p[0]>BOUNDS[0]+BODY_RADIUS&&p[0]<BOUNDS[1]-BODY_RADIUS&&p[2]>BOUNDS[2]+BODY_RADIUS&&p[2]<BOUNDS[3]-BODY_RADIUS&&p[1]>=0&&p[1]<=DECK.y+.001&&!this.blocked(p[0],p[1],p[2]);}
}
