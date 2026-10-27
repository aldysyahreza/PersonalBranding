#!/usr/bin/env python3
"""Transkripsi lokal dengan faster-whisper. Audio tidak keluar dari komputer.

Pemakaian: python3 transcribe_local.py <audio.wav> <model> [bahasa]
Output: JSON ke stdout -> {"language": ..., "segments": [{start,end,text,words:[{text,start,end}]}]}
Progres ditulis ke stderr sebagai baris "PROGRESS <0..1>".

Model diunduh otomatis dari Hugging Face pada pemakaian pertama (butuh internet
sekali), lalu disimpan di cache lokal.
"""
import json
import sys


def main():
    if len(sys.argv) < 3:
        print("usage: transcribe_local.py <audio> <model> [language]", file=sys.stderr)
        sys.exit(2)
    audio, model_name = sys.argv[1], sys.argv[2]
    language = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] else None
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("ERROR_NO_FASTER_WHISPER", file=sys.stderr)
        sys.exit(3)

    model = WhisperModel(model_name, device="auto", compute_type="auto")
    segments, info = model.transcribe(
        audio,
        language=language,
        word_timestamps=True,
        vad_filter=True,
        condition_on_previous_text=False,
    )
    total = float(info.duration or 0) or 1.0
    out = []
    for seg in segments:
        words = [
            {"text": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)}
            for w in (seg.words or [])
            if w.word.strip()
        ]
        out.append({"start": round(seg.start, 3), "end": round(seg.end, 3), "text": seg.text.strip(), "words": words})
        print(f"PROGRESS {min(1.0, seg.end / total):.3f}", file=sys.stderr, flush=True)
    json.dump({"language": info.language, "segments": out}, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
