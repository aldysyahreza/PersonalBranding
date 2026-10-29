// Logika murni yang dipakai BERSAMA oleh server (render) dan browser (preview),
// supaya preview dan hasil ekspor memakai aturan yang sama persis:
// pemotongan (cut), pemetaan waktu, pemecahan subtitle, dan sinkron kata.
// Tidak boleh mengimpor modul Node atau DOM di sini.

export const uid = (p = 'id') => `${p}_${Math.random().toString(36).slice(2, 9)}`;
export const r3 = (n) => Math.round(n * 1000) / 1000;

/* ----------------------------- Cut & waktu ----------------------------- */

/** Rentang sumber yang DIPERTAHANKAN setelah cut aktif dibuang. */
export function keepSegments(duration, cuts = []) {
  const active = cuts
    .filter((c) => c.enabled)
    .map((c) => ({ start: Math.max(0, c.start), end: Math.min(duration, c.end) }))
    .filter((c) => c.end - c.start > 0.01)
    .sort((a, b) => a.start - b.start);
  const keep = [];
  let t = 0;
  for (const c of active) {
    if (c.start > t + 0.01) keep.push({ start: r3(t), end: r3(c.start) });
    t = Math.max(t, c.end);
  }
  if (duration > t + 0.01) keep.push({ start: r3(t), end: r3(duration) });
  return keep;
}

export function outputDuration(keep) {
  return r3(keep.reduce((s, k) => s + (k.end - k.start), 0));
}

/** Kurangi rentang [start,end] dengan blok-blok (mis. waktu kartu); hasil: sisa rentang ≥ minLen. */
export function subtractRanges(range, blocks, minLen = 0.15) {
  let parts = [{ start: range.start, end: range.end }];
  for (const b of blocks) {
    parts = parts.flatMap((p) => {
      if (b.end <= p.start || b.start >= p.end) return [p];
      const out = [];
      if (b.start > p.start) out.push({ start: p.start, end: b.start });
      if (b.end < p.end) out.push({ start: b.end, end: p.end });
      return out;
    });
  }
  return parts.filter((p) => p.end - p.start >= minLen);
}

/** Waktu sumber -> waktu output. Waktu di dalam bagian yang dipotong mengembalikan null. */
export function mapTime(t, keep) {
  let acc = 0;
  for (const k of keep) {
    if (t < k.start - 1e-6) return null;
    if (t <= k.end + 1e-6) return r3(acc + (Math.min(t, k.end) - k.start));
    acc += k.end - k.start;
  }
  return null;
}

/** Rentang sumber -> daftar rentang output (bisa terpecah jika ada cut di tengah). */
export function mapRange(start, end, keep) {
  const out = [];
  let acc = 0;
  for (const k of keep) {
    const s = Math.max(start, k.start);
    const e = Math.min(end, k.end);
    if (e - s > 0.02) out.push({ start: r3(acc + s - k.start), end: r3(acc + e - k.start) });
    acc += k.end - k.start;
  }
  return out;
}

/** Rentang sumber -> satu rentang output utuh (awal pertama s.d. akhir terakhir) atau null. */
export function mapSpan(start, end, keep) {
  const parts = mapRange(start, end, keep);
  if (!parts.length) return null;
  return { start: parts[0].start, end: parts[parts.length - 1].end };
}

export function isCut(t, cuts = []) {
  return cuts.some((c) => c.enabled && t >= c.start && t < c.end);
}

/* ----------------------------- Zoom punch-in ----------------------------- */

/** Faktor zoom (punch-in) yang disetujui pada waktu sumber t; 1 bila tidak ada. */
export function zoomAt(t, zooms = []) {
  const z = zooms.find((x) => x.approved && t >= x.start && t < x.end);
  return z ? Math.max(1, Number(z.zoom) || 1) : 1;
}

/**
 * Pecah rentang keep di batas zoom, sehingga tiap potongan punya satu faktor zoom.
 * Dipakai render: tiap potongan di-scale/crop sendiri lalu disambung (jump-cut zoom).
 */
