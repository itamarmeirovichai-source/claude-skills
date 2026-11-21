// POST /api/lead/qualify { id, token, answers } → leads/<id>/qualify.json (optional step 2)
import { qualifySchema } from '../../../src/lib/lead-schema';
import { ID_RE, json, verify, type Env } from '../../_shared/util';

export const onRequestPost: PagesFunction<Env> = async ({ request, env }) => {
  const body = (await request.json().catch(() => null)) as { id?: string; token?: string; answers?: unknown } | null;
  const id = body?.id ?? '';
  if (!ID_RE.test(id) || !(await verify(env, id, body?.token ?? ''))) return json({ ok: false, error: 'token' }, 403);
  const parsed = qualifySchema.safeParse(body?.answers);
  if (!parsed.success) return json({ ok: false, error: 'invalid' }, 422);
  if (env.UPLOADS) await env.UPLOADS.put(`leads/${id}/qualify.json`, JSON.stringify(parsed.data), { httpMetadata: { contentType: 'application/json' } });
  return json({ ok: true, stored: !!env.UPLOADS });
};
