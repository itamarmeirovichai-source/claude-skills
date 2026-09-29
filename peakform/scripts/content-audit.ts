// Machine readable audit of every exercise, plan item, meal, recipe, and source.
// Usage: npx tsx scripts/content-audit.ts [out-file]
import { writeFileSync } from 'node:fs';
import { LIBRARY } from '../src/content/library';
import { BASELINE_PLAN } from '../src/content/plan';
import { ALL_TEMPLATES, BASELINE_TARGETS, NUTRITION_FLOORS, SABBATH_PLATE } from '../src/content/meals';
import { RECIPES, SHOPPING_LIST, PREP_STEPS } from '../src/content/recipes';
import { SOURCES } from '../src/content/sources';
import { MEDIA, CLAIM_REVIEWS } from '../src/content/media';
import { MUSCLES } from '../src/content/muscles';
import { FOODS } from '../src/content/foods';
import { templateTotals } from '../src/domain/nutrition';
import { coverageFrom, focusChecks, planCoverageInputs, shoulderOverlap } from '../src/domain/coverage';

const out = process.argv[2] ?? 'docs/content-audit.json';
const byId = Object.fromEntries(LIBRARY.map((e) => [e.id, e]));
const lookup = (id: string) => {
  const e = byId[id];
  return e ? { name: e.name, kind: e.kind, primary: e.muscles.primary, secondary: e.muscles.secondary, fatigueOverlap: e.fatigueOverlap } : undefined;
};
const r = (n: number) => Math.round(n);
const days = BASELINE_PLAN.days.map((d) => {
  const meals = ALL_TEMPLATES.filter((t) => t.weekdays.includes(d.weekday));
  const total = meals.reduce((a, t) => {
    const x = templateTotals(t).mid;
    return { kcal: a.kcal + x.kcal, protein: a.protein + x.protein, carbs: a.carbs + x.carbs, fat: a.fat + x.fat };
  }, { kcal: 0, protein: 0, carbs: 0, fat: 0 });
  const target = BASELINE_TARGETS.find((t) => t.weekday === d.weekday)!;
  return {
    weekday: d.weekday,
    title: d.title,
    rest: d.isRest,
    items: d.items.map((i) => ({ id: i.id, session: i.session, exercise: byId[i.exerciseId]?.name ?? i.exerciseId, sets: i.sets, target: i.target, per: i.per ?? null, restSec: i.restSec, rir: i.rir ?? null, tempo: i.tempo ?? null, rpe: i.rpe ?? null, notes: i.notes })),
    defaultMealsTotal: { kcal: r(total.kcal), protein: r(total.protein), carbs: r(total.carbs), fat: r(total.fat) },
    target: { kcal: target.kcal, band: target.kcalBand, protein: target.protein, carbs: target.carbs, fat: target.fat },
  };
});
const cov = coverageFrom(planCoverageInputs(BASELINE_PLAN.days), lookup);
const audit = {
  generated: new Date().toISOString(),
  counts: { exercises: LIBRARY.length, muscles: MUSCLES.length, planItems: BASELINE_PLAN.days.reduce((a, d) => a + d.items.length, 0), mealTemplates: ALL_TEMPLATES.length, recipes: RECIPES.length, foods: FOODS.length, sources: SOURCES.length, media: MEDIA.length },
  exercises: LIBRARY.map((e) => ({
    id: e.id,
    name: e.name,
    kind: e.kind,
    primary: e.muscles.primary,
    secondary: e.muscles.secondary,
    pattern: e.movementPattern,
    laterality: e.laterality,
    logSides: e.logSides,
    loadIncrement: e.loadIncrement,
    visual: { poses: e.visual.poses?.length ?? 0, diagram: e.visual.diagram?.kind ?? null },
    stopRules: e.stopRules.length,
    substitutions: [e.easierSubstitution.name, e.equipmentSubstitution.name, ...(e.otherSubstitutions ?? []).map((s) => s.name)],
    media: MEDIA.filter((m) => m.targetId === e.id).map((m) => ({ channel: m.channel, url: m.url, status: m.reviewStatus })),
  })),
  plan: days,
  coverage: {
    weights: { primarySet: 1, secondarySet: 0.5, activity: 'exposure only' },
    focus: focusChecks(cov),
    perMuscle: Object.values(cov).map((c) => ({ muscle: c.muscle, direct: c.direct, indirect: c.indirect, exposures: c.exposures })),
    shoulderNotes: shoulderOverlap(planCoverageInputs(BASELINE_PLAN.days), lookup).notes,
  },
  nutrition: { floors: NUTRITION_FLOORS, targets: BASELINE_TARGETS, sabbathPlate: SABBATH_PLATE },
  meals: ALL_TEMPLATES.map((t) => ({ id: t.id, slot: t.slot, time: t.time, weekdays: t.weekdays, items: t.items, estimatedAtSchool: !!t.estimated })),
  recipes: RECIPES.map((x) => ({ id: x.id, name: x.name, servings: x.servings, ingredients: x.ingredients, suitableFor: x.suitableFor })),
  mealPrep: { shopping: SHOPPING_LIST, steps: PREP_STEPS },
  sources: SOURCES.map((s) => ({ id: s.id, title: s.title, url: s.url, access: s.access, topic: s.topic })),
  claimReviews: CLAIM_REVIEWS,
};
writeFileSync(out, JSON.stringify(audit, null, 2));
console.log(`Audit written to ${out}.`, audit.counts);
console.log('Default meals vs targets:', days.map((d) => `${d.title}: ${d.defaultMealsTotal.kcal} kcal / target ${d.target.kcal}; protein ${d.defaultMealsTotal.protein} / ${d.target.protein}; carbs ${d.defaultMealsTotal.carbs} / ${d.target.carbs}; fat ${d.defaultMealsTotal.fat} / ${d.target.fat}`).join('\n'));
console.log('Focus checks:', JSON.stringify(audit.coverage.focus.map((f) => [f.label, f.present, f.directSets, f.indirectSets, f.exposures])));
