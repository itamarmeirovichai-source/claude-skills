import { FOOD_BY_ID } from '../content/foods';
import { NUTRITION_FLOORS, type MealTemplate, type NutritionTarget } from '../content/meals';
import type { BodyCheckIn, FoodLog, FoodLogItem, WaistMeasurement } from '../db/records';
import { addDays, diffDays, type DateKey } from './dates';
import { itemFromGrams, sumItems, type Totals } from './portions';

// ---------- Templates and day totals ----------

export function templateItems(t: MealTemplate, optionalOn: Record<string, boolean> = {}): FoodLogItem[] {
  return t.items
    .filter((it) => !it.optional || (optionalOn[it.foodId] ?? it.defaultOn ?? false))
    .map((it) => {
      const f = FOOD_BY_ID[it.foodId];
      if (!f) throw new Error(`Template ${t.id} uses unknown food ${it.foodId}`);
      // Cafeteria portions are not weighed, so the template carries household level uncertainty.
      const item = itemFromGrams(f, it.grams, 'template');
      if (t.estimated) {
        const widen = 0.2;
        return {
          ...item,
          estimate: { ...item.estimate, method: 'household' as const, gramsLow: Math.round(it.grams * (1 - widen)), gramsHigh: Math.round(it.grams * (1 + widen)), confidence: 'medium' as const },
          low: itemFromGrams(f, it.grams * (1 - widen), 'template').low,
          high: itemFromGrams(f, it.grams * (1 + widen), 'template').high,
        };
      }
      return item;
    });
}

export function templateTotals(t: MealTemplate, optionalOn: Record<string, boolean> = {}): Totals {
  return sumItems(templateItems(t, optionalOn));
}

export function dayTotals(logs: FoodLog[]): Totals {
  return sumItems(logs.flatMap((l) => l.items));
}

export type RangeStatus = 'below' | 'within' | 'above' | 'unknown';

/** Compare a day with its target. Uses the midpoint, and says unknown when the range straddles the band widely. */
export function calorieStatus(t: Totals, target: NutritionTarget): RangeStatus {
  if (t.mid.kcal === 0) return 'unknown';
  const [lo, hi] = target.kcalBand;
  if (t.mid.kcal < lo) return 'below';
  if (t.mid.kcal > hi) return 'above';
  return 'within';
}

/** Protein target is a floor with a typical range. Above the range is not a problem by itself. */
export function proteinMet(t: Totals, target: NutritionTarget): boolean {
  return t.mid.protein >= target.proteinRange[0];
}

// ---------- Weight trend ----------

export interface WeightPoint {
  date: DateKey;
  kg: number;
}

/** Morning weights taken under standard conditions, one per day (first of the day). */
export function morningWeights(checkins: BodyCheckIn[]): WeightPoint[] {
  const byDay = new Map<DateKey, WeightPoint>();
  for (const c of [...checkins].sort((a, b) => a.at - b.at)) {
    if (c.weightKg === null || !c.standardConditions) continue;
    if (!byDay.has(c.date)) byDay.set(c.date, { date: c.date, kg: c.weightKg });
  }
  return [...byDay.values()].sort((a, b) => a.date.localeCompare(b.date));
}

export interface WindowAverage {
  start: DateKey;
  end: DateKey;
  count: number;
  avg: number | null;
  /** A weekly trend needs at least four morning measurements. */
  reliable: boolean;
}

export const MIN_WEIGHTS_PER_WEEK = 4;

export function sevenDayAverage(points: WeightPoint[], end: DateKey): WindowAverage {
  const start = addDays(end, -6);
  const inWin = points.filter((p) => p.date >= start && p.date <= end);
  const avg = inWin.length ? inWin.reduce((a, p) => a + p.kg, 0) / inWin.length : null;
  return { start, end, count: inWin.length, avg: avg === null ? null : Math.round(avg * 100) / 100, reliable: inWin.length >= MIN_WEIGHTS_PER_WEEK };
}

/** Rolling seven day averages for charting, one value per day where the window has data. */
export function rollingAverages(points: WeightPoint[], from: DateKey, to: DateKey): Array<WindowAverage> {
  const out: WindowAverage[] = [];
  for (let d = from; d <= to; d = addDays(d, 1)) out.push(sevenDayAverage(points, d));
  return out;
}

// ---------- Fourteen day adjustment gate ----------

