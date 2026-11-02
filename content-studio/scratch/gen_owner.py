import json
A = '/home/user/content-studio/animatic/'
M = open('/home/user/content-studio/scratch/gen_meja.py', encoding='utf-8').read()
v3 = open(A + 'animatic-v3.html', encoding='utf-8').read()
head = v3[:v3.index('<div class="bgpaper" id="bgp"></div>')].replace('<title>Animatic v3 The Brand Fixer</title>', '<title>Animatic: marketing vs owner, cerita dari meja meeting #4</title>')
tail = v3[v3.index('<div id="scan">'):v3.index('<script>')]
eng = M[M.index("JS = r'''") + len("JS = r'''"):M.index("/* ---------- bangun objek ---------- */")]
cap = M[M.index("var CAP=BEATS.map"):M.index("/* ---------- adegan ---------- */")]
fin = M[M.index("var TR=["):M.index("'''.replace('__DEF__'")]
fin = fin[fin.index("function apply"):].replace('cur===14', 'cur===18')

DUR = [5.6,4.7,4.5,8.4,3.0,4.7,5.0,3.1,3.1,5.1,5.2,4.4,4.1,4.6,3.9,8.1,5.8,6.1,10.0]
SC = [("marketing","HOOK",1),("di","RELATE",2),("konten","RELATE",2),("dua","RELATE",2),("perusahaan","INSIGHT",3),("tahun","INSIGHT",3),("dananya","INSIGHT",3),("biasanya","INSIGHT",3),("tapi","INSIGHT",3),("kalau","INSIGHT",3),("jembatannya","REFRAME",4),("ice","REFRAME",4),("pertama","REFRAME",4),("kedua","REFRAME",4),("ketiga","REFRAME",4),("contohnya","REFRAME",4),("kampanye","REFRAME",4),("refresh","REFRAME",4),("kirim","CTA",5)]
SAY = ['Marketing bilang konten perlu refresh. Owner dengar: biaya lagi.','Di bisnis yang saya dampingi, usulan marketing sering mentok di meja owner.','Konten lama perlu di-refresh. Owner: Jadi ada biaya baru lagi?','Dua-duanya gak salah. Marketing bicara soal hasil. Owner bicara soal uang keluar. Bahasanya aja beda.','Perusahaan besar juga begitu.','Tahun 2010, Pepsi melewatkan iklan Super Bowl untuk pertama kalinya dalam 23 tahun.','Dananya dipindah ke kampanye sosial sekitar dua puluh juta dolar.','Kampanye begitu biasanya dinilai dari partisipasi dan obrolan.','Tapi pertanyaan owner tetap sama: berapa yang terjual?','Kalau dua bahasa ini gak dijembatani, usulan sebagus apa pun susah disetujui.','Jembatannya pakai kerangka yang sudah dikenal tim growth: ICE, dari Sean Ellis.','ICE itu tiga skor, satu sampai sepuluh, untuk tiap usulan.','Pertama, Impact.','Kedua, Confidence.','Ketiga, Ease.','Contohnya, ada dua usulan. Refresh konten lama: impact enam, confidence delapan, ease sembilan.','Kampanye baru: impact delapan, confidence empat, ease tiga.','Refresh jalan duluan. Kampanye baru boleh maju, kalau tim bisa kasih dasar yang lebih kuat.','Kirim ke tim marketing kamu.']
DEF = ',\n  '.join("{dur:%s,name:'%s',chap:%d,say:%s}" % (DUR[i], SC[i][1], SC[i][2], json.dumps(SAY[i], ensure_ascii=False)) for i in range(len(DUR)))

DISCP = '<div class="mono" style="position:absolute;left:96px;right:96px;top:1265px;font-size:19px;letter-spacing:.04em;color:#6B6560;text-transform:none;line-height:1.3">Logo dan kemasan digambar ulang sebagai ilustrasi; merek milik pemiliknya. Akun ini tidak berafiliasi dengan PepsiCo.</div>'
DISCS = '<div class="mono" style="position:absolute;left:96px;right:96px;top:1265px;font-size:19px;letter-spacing:.04em;color:#6B6560;text-transform:none;line-height:1.3">Sumber: ABC News, BevNET, Chronicle of Philanthropy (2009-2010). Akun ini tidak berafiliasi dengan PepsiCo.</div>'
DISCN = '<div class="mono" style="position:absolute;left:96px;right:96px;top:1265px;font-size:19px;letter-spacing:.04em;color:#6B6560;text-transform:none;line-height:1.3">Hasil penjualan kampanye ini tidak diklaim di video ini. Akun ini tidak berafiliasi dengan PepsiCo.</div>'

def emblem(sz, uid):
    return ('<svg viewBox="0 0 200 200" width="%d" height="%d" style="display:block"><defs><clipPath id="pc%s"><circle cx="100" cy="100" r="96"/></clipPath></defs>'
            '<g clip-path="url(#pc%s)"><rect width="200" height="200" fill="#fff"/><path d="M0 0H200V90C150 62 108 118 0 98Z" fill="#D8232A"/><path d="M0 112C108 134 150 84 200 108V200H0Z" fill="#0B4A9B"/></g>'
            '<circle cx="100" cy="100" r="96" fill="none" stroke="#0F0E0C" stroke-width="5"/></svg>') % (sz, sz, uid, uid)
def can(w, uid):
    h = int(w * 2)
    return ('<svg viewBox="0 0 100 200" width="%d" height="%d" style="display:block;overflow:visible"><rect x="6" y="14" width="88" height="176" rx="14" fill="#0B4A9B" stroke="#0F0E0C" stroke-width="5"/>'
            '<path d="M6 92C34 74 58 112 94 92V118C58 138 34 98 6 118Z" fill="#fff"/><path d="M6 60C34 46 58 76 94 62V92C58 108 34 76 6 92Z" fill="#D8232A"/>'
            '<rect x="6" y="2" width="88" height="22" rx="10" fill="#C9C9C9" stroke="#0F0E0C" stroke-width="5"/><rect x="6" y="176" width="88" height="22" rx="10" fill="#C9C9C9" stroke="#0F0E0C" stroke-width="5"/>'
            '<text x="50" y="158" text-anchor="middle" font-family="Archivo" font-weight="800" font-size="19" fill="#fff" stroke="none">PEPSI</text></svg>') % (w, h)
