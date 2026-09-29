import { useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../db/db';
import { getProfile, getTargets, saveProfile, saveTargets, savePlanVersion, updateSettings, KV, kvGet, kvSet } from '../db/repo';
import type { AppSettings, PlanRecord, Reminder, UserProfile } from '../db/records';
import { useSettings } from '../ui/state';
import { usePlan, useToday } from '../ui/hooks';
import { Item, Note, PageHead, Section, Seg, Stepper, Toggle, useToast } from '../ui/components';
import { WEEKDAY_SHORT, WEEKDAY_NAMES, addDays, formatDateKey } from '../domain/dates';
import { CITIES, fridayFor, sabbathWindow } from '../domain/sabbath';
import { prepareCalendar, recordCalendarExport } from '../services/exporter';
import { reminderHash } from '../domain/ics';
import { shareOrDownload } from '../lib/device';
import { NUTRITION_FLOORS, type NutritionTarget } from '../content/meals';
import { MUSCLES } from '../content/muscles';
import { exercise } from '../content/library';
import { navigate } from '../ui/router';
import { targetText } from './Train';
import { TAPER_TEMPLATE } from '../content/plan';
import { uid } from '../lib/id';
import { hashPin, newSalt } from '../lib/pin';

const upd = (fn: (s: AppSettings) => AppSettings) => void updateSettings(fn);

// ---------- Schedule and reminders ----------

export function ScheduleScreen() {
  const s = useSettings();
  const setReminder = (id: string, patch: Partial<Reminder>) => upd((x) => ({ ...x, reminders: x.reminders.map((r) => (r.id === id ? { ...r, ...patch } : r)) }));
  return (
    <div data-testid="schedule">
      <PageHead title="Schedule and reminders" backTo="/more" />
      <Note>
        PeakForm shows reminders inside the app. It cannot alert you while it is closed. For alarms on your phone, export the calendar after changing times.
      </Note>
      <Section title="Session times">
        <div className="group">
          <div className="item">
            <span className="item-main">Morning rope</span>
            <input className="input input-time" type="time" value={s.sessionTimes.morning} onChange={(e) => upd((x) => ({ ...x, sessionTimes: { ...x.sessionTimes, morning: e.target.value } }))} aria-label="Morning rope time" />
          </div>
          {[0, 1, 2, 3, 4, 5].map((d) => (
            <div className="item" key={d}>
              <span className="item-main">{WEEKDAY_NAMES[d]} main session</span>
              <input className="input input-time" type="time" value={s.sessionTimes.main[String(d)] ?? '16:30'} onChange={(e) => upd((x) => ({ ...x, sessionTimes: { ...x.sessionTimes, main: { ...x.sessionTimes.main, [String(d)]: e.target.value } } }))} aria-label={`${WEEKDAY_NAMES[d]} main session time`} />
            </div>
          ))}
          {[0, 5].map((d) => (
            <div className="item" key={`swim-${d}`}>
              <span className="item-main">{WEEKDAY_NAMES[d]} swim</span>
              <input className="input input-time" type="time" value={s.sessionTimes.swim[String(d)] ?? '19:30'} onChange={(e) => upd((x) => ({ ...x, sessionTimes: { ...x.sessionTimes, swim: { ...x.sessionTimes.swim, [String(d)]: e.target.value } } }))} aria-label={`${WEEKDAY_NAMES[d]} swim time`} />
            </div>
          ))}
        </div>
        <p className="small muted" style={{ marginTop: 6 }}>Keep swims at least three hours from the main session when possible, and Friday sessions before the Sabbath starts.</p>
      </Section>
      <Section title="Reminders">
        <div className="group" data-testid="reminders">
          {s.reminders.map((r) => (
            <div className="item" key={r.id} style={{ flexWrap: 'wrap' }}>
              <span className="item-main" style={{ minWidth: 140 }}>
                <span className="item-title" style={{ display: 'block' }}>{r.label}</span>
              </span>
              <input className="input input-time" type="time" value={r.time} onChange={(e) => setReminder(r.id, { time: e.target.value })} aria-label={`${r.label} time`} data-testid={`reminder-time-${r.id}`} />
              <span className="toggle">
                <input type="checkbox" role="switch" checked={r.enabled} onChange={(e) => setReminder(r.id, { enabled: e.target.checked })} aria-label={`${r.label} on`} />
              </span>
              <div className="chips" style={{ width: '100%', gap: 4 }}>
                {WEEKDAY_SHORT.map((wd, i) => (
                  <button key={wd} type="button" className="chip" style={{ minHeight: 34, padding: '0 9px' }} aria-pressed={r.weekdays.includes(i)} onClick={() => setReminder(r.id, { weekdays: r.weekdays.includes(i) ? r.weekdays.filter((x) => x !== i) : [...r.weekdays, i].sort() })}>
                    {wd}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      </Section>
      <Section>
        <button type="button" className="btn btn-primary btn-block" onClick={() => navigate('/more/calendar')}>
          Export these reminders to Calendar
        </button>
      </Section>
    </div>
  );
}

export function CalendarScreen() {
  const s = useSettings();
  const last = useLiveQuery(() => db.calendarExports.orderBy('createdAt').last(), []);
  const [file, setFile] = useState<{ file: File; events: number; excluded: number; until: string } | null>(null);
  const [msg, setMsg] = useState('');
  const stale = last && last.reminderHash !== reminderHash(s);
  return (
    <div data-testid="calendar">
      <PageHead title="Calendar export" backTo="/more" />
      <div className="stack">
        <p>
          PeakForm creates a calendar file with your reminders as weekly repeating events, each with an alarm. Apple Calendar then reminds you, even when PeakForm is closed.
        </p>
        {last ? (
          <Note tone={stale ? 'warn' : 'accent'} title={stale ? 'Your times changed since the last export' : 'Calendar is up to date'}>
            Last export {new Date(last.createdAt).toLocaleDateString()}, {last.eventCount} reminders, repeating until {last.untilDate}.
          </Note>
        ) : (
          <Note>No calendar exported yet.</Note>
        )}
        {s.sabbath.enabled && <p className="small muted">Sabbath Mode is on, so reminders inside the Friday to Saturday window are left out.</p>}
        {!file ? (
          <button type="button" className="btn btn-primary btn-block" data-testid="ics-prepare" onClick={async () => setFile(await prepareCalendar(s))}>
            Create calendar file
          </button>
        ) : (
          <>
            <p className="small">
              Ready: {file.events} reminders for 26 weeks{file.excluded ? `, ${file.excluded} Sabbath times left out` : ''}.
            </p>
            <button
              type="button"
              className="btn btn-primary btn-block"
              data-testid="ics-share"
              onClick={async () => {
                const r = await shareOrDownload([file.file], `${s.appName} reminders`);
                if (r !== 'cancelled') await recordCalendarExport(s, file.events, file.until);
                setMsg(r === 'shared' ? 'Shared. Choose Calendar, then Add All.' : r === 'downloaded' ? 'Saved. Open it from Files and tap Add All.' : 'Cancelled.');
                setFile(null);
              }}
            >
              Add to Calendar
            </button>
          </>
        )}
        {msg && <p className="small" role="status">{msg}</p>}
        <Section title="On iPhone">
          <ol className="steps small">
            <li>Tap Add to Calendar. If the share sheet opens, choose Calendar or Save to Files.</li>
            <li>Open the file and tap Add All. Pick a calendar, for example a new one called PeakForm.</li>
            <li>When you change times, export again. If you see doubles, delete the old PeakForm calendar first.</li>
          </ol>
        </Section>
      </div>
    </div>
  );
}

// ---------- Sabbath ----------

export function SabbathSettingsScreen() {
  const s = useSettings();
  const today = useToday();
  const sb = s.sabbath;
  const set = (patch: Partial<AppSettings['sabbath']>) => upd((x) => ({ ...x, sabbath: { ...x.sabbath, ...patch } }));
  const w = sabbathWindow(fridayFor(today), sb);
  return (
    <div data-testid="sabbath-settings">
      <PageHead title="Sabbath Mode" backTo="/more" />
      <div className="group">
        <Toggle checked={sb.enabled} onChange={(v) => set({ enabled: v })} label="Sabbath Mode" sub="Quiet reminders from Friday before sunset until Saturday night" testId="sabbath-toggle" />
      </div>
      {sb.enabled && (
        <>
          <Section title="Times">
            <Seg label="How to set times" value={sb.mode} onChange={(v) => set({ mode: v })} options={[{ value: 'manual', label: 'Enter times' }, { value: 'city', label: 'Calculate for a city' }]} />
            {sb.mode === 'manual' ? (
              <div className="grid-2" style={{ marginTop: 10 }}>
                <label className="field">
                  <span className="label">Friday from</span>
                  <input className="input" type="time" value={sb.fridayStart} onChange={(e) => set({ fridayStart: e.target.value })} data-testid="sabbath-start" />
                </label>
                <label className="field">
                  <span className="label">Saturday until</span>
                  <input className="input" type="time" value={sb.saturdayEnd} onChange={(e) => set({ saturdayEnd: e.target.value })} />
                </label>
              </div>
            ) : (
              <div className="stack" style={{ marginTop: 10 }}>
                <select
                  className="input"
                  value={sb.cityId ?? ''}
                  onChange={(e) => {
                    const c = CITIES.find((x) => x.id === e.target.value);
                    set({ cityId: e.target.value || null, candleOffsetMin: c?.candleOffsetMin ?? sb.candleOffsetMin, endOffsetMin: c?.endOffsetMin ?? sb.endOffsetMin });
                  }}
                  aria-label="City"
                >
                  <option value="">Choose a city</option>
                  {CITIES.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name}
                    </option>
                  ))}
                </select>
                <div className="grid-2">
                  <Stepper label="Minutes before sunset" value={sb.candleOffsetMin} onChange={(v) => set({ candleOffsetMin: v ?? 0 })} max={90} />
                  <Stepper label="Minutes after sunset" value={sb.endOffsetMin} onChange={(v) => set({ endOffsetMin: v ?? 0 })} max={120} />
                </div>
                <p className="small muted">Sunset is calculated on this phone from the city you pick. No location is requested or sent anywhere. Times are approximate, so follow your community's calendar.</p>
              </div>
            )}
          </Section>
          <Section title="This week">
            <div className="panel" data-testid="sabbath-window">
              Quiet from <b>{formatDateKey(w.friday, { weekday: 'long' })} {w.start}</b> until <b>{formatDateKey(w.saturday, { weekday: 'long' })} {w.end}</b>.
              <p className="small muted" style={{ marginTop: 4 }}>
                Saturday is a full rest day. The weekly review is on Sunday evening. Saturday meals can be logged afterwards with the plate guide.
              </p>
            </div>
          </Section>
        </>
      )}
    </div>
  );
}

// ---------- Settings ----------

export function SettingsScreen() {
  const s = useSettings();
  const profile = useLiveQuery(() => getProfile(), []);
  const [p, setP] = useState<UserProfile | null>(null);
  const toast = useToast();
  const cur = p ?? profile ?? null;
  return (
    <div data-testid="settings">
      <PageHead title="Settings" backTo="/more" />
      <Section title="App">
        <div className="panel stack">
          <label className="field">
            <span className="label">App name</span>
            <input className="input" value={s.appName} maxLength={40} onChange={(e) => upd((x) => ({ ...x, appName: e.target.value || 'PeakForm' }))} data-testid="app-name" />
          </label>
          <div>
            <div className="stepper-label">
              <span>Theme</span>
            </div>
            <Seg label="Theme" value={s.theme} onChange={(v) => upd((x) => ({ ...x, theme: v }))} options={[{ value: 'system', label: 'System' }, { value: 'light', label: 'Light' }, { value: 'dark', label: 'Dark' }]} />
          </div>
          <div>
            <div className="stepper-label">
              <span>Reduce motion</span>
            </div>
            <Seg label="Reduce motion" value={s.reducedMotion} onChange={(v) => upd((x) => ({ ...x, reducedMotion: v }))} options={[{ value: 'system', label: 'System' }, { value: 'on', label: 'On' }, { value: 'off', label: 'Off' }]} />
          </div>
          <div>
            <div className="stepper-label">
              <span>Clock</span>
            </div>
            <Seg label="Clock" value={s.units.clock} onChange={(v) => upd((x) => ({ ...x, units: { ...x.units, clock: v } }))} options={[{ value: '24h', label: '24 hour' }, { value: '12h', label: '12 hour' }]} />
          </div>
          <p className="small muted">Weights are kilograms and lengths are centimetres across the app.</p>
        </div>
      </Section>
      <Section title="Rest timer">
        <div className="group">
          <Toggle checked={s.autoStartRest} onChange={(v) => upd((x) => ({ ...x, autoStartRest: v }))} label="Start rest after each set" testId="auto-rest" />
          <Toggle checked={s.keepScreenOn} onChange={(v) => upd((x) => ({ ...x, keepScreenOn: v }))} label="Keep the screen on during workouts" sub="Works where the browser supports it" />
          <Toggle checked={s.vibration} onChange={(v) => upd((x) => ({ ...x, vibration: v }))} label="Vibrate when rest ends" sub="iPhone browsers do not allow vibration, so this may do nothing" />
          <div className="switch-row">
            <span>Sound</span>
            <div style={{ width: 200 }}>
              <Seg label="Sound" value={s.restSound} onChange={(v) => upd((x) => ({ ...x, restSound: v }))} options={[{ value: 'off', label: 'Off' }, { value: 'beep', label: 'Beep' }, { value: 'chime', label: 'Chime' }]} />
            </div>
          </div>
        </div>
        <p className="small muted" style={{ marginTop: 6 }}>Sounds play only while PeakForm is open. The timer stays correct after the screen locks and shows how long ago rest ended.</p>
      </Section>
      <Section title="Equipment steps">
        <div className="panel grid-2">
          <Stepper label="Barbell" unit="kg" value={s.equipment.barbellKg} onChange={(v) => v && upd((x) => ({ ...x, equipment: { ...x.equipment, barbellKg: v } }))} step={0.25} decimals={2} min={0.25} max={20} />
          <Stepper label="Machine" unit="kg" value={s.equipment.machineKg} onChange={(v) => v && upd((x) => ({ ...x, equipment: { ...x.equipment, machineKg: v } }))} step={0.25} decimals={2} min={0.25} max={20} />
          <Stepper label="Cable" unit="kg" value={s.equipment.cableKg} onChange={(v) => v && upd((x) => ({ ...x, equipment: { ...x.equipment, cableKg: v } }))} step={0.25} decimals={2} min={0.25} max={20} />
          <Stepper label="Dumbbell" unit="kg" value={s.equipment.dumbbellKg} onChange={(v) => v && upd((x) => ({ ...x, equipment: { ...x.equipment, dumbbellKg: v } }))} step={0.25} decimals={2} min={0.25} max={20} />
        </div>
        <p className="small muted" style={{ marginTop: 6 }}>Load suggestions never use a step your equipment cannot make. Upper body increases aim near {Math.round(s.equipment.upperPct * 1000) / 10}%, lower body near {Math.round(s.equipment.lowerPct * 1000) / 10}%, rounded to these steps.</p>
      </Section>
      <Section title="Pool">
        <Stepper label="Pool length" unit="m" value={s.poolLengthM} onChange={(v) => upd((x) => ({ ...x, poolLengthM: v }))} max={100} placeholder="Not set" />
        <p className="hint">Distance is only shown once this is set. One round trip is there and back.</p>
      </Section>
      <Section title="Profile, private">
        {cur && (
          <div className="panel stack">
            <p className="small muted">Stored only on this phone. Never part of the app's code or website.</p>
            <label className="field">
              <span className="label">Name</span>
              <input className="input" value={cur.name} maxLength={60} onChange={(e) => setP({ ...cur, name: e.target.value })} />
            </label>
            <div className="grid-2">
              <Stepper label="Height" unit="cm" value={cur.heightCm} onChange={(v) => setP({ ...cur, heightCm: v })} max={250} />
              <Stepper label="Birth year" value={cur.birthYear} onChange={(v) => setP({ ...cur, birthYear: v })} min={1990} max={2025} />
            </div>
            <label className="field">
              <span className="label">Goals</span>
              <textarea className="input" value={cur.goals.join('\n')} onChange={(e) => setP({ ...cur, goals: e.target.value.split('\n').slice(0, 10) })} maxLength={1500} />
            </label>
            <button
              type="button"
              className="btn btn-primary"
              onClick={async () => {
                await saveProfile(cur);
                setP(null);
                toast('Profile saved');
              }}
            >
              Save profile
            </button>
          </div>
        )}
      </Section>
      <Section title="Event and plan dates">
        <div className="panel stack">
          <label className="field">
            <span className="label">Plan start date</span>
            <input className="input" type="date" value={s.planStartDate ?? ''} onChange={(e) => upd((x) => ({ ...x, planStartDate: e.target.value || null }))} />
          </label>
          <label className="field">
            <span className="label">Event, for an optional taper week</span>
            <input className="input" value={s.eventLabel} maxLength={80} placeholder="For example, a tournament" onChange={(e) => upd((x) => ({ ...x, eventLabel: e.target.value }))} />
          </label>
          <input className="input" type="date" value={s.eventDate ?? ''} onChange={(e) => upd((x) => ({ ...x, eventDate: e.target.value || null }))} aria-label="Event date" />
          {s.eventDate && (
            <div className="group">
              {TAPER_TEMPLATE.map((t) => (
                <Item key={t.label} title={`${formatDateKey(addDays(s.eventDate!, t.offsetDays))}: ${t.label}`} sub={t.detail} />
              ))}
            </div>
          )}
          <p className="small muted">The taper is optional and never includes dehydration or eating less. No date based result is promised.</p>
        </div>
      </Section>
    </div>
  );
}

// ---------- Nutrition targets ----------

export function TargetsScreen() {
  const saved = useLiveQuery(() => getTargets(), []);
  const [t, setT] = useState<NutritionTarget[] | null>(null);
  const toast = useToast();
  const cur = t ?? saved;
  if (!cur) return null;
  const set = (i: number, patch: Partial<NutritionTarget>) => setT(cur.map((x, j) => (j === i ? { ...x, ...patch, kcalBand: patch.kcal !== undefined ? [Math.max(NUTRITION_FLOORS.kcal, patch.kcal - 100), patch.kcal + 100] : x.kcalBand } : x)));
  return (
    <div data-testid="targets">
      <PageHead title="Nutrition targets" backTo="/more" />
      <Note>These are starting points for a fourteen day observation. Review calorie targets with a parent, and ideally a pediatrician or pediatric sports dietitian. PeakForm never saves a day below {NUTRITION_FLOORS.kcal.toLocaleString('en-US')} calories or {NUTRITION_FLOORS.carbs} g carbohydrate.</Note>
      {[0, 1, 2, 3, 4, 5, 6].map((wd) => {
        const i = cur.findIndex((x) => x.weekday === wd);
        const x = cur[i]!;
        return (
          <Section key={wd} title={`${WEEKDAY_NAMES[wd]}, ${x.label}`}>
            <div className="panel grid-2">
              <Stepper label="Calories" value={x.kcal} onChange={(v) => v && set(i, { kcal: v })} step={50} min={NUTRITION_FLOORS.kcal} max={4000} />
              <Stepper label="Protein" unit="g" value={x.protein} onChange={(v) => v && set(i, { protein: v, proteinRange: [Math.min(v, 150), Math.max(v, 175)] })} step={5} max={250} />
              <Stepper label="Carbohydrate" unit="g" value={x.carbs} onChange={(v) => v && set(i, { carbs: v })} step={5} min={NUTRITION_FLOORS.carbs} max={600} />
              <Stepper label="Fat" unit="g" value={x.fat} onChange={(v) => v && set(i, { fat: v })} step={2} max={200} />
            </div>
          </Section>
        );
      })}
      <div style={{ marginTop: 16 }} className="stack">
        <button
          type="button"
          className="btn btn-primary btn-block"
          disabled={!t}
          onClick={async () => {
            await saveTargets(cur);
            setT(null);
            toast('Targets saved');
          }}
        >
          Save targets
        </button>
        <button
          type="button"
          className="btn btn-ghost btn-block"
          onClick={async () => {
            await kvSet(KV.targets, null);
            setT(null);
            toast('Baseline targets restored');
          }}
        >
          Restore baseline targets
        </button>
      </div>
    </div>
  );
}

// ---------- Supplements ----------

export function SupplementsScreen() {
  const s = useSettings();
  const today = useToday();
  const toast = useToast();
  const logs = useLiveQuery(() => db.supplementLogs.where('date').equals(today).toArray(), [today]) ?? [];
  const setSup = (id: string, patch: Partial<AppSettings['supplements'][number]>) => upd((x) => ({ ...x, supplements: x.supplements.map((y) => (y.id === id ? { ...y, ...patch } : y)) }));
  return (
    <div data-testid="supplements">
      <PageHead title="Supplements" backTo="/more" />
      <Note>A tracker, not advice to take anything. Review every supplement with a parent and a clinician. No fat burners, test boosters, dehydration products, or high stimulant pre workouts.</Note>
      {s.supplements.map((sup) => {
        const taken = logs.filter((l) => l.supplementId === sup.id).length;
        const needsReview = sup.kind === 'creatine' && !sup.reviewedWithGuardian;
        return (
          <Section key={sup.id} title={sup.name}>
            {sup.kind === 'creatine' && (
              <div className="group" style={{ marginBottom: 8 }}>
                <Toggle checked={sup.reviewedWithGuardian} onChange={(v) => setSup(sup.id, { reviewedWithGuardian: v })} label="A parent and a clinician have reviewed creatine for me" sub="Asked once because you are under 18" testId="creatine-review" />
              </div>
            )}
            <div className="panel stack">
              <label className="field">
                <span className="label">Product</span>
                <input className="input" value={sup.product} maxLength={120} onChange={(e) => setSup(sup.id, { product: e.target.value })} placeholder="Brand and product name" />
              </label>
              <div className="grid-2">
                <Stepper label={`Dose (${sup.unit})`} value={sup.dose} onChange={(v) => setSup(sup.id, { dose: v ?? 0 })} step={sup.kind === 'creatine' ? 0.5 : 1} decimals={1} max={20} />
                {sup.kind === 'calcium' && <Stepper label="Calcium per dose" unit="mg" value={sup.calciumMg ?? 0} onChange={(v) => setSup(sup.id, { calciumMg: v ?? 0 })} step={50} max={1500} />}
                {sup.kind === 'omega3' && <Stepper label="EPA plus DHA" unit="mg" value={sup.epaDhaMg ?? 0} onChange={(v) => setSup(sup.id, { epaDhaMg: v ?? 0 })} step={50} max={3000} />}
              </div>
              {sup.kind === 'calcium' && <p className="small muted">Teens need about 1,300 mg a day from food and supplements together. Food usually covers most of it. The Eat screen adds both. More than needed brings no benefit.</p>}
              {sup.kind === 'omega3' && <p className="small muted">Log EPA plus DHA from the label, not the total fish oil amount.</p>}
              {sup.kind === 'creatine' && <p className="small muted">The earlier plan discussed 3 to 5 g a day without a loading phase. Evidence in under 18s is limited, so this stays a decision for you, a parent, and a clinician.</p>}
              <button
                type="button"
                className="btn btn-outline"
                disabled={needsReview || sup.dose <= 0}
                onClick={async () => {
                  const t = Date.now();
                  await db.supplementLogs.put({ id: uid('sup'), createdAt: t, updatedAt: t, date: today, at: t, supplementId: sup.id, amount: 1, unit: 'dose' });
                  toast(`${sup.name} logged`);
                }}
              >
                {taken ? `Taken today (${taken}), log again` : 'Log today'}
              </button>
              {needsReview && <p className="small muted">Logging starts once the review is confirmed.</p>}
              {sup.dose <= 0 && !needsReview && <p className="small muted">Enter your dose to log it.</p>}
            </div>
          </Section>
        );
      })}
      <Section title="Protein powder">
        <p className="small muted">Optional food convenience, only when food protein is short. Prefer a third party tested product, reviewed with a parent.</p>
      </Section>
      <Section title="About testosterone">
        <p className="small muted">Normal development is supported by enough total food, enough dietary fat and carbohydrate, good sleep, gradual fat loss, and resistance training. Extreme dieting works against recovery and development. PeakForm has no testosterone score because there is no honest way to estimate one from these logs.</p>
      </Section>
    </div>
  );
}

// ---------- App lock ----------

export function LockSettingsScreen() {
  const s = useSettings();
  const toast = useToast();
  const [pin, setPin] = useState('');
  return (
    <div data-testid="lock-settings">
      <PageHead title="App lock" backTo="/more" />
      <Note>The lock is a privacy convenience that hides PeakForm from someone picking up your unlocked phone. It is not encryption. Your iPhone passcode is what protects the data on the device.</Note>
      {s.lock.enabled ? (
        <div className="stack" style={{ marginTop: 12 }}>
          <Stepper label="Lock after inactivity" unit="min" value={s.lock.idleMinutes} onChange={(v) => upd((x) => ({ ...x, lock: { ...x.lock, idleMinutes: v ?? 5 } }))} min={1} max={120} />
          <button
            type="button"
            className="btn btn-outline"
            onClick={() => {
              upd((x) => ({ ...x, lock: { ...x.lock, enabled: false, pinHash: null, salt: null } }));
              toast('App lock turned off');
            }}
          >
            Turn off app lock
          </button>
        </div>
      ) : (
        <div className="stack" style={{ marginTop: 12 }}>
          <label className="field">
            <span className="label">Choose a 4 to 8 digit PIN</span>
            <input className="input" inputMode="numeric" pattern="[0-9]*" type="password" autoComplete="new-password" maxLength={8} value={pin} onChange={(e) => setPin(e.target.value.replace(/\D/g, ''))} data-testid="pin-new" />
          </label>
          <p className="small muted">If you forget it, the only way back in is to erase PeakForm's data on this phone and restore a backup.</p>
          <button
            type="button"
            className="btn btn-primary"
            disabled={pin.length < 4}
            onClick={async () => {
              const salt = newSalt();
              const hash = await hashPin(pin, salt);
              upd((x) => ({ ...x, lock: { ...x.lock, enabled: true, pinHash: hash, salt } }));
              setPin('');
              toast('App lock on');
            }}
          >
            Turn on app lock
          </button>
        </div>
      )}
    </div>
  );
}

// ---------- Plan editor ----------

export function PlanEditorScreen() {
  const plan = usePlan();
  const versions = useLiveQuery(() => db.plans.orderBy('version').reverse().toArray(), []) ?? [];
  const [draft, setDraft] = useState<PlanRecord | null>(null);
  const [itemId, setItemId] = useState<string | null>(null);
  const [note, setNote] = useState('');
  const toast = useToast();
  if (!plan) return null;
  const cur = draft ?? plan;
  const item = cur.days.flatMap((d) => d.items).find((i) => i.id === itemId);
  const editItem = (patch: Partial<typeof item>) =>
    setDraft({ ...cur, days: cur.days.map((d) => ({ ...d, items: d.items.map((i) => (i.id === itemId ? ({ ...i, ...patch } as typeof i) : i)) })) });
  return (
    <div data-testid="plan-editor">
      <PageHead title="Edit the plan" eyebrow={`Version ${plan.version}`} backTo="/more" />
      <Note>Changes are saved as a new plan version. Sessions you already logged keep the prescription they were done against.</Note>
      {item ? (
        <Section title={exercise(item.exerciseId)?.name ?? item.exerciseId}>
          <div className="panel stack">
            <p className="small muted">Current: {targetText(item)}</p>
            <div className="grid-2">
              <Stepper label="Sets" value={item.sets} onChange={(v) => v && editItem({ sets: v })} min={1} max={10} />
              <Stepper label="Rest" unit="s" value={item.restSec} onChange={(v) => editItem({ restSec: v ?? 0 })} step={15} max={900} />
              {item.target.type === 'reps' && (
                <>
                  <Stepper label="Reps from" value={item.target.min} onChange={(v) => v && editItem({ target: { type: 'reps', min: v, max: Math.max(v, (item.target as { max: number }).max) } })} min={1} max={50} />
                  <Stepper label="Reps to" value={item.target.max} onChange={(v) => v && editItem({ target: { type: 'reps', min: Math.min(v, (item.target as { min: number }).min), max: v } })} min={1} max={50} />
                </>
              )}
              {item.rir !== undefined && <Stepper label="Reps in reserve" value={item.rir} onChange={(v) => editItem({ rir: Math.max(1, v ?? 2) })} min={1} max={5} />}
            </div>
            <p className="small muted">Reps in reserve cannot go below 1. Routine sets are never taken to failure.</p>
            <button type="button" className="btn btn-outline" onClick={() => setItemId(null)}>
              Done with this exercise
            </button>
          </div>
        </Section>
      ) : (
        cur.days
          .filter((d) => !d.isRest)
          .map((d) => (
            <Section key={d.key} title={`${WEEKDAY_NAMES[d.weekday]}, ${d.title}`}>
              <div className="group">
                {d.items.map((i) => (
                  <Item key={i.id} title={exercise(i.exerciseId)?.name ?? i.exerciseId} sub={targetText(i)} onClick={() => setItemId(i.id)} />
                ))}
              </div>
            </Section>
          ))
      )}
      {draft && (
        <div className="panel stack" style={{ marginTop: 16 }}>
          <input className="input" placeholder="What changed and why" value={note} onChange={(e) => setNote(e.target.value)} maxLength={300} />
          <button
            type="button"
            className="btn btn-primary"
            data-testid="save-plan"
            onClick={async () => {
              await savePlanVersion(draft, note || 'Edited in the app.');
              setDraft(null);
              setNote('');
              toast('New plan version saved');
            }}
          >
            Save as a new version
          </button>
          <button type="button" className="btn btn-ghost" onClick={() => setDraft(null)}>
            Discard changes
          </button>
        </div>
      )}
      <Section title="Versions">
        <div className="group">
          {versions.map((v) => (
            <Item
              key={v.id}
              title={`Version ${v.version}${v.id === plan.id ? ', active' : ''}`}
              sub={`${new Date(v.createdAt).toLocaleDateString()}. ${v.changeNote}`}
              onClick={v.id === plan.id ? undefined : () => void updateSettings({ activePlanId: v.id })}
              end={v.id === plan.id ? undefined : 'Use'}
            />
          ))}
        </div>
      </Section>
    </div>
  );
}

// ---------- Custom exercise ----------

export function CustomExerciseScreen() {
  const toast = useToast();
  const [name, setName] = useState('');
  const [kind, setKind] = useState<'strength' | 'bodyweight' | 'hold'>('strength');
  const [primary, setPrimary] = useState<string[]>([]);
  const [secondary, setSecondary] = useState<string[]>([]);
  const [sides, setSides] = useState(false);
  const [inc, setInc] = useState<'upper' | 'lower' | 'none'>('upper');
  const [equipment, setEquipment] = useState('');
  const [notes, setNotes] = useState('');
  const toggle = (list: string[], set: (x: string[]) => void, id: string) => set(list.includes(id) ? list.filter((x) => x !== id) : [...list, id]);
  return (
    <div data-testid="custom-exercise">
      <PageHead title="New exercise" backTo="/library" />
      <div className="stack">
        <input className="input" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} maxLength={80} />
        <Seg label="Type" value={kind} onChange={setKind} options={[{ value: 'strength', label: 'Weighted' }, { value: 'bodyweight', label: 'Bodyweight' }, { value: 'hold', label: 'Hold' }]} />
        <Seg label="Load steps" value={inc} onChange={setInc} options={[{ value: 'upper', label: 'Upper body' }, { value: 'lower', label: 'Lower body' }, { value: 'none', label: 'None' }]} />
        <input className="input" placeholder="Equipment, for example cable" value={equipment} onChange={(e) => setEquipment(e.target.value)} maxLength={200} />
        <div className="group">
          <Toggle checked={sides} onChange={setSides} label="Log left and right separately" />
        </div>
        <Section title="Primary muscles">
          <div className="chips">
            {MUSCLES.map((m) => (
              <button key={m.id} type="button" className="chip" aria-pressed={primary.includes(m.id)} onClick={() => toggle(primary, setPrimary, m.id)}>
                {m.shortName}
              </button>
            ))}
          </div>
        </Section>
        <Section title="Secondary muscles">
          <div className="chips">
            {MUSCLES.filter((m) => !primary.includes(m.id)).map((m) => (
              <button key={m.id} type="button" className="chip" aria-pressed={secondary.includes(m.id)} onClick={() => toggle(secondary, setSecondary, m.id)}>
                {m.shortName}
              </button>
            ))}
          </div>
        </Section>
        <textarea className="input" placeholder="Notes and cues" value={notes} onChange={(e) => setNotes(e.target.value)} maxLength={1000} />
        <button
          type="button"
          className="btn btn-primary btn-block"
          disabled={!name || primary.length === 0}
          onClick={async () => {
            const t = Date.now();
            const id = uid('custom');
            await db.customExercises.put({ id, createdAt: t, updatedAt: t, name, kind, primary, secondary: secondary.filter((x) => !primary.includes(x)), logSides: sides, loadIncrement: inc, equipment, notes });
            toast('Exercise saved');
            navigate(`/exercise/${id}`);
          }}
        >
          Save exercise
        </button>
      </div>
    </div>
  );
}

export async function supplementReviewSeen(): Promise<boolean> {
  return Boolean(await kvGet<boolean>(KV.supplementReview));
}
