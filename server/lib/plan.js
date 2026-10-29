// Rencana edit. Dua sumber saran:
//  1) "aturan"  — heuristik lokal, deterministik, tanpa jaringan (selalu tersedia).
//  2) "claude"  — opsional, hanya TEKS transkrip yang dikirim, hanya dengan persetujuan.
// Semua saran masuk dengan approved=false; pengguna yang menyetujui.
// Teks kartu wajib berasal dari ucapan; yang tidak cocok ditandai needsReview.
import { uid, r3, normWord, tokenize, DEFAULT_PACING, enforcePacing } from '../../public/shared/core.js';
import { config, getSecret, hasSecret } from './config.js';
import { UserError } from './media.js';

const FILLERS = new Set(['eh', 'ehm', 'em', 'emm', 'hmm', 'mm', 'anu', 'um', 'uh', 'uhm', 'erm', 'ah']);
const ORDINALS = /^(pertama|kedua|ketiga|keempat|kelima|keenam|ketujuh|first|second|third|fourth|fifth)[,.:]?$/i;
const NUMBER_RE = /^[\p{P}]*(rp\.?\s?)?\d[\d.,]*(%|k|rb|jt|x)?[\p{P}]*$/iu;
const SCALE_WORDS = /^(ribu|juta|miliar|triliun|persen|kali|thousand|million|billion|percent)[\p{P}]*$/iu;
const TRAILING_STOP = new Set(['yang', 'dan', 'di', 'ke', 'dari', 'untuk', 'dengan', 'itu', 'atau', 'kamu', 'saya', 'aku', 'kita', 'kami', 'bisa', 'akan', 'kalau', 'jika', 'agar', 'supaya', 'karena', 'tapi', 'juga', 'lebih', 'sangat', 'sedang', 'lagi', 'ya', 'sih', 'nih', 'deh', 'tanpa', 'oleh', 'pada', 'dalam', 'the', 'and', 'to', 'of', 'a', 'you', 'i', 'we', 'can', 'is']);

// Penanda kalimat inti: frasa setelahnya biasanya poin utama ("…adalah brand yang jelas").
const MARKERS = new Set(['adalah', 'yaitu', 'yakni', 'kuncinya', 'rahasianya', 'intinya', 'masalahnya', 'faktanya', 'artinya', 'solusinya', 'caranya', 'jawabannya', 'bukan']);
const CONTRAST = new Set(['tapi', 'tetapi', 'melainkan', 'namun', 'but']);
const CHAT = new Set(['chat', 'nge-chat', 'whatsapp', 'wa', 'dm', 'inbox', 'nanya', 'tanya', 'bertanya', 'nanyain', 'komplain']);
const QUOTE_MARKERS = new Set(['intinya', 'ingat', 'artinya', 'kuncinya', 'pelajarannya']);
const CTA = new Set(['simpan', 'save', 'follow', 'ikuti', 'komen', 'komentar', 'bagikan', 'share', 'kirim', 'klik', 'cek', 'dm', 'tag', 'subscribe', 'daftar']);
const NUM_WORDS = { satu: 1, dua: 2, tiga: 3, empat: 4, lima: 5, enam: 6, tujuh: 7, delapan: 8, sembilan: 9, sepuluh: 10, sebelas: 11, seratus: 100, seribu: 1000, sejuta: 1e6 };
const NUM_SCALE = { belas: 10, puluh: 10, ratus: 100, ribu: 1000, juta: 1e6, miliar: 1e9 };

/** Angka yang diucapkan sebagai kata ("tiga", "lima puluh", "dua ribu") → { value, len }. */
function spokenNumber(words, i) {
  const a = NUM_WORDS[normWord(words[i]?.text)];
  if (!a) return null;
  const sc = NUM_SCALE[normWord(words[i + 1]?.text)];
  if (sc && a < 10) return { value: sc === 10 && normWord(words[i + 1].text) === 'belas' ? 10 + a : a * sc, len: 2 };
  return { value: a, len: 1 };
}

