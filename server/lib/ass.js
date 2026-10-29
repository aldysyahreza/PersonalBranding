// Membangun file subtitle ASS (libass) untuk caption + kartu visual.
// Semua posisi dihitung dalam piksel output; semua waktu sudah dipetakan
// ke timeline output (setelah cut).
import { buildPhrases, splitLeadKey, mapSpan, mapTime, kineticLines, resolveEmphasis, subtractRanges } from '../../public/shared/core.js';
import { measure } from './fontmetrics.js';

export function assColor(hex, alpha = 0) {
  const m = String(hex || '#ffffff').replace('#', '').padEnd(6, '0');
  const r = m.slice(0, 2), g = m.slice(2, 4), b = m.slice(4, 6);
  return `&H${alpha.toString(16).padStart(2, '0').toUpperCase()}${b}${g}${r}`.toUpperCase();
}

function ts(t) {
  const cs = Math.max(0, Math.round(t * 100));
  const h = Math.floor(cs / 360000);
  const m = Math.floor((cs % 360000) / 6000);
  const s = Math.floor((cs % 6000) / 100);
  return `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}.${String(cs % 100).padStart(2, '0')}`;
}

/** Hilangkan karakter yang punya arti khusus di ASS agar teks pengguna tampil apa adanya. */
export function esc(text) {
  return String(text ?? '').replace(/\\/g, '/').replace(/\{/g, '(').replace(/\}/g, ')').replace(/\n/g, ' ');
}

const ICONS = {
  check: 'm 8 52 l 24 36 l 42 54 l 78 16 l 94 32 l 42 86',
  cross: 'm 20 6 l 50 36 l 80 6 l 94 20 l 64 50 l 94 80 l 80 94 l 50 64 l 20 94 l 6 80 l 36 50 l 6 20',
  arrow: 'm 6 38 l 56 38 l 56 10 l 96 50 l 56 90 l 56 62 l 6 62',
  warning: 'm 50 4 l 97 92 l 3 92',
  star: (() => {
    const pts = [];
    for (let i = 0; i < 10; i++) {
      const a = -Math.PI / 2 + (i * Math.PI) / 5;
      const r = i % 2 === 0 ? 48 : 20;
      pts.push(`${Math.round(50 + r * Math.cos(a))} ${Math.round(52 + r * Math.sin(a))}`);
    }
    return `m ${pts[0]} l ${pts.slice(1).join(' ')}`;
  })(),
};

/** Bungkus teks per kata ke baris dengan panjang maksimum (karakter). */
export function wrap(text, maxChars) {
  const lines = [];
  let cur = '';
  for (const w of String(text).trim().split(/\s+/).filter(Boolean)) {
    if (cur && (cur + ' ' + w).length > maxChars) {
      lines.push(cur);
      cur = w;
    } else cur = cur ? `${cur} ${w}` : w;
  }
  if (cur) lines.push(cur);
  return lines.length ? lines : [''];
}

/** Bungkus teks agar tiap baris tidak melebihi lebar (px) yang diukur dari font. */
export function wrapWidth(text, maxW, widthOf) {
  const lines = [];
  let cur = '';
  for (const w of String(text).trim().split(/\s+/).filter(Boolean)) {
    const next = cur ? `${cur} ${w}` : w;
    if (cur && widthOf(next) > maxW) {
      lines.push(cur);
      cur = w;
    } else cur = next;
  }
  if (cur) lines.push(cur);
  return lines.length ? lines : [''];
}

function rect(x, y, w, h) {
  return `m ${x} ${y} l ${x + w} ${y} ${x + w} ${y + h} ${x} ${y + h}`;
}

function roundedRect(w, h, r) {
  const k = r * 0.45;
  return [
    `m ${r} 0 l ${w - r} 0`,
    `b ${w - k} 0 ${w} ${k} ${w} ${r}`,
    `l ${w} ${h - r}`,
    `b ${w} ${h - k} ${w - k} ${h} ${w - r} ${h}`,
    `l ${r} ${h}`,
    `b ${k} ${h} 0 ${h - k} 0 ${h - r}`,
    `l 0 ${r}`,
    `b 0 ${k} ${k} 0 ${r} 0`,
  ].join(' ');
}

