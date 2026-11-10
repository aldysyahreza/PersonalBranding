import json, sys, re
sys.path.insert(0, '/home/user/content-studio/scratch')
from intro_scene import INTRO_HTML
A = '/home/user/content-studio/animatic/'
TIMING = sys.argv[1] if len(sys.argv) > 1 else '/home/user/content-studio/out/reel11/timing.json'
M = open('/home/user/content-studio/scratch/gen_meja.py', encoding='utf-8').read()
O = open('/home/user/content-studio/scratch/gen_owner.py', encoding='utf-8').read()
v3 = open(A + 'animatic-v3.html', encoding='utf-8').read()
head = v3[:v3.index('<div class="bgpaper" id="bgp"></div>')].replace('<title>Animatic v3 The Brand Fixer</title>', '<title>Animatic: Reddit anjlok, brand dan AI</title>')
tail = v3[v3.index('<div id="scan">'):v3.index('<script>')]
eng = M[M.index("JS = r'''") + len("JS = r'''"):M.index("/* ---------- bangun objek ---------- */")]
cap = M[M.index("var CAP=BEATS.map"):M.index("/* ---------- adegan ---------- */")]
fin = M[M.index("var TR=["):M.index("'''.replace('__DEF__'")]
fin = fin[fin.index("function apply"):].replace('cur===14', 'cur===21')
# fungsi person() dari generator owner
person_src = O[O.index("def person("):O.index("def card(")]
exec(person_src)

# ---------- spesifikasi adegan: (kata pembuka, nama babak, nomor babak) ----------
SC = [("saham","HOOK",1),("menunjuk","HOOK",1),("sebelumnya","HOOK",1),
 ("nah","RELATE",2),("dulu","RELATE",2),("sekarang","RELATE",2),("orang","RELATE",2),
 ("akhir","INSIGHT",3),("sahamnya","INSIGHT",3),("ceo","INSIGHT",3),("itu","INSIGHT",3),("tapi","INSIGHT",3),("tahan","INSIGHT",3),
 ("terus","REFRAME",4),("dia","REFRAME",4),("tujuannya","REFRAME",4),("dan","REFRAME",4),("jadi","REFRAME",4),("satu","REFRAME",4),("dua","REFRAME",4),("tiga","REFRAME",4),
 ("gak","CTA",5)]
nrm = lambda s: ''.join(c for c in s.lower() if c.isalnum())
tl = json.load(open(TIMING, encoding='utf-8'))
words, beat_of = [], []
for bi, b in enumerate(tl['beats']):
    for w in b['words']: words.append(w); beat_of.append(bi)
starts, k = [], 0
for st, ac, ch in SC:
    while k < len(words) and not (beat_of[k] == ch - 1 and nrm(words[k]['w']).startswith(st)): k += 1
    if k >= len(words): raise SystemExit('kata pembuka tidak ditemukan: ' + st)
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
IL = '<span class="chip a" id="%s" style="left:84px;top:%dpx;background:var(--amber);color:var(--ink)">%s</span>'
def serp(p, ai):
    rows = ''.join('<div class="a" id="%sr%d" style="left:44px;top:%dpx;width:824px;height:90px;border-radius:18px;background:%s;padding:16px 26px;font:700 30px/1.15 var(--f-body);color:#0F0E0C"><div style="height:12px;width:%s;background:%s;border-radius:6px"></div><div style="margin-top:12px;height:10px;width:%s;background:#E0D8CA;border-radius:5px"></div></div>' % (p, i, 250 + i * 104 + (170 if ai else 0), '#FFF1E4' if i == 1 else '#F2EDE3', ['62%', '48%', '70%', '55%'][i], '#B84A2E' if i == 1 else '#bdb5a8', ['85%', '75%', '90%', '66%'][i]) for i in range(4))
    chip = '<span class="chip a" id="%schip" style="left:560px;top:%dpx;background:#B84A2E;color:#fff;font-size:22px">forum Reddit</span>' % (p, 258 + 104 + (170 if ai else 0))
    aicard = ('<div class="a" id="%sai" style="left:44px;top:236px;width:824px;height:150px;border-radius:22px;background:#0F0E0C;color:#fff;padding:20px 28px"><div class="mono" style="font-size:20px;color:#FFE2B0">jawaban ringkas</div><div style="margin-top:12px;height:12px;width:90%%;background:#4a443c;border-radius:6px"></div><div style="margin-top:10px;height:12px;width:80%%;background:#4a443c;border-radius:6px"></div><div style="margin-top:10px;height:12px;width:60%%;background:#4a443c;border-radius:6px"></div></div>' % p) if ai else ''
    return ('<div class="a card" data-obj id="%sc" style="left:84px;top:410px;width:912px;height:700px"><div class="a" style="left:44px;top:44px;width:824px;height:76px;border-radius:38px;background:#F2EDE3;padding:0 32px;display:flex;align-items:center;font:700 30px/1 var(--f-body);color:#6B6560" id="%sq">sepatu kerja yang nyaman</div>%s%s%s'
            '<svg class="a" id="%scur" viewBox="0 0 40 40" style="left:600px;top:700px;width:70px;height:70px" fill="#0F0E0C" stroke="#fff" stroke-width="2"><path d="M6 4 L6 30 L13 24 L18 35 L23 33 L18 22 L28 22Z"/></svg></div>') % (p, p, aicard, rows, chip, p)

