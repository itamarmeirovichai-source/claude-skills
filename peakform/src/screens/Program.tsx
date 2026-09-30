import { useEffect, useState } from 'react';
import { exercise } from '../content/library';
import { PROGRAM_DAYS, PROGRAM_SLOTS, SLOT_BY_ID, normalizePicks, slotExposures, togglePick, type ProgramPicks, type ProgramSlot } from '../content/program';
import type { LibraryExerciseId } from '../content/exercises/ids';
import type { FailurePolicy } from '../content/types';
import { WEEKDAY_NAMES } from '../domain/dates';
import { activePlan } from '../db/repo';
import { applyProgram, draftPicks, saveDraftPicks } from '../services/planUpdate';
import { PoseSvg } from '../svg/Figures';
import { Item, Note, PageHead, Section, useToast } from '../ui/components';
import { Link, navigate } from '../ui/router';

// The exercise questionnaire. One step per muscle head. Every option in a step trains that head
// about equally, so the choice is about what the athlete enjoys and what the gym has.

const EFFORT_LABEL: Record<FailurePolicy, string> = {
  all: 'Every set to failure',
  last: 'Last set to failure',
  never: 'Stops one rep short',
};

function effortLabel(id: string): string {
  const ex = exercise(id);
  if (ex?.kind === 'hold') return 'Timed hold';
  return EFFORT_LABEL[ex?.failure ?? 'never'];
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

function Summary({ picks, onEdit }: { picks: ProgramPicks; onEdit: (step: number) => void }) {
  const chosen = normalizePicks(picks);
  return (
    <div className="stack" data-testid="program-summary">
      {PROGRAM_DAYS.map((d) => (
        <Section key={d.key} title={`${WEEKDAY_NAMES[d.weekday]}, ${d.title}`}>
          <div className="group">
            {d.main.map((e, i) => {
              if ('fixed' in e) return <Item key={i} title={exercise(e.fixed.exerciseId)?.name ?? e.fixed.exerciseId} sub="Always in the plan" />;
              const slot = SLOT_BY_ID[e.slot];
              const id = chosen[e.slot][e.choice] ?? chosen[e.slot][0]!;
              return <Item key={i} title={exercise(id)?.name ?? id} sub={`${slot.title}. ${effortLabel(id)}.`} onClick={() => onEdit(PROGRAM_SLOTS.indexOf(slot))} />;
            })}
          </div>
        </Section>
      ))}
    </div>
  );
}

export function ProgramScreen({ step: stepParam }: { step: string | null }) {
  const toast = useToast();
  const [picks, setPicks] = useState<ProgramPicks | null>(null);
  const [busy, setBusy] = useState(false);
  const total = PROGRAM_SLOTS.length;
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
              <li>One exercise for each muscle head, three work sets, with a slow stretch at the bottom of every rep.</li>
              <li>For each muscle you choose from exercises that build it about equally, so pick what you enjoy and what your gym has.</li>
              <li>Machines, cables, the Smith machine, and dumbbells only. No free barbell, because you train alone.</li>
              <li>Small exercises go to failure on every set, big machine exercises on the last set. Dumbbell presses, lunges, and hinges stop one rep short.</li>
              <li>A new exercise stays two reps short for its first two sessions while you learn it.</li>
            </ul>
          </Note>
          <p className="small muted">
            {total} short questions, with the answers from your questionnaire already filled in. Your history is kept, and you can change your choices here at any time. The plan is saved as a new version.
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
        <SlotStep slot={PROGRAM_SLOTS[step]!} picks={picks[PROGRAM_SLOTS[step]!.id] ?? []} onChange={(next) => update({ ...picks, [PROGRAM_SLOTS[step]!.id]: next })} />
      )}

      {step === total && <Summary picks={picks} onEdit={go} />}

      <div className="action-row" style={{ marginTop: 16 }}>
        {step >= 0 && (
          <button type="button" className="btn btn-outline" onClick={() => go(step - 1)} disabled={busy}>
            Back
          </button>
        )}
        {step >= 0 && step < total && (
          <button type="button" className="btn btn-primary" onClick={() => go(step + 1)} disabled={(picks[PROGRAM_SLOTS[step]!.id] ?? []).length === 0} data-testid="program-next">
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
                await applyProgram(await activePlan(), picks);
                toast('Your program is saved');
                navigate('/train');
              } catch {
                setBusy(false);
                toast('Could not save the program. Try again.');
              }
            }}
          >
            Save my program
          </button>
        )}
      </div>
    </div>
  );
}
