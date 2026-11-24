"""Reels 'aturan grow: bottleneck': animasi penuh Motion Kit dari timing.json vo_prep.
Pakai: python3 scratch/gen_metrik.py out/reel17/timing.json -> animatic/mk-grow.html + out/reel17/events.json"""
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
SC = [('budget',0,0),('sebelumnya',0,0),
      ('ini',1,0),
      ('eliyahu',2,0),('bisnis',2,1),('jadi',2,0),
      ('caranya',3,0),('lalu',3,0),('perbaiki',3,0),('kalau',3,0),
      ('kirim',4,0)]
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
KEY = {'bottleneck','pipa','sempit','lebarkan','grow','numpuk','perbaiki','pindah','bocor','tumbuh','goldratt','hambatan','kirim','omzetnya','three','sixty','iklan','besar'}
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
# 0 HOOK: tiga panel budget / chat / omzet
wd, wc, wo = W(0, 'dua', 2.8), W(0, 'chat', 4.1), W(0, 'omzetnya', 5.8)
scene(0, R("""MK.Headline(L,{y:280,size:100,html:'Iklan 2x.<br>Omzet <span style="color:'+C.terra+'">gak gerak.</span>'});
function pan(x,ti,at){var e=MK.el('div','left:'+x+'px;top:640px;width:282px;height:470px;border-radius:18px;background:#FBF8F3;border:5px solid #0F0E0C;padding:20px;box-sizing:border-box','<div class="mk-mono" style="font-size:22px;color:#6B6560">'+ti+'</div>',L.root);e.className='mk-a';L.on(function(t){var k=MK.pr(t,at,.3);e.style.opacity=k>0?1:0;e.style.transform='translateY('+((1-MK.E.over(k))*80)+'px)'});return e}
pan(96,'BUDGET IKLAN',.1);pan(399,'CHAT MASUK',.25);pan(702,'OMZET',.4);
var b1=MK.el('div','left:130px;top:960px;width:90px;height:110px;background:#C8944A;border:5px solid #0F0E0C;transform-origin:bottom',' ',L.root);b1.className='mk-a';
var b2=MK.el('div','left:240px;top:850px;width:90px;height:220px;background:#B84A2E;border:5px solid #0F0E0C;transform-origin:bottom',' ',L.root);b2.className='mk-a';
var l1=MK.el('div','left:120px;top:700px;font-size:44px','Rp10jt',L.root);l1.className='mk-a mk-fr';var l2=MK.el('div','left:120px;top:760px;font-size:44px;color:#B84A2E','→ Rp20jt',L.root);l2.className='mk-a mk-fr';
var bub=[];for(var i=0;i<8;i++){var e=MK.el('div','left:'+(424+(i%2)*110)+'px;top:'+(1040-Math.floor(i/2)*80)+'px;width:100px;height:60px;border-radius:18px 18px 18px 4px;background:'+(i%3?'#FBF8F3':'#C8944A')+';border:4px solid #0F0E0C',' ',L.root);e.className='mk-a';bub.push(e)}
var cx=MK.el('div','left:430px;top:700px;font-size:64px;color:#B84A2E','2x',L.root);cx.className='mk-a mk-fr';
MK.InkPath(L,{d:'M730 1000 L790 990 L850 1004 L910 994 L960 1000',w:9,at:@O@,dur:.9,color:'#0F0E0C'});
var fl=MK.el('div','left:730px;top:700px;width:240px;font-size:50px','datar',L.root);fl.className='mk-a mk-fri';
var nt=MK.el('div','left:96px;top:1130px;font-size:24px;color:#6B6560','contoh hitungan',L.root);nt.className='mk-a mk-mono';
L.on(function(t){var k=MK.E.over(MK.pr(t,@D@,.5));b2.style.transform='scaleY('+(.5+.5*k)+')';l2.style.opacity=MK.pr(t,@D@,.3);b1.style.opacity=b2.style.opacity=l1.style.opacity=MK.pr(t,.1,.3);
for(var i=0;i<8;i++){var q=MK.pr(t,@C@+i*.09,.2);bub[i].style.opacity=q>0?1:0;bub[i].style.transform='scale('+(.4+.6*MK.E.over(q))+')'}cx.style.opacity=MK.pr(t,@C@+.6,.3);fl.style.opacity=MK.pr(t,@O@+.6,.3);nt.style.opacity=MK.pr(t,.4,.3)});""", D=wd, C=wc, O=wo))
ev(0, .1, 'slide'); ev(0, wd, 'pop'); [ev(0, wc + i * .18, 'tick') for i in range(4)]; ev(0, wo, 'draw')
# 1 perkenalan
scene(1, R("""var ph=MK.el('div','left:96px;top:420px;width:420px;height:560px;border-radius:12px;overflow:hidden;box-shadow:0 18px 40px -18px rgba(15,14,12,.45);background:#B84A2E','<img src="../foto/profil-seminar.jpg" style="width:100%;height:100%;object-fit:cover;object-position:50% 20%">',L.root);ph.className='mk-a';
var nm=MK.el('div','left:560px;top:430px;width:430px;font-size:76px;line-height:.95','ALDY<br>SYAHREZA',L.root);nm.className='mk-a mk-fr';
MK.PaperCard(L,{x:560,y:650,w:420,at:@A@,from:'right',rot:1,html:'<div class="mk-fr" style="font-size:46px">100+ BRAND</div><div class="mk-ou" style="font-size:26px;color:#6B6560">belasan tahun</div>'});
var c3=MK.el('div','left:600px;top:850px;width:300px;height:300px','<svg viewBox="0 0 200 200" width="300" height="300"><circle cx="100" cy="100" r="80" fill="none" stroke="#E8E1D5" stroke-width="16"/><circle id="r360" cx="100" cy="100" r="80" fill="none" stroke="#B84A2E" stroke-width="16" stroke-linecap="round" stroke-dasharray="503" stroke-dashoffset="503" transform="rotate(-90 100 100)"/><text x="100" y="116" text-anchor="middle" font-family="Fraunces,serif" font-weight="800" font-size="54" fill="#0F0E0C">360°</text></svg>',L.root);c3.className='mk-a';
@SUB@
L.on(function(t){var k=MK.pr(t,.05,.4);ph.style.opacity=k;ph.style.transform='rotate(-2deg) translateY('+((1-MK.E.out(k))*40)+'px)';nm.style.opacity=MK.pr(t,@N@,.3);var r=document.getElementById('r360');var q=MK.E.io(MK.pr(t,@T@,1.2));if(r)r.setAttribute('stroke-dashoffset',503*(1-q));c3.style.opacity=MK.pr(t,@T@-.3,.3)});""",
  A=W(1, 'seratus', 4), T=W(1, 'three', 6.6), N=W(1, 'aldy', 1.6) - .2, SUB=sub(1)))
