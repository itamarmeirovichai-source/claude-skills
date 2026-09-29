import type { NutritionTarget } from '../content/meals';
import type { PlanDay } from '../content/plan';
import type { ActivityKind } from '../content/types';
import type {
  BodyCheckIn,
  ExerciseSession,
  FoodLog,
  FourExposureReviewRecord,
  PainLog,
  ProgressionSuggestionRecord,
  SetLog,
  SleepLog,
  WaistMeasurement,
  WaterLog,
  WorkoutSession,
} from '../db/records';
import { addDays, minutesOf, rangeKeys, weekdayOf, type DateKey } from './dates';
import { calorieStatus, dayTotals, morningWeights, proteinMet, sevenDayAverage, FAST_LOSS_KG_PER_WEEK } from './nutrition';
import { safetyState } from './safety';

// Deterministic weekly review. Every conclusion lists its evidence and a confidence.
// It reviews actions and evidence, never the person.

export type Confidence = 'high' | 'medium' | 'low';

export interface ReviewItem {
  id: string;
  text: string;
  evidence: string[];
  confidence: Confidence;
  /** Higher numbers are more important when picking priorities. */
  weight: number;
}

export interface WeekMetrics {
  weekStart: DateKey;
  weekEnd: DateKey;
  plannedSessions: number;
  completedSessions: number;
  plannedWorkSets: number;
  completedWorkSets: number;
  ropeDone: number;
  ropePlanned: number;
  swimDone: number;
  swimPlanned: number;
  volleyballExposures: number;
  jumpLandingPoor: number;
  foodDays: number;
  proteinDays: number;
  calorieDays: number;
  lowCalorieDays: number;
  plannedMeals: number;
  asPlannedMeals: number;
  loggedMeals: number;
  waterEntries: number;
  waterDays: number;
  sleepNights: number;
  sleepAvgH: number | null;
  bedtimeSpreadMin: number | null;
  morningWeights: number;
  weightAvg: number | null;
  weightReliable: boolean;
  waistLast: number | null;
  bodyFatAvg: number | null;
  bodyFatCount: number;
  energy: number | null;
  mood: number | null;
  soreness: number | null;
  concentration: number | null;
  calfSessions: number;
  calfPlanned: number;
}

export interface WeeklyReview {
  weekStart: DateKey;
  weekEnd: DateKey;
  generatedAt: number;
  keepDoing: ReviewItem[];
  readyToProgress: ReviewItem[];
  improve: ReviewItem[];
  safety: ReviewItem[];
  priorities: string[];
  current: WeekMetrics;
  previous: WeekMetrics;
  comparison: Array<{ label: string; previous: string; current: string; note: string }>;
  backupDaysAgo: number | null;
}

export interface ReviewData {
  planDays: PlanDay[];
  sessions: WorkoutSession[];
  exerciseSessions: ExerciseSession[];
  setLogs: SetLog[];
  foodLogs: FoodLog[];
  waterLogs: WaterLog[];
  checkins: BodyCheckIn[];
  waist: WaistMeasurement[];
  sleep: SleepLog[];
  pain: PainLog[];
  suggestions: ProgressionSuggestionRecord[];
  fourReviews: FourExposureReviewRecord[];
  targets: NutritionTarget[];
  lastBackupAt: number | null;
  exerciseKind: (id: string) => ActivityKind | undefined;
  exerciseName: (id: string) => string;
}

const avg = (xs: number[]) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : null);
const inWeek = (d: string, start: DateKey, end: DateKey) => d >= start && d <= end;
const CALF_IDS = new Set(['standing-calf-raise', 'seated-calf-raise']);
const VOLLEYBALL_KINDS: ActivityKind[] = ['jump', 'skill', 'throw', 'sprint'];

