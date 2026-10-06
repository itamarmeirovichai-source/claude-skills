import { db } from './db';
import {
  TABLE_NAMES,
  type AppSettings,
  type BodyCheckIn,
  type ExerciseSession,
  type FoodLog,
  type PainLog,
  type PlanRecord,
  type ProgressionSuggestionRecord,
  type SetLog,
  type SleepLog,
  type TableName,
  type UserProfile,
  type WaistMeasurement,
  type WaterLog,
  type WorkoutSession,
} from './records';
import { baselinePlanRecord, defaultProfile, defaultSettings } from '../domain/defaults';
import type { PlanItem, SessionKey } from '../content/plan';
import { dateKey, weekdayOf, type DateKey } from '../domain/dates';
import { uid } from '../lib/id';
import type { TableData } from '../domain/backup';
import { parseAthlete, type AthleteProfile } from '../domain/athlete';
import type { SportLog } from './records';
import type { RestTimerState } from '../domain/timer';

// Data access. Plan records are versioned and never rewritten; logs reference a
// snapshot of the prescription they were performed against.

export const now = () => Date.now();

export async function ensureInitialized(): Promise<AppSettings> {
  const existing = await db.settings.get('app');
  if (existing) {
    if (!(await db.plans.get(existing.activePlanId))) await db.plans.put(baselinePlanRecord(now()));
    return existing;
  }
  const t = now();
  const s = defaultSettings(t);
  await db.transaction('rw', db.settings, db.profile, db.plans, db.migrations, db.kv, async () => {
    await db.settings.put(s);
    await db.profile.put(defaultProfile(t));
    await db.plans.put(baselinePlanRecord(t));
    // A new install starts on the current plan, so there is no update to offer.
    await db.kv.put({ id: KV.planUpdates, value: { 'home-gym-v3': 'applied' }, updatedAt: t });
    await db.migrations.put({ id: 'init-1', createdAt: t, updatedAt: t, fromVersion: 0, toVersion: 1, appliedAt: t, note: 'Created database.' });
  });
  return s;
}

export async function getSettings(): Promise<AppSettings> {
  return (await db.settings.get('app')) ?? ensureInitialized();
}

export async function updateSettings(patch: Partial<AppSettings> | ((s: AppSettings) => AppSettings)): Promise<AppSettings> {
  const cur = await getSettings();
  const next = typeof patch === 'function' ? patch(structuredClone(cur)) : { ...cur, ...patch };
  next.updatedAt = now();
  await db.settings.put(next);
  return next;
}

export async function getProfile(): Promise<UserProfile> {
  return (await db.profile.get('me')) ?? defaultProfile(now());
}

export async function saveProfile(p: UserProfile): Promise<void> {
  await db.profile.put({ ...p, updatedAt: now() });
}

// ---------- Plans ----------

export async function activePlan(): Promise<PlanRecord> {
  const s = await getSettings();
  const p = await db.plans.get(s.activePlanId);
  if (p) return p;
  const b = baselinePlanRecord(now());
  await db.plans.put(b);
  return b;
}

/** Save an edited plan as a new version. History keeps pointing at the old snapshot. */
export async function savePlanVersion(edited: PlanRecord, changeNote: string): Promise<PlanRecord> {
  const all = await db.plans.where('planKey').equals(edited.planKey).toArray();
  const version = Math.max(0, ...all.map((p) => p.version)) + 1;
  const t = now();
  const rec: PlanRecord = { ...structuredClone(edited), id: `${edited.planKey}-v${version}`, version, createdAt: t, updatedAt: t, changeNote };
  await db.plans.put(rec);
  await updateSettings({ activePlanId: rec.id });
  return rec;
}

// ---------- Sessions ----------

export async function sessionsOn(date: DateKey): Promise<WorkoutSession[]> {
  return db.sessions.where('date').equals(date).toArray();
}

export async function activeSession(): Promise<WorkoutSession | undefined> {
  return db.sessions.where('status').equals('active').first();
}

