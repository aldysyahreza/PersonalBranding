// Kerangka aplikasi: navigasi langkah, header status, undo/redo, job.
import { h, toast } from './ui.js';
import { api, watchJob } from './api.js';
import { store, onChange, undo, redo, saveNow, setProject, mergeServer } from './store.js';
import { projectStatus } from '../shared/core.js';
import { renderProjects } from './views/projects.js';
import { renderTranscript } from './views/transcript.js';
import { renderPlan } from './views/plan.js';
import { renderEditor, refreshPreview, destroyEditor } from './views/editor.js';
import { renderExport } from './views/export.js';
import { renderBrand } from './views/brand.js';

const STEPS = [
  ['projects', '1', 'Proyek', 'Buat/buka proyek, impor video'],
  ['transcript', '2', 'Transkrip', 'Koreksi teks & timestamp'],
  ['plan', '3', 'Rencana edit', 'Tinjau saran & setujui'],
  ['editor', '4', 'Editor', 'Preview & atur gaya'],
  ['export', '5', 'Ekspor', 'Render & unduh'],
];

const root = document.getElementById('app');

export function go(view) {
  if (view !== 'projects' && view !== 'brand' && !store.project) {
    toast('Buka atau buat proyek terlebih dahulu.', 'warn');
    view = 'projects';
  }
  store.view = view;
  location.hash = store.project ? `${view}/${store.project.id}` : view;
  render();
}

/** Jalankan job server dan pantau progresnya; muat ulang proyek setelah selesai. */
export async function runJob(startPromise, { okMsg, reloadFields } = {}) {
  let job;
  try {
    job = await startPromise;
  } catch (e) {
    toast(e.message, 'error', e.hint);
    return null;
  }
  const pid = job.projectId;
  store.jobs[pid] = job;
  renderHeader();
  const final = await watchJob(job, (j) => {
    store.jobs[pid] = j;
    renderHeader();
    emitJob(j);
  });
  delete store.jobs[pid];
  if (final.state === 'done') {
    if (okMsg) toast(okMsg, 'ok');
  } else if (final.state === 'canceled') toast('Proses dibatalkan.', 'warn');
  else toast(final.error?.message || 'Proses gagal.', 'error', final.error?.hint);
  if (store.project?.id === pid) {
    const fresh = await api.project(pid).catch(() => null);
    if (fresh) reloadFields ? mergeServer(fresh, reloadFields) : setProject(fresh, { keepHistory: true });
  }
  renderHeader();
  return final;
}

const jobListeners = new Set();
export const onJob = (fn) => (jobListeners.add(fn), () => jobListeners.delete(fn));
const emitJob = (j) => jobListeners.forEach((f) => f(j));

function renderHeader() {
  const el = document.getElementById('header');
  if (!el) return;
  const p = store.project;
  const job = p && store.jobs[p.id];
  const st = p ? projectStatus(p, job ? [job] : []) : null;
  const saveLabel = { saved: 'Tersimpan', pending: 'Menyimpan…', saving: 'Menyimpan…', error: 'Gagal menyimpan' }[store.saveState];
  el.replaceChildren(
    h('div', { class: 'brand' }, h('span', { class: 'logo' }, '▶'), h('div', {}, h('strong', {}, 'Personal Branding Video Studio'), h('div', { class: 'sub' }, 'Raw talking head → video siap tinjau'))),
    p
      ? h(
          'div',
          { class: 'proj' },
          h('span', { class: 'proj-name', title: p.name }, p.name),
          h('span', { class: `status s-${st.code}` }, st.label),
          job ? h('span', { class: 'jobpill' }, `${job.label}: ${Math.round((job.progress || 0) * 100)}%`, h('button', { class: 'link', onclick: () => api.cancelJob(job.id) }, 'Batalkan')) : null,
        )
      : h('div'),
    p
      ? h(
          'div',
          { class: 'tools' },
          h('button', { class: 'btn ghost sm', title: 'Urungkan (Ctrl+Z)', disabled: !store.history.length, onclick: undo }, '↶ Urungkan'),
          h('button', { class: 'btn ghost sm', title: 'Ulangi (Ctrl+Shift+Z)', disabled: !store.future.length, onclick: redo }, '↷ Ulangi'),
          h('span', { class: `save s-${store.saveState}` }, saveLabel),
        )
      : h('div'),
  );
}

function renderNav() {
  const el = document.getElementById('nav');
  el.replaceChildren(
    ...STEPS.map(([id, n, label, sub]) =>
      h('button', { class: `step ${store.view === id ? 'active' : ''}`, disabled: id !== 'projects' && !store.project, onclick: () => go(id) }, h('span', { class: 'n' }, n), h('span', {}, h('strong', {}, label), h('small', {}, sub))),
    ),
    h('div', { class: 'nav-sep' }),
    h('button', { class: `step ${store.view === 'brand' ? 'active' : ''}`, onclick: () => go('brand') }, h('span', { class: 'n' }, 'i'), h('span', {}, h('strong', {}, 'Profil brand & sistem'), h('small', {}, 'Fakta, asumsi, status layanan'))),
  );
}

export function render() {
  renderHeader();
  renderNav();
  const main = document.getElementById('main');
  destroyEditor();
  main.replaceChildren();
  const views = { projects: renderProjects, transcript: renderTranscript, plan: renderPlan, editor: renderEditor, export: renderExport, brand: renderBrand };
  (views[store.view] || renderProjects)(main);
}

onChange((what) => {
  if (what === 'save') return renderHeader();
  if (what === 'preview') {
    renderHeader();
    return refreshPreview();
  }
  render();
});

document.addEventListener('keydown', (e) => {
  const tag = e.target.tagName;
  if (['INPUT', 'TEXTAREA', 'SELECT'].includes(tag) || e.target.isContentEditable) return;
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'z') {
    e.preventDefault();
    e.shiftKey ? redo() : undo();
  }
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'y') {
    e.preventDefault();
    redo();
  }
});
window.addEventListener('beforeunload', (e) => {
  if (store.saveState !== 'saved') {
    saveNow();
    e.preventDefault();
  }
});

async function boot() {
  root.replaceChildren(h('header', { id: 'header' }), h('div', { class: 'body' }, h('nav', { id: 'nav' }), h('main', { id: 'main' })), h('div', { id: 'toasts' }));
  try {
    store.status = await api.status();
  } catch (e) {
    document.getElementById('main').replaceChildren(h('div', { class: 'panel error' }, h('h2', {}, 'Server tidak dapat dihubungi'), h('p', {}, e.hint || e.message)));
    return;
  }
  const [view, id] = location.hash.slice(1).split('/');
  if (id) {
    try {
      setProject(await api.project(id));
    } catch {}
  }
  store.view = view && (store.project || ['projects', 'brand'].includes(view)) ? view : 'projects';
  render();
  if (!store.status.ffmpeg) toast('ffmpeg tidak ditemukan.', 'error', 'Analisis dan ekspor tidak dapat berjalan. Pasang ffmpeg lalu jalankan ulang aplikasi.');
}

boot();
