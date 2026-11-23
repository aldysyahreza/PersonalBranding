"""Reels 'metrik campaign branding': animasi penuh Motion Kit dari timing.json vo_prep.
Pakai: python3 scratch/gen_metrik.py out/reel17/timing.json -> animatic/mk-metrik.html + out/reel17/events.json"""
import json, sys, re, os
A = '/home/user/content-studio/animatic/'
TIMING = sys.argv[1]; OUT = os.path.dirname(TIMING)
tl = json.load(open(TIMING, encoding='utf-8'))
nrm = lambda s: ''.join(c for c in s.lower() if c.isalnum())
words, beat_of = [], []
for bi, b in enumerate(tl['beats']):
    for w in b['words']: words.append(w); beat_of.append(bi)
SC = [('campaign',0,0),('karena',0,0),('yang',0,0),('sebelumnya',0,0),
      ('banyak',1,0),('campaign',1,1),
      ('dan',2,0),('riset',2,0),('jadi',2,0),
      ('empat',3,0),('iklan',3,0),('kol',3,0),('kalau',3,0),('sampai',3,0),('satu',3,1),('kuncinya',3,0),
      ('simpan',4,0)]
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
KEY = {'tujuan','konsep','aktivasi','kol','reach','impression','frequency','thruplay','save','share','cac','diskon','setahun','perbaiki','rentang','panjang','nielsen','alat','ukurnya','simpan','iklan','bertahap','catat','gerak'}
def chunks(i):
    a = starts[i]; b = starts[i + 1] if i + 1 < len(starts) else len(words)
    out, cur, t0 = [], [], None
    for j in range(a, b):
        w = words[j]['w']
        if t0 is None: t0 = words[j]['t'] - T0[i] + .03
        clean = w.rstrip('.,:;?')
        cur.append('*%s*' % clean if nrm(w) in KEY else clean)
        if len(cur) == 3 or re.search(r'[.,?!:]$', w) or j == b - 1:
            out.append([round(max(0, t0), 2), ' '.join(cur)]); cur, t0 = [], None
    return out
def W(i, word, d):
    a = starts[i]; b = starts[i + 1] if i + 1 < len(starts) else len(words)
    for j in range(a, b):
        if nrm(words[j]['w']).startswith(word): return round(words[j]['t'] - T0[i], 2)
    return d
EV = []
def ev(i, local, kind): EV.append([round(T0[i] + local, 3), kind])
sub = lambda i: 'MK.Subtitle(L,%s,{y:1390});' % json.dumps(chunks(i), ensure_ascii=False)
def kam(name, mean, y, at, x=96, w=888, rot=-1, color='#0F0E0C'):
    h = ('<div class="mk-fr" style="font-size:58px;line-height:1;color:%s">%s</div>'
         '<div class="mk-ou" style="font-size:36px;color:#6B6560;margin-top:12px">%s</div>') % (color, name, mean)
    return "MK.PaperCard(L,{x:%d,y:%d,w:%d,at:%s,from:'right',rot:%s,html:'%s'});" % (x, y, w, at, rot, h.replace("'", "\\'"))
def chip(txt, y=250, at=.05):
    return ("var ch=MK.el('div','left:96px;top:%dpx;padding:12px 26px;border-radius:999px;background:#0F0E0C;color:#FBF8F3;font-size:28px;letter-spacing:.08em','%s',L.root);ch.className='mk-a mk-mono';"
            "L.on(function(t){var k=MK.pr(t,%s,.3);ch.style.opacity=k;ch.style.transform='translateY('+((1-MK.E.out(k))*16)+'px)'});") % (y, txt, at)
S = []
def scene(i, body, tr=False):
    S.append("{dur:%s,%s build:function(L){\n%s\n}}" % (DUR[i], " tr:'sweep'," if tr else '', body))
    if tr: ev(i, 0, 'sweep')
