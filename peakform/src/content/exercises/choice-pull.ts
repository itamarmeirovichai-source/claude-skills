import { EFFORT_RULE, PAIN_RULE } from './effort';
import type { ExerciseContent, Pose, PoseProp } from '../types';

// Pull day choices for the exercise questionnaire. Order matches PULL_CHOICE_IDS in ids.ts.
// Machines, cables, the Smith machine, and dumbbells only. Most of these are picked because they
// load a muscle hard in its long, stretched position: the top of a pulldown or pull up, the arms
// overhead in a pullover, the crossed start of a cable reverse fly, and the arm behind the body in
// a Bayesian curl. Poses are side views unless the caption says front view.

// ---------- Shared pose pieces ----------

type Base = Pick<Pose, 'trunk' | 'hip' | 'legNear' | 'legFar' | 'footX' | 'head'>;

/** Pulldown seat with the thighs under a pad and a slight lean back (the same seat as in upper.ts). */
const PULLDOWN: Base = { trunk: 190, hip: [92, 132], legNear: [90, 0] };
const PULLDOWN_PROPS: PoseProp[] = [
  { type: 'bench', x: 68, y: 140, w: 44 },
  { type: 'pad', x: 116, y: 115, w: 22, h: 9 },
];

/** Assisted pull up machine: a frame in front, handles at the top, a knee pad on a lever. */
const ASSIST_FRAME: PoseProp[] = [
  { type: 'line', x1: 172, y1: 14, x2: 172, y2: 172 },
  { type: 'line', x1: 112, y1: 24, x2: 172, y2: 24 },
];
const ASSIST_HANG: Base = { trunk: 180, head: 180, hip: [104.7, 125.5], legNear: [42, -90, -80] };
const ASSIST_HANG_PROPS: PoseProp[] = [
  ...ASSIST_FRAME,
  { type: 'line', x1: 132, y1: 164, x2: 168, y2: 138 },
  { type: 'pad', x: 88, y: 161.7, w: 48, h: 5 },
];
const ASSIST_TOP: Base = { trunk: 186, head: 180, hip: [100, 77], legNear: [42, -90, -80] };
const ASSIST_TOP_PROPS: PoseProp[] = [
  ...ASSIST_FRAME,
  { type: 'line', x1: 128, y1: 115.5, x2: 168, y2: 138 },
  { type: 'pad', x: 84, y: 113.2, w: 48, h: 5 },
];

/** Standing with a slight hip hinge, facing a high pulley. */
const HINGE: Base = { trunk: 155, head: 162, legNear: [16, -6], legFar: [12, -8], footX: 82 };
const HIGH_PULLEY: PoseProp = { type: 'line', x1: 176, y1: 2, x2: 176, y2: 172 };

/** Lying face up along a flat bench, head to the left, feet on the floor. */
const LYING: Base = { trunk: -90, hip: [130, 116], legNear: [68, -10] };
const FLAT_BENCH: PoseProp = { type: 'bench', x: 55, y: 125, w: 88 };

/** Seated facing the machine with the chest on a pad. */
const CHEST_ROW: Base = { trunk: 180, hip: [80, 132], legNear: [90, 0] };
const CHEST_ROW_PROPS: PoseProp[] = [
  { type: 'line', x1: 150, y1: 40, x2: 150, y2: 172 },
  { type: 'line', x1: 98, y1: 110, x2: 150, y2: 110 },
  { type: 'bench', x: 56, y: 140, w: 46 },
  { type: 'pad', x: 90, y: 92, w: 8, h: 32 },
];

/** Front view: the figure faces you, near side on the right of the picture. */
const FRONT: Base = { trunk: 180, legNear: [12, 0, 90], legFar: [-12, 0, -90], footX: 108 };
/** Crossover station seen from the front: a post on each side, pulleys at about shoulder height. */
const CROSSOVER: PoseProp[] = [
  { type: 'line', x1: 14, y1: 20, x2: 14, y2: 172 },
  { type: 'line', x1: 186, y1: 20, x2: 186, y2: 172 },
];

/** Split stance facing away from a low pulley, with a slight forward lean. */
const BAYES: Base = { trunk: 176, legNear: [16, 0], legFar: [-18, -8, 80], footX: 104 };
const LOW_PULLEY_BEHIND: PoseProp = { type: 'line', x1: 24, y1: 24, x2: 24, y2: 172 };

/** Seated at a preacher bench, upper arm on an angled pad. */
const PREACHER: Base = { trunk: 172, hip: [72, 132], legNear: [90, 0] };
const PREACHER_PROPS: PoseProp[] = [
  { type: 'line', x1: 104, y1: 118, x2: 104, y2: 172 },
  { type: 'bench', x: 48, y: 140, w: 46 },
  { type: 'bench', x: 75, y: 89, w: 36, h: 10, angle: 40 },
];

/** Standing tall, facing a low pulley. */
const STAND: Base = { trunk: 180, legNear: [0, 0], legFar: [3, -3] };
const LOW_PULLEY_FRONT: PoseProp = { type: 'line', x1: 178, y1: 20, x2: 178, y2: 172 };