/** Ambil frasa pendek dari kata-kata yang diucapkan: berhenti di tanda baca, buang kata sambung di ujung. */
function cleanPhrase(words, max) {
  const out = [];
  for (const w of words) {
    out.push(w.text);
    if (out.length >= max || /[.,!?;:…]$/.test(w.text)) break;
  }
  while (out.length && TRAILING_STOP.has(normWord(out[out.length - 1]))) out.pop();
  return out.join(' ').replace(/[.,!?;:…]+$/, '');
}

export function rulePlan(project) {
  const segs = project.transcript?.segments || [];
  const dur = project.source?.meta?.duration || 0;
  const silences = project.analysis?.silences || [];
  const keywords = new Set((project.brandKeywords || []).map(normWord).filter(Boolean));
  const out = { structure: [], emphasis: [], cards: [], broll: [], sfx: [], cuts: [], zooms: [], music: null, notes: [] };
  if (!segs.length) {
    out.notes.push('Belum ada transkrip; saran yang bergantung pada isi ucapan dilewati.');
  }

  // Struktur: hook = segmen pertama (maks ~5 dtk), penutup = segmen terakhir.
  if (segs.length) {
    const hookEnd = segs.findIndex((s) => s.end - segs[0].start > 5);
    const hookSegs = segs.slice(0, Math.max(1, hookEnd === -1 ? 1 : hookEnd));
    const closeSeg = segs.length > 2 ? segs[segs.length - 1] : null;
    out.structure.push({ part: 'Hook', start: hookSegs[0].start, end: hookSegs[hookSegs.length - 1].end, text: hookSegs.map((s) => s.text).join(' '), reason: 'Kalimat pembuka; tentukan apakah cukup kuat menahan 3 detik pertama.' });
    const bodyStart = hookSegs[hookSegs.length - 1].end;
    const bodyEnd = closeSeg ? closeSeg.start : segs[segs.length - 1].end;
    if (bodyEnd - bodyStart > 0.5) out.structure.push({ part: 'Isi', start: bodyStart, end: bodyEnd, text: '', reason: 'Bagian penjelasan utama.' });
    if (closeSeg) out.structure.push({ part: 'Penutup / CTA', start: closeSeg.start, end: closeSeg.end, text: closeSeg.text, reason: 'Kalimat terakhir; cek apakah sudah ada ajakan yang jelas.' });
  }

  // Penekanan kata + kandidat kartu (angka, poin, frasa inti, CTA, kata kunci).
  const cand = [];
  for (const seg of segs) {
    const words = seg.words || [];
    let lastEmph = -10;
    words.forEach((w, i) => {
      const n = normWord(w.text);
      let reason = null;
      if (NUMBER_RE.test(w.text)) reason = 'angka';
      else if (keywords.has(n)) reason = 'kata kunci brand (dapat diubah di Profil Brand)';
      if (reason && i - lastEmph >= 3) {
        out.emphasis.push({ segId: seg.id, wordIndex: i, word: w.text, reason });
        lastEmph = i;
      }
      const before = (k) => words.slice(Math.max(0, k - 2), k).map((x) => x.text).join(' ').replace(/[.,!?;:…]+$/, '');
      if (NUMBER_RE.test(w.text)) {
        const next = words[i + 1];
        const unit = next && SCALE_WORDS.test(next.text) ? next.text.replace(/[\p{P}]+$/u, '') : '';
        const label = [unit, cleanPhrase(words.slice(i + (unit ? 2 : 1)), 2)].filter(Boolean).join(' ');
        cand.push({ prio: 3, type: 'number', start: r3(Math.max(seg.start, w.start - 0.15)), end: r3(Math.min(seg.end + 0.3, w.start + 1.8)), kicker: before(i), title: w.text.replace(/[,.]$/, ''), subtitle: label, icon: 'auto', reason: 'Angka yang diucapkan lebih mudah diingat sebagai visual besar.' });
      } else {
        const sn = spokenNumber(words, i);
        const after = sn && words[i + sn.len];
        if (sn && sn.value >= 2 && after && !TRAILING_STOP.has(normWord(after.text)) && !/[.,!?]$/.test(words[i + sn.len - 1].text)) {
          cand.push({ prio: 3, type: 'number', numberValue: sn.value, start: r3(Math.max(seg.start, w.start - 0.15)), end: r3(Math.min(seg.end + 0.3, w.start + 1.8)), kicker: before(i), title: sn.value.toLocaleString('id-ID'), subtitle: cleanPhrase(words.slice(i + sn.len), 2), icon: 'auto', reason: `Angka yang diucapkan ("${words.slice(i, i + sn.len).map((x) => x.text).join(' ')}") ditampilkan sebagai angka besar.` });
        }
      }
      if (ORDINALS.test(w.text) && i <= 1) {
        cand.push({ prio: 3, type: 'keyword', start: r3(w.start), end: r3(Math.min(seg.end, w.start + 2.2)), kicker: w.text.replace(/[,.:]$/, ''), title: cleanPhrase(words.slice(i + 1), 5), subtitle: '', icon: 'check', reason: 'Penanda poin berurutan; kartu poin membantu penonton mengikuti struktur.' });
      }
      // "bukan X, tapi Y" → kartu banding: X dicoret, Y dalam Fraunces (bible: coret yang salah).
      if (n === 'bukan' && i < words.length - 2) {
        const j = words.findIndex((x, k) => k > i + 1 && CONTRAST.has(normWord(x.text)));
        if (j > i + 1 && j - i <= 6) {
          const x = cleanPhrase(words.slice(i + 1, j), 4), y = cleanPhrase(words.slice(j + 1), 4);
          if (x && y) cand.push({ prio: 4, type: 'compare', start: r3(w.start - 0.05), end: r3(words[Math.min(words.length - 1, j + 2)].end + 0.4), kicker: '', title: x, subtitle: y, icon: '', reason: `Pola "bukan … ${words[j].text} …": yang keliru dicoret, yang benar ditonjolkan.` });
        }
      }
      // "dari X ke Y" → diagram alur dua langkah.
      if (n === 'dari' && i < words.length - 2) {
        const j = words.findIndex((x, k) => k > i + 1 && k <= i + 4 && normWord(x.text) === 'ke');
        if (j > 0) {
          const x = cleanPhrase(words.slice(i + 1, j), 3), y = cleanPhrase(words.slice(j + 1), 3);
          if (x && y && !NUMBER_RE.test(x)) cand.push({ prio: 2, type: 'flow', start: r3(w.start - 0.05), end: r3(w.start + 2.4), kicker: '', title: x, subtitle: y, icon: '', reason: 'Pola "dari … ke …" lebih mudah dipahami sebagai alur.' });
        }
      }
      // Percakapan pelanggan → mockup chat melayang di atas footage (teks = ucapan, berlabel ilustrasi).
      if (CHAT.has(n) && i < words.length - 2) {
        const said = cleanPhrase(words.slice(i + 1), 7);
        if (tokenize(said).length >= 2) cand.push({ prio: 2.5, type: 'chat', layout: 'overlay', start: r3(w.start), end: r3(w.start + 3), kicker: '', title: said, subtitle: '', icon: '', reason: 'Menyebut chat/pertanyaan pelanggan: mockup chat (ilustrasi, teks dari ucapan) di atas footage.' });
      }
      if (QUOTE_MARKERS.has(n) && i <= 1 && tokenize(seg.text).length <= 14) {
        cand.push({ prio: 2, type: 'quote', start: r3(seg.start), end: r3(Math.min(seg.end + 0.4, seg.start + 3.5)), kicker: '', title: seg.text.replace(/[.,!?;:…]+$/, ''), subtitle: '', icon: 'quote', reason: `Kalimat inti ("${w.text} …") sebagai kutipan Fraunces.` });
        return;
      }
      if (MARKERS.has(n) && n !== 'bukan' && i < words.length - 1) {
        const title = cleanPhrase(words.slice(i + 1), 4);
        if (tokenize(title).length >= 1) cand.push({ prio: 2, type: 'keyword', start: r3(words[i + 1].start - 0.05), end: r3(Math.min(seg.end + 0.3, words[i + 1].start + 2)), kicker: words.slice(Math.max(0, i - 2), i + 1).map((x) => x.text).join(' ').replace(/[.,!?;:…]+$/, ''), title, subtitle: '', icon: 'auto', reason: `Frasa setelah "${w.text}" biasanya poin utama kalimat.` });
      }
      if (CTA.has(n)) {
        cand.push({ prio: 3, type: 'keyword', cta: true, start: r3(w.start - 0.05), end: r3(Math.min(seg.end + 0.5, w.start + 2.2)), kicker: '', title: cleanPhrase(words.slice(i), 4), subtitle: '', icon: 'auto', reason: 'Ajakan (CTA) lebih kuat bila terlihat di layar.' });
      }
      if (reason === 'kata kunci brand (dapat diubah di Profil Brand)') {
        cand.push({ prio: 1, type: 'keyword', start: r3(w.start - 0.05), end: r3(Math.min(seg.end + 0.3, w.start + 1.8)), kicker: before(i), title: cleanPhrase(words.slice(i), 2), subtitle: '', icon: 'auto', reason: `Kata kunci "${w.text}" sebagai kartu tipografi (pola di video referensi).` });
      }
    });
  }

  // Tiga poin berurutan atau lebih → satu kartu checklist rangkuman (menggantikan kartu poin satuan).
  const ords = cand.filter((c) => c.icon === 'check' && ORDINALS.test(c.kicker || ''));
  if (ords.length >= 3) {
    const last = ords[ords.length - 1];
    const lastSeg = segs.find((sg) => sg.start <= last.start && sg.end >= last.start);
    for (const o of ords) cand.splice(cand.indexOf(o), 1);
    const at = r3((lastSeg?.end ?? last.end) + 0.05);
    cand.push({ prio: 4, type: 'list', start: at, end: r3(at + 3.2), kicker: '', title: '', subtitle: ords.map((o) => cleanPhrase(tokenize(o.title).map((t) => ({ text: t })), 3)).join('; '), icon: '', reason: 'Poin berurutan dirangkum sebagai checklist (layak disimpan).', verifyFrom: ords[0].start });
  }

  // Pilih kartu: prioritas tinggi dulu, dengan jeda wajah minimal di antara kartu dan
  // maks ±1 kartu per 8 dtk agar wajah tetap dominan (keluhan "adegan wajah terlalu cepat").
  const P = { ...DEFAULT_PACING, ...(project.style?.pacing || {}) };
  const maxCards = Math.max(2, Math.round(dur / 7));
  for (const c of cand.sort((a, b) => b.prio - a.prio || a.start - b.start)) {
    if (out.cards.length >= maxCards) break;
    // Durasi kartu mengikuti waktu baca (±0,35 dtk/kata + 1,2 dtk), dalam batas min–maks.
    const words = tokenize([c.kicker, c.title, c.subtitle].join(' ')).length;
    c.start = r3(Math.max(c.start, P.firstCardAt));
    const extra = c.type === 'chat' || c.type === 'list' || c.type === 'compare' ? 0.8 : 0;
    c.end = r3(Math.min(dur, c.start + Math.min(P.maxCard, Math.max(P.minCard, 1.2 + extra + words * 0.35))));
    if ((!c.title && c.type !== 'list') || out.cards.some((x) => c.start < x.end + P.minFaceGap && c.end > x.start - P.minFaceGap)) continue;
    if (c.title && out.cards.some((x) => normWord(x.title) === normWord(c.title))) continue; // hindari kartu kembar
    const { prio, ...card } = c;
    out.cards.push(card);
  }
  out.cards.sort((a, b) => a.start - b.start);

  // Potongan: jeda panjang, kata pengisi, dan pengulangan/awal yang diulang.
  for (const s of silences) {
    const pad = 0.15;
    const st = s.start + pad;
    const en = s.end - pad;
    const atEdge = s.start < 0.05 || s.end > dur - 0.05;
    if (en - st >= 0.5 || (atEdge && en - st > 0.2)) {
      out.cuts.push({ start: r3(st), end: r3(en), kind: atEdge ? 'tepi' : 'jeda', reason: atEdge ? 'Hening di awal/akhir video.' : `Jeda ${(s.end - s.start).toFixed(1)} dtk.` });
    }
  }
  for (const seg of segs) {
    if (seg.timing !== 'asr') continue; // Hanya jika timestamp kata asli tersedia.
    (seg.words || []).forEach((w) => {
      if (FILLERS.has(normWord(w.text))) out.cuts.push({ start: r3(w.start), end: r3(w.end), kind: 'pengisi', reason: `Kata pengisi "${w.text}".` });
    });
  }
  for (let i = 0; i < segs.length - 1; i++) {
    const a = tokenize(segs[i].text).slice(0, 3).map(normWord).join(' ');
    const b = tokenize(segs[i + 1].text).slice(0, 3).map(normWord).join(' ');
    if (a && a === b && tokenize(segs[i].text).length >= 3) {
      out.cuts.push({ start: segs[i].start, end: segs[i + 1].start, kind: 'pengulangan', reason: 'Dua kalimat berurutan diawali kata yang sama — kemungkinan take ulang. Dengarkan sebelum menyetujui.' });
    }
  }

  // B-roll: bagian isi yang panjang tanpa kartu → saran jeda visual (tanpa aset).
  const covered = (a, b) => out.cards.some((c) => c.start < b && c.end > a);
  for (const seg of segs) {
    if (seg.end - seg.start >= 6 && !covered(seg.start, seg.end)) {
      const mid = seg.start + (seg.end - seg.start) / 2;
      out.broll.push({ start: r3(mid - 1.2), end: r3(mid + 1.2), idea: `Visual pendukung untuk: "${tokenize(seg.text).slice(0, 8).join(' ')}…"`, reason: 'Talking head lebih dari 6 detik tanpa jeda visual.' });
    }
  }

  // Foto milik pengguna (aset gambar) dipasang ke kartu pernyataan sebagai tile (bible: foto nyata dulu).
  const photos = (project.assets || []).filter((a) => a.kind === 'image' && !a.missing);
  let pi = 0;
  if (photos.length) for (const c of out.cards) if (c.type === 'keyword' && !c.cta) c.image = photos[pi++ % photos.length].id;

  out.hook = hookSuggestion(segs, keywords, project.style?.hook?.maxSec ?? 1.6);
  // Kartu tidak boleh menumpuk hook di awal.
  if (out.hook) out.cards = out.cards.filter((c) => c.start >= out.hook.end + 0.3);

  // SFX dari pustaka sintetis bawaan, disesuaikan jenis visualnya.
  out.sfx.push(...sfxForVisuals(out.cards, out.broll, project.style?.audio?.sfxPalette));

  // Zoom punch-in bergantian antar kalimat (ritme visual seperti referensi, tanpa footage tambahan).
  const level = project.style?.zoom?.punchIn ?? 1.12;
  segs.forEach((seg, i) => {
    if (i % 2 === 1 && seg.end - seg.start >= Math.max(2.5, P.minZoom)) {
      out.zooms.push({ start: seg.start, end: seg.end, zoom: level, approved: true, reason: 'Punch-in bergantian antar kalimat menjaga ritme visual (pola di video referensi).' });
    }
  });
  out.zooms = enforcePacing({ zooms: out.zooms, pacing: P }).zooms.filter((z) => z.approved).map(({ approved, ...z }) => z);

  out.music = musicSuggestion(project);
  return out;
}

