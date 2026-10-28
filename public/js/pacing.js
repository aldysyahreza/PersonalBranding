// Tombol "Rapikan ritme": menerapkan aturan jeda wajah/durasi kartu/zoom ke proyek (bisa di-undo).
import { h, toast } from './ui.js';
import { store, edit } from './store.js';
import { enforcePacing } from '../shared/core.js';

export function pacingIssues(p) {
  return enforcePacing({ cards: p.cards, zooms: p.zooms, duration: p.source?.meta?.duration, pacing: p.style?.pacing }).changes;
}

export function pacingButton() {
  const p = store.project;
  const issues = pacingIssues(p);
  return h('button', {
    class: `btn ${issues.length ? 'primary' : 'ghost'} sm`,
    title: issues.length ? issues.join('\n') : 'Ritme sudah sesuai aturan',
    onclick: () => {
      const r = enforcePacing({ cards: store.project.cards, zooms: store.project.zooms, duration: store.project.source?.meta?.duration, pacing: store.project.style?.pacing });
      if (!r.changes.length) return toast('Ritme sudah sesuai: jeda wajah, durasi kartu, dan zoom aman.', 'ok');
      edit((x) => {
        x.cards = r.cards;
        x.zooms = r.zooms;
      });
      toast(`Ritme dirapikan (${r.changes.length} perubahan, bisa di-Urungkan).`, 'ok', r.changes.slice(0, 4).join(' · ') + (r.changes.length > 4 ? ' …' : ''));
    },
  }, issues.length ? `Rapikan ritme (${issues.length})` : 'Ritme OK');
}