export function weekMetrics(data: ReviewData, weekStart: DateKey): WeekMetrics {
  const weekEnd = addDays(weekStart, 6);
  const days = rangeKeys(weekStart, 7);
  const sessions = data.sessions.filter((s) => s.status === 'done' && inWeek(s.date, weekStart, weekEnd));
  const sessionIds = new Set(sessions.map((s) => s.id));
  const uniqueSession = new Set(sessions.map((s) => `${s.date}:${s.session}`));

  let plannedSessions = 0;
  let plannedWorkSets = 0;
  let ropePlanned = 0;
  let swimPlanned = 0;
  let calfPlanned = 0;
  let plannedMeals = 0;
  for (const key of days) {
    const day = data.planDays.find((d) => d.weekday === weekdayOf(key));
    if (!day) continue;
    const sess = new Set(day.items.map((i) => i.session));
    plannedSessions += sess.size;
    if (sess.has('morning')) ropePlanned++;
    if (sess.has('swim')) swimPlanned++;
    plannedWorkSets += day.items.reduce((a, i) => a + i.sets, 0);
    if (day.items.some((i) => CALF_IDS.has(i.exerciseId))) calfPlanned++;
    if (!day.isRest) plannedMeals += 5;
  }

  const workSets = data.setLogs.filter((s) => sessionIds.has(s.sessionId) && !s.warmup);
  const completedWorkSets = new Set(workSets.map((s) => `${s.sessionId}:${s.planItemId}:${s.setIndex}`)).size;
  const exSessions = data.exerciseSessions.filter((e) => sessionIds.has(e.sessionId) && !e.skipped);
  const volleyballExposures = exSessions.filter((e) => VOLLEYBALL_KINDS.includes(data.exerciseKind(e.exerciseId) ?? 'strength')).length;
  const jumpLandingPoor = workSets.filter((s) => s.landing === 'poor').length;
  const calfSessions = new Set(exSessions.filter((e) => CALF_IDS.has(e.exerciseId) && workSets.some((s) => s.exerciseSessionId === e.id)).map((e) => e.sessionId)).size;

  const food = data.foodLogs.filter((f) => inWeek(f.date, weekStart, weekEnd));
  const foodByDay = new Map<string, FoodLog[]>();
  for (const f of food) foodByDay.set(f.date, [...(foodByDay.get(f.date) ?? []), f]);
  let proteinDays = 0;
  let calorieDays = 0;
  let lowCalorieDays = 0;
  for (const [date, logs] of foodByDay) {
    const t = dayTotals(logs);
    const target = data.targets.find((x) => x.weekday === weekdayOf(date));
    if (!target) continue;
    if (proteinMet(t, target)) proteinDays++;
    if (calorieStatus(t, target) === 'within') calorieDays++;
    // Only count a low day when most of the day was logged, to avoid flagging partial logs.
    if (logs.length >= 4 && t.high.kcal < 2000) lowCalorieDays++;
  }
  const water = data.waterLogs.filter((w) => inWeek(w.date, weekStart, weekEnd));
  const sleep = data.sleep.filter((s) => inWeek(s.date, weekStart, weekEnd));
  const bedRel = sleep.map((s) => (minutesOf(s.bedtime) + 1440 - 18 * 60) % 1440);
  const bedMean = avg(bedRel);
  const bedtimeSpreadMin = bedMean === null || bedRel.length < 3 ? null : Math.sqrt(avg(bedRel.map((b) => (b - bedMean) ** 2)) ?? 0);
  const checks = data.checkins.filter((c) => inWeek(c.date, weekStart, weekEnd));
  const weights = morningWeights(data.checkins);
  const wAvg = sevenDayAverage(weights, weekEnd);
  const waist = data.waist.filter((w) => inWeek(w.date, weekStart, weekEnd)).sort((a, b) => a.date.localeCompare(b.date));
  const bf = checks.filter((c) => c.bodyFatPct !== null && c.standardConditions).map((c) => c.bodyFatPct!);
  const sore = checks.map((c) => Math.max(0, ...Object.values(c.soreness)));

  return {
    weekStart,
    weekEnd,
    plannedSessions,
    completedSessions: uniqueSession.size,
    plannedWorkSets,
    completedWorkSets,
    ropeDone: sessions.filter((s) => s.session === 'morning').length,
    ropePlanned,
    swimDone: sessions.filter((s) => s.session === 'swim').length,
    swimPlanned,
    volleyballExposures,
    jumpLandingPoor,
    foodDays: foodByDay.size,
    proteinDays,
    calorieDays,
    lowCalorieDays,
    plannedMeals,
    asPlannedMeals: food.filter((f) => f.asPlanned).length,
    loggedMeals: food.length,
    waterEntries: water.length,
    waterDays: new Set(water.map((w) => w.date)).size,
    sleepNights: sleep.length,
    sleepAvgH: sleep.length ? (avg(sleep.map((s) => s.durationMin)) ?? 0) / 60 : null,
    bedtimeSpreadMin,
    morningWeights: wAvg.count,
    weightAvg: wAvg.avg,
    weightReliable: wAvg.reliable,
    waistLast: waist.length ? waist[waist.length - 1]!.cm : null,
    bodyFatAvg: bf.length >= 3 ? avg(bf) : null,
    bodyFatCount: bf.length,
    energy: avg(checks.map((c) => c.energy).filter((x): x is number => x !== null)),
    mood: avg(checks.map((c) => c.mood).filter((x): x is number => x !== null)),
    soreness: sore.length ? avg(sore) : null,
    concentration: avg(checks.map((c) => c.concentration).filter((x): x is number => x !== null)),
    calfSessions,
    calfPlanned,
  };
}

