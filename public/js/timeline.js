// Timeline sederhana: trek cut, subtitle, kartu, b-roll, SFX, struktur.
// Klik area kosong = pindah posisi; seret item = geser; seret tepi = ubah durasi.
import { h } from './ui.js';
import { store, edit } from './store.js';
import { buildPhrases, r3, fmtTime } from '../shared/core.js';

const TRACKS = [
  ['structure', 'Struktur'],
  ['cuts', 'Cut'],
  ['captions', 'Subtitle'],
  ['cards', 'Kartu'],
  ['broll', 'B-roll'],
  ['sfx', 'SFX'],
];

export function createTimeline({ onSeek, onSelect }) {
  let pps = 40; // piksel per detik
  const scroller = h('div', { class: 'tl-scroll' });
  const zoom = h('input', { type: 'range', min: 10, max: 200, value: pps, oninput: (e) => { pps = Number(e.target.value); draw(); } });
  const el = h('div', { class: 'timeline' }, h('div', { class: 'tl-head' }, h('strong', {}, 'Timeline'), h('span', { class: 'muted small' }, 'Klik untuk pindah posisi · seret item untuk menggeser · seret tepi untuk mengubah durasi'), h('label', { class: 'small' }, 'Zoom ', zoom)), h('div', { class: 'tl-body' }, h('div', { class: 'tl-labels' }, ...TRACKS.map(([, l]) => h('div', { class: 'tl-label' }, l))), scroller));
  let playheadEl;

  function items(track, p) {
    switch (track) {
      case 'structure': return (p.plan?.structure || []).map((s, i) => ({ id: `st${i}`, start: s.start, end: s.end, label: s.part, cls: 'st', readonly: true }));
      case 'cuts': return (p.cuts || []).map((c) => ({ id: c.id, start: c.start, end: c.end, label: c.kind || 'cut', cls: c.enabled ? 'cut on' : 'cut', list: 'cuts' }));
      case 'captions': return buildPhrases(p.transcript?.segments || [], { maxWords: p.style.captions.maxWords, maxChars: p.style.captions.maxChars }).map((ph, i) => ({ id: `ph${i}`, start: ph.start, end: ph.end, label: ph.words.map((w) => w.text).join(' '), cls: 'cap', readonly: true }));
      case 'cards': return (p.cards || []).map((c) => ({ id: c.id, start: c.start, end: c.end, label: c.title || c.type, cls: c.approved ? 'card on' : 'card', list: 'cards' }));
      case 'broll': return (p.broll || []).map((b) => ({ id: b.id, start: b.start, end: b.end, label: b.assetId ? (p.assets.find((a) => a.id === b.assetId)?.name || 'aset') : 'tanpa aset', cls: b.approved ? (b.assetId ? 'broll on' : 'broll warn') : 'broll', list: 'broll' }));
      case 'sfx': return (p.sfx || []).map((s) => ({ id: s.id, start: s.time, end: s.time + 0.25, label: s.builtin || 'sfx', cls: s.approved ? 'sfx on' : 'sfx', list: 'sfx', point: true }));
      default: return [];
    }
  }

  function startDrag(e, it, mode) {
    e.stopPropagation();
    e.preventDefault();
    const p = store.project;
    const dur = p.source.meta.duration;
    const x0 = e.clientX;
    const node = e.currentTarget.closest('.tl-item');
    let moved = false;
    const move = (ev) => {
      const d = (ev.clientX - x0) / pps;
      if (Math.abs(ev.clientX - x0) > 2) moved = true;
      let s = it.start, en = it.end;
      if (mode === 'move') { s = Math.max(0, Math.min(dur - (it.end - it.start), it.start + d)); en = s + (it.end - it.start); }
      if (mode === 'l') s = Math.max(0, Math.min(it.end - 0.1, it.start + d));
      if (mode === 'r') en = Math.min(dur, Math.max(it.start + 0.1, it.end + d));
      node.style.left = `${s * pps}px`;
      node.style.width = `${Math.max(4, (en - s) * pps)}px`;
      node.dataset.s = s;
      node.dataset.e = en;
    };
    const up = () => {
      window.removeEventListener('pointermove', move);
      window.removeEventListener('pointerup', up);
      if (!moved) return onSelect?.({ list: it.list, id: it.id });
      const s = r3(Number(node.dataset.s)), en = r3(Number(node.dataset.e));
      edit((x) => {
        const target = x[it.list].find((y) => y.id === it.id);
        if (it.list === 'sfx') target.time = s;
        else Object.assign(target, { start: s, end: en });
      });
    };
    window.addEventListener('pointermove', move);
    window.addEventListener('pointerup', up);
  }

  function draw() {
    const p = store.project;
    if (!p?.source) return;
    const dur = p.source.meta.duration;
    const width = Math.max(600, dur * pps);
    const ruler = h('div', { class: 'tl-ruler', style: { width: `${width}px` } });
    const step = pps > 80 ? 1 : pps > 30 ? 2 : 5;
    for (let t = 0; t <= dur; t += step) ruler.append(h('span', { style: { left: `${t * pps}px` } }, fmtTime(t)));
    const rows = TRACKS.map(([key]) => {
      const row = h('div', { class: 'tl-row', style: { width: `${width}px` } });
      for (const it of items(key, p)) {
        const sel = store.selected?.id === it.id;
        const node = h('div', { class: `tl-item ${it.cls} ${sel ? 'sel' : ''} ${it.point ? 'point' : ''}`, title: `${it.label} (${fmtTime(it.start)}–${fmtTime(it.end)})`, style: { left: `${it.start * pps}px`, width: `${Math.max(4, (it.end - it.start) * pps)}px` } }, h('span', {}, it.label));
        if (!it.readonly) {
          node.addEventListener('pointerdown', (e) => startDrag(e, it, 'move'));
          if (!it.point) {
            const l = h('i', { class: 'tl-h l' }), r = h('i', { class: 'tl-h r' });
            l.addEventListener('pointerdown', (e) => startDrag(e, it, 'l'));
            r.addEventListener('pointerdown', (e) => startDrag(e, it, 'r'));
            node.append(l, r);
          }
        } else node.addEventListener('click', (e) => { e.stopPropagation(); onSeek(it.start); });
        row.append(node);
      }
      return row;
    });
    playheadEl = h('div', { class: 'tl-playhead' });
    const inner = h('div', { class: 'tl-inner', style: { width: `${width}px` }, onclick: (e) => {
      const r = inner.getBoundingClientRect();
      onSeek((e.clientX - r.left) / pps);
    } }, ruler, ...rows, playheadEl);
    scroller.replaceChildren(inner);
    setTime(store.playhead || 0);
  }

  function setTime(t) {
    if (!playheadEl) return;
    playheadEl.style.left = `${t * pps}px`;
    const x = t * pps;
    if (x < scroller.scrollLeft || x > scroller.scrollLeft + scroller.clientWidth - 40) scroller.scrollLeft = Math.max(0, x - 80);
  }

  return { el, draw, setTime };
}
