// POST /api/lead/start  { lead, hp, elapsed, turnstileToken } → { id, token }
import { leadSchema, fieldErrors, MIN_FILL_MS } from '../../../src/lib/lead-schema';
import { json, newId, rateLimited, sign, turnstileOk, type Env } from '../../_shared/util';

export const onRequestPost: PagesFunction<Env> = async ({ request, env }) => {
  const body = (await request.json().catch(() => null)) as { lead?: unknown; hp?: unknown; elapsed?: unknown; turnstileToken?: unknown } | null;
  if (!body || typeof body !== 'object') return json({ ok: false, error: 'bad_request' }, 400);
  const ip = request.headers.get('cf-connecting-ip');
  // Honeypot or too-fast submit: answer like success, store nothing.
  if ((typeof body.hp === 'string' && body.hp.trim()) || (typeof body.elapsed === 'number' && body.elapsed < MIN_FILL_MS)) {
    return json({ ok: true, id: newId(), token: 'x.x' });
  }
  if (await rateLimited(env, ip)) return json({ ok: false, error: 'rate_limited' }, 429);
  if (!(await turnstileOk(env, typeof body.turnstileToken === 'string' ? body.turnstileToken : '', ip))) return json({ ok: false, error: 'turnstile' }, 403);
  const parsed = leadSchema.safeParse(body.lead);
  if (!parsed.success) return json({ ok: false, error: 'invalid', errors: fieldErrors(parsed.error) }, 422);
  const id = newId();
  const token = await sign(env, id);
  if (env.UPLOADS) {
    await env.UPLOADS.put(`leads/${id}/start.json`, JSON.stringify({ ...parsed.data, receivedAt: new Date().toISOString(), stage: 'start' }), {
      httpMetadata: { contentType: 'application/json' },
    });
  }
  return json({ ok: true, id, token, stored: !!env.UPLOADS });
};
