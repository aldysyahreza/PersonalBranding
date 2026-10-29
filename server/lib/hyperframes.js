// Mesin kartu grafis HyperFrames (HeyGen, open source): setiap kartu layar penuh ditulis
// sebagai komposisi HTML + GSAP, dirender ke MP4 oleh Chrome headless, lalu ditumpuk
// oleh ffmpeg pada waktu kartu. Hasil di-cache per isi kartu + gaya + ukuran.
// Bila HyperFrames/Chrome tidak tersedia, render memakai kartu bawaan (ASS) — tidak gagal diam-diam.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawn } from 'node:child_process';
import { createRequire } from 'node:module';
import { config, ROOT } from './config.js';
import { workDir } from './projects.js';
import { resolveIcon } from '../../public/shared/icons.js';
import { shade } from './ass.js';
import { measure } from './fontmetrics.js';
import { brandFixerHtml, BF_FONTS } from './hf-brandfixer.js';

const require = createRequire(import.meta.url);
const TEMPLATE_VERSION = 4;
const ICON_DIR = path.join(ROOT, 'assets', 'icons');

let availability = null;
/** { ok, detail } — paket hyperframes & gsap terpasang? (Chrome dicek/diunduh oleh hyperframes saat render). */
export function hyperframesStatus() {
  if (availability) return availability;
  try {
    const pkg = require.resolve('hyperframes/package.json');
    const gsap = require.resolve('gsap/dist/gsap.min.js');
    const version = JSON.parse(fs.readFileSync(pkg, 'utf8')).version;
    const nodeMajor = Number(process.versions.node.split('.')[0]);
    if (nodeMajor < 22) availability = { ok: false, detail: `HyperFrames butuh Node.js ≥ 22 (terpasang ${process.versions.node}).` };
    else availability = { ok: true, detail: `HyperFrames ${version}`, bin: path.join(path.dirname(pkg), 'bin', 'hyperframes.mjs'), gsap };
  } catch {
    availability = { ok: false, detail: 'Paket hyperframes/gsap belum terpasang. Jalankan "npm install".' };
  }
  return availability;
}

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

/** SVG Lucide inline, dengan pathLength=1 agar garisnya bisa "digambar" (stroke-dashoffset). */
function iconSvg(name, cls = '') {
  const file = path.join(ICON_DIR, `${name}.svg`);
  if (!name || !fs.existsSync(file)) return '';
  return fs
    .readFileSync(file, 'utf8')
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/<svg\b/, `<svg class="ic ${cls}"`)
    .replace(/<(path|circle|line|polyline|rect|ellipse|polygon)\b/g, '<$1 pathLength="1"')
    .replace(/\s+/g, ' ')
    .trim();
}

function rgba(hex, a) {
  const m = hex.replace('#', '');
  return `rgba(${parseInt(m.slice(0, 2), 16)},${parseInt(m.slice(2, 4), 16)},${parseInt(m.slice(4, 6), 16)},${a})`;
}

/** Folder kerja HyperFrames per proyek: font & gsap disalin sekali, komposisi kartu di dalamnya. */
export function hfDir(projectId) {
  const dir = path.join(workDir(projectId), 'hf');
  fs.mkdirSync(path.join(dir, 'fonts'), { recursive: true });
  for (const f of ['Montserrat-Medium.ttf', 'Montserrat-Bold.ttf', 'Montserrat-ExtraBold.ttf', 'Montserrat-Black.ttf', 'GreatVibes-Regular.ttf', ...BF_FONTS.map((x) => x[1])]) {
    const dst = path.join(dir, 'fonts', f);
    if (!fs.existsSync(dst)) fs.copyFileSync(path.join(config.fontsDir, f), dst);
  }
  const st = hyperframesStatus();
  const g = path.join(dir, 'gsap.min.js');
  if (st.ok && !fs.existsSync(g)) fs.copyFileSync(st.gsap, g);
  return dir;
}

function hashOf(card, style, W, H, fps, dur, image = '') {
  const key = JSON.stringify([TEMPLATE_VERSION, card.type, card.layout, card.kicker, card.title, card.subtitle, card.icon, card.cta, card.caseTag, card.endcard, image, resolveIcon(card), style.colors, style.cards, style.endcard, W, H, fps, Math.round(dur * 100)]);
  return crypto.createHash('sha1').update(key).digest('hex').slice(0, 12);
}

