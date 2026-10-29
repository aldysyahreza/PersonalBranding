// Profil brand yang ditampilkan di UI. Sumber kebenaran tertulis ada di
// docs/BRAND_PROFILE.md; file ini adalah versi terstruktur untuk aplikasi.
// Jangan menambahkan fakta personal tanpa sumber.

export const BRAND_PROFILE = {
  person: 'Aldy Syahreza',
  sourceNote:
    'Sumber: (1) preferensi profil yang ditulis Aldy di pengaturan Claude; (2) artifact milik Aldy di Claude — "Brand Fixer OS" (playbook Personal Branding Aldy Syahreza) dan design system "The Brand Fixer" (Visual System v2 — Editorial Diagnosis, beserta riset referensinya), dibaca 29 Okt 2026. Semua dinyatakan sendiri oleh Aldy; belum diverifikasi pihak ketiga. Tidak ada data yang diambil dari web atau media sosial.',
  facts: [
    { text: 'Nama: Aldy Syahreza. Positioning: "The Brand Fixer".', source: 'Brand Fixer OS & design system The Brand Fixer.' },
    { text: 'Core idea: "Brand kamu sudah jalan. Tapi belum naik kelas." Big idea: banyak masalah bisnis bukan karena kurang konten, tetapi brand belum cukup jelas.', source: 'Brand Fixer OS.' },
    { text: 'Audiens: business owner yang bisnisnya SUDAH berjalan (sudah jualan, posting, marketing, mungkin ads) — bukan pemula pencari tips gratis.', source: 'Brand Fixer OS.' },
    { text: 'The Brand-Up System: Brand Clarity · Brand Trust · Brand Premium · Brand System · Brand Content. Case tag 7 lapis diagnosis DX·01–07.', source: 'Brand Fixer OS & design system.' },
    { text: 'Pilar konten: 45% The Brand Diagnosis · 25% The Quiet Builders · 20% The Director\'s Mind · 10% AI as Strategic Tool (AI alat, bukan hero).', source: 'Brand Fixer OS.' },
    { text: 'Brand kit: Warm White #FBF8F3 · Ink #0F0E0C · Terracotta #B84A2E · Amber #C8944A · Warm Gray #6B6560; font Archivo, Fraunces Italic, Outfit, Caveat, JetBrains Mono.', source: 'Design system The Brand Fixer (tokens.json).' },
    { text: 'Peran yang dinyatakan: Brand Strategist, Digital Marketing Consultant, AI Workflow Builder, founder.', source: 'Preferensi profil Claude.' },
  ],
  preferences: [
    'Voice: saya/kamu, hangat, tenang, mature, observational, berbobot — terasa seperti realization, bukan ceramah.',
    'Hindari gaya motivator, listicle agresif ("5 cara sukses…", "rahasia…"), dan kata "wajib", "rahasia", "auto", "dijamin", "hack".',
    'Reels: hook 0–1,2 dtk kata besar slam 112%→100%; caption 2–4 kata, maks 1 kata Fraunces; markup terracotta maks 1×; end card 2 dtk; potong tiap 1,5–2,5 dtk; total 30–45 dtk.',
    'Jangan: audio meme trending, caption berwarna-warni, transisi zoom/whoosh, stiker emoji.',
    'Foto nyata dulu (bank foto Aldy, adegan bisnis Indonesia); AI dokumenter hanya untuk metafora dan diberi label AI.',
    'Ukur shares, saves, profile visits, follow conversion, inquiry — bukan hanya likes.',
  ],
  assumptions: [
    'Ukuran caption reels di aplikasi (100px @1080) lebih besar dari token bible (68px) agar terbaca di video talking head — ubah di Editor bila ingin persis bible.',
    'Ritme kinetik kata-per-kata diambil dari video referensi; gaya (font, warna, larangan) mengikuti bible.',
    'Kata kunci penekanan default diturunkan dari kosakata bible; belum tentu kosakata yang paling sering Aldy ucapkan.',
  ],
  unknowns: [
    'Keyword CTA aktif saat ini (AUDIT, KUAT, SOP, AI tercatat sebagai aset historis; bible: jangan otomatis dipakai).',
    'Platform prioritas dan handle yang boleh tampil di end card.',
    'Library musik berlisensi yang dimiliki.',
    'Foto bank bulanan yang siap dipakai sebagai tile kartu.',
  ],
};

export const DEFAULT_BRAND_KEYWORDS = [
  'brand', 'branding', 'positioning', 'clarity', 'jelas', 'trust', 'dipercaya', 'premium', 'sistem', 'system',
  'konten', 'content', 'owner', 'bisnis', 'dipilih', 'diagnosis', 'strategi', 'marketing', 'AI', 'customer',
];
