"""Siapkan voice over untuk animatic: jernihkan suara, buang napas/klik, atur jeda per kalimat, keluarkan waktu per kata.

Pakai:
  python3 animatic/vo_prep.py rekaman.m4a posts/reels-harga-ditawar.json out/vo [auto|akhir|awal]
  (kalimat yang Anda ulang untuk opsi intonasi dikenali otomatis; auto = pilih nada paling hidup, akhir/awal = pilih take terakhir/pertama)
Hasil di folder out/vo:
  vo_clean.wav   suara bersih dengan jeda rapi (-16 LUFS, puncak -1,5 dBTP)
  timing.json    durasi tiap langkah + waktu tiap kata (untuk animatic dan caption)
  laporan.txt    segmen yang ditemukan, kalimat yang dicocokkan, dan jeda baru

Butuh: ffmpeg dan numpy. Peredam bising RNNoise memakai model animatic/models/sh.rnnn
(diunduh otomatis bila belum ada); bila gagal, dipakai afftdn bawaan ffmpeg.
"""
import json, os, re, subprocess, sys, urllib.request, wave
import numpy as np

SR = 48000
PAUSE = {'koma': 0.18, 'kalimat': 0.35, 'langkah': 0.55, 'awal': 0.25, 'akhir': 0.6}
PAD_PRE, PAD_POST, FADE = 0.05, 0.09, 0.012
BOUND = {'koma': 0.1, 'kalimat': 0.6, 'langkah': 3.0}  # biaya menggabungkan frasa melewati batas ini
HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = os.path.join(HERE, 'models', 'sh.rnnn')
MODEL_URL = 'https://raw.githubusercontent.com/GregorR/rnnoise-models/master/somnolent-hogwash-2018-09-01/sh.rnnn'


def ff(*args):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *args], check=True)


def read_wav(p):
    with wave.open(p) as w:
        return np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float64) / 32768


def write_wav(p, x):
    with wave.open(p, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype('<i2').tobytes())


def denoise_filter():
    if not os.path.exists(MODEL):
        try:
            os.makedirs(os.path.dirname(MODEL), exist_ok=True)
            urllib.request.urlretrieve(MODEL_URL, MODEL)
        except Exception:
            pass
    if os.path.exists(MODEL) and open(MODEL, 'rb').read(14) == b'rnnoise-nu mod':
        return 'arnndn=m=' + MODEL.replace('\\', '/').replace(':', '\\:') + ':mix=0.85', 'RNNoise'
    return 'afftdn=nr=12:nf=-50:tn=1', 'afftdn'


def syllables(s):
    return max(1, len(re.findall(r'[aiueo]+', s.lower())))


def speech_segments(x, thr_db=-38, min_sil=0.2, min_seg=0.2):
    """Segmen bicara dari energi per 10 ms; buang potongan yang terlalu pelan atau tidak bersuara (napas, klik)."""
    hop = int(0.01 * SR)
    fr = x[:len(x) // hop * hop].reshape(-1, hop)
    db = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9)
    on = db > thr_db
    segs, i, n = [], 0, len(on)
    while i < n:
        if on[i]:
            j = i
            while j < n and (on[j] or (j + 1 < n and not on[j] and np.any(on[j:j + int(min_sil / 0.01)]))):
                j += 1
            segs.append([i * 0.01, j * 0.01]); i = j
        else:
            i += 1
    out = []
    for a, b in segs:
        s = x[int(a * SR):int(b * SR)]
        rms = 20 * np.log10(np.sqrt((s ** 2).mean()) + 1e-9)
        if b - a < min_seg or rms < -40:
            continue
        out.append([a, b, rms])
    return out


