# Analisis video referensi

**File:** unggahan `johnogwum_pindown.io_1785498973.mp4` (kreator lain — dipakai hanya sebagai acuan ritme & visual, bukan template).
**Metode:** `ffprobe` (metadata), kontak-sheet 1 fps (36 frame), `scdet` (deteksi pergantian adegan), `volumedetect`, `silencedetect`.
**Batasan:** audio **tidak** didengarkan dan **tidak** ditranskripsi. Isi narasi tidak dianalisis; teks yang terlihat di layar hanya dibaca dari frame. Tidak ada logo, kalimat, atau aset referensi yang disalin ke aplikasi.

## Fakta teknis
- 720 × 1280, 9:16, 30 fps, 34,9 detik, H.264 + AAC.
- Pergantian adegan terdeteksi di ±4,5 · 7,1 · 13,1 · 15,1 · 16,2 · 18,0 · 26,0 · 28,3 dtk.
- Audio: mean −22,7 dB, puncak −7 dB; tidak ada jeda hening ≥ 0,3 dtk pada −35 dB (kemungkinan ada musik latar atau jeda sudah dipotong — tidak dapat dipastikan tanpa mendengar).

## Pengamatan visual
| Aspek | Yang terlihat | Diterjemahkan ke preset sebagai |
|---|---|---|
| Pacing | Shot 2–6 dtk; kartu sisipan 1–2,5 dtk; ada punch-in ringan pada talking head | Kartu default ±2 dtk; saran b-roll bila talking head > 6 dtk; zoom reframe tersedia |
| Komposisi | Medium/medium-close, wajah di sepertiga atas, mikrofon terlihat, meja putih di bawah | Zona wajah default 14–50% tinggi; subtitle di ±64% (setinggi dada) |
| Subtitle | Dua tingkat: baris kecil (regular) di atas, baris besar (extra bold) di bawah; 1–4 kata; kata kunci diberi blok merah | Layout `stack`, maks 4 kata, penekanan `box` warna aksen |
| Warna | Latar gelap, lampu praktikal hangat, kulit natural, kontras sedang | Kontras +8%, saturasi +6%, kehangatan kecil, vignette ringan, intensitas 60% |
| Kartu | Layar terang abu-putih bertekstur, tipografi besar, angka besar merah dengan grid tipis, ikon sederhana | Kartu layar penuh `#F3F2EF`, angka aksen + grid, ikon vektor sederhana |
| Transisi | Potongan langsung; teks masuk dengan skala/fade singkat | Hard cut; animasi `pop`/`fade` ≤ 160 ms |
| Nuansa | Rapi, edukatif, mobile-first | Satu warna aksen, sisanya netral |

## Yang sengaja tidak ditiru
- Font tulisan tangan/script dan efek 3D pada teks referensi (diganti tipografi Inter yang bersih).
- Identitas, kalimat, dan aset kreator referensi.
- Pengubahan wajah/penampilan apa pun.