# 0 hook frame 1
w = W(0, 'dimatikan', 3.2)
scene(0, """MK.Headline(L,{y:300,size:100,html:'Rp30 juta.<br>Dimatikan di <span style="color:'+C.terra+'">minggu kedua.</span>'});
MK.PaperCard(L,{x:150,y:820,w:780,at:.15,from:'bottom',rot:-1.5,html:'<div class="mk-mono" style="font-size:24px;color:#6B6560">CAMPAIGN BRANDING</div><div class="mk-fr" style="font-size:84px">Rp30.000.000</div><div class="mk-mono" style="font-size:22px;color:#6B6560">contoh hitungan</div><div style="display:flex;align-items:center;gap:24px;margin-top:26px"><div id="sw" style="width:150px;height:76px;border-radius:40px;background:#C8944A;border:5px solid #0F0E0C;position:relative"><div id="kn" style="position:absolute;top:6px;left:80px;width:54px;height:54px;border-radius:50%%;background:#FBF8F3;border:5px solid #0F0E0C"></div></div><div id="st" class="mk-ou" style="font-size:40px">AKTIF</div></div>'});
L.on(function(t){var k=MK.E.out(MK.pr(t,%s,.25));var kn=document.getElementById('kn'),sw=document.getElementById('sw'),st=document.getElementById('st');if(!kn)return;kn.style.left=(80-70*k)+'px';sw.style.background=k>.5?'#B9BFC2':'#C8944A';st.textContent=k>.5?'DIMATIKAN':'AKTIF';st.style.color=k>.5?'#B84A2E':'#0F0E0C'});""" % w)
ev(0, .15, 'slide'); ev(0, w, 'tick')
# 1 balik modal
w = W(1, 'modal', 1.5)
scene(1, """MK.PaperCard(L,{x:120,y:480,w:840,at:.05,from:'right',rot:1,html:'<div class="mk-mono" style="font-size:24px;color:#6B6560">LAPORAN MINGGU KE-2</div><div class="mk-ou" style="font-size:44px;margin-top:14px">Biaya: Rp30 juta</div><div class="mk-ou" style="font-size:44px">Omzet dari iklan: Rp30 juta</div><div class="mk-fr" style="font-size:72px;margin-top:18px">= balik modal</div>'});
MK.StampBocor(L,{x:330,y:960,at:%s,rot:-6,text:'DIMATIKAN'});
%s""" % (w + .3, sub(1)))
ev(1, .05, 'slide'); ev(1, w + .3, 'stamp')
# 2 alat ukurnya salah: penggaris omzet ke bibit
w = W(2, 'alat', 2.4)
scene(2, """var sv=MK.el('div','left:140px;top:420px;width:800px;height:700px','<svg viewBox="0 0 800 700" width="800" height="700"><path d="M300 640 L500 640" stroke="#0F0E0C" stroke-width="8"/><path d="M400 640 L400 520" stroke="#3d6b3a" stroke-width="10" stroke-linecap="round"/><path d="M400 560 Q350 520 360 480 Q400 500 400 560Z M400 540 Q450 500 445 465 Q405 485 400 540Z" fill="#6f9a5a" stroke="#0F0E0C" stroke-width="5"/><g transform="rotate(-8 600 360)"><rect x="560" y="120" width="90" height="520" rx="8" fill="#C8944A" stroke="#0F0E0C" stroke-width="6"/>'+[0,1,2,3,4,5,6,7,8,9].map(function(i){return '<path d="M560 '+(150+i*48)+' l'+(i%%2?26:44)+' 0" stroke="#0F0E0C" stroke-width="5"/>'}).join('')+'</g><text x="240" y="60" font-family="JetBrains Mono,monospace" font-size="26" fill="#6B6560">OMZET MINGGU INI</text></svg>',L.root);sv.className='mk-a';
L.on(function(t){var k=MK.E.over(MK.pr(t,.05,.4));sv.style.opacity=k>0?1:0;sv.style.transform='translateY('+((1-k)*60)+'px)'});
MK.MarkerCircle(L,{x:640,y:520,w:170,h:540,at:%s});
%s""" % (w, sub(2)))
ev(2, .05, 'slide'); ev(2, w, 'scratch')
# 3 perkenalan
scene(3, """var ph=MK.el('div','left:96px;top:420px;width:420px;height:560px;border-radius:12px;overflow:hidden;box-shadow:0 18px 40px -18px rgba(15,14,12,.45);background:#B84A2E','<img src="../foto/profil-seminar.jpg" style="width:100%%;height:100%%;object-fit:cover;object-position:50%% 20%%">',L.root);ph.className='mk-a';
var nm=MK.el('div','left:560px;top:430px;width:430px;font-size:76px;line-height:.95','ALDY<br>SYAHREZA',L.root);nm.className='mk-a mk-fr';
MK.PaperCard(L,{x:560,y:650,w:420,at:%s,from:'right',rot:1,html:'<div class="mk-fr" style="font-size:46px">100+ BRAND</div><div class="mk-ou" style="font-size:26px;color:#6B6560">lintas industri</div>'});
MK.PaperCard(L,{x:560,y:830,w:420,at:%s,from:'right',rot:-1,html:'<div class="mk-fr" style="font-size:46px;color:#B84A2E">360°</div><div class="mk-ou" style="font-size:26px;color:#6B6560">dari hulu sampai hilir</div>'});
%s
L.on(function(t){var k=MK.pr(t,.05,.4);ph.style.opacity=k;ph.style.transform='rotate(-2deg) translateY('+((1-MK.E.out(k))*40)+'px)';nm.style.opacity=MK.pr(t,%s,.3)});""" % (W(3, 'seratus', 4), W(3, 'tiga', 7), sub(3), W(3, 'aldy', 1.6) - .2))
ev(3, .05, 'slide'); ev(3, W(3, 'seratus', 4), 'pop'); ev(3, W(3, 'tiga', 7), 'pop')
# 4 iklan = campaign brand?
wp, ws = W(4, 'padahal', 3.4), W(4, 'satu', 4.8)
scene(4, """MK.PaperCard(L,{x:190,y:520,w:700,at:.05,from:'bottom',rot:-2,html:'<div class="mk-fr" style="font-size:120px;text-align:center">IKLAN</div><div id="q" class="mk-ou" style="font-size:52px;text-align:center;margin-top:10px">= campaign brand?</div>'});
MK.MarkerStrike(L,{x:330,y:760,w:420,h:60,at:%s});
var lb=MK.el('div','left:190px;top:1010px;width:700px;text-align:center;font-size:56px;color:#B84A2E','cuma satu bagian',L.root);lb.className='mk-a mk-fri';
L.on(function(t){lb.style.opacity=MK.pr(t,%s,.3)});
%s""" % (wp + .2, ws, sub(4)), tr=True)
ev(4, wp + .2, 'scratch'); ev(4, ws, 'pop')
# 5 alur campaign
rows = [('tujuan', 30.0, 'TUJUAN', 'mau dikenal sebagai apa, oleh siapa', '#B84A2E'),
        ('konsep', 0, 'KONSEP', 'satu ide besar yang dibawa', '#0F0E0C'),
        ('aktivasi', 0, 'AKTIVASI', 'event offline · live · photoshoot', '#0F0E0C'),
        ('iklan', 0, 'IKLAN & KOL', 'yang memperbesar jangkauan', '#C8944A')]
