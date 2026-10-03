import type { ActivityKind } from '../content/types';
import type { WorkSet } from './progression';

// Every fourth completed exposure to an exercise, look back at the last four and give a
// careful recommendation. Four sessions is a small sample, so the text never claims a cause.

export interface Exposure {
  sessionId: string;
  date: string;
  sets: WorkSet[];
  /** Extra measures for quality based work. */
  reachCm?: number | null;
  timeSec?: number | null;
  sleepHours?: number | null;
  soreness?: number | null;
  plannedSets: number;
}

export type FourRecommendation = 'progress' | 'hold' | 'reduce' | 'change_technique' | 'coach_review';

export interface FourExposureResult {
  due: boolean;
  exposureNumber: number;
  recommendation: FourRecommendation;
  summary: string;
  details: string[];
  best: string;
  current: string;
}

export const REVIEW_EVERY = 4;

export function isReviewDue(completedExposures: number): boolean {
  return completedExposures > 0 && completedExposures % REVIEW_EVERY === 0;
}

function load(e: Exposure): number {
  const w = e.sets.map((s) => s.weightKg).filter((x): x is number => x !== null);
  return w.length ? Math.min(...w) : 0;
}
const totalReps = (e: Exposure) => e.sets.reduce((a, s) => a + (s.reps ?? 0), 0);
const avg = (xs: number[]) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : null);
const avgRir = (e: Exposure) => avg(e.sets.map((s) => s.rir).filter((x): x is number => x !== null));
const avgQuality = (e: Exposure) => avg(e.sets.map((s) => s.quality).filter((x): x is number => x !== null && x !== undefined));
const painSets = (e: Exposure) => e.sets.filter((s) => s.pain !== 'none' || (s.painScore ?? 0) > 0).length;
const maxPain = (e: Exposure) => Math.max(0, ...e.sets.map((s) => s.painScore ?? (s.pain === 'stop' ? 5 : s.pain === 'mild' ? 2 : 0)));
const poorForm = (e: Exposure) => e.sets.filter((s) => s.form === 'poor' || s.landing === 'poor').length;

function describeLoaded(e: Exposure): string {
  const l = load(e);
  const reps = e.sets.map((s) => s.reps ?? 0).join(', ');
  return l > 0 ? `${l} kg for ${reps}` : `${reps} reps`;
}

