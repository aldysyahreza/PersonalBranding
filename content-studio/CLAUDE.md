# Content Studio The Brand Fixer (CLAUDE.md)

Pemilik: Aldy Syahreza (@aldysyahreza, The Brand Fixer). Sapa dia "Anda". Dia awam teknis: beri langkah sangat rinci untuk apa pun yang perlu dijalankan di terminal. Jangan pakai Trello.

## Apa ini
Dasbor web satu file (`content-studio.html`, vanilla JS, tanpa build) untuk membuat carousel Instagram 1080x1350 dengan gaya "Campaign Pop". Dipublikasikan sebagai Artifact claude.ai: https://claude.ai/artifact/RDAAW9D4Rt7Kp7VVxvuFKM (konten v20 dipublikasikan 27 Okt 2026 = versi layanan 19, capabilities: db, downloads, sample).

## Fitur yang sudah jadi
- Tab: Brief, Pipeline, Studio, Topic Radar, Prompt foto.
- Brief: ide mentah -> `claude.use('sample').json()` -> carousel 8 slide + caption/pinned/story. Cadangan: salin prompt, tempel JSON, impor.
- Studio: edit teks per slide (semua kolom textarea, Enter = baris baru, `@handle` tidak terpisah dari kata sebelumnya), pratinjau langsung, skor kualitas, cek aturan (kata terlarang, batas kata).
- Slide: 1 cover (foto Aldy), 2 adegan (bubble chat + etching landscape 21:9), 3 gejala (bubble chat bernomor), 4 diagnosis (kata besar + lingkaran coretan + highlight amber, tanpa balok terakota), 5 akar (diagram batang 3 node), 6 reframe, 7 langkah (checklist, latar ink), 8 CTA (simpulan, SIMPAN & KIRIM, ikon simpan/kirim, tanpa kursor, tanpa otomasi).
- Upload gambar (IndexedDB 'cs-photos', kunci postId:slideIdx) untuk cover, scene, statement, cta. Semua punya Zoom 100-250, Geser kiri/kanan, Geser atas/bawah (`phz`, `phx`, `phy`, dihitung dari dimensi asli lewat `bgBox`).
- v20: slide berfoto memakai ANATOMI COVER (foto penuh, gradasi `PHSCRIM`, tanda tangan putih, bintang putih kanan atas untuk 6 & 8, blok teks tengah di bagian bawah). Slide 2 punya 3 Gaya gambar: `etching` (default, ciri khas), `foto` (foto penuh seperti cover), `kartu` (foto dalam kartu bulat, tampilan lama). Slide 6/8 tanpa foto tetap warna solid. Foto di slide 2/6/8 bukan wajah Aldy.
- Etching diproses saat unggah (`etchBake`): latar krem dibuang jadi transparan + tepi memudar, supaya pratinjau dan ekspor identik.
- Unduh: PNG slide aktif dan ZIP 8 slide (html-to-image 1.11.11 + jszip 3.10.1 TERTANAM di file, blok `<!-- CS:VENDOR -->`; CDN hanya cadangan; `downloads.save` dengan fallback anchor).
- Font TERTANAM base64 (blok `<!-- CS:FONTS -->`, `<style id="cs-fonts">`, subset latin+latin-ext). Ekspor memberi CSS ini langsung ke html-to-image (`fontEmbedCSS`) setelah `fontsReady()`. Tidak ada request ke Google Fonts. Terbukti identik offline (tests/t20_export_match.js).
- Tabel prompt gambar per slide (cover, scene A etching / B foto nyata, statement & cta opsional, sisanya "dibuat dari kode").
- Penyimpanan: SEED di dalam file, localStorage `cs.local.v1`, db bersama bila tersedia; `migrate(p)` memperbarui data lama berdasar `p.rev` (sekarang 5; v20 tidak mengubah SEED, jadi tanpa migrasi baru).

