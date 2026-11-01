import json
A = '/home/user/content-studio/animatic/'
v3 = open(A + 'animatic-v3.html', encoding='utf-8').read()
head = v3[:v3.index('<div class="bgpaper" id="bgp"></div>')]
head = head.replace('<title>Animatic v3 The Brand Fixer</title>', '<title>Animatic: finance vs marketing, cerita dari meja meeting</title>')
tail = v3[v3.index('<div id="scan">'):v3.index('<script>')]
DUR = [4.6,3.55,7.38,1.65,7.11,9.27,8.35,8.65,3.96,4.5,3.67,7.61,5.51,8.4,3.6]
SC = [("finance","HOOK",1),("di","RELATE",2),("finance","RELATE",2),("duaduanya","INSIGHT",3),("di","INSIGHT",3),("hasilnya","INSIGHT",3),("tapi","INSIGHT",3),("biasanya","REFRAME",4),("pertama","REFRAME",4),("kedua","REFRAME",4),("ketiga","REFRAME",4),("contohnya","REFRAME",4),("kalo","REFRAME",4),("kirim","CTA",5),("berikutnya","CTA",5)]
SAY = ['Finance dan marketing berdebat. Dan dua-duanya bener.','Di bisnis yang saya dampingi, adegannya hampir selalu sama.','Finance: Budget iklan mau naik? Hasilnya aja belum jelas. Marketing: Kalo gak dicoba, kapan kita tahu?','Dua-duanya masuk akal.','Di film AIR, Nike digambarkan ketinggalan dari Adidas dan Converse, lalu taruhan ke satu pemain muda.','Hasilnya, penjualan tahun pertama Air Jordan dilaporkan sekitar 126 juta dolar, dan sekarang Jordan Brand masih di atas 7 miliar dolar setahun.','Tapi kita tahu cerita ini karena Nike menang. Taruhan yang kalah gak dibikin film.','Biasanya debat ini selesai bukan karena ada yang menang. Mereka duduk bareng dan sepakat tiga hal. Saya sebut ini coordination system.','Pertama, cara ngukurnya: angka apa yang jadi patokan.','Kedua, batas ruginya: uang yang boleh hilang kalo percobaannya gagal.','Ketiga, tanggal ngecek: kapan hasilnya dibahas bareng.','Contohnya tes iklan dua minggu: ukurannya biaya per pesanan, batas ruginya lima juta, dicek tanggal yang udah ditentukan.','Kalo bagus, lanjut. Kalo kena batas rugi, stop, tanpa saling nyalahin.','Kirim ke tim internal kamu: finance, marketing, dan yang pegang keputusan. Duduk bareng sepuluh menit, dan tentukan tiga kesepakatan itu buat percobaan berikutnya.','percobaan berikutnya.']
DEF = ',\n  '.join("{dur:%s,name:'%s',chap:%d,say:%s}" % (DUR[i], SC[i][1], SC[i][2], json.dumps(SAY[i], ensure_ascii=False)) for i in range(len(DUR)))
AVT = '<svg viewBox="0 0 80 80" width="%d" height="%d"><circle cx="40" cy="40" r="38" fill="%s"/><circle cx="40" cy="31" r="13" fill="#0F0E0C"/><path d="M14 68 C16 50 64 50 66 68" fill="#0F0E0C"/></svg>'
SHOE = '<svg viewBox="0 0 200 120" style="display:block;overflow:visible"><path d="M10 82 Q10 62 30 60 L70 52 Q85 26 112 32 L150 56 Q186 62 192 86 L192 96 L10 96Z" fill="%s" stroke="#0F0E0C" stroke-width="5" stroke-linejoin="round"/><path d="M10 96 L192 96 L192 106 Q192 114 182 114 L20 114 Q10 114 10 106Z" fill="#0F0E0C"/></svg>'
DISC = '<div class="mono" style="position:absolute;left:96px;right:96px;top:1265px;font-size:19px;letter-spacing:.04em;color:#6B6560;text-transform:none;line-height:1.3">Logo dan foto milik pemiliknya. Akun ini tidak berafiliasi dengan Nike, Adidas, atau Converse.</div>'

