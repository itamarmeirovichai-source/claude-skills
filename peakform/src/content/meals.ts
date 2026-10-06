import type { Weekday } from './plan';
import { FOOD_BY_ID } from './foods';
import { minutesOf } from '../domain/dates';

// Example meals (3.0.0). Every quantity is an example serving in grams with a household
// equivalent, not a prescription. Nothing here is a daily limit or a validated energy requirement:
// individual energy targets need a parent and a pediatric professional, and PeakForm records them
// separately (Goals and reviews). Meals are the same on training days and days off, and no food
// depends on finishing a workout.

export type MealSlot = 'breakfast' | 'snack' | 'lunch' | 'preworkout' | 'dinner' | 'evening' | 'sabbath';

export const EXAMPLE_NOTE = 'Example serving. Adjust to appetite and activity; this is not a daily limit.';

export interface MealItem {
  foodId: string;
  grams: number;
  /** A household equivalent, so nothing has to be weighed. */
  household?: string;
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
  /** How to make it. */
  prep: string[];
  /** Ways to eat more when hungry or after a bigger day. */
  more: string[];
  substitutions: string[];
  storage: string[];
  /** Portions at school or restaurants are estimated, not weighed. */
  estimated?: boolean;
  recipeId?: string;
}

export const SLOT_LABELS: Record<MealSlot, string> = {
  breakfast: 'Breakfast',
  snack: 'School snack',
  lunch: 'School lunch',
  preworkout: 'Afternoon meal',
  dinner: 'Dinner',
  evening: 'Evening snack',
  sabbath: 'Sabbath meal',
};

export const SLOT_ORDER: MealSlot[] = ['breakfast', 'snack', 'lunch', 'preworkout', 'dinner', 'evening', 'sabbath'];

const SCHOOL_DAYS: Weekday[] = [0, 1, 2, 3, 4, 5];
const FRIDGE = 'Keep in the fridge at or below 4°C.';

export const BREAKFAST: MealTemplate = {
  id: 'breakfast',
  slot: 'breakfast',
  name: 'Yogurt, oats, banana, berries',
  time: '07:10',
  weekdays: SCHOOL_DAYS,
  recipeId: 'yogurt-oat-breakfast',
  items: [
    { foodId: 'yogurt-hp', grams: 300, household: 'one and a half 200 g tubs' },
    { foodId: 'oats', grams: 80, household: 'about 1 cup, weighed dry' },
    { foodId: 'banana', grams: 118, household: '1 medium banana' },
    { foodId: 'berries-frozen', grams: 100, household: 'a large handful', optional: true, defaultOn: true },
  ],
  notes: ['Dairy.'],
  prep: ['Spoon the yogurt into a bowl, stir in the dry oats, and top with the banana and frozen berries.'],
  more: ['Another 30 g oats', 'A slice of whole wheat bread with a tablespoon of tahini', 'A second piece of fruit'],
  substitutions: ['Skyr or cottage cheese instead of yogurt', 'An apple or 150 g of other fruit instead of the banana'],
  storage: ['Overnight oats keep two days in the fridge. Add the banana in the morning.', FRIDGE],
};

/** A snack that keeps at room temperature in a school bag. */
export const SCHOOL_SNACK: MealTemplate = {
  id: 'school-snack',
  slot: 'snack',
  name: 'Apple and almonds',
  time: '10:00',
  weekdays: SCHOOL_DAYS,
  items: [
    { foodId: 'apple', grams: 180, household: '1 medium apple' },
    { foodId: 'almonds', grams: 30, household: 'a handful' },
  ],
  notes: ['Pareve. Nothing in it needs a fridge.'],
  prep: ['Pack the apple and a small box of almonds.'],
  more: ['A banana as well', 'A second handful of nuts'],
  substitutions: ['Any fruit with nuts or seeds', 'Dates and walnuts'],
  storage: ['Keeps all day in a school bag.'],
};

export const SCHOOL_LUNCH: MealTemplate = {
  id: 'school-lunch',
  slot: 'lunch',
  name: 'Eggs, tofu, and a large salad',
  time: '12:00',
  weekdays: SCHOOL_DAYS,
  recipeId: 'school-plate',
  estimated: true,
  items: [
    { foodId: 'egg', grams: 100, household: '2 large eggs' },
    { foodId: 'egg-white', grams: 66, household: '2 egg whites' },
    { foodId: 'tofu', grams: 135, household: 'a palm sized piece' },
    { foodId: 'salad', grams: 300, household: 'half a plate or a large bowl' },
    { foodId: 'olives', grams: 30, household: 'about 7 olives' },
  ],
  notes: ['Pareve. Cafeteria portions are estimated, so the log shows a range.'],
  prep: ['Build the plate from the cafeteria: eggs, tofu, salad, olives. Log any oil or dressing you add.'],
  more: ['Another egg or a larger piece of tofu', 'Hummus or tahini with the salad', 'Rice, potatoes, or bread if the cafeteria has them and you are hungry'],
  substitutions: ['No tofu today: two more egg whites or a serving of legumes', 'No eggs today: a larger piece of tofu'],
  storage: ['Cafeteria food needs nothing from home.', 'If you bring eggs or tofu from home, carry them in an insulated bag with two ice packs. Perishable food should not sit warm for more than two hours, or one hour above 32°C.'],
};

