# Animatic reels (prototipe)

Reels animasi penuh: visual dibuat dari kode, suara dari voice over Anda.

- `animatic.html`: 7 adegan (observasi, situasi, ketegangan, diagnosis, reframe, pertanyaan, CTA) dengan bahasa visual Style Bible v2. Semua gerak dihitung dari waktu lewat `window.seek(t)`, jadi setiap frame bisa dirender ulang persis sama.
- `render-animatic.js`: Chromium (Playwright) memotret tiap frame lalu ffmpeg menyatukannya jadi MP4 1080x1920 30 fps. Tekniknya sama dengan HyperFrames, tanpa paket tambahan.

```
node animatic/render-animatic.js --out out/animatic.mp4 --stills 1.5
node animatic/render-animatic.js --audio vo.wav --out out/animatic-vo.mp4
```

Butuh: Node.js, Playwright (`npm install` + `npx playwright install chromium`), dan ffmpeg.

## v3 (dikembangkan dari referensi gerak yang Anda pilih)

- `animatic-v3.html`: gaya "buku catatan diagnosis". Kertas grid krem; objek semi-3D (label harga, HP, struk, toko, kartu pin, buku catatan); coretan pena merah; **mode Diagnosis** (pindai garis amber mengubah adegan jadi ink + garis amber); caption karaoke per kata; header bab; stempel DIDIAGNOSIS.
- Transisi: zoom-through, whip pan + blur, pindai, kartu jatuh disematkan, dorong vertikal; kamera terus mendorong pelan; odometer, notifikasi bertumpuk, benda jatuh memantul.
- `sfx-v3.py`: efek suara + musik latar buatan kode (bebas lisensi), sinkron dengan event animasi.

```
python3 animatic/sfx-v3.py out/sfx.wav
node animatic/render-animatic.js --file animatic-v3.html --audio out/sfx.wav --out out/animatic-v3.mp4
```

## Dari rekaman ke reels (satu perintah)

```
python3 animatic/build_reel.py rekaman.m4a posts/reels-harga-ditawar.json out/reel
```

1. `vo_prep.py` menjernihkan suara: buang dengung (high-pass 80 Hz), redam bising (RNNoise, model `models/sh.rnnn` diunduh otomatis; cadangan afftdn), jinakkan desis (EQ 6,5 kHz; filter deesser ffmpeg sengaja tidak dipakai karena terukur menimbulkan artefak), kompresor, -16 LUFS. Lalu buang napas/klik, cocokkan potongan bicara ke frasa naskah (kecepatan suku kata + intonasi naik untuk pertanyaan), dan atur jeda baku: koma 0,18 dtk, kalimat 0,35, antar langkah 0,55, awal 0,25, akhir 0,6. Hasil: `vo_clean.wav`, `timing.json` (waktu per kata), `laporan.txt`.
2. `sfx-v3.py --timing` membuat musik dan efek yang mengikuti waktu suara.
3. Campuran: musik mengecil saat Anda bicara (sidechain), -14 LUFS, puncak -1,5 dBTP.
4. Pemeriksa tata letak (`tests/t30_animatic_layout.js`) berjalan dengan waktu suara.
5. Render `reel.mp4`. Langkah yang lebih pendek dari rancangan animasinya otomatis dipercepat.

Catatan: tanpa alat transkripsi, kata dicocokkan dari pola suara, bukan didengar. Bila Anda berimprovisasi jauh dari naskah, cek caption di hasil akhir.

Status: prototipe. Durasi tiap adegan masih perkiraan dari naskah. Langkah berikutnya: durasi diambil otomatis dari voice over (stempel waktu per kata), subtitle kinetik per kata, dan efek suara buatan kode.