S = []   # (html, js)
# 1 hook
S.append(('<section class="sc" id="b1"><span class="chip a" id="a1c" style="left:84px;top:410px;background:var(--ink);color:#fff">REDDIT · RDDT · 30 OKT 2026</span>'
 '<svg class="a" viewBox="0 0 912 440" style="left:84px;top:470px;width:912px;height:440px" fill="none" stroke-linecap="round" stroke-linejoin="round"><path id="a1l" d="M10 70 L150 90 L290 50 L420 110 L520 150 L600 330 L680 410 L890 425" stroke="#B84A2E" stroke-width="14"/><path id="a1f" d="M10 70 L150 90 L290 50 L420 110 L520 150 L600 330 L680 410 L890 425 L890 440 L10 440Z" fill="rgba(184,74,46,.12)" stroke="none"/></svg>'
 '<div class="a disp" id="a1n" style="left:84px;top:930px;font-size:230px;color:#B84A2E;line-height:1">−29%</div><div class="a" id="a1s" style="left:92px;top:1170px;font:800 54px/1 var(--f-display)">dalam sehari</div>'
 + src('Sumber: TheStreet, Yahoo Finance (30 Okt 2026). Besar penurunan berbeda antar media: 23-36%.') + '</section>',
 "function(t){up($('a1c'),t,.15,.3,16);draw($('a1l'),t,w(0,'anjlok',.9)-.3,1.3);op($('a1f'),pr(t,w(0,'anjlok',.9)+.8,.5));pop($('a1n'),t,w(0,'29',1.8),.45);up($('a1s'),t,w(0,'sehari',3),.3,20)}"))
# 2 menunjuk
S.append(('<section class="sc" id="b2"><svg class="a" viewBox="0 0 300 520" id="a2p" style="left:90px;top:440px;width:330px;height:572px" fill="none" stroke="#0F0E0C" stroke-width="9" stroke-linejoin="round" stroke-linecap="round"><rect x="40" y="20" width="220" height="440" rx="34" fill="#fff"/><rect x="62" y="60" width="176" height="14" rx="7" fill="#E0D8CA" stroke="none"/><rect x="62" y="96" width="176" height="90" rx="12" fill="#F2EDE3" stroke="none"/><rect x="62" y="204" width="176" height="90" rx="12" fill="#F2EDE3" stroke="none"/><g id="a2t"><path d="M230 330 C230 300 262 296 262 330 L262 420 C262 470 190 480 170 440 L130 380" fill="#F1C9A3"/></g></svg>'
 '<div class="a disp" id="a2h" style="left:450px;top:560px;width:540px;font-size:92px;line-height:.95">satu<br><span style="color:#B84A2E">kebiasaan</span><br>kita</div><div class="a hand" id="a2q" style="left:450px;top:900px;font-size:120px">?</div></section>',
 "function(t){pop($('a2p'),t,.1,.45);up($('a2h'),t,w(1,'satu',.5),.4,40);pop($('a2q'),t,w(1,'kita',1.5),.4);tf($('a2t'),'translateY('+(Math.sin(t*5)*10)+'px)')}"))
# 3 intro
intro = INTRO_HTML('in').replace('id="inx"', 'id="b3"')
S.append((intro, "function(t){var P='in';pop($(P+'ph'),t,w(2,'saya',.9)-.4,.5,' rotate(-2deg)');up($(P+'nm'),t,w(2,'aldy',1.4),.4,40);up($(P+'rl'),t,w(2,'syahreza',2.2),.3,16);pop($(P+'1'),t,w(2,'belasan',3.4),.4);pop($(P+'2'),t,w(2,'seratus',w(2,'lebih',5.2)),.4);pop($(P+'3'),t,w(2,'branding',7.2),.4)}"))
# 4 nah
S.append(('<section class="sc" id="b4"><div class="a hand" id="d4a" style="left:84px;top:520px;width:900px;font-size:118px;line-height:1.05">kebiasaan yang saya maksud begini</div><svg class="a" viewBox="0 0 200 300" id="d4b" style="left:420px;top:900px;width:200px;height:300px" fill="none" stroke="#B84A2E" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"><path id="d4p" d="M100 10 C90 120 110 170 100 280 M45 215 L100 285 L155 215"/></svg></section>',
 "function(t){up($('d4a'),t,.1,.4,30);draw($('d4p'),t,w(3,'begini',1.3),.5)}"))
