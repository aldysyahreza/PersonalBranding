// Ikon kartu grafis (Lucide, lisensi ISC — file SVG di assets/icons/).
// Dipakai bersama oleh server (render HyperFrames) dan browser (pilihan ikon di UI).
import { normWord, tokenize } from './core.js';

export const ICON_NAMES = [
  'target', 'crosshair', 'sparkles', 'star', 'badge-check', 'check', 'circle-check', 'circle-x', 'circle-arrow-right',
  'arrow-right', 'triangle-alert', 'lightbulb', 'key-round', 'trending-up', 'chart-column', 'chart-no-axes-combined',
  'users', 'user-plus', 'user-round', 'message-circle', 'megaphone', 'pen-line', 'video', 'camera', 'clock', 'calendar',
  'wallet', 'banknote', 'shopping-cart', 'store', 'rocket', 'zap', 'heart', 'thumbs-up', 'bookmark', 'share-2', 'repeat',
  'eye', 'book-open', 'workflow', 'settings', 'bot', 'cpu', 'brain', 'puzzle', 'layers', 'compass', 'flag', 'trophy', 'gem',
  'shield-check', 'handshake', 'mic', 'list-checks', 'hash', 'percent', 'gift', 'search', 'funnel', 'link', 'mail', 'globe',
  'smartphone', 'briefcase', 'building-2', 'graduation-cap', 'hourglass', 'infinity', 'refresh-cw', 'quote', 'send',
  'hand-coins', 'piggy-bank', 'coins', 'badge-dollar-sign',
];

// Nilai ikon lama (versi sebelumnya) → ikon Lucide.
export const LEGACY_ICON = { check: 'circle-check', cross: 'circle-x', arrow: 'circle-arrow-right', warning: 'triangle-alert', star: 'star' };

// Kata (sudah dinormalisasi) → ikon. Urutan = prioritas.
const RULES = [
  [/^(simpan|save|bookmark)$/, 'bookmark'],
  [/^(bagikan|share|kirim|sebarkan)$/, 'share-2'],
  [/^(follow|ikuti|subscribe|gabung|daftar)$/, 'user-plus'],
  [/^(komen|komentar|comment|dm|chat|pesan|tanya|bertanya)$/, 'message-circle'],
  [/^(rekomendasi|direkomendasikan|merekomendasikan|referral|testimoni|review|percaya|trust)$/, 'thumbs-up'],
  [/^(brand|branding|merek|reputasi|otoritas)$/, 'badge-check'],
  [/^(positioning|posisi|posisinya|fokus|target|sasaran|niche)$/, 'target'],
  [/^(strategi|strategy|rencana|plan|arah)$/, 'compass'],
  [/^(sistem|system|proses|alur|workflow|funnel)$/, 'workflow'],
  [/^(ai|otomasi|automation|otomatis|bot|robot)$/, 'bot'],
  [/^(konten|content|posting|post|tulis|menulis|script|scripting|naskah|copywriting|caption)$/, 'pen-line'],
  [/^(video|reels|tiktok|youtube|shorts|rekam)$/, 'video'],
  [/^(iklan|ads|promosi|kampanye|marketing|pemasaran|awareness)$/, 'megaphone'],
  [/^(pelanggan|customer|klien|client|audiens|audience|orang|followers|pengikut|komunitas|tim)$/, 'users'],
  [/^(jual|jualan|penjualan|sales|closing|beli|order|checkout)$/, 'shopping-cart'],
  [/^(uang|omzet|omset|profit|untung|revenue|harga|biaya|budget|cuan|gaji)$/, 'wallet'],
  [/^(tumbuh|growth|naik|meningkat|scale|skala|berkembang)$/, 'trending-up'],
  [/^(data|angka|statistik|metrik|hasil|analisis|riset)$/, 'chart-column'],
  [/^(waktu|hari|jam|menit|minggu|bulan|tahun|cepat|lama)$/, 'clock'],
  [/^(masalah|problem|salah|kesalahan|gagal|risiko|bahaya|jebakan)$/, 'triangle-alert'],
  [/^(solusi|kunci|kuncinya|rahasia|rahasianya|cara|caranya|jawaban)$/, 'key-round'],
  [/^(ide|insight|inspirasi|kreatif|pelajaran)$/, 'lightbulb'],
  [/^(cerita|story|storytelling|kisah|pengalaman|buku)$/, 'book-open'],
  [/^(konsisten|konsistensi|rutin|ulang|diulang|berulang|kebiasaan)$/, 'repeat'],
  [/^(jelas|terlihat|dilihat|lihat|visibilitas|perhatian)$/, 'eye'],
  [/^(produk|bisnis|usaha|toko|umkm|ukm)$/, 'store'],
  [/^(founder|ceo|pemimpin|karier|karir|kerja|profesional)$/, 'briefcase'],
  [/^(belajar|edukasi|kursus|kelas|ilmu)$/, 'graduation-cap'],
  [/^(menang|juara|sukses|berhasil|pencapaian)$/, 'trophy'],
  [/^(kualitas|premium|nilai|value|berharga)$/, 'gem'],
  [/^(aman|keamanan|garansi|terpercaya)$/, 'shield-check'],
  [/^(kerjasama|kolaborasi|partner|kemitraan|deal)$/, 'handshake'],
  [/^(bonus|hadiah|gratis|free)$/, 'gift'],
  [/^(cari|search|seo|temukan)$/, 'search'],
  [/^(cepat|instan|langsung|energi)$/, 'zap'],
  [/^(mulai|launch|luncur|start)$/, 'rocket'],
];

/**
 * Pilih ikon dari teks kartu. Mengembalikan nama ikon Lucide; fallback sesuai tipe kartu.
 * card.icon: '' (tanpa ikon) | 'auto' | nama ikon | nilai lama (check/cross/...).
 */
export function resolveIcon(card) {
  const raw = card.icon ?? 'auto';
  if (raw === '' || raw === 'none') return null;
  if (LEGACY_ICON[raw]) return LEGACY_ICON[raw];
  if (raw !== 'auto' && ICON_NAMES.includes(raw)) return raw;
  const words = tokenize([card.title, card.kicker, card.subtitle].join(' ')).map(normWord);
  for (const [re, icon] of RULES) if (words.some((w) => re.test(w))) return icon;
  if (card.cta) return 'circle-arrow-right';
  if (card.type === 'number') return /%|persen/.test(`${card.title} ${card.subtitle}`) ? 'percent' : 'chart-no-axes-combined';
  if (card.type === 'list') return 'list-checks';
  return 'sparkles';
}