BODY = r'''<div class="bgpaper" id="bgp"></div><div class="bgdx" id="bgd"></div>

<!-- 1 HOOK -->
<section class="sc" id="b1">
  <div class="a card" data-obj id="h1f" style="left:84px;top:470px;width:420px;height:560px"><div class="a" style="left:130px;top:90px;width:160px"><svg viewBox="0 0 80 100" width="160" height="200"><rect x="6" y="6" width="68" height="88" rx="10" fill="#fff" stroke="#0F0E0C" stroke-width="5"/><rect x="16" y="16" width="48" height="20" rx="4" fill="#0F0E0C"/><g fill="#6B6560"><rect x="16" y="46" width="12" height="12" rx="2"/><rect x="34" y="46" width="12" height="12" rx="2"/><rect x="52" y="46" width="12" height="12" rx="2"/><rect x="16" y="66" width="12" height="12" rx="2"/><rect x="34" y="66" width="12" height="12" rx="2"/><rect x="52" y="66" width="12" height="12" rx="2" fill="#B84A2E"/></g></svg></div><div class="a disp" style="left:0;right:0;top:400px;text-align:center;font-size:62px">FINANCE</div><div class="a mono" style="left:0;right:0;top:480px;text-align:center;color:var(--gray);font-size:22px">jaga cashflow</div></div>
  <div class="a" data-obj id="h1m" style="left:576px;top:470px;width:420px;height:560px;border-radius:34px;background:var(--terra);box-shadow:var(--sh);color:#fff"><div class="a" style="left:100px;top:100px;width:220px"><svg viewBox="0 0 100 80" width="220" height="176" fill="none" stroke="#fff" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"><path d="M12 30 L48 30 L84 8 L84 72 L48 50 L12 50Z" fill="#FFE2B0" stroke="#0F0E0C"/><path d="M22 50 L28 72 L40 72 L36 50" stroke="#0F0E0C" fill="#fff"/></svg></div><div class="a disp" style="left:0;right:0;top:400px;text-align:center;font-size:62px">MARKETING</div><div class="a mono" style="left:0;right:0;top:480px;text-align:center;color:#FFE2B0;font-size:22px">berani nyoba</div></div>
  <svg class="a" viewBox="0 0 1080 1920" style="left:0;top:0;width:1080px;height:1920px" fill="none" stroke-linecap="round" stroke-linejoin="round"><path id="h1z" d="M510 700 L545 650 L520 750 L560 700 L535 800" stroke="#B84A2E" stroke-width="12"/><path id="h1c1" d="M244 1070 L284 1110 L344 1040" stroke="#B84A2E" stroke-width="14"/><path id="h1c2" d="M736 1070 L776 1110 L836 1040" stroke="#0F0E0C" stroke-width="14"/></svg>
</section>

<!-- 2 RELATE a: rapat -->
<section class="sc" id="b2">
  <div class="a mono" id="r2lab" style="left:84px;top:400px;color:var(--terra)">rapat sore</div>
  <div class="a card" data-obj id="r2card" style="left:84px;top:470px;width:912px;height:560px">
    <svg class="a" viewBox="0 0 912 560" style="left:0;top:0;width:912px;height:560px" fill="none" stroke-linecap="round" stroke-linejoin="round">
      <rect x="110" y="290" width="692" height="40" rx="14" fill="#C79A5E" stroke="#0F0E0C" stroke-width="6"/><path d="M170 330 L170 470 M742 330 L742 470" stroke="#0F0E0C" stroke-width="8"/>
      <g stroke="#0F0E0C" stroke-width="6"><path d="M240 250 L340 250 L360 290 L220 290Z" fill="#fff"/><path d="M572 250 L672 250 L692 290 L552 290Z" fill="#fff"/></g>
      <circle cx="290" cy="150" r="46" fill="#C8944A" stroke="#0F0E0C" stroke-width="6"/><path d="M200 250 C210 190 370 190 380 250" fill="#0F0E0C"/>
      <circle cx="622" cy="150" r="46" fill="#B84A2E" stroke="#0F0E0C" stroke-width="6"/><path d="M532 250 C542 190 702 190 712 250" fill="#0F0E0C"/>
    </svg>
    <div class="a mono" style="left:200px;top:500px;font-size:22px">finance</div><div class="a mono" style="left:560px;top:500px;font-size:22px">marketing</div>
  </div>
  <span class="chip a" id="r2il" style="left:84px;top:1070px;background:var(--amber);color:var(--ink)">ilustrasi dari pola</span>
</section>

<!-- 3 RELATE b: dialog -->
<section class="sc" id="b3">
  <div class="a" id="r3a" style="left:84px;top:380px;width:830px">
    <div class="a mono" style="left:0;top:0;color:var(--gray);font-size:22px">finance</div>
    <div class="a" style="left:0;top:40px;width:96px;height:96px">__AF__</div>
    <div class="a" id="r3b1" style="left:124px;top:36px;width:700px;padding:30px 38px;border-radius:36px 36px 36px 10px;background:#fff;box-shadow:0 10px 0 rgba(15,14,12,.9);font:700 44px/1.2 var(--f-body)"><span id="r3t1">“Budget iklan mau naik?</span> <span id="r3t2">Hasilnya aja belum jelas.”</span></div>
  </div>
  <div class="a" id="r3b" style="left:84px;top:840px;width:912px">
    <div class="a mono" style="right:0;top:0;color:var(--gray);font-size:22px;text-align:right;left:0">marketing</div>
    <div class="a" style="right:0;top:40px;width:96px;height:96px;left:816px">__AM__</div>
    <div class="a" id="r3b2" style="left:92px;top:36px;width:700px;padding:30px 38px;border-radius:36px 36px 10px 36px;background:#0F0E0C;color:#fff;box-shadow:0 10px 0 var(--terra);font:700 44px/1.2 var(--f-body)">“Kalo gak dicoba, kapan kita tahu?”</div>
  </div>
  <span class="chip a" id="r3il" style="left:84px;top:1120px;background:var(--amber);color:var(--ink)">ilustrasi dari pola</span>
</section>

<!-- 4 INSIGHT a: dua-duanya masuk akal -->
<section class="sc" id="b4">
  <svg class="a" viewBox="0 0 1080 700" style="left:0;top:420px;width:1080px;height:700px" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M540 120 L540 600" stroke="#0F0E0C" stroke-width="12"/><path d="M360 620 L720 620" stroke="#0F0E0C" stroke-width="14"/>
    <g id="s4beam"><path d="M180 150 L900 150" stroke="#0F0E0C" stroke-width="14"/>
    <path d="M180 150 L120 330 L320 330 Z" fill="#fff" stroke="#0F0E0C" stroke-width="8"/><path d="M900 150 L840 330 L1040 330 Z" fill="#fff" stroke="#0F0E0C" stroke-width="8"/></g>
  </svg>
  <div class="a disp" id="s4f" style="left:110px;top:760px;font-size:50px">FINANCE</div><div class="a disp" id="s4m" style="left:700px;top:760px;font-size:50px">MARKETING</div>
  <div class="a" id="s4ok" style="left:440px;top:1020px;width:200px;height:200px;border-radius:50%;background:var(--terra);display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 80 80" width="110" height="110" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"><path d="M18 42 L34 58 L64 22"/></svg></div>
</section>

<!-- 5 INSIGHT b: film AIR, tiga merek -->
<section class="sc" id="b5">
  <div class="a chip" id="s5chip" style="left:84px;top:300px;background:var(--ink);color:#fff">film AIR · dramatisasi</div>
  <div class="a" id="s5photo" data-obj style="__PHSTYLE__"><div style="__PHINNER__"></div><i style="position:absolute;left:50%;top:-16px;width:140px;height:34px;margin-left:-70px;background:rgba(200,148,74,.6);transform:rotate(-3deg)"></i></div>
  <div class="a" id="s5bars"></div>
  <div class="a hand" id="s5nt" style="left:90px;top:760px;font-size:56px;transform:rotate(-3deg)">tertinggal</div>
  __DISC__
</section>

<!-- 6 INSIGHT c: hasil -->
<section class="sc" id="b6">
  <div class="a card" data-obj id="s6a" style="left:84px;top:380px;width:912px;height:380px">
    <div class="a mono" style="left:44px;top:40px;color:var(--gray)">tahun pertama · 1985</div><span class="chip a" id="s6ca" style="right:44px;top:30px;background:var(--amber);color:var(--ink)">dilaporkan</span>
    <div class="a disp" style="left:44px;top:140px;font-size:150px;white-space:nowrap"><span style="font-size:80px">US$</span><span class="odo" id="s6odo"></span><span style="font-size:70px"> juta</span></div>
  </div>
  <div class="a" data-obj id="s6b" style="left:84px;top:820px;width:912px;height:400px;border-radius:34px;background:linear-gradient(150deg,#2b2824,#0F0E0C);box-shadow:var(--sh);color:#fff">
    <div class="a mono" style="left:44px;top:40px;color:#FFE2B0">sekarang · jordan brand</div><span class="chip a" style="right:44px;top:30px;background:var(--terra);color:#fff">laporan tahunan FY2025</span>
    <div class="a disp" id="s6big" style="left:44px;top:140px;font-size:150px;white-space:nowrap"><span style="font-size:80px">US$</span>7<span style="font-size:70px"> miliar+</span></div>
  </div>
  __DISC__
</section>

<!-- 7 INSIGHT d: yang kalah gak difilmkan (diagnosis) -->
<section class="sc" id="b7">
  <div class="a mono" id="s7lab" style="left:84px;top:400px;color:var(--gray)">taruhan yang kita tahu</div>
  <div id="s7g"></div>
  <div class="a hand" id="s7h" style="left:84px;top:1060px;font-size:84px;color:#FFE2B0;transform:rotate(-2deg);white-space:nowrap">yang kalah gak difilmkan</div>
</section>

<!-- 8 REFRAME a: duduk bareng, tiga kesepakatan -->
<section class="sc" id="b8">
  <div class="a" data-obj id="t8f" style="left:84px;top:380px;width:380px;height:190px;border-radius:30px;background:#fff;box-shadow:var(--sh);display:flex;align-items:center;justify-content:center"><span class="disp" style="font-size:54px">FINANCE</span></div>
  <div class="a" data-obj id="t8m" style="left:616px;top:380px;width:380px;height:190px;border-radius:30px;background:var(--terra);color:#fff;box-shadow:var(--sh);display:flex;align-items:center;justify-content:center"><span class="disp" style="font-size:54px">MARKETING</span></div>
  <div class="a" data-obj id="t8t" style="left:190px;top:830px;width:700px;height:460px;border-radius:50%;background:#F4EBD9;box-shadow:var(--sh),inset 0 0 0 8px #0F0E0C"></div>
  <div class="a" id="t8s" style="left:0;top:0;width:1080px;height:1920px"></div>
  <div class="a" id="t8stamp" style="left:140px;top:720px;transform-origin:center"><div style="border:8px solid var(--terra);color:var(--terra);border-radius:16px;padding:12px 26px;font:800 56px/1 var(--f-display);white-space:nowrap;background:rgba(251,248,243,.92)">COORDINATION SYSTEM</div></div>
</section>

<!-- 9-11 tiga kesepakatan -->
<section class="sc" id="b9">__KC9__</section>
<section class="sc" id="b10">__KC10__</section>
<section class="sc" id="b11">__KC11__</section>

<!-- 12 contoh tes iklan -->
<section class="sc" id="b12">
  <span class="chip a" id="c12chip" style="left:84px;top:330px;background:var(--amber);color:var(--ink)">contoh · ilustrasi</span>
  <div class="a mono" id="c12t" style="left:84px;top:400px;color:var(--terra)">tes iklan 2 minggu</div>
  <svg class="a" viewBox="0 0 1080 120" style="left:0;top:450px;width:1080px;height:120px" fill="none" stroke-linecap="round"><path id="c12l" d="M100 70 L980 70" stroke="#0F0E0C" stroke-width="10"/><g stroke="#0F0E0C" stroke-width="8"><path d="M100 40 L100 100"/><path d="M540 52 L540 88"/><path d="M980 40 L980 100"/></g></svg>
  <div class="a mono" style="left:84px;top:575px;font-size:20px;color:var(--gray)">hari 1</div><div class="a mono" style="left:880px;top:575px;font-size:20px;color:var(--gray)">hari 14</div>
  <div id="c12r"></div>
</section>

<!-- 13 lanjut atau stop -->
<section class="sc" id="b13">
  <div class="a card" data-obj id="f13a" style="left:84px;top:430px;width:430px;height:560px"><div class="a mono" style="left:0;right:0;top:40px;text-align:center;color:var(--gray)">kalo bagus</div><svg class="a" viewBox="0 0 100 100" style="left:105px;top:130px;width:220px;height:220px" fill="none" stroke-linecap="round" stroke-linejoin="round"><circle cx="50" cy="50" r="46" fill="#C8944A" stroke="#0F0E0C" stroke-width="5"/><path id="f13u" d="M50 72 L50 28 M30 48 L50 28 L70 48" stroke="#0F0E0C" stroke-width="9"/></svg><div class="a disp" id="f13l" style="left:0;right:0;top:400px;text-align:center;font-size:84px">LANJUT</div></div>
  <div class="a card" data-obj id="f13b" style="left:566px;top:430px;width:430px;height:560px"><div class="a mono" style="left:0;right:0;top:40px;text-align:center;color:var(--gray)">kena batas rugi</div><svg class="a" viewBox="0 0 100 100" style="left:105px;top:130px;width:220px;height:220px"><polygon points="32,6 68,6 94,32 94,68 68,94 32,94 6,68 6,32" fill="#B84A2E" stroke="#0F0E0C" stroke-width="5" stroke-linejoin="round"/><rect x="26" y="42" width="48" height="16" fill="#fff"/></svg><div class="a disp" id="f13s" style="left:0;right:0;top:400px;text-align:center;font-size:84px;color:var(--terra)">STOP</div></div>
  <div class="a hand" id="f13h" style="left:84px;top:1060px;font-size:78px;transform:rotate(-2deg)">tanpa saling nyalahin</div>
</section>

<!-- 14 CTA -->
<section class="sc" id="b14">
  <div class="a" id="k14send" data-obj style="left:84px;top:380px;width:200px;height:200px;border-radius:50%;background:var(--terra);display:flex;align-items:center;justify-content:center;box-shadow:var(--sh)"><svg viewBox="0 0 24 24" width="96" height="96" fill="none" stroke="#fff" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"><path d="M21 3L10 14M21 3l-7 18-4-7-7-4z"/></svg></div>
  <svg class="a" viewBox="0 0 1080 300" style="left:0;top:390px;width:1080px;height:300px" fill="none" stroke-linecap="round"><path id="k14a" d="M300 100 L370 100" stroke="#0F0E0C" stroke-width="6" stroke-dasharray="4 14"/></svg>
  <div class="a" id="k14av" style="left:370px;top:370px;width:630px;height:260px"></div>
  <div class="a card" data-obj id="k14card" style="left:84px;top:700px;width:912px;height:520px">
    <div class="a mono" style="left:44px;top:36px;color:var(--gray)">tentukan bareng</div><span class="chip a" id="k14chip" style="right:44px;top:26px;background:var(--ink);color:#fff">10 menit</span>
    <div id="k14rows"></div>
  </div>
</section>

<!-- 15 END CARD CTA -->
<section class="sc" id="b15">
  <div class="a" style="left:0;top:0;width:1080px;height:1920px;background:var(--terra)"></div>
  <div class="a" id="e15send" data-obj style="left:440px;top:330px;width:200px;height:200px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 14px 0 rgba(15,14,12,.35)"><svg viewBox="0 0 24 24" width="96" height="96" fill="none" stroke="#B84A2E" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"><path d="M21 3L10 14M21 3l-7 18-4-7-7-4z"/></svg></div>
  <div class="a disp" id="e15h1" style="left:0;right:0;top:600px;text-align:center;font-size:120px;color:#fff;line-height:1">KIRIM KE TIM</div>
  <div class="a disp" id="e15h2" style="left:0;right:0;top:730px;text-align:center;font-size:120px;color:#0F0E0C;line-height:1">INTERNAL KAMU</div>
  <div class="a" id="e15sub" style="left:96px;right:96px;top:900px;text-align:center;font:700 44px/1.25 var(--f-body);color:#fff">Duduk bareng 10 menit, tentukan 3 kesepakatan ini.</div>
  <div class="a" id="e15p0" style="left:96px;top:1060px;width:888px;height:110px;border-radius:999px;background:#fff;display:flex;align-items:center;padding-left:48px;font:800 48px/1 var(--f-display);color:#0F0E0C">1 &nbsp;Cara ngukur</div>
  <div class="a" id="e15p1" style="left:96px;top:1190px;width:888px;height:110px;border-radius:999px;background:#fff;display:flex;align-items:center;padding-left:48px;font:800 48px/1 var(--f-display);color:#0F0E0C">2 &nbsp;Batas rugi</div>
  <div class="a" id="e15p2" style="left:96px;top:1320px;width:888px;height:110px;border-radius:999px;background:#fff;display:flex;align-items:center;padding-left:48px;font:800 48px/1 var(--f-display);color:#0F0E0C">3 &nbsp;Tanggal cek</div>
  <div class="a mono" id="e15h" style="left:0;right:0;top:1500px;text-align:center;font-size:34px;color:#fff;letter-spacing:.06em">@aldysyahreza</div>
</section>
'''
def kc(p,num,col,title,sub,icon):
    return ('<div class="a card" data-obj id="%scard" style="left:84px;top:400px;width:912px;height:760px">'
            '<div class="a" style="left:44px;top:50px;width:170px;height:170px;border-radius:50%%;background:%s;color:#fff;display:flex;align-items:center;justify-content:center;font:800 100px/1 var(--f-display)">%s</div>'
            '<div class="a disp" id="%st" style="left:250px;top:84px;font-size:92px;white-space:nowrap">%s</div>'
            '<div class="a" id="%ss" style="left:44px;top:290px;width:824px;font:700 52px/1.22 var(--f-body)">%s</div>'
            '<div class="a" id="%si" style="left:44px;top:500px;width:824px;height:220px">%s</div></div>') % (p,col,num,p,title,p,sub,p,icon)
