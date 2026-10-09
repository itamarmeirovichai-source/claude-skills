import type { LibraryExerciseId } from './exercises/ids';
import { PROGRAM_DAYS, buildMainItems, defaultPicks, normalizePicks, type ProgramPicks } from './program';
import { HOME_JUMP_SESSION, HOME_SKILL_SESSION, buildHomeItems, type JumpLevel } from './homeSessions';
import type { WristStatus } from './traits';
import { DEFAULT_HOME, type HomeSetup } from '../domain/athlete';

// The weekly plan. Seeded from the program and the athlete's choices.
// Plan data is separate from logged data. Editing a plan creates a new plan version;
// sessions store a snapshot of the prescription they were performed against.

export type Weekday = 0 | 1 | 2 | 3 | 4 | 5 | 6; // 0 = Sunday, matching Date.getDay()

export type SetTarget =
  | { type: 'reps'; min: number; max: number }
  | { type: 'duration'; totalMin: number; workSec?: number; restSec?: number }
  | { type: 'hold'; seconds: number }
  | { type: 'roundTrips'; count: number };

/** 'morning' only exists in plans saved before 3.0.0. 'main' is the gym strength session. */
export type SessionKey = 'morning' | 'home' | 'main' | 'swim';

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

export const GLOBAL_RULES = [
  'Gym sessions are for strength. Jumps, landings, footwork, and volleyball skills happen at home, never inside a gym session.',
  'On Monday and Thursday do the home jumps first, on fresh legs, then the gym leg session. Treat both as one training day.',
  'Work sets stop about two reps short of failure, and three reps short for shoulder care and while you learn a new exercise. No routine sets to failure.',
  'Lower each rep under control, then push with full intent to move the weight fast, still stopping at the planned reps in reserve.',
  'Warm up sets do not count as work sets. Do one or two lighter sets before the first exercise for a muscle.',
  'The weight goes up only when every work set reaches the top of its range with good form, the planned reps in reserve, and no pain. One good set is not enough.',
  'Stop a jump drill as soon as height, speed, or landing control drops. Jump volume never goes up automatically.',
  'Count every landing, including school and club volleyball and basketball. After a day with a lot of jumping, keep the home jumps short or skip them. In a week with many games, the home jump session is the first thing to cut.',
  'Jump only while knee, heel, shin, or Achilles pain stays at 2 out of 10 or less during the session and the next morning. Above that, skip the next jump session and tell a parent.',
  'Soreness in a trained muscle that fades within two or three days is common. Pain in a joint, a tendon, the heel, below the kneecap, or the wrist is different: it pauses that exercise. Pain of 4 out of 10 or more, pain that worsens, or pain that changes your technique means telling a parent and a coach or clinician.',
  'While a wrist injury is not cleared by a clinician, gripping and pressing exercises keep their load, and there is no ball contact or falling onto the hands.',
  'Sleep 8 to 10 hours. Training is never planned at the cost of sleep.',
  'Do not test a one repetition maximum.',
  'Rest two to three minutes on the big exercises and about ninety seconds on the small ones.',
  'Take a lighter week when performance, sleep, pain, mood, or motivation show accumulated fatigue, and tell a parent or coach.',
];

export interface PlanOptions {
  home?: HomeSetup;
  wrist?: WristStatus;
  jumpLevel?: JumpLevel;
}

const restDay = (weekday: Weekday, key: PlanDay['key'], title: string, short: string, restNotes: string[]): PlanDay => ({ weekday, key, title, short, isRest: true, items: [], restNotes });

/**
 * Builds the week (3.0.0): four gym strength days, two home jump days that come before the gym leg
 * sessions, one light home skill day, and two days without structured training. Home drills are
 * fitted to the space and the wrist, and gym exercises to the wrist.
 */
export function planDaysFor(picks: ProgramPicks | undefined, opts: PlanOptions = {}): PlanDay[] {
  const chosen = normalizePicks(picks);
  const home = opts.home ?? DEFAULT_HOME;
  const wrist = opts.wrist ?? 'unknown';
  const jumps = HOME_JUMP_SESSION[opts.jumpLevel ?? 'intro'];
  const gym = (wd: Weekday) => PROGRAM_DAYS.find((d) => d.weekday === wd)!;
  const main = (wd: Weekday) => buildMainItems(gym(wd), chosen, wrist);
  return [
    { weekday: 0, key: 'sun', title: 'Upper A', short: 'Upper A', isRest: false, items: main(0) },
    { weekday: 1, key: 'mon', title: 'Home jumps and Lower A', short: 'Lower A', isRest: false, items: [...buildHomeItems('mon', jumps, home, wrist), ...main(1)] },
    restDay(2, 'tue', 'No structured training', 'Off', [
      'No planned training. School sport still counts as training.',
      'Easy walking or play is fine if you feel like it.',
      'A good day to sleep a little longer and eat normally. Meals do not change on days off.',
    ]),
    { weekday: 3, key: 'wed', title: 'Upper B', short: 'Upper B', isRest: false, items: main(3) },
    { weekday: 4, key: 'thu', title: 'Home jumps and Lower B', short: 'Lower B', isRest: false, items: [...buildHomeItems('thu', jumps, home, wrist), ...main(4)] },
    { weekday: 5, key: 'fri', title: 'Volleyball skills at home', short: 'Skills', isRest: false, items: buildHomeItems('fri', HOME_SKILL_SESSION, home, wrist) },
    restDay(6, 'sat', 'Full Rest', 'Rest', ['No formal training.', 'Comfortable walking is fine if you feel like it.', 'Sabbath Mode keeps the app quiet.', 'No make up workout and no food rules to compensate.']),
  ];
}

export const BASELINE_PLAN: WorkoutPlan = {
  id: 'baseline',
  version: 1,
  name: 'PeakForm week',
  createdAt: '2026-10-06T00:00:00.000Z',
  globalRules: GLOBAL_RULES,
  days: planDaysFor(defaultPicks()),
};

export const SESSION_LABELS: Record<SessionKey, string> = {
  morning: 'Morning session',
  home: 'Home jumps and skills',
  main: 'Gym strength',
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
  const order: SessionKey[] = ['morning', 'home', 'main', 'swim'];
  return order.filter((s) => day.items.some((i) => i.session === s));
}

/** Optional taper for the week of a target event. Never includes dehydration or food restriction. */
export const TAPER_TEMPLATE = [
  { offsetDays: -3, label: 'Reduced strength volume', detail: 'Do the planned session with about half the working sets. Keep loads and reps in reserve the same.' },
  { offsetDays: -2, label: 'Light skills', detail: 'Short volleyball skills and easy movement only. No hard jumps or sprints.' },
  { offsetDays: -1, label: 'Rest', detail: 'Rest, eat normally, and sleep on time.' },
  { offsetDays: 0, label: 'Optional short easy pump', detail: 'A few light sets in the morning if you want. Eat and drink normally. No dehydration, no skipped meals.' },
] as const;
