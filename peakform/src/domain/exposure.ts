import type { SetLog, SportLog, WorkoutSession } from '../db/records';
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
