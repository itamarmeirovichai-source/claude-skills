// Private access gate for the Cloudflare Pages deployment. Every request needs a session
// cookie that only someone who knows PEAKFORM_PASSWORD can get. The password is stored as
// an encrypted environment variable in Cloudflare, never in this repository.
//
// The login page is on the same origin, so it also works inside an iPhone Home Screen app,
// where a redirect to another site would open outside the app.

export interface GateEnv {
  PEAKFORM_PASSWORD?: string;
}

export const COOKIE_NAME = 'pf_gate';
export const LOGIN_PATH = '/__gate';
export const MIN_PASSWORD_LENGTH = 12;
const COOKIE_MAX_AGE = 60 * 60 * 24 * 365;
const TOKEN_LABEL = 'peakform-gate-v1';

const enc = new TextEncoder();

async function hmacHex(key: string, message: string): Promise<string> {
  const k = await crypto.subtle.importKey('raw', enc.encode(key), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = new Uint8Array(await crypto.subtle.sign('HMAC', k, enc.encode(message)));
  return [...sig].map((b) => b.toString(16).padStart(2, '0')).join('');
}

/** The session token. Changing the password in Cloudflare signs everyone out. */
export function sessionToken(password: string): Promise<string> {
  return hmacHex(password, TOKEN_LABEL);
}

/** Compares two strings without leaking where they differ, by comparing keyed hashes. */
async function sameSecret(a: string, b: string): Promise<boolean> {
  const [x, y] = await Promise.all([hmacHex(TOKEN_LABEL, a), hmacHex(TOKEN_LABEL, b)]);
  let diff = 0;
  for (let i = 0; i < x.length; i++) diff |= x.charCodeAt(i) ^ y.charCodeAt(i);
  return diff === 0;
}

function readCookie(request: Request, name: string): string | null {
  const header = request.headers.get('Cookie') ?? '';
  for (const part of header.split(';')) {
    const [k, ...v] = part.trim().split('=');
    if (k === name) return v.join('=');
  }
  return null;
}

const PRIVATE_HEADERS = {
  'Cache-Control': 'no-store',
  'X-Robots-Tag': 'noindex, nofollow',
  'Referrer-Policy': 'no-referrer',
  'X-Content-Type-Options': 'nosniff',
  'X-Frame-Options': 'DENY',
};

export function loginPage(wrong: boolean): Response {
  const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<meta name="color-scheme" content="light dark">
<title>PeakForm</title>
<style>
  :root { --bg: #f4f3ef; --surface: #fff; --text: #16191c; --muted: #5f676f; --accent: #245f4f; --line: #cfd2cc; --danger: #b3261e; }
  @media (prefers-color-scheme: dark) { :root { --bg: #0e1113; --surface: #171b1e; --text: #eceff1; --muted: #9aa3ab; --accent: #6cc0a5; --line: #2c3339; --danger: #ff8a7d; } }
  * { box-sizing: border-box; }
  body { margin: 0; min-height: 100dvh; display: grid; place-items: center; background: var(--bg); color: var(--text);
    font: -apple-system-body; font-family: -apple-system, system-ui, sans-serif;
    padding: max(24px, env(safe-area-inset-top)) 16px max(24px, env(safe-area-inset-bottom)); }
  main { width: 100%; max-width: 360px; }
  h1 { font-size: 1.6rem; margin: 0 0 8px; }
  p { color: var(--muted); margin: 0 0 20px; line-height: 1.4; }
  label { display: block; font-weight: 600; font-size: 0.9rem; margin-bottom: 6px; }
  input { width: 100%; min-height: 48px; padding: 10px 12px; font-size: 16px; border-radius: 10px; border: 1px solid var(--line); background: var(--surface); color: var(--text); }
  button { margin-top: 14px; width: 100%; min-height: 50px; border: 0; border-radius: 12px; background: var(--accent); color: var(--bg); font-size: 1.05rem; font-weight: 650; }
  .error { color: var(--danger); margin: 10px 0 0; }
</style>
</head>
<body>
<main>
  <h1>PeakForm</h1>
  <p>This copy of PeakForm is private. Enter the password to open it.</p>
  <form method="post" action="${LOGIN_PATH}">
    <label for="password">Password</label>
    <input id="password" name="password" type="password" autocomplete="current-password" required autofocus>
    ${wrong ? '<p class="error" role="alert">That password is not right.</p>' : ''}
    <button type="submit">Open PeakForm</button>
  </form>
</main>
</body>
</html>`;
  // 401, never 200, so the service worker can never cache this page in place of the app.
  return new Response(html, { status: 401, headers: { 'Content-Type': 'text/html; charset=utf-8', ...PRIVATE_HEADERS } });
}

export interface GateOptions {
  /** Pause after a wrong password, to slow down guessing. */
  wrongPasswordDelayMs?: number;
}

export async function gate(request: Request, env: GateEnv, next: () => Promise<Response>, opts: GateOptions = {}): Promise<Response> {
  const password = env.PEAKFORM_PASSWORD ?? '';
  // Fail closed: without a proper password configured, nothing is served.
  if (password.length < MIN_PASSWORD_LENGTH) {
    return new Response(`PeakForm is locked. Set PEAKFORM_PASSWORD, at least ${MIN_PASSWORD_LENGTH} characters, in the Cloudflare project settings, then deploy again.`, {
      status: 503,
      headers: { 'Content-Type': 'text/plain; charset=utf-8', ...PRIVATE_HEADERS },
    });
  }
  const url = new URL(request.url);

  if (url.pathname === LOGIN_PATH) {
    if (request.method !== 'POST') return loginPage(false);
    const given = await request
      .formData()
      .then((f) => String(f.get('password') ?? ''))
      .catch(() => '');
    if (await sameSecret(given, password)) {
      return new Response(null, {
        status: 303,
        headers: {
          Location: '/',
          'Set-Cookie': `${COOKIE_NAME}=${await sessionToken(password)}; Path=/; Max-Age=${COOKIE_MAX_AGE}; HttpOnly; Secure; SameSite=Lax`,
          ...PRIVATE_HEADERS,
        },
      });
    }
    const delay = opts.wrongPasswordDelayMs ?? 1000;
    if (delay > 0) await new Promise((r) => setTimeout(r, delay));
    return loginPage(true);
  }

  const cookie = readCookie(request, COOKIE_NAME);
  if (cookie && (await sameSecret(cookie, await sessionToken(password)))) {
    const res = await next();
    const out = new Response(res.body, res);
    out.headers.set('X-Robots-Tag', 'noindex, nofollow');
    out.headers.set('Referrer-Policy', 'no-referrer');
    out.headers.set('X-Content-Type-Options', 'nosniff');
    return out;
  }
  return loginPage(false);
}
