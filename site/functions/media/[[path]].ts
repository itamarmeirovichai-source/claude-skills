// GET/HEAD /media/* : serve the static file when the build has it (Direct Upload with local media);
// otherwise, when the R2 `MEDIA` binding exists, stream `media/<path>` from it with Range support
// (video needs 206 responses, Safari especially). public/media is git-ignored, so a Git-connected
// Pages build has no media until it is uploaded to that bucket (see DEPLOY_OWNER.md).
import type { Env } from '../_shared/util';

const TYPES: Record<string, string> = { mp4: 'video/mp4', webp: 'image/webp', jpg: 'image/jpeg', png: 'image/png', json: 'application/json', vtt: 'text/vtt', mp3: 'audio/mpeg', m4a: 'audio/mp4' };

async function serve(ctx: EventContext<Env, 'path', Record<string, unknown>>, head: boolean): Promise<Response> {
  const res = await ctx.next();
  if (res.status !== 404 || !ctx.env.MEDIA) return res;
  const parts = Array.isArray(ctx.params.path) ? ctx.params.path : [ctx.params.path];
  const rel = parts.join('/');
  if (!rel || rel.includes('..')) return res;
  const key = `media/${rel}`;
  const ext = rel.split('.').pop()?.toLowerCase() ?? '';
  const headers = new Headers({
    'content-type': TYPES[ext] ?? 'application/octet-stream',
    'accept-ranges': 'bytes',
    'cache-control': 'public, max-age=86400, stale-while-revalidate=604800',
    'x-content-type-options': 'nosniff',
  });
  if (head) {
    const meta = await ctx.env.MEDIA.head(key);
    if (!meta) return res;
    headers.set('content-length', String(meta.size));
    headers.set('etag', meta.httpEtag);
    return new Response(null, { status: 200, headers });
  }
  const range = ctx.request.headers.get('range');
  const obj = await ctx.env.MEDIA.get(key, range ? { range: ctx.request.headers } : {});
  if (!obj) return res;
  headers.set('etag', obj.httpEtag);
  if (range && obj.range && 'offset' in obj.range) {
    const offset = obj.range.offset ?? 0;
    const length = obj.range.length ?? obj.size - offset;
    headers.set('content-range', `bytes ${offset}-${offset + length - 1}/${obj.size}`);
    headers.set('content-length', String(length));
    return new Response(obj.body, { status: 206, headers });
  }
  headers.set('content-length', String(obj.size));
  return new Response(obj.body, { status: 200, headers });
}

export const onRequestGet: PagesFunction<Env, 'path'> = (ctx) => serve(ctx, false);
export const onRequestHead: PagesFunction<Env, 'path'> = (ctx) => serve(ctx, true);
