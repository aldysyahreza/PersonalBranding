# Sistem Produksi Reels The Brand Fixer v1

Disusun 13 Nov 2026. Status: rancangan untuk disetujui Aldy. Belum ada yang diubah di mesin produksi.

Cara membaca label:
- **[Ditemukan]** = ada di lampiran, repo, atau catatan proyek, dan saya baca sendiri.
- **[Tafsir]** = kesimpulan saya dari data itu.
- **[Usul]** = rekomendasi baru, belum diuji.

---

## 0. Ringkasan untuk keputusan

1. **Sistem Anda sudah kuat di naskah dan kontrol mutu, lemah di tiga hal:** tidak ada data performa yang kembali ke naskah, durasi melebar tanpa keputusan, dan semua reels memakai satu bahasa visual.
2. **Dua lampiran dan daftar GitHub lebih berguna sebagai sumber aturan, bukan sebagai alat yang dipasang.** Hampir semuanya butuh Mac, kunci API berbayar, atau gaya visual yang bertentangan dengan brand Anda.
3. **Tipe A (animasi + voice over) tetap berbasis kode.** Video buatan AI hanya sebagai sisipan pendek. Alasannya di bagian 4.
4. **Tipe B (talking head) belum ada mesinnya.** Bisa dibangun di atas mesin yang sekarang, tanpa alat baru. Butuh satu rekaman uji dari Anda.
5. **Satu hal yang saya tantang:** perkenalan 6–10 detik tepat setelah hook. Itu titik paling rawan penonton pergi. Saya usul diuji, bukan dihapus.

---

## 1. Personal Branding Creative Diagnostic Report

### 1.1 Bahan yang saya analisis

| Bahan | Status |
|---|---|
| `CLAUDE.md` proyek, 10 naskah reels, bank topik, 9 set adegan, hasil render | Dibaca dan diukur |
| Lampiran 1: Claude-Video-Editing-Studio (ZIP) | Semua dokumen `.md` dan 3 skill dibaca. Kode alat tidak dijalankan |
| Lampiran 2: claude-remotion-skill (ZIP) | README, SKILL, lisensi dibaca. Contoh tidak dirender |
| Daftar awesome-claude-video-skills | README dibaca (489 repo terdaftar). 18 repo dibuka README dan lisensinya |
| Data Instagram (retensi, simpan, kirim) | **Tidak tersedia.** Tidak ada satu pun angka performa di proyek |
| Rekaman talking head Anda | **Tidak tersedia** |

### 1.2 Audit identitas brand

**[Ditemukan]**
- Posisi: The Brand Fixer, "director yang mendiagnosis". Metode: assessment dulu, baru strategi.
- Audiens: pemilik bisnis omzet di atas Rp100 juta per bulan.
- Suara: "Suara Aldy v2" (kamu/saya, gak/aja/kan/kalo/bikin), tingkat "percakapan rapi".
- Visual: palet Ink, Paper, Terakota, Amber, Warm Gray. Font Archivo, Fraunces, Inter, Caveat, JetBrains Mono. Gaya animatic "buku catatan diagnosis" dikunci 28 Okt 2026.

**[Tafsir]**
- Posisi "diagnosis" terasa di carousel, kurang terasa di reels terbaru. Reels Reddit berisi tiga tips, bukan diagnosis. Kalau terus begitu, Anda bergeser ke "pemberi tips AI", kategori yang ramai.
- Wajah dan suara Anda adalah aset kepercayaan terbesar, tetapi baru muncul 6–10 detik per reels (kartu perkenalan).

### 1.3 Audit strategi konten

**[Ditemukan]** Durasi 10 reels yang dirender:

| Reels | Durasi | Aturan saat itu |
|---|---|---|
| Harga ditawar | 38 dtk | 35–45 |
| Omzet marketplace | 50 dtk | 35–45 |
| Persona brand | 51 dtk | maks 45 |
| Konten ramai | 59 dtk | maks 60 |
| Iklan penawaran | 57 dtk | maks 60 |
| Finance vs marketing | 85 dtk | maks ±75 (izin khusus) |
| Sales vs operasional | 75 dtk | - |
| Marketing vs owner | 99 dtk | - |
| Reddit (tanpa Insight) | 108 dtk | - |
| Reddit (lengkap) | 135 dtk | - |

**[Tafsir]** Durasi naik 3,5 kali lipat dalam dua minggu, tanpa satu pun data yang membenarkannya. Setiap revisi menambah penjelasan ("biar jelas"), tidak ada yang mengurangi. Untuk konten TOFU ke penonton yang belum kenal Anda, ini risiko terbesar. Saya ikut menyebabkannya karena tidak menahan.

**[Ditemukan]** Semua CTA adalah simpan atau kirim. Belum ada jembatan ke penawaran yang terukur (bank topik menyebut "Cek Brand 15 Menit", "Kit Alasan Dipilih", tapi belum dipakai di video).

### 1.4 Audit storytelling

**[Ditemukan]** Sudut hook yang dipakai: kontradiksi 3 kali, tanya 3 kali, angka 2 kali, cermin 1 kali, kutipan 1 kali. Eksekusi: banding 4 kali, layar 2 kali, angka 2 kali, coretan 1, chat 1.

**[Tafsir]**
- Sudut hook cukup bervariasi. Yang berulang adalah **bentuk isi**: empat dari lima reels terakhir berakhir dengan "tiga hal / tiga kesepakatan / tiga langkah". Penonton tetap akan mengenali pola itu.
- Belum pernah dipakai: pengalaman pribadi, kesalahan umum, mitos lawan fakta, sebelum-sesudah.
- Aturan "satu langkah solusi saja" (29 Okt) tidak dipegang di sebagian besar reels sesudahnya.

### 1.5 Audit identitas visual

**[Ditemukan]** Sembilan set adegan memakai kertas grid krem, kartu, coretan pena, caption pil yang sama.

**[Tafsir]** Konsistensi tinggi, variasi rendah. Yang berubah antar-reels hanya isi kartu. Belum ada adegan dengan lingkungan, karakter yang berperan (baru ada figur orang di reels owner dan Reddit), atau metafora fisik.