const f1 = (n: number | null, unit = '') => (n === null ? 'no data' : `${n.toFixed(1)}${unit}`);

export function generateWeeklyReview(data: ReviewData, weekStart: DateKey, now: number): WeeklyReview {
  const cur = weekMetrics(data, weekStart);
  const prev = weekMetrics(data, addDays(weekStart, -7));
  const keepDoing: ReviewItem[] = [];
  const ready: ReviewItem[] = [];
  const improve: ReviewItem[] = [];
  const safety: ReviewItem[] = [];

  // ---- Safety flags ----
  const s = safetyState(cur.weekEnd, data.checkins, data.pain, 7);
  s.messages.forEach((m, i) => safety.push({ id: `safety-${i}`, text: m, evidence: ['From your check ins and workout pain logs this week.'], confidence: 'high', weight: 100 }));
  if (cur.weightReliable && prev.weightReliable && cur.weightAvg !== null && prev.weightAvg !== null) {
    const loss = prev.weightAvg - cur.weightAvg;
    if (loss > FAST_LOSS_KG_PER_WEEK) {
      safety.push({
        id: 'fast-loss',
        text: `Weight is falling faster than about ${FAST_LOSS_KG_PER_WEEK} kg per week. Consider adding 150 to 200 calories a day and talk with a parent.`,
        evidence: [`Seven day average ${prev.weightAvg.toFixed(1)} kg last week and ${cur.weightAvg.toFixed(1)} kg this week.`],
        confidence: 'medium',
        weight: 90,
      });
    }
  }
  if (cur.lowCalorieDays >= 2) {
    safety.push({
      id: 'low-energy',
      text: 'On some fully logged days, food was well under 2,000 calories. Eating this little makes recovery and growth harder. Talk with a parent.',
      evidence: [`${cur.lowCalorieDays} fully logged days were under 2,000 calories even at the top of the estimate.`],
      confidence: 'medium',
      weight: 85,
    });
  }
  if (cur.sleepAvgH !== null && cur.sleepAvgH < 7 && cur.sleepNights >= 4) {
    safety.push({ id: 'sleep-low', text: 'Sleep averaged under seven hours. That is well below the eight to ten hours teens need.', evidence: [`${cur.sleepNights} nights logged, average ${cur.sleepAvgH.toFixed(1)} hours.`], confidence: 'high', weight: 70 });
  }

  // ---- Keep doing ----
  if (cur.ropePlanned > 0 && cur.ropeDone >= cur.ropePlanned) {
    keepDoing.push({ id: 'rope', text: `You completed all ${cur.ropePlanned} morning rope sessions.`, evidence: [`${cur.ropeDone} of ${cur.ropePlanned} logged.`], confidence: 'high', weight: 10 });
  }
  if (cur.calfPlanned > 0 && cur.calfSessions >= cur.calfPlanned) {
    keepDoing.push({ id: 'calves', text: 'You completed both calf sessions.', evidence: [`Calf raises logged in ${cur.calfSessions} of ${cur.calfPlanned} planned sessions.`], confidence: 'high', weight: 8 });
  }
  if (cur.volleyballExposures > 0 && cur.jumpLandingPoor === 0) {
    keepDoing.push({ id: 'jumps', text: 'Jump and volleyball work had no landings rated poor.', evidence: [`${cur.volleyballExposures} jump, sprint, throw, or skill exercises logged.`], confidence: 'medium', weight: 9 });
  }
  if (cur.plannedSessions > 0 && cur.completedSessions >= cur.plannedSessions) {
    keepDoing.push({ id: 'sessions', text: 'You completed every planned session this week.', evidence: [`${cur.completedSessions} of ${cur.plannedSessions} sessions.`], confidence: 'high', weight: 12 });
  }
  if (cur.sleepAvgH !== null && cur.sleepAvgH >= 8 && cur.sleepNights >= 5) {
    keepDoing.push({ id: 'sleep', text: `Sleep averaged ${cur.sleepAvgH.toFixed(1)} hours, inside the eight to ten hour target.`, evidence: [`${cur.sleepNights} nights logged.`], confidence: 'high', weight: 9 });
  }
  if (cur.foodDays >= 5 && cur.proteinDays >= Math.min(5, cur.foodDays)) {
    keepDoing.push({ id: 'protein', text: `Protein reached the target on ${cur.proteinDays} days.`, evidence: [`${cur.foodDays} days with food logged.`], confidence: 'medium', weight: 6 });
  }
  if (cur.morningWeights >= 4) {
    keepDoing.push({ id: 'weights', text: `You logged ${cur.morningWeights} morning weights, enough for a reliable weekly average.`, evidence: [`Seven day average ${f1(cur.weightAvg, ' kg')}.`], confidence: 'high', weight: 5 });
  }

  // ---- Ready to progress ----
  const weekSessionIds = new Set(data.sessions.filter((x) => inWeek(x.date, cur.weekStart, cur.weekEnd)).map((x) => x.id));
  const pending = data.suggestions.filter((x) => weekSessionIds.has(x.basedOnSessionId) && x.status === 'pending');
  const latestByEx = new Map<string, ProgressionSuggestionRecord>();
  for (const p of pending.sort((a, b) => a.createdAt - b.createdAt)) latestByEx.set(p.exerciseId, p);
  for (const p of latestByEx.values()) {
    if (s.stopProgression) break;
    if (p.kind === 'add_load' || p.kind === 'add_reps') {
      ready.push({
        id: `prog-${p.exerciseId}`,
        text: `${data.exerciseName(p.exerciseId)}: ${p.title}.`,
        evidence: [p.reason],
        confidence: p.kind === 'add_load' ? 'high' : 'medium',
        weight: p.kind === 'add_load' ? 20 : 8,
      });
    }
  }
  for (const r of data.fourReviews.filter((x) => inWeek(new Date(x.createdAt).toISOString().slice(0, 10), cur.weekStart, addDays(cur.weekEnd, 1)))) {
    const item: ReviewItem = { id: `four-${r.exerciseId}`, text: `${data.exerciseName(r.exerciseId)} four session review: ${r.summary}`, evidence: r.details, confidence: 'low', weight: 15 };
    if (r.recommendation === 'progress' && !s.stopProgression) ready.push(item);
    else if (r.recommendation === 'coach_review') safety.push({ ...item, weight: 60 });
    else improve.push(item);
  }
  if (s.stopProgression && pending.some((p) => p.kind === 'add_load' || p.kind === 'add_reps')) {
    improve.push({ id: 'prog-paused', text: 'Progression suggestions are paused until the safety flags are resolved.', evidence: ['A pain or safety flag is active this week.'], confidence: 'high', weight: 50 });
  }

  // ---- Improve next week ----
  if (cur.morningWeights < 4) {
    improve.push({
      id: 'weights-few',
      text: `Only ${cur.morningWeights} morning weight${cur.morningWeights === 1 ? ' was' : 's were'} logged, so the trend is too uncertain for a nutrition change.`,
      evidence: ['A weekly trend needs at least four morning weights taken after the toilet and before food or drink.'],
      confidence: 'high',
      weight: 30,
    });
  }
  if (cur.waistLast === null) {
    improve.push({ id: 'waist', text: 'No waist measurement this week. One measurement a week, same time and conditions, makes the trend much clearer.', evidence: ['No waist entry between Monday and Sunday.'], confidence: 'high', weight: 18 });
  }
  if (cur.sleepAvgH !== null && cur.sleepAvgH >= 7 && cur.sleepAvgH < 8) {
    improve.push({ id: 'sleep-short', text: `Sleep averaged ${cur.sleepAvgH.toFixed(1)} hours. Moving bedtime about 20 minutes earlier would bring it closer to eight.`, evidence: [`${cur.sleepNights} nights logged.`], confidence: cur.sleepNights >= 5 ? 'high' : 'medium', weight: 25 });
  }
  if (cur.bedtimeSpreadMin !== null && cur.bedtimeSpreadMin > 45) {
    improve.push({ id: 'bedtime', text: 'Bedtimes varied a lot. A steadier bedtime near 22:30 helps recovery.', evidence: [`Bedtimes spread by about ${Math.round(cur.bedtimeSpreadMin)} minutes around their average.`], confidence: 'medium', weight: 12 });
  }
  if (cur.sleepNights < 4) {
    improve.push({ id: 'sleep-log', text: 'Sleep was logged on fewer than four nights, so sleep conclusions are uncertain.', evidence: [`${cur.sleepNights} nights logged.`], confidence: 'high', weight: 10 });
  }
  if (cur.plannedSessions > 0 && cur.completedSessions < cur.plannedSessions) {
    const missed = cur.plannedSessions - cur.completedSessions;
    improve.push({
      id: 'sessions-missed',
      text: `${missed} planned session${missed === 1 ? ' was' : 's were'} not logged. If the week got busy, a missed session can move to another day without doubling up.`,
      evidence: [`${cur.completedSessions} of ${cur.plannedSessions} sessions logged.`],
      confidence: 'high',
      weight: 16,
    });
  }
  if (cur.foodDays < 5) {
    improve.push({ id: 'food-log', text: `Food was logged on ${cur.foodDays} days. The one tap default meals make logging quicker.`, evidence: ['The fourteen day nutrition check needs at least ten logged days.'], confidence: 'high', weight: 20 });
  } else if (cur.calorieDays < Math.ceil(cur.foodDays / 2)) {
    improve.push({ id: 'kcal-range', text: `Calories were inside the daily range on ${cur.calorieDays} of ${cur.foodDays} logged days.`, evidence: ['The range is the daily target plus or minus about 100 calories.', 'Estimated meals carry wide ranges, so this is approximate.'], confidence: 'low', weight: 9 });
  }
  if (cur.waterDays < 5) {
    improve.push({ id: 'water', text: 'Water was logged on fewer than five days.', evidence: [`${cur.waterEntries} water entries this week.`], confidence: 'medium', weight: 4 });
  }
  if (cur.swimPlanned > 0 && cur.swimDone < cur.swimPlanned) {
    improve.push({ id: 'swim', text: `${cur.swimDone} of ${cur.swimPlanned} easy swims were logged.`, evidence: ['Swims are easy aerobic work, spaced at least three hours from the main session when possible.'], confidence: 'high', weight: 6 });
  }
  const backupDaysAgo = data.lastBackupAt === null ? null : Math.floor((now - data.lastBackupAt) / 86400000);
  if (backupDaysAgo === null || backupDaysAgo > 14) {
    improve.push({ id: 'backup', text: backupDaysAgo === null ? 'No backup has been made yet. Export one to Files so your history is safe.' : `The last backup was ${backupDaysAgo} days ago. A fresh export keeps your history safe.`, evidence: ['iOS can remove website data in rare cases.'], confidence: 'high', weight: 14 });
  } else {
    keepDoing.push({ id: 'backup-ok', text: `Your last backup was ${backupDaysAgo === 0 ? 'today' : `${backupDaysAgo} day${backupDaysAgo === 1 ? '' : 's'} ago`}.`, evidence: ['Backups are stored where you saved them, not in PeakForm.'], confidence: 'high', weight: 2 });
  }

  // ---- Comparison ----
  const cmp = (label: string, p: string, c: string, note = '') => ({ label, previous: p, current: c, note });
  const comparison = [
    cmp('Sessions', `${prev.completedSessions} of ${prev.plannedSessions}`, `${cur.completedSessions} of ${cur.plannedSessions}`),
    cmp('Work sets', `${prev.completedWorkSets} of ${prev.plannedWorkSets}`, `${cur.completedWorkSets} of ${cur.plannedWorkSets}`),
    cmp('Morning rope', `${prev.ropeDone} of ${prev.ropePlanned}`, `${cur.ropeDone} of ${cur.ropePlanned}`),
    cmp('Swims', `${prev.swimDone} of ${prev.swimPlanned}`, `${cur.swimDone} of ${cur.swimPlanned}`),
    cmp('Volleyball and jump exercises', String(prev.volleyballExposures), String(cur.volleyballExposures)),
    cmp('Days with food logged', String(prev.foodDays), String(cur.foodDays)),
    cmp('Protein target days', String(prev.proteinDays), String(cur.proteinDays)),
    cmp('Calorie range days', String(prev.calorieDays), String(cur.calorieDays), 'Estimated'),
    cmp('Meals logged as planned', String(prev.asPlannedMeals), String(cur.asPlannedMeals)),
    cmp('Water entries', String(prev.waterEntries), String(cur.waterEntries)),
    cmp('Average sleep', f1(prev.sleepAvgH, ' h'), f1(cur.sleepAvgH, ' h')),
    cmp('Morning weights', String(prev.morningWeights), String(cur.morningWeights), 'Four or more needed'),
    cmp('Seven day weight average', prev.weightReliable ? f1(prev.weightAvg, ' kg') : 'too few', cur.weightReliable ? f1(cur.weightAvg, ' kg') : 'too few'),
    cmp('Waist', f1(prev.waistLast, ' cm'), f1(cur.waistLast, ' cm')),
    cmp('Scale body fat', prev.bodyFatAvg === null ? 'too few' : f1(prev.bodyFatAvg, '%'), cur.bodyFatAvg === null ? 'too few' : f1(cur.bodyFatAvg, '%'), 'Trend only, low confidence'),
    cmp('Energy', f1(prev.energy), f1(cur.energy), 'Out of 5'),
    cmp('Mood', f1(prev.mood), f1(cur.mood), 'Out of 5'),
    cmp('Soreness', f1(prev.soreness), f1(cur.soreness), 'Out of 3'),
    cmp('School concentration', f1(prev.concentration), f1(cur.concentration), 'Out of 5'),
  ];

  const byWeight = (a: ReviewItem, b: ReviewItem) => b.weight - a.weight;
  const priorities = [...safety.sort(byWeight), ...improve.sort(byWeight)].slice(0, 3).map((i) => i.text);
  if (priorities.length === 0 && ready.length) priorities.push(ready.sort(byWeight)[0]!.text);
  if (priorities.length === 0) priorities.push('Keep the same routine next week.');

  return {
    weekStart: cur.weekStart,
    weekEnd: cur.weekEnd,
    generatedAt: now,
    keepDoing: keepDoing.sort(byWeight),
    readyToProgress: ready.sort(byWeight),
    improve: improve.sort(byWeight),
    safety: safety.sort(byWeight),
    priorities,
    current: cur,
    previous: prev,
    comparison,
    backupDaysAgo,
  };
}
