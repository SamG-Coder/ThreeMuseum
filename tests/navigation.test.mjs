import test from 'node:test';
import assert from 'node:assert/strict';
import {buildArchitecture} from '../src/world/architecture.js';
import {NavigationWorld,groundHeight,intersectsSolid} from '../src/player/navigation.js';
import {ROOMS,EXHIBITS,RAMP} from '../src/world/layout.js';
const data=buildArchitecture(),nav=new NavigationWorld(data.colliders);
const near=(a,b,eps=.05)=>assert.ok(Math.abs(a-b)<eps,`${a} differs from ${b}`);

test('Architecture is deterministic; IDs and dimensions are valid',()=>{
 assert.deepEqual(buildArchitecture(),data);const ids=data.pieces.map(p=>p.id);assert.equal(new Set(ids).size,ids.length);
 for(const p of data.pieces){assert.ok(p.position.every(Number.isFinite),p.id);assert.ok(p.size.every(Number.isFinite),p.id);assert.ok(p.size[0]>0&&p.size[2]>0,p.id);if(p.kind!=='beam')assert.ok(p.size[1]>0,p.id);}
 for(const b of data.colliders){for(let i=0;i<3;i++)assert.ok(b.min[i]<=b.max[i],b.id);}
});
test('30 unique exhibit origins with unloaded asset defaults',()=>{
 assert.equal(EXHIBITS.length,30);assert.equal(new Set(EXHIBITS.map(e=>e.id)).size,30);
 for(const e of EXHIBITS){assert.equal(e.url,null);assert.ok(e.envelope.every(v=>v>0));assert.ok(ROOMS.some(r=>r.id===e.room));}
});
test('All eleven room entrance spawns are unobstructed',()=>{for(const r of ROOMS)assert.ok(nav.safePosition(r.spawn),r.id);});
test('Forecourt to arrival is a real eight-metre opening',()=>{const s={x:0,y:0,z:42};nav.move(s,0,-22);near(s.z,20);});
test('Glazed facade blocks walking, including a huge one-frame displacement',()=>{const s={x:9,y:0,z:42};nav.move(s,0,-35);assert.ok(s.z>29.25&&s.z<29.5);});
test('Central gallery-street path crosses the museum without blocked door gaps',()=>{const s={x:-35,y:0,z:11};nav.move(s,70,0);near(s.x,35);});
test('Main dinosaur entrance is connected to the arrival hall',()=>{const s={x:-17,y:0,z:11};nav.move(s,0,-10);near(s.z,1);});
test('Wall sliding preserves tangential movement',()=>{const s={x:0,y:0,z:-40};nav.move(s,12,-1);assert.ok(s.x<3.65);near(s.z,-41);});
test('Plinth footprints block visitors',()=>{const s={x:-17,y:0,z:-16};nav.move(s,10,0);assert.ok(s.x<-13.9);});
test('Split sauropod supports preserve the seven-metre cross passage',()=>{const s={x:-32,y:0,z:-16};nav.move(s,13,0);near(s.x,-19);});
test('Ramp rises continuously through all landings and joins the deck',()=>{
 const s={x:-35.8,y:0,z:7};for(let i=0;i<450;i++)nav.move(s,0,-.1);near(s.z,-38);near(s.y,2.4,.005);
 nav.move(s,14,0);near(s.x,-21.8);near(s.y,2.4,.005);
});
test('Descending the ramp reaches the ground with no teleport or step obstruction',()=>{
 const s={x:-35.8,y:2.4,z:-38};for(let i=0;i<450;i++)nav.move(s,0,.1);near(s.z,7);near(s.y,0,.005);
});
test('Deck guardrail prevents stepping off the overlook',()=>{const s={x:-21.8,y:2.4,z:-38};nav.move(s,0,8);assert.ok(s.z<-36.2);near(s.y,2.4,.005);});
test('Ground-floor visitor is not snapped onto the high deck',()=>{near(groundHeight(-20,-40,0),0,.0001);near(groundHeight(-20,-40,2.4),2.4,.0001);});
test('Ramp total rise and slope geometry match the design',()=>{const slopes=RAMP.segments.filter(s=>s.y2>s.y1);assert.equal(slopes.length,3);for(const s of slopes)near((s.z1-s.z2)/(s.y2-s.y1),15,.00001);});
test('All exhibit reading positions are reachable as safe standing points',()=>{for(const e of EXHIBITS){const p=[e.view[0],groundHeight(e.view[0],e.view[2],3),e.view[2]];assert.ok(nav.safePosition(p),`${e.id}: ${p}`);}});
test('Overlook table base starts on the deck, not on the ground below it',()=>{const b=data.colliders.find(b=>b.id.startsWith('D09-base'));near(b.min[1],2.4,.00001);near(b.max[1],3.28,.00001);});
test('Non-finite movement is rejected',()=>assert.throws(()=>nav.move({x:0,y:0,z:0},NaN,1),TypeError));
test('Vertical overlap test does not collide with a slab under the feet',()=>{const b={min:[-2,2.14,-2],max:[2,2.4,2]};assert.equal(intersectsSolid(0,2.4,0,b),false);});
test('Every segment of the suggested interpretation loop is continuously walkable',()=>{
 const route=data.visitorRoute,s={x:route[0][0],y:0,z:route[0][1]};
 for(const [x,z]of route.slice(1)){nav.move(s,x-s.x,z-s.z);near(s.x,x,.08);near(s.z,z,.08);}
});
test('Invalid and off-site teleport positions are rejected',()=>{
 assert.equal(nav.safePosition(null),false);assert.equal(nav.safePosition([500,0,500]),false);assert.equal(nav.safePosition([0,20,0]),false);
});
test('Diversity and habitat front portals are not blocked by wall cabinets',()=>{
 for(const x of[9,11,13,28,29,30]){const s={x,y:0,z:11};nav.move(s,0,-6);near(s.z,5,.05);}
});

