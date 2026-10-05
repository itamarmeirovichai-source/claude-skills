import { describe, expect, it } from 'vitest';
import { BASELINE_TARGETS, BREAKFAST, DINNERS, NUTRITION_FLOORS, PREWORKOUT, SCHOOL_LUNCH, EVENING, templatesForDay } from '../src/content/meals';
import { FOOD_BY_ID } from '../src/content/foods';
import { SHOPPING_LIST, scaleShopping } from '../src/content/recipes';
import { addDays, rangeKeys } from '../src/domain/dates';
import { applyKcalChange, morningWeights, nutritionAdjustment, sevenDayAverage, templateTotals, type AdjustmentInput } from '../src/domain/nutrition';
import { itemFromGrams, itemFromPortion, sumItems, formatRange } from '../src/domain/portions';
import type { BodyCheckIn, WaistMeasurement } from '../src/db/records';

function checkin(date: string, kg: number | null, standard = true): BodyCheckIn {
  return {
    id: `c-${date}`,
    createdAt: 0,
    updatedAt: 0,
    date,
    at: Date.parse(`${date}T07:00:00Z`),
    weightKg: kg,
    bodyFatPct: null,
    standardConditions: standard,
    energy: 4,
    mood: 4,
    concentration: 4,
    hunger: 3,
    soreness: {},
    illness: false,
    illnessNote: '',
    hydrationNote: '',
    redFlags: [],
    note: '',
  };
}
const waist = (date: string, cm: number): WaistMeasurement => ({ id: `w-${date}`, createdAt: 0, updatedAt: 0, date, cm, standardConditions: true });

function input(weights: Array<number | null>, waists: Array<[number, number]>, extra: Partial<AdjustmentInput> = {}): AdjustmentInput {
  const today = '2026-10-14';
  const start = addDays(today, -13);
  const days = rangeKeys(start, 14);
  return {
    today,
    planStart: addDays(start, -14),
    checkins: days.map((d, i) => checkin(d, weights[i] ?? null)).filter((c) => c.weightKg !== null),
    waist: waists.map(([i, cm]) => waist(days[i]!, cm)),
    foodLogDays: days,
    currentKcal: 2450,
    performanceDecline: false,
    wellbeing: { previous: { energy: 4, mood: 4, concentration: 4, sleepHours: 8.5 }, current: { energy: 4, mood: 4, concentration: 4, sleepHours: 8.5 } },
    ...extra,
  };
}
const flat = (kg: number, n = 14) => Array.from({ length: n }, () => kg);
const slope = (start: number, perWeek: number) => Array.from({ length: 14 }, (_, i) => Math.round((start - (perWeek / 7) * i) * 100) / 100);

describe('seven day weight average', () => {
  it('requires four morning measurements', () => {
    const pts = morningWeights([checkin('2026-10-01', 89), checkin('2026-10-02', 88.8), checkin('2026-10-03', 88.9)]);
    const w = sevenDayAverage(pts, '2026-10-07');
    expect(w.count).toBe(3);
    expect(w.reliable).toBe(false);
    const w2 = sevenDayAverage([...pts, { date: '2026-10-05', kg: 88.7 }], '2026-10-07');
    expect(w2.reliable).toBe(true);
    expect(w2.avg).toBeCloseTo(88.85, 2);
  });

  it('ignores weights not taken under morning conditions and keeps the first of the day', () => {
    const pts = morningWeights([checkin('2026-10-01', 89.5, false), { ...checkin('2026-10-02', 89), at: 2 }, { ...checkin('2026-10-02', 90), id: 'b', at: 3 }]);
    expect(pts).toEqual([{ date: '2026-10-02', kg: 89 }]);
  });
});

