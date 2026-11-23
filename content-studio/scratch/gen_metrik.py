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

HELP = r"""
function P(L,x,y,w,h,html,at){var e=MK.el('div','left:'+x+'px;top:'+y+'px;width:'+w+'px;height:'+h+'px',html,L.root);e.className='mk-a';L.on(function(t){var k=MK.pr(t,at,.35),v=MK.E.over(k);e.style.opacity=k>0?1:0;e.style.transform='scale('+(.55+.45*v)+')'});return e;}
function DOTS(L,x,y,c,r,at,dur,sz){var d=[];for(var i=0;i<c*r;i++){var e=MK.el('div','left:'+(x+(i%c)*(sz+12))+'px;top:'+(y+Math.floor(i/c)*(sz+12))+'px;width:'+sz+'px;height:'+sz+'px;border-radius:50%;border:4px solid #0F0E0C;background:#FBF8F3',' ',L.root);e.className='mk-a';d.push(e)}
 L.on(function(t){var n=Math.floor(MK.pr(t,at,dur)*d.length+.001);for(var i=0;i<d.length;i++){d[i].style.background=i<n?(i%7==3?'#B84A2E':'#C8944A'):'#FBF8F3';d[i].style.opacity=t>=at-.4?1:0}});}
function PANEL(L,x,y,ti,su,at){var e=MK.el('div','left:'+x+'px;top:'+y+'px;width:430px;height:430px;border-radius:18px;background:#FBF8F3;border:5px solid #0F0E0C;box-shadow:0 14px 30px -18px rgba(15,14,12,.5);padding:22px 26px;box-sizing:border-box','<div class="mk-fr" style="font-size:46px;line-height:1">'+ti+'</div><div class="mk-ou" style="font-size:26px;color:#6B6560;margin-top:6px">'+su+'</div>',L.root);e.className='mk-a';L.on(function(t){var k=MK.pr(t,at,.3);e.style.opacity=k>0?1:0;e.style.transform='scale('+(.7+.3*MK.E.over(k))+')'});}
function TREE(s){var h='<svg viewBox="0 0 220 240" width="220" height="240"><path d="M80 236 h60" stroke="#0F0E0C" stroke-width="6"/>';
 if(s==0)h+='<path d="M110 236 V190" stroke="#3d6b3a" stroke-width="8"/><path d="M110 200 Q84 186 90 166 Q112 176 110 200Z M110 192 Q134 174 132 154 Q112 166 110 192Z" fill="#6f9a5a" stroke="#0F0E0C" stroke-width="4"/>';
 else if(s==1)h+='<path d="M110 236 V140" stroke="#7a5230" stroke-width="12"/><circle cx="110" cy="120" r="52" fill="#6f9a5a" stroke="#0F0E0C" stroke-width="5"/>';
 else h+='<path d="M110 236 V120" stroke="#7a5230" stroke-width="16"/><circle cx="110" cy="92" r="84" fill="#5e8a4b" stroke="#0F0E0C" stroke-width="5"/><g fill="#C8944A" stroke="#0F0E0C" stroke-width="4"><ellipse cx="70" cy="110" rx="14" ry="18"/><ellipse cx="140" cy="70" rx="14" ry="18"/><ellipse cx="150" cy="125" rx="14" ry="18"/><ellipse cx="96" cy="58" rx="14" ry="18"/></g>';
 return h+'</svg>';}
"""
TREEC = lambda st: "P(L,880,190,110,120,'<div style=\"transform:scale(.5);transform-origin:0 0\">'+TREE(%d)+'</div>',.1);" % st
S = []
def scene(i, body, tr=False, dolly=0, paper=None):
    S.append("{dur:%s,%s%s%s build:function(L){\n%s\n}}" % (DUR[i], " tr:'sweep'," if tr else '', " dolly:%s," % dolly if dolly else '', " paper:'%s'," % paper if paper else '', body))
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

def R(js, **kw):
    for k_, v_ in kw.items(): js = js.replace('@' + k_ + '@', str(v_))
    return js
