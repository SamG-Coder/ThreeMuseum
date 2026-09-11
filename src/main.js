import * as THREE from 'three';
import {buildArchitecture} from './world/architecture.js';
import {renderArchitecture} from './world/renderWorld.js';
import {makeEnvironment} from './world/materials.js';
import {ROOMS,EXHIBITS,getRoom} from './world/layout.js';
import {NavigationWorld,groundHeight} from './player/navigation.js';
import {VisitorController} from './player/VisitorController.js';
import {ExhibitAssets} from './assets/ExhibitAssets.js';
import {drawMuseumMap} from './ui/map.js';
import {COLLECTION,COLLECTION_NOTE} from './world/collection.js';

const $=id=>document.getElementById(id), canvas=$('world');
const data=buildArchitecture();
const renderer=new THREE.WebGLRenderer({canvas,antialias:true,powerPreference:'high-performance'});
renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.15;
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
const scene=new THREE.Scene();scene.background=new THREE.Color('#bccac4');
const camera=new THREE.PerspectiveCamera(65,innerWidth/innerHeight,.08,260);
const world=renderArchitecture(data);scene.add(world.root);
const environment=makeEnvironment(renderer);scene.environment=environment.texture;scene.environmentIntensity=.85;
scene.add(new THREE.HemisphereLight('#f6f3e5','#7f7462',1.6));
const sun=new THREE.DirectionalLight('#fff0d3',2.5);sun.position.set(-20,48,18);sun.target.position.set(0,0,-10);
sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);sun.shadow.camera.left=-58;sun.shadow.camera.right=58;sun.shadow.camera.top=58;sun.shadow.camera.bottom=-58;sun.shadow.camera.near=1;sun.shadow.camera.far=130;sun.shadow.bias=-.00018;sun.shadow.normalBias=.055;scene.add(sun,sun.target);
// A fixed light budget avoids adding a separate real-time light to every empty case.
const fillLights=Array.from({length:4},()=>{const l=new THREE.PointLight('#fff1d9',55,30,1);scene.add(l);return l;});
const navigation=new NavigationWorld(data.colliders), visitor=new VisitorController(camera,canvas,navigation);
let toastTimer;function notify(text){$('toast').textContent=text;$('toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').hidden=true,6500);}
const assets=new ExhibitAssets(world.anchors,notify);
const modal=$('modal'),body=$('dialog-body');
let started=false,architect=false,helpers=false,nearest=null,selectedID='D01';
const orbit={yaw:.48,elevation:.92,distance:111,target:new THREE.Vector3(0,0,-8),drag:null};
const coarse=matchMedia('(pointer:coarse)').matches;
const settings={quality:coarse?'low':'standard',fov:65,speed:2.2,eyeHeight:1.62,sensitivity:.002};
try{const saved=JSON.parse(localStorage.getItem('three-museum-settings')||'{}');for(const k of Object.keys(settings))if(typeof saved[k]===typeof settings[k])settings[k]=saved[k];}catch{/* Private browsing and invalid saved state must not block a visit. */}
function applySettings(){
 settings.fov=THREE.MathUtils.clamp(settings.fov,50,90);settings.speed=THREE.MathUtils.clamp(settings.speed,1,4);
 settings.eyeHeight=THREE.MathUtils.clamp(settings.eyeHeight,1.1,1.8);settings.sensitivity=THREE.MathUtils.clamp(settings.sensitivity,.0005,.005);
 visitor.eyeHeight=settings.eyeHeight;visitor.walkSpeed=settings.speed;visitor.sensitivity=settings.sensitivity;
 camera.fov=settings.fov;camera.updateProjectionMatrix();
 renderer.setPixelRatio(Math.min(devicePixelRatio,settings.quality==='low'?1:1.5));renderer.shadowMap.enabled=settings.quality!=='low';
 try{localStorage.setItem('three-museum-settings',JSON.stringify(settings));}catch{}
 resize();
}
function resize(){renderer.setSize(innerWidth,innerHeight,false);camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();}
window.addEventListener('resize',resize);applySettings();

