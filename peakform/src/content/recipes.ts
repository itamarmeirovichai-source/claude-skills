// Built in text recipes. Every recipe is complete without any external video.
// Nutrition is calculated from the ingredient list in the app, then shown as a range.

export interface RecipeIngredient {
  /** Food ID when the ingredient maps to the food list, used for nutrition. */
  foodId?: string;
  name: string;
  /** Amount per full recipe. */
  grams?: number;
  amount?: string;
  state?: 'raw' | 'cooked' | 'dry' | 'as sold';
}

export type Suitability = 'before training' | 'after training' | 'rest day' | 'any day';

export interface Recipe {
  id: string;
  name: string;
  summary: string;
  servings: number;
  ingredients: RecipeIngredient[];
  /** When raw and cooked weights differ, explain which one the plan uses. */
  weightNote: string;
  steps: string[];
  storage: string[];
  reheating: string[];
  substitutions: string[];
  foodSafety: string[];
  suitableFor: Suitability[];
  /** Portion based guides have no fixed ingredient list for nutrition. */
  guideOnly?: boolean;
  /** Override for recipes whose final cooked weight changes the per serving math. */
  cookedYieldGrams?: number;
}

const COOL_AND_CHILL = 'Refrigerate or freeze cooked food within two hours of cooking.';
const FRIDGE = 'Keep the refrigerator at or below 4°C. Use refrigerated leftovers within three to four days.';
const REHEAT = 'Reheat leftovers until steaming hot, 74°C in the centre.';