# 5 dulu (serp lama)
S.append(('<section class="sc" id="b5">' + serp('e5', False) + '<div class="a hand" id="e5h" style="left:0;right:0;top:1150px;text-align:center;font-size:92px">dulu: cari, lalu klik</div></section>',
 "function(t){var c=$('e5c');op(c,pr(t,.05,.3));tf(c,'translateY('+((1-E.out(pr(t,.05,.4)))*50)+'px)');for(var i=0;i<4;i++)up($('e5r'+i),t,.4+i*.18,.3,20);op($('e5chip'),pr(t,w(4,'reddit',2.6)-.2,.3));"
 "var k=E.io(pr(t,w(4,'klik',2.2)-.5,.9));var cu=$('e5cur');tf(cu,'translate('+((1-k)*180)+'px,'+(-k*240)+'px)');var rr=$('e5r1');rr.style.boxShadow=k>.95?'0 0 0 6px #B84A2E':'none';up($('e5h'),t,w(4,'klik',2.2),.4,30)}"))
# 6 sekarang (serp baru + jawaban AI)
S.append(('<section class="sc" id="b6">' + serp('f6', True) + '<div class="a hand" id="f6h" style="left:0;right:0;top:1150px;text-align:center;font-size:92px">sekarang: jawaban di atas</div></section>',
 "function(t){var c=$('f6c');op(c,pr(t,.05,.3));var ai=$('f6ai');var k=E.out(pr(t,w(5,'menjawab',1.2)-.3,.6));op(ai,k);tf(ai,'translateY('+((1-k)*-60)+'px)');for(var i=0;i<4;i++){var r=$('f6r'+i);op(r,.9-.5*k)}op($('f6chip'),.6*(1-k));up($('f6h'),t,w(5,'langsung',2),.4,30)}"))
# 7 orang berhenti (figur)
S.append(('<section class="sc" id="b7"><div class="a" id="g7p" style="left:80px;top:470px;width:360px;height:660px">' + person('p7', '#B84A2E', '#8f3a24', '#2a1d14') + '</div>'
 '<div class="a" id="g7ph" style="left:360px;top:790px;width:110px;height:190px;border-radius:18px;background:#0F0E0C;border:6px solid #0F0E0C;box-shadow:var(--sh)"><div style="margin:10px;height:130px;border-radius:10px;background:#FFE2B0"></div></div>'
 '<div class="a mono" id="g7l" style="left:540px;top:520px;font-size:26px;color:var(--gray)">klik ke reddit</div><div class="a disp" id="g7n" style="left:540px;top:570px;font-size:300px;line-height:1;color:#B84A2E">0</div>'
 '<div class="a hand" id="g7h" style="left:540px;top:900px;font-size:84px">berhenti di jawaban</div></section>',
 "function(t){op($('g7p'),pr(t,.1,.3));pop($('g7ph'),t,.3,.3);BOB('p7',t,3);var st=t>w(6,'berhenti',2);ARM('p7','ra',-70+(st?0:Math.sin(t*6)*8));HEAD('p7',st?0:Math.sin(t*3)*5);up($('g7l'),t,w(6,'tidak',3.2),.3,16);pop($('g7n'),t,w(6,'klik',3.4),.45);up($('g7h'),t,w(6,'berhenti',2),.4,30)}"))
# 8 akhir oktober
S.append(('<section class="sc" id="b8"><div class="a card" data-obj id="h8c" style="left:84px;top:430px;width:912px;height:620px"><div class="a" style="left:0;top:0;width:912px;height:120px;border-radius:34px 34px 0 0;background:#B84A2E"></div><div class="a mono" style="left:44px;top:40px;font-size:30px;color:#fff">kuartal ketiga 2026</div>'
 '<div class="a disp" id="h8d" style="left:44px;top:170px;font-size:260px;line-height:1">30</div><div class="a disp" id="h8m" style="left:440px;top:200px;font-size:120px;line-height:1;color:#B84A2E">OKT</div><div class="a" id="h8t" style="left:44px;top:480px;width:824px;font:700 44px/1.2 var(--f-body)">Laporan keuangan Reddit</div></div></section>',
 "function(t){pop($('h8c'),t,.1,.45);up($('h8d'),t,w(7,'oktober',.9),.4,30);up($('h8m'),t,w(7,'oktober',.9)+.15,.4,30);up($('h8t'),t,w(7,'melaporkan',1.6),.4,20)}"))
# 9 sahamnya turun
S.append(('<section class="sc" id="b9"><div class="a mono" id="i9l" style="left:84px;top:430px;font-size:26px;color:var(--gray)">besar penurunan menurut media</div><div class="a" id="i9b" style="left:84px;top:520px;width:912px;height:60px;border-radius:30px;background:#E8E1D5"></div>'
 '<div class="a" id="i9r" style="left:84px;top:520px;width:912px;height:60px;border-radius:30px;background:#B84A2E;transform-origin:left"></div><div class="a mono" style="left:84px;top:600px;font-size:26px">23%</div><div class="a mono" style="left:900px;top:600px;font-size:26px">36%</div>'
 '<div class="a" id="i9m" style="left:500px;top:480px;width:12px;height:140px;background:#0F0E0C"></div><div class="a disp" id="i9n" style="left:84px;top:700px;font-size:240px;line-height:1">29%</div><div class="a hand" id="i9h" style="left:84px;top:960px;font-size:84px">dalam sehari</div>'
 + src('Sumber: TheStreet, Yahoo Finance, Quartz (30 Okt 2026). Angka bervariasi antar media.') + '</section>',
 "function(t){up($('i9l'),t,.1,.3,16);op($('i9b'),pr(t,.1,.3));var k=E.io(pr(t,w(8,'turun',.8)-.2,.9));tf($('i9r'),'scaleX('+(k*.78)+')');op($('i9r'),k>0?1:0);op($('i9m'),pr(t,w(8,'sekitar',1.2),.3));pop($('i9n'),t,w(8,'29',1.6),.45);up($('i9h'),t,w(8,'sehari',2.2),.35,24)}"))