b5 = ''
for j, (wd, _, nm_, mean, col) in enumerate(rows):
    at = W(5, wd, 1 + j * 3); b5 += kam(nm_, mean, 330 + j * 245, at, rot=(-1 if j % 2 else 1), color=col); ev(5, at, 'slide')
scene(5, b5 + sub(5))
# 6 perjalanan panjang
wg = W(6, 'gak', 4.5)
pts = [(180, 'MINGGU<br>4', 0.9), (540, 'BULAN<br>3', 2.6), (900, 'TAHUN<br>1–2', 3.6)]
b6 = "MK.InkPath(L,{d:'M100 820 Q300 700 540 820 T980 820',w:10,at:.1,dur:1.4});"
for x, lab, at in pts:
    b6 += ("var p%d=MK.el('div','left:%dpx;top:%dpx;width:150px;text-align:center;font-size:34px;line-height:1.05','<div style=\"width:40px;height:40px;margin:0 auto 14px;border-radius:50%%;background:#B84A2E;border:5px solid #0F0E0C\"></div>%s',L.root);p%d.className='mk-a mk-mono';"
           "L.on(function(t){p%d.style.opacity=MK.pr(t,%s,.3)});") % (x, x - 75, 800 if x != 540 else 800, lab, x, x, at)
b6 += ("MK.InkPath(L,{d:'M540 820 Q600 980 760 1080',w:6,at:%s,dur:.5,color:'#6B6560'});"
       "var nq=MK.el('div','left:700px;top:1090px;width:330px;font-size:40px;color:#6B6560','bisa juga<br>gak berefek',L.root);nq.className='mk-a mk-fri';L.on(function(t){nq.style.opacity=MK.pr(t,%s,.3)});") % (wg, wg + .3)
