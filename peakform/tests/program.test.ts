import { describe, expect, it } from 'vitest';
import { BASELINE_PLAN, planDaysFor } from '../src/content/plan';
import { BASELINE_TARGETS } from '../src/content/meals';
import { LIBRARY, exercise } from '../src/content/library';
import { PROGRAM_DAYS, PROGRAM_SLOTS, defaultPicks, normalizePicks, slotExposures, togglePick } from '../src/content/program';
import { coverageFrom, planCoverageInputs } from '../src/domain/coverage';
import { baselinePlanRecord } from '../src/domain/defaults';
import { withProgram, withProgramTargetLabels } from '../src/services/planUpdate';
import { JUMP_TEST_DATES, PHASES, contacts, nextJumpTest, phaseFor } from '../src/content/phases';
import { addDays, weekdayOf } from '../src/domain/dates';
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
    for (const id of ['chest-upper', 'lats', 'row', 'side-delt', 'rear-delt', 'biceps-long', 'triceps-long', 'hamstring-curl', 'glutes', 'glute-med', 'calves', 'abs'] as const) {
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

  it('has three upper days of 18 to 27 work sets, three lower days with fewer leg sets, a full rest Saturday, and both swims', () => {
    for (const d of PROGRAM_DAYS) {
      const items = main(d.weekday).filter((i) => exercise(i.exerciseId)?.kind !== 'jump' && exercise(i.exerciseId)?.kind !== 'warmup');
      const sets = items.reduce((n, i) => n + i.sets, 0);
      const upper = [0, 2, 4].includes(d.weekday);
      expect(sets, d.key).toBeGreaterThanOrEqual(upper ? 18 : 6);
      expect(sets, d.key).toBeLessThanOrEqual(upper ? 27 : 20);
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
    // Legs get fewer direct sets during the jump program, because the jumps load them too.
    const floors: Record<string, number> = { pec_clavicular: 6, pec_sternal: 6, lats: 9, traps_middle: 6, delt_lateral: 9, delt_posterior: 6, biceps: 9, triceps: 9, quads: 10, hamstrings: 8, glute_max: 10, glute_med: 4, adductors: 3, gastrocnemius: 5, rectus_abdominis: 6 };
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
    const picks = { ...defaultPicks(), 'side-delt': ['machine-lateral-raise' as const], quads: ['smith-squat' as const], glutes: ['bulgarian-split-squat' as const, 'walking-lunge' as const] };
    const days = planDaysFor(picks);
    const ids = (wd: number) => days.find((d) => d.weekday === wd)!.items.map((i) => i.exerciseId);
    for (const wd of [0, 2, 4]) expect(ids(wd)).toContain('machine-lateral-raise');
    expect(ids(1)).toContain('smith-squat');
    expect(ids(3)).toContain('bulgarian-split-squat');
    expect(ids(5)).toContain('walking-lunge');
    expect(ids(5)).not.toContain('bulgarian-split-squat');
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

describe('the jump program for the dunk goal', () => {
  const lowerIds = new Set(['quads', 'hamstrings', 'glute_max', 'glute_med', 'adductors', 'gastrocnemius', 'soleus']);
  const isLeg = (id: string) => {
    const ex = exercise(id);
    return !!ex && ex.kind !== 'jump' && ex.kind !== 'warmup' && ex.muscles.primary.some((m) => lowerIds.has(m));
  };

  it('runs in back to back blocks from Monday 5 October to Sunday 31 January, then keeps going', () => {
    expect(PHASES[0]!.start).toBe('2026-10-05');
    for (const [i, p] of PHASES.entries()) {
      expect(weekdayOf(p.start), p.id).toBe(1);
      if (p.end) expect(weekdayOf(p.end), p.id).toBe(0);
      const next = PHASES[i + 1];
      if (next) expect(next.start, p.id).toBe(addDays(p.end!, 1));
    }
    expect(PHASES.find((p) => p.id === 'taper')!.end).toBe('2027-01-31');
    expect(PHASES.at(-1)!.end).toBeNull();
    expect(phaseFor('2026-10-02').id).toBe('foundation');
    expect(phaseFor('2026-11-02').id).toBe('power');
    expect(phaseFor('2026-11-25').id).toBe('deload-1');
    expect(phaseFor('2027-01-29').id).toBe('taper');
    expect(phaseFor('2027-03-01').id).toBe('build');
  });

  it('tests on Fridays, at the end of blocks, and every four weeks after the goal date', () => {
    for (const d of JUMP_TEST_DATES) expect(weekdayOf(d), d).toBe(5);
    expect(nextJumpTest('2026-10-02')).toBe('2026-10-09');
    expect(nextJumpTest('2026-10-10')).toBe('2026-10-30');
    expect(phaseFor('2026-11-27').id).toBe('deload-1');
    expect(phaseFor('2027-01-29').id).toBe('taper');
    expect(nextJumpTest('2027-01-30')).toBe('2027-02-26');
  });

  it('keeps jump sessions between about 20 and 100 contacts, with lighter weeks before tests', () => {
    for (const p of PHASES) {
      const mon = contacts([...p.jumpsMon, ...p.complexMon]);
      const fri = contacts(p.jumpsFri);
      expect(mon, p.id).toBeLessThanOrEqual(100);
      expect(fri, p.id).toBeLessThanOrEqual(100);
      expect(mon + fri, p.id).toBeLessThanOrEqual(200);
      expect(mon, p.id).toBeGreaterThanOrEqual(20);
      for (const d of [...p.jumpsMon, ...p.complexMon, ...p.jumpsFri]) expect(exercise(d.exerciseId)?.kind, d.exerciseId).toBe('jump');
    }
    const week = (id: string) => {
      const p = PHASES.find((x) => x.id === id)!;
      return contacts([...p.jumpsMon, ...p.complexMon, ...p.jumpsFri]);
    };
    expect(week('deload-1')).toBeLessThan(week('power'));
    expect(week('deload-2')).toBeLessThan(week('reactive'));
    expect(week('taper')).toBeLessThan(week('realize'));
    expect(PHASES.find((p) => p.id === 'deload-2')!.jumpsMon.some((d) => d.exerciseId === 'depth-jump')).toBe(false);
  });

  it('puts the jumps first and never takes legs to failure on Wednesday or Friday', () => {
    for (const p of PHASES) {
      const days = planDaysFor(defaultPicks(), p);
      for (const wd of [1, 5]) {
        const items = days.find((d) => d.weekday === wd)!.items.filter((i) => i.session === 'main');
        const firstLeg = items.findIndex((i) => isLeg(i.exerciseId));
        const jumps = items.map((i, k) => (exercise(i.exerciseId)?.kind === 'jump' ? k : -1)).filter((k) => k >= 0);
        // Only the paired box jumps of the complex sets come after the first heavy set.
        expect(jumps.filter((k) => k < firstLeg).length, `${p.id} ${wd}`).toBe(wd === 1 ? p.jumpsMon.length : p.jumpsFri.length);
        expect(jumps.filter((k) => k > firstLeg).length, `${p.id} ${wd}`).toBe(wd === 1 ? p.complexMon.length : 0);
      }
      for (const wd of [3, 5]) {
        for (const i of days.find((d) => d.weekday === wd)!.items.filter((x) => x.session === 'main' && isLeg(x.exerciseId))) {
          if (exercise(i.exerciseId)!.kind === 'hold') continue;
          expect(i.rir, `${p.id} ${i.id}`).toBeGreaterThanOrEqual(1);
          expect(i.lastSetRir, `${p.id} ${i.id}`).toBeUndefined();
        }
      }
      const mon = days.find((d) => d.weekday === 1)!.items;
      for (const slotEx of [mon.find((i) => i.exerciseId === 'leg-press'), mon.find((i) => i.exerciseId === 'dumbbell-romanian-deadlift')]) {
        expect(slotEx, p.id).toBeDefined();
        expect(slotEx!.rir, p.id).toBeGreaterThanOrEqual(2);
      }
    }
  });

  it('builds each block into an installed plan, keeping the morning work and the swim', () => {
    const power = PHASES.find((p) => p.id === 'power')!;
    const before = baselinePlanRecord(0);
    const after = withProgram(before, defaultPicks(), false, power);
    const mon = after.days.find((d) => d.weekday === 1)!;
    expect(mon.items.some((i) => i.exerciseId === 'depth-jump')).toBe(true);
    expect(mon.items.find((i) => i.exerciseId === 'leg-press')!.sets).toBe(4);
    for (const d of after.days) {
      const old = before.days.find((x) => x.weekday === d.weekday)!;
      expect(d.items.filter((i) => i.session === 'morning')).toEqual(old.items.filter((i) => i.session === 'morning'));
      expect(d.items.filter((i) => i.session === 'swim')).toEqual(old.items.filter((i) => i.session === 'swim'));
    }
    expect(after.days.flatMap((d) => d.items).some((i) => i.exerciseId === 'nordic-hamstring-curl')).toBe(false);
  });
});
