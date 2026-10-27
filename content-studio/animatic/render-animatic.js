#!/usr/bin/env node
// Render animatic.html jadi MP4 1080x1920 30 fps: Chromium (Playwright) memotret tiap frame lewat window.seek(t),
// ffmpeg menyatukannya. Teknik yang sama dengan HyperFrames, tanpa paket tambahan.
//
// Pakai: node animatic/render-animatic.js [--file animatic-v3.html] [--fps 30] [--out out/animatic.mp4] [--audio vo.wav] [--stills 2.5]
//   --beats   : timing.json dari vo_prep.py (durasi langkah + waktu kata mengikuti voice over)
//   --audio   : voice over Anda, digabung ke video (durasi video mengikuti animatic)
//   --stills  : simpan lembar kontak (still tiap N detik) untuk QC
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const { chromium } = require('playwright');

const ROOT = path.join(__dirname, '..');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > -1 ? process.argv[i + 1] : d; };
const FPS = +arg('fps', 30);
const OUT = path.resolve(arg('out', path.join(ROOT, 'out', 'animatic.mp4')));
const AUDIO = arg('audio', '');
const STILLS = +arg('stills', 0);

(async () => {
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const errs = [];
  pg.on('pageerror', (e) => errs.push(e.message));
  await pg.route(/^https?:/, (r) => r.abort());
  const BEATS = arg('beats', '');
  if (BEATS) { const tl = JSON.parse(fs.readFileSync(BEATS, 'utf8')); await pg.addInitScript((b) => { window.ANIMATIC_BEATS = b; }, tl.beats); }
  const ANCH = path.join(__dirname, arg('file', 'animatic.html').replace(/^animatic(-v\d+)?\.html$/, 'anchors$1.json'));
  if (BEATS && fs.existsSync(ANCH)) await pg.addInitScript((a) => { window.ANIMATIC_ANCHORS = a; }, JSON.parse(fs.readFileSync(ANCH, 'utf8')));
  await pg.goto('file://' + path.join(__dirname, arg('file', 'animatic.html')));
  await pg.addStyleTag({ path: path.join(ROOT, 'assets', 'fonts-embed.css') });
  await pg.evaluate(() => Promise.all(['800 40px Archivo', 'italic 400 40px Fraunces', '600 40px Outfit', '600 40px Caveat', '500 40px "JetBrains Mono"'].map((f) => document.fonts.load(f))));
  const dur = await pg.evaluate(() => window.ANIMATIC_DURATION);
  const n = Math.round(dur * FPS);

  const ff = ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-'];
  if (AUDIO) ff.push('-i', AUDIO, '-c:a', 'aac', '-b:a', '192k', '-shortest');
  ff.push('-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', '-movflags', '+faststart', OUT);
  const enc = spawn('ffmpeg', ff, { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise((ok, no) => enc.on('close', (c) => (c ? no(new Error('ffmpeg keluar ' + c)) : ok())));

  const stills = [];
  const t0 = Date.now();
  for (let i = 0; i < n; i++) {
    const t = i / FPS;
    await pg.evaluate((x) => window.seek(x), t);
    const buf = await pg.screenshot({ type: 'jpeg', quality: 92 });
    if (!enc.stdin.write(buf)) await new Promise((r) => enc.stdin.once('drain', r));
    if (STILLS && Math.abs(t - Math.round(t / STILLS) * STILLS) < 0.5 / FPS) stills.push(buf);
    if (i % (FPS * 5) === 0) process.stdout.write('\r' + Math.round((i / n) * 100) + '% ');
  }
  enc.stdin.end();
  await done;
  if (STILLS) {
    const dir = OUT.replace(/\.mp4$/, '') + '_stills';
    fs.mkdirSync(dir, { recursive: true });
    stills.forEach((s, i) => fs.writeFileSync(path.join(dir, 'still-' + String(i).padStart(2, '0') + '.jpg'), s));
  }
  await b.close();
  console.log('\r✓ ' + n + ' frame (' + dur.toFixed(1) + ' dtk) → ' + path.relative(process.cwd(), OUT) + '  [' + ((Date.now() - t0) / 1000).toFixed(0) + ' dtk render]' + (errs.length ? '  ERROR: ' + errs.join(' | ') : ''));
})();
