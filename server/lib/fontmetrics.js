// Pengukur lebar teks dari file font asli (TTF/OTF) di assets/fonts — membaca tabel
// name, head, hhea, hmtx, dan cmap (format 4/12). Dipakai untuk menempatkan ornamen
// (garis lengkung, blok aksen) dan memilih ukuran angka secara akurat. Kerning diabaikan.
import fs from 'node:fs';
import path from 'node:path';
import { config } from './config.js';

const cache = new Map(); // nama lengkap (lowercase) → metrik
let indexed = false;

function parse(file) {
  const b = fs.readFileSync(file);
  const numTables = b.readUInt16BE(4);
  const tables = {};
  for (let i = 0; i < numTables; i++) {
    const o = 12 + i * 16;
    tables[b.toString('latin1', o, o + 4)] = { off: b.readUInt32BE(o + 8), len: b.readUInt32BE(o + 12) };
  }
  if (!tables.head || !tables.hhea || !tables.hmtx || !tables.cmap) return null;
  const unitsPerEm = b.readUInt16BE(tables.head.off + 18);
  const numHMetrics = b.readUInt16BE(tables.hhea.off + 34);
  const adv = [];
  for (let i = 0; i < numHMetrics; i++) adv.push(b.readUInt16BE(tables.hmtx.off + i * 4));

  // cmap: pilih subtabel Unicode (format 12 atau 4).
  const cm = tables.cmap.off;
  const n = b.readUInt16BE(cm + 2);
  let sub = null;
  for (let i = 0; i < n; i++) {
    const pid = b.readUInt16BE(cm + 4 + i * 8), eid = b.readUInt16BE(cm + 6 + i * 8);
    const off = cm + b.readUInt32BE(cm + 8 + i * 8);
    const fmt = b.readUInt16BE(off);
    if ((pid === 3 && (eid === 1 || eid === 10)) || pid === 0) {
      if (fmt === 12 || (fmt === 4 && (!sub || sub.fmt !== 12))) sub = { off, fmt };
    }
  }
  const glyphOf = (code) => {
    if (!sub) return 0;
    const o = sub.off;
    if (sub.fmt === 12) {
      const groups = b.readUInt32BE(o + 12);
      for (let g = 0; g < groups; g++) {
        const s = b.readUInt32BE(o + 16 + g * 12), e = b.readUInt32BE(o + 20 + g * 12);
        if (code >= s && code <= e) return b.readUInt32BE(o + 24 + g * 12) + (code - s);
      }
      return 0;
    }
    const segX2 = b.readUInt16BE(o + 6);
    const ends = o + 14, starts = ends + segX2 + 2, deltas = starts + segX2, ranges = deltas + segX2;
    for (let i = 0; i < segX2 / 2; i++) {
      const end = b.readUInt16BE(ends + i * 2);
      if (code > end) continue;
      const start = b.readUInt16BE(starts + i * 2);
      if (code < start) return 0;
      const delta = b.readInt16BE(deltas + i * 2);
      const ro = b.readUInt16BE(ranges + i * 2);
      if (!ro) return (code + delta) & 0xffff;
      const gi = b.readUInt16BE(ranges + i * 2 + ro + (code - start) * 2);
      return gi ? (gi + delta) & 0xffff : 0;
    }
    return 0;
  };

  // Nama lengkap (nameID 4) untuk dicocokkan dengan nama font di gaya ASS.
  const names = [];
  if (tables.name) {
    const no = tables.name.off;
    const count = b.readUInt16BE(no + 2), strOff = no + b.readUInt16BE(no + 4);
    for (let i = 0; i < count; i++) {
      const r = no + 6 + i * 12;
      const pid = b.readUInt16BE(r), nameId = b.readUInt16BE(r + 6), len = b.readUInt16BE(r + 8), off = b.readUInt16BE(r + 10);
      if (nameId !== 4 && nameId !== 1) continue;
      const raw = b.subarray(strOff + off, strOff + off + len);
      names.push(pid === 1 ? raw.toString('latin1') : raw.swap16 ? Buffer.from(raw).swap16().toString('utf16le') : '');
    }
  }
  const widthCache = new Map();
  return {
    names,
    width(text, size) {
      let u = 0;
      for (const ch of String(text)) {
        let w = widthCache.get(ch);
        if (w === undefined) {
          const g = glyphOf(ch.codePointAt(0));
          w = adv[Math.min(g, adv.length - 1)] ?? unitsPerEm * 0.6;
          widthCache.set(ch, w);
        }
        u += w;
      }
      return (u / unitsPerEm) * size;
    },
  };
}

function index() {
  if (indexed) return;
  indexed = true;
  for (const f of fs.readdirSync(config.fontsDir).filter((x) => /\.(ttf|otf)$/i.test(x))) {
    try {
      const m = parse(path.join(config.fontsDir, f));
      if (!m) continue;
      for (const nm of m.names) if (nm && !cache.has(nm.toLowerCase())) cache.set(nm.toLowerCase(), m);
    } catch {
      /* font tidak terbaca: abaikan, estimasi cadangan dipakai */
    }
  }
}

/** Lebar teks (px) untuk font bernama (mis. "Montserrat ExtraBold"); null bila font tidak ada di bundel. */
export function measure(fontName, text, size) {
  index();
  const m = cache.get(String(fontName).toLowerCase());
  return m ? m.width(text, size) : null;
}