ev(1, .05, 'slide'); ev(1, W(1, 'seratus', 4), 'pop'); ev(1, W(1, 'three', 6.6), 'draw')
# 2 RELATE: admin tenggelam chat, malam, pembeli pindah
wm, wb, wp = W(2, 'menumpuk', 2.1), W(2, 'besok', 5.7), W(2, 'pembelinya', 6.9)
scene(2, R("""var a1=MK.el('div','left:120px;top:780px;width:200px;height:380px',"@F1@",L.root);a1.className='mk-a';var a2=MK.el('div','left:300px;top:780px;width:200px;height:380px',"@F2@",L.root);a2.className='mk-a';
var dk=MK.el('div','left:90px;top:1060px;width:470px;height:40px;background:#7a5230;border:5px solid #0F0E0C;border-radius:6px',' ',L.root);dk.className='mk-a';
var bub=[];for(var i=0;i<16;i++){var e=MK.el('div','left:'+(110+(i*67)%390)+'px;top:0px;width:110px;height:56px;border-radius:18px 18px 18px 4px;background:'+(i%4?'#FBF8F3':'#C8944A')+';border:4px solid #0F0E0C',' ',L.root);e.className='mk-a';bub.push(e)}
MK.CountUp(L,{x:110,y:330,from:0,to:148,at:@M@,dur:1.6,size:96,suffix:'chat belum dibalas'});
var sky=MK.el('div','left:620px;top:330px;width:360px;height:200px;border-radius:18px;border:5px solid #0F0E0C;background:#FBF8F3;overflow:hidden','<svg viewBox="0 0 360 200" width="360" height="200"><circle id="mn" cx="270" cy="70" r="38" fill="#C8944A"/><text x="30" y="170" font-family="JetBrains Mono,monospace" font-size="28" fill="#FBF8F3" id="mt">dibalas: besok 08.00</text></svg>',L.root);sky.className='mk-a';
var shop=MK.el('div','left:760px;top:760px;width:250px;height:300px','<svg viewBox="0 0 250 300" width="250" height="300"><path d="M20 90 L40 30 H210 L230 90Z" fill="#B84A2E" stroke="#0F0E0C" stroke-width="6"/><rect x="34" y="90" width="182" height="190" fill="#FBF8F3" stroke="#0F0E0C" stroke-width="6"/><rect x="96" y="170" width="58" height="110" fill="#C8944A" stroke="#0F0E0C" stroke-width="5"/><text x="125" y="72" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="20" fill="#FBF8F3">TOKO SEBELAH</text></svg>',L.root);shop.className='mk-a';
var by=MK.el('div','left:560px;top:820px;width:150px;height:285px',"@F3@",L.root);by.className='mk-a';
L.on(function(t){for(var i=0;i<16;i++){var at=@M@-.6+i*.12,k=MK.pr(t,at,.4);var ty=440+Math.floor(i/4)*70;bub[i].style.top=(k>0?(ty-(1-MK.E.out(k))*500):-200)+'px';bub[i].style.opacity=k>0?1:0;bub[i].style.transform='rotate('+((i%5)-2)*4+'deg)'}
var n=MK.pr(t,@B@-.4,.5);sky.style.opacity=MK.pr(t,@B@-.6,.3);sky.style.background=n>.5?'#2A2824':'#FBF8F3';
var w=MK.pr(t,@P@,1.6);by.style.transform='translateX('+(w*260)+'px)';by.style.opacity=t>@P@-.6?1:0;shop.style.opacity=MK.pr(t,@P@-.5,.3);
var sh=Math.sin(t*20)*2;a1.style.transform='translateY('+sh+'px)';a2.style.transform='translateY('+(-sh)+'px)'});
@SUB@""", F1=fig('ad1', '#0F0E0C', '#2a2622'), F2=fig('ad2', '#C8944A', '#a57a35'), F3=fig('by1', '#6B6560', '#4a4540'), M=wm, B=wb, P=wp, SUB=sub(2)), tr=True, dolly=.05)
ev(2, wm, 'pop'); [ev(2, wm - .6 + i * .36, 'tick') for i in range(5)]; ev(2, wb - .4, 'slide'); ev(2, wp, 'sweep')
# 3 KARTU TOKOH Goldratt
wf, wt_, wh = W(3, 'fisikawan', .9), W(3, 'the', 2.8), W(3, 'hambatan', 4)
GOLD = ('<svg viewBox="0 0 260 360" width="300" height="415"><rect x="40" y="200" width="180" height="170" rx="60" fill="#2A2824"/>'
        '<path d="M110 200 L130 250 L150 200Z" fill="#FBF8F3"/><path d="M128 210 L134 214 L130 270 L126 214Z" fill="#B84A2E"/>'
        '<rect x="112" y="160" width="36" height="40" fill="#F1C9A3"/><circle cx="130" cy="118" r="58" fill="#F1C9A3"/>'
        '<path d="M76 130 Q80 196 130 200 Q180 196 184 130 Q170 160 130 162 Q90 160 76 130Z" fill="#9a9590"/>'
        '<path d="M74 104 Q80 56 130 56 Q180 56 186 104 Q170 82 130 82 Q92 82 74 104Z" fill="#6B6560"/>'
        '<g fill="none" stroke="#0F0E0C" stroke-width="5"><circle cx="108" cy="118" r="17"/><circle cx="152" cy="118" r="17"/><path d="M125 118 h10"/></g>'
        '<g transform="rotate(-8 200 300)"><rect x="150" y="250" width="100" height="120" rx="6" fill="#C8944A" stroke="#0F0E0C" stroke-width="5"/>'
        '<text x="200" y="318" text-anchor="middle" font-family="Fraunces,serif" font-weight="800" font-size="24" fill="#0F0E0C">THE GOAL</text></g></svg>')
