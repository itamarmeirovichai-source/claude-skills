import { useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../db/db';
import { addWater, deleteFoodLog, addFoodLog, KV, kvGet, kvSet } from '../db/repo';
import { useSettings } from '../ui/state';
import { useTargets, useToday } from '../ui/hooks';
import { Item, Note, PageHead, RangeBar, Section, Sheet, useToast } from '../ui/components';
import { Link, navigate } from '../ui/router';
import { IconCheck, IconWater } from '../ui/icons';
import { addDays, formatDateKey, weekdayOf } from '../domain/dates';
import { dayTarget, trainedOn } from '../domain/fuel';
import { SLOT_LABELS, templatesForDay, type MealTemplate } from '../content/meals';
import { FOOD_BY_ID } from '../content/foods';
import { dayTotals, templateTotals } from '../domain/nutrition';
import { formatRange } from '../domain/portions';
import { logTemplate } from '../services/food';
import type { FoodLog } from '../db/records';
import { isSabbathTime } from '../domain/sabbath';

export function portionSummary(t: MealTemplate, on: Record<string, boolean>): string {
  return t.items
    .filter((i) => !i.optional || (on[i.foodId] ?? i.defaultOn))
    .map((i) => {
      const f = FOOD_BY_ID[i.foodId];
      const name = (f?.name ?? i.foodId).split(',')[0]!.toLowerCase();
      const unit = f?.units?.find((u) => i.grams % u.grams === 0 && i.grams / u.grams <= 6);
      if (unit) {
        const n = i.grams / unit.grams;
        const label = unit.label.replace(/ \(.*\)/, '');
        return `${n} ${label}${n > 1 ? 's' : ''}`;
      }
      return `${i.grams} ${f?.liquid ? 'ml' : 'g'} ${name}`;
    })
    .join(', ');
}

export function EatScreen() {
  const settings = useSettings();
  const today = useToday();
  const [date, setDate] = useState(today);
  const [noteOpen, setNoteOpen] = useState(false);
  const toast = useToast();
  const wd = weekdayOf(date);
  const logs = useLiveQuery(() => db.foodLogs.where('date').equals(date).toArray(), [date]) ?? [];
  const water = useLiveQuery(() => db.waterLogs.where('date').equals(date).toArray(), [date]) ?? [];
  const notes = useLiveQuery(() => db.dayNotes.where('date').equals(date).toArray(), [date]) ?? [];
  const supLogs = useLiveQuery(() => db.supplementLogs.where('date').equals(date).toArray(), [date]) ?? [];
  const optionalOn = useLiveQuery(() => kvGet<Record<string, boolean>>(KV.optionalFoods), []) ?? {};
  const targets = useTargets();
  const sessions = useLiveQuery(() => db.sessions.where('date').equals(date).toArray(), [date]) ?? [];
  const target = dayTarget(targets.find((t) => t.weekday === wd)!, trainedOn(sessions, date));
  const templates = templatesForDay(wd);
  const totals = dayTotals(logs);
  const waterMl = water.filter((w) => w.drink === 'water').reduce((a, w) => a + w.ml, 0);
  const zeroMl = water.filter((w) => w.drink !== 'water').reduce((a, w) => a + w.ml, 0);
  const calciumSupp = supLogs.reduce((a, l) => a + (settings.supplements.find((s) => s.id === l.supplementId)?.calciumMg ?? 0) * l.amount, 0);
  const extra = logs.filter((l) => !templates.some((t) => t.id === l.templateId));
  const isSat = wd === 6;

  return (
    <div data-testid="eat">
      <PageHead
        title="Eat"
        eyebrow={date === today ? 'Today' : formatDateKey(date, { weekday: 'long', day: 'numeric', month: 'short' })}
        end={
          <div className="row">
            <button type="button" className="btn btn-sm btn-outline" onClick={() => setDate(addDays(date, -1))} aria-label="Previous day">
              ‹
            </button>
            <button type="button" className="btn btn-sm btn-outline" onClick={() => setDate(addDays(date, 1))} disabled={date >= today} aria-label="Next day">
              ›
            </button>
          </div>
        }
      />

      <div className="panel stack" data-testid="day-totals">
        <div className="row-between">
          <div>
            <div className="small muted">Calories, estimated range</div>
            <div className="big-number" style={{ fontSize: totals.mid.kcal > 0 ? '1.9rem' : '1.1rem' }} data-testid="kcal-range">
              {totals.mid.kcal > 0 ? formatRange(totals.low.kcal, totals.high.kcal) : 'Nothing logged yet'}
            </div>
          </div>
          <div style={{ textAlign: 'right' }}>
            <div className="small muted">Target range</div>
            <div className="num" style={{ fontWeight: 650 }}>
              {target.kcalBand[0]} to {target.kcalBand[1]}
            </div>
            <div className="small faint">{target.label}</div>
          </div>
        </div>
        {target.fuelKcal > 0 && (
          <p className="small muted" style={{ margin: 0 }} data-testid="training-fuel">
            {target.fuelIncluded
              ? `Includes ${target.fuelKcal} kcal of training fuel, the rice before your workout.`
              : `Base target. The rice before training adds ${target.fuelKcal} kcal once your workout starts. Not training today? Leave the rice out.`}
          </p>
        )}
        <RangeBar low={totals.low.kcal} mid={totals.mid.kcal} high={totals.high.kcal} band={target.kcalBand} max={Math.max(3200, totals.high.kcal)} label={`Calories about ${Math.round(totals.mid.kcal)} of target ${target.kcal}`} />
        <div className="metric-row cols-2" style={{ boxShadow: 'none' }}>
          <div className="metric">
            <div className="m-label">Protein</div>
            <div className="m-value">{Math.round(totals.mid.protein)} g</div>
            <div className="m-sub">at least {target.proteinRange[0]}</div>
          </div>
          <div className="metric">
            <div className="m-label">Carbs</div>
            <div className="m-value">{Math.round(totals.mid.carbs)} g</div>
            <div className="m-sub">about {target.carbs}</div>
          </div>
          <div className="metric">
            <div className="m-label">Fat</div>
            <div className="m-value">{Math.round(totals.mid.fat)} g</div>
            <div className="m-sub">about {target.fat}</div>
          </div>
          <div className="metric">
            <div className="m-label">Fibre</div>
            <div className="m-value">{Math.round(totals.mid.fibre)} g</div>
          </div>
        </div>
        <p className="small muted">
          Calcium {Math.round(totals.mid.calcium + calciumSupp)} mg of about 1,300 mg{calciumSupp ? `, including ${Math.round(calciumSupp)} mg from supplements` : ''}. Water {waterMl} ml{zeroMl ? `, zero calorie drinks ${zeroMl} ml` : ''}.
        </p>
        {totals.mid.calcium + calciumSupp > 2500 && <Note tone="warn">Calcium is above 2,500 mg today. The upper limit for teens is 3,000 mg, and more than needed brings no benefit. Check supplement doses with a parent.</Note>}
      </div>

      <div className="grid-2" style={{ marginTop: 12 }}>
        <button type="button" className="btn btn-outline" onClick={() => navigate(`/eat/log/other?mode=quick&date=${date}`)} data-testid="eat-quick">
          Quick food
        </button>
        <button type="button" className="btn btn-outline" onClick={() => navigate(`/eat/log/other?mode=restaurant&date=${date}`)} data-testid="eat-restaurant">
          Restaurant estimate
        </button>
      </div>

      {isSat ? (
        <Section title="Sabbath">
          <div className="group">
            <Item title="Sabbath plate guide" sub="Discreet, no scale, no special food" to={`/eat/sabbath?date=${date}`} testId="sabbath-guide" />
          </div>
        </Section>
      ) : (
        <Section title="Meals" end={<Link to="/recipes">Recipes</Link>}>
          <div className="group" data-testid="meal-list">
            {templates.map((t) => {
              const done = logs.filter((l) => l.templateId === t.id || (l.slot === t.slot && l.source !== 'manual'));
              const tt = templateTotals(t, optionalOn);
              const quiet = isSabbathTime(date, t.time, settings.sabbath);
              return (
                <div className="item" key={t.id} style={{ display: 'block', opacity: quiet ? 0.6 : 1 }} data-testid={`meal-${t.slot}`}>
                  <div className="row-between" style={{ alignItems: 'baseline' }}>
                    <span className="item-title">{SLOT_LABELS[t.slot]}</span>
                    <span className="num small faint">{t.time}</span>
                  </div>
                  <p className="item-sub">{portionSummary(t, optionalOn)}</p>
                  <p className="item-sub faint">
                    {formatRange(tt.low.kcal, tt.high.kcal, ' kcal')}, protein {Math.round(tt.mid.protein)} g{t.estimated ? ', estimated at school' : ''}
                  </p>
                  {done.length > 0 ? (
                    <div className="row-between" style={{ marginTop: 6 }}>
                      <span className="tag tag-accent">
                        <IconCheck size={14} /> Logged {done[0]!.asPlanned ? 'as planned' : 'with changes'}, {done[0]!.time}
                      </span>
                      <button
                        type="button"
                        className="btn btn-sm btn-ghost"
                        onClick={async () => {
                          const removed = await deleteFoodLog(done[0]!.id);
                          if (removed) toast('Meal removed', { label: 'Undo', run: () => void addFoodLog(removed) });
                        }}
                      >
                        Remove
                      </button>
                    </div>
                  ) : (
                    <div className="row" style={{ marginTop: 8 }}>
                      <button
                        type="button"
                        className="btn btn-sm btn-primary"
                        data-testid={`log-planned-${t.slot}`}
                        onClick={async () => {
                          const l = await logTemplate(date, t);
                          toast(`${SLOT_LABELS[t.slot]} logged`, { label: 'Undo', run: () => void deleteFoodLog(l.id) });
                        }}
                      >
                        <IconCheck size={18} /> Log as planned
                      </button>
                      <Link to={`/eat/log/${t.slot}?date=${date}&mode=template`} className="btn btn-sm btn-outline">
                        Change
                      </Link>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
          <OptionalFoods optionalOn={optionalOn} />
        </Section>
      )}

      {extra.length > 0 && (
        <Section title="Other food">
          <div className="group">
            {extra.map((l) => (
              <LoggedRow key={l.id} l={l} />
            ))}
          </div>
        </Section>
      )}

      <Section title="Drinks">
        <div className="grid-3">
          <button type="button" className="btn btn-outline" onClick={async () => { await addWater(date, 250, 'water'); toast('250 ml water'); }} data-testid="water-250">
            <IconWater size={20} /> 250 ml
          </button>
          <button type="button" className="btn btn-outline" onClick={async () => { await addWater(date, 500, 'water'); toast('500 ml water'); }}>
            <IconWater size={20} /> 500 ml
          </button>
          <button type="button" className="btn btn-outline" onClick={async () => { await addWater(date, 330, 'coke-zero'); toast('Coke Zero logged'); }} data-testid="coke-zero">
            Coke Zero
          </button>
        </div>
        <p className="small muted" style={{ marginTop: 6 }}>Water is the everyday default. Zero calorie drinks are fine to log too.</p>
      </Section>

      <Section title="Notes">
        <div className="group">
          {notes.map((n) => (
            <Item key={n.id} title={n.kind === 'not-hungry' ? 'Not hungry' : n.kind === 'schedule-changed' ? 'Schedule changed' : n.kind === 'ate-out' ? 'Ate out' : 'Note'} sub={n.note || undefined} />
          ))}
          <Item title="Add a day note" sub="Not hungry, schedule changed, or anything useful" onClick={() => setNoteOpen(true)} />
        </div>
      </Section>

      <Section title="Planning">
        <div className="group">
          <Item title="Weekly meal preparation" sub="Shopping list, cooking steps, storage" to="/prep" testId="meal-prep-link" />
          <Item title="Recipes" to="/recipes" />
          <Item title="Restaurant portion guide" to="/recipe/restaurant-guide" />
        </div>
      </Section>

      <Section>
        <details className="disclosure panel">
          <summary>About these targets</summary>
          <div className="small muted stack">
            <p>Targets are ranges and starting points for a fourteen day observation, not a diagnosis. Days within about 100 calories of the target count as equal.</p>
            <p>Insulin rising after a meal is normal. For fat loss, total energy over weeks, enough protein, training quality, sleep, and consistency matter far more than keeping insulin low.</p>
            <p>Carbohydrates around training fuel jumps, sprints, swimming, and lifting. PeakForm never plans fewer than 130 g a day or fewer than 2,000 calories.</p>
            <p>Estimated meals show a range. Weighed food and labels narrow it.</p>
          </div>
        </details>
      </Section>

      <DayNoteSheet open={noteOpen} onClose={() => setNoteOpen(false)} date={date} />
    </div>
  );
}

function OptionalFoods({ optionalOn }: { optionalOn: Record<string, boolean> }) {
  const opts = [
    { id: 'berries-frozen', label: 'Frozen berries at breakfast', def: true },
    { id: 'protein-powder', label: 'Half scoop protein powder at breakfast', def: false },
  ];
  return (
    <details className="disclosure" style={{ marginTop: 6 }}>
      <summary className="small">Optional breakfast items</summary>
      <div className="group">
        {opts.map((o) => {
          const on = optionalOn[o.id] ?? o.def;
          return (
            <label className="switch-row" key={o.id}>
              <span className="grow">{o.label}</span>
              <span className="toggle">
                <input type="checkbox" role="switch" checked={on} onChange={(e) => void kvSet(KV.optionalFoods, { ...optionalOn, [o.id]: e.target.checked })} />
              </span>
            </label>
          );
        })}
      </div>
      <p className="small muted" style={{ marginTop: 6 }}>Protein powder is optional. Only add it when food protein is short that day.</p>
    </details>
  );
}

function LoggedRow({ l }: { l: FoodLog }) {
  const toast = useToast();
  const t = dayTotals([l]);
  const photo = useLiveQuery(async () => (l.photoId ? await db.photos.get(l.photoId) : undefined), [l.photoId]);
  return (
    <div className="item" style={{ alignItems: 'flex-start' }}>
      {photo && <img src={photo.dataUrl} alt="Meal photo" width={48} height={48} style={{ borderRadius: 8, objectFit: 'cover' }} />}
      <span className="item-main">
        <span className="item-title" style={{ display: 'block' }}>
          {l.slot === 'other' || l.slot === 'snack' ? l.items.map((i) => i.name).join(', ') : SLOT_LABELS[l.slot as keyof typeof SLOT_LABELS] ?? l.slot}
        </span>
        <span className="item-sub" style={{ display: 'block' }}>
          {l.time}, {formatRange(t.low.kcal, t.high.kcal, ' kcal')}, {l.source === 'restaurant' ? 'restaurant estimate' : l.items.some((i) => i.estimate.confidence === 'low') ? 'estimated by eye' : 'weighed or label'}
        </span>
      </span>
      <button
        type="button"
        className="btn btn-sm btn-ghost"
        onClick={async () => {
          const removed = await deleteFoodLog(l.id);
          if (removed) toast('Removed', { label: 'Undo', run: () => void addFoodLog(removed) });
        }}
      >
        Remove
      </button>
    </div>
  );
}

function DayNoteSheet({ open, onClose, date }: { open: boolean; onClose: () => void; date: string }) {
  const [kind, setKind] = useState<'not-hungry' | 'schedule-changed' | 'ate-out' | 'other'>('not-hungry');
  const [note, setNote] = useState('');
  return (
    <Sheet open={open} onClose={onClose} title="Day note">
      <div className="stack">
        <div className="chips">
          {(
            [
              ['not-hungry', 'Not hungry'],
              ['schedule-changed', 'Schedule changed'],
              ['ate-out', 'Ate out'],
              ['other', 'Other'],
            ] as const
          ).map(([k, label]) => (
            <button key={k} type="button" className="chip" aria-pressed={kind === k} onClick={() => setKind(k)}>
              {label}
            </button>
          ))}
        </div>
        <textarea className="input" value={note} onChange={(e) => setNote(e.target.value)} maxLength={2000} placeholder="Optional details" />
        <p className="small muted">This is useful context for the weekly review. There is nothing to make up for.</p>
        <button
          type="button"
          className="btn btn-primary btn-block"
          onClick={async () => {
            const t = Date.now();
            await db.dayNotes.put({ id: `note-${t}`, createdAt: t, updatedAt: t, date, kind, note });
            setNote('');
            onClose();
          }}
        >
          Save note
        </button>
      </div>
    </Sheet>
  );
}
