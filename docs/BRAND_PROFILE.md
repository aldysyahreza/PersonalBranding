# Profil brand — Aldy Syahreza (The Brand Fixer)

> Versi terstruktur yang dipakai aplikasi ada di `server/lib/brand.js` (menu **Profil brand & sistem**). Perbarui keduanya bersamaan.

## Sumber
1. Preferensi profil yang ditulis Aldy di pengaturan Claude.
2. Artifact milik Aldy di Claude (dibaca 29 Okt 2026):
   - **Brand Fixer OS**: playbook proyek "Personal Branding Aldy Syahreza".
   - Design system **The Brand Fixer**: Visual System v2 — Editorial Diagnosis, `tokens.json`, komponen Reels/Stickers, riset referensi @mobileeditingclub.

Semua isinya dinyatakan sendiri oleh Aldy dan belum diverifikasi pihak ketiga. Tidak ada data yang diambil dari web atau media sosial.

## 1. Fakta bersumber
- **Positioning:** Aldy Syahreza — The Brand Fixer.
- **Core idea:** "Brand kamu sudah jalan. Tapi belum naik kelas."
- **Big idea:** Masalah bisnis sering bukan kurang konten, tetapi brand belum cukup jelas.
- **Audiens:** owner yang bisnisnya sudah berjalan, bukan pemula.
- **Brand-Up System:** Clarity · Trust · Premium · System · Content.
- **Case tag:** 7 lapis, DX·01 Foundation sampai DX·07 AI-Era Visibility.
- **Pilar konten:** 45% Brand Diagnosis · 25% Quiet Builders · 20% Director's Mind · 10% AI as Strategic Tool.
- **Warna:** paper #FBF8F3 · cream #F4EBD9 · sand #E7DDCD · ink #0F0E0C · ink-soft #2A2824 · warm gray #6B6560 · terracotta #B84A2E (garis/bidang, maks 2 elemen per slide) · terracotta-ink #9E3F25 · amber #C8944A.
- **Tipografi:**
  - Archivo 800: kata tegas.
  - Fraunces Italic: frasa rasa, satu per blok.
  - Outfit: lead dan body.
  - Caveat: catatan tangan.
  - JetBrains Mono: case tag.

## 2. Aturan reels dari bible (diterapkan di preset `brand-fixer`)

| Aturan | Implementasi di aplikasi |
|---|---|
| Hook 0–1,2 dtk, kata besar slam 112%→100% dalam 6 frame | Hook lockup (lead → kata besar → Fraunces), 200 ms; diambil dari kata pembuka yang diucapkan |
| Caption 2–4 kata, Archivo putih + maks 1 kata Fraunces | Caption kinetik, `maxWords` 4, penekanan `serif` |
| Zona aman x 60–880, y 250–1500 | `safeZone` top 13%, bottom 22%, right 18,5% |
| Scrim di bawah teks di atas foto | Overlay gradien 0→62% di bawah frame |
| Markup terracotta tergambar 12–15 frame, maks 1× | Lingkaran/coretan/centang tergambar ±0,45 dtk di kartu |
| UI melayang (chat) dengan radius 28 + shadow | Kartu `chat` overlay transparan, berlabel "ILUSTRASI · DARI UCAPAN" |
| End card 2 dtk, ink-soft, lockup + pill | Ditambahkan setelah video; teks bible perlu persetujuan; pill kosong secara default |
| Grading hangat, saturasi −10, hitam diangkat, grain 5–8% | `color` saturation 0,9, warmth, lift 0,03, grain 0,06 |
| Tanpa transisi zoom/whoosh, audio meme, caption berwarna-warni, emoji | Palet SFX `quiet` (klik/pop halus), caption putih, potong keras |

## 3. Asumsi (perlu dikonfirmasi)
- **Ukuran caption:** 100px @1080, sengaja lebih besar dari token bible (68px) agar terbaca di talking head.
- **Ritme:** gerak kinetik kata-per-kata dari video referensi; gaya visual tetap dari bible.

## 4. Belum diketahui
- Keyword CTA aktif saat ini.
- Platform prioritas dan handle untuk end card.
- Library musik berlisensi.
- Foto bank bulanan untuk tile kartu.
