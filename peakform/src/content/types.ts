import type { MuscleId } from './muscles';

/** How an activity is logged and progressed. */
export type ActivityKind =
  | 'strength' // loaded reps: weight, reps, RIR, form, pain
  | 'bodyweight' // reps without external load (Nordic, hanging leg raise)
  | 'hold' // seconds (Copenhagen plank)
  | 'jump' // quality reps: landing, height
  | 'sprint' // quality reps: time optional
  | 'skill' // volleyball skill reps
  | 'throw' // medicine ball throws
  | 'conditioning' // timed intervals, jump rope
  | 'warmup' // timed warm up, not counted as hypertrophy work
  | 'swim'; // pool round trips

export type MovementPattern =
  | 'squat'
  | 'hinge'
  | 'lunge'
  | 'hip_extension'
  | 'knee_flexion'
  | 'knee_extension'
  | 'hip_abduction'
  | 'hip_adduction'
  | 'plantar_flexion'
  | 'dorsiflexion'
  | 'horizontal_push'
  | 'vertical_pull'
  | 'horizontal_pull'
  | 'high_pull'
  | 'shoulder_abduction'
  | 'shoulder_horizontal_abduction'
  | 'shoulder_horizontal_adduction'
  | 'shoulder_external_rotation'
  | 'shoulder_extension'
  | 'shoulder_elevation'
  | 'elbow_flexion'
  | 'elbow_extension'
  | 'wrist_flexion'
  | 'wrist_extension'
  | 'anti_rotation'
  | 'anti_extension'
  | 'trunk_flexion'
  | 'lateral_core'
  | 'trunk_rotation'
  | 'jump'
  | 'sprint'
  | 'change_of_direction'
  | 'throw'
  | 'overhead_strike'
  | 'locomotion'
  | 'swim'
  | 'general_preparation';

export type FatigueArea =
  | 'shoulder'
  | 'elbow'
  | 'wrist_grip'
  | 'low_back'
  | 'knee'
  | 'hip'
  | 'hamstring'
  | 'achilles_calf'
  | 'shin'
  | 'neck'
  | 'systemic';

export type LoadIncrementClass = 'upper' | 'lower' | 'none';

/**
 * How close to failure the plan may take an exercise.
 *   'all'    every set may end at technical failure (machines, cables, safe isolation work)
 *   'last'   the first sets stop one rep short, only the last set goes to failure (machine and Smith compounds)
 *   'never'  always stop short, because a failed rep is hard to escape safely alone
 * Technical failure means the last rep that can be finished with clean form.
 */
export type FailurePolicy = 'all' | 'last' | 'never';

// ---------- Original keyframe illustrations ----------

/**
 * Side view pose. The figure faces right.
 * Angles are absolute, in degrees:
 *   0 = segment points straight down
 *   90 = points forward (to the right, where the figure faces)
 *   180 = points straight up
 *   -90 = points backward (to the left)
 * trunk goes from hip to neck, so standing upright is 180.
 * Arms go shoulder to elbow, then elbow to wrist. Legs go hip to knee, knee to ankle, ankle to toe.
 */
export interface Pose {
  label: 'Start' | 'Middle' | 'Finish' | string;
  caption: string;
  trunk: number;
  head?: number;
  armNear: [number, number];
  armFar?: [number, number];
  legNear: [number, number] | [number, number, number];
  legFar?: [number, number] | [number, number, number];
  /** Explicit hip position on the 200 x 180 canvas. Without it, the lowest foot point rests on the ground. */
  hip?: [number, number];
  /** Pixels above the ground for airborne frames. */
  lift?: number;
  /** Horizontal position of the near ankle when auto grounded. Default 95. */
  footX?: number;
  props?: PoseProp[];
}

export type Anchor = 'hands' | 'nearHand' | 'farHand' | 'shoulders' | 'hips' | 'nearAnkle' | 'nearKnee' | [number, number];

export type PoseProp =
  | { type: 'barbell'; at: Anchor }
  | { type: 'dumbbell'; at: Anchor }
  | { type: 'handle'; at: Anchor }
  | { type: 'cable'; from: Anchor; to: [number, number] }
  | { type: 'bench'; x: number; y: number; w: number; h?: number; angle?: number }
  | { type: 'box'; x: number; y: number; w: number; h: number }
  | { type: 'pad'; x: number; y: number; w: number; h: number }
  | { type: 'ball'; at: Anchor; r?: number }
  | { type: 'line'; x1: number; y1: number; x2: number; y2: number }
  | { type: 'rope' }
  | { type: 'water'; y: number }
  | { type: 'net'; x: number }
  | { type: 'arrow'; from: [number, number]; to: [number, number] };

