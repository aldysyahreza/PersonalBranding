# Uji variasi VoiceStudio TANPA pasca-proses (jeda asli model dibiarkan).
# Pakai: .\generate_uji.ps1 -TextFile teks.txt -Out hasil.wav -Temp 0.6 -Seed 7 -Speed 1.1
param(
  [Parameter(Mandatory = $true)][string]$TextFile,
  [Parameter(Mandatory = $true)][string]$Out,
  [string]$Temp = "0.3", [string]$Seed = "7", [string]$Speed = "1.1",
  [string]$Api = "http://127.0.0.1:3900"
)
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$text = (Get-Content $TextFile -Raw -Encoding UTF8).Trim()
$refText = (Get-Content "$here\ref_text.txt" -Raw -Encoding UTF8).Trim()
try { Invoke-WebRequest "$Api/model/status" -UseBasicParsing -TimeoutSec 5 | Out-Null }
catch { throw "VoiceStudio tidak aktif di $Api. Buka aplikasinya dulu." }
curl.exe -s -m 900 -X POST "$Api/generate" `
  -F "text=$text" -F "language=id" -F "seed=$Seed" -F "class_temperature=$Temp" -F "speed=$Speed" `
  -F "ref_audio=@$here\ref.wav" -F "ref_text=$refText" `
  -o $Out -w "generate http=%{http_code}`n"
if ((Get-Item $Out).Length -lt 4000) { throw "Gagal: $(Get-Content $Out -Raw)" }
"Selesai: $Out"
