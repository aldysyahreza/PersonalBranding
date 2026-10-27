// Preview di browser: video sumber + overlay HTML yang mengikuti aturan yang sama
// dengan render (pemecahan frasa, posisi, ukuran, cut). Ini perkiraan cepat;
// tombol "Cek frame akurat" merender frame asli lewat ffmpeg.
import { h } from './ui.js';
import { store } from './store.js';
import { buildPhrases, splitLeadKey, framing, isCut, OUTPUT_FORMATS, keepSegments, mapTime, fmtTime } from '../shared/core.js';

const WEIGHTS = { Thin: 100, ExtraLight: 200, Light: 300, Regular: 400, Medium: 500, SemiBold: 600, Bold: 700, ExtraBold: 800, Black: 900 };
export function fontCss(name = 'Inter') {
  const [family, ...rest] = String(name).split(' ');
  return { fontFamily: `'${family}', system-ui, sans-serif`, fontWeight: WEIGHTS[rest.join('')] || 400 };
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
  const cardLayer = h('div', { class: 'pv-layer' });
  const guides = h('div', { class: 'pv-layer pv-guides hidden' });
  frame.append(bgVideo, video, vignette, brollLayer, capLayer, cardLayer, guides);
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
      const c = framing(m.width, m.height, W, H, pr.output.reframe || {});
      Object.assign(video.style, { width: `${c.sw}px`, height: `${c.sh}px`, left: `${-c.cx}px`, top: `${-c.cy}px` });
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
    const key = JSON.stringify([pr.transcript?.segments, pr.style.captions.maxWords, pr.style.captions.maxChars]);
    if (key !== cache.key) cache = { key, phrases: buildPhrases(pr.transcript?.segments || [], { maxWords: pr.style.captions.maxWords, maxChars: pr.style.captions.maxChars }) };
    return cache.phrases;
  }

  function drawCaptions(pr, t) {
    const cap = pr.style.captions;
    capLayer.replaceChildren();
    if (!cap.enabled) return;
    const ph = phrasesFor(pr).find((x) => t >= x.start && t < x.end);
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

  function drawCards(pr, t) {
    cardLayer.replaceChildren();
    const card = (pr.cards || []).find((c) => c.approved && t >= c.start && t < c.end);
    if (!card) return;
    const st = pr.style, col = st.colors, k = Math.min(W, H) / 1080;
    const side = W * st.safeZone.side;
    const full = card.layout !== 'panel';
    const icon = card.icon ? { check: '✓', cross: '✕', arrow: '→', warning: '▲', star: '★' }[card.icon] : '';
    const label = (txt) => h('div', { style: { fontSize: `${st.cards.labelSize * k}px`, color: col.cardMuted, ...fontCss(st.fonts.lead) } }, txt);
    let titleEl;
    const numSize = st.cards.numberSize * k * Math.min(1, (W - side * 2) / Math.max(1, String(card.title || '').length * 0.62 * st.cards.numberSize * k));
    if (card.type === 'number') titleEl = h('div', { style: { whiteSpace: 'nowrap', fontSize: `${numSize}px`, lineHeight: 1, color: col.accent, textShadow: `0 ${6 * k}px ${10 * k}px rgba(0,0,0,.25)`, ...fontCss(st.fonts.card) } }, card.title);
    else if (card.type === 'list') titleEl = h('div', {}, h('div', { style: { fontSize: `${st.cards.titleSize * 0.8 * k}px`, color: col.cardText, ...fontCss(st.fonts.card) } }, card.title), ...String(card.subtitle || '').split(/\s*[;|]\s*/).filter(Boolean).map((it) => h('div', { style: { fontSize: `${st.cards.labelSize * k}px`, color: col.cardText, marginTop: `${18 * k}px`, ...fontCss(st.fonts.lead) } }, `• ${it}`)));
    else titleEl = h('div', { style: { fontSize: `${st.cards.titleSize * 0.85 * k}px`, lineHeight: 1.3, ...fontCss(st.fonts.key) } }, h('span', { style: { background: col.accent, color: '#fff', padding: `0 ${14 * k}px`, boxDecorationBreak: 'clone', WebkitBoxDecorationBreak: 'clone' } }, card.title));
    // Sama seperti render ASS: judul berpusat di cy, ikon + label atas di atasnya, label bawah di bawahnya.
    const head = h('div', { class: 'pv-card-head', style: { left: `${side}px`, right: `${side}px` } },
      icon ? h('div', { style: { fontSize: `${120 * k}px`, color: col.accent, lineHeight: 1 } }, icon) : null,
      card.kicker ? label(card.kicker) : null);
    const body = h('div', { class: 'pv-card-content', style: { left: `${side}px`, right: `${side}px` } }, titleEl);
    const foot = card.subtitle && card.type !== 'list' ? h('div', { class: 'pv-card-foot', style: { left: `${side}px`, right: `${side}px` } }, label(card.subtitle)) : null;
    let cy;
    if (full) {
      const bg = h('div', { class: 'pv-card-full', style: { background: col.cardBg } });
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
