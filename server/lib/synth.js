// Pustaka audio bawaan: musik latar & SFX yang DISINTESIS dari nol oleh aplikasi
// (osilator, noise, filter, envelope). Tidak memakai sampel/rekaman pihak lain,
// sehingga bebas royalti. Hasil ditulis sebagai WAV ke folder library/ (cache).
import fs from 'node:fs';
import path from 'node:path';
import { ROOT } from './config.js';

const SR = 44100;
const TAU = Math.PI * 2;
const LIB_VERSION = 2;
export const LIBRARY_DIR = path.join(ROOT, 'library');
export const LICENSE_NOTE = 'Disintesis oleh aplikasi ini — bebas royalti, boleh dipakai komersial';

/* ------------------------------ util DSP ------------------------------ */

const midiHz = (m) => 440 * Math.pow(2, (m - 69) / 12);

/** PRNG deterministik agar file yang sama selalu identik. */
function rng(seed) {
  let s = seed >>> 0;
  return () => {
    s = (s * 1664525 + 1013904223) >>> 0;
    return s / 4294967296;
  };
}

/** Biquad (RBJ). Koefisien bisa diperbarui per sampel untuk sweep. */
class Biquad {
  constructor() {
    this.x1 = this.x2 = this.y1 = this.y2 = 0;
  }
  set(type, freq, q = 0.707) {
    const w = (TAU * Math.min(freq, SR * 0.45)) / SR;
    const cos = Math.cos(w), alpha = Math.sin(w) / (2 * q);
    let b0, b1, b2;
    if (type === 'lp') [b0, b1, b2] = [(1 - cos) / 2, 1 - cos, (1 - cos) / 2];
    else if (type === 'hp') [b0, b1, b2] = [(1 + cos) / 2, -(1 + cos), (1 + cos) / 2];
    else [b0, b1, b2] = [alpha, 0, -alpha]; // bandpass
    const a0 = 1 + alpha;
    this.b0 = b0 / a0; this.b1 = b1 / a0; this.b2 = b2 / a0;
    this.a1 = (-2 * cos) / a0; this.a2 = (1 - alpha) / a0;
    return this;
  }
  run(x) {
    const y = this.b0 * x + this.b1 * this.x1 + this.b2 * this.x2 - this.a1 * this.y1 - this.a2 * this.y2;
    this.x2 = this.x1; this.x1 = x; this.y2 = this.y1; this.y1 = y;
    return y;
  }
}

class Buffer2 {
  constructor(seconds, { loop = false } = {}) {
    this.n = Math.ceil(seconds * SR);
    this.L = new Float32Array(this.n);
    this.R = new Float32Array(this.n);
    this.loop = loop;
  }
  /** Tambah sampel; pada mode loop, ekor yang melewati akhir dibungkus ke awal (loop mulus). */
  add(i, v, pan = 0) {
    if (i < 0) return;
    if (i >= this.n) {
      if (!this.loop) return;
      i %= this.n;
    }
    this.L[i] += v * Math.min(1, 1 - pan);
    this.R[i] += v * Math.min(1, 1 + pan);
  }
  normalize(peakDb = -3) {
    let peak = 1e-9;
    for (let i = 0; i < this.n; i++) peak = Math.max(peak, Math.abs(this.L[i]), Math.abs(this.R[i]));
    const g = Math.pow(10, peakDb / 20) / peak;
    for (let i = 0; i < this.n; i++) {
      this.L[i] *= g;
      this.R[i] *= g;
    }
    return this;
  }
  /** Fade pendek di awal/akhir (hanya untuk SFX) agar tidak ada klik. */
  edges(ms = 3) {
    const k = Math.round((ms / 1000) * SR);
    for (let i = 0; i < k; i++) {
      const g = i / k;
      this.L[i] *= g; this.R[i] *= g;
      this.L[this.n - 1 - i] *= g; this.R[this.n - 1 - i] *= g;
    }
    return this;
  }
  toWav() {
    const data = Buffer.alloc(this.n * 4);
    for (let i = 0; i < this.n; i++) {
      data.writeInt16LE(Math.round(Math.max(-1, Math.min(1, this.L[i])) * 32767), i * 4);
      data.writeInt16LE(Math.round(Math.max(-1, Math.min(1, this.R[i])) * 32767), i * 4 + 2);
    }
    const h = Buffer.alloc(44);
    h.write('RIFF', 0); h.writeUInt32LE(36 + data.length, 4); h.write('WAVE', 8);
    h.write('fmt ', 12); h.writeUInt32LE(16, 16); h.writeUInt16LE(1, 20); h.writeUInt16LE(2, 22);
    h.writeUInt32LE(SR, 24); h.writeUInt32LE(SR * 4, 28); h.writeUInt16LE(4, 32); h.writeUInt16LE(16, 34);
    h.write('data', 36); h.writeUInt32LE(data.length, 40);
    return Buffer.concat([h, data]);
  }
}