// Lebar relatif per huruf (em) untuk sans tebal (Montserrat ExtraBold); cukup akurat untuk
// menempatkan ornamen (garis lengkung, blok aksen) dan memilih ukuran angka.
const NARROW = { i: 0.3, l: 0.3, j: 0.3, I: 0.33, f: 0.42, t: 0.43, r: 0.45, ' ': 0.27, '.': 0.3, ',': 0.3, '!': 0.32, "'": 0.25, '1': 0.48 };
const WIDE = { m: 0.98, w: 0.9, M: 1.0, W: 1.05, O: 0.86, Q: 0.86, G: 0.82, D: 0.8, C: 0.76, '%': 0.95, '&': 0.8 };

/** Lebar teks (px): diukur dari file font bila tersedia, jika tidak memakai tabel perkiraan. */
export function estWidth(text, size, kind = 'bold', font = null) {
  const real = font ? measure(font, text, size) : null;
  if (real !== null) return real;
  if (kind === 'script') return String(text).length * size * 0.4;
  let em = 0;
  for (const ch of String(text)) {
    em += NARROW[ch] ?? WIDE[ch] ?? (/[A-Z]/.test(ch) ? 0.74 : /[0-9]/.test(ch) ? 0.66 : 0.6);
  }
  return em * size * (kind === 'small' ? 0.92 : 1);
}

// Lengkung merah (crescent) di bawah kata — ornamen "swoosh" seperti referensi.
function arcPath(w, h) {
  const r = (n) => Math.round(n);
  return `m 0 ${r(h * 0.9)} b ${r(w * 0.3)} ${r(h * 0.1)} ${r(w * 0.7)} 0 ${r(w)} ${r(h * 0.35)} l ${r(w)} ${r(h * 0.6)} b ${r(w * 0.7)} ${r(h * 0.32)} ${r(w * 0.3)} ${r(h * 0.42)} 0 ${r(h)}`;
}

