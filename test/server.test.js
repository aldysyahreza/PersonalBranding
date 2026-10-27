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
    makeSegment({ start: 6.1, end: 9, text: 'Dalam 90 hari hasilnya terlihat.' }),
  ];
  return {
    style,
    source: { meta: { duration: 10 } },
    analysis: { silences: [{ start: 9.2, end: 10 }] },
    transcript: { segments: segs },
    cards: [],
    brandKeywords: ['positioning'],
  };
}

test('preset level menimpa nilai dasar tanpa mengubah preset asli', () => {
  const base = getPreset('aldy-editorial');
  const dyn = resolveStyle(base, 'dinamis');
  assert.equal(dyn.captions.layout, 'karaoke');
  assert.equal(resolveStyle(base, 'editorial').captions.layout, 'stack');
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