export async function startSession(date: DateKey, session: SessionKey, items: PlanItem[], title: string, plan: PlanRecord, rescheduledFrom: DateKey | null = null, planWeekday?: number): Promise<WorkoutSession> {
  const t = now();
  const s = await getSettings();
  const ws: WorkoutSession = {
    id: uid('ses'),
    createdAt: t,
    updatedAt: t,
    date,
    weekday: weekdayOf(date),
    planWeekday: planWeekday ?? weekdayOf(date),
    planId: plan.id,
    planVersion: plan.version,
    session,
    title,
    status: 'active',
    startedAt: t,
    finishedAt: null,
    planSnapshot: structuredClone(items),
    sessionRpe: null,
    recovery: null,
    poolLengthM: session === 'swim' ? s.poolLengthM : null,
    note: '',
    rescheduledFrom,
  };
  const exs: ExerciseSession[] = items.map((it, order) => ({
    id: uid('exs'),
    createdAt: t,
    updatedAt: t,
    sessionId: ws.id,
    planItemId: it.id,
    order,
    exerciseId: it.exerciseId,
    originalExerciseId: null,
    substitutionReason: null,
    skipped: false,
    skipReason: null,
    note: '',
  }));
  await db.transaction('rw', db.sessions, db.exerciseSessions, async () => {
    await db.sessions.put(ws);
    await db.exerciseSessions.bulkPut(exs);
  });
  return ws;
}

export async function updateSession(id: string, patch: Partial<WorkoutSession>): Promise<void> {
  await db.sessions.update(id, { ...patch, updatedAt: now() });
}

export async function updateExerciseSession(id: string, patch: Partial<ExerciseSession>): Promise<void> {
  await db.exerciseSessions.update(id, { ...patch, updatedAt: now() });
}

export async function addExerciseToSession(sessionId: string, exerciseId: string, item: PlanItem): Promise<ExerciseSession> {
  const existing = await db.exerciseSessions.where('sessionId').equals(sessionId).toArray();
  const t = now();
  const ex: ExerciseSession = { id: uid('exs'), createdAt: t, updatedAt: t, sessionId, planItemId: item.id, order: existing.length, exerciseId, originalExerciseId: null, substitutionReason: null, skipped: false, skipReason: null, note: '' };
  await db.exerciseSessions.put(ex);
  const ses = await db.sessions.get(sessionId);
  if (ses) await updateSession(sessionId, { planSnapshot: [...ses.planSnapshot, item] });
  return ex;
}

// ---------- Sets ----------

export async function logSet(set: Omit<SetLog, 'id' | 'createdAt' | 'updatedAt'>): Promise<SetLog> {
  const t = now();
  const rec: SetLog = { ...set, id: uid('set'), createdAt: t, updatedAt: t };
  await db.setLogs.put(rec);
  if (!rec.warmup && rec.painScore !== null && rec.painScore > 0) {
    await db.pain.put({ id: uid('pain'), createdAt: t, updatedAt: t, date: dateKey(new Date(rec.completedAt)), at: rec.completedAt, region: 'exercise', score: rec.painScore, source: 'workout', exerciseId: rec.exerciseId, note: rec.note.slice(0, 300) });
  }
  return rec;
}

export async function updateSet(id: string, patch: Partial<SetLog>): Promise<void> {
  await db.setLogs.update(id, { ...patch, updatedAt: now() });
}

export async function deleteSet(id: string): Promise<SetLog | undefined> {
  const s = await db.setLogs.get(id);
  await db.setLogs.delete(id);
  return s;
}

export async function restoreSet(s: SetLog): Promise<void> {
  await db.setLogs.put(s);
}

