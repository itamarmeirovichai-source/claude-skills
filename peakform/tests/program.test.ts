import { describe, expect, it } from 'vitest';
import { BASELINE_PLAN, planDaysFor } from '../src/content/plan';
import { BASELINE_TARGETS } from '../src/content/meals';
import { LIBRARY, exercise } from '../src/content/library';
import { PROGRAM_DAYS, PROGRAM_SLOTS, defaultPicks, normalizePicks, slotExposures, togglePick } from '../src/content/program';
import { coverageFrom, planCoverageInputs } from '../src/domain/coverage';
import { baselinePlanRecord } from '../src/domain/defaults';
import { withProgram, withProgramTargetLabels } from '../src/services/planUpdate';
import type { PlanRecord } from '../src/db/records';
import { OLD_VOLLEYBALL_DAYS } from './fixtures/volleyballDays';

const lookup = (id: string) => {
  const e = exercise(id);
  return e && { name: e.name, kind: e.kind, primary: e.muscles.primary, secondary: e.muscles.secondary, fatigueOverlap: e.fatigueOverlap };
};

/** A phone installed before 2.0.0: morning sessions, and the old Tuesday and Friday volleyball days. */
function oldInstall(): PlanRecord {
  const p = baselinePlanRecord(0);
  for (const old of OLD_VOLLEYBALL_DAYS) {
    const d = p.days.find((x) => x.weekday === old.weekday)!;
    d.title = old.title;
    d.short = old.short;
    d.items = [...d.items.filter((i) => i.session === 'morning'), ...structuredClone(old.main), ...d.items.filter((i) => i.session === 'swim')];
  }
  return p;
}

const FREE_BARBELL = ['barbell-squat', 'romanian-deadlift', 'barbell-hip-thrust', 'barbell-bench-press', 'incline-barbell-bench-press'];

describe('program slots', () => {
  it('offer only library exercises that are safe alone, sharing a main muscle within each slot', () => {
    for (const slot of PROGRAM_SLOTS) {
      expect(slot.options.length, slot.id).toBeGreaterThanOrEqual(1);
      expect(slot.options.length, slot.id).toBeLessThanOrEqual(4);
      const muscles = slot.options.map((id) => {
        const ex = exercise(id);
        expect(ex, `${slot.id}: ${id}`).toBeDefined();
        expect(FREE_BARBELL).not.toContain(id);
        return new Set([...ex!.muscles.primary]);
      });
      // Every option shares at least one primary muscle with the first option.
      for (const m of muscles.slice(1)) expect([...m].some((x) => muscles[0]!.has(x)), slot.id).toBe(true);
      expect(new Set(slot.options).size).toBe(slot.options.length);
    }
  });

  it('put every slot in the week, and train most muscles at least twice', () => {
    for (const slot of PROGRAM_SLOTS) expect(slotExposures(slot.id), slot.id).toBeGreaterThanOrEqual(1);
    for (const id of ['chest-upper', 'lats', 'row', 'side-delt', 'rear-delt', 'biceps-long', 'triceps-long', 'quads', 'rectus-femoris', 'hamstring-curl', 'hinge', 'glutes', 'glute-med', 'adductors', 'calves', 'abs'] as const) {
      expect(slotExposures(id), id).toBeGreaterThanOrEqual(2);
    }
  });

  it('cycle a tap through first choice, second choice, and off', () => {
    expect(togglePick([], 'lateral-raise', true)).toEqual(['lateral-raise']);
    expect(togglePick(['lateral-raise'], 'machine-lateral-raise', true)).toEqual(['lateral-raise', 'machine-lateral-raise']);
    expect(togglePick(['lateral-raise', 'machine-lateral-raise'], 'single-arm-cable-lateral-raise', true)).toEqual(['lateral-raise', 'single-arm-cable-lateral-raise']);
    expect(togglePick(['lateral-raise'], 'machine-lateral-raise', false)).toEqual(['machine-lateral-raise']);
    expect(togglePick(['lateral-raise', 'machine-lateral-raise'], 'lateral-raise', true)).toEqual(['machine-lateral-raise']);
  });

  it('fall back to the defaults for missing or unknown picks', () => {
    const picks = normalizePicks({ 'side-delt': ['barbell-squat' as never, 'machine-lateral-raise'], quads: [] });
    expect(picks['side-delt']).toEqual(['machine-lateral-raise']);
    expect(picks.quads).toEqual(defaultPicks().quads);
  });
});