export function buildAss(project, { width: W, height: H, keep, paper = false, skipCards = new Set(), endSpan = null }) {
  const st = project.style;
  const cap = st.captions;
  const col = st.colors;
  const fonts = { accent: 'Great Vibes', ...st.fonts };
  const k = Math.min(W, H) / 1080;
  const px = (n) => Math.round(n * k);
  const side = Math.round(W * (st.safeZone?.side ?? 0.06));
  const safeTop = H * (st.safeZone?.top ?? 0.12);
  const safeBottom = H * (1 - (st.safeZone?.bottom ?? 0.2));
  const capY = Math.round(Math.min(safeBottom, Math.max(safeTop + px(cap.keySize) * 2, H * cap.position)));
  const shadow = cap.shadow ?? 3;
  const lines = [];
  const ev = (layer, start, end, style, text) => lines.push(`Dialogue: ${layer},${ts(start)},${ts(end)},${style},,0,0,0,,${text}`);
  const ms = (sec) => Math.max(0, Math.round(sec * 1000));
  const darkAccent = shade(col.accent, -0.38);
  // Lebar caption: zona aman kanan bisa lebih lebar (UI Instagram), caption tetap di tengah.
  const capWidth = (W - side - Math.max(side, Math.round(W * (st.safeZone?.right ?? 0)))) * 0.94;
  const scriptGap = cap.scriptGap ?? (/great vibes/i.test(fonts.accent) ? 0.82 : 1.0);
  const hook = project.hook;
  const hookSpan = hook?.approved && st.hook?.enabled !== false ? mapSpan(hook.start, hook.end, keep) : null;
  const hookOn = !!(hookSpan && hookSpan.end - hookSpan.start > 0.2 && (hook.big || '').trim());

  const emphBox = cap.emphasis === 'box' || cap.emphasis === 'mix' || cap.layout === 'kinetic';
  const styles = [
    `Style: Lead,${fonts.lead},${px(cap.leadSize)},${assColor(col.text)},${assColor(col.text)},&H00000000,&H78000000,0,0,0,0,100,100,0,0,1,0,${shadow * 0.7},2,${side},${side},0,1`,
    `Style: Key,${fonts.key},${px(cap.keySize)},${assColor(col.text)},${assColor(col.text)},&H00000000,&H78000000,-1,0,0,0,100,100,-1,0,1,0,${shadow},2,${side},${side},0,1`,
    emphBox
      ? `Style: Emph,${fonts.key},${px(cap.keySize)},${assColor(col.text)},${assColor(col.text)},${assColor(col.accent)},&H00000000,-1,0,0,0,100,100,-1,0,3,${px(10)},0,2,${side},${side},0,1`
      : `Style: Emph,${fonts.key},${px(cap.keySize)},${assColor(cap.emphasis === 'color' ? col.accent : col.text)},${assColor(col.text)},&H00000000,&H78000000,-1,0,0,0,100,100,-1,0,1,0,${shadow},2,${side},${side},0,1`,
    `Style: Accent,${fonts.accent},${px(cap.keySize * (cap.scriptScale ?? 1.8))},${assColor(col.text)},${assColor(col.text)},&H00000000,&H78000000,0,0,0,0,100,100,0,0,1,0,${shadow},2,${side},${side},0,1`,
    `Style: Card,${fonts.card},${px(st.cards.titleSize)},${assColor(col.cardText)},${assColor(col.cardText)},&H00000000,&H96000000,-1,0,0,0,100,100,-1,0,1,0,0,5,${side},${side},0,1`,
    `Style: CardLabel,${fonts.lead},${px(st.cards.labelSize)},${assColor(col.cardMuted)},${assColor(col.cardMuted)},&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,${side},${side},0,1`,
    `Style: CardAccent,${fonts.accent},${px(st.cards.labelSize * 1.9)},${assColor(col.cardText)},${assColor(col.cardText)},&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,${side},${side},0,1`,
    `Style: CardBox,${fonts.key},${px(st.cards.titleSize)},${assColor('#FFFFFF')},${assColor('#FFFFFF')},${assColor(col.accent)},&H00000000,-1,0,0,0,100,100,-1,0,3,${px(14)},0,5,${side},${side},0,1`,
    `Style: CardBoxShade,${fonts.key},${px(st.cards.titleSize)},&HFF000000,&HFF000000,${assColor(darkAccent)},&H00000000,-1,0,0,0,100,100,-1,0,3,${px(14)},0,5,${side},${side},0,1`,
    `Style: HookLead,${fonts.lead},${px(46)},${assColor(col.text)},${assColor(col.text)},&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,0,${shadow},2,${side},${side},0,1`,
    `Style: HookBig,${fonts.key},${px(200)},${assColor(col.text)},${assColor(col.text)},&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,0,${shadow * 1.5},2,${side},${side},0,1`,
    `Style: HookAccent,${fonts.accent},${px(140)},${assColor(col.text)},${assColor(col.text)},&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,0,${shadow * 1.5},2,${side},${side},0,1`,
    `Style: Shape,Arial,20,${assColor(col.cardBg)},${assColor(col.cardBg)},&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1`,
  ];

  const anim = cap.animation === 'pop'
    ? `\\fad(60,40)\\fscx94\\fscy94\\t(0,110,\\fscx100\\fscy100)`
    : cap.animation === 'fade' ? `\\fad(110,80)` : '';
  const word = (w) => esc(cap.uppercase ? w.text.toUpperCase() : w.text);
  const line = (words, base, activeIdx = -1) =>
    words
      .map((w, i) => {
        const hot = w.emph || i === activeIdx;
        return hot ? `{\\rEmph}${word(w)}{\\r${base}}` : word(w);
      })
      .join(' ');

  // ---------------- Caption ----------------
  if (cap.enabled) {
    const segs = project.transcript?.segments || [];
    const phrases = buildPhrases(segs, { maxWords: cap.maxWords, maxChars: cap.maxChars });
    if (cap.layout === 'kinetic') resolveEmphasis(phrases, cap.emphasis);
    // Selama kartu grafis tampil, subtitle disembunyikan (kartu sudah menampilkan kalimatnya),
    // supaya teks tidak muncul dua kali.
    const cardBlocks = (project.cards || []).filter((c) => c.approved).map((c) => mapSpan(c.start, c.end, keep)).filter(Boolean);
    if (hookOn) cardBlocks.push(hookSpan);
    for (const ph of phrases) {
      const whole = mapSpan(ph.start, ph.end, keep);
      if (!whole || whole.end - whole.start < 0.05) continue;
      for (const span of subtractRanges(whole, cardBlocks)) renderPhrase(ph, span);
    }
  }

  function renderPhrase(ph, span) {
      const x = Math.round(W / 2);
      if (cap.layout === 'kinetic') {
        kineticPhrase(ph, span, x);
      } else if (cap.layout === 'stack') {
        const { lead, key } = splitLeadKey(ph.words);
        if (lead.length) ev(2, span.start, span.end, 'Lead', `{\\an2\\pos(${x},${capY - Math.round(px(cap.keySize) * 1.08)})${anim}}${line(lead, 'Lead')}`);
        ev(2, span.start, span.end, 'Key', `{\\an2\\pos(${x},${capY})${anim}}${line(key, 'Key')}`);
      } else if (cap.layout === 'karaoke') {
        ph.words.forEach((w, i) => {
          const ws = mapSpan(w.start, i < ph.words.length - 1 ? ph.words[i + 1].start : ph.end, keep);
          if (!ws) return;
          const a = i === 0 ? anim : '';
          ev(2, ws.start, ws.end, 'Key', `{\\an2\\pos(${x},${capY})${a}}${line(ph.words, 'Key', i)}`);
        });
      } else {
        ev(2, span.start, span.end, 'Key', `{\\an2\\pos(${x},${capY})${anim}}${line(ph.words, 'Key')}`);
      }
  }

  /**
   * Caption kinetik: setiap baris muncul saat kata pertamanya diucapkan, lalu setiap kata
   * "menyala" (blur → tajam, transparan → penuh) tepat pada timestamp-nya. Baris naik
   * sedikit saat masuk. Seluruh blok hilang bersama di akhir frasa (seperti referensi).
   */
  function kineticPhrase(ph, span, x) {
    const size = { small: px(cap.leadSize), big: px(cap.keySize), script: px(cap.keySize * (cap.scriptScale ?? 1.8)) };
    const tierFont = { small: fonts.lead, big: fonts.key, script: fonts.accent };
    const ls = kineticLines(ph.words, {
      maxWidth: capWidth,
      widthOf: (text, tier) => estWidth(cap.uppercase ? text.toUpperCase() : text, size[tier], tier, tierFont[tier]),
    });
    const gap = { small: 1.15, big: 1.02, script: scriptGap };
    const heights = ls.map((l) => size[l.tier] * gap[l.tier]);
    let y = capY - heights.reduce((a, b) => a + b, 0);
    const fadeOut = 90;
    ls.forEach((l, li) => {
      y += heights[li];
      const firstOut = mapTime(l.words[0].start, keep);
      const lineStart = li === 0 ? span.start : Math.max(span.start, Math.min(span.end - 0.1, firstOut ?? span.start));
      const rel = (w) => {
        const t = mapTime(w.start, keep);
        return ms((t ?? lineStart) - lineStart);
      };
      const style = l.tier === 'small' ? 'Lead' : l.tier === 'script' ? 'Accent' : 'Key';
      const rise = px(l.tier === 'script' ? 22 : 16);
      const text = l.words.map((w) => {
        const t0 = rel(w);
        const reveal = `\\alpha&HFF&\\blur${px(7)}\\t(${t0},${t0 + 170},\\alpha&H00&\\blur0)`;
        const txt = word(w);
        if (w.style === 'box' && l.tier === 'big') return `{\\rEmph${reveal}\\3a&HFF&\\t(${t0},${t0 + 140},\\3a&H00&)}${txt}{\\r${style}}`;
        if (w.style === 'color') return `{\\1c${assColor(col.accent)}${reveal}}${txt}{\\r${style}}`;
        return `{${reveal}}${txt}`;
      }).join(' ');
      ev(3, lineStart, span.end, style, `{\\an2\\q2\\move(${x},${Math.round(y + rise)},${x},${Math.round(y)},0,220)\\fad(0,${fadeOut})}${text}`);

      // Ornamen lengkung merah di bawah kata bergaya 'arc', tergambar dari kiri ke kanan.
      l.words.forEach((w, wi) => {
        if (w.style !== 'arc') return;
        const lineW = estWidth(l.words.map((x) => x.text).join(' '), size[l.tier], l.tier, tierFont[l.tier]);
        const before = estWidth(l.words.slice(0, wi).map((x) => x.text).join(' ') + (wi ? ' ' : ''), size[l.tier], l.tier, tierFont[l.tier]);
        const ww = Math.max(px(70), estWidth(w.text.replace(/[.,!?;:]+$/, ''), size[l.tier], l.tier, tierFont[l.tier]));
        const ax = Math.round(x - lineW / 2 + before - ww * 0.04);
        const ay = Math.round(y + px(4));
        const ah = px(30);
        const t0 = rel(w) + 120;
        ev(2, lineStart, span.end, 'Shape', `{\\an7\\pos(${ax},${ay})\\1c${assColor(col.accent)}\\bord0\\shad0\\clip(${ax},${ay - ah},${ax},${ay + ah * 2})\\t(${t0},${t0 + 320},\\clip(${ax},${ay - ah},${Math.round(ax + ww * 1.15)},${ay + ah * 2}))\\fad(0,${fadeOut})\\p1}${arcPath(ww * 1.05, ah)}{\\p0}`);
      });
    });
  }

  // ---------------- Hook lockup (bible: kata besar "slam" 112%→100% dalam 6 frame) ----------------
  if (hookOn) {
    const { start, end } = hookSpan;
    const maxW = capWidth;
    const fit = (text, size, font) => {
      const w = estWidth(text, size, 'bold', font) * 0.96;
      return w > maxW ? Math.floor((size * maxW) / w) : size;
    };
    const big = String(hook.big).trim();
    const bigBase = px(big.length <= 9 ? 200 : big.length <= 12 ? 150 : 112);
    const bigSize = fit(big, bigBase, fonts.key);
    const leadSize = hook.lead ? fit(hook.lead, px(46), fonts.lead) : 0;
    const accSize = hook.accent ? fit(hook.accent, px(124), fonts.accent) : 0;
    const x = Math.round(W / 2);
    const bottom = Math.round(Math.min(H * (1 - (st.safeZone?.bottom ?? 0.22)), H * 0.73));
    let y = bottom - (accSize ? accSize * 0.95 : 0);
    const out = `\\fad(0,90)`;
    if (accSize) ev(4, start, end, 'HookAccent', `{\\an2\\fs${accSize}\\alpha&HFF&\\t(260,420,\\alpha&H00&)\\move(${x},${bottom + px(18)},${x},${bottom},260,460)${out}}${esc(hook.accent)}`);
    ev(4, start, end, 'HookBig', `{\\an2\\pos(${x},${Math.round(y)})\\fs${bigSize}\\fsp${-Math.round(bigSize * 0.035)}\\fscx112\\fscy112\\t(0,200,\\fscx100\\fscy100)${out}}${esc(big)}`);
    y -= bigSize * 0.88;
    if (leadSize) ev(4, start, end, 'HookLead', `{\\an2\\pos(${x},${Math.round(y)})\\fs${leadSize}\\alpha&HFF&\\t(0,140,\\alpha&H00&)${out}}${esc(hook.lead)}`);
  }

  // ---------------- Kartu visual (animasi bertahap) ----------------
  for (const card of project.cards || []) {
    // Kartu yang sudah dirender HyperFrames ditumpuk sebagai video; jangan digambar ulang di ASS.
    if (!card.approved || skipCards.has(card.id)) continue;
    const span = mapSpan(card.start, card.end, keep);
    if (!span || span.end - span.start < 0.1) continue;
    const dur = ms(span.end - span.start);
    const fadeIn = Math.round(st.cards.fadeMs ?? 150);
    const out = `\\fad(0,90)`;
    // Zoom-out pelan sepanjang kartu (Ken Burns) — dimulai setelah animasi masuk.
    const drift = (from = 104, to = 96, startAt = 260) => `\\fscx${from}\\fscy${from}\\t(${startAt},${dur},\\fscx${to}\\fscy${to})`;
    const full = card.layout !== 'panel' && card.layout !== 'overlay' && card.type !== 'chat';
    const cx = Math.round(W / 2);
    let cy;
    if (full) {
      // Dengan latar kertas (overlay PNG di render), kotak latar ASS tidak perlu.
      if (!paper) ev(5, span.start, span.end, 'Shape', `{\\an7\\pos(0,0)\\p1}${rect(0, 0, W, H)}{\\p0}`);
      cy = Math.round(H * 0.47);
      if (st.cards.grid) {
        const gw = px(760), gh = px(520), step = px(52);
        const parts = [];
        for (let gx = 0; gx <= gw; gx += step) parts.push(rect(gx, 0, Math.max(1, px(2)), gh));
        for (let gy = 0; gy <= gh; gy += step) parts.push(rect(0, gy, gw, Math.max(1, px(2))));
        ev(6, span.start, span.end, 'Shape', `{\\an5\\pos(${cx},${cy})\\1c${assColor('#000000')}\\1a&HFF&\\t(0,300,\\1a&HEC&)${drift(102, 94, 0)}${out}\\p1}${parts.join(' ')}{\\p0}`);
      }
    } else {
      const pw = W - side * 2, ph = px(card.icon ? 640 : 560);
      const top = Math.round(Math.min(safeBottom - ph, H * (st.faceZone?.bottom ?? 0.5) + px(20)));
      ev(5, span.start, span.end, 'Shape', `{\\an7\\pos(${side},${top})\\shad${px(st.cards.shadow ?? 6)}\\4c&H000000&\\4a&HC8&\\fad(${fadeIn},90)\\p1}${roundedRect(pw, ph, px(36))}{\\p0}`);
      cy = top + Math.round(ph / 2) + (card.icon ? px(70) : 0);
    }
    const kicker = esc(card.kicker || '');
    const sub = esc(card.subtitle || '');
    const labelH = px(st.cards.labelSize) * 1.3;
    let titleSize, titleLines, titleText, wrapped = [];
    if (card.type === 'number') {
      // Angka mengisi ±70% lebar aman (seperti "10K" di referensi), maks 1,6× ukuran dasar.
      const unit = estWidth(card.title || '0', 1, 'bold', fonts.card);
      titleSize = Math.round(Math.min(px(st.cards.numberSize) * 1.6, ((W - side * 2) * 0.7) / Math.max(0.5, unit)));
      titleLines = 1;
      titleText = esc(card.title || '');
    } else {
      titleSize = px(st.cards.titleSize * (card.type === 'list' ? 0.8 : 0.85));
      wrapped = wrapWidth(card.title || '', (W - side * 2) * 0.88, (t) => estWidth(t, titleSize, 'bold', fonts.key));
      titleLines = wrapped.length;
      titleText = wrapped.map(esc).join('\\N');
    }
    const titleH = titleSize * (card.type === 'number' ? 1.0 : 1.3) * titleLines;
    let top = cy - titleH / 2;
    const items = card.type === 'list' ? String(card.subtitle || '').split(/\s*[;|]\s*/).filter(Boolean).slice(0, 5) : [];
    if (card.type === 'list') top = cy - (titleH + labelH * 1.4 * Math.max(1, items.length)) / 2;
    const kickerY = top - labelH * 0.75;

    // Ikon: muncul dengan putaran & pantulan.
    if (card.icon && ICONS[card.icon]) {
      const size = px(130);
      const iy = Math.round((kicker ? kickerY - labelH * 0.6 : top - px(30)) - size / 2);
      ev(7, span.start, span.end, 'Shape', `{\\an5\\pos(${cx},${iy})\\1c${assColor(col.accent)}\\bord0\\shad0\\fscx0\\fscy0\\frz-25\\t(60,240,\\fscx${Math.round(size * 1.15)}\\fscy${Math.round(size * 1.15)}\\frz0)\\t(240,330,\\fscx${size}\\fscy${size})${out}\\p1}${ICONS[card.icon]}{\\p0}`);
    }
    // Label atas: turun pelan & muncul.
    if (kicker) {
      const ky = Math.round(kickerY + labelH * 0.5);
      ev(7, span.start, span.end, 'CardLabel', `{\\an2\\move(${cx},${ky - px(14)},${cx},${ky},0,240)\\alpha&HFF&\\t(0,220,\\alpha&H00&)${out}}${kicker}`);
    }
    if (card.type === 'number') {
      // Angka "dibanting" masuk (besar + blur → tajam), dengan ekstrusi 3D berlapis, lalu zoom-out pelan.
      const slam = `\\alpha&HFF&\\blur${px(12)}\\fscx135\\fscy135\\t(0,230,\\alpha&H00&\\blur0\\fscx104\\fscy104)\\t(230,${dur},\\fscx95\\fscy95)`;
      const depth = Math.max(4, px(14));
      const nw = estWidth(card.title || '', titleSize, 'bold', fonts.card);
      // Blok merah transparan di belakang sebagian angka (aksen seperti referensi).
      const bw = Math.round(Math.max(nw * 0.45, titleSize * 0.3)), bh = Math.round(titleSize * 0.28);
      const bx = Math.round(cx + nw * 0.08), by = Math.round(cy - bh * 0.05);
      ev(7, span.start, span.end, 'Shape', `{\\an7\\pos(${bx},${by})\\1c${assColor(col.accent)}\\1a&H70&\\bord0\\shad0\\clip(${bx},${by},${bx},${by + bh})\\t(200,420,\\clip(${bx},${by},${bx + bw},${by + bh}))${out}\\p1}${rect(0, 0, bw, bh)}{\\p0}`);
      ev(7, span.start, span.end, 'Card', `{\\an5\\pos(${cx + depth},${cy + depth * 1.6})\\fs${titleSize}\\1c&H000000&\\1a&HA8&\\blur${px(18)}${slam}${out}}${titleText}`);
      for (let d = depth; d >= 1; d -= Math.max(1, Math.round(depth / 7))) {
        ev(8, span.start, span.end, 'Card', `{\\an5\\pos(${cx + Math.round(d * 0.6)},${cy + d})\\fs${titleSize}\\1c${assColor(shade(col.accent, -0.55 + (0.25 * (depth - d)) / depth))}${slam}${out}}${titleText}`);
      }
      ev(9, span.start, span.end, 'Card', `{\\an5\\pos(${cx},${cy})\\fs${titleSize}\\1c${assColor(col.accent)}${slam}${out}}${titleText}`);
      if (sub) ev(9, span.start, span.end, 'CardLabel', `{\\an8\\pos(${cx},${Math.round(top + titleH + labelH * 0.15)})\\alpha&HFF&\\t(260,460,\\alpha&H00&)${out}}${sub}`);
    } else if (card.type === 'list') {
      ev(7, span.start, span.end, 'Card', `{\\an8\\pos(${cx},${Math.round(top)})\\fs${titleSize}\\alpha&HFF&\\t(0,200,\\alpha&H00&)${out}}${titleText}`);
      items.forEach((it, i) => {
        const iy = Math.round(top + titleH + labelH * 0.3 + i * labelH * 1.4);
        const t0 = 220 + i * 160;
        ev(7, span.start, span.end, 'CardLabel', `{\\an8\\move(${cx - px(30)},${iy},${cx},${iy},${t0},${t0 + 220})\\1c${assColor(col.cardText)}\\alpha&HFF&\\t(${t0},${t0 + 200},\\alpha&H00&)${out}}✓ ${esc(it)}`);
      });
    } else if (st.cards?.theme === 'brandfixer') {
      // Editorial Diagnosis: Archivo ink "slam" + frasa Fraunces + coretan bawah terracotta.
      const tc = assColor(col.cardText);
      ev(8, span.start, span.end, 'Card', `{\\an5\\pos(${cx},${cy})\\fs${titleSize}\\fn${fonts.key}\\1c${tc}\\fscx112\\fscy112\\t(0,200,\\fscx100\\fscy100)${out}}${titleText}`);
      const uw = px(360), uy = Math.round(cy + titleH / 2 + px(10)), ux = Math.round(cx - uw / 2);
      ev(8, span.start, span.end, 'Shape', `{\\an7\\pos(${ux},${uy})\\1c${assColor(col.accent)}\\bord0\\shad0\\clip(${ux},${uy - px(20)},${ux},${uy + px(40)})\\t(300,750,\\clip(${ux},${uy - px(20)},${ux + uw + px(10)},${uy + px(40)}))${out}\\p1}${arcPath(uw, px(14))}{\\p0}`);
      if (sub) ev(8, span.start, span.end, 'CardAccent', `{\\an8\\pos(${cx},${uy + px(40)})\\1c${tc}\\alpha&HFF&\\t(320,520,\\alpha&H00&)${out}}${sub}`);
    } else {
      // Judul kotak merah dengan "bayangan" blok gelap ter-offset (efek 3D), terbuka dari kiri ke kanan.
      const tw = Math.max(...wrapped.map((l) => estWidth(l, titleSize, 'bold', fonts.key))) + px(40);
      const x0 = Math.round(cx - tw / 2 - px(30)), x1 = Math.round(cx + tw / 2 + px(40));
      const y0 = Math.round(cy - titleH), y1 = Math.round(cy + titleH);
      const wipe = (delay) => `\\clip(${x0},${y0},${x0},${y1})\\t(${delay},${delay + 280},\\clip(${x0},${y0},${x1},${y1}))`;
      ev(7, span.start, span.end, 'CardBoxShade', `{\\an5\\pos(${cx + px(12)},${cy + px(12)})\\fs${titleSize}${wipe(80)}${drift(103, 97, 360)}${out}}${titleText}`);
      ev(8, span.start, span.end, 'CardBox', `{\\an5\\pos(${cx},${cy})\\fs${titleSize}${wipe(40)}${drift(103, 97, 360)}${out}}${titleText}`);
      if (sub) ev(8, span.start, span.end, 'CardLabel', `{\\an8\\pos(${cx},${Math.round(top + titleH + labelH * 0.4)})\\alpha&HFF&\\t(320,520,\\alpha&H00&)${out}}${sub}`);
    }
  }

  // ---------------- End card (cadangan bila HyperFrames tidak dipakai) ----------------
  if (endSpan && !skipCards.has('endcard')) {
    const ec = { ...(st.endcard || {}), ...(project.endcard || {}) };
    const { start, end } = endSpan;
    const x = Math.round(W / 2), cy = Math.round(H * 0.5);
    ev(5, start, end, 'Shape', `{\\an7\\pos(0,0)\\1c${assColor(col.inkSoft || '#2A2824')}\\p1}${rect(0, 0, W, H)}{\\p0}`);
    const big = String(ec.big || '').trim();
    const bs = Math.min(px(big.length <= 9 ? 200 : 150), Math.floor(capWidth / Math.max(0.3, estWidth(big, 1, 'bold', fonts.key))));
    if (ec.lead) ev(6, start, end, 'HookLead', `{\\an2\\pos(${x},${cy - Math.round(bs * 0.9)})\\fad(150,0)}${esc(ec.lead)}`);
    if (big) ev(6, start, end, 'HookBig', `{\\an2\\pos(${x},${cy})\\fs${bs}\\fsp${-Math.round(bs * 0.035)}\\fscx112\\fscy112\\t(100,300,\\fscx100\\fscy100)}${esc(big)}`);
    if (ec.accent) ev(6, start, end, 'HookAccent', `{\\an8\\pos(${x},${cy + px(10)})\\fs${px(120)}\\fad(300,0)}${esc(ec.accent)}`);
    ev(6, start, end, 'HookLead', `{\\an8\\pos(${x},${cy + px(220)})\\fs${px(26)}\\fad(500,0)}aldy syahreza · the brand fixer`);
  }

  return [
    '[Script Info]',
    'ScriptType: v4.00+',
    `PlayResX: ${W}`,
    `PlayResY: ${H}`,
    'WrapStyle: 0',
    'ScaledBorderAndShadow: yes',
    'YCbCr Matrix: TV.709',
    '',
    '[V4+ Styles]',
    'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
    ...styles,
    '',
    '[Events]',
    'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text',
    ...lines,
    '',
  ].join('\n');
}

/** Gelapkan/terangkan warna hex (amount -1..1). */
export function shade(hex, amount) {
  const m = String(hex).replace('#', '');
  const ch = [0, 2, 4].map((i) => parseInt(m.slice(i, i + 2), 16));
  const out = ch.map((c) => Math.round(amount < 0 ? c * (1 + amount) : c + (255 - c) * amount));
  return `#${out.map((c) => Math.max(0, Math.min(255, c)).toString(16).padStart(2, '0')).join('')}`;
}
