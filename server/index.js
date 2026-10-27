// Server lokal Personal Branding Video Studio.
// Hanya modul bawaan Node; mendengarkan di 127.0.0.1 secara default.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { pipeline } from 'node:stream/promises';
import { config, hasSecret, ROOT } from './lib/config.js';
import { which } from './lib/proc.js';
import { probe, kindOf, aspectLabel, detectSilences, audioLevels, speechRegions, UserError, VIDEO_EXT, IMAGE_EXT, AUDIO_EXT } from './lib/media.js';
import { createProject, loadProject, saveProject, listProjects, applyEdits, deleteProject, projectDir, assetsDir, workDir } from './lib/projects.js';
import { listPresets, getPreset, resolveStyle, savePreset, STYLE_LEVELS } from './lib/presets.js';
import { createJob, runJob, getJob, listJobs, cancelJob, publicJob } from './lib/jobs.js';
import { providerStatus, transcribeLocal, transcribeOpenAI } from './lib/transcribe.js';
import { rulePlan, claudePlan, planToItems } from './lib/plan.js';
import { renderVideo, renderStill, preflight, estimateSize, QUALITY, CONTAINERS, BUILTIN_SFX_LIST } from './lib/render.js';
import { BRAND_PROFILE } from './lib/brand.js';
import { catalog, libraryFile, isLibraryItem, LICENSE_NOTE, paperFile } from './lib/synth.js';
import { distributeText, parseSubtitles, toSrt, projectStatus, OUTPUT_FORMATS, uid } from '../public/shared/core.js';

const MIME = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.json': 'application/json', '.otf': 'font/otf', '.ttf': 'font/ttf', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.webp': 'image/webp', '.svg': 'image/svg+xml', '.mp4': 'video/mp4', '.m4v': 'video/mp4', '.mov': 'video/quicktime',
  '.webm': 'video/webm', '.mkv': 'video/x-matroska', '.avi': 'video/x-msvideo', '.mp3': 'audio/mpeg', '.wav': 'audio/wav',
  '.m4a': 'audio/mp4', '.aac': 'audio/aac', '.ogg': 'audio/ogg', '.flac': 'audio/flac', '.srt': 'text/plain; charset=utf-8',
};

/* ------------------------------ helpers ------------------------------ */

function send(res, status, body, headers = {}) {
  const isBuf = Buffer.isBuffer(body) || typeof body === 'string';
  res.writeHead(status, { 'Content-Type': isBuf ? 'text/plain; charset=utf-8' : 'application/json', 'Cache-Control': 'no-store', ...headers });
  res.end(isBuf ? body : JSON.stringify(body));
}

async function readJson(req, limit = 20 * 1024 * 1024) {
  let size = 0;
  const chunks = [];
  for await (const c of req) {
    size += c.length;
    if (size > limit) throw new UserError('Data yang dikirim terlalu besar.', '', 413);
    chunks.push(c);
  }
  if (!chunks.length) return {};
  try {
    return JSON.parse(Buffer.concat(chunks).toString('utf8'));
  } catch {
    throw new UserError('Format data tidak valid (bukan JSON).');
  }
}

function serveFile(req, res, file, { download = false } = {}) {
  if (!fs.existsSync(file)) return send(res, 404, { error: 'File tidak ditemukan.', hint: file });
  const stat = fs.statSync(file);
  const type = MIME[path.extname(file).toLowerCase()] || 'application/octet-stream';
  const headers = { 'Content-Type': type, 'Accept-Ranges': 'bytes', 'Cache-Control': 'no-store' };
  if (download) headers['Content-Disposition'] = `attachment; filename="${encodeURIComponent(path.basename(file))}"`;
  const range = req.headers.range?.match(/bytes=(\d*)-(\d*)/);
  if (range) {
    const start = range[1] ? Number(range[1]) : stat.size - Number(range[2]);
    const end = range[1] && range[2] ? Math.min(Number(range[2]), stat.size - 1) : stat.size - 1;
    if (start >= stat.size || start < 0) {
      res.writeHead(416, { 'Content-Range': `bytes */${stat.size}` });
      return res.end();
    }
    res.writeHead(206, { ...headers, 'Content-Range': `bytes ${start}-${end}/${stat.size}`, 'Content-Length': end - start + 1 });
    return fs.createReadStream(file, { start, end }).pipe(res);
  }
  res.writeHead(200, { ...headers, 'Content-Length': stat.size });
  fs.createReadStream(file).pipe(res);
}

