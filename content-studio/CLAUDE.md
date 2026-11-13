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

## Impor/ekspor JSON (v22)
- Studio: tombol Ekspor JSON (post aktif + foto tertanam sebagai data URL di `photos`) dan Impor JSON (Studio & Pipeline, bisa banyak file). Format = posts/*.json, jadi file ekspor langsung bisa dirender `render/render.js`.
- Impor TIDAK PERNAH menimpa: ID yang sudah ada -> post baru dengan judul '(impor)'. Foto berupa path file dilewati (dilaporkan di toast); data URL divalidasi ketat (`DATA_IMG`). Kolom divalidasi & dinormalisasi ke 8 slide ORDER.
- Tes: tests/t24_json_roundtrip.js.

## Reels Studio (v25, struktur HRIRC)
- Post format `reels` membuka Reels Studio: tab Cover + 5 babak HRIRC (Hook, Relate, Insight, Reframe, CTA). Per babak: `say` (ucapan), `txt` (teks layar, satu frasa Fraunces ditandai *bintang*), `shot` (kunci SHOTS), `dur` (kosong = 2,5 kata/detik + 0,4).
- Elemen alur wajib = kolom perencanaan per babak (BEAT_REQ): Relate `case` (studi kasus, jangan dikarang), Insight `solusi` (satu langkah), Reframe `contoh` (wujudnya). Kosong -> "Temuan" di panel cek.
- Hook 2 lapis: `reel.angle` (HOOK_ANGLE: kontradiksi, angka, rugi, cermin, tes, tanya) × `reel.exec` (HOOK_EXEC: coretan, layar, angka, chat, pindai, banding). Rancangan Claude, disetujui Aldy 29 Okt 2026 sebagai titik awal; ubah di kode bila Aldy menambah/mencoret.
- Data `p.reel`: v=2, beats[5], angle, exec, prod{}, coverH, coverHi. `reelInit` memigrasi data 7 langkah lama otomatis (Observasi->Hook, Situasi+Ketegangan->Relate, Diagnosis->Insight, Reframe+Pertanyaan->Reframe, CTA->CTA), cadangan di `reel.legacy7`. Tidak mengubah SEED.
- Pratinjau 9:16, daftar shot otomatis, checklist produksi, unduh cover 1080x1920 tetap seperti v23. Cek: hook > 4 dtk, hook belum 2 lapis, kolom wajib kosong, kalimat > 14 kata, teks layar > 4 kata, > 1 frasa Fraunces, kata terlarang/kaku, ctaCheck di babak CTA, total 30-45 dtk.
- Tes: tests/t25_reels.js (termasuk migrasi). Contoh: posts/reels-harga-ditawar.json (HRIRC v2; studi kasus/solusi/contoh sengaja kosong = Temuan terbuka).

## Reels animatic (v4, DISETUJUI Aldy 28 Okt 2026, gaya TERKUNCI)
- Satu perintah: `python3 animatic/build_reel.py rekaman.m4a posts/<reels>.json out/reel` -> reel.mp4. Aldy hanya mengirim voice over; visual dari kode.
- Gaya: buku catatan diagnosis (kertas grid krem, objek semi-3D, coretan pena merah Caveat, mode Diagnosis ink+amber lewat pindai, caption karaoke pill ink, header bab, stempel DIDIAGNOSIS). Teknik gerak diadaptasi dari referensi @decoyreport, bukan disalin.
- Audio: vo_prep.py (RNNoise + EQ desis, JANGAN deesser ffmpeg; jeda koma 0,18 / kalimat 0,35 / langkah 0,55), musik di-duck sidechain, -14 LUFS, limiter -2,5 dB (AAC menambah puncak).
- Babak narasi (HRIRC, 5) terpisah dari adegan visual (7 di v3): anchors-v3.json `scenes` = kata pembuka tiap adegan + babaknya; build_reel.to_scenes memetakan timing per babak ke per adegan (kata pembuka dicari hanya di babaknya). Label bab di video = babak HRIRC.
- Sinkron: anchors-v3.json mengikat momen visual ke kata; animasi + efek suara memakai peta waktu yang sama. Pencocokan kata tanpa ASR (DP suku kata + intonasi naik untuk tanya): cek caption bila Aldy improvisasi.
- QC wajib sebelum kirim: tests/t30_animatic_layout.js (tanpa tabrakan) + cek frame visual (kesejajaran) + loudness.
- Jangan pakai pkill -f dengan pola yang ada di baris perintah sendiri (membunuh shell). Jangan loudnorm di dalam filtergraph bersama asplit/sidechain (ffmpeg macet).

## Standar suara Aldy (WAJIB untuk semua copy, 28 Okt 2026)
- Pembaca: business owner omzet > Rp100 juta/bulan. Nada profesional, berbeda, bernilai, tidak kaku: bicara dengan owner di satu meja, bukan seminar.
- Tes tiap kalimat: owner paham dalam sekali baca tanpa penjelasan tambahan? Kalau belum, tulis ulang.
- Kata kaku/bunyi AI yang dihindari: nyata, relevan, krusial, esensial, signifikan, optimal, holistik, sinergi, transformasi, lanskap, "di era digital ini", "mari kita", "pada dasarnya", "tidak hanya... tetapi juga". Ganti dengan bahasa owner saat membicarakan bisnisnya sendiri.
- Istilah abstrak (sinyal, positioning yang kuat, value) wajib diterjemahkan jadi hal yang owner lihat/dengar/lakukan. Contoh: "AI membaca sinyal yang paling jelas" -> "AI memilih brand yang paling jelas: jualan apa, untuk siapa, dan kenapa harus dipilih."
- STRUKTUR BAKU REELS: HRIRC = Hook – Relate – Insight – Reframe – CTA. Hook memakai sistem hook 2-lapis (angle psikologis × eksekusi khas brand).
- Cek CTA (berlaku sampai Aldy mengubahnya): CTA hanya SATU dari save · share · follow; tanpa keyword, tanpa ajakan DM, tanpa otomasi; harus terhubung dengan isi (kenapa disimpan, dikirim ke siapa, apa yang didapat kalau follow). CTA komentar/keyword = pelanggaran. Diperiksa otomatis di Studio (ctaCheck, juga pinned comment).
- Alur wajib lengkap: 1 Problem spesifik, 2 Studi kasus (brand/situasi konkret, JANGAN dikarang: pakai kasus klien yang disamarkan atau publik bersumber), 3 Solusi satu langkah, 4 Contoh wujudnya, 5 CTA. Dibungkus storytelling karakter Aldy ("saya", director yang mendiagnosis). Reels: kelima elemen masuk struktur HRIRC. Elemen hilang/kabur -> tulis di bagian "Temuan".

## Keputusan topik (29 Okt 2026)
- DISETUJUI: topik 2 "Laporan marketplace bilang Rp100 juta, rekening bilang Rp79 juta" (selisih marketplace >21%, biaya terbesar admin + iklan, beli ulang 30-50% (direvisi Aldy 29 Okt; sebelumnya 20-30%), hit and run). Naskah: posts/reels-omzet-marketplace.json.
- DITOLAK Aldy: topik 1 (AI tidak menyebut bisnismu) dan topik 3 (barang impor murah, belum pernah menangani). Jangan diangkat lagi tanpa diminta.
- Studi kasus: tidak punya kasus klien yang boleh diceritakan sebelum ada pemicu topik. Boleh pakai kasus publik tanpa nama brand (syarat: sumber bisa dicek, nama diganti deskripsi, tidak dibingkai sebagai klien, sumber disimpan, detail identitas dihapus bila negatif). Per 29 Okt belum ada kasus publik terverifikasi untuk topik 2; compas.co.id dan ecommercefastlane.com tidak bisa dibuka dari sesi cloud (perlu diizinkan di pengaturan jaringan).
- Jenis bisnis yang pernah didampingi Aldy: jasa, skincare, vape, herbal, fashion, F&B, personal branding; omzet Rp100 juta sampai di atas Rp1 miliar. Masalah dominan: manajemen tim, strategi marketing dan sosial media, brand belum kuat/hilang arah dan positioning. Metodenya: assessment dan analisis dulu, baru strategi. Hasil terlihat paling cepat 6 bulan.

- CTA: penonton adalah business owner, JANGAN 'kirim ke owner lain'. Arahkan share ke tim/partner/orang yang pegang bisnisnya, atau save dengan alasan. Hindari 'malam ini', pakai 'hari ini'. Kata 'dibuat' dan 'isi ulang' di kartu dianggap tidak kuat/susah dipahami.
- Istilah: jangan tulis "aplikasi" untuk marketplace (ambigu). Pakai "laporan penjualan marketplace" / "laporan marketplace" (Aldy, 29 Okt 2026).

## Aturan desain (Style Bible v2)
- Palet: Ink #0F0E0C, Paper #FBF8F3, Terakota #B84A2E, Amber #C8944A, Warm Gray #6B6560. Dominan per carousel: terakota atau amber.
- Ritme latar: hero (terakota/amber) hanya cover, slide 6, slide 8. Slide 2-5 paper. Ink hanya slide 7.
- Foto wajah Aldy hanya di cover. Etching hanya slide 2. Slide lain visual dari kode.
- Font: Archivo 800 judul, Fraunces miring satu frasa, Inter/Outfit isi, Caveat catatan, JetBrains Mono label.
- Modern, segar, bukan "old". Tanpa label AI, tanpa kode DX di slide, tanpa teks terbaca di ilustrasi.

## Aturan copy
Natural, kalimat pendek (~14 kata), mulai dari adegan nyata, kata sehari-hari, "saya/kamu", diagnosis lembut. Hindari: Anda harus, wajib, rahasia, strategi jitu, auto, dijamin, hack, kesalahan fatal; istilah konsultan (fondasi, lapisan, ekosistem, sinergi); bunyi AI (pembuka klise, tanda pisah panjang, daftar tiga dipaksakan).
CTA: lihat 'Cek CTA' di Standar suara Aldy.

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
4. SELESAI (v23): Reels Studio. Lanjutan: Brief -> naskah reels otomatis lewat claude.use('sample'), foto Aldy untuk cover reels.
5. Jadwal Topic Radar mingguan, dokumen strategi (https://claude.ai/artifact/XUBf6jHwdpwkMs7QtTu5KA) belum diperbarui.
6. Style Bible v2 sudah ditulis ke Project (`06_STYLE_BIBLE_V2_CAROUSEL.md`); sinkronkan bila aturan berubah.

## Reels topik 2 (29 Okt 2026): set adegan "omzet"
- Set adegan = animatic-<nama>.html + anchors-<nama>.json + sfx-<nama>.py, dipilih lewat argumen ke-4 build_reel.py: `python3 animatic/build_reel.py rekaman.mp4 posts/reels-omzet-marketplace.json out/reel2 omzet` (default `v3` = topik harga ditawar).
- Hasil: out/reel2/reel.mp4 (49,8 dtk, -14,5 LUFS, puncak -2,2 dBFS). Hook 6,3 dtk (> 4) dan total > 45 dtk: terbuka untuk dipangkas.
- Terbuka: tarif admin per sumber belum diverifikasi di Seller Centre, aturan marketplace soal kartu/voucher belum dicek, angka 30-50% dari Aldy.

## Evaluasi reels topik 2 -> aturan reels berikutnya (29 Okt 2026)
- Video topik 2 dipakai sebagai bahan evaluasi, tidak direvisi. Terapkan di reels berikutnya: hook maksimal 4 dtk (satu kalimat, angka/kontradiksi di 1,5 dtk pertama), total 35-45 dtk (naskah maks ~95 kata), satu langkah solusi saja, tidak ada angka tanpa sumber atau label "contoh hitungan".

## Reels topik "arah brand / persona brand" (29 Okt 2026): set adegan "arah"
- Naskah final v7: posts/reels-persona-brand.json (hook cermin × chat "Tanya tim kontenmu: brand ini mau dibawa ke mana?", Reframe 3 baris persona brand dengan contoh skincare kulit sensitif, CTA save). Dihindari atas permintaan Aldy: "teman yang jujur", "serum yang tidak janji berlebihan", "satu hal yang ditolak", CTA kirim ke tim.
- Build: `python3 animatic/build_reel.py /home/user/vo/vo3_raw.ogg posts/reels-persona-brand.json out/reel3 arah`. Hasil: out/reel3/reel.mp4 (50,8 dtk > batas 45; hook 3,8 dtk OK; -14,9 LUFS).
- Adegan: 8 (chat grup, 3 jawaban, diagnosis jembatan, tulis 3 baris, kartu persona x3, simpan). Generator di scratchpad, HTML hasil: animatic/animatic-arah.html.

## Durasi reels (Aldy, 29 Okt 2026) - menggantikan batas 45 dtk
- Total sampai 60 dtk masih aman (target 40-55 dtk, naskah maks ~130 kata). Hook tetap maks 4 dtk. Studio masih menandai > 45 dtk; ubah ambang di reelAnalyze bila perlu.
- CTA reels berikutnya (topik "konten ramai, penjualan sepi"): follow, dengan alasan apa yang didapat kalau follow.

## Reels "konten ramai, penjualan sepi" (29 Okt 2026): set adegan "pillar", CTA follow
- Naskah v6: posts/reels-konten-ramai.json (cerita brand baju ilustrasi, Reframe = bedah content pillar P produk vs S solusi, problem-solution fit lalu product-market fit, contoh S "baju yang tidak bikin perut terlihat buncit", CTA follow + value message). Aldy menolak contoh skincare dan komentar "harganya berapa".
- Build: `python3 animatic/build_reel.py /home/user/vo/vo4_raw.ogg posts/reels-konten-ramai.json out/reel4 pillar auto` (argumen ke-5 = take: auto|akhir|awal). Hasil out/reel4/reel.mp4 (59,9 dtk).
- vo_prep.py sekarang mengenali take ulang (kalimat yang diulang Aldy untuk opsi intonasi) lewat jarak MFCC+DTW, memilih satu take per blok (auto = variasi nada terbesar; selisih <10% -> yang terakhir) dan membuang potongan batal di antara dua take. Laporan di out/reel4/laporan.txt. Tanpa ASR, jadi cek caption bila ragu.

## Suara robot / noise (29 Okt 2026)
- Penyebab: RNNoise pada rekaman yang sudah bersih (voice note HP, lantai bising -64 dB) menggeser spektrum 10 dB dari asli dan membuat HF kasar (suara robot). vo_prep.py sekarang mengukur lantai bising dan MELEWATI RNNoise bila < -55 dB (hanya highpass + kompresi 2:1 + loudnorm). Rekaman berisik tetap pakai RNNoise.
- SFX berbasis desis dilembutkan di semua sfx-*.py: whoosh dua kutub lowpass 1,8 kHz, scratch pita 0,7-2,2 kHz, tick klik bernada 1,7 kHz; efek -28 LUFS (sebelumnya -24).
- (29 Okt) vo_prep: napas/klik pelan tanpa nada dibuang otomatis; min_seg 0,2 dtk; laporan menandai tempo tidak wajar. Penyebab "peceh" detik 50-51 reel4: salah cocok potongan setelah RNNoise dimatikan + klik 0,12 dtk.

## Reels topik 5 "iklan jalan, pesanan tidak naik" (30 Okt 2026)
- Disetujui Aldy (topik 1 dari tiga kandidat: iklan/penawaran samar; kandidat lain belum dipakai: owner jadi penghambat tim, assessment dulu baru strategi). Naskah posts/reels-iklan-penawaran.json (CTA save, contoh brand sepatu ilustrasi (katering ditolak Aldy: tidak umum; boleh fashion muslim)). Menunggu rekaman voice over; build dengan set adegan baru ("iklan").
- (30 Okt) Rumus SMS diganti "kanvas 3 lawan 3" (adaptasi Value Proposition Canvas, Osterwalder): sisi pembeli = mau, butuh, takut; sisi produk = benefit, fitur, pengalaman; pasangan baris: mau->benefit, butuh->fitur, takut->pengalaman. Pemetaan ini adaptasi Claude, bukan bagian baku kanvas aslinya. Contoh: sepatu kerja (tampil rapi / tidak pegal / salah ukuran -> tampil rapi seharian / bantalan empuk / gratis tukar ukuran 7 hari).

## Reels iklan (30 Okt 2026): set adegan "iklan", kanvas 3 lawan 3
- Build: `python3 animatic/build_reel.py /home/user/vo/vo5_raw.mp4 posts/reels-iklan-penawaran.json out/reel5 iklan auto`. Hasil out/reel5/reel.mp4 (57,2 dtk).
- vo_prep.py (30 Okt): NR dilewati bila selisih ucapan-bising > 28 dB; segmentasi dari rekaman asli (ambang = lantai bising + 12 dB) untuk bising ringan; deteksi take ulang dicoba tanpa DAN dengan pembuangan, dipakai yang paling cocok naskah (kata yang memang diulang di naskah, mis. benefit/fitur/pengalaman, sempat salah dikira take ulang dan 12 potongan sah terbuang).

## Carousel "Harga kamu selalu ditawar" final (31 Okt 2026, rev 6)
- Slide 8 satu CTA (SIMPAN, alasan: buka lagi saat tim CS menjawab chat tawar-menawar); caption ditutup satu ajakan simpan; komentar pin tanpa ajakan berkomentar. SEED rev 6 + migrasi hanya mengganti bila nilai lama masih sama.
- Ikon tombol slide CTA kini mengikuti pill (`ctaBtns`): SIMPAN = ikon simpan saja, KIRIM = ikon kirim saja, FOLLOW/lain = tanpa ikon, "SIMPAN & KIRIM" (lama) = dua ikon.
- Cover berfoto: scrim lebih gelap (26% -> .46 -> .6) + text-shadow, supaya teks putih terbaca di atas kaos putih. Foto cover: foto/cover-aldy.jpg (posts/harga-ditawar.json photos "1"). Slide 2 butuh etching (ada di browser Aldy, bukan di repo): render repo menampilkan placeholder; ZIP dari Studio yang lengkap.
- Backup: content-studio.v26.bak.

## Carousel "Owner jadi penghambat" (1 Nov 2026)
- Topik dipilih Aldy dari 3 kandidat (31 Okt). Naskah posts/carousel-owner-penghambat.json (8 slide, CTA SIMPAN, cover berfoto). Solusi satu langkah: tulis 10 keputusan yang sering ditanyakan tim, beri label putuskan sendiri / lapor setelahnya / tanya dulu. Studi kasus = ilustrasi (bukan klien), label di slide 2. Etching slide 2 diunggah Aldy di Studio (prompt di scn).
- Topik ditinggalkan: polemik deklarasi Sumpah Pemuda (31 Okt): Aldy memilih lewati (berita masih bergerak, risiko menggiring opini). Topik cadangan yang sudah diriset: diskon biaya layanan marketplace 50% untuk UMK (Permen UMKM 3/2026, berlaku 25 Okt 2026, daftar SAPA UMKM; kategori dan syarat perlu dicek ulang sebelum dipakai).

## Pustaka tata letak slide (v27, 1 Nov 2026) - Tugas 5 mulai
- Slide punya kolom `lay` (a asli | b | c). Studio menampilkan "Gaya tampilan" di editor tipe yang punya varian. Palet, font, aturan foto tidak berubah; hanya bentuk. Diimpor/diekspor otomatis (kolom string).
- Varian: vertical a bubble chat / b daftar bernomor besar / c catatan tempel; akar a diagram batang / b tiga kartu bersisian / c tangga naik; action a checklist / b langkah bernomor besar (outline). Belum: markup, statement, cta, cover (rencana berikutnya).
- Pilot: posts/carousel-owner-penghambat.json (slide 3 c, 5 b, 7 b). Tes: tests/t26_layouts.js (unduhan = pratinjau, beda_rata < 5). Gotcha: di kartu miring jangan pakai <b><br><span> (export menggeser teks ~10 px); pakai blok div dengan tinggi baris tetap.
- Backup: content-studio.v27.bak. Belum dipublikasikan ulang ke Artifact.
- (1 Nov) Cover owner penghambat memakai foto foto/cover-owner-tim.jpg (825x1024, suasana kantor, tangan bersilang), phz 130 / phy 70 supaya wajah di atas blok teks. Sumber foto beresolusi rendah: minta versi >= 1600 px untuk cover berikutnya.

## SUARA ALDY v2 (1 Nov 2026) - WAJIB, menggantikan saran "nggak" dan register konsultan
Dasar: 3 sampel tulisan Aldy (voice/sampel-aldy.md). Tingkat disetujui Aldy: "percakapan rapi".
- Temuan: tulisan personal Aldy hangat dan natural (gak, aja, kan, kalo, kaya, bikin, dapatin; "Kamu boleh X, tapi Y"). Tulisan bisnisnya beralih ke register analitik yang kaku (kalimat rata-rata 30 kata, maks 51; "dimana" sebagai penghubung, "yaitu", "namun" 5x, "pola pikir", "ideologi", "kepastian nilai yang pasti"). Copy awal yang dibuat Claude meniru register analitik itu. Kalimat pendek BUKAN jaminan natural (carousel lama rata-rata 7-8 kata tapi tetap kaku): kaku datang dari kosakata, label abstrak, kalimat definisi, dan ritme seragam.
- Kosakata Aldy (pakai ejaan Aldy): gak, aja, kan, kalo, kaya, bikin, nunggu, nanya, bales, putusin, abis itu, biang kerok, meja meeting. Hindari "nggak", "gue", gaul cepat basi, singkatan chat berlebihan.
- Gerak khas yang dipertahankan: (1) prinsip pendek berdiri sendiri/refrain ("Manusia itu tidak pernah statis."); (2) "Kamu boleh X, tapi Y"; (3) pengamatan lapangan sebagai pembuka ("Di setiap bisnis yang saya dampingi, ada satu hal yang selalu sama di meja meeting"); (4) dua sisi dipertentangkan dengan adil, tanpa menyalahkan; (5) analogi atau cerita (film AIR: Nike, Adidas, Converse, Michael Jordan; film = dramatisasi, jangan disajikan sebagai sejarah persis); (6) memberi nama konsep sendiri ("coordination system": koordinasi dan delegasi membangun trust dan tanggung jawab, sisanya pengalaman dan intuisi); (7) paralelisme dengan contoh konkret ("Punya rumah harus dilepas / Punya mobil dijual").
- Aturan tulis: satu ide per kalimat, 8-14 kata, sesekali 3 kata; selang-seling pendek dan agak panjang; ganti "namun" -> "tapi", "dimana/yaitu" -> titik atau dua titik, "tidak" -> "gak" (di copy bernada ngobrol), kata kerja perintah formal ("Selesaikan", "Beri") -> "Lengkapin", "Kasih"; label abstrak -> kejadian yang bisa dibayangkan; satu kalimat tajam per carousel; tiap slide dibaca keras tanpa tersangkut.
- Pilar personal (pelajaran hidup, rezeki, iman) dipisah dari konten bisnis; tidak dicampur di carousel bisnis kecuali Aldy minta. Ucapan keagamaan hanya di pilar personal.
- Salah ketik di sampel TIDAK ditiru. Pola finance vs marketing = studi kasus sah sebagai pola dari pengalaman mendampingi (tanpa identitas klien).
- Pembaruan copy 1 Nov: posts/carousel-owner-penghambat.json ditulis ulang dengan aturan ini. Belum: posts/harga-ditawar.json, pemeriksa kaku di Studio, prompt Brief.
- SAPAAN KONTEN (Aldy setuju, 1 Nov 2026): semua konten sosmed (carousel, reels, caption, story) memakai "kamu" untuk audiens dan "saya" untuk Aldy. "Anda" hanya untuk dokumen formal (proposal klien, email resmi, ringkasan assessment). Jangan campur dengan "lu/gue". Hipotesis belum teruji: owner senior mungkin lebih nyaman "Anda"; kalau ada data simpan/balasan yang menunjukkan itu, tinjau lagi. Sapaan Claude ke Aldy di obrolan tetap "Anda" (terpisah dari bahasa konten).
- (1 Nov, lanjutan) Cover "Nunggu Kamu" kini memakai foto/cover-owner-meja.jpg (825x1024, duduk di meja kerja), phz 135 / phx 53 / phy 89 (wajah di atas blok teks). Scrim cover berfoto ditambah gradasi atas (.42 -> 0 di 20%) supaya tanda tangan terbaca di latar terang. Foto yang tidak dipakai lagi: cover-owner-tim.jpg.

## ATURAN CAPTION OTOMATIS (Aldy, 1 Nov 2026) - WAJIB
- Setiap konten yang dibuat Claude (carousel, reels, story) otomatis disertai caption ringkas: SATU kalimat berstruktur HVC (Hook, Value, CTA) + hashtag. Tulis di pesan penyerahan DAN simpan di field `caption` posts/*.json.
- Kalimat: suara Aldy v2 ("kamu", "gak", "bikin"), satu CTA saja (save/share/follow, dengan alasan, tanpa komentar/keyword/DM), angka contoh diberi label "(contoh hitungan)". Hashtag 6-8: 6 dasar (#brandstrategy #personalbranding #strategibisnis #pemilikbisnis #umkmindonesia #thebrandfixer) + 1-2 sesuai topik.
- Caption panjang lama diarsipkan di posts/caption-panjang.md. Komentar pin dan story poll tetap dibuat seperti biasa.

## Keputusan reels finance vs marketing (1 Nov 2026)
- Aldy memutuskan memakai logo dan foto asli Jordan/Nike (menggantikan saran Claude memakai ilustrasi). Aset disediakan Aldy (posts/aset-nike-jordan.md). Risiko dicatat; keterangan "tidak berafiliasi" wajib di layar dan komentar pin.
- Reframe diperjelas (tiga kesepakatan: cara ngukur, batas rugi, tanggal ngecek + contoh angka ilustrasi); durasi boleh lebih dari 60 dtk (target sampai ±75 dtk) untuk reels bercerita atas izin Aldy. CTA: share ke tim internal untuk menentukan kesepakatan.
- (1 Nov) Aset Nike/Jordan dari Aldy diterima: foto/aset/ (jordan-collage 474x331 resolusi rendah, jordan-kiri/kanan, nike-swoosh, adidas, converse, logo sudah transparan). Sengaja TIDAK di-commit (berhak cipta; repo bisa publik): ada di .gitignore. Voice over finance vs marketing belum diterima (audio terakhir 30 Okt). Foto Jordan dipakai kecil (kartu foto ber-selotip, maks ±360 px lebar, 3-4 dtk) karena resolusi rendah.

## Perkenalan standar reels (Aldy, 8 Nov 2026) - WAJIB di reels berikutnya
- Setelah hook, sebelum Relate, selalu ada perkenalan: "Hai, kenalin, saya Aldy Syahreza. Belasan tahun saya membangun dan mendampingi lebih dari seratus brand, lintas industri, dari branding sampai strategi marketing." (versi ringkas ±6 dtk, dipakai Aldy: "Sebelumnya, kenalin. Saya Aldy Syahreza. Belasan tahun mendampingi lebih dari seratus brand lintas industri, dari branding sampai strategi marketing."). Klaim "belasan tahun / 100+ brand / 360" adalah klaim Aldy; jangan menyebut nama klien.
- Visual: foto profil pertama dari Profile - Aldy Syahreza.pdf (foto/profil-seminar.jpg, Aldy di seminar memegang mikrofon) di kartu miring + nama + tiga kartu angka (scratch/intro_scene.py: INTRO_HTML/INTRO_JS). Ini PENGECUALIAN aturan "foto wajah hanya di cover carousel": foto Aldy boleh di adegan perkenalan reels.
- Kalimat Relate yang menjawab hook diawali penyambung yang mulus ("Nah, kebiasaan yang saya maksud begini.", bukan "Balik ke ...") supaya alur tidak terputus. Reels #3 dan #4 yang sudah dirender belum memakai perkenalan; berlaku untuk reels baru.

- Data profil dari PDF Aldy (8 Nov 2026), klaim Aldy sendiri: >10 tahun, >100 brand lintas industri; 50 ribu order dalam satu campaign; ROAS >20x; penghargaan rekor dunia Indonesia untuk branding; Creative Director hingga Business Consultant; membangun booth event terbesar; berkolaborasi dengan brand ternama; pengisi workshop dan sharing session; mengelola program kemitraan brand. Tagline: 'Branding & Digital Marketing Consultant - Helping Your Businesses Grow Up, Scale Up, and Brand Up'. Pakai satu klaim per konten, jangan menyebut nama klien.

## Cek isi rekaman dengan ASR (11 Nov 2026) - WAJIB sebelum merender
- Dulu tanpa ASR: pencocokan potongan ke naskah hanya dari suku kata/intonasi, sehingga BAGIAN YANG TIDAK DIREKAM bisa dipaksakan cocok ke audio lain (kasus reels Reddit: Insight tidak direkam, video salah sinkron). Sekarang ada ASR lokal: Whisper small lewat sherpa-onnx (`pip install sherpa-onnx`; model dari GitHub releases `k2-fsa/sherpa-onnx` asr-models/sherpa-onnx-whisper-small.tar.bz2, 640 MB; HuggingFace diblokir, GitHub dan PyPI terbuka).
- `python3 tools/asr_pieces.py rekaman.mp4 rekaman16k.wav hasil.txt` menulis transkrip per potongan bicara (bahasa 'id'). Bandingkan dengan naskah: kalimat hilang, take ulang, salah urut. Akurasi kata sedang (nama dan istilah sering salah), cukup untuk urutan kalimat.
- Setelah menemukan pengulangan: potong lewat VO_CUTS="a-b,c-d" (detik rekaman asli) dengan VO_NORETAKE=1. Naskah JSON harus sama dengan yang benar-benar direkam (hapus babak yang tidak direkam).

## Voice over suara klon (Aldy, 11 Nov 2026) - folder voiceover/
- Aldy menyerahkan klon suaranya (VoiceStudio lokal di komputernya, model OmniVoice, API 127.0.0.1:3900) untuk dipakai sebagai voice over. File: voiceover/generate.ps1 (satu teks -> satu WAV), voiceover/generate_batch.ps1 (BARU: satu kalimat per file, durasi pasti), README.md, ref_text.txt, ejaan.json (kamus pelafalan: AI -> "A I", Reddit -> "Redit", angka dieja). ref.wav (15 dtk suara Aldy) hanya ada di komputer Aldy dan salinan lokal sesi; TIDAK di-commit (sampel suara; repo bisa publik). Pengaturan dikunci: class_temperature 0.3, seed 7, speed 1.0, language id; jangan diubah tanpa izin. Jangan memasukkan API key.
- Sesi cloud TIDAK bisa menjalankan VoiceStudio (komputer Aldy tidak ditawarkan ke sesi cloud). Alur: (1) Claude menulis naskah dan `python3 tools/export_naskah.py posts/<reels>.json naskah/<nama>` (menghasilkan <nama>.kalimat.txt yang ejaannya sudah dinormalkan + <nama>.kalimat.json); (2) Aldy menjalankan di komputernya `.\voiceover\generate_batch.ps1 -LinesFile naskah\<nama>.kalimat.txt -OutDir hasil\<nama>` (uji dulu `-Limit 3`), lalu mengirim folder hasil (ZIP) beserta <nama>.kalimat.json sebagai kalimat.json di dalamnya; (3) `python3 animatic/build_reel.py <folder> posts/<reels>.json out/<dir> <set>` (jika argumen pertama folder, build_reel memakai tools/assemble_vo.py: rakit kalimat + jeda baku + timing kata, tanpa menebak batas kalimat).
- Peringatan (dari README Aldy): bobot model CC-BY-NC (non-komersial). Konten pemasaran jasa Aldy dan konten klien kemungkinan komersial: cek lisensi sebelum dipakai. Platform (Instagram/Meta) bisa mewajibkan label untuk audio buatan AI yang realistis: cek aturan terbaru dan pertimbangkan keterbukaan ke audiens. Klon kurang ekspresif dari rekaman asli (rentang intonasi ±12,7 vs 15-18 semitone, tempo ±2,8 kata/dtk): dengarkan hasilnya sebelum merender.
- Rekaman asli Aldy tetap sah dipakai (alur vo_prep + ASR); suara klon adalah pilihan.

## Hasil uji suara klon (Aldy, 11 Nov 2026)
- Speed 1.1 + ejaan v1 ("Redit", "anjlok") disetujui; tapi intonasi klon dinilai Aldy kaku/robotik, tidak menyambung, baik per kalimat maupun per paragraf.
- ref_A / ref_B (potongan dari rekaman asli) tidak lebih baik dari ref.wav (ASR: "anjlok"->"unlock"). Per paragraf memperbaiki nama sedikit, bukan intonasi.
- Keputusan: untuk konten yang butuh natural, pakai rekaman asli Aldy. Klon hanya untuk draf/panduan, bukan voice over final.

## Sistem produksi reels v1 (disetujui Aldy 13 Nov 2026) - strategi/reels-system-v1.md, strategi/creative-log.md
- KELAS DURASI (pagar, tempo terukur 2,2 kata/dtk): Pendek 30-45 dtk maks 95 kata; Standar 45-60 dtk maks 130 kata (bawaan); Cerita 60-90 dtk maks 195 kata (alasan ditulis di brief); di atas 90 dtk DITOLAK sampai ada data retensi. Perkenalan dihitung dalam anggaran. Revisi "biar jelas" tidak boleh menambah kata tanpa membuang kata lain.
- UJI PERKENALAN (dua reels berikutnya): versi 2 = ucapan pendek "Saya Aldy Syahreza, belasan tahun mendampingi brand." + kartu nama/100+ brand 3 dtk di atas adegan (dipakai di reels AI chat); versi 1 = perkenalan penuh (reels sesudahnya). Bandingkan retensi detik 15 dari Insights. Topiknya beda, jadi hasilnya indikasi, bukan bukti.
- Sebelum konsep baru: baca creative-log.md (jangan ulang sudut cerita 2 reels terakhir, bentuk penutup reels sebelumnya, representasi dominan 3x berturut). Reframe = SATU tindakan. Hindari penutup "tiga hal" berturut-turut dan tema AI berturut-turut.
- Tipe A tetap kode; video AI hanya sisipan 2-3 dtk tanpa teks dan tanpa wajah. Tipe B (talking head) belum punya mesin: menunggu rekaman uji Aldy (vertikal, sejajar mata, mikrofon sama).
- Gerbang mutu 14 metrik (lulus >= 85/100, metrik inti >= 8); skor = heuristik, bukan prediksi. Aturan CTA lama tetap (tanpa keyword/DM/komentar) walau instruksi master menyebut opsi keyword.
- Menunggu dari Aldy: tangkapan layar Insights tiap reels (retensi 3 dtk, rata-rata tonton, simpan, kirim, non-pengikut) untuk kolom performa creative-log.
- Reels AI chat (posts/reels-ai-chat.json, 115 kata): klaim "AI belajar dari arsip chat" DIBUANG (tidak ada sumber); diganti "jawab dari informasi yang kamu isi" (SWA, Warta Ekonomi). Dokumentasi resmi Meta belum dibaca.
- (13 Nov, Aldy) Topik reels AI chat DIBATALKAN (kurang menarik menurut Aldy). Arah topik: growth mindset & strategi, tidak teknis, diturunkan ke satu keputusan owner + teori dikenal. Dipilih: kandidat C "Kerja paling keras = masalahnya" (Gerber, The E-Myth) -> posts/reels-kerja-pada-bisnis.json (127 kata). Kandidat cadangan: A Porter "strategi = yang dicoret", B Dweck "kampanye gagal != brand jelek".
- (13 Nov, Aldy) Suara: HANYA VoiceStudio lokal (tidak boleh unggah suara ke Higgsfield/layanan lain). Caption TANPA keterbukaan "dibantu AI" (risiko label Meta & kepercayaan sudah disampaikan). Uji perbaikan intonasi lewat voiceover/generate_uji.ps1 (tanpa pasca-proses; variasi temp/seed); pengaturan terkunci baru diganti bila Aldy memilih hasil uji.
- (13 Nov, Aldy) Uji VoiceStudio tidak dijalankan: Aldy memilih REKAMAN ASLI untuk reels kerja pada bisnis. Suara klon tidak dipakai sampai Aldy memintanya lagi.
