import { useState, type ReactNode } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../db/db';
import { KV, addSportLog, deleteSportLog, kvGet, kvSet, saveAthlete } from '../db/repo';
import { Item, Note, PageHead, Section, Stepper, Toggle, useToast } from '../ui/components';
import { useAthlete, useToday } from '../ui/hooks';
import { useSettings } from '../ui/state';
import { navigate } from '../ui/router';
import { uid } from '../lib/id';
import { addDays, formatDateKey, reviewWeekStart } from '../domain/dates';
import { FOOD_BY_ID } from '../content/foods';
import { exercise } from '../content/library';
import { PLANNING_PHASES, planningPhaseFor, weekOfPlan } from '../content/phases';
import { DEFAULT_KOSHER_HOURS, openQuestions, type AthleteProfile, type ReviewedTarget, type UsualVeg } from '../domain/athlete';
import { weeklyExposure } from '../domain/exposure';
import { proposePlan } from '../services/planUpdate';
import type { SportLog } from '../db/records';

// The athlete profile (3.0.0): the facts that decide what the plan may contain, goals in the
// athlete's own words, targets a professional reviewed, and school sport. Everything stays on the phone.

function Choice<T extends string>({ label, value, options, onChange, testId }: { label: string; value: T; options: Array<[T, string]>; onChange: (v: T) => void; testId?: string }) {
  return (
    <fieldset className="choice" data-testid={testId}>
      <legend className="small muted">{label}</legend>
      <div className="row wrap" style={{ gap: 6 }}>
        {options.map(([v, text]) => (
          <button key={v} type="button" className={`btn btn-sm ${value === v ? 'btn-primary' : 'btn-outline'}`} aria-pressed={value === v} onClick={() => onChange(v)} data-value={v}>
            {text}
          </button>
        ))}
      </div>
    </fieldset>
  );
}

function Block({ title, children, testId }: { title: string; children: ReactNode; testId?: string }) {
  return (
    <Section title={title}>
      <div className="panel stack" data-testid={testId}>
        {children}
      </div>
    </Section>
  );
}

const GREEN_BEAN_FOOD: Record<UsualVeg['state'], string | null> = { unknown: null, raw: 'green-beans-raw', 'frozen-cooked': 'green-beans-frozen', 'boiled-drained': 'green-beans', 'canned-drained': 'green-beans-canned' };

/** A large green bean portion as numbers, with the arithmetic shown. Null until the state and the weight are known. */
export function vegEstimate(v: UsualVeg): { kcal: number; fibre: number; protein: number; lines: string[] } | null {
  const id = GREEN_BEAN_FOOD[v.state];
  const f = id ? FOOD_BY_ID[id] : null;
  if (!f || v.grams === null) return null;
  const k = v.grams / 100;
  const beanKcal = f.per100.kcal * k;
  const oil = v.oilG ?? 0;
  const oilKcal = oil * 8.84;
  const lines = [`${v.grams} g × ${f.per100.kcal} kcal per 100 g = ${Math.round(beanKcal)} kcal (${f.name})`];
  if (oil > 0) lines.push(`${oil} g oil × 8.84 kcal per g = ${Math.round(oilKcal)} kcal`);
  lines.push(`Fibre: ${v.grams} g × ${f.per100.fibre} g per 100 g = ${Math.round(f.per100.fibre * k)} g`);
  return { kcal: Math.round(beanKcal + oilKcal), fibre: Math.round(f.per100.fibre * k), protein: Math.round(f.per100.protein * k), lines };
}

