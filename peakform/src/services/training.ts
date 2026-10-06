import { db } from '../db/db';
import { exposuresFor, saveSuggestion, updateSession } from '../db/repo';
import type { SetLog, WorkoutSession } from '../db/records';
import { exercise, prescriptionFor } from '../content/library';
import type { PlanDay, PlanItem, SessionKey, WorkoutPlan } from '../content/plan';
import { suggestNext, wristGate, type WorkSet } from '../domain/progression';
import { wristHoldsLoad } from '../content/traits';
import { getAthlete } from '../db/repo';
import { fourExposureReview, isReviewDue, type Exposure } from '../domain/fourExposure';
import { safetyState } from '../domain/safety';
import { dateKey, minutesOf, type DateKey } from '../domain/dates';
import { uid } from '../lib/id';
import type { AppSettings } from '../db/records';
import { isSabbathTime } from '../domain/sabbath';
import { DEFAULT_HOME_TIMES } from '../domain/defaults';

export function toWorkSet(s: SetLog): WorkSet {
  return {
    setIndex: s.setIndex,
    side: s.side,
    weightKg: s.weightKg,
    reps: s.reps,
    rir: s.rir,
    seconds: s.seconds,
    form: s.form,
    pain: s.pain,
    painScore: s.painScore,
    quality: s.quality,
    landing: s.landing,
  };
}

/**
 * Finish a session: store it, then compute a progression suggestion for each exercise
 * and a four exposure review when one is due. Nothing changes a target automatically.
 */
export async function finishSession(session: WorkoutSession, patch: Partial<WorkoutSession>): Promise<{ suggestions: number; reviews: number }> {
  await updateSession(session.id, { ...patch, status: 'done', finishedAt: Date.now() });
  const exSessions = await db.exerciseSessions.where('sessionId').equals(session.id).toArray();
  const sets = await db.setLogs.where('sessionId').equals(session.id).toArray();
  const today = dateKey();
  const safety = safetyState(today, await db.checkins.toArray(), await db.pain.toArray());
  const wrist = (await getAthlete()).wrist.status;
  let suggestions = 0;
  let reviews = 0;
  for (const es of exSessions) {
    if (es.skipped) continue;
    const item = session.planSnapshot.find((i) => i.id === es.planItemId);
    const ex = exercise(es.exerciseId);
    if (!item || !ex) continue;
    const work = sets.filter((s) => s.exerciseSessionId === es.id && !s.warmup);
    if (!work.length) continue;
    const p = prescriptionFor(item, ex);
    let sug = wristGate(suggestNext(p, work.map(toWorkSet), (await db.settings.get('app'))?.equipment), wristHoldsLoad(es.exerciseId, wrist));
    if (safety.stopProgression && (sug.kind === 'add_load' || sug.kind === 'add_reps')) {
      sug = { ...sug, kind: 'pain_hold', title: 'Progression paused by a safety flag', reason: `${safety.messages[0] ?? 'A safety flag is active.'} Keep the same target for now.`, targets: [] };
    }
    await saveSuggestion({ exerciseId: es.exerciseId, planItemId: item.id, basedOnSessionId: session.id, kind: sug.kind, title: sug.title, reason: sug.reason, targets: sug.targets });
    suggestions++;

    const all = await exposuresFor(es.exerciseId);
    if (isReviewDue(all.length)) {
      const sleepLogs = await db.sleep.toArray();
      const checkins = await db.checkins.toArray();
      const exps: Exposure[] = all.map((x) => {
        const sl = sleepLogs.find((s) => s.date === x.session.date);
        const ck = checkins.find((c) => c.date === x.session.date);
        const reach = x.sets.map((s) => s.reachCm).filter((v): v is number => v !== null);
        const times = x.sets.map((s) => s.timeSec).filter((v): v is number => v !== null);
        return {
          sessionId: x.session.id,
          date: x.session.date,
          sets: x.sets.map(toWorkSet),
          plannedSets: x.session.planSnapshot.find((i) => i.exerciseId === es.exerciseId)?.sets ?? x.sets.length,
          sleepHours: sl ? sl.durationMin / 60 : null,
          soreness: ck ? Math.max(0, ...Object.values(ck.soreness)) : null,
          reachCm: reach.length ? Math.max(...reach) : null,
          timeSec: times.length ? Math.min(...times) : null,
        };
      });
      const r = fourExposureReview(ex.kind, exps, all.length, item.rir ?? null);
      if (r.due) {
        const t = Date.now();
        await db.fourReviews.put({ id: uid('four'), createdAt: t, updatedAt: t, exerciseId: es.exerciseId, exposureNumber: r.exposureNumber, sessionIds: exps.slice(-4).map((e) => e.sessionId), recommendation: r.recommendation, summary: r.summary, details: [r.best && `Best: ${r.best}`, r.current && `Latest: ${r.current}`, ...r.details].filter(Boolean) as string[], status: 'pending' });
        reviews++;
      }
    }
  }
  return { suggestions, reviews };
}

export function sessionTime(settings: AppSettings, weekday: number, session: SessionKey): string {
  if (session === 'morning') return settings.sessionTimes.morning;
  if (session === 'home') return settings.sessionTimes.home?.[String(weekday)] ?? DEFAULT_HOME_TIMES[String(weekday)] ?? '16:15';
  if (session === 'swim') return settings.sessionTimes.swim[String(weekday)] ?? '19:30';
  return settings.sessionTimes.main[String(weekday)] ?? '16:30';
}

/** Scheduling notes: swim spacing and Sabbath conflicts. Advice only, never a block. */
export function scheduleNotes(settings: AppSettings, day: PlanDay, date: DateKey): string[] {
  const notes: string[] = [];
  const has = (s: SessionKey) => day.items.some((i) => i.session === s);
  if (has('swim') && has('main')) {
    const gap = Math.abs(minutesOf(sessionTime(settings, day.weekday, 'swim')) - minutesOf(sessionTime(settings, day.weekday, 'main')));
    if (gap < 180) notes.push(`The swim is set ${Math.floor(gap / 60)} h ${gap % 60} min from the main session. Three hours or more is better when your day allows.`);
  }
  if (has('home') && has('main') && day.items.some((i) => i.session === 'home' && exercise(i.exerciseId)?.kind === 'jump')) {
    const home = minutesOf(sessionTime(settings, day.weekday, 'home'));
    const gym = minutesOf(sessionTime(settings, day.weekday, 'main'));
    if (home > gym) notes.push('The home jumps are set after the gym session. Jumps go first, on fresh legs: move them earlier in More, Schedule, or keep them short today.');
  }
  for (const s of ['morning', 'home', 'main', 'swim'] as SessionKey[]) {
    if (!has(s)) continue;
    const t = sessionTime(settings, day.weekday, s);
    if (isSabbathTime(date, t, settings.sabbath)) notes.push(`${s === 'main' ? 'The gym session' : s === 'swim' ? 'The swim' : s === 'home' ? 'The home session' : 'The morning session'} at ${t} falls inside your Sabbath window. Move it earlier in More, Schedule.`);
  }
  return notes;
}

export function planDayFor(plan: WorkoutPlan | { days: PlanDay[] }, weekday: number): PlanDay | undefined {
  return plan.days.find((d) => d.weekday === weekday);
}

export function itemsFor(day: PlanDay, session: SessionKey): PlanItem[] {
  return day.items.filter((i) => i.session === session);
}
