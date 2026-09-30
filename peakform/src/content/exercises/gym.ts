import type { ExerciseContent, Pose, PoseProp } from '../types';

// Gym exercises added when Tuesday and Friday became regular muscle building days.
// Order matches GYM_IDS in ids.ts. Each one fills a gap the other four gym days leave:
// upper chest with a free path, the mid back without lower back load, the long head of
// the biceps at long muscle length, quads without a bar on the spine, the lower back and
// glutes through hip extension, and the inner thigh.

const RIR_RULE = 'Stop when you reach the prescribed reps in reserve. Sets are not to failure.';
const RIR_RULE_SIDE = 'End the set on each leg when you reach the prescribed reps in reserve. Sets are not to failure.';
const PAIN_RULE =
  'Pain of 4 out of 10 or higher, or pain that worsens or changes your technique, pauses this exercise. Report it to a parent, coach, or clinician.';

type Base = Pick<Pose, 'trunk' | 'hip' | 'legNear' | 'legFar' | 'footX' | 'head'>;

/** Low incline bench, about 40 degrees, with a seat under the hips. */
const INCLINE: Base = { trunk: 230, hip: [122, 128], legNear: [83, -12] };
const INCLINE_PROPS: PoseProp[] = [
  { type: 'line', x1: 88, y1: 118, x2: 88, y2: 172 },
  { type: 'bench', x: 66, y: 94, w: 58, h: 8, angle: 40 },
  { type: 'bench', x: 100, y: 137, w: 40 },
];

/** Face down on an incline bench, feet on the floor behind. */
const PRONE: Base = { trunk: 130, head: 115, hip: [80, 92], legNear: [-15, 10] };
const PRONE_PROPS: PoseProp[] = [
  { type: 'line', x1: 100, y1: 88, x2: 100, y2: 172 },
  { type: 'bench', x: 82.6, y: 98.9, w: 55, h: 8, angle: -40 },
];

/** Leaning back on a steep incline bench, arms free to hang behind the body. */
const RECLINED: Base = { trunk: 212, hip: [110, 128], legNear: [83, -12] };
const RECLINED_PROPS: PoseProp[] = [
  { type: 'line', x1: 70, y1: 104, x2: 70, y2: 172 },
  { type: 'bench', x: 101, y: 130, w: 62, h: 8, angle: -122 },
  { type: 'bench', x: 92, y: 137, w: 40 },
];

/** Reclined in a 45 degree leg press, hands on the side handles. */
const LEG_PRESS = { trunk: 230, head: 215, hip: [72, 128] } satisfies Partial<Base>;
const LEG_PRESS_PROPS: PoseProp[] = [
  { type: 'bench', x: 65.6, y: 131.7, w: 58, h: 8, angle: -140 },
  { type: 'bench', x: 56, y: 138, w: 30 },
  { type: 'line', x1: 96, y1: 150, x2: 176, y2: 70 },
  { type: 'line', x1: 176, y1: 70, x2: 176, y2: 172 },
];

/** Hips on the pad of a 45 degree back extension bench, heels under the roller. */
const BACK_EXT: Base = { trunk: 135, hip: [98, 100], legNear: [-45, -45, 45] };
const BACK_EXT_PROPS: PoseProp[] = [
  { type: 'line', x1: 106, y1: 118, x2: 106, y2: 172 },
  { type: 'line', x1: 40, y1: 160, x2: 106, y2: 160 },
  { type: 'bench', x: 110.8, y: 97.8, w: 26, h: 10, angle: 135 },
  { type: 'bench', x: 30.2, y: 156.4, w: 20, h: 6, angle: 45 },
  { type: 'pad', x: 26, y: 146, w: 11, h: 11 },
];

/** Front view: standing beside a low pulley, cuff on the inside ankle. */
const ADDUCT = { trunk: 180, hip: [130, 89], legFar: [0, 0, -90] } satisfies Partial<Base>;
const ADDUCT_POST: PoseProp = { type: 'line', x1: 186, y1: 20, x2: 186, y2: 172 };