function summary(p) {
  return {
    id: p.id, name: p.name, updatedAt: p.updatedAt, createdAt: p.createdAt,
    status: projectStatus(p, listJobs(p.id)),
    source: p.source ? { name: p.source.originalName, duration: p.source.meta.duration, width: p.source.meta.width, height: p.source.meta.height, aspect: aspectLabel(p.source.meta.width, p.source.meta.height), missing: p.source.missing } : null,
  };
}

function full(p) {
  return { ...p, status: projectStatus(p, listJobs(p.id)), jobs: listJobs(p.id).filter((j) => j.state === 'running').map(publicJob) };
}

function assertNoRunning(projectId, type) {
  if (listJobs(projectId).some((j) => j.state === 'running' && (!type || j.type === type))) {
    throw new UserError('Masih ada proses yang berjalan untuk proyek ini.', 'Tunggu hingga selesai atau batalkan terlebih dahulu.', 409);
  }
}

/** Simpan unggahan (stream mentah) sebagai salinan baru; tidak pernah menimpa file lain. */
async function receiveUpload(req, dir, rawName, allowedExt, maxBytes) {
  const name = path.basename(String(rawName || 'file')).replace(/[^\w.\- ]+/g, '_').slice(0, 120) || 'file';
  const ext = path.extname(name).toLowerCase();
  if (!allowedExt.includes(ext)) {
    throw new UserError(`Format "${ext || 'tanpa ekstensi'}" tidak didukung.`, `Format yang didukung: ${allowedExt.join(', ')}`, 415);
  }
  const len = Number(req.headers['content-length'] || 0);
  if (len > maxBytes) throw new UserError('File terlalu besar.', `Batas saat ini ${Math.round(maxBytes / 1048576)} MB. Ubah MAX_UPLOAD_MB di .env atau gunakan opsi "path lokal".`, 413);
  fs.mkdirSync(dir, { recursive: true });
  let dest = path.join(dir, name);
  for (let n = 2; fs.existsSync(dest); n++) dest = path.join(dir, `${path.basename(name, ext)}_${n}${ext}`);
  let size = 0;
  const guard = new (await import('node:stream')).Transform({
    transform(chunk, _e, cb) {
      size += chunk.length;
      if (size > maxBytes) return cb(new UserError('File terlalu besar.', `Batas ${Math.round(maxBytes / 1048576)} MB.`, 413));
      cb(null, chunk);
    },
  });
  try {
    await pipeline(req, guard, fs.createWriteStream(dest, { flags: 'wx' }));
  } catch (e) {
    fs.rmSync(dest, { force: true });
    throw e instanceof UserError ? e : new UserError('Unggahan terputus.', 'Coba unggah ulang.', 400);
  }
  return { dest, name };
}

function validateLocalPath(p, allowedExt) {
  if (!p || typeof p !== 'string') throw new UserError('Path file kosong.');
  const abs = path.resolve(p.trim().replace(/^"|"$/g, ''));
  if (!fs.existsSync(abs) || !fs.statSync(abs).isFile()) throw new UserError('File tidak ditemukan di path tersebut.', abs, 404);
  const ext = path.extname(abs).toLowerCase();
  if (!allowedExt.includes(ext)) throw new UserError(`Format "${ext}" tidak didukung.`, `Format yang didukung: ${allowedExt.join(', ')}`, 415);
  return abs;
}

async function attachSource(p, filePath, originalName, copied) {
  const meta = await probe(filePath);
  if (!meta.hasVideo) throw new UserError('File tidak memiliki trek video.', 'Pilih file video (talking head) sebagai sumber.', 415);
  if (meta.duration < 1) throw new UserError('Video terlalu pendek atau durasinya tidak terbaca.', '', 415);
  p.source = { path: filePath, originalName, copied, size: fs.statSync(filePath).size, importedAt: new Date().toISOString(), meta };
  p.analysis = null;
  return saveProject(p);
}

