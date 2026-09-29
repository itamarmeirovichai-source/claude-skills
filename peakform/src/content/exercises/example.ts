import type { ExerciseContent } from '../types';

// Reference entry that shows the expected tone, depth, and pose conventions.
// The real library entries live in lower.ts, upper.ts, and athletic.ts.

export const EXAMPLE_BARBELL_SQUAT: ExerciseContent = {
  id: 'barbell-squat',
  name: 'Barbell Squat',
  aliases: ['Back squat'],
  kind: 'strength',
  purpose: 'Builds leg and hip strength that carries over to jumping, landing, and sprinting.',
  equipment: ['Barbell', 'Squat rack with safety bars'],
  setup: [
    'Set the safety bars just below the depth you reach at the bottom.',
    'Place the bar on your upper back, below the bony top of the spine.',
    'Stand with feet about shoulder width and toes turned out slightly.',
    'Brace your trunk as if someone were about to push on your stomach.',
  ],
  steps: [
    'Unrack the bar and take two or three small steps back.',
    'Sit down and back between your hips, letting the knees travel forward over the toes.',
    'Keep the whole foot on the floor and the chest facing forward.',
    'Pause briefly at the depth you control without the lower back rounding.',
    'Drive the floor away and stand up in one smooth line.',
  ],
  breathing: 'Breathe in and brace before each rep. Breathe out near the top.',
  tempo: '3 1 1 0 means three seconds down, one second pause at the bottom, one second up, no rest at the top.',
  rangeOfMotion: 'Go as deep as you can with a neutral back and heels down. Thighs near parallel or lower is a good target.',
  muscles: {
    primary: ['quads', 'glute_max'],
    secondary: ['adductors', 'erectors', 'hamstrings', 'obliques_core'],
  },
  emphasisNote:
    'Depth, stance width, and torso angle shift the balance between quads, glutes, and adductors. None of them switch off.',
  movementPattern: 'squat',
  joints: ['Hip', 'Knee', 'Ankle'],
  laterality: 'bilateral',
  logSides: false,
  fatigueOverlap: ['knee', 'low_back', 'hip', 'systemic'],
  commonMistakes: [
    'Heels lifting at the bottom.',
    'Knees caving inward on the way up.',
    'Hips shooting up first so the squat turns into a good morning.',
    'Losing the brace and rounding the lower back at depth.',
  ],
  goodFormFeels: 'Pressure through the whole foot, a tight trunk, and effort shared by the front of the thighs and the glutes.',
  stopRules: [
    'Stop the set when bar speed slows sharply or technique changes.',
    'Stop when you reach the prescribed reps in reserve.',
    'Stop and log pain if the knee, hip, or back hurts. Pain of 4 out of 10 or more pauses this exercise.',
  ],
  safetyNotes: [
    'Always use the safety bars.',
    'Learn this lift with a qualified coach first.',
    'Never test a one rep maximum.',
  ],
  easierSubstitution: {
    exerciseId: null,
    name: 'Goblet squat',
    reason: 'Lighter load in front of the body makes it easier to learn depth and bracing.',
  },
  equipmentSubstitution: {
    exerciseId: 'hack-squat',
    name: 'Hack Squat',
    reason: 'Use when the rack is busy. The machine guides the path and keeps the torso more upright.',
  },
  otherSubstitutions: [
    { exerciseId: null, name: 'Leg press', reason: 'Less demand on the lower back.' },
  ],
  loadIncrement: 'lower',
  visual: {
    poses: [
      {
        label: 'Start',
        caption: 'Stand tall with the bar on the upper back and the trunk braced.',
        trunk: 178,
        armNear: [-30, 160],
        legNear: [0, 0],
        legFar: [2, -2],
        props: [{ type: 'barbell', at: 'hands' }],
      },
      {
        label: 'Bottom',
        caption: 'Hips go down and back, knees travel forward, heels stay down.',
        trunk: 140,
        armNear: [-70, 120],
        legNear: [82, -38],
        legFar: [80, -36],
        props: [
          { type: 'barbell', at: 'hands' },
          { type: 'arrow', from: [150, 60], to: [150, 100] },
        ],
      },
      {
        label: 'Finish',
        caption: 'Drive up in one line and stand tall without leaning back.',
        trunk: 178,
        armNear: [-30, 160],
        legNear: [0, 0],
        legFar: [2, -2],
        props: [
          { type: 'barbell', at: 'hands' },
          { type: 'arrow', from: [150, 100], to: [150, 60] },
        ],
      },
    ],
  },
};
