import { db } from '../db/db';
import { KV, getAthlete, kvGet, kvSet, readAllTables, restoreSnapshot, snapshotBeforeImport, writeAllTables } from '../db/repo';
import { reviewedEnergy } from '../domain/athlete';
import { exampleDayTotals } from '../domain/nutrition';
import { templatesForDay } from '../content/meals';
import { SESSION_LABELS } from '../content/plan';
import { LOCATION_LABEL } from '../content/traits';
import { WEEKDAY_NAMES } from '../domain/dates';
import type { PlanRecord } from '../db/records';
import type { ReportContext } from '../domain/report';
import { TABLE_NAMES, type AppSettings } from '../db/records';
import { buildPreview, decryptBackup, detectFile, encryptBackup, makeBackup, mergeTables, toCsv, type BackupFile, type ConflictChoice, type ImportPreview, type TableData } from '../domain/backup';
import { generateWeeklyReview, type ReviewData, type WeeklyReview } from '../domain/review';
import { coachReportJson, coachReportMarkdown } from '../domain/report';
import { buildIcs, reminderHash } from '../domain/ics';
import { exercise, exerciseName } from '../content/library';
import { dateKey } from '../domain/dates';
import { shareOrDownload } from '../lib/device';
import { uid } from '../lib/id';

export const APP_VERSION = typeof __APP_VERSION__ === 'string' ? __APP_VERSION__ : '0.0.0';

const stamp = () => dateKey();

async function recordBackup(kind: 'plain' | 'encrypted' | 'coach-report' | 'csv', checksum: string, counts: Record<string, number>, note: string) {
  const t = Date.now();
  await db.backups.put({ id: uid('bak'), createdAt: t, updatedAt: t, kind, checksum, counts, note });
  if (kind === 'plain' || kind === 'encrypted') await kvSet(KV.lastBackupAt, t);
}

// ---------- Weekly review ----------

export async function reviewData(): Promise<ReviewData> {
  const settings = await db.settings.get('app');
  const plan = settings ? await db.plans.get(settings.activePlanId) : undefined;
  const athlete = await getAthlete();
  const reviewed = reviewedEnergy(athlete);
  const profile = await db.profile.get('me');
  const example = exampleDayTotals(templatesForDay(1, undefined, { meatToDairyHours: athlete.kosher.enabled ? athlete.kosher.meatToDairyHours : null }));
  return {
    planDays: plan?.days ?? [],
    sessions: await db.sessions.toArray(),
    exerciseSessions: await db.exerciseSessions.toArray(),
    setLogs: await db.setLogs.toArray(),
    foodLogs: await db.foodLogs.toArray(),
    waterLogs: await db.waterLogs.toArray(),
    checkins: await db.checkins.toArray(),
    waist: await db.waist.toArray(),
    sleep: await db.sleep.toArray(),
    pain: await db.pain.toArray(),
    suggestions: await db.suggestions.toArray(),
    fourReviews: await db.fourReviews.toArray(),
    reviewedKcal: reviewed?.kcalRange ?? null,
    exampleKcal: Math.round(example.mid.kcal),
    sportLogs: await db.sportLogs.toArray(),
    athlete,
    ageYears: profile?.birthYear ? new Date().getFullYear() - profile.birthYear : null,
    creatineActive: (settings?.supplements ?? []).some((x) => x.kind === 'creatine' && x.active),
    lastBackupAt: (await kvGet<number>(KV.lastBackupAt)) ?? null,
    exerciseKind: (id) => exercise(id)?.kind,
    exerciseName,
  };
}

export async function runWeeklyReview(weekStart: string): Promise<WeeklyReview> {
  const review = generateWeeklyReview(await reviewData(), weekStart, Date.now());
  const existing = await db.weeklyReviews.where('weekStart').equals(weekStart).first();
  const t = Date.now();
  await db.weeklyReviews.put({ id: existing?.id ?? uid('rev'), createdAt: existing?.createdAt ?? t, updatedAt: t, weekStart, generatedAt: t, data: review });
  return review;
}

/**
 * iOS only allows sharing straight after a tap, so files are prepared first and shared
 * by a second tap with no waiting in between.
 */
