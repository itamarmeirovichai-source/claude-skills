import { useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../db/db';
import { currentTarget, lastExposure } from '../db/repo';
import { allExercises, exercise } from '../content/library';
import { mediaFor } from '../content/mediaFor';
import { MUSCLE_GROUP_LABELS, MUSCLE_BY_ID } from '../content/muscles';
import type { FatigueArea, MediaReference } from '../content/types';
import { Item, Note, PageHead, Section, useOnline } from '../ui/components';
import { Link, useRoute } from '../ui/router';
import { IconPlay } from '../ui/icons';
import { BodyMap } from '../svg/BodyMap';
import { Keyframes } from '../svg/Figures';
import { usePlan } from '../ui/hooks';
import { restText, targetText } from './Train';
import { uid } from '../lib/id';
import { summarizeSets } from '../ui/format';

const FATIGUE_LABEL: Record<FatigueArea, string> = {
  shoulder: 'shoulder',
  elbow: 'elbow',
  wrist_grip: 'wrist and grip',
  low_back: 'low back',
  knee: 'knee',
  hip: 'hip',
  hamstring: 'hamstring',
  achilles_calf: 'Achilles and calf',
  shin: 'shin',
  neck: 'neck',
  systemic: 'whole body',
};

const sentence = (t: string) => t.charAt(0).toUpperCase() + t.slice(1);

const KIND_LABEL: Record<string, string> = {
  strength: 'Strength',
  bodyweight: 'Bodyweight',
  hold: 'Hold',
  jump: 'Jump',
  sprint: 'Sprint',
  skill: 'Volleyball skill',
  throw: 'Throw',
  conditioning: 'Conditioning',
  warmup: 'Warm up',
  swim: 'Swim',
};

export function ExerciseScreen({ id }: { id: string }) {
  const ex = exercise(id);
  const { query } = useRoute();
  const plan = usePlan();
  const itemId = query.get('item');
  const item = plan?.days.flatMap((d) => d.items).find((i) => (itemId ? i.id === itemId : i.exerciseId === id));
  const last = useLiveQuery(() => lastExposure(id), [id]);
  const target = useLiveQuery(() => (item ? currentTarget(item.id, id) : Promise.resolve(null)), [item?.id, id]);
  if (!ex) return <PageHead title="Exercise not found" backTo="/library" />;
  const media = mediaFor(id);
  const subs = [ex.easierSubstitution, ex.equipmentSubstitution, ...(ex.otherSubstitutions ?? [])];
  return (
    <div data-testid="exercise-detail">
      <PageHead title={ex.name} eyebrow={KIND_LABEL[ex.kind]} backTo="/train" />
      <p className="muted">{ex.purpose}</p>

      {item && (
        <div className="presc" style={{ marginTop: 10 }}>
          <span>
            <b>{targetText(item)}</b>
          </span>
          {item.rir !== undefined && <span>{item.rir} RIR</span>}
          {item.tempo && <span>tempo {item.tempo.split('').join(' ')}</span>}
          <span>{restText(item.restSec)}</span>
        </div>
      )}

      <Section title="How it looks">
        {(ex.visual.poses?.length ?? 0) > 0 || ex.visual.diagram ? (
          <>
            <Keyframes visual={ex.visual} name={ex.name} />
            <p className="small faint" style={{ marginTop: 6 }}>Original PeakForm illustration. It shows positions, not exact joint angles for your body.</p>
          </>
        ) : (
          <p className="small muted">You added this exercise, so it has no illustration. The muscle map below shows what it trains.</p>
        )}
      </Section>

      <Section title="Last time and next target">
        <div className="group">
          <Item
            title={last ? summarizeSets(last.sets) : 'Not logged yet'}
            sub={last ? `Last performance, ${last.session.date}` : 'Last performance'}
            testId="detail-last"
          />
          <Item title={target ? target.title : 'Follow the plan prescription'} sub={target ? `${target.status === 'accepted' ? 'Confirmed' : 'Suggested'}. ${target.reason}` : last ? 'A suggested next target appears when you finish a session with this exercise.' : 'A suggested next target appears after your first session.'} testId="detail-target" />
          <Item title="Full history" to={`/history/${id}`} />
        </div>
      </Section>

      <Section title="Muscles">
        <BodyMap highlight={{ primary: ex.muscles.primary, secondary: ex.muscles.secondary }} />
        <p className="small" style={{ marginTop: 8 }}>{ex.emphasisNote}</p>
      </Section>

      <Section title="Setup">
        <div className="panel">
          <p className="small muted" style={{ marginBottom: 6 }}>
            <b>Equipment:</b> {ex.equipment.join(', ')}
          </p>
          <ol className="steps">
            {ex.setup.map((s) => (
              <li key={s}>{s}</li>
            ))}
          </ol>
        </div>
      </Section>

      <Section title="Step by step">
        <div className="panel">
          <ol className="steps">
            {ex.steps.map((s) => (
              <li key={s}>{s}</li>
            ))}
          </ol>
        </div>
      </Section>

      <Section title="Breathing, tempo, range">
        <div className="group">
          <Item title="Breathing" sub={ex.breathing} />
          <Item title="Tempo" sub={ex.tempo} />
          <Item title="Range of motion" sub={ex.rangeOfMotion} />
          <Item title="What good form feels like" sub={ex.goodFormFeels} />
        </div>
      </Section>

      <Section title="Common mistakes">
        <div className="panel">
          <ul className="bullets">
            {ex.commonMistakes.map((s) => (
              <li key={s}>{s}</li>
            ))}
          </ul>
        </div>
      </Section>

      <Section title="Stop rules">
        <Note tone="warn">
          <ul className="bullets">
            {ex.stopRules.map((s) => (
              <li key={s}>{s}</li>
            ))}
          </ul>
        </Note>
        {ex.safetyNotes.length > 0 && (
          <div className="panel" style={{ marginTop: 8 }}>
            <ul className="bullets small">
              {ex.safetyNotes.map((s) => (
                <li key={s}>{s}</li>
              ))}
            </ul>
          </div>
        )}
      </Section>

      <Section title="Substitutions">
        <div className="group">
          {subs.map((s, i) => (
            <Item
              key={s.name + i}
              title={`${i === 0 ? 'Easier: ' : i === 1 ? 'Other equipment: ' : ''}${s.name}`}
              sub={s.reason}
              to={s.exerciseId ? `/exercise/${s.exerciseId}` : undefined}
            />
          ))}
        </div>
      </Section>

      <Section title="Movement details">
        <div className="group">
          <Item title="Pattern" end={sentence(ex.movementPattern.replace(/_/g, ' '))} />
          <Item title="Joints" end={ex.joints.join(', ')} />
          <Item title="Sides" end={ex.laterality === 'unilateral' ? 'One side at a time, log both' : ex.laterality === 'alternating' ? 'Alternating' : 'Both together'} />
          <Item title="Also tires" end={ex.fatigueOverlap.length ? sentence(ex.fatigueOverlap.map((f) => FATIGUE_LABEL[f]).join(', ')) : 'Nothing notable'} />
        </div>
      </Section>

      <Section title="Video">
        {media.length ? media.map((m) => <VideoGate key={m.id} m={m} />) : <p className="muted small">No vetted video for this exact exercise. The written steps and the illustration above cover it.</p>}
      </Section>
    </div>
  );
}

/** External video loads only after a tap, from youtube-nocookie. Nothing is downloaded or rehosted. */
function VideoGate({ m }: { m: MediaReference }) {
  const [play, setPlay] = useState(false);
  const online = useOnline();
  const status = useLiveQuery(() => db.mediaStatus.where('mediaId').equals(m.id).first(), [m.id]);
  const confirmed = status?.status === 'user-confirmed';
  const rejected = status?.status === 'user-rejected';
  const setStatus = async (s: 'user-confirmed' | 'user-rejected') => {
    const t = Date.now();
    await db.mediaStatus.put({ id: status?.id ?? uid('media'), createdAt: status?.createdAt ?? t, updatedAt: t, mediaId: m.id, status: s, note: '' });
  };
  return (
    <div className="stack" style={{ marginBottom: 16 }} data-testid="video-gate">
      <div className="video-gate">
        {play && m.videoId && online ? (
          <iframe
            src={`https://www.youtube-nocookie.com/embed/${m.videoId}?rel=0&modestbranding=1&playsinline=1`}
            title={m.title}
            allow="accelerometer; encrypted-media; gyroscope; picture-in-picture"
            referrerPolicy="strict-origin-when-cross-origin"
            sandbox="allow-scripts allow-same-origin allow-presentation allow-popups"
            allowFullScreen
          />
        ) : (
          <>
            <p className="small muted">
              {m.channel}. “{m.title}”
            </p>
            <button type="button" className="btn btn-primary" disabled={!online || !m.videoId} onClick={() => setPlay(true)} data-testid="video-play">
              <IconPlay /> {online ? 'Play video' : 'Needs internet'}
            </button>
            <p className="small faint">Loads from YouTube only after you tap. YouTube may then set cookies.</p>
          </>
        )}
      </div>
      <p className="small muted">
        {confirmed ? 'You confirmed this video matches the exercise.' : rejected ? 'You marked this video as not matching. The written steps above still apply.' : m.reviewerNote}
      </p>
      <div className="row wrap">
        <a className="btn btn-sm btn-outline" href={m.url} target="_blank" rel="noopener noreferrer">
          Open on YouTube
        </a>
        {!confirmed && (
          <button type="button" className="btn btn-sm btn-ghost" onClick={() => void setStatus('user-confirmed')}>
            It matches
          </button>
        )}
        {!rejected && (
          <button type="button" className="btn btn-sm btn-ghost" onClick={() => void setStatus('user-rejected')}>
            Wrong exercise
          </button>
        )}
      </div>
    </div>
  );
}

export function LibraryScreen() {
  const [q, setQ] = useState('');
  const list = allExercises().filter((e) => !q || `${e.name} ${e.muscles.primary.map((m) => MUSCLE_BY_ID[m]?.shortName).join(' ')}`.toLowerCase().includes(q.toLowerCase()));
  const groups = new Map<string, typeof list>();
  for (const e of list) {
    const g = e.kind === 'strength' || e.kind === 'bodyweight' || e.kind === 'hold' ? MUSCLE_GROUP_LABELS[MUSCLE_BY_ID[e.muscles.primary[0]!]?.group ?? 'core'] : 'Volleyball, jumps, and conditioning';
    groups.set(g, [...(groups.get(g) ?? []), e]);
  }
  return (
    <div data-testid="library">
      <PageHead title="Exercise library" backTo="/train" end={<Link to="/more/custom-exercise" className="btn btn-sm btn-outline">New</Link>} />
      <label className="field">
        <span className="sr-only">Search exercises</span>
        <input className="input" type="search" placeholder="Search by name or muscle" value={q} onChange={(e) => setQ(e.target.value)} />
      </label>
      {[...groups.entries()].map(([g, xs]) => (
        <Section key={g} title={g}>
          <div className="group">
            {xs.map((e) => (
              <Item key={e.id} to={`/exercise/${e.id}`} title={e.name} sub={e.muscles.primary.map((m) => MUSCLE_BY_ID[m]?.shortName).join(', ')} />
            ))}
          </div>
        </Section>
      ))}
    </div>
  );
}
