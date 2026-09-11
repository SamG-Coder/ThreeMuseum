import {cp,mkdir,access} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
export async function vendor(){
 const from=path.join(root,'node_modules/three'),to=path.join(root,'public/vendor/three');
 await access(path.join(from,'build/three.module.js'));await mkdir(to,{recursive:true});
 for(const item of['build','examples/jsm','LICENSE','package.json'])await cp(path.join(from,item),path.join(to,item),{recursive:true});
 console.log('Three.js copied to public/vendor/three. The museum can now run offline.');
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))await vendor();
