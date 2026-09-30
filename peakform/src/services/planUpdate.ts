import { BASELINE_PLAN, type PlanItem } from '../content/plan';
import { BASELINE_TARGETS, type NutritionTarget } from '../content/meals';
import type { AppSettings, PlanRecord, Reminder } from '../db/records';
import { KV, getTargets, kvGet, kvSet, saveTargets, savePlanVersion, updateSettings } from '../db/repo';

// Plan additions that ship after someone has already installed PeakForm. Their plan lives on the
// phone, so an update is offered once, applied as a new plan version, and never touches history.

export const MORNING_UPDATE_ID = 'morning-volleyball-v1';
export const GYM_DAYS_UPDATE_ID = 'gym-days-v1';

type UpdateId = typeof MORNING_UPDATE_ID | typeof GYM_DAYS_UPDATE_ID;
type UpdateState = Record<string, 'applied' | 'dismissed'>;

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

export async function updateState(id: UpdateId): Promise<'applied' | 'dismissed' | null> {
  const st = (await kvGet<UpdateState>(KV.planUpdates)) ?? {};
  return st[id] ?? null;
}

async function mark(ids: UpdateId[], value: 'applied' | 'dismissed') {
  const st = (await kvGet<UpdateState>(KV.planUpdates)) ?? {};
  await kvSet(KV.planUpdates, { ...st, ...Object.fromEntries(ids.map((id) => [id, value])) });
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

// ---------- Tuesday and Friday become gym days (1.2.0) ----------

/** Main session item IDs of the old Tuesday and Friday volleyball days. Only these are replaced. */
export const OLD_VOLLEYBALL_MAIN_IDS: Record<number, string[]> = {
  2: ['tue-1-dynamic-volleyball-warm-up', 'tue-2-volleyball-approach-footwork', 'tue-3-shuffle-to-sprint', 'tue-4-medicine-ball-spike-throw', 'tue-5-volleyball-spike', 'tue-6-cable-external-rotation', 'tue-7-face-pull'],
  5: [
    'fri-1-dynamic-volleyball-warm-up',
    'fri-2-volleyball-approach-footwork',
    'fri-3-volleyball-approach-jump',
    'fri-4-lateral-block-jump',
    'fri-5-block-to-spike-transition',
    'fri-6-ten-metre-sprint',
    'fri-7-shuffle-to-sprint',
    'fri-8-medicine-ball-spike-throw',
    'fri-9-volleyball-spike',
    'fri-10-nordic-hamstring-curl',
  ],
};
const OLD_TARGET_LABELS: Record<number, string> = { 2: 'Volleyball and shoulder care', 5: 'Speed, spike, and swim' };
const GYM_DAYS = [2, 5];

/** Weekdays whose main session still lacks the new gym work. Days made into rest days are left alone. */
export function gymDaysPending(active: PlanRecord): number[] {
  return GYM_DAYS.filter((weekday) => {
    const mine = active.days.find((d) => d.weekday === weekday);
    if (!mine || mine.isRest) return false;
    const have = new Set(mine.items.map((i) => i.id));
    return BASELINE_PLAN.days.find((d) => d.weekday === weekday)!.items.some((i) => i.session === 'main' && !have.has(i.id));
  });
}

/** Swaps the old volleyball main sessions for the new gym sessions. Morning work, the swim, and items the user added stay. */
export function withGymDays(active: PlanRecord): PlanRecord {
  const pending = new Set(gymDaysPending(active));
  const next = structuredClone(active);
  for (const day of next.days) {
    if (!pending.has(day.weekday)) continue;
    const base = BASELINE_PLAN.days.find((d) => d.weekday === day.weekday)!;
    const old = new Set(OLD_VOLLEYBALL_MAIN_IDS[day.weekday] ?? []);
    const have = new Set(day.items.map((i) => i.id));
    const kept = day.items.filter((i) => i.session === 'main' && !old.has(i.id));
    const add = base.items.filter((i) => i.session === 'main' && !have.has(i.id));
    day.items = [...day.items.filter((i) => i.session === 'morning'), ...add, ...kept, ...day.items.filter((i) => i.session === 'swim')];
    day.title = base.title;
    day.short = base.short;
  }
  return next;
}

/** Renames the Tuesday and Friday food targets when they still carry the old default labels. Numbers stay. */
export function withGymDayTargets(targets: NutritionTarget[]): NutritionTarget[] {
  return targets.map((t) => (OLD_TARGET_LABELS[t.weekday] === t.label ? { ...t, label: BASELINE_TARGETS.find((b) => b.weekday === t.weekday)!.label } : t));
}

// ---------- Offering and applying ----------

export interface PendingUpdates {
  morning: number;
  gymDays: number[];
}

/**
 * What the plan update card should offer, or null when nothing is waiting. With includeDismissed,
 * an update the user put off with "Not now" is offered again, as long as the plan still lacks it.
 */
export async function pendingUpdates(active: PlanRecord, opts: { includeDismissed?: boolean } = {}): Promise<PendingUpdates | null> {
  const skip = async (id: UpdateId) => {
    const st = await updateState(id);
    return st === 'applied' || (st === 'dismissed' && !opts.includeDismissed);
  };
  const morning = (await skip(MORNING_UPDATE_ID)) ? 0 : missingMorningItems(active).size;
  const gymDays = (await skip(GYM_DAYS_UPDATE_ID)) ? [] : gymDaysPending(active);
  return morning || gymDays.length ? { morning, gymDays } : null;
}

function offeredIds(p: PendingUpdates): UpdateId[] {
  return [...(p.morning ? [MORNING_UPDATE_ID] : []), ...(p.gymDays.length ? [GYM_DAYS_UPDATE_ID] : [])] as UpdateId[];
}

/** Applies every offered update as one new plan version. History is never changed. */
export async function applyPlanUpdates(active: PlanRecord, p: PendingUpdates): Promise<PlanRecord> {
  let plan = active;
  const notes: string[] = [];
  if (p.morning) {
    plan = withMorningItems(plan);
    notes.push('Added the 05:30 morning volleyball sessions, Sunday to Friday.');
  }
  if (p.gymDays.length) {
    plan = withGymDays(plan);
    notes.push('Tuesday and Friday are now gym days: Upper C and Lower C.');
  }
  const rec = await savePlanVersion(plan, notes.join(' '));
  if (p.morning) await updateSettings((s) => withMorningTimes(s));
  if (p.gymDays.length) await saveTargets(withGymDayTargets(await getTargets()));
  await mark(offeredIds(p), 'applied');
  return rec;
}

export function dismissPlanUpdates(p: PendingUpdates): Promise<void> {
  return mark(offeredIds(p), 'dismissed');
}
