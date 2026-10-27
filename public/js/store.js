// State aplikasi + undo/redo + autosave.
import { api } from './api.js';
import { toast } from './ui.js';

export const EDITABLE = ['name', 'style', 'styleLevel', 'output', 'transcript', 'cuts', 'emphasisSuggestions', 'cards', 'broll', 'sfx', 'music', 'brandKeywords', 'plan'];

export const store = {
  status: null,
  projects: [],
  project: null,
  view: 'projects',
  playhead: 0,
  history: [],
  future: [],
  saveState: 'saved', // saved | pending | saving | error
  jobs: {},
  selected: null, // { kind, id } item timeline/editor yang dipilih
};

const listeners = new Set();
export const onChange = (fn) => (listeners.add(fn), () => listeners.delete(fn));
export const emit = (what) => listeners.forEach((fn) => fn(what));

function pick(p) {
  const o = {};
  for (const k of EDITABLE) o[k] = p[k];
  return o;
}
const snap = () => JSON.stringify(pick(store.project));

let saveTimer = null;
let lastKey = null;
let lastKeyAt = 0;

/**
 * Ubah proyek. Setiap perubahan bermakna dicatat di riwayat (undo).
 * opts.key: perubahan beruntun dengan key yang sama dalam 1,5 dtk digabung jadi satu langkah undo.
 * opts.rerender: false untuk input kontinu (slider) agar fokus tidak hilang.
 */
export function edit(fn, { key = null, rerender = true } = {}) {
  if (!store.project) return;
  const before = snap();
  fn(store.project);
  if (snap() === before) return;
  const now = Date.now();
  if (!(key && key === lastKey && now - lastKeyAt < 1500)) {
    store.history.push(before);
    if (store.history.length > 200) store.history.shift();
  }
  lastKey = key;
  lastKeyAt = now;
  store.future = [];
  scheduleSave();
  emit(rerender ? 'render' : 'preview');
}

function restore(json) {
  Object.assign(store.project, JSON.parse(json));
  scheduleSave(0);
  emit('render');
}

export function undo() {
  if (!store.history.length) return;
  store.future.push(snap());
  restore(store.history.pop());
  lastKey = null;
}

export function redo() {
  if (!store.future.length) return;
  store.history.push(snap());
  restore(store.future.pop());
  lastKey = null;
}

export function scheduleSave(delay = 700) {
  store.saveState = 'pending';
  emit('save');
  clearTimeout(saveTimer);
  saveTimer = setTimeout(saveNow, delay);
}

export async function saveNow() {
  clearTimeout(saveTimer);
  if (!store.project || store.saveState === 'saved') return;
  store.saveState = 'saving';
  emit('save');
  try {
    const fresh = await api.saveProject(store.project.id, pick(store.project));
    // Ambil field yang dikelola server (status, ekspor, aset) tanpa menimpa editan lokal terbaru.
    for (const k of ['status', 'exports', 'assets', 'source', 'analysis', 'lastPreview', 'updatedAt', 'jobs']) store.project[k] = fresh[k];
    store.saveState = 'saved';
  } catch (e) {
    store.saveState = 'error';
    toast('Gagal menyimpan perubahan.', 'error', e.hint || e.message);
  }
  emit('save');
}

/** Ganti proyek dari respons server (mis. setelah impor/analisis). Riwayat undo direset. */
export function setProject(p, { keepHistory = false } = {}) {
  store.project = p;
  if (!keepHistory) {
    store.history = [];
    store.future = [];
  }
  store.saveState = 'saved';
  emit('render');
}

/** Gabungkan field server ke proyek lokal tanpa membuang editan yang belum tersimpan. */
export function mergeServer(p, fields) {
  if (!store.project || store.project.id !== p.id) return setProject(p);
  for (const k of fields) store.project[k] = p[k];
  emit('render');
}
