import { useLiveQuery } from 'dexie-react-hooks';
import { Note } from '../ui/components';
import { navigate } from '../ui/router';
import { dismissPlanUpdates, pendingUpdates } from '../services/planUpdate';

/**
 * Invites the athlete to build the program from his own exercise choices. On Today it can be put
 * off with "Not now". On Train it stays until the program is saved, so it can always be found.
 */
export function PlanUpdateCard({ canDismiss = true }: { canDismiss?: boolean }) {
  const offer = useLiveQuery(() => pendingUpdates({ includeDismissed: !canDismiss }), [canDismiss]);
  if (!offer) return null;
  return (
    <div style={{ marginBottom: 12 }} data-testid="plan-update">
      <Note tone="accent" title="New: choose your exercises">
        <p style={{ margin: '0 0 6px' }}>
          A new program with one exercise for each muscle head and a stretch on every rep. For each muscle you pick from exercises that build it about equally, with pictures of each. Machines, cables, the Smith machine, and dumbbells only.
        </p>
        <p className="small" style={{ margin: 0 }}>
          About five minutes. Your history is kept, and you can change your choices later.
        </p>
        <div className="row wrap" style={{ marginTop: 8 }}>
          <button type="button" className="btn btn-sm btn-primary" data-testid="plan-update-apply" onClick={() => navigate('/program')}>
            Choose my exercises
          </button>
          {canDismiss && (
            <button type="button" className="btn btn-sm btn-ghost" onClick={() => void dismissPlanUpdates()}>
              Not now
            </button>
          )}
        </div>
      </Note>
    </div>
  );
}
