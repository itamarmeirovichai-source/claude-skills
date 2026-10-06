import type { LibraryExerciseId } from './exercises/ids';
import type { ActivityKind } from './types';

// Where each exercise belongs, how much it loads the wrist, and what a home drill needs from the
// room it is done in. Gym sessions are for strength work. Home sessions hold the jumps, landings,
// footwork, agility, and volleyball skill practice (3.0.0).

/**
 * How much an exercise loads a healing wrist. A practical judgement from grip, hand position, and
 * impact, not a measured value:
 *   none      the hands hold nothing heavy and take no impact
 *   low       light grip or forearm support
 *   moderate  a firm grip on a load, or pressing through the hands
 *   high      heavy grip, the wrist bent back under load, a fall onto the hands, or ball contact
 */
export type WristLoad = 'none' | 'low' | 'moderate' | 'high';

export const WRIST_LOAD: Record<LibraryExerciseId, WristLoad> = {
  // Lower body and trunk
  'barbell-squat': 'moderate',
  'romanian-deadlift': 'moderate',
  'bulgarian-split-squat': 'moderate',
  'standing-calf-raise': 'none',
  'tibialis-raise': 'none',
  'hack-squat': 'none',
  'barbell-hip-thrust': 'low',
  'seated-leg-curl': 'none',
  'leg-extension': 'none',
  'cable-hip-abduction': 'low',
  'seated-calf-raise': 'none',
  'nordic-hamstring-curl': 'high',
  'leg-press': 'none',
  'back-extension': 'none',
  'cable-hip-adduction': 'low',
  'smith-squat': 'low',
  'dumbbell-romanian-deadlift': 'moderate',
  'smith-romanian-deadlift': 'moderate',
  'walking-lunge': 'moderate',
  'smith-hip-thrust': 'low',
  'hip-abduction-machine': 'none',
  'adductor-machine': 'none',
  'leg-press-calf-raise': 'none',
  'single-leg-calf-raise': 'low',
  'cable-crunch': 'low',
  'ab-wheel-rollout': 'high',
  'cable-woodchop': 'low',
  'pallof-press': 'low',
  'copenhagen-plank': 'low',
  'hanging-leg-raise': 'high',
  'dead-bug': 'none',
  // Pressing
  'barbell-bench-press': 'high',
  'incline-barbell-bench-press': 'high',
  'machine-bench-press': 'moderate',
  'incline-machine-press': 'moderate',
  'incline-smith-press': 'moderate',
  'smith-bench-press': 'moderate',
  'incline-dumbbell-press': 'high',
  'dumbbell-bench-press': 'high',
  'flat-cable-fly': 'low',
  'pec-deck-fly': 'low',
  'standing-cable-crossover': 'low',
  // Pulling
  'wide-grip-lat-pulldown': 'moderate',
  'one-arm-lat-pulldown': 'moderate',
  'neutral-grip-pulldown': 'moderate',
  'assisted-pull-up': 'moderate',
  'straight-arm-cable-pulldown': 'moderate',
  'dumbbell-pullover': 'moderate',
  'leverage-high-row': 'moderate',
  'seated-cable-row': 'moderate',
  'chest-supported-dumbbell-row': 'moderate',
  'chest-supported-machine-row': 'moderate',
  // Shoulders
  'reverse-machine-fly': 'low',
  'cable-reverse-fly': 'low',
  'face-pull': 'low',
  'lateral-raise': 'low',
  'single-arm-cable-lateral-raise': 'low',
  'machine-lateral-raise': 'low',
  'cable-external-rotation': 'low',
  'side-lying-external-rotation': 'low',
  'dumbbell-y-raise': 'low',
  'dumbbell-shrug': 'high',
  'smith-shrug': 'moderate',
  // Arms
  'hammer-curl': 'moderate',
  'machine-preacher-curl': 'moderate',
  'incline-dumbbell-curl': 'moderate',
  'bayesian-cable-curl': 'moderate',
  'dumbbell-preacher-curl': 'moderate',
  'rope-hammer-curl': 'moderate',
  'cable-reverse-curl': 'high',
  'triceps-pushdown': 'moderate',
  'single-arm-cable-pushdown': 'moderate',
  'rope-overhead-triceps-extension': 'moderate',
  'single-arm-cable-overhead-extension': 'moderate',
  'dumbbell-overhead-triceps-extension': 'high',
  'palm-down-wrist-curl': 'high',
  'palm-up-wrist-curl': 'high',
  // Jumps, sprints, volleyball, conditioning
  'easy-jump-rope': 'low',
  'dynamic-volleyball-warm-up': 'none',
  'volleyball-approach-jump': 'none',
  'countermovement-jump': 'none',
  'volleyball-approach-footwork': 'none',
  'shuffle-to-sprint': 'none',
  'medicine-ball-spike-throw': 'high',
  'volleyball-spike': 'high',
  'lateral-block-jump': 'low',
  'block-to-spike-transition': 'high',
  'ten-metre-sprint': 'none',
  'easy-pool-round-trip': 'moderate',
  'shadow-pass-footwork': 'none',
  'block-footwork': 'none',
  'pogo-hop': 'none',
  'snap-down-stick': 'none',
  'box-jump': 'low',
  'hurdle-hop': 'none',
  'broad-jump': 'none',
  'depth-jump': 'low',
  'single-leg-hop': 'none',
  'approach-touch-jump': 'none',
  'home-movement-prep': 'none',
  'lateral-line-hop': 'none',
  'spike-arm-swing-shadow': 'none',
  'wall-spike-control': 'high',
};

