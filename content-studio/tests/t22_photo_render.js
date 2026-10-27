// Unggah foto ke slide 1,2,6,8 lalu foto pratinjau 1080px tiap slide + slide 2 per mode gambar.
const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1280,height:900},deviceScaleFactor:1080/440});const errs=[];pg.on('pageerror',x=>errs.push(x.message));
await pg.goto('file://'+path.join(__dirname,'..',process.env.FILE||'content-studio.html'));await pg.click('[data-tab=studio]');await pg.waitForTimeout(400);
const fr=await pg.$('#frame');const O=n=>path.join(__dirname,'out_ph',n);
for(const i of [0,1,5,7]){await pg.click('[data-slide="'+i+'"]');await pg.waitForTimeout(200);await fr.screenshot({path:O('before_s'+(i+1)+'.png')});
  await pg.setInputFiles('#ph-file',path.join(__dirname,process.env.PHOTO||'test_busy.jpg'));await pg.waitForTimeout(900);
  if(i===1){for(const m of ['etching','foto','kartu']){await pg.selectOption('#sf-imgmode',m);await pg.waitForTimeout(500);await fr.screenshot({path:O('s2_'+m+'.png')})}}
  else await fr.screenshot({path:O('s'+(i+1)+'.png')})}
console.log('errors',errs);await b.close()})();