export function zoomPieces(keep, zooms = []) {
  const active = zooms.filter((z) => z.approved);
  const cuts = new Set(active.flatMap((z) => [z.start, z.end]));
  const pieces = [];
  for (const k of keep) {
    const pts = [k.start, ...[...cuts].filter((x) => x > k.start + 0.02 && x < k.end - 0.02).sort((a, b) => a - b), k.end];
    for (let i = 0; i < pts.length - 1; i++) {
      const mid = (pts[i] + pts[i + 1]) / 2;
      const zoom = zoomAt(mid, active);
      const prev = pieces[pieces.length - 1];
      // Gabungkan potongan bersebelahan dengan zoom sama (tanpa cut di antaranya).
      if (prev && prev.zoom === zoom && Math.abs(prev.end - pts[i]) < 1e-6) prev.end = r3(pts[i + 1]);
      else pieces.push({ start: r3(pts[i]), end: r3(pts[i + 1]), zoom });
    }
  }
  return pieces;
}

/* ----------------------------- Ritme (pacing) ----------------------------- */

export const DEFAULT_PACING = { minFaceGap: 2.5, minCard: 2.0, maxCard: 3.5, minZoom: 2.0, firstCardAt: 1.0 };

/**
 * Rapikan ritme agar adegan wajah tidak terlalu cepat:
 *  - kartu yang terlalu rapat dengan kartu sebelumnya dinonaktifkan (bukan dihapus — bisa disetujui lagi);
 *  - kartu terlalu singkat diperpanjang (tanpa melanggar jeda wajah), terlalu lama dipendekkan;
 *  - zoom terlalu singkat dibuang, zoom yang hampir bersambung digabung.
 * Mengembalikan salinan baru + daftar perubahan yang bisa ditampilkan ke pengguna.
 */
export function enforcePacing({ cards = [], zooms = [], duration = Infinity, pacing = {}, approvedOnly = true }) {
  const P = { ...DEFAULT_PACING, ...pacing };
  const changes = [];
  const label = (c) => `"${c.title || c.type}" (${fmtTime(c.start)})`;
  const out = cards.map((c) => ({ ...c })).sort((a, b) => a.start - b.start);
  const live = (c) => (approvedOnly ? c.approved : !c.rejected);
  let prevEnd = -Infinity;
  for (const c of out) {
    if (!live(c)) continue;
    if (c.start < P.firstCardAt) {
      const d = c.end - c.start;
      c.start = r3(P.firstCardAt);
      c.end = r3(c.start + d);
      changes.push(`Kartu ${label(c)} digeser agar video dibuka dengan wajah.`);
    }
    if (c.start - prevEnd < P.minFaceGap) {
      if (approvedOnly) c.approved = false;
      else c.rejected = true;
      c.pacingNote = `Dinonaktifkan: hanya ${(Math.max(0, c.start - prevEnd)).toFixed(1)} dtk wajah setelah kartu sebelumnya (min ${P.minFaceGap} dtk).`;
      changes.push(`Kartu ${label(c)} dinonaktifkan — terlalu rapat dengan kartu sebelumnya.`);
      continue;
    }
    const len = c.end - c.start;
    if (len < P.minCard) {
      c.end = r3(Math.min(duration, c.start + P.minCard));
      changes.push(`Kartu ${label(c)} diperpanjang menjadi ${(c.end - c.start).toFixed(1)} dtk.`);
    } else if (len > P.maxCard) {
      c.end = r3(c.start + P.maxCard);
      changes.push(`Kartu ${label(c)} dipendekkan menjadi ${P.maxCard} dtk.`);
    }
    prevEnd = c.end;
  }
  // Zoom: gabungkan yang hampir bersambung, buang yang terlalu singkat.
  const zs = zooms.map((z) => ({ ...z })).sort((a, b) => a.start - b.start);
  const merged = [];
  for (const z of zs) {
    const prev = merged[merged.length - 1];
    if (prev && z.approved && prev.approved && z.start - prev.end < P.minZoom) {
      prev.end = Math.max(prev.end, z.end);
      changes.push(`Zoom ${fmtTime(z.start)} digabung dengan zoom sebelumnya (pergantian terlalu cepat).`);
      continue;
    }
    merged.push(z);
  }
  for (const z of merged) {
    if (z.approved && z.end - z.start < P.minZoom) {
      z.approved = false;
      changes.push(`Zoom ${fmtTime(z.start)} dinonaktifkan — kurang dari ${P.minZoom} dtk.`);
    }
  }
  return { cards: out, zooms: merged, changes };
}