async function addAsset(p, filePath, name, copied, license) {
  const kind = kindOf(filePath);
  const meta = await probe(filePath).catch(() => null);
  if (!meta) throw new UserError('Aset tidak dapat dibaca.', 'File mungkin rusak atau formatnya tidak didukung.', 415);
  const asset = { id: uid('ast'), kind, name, path: filePath, copied, license: String(license || 'Belum diisi').slice(0, 200), addedAt: new Date().toISOString(), meta: { duration: meta.duration, width: meta.width, height: meta.height } };
  p.assets.push(asset);
  saveProject(p);
  return asset;
}

/* ------------------------------ routes ------------------------------ */

const routes = [];
const route = (method, pattern, handler) => routes.push({ method, re: new RegExp(`^${pattern.replace(/:(\w+)/g, '(?<$1>[^/]+)')}$`), handler });

route('GET', '/api/status', async () => {
  const [ffmpeg, ffprobe] = await Promise.all([which('ffmpeg'), which('ffprobe')]);
  return {
    ffmpeg, ffprobe,
    transcription: await providerStatus(),
    claude: { configured: hasSecret('ANTHROPIC_API_KEY'), model: config.anthropicModel, cloud: true },
    presets: listPresets().map(({ id, name, status, note }) => ({ id, name, status, note })),
    styleLevels: STYLE_LEVELS,
    formats: OUTPUT_FORMATS,
    qualities: Object.fromEntries(Object.entries(QUALITY).filter(([k]) => k !== 'pratinjau').map(([k, v]) => [k, v.label])),
    containers: Object.fromEntries(Object.entries(CONTAINERS).map(([k, v]) => [k, v.label])),
    builtinSfx: BUILTIN_SFX_LIST,
    library: catalog(),
    brand: BRAND_PROFILE,
    paths: { projects: config.projectsDir, output: config.outputDir, presets: config.presetsDir },
    limits: { maxUploadMB: Math.round(config.maxUploadBytes / 1048576) },
    accept: { video: VIDEO_EXT, image: IMAGE_EXT, audio: AUDIO_EXT },
  };
});

route('GET', '/api/projects', async () => listProjects().map(summary));
route('POST', '/api/projects', async ({ req }) => full(createProject(await readJson(req))));
route('GET', '/api/projects/:id', async ({ id }) => full(loadProject(id)));
route('PUT', '/api/projects/:id', async ({ id, req }) => {
  const body = await readJson(req);
  const p = loadProject(id);
  applyEdits(p, body);
  return full(saveProject(p));
});
route('DELETE', '/api/projects/:id', async ({ id }) => {
  assertNoRunning(id);
  deleteProject(id);
  return { ok: true };
});

route('POST', '/api/projects/:id/source/upload', async ({ id, req, url }) => {
  const p = loadProject(id);
  assertNoRunning(id);
  const { dest, name } = await receiveUpload(req, path.join(projectDir(id), 'source'), url.searchParams.get('name'), VIDEO_EXT, config.maxUploadBytes);
  try {
    return full(await attachSource(p, dest, name, true));
  } catch (e) {
    fs.rmSync(dest, { force: true });
    throw e;
  }
});
route('POST', '/api/projects/:id/source/path', async ({ id, req }) => {
  const p = loadProject(id);
  assertNoRunning(id);
  const abs = validateLocalPath((await readJson(req)).path, VIDEO_EXT);
  return full(await attachSource(p, abs, path.basename(abs), false));
});
route('GET', '/api/projects/:id/media/source', async ({ id, req, res }) => {
  const p = loadProject(id);
  if (!p.source) throw new UserError('Belum ada video sumber.', '', 404);
  serveFile(req, res, p.source.path);
  return null;
});