### 1.6 Audit alur produksi

**[Ditemukan, kuat]** Satu perintah dari rekaman ke video. Pengenal suara memeriksa isi rekaman. Pemeriksa tata letak. Musik dan efek dari kode. Catatan keputusan tersimpan.

**[Ditemukan, lemah]**
- Tiap reels butuh generator adegan baru yang ditulis tangan. Tidak ada pustaka adegan yang bisa dipakai ulang.
- Efek suara reels Reddit 22 adegan memakai penempatan versi 16 adegan (saya laporkan saat serah terima).
- Suara klon gagal uji natural (11 Nov). Voice over final = rekaman asli Anda.

### 1.7 KEEP / IMPROVE / EXPAND / AVOID

| | Isi |
|---|---|
| **KEEP** | HRIRC sebagai alat periksa. Suara Aldy v2. Satu CTA dengan alasan. Larangan mengarang kasus. Sumber fakta di pinned comment. Gaya buku catatan sebagai DNA. Rekaman asli Anda. Cek pengenal suara sebelum render. |
| **IMPROVE** | Durasi (kembali ke anggaran kata). Aturan satu langkah. Penempatan perkenalan. Efek suara per adegan. Pustaka adegan pakai ulang. |
| **EXPAND** | Tipe B talking head. Sudut cerita yang belum dipakai. Metafora fisik dan adegan berkarakter. Jembatan ke penawaran. Catatan variasi kreatif. |
| **AVOID** | Menambah penjelasan tiap revisi. Pola "tiga hal" berturut-turut. Tema AI berturut-turut. Suara klon untuk final. Video AI yang memuat teks atau wajah Anda. Gaya gelap-krom dari lampiran 1. |

### 1.8 Celah kritis (urut dampak)

1. **Tidak ada umpan balik performa.** Skor editorial saya adalah tebakan terdidik. Tanpa retensi 3 detik, rata-rata tonton, simpan, dan kirim per reels, sistem ini tidak bisa belajar.
2. **Durasi tanpa pagar.** Lihat 1.3.
3. **Satu bahasa visual.** Lihat 1.5.
4. **Tipe B belum ada.** Kepercayaan paling cepat tumbuh dari wajah, dan itu belum dipakai.
5. **Posisi "diagnosis" memudar** di reels berbasis berita.

### 1.9 Konflik pedoman dan penyelesaiannya

| Konflik | Usul penyelesaian | Alasan |
|---|---|---|
| Instruksi baru membuka "comment keyword strategy". Aturan Anda: tanpa keyword, tanpa DM, tanpa ajakan komentar. | Aturan lama tetap. Bagian keyword dikosongkan. | Aturan itu keputusan Anda yang eksplisit dan berulang. Ubah hanya kalau Anda menyatakannya. |
| Instruksi baru: variasi dinamis. Catatan proyek: gaya animatic "terkunci". | Tiga lapis identitas di bagian 5. Yang terkunci adalah DNA, bukan komposisi adegan. | Mengunci semuanya menghasilkan kejenuhan. Membebaskan semuanya menghasilkan identitas kabur. |
| Instruksi baru mengandaikan Tipe A dibuat dengan AI video (prompt, negative prompt, identity lock). Mesin sekarang: kode. | Kode sebagai utama, AI sebagai sisipan. Kolom "prompt" di kartu adegan diisi hanya untuk sisipan. | Bagian 4.1. |
| Target 40–55 dtk. Praktik: 75–135 dtk. | Dua kelas durasi di bagian 6.3. | Perlu keputusan, bukan pelebaran diam-diam. |
| Lampiran 1: "kamera tidak pernah diam", adegan 1,5 dtk. Lampiran 1 sendiri (bab lain): untuk video penjelasan, kamera diam adalah bawaan yang benar. | Pakai aturan video penjelasan. | Reels Anda menjelaskan mekanisme, bukan iklan 30 detik. |

---

## 2. Riset skill dan framework GitHub

### 2.1 Batas verifikasi (jujur dulu)

- **Yang saya lakukan:** membaca README 20 repo dan baris pertama berkas lisensinya; membaca isi penuh dua lampiran; membaca satu berkas skill (`short-form-video`) dari iart-ai.
- **Yang tidak saya lakukan:** menjalankan satu pun. Memeriksa tanggal commit terakhir, jumlah isu, atau jumlah bintang secara langsung (API GitHub diblokir dari sesi ini). Angka bintang di bawah berasal dari daftar awesome itu, bukan dari saya.
- **Temuan penting dari daftar itu sendiri [Ditemukan]:** pengelolanya menguji 16 skill dengan tugas yang sama. Semua lulus, dan **Claude Code tanpa skill juga lulus** dalam 4,4 menit. Kesimpulan mereka: skill layak dipasang kalau membawa gaya, alur kerja, atau footage untuk diedit. Ini mendukung keputusan "ambil aturannya, bukan alatnya".
- Komputer Anda Windows. Banyak repo menulis syarat macOS.

### 2.2 Dua lampiran Anda

**Claude-Video-Editing-Studio** (captainp369, MIT)
- Fungsi: ruang kerja edit talking head lewat percakapan. Bergantung pada dua skill luar (video-use, hyperframes) dan kunci API ElevenLabs untuk transkripsi.
- Yang layak diadaptasi:
  - **Dynamics Ledger**: tabel per ketukan (waktu, ucapan, kamera, grafis, zona, masuk, keluar) yang disetujui sebelum membangun.
  - **Sembilan Variety Laws**: dua grafis berurutan tidak boleh di zona yang sama atau masuk dengan cara yang sama; satu jenis gerak maksimal tiga kali; gerak istimewa maksimal 1–2 kali per video; grafis mengikuti ucapan, tidak mengarang isi.
  - **Jenis video menentukan fungsi kamera**: di hook kamera memberi energi; di penjelasan kamera hanya menunjuk sesuatu di layar, dan diam adalah bawaan yang benar.
  - **Aturan potong**: hanya di batas kata, fade audio 30 ms di tiap sambungan, rencana potong disetujui dulu.
  - **Tangga sumber media**: buat sendiri → lisensi terbuka → media milik subjek dengan izin → selain itu tidak dipakai.
  - **Efek suara**: variasikan dan kurangi; tidak semua gerak diberi bunyi.