/** Pecah angka judul ("10K", "1.000", "25%", "Rp 5,5") untuk animasi hitung naik. */
function parseNumber(title) {
  const m = String(title).match(/^(\D*?)(\d[\d.,]*)(.*)$/);
  if (!m) return null;
  const [, pre, num, post] = m;
  const thousands = /^\d{1,3}(\.\d{3})+$/.test(num);
  const decimals = !thousands && /,\d+$/.test(num) ? num.split(',')[1].length : 0;
  const value = thousands ? Number(num.replace(/\./g, '')) : Number(num.replace(/\./g, '').replace(',', '.'));
  return Number.isFinite(value) ? { pre, post, value, thousands, decimals } : null;
}

/** HTML komposisi HyperFrames untuk satu kartu layar penuh. */
export function cardHtml(card, style, { W, H, dur, image = '' }) {
  if ((style.cards?.theme ?? 'reference') === 'brandfixer') {
    const icon = resolveIcon(card);
    return brandFixerHtml(card, style, { W, H, dur, image, icon: icon ? iconSvg(icon, 'draw') : '' });
  }
  const k = Math.min(W, H) / 1080;
  const px = (n) => `${Math.round(n * k)}px`;
  const col = style.colors;
  const accent = col.accent, dark = shade(col.accent, -0.45);
  const side = Math.round(W * (style.safeZone?.side ?? 0.06));
  const icon = resolveIcon(card);
  const titleSize = (style.cards.titleSize ?? 128) * 0.85;
  const seed = parseInt(crypto.createHash('md5').update(card.title || 'x').digest('hex').slice(0, 8), 16);
  const rnd = (i) => ((seed * (i + 7) * 9301 + 49297) % 233280) / 233280;
  const decos = Array.from({ length: 6 }, (_, i) => {
    const kind = ['dot', 'ring', 'plus'][i % 3];
    const x = Math.round((i % 2 ? 0.62 + rnd(i) * 0.3 : 0.06 + rnd(i) * 0.28) * W);
    const y = Math.round((0.2 + rnd(i + 3) * 0.6) * H);
    return `<div class="deco ${kind}" id="deco${i}" style="left:${x}px;top:${y}px"></div>`;
  }).join('');

  let body = '';
  let script = '';
  const kicker = card.kicker ? `<div class="kicker" id="kicker">${esc(card.kicker)}</div>` : '';
  const sub = card.subtitle && card.type !== 'list' ? `<div class="sub" id="sub">${esc(card.subtitle)}</div>` : '';
  const badge = icon ? `<div class="badge" id="badge"><div class="ring" id="ring"></div>${iconSvg(icon, 'draw')}</div>` : '';

  if (card.type === 'number') {
    const n = parseNumber(card.title);
    const len = Math.max(1, String(card.title || '').length);
    const size = Math.min((style.cards.numberSize ?? 340) * 1.6 * k, ((W - side * 2) * 0.72) / (len * 0.66));
    const extrude = Array.from({ length: 8 }, (_, i) => `${Math.round((i + 1) * 1.1 * k)}px ${Math.round((i + 1) * 1.8 * k)}px 0 ${dark}`).join(',');
    body = `
      ${icon ? `<div class="chip" id="badge">${iconSvg(icon, 'draw')}</div>` : ''}
      ${kicker}
      <div class="numwrap"><div class="numblock" id="numblock"></div>
        <div class="num" id="num" style="font-size:${Math.round(size)}px;text-shadow:${extrude},${px(18)} ${px(34)} ${px(30)} rgba(0,0,0,.28)">${esc(card.title)}</div></div>
      ${sub}`;
    script = `
      tl.fromTo('#num', { scale: 1.45, opacity: 0, filter: 'blur(14px)' }, { scale: 1, opacity: 1, filter: 'blur(0px)', duration: 0.42, ease: 'expo.out' }, 0.08);
      tl.fromTo('#numblock', { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: 'power3.out' }, 0.32);
      ${n ? `const N = ${JSON.stringify(n)}; const o = { v: 0 };
      tl.to(o, { v: N.value, duration: 0.85, ease: 'power2.out', onUpdate: () => {
        const v = N.thousands ? Math.round(o.v).toLocaleString('id-ID') : o.v.toFixed(N.decimals).replace('.', ',');
        document.getElementById('num').textContent = N.pre + v + N.post;
      } }, 0.08);` : ''}`;
  } else if (card.type === 'list') {
    const items = String(card.subtitle || '').split(/\s*[;|]\s*/).filter(Boolean).slice(0, 5);
    body = `
      ${badge}${kicker}
      <div class="ltitle" id="ltitle">${esc(card.title)}<div class="bar" id="bar"></div></div>
      <div class="items">${items.map((it, i) => `<div class="item" id="item${i}">${iconSvg('circle-check', 'draw')}<span>${esc(it)}</span></div>`).join('')}</div>`;
    script = `
      tl.fromTo('#ltitle', { y: ${-20 * k}, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: 'power3.out' }, 0.1);
      tl.fromTo('#bar', { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: 'power3.out' }, 0.3);
      ${items.map((_, i) => `tl.fromTo('#item${i}', { x: ${-50 * k}, opacity: 0 }, { x: 0, opacity: 1, duration: 0.35, ease: 'power3.out' }, ${0.45 + i * 0.28});
      tl.to('#item${i} .draw > *', { strokeDashoffset: 0, duration: 0.4, ease: 'power2.out' }, ${0.5 + i * 0.28});`).join('\n')}`;
  } else {
    const lines = wrapForWidth(card.title || '', W - side * 2, titleSize * k);
    body = `
      ${badge}${kicker}
      <div class="title">${lines.map((l, i) => `<div><span class="ln" id="ln${i}">${esc(l)}</span></div>`).join('')}</div>
      <svg class="under" id="under" viewBox="0 0 400 40" preserveAspectRatio="none"><path pathLength="1" d="M6 30 C 120 6, 280 6, 394 22"/></svg>
      ${sub}`;
    script = `
      ${lines.map((_, i) => `tl.fromTo('#ln${i}', { clipPath: 'inset(-40% 100% -40% -8%)' }, { clipPath: 'inset(-40% -8% -40% -8%)', duration: 0.38, ease: 'power3.out' }, ${0.22 + i * 0.12});`).join('\n')}
      tl.to('#under path', { strokeDashoffset: 0, duration: 0.45, ease: 'power2.inOut' }, ${0.5 + lines.length * 0.12});
      ${card.cta ? `tl.to('#badge', { y: ${-14 * k}, duration: 0.32, ease: 'sine.inOut', yoyo: true, repeat: 5 }, 0.7);` : ''}`;
  }

  const fontFace = [['Medium', 500], ['Bold', 700], ['ExtraBold', 800], ['Black', 900]]
    .map(([w, n]) => `@font-face{font-family:'Montserrat';src:url(fonts/Montserrat-${w}.ttf);font-weight:${n}}`).join('') +
    `@font-face{font-family:'Great Vibes';src:url(fonts/GreatVibes-Regular.ttf)}`;

  return `<!doctype html>
<html><head><meta charset="utf-8"><style>
${fontFace}
html,body{margin:0;width:${W}px;height:${H}px;overflow:hidden;background:${col.cardBg}}
#root{position:relative;width:${W}px;height:${H}px;overflow:hidden;font-family:'Montserrat',sans-serif;
  background:
    linear-gradient(118deg, rgba(255,255,255,.75) 0 14%, rgba(255,255,255,0) 26% 46%, rgba(255,255,255,.55) 58%, rgba(255,255,255,0) 72%),
    radial-gradient(ellipse at 55% 42%, rgba(255,255,255,.6), rgba(0,0,0,.06) 85%), ${col.cardBg}}
#stage{position:absolute;inset:0;transform-origin:50% 47%}
.grid{position:absolute;left:50%;top:47%;width:${px(820)};height:${px(560)};transform:translate(-50%,-50%);opacity:0;
  background-image:linear-gradient(rgba(0,0,0,.07) ${px(2)},transparent ${px(2)}),linear-gradient(90deg,rgba(0,0,0,.07) ${px(2)},transparent ${px(2)});
  background-size:${px(56)} ${px(56)};-webkit-mask-image:radial-gradient(ellipse at center,#000 55%,transparent 80%)}
.sweep{position:absolute;top:-20%;height:140%;width:35%;left:-60%;transform:skewX(-20deg);background:linear-gradient(90deg,transparent,rgba(255,255,255,.65),transparent)}
.deco{position:absolute;opacity:0}
.deco.dot{width:${px(16)};height:${px(16)};border-radius:50%;background:${accent}}
.deco.ring{width:${px(34)};height:${px(34)};border-radius:50%;border:${px(4)} solid ${rgba(accent, 0.7)}}
.deco.plus{width:${px(30)};height:${px(30)};background:linear-gradient(${accent},${accent}) center/100% ${px(5)} no-repeat,linear-gradient(${accent},${accent}) center/${px(5)} 100% no-repeat}
.center{position:absolute;left:${side}px;right:${side}px;top:47%;transform:translateY(-50%);display:flex;flex-direction:column;align-items:center;text-align:center;gap:${px(26)}}
.badge{position:relative;width:${px(190)};height:${px(190)};border-radius:50%;background:${accent};display:grid;place-items:center;box-shadow:0 ${px(18)} ${px(40)} ${rgba(accent, 0.35)}}
.badge .ic{width:${px(104)};height:${px(104)};color:#fff;stroke-width:2.2}
.ring{position:absolute;inset:0;border-radius:50%;border:${px(5)} solid ${accent}}
.chip{width:${px(120)};height:${px(120)};border-radius:${px(30)};background:${rgba(accent, 0.1)};display:grid;place-items:center}
.chip .ic{width:${px(70)};height:${px(70)};color:${accent};stroke-width:2.3}
.draw > *{stroke-dasharray:1;stroke-dashoffset:1}
.kicker{font-weight:500;font-size:${px(46)};color:${col.cardMuted};line-height:1.2}
.title{display:flex;flex-direction:column;align-items:center}
.ln{display:inline-block;background:${accent};color:#fff;font-weight:800;font-size:${Math.round(titleSize * k)}px;line-height:1.16;padding:${px(4)} ${px(26)};margin:${px(6)} 0;box-shadow:${px(14)} ${px(14)} 0 ${dark};letter-spacing:-0.01em}
.under{width:${px(420)};height:${px(42)};margin-top:${px(-6)}}
.under path{fill:none;stroke:${accent};stroke-width:7;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:1}
.sub{font-weight:600;font-size:${px(48)};color:${col.cardText}}
.numwrap{position:relative;display:grid;place-items:center}
.numblock{position:absolute;right:${px(-30)};top:38%;width:46%;height:34%;background:${rgba(accent, 0.45)};transform-origin:left center}
.num{position:relative;font-weight:900;color:${accent};line-height:1;letter-spacing:-0.02em}
.ltitle{position:relative;font-weight:900;font-size:${Math.round(titleSize * 0.85 * k)}px;color:${col.cardText};padding-bottom:${px(16)}}
.bar{position:absolute;left:20%;right:20%;bottom:0;height:${px(10)};border-radius:${px(5)};background:${accent};transform-origin:left center}
.items{display:flex;flex-direction:column;align-items:flex-start;gap:${px(26)};margin-top:${px(20)}}
.item{display:flex;align-items:center;gap:${px(22)};font-weight:700;font-size:${px(54)};color:${col.cardText}}
.item .ic{width:${px(64)};height:${px(64)};color:${accent};stroke-width:2.4;flex:none}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="${W}" data-height="${H}" data-start="0" data-duration="${dur.toFixed(3)}">
  <div id="stage">
    <div class="grid" id="grid"></div>
    ${decos}
    <div class="center">${body}</div>
  </div>
  <div class="sweep" id="sweep"></div>
</div>
<script src="gsap.min.js"></script>
<script>
const D = ${dur.toFixed(3)};
const tl = gsap.timeline({ paused: true });
tl.fromTo('#stage', { scale: 1.05 }, { scale: 0.96, duration: D, ease: 'none' }, 0);
tl.to('#grid', { opacity: 1, duration: 0.5 }, 0);
tl.fromTo('#sweep', { left: '-60%' }, { left: '130%', duration: 1.1, ease: 'power1.inOut' }, 0.15);
${decos ? `for (let i = 0; i < 6; i++) {
  tl.fromTo('#deco' + i, { opacity: 0, scale: 0 }, { opacity: 0.55, scale: 1, duration: 0.3, ease: 'back.out(2)' }, 0.25 + i * 0.07);
  tl.to('#deco' + i, { y: (i % 2 ? -1 : 1) * ${Math.round(70 * k)}, x: (i % 3 - 1) * ${Math.round(30 * k)}, rotation: i % 3 === 2 ? 90 : 0, duration: D, ease: 'none' }, 0);
}` : ''}
if (document.getElementById('badge')) {
  tl.fromTo('#badge', { scale: 0, rotation: -35 }, { scale: 1, rotation: 0, duration: 0.5, ease: 'back.out(2.2)' }, 0.05);
  tl.to('#badge .draw > *', { strokeDashoffset: 0, duration: 0.55, ease: 'power2.out' }, 0.2);
}
if (document.getElementById('ring')) tl.fromTo('#ring', { scale: 1, opacity: 0.7 }, { scale: 1.7, opacity: 0, duration: 0.8, ease: 'power2.out' }, 0.35);
if (document.getElementById('kicker')) tl.fromTo('#kicker', { y: ${-18 * k}, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, ease: 'power3.out' }, 0.12);
if (document.getElementById('sub')) tl.fromTo('#sub', { y: ${18 * k}, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, ease: 'power3.out' }, 0.6);
${script}
window.__timelines = window.__timelines || {};
window.__timelines['root'] = tl;
</script>
</body></html>`;
}

