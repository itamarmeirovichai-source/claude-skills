import type { AppSettings } from '../db/records';
import { addDays, hhmmOf, localDateTime, minutesOf, parseKey, weekdayOf, type DateKey } from './dates';

// Sabbath Mode. Times come from the user's own entry, or are calculated locally from a
// chosen city. No location is requested or shared. Calculated times are approximate:
// the user should follow their community's calendar.

export interface City {
  id: string;
  name: string;
  lat: number;
  lon: number;
  tz: string;
  candleOffsetMin: number;
  endOffsetMin: number;
}

export const CITIES: City[] = [
  { id: 'jerusalem', name: 'Jerusalem', lat: 31.778, lon: 35.235, tz: 'Asia/Jerusalem', candleOffsetMin: 40, endOffsetMin: 40 },
  { id: 'tel-aviv', name: 'Tel Aviv', lat: 32.085, lon: 34.782, tz: 'Asia/Jerusalem', candleOffsetMin: 20, endOffsetMin: 40 },
  { id: 'haifa', name: 'Haifa', lat: 32.794, lon: 34.99, tz: 'Asia/Jerusalem', candleOffsetMin: 30, endOffsetMin: 40 },
  { id: 'beer-sheva', name: 'Beer Sheva', lat: 31.252, lon: 34.791, tz: 'Asia/Jerusalem', candleOffsetMin: 20, endOffsetMin: 40 },
  { id: 'bnei-brak', name: 'Bnei Brak', lat: 32.081, lon: 34.833, tz: 'Asia/Jerusalem', candleOffsetMin: 20, endOffsetMin: 40 },
  { id: 'petah-tikva', name: 'Petah Tikva', lat: 32.087, lon: 34.887, tz: 'Asia/Jerusalem', candleOffsetMin: 20, endOffsetMin: 40 },
  { id: 'netanya', name: 'Netanya', lat: 32.332, lon: 34.86, tz: 'Asia/Jerusalem', candleOffsetMin: 20, endOffsetMin: 40 },
  { id: 'ashdod', name: 'Ashdod', lat: 31.804, lon: 34.655, tz: 'Asia/Jerusalem', candleOffsetMin: 20, endOffsetMin: 40 },
  { id: 'modiin', name: "Modi'in", lat: 31.898, lon: 35.01, tz: 'Asia/Jerusalem', candleOffsetMin: 20, endOffsetMin: 40 },
  { id: 'eilat', name: 'Eilat', lat: 29.557, lon: 34.952, tz: 'Asia/Jerusalem', candleOffsetMin: 20, endOffsetMin: 40 },
  { id: 'new-york', name: 'New York', lat: 40.713, lon: -74.006, tz: 'America/New_York', candleOffsetMin: 18, endOffsetMin: 50 },
  { id: 'los-angeles', name: 'Los Angeles', lat: 34.052, lon: -118.244, tz: 'America/Los_Angeles', candleOffsetMin: 18, endOffsetMin: 50 },
  { id: 'toronto', name: 'Toronto', lat: 43.653, lon: -79.383, tz: 'America/Toronto', candleOffsetMin: 18, endOffsetMin: 50 },
  { id: 'london', name: 'London', lat: 51.507, lon: -0.128, tz: 'Europe/London', candleOffsetMin: 18, endOffsetMin: 50 },
  { id: 'paris', name: 'Paris', lat: 48.857, lon: 2.352, tz: 'Europe/Paris', candleOffsetMin: 18, endOffsetMin: 50 },
];

const rad = (d: number) => (d * Math.PI) / 180;
const deg = (r: number) => (r * 180) / Math.PI;

