"""Fabel Bisnis #04 Dua tukang sate (dari gen_fabel03b) ekor tikus: animasi penuh Motion Kit dari timing.json vo_prep.
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
SC = [('satu',0,0),('pak',0,0),('pak',0,0),('motor',0,0),('pak',0,1),
      ('di',1,0),('orang',1,0),('dan',1,0),('mata',1,0),('sentuhan',1,0),('jadi',1,0),
      ('di',2,0),('etalase',2,0),('begitu',2,0),('hasilnya',2,0),
      ('besok',3,0),('apa',3,0),('kalau',3,0),('dua',3,0),('kedua',3,0),
      ('sekarang',4,0),('mau',4,0)]
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
KEY = {'sama','jono','kardi','dicicipi','sensory','marketing','indra','logika','jarak','mata','hidung','telinga','menoleh','mendekat','masuk','membeli','kembali','produk','produknya','elegan','andalan','sorot','wangi','betah','mencoba','meter','kelihatan','kecium','kedengeran','cocok','pergi','google','maps','etalase','pertamamu','jujur','berhenti','sensory'}
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
EM = lambda s: s.replace('*', '<span style="color:#C8944A">', 1).replace('*', '</span>', 1)
# 0 HOOK: dua gerobak, satu dikerumuni, satu sepi (hasil akhir di 3 dtk pertama)
uk0, uj0 = F('k0', 'kardi'), F('j0', 'jono', True)
cus0 = [F('c0%d' % i, ['p1', 'p2', 'p3', 'cs'][i % 4], i % 2 == 0) for i in range(5)]
scene(0, R("""STREET(L,{});
var A=CART(L,40,800,{name:'SATE KARDI',roof:'#6B6560',smoke:'in',front:false});var B=CART(L,640,800,{name:'SATE JONO',front:true,side:'l',smoke:'out',reach:420});
var k=FIG(L,'@K@',300,700,150,false),j=FIG(L,'@J@',900,700,150,true);
var C=@C@;var cv=C.map(function(u,i){return FIG(L,u,420+i*70,860,130,i%2==0)});
HL(L,'Satenya sama enak.<br>*Yang satu sepi.*'.replace('*','<span style="color:#C8944A">').replace('*','</span>'),0,{y:300});
L.on(function(t){for(var i=0;i<C.length;i++){var k2=MK.E.out(MK.pr(t,.6+i*.25,.6));cv[i].style.opacity=k2>0?1:0;cv[i].style.transform=(i%2==0?'scaleX(-1) ':'')+'translateX('+((1-k2)*-300)+'px)';WALK(C[i],t,k2<1)}
ARM('@J@','ra',-110+Math.sin(t*12)*30);SMILE('@J@',.8);SMILE('@K@',-.4);HEAD('@K@',Math.sin(t*1.5)*10)});
@SUB@""", K=uk0, J=uj0, C=json.dumps(cus0), SUB=sub(0)), dolly=.03)
ev(0, .6, 'pop')
# 1 Pak Kardi: bakar di belakang, asap dikipas ke dalam, orang lewat tanpa menoleh
uk1 = F('k1', 'kardi'); pw1 = [F('w1%d' % i, ['p1', 'p3', 'cs'][i % 3]) for i in range(3)]
w1a = W(1, 'asapnya', 2.8); w1o = W(1, 'orang', 5.5)
scene(1, R("""STREET(L,{});
var A=CART(L,320,800,{name:'SATE KARDI',roof:'#6B6560',smoke:'in',front:false,smokeAt:@A@-.3});
var k=FIG(L,'@K@',560,690,150,true);LBL(L,96,300,'PAK KARDI · BAKAR DI BELAKANG',.1,{bg:'#6B6560'});
var arr=MK.el('div','left:520px;top:560px;width:200px;height:120px','<svg viewBox="0 0 200 120" width="200" height="120"><path d="M180 90 Q100 10 30 60" fill="none" stroke="#F4EBD9" stroke-width="6" stroke-dasharray="14 12"/><path d="M30 60 l26 -4 l-12 22z" fill="#F4EBD9"/></svg>',L.root);arr.className='mk-a';
var P=@P@;var pv=P.map(function(u,i){return FIG(L,u,0,980,140,false)});
L.on(function(t){ARM('@K@','ra',t>@A@-.3?-120+Math.sin(t*10)*28:-10);arr.style.opacity=MK.pr(t,@A@,.3);
for(var i=0;i<P.length;i++){var s=@O@-1.6+i*1.1;var p=(t-s)/4;pv[i].style.opacity=p>0&&p<1?1:0;pv[i].style.transform='translateX('+(-160+p*1300)+'px)';WALK(P[i],t,true);HEAD(P[i],0)}});
@SUB@""", K=uk1, A=w1a, O=w1o, P=json.dumps(pw1), SUB=sub(1)), tr=True, dolly=.04)
# 2 Pak Jono: api di depan (mata), asap ke jalan (hidung), desis (telinga)
uj2 = F('j2', 'jono', True)
w2a, w2s, w2d = W(2, 'apinya', 2.1), W(2, 'asapnya', 4.3), W(2, 'desisnya', 6.7)
scene(2, R("""STREET(L,{});
var B=CART(L,560,780,{name:'SATE JONO',front:true,side:'l',smoke:'out',reach:560,smokeAt:@S@-.3,n:20});
var j=FIG(L,'@J@',440,690,150,false);LBL(L,96,300,'PAK JONO · BAKAR DI DEPAN',.1,{bg:'#B84A2E'});
ICO(L,'eye',120,400,140,'#F0C77E',@A@);LBL(L,96,560,'kelihatan',@A@+.1,{bg:'transparent',c:'#F0C77E',fs:34});
ICO(L,'nose',470,400,140,'#F0C77E',@S@);LBL(L,450,560,'kecium',@S@+.1,{bg:'transparent',c:'#F0C77E',fs:34});
ICO(L,'ear',820,400,140,'#F0C77E',@D@);LBL(L,770,560,'kedengeran',@D@+.1,{bg:'transparent',c:'#F0C77E',fs:34});
var wv=MK.el('div','left:200px;top:820px;width:200px;height:200px','<svg viewBox="0 0 200 200" width="200" height="200"><g fill="none" stroke="#F0C77E" stroke-width="5" stroke-linecap="round"><path class="w0" d="M150 60 q30 40 0 80"/><path class="w1" d="M120 40 q50 60 0 120"/></g><text x="10" y="110" font-family="Caveat,cursive" font-size="44" fill="#F0C77E">sssh</text></svg>',L.root);wv.className='mk-a';
L.on(function(t){ARM('@J@','la',-110+Math.sin(t*12)*30);SMILE('@J@',.7);wv.style.opacity=t>@D@?(.5+.5*Math.sin(t*16)):0});
@SUB@""", J=uj2, A=w2a, S=w2s, D=w2d, SUB=sub(2)), tr=True, dolly=.04)
ev(2, w2a, 'pop'); ev(2, w2s, 'pop'); ev(2, w2d, 'pop')
# 3 Motor yang lewat berhenti di Pak Jono
w3s = W(3, 'semuanya', 2.5)
scene(3, R("""STREET(L,{gy:1000,speed:0});
var A=CART(L,-40,700,{name:'KARDI',roof:'#6B6560',smoke:'in',front:false});var B=CART(L,640,700,{name:'JONO',front:true,side:'l',smoke:'out',reach:380});
var cl=['#3e5a6b','#B84A2E','#C8944A','#2f4a3a'];for(var i=0;i<4;i++)MOTOR(L,1130+(i%2)*150,{x0:-260-i*60,x1:560+(i%2)*120-(i>1?220:0),at:.1+i*.5,d:1.8,stop:true,c:cl[i]});
var n=MK.el('div','left:700px;top:300px;font-size:120px;color:#F0C77E','0',L.root);n.className='mk-a mk-fr';var nl=LBL(L,700,440,'MAMPIR KE JONO',.2,{bg:'#B84A2E'});var z=MK.el('div','left:96px;top:300px;font-size:120px;color:#9a9590','0',L.root);z.className='mk-a mk-fr';LBL(L,96,440,'KE KARDI',.2,{bg:'#6B6560'});
L.on(function(t){n.textContent=Math.min(4,Math.max(0,Math.floor((t-.9)/.5)+1))});
@SUB@""", SUB=sub(3)), tr=True, dolly=.03)
[ev(3, 1.9 + i * .5, 'tick') for i in range(4)]
# 4 Kardi kalah sebelum dicicipi
uk4 = F('k4', 'kardi')
w4d = W(4, 'dicicipi', 3.2)
scene(4, R("""STREET(L,{});var A=CART(L,320,800,{name:'SATE KARDI',roof:'#6B6560',smoke:'in',front:false});
var k=FIG(L,'@K@',560,690,150,true);
var pl=MK.el('div','left:340px;top:900px;width:360px;height:160px','<svg viewBox="0 0 360 160" width="360" height="160"><ellipse cx="180" cy="120" rx="170" ry="34" fill="#F4EBD9" stroke="#0F0E0C" stroke-width="6"/>'+[0,1,2,3,4].map(function(i){return '<path d="M'+(70+i*50)+' 120 L'+(110+i*50)+' 40" stroke="#8a5a3a" stroke-width="5"/><rect x="'+(84+i*50)+'" y="70" width="18" height="40" rx="6" transform="rotate(25 '+(93+i*50)+' 90)" fill="#9a4a22" stroke="#0F0E0C" stroke-width="3"/>'}).join('')+'</svg>',L.root);pl.className='mk-a';
var tg=MK.el('div','left:600px;top:840px;padding:14px 24px;background:#F4EBD9;border:4px solid #0F0E0C;border-radius:10px;font-size:40px;transform:rotate(6deg)','belum dicicipi',L.root);tg.className='mk-a mk-ca';
HL(L,'Gak kalah rasa.<br>*Kalah duluan.*'.replace('*','<span style="color:#C8944A">').replace('*','</span>'),.1,{y:290});
L.on(function(t){SMILE('@K@',-.6);HEAD('@K@',-8+Math.sin(t*1.2)*6);var k2=MK.pr(t,@D@-.4,.3);tg.style.opacity=k2;tg.style.transform='rotate(6deg) scale('+(1.4-.4*MK.E.out(k2))+')'});
@SUB@""", K=uk4, D=w4d, SUB=sub(4)), tr=True, dolly=.05)
ev(4, w4d - .4, 'stamp')
# 5 POROS + kartu tokoh Krishna
w5s = W(5, 'sensory', 2.4)
scene(5, R("""DARK(L,{bg:'#080706'});
var sp=MK.el('div','left:190px;top:0;width:700px;height:1500px;background:linear-gradient(rgba(244,235,217,.14),rgba(244,235,217,0));clip-path:polygon(40% 0,60% 0,100% 100%,0 100%)',' ',L.root);sp.className='mk-a';
var tt=MK.el('div','left:96px;top:300px;width:888px;text-align:center;font-size:96px;line-height:1;color:#F4EBD9','Sensory<br><span style="color:#C8944A">Marketing</span>',L.root);tt.className='mk-a mk-fr';
var fr=MK.el('div','left:146px;top:560px;width:788px;height:760px;border-radius:24px;background:#F4EBD9;border:6px solid #0F0E0C;box-shadow:0 40px 80px -30px rgba(0,0,0,.8)',' ',L.root);fr.className='mk-a';
var tg=MK.el('div','left:190px;top:596px;font-size:26px;letter-spacing:.1em;color:#B84A2E','KARTU TOKOH',L.root);tg.className='mk-a mk-mono';
var pt=MK.el('div','left:390px;top:620px;width:300px;height:415px',@G@,L.root);pt.className='mk-a';
var nm=MK.el('div','left:146px;top:1060px;width:788px;text-align:center;font-size:60px;line-height:1;color:#0F0E0C','ARADHNA KRISHNA',L.root);nm.className='mk-a mk-fr';
var s1=MK.el('div','left:146px;top:1140px;width:788px;text-align:center;font-size:34px;color:#0F0E0C','Profesor marketing, University of Michigan',L.root);s1.className='mk-a mk-ou';
var s2=MK.el('div','left:146px;top:1190px;width:788px;text-align:center;font-size:34px;color:#B84A2E','Pelopor riset sensory marketing',L.root);s2.className='mk-a mk-ou';
LBL(L,96,1360,'DI DUNIA BISNIS',.2,{bg:'transparent',c:'#9a9590'});var E=@E@;L.on(function(t){sp.style.opacity=MK.pr(t,.1,.6);var a=MK.pr(t,E-.3,.4);tt.style.opacity=a;tt.style.transform='scale('+(.8+.2*MK.E.over(a))+')';var k=MK.E.over(MK.pr(t,E+.5,.5));[fr,tg,pt,nm,s1,s2].forEach(function(e,i){e.style.opacity=t<E+.5?0:MK.pr(t,E+.5+i*.08,.3)});fr.style.transform='rotate(-1.5deg) scale('+(.85+.15*k)+')';pt.style.transform='translateY('+((1-k)*50)+'px)'});
@SUB@""", G=json.dumps(KRISHNA), E=w5s, SUB=sub(5)), tr=True, dolly=.04)
ev(5, .1, 'sweep'); ev(5, w5s - .3, 'stamp')
# 6 indra vs logika: timbangan
w6b = W(6, 'bukan', 2.6)
scene(6, R("""DARK(L);
var sc=MK.el('div','left:140px;top:520px;width:800px;height:700px','<svg viewBox="0 0 800 700" width="800" height="700" style="overflow:visible"><path d="M400 680 V180" stroke="#F4EBD9" stroke-width="10"/><path d="M300 680 h200" stroke="#F4EBD9" stroke-width="12" stroke-linecap="round"/><g id="bm6"><path d="M100 180 H700" stroke="#C8944A" stroke-width="12" stroke-linecap="round"/><g id="pl6"><path d="M100 180 L40 380 H160Z" fill="none" stroke="#F4EBD9" stroke-width="4"/><path d="M20 380 h160 q-10 40 -80 40 q-70 0 -80 -40z" fill="#C8944A" stroke="#0F0E0C" stroke-width="4"/></g><g id="pr6"><path d="M700 180 L640 380 H760Z" fill="none" stroke="#F4EBD9" stroke-width="4"/><path d="M620 380 h160 q-10 40 -80 40 q-70 0 -80 -40z" fill="#6B6560" stroke="#0F0E0C" stroke-width="4"/></g></g><circle cx="400" cy="180" r="16" fill="#F4EBD9"/></svg>',L.root);sc.className='mk-a';
var ic=['eye','nose','ear'],ie=[];for(var i=0;i<3;i++)ie.push(ICO(L,ic[i],150+i*70,830,80,'#F0C77E',.2+i*.2));
var lg=MK.el('div','left:720px;top:820px;width:120px;text-align:center;font-size:30px;color:#F4EBD9;line-height:1.1','LOGIKA<br>harga · spek',L.root);lg.className='mk-a mk-mono';
LBL(L,96,300,'ORANG MAMPIR PAKAI',.1);HL(L,'Indra dulu.<br>*Logika belakangan.*'.replace('*','<span style="color:#C8944A">').replace('*','</span>'),@B@-.2,{y:380,fs:80});
L.on(function(t){var a=-14*MK.E.io(MK.pr(t,.8,.9));var bm=document.getElementById('bm6');if(bm)bm.setAttribute('transform','rotate('+a+' 400 180)');
var dl=-Math.sin(a*Math.PI/180)*300;ie.forEach(function(e){e.style.marginTop=dl+'px'});lg.style.marginTop=(-dl)+'px';
['pl6','pr6'].forEach(function(id,j){var g=document.getElementById(id);if(g)g.setAttribute('transform','rotate('+(-a)+' '+(j?700:100)+' 180)')})});
@SUB@""", B=w6b, SUB=sub(6)), tr=True, dolly=.03)
# 7 + 8: jarak indra (tampak atas): toko di bawah, cincin jarak; figur berjalan mendekat
w8h, w8t = W(8, 'hidung', 3.4), W(8, 'telinga', 5.3)
uw8 = F('w8', 'p1')
scene(7, R(BP + """
var st=MK.el('div','left:390px;top:1130px;width:300px;height:200px;background:#C8944A;border:5px solid #0F0E0C;border-radius:10px;text-align:center;font:800 44px/200px Fraunces,serif;color:#0F0E0C','TOKO',L.root);st.className='mk-a';
var R=[[760,'MATA'],[540,'HIDUNG'],[330,'TELINGA']],rg=[];for(var i=0;i<3;i++){var d=R[i][0];var e=MK.el('div','left:'+(540-d)+'px;top:'+(1230-d)+'px;width:'+(2*d)+'px;height:'+(2*d)+'px;border-radius:50%;border:4px dashed rgba(244,235,217,.55)',' ',L.root);e.className='mk-a';rg.push(e)}
var ru=MK.el('div','left:96px;top:300px;width:888px;height:60px','<svg viewBox="0 0 888 60" width="888" height="60"><path d="M0 30 H888" stroke="#F4EBD9" stroke-width="4"/>'+[0,1,2,3,4,5,6,7,8].map(function(i){return '<path d="M'+(i*111)+' 14 V46" stroke="#F4EBD9" stroke-width="4"/>'}).join('')+'</svg>',L.root);ru.className='mk-a';
LBL(L,96,380,'INDRA BEKERJA SESUAI JARAK',.2,{bg:'#C8944A',c:'#0F0E0C'});
L.on(function(t){for(var i=0;i<3;i++){var k=MK.E.out(MK.pr(t,.4+i*.5,.6));rg[i].style.transform='scale('+k+')';rg[i].style.opacity=k}});
@SUB@""", SUB=sub(7)), tr=True, dolly=.02)
scene(8, R(BP + """
var st=MK.el('div','left:390px;top:1130px;width:300px;height:200px;background:#C8944A;border:5px solid #0F0E0C;border-radius:10px;text-align:center;font:800 44px/200px Fraunces,serif;color:#0F0E0C','TOKO',L.root);st.className='mk-a';
var R=[[760,'eye','menoleh',0],[540,'nose','mendekat',@H@],[330,'ear','masuk',@T@]],rg=[];
for(var i=0;i<3;i++){var d=R[i][0];var e=MK.el('div','left:'+(540-d)+'px;top:'+(1230-d)+'px;width:'+(2*d)+'px;height:'+(2*d)+'px;border-radius:50%;border:5px dashed rgba(244,235,217,.45)',' ',L.root);e.className='mk-a';rg.push(e);
 ICO(L,R[i][1],60+i*330,1230-d+30-(i==0?0:0),110,'#F0C77E',R[i][3]);LBL(L,180+i*330,1230-d+60,R[i][2],R[i][3]+.15,{bg:'transparent',c:'#F0C77E',fs:36})}