## Render tanpa browser (v21)
- `node render/render.js posts/*.json [--out dir]` -> PNG 1080x1350 per slide di `out/<slug>/`. Panduan awam: `render/README.md`.
- Cara kerja: Playwright membuka content-studio.html dengan `window.__CS_RENDER__=true`; HTML lalu TIDAK boot (tanpa localStorage/IDB/db) dan mengekspos `window.CSRender.load(post,photos)` + `.show(i)` yang memakai `slideHTML` yang sama. Foto diproses seperti unggahan Studio (maks 1600px JPEG .9).
- JSON post: bentuk sama dengan objek post di SEED + `photos` {nomorSlide: path relatif JSON}. Contoh: `posts/harga-ditawar.json`.
- Terbukti identik dengan unduhan Studio (beda 0,3-1,4%, tepi huruf). Fixture uji: tests/fixture_foto.json, tests/fixture_etching.json.

## Aturan desain (Style Bible v2)
- Palet: Ink #0F0E0C, Paper #FBF8F3, Terakota #B84A2E, Amber #C8944A, Warm Gray #6B6560. Dominan per carousel: terakota atau amber.
- Ritme latar: hero (terakota/amber) hanya cover, slide 6, slide 8. Slide 2-5 paper. Ink hanya slide 7.
- Foto wajah Aldy hanya di cover. Etching hanya slide 2. Slide lain visual dari kode.
- Font: Archivo 800 judul, Fraunces miring satu frasa, Inter/Outfit isi, Caveat catatan, JetBrains Mono label.
- Modern, segar, bukan "old". Tanpa label AI, tanpa kode DX di slide, tanpa teks terbaca di ilustrasi.

## Aturan copy
Natural, kalimat pendek (~14 kata), mulai dari adegan nyata, kata sehari-hari, "saya/kamu", diagnosis lembut. Hindari: Anda harus, wajib, rahasia, strategi jitu, auto, dijamin, hack, kesalahan fatal; istilah konsultan (fondasi, lapisan, ekosistem, sinergi); bunyi AI (pembuka klise, tanda pisah panjang, daftar tiga dipaksakan).
CTA tanpa otomasi (tanpa komentar kata kunci).

## Gotcha teknis
- WAJIB ada `<meta charset="utf-8">` di baris 1. Tanpa itu, karena blok base64 besar di atas, browser salah menebak encoding (kutip “ ” dan → jadi rusak).
- Jangan edit blok CS:FONTS / CS:VENDOR manual. Ubah `assets/fonts-embed.css` atau `vendor/*.js`, lalu `python3 tools/embed_assets.py`.
- Tes ekspor = pratinjau: `MODE=offline node tests/t20_export_match.js` (beda_rata < 5 dan peta beda hanya di tepi huruf = lulus).
- Semua fungsi ada di dalam satu IIFE: untuk tes, gunakan klik UI (mis. `#dl-one`), bukan `page.evaluate` ke fungsi.
- Mengubah teks SEED tidak mengubah data tersimpan pengguna; tambah blok migrasi baru (naikkan `rev`) yang hanya mengganti bila nilai lama masih sama.
- Sejak v19 font & pustaka tertanam, jadi tes tidak butuh intersepsi rute lagi (t10.js lama masih memakainya).
- Artifact dipublikasikan ulang dengan file yang sama agar URL tetap.

## Belum selesai / kandidat lanjutan
1. SELESAI (v19): font + pustaka ditanam; unduhan jalan offline. Tetap cek sekali di browser asli Aldy setelah publish ulang Artifact.
2. Unggah ulang etching slide 2 dan foto cover, cek zoom/geser.
3. Uji A/B etching vs foto nyata di slide 2.
4. Reels Studio (format reels punya viewReels sederhana).
5. Jadwal Topic Radar mingguan, dokumen strategi (https://claude.ai/artifact/XUBf6jHwdpwkMs7QtTu5KA) belum diperbarui.
6. Style Bible v2 sudah ditulis ke Project (`06_STYLE_BIBLE_V2_CAROUSEL.md`); sinkronkan bila aturan berubah.