const MOOD_BY_LEVEL = { minimal: 'tenang', editorial: 'tenang', dinamis: 'energik' };

function musicSuggestion(project) {
  const mood = MOOD_BY_LEVEL[project.styleLevel] || 'tenang';
  return {
    builtin: mood,
    reason: `Saran: musik bawaan "${mood}" (disintesis aplikasi, bebas royalti) — atau impor musik berlisensi Anda sendiri.`,
    volumeDb: project.style?.audio?.musicDb ?? -24,
  };
}

/** Hook lockup dari kata-kata pembuka (semuanya diucapkan): lead kecil → 1–2 kata besar → frasa rasa. */
export function hookSuggestion(segs, keywords = new Set(), maxSec = 1.6) {
  const first = segs[0];
  const words = (first?.words || []).filter((w) => w.start - first.start <= Math.max(2.5, maxSec + 0.8));
  if (words.length < 2) return null;
  const score = (w, i) => {
    const n = normWord(w.text);
    if (!n || TRAILING_STOP.has(n) || FILLERS.has(n)) return -1;
    return (NUMBER_RE.test(w.text) ? 6 : 0) + (keywords.has(n) ? 4 : 0) + Math.min(4, n.length / 2) - i * 0.15;
  };
  let bi = 0;
  words.forEach((w, i) => { if (score(w, i) > score(words[bi], bi)) bi = i; });
  if (score(words[bi], bi) < 0) return null;
  const clean = (t) => t.replace(/[.,!?;:…]+$/, '');
  let big = clean(words[bi].text);
  let bEnd = bi;
  const nx = words[bi + 1];
  if (nx && !/[.,!?;:…]$/.test(words[bi].text) && (big + ' ' + clean(nx.text)).length <= 12 && !TRAILING_STOP.has(normWord(nx.text))) {
    big += ' ' + clean(nx.text);
    bEnd = bi + 1;
  }
  const lead = words.slice(Math.max(0, bi - 4), bi).map((w) => w.text).join(' ').replace(/[.,!?;:…]+$/, '').toLowerCase();
  const accWords = /[.,!?;:…]$/.test(words[bEnd].text) ? [] : words.slice(bEnd + 1, bEnd + 3);
  const accent = clean(accWords.map((w) => w.text).join(' '));
  const lastW = accWords.length ? accWords[accWords.length - 1] : words[bEnd];
  const start = r3(Math.max(0, first.start));
  const end = r3(Math.max(start + 1.0, Math.min(start + maxSec + 0.6, lastW.end + 0.25)));
  return { start, end, lead, big: big.charAt(0).toUpperCase() + big.slice(1), accent: accent.length <= 18 ? accent : '', reason: 'Hook 0–1,6 dtk: kata pembuka paling bermakna sebagai kata besar (diambil dari ucapan).' };
}