/* ------------------------------ instrumen ------------------------------ */

/** Pad hangat: beberapa sinus sedikit didetune + attack/release lembut. */
function pad(buf, t0, dur, notes, amp, pan = 0) {
  const a = 0.6, r = 1.2;
  const total = dur + r;
  const start = Math.round(t0 * SR);
  const lp = new Biquad().set('lp', 1800, 0.6);
  for (let i = 0; i < total * SR; i++) {
    const t = i / SR;
    const env = t < a ? t / a : t < dur ? 1 : Math.max(0, 1 - (t - dur) / r);
    let v = 0;
    for (const m of notes) {
      const f = midiHz(m);
      v += Math.sin(TAU * f * 0.998 * t) + Math.sin(TAU * f * 1.002 * t) + 0.25 * Math.sin(TAU * f * 2 * t);
    }
    v = (v / (notes.length * 2.25)) * env * amp;
    const y = lp.run(v);
    // Lebar stereo: komponen terfilter sedikit ke kiri, komponen terang tipis ke kanan.
    buf.add(start + i, y, pan - 0.15);
    buf.add(start + i, v * 0.35, pan + 0.35);
  }
}

function pluck(buf, t0, midi, amp, pan = 0, decay = 0.35) {
  const f = midiHz(midi);
  const start = Math.round(t0 * SR);
  for (let i = 0; i < decay * 4 * SR; i++) {
    const t = i / SR;
    const tri = (2 / Math.PI) * Math.asin(Math.sin(TAU * f * t));
    const v = (tri * 0.7 + 0.3 * Math.sin(TAU * f * 2 * t)) * Math.exp(-t / decay) * Math.min(1, t / 0.004) * amp;
    buf.add(start + i, v, pan);
  }
}

function bass(buf, t0, midi, len, amp) {
  const f = midiHz(midi);
  const start = Math.round(t0 * SR);
  for (let i = 0; i < len * SR; i++) {
    const t = i / SR;
    const env = Math.min(1, t / 0.01) * Math.min(1, (len - t) / 0.05) * Math.exp(-t * 1.5);
    buf.add(start + i, (Math.sin(TAU * f * t) + 0.2 * Math.sin(TAU * f * 2 * t)) * env * amp);
  }
}

function kick(buf, t0, amp) {
  const start = Math.round(t0 * SR);
  let ph = 0;
  for (let i = 0; i < 0.35 * SR; i++) {
    const t = i / SR;
    const f = 45 + 85 * Math.exp(-t * 28);
    ph += (TAU * f) / SR;
    buf.add(start + i, Math.sin(ph) * Math.exp(-t * 9) * amp);
  }
}

function hat(buf, t0, amp, rand, pan = 0.2) {
  const start = Math.round(t0 * SR);
  const hp = new Biquad().set('hp', 7000, 0.8);
  for (let i = 0; i < 0.06 * SR; i++) {
    const t = i / SR;
    buf.add(start + i, hp.run(rand() * 2 - 1) * Math.exp(-t * 70) * amp, pan);
  }
}

/* ------------------------------ musik ------------------------------ */

