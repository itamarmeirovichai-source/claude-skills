import type { PlanDay } from '../content/plan';
import type { AthleteProfile } from './athlete';
import { weeklyExposure, hoursAboveAge } from './exposure';
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
  SportLog,
  WaistMeasurement,
  WaterLog,
  WorkoutSession,
} from '../db/records';
import { addDays, minutesOf, rangeKeys, weekdayOf, type DateKey } from './dates';
import { dayTotals, morningWeights, sevenDayAverage, FAST_LOSS_KG_PER_WEEK, STABLE_WEIGHT_NOTE } from './nutrition';
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
  /** Home sessions done and planned. Plans before 3.0.0 called them morning sessions. */
  homeDone: number;
  homePlanned: number;
  swimDone: number;
  swimPlanned: number;
  volleyballExposures: number;
  jumpLandingPoor: number;
  foodDays: number;
  /** Logged meals with 20 g of protein or more. */
  proteinMeals: number;
  /** Days inside a professionally reviewed energy range, or null without one. */
  reviewedRangeDays: number | null;
  /** Fully logged days well below the example meals: a recovery signal, never a target. */
  lowIntakeDays: number;
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
  sportMin: number;
  trainingMin: number;
  lotsJumpingDays: number;
}

export interface WeeklyReview {
  weekStart: DateKey;
  weekEnd: DateKey;
  generatedAt: number;
  keepDoing: ReviewItem[];
  readyToProgress: ReviewItem[];
  improve: ReviewItem[];
  safety: ReviewItem[];
  /** 3.0.0: evidence of progress, missing data, recovery concerns, and reasons for a professional review. */
  progress?: ReviewItem[];
  insufficient?: ReviewItem[];
  recovery?: ReviewItem[];
  professional?: ReviewItem[];
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
  /** A professionally reviewed daily energy range, if there is one. */
  reviewedKcal: [number, number] | null;
  /** What the example meals add up to on a usual day, for the low intake check only. */
  exampleKcal: number | null;
  sportLogs?: SportLog[];
  athlete?: AthleteProfile;
  ageYears?: number | null;
  creatineActive?: boolean;
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
  let homePlanned = 0;
  let swimPlanned = 0;
  let calfPlanned = 0;
  let plannedMeals = 0;
  for (const key of days) {
    const day = data.planDays.find((d) => d.weekday === weekdayOf(key));
    if (!day) continue;
    const sess = new Set(day.items.map((i) => i.session));
    plannedSessions += sess.size;
    if (sess.has('morning') || sess.has('home')) homePlanned++;
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
  let reviewedRangeDays: number | null = data.reviewedKcal ? 0 : null;
  let lowIntakeDays = 0;
  for (const [, logs] of foodByDay) {
    const t = dayTotals(logs);
    if (data.reviewedKcal && t.mid.kcal >= data.reviewedKcal[0] && t.mid.kcal <= data.reviewedKcal[1]) reviewedRangeDays = (reviewedRangeDays ?? 0) + 1;
    // Only a day where most meals were logged counts, and only when even the top of the estimate is far
    // below the example meals or the reviewed range. It is a recovery signal, not a target.
    const floor = data.reviewedKcal ? data.reviewedKcal[0] * 0.8 : data.exampleKcal ? data.exampleKcal * 0.75 : null;
    if (floor !== null && logs.length >= 4 && t.high.kcal < floor) lowIntakeDays++;
  }
  const proteinMeals = food.filter((f) => dayTotals([f]).mid.protein >= 20).length;
  const exposure = weeklyExposure(weekStart, data.sessions, data.sportLogs ?? [], data.setLogs, (id) => data.exerciseKind(id) === 'jump');
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
    homeDone: sessions.filter((s) => s.session === 'morning' || s.session === 'home').length,
    homePlanned,
    swimDone: sessions.filter((s) => s.session === 'swim').length,
    swimPlanned,
    volleyballExposures,
    jumpLandingPoor,
    foodDays: foodByDay.size,
    proteinMeals,
    reviewedRangeDays,
    lowIntakeDays,
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
    sportMin: exposure.sportMin,
    trainingMin: exposure.trainingMin,
    lotsJumpingDays: exposure.lotsJumpingDays,
  };
}