function releaseMouse(){if(document.pointerLockElement)document.exitPointerLock();visitor.clearInput();}
function openDialog(title,tag='THREE MUSEUM'){
 releaseMouse();visitor.active=false;$('dialog-title').textContent=title;$('dialog-tag').textContent=tag;body.replaceChildren();
 if(!modal.open)modal.showModal();
}
function closeDialog(){modal.close();}
$('close-modal').onclick=closeDialog;
modal.addEventListener('close',()=>{visitor.clearInput();visitor.active=started&&!architect;});
modal.addEventListener('click',e=>{if(e.target===modal){const b=modal.getBoundingClientRect();if(e.clientX<b.left||e.clientX>b.right||e.clientY<b.top||e.clientY>b.bottom)closeDialog();}});
function setArchitect(value){
 architect=value;releaseMouse();visitor.active=started&&!architect&&!modal.open;world.roof.visible=!architect;
 $('mode-button').textContent=architect?'Return to visitor  V':'Architect  V';$('crosshair').hidden=architect||!started;
 $('touch-controls').hidden=architect||!started;$('interact-prompt').hidden=true;
 if(!architect)visitor.updateCamera();else notify('Architect view: drag to orbit, scroll to zoom. V returns to your walking position.');
}
function start(){
 started=true;document.body.classList.add('started');$('welcome').hidden=true;$('edition').hidden=true;
 for(const id of['toolbar','location-card','mini-map','controls','crosshair','touch-controls'])$(id).hidden=false;
 visitor.active=true;visitor.updateCamera();if(!coarse)visitor.lock();
}
$('enter').onclick=start;
$('mode-button').onclick=()=>setArchitect(!architect);
canvas.addEventListener('dblclick',()=>{if(started&&!architect&&!modal.open&&!coarse)visitor.lock();});
canvas.addEventListener('pointerdown',e=>{if(architect&&!modal.open){orbit.drag={x:e.clientX,y:e.clientY,id:e.pointerId};canvas.setPointerCapture(e.pointerId);}});
canvas.addEventListener('pointermove',e=>{if(architect&&orbit.drag?.id===e.pointerId){orbit.yaw-=(e.clientX-orbit.drag.x)*.006;orbit.elevation=THREE.MathUtils.clamp(orbit.elevation+(e.clientY-orbit.drag.y)*.005,.3,1.48);orbit.drag={x:e.clientX,y:e.clientY,id:e.pointerId};}});
for(const event of['pointerup','pointercancel'])canvas.addEventListener(event,()=>orbit.drag=null);
canvas.addEventListener('wheel',e=>{if(architect){e.preventDefault();orbit.distance=THREE.MathUtils.clamp(orbit.distance*Math.exp(e.deltaY*.001),20,180);}}, {passive:false});

function goTo(p,yaw=0){
 if(!visitor.teleport(p,yaw)){notify('That position is obstructed. Use a room entrance instead.');return false;}
 if(architect)setArchitect(false);closeDialog();visitor.active=started;return true;
}
function mapDialog(){
 openDialog('Find your next discovery','VISITOR MAP / M');
 body.innerHTML='<div class="map-layout"><canvas id="large-map" width="660" height="740" aria-label="Museum floor plan"></canvas><div class="room-list" id="room-list"></div></div>';
 drawMuseumMap($('large-map'),visitor.state,data.colliders,true);
 const list=$('room-list');
 for(const r of [...ROOMS,{id:'overlook',name:'Deep Time Overlook',tag:'LEVEL 01 / +2.40 M',spawn:[-20,2.4,-38]}]){
  const button=document.createElement('button');button.innerHTML=`<small>${r.tag}</small><strong>${r.name}</strong><span>Go to entrance ↗</span>`;button.onclick=()=>goTo(r.spawn);list.append(button);
 }
 const plan=document.createElement('a');plan.className='document-link';plan.textContent='Open measured plans ↗';plan.href='./public/plans/index.html';plan.target='_blank';plan.rel='noopener';list.append(plan);
}
$('map-button').onclick=mapDialog;