var f=FIG(L,'@U@',0,0,120,false);
L.on(function(t){var seg=t<@H@?0:t<@T@?1:2;for(var i=0;i<3;i++){rg[i].style.borderColor=i==seg?'#F0C77E':'rgba(244,235,217,.3)';rg[i].style.borderStyle=i<=seg?'solid':'dashed'}
var ys=[1230-760-60,1230-540-90,1230-330-110,1230-230];var p=seg+MK.E.io(MK.pr(t,[0,@H@,@T@][seg]+.2,1.0));var y=ys[Math.floor(p)]+(ys[Math.min(3,Math.floor(p)+1)]-ys[Math.floor(p)])*(p%1);
f.style.transform='translate(470px,'+(y-100)+'px)';WALK('@U@',t,true);if(seg==0)HEAD('@U@',-20+20*MK.pr(t,.3,.5))});
@SUB@""", H=w8h, T=w8t, U=uw8, SUB=sub(8)), dolly=.02)
ev(8, 0, 'pop'); ev(8, w8h, 'pop'); ev(8, w8t, 'pop')
# 9 sentuhan & rasa di dalam -> membeli -> kembali
w9m, w9k = W(9, 'membeli', 3.2), W(9, 'kembali', 3.9)
scene(9, R(BP + """
var ins=MK.el('div','left:96px;top:420px;width:888px;height:700px;border:5px solid #F4EBD9;border-radius:24px',' ',L.root);ins.className='mk-a';LBL(L,120,390,'DI DALAM TOKO',.1,{bg:'#C8944A',c:'#0F0E0C'});
ICO(L,'hand',190,560,200,'#F0C77E',.2,{float:true});ICO(L,'tongue',690,560,200,'#F0C77E',.6,{float:true});
var bg=ICO(L,'bag',440,820,200,'#F4EBD9',@M@-.3);
var rt=MK.el('div','left:700px;top:820px;width:240px;height:240px','<svg viewBox="0 0 240 240" width="240" height="240"><path d="M200 120 A80 80 0 1 1 120 40" fill="none" stroke="#B84A2E" stroke-width="10" stroke-linecap="round"/><path d="M110 20 L140 40 L110 62Z" fill="#B84A2E"/></svg>',L.root);rt.className='mk-a';
L.on(function(t){var k=MK.pr(t,@K@-.2,.4);rt.style.opacity=k;rt.style.transform='rotate('+(k*360)+'deg)'});
@SUB@""", M=w9m, K=w9k, SUB=sub(9)), tr=True, dolly=.03)
ev(9, w9m - .3, 'pop'); ev(9, w9k - .2, 'chime')
# 10 bukan kalah produk, kalah jarak indra
w10t = W(10, 'tapi', 3.6)
scene(10, R(BP + """
var cs=[['TOKOMU','#6B6560',260],['TOKO SEBELAH','#C8944A',760]];
for(var i=0;i<2;i++){var c=MK.el('div','left:'+(cs[i][2]-200)+'px;top:500px;width:400px;height:560px;border:5px solid #F4EBD9;border-radius:20px;text-align:center;color:#F4EBD9',
 '<div class="mk-mono" style="font-size:28px;margin-top:24px">'+cs[i][0]+'</div><div style="margin-top:30px">'+IC('shirt',150,'#F4EBD9')+'</div><div class="mk-fr" style="font-size:44px;color:#F0C77E;margin-top:10px">★★★★★</div><div class="mk-mono" style="font-size:24px;color:#9a9590">produk sama bagus</div>',L.root);c.className='mk-a'}
