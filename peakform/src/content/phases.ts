import { addDays, diffDays, type DateKey } from '../domain/dates';
import type { LibraryExerciseId } from './exercises/ids';

// The jump program for the dunk goal, 5 October 2026 to 31 January 2027, in training blocks.
// Jumps come first on Monday and Friday, then heavy leg work that stops short of failure.
// Wednesday is the lighter leg day, so Friday's jumps are done on fresh legs.
// Contacts per session start near 50 and stay under about 100, as youth plyometric guidance
// advises, and every block ends with lower volume before a jump test.

/** How a leg exercise is dosed in each block. `rirMin` is a floor: sets stop at least that far from failure. */
export type DoseKey = 'heavy' | 'hinge' | 'wedMain' | 'wedSmall' | 'friMain' | 'friSmall';

export interface Dose {
  sets: number;
  reps?: [number, number];
  rirMin?: number;
  restSec?: number;
}

export interface JumpDrill {
  exerciseId: LibraryExerciseId;
  sets: number;
  reps: number;
  restSec: number;
  per?: 'side';
  notes?: string[];
}

export type PhaseId = 'foundation' | 'power' | 'deload-1' | 'reactive' | 'deload-2' | 'realize' | 'taper' | 'build';

export interface ProgramPhase {
  id: PhaseId;
  name: string;
  /** Monday the block starts. */
  start: DateKey;
  /** Sunday the block ends, or null for the open ended block after the goal date. */
  end: DateKey | null;
  summary: string;
  /** Monday jumps, before the heavy leg work. */
  jumpsMon: JumpDrill[];
  /** Jumps paired with the heavy leg exercise on Monday. */
  complexMon: JumpDrill[];
  /** Friday jumps: the approach and the dunk. */
  jumpsFri: JumpDrill[];
  doses: Record<DoseKey, Dose>;
}

const FULL = 'Full effort on every jump with full rest. Stop the drill as soon as height or landing quality drops.';
const STEP_DOWN = 'Step down from the box. Do not jump down.';
const TOUCH = 'Log the height you touch in Reach. The rim is 305 cm.';
const COMPLEX = 'Do one set 2 to 3 minutes after each set of the heavy leg exercise above.';
const BUILD_UP = 'First 2 or 3 slow walk throughs of the last two steps, then 3 or 4 run ups at about 80 percent.';

const pogo = (sets: number, reps: number): JumpDrill => ({ exerciseId: 'pogo-hop', sets, reps, restSec: 60, notes: ['Quick, light contacts. Part warm up, part ankle spring.'] });
const snap = (sets: number, reps: number): JumpDrill => ({ exerciseId: 'snap-down-stick', sets, reps, restSec: 60, notes: ['Freeze each landing for 2 seconds.'] });
const box = (sets: number, reps: number, notes: string[] = []): JumpDrill => ({ exerciseId: 'box-jump', sets, reps, restSec: 90, notes: [...notes, STEP_DOWN, FULL] });
const hurdle = (sets: number, reps: number, height: string): JumpDrill => ({ exerciseId: 'hurdle-hop', sets, reps, restSec: 90, notes: [`Hurdles or cones ${height}.`, FULL] });
const broad = (sets: number, reps: number): JumpDrill => ({ exerciseId: 'broad-jump', sets, reps, restSec: 90, notes: ['Stick every landing.'] });
const depth = (sets: number, reps: number, note: string): JumpDrill => ({ exerciseId: 'depth-jump', sets, reps, restSec: 120, notes: [note, 'Step off the box, do not jump off it.', FULL] });
const oneLeg = (sets: number, reps: number, note?: string): JumpDrill => ({ exerciseId: 'single-leg-hop', sets, reps, restSec: 60, per: 'side', notes: note ? [note] : [] });
const approach = (reps: number, notes: string[]): JumpDrill => ({ exerciseId: 'approach-touch-jump', sets: reps, reps: 1, restSec: 90, notes: [...notes, TOUCH] });

const LIGHT: Record<DoseKey, Dose> = {
  heavy: { sets: 2, reps: [4, 6], rirMin: 3, restSec: 180 },
  hinge: { sets: 2, reps: [6, 8], rirMin: 3, restSec: 150 },
  wedMain: { sets: 2, reps: [8, 10], rirMin: 3 },
  wedSmall: { sets: 1, rirMin: 2 },
  friMain: { sets: 2, reps: [6, 8], rirMin: 3, restSec: 150 },
  friSmall: { sets: 1, rirMin: 3 },
};

