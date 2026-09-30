import { describe, expect, it } from 'vitest';
import { BASELINE_PLAN } from '../src/content/plan';
import { BASELINE_TARGETS } from '../src/content/meals';
import { exercise } from '../src/content/library';
import { coverageFrom, planCoverageInputs } from '../src/domain/coverage';
import { baselinePlanRecord, defaultSettings } from '../src/domain/defaults';
import { OLD_VOLLEYBALL_MAIN_IDS, gymDaysPending, missingMorningItems, withGymDayTargets, withGymDays, withMorningItems, withMorningTimes } from '../src/services/planUpdate';
import { bedtimeFor } from '../src/services/today';
import type { AppSettings, PlanRecord } from '../src/db/records';
import { OLD_VOLLEYBALL_DAYS } from './fixtures/volleyballDays';

/** The plan as installed before the morning sessions existed: only the rope in the morning, none on Sunday. */
function oldPlan(): PlanRecord {
  const p = baselinePlanRecord(0);
  for (const d of p.days) d.items = d.items.filter((i) => i.session !== 'morning' || (i.exerciseId === 'easy-jump-rope' && d.key !== 'sun'));
  return p;
}

/** An install that already has the morning sessions but still has the old Tuesday and Friday volleyball days. */
function volleyballDaysPlan(): PlanRecord {
  const p = baselinePlanRecord(0);
  for (const old of OLD_VOLLEYBALL_DAYS) {
    const d = p.days.find((x) => x.weekday === old.weekday)!;
    d.title = old.title;
    d.short = old.short;
    d.items = [...d.items.filter((i) => i.session === 'morning'), ...structuredClone(old.main), ...d.items.filter((i) => i.session === 'swim')];
  }
  return p;
}

const lookup = (id: string) => {
  const e = exercise(id);
  return e && { name: e.name, kind: e.kind, primary: e.muscles.primary, secondary: e.muscles.secondary, fatigueOverlap: e.fatigueOverlap };
};

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

describe('Tuesday and Friday gym days', () => {
  const main = (weekday: number) => BASELINE_PLAN.days.find((d) => d.weekday === weekday)!.items.filter((i) => i.session === 'main');

  it('are regular gym sessions with reps in reserve, and Friday keeps the swim', () => {
    for (const weekday of [2, 5]) {
      const items = main(weekday);
      expect(items.length).toBeGreaterThanOrEqual(6);
      const sets = items.reduce((n, i) => n + i.sets, 0);
      expect(sets).toBeGreaterThanOrEqual(15);
      expect(sets).toBeLessThanOrEqual(22);
      for (const i of items) {
        expect(['strength', 'bodyweight']).toContain(exercise(i.exerciseId)!.kind);
        expect(i.rir).toBeGreaterThanOrEqual(2);
        expect(i.rir).toBeLessThanOrEqual(3);
        // New IDs, so no old progression target carries over to a different exercise.
        expect(OLD_VOLLEYBALL_MAIN_IDS[weekday]).not.toContain(i.id);
      }
    }
    expect(BASELINE_PLAN.days.find((d) => d.weekday === 5)!.items.some((i) => i.session === 'swim')).toBe(true);
    expect(BASELINE_TARGETS.find((t) => t.weekday === 2)!.label).toBe('Upper C');
  });

  it('give every major muscle enough direct weekly sets without piling on any one', () => {
    const cov = coverageFrom(planCoverageInputs(BASELINE_PLAN.days), lookup);
    const floors: Record<string, number> = { lats: 10, traps_middle: 8, delt_lateral: 6, delt_posterior: 6, biceps: 4, triceps: 6, quads: 10, hamstrings: 10, glute_max: 10, adductors: 4, gastrocnemius: 6, erectors: 3 };
    for (const [m, min] of Object.entries(floors)) expect(cov[m as keyof typeof cov].direct, m).toBeGreaterThanOrEqual(min);
    expect(cov.pec_sternal.direct + cov.pec_clavicular.direct).toBeGreaterThanOrEqual(12);
    for (const c of Object.values(cov)) expect(c.direct, c.muscle).toBeLessThanOrEqual(20);
  });

  it('replaces only the old volleyball drills on an installed plan and keeps the rest', () => {
    const before = volleyballDaysPlan();
    before.days[2]!.items.push({ ...before.days[2]!.items.at(-1)!, id: 'my-extra-tue', notes: ['mine'] });
    expect(gymDaysPending(before)).toEqual([2, 5]);
    const after = withGymDays(before);
    expect(gymDaysPending(after)).toEqual([]);
    for (const weekday of [2, 5]) {
      const d = after.days.find((x) => x.weekday === weekday)!;
      const base = BASELINE_PLAN.days.find((x) => x.weekday === weekday)!;
      expect(d.title).toBe(base.title);
      expect(d.items.filter((i) => i.session === 'morning').map((i) => i.id)).toEqual(base.items.filter((i) => i.session === 'morning').map((i) => i.id));
      expect(d.items.map((i) => i.exerciseId)).not.toContain('volleyball-spike');
      expect(d.items.filter((i) => i.session === 'swim')).toHaveLength(weekday === 5 ? 1 : 0);
    }
    const tue = after.days[2]!.items.filter((i) => i.session === 'main').map((i) => i.id);
    expect(tue).toEqual([...main(2).map((i) => i.id), 'my-extra-tue']);
    // Other days are untouched.
    for (const weekday of [0, 1, 3, 4, 6]) expect(after.days[weekday]).toEqual(before.days[weekday]);
  });

  it('works together with the morning update on the oldest installs', () => {
    const p = volleyballDaysPlan();
    for (const d of p.days) d.items = d.items.filter((i) => i.session !== 'morning' || (i.exerciseId === 'easy-jump-rope' && d.key !== 'sun'));
    const after = withGymDays(withMorningItems(p));
    for (const d of after.days) expect(d.items.map((i) => i.id)).toEqual(BASELINE_PLAN.days[d.weekday]!.items.map((i) => i.id));
  });

  it('leaves a day the user turned into rest alone, and renames only default food labels', () => {
    const p = volleyballDaysPlan();
    p.days[5]!.isRest = true;
    expect(gymDaysPending(p)).toEqual([2]);
    expect(withGymDays(p).days[5]).toEqual(p.days[5]);

    const old = BASELINE_TARGETS.map((t) => ({ ...t }));
    old[2]!.label = 'Volleyball and shoulder care';
    old[5]!.label = 'My Friday';
    const renamed = withGymDayTargets(old);
    expect(renamed[2]!.label).toBe('Upper C');
    expect(renamed[2]!.kcal).toBe(old[2]!.kcal);
    expect(renamed[5]!.label).toBe('My Friday');
  });
});
