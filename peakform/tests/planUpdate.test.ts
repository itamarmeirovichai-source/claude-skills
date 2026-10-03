import { describe, expect, it } from 'vitest';
import { BASELINE_PLAN } from '../src/content/plan';
import { baselinePlanRecord, defaultSettings } from '../src/domain/defaults';
import { missingMorningItems, withMorningItems, withMorningTimes } from '../src/services/planUpdate';
import { bedtimeFor } from '../src/services/today';
import type { AppSettings, PlanRecord } from '../src/db/records';

/** The plan as installed before the morning sessions existed: only the rope in the morning, none on Sunday. */
function oldPlan(): PlanRecord {
  const p = baselinePlanRecord(0);
  for (const d of p.days) d.items = d.items.filter((i) => i.session !== 'morning' || (i.exerciseId === 'easy-jump-rope' && d.key !== 'sun'));
  return p;
}

function oldSettings(): AppSettings {
  const s = defaultSettings(0);
  s.sessionTimes.morning = '07:00';
  s.reminders = s.reminders.filter((r) => r.id !== 'morning');
  s.reminders.find((r) => r.id === 'checkin')!.time = '07:00';
  s.reminders.find((r) => r.id === 'winddown')!.time = '21:45';
  return s;
}

describe('morning volleyball plan', () => {
  it('has a no ball morning session with the rope first on every training day, and none on Saturday', () => {
    for (const day of BASELINE_PLAN.days) {
      const am = day.items.filter((i) => i.session === 'morning');
      if (day.isRest) {
        expect(am).toHaveLength(0);
        continue;
      }
      expect(am.length).toBeGreaterThanOrEqual(3);
      expect(am[0]!.exerciseId).toBe('easy-jump-rope');
      expect(am.map((i) => i.exerciseId)).not.toContain('volleyball-spike');
      // Nothing heavy or near failure in the morning.
      for (const i of am) if (i.rir !== undefined) expect(i.rir).toBeGreaterThanOrEqual(2);
    }
  });

  it('offers exactly the missing morning items to an installed plan and keeps everything else', () => {
    const before = oldPlan();
    const missing = missingMorningItems(before);
    expect([...missing.keys()].sort()).toEqual([0, 1, 2, 3, 4, 5]);
    expect(missing.get(0)!.map((i) => i.id)).toContain('sun-rope');

    const after = withMorningItems(before);
    expect(missingMorningItems(after).size).toBe(0);
    for (const d of after.days) {
      const old = before.days.find((x) => x.weekday === d.weekday)!;
      // Every original item is still there, in the same order.
      const kept = d.items.filter((i) => old.items.some((o) => o.id === i.id)).map((i) => i.id);
      expect(kept).toEqual(old.items.map((i) => i.id));
      const am = d.items.filter((i) => i.session === 'morning');
      if (am.length) expect(am[0]!.exerciseId).toBe('easy-jump-rope');
    }
    expect(after.globalRules[0]).toMatch(/05:30/);
  });

  it('keeps items the user added and does not offer the update twice', () => {
    const p = oldPlan();
    p.days[1]!.items.push({ ...p.days[1]!.items[0]!, id: 'my-extra', notes: ['mine'] });
    const after = withMorningItems(p);
    expect(after.days[1]!.items.some((i) => i.id === 'my-extra')).toBe(true);
    expect(missingMorningItems(withMorningItems(after)).size).toBe(0);
  });

  it('moves old default times to the 05:30 schedule but leaves times the user chose', () => {
    const moved = withMorningTimes(oldSettings());
    expect(moved.sessionTimes.morning).toBe('05:30');
    expect(moved.reminders.find((r) => r.id === 'checkin')!.time).toBe('05:15');
    expect(moved.reminders.find((r) => r.id === 'winddown')!.time).toBe('20:45');
    expect(moved.reminders.filter((r) => r.id === 'morning')).toHaveLength(1);

    const mine = oldSettings();
    mine.sessionTimes.morning = '06:10';
    mine.reminders.find((r) => r.id === 'winddown')!.time = '21:00';
    const kept = withMorningTimes(mine);
    expect(kept.sessionTimes.morning).toBe('06:10');
    expect(kept.reminders.find((r) => r.id === 'winddown')!.time).toBe('21:00');
    expect(withMorningTimes(kept).reminders.filter((r) => r.id === 'morning')).toHaveLength(1);
  });

  it('suggests a bedtime that keeps at least eight hours of sleep', () => {
    expect(bedtimeFor('05:30')).toBe('21:15');
    expect(bedtimeFor('07:00')).toBe('22:45');
    expect(bedtimeFor('00:30')).toBe('16:15');
  });
});
