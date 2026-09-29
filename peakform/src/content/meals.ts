import type { Weekday } from './plan';

// Default meal schedule and daily targets. All values are starting points for a
// fourteen day observation period, editable in the app, and never a diagnosis.

export type MealSlot = 'breakfast' | 'lunch' | 'preworkout' | 'dinner' | 'evening' | 'sabbath';

export interface MealItem {
  foodId: string;
  grams: number;
  /** Optional items can be switched off in one tap. */
  optional?: boolean;
  /** Whether an optional item is included by default. */
  defaultOn?: boolean;
  note?: string;
}

export interface MealTemplate {
  id: string;
  slot: MealSlot;
  name: string;
  /** Default time, 24 hour HH:MM. Editable in settings. */
  time: string;
  weekdays: Weekday[];
  items: MealItem[];
  notes: string[];
  /** Portions at school or restaurants are estimated, not weighed. */
  estimated?: boolean;
  recipeId?: string;
}

export const SLOT_LABELS: Record<MealSlot, string> = {
  breakfast: 'Breakfast',
  lunch: 'School lunch',
  preworkout: 'Before training',
  dinner: 'Dinner',
  evening: 'Evening milk',
  sabbath: 'Sabbath meal',
};

export const SLOT_ORDER: MealSlot[] = ['breakfast', 'lunch', 'preworkout', 'dinner', 'evening', 'sabbath'];

const TRAINING_DAYS: Weekday[] = [0, 1, 2, 3, 4, 5];

export const BREAKFAST: MealTemplate = {
  id: 'breakfast',
  slot: 'breakfast',
  name: 'Yogurt, oats, banana, berries',
  time: '07:10',
  weekdays: TRAINING_DAYS,
  recipeId: 'yogurt-oat-breakfast',
  items: [
    { foodId: 'yogurt-hp', grams: 300 },
    { foodId: 'banana', grams: 118 },
    { foodId: 'oats', grams: 60 },
    { foodId: 'berries-frozen', grams: 100, optional: true, defaultOn: true },
    { foodId: 'protein-powder', grams: 15, optional: true, defaultOn: false, note: 'Only if food protein is short that day.' },
  ],
  notes: ['After the morning session.', 'A full protein scoop is not needed.'],
};

export const SCHOOL_LUNCH: MealTemplate = {
  id: 'school-lunch',
  slot: 'lunch',
  name: 'Eggs, tofu, and a large salad',
  time: '12:00',
  weekdays: TRAINING_DAYS,
  recipeId: 'school-plate',
  estimated: true,
  items: [
    { foodId: 'egg', grams: 100, note: '2 whole eggs' },
    { foodId: 'egg-white', grams: 66, note: '2 egg whites' },
    { foodId: 'tofu', grams: 135, note: '120 to 150 g' },
    { foodId: 'salad', grams: 300, note: 'Large salad' },
    { foodId: 'olives', grams: 30, note: 'Small measured serving, about 7 olives' },
  ],
  notes: ['No added oil or mayonnaise by default.', 'Works without food from home.'],
};

const PRE_RICE: Record<Weekday, number> = { 0: 250, 1: 250, 2: 220, 3: 250, 4: 220, 5: 300, 6: 0 };

export const PREWORKOUT: MealTemplate[] = TRAINING_DAYS.map((d) => ({
  id: `preworkout-${d}`,
  slot: 'preworkout' as const,
  name: 'Chicken and rice',
  time: '15:20',
  weekdays: [d],
  recipeId: 'chicken-rice-boxes',
  items: [
    { foodId: 'rice-cooked', grams: PRE_RICE[d], note: 'Cooked weight' },
    { foodId: 'chicken-breast', grams: 120, note: 'Cooked weight' },
  ],
  notes: ['Eat about an hour before training.'],
}));

function dinner(d: Weekday, name: string, protein: [string, number], potato: number, oil: number, recipeId: string): MealTemplate {
  const items: MealItem[] = [
    { foodId: protein[0], grams: protein[1], note: 'Cooked weight' },
    { foodId: 'potato', grams: potato, note: 'Cooked weight' },
    { foodId: 'lentils-cooked', grams: 100, note: 'Cooked weight' },
    { foodId: 'veg-mixed', grams: 300 },
  ];
  if (oil > 0) items.push({ foodId: 'olive-oil', grams: oil });
  return {
    id: `dinner-${d}`,
    slot: 'dinner',
    name,
    time: '18:45',
    weekdays: [d],
    recipeId,
    items,
    notes: oil > 0 ? [`${oil} g olive oil.`] : ['No extra oil.'],
  };
}

