import { test } from 'node:test';
import assert from 'node:assert/strict';
import { keepSegments, mapTime, mapSpan, outputDuration, buildPhrases, makeSegment, syncSegmentWords, parseSubtitles, toSrt, distributeText, splitLeadKey, framing } from '../public/shared/core.js';

test('keepSegments membuang cut aktif saja', () => {
  const keep = keepSegments(10, [{ start: 2, end: 3, enabled: true }, { start: 5, end: 6, enabled: false }]);
  assert.deepEqual(keep, [{ start: 0, end: 2 }, { start: 3, end: 10 }]);
  assert.equal(outputDuration(keep), 9);
});

test('mapTime memetakan waktu sumber ke output dan null di bagian terpotong', () => {
  const keep = keepSegments(10, [{ start: 2, end: 3, enabled: true }]);
  assert.equal(mapTime(1, keep), 1);
  assert.equal(mapTime(2.5, keep), null);
  assert.equal(mapTime(4, keep), 3);
  assert.deepEqual(mapSpan(1, 4, keep), { start: 1, end: 3 });
});

test('buildPhrases tidak mengubah teks dan menghormati batas kata', () => {
  const seg = makeSegment({ start: 0, end: 4, text: 'Pertama, tentukan positioning yang jelas untuk bisnis.' });
  const phrases = buildPhrases([seg], { maxWords: 4, maxChars: 30 });
  const rejoined = phrases.map((p) => p.words.map((w) => w.text).join(' ')).join(' ');
  assert.equal(rejoined, seg.text);
  for (const p of phrases) assert.ok(p.words.length <= 4);
});

test('syncSegmentWords mempertahankan timestamp & penekanan saat jumlah kata sama', () => {
  const seg = makeSegment({ start: 0, end: 2, text: 'halo dunia', words: [{ text: 'halo', start: 0.1, end: 0.5 }, { text: 'dunia', start: 0.6, end: 1.2 }], timing: 'asr' });
  seg.words[1].emph = true;
  seg.text = 'Halo dunia!';
  syncSegmentWords(seg);
  assert.equal(seg.words[0].start, 0.1);
  assert.equal(seg.words[1].text, 'dunia!');
  assert.equal(seg.words[1].emph, true);
  assert.equal(seg.timing, 'asr');
  seg.text = 'halo semua dunia';
  syncSegmentWords(seg);
  assert.equal(seg.words.length, 3);
  assert.equal(seg.timing, 'estimated');
});

test('SRT parse ↔ export', () => {
  const srt = '1\n00:00:01,000 --> 00:00:02,500\nHalo semua\n\n2\n00:00:03,000 --> 00:00:04,000\nIni tes\n';
  const segs = parseSubtitles(srt);
  assert.equal(segs.length, 2);
  assert.equal(segs[0].start, 1);
  assert.equal(segs[0].end, 2.5);
  assert.match(toSrt(segs), /00:00:01,000 --> 00:00:02,500\nHalo semua/);
});

test('distributeText mengikuti rentang ucapan', () => {
  const segs = distributeText('Satu dua. Tiga empat.', [{ start: 1, end: 2 }, { start: 3, end: 4 }], 5);
  assert.equal(segs.length, 2);
  assert.ok(segs[0].start >= 1);
  assert.ok(segs[1].end <= 4.001);
});

test('splitLeadKey memulai baris besar di kata yang ditekankan', () => {
  const words = ['yang', 'menahan', 'konten', 'kamu'].map((t) => ({ text: t }));
  words[2].emph = true;
  const { lead, key } = splitLeadKey(words);
  assert.deepEqual(lead.map((w) => w.text), ['yang', 'menahan']);
  assert.deepEqual(key.map((w) => w.text), ['konten', 'kamu']);
});

test('framing menutupi bingkai output', () => {
  const f = framing(1920, 1080, 1080, 1920, { x: 0.5, y: 0.5, zoom: 1 });
  assert.ok(f.sw >= 1080 && f.sh >= 1920);
  assert.equal(f.cy, 0);
});

test('zoomPieces memecah rentang keep di batas zoom yang disetujui', async () => {
  const { zoomPieces } = await import('../public/shared/core.js');
  const keep = keepSegments(10, [{ start: 4, end: 5, enabled: true }]);
  const pieces = zoomPieces(keep, [{ start: 2, end: 6, zoom: 1.2, approved: true }, { start: 8, end: 9, zoom: 1.5, approved: false }]);
  assert.deepEqual(pieces, [
    { start: 0, end: 2, zoom: 1 },
    { start: 2, end: 4, zoom: 1.2 },
    { start: 5, end: 6, zoom: 1.2 },
    { start: 6, end: 10, zoom: 1 },
  ]);
});