/* ----------------------------- Transkrip ----------------------------- */

export function tokenize(text) {
  return String(text || '').trim().split(/\s+/).filter(Boolean);
}

/** Bagi rentang waktu ke kata secara proporsional terhadap panjang kata (estimasi). */
export function estimateWords(text, start, end) {
  const toks = tokenize(text);
  if (!toks.length) return [];
  const weights = toks.map((w) => Math.max(2, w.replace(/[^\p{L}\p{N}]/gu, '').length) + 1);
  const total = weights.reduce((a, b) => a + b, 0);
  const dur = Math.max(0.05, end - start);
  let t = start;
  return toks.map((w, i) => {
    const d = (dur * weights[i]) / total;
    const word = { text: w, start: r3(t), end: r3(t + d) };
    t += d;
    return word;
  });
}

/**
 * Sinkronkan daftar kata dengan teks segmen setelah diedit pengguna.
 * - Jumlah kata sama: pertahankan timestamp + penekanan, ganti teks saja.
 * - Berbeda: estimasi ulang timestamp di dalam rentang segmen (ditandai 'estimated').
 */
export function syncSegmentWords(seg) {
  const toks = tokenize(seg.text);
  const words = seg.words || [];
  if (words.length === toks.length && words.length) {
    seg.words = words.map((w, i) => ({ ...w, text: toks[i] }));
    return seg;
  }
  const emphSet = new Set(words.filter((w) => w.emph).map((w) => normWord(w.text)));
  seg.words = estimateWords(seg.text, seg.start, seg.end).map((w) => ({ ...w, emph: emphSet.has(normWord(w.text)) || undefined }));
  seg.timing = 'estimated';
  return seg;
}

export function normWord(w) {
  return String(w).toLowerCase().replace(/[^\p{L}\p{N}%]/gu, '');
}

/** Bagikan teks ketikan manual ke rentang ucapan hasil deteksi hening (estimasi waktu). */
export function distributeText(text, regions, duration) {
  const sentences = String(text)
    .replace(/\s+/g, ' ')
    .split(/(?<=[.!?…])\s+|\n+/)
    .map((s) => s.trim())
    .filter(Boolean);
  if (!sentences.length) return [];
  const useRegions = regions?.length ? regions : [{ start: 0, end: duration }];
  // Petakan panjang karakter kumulatif ke durasi ucapan kumulatif.
  const speechTotal = useRegions.reduce((s, r) => s + (r.end - r.start), 0);
  const charTotal = sentences.reduce((s, x) => s + x.length, 0);
  const speechToTime = (x) => {
    let acc = 0;
    for (const r of useRegions) {
      const d = r.end - r.start;
      if (x <= acc + d) return r.start + (x - acc);
      acc += d;
    }
    return useRegions[useRegions.length - 1].end;
  };
  let c = 0;
  return sentences.map((s) => {
    const start = speechToTime((c / charTotal) * speechTotal);
    c += s.length;
    const end = speechToTime((c / charTotal) * speechTotal);
    return makeSegment({ start, end, text: s, timing: 'estimated' });
  });
}

export function makeSegment({ start, end, text, words, speaker = '', timing = 'manual' }) {
  const seg = {
    id: uid('seg'),
    start: r3(start),
    end: r3(Math.max(end, start + 0.1)),
    text: String(text).trim(),
    speaker,
    timing,
    words: words?.length ? words.map((w) => ({ text: w.text, start: r3(w.start), end: r3(w.end) })) : null,
  };
  seg.originalText = seg.text;
  if (!seg.words) seg.words = estimateWords(seg.text, seg.start, seg.end);
  return seg;
}

/* ------------------------------ SRT / VTT ------------------------------ */

function parseTs(s) {
  const m = s.trim().replace(',', '.').match(/(?:(\d+):)?(\d+):(\d+(?:\.\d+)?)/);
  if (!m) return NaN;
  return Number(m[1] || 0) * 3600 + Number(m[2]) * 60 + Number(m[3]);
}

