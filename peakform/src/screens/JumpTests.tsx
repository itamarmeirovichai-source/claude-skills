import { useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { KV, kvGet, kvSet } from '../db/repo';
import { Item, Metric, Note, Section, Sheet, Stepper, useToast } from '../ui/components';
import { useToday } from '../ui/hooks';
import { useSettings } from '../ui/state';
import { uid } from '../lib/id';
import { formatDateKey } from '../domain/dates';
import { heights, jumpTrend, parseTests, type JumpTest } from '../domain/jumpTests';
import { nextMeasurementDate } from '../content/phases';

// Jump measurements on Progress (3.0.0). Replaces the dunk goal: no target height, no deadline,
// and no estimate from touching part of a hoop. Only tests done the same way are compared.

const PROTOCOL = [
  'Warm up the same way each time, then rest two minutes. Test on a home jump day, before any other jumps, not after a hard sport day.',
  'Standing reach: stand side on to a wall in your test shoes, feet flat, and reach as high as you can with one hand. Mark the fingertips with tape or chalk.',
  'Jump and reach: from the same spot, jump with both feet and touch as high as you can. Three attempts with a minute of rest. The best one counts.',
  'Approach jump and reach only outdoors or in a hall where the ceiling cannot be reached, and only with a safe run up.',
  'Use the same wall, shoes, and surface every time. Measure from the floor to each mark with a tape measure.',
];

export function JumpTestsSection() {
  const today = useToday();
  const settings = useSettings();
  const raw = useLiveQuery(() => Promise.all([kvGet<unknown>(KV.jumpTests), kvGet<{ standingReachCm?: number | null }>(KV.dunkProfile)]), []);
  const [open, setOpen] = useState(false);
  if (!raw) return null;
  const tests = parseTests(raw[0]);
  const trend = jumpTrend(tests);
  const last = trend.latest ? heights(trend.latest) : null;
  const next = nextMeasurementDate(settings.planStartDate, today);
  return (
    <Section title="Jump measurements">
      <div className="panel stack" data-testid="jump-tests">
        {trend.latest ? (
          <>
            <div className="metric-row">
              <Metric label="Standing jump" value={last?.standing !== null && last?.standing !== undefined ? `${last.standing} cm` : 'Not measured'} sub={formatDateKey(trend.latest.date, { day: 'numeric', month: 'short' })} testId="jump-standing" />
              <Metric label="Approach jump" value={last?.approach !== null && last?.approach !== undefined ? `${last.approach} cm` : 'Not measured'} sub="Reach minus standing reach" />
            </div>
            {trend.previous ? (
              <p className="small" data-testid="jump-change">
                Since {formatDateKey(trend.previous.date, { day: 'numeric', month: 'short' })}, same method and shoes: standing {fmtChange(trend.standingChange)}, approach {fmtChange(trend.approachChange)}.{' '}
                {trend.withinNoise ? 'That is within the usual day to day difference of about 2 cm, so it is too early to call it a change.' : ''}
              </p>
            ) : (
              <p className="small muted">The next test done the same way will show a comparison.</p>
            )}
          </>
        ) : (
          <p className="muted">No jump test yet. One test every four weeks, done the same way, shows real progress better than daily touches.</p>
        )}
        {next && <p className="small muted">Next test around {formatDateKey(next, { weekday: 'long', day: 'numeric', month: 'short' })}, every four weeks from the plan start.</p>}
        <button type="button" className="btn btn-outline" onClick={() => setOpen(true)} data-testid="jump-test-add">
          Add a jump test
        </button>
        <details className="disclosure">
          <summary className="small">How to measure the same way every time</summary>
          <ol className="steps small">
            {PROTOCOL.map((p) => (
              <li key={p}>{p}</li>
            ))}
          </ol>
        </details>
        {tests.length > 1 && (
          <div className="group">
            {[...tests].reverse().map((t) => {
              const h = heights(t);
              return <Item key={t.id} title={formatDateKey(t.date, { day: 'numeric', month: 'short', year: 'numeric' })} sub={`Standing ${h.standing ?? 'none'} cm, approach ${h.approach ?? 'none'} cm, ${t.method === 'wall-tape' ? 'tape on a wall' : t.method}, ${t.shoes || 'shoes not noted'}`} />;
            })}
          </div>
        )}
      </div>
      <JumpTestSheet open={open} onClose={() => setOpen(false)} tests={tests} reach={tests[tests.length - 1]?.standingReachCm ?? raw[1]?.standingReachCm ?? null} />
    </Section>
  );
}

function fmtChange(n: number | null): string {
  if (n === null) return 'not compared';
  return `${n > 0 ? '+' : ''}${n} cm`;
}

function JumpTestSheet({ open, onClose, tests, reach }: { open: boolean; onClose: () => void; tests: JumpTest[]; reach: number | null }) {
  const toast = useToast();
  const today = useToday();
  const prev = tests[tests.length - 1];
  const [t, setT] = useState<JumpTest>({ id: '', date: today, standingReachCm: reach, standingJumpCm: [], approachJumpCm: [], method: prev?.method ?? 'wall-tape', surface: prev?.surface ?? '', shoes: prev?.shoes ?? '', note: '' });
  const attempt = (k: 'standingJumpCm' | 'approachJumpCm', i: number, v: number | null) => {
    const xs = [...t[k]];
    if (v === null) xs.splice(i, 1);
    else xs[i] = v;
    setT({ ...t, [k]: xs.filter((x) => typeof x === 'number') });
  };
  return (
    <Sheet open={open} onClose={onClose} title="Jump test" testId="jump-test-sheet">
      <div className="stack">
        <Stepper label="Standing reach" unit="cm" value={t.standingReachCm} onChange={(v) => setT({ ...t, standingReachCm: v })} min={100} max={300} testId="jt-reach" />
        {[0, 1, 2].map((i) => (
          <Stepper key={`s${i}`} label={`Standing jump and reach, attempt ${i + 1}`} unit="cm" value={t.standingJumpCm[i] ?? null} onChange={(v) => attempt('standingJumpCm', i, v)} min={100} max={400} testId={`jt-s${i}`} />
        ))}
        {[0, 1, 2].map((i) => (
          <Stepper key={`a${i}`} label={`Approach jump and reach, attempt ${i + 1}, optional`} unit="cm" value={t.approachJumpCm[i] ?? null} onChange={(v) => attempt('approachJumpCm', i, v)} min={100} max={400} />
        ))}
        <label className="field">
          <span className="small muted">Surface</span>
          <input className="input" value={t.surface} maxLength={40} placeholder="For example, grass in the yard" onChange={(e) => setT({ ...t, surface: e.target.value })} />
        </label>
        <label className="field">
          <span className="small muted">Shoes</span>
          <input className="input" value={t.shoes} maxLength={40} placeholder="For example, court shoes" onChange={(e) => setT({ ...t, shoes: e.target.value })} />
        </label>
        <Note>Only tests with the same method, surface, and shoes are compared.</Note>
        <button
          type="button"
          className="btn btn-primary btn-large btn-block"
          disabled={t.standingReachCm === null || (t.standingJumpCm.length === 0 && t.approachJumpCm.length === 0)}
          data-testid="jt-save"
          onClick={async () => {
            await kvSet(KV.jumpTests, [...tests, { ...t, id: uid('jt').slice(0, 40) }]);
            toast('Jump test saved');
            onClose();
          }}
        >
          Save test
        </button>
      </div>
    </Sheet>
  );
}
