// Muscle regions used for mapping, coverage, and the original body diagrams.
// Region IDs are stable. Never rename an ID; add a new one and migrate instead.

export const MUSCLE_IDS = [
  'pec_clavicular',
  'pec_sternal',
  'delt_anterior',
  'delt_lateral',
  'delt_posterior',
  'serratus_anterior',
  'biceps',
  'brachialis',
  'brachioradialis',
  'triceps',
  'forearm_flexors',
  'forearm_extensors',
  'rectus_abdominis',
  'obliques_core',
  'hip_flexors',
  'traps_upper',
  'traps_middle',
  'traps_lower',
  'rhomboids',
  'lats',
  'teres_major',
  'rotator_cuff',
  'erectors',
  'glute_max',
  'glute_med',
  'adductors',
  'quads',
  'hamstrings',
  'gastrocnemius',
  'soleus',
  'tibialis_anterior',
] as const;

export type MuscleId = (typeof MUSCLE_IDS)[number];

export type MuscleGroup =
  | 'chest'
  | 'shoulders'
  | 'arms'
  | 'forearms'
  | 'core'
  | 'upper_back'
  | 'lower_back'
  | 'hips'
  | 'thighs'
  | 'calves_shins';

export interface MuscleRegion {
  id: MuscleId;
  name: string;
  shortName: string;
  group: MuscleGroup;
  /** Which diagram views show this region. */
  views: Array<'front' | 'back'>;
  /** Plain educational note. Uses bias language, never isolation claims. */
  note: string;
  /** Optional sub part labels for education only. Not tracked separately. */
  parts?: string[];
}

export const MUSCLE_GROUP_LABELS: Record<MuscleGroup, string> = {
  chest: 'Chest',
  shoulders: 'Shoulders',
  arms: 'Upper arms',
  forearms: 'Forearms',
  core: 'Core',
  upper_back: 'Upper back',
  lower_back: 'Lower back',
  hips: 'Hips and glutes',
  thighs: 'Thighs',
  calves_shins: 'Calves and shins',
};

