import { FOOD_BY_ID } from '../content/foods';
import type { MealTemplate, NutritionTarget } from '../content/meals';
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

// ---------- Weekly weighing ----------

/** One morning weight per Monday to Sunday week, the first standard one, for people who weigh once a week. */
export function weeklyWeights(points: WeightPoint[], end: DateKey, weeks: number): Array<{ weekEnd: DateKey; kg: number | null }> {
  const out: Array<{ weekEnd: DateKey; kg: number | null }> = [];
  for (let w = weeks - 1; w >= 0; w--) {
    const we = addDays(end, -7 * w);
    const ws = addDays(we, -6);
    const p = points.find((x) => x.date >= ws && x.date <= we);
    out.push({ weekEnd: we, kg: p ? p.kg : null });
  }
  return out;
}

// ---------- The nutrition check ----------

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
  /** Signals from training and wellbeing. */
  performanceDecline: boolean;
  wellbeing: { previous: WellbeingWeek; current: WellbeingWeek };
  /** How often the athlete chose to weigh. Defaults to several mornings a week. */
  weightMode?: 'frequent' | 'weekly' | 'off';
}

export type AdjustmentStatus = 'insufficient-data' | 'no-change' | 'eat-more' | 'talk-to-parent';

export interface AdjustmentResult {
  status: AdjustmentStatus;
  title: string;
  /** A suggested increase in daily food as a calorie range, or null. PeakForm never suggests eating less. */
  kcalChange: [number, number] | null;
  reasons: string[];
  missing: string[];
  confidence: 'high' | 'medium' | 'low';
  weeklyChangeKg: number | null;
  waistChangeCm: number | null;
  involveGuardian: boolean;
}

/**
 * Above this weekly loss PeakForm suggests more food. About 0.45 kg (1 lb) a week is the upper rate
 * the AAP gives for a growing athlete (Carl 2017).
 */
export const FAST_LOSS_KG_PER_WEEK = 0.45;
export const STABLE_WEIGHT_KG = 0.25;
export const MIN_FOOD_DAYS = 10;

/** Said wherever stable weight comes up, because both mistakes are easy to make. */
export const STABLE_WEIGHT_NOTE =
  'A steady weight over a week or two is not a plateau, and it does not show whether you eat enough. Growth, training, water, food in the gut, and creatine all move the scale.';

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
 * The nutrition check. It needs fourteen days of useful data, never uses smart scale body fat,
 * never suggests eating less, and never changes anything by itself. Weight loss that is too fast,
 * or a slide in energy, mood, sleep, or performance, leads to eating more and talking with a parent.
 * Everything else is "no change": personal energy targets belong to a parent and a pediatric professional.
 */
