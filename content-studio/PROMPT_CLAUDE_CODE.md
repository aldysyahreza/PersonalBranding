# Prompt untuk Claude Code (tempel apa adanya)

Saya Aldy Syahreza. Anda melanjutkan proyek "Content Studio The Brand Fixer" yang sebelumnya dikerjakan di Claude (claude.ai).

LANGKAH PERTAMA
1. Baca `CLAUDE.md` di folder ini sepenuhnya. Itu konteks, aturan desain, aturan copy, dan jebakan teknis.
2. Buka `content-studio.html`. Ini sumber utama (satu file, tanpa build). Jangan menulis ulang dari nol. Ubah secara bertahap.
3. Jalankan tes cepat untuk memastikan semuanya hidup: pasang Playwright (`npm i playwright` lalu `npx playwright install chromium`), lalu jalankan `node tests/t15.js` dan `node tests/t16.js` dari folder ini. Jelaskan setiap perintah kepada saya sebelum menjalankan, karena saya awam teknis.

CARA KERJA
- Panggil saya "Anda". Jawaban ringkas, terstruktur, berbahasa Indonesia.
- Sebelum mengubah sesuatu yang besar, beri saya satu rekomendasi dan alasannya. Untuk hal kecil, langsung kerjakan.
- Setiap perubahan visual: render slide dengan Playwright, lihat hasilnya sendiri, lalu laporkan. Pastikan unduhan PNG sama dengan pratinjau.
- Jangan membuat otomasi komentar-kata-kunci di CTA. Jangan menambah kode DX di slide. Foto wajah saya hanya di cover.
- Jangan pakai Trello.
- Simpan cadangan (`content-studio.vNN.bak`) sebelum perubahan besar. Jika mengubah SEED, tambahkan migrasi `rev` baru.

TUGAS BERIKUT (urut prioritas, kerjakan satu per satu dan tunjukkan hasilnya)
1. Pastikan font (Archivo, Fraunces, Inter/Outfit, Caveat, JetBrains Mono) ikut ter-render di PNG hasil unduhan, meski offline. Jika perlu, tanam font sebagai base64 agar tidak bergantung pada Google Fonts.
2. Ubah alur menjadi skrip yang bisa dijalankan ulang di komputer saya: satu perintah yang membaca data carousel (JSON) dan menghasilkan 8 PNG 1080x1350 dengan Playwright, tanpa membuka browser manual. Taruh di folder `render/`.
3. Pindahkan data carousel dari dalam HTML ke file JSON per post (`posts/*.json`) dan buat skrip untuk memuatnya ke Studio, tanpa merusak penyimpanan yang ada.
4. Tambahkan Reels Studio yang setara dengan carousel: skrip face reels (struktur 7 langkah: observasi, situasi relatable, ketegangan, diagnosis, reframe, pertanyaan reflektif, CTA lembut), daftar shot, dan checklist produksi.
5. Perluas modul visual slide agar ada variasi per topik (bukan hanya kasus "harga ditawar"), tetap dalam Style Bible v2.

DEFINISI SELESAI
Setiap tugas selesai bila: sudah dijalankan dan dilihat hasilnya, tidak ada error di konsol, PNG unduhan sama dengan pratinjau, dan saya mendapat ringkasan satu paragraf tentang apa yang berubah dan apa langkah berikutnya.
