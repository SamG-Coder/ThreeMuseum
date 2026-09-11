#!/usr/bin/env node
import http from 'node:http';
import {createReadStream} from 'node:fs';
import {stat,realpath} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const project=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const root=await realpath(process.argv.includes('--dist')?path.join(project,'dist'):project);
const port=Number(process.env.PORT||4173),host=process.env.HOST||'127.0.0.1';
if(!Number.isInteger(port)||port<1||port>65535)throw new Error('PORT must be a valid TCP port.');
const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.mjs':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp','.glb':'model/gltf-binary','.gltf':'model/gltf+json','.bin':'application/octet-stream','.pdf':'application/pdf','.md':'text/plain; charset=utf-8','.csv':'text/csv; charset=utf-8'};
const server=http.createServer(async(req,res)=>{
 const fail=(code,text)=>{res.writeHead(code,{'Content-Type':'text/plain; charset=utf-8'});res.end(text);};
 try{
  if(req.method!=='GET'&&req.method!=='HEAD')return fail(405,'Read-only static server.');
  const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
  if(pathname.includes('\0')||pathname.includes('\\'))return fail(400,'Invalid path.');
  let candidate=path.resolve(root,'.'+pathname);
  if(candidate!==root&&!candidate.startsWith(root+path.sep))return fail(403,'Outside project root.');
  if(pathname.split('/').some(part=>part.startsWith('.')&&part!==''))return fail(403,'Hidden files are not served.');
  let info=await stat(candidate);if(info.isDirectory()){candidate=path.join(candidate,'index.html');info=await stat(candidate);}
  const actual=await realpath(candidate);if(actual!==root&&!actual.startsWith(root+path.sep))return fail(403,'Outside project root.');
  if(!info.isFile())return fail(404,'Not found.');
  res.writeHead(200,{'Content-Type':mime[path.extname(actual).toLowerCase()]||'application/octet-stream','Content-Length':info.size,'Cache-Control':'no-cache','X-Content-Type-Options':'nosniff'});
  if(req.method==='HEAD')return res.end();
  const stream=createReadStream(actual);stream.on('error',()=>res.destroy());stream.pipe(res);
 }catch(e){fail(e.code==='ENOENT'||e.code==='ENOTDIR'?404:400,e.code==='ENOENT'?'Not found.':'Request could not be served.');}
});
server.on('error',err=>{console.error(err.code==='EADDRINUSE'?`Port ${port} is busy. Set PORT to another number.`:err.message);process.exitCode=1;});
server.listen(port,host,()=>console.log(`ThreeMuseum\n  http://${host}:${port}\n  ${root}\nPress Ctrl+C to stop. No files are uploaded or changed by this server.`));
