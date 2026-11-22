"""Reels Cerita #03 (satpam/tim packing): animasi penuh Motion Kit 'Tinta & Kertas' dari timing.json vo_prep.
Pakai: python3 scratch/gen_parkir.py out/reel16/timing.json  -> animatic/mk-parkir.html + out/reel16/events.json"""
import json, sys, re, os
A = '/home/user/content-studio/animatic/'
TIMING = sys.argv[1]; OUT = os.path.dirname(TIMING)
O = open('/home/user/content-studio/scratch/gen_owner.py', encoding='utf-8').read()
exec(O[O.index("def person("):O.index("def card(")])
tl = json.load(open(TIMING, encoding='utf-8'))
nrm = lambda s: ''.join(c for c in s.lower() if c.isalnum())
words, beat_of = [], []
for bi, b in enumerate(tl['beats']):
    for w in b['words']: words.append(w); beat_of.append(bi)
# (kata pembuka, babak 0-based, lewati n)
SC = [('makan',0,0),('pas',0,0),('yang',0,0),('sebelumnya',0,0),
      ('daniel',1,0),('orang',1,0),('lalu',1,0),('kebanyakan',1,0),('yang',1,1),
      ('di',2,0),('tapi',2,0),
      ('mereka',3,0),('satu',3,0),('dua',3,0),
      ('orang',4,0),('follow',4,0)]
starts, k = [], 0
for st, bi, skip in SC:
    n = skip
    while True:
        while k < len(words) and not (beat_of[k] == bi and nrm(words[k]['w']).startswith(st)): k += 1
        if k >= len(words): raise SystemExit('kata pembuka tidak ditemukan: ' + st)
        if n == 0: break
        n -= 1; k += 1
    starts.append(k); k += 1
T0 = [0.0 if i == 0 else round(words[a]['t'] - 0.2, 3) for i, a in enumerate(starts)]
DUR = [round((T0[i + 1] if i + 1 < len(T0) else tl['duration']) - T0[i], 3) for i in range(len(T0))]
KEY = {'satpamnya','akhirnya','packing','akhir','ceritanya','rapi','bersih','follow','terakhir','kahneman','nobel','pelanggan','hangat','lama','dingin','berantakan','kegencet','evaluasi','satpammu'}
def chunks(i):
    a = starts[i]; b = starts[i + 1] if i + 1 < len(starts) else len(words)
    out, cur, t0 = [], [], None
    for j in range(a, b):
        w = words[j]['w'].replace('“','').replace('”','').replace('"','')
        if t0 is None: t0 = words[j]['t'] - T0[i]
        clean = w.rstrip('.,:;')
        cur.append('*%s*' % clean if nrm(w) in KEY else clean)
        if len(cur) == 3 or re.search(r'[.,?!:]$', w) or j == b - 1:
            out.append([round(max(0, t0), 2), ' '.join(cur)]); cur, t0 = [], None
    return out
def W(i, word, d):  # waktu lokal kata pertama yang cocok di adegan i
    a = starts[i]; b = starts[i + 1] if i + 1 < len(starts) else len(words)
    for j in range(a, b):
        if nrm(words[j]['w']).startswith(word): return round(words[j]['t'] - T0[i], 2)
    return d
