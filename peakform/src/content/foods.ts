// Built in food values per 100 g (or per 100 ml for drinks).
// Values follow USDA FoodData Central (SR Legacy) entries for the state named, or a typical label
// for branded foods. The FDC pages could not be opened from the build environment, so values were
// checked against search results and the USDA SR28 data file (NUTRITION_DATA_AUDIT.md). Real labels
// and recipes differ, so every food carries a variability percentage that widens the displayed range.

export interface Nutrients {
  kcal: number;
  protein: number;
  carbs: number;
  fat: number;
  fibre: number;
  /** Calcium in mg. */
  calcium: number;
  /** Caffeine in mg, for drinks that contain it. */
  caffeine?: number;
}

export type FoodCategory =
  | 'protein'
  | 'dairy'
  | 'carb'
  | 'fruit'
  | 'vegetable'
  | 'fat'
  | 'drink'
  | 'mixed'
  | 'sweet'
  | 'bread';

export interface Food {
  id: string;
  name: string;
  category: FoodCategory;
  /** State the values refer to. */
  state: 'cooked' | 'raw' | 'dry' | 'as sold' | 'prepared' | 'frozen' | 'drained';
  /** Meat, dairy, or neither (pareve), for the meat and dairy interval. Certification is always checked on the product. */
  kosher: 'meat' | 'dairy' | 'pareve';
  /** Where the values come from. */
  source?: string;
  per100: Nutrients;
  /** Typical label or recipe variability, as a fraction (0.1 = plus or minus 10 percent). */
  variability: number;
  /** Named units such as one egg or one banana, in grams. */
  units?: Array<{ label: string; grams: number }>;
  /** Liquid measured in millilitres; grams equal millilitres for these entries. */
  liquid?: boolean;
  note?: string;
}

const n = (kcal: number, protein: number, carbs: number, fat: number, fibre: number, calcium: number, caffeine?: number): Nutrients =>
  caffeine === undefined ? { kcal, protein, carbs, fat, fibre, calcium } : { kcal, protein, carbs, fat, fibre, calcium, caffeine };

