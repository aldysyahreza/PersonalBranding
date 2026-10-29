// Penyimpanan proyek: projects/<id>/project.json (+ source/, assets/, work/).
// Video sumber TIDAK pernah ditulis ulang: unggahan disalin ke source/,
// path lokal hanya direferensikan (read-only).
import fs from 'node:fs';
import path from 'node:path';
import { config } from './config.js';
import { uid } from '../../public/shared/core.js';
import { getPreset, resolveStyle } from './presets.js';
import { UserError } from './media.js';
import { DEFAULT_BRAND_KEYWORDS } from './brand.js';

const ID_RE = /^prj_[a-z0-9]{4,12}$/;

export function projectDir(id) {
  if (!ID_RE.test(id)) throw new UserError('ID proyek tidak valid.', '', 400);
  return path.join(config.projectsDir, id);
}

function file(id) {
  return path.join(projectDir(id), 'project.json');
}

export function workDir(id) {
  const d = path.join(projectDir(id), 'work');
  fs.mkdirSync(d, { recursive: true });
  return d;
}

export function assetsDir(id) {
  const d = path.join(projectDir(id), 'assets');
  fs.mkdirSync(d, { recursive: true });
  return d;
}

export function createProject({ name, presetId = 'brand-fixer', level = 'editorial' }) {
  const id = uid('prj');
  const preset = getPreset(presetId);
  const now = new Date().toISOString();
  const p = {
    id,
    name: String(name || 'Proyek tanpa nama').slice(0, 120),
    createdAt: now,
    updatedAt: now,
    presetId,
    styleLevel: level,
    style: resolveStyle(preset, level),
    output: { aspect: preset.output?.aspect || '9:16', framing: 'fill', reframe: { x: 0.5, y: 0.5, zoom: 1 } },
    source: null,
    analysis: null,
    transcript: null,
    plan: null,
    cuts: [],
    zooms: [],
    emphasisSuggestions: [],
    cards: [],
    broll: [],
    sfx: [],
    music: { assetId: null, enabled: false, volumeDb: preset.audio?.musicDb ?? -24, fadeIn: 1, fadeOut: 1.5, startAt: 0 },
    assets: [],
    brandKeywords: DEFAULT_BRAND_KEYWORDS.slice(),
    exports: [],
  };
  fs.mkdirSync(projectDir(id), { recursive: true });
  saveProject(p);
  return p;
}

export function saveProject(p) {
  p.updatedAt = new Date().toISOString();
  const f = file(p.id);
  const tmp = `${f}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(p, null, 2));
  fs.renameSync(tmp, f);
  return p;
}

export function loadProject(id) {
  const f = file(id);
  if (!fs.existsSync(f)) throw new UserError('Proyek tidak ditemukan.', 'Mungkin sudah dihapus dari folder projects/.', 404);
  const p = JSON.parse(fs.readFileSync(f, 'utf8'));
  // Proyek lama dibuat sebelum fitur zoom punch-in.
  p.zooms ||= [];
  if (p.style && !p.style.zoom) p.style.zoom = { punchIn: 1.12 };
  if (p.source) {
    const exists = fs.existsSync(p.source.path);
    p.source.missing = !exists;
    p.source.changed = exists && fs.statSync(p.source.path).size !== p.source.size;
  }
  for (const a of p.assets || []) a.missing = !fs.existsSync(a.path);
  for (const e of p.exports || []) if (e.state === 'done') e.missing = !fs.existsSync(e.path);
  return p;
}

export function listProjects() {
  if (!fs.existsSync(config.projectsDir)) return [];
  return fs
    .readdirSync(config.projectsDir)
    .filter((d) => ID_RE.test(d) && fs.existsSync(path.join(config.projectsDir, d, 'project.json')))
    .map((d) => {
      try {
        return loadProject(d);
      } catch {
        return null;
      }
    })
    .filter(Boolean)
    .sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));
}

/** Field yang boleh diubah langsung dari UI lewat PUT. Field lain dikelola server. */
export const EDITABLE = ['name', 'style', 'styleLevel', 'output', 'transcript', 'cuts', 'zooms', 'emphasisSuggestions', 'cards', 'broll', 'sfx', 'music', 'brandKeywords', 'plan', 'hook', 'endcard'];

export function applyEdits(p, body) {
  for (const k of EDITABLE) if (k in body) p[k] = body[k];
  return p;
}

export function deleteProject(id) {
  // Hanya folder proyek (salinan unggahan, aset, file kerja) yang dihapus.
  // File sumber yang direferensikan via path lokal dan folder output TIDAK disentuh.
  fs.rmSync(projectDir(id), { recursive: true, force: true });
}
