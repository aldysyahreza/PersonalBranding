const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1280,height:900}});pg.on('pageerror',x=>console.log('ERR',x.message));
await pg.goto('file://'+process.cwd()+'/content-studio.html');await pg.click('[data-tab=studio]');await pg.waitForTimeout(300);
await pg.click('[data-slide="1"]');await pg.setInputFiles('#ph-file','tests/cream_etch.png');await pg.waitForTimeout(1200);
const fr=await pg.$('#frame');await fr.screenshot({path:'tests/out_e0.png'});
console.log(await pg.evaluate(()=>!!document.querySelector('#sf-phz')&&!!document.querySelector('#sf-phx')&&!!document.querySelector('#sf-phy')));
await pg.fill('#sf-phz','160');await pg.dispatchEvent('#sf-phz','input');await pg.fill('#sf-phx','20');await pg.dispatchEvent('#sf-phx','input');await pg.waitForTimeout(300);await fr.screenshot({path:'tests/out_e1.png'});
await pg.selectOption('#sf-imgmode','foto');await pg.waitForTimeout(300);await fr.screenshot({path:'tests/out_e2.png'});
await b.close()})();
