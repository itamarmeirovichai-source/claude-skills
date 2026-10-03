import { useEffect, useMemo, useRef, useState } from 'react';
import { db } from '../db/db';
import { FOODS, FOOD_BY_ID, type Food } from '../content/foods';
import { ALL_TEMPLATES, HIDDEN_OIL_RANGE, SLOT_LABELS, templatesForDay } from '../content/meals';
import type { FoodLog, FoodLogItem } from '../db/records';
import { CONFIDENCE_LABELS, PORTIONS, formatRange, hiddenOilItem, itemFromGrams, itemFromPortion, itemFromTotals, sumItems, type PortionKey } from '../domain/portions';
import { templateItems } from '../domain/nutrition';
import { weekdayOf } from '../domain/dates';
import { PageHead, Note, Section, Seg, Sheet, Stepper, Toggle, useOnline, useToast } from '../ui/components';
import { IconCamera, IconClose, IconPlus } from '../ui/icons';
import { navigate } from '../ui/router';
import { useToday } from '../ui/hooks';
import { PortionIcon } from '../svg/PortionIcons';
import { logItems, optionalFoodsOn } from '../services/food';
import { compressImage } from '../lib/device';
import { uid } from '../lib/id';

type Slot = FoodLog['slot'];
const SLOTS: Slot[] = ['breakfast', 'lunch', 'preworkout', 'dinner', 'evening', 'sabbath', 'snack', 'other'];
const slotLabel = (s: Slot) => (s === 'snack' ? 'Snack' : s === 'other' ? 'Other' : SLOT_LABELS[s]);