# 10 ceo mengaitkan
S.append(('<section class="sc" id="b10"><div class="a" id="j10a" data-obj style="left:84px;top:520px;width:380px;height:300px;border-radius:30px;background:#fff;box-shadow:var(--sh);padding:30px"><div class="mono" style="font-size:24px;color:var(--gray)">trafik dari</div><div class="disp" style="font-size:80px;margin-top:10px">GOOGLE</div><div class="disp" style="font-size:90px;color:#B84A2E;margin-top:6px">↓</div></div>'
 '<svg class="a" viewBox="0 0 1080 300" style="left:0;top:560px;width:1080px;height:300px" fill="none" stroke-linecap="round" stroke-linejoin="round"><path id="j10l" d="M480 120 L600 120 M570 90 L602 120 L570 150" stroke="#0F0E0C" stroke-width="10"/></svg>'
 '<div class="a" id="j10b" data-obj style="left:616px;top:520px;width:380px;height:300px;border-radius:30px;background:#0F0E0C;color:#fff;box-shadow:var(--sh);padding:30px"><div class="mono" style="font-size:24px;color:#FFE2B0">dikaitkan ke</div><div class="disp" style="font-size:72px;margin-top:10px;line-height:.95">JAWABAN<br>AI</div></div>'
 '<div class="a hand" id="j10h" style="left:84px;top:900px;font-size:84px">kata CEO Reddit</div></section>',
 "function(t){pop($('j10a'),t,w(9,'trafik',1.4)-.4,.45);draw($('j10l'),t,w(9,'mengaitkan',.9),.4);pop($('j10b'),t,w(9,'jawaban',2.2)-.3,.45);up($('j10h'),t,.2,.4,30)}"))
# 11 dugaan
S.append(('<section class="sc" id="b11"><div class="a disp" id="k11s" style="left:150px;top:600px;font-size:140px;color:#B84A2E;transform:rotate(-8deg);border:12px solid #B84A2E;border-radius:26px;padding:6px 34px;line-height:1">DUGAAN</div><div class="a hand" id="k11h" style="left:0;right:0;top:960px;text-align:center;font-size:100px">belum terbukti</div></section>',
 "function(t){pop($('k11s'),t,w(10,'dugaan',.4)-.1,.4);up($('k11h'),t,w(10,'belum',1.2),.4,30)}"))
# 12 login vs tidak login
S.append(('<section class="sc" id="b12"><div class="a" id="l12a" style="left:150px;top:420px;width:300px;height:640px"><div class="a" id="l12ar" style="left:0;bottom:0;width:300px;height:620px;background:#B84A2E;border-radius:24px 24px 0 0;transform-origin:50% 100%"></div></div>'
 '<div class="a" id="l12b" style="left:630px;top:420px;width:300px;height:640px"><div class="a" id="l12br" style="left:0;bottom:0;width:300px;height:200px;background:#0F0E0C;border-radius:24px 24px 0 0;transform-origin:50% 100%"></div></div>'
 '<div class="a disp" id="l12a1" style="left:130px;top:1090px;width:340px;text-align:center;font-size:40px;line-height:1.05">TIDAK LOGIN<br><span style="font:500 24px var(--f-mono)">dari Google</span></div><div class="a disp" id="l12b1" style="left:610px;top:1090px;width:340px;text-align:center;font-size:40px;line-height:1.05">APLIKASI &amp; LOGIN<br><span style="font:500 24px var(--f-mono)">langsung</span></div>'
 '<div class="a disp" id="l12u" style="left:380px;top:560px;font-size:120px;color:#B84A2E;opacity:0">↓</div><div class="a disp" id="l12v" style="left:860px;top:300px;font-size:120px;opacity:0">↑</div></section>',
 "function(t){op($('l12a'),pr(t,.1,.3));op($('l12b'),pr(t,.1,.3));var d=E.io(pr(t,w(11,'turun',1.4)-.2,1.2));tf($('l12ar'),'scaleY('+(1-.65*d)+')');op($('l12a1'),pr(t,w(11,'pengunjung',2.2),.3));op($('l12u'),pr(t,w(11,'turun',1.4)+.8,.3));"
 "var u=E.io(pr(t,w(11,'justru',4.6)-.4,1.0));tf($('l12br'),'scaleY('+(1+2.2*u)+')');op($('l12b1'),pr(t,w(11,'aplikasi',4.0),.3));op($('l12v'),pr(t,w(11,'naik',5),.3))}"))
