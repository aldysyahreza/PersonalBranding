// Langkah 1 — Proyek: buat/buka proyek, impor video sumber, analisis.
import { h, toast, modal, fmtBytes, fmtDate, field, select, badge } from '../ui.js';
import { api } from '../api.js';
import { store, setProject, edit } from '../store.js';
import { go, runJob, render } from '../app.js';
import { fmtTime, OUTPUT_FORMATS } from '../../shared/core.js';

export function renderProjects(main) {
  main.append(h('div', { class: 'view-head' }, h('h1', {}, 'Proyek'), h('p', { class: 'muted' }, 'Satu proyek = satu video raw. File sumber tidak pernah diubah, dipindahkan, atau ditimpa.')));
  if (store.project) main.append(projectPanel(store.project));
  main.append(listPanel());
}

function listPanel() {
  const panel = h('section', { class: 'panel' }, h('h2', {}, store.project ? 'Proyek lain' : 'Proyek Anda'));
  const name = h('input', { type: 'text', placeholder: 'mis. "Kenapa konten tidak menghasilkan klien"', maxlength: 120 });
  const presets = store.status.presets.map((p) => [p.id, p.name]);
  let presetId = presets[0]?.[0];
  let level = 'editorial';
  panel.append(
    h(
      'form',
      {
        class: 'row wrap create',
        onsubmit: async (e) => {
          e.preventDefault();
          try {
            const p = await api.createProject({ name: name.value.trim() || 'Proyek tanpa nama', presetId, level });
            setProject(p);
            go('projects');
          } catch (err) {
            toast(err.message, 'error', err.hint);
          }
        },
      },
      field('Nama proyek', name),
      field('Preset gaya', select(presetId, presets, (v) => (presetId = v))),
      field('Level gaya', select(level, store.status.styleLevels.map((l) => [l, l[0].toUpperCase() + l.slice(1)]), (v) => (level = v))),
      h('button', { class: 'btn primary', type: 'submit' }, '+ Buat proyek'),
    ),
  );
  const list = h('div', { class: 'cards-list' }, h('p', { class: 'muted' }, 'Memuat…'));
  panel.append(list);
  api.projects().then((items) => {
    store.projects = items;
    list.replaceChildren(
      ...(items.length
        ? items.map((p) =>
            h(
              'div',
              { class: `proj-card ${store.project?.id === p.id ? 'current' : ''}` },
              h('div', {}, h('strong', {}, p.name), h('div', { class: 'muted small' }, p.source ? `${p.source.name} · ${fmtTime(p.source.duration)} · ${p.source.width}×${p.source.height} (${p.source.aspect})` : 'Belum ada video'), h('div', { class: 'muted small' }, `Diubah ${fmtDate(p.updatedAt)}`)),
              h('span', { class: `status s-${p.status.code}` }, p.status.label),
              h('div', { class: 'row' },
                h('button', { class: 'btn sm', onclick: async () => { setProject(await api.project(p.id)); go(p.source ? 'transcript' : 'projects'); } }, 'Buka'),
                h('button', {
                  class: 'btn ghost sm danger',
                  onclick: async () => {
                    const ok = await modal('Hapus proyek?', h('p', {}, `Folder proyek "${p.name}" (transkrip, pengaturan, salinan unggahan) akan dihapus. File video asli yang direferensikan lewat path lokal dan file di folder output TIDAK dihapus.`), [{ label: 'Hapus proyek', kind: 'danger' }]);
                    if (!ok) return;
                    try {
                      await api.deleteProject(p.id);
                      if (store.project?.id === p.id) setProject(null);
                      render();
                    } catch (e) {
                      toast(e.message, 'error', e.hint);
                    }
                  },
                }, 'Hapus'),
              ),
            ),
          )
        : [h('p', { class: 'muted' }, 'Belum ada proyek. Buat proyek pertama di atas.')]),
    );
  });
  return panel;
}