export const RECIPES: Recipe[] = [
  {
    id: 'yogurt-oat-breakfast',
    name: 'Yogurt, oat, banana, and berry breakfast',
    summary: 'The example breakfast. Takes two minutes to assemble.',
    servings: 1,
    ingredients: [
      { foodId: 'yogurt-hp', name: 'High protein yogurt or skyr, 0 to 3% fat', grams: 300, state: 'as sold' },
      { foodId: 'oats', name: 'Rolled oats', grams: 80, state: 'dry' },
      { foodId: 'banana', name: 'Banana, sliced', grams: 118, amount: '1 medium' },
      { foodId: 'berries-frozen', name: 'Frozen berries (optional)', grams: 100 },
    ],
    weightNote: 'Oats are weighed dry. Yogurt is weighed as sold.',
    steps: [
      'Spoon the yogurt into a bowl.',
      'Add the dry oats and stir. Let it sit for a minute if you like softer oats.',
      'Slice the banana on top.',
      'Add frozen berries straight from the freezer. They thaw in a few minutes.',
    ],
    storage: ['Overnight version: mix yogurt and oats in a jar and keep it in the fridge for up to two days. Add the banana in the morning.'],
    reheating: ['Eat cold.'],
    substitutions: ['Oats can be swapped for 60 g of another whole grain cereal without added sugar.', 'Banana can be swapped for an apple or 150 g of other fruit.', 'Yogurt can be swapped for 300 g cottage cheese, which adds some fat.'],
    foodSafety: ['Keep opened yogurt in the fridge and use it by the date on the tub.'],
    suitableFor: ['any day'],
  },
  {
    id: 'chicken-rice-boxes',
    name: 'Chicken and rice boxes',
    summary: 'Six afternoon meals for Sunday to Friday, the same on training days and days off.',
    servings: 6,
    ingredients: [
      { foodId: 'chicken-breast', name: 'Chicken breast, cooked (about 1 kg raw)', grams: 720, state: 'cooked', amount: 'About 1 kg raw, which cooks down to about 720 g' },
      { foodId: 'rice-cooked', name: 'White rice, cooked (about 450 g dry)', grams: 1200, state: 'cooked', amount: 'About 450 g dry rice' },
      { name: 'Salt, pepper, paprika, garlic powder', amount: 'To taste' },
    ],
    weightNote: 'Weights are cooked: 120 g chicken and 200 g rice per box, an example serving. 1 kg raw chicken gives about 720 g cooked, and 450 g dry rice about 1,200 g cooked.',
    steps: [
      'Rinse 450 g dry rice and cook it with water by the packet instructions.',
      'Season the raw chicken with salt and spices. Wash your hands and any surface the raw chicken touched.',
      'Bake the chicken at about 200°C for 20 to 25 minutes, or pan cook it without extra oil.',
      'Check the thickest piece with a thermometer. It must reach 74°C.',
      'Spread the rice in a shallow container so it cools quickly, ideally within about an hour.',
      'Weigh 120 g chicken and 200 g rice into each of six boxes.',
    ],
    storage: ['Label each box with the day.', 'Keep the next day or two in the fridge.', 'Freeze the other boxes as soon as they have cooled. Cooked rice is safest eaten soon or frozen, and reheated only once.', COOL_AND_CHILL, FRIDGE],
    reheating: ['Move a frozen box to the fridge the night before.', REHEAT],
    substitutions: ['Chicken can be swapped for 120 g cooked turkey breast, 140 g tuna in water, or 200 g firm tofu. PeakForm shows the estimated change.', 'Rice can be swapped for the same energy in potato, sweet potato, couscous, or pasta.'],
    foodSafety: ['Poultry must reach 74°C.', 'Cooked rice should be cooled and refrigerated quickly. Do not leave it out for hours.', COOL_AND_CHILL],
    suitableFor: ['any day'],
  },
  {
    id: 'sheet-pan-salmon',
    name: 'Sheet pan salmon, potato, and vegetables',
    summary: 'Dinner for Sunday and Wednesday. One tray, 5 g oil per serving.',
    servings: 2,
    ingredients: [
      { foodId: 'salmon', name: 'Salmon fillet, about 450 g raw for two cooked portions of 180 g', grams: 360, state: 'cooked' },
      { foodId: 'potato', name: 'Potatoes, cubed', grams: 500, state: 'cooked' },
      { foodId: 'lentils-cooked', name: 'Cooked lentils', grams: 200, state: 'cooked' },
      { foodId: 'veg-mixed', name: 'Vegetables: broccoli, zucchini, peppers', grams: 600 },
      { foodId: 'olive-oil', name: 'Olive oil for the tray', grams: 10 },
      { name: 'Lemon, garlic, salt, pepper, dill or paprika', amount: 'To taste' },
    ],
    weightNote: 'Per serving: 180 g cooked salmon, 250 g cooked potato, 100 g cooked lentils, 300 g vegetables, 5 g oil.',
    steps: [
      'Heat the oven to 200°C and line a tray with baking paper.',
      'Roast the potato cubes for 15 minutes.',
      'Add the vegetables and the salmon to the tray. Season with lemon, garlic, and spices.',
      'Roast for 12 to 15 minutes more, until the salmon flakes easily and reaches 63°C in the thickest part.',
      'Serve with 100 g cooked lentils per portion.',
    ],
    storage: [COOL_AND_CHILL, FRIDGE],
    reheating: [REHEAT, 'Reheat salmon gently so it does not dry out.'],
    substitutions: ['Salmon can be swapped for another oily fish such as trout.', 'Potato can be swapped for sweet potato.'],
    foodSafety: ['Fish must reach 63°C.', COOL_AND_CHILL],
    suitableFor: ['after training'],
  },
  {
    id: 'beef-bowl',
    name: 'Lean beef, potato, lentil, and vegetable bowl',
    summary: 'Dinner for Monday and Thursday.',
    servings: 2,
    ingredients: [
      { foodId: 'beef-lean', name: 'Lean beef, about 500 g raw for two cooked portions of 180 g', grams: 360, state: 'cooked' },
      { foodId: 'potato', name: 'Potatoes', grams: 500, state: 'cooked' },
      { foodId: 'lentils-cooked', name: 'Cooked lentils', grams: 200, state: 'cooked' },
      { foodId: 'veg-mixed', name: 'Mixed vegetables', grams: 600 },
      { foodId: 'olive-oil', name: 'Olive oil for the vegetables', grams: 10 },
      { name: 'Onion, garlic, cumin, paprika, salt', amount: 'To taste' },
    ],
    weightNote: 'Per serving: 180 g cooked lean beef, 250 g cooked potato, 100 g cooked lentils, 300 g vegetables, 5 g oil.',
    steps: [
      'Boil or bake the potatoes until soft.',
      'Brown the beef in a non stick pan without extra oil. Pour off visible fat.',
      'If the beef is ground, cook it until it reaches 71°C and no pink remains.',
      'Steam or roast the vegetables.',
      'Build each bowl with the weights above.',
    ],
    storage: ['Keep the Monday bowl in the fridge.', 'Freeze the Thursday bowl as soon as it has cooled.', COOL_AND_CHILL, FRIDGE],
    reheating: ['Move the frozen bowl to the fridge the night before.', REHEAT],
    substitutions: ['Beef can be swapped for lean ground turkey.', 'Lentils can be swapped for chickpeas, which adds a little fat.'],
    foodSafety: ['Ground beef must reach 71°C. Whole cuts reach 63°C and rest for three minutes.', COOL_AND_CHILL],
    suitableFor: ['after training'],
  },
  {
    id: 'white-fish-plate',
    name: 'White fish, potato, lentil, and vegetable plate',
    summary: 'Tuesday dinner. Includes 5 g olive oil.',
    servings: 1,
    ingredients: [
      { foodId: 'white-fish', name: 'White fish, about 250 g raw', grams: 200, state: 'cooked' },
      { foodId: 'potato', name: 'Potatoes', grams: 250, state: 'cooked' },
      { foodId: 'lentils-cooked', name: 'Cooked lentils', grams: 100, state: 'cooked' },
      { foodId: 'veg-mixed', name: 'Vegetables', grams: 300 },
      { foodId: 'olive-oil', name: 'Olive oil', grams: 5 },
      { name: 'Lemon, parsley, salt, pepper', amount: 'To taste' },
    ],
    weightNote: '200 g cooked fish comes from about 250 g raw.',
    steps: [
      'Boil or bake the potatoes.',
      'Brush the fish with the 5 g olive oil and season it.',
      'Bake at 200°C for 10 to 14 minutes until it flakes and reaches 63°C.',
      'Serve with the lentils and vegetables.',
    ],
    storage: [COOL_AND_CHILL, FRIDGE],
    reheating: [REHEAT],
    substitutions: ['Any white fish works: cod, hake, tilapia, or sea bass.'],
    foodSafety: ['Fish must reach 63°C.', COOL_AND_CHILL],
    suitableFor: ['after training'],
  },
  {
    id: 'turkey-plate',
    name: 'Turkey, potato, lentil, and vegetable plate',
    summary: 'Friday dinner, cooked before the Sabbath. Includes 5 g olive oil.',
    servings: 1,
    ingredients: [
      { foodId: 'turkey-breast', name: 'Turkey breast, about 250 g raw', grams: 180, state: 'cooked' },
      { foodId: 'potato', name: 'Potatoes', grams: 250, state: 'cooked' },
      { foodId: 'lentils-cooked', name: 'Cooked lentils', grams: 100, state: 'cooked' },
      { foodId: 'veg-mixed', name: 'Vegetables', grams: 300 },
      { foodId: 'olive-oil', name: 'Olive oil', grams: 5 },
    ],
    weightNote: '180 g cooked turkey comes from about 250 g raw.',
    steps: [
      'Season the turkey and bake it at 200°C, or pan cook it with the 5 g olive oil.',
      'Check that the thickest part reaches 74°C.',
      'Cook the potatoes and vegetables.',
      'Serve with the lentils.',
    ],
    storage: ['Freeze as soon as it has cooled. Move it to the fridge on Thursday night.', COOL_AND_CHILL, FRIDGE],
    reheating: [REHEAT],
    substitutions: ['Turkey can be swapped for chicken breast.'],
    foodSafety: ['Poultry must reach 74°C.', COOL_AND_CHILL],
    suitableFor: ['after training'],
  },
  {
    id: 'lentil-soup',
    name: 'Lentil soup',
    summary: 'One pot, six servings. Replaces the lentils and part of the vegetables at dinner.',
    servings: 6,
    cookedYieldGrams: 2700,
    ingredients: [
      { name: 'Dry lentils', grams: 250, state: 'dry' },
      { name: 'Onion', amount: '1', grams: 150 },
      { name: 'Carrots', amount: '2 to 3', grams: 200 },
      { name: 'Celery', amount: '2 sticks', grams: 100 },
      { name: 'Tomatoes', amount: '3 to 4', grams: 300 },
      { name: 'Water', amount: 'About 2 litres' },
      { name: 'Olive oil', amount: 'No more than 10 g for the whole pot', grams: 10 },
      { name: 'Cumin, turmeric, garlic, iodised salt, pepper', amount: 'To taste' },
    ],
    weightNote: 'The finished pot weighs about 2.7 kg. One serving is about 450 g and is roughly 200 kcal and 11 g protein.',
    steps: [
      'Rinse the lentils.',
      'Chop the onion, carrots, celery, and tomatoes.',
      'Warm the olive oil in a large pot and soften the onion for three minutes.',
      'Add the other vegetables, lentils, spices, and about 2 litres of water.',
      'Simmer for 30 to 40 minutes until the lentils are soft. Add water if it gets too thick.',
      'Divide into six containers.',
    ],
    storage: ['Keep three servings in the fridge and freeze the rest.', COOL_AND_CHILL, FRIDGE],
    reheating: ['Bring the soup to a rolling boil or 74°C before eating.'],
    substitutions: ['Red lentils cook faster. Green or brown lentils hold their shape.', 'When soup replaces the dinner lentils and part of the vegetables, add about 200 g more vegetables to complete the plate.'],
    foodSafety: ['Cool the pot quickly by dividing it into shallow containers.', COOL_AND_CHILL],
    suitableFor: ['after training', 'rest day'],
  },
  {
    id: 'school-plate',
    name: 'Tofu, egg, and salad school plate',
    summary: 'Built from cafeteria food, so nothing perishable has to sit in a school bag.',
    servings: 1,
    ingredients: [
      { foodId: 'egg', name: 'Whole eggs', grams: 100, amount: '2' },
      { foodId: 'egg-white', name: 'Egg whites', grams: 66, amount: '2' },
      { foodId: 'tofu', name: 'Tofu', grams: 135, amount: '120 to 150 g, about the size of your palm' },
      { foodId: 'salad', name: 'Large salad: cucumber, tomato, cherry tomato, onion, peppers', grams: 300 },
      { foodId: 'olives', name: 'Olives, small serving', grams: 30, amount: 'About 7' },
    ],
    weightNote: 'Portions are estimated by eye, so PeakForm logs this plate with a range.',
    steps: [
      'Take two whole eggs and two egg whites, or the closest the cafeteria offers.',
      'Add a palm sized piece of tofu.',
      'Fill half the plate or a bowl with salad vegetables.',
      'Add a small serving of olives.',
      'Skip added oil and mayonnaise unless you want them. If you add them, log them.',
    ],
    storage: ['Cafeteria food needs nothing from home.', 'If you bring eggs or tofu from home, use an insulated bag with two ice packs. Perishable food should not sit warm for more than two hours, or one hour above 32°C.'],
    reheating: ['Not needed.'],
    substitutions: ['No tofu today: add two more egg whites or a serving of legumes.', 'No eggs today: take a larger tofu portion or cottage cheese if offered.'],
    foodSafety: ['Choose eggs that are fully cooked.'],
    suitableFor: ['any day'],
  },
  {
    id: 'sabbath-plate',
    name: 'Sabbath plate guide',
    summary: 'A discreet way to eat hosted meals without a scale or special food.',
    servings: 1,
    guideOnly: true,
    ingredients: [
      { name: 'Protein: about two palm sized portions of meat, chicken, fish, or eggs' },
      { name: 'Rice or potatoes: one normal serving' },
      { name: 'Salad or vegetables: a generous serving' },
      { name: 'Challah: one or two slices' },
      { name: 'A sweet portion after a meal, if you want one' },
      { name: 'Water or a zero calorie drink' },
    ],
    weightNote: 'Nothing is weighed. Log it after the Sabbath in one tap with an honest range.',
    steps: [
      'Start with salad or vegetables.',
      'Take two palm sized portions of protein.',
      'Add rice or potatoes and one or two slices of challah. Take more if you are hungry.',
      'Have a sweet portion after a meal if you want one, and enjoy it.',
      'There is no make up exercise and no guilt.',
    ],
    storage: ['Not needed.'],
    reheating: ['Not needed.'],
    substitutions: ['Any main dish works. Aim for the same plate shape.'],
    foodSafety: ['Normal hosted meal food safety applies.'],
    suitableFor: ['rest day'],
  },
  {
    id: 'restaurant-guide',
    name: 'Restaurant portion estimate guide',
    summary: 'How to log a restaurant meal honestly in under a minute.',
    servings: 1,
    guideOnly: true,
    ingredients: [
      { name: 'Protein portion: count palms' },
      { name: 'Rice, pasta, potato, or bread: count fists or pick small, medium, or large' },
      { name: 'Vegetables: count fists' },
      { name: 'Sauces and oil: count thumbs, or add a hidden oil allowance' },
    ],
    weightNote: 'Restaurant food usually has more oil than home food. PeakForm widens the range instead of guessing a single number.',
    steps: [
      'Open Eat and tap Restaurant estimate.',
      'Add each part of the plate using hand portions or a small, medium, or large restaurant portion.',
      'Leave the hidden oil allowance on unless the food was clearly grilled or steamed.',
      'Save. PeakForm stores the range and the method, not a false exact number.',
    ],
    storage: ['Not needed.'],
    reheating: ['Not needed.'],
    substitutions: ['If you are not hungry or plans changed, log a short note instead. That is useful data too.'],
    foodSafety: ['Refrigerate leftovers within two hours.'],
    suitableFor: ['any day'],
  },
];