const REACTIVE: Omit<ProgramPhase, 'id' | 'name' | 'start' | 'end' | 'summary'> = {
  jumpsMon: [pogo(2, 15), depth(3, 5, 'Use the box height where you rebound fastest. Go up to 40 cm only if the rebound stays quick.'), hurdle(3, 5, '30 to 45 cm'), broad(2, 3)],
  complexMon: [box(3, 2, [COMPLEX])],
  jumpsFri: [approach(10, [BUILD_UP, 'Aim for the rim or the backboard. Use the takeoff that touches higher.', FULL]), oneLeg(2, 4, 'Short single leg bounds forward if you take off from one foot.'), hurdle(2, 4, '30 to 45 cm')],
  doses: {
    heavy: { sets: 3, reps: [3, 5], rirMin: 2, restSec: 180 },
    hinge: { sets: 3, reps: [5, 6], rirMin: 2, restSec: 150 },
    wedMain: { sets: 2, reps: [8, 10], rirMin: 2 },
    wedSmall: { sets: 2, rirMin: 1 },
    friMain: { sets: 3, reps: [5, 6], rirMin: 2, restSec: 150 },
    friSmall: { sets: 2, rirMin: 2 },
  },
};

export const PHASES: ProgramPhase[] = [
  {
    id: 'foundation',
    name: 'Block 1: Landing and technique',
    start: '2026-10-05',
    end: '2026-11-01',
    summary: 'Four weeks of landings, box jumps, low hurdles, and the dunk approach, about 50 jumps a session. Legs go heavy but stop two reps short.',
    jumpsMon: [pogo(2, 10), snap(2, 5), box(3, 3), hurdle(2, 4, '15 to 30 cm'), broad(2, 3)],
    complexMon: [],
    jumpsFri: [approach(6, [BUILD_UP, 'Alternate two foot and one foot takeoffs to find the one that touches higher.', FULL]), oneLeg(2, 5, 'Low, quick hops in place.')],
    doses: {
      heavy: { sets: 3, reps: [6, 8], rirMin: 2, restSec: 180 },
      hinge: { sets: 3, reps: [8, 10], rirMin: 2, restSec: 150 },
      wedMain: { sets: 3, reps: [8, 10], rirMin: 2 },
      wedSmall: { sets: 2, rirMin: 1 },
      friMain: { sets: 3, reps: [6, 8], rirMin: 2, restSec: 150 },
      friSmall: { sets: 2, rirMin: 2 },
    },
  },
  {
    id: 'power',
    name: 'Block 2: Strength and power',
    start: '2026-11-02',
    end: '2026-11-22',
    summary: 'Depth jumps start, and box jumps are paired with heavy sets of the leg exercise. Fewer reps with more weight, still two reps short.',
    jumpsMon: [pogo(2, 10), depth(3, 4, 'In the first week try 20, 30, and 40 cm, and keep the height where you rebound fastest and highest. Start at 20 to 30 cm.'), hurdle(3, 5, '30 to 45 cm'), broad(2, 3)],
    complexMon: [box(4, 2, [COMPLEX])],
    jumpsFri: [approach(8, [BUILD_UP, 'Use the takeoff that touched higher. A few with the other one keep it fresh.', FULL]), oneLeg(2, 5), hurdle(2, 4, '30 to 45 cm')],
    doses: {
      heavy: { sets: 4, reps: [4, 6], rirMin: 2, restSec: 180 },
      hinge: { sets: 3, reps: [6, 8], rirMin: 2, restSec: 150 },
      wedMain: { sets: 2, reps: [8, 10], rirMin: 2 },
      wedSmall: { sets: 2, rirMin: 1 },
      friMain: { sets: 3, reps: [6, 8], rirMin: 2, restSec: 150 },
      friSmall: { sets: 2, rirMin: 2 },
    },
  },
  {
    id: 'deload-1',
    name: 'Lighter week and jump test',
    start: '2026-11-23',
    end: '2026-11-29',
    summary: 'About 60 percent of the usual jumps and sets, so your legs are fresh for the jump test on Friday.',
    jumpsMon: [pogo(2, 10), box(3, 2), hurdle(2, 4, '30 cm')],
    complexMon: [],
    jumpsFri: [approach(5, [BUILD_UP, 'Test day: your best touch counts.', FULL])],
    doses: LIGHT,
  },
  { id: 'reactive', name: 'Block 3: Reactive and specific', start: '2026-11-30', end: '2026-12-27', summary: 'More depth jumps and hurdle hops, and up to 10 approach jumps at the rim. Heavy sets drop to 3 to 5 reps.', ...REACTIVE },
  {
    id: 'deload-2',
    name: 'Lighter week',
    start: '2026-12-28',
    end: '2027-01-03',
    summary: 'About half the usual jumps and no depth jumps, so the last block starts fresh.',
    jumpsMon: [pogo(2, 10), box(3, 2), hurdle(2, 4, '30 cm')],
    complexMon: [],
    jumpsFri: [approach(6, [BUILD_UP, FULL])],
    doses: LIGHT,
  },
  {
    id: 'realize',
    name: 'Block 4: Dunk practice',
    start: '2027-01-04',
    end: '2027-01-24',
    summary: 'Fewer drills and more maximal approach jumps, with dunk attempts using a smaller ball first. Leg work drops to keep you fresh.',
    jumpsMon: [pogo(2, 10), depth(2, 4, 'Use your best box height from block 3.'), hurdle(2, 4, '30 to 45 cm')],
    complexMon: [box(2, 2, [COMPLEX])],
    jumpsFri: [approach(12, [BUILD_UP, 'After 4 touches, try dunks with a smaller ball: a tennis ball, then a volleyball, then a small basketball. Full rest between attempts.', FULL]), oneLeg(1, 5)],
    doses: {
      heavy: { sets: 2, reps: [3, 5], rirMin: 2, restSec: 180 },
      hinge: { sets: 2, reps: [5, 6], rirMin: 2, restSec: 150 },
      wedMain: { sets: 2, reps: [8, 10], rirMin: 2 },
      wedSmall: { sets: 1, rirMin: 1 },
      friMain: { sets: 2, reps: [5, 6], rirMin: 2, restSec: 150 },
      friSmall: { sets: 1, rirMin: 2 },
    },
  },
  {
    id: 'taper',
    name: 'Taper and final test',
    start: '2027-01-25',
    end: '2027-01-31',
    summary: 'Half the volume at the same intensity. Friday is the final test and your dunk attempts.',
    jumpsMon: [pogo(2, 8), depth(2, 3, 'Your usual box height.'), box(2, 2)],
    complexMon: [],
    jumpsFri: [approach(8, [BUILD_UP, 'Final test: your best touch first, then the dunk attempts.', FULL])],
    doses: {
      heavy: { sets: 2, reps: [3, 4], rirMin: 3, restSec: 180 },
      hinge: { sets: 2, reps: [5, 6], rirMin: 3, restSec: 150 },
      wedMain: { sets: 1, reps: [8, 10], rirMin: 3 },
      wedSmall: { sets: 1, rirMin: 2 },
      friMain: { sets: 1, reps: [5, 6], rirMin: 3, restSec: 150 },
      friSmall: { sets: 1, rirMin: 3 },
    },
  },
  { id: 'build', name: 'Keep building', start: '2027-02-01', end: null, summary: 'The block 3 week continues, with a jump test every four weeks.', ...REACTIVE },
];