export function fourExposureReview(kind: ActivityKind, exposures: Exposure[], totalExposures: number, targetRir: number | null): FourExposureResult {
  const last = exposures.slice(-REVIEW_EVERY);
  const due = isReviewDue(totalExposures) && last.length === REVIEW_EVERY;
  const first = last[0];
  const cur = last[last.length - 1];
  const empty: FourExposureResult = { due, exposureNumber: totalExposures, recommendation: 'hold', summary: 'Not enough sessions yet.', details: [], best: '', current: '' };
  if (!first || !cur) return empty;

  const details: string[] = [];
  const pains = last.map(painSets);
  const maxPains = last.map(maxPain);
  const sleep = avg(last.map((e) => e.sleepHours).filter((x): x is number => x !== null && x !== undefined));
  const soreness = avg(last.map((e) => e.soreness).filter((x): x is number => x !== null && x !== undefined));
  const adherence = last.reduce((a, e) => a + Math.min(e.sets.length, e.plannedSets), 0) / last.reduce((a, e) => a + e.plannedSets, 0);

  if (pains.some((p) => p > 0)) details.push(`Pain was logged in ${pains.filter((p) => p > 0).length} of the last 4 sessions, highest ${Math.max(...maxPains)} out of 10.`);
  if (sleep !== null) details.push(`Average sleep before these sessions was ${sleep.toFixed(1)} hours.`);
  if (soreness !== null) details.push(`Average soreness was ${soreness.toFixed(1)} out of 3.`);
  details.push(`${Math.round(adherence * 100)} percent of planned work sets were completed.`);

  const qualityKinds: ActivityKind[] = ['jump', 'sprint', 'skill', 'throw'];
  let recommendation: FourRecommendation;
  let summary: string;
  let best = '';
  let current = '';

  if (Math.max(...maxPains) >= 4 || (maxPains[3] ?? 0) > (maxPains[0] ?? 0)) {
    recommendation = 'coach_review';
    summary = 'Pain is present or rising. Pause progression and ask a parent, coach, or clinician to take a look.';
  } else if (qualityKinds.includes(kind)) {
    const q = last.map(avgQuality);
    const reach = last.map((e) => e.reachCm ?? null);
    const time = last.map((e) => e.timeSec ?? null);
    const qFirst = q[0] ?? null;
    const qLast = q[3] ?? null;
    best = `Best quality ${Math.max(...q.filter((x): x is number => x !== null), 0).toFixed(1)} out of 5`;
    current = qLast !== null ? `Latest quality ${qLast.toFixed(1)} out of 5` : 'No quality ratings logged';
    const reachUp = reach[0] !== null && reach[3] !== null && (reach[3] ?? 0) > (reach[0] ?? 0);
    const timeDown = time[0] !== null && time[3] !== null && (time[3] ?? 0) < (time[0] ?? 0);
    if (last.some((e) => poorForm(e) > 0)) {
      recommendation = 'change_technique';
      summary = 'Some landings or reps were rated poor. Work on technique before anything else.';
    } else if (qFirst !== null && qLast !== null && qLast >= qFirst && !reachUp && !timeDown) {
      recommendation = 'coach_review';
      summary = 'Quality is stable, but height or speed has not clearly improved. Ask your coach to look at approach, arm swing, or sprint mechanics. Volume stays the same.';
    } else {
      recommendation = 'hold';
      summary = 'Keep the same volume and keep chasing quality. Volume never increases automatically.';
    }
  } else {
    const loads = last.map(load);
    const reps = last.map(totalReps);
    const bestIdx = last.reduce((bi, e, i) => {
      const b = last[bi]!;
      return load(e) > load(b) || (load(e) === load(b) && totalReps(e) > totalReps(b)) ? i : bi;
    }, 0);
    best = describeLoaded(last[bestIdx]!);
    current = describeLoaded(cur);
    const loadUp = (loads[3] ?? 0) > (loads[0] ?? 0);
    const repsUp = (loads[3] ?? 0) === (loads[0] ?? 0) && (reps[3] ?? 0) > (reps[0] ?? 0);
    const declining = (loads[3] ?? 0) < (loads[0] ?? 0) || ((loads[3] ?? 0) === (loads[0] ?? 0) && (reps[3] ?? 0) < (reps[0] ?? 0));
    const rirFirst = avgRir(first);
    const rirLast = avgRir(cur);
    if (rirFirst !== null && rirLast !== null) details.push(`Reps in reserve went from about ${rirFirst.toFixed(1)} to ${rirLast.toFixed(1)}${targetRir !== null ? `, target ${targetRir}` : ''}.`);
    const formIssues = last.filter((e) => poorForm(e) > 0).length;
    if (formIssues > 0) details.push(`Form was rated poor in ${formIssues} of the last 4 sessions.`);
    if (formIssues >= 2) {
      recommendation = 'change_technique';
      summary = 'Form was poor more than once. Work on technique at the same load, ideally with a coach.';
    } else if (loadUp || repsUp) {
      recommendation = 'progress';
      summary = 'Load or reps have gone up over the last four sessions. Keep following double progression.';
    } else if (declining) {
      recommendation = 'reduce';
      summary = 'Performance is lower than four sessions ago. Consider a slightly lighter load or a reduced week, and check sleep, soreness, and stress.';
    } else {
      recommendation = 'hold';
      summary = 'Progress is flat. Before adding volume or load, check form, how many sets were completed, sleep, pain, and fatigue.';
    }
  }
  details.push('Four sessions is a small sample, so treat this as a prompt to look closer, not a verdict.');
  return { due, exposureNumber: totalExposures, recommendation, summary, details, best, current };
}
