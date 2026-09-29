import { useEffect, useMemo, useRef, useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../db/db';
import { currentTarget, decideSuggestion, deleteSet, lastExposure, logSet, restoreSet, updateExerciseSession } from '../db/repo';
import type { ExerciseSession, SetLog, WorkoutSession } from '../db/records';
import { exercise, sideLabel, sidesFor, equipmentType, allExercises } from '../content/library';
import type { PlanItem } from '../content/plan';
import { useSettings, useTimer } from '../ui/state';
import { Note, Seg, Sheet, Stepper, useToast } from '../ui/components';
import { Link } from '../ui/router';
import { IconTimer, IconUndo } from '../ui/icons';
import { restText, targetText } from './Train';
import { haptic } from '../lib/device';
import { summarizeSets } from '../ui/format';
import { incrementFor } from '../domain/progression';

type Side = 'left' | 'right' | null;

interface Draft {
  weightKg: number | null;
  reps: number | null;
  rir: number | null;
  seconds: number | null;
  form: SetLog['form'];
  pain: SetLog['pain'];
  painScore: number | null;
  quality: number | null;
  landing: SetLog['landing'];
  reachCm: number | null;
  timeSec: number | null;
  roundTrips: number | null;
  rpe: number | null;
  stroke: string | null;
  symptoms: string | null;
  note: string;
  warmup: boolean;
}

const QUALITY = ['jump', 'sprint', 'skill', 'throw'];

function fmtSet(s: SetLog): string {
  const bits: string[] = [];
  if (s.weightKg !== null) bits.push(`${s.weightKg} kg`);
  if (s.reps !== null) bits.push(s.weightKg !== null ? `× ${s.reps}` : `${s.reps} reps`);
  if (s.seconds !== null && s.roundTrips === null) bits.push(s.seconds >= 120 ? `${Math.round(s.seconds / 60)} min` : `${s.seconds} s`);
  if (s.roundTrips !== null) bits.push(`${s.roundTrips} round trips`);
  if (s.rir !== null) bits.push(`RIR ${s.rir}`);
  if (s.quality !== null) bits.push(`quality ${s.quality}/5`);
  if (s.timeSec !== null) bits.push(`${s.timeSec} s`);
  if (s.reachCm !== null) bits.push(`reach ${s.reachCm} cm`);
  if (s.rpe !== null) bits.push(`RPE ${s.rpe}`);
  return bits.join(' ');
}

export function SetLogger({ session, es, item, onNext, isLast }: { session: WorkoutSession; es: ExerciseSession; item: PlanItem; onNext: () => void; isLast: boolean }) {
  const settings = useSettings();
  const toast = useToast();
  const timer = useTimer();
  const ex = exercise(es.exerciseId);
  const sides = sidesFor(item, ex);
  const kind = ex?.kind ?? 'strength';
  const [extraSets, setExtraSets] = useState(0);
  const [subOpen, setSubOpen] = useState(false);
  const [skipOpen, setSkipOpen] = useState(false);
  const [noteOpen, setNoteOpen] = useState(false);

  const sets = useLiveQuery(() => db.setLogs.where('exerciseSessionId').equals(es.id).toArray(), [es.id]) ?? [];
  const last = useLiveQuery(() => lastExposure(es.exerciseId, session.id), [es.exerciseId, session.id]);
  const target = useLiveQuery(() => currentTarget(item.id, es.exerciseId), [item.id, es.exerciseId]);

  const work = sets.filter((s) => !s.warmup).sort((a, b) => a.completedAt - b.completedAt);
  const warm = sets.filter((s) => s.warmup);
  const totalSets = item.sets + extraSets;
  // Sequence of set slots, alternating sides for unilateral work.
  const slots = useMemo(() => {
    const out: Array<{ setIndex: number; side: Side }> = [];
    for (let i = 0; i < totalSets; i++) for (const sd of sides) out.push({ setIndex: i, side: sd });
    return out;
  }, [totalSets, sides]);
  const doneKeys = new Set(work.map((s) => `${s.setIndex}:${s.side}`));
  const skippedKey = (k: string) => skipped.includes(k);
  const [skipped, setSkipped] = useState<string[]>([]);
  const nextSlot = slots.find((s) => !doneKeys.has(`${s.setIndex}:${s.side}`) && !skippedKey(`${s.setIndex}:${s.side}`));

  const prevFor = (setIndex: number, side: Side) => last?.sets.find((s) => s.setIndex === setIndex && s.side === side) ?? last?.sets.find((s) => s.side === side) ?? last?.sets[0];
  const targetFor = (setIndex: number, side: Side) => (target?.targets ?? []).find((t) => t.setIndex === setIndex && t.side === side);

  const defaults = (slot: { setIndex: number; side: Side } | undefined, justLogged?: SetLog): Draft => {
    const p = slot ? prevFor(slot.setIndex, slot.side) : undefined;
    const tg = slot && target?.status === 'accepted' ? targetFor(slot.setIndex, slot.side) : undefined;
    const lastLogged = justLogged ?? work[work.length - 1];
    const t = item.target;
    return {
      weightKg: tg?.weightKg ?? lastLogged?.weightKg ?? p?.weightKg ?? null,
      reps: tg?.reps ?? (t.type === 'reps' ? (QUALITY.includes(kind) ? t.max : (p?.reps ?? lastLogged?.reps ?? t.min)) : null),
      rir: item.rir ?? null,
      seconds: t.type === 'hold' ? t.seconds : t.type === 'duration' ? t.totalMin * 60 : null,
      form: 'good',
      pain: 'none',
      painScore: null,
      quality: QUALITY.includes(kind) ? 4 : null,
      landing: kind === 'jump' ? 'good' : null,
      reachCm: null,
      timeSec: null,
      roundTrips: t.type === 'roundTrips' ? t.count : null,
      rpe: item.rpe ? item.rpe[0] : kind === 'swim' ? 4 : null,
      stroke: kind === 'swim' ? 'Freestyle' : null,
      symptoms: null,
      note: '',
      warmup: false,
    };
  };

  const slotKey = nextSlot ? `${nextSlot.setIndex}:${nextSlot.side}` : 'none';
  const [draft, setDraft] = useState<Draft>(() => defaults(nextSlot));
  // The next set's inputs are prepared the moment a set is completed, so a fast tap or
  // typed value is never overwritten when the stored set list catches up.
  const prepared = useRef<string | null>(null);
  const touched = useRef(false);
  useEffect(() => {
    if (prepared.current === slotKey) return;
    prepared.current = slotKey;
    touched.current = false;
    setDraft(defaults(nextSlot));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [slotKey]);
  useEffect(() => {
    // Last performance and targets load a moment later. Fill them in unless the user already typed.
    if (!touched.current) setDraft(defaults(nextSlot));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [target?.id, target?.status, last?.session.id]);
  const set = (patch: Partial<Draft>) => {
    touched.current = true;
    setDraft((d) => ({ ...d, ...patch }));
  };

  if (!ex) return <Note tone="warn">This exercise is missing from the library.</Note>;

  const eqStep = kind === 'strength' ? incrementFor(equipmentType(ex), settings.equipment) || 2.5 : 1;
  const prev = nextSlot ? prevFor(nextSlot.setIndex, nextSlot.side) : undefined;
  const complete = async () => {
    if (!nextSlot && !draft.warmup) return;
    const slot = nextSlot ?? { setIndex: 0, side: null };
    const rec = await logSet({
      sessionId: session.id,
      exerciseSessionId: es.id,
      exerciseId: es.exerciseId,
      planItemId: item.id,
      setIndex: draft.warmup ? warm.length : slot.setIndex,
      side: slot.side,
      warmup: draft.warmup,
      weightKg: draft.weightKg,
      reps: draft.reps,
      rir: kind === 'strength' || kind === 'bodyweight' ? draft.rir : null,
      seconds: draft.seconds,
      form: draft.form,
      pain: draft.pain,
      painScore: draft.pain === 'none' ? null : draft.painScore,
      quality: draft.quality,
      landing: draft.landing,
      reachCm: draft.reachCm,
      timeSec: draft.timeSec,
      roundTrips: draft.roundTrips,
      stroke: draft.stroke,
      rpe: draft.rpe,
      symptoms: draft.symptoms,
      note: draft.note.trim().slice(0, 2000),
      completedAt: Date.now(),
    });
    haptic(15);
    if (!draft.warmup) {
      const done = new Set([...doneKeys, `${slot.setIndex}:${slot.side}`]);
      const upcoming = slots.find((x) => !done.has(`${x.setIndex}:${x.side}`) && !skippedKey(`${x.setIndex}:${x.side}`));
      prepared.current = upcoming ? `${upcoming.setIndex}:${upcoming.side}` : 'none';
      touched.current = false;
      setDraft(defaults(upcoming, rec));
    } else {
      touched.current = false;
      setDraft((d) => ({ ...d, warmup: false }));
    }
    toast(draft.warmup ? 'Warm up set saved. It does not count as a work set.' : 'Set saved', {
      label: 'Undo',
      run: () => void deleteSet(rec.id),
    });
    const isFinalSlot = !draft.warmup && slots.filter((s) => !doneKeys.has(`${s.setIndex}:${s.side}`)).length <= 1;
    if (settings.autoStartRest && !(isFinalSlot && isLast) && item.restSec > 0 && draft.pain !== 'stop') {
      // Between sides of the same set, rest briefly; between sets, use the prescribed rest.
      const betweenSides = sides.length > 1 && slot.side === 'left';
      timer.start(`${ex.name}${betweenSides ? ', switch sides' : ''}`, betweenSides ? Math.min(30, item.restSec) : item.restSec, ex.id);
    }
    setNoteOpen(false);
  };

  const copyLast = () => {
    const l = work[work.length - 1];
    if (!l) return;
    set({ weightKg: l.weightKg, reps: l.reps, rir: l.rir, seconds: l.seconds, form: l.form, quality: l.quality, landing: l.landing, roundTrips: l.roundTrips, rpe: l.rpe });
  };

  const allDone = !nextSlot;
  const stopPain = draft.pain === 'stop';

  return (
    <div className="stack" data-testid="set-logger">
      <div>
        <div className="row-between" style={{ alignItems: 'flex-start' }}>
          <h2 className="grow" data-testid="exercise-name">
            {ex.name}
          </h2>
          <Link to={`/exercise/${ex.id}?item=${item.id}`} className="btn btn-sm btn-ghost">
            How to
          </Link>
        </div>
        {es.originalExerciseId && (
          <p className="small muted">
            Instead of {exercise(es.originalExerciseId)?.name}. {es.substitutionReason}
          </p>
        )}
        <div className="presc" style={{ marginTop: 6 }} data-testid="prescription">
          <span>
            <b>{targetText(item)}</b>
          </span>
          {item.rir !== undefined && (
            <span>
              <b>{item.rir} RIR</b>
            </span>
          )}
          {item.tempo && <span>tempo {item.tempo.split('').join(' ')}</span>}
          {item.rpe && <span>RPE {item.rpe[0]} to {item.rpe[1]}</span>}
          <span>{restText(item.restSec)}</span>
        </div>
        {item.notes.length > 0 && <p className="small muted" style={{ marginTop: 4 }}>{item.notes.join(' ')}</p>}
      </div>

      {/* Last performance and next target, always visible above the inputs */}
      <div className="group">
        <div className="item" data-testid="last-performance">
          <span className="item-main">
            <span className="item-sub" style={{ display: 'block' }}>
              Last time{last ? `, ${last.session.date}` : ''}
            </span>
            <span className="item-title num" style={{ display: 'block' }}>
              {last ? summarizeSets(last.sets) : firstTimeText(ex?.kind)}
            </span>
          </span>
        </div>
        {target && target.kind !== 'quality_hold' && (
          <div className="item" data-testid="next-target">
            <span className="item-main">
              <span className="item-sub" style={{ display: 'block' }}>
                {target.status === 'accepted' ? 'Target today' : 'Suggested target, not confirmed'}
              </span>
              <span className="item-title" style={{ display: 'block' }}>
                {target.title}
                {target.targets.length > 0 && (
                  <span className="num muted">
                    {'  '}
                    {target.targets.map((t) => `${t.weightKg !== null ? `${t.weightKg}×` : ''}${t.reps ?? t.seconds ?? ''}`).join(', ')}
                  </span>
                )}
              </span>
              <span className="item-sub" style={{ display: 'block' }}>{target.reason}</span>
            </span>
            {target.status === 'pending' && (
              <span className="item-end" style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                <button type="button" className="btn btn-sm btn-primary" onClick={() => void decideSuggestion(target.id, 'accepted')}>
                  Use it
                </button>
                <button type="button" className="btn btn-sm btn-ghost" onClick={() => void decideSuggestion(target.id, 'dismissed')}>
                  Not now
                </button>
              </span>
            )}
          </div>
        )}
      </div>

      {/* Logged sets */}
      {(work.length > 0 || warm.length > 0) && (
        <div className="stack" style={{ gap: 6 }} data-testid="logged-sets">
          {[...warm, ...work].map((s) => (
            <div className="set-card logged row-between" key={s.id}>
              <div className="set-summary grow">
                <span className="tag">{s.warmup ? 'Warm up' : `Set ${s.setIndex + 1}${s.side ? ` ${sideLabel(item, s.side)}` : ''}`}</span>
                <span className="num">{fmtSet(s)}</span>
                {s.form && s.form !== 'good' && <span className="tag tag-warn">form {s.form}</span>}
                {s.pain !== 'none' && <span className="tag tag-danger">pain {s.painScore ?? s.pain}</span>}
              </div>
              {!s.warmup && item.restSec > 0 && (
                <button type="button" className="btn btn-sm btn-ghost" aria-label="Start rest timer" onClick={() => timer.start(ex.name, item.restSec, ex.id)}>
                  <IconTimer size={20} />
                </button>
              )}
              <button
                type="button"
                className="btn btn-sm btn-ghost"
                aria-label="Delete set"
                onClick={async () => {
                  const removed = await deleteSet(s.id);
                  if (removed) toast('Set deleted', { label: 'Undo', run: () => void restoreSet(removed) });
                }}
              >
                <IconUndo size={20} />
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Current set */}
      {!allDone || draft.warmup ? (
        <div className="set-card" data-testid="current-set">
          <div className="set-head">
            <h3>
              {draft.warmup ? 'Warm up set' : `Set ${(nextSlot?.setIndex ?? 0) + 1} of ${totalSets}`}
              {nextSlot?.side && !draft.warmup ? `, ${sideLabel(item, nextSlot.side)}` : ''}
            </h3>
            {(kind === 'strength' || kind === 'bodyweight') && (
              <label className="row small" style={{ gap: 6 }}>
                <input type="checkbox" checked={draft.warmup} onChange={(e) => set({ warmup: e.target.checked })} data-testid="warmup-toggle" className="check" />
                Warm up
              </label>
            )}
          </div>
          <div className="stack">
            {(kind === 'strength' || kind === 'bodyweight') && (
              <div className="set-inputs">
                {kind === 'strength' && (
                  <Stepper label="Weight" unit="kg" value={draft.weightKg} onChange={(v) => set({ weightKg: v })} step={eqStep} decimals={2} max={500} prev={prev?.weightKg !== null && prev?.weightKg !== undefined ? `${prev.weightKg}` : undefined} testId="input-weight" />
                )}
                <Stepper label="Reps" value={draft.reps} onChange={(v) => set({ reps: v })} max={100} prev={prev?.reps !== null && prev?.reps !== undefined ? `${prev.reps}` : undefined} testId="input-reps" />
              </div>
            )}
            {kind === 'hold' && <Stepper label="Seconds held" value={draft.seconds} onChange={(v) => set({ seconds: v })} step={5} max={600} prev={prev?.seconds ? `${prev.seconds}` : undefined} testId="input-seconds" />}
            {QUALITY.includes(kind) && (
              <>
                <Stepper label="Good quality reps" value={draft.reps} onChange={(v) => set({ reps: v })} max={20} prev={prev?.reps ? `${prev.reps}` : undefined} testId="input-reps" />
                <div>
                  <div className="stepper-label">
                    <span>Quality</span>
                    {prev?.quality && <span className="prev">Last {prev.quality}</span>}
                  </div>
                  <Seg label="Quality" value={draft.quality} onChange={(v) => set({ quality: v })} options={[1, 2, 3, 4, 5].map((q) => ({ value: q, label: String(q) }))} />
                  <p className="hint">5 means your best height, speed, and control today.</p>
                </div>
                {kind === 'jump' && (
                  <div>
                    <div className="stepper-label">
                      <span>Landing</span>
                    </div>
                    <Seg label="Landing" value={draft.landing} onChange={(v) => set({ landing: v })} options={[{ value: 'good', label: 'Soft, stable' }, { value: 'ok', label: 'OK' }, { value: 'poor', label: 'Poor', tone: 'warn' }]} />
                  </div>
                )}

              </>
            )}
            {(kind === 'conditioning' || kind === 'warmup') && (
              <Stepper label="Minutes done" value={draft.seconds === null ? null : Math.round(draft.seconds / 60)} onChange={(v) => set({ seconds: v === null ? null : v * 60 })} max={120} testId="input-minutes" />
            )}
            {kind === 'swim' && (
              <>
                <div className="set-inputs">
                  <Stepper label="Round trips" value={draft.roundTrips} onChange={(v) => set({ roundTrips: v })} max={100} prev={prev?.roundTrips ? `${prev.roundTrips}` : undefined} testId="input-trips" />
                  <Stepper label="Effort RPE" value={draft.rpe} onChange={(v) => set({ rpe: v })} max={10} min={1} />
                </div>
                <PoolLength session={session} />
                <div>
                  <div className="stepper-label">
                    <span>Stroke</span>
                  </div>
                  <Seg label="Stroke" value={draft.stroke} onChange={(v) => set({ stroke: v })} options={['Freestyle', 'Breaststroke', 'Backstroke', 'Mixed'].map((s) => ({ value: s, label: s === 'Breaststroke' ? 'Breast' : s === 'Backstroke' ? 'Back' : s === 'Freestyle' ? 'Free' : s }))} />
                </div>
                <label className="field">
                  <span className="label">Symptoms, if any</span>
                  <input className="input" value={draft.symptoms ?? ''} placeholder="None" onChange={(e) => set({ symptoms: e.target.value || null })} maxLength={300} />
                </label>
                {draft.symptoms && /chest|breath|dizz|faint/i.test(draft.symptoms) && (
                  <Note tone="danger" title="Stop and get help">
                    Chest pain, unusual breathlessness, dizziness, or fainting means stop swimming now, tell an adult, and get medical help.
                  </Note>
                )}
              </>
            )}
            {(kind === 'strength' || kind === 'bodyweight') && (
              <div>
                <div className="stepper-label">
                  <span>Reps in reserve</span>
                  <span className="prev">{item.rir !== undefined ? `Target ${item.rir}` : ''}</span>
                </div>
                <Seg label="Reps in reserve" value={draft.rir} onChange={(v) => set({ rir: v })} options={[0, 1, 2, 3, 4, 5].map((r) => ({ value: r, label: String(r), tone: item.rir !== undefined && r < item.rir ? ('warn' as const) : undefined }))} />
                {draft.rir !== null && item.rir !== undefined && draft.rir < item.rir && <p className="hint">Below the target. Next set, stop a rep or two earlier.</p>}
              </div>
            )}
            {kind !== 'swim' && kind !== 'warmup' && (
              <div>
                <div className="stepper-label">
                  <span>Form</span>
                </div>
                <Seg label="Form" value={draft.form} onChange={(v) => set({ form: v })} options={[{ value: 'good', label: 'Good' }, { value: 'acceptable', label: 'Acceptable' }, { value: 'poor', label: 'Poor', tone: 'warn' }]} />
              </div>
            )}
            <div>
              <div className="stepper-label">
                <span>Pain</span>
              </div>
              <Seg
                label="Pain"
                value={draft.pain}
                onChange={(v) => set({ pain: v, painScore: v === 'none' ? null : v === 'mild' ? 2 : 5 })}
                options={[{ value: 'none', label: 'None' }, { value: 'mild', label: 'Mild', tone: 'warn' }, { value: 'stop', label: 'Had to stop', tone: 'danger' }]}
              />
              {draft.pain !== 'none' && (
                <div style={{ marginTop: 8 }}>
                  <Stepper label="Pain score out of 10" value={draft.painScore} onChange={(v) => set({ painScore: v })} min={1} max={10} testId="input-pain" />
                </div>
              )}
              {(stopPain || (draft.painScore ?? 0) >= 4) && (
                <div style={{ marginTop: 8 }}>
                  <Note tone="danger" title="Pause this exercise">
                    Pain of 4 out of 10 or more, or pain that changes your technique, means stop this exercise today and tell a parent or coach. Pain tracking is not a diagnosis.
                  </Note>
                </div>
              )}
            </div>
            {QUALITY.includes(kind) && (kind === 'jump' || kind === 'sprint') && (
                <details className="disclosure">
                    <summary>Optional measures</summary>
                    <div className="set-inputs">
                      {kind === 'jump' && <Stepper label="Reach" unit="cm" value={draft.reachCm} onChange={(v) => set({ reachCm: v })} max={400} />}
                      {kind === 'sprint' && <Stepper label="Time" unit="s" value={draft.timeSec} onChange={(v) => set({ timeSec: v })} step={0.01} decimals={2} max={60} />}
                    </div>
                  </details>
            )}
            {noteOpen ? (
              <label className="field">
                <span className="label">Note</span>
                <textarea className="input" value={draft.note} onChange={(e) => set({ note: e.target.value })} maxLength={2000} />
              </label>
            ) : (
              <button type="button" className="btn btn-ghost" style={{ alignSelf: 'flex-start' }} onClick={() => setNoteOpen(true)}>
                Add a note
              </button>
            )}
          </div>
          <div className="stack" style={{ marginTop: 14 }}>
            <div className="action-row">
              <button type="button" className="btn btn-outline btn-sm" onClick={copyLast} disabled={!work.length}>
                Copy last
              </button>
              <button type="button" className="btn btn-outline btn-sm" onClick={() => nextSlot && setSkipped((s) => [...s, `${nextSlot.setIndex}:${nextSlot.side}`])} data-testid="skip-set">
                Skip set
              </button>
              <button type="button" className="btn btn-outline btn-sm" onClick={() => timer.start(ex.name, item.restSec, ex.id)} data-testid="start-rest">
                Rest {item.restSec >= 60 ? `${Math.round((item.restSec / 60) * 10) / 10} min` : `${item.restSec} s`}
              </button>
            </div>
          </div>
          <p className="small muted" style={{ marginTop: 10 }}>
            {QUALITY.includes(kind)
              ? 'Stop the set as soon as height, speed, landing, or coordination drops.'
              : kind === 'swim'
                ? 'Easy to moderate, RPE 4 to 5. Stop for chest pain, dizziness, or unusual breathlessness.'
                : `Stop when technique changes, pain appears, or you reach ${item.rir ?? 2} reps in reserve.`}
          </p>
        </div>
      ) : (
        <div className="panel stack" data-testid="exercise-done">
          <p>
            <b>All sets logged.</b> {work.length} work set{work.length === 1 ? '' : 's'}.
          </p>
          <div className="grid-2">
            <button type="button" className="btn btn-outline" onClick={() => setExtraSets((n) => n + 1)} data-testid="add-set">
              Add set
            </button>
            <button type="button" className="btn btn-primary" onClick={onNext} data-testid="next-exercise">
              {isLast ? 'Finish' : 'Next exercise'}
            </button>
          </div>
          <p className="small muted">Extra sets are logged but never needed. Stopping at the plan is the right default.</p>
        </div>
      )}

      <div className="row wrap" style={{ gap: 8 }}>
        <button type="button" className="btn btn-sm btn-outline" onClick={() => setSubOpen(true)} data-testid="substitute">
          Substitute
        </button>
        <button type="button" className="btn btn-sm btn-outline" onClick={() => setSkipOpen(true)}>
          Skip exercise
        </button>
        {!allDone && (
          <button type="button" className="btn btn-sm btn-outline" onClick={() => setExtraSets((n) => n + 1)}>
            Add set
          </button>
        )}
      </div>

      <div className="dock" data-testid="workout-dock">
        <div className="dock-inner">
          {!allDone || draft.warmup ? (
            <button type="button" className="btn btn-primary btn-large grow" onClick={() => void complete()} data-testid="complete-set">
              {draft.warmup ? 'Save warm up set' : `Complete set ${(nextSlot?.setIndex ?? 0) + 1}${nextSlot?.side ? ` ${sideLabel(item, nextSlot.side).toLowerCase()}` : ''}`}
            </button>
          ) : (
            <button type="button" className="btn btn-primary btn-large grow" onClick={onNext} data-testid="dock-next">
              {isLast ? 'Finish workout' : 'Next exercise'}
            </button>
          )}
        </div>
      </div>

      <SubstituteSheet open={subOpen} onClose={() => setSubOpen(false)} es={es} />
      <Sheet open={skipOpen} onClose={() => setSkipOpen(false)} title="Skip this exercise">
        <div className="stack">
          <p className="muted">Skipping is fine. A reason helps the weekly review.</p>
          {['Pain or discomfort', 'Equipment busy', 'Out of time', 'Coach changed the plan', 'Feeling unwell'].map((r) => (
            <button
              key={r}
              type="button"
              className="btn btn-outline btn-block"
              onClick={async () => {
                await updateExerciseSession(es.id, { skipped: true, skipReason: r });
                setSkipOpen(false);
                onNext();
              }}
            >
              {r}
            </button>
          ))}
        </div>
      </Sheet>
    </div>
  );
}

function PoolLength({ session }: { session: WorkoutSession }) {
  const settings = useSettings();
  const [len, setLen] = useState<number | null>(session.poolLengthM ?? settings.poolLengthM);
  return (
    <div>
      <Stepper
        label="Pool length"
        unit="m"
        value={len}
        onChange={async (v) => {
          setLen(v);
          await db.sessions.update(session.id, { poolLengthM: v, updatedAt: Date.now() });
          if (v) await db.settings.update('app', { poolLengthM: v, updatedAt: Date.now() });
        }}
        step={1}
        max={100}
      />
      <p className="hint">{len ? `Ten round trips is ${len * 20} m at this pool length.` : 'Distance is only shown once you set the pool length.'}</p>
    </div>
  );
}

function SubstituteSheet({ open, onClose, es }: { open: boolean; onClose: () => void; es: ExerciseSession }) {
  const [reason, setReason] = useState('Equipment busy');
  const [q, setQ] = useState('');
  const orig = exercise(es.originalExerciseId ?? es.exerciseId);
  const options = orig ? [orig.easierSubstitution, orig.equipmentSubstitution, ...(orig.otherSubstitutions ?? [])].filter((s) => s.exerciseId) : [];
  const results = q.length >= 2 ? allExercises().filter((e) => e.name.toLowerCase().includes(q.toLowerCase())).slice(0, 8) : [];
  const choose = async (id: string) => {
    await updateExerciseSession(es.id, { exerciseId: id, originalExerciseId: es.originalExerciseId ?? es.exerciseId, substitutionReason: reason });
    onClose();
  };
  return (
    <Sheet open={open} onClose={onClose} title="Substitute exercise">
      <div className="stack">
        <label className="field">
          <span className="label">Reason</span>
          <select className="input" value={reason} onChange={(e) => setReason(e.target.value)}>
            {['Equipment busy', 'Equipment missing', 'Pain or discomfort', 'Easier version today', 'Coach suggestion'].map((r) => (
              <option key={r}>{r}</option>
            ))}
          </select>
        </label>
        {options.length > 0 && (
          <div className="group">
            {options.map((o) => (
              <button type="button" className="item" key={o.name} onClick={() => void choose(o.exerciseId!)}>
                <span className="item-main">
                  <span className="item-title" style={{ display: 'block' }}>{o.name}</span>
                  <span className="item-sub" style={{ display: 'block' }}>{o.reason}</span>
                </span>
              </button>
            ))}
          </div>
        )}
        {orig && (
          <p className="small muted">
            Other options without a library entry: {[orig.easierSubstitution, orig.equipmentSubstitution, ...(orig.otherSubstitutions ?? [])].filter((s) => !s.exerciseId).map((s) => s.name).join(', ') || 'none'}.
          </p>
        )}
        <label className="field">
          <span className="label">Search the library</span>
          <input className="input" value={q} onChange={(e) => setQ(e.target.value)} placeholder="For example, row" />
        </label>
        {results.length > 0 && (
          <div className="group">
            {results.map((e) => (
              <button type="button" className="item" key={e.id} onClick={() => void choose(e.id)}>
                <span className="item-main">{e.name}</span>
              </button>
            ))}
          </div>
        )}
        <p className="small muted">The original prescription stays in the session history. To make a permanent change, edit the plan in More.</p>
      </div>
    </Sheet>
  );
}

function firstTimeText(kind: string | undefined): string {
  if (kind === 'strength') return 'First time. Pick a load you can control with the prescribed reps in reserve.';
  if (kind === 'bodyweight' || kind === 'hold') return 'First time. Use a version you can do with good form and reps in reserve.';
  if (kind === 'jump' || kind === 'sprint' || kind === 'throw' || kind === 'skill') return 'First time. Keep every rep fast and controlled, and stop when quality drops.';
  return 'First time. Follow the prescription at an easy, steady effort.';
}
