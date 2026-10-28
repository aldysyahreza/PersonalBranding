// Langkah 4 — Editor: preview + timeline + kontrol gaya, bingkai, warna, audio, aset.
import { h, toast, modal, field, slider, select, num, badge, fmtBytes } from '../ui.js';
import { api } from '../api.js';
import { store, edit, setProject } from '../store.js';
import { go, runJob, onJob } from '../app.js';
import { createPreview } from '../preview.js';
import { createTimeline } from '../timeline.js';
import { OUTPUT_FORMATS, r3 } from '../../shared/core.js';
import { CARD_TYPES, ICON_OPTIONS } from './plan.js';
import { LEGACY_ICON } from '../../shared/icons.js';
import { musicLibrary, sfxOptions, previewButton } from '../library.js';
import { pacingButton } from '../pacing.js';

let preview = null;
let timeline = null;
let tab = 'gaya';
let inspector = null;
let offJob = null;

export function destroyEditor() {
  preview?.destroy();
  preview = null;
  timeline = null;
  inspector = null;
}

export function refreshPreview() {
  preview?.refresh();
  timeline?.draw();
  renderInspector();
}

const FONTS = ['Montserrat Medium', 'Montserrat Bold', 'Montserrat ExtraBold', 'Montserrat Black', 'Great Vibes', 'Inter Medium', 'Inter SemiBold', 'Inter Bold', 'Inter ExtraBold', 'Inter Black'].map((f) => [f, f]);

/** Ubah gaya tanpa merender ulang seluruh halaman (preview diperbarui langsung). */
const setStyle = (path, key) => (v) => edit((x) => {
  const parts = path.split('.');
  let o = x;
  for (const k of parts.slice(0, -1)) o = o[k];
  o[parts.at(-1)] = v;
}, { key: key || path, rerender: false });

const get = (path) => path.split('.').reduce((o, k) => o?.[k], store.project);

function sl(label, path, opts) {
  return field(label, slider(get(path), (v) => setStyle(path)(v), opts));
}
function chk(label, path) {
  return h('label', { class: 'check' }, h('input', { type: 'checkbox', checked: !!get(path), onchange: (e) => setStyle(path)(e.target.checked) }), ` ${label}`);
}
function sel(label, path, options) {
  return field(label, select(get(path), options, (v) => setStyle(path)(v)));
}
function color(label, path) {
  return field(label, h('input', { type: 'color', value: get(path), oninput: (e) => setStyle(path)(e.target.value) }));
}

