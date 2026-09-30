import { useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { activePlan } from '../db/repo';
import { Note, useToast } from '../ui/components';
import { navigate } from '../ui/router';
import { PROGRAM_SLOTS, defaultPicks } from '../content/program';
import { applyProgram, dismissPlanUpdates, pendingUpdates } from '../services/planUpdate';

/**
 * Offers the program built from the athlete's questionnaire answers. On Today it can be put off
 * with "Not now". On Train it stays until the program is saved, so it can always be found.
 */
export function PlanUpdateCard({ canDismiss = true }: { canDismiss?: boolean }) {
  const toast = useToast();
  const [busy, setBusy] = useState(false);
  const offer = useLiveQuery(() => pendingUpdates({ includeDismissed: !canDismiss }), [canDismiss]);
  if (!offer) return null;
  return (
    <div style={{ marginBottom: 12 }} data-testid="plan-update">
      <Note tone="accent" title="Your exercise choices are ready">
        <p style={{ margin: '0 0 6px' }}>
          The exercises you picked in the questionnaire, one for each muscle head, with three work sets each across the six gym days. Small machine and cable exercises go to failure, and a new exercise stays two reps short for its first two sessions.
        </p>
        <p className="small" style={{ margin: 0 }}>
          Your history is kept, and nothing you added yourself is removed. You can change any choice later from Train.
        </p>
        <div className="row wrap" style={{ marginTop: 8 }}>
          <button
            type="button"
            className="btn btn-sm btn-primary"
            disabled={busy}
            data-testid="plan-update-apply"
            onClick={async () => {
              setBusy(true);
              try {
                await applyProgram(await activePlan(), defaultPicks());
                toast('Your program is saved');
              } catch {
                setBusy(false);
                toast('Could not save the program. Try again.');
              }
            }}
          >
            Add to my plan
          </button>
          <button type="button" className="btn btn-sm btn-outline" disabled={busy} data-testid="plan-update-review" onClick={() => navigate(`/program?step=${PROGRAM_SLOTS.length}`)}>
            See the week first
          </button>
          {canDismiss && (
            <button type="button" className="btn btn-sm btn-ghost" disabled={busy} onClick={() => void dismissPlanUpdates()}>
              Not now
            </button>
          )}
        </div>
      </Note>
    </div>
  );
}