export function AthleteScreen({ next }: { next: string | null }) {
  const a = useAthlete();
  const settings = useSettings();
  const toast = useToast();
  const [busy, setBusy] = useState(false);
  const set = <K extends keyof AthleteProfile>(k: K, patch: Partial<AthleteProfile[K]>) => void saveAthlete(k, { ...(a[k] as object), ...patch } as AthleteProfile[K]);
  const creatineActive = settings.supplements.some((s) => s.kind === 'creatine' && s.active);
  const open = openQuestions(a, { creatineActive: creatineActive || !!a.supplements.creatineProduct });
  const veg = vegEstimate(a.veg);
  const build = async () => {
    setBusy(true);
    await saveAthlete('sport', { ...a.sport, confirmed: true });
    await proposePlan(next === 'v3' ? 'v3' : 'profile');
    navigate('/plan');
  };
  const eq = a.home.equipment;
  return (
    <div data-testid="athlete">
      <PageHead title="Your profile" eyebrow="Stays on this phone" backTo="/more" />
      <p className="muted">These answers decide which drills and exercises fit. Anything you have not answered is treated cautiously. Nothing here is a medical clearance.</p>
      {open.length > 0 && (
        <Note tone="accent" title={`${open.length} thing${open.length === 1 ? '' : 's'} still to confirm`}>
          <ul className="bullets small">
            {open.map((q) => (
              <li key={q.id}>
                <b>{q.title}.</b> {q.why}
              </li>
            ))}
          </ul>
        </Note>
      )}

      <Block title="Wrist after an injury" testId="athlete-wrist">
        <Choice
          label="What a clinician has said"
          value={a.wrist.status}
          onChange={(v) => set('wrist', { status: v })}
          testId="wrist-status"
          options={[
            ['unknown', 'Not sure'],
            ['not-cleared', 'Not cleared yet'],
            ['cleared', 'No injury, or cleared for full sport'],
            ['symptoms', 'Pain or swelling now'],
          ]}
        />
        {a.wrist.status === 'cleared' && (
          <>
            <label className="field">
              <span className="small muted">Who cleared it</span>
              <input className="input" value={a.wrist.clearedBy} maxLength={80} placeholder="For example, orthopaedic doctor" onChange={(e) => set('wrist', { clearedBy: e.target.value })} />
            </label>
            <label className="field">
              <span className="small muted">Date</span>
              <input className="input" type="date" value={a.wrist.date ?? ''} onChange={(e) => set('wrist', { date: e.target.value || null })} />
            </label>
            <label className="field">
              <span className="small muted">Any limits they gave</span>
              <input className="input" value={a.wrist.limits} maxLength={300} onChange={(e) => set('wrist', { limits: e.target.value })} />
            </label>
          </>
        )}
        <p className="small muted">
          {a.wrist.status === 'cleared'
            ? 'All exercises may be planned. Stop any exercise that hurts the wrist.'
            : a.wrist.status === 'symptoms'
              ? 'Exercises that grip or press a load are left out, and there is no ball contact. Tell a parent and see the clinician who treated the injury.'
              : 'Until a clinician confirms clearance, gripping and pressing exercises keep their load, heavy grip exercises are swapped, and there is no ball contact or falling onto the hands.'}
        </p>
      </Block>

      <Block title="Your space at home" testId="athlete-home">
        <Choice label="Clear floor indoors" value={a.home.space} onChange={(v) => set('home', { space: v })} testId="home-space" options={[['unknown', 'Not sure'], ['small', 'About 2 × 2 m'], ['medium', 'About 3 × 3 m'], ['large', '5 m or more']]} />
        <Choice label="Ceiling" value={a.home.ceiling} onChange={(v) => set('home', { ceiling: v })} testId="home-ceiling" options={[['unknown', 'Not sure'], ['low', 'I can touch it with a raised arm'], ['standard', 'I cannot touch it on my toes'], ['high', 'I cannot touch it even jumping']]} />
        <Choice label="Floor" value={a.home.surface} onChange={(v) => set('home', { surface: v })} testId="home-surface" options={[['unknown', 'Not sure'], ['slippery', 'Tiles or slippery'], ['hard', 'Hard, in trainers'], ['mat', 'Exercise mat'], ['carpet', 'Carpet']]} />
        <Choice label="Must you keep the noise down?" value={a.home.noiseLimits} onChange={(v) => set('home', { noiseLimits: v })} testId="home-noise" options={[['unknown', 'Not sure'], ['yes', 'Yes'], ['no', 'No']]} />
        <Choice label="People or breakable things close by?" value={a.home.breakables} onChange={(v) => set('home', { breakables: v })} testId="home-breakables" options={[['unknown', 'Not sure'], ['yes', 'Yes'], ['no', 'No']]} />
        <Choice label="A safe outdoor space you may use" value={a.home.outdoor} onChange={(v) => set('home', { outdoor: v })} testId="home-outdoor" options={[['unknown', 'Not sure'], ['none', 'None'], ['small', 'Small yard'], ['large', 'Court, park, or big yard']]} />
        {(a.home.outdoor === 'small' || a.home.outdoor === 'large') && (
          <Choice label="Outdoor surface" value={a.home.outdoorSurface} onChange={(v) => set('home', { outdoorSurface: v })} testId="home-outdoor-surface" options={[['unknown', 'Not sure'], ['grass', 'Grass'], ['court', 'Court'], ['concrete', 'Concrete']]} />
        )}
        <fieldset className="choice">
          <legend className="small muted">Equipment you have</legend>
          <div className="row wrap" style={{ gap: 6 }}>
            {(
              [
                ['tape', 'Tape'],
                ['mat', 'Mat'],
                ['box', 'Stable box'],
                ['cones', 'Cones'],
                ['ball', 'Volleyball'],
                ['wall', 'Solid outdoor wall'],
                ['rope', 'Jump rope'],
                ['light-dumbbells', 'Light dumbbells'],
              ] as const
            ).map(([v, text]) => (
              <button key={v} type="button" className={`btn btn-sm ${eq.includes(v) ? 'btn-primary' : 'btn-outline'}`} aria-pressed={eq.includes(v)} onClick={() => set('home', { equipment: eq.includes(v) ? eq.filter((x) => x !== v) : [...eq, v] })}>
                {text}
              </button>
            ))}
          </div>
        </fieldset>
        <p className="small muted">Jumps need a floor that is not slippery, room to land, and a ceiling you cannot reach. When the room does not allow a drill, PeakForm plans a quieter one without jumps.</p>
      </Block>

      <Block title="School and club sport" testId="athlete-sport">
        <p className="small muted">In a usual week. It counts toward the same weekly load as the plan.</p>
        <div className="grid-2">
          <Stepper label="Volleyball sessions a week" value={a.sport.volleyball.sessions} onChange={(v) => set('sport', { volleyball: { ...a.sport.volleyball, sessions: v } })} min={0} max={14} testId="sport-vb-sessions" />
          <Stepper label="Minutes each" value={a.sport.volleyball.minutes} onChange={(v) => set('sport', { volleyball: { ...a.sport.volleyball, minutes: v } })} step={15} min={0} max={300} />
          <Stepper label="Basketball sessions a week" value={a.sport.basketball.sessions} onChange={(v) => set('sport', { basketball: { ...a.sport.basketball, sessions: v } })} min={0} max={14} testId="sport-bb-sessions" />
          <Stepper label="Minutes each" value={a.sport.basketball.minutes} onChange={(v) => set('sport', { basketball: { ...a.sport.basketball, minutes: v } })} step={15} min={0} max={300} />
        </div>
        <Choice label="How much jumping in a usual week of school sport" value={a.sport.jumping} onChange={(v) => set('sport', { jumping: v })} options={[['unknown', 'Not sure'], ['little', 'Little'], ['some', 'Some'], ['lots', 'A lot']]} />
        <Toggle checked={a.sport.confirmed} onChange={(v) => set('sport', { confirmed: v })} label="This is my usual week" sub="Log single practices and games in More, School sport." />
      </Block>

      <Block title="Basics" testId="athlete-basics">
        <Toggle checked={a.basics.heightConfirmed} onChange={(v) => set('basics', { heightConfirmed: v, heightMeasuredOn: v ? (a.basics.heightMeasuredOn ?? new Date().toISOString().slice(0, 10)) : null })} label="Height measured again recently" sub="Edit the number in More, Settings, Profile. You are still growing." />
        <Choice label="Who supervises at the gym" value={a.basics.supervision} onChange={(v) => set('basics', { supervision: v })} options={[['unknown', 'Not sure'], ['none', 'Nobody'], ['gym staff', 'Gym staff'], ['qualified coach', 'Qualified coach'], ['parent', 'A parent']]} />
        <Stepper label="Usual sleep, hours" value={a.basics.typicalSleepH} onChange={(v) => set('basics', { typicalSleepH: v })} step={0.25} decimals={2} min={0} max={14} />
      </Block>

      <Block title="Creatine and supplements" testId="athlete-supplements">
        <p className="small muted">PeakForm never starts, increases, or recommends a supplement. The AAP discourages performance supplements for under 18s, and other experts accept creatine only with supervision. These details let a parent and a clinician review it.</p>
        <label className="field">
          <span className="small muted">Creatine product, if you take it</span>
          <input className="input" value={a.supplements.creatineProduct} maxLength={120} placeholder="Brand and product name" onChange={(e) => set('supplements', { creatineProduct: e.target.value })} />
        </label>
        <Stepper label="Grams a day" value={a.supplements.creatineDoseG} onChange={(v) => set('supplements', { creatineDoseG: v })} step={0.5} decimals={1} min={0} max={30} />
        <label className="field">
          <span className="small muted">Started on</span>
          <input className="input" type="date" value={a.supplements.startedOn ?? ''} onChange={(e) => set('supplements', { startedOn: e.target.value || null })} />
        </label>
        <Choice label="Third party tested, such as NSF Certified for Sport or Informed Sport" value={a.supplements.thirdPartyTested} onChange={(v) => set('supplements', { thirdPartyTested: v })} options={[['unknown', 'Not sure'], ['yes', 'Yes'], ['no', 'No']]} />
        <Choice label="Kosher certified" value={a.supplements.kosherCertified} onChange={(v) => set('supplements', { kosherCertified: v })} options={[['unknown', 'Not sure'], ['yes', 'Yes'], ['no', 'No']]} />
        <label className="field">
          <span className="small muted">Reviewed by</span>
          <input className="input" value={a.supplements.reviewedBy} maxLength={120} placeholder="For example, a parent and the family doctor" onChange={(e) => set('supplements', { reviewedBy: e.target.value })} />
        </label>
        <p className="small muted">Creatine usually adds some water to the muscles, often 1 to 2 kg early on, mostly in the first weeks. Smart scales count that water as lean mass, so it is not proof of new muscle.</p>
      </Block>

      <Block title="Green beans in large amounts" testId="athlete-veg">
        <p className="small muted">Only if you eat a lot of green beans most days. Leave it empty otherwise.</p>
        <Stepper label="Grams a day" value={a.veg.grams} onChange={(v) => set('veg', { grams: v })} step={50} min={0} max={3000} testId="veg-grams" />
        <Choice label="Weighed as" value={a.veg.state} onChange={(v) => set('veg', { state: v })} testId="veg-state" options={[['unknown', 'Not sure'], ['raw', 'Raw'], ['frozen-cooked', 'Frozen, then cooked'], ['boiled-drained', 'Boiled and drained'], ['canned-drained', 'Canned, drained']]} />
        <Choice label="Added on top, or instead of something" value={a.veg.role} onChange={(v) => set('veg', { role: v })} options={[['unknown', 'Not sure'], ['added', 'Added on top'], ['replaced', 'Instead of other food']]} />
        <Stepper label="Oil, grams" value={a.veg.oilG} onChange={(v) => set('veg', { oilG: v })} min={0} max={100} />
        <label className="field">
          <span className="small muted">Sauce or seasoning</span>
          <input className="input" value={a.veg.sauce} maxLength={120} onChange={(e) => set('veg', { sauce: e.target.value })} />
        </label>
        <Choice label="Stomach" value={a.veg.stomach} onChange={(v) => set('veg', { stomach: v })} options={[['unknown', 'Not sure'], ['fine', 'Fine'], ['bloating', 'Gas or bloating'], ['discomfort', 'Discomfort']]} />
        {veg ? (
          <div className="small" data-testid="veg-estimate">
            <p>
              About <b>{veg.kcal} kcal</b>, {veg.protein} g protein, and {veg.fibre} g fibre a day.
            </p>
            <ul className="bullets muted">
              {veg.lines.map((l) => (
                <li key={l}>{l}</li>
              ))}
            </ul>
            <p className="muted">
              Vegetables are good food. A large daily amount mostly adds water and fibre: it can add weight to the scale while it is in the gut, it fills you up, and it may leave less room for other food. {a.veg.stomach === 'bloating' || a.veg.stomach === 'discomfort' ? 'With bloating or discomfort, a smaller serving or more variety is worth trying, and worth mentioning to a parent.' : ''} It is not a reason to eat less of anything else.
            </p>
          </div>
        ) : (
          <p className="small muted">Choose how they are weighed and the grams, and PeakForm shows the numbers with the arithmetic.</p>
        )}
      </Block>

      <Block title="Meat and dairy" testId="athlete-kosher">
        <Toggle checked={a.kosher.enabled} onChange={(v) => set('kosher', { enabled: v })} label="Keep an interval after meat" sub="Example meals and notes follow it. Your family's custom decides the hours." />
        {a.kosher.enabled && <Stepper label="Hours after meat before dairy" value={a.kosher.meatToDairyHours} onChange={(v) => set('kosher', { meatToDairyHours: v ?? DEFAULT_KOSHER_HOURS })} step={0.5} decimals={1} min={0} max={8} testId="kosher-hours" />}
      </Block>

      <Block title="Weighing" testId="athlete-weight">
        <Choice label="How often" value={a.weight.mode} onChange={(v) => set('weight', { mode: v })} testId="weight-mode" options={[['weekly', 'Once a week'], ['frequent', 'Several mornings a week'], ['off', 'Off']]} />
        <Toggle checked={a.weight.hideNumbers} onChange={(v) => set('weight', { hideNumbers: v })} label="Hide weight numbers" sub="Weights are still saved for the review, but not shown on Today or Progress." testId="weight-hide" />
        <p className="small muted">Daily weighing is not needed. One number means little; a trend over several weeks means more.</p>
      </Block>

      <div style={{ marginTop: 16 }}>
        <button
          type="button"
          className="btn btn-primary btn-large btn-block"
          disabled={busy}
          onClick={() => {
            void build().catch(() => {
              setBusy(false);
              toast('Could not prepare the plan. Try again.');
            });
          }}
          data-testid="athlete-build"
        >
          {next === 'v3' ? 'See the new week' : 'Update my plan from these answers'}
        </button>
        <p className="small muted" style={{ marginTop: 6 }}>You see every change before anything is saved.</p>
      </div>
    </div>
  );
}

