// Langkah 5 — Ekspor: pemeriksaan, pilihan format/kualitas/lokasi, progres, riwayat.
import { h, toast, fmtBytes, fmtDate, field, select, badge } from '../ui.js';
import { api } from '../api.js';
import { store, saveNow } from '../store.js';
import { runJob, onJob, render } from '../app.js';
import { fmtTime } from '../../shared/core.js';

const opts = { quality: 'standar', container: 'mp4', outDir: '' };
let offJob = null;

export function renderExport(main) {
  const p = store.project;
  const S = store.status;
  if (!opts.aspect || opts.pid !== p.id) Object.assign(opts, { aspect: p.output.aspect, pid: p.id });
  main.append(h('div', { class: 'view-head' }, h('h1', {}, 'Ekspor'), h('p', { class: 'muted' }, 'Render dengan ffmpeg ke folder output terpisah. Status "Ekspor selesai" hanya muncul setelah file diverifikasi (ada, terbaca, durasi sesuai, dapat didekode).')));
  if (!p.source) return main.append(h('div', { class: 'panel' }, 'Impor video terlebih dahulu.'));

  const checks = h('div', {}, h('p', { class: 'muted' }, 'Memeriksa…'));
  const est = h('span', { class: 'muted' });
  const refreshChecks = async () => {
    await saveNow();
    try {
      const r = await api.preflight(p.id, { quality: opts.quality, aspect: opts.aspect });
      checks.replaceChildren(
        ...r.problems.map((x) => h('div', { class: 'alert error' }, x)),
        ...r.warnings.map((x) => h('div', { class: 'alert warn' }, x)),
        !r.problems.length && !r.warnings.length ? h('div', { class: 'alert ok' }, 'Siap diekspor.') : null,
      );
      if (r.estimate) est.textContent = `Durasi output ${fmtTime(r.estimate.durationSec)} · perkiraan ukuran ~${fmtBytes(r.estimate.approxBytes)} (perkiraan kasar, ukuran nyata ditampilkan setelah render)`;
      startBtn.disabled = !r.ok || !!store.jobs[p.id];
    } catch (e) {
      checks.replaceChildren(h('div', { class: 'alert error' }, e.message));
    }
  };

  const progress = h('div', {});
  const startBtn = h('button', { class: 'btn primary big', onclick: async () => {
    await saveNow();
    startBtn.disabled = true;
    const res = await runJob(api.render(p.id, { aspect: opts.aspect, quality: opts.quality, container: opts.container, outDir: opts.outDir.trim() || undefined }), { reloadFields: ['exports', 'status'] });
    if (res?.state === 'done') toast('Ekspor selesai dan terverifikasi.', 'ok', res.result.path);
    render();
  } }, 'Mulai ekspor');
  offJob?.();
  offJob = onJob((j) => {
    if (j.projectId !== p.id || j.type !== 'render') return;
    progress.replaceChildren(h('div', { class: 'row between' }, h('strong', {}, j.state === 'running' ? 'Sedang diekspor…' : j.state), h('button', { class: 'btn ghost sm', onclick: () => api.cancelJob(j.id) }, 'Batalkan')), h('div', { class: 'progress' }, h('div', { class: 'bar', style: { width: `${(j.progress || 0) * 100}%` } })), h('div', { class: 'muted small' }, `${Math.round((j.progress || 0) * 100)}% · ${j.message}`));
  });

  main.append(
    h('section', { class: 'panel' },
      h('h2', {}, 'Pemeriksaan'), checks,
      h('h2', {}, 'Pengaturan'),
      h('div', { class: 'grid3' },
        field('Rasio & ukuran', select(opts.aspect, Object.entries(S.formats).map(([k, f]) => [k, `${k} · ${f.width}×${f.height} — ${f.label}`]), (v) => { opts.aspect = v; refreshChecks(); })),
        field('Kualitas', select(opts.quality, Object.entries(S.qualities), (v) => { opts.quality = v; refreshChecks(); })),
        field('Format', select(opts.container, Object.entries(S.containers), (v) => (opts.container = v))),
      ),
      field('Folder output', h('input', { value: opts.outDir, placeholder: `Default: ${S.paths.output}/<nama-proyek>/`, oninput: (e) => (opts.outDir = e.target.value) }), 'Kosongkan untuk folder default. Folder kustom harus sudah ada dan tidak boleh sama dengan folder video sumber. File lama tidak pernah ditimpa.'),
      h('p', {}, est),
      h('div', { class: 'row' }, startBtn),
      progress,
    ),
    historyPanel(p),
  );
  refreshChecks();
}

function historyPanel(p) {
  const rows = (p.exports || []).map((e) => h('div', { class: 'item' },
    h('div', { class: 'row wrap' },
      e.state === 'done' ? badge(e.missing ? 'File sudah dipindah/dihapus' : 'Ekspor selesai', e.missing ? 'warn' : 'ok') : e.state === 'running' ? badge('Sedang diekspor', 'info') : e.state === 'canceled' ? badge('Dibatalkan', 'warn') : badge('Ekspor gagal', 'error'),
      h('span', {}, `${e.aspect} · ${e.quality} · ${e.container}`),
      h('span', { class: 'muted small' }, fmtDate(e.finishedAt || e.requestedAt)),
    ),
    e.state === 'done' ? h('div', {}, h('code', { class: 'path' }, e.path), h('div', { class: 'muted small' }, `${e.width}×${e.height} · ${fmtTime(e.duration)} · ${fmtBytes(e.size)}`),
      !e.missing ? h('div', { class: 'row' }, h('a', { class: 'btn sm', href: `/api/projects/${p.id}/exports/${e.id}/file`, target: '_blank' }, 'Putar'), h('a', { class: 'btn ghost sm', href: `/api/projects/${p.id}/exports/${e.id}/file?download=1` }, 'Unduh')) : null) : null,
    e.state === 'failed' ? h('div', { class: 'alert error small' }, e.error, e.hint ? h('div', { class: 'muted' }, e.hint) : null) : null,
  ));
  return h('section', { class: 'panel' }, h('h2', {}, 'Riwayat ekspor'), ...(rows.length ? rows : [h('p', { class: 'muted' }, 'Belum ada ekspor.')]));
}
