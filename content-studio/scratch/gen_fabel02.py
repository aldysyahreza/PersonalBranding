"""Fabel Bisnis #01 ekor tikus: animasi penuh Motion Kit dari timing.json vo_prep.
Pakai: python3 scratch/gen_metrik.py out/reel17/timing.json -> animatic/mk-fabel02.html + out/reel17/events.json"""
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
SC = [('ada',0,0),('tipe',0,1),('tipe',0,0),('di',0,0),('pelayannya',0,0),('pemiliknya',0,0),
      ('di',1,0),('pemiliknya',1,0),('mohon',1,0),
      ('tiga',2,0),('raka',2,0),('pelanggan',2,0),('cafe',2,0),('katanya',2,0),
      ('di',3,0),('albert',3,0),('bilang',3,0),
      ('di',4,0),('di',4,1),('satu',4,0),('satu',4,0),('jadi',4,0)]
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
KEY = {'gangguan','masukan','ketus','badmood','maaf','perbaiki','sepi','pindah','ramah','exit','voice','loyalty','hirschman','ngomong','kesempatan','jutek','loyal','solusi','selesai','rekomendasi','pergi','mana'}
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
def ev(i, local, kind):
    if i in globals().get('DROP', ()): return
    EV.append([round(T0[i] + local, 3), kind])
def chunks_all(i):
    out = list(chunks(i)); j = i + 1
    while j in globals().get('DROP', ()):
        out += [[round(t + T0[j] - T0[i], 2), w] for t, w in chunks(j)]; j += 1
    return out
sub = lambda i, c='#FBF8F3', y=1420: 'MK.Subtitle(L,%s,{y:%d,color:"%s",dark:true});' % (json.dumps(chunks_all(i), ensure_ascii=False), y, c)
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
DROP = {10}
for d_ in sorted(DROP): DUR[d_ - 1] = round(DUR[d_ - 1] + DUR[d_], 3)
def scene(i, body, tr=False, dolly=0, paper=None):
    if i in DROP: return
    S.append("{dur:%s,%s%s%s build:function(L){\n%s\n}}" % (DUR[i], " tr:'fade'," if i else '', " dolly:%s," % (dolly * .7) if dolly else '', " paper:'%s'," % paper if paper else '', body))

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
GOOD = ('<svg viewBox="0 0 260 360" width="300" height="415"><rect x="40" y="200" width="180" height="170" rx="60" fill="#2A2824"/>'
        '<path d="M110 200 L130 250 L150 200Z" fill="#FBF8F3"/><path d="M122 206 h16 l-4 40 h-8z" fill="#C8944A"/>'
        '<rect x="112" y="160" width="36" height="40" fill="#F1C9A3"/><circle cx="130" cy="118" r="58" fill="#F1C9A3"/>'
        '<path d="M74 110 Q72 60 130 58 Q188 60 186 110 Q176 84 150 80 Q120 92 96 86 Q80 92 74 110Z" fill="#E8E1D5"/>'
        '<g fill="none" stroke="#0F0E0C" stroke-width="4"><rect x="92" y="108" width="30" height="22" rx="6"/><rect x="138" y="108" width="30" height="22" rx="6"/><path d="M122 118 h16"/></g>'
        '<path d="M112 150 Q130 160 148 150" fill="none" stroke="#0F0E0C" stroke-width="4" stroke-linecap="round"/>'
        '<g transform="rotate(8 70 300)"><rect x="10" y="250" width="110" height="80" rx="6" fill="#FBF8F3" stroke="#0F0E0C" stroke-width="5"/><path d="M24 312 L50 290 L72 298 L104 266" fill="none" stroke="#B84A2E" stroke-width="5"/></g></svg>')

def R(js, **kw):
    for k_, v_ in kw.items(): js = js.replace('@' + k_ + '@', str(v_))
    return js
PAL = {'lord': ('#2f4a3a', '#22362a', '#e8e1d5'), 'v1': ('#B84A2E', '#8f3a24', '#2a1d14'), 'v2': ('#C8944A', '#a57a35', '#2a1d14'), 'v3': ('#6B6560', '#4a4540', '#2a1d14'),
       'v4': ('#8a5a3a', '#6a442c', '#2a1d14'), 'v5': ('#3e5a6b', '#2d4350', '#2a1d14'), 'own': ('#B84A2E', '#8f3a24', '#2a1d14')}
FIGS = {}
def F(u, kind, flip=False):
    c = PAL[kind]; FIGS[u] = person(u, c[0], c[1], c[2], flip).replace('\n', ''); return u
