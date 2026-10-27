# Personal Branding Video Studio

Aplikasi **lokal** untuk mengubah video talking head raw menjadi video personal branding yang siap ditinjau dan diekspor: subtitle tersinkron, penekanan kata, kartu visual, b-roll milik sendiri, musik & SFX, koreksi warna, preview, dan ekspor ffmpeg. Preset awal: **"Aldy — Editorial Talking Head"** (konsep yang dapat diubah).

> Status jujur: alat lokal tahap awal (v0.1). Belum diuji oleh pengguna sungguhan dan bukan produk "produksi". Fitur AI bersifat opsional dan **tidak terhubung** sampai Anda mengisi API key sendiri.

## Menjalankan

Kebutuhan wajib: **Node.js ≥ 20** dan **ffmpeg + ffprobe** dengan libass (paket ffmpeg standar di macOS Homebrew / Ubuntu / Windows "full build" sudah menyertakannya).

```bash
npm install          # opsional: hanya memasang SDK Claude (untuk fitur rencana AI)
npm run check        # memeriksa ffmpeg, libass, transkripsi lokal, key (tanpa mencetak key)
npm start            # buka http://127.0.0.1:4317
npm test             # unit test logika inti
```

Opsional:
- **Transkripsi lokal (disarankan, data tidak keluar):** `pip install faster-whisper`. Model (default `small`) diunduh otomatis dari Hugging Face saat pertama dipakai — butuh internet sekali.
- **Cloud:** salin `.env.example` → `.env`, isi `OPENAI_API_KEY` (transkripsi) dan/atau `ANTHROPIC_API_KEY` (rencana edit Claude). Jalankan ulang aplikasi.

## Alur kerja

| Langkah | Yang dilakukan | Catatan |
|---|---|---|
| 1. Proyek | Buat proyek, impor video (unggah = disalin; atau path lokal = hanya dibaca). Lihat nama, durasi, resolusi, rasio, fps, codec, ukuran, status. Pilih rasio output (default 9:16). Jalankan **Analisis** (level audio + deteksi hening). | Sumber tidak pernah ditulis/dipindah. |
| 2. Transkrip | Whisper lokal / OpenAI (dengan dialog persetujuan) / ketik-tempel / impor `.srt`/`.vtt`. Koreksi teks, timestamp, pembicara; pisah/gabung/sembunyikan segmen; klik kata untuk penekanan. Tandai "sudah dikoreksi". | Segmen yang teksnya diubah ditandai dan teks asli tetap terlihat. Waktu estimasi diberi label. |
| 3. Rencana edit | Saran **aturan lokal** (atau **Claude**, opsional): struktur hook/isi/penutup, penekanan, kartu angka/poin, **zoom punch-in** antar kalimat, ide b-roll, SFX, musik, cut (jeda, tepi, kata pengisi, pengulangan). | Semua saran berlabel asalnya dan **belum disetujui**. Kartu dengan kata yang tidak diucapkan ditandai. |
| 4. Editor | Preview 9:16 dengan overlay (subtitle, kartu, b-roll, warna, musik, lompat cut), timeline yang bisa diseret, panduan zona aman & wajah, kontrol gaya/bingkai/warna/audio/aset, undo/redo (Ctrl+Z / Ctrl+Shift+Z). **Cek frame akurat** & **Render pratinjau** memakai pipeline ffmpeg yang sama dengan ekspor. | Preview browser = perkiraan cepat; frame akurat = hasil sebenarnya. |
| 5. Ekspor | Pemeriksaan (masalah & peringatan), rasio (9:16 1080×1920, 4:5, 1:1, 16:9), kualitas, format (MP4/MOV), folder output, perkiraan ukuran, progres, batal, riwayat. | "Ekspor selesai" hanya setelah file diverifikasi (ffprobe + decode frame + durasi). |

## Lokasi penting

| Apa | Di mana |
|---|---|
| Data proyek (JSON, salinan unggahan, aset, file kerja) | `projects/<id>/` (di-.gitignore) |
| Hasil ekspor | `output/<nama-proyek>/<nama>_<rasio>_<kualitas>_<waktu>.mp4` (di-.gitignore) |
| Musik & SFX bawaan (cache) | `library/` (dibuat otomatis) |
| Preset gaya | `config/presets/*.json` — `aldy-editorial.json` + preset yang Anda simpan dari Editor |
| Profil brand (fakta/asumsi) | `docs/BRAND_PROFILE.md`, `server/lib/brand.js` |
| Analisis referensi | `docs/REFERENCE_ANALYSIS.md` |
| Font (Inter, OFL) | `assets/fonts/` |
| Konfigurasi & secret | `.env` (tidak pernah di-commit; lihat `.env.example`) |

