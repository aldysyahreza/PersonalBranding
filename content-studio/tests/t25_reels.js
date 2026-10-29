// Reels Studio (HRIRC): impor contoh, 5 babak + cover, hook 2 lapis, Temuan kolom wajib, aturan CTA,
// checklist bertahan, unduh cover = render skrip, dan migrasi otomatis data 7 langkah lama.
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');const {execFileSync}=require('child_process');
const T=__dirname,O=n=>path.join(T,'out_reels',n);fs.mkdirSync(O(''),{recursive:true});
const checks=pg=>pg.$$eval('#checks .ck',e=>e.map(x=>x.className.split(' ')[1]+':'+x.textContent));
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:1280,height:1000},acceptDownloads:true});const pg=await ctx.newPage();
const errs=[];pg.on('pageerror',x=>errs.push(x.message));await pg.route(/^https?:/,r=>r.abort());
await pg.goto('file://'+path.join(T,'..','content-studio.html'));await pg.addStyleTag({content:'#toast{display:none!important}'});
await pg.click('[data-tab=pipeline]');await pg.waitForTimeout(300);
const [fc]=await Promise.all([pg.waitForEvent('filechooser'),pg.click('#im-json-btn')]);await fc.setFiles(path.join(T,'..','posts','reels-harga-ditawar.json'));await pg.waitForTimeout(800);
const tabs=await pg.$$eval('[data-beat]',e=>e.map(x=>x.querySelector('b').textContent+'/'+x.querySelector('span').textContent));console.log('tab:',tabs.join(' '));
const fr=await pg.$('#frame');await pg.screenshot({path:O('studio.png'),fullPage:true});
for(const k of [0,1,2,3,4,5]){await pg.click('[data-beat="'+k+'"]');await pg.waitForTimeout(250);await fr.screenshot({path:O('beat'+k+'.png')});
  console.log('babak',k,'|',(await checks(pg)).filter(x=>!/Checklist|Total|caption/.test(x)).join(' / '))}
// hook 2 lapis: ganti pilihan, petunjuk ikut berubah
await pg.click('[data-beat="1"]');await pg.selectOption('#rh-angle','tes');await pg.waitForTimeout(200);
console.log('hook: petunjuk angle ->',(await pg.$eval('#rh-angle',e=>e.parentNode.querySelector('.hint').textContent)).slice(0,60));
// kolom wajib Insight diisi -> Temuan hilang
await pg.click('[data-beat="3"]');await pg.fill('#rb-solusi','Tulis satu kalimat alasan dipilih, pakai di bio dan balasan pertama CS.');await pg.dispatchEvent('#rb-solusi','input');await pg.waitForTimeout(200);
console.log('insight setelah diisi:',(await checks(pg)).filter(x=>/solusi/i.test(x)).join(' / '));
// pelanggaran CTA
await pg.click('[data-beat="5"]');await pg.fill('#rb-say','Ketik HARGA di komentar, saya kirim panduannya.');await pg.dispatchEvent('#rb-say','input');await pg.waitForTimeout(200);
console.log('CTA kata kunci ->',(await pg.$$eval('#checks .ck.bad',e=>e.map(x=>x.textContent))).join(' / '));
await pg.fill('#rb-say','Kirim video ini ke satu owner yang masih sering ditawar, supaya dia tahu masalahnya bukan harga.');await pg.dispatchEvent('#rb-say','input');
await pg.fill('#rb-txt','Kirim ke *satu owner*');await pg.dispatchEvent('#rb-txt','input');await pg.waitForTimeout(200);
console.log('CTA satu ajakan ->',(await checks(pg)).filter(x=>/^(ok|warn|bad):CTA[ :]/.test(x)).join(' / '));
await pg.selectOption('#rb-shot','card');await pg.waitForTimeout(200);console.log('shot baris 5 di tabel:',await pg.$eval('#rshots tbody tr:nth-child(5) td:nth-child(4)',e=>e.textContent));
await pg.selectOption('#rb-shot','med');
await pg.check('[data-rp="p1"]');await pg.check('[data-rp="r1"]');await pg.waitForTimeout(200);
// unduh cover
await pg.click('[data-beat="0"]');await pg.waitForTimeout(200);
const [d]=await Promise.all([pg.waitForEvent('download'),pg.click('#dl-reel')]);await d.saveAs(O('studio_cover.png'));console.log('unduhan:',d.suggestedFilename());
execFileSync('node',[path.join(T,'..','render','render.js'),path.join(T,'..','posts','reels-harga-ditawar.json'),'--out',O('render')]);
const rd=fs.readdirSync(O('render'))[0];
console.log('cover studio vs skrip:',execFileSync('python3',['-I',path.join(T,'imgdiff.py'),O('studio_cover.png'),O('render/'+rd+'/reel-cover.png')]).toString().trim());
await pg.reload();await pg.waitForTimeout(700);
console.log('setelah reload: checklist p1,r1 =',await pg.$eval('[data-rp="p1"]',e=>e.checked),await pg.$eval('[data-rp="r1"]',e=>e.checked),'| hook tetap "tes":',await pg.evaluate(()=>{document.querySelector('[data-beat="1"]').click();return document.querySelector('#rh-angle').value==='tes'}));
// migrasi: data 7 langkah lama (legacy7 di file contoh) -> 5 babak HRIRC
const post=JSON.parse(fs.readFileSync(path.join(T,'..','posts','reels-harga-ditawar.json'),'utf8'));
const old={id:'old7',title:'Reels 7 langkah lama',format:'reels',reel:{beats:post.reel.legacy7}};fs.writeFileSync(O('old7.json'),JSON.stringify(old));
await pg.click('[data-tab=pipeline]');const [fc2]=await Promise.all([pg.waitForEvent('filechooser'),pg.click('#im-json-btn')]);await fc2.setFiles(O('old7.json'));await pg.waitForTimeout(800);
await pg.click('[data-beat="2"]');await pg.waitForTimeout(150);const relate=await pg.$eval('#rb-say',e=>e.value);
await pg.click('[data-beat="4"]');await pg.waitForTimeout(150);const reframe=await pg.$eval('#rb-say',e=>e.value);
console.log('migrasi: tab',await pg.$$eval('[data-beat]',e=>e.length),'| Relate gabung Situasi+Ketegangan:',relate.startsWith('Chat masuk')&&relate.includes('Besoknya'),'| Reframe gabung Reframe+Pertanyaan:',reframe.startsWith('Harga yang')&&reframe.includes('Coba jawab'));
console.log('error halaman:',errs.length?errs:'tidak ada');await b.close()})();
