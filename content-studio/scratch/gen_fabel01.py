"""Fabel Bisnis #01 ekor tikus: animasi penuh Motion Kit dari timing.json vo_prep.
Pakai: python3 scratch/gen_metrik.py out/reel17/timing.json -> animatic/mk-fabel01.html + out/reel17/events.json"""
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
SC = [('seorang',0,0),('dalam',0,0),('tuan',0,0),
      ('tapi',1,0),('warga',1,0),('beberapa',1,0),
      ('di',2,0),('begitu',2,0),
      ('kamu',3,0),('admin',3,0),('tim',3,0),('sales',3,0),('ekornya',3,0),
      ('jadi',4,0)]
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
KEY = {'koin','ekor','tikus','tikusnya','gudang','dibayar','goodhart','target','angkanya','tujuannya','ekornya','mejamu','banyak','bersih'}
def chunks(i):
    a = starts[i]; b = starts[i + 1] if i + 1 < len(starts) else len(words)
    out, cur, t0 = [], [], None
    for j in range(a, b):
        w = words[j]['w']
        if t0 is None: t0 = words[j]['t'] - T0[i] + .03
        clean = w.rstrip('.,:;?')
        cur.append('*%s*' % clean if nrm(w) in KEY else clean)
        if len(cur) == 1 or re.search(r'[.,?!:]$', w) or j == b - 1:
            out.append([round(max(0, t0), 2), ' '.join(cur)]); cur, t0 = [], None
    return out
def W(i, word, d):
    a = starts[i]; b = starts[i + 1] if i + 1 < len(starts) else len(words)
    for j in range(a, b):
        if nrm(words[j]['w']).startswith(word): return round(words[j]['t'] - T0[i], 2)
    return d
