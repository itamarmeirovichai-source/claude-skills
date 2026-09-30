import { describe, expect, it } from 'vitest';
import { nextLoad, suggestNext, type Prescription, type WorkSet } from '../src/domain/progression';

const squat: Prescription = { kind: 'strength', sets: 3, repMin: 6, repMax: 10, rir: 3, perSide: false, loadIncrement: 'lower', equipment: 'barbell' };
const bench: Prescription = { kind: 'strength', sets: 3, repMin: 8, repMax: 12, rir: 2, perSide: false, loadIncrement: 'upper', equipment: 'barbell' };

function sets(reps: number[], opts: Partial<WorkSet> = {}, weight = 50, rir = 3): WorkSet[] {
  return reps.map((r, i) => ({ setIndex: i, side: null, weightKg: weight, reps: r, rir, form: 'good', pain: 'none', ...opts }));
}

describe('double progression', () => {
  it('one set of nine reps does not increase the load', () => {
    const s = suggestNext(squat, sets([9]));
    expect(s.kind).toBe('complete_sets');
    expect(s.targets.every((t) => t.weightKg === null || t.weightKg === 50)).toBe(true);
  });

  it('9, 8, 8 at the target RIR adds one rep at the same load, never more weight', () => {
    const s = suggestNext(squat, sets([9, 8, 8]));
    expect(s.kind).toBe('add_reps');
    expect(s.targets.map((t) => t.weightKg)).toEqual([50, 50, 50]);
    const reps = s.targets.map((t) => t.reps ?? 0);
    expect(reps.reduce((a, b) => a + b, 0)).toBe(26);
    expect(reps.every((r) => r <= 10)).toBe(true);
    expect(reps).toEqual([9, 9, 8]);
    expect(s.requiresConfirmation).toBe(true);
    expect(s.reason).toMatch(/every work set reaches 10/);
  });

  it('10, 10, 10 at the target RIR with good form suggests the smallest practical increase and resets reps', () => {
    const s = suggestNext(squat, sets([10, 10, 10]));
    expect(s.kind).toBe('add_load');
    expect(s.targets.map((t) => t.weightKg)).toEqual([52.5, 52.5, 52.5]);
    expect(s.targets.map((t) => t.reps)).toEqual([6, 6, 6]);
  });

  it('10, 10, 9 does not qualify for more load', () => {
    const s = suggestNext(squat, sets([10, 10, 9]));
    expect(s.kind).toBe('add_reps');
    expect(s.targets.map((t) => t.reps)).toEqual([10, 10, 10]);
    expect(s.targets.every((t) => t.weightKg === 50)).toBe(true);
  });

  it('poor form blocks progression', () => {
    const s = suggestNext(squat, [...sets([10, 10]), { setIndex: 2, side: null, weightKg: 50, reps: 10, rir: 3, form: 'poor', pain: 'none' }]);
    expect(['hold', 'reduce']).toContain(s.kind);
    expect(s.targets.every((t) => (t.weightKg ?? 0) <= 50)).toBe(true);
  });

  it('acceptable form holds the load', () => {
    const s = suggestNext(squat, sets([10, 10, 10], { form: 'acceptable' }));
    expect(s.kind).toBe('hold');
    expect(s.targets.every((t) => t.weightKg === 50)).toBe(true);
  });

  it('pain blocks progression, and severe pain asks to pause and tell a parent or coach', () => {
    const mild = suggestNext(squat, [...sets([10, 10]), { setIndex: 2, side: null, weightKg: 50, reps: 10, rir: 3, form: 'good', pain: 'mild', painScore: 2 }]);
    expect(mild.kind).toBe('pain_hold');
    expect(mild.targets).toHaveLength(0);
    const severe = suggestNext(squat, [...sets([10, 10]), { setIndex: 2, side: null, weightKg: 50, reps: 10, rir: 3, form: 'good', pain: 'none', painScore: 4 }]);
    expect(severe.kind).toBe('pain_hold');
    expect(severe.title).toMatch(/parent or coach/);
  });

  it('RIR below prescription holds or reduces, never increases', () => {
    const s = suggestNext(squat, sets([10, 10, 10], {}, 50, 2));
    expect(s.kind).toBe('hold');
    const hard = suggestNext(squat, sets([10, 10, 10], {}, 50, 0));
    expect(hard.kind).toBe('reduce');
    expect(hard.targets.every((t) => (t.weightKg ?? 99) < 50)).toBe(true);
  });

  it('missing RIR or form never produces progress', () => {
    const s = suggestNext(squat, sets([10, 10, 10], { rir: null }));
    expect(s.kind).toBe('hold');
  });

  it('mixed loads are judged at the lowest load', () => {
    const s = suggestNext(squat, [
      { setIndex: 0, side: null, weightKg: 55, reps: 10, rir: 3, form: 'good', pain: 'none' },
      { setIndex: 1, side: null, weightKg: 50, reps: 10, rir: 3, form: 'good', pain: 'none' },
      { setIndex: 2, side: null, weightKg: 50, reps: 10, rir: 3, form: 'good', pain: 'none' },
    ]);
    expect(s.kind).toBe('hold');
    expect(s.targets.every((t) => t.weightKg === 50)).toBe(true);
  });

  it('reps below the range hold the load and target the bottom of the range', () => {
    const s = suggestNext(bench, sets([8, 7, 6], {}, 40, 2));
    expect(s.kind).toBe('hold');
    expect(s.targets.map((t) => t.reps)).toEqual([8, 8, 8]);
  });
});