export function FoodLogScreen({ slot, date, mode }: { slot: string; date: string | null; mode: string | null }) {
  const today = useToday();
  const d = date ?? today;
  const toast = useToast();
  const [s, setS] = useState<Slot>((SLOTS as string[]).includes(slot) ? (slot as Slot) : 'other');
  const restaurant = mode === 'restaurant';
  const tpl = mode === 'template' ? templatesForDay(weekdayOf(d)).find((t) => t.slot === s) : undefined;
  const [items, setItems] = useState<FoodLogItem[]>([]);
  const [pickerOpen, setPickerOpen] = useState(false);
  const [editIdx, setEditIdx] = useState<number | null>(null);
  const [oil, setOil] = useState(restaurant);
  const [note, setNote] = useState('');
  const [photo, setPhoto] = useState<{ dataUrl: string; bytes: number } | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  const tplId = tpl?.id;
  useEffect(() => {
    const t = ALL_TEMPLATES.find((x) => x.id === tplId);
    if (!t) return;
    void optionalFoodsOn().then((on) => setItems(templateItems(t, on)));
  }, [tplId]);

  const all = oil ? [...items, hiddenOilItem(HIDDEN_OIL_RANGE)] : items;
  const t = sumItems(all);
  const lowestConfidence = all.some((i) => i.estimate.confidence === 'low') ? 'low' : all.some((i) => i.estimate.confidence === 'medium') ? 'medium' : 'high';
  const original = tpl ? templateItems(tpl) : [];
  const unchanged = tpl && JSON.stringify(items.map((i) => [i.foodId, i.estimate.gramsMid])) === JSON.stringify(original.map((i) => [i.foodId, i.estimate.gramsMid]));

  const save = async () => {
    let photoId: string | null = null;
    if (photo) {
      photoId = uid('photo');
      const tm = Date.now();
      await db.photos.put({ id: photoId, createdAt: tm, updatedAt: tm, mime: 'image/jpeg', bytes: photo.bytes, dataUrl: photo.dataUrl });
    }
    await logItems(d, s, all, {
      source: restaurant ? 'restaurant' : tpl ? 'template' : all.some((i) => i.estimate.method === 'hand' || i.estimate.method === 'household') ? 'estimate' : 'manual',
      templateId: tpl?.id ?? null,
      asPlanned: !!unchanged,
      photoId,
      note,
      hiddenOil: oil ? HIDDEN_OIL_RANGE : null,
    });
    toast('Food logged');
    navigate('/eat');
  };

  return (
    <div data-testid="food-logger">
      <PageHead title={restaurant ? 'Restaurant estimate' : tpl ? `Change ${SLOT_LABELS[tpl.slot].toLowerCase()}` : 'Log food'} eyebrow={d === today ? 'Today' : d} backTo="/eat" />
      {restaurant && <Note title="Estimate by eye">Add each part of the plate with a hand or restaurant portion. Restaurant food often has extra oil, so an allowance is on by default.</Note>}
      <Section title="Meal">
        <select className="input" value={s} onChange={(e) => setS(e.target.value as Slot)} aria-label="Meal">
          {SLOTS.map((x) => (
            <option key={x} value={x}>
              {slotLabel(x)}
            </option>
          ))}
        </select>
      </Section>

      <Section title="Items">
        <div className="group" data-testid="log-items">
          {items.length === 0 && <div className="item muted">Nothing added yet.</div>}
          {items.map((it, i) => {
            const orig = tpl?.items[i];
            const swapped = it.substitutedFrom;
            return (
              <div className="item" key={i} style={{ alignItems: 'flex-start' }}>
                <button type="button" className="item-main" style={{ background: 'none', border: 0, textAlign: 'left', font: 'inherit', color: 'inherit', padding: 0 }} onClick={() => setEditIdx(i)}>
                  <span className="item-title" style={{ display: 'block' }}>
                    {it.name}
                  </span>
                  <span className="item-sub" style={{ display: 'block' }}>
                    {it.estimate.portion ? `${it.estimate.count} × ${PORTIONS.find((p) => p.key === it.estimate.portion)?.label.toLowerCase()}, ` : ''}
                    {it.foodId === null && it.estimate.gramsMid === 0 ? 'Your own numbers' : formatRange(it.estimate.gramsLow, it.estimate.gramsHigh, ' g')}, {formatRange(it.low.kcal, it.high.kcal, ' kcal')}
                  </span>
                  <span className="item-sub faint" style={{ display: 'block' }}>
                    {CONFIDENCE_LABELS[it.estimate.confidence]}
                    {swapped ? `, instead of ${FOOD_BY_ID[swapped]?.name ?? swapped}` : orig && orig.grams !== it.estimate.gramsMid ? `, planned ${orig.grams} g` : ''}
                  </span>
                </button>
                <button type="button" className="btn btn-sm btn-ghost" aria-label={`Remove ${it.name}`} onClick={() => setItems(items.filter((_, j) => j !== i))}>
                  <IconClose size={18} />
                </button>
              </div>
            );
          })}
          {oil && (
            <div className="item">
              <span className="item-main">
                <span className="item-title" style={{ display: 'block' }}>
                  Cooking oil you cannot see
                </span>
                <span className="item-sub" style={{ display: 'block' }}>
                  0 to 20 g, 0 to 180 kcal
                </span>
              </span>
            </div>
          )}
        </div>
        <button type="button" className="btn btn-outline btn-block" style={{ marginTop: 8 }} onClick={() => setPickerOpen(true)} data-testid="add-food">
          <IconPlus /> Add food
        </button>
        <div className="group" style={{ marginTop: 8 }}>
          <Toggle checked={oil} onChange={setOil} label="Add a hidden oil allowance" sub="For restaurant, hosted, or fried food. Widens the range rather than guessing." />
        </div>
      </Section>

      <Section title="Estimate">
        <div className="panel" data-testid="log-estimate">
          <div className="row-between">
            <div>
              <div className="big-number" style={{ fontSize: '1.7rem' }}>
                {formatRange(t.low.kcal, t.high.kcal)}
              </div>
              <div className="small muted">kcal, {lowestConfidence === 'low' ? 'estimated by eye, low confidence' : lowestConfidence === 'medium' ? 'household measures, medium confidence' : 'weighed or label, high confidence'}</div>
            </div>
            <div style={{ textAlign: 'right', whiteSpace: 'nowrap', flex: 'none' }} className="small">
              <div>Protein {formatRange(t.low.protein, t.high.protein, ' g')}</div>
              <div>Carbs {formatRange(t.low.carbs, t.high.carbs, ' g')}</div>
              <div>Fat {formatRange(t.low.fat, t.high.fat, ' g')}</div>
            </div>
          </div>
          {tpl && (
            <p className="small muted" style={{ marginTop: 8 }}>
              Planned meal: {formatRange(sumItems(original).low.kcal, sumItems(original).high.kcal, ' kcal')}. {unchanged ? 'No changes.' : `Change of about ${Math.round(t.mid.kcal - sumItems(original).mid.kcal)} kcal.`}
            </p>
          )}
        </div>
      </Section>

      <Section title="Photo and note">
        <div className="stack">
          <input ref={fileRef} type="file" accept="image/*" capture="environment" hidden onChange={async (e) => {
            const f = e.target.files?.[0];
            if (!f) return;
            try {
              setPhoto(await compressImage(f));
            } catch {
              toast('That photo could not be read');
            }
          }} />
          {photo ? (
            <div className="row">
              <img src={photo.dataUrl} alt="Meal photo preview" width={72} height={72} style={{ borderRadius: 10, objectFit: 'cover' }} />
              <span className="small muted grow">Stored only on this phone, about {Math.round(photo.bytes / 1024)} KB. Not included in coach reports unless you choose.</span>
              <button type="button" className="btn btn-sm btn-ghost" onClick={() => setPhoto(null)}>
                Remove
              </button>
            </div>
          ) : (
            <button type="button" className="btn btn-outline" onClick={() => fileRef.current?.click()}>
              <IconCamera /> Add photo, optional
            </button>
          )}
          <textarea className="input" placeholder="Note, optional" value={note} onChange={(e) => setNote(e.target.value)} maxLength={2000} />
        </div>
      </Section>

      <div style={{ marginTop: 20 }}>
        <button type="button" className="btn btn-primary btn-large btn-block" disabled={all.length === 0} onClick={() => void save()} data-testid="save-food">
          Save
        </button>
      </div>

      <FoodPicker
        open={pickerOpen}
        onClose={() => setPickerOpen(false)}
        restaurant={restaurant}
        onAdd={(it) => {
          setItems([...items, it]);
          setPickerOpen(false);
        }}
      />
      {editIdx !== null && items[editIdx] && (
        <FoodPicker
          open
          restaurant={restaurant}
          onClose={() => setEditIdx(null)}
          editing={items[editIdx]}
          onAdd={(it) => {
            const prev = items[editIdx]!;
            const next = [...items];
            next[editIdx] = { ...it, substitutedFrom: it.foodId !== prev.foodId ? (prev.substitutedFrom ?? prev.foodId) : prev.substitutedFrom };
            setItems(next);
            setEditIdx(null);
          }}
        />
      )}
    </div>
  );
}