export const DINNERS: MealTemplate[] = [
  dinner(0, 'Salmon, potato, lentils, vegetables', ['salmon', 180], 150, 0, 'sheet-pan-salmon'),
  dinner(1, 'Lean beef, potato, lentils, vegetables', ['beef-lean', 180], 150, 0, 'beef-bowl'),
  dinner(2, 'White fish, potato, lentils, vegetables', ['white-fish', 220], 250, 10, 'white-fish-plate'),
  dinner(3, 'Salmon, potato, lentils, vegetables', ['salmon', 180], 150, 0, 'sheet-pan-salmon'),
  dinner(4, 'Lean beef, potato, lentils, vegetables', ['beef-lean', 180], 150, 0, 'beef-bowl'),
  dinner(5, 'Turkey, potato, lentils, vegetables', ['turkey-breast', 180], 250, 10, 'turkey-plate'),
];

export const EVENING: MealTemplate = {
  id: 'evening-milk',
  slot: 'evening',
  name: 'Milk',
  time: '20:30',
  weekdays: TRAINING_DAYS,
  items: [{ foodId: 'milk', grams: 300, note: '300 ml' }],
  notes: ['Evening recovery item.'],
};

export const ALL_TEMPLATES: MealTemplate[] = [BREAKFAST, SCHOOL_LUNCH, ...PREWORKOUT, ...DINNERS, EVENING];

export function templatesForDay(weekday: Weekday, templates: MealTemplate[] = ALL_TEMPLATES): MealTemplate[] {
  return templates
    .filter((t) => t.weekdays.includes(weekday))
    .sort((a, b) => a.time.localeCompare(b.time));
}

// ---------- Daily targets ----------

export interface NutritionTarget {
  weekday: Weekday;
  label: string;
  kcal: number;
  /** Equivalent band around the calorie target. */
  kcalBand: [number, number];
  protein: number;
  proteinRange: [number, number];
  carbs: number;
  fat: number;
}

const band = (k: number): [number, number] => [k - 100, k + 100];

export const BASELINE_TARGETS: NutritionTarget[] = [
  { weekday: 0, label: 'Upper A and swim', kcal: 2450, kcalBand: band(2450), protein: 155, proteinRange: [150, 175], carbs: 260, fat: 88 },
  { weekday: 1, label: 'Lower A and jump', kcal: 2450, kcalBand: band(2450), protein: 155, proteinRange: [150, 175], carbs: 260, fat: 88 },
  { weekday: 2, label: 'Volleyball and shoulder care', kcal: 2350, kcalBand: band(2350), protein: 150, proteinRange: [150, 175], carbs: 230, fat: 92 },
  { weekday: 3, label: 'Lower B', kcal: 2450, kcalBand: band(2450), protein: 155, proteinRange: [150, 175], carbs: 260, fat: 88 },
  { weekday: 4, label: 'Upper B', kcal: 2350, kcalBand: band(2350), protein: 150, proteinRange: [150, 175], carbs: 230, fat: 92 },
  { weekday: 5, label: 'Speed, spike, and swim', kcal: 2550, kcalBand: band(2550), protein: 155, proteinRange: [150, 175], carbs: 285, fat: 88 },
  { weekday: 6, label: 'Rest', kcal: 2250, kcalBand: [2150, 2350], protein: 150, proteinRange: [150, 175], carbs: 190, fat: 93 },
];

/** Hard floors that no suggestion may cross. */
export const NUTRITION_FLOORS = {
  kcal: 2000,
  carbs: 130,
} as const;

// ---------- Sabbath plate guide ----------

export interface PlateGuideItem {
  label: string;
  detail: string;
  foodId: string;
  /** Grams for one plate, with a low to high range because nothing is weighed. */
  grams: [number, number, number];
}

export const SABBATH_PLATE: PlateGuideItem[] = [
  { label: 'Protein', detail: 'About two palm sized portions of meat, chicken, fish, or eggs.', foodId: 'chicken-breast', grams: [150, 200, 260] },
  { label: 'Rice or potatoes', detail: 'One normal serving, about the size of your fist.', foodId: 'rice-cooked', grams: [110, 150, 200] },
  { label: 'Salad or vegetables', detail: 'A generous serving. Half the plate is a good guide.', foodId: 'salad', grams: [150, 250, 350] },
  { label: 'Challah', detail: 'One or two slices.', foodId: 'challah', grams: [40, 60, 80] },
];

export const SABBATH_NOTES = [
  'One planned sweet portion right after one meal.',
  'No repeated grazing between meals.',
  'Water or a zero calorie drink.',
  'Hosted cooking often uses oil you cannot see. PeakForm adds that as uncertainty, not as a rule.',
  'No guilt and no exercise to make up for food.',
];

/** Unseen cooking oil allowance for hosted and restaurant meals, grams of oil. */
export const HIDDEN_OIL_RANGE: [number, number, number] = [0, 8, 20];