export const PHASE_BY_ID = Object.fromEntries(PHASES.map((p) => [p.id, p])) as Record<PhaseId, ProgramPhase>;

/** The block for a date. Dates before the first block use the first one. */
export function phaseFor(date: DateKey): ProgramPhase {
  return PHASES.find((p) => date >= p.start && (p.end === null || date <= p.end)) ?? PHASES[0]!;
}

/** Fridays of the jump tests: the baseline, the end of each block, and the final test. Then every four weeks. */
export const JUMP_TEST_DATES: DateKey[] = ['2026-10-09', '2026-10-30', '2026-11-27', '2026-12-25', '2027-01-22', '2027-01-29'];

export function nextJumpTest(today: DateKey): DateKey {
  const planned = JUMP_TEST_DATES.find((d) => d >= today);
  if (planned) return planned;
  const last = JUMP_TEST_DATES[JUMP_TEST_DATES.length - 1]!;
  const weeks = Math.ceil(diffDays(today, last) / 28);
  return addDays(last, Math.max(1, weeks) * 28);
}

export function isJumpTestDay(date: DateKey): boolean {
  return nextJumpTest(date) === date;
}

/** Foot contacts in a list of drills. A per side drill counts both legs. */
export function contacts(drills: JumpDrill[]): number {
  return drills.reduce((n, d) => n + d.sets * d.reps * (d.per === 'side' ? 2 : 1), 0);
}