const WRIST_RANK: Record<WristLoad, number> = { none: 0, low: 1, moderate: 2, high: 3 };

export function wristLoad(id: string): WristLoad {
  return WRIST_LOAD[id as LibraryExerciseId] ?? 'moderate';
}

export const WRIST_TEXT: Record<WristLoad, string> = {
  none: 'The hands hold nothing heavy and take no impact.',
  low: 'Light grip or forearm support. Keep the wrist straight and stop if it hurts.',
  moderate: 'A firm grip, or pressing through the hands. Keep the wrist straight, in line with the forearm. While the wrist is not cleared, the load stays the same: reps may go up, weight does not.',
  high: 'Heavy grip, the wrist bent back under load, a fall onto the hands, or ball contact. Only after a clinician has cleared the wrist.',
};

// ---------- Wrist clearance ----------

/**
 * Wrist status from the athlete profile.
 *   unknown      not answered yet, treated like not cleared
 *   not-cleared  still healing, or the clinician has not confirmed full return
 *   cleared      a clinician has confirmed full return to sport and lifting
 *   symptoms     pain, swelling, or weakness now
 */
export type WristStatus = 'unknown' | 'not-cleared' | 'cleared' | 'symptoms';

/** The heaviest wrist load allowed in the plan for a wrist status. */
export function maxWristLoad(status: WristStatus): WristLoad {
  if (status === 'cleared') return 'high';
  if (status === 'symptoms') return 'low';
  return 'moderate';
}

export function wristAllows(id: string, status: WristStatus): boolean {
  return WRIST_RANK[wristLoad(id)] <= WRIST_RANK[maxWristLoad(status)];
}

/** While the wrist is not cleared, exercises that grip or press a load keep their load. */
export function wristHoldsLoad(id: string, status: WristStatus): boolean {
  return status !== 'cleared' && WRIST_RANK[wristLoad(id)] >= WRIST_RANK.moderate;
}

// ---------- Location ----------

export type Location = 'gym' | 'home' | 'pool' | 'court';

export const LOCATION_LABEL: Record<Location, string> = { gym: 'Gym', home: 'Home', pool: 'Pool', court: 'Court or practice' };

const COURT_ONLY = new Set<string>(['volleyball-spike', 'block-to-spike-transition', 'lateral-block-jump', 'approach-touch-jump', 'volleyball-approach-jump', 'medicine-ball-spike-throw']);
const HOME_KINDS: ActivityKind[] = ['jump', 'sprint', 'skill', 'throw', 'conditioning'];

/** Where an exercise is planned. Strength work is for the gym; jumps, footwork, and skills are for home. */
export function locationOf(id: string, kind: ActivityKind): Location {
  if (kind === 'swim') return 'pool';
  if (COURT_ONLY.has(id)) return 'court';
  if (HOME_KINDS.includes(kind)) return 'home';
  if (kind === 'warmup') return id === 'home-movement-prep' ? 'home' : 'gym';
  return 'gym';
}

