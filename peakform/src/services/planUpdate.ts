import { BASELINE_PLAN, GLOBAL_RULES, planDaysFor, type PlanItem } from '../content/plan';
import { BASELINE_TARGETS, type NutritionTarget } from '../content/meals';
import { EXERCISE_BY_ID } from '../content/library';
import { defaultPicks, normalizePicks, type ProgramPicks } from '../content/program';
import { PHASES, phaseFor, type PhaseId, type ProgramPhase } from '../content/phases';
import { dateKey, type DateKey } from '../domain/dates';
import type { AppSettings, PlanRecord, Reminder } from '../db/records';
import { KV, activePlan, getTargets, kvDelete, kvGet, kvSet, saveTargets, savePlanVersion, updateSettings } from '../db/repo';

// Plan changes that ship after someone has already installed PeakForm. Their plan lives on the
// phone, so a change is offered, applied as a new plan version, and never touches history.

export const MORNING_UPDATE_ID = 'morning-volleyball-v1';
/** The head by head program with the exercise questionnaire (2.0.0). Replaces the 1.2 gym day update. */
export const PROGRAM_UPDATE_ID = 'program-v2';
/** The jump program for the dunk goal, in training blocks (2.1.0). */
export const DUNK_UPDATE_ID = 'dunk-v1';

type UpdateId = typeof MORNING_UPDATE_ID | typeof PROGRAM_UPDATE_ID | typeof DUNK_UPDATE_ID;
type UpdateState = Record<string, 'applied' | 'dismissed'>;

export async function updateState(id: UpdateId): Promise<'applied' | 'dismissed' | null> {
  const st = (await kvGet<UpdateState>(KV.planUpdates)) ?? {};
  return st[id] ?? null;
}

async function mark(ids: UpdateId[], value: 'applied' | 'dismissed') {
  const st = (await kvGet<UpdateState>(KV.planUpdates)) ?? {};
  await kvSet(KV.planUpdates, { ...st, ...Object.fromEntries(ids.map((id) => [id, value])) });
}

// ---------- Morning sessions (1.1.0) ----------

/** Morning items in the current baseline that the active plan does not have yet, by weekday. */
export function missingMorningItems(active: PlanRecord): Map<number, PlanItem[]> {
  const out = new Map<number, PlanItem[]>();
  for (const day of BASELINE_PLAN.days) {
    const mine = active.days.find((d) => d.weekday === day.weekday);
    if (!mine || mine.isRest) continue;
    const have = new Set(mine.items.map((i) => i.id));
    const add = day.items.filter((i) => i.session === 'morning' && !have.has(i.id));
    if (add.length) out.set(day.weekday, add);
  }
  return out;
}

export function withMorningItems(active: PlanRecord): PlanRecord {
  const missing = missingMorningItems(active);
  const next = structuredClone(active);
  for (const day of next.days) {
    const add = missing.get(day.weekday);
    if (!add) continue;
    const morning = day.items.filter((i) => i.session === 'morning');
    const rest = day.items.filter((i) => i.session !== 'morning');
    // The rope stays first, as the warm up, then the new drills, then the rest of the day.
    const rope = [...morning, ...add].filter((i) => i.exerciseId === 'easy-jump-rope');
    const drills = [...morning, ...add].filter((i) => i.exerciseId !== 'easy-jump-rope');
    day.items = [...rope, ...drills, ...rest];
  }
  const rule = BASELINE_PLAN.globalRules[0]!;
  if (!next.globalRules.includes(rule)) next.globalRules = [rule, ...next.globalRules];
  return next;
}

/** Moves the old default times to the 05:30 schedule. Times the user changed are left alone. */
export function withMorningTimes(s: AppSettings): AppSettings {
  const next = structuredClone(s);
  if (next.sessionTimes.morning === '07:00') next.sessionTimes.morning = '05:30';
  const fix = (id: string, from: string, to: string) => {
    const r = next.reminders.find((x) => x.id === id);
    if (r && r.time === from) r.time = to;
  };
  fix('checkin', '07:00', '05:15');
  fix('winddown', '21:45', '20:45');
  if (!next.reminders.some((r) => r.id === 'morning')) {
    const morning: Reminder = { id: 'morning', label: 'Morning volleyball and rope', time: '05:25', weekdays: [0, 1, 2, 3, 4, 5], enabled: true, kind: 'training' };
    const at = next.reminders.findIndex((r) => r.id === 'checkin');
    next.reminders.splice(at + 1, 0, morning);
  }
  return next;
}

// ---------- The chosen program (2.0.0) ----------

export async function savedPicks(): Promise<ProgramPicks | null> {
  return (await kvGet<ProgramPicks>(KV.programPicks)) ?? null;
}

/** Choices being made in the questionnaire, kept while the user looks at an exercise and comes back. */
export async function draftPicks(): Promise<ProgramPicks> {
  return (await kvGet<ProgramPicks>(KV.programDraft)) ?? (await savedPicks()) ?? {};
}

export function saveDraftPicks(picks: ProgramPicks): Promise<void> {
  return kvSet(KV.programDraft, picks);
}

/**
 * The plan with its main sessions rebuilt from the choices. Morning sessions, swims, and
 * exercises the user created stay. The morning sessions are added only if they are missing and the
 * user never turned that update down.
 */