FAB2 = r"""
function $(i){return document.getElementById(i)}
function RT(id,a,cx,cy){var e=$(id);if(e)e.setAttribute('transform','rotate('+a.toFixed(2)+' '+cx+' '+cy+')')}
function BOB(u,t,amp){var e=$(u+'_b');if(e)e.setAttribute('transform','translate(0,'+(Math.sin(t*3.2)*amp).toFixed(2)+')')}
function LEGS(u,ph,amp){RT(u+'_ll',Math.sin(ph)*amp,86,216);RT(u+'_lr',-Math.sin(ph)*amp,114,216)}
function ARM(u,side,a){RT(u+'_'+side,a,side==='la'?73:127,134)}
function HEAD(u,a){RT(u+'_h',a,100,104)}
function SMILE(u,k){var m=$(u+'_m');if(m)m.setAttribute('d',k>0?'M86 90 Q101 '+(96+k*10)+' 116 90':'M91 94 Q101 '+(94+k*6)+' 111 94')}
function WALK(u,t,on){LEGS(u,t*14,on?24:0);ARM(u,'la',on?Math.sin(t*14+3)*22:4);ARM(u,'ra',on?-Math.sin(t*14+3)*22:-4);BOB(u,t*4,on?3:1.5)}
function FIG(L,u,x,y,w,flip){var e=MK.el('div','left:'+x+'px;top:'+y+'px;width:'+w+'px;height:'+(w*1.9)+'px',FG[u],L.root);e.className='mk-a';if(flip)e.style.transform='scaleX(-1)';return e}
function VILLAGE(L,o){o=o||{};DARK(L,{moon:true,stars:true});
 var ly=[];function lay(html,k,top){var e=MK.el('div','left:-60px;top:'+top+'px;width:1200px;height:900px',html,L.root);e.className='mk-a';ly.push([e,k]);return e}
 lay('<svg viewBox="0 0 1200 900" width="1200" height="900"><path d="M0 300 Q200 140 420 260 T860 220 T1200 260 V900 H0Z" fill="#1d1915"/></svg>',8,(o.y||560)-80);
 lay('<svg viewBox="0 0 1200 900" width="1200" height="900"><path d="M0 360 Q300 250 600 330 T1200 300 V900 H0Z" fill="#171310"/></svg>',16,(o.y||560));
 var hs='';for(var i=0;i<6;i++){var x=40+i*200,h=120+(i%3)*30;hs+='<path d="M'+x+' '+(400-h)+' l70 -60 l70 60 v'+h+' h-140z" fill="#2a1f17" stroke="#0F0E0C" stroke-width="4"/><rect id="win'+i+(o.id||'')+'" x="'+(x+52)+'" y="'+(420-h)+'" width="36" height="34" fill="#F0C77E"/>';}
 var tr='';for(var i=0;i<7;i++){var x=100+i*170;tr+='<path d="M'+x+' 400 l-40 0 l40 -150 l40 150z" fill="#120f0c"/>'}
 lay('<svg viewBox="0 0 1200 900" width="1200" height="900">'+tr+hs+'<rect x="0" y="400" width="1200" height="500" fill="#14100c"/><g stroke="#3d2817" stroke-width="8">'+[0,1,2,3,4,5,6,7,8,9,10,11].map(function(i){return '<path d="M'+(i*100+20)+' 400 v60"/>'}).join('')+'<path d="M0 420 H1200 M0 445 H1200"/></g></svg>',30,(o.y||560)+60);
 L.on(function(t){ly.forEach(function(p){p[0].style.transform='translateX('+(Math.sin(t*.25)*p[1]-t*p[1]*.4)+'px)'});if(o.off!=null)for(var i=0;i<6;i++){var w=$('win'+i+(o.id||''));if(w)w.setAttribute('opacity',t>o.off+i*.35?0:1)}});
 return ly}
function RATS(L,n,o){var a=[];for(var i=0;i<n;i++){var e=MK.el('div','left:0;top:0;width:160px;height:90px','<div style="transform:scale('+(o.s||.7)+');transform-origin:0 0">'+RAT(o.c||'#8a827a',o.tail)+'</div>',L.root);e.className='mk-a';a.push(e)}
 L.on(function(t){for(var i=0;i<n;i++){var k=MK.pr(t,(o.at||0)+i*(o.gap||.12),.2);var p=(t-(o.at||0)-i*(o.gap||.12))*(o.v||260);var x=(o.x||0)+((i*97)%(o.sx||400))+p*(o.dir||1),y=(o.y||0)+((i*53)%(o.sy||200))-Math.abs(Math.sin(t*14+i))*10;a[i].style.transform='translate('+x+'px,'+y+'px) scaleX('+((o.dir||1)>0?1:-1)+')';a[i].style.opacity=k>0?1:0}});return a}
"""
PAL.update({'raka': ('#3e5a6b', '#2d4350', '#2a1d14'), 'dita': ('#B84A2E', '#8f3a24', '#2a1d14'), 'wt': ('#2A2824', '#1a1816', '#2a1d14'),
            'ow': ('#8a5a3a', '#6a442c', '#5a5550'), 'f1': ('#C8944A', '#a57a35', '#2a1d14'), 'f2': ('#6B6560', '#4a4540', '#2a1d14'), 'f3': ('#2f4a3a', '#22362a', '#2a1d14')})
HIRS = ('<svg viewBox="0 0 260 360" width="300" height="415"><rect x="40" y="200" width="180" height="170" rx="60" fill="#3d3a36"/>'
        '<path d="M110 200 L130 250 L150 200Z" fill="#FBF8F3"/><path d="M124 206 h12 l-3 40 h-6z" fill="#B84A2E"/>'
        '<rect x="112" y="160" width="36" height="40" fill="#F1C9A3"/><circle cx="130" cy="118" r="58" fill="#F1C9A3"/>'
        '<path d="M72 112 Q70 62 130 56 Q190 62 188 112 Q180 90 160 86 L100 86 Q80 90 72 112Z" fill="#9a9590"/>'
        '<g fill="none" stroke="#0F0E0C" stroke-width="4"><circle cx="108" cy="120" r="16"/><circle cx="152" cy="120" r="16"/><path d="M124 120 h12"/></g>'
        '<path d="M112 152 Q130 162 148 152" fill="none" stroke="#0F0E0C" stroke-width="4" stroke-linecap="round"/>'
        '<g transform="rotate(-8 200 300)"><rect x="150" y="250" width="100" height="120" rx="6" fill="#C8944A" stroke="#0F0E0C" stroke-width="5"/>'
        '<text x="200" y="300" text-anchor="middle" font-family="Fraunces,serif" font-weight="800" font-size="17" fill="#0F0E0C">EXIT</text>'
        '<text x="200" y="322" text-anchor="middle" font-family="Fraunces,serif" font-weight="800" font-size="17" fill="#0F0E0C">VOICE</text>'
        '<text x="200" y="344" text-anchor="middle" font-family="Fraunces,serif" font-weight="800" font-size="13" fill="#0F0E0C">LOYALTY</text></g></svg>')
