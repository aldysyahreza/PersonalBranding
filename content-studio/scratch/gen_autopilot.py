"""Reels 'bisnis autopilot': animasi penuh Motion Kit dari timing.json vo_prep.
Pakai: python3 scratch/gen_metrik.py out/reel17/timing.json -> animatic/mk-autopilot.html + out/reel17/events.json"""
import json, sys, re, os
O_PERSON = open('/home/user/content-studio/scratch/gen_owner.py', encoding='utf-8').read()
O_PERSON = O_PERSON[O_PERSON.index('def person('):O_PERSON.index('def card(')]
A = '/home/user/content-studio/animatic/'
TIMING = sys.argv[1]; OUT = os.path.dirname(TIMING)
tl = json.load(open(TIMING, encoding='utf-8'))
nrm = lambda s: ''.join(c for c in s.lower() if c.isalnum())
words, beat_of = [], []
for bi, b in enumerate(tl['beats']):
    for w in b['words']: words.append(w); beat_of.append(bi)
SC = [('bisnis',0,0),('sebelumnya',0,0),
      ('kata',1,0),('tapi',1,0),
      ('bisnis',2,0),('atul',2,0),('menemukan',2,0),('timnya',2,0),
      ('di',3,0),('mulai',3,0),('tulis',3,0),('kalau',3,0),('tetap',3,0),
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
KEY = {'autopilot','autopilotnya','kosong','pilot','pilotnya','ditulis','checklist','lupa','separuh','rutenya','layarnya','meleset','perbaiki','layar','kemudi','simpan','pertamamu','tiga','bisa'}
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
function PIPE(L,o){
 var n=5,x0=110,sw=172,cy=330,H=120,nh=34,id=o.id;
 var box=MK.el('div','left:0;top:'+(o.y-330)+'px;width:1080px;height:700px','',L.root);box.className='mk-a';
 var s='<svg viewBox="0 0 1080 700" width="1080" height="700" style="overflow:visible"><defs><pattern id="'+id+'pt" width="64" height="24" patternUnits="userSpaceOnUse"><rect width="64" height="24" fill="#7FA9BC"/><path d="M4 12 h26" stroke="#CFE3EA" stroke-width="5" stroke-linecap="round"/></pattern></defs>';
 s+='<path d="M30 120 h92 v46" fill="none" stroke="#0F0E0C" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/><rect x="70" y="96" width="30" height="16" rx="4" fill="#B84A2E"/><rect id="'+id+'pour" x="112" y="176" width="20" height="0" fill="#7FA9BC"/>';
 for(var i=0;i<n;i++)s+='<rect id="'+id+'s'+i+'" x="'+(x0+i*sw)+'" y="0" width="'+sw+'" height="0" rx="6" fill="#E8E1D5" stroke="#0F0E0C" stroke-width="6"/><rect id="'+id+'w'+i+'" x="'+(x0+i*sw+4)+'" y="0" width="'+(sw-8)+'" height="0" fill="url(#'+id+'pt)"/>';
 for(var i=1;i<n;i++)s+='<rect id="'+id+'f'+i+'" x="'+(x0+i*sw-9)+'" y="0" width="18" height="0" rx="4" fill="#6B6560" stroke="#0F0E0C" stroke-width="4"/>';
 for(var k=0;k<4;k++)s+='<circle id="'+id+'d'+k+'" cx="'+(x0+n*sw+14)+'" cy="0" r="11" fill="#7FA9BC" stroke="#0F0E0C" stroke-width="3"/>';
 s+='<path id="'+id+'out" d="" fill="#7FA9BC" stroke="#0F0E0C" stroke-width="4"/>';
 s+='<ellipse id="'+id+'pd" cx="0" cy="'+(cy+H/2+112)+'" rx="0" ry="16" fill="#7FA9BC" stroke="#0F0E0C" stroke-width="4"/>';
 for(var k=0;k<6;k++)s+='<circle id="'+id+'sp'+k+'" cx="0" cy="0" r="9" fill="#7FA9BC" stroke="#0F0E0C" stroke-width="3"/>';
 if(o.labels)for(var i=0;i<n;i++)s+='<text id="'+id+'lb'+i+'" x="'+(x0+i*sw+sw/2)+'" y="'+(cy+H/2+58)+'" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="28" fill="#0F0E0C">'+o.labels[i]+'</text>';
 var PL=o.piles||[];
 for(var p=0;p<PL.length;p++)for(var j=0;j<PL[p].cnt;j++)s+='<g id="'+id+'pl'+p+'_'+j+'" opacity="0"><rect x="'+(x0+PL[p].idx*sw+sw/2-40)+'" y="'+(cy-H/2-16-(j+1)*36)+'" width="80" height="30" rx="6" fill="'+(PL[p].col||'#FBF8F3')+'" stroke="#0F0E0C" stroke-width="4"/>'+(PL[p].chat?'<path d="M'+(x0+PL[p].idx*sw+sw/2-24)+' '+(cy-H/2-16-(j+1)*36+15)+' h48" stroke="#6B6560" stroke-width="4"/>':'')+'</g>';
 s+='</svg>';box.innerHTML=s;
 var g=function(x){return document.getElementById(id+x)};
 L.on(function(t){
  var ap=MK.E.over(MK.pr(t,o.at||0,.45));box.style.opacity=ap>0?1:0;box.style.transform='translateY('+((1-ap)*120)+'px)';
  var nar=o.nar,hn=nh;
  if(o.narrowAt!=null)hn=H-(H-nh)*MK.E.io(MK.pr(t,o.narrowAt,.7));
  if(o.widenAt!=null)hn=nh+(H-nh)*MK.E.io(MK.pr(t,o.widenAt,.9));
  var flow=MK.pr(t,o.flowAt==null?0:o.flowAt,.6),heavy=o.heavyAt!=null?MK.pr(t,o.heavyAt,.6):0;
  var hs=[];for(var i=0;i<n;i++){var h=(i===nar?hn:H);if(o.preWide!=null&&i===o.preWide)h=H;hs.push(h);var r=g('s'+i);r.setAttribute('y',cy-h/2);r.setAttribute('height',h);
   var wh=(i<=nar?h-8:Math.min(hn,h)-8)*flow;if(nar==null)wh=(h-8)*flow;var w=g('w'+i);w.setAttribute('y',cy-wh/2);w.setAttribute('height',Math.max(0,wh));}
  for(var i=1;i<n;i++){var fh=Math.max(hs[i-1],hs[i])+26;var f=g('f'+i);f.setAttribute('y',cy-fh/2);f.setAttribute('height',fh);}
  var pt=document.getElementById(id+'pt');if(pt)pt.setAttribute('patternTransform','translate('+((t*(140+220*heavy))%64)+',0)');
  var pw=14+30*heavy,po=g('pour');po.setAttribute('x',122-pw/2);po.setAttribute('width',pw);po.setAttribute('height',flow>0?(cy-H/2-176+8):0);
  var full=(nar==null)||hn>H*.8, xo=x0+n*sw;
  for(var k=0;k<4;k++){var d=g('d'+k);if(full||flow<=0){d.setAttribute('opacity',0)}else{d.setAttribute('opacity',1);d.setAttribute('cy',cy+((t*1.1+k/4)%1)*300)}}
  g('out').setAttribute('d',full&&flow>0?'M'+xo+' '+(cy-50)+' q60 0 70 60 l0 '+(240*flow)+' h-60 l0 -'+(200*flow)+' q-4 -20 -10 -20z':'');
  var over=(!full&&o.overAt!=null)?MK.pr(t,o.overAt,.8):0,pd=g('pd');pd.setAttribute('cx',x0+(nar||0)*sw-40);pd.setAttribute('rx',110*over);
  for(var k=0;k<6;k++){var c=g('sp'+k);if(over>0){var ph=(t*2.2+k/6)%1;c.setAttribute('cx',x0+(nar||0)*sw-20-k*10+ph*30);c.setAttribute('cy',cy-H/2-ph*(1-ph)*360);c.setAttribute('opacity',1)}else c.setAttribute('opacity',0)}
  for(var p=0;p<PL.length;p++)for(var j=0;j<PL[p].cnt;j++){var e=g('pl'+p+'_'+j);var on=t>=PL[p].at+j*.1&&(PL[p].out==null||t<PL[p].out+(PL[p].cnt-j)*.06);e.setAttribute('opacity',on?1:0)}
  if(o.labels&&o.hi!=null)for(var i=0;i<n;i++){var lb=g('lb'+i);lb.setAttribute('fill',i===o.hi&&t>=(o.hiAt||0)?'#B84A2E':'#0F0E0C');lb.setAttribute('font-weight',i===o.hi&&t>=(o.hiAt||0)?'800':'400')}
 });
}

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
exec(O_PERSON)
fig = lambda u, shirt, dark, flip=False: person(u, shirt, dark, '#2a1d14', flip).replace('"', '\\"').replace('\n', '')
S = []
def scene(i, body, tr=False, dolly=0, paper=None):
    S.append("{dur:%s,%s%s%s build:function(L){\n%s\n}}" % (DUR[i], " tr:'sweep'," if tr else '', " dolly:%s," % dolly if dolly else '', " paper:'%s'," % paper if paper else '', body))
    if tr: ev(i, 0, 'sweep')

def R(js, **kw):
    for k_, v_ in kw.items(): js = js.replace('@' + k_ + '@', str(v_))
    return js
PLANE = '<svg viewBox="0 0 200 90" width="200" height="90"><path d="M10 50 Q20 38 60 38 L150 38 Q190 40 195 50 Q190 60 150 62 L60 62 Q20 62 10 50Z" fill="#FBF8F3" stroke="#0F0E0C" stroke-width="6"/><path d="M90 40 L120 4 L136 4 L118 40Z M90 60 L120 86 L136 86 L118 60Z M20 42 L10 18 L24 18 L40 40Z" fill="#B84A2E" stroke="#0F0E0C" stroke-width="5" stroke-linejoin="round"/><g fill="#7FA9BC"><circle cx="150" cy="47" r="5"/><circle cx="135" cy="47" r="5"/><circle cx="120" cy="47" r="5"/></g></svg>'
# 0 HOOK: owner di kursi pantai + grafik omzet naik sendiri
we, wt, wj = W(0, 'emang', 4.3), W(0, 'tapi', 5.5), W(0, 'dijanjikan', 7.3)
scene(0, R("""MK.Headline(L,{y:280,size:104,html:'Bisnis autopilot.<br>Emang <span style="color:'+C.terra+'">bisa?</span>'});
var sc=MK.el('div','left:90px;top:640px;width:560px;height:560px','<svg viewBox="0 0 280 280" width="560" height="560"><circle cx="230" cy="40" r="26" fill="#C8944A"/><path d="M30 120 Q100 40 170 120Z" fill="#B84A2E" stroke="#0F0E0C" stroke-width="5"/><path d="M100 82 V250" stroke="#0F0E0C" stroke-width="6"/><path d="M40 240 L200 200 L230 240" fill="none" stroke="#0F0E0C" stroke-width="7" stroke-linejoin="round"/><path d="M60 236 L190 206" stroke="#C8944A" stroke-width="14"/><circle cx="178" cy="182" r="18" fill="#F1C9A3" stroke="#0F0E0C" stroke-width="4"/><path d="M164 178 h30" stroke="#0F0E0C" stroke-width="6"/><path d="M0 262 H280" stroke="#C8944A" stroke-width="10"/></svg>',L.root);sc.className='mk-a';
var ph=MK.el('div','left:650px;top:700px;width:330px;height:440px;border-radius:40px;background:#0F0E0C;padding:18px;box-sizing:border-box','<div style="width:100%;height:100%;border-radius:26px;background:#FBF8F3;position:relative;overflow:hidden"><div class="mk-mono" style="position:absolute;left:18px;top:16px;font-size:20px;color:#6B6560">OMZET</div><svg viewBox="0 0 290 400" width="290" height="400" style="position:absolute;left:0;top:0"><path id="og" d="M20 330 L80 300 L140 250 L200 170 L270 80" fill="none" stroke="#B84A2E" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="420" stroke-dashoffset="420"/></svg></div>',L.root);ph.className='mk-a';
var q=MK.el('div','left:560px;top:520px;font-size:280px;line-height:1;color:#B84A2E','?',L.root);q.className='mk-a mk-fr';
var jn=MK.el('div','left:96px;top:1240px;width:888px;font-size:44px;color:#6B6560','“owner liburan, omzet jalan sendiri”',L.root);jn.className='mk-a mk-fri';
MK.MarkerStrike(L,{x:96,y:1240,w:760,h:56,at:@J@});
L.on(function(t){var g=document.getElementById('og');var k=MK.E.io(MK.pr(t,.2,2.4));if(g){var wob=t>@T@?Math.sin(t*9)*12*Math.min(1,(t-@T@)*2):0;g.setAttribute('stroke-dashoffset',420*(1-k));g.setAttribute('transform','translate(0,'+wob+')')}
sc.style.opacity=MK.pr(t,.05,.3);ph.style.opacity=MK.pr(t,.15,.3);var a=MK.pr(t,@E@,.3);q.style.opacity=a;q.style.transform='rotate(8deg) scale('+(.4+.6*MK.E.over(a))+')';jn.style.opacity=MK.pr(t,@T@,.3)});""", E=we, T=wt, J=wj))
ev(0, .2, 'draw'); ev(0, we, 'stamp'); ev(0, wj, 'scratch')
# 1 perkenalan (sama gen_grow)
scene(1, R("""var ph=MK.el('div','left:96px;top:420px;width:420px;height:560px;border-radius:12px;overflow:hidden;box-shadow:0 18px 40px -18px rgba(15,14,12,.45);background:#B84A2E','<img src="../foto/profil-seminar.jpg" style="width:100%;height:100%;object-fit:cover;object-position:50% 20%">',L.root);ph.className='mk-a';
var nm=MK.el('div','left:560px;top:430px;width:430px;font-size:76px;line-height:.95','ALDY<br>SYAHREZA',L.root);nm.className='mk-a mk-fr';
MK.PaperCard(L,{x:560,y:650,w:420,at:@A@,from:'right',rot:1,html:'<div class="mk-fr" style="font-size:46px">100+ BRAND</div><div class="mk-ou" style="font-size:26px;color:#6B6560">belasan tahun</div>'});
var c3=MK.el('div','left:600px;top:850px;width:300px;height:300px','<svg viewBox="0 0 200 200" width="300" height="300"><circle cx="100" cy="100" r="80" fill="none" stroke="#E8E1D5" stroke-width="16"/><circle id="r360" cx="100" cy="100" r="80" fill="none" stroke="#B84A2E" stroke-width="16" stroke-linecap="round" stroke-dasharray="503" stroke-dashoffset="503" transform="rotate(-90 100 100)"/><text x="100" y="116" text-anchor="middle" font-family="Fraunces,serif" font-weight="800" font-size="54" fill="#0F0E0C">360°</text></svg>',L.root);c3.className='mk-a';
@SUB@
L.on(function(t){var k=MK.pr(t,.05,.4);ph.style.opacity=k;ph.style.transform='rotate(-2deg) translateY('+((1-MK.E.out(k))*40)+'px)';nm.style.opacity=MK.pr(t,@N@,.3);var r=document.getElementById('r360');var q=MK.E.io(MK.pr(t,@T@,1.2));if(r)r.setAttribute('stroke-dashoffset',503*(1-q));c3.style.opacity=MK.pr(t,@T@-.3,.3)});""",
  A=W(1, 'seratus', 4), T=W(1, 'three', 6.6), N=W(1, 'aldy', 1.6) - .2, SUB=sub(1)), tr=True)
ev(1, .05, 'slide'); ev(1, W(1, 'seratus', 4), 'pop'); ev(1, W(1, 'three', 6.6), 'draw')
# 2 PESAWAT di rute + 90% otomasi
wm, wh = W(2, 'mesin', 2.2), W(2, 'hampir', 4.1)
scene(2, R("""var sky=MK.el('div','left:0;top:0;width:1080px;height:1920px;background:linear-gradient(#DDE9EE,#FBF8F3 70%)',' ',L.root);sky.className='mk-a';
var cl=[];for(var i=0;i<4;i++){var c=MK.el('div','left:'+[80,620,300,760][i]+'px;top:'+[420,520,1020,1140][i]+'px;width:220px;height:80px;border-radius:40px;background:#FBF8F3;border:4px solid #0F0E0C',' ',L.root);c.className='mk-a';cl.push(c)}
MK.InkPath(L,{d:'M80 1180 C300 900 500 1000 620 760 S900 420 1000 330',w:6,at:.1,dur:1.2,color:'#6B6560'});
var pl=MK.el('div','left:0;top:0;width:200px;height:90px','@P@',L.root);pl.className='mk-a';
var bx=MK.el('div','left:96px;top:1220px;width:888px;height:150px;border-radius:18px;background:#FBF8F3;border:5px solid #0F0E0C;padding:18px 24px;box-sizing:border-box','<div class="mk-ou" style="font-size:30px">waktu terbang pakai otomasi</div><div style="margin-top:12px;height:40px;border-radius:20px;border:4px solid #0F0E0C;overflow:hidden;background:#E8E1D5"><div id="ab" style="height:100%;width:0;background:#B84A2E"></div></div>',L.root);bx.className='mk-a';
MK.CountUp(L,{x:780,y:1100,from:0,to:90,at:@H@,dur:1.2,size:96,prefix:'±',suffix:'%'});
var src=MK.el('div','left:96px;top:1380px;font-size:22px;color:#6B6560','sumber: FAA, dikutip Dept. Perhubungan AS (2016)',L.root);src.className='mk-a mk-mono';
L.on(function(t){var u=MK.E.io(MK.pr(t,.3,5));var x=80+u*920,y=1180-u*850+Math.sin(u*6)*60;pl.style.transform='translate('+(x-100)+'px,'+(y-45)+'px) rotate('+(-35+Math.cos(u*6)*12)+'deg)';
for(var i=0;i<4;i++)cl[i].style.transform='translateX('+(-(t*30+i*40)%300+150)+'px)';var k=MK.pr(t,@H@,.3);bx.style.opacity=src.style.opacity=k;var b=document.getElementById('ab');if(b)b.style.width=(MK.E.out(MK.pr(t,@H@,1.2))*90)+'%'});""", P=PLANE, H=wh))
ev(2, .1, 'sweep'); ev(2, wh, 'tick'); ev(2, wh + 1.2, 'pop')
# 3 KOKPIT: tidak pernah kosong + 3 tugas + badai
wk, wp, wpa, wa, wc = W(3, 'kokpitnya', .4), W(3, 'pasang', 4.1), W(3, 'pantau', 5.8), W(3, 'ambil', 8), W(3, 'cuaca', 8.7)
scene(3, R("""var ck=MK.el('div','left:60px;top:300px;width:960px;height:640px','<svg viewBox="0 0 480 320" width="960" height="640"><path d="M20 300 L60 60 Q240 0 420 60 L460 300Z" fill="#2A2824" stroke="#0F0E0C" stroke-width="6"/><path id="win" d="M80 170 L100 80 Q240 34 380 80 L400 170Z" fill="#BFD8E2" stroke="#0F0E0C" stroke-width="5"/><g id="storm" opacity="0"><path d="M150 120 q20 -30 50 -10 q20 -30 50 0 q30 -10 30 20 h-130z" fill="#6B6560"/><path d="M220 130 l-14 26 h14 l-10 24" fill="none" stroke="#C8944A" stroke-width="6"/></g><rect x="110" y="200" width="70" height="48" rx="6" fill="#0F0E0C" stroke="#6B6560" stroke-width="3"/><path id="sc1" d="M118 236 L134 220 L150 228 L172 208" fill="none" stroke="#7FD6A0" stroke-width="4"/><rect x="300" y="200" width="70" height="48" rx="6" fill="#0F0E0C" stroke="#6B6560" stroke-width="3"/><circle cx="335" cy="224" r="16" fill="none" stroke="#7FD6A0" stroke-width="4"/><path id="nd" d="M335 224 L335 210" stroke="#C8944A" stroke-width="4"/><g id="yk"><path d="M205 262 h70 M240 262 v40" stroke="#C8944A" stroke-width="10" stroke-linecap="round"/></g></svg>',L.root);ck.className='mk-a';
var pi=MK.el('div','left:430px;top:620px;width:220px;height:420px',"@F@",L.root);pi.className='mk-a';
var tx=MK.el('div','left:96px;top:300px;width:888px;font-size:60px;color:#FBF8F3;text-align:center',' ',L.root);
var ts=[];var lb=[['1','PASANG RUTE','sebelum terbang'],['2','PANTAU LAYAR','selama terbang'],['3','AMBIL ALIH','saat cuaca berubah']];
for(var i=0;i<3;i++){var e=MK.el('div','left:'+(70+i*320)+'px;top:1000px;width:300px;height:300px;border-radius:20px;background:#FBF8F3;border:5px solid #0F0E0C;padding:22px;box-sizing:border-box;box-shadow:0 16px 30px -18px rgba(15,14,12,.5)','<div class="mk-fr" style="font-size:80px;color:#B84A2E;line-height:1">'+lb[i][0]+'</div><div class="mk-fr" style="font-size:36px;line-height:1.05;margin-top:10px">'+lb[i][1]+'</div><div class="mk-ou" style="font-size:26px;color:#6B6560;margin-top:8px">'+lb[i][2]+'</div>',L.root);e.className='mk-a';ts.push(e)}
var AT=[@P@,@PA@,@A@];
L.on(function(t){var k=MK.E.over(MK.pr(t,0,.45));ck.style.opacity=k>0?1:0;ck.style.transform='scale('+(.85+.15*k)+')';pi.style.opacity=MK.pr(t,@K@,.3);
var n=document.getElementById('nd');if(n)n.setAttribute('transform','rotate('+(Math.sin(t*2)*60)+' 335 224)');
var s=document.getElementById('storm');if(s)s.setAttribute('opacity',MK.pr(t,@C@,.4));var y=document.getElementById('yk');if(y)y.setAttribute('transform',t>@C@?'rotate('+(Math.sin((t-@C@)*7)*14)+' 240 262)':'');
for(var i=0;i<3;i++){var q=MK.pr(t,AT[i],.35);ts[i].style.opacity=q>0?1:0;ts[i].style.transform='translateY('+((1-MK.E.over(q))*200)+'px) rotate('+((i-1)*2)+'deg)'}});
@SUB@""", F=fig('pil', '#2A2824', '#0F0E0C'), K=wk, P=wp, PA=wpa, A=wa, C=wc, SUB=sub(3)), tr=True, dolly=.05)
ev(3, wk, 'pop'); ev(3, wp, 'slide'); ev(3, wpa, 'slide'); ev(3, wa, 'slide'); ev(3, wc, 'stamp')
# 4 BUKAN APLIKASI -> CARA KERJA DITULIS
wap, wdt = W(4, 'aplikasi', 2.7), W(4, 'ditulis', 6)
scene(4, R("""var hd=MK.el('div','left:96px;top:300px;width:888px;font-size:64px;line-height:1.05','Autopilot bisnis itu...',L.root);hd.className='mk-a mk-fr';
var ph=MK.el('div','left:120px;top:520px;width:340px;height:600px;border-radius:44px;background:#0F0E0C;padding:18px;box-sizing:border-box','<div style="width:100%;height:100%;border-radius:30px;background:#FBF8F3;display:flex;flex-wrap:wrap;gap:18px;padding:30px;box-sizing:border-box;align-content:flex-start"><div style="width:110px;height:110px;border-radius:26px;background:#7FA9BC;border:4px solid #0F0E0C;display:flex;align-items:center;justify-content:center;font:800 26px Outfit;color:#fff">AUTO</div><div style="width:110px;height:110px;border-radius:26px;background:#E8E1D5"></div><div style="width:110px;height:110px;border-radius:26px;background:#E8E1D5"></div><div style="width:110px;height:110px;border-radius:26px;background:#E8E1D5"></div></div>',L.root);ph.className='mk-a';
var x=MK.el('div','left:150px;top:600px;font-size:340px;line-height:1;color:#B84A2E','×',L.root);x.className='mk-a mk-fr';
var cb=MK.el('div','left:560px;top:480px;width:420px;height:640px','<svg viewBox="0 0 210 320" width="420" height="640"><rect x="10" y="20" width="190" height="290" rx="12" fill="#C8944A" stroke="#0F0E0C" stroke-width="6"/><rect x="26" y="44" width="158" height="250" fill="#FBF8F3" stroke="#0F0E0C" stroke-width="4"/><rect x="70" y="8" width="70" height="28" rx="8" fill="#6B6560" stroke="#0F0E0C" stroke-width="5"/><g id="ln" stroke="#0F0E0C" stroke-width="5" stroke-linecap="round"></g></svg>',L.root);cb.className='mk-a';
var lbl=MK.el('div','left:560px;top:1150px;width:420px;text-align:center;font-size:44px;color:#B84A2E','cara kerja yang ditulis',L.root);lbl.className='mk-a mk-fri';
L.on(function(t){hd.style.opacity=MK.pr(t,.05,.3);ph.style.opacity=MK.pr(t,.3,.3);var a=MK.pr(t,@AP@,.25);x.style.opacity=a;x.style.transform='scale('+(.4+.6*MK.E.over(a))+')';
var c=MK.E.over(MK.pr(t,@AP@+.6,.45));cb.style.opacity=c>0?1:0;cb.style.transform='translateY('+((1-c)*300)+'px) rotate(3deg)';
var g=document.getElementById('ln');if(g){var n=Math.floor(MK.pr(t,@AP@+1,@DT@-@AP@)*6+.001);var h='';for(var i=0;i<n;i++)h+='<path d="M44 '+(80+i*36)+' l10 10 l16 -18 M84 '+(84+i*36)+' h'+(70+(i%3)*14)+'"/>';g.innerHTML=h}lbl.style.opacity=MK.pr(t,@DT@,.3)});""", AP=wap, DT=wdt))
ev(4, wap, 'scratch'); ev(4, wap + .6, 'slide'); ev(4, wdt, 'pop')
# 5 KARTU TOKOH Gawande
wd5, wcm = W(5, 'dokter', .7), W(5, 'checklist', 2.1)
GAW = ('<svg viewBox="0 0 260 360" width="300" height="415"><rect x="40" y="200" width="180" height="170" rx="60" fill="#5E9C93"/>'
       '<path d="M100 200 L130 236 L160 200" fill="none" stroke="#3f7a72" stroke-width="8"/>'
       '<path d="M80 236 Q70 300 110 310" fill="none" stroke="#2A2824" stroke-width="6"/><circle cx="112" cy="312" r="10" fill="#6B6560" stroke="#0F0E0C" stroke-width="3"/>'
       '<rect x="112" y="160" width="36" height="40" fill="#C89A72"/><circle cx="130" cy="118" r="58" fill="#C89A72"/>'
       '<path d="M70 104 Q74 50 130 48 Q186 50 190 104 Q170 76 130 76 Q90 76 70 104Z" fill="#2A2824"/>'
       '<path d="M108 150 Q130 160 152 150" fill="none" stroke="#0F0E0C" stroke-width="4" stroke-linecap="round"/>'
       '<circle cx="110" cy="120" r="5" fill="#0F0E0C"/><circle cx="150" cy="120" r="5" fill="#0F0E0C"/>'
       '<g transform="rotate(-8 200 300)"><rect x="150" y="250" width="100" height="120" rx="6" fill="#FBF8F3" stroke="#0F0E0C" stroke-width="5"/>'
       '<g stroke="#B84A2E" stroke-width="5" fill="none"><path d="M166 280 l6 6 l10 -12 M166 310 l6 6 l10 -12 M166 340 l6 6 l10 -12"/></g>'
       '<g stroke="#0F0E0C" stroke-width="4"><path d="M192 282 h40 M192 312 h40 M192 342 h40"/></g></g></svg>')
scene(5, R("""var fr=MK.el('div','left:96px;top:330px;width:888px;height:920px;border-radius:24px;background:#FBF8F3;border:6px solid #0F0E0C;box-shadow:0 30px 60px -30px rgba(15,14,12,.5)',' ',L.root);fr.className='mk-a';
var tg=MK.el('div','left:140px;top:370px;font-size:26px;letter-spacing:.1em;color:#B84A2E','KARTU TOKOH',L.root);tg.className='mk-a mk-mono';
var pt=MK.el('div','left:390px;top:410px;width:300px;height:415px','@G@',L.root);pt.className='mk-a';
var nm=MK.el('div','left:140px;top:850px;width:800px;text-align:center;font-size:80px;line-height:1','ATUL GAWANDE',L.root);nm.className='mk-a mk-fr';
var s1=MK.el('div','left:140px;top:950px;width:800px;text-align:center;font-size:34px','Dokter bedah & peneliti kesehatan',L.root);s1.className='mk-a mk-ou';
var s2=MK.el('div','left:140px;top:1000px;width:800px;text-align:center;font-size:34px;color:#B84A2E','Penulis <i>The Checklist Manifesto</i> (2009)',L.root);s2.className='mk-a mk-ou';
L.on(function(t){var k=MK.E.over(MK.pr(t,.05,.45));fr.style.opacity=k>0?1:0;fr.style.transform='rotate(1.5deg) scale('+(.8+.2*k)+')';tg.style.opacity=MK.pr(t,.2,.3);
var p=MK.E.over(MK.pr(t,.2,.5));pt.style.opacity=p>0?1:0;pt.style.transform='translateY('+((1-p)*80)+'px) rotate('+(Math.sin(t*1.5)*1.5)+'deg)';nm.style.opacity=MK.pr(t,.35,.3);s1.style.opacity=MK.pr(t,@D@,.3);s2.style.opacity=MK.pr(t,@C@,.3)});
@SUB@""", G=GAW, D=wd5, C=wcm, SUB=sub(5)), tr=True, dolly=.06)
ev(5, .05, 'stamp'); ev(5, .3, 'pop')
# 6 bukan gak tahu, tapi lupa
wbk, wlp = W(6, 'bukan', 3.5), W(6, 'lupa', 6)
scene(6, R("""var dr=MK.el('div','left:110px;top:640px;width:260px;height:500px',"@F@",L.root);dr.className='mk-a';
var bb=MK.el('div','left:400px;top:330px;width:600px;height:420px','<svg viewBox="0 0 300 210" width="600" height="420"><path d="M20 20 h260 v140 h-200 l-30 30 v-30 h-30z" fill="#FBF8F3" stroke="#0F0E0C" stroke-width="5" stroke-linejoin="round"/><g stroke="#0F0E0C" stroke-width="4" fill="none"><rect x="44" y="40" width="22" height="22"/><rect x="44" y="76" width="22" height="22"/><rect id="mis" x="44" y="112" width="22" height="22"/></g><g stroke="#B84A2E" stroke-width="5" fill="none"><path d="M47 51 l7 7 l12 -16 M47 87 l7 7 l12 -16"/></g><g stroke="#6B6560" stroke-width="5"><path d="M80 52 h150 M80 88 h130 M80 124 h160"/></g></svg>',L.root);bb.className='mk-a';
var a1=MK.el('div','left:430px;top:820px;width:600px;font-size:52px','bukan karena gak tahu',L.root);a1.className='mk-a mk-ou';
MK.MarkerStrike(L,{x:430,y:820,w:500,h:60,at:@B@+1});
var a2=MK.el('div','left:430px;top:920px;width:600px;font-size:62px;line-height:1.05;color:#B84A2E','tapi karena lupa langkah sederhana',L.root);a2.className='mk-a mk-fr';
MK.MarkerCircle(L,{x:480,y:550,w:60,h:60,at:@L@+.3});
L.on(function(t){var s=Math.sin(t*16)*3;dr.style.transform='translate('+s+'px,0)';var b=MK.E.over(MK.pr(t,.1,.4));bb.style.opacity=b>0?1:0;bb.style.transform='scale('+(.6+.4*b)+')';a1.style.opacity=MK.pr(t,@B@,.3);var k=MK.pr(t,@L@,.35);a2.style.opacity=k;a2.style.transform='translateY('+((1-MK.E.over(k))*30)+'px)';
var m=document.getElementById('mis');if(m)m.setAttribute('stroke',t>@L@&&Math.floor(t*4)%2?'#B84A2E':'#0F0E0C')});
@SUB@""", F=fig('dok', '#5E9C93', '#3f7a72'), B=wbk, L=wlp, SUB=sub(6)), paper='white', dolly=.04)
ev(6, .1, 'pop'); ev(6, wbk + 1, 'scratch'); ev(6, wlp + .3, 'scratch')
# 7 8 RS, 19 poin, kematian 1,5 -> 0,8
w8, w19, wkm = W(7, 'delapan', 2.6), W(7, 'sembilan', 1.6), W(7, 'kematian', 6.3)
scene(7, R("""var hs=[];for(var i=0;i<8;i++){var e=MK.el('div','left:'+(96+(i%4)*228)+'px;top:'+(330+Math.floor(i/4)*190)+'px;width:200px;height:170px','<svg viewBox="0 0 100 85" width="200" height="170"><rect x="10" y="20" width="80" height="60" fill="#FBF8F3" stroke="#0F0E0C" stroke-width="4"/><path d="M44 30 h12 v10 h10 v12 h-10 v10 h-12 v-10 h-10 v-12 h10z" fill="#B84A2E"/></svg>',L.root);e.className='mk-a';hs.push(e)}
var ck=[];for(var i=0;i<19;i++){var e=MK.el('div','left:'+(96+(i%10)*90)+'px;top:'+(740+Math.floor(i/10)*80)+'px;width:62px;height:62px;border-radius:10px;border:4px solid #0F0E0C;background:#FBF8F3;font:800 46px/56px Outfit;text-align:center;color:#B84A2E',' ',L.root);e.className='mk-a';ck.push(e)}
var lb=MK.el('div','left:96px;top:900px;font-size:30px;color:#6B6560','checklist 19 poin',L.root);lb.className='mk-a mk-mono';
function bar(y,w,at,col,lab){var b=MK.el('div','left:96px;top:'+y+'px;height:90px;width:'+w+'px;background:'+col+';border:5px solid #0F0E0C;border-radius:10px;transform-origin:left',' ',L.root);b.className='mk-a';var l=MK.el('div','left:'+(120+w)+'px;top:'+(y+10)+'px;font-size:56px',lab,L.root);l.className='mk-a mk-fr';L.on(function(t){var k=MK.E.out(MK.pr(t,at,.6));b.style.transform='scaleX('+k+')';b.style.opacity=k>0?1:0;l.style.opacity=MK.pr(t,at+.4,.3)});}
bar(980,600,@K@-.4,'#6B6560','1,5%');bar(1100,320,@K@+.4,'#B84A2E','0,8%');
var cap=MK.el('div','left:96px;top:1210px;font-size:24px;color:#6B6560','angka kematian pasien · sebelum vs sesudah checklist · NEJM 2009',L.root);cap.className='mk-a mk-mono';
L.on(function(t){for(var i=0;i<8;i++){var k=MK.pr(t,@E@-1+i*.12,.25);hs[i].style.opacity=k>0?1:0;hs[i].style.transform='scale('+(.5+.5*MK.E.over(k))+')'}
for(var i=0;i<19;i++){ck[i].style.opacity=t>@S@-.3?1:0;ck[i].textContent=t>@S@+i*.07?'✓':''}lb.style.opacity=MK.pr(t,@S@,.3);cap.style.opacity=MK.pr(t,@K@,.3)});
@SUB@""", E=w8, S=w19, K=wkm, SUB=sub(7)), dolly=.04)
[ev(7, w8 - 1 + i * .24, 'tick') for i in range(4)]; ev(7, w19 + .4, 'tick'); ev(7, w19 + .9, 'tick'); ev(7, wkm - .4, 'draw'); ev(7, wkm + .4, 'draw'); ev(7, wkm + 1, 'chime')
# 8 RUMUS: 4 ubin kokpit -> bisnis
wau, wru, wly, wam = W(8, 'autopilotnya', 2.1), W(8, 'rutenya', 4.4), W(8, 'layarnya', 9.5), W(8, 'ambil', 13.7)
TL = [('AUTOPILOT', 'checklist kerja', '<rect x="14" y="10" width="68" height="80" rx="8" fill="#FBF8F3" stroke="#0F0E0C" stroke-width="5"/><path d="M26 32 l6 6 l10 -12 M26 54 l6 6 l10 -12 M26 76 l6 6 l10 -12" stroke="#B84A2E" stroke-width="5" fill="none"/><path d="M50 36 h22 M50 58 h22 M50 80 h22" stroke="#0F0E0C" stroke-width="4"/>', wau),
      ('RUTE', 'standar: chat ≤ 5 menit', '<path d="M24 8 h48 M24 88 h48 M28 8 q0 30 20 40 q-20 10 -20 40 M68 8 q0 30 -20 40 q20 10 20 40" fill="none" stroke="#0F0E0C" stroke-width="5"/><path id="sand" d="M36 70 h24 l-12 -14z" fill="#C8944A"/>', wru),
      ('LAYAR', '2–3 angka tiap Jumat', '<rect x="6" y="14" width="84" height="62" rx="8" fill="#0F0E0C"/><path id="lg" d="M14 62 L32 48 L48 54 L66 34 L82 26" fill="none" stroke="#7FD6A0" stroke-width="5"/><path d="M38 76 v12 M58 76 v12 M28 88 h40" stroke="#0F0E0C" stroke-width="5"/>', wly),
      ('AMBIL ALIH', 'saat angka meleset', '<circle cx="48" cy="48" r="36" fill="#FBF8F3" stroke="#0F0E0C" stroke-width="5"/><circle id="rl" cx="48" cy="48" r="22" fill="#6B6560"/>', wam)]
b8 = "var hd=MK.el('div','left:96px;top:290px;width:888px;font-size:60px','Rumus autopilot bisnis',L.root);hd.className='mk-a mk-fr';L.on(function(t){hd.style.opacity=MK.pr(t,.05,.3)});"
for j, (nm_, sb, ic, at) in enumerate(TL):
    x, y = 96 + (j % 2) * 458, 400 + (j // 2) * 470
    b8 += R("""P(L,@X@,@Y@,430,440,'<div style="width:430px;height:440px;border-radius:22px;background:#FBF8F3;border:6px solid #0F0E0C;box-shadow:0 18px 34px -20px rgba(15,14,12,.5);padding:26px;box-sizing:border-box"><svg viewBox="0 0 96 96" width="170" height="170">@I@</svg><div class="mk-fr" style="font-size:46px;line-height:1;margin-top:14px;color:@C@">@N@</div><div class="mk-ou" style="font-size:30px;color:#6B6560;margin-top:10px">@S@</div></div>',@A@);""",
            X=x, Y=y, I=ic, N=nm_, S=sb, A=at, C='#B84A2E' if j == 3 else '#0F0E0C')
    ev(8, at, 'pop')
b8 += R("""L.on(function(t){var r=document.getElementById('rl');if(r)r.setAttribute('fill',t>@A@+.4&&Math.floor(t*3)%2?'#B84A2E':'#6B6560');var s=document.getElementById('sand');if(s)s.setAttribute('transform','translate(0,'+(-MK.pr(t,@R@,4)*30)+')')});""", A=wam, R=wru)
scene(8, b8 + sub(8), tr=True, dolly=.04)
# 9 pertanyaan tim menumpuk -> pilih satu
wdt9, wbl = W(9, 'ditanyakan', 2.4), W(9, 'balas', 4.6)
QS = ['cara balas chat?', 'stok habis gimana?', 'boleh kasih diskon?', 'resi telat, bilang apa?', 'balas chat calon pembeli gimana?', 'retur boleh?']
scene(9, R("""var ow=MK.el('div','left:110px;top:840px;width:230px;height:440px',"@F@",L.root);ow.className='mk-a';
var qs=@Q@,el=[];for(var i=0;i<qs.length;i++){var e=MK.el('div','left:'+(380+(i%2)*40)+'px;top:'+(330+i*130)+'px;max-width:560px;padding:18px 26px;border-radius:24px 24px 24px 6px;background:#FBF8F3;border:4px solid #0F0E0C;font-size:36px',qs[i],L.root);e.className='mk-a mk-ou';el.push(e)}
L.on(function(t){for(var i=0;i<qs.length;i++){var k=MK.pr(t,@D@-1.4+i*.28,.3);el[i].style.opacity=k>0?(t>@B@&&i!=4?.3:1):0;el[i].style.transform='translateX('+((1-MK.E.over(k))*300)+'px) scale('+(t>@B@&&i==4?1.08:1)+')';if(i==4){el[i].style.background=t>@B@?'#C8944A':'#FBF8F3'}}ow.style.transform='rotate('+(Math.sin(t*3)*2)+'deg)'});
@SUB@""", F=fig('own', '#B84A2E', '#8f3a24'), Q=json.dumps(QS), D=wdt9, B=wbl, SUB=sub(9)), tr=True)
[ev(9, wdt9 - 1.4 + i * .28, 'tick') for i in range(6)]; ev(9, wbl, 'pop')
# 10 papan klip 5 baris tulisan tangan
rows = [('balas', 'Balas maksimal 5 menit'), ('sapa', 'Sapa pakai nama'), ('tanya', 'Tanya kebutuhannya'), ('kasih', 'Kasih 2 pilihan produk'), ('catat', 'Catat hasilnya')]
ats = []
a_, cnt = starts[10], 0
for wd_, _ in rows:
    at = None
    for jj in range(a_, starts[11]):
        if nrm(words[jj]['w']).startswith(wd_):
            if wd_ == 'balas' and nrm(words[jj]['w']) != 'balas': continue
            at = round(words[jj]['t'] - T0[10], 2); break
    ats.append(at if at is not None else 1 + len(ats))
scene(10, R("""var cb=MK.el('div','left:110px;top:300px;width:860px;height:1020px;border-radius:24px;background:#C8944A;border:7px solid #0F0E0C;padding:46px 40px;box-sizing:border-box','<div style="width:100%;height:100%;background:#FBF8F3;border:4px solid #0F0E0C;border-radius:8px;padding:34px;box-sizing:border-box"><div class="mk-mono" style="font-size:26px;color:#6B6560">CHECKLIST</div><div class="mk-fr" style="font-size:52px;line-height:1.05;margin:8px 0 22px">Balas chat calon pembeli</div><div id="rw"></div></div>',L.root);cb.className='mk-a';
var clip=MK.el('div','left:430px;top:268px;width:220px;height:70px;border-radius:14px;background:#6B6560;border:6px solid #0F0E0C',' ',L.root);clip.className='mk-a';
var R5=@R@,A5=@A@;
L.on(function(t){var k=MK.E.over(MK.pr(t,0,.45));cb.style.transform=clip.style.transform='translateY('+((1-k)*400)+'px)';var w=document.getElementById('rw');if(!w)return;var h='';for(var i=0;i<5;i++){if(t<A5[i]-.1)break;var p=Math.min(1,(t-A5[i]+.1)/.6),s=R5[i],n=Math.ceil(s.length*p);h+='<div style="display:flex;align-items:center;gap:22px;margin:22px 0"><div style="width:58px;height:58px;border:5px solid #0F0E0C;border-radius:10px;font:800 50px/50px Outfit;text-align:center;color:#B84A2E">'+(p>=1?'✓':'')+'</div><div class="mk-ou" style="font-size:44px;font-family:Caveat,Outfit;color:#0F0E0C">'+s.slice(0,n)+'</div></div>'}w.innerHTML=h});""",
  R=json.dumps([r for _, r in rows]), A=json.dumps(ats)), paper='white', dolly=.05)
ev(10, 0, 'slide'); [ev(10, a + .5, 'tick') for a in ats]
# 11 meleset -> perbaiki checklist, bukan marahi orang
wpb, wmr = W(11, 'perbaiki', 1.4), W(11, 'marahin', 3.5)
scene(11, R("""var cd=MK.el('div','left:96px;top:330px;width:888px;padding:30px 36px;border-radius:20px;background:#FBF8F3;border:5px solid #0F0E0C;box-sizing:border-box','<div class="mk-mono" style="font-size:24px;color:#6B6560">CHECKLIST · baris 1</div><div id="l1" class="mk-ou" style="font-size:48px;margin-top:10px">Balas maksimal 5 menit</div><div id="l2" class="mk-ou" style="font-size:48px;margin-top:10px;color:#B84A2E;opacity:0">+ pakai template jawaban</div>',L.root);cd.className='mk-a';
var mel=MK.el('div','left:640px;top:330px;padding:10px 22px;border-radius:999px;background:#B84A2E;color:#FBF8F3;font-size:30px','meleset',L.root);mel.className='mk-a mk-mono';
var pn=MK.el('div','left:0;top:0;width:160px;height:160px','<svg viewBox="0 0 100 100" width="160" height="160"><path d="M20 86 L30 60 L76 14 L88 26 L42 72Z" fill="#C8944A" stroke="#0F0E0C" stroke-width="5" stroke-linejoin="round"/><path d="M20 86 L30 60 L42 72Z" fill="#0F0E0C"/></svg>',L.root);pn.className='mk-a';
var ad=MK.el('div','left:160px;top:820px;width:230px;height:440px',"@F@",L.root);ad.className='mk-a';
var ang=MK.el('div','left:440px;top:880px;width:540px;padding:22px 28px;border-radius:22px;background:#FBF8F3;border:4px solid #0F0E0C;font-size:44px','“Kok lama banget sih?!”',L.root);ang.className='mk-a mk-ou';
MK.MarkerStrike(L,{x:440,y:900,w:520,h:60,at:@M@+.2});
var ok=MK.el('div','left:440px;top:1050px;width:540px;font-size:52px;color:#B84A2E;line-height:1.05','perbaiki prosesnya, bukan orangnya',L.root);ok.className='mk-a mk-fr';
L.on(function(t){cd.style.opacity=MK.pr(t,0,.3);mel.style.opacity=MK.pr(t,.3,.25);var e=document.getElementById('l2');if(e)e.style.opacity=MK.pr(t,@P@+.4,.3);
var u=MK.E.io(MK.pr(t,@P@-.2,.8));pn.style.transform='translate('+(800-u*560+Math.sin(t*14)*5)+'px,'+(500-u*40)+'px)';pn.style.opacity=t>@P@-.3&&t<@P@+1.6?1:0;
ad.style.opacity=MK.pr(t,@M@-1,.3);ang.style.opacity=MK.pr(t,@M@-.8,.3);ok.style.opacity=MK.pr(t,@M@+.8,.3)});
@SUB@""", F=fig('adm', '#0F0E0C', '#2a2622'), P=wpb, M=wmr, SUB=sub(11)), tr=True)
ev(11, .3, 'pop'); ev(11, wpb - .2, 'draw'); ev(11, wmr + .2, 'scratch')
# 12 kamu tetap pilotnya: dari kemudi ke layar pantau
wpl, wky = W(12, 'layar', 3), W(12, 'kemudi', 4.4)
scene(12, R("""var hl=MK.el('div','left:96px;top:300px;width:900px;font-size:100px;line-height:1','Kamu tetap<br><span style="color:#B84A2E">pilotnya.</span>',L.root);hl.className='mk-a mk-fr';L.on(function(t){hl.style.opacity=MK.pr(t,.05,.3)});
var yk=MK.el('div','left:120px;top:900px;width:300px;height:200px','<svg viewBox="0 0 150 100" width="300" height="200"><path d="M20 30 h110 M75 30 v60" stroke="#C8944A" stroke-width="14" stroke-linecap="round"/></svg>',L.root);yk.className='mk-a';
var ds=MK.el('div','left:560px;top:560px;width:420px;height:300px;border-radius:20px;background:#0F0E0C;padding:22px;box-sizing:border-box','<svg viewBox="0 0 380 260" width="376" height="256"><g fill="none" stroke="#7FD6A0" stroke-width="6"><circle cx="70" cy="80" r="46"/><circle cx="190" cy="80" r="46"/><circle cx="310" cy="80" r="46"/></g><g id="nds" stroke="#C8944A" stroke-width="6" stroke-linecap="round"><path id="n1" d="M70 80 v-36"/><path id="n2" d="M190 80 v-36"/><path id="n3" d="M310 80 v-36"/></g><text x="190" y="200" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="26" fill="#FBF8F3">CEK TIAP JUMAT</text></svg>',L.root);ds.className='mk-a';
var ow=MK.el('div','left:200px;top:820px;width:230px;height:440px',"@F@",L.root);ow.className='mk-a';
L.on(function(t){var u=MK.E.io(MK.pr(t,@L@-.4,1.4));ow.style.transform='translateX('+(u*460)+'px)';yk.style.opacity=1-u*.6;ds.style.opacity=MK.pr(t,@L@-.8,.3);
for(var i=1;i<=3;i++){var n=document.getElementById('n'+i);if(n)n.setAttribute('transform','rotate('+(Math.sin(t*(1+i*.4)+i)*50)+' '+(i*120-50)+' 80)')}});
@SUB@""", SUB=sub(12), F=fig('own2', '#B84A2E', '#8f3a24'), L=wpl), tr=True, dolly=.05)
ev(12, .05, 'pop'); ev(12, wpl - .4, 'slide'); ev(12, wky, 'chime')
# 13 SIMPAN
scene(13, """MK.SeriesCard(L,{series:'AUTOPILOT BISNIS',title:'Tulis checklist<br>pertamamu.'});
var b=MK.el('div','left:96px;top:1180px;padding:20px 44px;border-radius:999px;background:#B84A2E;color:#FBF8F3;font-size:44px','Simpan',L.root);b.className='mk-a mk-ou';
L.on(function(t){var k=MK.pr(t,.8,.3);b.style.opacity=k;b.style.transform='scale('+(.8+.2*MK.E.over(k))+')'});""", tr=True)
ev(13, .8, 'chime')
html = ('<!DOCTYPE html>\n<html><head><meta charset="utf-8"><title>Bisnis autopilot</title><link rel="stylesheet" href="motionkit/fonts-mk.css"></head><body>\n'
        '<script src="motionkit/kit.js"></script>\n<script>\nvar C=MK.C;\n' + HELP + '\nMK.run([\n' + ',\n'.join(S) + '\n]);\n</script>\n</body></html>\n')
open(A + 'mk-autopilot.html', 'w', encoding='utf-8').write(html)
json.dump({'duration': tl['duration'], 'events': EV, 'cuts': T0}, open(os.path.join(OUT, 'events.json'), 'w'))
print('ok', len(S), 'adegan', round(sum(DUR), 1), 'dtk'); print([(SC[i][0], DUR[i]) for i in range(len(SC))])