export const RECIPE_BY_ID: Record<string, Recipe> = Object.fromEntries(RECIPES.map((r) => [r.id, r]));

// ---------- Weekly meal preparation ----------

export interface ShoppingItem {
  id: string;
  name: string;
  /** Quantity for the six example days, Sunday to Friday. */
  qty: number;
  unit: 'g' | 'kg' | 'ml' | 'l' | 'pcs' | '';
  section: 'Dairy' | 'Grains' | 'Produce' | 'Meat and fish' | 'Pantry' | 'Cafeteria backup';
  /** Items that do not scale with servings (spices, oil). */
  fixed?: boolean;
  note?: string;
}

export const SHOPPING_LIST: ShoppingItem[] = [
  { id: 'yogurt', name: 'High protein yogurt or skyr', qty: 1800, unit: 'g', section: 'Dairy' },
  { id: 'milk', name: 'Milk, for evenings after a fish dinner', qty: 900, unit: 'ml', section: 'Dairy' },
  { id: 'oats', name: 'Oats', qty: 480, unit: 'g', section: 'Grains' },
  { id: 'rice', name: 'Dry rice', qty: 450, unit: 'g', section: 'Grains' },
  { id: 'lentils', name: 'Dry lentils', qty: 200, unit: 'g', section: 'Grains' },
  { id: 'bananas', name: 'Bananas', qty: 6, unit: 'pcs', section: 'Produce' },
  { id: 'berries', name: 'Frozen berries', qty: 600, unit: 'g', section: 'Produce' },
  { id: 'apples', name: 'Apples, for the school snack and evenings after a meat dinner', qty: 8, unit: 'pcs', section: 'Produce' },
  { id: 'potatoes', name: 'Potatoes', qty: 1500, unit: 'g', section: 'Produce' },
  { id: 'vegetables', name: 'Non starchy vegetables, at least', qty: 1800, unit: 'g', section: 'Produce' },
  { id: 'almonds', name: 'Almonds', qty: 220, unit: 'g', section: 'Pantry' },
  { id: 'chicken', name: 'Raw chicken breast for the afternoon boxes', qty: 1000, unit: 'g', section: 'Meat and fish' },
  { id: 'salmon', name: 'Raw salmon', qty: 450, unit: 'g', section: 'Meat and fish' },
  { id: 'beef', name: 'Raw lean beef', qty: 500, unit: 'g', section: 'Meat and fish' },
  { id: 'white-fish', name: 'Raw white fish', qty: 250, unit: 'g', section: 'Meat and fish' },
  { id: 'turkey', name: 'Raw turkey', qty: 250, unit: 'g', section: 'Meat and fish' },
  { id: 'olive-oil', name: 'Olive oil', qty: 0, unit: '', section: 'Pantry', fixed: true },
  { id: 'salt', name: 'Iodised salt', qty: 0, unit: '', section: 'Pantry', fixed: true },
  { id: 'spices', name: 'Spices', qty: 0, unit: '', section: 'Pantry', fixed: true },
  { id: 'eggs', name: 'Eggs, only if the cafeteria does not provide them', qty: 24, unit: 'pcs', section: 'Cafeteria backup' },
  { id: 'tofu', name: 'Tofu, only if the cafeteria does not provide it', qty: 900, unit: 'g', section: 'Cafeteria backup' },
];

