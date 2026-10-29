import { test } from 'node:test';
import assert from 'node:assert/strict';
import { buildAss } from '../server/lib/ass.js';
import { rulePlan, planToItems, hookSuggestion } from '../server/lib/plan.js';
import { getPreset, resolveStyle, listPresets } from '../server/lib/presets.js';
import { brandFixerHtml } from '../server/lib/hf-brandfixer.js';
import { keepSegments, makeSegment, buildPhrases, resolveEmphasis } from '../public/shared/core.js';

function project(texts) {
  const style = resolveStyle(getPreset('brand-fixer'), 'editorial');
  let t = 0;
  const segs = texts.map((text) => {
    const s = makeSegment({ start: t, end: t + 3.5, text });
    t += 3.7;
    return s;
  });
  return { style, source: { meta: { duration: t } }, analysis: { silences: [] }, transcript: { segments: segs }, cards: [], assets: [], brandKeywords: ['brand', 'konten'] };
}

test('preset bible The Brand Fixer jadi default & memakai font/warna bible', () => {
  assert.equal(listPresets()[0].id, 'brand-fixer');
  const st = resolveStyle(getPreset('brand-fixer'), 'editorial');
  assert.equal(st.fonts.key, 'Archivo ExtraBold');
  assert.equal(st.fonts.accent, 'Fraunces Italic');
  assert.equal(st.colors.accent, '#B84A2E');
  assert.equal(st.audio.sfxPalette, 'quiet');
});

test('penekanan "serif": maksimal satu kata Fraunces per frasa', () => {
  const seg = makeSegment({ start: 0, end: 2, text: 'brand konten sistem' });
  seg.words.forEach((w) => (w.emph = true));
  const ph = resolveEmphasis(buildPhrases([seg], { maxWords: 4 }), 'serif');
  assert.deepEqual(ph[0].words.map((w) => w.style), ['script', null, null]);
});

test('planner: "bukan X, tapi Y" → kartu banding; poin berurutan → checklist; tanpa whoosh', () => {
  const p = project([
    'Kenapa brand kamu belum dipilih padahal bagus?',
    'Masalahnya bukan kurang konten, tapi brand kamu belum jelas.',
    'Pertama, tentukan siapa yang kamu layani.',
    'Kedua, tulis janji yang bisa dibuktikan.',
    'Ketiga, ulangi pesan itu di semua konten.',
    'Penutup yang cukup panjang untuk memberi ruang.',
  ]);
  const plan = rulePlan(p);
  const cmp = plan.cards.find((c) => c.type === 'compare');
  assert.ok(cmp, 'kartu banding ada');
  assert.equal(cmp.title, 'kurang konten');
  assert.equal(cmp.subtitle, 'brand kamu belum jelas');
  const list = plan.cards.find((c) => c.type === 'list');
  assert.ok(list, 'checklist rangkuman ada');
  assert.equal(list.subtitle.split(';').length, 3);
  assert.ok(plan.sfx.every((s) => ['click', 'pop'].includes(s.builtin)));
  // Otomatis: kartu yang seluruh teksnya diucapkan langsung disetujui.
  const items = planToItems(plan, 'aturan', p.transcript.segments, { autoApprove: true });
  assert.ok(items.cards.filter((c) => !c.needsReview).every((c) => c.approved && c.autoApproved));
  assert.ok(items.hook.approved);
  assert.ok(items.cuts.every((c) => !c.enabled));
});

test('hook diambil dari kata pembuka yang diucapkan', () => {
  const seg = makeSegment({ start: 0, end: 3, text: 'Kenapa brand kamu belum dipilih?' });
  const hk = hookSuggestion([seg], new Set(['brand']), 1.6);
  // Pola lockup bible: "kenapa brand kamu / Belum / dipilih".
  assert.equal(hk.big, 'Belum');
  assert.equal(hk.lead, 'kenapa brand kamu');
  assert.ok(hk.end <= 3.5);
});

