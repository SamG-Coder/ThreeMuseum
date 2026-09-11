// Run with Playwright installed in an external tools environment, or as a dev dependency.
import {createRequire} from 'node:module';
import {writeFile,mkdir} from 'node:fs/promises';
const require=createRequire(process.env.PLAYWRIGHT_PACKAGE||import.meta.url);
const {chromium}=require('playwright');
const browser=await chromium.launch({channel:'msedge',headless:true,args:['--autoplay-policy=no-user-gesture-required']});
const context=await browser.newContext({viewport:{width:1280,height:720},deviceScaleFactor:1,recordVideo:process.argv.includes('--record')?{dir:'media/raw',size:{width:1280,height:720}}:undefined});
const page=await context.newPage();
const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto('http://127.0.0.1:4173/?director');
await page.waitForFunction(()=>window.__DIRECTOR__?.ready,{},{timeout:180000});
const timeline=await page.evaluate(()=>({total:window.__DIRECTOR__.total,shots:window.__DIRECTOR__.shots}));
await writeFile('media/director-timeline.json',JSON.stringify(timeline,null,2));
if(process.argv.includes('--record')){
 const elapsed=await page.evaluate(()=>performance.now()/1000);
 await page.evaluate(()=>window.__DIRECTOR__.start());
 await page.waitForFunction(()=>window.__DIRECTOR__.done,{},{timeout:180000});
 const file=await page.video().path();
 await context.close();
 await writeFile('media/raw/recording.json',JSON.stringify({file,elapsed,total:timeline.total,errors},null,2));
 console.log(JSON.stringify({file,elapsed,total:timeline.total,errors}));
}else{
 await mkdir('media/frames',{recursive:true});let offset=0;
 for(let i=0;i<timeline.shots.length;i++){
  await page.evaluate(t=>window.__DIRECTOR__.seek(t),offset+timeline.shots[i].duration/2);
  await page.waitForTimeout(160);
  await page.screenshot({path:`media/frames/shot-${String(i).padStart(2,'0')}.jpg`});
  offset+=timeline.shots[i].duration;
 }
 console.log(JSON.stringify({shots:timeline.shots.length,total:timeline.total,errors}));
 await context.close();
}
await browser.close();
