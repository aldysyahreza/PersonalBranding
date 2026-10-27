// Penyedia transkripsi. Status kesiapan dilaporkan apa adanya ke UI.
//  - local  : faster-whisper di komputer ini (data tidak keluar).
//  - openai : OpenAI Whisper API (cloud) — hanya audio, hanya dengan persetujuan.
//  - manual : ketik/tempel teks, atau impor SRT/VTT (selalu tersedia).
import fs from 'node:fs';
import path from 'node:path';
import { config, getSecret, hasSecret, ROOT } from './config.js';
import { run } from './proc.js';
import { UserError } from './media.js';
import { makeSegment } from '../../public/shared/core.js';
import { workDir } from './projects.js';

let localCache = null;

export async function providerStatus() {
  if (!localCache || Date.now() - localCache.at > 60000) {
    let ok = false;
    let detail = '';
    try {
      const r = await run(config.whisperPython, ['-c', 'import faster_whisper,sys;print(faster_whisper.__version__)'], { timeoutMs: 20000 });
      ok = r.code === 0;
      detail = ok ? `faster-whisper ${r.stdout.trim()}` : 'Paket faster-whisper belum terpasang.';
    } catch {
      detail = `Python ("${config.whisperPython}") tidak ditemukan.`;
    }
    localCache = { at: Date.now(), ok, detail };
  }
  return {
    local: { available: localCache.ok, detail: localCache.detail, model: config.whisperModel, cloud: false, setup: 'pip install faster-whisper  (model diunduh otomatis saat pertama dipakai)' },
    openai: { available: hasSecret('OPENAI_API_KEY'), detail: hasSecret('OPENAI_API_KEY') ? 'API key terkonfigurasi di .env' : 'OPENAI_API_KEY belum diisi di .env', cloud: true, setup: 'Isi OPENAI_API_KEY di file .env lalu jalankan ulang aplikasi.' },
    manual: { available: true, detail: 'Ketik/tempel teks atau impor file .srt/.vtt', cloud: false },
  };
}

async function extractAudio(project, { mp3 = false, signal } = {}) {
  const out = path.join(workDir(project.id), mp3 ? 'audio_stt.mp3' : 'audio_stt.wav');
  const args = ['-hide_banner', '-y', '-i', project.source.path, '-vn', '-ac', '1', '-ar', '16000'];
  if (mp3) args.push('-c:a', 'libmp3lame', '-b:a', '48k');
  args.push(out);
  const r = await run('ffmpeg', args, { timeoutMs: 30 * 60000, signal });
  if (r.code !== 0) throw new UserError('Audio tidak dapat diekstrak dari video.', 'Pastikan video memiliki trek audio yang dapat dibaca.');
  return out;
}

export async function transcribeLocal(project, job) {
  const status = (await providerStatus()).local;
  if (!status.available) throw new UserError('Transkripsi lokal belum tersedia.', `${status.detail} Pasang dengan: ${status.setup}`, 412);
  job.message = 'Mengekstrak audio…';
  const wav = await extractAudio(project, { signal: job.controller.signal });
  job.message = `Mentranskripsi dengan model "${config.whisperModel}" (pertama kali dapat memakan waktu untuk mengunduh model)…`;
  const r = await run(config.whisperPython, [path.join(ROOT, 'scripts', 'transcribe_local.py'), wav, config.whisperModel, config.whisperLanguage], {
    signal: job.controller.signal,
    onStderr: (s) => {
      const m = s.match(/PROGRESS ([\d.]+)/g);
      if (m) job.progress = Number(m[m.length - 1].split(' ')[1]) * 0.98;
    },
  });
  fs.rmSync(wav, { force: true });
  if (r.code !== 0) {
    if (r.stderr.includes('ERROR_NO_FASTER_WHISPER')) throw new UserError('faster-whisper belum terpasang.', status.setup, 412);
    const hint = /huggingface|connection|resolve|HTTPSConnection|offline/i.test(r.stderr)
      ? 'Model belum ada di cache dan tidak dapat diunduh. Sambungkan internet sekali untuk mengunduh model, atau gunakan transkrip manual.'
      : r.stderr.split('\n').filter(Boolean).slice(-2).join(' ');
    throw new UserError('Transkripsi lokal gagal.', hint, 500);
  }
  const data = JSON.parse(r.stdout);
  return toTranscript(data, 'local-whisper');
}

