import type { PainLog, SetLog, SleepLog, SportLog, WorkoutSession } from '../db/records';
import { addDays, type DateKey } from './dates';

// Total weekly load: the plan's sessions and school or club sport together (3.0.0). Minutes are what
// was logged, so the totals are only as complete as the logs. No single number decides safety; the
// totals are shown next to the guidance and the athlete's own recovery.

export interface WeekExposure {
  weekStart: DateKey;
  trainingMin: number;
  sportMin: number;
  totalMin: number;
  /** Home jump landings logged (reps of jump drills). */
  jumpContacts: number;
  /** Sport sessions logged with a lot of jumping. */
  lotsJumpingDays: number;
  hardSportSessions: number;
  /** Days with any planned session or sport logged. */
  activeDays: number;
}

const inWeek = (d: string, start: DateKey) => d >= start && d <= addDays(start, 6);

export function sessionMinutes(s: WorkoutSession): number {
  if (s.status !== 'done' || s.finishedAt === null) return 0;
  return Math.min(180, Math.max(0, (s.finishedAt - s.startedAt) / 60000));
}

export function weeklyExposure(weekStart: DateKey, sessions: WorkoutSession[], sport: SportLog[], setLogs: SetLog[] = [], isJump: (exerciseId: string) => boolean = () => false): WeekExposure {
  const done = sessions.filter((s) => s.status === 'done' && inWeek(s.date, weekStart));
  const sp = sport.filter((l) => inWeek(l.date, weekStart));
  const ids = new Set(done.map((s) => s.id));
  const trainingMin = done.reduce((a, s) => a + sessionMinutes(s), 0);
  const sportMin = sp.reduce((a, l) => a + l.minutes, 0);
  const jumpContacts = setLogs.filter((s) => ids.has(s.sessionId) && !s.warmup && isJump(s.exerciseId)).reduce((a, s) => a + (s.reps ?? 0), 0);
  return {
    weekStart,
    trainingMin,
    sportMin,
    totalMin: trainingMin + sportMin,
    jumpContacts,
    lotsJumpingDays: new Set(sp.filter((l) => l.jumping === 'lots').map((l) => l.date)).size,
    hardSportSessions: sp.filter((l) => l.intensity === 'hard').length,
    activeDays: new Set([...done.map((s) => s.date), ...sp.map((l) => l.date)]).size,
  };
}

/**
 * Hours of organised sport and training a week above the athlete's age in years went with more
 * serious overuse injuries in one large study of young athletes (Jayanthi 2015). A prompt to review
 * the week, not a limit or a diagnosis. Null when the age is unknown.
 */
export function hoursAboveAge(e: WeekExposure, ageYears: number | null): boolean | null {
  if (ageYears === null) return null;
  return e.totalMin / 60 > ageYears;
}

/** Whether sport the day before or the same day had a lot of jumping, so a home jump day can be kept short. */
export function heavyJumpingNear(date: DateKey, sport: SportLog[]): SportLog | null {
  return sport.find((l) => (l.date === date || l.date === addDays(date, -1)) && l.jumping === 'lots') ?? null;
}

// ---------- Jump day advice (3.1.0) ----------

/** Pain here after jumping points to the tendon and growth plate problems common in jumping teenagers. */
export const JUMP_PAIN_REGIONS = ['knee', 'heel', 'shin', 'achilles'] as const;
const REGION_NAME: Record<(typeof JUMP_PAIN_REGIONS)[number], string> = { knee: 'Knee', heel: 'Heel', shin: 'Shin', achilles: 'Achilles' };

/**
 * Jumping returns only while pain stays at 2 out of 10 or less during activity and the next morning.
 * That is the threshold of the one loading protocol built for adolescents (Rathleff 2020, Osgood-Schlatter).
 */
export const JUMP_PAIN_LIMIT = 2;
/** Teenagers need 8 to 10 hours; under 8 went with more injuries in young athletes (Milewski 2014). */
export const SHORT_SLEEP_MIN = 8 * 60;

export interface JumpDayAdvice {
  level: 'skip' | 'lighter';
  title: string;
  text: string;
}

/**
 * Advice for a day with home jumps, from this morning's check in (or yesterday's when today has none)
 * and last night's sleep. Pain above the limit skips the jumps; short sleep makes them lighter. It never
 * adds jumps, and it changes nothing in the plan by itself.
 */
export function jumpDayAdvice(date: DateKey, pain: PainLog[], sleep: SleepLog | null): JumpDayAdvice | null {
  const relevant = pain.filter((p) => p.source === 'checkin' && (JUMP_PAIN_REGIONS as readonly string[]).includes(p.region));
  const today = relevant.filter((p) => p.date === date);
  const recent = today.length ? today : relevant.filter((p) => p.date === addDays(date, -1));
  const over = recent.filter((p) => p.score > JUMP_PAIN_LIMIT).sort((a, b) => b.score - a.score);
  if (over.length) {
    const worst = over[0]!;
    const when = worst.date === date ? 'this morning' : 'in yesterday\'s check in';
    return {
      level: 'skip',
      title: 'Skip the jumps today',
      text: `${REGION_NAME[worst.region as (typeof JUMP_PAIN_REGIONS)[number]]} pain ${worst.score} out of 10 ${when}. Do the warm up and the footwork only, without jumps. Jump again once the pain stays at ${JUMP_PAIN_LIMIT} out of 10 or less during activity and the next morning. Tell a parent, and see a doctor if it has not settled within about two weeks.`,
    };
  }
  if (sleep && sleep.date === date && sleep.durationMin < SHORT_SLEEP_MIN) {
    const h = Math.floor(sleep.durationMin / 60);
    const m = sleep.durationMin % 60;
    return {
      level: 'lighter',
      title: 'A lighter jump session',
      text: `About ${h} h${m ? ` ${m} min` : ''} of sleep last night. Do one set of each jump drill instead of the planned sets, and stop as soon as a jump feels flat. Aim for 8 to 10 hours tonight.`,
    };
  }
  return null;
}