EV = []
def ev(i, local, kind): EV.append([round(T0[i] + local, 3), kind])
sub = lambda i, c='#FBF8F3', y=1420: 'MK.Subtitle(L,%s,{y:%d,color:"%s",dark:true});' % (json.dumps(chunks(i), ensure_ascii=False), y, c)
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
FAB = r"""
function DARK(L,o){o=o||{};var d=MK.el('div','left:0;top:0;width:1080px;height:1920px;background:'+(o.bg||'radial-gradient(120% 80% at 50% 30%,#2a231c 0%,#14110e 55%,#0b0a08 100%)'),' ',L.root);d.className='mk-a';
 if(o.moon){var m=MK.el('div','left:780px;top:230px;width:110px;height:110px;border-radius:50%;background:#F4EBD9;box-shadow:0 0 80px 20px rgba(244,235,217,.18)',' ',L.root);m.className='mk-a';}
 if(o.stars){for(var i=0;i<26;i++){var s=MK.el('div','left:'+((i*137)%1040+20)+'px;top:'+((i*89)%560+120)+'px;width:4px;height:4px;border-radius:50%;background:#F4EBD9;opacity:'+(.25+(i%4)*.15),' ',L.root);s.className='mk-a';}}
 return d;}
function RAT(c,tail){c=c||'#8a827a';return '<svg viewBox="0 0 160 90" width="160" height="90" style="overflow:visible"><path d="M30 60 Q30 24 80 24 Q120 24 128 52 L150 60 Q120 72 90 70 L44 70 Q30 70 30 60Z" fill="'+c+'" stroke="#0F0E0C" stroke-width="4"/><circle cx="112" cy="30" r="11" fill="'+c+'" stroke="#0F0E0C" stroke-width="4"/><circle cx="130" cy="50" r="3.5" fill="#0F0E0C"/><circle cx="150" cy="60" r="4" fill="#B84A2E"/>'+(tail===false?'':'<path d="M32 62 Q4 60 8 36 Q12 18 -6 10" fill="none" stroke="#D98C7A" stroke-width="5" stroke-linecap="round"/>')+'</svg>';}
function TAIL(){return '<svg viewBox="0 0 80 40" width="80" height="40"><path d="M4 30 Q30 34 44 18 Q56 4 76 10" fill="none" stroke="#D98C7A" stroke-width="6" stroke-linecap="round"/></svg>';}
function COIN(sz){sz=sz||70;return '<div style="width:'+sz+'px;height:'+sz+'px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#F0C77E,#C8944A 60%,#8a6326);border:4px solid #0F0E0C;box-shadow:inset 0 0 0 6px rgba(15,14,12,.25)"></div>';}
function LINE(w,h,inner){return '<svg viewBox="0 0 '+w+' '+h+'" width="'+w+'" height="'+h+'" style="overflow:visible"><g fill="none" stroke="#F4EBD9" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">'+inner+'</g></svg>';}
function LFIG(){return '<circle cx="50" cy="26" r="20"/><path d="M50 46 V130 M50 70 L18 104 M50 70 L82 100 M50 130 L28 190 M50 130 L72 190"/>';}
function GLOW(L,x,y,r,at){var g=MK.el('div','left:'+(x-r)+'px;top:'+(y-r)+'px;width:'+(2*r)+'px;height:'+(2*r)+'px;border-radius:50%;background:radial-gradient(circle,rgba(200,148,74,.45),rgba(200,148,74,0) 70%)',' ',L.root);g.className='mk-a';L.on(function(t){g.style.opacity=MK.pr(t,at||0,.6)*(.85+Math.sin(t*7)*.08+Math.sin(t*13)*.05)});return g;}
"""
LORD = fig('lord', '#2f4a3a', '#22362a')
VILR = [person('vr%d' % i, c, d, '#2a1d14').replace('\n', '') for i, (c, d) in enumerate([('#B84A2E', '#8f3a24'), ('#C8944A', '#a57a35'), ('#6B6560', '#4a4540'), ('#8a5a3a', '#6a442c'), ('#3e5a6b', '#2d4350')])]
VIL = [fig('v%d' % i, c, d) for i, (c, d) in enumerate([('#B84A2E', '#8f3a24'), ('#C8944A', '#a57a35'), ('#6B6560', '#4a4540'), ('#8a5a3a', '#6a442c'), ('#3e5a6b', '#2d4350')])]
# 0 FRAME 1: tangan menjatuhkan koin ke ekor tikus, meja tuan tanah
wk, we = W(0, 'koin', 2.4), W(0, 'ekor', 3.8)
scene(0, R("""DARK(L);GLOW(L,800,520,360,0);
var hl=MK.el('div','left:96px;top:270px;width:900px;font-size:92px;line-height:1.02;color:#F4EBD9','Satu koin<br>untuk satu <span style="color:#D98C7A">ekor.</span>',L.root);hl.className='mk-a mk-fr';L.headline=true;
var tb=MK.el('div','left:-20px;top:1050px;width:1120px;height:900px;background:linear-gradient(#5a3b24,#3d2817);border-top:8px solid #0F0E0C',' ',L.root);tb.className='mk-a';
var ln=MK.el('div','left:880px;top:760px;width:120px;height:300px','<svg viewBox="0 0 60 150" width="120" height="300"><path d="M30 0 V20" stroke="#0F0E0C" stroke-width="5"/><rect x="12" y="20" width="36" height="60" rx="8" fill="#F0C77E" stroke="#0F0E0C" stroke-width="5"/><path d="M8 80 h44 v10 h-44z" fill="#0F0E0C"/></svg>',L.root);ln.className='mk-a';
var tl=[];for(var i=0;i<9;i++){var e=MK.el('div','left:'+(470+(i%3)*90+(i>5?40:0))+'px;top:'+(1010-Math.floor(i/3)*22)+'px;width:80px;height:40px',TAIL(),L.root);e.className='mk-a';e.style.transform='rotate('+((i*37)%40-20)+'deg)';tl.push(e)}
var cn=MK.el('div','left:620px;top:0;width:90px;height:90px',COIN(90),L.root);cn.className='mk-a';
var hd=MK.el('div','left:570px;top:0;width:200px;height:260px','<svg viewBox="0 0 100 130" width="200" height="260"><path d="M30 0 V60 Q30 90 50 92 Q72 92 74 66 V0Z" fill="#F1C9A3" stroke="#0F0E0C" stroke-width="5"/><rect x="24" y="-40" width="56" height="50" fill="#2f4a3a" stroke="#0F0E0C" stroke-width="5"/></svg>',L.root);hd.className='mk-a';
L.on(function(t){var d=MK.E.out(MK.pr(t,.2,.7));hd.style.transform='translateY('+(560+d*120)+'px)';hd.style.opacity=t>@K@+.3?Math.max(0,1-(t-@K@-.3)*3):1;var f=t<@K@?0:Math.min(1,(t-@K@)/.35);cn.style.transform='translateY('+(800+f*f*180)+'px) rotate('+(f*200)+'deg)';cn.style.opacity=t>@K@-.05?1:0;
for(var i=0;i<9;i++)tl[i].style.opacity=t>@E@-.6+i*.05?1:.0});
@SUB@""", K=wk, E=we, SUB=sub(0)))
ev(0, wk + .35, 'tick'); ev(0, we, 'pop')
# 1 antre warga menyerahkan ekor, tumpukan naik + hitung
wr = W(1, 'ribuan', 1.2)
scene(1, R("""DARK(L,{stars:true});GLOW(L,880,700,300,0);
var tb=MK.el('div','left:620px;top:1060px;width:520px;height:120px;background:#5a3b24;border:6px solid #0F0E0C;border-radius:8px',' ',L.root);tb.className='mk-a';
var lord=MK.el('div','left:800px;top:620px;width:250px;height:470px',"@LORD@",L.root);lord.className='mk-a';
var V=@V@,vv=[];for(var i=0;i<5;i++){var e=MK.el('div','left:0;top:760px;width:190px;height:360px',V[i],L.root);e.className='mk-a';vv.push(e)}
var pile=MK.el('div','left:640px;top:0;width:240px;height:400px',' ',L.root);pile.className='mk-a';var ph='';for(var i=0;i<30;i++)ph+='<div style="position:absolute;left:'+((i*53)%170)+'px;bottom:'+(Math.floor(i/4)*16)+'px;transform:rotate('+((i*41)%60-30)+'deg)">'+TAIL()+'</div>';pile.innerHTML=ph;
MK.CountUp(L,{x:96,y:300,from:0,to:1284,at:@R@,dur:1.6,size:130,suffix:'ekor',color:'#F4EBD9'});
L.on(function(t){for(var i=0;i<5;i++){var x=20+i*120+Math.min(1,t/3)*60-(i==4?0:0);vv[i].style.transform='translateX('+x+'px) translateY('+(Math.abs(Math.sin(t*6+i))*-8)+'px)'}var n=Math.min(30,Math.floor(t*4));var ch=pile.children;for(var i=0;i<ch.length;i++)ch[i].style.opacity=i<n?1:0;pile.style.top=(1060-400)+'px'});
@SUB@""", LORD=LORD, V=json.dumps(VILR), R=wr, SUB=sub(1)), tr=True, dolly=.04)
ev(1, .2, 'slide'); [ev(1, .25 * i + .3, 'tick') for i in range(0, 12, 3)]; ev(1, wr, 'pop')
# 2 tuan tanah tersenyum, jendela desa tenang
ws = W(2, 'tersenyum', .5)
scene(2, R("""DARK(L,{moon:true,stars:true});
var win=MK.el('div','left:520px;top:420px;width:440px;height:520px;border:10px solid #3d2817;background:linear-gradient(#1c2a33,#2a3a40);overflow:hidden','<svg viewBox="0 0 440 520" width="440" height="520"><circle cx="330" cy="110" r="40" fill="#F4EBD9"/><g fill="#14110e"><path d="M0 420 L60 360 L120 420Z M120 430 L190 350 L260 430Z M260 420 L330 370 L400 420Z"/><rect x="0" y="420" width="440" height="100"/></g><g fill="#F0C77E"><rect x="80" y="440" width="18" height="18"/><rect x="210" y="450" width="18" height="18"/></g></svg>',L.root);win.className='mk-a';
var lord=MK.el('div','left:90px;top:520px;width:380px;height:720px',"@LORD@",L.root);lord.className='mk-a';
var q=MK.el('div','left:560px;top:1010px;width:420px;font-size:52px;line-height:1.1;color:#F4EBD9','“Desaku<br>sudah bersih.”',L.root);q.className='mk-a mk-fri';
L.on(function(t){lord.style.transform='translateY('+(Math.sin(t*1.4)*6)+'px)';var m=document.getElementById('lord_m');if(m)m.setAttribute('d',t>@S@?'M86 90 Q101 104 116 90':'M91 92 Q101 99 111 92');q.style.opacity=MK.pr(t,@S@+.8,.4)});
@SUB@""", LORD=LORD, S=ws, SUB=sub(2)), dolly=.06)
ev(2, ws, 'pop')
# 3 gudang: suara, mata menyala makin banyak
wg, wb = W(3, 'gudang', 2.1), W(3, 'banyak', 4.2)
scene(3, R("""DARK(L,{bg:'#0b0a08'});
var bn=MK.el('div','left:120px;top:420px;width:840px;height:900px','<svg viewBox="0 0 420 450" width="840" height="900"><path d="M20 160 L210 40 L400 160 V440 H20Z" fill="#2a1f17" stroke="#0F0E0C" stroke-width="6"/><g id="door"><rect x="120" y="230" width="180" height="210" fill="#140f0b" stroke="#5a3b24" stroke-width="6"/></g><path d="M120 230 L300 440 M300 230 L120 440" stroke="#5a3b24" stroke-width="5"/></svg>',L.root);bn.className='mk-a';
var ey=[];for(var i=0;i<40;i++){var e=MK.el('div','left:'+(370+(i*73)%340)+'px;top:'+(910+(i*47)%380)+'px;width:34px;height:12px','<svg viewBox="0 0 34 12" width="34" height="12"><circle cx="6" cy="6" r="5" fill="#F0C77E"/><circle cx="28" cy="6" r="5" fill="#F0C77E"/></svg>',L.root);e.className='mk-a';ey.push(e)}
var lt=GLOW(L,240,820,200,0);
L.on(function(t){var n=t<@G@?0:Math.floor(MK.pr(t,@G@,@B@-@G@+1.2)*40);for(var i=0;i<40;i++){ey[i].style.opacity=i<n?(Math.sin(t*3+i)>.9?0:1):0}bn.style.transform='translateX('+(t>@G@&&t<@G@+.5?Math.sin(t*60)*4:0)+'px)'});
@SUB@""", G=wg, B=wb, SUB=sub(3)), tr=True, dolly=.08)
ev(3, wg, 'scratch'); ev(3, wb, 'stamp')
# 4 gunting memotong ekor, tikus kabur, beranak, jadi koin
wpt, wbr, wkn = W(4, 'memotong', .3), W(4, 'beranak', 4.7), W(4, 'koin', 7.9)
scene(4, R("""DARK(L,{stars:true});
var rt=MK.el('div','left:380px;top:760px;width:320px;height:180px','<div style="transform:scale(2);transform-origin:0 0" id="rt">'+RAT()+'</div>',L.root);rt.className='mk-a';
var sc=MK.el('div','left:0;top:0;width:200px;height:200px','<svg viewBox="0 0 100 100" width="200" height="200"><g stroke="#0F0E0C" stroke-width="4"><path id="b1" d="M50 50 L95 30" stroke="#C9CCCF" stroke-width="10" stroke-linecap="round"/><path id="b2" d="M50 50 L95 70" stroke="#C9CCCF" stroke-width="10" stroke-linecap="round"/></g><circle cx="35" cy="40" r="12" fill="none" stroke="#B84A2E" stroke-width="7"/><circle cx="35" cy="62" r="12" fill="none" stroke="#B84A2E" stroke-width="7"/></svg>',L.root);sc.className='mk-a';
var tl=MK.el('div','left:330px;top:820px;width:80px;height:40px',TAIL(),L.root);tl.className='mk-a';
var kid=[];for(var i=0;i<5;i++){var e=MK.el('div','left:0;top:0;width:160px;height:90px','<div style="transform:scale(.7);transform-origin:0 0">'+RAT('#9a928a',false)+'</div>',L.root);e.className='mk-a';kid.push(e)}
var cs=[];for(var i=0;i<5;i++){var e=MK.el('div','left:0;top:0;width:80px;height:80px',COIN(80),L.root);e.className='mk-a';cs.push(e)}
L.on(function(t){var c=MK.pr(t,@P@,.4);var o=Math.sin(Math.min(1,c)*Math.PI*2)*12;var a=document.getElementById('b1'),b=document.getElementById('b2');if(a){a.setAttribute('transform','rotate('+(-o)+' 50 50)');b.setAttribute('transform','rotate('+o+' 50 50)')}
sc.style.transform='translate('+(240-80*c)+'px,'+(740)+'px)';sc.style.opacity=t<@P@+1?1:0;var cut=t>@P@+.4;tl.style.transform=cut?'translate('+(-(t-@P@)*80)+'px,'+(Math.min(300,(t-@P@-.4)*600))+'px) rotate('+((t-@P@)*200)+'deg)':'';
var r=document.getElementById('rt');if(r&&cut){var path=r.querySelector('path:last-child');if(path&&path.getAttribute('stroke')=='#D98C7A')path.setAttribute('opacity',0)}
var run=MK.E.io(MK.pr(t,@P@+1.2,1.4));rt.style.transform='translate('+(run*560)+'px,'+(-run*120)+'px)';rt.style.opacity=t<@B@-.2?1:0;
for(var i=0;i<5;i++){var k=MK.pr(t,@B@-.2+i*.12,.3);var x=180+i*150,y=980+(i%2)*90;kid[i].style.transform='translate('+x+'px,'+(y-Math.abs(Math.sin(t*8+i))*14)+'px) scale('+(.4+.6*MK.E.over(k))+')';kid[i].style.opacity=k>0&&t<@C@+.1?1:0;
var q=MK.pr(t,@C@+i*.08,.3);cs[i].style.transform='translate('+(x+20)+'px,'+(y-q*40)+'px) rotateY('+(q*360)+'deg)';cs[i].style.opacity=q>0?1:0}});
@SUB@""", P=wpt, B=wbr, C=wkn, SUB=sub(4)), dolly=.05)
ev(4, wpt + .2, 'scratch'); ev(4, wpt + 1.2, 'slide'); [ev(4, wbr - .2 + i * .12, 'tick') for i in range(5)]; ev(4, wkn, 'chime')
# 5 kandang tikus di belakang rumah, warga tersenyum, aturan dicentang
wpm, wat, wdb = W(5, 'memelihara', 1), W(5, 'aturan', 3.8), W(5, 'dibayar', 7.4)
scene(5, R("""DARK(L,{moon:true,stars:true});
var hs=MK.el('div','left:60px;top:560px;width:600px;height:560px','<svg viewBox="0 0 300 280" width="600" height="560"><path d="M20 120 L150 30 L280 120 V270 H20Z" fill="#3d2817" stroke="#0F0E0C" stroke-width="6"/><rect x="120" y="170" width="60" height="100" fill="#F0C77E" stroke="#0F0E0C" stroke-width="5"/></svg>',L.root);hs.className='mk-a';
var cg=[];for(var i=0;i<3;i++){var e=MK.el('div','left:'+(560+i*150)+'px;top:'+(960-i*20)+'px;width:150px;height:150px','<svg viewBox="0 0 150 150" width="150" height="150"><rect x="6" y="20" width="138" height="120" fill="rgba(15,14,12,.4)" stroke="#C9CCCF" stroke-width="5"/><g stroke="#C9CCCF" stroke-width="4"><path d="M30 20 V140 M55 20 V140 M80 20 V140 M105 20 V140 M130 20 V140"/></g></svg><div style="position:absolute;left:20px;top:70px;transform:scale(.6);transform-origin:0 0">'+RAT('#9a928a',false)+'</div>',L.root);e.className='mk-a';cg.push(e)}
var vl=MK.el('div','left:360px;top:850px;width:160px;height:300px',"@VIL@",L.root);vl.className='mk-a';
var rl=MK.el('div','left:120px;top:300px;width:840px;padding:24px 30px;background:#F4EBD9;border:5px solid #0F0E0C;border-radius:10px;transform:rotate(-2deg)','<div class="mk-mono" style="font-size:24px;color:#6B6560">ATURAN DESA</div><div class="mk-fr" style="font-size:54px">1 ekor tikus = 1 koin</div>',L.root);rl.className='mk-a';
var ck=MK.el('div','left:860px;top:310px;font-size:110px;color:#B84A2E','✓',L.root);ck.className='mk-a mk-ou';
L.on(function(t){for(var i=0;i<3;i++){var k=MK.pr(t,@M@+i*.25,.35);cg[i].style.opacity=k>0?1:0;cg[i].style.transform='scale('+(.5+.5*MK.E.over(k))+')'}var m=document.getElementById('v0_m');if(m)m.setAttribute('d','M86 90 Q101 104 116 90');
rl.style.opacity=MK.pr(t,@A@-.4,.3);var c=MK.pr(t,@A@,.25);ck.style.opacity=c;ck.style.transform='scale('+(.4+.6*MK.E.over(c))+')'});
@SUB@""", VIL=VIL[0], M=wpm, A=wat, D=wdb, SUB=sub(5)), tr=True, dolly=.04)
[ev(5, wpm + i * .25, 'pop') for i in range(3)]; ev(5, wat, 'tick'); ev(5, wdb, 'stamp')
# 6 POROS: gelap total, sorot, kartu tokoh Goodhart
wh = W(6, 'hukum', 2.7)
GOOD = ('<svg viewBox="0 0 260 360" width="300" height="415"><rect x="40" y="200" width="180" height="170" rx="60" fill="#2A2824"/>'
        '<path d="M110 200 L130 250 L150 200Z" fill="#FBF8F3"/><path d="M122 206 h16 l-4 40 h-8z" fill="#C8944A"/>'
        '<rect x="112" y="160" width="36" height="40" fill="#F1C9A3"/><circle cx="130" cy="118" r="58" fill="#F1C9A3"/>'
        '<path d="M74 110 Q72 60 130 58 Q188 60 186 110 Q176 84 150 80 Q120 92 96 86 Q80 92 74 110Z" fill="#E8E1D5"/>'
        '<g fill="none" stroke="#0F0E0C" stroke-width="4"><rect x="92" y="108" width="30" height="22" rx="6"/><rect x="138" y="108" width="30" height="22" rx="6"/><path d="M122 118 h16"/></g>'
        '<path d="M112 150 Q130 160 148 150" fill="none" stroke="#0F0E0C" stroke-width="4" stroke-linecap="round"/>'
        '<g transform="rotate(8 70 300)"><rect x="10" y="250" width="110" height="80" rx="6" fill="#FBF8F3" stroke="#0F0E0C" stroke-width="5"/><path d="M24 312 L50 290 L72 298 L104 266" fill="none" stroke="#B84A2E" stroke-width="5"/></g></svg>')
