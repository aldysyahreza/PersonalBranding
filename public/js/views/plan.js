// Langkah 3 — Rencana edit: saran (aturan lokal / Claude opsional) yang harus disetujui pengguna.
import { h, toast, consentDialog, badge, originBadge, num, select } from '../ui.js';
import { api } from '../api.js';
import { store, edit, setProject } from '../store.js';
import { go } from '../app.js';
import { musicLibrary, sfxOptions, previewButton } from '../library.js';
import { pacingButton, pacingIssues } from '../pacing.js';
import { ICON_NAMES, LEGACY_ICON } from '../../shared/icons.js';
import { fmtTime, uid, r3, tokenize, normWord } from '../../shared/core.js';

export const ICON_OPTIONS = [['auto', 'Ikon otomatis (sesuai isi)'], ['', 'Tanpa ikon'], ...ICON_NAMES.map((n) => [n, `Ikon: ${n}`])];
export const CARD_TYPES = [['keyword', 'Kata kunci (blok aksen)'], ['number', 'Angka besar'], ['list', 'Daftar poin']];

/** Kata pada kartu yang tidak ditemukan di ucapan sekitar rentang kartu. */
export function unknownCardWords(card, segments) {
  const spoken = new Set(segments.filter((s) => s.end >= card.start - 1.5 && s.start <= card.end + 1.5).flatMap((s) => tokenize(s.text).map(normWord)));
  const numeric = card.numberValue ? normWord(card.title) : null;
  return [card.kicker, card.title, card.subtitle].flatMap((t) => tokenize(String(t || '').replace(/[;|]/g, ' ')).map(normWord)).filter((w) => w && !spoken.has(w) && w !== numeric);
}

export function renderPlan(main) {
  const p = store.project;
  main.append(h('div', { class: 'view-head' }, h('h1', {}, 'Rencana edit'), h('p', { class: 'muted' }, 'Semua saran berstatus "Disarankan" sampai Anda setujui. Hanya item yang disetujui yang masuk preview & ekspor.')));
  if (!p.source) return main.append(h('div', { class: 'panel' }, 'Impor video terlebih dahulu.'));
  const video = h('video', { src: `/api/projects/${p.id}/media/source`, controls: true, preload: 'metadata', class: 'side-video' });
  const seek = (t) => {
    video.currentTime = Math.max(0, t - 0.5);
    video.play();
  };
  const col = h('div', { class: 'split-main' });
  main.append(h('div', { class: 'split' }, col, h('aside', { class: 'split-side' }, h('div', { class: 'sticky' }, video))));

  // --- Generator ---
  const segs = p.transcript?.segments || [];
  const claude = store.status.claude;
  col.append(
    h('section', { class: 'panel' },
      h('div', { class: 'row between wrap' }, h('h2', {}, 'Buat saran'), pacingButton()),
      pacingIssues(p).length ? h('div', { class: 'alert warn small' }, `Ritme: ${pacingIssues(p).length} kartu/zoom terlalu rapat atau terlalu singkat — adegan wajah bisa terasa terlalu cepat. Klik "Rapikan ritme".`) : null,
      !segs.length ? h('div', { class: 'alert warn' }, 'Belum ada transkrip: saran penekanan, kartu, dan struktur membutuhkan transkrip. Saran cut dari jeda tetap bisa dibuat.') : null,
      p.transcript && !p.transcript.reviewed ? h('div', { class: 'alert warn' }, 'Transkrip belum ditandai sudah dikoreksi. Saran mengikuti teks saat ini.') : null,
      h('div', { class: 'provider' }, h('div', {}, h('strong', {}, 'Saran berbasis aturan (lokal)'), h('div', { class: 'muted small' }, 'Heuristik transparan: angka → kartu angka, "pertama/kedua" → kartu poin, kata kunci brand → penekanan, jeda > 0,5 dtk → cut, segmen > 6 dtk → ide b-roll.')),
        h('button', { class: 'btn primary', onclick: () => generate(p, 'rules') }, 'Buat saran aturan')),
      h('div', { class: `provider ${claude.configured ? '' : 'off'}` }, h('div', {}, h('strong', {}, `Saran AI — Claude (${claude.model})`), h('div', { class: 'muted small' }, claude.configured ? 'Hanya teks transkrip yang dikirim, setelah persetujuan. Hasil tetap perlu ditinjau.' : 'Belum tersedia: isi ANTHROPIC_API_KEY di .env lalu jalankan ulang (opsional).')),
        h('button', { class: 'btn', disabled: !claude.configured || !segs.length, onclick: async () => {
          const ok = await consentDialog({ title: 'Kirim transkrip ke Claude?', service: 'Anthropic Claude API', sent: 'teks transkrip beserta timestamp dan durasi video.', notSent: 'video, audio, wajah, nama file, API key lain.' });
          if (ok) generate(p, 'claude', true);
        } }, 'Buat saran AI')),
      p.plan ? h('p', { class: 'muted small' }, `Saran terakhir: ${p.plan.origin === 'claude' ? 'Claude' : 'aturan'} · ${new Date(p.plan.at).toLocaleString('id-ID')}. Membuat ulang hanya mengganti saran yang belum disetujui.`) : null,
    ),
  );

  if (p.plan?.structure?.length) {
    col.append(h('section', { class: 'panel' }, h('h2', {}, 'Struktur'), h('div', { class: 'structure' }, ...p.plan.structure.map((s) =>
      h('div', { class: 'struct' }, h('strong', {}, s.part), h('span', { class: 'muted' }, `${fmtTime(s.start)}–${fmtTime(s.end)}`), s.text ? h('q', {}, s.text) : null, h('div', { class: 'muted small' }, s.reason), h('button', { class: 'link', onclick: () => seek(s.start) }, 'Putar'))),
    ), ...(p.plan.notes || []).map((n) => h('p', { class: 'muted small' }, n))));
  }

  col.append(emphasisPanel(p, seek), cardsPanel(p, seek), zoomPanel(p, seek), brollPanel(p, seek), audioPanel(p, seek), cutsPanel(p, seek));
  col.append(h('div', { class: 'row end' }, h('button', { class: 'btn primary', onclick: () => go('editor') }, 'Lanjut ke Editor →')));
}

