"""Fabel Bisnis #06 Kerudung adem ekor tikus: animasi penuh Motion Kit dari timing.json vo_prep.
Pakai: python3 scratch/gen_metrik.py out/reel17/timing.json -> animatic/mk-fabel03b.html + out/reel17/events.json"""
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
SC = [('pagi',0,0),('kerudung',0,0),('jamu',0,0),('dan',0,0),('yang',0,0),
      ('di',1,0),('market',1,1),('problem',1,0),
      ('di',2,0),('jawabannya',2,0),
      ('kalau',3,0),('kalau',3,0),('psikolog',3,0),('pesan',3,0),('dan',3,0),('kembangkan',3,0),
      ('jadi',4,0),('mau',4,0)]
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
KEY = {'suka','butuh','adem','gerah','habis','teman','market','fit','problemsolution','selera','masalah','strategi','konten','copywriting','keinginannya','amannya','testimoni','promotion','prevention','dipercaya','keduanya','hero','jarang','kembangkan','brandnya','sasaran','motif','jamu','produk'}
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
DROP = set()
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

PAL.update({'t1': ('#6B6560', '#4a4540', '#2a1d14'), 't2': ('#C8944A', '#a57a35', '#2a1d14'), 'ref': ('#0F0E0C', '#2a2622', '#2a1d14')})
FIELD_JS = r"""
function FIELD(L,o){o=o||{};
 var sk=MK.el('div','left:0;top:0;width:1080px;height:1920px;background:linear-gradient(#f2d9a6 0%,#e7b878 35%,#c98f52 62%,#5e7a3c 62.2%,#4a6230 100%)',' ',L.root);sk.className='mk-a';
 var sun=MK.el('div','left:760px;top:250px;width:160px;height:160px;border-radius:50%;background:#fbe7b8;box-shadow:0 0 120px 40px rgba(251,231,184,.5)',' ',L.root);sun.className='mk-a';
 var cr=MK.el('div','left:-40px;top:1050px;width:1160px;height:160px',' ',L.root);cr.className='mk-a';var ch='';for(var i=0;i<26;i++)ch+='<div class="cw" style="position:absolute;left:'+(i*45)+'px;top:'+(20+(i%3)*14)+'px;width:40px;height:90px"><svg viewBox="0 0 40 90" width="40" height="90"><circle cx="20" cy="16" r="13" fill="'+['#3d2817','#5a3b24','#2a1f17'][i%3]+'"/><rect x="6" y="30" width="28" height="60" rx="12" fill="'+['#8f3a24','#3e5a6b','#6B6560','#2f4a3a'][i%4]+'"/></svg></div>';cr.innerHTML=ch;
 var bt=MK.el('div','left:0;top:0;width:1080px;height:300px',' ',L.root);bt.className='mk-a';var bh='<svg viewBox="0 0 1080 300" width="1080" height="300"><path d="M-20 140 Q540 260 1100 140" fill="none" stroke="#3d2817" stroke-width="4"/>';for(var i=0;i<16;i++){var x=i*70,y=140+Math.sin(i/15*Math.PI)*118*.9;bh+='<path d="M'+x+' '+y+' l30 0 l-15 40z" fill="'+(i%2?'#F4EBD9':'#B84A2E')+'" stroke="#3d2817" stroke-width="2"/>'}bt.innerHTML=bh+'</svg>';
 for(var k=0;k<2;k++){var p=MK.el('div','left:'+(k?960:60)+'px;top:500px;width:60px;height:620px','<svg viewBox="0 0 60 620" width="60" height="620"><path d="M10 0 V620" stroke="#3d2817" stroke-width="8"/><path class="uf" d="M14 10 Q40 120 20 260 L50 250 Q70 120 40 10z" fill="#B84A2E"/><path d="M14 260 Q40 360 20 480 L50 470 Q70 360 40 260z" fill="#F4EBD9"/></svg>',L.root);p.className='mk-a'}
 L.on(function(t){var c=cr.querySelectorAll('.cw');for(var i=0;i<c.length;i++)c[i].style.transform='translateY('+(-Math.abs(Math.sin(t*(o.cheer||5)+i*.7))*(o.jump||10))+'px)';bt.style.transform='translateY('+(Math.sin(t*2)*3)+'px)'});}
function ROPE(L,y,getx){var r=MK.el('div','left:-40px;top:'+y+'px;width:1160px;height:24px;border-radius:12px;background:repeating-linear-gradient(60deg,#d9b27a 0 14px,#b98d55 14px 28px);border:3px solid #5a3b24',' ',L.root);r.className='mk-a';
 var rb=MK.el('div','left:0;top:'+(y-30)+'px;width:30px;height:84px;background:#B84A2E;border:3px solid #0F0E0C',' ',L.root);rb.className='mk-a';
 var ln=MK.el('div','left:538px;top:'+(y-80)+'px;width:4px;height:180px;background:#F4EBD9;opacity:.8',' ',L.root);ln.className='mk-a';
 L.on(function(t){var x=getx?getx(t):0;rb.style.transform='translateX('+(525+x)+'px)';r.style.transform='translateX('+x+'px)'});}
function TEAM(L,us,x0,dx,y,w,flip,lean){var vv=us.map(function(u,i){var e=FIG(L,u,x0+i*dx,y,w,flip);return e});
 L.on(function(t){for(var i=0;i<us.length;i++){var l=lean?lean(t,i):0;vv[i].style.transform=(flip?'scaleX(-1) ':'')+'rotate('+l+'deg)';ARM(us[i],'la',-70);ARM(us[i],'ra',-75)}});return vv}
"""
LT_ = "L.headline=true;"
T1 = [F('a%d' % i, 't1') for i in range(10)]
T2 = [F('b%d' % i, 't2', True) for i in range(6)]
def team1(prefix, n=10, y=880, w=130, x0=20, dx=48):
    us = [F('%s%d' % (prefix, i), 't1') for i in range(n)]
    return us

PAL.update({'kardi': ('#6B6560', '#4a4540', '#2a1d14'), 'jono': ('#B84A2E', '#8f3a24', '#2a1d14'), 'cs': ('#2f4a3a', '#22362a', '#2a1d14'),
            'p1': ('#3e5a6b', '#2d4350', '#2a1d14'), 'p2': ('#C8944A', '#a57a35', '#5a4a40'), 'p3': ('#8a5a3a', '#6a442c', '#2a1d14')})
KRISHNA = ('<svg viewBox="0 0 260 360" width="300" height="415"><rect x="40" y="200" width="180" height="170" rx="60" fill="#2f4a3a"/>'
           '<path d="M104 200 L130 246 L156 200Z" fill="#F4EBD9"/>'
           '<path d="M70 120 Q64 60 130 54 Q196 60 190 120 L196 196 Q170 176 172 130 L88 130 Q90 176 64 196Z" fill="#1e1a16"/>'
           '<rect x="112" y="160" width="36" height="40" fill="#C99A74"/><circle cx="130" cy="118" r="56" fill="#C99A74"/>'
           '<path d="M76 104 Q86 62 130 62 Q176 62 184 104 Q160 80 130 84 Q100 80 76 104Z" fill="#1e1a16"/>'
           '<circle cx="110" cy="122" r="5" fill="#0F0E0C"/><circle cx="150" cy="122" r="5" fill="#0F0E0C"/>'
           '<path d="M112 150 Q130 162 148 150" fill="none" stroke="#0F0E0C" stroke-width="4" stroke-linecap="round"/>'
           '<g transform="rotate(-8 200 300)"><rect x="150" y="256" width="96" height="116" rx="6" fill="#C8944A" stroke="#0F0E0C" stroke-width="5"/>'
           '<g fill="none" stroke="#0F0E0C" stroke-width="4"><circle cx="198" cy="292" r="9"/><path d="M180 320 q18 -14 36 0"/><path d="M176 340 h44"/></g></g></svg>')
