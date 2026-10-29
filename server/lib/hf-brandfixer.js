// Tema kartu HyperFrames "Editorial Diagnosis" — diturunkan dari design system
// "The Brand Fixer" milik Aldy (Claude): paper/sand/cream + ink, Archivo 800 untuk fakta,
// Fraunces Italic untuk rasa (satu frasa per kartu), Outfit untuk lead/body, Caveat untuk
// catatan tangan, JetBrains Mono untuk case tag. Terracotta = "pena sang Fixer" (garis &
// bidang: lingkaran, coretan, centang, pill), maks 2 elemen per kartu.
// Gerak: kata besar "slam" 112%→100% dalam ±6 frame, markup tergambar 12–15 frame,
// drift pelan; masuk/keluar potong keras (bible: tanpa transisi zoom/whoosh).
import { measure } from './fontmetrics.js';

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

export const BF_FONTS = [
  ['Archivo', 'Archivo-ExtraBold.ttf', 800, 'normal'],
  ['Archivo', 'Archivo-Bold.ttf', 700, 'normal'],
  ['Fraunces', 'Fraunces-Italic.ttf', 400, 'italic'],
  ['Outfit', 'Outfit-Medium.ttf', 500, 'normal'],
  ['Outfit', 'Outfit-SemiBold.ttf', 600, 'normal'],
  ['Caveat', 'Caveat-SemiBold.ttf', 600, 'normal'],
  ['JetBrains Mono', 'JetBrainsMono-Medium.ttf', 500, 'normal'],
];

// Garis tangan (dari komponen Stickers/SlideMarkup di design system): sedikit tidak sempurna.
const LOOP = 'M210 22 C 330 18, 402 92, 396 196 C 390 300, 300 378, 196 374 C 90 370, 20 300, 24 196 C 28 104, 96 30, 222 36';
const UNDER = 'M6 26 C 120 10, 260 34, 412 14';
const STRIKE = 'M0 30 C 60 27, 110 29, 158 25';
const ARROW = 'M20 6 C 24 40, 18 70, 22 104 M6 86 L 22 108 L 40 84';
const CHECK = 'M6 30 L 22 46 L 54 8';

/** Ukuran font agar kata terpanjang & baris muat di lebar yang tersedia. */
function fitSize(text, base, maxW, font = 'Archivo ExtraBold', maxLines = 3) {
  const words = String(text || '').split(/\s+/).filter(Boolean);
  const w = (t, s) => measure(font, t, s) ?? t.length * s * 0.6;
  let size = base;
  const longest = words.reduce((a, b) => (w(b, 1) > w(a, 1) ? b : a), '');
  if (longest && w(longest, size) > maxW) size = Math.floor((size * maxW) / w(longest, size));
  // Perkiraan jumlah baris: total lebar / lebar box.
  while (size > base * 0.5 && w(String(text), size) / maxW > maxLines * 0.92) size = Math.floor(size * 0.92);
  return size;
}

function parseNumber(title) {
  const m = String(title).match(/^(\D*?)(\d[\d.,]*)(.*)$/);
  if (!m) return null;
  const [, pre, num, post] = m;
  const thousands = /^\d{1,3}(\.\d{3})+$/.test(num);
  const decimals = !thousands && /,\d+$/.test(num) ? num.split(',')[1].length : 0;
  const value = thousands ? Number(num.replace(/\./g, '')) : Number(num.replace(/\./g, '').replace(',', '.'));
  return Number.isFinite(value) ? { pre, post, value, thousands, decimals } : null;
}

const stroke = (id, d, vb, cls = '') => `<svg class="mk ${cls}" id="${id}" viewBox="${vb}" preserveAspectRatio="none"><path pathLength="1" d="${d}"/></svg>`;

/**
 * @param card  kartu proyek (type: keyword|number|list|compare|quote|flow|chat|endcard)
 * @param style project.style
 * @param o     { W, H, dur, icon: svg string|'' , image: path relatif|'' }
 */
