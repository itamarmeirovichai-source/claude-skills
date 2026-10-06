import { useEffect, useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../db/db';
import { dateKey, type DateKey } from '../domain/dates';
import type { PlanRecord } from '../db/records';
import { useSettings } from './state';
import { registerCustomExercises } from '../content/library';
import type { DayOptions, MealSlot } from '../content/meals';
import { getAthlete } from '../db/repo';
import { DEFAULT_ATHLETE, type AthleteProfile } from '../domain/athlete';

/** Today's date key, refreshed when the app returns to the foreground or the day changes. */
export function useToday(): DateKey {
  const [d, setD] = useState(dateKey());
  useEffect(() => {
    const tick = () => setD(dateKey());
    const iv = window.setInterval(tick, 60_000);
    document.addEventListener('visibilitychange', tick);
    return () => {
      window.clearInterval(iv);
      document.removeEventListener('visibilitychange', tick);
    };
  }, []);
  return d;
}

export function usePlan(): PlanRecord | undefined {
  const s = useSettings();
  return useLiveQuery(() => db.plans.get(s.activePlanId), [s.activePlanId]);
}

export function useCustomExercises(): void {
  const list = useLiveQuery(() => db.customExercises.toArray(), []);
  useEffect(() => {
    if (list) registerCustomExercises(list);
  }, [list]);
}

export function fmtKg(n: number | null | undefined, unit: 'kg' | 'lb' = 'kg'): string {
  if (n === null || n === undefined) return 'none';
  const v = unit === 'lb' ? n * 2.20462 : n;
  return `${Math.round(v * 10) / 10} ${unit}`;
}

export function fmtTime(ms: number, clock: '24h' | '12h' = '24h'): string {
  return new Intl.DateTimeFormat(undefined, { hour: '2-digit', minute: '2-digit', hour12: clock === '12h' }).format(new Date(ms));
}

export function fmtHhmm(hhmm: string, clock: '24h' | '12h' = '24h'): string {
  if (clock === '24h') return hhmm;
  const [h, m] = hhmm.split(':').map(Number);
  const hh = ((h ?? 0) % 12) || 12;
  return `${hh}:${String(m ?? 0).padStart(2, '0')} ${(h ?? 0) < 12 ? 'am' : 'pm'}`;
}

export function round(n: number, step = 1): number {
  return Math.round(n / step) * step;
}

/** The athlete profile, with cautious defaults while it loads. */
export function useAthlete(): AthleteProfile {
  return useLiveQuery(() => getAthlete(), []) ?? DEFAULT_ATHLETE;
}

/** Meal times from the reminders and the family's meat and dairy interval, for the example meals. */
export function useMealOptions(): DayOptions {
  const s = useSettings();
  const a = useAthlete();
  const times: Partial<Record<MealSlot, string>> = {};
  for (const slot of ['breakfast', 'lunch', 'preworkout', 'dinner'] as const) {
    const r = s.reminders.find((x) => x.id === slot);
    if (r) times[slot] = r.time;
  }
  const milk = s.reminders.find((x) => x.id === 'milk');
  if (milk) times.evening = milk.time;
  return { times, meatToDairyHours: a.kosher.enabled ? a.kosher.meatToDairyHours : null };
}