describe('left and right qualification', () => {
  const bss: Prescription = { kind: 'strength', sets: 2, repMin: 8, repMax: 12, rir: 3, perSide: true, loadIncrement: 'lower', equipment: 'dumbbell' };
  const side = (s: 'left' | 'right', reps: number[], w = 16): WorkSet[] =>
    reps.map((r, i) => ({ setIndex: i, side: s, weightKg: w, reps: r, rir: 3, form: 'good', pain: 'none' }));

  it('requires both sides to reach the top before adding load', () => {
    const s = suggestNext(bss, [...side('left', [12, 12]), ...side('right', [12, 11])]);
    expect(s.kind).toBe('add_reps');
    expect(s.reason).toMatch(/both sides must qualify/);
    expect(s.targets.every((t) => t.weightKg === 16)).toBe(true);
    expect(s.targets.filter((t) => t.side === 'right').map((t) => t.reps)).toEqual([12, 12]);
  });

  it('adds load when both sides qualify', () => {
    const s = suggestNext(bss, [...side('left', [12, 12]), ...side('right', [12, 12])]);
    expect(s.kind).toBe('add_load');
    expect(s.targets.every((t) => t.weightKg === 18)).toBe(true);
  });

  it('requires all sets on each side', () => {
    const s = suggestNext(bss, [...side('left', [12, 12]), ...side('right', [12])]);
    expect(s.kind).toBe('complete_sets');
  });
});

describe('load increments', () => {
  it('uses the equipment step as the minimum', () => {
    expect(nextLoad(40, 'upper', 'barbell')).toBe(42.5);
    expect(nextLoad(20, 'upper', 'cable')).toBe(22.5);
  });
  it('rounds the percentage down to the equipment grid for heavier loads', () => {
    expect(nextLoad(100, 'lower', 'barbell')).toBe(105);
    expect(nextLoad(120, 'upper', 'machine')).toBe(122.5);
  });
  it('respects custom increments', () => {
    expect(nextLoad(40, 'upper', 'barbell', { barbellKg: 1, machineKg: 5, cableKg: 1.25, dumbbellKg: 1, upperPct: 0.025, lowerPct: 0.05 })).toBe(41);
    expect(nextLoad(40, 'upper', 'machine', { barbellKg: 1, machineKg: 5, cableKg: 1.25, dumbbellKg: 1, upperPct: 0.025, lowerPct: 0.05 })).toBe(45);
  });
});

