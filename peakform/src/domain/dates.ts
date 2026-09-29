// Date helpers. Day based records use local calendar date keys (YYYY-MM-DD).
// Timestamps are stored as epoch milliseconds. Date key arithmetic is done in UTC
// so daylight saving changes never shift a day.

export type DateKey = string; // YYYY-MM-DD

const pad = (n: number) => String(n).padStart(2, '0');

export function dateKey(d: Date = new Date()): DateKey {
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

/** Date key for an instant in a specific IANA time zone. */
export function dateKeyInZone(ms: number, timeZone: string): DateKey {
  const parts = new Intl.DateTimeFormat('en-CA', { timeZone, year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(new Date(ms));
  const get = (t: string) => parts.find((p) => p.type === t)?.value ?? '';
  return `${get('year')}-${get('month')}-${get('day')}`;
}

export function parseKey(key: DateKey): { y: number; m: number; d: number } {
  const [y, m, d] = key.split('-').map(Number);
  if (!y || !m || !d) throw new Error(`Bad date key ${key}`);
  return { y, m, d };
}

export function keyToUtcMs(key: DateKey): number {
  const { y, m, d } = parseKey(key);
  return Date.UTC(y, m - 1, d);
}

export function addDays(key: DateKey, days: number): DateKey {
  const t = new Date(keyToUtcMs(key) + days * 86400000);
  return `${t.getUTCFullYear()}-${pad(t.getUTCMonth() + 1)}-${pad(t.getUTCDate())}`;
}

export function diffDays(a: DateKey, b: DateKey): number {
  return Math.round((keyToUtcMs(a) - keyToUtcMs(b)) / 86400000);
}

/** 0 = Sunday. */
export function weekdayOf(key: DateKey): 0 | 1 | 2 | 3 | 4 | 5 | 6 {
  return new Date(keyToUtcMs(key)).getUTCDay() as 0 | 1 | 2 | 3 | 4 | 5 | 6;
}

/**
 * Review weeks run Monday to Sunday so the Sunday evening review covers the full training week,
 * including Sunday's session.
 */
export function reviewWeekStart(key: DateKey): DateKey {
  const wd = weekdayOf(key);
  const back = wd === 0 ? 6 : wd - 1;
  return addDays(key, -back);
}

export function rangeKeys(start: DateKey, days: number): DateKey[] {
  return Array.from({ length: days }, (_, i) => addDays(start, i));
}

/** Local wall clock time for a date key and HH:MM in the device zone. Handles DST through Date. */
export function localDateTime(key: DateKey, hhmm: string): Date {
  const { y, m, d } = parseKey(key);
  const [hh, mm] = hhmm.split(':').map(Number);
  return new Date(y, m - 1, d, hh ?? 0, mm ?? 0, 0, 0);
}

export function minutesOf(hhmm: string): number {
  const [h, m] = hhmm.split(':').map(Number);
  return (h ?? 0) * 60 + (m ?? 0);
}

export function hhmmOf(minutes: number): string {
  const m = ((Math.round(minutes) % 1440) + 1440) % 1440;
  return `${pad(Math.floor(m / 60))}:${pad(m % 60)}`;
}

/** Sleep duration in minutes from bedtime to wake time, crossing midnight when needed. */
export function sleepMinutes(bed: string, wake: string): number {
  const b = minutesOf(bed);
  const w = minutesOf(wake);
  return w > b ? w - b : w + 1440 - b;
}

export const WEEKDAY_NAMES = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'] as const;
export const WEEKDAY_SHORT = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'] as const;

export function formatDateKey(key: DateKey, opts: Intl.DateTimeFormatOptions = { weekday: 'short', day: 'numeric', month: 'short' }, locale?: string): string {
  const { y, m, d } = parseKey(key);
  return new Intl.DateTimeFormat(locale, { ...opts, timeZone: 'UTC' }).format(new Date(Date.UTC(y, m - 1, d)));
}
