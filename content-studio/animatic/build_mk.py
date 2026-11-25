"""Rakit reels Motion Kit: musik + efek dari events.json, campur dengan vo_clean.wav (ducking, -14 LUFS), render HTML.
Pakai: python3 animatic/build_mk.py out/reel16 mk-parkir.html"""
import json, os, sys, wave, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_reel import loudness, run, TARGET_LUFS, LIMIT_DB
SR = 48000
out_dir, html = sys.argv[1], sys.argv[2]
E = json.load(open(os.path.join(out_dir, 'events.json')))
DUR = E['duration']; n = int(SR * (DUR + 1))
fx = np.zeros(n); mus = np.zeros(n); rng = np.random.default_rng(7)
def lp(x, c):
    y = np.zeros_like(x); s = 0.0; k = 1 - np.exp(-2 * np.pi * c / SR)
    for i in range(len(x)): s += k * (x[i] - s); y[i] = s
    return y
def add(buf, t, sig, g):
    i = int(t * SR)
    if i < 0: sig = sig[-i:]; i = 0
    if i >= len(buf): return
    sig = sig[:len(buf) - i]; buf[i:i + len(sig)] += sig * g
def env(m, a, r): t = np.arange(m) / SR; return np.minimum(1, t / a) * np.exp(-t / r)
def paper(t, g=.22):   # kertas geser: desis pita sempit, lembut
    m = int(.32 * SR); x = lp(rng.standard_normal(m), 2400) - lp(rng.standard_normal(m) * 0, 1); add(fx, t - .05, (x - lp(x, 600)) * np.sin(np.linspace(0, np.pi, m)) ** 2, g)
def pop(t, g=.2):
    m = int(.09 * SR); ph = np.cumsum(np.linspace(760, 360, m)) / SR * 2 * np.pi; add(fx, t, np.sin(ph) * env(m, .002, .03), g)
def tick(t, g=.1):   # ketukan kayu lembut (sebelumnya klik 1,7 kHz terdengar seperti glitch)
    m = int(.06 * SR); tt = np.arange(m) / SR; add(fx, t, lp(np.sin(2 * np.pi * 820 * tt) * env(m, .003, .018), 2500), g)
def scratch(t, d=.35, g=.16):   # goresan spidol
    m = int(d * SR); x = rng.standard_normal(m); y = lp(x, 2200) - lp(x, 700); add(fx, t, y * (.6 + .4 * np.sin(np.linspace(0, d * 2 * np.pi * 18, m))) * np.sin(np.linspace(0, np.pi, m)), g)
def stamp(t, g=.55):   # dentum cap (pendek, tanpa boom)
    m = int(.18 * SR); tt = np.arange(m) / SR; add(fx, t, np.sin(2 * np.pi * (180 - 80 * tt / .18) * tt) * np.exp(-tt / .04) + .25 * rng.standard_normal(m) * np.exp(-tt / .01), g)
def chime(t, g=.18):
    for k, f in enumerate([880, 1108.7, 1318.5]):
        m = int(.6 * SR); tt = np.arange(m) / SR; add(fx, t + k * .06, np.sin(2 * np.pi * f * tt) * np.exp(-tt / .18), g * .6)
def splash(t, g=.3):   # celup air: desis basah + beberapa gelembung
    m = int(.45 * SR); x = rng.standard_normal(m); y = (lp(x, 1800) - lp(x, 300)) * np.exp(-np.arange(m) / SR / .12); add(fx, t, y, g)
    for k in range(4):
        q = int(.05 * SR); f0 = 500 + 180 * k; ph = np.cumsum(np.linspace(f0, f0 * 1.8, q)) / SR * 2 * np.pi; add(fx, t + .08 + k * .07, np.sin(ph) * env(q, .002, .015), g * .5)
