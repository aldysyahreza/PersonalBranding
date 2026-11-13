import json, sys, re
sys.path.insert(0, '/home/user/content-studio/scratch')
from intro_scene import INTRO_HTML
A = '/home/user/content-studio/animatic/'
TIMING = sys.argv[1]
M = open('/home/user/content-studio/scratch/gen_meja.py', encoding='utf-8').read()
O = open('/home/user/content-studio/scratch/gen_owner.py', encoding='utf-8').read()
v3 = open(A + 'animatic-v3.html', encoding='utf-8').read()
head = v3[:v3.index('<div class="bgpaper" id="bgp"></div>')].replace('<title>Animatic v3 The Brand Fixer</title>', '<title>Animatic: kerja pada bisnis</title>')
tail = v3[v3.index('<div id="scan">'):v3.index('<script>')]
eng = M[M.index("JS = r'''") + len("JS = r'''"):M.index("/* ---------- bangun objek ---------- */")]
cap = M[M.index("var CAP=BEATS.map"):M.index("/* ---------- adegan ---------- */")]
fin = M[M.index("var TR=["):M.index("'''.replace('__DEF__'")]
fin = fin[fin.index("function apply"):]
exec(O[O.index("def person("):O.index("def card(")])

# (kata pembuka, babak, nomor babak, lewati n kemunculan)
SC = [("kamu","HOOK",1,0),("justru","HOOK",1,0),("kenalin","HOOK",1,0),
 ("pagi","RELATE",2,0),("malam","RELATE",2,0),
 ("michael","INSIGHT",3,0),("kerja","INSIGHT",3,1),("dan","INSIGHT",3,0),("kalo","INSIGHT",3,0),
 ("jadi","REFRAME",4,0),("di","REFRAME",4,1),("pilih","REFRAME",4,0),("tulis","REFRAME",4,0),
 ("simpan","CTA",5,0)]
nrm = lambda s: ''.join(c for c in s.lower() if c.isalnum())
tl = json.load(open(TIMING, encoding='utf-8'))
words, beat_of = [], []
for bi, b in enumerate(tl['beats']):
    for w in b['words']: words.append(w); beat_of.append(bi)
starts, k = [], 0
for st, ac, ch, skip in SC:
    n = skip
    while True:
        while k < len(words) and not (beat_of[k] == ch - 1 and nrm(words[k]['w']).startswith(st)): k += 1
        if k >= len(words): raise SystemExit('kata pembuka tidak ditemukan: ' + st)
        if n == 0: break
        n -= 1; k += 1
    starts.append(k); k += 1
t0s = [0.0 if i == 0 else max(0.0, words[a]['t'] - 0.2) for i, a in enumerate(starts)]
DUR = []; WT = []
for i, a in enumerate(starts):
    b = starts[i + 1] if i + 1 < len(starts) else len(words)
    end = t0s[i + 1] if i + 1 < len(starts) else tl['duration']
    DUR.append(round(end - t0s[i], 3))
    d = {}
    for w in words[a:b]:
        key = nrm(w['w'])
        if key and key not in d: d[key] = round(w['t'] - t0s[i], 3)
    WT.append(d)
SAY = [' '.join(w['w'] for w in words[a:(starts[i + 1] if i + 1 < len(starts) else len(words))]) for i, a in enumerate(starts)]
DEF = ',\n  '.join("{dur:%s,name:'%s',chap:%d,say:%s}" % (DUR[i], SC[i][1], SC[i][2], json.dumps(SAY[i], ensure_ascii=False)) for i in range(len(SC)))

def src(txt): return '<div class="mono" style="position:absolute;left:96px;right:96px;top:1265px;font-size:19px;letter-spacing:.04em;color:#6B6560;text-transform:none;line-height:1.3">%s</div>' % txt
def fig(id_, u, x, y, w_, h_, shirt='#B84A2E', dark='#8f3a24', flip=False):
    return '<div class="a" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">%s</div>' % (id_, x, y, w_, h_, person(u, shirt, dark, '#2a1d14', flip))
