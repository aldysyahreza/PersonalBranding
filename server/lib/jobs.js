// Registry pekerjaan panjang (analisis, transkripsi, render) di memori.
// Status dilaporkan apa adanya: running → done | failed | canceled.
import { uid } from '../../public/shared/core.js';

const jobs = new Map();

export function createJob(type, projectId, label) {
  const job = {
    id: uid('job'),
    type,
    projectId,
    label,
    state: 'running',
    progress: 0,
    message: 'Memulai…',
    startedAt: new Date().toISOString(),
    finishedAt: null,
    result: null,
    error: null,
    controller: new AbortController(),
  };
  jobs.set(job.id, job);
  return job;
}

export function runJob(job, fn) {
  Promise.resolve()
    .then(() => fn(job))
    .then((result) => {
      if (job.state === 'running') Object.assign(job, { state: 'done', progress: 1, result, message: 'Selesai' });
    })
    .catch((err) => {
      if (job.controller.signal.aborted) {
        Object.assign(job, { state: 'canceled', message: 'Dibatalkan oleh pengguna.' });
      } else {
        Object.assign(job, { state: 'failed', message: err.message, error: { message: err.message, hint: err.hint || '' } });
        if (!err.hint) console.error(`[job ${job.type}]`, err.message);
      }
    })
    .finally(() => {
      job.finishedAt = new Date().toISOString();
    });
  return job;
}

export function getJob(id) {
  return jobs.get(id);
}

export function listJobs(projectId) {
  return [...jobs.values()].filter((j) => !projectId || j.projectId === projectId);
}

export function cancelJob(id) {
  const j = jobs.get(id);
  if (j && j.state === 'running') j.controller.abort();
  return j;
}

export function publicJob(j) {
  if (!j) return null;
  const { controller, ...rest } = j;
  return rest;
}
