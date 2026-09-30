import type { LibraryExerciseId } from './exercises/ids';
import { PROGRAM_DAYS, buildMainItems, defaultPicks, normalizePicks, type ProgramPicks } from './program';

// The baseline weekly plan. Seeded exactly as prescribed.
// Plan data is separate from logged data. Editing a plan creates a new plan version;
// sessions store a snapshot of the prescription they were performed against.

export type Weekday = 0 | 1 | 2 | 3 | 4 | 5 | 6; // 0 = Sunday, matching Date.getDay()

export type SetTarget =
  | { type: 'reps'; min: number; max: number }
  | { type: 'duration'; totalMin: number; workSec?: number; restSec?: number }
  | { type: 'hold'; seconds: number }
  | { type: 'roundTrips'; count: number };

export type SessionKey = 'morning' | 'main' | 'swim';

export interface PlanItem {
  id: string;
  exerciseId: LibraryExerciseId | string;
  session: SessionKey;
  sets: number;
  target: SetTarget;
  /** Rest between sets in seconds. */
  restSec: number;
  /** Prescribed reps in reserve, when relevant. 0 means to technical failure. */
  rir?: number;
  /** Reps in reserve for the last set only, when it differs from the others. */
  lastSetRir?: number;
  /** Target RPE range for aerobic work. */
  rpe?: [number, number];
  /** Tempo as four digits: lowering, pause, lifting, pause. */
  tempo?: string;
  /** Per side or per direction. */
  per?: 'side' | 'direction';
  notes: string[];
}

export interface PlanDay {
  weekday: Weekday;
  key: 'sun' | 'mon' | 'tue' | 'wed' | 'thu' | 'fri' | 'sat';
  title: string;
  short: string;
  isRest: boolean;
  items: PlanItem[];
  restNotes?: string[];
}

export interface WorkoutPlan {
  id: string;
  version: number;
  name: string;
  createdAt: string;
  days: PlanDay[];
  globalRules: string[];
}

const ROPE_NOTE_QUALITY = 'Stop when speed, jump height, landing control, or technique declines.';
const SWIM_SPACING = 'Separate swimming from the main workout by at least three hours when possible.';

function rope(day: PlanDay['key'], totalMin: number, extra: string[] = []): PlanItem {
  return {
    id: `${day}-rope`,
    exerciseId: 'easy-jump-rope',
    session: 'morning',
    sets: 1,
    target: { type: 'duration', totalMin, workSec: 60, restSec: 30 },
    restSec: 30,
    notes: ['1 minute easy work and 30 seconds rest.', 'No double unders.', ROPE_NOTE_QUALITY, ...extra],
  };
}

function swim(day: PlanDay['key']): PlanItem {
  return {
    id: `${day}-swim`,
    exerciseId: 'easy-pool-round-trip',
    session: 'swim',
    sets: 2,
    target: { type: 'roundTrips', count: 10 },
    restSec: 300,
    rpe: [4, 5],
    notes: [
      'Twenty round trips in total, with a five minute break after the first ten.',
      'Easy to moderate effort, RPE 4 to 5.',
      SWIM_SPACING,
      'Distance depends on pool length. Set it in the log.',
    ],
  };
}

const r = (min: number, max: number): SetTarget => ({ type: 'reps', min, max });

type ItemInput = Omit<PlanItem, 'id' | 'session' | 'notes'> & { notes?: string[]; session?: SessionKey };

const AM_NOTE = 'Home session at 05:30 with no ball: a rope, a few light dumbbells, and some floor space. Rope first as the warm up.';

/** Morning volleyball work added after the baseline: footwork without a ball, shoulder care, and trunk control. */
function morning(day: PlanDay['key'], list: ItemInput[]): PlanItem[] {
  return list.map((it, i) => ({
    ...it,
    id: `${day}-am-${i + 1}-${it.exerciseId}`,
    session: 'morning',
    notes: it.notes ?? [],
  }));
}

const PASS = (sets = 3): ItemInput => ({ exerciseId: 'shadow-pass-footwork', sets, target: r(8, 8), restSec: 45, notes: [AM_NOTE, 'Eight directions per set, exact rather than fast.'] });
const BLOCK = (sets = 3): ItemInput => ({ exerciseId: 'block-footwork', sets, target: r(6, 6), restSec: 45, notes: ['Six moves per set. No jump, or only a tiny soft hop at the stop.'] });
const YRAISE: ItemInput = { exerciseId: 'dumbbell-y-raise', sets: 2, target: r(12, 15), restSec: 60, rir: 3, tempo: '3011', notes: ['Light dumbbells, usually 1 to 3 kg.'] };
const EXTROT: ItemInput = { exerciseId: 'side-lying-external-rotation', sets: 2, target: r(12, 15), restSec: 45, rir: 3, tempo: '3011', per: 'side', notes: ['Light dumbbell, usually 1 to 2 kg.'] };
const DEADBUG: ItemInput = { exerciseId: 'dead-bug', sets: 2, target: r(6, 8), restSec: 45, rir: 3, per: 'side' };