async function generate(p, source, consent) {
  try {
    const { saveNow } = await import('../store.js');
    await saveNow();
    setProject(await api.plan(p.id, source, consent), { keepHistory: true });
    toast('Saran dibuat. Tinjau dan setujui yang sesuai.', 'ok');
  } catch (e) {
    toast(e.message, 'error', e.hint);
  }
}

function section(title, help, items, actions) {
  return h('section', { class: 'panel' }, h('div', { class: 'row between wrap' }, h('h2', {}, title), h('div', { class: 'row' }, ...(actions || []))), help ? h('p', { class: 'muted small' }, help) : null, ...(items.length ? items : [h('p', { class: 'muted' }, 'Belum ada item.')]));
}

function approveToggle(item, onToggle, label = 'Setujui') {
  return h('label', { class: `approve ${item.approved ? 'on' : ''}` }, h('input', { type: 'checkbox', checked: !!item.approved, onchange: (e) => onToggle(e.target.checked) }), item.approved ? 'Disetujui' : label);
}

function timeFields(list, i, seek, dur) {
  const it = store.project[list][i];
  const set = (k) => (v) => edit((x) => (x[list][i][k] = r3(Math.max(0, Math.min(dur, v)))));
  return h('span', { class: 'row' }, h('button', { class: 'btn icon', onclick: () => seek(it.start ?? it.time) }, '▶'),
    'start' in it ? [num(it.start, set('start'), { step: 0.05, width: '5em' }), '–', num(it.end, set('end'), { step: 0.05, width: '5em' })] : num(it.time, set('time'), { step: 0.05, width: '5em' }));
}

function emphasisPanel(p, seek) {
  const segs = p.transcript?.segments || [];
  const items = (p.emphasisSuggestions || []).map((e, i) => {
    const seg = segs.find((s) => s.id === e.segId);
    const w = seg?.words?.[e.wordIndex];
    const live = w && !!w.emph;
    return h('div', { class: 'item' },
      h('span', { class: 'row' }, h('button', { class: 'btn icon', onclick: () => seg && seek(w?.start ?? seg.start) }, '▶'), h('strong', { class: 'emph-word' }, e.word)),
      h('span', { class: 'muted small grow' }, seg ? `“${seg.text.slice(0, 70)}”` : 'Segmen sudah tidak ada', h('br'), e.reason),
      originBadge(e.origin),
      approveToggle({ approved: live }, (on) => edit((x) => {
        const ww = x.transcript.segments.find((s) => s.id === e.segId)?.words?.[e.wordIndex];
        if (ww) ww.emph = on || undefined;
        x.emphasisSuggestions[i].approved = on;
      })),
    );
  });
  return section('Penekanan kata', 'Kata yang diberi blok warna aksen di subtitle. Bisa juga diatur langsung di Transkrip dengan klik kata.', items, [
    items.length ? h('button', { class: 'btn ghost sm', onclick: () => edit((x) => x.emphasisSuggestions.forEach((e) => {
      const ww = x.transcript.segments.find((s) => s.id === e.segId)?.words?.[e.wordIndex];
      if (ww) ww.emph = true;
      e.approved = true;
    })) }, 'Setujui semua') : null,
  ]);
}