route('POST', '/api/projects/:id/assets/upload', async ({ id, req, url }) => {
  const p = loadProject(id);
  const allowed = [...VIDEO_EXT, ...IMAGE_EXT, ...AUDIO_EXT];
  const { dest, name } = await receiveUpload(req, assetsDir(id), url.searchParams.get('name'), allowed, config.maxUploadBytes);
  try {
    return await addAsset(p, dest, name, true, url.searchParams.get('license'));
  } catch (e) {
    fs.rmSync(dest, { force: true });
    throw e;
  }
});
route('POST', '/api/projects/:id/assets/path', async ({ id, req }) => {
  const p = loadProject(id);
  const body = await readJson(req);
  const abs = validateLocalPath(body.path, [...VIDEO_EXT, ...IMAGE_EXT, ...AUDIO_EXT]);
  return addAsset(p, abs, path.basename(abs), false, body.license);
});
route('PUT', '/api/projects/:id/assets/:assetId', async ({ id, assetId, req }) => {
  const p = loadProject(id);
  const a = p.assets.find((x) => x.id === assetId);
  if (!a) throw new UserError('Aset tidak ditemukan.', '', 404);
  const body = await readJson(req);
  if ('license' in body) a.license = String(body.license).slice(0, 200);
  saveProject(p);
  return a;
});
route('DELETE', '/api/projects/:id/assets/:assetId', async ({ id, assetId }) => {
  const p = loadProject(id);
  const a = p.assets.find((x) => x.id === assetId);
  if (!a) throw new UserError('Aset tidak ditemukan.', '', 404);
  // Hanya salinan di folder proyek yang dihapus; file referensi milik pengguna tidak disentuh.
  if (a.copied && a.path.startsWith(assetsDir(id))) fs.rmSync(a.path, { force: true });
  p.assets = p.assets.filter((x) => x.id !== assetId);
  for (const b of p.broll) if (b.assetId === assetId) b.assetId = null;
  for (const s of p.sfx) if (s.assetId === assetId) s.assetId = null;
  if (p.music.assetId === assetId) Object.assign(p.music, { assetId: null, enabled: false });
  saveProject(p);
  return full(p);
});
route('GET', '/api/projects/:id/media/asset/:assetId', async ({ id, assetId, req, res }) => {
  const a = loadProject(id).assets.find((x) => x.id === assetId);
  if (!a) throw new UserError('Aset tidak ditemukan.', '', 404);
  serveFile(req, res, a.path);
  return null;
});

// Pustaka audio sintetis bawaan (dibuat on-demand, di-cache di library/).
route('GET', '/api/library/:kind/:item/file', async ({ kind, item, req, res }) => {
  if (!isLibraryItem(kind, item)) throw new UserError('Item pustaka tidak ditemukan.', '', 404);
  serveFile(req, res, libraryFile(kind, item));
  return null;
});
route('GET', '/api/library/paper/:w/:h/file', async ({ w, h, req, res, url }) => {
  const W = Number(w), Hh = Number(h);
  if (!(W > 0 && W <= 4096)) throw new UserError('Ukuran tidak valid.', '', 400);
  const c = /^#[0-9a-fA-F]{6}$/.test(url.searchParams.get('c') || '') ? url.searchParams.get('c') : '#F2F1ED';
  if (!(Hh > 0 && Hh <= 4096)) throw new UserError('Ukuran tidak valid.', '', 400);
  serveFile(req, res, paperFile(W, Hh, c));
  return null;
});
route('POST', '/api/projects/:id/library/music', async ({ id, req }) => {
  const { item } = await readJson(req);
  if (!isLibraryItem('music', item)) throw new UserError('Musik bawaan tidak ditemukan.', '', 404);
  const p = loadProject(id);
  const file = libraryFile('music', item);
  let asset = p.assets.find((a) => a.builtin === `music:${item}`);
  if (!asset) {
    const meta = await probe(file);
    asset = { id: uid('ast'), kind: 'audio', builtin: `music:${item}`, name: `Musik bawaan — ${catalog().music.find((m) => m.id === item).name}`, path: file, copied: false, license: LICENSE_NOTE, addedAt: new Date().toISOString(), meta: { duration: meta.duration } };
    p.assets.push(asset);
  }
  Object.assign(p.music, { assetId: asset.id, enabled: true });
  return full(saveProject(p));
});