/** The meal after school. On gym days eat it about an hour before training; on days off it is a normal meal. */
export const AFTERNOON: MealTemplate = {
  id: 'afternoon',
  slot: 'preworkout',
  name: 'Chicken and rice',
  time: '15:20',
  weekdays: SCHOOL_DAYS,
  recipeId: 'chicken-rice-boxes',
  items: [
    { foodId: 'rice-cooked', grams: 200, household: 'about one and a quarter cups cooked, from 75 g dry', note: 'Cooked weight' },
    { foodId: 'chicken-breast', grams: 120, household: 'a palm sized piece, from about 165 g raw', note: 'Cooked weight' },
  ],
  notes: ['Meat. On training days, eat it about an hour before the home jumps or the gym.'],
  prep: ['Reheat a prepared box until steaming hot, or cook fresh.'],
  more: ['Another 50 to 100 g cooked rice', 'A banana before training'],
  substitutions: ['200 g firm tofu and rice, a pareve meal', '140 g tuna in water instead of chicken', 'Potato, sweet potato, couscous, or pasta instead of rice'],
  storage: ['Cool cooked rice quickly, within about an hour, and refrigerate it. Freeze the boxes you will not eat in the next day or two, and reheat once until steaming hot.', FRIDGE],
};

function dinner(d: Weekday, name: string, protein: [string, number, string], recipeId: string): MealTemplate {
  return {
    id: `dinner-${d}`,
    slot: 'dinner',
    name,
    time: '19:00',
    weekdays: [d],
    recipeId,
    items: [
      { foodId: protein[0], grams: protein[1], household: protein[2], note: 'Cooked weight' },
      { foodId: 'potato', grams: 250, household: '2 to 3 medium potatoes', note: 'Cooked weight' },
      { foodId: 'lentils-cooked', grams: 100, household: 'about half a cup cooked', note: 'Cooked weight' },
      { foodId: 'veg-mixed', grams: 300, household: 'half the plate' },
      { foodId: 'olive-oil', grams: 5, household: 'about one teaspoon', note: 'Cooking oil counts. Log what you use.' },
    ],
    notes: [FOOD_BY_ID[protein[0]]?.kosher === 'meat' ? 'Meat.' : 'Fish, pareve.'],
    prep: ['Cook the protein, potatoes, and vegetables. Serve with the lentils.'],
    more: ['Another 100 g potato or rice', 'More lentils or vegetables', 'Bread with the meal'],
    substitutions: ['Any fish, chicken, turkey, or lean beef', 'Sweet potato or rice instead of potato'],
    storage: ['Refrigerate leftovers within two hours and eat them within three to four days.', FRIDGE],
  };
}

export const DINNERS: MealTemplate[] = [
  dinner(0, 'Salmon, potato, lentils, vegetables', ['salmon', 180, 'a fillet about the size of your hand'], 'sheet-pan-salmon'),
  dinner(1, 'Lean beef, potato, lentils, vegetables', ['beef-lean', 180, 'two palm sized portions'], 'beef-bowl'),
  dinner(2, 'White fish, potato, lentils, vegetables', ['white-fish', 200, 'a large fillet'], 'white-fish-plate'),
  dinner(3, 'Salmon, potato, lentils, vegetables', ['salmon', 180, 'a fillet about the size of your hand'], 'sheet-pan-salmon'),
  dinner(4, 'Lean beef, potato, lentils, vegetables', ['beef-lean', 180, 'two palm sized portions'], 'beef-bowl'),
  dinner(5, 'Turkey, potato, lentils, vegetables', ['turkey-breast', 180, 'two palm sized portions'], 'turkey-plate'),
];

export const EVENING: MealTemplate = {
  id: 'evening-milk',
  slot: 'evening',
  name: 'Milk',
  time: '20:45',
  weekdays: [0, 1, 2, 3, 4],
  items: [{ foodId: 'milk', grams: 300, household: 'a large glass, 300 ml' }],
  notes: ['Dairy. Only when it is past the meat and dairy interval after the last meat meal.'],
  prep: ['Pour a glass.'],
  more: ['A piece of fruit'],
  substitutions: ['Yogurt instead of milk', 'The pareve snack after a meat dinner'],
  storage: [FRIDGE],
};