function cardsPanel(p, seek) {
  const dur = p.source.meta.duration;
  const segs = p.transcript?.segments || [];
  const items = (p.cards || []).map((c, i) => {
    const unknown = unknownCardWords(c, segs);
    const set = (k) => (e) => edit((x) => {
      x.cards[i][k] = e.target.value;
      x.cards[i].needsReview = unknownCardWords(x.cards[i], segs).length > 0;
    });
    return h('div', { class: `item card-item ${c.approved ? 'approved' : ''}` },
      h('div', { class: 'row wrap' }, timeFields('cards', i, seek, dur), select(c.type, CARD_TYPES, (v) => edit((x) => (x.cards[i].type = v))), select(c.layout || 'full', [['full', 'Layar penuh'], ['panel', 'Panel bawah (wajah terlihat)']], (v) => edit((x) => (x.cards[i].layout = v))), select(LEGACY_ICON[c.icon] || (c.icon ?? 'auto'), ICON_OPTIONS, (v) => edit((x) => (x.cards[i].icon = v))), originBadge(c.origin),
        approveToggle(c, (on) => edit((x) => (x.cards[i].approved = on))), h('button', { class: 'link danger', onclick: () => edit((x) => x.cards.splice(i, 1)) }, 'Hapus')),
      h('div', { class: 'grid3' },
        h('label', { class: 'field' }, h('span', { class: 'field-label' }, 'Label atas'), h('input', { value: c.kicker || '', onchange: set('kicker') })),
        h('label', { class: 'field' }, h('span', { class: 'field-label' }, c.type === 'number' ? 'Angka' : 'Judul'), h('input', { value: c.title || '', onchange: set('title') })),
        h('label', { class: 'field' }, h('span', { class: 'field-label' }, c.type === 'list' ? 'Poin (pisahkan dengan ;)' : 'Label bawah'), h('input', { value: c.subtitle || '', onchange: set('subtitle') })),
      ),
      h('div', { class: 'muted small' }, c.reason || ''),
      c.pacingNote && !c.approved ? h('div', { class: 'alert warn small' }, c.pacingNote) : null,
      unknown.length ? h('div', { class: 'alert warn small' }, `Kata tidak ditemukan di ucapan sekitar kartu: ${unknown.join(', ')}. Pastikan tidak menambah klaim/fakta baru.`) : null,
    );
  });
  return section('Kartu visual', 'Tipografi besar, angka, atau poin di layar terang. Teks kartu sebaiknya diambil dari ucapan Anda.', items, [
    h('button', { class: 'btn ghost sm', onclick: () => edit((x) => x.cards.push({ id: uid('card'), origin: 'pengguna', approved: true, type: 'keyword', layout: 'full', start: r3(store.playhead || 0), end: r3((store.playhead || 0) + 2), kicker: '', title: 'Judul', subtitle: '', icon: '' })) }, '+ Kartu'),
    items.length ? h('button', { class: 'btn ghost sm', onclick: () => edit((x) => x.cards.forEach((c) => (c.approved = true))) }, 'Setujui semua') : null,
  ]);
}

function assetOptions(p, kinds) {
  return [['', '— Belum ada aset —'], ...p.assets.filter((a) => kinds.includes(a.kind)).map((a) => [a.id, `${a.name}${a.missing ? ' (hilang)' : ''} · lisensi: ${a.license}`])];
}

/** Kartu kata kunci dari kata yang diucapkan pada rentang b-roll (pengganti footage). */
function cardFromSpeech(p, b) {
  const words = (p.transcript?.segments || []).flatMap((s) => s.words || []).filter((w) => w.start >= b.start - 0.2 && w.start < b.end);
  const toks = [];
  for (const w of words) {
    toks.push(w.text);
    if (toks.length >= 4 || /[.,!?;:…]$/.test(w.text)) break;
  }
  const STOP = new Set(['yang', 'dan', 'di', 'ke', 'dari', 'untuk', 'dengan', 'itu', 'atau', 'kalau', 'tapi', 'tanpa', 'kamu', 'saya']);
  while (toks.length > 1 && STOP.has(normWord(toks[toks.length - 1]))) toks.pop();
  const title = toks.join(' ').replace(/[.,!?;:…]+$/, '');
  return { id: uid('card'), origin: 'pengguna', approved: true, type: 'keyword', layout: 'full', start: b.start, end: Math.min(b.end, b.start + 2), kicker: '', title: title || 'Judul', subtitle: '', icon: '', reason: 'Pengganti b-roll; diambil dari ucapan pada rentang ini — rapikan teksnya.' };
}