/** Bungkus judul berdasarkan lebar terukur (pakai pengukur font server). */
function wrapForWidth(text, maxW, size) {
  const words = String(text).trim().split(/\s+/).filter(Boolean);
  const lines = [];
  let cur = '';
  const width = (t) => (measure('Montserrat ExtraBold', t, size) ?? t.length * size * 0.62) + size * 0.5;
  for (const w of words) {
    const next = cur ? `${cur} ${w}` : w;
    if (cur && width(next) > maxW * 0.92) {
      lines.push(cur);
      cur = w;
    } else cur = next;
  }
  if (cur) lines.push(cur);
  return lines.length ? lines : [''];
}

/**
 * Pastikan klip MP4 tiap kartu ada (render bila belum di-cache).
 * @returns {Map<cardId, {file, start, end}>} rentang dalam waktu output.
 */
export async function prepareCardClips(project, { W, H, fps, spans, job, signal }) {
  const st = hyperframesStatus();
  if (!st.ok) throw new Error(st.detail);
  const dir = hfDir(project.id);
  const out = new Map();
  let i = 0;
  for (const { card, span } of spans) {
    i++;
    const dur = Math.max(0.3, span.end - span.start);
    const image = cardImage(project, card, dir);
    // Kartu overlay (mis. chat melayang di atas footage) dirender dengan alpha (ProRes 4444).
    const alpha = isOverlay(card);
    const hash = hashOf(card, project.style, W, H, fps, dur, image);
    const html = path.join(dir, `card-${hash}.html`);
    const file = path.join(dir, `card-${hash}.${alpha ? 'mov' : 'mp4'}`);
    if (!fs.existsSync(file)) {
      fs.writeFileSync(html, cardHtml(card, project.style, { W, H, dur, image }));
      if (job) job.message = `Merender grafis HyperFrames ${i}/${spans.length}…`;
      const part = `${path.basename(file)}.part.${alpha ? 'mov' : 'mp4'}`;
      const fmt = alpha ? ['--format', 'mov'] : ['-q', 'standard'];
      await runHyperframes(st.bin, ['render', '.', '-c', path.basename(html), '-o', part, '-f', String(fps), ...fmt], dir, signal);
      fs.renameSync(path.join(dir, part), file);
    }
    out.set(card.id, { file, start: span.start, end: span.end, alpha });
  }
  return out;
}

