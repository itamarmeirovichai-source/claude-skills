import { describe, expect, it } from 'vitest';
import { BASELINE_PLAN, GLOBAL_RULES, planDaysFor } from '../src/content/plan';
import { LIBRARY, exercise } from '../src/content/library';
import { ACTIVE_SLOTS, PROGRAM_DAYS, PROGRAM_SLOTS, SLOT_BY_ID, defaultPicks, normalizePicks, slotExposures, togglePick, wristSafePick } from '../src/content/program';
import { HOME_JUMP_SESSION, HOME_SKILL_SESSION, buildHomeItems } from '../src/content/homeSessions';
import { HOME_NEEDS, WRIST_LOAD, locationOf, maxWristLoad, wristAllows, wristHoldsLoad } from '../src/content/traits';
import { LIBRARY_IDS } from '../src/content/exercises/ids';
import { PLANNING_PHASES, contacts, nextMeasurementDate, planningPhaseFor } from '../src/content/phases';
import { coverageFrom, planCoverageInputs } from '../src/domain/coverage';
import { DEFAULT_HOME, type HomeSetup } from '../src/domain/athlete';
import { chooseDrill, environments } from '../src/domain/homeSpace';
import { diffPlans } from '../src/domain/planDiff';
import { sessionInfo } from '../src/domain/sessionInfo';
import { baselinePlanRecord } from '../src/domain/defaults';
import { buildPlan } from '../src/services/planUpdate';
import type { PlanDay } from '../src/content/plan';

const lookup = (id: string) => {
  const e = exercise(id);
  return e && { name: e.name, kind: e.kind, primary: e.muscles.primary, secondary: e.muscles.secondary, fatigueOverlap: e.fatigueOverlap };
};

const FREE_BARBELL = ['barbell-squat', 'romanian-deadlift', 'barbell-hip-thrust', 'barbell-bench-press', 'incline-barbell-bench-press'];
const GYM_ONLY_KINDS = ['jump', 'sprint', 'skill', 'throw'];

/** A home with room for every home drill: a mat indoors, a large grass yard, and a solid outdoor wall. */
const ROOMY: HomeSetup = { space: 'large', ceiling: 'standard', surface: 'mat', noiseLimits: 'no', breakables: 'no', outdoor: 'large', outdoorSurface: 'grass', equipment: ['tape', 'ball', 'wall', 'mat'] };
/** A small flat: 2 by 2 metres, low ceiling, tiles, quiet neighbours, no yard. */
const SMALL_FLAT: HomeSetup = { space: 'small', ceiling: 'low', surface: 'slippery', noiseLimits: 'yes', breakables: 'yes', outdoor: 'none', outdoorSurface: 'unknown', equipment: [] };

