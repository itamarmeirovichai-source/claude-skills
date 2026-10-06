import { GLOBAL_RULES, planDaysFor, type PlanDay } from '../content/plan';
import { EXERCISE_BY_ID } from '../content/library';
import { defaultPicks, normalizePicks, type ProgramPicks } from '../content/program';
import type { JumpLevel } from '../content/homeSessions';
import { DEFAULT_HOME_TIMES } from '../domain/defaults';
import { diffPlans, type DayDiff } from '../domain/planDiff';
import type { AthleteProfile } from '../domain/athlete';
import type { AppSettings, PlanRecord, Reminder } from '../db/records';
import { KV, activePlan, getAthlete, getSettings, kvDelete, kvGet, kvSet, savePlanVersion, updateSettings } from '../db/repo';

// Plan changes for an app that is already installed. The plan lives on the phone, so every change
// is prepared as a proposal, shown as a summary and a day by day difference, and applied only when
// the athlete activates it. It becomes a new plan version, so finished sessions keep pointing at the
// prescription they were done against.

/** The home and gym week with no early mornings (3.0.0). */
export const V3_UPDATE_ID = 'home-gym-v3';

type UpdateState = Record<string, 'applied' | 'dismissed'>;

export async function updateState(id: string): Promise<'applied' | 'dismissed' | null> {
  const st = (await kvGet<UpdateState>(KV.planUpdates)) ?? {};
  return st[id] ?? null;
}

async function mark(id: string, value: 'applied' | 'dismissed') {
  const st = (await kvGet<UpdateState>(KV.planUpdates)) ?? {};
  await kvSet(KV.planUpdates, { ...st, [id]: value });
}

// ---------- Choices ----------

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

export async function jumpLevel(): Promise<JumpLevel> {
  return (await kvGet<JumpLevel>(KV.jumpLevel)) === 'build' ? 'build' : 'intro';
}

// ---------- Building a plan ----------

/**
 * The week rebuilt from the choices, the athlete profile, and the jump level. Exercises the athlete
 * created stay on their day. Morning sessions and swims from older versions are not carried over.
 */
export function buildPlan(active: PlanRecord, picks: ProgramPicks, athlete: Pick<AthleteProfile, 'home' | 'wrist'>, level: JumpLevel): PlanRecord {
  const next = structuredClone(active);
  const built = planDaysFor(picks, { home: athlete.home, wrist: athlete.wrist.status, jumpLevel: level });
  next.days = built.map((day): PlanDay => {
    const mine = active.days.find((d) => d.weekday === day.weekday);
    const own = (mine?.items ?? []).filter((i) => (i.session === 'main' || i.session === 'home') && !EXERCISE_BY_ID[i.exerciseId]);
    return own.length ? { ...day, isRest: false, items: [...day.items, ...own] } : day;
  });
  next.globalRules = [...GLOBAL_RULES];
  return next;
}

// ---------- Settings for the 3.0 week ----------

/** Moves the old early morning defaults to the 3.0 schedule. Times the user changed are left alone. */
export function withV3Times(s: AppSettings): { settings: AppSettings; changes: string[] } {
  const next = structuredClone(s);
  const changes: string[] = [];
  if (!next.sessionTimes.home) {
    next.sessionTimes.home = { ...DEFAULT_HOME_TIMES };
    changes.push('Home jumps on Monday and Thursday at 16:15, and the skill session on Friday at 13:30.');
  }
  for (const d of ['1', '4']) {
    if (next.sessionTimes.main[d] === '16:30') {
      next.sessionTimes.main[d] = '17:00';
      changes.push(`The ${d === '1' ? 'Monday' : 'Thursday'} gym session moves from 16:30 to 17:00, after the home jumps.`);
    }
  }
  const r = (id: string) => next.reminders.find((x) => x.id === id);
  const morning = r('morning');
  if (morning?.enabled) {
    morning.enabled = false;
    changes.push('The 05:25 morning session reminder is switched off. There is no early morning training any more.');
  }
  const move = (id: string, from: string, to: string, text: string) => {
    const x = r(id);
    if (x && x.time === from) {
      x.time = to;
      changes.push(text);
    }
  };
  move('checkin', '05:15', '07:00', 'The morning check in moves from 05:15 to 07:00.');
  move('winddown', '20:45', '21:30', 'Wind down moves from 20:45 to 21:30.');
  move('dinner', '18:45', '19:00', 'Dinner moves from 18:45 to 19:00.');
  move('milk', '20:30', '20:45', 'The evening snack moves from 20:30 to 20:45.');
  const relabel = (id: string, from: string, to: string) => {
    const x = r(id);
    if (x && x.label === from) x.label = to;
  };
  relabel('preworkout', 'Pre workout meal', 'Afternoon meal');
  relabel('milk', 'Evening milk', 'Evening snack');
  relabel('training', 'Get ready for training', 'Get ready for the gym');
  relabel('dinner', 'Dinner after training', 'Dinner');
  const training = r('training');
  if (training && training.weekdays.length === 6) {
    training.weekdays = [0, 3];
    changes.push('The gym reminder is on Sunday and Wednesday. Monday and Thursday have the home jumps reminder first.');
  }
  if (!r('home')) {
    const home: Reminder = { id: 'home', label: 'Home jumps', time: '16:05', weekdays: [1, 4], enabled: true, kind: 'training' };
    next.reminders.splice(Math.max(0, next.reminders.findIndex((x) => x.id === 'training')), 0, home);
  }
  return { settings: next, changes };
}

// ---------- Proposals ----------

