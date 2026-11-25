"""Fabel Bisnis #01 ekor tikus: animasi penuh Motion Kit dari timing.json vo_prep.
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
SC = [('tim',0,0),('tujuh',0,0),('tim',0,1),
      ('peluit',1,0),('tim',1,1),('tim',1,0),
      ('di',2,0),('makin',2,0),('sebabnya',2,0),
      ('di',3,0),('seminggu',3,0),('semua',3,0),('di',3,0),
      ('perusahaan',4,0),('buat',4,0),('karena',4,0),('mau',4,0)]
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
KEY = {'kalah','posisi','aba','tarik','duluan','ringelmann','kecil','kelihatan','jempol','habis','urus','nama','raci','responsible','accountable','consulted','informed','tenggat','selesai','lapor','narik'}
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

# 0 HOOK: close-up tali tegang -> tarik mundur memperlihatkan lapangan; tim abu jatuh
u0a = [F('h0a%d' % i, 't1') for i in range(8)]; u0b = [F('h0b%d' % i, 't2', True) for i in range(5)]
scene(0, R("""var wrap=MK.el('div','left:0;top:0;width:1080px;height:1920px;transform-origin:540px 1080px','',L.root);wrap.className='mk-a';
FIELD(L,{cheer:8,jump:16});ROPE(L,1080,function(t){return t<2.2?Math.sin(t*30)*6:MK.E.out(MK.pr(t,2.2,1.2))*260});
var A=@A@,B=@B@;var va=A.map(function(u,i){return FIG(L,u,-40+i*62,890,140,false)});var vb=TEAM(L,B,640,95,890,150,true,function(t,i){return t<2.2?6+Math.sin(t*20+i)*3:14});
var ds=[];for(var i=0;i<12;i++){var e=MK.el('div','left:'+(40+i*40)+'px;top:'+(1120+(i%3)*20)+'px;width:80px;height:80px;border-radius:50%;background:rgba(201,143,82,.75)',' ',L.root);e.className='mk-a';ds.push(e)}
Array.prototype.slice.call(L.root.children).forEach(function(n){if(n!==wrap)wrap.appendChild(n)});
var hl=MK.el('div','left:96px;top:250px;width:900px;font-size:100px;line-height:1.02;color:#0F0E0C;text-shadow:0 2px 0 rgba(251,231,184,.6)','Lebih banyak orang,<br><span style="color:#B84A2E">kalah.</span>',L.root);hl.className='mk-a mk-fr';L.headline=true;
L.on(function(t){var z=1+1.3*(1-MK.E.io(MK.pr(t,.4,2.2)));wrap.style.transform='scale('+z+')';
var f=MK.E.out(MK.pr(t,2.6,.5));for(var i=0;i<A.length;i++){ARM(A[i],'la',-70);ARM(A[i],'ra',-75);va[i].style.transform=t<2.6?'rotate('+(-8+Math.sin(t*22+i)*5)+'deg)':'translate('+(f*(200-i*15))+'px,'+(f*110)+'px) rotate('+(f*(70+i*5))+'deg)';SMILE(A[i],t>2.6?-.7:-.2)}
for(var i=0;i<B.length;i++)SMILE(B[i],t>2.6?.9:.3);for(var i=0;i<12;i++){var d=MK.pr(t,2.7,.9);ds[i].style.opacity=d>0?(1-d):0;ds[i].style.transform='scale('+(.4+d*1.6)+')'}
var hk=MK.pr(t,2.6,.15);hl.style.transform='translate('+(t>2.6&&t<2.9?Math.sin(t*90)*6:0)+'px,0)'});""", A=json.dumps(u0a), B=json.dumps(u0b)), dolly=.0)
ev(0, .1, 'slide'); ev(0, 2.6, 'stamp')
# 1 17-an: spanduk lalu tim 1 kacau (tiap orang sibuk sendiri)
u1 = [F('c1%d' % i, 't1') for i in range(10)]
w1t = W(1, 'tim', 1.6)
scene(1, R("""FIELD(L,{cheer:7,jump:14});ROPE(L,1080,function(t){return Math.sin(t*3)*6});
var bn=MK.el('div','left:180px;top:360px;width:720px;padding:20px 0;text-align:center;background:#B84A2E;border:6px solid #0F0E0C;color:#F4EBD9;font-size:64px','LOMBA 17-AN',L.root);bn.className='mk-a mk-fr';
var lb=MK.el('div','left:96px;top:300px;padding:12px 26px;border-radius:999px;background:#6B6560;color:#F4EBD9;font-size:32px','TIM 1 · 10 ORANG · GAK ADA YANG NGATUR',L.root);lb.className='mk-a mk-mono';
var U=@U@;var vv=U.map(function(u,i){return FIG(L,u,10+i*102,860,150,i%3==1)});
var ic=['?','?','!','?'];var qs=[];for(var i=0;i<4;i++){var e=MK.el('div','left:'+(60+i*260)+'px;top:740px;font-size:64px;color:#0F0E0C',ic[i],L.root);e.className='mk-a mk-fr';qs.push(e)}
L.on(function(t){var k=MK.E.over(MK.pr(t,0,.4));bn.style.opacity=t<@T@-.2?1:Math.max(0,1-(t-@T@+.2)*3);bn.style.transform='rotate(-2deg) scale('+(.6+.4*k)+')';lb.style.opacity=MK.pr(t,@T@,.3);
for(var i=0;i<U.length;i++){var on=t>@T@-.3;vv[i].style.opacity=on?1:0;var m=i%4;if(m==0){ARM(U[i],'ra',-150+Math.sin(t*6+i)*20);SMILE(U[i],.8)}else if(m==1){HEAD(U[i],Math.sin(t*5+i)*25);ARM(U[i],'la',-60)}else if(m==2){ARM(U[i],'la',-70);ARM(U[i],'ra',-75);vv[i].style.transform='rotate(-6deg)'}else{LEGS(U[i],t*10,10);ARM(U[i],'la',20)}BOB(U[i],t+i,3)}
for(var i=0;i<4;i++){qs[i].style.opacity=t>@T@+.5?(.5+.5*Math.sin(t*4+i)):0}});
@SUB@""", U=json.dumps(u1), T=w1t, SUB=sub(1)), tr=True, dolly=.04)
ev(1, 0, 'pop')
# 2 tim 2: posisi bernomor di lantai + kapten pakai peluit/aba-aba
u2 = [F('d2%d' % i, 't2', True) for i in range(6)]
w2a = W(2, 'aba', 4.8)
scene(2, R("""FIELD(L,{});ROPE(L,1080,function(t){return 0});
var lb=MK.el('div','left:96px;top:300px;padding:12px 26px;border-radius:999px;background:#C8944A;color:#0F0E0C;font-size:32px','TIM 2 · 6 ORANG · TIAP ORANG PUNYA POSISI',L.root);lb.className='mk-a mk-mono';
var mk=[];for(var i=0;i<6;i++){var e=MK.el('div','left:'+(150+i*125)+'px;top:1200px;width:100px;height:40px;border-radius:50%;border:5px dashed #F4EBD9;text-align:center;color:#F4EBD9;font:800 26px/30px Outfit',''+(i+1),L.root);e.className='mk-a';mk.push(e)}
var U=@U@;var vv=U.map(function(u,i){return FIG(L,u,150+i*125,860,150,true)});
var cap=FIG(L,'@C@',880,780,180,true);var bb=MK.el('div','left:640px;top:540px;width:400px;padding:18px;border-radius:22px;background:#F4EBD9;border:4px solid #0F0E0C;font-size:40px;text-align:center','“Posisi! Ikutin hitungan saya.”',L.root);bb.className='mk-a mk-ou';
L.on(function(t){for(var i=0;i<6;i++){var k=MK.pr(t,.2+i*.25,.3);mk[i].style.opacity=k;var w=MK.E.out(MK.pr(t,.3+i*.25,.5));vv[i].style.opacity=w>0?1:0;vv[i].style.transform='scaleX(-1) translateY('+((1-w)*-80)+'px)';ARM(U[i],'la',-70);ARM(U[i],'ra',-75);SMILE(U[i],.4)}
ARM('@C@','ra',t>@A@-.8?-150+Math.sin(t*8)*12:-20);bb.style.opacity=MK.pr(t,@A@-.8,.3)});
@SUB@""", U=json.dumps(u2), C=F('cap2', 'ref'), A=w2a, SUB=sub(2)), tr=True, dolly=.04)
[ev(2, .2 + i * .25, 'tick') for i in range(0, 6, 2)]
# 3 peluit -> tim 1 menoleh kiri kanan + gelembung pikiran tiap kepala
u3 = [F('e3%d' % i, 't1') for i in range(5)]
w3s = W(3, 'semua', 3.7)
scene(3, R("""FIELD(L,{cheer:4,jump:8});ROPE(L,1100,function(t){return Math.sin(t*2)*8});
var ref=FIG(L,'@R@',420,640,170,false);var wv=MK.el('div','left:600px;top:660px;width:140px;height:140px','<svg viewBox="0 0 70 70" width="140" height="140"><g fill="none" stroke="#0F0E0C" stroke-width="5" stroke-linecap="round"><path d="M10 20 q12 15 0 30"/><path d="M24 10 q20 25 0 50"/></g></svg>',L.root);wv.className='mk-a';
var U=@U@;var vv=U.map(function(u,i){return FIG(L,u,40+i*190,800,220,false)});
var bs=[];var tx=['pasti dia narik','pasti dia kuat','aku santai dikit','yang lain aja','pasti udah kuat'];for(var i=0;i<5;i++){var e=MK.el('div','left:'+(20+i*200)+'px;top:'+(620+(i%2)*70)+'px;width:196px;padding:10px;border-radius:16px;background:#F4EBD9;border:3px solid #0F0E0C;font-size:30px;text-align:center',tx[i],L.root);e.className='mk-a mk-ou';bs.push(e)}
L.on(function(t){ARM('@R@','ra',-120);wv.style.opacity=t<1.4&&Math.floor(t*8)%2?1:0;ref.style.opacity=t<1.6?1:Math.max(0,1-(t-1.6)*3);wv.style.display=t<1.6?'block':'none';
for(var i=0;i<5;i++){HEAD(U[i],Math.sin(t*3+i*1.7)*24);ARM(U[i],'la',-70);ARM(U[i],'ra',-75);var k=MK.pr(t,@S@-.2+i*.18,.3);bs[i].style.opacity=k;bs[i].style.transform='scale('+(.5+.5*MK.E.over(k))+')'}});
@SUB@""", R=F('ref3', 'ref'), U=json.dumps(u3), S=w3s, SUB=sub(3)), tr=True, dolly=.05)
ev(3, 0, 'chime'); [ev(3, w3s - .2 + i * .36, 'pop') for i in range(3)]
u6 = [F('f6%d' % i, 't2', True) for i in range(6)]
wt6 = [W(4, x, d) for x, d in (('satu', 1), ('dua', 1.4), ('tarik', 1.9))]
scene(4, R("""FIELD(L,{cheer:8,jump:20});ROPE(L,1080,function(t){return MK.E.out(MK.pr(t,@T@,1.5))*80});
var U=@U@;var AT=@A@;var vv=TEAM(L,U,170,130,860,170,true,function(t,i){var p=0;for(var k=0;k<3;k++){var q=t-AT[k];if(q>0&&q<.5)p=Math.sin(q/.5*Math.PI)*14}return 4+p+(t>AT[2]?12:0)});
var cn=MK.el('div','left:0;top:360px;width:1080px;text-align:center;font-size:150px;color:#B84A2E;line-height:1','',L.root);cn.className='mk-a mk-fr';
L.on(function(t){var s='';if(t>AT[2])s='TARIK!';else if(t>AT[1])s='2';else if(t>AT[0])s='1';cn.textContent=s;var k=t>AT[2]?MK.pr(t,AT[2],.3):1;cn.style.transform='scale('+(.7+.3*MK.E.over(k))+')';for(var i=0;i<6;i++)SMILE(U[i],.5)});
@SUB@""", U=json.dumps(u6), A=json.dumps(wt6), T=wt6[2], SUB=sub(4)), tr=True, dolly=.06)
[ev(4, a, 'stamp') for a in wt6]
u7a = [F('g7a%d' % i, 't1') for i in range(6)]; u7b = [F('g7b%d' % i, 't2', True) for i in range(4)]
scene(5, R("""FIELD(L,{cheer:9,jump:24});ROPE(L,1080,function(t){return 80+MK.E.io(MK.pr(t,0,1.6))*220});
var A=@A@,B=@B@;var va=A.map(function(u,i){return FIG(L,u,10+i*72,860,150,false)});var vb=TEAM(L,B,650,100,860,150,true,function(t,i){return 14});
var ds=[];for(var i=0;i<10;i++){var e=MK.el('div','left:'+(60+i*45)+'px;top:'+(1120+(i%3)*20)+'px;width:70px;height:70px;border-radius:50%;background:rgba(201,143,82,.7)',' ',L.root);e.className='mk-a';ds.push(e)}
L.on(function(t){var f=MK.E.out(MK.pr(t,@J@-.3,.5));for(var i=0;i<A.length;i++){va[i].style.transform='translate('+(f*(260-i*20))+'px,'+(f*120)+'px) rotate('+(f*(70+i*6))+'deg)';SMILE(A[i],-.6*f)}
for(var i=0;i<10;i++){var d=MK.pr(t,@J@,.8);ds[i].style.opacity=d>0?(1-d)*.9:0;ds[i].style.transform='scale('+(.5+d*1.5)+')'}for(var i=0;i<B.length;i++){vb[i].style.transform='scaleX(-1) translateY('+(t>@J@+.3?-Math.abs(Math.sin(t*8+i))*40:0)+'px)';SMILE(B[i],.9)}});
@SUB@""", A=json.dumps(u7a), B=json.dumps(u7b), J=W(5, 'jatuh', 2), SUB=sub(5)), dolly=.05)
ev(5, W(5, 'jatuh', 2), 'stamp')
# B2 poros
RING = ('<svg viewBox="0 0 260 360" width="300" height="415"><rect x="40" y="200" width="180" height="170" rx="60" fill="#3d3a36"/>'
        '<path d="M110 200 L130 250 L150 200Z" fill="#FBF8F3"/><path d="M118 204 L130 216 L142 204" fill="#0F0E0C"/>'
        '<rect x="112" y="160" width="36" height="40" fill="#F1C9A3"/><circle cx="130" cy="118" r="58" fill="#F1C9A3"/>'
        '<path d="M76 100 Q80 60 130 58 Q180 60 184 100 Q170 80 130 80 Q90 80 76 100Z" fill="#5a4a40"/>'
        '<path d="M100 146 Q130 168 160 146 Q150 160 130 162 Q110 160 100 146Z" fill="#5a4a40"/>'
        '<circle cx="110" cy="118" r="5" fill="#0F0E0C"/><circle cx="150" cy="118" r="5" fill="#0F0E0C"/>'
        '<g transform="rotate(-6 200 300)"><path d="M150 300 H250" stroke="#b98d55" stroke-width="14" stroke-linecap="round"/><path d="M150 300 H250" stroke="#5a3b24" stroke-width="2"/></g></svg>')
scene(6, R("""DARK(L,{bg:'#080706'});
var sp=MK.el('div','left:190px;top:0;width:700px;height:1500px;background:linear-gradient(rgba(244,235,217,.14),rgba(244,235,217,0));clip-path:polygon(40% 0,60% 0,100% 100%,0 100%)',' ',L.root);sp.className='mk-a';
var fr=MK.el('div','left:96px;top:330px;width:888px;height:900px;border-radius:24px;background:#F4EBD9;border:6px solid #0F0E0C;box-shadow:0 40px 80px -30px rgba(0,0,0,.8)',' ',L.root);fr.className='mk-a';
var tg=MK.el('div','left:140px;top:370px;font-size:26px;letter-spacing:.1em;color:#B84A2E','KARTU TOKOH',L.root);tg.className='mk-a mk-mono';
var pt=MK.el('div','left:390px;top:410px;width:300px;height:415px',@G@,L.root);pt.className='mk-a';
var nm=MK.el('div','left:140px;top:850px;width:800px;text-align:center;font-size:56px;white-space:nowrap;line-height:1;color:#0F0E0C','MAXIMILIEN RINGELMANN',L.root);nm.className='mk-a mk-fr';
var s1=MK.el('div','left:140px;top:940px;width:800px;text-align:center;font-size:34px;color:#0F0E0C','Insinyur pertanian (1861–1931)',L.root);s1.className='mk-a mk-ou';
var s2=MK.el('div','left:140px;top:990px;width:800px;text-align:center;font-size:34px;color:#B84A2E','Percobaan menarik tali bersama',L.root);s2.className='mk-a mk-ou';
var E=@E@;L.on(function(t){sp.style.opacity=MK.pr(t,.1,.6);var k=MK.E.over(MK.pr(t,E-.2,.5));[fr,tg,pt,nm,s1,s2].forEach(function(e,i){e.style.opacity=t<E-.2?0:MK.pr(t,E-.2+i*.1,.3)});fr.style.transform='rotate(-1.5deg) scale('+(.8+.2*k)+')';pt.style.transform='translateY('+((1-k)*60)+'px)'});
@SUB@""", G=json.dumps(RING), E=W(6, 'efek', 2.6), SUB=sub(6)), tr=True, dolly=.05)
ev(6, .1, 'sweep'); ev(6, W(6, 'efek', 2.6) - .2, 'stamp')
scene(7, R("""DARK(L);
var hd=MK.el('div','left:96px;top:300px;width:888px;font-size:30px;color:#9a9590','TENAGA TIAP ORANG · PERCOBAAN RINGELMANN',L.root);hd.className='mk-a mk-mono';
var G=[[1,100],[3,85],[8,49]],rows=[];
for(var g=0;g<3;g++){var n=G[g][0],y=430+g*330;var lb=MK.el('div','left:96px;top:'+(y+150)+'px;font-size:44px;color:#F4EBD9',n+' orang',L.root);lb.className='mk-a mk-fr';
 var fs=[];for(var i=0;i<n;i++){var x=330+i*82;var f=MK.el('div','left:'+x+'px;top:'+(y+90)+'px;width:70px;height:150px','<svg viewBox="0 0 70 150" width="70" height="150"><circle cx="35" cy="24" r="20" fill="#F1C9A3" stroke="#0F0E0C" stroke-width="4"/><path d="M14 150 V70 Q14 50 35 50 Q56 50 56 70 V150Z" fill="'+(g==2?'#8a6a45':'#C8944A')+'" stroke="#0F0E0C" stroke-width="4"/></svg>',L.root);f.className='mk-a';
  var m=MK.el('div','left:'+(x+5)+'px;top:'+(y+50)+'px;width:60px;height:22px;border:3px solid #F4EBD9;border-radius:6px;overflow:hidden','<div style="height:100%;width:100%;background:#C8944A;transform-origin:left"></div>',L.root);m.className='mk-a';fs.push([f,m])}
 var pc=MK.el('div','left:'+(330+n*82+20)+'px;top:'+(y+120)+'px;font-size:64px;color:'+(g==2?'#B84A2E':'#F4EBD9'),'0%',L.root);pc.className='mk-a mk-fr';if(g==2){pc.style.left='96px';pc.style.top=(y+210)+'px'}
 rows.push([fs,pc,G[g][1]])}
