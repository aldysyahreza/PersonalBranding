// Preset gaya disimpan sebagai JSON di config/presets/. Satu file = satu preset.
// Gaya proyek = deepMerge(preset dasar, override level gaya), lalu disalin ke
// project.style sehingga perubahan pengguna tersimpan per proyek.
import fs from 'node:fs';
import path from 'node:path';
import { config } from './config.js';
import { UserError } from './media.js';

export const STYLE_LEVELS = ['minimal', 'editorial', 'dinamis'];

export function deepMerge(base, over) {
  if (Array.isArray(over)) return over.slice();
  if (over === null || typeof over !== 'object') return over === undefined ? base : over;
  const out = { ...(base && typeof base === 'object' ? base : {}) };
  for (const [k, v] of Object.entries(over)) out[k] = deepMerge(out[k], v);
  return out;
}

export function listPresets() {
  return fs
    .readdirSync(config.presetsDir)
    .filter((f) => f.endsWith('.json'))
    .map((f) => {
      try {
        return JSON.parse(fs.readFileSync(path.join(config.presetsDir, f), 'utf8'));
      } catch {
        return null;
      }
    })
    .filter(Boolean);
}

export function getPreset(id) {
  const p = listPresets().find((x) => x.id === id);
  if (!p) throw new UserError(`Preset "${id}" tidak ditemukan.`, `Periksa folder ${config.presetsDir}.`, 404);
  return p;
}

export function resolveStyle(preset, level = 'editorial') {
  const { styleLevels = {}, id, name, status, note, ...base } = preset;
  return deepMerge(base, styleLevels[level] || {});
}

export function savePreset({ id, name, style, basedOn }) {
  if (!/^[a-z0-9-]{3,60}$/.test(id || '')) {
    throw new UserError('ID preset tidak valid.', 'Gunakan huruf kecil, angka, dan tanda hubung (3–60 karakter).');
  }
  const file = path.join(config.presetsDir, `${id}.json`);
  if (id === 'aldy-editorial') {
    throw new UserError('Preset bawaan tidak ditimpa dari aplikasi.', 'Simpan dengan ID lain, atau edit file JSON-nya secara langsung.');
  }
  const data = {
    id,
    name: name || id,
    status: 'buatan pengguna',
    note: basedOn ? `Disimpan dari proyek, berbasis preset "${basedOn}".` : 'Disimpan dari proyek.',
    ...style,
    styleLevels: {},
  };
  fs.writeFileSync(file, JSON.stringify(data, null, 2));
  return data;
}
