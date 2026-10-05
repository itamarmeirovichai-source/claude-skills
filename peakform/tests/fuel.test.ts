import { describe, expect, it } from 'vitest';
import { BASELINE_TARGETS, NUTRITION_FLOORS, PREWORKOUT } from '../src/content/meals';
import { dayTarget, trainedOn, trainingFuel } from '../src/domain/fuel';

const target = (wd: number) => BASELINE_TARGETS.find((t) => t.weekday === wd)!;

describe('training fuel', () => {
  it('is the rice before training, and nothing on the rest day', () => {
    expect(trainingFuel(1)).toEqual({ kcal: 325, carbs: 71 });
    expect(trainingFuel(2).kcal).toBe(286);
    expect(trainingFuel(5).kcal).toBe(390);
    expect(trainingFuel(6)).toEqual({ kcal: 0, carbs: 0 });
    for (const t of PREWORKOUT) expect(t.items.filter((i) => i.trainingFuel).map((i) => i.foodId)).toEqual(['rice-cooked']);
  });

  it('is left out of the target until the main workout starts, so a missed workout still means a deficit', () => {
    const rest = dayTarget(target(1), false);
    expect(rest.kcal).toBe(2450 - 325);
    expect(rest.kcalBand).toEqual([2350 - 325, 2550 - 325]);
    expect(rest.carbs).toBe(260 - 71);
    expect(rest.fuelIncluded).toBe(false);
    const trained = dayTarget(target(1), true);
    expect(trained.kcal).toBe(2450);
    expect(trained.fuelIncluded).toBe(true);
    expect(trained.baseKcal).toBe(2125);
  });

  it('never goes below the calorie and carbohydrate floors', () => {
    const low = dayTarget({ ...target(2), kcal: 2100, kcalBand: [2000, 2200], carbs: 140 }, false);
    expect(low.kcal).toBeGreaterThanOrEqual(NUTRITION_FLOORS.kcal);
    expect(low.kcalBand[0]).toBeGreaterThanOrEqual(NUTRITION_FLOORS.kcal);
    expect(low.carbs).toBeGreaterThanOrEqual(NUTRITION_FLOORS.carbs);
    expect(dayTarget(target(6), false).kcal).toBe(2250);
  });

  it('counts a started or finished main workout, but not a morning session or an abandoned one', () => {
    const d = '2026-10-05';
    expect(trainedOn([{ date: d, session: 'main', status: 'active' }], d)).toBe(true);
    expect(trainedOn([{ date: d, session: 'main', status: 'done' }], d)).toBe(true);
    expect(trainedOn([{ date: d, session: 'main', status: 'abandoned' }], d)).toBe(false);
    expect(trainedOn([{ date: d, session: 'morning', status: 'done' }], d)).toBe(false);
    expect(trainedOn([{ date: '2026-10-04', session: 'main', status: 'done' }], d)).toBe(false);
  });
});
