const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1280,height:900}});const e=[];pg.on('pageerror',x=>e.push(x.message));
await pg.route('**/html-to-image*',r=>r.fulfill({contentType:'text/javascript',body:fs.readFileSync('../nm/node_modules/html-to-image/dist/html-to-image.js')}));
await pg.goto('file://'+process.cwd()+'/content-studio.html');await pg.click('[data-tab=studio]');await pg.waitForTimeout(400);
await pg.click('[data-slide="1"]');await pg.setInputFiles('#ph-file','cream_etch.png');await pg.waitForTimeout(1500);
await (await pg.$('#frame')).screenshot({path:'p_prev.png'});
const [dw]=await Promise.all([pg.waitForEvent('download',{timeout:20000}),pg.click('#dl-one')]);await dw.saveAs('p_exp.png');console.log(e);await b.close()})();
