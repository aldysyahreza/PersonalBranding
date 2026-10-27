"""Efek suara + musik latar buatan kode untuk animatic-v3 (bebas lisensi).
Waktu event mengikuti timeline di animatic-v3.html. Pakai: python3 animatic/sfx-v3.py out/sfx-v3.wav
Nanti voice over Anda ditaruh di atasnya; musik otomatis mengecil saat Anda bicara (ducking di ffmpeg)."""
import sys, wave
import numpy as np

SR = 48000
DUR = 37.6
T0 = [0, 4.4, 10.0, 15.4, 22.0, 27.4, 32.4]
rng = np.random.default_rng(7)
out = np.zeros(int(SR * (DUR + 1)))

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
out += pad * fade

# ---------- event per langkah (sinkron dengan animasi) ----------
pop(0.15)                                  # lencana diskon
scratch(0.95); tick(1.05); tick(1.15)      # coretan harga
scratch(1.9); tick(2.0); tick(2.1)
whoosh(T0[1], up=True)                     # zoom-through
for i in range(4): pop(T0[1] + 0.35 + i * 0.42, 900, 500, 0.22)
pop(T0[1] + 3.0, 600, 260, 0.35)
whoosh(T0[2], up=False)                    # whip
buzz(T0[2] + 0.15, 1.6)
for k in range(15): tick(T0[2] + 1.8 + k * 0.12, 0.12)
whoosh(T0[3], up=False)
thud(T0[3] + 0.55, 0.55); thud(T0[3] + 0.8, 0.45)
scratch(T0[3] + 1.2, 0.6, 0.18)
sweep(T0[3] + 2.6)
for i in range(3): pop(T0[3] + 3.8 + i * 0.55, 800, 400, 0.25)
whoosh(T0[4] - 0.05, up=True, g=0.4)       # kilat keluar mode diagnosis
thud(T0[4] + 0.5, 0.6)                      # kartu disematkan
chime(T0[4] + 3.1, 0.18)                    # sorot "akarnya"
whoosh(T0[5], up=True)
scratch(T0[5] + 1.6, 1.1, 0.16)             # pensil mencoret
pop(T0[5] + 2.9, 700, 300, 0.3)
whoosh(T0[6], up=False)
pop(T0[6] + 0.1); pop(T0[6] + 0.35, 900, 450)
thud(T0[6] + 2.1, 0.9)                      # stempel
pop(T0[6] + 2.7, 650, 330, 0.25)
chime(T0[6] + 2.75, 0.14)

out = out[:int(SR * DUR)]
out = out / max(1e-9, np.max(np.abs(out))) * 0.85
pcm = (out * 32767).astype('<i2')
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok', sys.argv[1], round(len(out) / SR, 1), 'dtk')
