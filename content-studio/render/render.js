#!/usr/bin/env node
// Render carousel dari file JSON jadi PNG 1080x1350, tanpa membuka browser.
//
// Pakai (dari folder proyek):
//   node render/render.js posts/harga-ditawar.json
//   node render/render.js posts/*.json              -> semua post sekaligus
//   node render/render.js posts/a.json --out hasil  -> folder hasil lain (default: out/)
//
// Foto: isi "photos" di JSON, kunci = nomor slide (1-8), nilai = path file relatif terhadap JSON.
//   "photos": { "1": "../foto/cover.jpg", "2": "../foto/etching-s2.png" }
// Slide memakai kode desain yang sama dengan Studio (content-studio.html), jadi hasilnya identik.
const fs = require('fs');
const path = require('path');

let chromium;
try { ({ chromium } = require('playwright')); }
catch (e) {
  console.error('Playwright belum terpasang. Jalankan dulu:\n  npm install\n  npx playwright install chromium');
  process.exit(1);
}

const ROOT = path.join(__dirname, '..');
const APP = path.join(ROOT, 'content-studio.html');
const MIME = { '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp' };

function slug(s) {
  return String(s || 'carousel').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'carousel';
}

function readPost(file) {
  const post = JSON.parse(fs.readFileSync(file, 'utf8'));
  if (!Array.isArray(post.slides) || !post.slides.length) throw new Error('JSON tidak punya "slides"');
  const photos = {};
  for (const [k, rel] of Object.entries(post.photos || {})) {
    if (k.startsWith('_') || !rel) continue;
    const n = parseInt(k, 10);
    if (!(n >= 1 && n <= post.slides.length)) throw new Error('Nomor slide foto tidak valid: ' + k);
    const p = path.resolve(path.dirname(file), rel);
    if (!fs.existsSync(p)) throw new Error('Foto slide ' + n + ' tidak ditemukan: ' + p);
    const mime = MIME[path.extname(p).toLowerCase()];
    if (!mime) throw new Error('Format foto slide ' + n + ' tidak didukung (pakai jpg, png, webp): ' + p);
    photos[n - 1] = 'data:' + mime + ';base64,' + fs.readFileSync(p).toString('base64');
  }
  delete post.photos;
  return { post, photos };
}

(async () => {
  const args = process.argv.slice(2);
  let out = path.join(ROOT, 'out');
  const files = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--out') out = path.resolve(args[++i]);
    else files.push(args[i]);
  }
  if (!files.length) {
    console.error('Pakai: node render/render.js posts/nama-post.json [--out folder]');
    process.exit(1);
  }

  const browser = await chromium.launch();
  let failed = 0;
  try {
    for (const file of files) {
      const t0 = Date.now();
      let data;
      try { data = readPost(file); }
      catch (e) { console.error('✗ ' + file + ': ' + e.message); failed++; continue; }

      const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
      const errs = [];
      page.on('pageerror', (e) => errs.push(e.message));
      await page.route(/^https?:/, (r) => r.abort()); // semua aset sudah tertanam: tidak butuh internet
      await page.addInitScript(() => { window.__CS_RENDER__ = true; });
      await page.goto('file://' + APP);

      const n = await page.evaluate(([p, ph]) => window.CSRender.load(p, ph), [data.post, data.photos]);
      const dir = path.join(out, slug(data.post.title));
      fs.mkdirSync(dir, { recursive: true });
      for (let i = 0; i < n; i++) {
        await page.evaluate((k) => window.CSRender.show(k), i);
        await page.screenshot({ path: path.join(dir, 'slide-' + String(i + 1).padStart(2, '0') + '.png'), clip: { x: 0, y: 0, width: 1080, height: 1350 } });
      }
      await page.close();
      if (errs.length) { console.error('✗ ' + file + ': error di halaman: ' + errs.join(' | ')); failed++; continue; }
      console.log('✓ ' + n + ' slide → ' + path.relative(process.cwd(), dir) + '  (' + ((Date.now() - t0) / 1000).toFixed(1) + ' dtk)');
    }
  } finally {
    await browser.close();
  }
  process.exit(failed ? 1 : 0);
})();
