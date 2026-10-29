import { test } from 'node:test';
import assert from 'node:assert/strict';
import { buildAss, esc, assColor, wrap } from '../server/lib/ass.js';
import { rulePlan, planToItems } from '../server/lib/plan.js';
import { getPreset, resolveStyle, deepMerge } from '../server/lib/presets.js';
import { keepSegments, makeSegment } from '../public/shared/core.js';

function project() {
  const style = resolveStyle(getPreset('aldy-editorial'), 'editorial');
  const segs = [
    makeSegment({ start: 0, end: 3, text: 'Banyak bisnis sibuk posting tanpa positioning.' }),
    makeSegment({ start: 3.2, end: 6, text: 'Pertama, pilih satu masalah utama.' }),
    makeSegment({ start: 11, end: 14, text: 'Dalam 90 hari hasilnya terlihat.' }),
  ];
  return {
    style,
    source: { meta: { duration: 20 } },
    analysis: { silences: [{ start: 19.2, end: 20 }] },
    transcript: { segments: segs },
    cards: [],
    brandKeywords: ['positioning'],
  };
}

test('preset level menimpa nilai dasar tanpa mengubah preset asli', () => {
  const base = getPreset('aldy-editorial');
  const dyn = resolveStyle(base, 'dinamis');
  assert.equal(dyn.captions.layout, 'kinetic');
  assert.equal(dyn.captions.keySize, 96);
  assert.equal(resolveStyle(base, 'editorial').captions.layout, 'kinetic');
  assert.equal(resolveStyle(base, 'minimal').captions.layout, 'single');
  assert.deepEqual(deepMerge({ a: { b: 1, c: 2 } }, { a: { b: 3 } }), { a: { b: 3, c: 2 } });
});

test('ASS: warna, escape, dan wrap', () => {
  assert.equal(assColor('#D92A2A'), '&H002A2AD9');
  assert.equal(esc('a{b}\\c'), 'a(b)/c');
  assert.deepEqual(wrap('tentukan positioning yang jelas', 20), ['tentukan positioning', 'yang jelas']);
});

test('ASS berisi caption dari transkrip dan melewati bagian yang dipotong', () => {
  const p = project();
  const keep = keepSegments(10, [{ start: 0, end: 3, enabled: true }]);
  const ass = buildAss(p, { width: 1080, height: 1920, keep });
  assert.match(ass, /PlayResX: 1080/);
  assert.doesNotMatch(ass, /Banyak/); // segmen pertama terpotong seluruhnya
  assert.match(ass, /pilih/);
});

test('rencana aturan: kartu angka dari ucapan, penanda poin, cut jeda di tepi, semua belum disetujui', () => {
  const p = project();
  const plan = rulePlan(p);
  const items = planToItems(plan, 'aturan', p.transcript.segments);
  const num = items.cards.find((c) => c.type === 'number');
  assert.equal(num.title, '90');
  assert.equal(num.needsReview, false);
  assert.ok(items.cards.some((c) => c.kicker === 'Pertama'));
  assert.ok(items.cuts.some((c) => c.kind === 'tepi'));
  assert.ok(items.emphasis.some((e) => e.word.startsWith('positioning')));
  for (const list of [items.cards, items.cuts, items.emphasis, items.sfx, items.broll]) for (const x of list) assert.equal(x.approved, false);
  for (const c of items.cuts) assert.equal(c.enabled, false);
});

test('kartu dengan kata di luar ucapan ditandai perlu ditinjau', () => {
  const p = project();
  const items = planToItems({ cards: [{ type: 'keyword', start: 3.2, end: 5, kicker: '', title: 'Naik 300% omzet', subtitle: '' }] }, 'claude', p.transcript.segments);
  assert.equal(items.cards[0].needsReview, true);
  assert.ok(items.cards[0].unknownWords.includes('omzet'));
});

test('pustaka audio sintetis menghasilkan WAV valid', async () => {
  const fs = await import('node:fs');
  const { catalog, libraryFile } = await import('../server/lib/synth.js');
  const c = catalog();
  assert.equal(c.music.length, 3);
  assert.ok(c.sfx.length >= 8);
  const buf = fs.readFileSync(libraryFile('sfx', 'pop'));
  assert.equal(buf.toString('ascii', 0, 4), 'RIFF');
  assert.equal(buf.toString('ascii', 8, 12), 'WAVE');
});

