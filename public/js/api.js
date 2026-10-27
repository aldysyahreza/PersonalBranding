// Klien API. Semua permintaan non-GET membawa header X-PB-App (proteksi CSRF lokal).

export class ApiError extends Error {
  constructor(message, hint, status) {
    super(message);
    this.hint = hint;
    this.status = status;
  }
}

async function req(method, url, body, { raw = false, query } = {}) {
  const u = query ? `${url}?${new URLSearchParams(query)}` : url;
  const opts = { method, headers: { 'X-PB-App': '1' } };
  if (body !== undefined) {
    if (raw) opts.body = body;
    else {
      opts.headers['Content-Type'] = 'application/json';
      opts.body = JSON.stringify(body);
    }
  }
  let res;
  try {
    res = await fetch(u, opts);
  } catch {
    throw new ApiError('Tidak dapat terhubung ke server lokal.', 'Pastikan "npm start" masih berjalan di terminal.', 0);
  }
  const data = (res.headers.get('content-type') || '').includes('json') ? await res.json() : await res.text();
  if (!res.ok) throw new ApiError(data?.error || `Permintaan gagal (${res.status})`, data?.hint || '', res.status);
  return data;
}

/** Unggah file dengan progres (XHR karena fetch belum punya progres upload). */
function upload(url, file, query, onProgress) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', `${url}?${new URLSearchParams({ name: file.name, ...query })}`);
    xhr.setRequestHeader('X-PB-App', '1');
    xhr.upload.onprogress = (e) => e.lengthComputable && onProgress?.(e.loaded / e.total);
    xhr.onload = () => {
      let data = {};
      try {
        data = JSON.parse(xhr.responseText);
      } catch {}
      if (xhr.status >= 200 && xhr.status < 300) resolve(data);
      else reject(new ApiError(data.error || `Unggahan gagal (${xhr.status})`, data.hint || '', xhr.status));
    };
    xhr.onerror = () => reject(new ApiError('Unggahan terputus.', 'Periksa apakah server masih berjalan.', 0));
    xhr.send(file);
  });
}

export const api = {
  status: () => req('GET', '/api/status'),
  projects: () => req('GET', '/api/projects'),
  createProject: (b) => req('POST', '/api/projects', b),
  project: (id) => req('GET', `/api/projects/${id}`),
  saveProject: (id, b) => req('PUT', `/api/projects/${id}`, b),
  deleteProject: (id) => req('DELETE', `/api/projects/${id}`),
  uploadSource: (id, file, onP) => upload(`/api/projects/${id}/source/upload`, file, {}, onP),
  sourceFromPath: (id, path) => req('POST', `/api/projects/${id}/source/path`, { path }),
  uploadAsset: (id, file, license, onP) => upload(`/api/projects/${id}/assets/upload`, file, { license }, onP),
  assetFromPath: (id, path, license) => req('POST', `/api/projects/${id}/assets/path`, { path, license }),
  updateAsset: (id, aid, b) => req('PUT', `/api/projects/${id}/assets/${aid}`, b),
  deleteAsset: (id, aid) => req('DELETE', `/api/projects/${id}/assets/${aid}`),
  analyze: (id) => req('POST', `/api/projects/${id}/analyze`),
  transcribe: (id, provider, consent) => req('POST', `/api/projects/${id}/transcribe`, { provider, consent }),
  manualTranscript: (id, text) => req('POST', `/api/projects/${id}/transcript/manual`, { text }),
  importTranscript: (id, content, name) => req('POST', `/api/projects/${id}/transcript/import`, { content, name }),
  plan: (id, source, consent) => req('POST', `/api/projects/${id}/plan`, { source, consent }),
  applyPreset: (id, presetId, level) => req('POST', `/api/projects/${id}/apply-preset`, { presetId, level }),
  savePreset: (b) => req('POST', '/api/presets', b),
  preflight: (id, q) => req('GET', `/api/projects/${id}/preflight`, undefined, { query: q }),
  still: (id, b) => req('POST', `/api/projects/${id}/still`, b),
  render: (id, b) => req('POST', `/api/projects/${id}/render`, b),
  job: (jid) => req('GET', `/api/jobs/${jid}`),
  cancelJob: (jid) => req('POST', `/api/jobs/${jid}/cancel`),
};

/** Pantau job sampai selesai. onTick dipanggil setiap pembaruan. */
export async function watchJob(job, onTick) {
  let j = job;
  onTick?.(j);
  while (j.state === 'running') {
    await new Promise((r) => setTimeout(r, 900));
    try {
      j = await api.job(j.id);
    } catch (e) {
      j = { ...j, state: 'failed', error: { message: e.message, hint: e.hint } };
    }
    onTick?.(j);
  }
  return j;
}
