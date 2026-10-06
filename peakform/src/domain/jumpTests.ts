import { z } from 'zod';

// Jump and reach tests (3.0.0). A standing reach and the best of three jump and reach attempts,
// marked on a wall with tape or chalk, in the same shoes, on the same surface, rested, after the same
// warm up. Two tests are only compared when they used the same method, surface, and shoes. Reaching
// a part of a basketball hoop is not a measurement, so PeakForm never estimates a jump from it.

const dateKey = z.string().regex(/^\d{4}-\d{2}-\d{2}$/);
const cm = z.number().min(50).max(450);

export const JumpTestSchema = z.object({
  id: z.string().min(1).max(40),
  date: dateKey,
  standingReachCm: cm.nullable(),
  /** Two foot jump and reach from standing, up to three attempts. */
  standingJumpCm: z.array(cm).max(3),
  /** Approach jump and reach, up to three attempts, only where the space is safe for it. */
  approachJumpCm: z.array(cm).max(3),
  method: z.enum(['wall-tape', 'chalk', 'vertec', 'other']),
  surface: z.string().max(40),
  shoes: z.string().max(40),
  note: z.string().max(200),
});
export type JumpTest = z.infer<typeof JumpTestSchema>;

export function parseTests(raw: unknown): JumpTest[] {
  const r = z.array(JumpTestSchema).safeParse(raw);
  return r.success ? [...r.data].sort((a, b) => a.date.localeCompare(b.date)) : [];
}

const best = (xs: number[]) => (xs.length ? Math.max(...xs) : null);

/** Jump height as the best reach minus standing reach. Null when either is missing. */
export function heights(t: JumpTest): { standing: number | null; approach: number | null } {
  const sr = t.standingReachCm;
  const s = best(t.standingJumpCm);
  const a = best(t.approachJumpCm);
  return { standing: sr !== null && s !== null ? s - sr : null, approach: sr !== null && a !== null ? a - sr : null };
}

/** Same method, surface, and shoes, so the numbers can be compared. */
export function comparable(a: JumpTest, b: JumpTest): boolean {
  const same = (x: string, y: string) => x.trim().toLowerCase() === y.trim().toLowerCase();
  return a.method === b.method && same(a.surface, b.surface) && same(a.shoes, b.shoes);
}

export interface JumpTrend {
  latest: JumpTest | null;
  /** The most recent earlier test under the same conditions. */
  previous: JumpTest | null;
  standingChange: number | null;
  approachChange: number | null;
  /** Differences of about 2 cm or less are within the usual day to day variation of this kind of test. */
  withinNoise: boolean;
}

export const NOISE_CM = 2;

export function jumpTrend(tests: JumpTest[]): JumpTrend {
  const sorted = [...tests].sort((a, b) => a.date.localeCompare(b.date));
  const latest = sorted[sorted.length - 1] ?? null;
  if (!latest) return { latest: null, previous: null, standingChange: null, approachChange: null, withinNoise: true };
  const previous = [...sorted.slice(0, -1)].reverse().find((t) => comparable(t, latest)) ?? null;
  if (!previous) return { latest, previous: null, standingChange: null, approachChange: null, withinNoise: true };
  const a = heights(latest);
  const b = heights(previous);
  const standingChange = a.standing !== null && b.standing !== null ? a.standing - b.standing : null;
  const approachChange = a.approach !== null && b.approach !== null ? a.approach - b.approach : null;
  const changes = [standingChange, approachChange].filter((x): x is number => x !== null);
  return { latest, previous, standingChange, approachChange, withinNoise: changes.every((c) => Math.abs(c) <= NOISE_CM) };
}
