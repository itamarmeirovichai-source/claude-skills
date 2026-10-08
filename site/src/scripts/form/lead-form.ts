import { leadSchema, qualifySchema, fieldErrors, MESSAGES, MAX_FILES, MAX_CLIENT_FILE_BYTES } from '../../lib/lead-schema';
import { track } from '../core/analytics';
import { site } from '../../lib/site';

const MAX_EDGE = 2048;

async function resize(file: File): Promise<Blob | null> {
  try {
    const bmp = await createImageBitmap(file);
    const scale = Math.min(1, MAX_EDGE / Math.max(bmp.width, bmp.height));
    const w = Math.round(bmp.width * scale);
    const h = Math.round(bmp.height * scale);
    const c = document.createElement('canvas');
    c.width = w;
    c.height = h;
    c.getContext('2d')?.drawImage(bmp, 0, 0, w, h);
    bmp.close();
    // Re-encoding also strips EXIF (location) data.
    for (const q of [0.88, 0.8, 0.7, 0.6]) {
      const b = await new Promise<Blob | null>((r) => c.toBlob(r, 'image/webp', q));
      const out = b && b.type === 'image/webp' ? b : await new Promise<Blob | null>((r) => c.toBlob(r, 'image/jpeg', q));
      if (out && out.size <= 3.8 * 1024 * 1024) return out;
    }
    return null;
  } catch {
    return null; // e.g. HEIC the browser can't decode → we use the site photos instead
  }
}

function setError(form: HTMLFormElement, name: string, msg: string): void {
  const input = form.querySelector<HTMLElement>(`[name="${name}"]`);
  const err = form.querySelector<HTMLElement>(`[data-error="${name}"]`);
  if (input) input.setAttribute('aria-invalid', msg ? 'true' : 'false');
  if (err) err.textContent = msg;
}

function loadTurnstile(form: HTMLFormElement): void {
  const box = form.querySelector<HTMLElement>('[data-turnstile]');
  const key = site.turnstileSiteKey;
  if (!box || !key) return;
  const w = window as unknown as { turnstile?: { render: (el: HTMLElement, o: object) => void }; onVxoTurnstile?: () => void };
  w.onVxoTurnstile = () => w.turnstile?.render(box, { sitekey: key, appearance: 'interaction-only', 'response-field-name': 'turnstileToken' });
  const s = document.createElement('script');
  s.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit&onload=onVxoTurnstile';
  s.async = true;
  document.head.append(s);
}

