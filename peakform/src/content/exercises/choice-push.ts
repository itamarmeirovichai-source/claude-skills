import { EFFORT_RULE, PAIN_RULE } from './effort';
import type { ExerciseContent, Pose, PoseProp } from '../types';

// Push alternatives for the exercise questionnaire. Order matches PUSH_CHOICE_IDS in ids.ts.
// Machines, cables, the Smith machine, and dumbbells only, so hard sets are safe without a spotter.
// Poses are side views unless the caption says front view. Flyes and lateral raises move the
// arms out to the sides, so they read far better from the front.

type Base = Pick<Pose, 'trunk' | 'hip' | 'legNear' | 'legFar' | 'footX' | 'head'>;

/** Seated in an incline chest press, back pad reclined about 32 degrees, feet flat. */
const INCLINE_MACHINE: Base = { trunk: 212, hip: [80, 132], legNear: [90, 0] };
const INCLINE_MACHINE_PROPS: PoseProp[] = [
  { type: 'bench', x: 56, y: 140, w: 46 },
  { type: 'bench', x: 69.4, y: 134.6, w: 64, h: 8, angle: -122 },
];

/** Low incline bench, about 40 degrees, under a Smith bar that runs on a vertical rail. */
const INCLINE: Base = { trunk: 230, hip: [122, 128], legNear: [83, -12] };
const SMITH_INCLINE_PROPS: PoseProp[] = [
  { type: 'line', x1: 98.3, y1: 6, x2: 98.3, y2: 172 },
  { type: 'line', x1: 88, y1: 118, x2: 88, y2: 172 },
  { type: 'bench', x: 66, y: 94, w: 58, h: 8, angle: 40 },
  { type: 'bench', x: 100, y: 137, w: 40 },
  // Safety stop on the rail, just above the chest.
  { type: 'pad', x: 92.3, y: 89, w: 12, h: 5 },
];

/** Lying face up on a flat bench, head to the left, feet on the floor. */
const LYING: Base = { trunk: -90, hip: [130, 116], legNear: [68, -10] };
const FLAT_BENCH: PoseProp = { type: 'bench', x: 55, y: 125, w: 88 };
const SMITH_FLAT_PROPS: PoseProp[] = [
  { type: 'line', x1: 100.9, y1: 6, x2: 100.9, y2: 172 },
  FLAT_BENCH,
  // Safety stop on the rail, just above the chest.
  { type: 'pad', x: 94.9, y: 101, w: 12, h: 5 },
];

/** Front view, seated: the figure faces you, near side on the right of the picture, knees apart. */
const FRONT_SEATED: Base = { trunk: 180, hip: [100, 100], legNear: [40, 0, 90], legFar: [-40, 0, -90] };
/** Seat and post seen from the front. */
const FRONT_SEAT: PoseProp[] = [
  { type: 'box', x: 76, y: 100, w: 48, h: 8 },
  { type: 'line', x1: 100, y1: 108, x2: 100, y2: 172 },
];
/** Seat with a back pad that shows on both sides of the trunk. */
const FRONT_SEAT_PROPS: PoseProp[] = [{ type: 'box', x: 86, y: 44, w: 28, h: 56 }, ...FRONT_SEAT];
const PEC_DECK_PROPS: PoseProp[] = [
  { type: 'line', x1: 22, y1: 14, x2: 22, y2: 172 },
  { type: 'line', x1: 178, y1: 14, x2: 178, y2: 172 },
  { type: 'line', x1: 22, y1: 14, x2: 178, y2: 14 },
  ...FRONT_SEAT_PROPS,
];

/** Lateral raise machine pads on the outside of the upper arms, just above the elbows. */
const LATERAL_PADS_DOWN: PoseProp[] = [
  { type: 'pad', x: 113.4, y: 62.1, w: 5, h: 13 },
  { type: 'pad', x: 81.6, y: 62.1, w: 5, h: 13 },
];
const LATERAL_PADS_UP: PoseProp[] = [
  { type: 'pad', x: 116.9, y: 44.6, w: 13, h: 5 },
  { type: 'pad', x: 70.1, y: 44.6, w: 13, h: 5 },
];

/** Front view, standing between two cable towers, pulleys a little above shoulder height. */
const FRONT: Base = { trunk: 180, legNear: [12, 0, 90], legFar: [-12, 0, -90], footX: 108 };
const CROSSOVER_POSTS: PoseProp[] = [
  { type: 'line', x1: 12, y1: 14, x2: 12, y2: 172 },
  { type: 'line', x1: 188, y1: 14, x2: 188, y2: 172 },
];

/** Upright bench with a back pad that ends below the shoulders, so the dumbbell has room behind the head. */
const UPRIGHT: Base = { trunk: 180, head: 162, hip: [80, 132], legNear: [90, 0] };
const UPRIGHT_PROPS: PoseProp[] = [
  { type: 'bench', x: 56, y: 140, w: 46 },
  { type: 'bench', x: 67.5, y: 136, w: 46, h: 8, angle: -90 },
];

/** Split stance facing away from the pulley, trunk leaning forward, head tipped so the arm stays visible. */
const OVERHEAD: Base = { trunk: 150, head: 128, legNear: [18, 0], legFar: [-20, -20, 75], footX: 110 };
const OVERHEAD_POST: PoseProp = { type: 'line', x1: 18, y1: 10, x2: 18, y2: 172 };

/** Standing, slight forward lean, facing a high pulley. */
const PUSHDOWN: Base = { trunk: 172, legNear: [0, 0], legFar: [3, -3] };