/** Sunset in minutes after UTC midnight for a calendar date, using the NOAA approximation. */
export function sunsetUtcMinutes(key: DateKey, lat: number, lon: number): number | null {
  const { y, m, d } = parseKey(key);
  const start = Date.UTC(y, 0, 1);
  const n = Math.round((Date.UTC(y, m - 1, d) - start) / 86400000) + 1;
  const daysInYear = (y % 4 === 0 && y % 100 !== 0) || y % 400 === 0 ? 366 : 365;
  const g = ((2 * Math.PI) / daysInYear) * (n - 1);
  const eqtime = 229.18 * (0.000075 + 0.001868 * Math.cos(g) - 0.032077 * Math.sin(g) - 0.014615 * Math.cos(2 * g) - 0.040849 * Math.sin(2 * g));
  const decl =
    0.006918 - 0.399912 * Math.cos(g) + 0.070257 * Math.sin(g) - 0.006758 * Math.cos(2 * g) + 0.000907 * Math.sin(2 * g) - 0.002697 * Math.cos(3 * g) + 0.00148 * Math.sin(3 * g);
  const cosHa = Math.cos(rad(90.833)) / (Math.cos(rad(lat)) * Math.cos(decl)) - Math.tan(rad(lat)) * Math.tan(decl);
  if (cosHa < -1 || cosHa > 1) return null;
  const ha = deg(Math.acos(cosHa));
  return 720 - 4 * (lon - ha) - eqtime;
}

/** Local HH:MM of sunset in the city's own time zone. Daylight saving is handled by Intl. */
export function sunsetLocal(key: DateKey, city: City): string | null {
  const utcMin = sunsetUtcMinutes(key, city.lat, city.lon);
  if (utcMin === null) return null;
  const { y, m, d } = parseKey(key);
  const ms = Date.UTC(y, m - 1, d) + utcMin * 60000;
  return new Intl.DateTimeFormat('en-GB', { timeZone: city.tz, hour: '2-digit', minute: '2-digit', hour12: false }).format(new Date(ms));
}

export interface SabbathWindow {
  friday: DateKey;
  saturday: DateKey;
  start: string; // HH:MM on Friday
  end: string; // HH:MM on Saturday
  startMs: number;
  endMs: number;
  source: 'manual' | 'city';
}

/** The Friday on or before a date (for Saturday) or the coming Friday for other days. */
export function fridayFor(key: DateKey): DateKey {
  const wd = weekdayOf(key);
  if (wd === 6) return addDays(key, -1);
  return addDays(key, (5 - wd + 7) % 7);
}

export function sabbathWindow(friday: DateKey, s: AppSettings['sabbath']): SabbathWindow {
  const saturday = addDays(friday, 1);
  let start = s.fridayStart;
  let end = s.saturdayEnd;
  let source: SabbathWindow['source'] = 'manual';
  if (s.mode === 'city' && s.cityId) {
    const city = CITIES.find((c) => c.id === s.cityId);
    const fri = city ? sunsetLocal(friday, city) : null;
    const sat = city ? sunsetLocal(saturday, city) : null;
    if (fri && sat) {
      start = hhmmOf(minutesOf(fri) - s.candleOffsetMin);
      end = hhmmOf(minutesOf(sat) + s.endOffsetMin);
      source = 'city';
    }
  }
  return {
    friday,
    saturday,
    start,
    end,
    startMs: localDateTime(friday, start).getTime(),
    endMs: localDateTime(saturday, end).getTime(),
    source,
  };
}

/** True when an instant falls inside the Sabbath window and Sabbath Mode is on. */
export function isSabbathAt(ms: number, key: DateKey, s: AppSettings['sabbath']): boolean {
  if (!s.enabled) return false;
  const wd = weekdayOf(key);
  if (wd !== 5 && wd !== 6) return false;
  const w = sabbathWindow(fridayFor(key), s);
  return ms >= w.startMs && ms < w.endMs;
}

/** True when a wall clock time on a given date would fall inside the window. */
export function isSabbathTime(key: DateKey, hhmm: string, s: AppSettings['sabbath']): boolean {
  return isSabbathAt(localDateTime(key, hhmm).getTime(), key, s);
}
