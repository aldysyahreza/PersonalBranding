// Unduh PNG tiap slide lewat tombol #dl-one dan bandingkan dengan pratinjau (#frame) di resolusi 1080.
// MODE=offline : semua akses internet diputus (kecuali VENDOR=1 -> CDN pustaka dilayani dari folder vendor/).
// Hasil: tests/out_match/sNN_prev.png, sNN_exp.png, dan skor beda per slide (0 = identik).
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');const {execFileSync}=require('child_process');
const ROOT=path.join(__dirname,'..');const OUT=path.join(__dirname,process.env.OUT||'out_match');fs.mkdirSync(OUT,{recursive:true});
const FILE=process.env.FILE||'content-studio.html';
(async()=>{const b=await chromium.launch();
  const pg=await b.newPage({viewport:{width:1280,height:900},deviceScaleFactor:1080/440,acceptDownloads:true});
  const errs=[];pg.on('pageerror',x=>errs.push(x.message));pg.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
  await pg.route(/^https?:/,r=>{const u=r.request().url();
    if(process.env.VENDOR&&/html-to-image/.test(u))return r.fulfill({contentType:'text/javascript',body:fs.readFileSync(path.join(ROOT,'vendor/html-to-image.js'))});
    if(process.env.VENDOR&&/jszip/.test(u))return r.fulfill({contentType:'text/javascript',body:fs.readFileSync(path.join(ROOT,'vendor/jszip.min.js'))});
    if(process.env.MODE==='offline')return r.abort();return r.continue()});
  await pg.goto('file://'+path.join(ROOT,FILE));await pg.addStyleTag({content:'#toast{display:none!important}'});await pg.click('[data-tab=studio]');await pg.waitForTimeout(600);
  const fr=await pg.$('#frame');const n=await pg.$$eval('[data-slide]',e=>e.length);const res=[];
  for(let i=0;i<n;i++){await pg.click('[data-slide="'+i+'"]');await pg.waitForTimeout(250);
    const pp=path.join(OUT,'s'+String(i+1).padStart(2,'0')+'_prev.png'),ep=pp.replace('_prev','_exp');
    await fr.screenshot({path:pp});
    try{const [dw]=await Promise.all([pg.waitForEvent('download',{timeout:20000}),pg.click('#dl-one')]);await dw.saveAs(ep);
      res.push(execFileSync('python3',['-I',path.join(__dirname,'imgdiff.py'),pp,ep]).toString().trim());
    }catch(e){res.push('GAGAL UNDUH: '+String(e.message).split('\n')[0])}
    await pg.waitForTimeout(300)}
  res.forEach((r,i)=>console.log('slide',i+1,r));console.log('error konsol:',errs.length?errs:'tidak ada');await b.close()})();
