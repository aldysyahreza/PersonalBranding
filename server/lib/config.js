// Konfigurasi aplikasi. Membaca `.env` secara manual (tanpa dependensi) dan
// TIDAK pernah mencetak nilai secret. Modul lain hanya boleh menanyakan
// apakah sebuah key tersedia lewat `hasSecret()`, atau mengambilnya lewat
// `getSecret()` tepat sebelum dipakai.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

const SECRET_KEYS = new Set(['OPENAI_API_KEY', 'ANTHROPIC_API_KEY']);

function loadDotEnv() {
  const file = path.join(ROOT, '.env');
  const out = {};
  if (!fs.existsSync(file)) return out;
  for (const raw of fs.readFileSync(file, 'utf8').split(/\r?\n/)) {
    const line = raw.trim();
    if (!line || line.startsWith('#')) continue;
    const eq = line.indexOf('=');
    if (eq < 0) continue;
    const key = line.slice(0, eq).trim();
    let val = line.slice(eq + 1).trim();
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1);
    }
    out[key] = val;
  }
  return out;
}

const fileEnv = loadDotEnv();

function env(key, fallback = '') {
  const v = process.env[key] ?? fileEnv[key];
  return v === undefined || v === '' ? fallback : v;
}

function resolveDir(p) {
  return path.isAbsolute(p) ? p : path.join(ROOT, p);
}

export const config = {
  port: Number(env('PORT', '4317')),
  host: env('HOST', '127.0.0.1'),
  projectsDir: resolveDir(env('PROJECTS_DIR', 'projects')),
  outputDir: resolveDir(env('OUTPUT_DIR', 'output')),
  maxUploadBytes: Number(env('MAX_UPLOAD_MB', '4096')) * 1024 * 1024,
  whisperModel: env('WHISPER_MODEL', 'small'),
  whisperPython: env('WHISPER_PYTHON', 'python3'),
  whisperLanguage: env('WHISPER_LANGUAGE', ''),
  openaiTranscribeModel: env('OPENAI_TRANSCRIBE_MODEL', 'whisper-1'),
  anthropicModel: env('ANTHROPIC_MODEL', 'claude-opus-5-5'),
  fontsDir: path.join(ROOT, 'assets', 'fonts'),
  presetsDir: path.join(ROOT, 'config', 'presets'),
};

export function hasSecret(key) {
  if (!SECRET_KEYS.has(key)) throw new Error(`Bukan secret yang dikenal: ${key}`);
  return Boolean(env(key));
}

export function getSecret(key) {
  if (!SECRET_KEYS.has(key)) throw new Error(`Bukan secret yang dikenal: ${key}`);
  return env(key);
}

for (const dir of [config.projectsDir, config.outputDir]) {
  fs.mkdirSync(dir, { recursive: true });
}