/** Morning home sessions at 05:30: rope first as the warm up, then footwork, shoulder care, and trunk work. */
const MORNING: Record<Exclude<PlanDay['key'], 'sat'>, PlanItem[]> = {
  sun: [rope('sun', 6), ...morning('sun', [PASS(), DEADBUG, { exerciseId: 'tibialis-raise', sets: 2, target: r(15, 20), restSec: 45, rir: 2 }])],
  mon: [rope('mon', 9), ...morning('mon', [BLOCK(), YRAISE, EXTROT])],
  tue: [rope('tue', 9), ...morning('tue', [PASS(), DEADBUG])],
  wed: [rope('wed', 9), ...morning('wed', [BLOCK(), YRAISE, EXTROT])],
  thu: [rope('thu', 15), ...morning('thu', [PASS(), DEADBUG])],
  fri: [rope('fri', 6), ...morning('fri', [PASS(2), DEADBUG])],
};

export const GLOBAL_RULES = [
  'Morning volleyball sessions at 05:30 stay easy: footwork without a ball, light shoulder care, and trunk control. Hard jumps and heavy work stay in the main session.',
  'One exercise for each muscle head, three work sets, with a slow, controlled stretch at the long muscle length.',
  'Warm up sets do not count as working sets. Do one or two lighter sets before the first exercise for a muscle.',
  'Failure means the last rep you can finish with clean form. Never cheat, bounce, or grind out a rep.',
  'Machines, cables, and the Smith machine with safety stops go to failure as prescribed. Dumbbell presses, lunges, and hinges stop one rep short. No free barbell when you train alone.',
  'For a new exercise, stop two reps short for the first two sessions while you learn it.',
  'Rest two to three minutes on the big exercises and about ninety seconds on the small ones.',
  'Do not test a one repetition maximum.',
  'No leg sets to failure in the 48 hours before a volleyball match.',
  'Stop explosive work as soon as quality drops.',
  'Separate swimming and the main workout by at least three hours when possible.',
  'Do not add extra high intensity intervals.',
  'Take a reduced week when performance, sleep, pain, or motivation show accumulated fatigue.',
];

/** Builds the week from program choices. Morning sessions and swims are fixed. */
export function planDaysFor(picks: ProgramPicks | undefined): PlanDay[] {
  const chosen = normalizePicks(picks);
  const days: PlanDay[] = PROGRAM_DAYS.map((d) => ({
    weekday: d.weekday,
    key: d.key,
    title: d.title,
    short: d.short,
    isRest: false,
    items: [...MORNING[d.key as Exclude<PlanDay['key'], 'sat'>], ...buildMainItems(d, chosen), ...(d.key === 'sun' || d.key === 'fri' ? [swim(d.key)] : [])],
  }));
  days.push({
    weekday: 6,
    key: 'sat',
    title: 'Full Rest',
    short: 'Rest',
    isRest: true,
    items: [],
    restNotes: [
      'No formal training.',
      'Comfortable walking is fine if you feel like it.',
      'Sabbath Mode keeps the app quiet.',
      'No make up workout and no food rules to compensate.',
    ],
  });
  return days;
}

export const BASELINE_PLAN: WorkoutPlan = {
  id: 'baseline',
  version: 1,
  name: 'PeakForm baseline week',
  createdAt: '2026-09-29T00:00:00.000Z',
  globalRules: GLOBAL_RULES,
  days: planDaysFor(defaultPicks()),
};

export const SESSION_LABELS: Record<SessionKey, string> = {
  morning: 'Morning volleyball and rope',
  main: 'Main session',
  swim: 'Swim',
};

export function planDay(plan: WorkoutPlan, weekday: number): PlanDay {
  const d = plan.days.find((x) => x.weekday === weekday);
  if (!d) throw new Error(`Plan has no day for weekday ${weekday}`);
  return d;
}

export function sessionItems(day: PlanDay, session: SessionKey): PlanItem[] {
  return day.items.filter((i) => i.session === session);
}

export function sessionsForDay(day: PlanDay): SessionKey[] {
  const order: SessionKey[] = ['morning', 'main', 'swim'];
  return order.filter((s) => day.items.some((i) => i.session === s));
}

/** Optional taper for the week of a target event. Never includes dehydration or food restriction. */
export const TAPER_TEMPLATE = [
  { offsetDays: -3, label: 'Reduced strength volume', detail: 'Do the planned session with about half the working sets. Keep loads and reps in reserve the same.' },
  { offsetDays: -2, label: 'Light skills', detail: 'Short volleyball skills and easy movement only. No hard jumps or sprints.' },
  { offsetDays: -1, label: 'Rest', detail: 'Rest, eat normally, and sleep on time.' },
  { offsetDays: 0, label: 'Optional short easy pump', detail: 'A few light sets in the morning if you want. Eat and drink normally. No dehydration, no skipped meals.' },
] as const;
