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
  for (const seg of segments) {
    if (seg.hidden) continue;
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
  // Rapatkan celah kecil antar frasa agar subtitle tidak berkedip.
  for (let i = 0; i < phrases.length - 1; i++) {
    const gap = phrases[i + 1].start - phrases[i].end;
    if (gap > 0 && gap < 0.25) phrases[i].end = phrases[i + 1].start;
  }
  return phrases;
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