const f1 = (n: number | null, unit = '') => (n === null ? 'No data' : `${n.toFixed(1)}${unit}`);

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
  if (cur.lowIntakeDays >= 2) {
    safety.push({
      id: 'low-energy',
      text: 'On some fully logged days, food was well below the example meals. Eating this little makes recovery and growth harder. Eat more and talk with a parent.',
      evidence: [`${cur.lowIntakeDays} fully logged days were far below the example meals even at the top of the estimate.`, 'Stable weight would not prove that food is enough.'],
      confidence: 'medium',
      weight: 85,
    });
  }
  if (cur.sleepAvgH !== null && cur.sleepAvgH < 7 && cur.sleepNights >= 4) {
    safety.push({ id: 'sleep-low', text: 'Sleep averaged under seven hours. That is well below the eight to ten hours teens need.', evidence: [`${cur.sleepNights} nights logged, average ${cur.sleepAvgH.toFixed(1)} hours.`], confidence: 'high', weight: 70 });
  }

  // ---- Keep doing ----
  if (cur.homePlanned > 0 && cur.homeDone >= cur.homePlanned) {
    keepDoing.push({ id: 'home', text: `You completed all ${cur.homePlanned} home sessions.`, evidence: [`${cur.homeDone} of ${cur.homePlanned} logged.`], confidence: 'high', weight: 10 });
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
  if (cur.loggedMeals >= 10 && cur.proteinMeals >= cur.loggedMeals * 0.6) {
    keepDoing.push({ id: 'protein', text: `Most meals had a good protein portion: ${cur.proteinMeals} of ${cur.loggedMeals} logged meals had 20 g or more.`, evidence: ['Protein spread over the day helps muscles recover.'], confidence: 'medium', weight: 6 });
  }
  if (cur.morningWeights >= 4 && data.athlete?.weight.mode !== 'weekly') {
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
  if (cur.morningWeights < 4 && (data.athlete?.weight.mode ?? 'frequent') === 'frequent') {
    improve.push({
      id: 'weights-few',
      text: `${cur.morningWeights === 0 ? 'No morning weights were' : `Only ${cur.morningWeights} morning weight${cur.morningWeights === 1 ? ' was' : 's were'}`} logged, so the trend is too uncertain for a nutrition change.`,
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
      text: `${missed === 1 ? 'One planned session was' : `${missed} planned sessions were`} not logged. If the week got busy, a missed session can move to another day without doubling up.`,
      evidence: [`${cur.completedSessions} of ${cur.plannedSessions} sessions logged.`],
      confidence: 'high',
      weight: 16,
    });
  }
  if (cur.foodDays < 5) {
    improve.push({ id: 'food-log', text: `${cur.foodDays === 0 ? 'No food was logged this week' : `Food was logged on ${cur.foodDays} day${cur.foodDays === 1 ? '' : 's'}`}. Logging is optional; the one tap example meals make it quick when it helps.`, evidence: ['The nutrition check reads better with ten or more logged days in two weeks.'], confidence: 'high', weight: 8 });
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
    cmp('Home sessions', `${prev.homeDone} of ${prev.homePlanned}`, `${cur.homeDone} of ${cur.homePlanned}`),
    cmp('School and club sport', `${Math.round(prev.sportMin)} min`, `${Math.round(cur.sportMin)} min`, 'From your sport log'),
    cmp('Swims', `${prev.swimDone} of ${prev.swimPlanned}`, `${cur.swimDone} of ${cur.swimPlanned}`),
    cmp('Volleyball and jump exercises', String(prev.volleyballExposures), String(cur.volleyballExposures)),
    cmp('Days with food logged', String(prev.foodDays), String(cur.foodDays)),
    cmp('Meals with 20 g protein or more', String(prev.proteinMeals), String(cur.proteinMeals)),
    cmp('Days in the reviewed energy range', prev.reviewedRangeDays === null ? 'No reviewed target' : String(prev.reviewedRangeDays), cur.reviewedRangeDays === null ? 'No reviewed target' : String(cur.reviewedRangeDays), 'Estimated'),
    cmp('Meals logged as planned', String(prev.asPlannedMeals), String(cur.asPlannedMeals)),
    cmp('Water entries', String(prev.waterEntries), String(cur.waterEntries)),
    cmp('Average sleep', f1(prev.sleepAvgH, ' h'), f1(cur.sleepAvgH, ' h')),
    cmp('Morning weights', String(prev.morningWeights), String(cur.morningWeights), 'Optional'),
    cmp('Seven day weight average', prev.weightReliable ? f1(prev.weightAvg, ' kg') : 'Too few', cur.weightReliable ? f1(cur.weightAvg, ' kg') : 'Too few'),
    cmp('Waist', f1(prev.waistLast, ' cm'), f1(cur.waistLast, ' cm')),
    cmp('Scale body fat', prev.bodyFatAvg === null ? 'Too few' : f1(prev.bodyFatAvg, '%'), cur.bodyFatAvg === null ? 'Too few' : f1(cur.bodyFatAvg, '%'), 'Trend only, low confidence'),
    cmp('Energy', f1(prev.energy), f1(cur.energy), 'Out of 5'),
    cmp('Mood', f1(prev.mood), f1(cur.mood), 'Out of 5'),
    cmp('Soreness', f1(prev.soreness), f1(cur.soreness), 'Out of 3'),
    cmp('School concentration', f1(prev.concentration), f1(cur.concentration), 'Out of 5'),
  ];

  const extra = reviewSections(data, cur, prev, s.stopProgression, ready);

  const byWeight = (a: ReviewItem, b: ReviewItem) => b.weight - a.weight;
  const priorities = [...safety.sort(byWeight), ...extra.recovery.sort(byWeight), ...improve.sort(byWeight)].slice(0, 3).map((i) => i.text);
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
    progress: extra.progress.sort(byWeight),
    insufficient: extra.insufficient.sort(byWeight),
    recovery: extra.recovery.sort(byWeight),
    professional: extra.professional.sort(byWeight),
    priorities,
    current: cur,
    previous: prev,
    comparison,
    backupDaysAgo,
  };
}