ICON1='<svg viewBox="0 0 824 220" width="824" height="220" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M20 190 L804 190" stroke="#0F0E0C" stroke-width="8"/><g stroke="#0F0E0C" stroke-width="6"><path d="M60 190 L60 150 M120 190 L120 170 M180 190 L180 150 M240 190 L240 170 M300 190 L300 150 M360 190 L360 170 M420 190 L420 150 M480 190 L480 170 M540 190 L540 150 M600 190 L600 170 M660 190 L660 150"/></g><circle cx="560" cy="70" r="46" stroke="#B84A2E" stroke-width="10"/><circle cx="560" cy="70" r="12" fill="#B84A2E"/><path d="M560 70 L760 20" stroke="#B84A2E" stroke-width="8"/></svg>'
ICON2='<svg viewBox="0 0 824 220" width="824" height="220" fill="none" stroke-linecap="round" stroke-linejoin="round"><rect x="20" y="70" width="784" height="80" rx="40" fill="#F4EBD9" stroke="#0F0E0C" stroke-width="8"/><rect x="24" y="74" width="470" height="72" rx="36" fill="#C8944A"/><path d="M600 30 L600 190" stroke="#B84A2E" stroke-width="12"/><path d="M570 40 L600 20 L630 40" stroke="#B84A2E" stroke-width="8"/></svg>'
ICON3='<svg viewBox="0 0 824 220" width="824" height="220" fill="none" stroke-linecap="round" stroke-linejoin="round"><rect x="260" y="20" width="300" height="190" rx="22" fill="#fff" stroke="#0F0E0C" stroke-width="8"/><rect x="260" y="20" width="300" height="56" rx="22" fill="#B84A2E" stroke="#0F0E0C" stroke-width="8"/><g fill="#0F0E0C"><circle cx="320" cy="116" r="9"/><circle cx="380" cy="116" r="9"/><circle cx="440" cy="116" r="9"/><circle cx="500" cy="116" r="9"/><circle cx="320" cy="164" r="9"/><circle cx="380" cy="164" r="9"/></g><circle cx="440" cy="164" r="22" stroke="#B84A2E" stroke-width="7"/></svg>'
BODY = BODY.replace('__KC9__',kc('k9','1','#B84A2E','Cara ngukur','angka apa yang jadi patokan',ICON1)).replace('__KC10__',kc('k10','2','#0F0E0C','Batas rugi','uang yang boleh hilang kalo percobaannya gagal',ICON2)).replace('__KC11__',kc('k11','3','#C8944A','Tanggal cek','kapan hasilnya dibahas bareng',ICON3))
import os
HIRES=os.path.exists('/home/user/content-studio/foto/aset/jordan-hires.jpg')
if HIRES:
    PHS="left:84px;top:430px;width:912px;height:700px;background:#fff;padding:14px;box-shadow:0 22px 36px rgba(15,14,12,.3);transform:rotate(-2deg)"
    PHI="width:884px;height:672px;background:url('../foto/aset/jordan-hires.jpg') center/cover"