export const EVENING_PAREVE: MealTemplate = {
  id: 'evening-pareve',
  slot: 'evening',
  name: 'Apple and almonds',
  time: '20:45',
  weekdays: [0, 1, 2, 3, 4],
  items: [
    { foodId: 'apple', grams: 180, household: '1 medium apple' },
    { foodId: 'almonds', grams: 20, household: 'a small handful' },
  ],
  notes: ['Pareve, so it fits after a meat dinner.'],
  prep: ['Wash the apple.'],
  more: ['More almonds or a second fruit'],
  substitutions: ['Any fruit with a few nuts', 'Rice cakes with tahini'],
  storage: ['Keep nuts in a closed jar.'],
};

export const ALL_TEMPLATES: MealTemplate[] = [BREAKFAST, SCHOOL_SNACK, SCHOOL_LUNCH, AFTERNOON, ...DINNERS, EVENING, EVENING_PAREVE];

/**
 * General context shown with the examples, so their total is never read as enough. It is a range for
 * active teenage boys in general, from the 2023 energy equations, not an estimate for one person.
 */
export const EXAMPLE_CONTEXT =
  'Teen athletes often need more than these examples, especially on long training and sport days. For active boys in their mid teens, energy needs commonly run from about 2,800 to well over 4,000 kcal a day, depending on size, growth, and activity. Eat to appetite, use the options for more food, and ask a pediatric sports dietitian for a personal number.';

/** Templates kept for backward compatibility with tests and older imports. */
export const PREWORKOUT: MealTemplate[] = [AFTERNOON];

// ---------- Meat and dairy ----------

export type KosherCategory = 'meat' | 'dairy' | 'pareve';

/** Meat, dairy, or pareve, from the foods in a template. A template never mixes meat and dairy. */
export function templateKosher(t: MealTemplate): KosherCategory {
  const cats = new Set(t.items.map((i) => FOOD_BY_ID[i.foodId]?.kosher ?? 'pareve'));
  if (cats.has('meat')) return 'meat';
  if (cats.has('dairy')) return 'dairy';
  return 'pareve';
}

export interface DayOptions {
  /** Hours waited after meat before dairy. Null switches the check off. */
  meatToDairyHours?: number | null;
  /** Times the athlete set, per slot. */
  times?: Partial<Record<MealSlot, string>>;
}

/**
 * The example meals for a weekday, in time order. When the evening milk would come sooner after a
 * meat meal than the family's interval, the pareve snack is used instead.
 */
export function templatesForDay(weekday: Weekday, templates: MealTemplate[] = ALL_TEMPLATES, opts: DayOptions = {}): MealTemplate[] {
  const timeOf = (t: MealTemplate) => opts.times?.[t.slot] ?? t.time;
  const day = templates.filter((t) => t.weekdays.includes(weekday) && t.id !== EVENING_PAREVE.id);
  // Six hours unless the family set another interval: the most widespread custom, and never too short.
  const hours = opts.meatToDairyHours === undefined ? 6 : opts.meatToDairyHours;
  const out = day.map((t) => {
    if (t.slot !== 'evening' || hours === null || templateKosher(t) !== 'dairy') return t;
    const lastMeat = day.filter((x) => templateKosher(x) === 'meat' && minutesOf(timeOf(x)) <= minutesOf(timeOf(t))).map((x) => minutesOf(timeOf(x)));
    const tooSoon = lastMeat.some((m) => minutesOf(timeOf(t)) - m < hours * 60);
    return tooSoon && templates.some((x) => x.id === EVENING_PAREVE.id) ? EVENING_PAREVE : t;
  });
  return out.sort((a, b) => minutesOf(timeOf(a)) - minutesOf(timeOf(b)));
}

// ---------- Targets ----------

/**
 * A daily target. Since 3.0.0 PeakForm ships no default calorie target: targets only exist when a
 * professional reviewed them (Goals and reviews). The type stays for targets saved by earlier versions.
 */
export interface NutritionTarget {
  weekday: Weekday;
  label: string;
  kcal: number;
  kcalBand: [number, number];
  protein: number;
  proteinRange: [number, number];
  carbs: number;
  fat: number;
}

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
  { label: 'Rice or potatoes', detail: 'One normal serving, about the size of your fist, or more when hungry.', foodId: 'rice-cooked', grams: [110, 150, 200] },
  { label: 'Salad or vegetables', detail: 'A generous serving. Half the plate is a good guide.', foodId: 'salad', grams: [150, 250, 350] },
  { label: 'Challah', detail: 'One or two slices.', foodId: 'challah', grams: [40, 60, 80] },
];

export const SABBATH_NOTES = [
  'A sweet portion after a meal is part of a normal Sabbath. After a meat meal, choose a pareve one.',
  'Eat to appetite at each meal.',
  'Water or a zero calorie drink.',
  'Hosted cooking often uses oil you cannot see. PeakForm adds that as uncertainty, not as a rule.',
  'No guilt and no exercise to make up for food.',
];

/** Unseen cooking oil allowance for hosted and restaurant meals, grams of oil. */
export const HIDDEN_OIL_RANGE: [number, number, number] = [0, 8, 20];
