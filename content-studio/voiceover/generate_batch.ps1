# Buat voice over suara Aldy per KALIMAT (klon lokal VoiceStudio), supaya durasi tiap kalimat pasti dan tidak perlu menebak batas kalimat.
# Pemakaian:  .\generate_batch.ps1 -LinesFile naskah\reddit.kalimat.txt -OutDir hasil\reddit
# Opsi uji:   -Limit 3   (hanya 3 kalimat pertama)
# Hasil: OutDir\kalimat_001.wav, kalimat_002.wav, ... (WAV 24 kHz mono, pasca-proses "halus" sama dengan generate.ps1).
# Pengaturan DIKUNCI (jangan diubah tanpa izin Aldy): class_temperature=0.3, seed=7, speed=1.0, language=id, referensi ref.wav + ref_text.txt.
param(
  [Parameter(Mandatory = $true)][string]$LinesFile,
  [Parameter(Mandatory = $true)][string]$OutDir,
  [int]$Limit = 0,
  [string]$Api = "http://127.0.0.1:3900"
)
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$refText = (Get-Content "$here\ref_text.txt" -Raw -Encoding UTF8).Trim()
$lines = @(Get-Content $LinesFile -Encoding UTF8 | Where-Object { $_.Trim() -ne "" })
if ($Limit -gt 0) { $lines = $lines | Select-Object -First $Limit }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$OutDir = (Resolve-Path $OutDir).Path

try { Invoke-WebRequest "$Api/model/status" -UseBasicParsing -TimeoutSec 5 | Out-Null }
catch { throw "VoiceStudio tidak aktif di $Api. Buka aplikasinya dulu." }

function ToWsl($p) { $f = (Resolve-Path $p).Path; "/mnt/" + $f.Substring(0,1).ToLower() + ($f.Substring(2) -replace '\\','/') }

$i = 0
foreach ($line in $lines) {
  $i++
  $name = "kalimat_{0:D3}" -f $i
  $raw = Join-Path $OutDir "$name.mentah.wav"
  # teks kalimat ditulis ke file sementara supaya karakter khusus aman
  $tmp = Join-Path $OutDir "$name.txt"
  [IO.File]::WriteAllText($tmp, $line.Trim(), (New-Object System.Text.UTF8Encoding($false)))
  Write-Host ("[{0}/{1}] {2}" -f $i, $lines.Count, $line.Trim())
  curl.exe -s -m 900 -X POST "$Api/generate" `
    -F "text=<$tmp" -F "language=id" -F "seed=7" -F "class_temperature=0.3" -F "speed=1.0" `
    -F "ref_audio=@$here\ref.wav" -F "ref_text=$refText" `
    -o $raw -w "  http=%{http_code}`n"
  if ((Get-Item $raw).Length -lt 4000) { throw "Gagal di kalimat ${i}: $(Get-Content $raw -Raw)" }
  Remove-Item $tmp
}

# Pasca-proses semua file sekaligus (satu panggilan WSL): jeda dipendekkan, napas pelan diredam
$outW = ToWsl $OutDir
$sh = "$env:TEMP\vo-postproc-batch.sh"
$lines2 = @(
  '#!/bin/bash',
  'FF=$(ls -d /home/aldy/.cache/km-video-components/*/ffmpeg-*/bin/ffmpeg | head -1)',
  ('cd "{0}"' -f $outW),
  'for f in kalimat_*.mentah.wav; do',
  '  o="${f/.mentah/}"',
  '  "$FF" -y -v error -i "$f" -af "silenceremove=stop_periods=-1:stop_duration=0.2:stop_threshold=-42dB:stop_silence=0.12,agate=threshold=0.012:ratio=3:attack=5:release=80:range=0.1" -c:a pcm_s16le "$o" && rm "$f"',
  'done'
)
[IO.File]::WriteAllText($sh, ($lines2 -join "`n") + "`n")
wsl -d Ubuntu -- bash (ToWsl $sh)
if ($LASTEXITCODE -ne 0) { throw "ffmpeg gagal" }
"Selesai: $i kalimat di $OutDir"
