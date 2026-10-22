const { chromium } = require('playwright'); const fs=require('fs'); const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(async()=>await chromium.launch());
const dir=process.argv[2], out=process.argv[3], font=process.argv[4];
const p=await b.newPage({viewport:{width:1200,height:720},deviceScaleFactor:1});
for (const f of fs.readdirSync(dir).filter(f=>f.endsWith('.svg'))){
 const svg=fs.readFileSync(path.join(dir,f),'utf8');
 await p.setContent(`<html><head><style>@font-face{font-family:Pretendard;src:url(data:font/ttf;base64,${fs.readFileSync(font).toString('base64')})}body{margin:0}</style></head><body>${svg}</body></html>`);
 await p.waitForTimeout(300);
 await p.screenshot({path:path.join(out,f.replace('.svg','.png')),clip:{x:0,y:0,width:1200,height:720}});}
await b.close();})();