export function renderEditor(main) {
  preview?.destroy();
  preview = null;
  const p = store.project;
  main.append(h('div', { class: 'view-head' }, h('h1', {}, 'Editor'), h('p', { class: 'muted' }, 'Preview cepat di browser mengikuti aturan render yang sama. Untuk hasil persis piksel, gunakan "Cek frame akurat" atau "Render pratinjau".')));
  if (!p.source) return main.append(h('div', { class: 'panel' }, 'Impor video terlebih dahulu.'));
  if (p.source.missing) return main.append(h('div', { class: 'alert error' }, `File sumber tidak ditemukan: ${p.source.path}`));

  preview = createPreview();
  timeline = createTimeline({ onSeek: (t) => preview.seek(t), onSelect: (s) => { store.selected = s; tab = 'item'; renderTabs(); timeline.draw(); } });
  preview.el.addEventListener('time', (e) => timeline.setTime(e.detail));

  const frameOut = h('div', { class: 'accurate' });
  const tools = h('div', { class: 'row wrap' },
    pacingButton(),
    h('button', { class: 'btn', onclick: async (e) => {
      const b = e.currentTarget;
      b.disabled = true;
      b.textContent = 'Merender frame…';
      try {
        const { saveNow } = await import('../store.js');
        await saveNow();
        const r = await api.still(p.id, { sourceTime: preview.video.currentTime, aspect: p.output.aspect });
        frameOut.replaceChildren(h('div', { class: 'muted small' }, `Frame ffmpeg pada output ${r.outputTime.toFixed(2)} dtk (setengah resolusi)`), r.note ? h('div', { class: 'alert warn small' }, r.note) : null, h('img', { src: r.url, alt: 'Frame hasil render' }));
      } catch (err) {
        toast(err.message, 'error', err.hint);
      } finally {
        b.disabled = false;
        b.textContent = 'Cek frame akurat';
      }
    } }, 'Cek frame akurat'),
    h('button', { class: 'btn', disabled: !!store.jobs[p.id], onclick: async () => {
      const { saveNow } = await import('../store.js');
      await saveNow();
      const res = await runJob(api.render(p.id, { preview: true, aspect: p.output.aspect }), { okMsg: 'Render pratinjau selesai.', reloadFields: ['lastPreview', 'status'] });
      if (res?.state === 'done') showPreviewVideo(frameOut);
    } }, 'Render pratinjau (540p, cepat)'),
    p.lastPreview?.state === 'done' ? h('button', { class: 'btn ghost sm', onclick: () => showPreviewVideo(frameOut) }, 'Lihat pratinjau terakhir') : null,
  );
  offJob?.();
  offJob = onJob((j) => {
    if (j.type === 'render' && j.projectId === p.id) frameOut.replaceChildren(h('div', { class: 'progress' }, h('div', { class: 'bar', style: { width: `${(j.progress || 0) * 100}%` } })), h('div', { class: 'muted small' }, j.message));
  });

  inspector = h('div', { class: 'tabs-body' });
  const tabsHead = h('div', { class: 'tabs' });
  main.append(
    h('div', { class: 'editor' },
      h('div', { class: 'ed-left' }, preview.el, tools, frameOut),
      h('div', { class: 'ed-right panel' }, tabsHead, inspector),
    ),
    timeline.el,
    h('div', { class: 'row end' }, h('button', { class: 'btn primary', onclick: () => go('export') }, 'Lanjut ke Ekspor →')),
  );
  timeline.draw();

  function renderTabs() {
    const TABS = [['gaya', 'Gaya'], ['subtitle', 'Subtitle'], ['kartu', 'Kartu'], ['bingkai', 'Bingkai'], ['warna', 'Warna'], ['audio', 'Audio'], ['aset', 'Aset'], ['item', 'Item terpilih']];
    tabsHead.replaceChildren(...TABS.map(([k, l]) => h('button', { class: `tab ${tab === k ? 'on' : ''}`, onclick: () => { tab = k; renderTabs(); } }, l)));
    renderInspector();
  }
  renderTabs();
}

function showPreviewVideo(box) {
  const p = store.project;
  box.replaceChildren(h('div', { class: 'muted small' }, 'Pratinjau hasil render ffmpeg (termasuk musik, SFX, ducking, warna):'), h('video', { src: `/api/projects/${p.id}/exports/preview/file?t=${Date.now()}`, controls: true, autoplay: true, class: 'render-preview' }));
}

