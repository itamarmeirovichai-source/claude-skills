import { useEffect } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../db/db';
import { activePlan, activeSession, startSession } from '../db/repo';
import { useSettings } from '../ui/state';
import { usePlan, useToday } from '../ui/hooks';
import { Item, Note, PageHead, Section } from '../ui/components';
import { Link, navigate } from '../ui/router';
import { addDays, formatDateKey, weekdayOf, WEEKDAY_NAMES } from '../domain/dates';
import { SESSION_LABELS, type PlanDay, type PlanItem, type SessionKey } from '../content/plan';
import { exercise } from '../content/library';
import { BodyMap } from '../svg/BodyMap';
import { scheduleNotes, sessionTime } from '../services/training';
import type { MuscleId } from '../content/muscles';
import type { PlanRecord } from '../db/records';

export function targetText(it: PlanItem): string {
  const t = it.target;
  const per = it.per === 'side' ? ' per side' : it.per === 'direction' ? ' per direction' : '';
  switch (t.type) {
    case 'reps':
      return `${it.sets} × ${t.min === t.max ? t.min : `${t.min} to ${t.max}`}${per}`;
    case 'duration':
      return t.workSec ? `${t.totalMin} min, ${t.workSec / 60} min on, ${t.restSec} s off` : `${t.totalMin} min`;
    case 'hold':
      return `${it.sets} × ${t.seconds} s${per}`;
    case 'roundTrips':
      return `${it.sets} × ${t.count} round trips`;
  }
}

export function restText(sec: number): string {
  if (sec >= 60 && sec % 60 === 0) return `${sec / 60} min rest`;
  if (sec > 60) return `${Math.floor(sec / 60)} min ${sec % 60} s rest`;
  return `${sec} s rest`;
}

export function dayMuscles(items: PlanItem[]): { primary: MuscleId[]; secondary: MuscleId[]; exposure: MuscleId[] } {
  const p = new Set<MuscleId>();
  const s = new Set<MuscleId>();
  const e = new Set<MuscleId>();
  for (const it of items) {
    const ex = exercise(it.exerciseId);
    if (!ex) continue;
    const counts = ex.kind === 'strength' || ex.kind === 'bodyweight' || ex.kind === 'hold';
    for (const m of ex.muscles.primary) (counts ? p : e).add(m);
    for (const m of ex.muscles.secondary) if (counts) s.add(m);
  }
  for (const m of p) s.delete(m);
  for (const m of [...p, ...s]) e.delete(m);
  return { primary: [...p], secondary: [...s], exposure: [...e] };
}

export function TrainScreen() {
  const plan = usePlan();
  const today = useToday();
  const settings = useSettings();
  const week = useLiveQuery(() => db.sessions.where('date').between(addDays(today, -6), addDays(today, 6), true, true).toArray(), [today]);
  if (!plan) return null;
  const order = [0, 1, 2, 3, 4, 5, 6].map((i) => weekdayOf(addDays(today, i)));
  return (
    <div data-testid="train">
      <PageHead title="Train" eyebrow={plan.name} end={<Link to="/coverage" className="btn btn-sm btn-outline">Coverage</Link>} />
      <Section title="This week">
        <div className="group">
          {order.map((wd, i) => {
            const d = plan.days.find((x) => x.weekday === wd)!;
            const date = addDays(today, i);
            const done = (week ?? []).filter((s) => s.date === date && s.status === 'done' && s.planWeekday === wd).map((s) => s.session);
            const sessions = [...new Set(d.items.map((x) => x.session))];
            return (
              <Item
                key={wd}
                to={`/train/day/${wd}?date=${date}`}
                title={
                  <span>
                    {i === 0 ? 'Today' : WEEKDAY_NAMES[wd]} <span className="faint small">{formatDateKey(date, { day: 'numeric', month: 'short' })}</span>
                  </span>
                }
                sub={d.isRest ? 'Full rest and Sabbath' : `${d.title}. ${sessions.map((s) => SESSION_LABELS[s]).join(', ')}`}
                end={d.isRest ? undefined : done.length ? `${done.length} of ${sessions.length} done` : sessionTime(settings, wd, 'main')}
                testId={`train-day-${wd}`}
              />
            );
          })}
        </div>
      </Section>
      <Section title="Rules for every session">
        <div className="panel">
          <ul className="bullets small">
            {plan.globalRules.map((r) => (
              <li key={r}>{r}</li>
            ))}
          </ul>
        </div>
      </Section>
      <Section title="More">
        <div className="group">
          <Item title="Exercise library" sub="Instructions, muscles, visuals, and videos" to="/library" />
          <Item title="Muscle coverage this week" sub="Direct and indirect sets, shoulder load" to="/coverage" />
          <Item title="Edit the plan" sub="Changes create a new version. History keeps the original." to="/more/plan" />
        </div>
      </Section>
    </div>
  );
}