describe('fourteen day nutrition gate', () => {
  it('refuses to adjust without fourteen days of useful data', () => {
    const r = nutritionAdjustment(input([89, 89, 89, null, null, null, null, 89, 89, 89, 89, 89, 89, 89], [[0, 90], [8, 90]]));
    expect(r.status).toBe('insufficient-data');
    expect(r.kcalChange).toBeNull();
    expect(r.missing.join(' ')).toMatch(/Week one has 3/);
  });

  it('refuses when food logging is sparse', () => {
    const r = nutritionAdjustment(input(flat(89), [[0, 90], [8, 90]], { foodLogDays: ['2026-10-10', '2026-10-11'] }));
    expect(r.status).toBe('insufficient-data');
  });

  it('flags a loss of 0.6 kg a week as too fast for a growing athlete', () => {
    const r = nutritionAdjustment(input(slope(89, 0.6), [[0, 90], [8, 89.4]]));
    expect(r.status).toBe('increase');
    expect(r.kcalChange).toEqual([150, 200]);
  });

  it('holds when loss is 0.25 to 0.5 kg per week', () => {
    const r = nutritionAdjustment(input(slope(89, 0.4), [[0, 90], [8, 89.5]]));
    expect(r.status).toBe('hold');
    expect(r.kcalChange).toBeNull();
  });

  it('labels stable weight with a smaller waist as possible recomposition', () => {
    const r = nutritionAdjustment(input(flat(89), [[0, 90], [8, 89]]));
    expect(r.status).toBe('hold-recomposition');
  });

  it('suggests checking estimates then a small reduction when weight and waist are stable', () => {
    const r = nutritionAdjustment(input(flat(89), [[0, 90], [8, 90]]));
    expect(r.status).toBe('check-then-reduce');
    expect(r.kcalChange).toEqual([-150, -100]);
    expect(r.reasons.join(' ')).toMatch(/portion estimates/);
  });

  it('flags fast loss after the first week and suggests more food with a parent', () => {
    const r = nutritionAdjustment(input(slope(89, 1.0), [[0, 90], [8, 89]]));
    expect(r.status).toBe('increase');
    expect(r.kcalChange).toEqual([150, 200]);
    expect(r.involveGuardian).toBe(true);
  });

  it('adds food when wellbeing declines', () => {
    const r = nutritionAdjustment(
      input(slope(89, 0.4), [[0, 90], [8, 89.6]], { wellbeing: { previous: { energy: 4, mood: 4, concentration: 4, sleepHours: 8.5 }, current: { energy: 2.8, mood: 4, concentration: 4, sleepHours: 8.4 } } }),
    );
    expect(r.status).toBe('increase');
  });

  it('never suggests going below 2,000 calories', () => {
    const r = nutritionAdjustment(input(flat(89), [[0, 90], [8, 90]], { currentKcal: 2080 }));
    expect(r.status).toBe('clinician-review');
    expect(r.kcalChange).toBeNull();
    expect(applyKcalChange(2050, -150)).toBe(NUTRITION_FLOORS.kcal);
    expect(applyKcalChange(2450, -150)).toBe(2300);
  });

  it('asks for a waist measurement before judging stable weight', () => {
    const r = nutritionAdjustment(input(flat(89), []));
    expect(r.status).toBe('insufficient-data');
    expect(r.missing.join(' ')).toMatch(/waist/i);
  });
});

describe('estimate by eye', () => {
  it('stores the method, midpoint, and an honest range', () => {
    const chicken = FOOD_BY_ID['chicken-breast']!;
    const item = itemFromPortion(chicken, 'palm', 2);
    expect(item.estimate.method).toBe('hand');
    expect(item.estimate.confidence).toBe('low');
    expect(item.estimate.gramsMid).toBe(220);
    expect(item.estimate.gramsLow).toBeLessThan(item.estimate.gramsMid);
    expect(item.estimate.gramsHigh).toBeGreaterThan(item.estimate.gramsMid);
    expect(item.low.kcal).toBeLessThan(item.mid.kcal);
    expect(item.high.kcal).toBeGreaterThan(item.mid.kcal);
    // The spread is wide: an eye estimate is not precise.
    expect(item.high.kcal / item.low.kcal).toBeGreaterThan(1.5);
  });

  it('restaurant portions are wider than household measures, which are wider than weighed food', () => {
    const rice = FOOD_BY_ID['rice-cooked']!;
    const spread = (i: ReturnType<typeof itemFromGrams>) => (i.high.kcal - i.low.kcal) / i.mid.kcal;
    const weighed = spread(itemFromGrams(rice, 250, 'weighed'));
    const spoon = spread(itemFromPortion(rice, 'serving-spoon', 5));
    const rest = spread(itemFromPortion(rice, 'restaurant-medium', 1));
    expect(weighed).toBeLessThan(spoon);
    expect(spoon).toBeLessThan(rest);
  });

  it('formats wide ranges coarsely', () => {
    expect(formatRange(412, 688, ' kcal')).toBe('410 to 690 kcal');
    expect(formatRange(1234, 1811)).toBe('1250 to 1800');
  });

  it('logs an approximate day like the one described without false accuracy', () => {
    const items = [
      itemFromPortion(FOOD_BY_ID['egg-white']!, 'serving-spoon', 3),
      itemFromPortion(FOOD_BY_ID['tofu']!, 'palm', 1),
      itemFromPortion(FOOD_BY_ID['salad']!, 'fist', 3),
      itemFromPortion(FOOD_BY_ID['olives']!, 'thumb', 2),
      itemFromGrams(FOOD_BY_ID['chicken-breast']!, 320, 'weighed'),
      itemFromGrams(FOOD_BY_ID['green-beans']!, 250, 'weighed'),
      itemFromGrams(FOOD_BY_ID['rice-cooked']!, 100, 'weighed'),
      itemFromGrams(FOOD_BY_ID['peas']!, 35, 'weighed'),
      itemFromGrams(FOOD_BY_ID['coke-zero']!, 330, 'label'),
    ];
    const t = sumItems(items);
    expect(t.low.kcal).toBeLessThan(t.mid.kcal);
    expect(t.high.kcal).toBeGreaterThan(t.mid.kcal);
    expect(t.mid.protein).toBeGreaterThan(100);
  });
});

