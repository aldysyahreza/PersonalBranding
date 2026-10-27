// Unggah foto contoh ke setiap slide, foto panel editor + pratinjau per slide.
const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1400,height:1500}});const errs=[];pg.on('pageerror',x=>errs.push(x.message));
await pg.goto('file://'+path.join(__dirname,'..',process.env.FILE||'content-studio.html'));await pg.click('[data-tab=studio]');await pg.waitForTimeout(400);
for(let i=0;i<8;i++){await pg.click('[data-slide="'+i+'"]');await pg.waitForTimeout(200);
  const has=await pg.$('#ph-file');if(has){await pg.setInputFiles('#ph-file',path.join(__dirname,process.env.PHOTO||'test_busy.jpg'));await pg.waitForTimeout(900)}
  const desk=await pg.$('.desk');await desk.screenshot({path:path.join(__dirname,'out_ph','d'+(i+1)+'.png')});console.log('slide',i+1,has?'ADA kontrol foto':'tanpa kontrol foto')}
console.log('errors',errs);await b.close()})();
