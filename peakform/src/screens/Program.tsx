import { useEffect, useState } from 'react';
import { exercise } from '../content/library';
import { ACTIVE_SLOTS, PROGRAM_DAYS, SLOT_BY_ID, normalizePicks, slotExposures, togglePick, type ProgramPicks, type ProgramSlot } from '../content/program';
import type { LibraryExerciseId } from '../content/exercises/ids';
import { WEEKDAY_NAMES } from '../domain/dates';
import { contacts } from '../content/phases';
import { JUMP_LEVEL_LABEL } from '../content/homeSessions';
import { draftPicks, jumpLevel, proposePlan, saveDraftPicks } from '../services/planUpdate';
import { PoseSvg } from '../svg/Figures';
import { Item, Note, PageHead, Section, useToast } from '../ui/components';
import { Link, navigate } from '../ui/router';
import { usePlan } from '../ui/hooks';
import { useLiveQuery } from 'dexie-react-hooks';
import { wristLoad, WRIST_TEXT } from '../content/traits';

// The exercise questionnaire. One step per muscle head. Every option in a step trains that head
// about equally, so the choice is about what the athlete enjoys and what the gym has.

function effortLabel(id: string): string {
  const ex = exercise(id);
  if (ex?.kind === 'hold') return 'Timed hold';
  const w = wristLoad(id);
  return `Stops about two reps short${w === 'high' ? '. Heavy on the wrist' : ''}`;
}


function OptionCard({ id, rank, onTap }: { id: LibraryExerciseId; rank: number; onTap: () => void }) {
  const ex = exercise(id);
  if (!ex) return null;
  const pose = ex.visual.poses?.[1] ?? ex.visual.poses?.[0];
  const chosen = rank >= 0;
  return (
    <div className={`choice${chosen ? ' chosen' : ''}`}>
      <button type="button" className="choice-main" onClick={onTap} aria-pressed={chosen} data-testid={`choice-${id}`}>
        <span className="choice-fig" aria-hidden="true">
          {pose && <PoseSvg pose={pose} label="" />}
        </span>
        <span className="choice-text">
          <span className="choice-name">{ex.name}</span>
          <span className="choice-sub">{ex.equipment.slice(0, 2).join(', ')}</span>
          <span className="choice-sub">{effortLabel(id)}</span>
        </span>
        {chosen && <span className="choice-rank">{rank === 0 ? '1st' : '2nd'}</span>}
      </button>
      <Link to={`/exercise/${id}`} className="choice-how">
        How to do it
      </Link>
    </div>
  );
}

function SlotStep({ slot, picks, onChange }: { slot: ProgramSlot; picks: LibraryExerciseId[]; onChange: (next: LibraryExerciseId[]) => void }) {
  const times = slotExposures(slot.id);
  const allowSecond = times > 1 && slot.options.length > 1;
  return (
    <div className="stack" data-testid={`slot-${slot.id}`}>
      <div>
        <div className="eyebrow">{slot.group}</div>
        <h2 style={{ margin: '2px 0 4px' }}>{slot.title}</h2>
        <p className="small muted" style={{ margin: 0 }}>
          {slot.head}. {times === 1 ? 'Once' : times === 2 ? 'Twice' : `${times} times`} a week, {slot.sets} sets.
        </p>
      </div>
      <p className="small" style={{ margin: 0 }}>
        {slot.why}
      </p>
      <p className="small muted" style={{ margin: 0 }}>
        {slot.options.length === 1
          ? 'One exercise does this job clearly best, so it is set for you.'
          : allowSecond
            ? 'All options work about equally well. Tap your favourite. Tap a second one to switch between them on the two days, or keep one for both.'
            : 'All options work about equally well. Tap your favourite.'}
      </p>
      <div className="choices">
        {slot.options.map((id) => (
          <OptionCard key={id} id={id} rank={picks.indexOf(id)} onTap={() => slot.options.length > 1 && onChange(togglePick(picks, id, allowSecond))} />
        ))}
      </div>
    </div>
  );
}