// ---------- Goals and reviews ----------

const REVIEW_TOPICS = [
  { id: 'energy', label: 'How much to eat: energy needs, regular meals, and whether weight goals make sense now' },
  { id: 'supplements', label: 'Creatine and other supplements: product, dose, and whether to continue' },
  { id: 'physique', label: 'Body fat and muscle aspirations, and how to measure progress' },
  { id: 'wrist', label: 'Wrist clearance for gripping, pressing, and ball contact' },
  { id: 'load', label: 'Total weekly load: school sport, gym, and home jumps' },
  { id: 'sleep', label: 'Sleep, at least 8 hours' },
] as const;

interface ParentReview {
  done: string[];
  date: string | null;
  notes: string;
}

export function GoalsScreen() {
  const a = useAthlete();
  const s = useSettings();
  const today = useToday();
  const toast = useToast();
  const review = useLiveQuery(() => kvGet<ParentReview>(KV.parentReview), []) ?? { done: [], date: null, notes: '' };
  const [text, setText] = useState('');
  const [adding, setAdding] = useState(false);
  const phase = planningPhaseFor(s.planStartDate, today);
  return (
    <div data-testid="goals">
      <PageHead title="Goals and reviews" backTo="/more" />

      <Section title="Your aspirations">
        <div className="panel stack" data-testid="aspirations">
          <p className="small muted">In your own words. They are kept exactly as you write them, apart from any target a professional reviewed.</p>
          {a.aspirations.length === 0 ? (
            <p className="muted">None written yet.</p>
          ) : (
            <ul className="bullets">
              {a.aspirations.map((x) => (
                <li key={x.id}>
                  {x.text} <span className="small faint">({formatDateKey(x.recordedOn, { day: 'numeric', month: 'short', year: 'numeric' })})</span>{' '}
                  <button type="button" className="btn btn-sm btn-ghost" aria-label={`Remove ${x.text}`} onClick={() => void saveAthlete('aspirations', a.aspirations.filter((y) => y.id !== x.id))}>
                    Remove
                  </button>
                </li>
              ))}
            </ul>
          )}
          <label className="field">
            <span className="small muted">Add an aspiration</span>
            <input className="input" value={text} maxLength={300} onChange={(e) => setText(e.target.value)} placeholder="For example, jump higher for volleyball" data-testid="aspiration-input" />
          </label>
          <button
            type="button"
            className="btn btn-outline"
            disabled={!text.trim()}
            data-testid="aspiration-add"
            onClick={async () => {
              await saveAthlete('aspirations', [...a.aspirations, { id: uid('asp').slice(0, 40), text: text.trim(), recordedOn: today }]);
              setText('');
              toast('Aspiration saved');
            }}
          >
            Save aspiration
          </button>
          <details className="disclosure">
            <summary className="small">What research says about timelines</summary>
            <div className="small muted stack">
              <p>For a growing athlete, the AAP advises losing no more than about 0.45 kg a week. Faster loss puts growth, recovery, and performance at risk.</p>
              <p>Teen boys gain lean mass from growth alone. Strength training improves strength reliably, while its added effect on muscle size in young athletes is smaller and varies a lot. A smart scale cannot tell muscle from water.</p>
              <p>Smart scale body fat readings can be off by several percentage points, and they move with water, food, and creatine. They cannot show whether a body fat goal is near.</p>
              <p>Jump training studies in teens report average gains of a few centimetres over two to three months, with big differences between people.</p>
              <p>These are averages, not predictions for you. Missing a number by a date is not a failure. Steady training, food, and sleep are the parts you control.</p>
            </div>
          </details>
        </div>
      </Section>

      <Section title="Targets a professional reviewed">
        <div className="panel stack" data-testid="reviewed-targets">
          {a.reviewed.length === 0 ? (
            <p className="muted">None yet. PeakForm does not set calorie, weight, or body fat targets itself. When a pediatrician or a pediatric sports dietitian gives one, record it here with the date and units.</p>
          ) : (
            <ul className="bullets">
              {a.reviewed.map((t) => (
                <li key={t.id}>
                  <b>{t.value}</b> {t.units} · {t.source} ({t.role}), {formatDateKey(t.date, { day: 'numeric', month: 'short', year: 'numeric' })} · {t.status}{' '}
                  <button type="button" className="btn btn-sm btn-ghost" onClick={() => void saveAthlete('reviewed', a.reviewed.filter((x) => x.id !== t.id))}>
                    Remove
                  </button>
                </li>
              ))}
            </ul>
          )}
          {adding ? <ReviewedTargetForm onDone={() => setAdding(false)} /> : (
            <button type="button" className="btn btn-outline" onClick={() => setAdding(true)} data-testid="reviewed-add">
              Record a reviewed target
            </button>
          )}
        </div>
      </Section>

      <Section title="Review with a parent">
        <div className="panel stack" data-testid="parent-review">
          <p className="small muted">A calm conversation, ideally followed by a pediatrician or a pediatric sports dietitian. Share the coach report from More, Backup and export, so they see the same data.</p>
          {REVIEW_TOPICS.map((t) => (
            <label key={t.id} className="row" style={{ alignItems: 'flex-start', gap: 8 }}>
              <input
                type="checkbox"
                className="check"
                checked={review.done.includes(t.id)}
                onChange={(e) => void kvSet(KV.parentReview, { ...review, done: e.target.checked ? [...review.done, t.id] : review.done.filter((x) => x !== t.id), date: today })}
              />
              <span className="small">{t.label}</span>
            </label>
          ))}
          {review.date && <p className="small faint">Last updated {formatDateKey(review.date, { day: 'numeric', month: 'short' })}.</p>}
          <Item title="Export the coach report" sub="Markdown and JSON, shared only when you choose" to="/more/data" />
        </div>
      </Section>

      <Section title="The four months, step by step">
        <div className="stack" data-testid="planning-phases">
          {!s.planStartDate && <p className="small muted">Set the plan start date in More, Settings to see where you are.</p>}
          {PLANNING_PHASES.map((p) => (
            <div key={p.id} className="panel" style={{ outline: phase?.id === p.id ? '2px solid var(--accent)' : undefined }}>
              <h3>
                {p.name} <span className="small faint">weeks {p.weeks[0]} to {p.weeks[1]}</span>
              </h3>
              <p className="small">{p.focus}</p>
              <p className="small muted" style={{ marginTop: 4 }}>
                <b>Process goals:</b> {p.processGoals.join('. ')}.
              </p>
              <p className="small muted" style={{ marginTop: 4 }}>
                <b>Review looks at:</b> {p.reviewChecks.join('. ')}.
              </p>
              {phase?.id === p.id && s.planStartDate && <p className="small" style={{ marginTop: 4 }}>You are in week {weekOfPlan(s.planStartDate, today)}.</p>}
            </div>
          ))}
          <p className="small muted">Stages never change the plan by themselves. Any change is shown first and only saved when you activate it.</p>
        </div>
      </Section>
    </div>
  );
}