function sfxForVisuals(cards, broll, palette = 'reference') {
  const out = [];
  // Bible: tanpa whoosh/zoom/audio meme — hanya bunyi halus.
  if (palette === 'quiet') {
    for (const c of cards) if (c.type !== 'chat') out.push({ time: c.start, builtin: c.type === 'number' ? 'pop' : 'click', reason: 'Penanda halus munculnya kartu (palet tenang sesuai bible).' });
    return out;
  }
  for (const c of cards) {
    const [builtin, reason] = c.type === 'number' ? ['impact', 'Menegaskan angka besar.']
      : c.cta ? ['notif', 'Menarik perhatian ke ajakan (CTA).']
      : c.icon === 'check' ? ['pop', 'Menandai poin berurutan.']
      : c.type === 'list' ? ['click', 'Menandai daftar poin.']
      : ['swoosh', 'Menandai munculnya kartu.'];
    out.push({ time: c.start, builtin, reason });
  }
  for (const b of broll) out.push({ time: b.start, builtin: 'whoosh', reason: 'Transisi ke footage sisipan.' });
  return out;
}

/* ------------------------------ Claude (opsional) ------------------------------ */

const PLAN_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['structure', 'emphasis', 'cards', 'broll', 'cuts', 'notes'],
  properties: {
    structure: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['part', 'start', 'end', 'reason'], properties: { part: { type: 'string' }, start: { type: 'number' }, end: { type: 'number' }, reason: { type: 'string' } } } },
    emphasis: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['segId', 'word', 'reason'], properties: { segId: { type: 'string' }, word: { type: 'string' }, reason: { type: 'string' } } } },
    cards: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['type', 'start', 'end', 'kicker', 'title', 'subtitle', 'icon', 'reason'], properties: { type: { type: 'string', enum: ['keyword', 'number', 'list', 'compare', 'quote', 'flow'] }, start: { type: 'number' }, end: { type: 'number' }, kicker: { type: 'string' }, title: { type: 'string' }, subtitle: { type: 'string' }, icon: { type: 'string', enum: ['', 'check', 'cross', 'arrow', 'warning', 'star'] }, reason: { type: 'string' } } } },
    broll: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['start', 'end', 'idea', 'reason'], properties: { start: { type: 'number' }, end: { type: 'number' }, idea: { type: 'string' }, reason: { type: 'string' } } } },
    cuts: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['start', 'end', 'reason'], properties: { start: { type: 'number' }, end: { type: 'number' }, reason: { type: 'string' } } } },
    notes: { type: 'array', items: { type: 'string' } },
  },
};

