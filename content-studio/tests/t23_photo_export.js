// Slide berfoto (1, 2 foto penuh, 6, 8): unduh PNG offline dan bandingkan dengan pratinjau.
const {chromium}=require('playwright');const path=require('path');const {execFileSync}=require('child_process');
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1280,height:900},deviceScaleFactor:1080/440,acceptDownloads:true});
const errs=[];pg.on('pageerror',x=>errs.push(x.message));pg.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await pg.route(/^https?:/,r=>r.abort());
await pg.goto('file://'+path.join(__dirname,'..','content-studio.html'));await pg.addStyleTag({content:'#toast{display:none!important}'});
await pg.click('[data-tab=studio]');await pg.waitForTimeout(400);const fr=await pg.$('#frame');const O=n=>path.join(__dirname,'out_ph',n);
for(const i of [0,1,5,7]){await pg.click('[data-slide="'+i+'"]');await pg.waitForTimeout(200);
  await pg.setInputFiles('#ph-file',path.join(__dirname,'test_busy.jpg'));await pg.waitForTimeout(900);
  if(i===1){await pg.selectOption('#sf-imgmode','foto');await pg.waitForTimeout(400)}
  await fr.screenshot({path:O('x'+(i+1)+'_prev.png')});
  const [dw]=await Promise.all([pg.waitForEvent('download',{timeout:20000}),pg.click('#dl-one')]);await dw.saveAs(O('x'+(i+1)+'_exp.png'));
  console.log('slide',i+1,execFileSync('python3',['-I',path.join(__dirname,'imgdiff.py'),O('x'+(i+1)+'_prev.png'),O('x'+(i+1)+'_exp.png')]).toString().trim());await pg.waitForTimeout(300)}
console.log('error konsol:',errs.length?errs:'tidak ada');await b.close()})();