export const MUSCLES: MuscleRegion[] = [
  {
    id: 'pec_clavicular',
    name: 'Pectoralis major, clavicular part',
    shortName: 'Upper chest',
    group: 'chest',
    views: ['front'],
    note: 'The upper fibres of the chest. Incline pressing and low to high fly angles tend to bias this part, while the rest of the chest still works.',
  },
  {
    id: 'pec_sternal',
    name: 'Pectoralis major, sternal part',
    shortName: 'Mid and lower chest',
    group: 'chest',
    views: ['front'],
    note: 'The larger middle and lower part of the chest. Flat pressing and flat flyes load it well.',
  },
  {
    id: 'delt_anterior',
    name: 'Anterior deltoid',
    shortName: 'Front delt',
    group: 'shoulders',
    views: ['front'],
    note: 'Front of the shoulder. Works hard in pressing, so it rarely needs much direct work.',
  },
  {
    id: 'delt_lateral',
    name: 'Lateral deltoid',
    shortName: 'Side delt',
    group: 'shoulders',
    views: ['front', 'back'],
    note: 'Side of the shoulder. Lateral raises are the most direct way to train it.',
  },
  {
    id: 'delt_posterior',
    name: 'Posterior deltoid',
    shortName: 'Rear delt',
    group: 'shoulders',
    views: ['back'],
    note: 'Back of the shoulder. Trained by rows with the elbows out, face pulls, and reverse flyes.',
  },
  {
    id: 'serratus_anterior',
    name: 'Serratus anterior',
    shortName: 'Serratus',
    group: 'chest',
    views: ['front'],
    note: 'Along the side of the ribs. Moves the shoulder blade forward and upward during reaching, punching, spiking, and overhead work.',
  },
  {
    id: 'biceps',
    name: 'Biceps brachii',
    shortName: 'Biceps',
    group: 'arms',
    views: ['front'],
    parts: ['Long head', 'Short head'],
    note: 'Two heads. Arm position and grip can shift emphasis between the long and short head, but both work in every curl.',
  },
  {
    id: 'brachialis',
    name: 'Brachialis',
    shortName: 'Brachialis',
    group: 'arms',
    views: ['front', 'back'],
    note: 'Sits under the biceps. It flexes the elbow in every grip and gets extra emphasis from neutral and palm down grips.',
  },
  {
    id: 'brachioradialis',
    name: 'Brachioradialis',
    shortName: 'Brachioradialis',
    group: 'forearms',
    views: ['front', 'back'],
    note: 'Top of the forearm near the elbow. Hammer curls and neutral grip rows use it heavily.',
  },
  {
    id: 'triceps',
    name: 'Triceps brachii',
    shortName: 'Triceps',
    group: 'arms',
    views: ['back'],
    parts: ['Long head', 'Lateral head', 'Medial head'],
    note: 'Three heads. Overhead positions stretch the long head more, but all three heads extend the elbow in every triceps exercise.',
  },
  {
    id: 'forearm_flexors',
    name: 'Forearm flexors',
    shortName: 'Forearm flexors',
    group: 'forearms',
    views: ['front'],
    note: 'Palm side of the forearm. They close the hand and curl the wrist. Palm up wrist curls and heavy gripping train them.',
  },
  {
    id: 'forearm_extensors',
    name: 'Forearm extensors',
    shortName: 'Forearm extensors',
    group: 'forearms',
    views: ['back'],
    note: 'Back of the forearm. They lift the back of the hand. Palm down wrist curls train them directly.',
  },
  {
    id: 'rectus_abdominis',
    name: 'Rectus abdominis',
    shortName: 'Abs',
    group: 'core',
    views: ['front'],
    note: 'The front abdominal wall. It flexes the trunk and resists arching.',
  },
  {
    id: 'obliques_core',
    name: 'Obliques and deep core',
    shortName: 'Obliques and deep core',
    group: 'core',
    views: ['front', 'back'],
    note: 'Internal and external obliques plus the transverse abdominis. They resist rotation and side bending and stiffen the trunk for jumping and throwing.',
  },
  {
    id: 'hip_flexors',
    name: 'Hip flexors',
    shortName: 'Hip flexors',
    group: 'hips',
    views: ['front'],
    note: 'Iliopsoas and rectus femoris lift the thigh. They work hard in sprinting and leg raises.',
  },
  {
    id: 'traps_upper',
    name: 'Upper trapezius',
    shortName: 'Upper traps',
    group: 'upper_back',
    views: ['front', 'back'],
    note: 'Between the neck and shoulder. Elevates and upwardly rotates the shoulder blade.',
  },
  {
    id: 'traps_middle',
    name: 'Middle trapezius',
    shortName: 'Mid traps',
    group: 'upper_back',
    views: ['back'],
    note: 'Between the shoulder blades. Pulls the shoulder blades together in rows and reverse flyes.',
  },
  {
    id: 'traps_lower',
    name: 'Lower trapezius',
    shortName: 'Lower traps',
    group: 'upper_back',
    views: ['back'],
    note: 'Below the shoulder blades. Draws them down and helps overhead arm movement stay smooth.',
  },
  {
    id: 'rhomboids',
    name: 'Rhomboids',
    shortName: 'Rhomboids',
    group: 'upper_back',
    views: ['back'],
    note: 'Under the middle traps. Retract the shoulder blades in rows and high rows.',
  },
  {
    id: 'lats',
    name: 'Latissimus dorsi',
    shortName: 'Lats',
    group: 'upper_back',
    views: ['back'],
    note: 'The large back muscle. Pulls the upper arm down and back in pulldowns, rows, swimming, and spikes.',
  },
  {
    id: 'teres_major',
    name: 'Teres major',
    shortName: 'Teres major',
    group: 'upper_back',
    views: ['back'],
    note: 'Works with the lats to pull the arm down and back.',
  },
  {
    id: 'rotator_cuff',
    name: 'Rotator cuff',
    shortName: 'Rotator cuff',
    group: 'shoulders',
    views: ['back'],
    parts: ['Supraspinatus', 'Infraspinatus', 'Teres minor', 'Subscapularis'],
    note: 'Four small muscles that keep the ball of the shoulder centred. Infraspinatus and teres minor rotate the arm outward.',
  },
  {
    id: 'erectors',
    name: 'Spinal erectors',
    shortName: 'Spinal erectors',
    group: 'lower_back',
    views: ['back'],
    note: 'Run along the spine. Hold the back straight in squats, hinges, and rows.',
  },
  {
    id: 'glute_max',
    name: 'Gluteus maximus',
    shortName: 'Glute max',
    group: 'hips',
    views: ['back'],
    note: 'The main hip extensor. Drives jumping, sprinting, squats, hinges, and hip thrusts.',
  },
  {
    id: 'glute_med',
    name: 'Gluteus medius and minimus',
    shortName: 'Glute med and min',
    group: 'hips',
    views: ['back', 'front'],
    note: 'Side of the hip. Keep the pelvis level on one leg and control the knee on landings. Tensor fasciae latae helps in abduction.',
  },
  {
    id: 'adductors',
    name: 'Adductors',
    shortName: 'Adductors',
    group: 'thighs',
    views: ['front', 'back'],
    note: 'Inner thigh. Adductor magnus also helps extend the hip in squats and hinges.',
  },
  {
    id: 'quads',
    name: 'Quadriceps',
    shortName: 'Quads',
    group: 'thighs',
    views: ['front'],
    note: 'Front of the thigh. Extend the knee in squats, jumps, and leg extensions.',
  },
  {
    id: 'hamstrings',
    name: 'Hamstrings',
    shortName: 'Hamstrings',
    group: 'thighs',
    views: ['back'],
    note: 'Back of the thigh. Bend the knee and extend the hip. Important for sprinting and hamstring injury resilience.',
  },
  {
    id: 'gastrocnemius',
    name: 'Gastrocnemius',
    shortName: 'Gastrocnemius',
    group: 'calves_shins',
    views: ['back', 'front'],
    note: 'The upper calf. Works most with a straight knee, as in standing calf raises and jumping.',
  },
  {
    id: 'soleus',
    name: 'Soleus',
    shortName: 'Soleus',
    group: 'calves_shins',
    views: ['back', 'front'],
    note: 'The deeper, lower calf. Takes more of the load with a bent knee, as in seated calf raises and running.',
  },
  {
    id: 'tibialis_anterior',
    name: 'Tibialis anterior',
    shortName: 'Tibialis',
    group: 'calves_shins',
    views: ['front'],
    note: 'Front of the shin. Lifts the foot and helps control landings.',
  },
];

export const MUSCLE_BY_ID: Record<MuscleId, MuscleRegion> = Object.fromEntries(
  MUSCLES.map((m) => [m.id, m]),
) as Record<MuscleId, MuscleRegion>;

/** Regions the user asked to see clearly represented. Used by coverage checks. */
export const FOCUS_CHECKS: Array<{ key: string; label: string; muscles: MuscleId[] }> = [
  {
    key: 'upper_back',
    label: 'Upper back',
    muscles: ['traps_middle', 'traps_lower', 'rhomboids', 'lats', 'delt_posterior', 'teres_major'],
  },
  { key: 'calves', label: 'Calves', muscles: ['gastrocnemius', 'soleus'] },
  {
    key: 'forearms',
    label: 'Forearms',
    muscles: ['forearm_flexors', 'forearm_extensors', 'brachioradialis'],
  },
];

export const SHOULDER_MUSCLES: MuscleId[] = [
  'delt_anterior',
  'delt_lateral',
  'delt_posterior',
  'rotator_cuff',
];