/** Work sets from the most recent completed exposure of an exercise before a session. */
export async function lastExposure(exerciseId: string, beforeSessionId?: string): Promise<{ session: WorkoutSession; sets: SetLog[] } | null> {
  const sets = await db.setLogs.where('exerciseId').equals(exerciseId).toArray();
  const bySession = new Map<string, SetLog[]>();
  for (const s of sets) if (!s.warmup && s.sessionId !== beforeSessionId) bySession.set(s.sessionId, [...(bySession.get(s.sessionId) ?? []), s]);
  if (!bySession.size) return null;
  const sessions = (await db.sessions.bulkGet([...bySession.keys()])).filter((x): x is WorkoutSession => !!x && x.status === 'done');
  sessions.sort((a, b) => b.startedAt - a.startedAt);
  const latest = sessions[0];
  if (!latest) return null;
  return { session: latest, sets: (bySession.get(latest.id) ?? []).sort((a, b) => a.setIndex - b.setIndex || (a.side ?? '').localeCompare(b.side ?? '')) };
}

/** Finished sessions with work sets of this exercise, not counting the current session. */
export async function priorExposureCount(exerciseId: string, excludeSessionId: string): Promise<number> {
  const sets = await db.setLogs.where('exerciseId').equals(exerciseId).toArray();
  const ids = [...new Set(sets.filter((s) => !s.warmup && s.sessionId !== excludeSessionId).map((s) => s.sessionId))];
  const sessions = await db.sessions.bulkGet(ids);
  return sessions.filter((x) => x?.status === 'done').length;
}

export async function exposuresFor(exerciseId: string): Promise<Array<{ session: WorkoutSession; sets: SetLog[] }>> {
  const sets = await db.setLogs.where('exerciseId').equals(exerciseId).toArray();
  const bySession = new Map<string, SetLog[]>();
  for (const s of sets) if (!s.warmup) bySession.set(s.sessionId, [...(bySession.get(s.sessionId) ?? []), s]);
  const sessions = (await db.sessions.bulkGet([...bySession.keys()])).filter((x): x is WorkoutSession => !!x && x.status === 'done');
  return sessions.sort((a, b) => a.startedAt - b.startedAt).map((session) => ({ session, sets: bySession.get(session.id) ?? [] }));
}

// ---------- Suggestions ----------

export async function saveSuggestion(s: Omit<ProgressionSuggestionRecord, 'id' | 'createdAt' | 'updatedAt' | 'status' | 'decidedAt'>): Promise<ProgressionSuggestionRecord> {
  const t = now();
  // Older pending suggestions for the same plan item are replaced by the newest.
  const old = await db.suggestions.where('planItemId').equals(s.planItemId).filter((x) => x.status === 'pending').toArray();
  await db.suggestions.bulkUpdate(old.map((o) => ({ key: o.id, changes: { status: 'dismissed' as const, decidedAt: t, updatedAt: t } })));
  const rec: ProgressionSuggestionRecord = { ...s, id: uid('sug'), createdAt: t, updatedAt: t, status: 'pending', decidedAt: null };
  await db.suggestions.put(rec);
  return rec;
}

export async function decideSuggestion(id: string, status: 'accepted' | 'dismissed'): Promise<void> {
  await db.suggestions.update(id, { status, decidedAt: now(), updatedAt: now() });
}

/** The latest target for a plan item: an accepted suggestion, or a pending one waiting for confirmation. */
export async function currentTarget(planItemId: string, exerciseId: string): Promise<ProgressionSuggestionRecord | null> {
  let list = await db.suggestions.where('planItemId').equals(planItemId).toArray();
  if (!list.length) list = await db.suggestions.where('exerciseId').equals(exerciseId).toArray();
  const live = list.filter((x) => x.status !== 'dismissed').sort((a, b) => b.createdAt - a.createdAt);
  return live[0] ?? null;
}

// ---------- Food and water ----------

export async function addFoodLog(log: Omit<FoodLog, 'id' | 'createdAt' | 'updatedAt'>): Promise<FoodLog> {
  const t = now();
  const rec: FoodLog = { ...log, id: uid('food'), createdAt: t, updatedAt: t };
  await db.foodLogs.put(rec);
  return rec;
}