CAFE_JS = r"""
function CAFE(L,o){o=o||{};var dim=o.dim||0;
 var w=MK.el('div','left:0;top:0;width:1080px;height:1920px;background:linear-gradient(#3a2a1e,#2a1f17 60%,#1b140f)',' ',L.root);w.className='mk-a';
 var win=MK.el('div','left:620px;top:360px;width:380px;height:420px;border:12px solid #5a3b24;background:linear-gradient(#2a3a40,#1c2a33);overflow:hidden','<svg viewBox="0 0 380 420" width="380" height="420"><g fill="#14110e"><rect x="20" y="240" width="80" height="180"/><rect x="120" y="200" width="90" height="220"/><rect x="230" y="260" width="120" height="160"/></g><g fill="#F0C77E" opacity=".8"><rect x="140" y="230" width="14" height="14"/><rect x="250" y="290" width="14" height="14"/></g></svg>',L.root);win.className='mk-a';
 var ct=MK.el('div','left:60px;top:880px;width:520px;height:260px;background:#5a3b24;border:6px solid #0F0E0C;border-radius:8px','<div style="position:absolute;left:30px;top:-110px;width:90px;height:110px;background:#2A2824;border:5px solid #0F0E0C;border-radius:8px"></div><div style="position:absolute;left:150px;top:-60px;width:60px;height:60px;border-radius:50%;background:#C8944A;border:5px solid #0F0E0C"></div>',L.root);ct.className='mk-a';
 var lp=[];for(var i=0;i<3;i++){var e=MK.el('div','left:'+(160+i*300)+'px;top:0;width:80px;height:330px','<svg viewBox="0 0 80 330" width="80" height="330"><path d="M40 0 V250" stroke="#0F0E0C" stroke-width="4"/><path d="M10 290 Q40 230 70 290Z" fill="#C8944A" stroke="#0F0E0C" stroke-width="4"/></svg>',L.root);e.className='mk-a';lp.push(e);GLOW(L,200+i*300,330,150,0)}
 var lb=MK.el('div','left:96px;top:250px;padding:12px 26px;border-radius:999px;background:'+(o.type==2?'#C8944A':'#6B6560')+';color:#0F0E0C;font-size:30px;letter-spacing:.06em','TIPE '+o.type+' · KOMPLAIN = '+(o.type==2?'MASUKAN':'GANGGUAN'),L.root);lb.className='mk-a mk-mono';
 var sh=MK.el('div','left:0;top:0;width:1080px;height:1920px;background:#000;pointer-events:none',' ',L.root);sh.className='mk-a';
 L.on(function(t){lp.forEach(function(e,i){e.style.transform='rotate('+(Math.sin(t*1.2+i)*2)+'deg)'});var d=typeof dim=='function'?dim(t):dim;sh.style.opacity=d});
 return {lb:lb}}
function TABLE(L,x,y){var e=MK.el('div','left:'+x+'px;top:'+y+'px;width:260px;height:200px','<svg viewBox="0 0 260 200" width="260" height="200"><rect x="10" y="20" width="240" height="22" rx="6" fill="#8a5a3a" stroke="#0F0E0C" stroke-width="5"/><path d="M60 42 V200 M200 42 V200" stroke="#0F0E0C" stroke-width="8"/></svg>',L.root);e.className='mk-a';return e}
function CUP(L,x,y,c){var e=MK.el('div','left:'+x+'px;top:'+y+'px;width:50px;height:60px','<svg viewBox="0 0 50 60" width="50" height="60"><path d="M6 10 h38 l-4 46 h-30z" fill="'+(c||'#F4EBD9')+'" stroke="#0F0E0C" stroke-width="4"/><path d="M10 22 h30" stroke="#8a5a3a" stroke-width="10"/></svg>',L.root);e.className='mk-a';return e}
function BUB(L,x,y,w,html,at,c,dur){var e=MK.el('div','left:'+x+'px;top:'+y+'px;width:'+w+'px;padding:18px 24px;border-radius:24px;background:'+(c||'#F4EBD9')+';border:4px solid #0F0E0C;font-size:38px;line-height:1.15',html,L.root);e.className='mk-a mk-ou';L.on(function(t){var k=MK.pr(t,at,.3);var o=dur?Math.min(k,1-MK.pr(t,at+dur,.3)):k;e.style.opacity=o;e.style.transform='scale('+(.6+.4*MK.E.over(k))+')'});return e}
function FACADE(L,x,o){var c=MK.el('div','left:'+x+'px;top:560px;width:520px;height:760px',' ',L.root);c.className='mk-a';
 c.innerHTML='<svg viewBox="0 0 520 760" width="520" height="760"><rect x="20" y="140" width="480" height="620" fill="#3d2817" stroke="#0F0E0C" stroke-width="6"/><path d="M0 140 L520 140 L490 230 L30 230Z" fill="'+(o.type==2?'#C8944A':'#6B6560')+'" stroke="#0F0E0C" stroke-width="6"/>'+[0,1,2,3,4,5].map(function(i){return '<path d="M'+(30+i*80)+' 230 l40 -90 l40 90" fill="none" stroke="#0F0E0C" stroke-width="3" opacity=".4"/>'}).join('')+'<rect x="60" y="280" width="240" height="220" fill="#F0C77E" stroke="#0F0E0C" stroke-width="6" id="fw'+o.id+'"/><rect x="340" y="320" width="120" height="440" fill="#2a1f17" stroke="#0F0E0C" stroke-width="6"/><text x="260" y="110" text-anchor="middle" font-family="Fraunces,serif" font-weight="800" font-size="56" fill="#F4EBD9">CAFE</text></svg>';
 var pp=[];for(var i=0;i<4;i++){var e=MK.el('div','left:'+(x+80+i*55)+'px;top:880px;width:40px;height:90px','<svg viewBox="0 0 40 90" width="40" height="90"><circle cx="20" cy="18" r="14" fill="#2a1f17"/><rect x="6" y="34" width="28" height="56" rx="12" fill="#2a1f17"/></svg>',L.root);e.className='mk-a';pp.push(e)}
 L.on(function(t){var n=typeof o.n=='function'?o.n(t):o.n;for(var i=0;i<4;i++){pp[i].style.opacity=i<n?1:0;pp[i].style.transform='translateY('+(Math.sin(t*3+i)*3)+'px)'}var w=document.getElementById('fw'+o.id);if(w)w.setAttribute('fill',(typeof o.lit=='function'?o.lit(t):o.lit)?'#F0C77E':'#2b241d')});return c}
"""
BP = "DARK(L,{bg:'#101317'});var grid=MK.el('div','left:0;top:0;width:1080px;height:1920px;background-image:linear-gradient(rgba(244,235,217,.06) 2px,transparent 2px),linear-gradient(90deg,rgba(244,235,217,.06) 2px,transparent 2px);background-size:60px 60px',' ',L.root);grid.className='mk-a';"
def LF(x, y, sc=1, extra=''):
    return "MK.el('div','left:%dpx;top:%dpx;width:%dpx;height:%dpx',LINE(100,200,LFIG()%s),L.root)" % (x, y, 100 * sc, 200 * sc, extra)

