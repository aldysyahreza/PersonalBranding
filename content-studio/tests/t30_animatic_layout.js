// Pemeriksa tata letak animatic: tiap 0,2 detik cek (1) teks bertabrakan dengan teks lain, (2) teks menimpa objek,
// (3) objek menimpa caption, (4) teks keluar zona aman (x 60-1020, y 220-1540). Jeda transisi dan pindai dilewati.
// Pakai: node tests/t30_animatic_layout.js [animatic-v3.html] [timing.json dari vo_prep.py]
const {chromium}=require('playwright');const path=require('path');
const FILE=process.argv[2]||'animatic-v3.html';
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1920}});
await pg.route(/^https?:/,r=>r.abort());
if(process.argv[3]){const fs=require('fs');const tl=JSON.parse(fs.readFileSync(process.argv[3],'utf8'));await pg.addInitScript(b=>{window.ANIMATIC_BEATS=b},tl.beats);
  const an=path.join(__dirname,'..','animatic',FILE.replace(/^animatic/,'anchors').replace(/\.html$/,'.json'));if(fs.existsSync(an))await pg.addInitScript(a=>{window.ANIMATIC_ANCHORS=a},JSON.parse(fs.readFileSync(an,'utf8')))}
await pg.goto('file://'+path.join(__dirname,'..','animatic',FILE));
await pg.addStyleTag({path:path.join(__dirname,'..','assets','fonts-embed.css')});
await pg.evaluate(()=>Promise.all(['800 40px Archivo','italic 400 40px Fraunces','600 40px Outfit','600 40px Caveat','500 40px "JetBrains Mono"'].map(f=>document.fonts.load(f))));
const res=await pg.evaluate(()=>{
  const dur=window.ANIMATIC_DURATION,issues={};
  const T0=[];let acc=0;(window.ANIMATIC_BEATS||null);document.querySelectorAll('section.sc').forEach(()=>{});
  // ambil awal tiap langkah dari teks bab yang berganti
  function hidden(el){for(let e=el;e&&e.id!=='stage';e=e.parentElement){const cs=getComputedStyle(e);if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity<.5)return true;const cp=e.style.clipPath||'';if(/inset\(100%|inset\(0px 0px 100%|inset\(0 0 100%/.test(cp))return true}return false}
  function eff(el){let o=1;for(let e=el;e&&e.id!=='stage';e=e.parentElement)o*=+getComputedStyle(e).opacity;return o}
  function block(n){let e=n.parentElement;while(e&&getComputedStyle(e).display.startsWith('inline'))e=e.parentElement;return e}
  function name(e){return (e.id?'#'+e.id:'')||(e.className&&e.className.baseVal===undefined?'.'+String(e.className).split(' ')[0]:e.tagName.toLowerCase())}
  function label(e){let s=[],x=e;for(let k=0;k<3&&x&&x.id!=='stage';k++,x=x.parentElement)s.unshift(name(x));return s.join('>')}
  function inter(a,b){const w=Math.min(a.right,b.right)-Math.max(a.left,b.left),h=Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top);return w>6&&h>Math.max(10,.18*Math.min(a.bottom-a.top,b.bottom-b.top))}
  function inside(a,b){return a.left>=b.left-2&&a.right<=b.right+2&&a.top>=b.top-2&&a.bottom<=b.bottom+2}
  function clipRect(el,rc){let r={left:rc.left,right:rc.right,top:rc.top,bottom:rc.bottom};for(let e=el;e&&e.id!=='stage';e=e.parentElement){const cs=getComputedStyle(e);if(cs.overflow!=='visible'||cs.overflowY==='hidden'){const b=e.getBoundingClientRect();r.left=Math.max(r.left,b.left);r.right=Math.min(r.right,b.right);r.top=Math.max(r.top,b.top);r.bottom=Math.min(r.bottom,b.bottom)}}return (r.right-r.left>2&&r.bottom-r.top>2)?r:null}
  // jeda transisi tiap adegan + jendela pindai (adegan 4, detik rancangan 2,2-3,8) dibaca langsung dari animasi
  const starts=window.ANIMATIC_T0||[];
  const sc=window.ANIMATIC_SCAN||{i:3,a:2.2,b:3.8};const skip=t=>starts.some(s=>t>=s-.05&&t<s+.6)||(starts.length>sc.i&&t>=starts[sc.i]&&t<(starts[sc.i+1]||dur)&&(l=>l>=sc.a&&l<sc.b)(window.ANIMATIC_LOCAL(sc.i,t-starts[sc.i])));
  for(let t=0.1;t<dur;t+=0.2){if(skip(t))continue;window.seek(t);
    const texts=[];const w=document.createTreeWalker(document.getElementById('stage'),NodeFilter.SHOW_TEXT);let n;
    while(n=w.nextNode()){if(!n.textContent.trim())continue;const el=n.parentElement;if(hidden(el)||eff(el)<.5)continue;const r=document.createRange();r.selectNodeContents(n);
      for(const rc0 of r.getClientRects()){if(rc0.width<2)continue;const rc=clipRect(el,rc0);if(!rc)continue;texts.push({r:rc,blk:block(n),el,txt:n.textContent.trim().slice(0,24)})}}
    const objs=[...document.querySelectorAll('[data-obj]')].filter(o=>!hidden(o)&&eff(o)>=.5).map(o=>({o,r:clipRect(o.parentElement,o.getBoundingClientRect())})).filter(o=>o.r);
    const capEl=document.querySelector('#cap span');const cap=(+getComputedStyle(capEl).opacity>.5)?capEl.getBoundingClientRect():null;
    const add=(k)=>{(issues[k]=issues[k]||[]).push(+t.toFixed(1))};
    for(let i=0;i<texts.length;i++){const A=texts[i];
      if(A.r.left<60||A.r.right>1020||A.r.top<220||A.r.bottom>1540)add('KELUAR ZONA: "'+A.txt+'" '+label(A.el));
      for(let j=i+1;j<texts.length;j++){const B=texts[j];if(A.blk===B.blk||A.blk.contains(B.blk)||B.blk.contains(A.blk))continue;if(inter(A.r,B.r))add('TEKS×TEKS: "'+A.txt+'" ↔ "'+B.txt+'"')}
      for(const O of objs){if(O.o.contains(A.el)||A.el.contains(O.o))continue;if(inter(A.r,O.r)&&!inside(A.r,O.r))add('TEKS×OBJEK: "'+A.txt+'" ↔ '+label(O.o))}}
    if(cap)for(const O of objs)if(inter(cap,O.r))add('OBJEK×CAPTION: '+label(O.o));
  }
  return issues});
const keys=Object.keys(res);
if(!keys.length)console.log('✓ Tidak ada tabrakan atau teks keluar zona.');
else keys.forEach(k=>{const ts=res[k];console.log((ts.length<3?'~ sesaat ':'✗ ')+k+'  @ '+ts[0]+'–'+ts[ts.length-1]+' dtk ('+ts.length+' sampel)')});
await b.close()})();