describe('the default week', () => {
  const main = (weekday: number) => BASELINE_PLAN.days.find((d) => d.weekday === weekday)!.items.filter((i) => i.session === 'main');

  it('has six gym days of about 18 to 26 work sets, a full rest Saturday, and both swims', () => {
    for (const d of PROGRAM_DAYS) {
      const sets = main(d.weekday).reduce((n, i) => n + i.sets, 0);
      expect(sets, d.key).toBeGreaterThanOrEqual(18);
      expect(sets, d.key).toBeLessThanOrEqual(27);
    }
    expect(BASELINE_PLAN.days.find((d) => d.weekday === 6)!.isRest).toBe(true);
    for (const wd of [0, 5]) expect(BASELINE_PLAN.days.find((d) => d.weekday === wd)!.items.some((i) => i.session === 'swim')).toBe(true);
  });

  it('sets failure only where the exercise allows it, and keeps shoulder care and dumbbell work short of failure', () => {
    for (const d of BASELINE_PLAN.days)
      for (const it of d.items.filter((i) => i.session === 'main')) {
        const ex = exercise(it.exerciseId)!;
        if (it.rir === 0) expect(ex.failure, it.id).toBe('all');
        if (it.lastSetRir === 0) expect(ex.failure, it.id).toBe('last');
        if (ex.failure === 'never' && it.rir !== undefined) expect(it.rir, it.id).toBeGreaterThanOrEqual(1);
        expect(FREE_BARBELL).not.toContain(it.exerciseId);
      }
    const care = main(0).find((i) => i.exerciseId === 'cable-external-rotation')!;
    expect(care.rir).toBe(3);
  });

  it('gives every major muscle about 9 to 18 direct sets a week and none more than 20', () => {
    const cov = coverageFrom(planCoverageInputs(BASELINE_PLAN.days), lookup);
    const floors: Record<string, number> = { pec_clavicular: 6, pec_sternal: 6, lats: 9, traps_middle: 6, delt_lateral: 9, delt_posterior: 6, biceps: 9, triceps: 9, quads: 12, hamstrings: 12, glute_max: 12, glute_med: 6, adductors: 6, gastrocnemius: 9, rectus_abdominis: 6 };
    for (const [m, min] of Object.entries(floors)) expect(cov[m as keyof typeof cov].direct, m).toBeGreaterThanOrEqual(min);
    for (const c of Object.values(cov)) expect(c.direct, c.muscle).toBeLessThanOrEqual(20);
  });

  it('starts every upper day with shoulder care and puts the big exercises before the small ones', () => {
    for (const wd of [0, 2, 4]) expect(['cable-external-rotation', 'side-lying-external-rotation']).toContain(main(wd)[0]!.exerciseId);
    for (const d of PROGRAM_DAYS) {
      const items = main(d.weekday).filter((i) => exercise(i.exerciseId)?.kind === 'strength' && !['cable-external-rotation', 'side-lying-external-rotation'].includes(i.exerciseId));
      const firstSmall = items.findIndex((i) => i.restSec < 150);
      const lastBig = items.map((i) => i.restSec >= 150).lastIndexOf(true);
      if (firstSmall >= 0 && lastBig >= 0) expect(lastBig, d.key).toBeLessThan(firstSmall);
    }
  });

  it('builds the chosen exercises into the right days', () => {
    const picks = { ...defaultPicks(), 'side-delt': ['machine-lateral-raise' as const], quads: ['leg-press' as const, 'smith-squat' as const] };
    const days = planDaysFor(picks);
    const ids = (wd: number) => days.find((d) => d.weekday === wd)!.items.map((i) => i.exerciseId);
    for (const wd of [0, 2, 4]) expect(ids(wd)).toContain('machine-lateral-raise');
    expect(ids(1)).toContain('leg-press');
    expect(ids(5)).toContain('smith-squat');
    expect(ids(1)).not.toContain('smith-squat');
  });
});

describe('moving an installed plan to the program', () => {
  it('replaces the main sessions, keeps morning work, swims, and exercises the user created', () => {
    const before = oldInstall();
    before.days[2]!.items.push({ ...before.days[2]!.items.at(-1)!, id: 'my-own', exerciseId: 'custom-abc', session: 'main', notes: ['mine'] });
    const after = withProgram(before, defaultPicks(), false);
    const built = planDaysFor(defaultPicks());
    for (const d of after.days) {
      const b = built.find((x) => x.weekday === d.weekday)!;
      const old = before.days.find((x) => x.weekday === d.weekday)!;
      expect(d.title).toBe(b.title);
      expect(d.items.filter((i) => i.session === 'morning')).toEqual(old.items.filter((i) => i.session === 'morning'));
      expect(d.items.filter((i) => i.session === 'swim')).toEqual(old.items.filter((i) => i.session === 'swim'));
      expect(d.items.map((i) => i.exerciseId)).not.toContain('volleyball-spike');
    }
    expect(after.days[2]!.items.some((i) => i.id === 'my-own')).toBe(true);
    expect(after.globalRules.join(' ')).toMatch(/clean form/);
    expect(after.globalRules.join(' ')).not.toMatch(/Do not take routine sets to failure/);
  });

  it('gives the oldest installs the full current week, morning sessions included', () => {
    const p = oldInstall();
    for (const d of p.days) d.items = d.items.filter((i) => i.session !== 'morning' || (i.exerciseId === 'easy-jump-rope' && d.key !== 'sun'));
    const after = withProgram(p, defaultPicks(), true);
    for (const d of after.days) expect(d.items.map((i) => i.id)).toEqual(BASELINE_PLAN.days.find((x) => x.weekday === d.weekday)!.items.map((i) => i.id));
  });

  it('renames only food targets that still have an old default name', () => {
    const old = BASELINE_TARGETS.map((t) => ({ ...t }));
    old[2]!.label = 'Upper C';
    old[4]!.label = 'Upper B';
    old[5]!.label = 'My Friday';
    const renamed = withProgramTargetLabels(old);
    expect(renamed[2]!.label).toBe('Upper B');
    expect(renamed[4]!.label).toBe('Upper C');
    expect(renamed[2]!.kcal).toBe(old[2]!.kcal);
    expect(renamed[5]!.label).toBe('My Friday');
  });
});

describe('exercise library', () => {
  it('describes effort for every loaded exercise and never prescribes failure on free barbell lifts', () => {
    for (const ex of LIBRARY) {
      if (['strength', 'bodyweight', 'hold'].includes(ex.kind)) expect(ex.failure, ex.id).toBeDefined();
      if (FREE_BARBELL.includes(ex.id)) expect(ex.failure).toBe('never');
    }
  });
});
