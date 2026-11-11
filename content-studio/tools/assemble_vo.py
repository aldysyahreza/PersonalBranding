"""Rakit voice over per kalimat (hasil voiceover/generate_batch.ps1) menjadi vo_clean.wav + timing.json (format sama dengan vo_prep.py),
sehingga build_reel.py bisa memakainya tanpa menebak batas kalimat.
Pemakaian: python3 tools/assemble_vo.py <folder kalimat_*.wav> <naskah.kalimat.json> <posts/reels-xxx.json> <outdir>"""
import sys, os, json, glob, subprocess
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'animatic'))
import vo_prep as v
def main(wavdir, rows_json, post, outdir):
    os.makedirs(outdir, exist_ok=True)
    rows = json.load(open(rows_json, encoding='utf-8'))
    files = sorted(glob.glob(os.path.join(wavdir, 'kalimat_*.wav')))
    if len(files) != len(rows): raise SystemExit('Jumlah file (%d) tidak sama dengan jumlah kalimat (%d).' % (len(files), len(rows)))
    beats = [b['say'] for b in json.load(open(post, encoding='utf-8'))['reel']['beats']]
    out, t, words, rep = [np.zeros(int(v.PAUSE['awal'] * v.SR))], v.PAUSE['awal'], [], []
    last_beat_of = {}
    for r in rows: last_beat_of[r['beat']] = r['i']
    for k, (f, r) in enumerate(zip(files, rows)):
        tmp = os.path.join(outdir, '_k.wav')
        v.ff('-i', f, '-ac', '1', '-ar', str(v.SR), tmp)
        x = v.read_wav(tmp); os.remove(tmp)
        # potong keheningan di awal/akhir kalimat (ambang relatif)
        env = np.abs(x); thr = max(0.01, float(np.percentile(env, 99)) * 0.04)
        idx = np.where(env > thr)[0]
        a, b = (max(0, idx[0] - int(0.03 * v.SR)), min(len(x), idx[-1] + int(0.06 * v.SR))) if len(idx) else (0, len(x))
        p = x[a:b].copy(); nf = int(v.FADE * v.SR); p[:nf] *= np.linspace(0, 1, nf); p[-nf:] *= np.linspace(1, 0, nf)
        d = len(p) / v.SR
        ws = r['tampil'].split(); tot = sum(v.syllables(w) for w in ws) or 1; acc = 0
        for w in ws:
            words.append({'w': w, 't': round(t + d * acc / tot, 3), 'beat': r['beat']}); acc += v.syllables(w)
        out.append(p); t += d
        kind = 'akhir' if k == len(rows) - 1 else ('langkah' if last_beat_of[r['beat']] == r['i'] else 'kalimat')
        out.append(np.zeros(int(v.PAUSE[kind] * v.SR))); t += v.PAUSE[kind]
        rep.append('kalimat %02d  %.2f dtk  jeda %s  %s' % (r['i'], d, kind, r['tampil']))
    y = np.concatenate(out); total = len(y) / v.SR
    starts = []
    for bi in range(len(beats)):
        ws = [w for w in words if w['beat'] == bi]
        starts.append(max(0, ws[0]['t'] - 0.2) if ws else (starts[-1] if starts else 0))
    starts[0] = 0
    tl = {'duration': round(total, 3), 'denoise': 'suara klon (tanpa peredam bising)', 'pauses': v.PAUSE, 'beats': []}
    for bi in range(len(beats)):
        end = starts[bi + 1] if bi + 1 < len(beats) else total
        tl['beats'].append({'start': round(starts[bi], 3), 'dur': round(end - starts[bi], 3), 'say': beats[bi], 'words': [{'w': w['w'], 't': w['t']} for w in words if w['beat'] == bi]})
    # normalisasi volume ke -16 LUFS lewat ffmpeg (sama seperti rekaman asli)
    raw = os.path.join(outdir, '_vo_raw.wav'); v.write_wav(raw, y)
    v.ff('-i', raw, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', str(v.SR), os.path.join(outdir, 'vo_clean.wav')); os.remove(raw)
    json.dump(tl, open(os.path.join(outdir, 'timing.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(os.path.join(outdir, 'laporan.txt'), 'w', encoding='utf-8').write('Suara klon, %d kalimat, %.1f dtk\n' % (len(rows), total) + '\n'.join(rep) + '\n')
    print('✓ %.1f dtk → %s/vo_clean.wav + timing.json' % (total, outdir))
if __name__ == '__main__': main(*sys.argv[1:5])
