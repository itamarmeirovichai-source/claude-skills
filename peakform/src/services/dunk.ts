import { KV, exposuresFor, kvGet, kvSet } from '../db/repo';
import { DEFAULT_DUNK_PROFILE, TOUCH_EXERCISES, bestTouchPerDay, type DunkProfile, type Touch } from '../domain/dunk';

export async function getDunkProfile(): Promise<DunkProfile> {
  return { ...DEFAULT_DUNK_PROFILE, ...((await kvGet<Partial<DunkProfile>>(KV.dunkProfile)) ?? {}) };
}

export function saveDunkProfile(p: DunkProfile): Promise<void> {
  return kvSet(KV.dunkProfile, p);
}

/** The best logged touch height of each training day, from the approach jumps. */
export async function touchHistory(): Promise<Touch[]> {
  const all = await Promise.all(TOUCH_EXERCISES.map((id) => exposuresFor(id)));
  return bestTouchPerDay(all.flat().flatMap(({ session, sets }) => sets.map((s) => ({ date: session.date, reachCm: s.reachCm }))));
}
