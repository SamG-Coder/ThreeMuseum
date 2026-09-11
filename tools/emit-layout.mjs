import {mkdir,writeFile,access} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {buildArchitecture} from '../src/world/architecture.js';
import {SOURCES} from '../src/world/layout.js';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'),dir=path.join(root,'public'),data=buildArchitecture();
await mkdir(dir,{recursive:true});await writeFile(path.join(dir,'architecture.json'),JSON.stringify({...data,sources:SOURCES},null,2)+'\n');
const target=path.join(dir,'exhibits.json');let exists=true;try{await access(target);}catch{exists=false;}
if(!exists||process.argv.includes('--reset'))await writeFile(target,JSON.stringify({version:1,units:'metres',note:'Paths are relative to public/. Models are intentionally absent.',exhibits:data.exhibits.map(e=>({id:e.id,title:e.title,url:e.url,position:e.position,envelope:e.envelope,offset:e.offset,rotation:e.rotation,scale:e.scale}))},null,2)+'\n');
console.log(`Architecture compiled: ${data.pieces.length} pieces, ${data.colliders.length} solids, ${data.exhibits.length} exhibit anchors.`);