export function withProgram(active: PlanRecord, picks: ProgramPicks, addMorning: boolean, phase: ProgramPhase = PHASES[0]!): PlanRecord {
  const base = addMorning ? withMorningItems(active) : structuredClone(active);
  const built = planDaysFor(picks, phase);
  base.days = built.map((day) => {
    const mine = base.days.find((d) => d.weekday === day.weekday);
    if (!mine || day.isRest) return mine ?? day;
    const morning = mine.items.filter((i) => i.session === 'morning');
    const swim = mine.items.filter((i) => i.session === 'swim');
    const own = mine.items.filter((i) => i.session === 'main' && !EXERCISE_BY_ID[i.exerciseId]);
    const main = day.items.filter((i) => i.session === 'main');
    return { ...mine, title: day.title, short: day.short, isRest: false, items: [...morning, ...main, ...own, ...(swim.length ? swim : day.items.filter((i) => i.session === 'swim'))] };
  });
  const morningRule = GLOBAL_RULES[0]!;
  base.globalRules = base.globalRules.includes(morningRule) || addMorning ? [...GLOBAL_RULES] : GLOBAL_RULES.slice(1);
  return base;
}

/** Food target names that were defaults in earlier versions, renamed to match the new days. */
const OLD_TARGET_LABELS: Record<number, string[]> = { 2: ['Volleyball and shoulder care', 'Upper C'], 4: ['Upper B'], 5: ['Speed, spike, and swim'] };

export function withProgramTargetLabels(targets: NutritionTarget[]): NutritionTarget[] {
  return targets.map((t) => ((OLD_TARGET_LABELS[t.weekday] ?? []).includes(t.label) ? { ...t, label: BASELINE_TARGETS.find((b) => b.weekday === t.weekday)!.label } : t));
}

/** Saves the choices and the plan rebuilt for the current training block as a new version. */
export async function applyProgram(active: PlanRecord, picks: ProgramPicks, phase: ProgramPhase = phaseFor(dateKey())): Promise<PlanRecord> {
  const clean = normalizePicks(picks);
  const morningAnswer = await updateState(MORNING_UPDATE_ID);
  const addMorning = morningAnswer !== 'dismissed' && missingMorningItems(active).size > 0;
  const rec = await savePlanVersion(withProgram(active, clean, addMorning, phase), `Main sessions built from your exercise choices, ${phase.name}.`);
  if (addMorning) await updateSettings((s) => withMorningTimes(s));
  await saveTargets(withProgramTargetLabels(await getTargets()));
  await kvSet(KV.programPicks, clean);
  await kvSet(KV.programPhase, phase.id);
  await kvDelete(KV.programDraft);
  await kvDelete(KV.phaseNotice);
  await mark(addMorning ? [PROGRAM_UPDATE_ID, DUNK_UPDATE_ID, MORNING_UPDATE_ID] : [PROGRAM_UPDATE_ID, DUNK_UPDATE_ID], 'applied');
  return rec;
}

let syncing: Promise<ProgramPhase | null> | null = null;

/**
 * When a new training block starts, rebuilds the plan for it as a new version and leaves a notice
 * for Today. Runs only for plans built from the program, and only once per block.
 */
export function syncProgramPhase(today: DateKey = dateKey()): Promise<ProgramPhase | null> {
  syncing ??= (async () => {
    const current = await kvGet<PhaseId>(KV.programPhase);
    const phase = phaseFor(today);
    if (!current || current === phase.id) return null;
    const picks = normalizePicks((await savedPicks()) ?? defaultPicks());
    await savePlanVersion(withProgram(await activePlan(), picks, false, phase), `New training block: ${phase.name}.`);
    await kvSet(KV.programPhase, phase.id);
    await kvSet(KV.phaseNotice, phase.id);
    return phase;
  })().finally(() => {
    syncing = null;
  });
  return syncing;
}

// ---------- Offering ----------

export interface PendingUpdates {
  /** The questionnaire has not been done yet. */
  program: boolean;
  /** The choices are saved, but the plan was built before the jump program existed. */
  dunk: boolean;
}

/**
 * What the plan update card should offer, or null when nothing is waiting. With includeDismissed,
 * an offer the user put off with "Not now" is shown again.
 */
export async function pendingUpdates(opts: { includeDismissed?: boolean } = {}): Promise<PendingUpdates | null> {
  // Both reads start together so a live query sees both. A read after an await is not always tracked.
  const [picks, st, phase, dunk] = await Promise.all([savedPicks(), updateState(PROGRAM_UPDATE_ID), kvGet<PhaseId>(KV.programPhase), updateState(DUNK_UPDATE_ID)]);
  const hidden = (state: 'applied' | 'dismissed' | null) => state === 'applied' || (state === 'dismissed' && !opts.includeDismissed);
  if (!picks) return hidden(st) ? null : { program: true, dunk: false };
  if (phase || hidden(dunk)) return null;
  return { program: false, dunk: true };
}

export function dismissPlanUpdates(offer: PendingUpdates): Promise<void> {
  return mark([offer.dunk ? DUNK_UPDATE_ID : PROGRAM_UPDATE_ID], 'dismissed');
}

/** The block that just started, until Today shows it once. */
export async function phaseNotice(): Promise<ProgramPhase | null> {
  const id = await kvGet<PhaseId>(KV.phaseNotice);
  return PHASES.find((p) => p.id === id) ?? null;
}

export function dismissPhaseNotice(): Promise<void> {
  return kvDelete(KV.phaseNotice);
}