export type ProposalKind = 'v3' | 'choices' | 'profile' | 'jump-level' | 'edit';

export interface PlanProposal {
  kind: ProposalKind;
  createdAt: number;
  title: string;
  reason: string;
  summary: string[];
  /** Schedule and reminder changes that come with it. */
  settingsChanges: string[];
  plan: PlanRecord;
  picks: ProgramPicks;
  jumpLevel: JumpLevel;
}

const V3_SUMMARY = [
  'Four gym strength days: Upper A on Sunday, Lower A on Monday, Upper B on Wednesday, Lower B on Thursday. Every muscle is still trained twice a week.',
  'Jumps, landings, and footwork move home: Monday and Thursday before the gym, about 60 landings, fitted to your space. Friday is a light skill session at home without jumps.',
  'Tuesday and Saturday have no structured training. School sport counts as training.',
  'No early morning sessions, so 8 to 10 hours of sleep fit.',
  'Work sets stop about two reps short of failure. No routine sets to failure.',
  'While the wrist is not cleared, gripping and pressing loads stay the same and there is no ball contact.',
  'Your exercise choices are kept. Your history is kept, because the new plan is a new version.',
];

/** Prepares a proposal and stores it until it is activated or discarded. Nothing changes yet. */
export async function proposePlan(kind: ProposalKind, opts: { picks?: ProgramPicks; level?: JumpLevel } = {}): Promise<PlanProposal> {
  const [active, athlete, settings, saved, level] = await Promise.all([activePlan(), getAthlete(), getSettings(), savedPicks(), jumpLevel()]);
  const picks = normalizePicks(opts.picks ?? saved ?? defaultPicks());
  const lvl = opts.level ?? level;
  const plan = buildPlan(active, picks, athlete, lvl);
  const settingsChanges = kind === 'v3' ? withV3Times(settings).changes : [];
  const titles: Record<ProposalKind, [string, string]> = {
    v3: ['The home and gym week', 'Gym days for strength, home sessions for jumps and skills, more recovery, and no early mornings.'],
    choices: ['Your exercise choices', 'The gym sessions rebuilt from the exercises you picked.'],
    profile: ['Fitted to your answers', 'Home drills fitted to your space, and gym exercises fitted to the wrist status you entered.'],
    'jump-level': [lvl === 'build' ? 'The next jump level' : 'Back to the starting jump level', lvl === 'build' ? 'About 95 landings per home jump session instead of about 60, chosen after a review.' : 'About 60 landings per home jump session.'],
    edit: ['Your edits', 'Changes made in the plan editor.'],
  };
  const proposal: PlanProposal = { kind, createdAt: Date.now(), title: titles[kind][0], reason: titles[kind][1], summary: kind === 'v3' ? V3_SUMMARY : [], settingsChanges, plan, picks, jumpLevel: lvl };
  await kvSet(KV.planProposal, proposal);
  return proposal;
}

/** A plan edited by hand, or an earlier version to go back to, offered with the same preview. */
export async function proposeExact(plan: PlanRecord, title: string, reason: string): Promise<PlanProposal> {
  const [saved, level] = await Promise.all([savedPicks(), jumpLevel()]);
  const proposal: PlanProposal = { kind: 'edit', createdAt: Date.now(), title, reason, summary: [], settingsChanges: [], plan: structuredClone(plan), picks: normalizePicks(saved ?? defaultPicks()), jumpLevel: level };
  await kvSet(KV.planProposal, proposal);
  return proposal;
}

export async function currentProposal(): Promise<PlanProposal | null> {
  return (await kvGet<PlanProposal>(KV.planProposal)) ?? null;
}

export function proposalDiff(active: PlanRecord, proposal: PlanProposal): DayDiff[] {
  return diffPlans(active, proposal.plan);
}

/** Saves the proposal as a new plan version, with its schedule changes. */
export async function activateProposal(): Promise<PlanRecord> {
  const p = await currentProposal();
  if (!p) throw new Error('No plan is waiting to be activated.');
  const rec = await savePlanVersion(p.plan, `${p.title}. ${p.reason}`.slice(0, 300));
  if (p.kind === 'v3') await updateSettings((s) => withV3Times(s).settings);
  await kvSet(KV.programPicks, p.picks);
  await kvSet(KV.jumpLevel, p.jumpLevel);
  await kvDelete(KV.programDraft);
  await kvDelete(KV.planProposal);
  await kvDelete(KV.phaseNotice);
  if (p.kind === 'v3') await mark(V3_UPDATE_ID, 'applied');
  return rec;
}

export async function discardProposal(): Promise<void> {
  const p = await currentProposal();
  await kvDelete(KV.planProposal);
  if (p?.kind === 'v3') await mark(V3_UPDATE_ID, 'dismissed');
}

// ---------- Offering ----------

export interface PendingUpdates {
  v3: boolean;
}

/** Whether the 3.0 week should be offered. With includeDismissed, an offer put off with "Not now" is shown again. */
export async function pendingUpdates(opts: { includeDismissed?: boolean } = {}): Promise<PendingUpdates | null> {
  const [st, active] = await Promise.all([updateState(V3_UPDATE_ID), activePlan()]);
  if (st === 'applied') return null;
  if (st === 'dismissed' && !opts.includeDismissed) return null;
  const builtForV3 = active.days.some((d) => d.items.some((i) => i.session === 'home'));
  return builtForV3 ? null : { v3: true };
}

export function dismissPlanUpdates(): Promise<void> {
  return mark(V3_UPDATE_ID, 'dismissed');
}