export const DEFAULT_PREP_DAYS = 6;

export function scaleShopping(item: ShoppingItem, days: number): number {
  if (item.fixed) return 0;
  const raw = (item.qty * days) / DEFAULT_PREP_DAYS;
  if (item.unit === 'pcs') return Math.ceil(raw);
  if (item.unit === 'g' || item.unit === 'ml') return Math.ceil(raw / 10) * 10;
  return Math.round(raw * 10) / 10;
}

export const PREP_STEPS: Array<{ id: string; title: string; detail: string }> = [
  { id: 'rice', title: 'Cook the rice', detail: 'Cook 450 g dry rice, which makes about 1,200 g cooked. Spread it out to cool quickly and portion 200 g into each box.' },
  { id: 'lentils', title: 'Cook the lentils', detail: 'Simmer 200 g dry lentils for about 20 to 30 minutes. They make about 600 g cooked, 100 g for each dinner.' },
  { id: 'chicken', title: 'Cook the chicken', detail: 'Cook the chicken until the thickest part reaches 74°C. Portion 120 g cooked into six containers.' },
  { id: 'dinners', title: 'Prepare the six dinners', detail: 'Sunday and Wednesday salmon, Monday and Thursday lean beef, Tuesday white fish, Friday turkey. Each with 250 g potato, 100 g cooked lentils, 300 g vegetables, and about 5 g oil.' },
  { id: 'breakfast', title: 'Prepare breakfast parts', detail: 'Portion 80 g oats into six bags or jars. Keep yogurt, bananas, and frozen berries ready. Pack apples and almonds for school.' },
  { id: 'lunch', title: 'Plan school lunch', detail: 'Lunch comes from the cafeteria. If the cafeteria has no eggs or tofu and you bring them, pack them cold with two ice packs in an insulated bag.' },
  { id: 'label', title: 'Label every container', detail: 'Write the day and the meal on each container.' },
  { id: 'fridge', title: 'Refrigerate the next two days', detail: 'Keep the meals for the next one or two days in the fridge.' },
  { id: 'freeze', title: 'Freeze the rest', detail: 'Freeze the other meals, and all rice boxes after the second day, as soon as they have cooled.' },
  { id: 'thaw', title: 'Thaw the night before', detail: 'Move a frozen meal to the fridge the night before you need it.' },
  { id: 'two-hours', title: 'Two hour rule', detail: 'Refrigerate or freeze cooked food within two hours.' },
  { id: 'fridge-temp', title: 'Fridge temperature', detail: 'Keep the fridge at or below 4°C.' },
  { id: 'leftovers', title: 'Leftover limit', detail: 'Use refrigerated leftovers within three to four days.' },
  { id: 'reheat', title: 'Reheat properly', detail: 'Reheat leftovers to 74°C.' },
];

export const COOKING_TEMPERATURES = [
  { food: 'Poultry', celsius: 74 },
  { food: 'Fish', celsius: 63 },
  { food: 'Ground beef', celsius: 71 },
  { food: 'Leftovers, reheated', celsius: 74 },
] as const;

export const RAW_COOKED_NOTE =
  'Meat and fish lose about 25 to 30 percent of their weight when cooked. Rice and lentils gain weight: 100 g dry rice becomes about 270 g cooked, and 100 g dry lentils about 300 g. PeakForm meal weights are cooked unless a recipe says raw or dry, and the food list has separate raw and dry entries.';
