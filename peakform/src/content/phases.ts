import { addDays, diffDays, type DateKey } from '../domain/dates';
import type { PlanItem } from './plan';
import { exercise } from './library';

// Four month planning (3.0.0). Phases are flexible stages with process goals and a review, counted
// from the plan start. They never change the plan by themselves: any change is offered after a
// review, shown as a visible difference, and only applied when the athlete confirms it.
// They replace the dated jump blocks of 2.1.0, which aimed at a dunk deadline.

export type PlanningPhaseId = 'assess' | 'progress' | 'consolidate' | 'review';

export interface PlanningPhase {
  id: PlanningPhaseId;
  name: string;
  /** Weeks from the plan start, inclusive. The last phase stays open until the review is done. */
  weeks: [number, number];
  focus: string;
  processGoals: string[];
  /** What the review at the end of the phase looks at before anything changes. */
  reviewChecks: string[];
}

export const PLANNING_PHASES: PlanningPhase[] = [
  {
    id: 'assess',
    name: 'Technique and workload check',
    weeks: [1, 3],
    focus: 'Learn the exercises and landings, find working loads that leave two or three reps in reserve, and see how school sport, home jumps, and the gym fit together.',
    processGoals: ['Most planned sessions done, with form logged', 'Landings rated good or OK', 'A regular meal routine, logged when it helps', '8 to 10 hours of sleep on most nights', 'Clearance for any injury and the home space confirmed'],
    reviewChecks: ['Any joint, tendon, heel, knee, back, or wrist pain', 'Soreness that lasts more than three days', 'Sleep, energy, mood, and school concentration', 'How many hours of sport and training the week really held'],
  },
  {
    id: 'progress',
    name: 'Gradual progression',
    weeks: [4, 9],
    focus: 'Add reps, then small loads, when every work set qualifies. Jump work stays at the same level unless a review shows landings, recovery, and school jumping allow more.',
    processGoals: ['Comparable sets improve at the same reps in reserve', 'No progression through pain', 'Regular meals and enough sleep', 'A jump measurement every four weeks under the same conditions'],
    reviewChecks: ['Strength trends on the main exercises', 'Jump measurements compared under the same conditions', 'Recovery between sessions', 'Whether the next jump level is appropriate'],
  },
  {
    id: 'consolidate',
    name: 'Consolidation and skill',
    weeks: [10, 15],
    focus: 'Keep the strength work steady, spend more of the home time on approach rhythm, arm swing, and accuracy, and take a lighter week when fatigue builds.',
    processGoals: ['Consistent training weeks', 'Approach footwork that looks the same every rep', 'Coach feedback on the spike approach', 'Recovery and sleep held up through the school term'],
    reviewChecks: ['Skill notes from a coach', 'Jump measurements and landing quality', 'Any recurring pain', 'Weight trend only if weighing is on, and never on its own'],
  },
  {
    id: 'review',
    name: 'Review and the next block',
    weeks: [16, 18],
    focus: 'Look back over the four months with a parent and, ideally, a coach and a pediatric professional. Plan the next block from what the measurements, recovery, and wellbeing showed.',
    processGoals: ['A coach report shared with the people helping you', 'Professional review of goals and targets', 'A plan for the next block'],
    reviewChecks: ['Measured outcomes next to the process goals', 'Aspirations reviewed with a professional', 'What to keep, change, or stop'],
  },
];

export function weekOfPlan(planStart: DateKey, today: DateKey): number {
  return Math.floor(diffDays(today, planStart) / 7) + 1;
}

/** The planning phase for a date, or null before the plan starts. After the last phase the review stays current. */
export function planningPhaseFor(planStart: DateKey | null, today: DateKey): PlanningPhase | null {
  if (!planStart || today < planStart) return null;
  const week = weekOfPlan(planStart, today);
  return PLANNING_PHASES.find((p) => week >= p.weeks[0] && week <= p.weeks[1]) ?? PLANNING_PHASES[PLANNING_PHASES.length - 1]!;
}

/** Jump and reach measurements every four weeks from the plan start. */
export function nextMeasurementDate(planStart: DateKey | null, today: DateKey): DateKey | null {
  if (!planStart) return null;
  if (today <= planStart) return planStart;
  const weeks = Math.ceil(diffDays(today, planStart) / 28);
  return addDays(planStart, weeks * 28);
}

/** Foot contacts in a list of plan items. A per side drill counts both legs. */
export function contacts(items: PlanItem[]): number {
  return items.reduce((n, i) => {
    if (exercise(i.exerciseId)?.kind !== 'jump' || i.target.type !== 'reps') return n;
    return n + i.sets * i.target.max * (i.per === 'side' ? 2 : 1);
  }, 0);
}