const MOODS = {
  tenang: {
    name: 'Tenang — editorial', bpm: 84, bars: 16, desc: 'Pad hangat + arpeggio lembut. Cocok untuk penjelasan/edukasi, tidak mengganggu suara.',
    chords: [[53, 57, 60, 64], [57, 60, 64, 67], [50, 53, 57, 60], [48, 52, 55, 62]], // Fmaj7 Am7 Dm7 Cadd9
    kickBeats: [0], hats: false, arp: 'eighth', bassPattern: [0, 2],
  },
  fokus: {
    name: 'Fokus — minimal pulse', bpm: 100, bars: 16, desc: 'Denyut ringan, bass 8-an, ketukan pelan. Cocok untuk tips/bisnis.',
    chords: [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]], // Am F C G
    kickBeats: [0, 2], hats: 'offbeat', arp: false, bassPattern: [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5],
  },
  energik: {
    name: 'Energik — upbeat', bpm: 118, bars: 16, desc: 'Ketukan 4/4, pluck 16-an. Cocok untuk hook cepat & konten dinamis.',
    chords: [[50, 53, 57], [46, 50, 53], [53, 57, 60], [48, 52, 55]], // Dm Bb F C
    kickBeats: [0, 1, 2, 3], hats: 'eighth', arp: 'sixteenth', bassPattern: [0.5, 1.5, 2.5, 3.5],
  },
};

function renderMusic(id) {
  const m = MOODS[id];
  const beat = 60 / m.bpm, bar = beat * 4;
  const buf = new Buffer2(bar * m.bars, { loop: true });
  const rand = rng(7);
  for (let b = 0; b < m.bars; b++) {
    const chord = m.chords[b % m.chords.length];
    const t = b * bar;
    pad(buf, t, bar, chord, 0.22);
    for (const k of m.kickBeats) kick(buf, t + k * beat, 0.55);
    // Paruh kedua loop sedikit lebih padat agar tidak terasa berulang.
    const hats = b >= m.bars / 2 ? m.hats || 'offbeat' : m.hats;
    if (hats) {
      const steps = hats === 'offbeat' ? [0.5, 1.5, 2.5, 3.5] : [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5];
      for (const s of steps) hat(buf, t + s * beat, 0.12 * (s % 1 ? 1 : 0.6), rand);
    }
    for (const s of m.bassPattern) bass(buf, t + s * beat, chord[0] - 12, beat * 0.45, 0.32);
    const arp = m.arp || (b >= m.bars / 2 ? 'eighth' : false);
    if (arp) {
      const div = arp === 'sixteenth' ? 4 : 2;
      const seq = [...chord, chord[1] + 12];
      for (let s = 0; s < 4 * div; s++) pluck(buf, t + (s * beat) / div, seq[s % seq.length] + 12, m.arp ? 0.1 : 0.06, s % 2 ? 0.3 : -0.3, arp === 'sixteenth' ? 0.12 : 0.3);
    }
  }
  return buf.normalize(-3);
}

/* ------------------------------ SFX ------------------------------ */