const items = (days: PlanDay[], wd: number, session: 'home' | 'main') => days.find((d) => d.weekday === wd)!.items.filter((i) => i.session === session);

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
      for (const m of muscles.slice(1)) expect([...m].some((x) => muscles[0]!.has(x)), slot.id).toBe(true);
      expect(new Set(slot.options).size).toBe(slot.options.length);
    }
  });

  it('train the main muscles twice a week, and the questionnaire asks only about slots in the week', () => {
    for (const id of ['chest-upper', 'lats', 'row', 'side-delt', 'hamstring-curl', 'calves', 'shoulder-care'] as const) expect(slotExposures(id), id).toBe(2);
    for (const slot of ACTIVE_SLOTS) expect(slotExposures(slot.id), slot.id).toBeGreaterThanOrEqual(1);
    expect(ACTIVE_SLOTS.map((s) => s.id)).not.toContain('forearm-flexors');
    expect(ACTIVE_SLOTS.map((s) => s.id)).not.toContain('traps');
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

describe('the week', () => {
  const days = BASELINE_PLAN.days;

  it('has four gym strength days, two days without structured training, and no early morning sessions', () => {
    const gym = days.filter((d) => d.items.some((i) => i.session === 'main')).map((d) => d.weekday);
    expect(gym).toEqual([0, 1, 3, 4]);
    expect(days.find((d) => d.weekday === 2)!.isRest).toBe(true);
    expect(days.find((d) => d.weekday === 6)!.isRest).toBe(true);
    for (const d of days) expect(d.items.some((i) => i.session === 'morning' || i.session === 'swim'), d.key).toBe(false);
    expect(PROGRAM_DAYS.map((d) => d.title)).toEqual(['Upper A', 'Lower A', 'Upper B', 'Lower B']);
  });

  it('keeps gym and home apart: no jumps, sprints, or skills in the gym, and no gym strength work at home', () => {
    for (const opts of [{}, { home: ROOMY, wrist: 'cleared' as const }, { home: ROOMY, wrist: 'cleared' as const, jumpLevel: 'build' as const }]) {
      for (const d of planDaysFor(defaultPicks(), opts)) {
        for (const i of d.items) {
          const ex = exercise(i.exerciseId)!;
          if (i.session === 'main') {
            expect(GYM_ONLY_KINDS, `${d.key} ${i.exerciseId}`).not.toContain(ex.kind);
            expect(locationOf(i.exerciseId, ex.kind), i.exerciseId).toBe('gym');
          }
          if (i.session === 'home') {
            expect(['strength', 'hold'], `${d.key} ${i.exerciseId}`).not.toContain(ex.kind);
            expect(HOME_NEEDS[i.exerciseId as keyof typeof HOME_NEEDS], i.exerciseId).toBeDefined();
          }
        }
      }
    }
  });

  it('puts the home jumps on the gym leg days, before the gym, and never on consecutive days', () => {
    const full = planDaysFor(defaultPicks(), { home: ROOMY, wrist: 'cleared' });
    const jumpDays = full.filter((d) => d.items.some((i) => i.session === 'home' && exercise(i.exerciseId)?.kind === 'jump')).map((d) => d.weekday);
    expect(jumpDays).toEqual([1, 4]);
    for (const wd of jumpDays) {
      const sessions = full.find((d) => d.weekday === wd)!.items.map((i) => i.session);
      expect(sessions.indexOf('home')).toBeLessThan(sessions.indexOf('main'));
    }
    expect(items(full, 5, 'home').some((i) => exercise(i.exerciseId)?.kind === 'jump')).toBe(false);
  });

  it('prescribes no sets to failure: two reps in reserve for work sets, three for shoulder care', () => {
    for (const d of days)
      for (const it of d.items.filter((i) => i.session === 'main')) {
        if (it.rir !== undefined) expect(it.rir, it.id).toBeGreaterThanOrEqual(2);
        expect(it.lastSetRir, it.id).toBeUndefined();
        expect(FREE_BARBELL).not.toContain(it.exerciseId);
      }
    expect(items(days, 0, 'main')[0]).toMatchObject({ exerciseId: 'cable-external-rotation', rir: 3 });
    expect(GLOBAL_RULES.join(' ')).toMatch(/No routine sets to failure/);
  });

  it('keeps every gym session to 12 to 22 work sets and 75 minutes or less, counting every rest', () => {
    for (const d of PROGRAM_DAYS) {
      const it = items(days, d.weekday, 'main');
      const sets = it.reduce((n, i) => n + i.sets, 0);
      expect(sets, d.key).toBeGreaterThanOrEqual(12);
      expect(sets, d.key).toBeLessThanOrEqual(22);
      expect(sessionInfo(it, 'main').minutes, d.key).toBeLessThanOrEqual(75);
    }
  });

  it('gives each main muscle direct work every week without exceeding 20 sets', () => {
    const cov = coverageFrom(planCoverageInputs(days), lookup);
    const floors: Record<string, number> = { pec_clavicular: 4, pec_sternal: 4, lats: 9, traps_middle: 4, delt_lateral: 4, delt_posterior: 3, biceps: 4, triceps: 4, quads: 6, hamstrings: 6, glute_max: 6, glute_med: 2, adductors: 2, gastrocnemius: 4, rectus_abdominis: 2, rotator_cuff: 4 };
    for (const [m, min] of Object.entries(floors)) expect(cov[m as keyof typeof cov].direct, m).toBeGreaterThanOrEqual(min);
    for (const c of Object.values(cov)) expect(c.direct, c.muscle).toBeLessThanOrEqual(20);
  });

  it('starts every upper day with shoulder care and puts the big exercises before the small ones', () => {
    for (const wd of [0, 3]) expect(['cable-external-rotation', 'side-lying-external-rotation']).toContain(items(days, wd, 'main')[0]!.exerciseId);
    for (const d of PROGRAM_DAYS) {
      const it = items(days, d.weekday, 'main').filter((i) => exercise(i.exerciseId)?.kind === 'strength' && !['cable-external-rotation', 'side-lying-external-rotation'].includes(i.exerciseId));
      const firstSmall = it.findIndex((i) => i.restSec < 150);
      const lastBig = it.map((i) => i.restSec >= 150).lastIndexOf(true);
      if (firstSmall >= 0 && lastBig >= 0) expect(lastBig, d.key).toBeLessThan(firstSmall);
    }
  });

  it('builds the chosen exercises into the right days', () => {
    const picks = { ...defaultPicks(), 'side-delt': ['machine-lateral-raise' as const], quads: ['smith-squat' as const], glutes: ['walking-lunge' as const] };
    const built = planDaysFor(picks, { wrist: 'cleared' });
    const ids = (wd: number) => items(built, wd, 'main').map((i) => i.exerciseId);
    for (const wd of [0, 3]) expect(ids(wd)).toContain('machine-lateral-raise');
    expect(ids(1)).toContain('smith-squat');
    expect(ids(4)).toContain('walking-lunge');
  });

  it('labels every session with a location, equipment, space, duration, and stop rules', () => {
    const full = planDaysFor(defaultPicks(), { home: ROOMY, wrist: 'cleared' });
    for (const d of full)
      for (const s of ['home', 'main'] as const) {
        const it = d.items.filter((i) => i.session === s);
        if (!it.length) continue;
        const info = sessionInfo(it, s);
        expect(info.locationLabel).toBe(s === 'main' ? 'Gym' : 'Home');
        expect(info.equipment.length, `${d.key} ${s}`).toBeGreaterThan(0);
        expect(info.space.length).toBeGreaterThan(10);
        expect(info.minutes).toBeGreaterThanOrEqual(5);
        expect(info.stopRules.length).toBeGreaterThanOrEqual(2);
      }
  });
});

describe('home space decides the home drills', () => {
  it('reads unknown answers as the most limited room', () => {
    const [indoor] = environments(DEFAULT_HOME);
    expect(indoor).toMatchObject({ space: 'small', ceiling: 'low', maxImpact: 'none', quietOnly: true, ballOk: false });
    expect(environments(DEFAULT_HOME)).toHaveLength(1);
  });

  it('plans the full introductory session, about 65 landings, when the space allows it', () => {
    const it = buildHomeItems('mon', HOME_JUMP_SESSION.intro, ROOMY, 'cleared');
    expect(it.map((i) => i.exerciseId)).toEqual(['home-movement-prep', 'snap-down-stick', 'pogo-hop', 'lateral-line-hop', 'countermovement-jump', 'broad-jump', 'volleyball-approach-footwork', 'approach-touch-jump']);
    expect(contacts(it)).toBe(64);
    expect(it.find((i) => i.exerciseId === 'countermovement-jump')).toMatchObject({ sets: 2, target: { type: 'reps', min: 4, max: 4 }, restSec: 90 });
    expect(it.find((i) => i.exerciseId === 'countermovement-jump')!.notes.join(' ')).toMatch(/Outdoors/);
  });

  it('ends with full approach jumps after the approach footwork, outdoors, with full rest', () => {
    const it = buildHomeItems('mon', HOME_JUMP_SESSION.intro, ROOMY, 'cleared');
    const ids = it.map((i) => i.exerciseId);
    const jump = it.find((i) => i.exerciseId === 'approach-touch-jump')!;
    expect(ids.indexOf('approach-touch-jump')).toBe(ids.indexOf('volleyball-approach-footwork') + 1);
    expect(jump).toMatchObject({ sets: 2, target: { type: 'reps', min: 3, max: 3 }, restSec: 120 });
    expect(jump.notes.join(' ')).toMatch(/Outdoors/);
    expect(jump.notes.join(' ')).toMatch(/landings earlier in the session were clean/);
    // Without a wall to mark, the jump reaches for a spot in the air instead.
    const noWall = buildHomeItems('mon', HOME_JUMP_SESSION.intro, { ...ROOMY, equipment: ['tape'] }, 'cleared').map((i) => i.exerciseId);
    expect(noWall).toContain('volleyball-approach-jump');
    expect(noWall).not.toContain('approach-touch-jump');
    // Without an outdoor area or a hall, there is no full approach jump at all.
    const indoors = buildHomeItems('mon', HOME_JUMP_SESSION.intro, { ...ROOMY, outdoor: 'none' }, 'cleared').map((i) => i.exerciseId);
    expect(indoors.some((id) => id === 'approach-touch-jump' || id === 'volleyball-approach-jump')).toBe(false);
  });

  it('plans no jumps in a small flat with a low ceiling, tiles, and noise limits', () => {
    const it = buildHomeItems('mon', HOME_JUMP_SESSION.intro, SMALL_FLAT, 'cleared');
    expect(contacts(it)).toBe(0);
    for (const i of it) expect(exercise(i.exerciseId)!.kind).not.toBe('jump');
    expect(it.map((i) => i.exerciseId)).toContain('home-movement-prep');
  });

  it('swaps a drill for its quiet version when only the noise limit stops it, and says why', () => {
    const quiet: HomeSetup = { ...ROOMY, outdoor: 'none', noiseLimits: 'yes' };
    const c = chooseDrill(['pogo-hop', 'tibialis-raise'], quiet, 'cleared');
    expect(c?.exerciseId).toBe('tibialis-raise');
    expect(c?.passed[0]?.reasons).toContain('it is too loud for the noise limits');
    const it = buildHomeItems('mon', HOME_JUMP_SESSION.intro, quiet, 'cleared');
    expect(it.find((i) => i.exerciseId === 'tibialis-raise')!.notes[0]).toMatch(/Planned instead of Pogo Hop, because it is too loud/);
  });

  it('keeps maximal jumps away from a standard ceiling indoors', () => {
    const indoorOnly: HomeSetup = { ...ROOMY, outdoor: 'none' };
    const it = buildHomeItems('mon', HOME_JUMP_SESSION.intro, indoorOnly, 'cleared').map((i) => i.exerciseId);
    expect(it).not.toContain('countermovement-jump');
    expect(it).toContain('pogo-hop');
  });

  it('keeps the next level at about 95 landings and the skill session free of jumps', () => {
    expect(contacts(buildHomeItems('mon', HOME_JUMP_SESSION.build, ROOMY, 'cleared'))).toBe(94);
    expect(contacts(buildHomeItems('fri', HOME_SKILL_SESSION, ROOMY, 'cleared'))).toBe(0);
  });
});

describe('wrist clearance', () => {
  it('rates every library exercise', () => {
    for (const id of LIBRARY_IDS) expect(WRIST_LOAD[id], id).toBeDefined();
  });

  it('allows heavy wrist work only after clearance, and little with symptoms', () => {
    expect(maxWristLoad('cleared')).toBe('high');
    expect(maxWristLoad('unknown')).toBe('moderate');
    expect(maxWristLoad('not-cleared')).toBe('moderate');
    expect(maxWristLoad('symptoms')).toBe('low');
    expect(wristAllows('wall-spike-control', 'unknown')).toBe(false);
    expect(wristAllows('wall-spike-control', 'cleared')).toBe(true);
    expect(wristAllows('machine-bench-press', 'symptoms')).toBe(false);
    expect(wristHoldsLoad('machine-bench-press', 'unknown')).toBe(true);
    expect(wristHoldsLoad('machine-bench-press', 'cleared')).toBe(false);
    expect(wristHoldsLoad('leg-press', 'unknown')).toBe(false);
  });

  it('swaps a heavy wrist pick for an equivalent option until the wrist is cleared', () => {
    const picks = normalizePicks({ ...defaultPicks(), 'triceps-long': ['dumbbell-overhead-triceps-extension'] });
    const entry = { slot: 'triceps-long' as const, choice: 0 as const };
    expect(wristSafePick(picks, entry, 'cleared')).toBe('dumbbell-overhead-triceps-extension');
    expect(wristSafePick(picks, entry, 'unknown')).toBe(SLOT_BY_ID['triceps-long'].options.find((id) => WRIST_LOAD[id] !== 'high'));
    const sun = items(planDaysFor(picks, { wrist: 'unknown' }), 0, 'main');
    const swapped = sun.find((i) => i.exerciseId === 'rope-overhead-triceps-extension')!;
    expect(swapped.notes.join(' ')).toMatch(/while the wrist is not cleared/);
  });

  it('plans no ball contact before clearance, and the no ball arm swing instead', () => {
    const before = buildHomeItems('fri', HOME_SKILL_SESSION, ROOMY, 'not-cleared').map((i) => i.exerciseId);
    expect(before).not.toContain('wall-spike-control');
    expect(before).toContain('spike-arm-swing-shadow');
    expect(buildHomeItems('fri', HOME_SKILL_SESSION, ROOMY, 'cleared').map((i) => i.exerciseId)).toContain('wall-spike-control');
  });

  it('leaves out gripping and pressing exercises while the wrist has symptoms', () => {
    const sun = items(planDaysFor(defaultPicks(), { wrist: 'symptoms' }), 0, 'main');
    for (const i of sun) expect(['none', 'low']).toContain(WRIST_LOAD[i.exerciseId as keyof typeof WRIST_LOAD]);
  });
});

describe('plan changes', () => {
  it('rebuilds an older plan, drops the early morning and swim sessions, and keeps exercises the user created', () => {
    const before = baselinePlanRecord(0);
    before.days[1]!.items.unshift({ id: 'mon-rope', exerciseId: 'easy-jump-rope', session: 'morning', sets: 1, target: { type: 'duration', totalMin: 9 }, restSec: 30, notes: [] });
    before.days[0]!.items.push({ id: 'my-own', exerciseId: 'custom-abc', session: 'main', sets: 2, target: { type: 'reps', min: 10, max: 12 }, restSec: 60, notes: ['mine'] });
    const after = buildPlan(before, defaultPicks(), { home: ROOMY, wrist: { status: 'cleared', clearedBy: '', date: null, limits: '' } }, 'intro');
    expect(after.days.flatMap((d) => d.items).some((i) => i.session === 'morning')).toBe(false);
    expect(after.days[0]!.items.some((i) => i.id === 'my-own')).toBe(true);
    expect(after.globalRules).toEqual(GLOBAL_RULES);
  });

  it('shows a visible difference, day by day, with added, removed, and changed items', () => {
    const before = baselinePlanRecord(0);
    const after = structuredClone(before);
    const sun = after.days.find((d) => d.weekday === 0)!;
    sun.items[1] = { ...sun.items[1]!, sets: 4 };
    sun.items.push({ id: 'x', exerciseId: 'face-pull', session: 'main', sets: 2, target: { type: 'reps', min: 12, max: 15 }, restSec: 60, rir: 2, notes: [] });
    const removed = sun.items.splice(2, 1)[0]!;
    const diff = diffPlans(before, after);
    expect(diff).toHaveLength(1);
    expect(diff[0]!.dayName).toBe('Sunday');
    const kinds = Object.fromEntries(diff[0]!.changes.map((c) => [c.exerciseId, c.kind]));
    expect(kinds['face-pull']).toBe('added');
    expect(kinds[removed.exerciseId]).toBe('removed');
    expect(kinds[sun.items[1]!.exerciseId]).toBe('changed');
    expect(diffPlans(before, structuredClone(before))).toEqual([]);
  });
});

describe('four month planning', () => {
  it('runs in flexible stages from the plan start and never changes the plan by itself', () => {
    expect(PLANNING_PHASES.map((p) => p.id)).toEqual(['assess', 'progress', 'consolidate', 'review']);
    expect(planningPhaseFor(null, '2026-10-06')).toBeNull();
    expect(planningPhaseFor('2026-10-05', '2026-10-06')!.id).toBe('assess');
    expect(planningPhaseFor('2026-10-05', '2026-11-05')!.id).toBe('progress');
    expect(planningPhaseFor('2026-10-05', '2027-06-01')!.id).toBe('review');
    for (const p of PLANNING_PHASES) expect(p.processGoals.length).toBeGreaterThan(0);
    const text = JSON.stringify(PLANNING_PHASES);
    expect(text).not.toMatch(/\d+ ?% body fat|kg of muscle|dunk/i);
  });

  it('plans a jump measurement every four weeks', () => {
    expect(nextMeasurementDate('2026-10-05', '2026-10-05')).toBe('2026-10-05');
    expect(nextMeasurementDate('2026-10-05', '2026-10-06')).toBe('2026-11-02');
    expect(nextMeasurementDate(null, '2026-10-06')).toBeNull();
  });
});

describe('exercise library', () => {
  it('describes effort for every loaded exercise and never prescribes failure on free barbell lifts', () => {
    for (const ex of LIBRARY) {
      if (['strength', 'bodyweight', 'hold'].includes(ex.kind)) expect(ex.failure, ex.id).toBeDefined();
      if (FREE_BARBELL.includes(ex.id)) expect(ex.failure).toBe('never');
    }
    expect(LIBRARY).toHaveLength(103);
  });
});