scene(3, R("""var fr=MK.el('div','left:96px;top:330px;width:888px;height:920px;border-radius:24px;background:#FBF8F3;border:6px solid #0F0E0C;box-shadow:0 30px 60px -30px rgba(15,14,12,.5)',' ',L.root);fr.className='mk-a';
var tg=MK.el('div','left:140px;top:370px;font-size:26px;letter-spacing:.1em;color:#B84A2E','KARTU TOKOH',L.root);tg.className='mk-a mk-mono';
var pt=MK.el('div','left:390px;top:410px;width:300px;height:415px','@G@',L.root);pt.className='mk-a';
var nm=MK.el('div','left:140px;top:850px;width:800px;text-align:center;font-size:74px;line-height:1','ELIYAHU GOLDRATT',L.root);nm.className='mk-a mk-fr';
var s1=MK.el('div','left:140px;top:945px;width:800px;text-align:center;font-size:32px','Fisikawan & pakar manajemen · Israel (1947–2011)',L.root);s1.className='mk-a mk-ou';
var s2=MK.el('div','left:140px;top:995px;width:800px;text-align:center;font-size:32px;color:#B84A2E','Penulis <i>The Goal</i> (1984), pencetus Theory of Constraints',L.root);s2.className='mk-a mk-ou';
var bt=MK.el('div','left:270px;top:1140px;width:540px;text-align:center;padding:14px 0;border-radius:999px;background:#0F0E0C;color:#FBF8F3;font-size:40px','“hambatan” = bottleneck',L.root);bt.className='mk-a mk-ou';
L.on(function(t){var k=MK.E.over(MK.pr(t,.05,.45));fr.style.opacity=k>0?1:0;fr.style.transform='rotate(-1.5deg) scale('+(.8+.2*k)+')';tg.style.opacity=MK.pr(t,.2,.3);
var p=MK.E.over(MK.pr(t,.2,.5));pt.style.opacity=p>0?1:0;pt.style.transform='translateY('+((1-p)*80)+'px) rotate('+(Math.sin(t*1.5)*1.5)+'deg)';nm.style.opacity=MK.pr(t,.35,.3);s1.style.opacity=MK.pr(t,@F@,.3);s2.style.opacity=MK.pr(t,@T@,.3);
var b=MK.pr(t,@H@,.3);bt.style.opacity=b;bt.style.transform='scale('+(.6+.4*MK.E.over(b))+')'});
@SUB@""", G=GOLD, F=wf, T=wt_, H=wh, SUB=sub(3)), tr=True, dolly=.06)
ev(3, .05, 'stamp'); ev(3, .3, 'pop'); ev(3, wh, 'pop')
# 4 PIPA: air dituang, keluar menetes, meluap
whv, wsp = W(4, 'seberapa', 2), W(4, 'sempit', 6.3)
scene(4, R("""var hd=MK.el('div','left:96px;top:300px;width:888px;font-size:88px;line-height:1','Bisnis itu<br>kayak <span style="color:#B84A2E">pipa.</span>',L.root);hd.className='mk-a mk-fr';L.on(function(t){hd.style.opacity=MK.pr(t,.05,.3)});
PIPE(L,{id:'p4',y:850,at:.1,nar:2,flowAt:.6,heavyAt:@H@,overAt:@H@+.8});
var gl=MK.el('div','left:770px;top:1220px;width:280px;font-size:40px;color:#6B6560','cuma menetes',L.root);gl.className='mk-a mk-fri';L.on(function(t){gl.style.opacity=MK.pr(t,@H@+1.2,.3)});
MK.MarkerCircle(L,{x:454,y:820,w:172,h:60,at:@S@});
@SUB@""", H=whv, S=wsp, SUB=sub(4)), dolly=.05)
ev(4, .1, 'slide'); ev(4, .6, 'splash'); ev(4, whv, 'splash'); ev(4, whv + .8, 'splash'); ev(4, wsp, 'scratch')
# 5 ATURAN GROW #1: coret 'tambah yang besar', lebarkan yang sempit
wbs, wlb = W(5, 'besar', 3.6), W(5, 'lebarkan', 4.6)
scene(5, chip('ATURAN GROW #1', 280) + R("""
var r1=MK.el('div','left:96px;top:370px;width:888px;font-size:52px;line-height:1.1;white-space:nowrap','Jangan tambah yang udah besar.',L.root);r1.className='mk-a mk-fr';
MK.MarkerStrike(L,{x:96,y:378,w:760,h:50,at:@B@});
var r2=MK.el('div','left:96px;top:480px;width:888px;font-size:80px;line-height:1.05;color:#B84A2E','Lebarkan yang paling sempit.',L.root);r2.className='mk-a mk-fr';
PIPE(L,{id:'p5',y:1000,at:-1,nar:2,flowAt:-1,heavyAt:-1,overAt:-1,widenAt:@L@});
var ok=MK.el('div','left:760px;top:1300px;width:300px;font-size:40px;color:#B84A2E','mengalir penuh',L.root);ok.className='mk-a mk-fri';
L.on(function(t){r1.style.opacity=MK.pr(t,.3,.3);var k=MK.pr(t,@L@-.2,.35);r2.style.opacity=k;r2.style.transform='translateY('+((1-MK.E.over(k))*30)+'px)';ok.style.opacity=MK.pr(t,@L@+1,.3)});""", B=wbs, L=wlb), tr=True)
ev(5, .05, 'pop'); ev(5, wbs, 'scratch'); ev(5, wlb, 'sweep'); ev(5, wlb + .9, 'chime')
# 6 CARANYA: gambar alur dengan ikon stasiun
ST = [('iklan', 'IKLAN', '<path d="M14 40 h18 l40 -24 v68 l-40 -24 h-18z" fill="#C8944A" stroke="#0F0E0C" stroke-width="6" stroke-linejoin="round"/>'),
      ('chat', 'CHAT', '<path d="M10 14 h76 v48 H40 l-18 16 V62 H10z" fill="#FBF8F3" stroke="#0F0E0C" stroke-width="6" stroke-linejoin="round"/>'),
      ('closing', 'CLOSING', '<circle cx="48" cy="48" r="36" fill="#B84A2E" stroke="#0F0E0C" stroke-width="6"/><path d="M30 50 l12 12 l24 -28" fill="none" stroke="#FBF8F3" stroke-width="8" stroke-linecap="round"/>'),
      ('packing', 'PACKING', '<path d="M12 30 L48 14 L84 30 V72 L48 88 L12 72Z" fill="#C8944A" stroke="#0F0E0C" stroke-width="6" stroke-linejoin="round"/><path d="M12 30 L48 46 L84 30 M48 46 V88" fill="none" stroke="#0F0E0C" stroke-width="5"/>'),
      ('kirim', 'KIRIM', '<rect x="6" y="28" width="56" height="40" fill="#FBF8F3" stroke="#0F0E0C" stroke-width="6"/><path d="M62 40 h18 l12 14 v14 h-30z" fill="#B84A2E" stroke="#0F0E0C" stroke-width="6" stroke-linejoin="round"/><circle cx="24" cy="74" r="9" fill="#0F0E0C"/><circle cx="74" cy="74" r="9" fill="#0F0E0C"/>')]