export function TrainDayScreen({ weekday, date }: { weekday: number; date: string | null }) {
  const plan = usePlan();
  const today = useToday();
  const settings = useSettings();
  const d = date ?? today;
  const sessions = useLiveQuery(() => db.sessions.where('date').equals(d).toArray(), [d]);
  const active = useLiveQuery(() => db.sessions.where('status').equals('active').first(), []);
  if (!plan || !sessions) return null;
  const day = plan.days.find((x) => x.weekday === weekday);
  if (!day) return <PageHead title="Not found" backTo="/train" />;
  const notes = scheduleNotes(settings, day, d);
  const isMoved = weekdayOf(d) !== weekday;
  return (
    <div data-testid="train-day">
      <PageHead title={day.title} eyebrow={`${WEEKDAY_NAMES[weekday]}${d !== today ? `, ${formatDateKey(d)}` : ''}`} backTo="/train" />
      {isMoved && (
        <Note tone="accent" title="Moved session">
          You are doing {WEEKDAY_NAMES[weekday]}'s plan on {formatDateKey(d)}. It replaces that day's session rather than adding to it.
        </Note>
      )}
      {day.isRest ? (
        <div className="panel stack">
          {day.restNotes?.map((n) => (
            <p key={n}>{n}</p>
          ))}
        </div>
      ) : (
        <>
          {notes.map((n) => (
            <div key={n} style={{ marginBottom: 8 }}>
              <Note tone="warn">{n}</Note>
            </div>
          ))}
          <Section title="Muscles in this workout">
            <BodyMap highlight={dayMuscles(day.items)} caption="Jumps, sprints, swims, rope, and warm ups are shown as activity exposure." />
          </Section>
          {(['morning', 'main', 'swim'] as SessionKey[]).map((s) => {
            const items = day.items.filter((i) => i.session === s);
            if (!items.length) return null;
            const done = sessions.find((x) => x.session === s && x.status === 'done' && x.planWeekday === weekday);
            const running = active && active.date === d && active.session === s && active.planWeekday === weekday ? active : undefined;
            return (
              <Section key={s} title={`${SESSION_LABELS[s]}, ${sessionTime(settings, weekday, s)}`}>
                <div className="group">
                  {items.map((it, i) => {
                    const ex = exercise(it.exerciseId);
                    return (
                      <Item
                        key={it.id}
                        to={`/exercise/${it.exerciseId}?item=${it.id}`}
                        title={`${i + 1}. ${ex?.name ?? it.exerciseId}`}
                        sub={[targetText(it), restText(it.restSec), it.rir !== undefined ? `${it.rir} RIR` : '', it.tempo ? `tempo ${it.tempo.split('').join(' ')}` : '', it.rpe ? `RPE ${it.rpe[0]} to ${it.rpe[1]}` : ''].filter(Boolean).join(' · ')}
                      />
                    );
                  })}
                </div>
                <div style={{ marginTop: 10 }}>
                  {running ? (
                    <button type="button" className="btn btn-primary btn-large btn-block" onClick={() => navigate(`/workout/${running.id}`)}>
                      Resume
                    </button>
                  ) : done ? (
                    <div className="row-between">
                      <span className="tag tag-accent">Done</span>
                      <Link to={`/workout/${done.id}`} className="btn btn-ghost">
                        View plan and actual
                      </Link>
                    </div>
                  ) : (
                    <button
                      type="button"
                      className="btn btn-primary btn-large btn-block"
                      disabled={!!active}
                      data-testid={`start-${s}`}
                      onClick={async () => {
                        const p = await activePlan();
                        const original = addDays(d, -((weekdayOf(d) - weekday + 7) % 7));
                        const ws = await startSession(d, s, items, s === 'main' ? day.title : SESSION_LABELS[s], p as PlanRecord, isMoved ? original : null, weekday);
                        navigate(`/workout/${ws.id}`);
                      }}
                    >
                      Start {SESSION_LABELS[s].toLowerCase()}
                    </button>
                  )}
                  {active && !running && <p className="small muted" style={{ marginTop: 6 }}>Finish the workout in progress first.</p>}
                </div>
              </Section>
            );
          })}
        </>
      )}
    </div>
  );
}

/** Home Screen shortcut target: resume or start the next session of the day. */
export function StartWorkoutRedirect() {
  const today = useToday();
  useEffect(() => {
    void (async () => {
      const a = await activeSession();
      if (a) return navigate(`/workout/${a.id}`, { replace: true });
      const plan = await activePlan();
      const wd = weekdayOf(today);
      const day: PlanDay | undefined = plan.days.find((x) => x.weekday === wd);
      if (!day || day.isRest) return navigate('/train', { replace: true });
      const done = (await db.sessions.where('date').equals(today).toArray()).filter((s) => s.status === 'done').map((s) => s.session);
      const hour = new Date().getHours();
      const order: SessionKey[] = hour < 11 ? ['morning', 'main', 'swim'] : ['main', 'swim', 'morning'];
      const next = order.find((s) => day.items.some((i) => i.session === s) && !done.includes(s));
      if (!next) return navigate(`/train/day/${wd}?date=${today}`, { replace: true });
      navigate(`/train/day/${wd}?date=${today}`, { replace: true });
    })();
  }, [today]);
  return <p className="muted">Opening today's workout…</p>;
}