function ReviewedTargetForm({ onDone }: { onDone: () => void }) {
  const a = useAthlete();
  const today = useToday();
  const [t, setT] = useState<Omit<ReviewedTarget, 'id'>>({ kind: 'energy', value: '', units: 'kcal a day', source: '', role: 'pediatric sports dietitian', date: today, status: 'professionally reviewed', kcalRange: null, notes: '' });
  const ok = t.value.trim() && t.source.trim();
  return (
    <div className="stack" data-testid="reviewed-form">
      <Choice label="About" value={t.kind} onChange={(v) => setT({ ...t, kind: v })} options={[['energy', 'Energy'], ['protein', 'Protein'], ['weight', 'Weight'], ['body-composition', 'Body composition'], ['supplement', 'Supplement'], ['training', 'Training'], ['other', 'Other']]} />
      <label className="field">
        <span className="small muted">Target, in their words</span>
        <input className="input" value={t.value} maxLength={200} onChange={(e) => setT({ ...t, value: e.target.value })} data-testid="reviewed-value" />
      </label>
      <label className="field">
        <span className="small muted">Units</span>
        <input className="input" value={t.units} maxLength={40} onChange={(e) => setT({ ...t, units: e.target.value })} />
      </label>
      <label className="field">
        <span className="small muted">Who gave it</span>
        <input className="input" value={t.source} maxLength={120} onChange={(e) => setT({ ...t, source: e.target.value })} placeholder="Name or clinic" data-testid="reviewed-source" />
      </label>
      <Choice label="Their role" value={t.role} onChange={(v) => setT({ ...t, role: v })} options={[['pediatrician', 'Pediatrician'], ['pediatric sports dietitian', 'Pediatric sports dietitian'], ['dietitian', 'Dietitian'], ['physiotherapist', 'Physiotherapist'], ['orthopaedic clinician', 'Orthopaedic clinician'], ['qualified coach', 'Qualified coach'], ['other', 'Other']]} />
      <label className="field">
        <span className="small muted">Date</span>
        <input className="input" type="date" value={t.date} onChange={(e) => setT({ ...t, date: e.target.value || today })} />
      </label>
      <Choice label="Status" value={t.status} onChange={(v) => setT({ ...t, status: v })} options={[['professionally reviewed', 'Reviewed by a professional'], ['discussed with a parent only', 'Discussed with a parent only']]} />
      {t.kind === 'energy' && (
        <div className="grid-2">
          <Stepper label="From, kcal" value={t.kcalRange?.[0] ?? null} onChange={(v) => setT({ ...t, kcalRange: v === null ? null : [v, Math.max(v, t.kcalRange?.[1] ?? v)] })} step={50} min={500} max={8000} />
          <Stepper label="To, kcal" value={t.kcalRange?.[1] ?? null} onChange={(v) => setT({ ...t, kcalRange: v === null ? null : [Math.min(v, t.kcalRange?.[0] ?? v), v] })} step={50} min={500} max={8000} />
        </div>
      )}
      <label className="field">
        <span className="small muted">Notes</span>
        <input className="input" value={t.notes} maxLength={500} onChange={(e) => setT({ ...t, notes: e.target.value })} />
      </label>
      <div className="grid-2">
        <button
          type="button"
          className="btn btn-primary"
          disabled={!ok}
          data-testid="reviewed-save"
          onClick={async () => {
            await saveAthlete('reviewed', [...a.reviewed, { ...t, id: uid('tgt').slice(0, 40), value: t.value.trim(), source: t.source.trim() }]);
            onDone();
          }}
        >
          Save
        </button>
        <button type="button" className="btn btn-outline" onClick={onDone}>
          Cancel
        </button>
      </div>
    </div>
  );
}