TV = '<svg viewBox="0 0 200 150" width="260" height="195" fill="none" stroke="#0F0E0C" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"><rect x="14" y="20" width="172" height="106" rx="16" fill="#fff"/><path d="M60 140 L140 140 M100 126 V140"/><path d="M84 58 L124 74 L84 92Z" fill="#B84A2E"/></svg>'
REFRESH = '<svg viewBox="0 0 100 100" width="130" height="130" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"><path d="M80 40A32 32 0 0 0 24 34M20 60A32 32 0 0 0 76 66"/><path d="M80 18 V40 H58 M20 82 V60 H42"/></svg>'
COINS = '<svg viewBox="0 0 120 100" width="150" height="125" fill="none" stroke="#0F0E0C" stroke-width="6"><ellipse cx="60" cy="76" rx="42" ry="16" fill="#C8944A"/><ellipse cx="60" cy="58" rx="42" ry="16" fill="#C8944A"/><ellipse cx="60" cy="40" rx="42" ry="16" fill="#E0B060"/><text x="60" y="47" text-anchor="middle" font-family="Archivo" font-weight="800" font-size="20" fill="#0F0E0C" stroke="none">Rp</text></svg>'
BULL = '<svg viewBox="0 0 400 220" width="400" height="220" style="display:block;margin:0 auto" fill="none" stroke="#0F0E0C" stroke-width="8"><circle cx="200" cy="110" r="96" fill="#fff"/><circle cx="200" cy="110" r="62" fill="#fff"/><circle cx="200" cy="110" r="28" fill="#B84A2E"/><path id="bul" d="M330 20 L204 106 M330 20 L330 52 M330 20 L298 20" stroke-linecap="round"/></svg>'
SHIELD = '<svg viewBox="0 0 400 220" width="400" height="220" style="display:block;margin:0 auto" fill="none" stroke="#0F0E0C" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"><path d="M200 14 L300 46 V112 C300 160 250 196 200 210 C150 196 100 160 100 112 V46Z" fill="#fff"/><path id="chk" d="M150 112 L190 150 L252 74" stroke="#B84A2E" stroke-width="16"/></svg>'
WATCH = '<svg viewBox="0 0 400 220" width="400" height="220" style="display:block;margin:0 auto" fill="none" stroke="#0F0E0C" stroke-width="8" stroke-linecap="round"><circle cx="200" cy="124" r="84" fill="#fff"/><path d="M176 26 H224 M200 26 V40 M262 56 L278 40"/><g id="wh" style="transform-origin:200px 124px"><path d="M200 124 V72" stroke="#B84A2E" stroke-width="12"/></g><circle cx="200" cy="124" r="9" fill="#0F0E0C"/></svg>'

def person(u, shirt, dark, hair, flip=False, tie=False):
    inner = ('<g id="%(u)s_ll"><rect x="73" y="214" width="26" height="146" rx="13" fill="#2a2622"/></g><g id="%(u)s_lr"><rect x="101" y="214" width="26" height="146" rx="13" fill="#2a2622"/></g>'
             '<g id="%(u)s_b"><g id="%(u)s_la"><rect x="62" y="126" width="22" height="104" rx="11" fill="%(dark)s"/><circle cx="73" cy="236" r="12" fill="#F1C9A3"/></g>'
             '<rect x="66" y="112" width="68" height="124" rx="28" fill="%(shirt)s"/>%(tie)s'
             '<g id="%(u)s_ra"><rect x="116" y="126" width="22" height="104" rx="11" fill="%(dark)s"/><circle cx="127" cy="236" r="12" fill="#F1C9A3"/></g>'
             '<g id="%(u)s_h"><rect x="90" y="96" width="20" height="22" fill="#F1C9A3"/><circle cx="100" cy="70" r="35" fill="#F1C9A3"/><path d="M65 66 A35 35 0 0 1 135 66 Q118 44 100 47 Q82 44 65 66Z" fill="%(hair)s"/><circle cx="88" cy="76" r="3.4" fill="#0F0E0C"/><circle cx="114" cy="76" r="3.4" fill="#0F0E0C"/><path id="%(u)s_m" d="M91 92 Q101 99 111 92" fill="none" stroke="#0F0E0C" stroke-width="3.4" stroke-linecap="round"/></g></g>'
             ) % {'u': u, 'shirt': shirt, 'dark': dark, 'hair': hair, 'tie': ('<path d="M100 114 L110 130 L103 176 L100 182 L97 176 L90 130Z" fill="#0F0E0C"/>' if tie else '')}
    if flip: inner = '<g transform="translate(200,0) scale(-1,1)">' + inner + '</g>'
    return '<svg viewBox="0 0 200 380" style="overflow:visible;display:block" width="100%%" height="100%%"><ellipse cx="100" cy="366" rx="64" ry="9" fill="rgba(15,14,12,.16)"/>' + inner + '</svg>'

def card(p, num, col, title, sub, icon, fs=92):
    return ('<section class="sc" id="%s"><div class="a card" data-obj id="%sc" style="left:84px;top:400px;width:912px;height:760px">'
            '<div class="a" style="left:44px;top:50px;width:170px;height:170px;border-radius:50%%;background:%s;color:#fff;display:flex;align-items:center;justify-content:center;font:800 100px/1 var(--f-display)">%s</div>'
            '<div class="a disp" id="%st" style="left:250px;top:84px;font-size:%dpx;white-space:nowrap">%s</div>'
            '<div class="a" id="%ss" style="left:44px;top:290px;width:824px;font:700 52px/1.22 var(--f-body)">%s</div>'
            '<div class="a" id="%si" style="left:44px;top:470px;width:824px;height:250px">%s</div></div></section>') % (p, p, col, num, p, fs, title, p, sub, p, icon)