- Yang dihindari: paket gaya "Premium Dark" (hitam, krom, kaca) bertentangan dengan palet Anda. "Adegan 1,5 detik" terlalu cepat untuk owner yang sedang mencerna argumen.
- Keputusan: **referensi konsep.** Tidak dipasang.

**claude-remotion-skill** (haidrrrry, MIT)
- Fungsi: 10 aturan gerak untuk Remotion ditambah putaran wajib render → periksa frame → perbaiki.
- Yang layak diadaptasi: masuk dengan 2–3 properti sekaligus; berurutan, tidak serempak; keluar lebih cepat dari masuk; elemen yang diam lebih dari 2 detik diberi gerak halus; satu berkas tema; emoji dilarang sebagai ikon.
- Yang dihindari: pindah ke Remotion. Mesin Anda sudah HTML dan Playwright dengan putaran periksa yang sama. Menulis ulang sembilan set adegan tidak menambah nilai. Lisensi Remotion untuk perusahaan juga perlu dicek dulu (saya tidak memeriksanya).
- Keputusan: **adaptasi aturan geraknya** ke daftar periksa.

### 2.3 Repo dari daftar yang dibuka

| Repo | Fungsi (dari README) | Lisensi | Relevan | Risiko / batas | Keputusan |
|---|---|---|---|---|---|
| [iart-ai/tiktok-video-skills](https://github.com/iart-ai/tiktok-video-skills) | Tata bahasa hook → retensi → loop, caption per kata, lower third | MIT | A dan B | Angka retensi di dalamnya (87% memutuskan dalam 3 dtk, ambang 70%) tanpa sumber. Repo berfungsi sebagai corong ke produk berbayar | Adaptasi kerangka "buka pertanyaan di 3 dtk, tutup di akhir". Angka jangan dikutip |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | Kumpulan skill pemasaran: copywriting, copy-editing, psikologi, konten sosial | MIT | Naskah | Berbahasa Inggris, condong SaaS. Banyak tautan afiliasi di README | Referensi untuk skill periksa naskah. Suara Aldy v2 tetap di atasnya |
| [jtydhr88/screenwriting-skills](https://github.com/jtydhr88/screenwriting-skills) | 26 skill penulisan skenario dari 47 buku | MIT | Storytelling | Isi skill berbahasa Mandarin. Untuk film panjang, bukan 60 detik | Referensi konsep saja |
| [sharon-laicc/viral-video-decomposer](https://github.com/sharon-laicc/viral-video-decomposer) | Membedah video pendek jadi per-shot, mekanisme, dan cetak biru | MIT | Riset referensi | 12 bintang menurut daftar. Belum teruji | Adaptasi format bedah untuk mempelajari reels referensi. Kita sudah melakukan ini manual (@decoyreport) |
| [beatra-ai/viral-video-remake-skill](https://github.com/beatra-ai/viral-video-remake-skill) | Bedah lalu bangun ulang struktur video | MIT-0 | - | Render butuh akun berbayar Beatra | Lewati |
| [artemnovitckii/claude-animation-skills](https://github.com/artemnovitckii/claude-animation-skills) | Enam gaya animasi tanpa footage: kartun 3D, figur garis, garis minimal, rute peta, tampilan urai, grafik | MIT | A | macOS/Linux. Gayanya milik pembuatnya | Adaptasi dua gagasan: **tampilan urai** (barang dibongkar per lapis) dan **grafik satu angka**, digambar ulang dalam gaya Anda |
| [haiderfarooq3/paper-reel](https://github.com/haiderfarooq3/paper-reel) | Reels kertas potong; "suara adalah jam", properti muncul tepat di kata | MIT | A | macOS. Suara TTS | Prinsipnya sudah Anda miliki (jangkar kata). Tidak perlu |
| [0xS4N4TG/papercut-explainer](https://github.com/0xS4N4TG/papercut-explainer) | Sembilan skill plus pustaka Remotion gaya kertas potong | MIT | A | Remotion | Referensi cara menyusun pustaka adegan |
| [isaachang/motion-video-workflow](https://github.com/isaachang/motion-video-workflow) | Satu rekaman suara jadi video gerak per frame | MIT | A | README berbahasa Mandarin; hanya saya baca sekilas | Belum dinilai |
| [browser-use/video-use](https://github.com/browser-use/video-use) | Potong filler, grade warna, subtitle, evaluasi diri | MIT | B | Butuh kunci API ElevenLabs | Referensi aturan potong. Pengenal suara lokal kita menggantikan API-nya |
| [kurbaitaev/ghost-editor](https://github.com/kurbaitaev/ghost-editor) | Rekaman mentah jadi reels, banyak gaya bernama | MIT | B | Render di Mac | Referensi daftar gaya: "papan tulis di atas, pembicara di bawah", "kartu kutipan di samping wajah, tidak pernah menutupinya" |
| [artemnovitckii/claude-editing-skills](https://github.com/artemnovitckii/claude-editing-skills) | 11 tata letak talking head: grafis di belakang orang, layar belah, kartu gambar | MIT | B | Butuh pemotongan latar orang | Adaptasi tata letak "layar belah" dan "tiga kartu gambar" |
| [adriiita/vertical-video-editing-skill](https://github.com/adriiita/vertical-video-editing-skill) | Standar edit 9:16: A-roll sebagai tulang punggung, B-roll menutup dan menekan | MIT | B | Di atas HyperFrames. Menyebut potongan sampai 0,2 dtk dan "jangan buka dengan talking head diam" | Adaptasi prinsip tulang punggung. Aturan "jangan buka dengan wajah" saya tolak untuk Anda (wajah adalah bukti) |
| [louisedesadeleer/cut-video](https://github.com/louisedesadeleer/cut-video) | Buang jeda dan filler, pertahankan tawa dan jeda sengaja | MIT | B | Apple Silicon, bahasa Inggris | Adaptasi gagasan "profil nada" (agresif, seimbang, sentimental) untuk kerapatan potong |
| [Vibha-Ramprakash/claude-video-effects](https://github.com/Vibha-Ramprakash/claude-video-effects) | 51 efek untuk klip talking head | MIT | B | Efek demi efek; rawan dekoratif | Lewati |
| [erduo1998-cell/erduo-broll-loop-engineering](https://github.com/erduo1998-cell/erduo-broll-loop-engineering) | B-roll dari SRT, 152 kartu shot | MIT | B | **README menyatakan proyek dihentikan** | Lewati |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | Perender HTML ke MP4 | Apache-2.0 | A | Dalam uji daftar itu paling lambat (23,5 menit untuk 15 detik) | Tidak perlu. Fungsinya sama dengan perender Anda |
| [remotion-dev/skills](https://github.com/remotion-dev/skills) | Skill resmi Remotion | Berkas lisensi tidak ditemukan | A | Lihat catatan Remotion di 2.2 | Tidak perlu |

### 2.4 Creative Skill Stack Recommendation

Skor 1–5. Kerumitan teknis: 5 = paling mudah.

| # | Modul | Sumber gagasan | Penting | Dampak | Mudah | Cocok brand | Teknis | Total |
|---|---|---|---|---|---|---|---|---|
| 1 | Catatan performa + catatan variasi | Baru | 5 | 5 | 4 | 5 | 5 | 24 |
| 2 | Anggaran kata dan durasi per kelas | Aturan Anda sendiri | 5 | 5 | 5 | 5 | 5 | 25 |
| 3 | Kartu adegan "harus layak ada" | Master instruction + Variety Laws | 5 | 4 | 4 | 5 | 4 | 22 |
| 4 | Dynamics Ledger + Variety Laws | Lampiran 1 | 4 | 4 | 4 | 4 | 4 | 20 |
| 5 | Gerbang mutu 14 metrik | Master instruction | 4 | 4 | 5 | 5 | 5 | 23 |
| 6 | Mesin Tipe B (potong + lapisan grafis) | Lampiran 1, video-use, editing-skills | 5 | 5 | 2 | 5 | 2 | 19 |
| 7 | Pustaka adegan pakai ulang | papercut-explainer | 3 | 4 | 3 | 5 | 3 | 18 |
| 8 | Aturan gerak 10 butir | Lampiran 2 | 3 | 3 | 5 | 4 | 5 | 20 |
| 9 | Sisipan video AI | Higgsfield / Krea (sudah terhubung) | 2 | 3 | 3 | 3 | 3 | 14 |

Urutan pengerjaan: 2 → 1 → 5 → 3 → 4 → 6 → 8 → 7 → 9.

### 2.5 Arsitektur skill modular di Claude

```
reels-brief          tujuan, audiens, satu pesan, sudut, CTA      -> brief.md
reels-variasi        baca creative-log, pilih kombinasi yang belum jenuh
reels-naskah         HRIRC + Suara Aldy v2 + anggaran kata        -> posts/<x>.json
reels-peta-adegan    narasi -> kartu adegan + ledger              -> adegan.md
reels-bangun-A       animatic dari kode (mesin sekarang)
reels-bangun-B       potong talking head + lapisan grafis (baru)
reels-gerbang        14 metrik + cek fakta + pengenal suara + tata letak
reels-serah          video + caption + pinned + story + baris baru di creative-log
```

Setiap modul satu berkas aturan pendek. `CLAUDE.md` sekarang sudah 200 baris lebih dan terus tumbuh; memecahnya mengurangi aturan yang terlewat.

---

## 3. Kerangka identitas kreatif

| Lapis | Isi | Aturan ubah |
|---|---|---|
| **Tidak bisa ditawar** | Palet lima warna. Lima font. Caption pil ink. Header "THE BRAND FIXER // babak". Coretan pena merah. Suara asli Anda. Suara Aldy v2. Satu CTA beralasan. Tanpa kasus karangan. Sumber di pinned comment. Sikap "mendiagnosis, bukan menggurui". | Hanya Anda |
| **Lentur** | Sudut cerita. Jenis representasi visual. Komposisi dan zona. Latar adegan (kertas grid, meja, papan, layar ponsel, ruang rapat). Ritme. Suasana musik. Bentuk penutup. | Dipilih per topik lewat matriks, dicatat di log |
| **Eksperimen** | Sisipan video AI tanpa teks dan tanpa wajah. Objek semi-3D. Foto asli sebagai kolase. Tata letak layar belah. Perkenalan sebagai lower third. | Maksimal satu per reels, ditandai di log, dinilai setelah ada data |

Aturan baca: kalau penonton menutup suara dan menutup nama akun, tiga detik pertama harus tetap terlihat sebagai video Anda. Itu uji DNA.

---

## 4. Dua sistem produksi

### 4.1 Tipe A: animasi penuh + voice over

**Keputusan arsitektur: kode sebagai utama.** Alasan:
- Teks Indonesia di layar harus tepat. Model video AI belum bisa diandalkan menulis teks.
- Sinkron per kata sudah ada di mesin sekarang. Video AI tidak bisa dijangkar ke kata.
- Karakter konsisten gratis di kode, mahal dan rapuh di AI.
- Aturan Anda: tanpa label AI di konten. Sisipan AI realistis bisa memicu kewajiban label platform (perlu dicek aturan terbaru Meta; saya belum memeriksanya).

**Sisipan AI boleh bila:** tanpa teks, tanpa wajah Anda, maksimal 2–3 detik, satu aksi, dan menggambarkan hal yang tidak bisa digambar kode dengan wajar (tekstur nyata, tangan, benda fisik).

**Alur**

1. Brief (satu pesan, kelas durasi).
2. Pilih variasi dari log.
3. Naskah, lalu Anda setujui.
4. Peta adegan: tiap kalimat diberi **fungsi**, bukan gambar. Fungsi yang tersedia: menunjukkan bukti, menunjukkan sebab-akibat, membandingkan, menunjukkan proses, menghadirkan orang, memberi jeda.
5. Kartu adegan dan ledger, lalu uji "layak ada".
6. Anda rekam voice over.
7. Pengenal suara → potong → bangun → gerbang mutu → serah.

**Uji "layak ada" per adegan** (gagal satu = adegan digabung atau dibuang)
1. Apa yang dijelaskan?
2. Kalau adegan ini dihapus, apa yang hilang dari pemahaman?
3. Satu objek atau aksi apa yang membawa maknanya?
4. Apa yang penonton pahami setelahnya?
5. Elemen DNA mana yang hadir?
6. Bisa dibuat stabil? (kode: selalu; sisipan AI: satu aksi, kamera diam atau dorong pelan)

**Sistem properti edukatif** (pustaka yang dibangun bertahap): kartu bukti, batang banding, garis grafik, layar chat, layar pencarian, figur orang, meja rapat, stempel, daftar centang, timbangan, tangga, corong, tampilan urai.

**Kontrol kerumitan:** maksimal satu hal baru bergerak per ketukan. Maksimal tiga elemen aktif di layar. Elemen diam lebih dari 2 detik bernapas halus. Keluar lebih cepat dari masuk.

**Kunci karakter:** figur orang dari `gen_owner.py` (proporsi, warna baju, garis muka) menjadi satu-satunya gaya orang. Peran dibedakan lewat warna baju dan satu atribut (kacamata, lanyard, celemek).

### 4.2 Tipe B: talking head + footage pendukung

**Prinsip:** wajah Anda adalah bukti. Grafis masuk hanya bila menambah arti.

**Pohon keputusan per segmen**

| Pertanyaan | Jika ya |
|---|---|
| Kalimat ini klaim, pendapat, atau pengalaman pribadi? | Wajah penuh. Tanpa grafis |
| Ada penekanan satu kata kunci? | Wajah + punch-in 1,08–1,15 di kata itu, lalu kembali |
| Ada angka, perbandingan, atau daftar? | Wajah tetap, grafis di zona samping atau atas. Tidak di tengah |
| Ada proses atau mekanisme yang sulit dibayangkan? | Potong ke B-roll atau animasi 2–4 dtk, suara Anda lanjut |
| Ada benda atau situasi nyata yang disebut? | Close-up kontekstual atau B-roll dokumenter |
| Tidak satu pun? | Wajah penuh. Diam bukan cacat |

Larangan: memotong hanya karena "sudah 4 detik". Potongan B-roll tanpa makna. B-roll kantor generik bergaya stok.

**Alur**

1. Brief, variasi, naskah (sama dengan A), ditambah **catatan penyampaian** per kalimat: tekanan kata, jeda, arah pandang.
2. Anda merekam. Syarat: vertikal 1080×1920, kamera sejajar mata, cahaya dari depan-samping, mikrofon yang sama dengan voice over, ruang kosong di atas kepala dan satu sisi untuk grafis.
3. Pengenal suara → rencana potong berbentuk tabel → Anda setujui → potong di batas kata dengan fade 30 ms.
4. Ledger: kamera, grafis, zona, masuk, keluar per ketukan. Diperiksa terhadap Variety Laws.
5. Grafis dirender dari mesin HTML yang sama dengan latar transparan, ditumpuk di atas footage. Caption paling akhir.
6. Gerbang mutu → serah.

**Status jujur:** langkah 3–5 belum dibangun. Komponennya ada (pengenal suara, pemotong, perender). Yang belum: lapisan transparan di atas video dan zoom pada footage. Perkiraan saya satu sampai dua sesi kerja setelah ada rekaman uji. Itu perkiraan, bukan janji.

**Bahasa kamera untuk Tipe B:** statis sebagai bawaan; dorong pelan 1,00→1,06 hanya di hook; punch-in pada kata; tidak ada orbit, tidak ada whip. Gerak istimewa maksimal satu per video.

---

## 5. Mesin naskah dan retensi

### 5.1 Anggaran kata (pagar durasi)

Tempo bicara Anda terukur 2,2 kata per detik setelah jeda dirapikan (reels Reddit: 288 kata dalam 132 detik).

| Kelas | Durasi | Maks kata | Pakai untuk | Syarat |
|---|---|---|---|---|
| **Pendek** | 30–45 dtk | 95 | TOFU, satu gagasan, satu langkah | Bawaan |
| **Standar** | 45–60 dtk | 130 | Satu gagasan + satu contoh | Bawaan untuk topik berita |
| **Cerita** | 60–90 dtk | 195 | Kasus bercerita (finance vs marketing) | Ditulis di brief, dengan alasan |
| Di atas 90 dtk | - | - | - | **Ditolak** sampai ada data retensi yang mendukung |

Perkenalan (20 kata, ±9 dtk) dihitung dalam anggaran.

### 5.2 Pemeriksaan naskah (lulus/gagal sebelum diskor)

- **Satu hal:** pesan inti bisa ditulis dalam satu kalimat 12 kata.
- **Hook:** maksimal 4 dtk; ketegangan atau angka muncul di 1,5 dtk pertama; bisa dibuktikan.
- **Pertanyaan terbuka:** hook membuka satu pertanyaan, jawabannya tidak muncul sebelum Insight.
- **Bertahap:** tiap kalimat menambah satu informasi baru. Kalimat yang mengulang, dibuang.
- **Uji ucap:** dibaca keras tanpa tersangkut; tidak ada kalimat di atas 14 kata; tidak ada tiga kalimat sama panjang berturut-turut.
- **Kata terlarang dan kata kaku:** daftar di `CLAUDE.md`.
- **Klaim:** tiap fakta punya sumber, tiap contoh berlabel ilustrasi, klaim diri Anda satu per video.
- **Satu langkah:** Reframe berisi satu tindakan. Daftar tiga hanya bila ketiganya bagian dari satu tindakan.
- **CTA:** satu, beralasan, penerima kiriman disebut.

### 5.3 Perkenalan: yang saya tantang

- **[Ditemukan]** Aturan 8 Nov: perkenalan penuh setelah hook, sebelum Relate.
- **[Tafsir]** Hook membuka pertanyaan, lalu 8 detik berikutnya tidak menjawab dan tidak menambah ketegangan. Di detik 4–12 itulah penonton baru memutuskan bertahan. Ini hipotesis, saya tidak punya data Anda.
- **[Usul]** Uji dua versi pada dua reels berikutnya:
  - Versi 1 (sekarang): perkenalan diucapkan penuh.
  - Versi 2: nama dan "100+ brand" tampil sebagai kartu kecil 3 detik sementara Anda langsung masuk Relate. Ucapan perkenalan dipendekkan jadi "Saya Aldy Syahreza, belasan tahun mendampingi brand."
  - Bandingkan retensi di detik 15. Putuskan dari angka.

---

## 6. Mesin variasi kreatif

### 6.1 Matriks

| Dimensi | Pilihan |
|---|---|
| Sudut cerita | pengalaman pribadi · kontrarian · kesalahan umum · masalah-solusi · sebelum-sesudah · bedah edukatif · mitos vs fakta · reflektif · berbasis kasus · analogi visual |
| Representasi | karakter berperan · situasi nyata · benda simbolik · lingkungan · sebab-akibat · proses · close-up detail · pengamatan dokumenter |
| Kamera | statis · dorong pelan · geser · over-the-shoulder · makro · lebar |
| Ritme emosi | tenang-reflektif · lugas-berwibawa · hangat-ngobrol · penasaran · edukatif · berenergi terkendali |
| Tempo | buka pelan · buka langsung · ungkap bertahap · kontras · selang-seling jelaskan dan tunjukkan |

### 6.2 Aturan pilih (bukan acak)

1. Topik menentukan sudut: berita → bedah atau kontrarian; konflik tim → berbasis kasus; kebiasaan owner → cermin atau kesalahan umum; metode Anda → pengalaman pribadi.
2. Sudut cerita tidak boleh sama dengan dua reels terakhir.
3. Bentuk penutup ("tiga hal") tidak boleh sama dengan reels sebelumnya.
4. Representasi dominan tidak boleh sama tiga kali berturut-turut.
5. Minimal satu dari tiga reels memakai sudut yang belum pernah dipakai.
6. Semua pilihan ditulis di log beserta alasannya.

### 6.3 Creative Variation Log

Berkas: `strategi/creative-log.md`. Sudah saya isi dari sepuluh reels yang ada. Kolom performa kosong menunggu data Anda.

---

## 7. Kecerdasan visual per adegan

Kartu adegan memuat 17 kolom dari instruksi Anda. Untuk adegan berbasis kode, kolom "prompt AI" dan "negative prompt" diganti "komponen kode" dan "larangan tata letak". Contoh terisi ada di bagian 9.

Terjemahan instruksi kabur menjadi pilihan konkret:

| Jangan tulis | Tulis |
|---|---|
| "sinematik" | "kamera statis setinggi mata, latar buram, satu sumber cahaya dari kiri" |
| "profesional" | "kemeja polos gelap, meja kayu bersih, tanpa logo terlihat" |
| "menarik" | sebutkan apa yang berubah di layar dan pada kata apa |
| "visual pendukung" | sebutkan fungsi: bukti, sebab-akibat, banding, proses, orang, jeda |

---

## 8. Gerbang mutu kreatif

14 metrik, skor 0–10, dinormalkan ke 100. Lulus: ≥ 85 dan tidak ada metrik inti di bawah 8.

Metrik inti: kekuatan hook, relevansi audiens, kejelasan informasi, konsistensi brand, kepercayaan, integritas klaim.

Aturan:
- Skor adalah penilaian heuristik saya. Bukan prediksi performa.
- Tiap skor di bawah 8 wajib memuat masalah, risiko bagi penonton, penyebab, revisi, dan versi yang lebih kuat.
- Integritas klaim tidak boleh dinilai 8 ke atas selama ada fakta yang belum dicek ulang.
- Setelah tayang, angka Instagram dicatat di log. Setelah sepuluh reels berdata, bobot metrik ditinjau: metrik yang tidak berhubungan dengan hasil dibuang.

---

## 9. Proof of concept: satu topik, dua versi

**Asumsi kerja:** saya memakai kandidat A yang saya sarankan kemarin karena Anda belum memilih. Kalau Anda memilih topik lain, kerangkanya tetap.

### 9.1 Brief

| | |
|---|---|
| Topik | AI membalas chat pelanggan: pakai suara siapa? |
| Audiens | Owner dengan admin chat, omzet > Rp100 juta |
| Masalah | Admin menjawab berbeda-beda; AI akan meniru itu dalam skala besar |
| Tujuan | TOFU: dikirim owner ke admin chat |
| Satu pesan | Sebelum AI membalas chat, tulis dulu cara brand kamu menjawab. |
| Sudut cerita | Kesalahan umum (belum pernah dipakai) |
| Satu langkah | Tulis lima jawaban standar |
| CTA | Kirim ke admin yang memegang chat |
| Kelas durasi | Standar, maks 130 kata |
| Jembatan | Kit Alasan Dipilih (disebut di caption, bukan di video) |

**Fakta yang wajib dicek ulang sebelum rekam** (dari bank topik 8 Nov, belum saya verifikasi lagi): Meta Business Agent di WhatsApp Business diluncurkan di Indonesia 11 Agu 2026; belajar dari arsip chat dan katalog; tiga mode.

### 9.2 Tiga arah kreatif

| | 1. Dua admin, satu pertanyaan | 2. AI sebagai pegawai baru | 3. Layar chat saja |
|---|---|---|---|
| Gagasan | Satu pertanyaan pelanggan dijawab berbeda oleh dua admin, lalu AI menyalin keduanya | AI digambarkan sebagai pegawai hari pertama yang diberi tumpukan arsip chat | Seluruh video adalah percakapan WhatsApp |
| Emosi | Cermin, sedikit geli | Hangat | Lugas |
| Kuat | Masalah terlihat dalam 5 detik. Memakai figur orang | Metafora mudah diingat | Paling murah dibuat |
| Lemah | Butuh dua karakter konsisten | Metafora "pegawai" bisa terasa klise | Mirip adegan chat di reels persona brand |
| Produksi | Sedang | Sedang | Ringan |

**Rekomendasi: arah 1.** Paling cepat membuat owner berkata "itu admin saya", dan memperkenalkan adegan berkarakter yang belum ada di pustaka.

### 9.3 Naskah (125 kata, perkiraan 57 detik)

| Babak | Ucapan | Catatan penyampaian |
|---|---|---|
| Hook | AI bales chat pelangganmu 24 jam. Pakai suara siapa? | Tekan "suara siapa". Jeda setengah detik setelahnya |
| Perkenalan | Sebelumnya, kenalin. Saya Aldy Syahreza. Belasan tahun mendampingi lebih dari seratus brand lintas industri, dari branding sampai strategi marketing. | Datar, cepat |
| Relate | Nah, coba cek chat toko kamu. Pertanyaannya sama: "bisa kurang, kak?" Admin pagi jawab begini. Admin malam jawab begitu. | "begini" dan "begitu" dibedakan nadanya |
| Insight | Sejak Agustus, WhatsApp Business punya agen AI yang belajar dari arsip chat kamu. Jadi AI gak bikin suara brand. Dia cuma ngulang yang udah ada. Lebih cepet, lebih sering. | Pelan di "ngulang yang udah ada" |
| Reframe | Jadi sebelum dinyalain, tulis dulu lima jawaban standar: harga, stok, kapan kirim, komplain, dan kalo ditawar. Contoh toko sepatu kerja. Ditawar? Jawabnya: "Harganya tetap, kak. Tapi kalo ukurannya gak pas, gratis tukar tujuh hari." | Kutipan diucapkan seperti admin yang ramah |
| CTA | Kirim video ini ke admin yang pegang chat kamu. Biar lima jawabannya ditulis minggu ini. | Lugas, tanpa senyum dipaksakan |

Catatan: "lima jawaban" adalah satu tindakan (menulis satu lembar), bukan lima langkah. Contoh sepatu kerja adalah ilustrasi dan menyambung ke reels iklan (gratis tukar ukuran 7 hari).

### 9.4 Versi A: animasi + voice over (9 adegan)

| # | Ucapan (awal) | Tujuan | Gagasan visual | Jenis | Subjek dan aksi | Kamera | Transisi | Dtk |
|---|---|---|---|---|---|---|---|---|
| 1 | "AI bales chat pelangganmu…" | Hentikan gulir | Layar chat; balasan muncul sendiri jam 02.14, gelembung "mengetik" tanpa orang | Situasi nyata | Gelembung balasan mengetik sendiri | Statis | Potong keras | 3 |
| 2 | "…pakai suara siapa?" | Buka pertanyaan | Gelembung balasan kosong, tanda tanya ditulis pena merah | Benda simbolik | Pena melingkari gelembung | Dorong pelan | Coretan | 2 |
| 3 | Perkenalan | Kredibilitas | Kartu foto + nama + angka (komponen baku) | - | - | Statis | Geser | 8 |
| 4 | "Pertanyaannya sama…" | Cermin | Satu gelembung pelanggan di tengah atas: "bisa kurang, kak?" | Situasi nyata | Gelembung jatuh ke tengah | Statis | - | 3 |
| 5 | "Admin pagi… admin malam…" | Tunjukkan masalah | Dua figur admin kiri-kanan, tiap orang mengeluarkan jawaban berbeda | Karakter berperan | Dua figur mengetik bergantian | Statis | - | 5 |
| 6 | "…agen AI yang belajar dari arsip…" | Sebab | Arsip chat dari kedua admin mengalir ke satu kotak "AI" | Sebab-akibat | Kartu chat bergerak masuk kotak | Geser pelan | Pindai amber (mode diagnosis) | 6 |
| 7 | "Dia cuma ngulang…" | Akibat | Kotak AI mengeluarkan dua jawaban yang sama-sama berbeda, berlipat ganda | Sebab-akibat | Jawaban menggandakan diri | Statis | - | 5 |
| 8 | "tulis dulu lima jawaban…" + contoh | Solusi dan wujudnya | Satu lembar "Cara kami menjawab" berisi lima baris; baris "ditawar" membesar dan menampilkan kutipan | Proses | Pena mengisi lima baris; satu baris disorot | Dorong pelan ke baris | Lembar masuk ke kotak AI | 14 |
| 9 | CTA | Tindakan | Lembar dikirim ke figur admin; ikon kirim | Karakter berperan | Lembar meluncur ke admin | Statis | Tahan 3 dtk | 6 |

Semua dari kode. Sisipan AI: tidak perlu. Elemen DNA: kertas grid, pena merah, caption pil, mode diagnosis di adegan 6.

### 9.5 Versi B: talking head + footage pendukung

| Segmen | Ucapan | Keputusan gambar | Alasan | Grafis / B-roll | Zona |
|---|---|---|---|---|---|
| Hook | "AI bales chat…suara siapa?" | Wajah penuh, dorong pelan 1,00→1,06 | Pertanyaan langsung butuh tatap mata | Teks "pakai suara siapa?" muncul di kata itu | Bawah tengah, di atas caption |
| Perkenalan | - | Wajah penuh | Sedang memperkenalkan diri | Lower third nama + "100+ brand" | Kiri bawah |
| Relate | "bisa kurang, kak?" | Wajah + grafis | Kutipan pelanggan lebih kuat dilihat | Gelembung chat pelanggan | Kanan atas |
| Relate | "Admin pagi… admin malam…" | Potong ke animasi 4 dtk | Perbandingan dua jawaban sulit dibayangkan dari ucapan | Dua gelembung jawaban berbeda, layar penuh | Penuh |
| Insight | "Sejak Agustus…arsip chat kamu" | B-roll 3 dtk | Benda nyata disebut | Close-up tangan memegang ponsel dengan daftar chat (rekam sendiri, atau sisipan AI) | Penuh |
| Insight | "AI gak bikin suara brand…" | **Wajah penuh, tanpa grafis** | Ini kalimat inti. Ekspresi adalah isinya | - | - |
| Reframe | "tulis dulu lima jawaban…" | Wajah + daftar | Daftar perlu dilihat | Lima baris muncul satu per satu | Kiri tengah |
| Reframe | contoh sepatu kerja | Potong ke animasi 5 dtk | Kutipan jawaban harus terbaca | Lembar "Cara kami menjawab" dengan kutipan | Penuh |
| CTA | "Kirim video ini…" | Wajah penuh, punch-in 1,10 di "admin" | Ajakan pribadi | Ikon kirim kecil | Kanan bawah |

Jumlah potongan dari wajah: tiga, masing-masing dengan alasan. Wajah Anda di layar ±70% durasi.

**Prompt sisipan B-roll** (hanya bila Anda tidak merekam sendiri; untuk image-to-video di Higgsfield atau Krea, belum diuji):

```
Close-up of a hand holding a smartphone above a wooden desk, thumb slowly scrolling
a messaging app chat list. Screen content soft and unreadable. Warm window light from
the left, shallow depth of field, cream and terracotta tones, static camera, 3 seconds,
one continuous action.
Negative: readable text, logos, brand names, face, multiple hands, fast motion,
camera shake, morphing fingers, neon or blue-teal grading, stock-photo office.
```

Saran saya: **rekam sendiri dengan ponsel**. Lebih otentik, tanpa risiko label AI, selesai dalam dua menit.

### 9.6 Perbandingan

| | Versi A | Versi B |
|---|---|---|
| Efektivitas pesan | Mekanisme "AI menyalin" sangat jelas | Kalimat inti lebih dipercaya karena diucapkan ke kamera |
| Dampak kreatif | Adegan dua admin baru untuk pustaka | Format baru bagi akun Anda |
| Cocok brand | Tinggi (DNA penuh) | Tinggi bila grafis memakai DNA yang sama |
| Logika retensi | Tiap adegan mengganti gambar; risiko di perkenalan | Wajah menahan; risiko bila penyampaian datar |
| Kelayakan produksi | Bisa hari ini setelah voice over | Butuh rekaman dan mesin yang belum dibangun |
| Membangun apa | Pemahaman | Kepercayaan |

### 9.7 Audit mutu naskah POC (heuristik)

| Metrik | Skor | Catatan |
|---|---|---|
| Kekuatan hook | 8 | Sembilan kata, pertanyaan jelas. Belum ada angka atau kerugian yang terasa; kekuatannya bergantung pada cara Anda mengucapkan |
| Relevansi audiens | 9 | Owner dengan admin chat langsung kena |
| Kualitas copy | 8 | Kosakata Aldy v2 dipakai |
| Koherensi narasi | 9 | Satu garis: beda jawaban → AI menyalin → tulis dulu |
| Kejelasan informasi | 8 | "Lima jawaban" jelas; "dinyalain" mengandaikan penonton tahu fiturnya |
| Ritme ucap | 8 | Perlu uji baca keras oleh Anda |
| Relevansi visual | 9 | Tiap adegan punya fungsi |
| Diferensiasi kreatif | 8 | Sudut dan adegan baru; penutup bukan "tiga hal" |
| Konsistensi brand | 9 | - |
| Kelayakan produksi | 9 (A) / 6 (B) | B menunggu mesin |
| Potensi retensi | 7 | Perkenalan 8 dtk setelah hook. Lihat 5.3 |
| Kepercayaan | 8 | - |
| Efektivitas CTA | 9 | Penerima dan alasan jelas |
| Integritas klaim | **6** | Fakta WhatsApp belum dicek ulang |

Total versi A: 115/140 = **82/100. Belum lulus.** Dua penghalang: integritas klaim (inti, di bawah 8) dan potensi retensi. Perbaikan: verifikasi fakta WhatsApp dan putuskan uji perkenalan. Kalau keduanya beres, skornya naik ke kisaran 86–88.

---

## 10. Rekomendasi akhir

**Sistem:** satu identitas, dua mesin. Tipe A sebagai andalan mingguan. Tipe B satu dari tiga reels setelah pilot berhasil. Rasio itu asumsi awal, ditinjau dari data.

**Prioritas skill:** pagar durasi → log performa dan variasi → gerbang mutu → kartu adegan dan ledger → mesin Tipe B.

**Alat:** tidak perlu alat baru. Higgsfield dan Krea sudah terhubung untuk sisipan bila diperlukan. Pengenal suara lokal sudah ada.

**Perbaikan paling berdampak:**
1. Anda mengirim angka Instagram tiap reels (retensi 3 dtk, rata-rata tonton, simpan, kirim, jangkauan non-pengikut).
2. Kelas durasi dipilih di brief dan dikunci.
3. Reframe kembali ke satu tindakan.
4. Pilot Tipe B.
5. Uji perkenalan.

**Risiko penerapan:**
- Sistem menjadi birokrasi. Penangkal: brief, variasi, dan peta adegan muat satu halaman; gerbang mutu otomatis sebisanya.
- Skor heuristik dianggap kebenaran. Penangkal: bagian 8.
- Tipe B menunda produksi. Penangkal: Tipe A tetap jalan selama mesin B dibangun.
- Variasi mengikis identitas. Penangkal: uji DNA di bagian 3.

**Langkah berikutnya yang paling bernilai:** setujui atau koreksi tiga hal di bawah.

1. Kelas durasi di 5.1 (termasuk menolak di atas 90 detik).
2. Uji perkenalan di 5.3.
3. Topik POC, dan versi mana yang diproduksi lebih dulu.

Lalu kirim dua bahan: tangkapan layar insight reels yang sudah tayang, dan satu rekaman uji talking head 30–60 detik.