# 4 iklan = campaign brand?
wp, ws = W(4, 'padahal', 3.4), W(4, 'satu', 4.8)
scene(4, R("""MK.PaperCard(L,{x:190,y:520,w:700,at:.05,from:'bottom',rot:-2,html:'<div class="mk-fr" style="font-size:120px;text-align:center">IKLAN</div><div class="mk-ou" style="font-size:52px;text-align:center;margin-top:10px">= campaign brand?</div>'});
MK.MarkerStrike(L,{x:330,y:760,w:420,h:60,at:@A@});
var pz=P(L,250,980,580,260,'<svg viewBox="0 0 580 260" width="580" height="260"><g fill="none" stroke="#0F0E0C" stroke-width="6"><rect x="10" y="40" width="120" height="120" rx="14"/><rect x="160" y="40" width="120" height="120" rx="14"/><rect x="310" y="40" width="120" height="120" rx="14"/><rect x="460" y="40" width="110" height="120" rx="14" fill="#C8944A"/></g><text x="290" y="230" text-anchor="middle" font-family="Fraunces,serif" font-style="italic" font-size="46" fill="#B84A2E">cuma satu bagian</text></svg>',@B@);
@SUB@""", A=wp + .2, B=ws, SUB=sub(4)), tr=True, dolly=.05)
ev(4, wp + .2, 'scratch'); ev(4, ws, 'pop')
# 5 alur 2x2 lingkaran ikon
IC = {'tujuan': '<circle cx="80" cy="80" r="56" fill="none" stroke="#FBF8F3" stroke-width="10"/><circle cx="80" cy="80" r="30" fill="none" stroke="#FBF8F3" stroke-width="10"/><circle cx="80" cy="80" r="8" fill="#FBF8F3"/>',
      'konsep': '<path d="M80 22 a42 42 0 0 1 26 75 v18 h-52 v-18 a42 42 0 0 1 26 -75z" fill="none" stroke="#FBF8F3" stroke-width="9"/><path d="M58 132 h44" stroke="#FBF8F3" stroke-width="9" stroke-linecap="round"/>',
      'aktivasi': '<path d="M20 130 L80 30 L140 130Z" fill="none" stroke="#FBF8F3" stroke-width="9" stroke-linejoin="round"/><path d="M80 30 V8 l26 8 -26 8" fill="#FBF8F3" stroke="#FBF8F3" stroke-width="5"/><path d="M62 130 L80 96 L98 130" fill="none" stroke="#FBF8F3" stroke-width="8"/>',
      'iklan': '<path d="M24 64 h26 l58 -34 v100 l-58 -34 h-26z" fill="none" stroke="#FBF8F3" stroke-width="9" stroke-linejoin="round"/><path d="M124 56 q18 24 0 48" fill="none" stroke="#FBF8F3" stroke-width="8" stroke-linecap="round"/>'}
pos = [(300, 520), (780, 520), (300, 940), (780, 940)]
cols = ['#B84A2E', '#0F0E0C', '#0F0E0C', '#C8944A']
labs = ['TUJUAN', 'KONSEP', 'AKTIVASI', 'IKLAN & KOL']
b5 = ''
ats = []
for j, (wd, (cx, cy), col, lb) in enumerate(zip(['tujuan', 'konsep', 'aktivasi', 'iklan'], pos, cols, labs)):
    at = W(5, wd, 1 + j * 3); ats.append(at)
    b5 += R("""P(L,@X@,@Y@,300,300,'<div style="width:280px;height:280px;border-radius:50%;background:@C@;border:7px solid #0F0E0C;display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 160 160" width="150" height="150">@I@</svg></div>',@A@);
var lb@J@=MK.el('div','left:@LX@px;top:@LY@px;width:360px;text-align:center;font-size:44px','@L@',L.root);lb@J@.className='mk-a mk-fr';L.on(function(t){lb@J@.style.opacity=MK.pr(t,@A@+.15,.3)});""",
            X=cx - 150, Y=cy - 150, C=col, I=IC[wd], A=at, J=j, LX=cx - 180, LY=cy + 150, L=lb)
    ev(5, at, 'pop')
for j, (x1, y1, x2, y2) in enumerate([(460, 520, 620, 520), (660, 680, 420, 790), (460, 940, 620, 940)]):
    b5 += "MK.InkPath(L,{d:'M%d %d L%d %d',w:7,at:%s,dur:.4,color:'#6B6560'});" % (x1, y1, x2, y2, ats[j + 1] - .35)
for j, (wd, tx) in enumerate([('event', 'EVENT OFFLINE'), ('live', 'LIVE'), ('photoshoot', 'PHOTOSHOOT')]):
    at = W(5, wd, 9 + j); ev(5, at, 'tick')
    b5 += R("""P(L,@X@,1210,@W@,70,'<div class="mk-mono" style="display:inline-block;padding:12px 22px;border-radius:999px;border:4px solid #0F0E0C;background:#FBF8F3;font-size:28px;transform:rotate(@R@deg)">@T@</div>',@A@);""", X=[96, 430, 610][j], W=[330, 170, 300][j], R=[-3, 2, -2][j], T=tx, A=at)
