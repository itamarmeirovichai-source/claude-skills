import { useEffect, useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../db/db';
import { decideSuggestion, updateSession } from '../db/repo';
import type { ExerciseSession, SetLog, WorkoutSession } from '../db/records';
import { exercise, exerciseName } from '../content/library';
import { PageHead, Note, Section, Seg, Sheet, Stepper, useToast } from '../ui/components';
import { navigate, Link } from '../ui/router';
import { useTimer, useSettings } from '../ui/state';
import { SetLogger } from './SetLogger';
import { finishSession } from '../services/training';
import { BodyMap } from '../svg/BodyMap';
import { dayMuscles, targetText } from './Train';
import { keepAwake, releaseAwake } from '../lib/device';
import { IconBack } from '../ui/icons';

function elapsed(ms: number) {
  const m = Math.floor(ms / 60000);
  return m >= 60 ? `${Math.floor(m / 60)} h ${m % 60} min` : `${m} min`;
}

export function WorkoutScreen({ sessionId }: { sessionId: string }) {
  const session = useLiveQuery(() => db.sessions.get(sessionId), [sessionId]);
  const exs = useLiveQuery(() => db.exerciseSessions.where('sessionId').equals(sessionId).sortBy('order'), [sessionId]);
  const sets = useLiveQuery(() => db.setLogs.where('sessionId').equals(sessionId).toArray(), [sessionId]);
  const settings = useSettings();
  const [idx, setIdx] = useState<number | null>(null);
  const [finishOpen, setFinishOpen] = useState(false);
  const { now } = useTimer();

  useEffect(() => {
    if (session?.status === 'active' && settings.keepScreenOn) void keepAwake();
    return () => void releaseAwake();
  }, [session?.status, settings.keepScreenOn]);
  useEffect(() => {
    const root = document.documentElement;
    if (session?.status === 'active') root.dataset.focus = '1';
    else delete root.dataset.focus;
    return () => {
      delete root.dataset.focus;
    };
  }, [session?.status]);

  if (session === undefined || !exs || !sets) return null;
  if (session === null) return <PageHead title="Workout not found" backTo="/train" />;
  if (session.status !== 'active') return <WorkoutSummary session={session} exs={exs} sets={sets} />;

  const doneFor = (es: ExerciseSession) => {
    const item = session.planSnapshot.find((i) => i.id === es.planItemId);
    const ex = exercise(es.exerciseId);
    const need = (item?.sets ?? 1) * (item?.per || ex?.logSides ? 2 : 1);
    return es.skipped || sets.filter((s) => s.exerciseSessionId === es.id && !s.warmup).length >= need;
  };
  const firstOpen = exs.findIndex((e) => !doneFor(e));
  const current = idx ?? (firstOpen === -1 ? exs.length - 1 : firstOpen);
  const es = exs[current];
  const item = es ? session.planSnapshot.find((i) => i.id === es.planItemId) : undefined;
  const allDone = exs.every(doneFor);

  return (
    <div data-testid="workout">
      <div className="workout-head">
        <div className="workout-title">
          <button type="button" className="btn btn-icon btn-ghost" onClick={() => navigate('/today')} aria-label="Leave the workout screen. The workout stays open.">
            <IconBack />
          </button>
          <span className="t small">{session.title}</span>
          <span className="small muted num" style={{ whiteSpace: 'nowrap' }}>
            {current + 1}/{exs.length} · {elapsed(Math.max(0, now - session.startedAt))}
          </span>
          <button type="button" className={`btn btn-sm ${allDone ? 'btn-primary' : 'btn-outline'}`} onClick={() => setFinishOpen(true)} data-testid="finish-workout">
            Finish
          </button>
        </div>
        <nav className="ex-nav" aria-label="Exercises">
          {exs.map((e, i) => (
            <button key={e.id} type="button" className={doneFor(e) ? 'done' : ''} aria-current={i === current ? 'true' : undefined} onClick={() => setIdx(i)} aria-label={`${i + 1}. ${exerciseName(e.exerciseId)}${doneFor(e) ? ', done' : ''}`}>
              {i + 1}
              {i === current ? `. ${exerciseName(e.exerciseId).split(' ').slice(0, 2).join(' ')}` : ''}
            </button>
          ))}
        </nav>
      </div>
      <div style={{ marginTop: 16 }}>
        {es && item ? (
          <SetLogger
            key={es.id + es.exerciseId}
            session={session}
            es={es}
            item={item}
            isLast={current === exs.length - 1}
            onNext={() => {
              if (current < exs.length - 1) {
                setIdx(current + 1);
                window.scrollTo({ top: 0 });
              } else setFinishOpen(true);
            }}
          />
        ) : (
          <Note>No exercises in this session.</Note>
        )}
      </div>
      <FinishSheet open={finishOpen} onClose={() => setFinishOpen(false)} session={session} allDone={allDone} />
    </div>
  );
}

function FinishSheet({ open, onClose, session, allDone }: { open: boolean; onClose: () => void; session: WorkoutSession; allDone: boolean }) {
  const [rpe, setRpe] = useState<number | null>(session.session === 'main' ? 7 : 4);
  const [energy, setEnergy] = useState<number | null>(3);
  const [soreness, setSoreness] = useState<number | null>(1);
  const [note, setNote] = useState('');
  const [busy, setBusy] = useState(false);
  const toast = useToast();
  const timer = useTimer();
  return (
    <Sheet open={open} onClose={onClose} title="Finish workout" testId="finish-sheet">
      <div className="stack">
        {!allDone && <Note tone="warn">Some sets are not logged. That is fine. Progression is only suggested from complete exercises.</Note>}
        <Stepper label="Session effort, RPE 1 to 10" value={rpe} onChange={setRpe} min={1} max={10} testId="session-rpe" />
        <div>
          <div className="stepper-label">
            <span>Energy now</span>
          </div>
          <Seg label="Energy now" value={energy} onChange={setEnergy} options={[1, 2, 3, 4, 5].map((v) => ({ value: v, label: String(v) }))} />
        </div>
        <div>
          <div className="stepper-label">
            <span>Soreness</span>
          </div>
          <Seg label="Soreness" value={soreness} onChange={setSoreness} options={[{ value: 0, label: 'None' }, { value: 1, label: 'Mild' }, { value: 2, label: 'Quite' }, { value: 3, label: 'Very' }]} />
        </div>
        <label className="field">
          <span className="label">Note, optional</span>
          <textarea className="input" value={note} onChange={(e) => setNote(e.target.value)} maxLength={2000} placeholder="Massage, how the spikes felt, anything useful" />
        </label>
        <button
          type="button"
          className="btn btn-primary btn-large btn-block"
          disabled={busy}
          data-testid="confirm-finish"
          onClick={async () => {
            setBusy(true);
            timer.stop();
            const r = await finishSession(session, { sessionRpe: rpe, recovery: { energy, soreness }, note });
            toast(r.suggestions ? 'Workout saved. Next targets are ready to review.' : 'Workout saved');
            onClose();
          }}
        >
          Save workout
        </button>
        <button
          type="button"
          className="btn btn-ghost btn-block"
          onClick={async () => {
            await updateSession(session.id, { status: 'abandoned', finishedAt: Date.now() });
            timer.stop();
            onClose();
            navigate('/train');
          }}
        >
          Discard this workout
        </button>
      </div>
    </Sheet>
  );
}

function fmt(s: SetLog) {
  const b: string[] = [];
  if (s.side) b.push(s.side === 'left' ? 'L' : 'R');
  if (s.weightKg !== null) b.push(`${s.weightKg}×${s.reps ?? ''}`);
  else if (s.reps !== null) b.push(`${s.reps}`);
  if (s.seconds !== null && s.roundTrips === null) b.push(`${s.seconds}s`);
  if (s.roundTrips !== null) b.push(`${s.roundTrips} trips`);
  if (s.rir !== null) b.push(`@${s.rir}`);
  if (s.quality !== null) b.push(`q${s.quality}`);
  return b.join(' ');
}

function WorkoutSummary({ session, exs, sets }: { session: WorkoutSession; exs: ExerciseSession[]; sets: SetLog[] }) {
  const suggestions = useLiveQuery(() => db.suggestions.filter((s) => s.basedOnSessionId === session.id).toArray(), [session.id]);
  const four = useLiveQuery(() => db.fourReviews.filter((r) => r.sessionIds.includes(session.id)).toArray(), [session.id]);
  const muscles = dayMuscles(session.planSnapshot);
  return (
    <div data-testid="workout-summary">
      <PageHead title={session.title} eyebrow={`${session.date} · ${session.status === 'done' ? 'Saved' : 'Discarded'}`} backTo="/train" />
      {session.status === 'done' && (
        <div className="metric-row">
          <div className="metric">
            <div className="m-label">Work sets</div>
            <div className="m-value">{sets.filter((s) => !s.warmup).length}</div>
          </div>
          <div className="metric">
            <div className="m-label">Effort</div>
            <div className="m-value">{session.sessionRpe ?? 'none'}</div>
            <div className="m-sub">RPE out of 10</div>
          </div>
          <div className="metric">
            <div className="m-label">Duration</div>
            <div className="m-value">{session.finishedAt ? elapsed(session.finishedAt - session.startedAt) : 'none'}</div>
          </div>
        </div>
      )}

      {suggestions && suggestions.length > 0 && (
        <Section title="Next targets">
          <p className="small muted" style={{ marginBottom: 8 }}>Nothing changes until you confirm it.</p>
          <div className="group" data-testid="suggestions">
            {suggestions.map((s) => (
              <div className="item" key={s.id} style={{ alignItems: 'flex-start' }}>
                <span className="item-main">
                  <span className="item-sub" style={{ display: 'block' }}>{exerciseName(s.exerciseId)}</span>
                  <span className="item-title" style={{ display: 'block' }}>{s.title}</span>
                  <span className="item-sub" style={{ display: 'block' }}>{s.reason}</span>
                </span>
                <span className="item-end" style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                  {s.status === 'pending' && s.targets.length > 0 ? (
                    <>
                      <button type="button" className="btn btn-sm btn-primary" onClick={() => void decideSuggestion(s.id, 'accepted')} data-testid="accept-suggestion">
                        Use it
                      </button>
                      <button type="button" className="btn btn-sm btn-ghost" onClick={() => void decideSuggestion(s.id, 'dismissed')}>
                        Not now
                      </button>
                    </>
                  ) : (
                    <span className="tag">{s.status === 'accepted' ? 'Confirmed' : s.status === 'dismissed' ? 'Dismissed' : 'Noted'}</span>
                  )}
                </span>
              </div>
            ))}
          </div>
        </Section>
      )}

      {four && four.length > 0 && (
        <Section title="Four session review">
          <div className="group">
            {four.map((r) => (
              <div className="item" key={r.id} style={{ alignItems: 'flex-start' }}>
                <span className="item-main">
                  <span className="item-title" style={{ display: 'block' }}>
                    {exerciseName(r.exerciseId)}: {r.recommendation.replace('_', ' ')}
                  </span>
                  <span className="item-sub" style={{ display: 'block' }}>{r.summary}</span>
                  <ul className="bullets small muted" style={{ marginTop: 4 }}>
                    {r.details.map((d) => (
                      <li key={d}>{d}</li>
                    ))}
                  </ul>
                </span>
              </div>
            ))}
          </div>
        </Section>
      )}

      <Section title="Plan and actual">
        <div className="panel" style={{ padding: 0, overflowX: 'auto' }}>
          <table className="prev-table" data-testid="plan-vs-actual">
            <thead>
              <tr>
                <th>Exercise</th>
                <th>Plan</th>
                <th>Actual</th>
              </tr>
            </thead>
            <tbody>
              {exs.map((e) => {
                const item = session.planSnapshot.find((i) => i.id === e.planItemId);
                const xs = sets.filter((s) => s.exerciseSessionId === e.id && !s.warmup).sort((a, b) => a.completedAt - b.completedAt);
                return (
                  <tr key={e.id}>
                    <td>
                      <Link to={`/history/${e.exerciseId}`}>{exerciseName(e.exerciseId)}</Link>
                      {e.originalExerciseId && <div className="small faint">for {exerciseName(e.originalExerciseId)}</div>}
                    </td>
                    <td className="small">{item ? targetText(item) : ''}</td>
                    <td className="small">{e.skipped ? `Skipped: ${e.skipReason ?? ''}` : xs.map(fmt).join(', ') || 'Not logged'}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </Section>
      <Section title="Muscles trained">
        <BodyMap highlight={muscles} />
      </Section>
      {session.note && (
        <Section title="Note">
          <div className="panel pre-wrap">{session.note}</div>
        </Section>
      )}
    </div>
  );
}