const SFX = {
  pop: { name: 'Pop', desc: 'Muncul kartu/angka', render() {
    const b = new Buffer2(0.14);
    let ph = 0;
    for (let i = 0; i < b.n; i++) {
      const t = i / SR;
      ph += (TAU * (520 + 500 * Math.exp(-t * 40))) / SR;
      b.add(i, Math.sin(ph) * Math.exp(-t * 32));
    }
    return b.edges(1).normalize(-4);
  } },
  click: { name: 'Klik', desc: 'Penekanan halus / ganti poin', render() {
    const b = new Buffer2(0.05), r = rng(3), hp = new Biquad().set('hp', 2500);
    for (let i = 0; i < b.n; i++) {
      const t = i / SR;
      b.add(i, (hp.run(r() * 2 - 1) * 0.6 + Math.sin(TAU * 3200 * t) * 0.4) * Math.exp(-t * 180));
    }
    return b.edges(0.5).normalize(-6);
  } },
  whoosh: { name: 'Whoosh', desc: 'Transisi ke kartu / b-roll', render() {
    const d = 0.55, b = new Buffer2(d), r = rng(11), bp = new Biquad();
    for (let i = 0; i < b.n; i++) {
      const t = i / SR, x = t / d;
      bp.set('bp', 350 * Math.pow(10, x * 1.0), 1.6);
      const env = Math.sin(Math.PI * Math.min(1, x)) ** 2;
      b.add(i, bp.run(r() * 2 - 1) * env, -0.8 + 1.6 * x);
    }
    return b.edges(4).normalize(-5);
  } },
  swoosh: { name: 'Swoosh pendek', desc: 'Teks masuk cepat', render() {
    const d = 0.28, b = new Buffer2(d), r = rng(13), bp = new Biquad();
    for (let i = 0; i < b.n; i++) {
      const t = i / SR, x = t / d;
      bp.set('bp', 2500 * Math.pow(0.35, x), 1.2);
      b.add(i, bp.run(r() * 2 - 1) * Math.sin(Math.PI * x) ** 2, 0.5 - x);
    }
    return b.edges(3).normalize(-6);
  } },
  riser: { name: 'Riser', desc: 'Membangun ketegangan sebelum poin penting', render() {
    const d = 1.6, b = new Buffer2(d), r = rng(17), bp = new Biquad();
    let ph = 0;
    for (let i = 0; i < b.n; i++) {
      const t = i / SR, x = t / d;
      bp.set('bp', 300 + 4000 * x * x, 2);
      ph += (TAU * (180 + 900 * x * x)) / SR;
      b.add(i, (bp.run(r() * 2 - 1) * 0.7 + Math.sin(ph) * 0.3) * x * x);
    }
    return b.edges(3).normalize(-5);
  } },
  impact: { name: 'Impact', desc: 'Angka besar / pernyataan kuat', render() {
    const d = 1.0, b = new Buffer2(d), r = rng(19), lp = new Biquad().set('lp', 900);
    let ph = 0;
    for (let i = 0; i < b.n; i++) {
      const t = i / SR;
      ph += (TAU * (38 + 60 * Math.exp(-t * 12))) / SR;
      b.add(i, Math.sin(ph) * Math.exp(-t * 4.5) + lp.run(r() * 2 - 1) * Math.exp(-t * 30) * 0.5);
    }
    return b.edges(2).normalize(-3);
  } },
  ding: { name: 'Ding', desc: 'Kesimpulan / jawaban benar', render() {
    const d = 1.4, b = new Buffer2(d);
    const parts = [[1318.5, 1, 2.2], [2637, 0.35, 3.5], [3639, 0.18, 5], [5270, 0.08, 7]];
    for (let i = 0; i < b.n; i++) {
      const t = i / SR;
      let v = 0;
      for (const [f, a, k] of parts) v += Math.sin(TAU * f * t) * a * Math.exp(-t * k);
      b.add(i, v * Math.min(1, t / 0.002));
    }
    return b.edges(2).normalize(-6);
  } },
  notif: { name: 'Notifikasi', desc: 'Dua nada naik — poin baru / CTA', render() {
    const b = new Buffer2(0.32);
    for (const [t0, f] of [[0, 880], [0.11, 1320]]) {
      const s = Math.round(t0 * SR);
      for (let i = 0; i < 0.2 * SR; i++) {
        const t = i / SR;
        b.add(s + i, (Math.sin(TAU * f * t) + 0.2 * Math.sin(TAU * f * 2 * t)) * Math.exp(-t * 18) * Math.min(1, t / 0.003));
      }
    }
    return b.edges(2).normalize(-6);
  } },
};

/* ------------------------------ katalog ------------------------------ */

export function catalog() {
  return {
    music: Object.entries(MOODS).map(([id, m]) => ({ id, kind: 'music', name: m.name, desc: m.desc, bpm: m.bpm, loopSec: Math.round(((60 / m.bpm) * 4 * m.bars) * 10) / 10 })),
    sfx: Object.entries(SFX).map(([id, s]) => ({ id, kind: 'sfx', name: s.name, desc: s.desc })),
    license: LICENSE_NOTE,
  };
}

export function isLibraryItem(kind, id) {
  return kind === 'music' ? id in MOODS : kind === 'sfx' ? id in SFX : false;
}

/** Path file WAV; dibuat (sekali) bila belum ada. */
export function libraryFile(kind, id) {
  if (!isLibraryItem(kind, id)) throw new Error(`Item pustaka tidak dikenal: ${kind}/${id}`);
  fs.mkdirSync(LIBRARY_DIR, { recursive: true });
  const file = path.join(LIBRARY_DIR, `${kind}-${id}-v${LIB_VERSION}.wav`);
  if (!fs.existsSync(file)) {
    const buf = kind === 'music' ? renderMusic(id) : SFX[id].render();
    const tmp = `${file}.tmp`;
    fs.writeFileSync(tmp, buf.toWav());
    fs.renameSync(tmp, file);
  }
  return file;
}
