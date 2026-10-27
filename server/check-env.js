// `npm run check` — memeriksa kesiapan lingkungan tanpa mencetak secret.
import { which } from './lib/proc.js';
import { hasSecret, config } from './lib/config.js';
import { providerStatus } from './lib/transcribe.js';
import { run } from './lib/proc.js';

const ok = (b) => (b ? '✔' : '✘');
const node = process.versions.node;
const ffmpeg = await which('ffmpeg');
const ffprobe = await which('ffprobe');
let libass = false;
if (ffmpeg) {
  const r = await run('ffmpeg', ['-hide_banner', '-filters']);
  libass = /\sass\s/.test(r.stdout);
}
const stt = await providerStatus();
let sdk = false;
try {
  await import('@anthropic-ai/sdk');
  sdk = true;
} catch {}

console.log(`${ok(Number(node.split('.')[0]) >= 20)} Node.js ${node} (butuh >= 20)`);
console.log(`${ok(ffmpeg)} ffmpeg: ${ffmpeg || 'tidak ditemukan — wajib untuk analisis & render'}`);
console.log(`${ok(ffprobe)} ffprobe: ${ffprobe || 'tidak ditemukan — wajib'}`);
console.log(`${ok(libass)} filter subtitle libass (ass) ${libass ? 'tersedia' : 'TIDAK tersedia — subtitle/kartu tidak bisa dirender'}`);
console.log(`${ok(stt.local.available)} Transkripsi lokal: ${stt.local.detail}${stt.local.available ? ` (model ${config.whisperModel})` : ` — opsional: ${stt.local.setup}`}`);
console.log(`${ok(hasSecret('OPENAI_API_KEY'))} Transkripsi cloud OpenAI: ${hasSecret('OPENAI_API_KEY') ? 'key terkonfigurasi' : 'tidak dikonfigurasi (opsional)'}`);
console.log(`${ok(hasSecret('ANTHROPIC_API_KEY') && sdk)} Rencana edit Claude: ${hasSecret('ANTHROPIC_API_KEY') ? 'key terkonfigurasi' : 'key tidak dikonfigurasi'}; SDK ${sdk ? 'terpasang' : 'belum terpasang (npm install)'} (opsional)`);
console.log(`  Folder proyek: ${config.projectsDir}`);
console.log(`  Folder output: ${config.outputDir}`);
