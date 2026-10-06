import { useEffect, useRef, useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../db/db';
import { KV, deleteAllData, ensureInitialized, kvGet, removeDemoData, restoreSnapshot, updateSettings, readAllTables, writeAllTables } from '../db/repo';
import { useSettings } from '../ui/state';
import { FilePick, Item, Note, PageHead, Section, Seg, useToast } from '../ui/components';
import { ExportAction } from '../ui/ExportAction';
import { applyImport, prepareBackup, prepareCsv, prepareImport, preparePlanExport } from '../services/exporter';
import type { ConflictChoice, ImportPreview } from '../domain/backup';
import { requestPersistence, storageEstimate } from '../lib/device';
import { checkRecommendation, type RecommendationCheck } from '../domain/report';
import { proposeExact } from '../services/planUpdate';
import { usePlan, useToday, useMealOptions } from '../ui/hooks';
import { exercise } from '../content/library';
import { WEEKDAY_NAMES, addDays } from '../domain/dates';
import { navigate } from '../ui/router';
import { generateDemo } from '../domain/demo';
import { BASELINE_PLAN } from '../content/plan';

const TABLE_LABELS: Record<string, string> = {
  settings: 'Settings',
  profile: 'Profile',
  plans: 'Plan versions',
  sessions: 'Workouts',
  exerciseSessions: 'Exercises in workouts',
  setLogs: 'Sets',
  suggestions: 'Progression suggestions',
  fourReviews: 'Four session reviews',
  foodLogs: 'Meals',
  waterLogs: 'Drinks',
  dayNotes: 'Day notes',
  checkins: 'Check ins',
  waist: 'Waist measurements',
  sleep: 'Sleep',
  pain: 'Pain entries',
  supplementLogs: 'Supplement logs',
  weeklyReviews: 'Weekly reviews',
  calendarExports: 'Calendar exports',
  backups: 'Backup history',
  mediaStatus: 'Video confirmations',
  photos: 'Photos',
  timerHistory: 'Timer history',
  customExercises: 'Custom exercises',
  migrations: 'Migration history',
  kv: 'Other app state',
};

export function DataScreen() {
  const s = useSettings();
  const mealOpts = useMealOptions();
  const today = useToday();
  const toast = useToast();
  const [pass, setPass] = useState('');
  const [encrypt, setEncrypt] = useState<'plain' | 'encrypted'>('encrypted');
  const lastBackup = useLiveQuery(() => kvGet<number>(KV.lastBackupAt), []);
  const snaps = useLiveQuery(() => db.snapshots.orderBy('createdAt').reverse().toArray(), []) ?? [];
  const [est, setEst] = useState<Awaited<ReturnType<typeof storageEstimate>>>(null);
  const [confirmDelete, setConfirmDelete] = useState(0);
  useEffect(() => {
    void storageEstimate().then(setEst);
  }, []);
  return (
    <div data-testid="data">
      <PageHead title="Backup and data" backTo="/more" />
      <Note title="Where your data lives">
        Everything is stored in this browser's storage on this phone. Nothing is sent to a server. iPhone can remove website storage in rare cases, for example when the phone runs very low on space, so keep a recent backup in Files or iCloud Drive. If you use PeakForm in a Safari tab instead of from the Home Screen, Safari may clear its data after about a week without a visit.
      </Note>

      <Section title="Status">
        <div className="group">
          <Item title="Last backup" end={lastBackup ? new Date(lastBackup).toLocaleDateString() : 'Never'} testId="last-backup" />
          <Item title="Storage used" end={est ? `${Math.round(est.usage / 1024)} KB` : 'Unknown'} />
          <Item
            title="Persistent storage"
            sub="Asks the browser to keep PeakForm's data when space runs low"
            end={est?.persisted === true ? 'Granted' : est?.persisted === false ? 'Not granted' : 'Unknown'}
            onClick={async () => {
              const r = await requestPersistence();
              setEst(await storageEstimate());
              toast(r === true ? 'Storage marked as persistent' : r === false ? 'The browser declined. Regular backups still protect you.' : 'Not supported in this browser');
            }}
          />
        </div>
      </Section>

      <Section title="Your plan">
        <div className="panel stack">
          <p className="small muted">The week with locations, equipment, space, duration, and stop rules, plus the example meals in grams. A private file for you, a parent, or a coach.</p>
          <ExportAction label="Prepare the plan file" testId="plan-export" prepare={() => preparePlanExport(mealOpts)} />
        </div>
      </Section>

      <Section title="Full backup">
        <div className="panel stack">
          <Seg label="Backup type" value={encrypt} onChange={setEncrypt} options={[{ value: 'encrypted', label: 'Encrypted' }, { value: 'plain', label: 'Plain' }]} />
          {encrypt === 'encrypted' ? (
            <>
              <input className="input" type="password" autoComplete="new-password" placeholder="Passphrase, at least 8 characters" value={pass} onChange={(e) => setPass(e.target.value)} data-testid="backup-pass" />
              <p className="small muted">Encrypted with AES on this phone. If you lose the passphrase, the backup cannot be opened by anyone, including you.</p>
            </>
          ) : (
            <p className="small muted">A plain backup is readable by anyone who gets the file. It contains your body measurements and logs. Store it somewhere private.</p>
          )}
          <ExportAction key={encrypt + (pass.length >= 8 ? 'ok' : 'no')} label="Create backup" primary testId="backup" prepare={async () => {
            if (encrypt === 'encrypted' && pass.length < 8) throw new Error('Use a passphrase of at least 8 characters.');
            return prepareBackup(encrypt === 'encrypted' ? pass : null);
          }} />
        </div>
      </Section>

      <Section title="Spreadsheet export">
        <div className="panel stack">
          <p className="small muted">Three CSV files: sets, food, and body measurements.</p>
          <ExportAction label="Create CSV files" testId="csv" prepare={() => prepareCsv()} />
        </div>
      </Section>

      <ImportSection />

      {snaps.length > 0 && (
        <Section title="Safety copies from before imports">
          <div className="group">
            {snaps.map((sn) => (
              <Item
                key={sn.id}
                title={new Date(sn.createdAt).toLocaleString()}
                sub={sn.reason}
                onClick={async () => {
                  if (!window.confirm('Restore this safety copy? It replaces the current data.')) return;
                  await restoreSnapshot(sn.id);
                  toast('Safety copy restored');
                }}
                end="Restore"
              />
            ))}
          </div>
        </Section>
      )}

      <Section title="Demo data">
        <div className="panel stack">
          <p className="small muted">Two weeks of made up example history, useful for trying the app. It contains no real person's data and can be removed in one tap.</p>
          {s.demoData ? (
            <button type="button" className="btn btn-outline" onClick={async () => { await removeDemoData(); toast('Demo data removed'); }} data-testid="remove-demo">
              Remove demo data
            </button>
          ) : (
            <button type="button" className="btn btn-outline" onClick={async () => { await loadDemo(today); toast('Demo data added'); }} data-testid="load-demo">
              Add demo data
            </button>
          )}
        </div>
      </Section>

      <Section title="Delete all data">
        <div className="panel stack" data-testid="delete-all">
          {confirmDelete === 0 && (
            <button type="button" className="btn btn-outline" style={{ color: 'var(--danger)' }} onClick={() => setConfirmDelete(1)}>
              Delete all data
            </button>
          )}
          {confirmDelete === 1 && (
            <>
              <Note tone="danger" title="This cannot be undone">
                All workouts, meals, measurements, settings, and photos on this phone will be erased. Make a final backup first if you might want them later.
              </Note>
              <ExportAction label="Make a final backup first" testId="final-backup" prepare={() => prepareBackup(null)} />
              <button type="button" className="btn btn-danger" onClick={() => setConfirmDelete(2)} data-testid="delete-continue">
                Continue to delete
              </button>
              <button type="button" className="btn btn-ghost" onClick={() => setConfirmDelete(0)}>
                Cancel
              </button>
            </>
          )}
          {confirmDelete === 2 && (
            <>
              <p>Last step. Tap to erase everything.</p>
              <button
                type="button"
                className="btn btn-danger btn-large"
                data-testid="delete-confirm"
                onClick={async () => {
                  await deleteAllData();
                  await ensureInitialized();
                  navigate('/today', { replace: true });
                  window.location.reload();
                }}
              >
                Erase everything
              </button>
              <button type="button" className="btn btn-ghost" onClick={() => setConfirmDelete(0)}>
                Cancel
              </button>
            </>
          )}
        </div>
      </Section>
    </div>
  );
}

export async function loadDemo(today: string, markOnboarded = true): Promise<void> {
  const demo = generateDemo(BASELINE_PLAN.days, addDays(today, -1), 2, { kind: (id) => exercise(id)?.kind ?? 'strength', logSides: (id) => exercise(id)?.logSides ?? false });
  const cur = await readAllTables();
  const merged = { ...cur };
  for (const [k, v] of Object.entries(demo)) merged[k as keyof typeof merged] = [...(cur[k as keyof typeof cur] ?? []), ...(v as Array<Record<string, unknown>>)];
  await writeAllTables(merged, 'replace');
  // The demo covers the last two weeks, so the plan counts as started when the demo does.
  const start = addDays(today, -14);
  await updateSettings((s) => ({ ...s, demoData: true, onboarded: markOnboarded ? true : s.onboarded, planStartDate: !s.planStartDate || s.planStartDate > start ? start : s.planStartDate }));
}

function ImportSection() {
  const toast = useToast();
  const fileRef = useRef<HTMLInputElement>(null);
  const [text, setText] = useState<string | null>(null);
  const [pass, setPass] = useState('');
  const [needPass, setNeedPass] = useState(false);
  const [preview, setPreview] = useState<ImportPreview | null>(null);
  const [error, setError] = useState('');
  const [mode, setMode] = useState<'replace' | ConflictChoice>('newer-wins');
  const reset = () => {
    setText(null);
    setPreview(null);
    setError('');
    setPass('');
    setNeedPass(false);
    if (fileRef.current) fileRef.current.value = '';
  };
  const parse = async (t: string, p: string | null) => {
    try {
      setError('');
      const r = await prepareImport(t, p);
      setPreview(r.preview);
      // A private setup file only carries settings, profile, and plan. Its values should win.
      if (r.preview.tables.every((x) => ['settings', 'profile', 'plans', 'kv'].includes(x.table))) setMode('use-incoming');
      setNeedPass(false);
    } catch (e) {
      const m = (e as Error).message;
      if (/encrypted/.test(m)) setNeedPass(true);
      setError(m);
    }
  };
  return (
    <Section title="Import">
      <div className="panel stack" data-testid="import">
        <p className="small muted">Restore a PeakForm backup or a private setup file. You will see exactly what is inside before anything changes, and a safety copy is made first.</p>
        <FilePick
          label="Choose a file"
          inputRef={fileRef}
          accept="application/json,.json"
          testId="import-file"
          onFile={async (f) => {
            if (f.size > 50 * 1024 * 1024) return setError('That file is too large to be a PeakForm backup.');
            const t = await f.text();
            setText(t);
            await parse(t, null);
          }}
        />
        {needPass && text && (
          <div className="row">
            <input className="input" type="password" placeholder="Backup passphrase" value={pass} onChange={(e) => setPass(e.target.value)} data-testid="import-pass" />
            <button type="button" className="btn btn-primary" onClick={() => void parse(text, pass)}>
              Open
            </button>
          </div>
        )}
        {error && !preview && (
          <Note tone="danger" title="Could not import">
            <span data-testid="import-error">{error}</span> Nothing was changed.
          </Note>
        )}
        {preview && (
          <div className="stack" data-testid="import-preview">
            <h3>Preview</h3>
            <p className="small">
              {preview.fileKind === 'encrypted' ? 'Encrypted backup' : 'Backup'} from {new Date(preview.exportedAt).toLocaleString()}
              {preview.dateRange ? `, with logs from ${preview.dateRange.from} to ${preview.dateRange.to}` : ''}.
            </p>
            {!preview.checksumOk && <Note tone="warn">The checksum does not match. The file was changed or damaged after export. Import only if you trust it.</Note>}
            {preview.migratedFrom.length > 0 && <p className="small muted">Upgraded from an older format.</p>}
            <div style={{ overflowX: 'auto' }}>
              <table className="prev-table">
                <thead>
                  <tr>
                    <th>Data</th>
                    <th>In file</th>
                    <th>New</th>
                    <th>Same</th>
                    <th>Different</th>
                  </tr>
                </thead>
                <tbody>
                  {preview.tables.map((t) => (
                    <tr key={t.table}>
                      <td>{TABLE_LABELS[t.table] ?? t.table}</td>
                      <td>{t.incoming}</td>
                      <td>{t.added}</td>
                      <td>{t.identical}</td>
                      <td>{t.conflicts}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {preview.issues.length > 0 && <Note tone="warn">{preview.issues.length} records failed validation and will be skipped.</Note>}
            <div>
              <div className="stepper-label">
                <span>When a record differs</span>
              </div>
              <Seg
                label="Conflict choice"
                value={mode}
                onChange={setMode}
                options={[
                  { value: 'newer-wins', label: 'Keep newer' },
                  { value: 'keep-existing', label: 'Keep mine' },
                  { value: 'use-incoming', label: 'Use file' },
                  { value: 'replace', label: 'Replace all' },
                ]}
              />
              {mode === 'replace' && <p className="hint">Replace all erases current data and uses only the file.</p>}
            </div>
            <button
              type="button"
              className="btn btn-primary"
              data-testid="import-apply"
              onClick={async () => {
                try {
                  await applyImport(preview, mode);
                  toast('Import complete. A safety copy was saved first.');
                  reset();
                } catch (e) {
                  setError(`Import failed and the safety copy was restored. ${(e as Error).message}`);
                  setPreview(null);
                }
              }}
            >
              Import
            </button>
            <button type="button" className="btn btn-ghost" onClick={reset}>
              Cancel
            </button>
          </div>
        )}
      </div>
    </Section>
  );
}

// ---------- Recommendation import ----------

export function RecommendationScreen() {
  const plan = usePlan();
  const toast = useToast();
  const [check, setCheck] = useState<RecommendationCheck | null>(null);
  if (!plan) return null;
  const items = plan.days.flatMap((d) => d.items);
  return (
    <div data-testid="recommendation">
      <PageHead title="Import a recommendation" backTo="/more" />
      <p className="small muted">
        A recommendation is a small JSON file, for example from a coach or an assistant you shared your report with. PeakForm checks it and shows every change. Plan changes open in the plan preview and are saved only when you activate them. Food targets and sets to failure are never imported.
      </p>
      <div style={{ marginTop: 12 }}>
        <FilePick label="Choose a recommendation file" accept="application/json,.json" testId="rec-file" onFile={async (f) => setCheck(checkRecommendation(await f.text()))} />
      </div>
      {check && !check.ok && (
        <Note tone="danger" title="This file cannot be used">
          <ul className="bullets small">
            {check.errors.slice(0, 6).map((x) => (
              <li key={x}>{x}</li>
            ))}
          </ul>
        </Note>
      )}
      {check?.ok && check.rec && (
        <Section title={`From ${check.rec.source}`}>
          <div className="group" data-testid="rec-diff">
            {check.rec.changes.map((c, i) => {
              if (c.type === 'plan-item') {
                const it = items.find((x) => x.id === c.planItemId);
                const from = it ? `${it.sets} sets${it.target.type === 'reps' ? `, ${it.target.min} to ${it.target.max}` : ''}, ${it.restSec} s rest${it.rir !== undefined ? `, ${it.rir} RIR` : ''}` : 'Not in the plan';
                const to = [c.sets !== undefined && `${c.sets} sets`, c.repMin !== undefined && `${c.repMin} to ${c.repMax ?? c.repMin}`, c.restSec !== undefined && `${c.restSec} s rest`, c.rir !== undefined && `${c.rir} RIR`].filter(Boolean).join(', ');
                return <Item key={i} title={it ? exercise(it.exerciseId)?.name ?? c.planItemId : c.planItemId} sub={`Now: ${from}. Proposed: ${to}. ${c.reason}`} />;
              }
              const to = [c.kcal !== undefined && `${c.kcal} kcal`, c.protein !== undefined && `${c.protein} g protein`, c.carbs !== undefined && `${c.carbs} g carbs`, c.fat !== undefined && `${c.fat} g fat`].filter(Boolean).join(', ');
              return <Item key={i} title={`${WEEKDAY_NAMES[c.weekday]} food targets, not imported`} sub={`Proposed: ${to}. ${c.reason}`} />;
            })}
          </div>
          {check.blocked.length > 0 && (
            <Note tone="danger" title="Blocked for safety">
              <ul className="bullets small">
                {check.blocked.map((b) => (
                  <li key={b}>{b}</li>
                ))}
              </ul>
              The file cannot be applied while it contains these changes.
            </Note>
          )}
          <button
            type="button"
            className="btn btn-primary btn-block"
            style={{ marginTop: 12 }}
            disabled={check.blocked.length > 0}
            data-testid="rec-apply"
            onClick={async () => {
              const rec = check.rec!;
              const planChanges = rec.changes.filter((c) => c.type === 'plan-item');
              if (planChanges.length) {
                const next = structuredClone(plan);
                for (const c of planChanges) {
                  if (c.type !== 'plan-item') continue;
                  for (const d of next.days)
                    for (const it of d.items)
                      if (it.id === c.planItemId) {
                        if (c.sets !== undefined) it.sets = c.sets;
                        if (c.restSec !== undefined) it.restSec = c.restSec;
                        if (c.rir !== undefined) it.rir = c.rir;
                        if (c.repMin !== undefined && it.target.type === 'reps') it.target = { type: 'reps', min: c.repMin, max: c.repMax ?? Math.max(c.repMin, it.target.max) };
                      }
                }
                // Like every other plan change, it is shown as a difference first and saved only when activated.
                await proposeExact(next, `Recommendation from ${rec.source}`.slice(0, 120), 'Changes from an imported recommendation');
                navigate('/plan');
                return;
              }
              toast('Nothing in this file changes the plan');
              navigate('/more');
            }}
          >
            See the plan with these changes
          </button>
        </Section>
      )}
      <Section title="File format">
        <pre className="panel small code">{`{
  "format": "peakform-recommendation",
  "version": 1,
  "source": "Coach",
  "createdAt": "2026-10-04",
  "changes": [
    { "type": "plan-item", "planItemId": "mon-5-barbell-squat",
      "repMin": 6, "repMax": 10, "reason": "Keep the range" },
    { "type": "plan-item", "planItemId": "sun-2-machine-bench-press",
      "sets": 3, "rir": 2, "reason": "Same dose" }
  ]
}`}</pre>
      </Section>
    </div>
  );
}