export async function transcribeOpenAI(project, job) {
  if (!hasSecret('OPENAI_API_KEY')) throw new UserError('OPENAI_API_KEY belum dikonfigurasi.', 'Isi OPENAI_API_KEY di file .env lalu jalankan ulang aplikasi.', 412);
  job.message = 'Mengekstrak audio (mono, terkompresi)…';
  const mp3 = await extractAudio(project, { mp3: true, signal: job.controller.signal });
  const size = fs.statSync(mp3).size;
  if (size > 25 * 1024 * 1024) {
    fs.rmSync(mp3, { force: true });
    throw new UserError('Audio terlalu besar untuk API cloud (>25 MB).', 'Gunakan transkripsi lokal, atau potong video menjadi bagian lebih pendek.', 413);
  }
  job.message = 'Mengunggah audio ke OpenAI (disetujui pengguna)…';
  const form = new FormData();
  form.append('file', new Blob([fs.readFileSync(mp3)], { type: 'audio/mpeg' }), 'audio.mp3');
  form.append('model', config.openaiTranscribeModel);
  form.append('response_format', 'verbose_json');
  form.append('timestamp_granularities[]', 'word');
  form.append('timestamp_granularities[]', 'segment');
  if (config.whisperLanguage) form.append('language', config.whisperLanguage);
  let res;
  try {
    res = await fetch('https://api.openai.com/v1/audio/transcriptions', {
      method: 'POST',
      headers: { Authorization: `Bearer ${getSecret('OPENAI_API_KEY')}` },
      body: form,
      signal: job.controller.signal,
    });
  } catch (e) {
    if (job.controller.signal.aborted) throw e;
    throw new UserError('Tidak dapat terhubung ke OpenAI.', 'Periksa koneksi internet.', 502);
  } finally {
    fs.rmSync(mp3, { force: true });
  }
  if (res.status === 401) throw new UserError('API key OpenAI ditolak.', 'Periksa OPENAI_API_KEY di file .env.', 401);
  if (!res.ok) throw new UserError(`Transkripsi cloud gagal (status ${res.status}).`, 'Coba lagi nanti atau gunakan transkripsi lokal/manual.', 502);
  const data = await res.json();
  // Pasangkan kata ke segmen berdasarkan waktu.
  const words = data.words || [];
  const segments = (data.segments || []).map((s) => ({
    start: s.start,
    end: s.end,
    text: s.text,
    words: words.filter((w) => w.start >= s.start - 0.01 && w.end <= s.end + 0.01).map((w) => ({ text: w.word, start: w.start, end: w.end })),
  }));
  return toTranscript({ language: data.language, segments }, 'openai');
}

function toTranscript(data, source) {
  const segments = (data.segments || [])
    .filter((s) => String(s.text || '').trim())
    .map((s) => {
      // Kata dari ASR bisa berisi spasi internal; satukan agar 1 token = 1 kata bertimestamp.
      const words = (s.words || []).map((w) => ({ ...w, text: String(w.text).trim().replace(/\s+/g, '') })).filter((w) => w.text);
      const hasWords = words.length > 0;
      const text = hasWords ? words.map((w) => w.text).join(' ') : s.text;
      return makeSegment({ start: s.start, end: s.end, text, words: hasWords ? words : null, timing: hasWords ? 'asr' : 'estimated' });
    });
  if (!segments.length) throw new UserError('Tidak ada ucapan yang terdeteksi.', 'Periksa apakah audio berisi suara, atau ketik transkrip secara manual.', 422);
  return { source, language: data.language || '', createdAt: new Date().toISOString(), reviewed: false, segments };
}
