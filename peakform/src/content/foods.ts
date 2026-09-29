// Built in food values per 100 g (or per 100 ml for drinks).
// Values are rounded approximations of common reference data (USDA FoodData Central style
// entries for the cooked or raw state named). Real labels and recipes differ, so every
// food carries a variability percentage that widens the displayed range.

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
  state: 'cooked' | 'raw' | 'dry' | 'as sold' | 'prepared';
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
  { id: 'yogurt-hp', name: 'High protein yogurt or skyr, 0 to 3% fat', category: 'dairy', state: 'as sold', per100: n(68, 10.5, 4.0, 1.2, 0, 120), variability: 0.15, units: [{ label: 'tub (200 g)', grams: 200 }], note: 'Brands vary. Check the label for protein per 100 g.' },
  { id: 'banana', name: 'Banana', category: 'fruit', state: 'raw', per100: n(89, 1.1, 22.8, 0.3, 2.6, 5), variability: 0.1, units: [{ label: 'medium banana', grams: 118 }, { label: 'small banana', grams: 100 }, { label: 'large banana', grams: 136 }] },
  { id: 'oats', name: 'Rolled oats', category: 'carb', state: 'dry', per100: n(379, 13.2, 67.7, 6.5, 10.1, 52), variability: 0.05 },
  { id: 'berries-frozen', name: 'Frozen mixed berries', category: 'fruit', state: 'raw', per100: n(50, 0.8, 11.5, 0.3, 3.5, 15), variability: 0.15 },
  { id: 'protein-powder', name: 'Whey protein powder', category: 'protein', state: 'as sold', per100: n(390, 78, 8, 5, 0, 400), variability: 0.1, units: [{ label: 'scoop (30 g)', grams: 30 }, { label: 'half scoop (15 g)', grams: 15 }], note: 'Prefer a third party tested product, reviewed with a parent.' },

  // School lunch
  { id: 'egg', name: 'Egg, whole', category: 'protein', state: 'cooked', per100: n(143, 12.6, 0.7, 9.5, 0, 56), variability: 0.1, units: [{ label: 'large egg', grams: 50 }] },
  { id: 'egg-white', name: 'Egg white', category: 'protein', state: 'cooked', per100: n(52, 10.9, 0.7, 0.2, 0, 7), variability: 0.1, units: [{ label: 'egg white', grams: 33 }] },
  { id: 'tofu', name: 'Tofu, firm', category: 'protein', state: 'as sold', per100: n(144, 17.3, 2.8, 8.7, 2.3, 350), variability: 0.3, note: 'Firmness and calcium vary a lot by brand and coagulant.' },
  { id: 'salad', name: 'Salad vegetables, no dressing', category: 'vegetable', state: 'raw', per100: n(20, 0.9, 4.0, 0.2, 1.3, 15), variability: 0.2, note: 'Cucumber, tomato, cherry tomato, onion, peppers, leaves.' },
  { id: 'olives', name: 'Olives', category: 'fat', state: 'as sold', per100: n(130, 1.0, 5.0, 13.0, 3.0, 60), variability: 0.15, units: [{ label: 'olive', grams: 4 }] },

  // Carbohydrates
  { id: 'rice-cooked', name: 'White rice', category: 'carb', state: 'cooked', per100: n(130, 2.7, 28.2, 0.3, 0.4, 10), variability: 0.1, note: 'About 100 g dry rice makes 250 to 300 g cooked.' },
  { id: 'potato', name: 'Potato, boiled or baked, no oil', category: 'carb', state: 'cooked', per100: n(87, 1.9, 20.1, 0.1, 1.8, 5), variability: 0.1 },
  { id: 'sweet-potato', name: 'Sweet potato, baked', category: 'carb', state: 'cooked', per100: n(90, 2.0, 20.7, 0.2, 3.3, 38), variability: 0.1 },
  { id: 'pasta-cooked', name: 'Pasta', category: 'carb', state: 'cooked', per100: n(158, 5.8, 30.9, 0.9, 1.8, 7), variability: 0.1 },
  { id: 'couscous-cooked', name: 'Couscous', category: 'carb', state: 'cooked', per100: n(112, 3.8, 23.2, 0.2, 1.4, 8), variability: 0.1 },
  { id: 'quinoa-cooked', name: 'Quinoa', category: 'carb', state: 'cooked', per100: n(120, 4.4, 21.3, 1.9, 2.8, 17), variability: 0.1 },
  { id: 'bread-wholewheat', name: 'Whole wheat bread', category: 'bread', state: 'as sold', per100: n(250, 12.0, 43.0, 3.5, 7.0, 100), variability: 0.15, units: [{ label: 'slice', grams: 35 }] },
  { id: 'challah', name: 'Challah', category: 'bread', state: 'as sold', per100: n(290, 8.5, 50.0, 6.0, 2.0, 60), variability: 0.2, units: [{ label: 'slice', grams: 40 }] },
  { id: 'lentils-cooked', name: 'Lentils', category: 'carb', state: 'cooked', per100: n(116, 9.0, 20.1, 0.4, 7.9, 19), variability: 0.1, note: 'About 100 g dry lentils makes 250 g cooked.' },
  { id: 'chickpeas-cooked', name: 'Chickpeas', category: 'carb', state: 'cooked', per100: n(164, 8.9, 27.4, 2.6, 7.6, 49), variability: 0.1 },

  // Proteins
  { id: 'chicken-breast', name: 'Chicken breast, skinless', category: 'protein', state: 'cooked', per100: n(165, 31.0, 0, 3.6, 0, 15), variability: 0.1, note: 'Raw chicken loses about 25 to 30 percent of its weight when cooked.' },
  { id: 'salmon', name: 'Salmon', category: 'protein', state: 'cooked', per100: n(206, 22.1, 0, 12.4, 0, 15), variability: 0.15 },
  { id: 'beef-lean', name: 'Lean beef, about 90% lean', category: 'protein', state: 'cooked', per100: n(200, 27.0, 0, 10.0, 0, 15), variability: 0.2, note: 'Fat content changes calories a lot. Check the cut or label.' },
  { id: 'white-fish', name: 'White fish (cod, hake, tilapia)', category: 'protein', state: 'cooked', per100: n(105, 23.0, 0, 1.2, 0, 15), variability: 0.1 },
  { id: 'turkey-breast', name: 'Turkey breast, skinless', category: 'protein', state: 'cooked', per100: n(147, 30.0, 0, 2.1, 0, 12), variability: 0.1 },
  { id: 'tuna-water', name: 'Tuna in water, drained', category: 'protein', state: 'as sold', per100: n(116, 25.5, 0, 0.8, 0, 11), variability: 0.1 },
  { id: 'cottage-cheese', name: 'Cottage cheese, 5%', category: 'dairy', state: 'as sold', per100: n(95, 11.0, 1.5, 5.0, 0, 90), variability: 0.1 },

  // Vegetables
  { id: 'veg-mixed', name: 'Mixed vegetables', category: 'vegetable', state: 'cooked', per100: n(35, 2.0, 7.0, 0.3, 3.0, 35), variability: 0.2, note: 'Broccoli, carrots, zucchini, cauliflower, green beans.' },
  { id: 'green-beans', name: 'Green beans', category: 'vegetable', state: 'cooked', per100: n(35, 1.9, 7.9, 0.3, 3.2, 44), variability: 0.1 },
  { id: 'peas', name: 'Peas', category: 'vegetable', state: 'cooked', per100: n(84, 5.4, 15.6, 0.2, 5.5, 27), variability: 0.1 },
  { id: 'lentil-soup', name: 'Lentil soup (PeakForm recipe)', category: 'mixed', state: 'prepared', per100: n(44, 2.5, 7.3, 0.5, 1.5, 10), variability: 0.2, units: [{ label: 'serving (about 450 g)', grams: 450 }], note: 'One sixth of the built in pot recipe, about 2.7 kg in total.' },

  // Fats
  { id: 'olive-oil', name: 'Olive oil', category: 'fat', state: 'as sold', per100: n(884, 0, 0, 100, 0, 1), variability: 0.02, units: [{ label: 'teaspoon', grams: 4.5 }, { label: 'tablespoon', grams: 13.5 }] },
  { id: 'tahini', name: 'Tahini sauce, prepared', category: 'fat', state: 'prepared', per100: n(290, 8.0, 10.0, 25.0, 4.0, 150), variability: 0.3, units: [{ label: 'tablespoon', grams: 15 }] },

  // Drinks
  { id: 'milk', name: 'Milk, 2%', category: 'dairy', state: 'as sold', liquid: true, per100: n(50, 3.3, 4.8, 2.0, 0, 120), variability: 0.1, units: [{ label: 'glass (250 ml)', grams: 250 }] },
  { id: 'coke-zero', name: 'Coke Zero', category: 'drink', state: 'as sold', liquid: true, per100: n(0.3, 0, 0, 0, 0, 0, 9.6), variability: 0, units: [{ label: 'can (330 ml)', grams: 330 }, { label: 'bottle (500 ml)', grams: 500 }] },
  { id: 'zero-drink', name: 'Zero calorie drink', category: 'drink', state: 'as sold', liquid: true, per100: n(0, 0, 0, 0, 0, 0), variability: 0, units: [{ label: 'glass (250 ml)', grams: 250 }] },
  { id: 'water', name: 'Water', category: 'drink', state: 'as sold', liquid: true, per100: n(0, 0, 0, 0, 0, 0), variability: 0, units: [{ label: 'glass (250 ml)', grams: 250 }, { label: 'bottle (500 ml)', grams: 500 }] },

  // Common hosted and restaurant foods
  { id: 'sweet-portion', name: 'Sweet portion (cake, cookies, dessert)', category: 'sweet', state: 'prepared', per100: n(400, 5.0, 55.0, 18.0, 1.5, 50), variability: 0.3, units: [{ label: 'normal portion (70 g)', grams: 70 }] },
  { id: 'hummus', name: 'Hummus', category: 'mixed', state: 'prepared', per100: n(240, 7.0, 14.0, 17.0, 6.0, 40), variability: 0.3 },
  { id: 'pita', name: 'Pita bread', category: 'bread', state: 'as sold', per100: n(275, 9.1, 55.7, 1.2, 2.2, 86), variability: 0.15, units: [{ label: 'pita (80 g)', grams: 80 }] },
  { id: 'falafel', name: 'Falafel', category: 'mixed', state: 'prepared', per100: n(333, 13.3, 31.8, 17.8, 5.0, 54), variability: 0.3, units: [{ label: 'ball (17 g)', grams: 17 }] },
  { id: 'schnitzel', name: 'Chicken schnitzel, fried', category: 'protein', state: 'prepared', per100: n(260, 21.0, 14.0, 13.0, 0.8, 20), variability: 0.3 },
  { id: 'shawarma', name: 'Shawarma meat', category: 'protein', state: 'prepared', per100: n(230, 22.0, 2.0, 15.0, 0, 20), variability: 0.35 },
  { id: 'fries', name: 'French fries', category: 'carb', state: 'prepared', per100: n(312, 3.4, 41.0, 15.0, 3.8, 18), variability: 0.3 },
  { id: 'pizza', name: 'Pizza, cheese', category: 'mixed', state: 'prepared', per100: n(266, 11.4, 33.0, 10.0, 2.3, 190), variability: 0.3, units: [{ label: 'slice (110 g)', grams: 110 }] },
];

export const FOOD_BY_ID: Record<string, Food> = Object.fromEntries(FOODS.map((f) => [f.id, f]));

export function food(id: string): Food {
  const f = FOOD_BY_ID[id];
  if (!f) throw new Error(`Unknown food ${id}`);
  return f;
}
