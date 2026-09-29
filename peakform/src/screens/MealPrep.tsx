import { useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { KV, kvGet, kvSet } from '../db/repo';
import { COOKING_TEMPERATURES, DEFAULT_PREP_DAYS, PREP_STEPS, RAW_COOKED_NOTE, RECIPES, RECIPE_BY_ID, SHOPPING_LIST, scaleShopping, type Recipe } from '../content/recipes';
import { FOOD_BY_ID } from '../content/foods';
import { Item, Note, PageHead, Section, Stepper } from '../ui/components';
import { itemFromGrams, sumItems, formatRange } from '../domain/portions';
import { mediaFor } from '../content/mediaFor';

interface PrepState {
  days: number;
  bought: Record<string, boolean>;
  done: Record<string, boolean>;
  qty: Record<string, number>;
}

const EMPTY: PrepState = { days: DEFAULT_PREP_DAYS, bought: {}, done: {}, qty: {} };

function unitLabel(n: number, unit: string) {
  if (unit === 'g' && n >= 1000) return `${Math.round(n / 100) / 10} kg`;
  if (unit === 'ml' && n >= 1000) return `${Math.round(n / 100) / 10} l`;
  return unit === 'pcs' ? `${n}` : `${n} ${unit}`;
}

export function MealPrepScreen() {
  const state = useLiveQuery(() => kvGet<PrepState>(KV.mealPrep), []) ?? EMPTY;
  const save = (s: PrepState) => void kvSet(KV.mealPrep, s);
  const sections = [...new Set(SHOPPING_LIST.map((i) => i.section))];
  const boughtCount = SHOPPING_LIST.filter((i) => state.bought[i.id]).length;
  const doneCount = PREP_STEPS.filter((s) => state.done[s.id]).length;
  return (
    <div data-testid="meal-prep">
      <PageHead title="Meal preparation" eyebrow={`${state.days} training days`} backTo="/eat" />
      <Stepper label="Training days to prepare" value={state.days} onChange={(v) => save({ ...state, days: v ?? DEFAULT_PREP_DAYS, qty: {} })} min={1} max={7} testId="prep-days" />
      <p className="hint">Quantities update when you change the number of days. Tap a quantity to adjust it.</p>

      <Section title={`Shopping list, ${boughtCount} of ${SHOPPING_LIST.length}`} end={<button type="button" className="btn btn-ghost btn-sm" onClick={() => save({ ...state, bought: {} })}>Clear</button>}>
        {sections.map((sec) => (
          <div key={sec} style={{ marginBottom: 10 }}>
            <div className="small muted" style={{ margin: '0 4px 4px', fontWeight: 600 }}>
              {sec}
            </div>
            <div className="group">
              {SHOPPING_LIST.filter((i) => i.section === sec).map((i) => {
                const q = state.qty[i.id] ?? scaleShopping(i, state.days);
                return (
                  <label className="item" key={i.id} style={{ cursor: 'pointer' }}>
                    <input type="checkbox" checked={!!state.bought[i.id]} onChange={(e) => save({ ...state, bought: { ...state.bought, [i.id]: e.target.checked } })} className="check" data-testid={`buy-${i.id}`} />
                    <span className="item-main" style={{ textDecoration: state.bought[i.id] ? 'line-through' : undefined, opacity: state.bought[i.id] ? 0.6 : 1 }}>
                      {i.name}
                    </span>
                    {!i.fixed && (
                      <input
                        className="input num"
                        style={{ width: 92, minHeight: 36, padding: '4px 8px', textAlign: 'right' }}
                        inputMode="numeric"
                        aria-label={`Quantity of ${i.name} in ${i.unit || 'items'}`}
                        value={q}
                        onClick={(e) => e.preventDefault()}
                        onChange={(e) => save({ ...state, qty: { ...state.qty, [i.id]: Number(e.target.value.replace(/\D/g, '')) || 0 } })}
                      />
                    )}
                    {!i.fixed && <span className="small faint" style={{ width: 28 }}>{i.unit === 'pcs' ? '' : i.unit}</span>}
                    {i.fixed && <span className="small faint">as needed</span>}
                  </label>
                );
              })}
            </div>
          </div>
        ))}
        <p className="small muted">Totals: {SHOPPING_LIST.filter((i) => !i.fixed).map((i) => `${i.name.split(',')[0]} ${unitLabel(state.qty[i.id] ?? scaleShopping(i, state.days), i.unit)}`).slice(0, 4).join(', ')}, and more.</p>
      </Section>

      <Section title={`Preparation, ${doneCount} of ${PREP_STEPS.length}`} end={<button type="button" className="btn btn-ghost btn-sm" onClick={() => save({ ...state, done: {} })}>Reset</button>}>
        <div className="group">
          {PREP_STEPS.map((s, i) => (
            <label className="item" key={s.id} style={{ alignItems: 'flex-start', cursor: 'pointer' }}>
              <input type="checkbox" checked={!!state.done[s.id]} onChange={(e) => save({ ...state, done: { ...state.done, [s.id]: e.target.checked } })} className="check" style={{ marginTop: 2 }} />
              <span className="item-main">
                <span className="item-title" style={{ display: 'block' }}>
                  {i + 1}. {s.title}
                </span>
                <span className="item-sub" style={{ display: 'block' }}>{s.detail}</span>
              </span>
            </label>
          ))}
        </div>
      </Section>

      <Section title="Food safety">
        <div className="group">
          {COOKING_TEMPERATURES.map((c) => (
            <Item key={c.food} title={c.food} end={`${c.celsius}°C`} />
          ))}
        </div>
        <p className="small muted" style={{ marginTop: 8 }}>{RAW_COOKED_NOTE}</p>
        <p className="small muted">Source: USDA and FoodSafety.gov guidance. Follow local food safety advice if it differs.</p>
      </Section>

      <Section title="Recipes">
        <div className="group">
          {RECIPES.map((r) => (
            <Item key={r.id} to={`/recipe/${r.id}`} title={r.name} sub={r.summary} />
          ))}
        </div>
      </Section>
    </div>
  );
}

export function RecipesScreen() {
  return (
    <div>
      <PageHead title="Recipes" backTo="/eat" />
      <div className="group">
        {RECIPES.map((r) => (
          <Item key={r.id} to={`/recipe/${r.id}`} title={r.name} sub={r.summary} />
        ))}
      </div>
    </div>
  );
}

function recipeNutrition(r: Recipe, servings: number) {
  const items = r.ingredients.filter((i) => i.foodId && i.grams).map((i) => itemFromGrams(FOOD_BY_ID[i.foodId!]!, (i.grams! * servings) / r.servings, 'template'));
  return sumItems(items);
}

export function RecipeScreen({ id }: { id: string }) {
  const r = RECIPE_BY_ID[id];
  const [servings, setServings] = useState<number | null>(r?.servings ?? 1);
  if (!r) return <PageHead title="Recipe not found" backTo="/recipes" />;
  const s = servings ?? r.servings;
  const k = s / r.servings;
  const perServing = recipeNutrition(r, 1);
  const media = mediaFor(r.id);
  const soup = r.id === 'lentil-soup';
  return (
    <div data-testid="recipe">
      <PageHead title={r.name} eyebrow={suitability(r.suitableFor)} backTo="/recipes" />
      <p className="muted">{r.summary}</p>
      {!r.guideOnly && (
        <Section title="Servings">
          <Stepper label="Servings" value={servings} onChange={setServings} min={1} max={24} testId="recipe-servings" />
        </Section>
      )}
      <Section title="Ingredients">
        <div className="group">
          {r.ingredients.map((i) => (
            <Item key={i.name} title={i.name} end={i.grams && !r.guideOnly ? `${Math.round(i.grams * k)} g${i.state && i.state !== 'as sold' ? ` ${i.state}` : ''}` : i.amount} />
          ))}
        </div>
        <p className="small muted" style={{ marginTop: 8 }}>{r.weightNote}</p>
      </Section>
      {!r.guideOnly && (
        <Section title="Approximate nutrition per serving">
          <div className="panel small">
            {soup ? (
              <p>About 180 to 220 kcal, 10 to 13 g protein, 30 to 36 g carbohydrate, and 2 to 3 g fat per 450 g serving. Calculated from the whole pot of about 2.7 kg.</p>
            ) : (
              <p>
                {formatRange(perServing.low.kcal, perServing.high.kcal, ' kcal')}, protein {formatRange(perServing.low.protein, perServing.high.protein, ' g')}, carbohydrate {formatRange(perServing.low.carbs, perServing.high.carbs, ' g')}, fat {formatRange(perServing.low.fat, perServing.high.fat, ' g')}.
              </p>
            )}
            <p className="muted" style={{ marginTop: 4 }}>Labels and cooking change the real numbers. Ranges are honest about that.</p>
          </div>
        </Section>
      )}
      <Section title="Steps">
        <div className="panel">
          <ol className="steps">
            {r.steps.map((x) => (
              <li key={x}>{x}</li>
            ))}
          </ol>
        </div>
      </Section>
      <Section title="Storage and reheating">
        <div className="panel">
          <ul className="bullets">
            {[...r.storage, ...r.reheating].map((x) => (
              <li key={x}>{x}</li>
            ))}
          </ul>
        </div>
      </Section>
      <Section title="Food safety">
        <Note tone="warn">
          <ul className="bullets">
            {r.foodSafety.map((x) => (
              <li key={x}>{x}</li>
            ))}
          </ul>
        </Note>
      </Section>
      <Section title="Substitutions">
        <div className="panel">
          <ul className="bullets">
            {r.substitutions.map((x) => (
              <li key={x}>{x}</li>
            ))}
          </ul>
        </div>
      </Section>
      {media.length > 0 && (
        <Section title="External video">
          <div className="group">
            {media.map((m) => (
              <a key={m.id} className="item" href={m.url} target="_blank" rel="noopener noreferrer">
                <span className="item-main">
                  <span className="item-title" style={{ display: 'block' }}>{m.title}</span>
                  <span className="item-sub" style={{ display: 'block' }}>{m.channel}. {m.reviewerNote}</span>
                </span>
              </a>
            ))}
          </div>
          <p className="small muted" style={{ marginTop: 6 }}>Opens outside PeakForm. The recipe above is complete without it.</p>
        </Section>
      )}
    </div>
  );
}

function suitability(xs: string[]): string {
  const t = xs.join(', ');
  return t.charAt(0).toUpperCase() + t.slice(1);
}
