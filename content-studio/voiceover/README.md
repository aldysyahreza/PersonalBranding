# Voice over suara Aldy (klon lokal VoiceStudio)

Mengubah file teks menjadi WAV dengan suara Aldy, tanpa API berbayar.

## Syarat
1. Aplikasi **VoiceStudio** terbuka (API lokal di `http://127.0.0.1:3900`).
2. **WSL Ubuntu** dengan ffmpeg dari skill `buat-video-motion-grafik` (untuk pasca-proses napas/jeda).
3. Lisensi: bobot model OmniVoice **CC-BY-NC (non-komersial)**. Cek sebelum dipakai untuk konten yang menghasilkan uang atau untuk klien.

## Pemakaian
```powershell
.\generate.ps1 -TextFile naskah.txt -Out hasil.wav
```
Hasil: WAV 24 kHz mono, napas diredam dan jeda dipendekkan (versi "halus").

## Pengaturan yang disetujui
| Parameter | Nilai |
|---|---|
| Referensi suara | `ref.wav` (15 dtk dari rekaman Aldy) + `ref_text.txt` |
| `class_temperature` | 0.3 (lebih ekspresif dari bawaan 0) |
| `seed` | 7 (hasil bisa diulang) |
| `speed` | 1.0 |
| `language` | `id` |
| Pasca-proses | `silenceremove` (jeda >0,2 dtk jadi ~0,12 dtk) + `agate` (redam napas pelan) |

Ukuran kasar hasilnya: tempo sekitar 2,8 kata/dtk, nada tengah sekitar 163 Hz, rentang intonasi sekitar 12,7 semitone (reel Aldy sekitar 15-18).

## Menyambungkan ke proyek Content Studio The Brand Fixer
1. Salin folder `voiceover/` ini ke dalam proyek Content Studio (atau tunjuk jalurnya dari sana).
2. Di sesi Claude Code proyek itu, tempel instruksi ini:

> Di folder `voiceover/` ada `generate.ps1` yang membuat voice over suara Aldy dari file teks (klon lokal VoiceStudio, pengaturan sudah dikunci di README). Untuk setiap konten: tulis naskah ke file .txt, jalankan `.\voiceover\generate.ps1 -TextFile naskah.txt -Out vo.wav`, lalu pakai `vo.wav` sebagai audio di visual. Jangan ubah `ref.wav`, `ref_text.txt` atau pengaturannya tanpa izin. Jangan memasukkan API key apa pun.

3. Sinkronkan visual ke durasi `vo.wav` (animasi mengikuti suara, bukan sebaliknya).

## Catatan
- Sampel referensi dipotong acak dari rekaman 3 dan awal kalimatnya terpotong ("kan turunnya..."). Rekaman baru yang lebih ekspresif dan dipotong di batas kalimat bisa memperbaiki intonasi.
- Nama orang/brand kadang salah dibaca; cek hasilnya, dan tulis ejaan fonetik di naskah kalau perlu.