def chipb(id_, x, y, txt, bg='#0F0E0C', col='#fff', fs=34):
    return '<div class="a" id="%s" style="left:%dpx;top:%dpx;padding:16px 28px;border-radius:999px;background:%s;color:%s;font:800 %dpx/1 var(--f-display);white-space:nowrap">%s</div>' % (id_, x, y, bg, col, fs, txt)

S = []
# 1 kerja paling keras: owner + tumpukan tugas
S.append(('<section class="sc" id="b1">' + fig('a1p', 'p1', 90, 470, 330, 620)
 + '<div class="a" id="a1d" style="left:60px;top:1010px;width:960px;height:34px;border-radius:10px;background:#0F0E0C"></div>'
 + ''.join(chipb('a1t%d' % i, x, y, t, bg, col, 32) for i, (x, y, t, bg, col) in enumerate([(470, 470, 'chat pelanggan', '#fff', '#0F0E0C'), (560, 580, 'cek stok', '#C8944A', '#0F0E0C'), (480, 690, 'approve desain', '#fff', '#0F0E0C'), (600, 800, 'transfer', '#B84A2E', '#fff'), (500, 910, 'meeting', '#0F0E0C', '#fff')]))
 + '<div class="a disp" id="a1h" style="left:84px;top:1090px;font-size:96px;line-height:1">PALING <span style="color:#B84A2E">KERAS</span></div></section>',
 "function(t){op($('a1p'),pr(t,.05,.3));op($('a1d'),pr(t,.05,.3));BOB('p1',t,4);ARM('p1','ra',-60+Math.sin(t*9)*14);ARM('p1','la',50+Math.sin(t*8+1)*12);HEAD('p1',Math.sin(t*4)*5);for(var i=0;i<5;i++)pop($('a1t'+i),t,.4+i*.32,.35);up($('a1h'),t,w(0,'paling',1.2),.4,40)}"))
# 2 justru itu masalahnya: stempel
S.append(('<section class="sc" id="b2">' + fig('b2p', 'p2', 110, 470, 300, 560)
 + '<div class="a disp" id="b2s" style="left:380px;top:640px;font-size:96px;color:#B84A2E;transform:rotate(-8deg);border:12px solid #B84A2E;border-radius:26px;padding:8px 30px;line-height:1">MASALAH</div>'
 + '<div class="a hand" id="b2h" style="left:0;right:0;top:1090px;text-align:center;font-size:100px">justru itu</div></section>',
 "function(t){op($('b2p'),pr(t,.05,.3));BOB('p2',t,2);HEAD('p2',-6);up($('b2h'),t,.1,.4,30);pop($('b2s'),t,w(1,'masalahnya',.7)-.1,.4,' rotate(-8deg)')}"))
# 3 perkenalan
S.append((INTRO_HTML('in').replace('id="inx"', 'id="b3"'),
 "function(t){var P='in';pop($(P+'ph'),t,w(2,'saya',.6)-.4,.5,' rotate(-2deg)');up($(P+'nm'),t,w(2,'aldy',1),.4,40);up($(P+'rl'),t,w(2,'syahreza',1.6),.3,16);pop($(P+'1'),t,w(2,'belasan',2.3),.4);pop($(P+'2'),t,w(2,'brand',3.6),.4);pop($(P+'3'),t,w(2,'lintas',4.2),.4)}"))
# 4 pagi siang sore
rows = [('PAGI', 'bales chat pelanggan', '#FFE2B0'), ('SIANG', 'cek stok', '#C8944A'), ('SORE', 'approve desain konten', '#B84A2E')]
S.append(('<section class="sc" id="b4"><div class="a" id="c4l" style="left:150px;top:440px;width:10px;height:700px;background:#0F0E0C;border-radius:5px;transform-origin:top"></div>'
 + ''.join('<div class="a" id="c4r%d" style="left:120px;top:%dpx;width:880px;height:170px"><div style="position:absolute;left:0;top:50px;width:70px;height:70px;border-radius:50%%;background:%s;border:8px solid #0F0E0C"></div><div class="mono" style="position:absolute;left:110px;top:20px;font-size:30px;color:var(--gray)">%s</div><div style="position:absolute;left:110px;top:66px;width:760px;padding:22px 30px;border-radius:24px;background:#fff;box-shadow:var(--sh);font:800 44px/1 var(--f-display)">%s</div></div>' % (i, 460 + i * 230, c, a, b) for i, (a, b, c) in enumerate(rows))
 + '</section>',
 "function(t){var k=E.io(pr(t,.05,1.2));tf($('c4l'),'scaleY('+k+')');var a=['pagi','siang','sore'];for(var i=0;i<3;i++)up($('c4r'+i),t,w(3,a[i],.3+i*1.5)-.15,.35,30)}"))
