import { useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { dunkSummary, RIM_CM } from '../domain/dunk';
import { formatDateKey } from '../domain/dates';
import { nextJumpTest } from '../content/phases';
import { getDunkProfile, saveDunkProfile, touchHistory } from '../services/dunk';
import { Item, Metric, Section, Stepper } from '../ui/components';
import { LineChart } from '../ui/Chart';
import { useToday } from '../ui/hooks';

/** Progress toward the dunk: best touch height from the approach jumps, the gap, and milestones. */
export function DunkGoalSection() {
  const today = useToday();
  // Both reads start together so the live query tracks both. A read after an await is not always tracked.
  const data = useLiveQuery(() => Promise.all([getDunkProfile(), touchHistory()]), []);
  // The checkbox answers at once; the saved value catches up through the live query.
  const [palm, setPalm] = useState<boolean | null>(null);
  if (!data) return null;
  const [saved, touches] = data;
  const profile = { ...saved, canPalm: palm ?? saved.canPalm };
  const sum = dunkSummary(touches, profile);
  const next = nextJumpTest(today);
  return (
    <Section title="Dunk goal">
      <div data-testid="dunk-goal" className="stack">
        <div className="metric-row">
          <Metric label="Best touch" value={sum.best ? `${sum.best.cm} cm` : 'None yet'} sub={sum.best ? formatDateKey(sum.best.date) : 'Log Reach on approach jumps'} testId="dunk-best" />
          <Metric label="Still to go" value={sum.gap === null ? 'Needs a touch' : sum.gap === 0 ? 'Reached' : `${sum.gap} cm`} sub={`Dunk target about ${sum.target} cm`} testId="dunk-gap" />
        </div>
        {touches.length >= 2 && (
          <div className="panel">
            <LineChart points={touches.map((t) => ({ x: t.date, y: t.cm }))} line={touches.map((t) => ({ x: t.date, y: t.cm }))} unit="cm" label="Best touch height" />
          </div>
        )}
        <div className="group">
          {sum.milestones.map((m) => (
            <Item key={m.key} title={`${m.reached ? 'Done: ' : ''}${m.label}`} sub={`About ${m.cm} cm${m.key === 'rim' ? '' : `, ${m.cm - RIM_CM} cm above the rim`}`} testId={`milestone-${m.key}`} />
          ))}
        </div>
        <div className="set-inputs">
          <Stepper label="Standing reach" unit="cm" value={profile.standingReachCm} onChange={(v) => void saveDunkProfile({ ...profile, standingReachCm: v })} min={150} max={300} testId="input-standing-reach" placeholder="cm" />
        </div>
        <div className="group">
          <label className="switch-row">
            <span className="grow">I can hold a basketball in one hand</span>
            <input type="checkbox" className="check" checked={profile.canPalm} onChange={(e) => {
                setPalm(e.target.checked);
                void saveDunkProfile({ ...profile, canPalm: e.target.checked });
              }} data-testid="input-palm" />
          </label>
        </div>
        <p className="small muted" data-testid="dunk-vertical">
          {sum.approachVertical !== null
            ? `Your approach jump is about ${sum.approachVertical} cm: best touch minus standing reach.`
            : 'Add your standing reach to see how high you jump: stand side on to a wall, feet flat, and mark the highest point of one hand.'}
        </p>
        <p className="small muted" data-testid="dunk-next-test">
          Next jump test: {formatDateKey(next, { weekday: 'long', day: 'numeric', month: 'long' })}. After the warm up, do 3 to 5 approach touches with each takeoff and log the best in Reach. Re-measure your standing reach too, because you are still growing.
        </p>
        <p className="small muted">The heights for grabbing the rim and dunking are rough coaching figures, not research. Your own tests decide.</p>
      </div>
    </Section>
  );
}
