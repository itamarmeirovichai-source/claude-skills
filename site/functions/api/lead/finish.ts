// POST /api/lead/finish { id, token, lead, uploaded } → writes lead.json, emails (optional)
import { leadSchema } from '../../../src/lib/lead-schema';
import { ID_RE, json, sendMail, verify, type Env } from '../../_shared/util';

export const onRequestPost: PagesFunction<Env> = async ({ request, env }) => {
  const body = (await request.json().catch(() => null)) as { id?: string; token?: string; lead?: unknown; uploaded?: number } | null;
  const id = body?.id ?? '';
  if (!ID_RE.test(id) || !(await verify(env, id, body?.token ?? ''))) return json({ ok: false, error: 'token' }, 403);
  const parsed = leadSchema.safeParse(body?.lead);
  if (!parsed.success) return json({ ok: false, error: 'invalid' }, 422);
  const lead = { id, ...parsed.data, uploaded: Math.max(0, Math.min(3, Number(body?.uploaded) || 0)), finishedAt: new Date().toISOString() };
  if (env.UPLOADS) {
    await env.UPLOADS.put(`leads/${id}/lead.json`, JSON.stringify(lead, null, 2), { httpMetadata: { contentType: 'application/json' } });
  }
  const summary = `New frames request\n\nEmail: ${lead.email}\nSite: ${lead.website}\nProduct: ${lead.product}\nLook: ${lead.look}\nIntent: ${lead.intent}\nName: ${lead.firstName}\nPhotos: ${lead.uploaded}\nUTM: ${JSON.stringify(lead.utm)}\nID: ${id}`;
  const alerted = env.NOTIFY_TO ? await sendMail(env, env.NOTIFY_TO, `Frames request: ${lead.product}`, summary, lead.email) : false;
  const replied = await sendMail(
    env,
    lead.email,
    'Your 5 frames are on the way',
    `Hi${lead.firstName ? ` ${lead.firstName}` : ''},\n\nThanks. Your frames for ${lead.product} land in your inbox in 3–5 business days, marked "AI concept".\n\nIf you like them, we talk film. If not, tell us what's off.\n`,
  );
  return json({ ok: true, stored: !!env.UPLOADS, alerted, replied });
};