export interface WellbeingWeek {
  energy: number | null;
  mood: number | null;
  concentration: number | null;
  sleepHours: number | null;
}

export interface AdjustmentInput {
  today: DateKey;
  planStart: DateKey | null;
  checkins: BodyCheckIn[];
  waist: WaistMeasurement[];
  foodLogDays: DateKey[];
  currentKcal: number;
  /** Signals from training and wellbeing. */
  performanceDecline: boolean;
  wellbeing: { previous: WellbeingWeek; current: WellbeingWeek };
}

export type AdjustmentStatus =
  | 'insufficient-data'
  | 'hold'
  | 'hold-recomposition'
  | 'check-then-reduce'
  | 'increase'
  | 'clinician-review';

export interface AdjustmentResult {
  status: AdjustmentStatus;
  title: string;
  /** Suggested change to daily calories as a range, or null for no change. */
  kcalChange: [number, number] | null;
  reasons: string[];
  missing: string[];
  confidence: 'high' | 'medium' | 'low';
  weeklyChangeKg: number | null;
  waistChangeCm: number | null;
  involveGuardian: boolean;
}

export const FAST_LOSS_KG_PER_WEEK = 0.7;
export const STABLE_WEIGHT_KG = 0.25;
export const STABLE_WAIST_CM = 0.5;
export const MIN_FOOD_DAYS = 10;

function wellbeingDeclined(prev: WellbeingWeek, cur: WellbeingWeek): string[] {
  const out: string[] = [];
  const check = (label: string, a: number | null, b: number | null, drop: number) => {
    if (a !== null && b !== null && a - b >= drop) out.push(`${label} dropped from ${a.toFixed(1)} to ${b.toFixed(1)}`);
  };
  check('Energy', prev.energy, cur.energy, 0.7);
  check('Mood', prev.mood, cur.mood, 0.7);
  check('Concentration', prev.concentration, cur.concentration, 0.7);
  if (cur.sleepHours !== null && cur.sleepHours < 7.5) out.push(`Average sleep was ${cur.sleepHours.toFixed(1)} hours`);
  return out;
}

/**
 * The nutrition decision gate. Runs only with fourteen days of useful data and never
 * suggests going below the calorie floor. Smart scale body fat is never an input.
 */
