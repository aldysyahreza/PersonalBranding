"""Efek suara + musik latar buatan kode untuk animatic-pillar (bebas lisensi).
Pakai:
  python3 animatic/sfx-pillar.py out/sfx.wav                          -> satu file gabungan, waktu rancangan
  python3 animatic/sfx-pillar.py out/dir --timing out/vo/timing.json  -> out/dir/music.wav + fx.wav mengikuti voice over
Musik dan efek dipisah supaya hanya musik yang mengecil saat Anda bicara (ducking di build_reel.py)."""
import json, os, sys, wave
import numpy as np

SR = 48000
DESIGN = [3.78, 4.26, 5.29, 3.81, 6.57, 6.6, 3.15, 3.27, 2.65, 4.43, 4.26, 2.35, 9.52]   # durasi rancangan tiap langkah (sama dengan DEF di animatic-pillar.html)
args = sys.argv[1:]
TIMING = args[args.index('--timing') + 1] if '--timing' in args else None
if TIMING:
    tl = json.load(open(TIMING, encoding='utf-8'))
    T0 = [b['start'] for b in tl['beats']]; DURS = [b['dur'] for b in tl['beats']]; DUR = tl['duration']
else:
    T0 = list(np.cumsum([0] + DESIGN[:-1])); DURS = DESIGN; DUR = float(sum(DESIGN))
SPEED = [max(1, d / a) for d, a in zip(DESIGN, DURS)]
WARP = [None] * len(DESIGN)
ANCH_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'anchors-pillar.json')
if TIMING and os.path.exists(ANCH_FILE):  # jangkar kata: sama persis dengan LOCAL() di animatic-pillar.html
    anch = json.load(open(ANCH_FILE, encoding='utf-8'))['beats']
    nrm = lambda s: ''.join(c for c in s.lower() if c.isalnum())
    for i, b in enumerate(tl['beats']):
        pts, frm = [(0.0, 0.0)], 0
        for d, word in anch[i]:
            for k in range(frm, len(b['words'])):
                if nrm(b['words'][k]['w']).startswith(word):
                    r = b['words'][k]['t'] - T0[i]
                    if r > pts[-1][1] + 0.05 and d > pts[-1][0]: pts.append((d, r))
                    frm = k + 1; break
        WARP[i] = pts if len(pts) > 1 else None


def at(i, off):  # waktu event = waktu nyata saat animasi langkah i mencapai detik rancangan off
    p = WARP[i]
    if not p: return T0[i] + off / SPEED[i]
    for k in range(1, len(p)):
        if off <= p[k][0]: return T0[i] + p[k - 1][1] + (off - p[k - 1][0]) * (p[k][1] - p[k - 1][1]) / (p[k][0] - p[k - 1][0])
    d, r = p[-1]; tail = max(1, (DESIGN[i] - d) / max(0.3, DURS[i] - r))
    return T0[i] + r + (off - d) / tail
rng = np.random.default_rng(7)
out = np.zeros(int(SR * (DUR + 1)))
mus = np.zeros(int(SR * (DUR + 1)))

def env(n, a=0.005, r=0.1):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(r, 1e-4))
    return e

def lowpass(x, cut0, cut1):  # filter satu kutub dengan frekuensi potong yang bergerak
    y = np.zeros_like(x); s = 0.0
    cuts = np.linspace(cut0, cut1, len(x))
    k = 1 - np.exp(-2 * np.pi * cuts / SR)
    for i in range(len(x)):
        s += k[i] * (x[i] - s); y[i] = s
    return y

def add(t, sig, gain):
    i = int(t * SR); out[i:i + len(sig)] += sig[:len(out) - i] * gain

def whoosh(t, up=True, d=0.42, g=0.55):
    n = int(d * SR); x = rng.standard_normal(n)
    y = lowpass(x, 300, 3200) if up else lowpass(x, 3200, 300)
    w = np.sin(np.linspace(0, np.pi, n)) ** 2
    add(t - d * 0.4, y * w, g)

def pop(t, f0=700, f1=320, g=0.35):
    n = int(0.09 * SR); ph = np.cumsum(np.linspace(f0, f1, n)) / SR * 2 * np.pi
    add(t, np.sin(ph) * env(n, 0.002, 0.03), g)

def tick(t, g=0.18):
    n = int(0.018 * SR); add(t, rng.standard_normal(n) * env(n, 0.0005, 0.004), g)

def thud(t, g=0.8):
    n = int(0.35 * SR); tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * (95 - 40 * tt / 0.35) * tt) * np.exp(-tt / 0.09) + 0.25 * rng.standard_normal(n) * np.exp(-tt / 0.02)
    add(t, s, g)

def scratch(t, d=0.25, g=0.22):
    n = int(d * SR); x = rng.standard_normal(n); y = x - lowpass(x, 2500, 2500)
    am = 0.6 + 0.4 * np.sin(np.linspace(0, d * 2 * np.pi * 18, n))
    add(t, y * am * np.sin(np.linspace(0, np.pi, n)), g)

def sweep(t, d=0.9, g=0.18):
    n = int(d * SR); ph = np.cumsum(np.linspace(240, 1400, n)) / SR * 2 * np.pi
    add(t, (np.sin(ph) + 0.3 * np.sin(2 * ph)) * np.sin(np.linspace(0, np.pi, n)), g)