export async function prepareCoachReport(review: WeeklyReview, settings: AppSettings): Promise<File[]> {
  const plan = await db.plans.get(settings.activePlanId);
  const logs = { sessions: await db.sessions.toArray(), setLogs: await db.setLogs.toArray(), foodLogs: await db.foodLogs.toArray(), exerciseName, context: plan ? reportContext(plan, await getAthlete()) : undefined };
  const opts = { includeNotes: settings.coachShare.includeNotes, includePhotos: settings.coachShare.includePhotos, appVersion: APP_VERSION, appName: settings.appName };
  const md = coachReportMarkdown(review, logs, opts);
  const json = coachReportJson(review, logs, opts);
  const files = [
    new File([md], `peakform-review-${review.weekStart}.md`, { type: 'text/markdown' }),
    new File([JSON.stringify(json, null, 2)], `peakform-review-${review.weekStart}.json`, { type: 'application/json' }),
  ];
  if (settings.coachShare.includePhotos) {
    const ids = new Set(logs.foodLogs.filter((f) => f.date >= review.weekStart && f.date <= review.weekEnd && f.photoId).map((f) => f.photoId!));
    for (const p of await db.photos.bulkGet([...ids])) {
      if (!p) continue;
      const blob = await (await fetch(p.dataUrl)).blob();
      files.push(new File([blob], `${p.id}.jpg`, { type: 'image/jpeg' }));
    }
  }
  return files;
}

export async function shareFiles(files: File[], title: string, record?: { kind: 'plain' | 'encrypted' | 'coach-report' | 'csv'; checksum: string; counts: Record<string, number>; note: string }): Promise<string> {
  const r = await shareOrDownload(files, title);
  if (record && r !== 'cancelled') await recordBackup(record.kind, record.checksum, record.counts, record.note);
  return r;
}

// ---------- Backups ----------

export interface PreparedExport {
  files: File[];
  title: string;
  record?: { kind: 'plain' | 'encrypted' | 'coach-report' | 'csv'; checksum: string; counts: Record<string, number>; note: string };
}

export async function prepareBackup(passphrase: string | null): Promise<PreparedExport> {
  const tables = await readAllTables();
  const backup = await makeBackup(tables, APP_VERSION);
  const counts = Object.fromEntries(TABLE_NAMES.map((n) => [n, tables[n]?.length ?? 0]));
  let file: File;
  if (passphrase) {
    const enc = await encryptBackup(backup, passphrase);
    file = new File([JSON.stringify(enc)], `peakform-backup-${stamp()}-encrypted.json`, { type: 'application/json' });
  } else {
    file = new File([JSON.stringify(backup)], `peakform-backup-${stamp()}.json`, { type: 'application/json' });
  }
  return { files: [file], title: 'PeakForm backup', record: { kind: passphrase ? 'encrypted' : 'plain', checksum: backup.checksum, counts, note: file.name } };
}

export async function prepareCsv(): Promise<PreparedExport> {
  const t = await readAllTables();
  const sets = (t.setLogs ?? []).map((s) => ({ ...s, exercise: exerciseName(String(s.exerciseId)), completed: new Date(Number(s.completedAt)).toISOString() }));
  const food = (t.foodLogs ?? []).flatMap((f) =>
    (f.items as Array<{ name: string; estimate: { method: string; gramsLow: number; gramsMid: number; gramsHigh: number }; low: { kcal: number; protein: number }; mid: { kcal: number; protein: number }; high: { kcal: number; protein: number } }>).map((i) => ({
      date: f.date,
      slot: f.slot,
      time: f.time,
      source: f.source,
      food: i.name,
      method: i.estimate.method,
      grams_low: i.estimate.gramsLow,
      grams_mid: i.estimate.gramsMid,
      grams_high: i.estimate.gramsHigh,
      kcal_low: Math.round(i.low.kcal),
      kcal_mid: Math.round(i.mid.kcal),
      kcal_high: Math.round(i.high.kcal),
      protein_mid: Math.round(i.mid.protein),
    })),
  );
  const body = t.checkins ?? [];
  const files = [
    new File([toCsv(sets, ['completed', 'exercise', 'setIndex', 'side', 'warmup', 'weightKg', 'reps', 'rir', 'seconds', 'form', 'pain', 'painScore', 'quality', 'landing', 'roundTrips', 'rpe'])], `peakform-sets-${stamp()}.csv`, { type: 'text/csv' }),
    new File([toCsv(food, ['date', 'slot', 'time', 'source', 'food', 'method', 'grams_low', 'grams_mid', 'grams_high', 'kcal_low', 'kcal_mid', 'kcal_high', 'protein_mid'])], `peakform-food-${stamp()}.csv`, { type: 'text/csv' }),
    new File([toCsv([...body, ...(t.waist ?? []).map((w) => ({ date: w.date, waistCm: w.cm }))], ['date', 'weightKg', 'bodyFatPct', 'waistCm', 'standardConditions', 'energy', 'mood', 'concentration', 'illness'])], `peakform-body-${stamp()}.csv`, { type: 'text/csv' }),
  ];
  return { files, title: 'PeakForm CSV export', record: { kind: 'csv', checksum: '', counts: { sets: sets.length, food: food.length, body: body.length }, note: 'CSV export' } };
}

