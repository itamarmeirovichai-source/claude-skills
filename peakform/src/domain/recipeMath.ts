import { FOOD_BY_ID } from '../content/foods';
import type { Recipe, RecipeIngredient } from '../content/recipes';
import { itemFromGrams, sumItems, type Totals } from './portions';

// Recipe scaling and nutrition. Ingredient grams scale with the number of servings, and nutrition
// comes only from ingredients that map to a food in the list, oil included.

/** Grams of an ingredient for a number of servings, or null when the recipe gives no weight. */
export function scaledGrams(r: Recipe, i: RecipeIngredient, servings: number): number | null {
  if (!i.grams) return null;
  return Math.round(((i.grams * servings) / r.servings) * 10) / 10;
}

/** Nutrition of the recipe for a number of servings, as a range. */
export function recipeNutrition(r: Recipe, servings: number): Totals {
  const items = r.ingredients.filter((i) => i.foodId && i.grams && FOOD_BY_ID[i.foodId]).map((i) => itemFromGrams(FOOD_BY_ID[i.foodId!]!, scaledGrams(r, i, servings)!, 'template'));
  return sumItems(items);
}