# ===== B0 =====
scene(0, R("""DARK(L,{stars:true,moon:true});
var hl=MK.el('div','left:96px;top:250px;width:900px;font-size:84px;line-height:1.04;color:#F4EBD9','Komplain itu gangguan,<br>atau <span style="color:#C8944A">masukan?</span>',L.root);hl.className='mk-a mk-fr';L.headline=true;
FACADE(L,10,{id:'a0',type:1,n:4,lit:true});FACADE(L,550,{id:'b0',type:2,n:4,lit:true});
var rd=MK.el('div','left:0;top:1320px;width:1080px;height:600px;background:#1b1612;border-top:6px solid #0F0E0C',' ',L.root);rd.className='mk-a';"""))
ev(0, .1, 'slide')
def LBL(type_, at=.05):
    return R("""var tl=MK.el('div','left:96px;top:300px;width:888px;font-size:66px;line-height:1.05;color:#F4EBD9','<span class="mk-mono" style="font-size:28px;color:@C@">TIPE @T@</span><br>Komplain = <span style="color:@C@">@W@</span>',L.root);tl.className='mk-a mk-fr';L.on(function(t){var k=MK.pr(t,@A@,.4);tl.style.opacity=k;tl.style.transform='translateY('+((1-MK.E.out(k))*24)+'px)'});""",
             T=type_, C='#C8944A' if type_ == 2 else '#9a9590', W='masukan.' if type_ == 2 else 'gangguan.', A=at)
EAR = lambda covered: ('<svg viewBox="0 0 120 140" width="240" height="280"><path d="M60 10 Q110 10 110 64 Q110 96 82 110 Q70 116 70 130 Q70 140 56 140 Q40 140 40 124" fill="none" stroke="#F4EBD9" stroke-width="10" stroke-linecap="round"/>'
                       '<path d="M50 60 Q50 34 72 34 Q92 34 92 60" fill="none" stroke="#F4EBD9" stroke-width="8" stroke-linecap="round"/>'
                       + ('<rect x="20" y="20" width="100" height="110" rx="40" fill="#6B6560" stroke="#0F0E0C" stroke-width="6" transform="rotate(-18 70 75)"/>' if covered else
                          '<path d="M-10 50 q-14 20 0 40 M-30 36 q-24 34 0 68" fill="none" stroke="#C8944A" stroke-width="8" stroke-linecap="round"/>') + '</svg>')