var r1=MK.el('div','left:140px;top:1100px;width:240px;height:24px;background:#6B6560;border-radius:12px;transform-origin:left',' ',L.root);r1.className='mk-a';var r2=MK.el('div','left:600px;top:1100px;width:320px;height:24px;background:#F0C77E;border-radius:12px;transform-origin:left',' ',L.root);r2.className='mk-a';
var l1=LBL(L,140,1140,'JANGKAUAN INDRA',@T@-.4,{bg:'transparent',fs:26});
HL(L,'Bukan kalah produk.<br>*Kalah jarak indra.*'.replace('*','<span style="color:#C8944A">').replace('*','</span>'),@T@-.2,{y:300,fs:80});
L.on(function(t){var k=MK.E.out(MK.pr(t,@T@-.4,.8));r1.style.transform='scaleX('+(.35*k)+')';r2.style.transform='scaleX('+k+')'});
@SUB@""", T=w10t, SUB=sub(10)), tr=True, dolly=.03)
# 11 kesaksian: produk tetap, indra diubah
w11k = W(11, 'kami', 1.9); w11c = W(11, 'cara', 3.9)
scene(11, R(BP + """
var st=MK.el('div','left:96px;top:300px;padding:16px 28px;border:6px solid #C8944A;border-radius:12px;color:#C8944A;font-size:40px;transform:rotate(-3deg)','DARI BRAND FASHION YANG SAYA DAMPINGI',L.root);st.className='mk-a mk-fr';
var pr=MK.el('div','left:96px;top:520px;width:380px;height:440px;border:5px solid #F4EBD9;border-radius:20px;text-align:center;color:#F4EBD9','<div class="mk-mono" style="font-size:28px;margin-top:24px">PRODUK</div><div style="margin-top:24px">'+IC('shirt',170,'#F4EBD9')+'</div><div class="mk-fr" style="font-size:52px;margin-top:14px">TETAP</div>',L.root);pr.className='mk-a';
var bx=MK.el('div','left:540px;top:520px;width:444px;height:440px;border:5px solid #F0C77E;border-radius:20px',' ',L.root);bx.className='mk-a';LBL(L,570,540,'YANG DIUBAH',@C@-.2,{bg:'#F0C77E',c:'#0F0E0C',fs:26});
var ic=['eye','ear','nose','hand'];for(var i=0;i<4;i++)ICO(L,ic[i],580+(i%2)*200,640+Math.floor(i/2)*160,130,'#F0C77E',@C@+i*.25);
L.on(function(t){var k=MK.pr(t,.1,.25);st.style.opacity=k;st.style.transform='rotate(-3deg) scale('+(1.3-.3*MK.E.out(k))+')';pr.style.opacity=MK.pr(t,@K@-.3,.3);bx.style.opacity=MK.pr(t,@C@-.3,.3)});
@SUB@""", K=w11k, C=w11c, SUB=sub(11)), tr=True, dolly=.03)
ev(11, .1, 'stamp'); [ev(11, w11c + i * .25, 'tick') for i in range(4)]
# 12 etalase kaca elegan + hero produk disorot
w12s = W(12, 'sorot', 5.4); w12a = W(12, 'andalan', 4.1)
scene(12, R("""DARK(L,{bg:'linear-gradient(#141210,#0b0a08)'});
var fc=MK.el('div','left:60px;top:300px;width:960px;height:1100px','<svg viewBox="0 0 960 1100" width="960" height="1100"><rect x="0" y="0" width="960" height="1100" fill="#1e1a17"/><rect x="0" y="0" width="960" height="110" fill="#0F0E0C"/><text x="480" y="72" text-anchor="middle" font-family="Fraunces,serif" font-style="italic" font-weight="600" font-size="52" fill="#C8944A" letter-spacing="6">maison</text><rect x="60" y="170" width="840" height="800" fill="#2a2622" stroke="#C8944A" stroke-width="6"/><rect x="60" y="930" width="840" height="40" fill="#3a332c"/></svg>',L.root);fc.className='mk-a';
var mk=[];var xs=[230,780,505];for(var i=0;i<3;i++){var hero=i==2;var e=MK.el('div','left:'+(xs[i]-90)+'px;top:'+(hero?640:720)+'px;width:180px;height:'+(hero?560:480)+'px','<svg viewBox="0 0 180 560" width="180" height="'+(hero?560:480)+'" preserveAspectRatio="none"><circle cx="90" cy="50" r="34" fill="#d9cfbf"/><path d="M90 84 V110" stroke="#d9cfbf" stroke-width="16"/><path d="M40 120 Q90 100 140 120 L150 300 L170 520 H10 L30 300Z" fill="'+(hero?'#B84A2E':'#4a4540')+'" stroke="#0F0E0C" stroke-width="5"/><path d="M90 540 V560" stroke="#0F0E0C" stroke-width="6"/></svg>',L.root);e.className='mk-a';mk.push(e)}
var beam=MK.el('div','left:355px;top:300px;width:300px;height:1000px;background:linear-gradient(rgba(251,231,184,.5),rgba(251,231,184,0));clip-path:polygon(42% 0,58% 0,100% 100%,0 100%)',' ',L.root);beam.className='mk-a';
var gl=MK.el('div','left:60px;top:470px;width:960px;height:800px;background:linear-gradient(115deg,rgba(255,255,255,0) 30%,rgba(255,255,255,.12) 40%,rgba(255,255,255,0) 50%)',' ',L.root);gl.className='mk-a';
LBL(L,96,250,'ETALASE · ELEGAN',.1,{bg:'#C8944A',c:'#0F0E0C'});var ht=LBL(L,700,560,'PRODUK ANDALAN',@A@,{bg:'#B84A2E'});
L.on(function(t){var b=MK.pr(t,@S@-.3,.2);beam.style.opacity=b*(0.9+.1*Math.sin(t*9));mk[2].style.filter='brightness('+(.6+.7*b)+')';for(var i=0;i<2;i++)mk[i].style.filter='brightness('+(1-.4*b)+')';gl.style.transform='translateX('+(((t*120)%1400)-700)+'px)'});
@SUB@""", S=w12s, A=w12a, SUB=sub(12)), tr=True, dolly=.04)
ev(12, w12s - .3, 'chime')
# 13 di dalam: musik, bersih, wangi
w13m, w13b, w13w = W(13, 'musiknya', 1.2), W(13, 'bersih', 3.8), W(13, 'wangi', 4.6)
uc13 = F('c13', 'p2')
scene(13, R("""DARK(L,{bg:'linear-gradient(#2a221c,#16120f)'});
var fl=MK.el('div','left:0;top:1080px;width:1080px;height:840px;background:repeating-linear-gradient(90deg,#3a2f26 0 120px,#33291f 120px 240px)',' ',L.root);fl.className='mk-a';
var rk=MK.el('div','left:80px;top:560px;width:420px;height:520px','<svg viewBox="0 0 420 520" width="420" height="520"><path d="M10 30 H410" stroke="#C8944A" stroke-width="8"/>'+[0,1,2,3,4,5].map(function(i){return '<path d="M'+(40+i*64)+' 30 v20" stroke="#C8944A" stroke-width="4"/><path d="M'+(20+i*64)+' 50 h44 l6 180 h-56z" fill="'+['#B84A2E','#F4EBD9','#2f4a3a','#C8944A','#6B6560','#F4EBD9'][i]+'" stroke="#0F0E0C" stroke-width="4"/>'}).join('')+'</svg>',L.root);rk.className='mk-a';
var c=FIG(L,'@C@',620,780,170,false);
var nt=[];for(var i=0;i<5;i++)nt.push(ICO(L,'music',560+(i%3)*130,400+(i%2)*90,90,'#F0C77E',@M@+i*.15));
var sp=[];for(var i=0;i<4;i++)sp.push(ICO(L,'spark',120+i*230,1180+(i%2)*80,70,'#F4EBD9',@B@+i*.12));
var sc=[];for(var i=0;i<3;i++)sc.push(ICO(L,'scent',150+i*300,900,120,'#C8944A',@W@+i*.15));
L.on(function(t){nt.forEach(function(e,i){e.style.marginTop=(-((t*40+i*30)%120))+'px'});sc.forEach(function(e,i){e.style.marginTop=(-((t*30+i*20)%60))+'px'});SMILE('@C@',.8);HEAD('@C@',Math.sin(t*3)*8);BOB('@C@',t,3)});
@SUB@""", C=uc13, M=w13m, B=w13b, W=w13w, SUB=sub(13)), tr=True, dolly=.03)
ev(13, w13m, 'chime'); ev(13, w13b, 'pop')
# 14 hasil: betah (jam), mencoba (ruang ganti), membeli (tas)
w14b, w14c, w14m = W(14, 'betah', 1.1), W(14, 'mencoba', 2.8), W(14, 'membeli', 3.9)
scene(14, R(BP + """
var cols=[['clock','BETAH LEBIH LAMA',@B@],['shirt','MULAI MENCOBA',@C@],['bag','MEMBELI',@M@]];
for(var i=0;i<3;i++){var x=96+i*300;var e=MK.el('div','left:'+x+'px;top:560px;width:280px;height:420px;border:5px solid '+(i==2?'#F0C77E':'#F4EBD9')+';border-radius:20px',' ',L.root);e.className='mk-a';(function(e,a){L.on(function(t){var k=MK.pr(t,a-.2,.3);e.style.opacity=k;e.style.transform='translateY('+((1-MK.E.out(k))*60)+'px)'})})(e,cols[i][2]);
 ICO(L,cols[i][0],x+50,620,180,i==2?'#F0C77E':'#F4EBD9',cols[i][2]);LBL(L,x+10,860,cols[i][1],cols[i][2]+.1,{bg:'transparent',fs:24})}
