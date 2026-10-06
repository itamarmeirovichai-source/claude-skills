import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../db/db';
import { exposuresFor } from '../db/repo';
import { useAthlete, useToday, usePlan } from '../ui/hooks';
import { Item, Note, PageHead, Section, Metric } from '../ui/components';
import { LineChart } from '../ui/Chart';
import { Link } from '../ui/router';
import { addDays, diffDays, formatDateKey, reviewWeekStart, rangeKeys } from '../domain/dates';
import { morningWeights, rollingAverages, sevenDayAverage, nutritionAdjustment, dayTotals, STABLE_WEIGHT_NOTE } from '../domain/nutrition';
import { coverageFrom, focusChecks, shoulderOverlap, COVERAGE_WEIGHTS, planCoverageInputs, type CoverageInput } from '../domain/coverage';
import { exercise, exerciseName, allExercises } from '../content/library';
import { MUSCLES, MUSCLE_GROUP_LABELS, type MuscleId } from '../content/muscles';
import { BodyMap } from '../svg/BodyMap';
import { useSettings } from '../ui/state';
import type { SetLog } from '../db/records';
import { summarizeSets } from '../ui/format';
import { JumpTestsSection } from './JumpTests';

const lookup = (id: string) => {
  const e = exercise(id);
  return e ? { name: e.name, kind: e.kind, primary: e.muscles.primary, secondary: e.muscles.secondary, fatigueOverlap: e.fatigueOverlap } : undefined;
};

