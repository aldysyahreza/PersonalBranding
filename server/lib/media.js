// Membaca informasi media (ffprobe) dan analisis audio dasar (ffmpeg).
// Semua fungsi di sini hanya MEMBACA file sumber; tidak pernah menulisnya.
import fs from 'node:fs';
import path from 'node:path';
import { run } from './proc.js';

export const VIDEO_EXT = ['.mp4', '.mov', '.m4v', '.mkv', '.webm', '.avi'];
export const IMAGE_EXT = ['.png', '.jpg', '.jpeg', '.webp'];
export const AUDIO_EXT = ['.mp3', '.wav', '.m4a', '.aac', '.ogg', '.flac'];

export class UserError extends Error {
  constructor(message, hint = '', status = 400) {
    super(message);
    this.hint = hint;
    this.status = status;
  }
}

export function kindOf(file) {
  const ext = path.extname(file).toLowerCase();
  if (VIDEO_EXT.includes(ext)) return 'video';
  if (IMAGE_EXT.includes(ext)) return 'image';
  if (AUDIO_EXT.includes(ext)) return 'audio';
  return null;
}

function parseRate(r) {
  if (!r || r === '0/0') return 0;
  const [a, b] = r.split('/').map(Number);
  return b ? a / b : a;
}

export async function probe(file) {
  if (!fs.existsSync(file)) {
    throw new UserError('File tidak ditemukan.', `Periksa kembali lokasi file: ${file}`, 404);
  }
  const r = await run('ffprobe', ['-v', 'error', '-show_format', '-show_streams', '-of', 'json', file], { timeoutMs: 60000 });
  if (r.code !== 0) {
    throw new UserError(
      'File tidak dapat dibaca sebagai media.',
      'Format mungkin tidak didukung atau file rusak. Coba ekspor ulang video sebagai MP4 (H.264 + AAC).',
    );
  }
  const data = JSON.parse(r.stdout);
  const v = data.streams.find((s) => s.codec_type === 'video' && s.disposition?.attached_pic !== 1);
  const a = data.streams.find((s) => s.codec_type === 'audio');
  let rotation = 0;
  if (v) {
    const sd = (v.side_data_list || []).find((d) => d.rotation !== undefined);
    rotation = Number(sd?.rotation ?? v.tags?.rotate ?? 0);
  }
  let width = v?.width || 0;
  let height = v?.height || 0;
  if (Math.abs(rotation) % 180 === 90) [width, height] = [height, width];
  const duration = Number(data.format?.duration || v?.duration || a?.duration || 0);
  return {
    duration,
    width,
    height,
    rotation,
    fps: v ? Math.round(parseRate(v.avg_frame_rate || v.r_frame_rate) * 100) / 100 : 0,
    videoCodec: v?.codec_name || null,
    hasVideo: Boolean(v),
    hasAudio: Boolean(a),
    audioCodec: a?.codec_name || null,
    sampleRate: a ? Number(a.sample_rate) : 0,
    size: Number(data.format?.size || fs.statSync(file).size),
    formatName: data.format?.format_name || '',
  };
}

export function aspectLabel(w, h) {
  if (!w || !h) return '-';
  const r = w / h;
  const known = [['9:16', 9 / 16], ['4:5', 4 / 5], ['1:1', 1], ['4:3', 4 / 3], ['16:9', 16 / 9], ['3:4', 3 / 4]];
  for (const [label, val] of known) if (Math.abs(r - val) < 0.02) return label;
  return r.toFixed(2) + ':1';
}

/** Deteksi bagian hening. Mengembalikan [{start,end}] dalam detik (timeline sumber). */
export async function detectSilences(file, { noiseDb = -35, minDur = 0.45 } = {}) {
  const r = await run('ffmpeg', ['-hide_banner', '-nostats', '-i', file, '-vn', '-af', `silencedetect=n=${noiseDb}dB:d=${minDur}`, '-f', 'null', '-'], { timeoutMs: 30 * 60000 });
  if (r.code !== 0) throw new UserError('Audio tidak dapat dianalisis.', 'Pastikan video memiliki trek audio yang valid.');
  const out = [];
  let start = null;
  for (const line of r.stderr.split('\n')) {
    const s = line.match(/silence_start: (-?[\d.]+)/);
    const e = line.match(/silence_end: ([\d.]+)/);
    if (s) start = Math.max(0, Number(s[1]));
    if (e && start !== null) {
      out.push({ start: round(start), end: round(Number(e[1])) });
      start = null;
    }
  }
  return out;
}

/** Statistik loudness kasar (mean/max dB) untuk mendeteksi audio terlalu pelan atau kosong. */
export async function audioLevels(file) {
  const r = await run('ffmpeg', ['-hide_banner', '-nostats', '-i', file, '-vn', '-af', 'volumedetect', '-f', 'null', '-'], { timeoutMs: 30 * 60000 });
  const mean = r.stderr.match(/mean_volume: (-?[\d.]+) dB/);
  const max = r.stderr.match(/max_volume: (-?[\d.]+) dB/);
  return { meanDb: mean ? Number(mean[1]) : null, maxDb: max ? Number(max[1]) : null };
}

/** Kebalikan dari bagian hening: rentang yang berisi suara. */
export function speechRegions(silences, duration) {
  const regions = [];
  let t = 0;
  for (const s of silences) {
    if (s.start > t + 0.05) regions.push({ start: round(t), end: round(s.start) });
    t = Math.max(t, s.end);
  }
  if (duration > t + 0.05) regions.push({ start: round(t), end: round(duration) });
  return regions;
}

export function round(n, d = 3) {
  const f = 10 ** d;
  return Math.round(n * f) / f;
}