var hd=MK.el('div','left:146px;top:700px;width:180px;height:4px;background:#B84A2E;transform-origin:left',' ',L.root);hd.className='mk-a';
var ar=MK.el('div','left:96px;top:1040px;width:888px;height:60px','<svg viewBox="0 0 888 60" width="888" height="60"><path d="M10 30 H860" stroke="#C8944A" stroke-width="6" stroke-dasharray="16 12"/><path d="M860 10 L886 30 L860 50Z" fill="#C8944A"/></svg>',L.root);ar.className='mk-a';
L.on(function(t){ar.style.clipPath='inset(0 '+(100-100*MK.pr(t,.3,@M@))+'% 0 0)'});
@SUB@""", B=w14b, C=w14c, M=w14m, SUB=sub(14)), tr=True, dolly=.03)
ev(14, w14m - .2, 'chime')
# 15 tes 20 meter
uw15 = F('w15', 'cs')
scene(15, R(BP + """
var sun=MK.el('div','left:820px;top:300px;width:140px;height:140px;border-radius:50%;background:#F0C77E;box-shadow:0 0 90px 30px rgba(240,199,126,.35)',' ',L.root);sun.className='mk-a';LBL(L,96,300,'BESOK PAGI',.1,{bg:'#C8944A',c:'#0F0E0C'});
var st=MK.el('div','left:700px;top:780px;width:300px;height:300px;background:#C8944A;border:5px solid #0F0E0C;border-radius:10px;text-align:center;font:800 44px/300px Fraunces,serif;color:#0F0E0C','TOKOMU',L.root);st.className='mk-a';
var f=FIG(L,'@U@',110,820,140,false);
var tp=MK.el('div','left:260px;top:1100px;width:440px;height:80px','<svg viewBox="0 0 440 80" width="440" height="80"><rect x="0" y="20" width="440" height="40" fill="#F0C77E" stroke="#0F0E0C" stroke-width="4"/>'+Array.apply(null,Array(22)).map(function(_,i){return '<path d="M'+(i*20)+' 20 v'+(i%5?12:22)+'" stroke="#0F0E0C" stroke-width="3"/>'}).join('')+'</svg>',L.root);tp.className='mk-a';
var m=MK.el('div','left:330px;top:1200px;font-size:96px;color:#F4EBD9','0 m',L.root);m.className='mk-a mk-fr';
L.on(function(t){var k=MK.E.out(MK.pr(t,1.8,1.4));tp.style.clipPath='inset(0 '+(100-100*k)+'% 0 0)';m.textContent=Math.round(20*k)+' m';HEAD('@U@',8)});
@SUB@""", U=uw15, SUB=sub(15)), tr=True, dolly=.03)
ev(15, 1.8, 'slide')
# 16 tiga pertanyaan
w16 = [W(16, 'apa', 0.2)]; ws16 = [w['t'] - T0[16] for w in words[starts[16]:starts[17]] if nrm(w['w']) == 'apa']
scene(16, R(BP + """
var Q=[['eye','Apa yang kelihatan?'],['nose','Apa yang kecium?'],['ear','Apa yang kedengeran?']],T=@T@;
for(var i=0;i<3;i++){var y=520+i*250;var bx=MK.el('div','left:96px;top:'+y+'px;width:888px;height:210px;border:5px solid #F4EBD9;border-radius:20px',' ',L.root);bx.className='mk-a';(function(e,a){L.on(function(t){var k=MK.pr(t,a-.2,.3);e.style.opacity=k;e.style.transform='translateX('+((1-MK.E.out(k))*-80)+'px)'})})(bx,T[i]);
 ICO(L,Q[i][0],130,y+40,130,'#F0C77E',T[i]);var q=MK.el('div','left:300px;top:'+(y+70)+'px;font-size:52px;color:#F4EBD9',Q[i][1],L.root);q.className='mk-a mk-fr';(function(e,a){L.on(function(t){e.style.opacity=MK.pr(t,a,.3)})})(q,T[i])}