export const FOODS: Food[] = [
  // Breakfast
  { id: 'yogurt-hp', name: 'High protein yogurt or skyr, 0 to 3% fat', kosher: 'dairy', category: 'dairy', state: 'as sold', per100: n(68, 10.5, 4.0, 1.2, 0, 120), variability: 0.15, units: [{ label: 'tub (200 g)', grams: 200 }], note: 'Brands vary. Check the label for protein per 100 g.' },
  { id: 'banana', name: 'Banana', kosher: 'pareve', category: 'fruit', state: 'raw', per100: n(89, 1.1, 22.8, 0.3, 2.6, 5), variability: 0.1, units: [{ label: 'medium banana', grams: 118 }, { label: 'small banana', grams: 100 }, { label: 'large banana', grams: 136 }] },
  { id: 'oats', name: 'Rolled oats', kosher: 'pareve', category: 'carb', state: 'dry', per100: n(379, 13.2, 67.7, 6.5, 10.1, 52), variability: 0.05 },
  { id: 'berries-frozen', name: 'Frozen mixed berries', kosher: 'pareve', category: 'fruit', state: 'frozen', per100: n(50, 0.8, 11.5, 0.3, 3.5, 15), variability: 0.15 },
  { id: 'protein-powder', name: 'Whey protein powder', kosher: 'dairy', category: 'protein', state: 'as sold', per100: n(390, 78, 8, 5, 0, 400), variability: 0.1, units: [{ label: 'scoop (30 g)', grams: 30 }, { label: 'half scoop (15 g)', grams: 15 }], note: 'Prefer a third party tested product, reviewed with a parent.' },

  // School lunch
  { id: 'egg', name: 'Egg, whole', kosher: 'pareve', category: 'protein', state: 'raw', per100: n(143, 12.6, 0.7, 9.5, 0, 56), variability: 0.1, units: [{ label: 'large egg', grams: 50 }], source: 'USDA FDC 171287, egg, whole, raw', note: 'A boiled egg weighs about the same as a raw one, and its values are within about 10 percent.' },
  { id: 'egg-white', name: 'Egg white', kosher: 'pareve', category: 'protein', state: 'raw', per100: n(52, 10.9, 0.7, 0.2, 0, 7), variability: 0.1, units: [{ label: 'egg white', grams: 33 }], source: 'USDA FDC 172183, egg, white, raw' },
  { id: 'tofu', name: 'Tofu, firm', kosher: 'pareve', category: 'protein', state: 'as sold', per100: n(144, 17.3, 2.8, 8.7, 2.3, 350), variability: 0.3, source: 'USDA FDC 172475, tofu, firm, for the macros', note: 'Calcium varies a lot: tofu made with calcium sulfate has about 680 mg per 100 g, tofu made with nigari much less. 350 mg is a middle value. Check the label.' },
  { id: 'salad', name: 'Salad vegetables, no dressing', kosher: 'pareve', category: 'vegetable', state: 'raw', per100: n(20, 0.9, 4.0, 0.2, 1.3, 15), variability: 0.2, note: 'Cucumber, tomato, cherry tomato, onion, peppers, leaves.' },
  { id: 'olives', name: 'Olives', kosher: 'pareve', category: 'fat', state: 'as sold', per100: n(130, 1.0, 5.0, 13.0, 3.0, 60), variability: 0.15, units: [{ label: 'olive', grams: 4 }] },

  // Carbohydrates
  { id: 'rice-cooked', name: 'White rice, cooked', kosher: 'pareve', category: 'carb', state: 'cooked', per100: n(130, 2.7, 28.2, 0.3, 0.4, 10), variability: 0.1, source: 'USDA FDC 168878, rice, white, long grain, cooked', note: 'About 100 g dry rice makes about 270 g cooked, depending on the water.' },
  { id: 'rice-dry', name: 'White rice, dry (uncooked)', kosher: 'pareve', category: 'carb', state: 'dry', per100: n(365, 7.1, 80.0, 0.7, 1.3, 28), variability: 0.05, source: 'USDA FDC 168877, rice, white, long grain, raw', note: 'Weigh before cooking. 100 g dry makes about 270 g cooked.' },
  { id: 'potato', name: 'Potato, boiled, no oil', kosher: 'pareve', category: 'carb', state: 'cooked', per100: n(87, 1.9, 20.1, 0.1, 1.8, 5), variability: 0.1, source: 'USDA SR 11365, potato, boiled in skin', note: 'Roasted or baked potatoes lose water, so 100 g of them holds a little more energy.' },
  { id: 'potato-raw', name: 'Potato, raw', kosher: 'pareve', category: 'carb', state: 'raw', per100: n(77, 2.0, 17.5, 0.1, 2.1, 12), variability: 0.1, source: 'USDA FDC 170026, potato, flesh and skin, raw' },
  { id: 'sweet-potato', name: 'Sweet potato, baked', kosher: 'pareve', category: 'carb', state: 'cooked', per100: n(90, 2.0, 20.7, 0.2, 3.3, 38), variability: 0.1 },
  { id: 'pasta-cooked', name: 'Pasta', kosher: 'pareve', category: 'carb', state: 'cooked', per100: n(158, 5.8, 30.9, 0.9, 1.8, 7), variability: 0.1 },
  { id: 'couscous-cooked', name: 'Couscous', kosher: 'pareve', category: 'carb', state: 'cooked', per100: n(112, 3.8, 23.2, 0.2, 1.4, 8), variability: 0.1 },
  { id: 'quinoa-cooked', name: 'Quinoa', kosher: 'pareve', category: 'carb', state: 'cooked', per100: n(120, 4.4, 21.3, 1.9, 2.8, 17), variability: 0.1 },
  { id: 'bread-wholewheat', name: 'Whole wheat bread', kosher: 'pareve', category: 'bread', state: 'as sold', per100: n(250, 12.0, 43.0, 3.5, 7.0, 100), variability: 0.15, units: [{ label: 'slice', grams: 35 }] },
  { id: 'challah', name: 'Challah', kosher: 'pareve', category: 'bread', state: 'as sold', per100: n(290, 8.5, 50.0, 6.0, 2.0, 60), variability: 0.2, units: [{ label: 'slice', grams: 40 }] },
  { id: 'lentils-cooked', name: 'Lentils, cooked', kosher: 'pareve', category: 'carb', state: 'cooked', per100: n(116, 9.0, 20.1, 0.4, 7.9, 19), variability: 0.1, source: 'USDA SR 16070, lentils, boiled, without salt', note: 'About 100 g dry lentils makes about 300 g cooked.' },
  { id: 'lentils-dry', name: 'Lentils, dry (uncooked)', kosher: 'pareve', category: 'carb', state: 'dry', per100: n(352, 24.6, 63.4, 1.1, 10.7, 35), variability: 0.05, source: 'USDA FDC 172420, lentils, raw' },
  { id: 'chickpeas-cooked', name: 'Chickpeas', kosher: 'pareve', category: 'carb', state: 'cooked', per100: n(164, 8.9, 27.4, 2.6, 7.6, 49), variability: 0.1 },

  // Proteins
  { id: 'chicken-breast', name: 'Chicken breast, skinless, cooked', kosher: 'meat', category: 'protein', state: 'cooked', per100: n(165, 31.0, 0, 3.6, 0, 15), variability: 0.1, source: 'USDA FDC 171477, chicken breast, meat only, roasted', note: 'Raw chicken loses about 25 to 30 percent of its weight when cooked.' },
  { id: 'chicken-raw', name: 'Chicken breast, skinless, raw', kosher: 'meat', category: 'protein', state: 'raw', per100: n(120, 22.5, 0, 2.6, 0, 5), variability: 0.1, source: 'USDA FDC 171077, chicken breast, meat only, raw', note: 'Weigh before cooking. 100 g raw cooks down to about 72 g.' },
  { id: 'salmon', name: 'Salmon', kosher: 'pareve', category: 'protein', state: 'cooked', per100: n(206, 22.1, 0, 12.4, 0, 15), variability: 0.15 },
  { id: 'beef-lean', name: 'Lean beef, about 90% lean', kosher: 'meat', category: 'protein', state: 'cooked', per100: n(200, 27.0, 0, 10.0, 0, 15), variability: 0.2, note: 'Fat content changes calories a lot. Check the cut or label.' },
  { id: 'white-fish', name: 'White fish (cod, hake, tilapia)', kosher: 'pareve', category: 'protein', state: 'cooked', per100: n(105, 23.0, 0, 1.2, 0, 15), variability: 0.1 },
  { id: 'turkey-breast', name: 'Turkey breast, skinless', kosher: 'meat', category: 'protein', state: 'cooked', per100: n(147, 30.0, 0, 2.1, 0, 12), variability: 0.1 },
  { id: 'tuna-water', name: 'Tuna in water, drained', kosher: 'pareve', category: 'protein', state: 'drained', per100: n(116, 25.5, 0, 0.8, 0, 11), variability: 0.15, source: 'USDA FDC 171986, light tuna in water, drained', note: 'Another USDA entry gives about 86 kcal per 100 g. Brands differ, so check the label.' },
  { id: 'cottage-cheese', name: 'Cottage cheese, 5%', kosher: 'dairy', category: 'dairy', state: 'as sold', per100: n(95, 11.0, 1.5, 5.0, 0, 90), variability: 0.1 },

  // Vegetables
  { id: 'veg-mixed', name: 'Non starchy vegetables, cooked', kosher: 'pareve', category: 'vegetable', state: 'cooked', per100: n(35, 2.0, 7.0, 0.3, 3.0, 35), variability: 0.2, note: 'Broccoli, zucchini, cauliflower, peppers, green beans. A frozen mix with corn, peas, and carrots has about 65 kcal per 100 g.' },
  { id: 'green-beans', name: 'Green beans, boiled and drained', kosher: 'pareve', category: 'vegetable', state: 'cooked', per100: n(35, 1.9, 7.9, 0.3, 3.2, 44), variability: 0.1, source: 'USDA SR 11053, snap beans, green, boiled, drained, without salt', note: 'Fresh beans weighed after cooking and draining.' },
  { id: 'green-beans-raw', name: 'Green beans, raw', kosher: 'pareve', category: 'vegetable', state: 'raw', per100: n(31, 1.8, 7.0, 0.2, 2.7, 37), variability: 0.1, source: 'USDA FDC 169961, snap beans, green, raw', note: 'Weighed raw, after trimming the ends.' },
  { id: 'green-beans-frozen', name: 'Green beans, frozen, cooked and drained', kosher: 'pareve', category: 'vegetable', state: 'cooked', per100: n(28, 1.5, 6.5, 0.2, 3.0, 40), variability: 0.15, source: 'USDA FDC 169963, snap beans, green, frozen, boiled, drained', note: 'Calcium is approximate.' },
  { id: 'green-beans-canned', name: 'Green beans, canned, drained', kosher: 'pareve', category: 'vegetable', state: 'drained', per100: n(22, 1.1, 4.3, 0.5, 1.9, 26), variability: 0.15, source: 'USDA FDC 169143, snap beans, green, canned, drained solids', note: 'Regular canned beans hold about 230 mg sodium per 100 g. No salt added cans hold almost none. Calcium is approximate.' },
  { id: 'peas', name: 'Peas', kosher: 'pareve', category: 'vegetable', state: 'cooked', per100: n(84, 5.4, 15.6, 0.2, 5.5, 27), variability: 0.1 },
  { id: 'lentil-soup', name: 'Lentil soup (PeakForm recipe)', kosher: 'pareve', category: 'mixed', state: 'prepared', per100: n(44, 2.5, 7.3, 0.5, 1.5, 10), variability: 0.2, units: [{ label: 'serving (about 450 g)', grams: 450 }], note: 'One sixth of the built in pot recipe, about 2.7 kg in total.' },

  // Fats
  { id: 'olive-oil', name: 'Olive oil', kosher: 'pareve', category: 'fat', state: 'as sold', per100: n(884, 0, 0, 100, 0, 1), variability: 0.02, source: 'USDA SR 04053, olive oil', units: [{ label: 'teaspoon', grams: 4.5 }, { label: 'tablespoon', grams: 13.5 }] },
  { id: 'tahini', name: 'Tahini sauce, prepared', kosher: 'pareve', category: 'fat', state: 'prepared', per100: n(290, 8.0, 10.0, 25.0, 4.0, 150), variability: 0.3, units: [{ label: 'tablespoon', grams: 15 }], note: 'Raw tahini mixed with about the same amount of water and lemon. Not verified against a reference entry.' },
  { id: 'tahini-raw', name: 'Tahini, raw paste', kosher: 'pareve', category: 'fat', state: 'as sold', per100: n(595, 17.0, 21.2, 53.8, 9.3, 426), variability: 0.1, units: [{ label: 'tablespoon', grams: 15 }], source: 'USDA FDC 170189, sesame butter, tahini' },
  { id: 'almonds', name: 'Almonds', kosher: 'pareve', category: 'fat', state: 'as sold', per100: n(579, 21.2, 21.6, 49.9, 12.5, 269), variability: 0.05, units: [{ label: 'small handful (20 g)', grams: 20 }], source: 'USDA FDC 170567, almonds' },
  { id: 'apple', name: 'Apple', kosher: 'pareve', category: 'fruit', state: 'raw', per100: n(52, 0.3, 13.8, 0.2, 2.4, 6), variability: 0.1, units: [{ label: 'medium apple', grams: 180 }], source: 'USDA FDC 171688, apples, raw, with skin' },

  // Drinks
  { id: 'milk', name: 'Milk, 2%', kosher: 'dairy', category: 'dairy', state: 'as sold', liquid: true, per100: n(50, 3.3, 4.8, 2.0, 0, 120), variability: 0.1, units: [{ label: 'glass (250 ml)', grams: 250 }] },
  { id: 'coke-zero', name: 'Coke Zero', kosher: 'pareve', category: 'drink', state: 'as sold', liquid: true, per100: n(0.3, 0, 0, 0, 0, 0, 9.6), variability: 0, units: [{ label: 'can (330 ml)', grams: 330 }, { label: 'bottle (500 ml)', grams: 500 }] },
  { id: 'zero-drink', name: 'Zero calorie drink', kosher: 'pareve', category: 'drink', state: 'as sold', liquid: true, per100: n(0, 0, 0, 0, 0, 0), variability: 0, units: [{ label: 'glass (250 ml)', grams: 250 }] },
  { id: 'water', name: 'Water', kosher: 'pareve', category: 'drink', state: 'as sold', liquid: true, per100: n(0, 0, 0, 0, 0, 0), variability: 0, units: [{ label: 'glass (250 ml)', grams: 250 }, { label: 'bottle (500 ml)', grams: 500 }] },

  // Common hosted and restaurant foods
  { id: 'sweet-portion', name: 'Sweet portion (cake, cookies, dessert)', kosher: 'pareve', note: 'After a kosher meat meal, dessert is pareve. Values are a rough average.', category: 'sweet', state: 'prepared', per100: n(400, 5.0, 55.0, 18.0, 1.5, 50), variability: 0.3, units: [{ label: 'normal portion (70 g)', grams: 70 }] },
  { id: 'hummus', name: 'Hummus', kosher: 'pareve', category: 'mixed', state: 'prepared', per100: n(240, 7.0, 14.0, 17.0, 6.0, 40), variability: 0.3 },
  { id: 'pita', name: 'Pita bread', kosher: 'pareve', category: 'bread', state: 'as sold', per100: n(275, 9.1, 55.7, 1.2, 2.2, 86), variability: 0.15, units: [{ label: 'pita (80 g)', grams: 80 }] },
  { id: 'falafel', name: 'Falafel', kosher: 'pareve', category: 'mixed', state: 'prepared', per100: n(333, 13.3, 31.8, 17.8, 5.0, 54), variability: 0.3, units: [{ label: 'ball (17 g)', grams: 17 }] },
  { id: 'schnitzel', name: 'Chicken schnitzel, fried', kosher: 'meat', category: 'protein', state: 'prepared', per100: n(260, 21.0, 14.0, 13.0, 0.8, 20), variability: 0.3 },
  { id: 'shawarma', name: 'Shawarma meat', kosher: 'meat', category: 'protein', state: 'prepared', per100: n(230, 22.0, 2.0, 15.0, 0, 20), variability: 0.35 },
  { id: 'fries', name: 'French fries', kosher: 'pareve', category: 'carb', state: 'prepared', per100: n(312, 3.4, 41.0, 15.0, 3.8, 18), variability: 0.3 },
  { id: 'pizza', name: 'Pizza, cheese', kosher: 'dairy', category: 'mixed', state: 'prepared', per100: n(266, 11.4, 33.0, 10.0, 2.3, 190), variability: 0.3, units: [{ label: 'slice (110 g)', grams: 110 }] },
];

