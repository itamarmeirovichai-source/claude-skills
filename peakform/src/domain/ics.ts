import type { AppSettings, Reminder } from '../db/records';
import { addDays, parseKey, weekdayOf, type DateKey } from './dates';
import { isSabbathTime } from './sabbath';

// Apple Calendar compatible reminder calendar. Events use floating local times, so they
// follow the phone's clock and daylight saving changes. Each reminder is one weekly
// recurring event with an alarm. Sabbath occurrences are removed with EXDATE.

const BYDAY = ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'];
const pad = (n: number) => String(n).padStart(2, '0');

export function escapeText(s: string): string {
  return s.replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\r?\n/g, '\\n');
}

/** Fold lines longer than 75 octets as RFC 5545 requires. */
export function foldLine(line: string): string {
  const bytes = new TextEncoder().encode(line);
  if (bytes.length <= 75) return line;
  const out: string[] = [];
  let cur = '';
  let curBytes = 0;
  for (const ch of line) {
    const b = new TextEncoder().encode(ch).length;
    const limit = out.length === 0 ? 75 : 74;
    if (curBytes + b > limit) {
      out.push(cur);
      cur = '';
      curBytes = 0;
    }
    cur += ch;
    curBytes += b;
  }
  out.push(cur);
  return out.join('\r\n ');
}

function floating(key: DateKey, hhmm: string): string {
  const { y, m, d } = parseKey(key);
  return `${y}${pad(m)}${pad(d)}T${hhmm.replace(':', '')}00`;
}

function utcStamp(ms: number): string {
  const d = new Date(ms);
  return `${d.getUTCFullYear()}${pad(d.getUTCMonth() + 1)}${pad(d.getUTCDate())}T${pad(d.getUTCHours())}${pad(d.getUTCMinutes())}${pad(d.getUTCSeconds())}Z`;
}

export interface IcsOptions {
  today: DateKey;
  weeks: number;
  now: number;
  sequence: number;
  calName: string;
}

export interface IcsResult {
  text: string;
  eventCount: number;
  excludedCount: number;
  untilDate: DateKey;
}

export function effectiveReminders(settings: AppSettings): Reminder[] {
  return settings.reminders.filter((r) => r.enabled && r.weekdays.length > 0);
}

export function buildIcs(settings: AppSettings, opts: IcsOptions): IcsResult {
  const lines: string[] = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//PeakForm//Reminders//EN',
    'CALSCALE:GREGORIAN',
    'METHOD:PUBLISH',
    `X-WR-CALNAME:${escapeText(opts.calName)}`,
  ];
  const until = addDays(opts.today, opts.weeks * 7);
  let events = 0;
  let excluded = 0;
  for (const r of effectiveReminders(settings)) {
    // First occurrence on or after today.
    let first = opts.today;
    for (let i = 0; i < 7; i++) {
      const k = addDays(opts.today, i);
      if (r.weekdays.includes(weekdayOf(k))) {
        first = k;
        break;
      }
    }
    const exdates: string[] = [];
    if (settings.sabbath.enabled) {
      for (let k = first; k <= until; k = addDays(k, 1)) {
        if (r.weekdays.includes(weekdayOf(k)) && isSabbathTime(k, r.time, settings.sabbath)) exdates.push(floating(k, r.time));
      }
    }
    // If every occurrence would be excluded, skip the event entirely.
    const occurrences = countOccurrences(first, until, r.weekdays);
    if (exdates.length >= occurrences) {
      excluded += exdates.length;
      continue;
    }
    excluded += exdates.length;
    const days = [...r.weekdays].sort().map((d) => BYDAY[d]).join(',');
    lines.push(
      'BEGIN:VEVENT',
      `UID:peakform-${r.id}@peakform.local`,
      `SEQUENCE:${opts.sequence}`,
      `DTSTAMP:${utcStamp(opts.now)}`,
      `DTSTART:${floating(first, r.time)}`,
      'DURATION:PT10M',
      `RRULE:FREQ=WEEKLY;BYDAY=${days};UNTIL=${floating(until, '23:59').slice(0, 8)}T235900`,
      ...(exdates.length ? [`EXDATE:${exdates.join(',')}`] : []),
      `SUMMARY:${escapeText(r.label)}`,
      `DESCRIPTION:${escapeText('From PeakForm. Open the app to log it.')}`,
      'TRANSP:TRANSPARENT',
      'BEGIN:VALARM',
      'ACTION:DISPLAY',
      `DESCRIPTION:${escapeText(r.label)}`,
      'TRIGGER:PT0M',
      'END:VALARM',
      'END:VEVENT',
    );
    events++;
  }
  lines.push('END:VCALENDAR');
  return { text: lines.map(foldLine).join('\r\n') + '\r\n', eventCount: events, excludedCount: excluded, untilDate: until };
}

function countOccurrences(first: DateKey, until: DateKey, weekdays: number[]): number {
  let n = 0;
  for (let k = first; k <= until; k = addDays(k, 1)) if (weekdays.includes(weekdayOf(k))) n++;
  return n;
}

/** Stable hash of reminder settings, used to tell the user when the calendar is out of date. */
export function reminderHash(settings: AppSettings): string {
  const s = JSON.stringify({ r: settings.reminders, s: settings.sabbath });
  let h = 5381;
  for (let i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) | 0;
  return (h >>> 0).toString(36);
}
