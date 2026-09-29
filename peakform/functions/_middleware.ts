// Cloudflare Pages runs this before every request. See edge/gate.ts.
import { gate, type GateEnv } from '../edge/gate';

interface PagesContext {
  request: Request;
  env: GateEnv;
  next: () => Promise<Response>;
}

export const onRequest = (ctx: PagesContext): Promise<Response> => gate(ctx.request, ctx.env, () => ctx.next());