/** Top down drill diagram for volleyball footwork, sprints, and pool work. Units are metres. */
export interface DrillDiagram {
  kind: 'court' | 'lane' | 'pool';
  caption: string;
  /** Court: half court 9 m wide and 9 m deep, net at y = 0. Lane: x along the lane 0 to 12. Pool: x along the length 0 to 25. */
  steps: Array<{ x: number; y: number; label?: string }>;
  ball?: { x: number; y: number };
  markers?: Array<{ x: number; y: number; label: string }>;
}

export interface ExerciseVisual {
  poses?: Pose[];
  diagram?: DrillDiagram;
}

export interface Substitution {
  /** Exercise ID if it exists in the library, otherwise null. */
  exerciseId: string | null;
  name: string;
  reason: string;
}

export interface ExerciseContent {
  id: string;
  name: string;
  aliases?: string[];
  kind: ActivityKind;
  purpose: string;
  equipment: string[];
  setup: string[];
  steps: string[];
  breathing: string;
  tempo: string;
  rangeOfMotion: string;
  muscles: {
    primary: MuscleId[];
    secondary: MuscleId[];
  };
  /** Bias language for muscle emphasis. Never claims isolation. */
  emphasisNote: string;
  movementPattern: MovementPattern;
  joints: string[];
  laterality: 'bilateral' | 'unilateral' | 'alternating';
  /** True when the log should capture left and right separately. */
  logSides: boolean;
  fatigueOverlap: FatigueArea[];
  commonMistakes: string[];
  goodFormFeels: string;
  stopRules: string[];
  safetyNotes: string[];
  easierSubstitution: Substitution;
  equipmentSubstitution: Substitution;
  otherSubstitutions?: Substitution[];
  loadIncrement: LoadIncrementClass;
  /** How close to failure the plan may take this exercise. Required for loaded and body weight work. */
  failure?: FailurePolicy;
  visual: ExerciseVisual;
}

// ---------- Media and sources ----------

/**
 * A lawful external reference. PeakForm never downloads or rehosts creator media.
 * reviewStatus is honest about how far a reference was checked:
 *   'metadata-match'  title, channel, and description match the exact exercise, video not watched frame by frame
 *   'user-confirmed'  the user watched it in the app and confirmed it matches (set at runtime only)
 *   'not-accessible'  the link could not be opened from the build environment
 */
export interface MediaReference {
  id: string;
  /** Exercise or recipe ID this reference belongs to. */
  targetId: string;
  targetType: 'exercise' | 'recipe' | 'claim';
  platform: 'youtube' | 'tiktok' | 'instagram' | 'web';
  title: string;
  channel: string;
  url: string;
  /** YouTube video ID when platform is youtube. */
  videoId?: string;
  verifiedOn: string; // YYYY-MM-DD
  language: string;
  captions: 'yes' | 'no' | 'unknown';
  reviewStatus: 'metadata-match' | 'user-confirmed' | 'not-accessible';
  reviewerNote: string;
}

export interface SourceReference {
  id: string;
  title: string;
  publisher: string;
  url: string;
  /** Publication year or date as printed by the source. */
  published: string;
  /** Date PeakForm reviewed it, YYYY-MM-DD. */
  reviewedOn: string;
  topic: 'youth-training' | 'nutrition' | 'recovery' | 'body-composition' | 'supplements' | 'food-safety' | 'platform' | 'media' | 'hosting';
  conclusion: string;
  productDecision: string;
  uncertainty: string;
  /** How the reviewer accessed it, stated honestly. */
  access: 'full-text' | 'abstract-or-summary' | 'search-snippet' | 'prior-knowledge';
}

/** Record of a social media claim review. Social claims are leads, not evidence. */
export interface ClaimReview {
  id: string;
  url: string;
  platform: 'tiktok' | 'instagram' | 'youtube' | 'web';
  accessible: boolean;
  claimed: string;
  evidence: string;
  verdict: string;
  changesApp: boolean;
  reviewedOn: string;
}
