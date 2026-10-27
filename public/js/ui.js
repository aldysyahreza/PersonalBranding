// Helper DOM kecil tanpa framework.

export function h(tag, attrs = {}, ...children) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v === undefined || v === null || v === false) continue;
    if (k === 'class') el.className = v;
    else if (k === 'style' && typeof v === 'object') Object.assign(el.style, v);
    else if (k.startsWith('on') && typeof v === 'function') el.addEventListener(k.slice(2).toLowerCase(), v);
    else if (k === 'html') el.innerHTML = v;
    else if (k === 'value' || k === 'checked') el[k] = v;
    else if (k in el && typeof v !== 'string') el[k] = v;
    else el.setAttribute(k, v === true ? '' : v);
  }
  for (const c of children.flat(Infinity)) {
    if (c === null || c === undefined || c === false) continue;
    el.append(c instanceof Node ? c : document.createTextNode(String(c)));
  }
  return el;
}

export function toast(msg, kind = 'info', hint = '') {
  const box = document.getElementById('toasts');
  const t = h('div', { class: `toast ${kind}` }, h('strong', {}, msg), hint ? h('div', { class: 'hint' }, hint) : null);
  box.append(t);
  setTimeout(() => t.classList.add('out'), kind === 'error' ? 9000 : 4000);
  setTimeout(() => t.remove(), kind === 'error' ? 9600 : 4600);
}

export function modal(title, body, actions = []) {
  return new Promise((resolve) => {
    const close = (v) => {
      back.remove();
      resolve(v);
    };
    const back = h(
      'div',
      { class: 'modal-back', onclick: (e) => e.target === back && close(null) },
      h(
        'div',
        { class: 'modal', role: 'dialog', 'aria-modal': 'true' },
        h('h3', {}, title),
        h('div', { class: 'modal-body' }, body),
        h('div', { class: 'modal-actions' }, h('button', { class: 'btn ghost', onclick: () => close(null) }, 'Batal'), ...actions.map((a) => h('button', { class: `btn ${a.kind || ''}`, onclick: () => close(a.value ?? true), disabled: a.disabled }, a.label))),
      ),
    );
    document.body.append(back);
    back.querySelector('.modal-actions .btn:last-child')?.focus();
  });
}

/** Dialog persetujuan untuk fitur yang mengirim data ke layanan cloud. */
export function consentDialog({ title, service, sent, notSent }) {
  const cb = h('input', { type: 'checkbox', id: 'consent' });
  const body = h(
    'div',
    {},
    h('p', {}, `Fitur ini memakai layanan cloud: `, h('strong', {}, service), '.'),
    h('ul', {}, h('li', {}, h('strong', {}, 'Yang dikirim: '), sent), h('li', {}, h('strong', {}, 'Yang tidak dikirim: '), notSent)),
    h('p', { class: 'muted' }, 'Data diproses sesuai kebijakan penyedia layanan. Gunakan opsi lokal/manual bila materi bersifat rahasia.'),
    h('label', { class: 'check' }, cb, ' Saya setuju mengirim data di atas untuk proses ini.'),
  );
  return new Promise(async (resolve) => {
    const res = await modal(title, body, [{ label: 'Kirim & lanjutkan', kind: 'primary', value: 'go' }]);
    resolve(res === 'go' && cb.checked);
    if (res === 'go' && !cb.checked) toast('Dibatalkan: kotak persetujuan belum dicentang.', 'warn');
  });
}

export function fmtBytes(n) {
  if (!n && n !== 0) return '-';
  const u = ['B', 'KB', 'MB', 'GB'];
  let i = 0;
  while (n >= 1024 && i < u.length - 1) {
    n /= 1024;
    i++;
  }
  return `${n.toFixed(i ? 1 : 0)} ${u[i]}`;
}

export function fmtDate(iso) {
  if (!iso) return '-';
  return new Date(iso).toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' });
}

export function badge(text, kind = '') {
  return h('span', { class: `badge ${kind}` }, text);
}

export function originBadge(origin) {
  const map = { aturan: ['Saran aturan', 'sug'], claude: ['Saran AI (Claude)', 'ai'], pengguna: ['Dibuat pengguna', 'user'] };
  const [t, k] = map[origin] || [origin || '-', ''];
  return badge(t, k);
}

export function field(label, input, help) {
  return h('label', { class: 'field' }, h('span', { class: 'field-label' }, label), input, help ? h('span', { class: 'field-help' }, help) : null);
}

export function num(value, onChange, { step = 0.1, min, max, width } = {}) {
  return h('input', { type: 'number', value: value ?? '', step, min, max, style: width ? { width } : undefined, onchange: (e) => onChange(Number(e.target.value)) });
}

export function slider(value, onInput, { min = 0, max = 1, step = 0.01, fmt = (v) => v } = {}) {
  const out = h('output', {}, fmt(value));
  const inp = h('input', {
    type: 'range', min, max, step, value,
    oninput: (e) => { out.textContent = fmt(Number(e.target.value)); onInput(Number(e.target.value), false); },
    onchange: (e) => onInput(Number(e.target.value), true),
  });
  return h('span', { class: 'slider' }, inp, out);
}

export function select(value, options, onChange) {
  return h('select', { onchange: (e) => onChange(e.target.value) }, ...options.map(([v, l]) => h('option', { value: v, selected: v === value }, l)));
}

// append()/replaceChildren() bawaan DOM mengubah null menjadi teks "null".
// Abaikan null/undefined/false agar child kondisional bisa ditulis inline.
for (const m of ['append', 'replaceChildren']) {
  const native = Element.prototype[m];
  Element.prototype[m] = function (...nodes) {
    return native.apply(this, nodes.filter((n) => n !== null && n !== undefined && n !== false));
  };
}
