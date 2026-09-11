import {ROOMS,EXHIBITS,RAMP,DECK,BOUNDS,VISITOR_ROUTE} from './layout.js';

/** Pure, dependency-free architecture compiler. The renderer, tests, plans and Blender use the same records. */
export function buildArchitecture(){
 const pieces=[],colliders=[],panels=[],lights=[]; let serial=0;
 const add=(kind,name,p,s,mat,options={})=>{const v={id:`${name}-${serial++}`,kind,position:p,size:s,material:mat,...options};pieces.push(v);return v;};
 function box(name,p,s,mat,solid=false,options={}){
  const v=add('box',name,p,s,mat,options);
  if(solid)colliders.push({id:v.id,min:[p[0]-s[0]/2,p[1]-s[1]/2,p[2]-s[2]/2],max:[p[0]+s[0]/2,p[1]+s[1]/2,p[2]+s[2]/2]});
  return v;
 }
 function cyl(name,p,r,h,mat,solid=false){const v=add('cylinder',name,p,[r*2,h,r*2],mat);if(solid)colliders.push({id:v.id,min:[p[0]-r,p[1]-h/2,p[2]-r],max:[p[0]+r,p[1]+h/2,p[2]+r]});return v;}
 function panel(title,subtitle,p,w,h,options={}){panels.push({id:`panel-${serial++}`,title,subtitle,position:p,width:w,height:h,yaw:0,style:'dark',...options});}
 function wall(axis,at,a,b,h,doors=[],material='plaster'){
  const spans=doors.map(([c,w])=>[Math.max(a,c-w/2),Math.min(b,c+w/2)]).sort((x,y)=>x[0]-y[0]);let start=a;
  const segment=(s,e,y,height,header=false)=>{if(e-s<.01)return;box('wall',[axis==='x'?at:(s+e)/2,y,axis==='x'?(s+e)/2:at],axis==='x'?[.32,height,e-s]:[e-s,height,.32],material,true,{section:header?'roof':'wall'});
   // Recess trim ends 5 mm from the plaster ends: coplanar end caps flicker at door jambs.
   if(!header){box('skirting',[axis==='x'?at:(s+e)/2,.13,axis==='x'?(s+e)/2:at],axis==='x'?[.37,.25,e-s-.01]:[e-s-.01,.25,.37],'charcoal',false,{section:'wall'});}};
  for(const [s,e] of spans){segment(start,s,h/2,h);segment(s,e,(h+3.65)/2,h-3.65,true);start=e;}
  segment(start,b,h/2,h);
 }
 function beam(a,b,r,mat='bronze',name='rail',section='architecture'){
  add('beam',name,a,[r,0,r],mat,{end:b,section});
 }
 function bench(x,z,w=3,y=0,yaw=0){
  box('bench-seat',[x,y+.46,z],[w,.16,.7],'oak',true,{yaw});
  for(const dx of[-w*.36,w*.36])box('bench-leg',[x+dx,y+.2,z],[.13,.4,.5],'charcoal');
 }
 function rail(x1,z1,x2,z2,y=0){
  const length=Math.hypot(x2-x1,z2-z1),steps=Math.ceil(length/1.8);
  beam([x1,y+1.1,z1],[x2,y+1.1,z2],.045);
  for(let i=0;i<=steps;i++){let t=i/steps;beam([x1+(x2-x1)*t,y,z1+(z2-z1)*t],[x1+(x2-x1)*t,y+1.08,z1+(z2-z1)*t],.025);}
  box('guard-glass',[(x1+x2)/2,y+.55,(z1+z2)/2],[Math.max(Math.abs(x2-x1),.055),.95,Math.max(Math.abs(z2-z1),.055)],'glass',true);
 }
 // Campus plinth and forecourt; no ornamental plants or sculptures.
 box('site',[0,-.3,0],[88,.5,96],'concrete');
 box('ground-floor',[0,-.08,-7],[76,.16,72],'terrazzo');
 box('plaza',[0,-.02,38],[83,.1,18],'paving');
 for(let x=-40;x<=40;x+=4)box('paving-joint',[x,.041,38],[.025,.006,18],'joint');
 for(let z=31;z<=47;z+=4)box('paving-joint',[0,.041,z],[83,.006,.025],'joint');
 for(const side of[-1,1]){
  box('forecourt-seat',[side*15,.34,38],[7,.68,1.6],'limestone',true);
  box('forecourt-inlay',[side*15,.687,38],[6.6,.014,1.35],'oak');
  for(const z of[33,41])cyl('bollard',[side*7,.5,z],.1,1,'bronze',true);
 }
 // Main shell.
 wall('x',-38,-43,29,11.8,[],'plaster');wall('x',38,-43,29,5.6,[],'plaster');
 wall('z',-43,-38,-4,11.8,[],'plaster');wall('z',-43,-4,4,10,[],'plaster');
 wall('z',-43,4,21,8,[],'plaster');wall('z',-43,21,38,5.6,[],'charcoal');
 wall('z',29,-38,-20,5.6,[],'plaster');wall('z',29,20,38,5.6,[],'plaster');
 // Glazed entrance, open central double-width doors.
 for(const [a,b]of[[-20,-4],[4,20]]){
  box('front-glazing',[(a+b)/2,3.8,29],[b-a,7.6,.1],'glass',true);
  for(let x=a;x<=b;x+=4)box('facade-mullion',[x,3.8,29],[.1,7.6,.18],'charcoal');
  for(const y of[.1,3.65,7.65])box('facade-transom',[(a+b)/2,y,29],[b-a,.1,.18],'charcoal');
 }
 box('front-door-header',[0,6.8,29],[8,2.8,.4],'charcoal',true,{section:'roof'});
 box('floating-canopy',[0,8.65,31.5],[47,.45,10],'charcoal',false,{section:'roof'});
 box('canopy-soffit',[0,8.38,31.5],[46,.08,9.7],'oak',false,{section:'roof'});
 for(let x=-22;x<=22;x+=.7)box('canopy-rib',[x,8.28,31.5],[.075,.18,9.7],'bronze',false,{section:'roof'});
 panel('THREE MUSEUM','A MUSEUM FOR THE VERY SMALL. AND THE VERY LARGE.',[0,7.05,29.3],18,1.5,{style:'bronze'});
 // Gallery boundaries and generous portals. Doorway spans are cut, never invisible teleporters.
 wall('x',-4,-43,9,11.8,[[-29,6],[-12,4],[3,6]],'plaster');
 wall('x',4,-43,9,8,[[-29,5],[-15,4],[3,5]],'plaster');
 wall('z',9,-38,-4,11.8,[[-17,8]],'plaster');
 wall('z',9,4,38,5.6,[[11,6],[29,5]],'plaster');
 wall('x',21,-43,9,5.6,[[-27,3.6],[-11,3.6],[3,3.6]],'plaster');
 wall('z',-7,4,21,5.6,[[8,3.6]],'plaster');wall('z',-7,21,38,5.6,[[25,3.6]],'plaster');
 wall('z',-23,4,21,8,[[8,3.6]],'plaster');wall('z',-23,21,38,5.6,[[25,3.6]],'charcoal');
 wall('x',-20,13,29,5.6,[[17,4]],'plaster');wall('x',20,13,29,5.6,[[17,4]],'plaster');
 wall('z',13,-38,-20,5.6,[[-25,4]],'plaster');wall('z',13,20,38,5.6,[[25,4]],'plaster');
 // Materials, ceiling systems and gallery fixtures.
 for(const room of ROOMS){
  const [x1,x2,z1,z2]=room.bounds,cx=(x1+x2)/2,cz=(z1+z2)/2,w=x2-x1,d=z2-z1;
  const floorMat=room.id==='dinosaurs'||room.id==='feature'?'oak':room.id==='theatre'?'carpet':room.id==='court'?'limestone':'terrazzo';
  box(`${room.id}-finish`,[cx,.015,cz],[w-.36,.028,d-.36],floorMat);
  if(room.id==='dinosaurs'){
   // Two solid roof ribbons and a ten-metre northlight, with deep exposed beams.
   box('dinosaur-roof-west',[-31.5,11.8,cz],[13,.22,d],'charcoal',false,{section:'roof'});
   box('dinosaur-roof-east',[-9.5,11.8,cz],[11,.22,d],'charcoal',false,{section:'roof'});
   box('northlight',[-20,11.8,cz],[10,.07,d],'skylight',false,{section:'roof'});
   for(let z=-41;z<9;z+=4){box('dino-beam',[-21,11.1,z],[33.6,.8,.22],'charcoal',false,{section:'roof'});box('skylight-mullion',[-20,11.88,z],[10,.12,.1],'bronze',false,{section:'roof'});}
   for(const x of[-32,-10])for(let z=-33;z<8;z+=8){box('track',[x,9.8,z],[.1,.1,7],'charcoal',false,{section:'roof'});box('linear-light',[x,9.7,z],[.12,.05,4],'light',false,{section:'roof'});}
  }else if(room.id==='court'||room.id==='arrival'){
   box('glazed-roof',[cx,room.height,cz],[w,.08,d],'skylight',false,{section:'roof'});
   for(let z=z1+1;z<z2;z+=3)box('light-court-rib',[cx,room.height-.3,z],[w,.45,.12],'charcoal',false,{section:'roof'});
   for(const x of[x1+.45,x2-.45])for(let z=z1+1;z<z2;z+=8)box('court-column',[x,room.height/2,z],[.2,room.height,.2],'bronze',true);
  }else{
   box('gallery-ceiling',[cx,room.height,cz],[w,.15,d],'charcoal',false,{section:'roof'});
   for(let z=z1+1;z<z2;z+=.65)box('acoustic-fin',[cx,room.height-.27,z],[w-.5,.28,.06],'oakDark',false,{section:'roof'});
   for(const x of[cx-4,cx+4])for(let z=z1+3;z<z2;z+=6){box('ceiling-light',[x,room.height-.46,z],[.18,.04,3.2],'light',false,{section:'roof'});}
  }
  if(!['court','arrival'].includes(room.id))lights.push({position:[cx,Math.min(room.height-1,5),cz],color:room.id==='dinosaurs'?'#ffd7ab':room.color,power:room.id==='theatre'?18:42});
 }
 // Glazed linking roofs over the side portions of Gallery Street.
 for(const x of[-29,29]){box('gallery-street-roof',[x,5.6,11],[18,.08,4],'skylight',false,{section:'roof'});for(const z of[10,12])box('street-roof-rib',[x,5.4,z],[18,.3,.12],'charcoal',false,{section:'roof'});}
 // Flush bronze walking-route inlays. These identify a walk, not a forced route.
 for(const x of[-2.8,2.8])box('court-inlay',[x,.038,-17],[.035,.008,50],'bronze');
 box('gallery-street-inlay',[0,.038,11],[73,.008,.035],'bronze');
 // Welcome desk, slatted feature wall, orienting plaques.
 box('reception',[-11,.57,19],[5.5,1.14,1.65],'limestone',true);
 box('reception-cap',[-11,1.17,19],[5.7,.075,1.8],'oak');
 panel('INFORMATION','YOUR VISIT BEGINS HERE',[-11,.7,19.84],4.2,.65,{style:'light'});
 for(let x=-18.5;x<-5;x+=.35)box('welcome-slat',[x,2.25,14],[.09,4.5,.14],'oak',true);
 panel('From small worlds','to deep time.',[-11.8,2.7,14.14],10,1.45,{style:'light'});
 panel('01  DEEP TIME HALL','DINOSAURS  /  OVERLOOK',[-17,4.5,9.21],9,1.2,{style:'bronze'});
 panel('02  THE BUG GALLERIES','DIVERSITY  /  HABITATS  /  ANATOMY',[14,4.25,9.21],14,1,{style:'green'});
 panel('LIGHT COURT','FOLLOW YOUR CURIOSITY',[0,5.25,6],6.8,1,{style:'green'});
 panel('06  LAST GIANTS','THE FEATURE GALLERY',[12.5,4.35,-22.77],11,1,{style:'bronze'});
 panel('08  DISCOVERY STUDIO','LEARN. LOOK CLOSER. ASK QUESTIONS.',[29,3.7,13.21],11,.9,{style:'light'});
 panel('VISITOR LOUNGE','REST  /  ORIENTATION',[-29,3.7,13.21],10,.9,{style:'light'});
 panel('LIVING HABITATS','A GALLERY OF INTERCONNECTED WORLDS',[28.5,3.95,8.77],12,.8,{style:'green',yaw:Math.PI});
 panel('SMALL WORLDS LAB','STRUCTURE  /  FUNCTION  /  CHANGE',[12.8,3.95,-22.75],12,.8,{style:'green'});
 panel('THE EIGHT-LEGGED ROOM','OBSERVE WITHOUT THE JUMP SCARES',[29,3.95,-22.75],13,.8,{style:'purple'});
 panel('DEEP TIME','A DIFFERENT SENSE OF SCALE',[-21,6.8,-42.77],23,2.5,{style:'bronze'});
 panel('LAST GIANTS','FOSSILS. EVIDENCE. EXTINCTION.',[12.5,5.3,-42.77],12,1.5,{style:'bronze'});
 // Ramp: three 12 m slopes with two 3 m level landings, +2.40 m total.
 for(const seg of RAMP.segments){
  add('ramp','overlook-ramp',[RAMP.x1,0,seg.z1],[RAMP.x2-RAMP.x1,.2,seg.z1-seg.z2],'oak',{...seg,x1:RAMP.x1,x2:RAMP.x2});
  for(const x of[RAMP.x1,RAMP.x2]){
   beam([x,seg.y1+1.1,seg.z1],[x,seg.y2+1.1,seg.z2],.045);
   beam([x,seg.y1+.15,seg.z1],[x,seg.y2+.15,seg.z2],.03);
   const count=Math.ceil((seg.z1-seg.z2)/1.5);
   for(let i=0;i<count;i++){const t=i/count,z=seg.z1+(seg.z2-seg.z1)*t,y=seg.y1+(seg.y2-seg.y1)*t;beam([x,y,z],[x,y+1.1,z],.025);}
   // A low, continuous collision barrier also closes the intentionally unused under-ramp space.
   const n=Math.ceil(seg.z1-seg.z2);for(let i=0;i<n;i++){let t=(i+.5)/n,z=seg.z1+(seg.z2-seg.z1)*t,top=seg.y1+(seg.y2-seg.y1)*t+1.1;colliders.push({id:'ramp-side',min:[x-.055,-.15,z-(seg.z1-seg.z2)/n/2],max:[x+.055,top,z+(seg.z1-seg.z2)/n/2]});}
  }
 }
 const [dx1,dx2,dz1,dz2]=DECK.bounds;
 box('overlook-deck',[(dx1+dx2)/2,2.27,(dz1+dz2)/2],[dx2-dx1,.26,dz2-dz1],'oak',true);
 rail(-34.15,-36,-4.6,-36,2.4);rail(-4.6,-36,-4.6,-42.5,2.4);
 panel('THE LONG VIEW','RAMP TO THE DEEP TIME OVERLOOK',[-35.8,2.8,7.9],3.1,.95,{style:'bronze'});
 bench(-26,-40,4,2.4);bench(-8,-40,3,2.4);
 // Display architecture only; absolutely no bug, fossil, dinosaur or plant meshes.
 for(const e of EXHIBITS){
  const[x,y,z]=e.position,[w,h,d]=e.envelope;
  if(e.kind==='suspended'){
   for(const ax of[-w*.35,w*.35])beam([x+ax,11,z],[x+ax,y+h,z],.012,'charcoal','future-rigging','roof');
  }else if(e.kind==='split'){
   for(const s of[-1,1]){const pz=z+s*8.75;box(`${e.id}-island`,[x,.14,pz],[w+.45,.28,10.5],'limestone',true);box('island-cap',[x,.288,pz],[w+.49,.018,10.54],'bronze');}
  }else if(e.kind==='plinth'){
   box(`${e.id}-plinth`,[x,y/2,z],[w+.35,y,d+.35],'limestone',true);
   box('plinth-reveal',[x,y*.4,z],[w+.43,.045,d+.43],'charcoal');
   box('plinth-top',[x,y-.018,z],[w+.25,.03,d+.25],'sand');
  }else if(e.kind==='wall'){
   const side=w<d;
   const fy=y+h/2,front=side?1:(z>0?-1:1);
   // Backing and rails fit between the uprights, avoiding coplanar exterior faces.
   if(side){
    box('cabinet-back',[x-w/2-.03,fy,z],[.06,h,d],'linen');
    for(const az of[-1,1])box('cabinet-jamb',[x,fy,z+az*(d/2+.035)],[w+.1,h+.14,.07],'oakDark');
    for(const ay of[-1,1])box('cabinet-rail',[x,fy+ay*(h/2+.035),z],[w+.1,.07,d],'oakDark');
    box('cabinet-front',[x+w/2+.025,fy,z],[.02,h,d],'glass');
   }else{
    box('cabinet-back',[x,fy,z-front*(d/2+.03)],[w,h,.06],'linen');
    for(const ax of[-1,1])box('cabinet-jamb',[x+ax*(w/2+.035),fy,z],[.07,h+.14,d+.1],'oakDark');
    for(const ay of[-1,1])box('cabinet-rail',[x,fy+ay*(h/2+.035),z],[w,.07,d+.1],'oakDark');
    box('cabinet-front',[x,fy,z+front*(d/2+.025)],[w,h,.02],'glass');
   }
   colliders.push({id:e.id+'-wallcase',min:[x-w/2-.08,y-.07,z-d/2-.08],max:[x+w/2+.08,y+h+.07,z+d/2+.08]});
  }else if(e.kind==='planter'){
   box('planter-soil',[x,.07,z],[w,.1,d],'soil',true);
   for(const sx of[-1,1])box('planter-side',[x+sx*(w/2+.1),y/2,z],[.2,y,d+.4],'limestone',true);
   for(const sz of[-1,1])box('planter-end',[x,y/2,z+sz*(d/2+.1)],[w,.55,.2],'limestone',true);
  }else{
   const baseY=y, floorY=e.id==='D09'?2.4:0;
   box(`${e.id}-base`,[x,(baseY+floorY)/2,z],[w+.2,baseY-floorY,d+.2],e.kind==='habitat'?'oakDark':'limestone',true);
   box('case-reveal',[x,baseY-.05,z],[w+.26,.045,d+.26],'charcoal');
   box('display-bed',[x,baseY+.012,z],[w,.024,d],'linen');
   if(e.kind==='case'||e.kind==='habitat'){
    for(const sx of[-1,1]){box('case-glass-side',[x+sx*w/2,y+h/2,z],[.035,h,d],'glass',true);for(const sz of[-1,1])box('case-upright',[x+sx*w/2,y+h/2,z+sz*d/2],[.045,h,.045],'bronze');}
    for(const sz of[-1,1])box('case-glass-front',[x,y+h/2,z+sz*d/2],[w,h,.035],'glass',true);
    box('case-cap',[x,y+h,z],[w+.1,.08,d+.1],e.kind==='habitat'?'oakDark':'bronze');
    box('case-lamp',[x,y+h-.05,z],[w*.8,.025,.16],'light');
   }
  }
  // Labels are fixtures. Visitors see a human-scale, intentionally empty museum, not debug cubes.
  if(e.kind!=='wall' && e.kind!=='suspended' && e.kind!=='planter'){
   const signX=e.view[0],signZ=e.view[2];
   // Keep the reading position itself clear: labels sit 0.6 m towards the display.
   let vx=x-signX,vz=z-signZ,len=Math.hypot(vx,vz)||1;vx/=len;vz/=len;
   const px=signX+vx*.9,pz=signZ+vz*.9,py=(e.view[1]||0)+1.05;
   box('label-stem',[px,(py+(e.id==='D09'?2.4:0))/2,pz],[.06,py-(e.id==='D09'?2.4:0),.06],'bronze',false);
   const yaw=Math.atan2(signX-px,signZ-pz);
   panel(`${e.id}  /  ${e.title}`,e.subject.toUpperCase(),[px,py,pz],e.id==='D01'?2:1.65,.48,{style:'light',yaw,exhibit:e.id});
  }
 }
 // Gallery benches, a quiet lounge and a useful teaching shell.
 bench(-7,-7,3);bench(-32,1,2.5);bench(6.6,-1.5,2.5);bench(23.2,-19,2.8);
 bench(0,-22.4,2.3);bench(0,-38,2.3);
 for(const z of[21,25]){bench(-32,z,5);bench(-25,z,4);}
 panel('Take your time.','THIS IS A PLACE TO LOOK CLOSER.',[-29,2.8,28.7],12,1.5,{style:'light',yaw:Math.PI});
 // Theatre: level aisles and bench rows, no movie or creature content is provided.
 box('cinema-screen',[29.5,2.35,-42.65],[13,3.6,.1],'screen');
 panel('BIG QUESTIONS','A QUIET SPACE FOR FUTURE STORIES',[29.5,2.6,-42.56],11,1.8,{style:'screen'});
 for(const z of[-38,-34.5,-31]){bench(28,z,4.3);bench(34,z,3.6);}
 for(const [x,z]of[[23,25.5],[23,21]]){box('studio-stool',[x,.42,z],[.55,.84,.55],'oakDark',true);}
 // Site boundary is explicit; no falling off the map or walking through external walls.
 const [bx1,bx2,bz1,bz2]=BOUNDS;
 for(const b of[{min:[bx1-.5,-2,bz1],max:[bx1,20,bz2]},{min:[bx2,-2,bz1],max:[bx2+.5,20,bz2]},{min:[bx1,-2,bz1-.5],max:[bx2,20,bz1]},{min:[bx1,-2,bz2],max:[bx2,20,bz2+.5]}])colliders.push({id:'site-boundary',...b});
 return {version:1,units:'metres',north:'-Z',pieces,colliders,panels,lights,rooms:ROOMS,exhibits:EXHIBITS,ramp:RAMP,deck:DECK,visitorRoute:VISITOR_ROUTE};
}
