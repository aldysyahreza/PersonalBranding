// Langkah 2 — Transkrip: buat (lokal/cloud/manual/impor), lalu koreksi teks & timestamp.
import { h, toast, consentDialog, badge, num } from '../ui.js';
import { api } from '../api.js';
import { store, edit, setProject } from '../store.js';
import { go, runJob } from '../app.js';
import { fmtTime, syncSegmentWords, makeSegment, tokenize, r3 } from '../../shared/core.js';

const TIMING = { asr: ['Timestamp kata asli', 'ok'], estimated: ['Waktu kata diestimasi', 'warn'], imported: ['Diimpor (kata diestimasi)', 'warn'], manual: ['Manual', ''] };

export function renderTranscript(main) {
  const p = store.project;
  main.append(h('div', { class: 'view-head' }, h('h1', {}, 'Transkrip'), h('p', { class: 'muted' }, 'Subtitle diambil dari transkrip ini. Koreksi kata dan waktu sebelum edit diterapkan — aplikasi tidak pernah menulis ulang ucapan Anda.')));
  if (!p.source) {
    main.append(h('div', { class: 'panel' }, h('p', {}, 'Impor video terlebih dahulu.'), h('button', { class: 'btn', onclick: () => go('projects') }, '← Ke Proyek')));
    return;
  }
  const video = h('video', { src: `/api/projects/${p.id}/media/source`, controls: true, preload: 'metadata', class: 'side-video' });
  const layout = h('div', { class: 'split' }, h('div', { class: 'split-main' }), h('aside', { class: 'split-side' }, h('div', { class: 'sticky' }, video, h('p', { class: 'muted small' }, 'Klik ▶ pada segmen untuk memutar bagian itu.'))));
  main.append(layout);
  const col = layout.firstChild;
  col.append(providersPanel(p));
  if (p.transcript?.segments?.length) col.append(segmentsPanel(p, video));
}

function providersPanel(p) {
  const st = store.status.transcription;
  const job = store.jobs[p.id];
  const panel = h('section', { class: 'panel' }, h('h2', {}, p.transcript ? 'Buat ulang transkrip' : 'Buat transkrip'));
  if (p.transcript) panel.append(h('div', { class: 'alert warn' }, 'Membuat transkrip baru akan mengganti transkrip saat ini (bisa dibatalkan dengan Urungkan selama sesi ini untuk opsi manual/impor).'));
  const opt = (title, info, ready, btn) => h('div', { class: `provider ${ready ? '' : 'off'}` }, h('div', {}, h('strong', {}, title), h('div', { class: 'muted small' }, info)), btn);

  panel.append(
    opt('Lokal — faster-whisper (disarankan)', `${st.local.available ? `Siap. ${st.local.detail}, model "${st.local.model}".` : `Belum tersedia: ${st.local.detail} Pasang: ${st.local.setup}`} Audio tidak keluar dari komputer.`, st.local.available,
      h('button', { class: 'btn primary', disabled: !st.local.available || !!job || !p.source.meta.hasAudio, onclick: () => runJob(api.transcribe(p.id, 'local'), { okMsg: 'Transkrip selesai — silakan koreksi.' }) }, 'Transkripsi lokal')),
    opt('Cloud — OpenAI Whisper API', `${st.openai.available ? 'API key terkonfigurasi.' : `Belum tersedia: ${st.openai.detail}.`} Mengirim audio (bukan video) ke OpenAI setelah persetujuan.`, st.openai.available,
      h('button', {
        class: 'btn', disabled: !st.openai.available || !!job || !p.source.meta.hasAudio,
        onclick: async () => {
          const ok = await consentDialog({ title: 'Kirim audio ke OpenAI?', service: 'OpenAI Whisper API', sent: 'trek audio video ini (mono, 16 kHz, terkompresi).', notSent: 'gambar video, wajah, nama file, data proyek lain, API key lain.' });
          if (ok) runJob(api.transcribe(p.id, 'openai', true), { okMsg: 'Transkrip selesai — silakan koreksi.' });
        },
      }, 'Transkripsi cloud')),
  );

  const ta = h('textarea', { rows: 5, placeholder: 'Tempel atau ketik naskah/ucapan di sini. Pisahkan kalimat dengan titik atau baris baru.' });
  const fileIn = h('input', {
    type: 'file', accept: '.srt,.vtt',
    onchange: async (e) => {
      const f = e.target.files[0];
      if (!f) return;
      try {
        setProject(await api.importTranscript(p.id, await f.text(), f.name), { keepHistory: true });
        toast(`Subtitle "${f.name}" diimpor.`, 'ok');
      } catch (err) {
        toast(err.message, 'error', err.hint);
      }
    },
  });
  panel.append(
    h('details', { class: 'provider', open: !st.local.available && !st.openai.available },
      h('summary', {}, h('strong', {}, 'Manual — ketik/tempel teks atau impor .srt/.vtt'), h('span', { class: 'muted small' }, ' · selalu tersedia, tanpa jaringan')),
      h('p', { class: 'muted small' }, p.analysis?.speech?.length ? 'Waktu tiap kalimat diestimasi dari rentang ucapan hasil analisis; koreksi setelahnya.' : 'Tips: jalankan Analisis video dulu agar estimasi waktu mengikuti jeda bicara.'),
      ta,
      h('div', { class: 'row' },
        h('button', { class: 'btn', onclick: async () => {
          try {
            setProject(await api.manualTranscript(p.id, ta.value), { keepHistory: true });
            toast('Transkrip manual dibuat. Waktu masih estimasi — mohon dikoreksi.', 'ok');
          } catch (e) {
            toast(e.message, 'error', e.hint);
          }
        } }, 'Buat dari teks'),
        h('span', { class: 'muted' }, 'atau'),
        fileIn,
      ),
    ),
  );
  if (!p.source.meta.hasAudio) panel.append(h('div', { class: 'alert warn' }, 'Video tidak memiliki audio — transkripsi otomatis tidak tersedia. Gunakan opsi manual.'));
  return panel;
}