function renderInspector() {
  if (!inspector || !store.project) return;
  const p = store.project;
  const st = p.style;
  const views = {
    gaya: () => [
      h('div', { class: 'alert info small' }, `Preset: ${store.status.presets.find((x) => x.id === p.presetId)?.name || p.presetId} — status: konsep yang dapat diubah. Lihat Profil brand untuk asumsi.`),
      field('Level gaya', h('div', { class: 'row' }, ...store.status.styleLevels.map((l) => h('button', { class: `chip ${p.styleLevel === l ? 'on' : ''}`, onclick: async () => {
        const ok = await modal(`Terapkan level "${l}"?`, h('p', {}, 'Semua pengaturan gaya (subtitle, kartu, warna, audio) diganti dengan nilai preset untuk level ini. Bisa dibatalkan dengan Urungkan.'), [{ label: 'Terapkan', kind: 'primary' }]);
        if (!ok) return;
        try {
          const fresh = await api.applyPreset(p.id, p.presetId, l);
          edit((x) => { x.style = fresh.style; x.styleLevel = fresh.styleLevel; });
        } catch (e) { toast(e.message, 'error', e.hint); }
      } }, l)))),
      h('h4', {}, 'Warna'),
      h('div', { class: 'grid2' }, color('Aksen', 'style.colors.accent'), color('Teks subtitle', 'style.colors.text'), color('Latar kartu', 'style.colors.cardBg'), color('Teks kartu', 'style.colors.cardText'), color('Teks label kartu', 'style.colors.cardMuted')),
      h('h4', {}, 'Font (bundel Inter, lisensi OFL)'),
      sel('Baris kecil / label', 'style.fonts.lead', FONTS), sel('Baris utama & penekanan', 'style.fonts.key', FONTS), sel('Judul kartu', 'style.fonts.card', FONTS),
      h('h4', {}, 'Simpan sebagai preset'),
      savePresetForm(p),
    ],
    subtitle: () => [
      chk('Tampilkan subtitle', 'style.captions.enabled'),
      sel('Tata letak', 'style.captions.layout', [['stack', 'Dua tingkat (kecil + besar)'], ['single', 'Satu baris'], ['karaoke', 'Kata aktif disorot']]),
      sel('Penekanan kata', 'style.captions.emphasis', [['box', 'Blok warna aksen'], ['color', 'Teks warna aksen'], ['none', 'Tanpa penekanan']]),
      sel('Animasi', 'style.captions.animation', [['pop', 'Pop ringan'], ['fade', 'Fade'], ['none', 'Tanpa animasi']]),
      chk('HURUF KAPITAL', 'style.captions.uppercase'),
      sl('Posisi vertikal (dari atas)', 'style.captions.position', { min: 0.3, max: 0.85, step: 0.005, fmt: (v) => `${Math.round(v * 100)}%` }),
      sl('Ukuran baris utama', 'style.captions.keySize', { min: 40, max: 140, step: 1, fmt: (v) => `${v}px` }),
      sl('Ukuran baris kecil', 'style.captions.leadSize', { min: 24, max: 90, step: 1, fmt: (v) => `${v}px` }),
      sl('Maks kata per frasa', 'style.captions.maxWords', { min: 1, max: 8, step: 1 }),
      sl('Maks karakter per frasa', 'style.captions.maxChars', { min: 10, max: 50, step: 1 }),
      sl('Bayangan teks', 'style.captions.shadow', { min: 0, max: 10, step: 0.5 }),
      h('p', { class: 'muted small' }, 'Ukuran dalam piksel untuk lebar 1080. Subtitle dijaga di dalam zona aman. Hidupkan "Zona aman & wajah" di bawah preview untuk memastikan wajah tidak tertutup.'),
    ],
    kartu: () => [
      sel('Mesin grafis kartu layar penuh', 'style.cards.engine', [['hyperframes', 'HyperFrames — animasi kaya, ikon, hitung angka'], ['ass', 'Bawaan — lebih cepat, lebih sederhana']]),
      h('p', { class: `small ${store.status.hyperframes?.ok ? 'muted' : 'alert warn'}` }, store.status.hyperframes?.ok ? `${store.status.hyperframes.detail}. Render pertama tiap kartu memakan beberapa detik (Chrome headless); hasilnya di-cache. Chrome diunduh otomatis sekali saat render pertama.` : `HyperFrames tidak tersedia: ${store.status.hyperframes?.detail || '-'} Kartu bawaan dipakai.`),
      sl('Ukuran judul', 'style.cards.titleSize', { min: 50, max: 180, step: 1, fmt: (v) => `${v}px` }),
      sl('Ukuran angka', 'style.cards.numberSize', { min: 120, max: 420, step: 2, fmt: (v) => `${v}px` }),
      sl('Ukuran label', 'style.cards.labelSize', { min: 24, max: 90, step: 1, fmt: (v) => `${v}px` }),
      sl('Durasi fade masuk', 'style.cards.fadeMs', { min: 0, max: 600, step: 10, fmt: (v) => `${v} ms` }),
      sl('Bayangan', 'style.cards.shadow', { min: 0, max: 20, step: 1 }),
      chk('Pola grid tipis di belakang judul', 'style.cards.grid'),
      h('p', { class: 'muted small' }, 'Isi & waktu tiap kartu diatur di Rencana edit, atau pilih kartu di timeline lalu buka tab "Item terpilih".'),
    ],
    bingkai: () => [
      field('Rasio output', h('div', { class: 'row wrap' }, ...Object.keys(OUTPUT_FORMATS).map((k) => h('button', { class: `chip ${p.output.aspect === k ? 'on' : ''}`, onclick: () => edit((x) => (x.output.aspect = k), { rerender: false }) }, k)))),
      sel('Mode bingkai', 'output.framing', [['fill', 'Isi bingkai (crop)'], ['fit', 'Muat utuh + latar blur']]),
      sl('Posisi horizontal', 'output.reframe.x', { min: 0, max: 1, step: 0.01, fmt: (v) => `${Math.round(v * 100)}%` }),
      sl('Posisi vertikal', 'output.reframe.y', { min: 0, max: 1, step: 0.01, fmt: (v) => `${Math.round(v * 100)}%` }),
      sl('Zoom dasar', 'output.reframe.zoom', { min: 1, max: 2, step: 0.01, fmt: (v) => `${v.toFixed(2)}×` }),
      sl('Kekuatan punch-in (saran baru)', 'style.zoom.punchIn', { min: 1, max: 1.4, step: 0.01, fmt: (v) => `${v.toFixed(2)}×` }),
      h('p', { class: 'muted small' }, 'Item zoom punch-in diatur di Rencana edit atau pilih di timeline (trek "Zoom").'),
      h('h4', {}, 'Zona aman platform'),
      sl('Atas', 'style.safeZone.top', { min: 0, max: 0.3, step: 0.005, fmt: (v) => `${Math.round(v * 100)}%` }),
      sl('Bawah', 'style.safeZone.bottom', { min: 0, max: 0.35, step: 0.005, fmt: (v) => `${Math.round(v * 100)}%` }),
      sl('Samping', 'style.safeZone.side', { min: 0, max: 0.15, step: 0.005, fmt: (v) => `${Math.round(v * 100)}%` }),
      h('h4', {}, 'Zona wajah (panduan, atur sesuai framing Anda)'),
      sl('Atas', 'style.faceZone.top', { min: 0, max: 0.6, step: 0.005, fmt: (v) => `${Math.round(v * 100)}%` }),
      sl('Bawah', 'style.faceZone.bottom', { min: 0.2, max: 0.8, step: 0.005, fmt: (v) => `${Math.round(v * 100)}%` }),
      st.captions.position * 1 > st.faceZone.top && st.captions.position < st.faceZone.bottom ? h('div', { class: 'alert warn small' }, 'Garis subtitle berada di dalam zona wajah — subtitle bisa menutupi wajah.') : null,
    ],
    warna: () => [
      chk('Aktifkan koreksi warna', 'style.color.enabled'),
      sl('Intensitas keseluruhan', 'style.color.intensity', { min: 0, max: 1, step: 0.01, fmt: (v) => `${Math.round(v * 100)}%` }),
      sl('Kecerahan', 'style.color.brightness', { min: -0.15, max: 0.15, step: 0.005 }),
      sl('Kontras', 'style.color.contrast', { min: 0.8, max: 1.3, step: 0.01 }),
      sl('Saturasi', 'style.color.saturation', { min: 0.7, max: 1.25, step: 0.01 }),
      sl('Gamma', 'style.color.gamma', { min: 0.8, max: 1.2, step: 0.01 }),
      sl('Kehangatan', 'style.color.warmth', { min: -0.15, max: 0.15, step: 0.005 }),
      sl('Vignette', 'style.color.vignette', { min: 0, max: 1, step: 0.01 }),
      h('p', { class: 'muted small' }, 'Batas slider sengaja sempit agar warna kulit tetap natural. Preview browser adalah perkiraan; cek dengan "Cek frame akurat". Tidak ada efek yang mengubah bentuk wajah.'),
    ],
    audio: () => [
      chk('Normalisasi loudness suara (−14 LUFS)', 'style.audio.normalize'),
      chk('Filter dengung rendah (high-pass 80 Hz)', 'style.audio.highpass'),
      sl('Gain suara', 'style.audio.voiceGainDb', { min: -12, max: 12, step: 0.5, fmt: (v) => `${v} dB` }),
      h('h4', {}, 'Musik latar'),
      musicControls(p),
      musicLibrary(p),
      h('h4', {}, 'Sound effect'),
      sl('Volume dasar SFX', 'style.audio.sfxDb', { min: -30, max: 0, step: 1, fmt: (v) => `${v} dB` }),
      h('p', { class: 'muted small' }, 'Preview browser memutar suara asli + musik (tanpa ducking/SFX). Dengarkan campuran lengkap lewat "Render pratinjau".'),
    ],
    aset: () => assetsPanel(p),
    item: () => itemInspector(p),
  };
  inspector.replaceChildren(...(views[tab] || views.gaya)().filter(Boolean));
}

