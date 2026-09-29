import { describe, expect, it } from 'vitest';
import { addDays, dateKeyInZone, diffDays, reviewWeekStart, sleepMinutes, weekdayOf } from '../src/domain/dates';
import { adjustTimer, isFinished, pauseTimer, remainingMs, restoreTimer, resumeTimer, startTimer } from '../src/domain/timer';
import { fridayFor, isSabbathTime, sabbathWindow, sunsetLocal, CITIES } from '../src/domain/sabbath';
import { buildIcs, foldLine } from '../src/domain/ics';
import { defaultSettings } from '../src/domain/defaults';

describe('dates, week boundaries, and daylight saving', () => {
  it('adds days across daylight saving changes without drifting', () => {
    // Israel leaves summer time on 2026-10-25, the US on 2026-11-01.
    expect(addDays('2026-10-24', 1)).toBe('2026-10-25');
    expect(addDays('2026-10-25', 1)).toBe('2026-10-26');
    expect(addDays('2026-10-31', 2)).toBe('2026-11-02');
    expect(diffDays('2026-11-02', '2026-10-24')).toBe(9);
  });

  it('review weeks run Monday to Sunday so the Sunday review includes Sunday', () => {
    expect(weekdayOf('2026-10-04')).toBe(0);
    expect(reviewWeekStart('2026-10-04')).toBe('2026-09-28');
    expect(reviewWeekStart('2026-09-28')).toBe('2026-09-28');
    expect(reviewWeekStart('2026-10-03')).toBe('2026-09-28');
    expect(reviewWeekStart('2026-10-05')).toBe('2026-10-05');
  });

  it('computes date keys in a named zone around midnight', () => {
    const ms = Date.UTC(2026, 9, 24, 22, 30); // 01:30 on 25 Oct in Jerusalem (still summer time)
    expect(dateKeyInZone(ms, 'Asia/Jerusalem')).toBe('2026-10-25');
    expect(dateKeyInZone(ms, 'America/New_York')).toBe('2026-10-24');
  });

  it('measures sleep across midnight', () => {
    expect(sleepMinutes('22:30', '07:00')).toBe(510);
    expect(sleepMinutes('00:15', '07:00')).toBe(405);
  });
});

describe('rest timer', () => {
  it('restores the correct remaining time after the app was backgrounded', () => {
    const t0 = 1_000_000;
    const t = startTimer('Squat', 180, t0);
    // Suspended for 100 seconds: nothing ticked in between.
    const back = t0 + 100_000;
    const { timer, overdueMs } = restoreTimer(JSON.parse(JSON.stringify(t)), back);
    expect(timer).not.toBeNull();
    expect(remainingMs(timer!, back)).toBe(80_000);
    expect(overdueMs).toBe(0);
  });

  it('reports how long ago the rest finished when resumed late', () => {
    const t = startTimer('Row', 90, 0);
    const r = restoreTimer(t, 120_000);
    expect(isFinished(r.timer!, 120_000)).toBe(true);
    expect(r.overdueMs).toBe(30_000);
    expect(restoreTimer(t, 90_000 + 16 * 60_000).timer).toBeNull();
  });

  it('pauses, resumes, and adjusts from the absolute end', () => {
    let t = startTimer('Curl', 90, 0);
    t = pauseTimer(t, 30_000);
    expect(remainingMs(t, 500_000)).toBe(60_000);
    t = resumeTimer(t, 500_000);
    expect(remainingMs(t, 510_000)).toBe(50_000);
    t = adjustTimer(t, 15, 510_000);
    expect(remainingMs(t, 510_000)).toBe(65_000);
    t = adjustTimer(t, -120, 510_000);
    expect(remainingMs(t, 510_000)).toBe(0);
  });
});