# 5 malam, capek
S.append(('<section class="sc" id="b5"><div class="a" id="d5bg" style="left:84px;top:420px;width:912px;height:800px;border-radius:40px;background:#0F0E0C"></div>'
 '<svg class="a" id="d5m" viewBox="0 0 100 100" style="left:760px;top:470px;width:160px;height:160px"><path d="M70 10 A42 42 0 1 0 90 70 A34 34 0 1 1 70 10Z" fill="#FFE2B0"/></svg>'
 + fig('d5p', 'p5', 160, 560, 300, 560, '#6B6560', '#4a4540')
 + '<div class="a" id="d5bt" style="left:560px;top:760px;width:300px;height:130px;border:10px solid #fff;border-radius:22px"><div id="d5bl" style="position:absolute;left:10px;top:10px;bottom:10px;width:250px;border-radius:8px;background:#B84A2E;transform-origin:left"></div></div><div class="a" style="left:870px;top:800px;width:20px;height:50px;border-radius:0 8px 8px 0;background:#fff" id="d5bc"></div>'
 '<div class="a hand" id="d5h" style="left:540px;top:930px;width:440px;font-size:76px;color:#fff;line-height:1.05">baru sempat mikir, udah capek</div></section>',
 "function(t){op($('d5bg'),pr(t,.05,.3));pop($('d5m'),t,.2,.4);op($('d5p'),pr(t,.1,.3));BOB('p5',t,1.5);var c=pr(t,w(4,'capek',2.5)-.6,.8);HEAD('p5',8+18*c);ARM('p5','ra',10);ARM('p5','la',-10);op($('d5bt'),pr(t,.3,.3));op($('d5bc'),pr(t,.3,.3));tf($('d5bl'),'scaleX('+(1-.88*E.io(pr(t,.5,w(4,'capek',2.5))))+')');up($('d5h'),t,w(4,'mikir',1.2),.4,30)}"))
# 6 Michael Gerber, buku, dua jenis kerja
S.append(('<section class="sc" id="b6"><div class="a" id="e6b" data-obj style="left:110px;top:440px;width:380px;height:540px;border-radius:12px 26px 26px 12px;background:#B84A2E;box-shadow:var(--sh);transform:rotate(-4deg)"><div style="position:absolute;left:0;top:0;bottom:0;width:30px;background:rgba(15,14,12,.25);border-radius:12px 0 0 12px"></div><div class="disp" style="position:absolute;left:60px;top:70px;font-size:66px;line-height:.95;color:#fff">THE<br>E-MYTH</div><div class="mono" style="position:absolute;left:60px;bottom:50px;font-size:22px;color:#FFE2B0">Michael E. Gerber</div></div>'
 '<div class="a mono" id="e6n" style="left:560px;top:470px;font-size:26px;color:var(--gray)">penulis bisnis kecil, AS</div><div class="a disp" id="e6g" style="left:560px;top:515px;width:440px;font-size:70px;line-height:.95">MICHAEL GERBER</div>'
 '<div class="a disp" id="e6d" style="left:560px;top:700px;font-size:250px;line-height:1;color:#B84A2E">2</div><div class="a hand" id="e6h" style="left:700px;top:790px;width:300px;font-size:72px;line-height:1">jenis kerja</div>'
 + src('Michael E. Gerber, The E-Myth Revisited (1995). Sampul digambar ulang, bukan foto sampul asli.') + '</section>',
 "function(t){pop($('e6b'),t,.1,.5,' rotate(-4deg)');up($('e6n'),t,.3,.3,16);up($('e6g'),t,w(5,'gerber',.6),.4,30);pop($('e6d'),t,w(5,'dua',2.4)-.1,.45);up($('e6h'),t,w(5,'jenis',2.7),.4,24)}"))