route('POST', '/api/projects/:id/analyze', async ({ id }) => {
  const p = loadProject(id);
  if (!p.source || p.source.missing) throw new UserError('Video sumber tidak tersedia.', 'Impor ulang video sumber.', 404);
  assertNoRunning(id);
  const job = createJob('analyze', id, 'Analisis video');
  return publicJob(runJob(job, async () => {
    job.message = 'Membaca informasi video…';
    const meta = await probe(p.source.path);
    job.progress = 0.2;
    const analysis = { at: new Date().toISOString(), silences: [], speech: [], levels: null, warnings: [] };
    if (!meta.hasAudio) {
      analysis.warnings.push('Video tidak memiliki trek audio. Transkripsi otomatis tidak bisa dilakukan; ketik transkrip manual bila perlu.');
    } else {
      job.message = 'Mengukur level audio…';
      analysis.levels = await audioLevels(p.source.path);
      job.progress = 0.45;
      if (analysis.levels.maxDb !== null && analysis.levels.maxDb < -45) analysis.warnings.push('Audio sangat pelan atau kosong. Periksa mikrofon/trek audio.');
      job.message = 'Mendeteksi bagian hening…';
      analysis.silences = await detectSilences(p.source.path);
      analysis.speech = speechRegions(analysis.silences, meta.duration);
    }
    const fresh = loadProject(id);
    fresh.source.meta = meta;
    fresh.analysis = analysis;
    saveProject(fresh);
    return { silences: analysis.silences.length };
  }));
});

route('POST', '/api/projects/:id/transcribe', async ({ id, req }) => {
  const body = await readJson(req);
  const p = loadProject(id);
  if (!p.source || p.source.missing) throw new UserError('Video sumber tidak tersedia.', '', 404);
  if (!p.source.meta.hasAudio) throw new UserError('Video tidak memiliki audio untuk ditranskripsi.', 'Gunakan transkrip manual.', 422);
  if (body.provider === 'openai' && body.consent !== true) {
    throw new UserError('Persetujuan diperlukan sebelum mengirim audio ke layanan cloud.', 'Centang persetujuan pada dialog transkripsi cloud.', 428);
  }
  assertNoRunning(id);
  const job = createJob('transcribe', id, body.provider === 'openai' ? 'Transkripsi cloud (OpenAI)' : 'Transkripsi lokal');
  return publicJob(runJob(job, async () => {
    const t = body.provider === 'openai' ? await transcribeOpenAI(p, job) : await transcribeLocal(p, job);
    const fresh = loadProject(id);
    fresh.transcript = t;
    saveProject(fresh);
    return { segments: t.segments.length };
  }));
});

route('POST', '/api/projects/:id/transcript/manual', async ({ id, req }) => {
  const { text } = await readJson(req);
  const p = loadProject(id);
  if (!p.source) throw new UserError('Impor video terlebih dahulu.');
  if (!String(text || '').trim()) throw new UserError('Teks transkrip kosong.');
  const segments = distributeText(text, p.analysis?.speech, p.source.meta.duration);
  p.transcript = { source: 'manual', language: '', createdAt: new Date().toISOString(), reviewed: false, segments, note: p.analysis?.speech?.length ? 'Waktu diestimasi dari bagian ucapan hasil deteksi hening.' : 'Waktu diestimasi merata (video belum dianalisis).' };
  return full(saveProject(p));
});

route('POST', '/api/projects/:id/transcript/import', async ({ id, req }) => {
  const { content, name } = await readJson(req);
  const p = loadProject(id);
  const segments = parseSubtitles(content);
  if (!segments.length) throw new UserError('Tidak ada subtitle yang dapat dibaca dari file.', 'Pastikan file berformat .srt atau .vtt yang valid.', 422);
  p.transcript = { source: 'import', fileName: name || '', language: '', createdAt: new Date().toISOString(), reviewed: false, segments, note: 'Timestamp per kata diestimasi dari timestamp kalimat.' };
  return full(saveProject(p));
});

route('GET', '/api/projects/:id/transcript.srt', async ({ id, res }) => {
  const p = loadProject(id);
  if (!p.transcript?.segments?.length) throw new UserError('Belum ada transkrip.', '', 404);
  send(res, 200, toSrt(p.transcript.segments), { 'Content-Type': 'text/plain; charset=utf-8', 'Content-Disposition': `attachment; filename="transkrip.srt"` });
  return null;
});