# 13 tahan = hubungan langsung
S.append(('<section class="sc" id="b13"><div class="a" id="m13a" data-obj style="left:84px;top:520px;width:330px;height:260px;border-radius:30px;background:var(--terra);color:#fff;box-shadow:var(--sh);display:flex;align-items:center;justify-content:center;font:800 64px/1 var(--f-display)">BRAND</div>'
 '<div class="a" id="m13b" data-obj style="left:666px;top:520px;width:330px;height:260px;border-radius:30px;background:#0F0E0C;color:#fff;box-shadow:var(--sh);display:flex;align-items:center;justify-content:center;font:800 42px/1 var(--f-display)">PELANGGAN</div>'
 '<div class="a" id="m13l" style="left:414px;top:632px;width:252px;height:36px;border-radius:8px;background:#C8944A;border:7px solid #0F0E0C;transform-origin:left"></div>'
 '<div class="a disp" id="m13h" style="left:84px;top:900px;font-size:104px;line-height:.95">HUBUNGAN<br><span style="color:#B84A2E">LANGSUNG</span></div></section>',
 "function(t){pop($('m13a'),t,.1,.4);pop($('m13b'),t,.25,.4);var k=E.io(pr(t,w(12,'hubungan',.8)-.1,.7));tf($('m13l'),'scaleX('+k+')');op($('m13l'),k>0?1:0);up($('m13h'),t,w(12,'hubungan',.8),.4,40)}"))
# 14 terus apa hubungannya (pelanggan cari sepatu)
S.append(('<section class="sc" id="b14"><div class="a" id="n14p" style="left:70px;top:520px;width:330px;height:620px">' + person('p14', '#C8944A', '#a57a35', '#2a1d14') + '</div>'
 '<div class="a" id="n14b" style="left:420px;top:470px;width:580px;padding:30px 36px;border-radius:40px 40px 40px 10px;background:#fff;box-shadow:0 10px 0 rgba(15,14,12,.9);font:700 48px/1.2 var(--f-body)">“Sepatu kerja yang nyaman, apa ya?”</div>'
 '<svg class="a" id="n14s" viewBox="0 0 200 120" style="left:520px;top:800px;width:360px;height:216px;overflow:visible"><path d="M10 82 Q10 62 30 60 L70 52 Q85 26 112 32 L150 56 Q186 62 192 86 L192 96 L10 96Z" fill="#C8944A" stroke="#0F0E0C" stroke-width="5" stroke-linejoin="round"/><path d="M10 96 L192 96 L192 106 Q192 114 182 114 L20 114 Q10 114 10 106Z" fill="#0F0E0C"/></svg>'
 + IL % ('n14il', 1080, 'ilustrasi') + '</section>',
 "function(t){op($('n14p'),pr(t,.1,.3));BOB('p14',t,3);ARM('p14','ra',-50+Math.sin(t*3)*6);HEAD('p14',Math.sin(t*2)*4);pop($('n14b'),t,w(13,'bayangin',2),.45);pop($('n14s'),t,w(13,'sepatu',4.3)-.2,.45);pop($('n14il'),t,w(13,'cari',3.6),.3)}"))
# 15 AI nyebut brand lain
S.append(('<section class="sc" id="b15"><div class="a" id="o15u" style="left:300px;top:430px;width:700px;padding:28px 36px;border-radius:36px 36px 10px 36px;background:#0F0E0C;color:#fff;box-shadow:0 10px 0 var(--terra);font:700 44px/1.2 var(--f-body)">Sepatu kerja yang nyaman, brand apa?</div>'
 '<div class="a" id="o15a" style="left:84px;top:640px;width:800px;padding:30px 36px;border-radius:36px 36px 36px 10px;background:#fff;box-shadow:0 10px 0 rgba(15,14,12,.9)"><div class="mono" style="font-size:22px;color:var(--gray)">jawaban AI</div><div style="font:700 40px/1.2 var(--f-body);margin-top:10px">Rekomendasi:</div><div style="display:flex;gap:14px;margin-top:16px"><span class="chip" style="background:#E8E1D5;font-size:26px">Brand A</span><span class="chip" style="background:#E8E1D5;font-size:26px">Brand B</span><span class="chip" style="background:#E8E1D5;font-size:26px">Brand C</span></div></div>'
 '<div class="a" id="o15k" style="left:84px;top:960px;width:560px;padding:22px 30px;border-radius:999px;border:6px dashed #9a948c;color:#9a948c;font:800 42px/1 var(--f-display)">BRAND KAMU</div><div class="a hand" id="o15h" style="left:660px;top:960px;font-size:84px;color:#B84A2E">gak disebut</div>'
 + IL % ('o15il', 1130, 'ilustrasi') + '</section>',
 "function(t){pop($('o15u'),t,.1,.4);pop($('o15a'),t,w(14,'nyebut',1.2)-.6,.45);pop($('o15k'),t,w(14,'bukan',2.4),.4);up($('o15h'),t,w(14,'alasan',4.6),.4,20);pop($('o15il'),t,.5,.3)}"))
