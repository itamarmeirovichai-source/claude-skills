import { useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { activePlan } from '../db/repo';
import { Note, useToast } from '../ui/components';
import { applyPlanUpdates, dismissPlanUpdates, pendingUpdates } from '../services/planUpdate';

/**
 * Offers plan changes that shipped after install. On Today it can be put off with "Not now".
 * On Train it stays until the change is added, so a dismissed update can still be found.
 */
export function PlanUpdateCard({ canDismiss = true }: { canDismiss?: boolean }) {
  const toast = useToast();
  const [busy, setBusy] = useState(false);
  const offer = useLiveQuery(async () => pendingUpdates(await activePlan(), { includeDismissed: !canDismiss }), [canDismiss]);
  if (!offer) return null;
  const both = offer.morning > 0 && offer.gymDays.length > 0;
  const title = both ? 'New: morning volleyball and two new gym days' : offer.morning ? 'New: morning volleyball at 05:30' : 'New: Tuesday and Friday are gym days';
  return (
    <div style={{ marginBottom: 12 }} data-testid="plan-update">
      <Note tone="accent" title={title}>
        {offer.morning > 0 && (
          <p style={{ margin: '0 0 6px' }}>
            {offer.morning} home sessions a week, Sunday to Friday, with no ball: easy rope as the warm up, footwork, light dumbbell shoulder care, and trunk control. Reminders move to 05:15 for the check in and 20:45 to wind down, so sleep still fits.
          </p>
        )}
        {offer.gymDays.length > 0 && (
          <p style={{ margin: '0 0 6px' }} data-testid="plan-update-gym">
            Your volleyball is now in the mornings, so {offer.gymDays.length === 2 ? 'Tuesday and Friday become' : offer.gymDays[0] === 2 ? 'Tuesday becomes' : 'Friday becomes'} muscle building days in the gym. Tuesday, Upper C: upper chest, mid back, side and rear shoulders, biceps, and triceps. Friday, Lower C: leg press, back extension, hamstrings, inner and outer thighs, and calves, with the swim after.
          </p>
        )}
        <p className="small" style={{ margin: 0 }}>
          Your history is kept. Nothing you added yourself is removed.
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
                await applyPlanUpdates(await activePlan(), offer);
                toast('Your plan is up to date');
              } catch {
                setBusy(false);
                toast('Could not update the plan. Try again.');
              }
            }}
          >
            Add to my plan
          </button>
          {canDismiss && (
            <button type="button" className="btn btn-sm btn-ghost" disabled={busy} onClick={() => void dismissPlanUpdates(offer)}>
              Not now
            </button>
          )}
        </div>
      </Note>
    </div>
  );
}
