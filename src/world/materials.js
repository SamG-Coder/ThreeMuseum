import * as THREE from 'three';
let seed=20817;const random=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
export function canvasTexture(width,height,paint){const c=document.createElement('canvas');c.width=width;c.height=height;paint(c.getContext('2d'),width,height);const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=8;return t;}
function surface(kind){return canvasTexture(512,512,(c,w,h)=>{
 if(kind==='wood'){
  c.fillStyle='#9b7650';c.fillRect(0,0,w,h);
  for(let p=0;p<8;p++){const x=p*64,v=Math.floor(random()*20);c.fillStyle=`rgb(${143+v},${109+v},${76+v})`;c.fillRect(x,0,64,h);c.fillStyle='#745a42';c.fillRect(x,0,1,h);
   for(let i=0;i<80;i++){c.strokeStyle=`rgba(53,32,16,${random()*.12})`;c.lineWidth=.4+random();c.beginPath();let gx=x+random()*62;c.moveTo(gx,0);for(let y=0;y<=512;y+=16)c.lineTo(gx+Math.sin(y*.018+i)*1.8,y);c.stroke();}
   c.fillStyle='rgba(51,37,27,.25)';c.fillRect(x,(p%2)*256,64,1);
  }
 }else{
  c.fillStyle=kind==='sand'?'#b4a28b':'#c5c4b9';c.fillRect(0,0,w,h);
  for(let i=0;i<18000;i++){const v=random(),a=.03+random()*.1;c.fillStyle=v>.5?`rgba(255,255,244,${a})`:`rgba(32,37,36,${a})`;const r=kind==='stone'?random()*2.2:random()*1.1;c.fillRect(random()*w,random()*h,r+.4,r+.4);}
  if(kind==='stone')for(let i=0;i<250;i++){c.fillStyle=['#aaafa6','#9a9b95','#dfddcf','#7e837e'][i%4];c.beginPath();c.ellipse(random()*w,random()*h,1+random()*3,1+random()*2,random()*3,0,Math.PI*2);c.fill();}
 }
 });}
export function makeMaterials(){
 const wood=surface('wood'),stone=surface('stone'),sand=surface('sand');for(const t of[wood,stone,sand])t.wrapS=t.wrapT=THREE.RepeatWrapping;
 const std=(color,roughness=.7,metalness=0,map=null)=>new THREE.MeshStandardMaterial({color,roughness,metalness,map});
 const m={
  plaster:std('#eee9dc',.88),concrete:std('#969f9b',.96),paving:std('#a2aaa6',.92),joint:std('#737d77',.95),
  terrazzo:std('#f0ede4',.66,0,stone),limestone:std('#e1d9c5',.73,0,sand),sand:std('#d4c6ae',.94,0,sand),
  oak:std('#c6a57c',.52,0,wood),oakDark:std('#776448',.67,0,wood),charcoal:std('#282f31',.75,.14),
  bronze:std('#bc9360',.31,.7),linen:std('#e2dcc9',.97),soil:std('#433e33',1),carpet:std('#4d5a5c',1),
  glass:new THREE.MeshPhysicalMaterial({color:'#c1e1d9',roughness:.14,metalness:.08,transparent:true,opacity:.16,depthWrite:false,side:THREE.DoubleSide}),
  skylight:new THREE.MeshStandardMaterial({color:'#d6e6e2',emissive:'#adcbc7',emissiveIntensity:.65,roughness:.3,transparent:true,opacity:.32,depthWrite:false,side:THREE.DoubleSide}),
  light:new THREE.MeshBasicMaterial({color:'#fff1cd',toneMapped:false}),screen:std('#172527',.8),
 };return m;
}
export function makeEnvironment(renderer){
 const tex=canvasTexture(1024,512,(c,w,h)=>{
  const g=c.createLinearGradient(0,0,0,h);g.addColorStop(0,'#dce6e3');g.addColorStop(.45,'#b9c6c0');g.addColorStop(.51,'#747d77');g.addColorStop(1,'#4d463e');c.fillStyle=g;c.fillRect(0,0,w,h);
  for(const x of[90,310,560,790]){c.fillStyle='#fff3d8';c.fillRect(x,80,36,170);c.fillStyle='#effcf7';c.fillRect(x+50,110,100,35);}
 });tex.mapping=THREE.EquirectangularReflectionMapping;
 const pmrem=new THREE.PMREMGenerator(renderer);const target=pmrem.fromEquirectangular(tex);tex.dispose();pmrem.dispose();return target;
}