export function parseSubtitles(text) {
  const blocks = String(text).replace(/\r/g, '').replace(/^WEBVTT.*\n/, '').split(/\n{2,}/);
  const segs = [];
  for (const b of blocks) {
    const lines = b.split('\n').filter((l) => l.trim() !== '');
    const i = lines.findIndex((l) => l.includes('-->'));
    if (i < 0) continue;
    const [a, z] = lines[i].split('-->');
    const start = parseTs(a);
    const end = parseTs(z.split(/\s/).filter(Boolean)[0] || '');
    const body = lines.slice(i + 1).join(' ').replace(/<[^>]+>/g, '').trim();
    if (!Number.isFinite(start) || !Number.isFinite(end) || !body) continue;
    segs.push(makeSegment({ start, end, text: body, timing: 'imported' }));
  }
  return segs;
}

function fmtTs(t, sep) {
  const ms = Math.round(t * 1000);
  const h = Math.floor(ms / 3600000);
  const m = Math.floor((ms % 3600000) / 60000);
  const s = Math.floor((ms % 60000) / 1000);
  const p = (n, l = 2) => String(n).padStart(l, '0');
  return `${p(h)}:${p(m)}:${p(s)}${sep}${p(ms % 1000, 3)}`;
}

export function toSrt(segments) {
  return segments.map((s, i) => `${i + 1}\n${fmtTs(s.start, ',')} --> ${fmtTs(s.end, ',')}\n${s.text}\n`).join('\n');
}

/* ------------------------------ Subtitle ------------------------------ */

/**
 * Pecah kata-kata menjadi frasa subtitle. Tidak mengubah teks — hanya
 * mengelompokkan kata. Pemecahan mengikuti tanda baca, jeda, dan batas
 * jumlah kata/karakter, bukan pemotongan acak.
 */
export function buildPhrases(segments, { maxWords = 4, maxChars = 26, pauseBreak = 0.35 } = {}) {
  const phrases = [];
  const ordered = [...segments].filter((s) => !s.hidden).sort((a, b) => a.start - b.start);
  for (const seg of ordered) {
    const words = seg.words || [];
    let cur = [];
    const flush = () => {
      if (!cur.length) return;
      phrases.push({ segId: seg.id, start: cur[0].start, end: cur[cur.length - 1].end, words: cur });
      cur = [];
    };
    words.forEach((w, i) => {
      const next = words[i + 1];
      const chars = cur.reduce((s, x) => s + x.text.length + 1, 0) + w.text.length;
      if (cur.length && (cur.length >= maxWords || chars > maxChars)) flush();
      cur.push(w);
      const strongPunct = /[.!?…:;]$/.test(w.text);
      const softPunct = /[,]$/.test(w.text) && cur.length >= 2;
      const gap = next ? next.start - w.end : 0;
      if (strongPunct || softPunct || gap > pauseBreak) flush();
    });
    flush();
  }
  phrases.sort((a, b) => a.start - b.start);
  return dedupePhrases(phrases);
}

const phraseKey = (ph) => ph.words.map((w) => normWord(w.text)).join(' ');

/**
 * Cegah subtitle berulang:
 *  - frasa kembar berurutan (ASR kadang menulis kalimat yang sama dua kali) dibuang;
 *  - frasa yang seluruh katanya sudah tampil di frasa sebelumnya pada waktu yang bertumpuk dibuang;
 *  - waktu yang bertumpuk dipotong sehingga tidak pernah ada dua frasa tampil bersamaan.
 */
export function dedupePhrases(phrases) {
  const out = [];
  for (const ph of phrases) {
    const prev = out[out.length - 1];
    if (prev) {
      const same = phraseKey(prev) === phraseKey(ph);
      const contained = ph.start < prev.end - 0.05 && phraseKey(prev).includes(phraseKey(ph));
      if ((same && ph.start - prev.end < 1.5) || contained) continue;
      if (prev.end > ph.start) prev.end = ph.start;
    }
    out.push({ ...ph });
  }
  // Rapatkan celah kecil antar frasa agar subtitle tidak berkedip; buang frasa yang jadi terlalu pendek.
  for (let i = 0; i < out.length - 1; i++) {
    const gap = out[i + 1].start - out[i].end;
    if (gap > 0 && gap < 0.25) out[i].end = out[i + 1].start;
  }
  return out.filter((ph) => ph.end - ph.start >= 0.12);
}