route('POST', '/api/projects/:id/plan', async ({ id, req }) => {
  const body = await readJson(req);
  const p = loadProject(id);
  let plan, origin;
  if (body.source === 'claude') {
    if (body.consent !== true) throw new UserError('Persetujuan diperlukan sebelum mengirim transkrip ke Claude.', 'Centang persetujuan pada dialog.', 428);
    plan = await claudePlan(p);
    origin = 'claude';
  } else {
    plan = rulePlan(p);
    origin = 'aturan';
  }
  const items = planToItems(plan, origin, p.transcript?.segments || []);
  // Ganti saran lama yang belum disetujui; pertahankan yang disetujui/dibuat pengguna.
  const keepOld = (arr) => arr.filter((x) => x.origin === 'pengguna' || x.approved || x.enabled);
  p.cuts = [...keepOld(p.cuts), ...items.cuts];
  p.cards = [...keepOld(p.cards), ...items.cards];
  p.broll = [...keepOld(p.broll), ...items.broll];
  p.sfx = [...keepOld(p.sfx), ...items.sfx];
  p.emphasisSuggestions = [...keepOld(p.emphasisSuggestions || []), ...items.emphasis];
  p.zooms = [...keepOld(p.zooms || []), ...items.zooms];
  p.plan = { origin, at: new Date().toISOString(), structure: items.structure, music: items.music, notes: items.notes };
  return full(saveProject(p));
});

route('POST', '/api/projects/:id/apply-preset', async ({ id, req }) => {
  const { presetId, level } = await readJson(req);
  const p = loadProject(id);
  const preset = getPreset(presetId || p.presetId);
  p.presetId = preset.id;
  p.styleLevel = STYLE_LEVELS.includes(level) ? level : 'editorial';
  p.style = resolveStyle(preset, p.styleLevel);
  return full(saveProject(p));
});

route('POST', '/api/presets', async ({ req }) => {
  const { id, name, projectId } = await readJson(req);
  const p = loadProject(projectId);
  return savePreset({ id, name, style: p.style, basedOn: p.presetId });
});

route('GET', '/api/projects/:id/preflight', async ({ id, url }) => {
  const p = loadProject(id);
  return { ...preflight(p), estimate: p.source ? estimateSize(p, url.searchParams.get('quality') || 'standar', url.searchParams.get('aspect') || '9:16') : null };
});

route('POST', '/api/projects/:id/still', async ({ id, req }) => {
  const body = await readJson(req);
  const p = loadProject(id);
  const pf = preflight(p);
  if (!pf.ok) throw new UserError(pf.problems.join(' '), '', 409);
  const r = await renderStill(p, { aspect: body.aspect || p.output.aspect, sourceTime: Number(body.sourceTime) || 0 });
  return { url: `/api/projects/${id}/frame/${path.basename(r.file)}`, outputTime: r.outputTime };
});
route('GET', '/api/projects/:id/frame/:name', async ({ id, name, req, res }) => {
  if (!/^frame_\d+\.png$/.test(name)) throw new UserError('Nama frame tidak valid.', '', 400);
  serveFile(req, res, path.join(workDir(id), name));
  return null;
});

route('POST', '/api/projects/:id/render', async ({ id, req }) => {
  const body = await readJson(req);
  const p = loadProject(id);
  const pf = preflight(p);
  if (!pf.ok) throw new UserError(pf.problems.join(' '), 'Perbaiki masalah di atas lalu coba lagi.', 409);
  assertNoRunning(id, 'render');
  const preview = Boolean(body.preview);
  const job = createJob('render', id, preview ? 'Render pratinjau' : 'Ekspor video');
  const record = { id: uid('exp'), state: 'running', preview, requestedAt: new Date().toISOString(), aspect: body.aspect || '9:16', quality: body.quality || 'standar', container: body.container || 'mp4', jobId: job.id };
  if (!preview) {
    p.exports = [record, ...(p.exports || [])].slice(0, 30);
    saveProject(p);
  }
  return publicJob(runJob(job, async () => {
    const finish = (patch) => {
      const fresh = loadProject(id);
      if (preview) fresh.lastPreview = { ...record, ...patch };
      else fresh.exports = (fresh.exports || []).map((e) => (e.id === record.id ? { ...e, ...patch } : e));
      saveProject(fresh);
    };
    try {
      const out = await renderVideo(p, job, { aspect: record.aspect, quality: record.quality, container: record.container, outDir: body.outDir, preview });
      finish({ state: 'done', ...out, finishedAt: new Date().toISOString() });
      return { exportId: record.id, ...out };
    } catch (e) {
      finish({ state: job.controller.signal.aborted ? 'canceled' : 'failed', error: e.message, hint: e.hint || '', finishedAt: new Date().toISOString() });
      throw e;
    }
  }));
});
route('GET', '/api/projects/:id/exports/:exportId/file', async ({ id, exportId, req, res, url }) => {
  const p = loadProject(id);
  const e = exportId === 'preview' ? p.lastPreview : (p.exports || []).find((x) => x.id === exportId);
  if (!e || e.state !== 'done') throw new UserError('File ekspor tidak tersedia.', '', 404);
  serveFile(req, res, e.path, { download: url.searchParams.get('download') === '1' });
  return null;
});

