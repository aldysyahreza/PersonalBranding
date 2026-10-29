// Memperbarui proyek lama (gaya video referensi) ke preset bible "The Brand Fixer" dalam satu klik:
// terapkan gaya baru, lalu buat ulang rencana otomatis. Bisa dibatalkan dengan Urungkan.
import { h, toast, modal } from './ui.js';
import { api } from './api.js';
import { store, setProject } from './store.js';

export const MAIN_PRESET = 'brand-fixer';

export function upgradeBanner(p, onDone) {
  if (!p || p.presetId === MAIN_PRESET || !store.status.presets.some((x) => x.id === MAIN_PRESET)) return null;
  return h('div', { class: 'alert warn row between wrap' },
    h('span', {}, h('strong', {}, 'Proyek ini masih memakai gaya lama (video referensi: kotak merah, Montserrat). '), 'Gaya baru "The Brand Fixer" dari bible Anda belum diterapkan di proyek ini.'),
    h('button', { class: 'btn primary', onclick: () => upgradeProject(p, onDone) }, 'Pakai gaya The Brand Fixer'));
}

export async function upgradeProject(p, onDone) {
  const ok = await modal('Pakai gaya The Brand Fixer?', h('div', {},
    h('p', {}, 'Gaya proyek diganti ke preset bible (font, warna, caption, kartu), lalu rencana dibuat ulang otomatis: hook, kartu, penekanan, zoom & SFX yang teksnya terverifikasi dari ucapan langsung disetujui.'),
    h('p', { class: 'muted small' }, 'Kartu/saran lama buatan aturan diganti. Item yang Anda buat sendiri tetap ada. Transkrip, cut, dan video sumber tidak disentuh. Bisa dibatalkan dengan Urungkan.')),
  [{ label: 'Terapkan', kind: 'primary' }]);
  if (!ok) return;
  try {
    const { saveNow } = await import('./store.js');
    await saveNow();
    await api.applyPreset(p.id, MAIN_PRESET, p.styleLevel || 'editorial');
    const fresh = p.transcript?.segments?.length ? await api.plan(p.id, 'rules', false, true, true) : await api.project(p.id);
    setProject(fresh, { keepHistory: true });
    toast('Gaya The Brand Fixer diterapkan dan rencana dibuat ulang otomatis.', 'ok');
    onDone?.();
  } catch (e) {
    toast(e.message, 'error', e.hint);
  }
}