export function ProgressScreen() {
  const today = useToday();
  const settings = useSettings();
  const athlete = useAthlete();
  const hide = athlete.weight.hideNumbers;
  const weighOff = athlete.weight.mode === 'off';
  const creatine = settings.supplements.some((x) => x.kind === 'creatine' && x.active) || athlete.supplements.creatineProduct !== '';
  const from = addDays(today, -55);
  const data = useLiveQuery(async () => {
    const [checkins, waist, sleep, food, sessions, exSessions, sets] = await Promise.all([
      db.checkins.where('date').between(from, today, true, true).toArray(),
      db.waist.where('date').between(from, today, true, true).toArray(),
      db.sleep.where('date').between(addDays(today, -27), today, true, true).toArray(),
      db.foodLogs.where('date').between(addDays(today, -27), today, true, true).toArray(),
      db.sessions.where('date').between(addDays(today, -13), today, true, true).toArray(),
      db.exerciseSessions.toArray(),
      db.setLogs.where('completedAt').above(Date.now() - 14 * 86400000).toArray(),
    ]);
    return { checkins, waist, sleep, food, sessions, exSessions, sets };
  }, [today]);
  if (!data) return null;

  const weights = morningWeights(data.checkins);
  const avg = rollingAverages(weights, from, today).filter((w) => w.reliable && w.avg !== null).map((w) => ({ x: w.end, y: w.avg! }));
  const thisWeek = sevenDayAverage(weights, today);
  const lastWeek = sevenDayAverage(weights, addDays(today, -7));
  const bf = data.checkins.filter((c) => c.bodyFatPct !== null && c.standardConditions).map((c) => ({ x: c.date, y: c.bodyFatPct! }));
  const bfWeekly = rangeKeys(addDays(today, -49), 8)
    .map((_, i) => addDays(today, -7 * (7 - i)))
    .map((end) => {
      const xs = bf.filter((p) => p.x > addDays(end, -7) && p.x <= end);
      return xs.length >= 3 ? { x: end, y: xs.reduce((a, p) => a + p.y, 0) / xs.length } : null;
    })
    .filter((p): p is { x: string; y: number } => p !== null);
  const sleepPts = data.sleep.map((s) => ({ x: s.date, y: s.durationMin / 60 }));
  const foodDays = [...new Set(data.food.map((f) => f.date))];
  const gate = nutritionAdjustment({
    today,
    planStart: settings.planStartDate,
    checkins: data.checkins,
    waist: data.waist,
    foodLogDays: foodDays,
    performanceDecline: false,
    weightMode: athlete.weight.mode,
    wellbeing: {
      previous: wellbeing(data.checkins, data.sleep, addDays(today, -13), addDays(today, -7)),
      current: wellbeing(data.checkins, data.sleep, addDays(today, -6), today),
    },
  });
  const weekStart = reviewWeekStart(today);
  const weekFood = data.food.filter((f) => f.date >= weekStart);
  const weekFoodDays = [...new Set(weekFood.map((f) => f.date))];
  const proteinMeals = weekFood.filter((f) => dayTotals([f]).mid.protein >= 20).length;
  const quality = data.sets.filter((s) => s.quality !== null);
  const avgQuality = quality.length ? quality.reduce((a, s) => a + (s.quality ?? 0), 0) / quality.length : null;
  const homeSessions = data.sessions.filter((s) => (s.session === 'home' || s.session === 'morning') && s.status === 'done');
  const w = (k: 'energy' | 'mood' | 'concentration', start: string, end: string) => {
    const xs = data.checkins.filter((c) => c.date >= start && c.date <= end && c[k] !== null).map((c) => c[k]!);
    return xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : null;
  };

  return (
    <div data-testid="progress">
      <PageHead title="Progress" end={<Link to="/review" className="btn btn-sm btn-primary" data-testid="open-review">Weekly review</Link>} />

      <JumpTestsSection />

      {weighOff ? (
        <Section title="Body weight">
          <p className="small muted" data-testid="weight-off">Weighing is off. Change it in More, Your profile, Weighing. Training, recovery, and how you feel tell more day to day.</p>
        </Section>
      ) : hide ? (
        <Section title="Body weight">
          <p className="small muted" data-testid="weight-hidden">Weight numbers are hidden. They are still saved, and the weekly review reads the trend. Show them again in More, Your profile, Weighing.</p>
        </Section>
      ) : (
      <Section title="Body weight">
        <div className="metric-row">
          <Metric label="7 day average" value={thisWeek.reliable ? `${thisWeek.avg?.toFixed(1)} kg` : 'Not enough yet'} sub={`${thisWeek.count} morning weight${thisWeek.count === 1 ? '' : 's'}`} testId="weight-avg" />
          <Metric label="Week before" value={lastWeek.reliable ? `${lastWeek.avg?.toFixed(1)} kg` : 'Not enough yet'} sub={thisWeek.reliable && lastWeek.reliable ? weekChange((thisWeek.avg ?? 0) - (lastWeek.avg ?? 0)) : 'Needs 4 a week'} />
        </div>
        <div className="panel" style={{ marginTop: 8 }}>
          <LineChart points={weights.filter((p) => p.date >= from).map((p) => ({ x: p.date, y: p.kg }))} line={avg} unit="kg" label="Seven day average weight" />
          <p className="small muted">Dots are single mornings. The line is the seven day average, drawn only when a week has at least four morning weights. Daily changes of half a kilogram are normal water and food.</p>
        </div>
        {settings.planStartDate && diffDays(today, settings.planStartDate) < 21 && (
          <div style={{ marginTop: 8 }} data-testid="early-weight-note">
            <Note tone="info" title="Weight often rises a little in the first weeks">
              New training makes muscles hold more water and stored carbohydrate while they adapt, so the scale can go up for a week or two. Judge any trend over several weeks, together with your waist, performance, and how you feel.
            </Note>
          </div>
        )}
        <p className="small muted" style={{ marginTop: 8 }} data-testid="stable-note">
          {STABLE_WEIGHT_NOTE}
          {creatine ? ' Creatine usually adds some water to the muscles in the first weeks, often 1 to 2 kg, but not every rise is creatine.' : ''}
        </p>
      </Section>
      )}

      <Section title="Waist">
        <div className="panel">
          <LineChart points={data.waist.map((m) => ({ x: m.date, y: m.cm }))} line={data.waist.map((m) => ({ x: m.date, y: m.cm }))} unit="cm" label="Waist" />
          <p className="small muted">Measure once a week, same morning conditions, tape level at the navel.</p>
        </div>
      </Section>

      <Section title="Scale body fat, an uncertain estimate">
        <div className="panel">
          <Note tone="warn">Smart scales estimate body fat from an electrical signal. The number moves with water, food, timing, and creatine, and can be off by several percentage points. Scale "muscle" figures are not skeletal muscle. Watch a weekly trend at most, never the daily number.</Note>
          <div style={{ marginTop: 8 }}>
            {bfWeekly.length >= 2 ? <LineChart points={[]} line={bfWeekly} unit="%" label="Weekly average scale body fat" /> : <p className="small muted">Needs at least three readings a week for two weeks before a trend is shown.</p>}
          </div>
        </div>
      </Section>

      <Section title="Nutrition check">
        <div className="panel stack" data-testid="nutrition-gate">
          <h3>{gate.title}</h3>
          {gate.missing.length > 0 && (
            <ul className="bullets small muted">
              {gate.missing.map((m) => (
                <li key={m}>{m}</li>
              ))}
            </ul>
          )}
          {gate.reasons.length > 0 && (
            <ul className="bullets small">
              {gate.reasons.filter((m) => !hide || !/kg/.test(m)).map((m) => (
                <li key={m}>{m}</li>
              ))}
            </ul>
          )}
          <p className="small faint">Reads two or more weeks of data, never one day and never scale body fat. It never suggests eating less and never changes anything by itself{gate.involveGuardian ? '. Talk it through with a parent' : ''}.</p>
        </div>
      </Section>

      <Section title="Sleep">
        <div className="panel">
          <LineChart points={sleepPts} line={sleepPts} unit="h" label="Sleep duration" band={[8, 10]} />
          <p className="small muted">The shaded band is the 8 to 10 hour target for teens.</p>
        </div>
      </Section>

      <Section title="How you feel">
        <div className="metric-row">
          <Metric label="Energy" value={fmt1(w('energy', addDays(today, -6), today))} sub={priorWeekText(w('energy', addDays(today, -13), addDays(today, -7)))} />
          <Metric label="Mood" value={fmt1(w('mood', addDays(today, -6), today))} sub={priorWeekText(w('mood', addDays(today, -13), addDays(today, -7)))} />
          <Metric label="Concentration" value={fmt1(w('concentration', addDays(today, -6), today))} sub={priorWeekText(w('concentration', addDays(today, -13), addDays(today, -7)))} />
        </div>
        <p className="small faint" style={{ marginTop: 4 }}>Averages out of 5 from morning check ins.</p>
      </Section>

      <Section title="Training">
        <div className="metric-row">
          <Metric label="Sessions, 14 days" value={String(data.sessions.filter((s) => s.status === 'done').length)} />
          <Metric label="Jump and skill quality" value={avgQuality === null ? 'None yet' : `${avgQuality.toFixed(1)} / 5`} />
          <Metric label="Home sessions, 14 days" value={String(homeSessions.length)} />
        </div>
        <div className="group" style={{ marginTop: 8 }}>
          <Item title="Muscle coverage and weekly volume" sub="Direct and indirect sets, shoulder overlap" to="/coverage" testId="coverage-link" />
          <Item title="Exercise progress" sub="History and best comparable sets" to="/history/" />
        </div>
      </Section>

      <Section title="Meals this week">
        <div className="metric-row">
          <Metric label="Days logged" value={String(weekFoodDays.length)} />
          <Metric label="Meals with 20 g protein" value={String(proteinMeals)} />
          <Metric label="As planned" value={String(weekFood.filter((f) => f.asPlanned).length)} sub="meals" />
        </div>
      </Section>
    </div>
  );
}