b6 += "var hd=MK.el('div','left:96px;top:380px;width:888px;font-size:84px;line-height:1','Perjalanan<br><span style=\"color:#B84A2E\">panjang.</span>',L.root);hd.className='mk-a mk-fr';L.on(function(t){hd.style.opacity=MK.pr(t,.05,.3)});"
scene(6, b6 + sub(6), tr=True)
ev(6, .1, 'draw'); [ev(6, at, 'pop') for _, _, at in pts]; ev(6, wg, 'scratch')
# 7 Nielsen
wm, wt, wk = W(7, 'minggu', 4.5), W(7, 'tahun', 8.5), W(7, 'kali', 9.8)
scene(7, """MK.PaperCard(L,{x:96,y:330,w:888,at:.05,from:'bottom',rot:0,html:'<div class="mk-mono" style="font-size:24px;color:#6B6560">NIELSEN CATALINA SOLUTIONS (2015) · 31 STUDI</div><div class="mk-ou" style="font-size:40px;margin-top:10px">Efek iklan ke penjualan</div>'});
function bar(y,w,at,lab,col){var b=MK.el('div','left:96px;top:'+y+'px;height:120px;width:'+w+'px;background:'+col+';border:5px solid #0F0E0C;border-radius:8px;transform-origin:left',' ',L.root);b.className='mk-a';var l=MK.el('div','left:96px;top:'+(y+132)+'px;font-size:36px',lab,L.root);l.className='mk-a mk-ou';L.on(function(t){var k=MK.E.out(MK.pr(t,at,.6));b.style.transform='scaleX('+k+')';b.style.opacity=k>0?1:0;l.style.opacity=MK.pr(t,at+.2,.3)});}
bar(640,380,%s,'sampai 12 minggu','#C8944A');
bar(900,760,%s,'jangka panjang, 1–2 tahun','#B84A2E');
var x2=MK.el('div','left:700px;top:620px;font-size:110px;color:#B84A2E','±2x',L.root);x2.className='mk-a mk-fr';L.on(function(t){var k=MK.pr(t,%s,.3);x2.style.opacity=k;x2.style.transform='scale('+(.7+.3*MK.E.over(k))+')'});
var nt=MK.el('div','left:96px;top:1180px;font-size:24px;color:#6B6560','rata-rata, beda per brand',L.root);nt.className='mk-a mk-mono';L.on(function(t){nt.style.opacity=MK.pr(t,%s,.3)});
%s""" % (wm - .3, wt - .3, wk, wk + .3, sub(7)))
ev(7, .05, 'slide'); ev(7, wm - .3, 'draw'); ev(7, wt - .3, 'draw'); ev(7, wk, 'pop')
# 8 ukur pakai rentang waktu
scene(8, """MK.Headline(L,{y:640,size:110,at:.05,html:'Ukur pakai<br><span style="color:'+C.terra+'">rentang waktu.</span>'});""")
ev(8, .05, 'pop')
# 9 4 minggu: aktivasi
wa, wd_, wp_ = W(9, 'aktivasi', 2.7), W(9, 'datang', 4.4), W(9, 'posting', 7)
scene(9, chip('PATOK 1 · 4 MINGGU · TANDA AWAL') + """
var hd=MK.el('div','left:96px;top:360px;width:888px;font-size:96px','AKTIVASI',L.root);hd.className='mk-a mk-fr';L.on(function(t){hd.style.opacity=MK.pr(t,%s,.3)});
""" % wa + kam('Hadir & nonton live', 'berapa yang datang atau nonton', 560, wd_) + kam('Posting tag brand', 'berapa yang posting sambil tag kamu', 820, wp_, rot=1) + sub(9), tr=True)
ev(9, 0.05, 'pop'); ev(9, wd_, 'slide'); ev(9, wp_, 'slide')
# 10 iklan: 4 kamus
b10 = chip('PATOK 1 · 4 MINGGU · IKLAN')
for j, (wd, nm_, mean) in enumerate([('reach', 'REACH', 'berapa orang yang lihat'), ('impression', 'IMPRESSION', 'berapa kali iklan tampil'),
                                       ('frequency', 'FREQUENCY', 'tiap orang lihat berapa kali'), ('thruplay', 'THRUPLAY', 'nonton habis / minimal 15 detik')]):
    at = W(10, wd, 1 + j * 3); b10 += kam(nm_, mean, 340 + j * 240, at, rot=(1 if j % 2 else -1)); ev(10, at, 'slide')
scene(10, b10 + sub(10))
# 11 KOL
b11 = chip('PATOK 1 · 4 MINGGU · KOL')
for j, (wd, nm_, mean) in enumerate([('save', 'SAVE', 'kontennya disimpan'), ('share', 'SHARE', 'kontennya dikirim ke orang lain'), ('komentar', 'KOMENTAR', 'yang nyebut nama brand kamu')]):
    at = W(11, wd, .5 + j * 1.2); b11 += kam(nm_, mean, 360 + j * 250, at, rot=(1 if j % 2 else -1), color='#B84A2E' if j == 2 else '#0F0E0C'); ev(11, at, 'slide')
