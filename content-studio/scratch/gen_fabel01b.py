"""Fabel Bisnis #01 ekor tikus: animasi penuh Motion Kit dari timing.json vo_prep.
Pakai: python3 scratch/gen_metrik.py out/reel17/timing.json -> animatic/mk-fabel01b.html + out/reel17/events.json"""
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
SC = [('seorang',0,0),('dalam',0,0),('tuan',0,0),('desanya',0,0),
      ('tapi',1,0),('tikusnya',1,0),('warga',1,0),('tikus',1,1),('dan',1,0),('beberapa',1,0),('gak',1,0),('semua',1,0),
      ('di',2,0),('hukum',2,0),('begitu',2,0),
      ('kamu',3,0),('admin',3,0),('chat',3,1),('tim',3,0),('followers',3,1),('sales',3,0),('omzet',3,1),('ekornya',3,0),('tikusnya',3,0),
      ('jadi',4,0),('yang',4,0)]
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
DROP = {3, 10}
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
LT = 'L.headline=true;'
def LORDF(u): return F(u, 'lord')
# ===== B0 =====
w0c = W(0, 'koin', 2.4)
u0l, u0v = LORDF('l0'), F('v0a', 'v1', True)
scene(0, R("""VILLAGE(L,{y:600});GLOW(L,800,1000,320,0);
var hl=MK.el('div','left:96px;top:250px;width:900px;font-size:92px;line-height:1.02;color:#F4EBD9','Satu koin<br>untuk satu <span style="color:#D98C7A">ekor.</span>',L.root);hl.className='mk-a mk-fr';""" + LT + """
var tb=MK.el('div','left:560px;top:1130px;width:420px;height:40px;background:#5a3b24;border:6px solid #0F0E0C;border-radius:6px',' ',L.root);tb.className='mk-a';
var lo=FIG(L,'@L@',760,820,230,true);var vi=FIG(L,'@V@',0,860,200,false);
var tl=MK.el('div','left:0;top:0;width:80px;height:40px',TAIL(),L.root);tl.className='mk-a';
var cn=MK.el('div','left:0;top:0;width:60px;height:60px',COIN(60),L.root);cn.className='mk-a';
L.on(function(t){var w=MK.E.io(MK.pr(t,0,1.6));vi.style.transform='translateX('+(120+w*320)+'px)';WALK('@V@',t,t<1.6);ARM('@V@','ra',t<1.6?-20:-70);
var hx=120+w*320+150,hy=1000;tl.style.transform='translate('+(t<@C@?hx:hx+60)+'px,'+(t<@C@?hy:1110)+'px) rotate(-10deg)';
ARM('@L@','ra',t>@C@-.5&&t<@C@+.6?-75:-5);HEAD('@L@',Math.sin(t*1.5)*4);SMILE('@L@',t>@C@?.6:0);
var f=MK.pr(t,@C@-.1,.6);cn.style.opacity=f>0&&f<1?1:(f>=1?1:0);cn.style.transform='translate('+(760-f*240)+'px,'+(1000-Math.sin(f*Math.PI)*160+f*20)+'px) rotateY('+(f*720)+'deg)';ARM('@V@','la',f>.9?-60:0);SMILE('@V@',f>.9?.8:0)});
@SUB@""", L=u0l, V=u0v, C=w0c, SUB=sub(0)))
ev(0, .2, 'slide'); ev(0, w0c - .1, 'sweep'); ev(0, w0c + .5, 'tick')
# 1 sebulan: kalender + antrean + tumpukan + angka
u1 = [F('v1%d' % i, k, True) for i, k in enumerate(['v1', 'v2', 'v3', 'v4', 'v5'])]; u1l = LORDF('l1')
scene(1, R("""DARK(L,{stars:true});GLOW(L,860,900,300,0);
var cal=MK.el('div','left:96px;top:300px;width:250px;height:280px;background:#F4EBD9;border:5px solid #0F0E0C;border-radius:12px;overflow:hidden','<div style="height:60px;background:#B84A2E"></div><div id="cald" class="mk-fr" style="text-align:center;font-size:130px;line-height:200px">1</div>',L.root);cal.className='mk-a';
MK.CountUp(L,{x:400,y:380,from:0,to:1284,at:.6,dur:2.6,size:110,suffix:'ekor',color:'#F4EBD9'});
var tb=MK.el('div','left:640px;top:1150px;width:440px;height:40px;background:#5a3b24;border:6px solid #0F0E0C',' ',L.root);tb.className='mk-a';
var lo=FIG(L,'@L@',820,830,220,true);var U=@U@,vv=U.map(function(u,i){return FIG(L,u,0,880,180,false)});
var pile=MK.el('div','left:650px;top:900px;width:200px;height:250px',' ',L.root);pile.className='mk-a';var ph='';for(var i=0;i<36;i++)ph+='<div style="position:absolute;left:'+((i*53)%150)+'px;bottom:'+(Math.floor(i/4)*14)+'px;transform:rotate('+((i*41)%60-30)+'deg)">'+TAIL()+'</div>';pile.innerHTML=ph;
L.on(function(t){var d=document.getElementById('cald');if(d)d.textContent=Math.min(30,1+Math.floor(t*9));
for(var i=0;i<5;i++){var x=40+i*120+Math.sin(t*1.3+i)*6;vv[i].style.transform='translateX('+x+'px)';WALK(U[i],t+i,Math.floor(t*2+i)%3==0)}ARM('@L@','ra',-40-Math.abs(Math.sin(t*5))*40);
var n=Math.min(36,Math.floor(t*12));var ch=pile.children;for(var i=0;i<ch.length;i++)ch[i].style.opacity=i<n?1:0});
@SUB@""", U=json.dumps(u1), L=u1l, SUB=sub(1)), tr=True, dolly=.04)
ev(1, .1, 'sweep'); [ev(1, .6 + i * .5, 'tick') for i in range(5)]
# 2 tuan tanah tersenyum (close-up)
u2 = LORDF('l2')
scene(2, R("""DARK(L);GLOW(L,540,800,420,0);
var lo=FIG(L,'@L@',190,330,700,false);
var mn=MK.el('div','left:130px;top:1180px;width:820px;text-align:center;font-size:56px;color:#F4EBD9','“Desaku pasti sudah bersih.”',L.root);mn.className='mk-a mk-fri';
L.on(function(t){HEAD('@L@',Math.sin(t*1.2)*5);SMILE('@L@',MK.pr(t,.3,.5));ARM('@L@','la',Math.sin(t*1.5)*6);ARM('@L@','ra',-Math.sin(t*1.5)*6);mn.style.opacity=MK.pr(t,1.2,.4)});
@SUB@""", L=u2, SUB=sub(2)), dolly=.09)
ev(2, .3, 'pop')
# 3 desa tidur, lampu padam satu per satu
scene(3, R("""VILLAGE(L,{y:520,off:.4,id:'d3'});
var cl=MK.el('div','left:96px;top:330px;width:888px;font-size:64px;color:#F4EBD9;line-height:1.05','Desa yang <span style="color:#C8944A">tenang.</span>',L.root);cl.className='mk-a mk-fr';L.on(function(t){cl.style.opacity=MK.pr(t,.2,.4)});
@SUB@""", SUB=sub(3)), dolly=.05)
# ===== B1 =====
u4 = LORDF('l4')
w4g = W(4, 'gudang', 2.1)
scene(4, R("""DARK(L,{bg:'#0d0b09',stars:true});
var bn=MK.el('div','left:520px;top:520px;width:520px;height:700px','<svg viewBox="0 0 260 350" width="520" height="700"><path d="M10 120 L130 30 L250 120 V340 H10Z" fill="#2a1f17" stroke="#0F0E0C" stroke-width="5"/><rect x="70" y="190" width="120" height="150" fill="#140f0b" stroke="#5a3b24" stroke-width="5"/><path d="M70 190 L190 340 M190 190 L70 340" stroke="#5a3b24" stroke-width="4"/></svg>',L.root);bn.className='mk-a';
var lo=FIG(L,'@L@',0,820,230,false);var ln=MK.el('div','left:0;top:0;width:60px;height:110px','<svg viewBox="0 0 30 55" width="60" height="110"><path d="M15 0 V8" stroke="#0F0E0C" stroke-width="3"/><rect x="5" y="8" width="20" height="30" rx="5" fill="#F0C77E" stroke="#0F0E0C" stroke-width="3"/></svg>',L.root);ln.className='mk-a';var gl=GLOW(L,0,0,220,0);
var sd=MK.el('div','left:620px;top:420px;font-size:90px;color:#F4EBD9','!',L.root);sd.className='mk-a mk-fr';
L.on(function(t){var w=MK.E.io(MK.pr(t,0,@G@));var x=40+w*300;lo.style.transform='translateX('+x+'px)';WALK('@L@',t,t<@G@);ARM('@L@','ra',-60);ln.style.transform='translate('+(x+190)+'px,'+(930+Math.sin(t*14)*3)+'px)';gl.style.transform='translate('+(x+220-0)+'px,'+(980-220)+'px)';gl.style.left='0px';gl.style.top='0px';
var s=MK.pr(t,@G@,.2);sd.style.opacity=s*(Math.floor(t*6)%2?1:.4);HEAD('@L@',t>@G@?12:0);bn.style.transform='translateX('+(t>@G@&&t<@G@+.4?Math.sin(t*70)*5:0)+'px)'});
@SUB@""", L=u4, G=w4g, SUB=sub(4)), tr=True, dolly=.05)
ev(4, .2, 'slide'); ev(4, w4g, 'stamp')
# 5 pintu gudang terbuka: tikus membanjir
scene(5, R("""DARK(L,{bg:'#0b0a08'});
var dr=MK.el('div','left:240px;top:420px;width:600px;height:640px;background:#000;border:10px solid #5a3b24',' ',L.root);dr.className='mk-a';
var d1=MK.el('div','left:250px;top:430px;width:290px;height:620px;background:#2a1f17;border-right:5px solid #0F0E0C;transform-origin:left',' ',L.root);d1.className='mk-a';
var d2=MK.el('div','left:540px;top:430px;width:290px;height:620px;background:#2a1f17;border-left:5px solid #0F0E0C;transform-origin:right',' ',L.root);d2.className='mk-a';
var ey=[];for(var i=0;i<24;i++){var e=MK.el('div','left:'+(280+(i*73)%520)+'px;top:'+(470+(i*47)%540)+'px;width:30px;height:10px','<svg viewBox="0 0 30 10" width="30" height="10"><circle cx="5" cy="5" r="4" fill="#F0C77E"/><circle cx="25" cy="5" r="4" fill="#F0C77E"/></svg>',L.root);e.className='mk-a';ey.push(e)}
RATS(L,14,{at:.9,x:300,y:980,sx:420,sy:240,v:420,dir:1,s:.9});RATS(L,10,{at:1.2,x:700,y:1060,sx:300,sy:160,v:380,dir:-1,s:.8});
MK.CountUp(L,{x:96,y:300,from:12,to:640,at:.8,dur:2,size:110,suffix:'tikus',color:'#D98C7A'});
L.on(function(t){var o=MK.E.out(MK.pr(t,.3,.6));d1.style.transform='perspective(900px) rotateY('+(-o*75)+'deg)';d2.style.transform='perspective(900px) rotateY('+(o*75)+'deg)';for(var i=0;i<24;i++)ey[i].style.opacity=t>.2+i*.03?(Math.sin(t*3+i)>.9?0:1):0});
@SUB@""", SUB=sub(5)), dolly=.07)
ev(5, .3, 'sweep'); ev(5, .9, 'slide'); ev(5, 1.3, 'slide')
# 6 gunting memotong ekor (warga berlutut)
u6 = F('v6', 'v2')
scene(6, R("""DARK(L,{stars:true});GLOW(L,540,1000,360,0);
var vi=FIG(L,'@V@',120,700,300,false);
var rt=MK.el('div','left:520px;top:1010px;width:320px;height:180px','<div style="transform:scale(2);transform-origin:0 0">'+RAT('#8a827a',false)+'</div>',L.root);rt.className='mk-a';
var tl=MK.el('div','left:440px;top:1080px;width:160px;height:80px','<div style="transform:scale(2);transform-origin:0 0">'+TAIL()+'</div>',L.root);tl.className='mk-a';
var sc=MK.el('div','left:380px;top:930px;width:240px;height:240px','<svg viewBox="0 0 100 100" width="240" height="240"><g stroke="#0F0E0C" stroke-width="3"><path id="b61" d="M50 50 L96 30" stroke="#C9CCCF" stroke-width="11" stroke-linecap="round"/><path id="b62" d="M50 50 L96 70" stroke="#C9CCCF" stroke-width="11" stroke-linecap="round"/></g><circle cx="33" cy="38" r="13" fill="none" stroke="#B84A2E" stroke-width="7"/><circle cx="33" cy="64" r="13" fill="none" stroke="#B84A2E" stroke-width="7"/></svg>',L.root);sc.className='mk-a';
L.on(function(t){var c=t<.6?Math.sin(t*12)*10:(t<.9?14:0);var a=$('b61'),b=$('b62');if(a){a.setAttribute('transform','rotate('+(-c)+' 50 50)');b.setAttribute('transform','rotate('+c+' 50 50)')}ARM('@V@','ra',-70+Math.sin(t*12)*6);ARM('@V@','la',-50);SMILE('@V@',.5);
var cut=t>.75;tl.style.transform=cut?'translate('+(-(t-.75)*60)+'px,'+Math.min(140,(t-.75)*500)+'px) rotate('+((t-.75)*300)+'deg)':'';sc.style.opacity=t<1.6?1:0;
var r=MK.E.io(MK.pr(t,1.1,1.4));rt.style.transform='translate('+(r*600)+'px,'+(-r*60)+'px)'});
@SUB@""", V=u6, SUB=sub(6)), tr=True, dolly=.06)
ev(6, .3, 'scratch'); ev(6, .75, 'tick'); ev(6, 1.1, 'slide')
# 7 tikus tanpa ekor beranak: 1 -> 2 -> 4 -> 8 -> 16
w7b = W(7, 'beranak', 1.3)
scene(7, R("""DARK(L,{stars:true});
var gr=[];for(var i=0;i<16;i++){var e=MK.el('div','left:'+(110+(i%4)*220)+'px;top:'+(480+Math.floor(i/4)*190)+'px;width:160px;height:90px','<div style="transform:scale(.9);transform-origin:0 0">'+RAT(i?'#9a928a':'#8a827a',false)+'</div>',L.root);e.className='mk-a';gr.push(e)}
var lb=MK.el('div','left:96px;top:300px;font-size:100px;color:#F4EBD9','×<span id="mul">1</span>',L.root);lb.className='mk-a mk-fr';
L.on(function(t){var g=t<@B@?0:Math.floor((t-@B@)/.45)+1;var n=Math.min(16,Math.pow(2,g));for(var i=0;i<16;i++){var k=i<n;gr[i].style.opacity=k?1:0;gr[i].style.transform='translateY('+(-Math.abs(Math.sin(t*9+i))*12)+'px) scale('+(k?1:.3)+')'}var m=$('mul');if(m)m.textContent=n});
@SUB@""", B=w7b, SUB=sub(7)), dolly=.05)
[ev(7, w7b + i * .45, 'pop') for i in range(5)]
# 8 anak tikus jadi koin, hujan koin ke kantong
scene(8, R("""DARK(L,{stars:true});GLOW(L,540,1100,360,0);
var pk=MK.el('div','left:390px;top:1010px;width:300px;height:260px','<svg viewBox="0 0 150 130" width="300" height="260"><path d="M30 30 Q20 120 75 126 Q130 120 120 30Z" fill="#8a5a3a" stroke="#0F0E0C" stroke-width="5"/><path d="M30 30 Q75 46 120 30" fill="none" stroke="#0F0E0C" stroke-width="5"/><path d="M40 26 Q75 0 110 26" fill="none" stroke="#C8944A" stroke-width="5"/></svg>',L.root);pk.className='mk-a';
var rs=[],cs=[];for(var i=0;i<12;i++){var r=MK.el('div','left:'+(100+(i*79)%820)+'px;top:'+(380+(i*53)%380)+'px;width:160px;height:90px','<div style="transform:scale(.6);transform-origin:0 0">'+RAT('#9a928a',false)+'</div>',L.root);r.className='mk-a';rs.push(r);var c=MK.el('div','left:0;top:0;width:66px;height:66px',COIN(66),L.root);c.className='mk-a';cs.push(c)}
L.on(function(t){for(var i=0;i<12;i++){var s=.6+i*.12,f=MK.pr(t,s,.25),fall=Math.max(0,t-s-.25);var x0=100+(i*79)%820+30,y0=380+(i*53)%380;rs[i].style.opacity=1-f;
var tx=x0+(520-x0)*Math.min(1,fall/.7),ty=y0+(1040-y0)*Math.min(1,fall/.7)-Math.sin(Math.min(1,fall/.7)*Math.PI)*120;cs[i].style.transform='translate('+tx+'px,'+ty+'px) rotateY('+(t*600+i*40)+'deg)';cs[i].style.opacity=f>0&&fall<.75?1:0}
pk.style.transform='scale('+(1+Math.min(.25,Math.max(0,t-1.2)*.08))+')'});
@SUB@""", SUB=sub(8)), tr=True, dolly=.04)
[ev(8, 1.3 + i * .24, 'tick') for i in range(0, 12, 2)]
# 9 kandang tikus di belakang rumah, warga memberi makan sambil tersenyum
u9 = F('v9', 'v1')
scene(9, R("""VILLAGE(L,{y:700});
var hs=MK.el('div','left:40px;top:640px;width:520px;height:560px','<svg viewBox="0 0 260 280" width="520" height="560"><path d="M10 110 L130 20 L250 110 V270 H10Z" fill="#3d2817" stroke="#0F0E0C" stroke-width="5"/><rect x="100" y="160" width="60" height="110" fill="#F0C77E" stroke="#0F0E0C" stroke-width="4"/></svg>',L.root);hs.className='mk-a';
var cg=[];for(var i=0;i<4;i++){var e=MK.el('div','left:'+(560+(i%2)*200)+'px;top:'+(900+Math.floor(i/2)*190)+'px;width:180px;height:170px','<svg viewBox="0 0 180 170" width="180" height="170"><rect x="6" y="10" width="168" height="150" fill="rgba(15,14,12,.5)" stroke="#C9CCCF" stroke-width="5"/><g stroke="#C9CCCF" stroke-width="4"><path d="M40 10 V160 M74 10 V160 M108 10 V160 M142 10 V160"/></g></svg><div class="rr" style="position:absolute;left:30px;top:70px;transform:scale(.6);transform-origin:0 0">'+RAT('#9a928a',false)+'</div>',L.root);e.className='mk-a';cg.push(e)}
var vi=FIG(L,'@V@',360,860,200,true);
L.on(function(t){for(var i=0;i<4;i++){var k=MK.pr(t,.2+i*.3,.3);cg[i].style.opacity=k>0?1:0;cg[i].style.transform='scale('+(.6+.4*MK.E.over(k))+')';var r=cg[i].querySelector('.rr');if(r)r.style.transform='scale(.6) translateX('+(Math.sin(t*6+i)*30)+'px)'}
ARM('@V@','ra',-60+Math.sin(t*5)*20);SMILE('@V@',.8);HEAD('@V@',Math.sin(t*2)*6);BOB('@V@',t,2)});
@SUB@""", V=u9, SUB=sub(9)), tr=True, dolly=.05)
[ev(9, .2 + i * .3, 'pop') for i in range(4)]
# 10 papan aturan desa, warga mengangguk
u10 = [F('v10%d' % i, k) for i, k in enumerate(['v2', 'v3', 'v4'])]
scene(10, R("""VILLAGE(L,{y:760});
var bd=MK.el('div','left:200px;top:330px;width:680px;height:520px','<svg viewBox="0 0 340 260" width="680" height="520"><path d="M60 180 V260 M280 180 V260" stroke="#3d2817" stroke-width="14"/><rect x="10" y="10" width="320" height="180" fill="#5a3b24" stroke="#0F0E0C" stroke-width="6"/></svg>',L.root);bd.className='mk-a';
var pp=MK.el('div','left:250px;top:370px;width:580px;padding:22px 28px;background:#F4EBD9;border:4px solid #0F0E0C;transform:rotate(-2deg)','<div class="mk-mono" style="font-size:24px;color:#6B6560">ATURAN DESA</div><div class="mk-fr" style="font-size:56px">1 ekor = 1 koin</div><div id="ok10" class="mk-ou" style="font-size:34px;color:#2f7a4a;opacity:0">✓ tidak ada yang melanggar</div>',L.root);pp.className='mk-a';
var U=@U@,vv=U.map(function(u,i){return FIG(L,u,140+i*290,900,200,i==2)});
L.on(function(t){for(var i=0;i<3;i++){HEAD(U[i],Math.sin(t*5+i)*8);SMILE(U[i],.6);BOB(U[i],t+i,2)}var o=$('ok10');if(o)o.style.opacity=MK.pr(t,.6,.3)});
@SUB@""", U=json.dumps(u10), SUB=sub(10)), tr=True, dolly=.04)
ev(10, .6, 'tick')
# 11 warga pegang ekor & koin, tuan tanah garuk kepala
u11 = [F('v11%d' % i, k) for i, k in enumerate(['v1', 'v5'])]; u11l = LORDF('l11')
w11d = W(11, 'dibayar', 2.5)
scene(11, R("""DARK(L,{stars:true});GLOW(L,540,900,420,0);
var U=@U@;var a=FIG(L,U[0],90,760,230,false);var b=FIG(L,U[1],760,760,230,true);var lo=FIG(L,'@L@',400,700,280,false);
var hd=[];for(var i=0;i<2;i++){var c=MK.el('div','left:'+(i?740:300)+'px;top:900px;width:60px;height:60px',COIN(60),L.root);c.className='mk-a';hd.push(c)}
var q=MK.el('div','left:430px;top:560px;font-size:120px;color:#C8944A','?',L.root);q.className='mk-a mk-fr';
L.on(function(t){ARM(U[0],'ra',-80);ARM(U[1],'ra',-80);SMILE(U[0],.9);SMILE(U[1],.9);hd.forEach(function(c,i){c.style.transform='translateY('+(Math.sin(t*4+i)*8)+'px) rotateY('+(t*200)+'deg)'});
ARM('@L@','ra',-150+Math.sin(t*8)*10);SMILE('@L@',-.6);HEAD('@L@',Math.sin(t*3)*8);var k=MK.pr(t,@D@,.3);q.style.opacity=k;q.style.transform='scale('+(.4+.6*MK.E.over(k))+')'});
@SUB@""", U=json.dumps(u11), L=u11l, D=w11d, SUB=sub(11)), dolly=.06)
ev(11, w11d, 'pop')
# ===== B2 poros =====
u12 = LORDF('l12')
scene(12, R("""DARK(L,{bg:'#080706'});
var sp=MK.el('div','left:240px;top:0;width:600px;height:1400px;background:linear-gradient(rgba(244,235,217,.18),rgba(244,235,217,0));clip-path:polygon(42% 0,58% 0,100% 100%,0 100%)',' ',L.root);sp.className='mk-a';
var lo=FIG(L,'@L@',420,820,240,false);var pile=MK.el('div','left:380px;top:1180px;width:320px;height:80px',[0,1,2,3,4,5].map(function(i){return '<div style="position:absolute;left:'+(i*45)+'px;top:'+((i%2)*14)+'px">'+TAIL()+'</div>'}).join(''),L.root);pile.className='mk-a';
L.on(function(t){sp.style.opacity=MK.pr(t,.2,.8);HEAD('@L@',-12+Math.sin(t)*3);SMILE('@L@',-.3)});
@SUB@""", L=u12, SUB=sub(12)), tr=True, dolly=.1)
ev(12, .2, 'sweep')
scene(13, R("""DARK(L,{bg:'#080706'});
var sp=MK.el('div','left:190px;top:0;width:700px;height:1500px;background:linear-gradient(rgba(244,235,217,.14),rgba(244,235,217,0));clip-path:polygon(40% 0,60% 0,100% 100%,0 100%)',' ',L.root);sp.className='mk-a';
var fr=MK.el('div','left:96px;top:330px;width:888px;height:900px;border-radius:24px;background:#F4EBD9;border:6px solid #0F0E0C;box-shadow:0 40px 80px -30px rgba(0,0,0,.8)',' ',L.root);fr.className='mk-a';
var tg=MK.el('div','left:140px;top:370px;font-size:26px;letter-spacing:.1em;color:#B84A2E','KARTU TOKOH',L.root);tg.className='mk-a mk-mono';
var pt=MK.el('div','left:390px;top:410px;width:300px;height:415px','@G@',L.root);pt.className='mk-a';
var nm=MK.el('div','left:140px;top:850px;width:800px;text-align:center;font-size:60px;white-space:nowrap;line-height:1;color:#0F0E0C','CHARLES GOODHART',L.root);nm.className='mk-a mk-fr';
var s1=MK.el('div','left:140px;top:940px;width:800px;text-align:center;font-size:34px;color:#0F0E0C','Ekonom, mantan penasihat Bank of England',L.root);s1.className='mk-a mk-ou';
var s2=MK.el('div','left:140px;top:990px;width:800px;text-align:center;font-size:34px;color:#B84A2E','Pencetus Hukum Goodhart (1975)',L.root);s2.className='mk-a mk-ou';
L.on(function(t){var k=MK.E.over(MK.pr(t,0,.5));[fr,tg,pt,nm,s1,s2].forEach(function(e,i){e.style.opacity=MK.pr(t,i*.1,.3)});fr.style.transform='rotate(-1.5deg) scale('+(.8+.2*k)+')';pt.style.transform='translateY('+((1-k)*60)+'px) rotate('+(Math.sin(t*1.5)*2)+'deg)'});
@SUB@""", G=GOOD, SUB=sub(13)), dolly=.05)
ev(13, 0, 'stamp'); ev(13, .4, 'pop')
# 14 pemanah: membidik TUJUAN, panah berbelok ke ANGKA
u14 = F('v14', 'v3')
w14t, w14a = W(14, 'tujuannya', 3.6), W(14, 'angkanya', 5.8)
scene(14, R("""DARK(L);
var tj=MK.el('div','left:640px;top:420px;width:340px;height:400px','<svg viewBox="0 0 170 200" width="340" height="400"><circle cx="85" cy="85" r="76" fill="#F4EBD9" stroke="#0F0E0C" stroke-width="6"/><circle cx="85" cy="85" r="52" fill="#B84A2E"/><circle cx="85" cy="85" r="28" fill="#F4EBD9"/><circle cx="85" cy="85" r="10" fill="#B84A2E"/><text x="85" y="192" text-anchor="middle" font-family="Fraunces,serif" font-weight="800" font-size="28" fill="#F4EBD9">TUJUAN</text></svg>',L.root);tj.className='mk-a';
var an=MK.el('div','left:640px;top:960px;width:340px;height:300px;border-radius:18px;background:#1f1b17;border:5px solid #F4EBD9;display:flex;flex-direction:column;align-items:center;justify-content:center','<div id="n14" class="mk-fr" style="font-size:110px;color:#C8944A">0</div><div class="mk-mono" style="font-size:26px;color:#F4EBD9">ANGKA</div>',L.root);an.className='mk-a';
var ar=FIG(L,'@V@',90,760,240,false);var bw=MK.el('div','left:300px;top:820px;width:120px;height:240px','<svg viewBox="0 0 60 120" width="120" height="240"><path d="M10 0 Q60 60 10 120" fill="none" stroke="#8a5a3a" stroke-width="7"/><path d="M10 0 V120" stroke="#F4EBD9" stroke-width="2"/></svg>',L.root);bw.className='mk-a';
var aw=MK.el('div','left:0;top:0;width:160px;height:30px','<svg viewBox="0 0 160 30" width="160" height="30"><path d="M0 15 H140" stroke="#F4EBD9" stroke-width="6"/><path d="M140 4 L160 15 L140 26Z" fill="#F4EBD9"/></svg>',L.root);aw.className='mk-a';
L.on(function(t){ARM('@V@','ra',-90);ARM('@V@','la',-80);HEAD('@V@',t>@T@?18:-8);var f=MK.E.io(MK.pr(t,@T@,1.2));
var sx=330,sy=940,ex1=810,ey1=590,ex2=810,ey2=1090;var x=sx+(ex2-sx)*f,y=sy+(ey1-sy)*Math.min(1,f*1.6)*(1-f)+(ey2-sy)*f*f;if(t<@T@){x=sx;y=sy}
aw.style.transform='translate('+(x-80)+'px,'+(y-15)+'px) rotate('+(t<@T@?-25:(-25+f*60))+'deg)';aw.style.opacity=t>.3?1:0;var n=$('n14');if(n)n.textContent=Math.round(MK.pr(t,@T@+1,1.6)*999);an.style.boxShadow=t>@A@?'0 0 60px 10px rgba(200,148,74,.4)':'none';tj.style.opacity=t>@T@+1.2?.35:1});
@SUB@""", V=u14, T=w14t, A=w14a, SUB=sub(14)), tr=True, dolly=.04)
ev(14, w14t, 'sweep'); ev(14, w14t + 1.2, 'stamp'); ev(14, w14a, 'pop')
# ===== B3 dunia cetak biru =====
BP = "DARK(L,{bg:'#101317'});var grid=MK.el('div','left:0;top:0;width:1080px;height:1920px;background-image:linear-gradient(rgba(244,235,217,.06) 2px,transparent 2px),linear-gradient(90deg,rgba(244,235,217,.06) 2px,transparent 2px);background-size:60px 60px',' ',L.root);grid.className='mk-a';"
scene(15, R(BP + """
var rt=MK.el('div','left:300px;top:640px;width:480px;height:270px','<div style="transform:scale(3);transform-origin:0 0">'+RAT('#20242a')+'</div>',L.root);rt.className='mk-a';
var bd=MK.el('div','left:240px;top:420px;width:600px;height:760px',LINE(600,760,'<path d="M60 740 V180 H300 V740 M300 740 V60 H540 V740 M20 740 H580"/><path d="M100 240 h60 M180 240 h60 M100 320 h60 M180 320 h60 M100 400 h60 M180 400 h60 M340 140 h60 M420 140 h60 M340 220 h60 M420 220 h60 M340 300 h60 M420 300 h60 M340 380 h60 M420 380 h60"/>'),L.root);bd.className='mk-a';
L.on(function(t){var m=MK.pr(t,.5,.8);rt.style.opacity=1-m;rt.style.transform='scale('+(1-m*.3)+') rotate('+(m*20)+'deg)';bd.style.opacity=m;bd.style.clipPath='inset('+((1-m)*100)+'% 0 0 0)'});
@SUB@""", SUB=sub(15)), tr=True, dolly=.06)
ev(15, .5, 'sweep')
def LF(x, y, sc=1, extra=''):
    return "MK.el('div','left:%dpx;top:%dpx;width:%dpx;height:%dpx',LINE(100,200,LFIG()%s),L.root)" % (x, y, 100 * sc, 200 * sc, extra)
