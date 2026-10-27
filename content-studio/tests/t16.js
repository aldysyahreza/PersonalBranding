const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1280,height:900}});pg.on('pageerror',x=>console.log('ERR',x.message));
await pg.goto('file://'+process.cwd()+'/content-studio.html');await pg.click('[data-tab=studio]');await pg.waitForTimeout(400);
const fr=await pg.$('#frame');
for(const i of [3,7]){await pg.click('[data-slide="'+i+'"]');await pg.waitForTimeout(200);await fr.screenshot({path:'k'+i+'.png'})}
const el=await pg.$('#ptable');await el.scrollIntoViewIfNeeded();await el.screenshot({path:'tests/out_pt.png'});
console.log(await pg.evaluate(()=>document.querySelectorAll('[data-cp]').length));
await b.close()})();
