import type { AppSettings, BodyCheckIn, FoodLog, WorkoutSession } from '../db/records';
import { templatesForDay, SLOT_LABELS, type MealTemplate } from '../content/meals';
import { SESSION_LABELS, type PlanDay, type SessionKey } from '../content/plan';
import { minutesOf, weekdayOf, type DateKey } from '../domain/dates';
import { isSabbathTime } from '../domain/sabbath';
import { sessionTime } from './training';

export type TimelineKind = 'checkin' | 'meal' | 'session' | 'sleep';

export interface TimelineEntry {
  id: string;
  time: string;
  kind: TimelineKind;
  label: string;
  detail: string;
  done: boolean;
  to: string;
  session?: SessionKey;
  template?: MealTemplate;
  quiet: boolean;
}

export function buildTimeline(date: DateKey, settings: AppSettings, day: PlanDay | undefined, food: FoodLog[], sessions: WorkoutSession[], checkins: BodyCheckIn[]): TimelineEntry[] {
  const wd = weekdayOf(date);
  const out: TimelineEntry[] = [];
  const quiet = (t: string) => isSabbathTime(date, t, settings.sabbath);
  const checkinReminder = settings.reminders.find((r) => r.id === 'checkin');
  const ct = checkinReminder?.time ?? '05:15';
  out.push({ id: 'checkin', time: ct, kind: 'checkin', label: 'Morning check in', detail: 'Weight, sleep, and how you feel', done: checkins.some((c) => c.date === date), to: '/checkin', quiet: quiet(ct) });

  if (day && !day.isRest) {
    for (const s of ['morning', 'main', 'swim'] as SessionKey[]) {
      const items = day.items.filter((i) => i.session === s);
      if (!items.length) continue;
      const t = sessionTime(settings, wd, s);
      const done = sessions.some((x) => x.session === s && x.status === 'done' && x.planWeekday === wd);
      const title = s === 'main' ? day.title : SESSION_LABELS[s];
      const detail = s === 'morning' ? morningDetail(items) : s === 'swim' ? '2 sets of 10 round trips' : `${items.length} exercises`;
      out.push({ id: `session-${s}`, time: t, kind: 'session', label: title, detail, done, to: `/train/day/${wd}?date=${date}`, session: s, quiet: quiet(t) });
    }
  }

  for (const tpl of templatesForDay(wd)) {
    const done = food.some((f) => f.date === date && (f.templateId === tpl.id || f.slot === tpl.slot));
    const reminder = settings.reminders.find((r) => r.id === tpl.slot || (tpl.slot === 'evening' && r.id === 'milk'));
    const t = reminder?.time ?? tpl.time;
    out.push({ id: `meal-${tpl.id}`, time: t, kind: 'meal', label: SLOT_LABELS[tpl.slot], detail: tpl.name, done, to: `/eat/log/${tpl.slot}?date=${date}`, template: tpl, quiet: quiet(t) });
  }
  const wind = settings.reminders.find((r) => r.id === 'winddown');
  if (wind) out.push({ id: 'sleep', time: wind.time, kind: 'sleep', label: 'Wind down', detail: `Screens away, lights low, aim for sleep near ${bedtimeFor(settings.sessionTimes.morning)}`, done: false, to: '/today', quiet: quiet(wind.time) });
  return out.sort((a, b) => minutesOf(a.time) - minutesOf(b.time));
}

/** The next thing to do: the first entry not done whose time has come, or the next upcoming one. */
export function nextEntry(entries: TimelineEntry[], nowMinutes: number): TimelineEntry | null {
  const open = entries.filter((e) => !e.done && e.kind !== 'sleep' && !e.quiet);
  const due = open.filter((e) => minutesOf(e.time) <= nowMinutes + 30);
  if (due.length) return due[due.length - 1]!;
  return open[0] ?? null;
}

function morningDetail(items: PlanDay['items']): string {
  const rope = items.find((i) => i.target.type === 'duration');
  const mins = rope && rope.target.type === 'duration' ? `${rope.target.totalMin} minutes easy rope` : '';
  const others = items.length - (rope ? 1 : 0);
  if (!others) return mins;
  return `${mins}${mins ? ', then ' : ''}${others} volleyball and shoulder drills`;
}

/** About eight and a quarter hours before the morning session, so the teen sleep target of 8 to 10 hours still fits. */
export function bedtimeFor(morning: string): string {
  const m = (minutesOf(morning) - 8 * 60 - 15 + 24 * 60) % (24 * 60);
  return `${String(Math.floor(m / 60)).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`;
}
