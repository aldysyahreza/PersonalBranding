// Preview di browser: video sumber + overlay HTML yang mengikuti aturan yang sama
// dengan render (pemecahan frasa, posisi, ukuran, cut). Ini perkiraan cepat;
// tombol "Cek frame akurat" merender frame asli lewat ffmpeg.
import { h } from './ui.js';
import { store } from './store.js';
import { buildPhrases, splitLeadKey, framing, isCut, OUTPUT_FORMATS, keepSegments, mapTime, fmtTime, zoomAt, kineticLines, resolveEmphasis } from '../shared/core.js';

const WEIGHTS = { Thin: 100, ExtraLight: 200, Light: 300, Regular: 400, Medium: 500, SemiBold: 600, Bold: 700, ExtraBold: 800, Black: 900 };
export function fontCss(name = 'Inter') {
  const italic = /\sItalic$/.test(String(name));
  const parts = String(name).replace(/\sItalic$/, '').split(' ');
  const last = parts[parts.length - 1];
  // "Montserrat ExtraBold" → keluarga "Montserrat", tebal 800; "Great Vibes" → keluarga utuh, tebal 400.
  const family = WEIGHTS[last] ? parts.slice(0, -1).join(' ') : parts.join(' ');
  return { fontFamily: `'${family}', system-ui, sans-serif`, fontWeight: WEIGHTS[last] || 400, fontStyle: italic ? 'italic' : 'normal' };
}

const measureCtx = document.createElement('canvas').getContext('2d');
/** Lebar teks (px) di browser dengan font yang sama dengan render. */
function textWidth(text, size, font) {
  const f = fontCss(font);
  measureCtx.font = `${f.fontStyle} ${f.fontWeight} ${size}px ${f.fontFamily}`;
  return measureCtx.measureText(text).width;
}