function FoodPicker({ open, onClose, onAdd, restaurant, editing }: { open: boolean; onClose: () => void; onAdd: (it: FoodLogItem) => void; restaurant: boolean; editing?: FoodLogItem }) {
  const [q, setQ] = useState('');
  const [food, setFood] = useState<Food | null>(editing?.foodId ? (FOOD_BY_ID[editing.foodId] ?? null) : null);
  const [how, setHow] = useState<'eye' | 'grams' | 'barcode'>(restaurant ? 'eye' : editing && editing.estimate.method !== 'hand' && editing.estimate.method !== 'restaurant' ? 'grams' : 'eye');
  const [grams, setGrams] = useState<number | null>(editing?.estimate.gramsMid ?? 100);
  const [portion, setPortion] = useState<PortionKey>(restaurant ? 'restaurant-medium' : 'palm');
  const [count, setCount] = useState<number | null>(editing?.estimate.count ?? 1);
  const [own, setOwn] = useState(false);
  const list = useMemo(() => FOODS.filter((f) => !q || f.name.toLowerCase().includes(q.toLowerCase())).slice(0, 40), [q]);
  const preview = food ? (how === 'eye' ? itemFromPortion(food, portion, count ?? 1) : itemFromGrams(food, grams ?? 0, 'weighed')) : null;
  return (
    <Sheet open={open} onClose={onClose} title={own ? 'Your own food' : food ? food.name : editing ? 'Swap food' : 'Add food'} testId="food-picker">
      {own ? (
        <OwnFood name={q} onBack={() => setOwn(false)} onAdd={onAdd} />
      ) : !food ? (
        <div className="stack">
          <input className="input" type="search" placeholder="Search foods" value={q} onChange={(e) => setQ(e.target.value)} aria-label="Search foods" autoFocus />
          {q && list.length === 0 && <p className="small muted">No match for “{q}” in the food list.</p>}
          <button type="button" className={`btn ${q && list.length === 0 ? 'btn-primary' : 'btn-outline'}`} onClick={() => setOwn(true)} data-testid="own-food">
            Not in the list? Enter your own numbers
          </button>
          <div className="group" style={{ maxHeight: '50dvh', overflowY: 'auto' }}>
            {list.map((f) => (
              <button type="button" className="item" key={f.id} onClick={() => setFood(f)}>
                <span className="item-main">
                  <span className="item-title" style={{ display: 'block' }}>{f.name}</span>
                  <span className="item-sub" style={{ display: 'block' }}>
                    {f.per100.kcal} kcal and {f.per100.protein} g protein per 100 {f.liquid ? 'ml' : 'g'}, {f.state}
                  </span>
                </span>
              </button>
            ))}
          </div>
          <BarcodeLookup onFood={(f) => setFood(f)} />
        </div>
      ) : (
        <div className="stack">
          <Seg
            label="How to measure"
            value={how}
            onChange={setHow}
            options={[
              { value: 'eye', label: 'Estimate by eye' },
              { value: 'grams', label: f(food) },
            ]}
          />
          {how === 'eye' ? (
            <>
              <div className="grid-3" role="radiogroup" aria-label="Portion">
                {PORTIONS.map((p) => (
                  <button key={p.key} type="button" role="radio" aria-checked={portion === p.key} className={`btn ${portion === p.key ? 'btn-primary' : 'btn-outline'}`} style={{ flexDirection: 'column', height: 86, gap: 2, whiteSpace: 'normal', lineHeight: 1.1, padding: 4 }} onClick={() => setPortion(p.key)} data-testid={`portion-${p.key}`}>
                    <PortionIcon k={p.key} size={34} />
                    <span className="small">{p.label.replace(' restaurant portion', '')}</span>
                  </button>
                ))}
              </div>
              <p className="small muted">{PORTIONS.find((p) => p.key === portion)?.hint}</p>
              <Stepper label="How many" value={count} onChange={setCount} step={0.5} decimals={1} min={0.5} max={20} testId="portion-count" />
            </>
          ) : (
            <Stepper label={food.liquid ? 'Millilitres' : 'Grams'} value={grams} onChange={setGrams} step={food.liquid ? 50 : 10} max={3000} testId="grams-input" />
          )}
          {how === 'grams' && food.units && (
            <div className="chips">
              {food.units.map((u) => (
                <button key={u.label} type="button" className="chip" onClick={() => setGrams(u.grams)}>
                  {u.label}
                </button>
              ))}
            </div>
          )}
          {preview && (
            <div className="note" data-testid="portion-preview">
              <strong>
                {formatRange(preview.estimate.gramsLow, preview.estimate.gramsHigh, food.liquid ? ' ml' : ' g')}, {formatRange(preview.low.kcal, preview.high.kcal, ' kcal')}
              </strong>
              Protein {formatRange(preview.low.protein, preview.high.protein, ' g')}. {CONFIDENCE_LABELS[preview.estimate.confidence]}. {food.note ?? ''}
            </div>
          )}
          <div className="grid-2">
            <button type="button" className="btn btn-outline" onClick={() => setFood(null)}>
              Other food
            </button>
            <button type="button" className="btn btn-primary" disabled={!preview || preview.estimate.gramsMid <= 0} onClick={() => preview && onAdd(preview)} data-testid="add-item">
              {editing ? 'Update' : 'Add'}
            </button>
          </div>
        </div>
      )}
    </Sheet>
  );
}