export function nutritionAdjustment(input: AdjustmentInput): AdjustmentResult {
  const end = input.today;
  const w2 = sevenDayAverage(morningWeights(input.checkins), end);
  const w1 = sevenDayAverage(morningWeights(input.checkins), addDays(end, -7));
  const start14 = addDays(end, -13);
  const foodDays = new Set(input.foodLogDays.filter((d) => d >= start14 && d <= end)).size;
  const missing: string[] = [];
  if (!w1.reliable) missing.push(`Week one has ${w1.count} of ${MIN_WEIGHTS_PER_WEEK} morning weights needed.`);
  if (!w2.reliable) missing.push(`Week two has ${w2.count} of ${MIN_WEIGHTS_PER_WEEK} morning weights needed.`);
  if (foodDays < MIN_FOOD_DAYS) missing.push(`Food was logged on ${foodDays} of the last 14 days. At least ${MIN_FOOD_DAYS} are needed.`);
  if (input.planStart && diffDays(end, input.planStart) < 13) missing.push('The plan started less than fourteen days ago.');

  const base: Omit<AdjustmentResult, 'status' | 'title'> = {
    kcalChange: null,
    reasons: [],
    missing,
    confidence: 'low',
    weeklyChangeKg: null,
    waistChangeCm: null,
    involveGuardian: false,
  };

  if (missing.length > 0 || w1.avg === null || w2.avg === null) {
    return { ...base, status: 'insufficient-data', title: 'Not enough data yet for a nutrition change' };
  }

  const change = Math.round((w2.avg - w1.avg) * 100) / 100; // kg per week, negative is loss
  const loss = -change;
  const waistW1 = input.waist.filter((m) => m.date >= start14 && m.date <= addDays(end, -7)).sort((a, b) => a.date.localeCompare(b.date));
  const waistW2 = input.waist.filter((m) => m.date > addDays(end, -7) && m.date <= end).sort((a, b) => a.date.localeCompare(b.date));
  const waistChange = waistW1.length && waistW2.length ? Math.round((waistW2[waistW2.length - 1]!.cm - waistW1[0]!.cm) * 10) / 10 : null;
  const declines = wellbeingDeclined(input.wellbeing.previous, input.wellbeing.current);
  const firstWeek = input.planStart !== null && diffDays(addDays(end, -13), input.planStart) < 7;
  const confidence: AdjustmentResult['confidence'] = w1.count >= 6 && w2.count >= 6 && waistChange !== null ? 'high' : 'medium';
  const r: Omit<AdjustmentResult, 'status' | 'title'> = { ...base, confidence, weeklyChangeKg: change, waistChangeCm: waistChange };
  const trend = `Seven day average went from ${w1.avg.toFixed(1)} kg to ${w2.avg.toFixed(1)} kg (${change > 0 ? '+' : ''}${change.toFixed(2)} kg).`;

  // Too fast, or wellbeing and performance are sliding: add food, involve a parent.
  const sliding = input.performanceDecline || declines.length > 0;
  if (sliding && change > STABLE_WEIGHT_KG) {
    return {
      ...r,
      status: 'clinician-review',
      title: 'Wellbeing or performance dipped. Talk with a parent',
      reasons: [trend, ...(input.performanceDecline ? ['Training performance declined.'] : []), ...declines, 'Weight is not falling, so eating less is not the answer. Check sleep, illness, stress, and training load with a parent or coach.'],
      involveGuardian: true,
    };
  }
  if ((loss > FAST_LOSS_KG_PER_WEEK && !firstWeek) || sliding) {
    const reasons = [trend];
    if (loss > FAST_LOSS_KG_PER_WEEK && !firstWeek) reasons.push(`That is faster than about ${FAST_LOSS_KG_PER_WEEK} kg per week.`);
    if (input.performanceDecline) reasons.push('Training performance declined.');
    reasons.push(...declines);
    return {
      ...r,
      status: 'increase',
      title: 'Add 150 to 200 calories a day and talk with a parent',
      kcalChange: [150, 200],
      reasons: [...reasons, 'Speak with a parent, and a pediatrician or pediatric sports dietitian if it continues.'],
      involveGuardian: true,
    };
  }

  if (loss >= STABLE_WEIGHT_KG && loss <= FAST_LOSS_KG_PER_WEEK) {
    return { ...r, status: 'hold', title: 'Keep the plan as it is', reasons: [trend, 'That is a steady, gradual rate with stable performance.'] };
  }

  const waistDown = waistChange !== null && waistChange <= -STABLE_WAIST_CM;
  if (loss < STABLE_WEIGHT_KG && waistDown) {
    return {
      ...r,
      status: 'hold-recomposition',
      title: 'Keep the plan. This may be a recomposition pattern',
      reasons: [trend, `Waist went down ${Math.abs(waistChange!).toFixed(1)} cm while weight held steady, and performance is stable.`],
    };
  }

  if (waistChange === null) {
    return {
      ...r,
      status: 'insufficient-data',
      title: 'Measure your waist before changing anything',
      confidence: 'low',
      reasons: [trend],
      missing: ['A waist measurement in each of the two weeks is needed to judge a stable weight.'],
    };
  }

  // Weight and waist stable (or rising): check the estimates first, then a small change.
  const reduction: [number, number] = [100, 150];
  const reasons = [
    trend,
    `Waist changed ${waistChange > 0 ? '+' : ''}${waistChange.toFixed(1)} cm.`,
    'First check portion estimates, cooking oil, sauces, weekend grazing, and missing logs.',
    'You are still growing, so some weight gain can be growth. A parent or clinician can help judge this.',
  ];
  if (input.currentKcal - reduction[1] < NUTRITION_FLOORS.kcal || input.currentKcal - reduction[0] < NUTRITION_FLOORS.kcal) {
    return {
      ...r,
      status: 'clinician-review',
      title: 'Talk with a parent and a clinician before any reduction',
      reasons: [...reasons, `A reduction would take daily calories below ${NUTRITION_FLOORS.kcal}. PeakForm never suggests that.`],
      involveGuardian: true,
    };
  }
  return {
    ...r,
    status: 'check-then-reduce',
    title: 'Check your estimates, then consider 100 to 150 fewer calories',
    kcalChange: [-reduction[1], -reduction[0]],
    reasons: [...reasons, 'A modest routine change, such as a smaller evening portion, also works.'],
  };
}

/** Apply a confirmed calorie change, never crossing the floor. */
export function applyKcalChange(current: number, delta: number): number {
  return Math.max(NUTRITION_FLOORS.kcal, Math.round(current + delta));
}