SATE_JS = r"""
function STREET(L,o){o=o||{};var d=MK.el('div','left:0;top:0;width:1080px;height:1920px;background:linear-gradient(#0d1420 0%,#1a1f2b 45%,#231d18 66%)',' ',L.root);d.className='mk-a';
 for(var i=0;i<24;i++){var s=MK.el('div','left:'+((i*137)%1040+20)+'px;top:'+((i*71)%380+120)+'px;width:4px;height:4px;border-radius:50%;background:#F4EBD9;opacity:'+(.2+(i%4)*.15),' ',L.root);s.className='mk-a';}
 var bh='<svg viewBox="0 0 1200 520" width="1200" height="520">';for(var i=0;i<9;i++){var x=i*140-20,h=220+((i*53)%160);bh+='<rect x="'+x+'" y="'+(520-h)+'" width="128" height="'+h+'" fill="'+(i%2?'#151a24':'#121722')+'"/>';for(var r=0;r<4;r++)for(var c=0;c<3;c++)if((i+r*3+c)%4!=0)bh+='<rect x="'+(x+16+c*38)+'" y="'+(520-h+24+r*48)+'" width="22" height="28" fill="'+((i+r+c)%3?'#2a2f3a':'#C8944A')+'" opacity=".7"/>'}
 bh+='</svg>';var b=MK.el('div','left:-60px;top:'+((o.gy||1100)-520)+'px;width:1200px;height:520px',bh,L.root);b.className='mk-a';
 var sw=MK.el('div','left:0;top:'+(o.gy||1100)+'px;width:1080px;height:90px;background:#3a332c;border-top:6px solid #0F0E0C',' ',L.root);sw.className='mk-a';
 var rd=MK.el('div','left:0;top:'+((o.gy||1100)+90)+'px;width:1080px;height:400px;background:#1c1c1e',' ',L.root);rd.className='mk-a';
 var ds=MK.el('div','left:-200px;top:'+((o.gy||1100)+230)+'px;width:1600px;height:10px;background:repeating-linear-gradient(90deg,#F4EBD9 0 80px,transparent 80px 160px);opacity:.6',' ',L.root);ds.className='mk-a';
 var lm=[];(o.lamps||[160,920]).forEach(function(x){var e=MK.el('div','left:'+(x-140)+'px;top:'+((o.gy||1100)-560)+'px;width:280px;height:560px','<svg viewBox="0 0 280 560" width="280" height="560"><path d="M140 560 V40 q0 -20 30 -20 h30" fill="none" stroke="#0F0E0C" stroke-width="10"/><rect x="186" y="14" width="40" height="18" rx="6" fill="#2A2824"/></svg>',L.root);e.className='mk-a';
  var g=MK.el('div','left:'+(x-60)+'px;top:'+((o.gy||1100)-560)+'px;width:280px;height:280px;border-radius:50%;background:radial-gradient(circle,rgba(251,231,184,.35),rgba(251,231,184,0) 65%)',' ',L.root);g.className='mk-a';lm.push(g)});
 L.on(function(t){ds.style.transform='translateX('+(-(t*(o.speed||0))%160)+'px)';lm.forEach(function(g,i){g.style.opacity=.85+.15*Math.sin(t*7+i*2)})});}
function CART(L,x,y,o){o=o||{};var front=o.front;
 var h='<svg viewBox="0 0 400 330" width="400" height="330" style="overflow:visible">';
 h+='<path d="M20 40 L380 40 L360 0 L40 0Z" fill="'+(o.roof||'#B84A2E')+'" stroke="#0F0E0C" stroke-width="5"/><path d="M60 40 V120 M340 40 V120" stroke="#5a3b24" stroke-width="8"/>';
 h+='<rect x="30" y="120" width="340" height="150" rx="8" fill="#E8D7B5" stroke="#0F0E0C" stroke-width="6"/><rect x="50" y="140" width="300" height="56" fill="'+(o.roof||'#B84A2E')+'"/>';
 h+='<text x="200" y="180" text-anchor="middle" font-family="Fraunces,serif" font-weight="800" font-size="34" fill="#F4EBD9">'+(o.name||'SATE')+'</text>';
 h+='<rect x="60" y="210" width="70" height="44" fill="#F4EBD9" stroke="#0F0E0C" stroke-width="4"/><rect x="150" y="210" width="70" height="44" fill="#F4EBD9" stroke="#0F0E0C" stroke-width="4"/>';
 h+='<circle cx="90" cy="290" r="36" fill="#2A2824" stroke="#0F0E0C" stroke-width="6"/><circle cx="90" cy="290" r="10" fill="#9a9590"/><circle cx="310" cy="290" r="36" fill="#2A2824" stroke="#0F0E0C" stroke-width="6"/><circle cx="310" cy="290" r="10" fill="#9a9590"/></svg>';
 var c=MK.el('div','left:'+x+'px;top:'+y+'px;width:400px;height:330px',h,L.root);c.className='mk-a';
 var gx=front?x+(o.side=='l'?-150:330):x+150, gy=front?y+150:y+40;
 var gl=MK.el('div','left:'+(gx-110)+'px;top:'+(gy-150)+'px;width:440px;height:300px;border-radius:50%;background:radial-gradient(circle,rgba(255,150,60,.55),rgba(255,150,60,0) 65%)',' ',L.root);gl.className='mk-a';
 var gr=MK.el('div','left:'+gx+'px;top:'+gy+'px;width:220px;height:90px','<svg viewBox="0 0 220 90" width="220" height="90" style="overflow:visible"><g class="fl">'+[0,1,2,3,4,5].map(function(i){return '<path d="M'+(20+i*34)+' 30 q10 -40 0 -60 q24 30 12 60z" fill="'+(i%2?'#F0C77E':'#E0703A')+'"/>'}).join('')+'</g><rect x="0" y="30" width="220" height="40" rx="6" fill="#2A2824" stroke="#0F0E0C" stroke-width="5"/>'+[0,1,2,3,4,5,6].map(function(i){return '<path d="M'+(14+i*30)+' 20 v34" stroke="#8a5a3a" stroke-width="4"/><rect x="'+(8+i*30)+'" y="14" width="14" height="22" rx="5" fill="#9a4a22"/>'}).join('')+'<path d="M30 70 L20 90 M190 70 L200 90" stroke="#0F0E0C" stroke-width="6"/></svg>',L.root);gr.className='mk-a';
 if(!front){gr.style.opacity=.0;gl.style.opacity=.15}
 var sm=[];for(var i=0;i<(o.n||16);i++){var e=MK.el('div','left:0;top:0;width:90px;height:90px;border-radius:50%;background:radial-gradient(circle,rgba(220,214,204,.55),rgba(220,214,204,0) 70%)',' ',L.root);e.className='mk-a';sm.push(e)}
 L.on(function(t){var fl=gr.querySelector('.fl');if(fl)fl.setAttribute('transform','translate(0,'+(Math.sin(t*20)*3)+') scale(1,'+(1+.15*Math.sin(t*13))+')');if(front)gl.style.opacity=.75+.25*Math.sin(t*11);
  var on=o.smokeAt==null||t>o.smokeAt;
  for(var i=0;i<sm.length;i++){var p=((t*.45+i/sm.length)%1),e=sm[i];if(!on){e.style.opacity=0;continue}
   if(o.smoke=='in'){var sx=gx+80-p*120,sy=gy-20-p*160;e.style.transform='translate('+(sx)+'px,'+sy+'px) scale('+(.5+p*.6)+')';e.style.opacity=(1-p)*.5}
   else{var dir=o.side=='l'?-1:1;var sx=gx+90+dir*p*(o.reach||520)+Math.sin(i)*40,sy=gy-30-p*120+Math.sin(p*6+i)*30;e.style.transform='translate('+sx+'px,'+sy+'px) scale('+(.7+p*2.2)+')';e.style.opacity=(1-p)*.75}}});
 return {c:c,gr:gr,gl:gl,gx:gx,gy:gy}}
function MOTOR(L,y,o){var h='<svg viewBox="0 0 220 150" width="220" height="150" style="overflow:visible"><circle cx="44" cy="120" r="26" fill="#2A2824" stroke="#0F0E0C" stroke-width="6"/><circle cx="176" cy="120" r="26" fill="#2A2824" stroke="#0F0E0C" stroke-width="6"/><path d="M40 112 L80 70 H150 L186 112 Z" fill="'+(o.c||'#3e5a6b')+'" stroke="#0F0E0C" stroke-width="5"/><path d="M150 70 L170 30 h20" stroke="#0F0E0C" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M90 70 Q96 20 120 10 Q140 20 130 70Z" fill="'+(o.r||'#8a5a3a')+'" stroke="#0F0E0C" stroke-width="4"/><circle cx="118" cy="0" r="18" fill="'+(o.hm||'#F4EBD9')+'" stroke="#0F0E0C" stroke-width="4"/><circle cx="196" cy="96" r="7" fill="#fbe7b8"/></svg>';
 var e=MK.el('div','left:0;top:'+y+'px;width:220px;height:150px',h,L.root);e.className='mk-a';
 L.on(function(t){var k=MK.pr(t,o.at||0,o.d||1.4),x=o.x0+(o.x1-o.x0)*(o.stop?MK.E.out(k):k);e.style.transform='translateX('+x+'px)'+(o.flip?' scaleX(-1)':'');e.style.opacity=t<(o.at||0)?0:1});return e}
function IC(n,s,c){c=c||'#F4EBD9';var P={eye:'<path d="M8 50 Q50 10 92 50 Q50 90 8 50Z"/><circle cx="50" cy="50" r="14" fill="'+c+'"/>',
 nose:'<path d="M50 12 C44 40 30 58 32 70 Q36 82 50 78 Q64 82 68 70 C70 58 56 40 50 12Z"/><path d="M38 72 q4 6 8 2 M62 72 q-4 6 -8 2"/>',
 ear:'<path d="M66 70 Q58 92 42 86 Q34 82 38 70 Q22 60 26 38 Q32 12 58 14 Q80 18 78 42 Q76 58 66 70Z"/><path d="M48 42 Q54 30 62 40 Q64 50 54 54"/>',
 hand:'<path d="M30 92 V48 Q30 40 38 40 Q46 40 46 48 V20 Q46 12 54 12 Q62 12 62 20 V46 Q62 38 70 38 Q78 38 78 46 V70 Q78 92 56 92Z"/>',
 tongue:'<path d="M16 34 Q50 56 84 34"/><path d="M30 42 Q30 86 50 86 Q70 86 70 42"/><path d="M50 50 V72"/>',
 music:'<path d="M36 76 V22 L76 14 V66"/><circle cx="28" cy="78" r="10" fill="'+c+'"/><circle cx="68" cy="68" r="10" fill="'+c+'"/>',
 spark:'<path d="M50 10 L58 42 L90 50 L58 58 L50 90 L42 58 L10 50 L42 42Z"/>',
 clock:'<circle cx="50" cy="50" r="38"/><path d="M50 26 V50 L66 60"/>',
 bag:'<path d="M18 36 H82 L76 90 H24Z"/><path d="M36 36 Q36 12 50 12 Q64 12 64 36"/>',
 pin:'<path d="M50 92 Q20 56 20 38 Q20 10 50 10 Q80 10 80 38 Q80 56 50 92Z"/><circle cx="50" cy="38" r="10"/>',
 scent:'<path d="M22 80 Q34 64 22 48 Q10 32 22 16 M50 80 Q62 64 50 48 Q38 32 50 16 M78 80 Q90 64 78 48 Q66 32 78 16"/>',
 shirt:'<path d="M34 12 L18 22 L8 44 L22 50 L26 40 V90 H74 V40 L78 50 L92 44 L82 22 L66 12 Q50 28 34 12Z"/>'};
 return '<svg viewBox="0 0 100 100" width="'+s+'" height="'+s+'"><g fill="none" stroke="'+c+'" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">'+P[n]+'</g></svg>'}
function ICO(L,n,x,y,s,c,at,o){o=o||{};var e=MK.el('div','left:'+x+'px;top:'+y+'px;width:'+s+'px;height:'+s+'px',IC(n,s,c),L.root);e.className='mk-a';
 L.on(function(t){var k=MK.pr(t,at,.35);e.style.opacity=k>0?(o.out!=null&&t>o.out?Math.max(0,1-(t-o.out)*3):1):0;e.style.transform='scale('+(.4+.6*MK.E.over(k))+') translateY('+(o.float?Math.sin(t*2.4)*6:0)+'px)'});return e}
function LBL(L,x,y,txt,at,o){o=o||{};var e=MK.el('div','left:'+x+'px;top:'+y+'px;padding:10px 22px;border-radius:999px;background:'+(o.bg||'#0F0E0C')+';color:'+(o.c||'#F4EBD9')+';font-size:'+(o.fs||30)+'px;letter-spacing:.05em;white-space:nowrap',txt,L.root);e.className='mk-a mk-mono';
 L.on(function(t){var k=MK.pr(t,at,.3);e.style.opacity=k*(o.out!=null&&t>o.out?Math.max(0,1-(t-o.out)*3):1);e.style.transform='translateY('+((1-MK.E.out(k))*16)+'px)'});return e}
function HL(L,html,at,o){o=o||{};var e=MK.el('div','left:96px;top:'+(o.y||290)+'px;width:888px;font-size:'+(o.fs||92)+'px;line-height:1.02;color:'+(o.c||'#F4EBD9'),html,L.root);e.className='mk-a mk-fr';L.headline=true;
 L.on(function(t){var k=at<=0?1:MK.pr(t,at,.35);e.style.opacity=k*(o.out!=null&&t>o.out?Math.max(0,1-(t-o.out)*3):1);e.style.transform='translateY('+((1-MK.E.out(k))*20)+'px)'});return e}
"""
PAL.update({'dad': ('#2f4a3a', '#22362a', '#2a1d14'), 'own': ('#B84A2E', '#8f3a24', '#2a1d14')})
SELIG = ('<svg viewBox="0 0 260 360" width="300" height="415"><rect x="40" y="200" width="180" height="170" rx="60" fill="#3e5a6b"/>'
         '<path d="M108 200 L130 248 L152 200Z" fill="#FBF8F3"/><path d="M124 206 h12 l-3 40 h-6z" fill="#C8944A"/>'
         '<rect x="112" y="160" width="36" height="40" fill="#F1C9A3"/><circle cx="130" cy="116" r="58" fill="#F1C9A3"/>'
         '<path d="M72 118 Q70 92 84 82 L92 110Z M188 118 Q190 92 176 82 L168 110Z" fill="#E8E1D5"/>'
         '<g fill="none" stroke="#0F0E0C" stroke-width="4"><rect x="94" y="108" width="30" height="22" rx="10"/><rect x="136" y="108" width="30" height="22" rx="10"/><path d="M124 118 h12"/></g>'
         '<path d="M106 150 Q130 168 154 150" fill="none" stroke="#0F0E0C" stroke-width="4" stroke-linecap="round"/>'
         '<g transform="rotate(-8 200 300)"><rect x="150" y="252" width="100" height="118" rx="6" fill="#C8944A" stroke="#0F0E0C" stroke-width="5"/>'
         '<circle cx="200" cy="300" r="24" fill="none" stroke="#0F0E0C" stroke-width="4"/><path d="M190 296 v2 M210 296 v2 M188 308 q12 10 24 0" stroke="#0F0E0C" stroke-width="4" fill="none" stroke-linecap="round"/></g></svg>')
