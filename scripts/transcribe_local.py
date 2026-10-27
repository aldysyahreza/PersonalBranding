#!/usr/bin/env python3
"""Transkripsi lokal dengan faster-whisper. Audio tidak keluar dari komputer.

Pemakaian: python3 transcribe_local.py <audio.wav> <model> [bahasa] [device]
device: auto (GPU bila library CUDA lengkap, jika tidak otomatis CPU) | cpu | cuda
Output: JSON ke stdout -> {"language": ..., "segments": [{start,end,text,words:[{text,start,end}]}]}
Progres ditulis ke stderr sebagai baris "PROGRESS <0..1>".

Model diunduh otomatis dari Hugging Face pada pemakaian pertama (butuh internet
sekali), lalu disimpan di cache lokal.
"""
import json
import re
import sys


def load_wav(path):
    """Baca WAV PCM 16-bit mono 16 kHz (sudah diekstrak ffmpeg) sebagai float32.

    Sengaja tidak memakai decoder bawaan faster-whisper (PyAV), karena versi PyAV
    terbaru tidak kompatibel (TypeError: open() ... 'metadata_errors').
    """
    import wave

    import numpy as np

    with wave.open(path, "rb") as w:
        if w.getsampwidth() != 2 or w.getnchannels() != 1 or w.getframerate() != 16000:
            raise ValueError("Audio harus WAV PCM 16-bit mono 16 kHz")
        data = w.readframes(w.getnframes())
    return np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0


GPU_ERROR = re.compile(r"cublas|cudnn|cuda|\.dll|libcu", re.IGNORECASE)


def run(WhisperModel, model_name, device, samples, language):
    compute_type = "int8" if device == "cpu" else "auto"
    model = WhisperModel(model_name, device=device, compute_type=compute_type)
    segments, info = model.transcribe(
        samples,
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
    return info, out


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

    device = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] else "auto"
    samples = load_wav(audio)
    try:
        info, out = run(WhisperModel, model_name, device, samples, language)
    except RuntimeError as err:
        # GPU NVIDIA terdeteksi tetapi library CUDA (cuBLAS/cuDNN) tidak terpasang:
        # kegagalan baru muncul saat inferensi, jadi ulangi seluruhnya di CPU.
        if device == "cpu" or not GPU_ERROR.search(str(err)):
            raise
        print(f"GPU tidak dapat dipakai ({err}); beralih ke CPU.", file=sys.stderr, flush=True)
        info, out = run(WhisperModel, model_name, "cpu", samples, language)
    json.dump({"language": info.language, "segments": out}, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
