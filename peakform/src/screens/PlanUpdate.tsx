import { useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { activePlan } from '../db/repo';
import { Note, useToast } from '../ui/components';
import { navigate } from '../ui/router';
import { PROGRAM_SLOTS, defaultPicks } from '../content/program';
import { applyProgram, dismissPhaseNotice, dismissPlanUpdates, pendingUpdates, phaseNotice, savedPicks } from '../services/planUpdate';

/**
 * Offers the program built from the athlete's choices, or the jump program for a plan saved
 * before it existed. On Today it can be put off with "Not now". On Train it stays until it is
 * added, so it can always be found.
 */
export function PlanUpdateCard({ canDismiss = true }: { canDismiss?: boolean }) {
  const toast = useToast();
  const [busy, setBusy] = useState(false);
  const offer = useLiveQuery(() => pendingUpdates({ includeDismissed: !canDismiss }), [canDismiss]);
  if (!offer) return null;
  const add = async () => {
    setBusy(true);
    try {
      await applyProgram(await activePlan(), (await savedPicks()) ?? defaultPicks());
      toast(offer.dunk ? 'The jump program is in your plan' : 'Your program is saved');
    } catch {
      setBusy(false);
      toast('Could not save the program. Try again.');
    }
  };
  const buttons = (
    <div className="row wrap" style={{ marginTop: 8 }}>
      <button type="button" className="btn btn-sm btn-primary" disabled={busy} data-testid="plan-update-apply" onClick={() => void add()}>
        Add to my plan
      </button>
      <button type="button" className="btn btn-sm btn-outline" disabled={busy} data-testid="plan-update-review" onClick={() => navigate(`/program?step=${PROGRAM_SLOTS.length}`)}>
        See the week first
      </button>
      {canDismiss && (
        <button type="button" className="btn btn-sm btn-ghost" disabled={busy} onClick={() => void dismissPlanUpdates(offer)}>
          Not now
        </button>
      )}
    </div>
  );
  return (
    <div style={{ marginBottom: 12 }} data-testid="plan-update">
      {offer.dunk ? (
        <Note tone="accent" title="New: the jump program for your dunk goal">
          <p style={{ margin: '0 0 6px' }}>
            Monday and Friday start with jump drills: landings, box jumps, hurdle hops, depth jumps later, and the dunk approach with your touch height logged. Training blocks change every few weeks until the end of January, with a jump test at the end of each one.
          </p>
          <p style={{ margin: '0 0 6px' }}>
            Your legs train heavy but mostly stop two reps short of failure, so the jumps are done on fresh legs. Wednesday is the lighter leg day. The upper body stays as it is, and your exercise choices are kept.
          </p>
          <p className="small" style={{ margin: 0 }}>
            Your history is kept, and nothing you added yourself is removed.
          </p>
          {buttons}
        </Note>
      ) : (
        <Note tone="accent" title="Your exercise choices are ready">
          <p style={{ margin: '0 0 6px' }}>
            The exercises you picked in the questionnaire, one for each muscle head, with three work sets each across the six gym days, and jump drills on Monday and Friday. Small upper body machine and cable exercises go to failure, and a new exercise stays two reps short for its first two sessions.
          </p>
          <p className="small" style={{ margin: 0 }}>
            Your history is kept, and nothing you added yourself is removed. You can change any choice later from Train.
          </p>
          {buttons}
        </Note>
      )}
    </div>
  );
}

/** Shown once on Today when a new training block has started and the plan was rebuilt for it. */
export function PhaseNoticeCard() {
  const phase = useLiveQuery(() => phaseNotice(), []);
  if (!phase) return null;
  return (
    <div style={{ marginBottom: 12 }} data-testid="phase-notice">
      <Note tone="accent" title={`New training block: ${phase.name}`}>
        <p style={{ margin: '0 0 6px' }}>{phase.summary}</p>
        <p className="small" style={{ margin: 0 }}>
          Your plan was updated for it as a new version. Your history and exercise choices are kept.
        </p>
        <div className="row wrap" style={{ marginTop: 8 }}>
          <button type="button" className="btn btn-sm btn-primary" onClick={() => void dismissPhaseNotice()}>
            Got it
          </button>
          <button type="button" className="btn btn-sm btn-outline" onClick={() => navigate('/train')}>
            See this week
          </button>
        </div>
      </Note>
    </div>
  );
}