export function createPreview() {
  const p = store.project;
  const video = h('video', { src: `/api/projects/${p.id}/media/source`, preload: 'auto', playsInline: true, class: 'pv-video' });
  const bgVideo = h('video', { src: `/api/projects/${p.id}/media/source`, muted: true, preload: 'auto', playsInline: true, class: 'pv-bg hidden' });
  const music = h('audio', { preload: 'auto' });
  const frame = h('div', { class: 'pv-frame' });
  const vignette = h('div', { class: 'pv-vignette' });
  const brollLayer = h('div', { class: 'pv-layer' });
  const capLayer = h('div', { class: 'pv-layer' });
  const scrimLayer = h('div', { class: 'pv-layer pv-scrim' });
  const hookLayer = h('div', { class: 'pv-layer' });
  const cardLayer = h('div', { class: 'pv-layer' });
  const guides = h('div', { class: 'pv-layer pv-guides hidden' });
  frame.append(bgVideo, video, vignette, brollLayer, scrimLayer, capLayer, hookLayer, cardLayer, guides);
  const stage = h('div', { class: 'pv-stage' }, frame);
  const timeLabel = h('span', { class: 'mono' });
  const playBtn = h('button', { class: 'btn primary', onclick: () => (video.paused ? video.play() : video.pause()) }, '▶ Putar');
  const guideToggle = h('input', { type: 'checkbox', onchange: (e) => guides.classList.toggle('hidden', !e.target.checked) });
  const controls = h('div', { class: 'pv-controls' },
    playBtn,
    h('button', { class: 'btn ghost sm', onclick: () => seek(video.currentTime - 2) }, '−2 dtk'),
    h('button', { class: 'btn ghost sm', onclick: () => seek(video.currentTime + 2) }, '+2 dtk'),
    timeLabel,
    h('label', { class: 'check small' }, guideToggle, ' Zona aman & wajah'),
  );
  const el = h('div', { class: 'preview' }, stage, controls);

  let W = 1080, H = 1920, cache = { key: '', phrases: [] }, activeBroll = null, raf = 0, lastT = -1;

  function seek(t) {
    video.currentTime = Math.max(0, Math.min(p.source.meta.duration - 0.05, t));
    draw(true);
  }

  let curZoom = 0;
  /** Zoom punch-in = framing dengan faktor zoom dikalikan (sama dengan render). */
  function applyZoom(z, force = false) {
    const pr = store.project;
    if (pr.output.framing === 'fit' || (!force && z === curZoom)) return;
    curZoom = z;
    const m = pr.source.meta, fr = pr.output.reframe || {};
    const c = framing(m.width, m.height, W, H, { ...fr, zoom: (fr.zoom || 1) * z });
    Object.assign(video.style, { width: `${c.sw}px`, height: `${c.sh}px`, left: `${-c.cx}px`, top: `${-c.cy}px` });
  }

  function layout() {
    const pr = store.project;
    const fmt = OUTPUT_FORMATS[pr.output.aspect] || OUTPUT_FORMATS['9:16'];
    W = fmt.width;
    H = fmt.height;
    const box = stage.getBoundingClientRect();
    const k = Math.min((box.width || 360) / W, (Math.min(window.innerHeight * 0.72, 760)) / H);
    frame.style.width = `${W}px`;
    frame.style.height = `${H}px`;
    frame.style.transform = `scale(${k})`;
    stage.style.height = `${H * k}px`;
    stage.style.width = `${W * k}px`;
    const m = pr.source.meta;
    if (pr.output.framing === 'fit') {
      const fit = Math.min(W / m.width, H / m.height);
      Object.assign(video.style, { width: `${m.width * fit}px`, height: `${m.height * fit}px`, left: `${(W - m.width * fit) / 2}px`, top: `${(H - m.height * fit) / 2}px` });
      const c = framing(m.width, m.height, W, H, {});
      Object.assign(bgVideo.style, { width: `${c.sw}px`, height: `${c.sh}px`, left: `${-c.cx}px`, top: `${-c.cy}px` });
      bgVideo.classList.remove('hidden');
    } else {
      applyZoom(zoomAt(video.currentTime, pr.zooms), true);
      bgVideo.classList.add('hidden');
    }
    // Koreksi warna (perkiraan CSS dari parameter ffmpeg eq/colorbalance).
    const col = pr.style.color;
    const i = col.enabled ? col.intensity : 0;
    const filter = col.enabled ? `brightness(${1 + (col.brightness || 0) * i * 1.6}) contrast(${1 + (col.contrast - 1) * i}) saturate(${1 + (col.saturation - 1) * i}) sepia(${Math.max(0, (col.warmth || 0) * i * 1.4)})` : 'none';
    video.style.filter = filter;
    bgVideo.style.filter = `${filter === 'none' ? '' : filter} blur(20px) brightness(0.85)`;
    vignette.style.opacity = col.enabled ? String(Math.min(1, (col.vignette || 0) * i * 1.6)) : '0';
    // Panduan zona aman & wajah.
    const sz = pr.style.safeZone, fz = pr.style.faceZone;
    guides.replaceChildren(
      h('div', { class: 'g-safe', style: { left: `${sz.side * W}px`, right: `${sz.side * W}px`, top: `${sz.top * H}px`, bottom: `${sz.bottom * H}px` } }, h('span', {}, 'Zona aman (UI platform di luar kotak)')),
      h('div', { class: 'g-face', style: { top: `${fz.top * H}px`, height: `${(fz.bottom - fz.top) * H}px` } }, h('span', {}, 'Zona wajah — hindari teks di sini')),
      h('div', { class: 'g-cap', style: { top: `${pr.style.captions.position * H}px` } }, h('span', {}, 'Garis dasar subtitle')),
    );
    draw(true);
  }

  function phrasesFor(pr) {
    const cap = pr.style.captions;
    const key = JSON.stringify([pr.transcript?.segments, cap.maxWords, cap.maxChars, cap.layout, cap.emphasis]);
    if (key !== cache.key) {
      // Salinan kata agar penandaan gaya penekanan tidak mengubah data transkrip.
      const segs = JSON.parse(JSON.stringify(pr.transcript?.segments || []));
      const phrases = buildPhrases(segs, { maxWords: cap.maxWords, maxChars: cap.maxChars });
      if (cap.layout === 'kinetic') resolveEmphasis(phrases, cap.emphasis);
      cache = { key, phrases };
    }
    return cache.phrases;
  }

  let capState = { key: null, words: [] };
  /** Caption kinetik: blok baris dibangun sekali per frasa; tiap kata menyala saat waktunya tiba. */
  function drawKinetic(pr, t, ph) {
    const cap = pr.style.captions;
    const stateKey = `${ph.start}|${W}|${JSON.stringify(cap)}|${JSON.stringify(pr.style.colors)}|${JSON.stringify(pr.style.fonts)}`;
    if (capState.key !== stateKey) {
      const k = Math.min(W, H) / 1080, col = pr.style.colors, fonts = { accent: 'Great Vibes', ...pr.style.fonts };
      const side = W * pr.style.safeZone.side;
      const safeTop = H * pr.style.safeZone.top, safeBottom = H * (1 - pr.style.safeZone.bottom);
      const capY = Math.round(Math.min(safeBottom, Math.max(safeTop + cap.keySize * k * 2, H * cap.position)));
      const size = { small: cap.leadSize * k, big: cap.keySize * k, script: cap.keySize * (cap.scriptScale ?? 1.8) * k };
      const fontOf = { small: fonts.lead, big: fonts.key, script: fonts.accent };
      const capW = (W - side - Math.max(side, W * (pr.style.safeZone.right || 0))) * 0.94;
      const ls = kineticLines(ph.words, { maxWidth: capW, widthOf: (text, tier) => textWidth(cap.uppercase ? text.toUpperCase() : text, size[tier], fontOf[tier]) });
      const gap = { small: 1.15, big: 1.02, script: cap.scriptGap ?? (/great vibes/i.test(fonts.accent) ? 0.82 : 1.0) };
      const font = { small: fonts.lead, big: fonts.key, script: fonts.accent };
      const heights = ls.map((l) => size[l.tier] * gap[l.tier]);
      let y = capY - heights.reduce((a, b) => a + b, 0);
      const shadow = `0 ${cap.shadow * k}px ${cap.shadow * k * 1.2}px rgba(0,0,0,.5)`;
      const words = [];
      capLayer.replaceChildren(...ls.map((l, li) => {
        y += heights[li];
        const lineEl = h('div', { class: 'pv-cap-line pv-kin-line', style: { left: `${side}px`, right: `${side}px`, top: `${y}px`, fontSize: `${size[l.tier]}px`, lineHeight: 1, color: col.text, textShadow: shadow, letterSpacing: l.tier === 'big' ? '-0.01em' : '0', ...fontCss(font[l.tier]) } });
        lineEl.dataset.start = l.words[0].start;
        l.words.forEach((w) => {
          const txt = cap.uppercase ? w.text.toUpperCase() : w.text;
          let el;
          if (w.style === 'box' && l.tier === 'big') el = h('span', { class: 'pv-kin-word pv-emph-box', style: { background: col.accent, padding: `0 ${10 * k}px`, textShadow: 'none' } }, txt);
          else if (w.style === 'color') el = h('span', { class: 'pv-kin-word', style: { color: col.accent } }, txt);
          else if (w.style === 'arc') el = h('span', { class: 'pv-kin-word pv-arc', style: { '--arc': col.accent } }, txt);
          else el = h('span', { class: 'pv-kin-word' }, txt);
          el.dataset.start = w.start;
          words.push(el);
          lineEl.append(el, ' ');
        });
        return lineEl;
      }));
      capState = { key: stateKey, words, lines: [...capLayer.children] };
    }
    for (const el of capState.words) el.classList.toggle('on', t >= Number(el.dataset.start) - 0.02);
    for (const el of capState.lines) el.classList.toggle('on', t >= Number(el.dataset.start) - 0.02);
  }

  function drawCaptions(pr, t) {
    const cap = pr.style.captions;
    // Saat kartu grafis tampil, subtitle disembunyikan (sama dengan render).
    const hk = pr.hook?.approved && pr.style.hook?.enabled !== false && pr.hook.big ? pr.hook : null;
    const onHook = hk && t >= hk.start && t < hk.end;
    drawHook(pr, onHook ? hk : null);
    scrimLayer.style.opacity = cap.enabled ? String(cap.scrim || 0) : '0';
    const onCard = onHook || (pr.cards || []).some((c) => c.approved && t >= c.start && t < c.end);
    const ph = cap.enabled && !onCard ? phrasesFor(pr).find((x) => t >= x.start && t < x.end) : null;
    if (ph && cap.layout === 'kinetic') return drawKinetic(pr, t, ph);
    capState = { key: null, words: [] };
    capLayer.replaceChildren();
    if (!ph) return;
    const k = Math.min(W, H) / 1080;
    const col = pr.style.colors;
    const side = W * pr.style.safeZone.side;
    const safeTop = H * pr.style.safeZone.top, safeBottom = H * (1 - pr.style.safeZone.bottom);
    const capY = Math.round(Math.min(safeBottom, Math.max(safeTop + cap.keySize * k * 2, H * cap.position)));
    const shadow = `0 ${cap.shadow * k}px ${cap.shadow * k * 1.2}px rgba(0,0,0,.5)`;
    const activeIdx = cap.layout === 'karaoke' ? ph.words.findIndex((w, i) => t >= w.start && (i === ph.words.length - 1 || t < ph.words[i + 1].start)) : -1;
    const wordEl = (w, i) => {
      const txt = cap.uppercase ? w.text.toUpperCase() : w.text;
      const hot = w.emph || i === activeIdx;
      if (!hot) return h('span', {}, txt);
      if (cap.emphasis === 'box') return h('span', { class: 'pv-emph-box', style: { background: col.accent, padding: `0 ${10 * k}px`, textShadow: 'none', ...fontCss(pr.style.fonts.key) } }, txt);
      if (cap.emphasis === 'color') return h('span', { style: { color: col.accent, ...fontCss(pr.style.fonts.key) } }, txt);
      return h('span', { style: fontCss(pr.style.fonts.key) }, txt);
    };
    const lineEl = (words, size, font, offset = 0) =>
      h('div', { class: 'pv-cap-line', style: { left: `${side}px`, right: `${side}px`, top: `${capY - offset}px`, fontSize: `${size}px`, color: col.text, textShadow: shadow, ...fontCss(font) } },
        ...words.flatMap((w, i) => [wordEl(w, i), ' ']));
    if (cap.layout === 'stack') {
      const { lead, key } = splitLeadKey(ph.words);
      if (lead.length) capLayer.append(lineEl(lead, cap.leadSize * k, pr.style.fonts.lead, Math.round(cap.keySize * k * 1.08)));
      capLayer.append(lineEl(key, cap.keySize * k, pr.style.fonts.key));
    } else {
      capLayer.append(lineEl(ph.words, cap.keySize * k, pr.style.fonts.key));
    }
  }

  let hookKey = null;
  /** Hook lockup (sama dengan render ASS): lead → kata besar slam → frasa rasa. */
  function drawHook(pr, hk) {
    const key = hk ? JSON.stringify([hk, W, pr.style.fonts]) : null;
    if (key === hookKey) return;
    hookKey = key;
    hookLayer.replaceChildren();
    if (!hk) return;
    const k = Math.min(W, H) / 1080, f = pr.style.fonts;
    const big = String(hk.big).trim();
    const capW = (W - W * pr.style.safeZone.side - Math.max(W * pr.style.safeZone.side, W * (pr.style.safeZone.right || 0))) * 0.94;
    const fit = (txt, size, font) => Math.min(size, size * capW / Math.max(1, textWidth(txt, size, font)));
    const bs = fit(big, (big.length <= 9 ? 200 : big.length <= 12 ? 150 : 112) * k, f.key);
    const bottom = Math.min(H * (1 - pr.style.safeZone.bottom), H * 0.73);
    hookLayer.append(h('div', { class: 'pv-hook', style: { left: '0', right: '0', bottom: `${H - bottom}px`, color: pr.style.colors.text } },
      hk.lead ? h('div', { class: 'pv-hook-lead', style: { fontSize: `${fit(hk.lead, 46 * k, f.lead)}px`, ...fontCss(f.lead) } }, hk.lead) : null,
      h('div', { class: 'pv-hook-big', style: { fontSize: `${bs}px`, letterSpacing: '-0.035em', lineHeight: 0.88, ...fontCss(f.key) } }, big),
      hk.accent ? h('div', { class: 'pv-hook-acc', style: { fontSize: `${fit(hk.accent, 124 * k, f.accent)}px`, lineHeight: 0.95, ...fontCss(f.accent) } }, hk.accent) : null));
  }

  let cardKey = null;
  function drawCards(pr, t) {
    const card = (pr.cards || []).find((c) => c.approved && t >= c.start && t < c.end);
    const key = card ? `${JSON.stringify(card)}|${W}|${JSON.stringify(pr.style.cards)}|${JSON.stringify(pr.style.colors)}|${JSON.stringify(pr.style.fonts)}` : null;
    if (key === cardKey) {
      // Kartu HyperFrames: geser timeline GSAP di iframe ke waktu kartu (sama dengan render).
      const fr = cardLayer.querySelector('iframe');
      if (fr && card) {
        try {
          fr.contentWindow.__timelines?.root?.seek(Math.max(0, t - card.start), false);
        } catch {}
      }
      return;
    }
    cardKey = key;
    cardLayer.replaceChildren();
    if (!card) return;
    if ((pr.style.cards?.engine ?? 'hyperframes') === 'hyperframes' && store.status.hyperframes?.ok && card.layout !== 'panel') {
      const fr = h('iframe', { class: 'pv-hf', allowTransparency: 'true', src: `/api/projects/${pr.id}/hf/preview/${card.id}?w=${W}&h=${H}&v=${encodeURIComponent(key.length + ':' + card.title)}`, style: { width: `${W}px`, height: `${H}px` }, scrolling: 'no' });
      fr.addEventListener('load', () => { try { fr.contentWindow.__timelines?.root?.seek(Math.max(0, store.playhead - card.start), false); } catch {} });
      cardLayer.append(fr);
      return;
    }
    cardLayer.style.setProperty('--card-dur', `${Math.max(0.3, card.end - card.start)}s`);
    const st = pr.style, col = st.colors, k = Math.min(W, H) / 1080;
    const side = W * st.safeZone.side;
    const full = card.layout !== 'panel';
    const icon = card.icon ? { check: '✓', cross: '✕', arrow: '→', warning: '▲', star: '★' }[card.icon] : '';
    const label = (txt) => h('div', { style: { fontSize: `${st.cards.labelSize * k}px`, color: col.cardMuted, ...fontCss(st.fonts.lead) } }, txt);
    let titleEl;
    const numSize = Math.min(st.cards.numberSize * k * 1.6, ((W - side * 2) * 0.7) / Math.max(0.5, String(card.title || '0').length * 0.66));
    const dark = 'rgba(90,10,10,1)';
    const extrude = Array.from({ length: 7 }, (_, i) => `${(i + 1) * 0.9 * k}px ${(i + 1) * 1.6 * k}px 0 ${dark}`).join(',');
    if (card.type === 'number') titleEl = h('div', { class: 'pv-anim-slam', style: { whiteSpace: 'nowrap', fontSize: `${numSize}px`, lineHeight: 1, color: col.accent, textShadow: `${extrude}, ${14 * k}px ${26 * k}px ${22 * k}px rgba(0,0,0,.35)`, ...fontCss(st.fonts.card) } }, card.title);
    else if (card.type === 'list') titleEl = h('div', {}, h('div', { style: { fontSize: `${st.cards.titleSize * 0.8 * k}px`, color: col.cardText, ...fontCss(st.fonts.card) } }, card.title), ...String(card.subtitle || '').split(/\s*[;|]\s*/).filter(Boolean).map((it) => h('div', { style: { fontSize: `${st.cards.labelSize * k}px`, color: col.cardText, marginTop: `${18 * k}px`, ...fontCss(st.fonts.lead) } }, `• ${it}`)));
    else titleEl = h('div', { class: 'pv-anim-wipe', style: { fontSize: `${st.cards.titleSize * 0.85 * k}px`, lineHeight: 1.3, ...fontCss(st.fonts.key) } }, h('span', { style: { background: col.accent, color: '#fff', padding: `0 ${14 * k}px`, boxShadow: `${12 * k}px ${12 * k}px 0 rgba(120,15,15,1)`, boxDecorationBreak: 'clone', WebkitBoxDecorationBreak: 'clone' } }, card.title));
    // Sama seperti render ASS: judul berpusat di cy, ikon + label atas di atasnya, label bawah di bawahnya.
    const head = h('div', { class: 'pv-card-head pv-anim-drop', style: { left: `${side}px`, right: `${side}px` } },
      icon ? h('div', { class: 'pv-anim-pop', style: { fontSize: `${120 * k}px`, color: col.accent, lineHeight: 1 } }, icon) : null,
      card.kicker ? label(card.kicker) : null);
    const body = h('div', { class: 'pv-card-content', style: { left: `${side}px`, right: `${side}px` } }, titleEl);
    const foot = card.subtitle && card.type !== 'list' ? h('div', { class: 'pv-card-foot', style: { left: `${side}px`, right: `${side}px` } }, label(card.subtitle)) : null;
    let cy;
    if (full) {
      const paper = st.cards.paper !== false ? `url(/api/library/paper/${W}/${H}/file?c=${encodeURIComponent(col.cardBg)}) center/cover, ` : '';
      const bg = h('div', { class: 'pv-card-full', style: { background: `${paper}${col.cardBg}` } });
      if (st.cards.grid) bg.append(h('div', { class: 'pv-grid', style: { width: `${760 * k}px`, height: `${520 * k}px`, top: `${H * 0.47}px`, backgroundSize: `${52 * k}px ${52 * k}px` } }));
      cy = H * 0.47;
      cardLayer.append(bg);
    } else {
      const ph = (card.icon ? 640 : 560) * k;
      const top = Math.min(H * (1 - st.safeZone.bottom) - ph, H * st.faceZone.bottom + 20 * k);
      cardLayer.append(h('div', { class: 'pv-card-panel', style: { left: `${side}px`, right: `${side}px`, top: `${top}px`, height: `${ph}px`, background: col.cardBg, borderRadius: `${36 * k}px` } }));
      cy = top + ph / 2 + (card.icon ? 70 * k : 0);
    }
    body.style.top = `${cy}px`;
    body.classList.add('pv-anim-drift');
    if (foot) foot.classList.add('pv-anim-late');
    cardLayer.append(body, head, foot);
    const th = body.offsetHeight;
    head.style.top = `${cy - th / 2 - 8 * k}px`;
    if (foot) foot.style.top = `${cy + th / 2 + 8 * k}px`;
  }

  function drawBroll(pr, t) {
    const b = (pr.broll || []).find((x) => x.approved && x.assetId && t >= x.start && t < x.end);
    const asset = b && pr.assets.find((a) => a.id === b.assetId && !a.missing);
    const key = asset ? `${b.id}:${asset.id}` : null;
    if (key !== activeBroll) {
      brollLayer.replaceChildren();
      activeBroll = key;
      if (asset) {
        const src = `/api/projects/${pr.id}/media/asset/${asset.id}`;
        const el = asset.kind === 'image' ? h('img', { src, class: 'pv-broll' }) : h('video', { src, muted: true, class: 'pv-broll', autoplay: !video.paused });
        brollLayer.append(el);
      }
    }
    const v = brollLayer.querySelector('video');
    if (v && b) {
      const want = t - b.start;
      if (Math.abs(v.currentTime - want) > 0.3) v.currentTime = Math.max(0, want);
      if (video.paused !== v.paused) video.paused ? v.pause() : v.play().catch(() => {});
    }
  }

  function syncMusic(pr, t) {
    const m = pr.music;
    const asset = m.enabled && pr.assets.find((a) => a.id === m.assetId && !a.missing);
    if (!asset) {
      if (!music.paused) music.pause();
      return;
    }
    const src = `/api/projects/${pr.id}/media/asset/${asset.id}`;
    if (!music.src.endsWith(src)) music.src = src;
    music.volume = Math.min(1, Math.pow(10, (m.volumeDb ?? -24) / 20) * 2.5);
    const keep = keepSegments(pr.source.meta.duration, pr.cuts);
    const outT = mapTime(t, keep);
    if (outT === null) return;
    const want = outT - (m.startAt || 0);
    if (want < 0) {
      if (!music.paused) music.pause();
      return;
    }
    if (music.duration && Math.abs(music.currentTime - (want % music.duration)) > 0.4) music.currentTime = want % music.duration;
    if (video.paused !== music.paused) video.paused ? music.pause() : music.play().catch(() => {});
  }

  function draw(force = false) {
    const pr = store.project;
    if (!pr) return;
    let t = video.currentTime;
    if (!video.paused && isCut(t, pr.cuts)) {
      const c = pr.cuts.find((x) => x.enabled && t >= x.start && t < x.end);
      video.currentTime = c.end + 0.001;
      t = c.end;
    }
    if (!force && Math.abs(t - lastT) < 0.015) return;
    lastT = t;
    store.playhead = t;
    if (pr.output.framing === 'fit' && Math.abs(bgVideo.currentTime - t) > 0.25) bgVideo.currentTime = t;
    applyZoom(zoomAt(t, pr.zooms));
    drawCaptions(pr, t);
    drawCards(pr, t);
    drawBroll(pr, t);
    syncMusic(pr, t);
    const keep = keepSegments(pr.source.meta.duration, pr.cuts);
    const outT = mapTime(t, keep);
    timeLabel.textContent = `Sumber ${fmtTime(t)} · Output ${outT === null ? '(dipotong)' : fmtTime(outT)}`;
    el.dispatchEvent(new CustomEvent('time', { detail: t }));
  }

  function loop() {
    draw();
    raf = requestAnimationFrame(loop);
  }

  video.addEventListener('play', () => {
    playBtn.textContent = '❚❚ Jeda';
    if (store.project.output.framing === 'fit') bgVideo.play().catch(() => {});
  });
  video.addEventListener('pause', () => {
    playBtn.textContent = '▶ Putar';
    bgVideo.pause();
    music.pause();
    brollLayer.querySelector('video')?.pause();
  });
  video.addEventListener('loadedmetadata', () => {
    if (store.playhead) video.currentTime = store.playhead;
    layout();
  });
  video.addEventListener('error', () => stage.append(h('div', { class: 'pv-error' }, 'Browser tidak dapat memutar format video ini. Preview overlay tetap bisa dicek dengan "Cek frame akurat"; ekspor tidak terpengaruh.')));
  const ro = new ResizeObserver(() => layout());
  ro.observe(el);
  raf = requestAnimationFrame(loop);

  return {
    el,
    video,
    seek,
    refresh: layout,
    destroy() {
      cancelAnimationFrame(raf);
      ro.disconnect();
      video.pause();
      music.pause();
    },
  };
}