scene(11, b11 + sub(11))
# 12 gak gerak -> perbaiki konsep
ws_, wpb = W(12, 'setahun', 1.8), W(12, 'perbaiki', 2.8)
scene(12, """MK.PaperCard(L,{x:120,y:420,w:840,at:.05,from:'bottom',rot:-1,html:'<div class="mk-ou" style="font-size:50px">Tanda awal gak gerak?</div><div class="mk-ou" style="font-size:50px;margin-top:22px;color:#6B6560">Nunggu setahun</div>'});
MK.MarkerStrike(L,{x:160,y:560,w:380,h:60,at:%s});
MK.StampBocor(L,{x:200,y:860,at:%s,rot:-5,size:76,text:'PERBAIKI KONSEP'});
%s""" % (ws_, wpb, sub(12)))
ev(12, .05, 'slide'); ev(12, ws_, 'scratch'); ev(12, wpb, 'stamp')
# 13 3 bulan
wn, wc = W(13, 'nyari', 2.4), W(13, 'cac', 6)
scene(13, chip('PATOK 2 · 3 BULAN') + kam('BRANDED SEARCH ↑', 'makin banyak yang nyari nama brand kamu', 420, wn) +
      kam('CAC ↓', 'biaya dapat satu pelanggan baru turun', 720, wc, rot=1, color='#B84A2E') + sub(13), tr=True)
ev(13, wn, 'slide'); ev(13, wc, 'slide')
# 14 1-2 tahun
wb, wdk = W(14, 'pelanggan', 1.5), W(14, 'diskon', 4.5)
scene(14, chip('PATOK 3 · 1–2 TAHUN') + kam('REPEAT ORDER ↑', 'pelanggan balik lagi', 420, wb) +
      kam('DISKON ↓', 'makin jarang butuh diskon', 720, wdk, rot=1, color='#B84A2E') + sub(14), tr=True)
ev(14, wb, 'slide'); ev(14, wdk, 'slide')
# 15 checklist angka awal
tk = [W(15, x, d) for x, d in (('catat', .5), ('semua', 1.1), ('angka', 1.6), ('sebelum', 2.2))]
scene(15, """var rows=['Reach & ThruPlay','Tag & komentar sebut brand','Pencarian nama brand','CAC'],h='<div class="mk-mono" style="font-size:26px;color:#6B6560;margin-bottom:12px">ANGKA SEBELUM CAMPAIGN JALAN</div>';
for(var i=0;i<4;i++)h+='<div style="display:flex;align-items:center;gap:22px;margin:16px 0"><div id="ck'+i+'" style="width:54px;height:54px;border:5px solid #0F0E0C;border-radius:10px;font:800 46px/44px Outfit;text-align:center;color:#B84A2E"></div><div class="mk-ou" style="font-size:44px">'+rows[i]+'</div></div>';
MK.PaperCard(L,{x:110,y:440,w:860,at:.05,from:'bottom',rot:-1,html:h});
var T=%s;L.on(function(t){for(var i=0;i<4;i++){var e=document.getElementById('ck'+i);if(e)e.textContent=t>=T[i]?'✓':''}});
%s""" % (json.dumps(tk), sub(15)))
ev(15, .05, 'slide'); [ev(15, x, 'tick') for x in tk]
# 16 simpan
scene(16, """MK.SeriesCard(L,{series:'DAFTAR CEK CAMPAIGN BRAND',title:'Simpan<br>daftar cek.'});
var b=MK.el('div','left:96px;top:1180px;padding:20px 44px;border-radius:999px;background:#B84A2E;color:#FBF8F3;font-size:44px','Simpan',L.root);b.className='mk-a mk-ou';
L.on(function(t){var k=MK.pr(t,.8,.3);b.style.opacity=k;b.style.transform='scale('+(.8+.2*MK.E.over(k))+')'});""", tr=True)
ev(16, .8, 'chime')
html = ('<!DOCTYPE html>\n<html><head><meta charset="utf-8"><title>Metrik campaign brand</title><link rel="stylesheet" href="motionkit/fonts-mk.css"></head><body>\n'
        '<script src="motionkit/kit.js"></script>\n<script>\nvar C=MK.C;\nMK.run([\n' + ',\n'.join(S) + '\n]);\n</script>\n</body></html>\n')
open(A + 'mk-metrik.html', 'w', encoding='utf-8').write(html)
json.dump({'duration': tl['duration'], 'events': EV, 'cuts': T0}, open(os.path.join(OUT, 'events.json'), 'w'))
print('ok', len(S), 'adegan', round(sum(DUR), 1), 'dtk'); print([(SC[i][0], DUR[i]) for i in range(len(SC))])
