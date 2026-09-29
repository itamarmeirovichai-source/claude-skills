import type { LibraryExerciseId } from './exercises/ids';

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
  /** Prescribed reps in reserve, when relevant. */
  rir?: number;
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
const QUALITY_FIRST = 'Quality first. Stop the set when height, speed, landing control, or coordination drops.';
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

function items(day: PlanDay['key'], list: ItemInput[]): PlanItem[] {
  return list.map((it, i) => ({
    ...it,
    id: `${day}-${i + 1}-${it.exerciseId}`,
    session: it.session ?? 'main',
    notes: it.notes ?? [],
  }));
}


export const BASELINE_PLAN: WorkoutPlan = {
  id: 'baseline',
  version: 1,
  name: 'PeakForm baseline week',
  createdAt: '2026-09-29T00:00:00.000Z',
  globalRules: [
    'Morning volleyball sessions at 05:30 stay easy: footwork without a ball, light shoulder care, and trunk control. Hard jumps and heavy work stay in the main session.',
    'Warm up sets do not count as working sets.',
    'Use controlled technique on every rep.',
    'Learn unfamiliar barbell and jump movements with a qualified coach.',
    'Do not test a one repetition maximum.',
    'Do not take routine sets to failure.',
    'Keep two to three repetitions in reserve as prescribed.',
    'Stop explosive work as soon as quality drops.',
    'Separate swimming and the main workout by at least three hours when possible.',
    'Do not add extra high intensity intervals.',
    'Take a reduced week when performance, sleep, pain, or motivation show accumulated fatigue.',
  ],
  days: [
    {
      weekday: 0,
      key: 'sun',
      title: 'Upper A and Swim',
      short: 'Upper A',
      isRest: false,
      items: [
        rope('sun', 6),
        ...morning('sun', [PASS(), DEADBUG, { exerciseId: 'tibialis-raise', sets: 2, target: r(15, 20), restSec: 45, rir: 2 }]),
        ...items('sun', [
          { exerciseId: 'barbell-bench-press', sets: 3, target: r(8, 12), restSec: 150, rir: 2, notes: ['Medium grip.'] },
          { exerciseId: 'flat-cable-fly', sets: 2, target: r(12, 15), restSec: 90, rir: 2 },
          { exerciseId: 'seated-cable-row', sets: 3, target: r(8, 12), restSec: 150, rir: 2 },
          { exerciseId: 'one-arm-lat-pulldown', sets: 2, target: r(10, 15), restSec: 120, rir: 2, per: 'side' },
          { exerciseId: 'single-arm-cable-lateral-raise', sets: 2, target: r(12, 20), restSec: 90, rir: 2, per: 'side' },
          { exerciseId: 'machine-preacher-curl', sets: 2, target: r(10, 15), restSec: 90, rir: 2 },
          { exerciseId: 'palm-up-wrist-curl', sets: 2, target: r(12, 20), restSec: 90, rir: 2 },
          { exerciseId: 'rope-overhead-triceps-extension', sets: 2, target: r(10, 15), restSec: 90, rir: 2 },
          { exerciseId: 'cable-external-rotation', sets: 2, target: r(15, 20), restSec: 75, rir: 3 },
        ]),
        swim('sun'),
      ],
    },
    {
      weekday: 1,
      key: 'mon',
      title: 'Lower A Strength and Jump',
      short: 'Lower A',
      isRest: false,
      items: [
        rope('mon', 9),
        ...morning('mon', [BLOCK(), YRAISE, EXTROT]),
        ...items('mon', [
          { exerciseId: 'dynamic-volleyball-warm-up', sets: 1, target: { type: 'duration', totalMin: 8 }, restSec: 30 },
          { exerciseId: 'volleyball-approach-jump', sets: 3, target: r(2, 2), restSec: 180, notes: [QUALITY_FIRST] },
          { exerciseId: 'countermovement-jump', sets: 3, target: r(2, 2), restSec: 150, notes: [QUALITY_FIRST] },
          { exerciseId: 'barbell-squat', sets: 3, target: r(6, 10), restSec: 180, rir: 3, tempo: '3110' },
          { exerciseId: 'romanian-deadlift', sets: 3, target: r(8, 12), restSec: 180, rir: 3, tempo: '3110' },
          { exerciseId: 'bulgarian-split-squat', sets: 2, target: r(8, 12), restSec: 150, rir: 3, per: 'side' },
          { exerciseId: 'standing-calf-raise', sets: 3, target: r(10, 15), restSec: 120, rir: 2, tempo: '2111' },
          { exerciseId: 'tibialis-raise', sets: 2, target: r(15, 20), restSec: 75, rir: 3 },
          { exerciseId: 'pallof-press', sets: 2, target: r(10, 15), restSec: 75, rir: 3, per: 'side' },
        ]),
      ],
    },
    {
      weekday: 2,
      key: 'tue',
      title: 'Upper C Hypertrophy',
      short: 'Upper C',
      isRest: false,
      items: [
        rope('tue', 9),
        ...morning('tue', [PASS(), DEADBUG]),
        ...items('tue', [
          { exerciseId: 'incline-dumbbell-press', sets: 3, target: r(8, 12), restSec: 150, rir: 2, tempo: '3110' },
          { exerciseId: 'chest-supported-dumbbell-row', sets: 3, target: r(10, 12), restSec: 150, rir: 2, tempo: '2011' },
          { exerciseId: 'flat-cable-fly', sets: 2, target: r(12, 15), restSec: 90, rir: 2 },
          { exerciseId: 'lateral-raise', sets: 3, target: r(12, 20), restSec: 90, rir: 2 },
          { exerciseId: 'face-pull', sets: 2, target: r(12, 20), restSec: 75, rir: 3 },
          { exerciseId: 'incline-dumbbell-curl', sets: 3, target: r(10, 15), restSec: 90, rir: 2, tempo: '3011' },
          { exerciseId: 'rope-overhead-triceps-extension', sets: 3, target: r(10, 15), restSec: 90, rir: 2 },
        ]),
      ],
    },
    {
      weekday: 3,
      key: 'wed',
      title: 'Lower B Hypertrophy',
      short: 'Lower B',
      isRest: false,
      items: [
        rope('wed', 9),
        ...morning('wed', [BLOCK(), YRAISE, EXTROT]),
        ...items('wed', [
          { exerciseId: 'hack-squat', sets: 3, target: r(8, 12), restSec: 180, rir: 2, tempo: '3110' },
          { exerciseId: 'barbell-hip-thrust', sets: 3, target: r(8, 12), restSec: 150, rir: 2, tempo: '2111' },
          { exerciseId: 'seated-leg-curl', sets: 3, target: r(10, 15), restSec: 120, rir: 2, tempo: '2111' },
          { exerciseId: 'leg-extension', sets: 2, target: r(12, 15), restSec: 90, rir: 2, tempo: '2111' },
          { exerciseId: 'cable-hip-abduction', sets: 2, target: r(12, 20), restSec: 90, rir: 2, per: 'side' },
          { exerciseId: 'seated-calf-raise', sets: 3, target: r(12, 20), restSec: 120, rir: 2, tempo: '2111' },
          { exerciseId: 'copenhagen-plank', sets: 2, target: { type: 'hold', seconds: 20 }, restSec: 75, per: 'side' },
          { exerciseId: 'hanging-leg-raise', sets: 2, target: r(8, 15), restSec: 75, rir: 3 },
        ]),
      ],
    },
    {
      weekday: 4,
      key: 'thu',
      title: 'Upper B Hypertrophy',
      short: 'Upper B',
      isRest: false,
      items: [
        rope('thu', 15),
        ...morning('thu', [PASS(), DEADBUG]),
        ...items('thu', [
          { exerciseId: 'incline-barbell-bench-press', sets: 3, target: r(8, 12), restSec: 150, rir: 2, notes: ['Medium grip.'] },
          { exerciseId: 'machine-bench-press', sets: 2, target: r(8, 12), restSec: 150, rir: 2 },
          { exerciseId: 'wide-grip-lat-pulldown', sets: 3, target: r(8, 12), restSec: 150, rir: 2 },
          { exerciseId: 'leverage-high-row', sets: 3, target: r(10, 15), restSec: 150, rir: 2 },
          { exerciseId: 'reverse-machine-fly', sets: 2, target: r(12, 20), restSec: 90, rir: 2 },
          { exerciseId: 'lateral-raise', sets: 2, target: r(12, 20), restSec: 90, rir: 2 },
          { exerciseId: 'hammer-curl', sets: 2, target: r(10, 15), restSec: 90, rir: 2 },
          { exerciseId: 'palm-down-wrist-curl', sets: 2, target: r(12, 20), restSec: 90, rir: 2 },
          { exerciseId: 'triceps-pushdown', sets: 2, target: r(10, 15), restSec: 90, rir: 2 },
        ]),
      ],
    },
    {
      weekday: 5,
      key: 'fri',
      title: 'Lower C Hypertrophy and Swim',
      short: 'Lower C',
      isRest: false,
      items: [
        rope('fri', 6),
        ...morning('fri', [PASS(2), DEADBUG]),
        ...items('fri', [
          { exerciseId: 'leg-press', sets: 3, target: r(10, 15), restSec: 180, rir: 2, tempo: '3110' },
          { exerciseId: 'back-extension', sets: 3, target: r(10, 15), restSec: 120, rir: 3, tempo: '2011' },
          { exerciseId: 'nordic-hamstring-curl', sets: 2, target: r(4, 6), restSec: 180, rir: 3, notes: ['Difficulty never increases automatically.'] },
          { exerciseId: 'seated-leg-curl', sets: 2, target: r(10, 15), restSec: 120, rir: 2, tempo: '2111' },
          { exerciseId: 'cable-hip-adduction', sets: 2, target: r(12, 15), restSec: 75, rir: 2, per: 'side' },
          { exerciseId: 'cable-hip-abduction', sets: 2, target: r(12, 20), restSec: 75, rir: 2, per: 'side' },
          { exerciseId: 'standing-calf-raise', sets: 3, target: r(10, 15), restSec: 120, rir: 2, tempo: '2111' },
        ]),
        swim('fri'),
      ],
    },
    {
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
    },
  ],
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