const LEVEL_CHECKS = [
  'At least four weeks at the starting level',
  'No knee, heel, shin, or back pain in the last two weeks',
  'Landings rated good or OK on almost every set',
  'School jumping is known and not heavy this month',
  'Sleep mostly 8 hours or more',
] as const;

/** The jump level is a decision after a review, never an automatic step. */
function JumpLevelCard() {
  const level = useLiveQuery(() => jumpLevel(), []) ?? 'intro';
  const [ticks, setTicks] = useState<string[]>([]);
  const all = ticks.length === LEVEL_CHECKS.length;
  return (
    <Section title="Home jump level">
      <div className="panel stack" data-testid="jump-level">
        <p>
          Now: <b>{JUMP_LEVEL_LABEL[level]}</b>.
        </p>
        {level === 'intro' ? (
          <>
            <p className="small muted">The next level adds sets, not harder jumps. It is worth it only when all of these are true. A coach's opinion helps.</p>
            {LEVEL_CHECKS.map((c) => (
              <label key={c} className="row" style={{ gap: 8, alignItems: 'flex-start' }}>
                <input type="checkbox" className="check" checked={ticks.includes(c)} onChange={(e) => setTicks(e.target.checked ? [...ticks, c] : ticks.filter((x) => x !== c))} />
                <span className="small">{c}</span>
              </label>
            ))}
            <button type="button" className="btn btn-outline" disabled={!all} data-testid="jump-level-up" onClick={() => void proposePlan('jump-level', { level: 'build' }).then(() => navigate('/plan'))}>
              See the next level
            </button>
          </>
        ) : (
          <button type="button" className="btn btn-outline" onClick={() => void proposePlan('jump-level', { level: 'intro' }).then(() => navigate('/plan'))}>
            Go back to the starting level
          </button>
        )}
      </div>
    </Section>
  );
}

function Summary({ picks, onEdit }: { picks: ProgramPicks; onEdit: (step: number) => void }) {
  const chosen = normalizePicks(picks);
  const plan = usePlan();
  const homeDays = (plan?.days ?? []).filter((d) => d.items.some((i) => i.session === 'home'));
  return (
    <div className="stack" data-testid="program-summary">
      <p className="small muted" data-testid="program-week">
        Gym days are for strength. Jumps, landings, footwork, and volleyball skills are at home, fitted to the space you described in More, Your profile.
      </p>
      {PROGRAM_DAYS.map((d) => (
        <Section key={d.key} title={`${WEEKDAY_NAMES[d.weekday]}, gym: ${d.title}`}>
          <div className="group">
            {d.main.map((e, i) => {
              if ('fixed' in e) return <Item key={i} title={exercise(e.fixed.exerciseId)?.name ?? e.fixed.exerciseId} sub="Always in the plan" />;
              const slot = SLOT_BY_ID[e.slot];
              const id = chosen[e.slot][e.choice] ?? chosen[e.slot][0]!;
              const sets = e.sets ?? slot.sets;
              return <Item key={i} title={exercise(id)?.name ?? id} sub={`${slot.title}. ${sets} sets. ${effortLabel(id)}.`} onClick={() => onEdit(ACTIVE_SLOTS.indexOf(slot))} />;
            })}
          </div>
        </Section>
      ))}
      {homeDays.map((d) => {
        const items = d.items.filter((i) => i.session === 'home');
        const n = contacts(items);
        return (
          <Section key={`home-${d.key}`} title={`${WEEKDAY_NAMES[d.weekday]}, home`}>
            <div className="group">
              <Item title={items.map((i) => exercise(i.exerciseId)?.name ?? i.exerciseId).join(', ')} sub={n > 0 ? `About ${n} landings. In your current plan.` : 'No jumps. In your current plan.'} to="/more/athlete" />
            </div>
          </Section>
        );
      })}
      <JumpLevelCard />
      <p className="small faint">{WRIST_TEXT.moderate}</p>
    </div>
  );
}

