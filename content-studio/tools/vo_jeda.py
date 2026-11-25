"""Sisipkan jeda hening setelah satu kata di vo_clean.wav dan geser timing.json.
Pakai: python3 tools/vo_jeda.py out/reelNN "Ringelmann." 1.0   (total jeda sesudah kata = 1.0 dtk)"""
import json, sys, wave, numpy as np
d, word, total = sys.argv[1], sys.argv[2], float(sys.argv[3])
tj = json.load(open(d + '/timing.json')); W = [w for b in tj['beats'] for w in b['words']]
i = next(k for k, w in enumerate(W) if w['w'] == word)
w = wave.open(d + '/vo_clean.wav'); pr = w.getparams(); sr = pr.framerate
x = np.frombuffer(w.readframes(pr.nframes), '<i2').reshape(-1, pr.nchannels).astype(np.float32); w.close()
a, b = W[i]['t'], W[i + 1]['t']; win = int(.01 * sr)
e = np.abs(x[:, 0]); lo, hi = int((a + .3) * sr), int(b * sr)
env = np.convolve(e, np.ones(win) / win, 'same')
# akhir ucapan = titik terakhir di atas -45 dB sebelum kata berikutnya
loud = np.flatnonzero(env[lo:hi] > 32768 * 10 ** (-45 / 20)); 
end = lo + (loud[loud < (hi - lo) * .7][-1] if len(loud) and (loud < (hi - lo) * .7).any() else 0)
cur = (hi - end) / sr; P = max(0.0, total - cur)
cut = end + int(.05 * sr); f = int(.012 * sr); r = np.linspace(1, 0, f)[:, None]
y1 = x[:cut].copy(); y1[-f:] *= r; y2 = x[cut:].copy(); y2[:f] *= r[::-1]
y = np.concatenate([y1, np.zeros((int(P * sr), pr.nchannels), np.float32), y2]).astype(np.int16)
w = wave.open(d + '/vo_clean.wav', 'wb'); w.setparams(pr); w.writeframes(y.tobytes()); w.close()
t0 = cut / sr
for bt in tj['beats']:
    if bt['start'] > t0: bt['start'] = round(bt['start'] + P, 3)
    elif bt['start'] + bt['dur'] > t0: bt['dur'] = round(bt['dur'] + P, 3)
    for wd in bt['words']:
        if wd['t'] > t0: wd['t'] = round(wd['t'] + P, 3)
tj['duration'] = round(tj['duration'] + P, 3); json.dump(tj, open(d + '/timing.json', 'w'), ensure_ascii=False, indent=1)
print('jeda setelah %r: %.2f -> %.2f dtk (disisip %.2f di %.2f)' % (word, cur, cur + P, P, t0))
