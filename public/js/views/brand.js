// Profil brand (fakta/preferensi/asumsi/belum diketahui) + status layanan sistem.
import { h, badge } from '../ui.js';
import { store, edit } from '../store.js';

export function renderBrand(main) {
  const S = store.status;
  const b = S.brand;
  const list = (items, fmt = (x) => x) => h('ul', { class: 'facts' }, ...items.map((x) => h('li', {}, fmt(x))));
  main.append(
    h('div', { class: 'view-head' }, h('h1', {}, `Profil brand — ${b.person}`), h('p', { class: 'muted' }, b.sourceNote)),
    h('div', { class: 'grid2' },
      h('section', { class: 'panel' }, h('h2', {}, '1. Fakta bersumber'), list(b.facts, (f) => [f.text, h('div', { class: 'muted small' }, `Sumber: ${f.source}`)])),
      h('section', { class: 'panel' }, h('h2', {}, '2. Preferensi yang dinyatakan'), list(b.preferences)),
      h('section', { class: 'panel' }, h('h2', {}, '3. Asumsi desain sementara'), list(b.assumptions)),
      h('section', { class: 'panel' }, h('h2', {}, '4. Belum diketahui — perlu ditanyakan'), list(b.unknowns)),
    ),
  );
  if (store.project) {
    const ta = h('textarea', { rows: 3, value: (store.project.brandKeywords || []).join(', '), onchange: (e) => edit((x) => (x.brandKeywords = e.target.value.split(',').map((s) => s.trim()).filter(Boolean)), { rerender: false }) });
    main.append(h('section', { class: 'panel' }, h('h2', {}, 'Kata kunci penekanan (proyek ini)'), h('p', { class: 'muted small' }, 'Dipakai saran berbasis aturan untuk memilih kata yang diberi blok warna. Asumsi awal dari bidang fokus yang dinyatakan — sesuaikan dengan kosakata Anda.'), ta));
  }
  const svc = (label, ok, detail, cloud) => h('tr', {}, h('th', {}, label), h('td', {}, badge(ok ? 'Tersedia' : 'Tidak tersedia', ok ? 'ok' : 'warn'), cloud ? badge('Cloud — perlu persetujuan', 'info') : badge('Lokal', ''), h('div', { class: 'muted small' }, detail)));
  main.append(
    h('section', { class: 'panel' }, h('h2', {}, 'Status sistem'),
      h('table', { class: 'info' },
        svc('ffmpeg', !!S.ffmpeg, S.ffmpeg || 'Pasang ffmpeg (wajib untuk analisis & ekspor).'),
        svc('Transkripsi lokal', S.transcription.local.available, `${S.transcription.local.detail}${S.transcription.local.available ? '' : ` — ${S.transcription.local.setup}`}`),
        svc('Transkripsi OpenAI', S.transcription.openai.available, S.transcription.openai.detail, true),
        svc('Rencana edit Claude', S.claude.configured, S.claude.configured ? `Model ${S.claude.model}` : 'ANTHROPIC_API_KEY belum diisi di .env (opsional).', true),
      ),
      h('h3', {}, 'Lokasi penting'),
      h('table', { class: 'info' },
        h('tr', {}, h('th', {}, 'Proyek'), h('td', {}, h('code', {}, S.paths.projects))),
        h('tr', {}, h('th', {}, 'Output ekspor'), h('td', {}, h('code', {}, S.paths.output))),
        h('tr', {}, h('th', {}, 'Preset gaya'), h('td', {}, h('code', {}, S.paths.presets))),
      ),
      h('p', { class: 'muted small' }, 'API key hanya dibaca dari file .env di server lokal dan tidak pernah dikirim ke browser.'),
    ),
  );
}