scene(1, R("""DARK(L,{stars:true});""" + LBL(1) + """
FACADE(L,280,{id:'a1',type:1,n:4,lit:true});var er=MK.el('div','left:760px;top:540px;width:240px;height:280px',@E@,L.root);er.className='mk-a';L.on(function(t){er.style.opacity=MK.pr(t,.5,.4)});
@SUB@""", E=json.dumps(EAR(True)), SUB=sub(1)), dolly=.04)
ev(1, .5, 'pop')
scene(2, R("""DARK(L,{stars:true});""" + LBL(2) + """
FACADE(L,280,{id:'b2',type:2,n:4,lit:true});var er=MK.el('div','left:780px;top:540px;width:240px;height:280px',@E@,L.root);er.className='mk-a';L.on(function(t){er.style.opacity=MK.pr(t,.5,.4);er.style.transform='scale('+(1+Math.sin(t*4)*.03)+')'});
@SUB@""", E=json.dumps(EAR(False)), SUB=sub(2)), dolly=.04)
ev(2, .5, 'pop')
u3r, u3w = F('r3', 'raka'), F('w3', 'wt', True)
w3k = W(3, 'komplain', 1.6)
scene(3, R("""CAFE(L,{type:1});TABLE(L,360,1130);CUP(L,450,1100);
var rk=FIG(L,'@R@',250,820,230,false);var wt=FIG(L,'@W@',0,800,240,true);
L.on(function(t){var w=MK.E.io(MK.pr(t,.2,1.4));wt.style.transform='translateX('+(1100-w*480)+'px) scaleX(-1)';WALK('@W@',t,t>.2&&t<1.6);ARM('@R@','ra',t>@K@-.6?-150+Math.sin(t*6)*8:-5);SMILE('@R@',0)});
@SUB@""", R=u3r, W=u3w, K=w3k, SUB=sub(3)), dolly=.05)
u4r, u4w = F('r4', 'raka'), F('w4', 'wt', True)
scene(4, R("""CAFE(L,{type:1});TABLE(L,300,1130);
var rk=FIG(L,'@R@',180,820,230,false);var wt=FIG(L,'@W@',620,780,250,true);
BUB(L,120,520,460,'“Mas, menu yang<br>paling enak apa?”',.1);BUB(L,560,440,440,'“...ya baca aja<br>menunya.”',.9,'#D98C7A');
var an=MK.el('div','left:760px;top:740px;width:120px;height:60px','<svg viewBox="0 0 60 30" width="120" height="60"><path d="M6 6 L26 16 M54 6 L34 16" stroke="#0F0E0C" stroke-width="6" stroke-linecap="round"/></svg>',L.root);an.className='mk-a';
L.on(function(t){SMILE('@W@',-.8);HEAD('@W@',t>.9?-10:0);ARM('@W@','la',t>.9?40:0);SMILE('@R@',t>1.2?-.6:.2);HEAD('@R@',t>1.2?8:0);an.style.opacity=t>.9?1:0});
@SUB@""", R=u4r, W=u4w, SUB=sub(4)), dolly=.06)
ev(4, .1, 'pop'); ev(4, .9, 'stamp')
u5o, u5r = F('o5', 'ow'), F('r5', 'raka')
w5b = W(5, 'badmood', 2.8)
scene(5, R("""CAFE(L,{type:1});
var ow=FIG(L,'@O@',160,700,260,false);var rk=FIG(L,'@R@',700,820,220,true);
BUB(L,520,540,460,'“Pelayannya<br>ketus, Pak.”',.0,'#F4EBD9',1.6);
var th=MK.el('div','left:60px;top:430px;width:500px;height:240px','<svg viewBox="0 0 250 120" width="500" height="240"><ellipse cx="130" cy="50" rx="115" ry="45" fill="#F4EBD9" stroke="#0F0E0C" stroke-width="4"/><circle cx="60" cy="104" r="9" fill="#F4EBD9" stroke="#0F0E0C" stroke-width="3"/><circle cx="44" cy="116" r="5" fill="#F4EBD9" stroke="#0F0E0C" stroke-width="3"/><text x="130" y="44" text-anchor="middle" font-family="Outfit,sans-serif" font-size="26" fill="#0F0E0C">hal kecil...</text><text x="130" y="74" text-anchor="middle" font-family="Outfit,sans-serif" font-size="26" fill="#0F0E0C">badmood aja</text></svg>',L.root);th.className='mk-a';
L.on(function(t){var s=t>1.6?Math.sin((t-1.6)*8)*.5+.5:0;ARM('@O@','la',-40*s-10);ARM('@O@','ra',40*s+10);HEAD('@O@',t>1.6?-8:0);th.style.opacity=MK.pr(t,@B@-1,.4);SMILE('@R@',-.5)});
@SUB@""", O=u5o, R=u5r, B=w5b, SUB=sub(5)), dolly=.04)
ev(5, 1.6, 'pop')
# ===== B1 =====
u6d, u6w = F('d6', 'dita'), F('w6', 'wt', True)
scene(6, R("""CAFE(L,{type:2});TABLE(L,300,1130);CUP(L,400,1100);
var dt=FIG(L,'@D@',180,820,230,false);var wt=FIG(L,'@W@',620,780,250,true);
BUB(L,560,460,420,'“...ya baca aja<br>menunya.”',.3,'#D98C7A',1.6);
L.on(function(t){SMILE('@W@',-.8);SMILE('@D@',t>.8?-.6:0);ARM('@D@','ra',t>1.8?-150:-5)});
@SUB@""", D=u6d, W=u6w, SUB=sub(6)), dolly=.05)
ev(6, .3, 'stamp')
u7o, u7w = F('o7', 'ow'), F('w7', 'wt', True)
w7n = W(7, 'ngobrol', 1.4)
scene(7, R("""CAFE(L,{type:2});
var ow=FIG(L,'@O@',0,760,250,false);var wt=FIG(L,'@W@',620,780,240,true);
BUB(L,90,470,440,'“Kita obrolin<br>sebentar, ya.”',@N@,'#F4EBD9');
L.on(function(t){var w=MK.E.io(MK.pr(t,0,1.2));ow.style.transform='translateX('+(80+w*260)+'px)';WALK('@O@',t,t<1.2);ARM('@O@','ra',t>@N@?-60+Math.sin(t*5)*12:0);
HEAD('@W@',t>@N@+.8?Math.sin(t*6)*10:0);SMILE('@W@',t>@N@+1.6?.2:-.5)});
@SUB@""", O=u7o, W=u7w, N=w7n, SUB=sub(7)), dolly=.04)
u8o, u8d = F('o8', 'ow'), F('d8', 'dita')
scene(8, R("""CAFE(L,{type:2});TABLE(L,580,1130);CUP(L,680,1100);
var ow=FIG(L,'@O@',230,760,260,false);var dt=FIG(L,'@D@',700,820,230,true);
BUB(L,96,450,620,'“Mohon maaf, Kak.<br>Kami akan perbaiki<br>pelayanan kami.”',.1,'#F4EBD9');
var hs=[];for(var i=0;i<5;i++){var e=MK.el('div','left:'+(760+i*30)+'px;top:760px;font-size:40px;color:#D98C7A','♥',L.root);e.className='mk-a';hs.push(e)}
L.on(function(t){var b=Math.sin(Math.min(1,t/.6)*Math.PI)*.0;var bw=t>.1&&t<1.2?MK.E.io(Math.min(1,(t-.1)/.4))*18:0;RT('@O@_b',bw,100,330);SMILE('@O@',.4);SMILE('@D@',MK.pr(t,1.4,.5));
for(var i=0;i<5;i++){var p=((t-1.6)*.6+i*.2)%1;hs[i].style.transform='translateY('+(-p*200)+'px)';hs[i].style.opacity=t>1.6?1-p:0}});
@SUB@""", O=u8o, D=u8d, SUB=sub(8)), dolly=.05)
ev(8, 1.6, 'chime')
# ===== B2 =====
scene(9, R("""DARK(L,{stars:true,moon:true});
FACADE(L,10,{id:'a9',type:1,n:function(t){return 4-Math.min(4,Math.floor(t*1.2))},lit:true});FACADE(L,550,{id:'b9',type:2,n:4,lit:true});
var rd=MK.el('div','left:0;top:1320px;width:1080px;height:600px;background:#1b1612;border-top:6px solid #0F0E0C',' ',L.root);rd.className='mk-a';
var cal=MK.el('div','left:400px;top:260px;width:280px;height:280px;background:#F4EBD9;border:5px solid #0F0E0C;border-radius:12px;overflow:hidden;text-align:center','<div style="height:60px;background:#B84A2E"></div><div id="c9" class="mk-fr" style="font-size:72px;line-height:120px">1</div><div class="mk-mono" style="font-size:24px">BULAN</div>',L.root);cal.className='mk-a';
L.on(function(t){var c=$('c9');if(c)c.textContent=Math.min(3,1+Math.floor(t*1.2))});
@SUB@""", SUB=sub(9)), dolly=.03)
[ev(9, i * .83, 'tick') for i in range(3)]
scene(10, R("""CAFE(L,{type:1,dim:function(t){return Math.min(.45,t*.15)}});TABLE(L,360,1130);
var ch=MK.el('div','left:620px;top:980px;width:140px;height:200px','<svg viewBox="0 0 70 100" width="140" height="200"><rect x="6" y="40" width="58" height="10" fill="#8a5a3a" stroke="#0F0E0C" stroke-width="4"/><path d="M10 0 V100 M60 50 V100 M10 0 h50 V50" fill="none" stroke="#0F0E0C" stroke-width="6"/></svg>',L.root);ch.className='mk-a';
var gh=MK.el('div','left:600px;top:760px;width:200px;height:380px',FG['r3'].replace(/id="r3_/g,'id="g10_'),L.root);gh.className='mk-a';
L.on(function(t){gh.style.opacity=Math.max(0,.6-t*.5)});
@SUB@""", SUB=sub(10)), dolly=.05)
u11 = [F('c11%d' % i, k) for i, k in enumerate(['f1', 'f2', 'f3', 'raka'])]
scene(11, R("""CAFE(L,{type:1,dim:function(t){return .35+Math.min(.3,t*.08)}});
var U=@U@,vv=U.map(function(u,i){return FIG(L,u,0,820,200,true)});
var dr=MK.el('div','left:900px;top:700px;width:160px;height:460px;background:#14100c;border:6px solid #5a3b24',' ',L.root);dr.className='mk-a';
L.on(function(t){for(var i=0;i<4;i++){var s=.3+i*.9,w=MK.E.io(MK.pr(t,s,1.6));vv[i].style.transform='translateX('+(80+i*170+w*(820-i*170))+'px) scaleX(-1)';vv[i].style.opacity=w>.95?0:1;WALK(U[i],t+i,t>s&&w<1);SMILE(U[i],-.3)}});
@SUB@""", U=json.dumps(u11), SUB=sub(11)), dolly=.04)
[ev(11, .3 + i * .9, 'slide') for i in range(4)]
u12 = [F('g12%d' % i, k) for i, k in enumerate(['dita', 'f1', 'f2', 'f3'])]
scene(12, R("""CAFE(L,{type:2});
var dr=MK.el('div','left:20px;top:700px;width:160px;height:460px;background:#F0C77E;border:6px solid #5a3b24',' ',L.root);dr.className='mk-a';
var U=@U@,vv=U.map(function(u,i){return FIG(L,u,0,820,200,false)});
L.on(function(t){for(var i=0;i<4;i++){var s=.1+i*.35,w=MK.E.io(MK.pr(t,s,1.5));vv[i].style.transform='translateX('+(20+w*(620-i*150))+'px)';vv[i].style.opacity=t>s?1:0;WALK(U[i],t+i,t>s&&w<1);SMILE(U[i],.7)}});
@SUB@""", U=json.dumps(u12), SUB=sub(12)), dolly=.04)
[ev(12, .1 + i * .35, 'tick') for i in range(4)]
u13 = [F('t13%d' % i, k) for i, k in enumerate(['dita', 'f1', 'f2', 'f3'])]
scene(13, R("""CAFE(L,{type:2});TABLE(L,280,1130);TABLE(L,520,1130);for(var i=0;i<4;i++)CUP(L,330+i*130,1100);
var U=@U@,vv=U.map(function(u,i){return FIG(L,u,140+i*190,820,200,i>1)});
BUB(L,96,440,800,'“Cafe ini ramah,<br>mau menghargai pendapat pelanggan.”',1.2,'#F4EBD9');
L.on(function(t){for(var i=0;i<4;i++){SMILE(U[i],.6+Math.sin(t*6+i)*.3);HEAD(U[i],Math.sin(t*4+i)*8);BOB(U[i],t+i,3)}});
@SUB@""", U=json.dumps(u13), SUB=sub(13)), dolly=.05)
ev(13, 1.2, 'pop')
# ===== B3 poros =====
w14e, w14v, w14l = W(14, 'exit', 2.4), W(14, 'voice', 3.2), W(14, 'loyalty', 3.9)
scene(14, R("""DARK(L,{bg:'#080706'});
var sp=MK.el('div','left:240px;top:0;width:600px;height:1400px;background:linear-gradient(rgba(244,235,217,.16),rgba(244,235,217,0));clip-path:polygon(42% 0,58% 0,100% 100%,0 100%)',' ',L.root);sp.className='mk-a';
var ex=MK.el('div','left:110px;top:560px;width:330px;height:520px;border:6px solid #F4EBD9;background:#0b0a08;text-align:center','<div class="mk-fr" style="font-size:64px;color:#9a9590;margin-top:200px">EXIT</div><div class="mk-ou" style="font-size:30px;color:#9a9590">pergi diam-diam</div>',L.root);ex.className='mk-a';
var vc=MK.el('div','left:640px;top:560px;width:330px;height:520px;text-align:center','<svg viewBox="0 0 165 160" width="330" height="320"><path d="M10 10 h145 v100 h-90 l-30 30 v-30 h-25z" fill="#C8944A" stroke="#0F0E0C" stroke-width="5"/></svg><div class="mk-fr" style="font-size:64px;color:#C8944A">VOICE</div><div class="mk-ou" style="font-size:30px;color:#F4EBD9">bersuara</div>',L.root);vc.className='mk-a';
var ly=MK.el('div','left:470px;top:1120px;width:140px;font-size:120px;color:#D98C7A;text-align:center','♥',L.root);ly.className='mk-a';
L.on(function(t){sp.style.opacity=MK.pr(t,.2,.6);var a=MK.pr(t,@E@,.35),b=MK.pr(t,@V@,.35),c=MK.pr(t,@L@,.35);ex.style.opacity=a;ex.style.transform='translateY('+((1-MK.E.out(a))*60)+'px)';vc.style.opacity=b;vc.style.transform='translateY('+((1-MK.E.out(b))*60)+'px)';ly.style.opacity=c;ly.style.transform='scale('+(.5+.5*MK.E.over(c)+Math.sin(t*6)*.04)+')'});
@SUB@""", E=w14e, V=w14v, L=w14l, SUB=sub(14)), dolly=.05)
ev(14, w14e, 'pop'); ev(14, w14v, 'pop'); ev(14, w14l, 'chime')
scene(15, R("""DARK(L,{bg:'#080706'});
var fr=MK.el('div','left:96px;top:330px;width:888px;height:900px;border-radius:24px;background:#F4EBD9;border:6px solid #0F0E0C;box-shadow:0 40px 80px -30px rgba(0,0,0,.8)',' ',L.root);fr.className='mk-a';
var tg=MK.el('div','left:140px;top:370px;font-size:26px;letter-spacing:.1em;color:#B84A2E','KARTU TOKOH',L.root);tg.className='mk-a mk-mono';
var pt=MK.el('div','left:390px;top:410px;width:300px;height:415px',@G@,L.root);pt.className='mk-a';
var nm=MK.el('div','left:140px;top:850px;width:800px;text-align:center;font-size:62px;white-space:nowrap;line-height:1;color:#0F0E0C','ALBERT HIRSCHMAN',L.root);nm.className='mk-a mk-fr';
var s1=MK.el('div','left:140px;top:940px;width:800px;text-align:center;font-size:34px;color:#0F0E0C','Ekonom (1915–2012)',L.root);s1.className='mk-a mk-ou';
var s2=MK.el('div','left:140px;top:990px;width:800px;text-align:center;font-size:34px;color:#B84A2E','Penulis <i>Exit, Voice, and Loyalty</i> (1970)',L.root);s2.className='mk-a mk-ou';
L.on(function(t){var k=MK.E.over(MK.pr(t,0,.5));[fr,tg,pt,nm,s1,s2].forEach(function(e,i){e.style.opacity=MK.pr(t,i*.1,.3)});fr.style.transform='rotate(1.5deg) scale('+(.8+.2*k)+')';pt.style.transform='translateY('+((1-k)*60)+'px) rotate('+(Math.sin(t*1.5)*2)+'deg)'});
@SUB@""", G=json.dumps(HIRS), SUB=sub(15)), dolly=.05)
ev(15, 0, 'stamp'); ev(15, .4, 'pop')
u16 = F('p16', 'raka')
w16p, w16n, w16k = W(16, 'pergi', 3.3), W(16, 'ngomong', 4), W(16, 'kesempatan', 8)
scene(16, R("""DARK(L);
var rd=MK.el('div','left:0;top:0;width:1080px;height:1920px',LINE(1080,1920,'<path d="M540 1400 V1100 L240 700 M540 1100 L840 700" stroke-width="10"/>'),L.root);rd.className='mk-a';
var ex=MK.el('div','left:130px;top:470px;width:220px;height:300px;border:6px solid #9a9590;text-align:center','<div class="mk-fr" style="font-size:44px;color:#9a9590;margin-top:110px">EXIT</div>',L.root);ex.className='mk-a';
var vc=MK.el('div','left:720px;top:470px;width:240px;height:240px','<svg viewBox="0 0 165 160" width="240" height="233"><path d="M10 10 h145 v100 h-90 l-30 30 v-30 h-25z" fill="#C8944A" stroke="#0F0E0C" stroke-width="5"/></svg>',L.root);vc.className='mk-a';
var p=FIG(L,'@P@',440,1080,180,false);
L.on(function(t){HEAD('@P@',t<@A@?Math.sin(t*2)*14:(t<@B@?-14:14));var g=MK.pr(t,@K@,.5);vc.style.transform='scale('+(1+g*.15+Math.sin(t*5)*.03*g)+')';vc.style.filter=g>0?'drop-shadow(0 0 30px rgba(200,148,74,.8))':'none';ex.style.opacity=1-g*.6});
@SUB@""", P=u16, A=w16p, B=w16n, K=w16k, SUB=sub(16)), tr=True, dolly=.05)
ev(16, w16k, 'chime')
# ===== B4 cetak biru =====
w17j = W(17, 'jutek', 4.5)
scene(17, R(BP + """
var ph=MK.el('div','left:270px;top:400px;width:540px;height:860px;border:6px solid #F4EBD9;border-radius:56px',' ',L.root);ph.className='mk-a';
var hd=MK.el('div','left:320px;top:460px;font-size:28px;color:#F4EBD9','DM · pelanggan',L.root);hd.className='mk-a mk-mono';
BUB(L,320,560,420,'Kak, adminnya jutek ya.',@J@-1.2,'#F4EBD9');
L.on(function(t){});
@SUB@""", J=w17j, SUB=sub(17)), tr=True, dolly=.04)
ev(17, w17j - 1.2, 'tick')
w18 = [W(18, x, d) for x, d in (('loyal', 5.5), ('jangan', 6.4), ('solusi', 8), ('selesai', 9))]
scene(18, R(BP + """
var st=MK.el('div','left:96px;top:330px;padding:16px 28px;border:6px solid #C8944A;border-radius:12px;color:#C8944A;font-size:40px;transform:rotate(-3deg)','DARI BISNIS YANG SAYA DAMPINGI',L.root);st.className='mk-a mk-fr';
var lb=['KOMPLAIN','DENGAR','SOLUSI','SELESAI'],AT=@A@,bx=[];for(var i=0;i<4;i++){var e=MK.el('div','left:'+(96+i*230)+'px;top:700px;width:200px;height:200px;border:5px solid #F4EBD9;border-radius:18px;text-align:center;color:#F4EBD9','<div class="mk-fr" style="font-size:30px;margin-top:40px">'+lb[i]+'</div><div class="ck" style="font-size:80px;color:#C8944A"></div>',L.root);e.className='mk-a';bx.push(e)}
var ar=MK.el('div','left:96px;top:940px;width:888px;height:60px',LINE(888,60,'<path d="M20 30 H860 M840 14 L862 30 L840 46"/>'),L.root);ar.className='mk-a';
var lo=MK.el('div','left:96px;top:1080px;width:888px;font-size:64px;color:#F4EBD9;line-height:1.05','Yang komplain = <span style="color:#C8944A">pelanggan loyal.</span>',L.root);lo.className='mk-a mk-fr';
L.on(function(t){var k=MK.pr(t,.1,.25);st.style.opacity=k;st.style.transform='rotate(-3deg) scale('+(1.3-.3*MK.E.out(k))+')';for(var i=0;i<4;i++){bx[i].style.opacity=MK.pr(t,.6+i*.15,.3);var c=bx[i].querySelector('.ck');if(c)c.textContent=t>AT[i]?'✓':''}lo.style.opacity=MK.pr(t,AT[0]-.3,.4)});
@SUB@""", A=json.dumps(w18), SUB=sub(18)), dolly=.04)
ev(18, .1, 'stamp'); [ev(18, a, 'tick') for a in w18]
w19r = W(19, 'rekomendasi', 3)
scene(19, R(BP + """
var hd=MK.el('div','left:96px;top:330px;width:888px;font-size:56px;color:#C8944A','Diselesaikan →',L.root);hd.className='mk-a mk-fr';
var a=""" + LF(440, 760, 1.6) + """;a.className='mk-a';a.firstChild.setAttribute('width',160);a.firstChild.setAttribute('height',320);a.firstChild.querySelector('g').setAttribute('stroke','#C8944A');
var fr=[];for(var i=0;i<3;i++){var e=""" + LF(0, 0, 1.3) + """;e.className='mk-a';e.firstChild.setAttribute('width',130);e.firstChild.setAttribute('height',260);fr.push(e)}
L.on(function(t){for(var i=0;i<3;i++){var k=MK.E.out(MK.pr(t,@R@-.4+i*.25,.8));fr[i].style.transform='translate('+(140+i*260+(1-k)*400)+'px,'+(1140)+'px)';fr[i].style.opacity=k}});
@SUB@""", R=w19r, SUB=sub(19)), tr=True, dolly=.03)
[ev(19, w19r - .4 + i * .25, 'pop') for i in range(3)]
w20p = W(20, 'pergi', 3.6)
scene(20, R(BP + """
var hd=MK.el('div','left:96px;top:330px;width:888px;font-size:56px;color:#9a9590','Diabaikan →',L.root);hd.className='mk-a mk-fr';
var fs=[];for(var i=0;i<7;i++){var e=""" + LF(0, 0, 1.3) + """;e.className='mk-a';e.firstChild.setAttribute('width',130);e.firstChild.setAttribute('height',260);fs.push(e)}
L.on(function(t){for(var i=0;i<7;i++){var s=i==0?.2:1.2+i*.22,w=MK.E.io(MK.pr(t,s,1.6));var x=440+(i?((i*137)%600)-300:0)-w*900,y=760+(i?((i*71)%300):0);fs[i].style.transform='translate('+x+'px,'+y+'px) scaleX(-1)';fs[i].style.opacity=t>s-.3||i==0?Math.max(0,1-w):0}});
@SUB@""", SUB=sub(20)), dolly=.03)
[ev(20, 1.2 + i * .22, 'slide') for i in range(1, 7, 2)]
w21m = W(21, 'mana', 3.6)
scene(21, R("""DARK(L,{stars:true});
FACADE(L,10,{id:'a21',type:1,n:0,lit:false});FACADE(L,550,{id:'b21',type:2,n:4,lit:true});GLOW(L,810,1000,300,0);
var rd=MK.el('div','left:0;top:1320px;width:1080px;height:600px;background:#1b1612;border-top:6px solid #0F0E0C',' ',L.root);rd.className='mk-a';
var q=MK.el('div','left:96px;top:270px;width:888px;text-align:center;font-size:88px;line-height:1.04;color:#F4EBD9','Kamu mau jadi<br><span style="color:#C8944A">tipe yang mana?</span>',L.root);q.className='mk-a mk-fr';
L.on(function(t){var k=MK.pr(t,@M@-1,.5);q.style.opacity=k;q.style.transform='translateY('+((1-MK.E.out(k))*30)+'px)'});
@SUB@""", M=w21m, SUB=sub(21)), dolly=.05)
ev(21, w21m - 1, 'chime')
html = ('<!DOCTYPE html>\n<html><head><meta charset="utf-8"><title>Fabel Bisnis 02</title><link rel="stylesheet" href="motionkit/fonts-mk.css"></head><body>\n'
        '<script src="motionkit/kit.js"></script>\n<script>\nvar C=MK.C;\nvar FG=' + json.dumps(FIGS) + ';\n' + HELP + FAB + FAB2 + CAFE_JS + '\nMK.run([\n' + ',\n'.join(S) + '\n]);\n</script>\n</body></html>\n')
open(A + 'mk-fabel02.html', 'w', encoding='utf-8').write(html)
json.dump({'duration': tl['duration'], 'events': EV, 'cuts': T0}, open(os.path.join(OUT, 'events.json'), 'w'))
print('ok', len(S), 'adegan', round(sum(DUR), 1), 'dtk'); print([(SC[i][0], DUR[i]) for i in range(len(SC))])
