import { FOOD_BY_ID, type Food, type FoodCategory, type Nutrients } from '../content/foods';
import type { FoodLogItem, PortionEstimate } from '../db/records';

// Estimate by Eye. A visual portion becomes a gram range, never a false exact number.
// The stored record keeps the method, the midpoint, and the uncertainty range.

export type PortionKey =
  | 'palm'
  | 'fist'
  | 'cupped-hand'
  | 'thumb'
  | 'serving-spoon'
  | 'cup'
  | 'restaurant-small'
  | 'restaurant-medium'
  | 'restaurant-large';

export interface PortionDef {
  key: PortionKey;
  label: string;
  hint: string;
  method: 'hand' | 'household' | 'restaurant';
}

export const PORTIONS: PortionDef[] = [
  { key: 'palm', label: 'Palm', hint: 'The size and thickness of your palm, without fingers.', method: 'hand' },
  { key: 'fist', label: 'Fist', hint: 'About the size of your closed fist.', method: 'hand' },
  { key: 'cupped-hand', label: 'Cupped hand', hint: 'What fits in one cupped hand.', method: 'hand' },
  { key: 'thumb', label: 'Thumb', hint: 'About the size of your whole thumb.', method: 'hand' },
  { key: 'serving-spoon', label: 'Serving spoon', hint: 'One heaped serving spoon.', method: 'household' },
  { key: 'cup', label: 'Cup', hint: 'A normal 240 ml cup or mug.', method: 'household' },
  { key: 'restaurant-small', label: 'Small restaurant portion', hint: 'A side dish or a small plate.', method: 'restaurant' },
  { key: 'restaurant-medium', label: 'Medium restaurant portion', hint: 'A normal main portion.', method: 'restaurant' },
  { key: 'restaurant-large', label: 'Large restaurant portion', hint: 'A big plate or a generous serving.', method: 'restaurant' },
];

type Range = [number, number, number]; // low, mid, high grams

// Grams for one portion of a food category: [low, mid, high].
// Hand sizes differ and plates differ, so the ranges are intentionally wide.
const PORTION_GRAMS: Record<PortionKey, Partial<Record<FoodCategory | 'default', Range>>> = {
  palm: { protein: [80, 110, 140], dairy: [80, 110, 140], mixed: [90, 120, 160], default: [80, 110, 140] },
  fist: { carb: [110, 150, 200], vegetable: [60, 85, 110], fruit: [90, 120, 150], mixed: [150, 200, 260], bread: [40, 60, 80], default: [100, 140, 190] },
  'cupped-hand': { carb: [55, 75, 100], vegetable: [30, 45, 60], fruit: [50, 70, 90], fat: [20, 30, 40], sweet: [25, 35, 50], default: [40, 60, 85] },
  thumb: { fat: [6, 10, 15], dairy: [15, 22, 30], sweet: [10, 15, 20], default: [8, 12, 18] },
  'serving-spoon': { carb: [40, 50, 62], protein: [35, 45, 56], vegetable: [30, 40, 52], mixed: [48, 60, 75], fat: [9, 12, 15], default: [35, 45, 58] },
  cup: { drink: [225, 240, 255], dairy: [225, 240, 255], carb: [160, 180, 200], vegetable: [70, 90, 110], fruit: [130, 150, 170], mixed: [210, 240, 270], default: [170, 200, 230] },
  'restaurant-small': { protein: [80, 120, 160], carb: [100, 150, 210], vegetable: [60, 100, 150], mixed: [160, 250, 350], bread: [35, 60, 85], sweet: [45, 70, 105], default: [90, 150, 220] },
  'restaurant-medium': { protein: [120, 180, 250], carb: [170, 250, 350], vegetable: [90, 150, 220], mixed: [280, 400, 550], bread: [60, 90, 130], sweet: [70, 110, 160], default: [160, 250, 360] },
  'restaurant-large': { protein: [180, 260, 350], carb: [250, 350, 480], vegetable: [130, 220, 320], mixed: [400, 550, 750], bread: [90, 130, 180], sweet: [110, 160, 230], default: [240, 350, 500] },
};

export function portionGrams(portion: PortionKey, category: FoodCategory): Range {
  const table = PORTION_GRAMS[portion];
  return table[category] ?? table.default ?? [50, 100, 150];
}

export type EstimateMethod = PortionEstimate['method'];

/** Extra relative uncertainty by method, on top of the food's own label variability. */
export const METHOD_UNCERTAINTY: Record<EstimateMethod, number> = {
  weighed: 0.03,
  label: 0.03,
  template: 0.05,
  household: 0,
  hand: 0,
  restaurant: 0,
  'plate-guide': 0,
};

export function confidenceFor(method: EstimateMethod): PortionEstimate['confidence'] {
  switch (method) {
    case 'weighed':
    case 'label':
    case 'template':
      return 'high';
    case 'household':
      return 'medium';
    case 'hand':
    case 'restaurant':
    case 'plate-guide':
      return 'low';
  }
}

export const CONFIDENCE_LABELS: Record<PortionEstimate['confidence'], string> = {
  high: 'Weighed or label',
  medium: 'Household measure',
  low: 'Estimated by eye',
};

const r2 = (n: number) => Math.round(n * 100) / 100;