# 16 tujuan: disebut
S.append(('<section class="sc" id="b16"><div class="a mono" id="q16l" style="left:84px;top:410px;font-size:26px;color:var(--terra)">tujuannya</div>'
 '<div class="a" id="q16a" style="left:84px;top:470px;width:912px;padding:30px 36px;border-radius:36px;background:#fff;box-shadow:var(--sh)"><div class="mono" style="font-size:22px;color:var(--gray)">jawaban AI</div>'
 '<div style="display:flex;gap:16px;align-items:center;margin-top:20px;font:700 44px/1 var(--f-body)"><span>1</span><span class="chip" style="background:#E8E1D5;font-size:28px">Brand A</span></div>'
 '<div style="display:flex;gap:16px;align-items:center;margin-top:18px;font:700 44px/1 var(--f-body)"><span>2</span><span class="chip" id="q16k" style="background:#C8944A;color:#0F0E0C;font-size:34px">BRAND KAMU</span></div>'
 '<div style="display:flex;gap:16px;align-items:center;margin-top:18px;font:700 44px/1 var(--f-body)"><span>3</span><span class="chip" style="background:#E8E1D5;font-size:28px">Brand C</span></div></div>'
 '<div class="a disp" id="q16h" style="left:84px;top:960px;font-size:90px;line-height:.95">nama brand kamu<br><span style="color:#B84A2E">ikut disebut</span></div></section>',
 "function(t){up($('q16l'),t,.1,.3,16);pop($('q16a'),t,.2,.45);var kk=$('q16k');pop(kk,t,w(15,'nama',3)-.2,.45);up($('q16h'),t,w(15,'ikut',4.2)-.4,.4,40)}"))
# 17 AI baca internet
S.append(('<section class="sc" id="b17"><div class="a" id="r17u" data-obj style="left:84px;top:480px;width:360px;height:280px;border-radius:26px;border:8px dashed #9a948c;display:flex;align-items:center;justify-content:center;font:800 46px/1.05 var(--f-display);color:#9a948c;text-align:center">TITIP<br>DATA</div><div class="a hand" id="r17x" style="left:84px;top:772px;font-size:70px;color:#B84A2E;opacity:0">gak ada tempat titip</div>'
 '<div class="a" id="r17n" data-obj style="left:660px;top:520px;width:330px;height:220px;border-radius:30px;background:#0F0E0C;color:#fff;box-shadow:var(--sh);display:flex;align-items:center;justify-content:center;font:800 100px/1 var(--f-display)">AI</div>'
 '<div class="a" id="r17w0" style="left:84px;top:860px;width:260px;height:150px;border-radius:18px;background:#fff;box-shadow:var(--sh);padding:18px"><div style="height:12px;background:#E0D8CA;border-radius:6px"></div><div style="margin-top:12px;height:10px;width:70%;background:#E0D8CA;border-radius:5px"></div></div>'
 '<div class="a" id="r17w1" style="left:380px;top:900px;width:260px;height:150px;border-radius:18px;background:#fff;box-shadow:var(--sh);padding:18px"><div style="height:12px;background:#E0D8CA;border-radius:6px"></div><div style="margin-top:12px;height:10px;width:70%;background:#E0D8CA;border-radius:5px"></div></div>'
 '<div class="a" id="r17w2" style="left:676px;top:860px;width:260px;height:150px;border-radius:18px;background:#fff;box-shadow:var(--sh);padding:18px"><div style="height:12px;background:#E0D8CA;border-radius:6px"></div><div style="margin-top:12px;height:10px;width:70%;background:#E0D8CA;border-radius:5px"></div></div>'
 '<div class="a hand" id="r17h" style="left:0;right:0;top:1090px;text-align:center;font-size:84px">dia cuma baca internet</div></section>'.replace('id="r17"', 'id="b17"'),
 "function(t){pop($('r17u'),t,.1,.4);pop($('r17x'),t,w(16,'titip',2.1),.4);pop($('r17n'),t,w(16,'dia',3.4)-.4,.4);for(var i=0;i<3;i++)pop($('r17w'+i),t,w(16,'baca',4.4)-.2+i*.25,.35);up($('r17h'),t,w(16,'internet',5.2),.4,24)}"))
# 18 tiga hal
S.append(('<section class="sc" id="b18"><div class="a disp" id="s18n" style="left:0;right:0;top:430px;text-align:center;font-size:400px;line-height:1;color:#B84A2E">3</div><div class="a disp" id="s18h" style="left:0;right:0;top:960px;text-align:center;font-size:72px">hal yang bisa kamu lakuin</div></section>',
 "function(t){pop($('s18n'),t,w(17,'tiga',.7)-.2,.5);up($('s18h'),t,w(17,'hal',1),.4,30)}"))