scene(5, b5 + sub(5), dolly=.04)
# 6 perjalanan panjang + pohon tumbuh
wg = W(6, 'gak', 4.5)
pts = [(180, 'MINGGU 4', 0.9, 0), (540, 'BULAN 3', 2.6, 1), (900, 'TAHUN 1–2', 3.6, 2)]
b6 = "MK.InkPath(L,{d:'M100 900 Q300 780 540 900 T980 900',w:10,at:.1,dur:1.4});"
for x, lab, at, st in pts:
    b6 += R("""P(L,@X@,@Y@,220,300,'<div class="mk-mono" style="text-align:center;font-size:30px;margin-bottom:6px;background:#0F0E0C;color:#FBF8F3;border-radius:999px;padding:6px 0">@L@</div>'+TREE(@S@),@A@);""", X=x - 110, Y={0: 570, 1: 610, 2: 650}[st], S=st, L=lab, A=at)
b6 += R("""MK.InkPath(L,{d:'M540 920 Q600 1060 760 1140',w:6,at:@A@,dur:.5,color:'#6B6560'});
var nq=MK.el('div','left:690px;top:1150px;width:340px;font-size:40px;color:#6B6560','bisa juga<br>gak berefek',L.root);nq.className='mk-a mk-fri';L.on(function(t){nq.style.opacity=MK.pr(t,@B@,.3)});
var hd=MK.el('div','left:96px;top:330px;width:888px;font-size:90px;line-height:1','Perjalanan<br><span style="color:#B84A2E">panjang.</span>',L.root);hd.className='mk-a mk-fr';L.on(function(t){hd.style.opacity=MK.pr(t,.05,.3)});""", A=wg, B=wg + .3)
scene(6, b6 + sub(6), tr=True, dolly=.06)
ev(6, .1, 'draw'); [ev(6, at, 'pop') for _, _, at, _ in pts]; ev(6, wg, 'scratch')
# 7 Nielsen: kalender 12 minggu vs 2 tahun
wm, wt, wk = W(7, 'minggu', 4.5), W(7, 'tahun', 8.5), W(7, 'kali', 9.8)
scene(7, R("""var hd=MK.el('div','left:96px;top:300px;font-size:26px;color:#6B6560','NIELSEN CATALINA SOLUTIONS (2015) · 31 STUDI',L.root);hd.className='mk-a mk-mono';
var h2=MK.el('div','left:96px;top:345px;font-size:56px','Efek iklan ke penjualan',L.root);h2.className='mk-a mk-fr';
var g=MK.el('div','left:96px;top:450px;width:888px;height:240px',' ',L.root);g.className='mk-a';var cells=[];
for(var i=0;i<12;i++){var c=MK.el('div','left:'+(i*74)+'px;top:0;width:62px;height:62px;border-radius:10px;border:4px solid #0F0E0C;background:#FBF8F3',' ',g);c.className='mk-a';cells.push(c);}
var l1=MK.el('div','left:96px;top:540px;font-size:40px','12 minggu: efek pendek',L.root);l1.className='mk-a mk-ou';
function bar(y,w,at,col){var b=MK.el('div','left:96px;top:'+y+'px;height:130px;width:'+w+'px;background:'+col+';border:6px solid #0F0E0C;border-radius:10px;transform-origin:left',' ',L.root);b.className='mk-a';L.on(function(t){var k=MK.E.out(MK.pr(t,at,.7));b.style.transform='scaleX('+k+')';b.style.opacity=k>0?1:0});}
bar(700,380,@M@,'#C8944A');bar(880,780,@T@,'#B84A2E');
var l2=MK.el('div','left:96px;top:1030px;font-size:40px','1–2 tahun: efek jangka panjang',L.root);l2.className='mk-a mk-ou';
var x2=MK.el('div','left:520px;top:640px;font-size:150px;color:#B84A2E','±2x',L.root);x2.className='mk-a mk-fr';
var nt=MK.el('div','left:96px;top:1110px;font-size:24px;color:#6B6560','rata-rata, beda per brand',L.root);nt.className='mk-a mk-mono';
L.on(function(t){hd.style.opacity=h2.style.opacity=MK.pr(t,.05,.3);for(var i=0;i<12;i++){cells[i].style.background=t>@M0@+i*.12?'#C8944A':'#FBF8F3'}l1.style.opacity=MK.pr(t,@M@,.3);l2.style.opacity=MK.pr(t,@T@+.3,.3);var k=MK.pr(t,@K@,.3);x2.style.opacity=k;x2.style.transform='rotate(-6deg) scale('+(.6+.4*MK.E.over(k))+')';nt.style.opacity=MK.pr(t,@K@+.3,.3)});
@SUB@""", M=wm - .2, M0=wm - 1.6, T=wt - .3, K=wk, SUB=sub(7)), paper='white', dolly=.05)
ev(7, wm - 1.6, 'tick'); ev(7, wm - .2, 'draw'); ev(7, wt - .3, 'draw'); ev(7, wk, 'stamp')
# 8 jam pasir/jam
scene(8, """var ck=MK.el('div','left:340px;top:330px;width:400px;height:400px','<svg viewBox="0 0 200 200" width="400" height="400"><circle cx="100" cy="100" r="88" fill="#FBF8F3" stroke="#0F0E0C" stroke-width="8"/><g stroke="#0F0E0C" stroke-width="6" stroke-linecap="round"><path d="M100 22v14M100 164v14M22 100h14M164 100h14"/></g><path id="hm" d="M100 100 L100 48" stroke="#B84A2E" stroke-width="9" stroke-linecap="round"/><path id="hh" d="M100 100 L136 100" stroke="#0F0E0C" stroke-width="9" stroke-linecap="round"/><circle cx="100" cy="100" r="9" fill="#0F0E0C"/></svg>',L.root);ck.className='mk-a';
MK.Headline(L,{y:840,size:116,at:.15,html:'Ukur pakai<br><span style="color:'+C.terra+'">rentang waktu.</span>'});
L.on(function(t){var m=document.getElementById('hm'),h=document.getElementById('hh');if(m){m.setAttribute('transform','rotate('+(t*540)+' 100 100)');h.setAttribute('transform','rotate('+(t*45)+' 100 100)')}var k=MK.E.over(MK.pr(t,0,.35));ck.style.transform='scale('+(.5+.5*k)+')'});""", dolly=.08)
ev(8, .05, 'pop')
# 9 aktivasi: kerumunan + post tag
wa, wd_, wp_ = W(9, 'aktivasi', 2.7), W(9, 'datang', 4.4), W(9, 'posting', 7)
scene(9, chip('PATOK 1 · 4 MINGGU · TANDA AWAL') + TREEC(0) + R("""
var hd=MK.el('div','left:96px;top:330px;width:888px;font-size:100px','AKTIVASI',L.root);hd.className='mk-a mk-fr';
DOTS(L,96,500,8,5,@D@,1.6,46);
MK.CountUp(L,{x:96,y:800,from:0,to:240,at:@D@,dur:1.6,size:96,suffix:'hadir / nonton live'});
var tags=[];for(var i=0;i<3;i++){var q=MK.el('div','left:'+(600+i*28)+'px;top:'+(500+i*150)+'px;width:380px;padding:18px 22px;background:#FBF8F3;border:5px solid #0F0E0C;border-radius:16px;box-shadow:0 10px 24px -12px rgba(15,14,12,.5)','<div style="display:flex;gap:16px;align-items:center"><div style="width:84px;height:84px;border-radius:10px;background:'+['#C8944A','#B84A2E','#6B6560'][i]+'"></div><div class="mk-ou" style="font-size:32px">posting<br><b style="color:#B84A2E">@brandkamu</b></div></div>',L.root);q.className='mk-a';tags.push(q)}
var nt=MK.el('div','left:96px;top:1240px;font-size:24px;color:#6B6560','angka = contoh',L.root);nt.className='mk-a mk-mono';
L.on(function(t){hd.style.opacity=MK.pr(t,@A@,.3);for(var i=0;i<3;i++){var k=MK.pr(t,@P@+i*.35,.35);tags[i].style.opacity=k>0?1:0;tags[i].style.transform='rotate('+[-3,2,-1][i]+'deg) translateX('+((1-MK.E.over(k))*500)+'px)'}nt.style.opacity=MK.pr(t,@D@,.3)});
""", A=wa, D=wd_, P=wp_) + sub(9), tr=True, dolly=.04)
ev(9, .05, 'pop'); ev(9, wd_, 'tick'); [ev(9, wp_ + i * .35, 'slide') for i in range(3)]
# 10 iklan: 4 panel animasi
wr, wi, wf, wtp = W(10, 'reach', 1), W(10, 'impression', 4), W(10, 'frequency', 7), W(10, 'thruplay', 10)
scene(10, chip('PATOK 1 · 4 MINGGU · IKLAN') + TREEC(0) + R("""
PANEL(L,96,330,'REACH','orang yang lihat',@R@);DOTS(L,130,470,6,4,@R@+.2,1.2,40);MK.CountUp(L,{x:130,y:690,from:0,to:12000,at:@R@+.2,dur:1.2,size:60,suffix:'orang'});
PANEL(L,554,330,'IMPRESSION','kali iklan tampil',@I@);
var st=[];for(var i=0;i<4;i++){var c=MK.el('div','left:'+(600+i*34)+'px;top:'+(470+i*22)+'px;width:200px;height:130px;border-radius:12px;border:5px solid #0F0E0C;background:'+['#FBF8F3','#F4EBD9','#C8944A','#B84A2E'][i],' ',L.root);c.className='mk-a';st.push(c)}
MK.CountUp(L,{x:590,y:690,from:0,to:30000,at:@I@+.3,dur:1.2,size:60,suffix:'tampil'});
PANEL(L,96,790,'FREQUENCY','tiap orang lihat berapa kali',@F@);
var ey=[];for(var i=0;i<3;i++){var e=MK.el('div','left:'+(130+i*120)+'px;top:950px;width:100px;height:60px','<svg viewBox="0 0 100 60" width="100" height="60"><path d="M4 30 Q50 -6 96 30 Q50 66 4 30Z" fill="#FBF8F3" stroke="#0F0E0C" stroke-width="6"/><circle cx="50" cy="30" r="13" fill="#0F0E0C"/></svg>',L.root);e.className='mk-a';ey.push(e)}
var fq=MK.el('div','left:130px;top:1030px;font-size:84px;color:#B84A2E','2,5x',L.root);fq.className='mk-a mk-fr';
PANEL(L,554,790,'THRUPLAY','nonton habis / ≥15 detik',@T@);
var vd=MK.el('div','left:590px;top:940px;width:360px;height:150px;border-radius:12px;background:#0F0E0C','<svg viewBox="0 0 360 150" width="360" height="150"><path d="M160 45 L205 72 L160 99Z" fill="#FBF8F3"/></svg>',L.root);vd.className='mk-a';
var pb=MK.el('div','left:590px;top:1110px;width:360px;height:22px;border-radius:12px;background:#E8E1D5;border:4px solid #0F0E0C;overflow:hidden','<div id="pf" style="height:100%;width:0;background:#B84A2E"></div>',L.root);pb.className='mk-a';
var nt=MK.el('div','left:96px;top:1270px;font-size:24px;color:#6B6560','angka = contoh',L.root);nt.className='mk-a mk-mono';
L.on(function(t){for(var i=0;i<4;i++){var k=MK.pr(t,@I@+.1+i*.15,.3);st[i].style.opacity=k>0?1:0;st[i].style.transform='rotate('+(i*3-4)+'deg) translateY('+((1-MK.E.over(k))*120)+'px)'}
for(var i=0;i<3;i++){var k=MK.pr(t,@F@+.2+i*.25,.25);ey[i].style.opacity=k;ey[i].style.transform='scaleY('+(Math.sin(t*6+i)>.92?.15:1)+')'}fq.style.opacity=MK.pr(t,@F@+.9,.3);
var v=MK.pr(t,@T@+.2,.3);vd.style.opacity=pb.style.opacity=v;var f=document.getElementById('pf');if(f)f.style.width=(MK.E.io(MK.pr(t,@T@+.4,1.8))*100)+'%';nt.style.opacity=MK.pr(t,@R@,.3)});
""", R=wr, I=wi, F=wf, T=wtp) + sub(10))
ev(10, wr, 'slide'); ev(10, wr + .2, 'tick'); ev(10, wi, 'slide'); ev(10, wf, 'slide'); ev(10, wtp, 'slide'); ev(10, wtp + 2.2, 'chime')
# 11 KOL: ponsel + ikon + komentar
wsv, wsh, wko = W(11, 'save', .4), W(11, 'share', 1), W(11, 'komentar', 1.7)
scene(11, chip('PATOK 1 · 4 MINGGU · KOL') + TREEC(0) + R("""
var ph=MK.el('div','left:110px;top:330px;width:460px;height:900px;border-radius:52px;background:#0F0E0C;padding:20px','<div style="width:100%;height:100%;border-radius:36px;background:#FBF8F3;overflow:hidden"><div style="height:470px;background:linear-gradient(160deg,#C8944A,#B84A2E)"></div><div class="mk-ou" style="padding:18px 22px;font-size:30px;color:#6B6560">@kreator · konten kolaborasi</div></div>',L.root);ph.className='mk-a';
var bub=MK.el('div','left:150px;top:960px;width:560px;padding:20px 24px;border-radius:20px;background:#FBF8F3;border:5px solid #0F0E0C','<div class="mk-ou" style="font-size:34px">“ini <b style="color:#B84A2E">brand apa</b>, kak? mau coba”</div>',L.root);bub.className='mk-a';
function ic(y,path,lab,to,at){var e=MK.el('div','left:640px;top:'+y+'px;width:360px;display:flex;align-items:center;gap:20px','<svg viewBox="0 0 60 60" width="90" height="90"><path d="'+path+'" fill="#B84A2E" stroke="#0F0E0C" stroke-width="4" stroke-linejoin="round"/></svg><div class="mk-fr" style="font-size:50px">'+lab+'</div>',L.root);e.className='mk-a';L.on(function(t){var k=MK.pr(t,at,.3);e.style.opacity=k>0?1:0;e.style.transform='scale('+(.4+.6*MK.E.over(k))+')'});}
ic(420,'M14 6h32v48l-16-12-16 12z','SAVE',0,@S@);ic(580,'M6 30 L54 8 L40 54 L30 34Z','SHARE',0,@H@);ic(740,'M8 10h44v30H26l-12 12V40H8z','KOMENTAR',0,@K@);
L.on(function(t){var k=MK.E.out(MK.pr(t,0,.4));ph.style.opacity=k;ph.style.transform='rotate(-3deg) translateY('+((1-k)*200)+'px)';var b=MK.pr(t,@K@+.3,.3);bub.style.opacity=b;bub.style.transform='rotate(2deg) scale('+(.7+.3*MK.E.over(b))+')'});
""", S=wsv, H=wsh, K=wko) + sub(11), dolly=.05)
ev(11, 0, 'slide'); ev(11, wsv, 'pop'); ev(11, wsh, 'pop'); ev(11, wko, 'pop'); ev(11, wko + .3, 'tick')
# 12 gak gerak -> perbaiki konsep (lampu merah)
ws_, wpb = W(12, 'setahun', 1.8), W(12, 'perbaiki', 2.8)
scene(12, R("""var lp=MK.el('div','left:390px;top:300px;width:300px;height:300px','<svg viewBox="0 0 150 150" width="300" height="300"><rect x="35" y="5" width="80" height="140" rx="20" fill="#0F0E0C"/><circle id="l1" cx="75" cy="40" r="22" fill="#4a4540"/><circle cx="75" cy="75" r="22" fill="#4a4540"/><circle cx="75" cy="110" r="22" fill="#4a4540"/></svg>',L.root);lp.className='mk-a';
MK.PaperCard(L,{x:120,y:640,w:840,at:.1,from:'bottom',rot:-1,html:'<div class="mk-ou" style="font-size:50px">Tanda awal gak gerak?</div><div class="mk-ou" style="font-size:50px;margin-top:22px;color:#6B6560">Nunggu setahun</div>'});
MK.MarkerStrike(L,{x:160,y:780,w:380,h:60,at:@S@});
MK.StampBocor(L,{x:200,y:1040,at:@P@,rot:-5,size:76,text:'PERBAIKI KONSEP'});
L.on(function(t){var c=document.getElementById('l1');if(c)c.setAttribute('fill',(t>.3&&Math.floor(t*3)%2==0)?'#B84A2E':'#4a4540')});
@SUB@""", S=ws_, P=wpb, SUB=sub(12)), tr=True)
ev(12, .1, 'slide'); ev(12, ws_, 'scratch'); ev(12, wpb, 'stamp')
# 13 3 bulan: kolom cari + koin CAC
wn, wc, wtu = W(13, 'nyari', 2.4), W(13, 'cac', 6), W(13, 'turun', 6.6)
scene(13, chip('PATOK 2 · 3 BULAN') + TREEC(1) + R("""
var sb=MK.el('div','left:96px;top:340px;width:888px;height:110px;border-radius:60px;background:#FBF8F3;border:6px solid #0F0E0C;display:flex;align-items:center;gap:22px;padding:0 34px;box-sizing:border-box','<svg viewBox="0 0 50 50" width="56" height="56"><circle cx="21" cy="21" r="14" fill="none" stroke="#0F0E0C" stroke-width="6"/><path d="M32 32 L46 46" stroke="#0F0E0C" stroke-width="7" stroke-linecap="round"/></svg><div id="ty" class="mk-ou" style="font-size:48px"></div>',L.root);sb.className='mk-a';
MK.InkPath(L,{d:'M120 760 L300 720 L460 690 L620 610 L800 560 L960 470',w:9,at:@N@+.6,dur:1,color:'#B84A2E'});
var gl=MK.el('div','left:96px;top:480px;font-size:30px;color:#6B6560','pencarian nama brand',L.root);gl.className='mk-a mk-mono';
var cn=[];for(var i=0;i<5;i++){var c=MK.el('div','left:120px;top:'+(1120-i*40)+'px;width:180px;height:44px;border-radius:50%;background:#C8944A;border:5px solid #0F0E0C',' ',L.root);c.className='mk-a';cn.push(c)}
var cl=MK.el('div','left:340px;top:880px;font-size:56px','CAC',L.root);cl.className='mk-a mk-fr';
MK.CountUp(L,{x:340,y:950,from:85000,to:60000,at:@U@,dur:1.2,size:80,prefix:'Rp'});
var cs=MK.el('div','left:340px;top:1070px;font-size:32px;color:#6B6560','biaya dapat 1 pelanggan baru · contoh',L.root);cs.className='mk-a mk-ou';
L.on(function(t){var y=document.getElementById('ty');var txt='nama brand kamu';if(y)y.textContent=txt.slice(0,Math.max(0,Math.floor((t-@N@)*16)));sb.style.opacity=MK.pr(t,.05,.3);gl.style.opacity=MK.pr(t,@N@+.6,.3);
var a=MK.pr(t,@C@,.3);cl.style.opacity=cs.style.opacity=a;for(var i=0;i<5;i++){var on=a>0&&(i<3||t<@U@+.4);cn[i].style.opacity=on?1:(a>0?Math.max(0,1-(t-@U@-.4)*4):0);cn[i].style.transform='translateY('+(i>=3&&t>@U@+.4?-(t-@U@-.4)*200:0)+'px)'}});
""", N=wn, C=wc, U=wtu) + sub(13), tr=True, dolly=.04)
ev(13, wn, 'tick'); ev(13, wn + .6, 'draw'); ev(13, wc, 'pop'); ev(13, wtu + .4, 'slide')
# 14 1-2 tahun: repeat + label diskon menyusut
wb, wdk = W(14, 'balik', 1.9), W(14, 'diskon', 4.5)
scene(14, chip('PATOK 3 · 1–2 TAHUN') + TREEC(2) + R("""
var bg=MK.el('div','left:140px;top:360px;width:360px;height:360px','<svg viewBox="0 0 180 180" width="360" height="360"><g id="rot"><path d="M90 14 A76 76 0 1 1 20 60" fill="none" stroke="#B84A2E" stroke-width="10" stroke-linecap="round"/><path d="M8 40 L22 64 L44 48" fill="none" stroke="#B84A2E" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g><path d="M60 72 h60 l8 66 h-76z" fill="#C8944A" stroke="#0F0E0C" stroke-width="6" stroke-linejoin="round"/><path d="M74 72 q16 -30 32 0" fill="none" stroke="#0F0E0C" stroke-width="6"/></svg>',L.root);bg.className='mk-a';
var rl=MK.el('div','left:540px;top:430px;width:460px;font-size:64px;line-height:1','REPEAT<br>ORDER ↑',L.root);rl.className='mk-a mk-fr';
var tg=MK.el('div','left:200px;top:820px;width:560px;height:300px','<svg viewBox="0 0 280 150" width="560" height="300"><path d="M40 10 H260 V140 H40 L6 75Z" fill="#FBF8F3" stroke="#0F0E0C" stroke-width="7" stroke-linejoin="round"/><circle cx="38" cy="75" r="10" fill="#0F0E0C"/></svg><div id="dk" class="mk-fr" style="position:absolute;left:150px;top:80px;font-size:120px;color:#B84A2E"></div>',L.root);tg.className='mk-a';
var dl=MK.el('div','left:200px;top:1200px;font-size:34px;color:#6B6560','diskon yang dibutuhkan · contoh',L.root);dl.className='mk-a mk-ou';
L.on(function(t){var r=document.getElementById('rot');if(r)r.setAttribute('transform','rotate('+(t*120)+' 90 90)');var k=MK.pr(t,@B@-.3,.35);bg.style.opacity=k;bg.style.transform='scale('+(.5+.5*MK.E.over(k))+')';rl.style.opacity=MK.pr(t,@B@,.3);
var d=MK.pr(t,@D@-.6,.3);tg.style.opacity=dl.style.opacity=d;var v=Math.round(50-40*MK.E.io(MK.pr(t,@D@-.2,1.2)));var e=document.getElementById('dk');if(e)e.textContent=v+'%';var sc=.6+.4*(v/50);tg.style.transform='rotate(-4deg) scale('+(sc+.1)+')'});
""", B=wb, D=wdk) + sub(14), tr=True, dolly=.04)
ev(14, wb - .3, 'pop'); ev(14, wdk - .6, 'slide'); ev(14, wdk + .8, 'tick')
# 15 checklist angka awal
tk = [W(15, x, d) for x, d in (('catat', .5), ('semua', 1.1), ('angka', 1.6), ('sebelum', 2.2))]
scene(15, R("""var rows=['Reach & ThruPlay','Tag & komentar sebut brand','Pencarian nama brand','CAC'],h='<div class="mk-mono" style="font-size:26px;color:#6B6560;margin-bottom:12px">ANGKA SEBELUM CAMPAIGN JALAN</div>';
for(var i=0;i<4;i++)h+='<div style="display:flex;align-items:center;gap:22px;margin:16px 0"><div id="ck'+i+'" style="width:54px;height:54px;border:5px solid #0F0E0C;border-radius:10px;font:800 46px/44px Outfit;text-align:center;color:#B84A2E"></div><div class="mk-ou" style="font-size:44px">'+rows[i]+'</div></div>';
MK.PaperCard(L,{x:110,y:440,w:860,at:.05,from:'bottom',rot:-1,html:h});
var pn=MK.el('div','left:760px;top:330px;width:200px;height:200px','<svg viewBox="0 0 100 100" width="200" height="200"><path d="M20 86 L30 60 L76 14 L88 26 L42 72Z" fill="#C8944A" stroke="#0F0E0C" stroke-width="5" stroke-linejoin="round"/><path d="M20 86 L30 60 L42 72Z" fill="#0F0E0C"/></svg>',L.root);pn.className='mk-a';
var T=@T@;L.on(function(t){for(var i=0;i<4;i++){var e=document.getElementById('ck'+i);if(e)e.textContent=t>=T[i]?'✓':''}var n=0;for(var i=0;i<4;i++)if(t>=T[i])n=i;pn.style.transform='translate('+(-60+Math.sin(t*14)*6)+'px,'+(150+n*86)+'px)';pn.style.opacity=MK.pr(t,T[0]-.2,.2)});
@SUB@""", T=json.dumps(tk), SUB=sub(15)), paper='white', dolly=.05)
ev(15, .05, 'slide'); [ev(15, x, 'tick') for x in tk]
# 16 simpan
scene(16, """MK.SeriesCard(L,{series:'DAFTAR CEK CAMPAIGN BRAND',title:'Simpan<br>daftar cek.'});
var b=MK.el('div','left:96px;top:1180px;padding:20px 44px;border-radius:999px;background:#B84A2E;color:#FBF8F3;font-size:44px','Simpan',L.root);b.className='mk-a mk-ou';
L.on(function(t){var k=MK.pr(t,.8,.3);b.style.opacity=k;b.style.transform='scale('+(.8+.2*MK.E.over(k))+')'});""", tr=True)
ev(16, .8, 'chime')
html = ('<!DOCTYPE html>\n<html><head><meta charset="utf-8"><title>Metrik campaign brand</title><link rel="stylesheet" href="motionkit/fonts-mk.css"></head><body>\n'
        '<script src="motionkit/kit.js"></script>\n<script>\nvar C=MK.C;\n' + HELP + '\nMK.run([\n' + ',\n'.join(S) + '\n]);\n</script>\n</body></html>\n')
open(A + 'mk-metrik.html', 'w', encoding='utf-8').write(html)
json.dump({'duration': tl['duration'], 'events': EV, 'cuts': T0}, open(os.path.join(OUT, 'events.json'), 'w'))
print('ok', len(S), 'adegan', round(sum(DUR), 1), 'dtk'); print([(SC[i][0], DUR[i]) for i in range(len(SC))])