def scorecard(p, title, col, rows, note):
    h = ''.join('<div class="a mono" style="left:44px;top:%dpx;font-size:30px;color:#6B6560">%s</div><div class="a" style="left:300px;top:%dpx;width:480px;height:44px;border-radius:22px;background:#E8E1D5"></div><div class="a" id="%sb%d" style="left:300px;top:%dpx;width:480px;height:44px;border-radius:22px;background:%s;transform-origin:left"></div><div class="a disp" id="%sn%d" style="left:810px;top:%dpx;font-size:64px;line-height:1">%s</div>' % (200+i*120, r[0], 200+i*120-2, p, i, 200+i*120-2, col, p, i, 200+i*120-16, r[1]) for i, r in enumerate(rows))
    return ('<section class="sc" id="%s"><div class="a card" data-obj id="%sc" style="left:84px;top:400px;width:912px;height:620px"><div class="a disp" id="%st" style="left:44px;top:50px;font-size:60px;white-space:nowrap;color:%s">%s</div>%s</div>'
            '<span class="chip a" id="%sil" style="left:84px;top:1060px;background:var(--amber);color:var(--ink)">contoh hitungan</span><div class="a" id="%snt" style="left:84px;top:1130px;width:912px;font:700 40px/1.2 var(--f-body);color:#6B6560">%s</div></section>') % (p, p, p, col, title, h, p, p, note)