def buzz(t, d, g=0.07):
    n = int(d * SR); tt = np.arange(n) / SR
    add(t, np.sign(np.sin(2 * np.pi * 120 * tt)) * (0.5 + 0.5 * np.sin(2 * np.pi * 9 * tt)) * np.minimum(1, tt / 0.05) * np.minimum(1, (d - tt) / 0.05), g)

def chime(t, g=0.2):
    for k, f in enumerate([1046.5, 1318.5, 1568]):
        n = int(0.6 * SR); tt = np.arange(n) / SR
        add(t + k * 0.06, np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.18), g * 0.6)

# ---------- musik latar: pad lembut + denyut pelan, 96 bpm ----------
n = len(out); tt = np.arange(n) / SR
chords = [[220, 261.6, 329.6], [196, 246.9, 293.7], [174.6, 220, 261.6], [196, 246.9, 329.6]]
bar = 60 / 96 * 4
pad = np.zeros(n)
for i in range(int(DUR / bar) + 2):
    a, b = int(i * bar * SR), int((i + 1) * bar * SR)
    seg = tt[a:b] - i * bar
    if not len(seg): break
    e = np.minimum(1, seg / 0.8) * np.minimum(1, (bar - seg) / 0.6)
    pad[a:b] += sum(np.sin(2 * np.pi * f * tt[a:b]) + 0.3 * np.sin(4 * np.pi * f * tt[a:b]) for f in chords[i % 4]) * e
pad = lowpass(pad, 900, 900) * 0.05
beat = 60 / 96
for k in range(int(DUR / beat)):
    tk = k * beat
    m = int(0.12 * SR); s = np.sin(2 * np.pi * 55 * np.arange(m) / SR) * np.exp(-np.arange(m) / SR / 0.05)
    i = int(tk * SR); pad[i:i + m] += s * (0.10 if k % 2 == 0 else 0.05)
fade = np.minimum(1, tt / 1.0) * np.minimum(1, np.maximum(0, (DUR + 0.5 - tt)) / 1.2)
mus += pad * fade

# ---------- event per adegan ----------
pop(at(0, 0.25)); [tick(at(0, 0.5 + k * 0.1), 0.1) for k in range(10)]; thud(at(0, 2.9), 0.6)
whoosh(T0[1], up=True); pop(at(1, 0.2), 700, 320, 0.3); pop(at(1, 1.1), 900, 450, 0.22); [tick(at(1, 2.3 + k * 0.1), 0.1) for k in range(10)]
whoosh(T0[2], up=False)
for a in (0.3, 1.0, 1.9): pop(at(2, a), 800, 400, 0.25)
pop(at(2, 3.1), 600, 260, 0.3); thud(at(2, 4.6), 0.7)
whoosh(T0[3], up=False); sweep(at(3, 0.9), 0.9 / SPEED[3])
for k in range(6): tick(at(3, 1.75 + k * 0.12), 0.12)
whoosh(T0[4] - 0.05, up=True, g=0.4)
chime(at(4, 0.55), 0.14); scratch(at(4, 2.6), 0.4, 0.2); pop(at(4, 3.6), 800, 400, 0.25); thud(at(4, 4.4), 0.6)
whoosh(T0[5], up=True)
for k in range(8): pop(at(5, 2.45 + k * 0.15), 900, 500, 0.12)
pop(at(5, 3.92), 800, 400, 0.3); pop(at(5, 3.3), 800, 400, 0.2)
whoosh(T0[6], up=False, d=0.3, g=0.35); pop(at(6, 0.72), 800, 400, 0.22); pop(at(6, 2.16), 800, 400, 0.22)
pop(at(7, 0.64), 800, 400, 0.22); chime(at(7, 2.68), 0.14)
whoosh(T0[8], up=True, d=0.3, g=0.35); scratch(at(8, 1.4), 0.8, 0.2); thud(at(8, 1.83), 0.5)
whoosh(T0[9], up=False, d=0.3, g=0.35); pop(at(9, 0.2), 800, 400, 0.22); chime(at(9, 3.18), 0.16)
pop(at(10, 0.2), 800, 400, 0.22); chime(at(10, 3.05), 0.16)
whoosh(T0[11], up=True); pop(at(11, 0.8), 800, 400, 0.25); pop(at(11, 1.35), 800, 400, 0.25)
whoosh(T0[12], up=True); pop(at(12, 0.2), 700, 300, 0.3); pop(at(12, 1.15), 650, 330, 0.3); chime(at(12, 1.2), 0.14)
tick(at(12, 3.3), 0.2); pop(at(12, 5.4), 800, 400, 0.22); pop(at(12, 6.35), 800, 400, 0.25); chime(at(12, 6.4), 0.16)
thud(at(12, 8.4), 0.5); scratch(at(12, 8.5), 0.3, 0.18)

def save(p, x, peak):
    x = x[:int(SR * DUR)]; x = x / max(1e-9, np.max(np.abs(x))) * peak
    with wave.open(p, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype('<i2').tobytes())


if TIMING:
    os.makedirs(args[0], exist_ok=True)
    save(os.path.join(args[0], 'music.wav'), mus, 0.5); save(os.path.join(args[0], 'fx.wav'), out, 0.8)
    print('ok', args[0], 'music.wav + fx.wav', round(DUR, 1), 'dtk')
else:
    save(args[0], out + mus, 0.85); print('ok', args[0], round(DUR, 1), 'dtk')