/** Segmen transkrip yang kemungkinan duplikat ASR (teks sama/terkandung & waktunya bertumpuk/berdekatan). */
export function findDuplicateSegments(segments) {
  const ordered = [...segments].sort((a, b) => a.start - b.start);
  const dup = [];
  const key = (s) => tokenize(s.text).map(normWord).join(' ');
  for (let i = 1; i < ordered.length; i++) {
    const a = ordered[i - 1], b = ordered[i];
    const ka = key(a), kb = key(b);
    if (!kb) continue;
    if ((ka === kb && b.start - a.end < 1.5) || (b.start < a.end - 0.1 && ka.includes(kb))) dup.push(b.id);
  }
  return dup;
}

/* ------------------------- Caption kinetik (gaya referensi) ------------------------- */

// Kata sambung ditampilkan kecil & tipis; kata bermakna besar & tebal (hierarki seperti referensi).
const CONNECTORS = new Set([
  'yang', 'di', 'ke', 'dari', 'dan', 'atau', 'untuk', 'dengan', 'itu', 'ini', 'ada', 'adalah', 'akan', 'juga',
  'sudah', 'lagi', 'kalau', 'jika', 'tapi', 'karena', 'jadi', 'pun', 'sih', 'kok', 'ya', 'si', 'para', 'oleh',
  'pada', 'dalam', 'sebuah', 'seorang', 'bahwa', 'agar', 'supaya', 'lebih', 'paling', 'sangat', 'masih', 'bisa',
  'the', 'a', 'an', 'is', 'are', 'was', 'were', 'of', 'to', 'in', 'on', 'and', 'or', 'that', 'this', 'it', 'so',
  'be', 'as', 'at', 'for', 'if', 'but', 'with', 'your', 'my', 'our',
]);
export const EMPH_CYCLE = ['box', 'arc', 'script'];

/**
 * Tentukan gaya penekanan tiap kata. word.emph boleh true | 'box' | 'arc' | 'script'.
 * true + mode 'mix' → bergiliran box → arc → script di sepanjang video (variasi seperti referensi).
 */
export function resolveEmphasis(phrases, mode = 'mix') {
  let n = 0;
  for (const ph of phrases) {
    // 'serif' (bible The Brand Fixer): satu kata rasa per layar dalam Fraunces Italic, sisanya polos.
    let used = false;
    for (const w of ph.words) {
      if (mode === 'serif') {
        w.style = w.emph && !used ? (typeof w.emph === 'string' && w.emph !== 'script' ? w.emph : 'script') : null;
        if (w.style) used = true;
        continue;
      }
      if (!w.emph) w.style = null;
      else if (typeof w.emph === 'string') w.style = w.emph;
      else if (mode === 'mix') w.style = EMPH_CYCLE[n++ % EMPH_CYCLE.length];
      else if (mode === 'none') w.style = null;
      else w.style = mode === 'color' ? 'color' : 'box';
    }
  }
  return phrases;
}

/**
 * Susun satu frasa menjadi baris bertingkat: 'small' (kata sambung), 'big' (kata bermakna,
 * boleh berisi kotak/arc), 'script' (aksen huruf sambung). Posisi baris dihitung sekali
 * sehingga kata yang muncul belakangan tidak menggeser kata lain.
 */