# 7 kerja DI DALAM bisnis
def house(p, x, y):
    return ('<div class="a" id="%sH" data-obj style="left:%dpx;top:%dpx;width:520px;height:520px"><svg viewBox="0 0 520 520" width="520" height="520"><path d="M30 200 L260 30 L490 200 L490 500 L30 500Z" fill="#fff" stroke="#0F0E0C" stroke-width="14" stroke-linejoin="round"/></svg>'
            '<div class="mono" style="position:absolute;left:0;right:0;top:150px;text-align:center;font-size:28px;color:var(--gray)">BISNIS</div></div>') % (p, x, y)
S.append(('<section class="sc" id="b7">' + house('f7', 280, 430) + fig('f7p', 'p7', 450, 640, 180, 330)
 + ''.join(chipb('f7t%d' % i, x, y, t, '#F2EDE3', '#0F0E0C', 28) for i, (x, y, t) in enumerate([(330, 640, 'chat'), (640, 700, 'stok'), (330, 830, 'desain')]))
 + chipb('f7l', 84, 1010, 'DI DALAM BISNIS', '#0F0E0C', '#fff', 52)
 + '<div class="a hand" id="f7h" style="left:84px;top:1110px;font-size:76px">ngerjain tugas harian</div></section>',
 "function(t){pop($('f7H'),t,.05,.45);op($('f7p'),pr(t,.2,.3));BOB('p7',t,3);ARM('p7','ra',-70+Math.sin(t*10)*16);ARM('p7','la',70-Math.sin(t*9)*16);for(var i=0;i<3;i++)pop($('f7t'+i),t,w(6,'ngerjain',1.4)-.2+i*.2,.3);up($('f7l'),t,w(6,'dalam',.5),.4,30);up($('f7h'),t,w(6,'tugas',1.8),.4,24)}"))
# 8 kerja PADA bisnis
S.append(('<section class="sc" id="b8">' + house('g8', 460, 430)
 + '<svg class="a" id="g8g" viewBox="0 0 100 100" style="left:640px;top:660px;width:170px;height:170px"><g id="g8gr"><circle cx="50" cy="50" r="30" fill="none" stroke="#C8944A" stroke-width="14"/><g stroke="#C8944A" stroke-width="12" stroke-linecap="round"><path d="M50 6 V18"/><path d="M50 82 V94"/><path d="M6 50 H18"/><path d="M82 50 H94"/><path d="M19 19 L27 27"/><path d="M73 73 L81 81"/><path d="M81 19 L73 27"/><path d="M27 73 L19 81"/></g></g></svg>'
 + fig('g8p', 'p8', 70, 560, 260, 480)
 + '<svg class="a" viewBox="0 0 300 200" style="left:250px;top:760px;width:260px;height:180px" fill="none" stroke="#B84A2E" stroke-width="7" stroke-linecap="round"><path id="g8l" d="M10 150 L80 150 L80 80 L170 80 L170 30 L280 30"/></svg>'
 + chipb('g8c', 84, 1010, 'PADA BISNIS', '#B84A2E', '#fff', 52)
 + '<div class="a hand" id="g8h" style="left:84px;top:1110px;width:920px;font-size:70px;line-height:1.05">bikin cara kerja, jalan tanpa kamu</div></section>',
 "function(t){pop($('g8H'),t,.05,.45);op($('g8p'),pr(t,.1,.3));BOB('p8',t,2);ARM('p8','ra',-100+Math.sin(t*4)*10);HEAD('p8',4);up($('g8c'),t,w(7,'pada',.6),.4,30);draw($('g8l'),t,w(7,'membangun',1.4),1.2);pop($('g8g'),t,w(7,'cara',2),.4);var r=t>w(7,'jalan',4.2)?(t-w(7,'jalan',4.2))*120:0;$('g8gr').setAttribute('transform','rotate('+r.toFixed(1)+' 50 50)');up($('g8h'),t,w(7,'supaya',3.4),.4,24)}"))