function savePresetForm(p) {
  const id = h('input', { placeholder: 'id-preset-saya', pattern: '[a-z0-9-]{3,60}' });
  const name = h('input', { placeholder: 'Nama preset' });
  return h('div', { class: 'row wrap' }, id, name, h('button', { class: 'btn sm', onclick: async () => {
    try {
      const { saveNow } = await import('../store.js');
      await saveNow();
      const r = await api.savePreset({ id: id.value.trim(), name: name.value.trim(), projectId: p.id });
      toast(`Preset "${r.name}" disimpan di config/presets/${r.id}.json`, 'ok');
      store.status = await api.status();
    } catch (e) { toast(e.message, 'error', e.hint); }
  } }, 'Simpan preset'));
}

function musicControls(p) {
  const audioAssets = p.assets.filter((a) => a.kind === 'audio');
  const m = p.music;
  return h('div', {},
    audioAssets.length ? null : h('div', { class: 'alert warn small' }, 'Belum ada file musik. Tambahkan musik berlisensi di tab Aset — aplikasi tidak menyertakan musik.'),
    field('File musik', select(m.assetId || '', [['', '— Tidak ada —'], ...audioAssets.map((a) => [a.id, `${a.name} · ${a.license}`])], (v) => edit((x) => { x.music.assetId = v || null; if (!v) x.music.enabled = false; }, { rerender: false }))),
    h('label', { class: 'check' }, h('input', { type: 'checkbox', checked: !!m.enabled, disabled: !m.assetId, onchange: (e) => edit((x) => (x.music.enabled = e.target.checked), { rerender: false }) }), ' Aktifkan musik'),
    field('Volume musik', slider(m.volumeDb ?? -24, (v) => edit((x) => (x.music.volumeDb = v), { key: 'music.vol', rerender: false }), { min: -40, max: -6, step: 1, fmt: (v) => `${v} dB` })),
    chk('Ducking (musik turun saat bicara)', 'style.audio.ducking'),
    h('div', { class: 'grid3' },
      field('Mulai (dtk output)', num(m.startAt || 0, (v) => edit((x) => (x.music.startAt = Math.max(0, v)), { rerender: false }), { step: 0.5 })),
      field('Fade in', num(m.fadeIn ?? 1, (v) => edit((x) => (x.music.fadeIn = Math.max(0, v)), { rerender: false }), { step: 0.5 })),
      field('Fade out', num(m.fadeOut ?? 1.5, (v) => edit((x) => (x.music.fadeOut = Math.max(0, v)), { rerender: false }), { step: 0.5 })),
    ),
  );
}

