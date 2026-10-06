import type { PlanDay, PlanItem, SessionKey } from '../content/plan';
import { SESSION_LABELS } from '../content/plan';
import { WEEKDAY_NAMES } from './dates';

// A readable difference between the active plan and a proposed one, shown before any plan is
// activated. Items are matched by exercise within the same day and session, because item IDs
// change between versions.

export interface ItemChange {
  kind: 'added' | 'removed' | 'changed';
  session: SessionKey;
  exerciseId: string;
  before: string | null;
  after: string | null;
}

export interface DayDiff {
  weekday: number;
  dayName: string;
  titleBefore: string;
  titleAfter: string;
  changes: ItemChange[];
}

export function doseText(i: PlanItem): string {
  const t = i.target;
  const per = i.per === 'side' ? ' each side' : i.per === 'direction' ? ' each way' : '';
  const base =
    t.type === 'reps' ? `${i.sets} × ${t.min === t.max ? t.min : `${t.min} to ${t.max}`}${per}` : t.type === 'hold' ? `${i.sets} × ${t.seconds} s${per}` : t.type === 'duration' ? `${t.totalMin} min` : `${i.sets} × ${t.count} round trips`;
  const rir = i.rir !== undefined ? `, ${i.rir} in reserve${i.lastSetRir !== undefined ? ` (last set ${i.lastSetRir})` : ''}` : '';
  return `${base}${rir}`;
}

const keyOf = (i: PlanItem) => `${i.session}:${i.exerciseId}`;

export function diffDay(before: PlanDay | undefined, after: PlanDay | undefined, weekday: number): DayDiff {
  const b = before?.items ?? [];
  const a = after?.items ?? [];
  const changes: ItemChange[] = [];
  const bMap = new Map<string, PlanItem[]>();
  for (const i of b) bMap.set(keyOf(i), [...(bMap.get(keyOf(i)) ?? []), i]);
  for (const i of a) {
    const list = bMap.get(keyOf(i));
    const prev = list?.shift();
    if (!prev) changes.push({ kind: 'added', session: i.session, exerciseId: i.exerciseId, before: null, after: doseText(i) });
    else if (doseText(prev) !== doseText(i) || prev.restSec !== i.restSec) changes.push({ kind: 'changed', session: i.session, exerciseId: i.exerciseId, before: doseText(prev), after: doseText(i) });
  }
  for (const list of bMap.values()) for (const i of list) changes.push({ kind: 'removed', session: i.session, exerciseId: i.exerciseId, before: doseText(i), after: null });
  return {
    weekday,
    dayName: WEEKDAY_NAMES[weekday] ?? String(weekday),
    titleBefore: before ? (before.isRest ? 'Rest' : before.title) : 'Nothing',
    titleAfter: after ? (after.isRest ? 'Rest' : after.title) : 'Nothing',
    changes,
  };
}

/** Day by day differences, Sunday first. Days without any change are left out. */
export function diffPlans(before: { days: PlanDay[] }, after: { days: PlanDay[] }): DayDiff[] {
  const out: DayDiff[] = [];
  for (let wd = 0; wd < 7; wd++) {
    const d = diffDay(
      before.days.find((x) => x.weekday === wd),
      after.days.find((x) => x.weekday === wd),
      wd,
    );
    if (d.changes.length || d.titleBefore !== d.titleAfter) out.push(d);
  }
  return out;
}

/** Sessions of a day with their labels, for the plan preview. */
export function sessionLabel(s: SessionKey): string {
  return SESSION_LABELS[s];
}