function showExhibit(e){
 if(!e)return;selectedID=e.id;openDialog(e.title,`${e.id} / EXHIBIT DESIGN`);
 body.innerHTML=`<p class="lead">${e.subject}</p><p>${e.brief}</p><div class="meta-grid"><div><small>RESERVED ENVELOPE</small><strong>${e.envelope.join(' × ')} m</strong><span>Width × height × depth</span></div><div><small>DISPLAY TYPE</small><strong>${e.kind}</strong><span>Empty architectural fixture</span></div><div><small>MODEL ORIGIN</small><strong>${e.position.join(' / ')}</strong><span>X / Y / Z · bottom centre</span></div></div><p class="notice">This is an installation brief, not a finished scientific label. No specimen is currently loaded at this slot.</p><div class="button-row"><button class="primary" id="edit-this">Install a Blender model</button><button id="close-card">Continue exploring</button></div>`;
 if(assets.loaded.has(e.id)&&COLLECTION[e.id]){
  const [title,description]=COLLECTION[e.id];
  $('dialog-title').textContent=title;
  $('dialog-tag').textContent=`${e.id} / THE COLLECTION`;
  const note=e.id==='F01'?'Smithsonian Institution · CC0. This is not Melbourne Museum’s Horridus specimen.':COLLECTION_NOTE;
  body.innerHTML=`<p class="lead">${e.subject}</p><p>${description}</p><p class="notice">${note}</p><div class="button-row"><button class="primary" id="close-card">Continue exploring</button><button id="edit-this">Inspect installation</button></div>`;
 }
 $('edit-this').onclick=()=>installDialog(e.id);$('close-card').onclick=closeDialog;
}
$('interact-prompt').onclick=()=>showExhibit(nearest);
$('touch-interact').onclick=()=>nearest?showExhibit(nearest):notify('Walk closer to a labelled display to explore the exhibit.');

function saveManifest(){
 const blob=new Blob([JSON.stringify(assets.export(),null,2)+'\n'],{type:'application/json'}),url=URL.createObjectURL(blob);
 const a=document.createElement('a');a.href=url;a.download='exhibits.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
 notify('Replace public/exhibits.json with this file and copy your GLBs into public/models. The browser cannot write into your project folder.');
}
function installDialog(id=selectedID){
 selectedID=id;helpers=true;world.helpers.visible=true;openDialog('Exhibit installation','BLENDER HANDOFF / B');
 body.innerHTML=`<div class="install-top"><label class="field">Exhibit position<select id="exhibit-select"></select></label><button id="save-manifest">Export manifest ↓</button></div><div id="installation-content"></div>`;
 const select=$('exhibit-select');for(const e of EXHIBITS){const o=document.createElement('option');o.value=e.id;o.textContent=`${e.id} — ${e.subject}`;select.append(o);}select.value=id;select.onchange=()=>{selectedID=select.value;renderInstall();};
 $('save-manifest').onclick=saveManifest;renderInstall();
}
function renderInstall(){
 const e=assets.entries.get(selectedID),host=$('installation-content');
 host.innerHTML=`<h3>${e.title}</h3><p>${e.brief}</p><p class="badge">${e.id} · ${e.envelope.join(' × ')} m · bottom-centre origin</p><p id="asset-state"></p><label class="file-input">Choose a self-contained .glb <input id="glb-file" type="file" accept=".glb,model/gltf-binary"></label><div class="transform-grid" id="transform-fields"></div><div class="button-row"><button id="fit-model">Fit to envelope</button><button id="reset-model">Reset transform</button><button id="remove-model">Remove model</button><button id="visit-bay">Go to this bay ↗</button></div><p class="notice">Local GLB previews last for this session only. Copy the file into public/models, export the manifest, and replace public/exhibits.json. Compressed Draco/KTX2 assets require additional decoders and are not supported by this baseline loader. Imported models do not automatically become collision geometry.</p><label><input id="helper-toggle" type="checkbox" checked> Show installation envelopes</label>`;
 $('asset-state').textContent=assets.loaded.has(e.id)?'Loaded · '+(e.url||'session model'):'No model loaded · the display is intentionally empty.';
 const fields=$('transform-fields');
 for(const group of['offset','rotation'])for(let i=0;i<3;i++){
  const label=document.createElement('label');label.className='field';label.textContent=`${group==='offset'?'Offset':'Rotation'} ${'XYZ'[i]} ${group==='offset'?'(m)':'(°)'}`;
  const input=document.createElement('input');input.type='number';input.step=group==='offset'?'.01':'1';input.value=e[group][i];
  input.onchange=()=>{const value=Number(input.value);if(!Number.isFinite(value)||input.value.trim()===''){input.value=e[group][i];return;}e[group][i]=value;assets.apply(e.id);const warning=assets.checkEnvelope(e.id);if(warning)notify(warning);};label.append(input);fields.append(label);
 }
 const scaleLabel=document.createElement('label');scaleLabel.className='field';scaleLabel.textContent='Uniform scale';const scale=document.createElement('input');scale.type='number';scale.min='.0001';scale.step='.01';scale.value=e.scale;scale.onchange=()=>{const value=Number(scale.value);if(!Number.isFinite(value)||value<=0){scale.value=e.scale;return;}e.scale=value;assets.apply(e.id);const warning=assets.checkEnvelope(e.id);if(warning)notify(warning);};scaleLabel.append(scale);fields.append(scaleLabel);
 $('glb-file').onchange=async event=>{const file=event.target.files?.[0];if(!file)return;event.target.disabled=true;try{await assets.loadFile(e.id,file);}catch(err){notify(err.message);}finally{if(modal.open&&selectedID===e.id&&$('installation-content'))renderInstall();}};
 $('fit-model').onclick=()=>{assets.fit(e.id);renderInstall();};
 $('reset-model').onclick=()=>{e.offset=[0,0,0];e.rotation=[0,0,0];e.scale=1;assets.apply(e.id);renderInstall();};
 $('remove-model').onclick=()=>{assets.remove(e.id);e.url=null;renderInstall();};
 $('helper-toggle').checked=helpers;$('helper-toggle').onchange=event=>{helpers=event.target.checked;world.helpers.visible=helpers;};
 $('visit-bay').onclick=()=>{
  helpers=false;world.helpers.visible=false;
  const p=[...e.view];p[1]=groundHeight(p[0],p[2],3);const yaw=Math.atan2(p[0]-e.position[0],p[2]-e.position[2]);
  if(!goTo(p,yaw)){const r=ROOMS.find(r=>r.id===e.room);goTo(r.spawn,yaw);}
 };
}
$('install-button').onclick=()=>installDialog();