pts6 = [(190, 560), (540, 470), (890, 640), (620, 880), (260, 1040)]
b6 = R("""var hd=MK.el('div','left:96px;top:300px;font-size:30px;color:#6B6560','ALUR BISNISKU: dari iklan sampai barang diterima',L.root);hd.className='mk-a mk-mono';L.on(function(t){hd.style.opacity=MK.pr(t,.1,.3)});
MK.InkPath(L,{d:'M190 560 Q360 440 540 470 Q760 500 890 640 Q900 820 620 880 Q420 930 260 1040',w:7,at:@A@,dur:@D@,color:'#6B6560'});""", A=W(6, 'iklan', 1.3) - .3, D=max(1.0, W(6, 'kirim', 6.5) - W(6, 'iklan', 1.3)))
for j, ((wd_, lb, ic), (x, y)) in enumerate(zip(ST, pts6)):
    at = W(6, wd_, 3 + j * .6) if j else [w for w in [W(6, 'iklan', 1.3)]][0]
    if wd_ == 'iklan':
        a_ = starts[6]; cnt = 0; at = 1.3
        for jj in range(a_, starts[7]):
            if nrm(words[jj]['w']).startswith('iklan'):
                cnt += 1
                if cnt == 2: at = round(words[jj]['t'] - T0[6], 2)
    b6 += R("""P(L,@X@,@Y@,200,200,'<div style="width:190px;height:190px;border-radius:50%;background:#FBF8F3;border:6px solid #0F0E0C;display:flex;align-items:center;justify-content:center;box-shadow:0 14px 30px -16px rgba(15,14,12,.5)"><svg viewBox="0 0 96 96" width="110" height="110">@I@</svg></div><div class="mk-fr" style="text-align:center;font-size:36px;margin-top:8px">@L@</div>',@A@);""", X=x - 100, Y=y - 100, I=ic, L=lb, A=at)
    ev(6, at, 'pop')
