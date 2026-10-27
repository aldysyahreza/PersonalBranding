// Komponen pustaka audio bawaan (musik & SFX sintetis) dipakai di Rencana edit & Editor.
import { h, toast, badge } from './ui.js';
import { api } from './api.js';
import { store, setProject, saveNow } from './store.js';

const player = new Audio();
let playing = null;

/** Putar/hentikan contoh audio pustaka. */
export function previewButton(kind, id) {
  const key = `${kind}:${id}`;
  return h('button', {
    class: 'btn icon', title: 'Dengarkan',
    onclick: (e) => {
      if (playing === key && !player.paused) {
        player.pause();
        playing = null;
        e.currentTarget.textContent = '▶';
        return;
      }
      player.src = `/api/library/${kind}/${id}/file`;
      player.currentTime = 0;
      player.play().catch(() => toast('Audio tidak dapat diputar di browser.', 'warn'));
      playing = key;
      document.querySelectorAll('.lib-play-on').forEach((b) => { b.textContent = '▶'; b.classList.remove('lib-play-on'); });
      e.currentTarget.textContent = '■';
      e.currentTarget.classList.add('lib-play-on');
    },
  }, '▶');
}
player.addEventListener('ended', () => {
  playing = null;
  document.querySelectorAll('.lib-play-on').forEach((b) => { b.textContent = '▶'; b.classList.remove('lib-play-on'); });
});

export function sfxOptions(p) {
  return [
    ...store.status.library.sfx.map((s) => [`builtin:${s.id}`, `Bawaan: ${s.name} — ${s.desc}`]),
    ...p.assets.filter((a) => a.kind === 'audio' && !a.builtin).map((a) => [`asset:${a.id}`, `${a.name} · ${a.license}`]),
  ];
}

/** Daftar musik bawaan dengan tombol dengar & pakai. */
export function musicLibrary(p) {
  const lib = store.status.library;
  const current = p.assets.find((a) => a.id === p.music.assetId)?.builtin;
  const suggested = p.plan?.music?.builtin;
  return h('div', { class: 'lib' },
    h('div', { class: 'muted small' }, `Musik bawaan — ${lib.license}. Loop otomatis sepanjang video.`),
    ...lib.music.map((m) => h('div', { class: 'lib-row' },
      previewButton('music', m.id),
      h('div', { class: 'grow' }, h('strong', {}, m.name), ' ', h('span', { class: 'muted small' }, `${m.bpm} BPM`), suggested === m.id ? [' ', badge('Disarankan', 'info')] : null, h('div', { class: 'muted small' }, m.desc)),
      current === `music:${m.id}` && p.music.enabled
        ? badge('Dipakai', 'ok')
        : h('button', { class: 'btn sm', onclick: async () => {
          try {
            await saveNow();
            setProject(await api.useLibraryMusic(p.id, m.id), { keepHistory: true });
            toast(`Musik "${m.name}" dipakai. Atur volume bila perlu.`, 'ok');
          } catch (e) {
            toast(e.message, 'error', e.hint);
          }
        } }, 'Pakai'),
    )),
  );
}