function brollPanel(p, seek) {
  const dur = p.source.meta.duration;
  const items = (p.broll || []).map((b, i) => {
    const asset = p.assets.find((a) => a.id === b.assetId);
    return h('div', { class: `item ${b.approved ? 'approved' : ''}` },
      h('div', { class: 'row wrap' }, timeFields('broll', i, seek, dur), originBadge(b.origin), asset ? badge(asset.missing ? 'Aset hilang' : 'Aset tersedia', asset.missing ? 'error' : 'ok') : badge('Hanya saran — belum ada aset', 'warn'),
        approveToggle(b, (on) => edit((x) => (x.broll[i].approved = on))), h('button', { class: 'link danger', onclick: () => edit((x) => x.broll.splice(i, 1)) }, 'Hapus')),
      h('div', {}, h('strong', {}, b.idea || 'B-roll'), h('div', { class: 'muted small' }, b.reason || '')),
      h('div', { class: 'row wrap' }, h('span', { class: 'muted small' }, 'Aset:'), select(b.assetId || '', assetOptions(p, ['image', 'video']), (v) => edit((x) => (x.broll[i].assetId = v || null))), h('button', { class: 'link', onclick: () => go('editor') }, 'Kelola aset di Editor →'),
        !asset ? [h('span', { class: 'muted small' }, 'Tidak punya footage?'),
          h('button', { class: 'btn ghost sm', onclick: () => edit((x) => { x.cards.push(cardFromSpeech(x, b)); x.broll.splice(i, 1); }) }, 'Jadikan kartu'),
          h('button', { class: 'btn ghost sm', onclick: () => edit((x) => { x.zooms.push({ id: uid('zoom'), origin: 'pengguna', approved: true, start: b.start, end: b.end, zoom: x.style.zoom?.punchIn ?? 1.12, reason: 'Pengganti b-roll' }); x.broll.splice(i, 1); }) }, 'Jadikan zoom')] : null),
    );
  });
  return section('Footage sisipan (B-roll)', 'Aplikasi tidak menyediakan atau membuat footage stok/AI. Pilih footage milik Anda (Editor → Aset) dan catat lisensinya. Item tanpa aset dilewati saat ekspor.', items, [
    h('button', { class: 'btn ghost sm', onclick: () => edit((x) => x.broll.push({ id: uid('broll'), origin: 'pengguna', approved: true, start: r3(store.playhead || 0), end: r3((store.playhead || 0) + 2), idea: 'B-roll manual', reason: '', assetId: null })) }, '+ B-roll'),
  ]);
}

function audioPanel(p, seek) {
  const dur = p.source.meta.duration;
  const sfxOpts = sfxOptions(p);
  const items = (p.sfx || []).map((s, i) => h('div', { class: `item ${s.approved ? 'approved' : ''}` },
    h('div', { class: 'row wrap' }, timeFields('sfx', i, seek, dur),
      select(s.builtin ? `builtin:${s.builtin}` : `asset:${s.assetId}`, sfxOpts, (v) => edit((x) => {
        const [k, id] = v.split(':');
        x.sfx[i].builtin = k === 'builtin' ? id : null;
        x.sfx[i].assetId = k === 'asset' ? id : null;
      })),
      s.builtin ? previewButton('sfx', s.builtin) : null,
      h('span', { class: 'muted small' }, 'dB'), num(s.volumeDb || 0, (v) => edit((x) => (x.sfx[i].volumeDb = v)), { step: 1, width: '4em' }),
      originBadge(s.origin), approveToggle(s, (on) => edit((x) => (x.sfx[i].approved = on))), h('button', { class: 'link danger', onclick: () => edit((x) => x.sfx.splice(i, 1)) }, 'Hapus')),
    h('div', { class: 'muted small' }, s.reason || '')));
  const music = p.music;
  const musicAsset = p.assets.find((a) => a.id === music.assetId);
  const musicBox = h('div', { class: 'item' },
    h('div', { class: 'row wrap' }, h('strong', {}, 'Musik latar'), musicAsset ? badge('Aset tersedia', 'ok') : badge('Belum ada musik — placeholder', 'warn'),
      h('label', { class: 'check' }, h('input', { type: 'checkbox', checked: !!music.enabled, disabled: !musicAsset, onchange: (e) => edit((x) => (x.music.enabled = e.target.checked)) }), ' Aktifkan')),
    h('div', { class: 'row wrap' }, select(music.assetId || '', assetOptions(p, ['audio']), (v) => edit((x) => (x.music.assetId = v || null))), h('span', { class: 'muted small' }, 'Volume (dB)'), num(music.volumeDb, (v) => edit((x) => (x.music.volumeDb = v)), { step: 1, width: '4.5em' })),
    h('div', { class: 'muted small' }, (!musicAsset && p.plan?.music?.reason) || 'Musik otomatis diredam (ducking) saat Anda berbicara. Musik milik sendiri bisa diimpor di Editor → Aset.'),
    musicLibrary(p),
  );
  return section('Audio: musik & sound effect', 'Musik & SFX bawaan disintesis dari nol oleh aplikasi (bukan rekaman pihak lain) — bebas royalti. Anda juga bisa memakai file berlisensi milik sendiri.', [musicBox, ...items], [
    h('button', { class: 'btn ghost sm', onclick: () => edit((x) => x.sfx.push({ id: uid('sfx'), origin: 'pengguna', approved: true, time: r3(store.playhead || 0), builtin: 'pop', assetId: null, volumeDb: 0 })) }, '+ SFX'),
    items.length ? h('button', { class: 'btn ghost sm', onclick: () => edit((x) => x.sfx.forEach((s) => (s.approved = true))) }, 'Setujui semua SFX') : null,
  ]);
}