export function scaleNutrients(per100: Nutrients, grams: number, factor = 1): Nutrients {
  const k = (grams / 100) * factor;
  const out: Nutrients = {
    kcal: r2(per100.kcal * k),
    protein: r2(per100.protein * k),
    carbs: r2(per100.carbs * k),
    fat: r2(per100.fat * k),
    fibre: r2(per100.fibre * k),
    calcium: r2(per100.calcium * k),
  };
  if (per100.caffeine !== undefined) out.caffeine = r2(per100.caffeine * k);
  return out;
}

export const ZERO: Nutrients = { kcal: 0, protein: 0, carbs: 0, fat: 0, fibre: 0, calcium: 0 };

export function addNutrients(a: Nutrients, b: Nutrients): Nutrients {
  const out: Nutrients = {
    kcal: a.kcal + b.kcal,
    protein: a.protein + b.protein,
    carbs: a.carbs + b.carbs,
    fat: a.fat + b.fat,
    fibre: a.fibre + b.fibre,
    calcium: a.calcium + b.calcium,
  };
  if (a.caffeine !== undefined || b.caffeine !== undefined) out.caffeine = (a.caffeine ?? 0) + (b.caffeine ?? 0);
  return out;
}

/** Build a food log item for a known weight (weighed, label, or template). */
export function itemFromGrams(f: Food, grams: number, method: 'weighed' | 'label' | 'template', substitutedFrom: string | null = null): FoodLogItem {
  const u = METHOD_UNCERTAINTY[method];
  const low = grams * (1 - u);
  const high = grams * (1 + u);
  return {
    foodId: f.id,
    name: f.name,
    estimate: { method, portion: null, count: null, gramsMid: grams, gramsLow: round1(low), gramsHigh: round1(high), confidence: confidenceFor(method) },
    mid: scaleNutrients(f.per100, grams),
    low: scaleNutrients(f.per100, low, 1 - f.variability),
    high: scaleNutrients(f.per100, high, 1 + f.variability),
    substitutedFrom,
  };
}

/** Build a food log item from a visual portion and a count, such as 2 palms. */
export function itemFromPortion(f: Food, portion: PortionKey, count: number, substitutedFrom: string | null = null): FoodLogItem {
  const def = PORTIONS.find((p) => p.key === portion);
  if (!def) throw new Error(`Unknown portion ${portion}`);
  const [lo, mid, hi] = portionGrams(portion, f.category);
  const method: EstimateMethod = def.method;
  const u = METHOD_UNCERTAINTY[method];
  const gLow = lo * count * (1 - u);
  const gMid = mid * count;
  const gHigh = hi * count * (1 + u);
  return {
    foodId: f.id,
    name: f.name,
    estimate: { method, portion, count, gramsMid: round1(gMid), gramsLow: round1(gLow), gramsHigh: round1(gHigh), confidence: confidenceFor(method) },
    mid: scaleNutrients(f.per100, gMid),
    low: scaleNutrients(f.per100, gLow, 1 - f.variability),
    high: scaleNutrients(f.per100, gHigh, 1 + f.variability),
    substitutedFrom,
  };
}

/** A plate guide item with its own gram range, used for Sabbath meals. */
export function itemFromRange(f: Food, grams: Range, name?: string): FoodLogItem {
  return {
    foodId: f.id,
    name: name ?? f.name,
    estimate: { method: 'plate-guide', portion: null, count: null, gramsMid: grams[1], gramsLow: grams[0], gramsHigh: grams[2], confidence: 'low' },
    mid: scaleNutrients(f.per100, grams[1]),
    low: scaleNutrients(f.per100, grams[0], 1 - f.variability),
    high: scaleNutrients(f.per100, grams[2], 1 + f.variability),
    substitutedFrom: null,
  };
}

export function hiddenOilItem(range: Range): FoodLogItem {
  const oil = FOOD_BY_ID['olive-oil']!;
  return { ...itemFromRange(oil, range, 'Cooking oil you cannot see (allowance)'), foodId: 'olive-oil' };
}

export interface Totals {
  mid: Nutrients;
  low: Nutrients;
  high: Nutrients;
}

/**
 * Sum items. Midpoints add up. Errors of different foods are treated as independent, so the
 * spread combines as the root of the summed squares instead of stacking every worst case.
 * A single item keeps its own full range.
 */
export function sumItems(items: FoodLogItem[]): Totals {
  const mid = items.reduce<Nutrients>((a, it) => addNutrients(a, it.mid), ZERO);
  const keys = ['kcal', 'protein', 'carbs', 'fat', 'fibre', 'calcium'] as const;
  const low = { ...mid };
  const high = { ...mid };
  for (const k of keys) {
    const down = Math.sqrt(items.reduce((a, it) => a + (it.mid[k] - it.low[k]) ** 2, 0));
    const up = Math.sqrt(items.reduce((a, it) => a + (it.high[k] - it.mid[k]) ** 2, 0));
    low[k] = Math.max(0, mid[k] - down);
    high[k] = mid[k] + up;
  }
  return { mid, low, high };
}

const round1 = (n: number) => Math.round(n * 10) / 10;

/** Display a range honestly: wide ranges are rounded more coarsely. */
export function formatRange(low: number, high: number, unit = ''): string {
  const span = high - low;
  const step = span > 400 ? 50 : span > 100 ? 10 : span > 20 ? 5 : 1;
  const lo = Math.round(low / step) * step;
  const hi = Math.round(high / step) * step;
  if (lo === hi) return `${lo}${unit}`;
  return `${lo} to ${hi}${unit}`;
}