K = {'splash': splash, 'slide': paper, 'sweep': lambda t: paper(t, .3), 'pop': pop, 'tick': tick, 'scratch': scratch, 'draw': lambda t: scratch(t, .6, .1), 'stamp': stamp, 'chime': chime}
for t, k in E['events']: K[k](t)
# musik: pad hangat (piano-ish) 84 bpm, akor I-vi-IV-V, fade in/out
tt = np.arange(n) / SR; DARK = os.environ.get('MK_MOOD') == 'dark'
bar = 60 / (64 if DARK else 84) * 4; DECAY = 2.6 if DARK else 1.6
ch = [[220.0, 261.6, 329.6], [174.6, 220.0, 261.6], [130.8, 164.8, 196.0], [146.8, 174.6, 220.0]] if DARK else [[261.6, 329.6, 392.0], [220.0, 261.6, 329.6], [174.6, 220.0, 261.6], [196.0, 246.9, 293.7]]
for i in range(int(DUR / bar) + 2):
    a, b = int(i * bar * SR), min(n, int((i + 1) * bar * SR))
    if a >= n: break
    s = tt[a:b] - i * bar
    for j, f in enumerate(ch[i % 4]):   # tiga not dipetik berurutan, meluruh pelan
        on = j * bar / 4; e = np.where(s >= on, np.exp(-(s - on) / DECAY) * np.minimum(1, np.maximum(0, s - on) / .015), 0)
        mus[a:b] += (np.sin(2 * np.pi * f * tt[a:b]) + .25 * np.sin(4 * np.pi * f * tt[a:b])) * e * .3
    mus[a:b] += np.sin(2 * np.pi * ch[i % 4][0] / 2 * tt[a:b]) * np.minimum(1, s / .5) * np.minimum(1, (bar - s) / .5) * .12
if DARK: mus += (np.sin(2 * np.pi * 55 * tt) * .18 + np.sin(2 * np.pi * 110 * tt) * .06) * (.7 + .3 * np.sin(2 * np.pi * tt / 9))
mus *= np.minimum(1, tt / 1.5) * np.minimum(1, np.maximum(0, DUR + .5 - tt) / 1.5)
def save(p, x, peak):
    x = x[:int(SR * DUR)]; x = x / max(1e-9, np.max(np.abs(x))) * peak
    with wave.open(p, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype('<i2').tobytes())
save(os.path.join(out_dir, 'music.wav'), mus, .5); save(os.path.join(out_dir, 'fx.wav'), fx, .8)
vo, mu, fxp = (os.path.join(out_dir, x) for x in ('vo_clean.wav', 'music.wav', 'fx.wav'))
lv = {}
for name, src, tgt in (('m', mu, -30.0), ('f', fxp, -28.0)):
    i, _ = loudness(src); lv[name] = os.path.join(out_dir, '_%s.wav' % name)
    run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', src, '-af', 'volume=%.2fdB' % (tgt - i), lv[name]])
pre = os.path.join(out_dir, '_mix.wav'); mix = os.path.join(out_dir, 'mix.wav')
graph = ('[0:a]asplit=2[v1][v2];[1:a][v1]sidechaincompress=threshold=0.015:ratio=8:attack=20:release=400[md];[v2][md][2:a]amix=inputs=3:normalize=0:duration=first[a]')
run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', vo, '-i', lv['m'], '-i', lv['f'], '-filter_complex', graph, '-map', '[a]', '-ar', '48000', pre])
for p in lv.values(): os.remove(p)
i0, _ = loudness(pre)
run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', pre, '-af', 'volume=%.2fdB,alimiter=limit=%.4f:attack=3:release=60:level=disabled' % (TARGET_LUFS - i0, 10 ** (LIMIT_DB / 20)), '-ar', '48000', mix])
os.remove(pre); i1, p1 = loudness(mix); print('   campuran: %.1f LUFS, puncak %.1f dBFS' % (i1, p1))
run(['node', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'render-animatic.js'), '--file', html, '--audio', mix, '--out', os.path.join(out_dir, 'reel.mp4')])
