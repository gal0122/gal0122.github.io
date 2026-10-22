// Render each SVG in a folder to PNG, cropped to the drawn content (keeps 1200 width).
const { chromium } = require('playwright'); const fs=require('fs'); const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(async()=>await chromium.launch());
const dir=process.argv[2], out=process.argv[3], font=process.argv[4];
const p=await b.newPage({viewport:{width:1200,height:720},deviceScaleFactor:1});
for (const f of fs.readdirSync(dir).filter(f=>f.endsWith('.svg'))){
 const svg=fs.readFileSync(path.join(dir,f),'utf8');
 await p.setContent(`<html><head><style>@font-face{font-family:Pretendard;src:url(data:font/ttf;base64,${fs.readFileSync(font).toString('base64')})}body{margin:0}</style></head><body>${svg}</body></html>`);
 await p.waitForTimeout(300);
 const h=await p.evaluate(()=>{const s=document.querySelector('svg');let m=0;[...s.children].slice(1).forEach(c=>{if(c.tagName==='defs')return;const r=c.getBBox();m=Math.max(m,r.y+r.height);});return Math.min(720,Math.ceil(m+48));});
 await p.screenshot({path:path.join(out,f.replace('.svg','.png')),clip:{x:0,y:0,width:1200,height:h}});}
await b.close();})();
