// Profil brand yang ditampilkan di UI. Sumber kebenaran tertulis ada di
// docs/BRAND_PROFILE.md; file ini adalah versi terstruktur untuk aplikasi.
// Jangan menambahkan fakta personal tanpa sumber.

export const BRAND_PROFILE = {
  person: 'Aldy Syahreza',
  sourceNote:
    'Satu-satunya sumber yang tersedia saat aplikasi dibuat adalah preferensi profil yang ditulis Aldy sendiri di pengaturan Claude (dibagikan ke sesi pembuatan aplikasi). Tidak ada memori Claude, file brand, atau akun media sosial yang dapat diakses.',
  facts: [
    { text: 'Nama: Aldy Syahreza.', source: 'Dinyatakan sendiri (preferensi profil Claude).' },
    { text: 'Menyebut diri sebagai Brand Strategist, Digital Marketing Consultant, AI Workflow Builder, dan founder.', source: 'Dinyatakan sendiri; belum diverifikasi dari sumber publik.' },
    { text: 'Fokus kerja: brand strategy, personal branding, social media & content strategy, Meta Ads, customer journey, business strategy, marketing system design, AI automation, product development, offer positioning, growth systems.', source: 'Dinyatakan sendiri.' },
  ],
  preferences: [
    'Komunikasi ringkas, padat, tanpa buzzword korporat dan tanpa basa-basi.',
    'Konten tidak generik: hook kuat, storytelling, nilai edukatif, layak disimpan, membangun otoritas.',
    'Konsistensi brand jangka panjang; hindari tren yang melemahkan positioning.',
    'Audiens default: pemilik bisnis, founder, UKM, personal brand, kreator, profesional.',
    'Lebih suka sistem yang dapat dipakai ulang daripada solusi sekali pakai.',
  ],
  assumptions: [
    'Gaya visual "Editorial Talking Head" (latar gelap-hangat, kartu terang, satu warna aksen merah) diturunkan dari video referensi, bukan dari panduan visual Aldy.',
    'Warna aksen #D92A2A serta font Montserrat + Great Vibes dipilih karena mirip referensi — placeholder sampai ada identitas visual resmi.',
    'Bahasa konten diasumsikan Bahasa Indonesia, kadang campur istilah Inggris.',
    'Daftar kata kunci penekanan diturunkan dari bidang fokus yang dinyatakan; belum tentu kosakata yang sering diucapkan.',
  ],
  unknowns: [
    'Warna, font, dan logo resmi brand Aldy (jika ada).',
    'Platform utama (Instagram, TikTok, LinkedIn, YouTube Shorts) dan prioritasnya.',
    'Gaya bicara di kamera, bahasa utama video, dan panjang video yang biasa dibuat.',
    'Apakah boleh menampilkan nama/handle/CTA tertentu di akhir video.',
    'Library musik dan sound effect berlisensi yang dimiliki.',
    'Apakah ada aturan tampilan wajah/pencahayaan yang disukai (mis. tingkat kehangatan warna).',
  ],
};

export const DEFAULT_BRAND_KEYWORDS = [
  'brand', 'branding', 'strategi', 'strategy', 'positioning', 'marketing', 'konten', 'content',
  'sistem', 'system', 'AI', 'otomasi', 'automation', 'funnel', 'offer', 'growth', 'bisnis',
  'business', 'customer', 'ads', 'iklan', 'audiens', 'audience', 'leverage', 'ROI',
];