const SYSTEM = `Anda editor video edukatif untuk konten personal branding vertikal (9:16).
Anda menerima transkrip bertimestamp. Usulkan rencana edit dalam JSON sesuai skema.
Aturan wajib:
- Jangan menambahkan klaim, statistik, kutipan, atau fakta yang tidak diucapkan.
- Teks kartu (kicker/title/subtitle) harus diambil dari kata-kata yang benar-benar diucapkan pada rentang waktu kartu itu. Boleh dipersingkat, tidak boleh diubah maknanya.
- Penekanan: maksimal satu kata per kalimat pendek; pilih kata yang membawa makna utama.
- B-roll hanya berupa ide visual (tanpa mengaku memiliki aset).
- Cut hanya untuk jeda kosong, pengulangan, atau salah ucap yang jelas.
- Semua waktu dalam detik pada timeline sumber.
- Tulis alasan singkat dalam Bahasa Indonesia.`;

export async function claudePlan(project) {
  if (!hasSecret('ANTHROPIC_API_KEY')) {
    throw new UserError('ANTHROPIC_API_KEY belum dikonfigurasi.', 'Isi ANTHROPIC_API_KEY di file .env lalu jalankan ulang aplikasi. Rencana berbasis aturan tetap bisa dipakai tanpa key.', 412);
  }
  let Anthropic;
  try {
    ({ default: Anthropic } = await import('@anthropic-ai/sdk'));
  } catch {
    throw new UserError('Paket @anthropic-ai/sdk belum terpasang.', 'Jalankan "npm install" di folder aplikasi.', 412);
  }
  const segs = project.transcript?.segments || [];
  if (!segs.length) throw new UserError('Belum ada transkrip untuk direncanakan.', 'Buat atau impor transkrip terlebih dahulu.');
  const transcript = segs.map((s) => `[${s.id}] ${s.start.toFixed(2)}–${s.end.toFixed(2)}: ${s.text}`).join('\n');
  const client = new Anthropic({ apiKey: getSecret('ANTHROPIC_API_KEY') });
  let res;
  try {
    res = await client.beta.messages.create({
      model: config.anthropicModel,
      max_tokens: 16000,
      betas: ['server-side-fallback-2026-07-01'],
      fallbacks: 'default',
      system: SYSTEM,
      output_config: { effort: 'medium', format: { type: 'json_schema', schema: PLAN_SCHEMA } },
      messages: [{ role: 'user', content: `Durasi video: ${(project.source?.meta?.duration || 0).toFixed(1)} detik.\n\nTranskrip:\n${transcript}` }],
    });
  } catch (err) {
    if (err instanceof Anthropic.AuthenticationError) throw new UserError('API key Anthropic ditolak.', 'Periksa ANTHROPIC_API_KEY di file .env.', 401);
    if (err instanceof Anthropic.RateLimitError) throw new UserError('Batas penggunaan API tercapai.', 'Tunggu sebentar lalu coba lagi.', 429);
    if (err instanceof Anthropic.APIError) throw new UserError(`Permintaan ke Claude gagal (status ${err.status ?? '-'}).`, 'Coba lagi, atau gunakan rencana berbasis aturan.', 502);
    throw new UserError('Tidak dapat terhubung ke API Claude.', 'Periksa koneksi internet.', 502);
  }
  if (res.stop_reason === 'refusal') throw new UserError('Claude menolak membuat rencana untuk transkrip ini.', 'Gunakan rencana berbasis aturan.', 422);
  if (res.stop_reason === 'max_tokens') throw new UserError('Respons Claude terpotong.', 'Coba lagi dengan transkrip yang lebih pendek.', 502);
  const text = res.content.filter((b) => b.type === 'text').map((b) => b.text).join('');
  let plan;
  try {
    plan = JSON.parse(text);
  } catch {
    throw new UserError('Respons Claude bukan JSON yang valid.', 'Coba lagi.', 502);
  }
  // Ubah penekanan berbasis kata → indeks kata.
  plan.emphasis = (plan.emphasis || []).flatMap((e) => {
    const seg = segs.find((s) => s.id === e.segId);
    const idx = seg ? (seg.words || []).findIndex((w) => normWord(w.text) === normWord(e.word)) : -1;
    return idx >= 0 ? [{ segId: seg.id, wordIndex: idx, word: seg.words[idx].text, reason: e.reason }] : [];
  });
  plan.sfx = sfxForVisuals(plan.cards || [], plan.broll || [], project.style?.audio?.sfxPalette);
  plan.hook = hookSuggestion(segs, new Set((project.brandKeywords || []).map(normWord)), project.style?.hook?.maxSec ?? 1.6);
  plan.zooms = [];
  plan.music = musicSuggestion(project);
  return plan;
}