scene(16, R(BP + """
var fg=""" + LF(140, 760, 2) + """;fg.className='mk-a';fg.firstChild.setAttribute('width',200);fg.firstChild.setAttribute('height',400);
var lt=MK.el('div','left:300px;top:930px;width:240px;height:150px',LINE(120,75,'<path d="M10 70 H110 M20 70 L30 10 H100 L110 70"/>'),L.root);lt.className='mk-a';lt.firstChild.setAttribute('width',240);lt.firstChild.setAttribute('height',150);
var sw=MK.el('div','left:120px;top:400px;width:260px;height:300px',LINE(130,150,'<circle cx="65" cy="85" r="55"/><path d="M65 30 V18 M50 14 h30"/><path id="swh" d="M65 85 V45"/>'),L.root);sw.className='mk-a';sw.firstChild.setAttribute('width',260);sw.firstChild.setAttribute('height',300);
var bs=[];for(var i=0;i<5;i++){var e=MK.el('div','left:560px;top:'+(380+i*130)+'px;width:420px;padding:16px 22px;border:4px solid #F4EBD9;border-radius:22px 22px 6px 22px;color:#F4EBD9;font-size:34px','dibalas ✓✓ <span style="color:#C8944A">'+(i+1)*7+' dtk</span>',L.root);e.className='mk-a mk-ou';bs.push(e)}
L.on(function(t){var h=$('swh');if(h)h.setAttribute('transform','rotate('+(t*360)+' 65 85)');fg.style.transform='translateY('+(Math.sin(t*20)*3)+'px)';for(var i=0;i<5;i++){var k=MK.pr(t,.4+i*.3,.25);bs[i].style.opacity=k>0?1:0;bs[i].style.transform='translateX('+((1-MK.E.over(k))*200)+'px)'}});
@SUB@""", SUB=sub(16)), dolly=.04)
[ev(16, .4 + i * .3, 'tick') for i in range(0, 5, 2)]
scene(17, R(BP + """
var sh=MK.el('div','left:560px;top:520px;width:420px;height:700px',LINE(210,350,'<path d="M10 340 V60 L105 10 L200 60 V340 Z"/><rect x="70" y="200" width="70" height="140"/><path d="M30 90 h150"/>'),L.root);sh.className='mk-a';sh.firstChild.setAttribute('width',420);sh.firstChild.setAttribute('height',700);
var by=""" + LF(0, 860, 2) + """;by.className='mk-a';by.firstChild.setAttribute('width',200);by.firstChild.setAttribute('height',400);
var ct=MK.el('div','left:120px;top:420px;width:300px;height:220px',LINE(150,110,'<path d="M10 20 h20 l16 60 h80 l14 -46 H40"/><circle cx="56" cy="98" r="8"/><circle cx="114" cy="98" r="8"/>'),L.root);ct.className='mk-a';ct.firstChild.setAttribute('width',300);ct.firstChild.setAttribute('height',220);
var x=MK.el('div','left:400px;top:400px;font-size:180px;color:#B84A2E;line-height:1','×',L.root);x.className='mk-a mk-fr';
L.on(function(t){var w=MK.E.io(MK.pr(t,.3,2.2));by.style.transform='translateX('+(620-w*700)+'px) translateY('+(-Math.abs(Math.sin(t*9))*8)+'px) scaleX(-1)';var c=MK.pr(t,1.6,.25);x.style.opacity=c;x.style.transform='scale('+(.4+.6*MK.E.over(c))+')'});
@SUB@""", SUB=sub(17)), tr=True)
ev(17, 1.6, 'scratch')
w18f = W(18, 'followers', 1.3)
scene(18, R(BP + """
var cr=""" + LF(120, 760, 2) + """;cr.className='mk-a';cr.firstChild.setAttribute('width',200);cr.firstChild.setAttribute('height',400);
var rl=MK.el('div','left:330px;top:700px;width:200px;height:200px',LINE(100,100,'<circle cx="50" cy="50" r="40"/><circle cx="50" cy="50" r="28"/><path d="M50 90 V200"/>'),L.root);rl.className='mk-a';rl.firstChild.setAttribute('width',200);rl.firstChild.setAttribute('height',200);
var ph=MK.el('div','left:560px;top:420px;width:400px;height:700px;border:5px solid #F4EBD9;border-radius:46px',' ',L.root);ph.className='mk-a';
var lb=MK.el('div','left:610px;top:500px;font-size:28px;color:#F4EBD9','FOLLOWERS',L.root);lb.className='mk-a mk-mono';
MK.CountUp(L,{x:610,y:550,from:1200,to:12400,at:@F@,dur:2,size:84,color:'#C8944A'});
var hs=[];for(var i=0;i<10;i++){var e=MK.el('div','left:'+(600+(i*67)%300)+'px;top:900px;font-size:44px;color:#D98C7A','♥',L.root);e.className='mk-a';hs.push(e)}
L.on(function(t){for(var i=0;i<10;i++){var p=((t*.8+i*.13)%1);hs[i].style.transform='translateY('+(-p*360)+'px)';hs[i].style.opacity=t>@F@?(1-p):0}cr.style.transform='rotate('+(Math.sin(t*2)*2)+'deg)'});
@SUB@""", F=w18f, SUB=sub(18)), tr=True, dolly=.04)
ev(18, w18f, 'pop')
scene(19, R(BP + """
var cw=[];for(var i=0;i<14;i++){var e=""" + LF(0, 0, 1) + """;e.className='mk-a';e.style.opacity=.35;cw.push(e)}
var bu=[];for(var i=0;i<3;i++){var e=""" + LF(0, 0, 1.6) + """;e.className='mk-a';e.firstChild.setAttribute('width',160);e.firstChild.setAttribute('height',320);e.firstChild.querySelector('g').setAttribute('stroke','#C8944A');bu.push(e)}
var lb=MK.el('div','left:96px;top:330px;width:888px;font-size:56px;color:#F4EBD9;line-height:1.05','Yang beli: <span style="color:#C8944A">orang yang sama.</span>',L.root);lb.className='mk-a mk-fr';
L.on(function(t){for(var i=0;i<14;i++){var x=((i*170+t*260)%1400)-200,y=980+(i%3)*90;cw[i].style.transform='translate('+x+'px,'+y+'px)'}for(var i=0;i<3;i++)bu[i].style.transform='translate('+(220+i*230)+'px,'+(560+Math.abs(Math.sin(t*3+i))*-10)+'px)';lb.style.opacity=MK.pr(t,1.2,.4)});
@SUB@""", SUB=sub(19)), dolly=.03)
ev(19, 1.2, 'tick')
scene(20, R(BP + """
var gl=MK.el('div','left:96px;top:620px;width:888px;height:0;border-top:5px dashed #C8944A',' ',L.root);gl.className='mk-a';
var gt=MK.el('div','left:96px;top:560px;font-size:28px;color:#C8944A','TARGET OMZET',L.root);gt.className='mk-a mk-mono';
var br=MK.el('div','left:520px;top:440px;width:220px;height:760px;border:5px solid #F4EBD9;border-bottom:none;transform-origin:bottom;background:rgba(244,235,217,.08)',' ',L.root);br.className='mk-a';
var sl=""" + LF(250, 800, 2) + """;sl.className='mk-a';sl.firstChild.setAttribute('width',200);sl.firstChild.setAttribute('height',400);
L.on(function(t){var g=MK.E.out(MK.pr(t,.3,2.2));br.style.transform='scaleY('+(.15+.85*g)+')';br.style.borderColor=g>.75?'#C8944A':'#F4EBD9';sl.style.transform='translateX('+(Math.sin(t*10)*4)+'px) rotate(8deg)'});
@SUB@""", SUB=sub(20)), tr=True, dolly=.04)
ev(20, 2.0, 'chime')
w21d = W(21, 'diskon', 1.6)
scene(21, R(BP + """
var tg=MK.el('div','left:120px;top:440px;width:520px;height:340px','<svg viewBox="0 0 220 150" width="520" height="340"><path d="M40 10 H210 V140 H40 L6 75Z" fill="#B84A2E" stroke="#F4EBD9" stroke-width="6" stroke-linejoin="round"/><circle cx="38" cy="75" r="10" fill="#101317"/><text x="128" y="70" text-anchor="middle" font-family="Fraunces,serif" font-weight="800" font-size="44" fill="#F4EBD9">DISKON</text><text x="128" y="118" text-anchor="middle" font-family="Fraunces,serif" font-weight="800" font-size="48" fill="#F4EBD9">50%</text></svg>',L.root);tg.className='mk-a';
var jr=MK.el('div','left:620px;top:780px;width:340px;height:420px',LINE(170,210,'<path d="M40 20 h90 v20 q30 20 30 60 v100 h-150 v-100 q0 -40 30 -60z"/><path id="crk" d="M90 70 l-14 30 l20 20 l-16 40" stroke="#B84A2E"/>'),L.root);jr.className='mk-a';jr.firstChild.setAttribute('width',340);jr.firstChild.setAttribute('height',420);
var cs=[];for(var i=0;i<8;i++){var c=MK.el('div','left:0;top:0;width:50px;height:50px',COIN(50),L.root);c.className='mk-a';cs.push(c)}
var lb=MK.el('div','left:120px;top:1180px;width:500px;font-size:44px;color:#D98C7A','margin bocor',L.root);lb.className='mk-a mk-fri';
L.on(function(t){var k=MK.pr(t,@D@-.4,.3);tg.style.opacity=k;tg.style.transform='rotate('+(-8+Math.sin(t*4)*3)+'deg) scale('+(.4+.6*MK.E.over(k))+')';for(var i=0;i<8;i++){var p=((t-@D@-.2)*1.1+i*.12)%1;cs[i].style.transform='translate('+(760+(i%3)*20)+'px,'+(1100+p*300)+'px)';cs[i].style.opacity=t>@D@+.2?(1-p):0}lb.style.opacity=MK.pr(t,@D@+.8,.3)});
@SUB@""", D=w21d, SUB=sub(21)), dolly=.04)
ev(21, w21d - .4, 'stamp'); [ev(21, w21d + .3 + i * .3, 'tick') for i in range(3)]
u22 = F('o22', 'own')
scene(22, R(BP + """
var dk=MK.el('div','left:180px;top:1100px;width:720px;height:24px;border-top:6px solid #F4EBD9',' ',L.root);dk.className='mk-a';
var ow=FIG(L,'@O@',420,720,220,false);ow.style.filter='grayscale(.2)';
var lbl=['chat','followers','omzet'],tl=[];for(var i=0;i<12;i++){var e=MK.el('div','left:'+(220+(i*97)%600)+'px;top:0;width:150px;height:80px',TAIL()+'<div class="mk-mono" style="font-size:22px;color:#D98C7A;margin-top:-6px">'+lbl[i%3]+'</div>',L.root);e.className='mk-a';tl.push(e)}
L.on(function(t){for(var i=0;i<12;i++){var s=.05+i*.16,f=Math.min(1,Math.max(0,(t-s)/.5));tl[i].style.transform='translateY('+(200+f*f*830-Math.floor(i/4)*26)+'px) rotate('+((i*47)%60-30)+'deg)';tl[i].style.opacity=t>s?1:0}HEAD('@O@',-15+Math.sin(t*2)*4);SMILE('@O@',-.4);ARM('@O@','ra',-30);ARM('@O@','la',30)});
@SUB@""", O=u22, SUB=sub(22)), tr=True, dolly=.05)
[ev(22, .05 + i * .32, 'tick') for i in range(5)]
scene(23, R(BP + """
var of=MK.el('div','left:300px;top:900px;width:480px;height:380px',LINE(240,190,'<path d="M10 180 V40 H230 V180 Z M60 80 h40 M140 80 h40 M60 130 h40 M140 130 h40"/>'),L.root);of.className='mk-a';of.firstChild.setAttribute('width',480);of.firstChild.setAttribute('height',380);
var bn=MK.el('div','left:240px;top:330px;width:600px;height:540px','<svg viewBox="0 0 300 270" width="600" height="540"><path d="M10 100 L150 20 L290 100 V260 H10Z" fill="#14100c" stroke="#5a3b24" stroke-width="5"/><rect x="100" y="150" width="100" height="110" fill="#000" stroke="#5a3b24" stroke-width="5"/></svg>',L.root);bn.className='mk-a';
var ey=[];for(var i=0;i<28;i++){var e=MK.el('div','left:'+(350+(i*53)%380)+'px;top:'+(560+(i*31)%260)+'px;width:26px;height:9px','<svg viewBox="0 0 26 9" width="26" height="9"><circle cx="4" cy="4.5" r="4" fill="#F0C77E"/><circle cx="22" cy="4.5" r="4" fill="#F0C77E"/></svg>',L.root);e.className='mk-a';ey.push(e)}
L.on(function(t){var b=MK.pr(t,.2,.7);bn.style.opacity=b;bn.style.transform='translateY('+((1-MK.E.out(b))*80)+'px)';for(var i=0;i<28;i++)ey[i].style.opacity=t>.6+i*.04?(Math.sin(t*3+i)>.92?0:1):0});
@SUB@""", SUB=sub(23)), dolly=.08)
ev(23, .2, 'sweep')
# ===== B4 penutup =====
u24 = F('o24', 'own')
scene(24, R("""DARK(L);GLOW(L,540,900,420,0);
var tb=MK.el('div','left:-20px;top:1120px;width:1120px;height:900px;background:linear-gradient(#5a3b24,#3d2817);border-top:8px solid #0F0E0C',' ',L.root);tb.className='mk-a';
var ow=FIG(L,'@O@',400,700,280,false);var cn=MK.el('div','left:0;top:0;width:70px;height:70px',COIN(70),L.root);cn.className='mk-a';
var pile=MK.el('div','left:120px;top:1080px;width:260px;height:60px',[0,1,2,3,4].map(function(i){return '<div style="position:absolute;left:'+(i*44)+'px;top:'+((i%2)*10)+'px">'+TAIL()+'</div>'}).join(''),L.root);pile.className='mk-a';
L.on(function(t){ARM('@O@','ra',-80+Math.sin(t*2)*8);HEAD('@O@',Math.sin(t*1.3)*8);SMILE('@O@',0);cn.style.transform='translate(620px,'+(840+Math.sin(t*2)*6)+'px) rotateY('+(t*90)+'deg)'});
@SUB@""", O=u24, SUB=sub(24)), tr=True, dolly=.06)
w25t = W(25, 'tikusnya', 1.1)
scene(25, R("""DARK(L);GLOW(L,540,1000,380,0);
var tb=MK.el('div','left:-20px;top:1120px;width:1120px;height:900px;background:linear-gradient(#5a3b24,#3d2817);border-top:8px solid #0F0E0C',' ',L.root);tb.className='mk-a';
var cn=MK.el('div','left:490px;top:1030px;width:100px;height:100px',COIN(100),L.root);cn.className='mk-a';
var rt=MK.el('div','left:180px;top:1040px;width:160px;height:90px',RAT('#8a827a',true),L.root);rt.className='mk-a';var tl=MK.el('div','left:780px;top:1060px;width:160px;height:80px','<div style="transform:scale(1.6);transform-origin:0 0">'+TAIL()+'</div>',L.root);tl.className='mk-a';
var q=MK.el('div','left:96px;top:330px;width:888px;text-align:center;font-size:104px;line-height:1.02;color:#F4EBD9','Tikusnya,<br>atau <span style="color:#D98C7A">ekornya?</span>',L.root);q.className='mk-a mk-fr';L.headline=true;
L.on(function(t){var s=Math.max(0,1-MK.pr(t,0,3.6));cn.style.transform='rotateY('+(t*900*s)+'deg) translateY('+(-Math.abs(Math.sin(t*10))*10*s)+'px)';var k=MK.pr(t,@T@-.2,.4);q.style.opacity=k;q.style.transform='translateY('+((1-MK.E.out(k))*30)+'px)';rt.style.opacity=tl.style.opacity=MK.pr(t,@T@,.4)});""", T=w25t), dolly=.05)
ev(25, 0, 'chime'); ev(25, w25t, 'pop')
html = ('<!DOCTYPE html>\n<html><head><meta charset="utf-8"><title>Fabel Bisnis 01</title><link rel="stylesheet" href="motionkit/fonts-mk.css"></head><body>\n'
        '<script src="motionkit/kit.js"></script>\n<script>\nvar C=MK.C;\nvar FG=' + json.dumps(FIGS) + ';\n' + HELP + FAB + FAB2 + '\nMK.run([\n' + ',\n'.join(S) + '\n]);\n</script>\n</body></html>\n')
open(A + 'mk-fabel01b.html', 'w', encoding='utf-8').write(html)
json.dump({'duration': tl['duration'], 'events': EV, 'cuts': T0}, open(os.path.join(OUT, 'events.json'), 'w'))
print('ok', len(S), 'adegan', round(sum(DUR), 1), 'dtk'); print([(SC[i][0], DUR[i]) for i in range(len(SC))])
