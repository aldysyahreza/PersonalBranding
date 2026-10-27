"""Satu perintah: rekaman voice over -> reels animatic siap tayang.

Pakai (dari folder proyek):
  python3 animatic/build_reel.py rekaman.m4a posts/reels-harga-ditawar.json out/reel

Langkah:
  1. vo_prep.py   jernihkan suara, buang napas/klik, atur jeda per kalimat, waktu per kata
  2. sfx-v3.py    musik latar + efek suara mengikuti waktu voice over
  3. campur       musik mengecil saat Anda bicara (sidechain), lalu -14 LUFS, puncak -1,5 dBTP
  4. cek tata letak (tests/t30_animatic_layout.js) dengan waktu voice over
  5. render MP4 1080x1920 30 fps
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TARGET_LUFS, TRUE_PEAK = -14.0, -1.5
LIMIT_DB = -2.5   # limiter lebih rendah dari target: kompresi AAC menambah lonjakan puncak ±1 dB


def run(cmd, **kw):
    print('→ ' + ' '.join(os.path.relpath(c, ROOT) if os.path.isabs(c) else c for c in cmd[:4]) + (' …' if len(cmd) > 4 else ''))
    return subprocess.run(cmd, check=True, **kw)


def loudness(path):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', path, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True)
    s = r.stderr[r.stderr.rfind('Summary'):]
    return float(re.search(r'I:\s+(-?[\d.]+) LUFS', s).group(1)), float(re.search(r'Peak:\s+(-?[\d.]+) dBFS', s).group(1))


def main(rec, script, outdir):
    os.makedirs(outdir, exist_ok=True)
    run([sys.executable, os.path.join(HERE, 'vo_prep.py'), rec, script, outdir])
    timing = os.path.join(outdir, 'timing.json')
    run([sys.executable, os.path.join(HERE, 'sfx-v3.py'), outdir, '--timing', timing])
    vo, mu, fx = (os.path.join(outdir, n) for n in ('vo_clean.wav', 'music.wav', 'fx.wav'))
    pre = os.path.join(outdir, '_mix.wav'); mix = os.path.join(outdir, 'mix.wav')
    # musik ±-30 LUFS di bawah suara, efek ±-24 LUFS. Dinormalkan di langkah terpisah: loudnorm di dalam graph
    # bersama asplit/sidechain membuat ffmpeg macet (saling tunggu buffer).
    lv = {}
    for name, src, tgt in (('m', mu, -30.0), ('f', fx, -24.0)):
        i, _ = loudness(src); lv[name] = os.path.join(outdir, '_%s.wav' % name)
        run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', src, '-af', 'volume=%.2fdB' % (tgt - i), lv[name]])
    graph = ('[0:a]asplit=2[v1][v2];[1:a][v1]sidechaincompress=threshold=0.015:ratio=8:attack=20:release=400[md];'
             '[v2][md][2:a]amix=inputs=3:normalize=0:duration=first[a]')
    run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', vo, '-i', lv['m'], '-i', lv['f'], '-filter_complex', graph, '-map', '[a]', '-ar', '48000', pre])
    for p in lv.values(): os.remove(p)
    i0, _ = loudness(pre)
    run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', pre, '-af',
         'volume=%.2fdB,alimiter=limit=%.4f:attack=3:release=60:level=disabled' % (TARGET_LUFS - i0, 10 ** (LIMIT_DB / 20)), '-ar', '48000', mix])
    os.remove(pre)
    i1, p1 = loudness(mix)
    print('   campuran: %.1f LUFS, puncak %.1f dBFS' % (i1, p1))
    run(['node', os.path.join(ROOT, 'tests', 't30_animatic_layout.js'), 'animatic-v3.html', timing])
    mp4 = os.path.join(outdir, 'reel.mp4')
    run(['node', os.path.join(HERE, 'render-animatic.js'), '--file', 'animatic-v3.html', '--beats', timing, '--audio', mix, '--stills', '1', '--out', mp4])
    print('✓ selesai: ' + os.path.relpath(mp4, os.getcwd()))


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print(__doc__); sys.exit(1)
    main(*sys.argv[1:4])