var ft=MK.el('div','left:96px;top:1420px;width:888px;font-size:26px;color:#6B6560','Ringelmann (1913): 8 orang menarik ≈ 49% tenaga per orang',L.root);ft.className='mk-a mk-mono';
L.on(function(t){rows.forEach(function(r,g){var k=MK.E.out(MK.pr(t,.2+g*1.0,.6)),v=100-(100-r[2])*MK.E.io(MK.pr(t,.5+g*1.0,.7));
 r[0].forEach(function(p,i){p[0].style.opacity=k;p[0].style.transform='translateY('+((1-k)*40)+'px)';p[1].style.opacity=k;p[1].firstChild.style.transform='scaleX('+(v/100)+')';p[1].firstChild.style.background=v<60?'#B84A2E':'#C8944A'});
 r[1].style.opacity=k;r[1].textContent=Math.round(v)+'%'});ft.style.opacity=MK.pr(t,2.8,.4)});
@SUB@""", SUB=sub(7)), dolly=.03)
[ev(7, .2 + g * .9, 'pop') for g in range(3)]
u10 = [F('k10%d' % i, 't1') for i in range(5)]
scene(8, R("""FIELD(L,{cheer:2,jump:4});ROPE(L,1100,function(t){return 0});
var U=@U@;var vv=TEAM(L,U,40,190,780,230,false,function(t,i){return i==2?2:-8});
var sp=MK.el('div','left:390px;top:560px;width:300px;height:900px;border-radius:50%;background:radial-gradient(rgba(255,255,255,.35),rgba(255,255,255,0) 70%)',' ',L.root);sp.className='mk-a';
var th=MK.el('div','left:430px;top:380px;width:600px;padding:18px 24px;border-radius:24px;background:#F4EBD9;border:4px solid #0F0E0C;font-size:40px','“gak kelihatan juga<br>kalau aku kurang narik”',L.root);th.className='mk-a mk-fri';
L.on(function(t){ARM(U[2],'la',-20);ARM(U[2],'ra',-20);SMILE(U[2],.4);HEAD(U[2],Math.sin(t*2)*8);th.style.opacity=MK.pr(t,@K@-.6,.4);sp.style.opacity=MK.pr(t,.2,.5)});
@SUB@""", U=json.dumps(u10), K=W(8, 'gak', 2.7), SUB=sub(8)), dolly=.07)
# B3 cetak biru
scene(9, R(BP + """
var ph=MK.el('div','left:240px;top:380px;width:600px;height:920px;border:6px solid #F4EBD9;border-radius:56px',' ',L.root);ph.className='mk-a';
var hd=MK.el('div','left:300px;top:440px;font-size:28px;color:#F4EBD9','GRUP WA · TIM (8)',L.root);hd.className='mk-a mk-mono';
BUB(L,290,540,480,'Stok produk terlaris<br>tinggal 12 pcs ya.',@N@,'#F4EBD9');
var th=[];for(var i=0;i<8;i++){var e=MK.el('div','left:'+(300+i*58)+'px;top:740px;font-size:44px','👍',L.root);e.className='mk-a';th.push(e)}
var rd=MK.el('div','left:300px;top:820px;font-size:28px;color:#9a9590','dibaca 8 · dibalas 0',L.root);rd.className='mk-a mk-mono';
L.on(function(t){for(var i=0;i<8;i++){var k=MK.pr(t,@J@-.6+i*.12,.2);th[i].style.opacity=k;th[i].style.transform='scale('+(.4+.6*MK.E.over(k))+')'}rd.style.opacity=MK.pr(t,@J@+.6,.3)});
@SUB@""", N=W(9, 'ada', 3), J=W(9, 'jempol', 7), SUB=sub(9)), tr=True, dolly=.04)
[ev(9, W(9, 'jempol', 7) - .6 + i * .24, 'tick') for i in range(4)]
scene(10, R(BP + """
var cal=MK.el('div','left:96px;top:330px;width:260px;height:260px;background:#F4EBD9;border:5px solid #0F0E0C;border-radius:12px;overflow:hidden;text-align:center','<div style="height:56px;background:#B84A2E"></div><div class="mk-mono" style="font-size:24px;margin-top:10px">HARI KE</div><div id="d12" class="mk-fr" style="font-size:96px;line-height:1">1</div>',L.root);cal.className='mk-a';
var sh=MK.el('div','left:440px;top:500px;width:520px;height:620px',LINE(260,310,'<path d="M10 300 V10 H250 V300 M10 100 H250 M10 200 H250"/>'),L.root);sh.className='mk-a';sh.firstChild.setAttribute('width',520);sh.firstChild.setAttribute('height',620);
var bx=[];for(var i=0;i<9;i++){var e=MK.el('div','left:'+(470+(i%3)*160)+'px;top:'+(560+Math.floor(i/3)*200)+'px;width:120px;height:120px;background:#C8944A;border:4px solid #0F0E0C;border-radius:8px',' ',L.root);e.className='mk-a';bx.push(e)}
var hb=MK.el('div','left:520px;top:1150px;padding:12px 30px;border:7px solid #B84A2E;border-radius:12px;color:#B84A2E;font-size:70px;transform:rotate(-6deg)','HABIS',L.root);hb.className='mk-a mk-fr';
L.on(function(t){var d=$('d12');if(d)d.textContent=Math.min(7,1+Math.floor(t*4));for(var i=0;i<9;i++)bx[i].style.opacity=t>.3+i*.15?0:1;var k=MK.pr(t,@H@,.2);hb.style.opacity=k;hb.style.transform='rotate(-6deg) scale('+(1.4-.4*k)+')'});
@SUB@""", H=W(10, 'habis', 1.6), SUB=sub(10)), dolly=.05)
ev(10, W(10, 'habis', 1.6), 'stamp')
scene(11, R(BP + """
var fs=[];for(var i=0;i<4;i++){var e=""" + LF(0, 0, 1.6) + """;e.className='mk-a';e.firstChild.setAttribute('width',160);e.firstChild.setAttribute('height',320);e.style.left=(80+i*240)+'px';e.style.top='860px';fs.push(e)}
var bb=[];for(var i=0;i<4;i++){var e=MK.el('div','left:'+(40+i*240)+'px;top:'+(640+(i%2)*60)+'px;width:230px;padding:14px;border-radius:20px;background:#1f2630;border:3px solid #F4EBD9;color:#F4EBD9;font-size:28px;text-align:center','pasti udah ada yang urus',L.root);e.className='mk-a mk-ou';bb.push(e)}
L.on(function(t){for(var i=0;i<4;i++){bb[i].style.opacity=MK.pr(t,.2+i*.3,.3);fs[i].style.transform='translateY('+(Math.sin(t*2+i)*4)+'px)'}});
@SUB@""", SUB=sub(11)), tr=True, dolly=.04)
scene(12, R(BP + """
var st=MK.el('div','left:96px;top:330px;padding:16px 28px;border:6px solid #C8944A;border-radius:12px;color:#C8944A;font-size:40px;transform:rotate(-3deg)','DARI BISNIS YANG SAYA DAMPINGI',L.root);st.className='mk-a mk-fr';
var rows=['Order ulang stok','Balas chat','Posting konten'],h='<div style="display:flex;font:28px JetBrains Mono,monospace;color:#9a9590;border-bottom:3px solid #F4EBD9;padding:10px 0"><div style="width:420px">PEKERJAAN</div><div>NAMA</div></div>';
for(var i=0;i<3;i++)h+='<div style="display:flex;font:38px Outfit,sans-serif;color:#F4EBD9;border-bottom:2px solid rgba(244,235,217,.3);padding:18px 0"><div style="width:420px">'+rows[i]+'</div><div class="q" style="color:#B84A2E">?</div></div>';
var tb=MK.el('div','left:96px;top:560px;width:888px',h,L.root);tb.className='mk-a';
var lo=MK.el('div','left:96px;top:1080px;width:888px;font-size:60px;color:#F4EBD9;line-height:1.05','Masalahnya,<br><span style="color:#C8944A">pekerjaan gak punya nama.</span>',L.root);lo.className='mk-a mk-fr';
L.on(function(t){var k=MK.pr(t,.1,.25);st.style.opacity=k;st.style.transform='rotate(-3deg) scale('+(1.3-.3*MK.E.out(k))+')';tb.style.opacity=MK.pr(t,.8,.4);var q=tb.querySelectorAll('.q');for(var i=0;i<q.length;i++)q[i].style.opacity=Math.floor(t*2+i)%2?1:.3;lo.style.opacity=MK.pr(t,@M@-.3,.4)});
@SUB@""", M=W(12, 'masalahnya', 3.8), SUB=sub(12)), tr=True, dolly=.04)
ev(12, .1, 'stamp')
# B4 RACI
wr = [W(13, x, d) for x, d in (('responsible', 2.3), ('accountable', 4.6), ('consulted', 7.1), ('informed', 9.7))]
RI = ['<path d="M20 70 L40 40 L60 56 L80 24" fill="none" stroke="#0F0E0C" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><circle cx="80" cy="24" r="8" fill="#0F0E0C"/>',
      '<rect x="26" y="20" width="48" height="34" rx="6" fill="#0F0E0C"/><rect x="16" y="54" width="68" height="16" rx="4" fill="#0F0E0C"/><rect x="12" y="76" width="76" height="8" fill="#B84A2E"/>',
      '<path d="M12 14 h76 v50 H44 l-18 16 V64 H12z" fill="none" stroke="#0F0E0C" stroke-width="7" stroke-linejoin="round"/>',
      '<path d="M50 14 q26 4 26 34 v16 l8 10 H16 l8 -10 V48 q0 -30 26 -34z" fill="none" stroke="#0F0E0C" stroke-width="7" stroke-linejoin="round"/><circle cx="50" cy="84" r="7" fill="#0F0E0C"/>']
RL = [('R', 'Responsible', 'yang mengerjakan'), ('A', 'Accountable', 'yang menanggung hasil'), ('C', 'Consulted', 'yang dimintai pendapat'), ('I', 'Informed', 'yang cukup dikabari')]
RX = ['Rani: order ulang stok', 'Owner: pastikan stok aman', 'Admin gudang: cek sisa', 'Tim CS: kabari pembeli']
b15 = BP + "var hd=MK.el('div','left:96px;top:300px;width:888px;font-size:56px;color:#F4EBD9','Matriks <span style=\"color:#C8944A\">RACI</span>',L.root);hd.className='mk-a mk-fr';var hx=MK.el('div','left:96px;top:375px;font-size:28px;color:#9a9590','CONTOH: STOK PRODUK TERLARIS',L.root);hx.className='mk-a mk-mono';"
for j, ((ch, en, idn), ic, at, ex) in enumerate(zip(RL, RI, wr, RX)):
    x, y = 96 + (j % 2) * 458, 420 + (j // 2) * 470
    b15 += R("""P(L,@X@,@Y@,430,440,'<div style="width:430px;height:440px;border-radius:22px;background:#F4EBD9;border:6px solid #0F0E0C;padding:26px;box-sizing:border-box"><div style="display:flex;justify-content:space-between;align-items:flex-start"><div class="mk-fr" style="font-size:150px;line-height:.9;color:#B84A2E">@C@</div><svg viewBox="0 0 100 100" width="120" height="120">@I@</svg></div><div class="mk-fr" style="font-size:44px;margin-top:20px">@E@</div><div class="mk-ou" style="font-size:32px;color:#6B6560;margin-top:6px">@D@</div><div class="mk-mono" style="font-size:22px;margin-top:16px;padding:8px 12px;border-radius:10px;background:#0F0E0C;color:#F4EBD9">@K@</div></div>',@A@);""",
             X=x, Y=y, C=ch, I=ic, E=en, D=idn, A=at, K=ex)
    ev(13, at, 'pop')
scene(13, b15 + sub(13), tr=True, dolly=.03)
wk = [W(14, x, d) for x, d in (('nama', 4.3), ('tenggat', 5.3), ('ukuran', 6.2), ('tempat', 7.6))]
scene(14, R("""DARK(L,{bg:'#101317'});
var cd=MK.el('div','left:96px;top:400px;width:888px;padding:36px 40px;border-radius:20px;background:#F4EBD9;border:6px solid #0F0E0C;box-sizing:border-box','<div class="mk-mono" style="font-size:26px;color:#6B6560">KARTU TUGAS</div><div class="mk-fr" style="font-size:58px;margin:6px 0 24px">Order ulang stok terlaris</div><div id="rw16"></div>',L.root);cd.className='mk-a';
var K=['NAMA','TENGGAT','UKURAN SELESAI','TEMPAT LAPOR'],V=['Rani','Kamis, 15.00','PO terkirim ke supplier','Grup WA + foto PO'],A=@A@;
var sx=MK.el('div','left:390px;top:600px;font-size:44px;color:#9a9590;text-decoration:line-through','tim gudang',L.root);sx.className='mk-a mk-ou';
L.on(function(t){var w=$('rw16');if(!w)return;var h='';for(var i=0;i<4;i++){if(t<A[i]-.1)break;var p=Math.min(1,(t-A[i]+.1)/.6),s=V[i];h+='<div style="display:flex;gap:20px;align-items:baseline;margin:16px 0;border-bottom:2px dashed rgba(15,14,12,.25);padding-bottom:10px"><div class="mk-mono" style="width:300px;font-size:26px;color:#B84A2E">'+K[i]+'</div><div style="font:44px Caveat,Outfit,sans-serif">'+s.slice(0,Math.ceil(s.length*p))+'</div></div>'}w.innerHTML=h;sx.style.opacity=t>A[0]-.6&&t<A[0]+.1?1:0});
@SUB@""", A=json.dumps(wk), SUB=sub(14)), tr=True, dolly=.04)
[ev(14, a, 'tick') for a in wk]
u17 = [F('n17%d' % i, 't2', True) for i in range(5)]
scene(15, R("""FIELD(L,{cheer:3,jump:6});ROPE(L,1080,function(t){return 0});
var U=@U@;var vv=TEAM(L,U,150,160,860,170,true,function(t,i){return 8});
var NM=['Rani','Dodi','Sari','Bima','Tia'];for(var i=0;i<5;i++){var e=MK.el('div','left:'+(150+i*160+30)+'px;top:1140px;padding:6px 14px;border-radius:999px;background:#0F0E0C;color:#F4EBD9;font-size:26px','@'+NM[i],L.root);e.className='mk-a mk-mono'}
var q=MK.el('div','left:96px;top:290px;width:888px;text-align:center;font-size:84px;line-height:1.04;color:#0F0E0C','Siapa yang<br><span style="color:#B84A2E">benar-benar narik?</span>',L.root);q.className='mk-a mk-fr';
L.on(function(t){q.style.opacity=MK.pr(t,@S@-.4,.4)});
@SUB@""", U=json.dumps(u17), S=W(15, 'siapa', 2.2), SUB=sub(15)), tr=True, dolly=.05)
scene(16, R("""DARK(L,{bg:'#0F0E0C'});
var dc=MK.el('div','left:300px;top:420px;width:480px;height:620px;background:#F4EBD9;border:6px solid #0F0E0C;border-radius:16px;transform:rotate(-4deg);padding:36px;box-sizing:border-box','<div class="mk-mono" style="font-size:24px;color:#B84A2E">PANDUAN</div><div class="mk-fr" style="font-size:64px;line-height:1">RACI</div><div class="mk-ou" style="font-size:28px;color:#6B6560;margin-top:8px">siap dipakai tim</div><div style="margin-top:30px">'+[0,1,2,3,4].map(function(){return '<div style="height:16px;background:#E8E1D5;margin:14px 0;border-radius:6px"></div>'}).join('')+'</div>',L.root);dc.className='mk-a';
var bt=MK.el('div','left:200px;top:1120px;width:680px;padding:26px 0;text-align:center;border-radius:999px;background:#B84A2E;color:#F4EBD9;font-size:56px','Komen “RACI”',L.root);bt.className='mk-a mk-fr';
L.on(function(t){var k=MK.E.over(MK.pr(t,.1,.5));dc.style.transform='rotate(-4deg) translateY('+((1-k)*200)+'px)';dc.style.opacity=k>0?1:0;var b=MK.pr(t,@K@-.3,.3);bt.style.opacity=b;bt.style.transform='scale('+(.7+.3*MK.E.over(b)+Math.sin(t*5)*.02*b)+')'});
@SUB@""", K=W(16, 'komen', 2.5), SUB=sub(16)), tr=True, dolly=.04)
ev(16, .1, 'slide'); ev(16, W(16, 'komen', 2.5) - .3, 'chime')
html = ('<!DOCTYPE html>\n<html><head><meta charset="utf-8"><title>Fabel Bisnis 03</title><link rel="stylesheet" href="motionkit/fonts-mk.css"></head><body>\n'
        '<script src="motionkit/kit.js"></script>\n<script>\nvar C=MK.C;\nvar FG=' + json.dumps(FIGS) + ';\n' + HELP + FAB + FAB2 + CAFE_JS + FIELD_JS + '\nMK.run([\n' + ',\n'.join(S) + '\n]);\n</script>\n</body></html>\n')
open(A + 'mk-fabel03b.html', 'w', encoding='utf-8').write(html)
json.dump({'duration': tl['duration'], 'events': EV, 'cuts': T0}, open(os.path.join(OUT, 'events.json'), 'w'))
print('ok', len(S), 'adegan', round(sum(DUR), 1), 'dtk'); print([(SC[i][0], DUR[i]) for i in range(len(SC))])
