"""Satu perintah: rekaman voice over -> reels animatic siap tayang.

Pakai (dari folder proyek):
  python3 animatic/build_reel.py rekaman.m4a posts/reels-harga-ditawar.json out/reel [v3|omzet|arah|pillar]

Langkah:
  1. vo_prep.py   jernihkan suara, buang napas/klik, atur jeda per kalimat, waktu per kata
  2. sfx-*.py     musik latar + efek suara mengikuti waktu voice over
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


def to_scenes(timing_path, anchors_path, out_path):
    """Babak narasi (HRIRC, dari vo_prep) -> adegan visual animatic. Tiap adegan mulai pada kata pembukanya
    (anchors 'scenes'); kata-kata ikut adegan tempat ia diucapkan."""
    import json
    tl = json.load(open(timing_path, encoding='utf-8')); an = json.load(open(anchors_path, encoding='utf-8'))
    sc = an.get('scenes')
    if not sc: return timing_path
    nrm = lambda s: ''.join(c for c in s.lower() if c.isalnum())
    words, beat_of = [], []
    for bi, b in enumerate(tl['beats']):
        for w in b['words']: words.append(w); beat_of.append(bi)
    starts, k = [], 0
    for s in sc:   # kata pembuka dicari hanya di dalam babak HRIRC adegan itu (chap), supaya "harga." di babak lain tidak tertangkap
        bi = s['chap'] - 1
        while k < len(words) and not (beat_of[k] == bi and nrm(words[k]['w']).startswith(s['start'])): k += 1
        if k >= len(words): raise SystemExit('Kata pembuka adegan "%s" tidak ditemukan di babak %d naskah' % (s['start'], s['chap']))
        starts.append(k); k += 1
    out = []
    for i, s in enumerate(sc):
        a = starts[i]; b = starts[i + 1] if i + 1 < len(sc) else len(words)
        t0 = 0.0 if i == 0 else max(0.0, words[a]['t'] - 0.2)
        out.append({'start': round(t0, 3), 'name': s['act'], 'chap': s['chap'], 'words': words[a:b]})
    for i, s in enumerate(out):
        end = out[i + 1]['start'] if i + 1 < len(out) else tl['duration']
        s['dur'] = round(end - s['start'], 3)
    tl2 = dict(tl, beats=out)
    json.dump(tl2, open(out_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return out_path


SETS = {'v3': ('animatic-v3.html', 'anchors-v3.json', 'sfx-v3.py'),
        'omzet': ('animatic-omzet.html', 'anchors-omzet.json', 'sfx-omzet.py'),
        'arah': ('animatic-arah.html', 'anchors-arah.json', 'sfx-arah.py'),
        'pillar': ('animatic-pillar.html', 'anchors-pillar.json', 'sfx-pillar.py')}


def main(rec, script, outdir, setname='v3', take='auto'):
    html, anchors, sfx = SETS[setname]
    os.makedirs(outdir, exist_ok=True)
    run([sys.executable, os.path.join(HERE, 'vo_prep.py'), rec, script, outdir, take])
    timing = to_scenes(os.path.join(outdir, 'timing.json'), os.path.join(HERE, anchors), os.path.join(outdir, 'timing_scenes.json'))
    run([sys.executable, os.path.join(HERE, sfx), outdir, '--timing', timing])
    vo, mu, fx = (os.path.join(outdir, n) for n in ('vo_clean.wav', 'music.wav', 'fx.wav'))
    pre = os.path.join(outdir, '_mix.wav'); mix = os.path.join(outdir, 'mix.wav')
    # musik ±-30 LUFS di bawah suara, efek ±-28 LUFS. Dinormalkan di langkah terpisah: loudnorm di dalam graph
    # bersama asplit/sidechain membuat ffmpeg macet (saling tunggu buffer).
    lv = {}
    for name, src, tgt in (('m', mu, -30.0), ('f', fx, -28.0)):
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
    run(['node', os.path.join(ROOT, 'tests', 't30_animatic_layout.js'), html, timing])
    mp4 = os.path.join(outdir, 'reel.mp4')
    run(['node', os.path.join(HERE, 'render-animatic.js'), '--file', html, '--beats', timing, '--audio', mix, '--stills', '1', '--out', mp4])
    print('✓ selesai: ' + os.path.relpath(mp4, os.getcwd()))


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print(__doc__); sys.exit(1)
    main(*sys.argv[1:6])