export const GYM_EXERCISES: ExerciseContent[] = [
  // ---------------------------------------------------------------- Incline Dumbbell Press
  {
    id: 'incline-dumbbell-press',
    name: 'Incline Dumbbell Press',
    aliases: ['Low incline dumbbell press'],
    kind: 'strength',
    purpose:
      'Builds the upper chest and the front of the shoulders. Dumbbells let each arm find its own path and lower a little deeper than a bar, which gives the chest a good stretch.',
    equipment: ['A pair of dumbbells', 'Adjustable bench set to a low incline'],
    setup: [
      'Set the bench to a low incline of about 30 degrees.',
      'Sit with the dumbbells standing on your thighs.',
      'Lie back and bring the dumbbells up to the sides of your chest in one smooth move, one knee helping each dumbbell up.',
      'Press them up over your shoulders. Feet flat, shoulder blades pulled back and down.',
    ],
    steps: [
      'Start with the arms straight over the shoulders and the palms facing forward or slightly in.',
      'Lower both dumbbells slowly to the sides of the upper chest, elbows angled partway between your sides and straight out.',
      'Stop when you feel a stretch across the chest and the upper arms are about level with the bench or a little below.',
      'Press back up and slightly in until the dumbbells are over the shoulders again.',
      'After the last rep, bring the dumbbells to the chest, then sit up with them on your thighs.',
    ],
    breathing: 'Breathe in as you lower the dumbbells. Breathe out as you press up through the hardest part.',
    tempo: '3 1 1 0 means three seconds down, a one second pause at the stretch, one second up, and no rest at the top.',
    rangeOfMotion:
      'From straight arms over the shoulders down to a comfortable stretch at the chest. The shoulders stay pulled back on the bench the whole time, and the dumbbells never drop so low that the shoulders roll forward.',
    muscles: {
      primary: ['pec_clavicular', 'delt_anterior'],
      secondary: ['triceps', 'pec_sternal'],
    },
    emphasisNote:
      'The low incline biases the upper chest and the front of the shoulder. The middle chest and triceps still share the work. A steeper bench hands more of it to the shoulders, so the bench stays low.',
    movementPattern: 'horizontal_push',
    joints: ['Shoulder', 'Elbow', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder', 'elbow'],
    commonMistakes: [
      'Setting the bench so steep that it becomes a shoulder press.',
      'Flaring the elbows straight out to the sides.',
      'Letting the dumbbells drift toward the face or the belly.',
      'Clanking the dumbbells together at the top, which takes the tension off the chest.',
      'Lowering so deep that the shoulders roll forward off the bench.',
    ],
    goodFormFeels:
      'A clear stretch across the upper chest at the bottom, a smooth press up, and shoulders that feel steady and never pinched.',
    stopRules: ['Stop the set when a dumbbell wobbles, slows sharply, or your technique changes.', RIR_RULE, PAIN_RULE],
    safetyNotes: [
      'Get in and out of position with the knees helping, as in the setup. Never drop heavy dumbbells to the sides from straight arms.',
      'Your shoulders also work in volleyball and swimming. Keep the incline low and stop the set at any pinch in the front of the shoulder.',
    ],
    easierSubstitution: {
      exerciseId: 'machine-bench-press',
      name: 'Machine Bench Press',
      reason: 'The machine guides the path, so there is nothing to balance.',
    },
    equipmentSubstitution: {
      exerciseId: 'incline-barbell-bench-press',
      name: 'Incline Barbell Bench Press',
      reason: 'Use when no dumbbells in the right weight are free. It needs safety arms or a spotter.',
    },
    otherSubstitutions: [
      {
        exerciseId: null,
        name: 'Incline machine press',
        reason: 'Same angle with a guided path when the bench is busy.',
      },
    ],
    loadIncrement: 'upper',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Lie back on a low incline, feet flat, dumbbells straight over the shoulders.',
          ...INCLINE,
          armNear: [180, 180],
          props: [...INCLINE_PROPS, { type: 'dumbbell', at: 'hands' }],
        },
        {
          label: 'Bottom',
          caption: 'Lower slowly to the sides of the upper chest until you feel a stretch.',
          ...INCLINE,
          armNear: [20, 178],
          props: [...INCLINE_PROPS, { type: 'dumbbell', at: 'hands' }, { type: 'arrow', from: [118, 46], to: [118, 80] }],
        },
        {
          label: 'Finish',
          caption: 'Press back up until the dumbbells are over the shoulders.',
          ...INCLINE,
          armNear: [180, 180],
          props: [...INCLINE_PROPS, { type: 'dumbbell', at: 'hands' }, { type: 'arrow', from: [118, 80], to: [118, 46] }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Chest Supported Dumbbell Row
  {
    id: 'chest-supported-dumbbell-row',
    name: 'Chest Supported Dumbbell Row',
    aliases: ['Incline dumbbell row', 'Seal row with dumbbells'],
    kind: 'strength',
    purpose:
      'Builds the middle of the back, the lats, and the back of the shoulders. The bench holds your chest, so the lower back rests while the upper back does all the pulling.',
    equipment: ['A pair of dumbbells', 'Adjustable bench set to about 30 to 45 degrees'],
    setup: [
      'Set the bench to about 30 to 45 degrees and put the dumbbells on the floor at the front of it.',
      'Lie face down with the chest on the pad and the top of the pad just below your collarbones.',
      'Feet on the floor behind you, or on the bench frame, legs firm.',
      'Pick up the dumbbells and let the arms hang straight down, palms facing each other.',
    ],
    steps: [
      'Let the shoulder blades move forward a little at the bottom, so the upper back gets a stretch.',
      'Pull both elbows up and back toward your hips, keeping the chest on the pad.',
      'Squeeze the shoulder blades together at the top for one second.',
      'Lower slowly until the arms are straight again.',
    ],
    breathing: 'Breathe out as you pull up. Breathe in as you lower.',
    tempo: '2 0 1 1 means two seconds down, no pause at the bottom, one second up, and a one second squeeze at the top.',
    rangeOfMotion:
      'From straight arms with the shoulder blades apart to elbows just past the body with the shoulder blades together. The chest stays on the pad and the neck stays long.',
    muscles: {
      primary: ['lats', 'traps_middle', 'rhomboids'],
      secondary: ['delt_posterior', 'teres_major', 'traps_lower', 'biceps', 'brachialis', 'brachioradialis'],
    },
    emphasisNote:
      'Elbows close to the sides and pulled toward the hips bias the lats. Elbows flared wider bias the upper back and the back of the shoulders. All of these muscles work in both versions.',
    movementPattern: 'horizontal_pull',
    joints: ['Shoulder', 'Elbow', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['wrist_grip', 'elbow'],
    commonMistakes: [
      'Lifting the chest off the pad to heave the weight up.',
      'Shrugging the shoulders up toward the ears.',
      'Cutting the lowering phase short so the back never gets its stretch.',
      'Craning the neck up to look forward.',
    ],
    goodFormFeels:
      'The chest stays glued to the pad, the upper back does the pulling, and you feel the squeeze between the shoulder blades at the top.',
    stopRules: ['Stop the set when the chest starts to lift off the pad or the reps get jerky.', RIR_RULE, PAIN_RULE],
    safetyNotes: [
      'Put the dumbbells down on the floor before you get off the bench.',
      'If the edge of the pad presses uncomfortably, move a little higher or lower on it.',
    ],
    easierSubstitution: {
      exerciseId: 'seated-cable-row',
      name: 'Seated Cable Row',
      reason: 'A steady cable pull with the feet braced, easy to set up and adjust.',
    },
    equipmentSubstitution: {
      exerciseId: 'leverage-high-row',
      name: 'Leverage High Row',
      reason: 'A chest supported machine row when no incline bench is free.',
    },
    otherSubstitutions: [
      {
        exerciseId: null,
        name: 'Chest supported T bar row',
        reason: 'The same idea on a machine with a chest pad, if the gym has one.',
      },
    ],
    loadIncrement: 'upper',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Chest on the incline pad, feet on the floor, arms hanging straight down.',
          ...PRONE,
          armNear: [0, 0],
          props: [...PRONE_PROPS, { type: 'dumbbell', at: 'hands' }],
        },
        {
          label: 'Top',
          caption: 'Pull the elbows up and back toward the hips and squeeze the shoulder blades together.',
          ...PRONE,
          armNear: [-62, 0],
          props: [...PRONE_PROPS, { type: 'dumbbell', at: 'hands' }, { type: 'arrow', from: [150, 116], to: [150, 90] }],
        },
        {
          label: 'Finish',
          caption: 'Lower slowly until the arms are straight. The chest stays on the pad.',
          ...PRONE,
          armNear: [0, 0],
          props: [...PRONE_PROPS, { type: 'dumbbell', at: 'hands' }, { type: 'arrow', from: [150, 90], to: [150, 116] }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Incline Dumbbell Curl
  {
    id: 'incline-dumbbell-curl',
    name: 'Incline Dumbbell Curl',
    aliases: ['Incline curl'],
    kind: 'strength',
    purpose:
      'Builds the biceps with the arms hanging behind the body, which puts the long head of the biceps on a stretch. Training a muscle at long lengths is a strong signal for growth.',
    equipment: ['A pair of light dumbbells', 'Adjustable bench set to about 45 to 60 degrees'],
    setup: [
      'Set the bench to about 45 to 60 degrees. Lower angles stretch more, so start higher if the front of the shoulder feels tight.',
      'Sit back with the head and upper back on the pad and the feet flat.',
      'Let the arms hang straight down beside the bench, palms facing forward.',
    ],
    steps: [
      'Keep the upper arms still, hanging straight down.',
      'Curl both dumbbells up by bending only at the elbows.',
      'Stop when the forearms are close to vertical, before the elbows move forward, and squeeze.',
      'Lower slowly all the way until the arms are straight again.',
    ],
    breathing: 'Breathe out as you curl up. Breathe in as you lower.',
    tempo: '3 0 1 1 means three seconds down, no pause at the bottom, one second up, and a one second squeeze at the top.',
    rangeOfMotion:
      'From straight arms, with a gentle stretch in the front of the upper arm, up to forearms near vertical. The elbows stay under the shoulders the whole time.',
    muscles: {
      primary: ['biceps'],
      secondary: ['brachialis', 'brachioradialis', 'forearm_flexors'],
    },
    emphasisNote:
      'With the arms behind the body, the long head of the biceps works from a longer length. The brachialis and forearms still help on every rep. It complements the preacher curl and the hammer curl from the other days.',
    movementPattern: 'elbow_flexion',
    joints: ['Elbow'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['elbow', 'wrist_grip'],
    commonMistakes: [
      'Swinging the elbows forward to finish the rep, which turns it into a front raise.',
      'Lifting the head and shoulders off the pad.',
      'Stopping short of straight arms at the bottom.',
      'Using dumbbells that are too heavy for a slow lowering.',
    ],
    goodFormFeels: 'A gentle stretch at the bottom, the work right in the front of the upper arm, and elbows that stay put.',
    stopRules: [
      'Stop the set when the elbows start to swing forward or the lowering speeds up.',
      RIR_RULE,
      PAIN_RULE,
      'A sharp pull in the front of the shoulder means the bench is too low. Raise it before the next set.',
    ],
    safetyNotes: [
      'Start lighter than your standing curl. The stretched position is much harder.',
      'Lower the dumbbells to the floor beside the bench before you sit up.',
    ],
    easierSubstitution: {
      exerciseId: 'machine-preacher-curl',
      name: 'Machine Preacher Curl',
      reason: 'The pad holds the upper arms, so the curl is easy to keep strict.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Cable curl facing away from the pulley',
      reason: 'Stand with the pulley behind you so the arm starts slightly behind the body, like on the bench.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'hammer-curl',
        name: 'Hammer Curl',
        reason: 'A standing curl with neutral palms when the bench is busy.',
      },
    ],
    loadIncrement: 'upper',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Lean back on a steep incline, arms hanging straight down beside the bench.',
          ...RECLINED,
          armNear: [0, 0],
          props: [...RECLINED_PROPS, { type: 'dumbbell', at: 'hands' }],
        },
        {
          label: 'Top',
          caption: 'Curl up by bending only the elbows. The upper arms stay hanging still.',
          ...RECLINED,
          armNear: [0, 160],
          props: [...RECLINED_PROPS, { type: 'dumbbell', at: 'hands' }, { type: 'arrow', from: [40, 150], to: [40, 116] }],
        },
        {
          label: 'Finish',
          caption: 'Lower slowly all the way to straight arms.',
          ...RECLINED,
          armNear: [0, 0],
          props: [...RECLINED_PROPS, { type: 'dumbbell', at: 'hands' }, { type: 'arrow', from: [40, 116], to: [40, 150] }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Leg Press
  {
    id: 'leg-press',
    name: 'Leg Press',
    aliases: ['45 degree leg press', 'Sled leg press'],
    kind: 'strength',
    purpose:
      'Builds the thighs and glutes with no bar on the spine. The back rests on a pad, so the legs can work hard on the same week as squats while the lower back recovers.',
    equipment: ['45 degree leg press machine'],
    setup: [
      'Sit with the lower back and hips pressed into the seat.',
      'Place the feet in the middle of the platform, about shoulder width, toes turned out a little.',
      'Press the platform up and release the safety handles. Hold the side handles.',
    ],
    steps: [
      'Lower the platform slowly by bending the knees toward the chest. Knees follow the line of the toes.',
      'Stop at the deepest point where the lower back and hips still stay flat on the seat.',
      'Press the platform away through the whole foot.',
      'Stop just short of locking the knees, then start the next rep.',
      'After the last rep, lock the safety handles before you take the feet off.',
    ],
    breathing: 'Breathe in as you lower. Breathe out as you press through the hardest part.',
    tempo: '3 1 1 0 means three seconds down, a one second pause at the bottom, one second up, and no rest at the top.',
    rangeOfMotion:
      'Knees usually bend to about a right angle or a little deeper. The depth ends where the tailbone would start to curl off the seat, so the lower back never rounds.',
    muscles: {
      primary: ['quads', 'glute_max'],
      secondary: ['adductors', 'hamstrings'],
    },
    emphasisNote:
      'Feet lower on the platform bias the quads, feet higher and a little wider bring in more glutes and inner thighs. The quads and glutes work together in every version.',
    movementPattern: 'squat',
    joints: ['Hip', 'Knee', 'Ankle'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['knee', 'hip'],
    commonMistakes: [
      'Going so deep that the hips lift and the lower back rounds off the seat.',
      'Knees caving inward on the way up.',
      'Heels lifting off the platform.',
      'Snapping the knees straight and locked at the top.',
      'Pushing with the hands on the knees.',
    ],
    goodFormFeels: 'Hips and back stay heavy in the seat, the push comes through the whole foot, and the thighs and glutes feel the work.',
    stopRules: ['Stop the set when the knees start to cave, the depth shrinks, or the hips lift.', RIR_RULE, PAIN_RULE],
    safetyNotes: [
      'Use the safety stops or locks every time, and set them before loading the machine heavily.',
      'Never lock the knees straight under load.',
      'Monday already has squats. Keep this at the prescribed reps in reserve so Monday stays strong.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Goblet squat',
      reason: 'Hold one dumbbell at the chest and squat to a box. Light and easy to learn.',
    },
    equipmentSubstitution: {
      exerciseId: 'hack-squat',
      name: 'Hack Squat',
      reason: 'Another machine that loads the legs with the back supported.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'bulgarian-split-squat',
        name: 'Bulgarian Split Squat',
        reason: 'One leg at a time with dumbbells when the machine is busy.',
      },
    ],
    loadIncrement: 'lower',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Back and hips in the seat, feet in the middle of the platform, legs almost straight.',
          ...LEG_PRESS,
          armNear: [12, 62],
          legNear: [135, 135, 225],
          props: [
            ...LEG_PRESS_PROPS,
            { type: 'bench', x: 120.7, y: 46.5, w: 36, h: 6, angle: 45 },
            { type: 'handle', at: 'hands' },
          ],
        },
        {
          label: 'Bottom',
          caption: 'Lower the platform until the knees are bent about a right angle. Lower back stays on the seat.',
          ...LEG_PRESS,
          armNear: [12, 62],
          legNear: [168, 97, 225],
          props: [
            ...LEG_PRESS_PROPS,
            { type: 'bench', x: 109.7, y: 59.9, w: 36, h: 6, angle: 45 },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [170, 30], to: [150, 50] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Press through the whole foot and stop just short of locking the knees.',
          ...LEG_PRESS,
          armNear: [12, 62],
          legNear: [135, 135, 225],
          props: [
            ...LEG_PRESS_PROPS,
            { type: 'bench', x: 120.7, y: 46.5, w: 36, h: 6, angle: 45 },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [150, 50], to: [170, 30] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- 45 Degree Back Extension
  {
    id: 'back-extension',
    name: '45 Degree Back Extension',
    aliases: ['Hyperextension', '45 degree hip extension'],
    kind: 'strength',
    purpose:
      'Strengthens the glutes, hamstrings, and the long muscles beside the spine. A strong back of the body helps you jump, land, and stay healthy through a season, and no other day trains the lower back directly.',
    equipment: ['45 degree back extension bench', 'Optional weight plate or dumbbell to hold at the chest'],
    setup: [
      'Set the pad so its top edge sits just below the hip bones, where the body folds.',
      'Step onto the foot plate with the heels under the roller.',
      'Stand the body up straight in line with the legs. Cross the arms on the chest, or hold a plate against it.',
    ],
    steps: [
      'Keep the back flat and the neck long, and fold forward at the hips over the pad.',
      'Go down until you feel a stretch in the back of the thighs, before the lower back starts to round.',
      'Squeeze the glutes and lift the body back up by driving the hips into the pad.',
      'Stop when the body is in a straight line with the legs. Do not lean back past that.',
    ],
    breathing: 'Breathe in at the top before you fold. Breathe out as you rise back up.',
    tempo: '2 0 1 1 means two seconds down, no pause at the bottom, one second up, and a one second squeeze at the top.',
    rangeOfMotion:
      'From a straight line down to a stretch in the hamstrings, usually with the trunk close to vertical. The lower back stays flat, and the top ends in a straight line, never arched past it.',
    muscles: {
      primary: ['glute_max', 'hamstrings', 'erectors'],
      secondary: ['adductors'],
    },
    emphasisNote:
      'A flat back and a squeeze at the top bias the glutes and hamstrings. The long back muscles hold the spine straight the whole time, which is how they get stronger here.',
    movementPattern: 'hinge',
    joints: ['Hip', 'Spine'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['low_back', 'hamstring'],
    commonMistakes: [
      'Setting the pad too high so it blocks the hips from folding.',
      'Rounding the lower back at the bottom.',
      'Swinging up fast and arching back past a straight line at the top.',
      'Holding a plate that is too heavy for a smooth rep.',
    ],
    goodFormFeels: 'The glutes and the back of the thighs do the lifting, the back stays straight, and the top is a calm straight line.',
    stopRules: [
      'Stop the set when the lower back starts to round or the reps get jerky.',
      RIR_RULE,
      PAIN_RULE,
      'Lower back pain that stays after the set means stop for today and tell a parent, coach, or clinician.',
    ],
    safetyNotes: [
      'Start with body weight only. Enter 0 kg in the log, and add a light plate only when 15 clean reps feel easy.',
      'Monday already has Romanian deadlifts. Keep this at the prescribed reps in reserve.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Glute bridge on the floor',
      reason: 'The same hip drive while lying on your back, with no load on the lower back.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Cable pull through',
      reason: 'A hip hinge with a rope between the legs from a low pulley, when there is no back extension bench.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'barbell-hip-thrust',
        name: 'Barbell Hip Thrust',
        reason: 'Trains the glutes hard with the back supported on a bench.',
      },
    ],
    loadIncrement: 'lower',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Hips on the pad, heels under the roller, body in a straight line, arms crossed on the chest.',
          ...BACK_EXT,
          armNear: [-10, 150],
          props: BACK_EXT_PROPS,
        },
        {
          label: 'Bottom',
          caption: 'Fold forward at the hips with a flat back until the hamstrings stretch.',
          ...BACK_EXT,
          trunk: 40,
          head: 50,
          armNear: [-105, 55],
          props: [...BACK_EXT_PROPS, { type: 'arrow', from: [160, 90], to: [165, 126] }],
        },
        {
          label: 'Finish',
          caption: 'Squeeze the glutes and rise back to a straight line. Do not lean back past it.',
          ...BACK_EXT,
          armNear: [-10, 150],
          props: [...BACK_EXT_PROPS, { type: 'arrow', from: [165, 126], to: [160, 90] }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Cable Hip Adduction
  {
    id: 'cable-hip-adduction',
    name: 'Cable Hip Adduction',
    aliases: ['Standing cable adduction', 'Inner thigh cable pull'],
    kind: 'strength',
    purpose:
      'Strengthens the inner thigh muscles that pull the leg in. They steady the knee and hip in every side step and landing, and strong adductors are linked to fewer groin strains in court sports.',
    equipment: ['Cable machine with a low pulley', 'Ankle cuff'],
    setup: [
      'Attach the ankle cuff to the low pulley and strap it around the ankle nearest the machine.',
      'Stand side on to the machine, one step away, and hold it with the near hand for balance.',
      'Let the cuffed leg be pulled out to the side a little, foot just off the floor.',
    ],
    steps: [
      'Stand tall on the outside leg with a soft knee.',
      'Pull the cuffed leg in toward and just in front of the standing foot, toes pointing forward.',
      'Pause for one second when the feet are close together.',
      'Let the leg travel back out slowly, stopping before the weight touches down.',
      'Finish all reps, then turn around and do the other leg.',
    ],
    breathing: 'Breathe out as you pull the leg in. Breathe in as it goes back out.',
    tempo: '2 1 1 0 means two seconds out, a one second pause in, one second in, and no rest at the outside.',
    rangeOfMotion:
      'From a comfortable stretch out to the side, to the working foot just in front of the standing foot. The trunk stays upright and the hips stay level.',
    muscles: {
      primary: ['adductors'],
      secondary: ['hip_flexors', 'obliques_core'],
    },
    emphasisNote:
      'The inner thigh muscles do the pulling. The trunk and the standing leg hold you steady. Wednesday adds the Copenhagen plank for the same muscles in a harder, held position.',
    movementPattern: 'hip_adduction',
    joints: ['Hip'],
    laterality: 'unilateral',
    logSides: true,
    fatigueOverlap: ['hip'],
    commonMistakes: [
      'Leaning the trunk away to swing the leg in.',
      'Letting the weight yank the leg out fast.',
      'Turning the toes up or out instead of keeping them forward.',
      'Standing so far away that the leg is pulled too wide at the start.',
    ],
    goodFormFeels: 'A steady upright body, a smooth pull, and the work right in the inner thigh.',
    stopRules: ['Stop the set when the trunk starts to lean or the leg swings.', RIR_RULE_SIDE, PAIN_RULE],
    safetyNotes: [
      'Start light. The inner thigh muscles are small compared with the thighs, and groin pain is a reason to stop.',
      'Hold the machine the whole time for balance.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Side lying adductor lift',
      reason: 'Lie on your side and lift the bottom leg a few centimetres, with no equipment.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Seated adductor machine',
      reason: 'Squeeze the pads together while seated. Many gyms have one.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'copenhagen-plank',
        name: 'Copenhagen Plank',
        reason: 'A held version for the same muscles, harder than it looks.',
      },
    ],
    loadIncrement: 'lower',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Front view. Stand side on to the low pulley, cuff on the inside ankle, hand on the machine.',
          ...ADDUCT,
          armNear: [70, 105],
          armFar: [-35, 45],
          legNear: [20, 20, 85],
          props: [ADDUCT_POST, { type: 'cable', from: 'nearAnkle', to: [182, 166] }],
        },
        {
          label: 'In',
          caption: 'Front view. Pull the leg in until the foot is just in front of the standing foot. Trunk stays upright.',
          ...ADDUCT,
          armNear: [70, 105],
          armFar: [-35, 45],
          legNear: [-6, -6, 95],
          props: [ADDUCT_POST, { type: 'cable', from: 'nearAnkle', to: [182, 166] }, { type: 'arrow', from: [170, 140], to: [146, 150] }],
        },
        {
          label: 'Finish',
          caption: 'Front view. Let the leg travel back out slowly without letting the weight touch down.',
          ...ADDUCT,
          armNear: [70, 105],
          armFar: [-35, 45],
          legNear: [20, 20, 85],
          props: [ADDUCT_POST, { type: 'cable', from: 'nearAnkle', to: [182, 166] }, { type: 'arrow', from: [146, 150], to: [170, 140] }],
        },
      ],
    },
  },
];