export type ParsedImport = { preview: ImportPreview; encrypted: boolean };

export async function prepareImport(text: string, passphrase: string | null): Promise<ParsedImport> {
  const parsed = detectFile(text);
  let file: BackupFile;
  if (parsed.kind === 'encrypted') {
    if (!passphrase) throw new Error('This backup is encrypted. Enter its passphrase.');
    const inner = await decryptBackup(parsed.file, passphrase);
    const again = detectFile(JSON.stringify(inner));
    if (again.kind !== 'plain') throw new Error('The decrypted file is not a PeakForm backup.');
    file = again.file;
  } else file = parsed.file;
  const preview = await buildPreview(file, await readAllTables(), parsed.kind);
  return { preview, encrypted: parsed.kind === 'encrypted' };
}

export async function applyImport(preview: ImportPreview, mode: 'replace' | ConflictChoice): Promise<string> {
  const snap = await snapshotBeforeImport(`Before import of backup from ${preview.exportedAt}`);
  try {
    if (mode === 'replace') await writeAllTables(preview.data, 'replace');
    else await writeAllTables(mergeTables(await readAllTables(), preview.data, mode), 'replace');
    const t = Date.now();
    await db.migrations.put({ id: uid('mig'), createdAt: t, updatedAt: t, fromVersion: preview.schemaVersion, toVersion: 1, appliedAt: t, note: `Imported backup (${mode}).` });
  } catch (e) {
    await restoreSnapshot(snap);
    throw e;
  }
  return snap;
}

// ---------- Calendar ----------

export async function prepareCalendar(settings: AppSettings): Promise<{ file: File; events: number; excluded: number; until: string }> {
  const prior = await db.calendarExports.count();
  const r = buildIcs(settings, { today: dateKey(), weeks: 26, now: Date.now(), sequence: prior + 1, calName: settings.appName });
  const file = new File([r.text], 'peakform-reminders.ics', { type: 'text/calendar' });
  return { file, events: r.eventCount, excluded: r.excludedCount, until: r.untilDate };
}

export async function recordCalendarExport(settings: AppSettings, events: number, until: string): Promise<void> {
  const t = Date.now();
  await db.calendarExports.put({ id: uid('cal'), createdAt: t, updatedAt: t, eventCount: events, reminderHash: reminderHash(settings), untilDate: until });
}

export type { TableData };

/** One line per day with each session's location, for reports and the plan export. */
export function weekLines(plan: Pick<PlanRecord, 'days'>): string[] {
  return [...plan.days]
    .sort((a, b) => a.weekday - b.weekday)
    .map((d) => {
      if (d.isRest || d.items.length === 0) return `${WEEKDAY_NAMES[d.weekday]}: ${d.isRest ? d.title : 'nothing planned'}`;
      const sessions = [...new Set(d.items.map((i) => i.session))].map((s) => {
        const loc = s === 'main' ? LOCATION_LABEL.gym : s === 'swim' ? LOCATION_LABEL.pool : LOCATION_LABEL.home;
        const names = d.items.filter((i) => i.session === s).map((i) => exerciseName(i.exerciseId));
        return `${SESSION_LABELS[s]} (${loc}): ${names.join(', ')}`;
      });
      return `${WEEKDAY_NAMES[d.weekday]}, ${d.title}. ${sessions.join('. ')}`;
    });
}

export function reportContext(plan: PlanRecord, athlete: Awaited<ReturnType<typeof getAthlete>>): ReportContext {
  return { athlete, week: weekLines(plan), planVersion: `${plan.name}, version ${plan.version}` };
}

/** The plan, session details, and example meals as a private Markdown file. */
export async function preparePlanExport(mealOpts: import('../content/meals').DayOptions): Promise<PreparedExport> {
  const settings = await db.settings.get('app');
  const plan = settings ? await db.plans.get(settings.activePlanId) : undefined;
  if (!plan) throw new Error('No plan found.');
  const { planMarkdown } = await import('../domain/planExport');
  const md = planMarkdown(plan, await getAthlete(), mealOpts, settings?.appName);
  return { files: [new File([md], `peakform-plan-${stamp()}.md`, { type: 'text/markdown' })], title: 'PeakForm plan' };
}