EV = []
def ev(i, local, kind): EV.append([round(T0[i] + local, 3), kind])
fig = lambda u, shirt, dark, flip=False: person(u, shirt, dark, '#2a1d14', flip).replace('"', '\\"').replace('\n', '')
S = []
# 1 frame 1: restoran enak (headline tampil di frame 1, tanpa animasi masuk)
S.append("""{dur:%s, build:function(L){
 MK.Headline(L,{y:300,size:96,html:'Restorannya enak.<br>Yang diingat: <span style="color:'+C.terra+'">satpamnya.</span>'});
 MK.PaperCard(L,{x:120,y:780,w:840,at:.15,from:'bottom',rot:-1,html:'<div style="display:flex;align-items:center;gap:34px"><svg viewBox="0 0 120 120" width="190" height="190"><circle cx="60" cy="60" r="52" fill="#fff" stroke="#0F0E0C" stroke-width="5"/><circle cx="60" cy="60" r="34" fill="none" stroke="#C8944A" stroke-width="5"/><path d="M44 62 Q60 40 76 62 Q60 80 44 62Z" fill="#B84A2E"/></svg><div><div class="mk-mono" style="font-size:24px;color:#6B6560">ulasan pelanggan</div><div class="mk-fr" style="font-size:74px;color:#C8944A;letter-spacing:.06em">★★★★★</div><div class="mk-ou" style="font-size:40px">makanannya enak, pelayannya ramah</div></div></div>'});
}}""" % DUR[0]); ev(0, .15, 'slide')
# 2 satpam main HP
S.append("""{dur:%s, build:function(L){
 var f=MK.el('div','left:120px;top:470px;width:330px;height:620px',"%s",L.root);f.className='mk-a';
 var ph=MK.el('div','left:380px;top:770px;width:70px;height:120px;border-radius:12px;background:#0F0E0C',' ',L.root);ph.className='mk-a';
 var b=MK.PaperCard(L,{x:500,y:520,w:470,at:W1,from:'right',rot:2,html:'<div class="mk-fr" style="font-size:64px;line-height:1">“Mundur…<br>mundur.”</div><div class="mk-ou" style="font-size:30px;color:#6B6560;margin-top:14px">(sambil lihat HP)</div>'});
 MK.Subtitle(L,%s,{y:1390});
 L.on(function(t){f.style.transform='translateY('+(Math.sin(t*3)*4)+'px)';ph.style.transform='rotate('+(Math.sin(t*2)*4)+'deg)'});
}}""".replace('W1', str(W(1, 'nyuruh', .8))) % (DUR[1], fig('p2', '#6B6560', '#4a4540'), json.dumps(chunks(1), ensure_ascii=False))); ev(1, W(1, 'nyuruh', .8), 'pop')
# 3 yang kamu ceritain: satpamnya
S.append("""{dur:%s, build:function(L){
 MK.PaperCard(L,{x:96,y:500,w:888,at:.1,from:'bottom',rot:-1.5,html:'<div class="mk-mono" style="font-size:24px;color:#6B6560">cerita di mobil, perjalanan pulang</div><div class="mk-ou" style="font-size:52px;line-height:1.25;margin-top:18px">“Makanannya enak sih…<br>tapi satpamnya, ya ampun.”</div>'});
 MK.MarkerCircle(L,{x:240,y:684,w:230,h:36,at:W2});
 MK.Subtitle(L,%s,{y:1390});
}}""".replace('W2', str(W(2, 'satpamnya', 1.4))) % (DUR[2], json.dumps(chunks(2), ensure_ascii=False))); ev(2, .1, 'slide'); ev(2, W(2, 'satpamnya', 1.4), 'scratch')
# 4 perkenalan berfoto (lengkap)
S.append("""{dur:%s, build:function(L){
 var ph=MK.el('div','left:96px;top:420px;width:420px;height:560px;border-radius:12px;overflow:hidden;box-shadow:0 18px 40px -18px rgba(15,14,12,.45);background:#B84A2E','<img src="../foto/profil-seminar.jpg" style="width:100%%;height:100%%;object-fit:cover;object-position:50%% 20%%">',L.root);ph.className='mk-a';
 var nm=MK.el('div','left:560px;top:430px;width:430px;font-size:76px;line-height:.95','ALDY<br>SYAHREZA',L.root);nm.className='mk-a mk-fr';
 var c1=MK.PaperCard(L,{x:560,y:650,w:420,at:W3a,from:'right',rot:1,html:'<div class="mk-fr" style="font-size:46px">100+ BRAND</div><div class="mk-ou" style="font-size:26px;color:#6B6560">lintas industri</div>'});
 var c2=MK.PaperCard(L,{x:560,y:830,w:420,at:W3b,from:'right',rot:-1,html:'<div class="mk-fr" style="font-size:46px;color:#B84A2E">360°</div><div class="mk-ou" style="font-size:26px;color:#6B6560">dari hulu sampai hilir</div>'});
 MK.Subtitle(L,%s,{y:1390});
 L.on(function(t){var k=MK.pr(t,.05,.4);ph.style.opacity=k;ph.style.transform='rotate(-2deg) translateY('+((1-MK.E.out(k))*40)+'px)';nm.style.opacity=MK.pr(t,W3n,.3)});
}}""".replace('W3a', str(W(3, 'seratus', 4))).replace('W3b', str(W(3, 'tiga', 7))).replace('W3n', str(W(3, 'aldy', 1.6) - .2)) % (DUR[3], json.dumps(chunks(3), ensure_ascii=False))); ev(3, .05, 'slide'); ev(3, W(3, 'seratus', 4), 'pop'); ev(3, W(3, 'tiga', 7), 'pop')
# 5 Daniel Kahneman
S.append("""{dur:%s, tr:'sweep', build:function(L){
 MK.PaperCard(L,{x:96,y:470,w:888,at:.15,from:'left',rot:-1,html:'<div class="mk-mono" style="font-size:24px;color:#6B6560">psikolog · peraih Nobel Ekonomi 2002</div><div class="mk-fr" style="font-size:96px;line-height:1;margin-top:14px">Daniel<br>Kahneman</div>'});
 MK.Subtitle(L,%s,{y:1390});
}}""" % (DUR[4], json.dumps(chunks(4), ensure_ascii=False))); ev(4, 0, 'sweep')
# 6-8 tangan & baskom air (eksperimen Kahneman)
BASIN = r"""
function basin(L,o){ // o: x,y,s(scale),label,dur(detik eksperimen),tDip,tWarm(null=tanpa hangat),tEnd(waktu lokal hitungan selesai),dim
 var W=420*o.s,H=520*o.s,box=MK.el('div','left:'+o.x+'px;top:'+o.y+'px;width:'+W+'px;height:'+H+'px',' ',L.root);box.className='mk-a';
 var sv='<svg viewBox="0 0 420 520" width="'+W+'" height="'+H+'" style="overflow:visible">'
 +'<g id="'+o.id+'hand"><rect x="170" y="-40" width="80" height="220" rx="36" fill="#F1C9A3" stroke="#0F0E0C" stroke-width="6"/>'
 +'<path d="M150 170 Q150 130 190 128 L232 128 Q272 130 272 170 L272 300 Q272 330 250 332 L236 332 L236 360 Q236 372 226 372 Q216 372 216 360 L216 336 L204 336 L204 366 Q204 378 194 378 Q184 378 184 366 L184 336 L172 334 Q150 330 150 300Z" fill="#F1C9A3" stroke="#0F0E0C" stroke-width="6" stroke-linejoin="round"/></g>'
 +'<g id="'+o.id+'brr" stroke="#2A2824" stroke-width="5" stroke-linecap="round" fill="none"><path d="M118 200 l-26 -8 M114 240 l-30 0 M118 280 l-26 8"/><path d="M302 200 l26 -8 M306 240 l30 0 M302 280 l26 8"/></g>'
 +'<path d="M40 300 Q40 470 210 470 Q380 470 380 300Z" fill="#E8E1D5" stroke="#0F0E0C" stroke-width="7"/>'
 +'<clipPath id="'+o.id+'cp"><path d="M44 306 Q44 466 210 466 Q376 466 376 306Z"/></clipPath>'
 +'<g clip-path="url(#'+o.id+'cp)"><rect id="'+o.id+'cold" x="30" y="318" width="360" height="160" fill="#B9BFC2"/><rect id="'+o.id+'warm" x="30" y="318" width="360" height="160" fill="#C8944A" opacity="0"/>'
 +'<rect x="150" y="300" width="122" height="90" fill="#F1C9A3" opacity=".55"/></g>'
 +'<ellipse id="'+o.id+'r1" cx="210" cy="320" rx="80" ry="10" fill="none" stroke="#FBF8F3" stroke-width="4"/>'
 +'<ellipse cx="210" cy="300" rx="170" ry="26" fill="none" stroke="#0F0E0C" stroke-width="7"/>'
 +'<g id="'+o.id+'steam" stroke="#C8944A" stroke-width="6" stroke-linecap="round" fill="none" opacity="0"><path d="M110 270 q-14 -24 0 -48 q14 -24 0 -48"/><path d="M320 270 q-14 -24 0 -48 q14 -24 0 -48"/></g>'
 +'</svg>';
 box.innerHTML=sv;
 var lab=MK.el('div','left:'+o.x+'px;top:'+(o.y+H+12)+'px;width:'+W+'px;text-align:center;font-size:'+(44*o.s+6)+'px',' ',L.root);lab.className='mk-a mk-fr';
 var cap=MK.el('div','left:'+o.x+'px;top:'+(o.y+H+12+60*o.s+14)+'px;width:'+W+'px;text-align:center;font-size:'+(26*o.s+6)+'px;color:#6B6560',o.label||'',L.root);cap.className='mk-a mk-ou';
 var $=function(i){return document.getElementById(o.id+i)};
 L.on(function(t){
  var k=MK.E.out(MK.pr(t,o.tDip,.6)),h=$('hand');if(h)h.setAttribute('transform','translate('+(o.dim?0:Math.sin(t*38)*1.6*(t>o.tDip?1:0))+','+(k*140-140)+')');
  var c=Math.round(MK.pr(t,o.tDip,Math.max(.1,o.tEnd-o.tDip))*o.dur);lab.innerHTML=c+'<span class="mk-ou" style="font-size:.5em"> detik</span>';
  var r=$('r1');if(r){var q=((t-o.tDip)%1.2+1.2)%1.2/1.2;r.setAttribute('rx',80+q*80);r.setAttribute('opacity',t>o.tDip?1-q:0)}
  var wk=o.tWarm==null?0:MK.pr(t,o.tWarm,.6);var w=$('warm');if(w)w.setAttribute('opacity',wk);var st=$('steam');if(st)st.setAttribute('opacity',wk);
  var br=$('brr');if(br)br.setAttribute('opacity',(t>o.tDip&&wk<.5&&!o.dim)?(Math.floor(t*6)%2?1:.35):0);
  box.style.opacity=o.dim?.45:1;lab.style.opacity=o.dim?.45:1;cap.style.opacity=o.dim?.45:1;
 });
 return box;
}
"""
S.append("""{dur:%s, build:function(L){
 basin(L,{id:'b6',x:330,y:430,s:1,dur:60,tDip:.3,tWarm:null,tEnd:%s,label:'air dingin'});
 MK.Subtitle(L,%s,{y:1390});
}}""" % (DUR[5], max(1.0, DUR[5] - .4), json.dumps(chunks(5), ensure_ascii=False))); ev(5, .3, 'splash')
S.append("""{dur:%s, build:function(L){
 basin(L,{id:'b7',x:330,y:430,s:1,dur:90,tDip:.2,tWarm:%s,tEnd:%s,label:'30 detik terakhir sedikit lebih hangat'});
 MK.Subtitle(L,%s,{y:1390});
}}""" % (DUR[6], W(6, 'hangat', 3) - .5, max(1.0, DUR[6] - .4), json.dumps(chunks(6), ensure_ascii=False))); ev(6, .2, 'splash'); ev(6, W(6, 'hangat', 3) - .5, 'pop')
# 8 kebanyakan memilih yang 90 detik: dua baskom, yang hangat dilingkari
S.append("""{dur:%s, build:function(L){
 basin(L,{id:'b8a',x:90,y:470,s:.78,dur:60,tDip:-5,tWarm:null,tEnd:-4,label:'60 detik, dingin',dim:true});
 basin(L,{id:'b8b',x:600,y:470,s:.78,dur:90,tDip:-5,tWarm:-4,tEnd:-4,label:'90 detik, akhirnya hangat'});
 var lb=MK.el('div','left:96px;top:1090px;width:888px;text-align:center;font-size:42px','mayoritas memilih mengulang <span style="color:#B84A2E">yang ini</span>',L.root);lb.className='mk-a mk-ou';
 MK.MarkerCircle(L,{x:600,y:470,w:330,h:520,at:W8});
 MK.Subtitle(L,%s,{y:1390});
 L.on(function(t){lb.style.opacity=MK.pr(t,W8,.3)});
}}""".replace('W8', str(W(7, 'mengulang', 1))) % (DUR[7], json.dumps(chunks(7), ensure_ascii=False))); ev(7, W(7, 'mengulang', 1), 'scratch')
# 9 Yang diingat: akhirnya (headline + lingkar di ujung)
S.append("""{dur:%s, build:function(L){
 MK.Headline(L,{y:560,size:120,at:.05,html:'Yang diingat:<br><span style="color:#B84A2E">akhirnya.</span>'});
 MK.InkPath(L,{d:'M120 1050 C320 1000 420 1110 600 1040 S860 980 940 1040',w:8,at:.2,dur:.7});
 MK.MarkerCircle(L,{x:880,y:1010,w:90,h:60,at:%s});
}}""" % (DUR[8], W(8, 'akhirnya', .9))); ev(8, .2, 'draw'); ev(8, W(8, 'akhirnya', .9), 'scratch')
# 10 perjalanan pelanggan: iklan -> foto -> admin -> paket dibuka
S.append("""{dur:%s, tr:'sweep', build:function(L){
 MK.InkPath(L,{d:'M150 760 L930 760',w:8,at:.1,dur:.8});
 var lab=['iklan','foto produk','admin','paket dibuka'],xs=[150,410,670,930],at=[.3,W10a,W10b,W10c],dots=[],tx=[];
 for(var i=0;i<4;i++){var last=i===3;var d=MK.el('div','left:'+(xs[i]-28)+'px;top:732px;width:56px;height:56px;border-radius:50%%;border:6px solid '+(last?'#B84A2E':'#0F0E0C')+';background:'+(last?'#B84A2E':'#FBF8F3'),' ',L.root);d.className='mk-a';dots.push(d);
  var x=MK.el('div','left:'+(xs[i]-110)+'px;width:220px;top:'+(i%%2?640:820)+'px;text-align:center;font-size:32px;color:'+(last?'#B84A2E':'#0F0E0C'),lab[i],L.root);x.className='mk-a mk-ou';tx.push(x)}
 var tag=MK.el('div','left:640px;top:470px;font-size:30px;color:#6B6560;text-align:center;width:420px','satpammu ada di sini ↓',L.root);tag.className='mk-a mk-mono';
 MK.Subtitle(L,%s,{y:1390});
 L.on(function(t){for(var i=0;i<4;i++){var k=MK.pr(t,at[i],.3);dots[i].style.opacity=k;tx[i].style.opacity=k;dots[i].style.transform='scale('+(.6+.4*MK.E.out(k))+')'}tag.style.opacity=MK.pr(t,W10t,.3)});
}}""".replace('W10a', str(W(9, 'foto', 1.5))).replace('W10b', str(W(9, 'admin', 2.5))).replace('W10c', str(W(9, 'satpammu', 1.2))).replace('W10t', str(W(9, 'packing', 2.5))) % (DUR[9], json.dumps(chunks(9), ensure_ascii=False))); ev(9, 0, 'sweep'); ev(9, W(9, 'satpammu', 1.2), 'pop')
# 11 paket dibuka berantakan + cap
S.append("""{dur:%s, build:function(L){
 var bx=MK.el('div','left:170px;top:440px;width:740px;height:620px','<svg viewBox="0 0 740 620" width="740" height="620"><path d="M40 120 L700 100 L720 590 L30 600Z" fill="#C8944A" stroke="#0F0E0C" stroke-width="6"/><path d="M90 170 L650 160 L660 540 L80 550Z" fill="#8a6a3c"/><path d="M120 300 Q260 240 380 330 L520 300 L560 470 L150 500Z" fill="#FBF8F3" stroke="#0F0E0C" stroke-width="5"/><path d="M300 340 L330 380 L300 420" fill="none" stroke="#0F0E0C" stroke-width="4"/><path d="M20 130 L310 240 M720 110 L430 250 M60 80 L240 300 M600 90 L700 330" stroke="#d9d0bd" stroke-width="26" stroke-linecap="round" opacity=".9"/></svg>',L.root);bx.className='mk-a';
 var e=MK.el('div','left:250px;top:1080px;width:580px;text-align:center;font-size:30px;color:#6B6560','(kosong. tanpa satu kata pun dari kamu)',L.root);e.className='mk-a mk-mono';
 MK.StampBocor(L,{x:560,y:450,at:%s,rot:-8,size:54});
 MK.Subtitle(L,%s,{y:1390});
 L.on(function(t){var k=MK.pr(t,.05,.35);bx.style.opacity=k;bx.style.transform='translateY('+((1-MK.E.out(k))*50)+'px)';e.style.opacity=MK.pr(t,%s,.3)});
}}""" % (DUR[10], W(10, 'kata', 5.5), json.dumps(chunks(10), ensure_ascii=False), W(10, 'gak', 5))); ev(10, .05, 'slide'); ev(10, W(10, 'kata', 5.5), 'stamp')
# 12 mereka bukan malas: figur packer + label akhir cerita
S.append("""{dur:%s, tr:'sweep', build:function(L){
 var f=MK.el('div','left:140px;top:480px;width:330px;height:620px',"%s",L.root);f.className='mk-a';
 var tag=MK.PaperCard(L,{x:520,y:600,w:440,at:%s,from:'right',rot:-3,html:'<div class="mk-mono" style="font-size:22px;color:#6B6560">tim packing</div><div class="mk-fr" style="font-size:58px;line-height:1;color:#B84A2E;margin-top:8px">AKHIR<br>CERITA</div>'});
 MK.Subtitle(L,%s,{y:1390});
 L.on(function(t){f.style.transform='translateY('+(Math.sin(t*3)*4)+'px)'});
}}""" % (DUR[11], fig('p12', '#C8944A', '#a57a35'), W(11, 'akhir', 4.5) - .2, json.dumps(chunks(11), ensure_ascii=False))); ev(11, 0, 'sweep'); ev(11, W(11, 'akhir', 4.5) - .2, 'pop')
# 13 standar meja packing (3 centang)
S.append("""{dur:%s, build:function(L){
 var rows=['RAPI','BERSIH','1 KARTU TERIMA KASIH'],at=[%s,%s,%s],h='<div class="mk-mono" style="font-size:24px;color:#6B6560">ditempel di meja packing</div><div class="mk-fr" style="font-size:54px;margin:10px 0 18px">Standar akhir</div>';
 for(var i=0;i<3;i++)h+='<div style="display:flex;align-items:center;gap:22px;margin:16px 0"><div id="ck'+i+'" style="width:54px;height:54px;border:5px solid #0F0E0C;border-radius:10px;font:800 46px/44px Outfit;text-align:center;color:#B84A2E"></div><div class="mk-ou" style="font-size:44px">'+rows[i]+'</div></div>';
 MK.PaperCard(L,{x:120,y:470,w:840,at:.1,from:'bottom',rot:-1.2,html:h});
 MK.Subtitle(L,%s,{y:1390});
 L.on(function(t){for(var i=0;i<3;i++){var c=document.getElementById('ck'+i);if(c)c.textContent=t>=at[i]?'✓':''}});
}}""" % (DUR[12], W(12, 'rapi', 3.5), W(12, 'bersih', 4.3), W(12, 'kartu', 5.2), json.dumps(chunks(12), ensure_ascii=False))); ev(12, .1, 'slide'); [ev(12, W(12, w_, d_), 'tick') for w_, d_ in (('rapi', 3.5), ('bersih', 4.3), ('kartu', 5.2))]
# 14 evaluasi bareng: tiga figur + kotak + bubble
S.append("""{dur:%s, build:function(L){
 var xs=[70,390,710],cs=[['#B84A2E','#8f3a24'],['#0F0E0C','#2a2622'],['#C8944A','#a57a35']],nm=['owner','admin','packing'];
 %s
 var box=MK.el('div','left:400px;top:1000px;width:280px;height:150px;background:#C8944A;border:6px solid #0F0E0C;border-radius:8px',' ',L.root);box.className='mk-a';
 var bub=MK.PaperCard(L,{x:250,y:420,w:580,at:%s,from:'bottom',rot:1,html:'<div class="mk-fr" style="font-size:50px;line-height:1.1">“Kalau aku<br>pelanggannya…”</div>'});
 MK.Subtitle(L,%s,{y:1390});
}}""" % (DUR[13], ''.join("var f%d=MK.el('div','left:%dpx;top:560px;width:280px;height:520px',\"%s\",L.root);f%d.className='mk-a';var n%d=MK.el('div','left:%dpx;top:1170px;width:280px;text-align:center;font-size:26px;color:#6B6560','%s',L.root);n%d.className='mk-a mk-mono';" % (i, x, fig('p14%d' % i, c[0], c[1], i == 2), i, i, x, n, i) for i, (x, c, n) in enumerate(zip([70, 400, 730], [['#B84A2E', '#8f3a24'], ['#0F0E0C', '#2a2622'], ['#C8944A', '#a57a35']], ['owner', 'admin', 'packing']))), W(13, 'rasakan', 3), json.dumps(chunks(13), ensure_ascii=False))); ev(13, W(13, 'rasakan', 3), 'pop')
# 15 kalimat penutup
S.append("""{dur:%s, tr:'sweep', build:function(L){
 MK.PaperCard(L,{x:96,y:520,w:888,at:.1,from:'bottom',rot:-1,html:'<div class="mk-fri" style="font-size:64px;line-height:1.15">Orang yang pegang momen terakhir sering yang <span style="color:#B84A2E">paling jarang</span> kamu ajak ngobrol.</div>'});
}}""" % DUR[14]); ev(14, 0, 'sweep')
# 16 follow
S.append("""{dur:%s, build:function(L){
 MK.SeriesCard(L,{series:'CATATAN MEJA ALDY',title:'Momen kecil<br>berikutnya.'});
 var b=MK.el('div','left:96px;top:1180px;padding:20px 44px;border-radius:999px;background:#B84A2E;color:#FBF8F3;font-size:44px','Follow',L.root);b.className='mk-a mk-ou';
 L.on(function(t){var k=MK.pr(t,.8,.3);b.style.opacity=k;b.style.transform='scale('+(.8+.2*MK.E.over(k))+')'});
}}""" % DUR[15]); ev(15, .8, 'chime')
html = ('<!DOCTYPE html>\n<html><head><meta charset="utf-8"><title>Cerita #03 satpam</title><link rel="stylesheet" href="motionkit/fonts-mk.css"></head><body>\n'
        '<script src="motionkit/kit.js"></script>\n<script>\nvar C=MK.C;\n' + BASIN + '\nMK.run([\n' + ',\n'.join(S) + '\n]);\n</script>\n</body></html>\n')
open(A + 'mk-parkir.html', 'w', encoding='utf-8').write(html)
json.dump({'duration': tl['duration'], 'events': EV, 'cuts': T0}, open(os.path.join(OUT, 'events.json'), 'w'))
print('ok', len(S), 'adegan', round(sum(DUR), 1), 'dtk'); print([(SC[i][0], DUR[i]) for i in range(len(SC))])