// ---------- What a home drill needs from the room ----------

/** Clear floor: small about 2 by 2 metres, medium about 3 by 3 metres, large 5 metres or more in one direction. */
export type SpaceSize = 'small' | 'medium' | 'large';
/** Low: you can touch it with a raised arm. Standard: you cannot, even on your toes. High: you cannot even jumping, such as outdoors or in a hall. */
export type CeilingLevel = 'low' | 'standard' | 'high';
export type Impact = 'none' | 'low' | 'moderate' | 'high';
export type Noise = 'quiet' | 'some' | 'loud';
export type HomeEquipment = 'mat' | 'box' | 'cones' | 'ball' | 'wall' | 'rope' | 'tape' | 'light-dumbbells';

export interface SpaceNeeds {
  space: SpaceSize;
  ceiling: CeilingLevel;
  impact: Impact;
  noise: Noise;
  /** Ball contact needs a space without people or breakable things nearby. */
  ball?: boolean;
  equipment?: HomeEquipment[];
}

export const HOME_NEEDS: Partial<Record<LibraryExerciseId, SpaceNeeds>> = {
  'home-movement-prep': { space: 'small', ceiling: 'low', impact: 'none', noise: 'quiet' },
  'dynamic-volleyball-warm-up': { space: 'large', ceiling: 'high', impact: 'low', noise: 'some' },
  'tibialis-raise': { space: 'small', ceiling: 'low', impact: 'none', noise: 'quiet', equipment: ['wall'] },
  'dead-bug': { space: 'small', ceiling: 'low', impact: 'none', noise: 'quiet' },
  'shadow-pass-footwork': { space: 'medium', ceiling: 'low', impact: 'none', noise: 'quiet' },
  'block-footwork': { space: 'medium', ceiling: 'standard', impact: 'none', noise: 'quiet' },
  'volleyball-approach-footwork': { space: 'large', ceiling: 'standard', impact: 'none', noise: 'quiet' },
  'spike-arm-swing-shadow': { space: 'small', ceiling: 'standard', impact: 'none', noise: 'quiet' },
  'pogo-hop': { space: 'small', ceiling: 'standard', impact: 'low', noise: 'some' },
  'snap-down-stick': { space: 'small', ceiling: 'standard', impact: 'low', noise: 'some' },
  'lateral-line-hop': { space: 'small', ceiling: 'standard', impact: 'low', noise: 'some', equipment: ['tape'] },
  'easy-jump-rope': { space: 'medium', ceiling: 'standard', impact: 'low', noise: 'some', equipment: ['rope'] },
  'countermovement-jump': { space: 'small', ceiling: 'high', impact: 'moderate', noise: 'loud' },
  'broad-jump': { space: 'large', ceiling: 'standard', impact: 'moderate', noise: 'loud' },
  'single-leg-hop': { space: 'medium', ceiling: 'standard', impact: 'moderate', noise: 'loud' },
  'box-jump': { space: 'medium', ceiling: 'high', impact: 'moderate', noise: 'loud', equipment: ['box'] },
  'hurdle-hop': { space: 'large', ceiling: 'high', impact: 'moderate', noise: 'loud', equipment: ['cones'] },
  'depth-jump': { space: 'medium', ceiling: 'high', impact: 'high', noise: 'loud', equipment: ['box'] },
  'shuffle-to-sprint': { space: 'large', ceiling: 'standard', impact: 'moderate', noise: 'some', equipment: ['cones'] },
  'ten-metre-sprint': { space: 'large', ceiling: 'standard', impact: 'moderate', noise: 'some', equipment: ['cones'] },
  'wall-spike-control': { space: 'large', ceiling: 'high', impact: 'none', noise: 'loud', ball: true, equipment: ['ball', 'wall'] },
};

export const SPACE_TEXT: Record<SpaceSize, string> = { small: 'about 2 by 2 metres of clear floor', medium: 'about 3 by 3 metres of clear floor', large: '5 metres or more of clear space in one direction' };
export const CEILING_TEXT: Record<CeilingLevel, string> = { low: 'any ceiling', standard: 'a ceiling you cannot touch with a raised arm', high: 'outdoors or a hall where you cannot touch the ceiling even when jumping' };
