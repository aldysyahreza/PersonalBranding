// Rencana edit. Dua sumber saran:
//  1) "aturan"  — heuristik lokal, deterministik, tanpa jaringan (selalu tersedia).
//  2) "claude"  — opsional, hanya TEKS transkrip yang dikirim, hanya dengan persetujuan.
// Semua saran masuk dengan approved=false; pengguna yang menyetujui.
// Teks kartu wajib berasal dari ucapan; yang tidak cocok ditandai needsReview.
import { uid, r3, normWord, tokenize } from '../../public/shared/core.js';
import { config, getSecret, hasSecret } from './config.js';
import { UserError } from './media.js';

const FILLERS = new Set(['eh', 'ehm', 'em', 'emm', 'hmm', 'mm', 'anu', 'um', 'uh', 'uhm', 'erm', 'ah']);
const ORDINALS = /^(pertama|kedua|ketiga|keempat|kelima|keenam|ketujuh|first|second|third|fourth|fifth|satu|dua|tiga|empat|lima)[,.:]?$/i;
const NUMBER_RE = /^[\p{P}]*(rp\.?\s?)?\d[\d.,]*(%|k|rb|jt|x)?[\p{P}]*$/iu;
const SCALE_WORDS = /^(ribu|juta|miliar|triliun|persen|kali|thousand|million|billion|percent)[\p{P}]*$/iu;
const TRAILING_STOP = new Set(['yang', 'dan', 'di', 'ke', 'dari', 'untuk', 'dengan', 'itu', 'ini', 'atau', 'kamu', 'saya', 'aku', 'kita', 'kami', 'bisa', 'akan', 'the', 'and', 'to', 'of', 'a', 'you', 'i', 'we', 'can', 'is']);

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
  const out = { structure: [], emphasis: [], cards: [], broll: [], sfx: [], cuts: [], music: null, notes: [] };
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

  // Penekanan kata + kartu angka + kartu poin.
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
      if (NUMBER_RE.test(w.text)) {
        const next = words[i + 1];
        const unit = next && SCALE_WORDS.test(next.text) ? next.text.replace(/[\p{P}]+$/u, '') : '';
        const label = [unit, cleanPhrase(words.slice(i + (unit ? 2 : 1)), 2)].filter(Boolean).join(' ');
        const before = words.slice(Math.max(0, i - 2), i).map((x) => x.text).join(' ').replace(/[.,!?;:…]+$/, '');
        out.cards.push({
          type: 'number',
          start: r3(Math.max(seg.start, w.start - 0.15)),
          end: r3(Math.min(seg.end + 0.3, w.start + 1.8)),
          kicker: before,
          title: w.text.replace(/[,.]$/, ''),
          subtitle: label,
          icon: '',
          reason: 'Angka yang diucapkan lebih mudah diingat sebagai visual besar.',
        });
      }
      if (ORDINALS.test(w.text) && i <= 1) {
        const phrase = cleanPhrase(words.slice(i + 1), 5);
        out.cards.push({
          type: 'keyword',
          start: r3(w.start),
          end: r3(Math.min(seg.end, w.start + 2.2)),
          kicker: w.text.replace(/[,.:]$/, ''),
          title: phrase,
          subtitle: '',
          icon: 'check',
          reason: 'Penanda poin berurutan; kartu poin membantu penonton mengikuti struktur.',
        });
      }
    });
  }

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

  // SFX: pop sintetis di awal setiap kartu.
  for (const c of out.cards) out.sfx.push({ time: c.start, builtin: 'pop', reason: 'Menandai munculnya kartu.' });

  out.music = { reason: 'Musik instrumental pelan sebagai dasar ritme. Belum ada aset — impor file musik berlisensi milik Anda.', volumeDb: project.style?.audio?.musicDb ?? -24 };
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
    cards: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['type', 'start', 'end', 'kicker', 'title', 'subtitle', 'icon', 'reason'], properties: { type: { type: 'string', enum: ['keyword', 'number', 'list'] }, start: { type: 'number' }, end: { type: 'number' }, kicker: { type: 'string' }, title: { type: 'string' }, subtitle: { type: 'string' }, icon: { type: 'string', enum: ['', 'check', 'cross', 'arrow', 'warning', 'star'] }, reason: { type: 'string' } } } },
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
  plan.sfx = (plan.cards || []).map((c) => ({ time: c.start, builtin: 'pop', reason: 'Menandai munculnya kartu.' }));
  plan.music = { reason: 'Musik instrumental pelan. Belum ada aset — impor file musik berlisensi milik Anda.', volumeDb: project.style?.audio?.musicDb ?? -24 };
  return plan;
}

/** Tandai kartu yang berisi kata di luar ucapan pada rentang waktunya. */
export function verifyCardText(card, segments) {
  const spoken = new Set(
    segments
      .filter((s) => s.end >= card.start - 1.5 && s.start <= card.end + 1.5)
      .flatMap((s) => tokenize(s.text).map(normWord)),
  );
  const used = [card.kicker, card.title, card.subtitle].flatMap((t) => tokenize(String(t || '').replace(/[;|]/g, ' ')).map(normWord)).filter(Boolean);
  const unknown = used.filter((w) => !spoken.has(w));
  return unknown;
}

/** Ubah hasil rencana menjadi item proyek (semua belum disetujui). */
export function planToItems(plan, origin, segments) {
  const tag = (o) => ({ id: uid(o), origin, approved: false });
  return {
    structure: plan.structure || [],
    emphasis: (plan.emphasis || []).map((e) => ({ ...tag('em'), ...e })),
    cards: (plan.cards || []).map((c) => {
      const unknown = verifyCardText(c, segments);
      return { ...tag('card'), ...c, unknownWords: unknown, needsReview: unknown.length > 0 };
    }),
    broll: (plan.broll || []).map((b) => ({ ...tag('broll'), ...b, assetId: null })),
    sfx: (plan.sfx || []).map((s) => ({ ...tag('sfx'), ...s, volumeDb: 0 })),
    cuts: (plan.cuts || []).map((c) => ({ ...tag('cut'), ...c, enabled: false })),
    music: plan.music || null,
    notes: plan.notes || [],
  };
}