function settingsDialog(){
 openDialog('Make yourself comfortable','VISITOR SETTINGS');
 body.innerHTML=`<div class="settings-grid"><label class="field">Field of view<input id="set-fov" type="range" min="50" max="90" step="1"><output id="fov-output"></output></label><label class="field">Walking speed<input id="set-speed" type="range" min="1" max="4" step=".1"><output id="speed-output"></output></label><label class="field">Eye height<select id="set-eye"><option value="1.62">Standing · 1.62 m</option><option value="1.2">Lower viewpoint · 1.20 m</option></select></label><label class="field">Look sensitivity<input id="set-sensitivity" type="range" min=".0005" max=".005" step=".0001"></label><label class="field">Graphics<select id="set-quality"><option value="standard">Standard · soft sun shadow</option><option value="low">Low · no shadow map</option></select></label></div><p class="notice">No camera bob, jump scares, automatic sound, motion blur or forced tour. Arrow keys look around without mouse capture. Map destinations provide an alternative to continuous walking. This is not a substitute for a real accessibility audit.</p><div class="button-row"><button id="full-screen">Toggle full screen</button><button id="home-position">Return to arrival</button><button id="hide-guides">Hide installation guides</button></div>`;
 for(const[key,id]of[['fov','set-fov'],['speed','set-speed'],['sensitivity','set-sensitivity'],['eyeHeight','set-eye'],['quality','set-quality']]){
  $(id).value=settings[key];$(id).oninput=event=>{settings[key]=key==='quality'?event.target.value:Number(event.target.value);applySettings();updateOutputs();};
 }
 function updateOutputs(){$('fov-output').textContent=settings.fov+'°';$('speed-output').textContent=settings.speed.toFixed(1)+' metres / second';}updateOutputs();
 $('full-screen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch{notify('Full screen is not available in this browser context.');}};
 $('home-position').onclick=()=>goTo([0,0,23]);$('hide-guides').onclick=()=>{helpers=false;world.helpers.visible=false;notify('Installation guides hidden.');};
}
$('settings-button').onclick=settingsDialog;
window.addEventListener('keydown',e=>{
 if(!started||e.repeat||/INPUT|SELECT|TEXTAREA/.test(document.activeElement?.tagName||''))return;
 if(modal.open)return;
 if(e.code==='KeyM'){e.preventDefault();mapDialog();}
 if(e.code==='KeyB'){e.preventDefault();installDialog();}
 if(e.code==='KeyV'){e.preventDefault();setArchitect(!architect);}
 if(e.code==='KeyE'&&nearest&&!architect){e.preventDefault();showExhibit(nearest);}
});
// Separate pointer IDs let one thumb move while the other looks around.
const stick=$('joystick'),thumb=$('joystick-thumb');let stickPointer=null;
function moveStick(e){const r=stick.getBoundingClientRect(),dx=(e.clientX-r.left-r.width/2)/(r.width*.35),dy=(e.clientY-r.top-r.height/2)/(r.height*.35),length=Math.max(1,Math.hypot(dx,dy));visitor.touchMove.x=dx/length;visitor.touchMove.y=dy/length;thumb.style.transform=`translate(${visitor.touchMove.x*28}px,${visitor.touchMove.y*28}px)`;}
stick.addEventListener('pointerdown',e=>{e.preventDefault();stickPointer=e.pointerId;stick.setPointerCapture(e.pointerId);moveStick(e);});
stick.addEventListener('pointermove',e=>{if(stickPointer===e.pointerId)moveStick(e);});
for(const name of['pointerup','pointercancel','lostpointercapture'])stick.addEventListener(name,()=>{stickPointer=null;visitor.touchMove.x=visitor.touchMove.y=0;thumb.style.transform='';});

function updateNearby(){
 nearest=null;let distance=4.5;const s=visitor.state,room=getRoom(s.x,s.z,s.y);
 for(const e of EXHIBITS){if(e.room!==room.id&&!(room.id==='overlook'&&e.id==='D09'))continue;const p=e.view,d=Math.hypot(s.x-p[0],s.z-p[2]);if(d<distance&&Math.abs(s.y-groundHeight(p[0],p[2],3))<1.2){distance=d;nearest=e;}}
 $('interact-prompt').hidden=!nearest||architect||modal.open||!started;
 if(nearest)$('interact-prompt').querySelector('span').textContent=`${nearest.id} · ${nearest.title}`;
 $('location-tag').textContent=architect?'ARCHITECTURE / CUTAWAY':room.tag;
 $('location-name').textContent=architect?'The whole museum':room.name;
 $('mode-label').textContent=architect?'DRAG TO ORBIT / SCROLL TO ZOOM':s.y>.1?`VISITOR / +${s.y.toFixed(2)} M`:'VISITOR / GROUND LEVEL';
 $('coords').textContent=`${s.x.toFixed(1)} / ${s.z.toFixed(1)}`;
 drawMuseumMap($('minimap-canvas'),s,data.colliders);
 const sorted=data.lights.map(l=>({l,d:(l.position[0]-camera.position.x)**2+(l.position[2]-camera.position.z)**2})).sort((a,b)=>a.d-b.d);
 fillLights.forEach((light,i)=>{const item=sorted[i]?.l;if(item){light.position.set(...item.position);light.color.set('#ffebcf').lerp(new THREE.Color(item.color),.1);light.intensity=item.power;}});
}
let previous=performance.now(),hudTime=0,fpsTime=0,frames=0;
let director=null;
function frame(now){
 const dt=Math.min((now-previous)/1000,.05);previous=now;
 if(director){director(now);}
 else if(architect){const c=Math.cos(orbit.elevation);camera.position.set(orbit.target.x+Math.sin(orbit.yaw)*orbit.distance*c,orbit.target.y+Math.sin(orbit.elevation)*orbit.distance,orbit.target.z+Math.cos(orbit.yaw)*orbit.distance*c);camera.lookAt(orbit.target);}
 else if(started)visitor.update(dt);
 assets.update(dt);renderer.render(scene,camera);
 if(now-hudTime>150){updateNearby();hudTime=now;}
 frames++;if(now-fpsTime>1000){$('performance').textContent=`${Math.round(frames*1000/(now-fpsTime))} fps · ${renderer.info.render.calls} draws`;fpsTime=now;frames=0;}
 requestAnimationFrame(frame);
}
// A deliberate exterior welcome composition; entering returns to the saved visitor pose.
camera.position.set(16,5.8,43);camera.lookAt(-6,3,5);
$('loading-status').textContent='Museum ready. Loading the specimen collection…';$('enter').disabled=false;$('enter').innerHTML='Enter the museum <span>↗</span>';
requestAnimationFrame(frame);assets.readManifest().then(()=>{
 $('specimen-count').textContent=assets.loaded.size;
 $('loading-status').textContent=`${assets.loaded.size} of ${EXHIBITS.length} exhibit installations loaded. Ready to explore.`;
 if(new URLSearchParams(location.search).has('director'))import('./director.js').then(({createDirector})=>{
  director=createDirector({camera,world,assets,data,visitor,fillLights,mapDialog,settingsDialog,installDialog,showExhibit,closeDialog});
 });
});
canvas.addEventListener('webglcontextlost',event=>{event.preventDefault();visitor.active=false;notify('Graphics context lost. Reload the page to restore the museum.');});
// Explicit, inspectable diagnostics for local testing and future integration.
window.__THREE_MUSEUM__={data,scene,camera,renderer,world,navigation,visitor,assets,setArchitect,goTo,version:'1.0.0'};