# 9 bisnis sebesar tenaga
S.append(('<section class="sc" id="b9">' + fig('h9p', 'p9', 380, 640, 300, 560)
 + '<div class="a" id="h9b" data-obj style="left:330px;top:420px;width:400px;height:250px;border-radius:24px;background:#fff;box-shadow:var(--sh);display:flex;align-items:center;justify-content:center;font:800 64px/1 var(--f-display)">BISNIS</div>'
 + '<div class="a hand" id="h9e" style="left:760px;top:520px;width:260px;font-size:56px;line-height:1;color:#B84A2E">sebesar tenagamu</div>'
 + '<div class="a hand" id="h9h" style="left:84px;top:520px;width:240px;font-size:56px;line-height:1">owner terus di dalam</div></section>',
 "function(t){op($('h9p'),pr(t,.05,.3));var s=Math.sin(t*7)*3;BOB('p9',t,2);ARM('p9','ra',-160+s);ARM('p9','la',160-s);HEAD('p9',0);pop($('h9b'),t,.25,.45);var sh=pr(t,w(8,'sebesar',2.2)-.2,.6);tf($('h9b'),'translateX('+(Math.sin(t*20)*4*sh)+'px)');up($('h9h'),t,w(8,'owner',.4),.4,24);up($('h9e'),t,w(8,'sebesar',2.2),.4,24)}"))
# 10 kalender: blok 2 jam, hari dan jam sama tiap minggu
days = ['SEN', 'SEL', 'RAB', 'KAM', 'JUM', 'SAB', 'MIN']
cal = '<div class="a card" data-obj id="i10c" style="left:84px;top:430px;width:912px;height:660px">'
cal += ''.join('<div class="mono" style="position:absolute;left:%dpx;top:40px;width:110px;text-align:center;font-size:24px;color:var(--gray)">%s</div>' % (44 + i * 120, d) for i, d in enumerate(days))
cal += ''.join('<div style="position:absolute;left:%dpx;top:%dpx;width:108px;height:120px;border-radius:14px;background:#F2EDE3"></div>' % (44 + c * 120, 90 + r * 135) for r in range(4) for c in range(7))
cal += ''.join('<div class="a" id="i10k%d" style="left:164px;top:%dpx;width:108px;height:120px;border-radius:14px;background:#C8944A;border:6px solid #0F0E0C;display:flex;align-items:center;justify-content:center;font:800 34px/1 var(--f-display)">2 JAM</div>' % (r, 90 + r * 135) for r in range(4))
cal += '</div>'
S.append(('<section class="sc" id="b10">' + cal + '<div class="a hand" id="i10h" style="left:84px;top:1120px;width:920px;font-size:76px">hari &amp; jam sama, tiap minggu</div></section>',
 "function(t){var c=$('i10c');op(c,pr(t,.05,.3));tf(c,'translateY('+((1-E.out(pr(t,.05,.4)))*50)+'px)');pop($('i10k0'),t,w(9,'blok',2)-.1,.4);for(var r=1;r<4;r++)pop($('i10k'+r),t,w(9,'tiap',w(9,'sama',5))-.2+r*.22,.35);up($('i10h'),t,w(9,'hari',4.2),.4,24)}"))
# 11 di dua jam itu: tugas harian dicoret
tasks = ['bales chat', 'cek stok', 'approve desain']
S.append(('<section class="sc" id="b11"><div class="a card" data-obj id="j11c" style="left:84px;top:430px;width:912px;height:640px;background:#C8944A"><div class="disp" style="position:absolute;left:44px;top:40px;font-size:56px">2 JAM INI</div><div class="mono" style="position:absolute;left:44px;top:110px;font-size:24px">dilarang:</div>'
 + ''.join('<div class="a" id="j11t%d" style="left:44px;top:%dpx;width:824px;height:110px;border-radius:22px;background:#fff;display:flex;align-items:center;padding-left:36px;font:800 50px/1 var(--f-display)">%s</div><svg class="a" viewBox="0 0 824 110" style="left:44px;top:%dpx;width:824px;height:110px"><path id="j11x%d" d="M20 60 L800 50" stroke="#B84A2E" stroke-width="12" stroke-linecap="round" fill="none"/></svg>' % (i, 170 + i * 140, t, 170 + i * 140, i) for i, t in enumerate(tasks))
 + '</div><div class="a hand" id="j11h" style="left:84px;top:1110px;font-size:80px">gak boleh tugas harian</div></section>',
 "function(t){pop($('j11c'),t,.05,.45);for(var i=0;i<3;i++){up($('j11t'+i),t,.4+i*.2,.3,20);draw($('j11x'+i),t,w(10,'boleh',1.8)+i*.25,.35)}up($('j11h'),t,w(10,'tugas',2.4),.4,24)}"))
