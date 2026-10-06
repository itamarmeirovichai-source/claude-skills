import { useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../db/db';
import { FOOD_BY_ID } from '../content/foods';
import { HIDDEN_OIL_RANGE, SABBATH_NOTES, SABBATH_PLATE } from '../content/meals';
import { formatRange, hiddenOilItem, itemFromRange, itemFromPortion, sumItems } from '../domain/portions';
import { PageHead, Section, Seg, useToast } from '../ui/components';
import { useToday } from '../ui/hooks';
import { logItems } from '../services/food';
import { navigate } from '../ui/router';
import { formatDateKey, weekdayOf, addDays } from '../domain/dates';
import type { FoodLogItem } from '../db/records';

// A discreet plate guide for hosted Sabbath meals, plus a two tap way to log them after the Sabbath.

type Size = 'smaller' | 'guide' | 'bigger';
const SCALE: Record<Size, number> = { smaller: 0.75, guide: 1, bigger: 1.35 };

function plateItems(size: Size): FoodLogItem[] {
  const k = SCALE[size];
  return [
    ...SABBATH_PLATE.map((p) => itemFromRange(FOOD_BY_ID[p.foodId]!, [p.grams[0] * k, p.grams[1] * k, p.grams[2] * k], `${p.label} (plate guide)`)),
    hiddenOilItem(HIDDEN_OIL_RANGE),
  ];
}

export function SabbathPlateScreen({ date }: { date: string | null }) {
  const today = useToday();
  const toast = useToast();
  const wd = weekdayOf(today);
  const d = date ?? (wd === 6 ? today : wd === 0 ? addDays(today, -1) : today);
  const logged = useLiveQuery(() => db.foodLogs.where('date').equals(d).filter((f) => f.slot === 'sabbath').toArray(), [d]) ?? [];
  const [meals, setMeals] = useState<Size[]>(['guide', 'guide']);
  const [sweet, setSweet] = useState(true);
  const all = meals.flatMap((m) => plateItems(m));
  const withSweet = sweet ? [...all, itemFromPortion(FOOD_BY_ID['sweet-portion']!, 'cupped-hand', 2)] : all;
  const t = sumItems(withSweet);
  return (
    <div data-testid="sabbath">
      <PageHead title="Sabbath plate" eyebrow="Guide for hosted meals" backTo="/eat" />
      <Section title="Each plate">
        <div className="group">
          {SABBATH_PLATE.map((p) => (
            <div className="item" key={p.label}>
              <span className="item-main">
                <span className="item-title" style={{ display: 'block' }}>{p.label}</span>
                <span className="item-sub" style={{ display: 'block' }}>{p.detail}</span>
              </span>
            </div>
          ))}
        </div>
        <ul className="bullets small muted" style={{ marginTop: 10 }}>
          {SABBATH_NOTES.map((n) => (
            <li key={n}>{n}</li>
          ))}
        </ul>
      </Section>

      <Section title={`Log ${formatDateKey(d, { weekday: 'long', day: 'numeric', month: 'short' })}`}>
        {logged.length > 0 ? (
          <p className="muted">{logged.length} Sabbath meal{logged.length === 1 ? ' is' : 's are'} already logged for this day.</p>
        ) : (
          <div className="stack">
            <p className="small muted">After the Sabbath, tap how each main meal compared with the guide. Nothing needs weighing.</p>
            {meals.map((m, i) => (
              <div key={i}>
                <div className="stepper-label">
                  <span>Meal {i + 1}</span>
                  {meals.length > 1 && (
                    <button type="button" className="btn btn-sm btn-ghost" onClick={() => setMeals(meals.filter((_, j) => j !== i))}>
                      Remove
                    </button>
                  )}
                </div>
                <Seg label={`Meal ${i + 1} size`} value={m} onChange={(v) => setMeals(meals.map((x, j) => (j === i ? v : x)))} options={[{ value: 'smaller', label: 'Smaller' }, { value: 'guide', label: 'Like the guide' }, { value: 'bigger', label: 'Bigger' }]} />
              </div>
            ))}
            {meals.length < 4 && (
              <button type="button" className="btn btn-outline btn-sm" onClick={() => setMeals([...meals, 'guide'])}>
                Add another meal
              </button>
            )}
            <label className="switch-row" style={{ padding: 0 }}>
              <span>One planned sweet portion</span>
              <span className="toggle">
                <input type="checkbox" role="switch" checked={sweet} onChange={(e) => setSweet(e.target.checked)} />
              </span>
            </label>
            <div className="note">
              <strong>
                {formatRange(t.low.kcal, t.high.kcal, ' kcal')} for the day, estimated
              </strong>
              Hosted meals are uncertain, so the range is wide on purpose. It is an estimate, not a limit. Add breakfast or anything else from the Eat screen.
            </div>
            <button
              type="button"
              className="btn btn-primary btn-large btn-block"
              data-testid="log-sabbath-meals"
              onClick={async () => {
                for (const [i, m] of meals.entries()) {
                  const items = plateItems(m);
                  if (sweet && i === 0) items.push(itemFromPortion(FOOD_BY_ID['sweet-portion']!, 'cupped-hand', 2));
                  await logItems(d, 'sabbath', items, { source: 'sabbath', templateId: 'sabbath-plate', asPlanned: m === 'guide', hiddenOil: HIDDEN_OIL_RANGE, time: i === 0 ? '12:30' : '17:00' });
                }
                toast('Sabbath meals logged');
                navigate('/eat');
              }}
            >
              Log {meals.length} meal{meals.length === 1 ? '' : 's'}
            </button>
          </div>
        )}
      </Section>
    </div>
  );
}