export const FOOD_BY_ID: Record<string, Food> = Object.fromEntries(FOODS.map((f) => [f.id, f]));

export function food(id: string): Food {
  const f = FOOD_BY_ID[id];
  if (!f) throw new Error(`Unknown food ${id}`);
  return f;
}

// ---------- Raw, dry, and cooked weights ----------

/** Typical weight change from the raw or dry state to the cooked state, with a range, because water and cooking time differ. */
export interface CookingYield {
  from: string;
  to: string;
  /** Cooked grams per raw or dry gram. */
  factor: number;
  range: [number, number];
  note: string;
}

export const YIELDS: CookingYield[] = [
  { from: 'rice-dry', to: 'rice-cooked', factor: 2.7, range: [2.5, 3.0], note: 'Rice absorbs water. Values for dry and cooked rice imply about 2.7 to 2.8 times.' },
  { from: 'lentils-dry', to: 'lentils-cooked', factor: 3.0, range: [2.7, 3.1], note: 'Lentils absorb water. Values for dry and boiled lentils imply about 3 times.' },
  { from: 'chicken-raw', to: 'chicken-breast', factor: 0.72, range: [0.68, 0.78], note: 'Chicken loses water when cooked, about 25 to 30 percent of its weight.' },
];

/** Cooked weight from a raw or dry weight, as a middle value with a range. Null when no yield is known. */
export function cookedWeight(fromId: string, grams: number): { toId: string; mid: number; low: number; high: number } | null {
  const y = YIELDS.find((x) => x.from === fromId);
  if (!y) return null;
  return { toId: y.to, mid: Math.round(grams * y.factor), low: Math.round(grams * y.range[0]), high: Math.round(grams * y.range[1]) };
}

/** Raw or dry weight needed for a cooked weight. Null when no yield is known. */
export function rawWeightFor(cookedId: string, grams: number): { fromId: string; mid: number; low: number; high: number } | null {
  const y = YIELDS.find((x) => x.to === cookedId);
  if (!y) return null;
  return { fromId: y.from, mid: Math.round(grams / y.factor), low: Math.round(grams / y.range[1]), high: Math.round(grams / y.range[0]) };
}
