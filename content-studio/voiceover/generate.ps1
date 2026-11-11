# Buat voice over (suara Aldy, klon lokal VoiceStudio) dari file teks.
# Pemakaian:  .\generate.ps1 -TextFile naskah.txt -Out hasil.wav
# Syarat: aplikasi VoiceStudio terbuka (API di 127.0.0.1:3900) dan WSL Ubuntu dengan ffmpeg dari skill buat-video-motion-grafik.
param(
  [Parameter(Mandatory = $true)][string]$TextFile,
  [Parameter(Mandatory = $true)][string]$Out,
  [string]$Api = "http://127.0.0.1:3900"
)
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$text = (Get-Content $TextFile -Raw -Encoding UTF8).Trim()
$refText = (Get-Content "$here\ref_text.txt" -Raw -Encoding UTF8).Trim()
$raw = [IO.Path]::ChangeExtension($Out, ".mentah.wav")

try { Invoke-WebRequest "$Api/model/status" -UseBasicParsing -TimeoutSec 5 | Out-Null }
catch { throw "VoiceStudio tidak aktif di $Api. Buka aplikasinya dulu." }

# Pengaturan yang disetujui: class_temperature=0.3, seed=7, speed=1.0, referensi rekaman 3
curl.exe -s -m 900 -X POST "$Api/generate" `
  -F "text=$text" -F "language=id" -F "seed=7" -F "class_temperature=0.3" -F "speed=1.0" `
  -F "ref_audio=@$here\ref.wav" -F "ref_text=$refText" `
  -o $raw -w "generate http=%{http_code}`n"
if ((Get-Item $raw).Length -lt 4000) { throw "Gagal: $(Get-Content $raw -Raw)" }

# Pasca-proses "halus": jeda dipendekkan, napas pelan diredam
function ToWsl($p) { $f = (Resolve-Path $p).Path; "/mnt/" + $f.Substring(0,1).ToLower() + ($f.Substring(2) -replace '\\','/') }
$in = ToWsl $raw
$outDir = ToWsl (Split-Path -Parent (Resolve-Path $raw).Path)
$outName = Split-Path -Leaf $Out
$sh = "$env:TEMP\vo-postproc.sh"
$lines = @(
  '#!/bin/bash',
  'FF=$(ls -d /home/aldy/.cache/km-video-components/*/ffmpeg-*/bin/ffmpeg | head -1)',
  ('"$FF" -y -v error -i "{0}" -af "silenceremove=stop_periods=-1:stop_duration=0.2:stop_threshold=-42dB:stop_silence=0.12,agate=threshold=0.012:ratio=3:attack=5:release=80:range=0.1" -c:a pcm_s16le "{1}/{2}"' -f $in, $outDir, $outName)
)
[IO.File]::WriteAllText($sh, ($lines -join "`n") + "`n")
wsl -d Ubuntu -- bash (ToWsl $sh)
if ($LASTEXITCODE -ne 0) { throw "ffmpeg gagal" }
Remove-Item $raw
"Selesai: $Out"
