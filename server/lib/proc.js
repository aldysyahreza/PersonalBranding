// Utilitas menjalankan proses eksternal (ffmpeg, ffprobe, python) tanpa shell,
// sehingga path file dengan spasi/karakter khusus aman dan tidak ada injeksi.
import { spawn } from 'node:child_process';

export function run(cmd, args, { onStderr, onStdout, timeoutMs = 0, signal } = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(cmd, args, { stdio: ['ignore', 'pipe', 'pipe'], signal });
    let stdout = '';
    let stderr = '';
    let timer;
    if (timeoutMs) timer = setTimeout(() => child.kill('SIGKILL'), timeoutMs);
    child.stdout.on('data', (d) => {
      const s = d.toString();
      stdout += s;
      onStdout?.(s);
    });
    child.stderr.on('data', (d) => {
      const s = d.toString();
      // Simpan hanya ekor stderr agar memori tidak membengkak pada render panjang.
      stderr = (stderr + s).slice(-20000);
      onStderr?.(s);
    });
    child.on('error', (err) => {
      clearTimeout(timer);
      if (err.code === 'ENOENT') err.message = `Program "${cmd}" tidak ditemukan. Pastikan sudah terpasang dan ada di PATH.`;
      reject(err);
    });
    child.on('close', (code, sig) => {
      clearTimeout(timer);
      resolve({ code, signal: sig, stdout, stderr });
    });
  });
}

export async function which(cmd, args = ['-version']) {
  try {
    const r = await run(cmd, args, { timeoutMs: 15000 });
    return r.code === 0 ? (r.stdout || r.stderr).split('\n')[0].trim() : null;
  } catch {
    return null;
  }
}