function assetsPanel(p) {
  const license = h('input', { placeholder: 'mis. "Rekaman sendiri" / "Artlist lisensi #123"' });
  const progress = h('div', { class: 'progress hidden' }, h('div', { class: 'bar' }));
  const refresh = async () => setProject(await api.project(p.id), { keepHistory: true });
  const fileIn = h('input', { type: 'file', accept: [...store.status.accept.video, ...store.status.accept.image, ...store.status.accept.audio].join(','), onchange: async (e) => {
    const f = e.target.files[0];
    if (!f) return;
    if (!license.value.trim()) toast('Lisensi/asal aset belum diisi.', 'warn', 'Isi agar status hak pakai tercatat. Aset tetap ditambahkan.');
    progress.classList.remove('hidden');
    try {
      const { saveNow } = await import('../store.js');
      await saveNow();
      await api.uploadAsset(p.id, f, license.value.trim() || 'Belum diisi', (r) => (progress.firstChild.style.width = `${r * 100}%`));
      await refresh();
      toast('Aset ditambahkan.', 'ok');
    } catch (err) { toast(err.message, 'error', err.hint); } finally { progress.classList.add('hidden'); }
  } });
  const pathIn = h('input', { placeholder: '/path/ke/footage.mp4' });
  return [
    h('p', { class: 'muted small' }, 'Aset adalah footage, gambar, musik, atau SFX milik Anda. Tidak ada footage stok atau hasil generatif yang ditambahkan otomatis. Catat lisensi/asalnya.'),
    field('Asal / lisensi', license),
    h('div', { class: 'row wrap' }, fileIn),
    progress,
    h('div', { class: 'row' }, pathIn, h('button', { class: 'btn sm', onclick: async () => {
      try {
        await api.assetFromPath(p.id, pathIn.value, license.value.trim() || 'Belum diisi');
        await refresh();
      } catch (e) { toast(e.message, 'error', e.hint); }
    } }, 'Tambah dari path')),
    h('div', { class: 'asset-list' }, ...(p.assets.length ? p.assets.map((a) => h('div', { class: 'item' },
      h('div', { class: 'row wrap' }, badge(a.kind), h('strong', {}, a.name), a.missing ? badge('File hilang', 'error') : null, h('span', { class: 'muted small' }, a.meta?.duration ? `${a.meta.duration.toFixed(1)} dtk` : '', a.meta?.width ? ` · ${a.meta.width}×${a.meta.height}` : '')),
      h('div', { class: 'row' }, h('span', { class: 'muted small' }, 'Lisensi:'), h('input', { value: a.license, onchange: async (e) => { await api.updateAsset(p.id, a.id, { license: e.target.value }); a.license = e.target.value; } }),
        h('button', { class: 'link danger', onclick: async () => {
          const ok = await modal('Hapus aset?', h('p', {}, a.copied ? 'Salinan di folder proyek akan dihapus.' : 'Hanya referensi yang dihapus; file asli Anda tidak disentuh.'), [{ label: 'Hapus', kind: 'danger' }]);
          if (ok) { try { setProject(await api.deleteAsset(p.id, a.id), { keepHistory: true }); } catch (e) { toast(e.message, 'error', e.hint); } }
        } }, 'Hapus')),
    )) : [h('p', { class: 'muted' }, 'Belum ada aset.')])),
  ];
}