// ---------- School and club sport ----------

export function SportScreen() {
  const today = useToday();
  const a = useAthlete();
  const toast = useToast();
  const from = addDays(today, -27);
  const data = useLiveQuery(
    () => Promise.all([db.sportLogs.where('date').between(from, today, true, true).toArray(), db.sessions.where('date').between(from, today, true, true).toArray(), db.setLogs.where('completedAt').above(Date.now() - 8 * 86400000).toArray()]),
    [today],
  );
  const [form, setForm] = useState<Omit<SportLog, 'id' | 'createdAt' | 'updatedAt'>>({ date: today, sport: 'volleyball', name: '', minutes: 90, intensity: 'moderate', jumping: 'some', note: '' });
  if (!data) return null;
  const [logs, sessions, sets] = data;
  const week = weeklyExposure(reviewWeekStart(today), sessions, logs, sets, (id) => exercise(id)?.kind === 'jump');
  return (
    <div data-testid="sport">
      <PageHead title="School and club sport" backTo="/more" />
      <p className="muted">Practices and games count toward the same weekly load as the gym and the home sessions. A day with a lot of jumping makes the next home jump session shorter.</p>
      <Section title="This week">
        <div className="panel small" data-testid="sport-week">
          <p>
            Sport {Math.round(week.sportMin)} min, plan sessions {Math.round(week.trainingMin)} min. Total about {(week.totalMin / 60).toFixed(1)} hours.
          </p>
          <p className="muted">Home jump landings logged: {week.jumpContacts}. Sport days with a lot of jumping: {week.lotsJumpingDays}.</p>
          {a.sport.confirmed ? null : <p className="muted">Your usual week is not set yet. Add it in More, Your profile.</p>}
        </div>
      </Section>
      <Section title="Log a practice or game">
        <div className="panel stack">
          <label className="field">
            <span className="small muted">Date</span>
            <input className="input" type="date" value={form.date} max={today} onChange={(e) => setForm({ ...form, date: e.target.value || today })} />
          </label>
          <Choice label="Sport" value={form.sport} onChange={(v) => setForm({ ...form, sport: v })} testId="sport-kind" options={[['volleyball', 'Volleyball'], ['basketball', 'Basketball'], ['other', 'Other']]} />
          <Stepper label="Minutes" value={form.minutes} onChange={(v) => setForm({ ...form, minutes: v ?? 0 })} step={15} min={0} max={600} testId="sport-minutes" />
          <Choice label="How hard" value={form.intensity} onChange={(v) => setForm({ ...form, intensity: v })} options={[['light', 'Light'], ['moderate', 'Moderate'], ['hard', 'Hard']]} />
          <Choice label="Jumping" value={form.jumping} onChange={(v) => setForm({ ...form, jumping: v })} testId="sport-jumping" options={[['little', 'Little'], ['some', 'Some'], ['lots', 'A lot']]} />
          <button
            type="button"
            className="btn btn-primary"
            data-testid="sport-save"
            onClick={async () => {
              await addSportLog(form);
              toast('Sport logged');
            }}
          >
            Save
          </button>
        </div>
      </Section>
      <Section title="Last four weeks">
        <div className="group" data-testid="sport-list">
          {logs.length === 0 && <Item title="Nothing logged yet" />}
          {[...logs]
            .sort((x, y) => y.date.localeCompare(x.date))
            .map((l) => (
              <Item
                key={l.id}
                title={`${l.sport === 'other' ? l.name || 'Other sport' : l.sport === 'volleyball' ? 'Volleyball' : 'Basketball'}, ${l.minutes} min`}
                sub={`${formatDateKey(l.date, { weekday: 'short', day: 'numeric', month: 'short' })} · ${l.intensity} · jumping ${l.jumping === 'lots' ? 'a lot' : l.jumping}`}
                end={
                  <button type="button" className="btn btn-sm btn-ghost" onClick={() => void deleteSportLog(l.id)}>
                    Remove
                  </button>
                }
              />
            ))}
        </div>
      </Section>
    </div>
  );
}