/**
 * The four 3.0.0 sections. Each item states its evidence. Nothing here changes a target: progress
 * means the athlete may confirm a step, and the rest point to rest, more data, or a person to ask.
 */
function reviewSections(data: ReviewData, cur: WeekMetrics, prev: WeekMetrics, paused: boolean, ready: ReviewItem[]) {
  const progress: ReviewItem[] = [];
  const insufficient: ReviewItem[] = [];
  const recovery: ReviewItem[] = [];
  const professional: ReviewItem[] = [];
  const a = data.athlete;

  // Evidence of progress: comparable performance and consistency, not the scale.
  const qualified = ready.filter((r) => r.id.startsWith('prog-'));
  if (qualified.length && !paused) progress.push({ id: 'qualified', text: `${qualified.length} exercise${qualified.length === 1 ? '' : 's'} met every work set target with good form and no pain.`, evidence: qualified.map((q) => q.text), confidence: 'high', weight: 20 });
  if (cur.plannedSessions > 0 && cur.completedSessions >= Math.ceil(cur.plannedSessions * 0.8)) progress.push({ id: 'consistent', text: 'A consistent week: most planned sessions were done.', evidence: [`${cur.completedSessions} of ${cur.plannedSessions} sessions.`], confidence: 'high', weight: 12 });
  if (cur.volleyballExposures > 0 && cur.jumpLandingPoor === 0) progress.push({ id: 'landings', text: 'Landings were controlled: none rated poor.', evidence: [`${cur.volleyballExposures} jump and skill exercises logged.`], confidence: 'medium', weight: 8 });

  // Not enough data yet.
  if (cur.sleepNights < 4) insufficient.push({ id: 'sleep-data', text: 'Sleep was logged on fewer than four nights.', evidence: [`${cur.sleepNights} nights logged.`], confidence: 'high', weight: 8 });
  if ((a?.weight.mode ?? 'frequent') !== 'off' && !cur.weightReliable && !prev.weightReliable) insufficient.push({ id: 'weight-data', text: 'Too few morning weights for a trend. That is fine: weight alone says little.', evidence: [STABLE_WEIGHT_NOTE], confidence: 'high', weight: 6 });
  if (a && !a.sport.confirmed && cur.sportMin === 0) insufficient.push({ id: 'sport-data', text: 'School sport is not logged, so the total weekly load is unknown.', evidence: ['Add your usual week in More, Your profile, or log practices in More, School sport.'], confidence: 'high', weight: 10 });
  if (a && (a.home.space === 'unknown' || a.home.ceiling === 'unknown')) insufficient.push({ id: 'home-data', text: 'Your space at home is not described, so home sessions use quiet drills without jumps.', evidence: ['More, Your profile, Your space at home.'], confidence: 'high', weight: 9 });

  // Recovery concerns.
  if (cur.soreness !== null && cur.soreness >= 2) recovery.push({ id: 'soreness', text: 'Soreness stayed high this week. Muscle soreness that lasts more than two or three days, or joint pain, is a reason to train lighter and tell a parent or coach.', evidence: [`Average soreness ${cur.soreness.toFixed(1)} of 3 in the check ins.`], confidence: 'medium', weight: 40 });
  if (cur.sleepAvgH !== null && cur.sleepAvgH < 8 && cur.sleepNights >= 4) recovery.push({ id: 'sleep-short', text: `Sleep averaged ${cur.sleepAvgH.toFixed(1)} hours, under the 8 to 10 hours teens need.`, evidence: [`${cur.sleepNights} nights logged.`], confidence: 'high', weight: 35 });
  if (cur.jumpLandingPoor > 0) recovery.push({ id: 'landings-poor', text: 'Some landings were rated poor. Keep jump sets shorter and stop when landings get loud.', evidence: [`${cur.jumpLandingPoor} sets with poor landings.`], confidence: 'medium', weight: 30 });
  if (cur.lotsJumpingDays >= 3) recovery.push({ id: 'sport-jumps', text: 'School sport had a lot of jumping on three or more days. Shorter home jump sessions are wise in weeks like this.', evidence: [`${cur.lotsJumpingDays} sport days with a lot of jumping.`], confidence: 'medium', weight: 28 });
  if (cur.energy !== null && prev.energy !== null && prev.energy - cur.energy >= 0.7) recovery.push({ id: 'energy-drop', text: 'Energy dropped compared with last week.', evidence: [`${prev.energy.toFixed(1)} to ${cur.energy.toFixed(1)} out of 5.`], confidence: 'medium', weight: 25 });
  const hours = (cur.sportMin + cur.trainingMin) / 60;
  const above = hoursAboveAge({ weekStart: cur.weekStart, trainingMin: cur.trainingMin, sportMin: cur.sportMin, totalMin: cur.sportMin + cur.trainingMin, jumpContacts: 0, lotsJumpingDays: cur.lotsJumpingDays, hardSportSessions: 0, activeDays: 0 }, data.ageYears ?? null);
  if (above) recovery.push({ id: 'hours', text: `Sport and training took about ${hours.toFixed(1)} hours this week, more hours than your age in years. That has been linked to more overuse injuries in young athletes. Review the week with a parent or coach.`, evidence: [`${Math.round(cur.sportMin)} min sport and ${Math.round(cur.trainingMin)} min planned sessions logged.`], confidence: 'medium', weight: 45 });

  // Reasons for a professional review.
  if (a && a.wrist.status !== 'cleared') professional.push({ id: 'wrist', text: a.wrist.status === 'symptoms' ? 'The wrist has pain or swelling. See the clinician who treated the injury before loading it again.' : 'Ask the clinician who treated the wrist whether it is cleared for gripping, pressing, and ball contact.', evidence: ['Until then, loads on wrist heavy exercises stay the same and ball contact is left out.'], confidence: 'high', weight: a.wrist.status === 'symptoms' ? 70 : 40 });
  if (data.creatineActive || (a?.supplements.creatineProduct ?? '') !== '') {
    if (!a?.supplements.reviewedBy) professional.push({ id: 'creatine', text: 'Creatine has not been reviewed with a parent and a clinician yet.', evidence: ['Evidence in under 18s is limited, product quality varies, and the AAP discourages performance supplements for young athletes.'], confidence: 'high', weight: 35 });
  }
  const physique = (a?.aspirations ?? []).some((x) => /fat|muscle|weight|kg|%|lean|cut|bulk/i.test(x.text));
  if (physique && !(a?.reviewed ?? []).some((r) => r.status === 'professionally reviewed' && (r.kind === 'body-composition' || r.kind === 'weight' || r.kind === 'energy'))) {
    professional.push({ id: 'physique', text: 'Your body composition aspirations have not been reviewed with a pediatric professional. They can set a safe rate, a way to measure progress, and how much to eat.', evidence: ['PeakForm keeps your aspirations as you wrote them and sets no weight or body fat targets itself.'], confidence: 'high', weight: 30 });
  }
  if (cur.lowIntakeDays >= 2) professional.push({ id: 'intake', text: 'Food was low on several fully logged days. If that continues, a pediatric sports dietitian can check whether you eat enough.', evidence: [`${cur.lowIntakeDays} days.`], confidence: 'medium', weight: 50 });
  return { progress, insufficient, recovery, professional };
}