function zoomPanel(p, seek) {
  const dur = p.source.meta.duration;
  const items = (p.zooms || []).map((z, i) => h('div', { class: `item ${z.approved ? 'approved' : ''}` },
    h('div', { class: 'row wrap' }, timeFields('zooms', i, seek, dur),
      h('span', { class: 'muted small' }, 'Zoom'), num(z.zoom, (v) => edit((x) => (x.zooms[i].zoom = Math.min(1.5, Math.max(1, v)))), { step: 0.01, width: '4.5em' }), h('span', { class: 'muted small' }, '×'),
      originBadge(z.origin), h('span', { class: 'muted small grow' }, z.reason || ''),
      approveToggle(z, (on) => edit((x) => (x.zooms[i].approved = on))), h('button', { class: 'link danger', onclick: () => edit((x) => x.zooms.splice(i, 1)) }, 'Hapus'))));
  return section('Zoom punch-in', 'Framing berganti dekat–normal antar kalimat (jump-cut zoom), seperti di video referensi. Memakai video Anda sendiri, tanpa footage tambahan. Hanya berlaku pada mode bingkai "Isi".', items, [
    h('button', { class: 'btn ghost sm', onclick: () => edit((x) => x.zooms.push({ id: uid('zoom'), origin: 'pengguna', approved: true, start: r3(store.playhead || 0), end: r3(Math.min(dur, (store.playhead || 0) + 2)), zoom: x.style.zoom?.punchIn ?? 1.12 })) }, '+ Zoom'),
    items.length ? h('button', { class: 'btn ghost sm', onclick: () => edit((x) => x.zooms.forEach((z) => (z.approved = true))) }, 'Setujui semua') : null,
  ]);
}

function cutsPanel(p, seek) {
  const dur = p.source.meta.duration;
  const total = (p.cuts || []).filter((c) => c.enabled).reduce((s, c) => s + c.end - c.start, 0);
  const items = (p.cuts || []).map((c, i) => h('div', { class: `item ${c.enabled ? 'approved' : ''}` },
    h('div', { class: 'row wrap' }, timeFields('cuts', i, seek, dur), badge(c.kind || 'manual'), originBadge(c.origin),
      h('span', { class: 'muted small grow' }, c.reason || ''),
      approveToggle({ approved: c.enabled }, (on) => edit((x) => {
        x.cuts[i].enabled = on;
        x.cuts[i].approved = on;
      }), 'Potong'), h('button', { class: 'link danger', onclick: () => edit((x) => x.cuts.splice(i, 1)) }, 'Hapus'))));
  return section(`Potongan (cut) — ${total.toFixed(1)} dtk dibuang`, 'Bagian yang dipotong tidak menghapus apa pun dari file sumber; hanya dilewati saat preview & ekspor. Dengarkan sebelum menyetujui.', items, [
    h('button', { class: 'btn ghost sm', onclick: () => edit((x) => x.cuts.push({ id: uid('cut'), origin: 'pengguna', enabled: true, approved: true, kind: 'manual', start: r3(store.playhead || 0), end: r3(Math.min(dur, (store.playhead || 0) + 0.5)), reason: 'Cut manual' })) }, '+ Cut'),
    items.length ? h('button', { class: 'btn ghost sm', onclick: () => edit((x) => x.cuts.forEach((c) => (c.enabled = c.approved = true))) }, 'Setujui semua') : null,
  ]);
}