export const PUSH_CHOICES: ExerciseContent[] = [
  // ---------------------------------------------------------------- Incline Machine Chest Press
  {
    id: 'incline-machine-press',
    name: 'Incline Machine Chest Press',
    aliases: ['Incline chest press machine', 'Plate loaded incline press'],
    kind: 'strength',
    purpose:
      'Builds the upper chest and the front of the shoulders on a guided path. You can press hard into a deep stretch with no spotter and no weight to balance, which suits training alone.',
    equipment: ['Incline chest press machine, with a weight stack or plate loaded'],
    setup: [
      'Set the seat so the handles start level with your upper chest, just below the collarbones.',
      'Sit with your hips, upper back, and head against the pads and your feet flat on the floor.',
      'Grip the handles with straight wrists, knuckles in line with your forearms.',
      'Pull your shoulder blades back and down before the first rep.',
      'If the handles have a start position setting, choose one that gives a deep chest stretch without your shoulders rolling forward.',
    ],
    steps: [
      'Press the handles up and slightly in until your arms are straight but not locked hard.',
      'Keep your back on the pad and your shoulders down, away from your ears.',
      'Let the handles come back slowly until they are level with your upper chest and you feel a deep stretch across it.',
      'Pause for one second in that stretch without letting the weight rest.',
      'Press again along the same path.',
    ],
    breathing: 'Breathe in as the handles come back. Breathe out as you press through the hardest part.',
    tempo: '3 1 1 0 means three seconds as the handles come back, a one second pause in the stretch, one second to press, and no rest at the top.',
    rangeOfMotion:
      'Bring the handles back until they are level with your upper chest, or a little behind if your shoulders stay pulled back and comfortable. Press to nearly straight arms.',
    muscles: {
      primary: ['pec_clavicular', 'delt_anterior'],
      secondary: ['triceps', 'pec_sternal'],
    },
    emphasisNote:
      'The upward angle of the press biases the upper chest and the front of the shoulder, while the middle chest and triceps still share the work. Machines and free weights build muscle about equally in the studies that compared them (Haugen 2023), so the guided path costs you nothing for growth and lets you work hard safely on your own.',
    movementPattern: 'horizontal_push',
    joints: ['Shoulder', 'Elbow', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder', 'elbow'],
    commonMistakes: [
      'Setting the seat so the handles start at the neck or the middle of the chest.',
      'Letting the handles pull the shoulders forward off the pad in the stretch.',
      'Shrugging the shoulders up toward the ears as you press.',
      'Cutting the stretch short so the handles never come back to the chest.',
      'Letting the weight crash between reps.',
    ],
    goodFormFeels:
      'Your back stays on the pad, you feel a deep stretch across the upper chest at the bottom, and the press feels smooth in the upper chest and the backs of the arms.',
    stopRules: [
      'Stop the set when the press slows sharply, your back leaves the pad, or your shoulders roll forward.',
      EFFORT_RULE.last,
      PAIN_RULE,
    ],
    safetyNotes: [
      'On a plate loaded machine, load both sides evenly and check the plates sit fully on before you sit down.',
      'If a rep stalls, let the handles back slowly to the start instead of dropping them.',
      'Your shoulders also work in spiking and swimming. Stop the set if the front of the shoulder pinches.',
    ],
    easierSubstitution: {
      exerciseId: 'machine-bench-press',
      name: 'Machine Bench Press',
      reason: 'The same guided press at a flat angle. It asks a little less of the front shoulder, so it is gentler if the incline pinches.',
    },
    equipmentSubstitution: {
      exerciseId: 'incline-smith-press',
      name: 'Incline Smith Machine Press',
      reason: 'Use when the machine is busy. The Smith bar runs on rails, so you still need no spotter once the safety stops are set.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'incline-dumbbell-press',
        name: 'Incline Dumbbell Press',
        reason: 'A free weight option at the same angle. Stop one rep earlier, because heavy dumbbells are harder to escape alone.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'last',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Sit back against the reclined pad with the handles level with the upper chest.',
          ...INCLINE_MACHINE,
          armNear: [-10, 145],
          props: [...INCLINE_MACHINE_PROPS, { type: 'handle', at: 'hands' }],
        },
        {
          label: 'Press',
          caption: 'Press up and slightly in to nearly straight arms, back still on the pad.',
          ...INCLINE_MACHINE,
          armNear: [150, 150],
          props: [...INCLINE_MACHINE_PROPS, { type: 'handle', at: 'hands' }, { type: 'arrow', from: [98, 94], to: [114, 46] }],
        },
        {
          label: 'Finish',
          caption: 'Let the handles come back slowly into a deep stretch at the upper chest.',
          ...INCLINE_MACHINE,
          armNear: [-10, 145],
          props: [...INCLINE_MACHINE_PROPS, { type: 'handle', at: 'hands' }, { type: 'arrow', from: [114, 46], to: [98, 94] }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Incline Smith Machine Press
  {
    id: 'incline-smith-press',
    name: 'Incline Smith Machine Press',
    aliases: ['Incline Smith press', 'Smith machine incline bench press'],
    kind: 'strength',
    purpose:
      'Builds the upper chest and the front of the shoulders with a bar that runs on fixed rails. You can press a heavy load at an incline on your own, because the safety stops catch the bar if a rep stalls.',
    equipment: ['Smith machine with safety stops', 'Adjustable bench set to 30 to 40 degrees'],
    setup: [
      'Set the bench to 30 to 40 degrees and roll it under the Smith bar so the bar comes straight down onto your upper chest.',
      'Set the safety stops at the height where the bar sits just above your chest when you lie back. A stalled rep then rests on the stops, not on you.',
      'Sit back with your feet flat and grip the bar a little wider than shoulder width.',
      'Pull your shoulder blades back and down so your upper back feels tight on the pad.',
      'Practise turning the bar off and back onto the hooks with an empty bar first.',
    ],
    steps: [
      'Turn the bar off the hooks and hold it with straight arms.',
      'Lower the bar straight down to your upper chest, just below the collarbones.',
      'Keep your elbows angled partway between your sides and straight out.',
      'Touch the chest lightly and pause. Do not bounce.',
      'Press straight up until your arms are straight. After the last rep, turn the bar back onto the hooks.',
    ],
    breathing:
      'Breathe in and brace before you lower the bar. Hold it through the bottom, then breathe out as the bar passes the hardest part of the press.',
    tempo: '3 1 1 0 means three seconds down, a one second pause on the upper chest, one second up, and no rest at the top.',
    rangeOfMotion:
      'Lower until the bar lightly touches your upper chest, then press to straight arms. The bar moves in a straight vertical line, so the bench position decides where it lands.',
    muscles: {
      primary: ['pec_clavicular', 'delt_anterior'],
      secondary: ['triceps', 'pec_sternal'],
    },
    emphasisNote:
      'The incline biases the upper chest and the front of the shoulder, and the middle chest and triceps still do a large share of the work. A bench much steeper than 40 degrees hands more of the press to the shoulders. The rails take balance out of the lift, so you can focus on a slow, deep lowering, and machine and free weight pressing build muscle about equally (Haugen 2023).',
    movementPattern: 'horizontal_push',
    joints: ['Shoulder', 'Elbow', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder', 'elbow'],
    commonMistakes: [
      'Placing the bench so the bar lands on the neck or the middle of the chest.',
      'Skipping the safety stops, or setting them too low to catch a stalled rep.',
      'Setting the bench so steep that it turns into a shoulder press.',
      'Bouncing the bar off the chest.',
      'Lifting the hips off the seat to finish a rep.',
    ],
    goodFormFeels:
      'The bar glides in a straight line, your upper back stays tight on the pad, and the work sits in the upper chest and the front of the shoulders without any pinching.',
    stopRules: ['Stop the set when the bar slows sharply or your hips lift off the seat.', EFFORT_RULE.last, PAIN_RULE],
    safetyNotes: [
      'Set the safety stops before the first set, every time. You train alone, so they are your spotter.',
      'If a rep stalls, lower the bar under control onto the stops, then slide out from under it.',
      'Turn the bar fully onto the hooks and check that it is caught before you let go.',
      'Your shoulders also work in spiking and swimming. Keep the incline at 40 degrees or lower and stop the set at any pinch.',
    ],
    easierSubstitution: {
      exerciseId: 'incline-machine-press',
      name: 'Incline Machine Chest Press',
      reason: 'The handles move on a fixed path with no hooks or stops to set, so there is less to manage.',
    },
    equipmentSubstitution: {
      exerciseId: 'incline-dumbbell-press',
      name: 'Incline Dumbbell Press',
      reason: 'Use when the Smith machine is busy. Stop one rep earlier, because heavy dumbbells are harder to escape alone.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'smith-bench-press',
        name: 'Smith Machine Bench Press',
        reason: 'Use when no incline bench fits under the bar. The flat angle shifts the bias toward the middle chest.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'last',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Low incline under the Smith bar, safety stop set just above the chest, arms straight.',
          ...INCLINE,
          armNear: [167, 167],
          props: [...SMITH_INCLINE_PROPS, { type: 'barbell', at: 'hands' }],
        },
        {
          label: 'Bottom',
          caption: 'Lower the bar straight down the rail to the upper chest, just above the stops.',
          ...INCLINE,
          armNear: [25, 180],
          props: [...SMITH_INCLINE_PROPS, { type: 'barbell', at: 'hands' }, { type: 'arrow', from: [124, 46], to: [124, 80] }],
        },
        {
          label: 'Finish',
          caption: 'Press straight up along the rail until the arms are straight.',
          ...INCLINE,
          armNear: [167, 167],
          props: [...SMITH_INCLINE_PROPS, { type: 'barbell', at: 'hands' }, { type: 'arrow', from: [124, 80], to: [124, 46] }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Dumbbell Bench Press
  {
    id: 'dumbbell-bench-press',
    name: 'Dumbbell Bench Press',
    aliases: ['Flat dumbbell press', 'Flat dumbbell bench press'],
    kind: 'strength',
    purpose:
      'Builds the middle and lower chest, with help from the triceps and front shoulders. Dumbbells let each arm lower a little deeper than a bar would, so the chest works through a long stretch, and each side has to carry its own load.',
    equipment: ['A pair of dumbbells', 'Flat bench'],
    setup: [
      'Sit on the end of a flat bench with the dumbbells standing on your thighs, close to your knees.',
      'Lie back, and as you go, drive one knee up under each dumbbell to help bring them to the sides of your chest.',
      'Press the dumbbells up over your chest. Keep your feet flat and your head, upper back, and hips on the bench.',
      'Pull your shoulder blades back and down so your chest feels high.',
    ],
    steps: [
      'Start with straight arms over your chest, palms facing forward or slightly in.',
      'Lower both dumbbells slowly to the sides of your chest, elbows angled partway between your sides and straight out.',
      'Stop when you feel a deep stretch across the chest, with the upper arms a little below the bench, and pause.',
      'Press back up and slightly in until the dumbbells are over your chest again.',
      'After the last rep, bring the dumbbells to your chest, lift your knees to meet them, and rock up to sitting with the dumbbells on your thighs.',
    ],
    breathing: 'Breathe in as you lower the dumbbells. Breathe out as you press up through the hardest part.',
    tempo: '3 1 1 0 means three seconds down, a one second pause in the stretch, one second up, and no rest at the top.',
    rangeOfMotion:
      'From straight arms over your chest down to a deep, comfortable stretch at the sides of the chest. Your shoulders stay pulled back on the bench, so the dumbbells never drop so low that the shoulders roll forward.',
    muscles: {
      primary: ['pec_sternal'],
      secondary: ['triceps', 'delt_anterior', 'pec_clavicular'],
    },
    emphasisNote:
      'A flat bench biases the middle and lower chest. The triceps and front shoulders help through the whole press, and the upper chest still works. The extra depth that dumbbells allow loads the chest at a long muscle length, which is linked to good muscle growth.',
    movementPattern: 'horizontal_push',
    joints: ['Shoulder', 'Elbow', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder', 'elbow'],
    commonMistakes: [
      'Dropping the dumbbells out to the sides from straight arms after the last rep.',
      'Flaring the elbows straight out to the sides.',
      'Clanking the dumbbells together at the top, which takes the tension off the chest.',
      'Lowering so deep that the shoulders roll forward off the bench.',
      'Lifting the hips off the bench to finish a rep.',
    ],
    goodFormFeels:
      'A long stretch across the chest at the bottom, a smooth press up, and shoulders that stay pinned back on the bench.',
    stopRules: ['Stop the set when a dumbbell wobbles, slows sharply, or drifts off its path.', EFFORT_RULE.never, PAIN_RULE],
    safetyNotes: [
      'You train alone, and nobody can take the dumbbells from you if a rep stalls. Always stop with at least one clean rep left.',
      'Get in and out of position with your knees helping, as in the setup. Never drop heavy dumbbells to the sides from straight arms.',
      'Your shoulders also work in spiking and swimming. Stop the set if the front of the shoulder pinches.',
    ],
    easierSubstitution: {
      exerciseId: 'machine-bench-press',
      name: 'Machine Bench Press',
      reason: 'The machine guides the path, so there is nothing to balance and nothing to put down after the set.',
    },
    equipmentSubstitution: {
      exerciseId: 'smith-bench-press',
      name: 'Smith Machine Bench Press',
      reason: 'Use when no dumbbells in the right weight are free. The safety stops make it safe to press hard alone.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'incline-dumbbell-press',
        name: 'Incline Dumbbell Press',
        reason: 'The same dumbbells on a low incline, which shifts the bias toward the upper chest.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'never',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Lie on the bench with the feet flat and the dumbbells straight over the chest.',
          ...LYING,
          armNear: [170, 172],
          props: [FLAT_BENCH, { type: 'dumbbell', at: 'hands' }],
        },
        {
          label: 'Bottom',
          caption: 'Lower slowly to the sides of the chest. The elbows sink below the bench into a deep stretch.',
          ...LYING,
          armNear: [34, 178],
          props: [FLAT_BENCH, { type: 'dumbbell', at: 'hands' }, { type: 'arrow', from: [128, 62], to: [128, 94] }],
        },
        {
          label: 'Finish',
          caption: 'Press back up and slightly in until the dumbbells are over the chest.',
          ...LYING,
          armNear: [170, 172],
          props: [FLAT_BENCH, { type: 'dumbbell', at: 'hands' }, { type: 'arrow', from: [128, 94], to: [128, 62] }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Smith Machine Bench Press
  {
    id: 'smith-bench-press',
    name: 'Smith Machine Bench Press',
    aliases: ['Smith bench press', 'Flat Smith press'],
    kind: 'strength',
    purpose:
      'Builds the middle and lower chest, the triceps, and the front shoulders with a bar that runs on fixed rails. With the safety stops set, you can press a heavy load on your own without a spotter.',
    equipment: ['Smith machine with safety stops', 'Flat bench'],
    setup: [
      'Roll a flat bench under the Smith bar so the bar comes straight down onto the middle of your chest.',
      'Set the safety stops at the height where the bar sits just above your chest when you lie flat. A stalled rep then rests on the stops, not on you.',
      'Lie back with your feet flat and grip the bar a little wider than shoulder width.',
      'Pull your shoulder blades back and down so your upper back feels tight on the bench.',
    ],
    steps: [
      'Turn the bar off the hooks and hold it with straight arms.',
      'Lower the bar straight down to the middle of your chest, elbows angled partway between your sides and straight out.',
      'Touch the chest lightly and pause. Do not bounce.',
      'Press straight up until your arms are straight.',
      'After the last rep, turn the bar back onto the hooks before you let go.',
    ],
    breathing:
      'Breathe in and brace before you lower the bar. Hold it through the bottom, then breathe out as the bar passes the hardest part of the press.',
    tempo: '3 1 1 0 means three seconds down, a one second pause on the chest, one second up, and no rest at the top.',
    rangeOfMotion:
      'Lower until the bar lightly touches the middle of your chest, then press to straight arms. The bar moves in a straight vertical line, so the bench position decides where it lands.',
    muscles: {
      primary: ['pec_sternal'],
      secondary: ['triceps', 'delt_anterior', 'pec_clavicular'],
    },
    emphasisNote:
      'A flat bench biases the middle and lower chest, with the triceps and front shoulders helping in every rep and the upper chest still working. The rails take balance out of the lift, so you can focus on a slow lowering and a full range, and machine and free weight pressing build muscle about equally (Haugen 2023).',
    movementPattern: 'horizontal_push',
    joints: ['Shoulder', 'Elbow', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder', 'elbow'],
    commonMistakes: [
      'Placing the bench so the bar lands on the neck or the belly.',
      'Skipping the safety stops, or setting them too low to catch the bar.',
      'Bouncing the bar off the chest.',
      'Flaring the elbows straight out to the sides.',
      'Lifting the hips off the bench to finish a rep.',
    ],
    goodFormFeels:
      'The bar glides in a straight line, your upper back stays pinned to the bench, and the effort sits across the chest and the backs of the arms.',
    stopRules: ['Stop the set when the bar slows sharply or your hips lift off the bench.', EFFORT_RULE.last, PAIN_RULE],
    safetyNotes: [
      'Set the safety stops before the first set, every time. You train alone, so they are your spotter.',
      'If a rep stalls, lower the bar under control onto the stops, then slide out from under it.',
      'Practise turning the bar on and off the hooks with an empty bar, and check that it is caught before you let go.',
    ],
    easierSubstitution: {
      exerciseId: 'machine-bench-press',
      name: 'Machine Bench Press',
      reason: 'The handles move on a fixed path with no hooks or stops to set, so there is less to manage.',
    },
    equipmentSubstitution: {
      exerciseId: 'dumbbell-bench-press',
      name: 'Dumbbell Bench Press',
      reason: 'Use when the Smith machine is busy. Stop one rep earlier, because heavy dumbbells are harder to escape alone.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'incline-smith-press',
        name: 'Incline Smith Machine Press',
        reason: 'The same machine on a low incline, which shifts the bias toward the upper chest.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'last',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Lie under the Smith bar, safety stop set just above the chest, arms straight.',
          ...LYING,
          armNear: [161, 161],
          props: [...SMITH_FLAT_PROPS, { type: 'barbell', at: 'hands' }],
        },
        {
          label: 'Bottom',
          caption: 'Lower the bar straight down the rail to the middle of the chest, just above the stops.',
          ...LYING,
          armNear: [38, 180],
          props: [...SMITH_FLAT_PROPS, { type: 'barbell', at: 'hands' }, { type: 'arrow', from: [128, 62], to: [128, 94] }],
        },
        {
          label: 'Finish',
          caption: 'Press straight up along the rail with the hips and upper back still on the bench.',
          ...LYING,
          armNear: [161, 161],
          props: [...SMITH_FLAT_PROPS, { type: 'barbell', at: 'hands' }, { type: 'arrow', from: [128, 94], to: [128, 62] }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Pec Deck Fly
  {
    id: 'pec-deck-fly',
    name: 'Pec Deck Fly',
    aliases: ['Machine chest fly', 'Pec deck'],
    kind: 'strength',
    purpose:
      'Trains the chest through a wide arc into a deep stretch, on a fixed path with steady tension. It adds chest work with very little load on the triceps or elbows, and the machine keeps every rep safe when you train alone.',
    equipment: ['Pec deck machine with handles or arm pads'],
    setup: [
      'Set the seat so the handles are at mid chest height when you sit tall.',
      'Set the handle start position so your arms open to a good chest stretch, with the hands about in line with your body and no further back.',
      'Sit with your back and head against the pad and your feet flat on the floor.',
      'Hold the handles with a slight bend in the elbows, then pull your shoulder blades back and down.',
    ],
    steps: [
      'Keeping the same slight elbow bend, bring the handles together in a wide arc in front of your chest.',
      'Squeeze your chest for a moment when the hands are close together.',
      'Open your arms slowly out to the sides until you feel a deep stretch across the chest.',
      'Keep your shoulder blades pulled back so the shoulders do not roll forward in the stretch.',
      'Pause briefly in the stretch, then bring the handles together again.',
    ],
    breathing: 'Breathe out as you bring the handles together. Breathe in as your arms open.',
    tempo:
      '3 1 1 1 means three seconds opening the arms, a one second pause in the stretch, one second to bring the handles together, and a one second squeeze in front of the chest.',
    rangeOfMotion:
      'Open until your hands are about in line with your body, or a little behind if the shoulders stay back on the pad. Bring the handles together until they nearly touch in front of your chest.',
    muscles: {
      primary: ['pec_sternal'],
      secondary: ['pec_clavicular', 'delt_anterior'],
    },
    emphasisNote:
      'With the handles at mid chest height, the fly biases the middle and lower chest, with help from the upper chest and front shoulders. The wide open position works the chest at a long muscle length, and training at long lengths like this is linked to good growth. No part of the chest switches off.',
    movementPattern: 'shoulder_horizontal_adduction',
    joints: ['Shoulder', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder'],
    commonMistakes: [
      'Letting the shoulders roll forward off the pad in the stretch.',
      'Bending and straightening the elbows so the fly turns into a press.',
      'Setting the seat so the handles are at the neck or the belly.',
      'Letting the weight crash at the open position.',
      'Opening so far that you feel strain in the front of the shoulder instead of a stretch across the chest.',
    ],
    goodFormFeels:
      'A deep, even stretch across the chest when the arms are open, a firm squeeze in the middle of the chest when the hands meet, and elbows that keep the same bend.',
    stopRules: [
      'Stop the set when the shoulders roll forward or the elbows start bending and straightening.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Control the stretch on every rep. The open position is where the shoulder is most exposed.',
      'Your shoulders also work in spiking and swimming. Shorten the stretch if the front of the shoulder aches.',
    ],
    easierSubstitution: {
      exerciseId: 'machine-bench-press',
      name: 'Machine Bench Press',
      reason: 'Trains the same chest muscles with a shorter reach, if the wide open position bothers your shoulder.',
    },
    equipmentSubstitution: {
      exerciseId: 'standing-cable-crossover',
      name: 'Standing Cable Crossover',
      reason: 'Use two cables when the machine is taken. The arc and the stretch are much the same.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'flat-cable-fly',
        name: 'Flat Cable Fly',
        reason: 'Lying on a bench between two low pulleys keeps tension on deep in the stretch.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Front view. Sit tall against the pad, arms open wide on the handles at mid chest height.',
          ...FRONT_SEATED,
          armNear: [80, 92],
          armFar: [-80, -92],
          props: [...PEC_DECK_PROPS, { type: 'handle', at: 'nearHand' }, { type: 'handle', at: 'farHand' }],
        },
        {
          label: 'In',
          caption: 'Front view. Keep the elbow bend and squeeze the handles together in front of the chest.',
          ...FRONT_SEATED,
          armNear: [70, -72],
          armFar: [-70, 72],
          props: [
            ...PEC_DECK_PROPS,
            { type: 'handle', at: 'nearHand' },
            { type: 'handle', at: 'farHand' },
            { type: 'arrow', from: [156, 92], to: [128, 92] },
            { type: 'arrow', from: [44, 92], to: [72, 92] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Front view. Open the arms slowly into a deep chest stretch, shoulders kept back.',
          ...FRONT_SEATED,
          armNear: [80, 92],
          armFar: [-80, -92],
          props: [
            ...PEC_DECK_PROPS,
            { type: 'handle', at: 'nearHand' },
            { type: 'handle', at: 'farHand' },
            { type: 'arrow', from: [128, 84], to: [156, 84] },
            { type: 'arrow', from: [72, 84], to: [44, 84] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Standing Cable Crossover
  {
    id: 'standing-cable-crossover',
    name: 'Standing Cable Crossover',
    aliases: ['Cable crossover', 'High to low cable fly'],
    kind: 'strength',
    purpose:
      'Trains the chest with two cables that keep tension on from the deep stretch to the squeeze. Pulling from pulleys a little above the shoulders down to the lower chest biases the middle and lower chest.',
    equipment: ['Cable crossover station with two adjustable pulleys', 'Two D handles'],
    setup: [
      'Set both pulleys at shoulder height or a little higher and attach a D handle to each.',
      'Take a handle in each hand, step forward between the towers until the cables have tension, and bring your hands together in front of your lower chest.',
      'Stand in a staggered stance, one foot a step ahead, with a slight forward lean from the hips.',
      'Soften your elbows and pull your shoulder blades back and down.',
    ],
    steps: [
      'Let your arms open wide until your hands are just behind the line of your body and your chest stretches.',
      'Keeping the same elbow bend, sweep the handles down and forward in a wide arc.',
      'Bring your hands together in front of your lower chest and squeeze for a moment.',
      'Let your arms open slowly back into the stretch without the shoulders rolling forward.',
      'Keep your trunk still, and swap the front foot between sets.',
    ],
    breathing: 'Breathe out as your hands come together. Breathe in as your arms open.',
    tempo:
      '3 1 1 1 means three seconds opening the arms, a one second pause in the stretch, one second to bring the hands together, and a one second squeeze.',
    rangeOfMotion:
      'Open until your hands are just behind your body line with the shoulders still pulled back, then bring the hands together in front of your lower chest.',
    muscles: {
      primary: ['pec_sternal'],
      secondary: ['pec_clavicular', 'delt_anterior'],
    },
    emphasisNote:
      'Pulling from high to low, with the hands meeting at the lower chest, biases the middle and lower chest. Low pulleys with the hands meeting at the upper chest would tilt the work toward the upper chest. Unlike dumbbells, the cables keep the chest loaded through the whole arc, including the deep stretch and the squeeze.',
    movementPattern: 'shoulder_horizontal_adduction',
    joints: ['Shoulder', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder'],
    commonMistakes: [
      'Bending and straightening the elbows so the fly turns into a press.',
      'Leaning far forward and using body weight to pull the handles down.',
      'Letting the cables yank the arms back so the shoulders roll forward.',
      'Standing so far forward that the arms are pulled well behind you before the set starts.',
    ],
    goodFormFeels:
      'A deep stretch across the chest with the arms open, steady tension the whole way, and a firm squeeze in the lower chest as the hands meet.',
    stopRules: [
      'Stop the set when the elbows start bending and straightening or your trunk starts rocking.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'At the end of the set, bring your hands together and step back toward the towers before you let the handles go, so the cables never pull your arms back.',
      'Your shoulders also work in spiking and swimming. Shorten the stretch if the front of the shoulder aches.',
    ],
    easierSubstitution: {
      exerciseId: 'flat-cable-fly',
      name: 'Flat Cable Fly',
      reason: 'Lying on a bench holds your body still, so you only have to think about the arc.',
    },
    equipmentSubstitution: {
      exerciseId: 'pec-deck-fly',
      name: 'Pec Deck Fly',
      reason: 'Use when the cable station is busy. The machine moves your arms through the same arc on a fixed path.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'dumbbell-bench-press',
        name: 'Dumbbell Bench Press',
        reason: 'A pressing option for the same chest muscles when neither the cables nor the pec deck are free.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Front view. Stand between the towers with the hands together in front of the lower chest.',
          ...FRONT,
          armNear: [62, -62],
          armFar: [-62, 62],
          props: [
            ...CROSSOVER_POSTS,
            { type: 'cable', from: 'nearHand', to: [188, 30] },
            { type: 'cable', from: 'farHand', to: [12, 30] },
            { type: 'handle', at: 'nearHand' },
            { type: 'handle', at: 'farHand' },
          ],
        },
        {
          label: 'Stretch',
          caption: 'Front view. Let the arms open wide and slightly up toward the pulleys until the chest stretches.',
          ...FRONT,
          armNear: [96, 100],
          armFar: [-96, -100],
          props: [
            ...CROSSOVER_POSTS,
            { type: 'cable', from: 'nearHand', to: [188, 30] },
            { type: 'cable', from: 'farHand', to: [12, 30] },
            { type: 'handle', at: 'nearHand' },
            { type: 'handle', at: 'farHand' },
            { type: 'arrow', from: [124, 70], to: [152, 52] },
            { type: 'arrow', from: [76, 70], to: [48, 52] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Front view. Sweep the handles down and in until the hands meet in front of the lower chest.',
          ...FRONT,
          armNear: [62, -62],
          armFar: [-62, 62],
          props: [
            ...CROSSOVER_POSTS,
            { type: 'cable', from: 'nearHand', to: [188, 30] },
            { type: 'cable', from: 'farHand', to: [12, 30] },
            { type: 'handle', at: 'nearHand' },
            { type: 'handle', at: 'farHand' },
            { type: 'arrow', from: [152, 52], to: [128, 72] },
            { type: 'arrow', from: [48, 52], to: [72, 72] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Machine Lateral Raise
  {
    id: 'machine-lateral-raise',
    name: 'Machine Lateral Raise',
    aliases: ['Seated lateral raise machine', 'Lateral raise machine'],
    kind: 'strength',
    purpose:
      'Builds the side of the shoulder on a guided path. The pads push on your upper arms, so a tired grip never ends the set early, and many machines keep tension on low in the lift, where dumbbells feel light.',
    equipment: ['Seated lateral raise machine'],
    setup: [
      'Set the seat so your shoulders line up with the machine pivots, often marked with a dot.',
      'Sit tall with your feet flat on the floor and your back or chest against the pad, depending on the machine.',
      'Place the pads on the outside of your upper arms, just above the elbows, and hold the handles lightly.',
      'Set your shoulders down away from your ears.',
    ],
    steps: [
      'Raise your arms out to the sides, leading with your elbows.',
      'Stop at about shoulder height, with the elbows level with the shoulders.',
      'Pause briefly without shrugging.',
      'Lower slowly until your arms are back at your sides, keeping a little tension on the pads.',
    ],
    breathing: 'Breathe out as you raise. Breathe in as you lower.',
    tempo: '3 0 1 1 means three seconds down, no pause at the bottom, one second up, and a one second hold at shoulder height.',
    rangeOfMotion:
      'Raise from your sides to about shoulder height. Going higher mostly brings in the upper traps. At the bottom, stop just before the weight rests.',
    muscles: {
      primary: ['delt_lateral'],
      secondary: ['traps_upper', 'rotator_cuff'],
    },
    emphasisNote:
      'Raising the arms out to the sides biases the side of the shoulder. The supraspinatus of the rotator cuff helps start the lift, and the upper traps help near the top, more so if you shrug. With the pads on the upper arms, the forearms and grip do very little, so the side of the shoulder decides when the set ends.',
    movementPattern: 'shoulder_abduction',
    joints: ['Shoulder', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder'],
    commonMistakes: [
      'Shrugging the shoulders toward the ears.',
      'Sitting so the shoulders do not line up with the machine pivots.',
      'Raising the arms well above shoulder height.',
      'Letting the weight crash at the bottom.',
      'Pulling with the hands instead of lifting through the elbows.',
    ],
    goodFormFeels:
      'A growing burn on the sides of the shoulders, a relaxed neck, and a smooth arc that the pads follow without slipping.',
    stopRules: ['Stop the set when you start shrugging or the arms stop short of shoulder height.', EFFORT_RULE.all, PAIN_RULE],
    safetyNotes: [
      'Light to moderate weights work well here. The side of the shoulder is a small muscle that responds well to smooth reps.',
      'Your shoulders also work in spiking and swimming. Stop the set if you feel a pinch at the top of the shoulder.',
    ],
    easierSubstitution: {
      exerciseId: 'lateral-raise',
      name: 'Lateral Raise',
      reason: 'Light dumbbells need no setup and are simple to learn.',
    },
    equipmentSubstitution: {
      exerciseId: 'single-arm-cable-lateral-raise',
      name: 'Single Arm Cable Lateral Raise',
      reason: 'Use a cable when the machine is busy. The cable also keeps tension on at the bottom of the lift.',
    },
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Front view. Sit tall with the arms at your sides and the pads on the outside of the upper arms.',
          ...FRONT_SEATED,
          armNear: [26, 14],
          armFar: [-26, -14],
          props: [...FRONT_SEAT, ...LATERAL_PADS_DOWN],
        },
        {
          label: 'Top',
          caption: 'Front view. Lead with the elbows and raise the arms out to the sides to shoulder height.',
          ...FRONT_SEATED,
          armNear: [86, 92],
          armFar: [-86, -92],
          props: [...FRONT_SEAT, ...LATERAL_PADS_UP, { type: 'arrow', from: [172, 96], to: [172, 62] }],
        },
        {
          label: 'Finish',
          caption: 'Front view. Lower slowly back to your sides without letting the weight rest.',
          ...FRONT_SEATED,
          armNear: [26, 14],
          armFar: [-26, -14],
          props: [...FRONT_SEAT, ...LATERAL_PADS_DOWN, { type: 'arrow', from: [172, 62], to: [172, 96] }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Seated Dumbbell Overhead Triceps Extension
  {
    id: 'dumbbell-overhead-triceps-extension',
    name: 'Seated Dumbbell Overhead Triceps Extension',
    aliases: ['Seated overhead dumbbell extension', 'Seated two hand dumbbell extension'],
    kind: 'strength',
    purpose:
      'Builds the triceps with the arms overhead, which lengthens the long head of the triceps. Sitting against a pad keeps your trunk still so the triceps do the work, and one dumbbell is all you need.',
    equipment: ['One dumbbell', 'Adjustable bench set upright'],
    setup: [
      'Set an adjustable bench fully upright. Sit so the pad supports your lower and middle back and there is room for the dumbbell behind your head.',
      'Sit with your feet flat and a little wide for balance.',
      'Stand the dumbbell on your thigh, lift it to your shoulder, then press it overhead with both hands.',
      'Cup the top plate with both palms, thumbs wrapped around the handle, arms straight overhead.',
    ],
    steps: [
      'Point your elbows up and keep your upper arms close to your head.',
      'Bend your elbows slowly to lower the dumbbell behind your head.',
      'Go down into a deep stretch along the backs of your upper arms, as far as your shoulders and elbows stay comfortable, and pause.',
      'Straighten your elbows to raise the dumbbell back overhead, without letting the elbows flare out.',
      'Keep your ribs down and your back on the pad the whole time.',
    ],
    breathing: 'Breathe in as you lower the dumbbell. Breathe out as you straighten your arms.',
    tempo: '3 1 1 0 means three seconds down, a one second pause in the stretch, one second up, and no rest at the top.',
    rangeOfMotion:
      'From straight arms overhead down to a deep elbow bend with the dumbbell behind your head. Stop the stretch where your shoulders and elbows still feel comfortable.',
    muscles: {
      primary: ['triceps'],
      secondary: [],
    },
    emphasisNote:
      'The long head of the triceps crosses the shoulder joint, so raising the arms overhead lengthens it and gives it a bigger share of the work, especially in the stretch. In one 12 week study (Maeo 2023), training in this overhead position gave about 1.4 times more triceps growth than pushdowns. The lateral and medial heads still straighten the elbow in every rep.',
    movementPattern: 'elbow_extension',
    joints: ['Elbow', 'Shoulder'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['elbow', 'shoulder'],
    commonMistakes: [
      'Letting the elbows flare out wide.',
      'Arching the lower back away from the pad.',
      'Moving the upper arms forward and back so the shoulders do the work.',
      'Rushing through the stretch at the bottom.',
      'Choosing a dumbbell too heavy to control behind your head.',
    ],
    goodFormFeels:
      'A strong stretch along the backs of the upper arms at the bottom, a firm squeeze at straight arms, and a steady trunk against the pad.',
    stopRules: [
      'Stop the set when the elbows flare, your back arches off the pad, or the dumbbell feels unsteady behind your head.',
      EFFORT_RULE.never,
      PAIN_RULE,
    ],
    safetyNotes: [
      'A stalled rep behind your head is hard to escape when you train alone. Always stop with at least one clean rep left.',
      'After the last rep, bring the dumbbell down to your shoulder and then to your thigh before you stand up.',
      'Holding the arms overhead also loads the shoulder, which already works in spiking and swimming. If the shoulder pinches, do pushdowns instead that day.',
    ],
    easierSubstitution: {
      exerciseId: 'triceps-pushdown',
      name: 'Triceps Pushdown',
      reason: 'Arms at your sides are easier on the shoulder, and there is no weight to control behind your head.',
    },
    equipmentSubstitution: {
      exerciseId: 'rope-overhead-triceps-extension',
      name: 'Rope Overhead Triceps Extension',
      reason: 'The same overhead position on a cable, which keeps tension on in the stretch.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'single-arm-cable-overhead-extension',
        name: 'Single Arm Cable Overhead Triceps Extension',
        reason: 'One arm at a time on a cable, so each side works through its own full range.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'never',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Sit against the upright pad and hold one dumbbell straight overhead with both hands.',
          ...UPRIGHT,
          armNear: [182, 182],
          props: [...UPRIGHT_PROPS, { type: 'dumbbell', at: 'hands' }],
        },
        {
          label: 'Stretch',
          caption: 'Elbows point up as you lower the dumbbell behind the head into a deep stretch.',
          ...UPRIGHT,
          armNear: [185, -45],
          props: [...UPRIGHT_PROPS, { type: 'dumbbell', at: 'hands' }, { type: 'arrow', from: [112, 34], to: [112, 66] }],
        },
        {
          label: 'Finish',
          caption: 'Straighten the elbows to raise the dumbbell back overhead. Upper arms stay still.',
          ...UPRIGHT,
          armNear: [182, 182],
          props: [...UPRIGHT_PROPS, { type: 'dumbbell', at: 'hands' }, { type: 'arrow', from: [112, 66], to: [112, 34] }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Single Arm Cable Overhead Triceps Extension
  {
    id: 'single-arm-cable-overhead-extension',
    name: 'Single Arm Cable Overhead Triceps Extension',
    aliases: ['One arm overhead cable extension', 'Single arm overhead cable extension'],
    kind: 'strength',
    purpose:
      'Builds the triceps with the arm overhead, which lengthens the long head. The cable keeps tension on deep in the stretch, and one arm at a time lets each side move through its own full range.',
    equipment: ['Cable pulley', 'Single D handle'],
    setup: [
      'Set the pulley low or at about chest height and attach a single handle.',
      'Take the handle in one hand, turn to face away from the machine, and bring the handle up behind your head.',
      'Step forward into a small split stance so the cable has tension, and lean your trunk forward slightly.',
      'Point the working elbow up with the upper arm beside your ear. Rest your free hand on your hip.',
    ],
    steps: [
      'Start with the elbow deeply bent and the hand behind your head.',
      'Straighten your elbow to push the handle up and forward.',
      'Keep your upper arm beside your ear and still.',
      'Finish with a straight arm and squeeze briefly.',
      'Bend your elbow slowly to let the handle return behind your head into a deep stretch, then pause.',
      'Finish all reps on one side, then switch.',
    ],
    breathing: 'Breathe out as you straighten your arm. Breathe in as the handle returns.',
    tempo:
      '3 1 1 0 means three seconds to bend the elbow, a one second pause in the stretch, one second to straighten, and no rest at the finish.',
    rangeOfMotion:
      'Go from a deep elbow bend with the hand behind your head to a straight arm. Stop the stretch where your shoulder and elbow still feel comfortable.',
    muscles: {
      primary: ['triceps'],
      secondary: [],
    },
    emphasisNote:
      'The long head of the triceps crosses the shoulder joint, so an arm beside your ear lengthens it and gives it a larger share of the work, especially in the stretch. In one 12 week study (Maeo 2023), training in this overhead position gave about 1.4 times more triceps growth than pushdowns. The lateral and medial heads still straighten the elbow in every rep.',
    movementPattern: 'elbow_extension',
    joints: ['Elbow', 'Shoulder'],
    laterality: 'unilateral',
    logSides: true,
    fatigueOverlap: ['elbow', 'shoulder'],
    commonMistakes: [
      'Letting the elbow drift out to the side.',
      'Arching the lower back instead of bracing.',
      'Moving the upper arm so the shoulder does the work.',
      'Rushing through the stretch at the bottom.',
    ],
    goodFormFeels:
      'A long stretch along the back of the upper arm when the hand is behind your head, a firm squeeze at a straight arm, and a trunk that stays still.',
    stopRules: ['Stop the set when the elbow drifts out or your lower back arches.', EFFORT_RULE.all, PAIN_RULE],
    safetyNotes: [
      'Start with your weaker arm, then match the reps on the other side.',
      'Holding the arm overhead also loads the shoulder, which already works in spiking and swimming. If it pinches, do pushdowns instead that day.',
    ],
    easierSubstitution: {
      exerciseId: 'single-arm-cable-pushdown',
      name: 'Single Arm Cable Pushdown',
      reason: 'With the arm at your side it is easier on the shoulder and simpler to set up.',
    },
    equipmentSubstitution: {
      exerciseId: 'dumbbell-overhead-triceps-extension',
      name: 'Seated Dumbbell Overhead Triceps Extension',
      reason: 'Use when no cable is free. One dumbbell held in both hands trains the same overhead position.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'rope-overhead-triceps-extension',
        name: 'Rope Overhead Triceps Extension',
        reason: 'Both arms together on a rope when you want to save time.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Split stance facing away from the pulley, upper arm beside the ear, hand behind the head.',
          ...OVERHEAD,
          armNear: [140, -80],
          armFar: [-62, 25],
          props: [OVERHEAD_POST, { type: 'cable', from: 'nearHand', to: [18, 64] }, { type: 'handle', at: 'nearHand' }],
        },
        {
          label: 'Extend',
          caption: 'Straighten the elbow to push the handle up and forward. The upper arm stays still.',
          ...OVERHEAD,
          armNear: [140, 140],
          armFar: [-62, 25],
          props: [
            OVERHEAD_POST,
            { type: 'cable', from: 'nearHand', to: [18, 64] },
            { type: 'handle', at: 'nearHand' },
            { type: 'arrow', from: [166, 52], to: [182, 26] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Bend the elbow slowly to let the handle return behind the head into a deep stretch.',
          ...OVERHEAD,
          armNear: [140, -80],
          armFar: [-62, 25],
          props: [
            OVERHEAD_POST,
            { type: 'cable', from: 'nearHand', to: [18, 64] },
            { type: 'handle', at: 'nearHand' },
            { type: 'arrow', from: [182, 26], to: [166, 52] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Single Arm Cable Pushdown
  {
    id: 'single-arm-cable-pushdown',
    name: 'Single Arm Cable Pushdown',
    aliases: ['One arm cable pushdown', 'Single arm triceps pressdown'],
    kind: 'strength',
    purpose:
      'Builds the triceps one arm at a time. You can line the cable up with your own arm, lock out fully, and make sure the weaker side does its full share of the work.',
    equipment: ['High cable pulley', 'Single D handle'],
    setup: [
      'Set the pulley at the top and attach a single handle.',
      'Stand facing the machine with the working hand in line with the pulley and a slight forward lean from the hips.',
      'Grip the handle with the palm facing down or facing in, and pin the elbow at your side.',
      'Let the free arm hang, or rest that hand lightly on the machine.',
    ],
    steps: [
      'Push the handle down by straightening your elbow.',
      'Keep the upper arm still, with the elbow pinned at your side.',
      'Lock the arm out fully and squeeze the back of the arm for a moment.',
      'Let the handle rise slowly until your forearm passes level with the floor.',
      'Finish all reps on one side, then switch.',
    ],
    breathing: 'Breathe out as you push down. Breathe in as the handle rises.',
    tempo: '3 0 1 1 means three seconds up, no pause at the top, one second down, and a one second squeeze at full lockout.',
    rangeOfMotion:
      'From the forearm a little above level with the floor down to a fully straight arm. The elbow stays at your side the whole way.',
    muscles: {
      primary: ['triceps'],
      secondary: [],
    },
    emphasisNote:
      'With the arm at your side, the lateral and medial heads of the triceps tend to do a bit more than the long head. Letting the hand rise past level with the floor adds a little stretch, and the full lockout trains the triceps where they are shortest. All three heads straighten the elbow in every rep, and pairing this with an overhead extension gives the long head its stretch too.',
    movementPattern: 'elbow_extension',
    joints: ['Elbow'],
    laterality: 'unilateral',
    logSides: true,
    fatigueOverlap: ['elbow'],
    commonMistakes: [
      'Letting the elbow drift forward so the shoulder helps.',
      'Leaning over the handle and pushing with body weight.',
      'Stopping short of a full lockout.',
      'Letting the handle fly up fast after each rep.',
    ],
    goodFormFeels:
      'The work stays in the back of the upper arm, the elbow feels pinned to your side, and the wrist stays straight.',
    stopRules: ['Stop the set when the elbow starts moving or you lean over the handle.', EFFORT_RULE.all, PAIN_RULE],
    safetyNotes: [
      'Start with your weaker arm, then match the reps on the other side.',
      'If the elbow aches after hitting practice, lower the weight and keep the reps smooth.',
    ],
    easierSubstitution: {
      exerciseId: 'triceps-pushdown',
      name: 'Triceps Pushdown',
      reason: 'Both arms share a bar or rope, which is simpler to learn and quicker to finish.',
    },
    equipmentSubstitution: {
      exerciseId: 'dumbbell-overhead-triceps-extension',
      name: 'Seated Dumbbell Overhead Triceps Extension',
      reason: 'Use when no cable is free. It trains the triceps with one dumbbell, in the overhead position that stretches the long head.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'single-arm-cable-overhead-extension',
        name: 'Single Arm Cable Overhead Triceps Extension',
        reason: 'The same cable and handle with the arm overhead, for more long head stretch.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Elbow pinned at the side, slight forward lean, forearm a little above level with the floor.',
          ...PUSHDOWN,
          armNear: [10, 115],
          armFar: [-6, -2],
          props: [{ type: 'cable', from: 'nearHand', to: [122, 4] }, { type: 'handle', at: 'nearHand' }],
        },
        {
          label: 'Bottom',
          caption: 'Push down to a fully straight arm while the upper arm stays still.',
          ...PUSHDOWN,
          armNear: [10, 8],
          armFar: [-6, -2],
          props: [
            { type: 'cable', from: 'nearHand', to: [122, 4] },
            { type: 'handle', at: 'nearHand' },
            { type: 'arrow', from: [152, 62], to: [152, 96] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Let the handle rise slowly until the forearm passes level with the floor.',
          ...PUSHDOWN,
          armNear: [10, 115],
          armFar: [-6, -2],
          props: [
            { type: 'cable', from: 'nearHand', to: [122, 4] },
            { type: 'handle', at: 'nearHand' },
            { type: 'arrow', from: [152, 96], to: [152, 62] },
          ],
        },
      ],
    },
  },
];
