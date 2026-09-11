/** All dimensions are metres. Three.js Y is up, north is -Z. This is an original design, not an as-built survey. */
export const ROOMS = [
 {id:'arrival',name:'Arrival hall',tag:'WELCOME',bounds:[-20,20,9,29],height:9,color:'#bd9c68',spawn:[0,0,23]},
 {id:'dinosaurs',name:'Deep Time Hall',tag:'01 / DINOSAURS',bounds:[-38,-4,-43,9],height:11.8,color:'#d7a86c',spawn:[-16,0,5]},
 {id:'court',name:'Light Court',tag:'THE CONNECTING WALK',bounds:[-4,4,-43,9],height:10,color:'#a8b9a2',spawn:[0,0,0]},
 {id:'diversity',name:'Cabinet of Diversity',tag:'02 / BUGS',bounds:[4,21,-7,9],height:5.6,color:'#86b7a4',spawn:[8,0,5]},
 {id:'habitats',name:'Living Habitats',tag:'03 / BUGS',bounds:[21,38,-7,9],height:5.6,color:'#809e76',spawn:[25,0,5]},
 {id:'anatomy',name:'Small Worlds Lab',tag:'04 / BUGS',bounds:[4,21,-23,-7],height:5.6,color:'#7faeb0',spawn:[8,0,-11]},
 {id:'arachnids',name:'The Eight-legged Room',tag:'05 / INVERTEBRATES',bounds:[21,38,-23,-7],height:5.6,color:'#a69eb9',spawn:[25,0,-11]},
 {id:'feature',name:'Last Giants',tag:'06 / FEATURE GALLERY',bounds:[4,21,-43,-23],height:8,color:'#be9174',spawn:[8,0,-27]},
 {id:'theatre',name:'Big Questions Theatre',tag:'07 / QUIET CINEMA',bounds:[21,38,-43,-23],height:5.6,color:'#8297a6',spawn:[25,0,-27]},
 {id:'learning',name:'Discovery Studio',tag:'08 / LEARNING',bounds:[20,38,13,29],height:5.6,color:'#c0b387',spawn:[23,0,17]},
 {id:'rest',name:'Visitor lounge',tag:'REST & ORIENTATION',bounds:[-38,-20,13,29],height:5.6,color:'#a9b4ac',spawn:[-24,0,17]},
];
export const BOUNDS = [-44,44,-48,48];
export const PLAYER_SPAWN = [0,0,23];
export const RAMP = {x1:-37.45,x2:-34.15, segments:[
 {z1:6,z2:-6,y1:0,y2:.8}, {z1:-6,z2:-9,y1:.8,y2:.8},
 {z1:-9,z2:-21,y1:.8,y2:1.6}, {z1:-21,z2:-24,y1:1.6,y2:1.6},
 {z1:-24,z2:-36,y1:1.6,y2:2.4}
]};
export const DECK = {bounds:[-37.45,-4.55,-42.5,-36],y:2.4};
export const SOURCES = [
 {id:'S1',title:'Museums Victoria — Bugs Alive!',url:'https://museumsvictoria.com.au/melbournemuseum/whats-on/bugs-alive/'},
 {id:'S2',title:'Museums Victoria — Dinosaur Walk',url:'https://museumsvictoria.com.au/melbournemuseum/whats-on/dinosaur-walk/'},
 {id:'S3',title:'Museums Victoria — Dinosaur Walk learning resources',url:'https://museumsvictoria.com.au/melbournemuseum/resources/dinosaur-walk/'},
 {id:'S4',title:'Museums Victoria — Triceratops: Fate of the Dinosaurs',url:'https://museumsvictoria.com.au/melbournemuseum/whats-on/triceratops-fate-of-the-dinosaurs/'},
 {id:'S5',title:'Museums Victoria — Visitor map (27 July 2026)',url:'https://museumsvictoria.com.au/media/ux5heeeh/melbourne-museum-map-27072026.pdf'},
 {id:'S6',title:'Denton Corker Marshall — Melbourne Museum',url:'https://dentoncorkermarshall.com/projects/melbourne-museum/'},
 {id:'S7',title:'Museums Victoria — Accessibility',url:'https://museumsvictoria.com.au/melbournemuseum/plan-your-visit/accessibility/'},
 {id:'S8',title:'Three.js — GLTFLoader',url:'https://threejs.org/docs/pages/GLTFLoader.html'},
];
export const EXHIBITS = [
 // An envelope is [width X, height Y, depth Z]. These are design allowances, never zoological measurements.
 {id:'D01',room:'dinosaurs',title:'The long-necked giant',subject:'Mamenchisaurus',kind:'split',position:[-24,.3,-16],envelope:[7,8.5,28],view:[-17.5,0,-16],source:'S3',brief:'A long, largely horizontal sauropod mount. Two separated support islands leave a 7 m cross-passage through the reserved bay. Keep the passage clear above 2.8 m; validate the final neck, tail and supports before installation.'},
 {id:'D02',room:'dinosaurs',title:'Predator in motion',subject:'Tarbosaurus',kind:'plinth',position:[-11,.3,-16],envelope:[5,5.8,11],view:[-7.5,0,-16],source:'S3',brief:'A tall theropod mount, read from the connecting walk and the north overlook. Orient the long axis along Z. Reserve the full tail sweep inside the envelope.'},
 {id:'D03',room:'dinosaurs',title:'Built for defence',subject:'Armoured dinosaur',kind:'plinth',position:[-12,.3,-30],envelope:[5.6,3.5,5],view:[-8,0,-30],source:'S3',brief:'Armour, tail mechanics and defensive body plans. No moving parts are supplied; use a separate animation clip later.'},
 {id:'D04',room:'dinosaurs',title:'Small dinosaur, big story',subject:'Protoceratops',kind:'plinth',position:[-28,.3,4],envelope:[3.2,2.5,3.2],view:[-24,0,4],source:'S3',brief:'A family-scale mount with a lower reading rail. Its envelope intentionally leaves the dinosaur entrance unobstructed.'},
 {id:'D05',room:'dinosaurs',title:'Footprints as evidence',subject:'Trackway casting',kind:'table',position:[-8,.88,4],envelope:[3,0.3,2],view:[-8,0,7],source:'S2',brief:'A shallow, accessible examination surface for a trackway cast. The display table is already built; add only the geological exhibit.'},
 {id:'D06',room:'dinosaurs',title:'Teeth tell a story',subject:'Comparative teeth',kind:'wall',position:[-37.08,1.4,-12],envelope:[.45,1.1,2.6],view:[-35.4,1,-12],source:'S2',brief:'A side-facing cabinet above the ramp. Compare feeding adaptations using original tooth models. Keep all geometry inside the shallow case.'},
 {id:'D07',room:'dinosaurs',title:'After the dinosaurs',subject:'Australian megafauna',kind:'plinth',position:[-28,.3,-32.5],envelope:[4,3.6,4],view:[-23.7,0,-32.5],source:'S2',brief:'Reserve for a Diprotodon or another Australian megafaunal subject. Label its different time period explicitly; do not call every prehistoric animal a dinosaur.'},
 {id:'D08',room:'dinosaurs',title:'A different kind of flight',subject:'Pterosaur',kind:'suspended',position:[-18,7,-5],envelope:[7,2.8,4],view:[-14,0,-5],source:'S3',brief:'Suspended pterosaur allowance. It is not a dinosaur. Model rigging separately, check supports against roof ribs, and keep the entire envelope above visitor head height.'},
 {id:'D09',room:'dinosaurs',title:'Reading deep time',subject:'Fossil comparison',kind:'table',position:[-16,3.28,-39.5],envelope:[4,.45,1.25],view:[-16,2.4,-37.6],source:'S2',brief:'An overlook-level comparison table. The shell includes the table and guardrails; add fossil specimens only.'},
 {id:'B01',room:'diversity',title:'A wall of wings',subject:'Butterfly diversity',kind:'wall',position:[6.2,1.25,8.35],envelope:[3,1.8,.38],view:[6.2,0,5.6],source:'S1',brief:'Pinned-specimen composition in a shallow wall cabinet. Use separate small models, or an original baked specimen atlas for distant views. No specimen artwork is supplied.'},
 {id:'B02',room:'diversity',title:'The beetle collection',subject:'Beetle diversity',kind:'wall',position:[17,1.25,8.35],envelope:[5.4,1.8,.38],view:[17,0,5.6],source:'S1',brief:'A second framed collection wall with warm conservation-style presentation. Design allowances are not real conservation specifications.'},
 {id:'B03',room:'diversity',title:'Record breakers',subject:'Insect Hall of Fame theme',kind:'case',position:[12.5,.88,-.5],envelope:[3,1.65,2],view:[12.5,0,2.8],source:'S1',brief:'An island vitrine for insect superlatives. Confirm any eventual largest/heaviest/longest claim with a species-specific source before adding final labels.'},
 {id:'B04',room:'diversity',title:'Six legs, many lives',subject:'Insect classification',kind:'table',position:[7.1,.88,-4.6],envelope:[3,.4,1.25],view:[7.1,0,-2.8],source:'S1',brief:'Low comparison table for body plan models. Deliberately separate insect classification from the eight-legged gallery next door.'},
 {id:'B05',room:'habitats',title:'A city in the leaves',subject:'Green tree ant colony',kind:'habitat',position:[28.5,.65,-.5],envelope:[3.5,2.4,3],view:[25,0,-.5],source:'S1',brief:'Empty habitat enclosure. You will supply nest, branches, substrate, ant meshes and animation. This is not a live-animal husbandry design.'},
 {id:'B06',room:'habitats',title:'The patient hunter',subject:'Mantid habitat',kind:'habitat',position:[36.6,.7,3.5],envelope:[1.35,1.8,2.6],view:[33.8,0,3.5],source:'S1',brief:'Wall-side enclosure reserved for mantid, branches and foliage. No placeholder insects or greenery are included.'},
 {id:'B07',room:'habitats',title:'Life below the surface',subject:'Aquatic invertebrates',kind:'habitat',position:[36.6,.7,-3.5],envelope:[1.35,1.8,2.6],view:[33.8,0,-3.5],source:'S1',brief:'An aquarium-format shell with a dry, empty interior. Add water and invertebrates later; avoid nested transmissive surfaces in the final GLB.'},
 {id:'B08',room:'habitats',title:'Nature’s recyclers',subject:'Decomposer habitat',kind:'habitat',position:[24.5,.7,7.5],envelope:[3,1.8,1.25],view:[24.5,0,5],source:'S1',brief:'An empty ecological exhibit for leaf litter and decomposer invertebrates. Habitat dressing remains part of your Blender stage.'},
 {id:'B09',room:'anatomy',title:'Anatomy, enlarged',subject:'Insect body systems',kind:'plinth',position:[12.6,.3,-16],envelope:[4,2.9,4],view:[8.7,0,-16],source:'S1',brief:'A deliberately enlarged anatomical model. Display its scale multiplier on the future label so visitors do not confuse model size with animal size.'},
 {id:'B10',room:'anatomy',title:'Tools for feeding',subject:'Insect mouthparts',kind:'case',position:[18.5,.88,-19.3],envelope:[2.8,1.1,1.6],view:[18.5,0,-16.7],source:'S1',brief:'Enlarged comparative mouthparts inside an island vitrine. Include chewing, piercing or other forms only after choosing referenced species.'},
 {id:'B11',room:'anatomy',title:'A life transformed',subject:'Life cycles',kind:'wall',position:[12.8,1.25,-22.4],envelope:[5.8,1.8,.38],view:[12.8,0,-19.6],source:'S1',brief:'A chronological specimen sequence. The cabinet and typography frame are present; model the lifecycle stages in Blender.'},
 {id:'B12',room:'anatomy',title:'Small but essential',subject:'Pollination',kind:'table',position:[7,.88,-19.5],envelope:[2.7,.7,1.5],view:[7,0,-16.8],source:'S1',brief:'A teaching-table allowance for insect–flower relationships. Flowers and insects are both intentionally omitted.'},
 {id:'B13',room:'arachnids',title:'Beyond six legs',subject:'Arachnid comparison',kind:'case',position:[28.8,.88,-15.3],envelope:[3,1.35,2],view:[25.5,0,-15.3],source:'S1',brief:'A comparison vitrine introducing arachnids. Use accurate leg counts and label specimens independently from insects.'},
 {id:'B14',room:'arachnids',title:'Behind the glass',subject:'Tarantula enclosure',kind:'habitat',position:[36.6,.7,-19],envelope:[1.35,1.8,2.6],view:[33.8,0,-19],source:'S1',brief:'An empty quarantine-themed enclosure. No fictional biosecurity system is presented as a working or legally compliant facility.'},
 {id:'B15',room:'arachnids',title:'Our backyard neighbours',subject:'Local spider enclosure',kind:'habitat',position:[36.6,.7,-11.5],envelope:[1.35,1.8,2.6],view:[33.8,0,-11.5],source:'S1',brief:'An enclosure for a chosen locally occurring spider. Final species, location and safety interpretation must be researched before publication.'},
 {id:'B16',room:'arachnids',title:'Architecture of silk',subject:'Web structures',kind:'wall',position:[28.5,1.25,-22.4],envelope:[4.6,1.8,.38],view:[28.5,0,-19.8],source:'S1',brief:'A backlit web-study cabinet. Supply the silk geometry or baked transparent texture; keep the future exhibit readable without bloom.'},
 {id:'F01',room:'feature',title:'The last giants',subject:'Triceratops',kind:'plinth',position:[13,.3,-34.4],envelope:[6.5,5,11],view:[7.3,0,-34.4],source:'S4',brief:'The feature-gallery mount with a full walk-around route. Inspired by the idea of Melbourne’s Triceratops gallery; this is not a model or reproduction of Horridus.'},
 {id:'F02',room:'feature',title:'Evidence in the rock',subject:'Fossil preparation',kind:'wall',position:[12.5,1.25,-42.4],envelope:[5,1.8,.38],view:[12.5,0,-40.8],source:'S4',brief:'A wall-case allowance for preparation tools, rock matrix and fossil evidence. All these assets are left for Blender.'},
 {id:'L01',room:'learning',title:'The discovery bench',subject:'Handling collection',kind:'table',position:[28,.88,21],envelope:[4,.55,2],view:[28,0,18.3],source:'S7',brief:'A school-group table for tactile or digital models. The runtime interaction is a readable design card, not a finished scientific activity.'},
 {id:'L02',room:'learning',title:'Make an observation',subject:'Microscope station',kind:'table',position:[35,.88,25.5],envelope:[2,.8,1.3],view:[32.5,0,25.5],source:'S1',brief:'Reserve for microscope and specimen-tray assets. Do not export room furniture with the specimen GLB.'},
 {id:'C01',room:'court',title:'A future living centre',subject:'Botanical installation',kind:'planter',position:[0,.55,-12],envelope:[2.2,6,12],view:[2.6,0,-12],source:'S6',brief:'An empty central planting bed. Trees, ferns, ground cover and fauna are excluded from this delivery. This is a quiet light-court interpretation, not the real Forest Gallery.'}
].map(e=>({...e,url:null,rotation:[0,0,0],scale:1,offset:[0,0,0]}));
export function getRoom(x,z,y=0){
 if(y>1.9 && x<-4 && z<-35) return {id:'overlook',name:'Deep Time Overlook',tag:'LEVEL 01',color:'#d7a86c'};
 return ROOMS.find(r=> x>=r.bounds[0] && x<=r.bounds[1] && z>=r.bounds[2] && z<=r.bounds[3]) || {id:'concourse',name:z>29?'Museum forecourt':'Gallery street',tag:'THREE MUSEUM',color:'#bd9c68'};
}
/** Optional ground-level interpretation loop. It is a drawn suggestion, not an autoplay tour. */
export const VISITOR_ROUTE=[[0,38],[0,11],[-17,11],[-17,-26.6],[-2.6,-26.6],[-2.6,-29],[8,-29],[8,-27],[25,-27],[25,-11],[8,-11],[8,-5.9],[10.2,-5.9],[10.2,3],[0,3],[0,11]];