export const PULL_CHOICES: ExerciseContent[] = [
  // ---------------------------------------------------------------- Neutral Grip Lat Pulldown
  {
    id: 'neutral-grip-pulldown',
    name: 'Neutral Grip Lat Pulldown',
    aliases: ['V handle pulldown', 'Close neutral grip pulldown', 'Parallel grip pulldown'],
    kind: 'strength',
    purpose:
      'Builds the lats, the big muscles along the sides of your back that pull the arm down in a spike and through the water when you swim. Palms facing each other let the elbows travel close to your sides, and the long reach at the top stretches the lats fully under load, which is a good position for growth.',
    equipment: ['Lat pulldown station', 'V handle or parallel grip handle'],
    setup: [
      'Attach a V handle, or a wide handle with parallel grips, to the pulldown cable.',
      'Set the thigh pad so your thighs are held firmly and your feet are flat on the floor.',
      'Stand, take the handle with your palms facing each other, and sit down with your arms straight.',
      'Lean back only slightly from the hips and lift your chest.',
    ],
    steps: [
      'Start with your arms fully straight and your shoulders reaching up toward the handle, so you feel a stretch along the sides of your back.',
      'Begin the pull by drawing your shoulder blades down.',
      'Drive your elbows down close to your sides as the handle moves toward your upper chest.',
      'Pull until the handle reaches your upper chest, chest still lifted, and pause briefly.',
      'Let the handle rise slowly until your arms are straight and the weight gently pulls your shoulders up into the full stretch.',
    ],
    breathing: 'Breathe out as you pull down. Breathe in as the handle rises.',
    tempo:
      '2 1 1 1 means two seconds to let the handle rise, a one second pause in the stretch at the top, one second to pull down, and a one second hold at the chest.',
    rangeOfMotion:
      'Go from fully straight arms, with the shoulders reaching up, to the handle at your upper chest. Keep the handle in front of your face and do not cut the top of the rep short.',
    muscles: {
      primary: ['lats'],
      secondary: ['teres_major', 'biceps', 'brachialis', 'brachioradialis', 'traps_lower', 'rhomboids'],
    },
    emphasisNote:
      'Palms facing each other keep the elbows close to your sides, which biases the lats and lets the biceps, brachialis, and brachioradialis help a little more than with a wide grip. The full reach at the top lengthens the lats under load, and studies suggest that training a muscle at long lengths is good for growth. The lower traps and rhomboids set the shoulder blades in every rep.',
    movementPattern: 'vertical_pull',
    joints: ['Shoulder', 'Elbow', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder', 'elbow', 'wrist_grip'],
    commonMistakes: [
      'Stopping the handle before the arms are straight, so the lats never reach their stretch.',
      'Leaning far back so the pulldown turns into a row.',
      'Swinging the body to start the pull.',
      'Pulling with the hands and biceps instead of driving the elbows down.',
      'Letting the weight stack crash at the top.',
    ],
    goodFormFeels:
      'A long stretch under the armpits at the top, then a strong squeeze along the sides of your back as the elbows reach your ribs. Your chest stays tall and your trunk stays still.',
    stopRules: [
      'Stop the set when you start leaning back or swinging, or when the handle no longer reaches your upper chest.',
      EFFORT_RULE.last,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Keep the thigh pad snug so a heavy weight cannot lift you off the seat.',
      'Your lats and shoulders also work hard in spiking and swimming this week, so keep every rep smooth and controlled.',
    ],
    easierSubstitution: {
      exerciseId: 'leverage-high-row',
      name: 'Leverage High Row',
      reason: 'A guided machine pull from above. The fixed path makes it easier to keep your trunk still while you learn the movement.',
    },
    equipmentSubstitution: {
      exerciseId: 'assisted-pull-up',
      name: 'Assisted Pull Up',
      reason: 'Use when the pulldown station is busy. It trains the same pull from a full hang.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'wide-grip-lat-pulldown',
        name: 'Wide Grip Lat Pulldown',
        reason: 'The same station with a long bar. It shares a little more of the work with the upper back.',
      },
      {
        exerciseId: 'one-arm-lat-pulldown',
        name: 'One Arm Lat Pulldown',
        reason: 'Trains one side at a time with an even longer reach at the top.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'last',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Sit with the thighs under the pad and the arms reaching long overhead to the V handle.',
          ...PULLDOWN,
          armNear: [168, 176],
          props: [...PULLDOWN_PROPS, { type: 'cable', from: 'hands', to: [94, 4] }, { type: 'handle', at: 'hands' }],
        },
        {
          label: 'Pull',
          caption: 'Drive the elbows down close to the sides until the handle reaches the upper chest.',
          ...PULLDOWN,
          armNear: [-30, 148],
          props: [
            ...PULLDOWN_PROPS,
            { type: 'cable', from: 'hands', to: [94, 4] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [130, 36], to: [130, 72] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Let the handle rise slowly until the arms are straight and the lats are fully stretched.',
          ...PULLDOWN,
          armNear: [168, 176],
          props: [
            ...PULLDOWN_PROPS,
            { type: 'cable', from: 'hands', to: [94, 4] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [130, 72], to: [130, 36] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Assisted Pull Up
  {
    id: 'assisted-pull-up',
    name: 'Assisted Pull Up',
    aliases: ['Machine assisted pull up', 'Band assisted pull up'],
    kind: 'bodyweight',
    purpose:
      'Builds the lats and teres major, the muscles that pull you up and drive the arm down in a spike, using your own body weight. The machine or band takes part of your weight, so you can do full reps from a dead hang, where the lats are fully stretched, to the chin over the handles.',
    equipment: ['Assisted pull up machine with a knee pad', 'Or a pull up bar with a looped resistance band'],
    setup: [
      'On the machine, choose the assistance on the weight stack. More weight on the stack gives more help. Pick the amount that makes your target reps hard but still clean.',
      'Climb the steps, grip the handles with your palms facing each other or facing away, then kneel on the pad one knee at a time.',
      'With a band instead, loop it securely over the bar, put one knee in the loop, and grip the bar a little wider than your shoulders.',
      'Let the pad or band lower you to a full hang with straight arms.',
      'Write the assistance you used in the note for this exercise, because the log does not track it. Over the weeks, aim to use less assistance for the same reps.',
    ],
    steps: [
      'Start from a dead hang with straight arms, so you feel a stretch along the sides of your back.',
      'Draw your shoulder blades down to begin the pull.',
      'Drive your elbows down toward your ribs and bring your chest up toward the handles.',
      'Pull until your chin is over the handles, and pause briefly.',
      'Lower slowly all the way back to a dead hang with straight arms.',
      'After the last rep, step back onto the steps one foot at a time before you let go of the handles.',
    ],
    breathing: 'Breathe out as you pull up. Breathe in as you lower.',
    tempo:
      '2 1 1 1 means two seconds to lower, a one second pause in the dead hang, one second to pull up, and a one second hold with the chin over the handles.',
    rangeOfMotion:
      'Go from a full dead hang with straight arms to the chin over the handles. Do not stop short of straight arms at the bottom, because that is where the lats are longest.',
    muscles: {
      primary: ['lats', 'teres_major'],
      secondary: ['biceps', 'brachialis', 'traps_lower', 'rhomboids', 'forearm_flexors'],
    },
    emphasisNote:
      'Driving the elbows down to your sides biases the lats and teres major. The biceps and brachialis bend the elbows, the lower traps and rhomboids pull the shoulder blades down and back, and the forearms work to hold the handles. The dead hang stretches the lats under load, which studies suggest is good for growth.',
    movementPattern: 'vertical_pull',
    joints: ['Shoulder', 'Elbow', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder', 'elbow', 'wrist_grip'],
    commonMistakes: [
      'Choosing so much assistance that the target reps feel easy.',
      'Stopping short of a dead hang at the bottom.',
      'Kicking or swinging to get the chin over.',
      'Reaching the chin forward instead of bringing the chest up.',
      'Dropping fast into the bottom.',
    ],
    goodFormFeels:
      'A long stretch under the armpits at the bottom, a smooth pull with the elbows driving down, and a body that stays quiet on the pad.',
    stopRules: [
      'Stop the set when your chin no longer clears the handles or you start kicking or swinging.',
      EFFORT_RULE.last,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Get on and off the knee pad slowly, one knee at a time, while holding the handles. The pad moves as soon as you put weight on it.',
      'With a band, check that it is looped securely around the bar, and step out of it carefully after the set.',
    ],
    easierSubstitution: {
      exerciseId: 'neutral-grip-pulldown',
      name: 'Neutral Grip Lat Pulldown',
      reason: 'You choose the exact load on the stack, so it is easy to start light and learn the pull.',
    },
    equipmentSubstitution: {
      exerciseId: 'wide-grip-lat-pulldown',
      name: 'Wide Grip Lat Pulldown',
      reason: 'Use when there is no assisted machine or band. It trains the same vertical pull on a seat.',
    },
    otherSubstitutions: [
      {
        exerciseId: null,
        name: 'Slow lowering pull up',
        reason: 'Step up from a sturdy box to the top position and lower yourself slowly over three to five seconds. It builds toward a full pull up.',
      },
    ],
    loadIncrement: 'none',
    failure: 'last',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Kneel on the pad and hang from the handles with straight arms.',
          ...ASSIST_HANG,
          armNear: [170, 175],
          props: [...ASSIST_HANG_PROPS, { type: 'handle', at: 'hands' }],
        },
        {
          label: 'Top',
          caption: 'Drive the elbows down and bring the chest up until the chin is over the handles.',
          ...ASSIST_TOP,
          armNear: [48.3, 190.6],
          props: [...ASSIST_TOP_PROPS, { type: 'handle', at: 'hands' }, { type: 'arrow', from: [148, 110], to: [148, 76] }],
        },
        {
          label: 'Finish',
          caption: 'Lower slowly all the way back to a dead hang with straight arms.',
          ...ASSIST_HANG,
          armNear: [170, 175],
          props: [...ASSIST_HANG_PROPS, { type: 'handle', at: 'hands' }, { type: 'arrow', from: [148, 76], to: [148, 110] }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Straight Arm Cable Pulldown
  {
    id: 'straight-arm-cable-pulldown',
    name: 'Straight Arm Cable Pulldown',
    aliases: ['Straight arm lat pulldown', 'Standing cable pullover'],
    kind: 'strength',
    purpose:
      'Trains the lats and teres major by sweeping the arms down from overhead with the elbows nearly straight. The biceps help very little, so more of the pull falls on the back, and the start overhead puts the lats on a long stretch.',
    equipment: ['High cable pulley', 'Rope or straight bar attachment'],
    setup: [
      'Set the pulley at the top and attach a rope or a straight bar.',
      'Grip the attachment with straight arms and step back two or three steps so the weight lifts off the stack.',
      'Stand with your feet hip width apart and your knees soft.',
      'Hinge forward slightly from the hips with a flat back, so your arms reach up and forward toward the pulley.',
    ],
    steps: [
      'Start with your arms long and reaching up toward the pulley, so you feel a stretch along the sides of your back.',
      'Keeping your elbows nearly straight, sweep your hands down in a wide arc toward your thighs.',
      'Finish with your hands by your thighs and squeeze the sides of your back briefly.',
      'Let your arms rise slowly along the same arc until they are back up in the full stretch.',
      'Keep your trunk still the whole time. Only the shoulders move.',
    ],
    breathing: 'Breathe out as you sweep the arms down. Breathe in as they rise.',
    tempo:
      '2 1 1 1 means two seconds for the arms to rise, a one second pause in the stretch, one second to sweep down, and a one second squeeze at the thighs.',
    rangeOfMotion:
      'Go from the arms reaching up past your head, as far as your shoulders move comfortably, to your hands at your thighs. Keep the same small elbow bend all the way.',
    muscles: {
      primary: ['lats', 'teres_major'],
      secondary: ['triceps', 'traps_lower', 'obliques_core'],
    },
    emphasisNote:
      'With the elbows nearly straight, the lats and teres major do most of the work of bringing the arms down, and the biceps help very little. The long head of the triceps also helps pull the arm down, and the core keeps your trunk still. The stretch at the top works the lats at a long length, which studies suggest is good for growth.',
    movementPattern: 'shoulder_extension',
    joints: ['Shoulder', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder'],
    commonMistakes: [
      'Bending the elbows so it turns into a triceps pushdown.',
      'Rocking the trunk up and down to move the weight.',
      'Stopping the arms at eye level instead of reaching up into the stretch.',
      'Shrugging the shoulders up toward the ears at the top.',
    ],
    goodFormFeels:
      'A long stretch under the armpits at the top, the effort along the sides of your back rather than in your arms, and a trunk that stays still.',
    stopRules: [
      'Stop the set when your elbows start bending more or your trunk starts rocking.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Use a moderate weight. Too much weight pulls you forward off balance.',
      'This counts as shoulder work alongside spiking and swimming. If the front of the shoulder pinches at the top, shorten the stretch a little.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Band straight arm pulldown',
      reason: 'A light band anchored high is simple to control and good for learning the arc.',
    },
    equipmentSubstitution: {
      exerciseId: 'dumbbell-pullover',
      name: 'Dumbbell Pullover',
      reason: 'Use when no cable is free. One dumbbell over a flat bench trains the same arm path lying down.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'neutral-grip-pulldown',
        name: 'Neutral Grip Lat Pulldown',
        reason: 'Trains the lats from the same long stretch overhead, with more help from the arms.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Hinge slightly at the hips, arms long and reaching up toward the high pulley.',
          ...HINGE,
          armNear: [130, 134],
          props: [HIGH_PULLEY, { type: 'cable', from: 'hands', to: [176, 6] }, { type: 'handle', at: 'hands' }],
        },
        {
          label: 'Bottom',
          caption: 'Sweep the nearly straight arms down in an arc until the hands reach the thighs.',
          ...HINGE,
          armNear: [-6, -2],
          props: [
            HIGH_PULLEY,
            { type: 'cable', from: 'hands', to: [176, 6] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [150, 40], to: [128, 96] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Let the arms rise slowly along the same arc back into the stretch.',
          ...HINGE,
          armNear: [130, 134],
          props: [
            HIGH_PULLEY,
            { type: 'cable', from: 'hands', to: [176, 6] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [128, 96], to: [150, 40] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Dumbbell Pullover
  {
    id: 'dumbbell-pullover',
    name: 'Dumbbell Pullover',
    aliases: ['Lying dumbbell pullover'],
    kind: 'strength',
    purpose:
      'Trains the lats and the lower part of the chest by lowering one dumbbell behind your head and pulling it back over your chest. Both muscles work through a long stretch with the arms overhead.',
    equipment: ['One dumbbell', 'Flat bench'],
    setup: [
      'Sit on the end of a flat bench with the dumbbell standing on your thigh.',
      'Lie back along the bench so your head is supported near the end and your feet are flat on the floor.',
      'Hold the top end of the dumbbell with both hands, palms flat against the inside of the plate and thumbs around the handle.',
      'Press the dumbbell up over your chest with a soft bend in your elbows.',
    ],
    steps: [
      'Keeping the same soft elbow bend, lower the dumbbell back in an arc over your face and behind your head.',
      'Stop when your upper arms are about in line with your body, or sooner if the shoulders feel tight.',
      'Pause briefly in the stretch without letting your lower back arch off the bench.',
      'Pull the dumbbell back along the same arc until it is over your chest again.',
      'After the last rep, bring the dumbbell down to your chest and sit up before you put it down.',
    ],
    breathing: 'Breathe in as you lower the dumbbell behind your head. Breathe out as you pull it back over your chest.',
    tempo:
      '3 1 1 0 means three seconds to lower the dumbbell behind your head, a one second pause in the stretch, one second to pull it back, and no rest over the chest.',
    rangeOfMotion:
      'Go from the dumbbell over your chest to behind your head, only as far as your shoulders feel comfortable. For most people that is when the upper arms are about level with the bench. Your ribs stay down and your lower back stays on the bench.',
    muscles: {
      primary: ['lats', 'pec_sternal'],
      secondary: ['teres_major', 'triceps', 'serratus_anterior'],
    },
    emphasisNote:
      'The lats and the middle and lower chest both pull the arms down and forward from overhead, so they share the work, with help from the teres major, the long head of the triceps, and the serratus. The arms overhead position stretches the lats and chest at a long length. Keeping the elbow bend fixed keeps the work at the shoulders instead of the elbows.',
    movementPattern: 'shoulder_extension',
    joints: ['Shoulder', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder'],
    commonMistakes: [
      'Lowering past the point where the shoulders feel comfortable.',
      'Bending and straightening the elbows so it turns into a triceps extension.',
      'Arching the lower back off the bench in the stretch.',
      'Using a dumbbell so heavy that the lowering speeds up.',
    ],
    goodFormFeels:
      'A steady stretch along the sides of your back and across the lower chest at the bottom, a slow even arc, and shoulders that feel open but never pinched.',
    stopRules: [
      'Stop the set when the lowering speeds up, your lower back arches, or a shoulder feels tight or pinched.',
      EFFORT_RULE.never,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Shoulder care for a hitter: the arms overhead position loads the same shoulder you spike with. Start light, go only as deep as feels comfortable, and skip this exercise on days the shoulder is already sore from volleyball.',
      'Hold the dumbbell firmly with both hands the whole time, because it passes over your face.',
    ],
    easierSubstitution: {
      exerciseId: 'straight-arm-cable-pulldown',
      name: 'Straight Arm Cable Pulldown',
      reason: 'Trains the same arm path standing at a cable, with no weight over your face.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Machine pullover',
      reason: 'Some gyms have a pullover machine with a guided path and a seat. Use it when no bench or dumbbell is free.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'neutral-grip-pulldown',
        name: 'Neutral Grip Lat Pulldown',
        reason: 'Trains the lats from a long stretch overhead on a guided cable.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'never',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Lie along the bench, feet flat, one dumbbell held over the chest with both hands.',
          ...LYING,
          armNear: [176, 186],
          props: [FLAT_BENCH, { type: 'dumbbell', at: 'hands' }],
        },
        {
          label: 'Stretch',
          caption: 'Lower the dumbbell in an arc behind the head, only as far as the shoulders are comfortable.',
          ...LYING,
          armNear: [-115, -125],
          props: [FLAT_BENCH, { type: 'dumbbell', at: 'hands' }, { type: 'arrow', from: [70, 50], to: [36, 82] }],
        },
        {
          label: 'Finish',
          caption: 'Pull the dumbbell back along the same arc until it is over the chest.',
          ...LYING,
          armNear: [176, 186],
          props: [FLAT_BENCH, { type: 'dumbbell', at: 'hands' }, { type: 'arrow', from: [36, 82], to: [70, 50] }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Chest Supported Machine Row
  {
    id: 'chest-supported-machine-row',
    name: 'Chest Supported Machine Row',
    aliases: ['Seated chest supported row', 'Chest supported T bar row'],
    kind: 'strength',
    purpose:
      'Builds the middle back, the lats, and the rear shoulders. The chest pad holds your trunk still and rests the lower back, so the back muscles do the pulling. Studies comparing machines and free weights find that both build muscle well when you train with similar effort.',
    equipment: ['Chest supported row machine, plate loaded or with a weight stack', 'Or a chest supported T bar row'],
    setup: [
      'Set the seat so the handles are at about the height of your lower chest.',
      'Set the chest pad so you can just reach the handles with your arms fully straight and your shoulders reaching forward.',
      'Sit with your chest against the pad and your feet flat on the floor or on the foot rests.',
      'Grip the handles with your palms facing each other or facing down, and lift your chest tall against the pad.',
      'A chest supported T bar row works the same way: chest on its pad, feet on the platform, and the same steps.',
    ],
    steps: [
      'Start with your arms long and let your shoulder blades spread forward, so the upper back gets a stretch.',
      'Pull your elbows back past your body, keeping your chest on the pad.',
      'Squeeze your shoulder blades together at the end and hold for one second.',
      'Let the handles travel forward slowly until your arms are straight and your shoulder blades spread again.',
    ],
    breathing: 'Breathe out as you pull. Breathe in as the handles move forward.',
    tempo:
      '2 1 1 1 means two seconds to let the handles travel forward, a one second pause in the stretch, one second to pull, and a one second squeeze at the end.',
    rangeOfMotion:
      'Go from fully straight arms with the shoulder blades spread forward to the elbows just behind your body with the shoulder blades together. Your chest stays on the pad the whole time.',
    muscles: {
      primary: ['lats', 'traps_middle', 'rhomboids'],
      secondary: ['delt_posterior', 'teres_major', 'traps_lower', 'biceps', 'brachialis', 'brachioradialis'],
    },
    emphasisNote:
      'Elbows close to your sides bias the lats. Elbows flared out wider bias the middle traps, rhomboids, and rear shoulders. The full forward reach stretches the middle back at a long length before each pull. The biceps and forearms help in every rep.',
    movementPattern: 'horizontal_pull',
    joints: ['Shoulder', 'Elbow', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['elbow', 'wrist_grip'],
    commonMistakes: [
      'Lifting the chest off the pad to heave the weight back.',
      'Cutting the forward reach short so the back never gets its stretch.',
      'Shrugging the shoulders up toward the ears.',
      'Letting the weight crash forward at the end of each rep.',
    ],
    goodFormFeels:
      'Your chest stays on the pad, the shoulder blades glide forward and back, and the squeeze sits between the shoulder blades and along the sides of your back.',
    stopRules: [
      'Stop the set when your chest lifts off the pad or the elbows no longer come back past your body.',
      EFFORT_RULE.last,
      PAIN_RULE,
    ],
    safetyNotes: [
      'On a plate loaded machine, load both sides evenly and let the handles come all the way forward to their rest before you let go.',
      'On a T bar row, lower the weight to its rest before you step off the platform.',
    ],
    easierSubstitution: {
      exerciseId: 'seated-cable-row',
      name: 'Seated Cable Row',
      reason: 'A steady cable pull with the feet braced. It is easy to set up and the weight changes in small steps.',
    },
    equipmentSubstitution: {
      exerciseId: 'chest-supported-dumbbell-row',
      name: 'Chest Supported Dumbbell Row',
      reason: 'Use when the machine is busy. An incline bench and two dumbbells give the same chest support.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'leverage-high-row',
        name: 'Leverage High Row',
        reason: 'A machine pull from a higher angle that trains the same back muscles.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'last',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Sit with the chest on the pad and the arms fully straight, reaching forward to the handles.',
          ...CHEST_ROW,
          armNear: [80, 86],
          props: [...CHEST_ROW_PROPS, { type: 'handle', at: 'hands' }],
        },
        {
          label: 'Pull',
          caption: 'Pull the elbows back past the body and squeeze the shoulder blades together.',
          ...CHEST_ROW,
          armNear: [-62, 86],
          props: [...CHEST_ROW_PROPS, { type: 'handle', at: 'hands' }, { type: 'arrow', from: [134, 76], to: [100, 76] }],
        },
        {
          label: 'Finish',
          caption: 'Let the handles travel forward slowly until the arms are straight and the upper back stretches.',
          ...CHEST_ROW,
          armNear: [80, 86],
          props: [...CHEST_ROW_PROPS, { type: 'handle', at: 'hands' }, { type: 'arrow', from: [100, 76], to: [134, 76] }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Cable Reverse Fly
  {
    id: 'cable-reverse-fly',
    name: 'Cable Reverse Fly',
    aliases: ['Cable rear delt fly', 'Standing cable reverse fly'],
    kind: 'strength',
    purpose:
      'Builds the rear shoulders and the muscles between the shoulder blades, which balance the front of the shoulder after lots of pressing and hitting. Crossing the cables lets your arms start across the front of your body, where the rear shoulders are stretched, and the cables keep tension on through the whole sweep.',
    equipment: ['Cable crossover station with two pulleys', 'Two single D handles, or the cable ends'],
    setup: [
      'Set both pulleys at about shoulder height. Attach single D handles, or hold the cable ends.',
      'Cross the cables: take the right cable in your left hand and the left cable in your right hand.',
      'Step to the middle, between the pulleys, and stand tall with your feet hip width apart.',
      'Start with your arms crossed in front of your chest at about shoulder height, elbows softly bent.',
    ],
    steps: [
      'Let the cables draw your arms across in front of you, so you feel a stretch at the back of the shoulders.',
      'Keeping the soft elbow bend, sweep your arms out and back at shoulder height in a wide arc.',
      'Stop when your arms are in line with your shoulders, and pause briefly.',
      'Return slowly along the same arc until your arms cross in front of you again.',
    ],
    breathing: 'Breathe out as your arms sweep out. Breathe in as they return.',
    tempo:
      '2 1 1 1 means two seconds to bring the arms back across, a one second pause in the stretch, one second to sweep out, and a one second hold with the arms wide.',
    rangeOfMotion:
      'Go from the arms crossed in front of your chest to the arms in line with your shoulders. Going further back mostly squeezes the shoulder blades and can pinch the shoulder.',
    muscles: {
      primary: ['delt_posterior'],
      secondary: ['traps_middle', 'rhomboids', 'rotator_cuff'],
    },
    emphasisNote:
      'Arms at shoulder height with the shoulder blades fairly still bias the rear shoulders. The crossed start lets the arms travel past the middle of your body, which lengthens the rear shoulders more than a start with the hands apart, and the cables keep them working at that long length. Squeezing the shoulder blades together at the end adds middle trap and rhomboid work, and the rotator cuff keeps the shoulder centred.',
    movementPattern: 'shoulder_horizontal_abduction',
    joints: ['Shoulder', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder'],
    commonMistakes: [
      'Bending the elbows more as you pull, so it turns into a row.',
      'Letting the arms drift down toward the hips.',
      'Shrugging the shoulders up toward the ears.',
      'Leaning back to swing the cables out.',
    ],
    goodFormFeels:
      'A stretch at the back of the shoulders when the arms cross, a steady burn there as they open, and a relaxed neck.',
    stopRules: [
      'Stop the set when the elbows bend more, the arms drop below shoulder height, or you start leaning back.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Use a light weight you control. The rear shoulders are small muscles that respond well to smooth reps.',
      'This counts toward your shoulder load for the week alongside spiking and swimming.',
    ],
    easierSubstitution: {
      exerciseId: 'reverse-machine-fly',
      name: 'Reverse Machine Fly',
      reason: 'The machine guides the path and the chest pad holds you still.',
    },
    equipmentSubstitution: {
      exerciseId: 'face-pull',
      name: 'Face Pull',
      reason: 'Needs only one pulley and a rope when the crossover station is busy.',
    },
    otherSubstitutions: [
      {
        exerciseId: null,
        name: 'Chest supported dumbbell reverse fly',
        reason: 'Lie face down on an incline bench with light dumbbells when no cable is free.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Front view. Cables crossed, arms crossed in front of the chest, elbows softly bent.',
          ...FRONT,
          armNear: [50, -85],
          armFar: [-50, 85],
          props: [
            ...CROSSOVER,
            { type: 'cable', from: 'nearHand', to: [14, 34] },
            { type: 'cable', from: 'farHand', to: [186, 34] },
          ],
        },
        {
          label: 'Out',
          caption: 'Front view. Sweep the arms out wide at shoulder height until they line up with the shoulders.',
          ...FRONT,
          armNear: [86, 90],
          armFar: [-86, -90],
          props: [
            ...CROSSOVER,
            { type: 'cable', from: 'nearHand', to: [14, 34] },
            { type: 'cable', from: 'farHand', to: [186, 34] },
            { type: 'arrow', from: [124, 66], to: [158, 66] },
            { type: 'arrow', from: [75, 66], to: [41, 66] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Front view. Return slowly until the arms cross in front of the chest again.',
          ...FRONT,
          armNear: [50, -85],
          armFar: [-50, 85],
          props: [
            ...CROSSOVER,
            { type: 'cable', from: 'nearHand', to: [14, 34] },
            { type: 'cable', from: 'farHand', to: [186, 34] },
            { type: 'arrow', from: [158, 84], to: [124, 84] },
            { type: 'arrow', from: [41, 84], to: [75, 84] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Bayesian Cable Curl
  {
    id: 'bayesian-cable-curl',
    name: 'Bayesian Cable Curl',
    aliases: ['Behind the body cable curl', 'Face away cable curl'],
    kind: 'strength',
    purpose:
      'Trains the biceps with the arm pulled behind your body, so each rep starts with the biceps in a long stretch. Like the incline dumbbell curl, it trains the biceps at a long length, and the cable keeps tension on from the bottom to the top.',
    equipment: ['Low cable pulley', 'Single D handle'],
    setup: [
      'Set the pulley at the lowest position and attach a single handle.',
      'Take the handle in one hand, palm facing forward, and turn so you face away from the machine.',
      'Step forward into a split stance until the cable draws your arm back behind your body.',
      'Stand tall with a slight forward lean and let the working arm hang straight, a little behind your hip.',
    ],
    steps: [
      'Start with the elbow straight and the arm behind your body, so you feel a stretch in the front of the upper arm.',
      'Curl the handle forward and up by bending only at the elbow.',
      'Keep the upper arm still, a little behind your body. Do not let the elbow drift forward.',
      'Curl until your forearm is close to vertical and squeeze briefly.',
      'Lower slowly all the way back to a straight elbow and the stretch.',
      'Finish all reps on one side, then switch.',
    ],
    breathing: 'Breathe out as you curl. Breathe in as you lower.',
    tempo:
      '3 1 1 1 means three seconds down, a one second pause in the stretch, one second up, and a one second squeeze at the top.',
    rangeOfMotion:
      'Go from a straight elbow with the arm behind your body to the forearm close to vertical. The elbow stays behind your trunk the whole time.',
    muscles: {
      primary: ['biceps'],
      secondary: ['brachialis', 'brachioradialis'],
    },
    emphasisNote:
      'The long head of the biceps crosses the front of the shoulder, so taking the arm behind the body lengthens it. That is why this curl and the incline dumbbell curl both train the biceps at a long length. The brachialis and brachioradialis still help bend the elbow in every rep.',
    movementPattern: 'elbow_flexion',
    joints: ['Elbow'],
    laterality: 'unilateral',
    logSides: true,
    fatigueOverlap: ['elbow'],
    commonMistakes: [
      'Letting the elbow drift forward as you curl, which takes away the stretch.',
      'Standing too close to the machine, so the arm hangs at your side instead of behind you.',
      'Rocking the trunk forward and back to move the handle.',
      'Stopping short of a straight elbow at the bottom.',
    ],
    goodFormFeels:
      'A clear stretch in the front of the upper arm at the bottom, the work right in the biceps as you curl, and an elbow that stays behind you.',
    stopRules: [
      'Stop the set when the elbow drifts forward or the lowering speeds up.',
      'A sharp pull in the front of the shoulder means the arm is too far back. Step a little closer to the machine before the next set.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Start lighter than a normal cable curl. The stretched position is harder.',
      'Start with your weaker arm, then match the reps on the other side.',
    ],
    easierSubstitution: {
      exerciseId: 'machine-preacher-curl',
      name: 'Machine Preacher Curl',
      reason: 'The pad holds the upper arms, so the curl is easy to keep strict.',
    },
    equipmentSubstitution: {
      exerciseId: 'incline-dumbbell-curl',
      name: 'Incline Dumbbell Curl',
      reason: 'Use when no cable is free. The incline bench puts the arms behind the body in the same way.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'dumbbell-preacher-curl',
        name: 'Single Arm Dumbbell Preacher Curl',
        reason: 'Another one arm curl that is hardest near a straight elbow.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Face away from a low pulley in a split stance, the working arm straight and pulled behind the body.',
          ...BAYES,
          armNear: [-30, -30],
          armFar: [12, 30],
          props: [LOW_PULLEY_BEHIND, { type: 'cable', from: 'nearHand', to: [24, 162] }, { type: 'handle', at: 'nearHand' }],
        },
        {
          label: 'Top',
          caption: 'Curl forward and up until the forearm is close to vertical. The elbow stays behind the body.',
          ...BAYES,
          armNear: [-30, 140],
          armFar: [12, 30],
          props: [
            LOW_PULLEY_BEHIND,
            { type: 'cable', from: 'nearHand', to: [24, 162] },
            { type: 'handle', at: 'nearHand' },
            { type: 'arrow', from: [128, 90], to: [128, 56] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Lower slowly back to a straight elbow with the arm behind the body.',
          ...BAYES,
          armNear: [-30, -30],
          armFar: [12, 30],
          props: [
            LOW_PULLEY_BEHIND,
            { type: 'cable', from: 'nearHand', to: [24, 162] },
            { type: 'handle', at: 'nearHand' },
            { type: 'arrow', from: [128, 56], to: [128, 90] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Single Arm Dumbbell Preacher Curl
  {
    id: 'dumbbell-preacher-curl',
    name: 'Single Arm Dumbbell Preacher Curl',
    aliases: ['One arm preacher curl', 'Dumbbell preacher curl'],
    kind: 'strength',
    purpose:
      'Trains the biceps and brachialis one arm at a time with the upper arm resting on a pad, so the body cannot swing. The preacher position makes the curl hardest in the lower half of the rep, where the arm is closer to straight and these muscles are long.',
    equipment: ['One dumbbell', 'Preacher bench, or an incline bench with a tall back pad'],
    setup: [
      'Set the preacher seat so your armpit fits snugly over the top edge of the pad. With an incline bench, stand behind it and rest your arm over the top of the back pad.',
      'Rest the back of your working upper arm flat on the pad.',
      'Hold the dumbbell with your palm facing up.',
      'Hold the pad with your free hand to keep steady.',
    ],
    steps: [
      'Curl the dumbbell up until your forearm is close to vertical.',
      'Squeeze briefly at the top without lifting your elbow off the pad.',
      'Lower slowly over three seconds until your arm is almost straight and you feel a stretch in the front of the upper arm.',
      'Stop just short of a hard lockout, then start the next rep.',
      'Finish all reps on one side, then switch.',
    ],
    breathing: 'Breathe out as you curl. Breathe in as you lower.',
    tempo:
      '3 0 1 1 means three seconds down, no pause at the bottom, one second up, and a one second squeeze at the top.',
    rangeOfMotion:
      'Go from an almost straight arm to the forearm close to vertical. Stop just short of a hard lockout at the bottom and control that part of the rep, where the elbow is most exposed.',
    muscles: {
      primary: ['biceps', 'brachialis'],
      secondary: ['brachioradialis'],
    },
    emphasisNote:
      'With the upper arm resting in front of your body, the curl is hardest in the lower half of the rep, where the biceps and brachialis are long. The preacher position tends to bias the short head of the biceps and the brachialis, and the long head still works in every rep. One arm at a time lets each side move through its own full range.',
    movementPattern: 'elbow_flexion',
    joints: ['Elbow'],
    laterality: 'unilateral',
    logSides: true,
    fatigueOverlap: ['elbow'],
    commonMistakes: [
      'Lifting the elbow off the pad to finish the rep.',
      'Dropping into the bottom and bouncing out of a locked elbow.',
      'Letting the armpit slide back off the top of the pad.',
      'Curling the wrist in to help the lift.',
    ],
    goodFormFeels:
      'A strong squeeze in the front of the upper arm, the upper arm quiet on the pad, and a slow, controlled lowering into the stretch.',
    stopRules: [
      'Stop the set when the elbow lifts off the pad or you can no longer lower slowly to an almost straight arm.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Take the bottom of each rep slowly, and never relax into a locked elbow with the weight on.',
      'Start with your weaker arm, then match the reps on the other side.',
    ],
    easierSubstitution: {
      exerciseId: 'machine-preacher-curl',
      name: 'Machine Preacher Curl',
      reason: 'The machine guides the path and the weight changes in small steps.',
    },
    equipmentSubstitution: {
      exerciseId: 'bayesian-cable-curl',
      name: 'Bayesian Cable Curl',
      reason: 'Use when no preacher bench is free. It also trains the biceps from a long stretch.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'hammer-curl',
        name: 'Hammer Curl',
        reason: 'A palms in grip that shifts the bias to the brachialis and forearm.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Upper arm flat on the angled pad, arm almost straight, palm up on the dumbbell.',
          ...PREACHER,
          armNear: [50, 65],
          props: [...PREACHER_PROPS, { type: 'dumbbell', at: 'hands' }],
        },
        {
          label: 'Top',
          caption: 'Curl until the forearm is close to vertical, elbow still on the pad.',
          ...PREACHER,
          armNear: [50, 170],
          props: [...PREACHER_PROPS, { type: 'dumbbell', at: 'hands' }, { type: 'arrow', from: [142, 112], to: [142, 80] }],
        },
        {
          label: 'Finish',
          caption: 'Lower slowly to an almost straight arm, just short of a hard lockout.',
          ...PREACHER,
          armNear: [50, 65],
          props: [...PREACHER_PROPS, { type: 'dumbbell', at: 'hands' }, { type: 'arrow', from: [142, 80], to: [142, 112] }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Cable Rope Hammer Curl
  {
    id: 'rope-hammer-curl',
    name: 'Cable Rope Hammer Curl',
    aliases: ['Rope hammer curl', 'Cable hammer curl'],
    kind: 'strength',
    purpose:
      'Builds the brachialis and brachioradialis, with help from the biceps, for thicker upper arms and forearms and sturdy elbows for pulling and gripping. The cable keeps tension on at the bottom, where dumbbells feel light.',
    equipment: ['Low cable pulley', 'Rope attachment'],
    setup: [
      'Set the pulley at the lowest position and attach a rope.',
      'Hold one rope end in each hand with your palms facing each other, thumbs up.',
      'Step back about one step so the cable has tension when your arms are straight.',
      'Stand tall with your feet hip width apart and your elbows at your sides.',
    ],
    steps: [
      'Start with your arms fully straight and the rope in front of your thighs.',
      'Curl the rope up by bending at the elbows, palms still facing each other.',
      'Keep your elbows at your sides. A little forward drift at the top is fine.',
      'Stop when your forearms are close to vertical and squeeze briefly.',
      'Lower slowly until your arms are fully straight again.',
    ],
    breathing: 'Breathe out as you curl. Breathe in as you lower.',
    tempo:
      '2 1 1 1 means two seconds down, a one second pause with straight arms, one second up, and a one second squeeze at the top.',
    rangeOfMotion:
      'Go from fully straight arms to your hands near your shoulders, without the elbows swinging forward.',
    muscles: {
      primary: ['brachialis', 'brachioradialis'],
      secondary: ['biceps'],
    },
    emphasisNote:
      'The palms facing grip biases the brachialis and brachioradialis. The biceps still helps bend the elbow, a little less than in a palms up curl. The brachialis lies under the biceps, so building it also adds to the size of the upper arm.',
    movementPattern: 'elbow_flexion',
    joints: ['Elbow'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['elbow', 'wrist_grip'],
    commonMistakes: [
      'Swinging the trunk to start each rep.',
      'Letting the elbows travel forward so the shoulders help.',
      'Letting the rope drop quickly on the way down.',
      'Stopping short of straight arms at the bottom.',
    ],
    goodFormFeels:
      'Work along the top of the forearm and the outside of the upper arm, with elbows that stay by your sides.',
    stopRules: [
      'Stop the set when you start swinging or the elbows drift forward.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'If your elbow already feels sore from hitting or blocking, lower the weight and keep the reps smooth.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Seated dumbbell hammer curl',
      reason: 'Sitting against a bench back removes body swing, so strict reps are easier.',
    },
    equipmentSubstitution: {
      exerciseId: 'hammer-curl',
      name: 'Hammer Curl',
      reason: 'Use dumbbells when no cable is free.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'cable-reverse-curl',
        name: 'Cable Reverse Curl',
        reason: 'A palms down grip on the same pulley that shifts even more work to the forearm.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Stand tall facing a low pulley, rope in front of the thighs, palms facing each other.',
          ...STAND,
          armNear: [14, 18],
          props: [LOW_PULLEY_FRONT, { type: 'cable', from: 'hands', to: [178, 162] }, { type: 'handle', at: 'hands' }],
        },
        {
          label: 'Top',
          caption: 'Curl up with the palms still facing each other until the forearms are close to vertical.',
          ...STAND,
          armNear: [16, 155],
          props: [
            LOW_PULLEY_FRONT,
            { type: 'cable', from: 'hands', to: [178, 162] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [140, 96], to: [140, 60] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Lower slowly until the arms are fully straight again.',
          ...STAND,
          armNear: [14, 18],
          props: [
            LOW_PULLEY_FRONT,
            { type: 'cable', from: 'hands', to: [178, 162] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [140, 60], to: [140, 96] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Cable Reverse Curl
  {
    id: 'cable-reverse-curl',
    name: 'Cable Reverse Curl',
    aliases: ['Reverse grip cable curl', 'Palms down cable curl'],
    kind: 'strength',
    purpose:
      'Builds the brachioradialis on the top of the forearm and the brachialis under the biceps, along with the muscles on the back of the forearm. The palms down grip hands more of the work to these muscles, which helps grip strength, the elbows, and forearm size.',
    equipment: ['Low cable pulley', 'Straight bar attachment'],
    setup: [
      'Set the pulley at the lowest position and attach a straight bar.',
      'Grip the bar with your palms facing down, hands about shoulder width apart.',
      'Step back about one step so the cable has tension when your arms are straight.',
      'Stand tall with your elbows at your sides and your wrists straight.',
    ],
    steps: [
      'Start with your arms fully straight and the bar in front of your thighs.',
      'Curl the bar up by bending at the elbows, palms still facing down and wrists straight.',
      'Keep your elbows at your sides.',
      'Stop when your forearms are close to vertical and squeeze briefly.',
      'Lower slowly until your arms are fully straight again.',
    ],
    breathing: 'Breathe out as you curl. Breathe in as you lower.',
    tempo:
      '2 1 1 1 means two seconds down, a one second pause with straight arms, one second up, and a one second squeeze at the top.',
    rangeOfMotion:
      'Go from fully straight arms to the bar near your shoulders. Keep the wrists straight, in line with the forearms, the whole way.',
    muscles: {
      primary: ['brachioradialis', 'brachialis'],
      secondary: ['forearm_extensors', 'biceps'],
    },
    emphasisNote:
      'Turning the palms down puts the biceps in a weaker position, so the brachioradialis and brachialis take a larger share of the work. The wrist extensors on the back of the forearm work to keep the wrists straight, and the biceps still helps. Expect to use less weight than in a palms up curl.',
    movementPattern: 'elbow_flexion',
    joints: ['Elbow', 'Wrist'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['elbow', 'wrist_grip'],
    commonMistakes: [
      'Letting the wrists bend back under the bar.',
      'Swinging the trunk to start each rep.',
      'Letting the elbows drift forward.',
      'Using a weight so heavy that the range shrinks.',
    ],
    goodFormFeels:
      'Work along the top of the forearm near the elbow, straight wrists, and elbows that stay by your sides.',
    stopRules: [
      'Stop the set when your wrists bend back or you start swinging.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'These muscles attach at the outside of the elbow, which hitting also loads. Keep the weight moderate and the reps smooth.',
    ],
    easierSubstitution: {
      exerciseId: 'rope-hammer-curl',
      name: 'Cable Rope Hammer Curl',
      reason: 'The palms facing grip is easier on the wrists and trains the same forearm muscles.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Dumbbell reverse curl',
      reason: 'Use dumbbells when no cable is free. Keep the palms down and the wrists straight.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'hammer-curl',
        name: 'Hammer Curl',
        reason: 'A palms in dumbbell curl that trains the brachialis and brachioradialis with less wrist strain.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Stand tall facing a low pulley, bar in front of the thighs, palms facing down.',
          ...STAND,
          armNear: [14, 18],
          props: [LOW_PULLEY_FRONT, { type: 'cable', from: 'hands', to: [178, 162] }, { type: 'handle', at: 'hands' }],
        },
        {
          label: 'Top',
          caption: 'Curl up with the palms down and the wrists straight until the forearms are close to vertical.',
          ...STAND,
          armNear: [16, 155],
          props: [
            LOW_PULLEY_FRONT,
            { type: 'cable', from: 'hands', to: [178, 162] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [140, 96], to: [140, 60] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Lower slowly until the arms are fully straight again.',
          ...STAND,
          armNear: [14, 18],
          props: [
            LOW_PULLEY_FRONT,
            { type: 'cable', from: 'hands', to: [178, 162] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [140, 60], to: [140, 96] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Dumbbell Shrug
  {
    id: 'dumbbell-shrug',
    name: 'Dumbbell Shrug',
    aliases: ['Dumbbell trap shrug'],
    kind: 'strength',
    purpose:
      'Builds the upper traps, the muscles that run from the neck to the tops of the shoulders and lift the shoulder blades. They also help turn the shoulder blades upward when you reach overhead to hit and block. Dumbbells at your sides let the shoulders lift straight up and drop into a full stretch at the bottom.',
    equipment: ['A pair of dumbbells'],
    setup: [
      'Stand tall with your feet hip width apart and a dumbbell in each hand.',
      'Hold the dumbbells at your sides with your palms facing your thighs.',
      'Keep your arms straight and relaxed, like hooks.',
      'Let the dumbbells draw your shoulders down so you feel a stretch along the tops of your shoulders.',
    ],
    steps: [
      'Lift your shoulders straight up toward your ears, keeping your arms straight.',
      'Hold the top for one second.',
      'Lower slowly until the weight draws your shoulders all the way down into a full stretch.',
      'Move straight up and down. Do not roll the shoulders forward or back.',
    ],
    breathing: 'Breathe out as you lift. Breathe in as you lower.',
    tempo:
      '2 1 1 1 means two seconds down, a one second pause in the stretch at the bottom, one second up, and a one second hold at the top.',
    rangeOfMotion:
      'Go from the shoulders drawn fully down by the weight to the shoulders as high toward the ears as they go. Keep the arms straight and the head still.',
    muscles: {
      primary: ['traps_upper'],
      secondary: ['forearm_flexors', 'traps_middle'],
    },
    emphasisNote:
      'Lifting straight up biases the upper traps. The middle traps help hold the shoulder blades steady, and the forearms work hard to hold the dumbbells. Letting the weight draw the shoulders all the way down trains the upper traps through their full length. Rolling the shoulders adds no useful work, so keep the path straight up and down.',
    movementPattern: 'shoulder_elevation',
    joints: ['Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['wrist_grip', 'neck'],
    commonMistakes: [
      'Rolling the shoulders in circles.',
      'Bending the elbows to help the lift.',
      'Pushing the head forward or looking down.',
      'Cutting the stretch short at the bottom.',
      'Bouncing the weight at the bottom.',
    ],
    goodFormFeels:
      'A squeeze along the tops of the shoulders up toward the neck, arms that hang like hooks, and a head that stays still.',
    stopRules: [
      'Stop the set when the height of the shrug shrinks, the elbows start to bend, or your grip starts to slip.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Your grip may tire before your traps. Set the dumbbells down with control rather than letting them drop.',
      'Stop the exercise if you feel a headache, neck pain, or tingling in the arms, and tell a parent or coach.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Seated dumbbell shrug',
      reason: 'Sitting on the end of a bench removes body swing, so strict reps with lighter dumbbells are easier.',
    },
    equipmentSubstitution: {
      exerciseId: 'smith-shrug',
      name: 'Smith Machine Shrug',
      reason: 'Use when the heavy dumbbells are busy. The bar rests on its hooks between sets.',
    },
    otherSubstitutions: [
      {
        exerciseId: null,
        name: 'Cable shrug',
        reason: 'Hold a straight bar on a low pulley and shrug with the same technique.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Front view. Stand tall, dumbbells at the sides, shoulders drawn down by the weight.',
          ...FRONT,
          armNear: [24, 12],
          armFar: [-24, -12],
          props: [
            { type: 'dumbbell', at: 'nearHand' },
            { type: 'dumbbell', at: 'farHand' },
          ],
        },
        {
          label: 'Top',
          caption: 'Front view. Lift the shoulders straight up toward the ears, arms straight, and hold one second.',
          ...FRONT,
          armNear: [24, 12],
          armFar: [-24, -12],
          props: [
            { type: 'dumbbell', at: 'nearHand' },
            { type: 'dumbbell', at: 'farHand' },
            { type: 'arrow', from: [124, 56], to: [124, 34] },
            { type: 'arrow', from: [75, 56], to: [75, 34] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Front view. Lower slowly into a full stretch. No rolling the shoulders.',
          ...FRONT,
          armNear: [24, 12],
          armFar: [-24, -12],
          props: [
            { type: 'dumbbell', at: 'nearHand' },
            { type: 'dumbbell', at: 'farHand' },
            { type: 'arrow', from: [124, 34], to: [124, 56] },
            { type: 'arrow', from: [75, 34], to: [75, 56] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Smith Machine Shrug
  {
    id: 'smith-shrug',
    name: 'Smith Machine Shrug',
    aliases: ['Smith shrug'],
    kind: 'strength',
    purpose:
      'Builds the upper traps with a bar that runs on fixed rails, so you can load it well and rest it on the hooks without a spotter. Studies comparing machines and free weights find that both build muscle well when you train with similar effort.',
    equipment: ['Smith machine'],
    setup: [
      'Set the bar at about mid thigh height, and set the safety stops a little below that.',
      'Stand close to the bar and grip it with your palms facing you, hands just outside your thighs.',
      'Stand up tall with the bar, turn it to unhook it, and let it hang in front of your thighs with straight arms.',
      'Let the bar draw your shoulders down so you feel a stretch along the tops of your shoulders.',
    ],
    steps: [
      'Lift your shoulders straight up toward your ears, keeping your arms straight.',
      'Hold the top for one second.',
      'Lower slowly until the bar draws your shoulders all the way down into a full stretch.',
      'Move straight up and down. Do not roll the shoulders forward or back.',
      'After the last rep, turn the bar to set it back on the hooks.',
    ],
    breathing: 'Breathe out as you lift. Breathe in as you lower.',
    tempo:
      '2 1 1 1 means two seconds down, a one second pause in the stretch at the bottom, one second up, and a one second hold at the top.',
    rangeOfMotion:
      'Go from the shoulders drawn fully down by the bar to the shoulders as high toward the ears as they go. Keep the arms straight and the bar close to your thighs.',
    muscles: {
      primary: ['traps_upper'],
      secondary: ['forearm_flexors', 'traps_middle'],
    },
    emphasisNote:
      'Lifting straight up biases the upper traps, and the fixed rails keep the bar on a straight path so you can focus on a full range. The middle traps help hold the shoulder blades steady, and the forearms work hard to hold the bar. Letting the bar draw the shoulders all the way down trains the upper traps through their full length.',
    movementPattern: 'shoulder_elevation',
    joints: ['Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['wrist_grip', 'neck'],
    commonMistakes: [
      'Rolling the shoulders in circles.',
      'Bending the elbows or the knees to help the lift.',
      'Standing too far from the bar so it pulls you forward.',
      'Cutting the stretch short at the bottom.',
    ],
    goodFormFeels:
      'A squeeze along the tops of the shoulders up toward the neck, arms that hang like hooks, and a bar that slides straight up and down close to your thighs.',
    stopRules: [
      'Stop the set when the height of the shrug shrinks, the elbows start to bend, or your grip starts to slip.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Set the safety stops a little below the bar before you start, so a slipped grip ends on the stops.',
      'Turn the bar back onto the hooks after the last rep before you let go.',
      'Stop the exercise if you feel a headache, neck pain, or tingling in the arms, and tell a parent or coach.',
    ],
    easierSubstitution: {
      exerciseId: 'dumbbell-shrug',
      name: 'Dumbbell Shrug',
      reason: 'Lighter dumbbells need no setup and let each shoulder move freely.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Cable shrug',
      reason: 'Hold a straight bar on a low pulley when the Smith machine is busy.',
    },
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Stand tall with the Smith bar hanging in front of the thighs and the arms straight.',
          ...STAND,
          armNear: [8, 8],
          props: [
            { type: 'line', x1: 103, y1: 8, x2: 103, y2: 172 },
            { type: 'line', x1: 96, y1: 120, x2: 118, y2: 120 },
            { type: 'barbell', at: 'hands' },
          ],
        },
        {
          label: 'Top',
          caption: 'Lift the shoulders straight up toward the ears and hold one second. The arms stay straight.',
          ...STAND,
          armNear: [8, 8],
          props: [
            { type: 'line', x1: 103, y1: 8, x2: 103, y2: 172 },
            { type: 'line', x1: 96, y1: 120, x2: 118, y2: 120 },
            { type: 'barbell', at: 'hands' },
            { type: 'arrow', from: [128, 60], to: [128, 36] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Lower slowly into a full stretch. No rolling the shoulders.',
          ...STAND,
          armNear: [8, 8],
          props: [
            { type: 'line', x1: 103, y1: 8, x2: 103, y2: 172 },
            { type: 'line', x1: 96, y1: 120, x2: 118, y2: 120 },
            { type: 'barbell', at: 'hands' },
            { type: 'arrow', from: [128, 36], to: [128, 60] },
          ],
        },
      ],
    },
  },
];