export function mountForm(form: HTMLFormElement): void {
  if (form.dataset['mounted']) return;
  form.dataset['mounted'] = '1';
  if (form.hasAttribute('data-qualify-form')) return mountQualify(form);
  const t0 = Date.now();
  const params = new URLSearchParams(location.search);
  const intent = params.get('for');
  const intentInput = form.querySelector<HTMLInputElement>('[name="intent"]');
  if (intentInput && (intent === 'bestseller' || intent === 'launch')) intentInput.value = intent;
  const utm: Record<string, string> = {};
  params.forEach((v, k) => {
    if (k.startsWith('utm_')) utm[k.slice(0, 40)] = v.slice(0, 120);
  });
  loadTurnstile(form);
  let started = false;
  form.addEventListener('input', () => {
    if (!started) {
      started = true;
      track('form_start');
    }
  });

  const fileInput = form.querySelector<HTMLInputElement>('input[type="file"]');
  const fileList = form.querySelector<HTMLElement>('[data-file-list]');
  fileInput?.addEventListener('change', () => {
    const files = [...(fileInput.files ?? [])];
    let msg = '';
    if (files.length > MAX_FILES) msg = `Up to ${MAX_FILES} photos, please.`;
    else if (files.some((f) => f.size > MAX_CLIENT_FILE_BYTES)) msg = MESSAGES.fileSize;
    setError(form, 'photos', msg);
    if (fileList) fileList.textContent = files.length ? files.map((f) => f.name).join(', ') : '';
  });

  const read = () => {
    const fd = new FormData(form);
    return {
      email: String(fd.get('email') ?? ''),
      website: String(fd.get('website') ?? ''),
      product: String(fd.get('product') ?? ''),
      look: (fd.get('look') === 'world' ? 'world' : 'studio') as 'studio' | 'world',
      firstName: String(fd.get('firstName') ?? ''),
      intent: (['bestseller', 'launch'].includes(String(fd.get('intent'))) ? fd.get('intent') : 'general') as 'bestseller' | 'launch' | 'general',
      consent: fd.get('consent') === 'on',
      utm,
    };
  };

  for (const name of ['email', 'website', 'product']) {
    form.querySelector(`[name="${name}"]`)?.addEventListener('blur', () => {
      const r = leadSchema.safeParse({ ...read(), files: [] });
      const errs = r.success ? {} : fieldErrors(r.error);
      const val = (form.querySelector<HTMLInputElement>(`[name="${name}"]`)?.value ?? '').trim();
      if (val) setError(form, name, errs[name] ?? '');
    });
  }

  const button = form.querySelector<HTMLButtonElement>('button[type="submit"]');
  const status = form.querySelector<HTMLElement>('[data-status]');
  const summary = form.querySelector<HTMLElement>('[data-summary]');
  const label = button?.textContent ?? '';

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (form.dataset['busy']) return;
    const hp = (form.querySelector<HTMLInputElement>('[name="company_url"]')?.value ?? '').trim();
    const raw = [...(fileInput?.files ?? [])];
    const base = read();
    const metaFiles = raw.slice(0, MAX_FILES).map((f) => ({ type: 'image/webp' as const, size: Math.min(f.size, 1) }));
    const parsed = leadSchema.safeParse({ ...base, files: metaFiles });
    ['email', 'website', 'product', 'consent', 'photos'].forEach((n) => setError(form, n, ''));
    if (raw.length > MAX_FILES || raw.some((f) => f.size > MAX_CLIENT_FILE_BYTES)) {
      setError(form, 'photos', raw.length > MAX_FILES ? `Up to ${MAX_FILES} photos, please.` : MESSAGES.fileSize);
    }
    if (!parsed.success) {
      const errs = fieldErrors(parsed.error);
      Object.entries(errs).forEach(([k, m]) => setError(form, k, m));
      if (summary) {
        summary.hidden = false;
        summary.textContent = `Check ${Object.keys(errs).length === 1 ? 'one field' : `${Object.keys(errs).length} fields`}: ${Object.values(errs).join(' ')}`;
        summary.focus();
      }
      const first = form.querySelector<HTMLElement>('[aria-invalid="true"]');
      first?.focus();
      track('form_submit', { ok: false, error_code: 'invalid' });
      return;
    }
    if (summary) summary.hidden = true;
    form.dataset['busy'] = '1';
    if (button) {
      button.disabled = true;
      button.textContent = 'Sending… (big photos take a few seconds)';
    }
    const fail = (msg: string): void => {
      delete form.dataset['busy'];
      if (button) {
        button.disabled = false;
        button.textContent = label;
      }
      if (status) status.textContent = msg;
      track('form_submit', { ok: false, error_code: 'network' });
    };
    try {
      const blobs = (await Promise.all(raw.slice(0, MAX_FILES).map(resize))).filter((b): b is Blob => !!b);
      const files = blobs.map((b) => ({ type: b.type as 'image/webp' | 'image/jpeg', size: b.size }));
      const lead = { ...base, files };
      const token = (form.querySelector<HTMLInputElement>('[name="turnstileToken"]')?.value ?? '');
      const start = await fetch('/api/lead/start', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ lead, hp, elapsed: Date.now() - t0, turnstileToken: token }),
      });
      if (!start.ok) {
        const j = (await start.json().catch(() => ({}))) as { errors?: Record<string, string> };
        if (j.errors) Object.entries(j.errors).forEach(([k, m]) => setError(form, k, m));
        return fail("That didn't go through. Check the fields above and try again.");
      }
      const { id, token: upToken } = (await start.json()) as { id: string; token: string };
      let uploaded = 0;
      for (const [n, b] of blobs.entries()) {
        const r = await fetch(`/api/lead/upload?id=${encodeURIComponent(id)}&n=${n}&token=${encodeURIComponent(upToken)}`, {
          method: 'PUT',
          headers: { 'content-type': b.type },
          body: b,
        }).catch(() => null);
        if (r?.ok) uploaded++;
        else setError(form, 'photos', MESSAGES.upload);
      }
      if (blobs.length) track('form_upload', { files: uploaded, kb_total: Math.round(blobs.reduce((a, b) => a + b.size, 0) / 1024) });
      const fin = await fetch('/api/lead/finish', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ id, token: upToken, lead, uploaded }),
      });
      if (!fin.ok) return fail("That didn't go through. Try again in a moment.");
      track('form_submit', { ok: true });
      const next = new URLSearchParams(location.search).get('next') === 'call' ? '&next=call' : '';
      location.assign(`/frames/thanks?id=${encodeURIComponent(id)}&t=${encodeURIComponent(upToken)}${next}`);
    } catch {
      fail("We couldn't reach the studio. Check your connection and try again.");
    }
  });
}

function mountQualify(form: HTMLFormElement): void {
  const params = new URLSearchParams(location.search);
  const status = form.querySelector<HTMLElement>('[data-status]');
  if (params.get('next') === 'call') form.querySelector<HTMLInputElement>('[name="next"][value="call"]')?.click();
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(form);
    const data = qualifySchema.safeParse({
      runs: fd.getAll('runs').map(String),
      win: String(fd.get('win') ?? ''),
      hardest: String(fd.get('hardest') ?? ''),
      spend: String(fd.get('spend') ?? ''),
      next: String(fd.get('next') ?? ''),
    });
    if (!data.success) {
      if (status) status.textContent = 'Something looks off. Check your answers?';
      return;
    }
    const r = await fetch('/api/lead/qualify', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ id: params.get('id') ?? '', token: params.get('t') ?? '', answers: data.data }),
    }).catch(() => null);
    if (status) status.textContent = r?.ok ? 'Thanks. That helps us aim the frames.' : "Couldn't save that. Your frames are still on the way.";
  });
}
