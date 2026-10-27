// Reels Studio: impor contoh, pratinjau tiap langkah, cek aturan, checklist bertahan, unduh cover = render skrip.
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');const {execFileSync}=require('child_process');
const T=__dirname,O=n=>path.join(T,'out_reels',n);fs.mkdirSync(O(''),{recursive:true});
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:1280,height:1000},acceptDownloads:true});const pg=await ctx.newPage();
const errs=[];pg.on('pageerror',x=>errs.push(x.message));await pg.route(/^https?:/,r=>r.abort());
await pg.goto('file://'+path.join(T,'..','content-studio.html'));await pg.addStyleTag({content:'#toast{display:none!important}'});
await pg.click('[data-tab=pipeline]');await pg.waitForTimeout(300);
const [fc]=await Promise.all([pg.waitForEvent('filechooser'),pg.click('#im-json-btn')]);await fc.setFiles(path.join(T,'..','posts','reels-harga-ditawar.json'));await pg.waitForTimeout(800);
const fr=await pg.$('#frame');const fw=await fr.evaluate(e=>e.clientWidth);console.log('lebar frame',fw);
await pg.screenshot({path:O('studio.png'),fullPage:true});
for(const k of [0,1,2,5,7]){await pg.click('[data-beat="'+k+'"]');await pg.waitForTimeout(250);await fr.screenshot({path:O('beat'+k+'.png')});
  console.log('langkah',k,'|',(await pg.$$eval('#checks .ck',e=>e.map(x=>x.className.split(' ')[1]+':'+x.textContent))).join(' / '))}
// pelanggaran CTA
await pg.fill('#rb-say','Ketik HARGA di komentar, saya kirim panduannya.');await pg.dispatchEvent('#rb-say','input');await pg.waitForTimeout(200);
console.log('CTA kata kunci ->',(await pg.$$eval('#checks .ck.bad',e=>e.map(x=>x.textContent))).join(' / '));
await pg.fill('#rb-say','Simpan video ini. Kirim ke satu teman yang masih sering ditawar.');await pg.dispatchEvent('#rb-say','input');
// ganti shot -> hint & tabel ikut
await pg.selectOption('#rb-shot','card');await pg.waitForTimeout(200);console.log('shot baris 7 di tabel:',await pg.$eval('#rshots tbody tr:nth-child(7) td:nth-child(4)',e=>e.textContent));
await pg.selectOption('#rb-shot','med');
await pg.check('[data-rp="p1"]');await pg.check('[data-rp="r1"]');await pg.waitForTimeout(200);
// unduh cover
await pg.click('[data-beat="0"]');await pg.waitForTimeout(200);
const [d]=await Promise.all([pg.waitForEvent('download'),pg.click('#dl-reel')]);await d.saveAs(O('studio_cover.png'));console.log('unduhan:',d.suggestedFilename());
console.log('cover studio vs skrip:',execFileSync('python3',['-I',path.join(T,'imgdiff.py'),O('studio_cover.png'),path.join(T,'..','out','reels-harga-ditawar-itu-gejala','reel-cover.png')]).toString().trim());
await pg.reload();await pg.waitForTimeout(700);
console.log('setelah reload: checklist p1,r1 =',await pg.$eval('[data-rp="p1"]',e=>e.checked),await pg.$eval('[data-rp="r1"]',e=>e.checked),'| ucapan langkah 7 kembali normal:',await pg.evaluate(()=>{document.querySelector('[data-beat="7"]').click();return document.querySelector('#rb-say').value.startsWith('Simpan')}));
console.log('error halaman:',errs.length?errs:'tidak ada');await b.close()})();
