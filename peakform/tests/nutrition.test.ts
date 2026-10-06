import { describe, expect, it } from 'vitest';
import { AFTERNOON, ALL_TEMPLATES, BREAKFAST, DINNERS, EVENING, EVENING_PAREVE, EXAMPLE_CONTEXT, EXAMPLE_NOTE, SCHOOL_LUNCH, templateKosher, templatesForDay } from '../src/content/meals';
import { FOOD_BY_ID, FOODS, YIELDS, cookedWeight, rawWeightFor } from '../src/content/foods';
import { RECIPE_BY_ID, SHOPPING_LIST, scaleShopping } from '../src/content/recipes';
import { addDays, rangeKeys } from '../src/domain/dates';
import { STABLE_WEIGHT_NOTE, exampleDayTotals, morningWeights, nutritionAdjustment, sevenDayAverage, templateTotals, weeklyWeights, type AdjustmentInput } from '../src/domain/nutrition';
import { recipeNutrition, scaledGrams } from '../src/domain/recipeMath';
import { dairyFrom, meatDairyNotes } from '../src/domain/kosher';
import { vegEstimate } from '../src/screens/Athlete';
import type { FoodLog } from '../src/db/records';
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

  it('mentions sparse food logs without blocking the trend, because logging is optional', () => {
    const r = nutritionAdjustment(input(flat(89), [[0, 90], [8, 90]], { foodLogDays: ['2026-10-10', '2026-10-11'] }));
    expect(r.status).toBe('no-change');
    expect(r.reasons.join(' ')).toMatch(/Logging is optional/);
  });

  it('flags a loss of 0.6 kg a week as too fast for a growing athlete and suggests more food', () => {
    const r = nutritionAdjustment(input(slope(89, 0.6), [[0, 90], [8, 89.4]]));
    expect(r.status).toBe('eat-more');
    expect(r.kcalChange).toEqual([150, 250]);
    expect(r.involveGuardian).toBe(true);
  });

  it('suggests no change for a gradual loss', () => {
    const r = nutritionAdjustment(input(slope(89, 0.3), [[0, 90], [8, 89.5]]));
    expect(r.status).toBe('no-change');
    expect(r.kcalChange).toBeNull();
  });

  it('never cuts food when weight and waist are stable for two weeks, and does not call it a plateau', () => {
    const r = nutritionAdjustment(input(flat(89), [[0, 90], [8, 90]]));
    expect(r.status).toBe('no-change');
    expect(r.kcalChange).toBeNull();
    const text = [r.title, ...r.reasons].join(' ');
    expect(text).not.toMatch(/fewer calories|eat less|reduc|smaller portion/i);
    expect(text).toContain(STABLE_WEIGHT_NOTE);
    expect(STABLE_WEIGHT_NOTE).toMatch(/not a plateau/);
    expect(STABLE_WEIGHT_NOTE).toMatch(/does not show whether you eat enough/);
  });

  it('never suggests eating less, whatever the trend', () => {
    for (const w of [flat(89), slope(88, -0.5), slope(89, 0.2), slope(89, 1.2)]) {
      const r = nutritionAdjustment(input(w, [[0, 90], [8, 90]]));
      if (r.kcalChange) expect(r.kcalChange[0]).toBeGreaterThan(0);
    }
  });

  it('treats five days of stable or slightly higher weight as not enough data, with no restriction', () => {
    const today = '2026-10-06';
    const days = rangeKeys(addDays(today, -4), 5);
    const r = nutritionAdjustment({ ...input([], []), today, planStart: addDays(today, -40), checkins: days.map((d, i) => checkin(d, 88 + i * 0.03)), foodLogDays: days });
    expect(r.status).toBe('insufficient-data');
    expect(r.kcalChange).toBeNull();
    expect(r.missing.length).toBeGreaterThan(0);
  });

  it('says what is missing when data are sparse', () => {
    const r = nutritionAdjustment(input([89, null, null, null, null, null, null, null, null, null, null, null, null, 89], []));
    expect(r.status).toBe('insufficient-data');
    expect(r.missing.join(' ')).toMatch(/Week one has 1/);
  });

  it('a slide in energy, mood, or sleep means eating a bit more and a parent, even with stable weight', () => {
    const r = nutritionAdjustment(
      input(flat(89), [[0, 90], [8, 90]], { wellbeing: { previous: { energy: 4, mood: 4, concentration: 4, sleepHours: 8.5 }, current: { energy: 2.8, mood: 4, concentration: 4, sleepHours: 8.4 } } }),
    );
    expect(r.status).toBe('talk-to-parent');
    expect(r.involveGuardian).toBe(true);
    expect(r.kcalChange?.[0]).toBeGreaterThan(0);
    expect(r.reasons.join(' ')).toMatch(/does not show whether you eat enough/);
  });

  it('works with weekly weighing and with weighing switched off', () => {
    const today = '2026-10-28';
    const pts = [0, 7, 14, 21].map((d) => checkin(addDays(today, -d), 89));
    const weekly = nutritionAdjustment({ ...input([], []), today, checkins: pts, weightMode: 'weekly' });
    expect(weekly.status).toBe('no-change');
    expect(weeklyWeights(morningWeights(pts), today, 4).filter((w) => w.kg !== null)).toHaveLength(4);
    const off = nutritionAdjustment({ ...input(flat(89), []), weightMode: 'off' });
    expect(off.status).toBe('insufficient-data');
    expect(off.kcalChange).toBeNull();
  });

  it('never reads smart scale body fat', () => {
    const base = input(flat(89), [[0, 90], [8, 90]]);
    const withFat = { ...base, checkins: base.checkins.map((c, i) => ({ ...c, bodyFatPct: 30 - i })) };
    expect(nutritionAdjustment(withFat)).toEqual(nutritionAdjustment(base));
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

describe('example meals in grams', () => {
  it('covers every school day and keeps the same meals on training days and days off', () => {
    for (const wd of [0, 1, 2, 3, 4, 5] as const) {
      const slots = templatesForDay(wd).map((t) => t.slot);
      for (const slot of ['breakfast', 'snack', 'lunch', 'preworkout', 'dinner'] as const) expect(slots).toContain(slot);
    }
    // Tuesday has no training and still gets the same afternoon meal as a gym day.
    expect(templatesForDay(2).find((t) => t.slot === 'preworkout')).toBe(templatesForDay(1).find((t) => t.slot === 'preworkout'));
  });

  it('labels every quantity as an example with a household measure, more food options, swaps, and storage', () => {
    expect(EXAMPLE_NOTE).toBe('Example serving. Adjust to appetite and activity; this is not a daily limit.');
    for (const t of ALL_TEMPLATES) {
      expect(t.more.length, t.id).toBeGreaterThan(0);
      expect(t.substitutions.length, t.id).toBeGreaterThan(0);
      expect(t.storage.length, t.id).toBeGreaterThan(0);
      for (const i of t.items) {
        expect(FOOD_BY_ID[i.foodId], `${t.id} ${i.foodId}`).toBeDefined();
        expect(i.household, `${t.id} ${i.foodId}`).toBeTruthy();
      }
    }
  });

  it('seeds the documented example quantities', () => {
    expect(BREAKFAST.items.map((i) => [i.foodId, i.grams])).toEqual([['yogurt-hp', 300], ['oats', 80], ['banana', 118], ['berries-frozen', 100]]);
    // No supplement is suggested in the examples: protein comes from food.
    expect(ALL_TEMPLATES.flatMap((t) => t.items).some((i) => i.foodId === 'protein-powder')).toBe(false);
    expect(SCHOOL_LUNCH.items.map((i) => i.grams)).toEqual([100, 66, 135, 300, 30]);
    expect(AFTERNOON.items.map((i) => [i.foodId, i.grams])).toEqual([['rice-cooked', 200], ['chicken-breast', 120]]);
    for (const d of DINNERS) expect(d.items.find((i) => i.foodId === 'potato')?.grams).toBe(250);
    expect(DINNERS).toHaveLength(6);
    for (const d of DINNERS) expect(d.items.find((i) => i.foodId === 'olive-oil')?.grams).toBe(5);
    expect(EVENING.items[0]).toMatchObject({ foodId: 'milk', grams: 300 });
  });

  it('never mixes meat and dairy in one example meal', () => {
    for (const t of ALL_TEMPLATES) {
      const cats = new Set(t.items.map((i) => FOOD_BY_ID[i.foodId]!.kosher));
      expect(cats.has('meat') && cats.has('dairy'), t.id).toBe(false);
    }
    expect(templateKosher(BREAKFAST)).toBe('dairy');
    expect(templateKosher(AFTERNOON)).toBe('meat');
    expect(templateKosher(SCHOOL_LUNCH)).toBe('pareve');
    expect(templateKosher(EVENING_PAREVE)).toBe('pareve');
  });

  it('swaps the evening milk for a pareve snack when it would come too soon after meat', () => {
    // Monday dinner is beef at 19:00, so 20:45 milk is too soon with a 3 hour interval.
    expect(templatesForDay(1, undefined, { meatToDairyHours: 3 }).find((t) => t.slot === 'evening')?.id).toBe('evening-pareve');
    // Sunday dinner is salmon, so with 3 hours milk fits 5 h 25 min after the chicken at 15:20.
    expect(templatesForDay(0, undefined, { meatToDairyHours: 3 }).find((t) => t.slot === 'evening')?.id).toBe('evening-milk');
    // With the default of 6 hours, the chicken at 15:20 is too close as well.
    expect(templatesForDay(0).find((t) => t.slot === 'evening')?.id).toBe('evening-pareve');
    expect(templatesForDay(0, undefined, { meatToDairyHours: 6 }).find((t) => t.slot === 'evening')?.id).toBe('evening-pareve');
    // Switched off, the milk stays.
    expect(templatesForDay(1, undefined, { meatToDairyHours: null }).find((t) => t.slot === 'evening')?.id).toBe('evening-milk');
    // Times the athlete set count: a later snack at 22:30 fits after a 19:00 meat dinner.
    expect(templatesForDay(1, undefined, { meatToDairyHours: 3, times: { evening: '22:30' } }).find((t) => t.slot === 'evening')?.id).toBe('evening-milk');
  });

  it('notes dairy logged too soon after meat, without blocking it', () => {
    const log = (id: string, time: string, foodId: string): FoodLog => {
      const f = FOOD_BY_ID[foodId]!;
      const item = itemFromGrams(f, 100, 'template');
      return { id, createdAt: 0, updatedAt: 0, date: '2026-10-05', slot: 'other', time, source: 'manual', templateId: null, asPlanned: false, items: [item], photoId: null, note: '', hiddenOil: null };
    };
    const logs = [log('a', '19:00', 'beef-lean'), log('b', '20:30', 'milk'), log('c', '23:00', 'yogurt-hp')];
    const notes = meatDairyNotes(logs, 3);
    expect(notes.map((n) => n.logId)).toEqual(['b']);
    expect(notes[0]!.text).toMatch(/1 h 30 min/);
    expect(meatDairyNotes(logs, null)).toEqual([]);
    expect(dairyFrom(logs, 3)).toBe('22:00');
    expect(dairyFrom([log('x', '08:00', 'banana')], 3)).toBeNull();
  });

  it('gives no food for finishing a workout: a gym day and a day off have the same examples', () => {
    // Wednesday (gym) and Tuesday (no training) differ only by the dinner fish, never by training.
    const ids = (wd: 2 | 3) => templatesForDay(wd).filter((t) => t.slot !== 'dinner').map((t) => t.id);
    expect(ids(2)).toEqual(ids(3));
  });

  it('describes the sum of the examples without turning it into a target, and says teens often need more', () => {
    const t = exampleDayTotals(templatesForDay(1));
    expect(t.mid.kcal).toBeGreaterThan(2600);
    expect(t.mid.kcal).toBeLessThan(3200);
    expect(t.mid.protein).toBeGreaterThan(120);
    expect(EXAMPLE_CONTEXT).toMatch(/often need more than these examples/);
  });
});

describe('raw, dry, cooked, and drained weights', () => {
  it('has separate entries with clear states', () => {
    expect(FOOD_BY_ID['rice-dry']!.state).toBe('dry');
    expect(FOOD_BY_ID['rice-cooked']!.state).toBe('cooked');
    expect(FOOD_BY_ID['chicken-raw']!.state).toBe('raw');
    expect(FOOD_BY_ID['green-beans-raw']!.state).toBe('raw');
    expect(FOOD_BY_ID['green-beans-canned']!.state).toBe('drained');
    expect(FOOD_BY_ID['egg']!.state).toBe('raw');
    for (const f of FOODS) expect(['meat', 'dairy', 'pareve']).toContain(f.kosher);
  });

  it('converts between raw and cooked weights with a range, consistent with the energy values', () => {
    expect(cookedWeight('rice-dry', 100)).toEqual({ toId: 'rice-cooked', mid: 270, low: 250, high: 300 });
    expect(rawWeightFor('rice-cooked', 1200)!.mid).toBe(444);
    expect(cookedWeight('chicken-raw', 1000)!.mid).toBe(720);
    expect(cookedWeight('banana', 100)).toBeNull();
    // Cooking changes water, not energy: dry and cooked energy match within about 10 percent.
    for (const y of YIELDS) {
      const raw = FOOD_BY_ID[y.from]!.per100.kcal;
      const cooked = FOOD_BY_ID[y.to]!.per100.kcal * y.factor;
      expect(Math.abs(cooked - raw) / raw, y.from).toBeLessThan(0.1);
    }
  });

  it('logs 100 g of dry rice as about 2.8 times the energy of 100 g cooked', () => {
    const dry = itemFromGrams(FOOD_BY_ID['rice-dry']!, 100, 'weighed');
    const cooked = itemFromGrams(FOOD_BY_ID['rice-cooked']!, 100, 'weighed');
    expect(dry.mid.kcal / cooked.mid.kcal).toBeCloseTo(2.81, 1);
  });

  it('calculates the daily green beans for each state with the arithmetic', () => {
    const base = { grams: 750, role: 'added', oilG: null, sauce: '', stomach: 'fine', weighed: 'weighed' } as const;
    expect(vegEstimate({ ...base, state: 'raw' })!.kcal).toBe(233);
    expect(vegEstimate({ ...base, state: 'boiled-drained' })!.kcal).toBe(263);
    expect(vegEstimate({ ...base, state: 'frozen-cooked' })!.kcal).toBe(210);
    expect(vegEstimate({ ...base, state: 'canned-drained' })!.kcal).toBe(165);
    const oiled = vegEstimate({ ...base, state: 'boiled-drained', oilG: 10 })!;
    expect(oiled.kcal).toBe(263 + 88);
    expect(oiled.lines.join(' ')).toMatch(/10 g oil × 8.84/);
    expect(vegEstimate({ ...base, state: 'unknown' })).toBeNull();
  });
});

describe('recipes', () => {
  it('scales ingredient grams with the servings', () => {
    const r = RECIPE_BY_ID['chicken-rice-boxes']!;
    const rice = r.ingredients.find((i) => i.foodId === 'rice-cooked')!;
    expect(scaledGrams(r, rice, 6)).toBe(1200);
    expect(scaledGrams(r, rice, 3)).toBe(600);
    expect(scaledGrams(r, { name: 'Spices' }, 3)).toBeNull();
  });

  it('adds up nutrition from the ingredients, per serving and in total', () => {
    const r = RECIPE_BY_ID['chicken-rice-boxes']!;
    const one = recipeNutrition(r, 1);
    const six = recipeNutrition(r, 6);
    expect(six.mid.kcal).toBeCloseTo(one.mid.kcal * 6, 0);
    // One box: 120 g chicken (198 kcal) and 200 g rice (260 kcal).
    expect(Math.round(one.mid.kcal)).toBe(458);
    expect(one).toEqual(templateTotals(AFTERNOON));
  });

  it('counts the oil in a recipe', () => {
    const r = RECIPE_BY_ID['white-fish-plate']!;
    const withOil = recipeNutrition(r, 1).mid.kcal;
    const without = recipeNutrition({ ...r, ingredients: r.ingredients.filter((i) => i.foodId !== 'olive-oil') }, 1).mid.kcal;
    expect(withOil - without).toBeCloseTo(44.2, 0);
  });
});

describe('meal preparation scaling', () => {
  it('scales quantities with the number of days and keeps pantry items fixed', () => {
    const yogurt = SHOPPING_LIST.find((s) => s.id === 'yogurt')!;
    expect(scaleShopping(yogurt, 6)).toBe(1800);
    expect(scaleShopping(SHOPPING_LIST.find((x) => x.id === 'rice')!, 6)).toBe(450);
    expect(scaleShopping(yogurt, 3)).toBe(900);
    const bananas = SHOPPING_LIST.find((s) => s.id === 'bananas')!;
    expect(scaleShopping(bananas, 4)).toBe(4);
    expect(scaleShopping(SHOPPING_LIST.find((s) => s.id === 'spices')!, 12)).toBe(0);
  });
});