scene(6, R("""DARK(L,{bg:'#0b0a08'});
var sp=MK.el('div','left:190px;top:0;width:700px;height:1500px;background:linear-gradient(rgba(244,235,217,.16),rgba(244,235,217,0));clip-path:polygon(40% 0,60% 0,100% 100%,0 100%)',' ',L.root);sp.className='mk-a';
var fr=MK.el('div','left:96px;top:330px;width:888px;height:900px;border-radius:24px;background:#F4EBD9;border:6px solid #0F0E0C;box-shadow:0 40px 80px -30px rgba(0,0,0,.8)',' ',L.root);fr.className='mk-a';
var tg=MK.el('div','left:140px;top:370px;font-size:26px;letter-spacing:.1em;color:#B84A2E','KARTU TOKOH',L.root);tg.className='mk-a mk-mono';
var pt=MK.el('div','left:390px;top:410px;width:300px;height:415px','@G@',L.root);pt.className='mk-a';
var nm=MK.el('div','left:140px;top:850px;width:800px;text-align:center;font-size:60px;line-height:1;white-space:nowrap;color:#0F0E0C','CHARLES GOODHART',L.root);nm.className='mk-a mk-fr';
var s1=MK.el('div','left:140px;top:950px;width:800px;text-align:center;font-size:34px;color:#0F0E0C','Ekonom, mantan penasihat Bank of England',L.root);s1.className='mk-a mk-ou';
var s2=MK.el('div','left:140px;top:1000px;width:800px;text-align:center;font-size:34px;color:#B84A2E','Pencetus Hukum Goodhart (1975)',L.root);s2.className='mk-a mk-ou';
L.on(function(t){sp.style.opacity=MK.pr(t,.1,.6)*(t<@H@-.3?1:.5);var k=MK.E.over(MK.pr(t,@H@-.3,.45));[fr,tg,pt,nm,s1,s2].forEach(function(e,i){e.style.opacity=k>0?MK.pr(t,@H@-.3+i*.08,.3):0});fr.style.transform='rotate(-1.5deg) scale('+(.8+.2*k)+')';pt.style.transform='translateY('+((1-k)*60)+'px) rotate('+(Math.sin(t*1.5)*1.5)+'deg)'});
@SUB@""", G=GOOD, H=wh, SUB=sub(6)), tr=True, dolly=.05)
ev(6, .1, 'sweep'); ev(6, wh - .3, 'stamp')
# 7 definisi: panah menuju TUJUAN berbelok ke ANGKA
wtj, wak = W(7, 'tujuannya', 3.6), W(7, 'angkanya', 5.8)
scene(7, R("""DARK(L);
var tj=MK.el('div','left:110px;top:520px;width:380px;height:460px','<svg viewBox="0 0 190 230" width="380" height="460"><circle cx="95" cy="95" r="85" fill="#F4EBD9" stroke="#0F0E0C" stroke-width="6"/><circle cx="95" cy="95" r="58" fill="#B84A2E"/><circle cx="95" cy="95" r="32" fill="#F4EBD9"/><circle cx="95" cy="95" r="12" fill="#B84A2E"/><text x="95" y="220" text-anchor="middle" font-family="Fraunces,serif" font-weight="800" font-size="30" fill="#F4EBD9">TUJUAN</text></svg>',L.root);tj.className='mk-a';
var an=MK.el('div','left:620px;top:600px;width:360px;height:380px;border-radius:18px;background:#1f1b17;border:5px solid #F4EBD9;display:flex;flex-direction:column;align-items:center;justify-content:center','<div id="num" class="mk-fr" style="font-size:120px;color:#C8944A">0</div><div class="mk-mono" style="font-size:28px;color:#F4EBD9">ANGKA</div>',L.root);an.className='mk-a';
var ar=MK.el('div','left:0;top:0;width:220px;height:60px','<svg viewBox="0 0 220 60" width="220" height="60"><path d="M0 30 H190" stroke="#F4EBD9" stroke-width="8"/><path d="M190 12 L218 30 L190 48Z" fill="#F4EBD9"/><path d="M0 30 l-20 -18 M0 30 l-20 18" stroke="#C8944A" stroke-width="7"/></svg>',L.root);ar.className='mk-a';
L.on(function(t){var u=MK.E.io(MK.pr(t,.3,1.4));var v=MK.E.io(MK.pr(t,@T@,1.4));
var x=200+u*0-v*0,y=1240;var px=540-u*0,py=1250-u*500;var tx=px+(820-px)*v,ty=py+(780-py)*v-(Math.sin(v*Math.PI)*180);var ang=v>0?(-90+v*120):-90;
ar.style.transform='translate('+(tx-110)+'px,'+(ty-30)+'px) rotate('+ang+'deg)';var n=document.getElementById('num');if(n)n.textContent=Math.round(MK.pr(t,@T@+.8,2)*999);an.style.boxShadow=t>@A@?'0 0 60px 10px rgba(200,148,74,.35)':'none';tj.style.opacity=t>@T@+.6?.35:1});
@SUB@""", T=wtj, A=wak, SUB=sub(7)), dolly=.04)
ev(7, .3, 'sweep'); ev(7, wtj, 'sweep'); ev(7, wak, 'pop')
# 8 dunia bisnis (garis): siluet tikus jadi gedung kantor
scene(8, R("""DARK(L,{bg:'#101317'});
var grid=MK.el('div','left:0;top:0;width:1080px;height:1920px;background-image:linear-gradient(rgba(244,235,217,.06) 2px,transparent 2px),linear-gradient(90deg,rgba(244,235,217,.06) 2px,transparent 2px);background-size:60px 60px',' ',L.root);grid.className='mk-a';
var rt=MK.el('div','left:300px;top:640px;width:480px;height:270px','<div style="transform:scale(3);transform-origin:0 0">'+RAT('#20242a')+'</div>',L.root);rt.className='mk-a';
var bd=MK.el('div','left:240px;top:420px;width:600px;height:760px',LINE(600,760,'<path d="M60 740 V180 H300 V740 M300 740 V60 H540 V740 M20 740 H580"/><path d="M100 240 h60 M180 240 h60 M100 320 h60 M180 320 h60 M100 400 h60 M180 400 h60 M340 140 h60 M420 140 h60 M340 220 h60 M420 220 h60 M340 300 h60 M420 300 h60 M340 380 h60 M420 380 h60"/>'),L.root);bd.className='mk-a';
var p=bd.querySelector('g');var len=0;
L.on(function(t){var m=MK.pr(t,.6,.8);rt.style.opacity=1-m;rt.style.transform='scale('+(1-m*.3)+')';bd.style.opacity=m;});
@SUB@""", SUB=sub(8)), tr=True, dolly=.06)
ev(8, .6, 'sweep')
# 9 admin + stopwatch, chat cepat, keranjang kosong
wbl, wpb = W(9, 'dibalas', 2.8), W(9, 'pembeli', 4.3)
scene(9, R("""DARK(L,{bg:'#101317'});
var fg=MK.el('div','left:120px;top:780px;width:200px;height:380px',LINE(100,190,LFIG())+'',L.root);fg.className='mk-a';fg.firstChild.setAttribute('width',200);fg.firstChild.setAttribute('height',380);
var dk=MK.el('div','left:80px;top:1060px;width:420px;height:20px;border-top:4px solid #F4EBD9',' ',L.root);dk.className='mk-a';
var sw=MK.el('div','left:120px;top:420px;width:260px;height:300px',LINE(130,150,'<circle cx="65" cy="85" r="55"/><path d="M65 30 V18 M50 14 h30"/><path id="swh" d="M65 85 V45"/>'),L.root);sw.className='mk-a';sw.firstChild.setAttribute('width',260);sw.firstChild.setAttribute('height',300);
var bs=[];for(var i=0;i<5;i++){var e=MK.el('div','left:520px;top:'+(380+i*120)+'px;width:440px;padding:16px 22px;border:4px solid #F4EBD9;border-radius:22px 22px 6px 22px;color:#F4EBD9;font-size:34px','dibalas ✓✓ <span style="color:#C8944A">'+(i+1)*7+' dtk</span>',L.root);e.className='mk-a mk-ou';bs.push(e)}
var ct=MK.el('div','left:560px;top:1020px;width:300px;height:220px',LINE(150,110,'<path d="M10 20 h20 l16 60 h80 l14 -46 H40"/><circle cx="56" cy="98" r="8"/><circle cx="114" cy="98" r="8"/>'),L.root);ct.className='mk-a';ct.firstChild.setAttribute('width',300);ct.firstChild.setAttribute('height',220);
var x=MK.el('div','left:860px;top:1020px;font-size:150px;color:#B84A2E;line-height:1','×',L.root);x.className='mk-a mk-fr';
L.on(function(t){var h=document.getElementById('swh');if(h)h.setAttribute('transform','rotate('+(t*360)+' 65 85)');for(var i=0;i<5;i++){var k=MK.pr(t,@B@-.6+i*.15,.25);bs[i].style.opacity=k>0?1:0;bs[i].style.transform='translateX('+((1-MK.E.over(k))*200)+'px)'}ct.style.opacity=MK.pr(t,@P@-.4,.3);var c=MK.pr(t,@P@+.5,.25);x.style.opacity=c;x.style.transform='scale('+(.4+.6*MK.E.over(c))+')'});
@SUB@""", B=wbl, P=wpb, SUB=sub(9)), dolly=.04)
[ev(9, wbl - .6 + i * .15, 'tick') for i in range(5)]; ev(9, wpb + .5, 'scratch')
# 10 konten: followers naik, pembeli orang yang sama
wfl, wsm = W(10, 'followers', 1.3), W(10, 'sama', 4.6)
scene(10, R("""DARK(L,{bg:'#101317'});
var ph=MK.el('div','left:110px;top:400px;width:380px;height:700px;border:5px solid #F4EBD9;border-radius:46px',' ',L.root);ph.className='mk-a';
var lb=MK.el('div','left:150px;top:470px;width:300px;font-size:28px;color:#F4EBD9','FOLLOWERS',L.root);lb.className='mk-a mk-mono';
MK.CountUp(L,{x:150,y:520,from:1200,to:12400,at:@F@,dur:1.8,size:84,color:'#C8944A'});
var ar=MK.el('div','left:150px;top:680px;width:300px;height:300px',LINE(150,150,'<path id="far" d="M10 140 L50 100 L80 112 L140 30"/><path d="M118 30 h22 v22"/>'),L.root);ar.className='mk-a';ar.firstChild.setAttribute('width',300);ar.firstChild.setAttribute('height',300);
var by=MK.el('div','left:560px;top:420px;width:420px;height:140px;font-size:28px;color:#F4EBD9','YANG BELI',L.root);by.className='mk-a mk-mono';
var ps=[];for(var i=0;i<6;i++){var e=MK.el('div','left:'+(560+(i%3)*140)+'px;top:'+(480+Math.floor(i/3)*280)+'px;width:100px;height:200px',LINE(100,200,LFIG()),L.root);e.className='mk-a';ps.push(e)}
var sm=MK.el('div','left:560px;top:1060px;width:420px;font-size:46px;color:#D98C7A','orangnya itu-itu lagi',L.root);sm.className='mk-a mk-fri';
L.on(function(t){for(var i=0;i<6;i++){var k=MK.pr(t,@S@-1.6+i*.18,.25);ps[i].style.opacity=k>0?(i<3?1:.45):0}sm.style.opacity=MK.pr(t,@S@,.3)});
@SUB@""", F=wfl, S=wsm, SUB=sub(10)), tr=True, dolly=.04)
ev(10, wfl, 'pop'); ev(10, wsm, 'scratch')
# 11 sales: batang omzet tembus target, label diskon
wtb, wds = W(11, 'tembus', 2.6), W(11, 'diskon', 4.6)
scene(11, R("""DARK(L,{bg:'#101317'});
var gl=MK.el('div','left:96px;top:600px;width:888px;height:0;border-top:5px dashed #C8944A',' ',L.root);gl.className='mk-a';
var gt=MK.el('div','left:96px;top:540px;font-size:28px;color:#C8944A','TARGET OMZET',L.root);gt.className='mk-a mk-mono';
var br=MK.el('div','left:240px;top:420px;width:220px;height:760px;border:5px solid #F4EBD9;border-bottom:none;transform-origin:bottom;background:rgba(244,235,217,.08)',' ',L.root);br.className='mk-a';
var tg=MK.el('div','left:560px;top:760px;width:440px;height:300px','<svg viewBox="0 0 220 150" width="440" height="300"><path d="M40 10 H210 V140 H40 L6 75Z" fill="#B84A2E" stroke="#F4EBD9" stroke-width="6" stroke-linejoin="round"/><circle cx="38" cy="75" r="10" fill="#101317"/><text x="128" y="70" text-anchor="middle" font-family="Fraunces,serif" font-weight="800" font-size="44" fill="#F4EBD9">DISKON</text><text x="128" y="118" text-anchor="middle" font-family="Fraunces,serif" font-weight="800" font-size="48" fill="#F4EBD9">50%</text></svg>',L.root);tg.className='mk-a';
L.on(function(t){var g=MK.E.out(MK.pr(t,.3,@T@));br.style.transform='scaleY('+(.2+.8*g)+')';br.style.borderColor=t>@T@?'#C8944A':'#F4EBD9';var k=MK.pr(t,@D@-.3,.3);tg.style.opacity=k;tg.style.transform='rotate('+(-8+Math.sin(t*4)*3)+'deg) scale('+(.4+.6*MK.E.over(k))+')'});
@SUB@""", T=wtb, D=wds, SUB=sub(11)), tr=True, dolly=.04)
ev(11, wtb, 'chime'); ev(11, wds - .3, 'stamp')
# 12 ekor jatuh ke meja owner, kamera mundur: gudang di belakang
wgu = W(12, 'gudang', 3.2)
scene(12, R("""DARK(L,{bg:'#101317'});
var dk=MK.el('div','left:80px;top:1080px;width:920px;height:30px;border-top:6px solid #F4EBD9',' ',L.root);dk.className='mk-a';
var lbl=['chat','followers','omzet'],tl=[];for(var i=0;i<9;i++){var e=MK.el('div','left:'+(200+(i*97)%600)+'px;top:0;width:150px;height:80px',TAIL()+'<div class="mk-mono" style="font-size:22px;color:#D98C7A;margin-top:-6px">'+lbl[i%3]+'</div>',L.root);e.className='mk-a';tl.push(e)}
var bn=MK.el('div','left:300px;top:340px;width:480px;height:460px','<svg viewBox="0 0 240 230" width="480" height="460"><g fill="none" stroke="#F4EBD9" stroke-width="3" opacity=".7"><path d="M10 90 L120 20 L230 90 V220 H10Z"/><rect x="70" y="120" width="100" height="100"/></g></svg>',L.root);bn.className='mk-a';
var ey=[];for(var i=0;i<18;i++){var e=MK.el('div','left:'+(380+(i*53)%170)+'px;top:'+(600+(i*31)%170)+'px;width:22px;height:8px','<svg viewBox="0 0 22 8" width="22" height="8"><circle cx="4" cy="4" r="3.5" fill="#F0C77E"/><circle cx="18" cy="4" r="3.5" fill="#F0C77E"/></svg>',L.root);e.className='mk-a';ey.push(e)}
L.on(function(t){for(var i=0;i<9;i++){var s=.1+i*.22,f=Math.min(1,Math.max(0,(t-s)/.5));tl[i].style.transform='translateY('+(300+f*f*740-Math.floor(i/3)*24)+'px) rotate('+((i*47)%60-30)+'deg)';tl[i].style.opacity=t>s?1:0}
var b=MK.pr(t,@G@-.6,.6);bn.style.opacity=b;for(var i=0;i<18;i++)ey[i].style.opacity=t>@G@-.2+i*.04?(Math.sin(t*3+i)>.92?0:1):0});
@SUB@""", G=wgu, SUB=sub(12)), dolly=.03)
[ev(12, .1 + i * .44, 'tick') for i in range(5)]; ev(12, wgu - .6, 'sweep')
# 13 penutup: kursi tuan tanah -> kursi owner, koin berputar lalu berhenti, pertanyaan
wtk = W(13, 'tikusnya', 4.1)
scene(13, R("""DARK(L);GLOW(L,540,900,380,0);
var tb=MK.el('div','left:-20px;top:1060px;width:1120px;height:900px;background:linear-gradient(#5a3b24,#3d2817);border-top:8px solid #0F0E0C',' ',L.root);tb.className='mk-a';
var ch=MK.el('div','left:390px;top:600px;width:300px;height:460px','<svg viewBox="0 0 150 230" width="300" height="460"><path id="chb" d="M20 10 Q75 -10 130 10 V140 H20Z" fill="#2f4a3a" stroke="#0F0E0C" stroke-width="6"/><rect x="10" y="140" width="130" height="30" rx="6" fill="#3d2817" stroke="#0F0E0C" stroke-width="6"/><path d="M75 170 V220 M40 222 h70" stroke="#0F0E0C" stroke-width="8"/></svg>',L.root);ch.className='mk-a';
var cn=MK.el('div','left:500px;top:990px;width:80px;height:80px',COIN(80),L.root);cn.className='mk-a';
var q=MK.el('div','left:96px;top:300px;width:888px;text-align:center;font-size:96px;line-height:1.05;color:#F4EBD9','Tikusnya,<br>atau <span style="color:#D98C7A">ekornya?</span>',L.root);q.className='mk-a mk-fr';
L.on(function(t){var m=MK.pr(t,1.2,1);var b=document.getElementById('chb');if(b)b.setAttribute('fill',m>.5?'#0F0E0C':'#2f4a3a');ch.style.transform='scale('+(1+m*.04)+')';
var s=Math.max(0,1-MK.pr(t,.3,4));cn.style.transform='rotateY('+(t*720*s+ (1-s)*0)+'deg) translateY('+(-Math.abs(Math.sin(t*10))*10*s)+'px)';var k=MK.pr(t,@Q@,.4);q.style.opacity=k;q.style.transform='translateY('+((1-MK.E.out(k))*30)+'px)'});""", Q=wtk), tr=True, dolly=.05)
ev(13, .3, 'chime'); ev(13, wtk, 'pop')
html = ('<!DOCTYPE html>\n<html><head><meta charset="utf-8"><title>Fabel Bisnis 01</title><link rel="stylesheet" href="motionkit/fonts-mk.css"></head><body>\n'
        '<script src="motionkit/kit.js"></script>\n<script>\nvar C=MK.C;\n' + HELP + FAB + '\nMK.run([\n' + ',\n'.join(S) + '\n]);\n</script>\n</body></html>\n')
open(A + 'mk-fabel01.html', 'w', encoding='utf-8').write(html)
json.dump({'duration': tl['duration'], 'events': EV, 'cuts': T0}, open(os.path.join(OUT, 'events.json'), 'w'))
print('ok', len(S), 'adegan', round(sum(DUR), 1), 'dtk'); print([(SC[i][0], DUR[i]) for i in range(len(SC))])