/** Free entry: any food with the totals you know or guess. */
function OwnFood({ name: name0, onBack, onAdd }: { name: string; onBack: () => void; onAdd: (it: FoodLogItem) => void }) {
  const [name, setName] = useState(name0);
  const [source, setSource] = useState<'label' | 'guess'>('guess');
  const [kcal, setKcal] = useState<number | null>(null);
  const [protein, setProtein] = useState<number | null>(null);
  const [carbs, setCarbs] = useState<number | null>(null);
  const [fat, setFat] = useState<number | null>(null);
  const item = kcal !== null ? itemFromTotals(name, { kcal, protein: protein ?? 0, carbs: carbs ?? 0, fat: fat ?? 0 }, source) : null;
  return (
    <div className="stack" data-testid="own-food-form">
      <label className="field">
        <span className="label">Food</span>
        <input className="input" value={name} onChange={(e) => setName(e.target.value)} maxLength={120} placeholder="For example, two slices of pizza" data-testid="own-food-name" />
      </label>
      <Seg
        label="Where the numbers come from"
        value={source}
        onChange={setSource}
        options={[
          { value: 'guess', label: 'My best guess' },
          { value: 'label', label: 'Label or menu' },
        ]}
      />
      <p className="small muted">Totals for what you ate, not per 100 g. Only calories are needed.</p>
      <div className="grid-2">
        <Stepper label="Calories" unit="kcal" value={kcal} onChange={setKcal} step={10} max={4000} testId="own-food-kcal" />
        <Stepper label="Protein" unit="g" value={protein} onChange={setProtein} step={1} decimals={1} max={400} testId="own-food-protein" />
        <Stepper label="Carbs" unit="g" value={carbs} onChange={setCarbs} step={1} decimals={1} max={600} />
        <Stepper label="Fat" unit="g" value={fat} onChange={setFat} step={1} decimals={1} max={300} />
      </div>
      {item && (
        <div className="note">
          <strong>{formatRange(item.low.kcal, item.high.kcal, ' kcal')}</strong> {CONFIDENCE_LABELS[item.estimate.confidence]}.
        </div>
      )}
      <div className="grid-2">
        <button type="button" className="btn btn-outline" onClick={onBack}>
          Back
        </button>
        <button type="button" className="btn btn-primary" disabled={!item || !name.trim()} onClick={() => item && onAdd(item)} data-testid="own-food-add">
          Add
        </button>
      </div>
    </div>
  );
}