scene(6, b6 + sub(6), paper='white', dolly=.05)
ev(6, W(6, 'gambar', .5), 'draw')
# 7 LALU CEK: pipa berlabel, tumpukan di CHAT, cap BOTTLENECK
wn, wbn = W(7, 'numpuk', 2.6), W(7, 'bottleneck', 3.6)
scene(7, R("""var hd=MK.el('div','left:96px;top:300px;width:888px;font-size:64px;line-height:1.05','Pekerjaan paling sering <span style="color:#B84A2E">numpuk</span> di mana?',L.root);hd.className='mk-a mk-fr';L.on(function(t){hd.style.opacity=MK.pr(t,.05,.3)});
PIPE(L,{id:'p7',y:900,at:.05,nar:1,flowAt:.3,overAt:.8,labels:['IKLAN','CHAT','CLOSING','PACKING','KIRIM'],hi:1,hiAt:@N@,piles:[{idx:1,at:@N@-1,cnt:7,chat:true},{idx:3,at:@N@-.5,cnt:2,col:'#C8944A'}]});
MK.StampBocor(L,{x:150,y:1230,at:@B@,rot:-5,size:70,text:'BOTTLENECK'});
@SUB@""", N=wn, B=wbn, SUB=sub(7)), tr=True, dolly=.04)
ev(7, .05, 'slide'); [ev(7, wn - 1 + i * .2, 'tick') for i in range(5)]; ev(7, wbn, 'stamp')
# 8 PERBAIKI DI SITU: lebarkan CHAT, budget iklan digembok
wsp8 = W(8, 'sepeser', 2.5)
scene(8, R("""PIPE(L,{id:'p8',y:700,at:-1,nar:1,flowAt:-1,widenAt:.4,labels:['IKLAN','CHAT','CLOSING','PACKING','KIRIM'],hi:1,piles:[{idx:1,at:-2,cnt:7,chat:true,out:.6}]});
var lk=MK.el('div','left:300px;top:1080px;width:480px;height:280px','<svg viewBox="0 0 240 140" width="480" height="280"><rect x="10" y="40" width="140" height="90" rx="12" fill="#C8944A" stroke="#0F0E0C" stroke-width="6"/><text x="80" y="96" text-anchor="middle" font-family="Fraunces,serif" font-weight="800" font-size="30" fill="#0F0E0C">Rp</text><g id="lck"><path d="M170 64 v-18 a22 22 0 0 1 44 0 v18" fill="none" stroke="#0F0E0C" stroke-width="8"/><rect x="160" y="62" width="64" height="56" rx="8" fill="#B84A2E" stroke="#0F0E0C" stroke-width="6"/></g></svg>',L.root);lk.className='mk-a';
var lt=MK.el('div','left:300px;top:1000px;width:600px;font-size:40px','budget iklan: tahan dulu',L.root);lt.className='mk-a mk-fri';
L.on(function(t){var k=MK.pr(t,@S@-.4,.35);lk.style.opacity=lt.style.opacity=k;lk.style.transform='scale('+(.6+.4*MK.E.over(k))+') rotate('+(t>@S@?Math.sin((t-@S@)*30)*Math.max(0,1-(t-@S@)*3)*6:0)+'deg)'});
@SUB@""", S=wsp8, SUB=sub(8)), dolly=.05)
ev(8, .4, 'sweep'); ev(8, 1.2, 'chime'); ev(8, wsp8 - .4, 'pop'); ev(8, wsp8, 'stamp')
# 9 PINDAH: bottleneck pindah ke PACKING, cari lagi, tumbuh tanpa bocor
wpi, wca, wtu = W(9, 'pindah', 2.2), W(9, 'cari', 3), W(9, 'tumbuh', 4.6)
scene(9, R("""var hd=MK.el('div','left:96px;top:300px;width:888px;font-size:64px;line-height:1.05','Bottleneck-nya <span style="color:#B84A2E">pindah.</span>',L.root);hd.className='mk-a mk-fr';L.on(function(t){hd.style.opacity=MK.pr(t,@P@-.3,.3)});
PIPE(L,{id:'p9',y:780,at:-1,nar:3,narrowAt:@P@-.4,flowAt:-1,overAt:@P@+.4,labels:['IKLAN','CHAT','CLOSING','PACKING','KIRIM'],hi:3,hiAt:@P@,piles:[{idx:3,at:@P@,cnt:6,col:'#C8944A'}]});
MK.MarkerCircle(L,{x:626,y:740,w:172,h:80,at:@C@});
var lp=MK.el('div','left:96px;top:1150px;width:888px;height:200px','<svg viewBox="0 0 888 200" width="888" height="200"><path d="M10 170 L150 150 L300 120 L450 120 L600 70 L760 40 L870 10" fill="none" stroke="#B84A2E" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1100" id="gl9" stroke-dashoffset="1100"/></svg>',L.root);lp.className='mk-a';
var gr=MK.el('div','left:96px;top:1100px;font-size:30px;color:#6B6560','cari → perbaiki → ulangi',L.root);gr.className='mk-a mk-mono';
L.on(function(t){var g=document.getElementById('gl9');if(g)g.setAttribute('stroke-dashoffset',1100*(1-MK.E.io(MK.pr(t,@T@-.3,1.2))));gr.style.opacity=MK.pr(t,@C@+.2,.3)});
@SUB@""", P=wpi, C=wca, T=wtu, SUB=sub(9)), tr=True, dolly=.04)
ev(9, wpi - .4, 'slide'); [ev(9, wpi + i * .2, 'tick') for i in range(4)]; ev(9, wca, 'scratch'); ev(9, wtu - .3, 'draw')
# 10 KIRIM: kartu alur jadi pesawat kertas -> kartu seri
scene(10, R("""var pl=MK.el('div','left:380px;top:700px;width:320px;height:220px','<svg viewBox="0 0 160 110" width="320" height="220"><path d="M4 50 L156 4 L100 104 L76 66Z" fill="#FBF8F3" stroke="#0F0E0C" stroke-width="5" stroke-linejoin="round"/><path d="M76 66 L156 4 L60 58Z" fill="#E8E1D5" stroke="#0F0E0C" stroke-width="5" stroke-linejoin="round"/></svg>',L.root);pl.className='mk-a';
var tr=MK.el('div','left:0;top:0;width:1080px;height:1920px','<svg viewBox="0 0 1080 1920" width="1080" height="1920"><path id="tr10" d="M200 1300 Q420 1000 540 810 T1000 400" fill="none" stroke="#6B6560" stroke-width="5" stroke-dasharray="14 14"/></svg>',L.root);tr.className='mk-a';
var sc=MK.el('div','left:0;top:0;width:1080px;height:1920px;background:#0F0E0C',' ',L.root);sc.className='mk-a';
var a=MK.el('div','left:96px;top:760px;font-size:30px;color:#C8944A','ATURAN GROW #1',L.root);a.className='mk-a mk-mono';
var b=MK.el('div','left:96px;top:810px;width:888px;font-size:110px;line-height:1;color:#FBF8F3','Lebarkan yang<br>paling sempit.',L.root);b.className='mk-a mk-fr';
var c=MK.el('div','left:96px;top:1080px;font-size:44px;color:#FBF8F3','@aldysyahreza',L.root);c.className='mk-a mk-ou';
var bt=MK.el('div','left:96px;top:1180px;padding:20px 44px;border-radius:999px;background:#B84A2E;color:#FBF8F3;font-size:44px','Kirim ke tim iklan',L.root);bt.className='mk-a mk-ou';
var cap=MK.el('div','left:96px;right:96px;top:1390px;text-align:center;font-size:62px','Kirim ke <span style="color:#B84A2E">tim iklan</span>',L.root);cap.className='mk-a mk-ou';
L.on(function(t){var f=MK.E.io(MK.pr(t,.3,1.6));pl.style.transform='translate('+(-180+f*640)+'px,'+(520-f*860)+'px) rotate('+(-20+f*10)+'deg) scale('+(1-f*.5)+')';pl.style.opacity=t<1.9?1:0;tr.style.opacity=t<1.9?MK.pr(t,.3,.3):0;cap.style.opacity=t<1.9?1:0;
var d=MK.pr(t,1.9,.25);sc.style.opacity=d;[a,b,c].forEach(function(x,i){var k=MK.pr(t,2+i*.12,.35);x.style.opacity=k;x.style.transform='translateY('+((1-MK.E.out(k))*20)+'px)'});var k=MK.pr(t,2.6,.3);bt.style.opacity=k;bt.style.transform='scale('+(.8+.2*MK.E.over(k))+')'});""" ), tr=True)
ev(10, .3, 'sweep'); ev(10, 1.9, 'slide'); ev(10, 2.6, 'chime')
html = ('<!DOCTYPE html>\n<html><head><meta charset="utf-8"><title>Aturan grow bottleneck</title><link rel="stylesheet" href="motionkit/fonts-mk.css"></head><body>\n'
        '<script src="motionkit/kit.js"></script>\n<script>\nvar C=MK.C;\n' + HELP + '\nMK.run([\n' + ',\n'.join(S) + '\n]);\n</script>\n</body></html>\n')
open(A + 'mk-grow.html', 'w', encoding='utf-8').write(html)
json.dump({'duration': tl['duration'], 'events': EV, 'cuts': T0}, open(os.path.join(OUT, 'events.json'), 'w'))
print('ok', len(S), 'adegan', round(sum(DUR), 1), 'dtk'); print([(SC[i][0], DUR[i]) for i in range(len(SC))])
