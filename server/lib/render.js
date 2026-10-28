// Komposisi & render dengan ffmpeg. Satu fungsi membangun filter graph yang
// dipakai untuk: ekspor final, render pratinjau cepat, dan frame pratinjau.
// Dengan begitu pratinjau mencerminkan konfigurasi aktual yang akan diekspor.
import fs from 'node:fs';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { config } from './config.js';
import { run } from './proc.js';
import { probe, UserError } from './media.js';
import { buildAss } from './ass.js';
import { keepSegments, outputDuration, mapSpan, mapTime, framing, zoomPieces, enforcePacing, OUTPUT_FORMATS, r3 } from '../../public/shared/core.js';
import { libraryFile, isLibraryItem, catalog, paperFile } from './synth.js';
import { hyperframesStatus, prepareCardClips } from './hyperframes.js';
import { workDir } from './projects.js';

export const QUALITY = {
  tinggi: { crf: 18, preset: 'slow', audio: '192k', label: 'Tinggi (file besar)', estMbps: 5 },
  standar: { crf: 21, preset: 'medium', audio: '160k', label: 'Standar (disarankan)', estMbps: 3 },
  kecil: { crf: 26, preset: 'medium', audio: '128k', label: 'Kecil (hemat ukuran)', estMbps: 1.5 },
  pratinjau: { crf: 30, preset: 'ultrafast', audio: '96k', label: 'Pratinjau cepat', estMbps: 1 },
};

export const CONTAINERS = { mp4: { ext: '.mp4', label: 'MP4 (H.264 + AAC)' }, mov: { ext: '.mov', label: 'MOV (H.264 + AAC)' } };

export const BUILTIN_SFX_LIST = catalog().sfx.map((x) => x.id);

let majorCache = null;
/** Versi mayor ffmpeg (0 bila tidak terbaca, mis. build git "N-xxxxx"). */
export function ffmpegMajor() {
  if (majorCache === null) {
    const r = spawnSync('ffmpeg', ['-version']);
    const m = String(r.stdout || '').match(/ffmpeg version n?(\d+)\./);
    majorCache = m ? Number(m[1]) : 0;
  }
  return majorCache;
}

function dbToLin(db) {
  return Math.pow(10, db / 20).toFixed(4);
}

function assetById(project, id) {
  return (project.assets || []).find((a) => a.id === id);
}

/** Periksa kesiapan render dan kumpulkan peringatan yang jujur. */
export function preflight(project) {
  const problems = [];
  const warnings = [];
  if (!project.source) problems.push('Belum ada video sumber.');
  else if (project.source.missing) problems.push(`File sumber tidak ditemukan: ${project.source.path}`);
  if (project.source?.changed) warnings.push('Ukuran file sumber berubah sejak diimpor. Periksa kembali sinkron subtitle.');
  if (!project.transcript?.segments?.length) warnings.push('Belum ada transkrip — video diekspor tanpa subtitle.');
  else if (!project.transcript.reviewed) warnings.push('Transkrip belum ditandai "sudah dikoreksi".');
  for (const b of project.broll || []) {
    if (!b.approved) continue;
    const a = b.assetId && assetById(project, b.assetId);
    if (!a) warnings.push(`B-roll ${b.start.toFixed(1)} dtk disetujui tetapi belum ada aset — dilewati.`);
    else if (a.missing) warnings.push(`Aset b-roll "${a.name}" hilang — dilewati.`);
  }
  if (project.music?.enabled) {
    const a = assetById(project, project.music.assetId);
    if (!a) warnings.push('Musik diaktifkan tetapi belum ada file musik — dilewati.');
    else if (a.missing) warnings.push(`File musik "${a.name}" hilang — dilewati.`);
  }
  for (const c of project.cards || []) if (c.approved && c.needsReview) warnings.push(`Kartu "${c.title}" berisi kata yang tidak ditemukan di ucapan.`);
  const pace = enforcePacing({ cards: project.cards, zooms: project.zooms, duration: project.source?.meta?.duration, pacing: project.style?.pacing }).changes;
  if (pace.length) warnings.push(`Ritme: ${pace.length} kartu/zoom terlalu rapat atau singkat (adegan wajah terasa terlalu cepat). Gunakan "Rapikan ritme" di Rencana edit.`);
  if (!project.source?.meta?.hasAudio) warnings.push('Video sumber tidak memiliki audio.');
  return { ok: problems.length === 0, problems, warnings };
}

