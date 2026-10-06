import type { PlanItem, SessionKey } from '../content/plan';
import { exercise } from '../content/library';
import { HOME_NEEDS, LOCATION_LABEL, SPACE_TEXT, CEILING_TEXT, type Location } from '../content/traits';
import type { LibraryExerciseId } from '../content/exercises/ids';

// What every session needs, worked out from its exercises: where, what equipment, how much
// space, about how long, and when to stop (3.0.0).

export interface SessionInfo {
  location: Location;
  locationLabel: string;
  equipment: string[];
  space: string;
  /** Estimated minutes, rounded to 5. */
  minutes: number;
  stopRules: string[];
}

const STOP_GYM = [
  'Stop a set when the technique changes or you reach the planned reps in reserve.',
  'Stop the exercise for pain of 4 out of 10 or more, pain that gets worse, or pain that changes how you move. Tell a parent and a coach or clinician.',
  'Stop wrist loaded exercises at once if the wrist hurts.',
];
const STOP_HOME = [
  'Stop a drill as soon as height, speed, or landing control drops, even with reps left.',
  'Stop jumping for the day for pain at the knee, below the kneecap, at the heel, or along the shin, and for any back pain when landing.',
  'Stop if the floor feels slippery, people come into the space, or something is in the way.',
];
const STOP_POOL = ['Stop for chest pain, unusual breathlessness, or dizziness, and get out of the water.', 'Stop shoulder strokes that pinch or hurt.'];

/** Seconds per rep, roughly, for the time estimate. */
function workSeconds(i: PlanItem): number {
  const t = i.target;
  const per = i.per ? 2 : 1;
  if (t.type === 'duration') return t.totalMin * 60;
  if (t.type === 'hold') return i.sets * t.seconds * per;
  if (t.type === 'roundTrips') return i.sets * t.count * 60;
  const kind = exercise(i.exerciseId)?.kind;
  const sec = kind === 'jump' ? 4 : kind === 'skill' ? 6 : 3;
  return i.sets * t.max * sec * per;
}

/** Time to move to the next exercise: about a minute at the gym to set up a machine, half that at home. */
const CHANGEOVER_SEC = { main: 60, home: 30, morning: 30, swim: 30 } as const;

export function estimateMinutes(items: PlanItem[], session: SessionKey): number {
  // Rest follows every set, including the last set of an exercise before the next one starts.
  // One sided work adds a short switch between sides, as the workout screen does. Only the very
  // last rest of the session is left out.
  const restAfter = (i: PlanItem) => (i.target.type === 'duration' ? 0 : i.sets * (i.restSec + (i.per ? Math.min(30, i.restSec) : 0)));
  const work = items.reduce((a, i) => a + workSeconds(i) + restAfter(i), 0);
  const last = items[items.length - 1];
  const total = work - (last ? Math.min(last.restSec, restAfter(last)) : 0) + Math.max(0, items.length - 1) * CHANGEOVER_SEC[session];
  const warm = session === 'main' ? 5 * 60 : 0;
  return Math.max(5, Math.round((total + warm) / 60 / 5) * 5);
}

export function sessionInfo(items: PlanItem[], session: SessionKey): SessionInfo {
  const location: Location = session === 'main' ? 'gym' : session === 'swim' ? 'pool' : 'home';
  // Space, floor, and ceiling have their own line, so they are not repeated as equipment.
  const isSpace = (e: string) => /\bmetres\b/i.test(e) || /^(no equipment|(a )?firm\b|a clear, flat|court or open floor|space to|a ceiling)/i.test(e);
  const equipment = [...new Set(items.flatMap((i) => (exercise(i.exerciseId)?.equipment ?? []).filter((e) => !isSpace(e)).slice(0, 2)))].slice(0, 8);
  let space = 'A normal gym floor.';
  if (location === 'home') {
    const needs = items.map((i) => HOME_NEEDS[i.exerciseId as LibraryExerciseId]).filter((n) => !!n);
    const rank = { small: 0, medium: 1, large: 2 } as const;
    const cRank = { low: 0, standard: 1, high: 2 } as const;
    const biggest = needs.reduce((a, n) => (rank[n!.space] > rank[a] ? n!.space : a), 'small' as keyof typeof rank);
    const ceiling = needs.reduce((a, n) => (cRank[n!.ceiling] > cRank[a] ? n!.ceiling : a), 'low' as keyof typeof cRank);
    space = `${SPACE_TEXT[biggest][0]!.toUpperCase()}${SPACE_TEXT[biggest].slice(1)}, ${CEILING_TEXT[ceiling]}, and a floor that is not slippery.`;
  }
  if (location === 'pool') space = 'A pool lane.';
  return {
    location,
    locationLabel: LOCATION_LABEL[location],
    equipment,
    space,
    minutes: estimateMinutes(items, session),
    stopRules: location === 'gym' ? STOP_GYM : location === 'pool' ? STOP_POOL : STOP_HOME,
  };
}
