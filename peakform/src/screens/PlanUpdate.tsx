import { useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { activePlan } from '../db/repo';
import { Note, useToast } from '../ui/components';
import { applyMorningUpdate, dismissMorningUpdate, missingMorningItems, morningUpdateState } from '../services/planUpdate';

/** Offers plan additions that shipped after install. Shown once, until added or dismissed. */
export function PlanUpdateCard() {
  const toast = useToast();
  const [busy, setBusy] = useState(false);
  const offer = useLiveQuery(async () => {
    if (await morningUpdateState()) return null;
    const missing = missingMorningItems(await activePlan());
    return missing.size ? missing.size : null;
  }, []);
  if (!offer) return null;
  return (
    <div style={{ marginBottom: 12 }} data-testid="plan-update">
      <Note tone="accent" title="New: morning volleyball at 05:30">
        {offer} home sessions a week, Sunday to Friday, with no ball: easy rope as the warm up, footwork, light dumbbell shoulder care, and trunk control. The main sessions stay as they are, and your history is kept. Reminders move to 05:15 for the check in and 20:45 to wind down, so sleep still fits.
        <div className="row wrap" style={{ marginTop: 8 }}>
          <button
            type="button"
            className="btn btn-sm btn-primary"
            disabled={busy}
            data-testid="plan-update-apply"
            onClick={async () => {
              setBusy(true);
              await applyMorningUpdate(await activePlan());
              toast('Morning sessions added to your plan');
            }}
          >
            Add to my plan
          </button>
          <button type="button" className="btn btn-sm btn-ghost" disabled={busy} onClick={() => void dismissMorningUpdate()}>
            Not now
          </button>
        </div>
      </Note>
    </div>
  );
}
