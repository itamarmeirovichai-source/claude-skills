import { useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../db/db';
import { saveCheckIn } from '../db/repo';
import { PAIN_REGIONS, PAIN_REGION_LABELS, RED_FLAGS, RED_FLAG_LABELS, SORENESS_REGIONS, type RedFlag } from '../db/records';
import { Note, PageHead, Section, Seg, Stepper, Toggle, useToast } from '../ui/components';
import { useToday } from '../ui/hooks';
import { navigate } from '../ui/router';
import { reviewWeekStart, sleepMinutes } from '../domain/dates';

const SORE_LABEL: Record<string, string> = { legs: 'Legs', glutes: 'Glutes', back: 'Back', chest: 'Chest', shoulders: 'Shoulders', arms: 'Arms', calves: 'Calves' };
const scale5 = [1, 2, 3, 4, 5].map((v) => ({ value: v, label: String(v) }));

export function CheckInScreen() {
  const today = useToday();
  const toast = useToast();
  const last = useLiveQuery(() => db.checkins.orderBy('at').reverse().filter((c) => c.weightKg !== null).first(), []);
  const lastSleep = useLiveQuery(() => db.sleep.orderBy('date').reverse().first(), []);
  const waistThisWeek = useLiveQuery(() => db.waist.where('date').between(reviewWeekStart(today), today, true, true).count(), [today]);
  const [weight, setWeight] = useState<number | null>(null);
  const [bf, setBf] = useState<number | null>(null);
  const [waist, setWaist] = useState<number | null>(null);
  const [standard, setStandard] = useState(true);
  const [bed, setBed] = useState<string | null>(null);
  const [wake, setWake] = useState<string | null>(null);
  const [sleepQ, setSleepQ] = useState<number | null>(null);
  const [energy, setEnergy] = useState<number | null>(null);
  const [mood, setMood] = useState<number | null>(null);
  const [conc, setConc] = useState<number | null>(null);
  const [sore, setSore] = useState<Record<string, number>>({});
  const [pain, setPain] = useState<Record<string, number>>({});
  const [ill, setIll] = useState(false);
  const [illNote, setIllNote] = useState('');
  const [hydration, setHydration] = useState('');
  const [note, setNote] = useState('');
  const [flags, setFlags] = useState<RedFlag[]>([]);
  const [saved, setSaved] = useState(false);

  const bedT = bed ?? lastSleep?.bedtime ?? '21:15';
  const wakeT = wake ?? lastSleep?.wakeTime ?? '05:10';
  const dur = sleepMinutes(bedT, wakeT);
  const needWaist = waistThisWeek === 0;
  const anyPain4 = Object.values(pain).some((v) => v >= 4);

  const save = async () => {
    await saveCheckIn({
      checkin: {
        date: today,
        at: Date.now(),
        weightKg: weight,
        bodyFatPct: bf,
        standardConditions: standard,
        energy,
        mood,
        concentration: conc,
        hunger: null,
        soreness: sore,
        illness: ill,
        illnessNote: illNote.slice(0, 300),
        hydrationNote: hydration.slice(0, 300),
        redFlags: flags,
        note: note.slice(0, 2000),
      },
      sleep: { date: today, bedtime: bedT, wakeTime: wakeT, durationMin: dur, quality: sleepQ },
      waist: waist !== null ? { date: today, cm: waist, standardConditions: standard } : null,
      pain: Object.entries(pain)
        .filter(([, v]) => v > 0)
        .map(([region, score]) => ({ date: today, at: Date.now(), region, score, source: 'checkin' as const, exerciseId: null, note: '' })),
    });
    if (flags.length || anyPain4) setSaved(true);
    else {
      toast('Check in saved');
      navigate('/today');
    }
  };

  if (saved) {
    return (
      <div>
        <PageHead title="Check in saved" />
        <Note tone="danger" title="Please tell a parent today">
          {flags.length > 0
            ? `You recorded ${flags.map((f) => RED_FLAG_LABELS[f].toLowerCase()).join(', ')}. PeakForm has paused progression advice. Tell a parent and get appropriate medical care. If it is severe or sudden, get help now.`
            : 'You recorded pain of 4 out of 10 or more. Pause exercises that load that area and talk with a parent, coach, or clinician.'}
        </Note>
        <button type="button" className="btn btn-primary btn-block" style={{ marginTop: 16 }} onClick={() => navigate('/today')}>
          Back to Today
        </button>
      </div>
    );
  }

  return (
    <div data-testid="checkin">
      <PageHead title="Morning check in" eyebrow="Under a minute" backTo="/today" />

      <Section title="Body">
        <div className="stack">
          <Stepper label="Morning weight" unit="kg" value={weight} onChange={setWeight} step={0.1} decimals={1} min={20} max={300} base={last?.weightKg ?? null} placeholder="Not weighed" prev={last?.weightKg ? String(last.weightKg) : undefined} testId="checkin-weight" />
          <div className="group">
            <Toggle checked={standard} onChange={setStandard} label="After the toilet, before food or drink" sub="Standard conditions make the trend meaningful." />
          </div>
          <details className="disclosure">
            <summary>Scale body fat, optional</summary>
            <Stepper label="Body fat" unit="%" value={bf} onChange={setBf} step={0.1} decimals={1} min={2} max={70} />
            <p className="hint">A trend signal only. It moves with water and timing.</p>
          </details>
          {needWaist ? (
            <div>
              <Stepper label="Waist, weekly" unit="cm" value={waist} onChange={setWaist} step={0.5} decimals={1} min={30} max={200} testId="checkin-waist" />
              <p className="hint">Once a week. Tape level at the navel, relaxed, after breathing out.</p>
            </div>
          ) : (
            <details className="disclosure">
              <summary>Waist, already measured this week</summary>
              <Stepper label="Waist" unit="cm" value={waist} onChange={setWaist} step={0.5} decimals={1} min={30} max={200} />
            </details>
          )}
        </div>
      </Section>

      <Section title="Sleep">
        <div className="panel stack">
          <div className="grid-2">
            <label className="field">
              <span className="label">Went to sleep</span>
              <input className="input" type="time" value={bedT} onChange={(e) => setBed(e.target.value)} data-testid="checkin-bed" />
            </label>
            <label className="field">
              <span className="label">Woke up</span>
              <input className="input" type="time" value={wakeT} onChange={(e) => setWake(e.target.value)} />
            </label>
          </div>
          <p className="small">
            <b>
              {Math.floor(dur / 60)} h {dur % 60} min
            </b>{' '}
            <span className="muted">{dur >= 480 ? 'inside the 8 to 10 hour target' : 'under the 8 to 10 hour target'}</span>
          </p>
          <div>
            <div className="stepper-label">
              <span>Sleep quality, 1 to 5</span>
            </div>
            <Seg label="Sleep quality" value={sleepQ} onChange={setSleepQ} options={scale5} />
          </div>
        </div>
      </Section>

      <Section title="How you feel, 1 to 5">
        <div className="panel stack">
          {(
            [
              ['Energy', energy, setEnergy],
              ['Mood', mood, setMood],
              ['School concentration', conc, setConc],
            ] as const
          ).map(([label, v, set]) => (
            <div key={label}>
              <div className="stepper-label">
                <span>{label}</span>
              </div>
              <Seg label={label} value={v} onChange={set} options={scale5} />
            </div>
          ))}
        </div>
      </Section>

      <Section title="Soreness">
        <div className="panel stack">
          {SORENESS_REGIONS.map((r) => (
            <div key={r} className="row" style={{ gap: 10 }}>
              <span className="small" style={{ width: 76, flex: '0 0 auto' }}>
                {SORE_LABEL[r]}
              </span>
              <div className="grow">
                <Seg label={`${SORE_LABEL[r]} soreness`} value={sore[r] ?? 0} onChange={(v) => setSore({ ...sore, [r]: v })} options={[{ value: 0, label: 'None' }, { value: 1, label: 'Mild' }, { value: 2, label: 'Some' }, { value: 3, label: 'Very' }]} />
              </div>
            </div>
          ))}
        </div>
      </Section>

      <Section title="Pain, 0 to 10">
        <div className="panel stack">
          <p className="small muted">Leave at 0 if there is no pain. This is tracking, not a diagnosis.</p>
          {PAIN_REGIONS.map((r) => (
            <Stepper key={r} label={PAIN_REGION_LABELS[r]} value={pain[r] ?? 0} onChange={(v) => setPain({ ...pain, [r]: v ?? 0 })} min={0} max={10} testId={`pain-${r}`} />
          ))}
          {anyPain4 && <Note tone="danger">Pain of 4 or more pauses exercises that load that area. Tell a parent or coach.</Note>}
        </div>
      </Section>

      <Section title="Health">
        <div className="group">
          <Toggle checked={ill} onChange={setIll} label="Feeling ill" sub="Cold, fever, stomach, or similar" />
        </div>
        {ill && <input className="input" style={{ marginTop: 8 }} placeholder="What symptoms?" value={illNote} onChange={(e) => setIllNote(e.target.value)} maxLength={300} />}
        <input className="input" style={{ marginTop: 8 }} placeholder="Hydration note, optional" value={hydration} onChange={(e) => setHydration(e.target.value)} maxLength={300} />
        <details className="disclosure" style={{ marginTop: 8 }}>
          <summary>Anything worrying?</summary>
          <div className="group">
            {RED_FLAGS.map((f) => (
              <label className="switch-row" key={f}>
                <span className="grow">{RED_FLAG_LABELS[f]}</span>
                <input type="checkbox" checked={flags.includes(f)} onChange={(e) => setFlags(e.target.checked ? [...flags, f] : flags.filter((x) => x !== f))} className="check" />
              </label>
            ))}
          </div>
          <p className="small muted" style={{ marginTop: 6 }}>If any of these happen, tell a parent and get medical help. PeakForm pauses progression advice.</p>
        </details>
        <textarea className="input" style={{ marginTop: 8 }} placeholder="Note, optional" value={note} onChange={(e) => setNote(e.target.value)} maxLength={2000} />
      </Section>

      <div style={{ marginTop: 20 }}>
        <button type="button" className="btn btn-primary btn-large btn-block" onClick={() => void save()} data-testid="checkin-save">
          Save check in
        </button>
      </div>
    </div>
  );
}