BODY = r'''<div class="bgpaper" id="bgp"></div><div class="bgdx" id="bgd"></div>

<section class="sc" id="b1">
  <div class="a mono" id="a1l" style="left:84px;top:410px;color:var(--terra);font-size:26px">marketing bilang</div>
  <div class="a" id="a1b" style="left:84px;top:455px;width:720px;padding:34px 40px;border-radius:36px 36px 36px 10px;background:var(--terra);color:#fff;box-shadow:0 10px 0 rgba(15,14,12,.9);font:700 52px/1.15 var(--f-body);display:flex;align-items:center;gap:26px">__REFRESH__<span>“konten perlu refresh”</span></div>
  <div class="a hand" id="a1h" style="left:0;right:0;top:760px;text-align:center;font-size:84px">yang didengar owner:</div>
  <div class="a mono" id="a1l2" style="left:276px;top:900px;color:var(--gray);font-size:26px">owner dengar</div>
  <div class="a" id="a1b2" style="left:276px;top:945px;width:720px;padding:34px 40px;border-radius:36px 36px 10px 36px;background:#0F0E0C;color:#fff;box-shadow:0 10px 0 var(--terra);font:700 56px/1.15 var(--f-body);display:flex;align-items:center;gap:26px">__COINS__<span>“biaya lagi”</span></div>
</section>

<section class="sc" id="b2">
  <div class="a" id="e2fl" style="left:70px;top:1150px;width:940px;height:8px;border-radius:4px;background:#0F0E0C;opacity:.85"></div>
  <div class="a" id="e2mS" style="left:60px;top:570px;width:320px;height:600px">__PM2__</div>
  <div class="a" id="e2oS" style="left:700px;top:570px;width:320px;height:600px">__PO2__</div>
  <div class="a mono" id="e2ml" style="left:60px;top:1180px;width:320px;text-align:center;font-size:24px;color:var(--terra)">marketing</div>
  <div class="a mono" id="e2ol" style="left:700px;top:1180px;width:320px;text-align:center;font-size:24px;color:var(--gray)">owner</div>
  <div class="a" id="e2p" data-obj style="left:340px;top:760px;width:190px;height:240px;background:#fff;border-radius:16px;box-shadow:var(--sh);padding:22px;font:700 32px/1.2 var(--f-body);transform-origin:left center">usulan<div style="margin-top:16px;height:9px;background:#E8E1D5;border-radius:5px"></div><div style="margin-top:12px;height:9px;background:#E8E1D5;border-radius:5px"></div><div style="margin-top:12px;height:9px;width:60%;background:#E8E1D5;border-radius:5px"></div></div>
  <div class="a disp" id="e2x" style="left:440px;top:470px;font-size:190px;color:#B84A2E;transform-origin:center">✕</div>
</section>

<section class="sc" id="b3">
  <div class="a mono" id="f3l1" style="left:84px;top:410px;color:var(--terra);font-size:24px">marketing</div>
  <div class="a" id="f3b1" style="left:84px;top:450px;width:800px;padding:30px 38px;border-radius:36px 36px 36px 10px;background:#fff;box-shadow:0 10px 0 rgba(15,14,12,.9);font:700 48px/1.2 var(--f-body)">“Konten lama perlu di-refresh.”</div>
  <div class="a mono" id="f3l2" style="left:180px;top:720px;color:var(--gray);font-size:24px">owner</div>
  <div class="a" id="f3b2" style="left:180px;top:760px;width:800px;padding:30px 38px;border-radius:36px 36px 10px 36px;background:#0F0E0C;color:#fff;box-shadow:0 10px 0 var(--terra);font:700 48px/1.2 var(--f-body)">“Jadi ada biaya baru lagi?”</div>
  <div class="a" id="f3mS" style="left:70px;top:890px;width:190px;height:360px">__PM3__</div><div class="a" id="f3oS" style="left:820px;top:890px;width:190px;height:360px">__PO3__</div>
  <span class="chip a" id="f3il" style="left:310px;top:1180px;background:var(--amber);color:var(--ink)">ilustrasi dari pola</span>
</section>

<section class="sc" id="b4">
  <div class="a card" data-obj id="g4a" style="left:84px;top:430px;width:430px;height:520px"><div class="a mono" style="left:30px;top:34px;font-size:24px;color:var(--terra)">marketing</div><svg class="a" viewBox="0 0 200 140" style="left:60px;top:110px;width:310px;height:217px" fill="none" stroke="#0F0E0C" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"><path d="M16 120 L16 20 M16 120 H184"/><path d="M34 100 L80 66 L112 84 L170 30 M146 30 H170 V54" stroke="#B84A2E" stroke-width="12"/></svg><div class="a disp" style="left:30px;top:360px;font-size:84px">HASIL</div></div>
  <div class="a card" data-obj id="g4b" style="left:566px;top:430px;width:430px;height:520px"><div class="a mono" style="left:30px;top:34px;font-size:24px;color:var(--gray)">owner</div><svg class="a" viewBox="0 0 200 140" style="left:60px;top:110px;width:310px;height:217px" fill="none" stroke="#0F0E0C" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"><rect x="20" y="36" width="140" height="92" rx="16" fill="#fff"/><path d="M160 66 H184 V98 H160"/><path d="M90 6 V30 M70 16 L90 4 L110 16" stroke="#B84A2E" stroke-width="12"/></svg><div class="a disp" style="left:30px;top:340px;font-size:62px;line-height:1">UANG<br>KELUAR</div></div>
  <div class="a disp" id="g4n" style="left:0;right:0;top:985px;text-align:center;font-size:110px;color:#B84A2E">≠</div>
  <div class="a hand" id="g4h" style="left:0;right:0;top:1100px;text-align:center;font-size:92px">bahasanya aja beda</div>
</section>

<section class="sc" id="b5">
  <span class="chip a" id="p5c" style="left:84px;top:410px;background:var(--ink);color:#fff">kasus publik · 2010</span>
  <div class="a" id="p5e" style="left:90px;top:560px;width:380px;height:380px">__EMB1__</div>
  <div class="a" id="p5k" style="left:620px;top:480px;width:260px;height:520px">__CAN1__</div>
  <div class="a disp" id="p5t" style="left:0;right:0;top:1030px;text-align:center;font-size:96px">PEPSI</div>
  __DISCP__
</section>

<section class="sc" id="b6">
  <div class="a disp" id="s6h" style="left:84px;right:84px;top:420px;font-size:128px;line-height:.95">SUPER<br>BOWL 2010</div>
  <svg class="a" viewBox="0 0 1080 400" style="left:0;top:400px;width:1080px;height:400px" fill="none" stroke-linecap="round"><path id="s6x" d="M70 330 L1010 40" stroke="#B84A2E" stroke-width="18"/></svg>
  <div class="a" id="s6g" style="left:77px;top:760px;width:930px;height:340px"></div>
  <div class="a hand" id="s6t" style="left:0;right:0;top:1120px;text-align:center;font-size:84px">23 tahun beruntun, lalu absen</div>
</section>

<section class="sc" id="b7">
  <div class="a card" data-obj id="m7a" style="left:84px;top:430px;width:400px;height:520px"><div class="a mono" style="left:26px;top:30px;font-size:22px;color:var(--gray)">iklan super bowl</div><div class="a" style="left:60px;top:90px;width:260px;height:195px;transform:scale(.9);transform-origin:left top">__TV__</div><div class="a disp" style="left:26px;top:340px;font-size:62px;line-height:1">US$33 jt</div><div class="a" style="left:26px;top:420px;font:700 30px/1.2 var(--f-body);color:#6B6560">belanja tahun sebelumnya</div></div>
  <svg class="a" viewBox="0 0 1080 300" style="left:0;top:520px;width:1080px;height:300px" fill="none" stroke-linecap="round" stroke-linejoin="round"><path id="m7l" d="M490 150 L590 150 M562 118 L592 150 L562 182" stroke="#0F0E0C" stroke-width="10"/></svg>
  <div class="a" id="m7c0" style="left:500px;top:640px;width:36px;height:36px;border-radius:50%;background:#C8944A;border:5px solid #0F0E0C"></div><div class="a" id="m7c1" style="left:500px;top:640px;width:36px;height:36px;border-radius:50%;background:#C8944A;border:5px solid #0F0E0C"></div><div class="a" id="m7c2" style="left:500px;top:640px;width:36px;height:36px;border-radius:50%;background:#C8944A;border:5px solid #0F0E0C"></div>
  <div class="a card" data-obj id="m7b" style="left:596px;top:430px;width:400px;height:520px"><div class="a mono" style="left:26px;top:30px;font-size:22px;color:var(--terra)">kampanye sosial</div><div class="a" style="left:100px;top:90px;width:200px;height:200px">__EMB2__</div><div class="a disp" id="m7n" style="left:26px;top:340px;font-size:62px;line-height:1">± US$20 jt</div><div class="a" style="left:26px;top:420px;font:700 30px/1.2 var(--f-body);color:#6B6560">Pepsi Refresh Project</div></div>
  __DISCS__
</section>

<section class="sc" id="b8">
  <span class="chip a" id="r8c" style="left:84px;top:410px;background:var(--ink);color:#fff">biasanya dinilai dari</span>
  <div class="a card" data-obj id="r8a" style="left:84px;top:500px;width:430px;height:500px"><svg class="a" viewBox="0 0 200 160" style="left:60px;top:50px;width:310px;height:248px" fill="none" stroke="#0F0E0C" stroke-width="9" stroke-linejoin="round" stroke-linecap="round"><rect x="30" y="30" width="140" height="110" rx="14" fill="#fff"/><path d="M62 84 L90 112 L146 50" stroke="#B84A2E" stroke-width="16"/></svg><div class="a disp" style="left:30px;top:340px;font-size:50px;white-space:nowrap">PARTISIPASI</div></div>
  <div class="a card" data-obj id="r8b" style="left:566px;top:500px;width:430px;height:500px"><svg class="a" viewBox="0 0 200 160" style="left:60px;top:50px;width:310px;height:248px" fill="none" stroke="#0F0E0C" stroke-width="9" stroke-linejoin="round"><path d="M20 30 H130 V90 H70 L46 114 V90 H20Z" fill="#fff"/><path d="M80 110 H170 V160 H146 V178 L120 160 H80Z" fill="#C8944A" transform="translate(0,-26)"/></svg><div class="a disp" style="left:30px;top:340px;font-size:56px;white-space:nowrap">OBROLAN</div></div>
  __DISCP__
</section>

<section class="sc" id="b9">
  <div class="a" id="q9s" style="left:84px;top:430px;width:912px;height:400px"></div>
  <div class="a disp" id="q9h" style="left:84px;right:84px;top:880px;font-size:112px;line-height:.98">Berapa yang<br>terjual?</div>
  __DISCN__
</section>

<section class="sc" id="b10">
  <div class="a" id="k10a" data-obj style="left:84px;top:520px;width:300px;height:360px;border-radius:30px;background:var(--terra);color:#fff;box-shadow:var(--sh);display:flex;align-items:center;justify-content:center;text-align:center;font:800 52px/1.05 var(--f-display)">MARKE-<br>TING</div>
  <div class="a" id="k10b" data-obj style="left:696px;top:520px;width:300px;height:360px;border-radius:30px;background:#0F0E0C;color:#fff;box-shadow:var(--sh);display:flex;align-items:center;justify-content:center;font:800 56px/1.05 var(--f-display)">OWNER</div>
  <svg class="a" viewBox="0 0 1080 300" style="left:0;top:540px;width:1080px;height:300px" fill="none" stroke-linecap="round"><path id="k10l" d="M390 120 L470 120 M610 120 L690 120" stroke="#0F0E0C" stroke-width="12" stroke-dasharray="2 22"/></svg>
  <div class="a" id="k10p" data-obj style="left:420px;top:760px;width:210px;height:150px;background:#fff;border-radius:16px;box-shadow:var(--sh);display:flex;align-items:center;justify-content:center;font:800 40px/1 var(--f-display)">usulan</div>
  <div class="a disp" id="k10s" style="left:130px;top:960px;font-size:130px;color:#B84A2E;transform:rotate(-8deg);border:12px solid #B84A2E;border-radius:20px;padding:6px 30px;line-height:1">DITUNDA</div>
</section>

<section class="sc" id="b11">
  <div class="a" id="z11a" data-obj style="left:84px;top:520px;width:300px;height:360px;border-radius:30px;background:var(--terra);color:#fff;box-shadow:var(--sh);display:flex;align-items:center;justify-content:center;text-align:center;font:800 52px/1.05 var(--f-display)">MARKE-<br>TING</div>
  <div class="a" id="z11b" data-obj style="left:696px;top:520px;width:300px;height:360px;border-radius:30px;background:#0F0E0C;color:#fff;box-shadow:var(--sh);display:flex;align-items:center;justify-content:center;font:800 56px/1.05 var(--f-display)">OWNER</div>
  <div class="a" id="z11br" style="left:370px;top:620px;width:340px;height:40px;border-radius:8px;background:#C8944A;border:7px solid #0F0E0C;transform-origin:left"></div>
  <div class="a disp" id="z11i" style="left:370px;top:545px;width:340px;text-align:center;font-size:84px;color:#B84A2E;line-height:1">ICE</div>
  <span class="chip a" id="z11c" style="left:84px;top:960px;background:var(--ink);color:#fff">kerangka tim growth · Sean Ellis</span>
</section>

<section class="sc" id="b12">
  <div class="a" id="w12a" data-obj style="left:84px;top:450px;width:270px;height:300px;border-radius:30px;background:var(--terra);color:#fff;box-shadow:var(--sh);display:flex;align-items:center;justify-content:center;font:800 190px/1 var(--f-display)">I</div>
  <div class="a" id="w12b" data-obj style="left:405px;top:450px;width:270px;height:300px;border-radius:30px;background:#0F0E0C;color:#fff;box-shadow:var(--sh);display:flex;align-items:center;justify-content:center;font:800 190px/1 var(--f-display)">C</div>
  <div class="a" id="w12c" data-obj style="left:726px;top:450px;width:270px;height:300px;border-radius:30px;background:var(--amber);color:#0F0E0C;box-shadow:var(--sh);display:flex;align-items:center;justify-content:center;font:800 190px/1 var(--f-display)">E</div>
  <div class="a" id="w12r" style="left:84px;top:900px;width:912px;height:20px;border-radius:10px;background:#E8E1D5"></div>
  <div class="a" id="w12t" style="left:84px;top:940px;width:912px;height:60px"></div>
  <div class="a" id="w12m" style="left:84px;top:884px;width:52px;height:52px;border-radius:50%;background:#B84A2E;border:6px solid #0F0E0C"></div>
</section>
__C13__
__C14__
__C15__
__C16__
__C17__

<section class="sc" id="b18">
  <div class="a card" data-obj id="y18a" style="left:84px;top:410px;width:912px;height:330px"><div class="a disp" style="left:44px;top:40px;font-size:60px;color:#B84A2E;white-space:nowrap">REFRESH KONTEN LAMA</div><div class="a" style="left:44px;top:150px;font:700 44px/1.2 var(--f-body)">skor tertinggi</div><div class="a" id="y18b" style="left:470px;top:140px;padding:14px 30px;border-radius:999px;background:#0F0E0C;color:#fff;font:800 36px/1 var(--f-display);white-space:nowrap">1 · JALAN DULUAN</div><svg class="a" id="y18k" viewBox="0 0 80 80" style="left:44px;top:220px;width:80px;height:80px" fill="none" stroke="#B84A2E" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"><path id="y18kp" d="M14 42 L34 62 L68 18"/></svg></div>
  <div class="a card" data-obj id="y18c" style="left:84px;top:790px;width:912px;height:330px"><div class="a disp" style="left:44px;top:40px;font-size:60px;color:#0F0E0C;white-space:nowrap">KAMPANYE BARU</div><div class="a" style="left:44px;top:150px;font:700 44px/1.2 var(--f-body)">boleh maju, kalau dasarnya lebih kuat</div><div class="a" id="y18q" style="left:700px;top:30px;width:150px;height:150px">__MAG__</div></div>
</section>

<section class="sc" id="b19">
  <div class="a" style="left:0;top:0;width:1080px;height:1920px;background:var(--terra)"></div>
  <div class="a" id="e19s" data-obj style="left:440px;top:300px;width:200px;height:200px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 14px 0 rgba(15,14,12,.35)"><svg viewBox="0 0 24 24" width="96" height="96" fill="none" stroke="#B84A2E" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"><path d="M21 3L10 14M21 3l-7 18-4-7-7-4z"/></svg></div>
  <div class="a disp" id="e19h1" style="left:0;right:0;top:540px;text-align:center;font-size:120px;color:#fff;line-height:1">KIRIM KE TIM</div>
  <div class="a disp" id="e19h2" style="left:0;right:0;top:675px;text-align:center;font-size:86px;color:#0F0E0C;line-height:1">MARKETING KAMU</div>
  <div class="a" id="e19sub" style="left:96px;right:96px;top:830px;text-align:center;font:700 42px/1.25 var(--f-body);color:#fff">Minta tiap usulan datang dengan skor ICE.</div>
  <div class="a" id="e19p0" style="left:96px;top:950px;width:888px;height:96px;border-radius:999px;background:#fff;display:flex;align-items:center;padding-left:48px;font:800 46px/1 var(--f-display);color:#0F0E0C">I &nbsp;Impact</div>
  <div class="a" id="e19p1" style="left:96px;top:1060px;width:888px;height:96px;border-radius:999px;background:#fff;display:flex;align-items:center;padding-left:48px;font:800 46px/1 var(--f-display);color:#0F0E0C">C &nbsp;Confidence</div>
  <div class="a" id="e19p2" style="left:96px;top:1170px;width:888px;height:96px;border-radius:999px;background:#fff;display:flex;align-items:center;padding-left:48px;font:800 46px/1 var(--f-display);color:#0F0E0C">E &nbsp;Ease</div>
  <div class="a mono" id="e19h" style="left:0;right:0;top:1296px;text-align:center;font-size:34px;color:#fff;letter-spacing:.06em">@aldysyahreza</div>
</section>
'''
AV = '<svg viewBox="0 0 80 80" width="170" height="170"><circle cx="40" cy="40" r="38" fill="%s"/><circle cx="40" cy="31" r="13" fill="#0F0E0C"/><path d="M14 68 C16 50 64 50 66 68" fill="#0F0E0C"/></svg>'
MAG = '<svg viewBox="0 0 100 100" width="150" height="150" fill="none" stroke="#0F0E0C" stroke-width="9" stroke-linecap="round"><circle cx="42" cy="42" r="28" fill="#fff"/><path d="M64 64 L90 90"/><text x="42" y="54" text-anchor="middle" font-family="Archivo" font-weight="800" font-size="34" fill="#B84A2E" stroke="none">?</text></svg>'
for k, val in {'__REFRESH__': REFRESH, '__COINS__': COINS, '__AVM__': AV % '#B84A2E', '__AVO__': AV % '#C8944A', '__EMB1__': emblem(380, 'a'), '__EMB2__': emblem(200, 'b'), '__CAN1__': can(260, 'a'), '__TV__': TV, '__DISCP__': DISCP, '__DISCS__': DISCS, '__DISCN__': DISCN, '__MAG__': MAG, '__PM2__': person('p2m', '#B84A2E', '#8f3a24', '#2a1d14'), '__PO2__': person('p2o', '#0F0E0C', '#2a2622', '#6B6560', flip=True, tie=True), '__PM3__': person('p3m', '#B84A2E', '#8f3a24', '#2a1d14'), '__PO3__': person('p3o', '#0F0E0C', '#2a2622', '#6B6560', flip=True, tie=True)}.items():
    BODY = BODY.replace(k, val)
