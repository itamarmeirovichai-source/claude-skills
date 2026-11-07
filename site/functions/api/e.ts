// POST /api/e  cookieless analytics beacon → Analytics Engine (if bound). Stores no IP, no IDs.
import { type Env } from '../_shared/util';

export const onRequestPost: PagesFunction<Env> = async ({ request, env }) => {
  const b = (await request.json().catch(() => null)) as { n?: unknown; p?: Record<string, unknown>; path?: unknown } | null;
  const name = typeof b?.n === 'string' ? b.n.slice(0, 40) : '';
  if (name && env.EVENTS) {
    const props = Object.entries(b?.p ?? {}).slice(0, 6).map(([k, v]) => `${k}=${String(v).slice(0, 40)}`).join('&');
    env.EVENTS.writeDataPoint({ blobs: [name, typeof b?.path === 'string' ? b.path.slice(0, 80) : '', props], indexes: [name] });
  }
  return new Response(null, { status: 204 });
};