function projectPanel(p) {
  const panel = h('section', { class: 'panel' });
  panel.append(h('div', { class: 'row between' }, h('h2', {}, p.name), h('input', { type: 'text', value: p.name, class: 'inline-name', title: 'Ganti nama proyek', onchange: (e) => edit((x) => (x.name = e.target.value.trim() || x.name)) })));

  // --- Impor ---
  const acc = store.status.accept.video.join(',');
  const progress = h('div', { class: 'progress hidden' }, h('div', { class: 'bar' }));
  const fileInput = h('input', {
    type: 'file', accept: acc,
    onchange: async (e) => {
      const f = e.target.files[0];
      if (!f) return;
      if (f.size > store.status.limits.maxUploadMB * 1048576) return toast('File terlalu besar untuk diunggah lewat browser.', 'error', `Batas ${store.status.limits.maxUploadMB} MB. Gunakan opsi path lokal (tanpa menyalin).`);
      progress.classList.remove('hidden');
      try {
        const res = await api.uploadSource(p.id, f, (r) => (progress.firstChild.style.width = `${r * 100}%`));
        setProject(res);
        toast('Video berhasil diimpor (disalin ke folder proyek).', 'ok');
      } catch (err) {
        toast(err.message, 'error', err.hint);
      } finally {
        progress.classList.add('hidden');
      }
    },
  });
  const pathInput = h('input', { type: 'text', placeholder: '/Users/aldy/Videos/raw-001.mp4' });
  panel.append(
    h('h3', {}, p.source ? 'Ganti video sumber' : 'Impor video raw'),
    h('div', { class: 'grid2' },
      h('div', { class: 'import-box' }, h('strong', {}, 'Pilih file'), h('p', { class: 'muted small' }, `File disalin ke folder proyek; aslinya tidak diubah. Format: ${store.status.accept.video.join(' ')} · maks ${store.status.limits.maxUploadMB} MB.`), fileInput, progress),
      h('div', { class: 'import-box' }, h('strong', {}, 'Gunakan path lokal (tanpa menyalin)'), h('p', { class: 'muted small' }, 'Cocok untuk file besar. File hanya dibaca, tidak pernah ditulis. Jangan pindahkan file selama proyek dipakai.'),
        h('div', { class: 'row' }, pathInput, h('button', { class: 'btn', onclick: async () => {
          try {
            setProject(await api.sourceFromPath(p.id, pathInput.value));
            toast('Video terhubung.', 'ok');
          } catch (e) {
            toast(e.message, 'error', e.hint);
          }
        } }, 'Hubungkan'))),
    ),
  );

  if (!p.source) return panel;
  const m = p.source.meta;
  const aspect = (w, hh) => { const r = w / hh; return Math.abs(r - 9 / 16) < 0.02 ? '9:16' : Math.abs(r - 16 / 9) < 0.02 ? '16:9' : Math.abs(r - 1) < 0.02 ? '1:1' : Math.abs(r - 0.8) < 0.02 ? '4:5' : `${r.toFixed(2)}:1`; };
  panel.append(
    h('h3', {}, 'Informasi video'),
    p.source.missing ? h('div', { class: 'alert error' }, `File sumber tidak ditemukan di ${p.source.path}. Kembalikan file ke lokasi tersebut atau impor ulang.`) : null,
    p.source.changed ? h('div', { class: 'alert warn' }, 'Ukuran file sumber berbeda dari saat diimpor. Jika video sudah diganti, jalankan analisis ulang dan periksa sinkron subtitle.') : null,
    h('table', { class: 'info' },
      ...[
        ['Nama file', p.source.originalName],
        ['Lokasi', h('code', {}, p.source.path), p.source.copied ? ' (salinan di folder proyek)' : ' (referensi, hanya dibaca)'],
        ['Durasi', fmtTime(m.duration)],
        ['Resolusi', `${m.width} × ${m.height}${m.rotation ? ` (rotasi ${m.rotation}°)` : ''}`],
        ['Rasio aspek', aspect(m.width, m.height)],
        ['Frame rate', `${m.fps} fps`],
        ['Codec', `${m.videoCodec || '-'} / ${m.hasAudio ? m.audioCodec : 'tanpa audio'}`],
        ['Ukuran', fmtBytes(p.source.size)],
        ['Status', h('span', { class: `status s-${p.status.code}` }, p.status.label)],
      ].map(([k, ...v]) => h('tr', {}, h('th', {}, k), h('td', {}, ...v))),
    ),
  );

  panel.append(
    h('h3', {}, 'Rasio output'),
    h('div', { class: 'row wrap' },
      ...Object.entries(OUTPUT_FORMATS).map(([k, f]) => h('button', { class: `chip ${p.output.aspect === k ? 'on' : ''}`, onclick: () => edit((x) => (x.output.aspect = k)) }, `${k} — ${f.label.split('(')[0].trim()} ${f.width}×${f.height}`)),
    ),
    h('p', { class: 'muted small' }, 'Default 9:16. Posisi crop (reframe) diatur di Editor → Bingkai.'),
  );

  // --- Analisis ---
  const a = p.analysis;
  const job = store.jobs[p.id];
  panel.append(
    h('h3', {}, 'Analisis video'),
    h('p', { class: 'muted small' }, 'Lokal di komputer ini: membaca metadata, level audio, dan mendeteksi bagian hening (kandidat cut). Tidak ada data yang dikirim ke luar.'),
    h('div', { class: 'row' },
      h('button', { class: 'btn primary', disabled: Boolean(job) || p.source.missing, onclick: () => runJob(api.analyze(p.id), { okMsg: 'Analisis selesai.' }) }, a ? 'Analisis ulang' : 'Analisis video'),
      a ? badge(`Dianalisis ${fmtDate(a.at)}`, 'ok') : badge('Belum dianalisis', 'warn'),
    ),
  );
  if (a) {
    const totalSil = a.silences.reduce((s, x) => s + x.end - x.start, 0);
    panel.append(
      h('ul', { class: 'facts' },
        h('li', {}, `Level audio: rata-rata ${a.levels?.meanDb ?? '-'} dB, puncak ${a.levels?.maxDb ?? '-'} dB`),
        h('li', {}, `${a.silences.length} bagian hening (total ${totalSil.toFixed(1)} dtk) — ambang −35 dB, min 0,45 dtk`),
        h('li', {}, `${a.speech.length} rentang ucapan terdeteksi`),
      ),
      ...a.warnings.map((w) => h('div', { class: 'alert warn' }, w)),
      a.silences.length === 0 && m.hasAudio ? h('p', { class: 'muted small' }, 'Tidak ada jeda hening terdeteksi. Jika video memiliki musik latar bawaan, jeda tidak dapat dibedakan dari musik.') : null,
      h('div', { class: 'row' }, h('button', { class: 'btn primary', onclick: () => go('transcript') }, 'Lanjut ke Transkrip →')),
    );
  }
  return panel;
}
