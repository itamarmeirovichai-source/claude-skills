// Every exercise ID in the built in library. Plan entries and substitutions must use these.
export const LOWER_IDS = [
  'barbell-squat',
  'romanian-deadlift',
  'bulgarian-split-squat',
  'standing-calf-raise',
  'tibialis-raise',
  'hack-squat',
  'barbell-hip-thrust',
  'seated-leg-curl',
  'leg-extension',
  'cable-hip-abduction',
  'seated-calf-raise',
  'nordic-hamstring-curl',
] as const;

export const UPPER_IDS = [
  'barbell-bench-press',
  'incline-barbell-bench-press',
  'machine-bench-press',
  'flat-cable-fly',
  'wide-grip-lat-pulldown',
  'one-arm-lat-pulldown',
  'leverage-high-row',
  'seated-cable-row',
  'reverse-machine-fly',
  'face-pull',
  'lateral-raise',
  'single-arm-cable-lateral-raise',
  'cable-external-rotation',
  'hammer-curl',
  'machine-preacher-curl',
  'triceps-pushdown',
  'rope-overhead-triceps-extension',
  'palm-down-wrist-curl',
  'palm-up-wrist-curl',
] as const;

export const ATHLETIC_IDS = [
  'easy-jump-rope',
  'dynamic-volleyball-warm-up',
  'volleyball-approach-jump',
  'countermovement-jump',
  'volleyball-approach-footwork',
  'shuffle-to-sprint',
  'medicine-ball-spike-throw',
  'volleyball-spike',
  'lateral-block-jump',
  'block-to-spike-transition',
  'ten-metre-sprint',
  'easy-pool-round-trip',
  'pallof-press',
  'copenhagen-plank',
  'hanging-leg-raise',
] as const;

export const MORNING_IDS = ['shadow-pass-footwork', 'block-footwork', 'dumbbell-y-raise', 'side-lying-external-rotation', 'dead-bug'] as const;

export const GYM_IDS = [
  'incline-dumbbell-press',
  'chest-supported-dumbbell-row',
  'incline-dumbbell-curl',
  'leg-press',
  'back-extension',
  'cable-hip-adduction',
] as const;

// Alternatives for the exercise questionnaire, added in 2.0.0. Machines, cables, the Smith machine,
// and dumbbells only, so failure sets are safe without a spotter.
export const PUSH_CHOICE_IDS = [
  'incline-machine-press',
  'incline-smith-press',
  'dumbbell-bench-press',
  'smith-bench-press',
  'pec-deck-fly',
  'standing-cable-crossover',
  'machine-lateral-raise',
  'dumbbell-overhead-triceps-extension',
  'single-arm-cable-overhead-extension',
  'single-arm-cable-pushdown',
] as const;

export const PULL_CHOICE_IDS = [
  'neutral-grip-pulldown',
  'assisted-pull-up',
  'straight-arm-cable-pulldown',
  'dumbbell-pullover',
  'chest-supported-machine-row',
  'cable-reverse-fly',
  'bayesian-cable-curl',
  'dumbbell-preacher-curl',
  'rope-hammer-curl',
  'cable-reverse-curl',
  'dumbbell-shrug',
  'smith-shrug',
] as const;

export const LEGS_CHOICE_IDS = [
  'smith-squat',
  'dumbbell-romanian-deadlift',
  'smith-romanian-deadlift',
  'walking-lunge',
  'smith-hip-thrust',
  'hip-abduction-machine',
  'adductor-machine',
  'leg-press-calf-raise',
  'single-leg-calf-raise',
  'cable-crunch',
  'ab-wheel-rollout',
  'cable-woodchop',
] as const;

export const LIBRARY_IDS = [...LOWER_IDS, ...UPPER_IDS, ...ATHLETIC_IDS, ...MORNING_IDS, ...GYM_IDS, ...PUSH_CHOICE_IDS, ...PULL_CHOICE_IDS, ...LEGS_CHOICE_IDS] as const;
export type LibraryExerciseId = (typeof LIBRARY_IDS)[number];