LBL(L,96,380,'DARI 20 METER',.1,{bg:'#C8944A',c:'#0F0E0C'});
@SUB@""", T=json.dumps([round(x, 2) for x in ws16[:3]] if len(ws16) >= 3 else [0.2, 1.6, 2.9]), SUB=sub(16)), tr=True, dolly=.02)
[ev(16, x, 'tick') for x in (ws16[:3] if len(ws16) >= 3 else [])]
# 17 kalau gak ada -> pembeli lewat
uw17 = F('w17', 'p3')
scene(17, R("""STREET(L,{});var A=CART(L,320,800,{name:'TOKOMU',roof:'#6B6560',smoke:'in',front:false,n:4});
var ic=['eye','nose','ear'];for(var i=0;i<3;i++){ICO(L,ic[i],180+i*260,330,140,'#9a9590',.1+i*.15);var x=MK.el('div','left:'+(170+i*260)+'px;top:320px;width:160px;height:160px','<svg viewBox="0 0 160 160" width="160" height="160"><path d="M20 20 L140 140 M140 20 L20 140" stroke="#B84A2E" stroke-width="12" stroke-linecap="round"/></svg>',L.root);x.className='mk-a';(function(e,a){L.on(function(t){var k=MK.pr(t,a,.2);e.style.opacity=k;e.style.transform='scale('+(1.5-.5*k)+')'})})(x,.9+i*.25)}
var f=FIG(L,'@U@',0,980,150,false);
L.on(function(t){var p=(t-.5)/3;f.style.opacity=p>0&&p<1?1:0;f.style.transform='translateX('+(-160+p*1300)+'px)';WALK('@U@',t,true)});
@SUB@""", U=uw17, SUB=sub(17)), tr=True, dolly=.03)
[ev(17, .9 + i * .25, 'stamp') for i in range(3)]
# 18 dua aturan: aturan 1 cocok vs salah
w18p, w18l = W(18, 'pertama', 1.4), W(18, 'lagu', 4.9)
uo18, ub18 = F('o18', 'p2'), F('b18', 'p1')
scene(18, R(BP + """
LBL(L,96,300,'ATURAN 1 · COCOK DENGAN PEMBELIMU',@P@-.2,{bg:'#C8944A',c:'#0F0E0C',fs:28});
var a=MK.el('div','left:96px;top:440px;width:420px;height:760px;border:5px solid #F0C77E;border-radius:20px',' ',L.root);a.className='mk-a';
var b=MK.el('div','left:564px;top:440px;width:420px;height:760px;border:5px solid #B84A2E;border-radius:20px',' ',L.root);b.className='mk-a';
ICO(L,'music',140,480,110,'#F0C77E',@P@);ICO(L,'scent',290,480,110,'#F0C77E',@P@+.2);var ok=MK.el('div','left:400px;top:460px;font-size:90px;color:#F0C77E','✓',L.root);ok.className='mk-a mk-fr';
ICO(L,'music',610,480,110,'#B84A2E',@L@);ICO(L,'scent',760,480,110,'#B84A2E',@L@+.2);var no=MK.el('div','left:870px;top:460px;font-size:90px;color:#B84A2E','✗',L.root);no.className='mk-a mk-fr';
var f1=FIG(L,'@O@',230,760,170,false),f2=FIG(L,'@B@',700,760,170,false);
LBL(L,140,1130,'pas · betah',@P@+.4,{bg:'transparent',c:'#F0C77E',fs:28});LBL(L,610,1130,'kencang · menyengat',@L@+.4,{bg:'transparent',c:'#B84A2E',fs:28});
L.on(function(t){ok.style.opacity=MK.pr(t,@P@+.5,.2);no.style.opacity=MK.pr(t,@L@+.6,.2);SMILE('@O@',.8);BOB('@O@',t,2);
var g=MK.E.io(MK.pr(t,@L@+.8,1.6));SMILE('@B@',-.6);f2.style.transform='translateX('+(g*400)+'px)';f2.style.opacity=1-g*.9;WALK('@B@',t,g>0&&g<1);ARM('@B@','la',g>0?-40:0)});
@SUB@""", P=w18p, L=w18l, O=uo18, B=ub18, SUB=sub(18)), tr=True, dolly=.02)
# 19 aturan 2 Google Maps
w19m, w19f = W(19, 'mata', 2.2), W(19, 'foto', 4.4)
scene(19, R(BP + """
LBL(L,96,300,'ATURAN 2 · ETALASE PERTAMA',.1,{bg:'#C8944A',c:'#0F0E0C',fs:28});
var ph=MK.el('div','left:270px;top:400px;width:540px;height:960px;border:8px solid #F4EBD9;border-radius:60px;background:#1a2230;overflow:hidden',
'<svg viewBox="0 0 540 960" width="540" height="960"><rect width="540" height="960" fill="#e8e1d5"/><g stroke="#cfc6b6" stroke-width="22"><path d="M-20 300 L560 220"/><path d="M180 -20 L260 980"/><path d="M-20 700 L560 760"/></g><rect x="300" y="60" width="160" height="120" fill="#cfe0c8"/></svg>',L.root);ph.className='mk-a';
var pin=MK.el('div','left:470px;top:560px;width:140px;height:140px',IC('pin',140,'#B84A2E'),L.root);pin.className='mk-a';
var cd=MK.el('div','left:300px;top:900px;width:480px;height:420px;background:#F4EBD9;border:4px solid #0F0E0C;border-radius:20px;overflow:hidden',
'<div id="ph19" style="height:250px;background:linear-gradient(#2a2622,#14110e);position:relative"><div style="position:absolute;left:60px;top:60px;width:360px;height:190px;background:#3a332c;border:4px solid #0F0E0C"></div><div id="ph19b" style="position:absolute;left:0;top:0;width:480px;height:250px;opacity:0;background:linear-gradient(#f2d9a6,#e7b878)"><div style="position:absolute;left:60px;top:60px;width:360px;height:190px;background:#C8944A;border:4px solid #0F0E0C;box-shadow:0 0 60px rgba(251,231,184,.9)"></div><div style="position:absolute;left:190px;top:40px;width:100px;height:30px;background:#B84A2E"></div></div></div><div class="mk-fr" style="font-size:40px;padding:18px 24px 0">Tokomu</div><div class="mk-mono" style="font-size:24px;padding:4px 24px;color:#6B6560">foto depan toko</div>',L.root);cd.className='mk-a';
L.on(function(t){var k=MK.E.over(MK.pr(t,@M@-.2,.4));pin.style.transform='translateY('+((1-k)*-200)+'px)';pin.style.opacity=k>0?1:0;var c=MK.E.out(MK.pr(t,@M@+.4,.5));cd.style.transform='translateY('+((1-c)*400)+'px)';cd.style.opacity=c>0?1:0;
var b=document.getElementById('ph19b');if(b)b.style.opacity=MK.pr(t,@F@+.4,.6)});
@SUB@""", M=w19m, F=w19f, SUB=sub(19)), tr=True, dolly=.02)
ev(19, w19m - .2, 'pop'); ev(19, w19f + .4, 'chime')
# 20 penutup: Kardi atau Jono?
w20k, w20j = W(20, 'kardi', 3.0), W(20, 'jono', 4.0)
scene(20, R("""STREET(L,{});
var A=CART(L,40,800,{name:'KARDI',roof:'#6B6560',smoke:'in',front:false});var B=CART(L,640,800,{name:'JONO',front:true,side:'l',smoke:'out',reach:420});
HL(L,'Tokomu yang mana?',.2,{y:300,fs:96});
var q1=LBL(L,140,600,'PAK KARDI ?',@K@-.2,{bg:'#6B6560',fs:40}),q2=LBL(L,700,600,'PAK JONO ?',@J@-.2,{bg:'#B84A2E',fs:40});
@SUB@""", K=w20k, J=w20j, SUB=sub(20)), tr=True, dolly=.03)
ev(20, w20k - .2, 'pop'); ev(20, w20j - .2, 'pop')
# 21 CTA
w21k = W(21, 'komen', 2.9)
scene(21, R("""DARK(L,{bg:'#0F0E0C'});
var dc=MK.el('div','left:290px;top:400px;width:500px;height:640px;background:#F4EBD9;border:6px solid #0F0E0C;border-radius:16px;transform:rotate(-4deg);padding:36px;box-sizing:border-box','<div class="mk-mono" style="font-size:24px;color:#B84A2E">CHECKLIST</div><div class="mk-fr" style="font-size:58px;line-height:1">Sensory<br>Marketing</div><div class="mk-ou" style="font-size:26px;color:#6B6560;margin-top:8px">audit tokomu dari 20 meter</div><div style="margin-top:26px">'+['eye','nose','ear','hand','tongue'].map(function(n){return '<div style="display:flex;align-items:center;gap:16px;margin:8px 0"><div style="width:30px;height:30px;border:4px solid #0F0E0C;border-radius:6px"></div>'+IC(n,46,'#0F0E0C')+'<div style="flex:1;height:12px;background:#E8E1D5;border-radius:6px"></div></div>'}).join('')+'</div>',L.root);dc.className='mk-a';
var bt=MK.el('div','left:170px;top:1120px;width:740px;padding:26px 0;text-align:center;border-radius:999px;background:#B84A2E;color:#F4EBD9;font-size:56px','Komen “SENSORY”',L.root);bt.className='mk-a mk-fr';
L.on(function(t){var k=MK.E.over(MK.pr(t,.1,.5));dc.style.transform='rotate(-4deg) translateY('+((1-k)*200)+'px)';dc.style.opacity=k>0?1:0;var b=MK.pr(t,@K@-.3,.3);bt.style.opacity=b;bt.style.transform='scale('+(.7+.3*MK.E.over(b)+Math.sin(t*5)*.02*b)+')'});
@SUB@""", K=w21k, SUB=sub(21)), tr=True, dolly=.04)
ev(21, .1, 'slide'); ev(21, w21k - .3, 'chime')
html = ('<!DOCTYPE html>\n<html><head><meta charset="utf-8"><title>Fabel Bisnis 04</title><link rel="stylesheet" href="motionkit/fonts-mk.css"></head><body>\n'
        '<script src="motionkit/kit.js"></script>\n<script>\nvar C=MK.C;\nvar FG=' + json.dumps(FIGS) + ';\n' + HELP + FAB + FAB2 + CAFE_JS + FIELD_JS + SATE_JS + '\nMK.run([\n' + ',\n'.join(S) + '\n]);\n</script>\n</body></html>\n')
open(A + 'mk-fabel04.html', 'w', encoding='utf-8').write(html)
json.dump({'duration': tl['duration'], 'events': EV, 'cuts': T0}, open(os.path.join(OUT, 'events.json'), 'w'))
print('ok', len(S), 'adegan', round(sum(DUR), 1), 'dtk'); print([(SC[i][0], DUR[i]) for i in range(len(SC))])