describe('Sabbath Mode', () => {
  const s = defaultSettings(0);

  it('uses manual Friday and Saturday times', () => {
    const w = sabbathWindow('2026-10-02', s.sabbath);
    expect(w.start).toBe('17:30');
    expect(w.end).toBe('18:45');
    expect(isSabbathTime('2026-10-02', '18:45', s.sabbath)).toBe(true);
    expect(isSabbathTime('2026-10-02', '16:15', s.sabbath)).toBe(false);
    expect(isSabbathTime('2026-10-03', '07:00', s.sabbath)).toBe(true);
    expect(isSabbathTime('2026-10-03', '21:45', s.sabbath)).toBe(false);
    expect(isSabbathTime('2026-10-04', '07:00', s.sabbath)).toBe(false);
  });

  it('is silent only when enabled', () => {
    expect(isSabbathTime('2026-10-03', '07:00', { ...s.sabbath, enabled: false })).toBe(false);
  });

  it('calculates approximate sunset locally for a city, including the clock change', () => {
    const jlm = CITIES.find((c) => c.id === 'jerusalem')!;
    const before = sunsetLocal('2026-10-23', jlm)!;
    const after = sunsetLocal('2026-10-30', jlm)!;
    // Published tables give about 17:55 in summer time before the change and 16:50 after it.
    expect(before >= '17:50' && before <= '18:05').toBe(true);
    expect(after >= '16:45' && after <= '17:00').toBe(true);
    const w = sabbathWindow('2026-10-30', { ...s.sabbath, mode: 'city', cityId: 'jerusalem', candleOffsetMin: 40, endOffsetMin: 40 });
    expect(w.source).toBe('city');
    expect(w.start < after).toBe(true);
  });

  it('finds the relevant Friday', () => {
    expect(fridayFor('2026-10-03')).toBe('2026-10-02');
    expect(fridayFor('2026-09-29')).toBe('2026-10-02');
    expect(fridayFor('2026-10-02')).toBe('2026-10-02');
  });
});

describe('ICS calendar', () => {
  it('creates recurring events with alarms and removes Sabbath occurrences', () => {
    const s = defaultSettings(0);
    const r = buildIcs(s, { today: '2026-09-29', weeks: 4, now: Date.UTC(2026, 8, 29), sequence: 1, calName: 'PeakForm' });
    expect(r.text.startsWith('BEGIN:VCALENDAR\r\n')).toBe(true);
    expect(r.text.trim().endsWith('END:VCALENDAR')).toBe(true);
    // Ten reminders, including the 05:25 morning session reminder.
    expect(r.eventCount).toBe(10);
    expect(r.text).toContain('RRULE:FREQ=WEEKLY;BYDAY=SU,MO,TU,WE,TH,FR,SA');
    expect(r.text).toContain('BEGIN:VALARM');
    expect(r.text).toContain('SUMMARY:Weekly review');
    // The Saturday 05:15 check in falls inside the window and is excluded.
    expect(r.text).toMatch(/EXDATE:20261003T051500/);
    // Friday 20:45 wind down is excluded, Saturday 20:45 is not.
    const wind = r.text.split('BEGIN:VEVENT').find((e) => e.includes('Wind down'))!;
    expect(wind).toContain('20261002T204500');
    expect(wind).not.toContain('20261003T204500');
    expect(r.excludedCount).toBeGreaterThan(0);
    for (const line of r.text.split('\r\n')) expect(new TextEncoder().encode(line).length).toBeLessThanOrEqual(75);
  });

  it('folds long lines', () => {
    const long = 'DESCRIPTION:' + 'x'.repeat(200);
    const folded = foldLine(long);
    expect(folded.split('\r\n ').join('')).toBe(long);
  });

  it('includes every weekday reminder when Sabbath Mode is off', () => {
    const s = defaultSettings(0);
    s.sabbath.enabled = false;
    const r = buildIcs(s, { today: '2026-09-29', weeks: 2, now: 0, sequence: 1, calName: 'PeakForm' });
    expect(r.text).not.toContain('EXDATE');
  });
});
