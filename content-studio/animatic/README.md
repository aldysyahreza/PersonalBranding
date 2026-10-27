# Animatic reels (prototipe)

Reels animasi penuh: visual dibuat dari kode, suara dari voice over Anda.

- `animatic.html`: 7 adegan (observasi, situasi, ketegangan, diagnosis, reframe, pertanyaan, CTA) dengan bahasa visual Style Bible v2. Semua gerak dihitung dari waktu lewat `window.seek(t)`, jadi setiap frame bisa dirender ulang persis sama.
- `render-animatic.js`: Chromium (Playwright) memotret tiap frame lalu ffmpeg menyatukannya jadi MP4 1080x1920 30 fps. Tekniknya sama dengan HyperFrames, tanpa paket tambahan.

```
node animatic/render-animatic.js --out out/animatic.mp4 --stills 1.5
node animatic/render-animatic.js --audio vo.wav --out out/animatic-vo.mp4
```

Butuh: Node.js, Playwright (`npm install` + `npx playwright install chromium`), dan ffmpeg.

Status: prototipe. Durasi tiap adegan masih perkiraan dari naskah. Langkah berikutnya: durasi diambil otomatis dari voice over (stempel waktu per kata), subtitle kinetik per kata, dan efek suara buatan kode.