# 19-21 langkah (kartu)
def stepcard(idn, bid, num, col, title, body):
    return ('<section class="sc" id="%s"><div class="a card" data-obj id="%sc" style="left:84px;top:410px;width:912px;height:760px"><div class="a" style="left:44px;top:44px;width:130px;height:130px;border-radius:50%%;background:%s;color:#fff;display:flex;align-items:center;justify-content:center;font:800 78px/1 var(--f-display)">%s</div>'
            '<div class="a disp" id="%st" style="left:200px;top:52px;width:680px;font-size:60px;line-height:1">%s</div>%s</div></section>') % (bid, idn, col, num, idn, title, body)
S.append((stepcard('t19', 'b19', '1', '#B84A2E', 'Tulis jelas di rumahmu sendiri',
  '<div class="a" id="t19q" style="left:44px;top:210px;width:824px;padding:26px 32px;border-radius:24px;background:#F2EDE3;font:700 38px/1.3 var(--f-body)">“<span style="color:#B84A2E">[Brand]</span> jual <span style="color:#B84A2E">[apa]</span>, untuk <span style="color:#B84A2E">[siapa]</span>, beda karena <span style="color:#B84A2E">[alasan]</span>.”</div>'
  '<div class="a mono" style="left:44px;top:430px;font-size:24px;color:var(--gray)">taruh di</div>'
  '<div class="a" id="t19p0" style="left:44px;top:480px;width:824px;height:70px;border-radius:999px;background:#0F0E0C;color:#fff;display:flex;align-items:center;padding-left:34px;font:700 34px/1 var(--f-body)">✓ &nbsp;Website</div>'
  '<div class="a" id="t19p1" style="left:44px;top:566px;width:824px;height:70px;border-radius:999px;background:#0F0E0C;color:#fff;display:flex;align-items:center;padding-left:34px;font:700 34px/1 var(--f-body)">✓ &nbsp;Profil Google bisnis</div>'
  '<div class="a" id="t19p2" style="left:44px;top:652px;width:824px;height:70px;border-radius:999px;background:#0F0E0C;color:#fff;display:flex;align-items:center;padding-left:34px;font:700 34px/1 var(--f-body)">✓ &nbsp;Deskripsi toko online</div>'),
 "function(t){var c=$('t19c');op(c,pr(t,.05,.3));tf(c,'translateY('+((1-E.out(pr(t,.05,.4)))*50)+'px)');up($('t19t'),t,w(18,'tulis',.8),.4,24);up($('t19q'),t,w(18,'kalimat',3.2)-.3,.4,24);var a=['website','profil','deskripsi'];for(var i=0;i<3;i++)up($('t19p'+i),t,w(18,a[i],6+i*1.2)-.1,.35,30)}"))
