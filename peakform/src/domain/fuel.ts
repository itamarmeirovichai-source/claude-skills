import { food } from '../content/foods';
import { NUTRITION_FLOORS, PREWORKOUT, type NutritionTarget } from '../content/meals';
import type { Weekday } from '../content/plan';
import type { WorkoutSession } from '../db/records';
import type { DateKey } from './dates';

// Food that does not depend on training. Each day's target is the base, the food you eat whether
// or not you train. The rice before training is training fuel: it is added to the target only
// once that day's main workout has started. A missed workout means a smaller target, so the
// plan still loses fat on that day.

export interface Fuel {
  kcal: number;
  carbs: number;
}

/** The training fuel in the meal before training on a weekday. Zero on days without one. */
export function trainingFuel(weekday: Weekday): Fuel {
  const tpl = PREWORKOUT.find((t) => t.weekdays.includes(weekday));
  const items = tpl?.items.filter((i) => i.trainingFuel) ?? [];
  return items.reduce(
    (acc, i) => {
      const f = food(i.foodId);
      return { kcal: acc.kcal + Math.round((f.per100.kcal * i.grams) / 100), carbs: acc.carbs + Math.round((f.per100.carbs * i.grams) / 100) };
    },
    { kcal: 0, carbs: 0 },
  );
}

/** A main workout was started or finished on the date. Abandoned sessions do not count. */
export function trainedOn(sessions: Pick<WorkoutSession, 'date' | 'session' | 'status'>[], date: DateKey): boolean {
  return sessions.some((s) => s.date === date && s.session === 'main' && s.status !== 'abandoned');
}

export interface DayTarget extends NutritionTarget {
  /** Training fuel for the day, in kcal. */
  fuelKcal: number;
  /** Whether the fuel is included because the workout started. */
  fuelIncluded: boolean;
  /** The target without training fuel. */
  baseKcal: number;
}

/** The day's target: the base, plus the training fuel once the main workout has started. Never below the floors. */
export function dayTarget(target: NutritionTarget, trained: boolean): DayTarget {
  const fuel = trainingFuel(target.weekday);
  const baseKcal = Math.max(NUTRITION_FLOORS.kcal, target.kcal - fuel.kcal);
  if (trained || fuel.kcal === 0) return { ...target, fuelKcal: fuel.kcal, fuelIncluded: fuel.kcal > 0, baseKcal };
  const shift = target.kcal - baseKcal;
  return {
    ...target,
    kcal: baseKcal,
    kcalBand: [Math.max(NUTRITION_FLOORS.kcal, target.kcalBand[0] - shift), target.kcalBand[1] - shift],
    carbs: Math.max(NUTRITION_FLOORS.carbs, target.carbs - fuel.carbs),
    fuelKcal: fuel.kcal,
    fuelIncluded: false,
    baseKcal,
  };
}