export function ProgramScreen({ step: stepParam }: { step: string | null }) {
  const toast = useToast();
  const [picks, setPicks] = useState<ProgramPicks | null>(null);
  const [busy, setBusy] = useState(false);
  const total = ACTIVE_SLOTS.length;
  const step = stepParam === null ? -1 : Math.max(-1, Math.min(total, Number(stepParam) || 0));

  useEffect(() => {
    void draftPicks().then((p) => setPicks(normalizePicks(p)));
  }, []);

  if (!picks) return null;
  const go = (n: number) => navigate(n < 0 ? '/program' : `/program?step=${n}`, { replace: true });
  const update = (next: ProgramPicks) => {
    setPicks(next);
    void saveDraftPicks(next);
  };

  return (
    <div data-testid="program">
      <PageHead title="Choose your exercises" eyebrow={step >= 0 && step < total ? `${step + 1} of ${total}` : 'Your program'} backTo="/train" />
      {step >= 0 && step < total && (
        <div className="progress-track" aria-hidden="true">
          <span style={{ width: `${((step + 1) / total) * 100}%` }} />
        </div>
      )}

      {step < 0 && (
        <div className="stack">
          <Note tone="accent" title="How your program works">
            <ul className="bullets small" style={{ marginTop: 4 }}>
              <li>Four gym days, upper and lower body in turn, so every muscle is trained twice a week with two or three work sets per exercise.</li>
              <li>For each muscle you choose from exercises that build it about equally, so pick what you enjoy and what your gym has.</li>
              <li>Machines, cables, the Smith machine, and dumbbells only. No free barbell, because you train alone.</li>
              <li>Work sets stop about two reps short of failure. That builds about as much muscle as going to failure, with less fatigue.</li>
              <li>Jumps and volleyball footwork are at home, on Monday and Thursday before the gym, and a light skill session on Friday.</li>
              <li>A new exercise stays three reps short for its first two sessions while you learn it.</li>
            </ul>
          </Note>
          <p className="small muted">
            {total} short questions, with the answers from your questionnaire already filled in. You see every change before it is saved, and the plan is saved as a new version, so your history is kept.
          </p>
          <div className="row wrap">
            <button type="button" className="btn btn-primary" onClick={() => go(0)} data-testid="program-start">
              Start
            </button>
            <button type="button" className="btn btn-outline" onClick={() => go(total)} data-testid="program-review">
              See the whole week
            </button>
          </div>
        </div>
      )}

      {step >= 0 && step < total && (
        <SlotStep slot={ACTIVE_SLOTS[step]!} picks={picks[ACTIVE_SLOTS[step]!.id] ?? []} onChange={(next) => update({ ...picks, [ACTIVE_SLOTS[step]!.id]: next })} />
      )}

      {step === total && <Summary picks={picks} onEdit={go} />}

      <div className="action-row" style={{ marginTop: 16 }}>
        {step >= 0 && (
          <button type="button" className="btn btn-outline" onClick={() => go(step - 1)} disabled={busy}>
            Back
          </button>
        )}
        {step >= 0 && step < total && (
          <button type="button" className="btn btn-primary" onClick={() => go(step + 1)} disabled={(picks[ACTIVE_SLOTS[step]!.id] ?? []).length === 0} data-testid="program-next">
            {step === total - 1 ? 'See the week' : 'Next'}
          </button>
        )}
        {step === total && (
          <button
            type="button"
            className="btn btn-primary"
            disabled={busy}
            data-testid="program-save"
            onClick={async () => {
              setBusy(true);
              try {
                await proposePlan('choices', { picks });
                navigate('/plan');
              } catch {
                setBusy(false);
                toast('Could not save the program. Try again.');
              }
            }}
          >
            Review the changes
          </button>
        )}
      </div>
    </div>
  );
}