# 12 pilih satu pekerjaan paling sering diulang
reps = [('bales chat', 42), ('cek stok', 18), ('approve desain', 9)]
S.append(('<section class="sc" id="b12"><div class="a mono" id="k12l" style="left:84px;top:430px;font-size:26px;color:var(--gray)">diulang per minggu (contoh)</div>'
 + ''.join('<div class="a" id="k12r%d" style="left:84px;top:%dpx;width:912px;height:150px"><div style="position:absolute;left:0;top:0;width:912px;height:150px;border-radius:26px;background:#fff;box-shadow:var(--sh)"></div><div style="position:absolute;left:40px;top:48px;font:800 52px/1 var(--f-display)">%s</div><div style="position:absolute;right:40px;top:40px;font:800 66px/1 var(--f-display);color:%s">%dx</div></div>' % (i, 490 + i * 190, a, '#B84A2E' if i == 0 else '#6B6560', n) for i, (a, n) in enumerate(reps))
 + '<svg class="a" viewBox="0 0 960 200" style="left:60px;top:460px;width:960px;height:200px" fill="none"><path id="k12o" d="M120 30 C40 40 10 150 160 175 C420 205 900 190 930 110 C955 40 700 18 300 22" stroke="#B84A2E" stroke-width="9" stroke-linecap="round"/></svg>'
 + '<div class="a hand" id="k12h" style="left:84px;top:1080px;font-size:80px">pilih yang paling sering</div></section>',
 "function(t){up($('k12l'),t,.05,.3,16);for(var i=0;i<3;i++)up($('k12r'+i),t,.2+i*.2,.35,30);draw($('k12o'),t,w(11,'paling',1.6),.6);up($('k12h'),t,w(11,'sering',2),.4,24)}"))
# 13 tulis caranya -> tim ambil alih
S.append(('<section class="sc" id="b13"><div class="a card" data-obj id="l13n" style="left:84px;top:430px;width:560px;height:620px"><div class="disp" style="position:absolute;left:40px;top:40px;font-size:44px;line-height:1">CARA BALES<br>CHAT</div>'
 + ''.join('<div style="position:absolute;left:40px;top:%dpx;width:46px;height:46px;border-radius:50%%;background:#0F0E0C;color:#fff;display:flex;align-items:center;justify-content:center;font:800 26px/1 var(--f-display)">%d</div><div class="a" id="l13s%d" style="left:104px;top:%dpx;width:%dpx;height:16px;border-radius:8px;background:#C8944A;transform-origin:left"></div>' % (170 + i * 95, i + 1, i, 185 + i * 95, [380, 320, 400, 280][i]) for i in range(4))
 + '</div>' + fig('l13p', 'p13', 700, 600, 260, 480, '#0F0E0C', '#2a2622', True)
 + chipb('l13t', 720, 1060, 'TIM', '#C8944A', '#0F0E0C', 40)
 + '<div class="a hand" id="l13h" style="left:84px;top:1100px;width:620px;font-size:72px;line-height:1">tim ambil alih</div></section>',
 "function(t){var n=$('l13n');op(n,pr(t,.05,.3));for(var i=0;i<4;i++){var k=E.io(pr(t,w(12,'caranya',.5)+i*.35,.4));tf($('l13s'+i),'scaleX('+k+')');op($('l13s'+i),k>0?1:0)}var g=E.io(pr(t,w(12,'ambil',2.2)-.5,.7));tf(n,'translateX('+(g*120)+'px) rotate('+(g*4)+'deg) scale('+(1-g*.25)+')');op($('l13p'),pr(t,.2,.3));BOB('p13',t,2);ARM('p13','ra',-60*g);pop($('l13t'),t,w(12,'tim',1.6),.35);up($('l13h'),t,w(12,'biar',1.3),.4,24)}"))
