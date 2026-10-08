// PUT /api/lead/upload?id=&n=&token=  (raw image body, ≤ 4 MB, JPEG/PNG/WebP by magic bytes)
import { MAX_FILES, MAX_UPLOAD_BYTES } from '../../../src/lib/lead-schema';
import { ID_RE, imageType, json, verify, type Env } from '../../_shared/util';

export const onRequestPut: PagesFunction<Env> = async ({ request, env }) => {
  const u = new URL(request.url);
  const id = u.searchParams.get('id') ?? '';
  const n = Number(u.searchParams.get('n'));
  const token = u.searchParams.get('token') ?? '';
  if (!ID_RE.test(id) || !Number.isInteger(n) || n < 0 || n >= MAX_FILES) return json({ ok: false, error: 'bad_request' }, 400);
  if (!(await verify(env, id, token))) return json({ ok: false, error: 'token' }, 403);
  const len = Number(request.headers.get('content-length') ?? '0');
  if (len > MAX_UPLOAD_BYTES) return json({ ok: false, error: 'too_big' }, 413);
  const buf = new Uint8Array(await request.arrayBuffer());
  if (buf.byteLength === 0 || buf.byteLength > MAX_UPLOAD_BYTES) return json({ ok: false, error: 'too_big' }, 413);
  const type = imageType(buf);
  if (!type) return json({ ok: false, error: 'type' }, 415);
  const ext = type.split('/')[1];
  if (env.UPLOADS) await env.UPLOADS.put(`leads/${id}/photo-${n}.${ext}`, buf, { httpMetadata: { contentType: type } });
  return json({ ok: true, stored: !!env.UPLOADS });
};
