import { useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { activePlan } from '../db/repo';
import { Note, PageHead, Section, useToast } from '../ui/components';
import { navigate } from '../ui/router';
import { exerciseName } from '../content/library';
import { SESSION_LABELS } from '../content/plan';
import { activateProposal, currentProposal, discardProposal, dismissPlanUpdates, pendingUpdates, proposalDiff } from '../services/planUpdate';

/**
 * Offers the 3.0 week to an app that still runs an older plan. On Today it can be put off with
 * "Not now". On Train it stays until it is added, so it can always be found.
 */
export function PlanUpdateCard({ canDismiss = true }: { canDismiss?: boolean }) {
  const offer = useLiveQuery(() => pendingUpdates({ includeDismissed: !canDismiss }), [canDismiss]);
  const waiting = useLiveQuery(() => currentProposal(), []);
  if (waiting) {
    return (
      <div style={{ marginBottom: 12 }} data-testid="proposal-waiting">
        <Note tone="accent" title="A plan change is waiting">
          <p style={{ margin: '0 0 6px' }}>{waiting.title}. Look at what changes before you activate it.</p>
          <button type="button" className="btn btn-sm btn-primary" onClick={() => navigate('/plan')} data-testid="proposal-open">
            See the changes
          </button>
        </Note>
      </div>
    );
  }
  if (!offer) return null;
  return (
    <div style={{ marginBottom: 12 }} data-testid="plan-update">
      <Note tone="accent" title="New: a calmer week with more recovery">
        <p style={{ margin: '0 0 6px' }}>
          Four gym days for strength, jumps and volleyball footwork at home on Monday and Thursday, a light skill session on Friday, and two days without structured training. No early morning sessions, so there is time to sleep 8 to 10 hours.
        </p>
        <p className="small" style={{ margin: '0 0 6px' }}>
          A few quick questions about your wrist and your space at home come first, so only drills that fit are planned. You see every change before anything is saved, and your history is kept.
        </p>
        <div className="row wrap" style={{ marginTop: 8 }}>
          <button type="button" className="btn btn-sm btn-primary" data-testid="plan-update-start" onClick={() => navigate('/more/athlete?next=v3')}>
            Answer and see the week
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

/** The change summary and the day by day difference, shown before a new plan is activated. */
export function PlanPreviewScreen() {
  const toast = useToast();
  const [busy, setBusy] = useState(false);
  const data = useLiveQuery(() => Promise.all([currentProposal(), activePlan()]), []);
  if (!data) return null;
  const [proposal, active] = data;
  if (!proposal) {
    return (
      <div data-testid="plan-preview">
        <PageHead title="No plan change waiting" backTo="/train" />
        <p className="muted">There is nothing to activate. Plan changes appear here after you answer the questions in More, Your profile, or change your exercise choices.</p>
      </div>
    );
  }
  const diff = proposalDiff(active, proposal);
  const activate = async () => {
    setBusy(true);
    try {
      await activateProposal();
      toast('The new plan is active. Your history is kept.');
      navigate('/train');
    } catch {
      setBusy(false);
      toast('Could not save the plan. Try again.');
    }
  };
  return (
    <div data-testid="plan-preview">
      <PageHead title={proposal.title} eyebrow="Plan change, not active yet" backTo="/train" />
      <p className="muted">{proposal.reason}</p>
      {proposal.summary.length > 0 && (
        <Section title="Summary">
          <div className="panel">
            <ul className="bullets" data-testid="plan-summary">
              {proposal.summary.map((x) => (
                <li key={x}>{x}</li>
              ))}
            </ul>
          </div>
        </Section>
      )}
      {proposal.settingsChanges.length > 0 && (
        <Section title="Schedule changes">
          <div className="panel">
            <ul className="bullets small">
              {proposal.settingsChanges.map((x) => (
                <li key={x}>{x}</li>
              ))}
            </ul>
            <p className="small muted" style={{ marginTop: 6 }}>Only times still at their old defaults change. Times you set yourself stay.</p>
          </div>
        </Section>
      )}
      <Section title="What changes, day by day">
        {diff.length === 0 ? (
          <p className="muted">The sessions are the same as now.</p>
        ) : (
          <div className="stack" data-testid="plan-diff">
            {diff.map((d) => (
              <div className="panel" key={d.weekday}>
                <h3>
                  {d.dayName}: {d.titleBefore === d.titleAfter ? d.titleAfter : `${d.titleBefore} → ${d.titleAfter}`}
                </h3>
                <ul className="diff-list small">
                  {d.changes.map((c, i) => (
                    <li key={`${c.exerciseId}-${i}`} className={`diff-${c.kind}`}>
                      <span className="diff-mark" aria-hidden="true">
                        {c.kind === 'added' ? '+' : c.kind === 'removed' ? '−' : '~'}
                      </span>
                      <span className="sr-only">{c.kind === 'added' ? 'Added' : c.kind === 'removed' ? 'Removed' : 'Changed'}: </span>
                      <b>{exerciseName(c.exerciseId)}</b> <span className="muted">({SESSION_LABELS[c.session]})</span>
                      {c.kind === 'changed' ? `: ${c.before} → ${c.after}` : `: ${c.after ?? c.before}`}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        )}
      </Section>
      <Note>Finished sessions keep the prescription they were done against. The old plan stays in the history as an earlier version.</Note>
      <div className="grid-2" style={{ marginTop: 12 }}>
        <button type="button" className="btn btn-primary btn-large" disabled={busy} onClick={() => void activate()} data-testid="plan-activate">
          Activate this plan
        </button>
        <button
          type="button"
          className="btn btn-outline btn-large"
          disabled={busy}
          onClick={async () => {
            await discardProposal();
            navigate('/train');
          }}
          data-testid="plan-discard"
        >
          Not now
        </button>
      </div>
    </div>
  );
}
