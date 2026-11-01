// Variasi tata letak (v27): impor carousel dengan s.lay, bandingkan unduhan PNG dengan pratinjau untuk slide bergaya b/c, dan cek pilihan "Gaya tampilan".
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');const {execFileSync}=require('child_process');
const ROOT=path.join(__dirname,'..');const OUT=path.join(__dirname,'out_layouts');fs.mkdirSync(OUT,{recursive:true});
(async()=>{const b=await chromium.launch();
  const pg=await b.newPage({viewport:{width:1280,height:900},deviceScaleFactor:1080/440,acceptDownloads:true});
  const errs=[];pg.on('pageerror',x=>errs.push(x.message));await pg.route(/^https?:/,r=>r.abort());
  await pg.goto('file://'+path.join(ROOT,'content-studio.html'));await pg.addStyleTag({content:'#toast{display:none!important}'});
  await pg.click('[data-tab=pipeline]');await pg.waitForTimeout(300);
  const [fc]=await Promise.all([pg.waitForEvent('filechooser'),pg.click('#im-json-btn')]);await fc.setFiles(path.join(ROOT,'posts','carousel-owner-penghambat.json'));await pg.waitForTimeout(800);
  await pg.click('[data-tab=studio]');await pg.waitForTimeout(500);const fr=await pg.$('#frame');
  for(const i of [2,4,6]){await pg.click('[data-slide="'+i+'"]');await pg.waitForTimeout(300);
    const lay=await pg.$eval('#sf-lay',e=>e.value+'/'+e.options.length+' pilihan');
    const pp=path.join(OUT,'s'+(i+1)+'_prev.png'),ep=pp.replace('_prev','_exp');await fr.screenshot({path:pp});
    const [dw]=await Promise.all([pg.waitForEvent('download',{timeout:20000}),pg.click('#dl-one')]);await dw.saveAs(ep);
    console.log('slide',i+1,'gaya',lay,'| beda pratinjau vs unduhan:',execFileSync('python3',['-I',path.join(__dirname,'imgdiff.py'),pp,ep]).toString().trim())}
  // ganti gaya lewat pilihan: slide 3 -> b, pratinjau berubah
  await pg.click('[data-slide="2"]');await pg.selectOption('#sf-lay','b');await pg.waitForTimeout(300);
  const p2=path.join(OUT,'s3_b.png');await fr.screenshot({path:p2});console.log('ganti gaya slide 3 ke b: pratinjau beda dari c =',execFileSync('python3',['-I',path.join(__dirname,'imgdiff.py'),path.join(OUT,'s3_prev.png'),p2]).toString().trim());
  console.log('error halaman:',errs.length?errs:'tidak ada');await b.close()})();
