/* Motion Kit "Tinta & Kertas" - The Brand Fixer (skill brand-fixer-reels-system v1, 17 Nov 2026)
   Dirender oleh animatic/render-animatic.js lewat window.seek(t) + window.ANIMATIC_DURATION.
   Pakai: <script src="motionkit/kit.js"></script> lalu MK.run([{dur, tr, build:function(L){...}}, ...])
   Aturan yang dijaga kit: hard cut bawaan, transisi resmi saja (cut | sweep | stamp), satu lapis teks
   (MK.subtitle otomatis disembunyikan saat adegan memasang headline), garis "boil" 12 fps, teks halus 30 fps,
   tanpa Math.random (deterministik). */
(function () {
  var C = { white: '#FBF8F3', cream: '#F4EBD9', ink: '#0F0E0C', soft: '#2A2824', terra: '#B84A2E', amber: '#C8944A', gray: '#6B6560' };
  var W = 1080, H = 1920, FPS = 30;
  var NS = 'http://www.w3.org/2000/svg';
  function $(id) { return document.getElementById(id); }
  function cl(x) { return x < 0 ? 0 : x > 1 ? 1 : x; }
  function pr(t, a, d) { return cl((t - a) / d); }
  var E = {
    out: function (k) { return 1 - Math.pow(1 - k, 3); },
    io: function (k) { return k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; },
    over: function (k) { var s = 1.03; return k >= 1 ? 1 : (k < .8 ? E.out(k / .8) * s : s - (s - 1) * E.io((k - .8) / .2)); }
  };
  function rng(seed) { var s = seed >>> 0 || 1; return function () { s ^= s << 13; s ^= s >>> 17; s ^= s << 5; return ((s >>> 0) % 100000) / 100000; }; }
  function el(tag, css, html, parent) { var e = document.createElement(tag); if (css) e.style.cssText = css; if (html != null) e.innerHTML = html; (parent || document.body).appendChild(e); return e; }
  function svg(tag, attrs, parent) { var e = document.createElementNS(NS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; }

  /* ---------- gaya dasar ---------- */
  var css = el('style', '', '', document.head);
  css.textContent = [
    'html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:' + C.cream + '}',
    '.mk-stage{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden}',
    '.mk-shot{position:absolute;left:0;top:0;width:1080px;height:1920px;visibility:hidden}',
    '.mk-a{position:absolute}',
    '.mk-fr{font-family:Fraunces,serif;font-weight:700;letter-spacing:-.01em}',
    '.mk-fri{font-family:Fraunces,serif;font-style:italic;font-weight:400}',
    '.mk-ou{font-family:Outfit,sans-serif;font-weight:600}',
    '.mk-mono{font-family:"JetBrains Mono",monospace;font-weight:500;letter-spacing:.06em;text-transform:uppercase}',
    '.mk-card{background:' + C.white + ';border-radius:10px;box-shadow:0 2px 0 rgba(15,14,12,.06),0 18px 40px -18px rgba(15,14,12,.35)}'
  ].join('');

  /* ---------- tekstur kertas + grain ---------- */
  function paperDataURL(seed, base, fiber) {
    var cv = document.createElement('canvas'); cv.width = 540; cv.height = 960; var g = cv.getContext('2d');
    g.fillStyle = base; g.fillRect(0, 0, 540, 960);
    var r = rng(seed), img = g.getImageData(0, 0, 540, 960), d = img.data;
    for (var i = 0; i < d.length; i += 4) { var n = (r() - .5) * 14; d[i] += n; d[i + 1] += n; d[i + 2] += n * .9; }
    g.putImageData(img, 0, 0);
    g.globalAlpha = fiber; g.strokeStyle = '#8a7a62';
    for (var k = 0; k < 900; k++) { var x = r() * 540, y = r() * 960, a = r() * 6.28, l = 4 + r() * 16; g.lineWidth = .4 + r() * .6; g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + Math.cos(a) * l * .5 + (r() - .5) * 4, y + Math.sin(a) * l * .5, x + Math.cos(a) * l, y + Math.sin(a) * l); g.stroke(); }
    g.globalAlpha = 1;
    var grd = g.createRadialGradient(270, 420, 120, 270, 480, 760); grd.addColorStop(0, 'rgba(255,255,255,0)'); grd.addColorStop(1, 'rgba(80,60,30,.16)');
    g.fillStyle = grd; g.fillRect(0, 0, 540, 960);
    return cv.toDataURL('image/jpeg', .9);
  }
  var GRAIN = [];
  function grainFrames() {
    for (var f = 0; f < 4; f++) {
      var cv = document.createElement('canvas'); cv.width = 360; cv.height = 640; var g = cv.getContext('2d'), img = g.createImageData(360, 640), d = img.data, r = rng(91 + f * 7);
      for (var i = 0; i < d.length; i += 4) { var v = r() * 255; d[i] = d[i + 1] = d[i + 2] = v; d[i + 3] = 255; }
      g.putImageData(img, 0, 0); GRAIN.push(cv.toDataURL('image/png'));
    }
  }

  /* ---------- filter "boil" (garis bergetar 1-2 px, ganti tiap 2 frame = 12 fps) ---------- */
  var defs;
  function boilDefs() {
    var s = svg('svg', { width: 0, height: 0, style: 'position:absolute' }, document.body);
    defs = svg('defs', {}, s);
    for (var i = 0; i < 6; i++) {
      var f = svg('filter', { id: 'boil' + i, x: '-5%', y: '-5%', width: '110%', height: '110%' }, defs);
      svg('feTurbulence', { type: 'fractalNoise', baseFrequency: '0.035', numOctaves: '2', seed: String(i * 13 + 3), result: 'n' }, f);
      svg('feDisplacementMap', { in: 'SourceGraphic', in2: 'n', scale: '3.2', xChannelSelector: 'R', yChannelSelector: 'G' }, f);
    }
    var m = svg('filter', { id: 'marker', x: '-5%', y: '-5%', width: '110%', height: '110%' }, defs);
    svg('feTurbulence', { type: 'fractalNoise', baseFrequency: '0.9', numOctaves: '1', seed: '5', result: 't' }, m);
    svg('feColorMatrix', { in: 't', type: 'matrix', values: '0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.1 1.35', result: 'a' }, m);
    svg('feComposite', { in: 'SourceGraphic', in2: 'a', operator: 'in' }, m);
  }
  function boilId(t) { return 'url(#boil' + (Math.floor(t * 12) % 6) + ')'; }

  /* ---------- komponen ---------- */
  // Teks headline (satu lapis teks: memasang headline menyembunyikan subtitle)
  function Headline(L, o) {
    var e = el('div', 'left:' + (o.x || 96) + 'px;top:' + (o.y || 330) + 'px;width:' + (o.w || 888) + 'px;font-size:' + (o.size || 104) + 'px;line-height:1.02;color:' + (o.color || C.ink), o.html, L.root);
    e.className = 'mk-a mk-fr'; L.headline = true;
    L.on(function (t) { var k = o.at == null ? 1 : pr(t, o.at, .35); e.style.opacity = o.at == null ? 1 : k; e.style.transform = o.at == null ? 'none' : 'translateY(' + ((1 - E.out(k)) * 24) + 'px)'; });
    return e;
  }
  // Subtitle editorial Outfit 60 px, 2-4 kata, kata kunci terracotta
  function Subtitle(L, chunks, o) {
    o = o || {};
    var e = el('div', 'left:96px;right:96px;top:' + (o.y || 1440) + 'px;text-align:center;font-size:62px;line-height:1.15;color:' + (o.color || C.ink) + ';text-shadow:' + (o.dark ? '0 2px 12px rgba(0,0,0,.45)' : 'none'), '', L.root);
    e.className = 'mk-a mk-ou';
    L.on(function (t) {
      if (L.headline && !o.force) { e.style.opacity = 0; return; }
      var cur = null; for (var i = 0; i < chunks.length; i++) if (t >= chunks[i][0]) cur = chunks[i];
      if (!cur) { e.innerHTML = ''; return; }
      e.innerHTML = cur[1].replace(/\*(.+?)\*/g, '<span style="color:' + C.terra + '">$1</span>').replace(/_(.+?)_/g, '<span class="mk-fri">$1</span>');
      e.style.opacity = 1;
    });
    return e;
  }
  // Hitung naik: Rp / % (Fraunces untuk angka, Outfit untuk satuan)
  function CountUp(L, o) {
    var e = el('div', 'left:' + o.x + 'px;top:' + o.y + 'px;white-space:nowrap;color:' + (o.color || C.ink), '', L.root); e.className = 'mk-a';
    function fmt(v) { return Math.round(v).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.'); }
    L.on(function (t) {
      var k = o.at == null ? 1 : E.out(pr(t, o.at, o.dur || .8));
      e.innerHTML = (o.prefix ? '<span class="mk-ou" style="font-size:' + (o.size * .42) + 'px;vertical-align:.9em;margin-right:10px">' + o.prefix + '</span>' : '') +
        '<span class="mk-fr" style="font-size:' + o.size + 'px">' + fmt(o.from + (o.to - o.from) * k) + '</span>' +
        (o.suffix ? '<span class="mk-ou" style="font-size:' + (o.size * .38) + 'px;margin-left:14px">' + o.suffix + '</span>' : '');
      e.style.opacity = o.at == null ? 1 : cl((t - o.at) * 8);
    });
    return e;
  }
  // Kartu kertas: masuk geser + rotasi kecil + overshoot 3%, 0,35 dtk
  function PaperCard(L, o) {
    var e = el('div', 'left:' + o.x + 'px;top:' + o.y + 'px;width:' + o.w + 'px;padding:34px 40px', o.html, L.root); e.className = 'mk-a mk-card';
    var rot = o.rot == null ? -1.5 : o.rot, from = o.from || 'right';
    L.on(function (t) {
      var k = pr(t, o.at || 0, .35), v = E.over(k), dx = from === 'left' ? -1 : from === 'right' ? 1 : 0, dy = from === 'bottom' ? 1 : 0;
      e.style.opacity = k > 0 ? 1 : 0;
      e.style.transform = 'translate(' + ((1 - v) * dx * 700) + 'px,' + ((1 - v) * dy * 900) + 'px) rotate(' + (rot + (1 - v) * 4 * (dx || 1)) + 'deg)';
    });
    return e;
  }
  // Garis tinta merambat (path SVG), boil 12 fps
  function InkPath(L, o) {
    var s = svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'position:absolute;left:0;top:0;overflow:visible' }, L.root);
    var p = svg('path', { d: o.d, fill: 'none', stroke: o.color || C.ink, 'stroke-width': o.w || 8, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, s);
    if (o.marker) p.setAttribute('filter', 'url(#marker)');
    var len = 0;
    L.on(function (t) {
      if (!len) { len = p.getTotalLength(); p.style.strokeDasharray = len; }
      var k = E.out(pr(t, o.at || 0, o.dur || .55));
      p.style.strokeDashoffset = len * (1 - k); p.style.opacity = t >= (o.at || 0) ? 1 : 0;
      if (!o.marker) s.style.filter = boilId(t);
    });
    return p;
  }
  // Lingkar spidol di sekitar kotak (x,y,w,h), 0,3-0,45 dtk
  function MarkerCircle(L, o) {
    var cx = o.x + o.w / 2, cy = o.y + o.h / 2, rx = o.w / 2 + 26, ry = o.h / 2 + 22, r = rng(o.seed || 7), pts = [];
    for (var i = 0; i <= 26; i++) { var a = -2.2 + i / 26 * 6.9, j = 1 + (r() - .5) * .06; pts.push((cx + Math.cos(a) * rx * j).toFixed(1) + ' ' + (cy + Math.sin(a) * ry * j).toFixed(1)); }
    return InkPath(L, { d: 'M' + pts.join(' L'), color: C.terra, w: 9, at: o.at, dur: o.dur || .4, marker: true });
  }
  function MarkerStrike(L, o) { return InkPath(L, { d: 'M' + (o.x - 10) + ' ' + (o.y + o.h * .55) + ' Q' + (o.x + o.w / 2) + ' ' + (o.y + o.h * .45) + ' ' + (o.x + o.w + 10) + ' ' + (o.y + o.h * .5), color: C.terra, w: 10, at: o.at, dur: .3, marker: true }); }
  // Stabilo amber 40% di belakang kata (kiri ke kanan 0,25 dtk)
  function Highlighter(L, o) {
    var e = el('div', 'left:' + o.x + 'px;top:' + o.y + 'px;width:' + o.w + 'px;height:' + o.h + 'px;background:rgba(200,148,74,.4);border-radius:6px;transform-origin:left;z-index:-1', '', o.parent || L.root); e.className = 'mk-a';
    L.on(function (t) { var k = E.out(pr(t, o.at, .25)); e.style.transform = 'scaleX(' + k + ') skewX(-6deg)'; e.style.opacity = k > 0 ? 1 : 0; });
    return e;
  }
  // Cap "BOCOR DI SINI": skala 1,35 -> 1 dalam 4 frame, guncang 2 frame +-6 px, percikan tinta
  function StampBocor(L, o) {
    var e = el('div', 'left:' + o.x + 'px;top:' + o.y + 'px;padding:14px 30px;border:9px solid ' + C.terra + ';border-radius:16px;color:' + C.terra + ';font-size:' + (o.size || 64) + 'px;line-height:1;white-space:nowrap;filter:url(#marker)', o.text || 'BOCOR DI SINI', L.root);
    e.className = 'mk-a mk-fr';
    var r = rng(o.seed || 11), dots = [];
    for (var i = 0; i < 9; i++) { var d = el('div', 'width:' + (6 + r() * 14) + 'px;height:' + (6 + r() * 14) + 'px;border-radius:50%;background:' + C.terra + ';left:' + (o.x + r() * 420) + 'px;top:' + (o.y - 30 + r() * 150) + 'px', '', L.root); d.className = 'mk-a'; dots.push(d); }
    L.stampAt = o.at;
    L.on(function (t) {
      var f = (t - o.at) * FPS, on = f >= 0;
      var s = !on ? 1.35 : f < 4 ? 1.35 - .35 * (f / 4) : 1;
      e.style.opacity = on ? 1 : 0; e.style.transform = 'rotate(' + (o.rot == null ? -7 : o.rot) + 'deg) scale(' + s + ')';
      dots.forEach(function (d) { d.style.opacity = f >= 3 ? .85 : 0; });
    });
    return e;
  }
  // Layar chat di atas kertas (before/after)
  function ChatPaper(L, o) {
    var html = '<div class="mk-mono" style="font-size:22px;color:' + C.gray + ';margin-bottom:22px">' + (o.label || '') + '</div>';
    o.messages.forEach(function (m, i) {
      var me = m.from === 'cs';
      html += '<div id="' + L.id + 'm' + i + '" style="display:flex;justify-content:' + (me ? 'flex-end' : 'flex-start') + ';margin:14px 0"><div style="max-width:640px;padding:20px 26px;border-radius:' + (me ? '26px 26px 6px 26px' : '26px 26px 26px 6px') + ';background:' + (me ? '#E7F1DD' : '#fff') + ';border:2px solid rgba(15,14,12,.12);font:500 38px/1.25 Outfit,sans-serif;color:' + C.ink + '">' + m.text + '<div style="font:500 22px JetBrains Mono,monospace;color:' + C.gray + ';text-align:right;margin-top:8px">' + (m.time || '') + '</div></div></div>';
    });
    var card = PaperCard(L, { x: o.x || 84, y: o.y || 420, w: o.w || 912, html: html, at: o.at || 0, from: o.from || 'bottom', rot: o.rot == null ? -1 : o.rot });
    L.on(function (t) { o.messages.forEach(function (m, i) { var b = $(L.id + 'm' + i); if (b) { var k = pr(t, (o.at || 0) + (m.at == null ? .25 + i * .5 : m.at), .3); b.style.opacity = k; b.style.transform = 'translateY(' + ((1 - E.out(k)) * 20) + 'px)'; } }); });
    return card;
  }
  // Diagram Brand-Up: corong 5 titik, satu menyala
  var DIMS = ['CLARITY', 'TRUST', 'PREMIUM', 'SYSTEM', 'CONTENT'];
  function InkDiagramBrandUp(L, o) {
    var at = o.at || 0, top = o.y || 470;
    InkPath(L, { d: 'M140 ' + top + ' L940 ' + top + ' L650 ' + (top + 760) + ' L430 ' + (top + 760) + ' Z', w: 7, at: at, dur: .7 });
    var nodes = [];
    DIMS.forEach(function (d, i) {
      var y = top + 90 + i * 150, lit = (i + 1) === o.active;
      var dot = el('div', 'left:510px;top:' + (y - 30) + 'px;width:60px;height:60px;border-radius:50%;border:6px solid ' + (lit ? C.terra : C.ink) + ';background:' + (lit ? C.terra : C.white), '', L.root); dot.className = 'mk-a';
      var lab = el('div', 'left:' + (i % 2 ? 600 : 140) + 'px;width:340px;top:' + (y - 22) + 'px;text-align:' + (i % 2 ? 'left' : 'right') + ';font-size:40px;color:' + (lit ? C.terra : C.ink), d, L.root); lab.className = 'mk-a mk-ou';
      if (!(i % 2)) lab.style.left = '140px', lab.style.width = '340px';
      nodes.push([dot, lab, lit]);
    });
    L.on(function (t) {
      nodes.forEach(function (n, i) {
        var k = pr(t, at + .5 + i * .18, .3); n[0].style.opacity = k; n[1].style.opacity = n[2] ? k : k * .55;
        n[0].style.transform = 'scale(' + (.6 + .4 * E.out(k)) + ')';
        if (n[2]) { var g = pr(t, at + .5 + 5 * .18 + .2, .4); n[0].style.boxShadow = '0 0 0 ' + (g * 18) + 'px rgba(184,74,46,' + (.25 * g) + ')'; }
      });
    });
    return { y: function (i) { return top + 90 + (i - 1) * 150; } };
  }
  // Kartu seri (penutup)
  function SeriesCard(L, o) {
    el('div', 'left:0;top:0;width:1080px;height:1920px;background:' + C.ink, '', L.root).className = 'mk-a';
    var a = el('div', 'left:96px;top:760px;font-size:30px;color:' + C.amber, o.series, L.root); a.className = 'mk-a mk-mono';
    var b = el('div', 'left:96px;top:810px;width:888px;font-size:120px;line-height:1;color:' + C.white, o.title, L.root); b.className = 'mk-a mk-fr';
    var c = el('div', 'left:96px;top:1080px;font-size:44px;color:' + C.white, o.handle || '@aldysyahreza', L.root); c.className = 'mk-a mk-ou';
    L.headline = true;
    L.on(function (t) { [a, b, c].forEach(function (x, i) { var k = pr(t, .05 + i * .12, .35); x.style.opacity = k; x.style.transform = 'translateY(' + ((1 - E.out(k)) * 20) + 'px)'; }); });
  }
  // Pengganti footage di demo (di produksi: klip Kamera A/B)
  function Slate(L, o) {
    el('div', 'left:0;top:0;width:1080px;height:1920px;background:' + C.soft, '', L.root).className = 'mk-a';
    var e = el('div', 'left:96px;right:96px;top:860px;text-align:center;font-size:40px;line-height:1.4;color:' + C.cream, o.text, L.root); e.className = 'mk-a mk-mono';
    L.headline = true;
  }

  /* ---------- mesin: shot, transisi, kamera kertas ---------- */
  var SHOTS = [], TOTAL = 0, PAPER, GR, SWEEP, stage, SHAKE = 0;
  function run(list) {
    boilDefs(); grainFrames();
    stage = el('div', '', '', document.body); stage.className = 'mk-stage';
    PAPER = el('div', 'left:0;top:0;width:1080px;height:1920px;background-size:cover', '', stage); PAPER.className = 'mk-a';
    var papers = [paperDataURL(17, C.cream, .10), paperDataURL(23, C.white, .08)];
    list.forEach(function (s, i) {
      var root = el('div', '', '', stage); root.className = 'mk-shot';
      var L = { id: 's' + i, root: root, fns: [], headline: false, on: function (f) { this.fns.push(f); } };
      s.t0 = TOTAL; TOTAL += s.dur; s.L = L; s.paper = papers[s.paper === 'white' ? 1 : 0];
      s.build(L, MK);
      SHOTS.push(s);
    });
    GR = el('div', 'left:0;top:0;width:1080px;height:1920px;background-size:360px 640px;mix-blend-mode:overlay;opacity:.045;pointer-events:none', '', document.body); GR.className = 'mk-a';
    SWEEP = el('div', 'left:0;top:-60px;width:1200px;height:2040px;background:' + C.cream + ';box-shadow:-30px 0 60px rgba(15,14,12,.25);opacity:0', '', document.body); SWEEP.className = 'mk-a';
    window.ANIMATIC_DURATION = TOTAL;
    seek(0);
  }
  function seek(t) {
    var cur = SHOTS.length - 1;
    for (var i = 0; i < SHOTS.length; i++) if (t < SHOTS[i].t0 + SHOTS[i].dur) { cur = i; break; }
    SHOTS.forEach(function (s, i) { s.L.root.style.visibility = i === cur ? 'visible' : 'hidden'; });
    var s = SHOTS[cur], lt = t - s.t0;
    PAPER.style.backgroundImage = 'url(' + s.paper + ')';
    // kamera kertas: dolly-in 5-8% sepanjang shot (bila diminta)
    var z = s.dolly ? 1 + s.dolly * E.io(cl(lt / s.dur)) : 1;
    var sh = 0; if (s.L.stampAt != null) { var f = Math.floor((lt - s.L.stampAt) * FPS); if (f === 0) sh = 6; else if (f === 1) sh = -6; }
    s.L.root.style.transform = 'translate(' + sh + 'px,' + (-sh * .5) + 'px) scale(' + z + ')';
    s.L.fns.forEach(function (f) { f(lt); });
    GR.style.backgroundImage = 'url(' + GRAIN[Math.floor(t * 12) % 4] + ')';
    // transisi "kertas menyapu" 7 frame menuju shot ini
    var sw = 0; if (s.tr === 'sweep') { var k = lt * FPS / 7; if (k < 1) sw = k; }
    var prev = SHOTS[cur + 1]; var k2 = prev && prev.tr === 'sweep' ? (s.t0 + s.dur - t) * FPS / 7 : 9;
    if (sw) { SWEEP.style.opacity = 1; SWEEP.style.transform = 'translateX(' + (-1200 + sw * 2400) + 'px) rotate(-2deg)'; }
    else if (k2 < 1) { SWEEP.style.opacity = 1; SWEEP.style.transform = 'translateX(' + (1080 - (1 - k2) * 1200) + 'px) rotate(-2deg)'; }
    else SWEEP.style.opacity = 0;
  }
  var MK = { C: C, E: E, pr: pr, el: el, run: run, Headline: Headline, Subtitle: Subtitle, CountUp: CountUp, PaperCard: PaperCard, InkPath: InkPath,
    MarkerCircle: MarkerCircle, MarkerStrike: MarkerStrike, Highlighter: Highlighter, StampBocor: StampBocor, ChatPaper: ChatPaper,
    InkDiagramBrandUp: InkDiagramBrandUp, SeriesCard: SeriesCard, Slate: Slate, DIMS: DIMS };
  window.MK = MK; window.seek = seek;
})();
