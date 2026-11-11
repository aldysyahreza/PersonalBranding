"""Ekspor naskah suara dari posts/<reels>.json untuk pembaca suara klon (voiceover/).
Pemakaian: python3 tools/export_naskah.py posts/reels-xxx.json naskah/xxx
Menulis: xxx.txt (utuh), xxx.kalimat.txt (satu kalimat per baris, sudah dinormalkan ejaannya untuk dibaca), xxx.kalimat.json (peta baris -> babak + teks layar)."""
import json, re, sys, os
SATUAN = ['nol', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh', 'delapan', 'sembilan', 'sepuluh', 'sebelas']
def terbilang(n):
    if n < 12: return SATUAN[n]
    if n < 20: return terbilang(n - 10) + ' belas'
    if n < 100: return terbilang(n // 10) + ' puluh' + (' ' + terbilang(n % 10) if n % 10 else '')
    if n < 200: return 'seratus' + (' ' + terbilang(n - 100) if n > 100 else '')
    if n < 1000: return terbilang(n // 100) + ' ratus' + (' ' + terbilang(n % 100) if n % 100 else '')
    if n < 2000: return 'seribu' + (' ' + terbilang(n - 1000) if n > 1000 else '')
    if n < 1000000: return terbilang(n // 1000) + ' ribu' + (' ' + terbilang(n % 1000) if n % 1000 else '')
    return str(n)
def normal(t, ejaan):
    t = t.replace('“', '').replace('”', '').replace('*', '')
    t = re.sub(r'(\d+)\s*-\s*(\d+)%', lambda m: terbilang(int(m.group(1))) + ' sampai ' + terbilang(int(m.group(2))) + ' persen', t)
    t = re.sub(r'(\d+)%', lambda m: terbilang(int(m.group(1))) + ' persen', t)
    t = re.sub(r'US\$\s*(\d+)', lambda m: terbilang(int(m.group(1))) + ' dolar', t)
    t = re.sub(r'\b(\d{1,6})\b', lambda m: terbilang(int(m.group(1))), t)
    t = t.replace('+', ' lebih').replace('-nya', ' nya')
    for k, v in ejaan.items(): t = re.sub(r'\b%s\b' % re.escape(k), v, t)
    return re.sub(r'\s+', ' ', t).strip()
def main(post, base):
    p = json.load(open(post, encoding='utf-8'))
    beats = [b['say'] for b in p['reel']['beats']] if 'reel' in p else [b['say'] for b in p['beats']]
    ejaan = {k: v for k, v in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'voiceover', 'ejaan.json'), encoding='utf-8')).items() if not k.startswith('_')}
    os.makedirs(os.path.dirname(base) or '.', exist_ok=True)
    rows = []
    for bi, say in enumerate(beats):
        for s in re.findall(r'[^.?!]+[.?!]+["”]?|[^.?!]+$', say.replace('“', '').replace('”', '')):
            s = s.strip()
            if s: rows.append({'beat': bi, 'tampil': s, 'baca': normal(s, ejaan)})
    for i, r in enumerate(rows, 1): r['i'] = i
    open(base + '.txt', 'w', encoding='utf-8').write('\n\n'.join(' '.join(r['baca'] for r in rows if r['beat'] == bi) for bi in range(len(beats)) if any(r['beat'] == bi for r in rows)) + '\n')
    open(base + '.kalimat.txt', 'w', encoding='utf-8').write('\n'.join(r['baca'] for r in rows) + '\n')
    json.dump(rows, open(base + '.kalimat.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('%d kalimat -> %s.kalimat.txt' % (len(rows), base))
if __name__ == '__main__': main(*sys.argv[1:3])