export const isOverlay = (card) => card.layout === 'overlay' || card.type === 'chat';

/** Foto milik pengguna untuk tile kartu: disalin ke folder HyperFrames (nama per id aset). */
export function cardImage(project, card, dir) {
  const a = card.image && (project.assets || []).find((x) => x.id === card.image && x.kind === 'image' && !x.missing);
  if (!a || !fs.existsSync(a.path)) return '';
  const name = `img-${a.id}${path.extname(a.path).toLowerCase() || '.jpg'}`;
  const dst = path.join(dir, name);
  if (!fs.existsSync(dst)) fs.copyFileSync(a.path, dst);
  return name;
}

function runHyperframes(bin, args, cwd, signal) {
  return new Promise((resolve, reject) => {
    const env = { ...process.env, HYPERFRAMES_NO_TELEMETRY: '1', DO_NOT_TRACK: '1', NO_COLOR: '1' };
    if (config.hyperframesBrowser) env.HYPERFRAMES_BROWSER_PATH = config.hyperframesBrowser;
    const child = spawn(process.execPath, [bin, ...args], { cwd, env, stdio: ['ignore', 'pipe', 'pipe'], signal });
    let log = '';
    const keep = (d) => (log = (log + d.toString()).slice(-6000));
    child.stdout.on('data', keep);
    child.stderr.on('data', keep);
    const timer = setTimeout(() => child.kill('SIGKILL'), 10 * 60000);
    child.on('error', (e) => {
      clearTimeout(timer);
      reject(e);
    });
    child.on('close', (code) => {
      clearTimeout(timer);
      if (code === 0) resolve();
      else {
        const lines = log.replace(/\x1b\[[0-9;]*m/g, '').split('\n').filter((l) => /error|fail|chrome|browser|cannot|not found/i.test(l)).slice(-3).join(' | ');
        reject(new Error(lines || `hyperframes keluar dengan kode ${code}`));
      }
    });
  });
}