SETANG_JS = r"""
function GANG(L,o){o=o||{};var dusk=o.dusk||0;
 var sk=MK.el('div','left:0;top:0;width:1080px;height:1920px;background:linear-gradient(#f3c98c 0%,#e9a06a 32%,#c9765a 52%,#8a5a4a 62%)',' ',L.root);sk.className='mk-a';
 var sun=MK.el('div','left:620px;top:620px;width:220px;height:220px;border-radius:50%;background:#fbe0a8;box-shadow:0 0 140px 60px rgba(251,224,168,.55)',' ',L.root);sun.className='mk-a';
 var cols=['#E8D7B5','#d9a273','#C8944A','#b9a48c','#d8c3a0','#c88a6a'];
 function row(w,y0,sc,dark){var h='<svg viewBox="0 0 '+w+' 700" width="'+w+'" height="700">';for(var i=0;i*230<w;i++){var x=i*230,hh=260+((i*67)%90),c=cols[(i+(dark?3:0))%cols.length];
  h+='<rect x="'+(x+10)+'" y="'+(560-hh)+'" width="210" height="'+hh+'" fill="'+c+'" stroke="#0F0E0C" stroke-width="5"/><path d="M'+(x-6)+' '+(564-hh)+' L'+(x+115)+' '+(470-hh)+' L'+(x+236)+' '+(564-hh)+'Z" fill="'+(i%2?'#8f3a24':'#5a3b24')+'" stroke="#0F0E0C" stroke-width="5"/>';
  h+='<rect x="'+(x+36)+'" y="'+(600-hh)+'" width="60" height="60" fill="#3a2f26" stroke="#0F0E0C" stroke-width="4"/><rect class="wl" x="'+(x+40)+'" y="'+(604-hh)+'" width="52" height="52" fill="#F0C77E" opacity="'+(dusk?.9:.25)+'"/><rect x="'+(x+130)+'" y="'+(560-150)+'" width="64" height="150" fill="#5a3b24" stroke="#0F0E0C" stroke-width="4"/>';
  h+='<g stroke="#0F0E0C" stroke-width="4" fill="#E8D7B5">'+[0,1,2,3,4,5].map(function(k){return '<rect x="'+(x+8+k*38)+'" y="490" width="14" height="80" rx="3"/>'}).join('')+'<rect x="'+x+'" y="510" width="230" height="10"/></g>';
  if(i%3==1)h+='<path d="M'+(x+115)+' 570 V60" stroke="#3d2817" stroke-width="10"/><path d="M'+(x+75)+' 90 h80" stroke="#3d2817" stroke-width="8"/><path d="M'+(x+115)+' 80 Q'+(x+460)+' 200 '+(x+805)+' 80" fill="none" stroke="#0F0E0C" stroke-width="3"/>';
  if(i%3==0)h+='<path d="M'+(x+20)+' 430 Q'+(x+115)+' 460 '+(x+210)+' 430" fill="none" stroke="#0F0E0C" stroke-width="3"/><g class="jm">'+[0,1,2].map(function(k){return '<rect x="'+(x+50+k*50)+'" y="'+(436+k*4)+'" width="34" height="'+(44+k*8)+'" fill="'+['#B84A2E','#F4EBD9','#3e5a6b'][k]+'" stroke="#0F0E0C" stroke-width="3"/>'}).join('')+'</g>'}
  return h+'</svg>'}
 var W=3000;var far=MK.el('div','left:0;top:'+((o.gy||1200)-700)+'px;width:'+W+'px;height:700px',row(W,0,1,false),L.root);far.className='mk-a';
 var rd=MK.el('div','left:0;top:'+(o.gy||1200)+'px;width:1080px;height:720px;background:linear-gradient(#5a4f46,#2e2823)',' ',L.root);rd.className='mk-a';
 var sh=MK.el('div','left:0;top:'+(o.gy||1200)+'px;width:3000px;height:60px;background:repeating-linear-gradient(100deg,rgba(15,14,12,.18) 0 60px,transparent 60px 230px)',' ',L.root);sh.className='mk-a';
 var cat=MK.el('div','left:0;top:'+((o.gy||1200)-52)+'px;width:110px;height:60px','<svg viewBox="0 0 110 60" width="110" height="60"><path d="M10 40 Q4 10 20 20" stroke="#2a2622" stroke-width="6" fill="none" stroke-linecap="round"/><ellipse cx="50" cy="40" rx="32" ry="16" fill="#2a2622"/><circle cx="86" cy="30" r="14" fill="#2a2622"/><path d="M78 20 l4 -12 l6 10 M90 18 l6 -10 l2 12" fill="#2a2622"/><path d="M34 54 v6 M64 54 v6" stroke="#2a2622" stroke-width="6"/></svg>',L.root);cat.className='mk-a';
 var nt=MK.el('div','left:0;top:0;width:1080px;height:1920px;background:#0b1020;pointer-events:none',' ',L.root);nt.className='mk-a';
 L.on(function(t){var x=(o.scroll?o.scroll(t):0);far.style.transform='translateX('+(-(x%1840))+'px)';sh.style.transform='translateX('+(-(x*1.2%460))+'px)';
  var jm=far.querySelectorAll('.jm');for(var i=0;i<jm.length;i++)jm[i].setAttribute('transform','skewX('+(Math.sin(t*2+i)*4)+')');
  cat.style.transform='translateX('+(((t*70+(o.cat||0))%1400)-200)+'px)';cat.style.opacity=o.nocat?0:1;
  var d=typeof dusk=='function'?dusk(t):dusk;nt.style.opacity=d*.55;sun.style.transform='translateY('+(d*300)+'px)'});}
function BIKE(L,x,y,o){o=o||{};var id='bk'+Math.floor(Math.random()*1e6);
 var sp=function(c){var s='';for(var k=0;k<6;k++)s+='<path d="M'+c+' 200 l'+(Math.cos(k*Math.PI/3)*48).toFixed(1)+' '+(Math.sin(k*Math.PI/3)*48).toFixed(1)+'" stroke="#2a2622" stroke-width="3"/>';return s};
 var h='<svg viewBox="0 0 320 270" width="320" height="270" style="overflow:visible">';
 h+='<g id="'+id+'w1"><circle cx="70" cy="200" r="52" fill="none" stroke="#0F0E0C" stroke-width="10"/>'+sp(70)+'</g><g id="'+id+'w2"><circle cx="250" cy="200" r="52" fill="none" stroke="#0F0E0C" stroke-width="10"/>'+sp(250)+'</g>';
 h+='<path d="M70 200 L130 120 L225 120 L250 200 M130 120 L160 200 L225 120 M160 200 L70 200" fill="none" stroke="#B84A2E" stroke-width="12" stroke-linejoin="round"/><path d="M225 120 L215 78" stroke="#0F0E0C" stroke-width="9"/><path d="M196 74 h40" stroke="#0F0E0C" stroke-width="10" stroke-linecap="round"/><rect x="108" y="102" width="52" height="16" rx="8" fill="#0F0E0C"/><circle cx="160" cy="200" r="14" fill="#2a2622"/>';
 if(!o.empty){h+='<path d="M134 104 L160 200" stroke="#3e5a6b" stroke-width="20" stroke-linecap="round"/><path d="M134 104 L176 210" stroke="#2a2622" stroke-width="0"/>';
  h+='<rect x="118" y="30" width="44" height="78" rx="20" fill="#C8944A" stroke="#0F0E0C" stroke-width="4"/><path d="M150 50 L210 76" stroke="#C8944A" stroke-width="16" stroke-linecap="round"/><circle cx="212" cy="76" r="9" fill="#F1C9A3"/>';
  h+='<circle cx="146" cy="6" r="30" fill="#F1C9A3" stroke="#0F0E0C" stroke-width="3"/><path d="M116 0 Q120 -30 150 -26 Q176 -22 176 4 Q160 -10 138 -8 Q124 -6 116 0Z" fill="#2a1d14"/><circle cx="158" cy="4" r="3.5" fill="#0F0E0C"/><path id="'+id+'m" d="M150 18 Q160 24 168 18" fill="none" stroke="#0F0E0C" stroke-width="3" stroke-linecap="round"/>';
  h+='<path id="'+id+'hr" d="M118 -6 q-20 4 -34 -2" stroke="#2a1d14" stroke-width="6" fill="none" stroke-linecap="round" opacity="0"/>'}
 h+='</svg>';var e=MK.el('div','left:'+x+'px;top:'+y+'px;width:320px;height:270px;transform-origin:160px 250px',h,L.root);e.className='mk-a';
 return {e:e,set:function(tilt,ang,dx,smile,hair){e.style.transform='translateX('+(dx||0)+'px) rotate('+tilt+'deg)';var a=document.getElementById(id+'w1'),b=document.getElementById(id+'w2');if(a)a.setAttribute('transform','rotate('+ang+' 70 200)');if(b)b.setAttribute('transform','rotate('+ang+' 250 200)');
  var m=document.getElementById(id+'m');if(m&&smile!=null)m.setAttribute('d',smile>0?'M150 16 Q160 '+(18+smile*10)+' 168 16':'M150 20 Q160 '+(20+smile*6)+' 168 20');var hr=document.getElementById(id+'hr');if(hr)hr.setAttribute('opacity',hair?1:0)}}}
function HAND(sz,c){c=c||'#F1C9A3';return '<svg viewBox="0 0 220 200" width="'+sz+'" height="'+(sz*200/220)+'" style="overflow:visible"><path d="M60 -40 L84 60 L150 60 L170 -40Z" fill="#2f4a3a" stroke="#0F0E0C" stroke-width="5"/><path d="M50 60 Q46 40 70 40 L160 40 Q190 40 186 70 L184 150 Q182 176 156 176 L80 176 Q50 176 50 150Z" fill="'+c+'" stroke="#0F0E0C" stroke-width="5"/>'+[0,1,2,3].map(function(i){return '<path d="M'+(70+i*28)+' 176 Q'+(70+i*28)+' 196 '+(84+i*28)+' 196 Q'+(98+i*28)+' 196 '+(98+i*28)+' 176" fill="'+c+'" stroke="#0F0E0C" stroke-width="5"/>'}).join('')+'<path d="M50 100 Q20 110 30 140 Q40 160 70 150" fill="'+c+'" stroke="#0F0E0C" stroke-width="5"/></svg>'}
function GRIP(L,x,y,w,lab,at,o){o=o||{};var e=MK.el('div','left:'+x+'px;top:'+y+'px;width:'+w+'px;height:260px','<div style="position:absolute;left:0;top:150px;width:'+w+'px;height:44px;border-radius:22px;background:#2a2622;border:5px solid #0F0E0C"></div><div style="position:absolute;left:'+(w/2-110)+'px;top:40px">'+HAND(220)+'</div>'+(lab?'<div class="mk-mono" style="position:absolute;left:0;top:220px;width:'+w+'px;text-align:center;font-size:28px;color:'+(o.c||'#F4EBD9')+';letter-spacing:.08em">'+lab+'</div>':''),L.root);e.className='mk-a';
 L.on(function(t){var k=MK.pr(t,at,.4);e.style.opacity=k>0?1:0;e.style.transform='translateY('+((1-MK.E.over(k))*-160)+'px)'});return e}
"""
PAL.update({'ratna': ('#B84A2E', '#8f3a24', '#2a1d14'), 'b1': ('#3e5a6b', '#2d4350', '#2a1d14'), 'b2': ('#2f4a3a', '#22362a', '#2a1d14'), 'b3': ('#C8944A', '#a57a35', '#2a1d14')})
HIGG = ('<svg viewBox="0 0 260 360" width="300" height="415"><rect x="40" y="200" width="180" height="170" rx="60" fill="#2A2824"/>'
        '<path d="M106 200 L130 250 L154 200Z" fill="#FBF8F3"/><path d="M124 206 h12 l-3 40 h-6z" fill="#B84A2E"/>'
        '<rect x="112" y="160" width="36" height="40" fill="#F1C9A3"/><circle cx="130" cy="116" r="58" fill="#F1C9A3"/>'
        '<path d="M72 108 Q74 56 130 54 Q186 56 188 108 Q176 76 150 74 Q130 86 110 76 Q86 80 72 108Z" fill="#9a9590"/>'
        '<g fill="none" stroke="#0F0E0C" stroke-width="4"><rect x="94" y="108" width="30" height="22" rx="4"/><rect x="136" y="108" width="30" height="22" rx="4"/><path d="M124 118 h12"/></g>'
        '<path d="M110 150 Q130 162 150 150" fill="none" stroke="#0F0E0C" stroke-width="4" stroke-linecap="round"/>'
        '<g transform="rotate(-8 200 300)"><rect x="150" y="252" width="100" height="118" rx="6" fill="#C8944A" stroke="#0F0E0C" stroke-width="5"/>'
        '<path d="M174 300 l12 -16 l12 16 M210 284 v28 l-10 -8 M210 312 l10 -8" stroke="#0F0E0C" stroke-width="4" fill="none" stroke-linecap="round"/></g></svg>')