def contour(x, a, b):
    """Arah nada di ujung potongan: +1 naik (pertanyaan), -1 turun (pernyataan), 0 tidak jelas. F0 lewat autokorelasi."""
    s = x[int(a * SR):int(b * SR)]; n = int(0.04 * SR); hop = int(0.01 * SR); ps = []
    lo, hi = int(SR / 350), int(SR / 70)
    for i in range(0, len(s) - n, hop):
        f = s[i:i + n] * np.hanning(n)
        if np.sqrt(np.mean(f ** 2)) < 0.01: continue
        ac = np.correlate(f, f, 'full')[n - 1:]
        k = lo + int(np.argmax(ac[lo:hi]))
        if ac[0] > 0 and ac[k] / ac[0] > 0.5: ps.append(SR / k)
    if len(ps) < 4: return 0
    q = max(2, len(ps) // 4); p0, p1 = np.median(ps[:q]), np.median(ps[-q:])
    return 1 if p1 > p0 * 1.08 else (-1 if p1 < p0 * 0.92 else 0)



def f0track(x, a, b):
    s = x[int(a * SR):int(b * SR)]; n = int(0.04 * SR); hop = int(0.01 * SR); ps = []
    lo, hi = int(SR / 350), int(SR / 70)
    for i in range(0, len(s) - n, hop):
        f = s[i:i + n] * np.hanning(n)
        if np.sqrt(np.mean(f ** 2)) < 0.01: continue
        ac = np.correlate(f, f, 'full')[n - 1:]
        k = lo + int(np.argmax(ac[lo:hi]))
        if ac[0] > 0 and ac[k] / ac[0] > 0.5: ps.append(SR / k)
    return ps


def _mel_fb(n_mels=26, n_fft=512, sr=16000):
    f = lambda m: 700 * (10 ** (m / 2595) - 1); m = lambda f_: 2595 * np.log10(1 + f_ / 700)
    pts = f(np.linspace(m(60), m(7600), n_mels + 2)); bins = np.floor((n_fft + 1) * pts / sr).astype(int)
    fb = np.zeros((n_mels, n_fft // 2 + 1))
    for i in range(1, n_mels + 1):
        a, b, c = bins[i - 1], bins[i], bins[i + 1]
        for k in range(a, b): fb[i - 1, k] = (k - a) / max(1, b - a)
        for k in range(b, c): fb[i - 1, k] = (c - k) / max(1, c - b)
    return fb


def _mfcc(sig, fb, dm):
    y = np.interp(np.arange(0, len(sig), SR / 16000), np.arange(len(sig)), sig)
    fr = [np.log(fb @ (np.abs(np.fft.rfft(y[i:i + 400] * np.hamming(400), 512)) ** 2) + 1e-8) for i in range(0, len(y) - 400, 160)]
    c = (dm @ np.array(fr).T).T[:, 1:13]
    return c - c.mean(0)


def _dtw(a, b):
    n, m = len(a), len(b); C = np.sqrt(((a[:, None, :] - b[None, :, :]) ** 2).sum(2))
    A = np.full((n + 1, m + 1), 1e9); A[0, 0] = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1): A[i, j] = C[i - 1, j - 1] + min(A[i - 1, j], A[i, j - 1], A[i - 1, j - 1])
    return A[n, m] / (n + m)


def retakes(x, segs, mode='auto', window=9, ratio=0.7):
    """Deteksi pengulangan (take ulang) tanpa ASR: potongan yang bunyinya sama (jarak MFCC+DTW jauh di bawah median).
    Potongan berurutan yang diulang berurutan dianggap satu blok. Dari tiap blok dipilih satu take:
    'akhir' = yang terakhir, 'awal' = yang pertama, 'auto' = nada paling hidup (variasi F0 terbesar; selisih < 10% -> yang terakhir).
    Mengembalikan (indeks potongan yang dibuang, catatan)."""
    fb = _mel_fb(); dm = np.cos(np.pi / 26 * (np.arange(26) + .5)[None, :] * np.arange(13)[:, None])
    M = [_mfcc(x[int(a * SR):int(b * SR)], fb, dm) for a, b, _ in segs]; n = len(segs); d = {}
    for i in range(n):
        for j in range(i + 1, min(n, i + window)):
            r = (segs[i][1] - segs[i][0]) / (segs[j][1] - segs[j][0])
            if 0.6 < r < 1.67: d[(i, j)] = _dtw(M[i], M[j])
    if not d: return set(), []
    med = float(np.median(list(d.values()))); dup = sorted(k for k, v in d.items() if v < ratio * med)
    done, blocks = set(), []
    for (i, j) in dup:
        if (i, j) in done: continue
        L = 1
        while (i + L, j + L) in set(dup) and i + L < j: L += 1
        for k in range(L): done.add((i + k, j + k))
        blocks.append((i, j, L))
    drop, notes = set(), []
    for i, j, L in blocks:
        def spread(r):
            ps = [p for k in r for p in f0track(x, segs[k][0], segs[k][1])]
            return float(np.std(np.log(ps))) if len(ps) > 4 else 0.0
        t1, t2 = list(range(i, i + L)), list(range(j, j + L)); s1, s2 = spread(t1), spread(t2)
        pick2 = True if mode == 'akhir' else (False if mode == 'awal' else (s1 > s2 * 1.10))
        pick2 = (not pick2) if mode == 'auto' else pick2
        if mode == 'auto': pick2 = not (s1 > s2 * 1.10)
        keep, lose = (t2, t1) if pick2 else (t1, t2)
        drop.update(lose)
        drop.update(range(i + L, j))   # potongan di antara dua take = take yang dibatalkan (awal kalimat yang tidak jadi)
        notes.append('Pengulangan: %.2f-%.2f dan %.2f-%.2f (%d potongan; %d potongan batal di antaranya), variasi nada %.3f vs %.3f → dipakai take %s'
                     % (segs[t1[0]][0], segs[t1[-1]][1], segs[t2[0]][0], segs[t2[-1]][1], L, max(0, j - i - L), s1, s2, 'ke-2' if pick2 else 'ke-1'))
    return drop, notes


def phrases(beats):
    """Naskah dipecah jadi frasa (di koma/titik/tanya), diberi jenis jeda sesudahnya."""
    out = []
    for bi, say in enumerate(beats):
        parts = [p.strip() for p in re.findall(r'[^,.?!]+[,.?!]*["”]?', say.replace('“', '').replace('”', '')) if p.strip()]
        for k, p in enumerate(parts):
            last = k == len(parts) - 1
            kind = 'langkah' if last else ('kalimat' if re.search(r'[.?!]$', p) else 'koma')
            out.append({'beat': bi, 'text': p, 'syl': syllables(p), 'after': kind})
    return out


def align(segs, phr, tone, maxa=3, maxb=3):
    """Pasangkan potongan bicara dengan frasa naskah (dynamic programming). Satu unit = 1-3 potongan berurutan
    dengan 1-3 frasa berurutan; dipilih susunan yang kecepatan bicaranya (suku kata/detik) paling konsisten."""
    n, m = len(segs), len(phr)
    dur = [b - a for a, b, _ in segs]; syl = [p['syl'] for p in phr]
    r0 = np.log(sum(syl) / sum(dur))
    INF = 1e18; dp = [[INF] * (m + 1) for _ in range(n + 1)]; bk = [[None] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            for a in range(1, min(maxa, i) + 1):
                for b in range(1, min(maxb, j) + 1):
                    if dp[i - a][j - b] >= INF: continue
                    d = sum(dur[i - a:i]); s_ = sum(syl[j - b:j])
                    gaps = [segs[k + 1][0] - segs[k][1] for k in range(i - a, i - 1)]
                    seg_pen = sum(0.15 * (1 + g / 0.3) for g in gaps)          # memecah satu frasa di jeda panjang itu mahal
                    phr_pen = sum(BOUND[phr[k]['after']] for k in range(j - b, j - 1))  # menggabung melewati akhir kalimat/langkah mahal
                    end = phr[j - 1]['text'].rstrip('"”')[-1:]                    # intonasi harus cocok dengan tanda baca
                    tone_pen = (0.8 if end == '?' and tone[i - 1] != 1 else 0) + (0.3 if end == '.' and tone[i - 1] == 1 else 0)
                    c = dp[i - a][j - b] + (np.log(s_ / d) - r0) ** 2 * (a + b) + seg_pen + phr_pen + tone_pen
                    if c < dp[i][j]: dp[i][j] = c; bk[i][j] = (a, b)
    if dp[n][m] >= INF: raise SystemExit('Potongan bicara tidak cocok dengan naskah. Cek apakah rekaman sesuai naskah.')
    units, i, j = [], n, m
    while i > 0:
        a, b = bk[i][j]; units.append((list(range(i - a, i)), list(range(j - b, j)))); i -= a; j -= b
    return units[::-1]


def main(src, script, outdir, take='auto'):
    os.makedirs(outdir, exist_ok=True)
    post = json.load(open(script, encoding='utf-8'))
    beats = [b['say'] for b in post['reel']['beats']] if 'reel' in post else [b['say'] for b in post['beats']]
    raw = os.path.join(outdir, '_raw.wav'); clean = os.path.join(outdir, '_clean.wav')
    ff('-i', src, '-ac', '1', '-ar', str(SR), raw)
    xr = read_wav(raw); hop = int(0.02 * SR); fr = xr[:len(xr) // hop * hop].reshape(-1, hop)
    lantai = float(np.percentile(20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9), 20))   # lantai bising: 20% bingkai terpelan
    if lantai < -55:
        # rekaman sudah bersih (mis. voice note HP): peredam bising justru menimbulkan suara "robot" (terukur: jarak spektrum 10 dB dari asli
        # dan HF kasar), jadi dilewati. Hanya filter dasar + kompresi lembut.
        dn_name = 'tidak dipakai (rekaman bersih, lantai %.0f dB)' % lantai
        chain = ','.join(['highpass=f=70', 'lowpass=f=15000',
                          'acompressor=threshold=-24dB:ratio=2:attack=15:release=160:makeup=1', 'loudnorm=I=-16:TP=-1.5:LRA=11'])
    else:
        dn, dn_name = denoise_filter(); dn_name += ' (lantai bising %.0f dB)' % lantai
        # catatan: filter deesser bawaan ffmpeg menimbulkan artefak >16 kHz (terukur), jadi desis dijinakkan dengan EQ statis
        chain = ','.join(['highpass=f=80', 'lowpass=f=15000', dn,
                          'equalizer=f=6500:t=q:w=1.4:g=-2.5', 'equalizer=f=180:t=q:w=1:g=-1.5',
                          'acompressor=threshold=-21dB:ratio=3:attack=6:release=90:makeup=2',
                          'loudnorm=I=-16:TP=-1.5:LRA=7', 'lowpass=f=14500'])
    ff('-i', raw, '-af', chain, '-ar', str(SR), clean)
    x = read_wav(clean)
    segs = speech_segments(x)
    # napas / klik / desis bibir: pelan (jauh di bawah ucapan lain) dan hampir tanpa nada. Dibuang supaya tidak ikut terputar ("peceh").
    med = float(np.median([r for _, _, r in segs])); keep = []
    for a_, b_, r_ in segs:
        voiced = len(f0track(x, a_, b_)) / max(1, int((b_ - a_) / 0.01) - 3)
        if voiced < 0.2 and r_ < med - 10: continue
        keep.append([a_, b_, r_])
    n_napas = len(segs) - len(keep); segs = keep
    drop, retake_notes = retakes(x, segs, take)
    segs = [sg for k, sg in enumerate(segs) if k not in drop]
    phr = phrases(beats)
    tone = [contour(x, a, b) for a, b, _ in segs]
    units = align(segs, phr, tone)

    # susun ulang: potongan bicara + jeda baku (antar unit) / jeda alami pendek (di dalam unit)
    out, t, words, rep = [np.zeros(int(PAUSE['awal'] * SR))], PAUSE['awal'], [], []
    def cut(si):
        a, b, _ = segs[si]; a2 = max(0, a - PAD_PRE); b2 = min(len(x) / SR, b + PAD_POST)
        if si: a2 = max(a2, (segs[si - 1][1] + a) / 2)
        if si < len(segs) - 1: b2 = min(b2, (b + segs[si + 1][0]) / 2)
        p = x[int(a2 * SR):int(b2 * SR)].copy(); nf = int(FADE * SR); p[:nf] *= np.linspace(0, 1, nf); p[-nf:] *= np.linspace(1, 0, nf)
        return p, a - a2, b - a
    for ui, (sidx, pidx) in enumerate(units):
        u0 = t; spans = []
        for k, si in enumerate(sidx):
            p, lead, d = cut(si); spans.append((t + lead, t + lead + d)); out.append(p); t += len(p) / SR
            if k < len(sidx) - 1:
                g = min(0.12, segs[sidx[k + 1]][0] - segs[si][1]); out.append(np.zeros(int(g * SR))); t += g
        # kata dibagi menurut suku kata sepanjang waktu bicara unit (jeda di dalam unit dilewati)
        ws = [(w, phr[j]['beat']) for j in pidx for w in phr[j]['text'].split()]
        tot = sum(syllables(w) for w, _ in ws); speech = sum(b - a for a, b in spans); acc = 0
        for w, bi in ws:
            pos = speech * acc / tot
            for a, b in spans:
                if pos <= b - a: tw = a + pos; break
                pos -= b - a
            else: tw = spans[-1][1]
            words.append({'w': w, 't': round(tw, 3), 'beat': bi}); acc += syllables(w)
        kind = phr[pidx[-1]]['after'] if ui < len(units) - 1 else 'akhir'
        out.append(np.zeros(int(PAUSE[kind] * SR))); t += PAUSE[kind]
        sp_dur = sum(segs[k][1] - segs[k][0] for k in sidx); rate = sum(phr[j]['syl'] for j in pidx) / max(sp_dur, 0.01)
        flag = '' if 3.2 <= rate <= 8.5 else '   ⚠ tempo %.1f suku kata/dtk tidak wajar: cek apakah potongan cocok dengan kalimat' % rate
        rep.append('%5.2f-%5.2f → %5.2f-%5.2f  jeda %.2f %-8s %s%s' % (segs[sidx[0]][0], segs[sidx[-1]][1], u0, t - PAUSE[kind], PAUSE[kind], kind, ' '.join(phr[j]['text'] for j in pidx), flag))
    y = np.concatenate(out)
    # langkah: mulai = awal bicara langkah itu (dikurangi 0,2 dtk), berakhir saat langkah berikutnya mulai
    starts = []
    for bi in range(len(beats)):
        ws = [w for w in words if w['beat'] == bi]
        starts.append(max(0, ws[0]['t'] - 0.2) if ws else (starts[-1] if starts else 0))
    starts[0] = 0
    total = len(y) / SR
    tl = {'duration': round(total, 3), 'denoise': dn_name, 'pauses': PAUSE, 'beats': []}
    for bi in range(len(beats)):
        end = starts[bi + 1] if bi + 1 < len(beats) else total
        tl['beats'].append({'start': round(starts[bi], 3), 'dur': round(end - starts[bi], 3), 'say': beats[bi],
                            'words': [{'w': w['w'], 't': w['t']} for w in words if w['beat'] == bi]})
    write_wav(os.path.join(outdir, 'vo_clean.wav'), y)
    json.dump(tl, open(os.path.join(outdir, 'timing.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    raw_dur = len(read_wav(raw)) / SR
    lines = ['Peredam bising: ' + dn_name, 'Durasi: %.1f dtk → %.1f dtk' % (raw_dur, total), 'Segmen bicara: %d (dibuang: %d pengulangan, %d napas/klik)' % (len(segs), len(drop), n_napas), ''] + retake_notes + [''] + rep + ['']
    lines += ['Langkah %d: mulai %.2f, %.2f dtk' % (i + 1, b['start'], b['dur']) for i, b in enumerate(tl['beats'])]
    open(os.path.join(outdir, 'laporan.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    for f in (raw, clean): os.remove(f)
    print('\n'.join(lines))


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print(__doc__); sys.exit(1)
    main(*sys.argv[1:5])
