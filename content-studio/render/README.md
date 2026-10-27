# Render carousel tanpa membuka browser

Satu perintah mengubah file JSON post menjadi 8 PNG 1080x1350. Hasilnya sama dengan tombol "Unduh" di Studio, karena memakai kode desain yang sama (`content-studio.html`).

## Persiapan (sekali saja per komputer)

1. Pasang **Node.js** versi LTS dari https://nodejs.org (klik tombol hijau, lalu ikuti penginstal sampai selesai).
2. Buka terminal di folder proyek ini:
   - **Mac:** buka aplikasi Terminal, ketik `cd ` (dengan spasi), seret folder proyek ke jendela Terminal, lalu tekan Enter.
   - **Windows:** buka folder proyek di File Explorer, klik bilah alamat, ketik `cmd`, lalu tekan Enter.
3. Ketik perintah berikut, tekan Enter setelah tiap baris, dan tunggu sampai selesai:
   ```
   npm install
   npx playwright install chromium
   ```
   Perintah pertama memasang Playwright, yaitu alat yang mengendalikan browser. Perintah kedua mengunduh browser Chromium khusus untuk render (sekitar 150 MB).

## Render satu post

```
npm run render -- posts/harga-ditawar.json
```

Hasilnya ada di folder `out/<judul-post>/slide-01.png` sampai `slide-08.png`.

- Semua post sekaligus: `npm run render -- posts/*.json`
- Folder hasil lain: `npm run render -- posts/harga-ditawar.json --out D:/carousel`

Render tidak butuh internet, karena font dan semua aset sudah tertanam di dalam file.

## Dari Studio ke skrip, dan sebaliknya

- **Studio → skrip:** buka post di Studio, klik **Ekspor JSON**, lalu simpan file ke folder `posts/`. Foto yang sudah Anda unggah ikut tertanam di file, jadi langsung bisa dirender: `npm run render -- posts/nama-file.json`.
- **Skrip → Studio:** di Studio atau Pipeline, klik **Impor JSON** dan pilih satu atau beberapa file. Post lama tidak pernah ditimpa: kalau post yang sama sudah ada, hasil impor menjadi post baru berlabel "(impor)". Foto yang ditulis sebagai lokasi file tidak bisa dibaca browser, jadi unggah ulang di Studio.

## Menambahkan foto

Di file JSON, isi bagian `"photos"`. Kuncinya nomor slide (1–8), nilainya lokasi file foto, ditulis relatif terhadap file JSON:

```json
"photos": {
  "1": "../foto/cover-look1.jpg",
  "2": "../foto/etching-slide2.png",
  "6": "../foto/suasana-toko.jpg"
}
```

- Slide 1: foto wajah Anda (hanya di cover).
- Slide 2: etching (default), atau foto penuh bila di slide 2 ada `"imgmode": "foto"`.
- Slide 6 dan 8: foto suasana, tangan, atau objek, tanpa wajah. Slide tampil seperti cover.
- Zoom dan geser bisa diatur per slide lewat `"phz"` (100–250), `"phx"` dan `"phy"` (0–100). Nilainya sama dengan slider di Studio.

## Kalau ada pesan error

| Pesan | Artinya | Yang dilakukan |
|---|---|---|
| `Playwright belum terpasang` | Langkah persiapan belum dijalankan | Jalankan `npm install` lalu `npx playwright install chromium` |
| `Foto slide N tidak ditemukan` | Lokasi foto di JSON salah | Cek ejaan nama file dan foldernya |
| `JSON tidak punya "slides"` | File JSON rusak atau tidak lengkap | Ekspor ulang dari Studio, atau salin dari `posts/harga-ditawar.json` |