# 14 CTA simpan
S.append(('<section class="sc" id="b14"><div class="a" style="left:0;top:0;width:1080px;height:1920px;background:var(--terra)"></div>'
 '<div class="a" id="m14s" data-obj style="left:440px;top:330px;width:200px;height:200px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 14px 0 rgba(15,14,12,.35)"><svg viewBox="0 0 24 24" width="92" height="92" fill="none" stroke="#B84A2E" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"><path d="M6 3h12v18l-6-4-6 4z"/></svg></div>'
 '<div class="a disp" id="m14h1" style="left:0;right:0;top:570px;text-align:center;font-size:130px;color:#fff;line-height:1">SIMPAN</div><div class="a disp" id="m14h2" style="left:0;right:0;top:705px;text-align:center;font-size:110px;color:#0F0E0C;line-height:1">VIDEO INI</div>'
 '<div class="a" id="m14sub" style="left:96px;right:96px;top:870px;text-align:center;font:700 42px/1.25 var(--f-body);color:#fff">Buka lagi pas gak punya waktu buat mikir.</div>'
 '<div class="a" id="m14p" style="left:96px;top:1010px;width:888px;height:110px;border-radius:999px;background:#fff;display:flex;align-items:center;justify-content:center;font:800 46px/1 var(--f-display);color:#0F0E0C">Blok 2 jam · tulis 1 cara kerja</div>'
 '<div class="a mono" id="m14a" style="left:0;right:0;top:1170px;text-align:center;font-size:34px;color:#fff;letter-spacing:.06em">@aldysyahreza</div></section>',
 "function(t){pop($('m14s'),t,.05,.45);up($('m14h1'),t,.2,.35,40);up($('m14h2'),t,.35,.35,40);up($('m14sub'),t,w(13,'buka',1.6),.35,30);up($('m14p'),t,w(13,'buka',1.6)+.6,.35,30);op($('m14a'),pr(t,w(13,'buka',1.6)+1.2,.4))}"))

assert len(S) == len(SC)
fin = re.sub(r'cur===\d+', 'cur===%d' % (len(S) - 1), fin)
BODY = '<div class="bgpaper" id="bgp"></div><div class="bgdx" id="bgd"></div>\n' + '\n'.join(h for h, j in S)
helpers = r"""
function RT(id,a,cx,cy){var e=$(id);if(e)e.setAttribute('transform','rotate('+a.toFixed(2)+' '+cx+' '+cy+')')}
function BOB(u,t,amp){var e=$(u+'_b');if(e)e.setAttribute('transform','translate(0,'+(Math.sin(t*3.2)*amp).toFixed(2)+')')}
function ARM(u,side,a){RT(u+'_'+side,a,side==='la'?73:127,134)}
function HEAD(u,a){RT(u+'_h',a,100,104)}
"""
TRS = ['zoom','drop','whip','drop','whip','drop','whip','drop','whip','drop','whip','drop','drop']
JS = (eng + "\nvar WT=" + json.dumps(WT) + ";\nfunction w(i,k,d){var v=WT[i]&&WT[i][k];return v==null?d:v}\n" + helpers + cap +
      "\nvar DI=99,SCAN_A=0,SCAN_B=0;\nvar S=[\n " + ',\n '.join(j for h, j in S) + "];\n"
      "var TR=[" + ','.join(["null"] + ["'%s'" % x for x in TRS[:len(S) - 1]]) + "];var TD=.42;\n" + fin)
JS = JS.replace('__DEF__', DEF)
open(A + 'animatic-kerja.html', 'w', encoding='utf-8').write(head + BODY + tail + JS)
anch = {"_petunjuk": "Adegan dimulai pada kata pembukanya.", "scenes": [{"start": a, "act": b, "chap": c, "skip": s} for a, b, c, s in SC], "beats": [[] for _ in SC]}
json.dump(anch, open(A + 'anchors-kerja.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', len(S), 'adegan; total', round(sum(DUR), 1), 's')
print([(SC[i][0], DUR[i]) for i in range(len(SC))])