export async function deleteFoodLog(id: string): Promise<FoodLog | undefined> {
  const f = await db.foodLogs.get(id);
  await db.foodLogs.delete(id);
  if (f?.photoId) await db.photos.delete(f.photoId);
  return f;
}

export async function addWater(date: DateKey, ml: number, drink: WaterLog['drink']): Promise<WaterLog> {
  const t = now();
  const rec: WaterLog = { id: uid('water'), createdAt: t, updatedAt: t, date, at: t, ml, drink };
  await db.waterLogs.put(rec);
  return rec;
}

// ---------- Check in ----------

export interface CheckInInput {
  checkin: Omit<BodyCheckIn, 'id' | 'createdAt' | 'updatedAt'>;
  sleep: Omit<SleepLog, 'id' | 'createdAt' | 'updatedAt'> | null;
  waist: Omit<WaistMeasurement, 'id' | 'createdAt' | 'updatedAt'> | null;
  pain: Array<Omit<PainLog, 'id' | 'createdAt' | 'updatedAt'>>;
}

export async function saveCheckIn(input: CheckInInput): Promise<BodyCheckIn> {
  const t = now();
  const rec: BodyCheckIn = { ...input.checkin, id: uid('chk'), createdAt: t, updatedAt: t };
  await db.transaction('rw', db.checkins, db.sleep, db.waist, db.pain, async () => {
    await db.checkins.put(rec);
    if (input.sleep) {
      const prior = await db.sleep.where('date').equals(input.sleep.date).toArray();
      await db.sleep.bulkDelete(prior.map((p) => p.id));
      await db.sleep.put({ ...input.sleep, id: uid('slp'), createdAt: t, updatedAt: t });
    }
    if (input.waist) await db.waist.put({ ...input.waist, id: uid('wst'), createdAt: t, updatedAt: t });
    for (const p of input.pain) await db.pain.put({ ...p, id: uid('pain'), createdAt: t, updatedAt: t });
  });
  return rec;
}

// ---------- Key value ----------

export async function kvGet<T>(key: string): Promise<T | undefined> {
  const r = await db.kv.get(key);
  return r?.value as T | undefined;
}

export async function kvSet(key: string, value: unknown): Promise<void> {
  await db.kv.put({ id: key, value, updatedAt: now() });
}

export async function kvDelete(key: string): Promise<void> {
  await db.kv.delete(key);
}

export const KV = {
  timer: 'activeTimer',
  lastBackupAt: 'lastBackupAt',
  mealPrep: 'mealPrep',
  shopping: 'shopping',
  persistAsked: 'persistAsked',
  lastReviewWeek: 'lastReviewWeek',
  optionalFoods: 'optionalFoods',
  unlockedAt: 'unlockedAt',
  targets: 'nutritionTargets',
  supplementReview: 'supplementReview',
  planUpdates: 'planUpdates',
  programPicks: 'programPicks',
  programDraft: 'programDraft',
  /** The training block the active plan was built for. */
  programPhase: 'programPhase',
  /** A block that started and has not been acknowledged on Today yet. */
  phaseNotice: 'phaseNotice',
  /** Standing reach from 2.1.0, read by the jump measurements. */
  dunkProfile: 'dunkProfile',
  athleteBasics: 'athleteBasics',
  wrist: 'wristInfo',
  homeSetup: 'homeSetup',
  sportLoad: 'sportLoad',
  weightPrefs: 'weightPrefs',
  kosherPrefs: 'kosherPrefs',
  supplementDetails: 'supplementDetails',
  usualVeg: 'usualVeg',
  aspirations: 'aspirations',
  reviewedTargets: 'reviewedTargets',
  jumpLevel: 'jumpLevel',
  /** A plan waiting for the athlete to look at the differences and activate it. */
  planProposal: 'planProposal',
  jumpTests: 'jumpTests',
  /** The review with a parent: when it was marked done, and what was discussed. */
  parentReview: 'parentReview',
} as const;

