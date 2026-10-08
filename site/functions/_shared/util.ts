// Shared helpers for Pages Functions. Every binding/secret is optional: without them the
// Functions still validate and answer, they just don't store, verify or email.
export interface Env {
  UPLOADS?: R2Bucket;
  RATE_LIMIT?: KVNamespace;
  EVENTS?: AnalyticsEngineDataset;
  TURNSTILE_SECRET?: string;
  LEAD_SIGNING_SECRET?: string;
  RESEND_API_KEY?: string;
  MAIL_FROM?: string;
  NOTIFY_TO?: string;
}

export const json = (data: unknown, status = 200): Response =>
  new Response(JSON.stringify(data), { status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' } });

const enc = new TextEncoder();
// Without LEAD_SIGNING_SECRET a per-isolate key is used: fine for local dev, not for production.
let fallbackKey: string | null = null;
async function key(env: Env): Promise<CryptoKey> {
  fallbackKey ??= crypto.randomUUID();
  return crypto.subtle.importKey('raw', enc.encode(env.LEAD_SIGNING_SECRET || fallbackKey), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign', 'verify']);
}
const b64url = (buf: ArrayBuffer): string => btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');

/** Token = exp.hmac(id.exp). Valid for 1 hour. */
export async function sign(env: Env, id: string): Promise<string> {
  const exp = Math.floor(Date.now() / 1000) + 3600;
  const mac = await crypto.subtle.sign('HMAC', await key(env), enc.encode(`${id}.${exp}`));
  return `${exp}.${b64url(mac)}`;
}
export async function verify(env: Env, id: string, token: string): Promise<boolean> {
  const [expS, mac] = token.split('.');
  const exp = Number(expS);
  if (!mac || !Number.isFinite(exp) || exp < Date.now() / 1000) return false;
  const expect = await crypto.subtle.sign('HMAC', await key(env), enc.encode(`${id}.${exp}`));
  return b64url(expect) === mac;
}

export const ID_RE = /^[a-z0-9-]{8,64}$/;
export const newId = (): string => `${new Date().toISOString().slice(0, 10)}-${crypto.randomUUID().slice(0, 13)}`;

export async function turnstileOk(env: Env, token: string, ip: string | null): Promise<boolean> {
  if (!env.TURNSTILE_SECRET) return true; // not configured yet
  if (!token) return false;
  const body = new FormData();
  body.append('secret', env.TURNSTILE_SECRET);
  body.append('response', token);
  if (ip) body.append('remoteip', ip);
  try {
    const r = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', { method: 'POST', body });
    const j = (await r.json()) as { success?: boolean };
    return j.success === true;
  } catch {
    return false;
  }
}

/** ≤ 8 submits per hour per IP hash, when a KV namespace is bound. */
export async function rateLimited(env: Env, ip: string | null): Promise<boolean> {
  if (!env.RATE_LIMIT || !ip) return false;
  const h = b64url(await crypto.subtle.digest('SHA-256', enc.encode(ip))).slice(0, 16);
  const k = `rl:${h}:${new Date().toISOString().slice(0, 13)}`;
  const n = Number((await env.RATE_LIMIT.get(k)) ?? '0') + 1;
  await env.RATE_LIMIT.put(k, String(n), { expirationTtl: 3700 });
  return n > 8;
}

/** JPEG, PNG or WebP by magic bytes. */
export function imageType(b: Uint8Array): 'image/jpeg' | 'image/png' | 'image/webp' | null {
  if (b[0] === 0xff && b[1] === 0xd8 && b[2] === 0xff) return 'image/jpeg';
  if (b[0] === 0x89 && b[1] === 0x50 && b[2] === 0x4e && b[3] === 0x47) return 'image/png';
  if (b[0] === 0x52 && b[1] === 0x49 && b[2] === 0x46 && b[3] === 0x46 && b[8] === 0x57 && b[9] === 0x45 && b[10] === 0x42 && b[11] === 0x50) return 'image/webp';
  return null;
}

export async function sendMail(env: Env, to: string, subject: string, text: string, replyTo?: string): Promise<boolean> {
  if (!env.RESEND_API_KEY || !env.MAIL_FROM || !to) return false;
  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { authorization: `Bearer ${env.RESEND_API_KEY}`, 'content-type': 'application/json' },
      body: JSON.stringify({ from: env.MAIL_FROM, to: [to], subject, text, ...(replyTo ? { reply_to: replyTo } : {}) }),
    });
    return r.ok;
  } catch {
    return false;
  }
}