export function brandFixerHtml(card, style, { W, H, dur, icon = '', image = '' }) {
  // Kanvas reels (9:16) lebih tinggi dari slide carousel: tipografi dibesarkan agar terbaca di HP.
  const k = (Math.min(W, H) / 1080) * (H / W > 1.5 ? 1.22 : 1);
  const px = (n) => `${Math.round(n * k)}px`;
  const c = { paper: '#FBF8F3', cream: '#F4EBD9', sand: '#E7DDCD', ink: '#0F0E0C', inkSoft: '#2A2824', muted: '#6B6560', terracotta: '#B84A2E', terracottaInk: '#9E3F25', amber: '#C8944A', ...pick(style.colors) };
  const M = Math.round(72 * (Math.min(W, H) / 1080)); // margin aman kanvas (space-5)
  const topY = Math.max(M, Math.round(H * (style.safeZone?.top ?? 0.13))); // di bawah UI platform
  const inner = W - M * 2;
  const overlay = card.layout === 'overlay' || card.type === 'chat';
  const type = card.type || 'keyword';
  const bg = type === 'endcard' ? c.inkSoft : image || type === 'flow' ? c.sand : type === 'list' ? c.cream : c.paper;
  const light = type === 'endcard';
  const tag = card.caseTag ? `<div class="case ${light ? 'light' : ''}" id="case">${esc(card.caseTag)}</div>` : '<div></div>';
  const sig = style.cards?.signature !== false && !overlay ? `<div class="sig ${light ? 'light' : ''}" id="sig">aldy syahreza<i>the brand fixer</i></div>` : '';
  const top = overlay ? '' : `<div class="top">${tag}${sig}</div>`;
  const titleBase = (style.cards?.titleSize ?? 104) * k;
  let body = '';
  let tl = '';

  const kicker = card.kicker ? `<div class="lead" id="kicker">${esc(card.kicker)}</div>` : '';
  const accentLine = (txt, id = 'acc', size = titleBase) => `<div class="acc" id="${id}" style="font-size:${Math.round(fitSize(txt, size, inner, 'Fraunces Italic', 2))}px">${esc(txt)}</div>`;
  const slam = (sel, at) => `tl.fromTo('${sel}', { scale: 1.12, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.2, ease: 'power2.out' }, ${at});`;
  const rise = (sel, at, dy = 18) => `tl.fromTo('${sel}', { y: ${Math.round(dy * k)}, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, ease: 'power3.out' }, ${at});`;
  const draw = (sel, at, d = 0.45) => `tl.to('${sel} path', { strokeDashoffset: 0, duration: ${d}, ease: 'power1.inOut' }, ${at});`;

  if (type === 'number') {
    const n = parseNumber(card.title);
    const size = fitSize(card.title, (style.cards?.numberSize ?? 300) * 1.2 * k, inner * 0.8, 'Archivo ExtraBold', 1);
    const nw = measure('Archivo ExtraBold', String(card.title), size) ?? String(card.title).length * size * 0.6;
    body = `
      <div class="mid">
        ${kicker}
        <div class="numwrap" style="width:${Math.round(nw + size * 0.5)}px;height:${Math.round(size * 1.15)}px">
          <div class="num" id="num" style="font-size:${size}px">${esc(card.title)}</div>
          ${stroke('loop', LOOP, '0 0 420 400')}
        </div>
        ${card.subtitle ? accentLine(card.subtitle, 'acc', 92 * k) : ''}
      </div>`;
    tl = `
      ${card.kicker ? rise('#kicker', 0.04) : ''}
      ${slam('#num', 0.08)}
      ${n ? `const N = ${JSON.stringify(n)}; const o = { v: 0 };
      tl.to(o, { v: N.value, duration: 0.7, ease: 'power2.out', onUpdate: () => {
        const v = N.thousands ? Math.round(o.v).toLocaleString('id-ID') : o.v.toFixed(N.decimals).replace('.', ',');
        document.getElementById('num').textContent = N.pre + v + N.post;
      } }, 0.08);` : ''}
      ${draw('#loop', 0.62, 0.48)}
      ${card.subtitle ? rise('#acc', 0.5) : ''}`;
  } else if (type === 'list') {
    const items = String(card.subtitle || '').split(/\s*[;|]\s*/).filter(Boolean).slice(0, 5);
    const hs = fitSize(card.title, 96 * k, inner, 'Archivo ExtraBold', 2);
    body = `
      <div class="col">
        ${kicker}
        ${card.title ? `<div class="h" id="h" style="font-size:${hs}px">${esc(card.title)}</div>` : ''}
        <div class="checks">${items.map((it, i) => `<div class="check" id="row${i}"><div class="n">${String(i + 1).padStart(2, '0')}</div><div class="t">${esc(it)}</div>${stroke(`ck${i}`, CHECK, '0 0 60 54', 'ck')}</div>`).join('')}</div>
      </div>`;
    tl = `
      ${card.kicker ? rise('#kicker', 0.04) : ''}
      ${card.title ? slam('#h', 0.08) : ''}
      ${items.map((_, i) => `${rise(`#row${i}`, 0.4 + i * 0.32, 24)}\n${draw(`#ck${i}`, 0.58 + i * 0.32, 0.3)}`).join('\n')}`;
  } else if (type === 'compare') {
    const xs = fitSize(card.title, titleBase, inner, 'Archivo ExtraBold', 2);
    const ys = fitSize(card.subtitle, titleBase * 1.05, inner, 'Fraunces Italic', 2);
    body = `
      <div class="col">
        ${kicker}
        <div class="wrong" id="wrong"><span class="h" style="font-size:${xs}px">${esc(card.title)}</span>${stroke('strike', STRIKE, '0 0 160 60', 'strike')}</div>
        <div class="acc" id="acc" style="font-size:${ys}px">${esc(card.subtitle)}</div>
        ${stroke('under', UNDER, '0 0 420 40', 'under')}
      </div>`;
    tl = `
      ${card.kicker ? rise('#kicker', 0.04) : ''}
      ${slam('#wrong', 0.08)}
      ${draw('#strike', 0.42, 0.4)}
      ${rise('#acc', 0.85, 26)}
      ${draw('#under', 1.15, 0.45)}`;
  } else if (type === 'quote') {
    const qs = fitSize(card.title, 96 * k, inner, 'Fraunces Italic', 5);
    const words = String(card.title || '').split(/\s+/).filter(Boolean);
    body = `
      <div class="col">
        ${icon ? `<div class="qicon" id="qicon">${icon}</div>` : ''}
        <div class="quote" style="font-size:${qs}px">${words.map((w, i) => `<span class="qw" id="qw${i}">${esc(w)}</span>`).join(' ')}</div>
        ${card.kicker ? `<div class="small" id="kicker">${esc(card.kicker)}</div>` : ''}
        ${stroke('under', UNDER, '0 0 420 40', 'under short')}
      </div>`;
    const step = Math.min(0.12, 1.1 / Math.max(1, words.length));
    tl = `
      ${icon ? `${rise('#qicon', 0.02)}
tl.to('#qicon .draw > *', { strokeDashoffset: 0, duration: 0.5, ease: 'power2.out' }, 0.05);` : ''}
      ${words.map((_, i) => `tl.fromTo('#qw${i}', { opacity: 0, y: ${Math.round(14 * k)} }, { opacity: 1, y: 0, duration: 0.22, ease: 'power2.out' }, ${(0.1 + i * step).toFixed(3)});`).join('\n')}
      ${draw('#under', (0.3 + words.length * step).toFixed(2), 0.45)}
      ${card.kicker ? rise('#kicker', (0.5 + words.length * step).toFixed(2)) : ''}`;
  } else if (type === 'flow') {
    const nodes = [card.title, ...String(card.subtitle || '').split(/\s*[;|]\s*/)].map((x) => String(x || '').trim()).filter(Boolean).slice(0, 4);
    const ns = Math.min(...nodes.map((t) => fitSize(t, 64 * k, inner - 100 * k, 'Archivo ExtraBold', 2)));
    body = `
      <div class="col center">
        ${kicker}
        ${nodes.map((t, i) => `${i ? stroke(`ar${i}`, ARROW, '0 0 46 112', 'arrow') : ''}<div class="node ${i === nodes.length - 1 ? 'last' : ''}" id="node${i}" style="font-size:${ns}px">${esc(t)}</div>`).join('')}
      </div>`;
    tl = `
      ${card.kicker ? rise('#kicker', 0.04) : ''}
      ${nodes.map((_, i) => `${i ? draw(`#ar${i}`, (0.2 + i * 0.5 - 0.28).toFixed(2), 0.3) : ''}\ntl.fromTo('#node${i}', { scale: 1.12, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.2, ease: 'power2.out' }, ${(0.08 + i * 0.5).toFixed(2)});`).join('\n')}`;
  } else if (type === 'chat') {
    const reply = card.subtitle ? `<div class="msg me" id="m1">${esc(card.subtitle)}</div>` : '';
    body = `
      <div class="chat" id="chat">
        <div class="meta">ILUSTRASI · DARI UCAPAN</div>
        <div class="msg" id="m0">${esc(card.title)}${reply ? '' : stroke('cloop', LOOP, '0 0 420 400', 'chatloop')}</div>
        ${reply ? reply.replace('</div>', `${stroke('cloop', LOOP, '0 0 420 400', 'chatloop')}</div>`) : ''}
      </div>
      ${card.kicker ? `<div class="hand" id="note">${esc(card.kicker)}</div>` : ''}`;
    tl = `
      tl.fromTo('#chat', { y: ${Math.round(40 * k)}, opacity: 0, scale: 0.96 }, { y: 0, opacity: 1, scale: 1, duration: 0.32, ease: 'power3.out' }, 0.02);
      tl.fromTo('#m0', { opacity: 0, y: ${Math.round(12 * k)} }, { opacity: 1, y: 0, duration: 0.22 }, 0.25);
      ${reply ? `tl.fromTo('#m1', { opacity: 0, y: ${Math.round(12 * k)} }, { opacity: 1, y: 0, duration: 0.22 }, 0.85);` : ''}
      ${draw('#cloop', reply ? 1.2 : 0.7, 0.48)}
      ${card.kicker ? `tl.fromTo('#note', { opacity: 0, rotation: -4 }, { opacity: 1, rotation: -2, duration: 0.3 }, ${reply ? 1.7 : 1.2});` : ''}`;
  } else if (type === 'endcard') {
    const ec = { ...(style.endcard || {}), ...(card.endcard || {}) };
    const big = ec.big || card.title || '';
    const bs = fitSize(big, (big.length <= 9 ? 200 : 150) * k, inner, 'Archivo ExtraBold', 2);
    body = `
      <div class="lockup">
        ${ec.lead ? `<div class="lead" id="kicker">${esc(ec.lead)}</div>` : ''}
        <div class="mega" id="big" style="font-size:${bs}px">${esc(big)}</div>
        ${ec.accent ? accentLine(ec.accent, 'acc', 140 * k) : ''}
        ${ec.pill ? `<div class="pill" id="pill">${esc(ec.pill)} →</div>` : ''}
        <div class="sig light center" id="sig2">aldy syahreza<i>the brand fixer</i></div>
      </div>`;
    tl = `
      ${ec.lead ? rise('#kicker', 0.04) : ''}
      ${slam('#big', 0.12)}
      ${ec.accent ? rise('#acc', 0.42, 22) : ''}
      ${ec.pill ? `tl.fromTo('#pill', { scale: 0.9, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.24, ease: 'back.out(2)' }, 0.75);` : ''}
      tl.fromTo('#sig2', { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.9);`;
  } else {
    // keyword / statement: fakta (Archivo) → rasa (Fraunces) + coretan bawah terracotta.
    const ts = fitSize(card.title, titleBase * (image ? 0.9 : 1.15), inner, 'Archivo ExtraBold', 3);
    body = `
      ${image ? `<div class="tile" id="tile"><img src="${esc(image)}" id="img"></div>` : ''}
      <div class="col ${image ? 'below' : 'center'}">
        ${icon && !image ? `<div class="ic" id="ic">${icon}</div>` : ''}
        ${kicker}
        <div class="h" id="h" style="font-size:${ts}px">${esc(card.title)}</div>
        ${card.subtitle ? accentLine(card.subtitle, 'acc', titleBase * (image ? 0.85 : 1)) : ''}
        ${stroke('under', UNDER, '0 0 420 40', 'under')}
      </div>`;
    tl = `
      ${image ? `tl.fromTo('#tile', { y: ${Math.round(30 * k)}, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, ease: 'power3.out' }, 0);
      tl.fromTo('#img', { scale: 1.08 }, { scale: 1.0, duration: D, ease: 'none' }, 0);` : ''}
      ${icon && !image ? `tl.fromTo('#ic', { opacity: 0, y: ${Math.round(-10 * k)} }, { opacity: 1, y: 0, duration: 0.25 }, 0.02);
      tl.to('#ic .draw > *', { strokeDashoffset: 0, duration: 0.5, ease: 'power2.out' }, 0.05);` : ''}
      ${card.kicker ? rise('#kicker', 0.04) : ''}
      ${slam('#h', 0.1)}
      ${card.subtitle ? rise('#acc', 0.42, 22) : ''}
      ${draw('#under', card.subtitle ? 0.7 : 0.45, 0.45)}`;
  }

  const fontFace = BF_FONTS.map(([fam, file, wt, sty]) => `@font-face{font-family:'${fam}';src:url(fonts/${file});font-weight:${wt};font-style:${sty}}`).join('');
  const grain = `url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")`;

  return `<!doctype html>
<html><head><meta charset="utf-8"><style>
${fontFace}
html,body{margin:0;width:${W}px;height:${H}px;overflow:hidden;background:${overlay ? 'transparent' : bg}}
#root{position:relative;width:${W}px;height:${H}px;overflow:hidden;font-family:'Outfit',sans-serif;color:${light ? '#fff' : c.ink};background:${overlay ? 'transparent' : bg}}
${overlay ? '' : `.grainlayer{position:absolute;inset:0;opacity:.16;mix-blend-mode:multiply;background-image:${grain};pointer-events:none}`}
#stage{position:absolute;inset:0;transform-origin:50% 45%}
.top{position:absolute;top:${topY}px;left:${M}px;right:${M}px;display:flex;justify-content:space-between;align-items:flex-start;z-index:3}
.case{display:inline-flex;align-items:center;gap:${px(12)};font:500 ${px(22)}/1 'JetBrains Mono',monospace;letter-spacing:.08em;text-transform:uppercase;color:${c.ink}}
.case::before{content:"";width:${px(14)};height:${px(14)};border-radius:50%;background:${c.amber}}
.case.light{color:#fff}
.sig{text-align:right;font:600 ${px(26)}/1.05 'Outfit',sans-serif;letter-spacing:.01em;color:${c.ink}}
.sig i{display:block;font:400 italic ${px(30)}/1.05 'Fraunces',serif}
.sig.light{color:#fff}.sig.center{text-align:center;margin-top:${px(70)}}
.col{position:absolute;left:${M}px;right:${M}px;top:50%;transform:translateY(-50%);display:flex;flex-direction:column;gap:${px(14)}}
.col.center{align-items:center;text-align:center}
.col.below{top:auto;bottom:${Math.round(H * 0.17)}px;transform:none}
.mid{position:absolute;left:${M}px;right:${M}px;top:47%;transform:translateY(-50%);display:flex;flex-direction:column;align-items:center;text-align:center;gap:${px(10)}}
.lead{font:500 ${px(46)}/1.1 'Outfit',sans-serif;color:${light ? '#fff' : c.inkSoft}}
.h{font-family:'Archivo';font-weight:800;line-height:.92;letter-spacing:-.045em;text-wrap:balance}
.acc{font-family:'Fraunces';font-style:italic;font-weight:400;line-height:.98;letter-spacing:-.02em;text-wrap:balance}
.mk{position:absolute;overflow:visible}
.mk path{fill:none;stroke:${c.terracotta};stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1}
.under{position:relative;width:${px(380)};height:${px(36)};margin-top:${px(4)}}
.under.short{width:${px(220)}}
.ic .ic,.ic svg{width:${px(96)};height:${px(96)};color:${c.ink};stroke-width:1.8}
.draw > *{stroke-dasharray:1;stroke-dashoffset:1}
.numwrap{position:relative;display:grid;place-items:center}
.num{font-family:'Archivo';font-weight:800;line-height:1;letter-spacing:-.05em;color:${c.ink};white-space:nowrap}
#loop{inset:-6% -4%;width:108%;height:112%}
.checks{display:flex;flex-direction:column;margin-top:${px(26)}}
.check{position:relative;display:grid;grid-template-columns:${px(96)} 1fr ${px(64)};gap:${px(18)};align-items:center;padding:${px(28)} 0;border-top:${Math.max(1, Math.round(2 * k))}px solid rgba(15,14,12,.18)}
.check .n{font:800 ${px(64)}/1 'Archivo';letter-spacing:-.04em}
.check .t{font:600 ${px(44)}/1.25 'Outfit',sans-serif}
.check .ck{position:relative;width:${px(52)};height:${px(46)}}
.wrong{position:relative;align-self:flex-start;color:${c.muted}}
.wrong .h{color:${c.muted}}
.strike{left:-2%;top:44%;width:104%;height:24%}
.quote{font-family:'Fraunces';font-style:italic;line-height:1.08;letter-spacing:-.015em;text-wrap:pretty}
.qicon svg{width:${px(70)};height:${px(70)};color:${c.ink};stroke-width:1.6}
.small{font:500 ${px(28)}/1.35 'Outfit',sans-serif;color:${c.muted}}
.node{background:${c.paper};border-radius:${px(20)};padding:${px(26)} ${px(42)};font-family:'Archivo';font-weight:800;letter-spacing:-.035em;line-height:1;box-shadow:0 ${px(18)} ${px(40)} rgba(15,14,12,.14);max-width:${inner - Math.round(60 * k)}px}
.node.last{background:${c.ink};color:#fff}
.arrow{position:relative;width:${px(46)};height:${px(100)};margin:${px(4)} 0}
.tile{position:absolute;left:${M}px;right:${M}px;top:${Math.round(H * 0.14)}px;height:${Math.round(H * 0.42)}px;border-radius:${px(28)};overflow:hidden;box-shadow:0 ${px(18)} ${px(40)} rgba(15,14,12,.18)}
.tile img{width:100%;height:100%;object-fit:cover;transform-origin:50% 40%}
.chat{position:absolute;right:${Math.round(W * 0.08)}px;top:${Math.round(H * ((style.faceZone?.bottom ?? 0.5) + 0.03))}px;width:${Math.round(W * 0.64)}px;background:#fff;border-radius:${px(28)};box-shadow:0 ${px(18)} ${px(40)} rgba(15,14,12,.28);padding:${px(28)} ${px(30)};font:500 ${px(32)}/1.35 'Outfit',sans-serif;color:${c.inkSoft}}
.chat .meta{font:500 ${px(18)}/1 'JetBrains Mono',monospace;color:${c.muted};letter-spacing:.06em}
.msg{position:relative;background:${c.cream};border-radius:${px(18)} ${px(18)} ${px(18)} ${px(6)};padding:${px(16)} ${px(20)};margin:${px(12)} 0}
.msg.me{background:#e3efd9;border-radius:${px(18)} ${px(18)} ${px(6)} ${px(18)};margin-left:${px(60)}}
.chatloop{left:-10%;top:-60%;width:120%;height:220%}
.hand{position:absolute;right:${Math.round(W * 0.1)}px;top:${Math.round(H * ((style.faceZone?.bottom ?? 0.5) + 0.03)) + Math.round(W * 0.42)}px;font:600 ${px(64)}/1 'Caveat',cursive;color:#fff;text-shadow:0 ${px(2)} ${px(10)} rgba(0,0,0,.45);transform:rotate(-2deg)}
.lockup{position:absolute;left:${M}px;right:${M}px;top:50%;transform:translateY(-50%);display:flex;flex-direction:column;align-items:center;text-align:center;color:#fff}
.mega{font-family:'Archivo';font-weight:800;line-height:.86;letter-spacing:-.055em}
.pill{margin-top:${px(56)};display:inline-flex;padding:${px(20)} ${px(38)};border-radius:999px;background:${c.terracotta};color:#fff;font:700 ${px(26)}/1 'Archivo';letter-spacing:.04em;text-transform:uppercase}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="${W}" data-height="${H}" data-start="0" data-duration="${dur.toFixed(3)}">
  <div id="stage">${top}${body}</div>
  ${overlay ? '' : '<div class="grainlayer"></div>'}
</div>
<script src="gsap.min.js"></script>
<script>
const D = ${dur.toFixed(3)};
// Tebal garis markup ±7px di layar (kanvas 1080), walau SVG direntang tanpa menjaga rasio.
for (const svg of document.querySelectorAll('svg.mk')) {
  const vb = svg.viewBox.baseVal, r = svg.getBoundingClientRect();
  const sc = Math.sqrt((r.width / vb.width) * (r.height / vb.height)) || 1;
  svg.querySelector('path').style.strokeWidth = (${(7 * Math.min(W, H) / 1080 * (H / W > 1.5 ? 1.2 : 1)).toFixed(2)} / sc).toFixed(2);
}
const tl = gsap.timeline({ paused: true });
${overlay ? '' : `tl.fromTo('#stage', { scale: 1.02 }, { scale: 1.0, duration: D, ease: 'none' }, 0);`}
if (document.getElementById('case')) tl.fromTo('#case', { opacity: 0 }, { opacity: 1, duration: 0.2 }, 0);
if (document.getElementById('sig')) tl.fromTo('#sig', { opacity: 0 }, { opacity: 1, duration: 0.2 }, 0);
${tl}
window.__timelines = window.__timelines || {};
window.__timelines['root'] = tl;
</script>
</body></html>`;
}

function pick(colors = {}) {
  const out = {};
  if (colors.cardBg) out.paper = colors.cardBg;
  if (colors.cardText) out.ink = colors.cardText;
  if (colors.cardMuted) out.muted = colors.cardMuted;
  for (const key of ['cream', 'sand', 'inkSoft', 'amber', 'accentInk']) if (colors[key]) out[key === 'accentInk' ? 'terracottaInk' : key] = colors[key];
  if (colors.accent) out.terracotta = colors.accent;
  return out;
}
