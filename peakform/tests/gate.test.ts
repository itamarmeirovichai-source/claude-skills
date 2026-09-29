import { describe, expect, it } from 'vitest';
import { COOKIE_NAME, LOGIN_PATH, gate, sessionToken } from '../edge/gate';

const PASSWORD = 'correct horse battery';
const env = { PEAKFORM_PASSWORD: PASSWORD };
const app = async () => new Response('<html>app</html>', { status: 200, headers: { 'Content-Type': 'text/html' } });
const noDelay = { wrongPasswordDelayMs: 0 };

function login(password: string) {
  const body = new URLSearchParams({ password });
  return new Request(`https://peakform.example${LOGIN_PATH}`, { method: 'POST', body, headers: { 'Content-Type': 'application/x-www-form-urlencoded' } });
}

describe('private access gate', () => {
  it('fails closed when no password is configured', async () => {
    const res = await gate(new Request('https://peakform.example/'), {}, app, noDelay);
    expect(res.status).toBe(503);
    expect(await res.text()).not.toContain('app');
  });

  it('fails closed when the configured password is too short', async () => {
    const res = await gate(new Request('https://peakform.example/'), { PEAKFORM_PASSWORD: 'short' }, app, noDelay);
    expect(res.status).toBe(503);
  });

  it('shows the login page with a 401 and never the app without a session', async () => {
    for (const path of ['/', '/index.html', '/sw.js', '/assets/index.js', '/manifest.webmanifest']) {
      const res = await gate(new Request(`https://peakform.example${path}`), env, app, noDelay);
      expect(res.status).toBe(401);
      const text = await res.text();
      expect(text).toContain('This copy of PeakForm is private');
      expect(text).not.toContain('<html>app</html>');
      expect(res.headers.get('Cache-Control')).toBe('no-store');
    }
  });

  it('rejects a wrong password and a forged cookie', async () => {
    const wrong = await gate(login('not the password'), env, app, noDelay);
    expect(wrong.status).toBe(401);
    expect(await wrong.text()).toContain('That password is not right');
    expect(wrong.headers.get('Set-Cookie')).toBeNull();

    const forged = new Request('https://peakform.example/', { headers: { Cookie: `${COOKIE_NAME}=${'0'.repeat(64)}` } });
    expect((await gate(forged, env, app, noDelay)).status).toBe(401);
  });

  it('signs in with the right password and then serves the app', async () => {
    const res = await gate(login(PASSWORD), env, app, noDelay);
    expect(res.status).toBe(303);
    expect(res.headers.get('Location')).toBe('/');
    const cookie = res.headers.get('Set-Cookie') ?? '';
    expect(cookie).toMatch(new RegExp(`^${COOKIE_NAME}=[0-9a-f]{64};`));
    expect(cookie).toContain('HttpOnly');
    expect(cookie).toContain('Secure');
    expect(cookie).not.toContain(PASSWORD);

    const token = cookie.split(';')[0]!.split('=')[1]!;
    const page = await gate(new Request('https://peakform.example/', { headers: { Cookie: `other=1; ${COOKIE_NAME}=${token}` } }), env, app, noDelay);
    expect(page.status).toBe(200);
    expect(await page.text()).toBe('<html>app</html>');
    expect(page.headers.get('X-Robots-Tag')).toContain('noindex');
  });

  it('signs everyone out when the password changes', async () => {
    const oldToken = await sessionToken(PASSWORD);
    const req = new Request('https://peakform.example/', { headers: { Cookie: `${COOKIE_NAME}=${oldToken}` } });
    expect((await gate(req, { PEAKFORM_PASSWORD: 'a different long password' }, app, noDelay)).status).toBe(401);
  });

  it('shows the form, not an error, for a plain visit to the login path', async () => {
    const res = await gate(new Request(`https://peakform.example${LOGIN_PATH}`), env, app, noDelay);
    expect(res.status).toBe(401);
    expect(await res.text()).toContain('<form method="post"');
  });
});