function f(food: Food) {
  return food.liquid ? 'Millilitres' : 'Grams';
}

/**
 * Optional barcode lookup. Uses the camera BarcodeDetector where it exists (not on iPhone
 * today), otherwise a typed code. Asks Open Food Facts only when online and only after a tap.
 * A manual label entry is always available.
 */
function BarcodeLookup({ onFood }: { onFood: (f: Food) => void }) {
  const online = useOnline();
  const [code, setCode] = useState('');
  const [status, setStatus] = useState<string>('');
  const [manual, setManual] = useState(false);
  const [label, setLabel] = useState({ name: '', kcal: null as number | null, protein: null as number | null, carbs: null as number | null, fat: null as number | null });
  const hasDetector = typeof window !== 'undefined' && 'BarcodeDetector' in window;
  const lookup = async () => {
    if (!/^\d{8,14}$/.test(code)) return setStatus('Enter the 8 to 14 digit number under the barcode.');
    setStatus('Looking up…');
    try {
      const res = await fetch(`https://world.openfoodfacts.org/api/v2/product/${code}.json?fields=product_name,nutriments`, { headers: { Accept: 'application/json' }, referrerPolicy: 'no-referrer', credentials: 'omit' });
      const j = (await res.json()) as { status?: number; product?: { product_name?: string; nutriments?: Record<string, number> } };
      const n = j.product?.nutriments;
      if (!j.product || !n || n['energy-kcal_100g'] === undefined) {
        setStatus('Not found or no nutrition data. Enter the label values instead.');
        setManual(true);
        return;
      }
      onFood({
        id: `off-${code}`,
        name: j.product.product_name || `Product ${code}`,
        category: 'mixed',
        state: 'as sold',
        per100: { kcal: n['energy-kcal_100g'] ?? 0, protein: n['proteins_100g'] ?? 0, carbs: n['carbohydrates_100g'] ?? 0, fat: n['fat_100g'] ?? 0, fibre: n['fiber_100g'] ?? 0, calcium: (n['calcium_100g'] ?? 0) * 1000 },
        variability: 0.1,
        note: 'Data from Open Food Facts, a community database under the ODbL. Check it against the label.',
      });
    } catch {
      setStatus('No connection to Open Food Facts. Enter the label values instead.');
      setManual(true);
    }
  };
  return (
    <details className="disclosure">
      <summary>Barcode or food label</summary>
      <div className="stack">
        <p className="small muted">
          {hasDetector ? 'Type the code, or use a camera app to read it.' : 'This browser cannot scan barcodes with the camera. Type the number printed under the barcode.'} Looking up sends only the barcode number to Open Food Facts.
        </p>
        <div className="row">
          <input className="input" inputMode="numeric" pattern="[0-9]*" value={code} onChange={(e) => setCode(e.target.value.replace(/\D/g, ''))} placeholder="Barcode number" aria-label="Barcode number" />
          <button type="button" className="btn btn-outline" disabled={!online} onClick={() => void lookup()}>
            {online ? 'Look up' : 'Offline'}
          </button>
        </div>
        {status && <p className="small">{status}</p>}
        <button type="button" className="btn btn-ghost" onClick={() => setManual((m) => !m)}>
          Enter label values by hand
        </button>
        {manual && (
          <div className="stack">
            <input className="input" placeholder="Food name" value={label.name} onChange={(e) => setLabel({ ...label, name: e.target.value })} maxLength={100} />
            <div className="grid-2">
              <Stepper label="kcal per 100 g" value={label.kcal} onChange={(v) => setLabel({ ...label, kcal: v })} step={5} max={900} />
              <Stepper label="Protein g" value={label.protein} onChange={(v) => setLabel({ ...label, protein: v })} step={0.5} decimals={1} max={100} />
              <Stepper label="Carbs g" value={label.carbs} onChange={(v) => setLabel({ ...label, carbs: v })} step={0.5} decimals={1} max={100} />
              <Stepper label="Fat g" value={label.fat} onChange={(v) => setLabel({ ...label, fat: v })} step={0.5} decimals={1} max={100} />
            </div>
            <button
              type="button"
              className="btn btn-primary"
              disabled={!label.name || label.kcal === null}
              onClick={() =>
                onFood({ id: `label-${Date.now()}`, name: label.name, category: 'mixed', state: 'as sold', per100: { kcal: label.kcal ?? 0, protein: label.protein ?? 0, carbs: label.carbs ?? 0, fat: label.fat ?? 0, fibre: 0, calcium: 0 }, variability: 0.05, note: 'From the food label.' })
              }
            >
              Use these values
            </button>
          </div>
        )}
      </div>
    </details>
  );
}

