"""Gerbang mutu VO: WAJIB lulus sebelum render.
Pakai: python3 tools/vo_cek.py vo/voNN_raw.ogg out/reelNN
Cek: (1) decoder: bandingkan decode bawaan ffmpeg vs libopus -> lokasi lonjakan yang dihindari
     (2) vo_clean.wav: nada tajam >3 kHz (lonjakan), sampel mentok (pecah), puncak, loudness"""
import subprocess, sys, wave, numpy as np
raw, d = sys.argv[1], sys.argv[2]; ok = True
def dec(pre):
    return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', *pre, '-i', raw, '-f', 'f32le', '-ac', '1', '-'], capture_output=True).stdout, np.float32)
codec = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=codec_name', '-of', 'csv=p=0', raw], capture_output=True, text=True).stdout.strip()
if codec == 'opus':
    a = dec([]); b = dec(['-c:a', 'libopus']); n = min(len(a), len(b)) - 4
    best = max(range(-4, 5), key=lambda k: float(np.dot(a[1000:200000], b[1000 + k:200000 + k])))
    b = np.roll(b, -best); w = 2400; m = n // w
    ra = np.sqrt((a[:m * w].reshape(m, w) ** 2).mean(1)); rb = np.sqrt((b[:m * w].reshape(m, w) ** 2).mean(1))
    bad = sorted({round(i * w / 48000, 1) for i in np.flatnonzero((ra > .1) & (ra > 1.8 * rb))})
    print('[1] decoder bawaan akan menyisipkan lonjakan di %d titik (dihindari dengan libopus): %s' % (len(bad), bad[:15]))
w = wave.open(d + '/vo_clean.wav'); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), '<i2').reshape(-1, w.getnchannels())[:, 0] / 32768
W = int(.05 * sr); burst = []
for i in range(0, len(x) - W, W):
    s = x[i:i + W]
    if np.sqrt((s ** 2).mean()) < .05: continue
    S = np.abs(np.fft.rfft(s * np.hanning(W))) ** 2; f = np.fft.rfftfreq(W, 1 / sr); k = np.argmax(S * (f > 3000))
    if S[max(0, k - 3):k + 4].sum() / S.sum() > .5: burst.append(round(i / sr, 2))
pk = np.abs(x).max(); stuck = int((np.abs(x) > .999).sum())
lu = subprocess.run(['ffmpeg', '-nostats', '-i', d + '/vo_clean.wav', '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
I = [l for l in lu.splitlines() if l.strip().startswith('I:')][-1].split()[1]
print('[2] vo_clean: lonjakan nada %d %s | sampel mentok %d | puncak %.1f dBFS | loudness %s LUFS' % (len(burst), burst[:10], stuck, 20 * np.log10(pk), I))
if burst or stuck > 0 or pk > 10 ** (-1 / 20): ok = False
print('LULUS' if ok else 'GAGAL: jangan render, periksa titik di atas'); sys.exit(0 if ok else 1)