// ---------- Athlete profile (3.0.0) ----------

export const ATHLETE_KV: Record<keyof AthleteProfile, string> = {
  basics: KV.athleteBasics,
  wrist: KV.wrist,
  home: KV.homeSetup,
  sport: KV.sportLoad,
  weight: KV.weightPrefs,
  kosher: KV.kosherPrefs,
  supplements: KV.supplementDetails,
  veg: KV.usualVeg,
  aspirations: KV.aspirations,
  reviewed: KV.reviewedTargets,
};

/** The athlete profile, with cautious defaults for anything not answered yet. All reads start together. */
export async function getAthlete(): Promise<AthleteProfile> {
  const keys = Object.keys(ATHLETE_KV) as Array<keyof AthleteProfile>;
  const values = await Promise.all(keys.map((k) => kvGet<unknown>(ATHLETE_KV[k])));
  return parseAthlete(Object.fromEntries(keys.map((k, i) => [k, values[i]])));
}

export async function saveAthlete<K extends keyof AthleteProfile>(key: K, value: AthleteProfile[K]): Promise<void> {
  await kvSet(ATHLETE_KV[key], value);
}

// ---------- School and club sport ----------

export async function addSportLog(log: Omit<SportLog, 'id' | 'createdAt' | 'updatedAt'>): Promise<SportLog> {
  const t = now();
  const rec: SportLog = { ...log, id: uid('sport'), createdAt: t, updatedAt: t };
  await db.sportLogs.put(rec);
  return rec;
}

export async function deleteSportLog(id: string): Promise<void> {
  await db.sportLogs.delete(id);
}

export async function saveTimer(t: RestTimerState | null): Promise<void> {
  if (t) await kvSet(KV.timer, t);
  else await kvDelete(KV.timer);
}

// ---------- Export, import, delete ----------

export async function readAllTables(): Promise<TableData> {
  const out: TableData = {};
  for (const name of TABLE_NAMES) {
    out[name] = (await db.table(name).toArray()) as Array<Record<string, unknown>>;
  }
  return out;
}

export async function writeAllTables(data: TableData, mode: 'replace' | 'merge'): Promise<void> {
  await db.transaction('rw', TABLE_NAMES.map((n) => db.table(n)), async () => {
    for (const name of TABLE_NAMES) {
      const rows = data[name as TableName];
      if (mode === 'replace') await db.table(name).clear();
      if (rows && rows.length) await db.table(name).bulkPut(rows);
    }
  });
}

export async function snapshotBeforeImport(reason: string): Promise<string> {
  const payload = JSON.stringify(await readAllTables());
  const t = now();
  const id = uid('snap');
  await db.snapshots.put({ id, createdAt: t, updatedAt: t, reason, payload });
  // Keep the three most recent snapshots.
  const all = await db.snapshots.orderBy('createdAt').reverse().toArray();
  await db.snapshots.bulkDelete(all.slice(3).map((s) => s.id));
  return id;
}

export async function restoreSnapshot(id: string): Promise<void> {
  const s = await db.snapshots.get(id);
  if (!s) throw new Error('Snapshot not found.');
  await writeAllTables(JSON.parse(s.payload) as TableData, 'replace');
}

export async function deleteAllData(): Promise<void> {
  await db.delete();
  await db.open();
}

export async function removeDemoData(): Promise<void> {
  const tables = ['sessions', 'exerciseSessions', 'setLogs', 'foodLogs', 'waterLogs', 'checkins', 'waist', 'sleep', 'pain', 'suggestions', 'fourReviews', 'weeklyReviews', 'sportLogs'] as const;
  await db.transaction('rw', tables.map((t) => db.table(t)), async () => {
    for (const t of tables) {
      const keys = (await db.table(t).toCollection().primaryKeys()) as string[];
      await db.table(t).bulkDelete(keys.filter((k) => String(k).startsWith('demo-')));
    }
  });
  await updateSettings({ demoData: false });
}
