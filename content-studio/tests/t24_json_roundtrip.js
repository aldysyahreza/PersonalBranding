// Ekspor JSON dari Studio -> render skrip -> bandingkan; impor balik tanpa menimpa; file rusak ditolak; data bertahan setelah reload.
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');const {execFileSync}=require('child_process');
const T=__dirname,O=n=>path.join(T,'out_json',n);fs.mkdirSync(O(''),{recursive:true});
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:1280,height:900},deviceScaleFactor:1080/440,acceptDownloads:true});
const pg=await ctx.newPage();const errs=[];pg.on('pageerror',x=>errs.push(x.message));
await pg.route(/^https?:/,r=>r.abort());
await pg.goto('file://'+path.join(T,'..','content-studio.html'));await pg.addStyleTag({content:'#toast{display:none!important}'});
await pg.click('[data-tab=studio]');await pg.waitForTimeout(400);
for(const i of [0,1,5,7]){await pg.click('[data-slide="'+i+'"]');await pg.setInputFiles('#ph-file',path.join(T,'test_busy.jpg'));await pg.waitForTimeout(800);if(i===1){await pg.selectOption('#sf-imgmode','foto');await pg.waitForTimeout(300)}}
await pg.click('[data-slide="5"]');await pg.fill('#sf-phz','140');await pg.dispatchEvent('#sf-phz','input');await pg.waitForTimeout(300);
// referensi: unduhan Studio slide 6 (zoom 140) dan slide 2
const ref={};for(const i of [1,5]){await pg.click('[data-slide="'+i+'"]');await pg.waitForTimeout(200);const [d]=await Promise.all([pg.waitForEvent('download'),pg.click('#dl-one')]);ref[i]=O('studio_s'+(i+1)+'.png');await d.saveAs(ref[i]);await pg.waitForTimeout(300)}
const [dj]=await Promise.all([pg.waitForEvent('download'),pg.click('#ex-json')]);const jp=O('ekspor.json');await dj.saveAs(jp);
const j=JSON.parse(fs.readFileSync(jp,'utf8'));console.log('ekspor:',dj.suggestedFilename(),'slides',j.slides.length,'foto',Object.keys(j.photos).join(','),'phz slide6',j.slides[5].phz,'imgmode s2',j.slides[1].imgmode);
// render skrip dari file ekspor
console.log(execFileSync('node',[path.join(T,'..','render','render.js'),jp,'--out',O('render')]).toString().trim());
const rd=fs.readdirSync(O('render'))[0];
for(const i of [1,5])console.log('render vs studio slide',i+1,execFileSync('python3',['-I',path.join(T,'imgdiff.py'),ref[i],O('render/'+rd+'/slide-0'+(i+1)+'.png')]).toString().trim());
// impor: file ekspor (ID sama -> salinan), fixture berpath foto, file rusak
const n0=await pg.$$eval('#sel-post option',o=>o.length);const origTitle=await pg.$eval('#f-title',e=>e.value);
fs.writeFileSync(O('rusak.json'),'{"title":"x"}');
await pg.evaluate(()=>{const t=document.getElementById('toast');window.__toasts=[];new MutationObserver(()=>window.__toasts.push(t.textContent)).observe(t,{childList:true,characterData:true,subtree:true})});
const [fc]=await Promise.all([pg.waitForEvent('filechooser'),pg.click('#im-json-btn')]);await fc.setFiles([jp,path.join(T,'fixture_foto.json'),O('rusak.json')]);await pg.waitForTimeout(1200);
console.log('toast:',await pg.evaluate(()=>window.__toasts.slice(-1)[0]));
const opts=await pg.$$eval('#sel-post option',o=>o.map(x=>x.textContent));console.log('post sebelum',n0,'sesudah',opts.length,opts);
await pg.click('[data-slide="5"]');await pg.waitForTimeout(400);await (await pg.$('#frame')).screenshot({path:O('impor_s6_prev.png')});
console.log('post aktif:',await pg.$eval('#f-title',e=>e.value),'| ada foto di slide 6:',await pg.$$eval('#frame .ph.has',e=>e.length>0));
await pg.reload();await pg.waitForTimeout(800);
console.log('setelah reload jumlah post:',await pg.$$eval('#sel-post option',o=>o.length),'| judul asli masih ada:',(await pg.$$eval('#sel-post option',o=>o.map(x=>x.textContent))).includes(origTitle));
console.log('error halaman:',errs.length?errs:'tidak ada');await b.close()})();
