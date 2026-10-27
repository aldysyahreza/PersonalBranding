// Membangun file subtitle ASS (libass) untuk caption + kartu visual.
// Semua posisi dihitung dalam piksel output; semua waktu sudah dipetakan
// ke timeline output (setelah cut).
import { buildPhrases, splitLeadKey, mapSpan } from '../../public/shared/core.js';

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

export function buildAss(project, { width: W, height: H, keep }) {
  const st = project.style;
  const cap = st.captions;
  const col = st.colors;
  const k = Math.min(W, H) / 1080;
  const px = (n) => Math.round(n * k);
  const side = Math.round(W * (st.safeZone?.side ?? 0.06));
  const safeTop = H * (st.safeZone?.top ?? 0.12);
  const safeBottom = H * (1 - (st.safeZone?.bottom ?? 0.2));
  const capY = Math.round(Math.min(safeBottom, Math.max(safeTop + px(cap.keySize) * 2, H * cap.position)));
  const shadow = cap.shadow ?? 3;
  const lines = [];
  const ev = (layer, start, end, style, text) => lines.push(`Dialogue: ${layer},${ts(start)},${ts(end)},${style},,0,0,0,,${text}`);

  const emphBox = cap.emphasis === 'box';
  const styles = [
    `Style: Lead,${st.fonts.lead},${px(cap.leadSize)},${assColor(col.text)},${assColor(col.text)},&H00000000,&H78000000,0,0,0,0,100,100,0,0,1,0,${shadow * 0.7},2,${side},${side},0,1`,
    `Style: Key,${st.fonts.key},${px(cap.keySize)},${assColor(col.text)},${assColor(col.text)},&H00000000,&H78000000,-1,0,0,0,100,100,0,0,1,0,${shadow},2,${side},${side},0,1`,
    emphBox
      ? `Style: Emph,${st.fonts.key},${px(cap.keySize)},${assColor(col.text)},${assColor(col.text)},${assColor(col.accent)},&H00000000,-1,0,0,0,100,100,0,0,3,${px(10)},0,2,${side},${side},0,1`
      : `Style: Emph,${st.fonts.key},${px(cap.keySize)},${assColor(cap.emphasis === 'color' ? col.accent : col.text)},${assColor(col.text)},&H00000000,&H78000000,-1,0,0,0,100,100,0,0,1,0,${shadow},2,${side},${side},0,1`,
    `Style: Card,${st.fonts.card},${px(st.cards.titleSize)},${assColor(col.cardText)},${assColor(col.cardText)},&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,0,0,5,${side},${side},0,1`,
    `Style: CardLabel,${st.fonts.lead},${px(st.cards.labelSize)},${assColor(col.cardMuted)},${assColor(col.cardMuted)},&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,${side},${side},0,1`,
    `Style: CardBox,${st.fonts.key},${px(st.cards.titleSize)},${assColor('#FFFFFF')},${assColor('#FFFFFF')},${assColor(col.accent)},&H00000000,-1,0,0,0,100,100,0,0,3,${px(14)},0,5,${side},${side},0,1`,
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
    for (const ph of phrases) {
      const span = mapSpan(ph.start, ph.end, keep);
      if (!span || span.end - span.start < 0.05) continue;
      const x = Math.round(W / 2);
      if (cap.layout === 'stack') {
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
  }

  // ---------------- Kartu visual ----------------
  for (const card of project.cards || []) {
    if (!card.approved) continue;
    const span = mapSpan(card.start, card.end, keep);
    if (!span || span.end - span.start < 0.1) continue;
    const fade = Math.round(st.cards.fadeMs ?? 150);
    const f = `\\fad(${fade},${Math.round(fade * 0.7)})`;
    const pop = `\\fscx90\\fscy90\\t(0,${fade + 60},\\fscx100\\fscy100)`;
    const full = card.layout !== 'panel';
    const cx = Math.round(W / 2);
    let cy;
    if (full) {
      ev(5, span.start, span.end, 'Shape', `{\\an7\\pos(0,0)\\p1${f}}${rect(0, 0, W, H)}{\\p0}`);
      cy = Math.round(H * 0.47);
      if (st.cards.grid) {
        const gw = px(760), gh = px(520), step = px(52), gx = Math.round(cx - gw / 2), gy = Math.round(cy - gh / 2);
        const parts = [];
        for (let x = 0; x <= gw; x += step) parts.push(rect(gx + x, gy, Math.max(1, px(2)), gh));
        for (let y = 0; y <= gh; y += step) parts.push(rect(gx, gy + y, gw, Math.max(1, px(2))));
        ev(6, span.start, span.end, 'Shape', `{\\an7\\pos(0,0)\\1c${assColor('#000000')}\\1a&HEE&\\p1${f}}${parts.join(' ')}{\\p0}`);
      }
    } else {
      const pw = W - side * 2, ph = px(card.icon ? 640 : 560);
      const top = Math.round(Math.min(safeBottom - ph, H * (st.faceZone?.bottom ?? 0.5) + px(20)));
      ev(5, span.start, span.end, 'Shape', `{\\an7\\pos(${side},${top})\\shad${px(st.cards.shadow ?? 6)}\\4c&H000000&\\4a&HC8&\\p1${f}}${roundedRect(pw, ph, px(36))}{\\p0}`);
      cy = top + Math.round(ph / 2) + (card.icon ? px(70) : 0);
    }
    const kicker = esc(card.kicker || '');
    const sub = esc(card.subtitle || '');
    const sh = `\\shad${px(st.cards.shadow ?? 6)}\\4c&H000000&\\4a&HB4&`;
    const labelH = px(st.cards.labelSize) * 1.3;
    // Tinggi blok judul menentukan posisi label & ikon agar tidak bertumpuk.
    let titleSize, titleLines, titleText;
    if (card.type === 'number') {
      // Angka tidak dibungkus; perkecil bila lebih lebar dari area aman.
      const est = String(card.title || '').length * 0.62 * px(st.cards.numberSize);
      titleSize = Math.round(px(st.cards.numberSize) * Math.min(1, (W - side * 2) / Math.max(1, est)));
      titleLines = 1;
      titleText = esc(card.title || '');
    } else {
      titleSize = px(st.cards.titleSize * (card.type === 'list' ? 0.8 : 0.85));
      const maxChars = Math.max(8, Math.round(((W - side * 2) / titleSize) * 1.9));
      const wrapped = wrap(card.title || '', maxChars);
      titleLines = wrapped.length;
      titleText = wrapped.map(esc).join('\\N');
    }
    const titleH = titleSize * (card.type === 'number' ? 1.0 : 1.3) * titleLines;
    let top = cy - titleH / 2;
    if (card.type === 'list') top = cy - (titleH + labelH * 1.4 * Math.max(1, String(card.subtitle || '').split(/\s*[;|]\s*/).filter(Boolean).length)) / 2;
    const kickerY = top - labelH * 0.75;
    if (card.icon && ICONS[card.icon]) {
      const size = px(130);
      const iy = Math.round((kicker ? kickerY - labelH * 0.6 : top - px(30)) - size);
      ev(7, span.start, span.end, 'Shape', `{\\an7\\pos(${cx - size / 2},${iy})\\1c${assColor(col.accent)}\\fscx${size}\\fscy${size}\\p1${f}}${ICONS[card.icon]}{\\p0}`);
    }
    if (kicker) ev(7, span.start, span.end, 'CardLabel', `{\\an2\\pos(${cx},${Math.round(kickerY + labelH * 0.5)})${f}}${kicker}`);
    if (card.type === 'number') {
      ev(7, span.start, span.end, 'Card', `{\\an5\\q2\\pos(${cx},${cy})\\fs${titleSize}\\1c${assColor(col.accent)}${sh}${f}${pop}}${titleText}`);
      if (sub) ev(7, span.start, span.end, 'CardLabel', `{\\an8\\pos(${cx},${Math.round(top + titleH + labelH * 0.1)})${f}}${sub}`);
    } else if (card.type === 'list') {
      const items = String(card.subtitle || '').split(/\s*[;|]\s*/).filter(Boolean).slice(0, 5);
      ev(7, span.start, span.end, 'Card', `{\\an8\\pos(${cx},${Math.round(top)})\\fs${titleSize}${f}}${titleText}`);
      items.forEach((it, i) => {
        ev(7, span.start, span.end, 'CardLabel', `{\\an8\\pos(${cx},${Math.round(top + titleH + labelH * 0.3 + i * labelH * 1.4)})\\1c${assColor(col.cardText)}${f}}• ${esc(it)}`);
      });
    } else {
      ev(7, span.start, span.end, 'CardBox', `{\\an5\\pos(${cx},${cy})\\fs${titleSize}${f}${pop}}${titleText}`);
      if (sub) ev(7, span.start, span.end, 'CardLabel', `{\\an8\\pos(${cx},${Math.round(top + titleH + labelH * 0.3)})${f}}${sub}`);
    }
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