/**
 * Bangun argumen ffmpeg.
 * @param {object} o { width, height, quality, container, outFile, stillAt (detik output, opsional), withAudio }
 */
export function buildCommand(project, o) {
  const meta = project.source.meta;
  const W = o.width, H = o.height;
  const fps = project.style?.output?.fps || 30;
  const keep = keepSegments(meta.duration, project.cuts);
  if (!keep.length) throw new UserError('Semua bagian video terpotong.', 'Nonaktifkan beberapa cut agar ada bagian yang tersisa.');
  const outDur = outputDuration(keep);
  const dir = workDir(project.id);
  const assName = `subs_${Date.now()}_${Math.random().toString(36).slice(2, 6)}.ass`;
  // Kartu layar penuh memakai latar kertas bertekstur (overlay PNG) di bawah teks ASS.
  const hfClips = o.hfClips || new Map();
  const fullCards = (project.cards || []).filter((c) => c.approved && c.layout !== 'panel' && !hfClips.has(c.id)).map((c) => mapSpan(c.start, c.end, keep)).filter(Boolean);
  const usePaper = project.style.cards?.paper !== false && fullCards.length > 0;
  fs.writeFileSync(path.join(dir, assName), buildAss(project, { width: W, height: H, keep, paper: usePaper, skipCards: new Set(hfClips.keys()) }));

  const inputs = ['-i', project.source.path];
  let nextInput = 1;
  const f = [];
  const withAudio = o.withAudio !== false;
  const hasAudio = meta.hasAudio;

  // 1+2) Cut & bingkai. Rentang keep dipecah di batas zoom punch-in; tiap potongan
  // di-trim, (pada mode isi) di-scale/crop dengan zoom-nya sendiri, lalu disambung.
  const fr = project.output.reframe || {};
  const fit = project.output.framing === 'fit';
  const pieces = fit ? keep.map((k) => ({ ...k, zoom: 1 })) : zoomPieces(keep, project.zooms);
  const K = pieces.length;
  const audio = withAudio && hasAudio;
  f.push(`[0:v]split=${K}${pieces.map((_, i) => `[vs${i}]`).join('')}`);
  if (audio) f.push(`[0:a]asplit=${K}${pieces.map((_, i) => `[as${i}]`).join('')}`);
  pieces.forEach((k, i) => {
    let frame = '';
    if (!fit) {
      const c = framing(meta.width, meta.height, W, H, { ...fr, zoom: (fr.zoom || 1) * k.zoom });
      frame = `,fps=${fps},scale=${c.sw}:${c.sh}:flags=lanczos,crop=${W}:${H}:${c.cx}:${c.cy},setsar=1`;
    }
    f.push(`[vs${i}]trim=start=${k.start}:end=${k.end},setpts=PTS-STARTPTS${frame}[v${i}]`);
    if (audio) f.push(`[as${i}]atrim=start=${k.start}:end=${k.end},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo[a${i}]`);
  });
  const joined = fit ? 'vc' : 'vf';
  if (audio) f.push(`${pieces.map((_, i) => `[v${i}][a${i}]`).join('')}concat=n=${K}:v=1:a=1[${joined}][voice0]`);
  else f.push(`${pieces.map((_, i) => `[v${i}]`).join('')}concat=n=${K}:v=1:a=0[${joined}]`);

  if (fit) {
    const fitScale = Math.min(W / meta.width, H / meta.height);
    const fw = Math.floor((meta.width * fitScale) / 2) * 2, fh = Math.floor((meta.height * fitScale) / 2) * 2;
    const cover = framing(meta.width, meta.height, W, H, { x: 0.5, y: 0.5, zoom: 1 });
    f.push(`[vc]fps=${fps},split[bgsrc][fgsrc]`);
    f.push(`[bgsrc]scale=${cover.sw}:${cover.sh},crop=${W}:${H}:${cover.cx}:${cover.cy},boxblur=20:2,eq=brightness=-0.08[bg]`);
    f.push(`[fgsrc]scale=${fw}:${fh}[fg]`);
    f.push(`[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1[vf]`);
  }

  // 3) Koreksi warna terukur.
  let cur = 'vf';
  const col = project.style.color;
  if (col?.enabled) {
    const i = Math.min(1, Math.max(0, col.intensity ?? 0.5));
    const eq = `eq=brightness=${r3((col.brightness || 0) * i)}:contrast=${r3(1 + ((col.contrast ?? 1) - 1) * i)}:saturation=${r3(1 + ((col.saturation ?? 1) - 1) * i)}:gamma=${r3(1 + ((col.gamma ?? 1) - 1) * i)}`;
    const w = (col.warmth || 0) * i;
    const cb = `colorbalance=rm=${r3(w * 0.6)}:bm=${r3(-w * 0.6)}:rh=${r3(w * 0.3)}:bh=${r3(-w * 0.3)}`;
    const vig = col.vignette > 0 ? `,vignette=a=${r3(col.vignette * i * (Math.PI / 4))}` : '';
    f.push(`[${cur}]${eq},${cb}${vig}[vcol]`);
    cur = 'vcol';
  }

  // 4) B-roll milik pengguna (hanya yang disetujui & asetnya ada).
  let bi = 0;
  for (const b of project.broll || []) {
    const a = b.approved && b.assetId && assetById(project, b.assetId);
    if (!a || a.missing) continue;
    const span = mapSpan(b.start, b.end, keep);
    if (!span) continue;
    const d = r3(span.end - span.start);
    if (a.kind === 'image') inputs.push('-loop', '1', '-t', String(d + 0.1), '-i', a.path);
    else inputs.push('-i', a.path);
    const idx = nextInput++;
    const c = framing(a.meta?.width || W, a.meta?.height || H, W, H, { x: 0.5, y: 0.5, zoom: 1 });
    const fd = Math.min(0.2, d / 4);
    f.push(`[${idx}:v]fps=${fps},scale=${c.sw}:${c.sh},crop=${W}:${H}:${c.cx}:${c.cy},setsar=1,trim=duration=${d},format=yuva420p,fade=t=in:st=0:d=${fd}:alpha=1,fade=t=out:st=${r3(d - fd)}:d=${fd}:alpha=1,setpts=PTS-STARTPTS+${span.start}/TB[br${bi}]`);
    f.push(`[${cur}][br${bi}]overlay=0:0:eof_action=pass:enable='between(t,${span.start},${span.end})'[vb${bi}]`);
    cur = `vb${bi}`;
    bi++;
  }

  // 4b) Latar kertas untuk kartu layar penuh (potong keras seperti referensi).
  if (usePaper) {
    inputs.push('-loop', '1', '-framerate', String(fps), '-t', String(outDur), '-i', paperFile(W, H, project.style.colors?.cardBg));
    const pi = nextInput++;
    const enable = fullCards.map((c) => `between(t,${r3(c.start)},${r3(c.end)})`).join('+');
    f.push(`[${pi}:v]format=yuv420p,setsar=1[paper]`);
    f.push(`[${cur}][paper]overlay=0:0:eof_action=pass:enable='${enable}'[vpaper]`);
    cur = 'vpaper';
  }

  // 4c) Kartu grafis HyperFrames (klip MP4 per kartu) — potong keras di waktu kartu.
  let hi = 0;
  for (const clip of hfClips.values()) {
    inputs.push('-i', clip.file);
    const idx = nextInput++;
    f.push(`[${idx}:v]fps=${fps},scale=${W}:${H},setsar=1,format=yuv420p,setpts=PTS-STARTPTS+${r3(clip.start)}/TB[hf${hi}]`);
    f.push(`[${cur}][hf${hi}]overlay=0:0:eof_action=pass:enable='between(t,${r3(clip.start)},${r3(clip.end)})'[vhf${hi}]`);
    cur = `vhf${hi}`;
    hi++;
  }

  // 5) Subtitle + kartu (ASS).
  const fontsRel = path.relative(dir, config.fontsDir).split(path.sep).join('/');
  const fontsArg = /[:'\\,\[\];]/.test(fontsRel) ? '' : `:fontsdir=${fontsRel}`;
  f.push(`[${cur}]ass=${assName}${fontsArg},format=yuv420p[vout]`);

  // 6) Audio: suara asli + musik (ducking) + SFX.
  const mix = [];
  if (withAudio) {
    if (hasAudio) {
      const a = project.style.audio || {};
      const chain = [];
      if (a.highpass) chain.push('highpass=f=80');
      if (a.voiceGainDb) chain.push(`volume=${a.voiceGainDb}dB`);
      if (a.normalize) chain.push('loudnorm=I=-14:TP=-1.5:LRA=11');
      chain.push('aresample=48000');
      const music = project.music?.enabled && assetById(project, project.music.assetId);
      const duck = music && !music.missing && a.ducking;
      f.push(`[voice0]${chain.join(',')}${duck ? ',asplit=2[voice][vkey]' : '[voice]'}`);
      mix.push('[voice]');
      if (music && !music.missing) {
        inputs.push('-stream_loop', '-1', '-i', music.path);
        const mi = nextInput++;
        const fi = project.music.fadeIn ?? 1, fo = project.music.fadeOut ?? 1.5;
        const st0 = Math.max(0, Number(project.music.startAt) || 0);
        f.push(`[${mi}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:${r3(outDur - st0)},asetpts=PTS-STARTPTS,volume=${dbToLin(project.music.volumeDb ?? -24)},afade=t=in:d=${fi},afade=t=out:st=${r3(Math.max(0, outDur - st0 - fo))}:d=${fo}${st0 ? `,adelay=${Math.round(st0 * 1000)}:all=1` : ''}[mus]`);
        if (duck) {
          f.push('[mus][vkey]sidechaincompress=threshold=0.04:ratio=8:attack=15:release=350[musd]');
          mix.push('[musd]');
        } else mix.push('[mus]');
      }
    } else {
      inputs.push('-f', 'lavfi', '-t', String(outDur), '-i', 'anullsrc=r=48000:cl=stereo');
      mix.push(`[${nextInput++}:a]`);
    }
    let si = 0;
    for (const s of project.sfx || []) {
      if (!s.approved) continue;
      const t = mapTime(s.time, keep);
      if (t === null) continue;
      const gain = dbToLin((project.style.audio?.sfxDb ?? -12) + (s.volumeDb || 0));
      if (s.builtin && isLibraryItem('sfx', s.builtin)) {
        inputs.push('-i', libraryFile('sfx', s.builtin));
        f.push(`[${nextInput++}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=${gain},adelay=${Math.round(t * 1000)}:all=1[sfx${si}]`);
      } else {
        const a = s.assetId && assetById(project, s.assetId);
        if (!a || a.missing) continue;
        inputs.push('-i', a.path);
        f.push(`[${nextInput++}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=${gain},adelay=${Math.round(t * 1000)}:all=1[sfx${si}]`);
      }
      mix.push(`[sfx${si++}]`);
    }
    f.push(`${mix.join('')}amix=inputs=${mix.length}:duration=first:dropout_transition=0:normalize=0,alimiter=limit=0.95,aresample=48000[aout]`);
  }

  // Graph dikirim langsung sebagai argumen (tanpa shell). -filter_complex_script tidak dipakai
  // karena sudah usang/dihapus di ffmpeg versi baru. Salinan graph disimpan untuk diagnosis.
  const graphFile = path.join(dir, assName.replace('.ass', '.graph.txt'));
  const graph = f.join(';');
  fs.writeFileSync(graphFile, graph);

  // Batas panjang baris perintah Windows ±32 rb karakter: graph sangat panjang dibaca dari file
  // (sintaks "-/filter_complex <file>" ffmpeg ≥ 7, atau -filter_complex_script untuk versi lama).
  const graphArgs = graph.length < 20000 ? ['-filter_complex', graph] : ffmpegMajor() >= 7 ? ['-/filter_complex', graphFile] : ['-filter_complex_script', graphFile];
  const args = ['-hide_banner', '-y', '-nostdin', ...inputs, ...graphArgs, '-map', '[vout]'];
  if (o.stillAt !== undefined) {
    args.push('-ss', String(Math.max(0, Math.min(outDur - 0.05, o.stillAt))), '-frames:v', '1', '-update', '1', o.outFile);
    return { args, cwd: dir, outDur, keep, tempFiles: [path.join(dir, assName), graphFile] };
  }
  const q = QUALITY[o.quality] || QUALITY.standar;
  if (withAudio) args.push('-map', '[aout]', '-c:a', 'aac', '-b:a', q.audio);
  args.push('-c:v', 'libx264', '-preset', q.preset, '-crf', String(q.crf), '-pix_fmt', 'yuv420p', '-r', String(fps));
  if (o.container !== 'mov') args.push('-movflags', '+faststart');
  args.push('-t', String(outDur), '-progress', 'pipe:1', '-nostats', o.outFile);
  return { args, cwd: dir, outDur, keep, tempFiles: [path.join(dir, assName), graphFile] };
}

async function ffmpegInDir(args, cwd, { onProgress, outDur, signal } = {}) {
  const { spawn } = await import('node:child_process');
  return new Promise((resolve, reject) => {
    const child = spawn('ffmpeg', args, { cwd, stdio: ['ignore', 'pipe', 'pipe'], signal });
    let stderr = '';
    child.stdout.on('data', (d) => {
      const m = d.toString().match(/out_time_(?:us|ms)=(\d+)/g);
      if (m && outDur) {
        const us = Number(m[m.length - 1].split('=')[1]);
        onProgress?.(Math.min(0.99, us / 1e6 / outDur));
      }
    });
    child.stderr.on('data', (d) => (stderr = (stderr + d.toString()).slice(-12000)));
    child.on('error', (e) => reject(e.name === 'AbortError' ? e : new UserError('ffmpeg tidak dapat dijalankan.', 'Pastikan ffmpeg terpasang dan ada di PATH.', 500)));
    child.on('close', (code) => resolve({ code, stderr }));
  });
}

function explainFfmpegError(stderr) {
  const tail = stderr.split('\n').filter((l) => /error|invalid|no such|not found|failed|cannot/i.test(l)).slice(-4).join(' | ');
  return tail || stderr.split('\n').slice(-4).join(' | ');
}

function timestamp() {
  const d = new Date();
  const p = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}${p(d.getMonth() + 1)}${p(d.getDate())}-${p(d.getHours())}${p(d.getMinutes())}${p(d.getSeconds())}`;
}

export function slug(s) {
  return String(s).toLowerCase().normalize('NFKD').replace(/[^\w\s-]/g, '').trim().replace(/[\s_]+/g, '-').slice(0, 50) || 'proyek';
}

export function resolveOutputDir(project, customDir) {
  let dir = customDir ? path.resolve(customDir) : path.join(config.outputDir, slug(project.name));
  if (customDir) {
    if (!fs.existsSync(dir) || !fs.statSync(dir).isDirectory()) throw new UserError('Folder output tidak ditemukan.', `Buat foldernya dulu: ${dir}`);
    if (project.source && path.resolve(path.dirname(project.source.path)) === dir) {
      throw new UserError('Folder output tidak boleh sama dengan folder video sumber.', 'Pilih folder terpisah agar file asli tetap aman.');
    }
  }
  fs.mkdirSync(dir, { recursive: true });
  try {
    fs.accessSync(dir, fs.constants.W_OK);
  } catch {
    throw new UserError('Folder output tidak dapat ditulisi.', `Periksa izin folder: ${dir}`);
  }
  return dir;
}

/**
 * Siapkan klip HyperFrames untuk kartu layar penuh (bila mesin grafis = hyperframes).
 * Gagal → kartu bawaan (ASS) dipakai dan alasannya dicatat; render tidak dibatalkan.
 * onlyAt: hanya kartu yang tampil pada waktu output itu (untuk frame pratinjau).
 */
async function cardClips(project, { W, H, job, onlyAt } = {}) {
  if ((project.style.cards?.engine ?? 'hyperframes') !== 'hyperframes') return { clips: new Map(), note: null };
  const st = hyperframesStatus();
  if (!st.ok) return { clips: new Map(), note: `Grafis HyperFrames tidak dipakai: ${st.detail} Kartu bawaan dipakai.` };
  const keep = keepSegments(project.source.meta.duration, project.cuts);
  const spans = (project.cards || [])
    .filter((c) => c.approved && c.layout !== 'panel')
    .map((card) => ({ card, span: mapSpan(card.start, card.end, keep) }))
    .filter((x) => x.span && x.span.end - x.span.start >= 0.3 && (onlyAt === undefined || (onlyAt >= x.span.start && onlyAt < x.span.end)));
  if (!spans.length) return { clips: new Map(), note: null };
  try {
    const clips = await prepareCardClips(project, { W, H, fps: project.style?.output?.fps || 30, spans, job, signal: job?.controller?.signal });
    return { clips, note: null };
  } catch (e) {
    if (job?.controller?.signal?.aborted) throw e;
    console.error('[hyperframes]', e.message);
    return { clips: new Map(), note: `Grafis HyperFrames gagal dirender (${e.message.slice(0, 200)}). Kartu bawaan dipakai. Jalankan "npx hyperframes doctor" untuk memeriksa Chrome.` };
  }
}

/** Render penuh (ekspor atau pratinjau cepat). Status sukses hanya setelah file diverifikasi. */
export async function renderVideo(project, job, { aspect = '9:16', quality = 'standar', container = 'mp4', outDir, preview = false }) {
  const fmt = OUTPUT_FORMATS[aspect];
  if (!fmt) throw new UserError('Rasio output tidak dikenal.');
  const scale = preview ? 0.5 : 1;
  const W = Math.round((fmt.width * scale) / 2) * 2, H = Math.round((fmt.height * scale) / 2) * 2;
  const ext = (CONTAINERS[container] || CONTAINERS.mp4).ext;
  const dir = preview ? workDir(project.id) : resolveOutputDir(project, outDir);
  const base = preview ? `pratinjau_${timestamp()}` : `${slug(project.name)}_${aspect.replace(':', 'x')}_${quality}_${timestamp()}`;
  let outFile = path.join(dir, base + ext);
  for (let n = 2; fs.existsSync(outFile); n++) outFile = path.join(dir, `${base}_${n}${ext}`);
  const tmpFile = outFile.replace(ext, `.part${ext}`);

  const { clips, note } = await cardClips(project, { W, H, job });
  const cmd = buildCommand(project, { width: W, height: H, quality: preview ? 'pratinjau' : quality, container, outFile: tmpFile, hfClips: clips });
  job.message = 'Merender…';
  const res = await ffmpegInDir(cmd.args, cmd.cwd, { outDur: cmd.outDur, signal: job.controller.signal, onProgress: (p) => (job.progress = p) });
  for (const t of cmd.tempFiles) fs.rmSync(t, { force: true });
  if (res.code !== 0) {
    fs.rmSync(tmpFile, { force: true });
    if (job.controller.signal.aborted) throw new UserError('Render dibatalkan.');
    throw new UserError('Render gagal.', `Detail ffmpeg: ${explainFfmpegError(res.stderr)}`, 500);
  }
  // Verifikasi: file ada, dapat dibaca ffprobe, durasi sesuai, dan frame dapat didekode.
  job.message = 'Memverifikasi file output…';
  if (!fs.existsSync(tmpFile) || fs.statSync(tmpFile).size < 1000) throw new UserError('File output tidak terbentuk.', 'Coba render ulang; periksa ruang disk.', 500);
  const meta = await probe(tmpFile);
  if (!meta.hasVideo || Math.abs(meta.duration - cmd.outDur) > 1.0) {
    throw new UserError('File output tidak lolos verifikasi.', `Durasi ${meta.duration.toFixed(2)} dtk, diharapkan ${cmd.outDur.toFixed(2)} dtk.`, 500);
  }
  const dec = await run('ffmpeg', ['-v', 'error', '-ss', String(Math.max(0, meta.duration / 2)), '-i', tmpFile, '-frames:v', '1', '-f', 'null', '-'], { timeoutMs: 60000 });
  if (dec.code !== 0) throw new UserError('File output tidak dapat didekode.', 'Coba render ulang.', 500);
  fs.renameSync(tmpFile, outFile);
  return { path: outFile, size: fs.statSync(outFile).size, duration: meta.duration, width: meta.width, height: meta.height, aspect, quality: preview ? 'pratinjau' : quality, container, graphics: clips.size ? `HyperFrames (${clips.size} kartu)` : 'bawaan', note };
}

/** Render satu frame PNG pada waktu output tertentu — pipeline identik dengan ekspor. */
export async function renderStill(project, { aspect = '9:16', sourceTime = 0 }) {
  const fmt = OUTPUT_FORMATS[aspect] || OUTPUT_FORMATS['9:16'];
  const keep = keepSegments(project.source.meta.duration, project.cuts);
  let t = mapTime(sourceTime, keep);
  if (t === null) {
    const next = keep.find((k) => k.start > sourceTime);
    t = next ? mapTime(next.start, keep) : 0;
  }
  const W = Math.round(fmt.width / 2 / 2) * 2, H = Math.round(fmt.height / 2 / 2) * 2;
  const outFile = path.join(workDir(project.id), `frame_${Date.now()}.png`);
  const { clips, note } = await cardClips(project, { W, H, onlyAt: t });
  const cmd = buildCommand(project, { width: W, height: H, stillAt: t, withAudio: false, outFile, hfClips: clips });
  const res = await ffmpegInDir(cmd.args, cmd.cwd, {});
  for (const f of cmd.tempFiles) fs.rmSync(f, { force: true });
  if (res.code !== 0 || !fs.existsSync(outFile)) throw new UserError('Frame pratinjau gagal dirender.', explainFfmpegError(res.stderr), 500);
  return { file: outFile, outputTime: t, note };
}

export function estimateSize(project, quality, aspect) {
  const keep = keepSegments(project.source?.meta?.duration || 0, project.cuts);
  const d = outputDuration(keep);
  const q = QUALITY[quality] || QUALITY.standar;
  const px = (OUTPUT_FORMATS[aspect] || OUTPUT_FORMATS['9:16']).width * (OUTPUT_FORMATS[aspect] || OUTPUT_FORMATS['9:16']).height;
  const mbps = q.estMbps * (px / (1080 * 1920));
  return { durationSec: d, approxBytes: Math.round(((mbps + 0.16) * 1e6 * d) / 8) };
}