describe('activities that never auto progress', () => {
  it('jumps, sprints, and swims hold volume', () => {
    const jump = suggestNext({ ...squat, kind: 'jump', equipment: 'bodyweight', loadIncrement: 'none' }, [
      { setIndex: 0, side: null, weightKg: null, reps: 2, rir: null, form: 'good', pain: 'none', quality: 5, landing: 'good' },
    ]);
    expect(jump.kind).toBe('quality_hold');
    expect(jump.targets).toHaveLength(0);
    const swim = suggestNext({ ...squat, kind: 'swim', equipment: 'bodyweight', loadIncrement: 'none' }, []);
    expect(swim.kind).toBe('hold');
  });

  it('bodyweight exercises at the top of the range do not add difficulty automatically', () => {
    const nordic: Prescription = { kind: 'bodyweight', sets: 2, repMin: 4, repMax: 6, rir: 3, perSide: false, loadIncrement: 'none', equipment: 'bodyweight' };
    const s = suggestNext(nordic, [
      { setIndex: 0, side: null, weightKg: null, reps: 6, rir: 3, form: 'good', pain: 'none' },
      { setIndex: 1, side: null, weightKg: null, reps: 6, rir: 3, form: 'good', pain: 'none' },
    ]);
    expect(s.kind).toBe('hold');
    expect(s.reason).toMatch(/coach/);
  });
});

describe('sets taken to failure', () => {
  const fly: Prescription = { kind: 'strength', sets: 3, repMin: 10, repMax: 15, rir: 0, perSide: false, loadIncrement: 'upper', equipment: 'cable' };
  const press: Prescription = { kind: 'strength', sets: 3, repMin: 8, repMax: 12, rir: 1, lastSetRir: 0, perSide: false, loadIncrement: 'upper', equipment: 'machine' };
  const perSet = (reps: number[], rirs: number[], w = 20): WorkSet[] => reps.map((r, i) => ({ setIndex: i, side: null, weightKg: w, reps: r, rir: rirs[i]!, form: 'good', pain: 'none' }));

  it('adds load once the first set reaches the top, even though later sets lose reps', () => {
    const s = suggestNext(fly, perSet([15, 12, 10], [0, 0, 0]));
    expect(s.kind).toBe('add_load');
    expect(s.targets.every((t) => (t.weightKg ?? 0) > 20)).toBe(true);
    expect(s.targets.map((t) => t.reps)).toEqual([10, 10, 10]);
  });

  it('asks for one more rep on the first set otherwise', () => {
    const s = suggestNext(fly, perSet([13, 11, 9], [0, 0, 0]));
    expect(s.kind).toBe('add_reps');
    expect(s.targets.map((t) => t.reps)).toEqual([14, 11, 9]);
    expect(s.targets.every((t) => t.weightKg === 20)).toBe(true);
    expect(s.reason).toMatch(/first set/);
  });

  it('holds when the first set is below the range, and never treats failure on a failure set as too hard', () => {
    expect(suggestNext(fly, perSet([9, 8, 7], [0, 0, 0])).kind).toBe('hold');
    const s = suggestNext(press, perSet([12, 11, 9], [1, 1, 0], 60));
    expect(s.kind).toBe('add_load');
  });

  it('still holds when a set meant to stop one rep short went to failure', () => {
    const s = suggestNext(press, perSet([12, 10, 9], [0, 1, 0], 60));
    expect(['hold', 'reduce']).toContain(s.kind);
    expect(s.reason).toMatch(/below the prescribed 1/);
  });

  it('keeps pain and form rules on failure sets', () => {
    expect(suggestNext(fly, perSet([15, 12, 10], [0, 0, 0]).map((x, i) => (i === 1 ? { ...x, pain: 'mild' as const } : x))).kind).toBe('pain_hold');
    expect(suggestNext(fly, perSet([15, 12, 10], [0, 0, 0]).map((x, i) => (i === 2 ? { ...x, form: 'acceptable' as const } : x))).kind).toBe('hold');
  });
});
