import type { DateKey } from './dates';

// Touch heights logged on approach jumps, in centimetres. Since 3.0.0 there is no dunk target or
// deadline: a touch on a set is a training note, and comparable progress comes from the jump tests.

/** Approach jumps that log the height touched. */
export const TOUCH_EXERCISES = ['approach-touch-jump', 'volleyball-approach-jump'] as const;

export interface Touch {
  date: DateKey;
  cm: number;
}

/** The best touch of each day, oldest first. Entries without a height are ignored. */
export function bestTouchPerDay(entries: Array<{ date: DateKey; reachCm: number | null | undefined }>): Touch[] {
  const best = new Map<DateKey, number>();
  for (const e of entries) {
    if (typeof e.reachCm !== 'number' || e.reachCm <= 0) continue;
    best.set(e.date, Math.max(best.get(e.date) ?? 0, e.reachCm));
  }
  return [...best.entries()].sort(([a], [b]) => a.localeCompare(b)).map(([date, cm]) => ({ date, cm }));
}