route('GET', '/api/jobs/:jobId', async ({ jobId }) => {
  const j = getJob(jobId);
  if (!j) throw new UserError('Proses tidak ditemukan (server mungkin dijalankan ulang).', '', 404);
  return publicJob(j);
});
route('POST', '/api/jobs/:jobId/cancel', async ({ jobId }) => publicJob(cancelJob(jobId)));

/* ------------------------------ server ------------------------------ */

const STATIC = [
  ['/fonts/', path.join(ROOT, 'assets', 'fonts')],
  ['/', path.join(ROOT, 'public')],
];

function allowedHost(req) {
  const host = String(req.headers.host || '').replace(/:\d+$/, '');
  return ['localhost', '127.0.0.1', '[::1]'].includes(host) || host === config.host;
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://localhost');
  try {
    // Lindungi dari DNS rebinding & permintaan lintas situs ke server lokal.
    if (!allowedHost(req)) return send(res, 403, { error: 'Host tidak diizinkan.' });
    if (url.pathname.startsWith('/api/')) {
      if (req.method !== 'GET' && req.headers['x-pb-app'] !== '1') return send(res, 403, { error: 'Permintaan ditolak.' });
      for (const r of routes) {
        if (r.method !== req.method) continue;
        const m = url.pathname.match(r.re);
        if (!m) continue;
        const out = await r.handler({ ...m.groups, req, res, url });
        if (out !== null && !res.headersSent) send(res, 200, out);
        return;
      }
      return send(res, 404, { error: 'Endpoint tidak ditemukan.' });
    }
    if (req.method !== 'GET') return send(res, 405, 'Method tidak diizinkan');
    for (const [prefix, dir] of STATIC) {
      if (!url.pathname.startsWith(prefix)) continue;
      const rel = decodeURIComponent(url.pathname.slice(prefix.length)) || 'index.html';
      const file = path.resolve(dir, rel);
      if (!file.startsWith(dir + path.sep) && file !== dir) return send(res, 403, 'Terlarang');
      if (fs.existsSync(file) && fs.statSync(file).isFile()) return serveFile(req, res, file);
    }
    send(res, 404, 'Tidak ditemukan');
  } catch (err) {
    const status = err.status || (err instanceof UserError ? 400 : 500);
    if (!(err instanceof UserError)) console.error('[server]', err);
    if (!res.headersSent) send(res, status, { error: err instanceof UserError ? err.message : 'Terjadi kesalahan di server.', hint: err.hint || (err instanceof UserError ? '' : 'Lihat log terminal untuk detail.') });
    else res.end();
  }
});

// Ekspor yang tercatat "running" dari sesi server sebelumnya tidak mungkin selesai lagi.
for (const p of listProjects()) {
  const stale = (p.exports || []).filter((e) => e.state === 'running');
  if (!stale.length) continue;
  for (const e of stale) Object.assign(e, { state: 'failed', error: 'Ekspor terhenti karena server dimatikan.', hint: 'Jalankan ekspor ulang.' });
  saveProject(p);
}

server.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.error(`Port ${config.port} sudah dipakai aplikasi lain.`);
    console.error(`Ubah PORT di file .env (mis. PORT=${config.port + 83}) lalu jalankan "npm start" lagi.`);
    process.exit(1);
  }
  throw err;
});

server.listen(config.port, config.host, () => {
  console.log(`Personal Branding Video Studio berjalan di http://${config.host === '0.0.0.0' ? 'localhost' : config.host}:${config.port}`);
  console.log(`Proyek: ${config.projectsDir}`);
  console.log(`Output: ${config.outputDir}`);
});
