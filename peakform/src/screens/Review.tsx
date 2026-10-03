import { useEffect, useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../db/db';
import { updateSettings } from '../db/repo';
import { useSettings } from '../ui/state';
import { useToday } from '../ui/hooks';
import { Item, Note, PageHead, Section, Toggle } from '../ui/components';
import { Link } from '../ui/router';
import { addDays, formatDateKey, reviewWeekStart, weekdayOf } from '../domain/dates';
import { prepareCoachReport, runWeeklyReview } from '../services/exporter';
import type { ReviewItem, WeeklyReview } from '../domain/review';
import { ExportAction } from '../ui/ExportAction';

function defaultWeek(today: string): string {
  // Sunday evening reviews the week that ends today. Other days review the last full week.
  return weekdayOf(today) === 0 ? reviewWeekStart(today) : addDays(reviewWeekStart(today), -7);
}

const SECTION_TONE: Record<string, string> = { keep: 'tag-accent', ready: 'tag-accent', improve: 'tag-warn', safety: 'tag-danger' };

function Items({ items, empty, tone }: { items: ReviewItem[]; empty: string; tone: string }) {
  if (!items.length) return <p className="small muted" style={{ padding: '4px 4px' }}>{empty}</p>;
  return (
    <div className="group">
      {items.map((i) => (
        <div className="item" key={i.id} style={{ alignItems: 'flex-start' }}>
          <span className="item-main">
            <span className="item-title" style={{ display: 'block', fontWeight: 520 }}>{i.text}</span>
            <details className="disclosure">
              <summary className="small">
                <span>
                  Evidence <span className={`tag ${SECTION_TONE[tone]}`}>{i.confidence} confidence</span>
                </span>
              </summary>
              <ul className="bullets small muted">
                {i.evidence.map((e) => (
                  <li key={e}>{e}</li>
                ))}
              </ul>
            </details>
          </span>
        </div>
      ))}
    </div>
  );
}

export function ReviewScreen({ weekStart }: { weekStart: string | null }) {
  const today = useToday();
  const settings = useSettings();
  // Reviews start with the week the plan started. Earlier weeks have nothing to review.
  const firstWeek = settings.planStartDate ? reviewWeekStart(settings.planStartDate) : null;
  const [week, setWeek] = useState(() => {
    const w = weekStart ?? defaultWeek(today);
    return firstWeek && w < firstWeek ? firstWeek : w;
  });
  const beforeStart = firstWeek !== null && week < firstWeek;
  const [review, setReview] = useState<WeeklyReview | null>(null);
  const stored = useLiveQuery(() => db.weeklyReviews.where('weekStart').equals(week).first(), [week]);
  useEffect(() => {
    let live = true;
    void runWeeklyReview(week).then((r) => live && setReview(r));
    return () => {
      live = false;
    };
  }, [week]);
  void stored;
  return (
    <div data-testid="review">
      <PageHead
        title="Weekly review"
        eyebrow={`${formatDateKey(week, { day: 'numeric', month: 'short' })} to ${formatDateKey(addDays(week, 6), { day: 'numeric', month: 'short' })}`}
        backTo="/progress"
        end={
          <div className="row">
            <button type="button" className="btn btn-sm btn-outline" onClick={() => setWeek(addDays(week, -7))} disabled={firstWeek !== null && addDays(week, -7) < firstWeek} aria-label="Previous week">
              ‹
            </button>
            <button type="button" className="btn btn-sm btn-outline" onClick={() => setWeek(addDays(week, 7))} disabled={addDays(week, 7) > today} aria-label="Next week">
              ›
            </button>
          </div>
        }
      />
      {beforeStart ? (
        <Note>This week is before your plan started on {formatDateKey(settings.planStartDate!)}, so there is nothing to review.</Note>
      ) : !review ? (
        <p className="muted">Reviewing the week…</p>
      ) : (
        <>
          <p className="small muted">Worked out on this phone from your logs. Each point shows its evidence and how confident it is. If data is missing, it says so.</p>
          <Section title="Next week">
            <div className="panel">
              <ol className="steps" data-testid="priorities">
                {review.priorities.map((p) => (
                  <li key={p}>{p}</li>
                ))}
              </ol>
            </div>
          </Section>
          <Section title="Keep doing">
            <div data-testid="review-keep">
              <Items items={review.keepDoing} tone="keep" empty="Not enough logged this week to say. That is fine, next week will be clearer." />
            </div>
          </Section>
          <Section title="Ready to progress">
            <div data-testid="review-ready">
              <Items items={review.readyToProgress} tone="ready" empty="Nothing is ready to progress yet. Progress comes after every work set reaches the top of its range with good form." />
            </div>
          </Section>
          <Section title="Improve next week">
            <div data-testid="review-improve">
              <Items items={review.improve} tone="improve" empty="Nothing stands out." />
            </div>
          </Section>
          <Section title="Safety flags">
            <div data-testid="review-safety">
              {review.safety.length > 0 && (
                <div style={{ marginBottom: 8 }}>
                  <Note tone="danger">Tell a parent about these. Pain tracking and these checks are not a diagnosis.</Note>
                </div>
              )}
              <Items items={review.safety} tone="safety" empty="No safety flags this week." />
            </div>
          </Section>
          <Section title="Compared with the week before">
            <div className="panel" style={{ padding: 0, overflowX: 'auto' }}>
              <table className="prev-table" data-testid="comparison">
                <thead>
                  <tr>
                    <th>Measure</th>
                    <th>Before</th>
                    <th>This week</th>
                  </tr>
                </thead>
                <tbody>
                  {review.comparison.map((c) => (
                    <tr key={c.label}>
                      <td>
                        {c.label}
                        {c.note && <div className="small faint">{c.note}</div>}
                      </td>
                      <td>{c.previous}</td>
                      <td>{c.current}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Section>
          <Section title="Share with a coach or assistant">
            <div className="panel stack">
              <p className="small">
                PeakForm cannot send anything by itself, and no assistant can read this phone. Share the report yourself: a readable Markdown file and a JSON file with the same review. You can send them to Codex, Claude, a coach, or a parent.
              </p>
              <div className="group">
                <Toggle checked={settings.coachShare.includeNotes} onChange={(v) => void updateSettings((s) => ({ ...s, coachShare: { ...s.coachShare, includeNotes: v } }))} label="Include private notes" sub="Off by default" />
                <Toggle checked={settings.coachShare.includePhotos} onChange={(v) => void updateSettings((s) => ({ ...s, coachShare: { ...s.coachShare, includePhotos: v } }))} label="Include food photos" sub="Off by default" />
              </div>
              <ExportAction label="Prepare coach report" primary testId="share-report" prepare={async () => ({ files: await prepareCoachReport(review, settings), title: `${settings.appName} weekly review`, record: { kind: 'coach-report', checksum: '', counts: {}, note: `Coach report ${review.weekStart}` } })} />
              <Item title="Import a reviewed plan or recommendation" sub="Shows every change before anything is applied" to="/more/recommendation" />
            </div>
          </Section>
          <p className="small faint" style={{ marginTop: 12 }}>
            Generated {new Date(review.generatedAt).toLocaleString()}. <Link to="/more/safety">Safety guidance</Link>
          </p>
        </>
      )}
    </div>
  );
}
