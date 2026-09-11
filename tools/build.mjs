import {cp,mkdir,rm,access} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {vendor} from './vendor.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'),out=path.join(root,'dist');
try{await access(path.join(root,'node_modules/three/package.json'));await vendor();}catch{console.warn('No npm-installed Three.js found. Existing public/vendor files, or the CDN fallback, will be used.');}
await import('./emit-layout.mjs');await rm(out,{recursive:true,force:true});await mkdir(out,{recursive:true});
for(const item of['index.html','style.css','src','public'])await cp(path.join(root,item),path.join(out,item),{recursive:true});
console.log('Built dist/. All asset paths are relative, including GitHub Pages project paths.');