test('kartu dari ucapan: angka terucap, frasa inti, CTA — tanpa kata di luar ucapan', () => {
  const style = resolveStyle(getPreset('aldy-editorial'), 'editorial');
  const segs = [
    makeSegment({ start: 0, end: 6, text: 'Brand yang mudah direkomendasikan adalah brand yang jelas posisinya.' }),
    makeSegment({ start: 10, end: 16, text: 'Ada tiga hal yang membuat orang mau merekomendasikan.' }),
    makeSegment({ start: 22, end: 28, text: 'Kalau berguna, simpan video ini sekarang.' }),
  ];
  const p = { style, styleLevel: 'editorial', source: { meta: { duration: 28 } }, analysis: { silences: [] }, transcript: { segments: segs }, brandKeywords: [] };
  const items = planToItems(rulePlan(p), 'aturan', segs);
  const titles = items.cards.map((c) => [c.title, c.subtitle].filter(Boolean).join(' '));
  assert.ok(titles.includes('brand yang jelas posisinya'));
  const num = items.cards.find((c) => c.type === 'number');
  assert.equal(num.title, '3');
  assert.equal(num.needsReview, false); // "tiga" diucapkan → "3" tidak dianggap kata baru
  assert.ok(items.cards.some((c) => c.cta && c.title.startsWith('simpan')));
  assert.ok(items.sfx.some((s) => s.builtin === 'impact') && items.sfx.some((s) => s.builtin === 'notif'));
});

test('caption kinetik: kata muncul pada timestamp-nya & ornamen lengkung untuk aksen arc', () => {
  const p = project();
  p.transcript.segments[1].words[1].emph = 'arc';
  const keep = keepSegments(20, []);
  const ass = buildAss(p, { width: 1080, height: 1920, keep });
  // Tiap kata punya animasi muncul (transparan → penuh) dengan waktu relatif sendiri.
  assert.match(ass, /\\alpha&HFF&\\blur\d+\\t\(\d+,\d+,\\alpha&H00&\\blur0\)\}pilih/);
  assert.match(ass, /\\clip\(\d+,\d+,\d+,\d+\)\\t\(\d+,\d+,\\clip/); // lengkung tergambar (clip beranimasi)
  assert.match(ass, /Style: Accent,Great Vibes/);
});

test('ritme: kartu rapat dinonaktifkan, kartu singkat diperpanjang, zoom singkat dibuang', async () => {
  const { enforcePacing } = await import('../public/shared/core.js');
  const r = enforcePacing({
    cards: [
      { id: 'a', approved: true, start: 2, end: 3, title: 'satu' },
      { id: 'b', approved: true, start: 4, end: 6, title: 'dua' },
      { id: 'c', approved: true, start: 9, end: 15, title: 'tiga' },
    ],
    zooms: [{ id: 'z', approved: true, start: 20, end: 21, zoom: 1.1 }],
    duration: 30,
  });
  const [a, b, c] = r.cards;
  assert.equal(a.end - a.start, 2); // diperpanjang ke minimal 2 dtk
  assert.equal(b.approved, false); // hanya 0 dtk wajah setelah kartu a
  assert.equal(c.end - c.start, 3.5); // dipendekkan ke maksimal
  assert.equal(r.zooms[0].approved, false);
  assert.ok(r.changes.length >= 4);
});

test('subtitle: frasa kembar ASR & frasa bertumpuk tidak tampil dua kali', async () => {
  const { buildPhrases } = await import('../public/shared/core.js');
  const segs = [
    makeSegment({ start: 0, end: 2, text: 'Halo semua apa kabar' }),
    makeSegment({ start: 1.8, end: 3.6, text: 'Halo semua apa kabar' }),
    makeSegment({ start: 3.0, end: 5, text: 'ini lanjutan' }),
  ];
  const ph = buildPhrases(segs, { maxWords: 5, maxChars: 40 });
  assert.equal(ph.length, 2);
  for (let i = 1; i < ph.length; i++) assert.ok(ph[i].start >= ph[i - 1].end);
});

test('subtitle disembunyikan selama kartu tampil', () => {
  const p = project();
  p.cards = [{ id: 'k', approved: true, type: 'keyword', start: 3.2, end: 6, title: 'pilih satu masalah', kicker: '', subtitle: '' }];
  const ass = buildAss(p, { width: 1080, height: 1920, keep: keepSegments(20, []) });
  const capLines = ass.split('\n').filter((l) => /^Dialogue: 3,/.test(l));
  for (const l of capLines) {
    const [, st, en] = l.match(/^Dialogue: 3,([^,]+),([^,]+)/);
    const sec = (x) => x.split(':').reduce((a, v) => a * 60 + Number(v), 0);
    assert.ok(sec(en) <= 3.2 + 0.01 || sec(st) >= 6 - 0.01, `caption bertumpuk dengan kartu: ${l.slice(0, 60)}`);
  }
});