describe('meal templates and targets', () => {
  it('has every training day and all slots', () => {
    for (const d of [0, 1, 2, 3, 4, 5] as const) {
      const slots = templatesForDay(d).map((t) => t.slot);
      expect(slots).toEqual(['breakfast', 'lunch', 'preworkout', 'dinner', 'evening']);
    }
    expect(templatesForDay(6)).toHaveLength(0);
  });

  it('seeds the exact default quantities', () => {
    expect(BREAKFAST.items.map((i) => [i.foodId, i.grams])).toEqual([
      ['yogurt-hp', 300],
      ['banana', 118],
      ['oats', 60],
      ['berries-frozen', 100],
      ['protein-powder', 15],
    ]);
    expect(SCHOOL_LUNCH.items.find((i) => i.foodId === 'olive-oil')).toBeUndefined();
    // Since 2.1.1 every day is eaten like the rest day, with 100 g rice before training.
    expect(PREWORKOUT.map((p) => p.items[0]!.grams)).toEqual([100, 100, 100, 100, 100, 100]);
    expect(PREWORKOUT.every((p) => p.items[1]!.grams === 120)).toBe(true);
    expect(DINNERS.map((d) => d.items[0]!.foodId)).toEqual(['salmon', 'beef-lean', 'white-fish', 'salmon', 'beef-lean', 'turkey-breast']);
    expect(DINNERS.map((d) => d.items[1]!.grams)).toEqual([150, 150, 200, 150, 150, 200]);
    expect(DINNERS.map((d) => d.items.find((i) => i.foodId === 'olive-oil')?.grams ?? 0)).toEqual([0, 0, 10, 0, 0, 5]);
    expect(EVENING.items[0]).toMatchObject({ foodId: 'milk', grams: 300 });
  });

  it('keeps targets at or above the safety floors, with every day at the rest day amount', () => {
    for (const t of BASELINE_TARGETS) {
      expect(t.kcalBand[0]).toBeGreaterThanOrEqual(NUTRITION_FLOORS.kcal);
      expect(t.carbs).toBeGreaterThanOrEqual(NUTRITION_FLOORS.carbs);
      expect(t.kcal, t.label).toBe(2250);
      // The macros add up to the calories, within the band.
      const fromMacros = t.protein * 4 + t.carbs * 4 + t.fat * 9;
      expect(Math.abs(fromMacros - t.kcal), t.label).toBeLessThanOrEqual(100);
    }
  });

  it('default meals land near the target on every training day, so a missed workout leaves no extra food', () => {
    for (let wd = 0; wd < 6; wd++) {
      const d = templatesForDay(wd as 0).reduce((a, t) => a + templateTotals(t).mid.kcal, 0);
      expect(d, `weekday ${wd}`).toBeGreaterThan(2150);
      expect(d, `weekday ${wd}`).toBeLessThan(2350);
    }
  });
});

describe('meal preparation scaling', () => {
  it('scales quantities with the number of days and keeps pantry items fixed', () => {
    const yogurt = SHOPPING_LIST.find((s) => s.id === 'yogurt')!;
    expect(scaleShopping(yogurt, 6)).toBe(1800);
    expect(scaleShopping(yogurt, 3)).toBe(900);
    const bananas = SHOPPING_LIST.find((s) => s.id === 'bananas')!;
    expect(scaleShopping(bananas, 4)).toBe(4);
    expect(scaleShopping(SHOPPING_LIST.find((s) => s.id === 'spices')!, 12)).toBe(0);
  });
});