/** Tandai kartu yang berisi kata di luar ucapan pada rentang waktunya. */
export function verifyCardText(card, segments) {
  const spoken = new Set(
    segments
      .filter((s) => s.end >= (card.verifyFrom ?? card.start) - 1.5 && s.start <= card.end + 1.5)
      .flatMap((s) => tokenize(s.text).map(normWord)),
  );
  const numeric = card.numberValue ? normWord(card.title) : null;
  const used = [card.kicker, card.title, card.subtitle].flatMap((t) => tokenize(String(t || '').replace(/[;|]/g, ' ')).map(normWord)).filter(Boolean);
  // Angka hasil konversi dari kata ("tiga" → "3") dihitung sebagai diucapkan.
  const unknown = used.filter((w) => !spoken.has(w) && w !== numeric);
  return unknown;
}

/** Ubah hasil rencana menjadi item proyek (semua belum disetujui). */
export function planToItems(plan, origin, segments, { autoApprove = false } = {}) {
  const tag = (o) => ({ id: uid(o), origin, approved: false });
  // Otomatis: kartu yang SELURUH teksnya ditemukan di ucapan langsung disetujui (bukan klaim baru);
  // yang berisi kata di luar ucapan tetap menunggu persetujuan. Cut tidak pernah otomatis.
  const auto = (ok) => (autoApprove && ok ? { approved: true, autoApproved: true } : {});
  const hook = plan.hook ? { ...plan.hook, unknownWords: verifyCardText({ ...plan.hook, kicker: plan.hook.lead, title: plan.hook.big, subtitle: plan.hook.accent }, segments) } : null;
  return {
    structure: plan.structure || [],
    emphasis: (plan.emphasis || []).map((e) => ({ ...tag('em'), ...e, ...auto(true) })),
    cards: (plan.cards || []).map((c) => {
      const unknown = verifyCardText(c, segments);
      return { ...tag('card'), ...c, unknownWords: unknown, needsReview: unknown.length > 0, ...auto(unknown.length === 0) };
    }),
    hook: hook ? { ...hook, origin, approved: false, needsReview: hook.unknownWords.length > 0, ...auto(hook.unknownWords.length === 0) } : null,
    broll: (plan.broll || []).map((b) => ({ ...tag('broll'), ...b, assetId: null })),
    sfx: (plan.sfx || []).map((s) => ({ ...tag('sfx'), ...s, volumeDb: 0, ...auto(true) })),
    cuts: (plan.cuts || []).map((c) => ({ ...tag('cut'), ...c, enabled: false })),
    zooms: (plan.zooms || []).map((z) => ({ ...tag('zoom'), ...z, ...auto(true) })),
    music: plan.music || null,
    notes: plan.notes || [],
  };
}