S.append((stepcard('t20', 'b20', '2', '#0F0E0C', 'Bikin orang lain yang ngomongin kamu',
  ''.join('<div class="a" id="t20c%d" style="left:%dpx;top:%dpx;width:392px;height:140px;border-radius:24px;background:#F2EDE3;padding:22px 26px"><div class="disp" style="font-size:44px">%s</div><div style="margin-top:8px;font:700 26px/1.2 var(--f-body);color:#6B6560">%s</div></div>' % (i, 44 + (i % 2) * 432, 240 + (i // 2) * 164, a, b) for i, (a, b) in enumerate([('★★★★★', 'ulasan pelanggan'), ('KORAN', 'liputan'), ('▶ VIDEO', 'konten orang lain'), ('FORUM', 'obrolan')]))
  + '<div class="a mono" style="left:44px;top:590px;font-size:22px;color:var(--gray)">yang disebut banyak tempat</div><div class="a" style="left:44px;top:630px;width:824px;height:26px;border-radius:13px;background:#E8E1D5"></div><div class="a" id="t20b" style="left:44px;top:630px;width:824px;height:26px;border-radius:13px;background:#B84A2E;transform-origin:left"></div><div class="a mono" style="left:44px;top:672px;font-size:22px;color:var(--gray)">omongan sendiri: pendek</div>'),
 "function(t){var c=$('t20c');op($('t20c'),pr(t,.05,.3));tf($('t20c'),'translateY('+((1-E.out(pr(t,.05,.4)))*50)+'px)');up($('t20t'),t,w(19,'bikin',.8),.4,24);var a=['ulasan','liputan','video','obrolan'];for(var i=0;i<4;i++)pop($('t20c'+i),t,w(19,a[i],3+i*1.1)-.1,.35);var k=E.io(pr(t,w(19,'percaya',9)-.2,1.0));tf($('t20b'),'scaleX('+k+')')}"))
S.append((stepcard('t21', 'b21', '3', '#C8944A', 'Samain di semua tempat, cek tiap bulan',
  '<div class="a mono" style="left:44px;top:200px;font-size:24px;color:var(--gray)">tanya AI, lima pertanyaan pelanggan</div>'
  + ''.join('<div class="a" id="t21q%d" style="left:44px;top:%dpx;width:824px;height:62px;border-radius:14px;background:#F2EDE3;display:flex;align-items:center;gap:18px;padding-left:20px;font:700 30px/1 var(--f-body)"><span style="display:inline-block;width:34px;height:34px;border:5px solid #0F0E0C;border-radius:9px"></span><span style="width:%dpx;height:14px;background:#d8d0c2;border-radius:7px"></span></div>' % (i, 250 + i * 74, 420 - i * 30) for i in range(5))
  + '<div class="a" id="t21r" style="left:44px;top:640px;width:824px;padding:22px 30px;border-radius:999px;background:#0F0E0C;color:#fff;font:800 38px/1 var(--f-display)">nama brand kamu muncul gak?</div>'),
 "function(t){op($('t21c'),pr(t,.05,.3));tf($('t21c'),'translateY('+((1-E.out(pr(t,.05,.4)))*50)+'px)');up($('t21t'),t,w(20,'samain',.8),.4,24);for(var i=0;i<5;i++)up($('t21q'+i),t,w(20,'lima',5.8)-.2+i*.3,.3,20);pop($('t21r'),t,w(20,'nama',w(20,'muncul',9.5))-.3,.45)}"))
# 22 CTA
S.append(('<section class="sc" id="b22"><div class="a" style="left:0;top:0;width:1080px;height:1920px;background:var(--terra)"></div>'
 '<div class="a" id="u22s" data-obj style="left:440px;top:300px;width:200px;height:200px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 14px 0 rgba(15,14,12,.35)"><svg viewBox="0 0 24 24" width="92" height="92" fill="none" stroke="#B84A2E" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"><path d="M6 3h12v18l-6-4-6 4z"/></svg></div>'
 '<div class="a disp" id="u22h1" style="left:0;right:0;top:540px;text-align:center;font-size:130px;color:#fff;line-height:1">SIMPAN</div><div class="a disp" id="u22h2" style="left:0;right:0;top:675px;text-align:center;font-size:110px;color:#0F0E0C;line-height:1">VIDEO INI</div>'
 '<div class="a" id="u22sub" style="left:96px;right:96px;top:830px;text-align:center;font:700 42px/1.25 var(--f-body);color:#fff">Tulis satu kalimat brand kamu hari ini.</div>'
 + ''.join('<div class="a" id="u22p%d" style="left:96px;top:%dpx;width:888px;height:96px;border-radius:999px;background:#fff;display:flex;align-items:center;padding-left:48px;font:800 44px/1 var(--f-display);color:#0F0E0C">%s</div>' % (i, 960 + i * 110, t) for i, t in enumerate(['1 &nbsp;Tulis jelas di rumah sendiri', '2 &nbsp;Bikin orang lain ngomongin', '3 &nbsp;Samain, cek tiap bulan']))
 + '<div class="a mono" id="u22h" style="left:0;right:0;top:1310px;text-align:center;font-size:34px;color:#fff;letter-spacing:.06em">@aldysyahreza</div></section>',
 "function(t){pop($('u22s'),t,.05,.45);up($('u22h1'),t,.2,.35,40);up($('u22h2'),t,.35,.35,40);up($('u22sub'),t,w(21,'mulai',1.6),.35,30);for(var i=0;i<3;i++)up($('u22p'+i),t,w(21,'simpan',3)-.2+i*.25,.35,40);op($('u22h'),pr(t,w(21,'simpan',3)+.9,.4))}"))

BODY = '<div class="bgpaper" id="bgp"></div><div class="bgdx" id="bgd"></div>\n' + '\n'.join(h for h, j in S)
helpers = r"""
function RT(id,a,cx,cy){var e=$(id);if(e)e.setAttribute('transform','rotate('+a.toFixed(2)+' '+cx+' '+cy+')')}
function BOB(u,t,amp){var e=$(u+'_b');if(e)e.setAttribute('transform','translate(0,'+(Math.sin(t*3.2)*amp).toFixed(2)+')')}
function ARM(u,side,a){RT(u+'_'+side,a,side==='la'?73:127,134)}
function HEAD(u,a){RT(u+'_h',a,100,104)}
"""
JS = (eng + "\nvar WT=" + json.dumps(WT) + ";\nfunction w(i,k,d){var v=WT[i]&&WT[i][k];return v==null?d:v}\n" + helpers + cap +
      "\nvar DI=99,SCAN_A=0,SCAN_B=0;\nvar S=[\n " + ',\n '.join(j for h, j in S) + "];\n"
      "var TR=[" + ','.join(["null"] + ["'%s'" % x for x in ['zoom','drop','whip','whip','drop','whip','drop','drop','whip','drop','whip','drop','whip','drop','drop','whip','drop','whip','whip','drop','drop'][:len(S)-1]]) + "];var TD=.42;\n" + fin)
JS = JS.replace('__DEF__', DEF)
open(A + 'animatic-reddit.html', 'w', encoding='utf-8').write(head + BODY + tail + JS)
anch = {"_petunjuk": "Adegan dimulai pada kata pembukanya.", "scenes": [{"start": a, "act": b, "chap": c} for a, b, c in SC], "beats": [[] for _ in SC]}
json.dump(anch, open(A + 'anchors-reddit.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', len(S), 'adegan; total', round(sum(DUR), 1), 's')
print([ (SC[i][0], DUR[i]) for i in range(len(SC))])
