import { BASELINE_PLAN, type PlanItem } from '../content/plan';
import type { AppSettings, PlanRecord, Reminder } from '../db/records';
import { KV, kvGet, kvSet, savePlanVersion, updateSettings } from '../db/repo';

// Plan additions that ship after someone has already installed PeakForm. Their plan lives on the
// phone, so an update is offered once, applied as a new plan version, and never touches history.

export const MORNING_UPDATE_ID = 'morning-volleyball-v1';

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

export async function morningUpdateState(): Promise<'applied' | 'dismissed' | null> {
  const st = (await kvGet<UpdateState>(KV.planUpdates)) ?? {};
  return st[MORNING_UPDATE_ID] ?? null;
}

async function mark(value: 'applied' | 'dismissed') {
  const st = (await kvGet<UpdateState>(KV.planUpdates)) ?? {};
  await kvSet(KV.planUpdates, { ...st, [MORNING_UPDATE_ID]: value });
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

export async function applyMorningUpdate(active: PlanRecord): Promise<PlanRecord> {
  const rec = await savePlanVersion(withMorningItems(active), 'Added the 05:30 morning volleyball sessions, Sunday to Friday.');
  await updateSettings((s) => withMorningTimes(s));
  await mark('applied');
  return rec;
}

export function dismissMorningUpdate(): Promise<void> {
  return mark('dismissed');
}
