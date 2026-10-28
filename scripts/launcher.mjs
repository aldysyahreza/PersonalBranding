#!/usr/bin/env node
// Peluncur Personal Branding Video Studio (lintas platform, utama untuk Windows).
//
//   node scripts/launcher.mjs                 nyalakan (jika belum) lalu buka browser
//   node scripts/launcher.mjs --no-browser    nyalakan di latar belakang saja (dipakai auto-start)
//   node scripts/launcher.mjs --status        cek apakah aplikasi sedang berjalan
//   node scripts/launcher.mjs --stop          matikan aplikasi
//   node scripts/launcher.mjs --install-autostart     nyala otomatis saat login Windows
//   node scripts/launcher.mjs --uninstall-autostart   hapus auto-start
//
// Server berjalan tersembunyi (tanpa jendela terminal); log ada di logs/server.log.
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const LOG_DIR = path.join(ROOT, 'logs');
const PID_FILE = path.join(LOG_DIR, 'server.pid');
const AUTOSTART_NAME = 'Personal Branding Video Studio.vbs';

/** Baca PORT/HOST dari .env tanpa memuat modul aplikasi (dan tanpa mencetak secret). */
function readEnv() {
  const out = {};
  const f = path.join(ROOT, '.env');
  if (fs.existsSync(f)) {
    for (const raw of fs.readFileSync(f, 'utf8').split(/\r?\n/)) {
      const m = raw.match(/^\s*(PORT|HOST)\s*=\s*"?([^"#\s]*)"?/);
      if (m && m[2]) out[m[1]] = m[2];
    }
  }
  return { port: Number(process.env.PORT || out.PORT || 4317), host: process.env.HOST || out.HOST || '127.0.0.1' };
}

const { port, host } = readEnv();
const browserHost = host === '0.0.0.0' ? '127.0.0.1' : host;
const URL_APP = `http://${browserHost}:${port}`;

async function isRunning() {
  try {
    const r = await fetch(`${URL_APP}/api/status`, { signal: AbortSignal.timeout(2500) });
    if (!r.ok) return false;
    const d = await r.json();
    return d.app === 'personal-branding-video-studio';
  } catch {
    return false;
  }
}

/** Ada program lain di port ini? (merespons, tapi bukan aplikasi ini) */
async function portTakenByOther() {
  try {
    await fetch(`${URL_APP}/`, { signal: AbortSignal.timeout(2000) });
    return !(await isRunning());
  } catch {
    return false;
  }
}

function openBrowser(url) {
  const [cmd, args] =
    process.platform === 'win32' ? ['cmd.exe', ['/c', 'start', '', url]]
    : process.platform === 'darwin' ? ['open', [url]]
    : ['xdg-open', [url]];
  try {
    const c = spawn(cmd, args, { detached: true, stdio: 'ignore', windowsHide: true });
    c.on('error', () => console.log(`Buka di browser: ${url}`));
    c.unref();
  } catch {
    console.log(`Buka di browser: ${url}`);
  }
}

function tailLog(n = 12) {
  const f = path.join(LOG_DIR, 'server.log');
  if (!fs.existsSync(f)) return '';
  return fs.readFileSync(f, 'utf8').split(/\r?\n/).filter(Boolean).slice(-n).join('\n');
}

async function start({ browser = true } = {}) {
  if (await isRunning()) {
    console.log(`Aplikasi sudah berjalan di ${URL_APP}`);
    if (browser) openBrowser(URL_APP);
    return 0;
  }
  if (await portTakenByOther()) {
    console.error(`Port ${port} dipakai program lain. Ubah PORT di file .env (mis. PORT=${port + 83}), lalu coba lagi.`);
    return 1;
  }
  if (!fs.existsSync(path.join(ROOT, 'node_modules'))) {
    console.error('Paket belum terpasang. Jalankan "npm install" sekali di folder aplikasi, lalu coba lagi.');
    return 1;
  }
  fs.mkdirSync(LOG_DIR, { recursive: true });
  const log = fs.openSync(path.join(LOG_DIR, 'server.log'), 'a');
  fs.writeSync(log, `\n===== ${new Date().toISOString()} — mulai =====\n`);
  // Proses server terlepas dari peluncur & tanpa jendela, sehingga tetap jalan setelah peluncur selesai.
  const child = spawn(process.execPath, [path.join(ROOT, 'server', 'index.js')], {
    cwd: ROOT,
    detached: true,
    windowsHide: true,
    stdio: ['ignore', log, log],
  });
  child.unref();
  console.log('Menyalakan aplikasi...');
  for (let i = 0; i < 40; i++) {
    await new Promise((r) => setTimeout(r, 500));
    if (await isRunning()) {
      console.log(`Aplikasi berjalan di ${URL_APP}`);
      if (browser) openBrowser(URL_APP);
      return 0;
    }
    if (child.exitCode !== null) break;
  }
  console.error('Aplikasi gagal menyala. Cuplikan log terakhir:\n' + tailLog());
  return 1;
}

async function stop() {
  if (!(await isRunning())) {
    console.log('Aplikasi tidak sedang berjalan.');
    return 0;
  }
  const pid = fs.existsSync(PID_FILE) ? Number(fs.readFileSync(PID_FILE, 'utf8')) : 0;
  if (!pid) {
    console.error('Aplikasi berjalan, tetapi PID tidak diketahui. Tutup jendela terminal "npm start" bila ada, atau restart laptop.');
    return 1;
  }
  try {
    process.kill(pid);
  } catch (e) {
    console.error(`Gagal menghentikan proses ${pid}: ${e.message}`);
    return 1;
  }
  for (let i = 0; i < 20; i++) {
    await new Promise((r) => setTimeout(r, 300));
    if (!(await isRunning())) {
      console.log('Aplikasi dihentikan.');
      return 0;
    }
  }
  console.error('Aplikasi belum berhenti. Coba lagi beberapa detik lagi.');
  return 1;
}

function startupDir() {
  if (process.env.PB_STARTUP_DIR) return process.env.PB_STARTUP_DIR; // untuk pengujian
  if (process.platform !== 'win32') return null;
  return path.join(process.env.APPDATA || '', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup');
}

/** Skrip VBS kecil di folder Startup: menjalankan peluncur tanpa jendela saat login. */
export function autostartScript(nodePath = process.execPath) {
  const q = (s) => s.replace(/"/g, '""');
  const launcher = path.join(ROOT, 'scripts', 'launcher.mjs');
  return [
    "' Dibuat oleh Personal Branding Video Studio - menyalakan aplikasi saat login (tanpa jendela).",
    "' Hapus dengan: Hapus-Autostart.cmd (atau hapus file ini).",
    'Set sh = CreateObject("WScript.Shell")',
    `sh.CurrentDirectory = "${q(ROOT)}"`,
    `sh.Run """${q(nodePath)}"" ""${q(launcher)}"" --no-browser", 0, False`,
    '',
  ].join('\r\n');
}

function installAutostart() {
  const dir = startupDir();
  if (!dir) {
    console.error('Auto-start otomatis saat ini hanya disiapkan untuk Windows. Di macOS/Linux, tambahkan "node scripts/launcher.mjs --no-browser" ke Login Items / aplikasi startup.');
    return 1;
  }
  fs.mkdirSync(dir, { recursive: true });
  const file = path.join(dir, AUTOSTART_NAME);
  fs.writeFileSync(file, autostartScript());
  console.log(`Auto-start aktif. Aplikasi akan menyala sendiri setiap Anda login ke Windows.\nFile: ${file}\nBuka ${URL_APP} di browser kapan saja (simpan sebagai bookmark).`);
  return 0;
}

function uninstallAutostart() {
  const dir = startupDir();
  const file = dir && path.join(dir, AUTOSTART_NAME);
  if (file && fs.existsSync(file)) {
    fs.rmSync(file);
    console.log('Auto-start dihapus. Aplikasi tidak lagi menyala otomatis saat login.');
  } else console.log('Auto-start memang belum terpasang.');
  return 0;
}

const args = new Set(process.argv.slice(2));
let code;
if (args.has('--status')) {
  const up = await isRunning();
  console.log(up ? `Aplikasi berjalan di ${URL_APP}` : 'Aplikasi tidak sedang berjalan.');
  code = up ? 0 : 3;
} else if (args.has('--stop')) code = await stop();
else if (args.has('--install-autostart')) code = installAutostart();
else if (args.has('--uninstall-autostart')) code = uninstallAutostart();
else code = await start({ browser: !args.has('--no-browser') });
process.exit(code);