else:
    PHS="left:716px;top:310px;width:270px;height:380px;background:#fff;padding:12px;box-shadow:0 18px 30px rgba(15,14,12,.25);transform:rotate(4deg)"
    PHI="width:246px;height:356px;background:url('../foto/aset/jordan-kiri.jpg') center/cover"
BODY = BODY.replace('__PHSTYLE__',PHS).replace('__PHINNER__',PHI)
BODY = BODY.replace('__AF__',AVT%(96,96,'#C8944A')).replace('__AM__',AVT%(96,96,'#B84A2E')).replace('__DISC__',DISC)

JS = r'''
<script>
(function(){
'use strict';
var DEF=[
  __DEF__];
var BEATS=window.ANIMATIC_BEATS?DEF.map(function(d,i){return Object.assign({},d,window.ANIMATIC_BEATS[i]||{})}):DEF;
var SPEED=BEATS.map(function(b,i){return Math.max(1,DEF[i].dur/b.dur)});
var T0=[],acc=0;BEATS.forEach(function(b){T0.push(acc);acc+=b.dur});window.ANIMATIC_DURATION=acc;
var ANCH=(window.ANIMATIC_ANCHORS||{}).beats||[];
function nrm(s){return String(s).toLowerCase().replace(/[^a-z0-9]/g,'')}
var WARP=BEATS.map(function(b,i){var pts=[[0,0]];if(!b.words||!ANCH[i])return null;var from=0;
  ANCH[i].forEach(function(a){for(var k=from;k<b.words.length;k++){if(nrm(b.words[k].w).indexOf(a[1])===0){var r=b.words[k].t-T0[i],l=pts[pts.length-1];if(r>l[1]+.05&&a[0]>l[0])pts.push([a[0],r]);from=k+1;break}}});
  return pts.length>1?pts:null});
function LOCAL(i,lt){var p=WARP[i];if(!p)return lt*SPEED[i];
  for(var k=1;k<p.length;k++)if(lt<=p[k][1])return p[k-1][0]+(lt-p[k-1][1])*(p[k][0]-p[k-1][0])/(p[k][1]-p[k-1][1]);
  var L=p[p.length-1],tail=Math.max(1,(DEF[i].dur-L[0])/Math.max(.3,BEATS[i].dur-L[1]));return L[0]+(lt-L[1])*tail}
function $(id){return document.getElementById(id)}
function cl(x){return x<0?0:x>1?1:x}
function pr(t,a,d){return cl((t-a)/d)}
var E={out:function(t){return 1-Math.pow(1-t,3)},io:function(t){return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2},
  back:function(t){var c=1.70158;return 1+(c+1)*Math.pow(t-1,3)+c*Math.pow(t-1,2)}};
function op(el,v){el.style.opacity=v}
function tf(el,s){el.style.transform=s}
function up(el,t,a,d,dist){var k=E.out(pr(t,a,d||.45));op(el,k);tf(el,'translateY('+((1-k)*(dist==null?60:dist))+'px)')}
function pop(el,t,a,d,extra){var k=pr(t,a,d||.5);op(el,cl(k*4));tf(el,'scale('+(k?E.back(k):.4)+')'+(extra||''))}
function draw(p,t,a,d){var L=p.getTotalLength();p.style.strokeDasharray=L;p.style.strokeDashoffset=L*(1-E.io(pr(t,a,d)));p.style.opacity=t>=a?1:0}
function odo(el,digits){el.innerHTML='';for(var i=0;i<digits;i++){var c=document.createElement('i'),s=document.createElement('s');s.innerHTML='0<br>1<br>2<br>3<br>4<br>5<br>6<br>7<br>8<br>9<br>0';c.appendChild(s);el.appendChild(c)}}
function odoSet(el,v){var n=el.children.length,str=String(Math.max(0,Math.round(v))).padStart(n,' ');v=Math.max(0,Math.round(v));for(var i=0;i<n;i++){var ch=str[i],c=el.children[i];if(ch===' '){c.style.display='none';continue}c.style.display='block';
  var place=Math.pow(10,n-1-i),d=Math.floor(v/place)%10;tf(c.firstChild,'translateY('+(-d*100/11)+'%)')}}

/* ---------- bangun objek ---------- */
var HIRESJS=__HIRES__;
odo($('s6odo'),3);
var LOGO={conv:'../foto/aset/converse.png',adi:'../foto/aset/adidas.png',nike:'../foto/aset/nike-swoosh.png'};
$('s5bars').innerHTML=[['conv',84,520,'Converse'],['adi',410,420,'Adidas'],['nike',736,300,'Nike']].map(function(b,k){return '<div class="a" id="s5b'+k+'" style="left:'+b[1]+'px;top:'+(1170-b[2])+'px;width:260px;height:'+b[2]+'px;background:'+['#0F0E0C','#C8944A','#B84A2E'][k]+';border-radius:22px 22px 0 0;box-shadow:var(--sh)"></div><div class="a" id="s5l'+k+'" data-obj style="left:'+b[1]+'px;top:'+(1170-b[2]-150)+'px;width:260px;height:130px;background:#fff;border-radius:22px;box-shadow:var(--sh);display:flex;align-items:center;justify-content:center"><img src="'+LOGO[b[0]]+'" style="max-width:190px;max-height:90px;object-fit:contain" alt=""></div>'}).join('');
(function(){var h='';for(var k=0;k<8;k++){var c=k%4,r=Math.floor(k/4);h+='<div class="a card" data-obj id="s7t'+k+'" style="left:'+(78+c*238)+'px;top:'+(470+r*290)+'px;width:210px;height:250px;border-radius:26px"><div class="a" style="left:20px;top:80px;width:170px">'+'<svg viewBox="0 0 200 120" style="display:block;overflow:visible"><path d="M10 82 Q10 62 30 60 L70 52 Q85 26 112 32 L150 56 Q186 62 192 86 L192 96 L10 96Z" fill="'+(k===2?'#B84A2E':'#E2C592')+'" stroke="#0F0E0C" stroke-width="5" stroke-linejoin="round"/><path d="M10 96 L192 96 L192 106 Q192 114 182 114 L20 114 Q10 114 10 106Z" fill="#0F0E0C"/></svg></div>'+(k===2?'<img src="'+LOGO.nike+'" style="position:absolute;left:55px;top:16px;width:100px" alt="">':'')+'<div class="a disp" id="s7q'+k+'" style="left:0;right:0;top:150px;text-align:center;font-size:96px;color:#FFE2B0;opacity:0">?</div></div>'}$('s7g').innerHTML=h})();
(function(){var h='',pos=[[300,1130],[540,1030],[780,1130]],cols=['#B84A2E','#0F0E0C','#C8944A'];pos.forEach(function(q,k){h+='<div class="a" id="t8n'+k+'" style="left:'+(q[0]-70)+'px;top:'+(q[1]-70)+'px;width:140px;height:140px;border-radius:50%;background:'+cols[k]+';color:'+(k===2?'#0F0E0C':'#fff')+';display:flex;align-items:center;justify-content:center;font:800 70px/1 var(--f-display);box-shadow:var(--sh)">'+(k+1)+'</div>'});$('t8s').innerHTML=h})();
var C12=[['Ukuran','biaya per pesanan','#B84A2E'],['Batas rugi','Rp5 juta','#0F0E0C'],['Cek','tanggal yang ditentukan','#C8944A']];
$('c12r').innerHTML=C12.map(function(r,k){return '<div class="a card" data-obj id="c12r'+k+'" style="left:84px;top:680px;left:84px;top:'+(660+k*190)+'px;width:912px;height:160px;border-radius:28px"><div class="a" style="left:0;top:26px;width:14px;height:108px;border-radius:0 8px 8px 0;background:'+r[2]+'"></div><div class="a mono" style="left:44px;top:34px;color:var(--gray);font-size:22px">'+r[0]+'</div><div class="a disp" style="left:44px;top:78px;font-size:62px;white-space:nowrap">'+r[1]+'</div></div>'}).join('');
var AVS=[['FINANCE','#C8944A'],['MARKETING','#B84A2E'],['PEMEGANG KEPUTUSAN','#6B6560']];
$('k14av').innerHTML=AVS.map(function(a,k){return '<div class="a" id="k14a'+k+'" style="left:'+(k*210)+'px;top:20px;width:200px"><div style="width:120px;height:120px;margin:0 auto;border-radius:50%;background:'+a[1]+';box-shadow:var(--sh);display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 80 80" width="84" height="84"><circle cx="40" cy="30" r="14" fill="#fff"/><path d="M12 70 C14 48 66 48 68 70" fill="#fff"/></svg></div><div class="a mono" style="left:0;right:0;top:140px;text-align:center;font-size:15px;letter-spacing:.02em;line-height:1.15">'+a[0]+'</div></div>'}).join('');
var K14=['Cara ngukur','Batas rugi','Tanggal cek'];
$('k14rows').innerHTML=K14.map(function(r,k){return '<div class="a" style="left:44px;top:'+(110+k*130)+'px;width:824px;height:110px"><div class="a" style="left:0;top:14px;width:74px;height:74px;border:6px solid #0F0E0C;border-radius:18px"></div><svg class="a" viewBox="0 0 80 80" style="left:-3px;top:8px;width:92px;height:92px" fill="none" stroke-linecap="round" stroke-linejoin="round"><path id="k14k'+k+'" d="M18 42 L34 58 L68 14" stroke="#B84A2E" stroke-width="10"/></svg><div class="a" style="left:116px;top:20px;font:700 46px/1.1 var(--f-body);white-space:nowrap">'+r+'</div></div>'}).join('');
var CAP=BEATS.map(function(b,bi){
  if(b.words&&b.words.length){var out=[],chunk=[];b.words.forEach(function(w,i){chunk.push({w:w.w.replace(/[“”"]/g,''),t:w.t});
    if(chunk.length===3||/[.,?!:]["”]?$/.test(w.w)||i===b.words.length-1){var nx=b.words[i+1];out.push({words:chunk,end:nx?Math.min(nx.t,w.t+1.2):w.t+.9});chunk=[]}});return out}
  var ws=b.say.replace(/[“”"]/g,'').split(/\s+/).filter(Boolean),tot=0;ws.forEach(function(w){tot+=w.length+2});
  var t=T0[bi]+.15,span=b.dur-.35,out=[],chunk=[];
  ws.forEach(function(w,i){var d=span*(w.length+2)/tot;chunk.push({w:w,t:t});t+=d;if(chunk.length===3||/[.,?!:]$/.test(w)||i===ws.length-1){out.push({words:chunk,end:t});chunk=[]}});
  return out});

/* ---------- adegan ---------- */
var DI=6,SCAN_A=4.4,SCAN_B=5.2;
window.ANIMATIC_SCAN={i:DI,a:SCAN_A+.4,b:SCAN_B+1.0};
function kcard(p,t,t0,tt,ts,ti){var kc=E.out(pr(t,.05,.4));op($(p+'card'),cl(kc*3));tf($(p+'card'),'translateY('+((1-kc)*60)+'px)');up($(p+'t'),t,tt,.35,24);up($(p+'s'),t,ts,.4,24);up($(p+'i'),t,ti,.45,24)}
var S=[
 function(t){ // 1
   pop($('h1f'),t,.25,.45);pop($('h1m'),t,.95,.45);draw($('h1z'),t,1.5,.9);
   draw($('h1c1'),t,2.77,.3);draw($('h1c2'),t,3.57,.3)},
 function(t){ // 2
   up($('r2lab'),t,.2,.35,20);pop($('r2card'),t,.3,.5);pop($('r2il'),t,1.1,.35)},
 function(t){ // 3
   pop($('r3a'),t,.2,.45);var a=$('r3t2');op(a,pr(t,2.43,.3));op($('r3t1'),1);
   pop($('r3b'),t,4.13,.45);pop($('r3il'),t,.5,.35)},
 function(t){ // 4
   var k=E.io(pr(t,0,.6));tf($('s4beam'),'rotate('+((1-k)*-6)+'deg)');$('s4beam').style.transformOrigin='540px 150px';up($('s4f'),t,.2,.3,20);up($('s4m'),t,.35,.3,20);pop($('s4ok'),t,.9,.4)},
 function(t){ // 5
   pop($('s5chip'),t,.2,.35);[[1.3,2],[3.35,1],[4.03,0]].forEach(function(a){var k=a[1],b=$('s5b'+k),l=$('s5l'+k),kk=E.out(pr(t,a[0],.5));tf(b,'scaleY('+kk+')');b.style.transformOrigin='50% 100%';tf(l,'translateY('+((1-kk)*-120)+'px)');op(l,cl(kk*3));op(b,cl(kk*3))});
   up($('s5nt'),t,2.6,.35,18);var ph=$('s5photo'),rot=HIRESJS?-2:4;op(ph,pr(t,5.5,.4));tf(ph,'translateY('+((1-E.out(pr(t,5.5,.5)))*-60)+'px) rotate('+rot+'deg)');if(HIRESJS){var fd=1-.85*pr(t,5.5,.4);op($('s5bars'),fd);op($('s5nt'),fd)}},
 function(t){ // 6
   pop($('s6a'),t,.8,.5);pop($('s6ca'),t,3.3,.3);odoSet($('s6odo'),126*E.io(pr(t,3.6,.9)));
   var kb=E.out(pr(t,5.0,.55));op($('s6b'),cl(kb*3));tf($('s6b'),'translateX('+((1-kb)*1080)+'px)');up($('s6big'),t,7.3,.4,30);op($('s6big'),t<7.3?0:parseFloat($('s6big').style.opacity))},
 function(t){ // 7 diagnosis
   var ks=E.io(pr(t,SCAN_A,SCAN_B-SCAN_A+.9)),dark=ks>.5;
   var scan=$('scan'),lab=$('scanlab');op(scan,ks>0&&ks<1?1:0);scan.style.top=(ks*1920)+'px';op(lab,ks>0&&ks<1?1:0);lab.style.top=(ks*1920-40)+'px';
   $('bgd').style.opacity=ks>0?1:0;$('bgd').style.clipPath='inset(0 0 '+((1-ks)*100)+'% 0)';
   $('s7lab').textContent=dark?'taruhan yang gak kita tahu':'taruhan yang kita tahu';$('s7lab').style.color=dark?'#FFE2B0':'#6B6560';op($('s7lab'),pr(t,.1,.3));
   for(var k=0;k<8;k++){var c=$('s7t'+k),kk=E.out(pr(t,.2+k*.08,.4));op(c,cl(kk*3));tf(c,'translateY('+((1-kk)*50)+'px)');
     if(k!==2&&dark){c.style.background='transparent';c.style.boxShadow='none';c.style.border='4px dashed rgba(255,226,176,.55)';c.firstChild.style.opacity=.15;$('s7q'+k).style.opacity=1}else{c.style.background='#fff';c.style.boxShadow='';c.style.border='none';c.firstChild.style.opacity=1;$('s7q'+k).style.opacity=0}}
   var h=$('s7h');up(h,t,6.0,.5,24);op(h,t<6.0?0:parseFloat(h.style.opacity))},
 function(t){ // 8
   var m=E.io(pr(t,2.9,1.0));tf($('t8f'),'translate('+(m*(100))+'px,'+(m*(250))+'px)');tf($('t8m'),'translate('+(-m*100)+'px,'+(m*120)+'px)');pop($('t8f'),t,.2,.4,'');pop($('t8m'),t,.3,.4,'');
   tf($('t8f'),'translate('+(m*60)+'px,'+(m*120)+'px) scale('+(t<.5?E.back(pr(t,.2,.4)):1)+')');tf($('t8m'),'translate('+(-m*60)+'px,'+(m*120)+'px) scale('+(t<.6?E.back(pr(t,.3,.4)):1)+')');
   var tb=$('t8t');op($('t8t'),pr(t,3.9,.4));tf($('t8t'),'scale('+E.out(pr(t,3.9,.5))+')');
   [0,1,2].forEach(function(k){pop($('t8n'+k),t,5.8+k*.35,.35)});
   var s=$('t8stamp'),ks=pr(t,7.6,.3);op(s,ks?1:0);tf(s,'rotate(-5deg) scale('+(ks<1?1.25-.25*E.out(ks):1)+')')},
 function(t){kcard('k9',t,0,.2,1.2,1.7)},
 function(t){kcard('k10',t,0,.2,1.1,1.9)},
 function(t){kcard('k11',t,0,.2,1.3,1.7)},
 function(t){ // 12
   pop($('c12chip'),t,.2,.3);up($('c12t'),t,.4,.3,16);draw($('c12l'),t,1.38,1.4);
   [[2.7,0],[3.9,1],[5.6,2]].forEach(function(a){var c=$('c12r'+a[1]),kk=E.out(pr(t,a[0],.45));op(c,cl(kk*3));tf(c,'translateX('+((1-kk)*-500)+'px)')})},
 function(t){ // 13
   var a=$('f13a'),kk=E.out(pr(t,.45,.45));op(a,cl(kk*3));tf(a,'translateX('+((1-kk)*-400)+'px)');draw($('f13u'),t,1.0,.4);up($('f13l'),t,1.1,.3,20);
   var b=$('f13b'),k2=E.out(pr(t,2.2,.45));op(b,cl(k2*3));tf(b,'translateX('+((1-k2)*400)+'px)');up($('f13s'),t,3.3,.3,20);
   var h=$('f13h');pop(h,t,3.9,.4,' rotate(-2deg)')},
 function(t){ // 14
   pop($('k14send'),t,.2,.5);draw($('k14a'),t,.9,.4);[1.88,2.68,3.61].forEach(function(a,k){pop($('k14a'+k),t,a,.4)});
   var kc=E.out(pr(t,4.8,.5));op($('k14card'),cl(kc*3));tf($('k14card'),'translateY('+((1-kc)*70)+'px)');pop($('k14chip'),t,6.1,.3);
   [7.0,7.9,8.8].forEach(function(a,k){draw($('k14k'+k),t,a,.35)})},
 function(t){ // 15 end card
   pop($('e15send'),t,.05,.45);up($('e15h1'),t,.2,.35,40);up($('e15h2'),t,.35,.35,40);up($('e15sub'),t,.6,.35,30);[0,1,2].forEach(function(k){up($('e15p'+k),t,.8+k*.18,.35,40)});op($('e15h'),pr(t,1.5,.4))}];

var TR=[null,'zoom','drop','whip','whip','whip','whip','whip','drop','drop','drop','whip','drop','up','drop'],TD=.42;
function apply(i,t){
  var sec=$('b'+(i+1)),start=T0[i],end=start+BEATS[i].dur,inK=i?pr(t,start,TD):1,outK=i<BEATS.length-1?pr(t,end,TD):0;
  var vis=t>=start&&(i===BEATS.length-1||t<end+TD);sec.style.visibility=vis?'visible':'hidden';if(!vis)return;
  var tx=0,sc=1+.03*pr(t,start,BEATS[i].dur),blur=0,o=1,ty=0;
  var ti=TR[i];if(inK<1){var e=E.io(inK);if(ti==='zoom'){sc*=.82+.18*e;o=e}else if(ti==='whip'){tx=(1-e)*1080;blur=(1-e)*14}else if(ti==='up'){ty=(1-e)*1920}else if(ti==='drop'){o=e}}
  var to=TR[i+1];if(outK>0){var e2=E.io(outK);if(to==='zoom'){sc*=1+e2*1.2;o=1-e2;blur=e2*10}else if(to==='whip'){tx=-e2*1080;blur=e2*14}else if(to==='up'){ty=-e2*1920}else if(to==='drop'){o=1-e2}}
  tf(sec,'translate('+tx+'px,'+ty+'px) scale('+sc+')');sec.style.filter=blur>.3?'blur('+blur.toFixed(1)+'px)':'none';op(sec,o);sec.style.zIndex=i+1;
  S[i](LOCAL(i,t-start));
}
window.ANIMATIC_T0=T0;window.ANIMATIC_LOCAL=function(i,lt){return LOCAL(i,lt)};
window.seek=function(t){
  var cur=0;for(var i=0;i<BEATS.length;i++)if(t>=T0[i])cur=i;
  for(var j=0;j<BEATS.length;j++)apply(j,t);
  if(cur!==DI&&!(cur===DI+1&&t<T0[DI+1]+TD)){$('bgd').style.opacity=0;$('scan').style.opacity=0;$('scanlab').style.opacity=0}
  var fl=pr(t,T0[DI+1]-.05,.35);op($('flash'),fl>0&&fl<1?(1-fl)*.85:0);
  var dark=cur===DI&&LOCAL(DI,t-T0[DI])>SCAN_A+.7;
  $('hdl').style.color=dark?'#FFE2B0':(cur===14?'#fff':'#0F0E0C');
  $('chap').textContent='// 0'+(BEATS[cur].chap||cur+1)+' · '+BEATS[cur].name;$('chap').style.color=dark?'#FFE2B0':(cur===14?'#fff':'#B84A2E');
  var span=$('cap').firstChild,list=CAP[cur],c=null;for(var k=0;k<list.length;k++)if(t>=list[k].words[0].t-.05)c=list[k];
  if(!c||t>list[list.length-1].end+.1){op(span,0)}else{op(span,1);span.innerHTML=c.words.map(function(w){return '<u style="color:'+(t>=w.t?'#fff':'rgba(255,255,255,.38)')+'">'+w.w+'</u>'}).join(' ');
    var kk=pr(t,c.words[0].t-.05,.12);tf(span,'scale('+(.92+.08*E.back(kk))+')')}
};
window.seek(0);
})();
</script>
</body>
</html>
'''.replace('__DEF__', DEF).replace('__HIRES__','true' if HIRES else 'false')
open(A + 'animatic-meja.html', 'w', encoding='utf-8').write(head + BODY + tail + JS)
sc_json=[{"start":s,"act":a,"chap":c} for s,a,c in SC]
anch={"_petunjuk":"Adegan dimulai pada kata pembukanya.","scenes":sc_json,"beats":[
 [[0.3,"finance"],[2.77,"duaduanya"]],[[0.2,"di"],[1.07,"dampingi"]],[[0.2,"finance"],[2.43,"hasilnya"],[4.13,"marketing"]],[[0.2,"duaduanya"]],
 [[0.2,"di"],[1.3,"nike"],[3.35,"adidas"],[4.03,"converse"],[5.97,"satu"]],
 [[0.2,"hasilnya"],[3.82,"126"],[5.0,"dan"],[7.39,"7"]],
 [[0.2,"tapi"],[4.39,"nike"],[5.93,"taruhan"]],
 [[0.2,"biasanya"],[3.97,"mereka"],[6.68,"saya"],[7.6,"coordination"]],
 [[0.2,"pertama"],[1.25,"ngukurnya"]],[[0.2,"kedua"],[1.17,"ruginya"]],[[0.2,"ketiga"],[1.29,"ngecek"]],
 [[0.2,"contohnya"],[1.38,"dua"],[2.72,"biaya"],[3.96,"batas"],[5.7,"dicek"]],
 [[0.2,"kalo"],[1.15,"lanjut"],[2.25,"kena"],[3.43,"stop"],[4.54,"nyalahin"]],
 [[0.2,"kirim"],[1.88,"finance"],[2.68,"marketing"],[3.61,"pegang"],[5.22,"duduk"],[7.8,"kesepakatan"]],[[0.2,"berikutnya"]]]}
json.dump(anch,open(A+'anchors-meja.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ok')