BODY = BODY.replace('__C13__', card('b13','1','#B84A2E','Impact','seberapa besar efeknya ke penjualan',BULL)).replace('__C14__', card('b14','2','#0F0E0C','Confidence','seberapa yakin tim, dan apa dasarnya',SHIELD,82)).replace('__C15__', card('b15','3','#C8944A','Ease','seberapa mudah dan cepat dikerjakan',WATCH))
BODY = BODY.replace('__C16__', scorecard('b16','REFRESH KONTEN LAMA','#B84A2E',[('IMPACT','6'),('CONFIDENCE','8'),('EASE','9')],'confidence tinggi: sudah pernah dibaca')).replace('__C17__', scorecard('b17','KAMPANYE BARU','#0F0E0C',[('IMPACT','8'),('CONFIDENCE','4'),('EASE','3')],'confidence rendah: belum pernah dicoba'))

OBJ = r"""
/* ---------- bangun objek ---------- */
(function(){var h='';for(var k=0;k<24;k++){var c=k%8,r=Math.floor(k/8),last=k===23;h+='<div class="a" id="s6c'+k+'" style="left:'+(c*118)+'px;top:'+(r*118)+'px;width:100px;height:100px;border-radius:18px;'+(last?'border:6px dashed #B84A2E;color:#B84A2E':'background:#B84A2E;color:#fff;box-shadow:var(--sh)')+';display:flex;align-items:center;justify-content:center;font:800 30px/1 var(--f-display)">'+(last?'2010':(k+1))+'</div>'}$('s6g').innerHTML=h})();
(function(){var h='';for(var k=0;k<6;k++){var c=k%3,r=Math.floor(k/3);h+='<div class="a" id="q9c'+k+'" style="left:'+(40+c*300)+'px;top:'+(r*200+10)+'px;width:130px;height:180px;display:flex;align-items:flex-end;justify-content:center"><div style="width:90px;height:180px">__CANS__</div></div>'}$('q9s').innerHTML=h})();
(function(){var h='';for(var k=1;k<=10;k++){h+='<div class="a mono" style="left:'+((k-1)*94-4)+'px;top:0;width:60px;text-align:center;font-size:26px;color:#6B6560">'+k+'</div>'}$('w12t').innerHTML=h})();
"""
OBJ = OBJ.replace('__CANS__', can(90, 'z').replace('"', '\\"').replace("'", "\\'").replace('\n', ''))
SCN = r"""
var DI=99,SCAN_A=0,SCAN_B=0;
function kcard(p,t,tt,ts,ti){var kc=E.out(pr(t,.05,.4));op($(p+'c'),cl(kc*3));tf($(p+'c'),'translateY('+((1-kc)*60)+'px)');up($(p+'t'),t,tt,.35,24);up($(p+'s'),t,ts,.4,24);up($(p+'i'),t,ti,.45,24)}
function sc(p,t,t0,vals,ts){var kc=E.out(pr(t,.05,.4));op($(p+'c'),cl(kc*3));tf($(p+'c'),'translateY('+((1-kc)*60)+'px)');up($(p+'t'),t,.1,.3,20);
  for(var i=0;i<3;i++){var f=E.io(pr(t,ts[i],.7)),b=$(p+'b'+i);tf(b,'scaleX('+(vals[i]/10*f)+')');b.style.transformOrigin='left';b.style.width='480px';op($(p+'n'+i),pr(t,ts[i]+.5,.25))}pop($(p+'il'),t,.3,.3);up($(p+'nt'),t,ts[2]+1.0,.4,20)}

function RT(id,a,cx,cy){var e=$(id);if(e)e.setAttribute('transform','rotate('+a.toFixed(2)+' '+cx+' '+cy+')')}
function BOB(u,t,amp){var e=$(u+'_b');if(e)e.setAttribute('transform','translate(0,'+(Math.sin(t*3.2)*amp).toFixed(2)+')')}
function LEGS(u,ph,amp){RT(u+'_ll',Math.sin(ph)*amp,86,216);RT(u+'_lr',-Math.sin(ph)*amp,114,216)}
function ARM(u,side,a){RT(u+'_'+side,a,side==='la'?73:127,134)}
function HEAD(u,a){RT(u+'_h',a,100,104)}
var S=[
 function(t){up($('a1l'),t,.25,.3,16);pop($('a1b'),t,.4,.45);tf($('a1b').firstChild,'rotate('+(t*120)+'deg)');up($('a1h'),t,3.0,.35,24);up($('a1l2'),t,4.0,.25,12);pop($('a1b2'),t,4.2,.45)},
 function(t){
   var ap=pr(t,.15,.35);op($('e2mS'),ap);op($('e2oS'),pr(t,.35,.35));op($('e2fl'),pr(t,.1,.3));op($('e2ml'),pr(t,.3,.3));op($('e2ol'),pr(t,.5,.3));
   var w=E.io(pr(t,1.7,1.1)),x=w*250,walking=t>1.7&&t<2.8;
   tf($('e2mS'),'translateX('+x+'px) translateY('+(ap<1?(1-ap)*30:0)+'px)');tf($('e2ml'),'translateX('+x+'px)');
   BOB('p2m',t,3);BOB('p2o',t+.7,3);LEGS('p2m',t*16,walking?24:0);LEGS('p2o',0,0);
   var hold=E.out(pr(t,1.5,.7)),drop=E.out(pr(t,3.1,.6));
   ARM('p2m','ra',-80*hold*(1-drop)+(Math.sin(t*2.4)*5));ARM('p2m','la',walking?Math.sin(t*16+3)*26:8+Math.sin(t*2)*4);
   var slump=E.out(pr(t,3.0,.6));HEAD('p2m',-18*slump+(t>1.7&&t<2.9?Math.sin(t*9)*4:0));
   var rj=E.out(pr(t,2.95,.35));ARM('p2o','ra',-105*rj);ARM('p2o','la',10);
   HEAD('p2o',t>2.95&&t<4.4?Math.sin((t-2.95)*17)*13*(1-pr(t,3.9,.5)):0);
   var pe=$('e2p'),back=E.out(pr(t,2.95,.5)),fall=E.out(pr(t,3.15,.6));
   op(pe,pr(t,1.45,.2));pe.style.left=(60+x+265-back*95)+'px';pe.style.top=(700+fall*110)+'px';tf(pe,'rotate('+(-8*hold-back*10-fall*10)+'deg)');
   pop($('e2x'),t,3.0,.4)},
 function(t){up($('f3l1'),t,.2,.25,12);pop($('f3b1'),t,.3,.45);up($('f3l2'),t,2.2,.25,12);pop($('f3b2'),t,2.35,.45);pop($('f3il'),t,3.6,.3);
   op($('f3mS'),pr(t,.1,.3));op($('f3oS'),pr(t,.1,.3));BOB('p3m',t,3);BOB('p3o',t+.5,3);
   var tm=t>.3&&t<2.1,to=t>2.35&&t<4.3;
   ARM('p3m','ra',tm?-50+Math.sin(t*9)*18:6);HEAD('p3m',tm?Math.sin(t*8)*6:0);ARM('p3m','la',8);
   ARM('p3o','ra',to?-35+Math.sin(t*8)*14:6);HEAD('p3o',to?Math.sin(t*7)*7:0);ARM('p3o','la',-20*(to?1:0))},
 function(t){pop($('g4a'),t,1.9,.45);pop($('g4b'),t,4.1,.45);pop($('g4n'),t,5.8,.4);up($('g4h'),t,6.8,.4,30);
   if(t<1.8){op($('g4a'),0);op($('g4b'),0)}},
 function(t){pop($('p5c'),t,.2,.3);pop($('p5e'),t,.3,.5);up($('p5k'),t,.8,.5,60);up($('p5t'),t,1.4,.4,30)},
 function(t){up($('s6h'),t,.2,.45,50);draw($('s6x'),t,1.0,.4);
   if(t>3.5){op($('s6h'),1-pr(t,3.5,.3));op($('s6x'),1-pr(t,3.5,.3))}
   for(var k=0;k<24;k++){var a=3.6+k*.035;if(k===23)a=4.5;pop($('s6c'+k),t,a,.28)}up($('s6t'),t,4.3,.3,24)},
 function(t){pop($('m7a'),t,.2,.45);draw($('m7l'),t,.8,.5);
   for(var k=0;k<3;k++){var f=((t*.8+k*.33)%1);op($('m7c'+k),(t>.8&&t<4.5)?1:0);tf($('m7c'+k),'translate('+(f*100)+'px,'+(-Math.sin(f*Math.PI)*60)+'px)')}
   pop($('m7b'),t,1.4,.5);up($('m7n'),t,2.7,.4,20)},
 function(t){pop($('r8c'),t,.2,.3);pop($('r8a'),t,1.3,.45);pop($('r8b'),t,2.2,.45)},
 function(t){var qs=$('q9s');for(var k=0;k<6;k++){pop($('q9c'+k),t,.3+k*.12,.3)}up($('q9h'),t,2.0,.45,40);
   for(var k=0;k<6;k++){var c=$('q9c'+k);c.style.filter=t>2.8?'grayscale(1) brightness(1.4)':'none';c.style.opacity=t>2.8?.35+.05*k:c.style.opacity}},
 function(t){pop($('k10a'),t,.1,.4);pop($('k10b'),t,.3,.4);draw($('k10l'),t,1.4,.5);pop($('k10p'),t,2.4,.4);
   var k=E.io(pr(t,2.5,.8));tf($('k10p'),'translateX('+(k*-60)+'px) rotate('+(k*-8)+'deg)');pop($('k10s'),t,3.7,.35)},
 function(t){pop($('z11a'),t,.1,.4);pop($('z11b'),t,.2,.4);var k=E.io(pr(t,.6,1.1));tf($('z11br'),'scaleX('+k+')');op($('z11br'),k>0?1:0);pop($('z11i'),t,2.9,.4);up($('z11c'),t,4.2,.35,20)},
 function(t){pop($('w12a'),t,.2,.4);pop($('w12b'),t,.5,.4);pop($('w12c'),t,.8,.4);op($('w12r'),pr(t,1.2,.3));op($('w12t'),pr(t,1.2,.3));
   var m=E.io(pr(t,1.5,.9));tf($('w12m'),'translateX('+(m*846)+'px)');op($('w12m'),pr(t,1.4,.2))},
 function(t){kcard('b13',t,1.0,1.3,.5);draw($('bul'),t,1.6,.5)},
 function(t){kcard('b14',t,1.0,1.8,.5);draw($('chk'),t,2.6,.4)},
 function(t){kcard('b15',t,1.1,1.6,.5);tf($('wh'),'rotate('+(t*200)+'deg)')},
 function(t){sc('b16',t,0,[6,8,9],[3.3,4.5,6.8])},
 function(t){sc('b17',t,0,[8,4,3],[1.3,2.5,4.7])},
 function(t){pop($('y18a'),t,.2,.45);pop($('y18b'),t,.7,.35);pop($('y18c'),t,2.0,.45);pop($('y18q'),t,4.0,.4);draw($('y18kp'),t,1.0,.4)},
 function(t){pop($('e19s'),t,.05,.45);up($('e19h1'),t,.2,.35,40);up($('e19h2'),t,.35,.35,40);up($('e19sub'),t,2.0,.35,30);[0,1,2].forEach(function(k){up($('e19p'+k),t,3.8+k*.3,.35,40)});op($('e19h'),pr(t,4.6,.4))}];
var TR=[null,'zoom','drop','whip','whip','drop','whip','drop','whip','drop','whip','whip','drop','drop','drop','whip','drop','drop','drop'];var TD=.42;
"""
JS = eng + OBJ + cap + SCN + fin
JS = JS.replace('__DEF__', DEF)
open(A + 'animatic-owner.html', 'w', encoding='utf-8').write(head + BODY + tail + JS)
anch = {"_petunjuk":"Adegan dimulai pada kata pembukanya.","scenes":[{"start":a,"act":b,"chap":c} for a,b,c in SC],"beats":[
 [[0.3,"marketing"],[3.3,"owner"],[4.3,"biaya"]],
 [[0.2,"di"],[1.7,"usulan"],[2.9,"mentok"]],
 [[0.2,"konten"],[2.2,"owner"]],
 [[0.2,"dua"],[1.9,"marketing"],[4.2,"owner"],[6.8,"bahasanya"]],
 [[0.2,"perusahaan"],[1.9,"begitu"]],
 [[0.2,"tahun"],[1.0,"melewatkan"],[3.7,"dalam"]],
 [[0.2,"dananya"],[1.4,"kampanye"],[2.7,"dua"]],
 [[0.2,"biasanya"],[1.4,"partisipasi"],[2.3,"obrolan"]],
 [[0.2,"tapi"],[2.0,"berapa"]],
 [[0.2,"kalau"],[1.4,"dijembatani"],[2.4,"usulan"],[3.7,"susah"]],
 [[0.2,"jembatannya"],[2.9,"ice"],[4.3,"sean"]],
 [[0.2,"ice"],[0.8,"tiga"],[1.5,"satu"],[2.3,"sepuluh"]],
 [[0.2,"pertama"],[1.0,"impact"]],
 [[0.2,"kedua"],[1.1,"confidence"],[2.0,"seberapa"]],
 [[0.2,"ketiga"],[1.0,"ease"]],
 [[0.2,"contohnya"],[2.1,"refresh"],[3.4,"impact"],[4.5,"confidence"],[6.9,"ease"]],
 [[0.2,"kampanye"],[1.3,"impact"],[2.5,"confidence"],[4.7,"ease"]],
 [[0.2,"refresh"],[2.0,"kampanye"],[3.5,"kalau"]],
 [[0.2,"kirim"],[2.0,"minta"],[4.6,"skor"]]]}
json.dump(anch, open(A + 'anchors-owner.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok')