function fmt1(n: number | null) {
  return n === null ? 'None yet' : n.toFixed(1);
}

function priorWeekText(n: number | null) {
  return n === null ? 'Nothing last week' : `last week ${n.toFixed(1)}`;
}

function wellbeing(checkins: Array<{ date: string; energy: number | null; mood: number | null; concentration: number | null }>, sleep: Array<{ date: string; durationMin: number }>, start: string, end: string) {
  const c = checkins.filter((x) => x.date >= start && x.date <= end);
  const a = (k: 'energy' | 'mood' | 'concentration') => {
    const xs = c.map((x) => x[k]).filter((v): v is number => v !== null);
    return xs.length >= 3 ? xs.reduce((p, q) => p + q, 0) / xs.length : null;
  };
  const s = sleep.filter((x) => x.date >= start && x.date <= end);
  return { energy: a('energy'), mood: a('mood'), concentration: a('concentration'), sleepHours: s.length >= 3 ? s.reduce((p, q) => p + q.durationMin, 0) / s.length / 60 : null };
}

// ---------- Coverage ----------

export function CoverageScreen() {
  const plan = usePlan();
  const today = useToday();
  const weekStart = reviewWeekStart(today);
  const done = useLiveQuery(async () => {
    const sessions = (await db.sessions.where('date').between(weekStart, addDays(weekStart, 6), true, true).toArray()).filter((s) => s.status === 'done');
    const sets = await db.setLogs.where('sessionId').anyOf(sessions.map((s) => s.id)).toArray();
    const byEx = new Map<string, { weekday: number; sets: Set<string> }>();
    for (const s of sets.filter((x) => !x.warmup)) {
      const ses = sessions.find((x) => x.id === s.sessionId)!;
      const key = `${s.exerciseId}:${ses.weekday}`;
      const cur = byEx.get(key) ?? { weekday: ses.weekday, sets: new Set<string>() };
      cur.sets.add(`${s.sessionId}:${s.setIndex}`);
      byEx.set(key, cur);
    }
    return [...byEx.entries()].map(([k, v]) => ({ exerciseId: k.split(':')[0]!, weekday: v.weekday, sets: v.sets.size }));
  }, [weekStart]);
  if (!plan || !done) return null;
  const planned = planCoverageInputs(plan.days);
  const covPlan = coverageFrom(planned, lookup);
  const covDone = coverageFrom(done as CoverageInput[], lookup);
  const focus = focusChecks(covPlan);
  const overlap = shoulderOverlap(planned, lookup);
  const groups = [...new Set(MUSCLES.map((m) => m.group))];
  const highlight = {
    primary: MUSCLES.filter((m) => covPlan[m.id].direct > 0).map((m) => m.id),
    secondary: MUSCLES.filter((m) => covPlan[m.id].direct === 0 && covPlan[m.id].indirect > 0).map((m) => m.id),
    exposure: MUSCLES.filter((m) => covPlan[m.id].direct === 0 && covPlan[m.id].indirect === 0 && covPlan[m.id].exposures > 0).map((m) => m.id) as MuscleId[],
  };
  return (
    <div data-testid="coverage">
      <PageHead title="Muscle coverage" eyebrow="Planned week and this week so far" backTo="/progress" />
      <BodyMap highlight={highlight} caption="Solid means direct sets, hatched means only indirect sets, dotted means activity exposure only." />

      <Section title="Checks you asked for">
        <div className="group" data-testid="focus-checks">
          {focus.map((f) => (
            <Item key={f.key} title={`${f.label}: ${f.present ? 'covered' : 'missing'}`} sub={`${f.directSets} direct and ${f.indirectSets} indirect weighted sets a week, ${f.exposures} activity exposures. ${f.exercises.slice(0, 8).join(', ')}.`} />
          ))}
        </div>
      </Section>

      <Section title="Shoulder load">
        <Note tone="warn" title="Pressing, volleyball, swimming, and shoulder care share one joint">
          <ul className="bullets small" style={{ marginTop: 4 }}>
            {overlap.notes.map((n) => (
              <li key={n}>{n}</li>
            ))}
          </ul>
        </Note>
        <div className="group" style={{ marginTop: 8 }} data-testid="shoulder-days">
          {overlap.days
            .filter((d) => d.items.length)
            .map((d) => (
              <Item key={d.weekday} title={['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][d.weekday]!} sub={d.items.map((i) => `${i.name} (${i.category.replace('-', ' ')}, ${i.sets} set${i.sets === 1 ? '' : 's'})`).join('; ')} />
            ))}
        </div>
      </Section>

      <Section title="Weekly sets by muscle">
        <p className="small muted" style={{ marginBottom: 8 }}>
          A work set counts {COVERAGE_WEIGHTS.primarySet} for a primary muscle and {COVERAGE_WEIGHTS.secondarySet} for a secondary muscle. Volleyball, jumps, swimming, rope, and warm ups count as activity exposure, not as hypertrophy sets. These are simple, transparent estimates, not measurements.
        </p>
        {groups.map((g) => (
          <div key={g} style={{ marginBottom: 12 }}>
            <div className="small" style={{ fontWeight: 650, margin: '0 4px 4px' }}>
              {MUSCLE_GROUP_LABELS[g]}
            </div>
            <div className="panel" style={{ padding: '8px 10px', overflowX: 'auto' }}>
              <table className="prev-table">
                <thead>
                  <tr>
                    <th>Muscle</th>
                    <th>Direct</th>
                    <th>Indirect</th>
                    <th>Exposure</th>
                    <th>Done</th>
                  </tr>
                </thead>
                <tbody>
                  {MUSCLES.filter((m) => m.group === g).map((m) => (
                    <tr key={m.id}>
                      <td>{m.shortName}</td>
                      <td>{covPlan[m.id].direct}</td>
                      <td>{covPlan[m.id].indirect}</td>
                      <td>{covPlan[m.id].exposures}</td>
                      <td>{covDone[m.id].direct + covDone[m.id].indirect}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ))}
        <p className="small faint">Direct, indirect, and exposure columns come from the plan. Done counts weighted sets logged since Monday.</p>
      </Section>
    </div>
  );
}

// ---------- Exercise history ----------

export function ExerciseHistoryScreen({ id }: { id: string }) {
  if (!id) return <ExercisePicker />;
  return <ExerciseHistory id={id} />;
}

function ExercisePicker() {
  const logged = useLiveQuery(async () => [...new Set((await db.setLogs.toArray()).map((s) => s.exerciseId))], []) ?? [];
  const list = allExercises().filter((e) => logged.includes(e.id));
  return (
    <div>
      <PageHead title="Exercise progress" backTo="/progress" />
      {list.length === 0 ? (
        <p className="muted">Log a workout to see progress here.</p>
      ) : (
        <div className="group">
          {list.map((e) => (
            <Item key={e.id} to={`/history/${e.id}`} title={e.name} />
          ))}
        </div>
      )}
    </div>
  );
}

function best(sets: SetLog[], rirTarget: number | null): SetLog | null {
  const ok = sets.filter((s) => !s.warmup && s.form === 'good' && s.pain === 'none' && (rirTarget === null || (s.rir ?? -1) >= rirTarget) && s.weightKg !== null && s.reps !== null);
  return ok.sort((a, b) => b.weightKg! - a.weightKg! || b.reps! - a.reps!)[0] ?? null;
}

function ExerciseHistory({ id }: { id: string }) {
  const plan = usePlan();
  const hist = useLiveQuery(() => exposuresFor(id), [id]);
  if (!hist) return null;
  const item = plan?.days.flatMap((d) => d.items).find((i) => i.exerciseId === id);
  const pr = best(hist.flatMap((h) => h.sets), item?.rir ?? null);
  const vol = hist.map((h) => ({ x: h.session.date, y: h.sets.reduce((a, s) => a + (s.weightKg ?? 0) * (s.reps ?? 0), 0) })).filter((p) => p.y > 0);
  return (
    <div data-testid="exercise-history">
      <PageHead title={exerciseName(id)} eyebrow="History" backTo="/progress" />
      <div className="metric-row">
        <Metric label="Sessions" value={String(hist.length)} />
        <Metric label="Best clean set" value={pr ? `${pr.weightKg} kg × ${pr.reps}` : 'None yet'} sub={item?.rir !== undefined ? `good form, ${item.rir}+ RIR, no pain` : 'good form, no pain'} />
      </div>
      {vol.length > 1 && (
        <Section title="Work done per session">
          <div className="panel">
            <LineChart points={vol} line={vol} unit="kg" label="Load times reps" decimals={0} />
          </div>
        </Section>
      )}
      <Section title="Sessions">
        <div className="group">
          {[...hist].reverse().map((h) => (
            <Item
              key={h.session.id}
              to={`/workout/${h.session.id}`}
              title={formatDateKey(h.session.date)}
              sub={summarizeSets(h.sets)}
            />
          ))}
        </div>
      </Section>
      <p className="small faint" style={{ marginTop: 12 }}>Personal bests only count sets with good form, the prescribed reps in reserve, and no pain.</p>
    </div>
  );
}

function weekChange(d: number): string {
  const r = Math.round(d * 10) / 10;
  if (r === 0) return 'About the same this week';
  return `${Math.abs(r).toFixed(1)} kg ${r > 0 ? 'higher' : 'lower'} this week`;
}