export function nutritionAdjustment(input: AdjustmentInput): AdjustmentResult {
  const end = input.today;
  const mode = input.weightMode ?? 'frequent';
  const declines = wellbeingDeclined(input.wellbeing.previous, input.wellbeing.current);
  const sliding = input.performanceDecline || declines.length > 0;
  const base: Omit<AdjustmentResult, 'status' | 'title'> = { kcalChange: null, reasons: [], missing: [], confidence: 'low', weeklyChangeKg: null, waistChangeCm: null, involveGuardian: false };

  const slideResult = (trend: string | null): AdjustmentResult => ({
    ...base,
    status: 'talk-to-parent',
    title: 'Energy, mood, sleep, or performance dipped. Eat a bit more and talk with a parent',
    kcalChange: [150, 250],
    reasons: [...(trend ? [trend] : []), ...(input.performanceDecline ? ['Training performance declined.'] : []), ...declines, STABLE_WEIGHT_NOTE, 'An extra snack a day, such as fruit with yogurt or a sandwich, is a simple start. If it continues, a pediatrician or pediatric sports dietitian can check whether you are eating enough.'],
    involveGuardian: true,
  });

  if (mode === 'off') {
    if (sliding) return slideResult(null);
    return { ...base, status: 'insufficient-data', title: 'Weighing is off', reasons: ['PeakForm reads energy, mood, sleep, recovery, and training instead. That is enough for day to day decisions.'] };
  }

  const points = morningWeights(input.checkins);
  const start14 = addDays(end, -13);
  const foodDays = new Set(input.foodLogDays.filter((d) => d >= start14 && d <= end)).size;
  const missing: string[] = [];
  let before: number | null = null;
  let after: number | null = null;
  let perWeek: number | null = null;
  let counts = 0;
  if (mode === 'weekly') {
    const ws = weeklyWeights(points, end, 4).filter((w) => w.kg !== null);
    if (ws.length < 3) missing.push(`${ws.length} of the last 4 weeks have a morning weight. At least 3 are needed for a trend.`);
    else {
      const first = ws[0]!;
      const last = ws[ws.length - 1]!;
      before = first.kg;
      after = last.kg;
      perWeek = Math.round(((last.kg! - first.kg!) / Math.max(1, diffDays(last.weekEnd, first.weekEnd) / 7)) * 100) / 100;
      counts = ws.length;
    }
  } else {
    const w2 = sevenDayAverage(points, end);
    const w1 = sevenDayAverage(points, addDays(end, -7));
    if (!w1.reliable) missing.push(`Week one has ${w1.count} of ${MIN_WEIGHTS_PER_WEEK} morning weights needed.`);
    if (!w2.reliable) missing.push(`Week two has ${w2.count} of ${MIN_WEIGHTS_PER_WEEK} morning weights needed.`);
    if (w1.reliable && w2.reliable && w1.avg !== null && w2.avg !== null) {
      before = w1.avg;
      after = w2.avg;
      perWeek = Math.round((w2.avg - w1.avg) * 100) / 100;
      counts = Math.min(w1.count, w2.count);
    }
  }
  const foodNote = foodDays < MIN_FOOD_DAYS ? `Food was logged on ${foodDays} of the last 14 days. Logging is optional; with fewer logs the check reads only weight and wellbeing.` : null;
  if (input.planStart && diffDays(end, input.planStart) < 13) missing.push('The plan started less than fourteen days ago.');

  const trend = before !== null && after !== null && perWeek !== null ? `Weight went from about ${before.toFixed(1)} kg to ${after.toFixed(1)} kg (${perWeek > 0 ? '+' : ''}${perWeek.toFixed(2)} kg a week).` : null;
  if (sliding) return { ...slideResult(trend), weeklyChangeKg: perWeek, missing };
  if (missing.length > 0 || perWeek === null) {
    return { ...base, status: 'insufficient-data', title: 'Not enough data yet to read the trend', missing, reasons: [STABLE_WEIGHT_NOTE] };
  }
  if (foodNote) base.reasons.push(foodNote);

  const waistW1 = input.waist.filter((m) => m.date >= start14 && m.date <= addDays(end, -7)).sort((a, b) => a.date.localeCompare(b.date));
  const waistW2 = input.waist.filter((m) => m.date > addDays(end, -7) && m.date <= end).sort((a, b) => a.date.localeCompare(b.date));
  const waistChange = waistW1.length && waistW2.length ? Math.round((waistW2[waistW2.length - 1]!.cm - waistW1[0]!.cm) * 10) / 10 : null;
  const firstWeek = input.planStart !== null && diffDays(addDays(end, -13), input.planStart) < 7;
  const confidence: AdjustmentResult['confidence'] = counts >= 6 && waistChange !== null ? 'high' : 'medium';
  const r: Omit<AdjustmentResult, 'status' | 'title'> = { ...base, confidence, weeklyChangeKg: perWeek, waistChangeCm: waistChange };
  const loss = -perWeek;

  if (loss > FAST_LOSS_KG_PER_WEEK && !firstWeek) {
    return {
      ...r,
      status: 'eat-more',
      title: 'Weight is falling fast. Eat a bit more and talk with a parent',
      kcalChange: [150, 250],
      reasons: [trend!, `That is faster than about ${FAST_LOSS_KG_PER_WEEK} kg a week, the upper rate advised for a growing athlete.`, 'Speak with a parent, and a pediatrician or pediatric sports dietitian if it continues.', ...base.reasons],
      involveGuardian: true,
    };
  }
  return {
    ...r,
    status: 'no-change',
    title: 'No change suggested',
    reasons: [
      trend!,
      ...(waistChange !== null ? [`Waist changed ${waistChange > 0 ? '+' : ''}${waistChange.toFixed(1)} cm.`] : []),
      STABLE_WEIGHT_NOTE,
      'PeakForm never cuts food from a weight trend. Goals about weight or body fat are worth reviewing with a parent and a pediatric professional, who can also say whether you eat enough.',
      ...base.reasons,
    ],
  };
}

// ---------- Example day ----------

/** What the example meals for a day add up to. A description of the examples, never a target or a limit. */
export function exampleDayTotals(templates: MealTemplate[], optionalOn: Record<string, boolean> = {}): Totals {
  return sumItems(templates.flatMap((t) => templateItems(t, optionalOn)));
}