test('ASS: hook menyembunyikan caption & end card ditambahkan setelah video', () => {
  const p = project(['Kenapa brand kamu belum dipilih padahal bagus?', 'Isi video.']);
  p.hook = { approved: true, start: 0, end: 1.5, lead: 'kenapa', big: 'Brand', accent: 'kamu belum' };
  const ass = buildAss(p, { width: 1080, height: 1920, keep: keepSegments(p.source.meta.duration, []), endSpan: { start: 7.4, end: 9.4 } });
  assert.match(ass, /HookBig,,0,0,0,,\{[^}]*\\fscx112\\fscy112\\t\(0,200,\\fscx100\\fscy100\)/);
  assert.match(ass, /Tapi Belum/);
  // Tidak ada caption yang mulai sebelum hook selesai.
  const caps = ass.split('\n').filter((l) => /^Dialogue: 3,/.test(l)).map((l) => l.split(',')[1]);
  assert.ok(caps.every((t) => t >= '0:00:01.50'));
});

test('template HyperFrames tema bible: semua jenis kartu menghasilkan HTML + timeline', () => {
  const st = resolveStyle(getPreset('brand-fixer'), 'editorial');
  for (const type of ['keyword', 'number', 'list', 'compare', 'quote', 'flow', 'chat', 'endcard']) {
    const html = brandFixerHtml({ type, title: type === 'number' ? '120' : 'Brand belum jelas', subtitle: 'a; b; c', kicker: 'kenapa' }, st, { W: 1080, H: 1920, dur: 2.5 });
    assert.match(html, /window\.__timelines\['root'\] = tl/, type);
    assert.match(html, /Archivo-ExtraBold\.ttf/, type);
    if (type === 'chat') assert.match(html, /background:transparent/);
  }
});

test('teks kartu otomatis tidak terpotong menggantung ("…ditemukan belum")', () => {
  const p = project(['Banyak owner sibuk bikin konten setiap hari.', 'Faktanya, brand yang ditemukan belum tentu dipilih.', 'Isi.', 'Isi lagi.']);
  const c = rulePlan(p).cards.find((x) => x.kicker === 'Faktanya');
  assert.ok(c, 'kartu Faktanya ada');
  assert.equal(c.title, 'brand yang ditemukan');
  assert.equal(c.subtitle, 'belum tentu dipilih');
});

test('pola dari transkrip asli: hook "belum tentu", enumerasi → alur/checklist, potongan kata terulang', () => {
  const p = project([
    'Faktanya, brand yang ditemukan belum tentu direkomendasikan.',
    'Buka Instagram, cek Google, tanya teman, lalu bandingin satu per satu.',
    'Biasanya, brand yang lebih mudah direkomendasikan adalah brand yang signalnya jelas, jelas kategorinya, jelas untuk siapa, pesannya konsisten dan ada bukti yang bikin orang merasa aman.',
    'Karena, brand bukan cuma harus ditemukan, brand harus punya alasan untuk direkomendasikan.',
    'Komendasikan, simpan ini kalau kamu sedang ngebangun brand.',
  ]);
  // Beri jarak antar kalimat seperti video asli (±65 dtk) agar ritme kartu tidak memotong saran.
  p.transcript.segments = p.transcript.segments.map((sg, i) => makeSegment({ start: i * 9 + (i ? 0 : 1), end: i * 9 + 7.5, text: sg.text }));
  p.source.meta.duration = 50;
  const plan = rulePlan(p);
  assert.deepEqual([plan.hook.lead, plan.hook.big, plan.hook.accent], ['brand yang ditemukan', 'Belum Tentu', 'direkomendasikan']);
  const flow = plan.cards.find((c) => c.type === 'flow');
  assert.equal(flow?.title, 'Buka Instagram');
  const list = plan.cards.find((c) => c.type === 'list');
  assert.equal(list?.title, 'brand yang lebih mudah direkomendasikan');
  assert.ok(list.subtitle.startsWith('signalnya jelas; jelas kategorinya'));
  assert.ok(plan.cuts.some((c) => c.kind === 'pengulangan' && c.start === p.transcript.segments[4].words[0].start));
  assert.ok(!plan.cards.some((c) => c.cta && /cek/i.test(c.title)));
});
