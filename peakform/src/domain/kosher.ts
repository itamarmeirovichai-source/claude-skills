import { FOOD_BY_ID } from '../content/foods';
import type { FoodLog } from '../db/records';
import { minutesOf } from './dates';

// The meat and dairy interval as a family setting. PeakForm takes no position on which custom is
// right; it only keeps the example meals and the gentle notes in line with the hours chosen.

export type Category = 'meat' | 'dairy' | 'pareve';

export function logCategory(l: Pick<FoodLog, 'items'>): Category {
  const cats = new Set(l.items.map((i) => (i.foodId ? FOOD_BY_ID[i.foodId]?.kosher : undefined) ?? 'pareve'));
  if (cats.has('meat')) return 'meat';
  if (cats.has('dairy')) return 'dairy';
  return 'pareve';
}

export interface IntervalNote {
  logId: string;
  /** Minutes between the meat and the dairy. */
  gapMin: number;
  text: string;
}

/** Dairy logged sooner after meat than the interval, on the same day. Information only, never a block. */
export function meatDairyNotes(logs: FoodLog[], hours: number | null): IntervalNote[] {
  if (hours === null) return [];
  const sorted = [...logs].sort((a, b) => minutesOf(a.time) - minutesOf(b.time));
  const out: IntervalNote[] = [];
  for (const l of sorted) {
    if (logCategory(l) !== 'dairy') continue;
    const meat = sorted.filter((m) => logCategory(m) === 'meat' && m.date === l.date && minutesOf(m.time) <= minutesOf(l.time));
    const last = meat[meat.length - 1];
    if (!last) continue;
    const gap = minutesOf(l.time) - minutesOf(last.time);
    if (gap < hours * 60) out.push({ logId: l.id, gapMin: gap, text: `Dairy at ${l.time} came ${Math.floor(gap / 60)} h ${gap % 60} min after meat at ${last.time}, sooner than your ${hours} hour interval.` });
  }
  return out;
}

/** The earliest time dairy fits after the last meat logged today, or null when no meat was logged. */
export function dairyFrom(logs: FoodLog[], hours: number | null): string | null {
  if (hours === null) return null;
  const meat = logs.filter((l) => logCategory(l) === 'meat').map((l) => minutesOf(l.time));
  if (!meat.length) return null;
  const t = Math.max(...meat) + Math.round(hours * 60);
  if (t >= 24 * 60) return null;
  return `${String(Math.floor(t / 60)).padStart(2, '0')}:${String(t % 60).padStart(2, '0')}`;
}