function playRange(video, s, e) {
  video.currentTime = s;
  video.play();
  const stop = () => {
    if (video.currentTime >= e) {
      video.pause();
      video.removeEventListener('timeupdate', stop);
    }
  };
  video.addEventListener('timeupdate', stop);
}

function rescaleWords(seg, oldS, oldE) {
  const d = oldE - oldS || 1;
  seg.words = (seg.words || []).map((w) => ({ ...w, start: r3(seg.start + ((w.start - oldS) / d) * (seg.end - seg.start)), end: r3(seg.start + ((w.end - oldS) / d) * (seg.end - seg.start)) }));
}

function segmentsPanel(p, video) {
  const t = p.transcript;
  const dur = p.source.meta.duration;
  const panel = h('section', { class: 'panel' });
  const edited = t.segments.filter((s) => s.text !== s.originalText).length;
  panel.append(
    h('div', { class: 'row between wrap' },
      h('div', {}, h('h2', {}, `Transkrip (${t.segments.length} segmen)`),
        h('div', { class: 'row wrap' }, badge({ 'local-whisper': 'Sumber: Whisper lokal', openai: 'Sumber: OpenAI (cloud)', manual: 'Sumber: ketikan manual', import: `Sumber: impor ${t.fileName || ''}` }[t.source] || t.source), t.language ? badge(`Bahasa: ${t.language}`) : null, edited ? badge(`${edited} segmen diubah dari asli`, 'warn') : null)),
      h('div', { class: 'row' },
        h('a', { class: 'btn ghost sm', href: `/api/projects/${p.id}/transcript.srt`, download: 'transkrip.srt' }, 'Unduh .srt'),
        h('button', { class: 'btn ghost sm', onclick: () => edit((x) => {
          const at = Math.min(dur - 0.5, video.currentTime || 0);
          x.transcript.segments.push(makeSegment({ start: at, end: Math.min(dur, at + 2), text: 'teks baru', timing: 'manual' }));
          x.transcript.segments.sort((a, b) => a.start - b.start);
        }) }, '+ Segmen di posisi video'),
      ),
    ),
  );
  if (t.note) panel.append(h('p', { class: 'muted small' }, t.note));
  panel.append(h('p', { class: 'muted small' }, 'Klik kata untuk menandai/menghapus penekanan (blok warna aksen). Ubah teks hanya untuk memperbaiki salah dengar — bukan menulis ulang makna.'));

  t.segments.forEach((seg, i) => {
    const overlap = i > 0 && seg.start < t.segments[i - 1].end - 0.01;
    const [tl, tk] = TIMING[seg.timing] || [seg.timing, ''];
    const textArea = h('textarea', {
      rows: 2, value: seg.text, class: seg.text !== seg.originalText ? 'changed' : '',
      onchange: (e) => edit((x) => {
        const s = x.transcript.segments[i];
        s.text = e.target.value.replace(/\s+/g, ' ').trim();
        syncSegmentWords(s);
        x.transcript.reviewed = false;
      }),
    });
    const words = h('div', { class: 'words' }, ...(seg.words || []).map((w, wi) =>
      h('button', { class: `word ${w.emph ? 'emph' : ''}`, title: `${w.start.toFixed(2)}–${w.end.toFixed(2)} dtk`, onclick: () => edit((x) => {
        const ww = x.transcript.segments[i].words[wi];
        ww.emph = !ww.emph || undefined;
      }) }, w.text)));
    const setTime = (k) => (v) => edit((x) => {
      const s = x.transcript.segments[i];
      const oS = s.start, oE = s.end;
      s[k] = Math.max(0, Math.min(dur, v));
      if (s.end <= s.start) return toast('Waktu selesai harus lebih besar dari waktu mulai.', 'warn');
      rescaleWords(s, oS, oE);
    });
    panel.append(
      h('div', { class: `seg ${seg.hidden ? 'hidden-seg' : ''}` },
        h('div', { class: 'seg-time' },
          h('button', { class: 'btn icon', title: 'Putar segmen', onclick: () => playRange(video, seg.start, seg.end) }, '▶'),
          num(seg.start, setTime('start'), { step: 0.05, width: '6.2em' }), '–', num(seg.end, setTime('end'), { step: 0.05, width: '6.2em' }),
          h('button', { class: 'btn ghost sm', title: 'Set mulai = posisi video', onclick: () => setTime('start')(r3(video.currentTime)) }, '⇤'),
          h('button', { class: 'btn ghost sm', title: 'Set selesai = posisi video', onclick: () => setTime('end')(r3(video.currentTime)) }, '⇥'),
        ),
        h('div', { class: 'seg-body' },
          textArea,
          words,
          h('div', { class: 'row wrap small' },
            badge(tl, tk),
            overlap ? badge('Tumpang tindih dengan segmen sebelumnya', 'error') : null,
            seg.text !== seg.originalText ? h('span', { class: 'muted', title: seg.originalText }, `Asli: “${seg.originalText.slice(0, 80)}${seg.originalText.length > 80 ? '…' : ''}”`) : null,
            h('input', { type: 'text', class: 'speaker', placeholder: 'Pembicara', value: seg.speaker || '', onchange: (e) => edit((x) => (x.transcript.segments[i].speaker = e.target.value)) }),
            h('button', { class: 'link', onclick: () => edit((x) => {
              const s = x.transcript.segments[i];
              const toks = tokenize(s.text);
              if (toks.length < 2) return;
              const cut = Math.ceil(toks.length / 2);
              const mid = s.words?.[cut]?.start ?? (s.start + s.end) / 2;
              const a = { ...s, end: r3(mid), text: toks.slice(0, cut).join(' '), words: s.words.slice(0, cut), originalText: toks.slice(0, cut).join(' ') };
              const b = { ...s, id: `${s.id}b${Date.now() % 1000}`, start: r3(mid), text: toks.slice(cut).join(' '), words: s.words.slice(cut), originalText: toks.slice(cut).join(' ') };
              x.transcript.segments.splice(i, 1, a, b);
            }) }, 'Pisah'),
            i < t.segments.length - 1 ? h('button', { class: 'link', onclick: () => edit((x) => {
              const [a, b] = x.transcript.segments.slice(i, i + 2);
              const m = { ...a, end: b.end, text: `${a.text} ${b.text}`, originalText: `${a.originalText} ${b.originalText}`, words: [...(a.words || []), ...(b.words || [])] };
              x.transcript.segments.splice(i, 2, m);
            }) }, 'Gabung dgn berikutnya') : null,
            h('button', { class: 'link', onclick: () => edit((x) => (x.transcript.segments[i].hidden = !x.transcript.segments[i].hidden || undefined)) }, seg.hidden ? 'Tampilkan di subtitle' : 'Sembunyikan dari subtitle'),
            h('button', { class: 'link danger', onclick: () => edit((x) => x.transcript.segments.splice(i, 1)) }, 'Hapus'),
          ),
        ),
      ),
    );
  });

  panel.append(
    h('div', { class: 'review-bar' },
      h('label', { class: 'check big' }, h('input', { type: 'checkbox', checked: !!t.reviewed, onchange: (e) => edit((x) => (x.transcript.reviewed = e.target.checked)) }), ' Transkrip sudah saya koreksi (teks & waktu sesuai ucapan)'),
      h('button', { class: 'btn primary', onclick: () => go('plan') }, 'Lanjut ke Rencana edit →'),
    ),
  );
  return panel;
}