PASAR_JS = r"""
function PASAR(L,o){o=o||{};
 var sk=MK.el('div','left:0;top:0;width:1080px;height:1920px;background:linear-gradient(#f6e7c8 0%,#efd3a0 40%,#d9b27a 60%)',' ',L.root);sk.className='mk-a';
 var sun=MK.el('div','left:120px;top:240px;width:150px;height:150px;border-radius:50%;background:#fbf1d6;box-shadow:0 0 120px 50px rgba(251,241,214,.7)',' ',L.root);sun.className='mk-a';
 var bh='<svg viewBox="0 0 2200 520" width="2200" height="520">';for(var i=0;i<10;i++){var x=i*220;var c=i%2?'#B84A2E':'#3e5a6b';
  bh+='<rect x="'+(x+20)+'" y="240" width="180" height="280" fill="#8a6a4a" stroke="#0F0E0C" stroke-width="4"/>';
  bh+='<path d="M'+x+' 240 L'+(x+110)+' 160 L'+(x+220)+' 240Z" fill="'+c+'" stroke="#0F0E0C" stroke-width="4"/>'+[0,1,2,3].map(function(k){return '<path d="M'+(x+k*55)+' 240 q27 26 55 0" fill="'+(k%2?'#F4EBD9':c)+'" stroke="#0F0E0C" stroke-width="3"/>'}).join('');
  bh+='<rect x="'+(x+40)+'" y="380" width="60" height="44" fill="#C8944A" stroke="#0F0E0C" stroke-width="3"/><rect x="'+(x+110)+'" y="392" width="70" height="32" fill="#2f4a3a" stroke="#0F0E0C" stroke-width="3"/><circle cx="'+(x+150)+'" cy="300" r="14" fill="#6f9a5a" stroke="#0F0E0C" stroke-width="3"/>'}
 bh+='</svg>';var b=MK.el('div','left:0;top:'+((o.gy||1180)-520)+'px;width:2200px;height:520px',bh,L.root);b.className='mk-a';
 var gr=MK.el('div','left:0;top:'+(o.gy||1180)+'px;width:1080px;height:740px;background:linear-gradient(#7d6650,#4a3b2e)',' ',L.root);gr.className='mk-a';
 var bt=MK.el('div','left:0;top:120px;width:1080px;height:120px','<svg viewBox="0 0 1080 120" width="1080" height="120"><path d="M-10 30 Q540 120 1090 30" fill="none" stroke="#3d2817" stroke-width="4"/>'+Array.apply(null,Array(14)).map(function(_,i){var x=40+i*75,y=30+Math.sin(i/13*Math.PI)*42;return '<path d="M'+x+' '+y+' l18 34 l18 -34z" fill="'+['#B84A2E','#F4EBD9','#C8944A'][i%3]+'" stroke="#0F0E0C" stroke-width="2"/>'}).join('')+'</svg>',L.root);bt.className='mk-a';
 L.on(function(t){b.style.transform='translateX('+(-(t*(o.speed||8))%440)+'px)';bt.style.transform='translateY('+(Math.sin(t*2)*3)+'px)'});}
function KRD(c,pat,sz){sz=sz||200;var id='p'+Math.floor(Math.random()*1e6);var p=pat?'<defs><pattern id="'+id+'" width="26" height="26" patternUnits="userSpaceOnUse"><rect width="26" height="26" fill="'+c+'"/><circle cx="13" cy="13" r="5" fill="#F4EBD9"/><path d="M0 0 l26 26" stroke="#0F0E0C" stroke-width="1.5" opacity=".3"/></pattern></defs>':'';
 return '<svg viewBox="0 0 200 240" width="'+sz+'" height="'+(sz*1.2)+'" style="overflow:visible">'+p+'<path d="M100 6 V24" stroke="#0F0E0C" stroke-width="5"/><path d="M60 30 Q100 6 140 30" fill="none" stroke="#0F0E0C" stroke-width="6"/><path d="M100 30 Q30 40 26 120 Q20 200 10 236 L190 236 Q180 200 174 120 Q170 40 100 30Z" fill="'+(pat?'url(#'+id+')':c)+'" stroke="#0F0E0C" stroke-width="5"/><ellipse cx="100" cy="104" rx="38" ry="46" fill="#F4EBD9" stroke="#0F0E0C" stroke-width="4"/></svg>'}
function JAMU(sz){sz=sz||140;return '<svg viewBox="0 0 120 220" width="'+sz+'" height="'+(sz*220/120)+'"><rect x="44" y="6" width="32" height="26" rx="4" fill="#5a3b24" stroke="#0F0E0C" stroke-width="4"/><path d="M40 32 h40 v20 Q104 62 104 100 V200 Q104 214 90 214 H30 Q16 214 16 200 V100 Q16 62 40 52Z" fill="#C8944A" stroke="#0F0E0C" stroke-width="5"/><rect x="24" y="110" width="72" height="60" rx="6" fill="#F4EBD9" stroke="#0F0E0C" stroke-width="4"/><path d="M60 158 Q40 140 52 122 Q66 130 60 158Z M60 158 Q78 142 72 122" fill="#6f9a5a" stroke="#0F0E0C" stroke-width="3"/></svg>'}
function PROD(L,kind,x,y,sz,at,o){o=o||{};var h=kind=='motif'?KRD('#B84A2E',true,sz):kind=='adem'?KRD('#7FA9BC',false,sz):JAMU(sz*.7);
 var e=MK.el('div','left:'+x+'px;top:'+y+'px;width:'+sz+'px;height:'+(sz*1.3)+'px',h,L.root);e.className='mk-a';
 if(kind=='adem'){var w=MK.el('div','left:'+(x-40)+'px;top:'+(y+40)+'px;width:'+(sz+80)+'px;height:'+sz+'px','<svg viewBox="0 0 280 200" width="'+(sz+80)+'" height="'+sz+'"><g fill="none" stroke="#7FA9BC" stroke-width="6" stroke-linecap="round"><path class="w1" d="M10 40 q30 -16 60 0"/><path class="w2" d="M200 90 q30 -16 60 0"/><path class="w3" d="M20 150 q30 -16 60 0"/></g></svg>',L.root);w.className='mk-a';o.wind=w}
 L.on(function(t){var k=MK.pr(t,at,.4);e.style.opacity=k>0?1:0;e.style.transform='translateY('+((1-MK.E.over(k))*60)+'px) rotate('+(Math.sin(t*2+x)*(o.sway||2))+'deg)';if(o.wind){o.wind.style.opacity=k>0?(.6+.4*Math.sin(t*4)):0;o.wind.style.transform='translateX('+(Math.sin(t*3)*10)+'px)'}});return e}
function VENN(L,y,o){o=o||{};var a=MK.el('div','left:120px;top:'+y+'px;width:540px;height:540px;border-radius:50%;border:6px solid #F0C77E;background:rgba(240,199,126,.12)',' ',L.root);a.className='mk-a';
 var b=MK.el('div','left:420px;top:'+y+'px;width:540px;height:540px;border-radius:50%;border:6px solid #7FA9BC;background:rgba(127,169,188,.12)',' ',L.root);b.className='mk-a';
 var la=MK.el('div','left:150px;top:'+(y+230)+'px;width:260px;text-align:center;font-size:34px;color:#F0C77E;line-height:1.1','MARKET<br>FIT',L.root);la.className='mk-a mk-fr';
 var lb=MK.el('div','left:670px;top:'+(y+230)+'px;width:260px;text-align:center;font-size:34px;color:#7FA9BC;line-height:1.1','PROBLEM-<br>SOLUTION FIT',L.root);lb.className='mk-a mk-fr';
 var hz=MK.el('div','left:420px;top:'+(y+170)+'px;width:240px;height:200px;text-align:center;color:#F4EBD9;font-size:40px;line-height:1.1;padding-top:40px;box-sizing:border-box','★<br>HERO',L.root);hz.className='mk-a mk-fr';
 L.on(function(t){var ka=MK.E.over(MK.pr(t,o.a||0,.5)),kb=MK.E.over(MK.pr(t,o.b||0,.5));a.style.transform='scale('+ka+')';la.style.opacity=ka;b.style.transform='scale('+kb+')';lb.style.opacity=kb;
  var h=o.h==null?0:MK.pr(t,o.h,.4);hz.style.opacity=h;hz.style.transform='scale('+(.6+.4*MK.E.over(h)+.04*Math.sin(t*5)*h)+')';hz.style.textShadow=h>0?'0 0 30px rgba(240,199,126,.9)':'none'});}
"""
def ST(t, c='#C8944A'): return t.replace('*', '<span style="color:%s">' % c, 1).replace('*', '</span>', 1)
# 0 HOOK: lapak dengan 3 produk; hasil akhir: satu habis duluan
ur0 = F('r0', 'ratna')
scene(0, R("""PASAR(L,{});
var tb=MK.el('div','left:80px;top:1010px;width:920px;height:200px;background:#8a5a3a;border:6px solid #0F0E0C;border-radius:10px',' ',L.root);tb.className='mk-a';
var r=FIG(L,'@R@',440,700,170,false);
PROD(L,'motif',120,780,190,.1);PROD(L,'jamu',470,820,150,.3);PROD(L,'adem',730,780,190,.5);
var tg=MK.el('div','left:740px;top:700px;padding:8px 18px;background:#B84A2E;color:#F4EBD9;border:4px solid #0F0E0C;border-radius:8px;font-size:30px;transform:rotate(6deg)','HABIS!',L.root);tg.className='mk-a mk-fr';
HL(L,@H@,0,{y:300,c:'#0F0E0C',fs:84});
L.on(function(t){SMILE('@R@',.8);ARM('@R@','ra',-30+Math.sin(t*4)*12);var k=MK.pr(t,1.8,.2);tg.style.opacity=k;tg.style.transform='rotate(6deg) scale('+(1.5-.5*k)+')'});
@SUB@""", R=ur0, H=json.dumps(ST('Disukai. Dibutuhkan.<br>*Atau dua-duanya.*', '#B84A2E')), SUB=sub(0)), dolly=.03)
ev(0, 1.8, 'stamp')
# 1 kerudung motif: laku karena suka (hati)
ub1 = [F('k1%d' % i, ['b1', 'b2', 'b3'][i]) for i in range(3)]
w1s = W(1, 'suka', 2.9)
scene(1, R("""PASAR(L,{});
var p=PROD(L,'motif',380,520,320,.1,{sway:4});
var U=@U@;var v=U.map(function(u,i){return FIG(L,u,60+i*360,880,160,i==2)});
var hs=[];for(var i=0;i<6;i++){var e=MK.el('div','left:'+(300+i*80)+'px;top:500px;font-size:64px;color:#B84A2E','♥',L.root);e.className='mk-a';hs.push(e)}
LBL(L,96,300,'LAKU KARENA PEMBELI SUKA',@S@-.3,{bg:'#B84A2E',fs:32});
L.on(function(t){for(var i=0;i<3;i++){SMILE(U[i],.9);HEAD(U[i],Math.sin(t*3+i)*10);ARM(U[i],i==2?'la':'ra',-60+Math.sin(t*5+i)*20)}
 for(var i=0;i<6;i++){var p2=((t*.6+i/6)%1);hs[i].style.transform='translateY('+(-p2*260)+'px)';hs[i].style.opacity=t>.6?(1-p2):0}});
@SUB@""", U=json.dumps(ub1), S=w1s, SUB=sub(1)), tr=True, dolly=.04)
# 2 jamu: laku karena butuh (pegal)
ub2 = F('k2', 'b1')
w2b = W(2, 'butuh', 3.0)
scene(2, R("""PASAR(L,{});
var p=PROD(L,'jamu',600,560,300,.1,{sway:1});
var u=FIG(L,'@U@',220,760,220,false);
var pg=MK.el('div','left:170px;top:700px;width:240px;height:120px','<svg viewBox="0 0 240 120" width="240" height="120"><g stroke="#B84A2E" stroke-width="7" stroke-linecap="round"><path d="M40 60 l-30 -20 M40 70 l-34 6 M200 60 l30 -20 M200 70 l34 6"/></g></svg>',L.root);pg.className='mk-a';
LBL(L,96,300,'LAKU KARENA PEMBELI BUTUH',@B@-.3,{bg:'#3e5a6b',fs:32});
var pl=MK.el('div','left:640px;top:420px;font-size:120px;color:#6f9a5a','✚',L.root);pl.className='mk-a mk-fr';
L.on(function(t){SMILE('@U@',t<@B@?-.6:.4);ARM('@U@','la',-140);ARM('@U@','ra',-150);HEAD('@U@',8+Math.sin(t*6)*3);pg.style.opacity=t<@B@?(.5+.5*Math.sin(t*10)):0;pl.style.opacity=MK.pr(t,@B@,.3)});
@SUB@""", U=ub2, B=w2b, SUB=sub(2)), tr=True, dolly=.04)
# 3 kerudung adem: cantik + gak gerah
w3g, w3c, w3m = W(3, 'gak', 1.4), W(3, 'cantik', 3.6), W(3, 'masalah', 6.1)
scene(3, R("""PASAR(L,{});
var a=PROD(L,'adem',380,480,320,.1,{sway:3});
var th=MK.el('div','left:120px;top:560px;width:120px;height:360px','<svg viewBox="0 0 120 360" width="120" height="360"><rect x="40" y="10" width="40" height="280" rx="20" fill="#F4EBD9" stroke="#0F0E0C" stroke-width="5"/><circle cx="60" cy="310" r="40" fill="#7FA9BC" stroke="#0F0E0C" stroke-width="5"/><rect id="th3" x="50" y="200" width="20" height="100" fill="#7FA9BC"/></svg>',L.root);th.className='mk-a';
var b1=LBL(L,700,620,'♥ CANTIK',@C@,{bg:'#B84A2E',fs:36});var b2=LBL(L,700,720,'✚ GAK GERAH',@M@,{bg:'#3e5a6b',fs:36});
LBL(L,96,300,'SATU PRODUK, DUA ALASAN',.2,{bg:'#0F0E0C',fs:32});
L.on(function(t){var r=$('th3');if(r){var h=60+40*Math.sin(t*1.5);r.setAttribute('y',300-h);r.setAttribute('height',h)}th.style.opacity=MK.pr(t,@G@-.2,.3)});
@SUB@""", G=w3g, C=w3c, M=w3m, SUB=sub(3)), tr=True, dolly=.04)
ev(3, w3c, 'pop'); ev(3, w3m, 'pop')
# 4 habis duluan + balik bawa teman
ub4 = [F('h4%d' % i, ['b2', 'b3', 'b1'][i], True) for i in range(3)]
w4b = W(4, 'pembelinya', 2.3)
scene(4, R("""PASAR(L,{});
var n=MK.el('div','left:96px;top:300px;font-size:150px;color:#0F0E0C;line-height:1','10',L.root);n.className='mk-a mk-fr';var nl=LBL(L,100,470,'STOK KERUDUNG ADEM',.1,{fs:28});
var hb=MK.el('div','left:440px;top:340px;padding:12px 30px;border:8px solid #B84A2E;border-radius:12px;color:#B84A2E;font-size:84px;transform:rotate(-6deg)','HABIS',L.root);hb.className='mk-a mk-fr';
var U=@U@;var v=U.map(function(u,i){return FIG(L,u,0,860,170,true)});
L.on(function(t){var c=Math.max(0,10-Math.floor(t*5));n.textContent=c;var k=MK.pr(t,2.1,.2);hb.style.opacity=k;hb.style.transform='rotate(-6deg) scale('+(1.5-.5*k)+')';
 for(var i=0;i<3;i++){var s=@B@+i*.35;var p=MK.E.out(MK.pr(t,s,1.6));v[i].style.opacity=t>s?1:0;v[i].style.transform='scaleX(-1) translateX('+(-(1200-p*(820-i*240)))+'px)';WALK(U[i],t,p<1);SMILE(U[i],.8)}});
@SUB@""", U=json.dumps(ub4), B=w4b, SUB=sub(4)), tr=True, dolly=.03)
ev(4, 2.1, 'stamp')
# 5 POROS: dua lingkaran
w5m, w5p = W(5, 'market', 2.2), W(5, 'problemsolution', 3.2)
scene(5, R("""DARK(L,{bg:'#080706'});
var sp=MK.el('div','left:190px;top:0;width:700px;height:1500px;background:linear-gradient(rgba(244,235,217,.12),rgba(244,235,217,0));clip-path:polygon(40% 0,60% 0,100% 100%,0 100%)',' ',L.root);sp.className='mk-a';
LBL(L,96,300,'DI DUNIA BISNIS',.2,{bg:'transparent',c:'#9a9590'});VENN(L,620,{a:@M@-.2,b:@P@-.2});
@SUB@""", M=w5m, P=w5p, SUB=sub(5)), tr=True, dolly=.03)
ev(5, w5m - .2, 'pop'); ev(5, w5p - .2, 'pop')
# 6 definisi market fit
scene(6, R("""DARK(L);
var c=MK.el('div','left:96px;top:520px;width:888px;padding:40px;background:#F4EBD9;border:6px solid #0F0E0C;border-radius:24px;box-sizing:border-box','<div class="mk-mono" style="font-size:28px;color:#B84A2E">MARKET FIT</div><div class="mk-fr" style="font-size:66px;line-height:1.05;margin-top:14px">Cocok dengan<br><span style="color:#B84A2E">selera pasarnya.</span></div><div class="mk-ou" style="font-size:34px;color:#6B6560;margin-top:16px">Orang beli karena suka.</div>',L.root);c.className='mk-a';
var p=PROD(L,'motif',720,300,190,.4,{sway:3});
L.on(function(t){var k=MK.E.over(MK.pr(t,.1,.4));c.style.opacity=k>0?1:0;c.style.transform='rotate(-1.5deg) scale('+(.8+.2*k)+')'});
@SUB@""", SUB=sub(6)), tr=True, dolly=.03)
# 7 definisi problem-solution fit
scene(7, R("""DARK(L);
var c=MK.el('div','left:96px;top:520px;width:888px;padding:40px;background:#F4EBD9;border:6px solid #0F0E0C;border-radius:24px;box-sizing:border-box','<div class="mk-mono" style="font-size:28px;color:#3e5a6b">PROBLEM-SOLUTION FIT</div><div class="mk-fr" style="font-size:66px;line-height:1.05;margin-top:14px">Menyelesaikan<br><span style="color:#3e5a6b">masalah pembelinya.</span></div><div class="mk-ou" style="font-size:34px;color:#6B6560;margin-top:16px">Orang beli karena butuh.</div>',L.root);c.className='mk-a';
var p=PROD(L,'jamu',760,250,190,.4,{sway:1});
L.on(function(t){var k=MK.E.over(MK.pr(t,.1,.4));c.style.opacity=k>0?1:0;c.style.transform='rotate(1.5deg) scale('+(.8+.2*k)+')'});
@SUB@""", SUB=sub(7)), tr=True, dolly=.03)
# 8 kesaksian: dua pertanyaan strategi
w8p, w8a = W(8, 'produk', 4.5), W(8, 'atau', 6.7)
scene(8, R(BP + """
var st=MK.el('div','left:96px;top:300px;padding:16px 28px;border:6px solid #C8944A;border-radius:12px;color:#C8944A;font-size:40px;transform:rotate(-3deg)','DARI BISNIS YANG SAYA DAMPINGI',L.root);st.className='mk-a mk-fr';
var Q=[['Sudah fit dengan marketnya?','#F0C77E',@P@],['Sudah jadi solusi masalah target marketnya?','#7FA9BC',@A@]];
for(var i=0;i<2;i++){var e=MK.el('div','left:96px;top:'+(560+i*280)+'px;width:888px;height:230px;border:5px solid '+Q[i][1]+';border-radius:22px;display:flex;align-items:center;gap:30px;padding:0 36px;box-sizing:border-box','<div style="width:80px;height:80px;border:6px solid '+Q[i][1]+';border-radius:14px;flex:none"></div><div class="mk-fr" style="font-size:50px;color:#F4EBD9;line-height:1.1">'+Q[i][0]+'</div>',L.root);e.className='mk-a';
 (function(e,a){L.on(function(t){var k=MK.pr(t,a-.2,.35);e.style.opacity=k;e.style.transform='translateX('+((1-MK.E.out(k))*-100)+'px)'})})(e,Q[i][2])}
L.on(function(t){var k=MK.pr(t,.1,.25);st.style.opacity=k;st.style.transform='rotate(-3deg) scale('+(1.3-.3*MK.E.out(k))+')'});
@SUB@""", P=w8p, A=w8a, SUB=sub(8)), tr=True, dolly=.03)
ev(8, .1, 'stamp'); ev(8, w8p - .2, 'pop'); ev(8, w8a - .2, 'pop')
# 9 jawaban -> konten & copywriting
w9k, w9c = W(9, 'konten', 0.9), W(9, 'copywriting', 1.3)
scene(9, R(BP + """
var a=MK.el('div','left:390px;top:400px;width:300px;padding:24px;text-align:center;border-radius:999px;background:#F4EBD9;font-size:40px','JAWABANNYA',L.root);a.className='mk-a mk-fr';
var ar=MK.el('div','left:240px;top:520px;width:600px;height:240px','<svg viewBox="0 0 600 240" width="600" height="240"><g fill="none" stroke="#C8944A" stroke-width="8" stroke-linecap="round"><path d="M300 10 Q300 120 90 220"/><path d="M300 10 Q300 120 510 220"/></g></svg>',L.root);ar.className='mk-a';
var k=MK.el('div','left:80px;top:780px;width:420px;height:440px;background:#F4EBD9;border:5px solid #0F0E0C;border-radius:20px;padding:26px;box-sizing:border-box','<div class="mk-mono" style="font-size:26px;color:#B84A2E">KONTEN</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:20px"><div style="height:140px;background:#C8944A"></div><div style="height:140px;background:#7FA9BC"></div><div style="height:140px;background:#B84A2E"></div><div style="height:140px;background:#E8E1D5"></div></div>',L.root);k.className='mk-a';
var c=MK.el('div','left:580px;top:780px;width:420px;height:440px;background:#F4EBD9;border:5px solid #0F0E0C;border-radius:20px;padding:26px;box-sizing:border-box','<div class="mk-mono" style="font-size:26px;color:#B84A2E">COPYWRITING</div><div class="mk-ca" style="font-size:44px;line-height:1.15;margin-top:20px">"Cantik dari pagi sampai sore, tanpa gerah."</div>',L.root);c.className='mk-a';
L.on(function(t){ar.style.clipPath='inset(0 0 '+(100-100*MK.pr(t,.2,.6))+'% 0)';[k,c].forEach(function(e,i){var q=MK.E.over(MK.pr(t,[@K@,@C@][i]-.2,.35));e.style.opacity=q>0?1:0;e.style.transform='scale('+(.7+.3*q)+')'})});
@SUB@""", K=w9k, C=w9c, SUB=sub(9)), tr=True, dolly=.03)
# 10 market fit -> jual keinginan (feed lookbook)
w10t = W(10, 'tunjukkan', 3.3)
scene(10, R(BP + """
LBL(L,96,300,'MARKET FIT → JUAL KEINGINAN',.1,{bg:'#F0C77E',c:'#0F0E0C',fs:30});
var ph=MK.el('div','left:240px;top:400px;width:600px;height:960px;border:8px solid #F4EBD9;border-radius:56px;background:#FBF8F3;overflow:hidden',' ',L.root);ph.className='mk-a';
var tl=[];var cl=['#B84A2E','#C8944A','#3e5a6b','#2f4a3a','#7FA9BC','#B84A2E'];for(var i=0;i<6;i++){var e=MK.el('div','left:'+(268+(i%2)*276)+'px;top:'+(470+Math.floor(i/2)*290)+'px;width:260px;height:270px;border-radius:14px;background:#E8E1D5;overflow:hidden','<div style="margin:20px auto 0;width:150px">'+KRD(cl[i],i%2==0,150)+'</div>',L.root);e.className='mk-a';tl.push(e)}
var hs=[];for(var i=0;i<5;i++){var e=MK.el('div','left:'+(820+(i%2)*40)+'px;top:1200px;font-size:70px;color:#B84A2E','♥',L.root);e.className='mk-a';hs.push(e)}
L.on(function(t){for(var i=0;i<6;i++){var k=MK.E.out(MK.pr(t,@T@-.4+i*.15,.4));tl[i].style.opacity=k;tl[i].style.transform='scale('+(.6+.4*k)+')'}
 for(var i=0;i<5;i++){var p=((t*.7+i/5)%1);hs[i].style.transform='translate('+(Math.sin(p*6+i)*30)+'px,'+(-p*500)+'px)';hs[i].style.opacity=t>@T@?(1-p):0}});
@SUB@""", T=w10t, SUB=sub(10)), tr=True, dolly=.03)
# 11 problem-solution -> jual rasa aman (masalah, bukti, testimoni)
w11m, w11b, w11t = W(11, 'masalahnya', 3.6), W(11, 'bukti', 4.6), W(11, 'testimoni', 6.0)
scene(11, R(BP + """
LBL(L,96,300,'PROBLEM-SOLUTION FIT → JUAL RASA AMAN',.1,{bg:'#7FA9BC',c:'#0F0E0C',fs:28});
var sh=MK.el('div','left:390px;top:400px;width:300px;height:340px','<svg viewBox="0 0 300 340" width="300" height="340"><path d="M150 10 L280 60 V160 Q280 270 150 330 Q20 270 20 160 V60Z" fill="#3e5a6b" stroke="#F4EBD9" stroke-width="8"/><path d="M95 170 l40 40 l80 -90" fill="none" stroke="#F4EBD9" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/></svg>',L.root);sh.className='mk-a';
var C=[['MASALAH','"Pegal, takut obat kimia"',@M@],['BUKTI HASIL','sebelum → sesudah',@B@],['TESTIMONI','★★★★★',@T@]];
for(var i=0;i<3;i++){var e=MK.el('div','left:'+(60+i*330)+'px;top:820px;width:300px;height:300px;background:#F4EBD9;border:5px solid #0F0E0C;border-radius:18px;padding:22px;box-sizing:border-box','<div class="mk-mono" style="font-size:24px;color:#3e5a6b">'+C[i][0]+'</div><div class="mk-fr" style="font-size:'+(i==2?54:36)+'px;margin-top:30px;line-height:1.15;color:'+(i==2?'#C8944A':'#0F0E0C')+'">'+C[i][1]+'</div>',L.root);e.className='mk-a';
 (function(e,a){L.on(function(t){var k=MK.E.over(MK.pr(t,a-.2,.35));e.style.opacity=k>0?1:0;e.style.transform='translateY('+((1-k)*80)+'px)'})})(e,C[i][2])}
L.on(function(t){var k=MK.E.over(MK.pr(t,.4,.5));sh.style.transform='scale('+k+')';sh.style.opacity=k>0?1:0});
@SUB@""", M=w11m, B=w11b, T=w11t, SUB=sub(11)), tr=True, dolly=.03)
[ev(11, x - .2, 'pop') for x in (w11m, w11b, w11t)]
# 12 kartu tokoh Higgins + promotion / prevention
w12p, w12v = W(12, 'promotion', 2.0), W(12, 'prevention', 3.6)
scene(12, R("""DARK(L,{bg:'#080706'});
var sp=MK.el('div','left:190px;top:0;width:700px;height:1500px;background:linear-gradient(rgba(244,235,217,.14),rgba(244,235,217,0));clip-path:polygon(40% 0,60% 0,100% 100%,0 100%)',' ',L.root);sp.className='mk-a';
var fr=MK.el('div','left:146px;top:300px;width:788px;height:700px;border-radius:24px;background:#F4EBD9;border:6px solid #0F0E0C',' ',L.root);fr.className='mk-a';
var tg=MK.el('div','left:190px;top:336px;font-size:26px;letter-spacing:.1em;color:#B84A2E','KARTU TOKOH',L.root);tg.className='mk-a mk-mono';
var pt=MK.el('div','left:390px;top:350px;width:300px;height:415px',@G@,L.root);pt.className='mk-a';
var nm=MK.el('div','left:146px;top:790px;width:788px;text-align:center;font-size:58px;line-height:1;color:#0F0E0C','E. TORY HIGGINS',L.root);nm.className='mk-a mk-fr';
var s1=MK.el('div','left:146px;top:866px;width:788px;text-align:center;font-size:32px;color:#0F0E0C','Psikolog, Columbia University',L.root);s1.className='mk-a mk-ou';
var s2=MK.el('div','left:146px;top:912px;width:788px;text-align:center;font-size:32px;color:#B84A2E','Regulatory Focus Theory (1997)',L.root);s2.className='mk-a mk-ou';
var a=MK.el('div','left:96px;top:1080px;width:420px;padding:22px;border-radius:18px;background:#F0C77E;text-align:center','<div class="mk-fr" style="font-size:44px">PROMOTION</div><div class="mk-ou" style="font-size:28px">mengejar keinginan</div>',L.root);a.className='mk-a';
var b=MK.el('div','left:564px;top:1080px;width:420px;padding:22px;border-radius:18px;background:#7FA9BC;text-align:center','<div class="mk-fr" style="font-size:44px">PREVENTION</div><div class="mk-ou" style="font-size:28px">mencari rasa aman</div>',L.root);b.className='mk-a';
L.on(function(t){sp.style.opacity=MK.pr(t,.1,.5);var k=MK.E.over(MK.pr(t,.2,.5));[fr,tg,pt,nm,s1,s2].forEach(function(e,i){e.style.opacity=MK.pr(t,.2+i*.08,.3)});fr.style.transform='rotate(-1.5deg) scale('+(.85+.15*k)+')';
 [a,b].forEach(function(e,i){var q=MK.E.over(MK.pr(t,[@P@,@V@][i]-.2,.35));e.style.opacity=q>0?1:0;e.style.transform='scale('+(.6+.4*q)+')'})});
@SUB@""", G=json.dumps(HIGG), P=w12p, V=w12v, SUB=sub(12)), tr=True, dolly=.03)
ev(12, .2, 'stamp'); ev(12, w12p - .2, 'pop'); ev(12, w12v - .2, 'pop')
# 13 pesan cocok = kunci pas lubangnya
scene(13, R(BP + """
var L1=[['PROMOTION','#F0C77E','“dapatkan”',220],['PREVENTION','#7FA9BC','“aman”',760]];var ks=[];
for(var i=0;i<2;i++){var x=L1[i][3];var s=MK.el('div','left:'+(x-150)+'px;top:820px;width:300px;height:300px;border:6px dashed '+L1[i][1]+';border-radius:24px;text-align:center;color:'+L1[i][1]+';font-size:34px;padding-top:240px;box-sizing:border-box',L1[i][0],L.root);s.className='mk-a mk-mono';
 var k=MK.el('div','left:'+(x-130)+'px;top:420px;width:260px;height:220px;border-radius:20px;background:'+L1[i][1]+';border:5px solid #0F0E0C;text-align:center;font:800 52px/220px Fraunces,serif;color:#0F0E0C',L1[i][2],L.root);k.className='mk-a';ks.push(k)}
var ok=MK.el('div','left:96px;top:300px;font-size:44px;color:#F4EBD9','PESAN COCOK = LEBIH DIPERCAYA',L.root);ok.className='mk-a mk-mono';
L.on(function(t){for(var i=0;i<2;i++){var p=MK.E.io(MK.pr(t,.5+i*.6,.8));ks[i].style.transform='translateY('+(p*420)+'px)';ks[i].style.boxShadow=p>=1?'0 0 40px rgba(240,199,126,.8)':'none'}ok.style.opacity=MK.pr(t,2.2,.4)});
@SUB@""", SUB=sub(13)), tr=True, dolly=.03)
ev(13, 1.3, 'tick'); ev(13, 1.9, 'tick')
# 14 keduanya = hero (venn + kaca pembesar di antara banyak produk)
w14h, w14j = W(14, 'hero', 2.5), W(14, 'jarang', 3.3)
scene(14, R("""DARK(L);VENN(L,560,{a:0,b:0,h:@H@-.2});
var g=MK.el('div','left:96px;top:300px;width:888px;font-size:40px;color:#9a9590','',L.root);g.className='mk-a mk-mono';
L.on(function(t){g.textContent=t>@J@?'JARANG YANG BISA MENEMUKANNYA':''});
@SUB@""", H=w14h, J=w14j, SUB=sub(14)), tr=True, dolly=.04)
ev(14, w14h - .2, 'chime')
# 15 tiga langkah produk hero
w15 = [W(15, 'kembangkan', .1), W(15, 'perkuat', .9), W(15, 'lalu', 1.8)]
scene(15, R(BP + """
LBL(L,96,300,'★ PRODUK HERO',.05,{bg:'#C8944A',c:'#0F0E0C',fs:32});
var S=[['1','KEMBANGKAN','produknya','<path d="M50 90 V40 M50 60 Q20 50 22 22 Q48 26 50 52 M50 46 Q78 34 80 10 Q54 14 50 40"/>'],['2','PERKUAT','brandnya','<circle cx="50" cy="42" r="28"/><path d="M34 66 L28 94 L50 82 L72 94 L66 66"/>'],['3','MARKETING','tepat sasaran','<circle cx="50" cy="50" r="40"/><circle cx="50" cy="50" r="24"/><circle cx="50" cy="50" r="8"/>']],T=@T@;
for(var i=0;i<3;i++){var e=MK.el('div','left:96px;top:'+(440+i*290)+'px;width:888px;height:250px;border:5px solid #F4EBD9;border-radius:22px;display:flex;align-items:center;gap:36px;padding:0 40px;box-sizing:border-box','<svg viewBox="0 0 100 100" width="150" height="150"><g fill="none" stroke="#F0C77E" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">'+S[i][3]+'</g></svg><div><div class="mk-fr" style="font-size:60px;color:#F4EBD9;line-height:1">'+S[i][1]+'</div><div class="mk-ou" style="font-size:36px;color:#9a9590">'+S[i][2]+'</div></div>',L.root);e.className='mk-a';
 (function(e,a){L.on(function(t){var k=MK.E.over(MK.pr(t,a-.1,.35));e.style.opacity=k>0?1:0;e.style.transform='translateX('+((1-k)*-120)+'px)'})})(e,T[i])}
@SUB@""", T=json.dumps(w15), SUB=sub(15)), tr=True, dolly=.03)
[ev(15, x - .1, 'pop') for x in w15]
# 16 PENUTUP: ikon 3 produk + kategorinya (permintaan Aldy)
w16 = [W(16, 'kerudung', 1.0), W(16, 'jamu', 2.1), W(16, 'adem', 2.9)]
scene(16, R("""PASAR(L,{});
var dim=MK.el('div','left:0;top:0;width:1080px;height:1920px;background:rgba(15,14,12,.55)',' ',L.root);dim.className='mk-a';
HL(L,'Produkmu<br>*yang mana?*'.replace('*','<span style="color:#F0C77E">').replace('*','</span>'),.1,{y:290,fs:88});
var P=[['motif','MARKET FIT','disukai','#F0C77E'],['jamu','PROBLEM-SOLUTION FIT','dibutuhkan','#7FA9BC'],['adem','★ KEDUANYA = HERO','disukai + dibutuhkan','#C8944A']],T=@T@;
for(var i=0;i<3;i++){var x=50+i*335;var cd=MK.el('div','left:'+x+'px;top:560px;width:310px;height:640px;background:#F4EBD9;border:6px solid '+(i==2?'#C8944A':'#0F0E0C')+';border-radius:24px;box-shadow:'+(i==2?'0 0 50px rgba(200,148,74,.8)':'none'),' ',L.root);cd.className='mk-a';
 var ic=MK.el('div','left:'+(x+(i==1?95:55))+'px;top:600px;width:200px;height:260px',i==0?KRD('#B84A2E',true,200):i==1?JAMU(120):KRD('#7FA9BC',false,200),L.root);ic.className='mk-a';
 var lb=MK.el('div','left:'+(x+14)+'px;top:900px;width:282px;text-align:center','<div class="mk-fr" style="font-size:'+(i==1?32:36)+'px;line-height:1.1;color:#0F0E0C">'+P[i][1]+'</div><div class="mk-ou" style="font-size:28px;color:#6B6560;margin-top:10px">'+P[i][2]+'</div><div style="margin:16px auto 0;width:120px;height:10px;border-radius:5px;background:'+P[i][3]+'"></div>',L.root);lb.className='mk-a';
 (function(els,a,hero){L.on(function(t){var k=MK.E.over(MK.pr(t,a-.25,.4));els.forEach(function(e){e.style.opacity=k>0?1:0;e.style.transform='translateY('+((1-k)*120)+'px) scale('+(hero&&t>a+.4?1+.03*Math.sin(t*5):1)+')'})})})([cd,ic,lb],T[i],i==2)}
@SUB@""", T=json.dumps(w16), SUB=sub(16, y=1300)), tr=True, dolly=.02)
[ev(16, x - .25, 'pop') for x in w16[:2]]; ev(16, w16[2] - .25, 'chime')
# 17 CTA
w17k = W(17, 'komen', 3.6)
scene(17, R("""DARK(L,{bg:'#0F0E0C'});
var dc=MK.el('div','left:290px;top:400px;width:500px;height:640px;background:#F4EBD9;border:6px solid #0F0E0C;border-radius:16px;transform:rotate(-4deg);padding:36px;box-sizing:border-box','<div class="mk-mono" style="font-size:24px;color:#B84A2E">PANDUAN</div><div class="mk-fr" style="font-size:58px;line-height:1">Strategi<br>Produk</div><div class="mk-ou" style="font-size:26px;color:#6B6560;margin-top:8px">market fit · problem-solution fit · hero</div><div style="display:flex;gap:12px;margin-top:30px"><div style="flex:1;height:120px;border-radius:12px;background:#F0C77E"></div><div style="flex:1;height:120px;border-radius:12px;background:#7FA9BC"></div><div style="flex:1;height:120px;border-radius:12px;background:#C8944A"></div></div><div style="margin-top:24px">'+[0,1,2].map(function(){return '<div style="height:14px;background:#E8E1D5;margin:14px 0;border-radius:6px"></div>'}).join('')+'</div>',L.root);dc.className='mk-a';
var bt=MK.el('div','left:200px;top:1120px;width:680px;padding:26px 0;text-align:center;border-radius:999px;background:#B84A2E;color:#F4EBD9;font-size:56px','Komen “PRODUK”',L.root);bt.className='mk-a mk-fr';
L.on(function(t){var k=MK.E.over(MK.pr(t,.1,.5));dc.style.transform='rotate(-4deg) translateY('+((1-k)*200)+'px)';dc.style.opacity=k>0?1:0;var b=MK.pr(t,@K@-.3,.3);bt.style.opacity=b;bt.style.transform='scale('+(.7+.3*MK.E.over(b)+Math.sin(t*5)*.02*b)+')'});
@SUB@""", K=w17k, SUB=sub(17)), tr=True, dolly=.04)
ev(17, .1, 'slide'); ev(17, w17k - .3, 'chime')
html = ('<!DOCTYPE html>\n<html><head><meta charset="utf-8"><title>Fabel Bisnis 06</title><link rel="stylesheet" href="motionkit/fonts-mk.css"></head><body>\n'
        '<script src="motionkit/kit.js"></script>\n<script>\nvar C=MK.C;\nvar FG=' + json.dumps(FIGS) + ';\n' + HELP + FAB + FAB2 + CAFE_JS + FIELD_JS + SATE_JS + SETANG_JS + PASAR_JS + '\nMK.run([\n' + ',\n'.join(S) + '\n]);\n</script>\n</body></html>\n')
open(A + 'mk-fabel06.html', 'w', encoding='utf-8').write(html)
json.dump({'duration': tl['duration'], 'events': EV, 'cuts': T0}, open(os.path.join(OUT, 'events.json'), 'w'))
print('ok', len(S), 'adegan', round(sum(DUR), 1), 'dtk'); print([(SC[i][0], DUR[i]) for i in range(len(SC))])