function itemInspector(p) {
  const s = store.selected;
  const list = s?.list;
  const i = list ? p[list].findIndex((x) => x.id === s.id) : -1;
  if (i < 0) return [h('p', { class: 'muted' }, 'Pilih item (kartu, b-roll, cut, SFX) di timeline untuk mengeditnya di sini.')];
  const it = p[list][i];
  const dur = p.source.meta.duration;
  const up = (k, key) => (v) => edit((x) => (x[list][i][k] = typeof v === 'number' ? r3(Math.max(0, Math.min(dur, v))) : v), { key: key ? `${it.id}.${k}` : null, rerender: false });
  const title = { cards: 'Kartu', broll: 'B-roll', cuts: 'Cut', sfx: 'Sound effect', zooms: 'Zoom punch-in' }[list];
  const out = [h('h3', {}, title), h('div', { class: 'row' }, h('button', { class: 'btn sm', onclick: () => preview.seek(it.start ?? it.time) }, '▶ Lompat ke item'))];
  if (list === 'sfx') out.push(field('Waktu (dtk sumber)', num(it.time, up('time'), { step: 0.05 })));
  else out.push(h('div', { class: 'grid2' }, field('Mulai (dtk sumber)', num(it.start, up('start'), { step: 0.05 })), field('Selesai', num(it.end, up('end'), { step: 0.05 }))));
  const flag = list === 'cuts' ? 'enabled' : 'approved';
  out.push(h('label', { class: 'check' }, h('input', { type: 'checkbox', checked: !!it[flag], onchange: (e) => edit((x) => { x[list][i][flag] = e.target.checked; x[list][i].approved = e.target.checked; }, { rerender: false }) }), list === 'cuts' ? ' Potong bagian ini' : ' Disetujui (masuk ke video)'));
  if (list === 'cards') {
    out.push(
      field('Tipe', select(it.type, CARD_TYPES, up('type'))),
      field('Tata letak', select(it.layout || 'full', [['full', 'Layar penuh'], ['panel', 'Panel bawah (wajah terlihat)']], up('layout'))),
      field('Ikon', select(LEGACY_ICON[it.icon] || (it.icon ?? 'auto'), ICON_OPTIONS, up('icon'))),
      field('Label atas', h('input', { value: it.kicker || '', onchange: (e) => up('kicker')(e.target.value) })),
      field(it.type === 'number' ? 'Angka' : 'Judul', h('input', { value: it.title || '', onchange: (e) => up('title')(e.target.value) })),
      field(it.type === 'list' ? 'Poin (pisahkan dengan ;)' : 'Label bawah', h('input', { value: it.subtitle || '', onchange: (e) => up('subtitle')(e.target.value) })),
    );
  }
  if (list === 'zooms') out.push(field('Zoom', slider(it.zoom, (v) => edit((x) => (x.zooms[i].zoom = v), { key: `${it.id}.zoom`, rerender: false }), { min: 1, max: 1.5, step: 0.01, fmt: (v) => `${v.toFixed(2)}×` })));
  if (list === 'sfx') out.push(field('Suara', h('div', { class: 'row' }, select(it.builtin ? `builtin:${it.builtin}` : `asset:${it.assetId}`, sfxOptions(p), (v) => edit((x) => {
    const [k, id] = v.split(':');
    x.sfx[i].builtin = k === 'builtin' ? id : null;
    x.sfx[i].assetId = k === 'asset' ? id : null;
  }, { rerender: false })), it.builtin ? previewButton('sfx', it.builtin) : null)));
  if (list === 'broll') out.push(field('Aset', select(it.assetId || '', [['', '— Belum ada aset —'], ...p.assets.filter((a) => a.kind !== 'audio').map((a) => [a.id, `${a.name} · ${a.license}`])], (v) => up('assetId')(v || null))));
  if (list === 'sfx') out.push(field('Volume tambahan (dB)', num(it.volumeDb || 0, (v) => edit((x) => (x.sfx[i].volumeDb = v), { rerender: false }), { step: 1 })));
  out.push(h('button', { class: 'link danger', onclick: () => { edit((x) => x[list].splice(i, 1)); store.selected = null; } }, 'Hapus item'));
  return out;
}