Lokasi `projects/` dan `output/` dapat diubah via `PROJECTS_DIR` / `OUTPUT_DIR` di `.env`.

## Preset gaya

`config/presets/aldy-editorial.json` berisi semua nilai yang dapat diubah: warna, font, ukuran & posisi subtitle, layout (`stack`/`single`/`karaoke`), penekanan (`box`/`color`/`none`), animasi, kartu, zona aman & wajah, koreksi warna (dengan `intensity`), level audio. `styleLevels` mendefinisikan **minimal / editorial / dinamis** sebagai override. Gaya disalin ke tiap proyek, jadi perubahan di Editor tidak mengubah preset; gunakan "Simpan sebagai preset" untuk membuat preset baru.

## Arsitektur

Dipilih yang paling sederhana untuk dipelihara: **Node.js tanpa framework + ffmpeg**, UI **vanilla JS** tanpa build step.

```
server/index.js          HTTP API + file statis (127.0.0.1)
server/lib/media.js      ffprobe, deteksi hening, level audio (hanya baca)
server/lib/projects.js   penyimpanan proyek (JSON atomik)
server/lib/transcribe.js penyedia STT: lokal / OpenAI / manual
server/lib/plan.js       saran aturan + Claude (opsional) + verifikasi teks kartu
server/lib/ass.js        subtitle & kartu → ASS (libass)
server/lib/render.js     filter graph ffmpeg: cut + zoom punch-in → reframe → warna → b-roll → ASS → audio mix; verifikasi output
server/lib/synth.js      musik & SFX sintetis bawaan (WAV, bebas royalti)
public/shared/core.js    logika bersama server & browser (cut, pemetaan waktu, frasa subtitle) → preview = aturan render
public/js/…              UI (store + undo/redo, views, preview, timeline)
scripts/transcribe_local.py  faster-whisper
```

## Privasi & keamanan
- Server hanya mendengarkan di `127.0.0.1`, menolak Host asing (DNS rebinding) dan permintaan tulis tanpa header aplikasi (CSRF lokal).
- Tidak ada data yang keluar tanpa aksi + persetujuan eksplisit: OpenAI menerima **audio saja**, Claude menerima **teks transkrip saja**.
- API key hanya dibaca dari `.env` di server, tidak pernah dikirim ke browser, ditulis ke log, atau disimpan di proyek/ekspor.
- Tidak ada pembuatan wajah/suara/ucapan sintetis, dan tidak ada footage stok/generatif otomatis.
- **Pustaka audio bawaan** (`server/lib/synth.js`): 3 musik latar (Tenang 84 BPM, Fokus 100 BPM, Energik 118 BPM, loop ±40–45 dtk) dan 8 SFX (pop, klik, whoosh, swoosh, riser, impact, ding, notifikasi) disintesis dari nol (osilator, noise, filter) — bukan sampel pihak lain, bebas royalti. File dibuat sekali ke `library/` (di-.gitignore). Musik/SFX milik sendiri tetap bisa diimpor dengan catatan lisensi.
- Menghapus proyek hanya menghapus folder proyek; file sumber yang direferensikan dan folder output tidak disentuh.

## Batasan yang diketahui
- Transkripsi otomatis perlu faster-whisper (lokal) atau OpenAI key; tanpa itu, waktu transkrip manual adalah **estimasi** dari deteksi hening dan perlu dikoreksi.
- Deteksi pembicara (diarization) belum ada — label pembicara diisi manual.
- Zoom punch-in hanya berlaku pada mode bingkai "Isi" (bukan "Muat + latar blur").
- Musik bawaan sengaja sederhana (latar instrumental); untuk karakter musik yang kuat, impor musik berlisensi.
- Deteksi wajah otomatis tidak ada; "zona wajah" adalah panduan yang Anda atur.
- Preview browser memakai CSS untuk warna & tidak memutar SFX/ducking — gunakan "Render pratinjau" untuk campuran final.
- Codec yang tidak didukung browser (mis. HEVC di beberapa browser) tidak bisa dipreview langsung, tetapi tetap bisa dirender.
- Render frame akurat men-decode dari awal video, jadi lebih lambat untuk video panjang.
- Ekspor berjalan satu per proyek; status job disimpan di memori (hilang bila server dimatikan; riwayat ekspor tetap tersimpan di proyek).