export function kineticLines(words, { bigChars = 16, smallChars = 26, maxWidth = 0, widthOf = null } = {}) {
  // Batas baris: lebar teks terukur (px) bila tersedia, jika tidak jumlah karakter.
  const fits = (tier, text) => (widthOf && maxWidth ? widthOf(text, tier) <= maxWidth : text.length <= (tier === 'small' ? smallChars : bigChars));
  const tierOf = (w) => (w.style === 'script' ? 'script' : !w.style && CONNECTORS.has(normWord(w.text)) ? 'small' : 'big');
  const allSmall = words.every((w) => tierOf(w) === 'small');
  const lines = [];
  for (const w of words) {
    const tier = allSmall ? 'big' : tierOf(w);
    const cur = lines[lines.length - 1];
    if (cur && cur.tier === tier && fits(tier, [...cur.words, w].map((x) => x.text).join(' '))) cur.words.push(w);
    else lines.push({ tier, words: [w] });
  }
  // Rapikan: baris 'small' berisi satu kata pendek di tengah dua baris 'big' digabung ke baris berikutnya.
  for (let i = 1; i < lines.length - 1; i++) {
    const l = lines[i];
    const merged = [...l.words, ...lines[i + 1].words].map((x) => x.text).join(' ');
    if (l.tier === 'small' && l.words.length === 1 && lines[i + 1].tier === 'big' && lines[i - 1].tier === 'big' && fits('big', merged)) {
      lines[i + 1].words.unshift(...l.words);
      lines.splice(i, 1);
    }
  }
  return lines.slice(0, 4);
}

/** Bagi frasa menjadi baris kecil (lead) dan baris besar (key) untuk layout "stack". */
export function splitLeadKey(words) {
  if (words.length <= 2) return { lead: [], key: words };
  const firstEmph = words.findIndex((w) => w.emph);
  let cut = firstEmph > 0 ? firstEmph : Math.ceil(words.length / 2);
  cut = Math.min(cut, words.length - 1);
  return { lead: words.slice(0, cut), key: words.slice(cut) };
}

/* ------------------------------ Status ------------------------------ */

export function projectStatus(p, activeJobs = []) {
  const job = activeJobs.find((j) => j.projectId === p.id && j.state === 'running');
  if (job?.type === 'render') return { code: 'exporting', label: 'Sedang diekspor' };
  if (job?.type === 'analyze') return { code: 'analyzing', label: 'Sedang dianalisis' };
  if (job?.type === 'transcribe') return { code: 'transcribing', label: 'Sedang ditranskrip' };
  if (!p.source) return { code: 'empty', label: 'Belum ada video' };
  if (p.source.missing) return { code: 'missing', label: 'File sumber hilang' };
  const lastExport = (p.exports || [])[0];
  if (lastExport?.state === 'done') return { code: 'exported', label: 'Ekspor selesai' };
  if (!p.analysis) return { code: 'new', label: 'Belum dianalisis' };
  if (!p.transcript?.segments?.length) return { code: 'needs-transcript', label: 'Menunggu transkrip' };
  if (!p.transcript.reviewed) return { code: 'needs-review', label: 'Menunggu koreksi' };
  if (lastExport?.state === 'failed') return { code: 'export-failed', label: 'Ekspor gagal' };
  return { code: 'ready', label: 'Siap dipreview' };
}

/* ------------------------------ Format ------------------------------ */

export const OUTPUT_FORMATS = {
  '9:16': { width: 1080, height: 1920, label: 'Vertikal 9:16 (Reels/TikTok/Shorts)' },
  '4:5': { width: 1080, height: 1350, label: 'Portrait 4:5 (Feed IG/LinkedIn)' },
  '1:1': { width: 1080, height: 1080, label: 'Persegi 1:1' },
  '16:9': { width: 1920, height: 1080, label: 'Horizontal 16:9 (YouTube)' },
};

/** Hitung ukuran skala + offset crop agar sumber menutupi bingkai output. */
export function framing(srcW, srcH, outW, outH, { x = 0.5, y = 0.5, zoom = 1 } = {}) {
  const s = Math.max(outW / srcW, outH / srcH) * Math.max(1, zoom);
  const sw = Math.ceil((srcW * s) / 2) * 2;
  const sh = Math.ceil((srcH * s) / 2) * 2;
  const cx = Math.round((sw - outW) * Math.min(1, Math.max(0, x)));
  const cy = Math.round((sh - outH) * Math.min(1, Math.max(0, y)));
  return { scale: s, sw, sh, cx, cy };
}

export function fmtTime(t) {
  if (!Number.isFinite(t)) return '-';
  const m = Math.floor(t / 60);
  const s = (t % 60).toFixed(1).padStart(4, '0');
  return `${m}:${s}`;
}
