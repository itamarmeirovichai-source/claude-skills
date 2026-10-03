import { EFFORT_RULE } from './effort';
import type { ExerciseContent, Pose, PoseProp } from '../types';

// Upper body strength library. Order matches UPPER_IDS in ids.ts.
// Poses are side views unless the caption says front view. Frontal plane
// movements (lateral raises, external rotation) read far better from the front.

const PAIN_RULE =
  'Pain of 4 out of 10 or higher, or pain that worsens or changes your technique, pauses this exercise. Report it to a parent, coach, or clinician.';

// ---------- Shared pose pieces ----------

type Base = Pick<Pose, 'trunk' | 'hip' | 'legNear' | 'legFar' | 'footX' | 'head'>;

/** Lying face up on a flat bench, head to the left, feet on the floor. */
const LYING: Base = { trunk: -90, hip: [130, 116], legNear: [68, -10] };
const FLAT_BENCH: PoseProp = { type: 'bench', x: 55, y: 125, w: 88 };

/** Low incline bench, about 40 degrees, with a seat under the hips. */
const INCLINE: Base = { trunk: 230, hip: [122, 128], legNear: [83, -12] };
const INCLINE_PROPS: PoseProp[] = [
  { type: 'line', x1: 88, y1: 118, x2: 88, y2: 172 },
  { type: 'bench', x: 66, y: 94, w: 58, h: 8, angle: 40 },
  { type: 'bench', x: 100, y: 137, w: 40 },
];

/** Seated chest press with a slightly reclined back pad. */
const CHEST_PRESS: Base = { trunk: 188, hip: [82, 132], legNear: [90, 0] };
const CHEST_PRESS_PROPS: PoseProp[] = [
  { type: 'bench', x: 58, y: 140, w: 46 },
  { type: 'bench', x: 69, y: 130, w: 60, h: 8, angle: -98 },
];

/** Pulldown seat with the thighs under a pad and a slight lean back. */
const PULLDOWN: Base = { trunk: 190, hip: [92, 132], legNear: [90, 0] };
const PULLDOWN_PROPS: PoseProp[] = [
  { type: 'bench', x: 68, y: 140, w: 44 },
  { type: 'pad', x: 116, y: 115, w: 22, h: 9 },
];

/** Upright seat with a thigh pad for the high row. */
const HIGH_ROW: Base = { trunk: 178, hip: [82, 132], legNear: [90, 0] };
const HIGH_ROW_PROPS: PoseProp[] = [
  { type: 'bench', x: 58, y: 140, w: 46 },
  { type: 'pad', x: 106, y: 115, w: 22, h: 9 },
];

/** Low seat, feet on a platform, trunk upright. */
const CABLE_ROW: Base = { trunk: 180, hip: [70, 140], legNear: [100, 72, 170] };
const CABLE_ROW_PROPS: PoseProp[] = [
  { type: 'bench', x: 42, y: 148, w: 48 },
  { type: 'pad', x: 153, y: 124, w: 6, h: 30 },
  { type: 'line', x1: 156, y1: 154, x2: 156, y2: 172 },
  { type: 'line', x1: 190, y1: 70, x2: 190, y2: 172 },
];

/** Seated facing the machine with the chest on a pad. */
const REAR_FLY: Base = { trunk: 180, hip: [80, 132], legNear: [90, 0] };
const REAR_FLY_PROPS: PoseProp[] = [
  { type: 'line', x1: 150, y1: 28, x2: 150, y2: 172 },
  { type: 'line', x1: 98, y1: 108, x2: 150, y2: 108 },
  { type: 'bench', x: 56, y: 140, w: 46 },
  { type: 'pad', x: 90, y: 88, w: 8, h: 34 },
];

/** Standing, feet hip width. */
const STAND: Base = { trunk: 180, legNear: [0, 0], legFar: [3, -3] };
/** Standing with a small stagger for cable pulls. */
const STAGGER: Base = { trunk: 180, legNear: [8, 0], legFar: [-8, -4] };
/** Front view: the figure faces you, near side on the right of the picture. */
const FRONT: Base = { trunk: 180, legNear: [12, 0, 90], legFar: [-12, 0, -90], footX: 108 };

/** Seated on a machine, upper arms on an angled preacher pad. */
const PREACHER: Base = { trunk: 172, hip: [72, 132], legNear: [90, 0] };
const PREACHER_PROPS: PoseProp[] = [
  { type: 'line', x1: 104, y1: 118, x2: 104, y2: 172 },
  { type: 'bench', x: 48, y: 140, w: 46 },
  { type: 'bench', x: 75, y: 89, w: 36, h: 10, angle: 40 },
];

/** Standing, slight forward lean, facing a high pulley. */
const PUSHDOWN: Base = { trunk: 172, legNear: [0, 0], legFar: [3, -3] };

/** Split stance facing away from the pulley, trunk leaning forward. The head tips slightly forward so the arms stay visible beside it. */
const OVERHEAD: Base = { trunk: 150, head: 128, legNear: [18, 0], legFar: [-20, -20, 75], footX: 110 };

/** Seated on a bench, forearms resting on the thighs. */
const WRIST: Base = { trunk: 152, head: 165, hip: [70, 132], legNear: [90, 0] };
const WRIST_SEAT: PoseProp = { type: 'bench', x: 44, y: 140, w: 46 };

export const UPPER_EXERCISES: ExerciseContent[] = [
  // ---------- Chest ----------
  {
    id: 'barbell-bench-press',
    name: 'Barbell Bench Press',
    aliases: ['Flat bench press', 'Bench press'],
    kind: 'strength',
    purpose:
      'Builds pressing strength in the chest, triceps, and front of the shoulders. It supports a sturdy upper body for blocking, diving, and pushing yourself up off the floor.',
    equipment: ['Barbell', 'Flat bench with a rack', 'Safety arms or a spotter'],
    setup: [
      'Set the safety arms just below the height of your chest when you lie on the bench.',
      'Lie down with your eyes under the bar and your feet flat on the floor.',
      'Grip the bar a little wider than shoulder width, wrists stacked over the elbows.',
      'Pull your shoulder blades back and down so your upper back feels tight on the bench.',
      'Keep your head, upper back, and hips on the bench for the whole set.',
    ],
    steps: [
      'Unrack the bar with straight arms and bring it over your shoulders.',
      'Lower the bar with control to your lower chest, elbows angled partway between your sides and straight out.',
      'Touch the chest lightly. Do not bounce.',
      'Press the bar up and slightly back until it is over your shoulders again.',
      'Keep your feet pressing into the floor and your hips on the bench as you press.',
      'Rerack only when your arms are straight and the bar is under control.',
    ],
    breathing:
      'Breathe in and brace before you lower the bar. Hold it through the bottom, then breathe out as the bar passes the hardest part of the press.',
    tempo: '2 1 1 0 means two seconds down, a one second pause touching the chest lightly, one second up, no rest at the top.',
    rangeOfMotion:
      'Lower the bar until it lightly touches your lower chest, then press to straight arms without slamming into the top. Use a shorter range only if a coach tells you to.',
    muscles: {
      primary: ['pec_sternal'],
      secondary: ['triceps', 'delt_anterior', 'pec_clavicular'],
    },
    emphasisNote:
      'A medium grip on a flat bench biases the middle and lower chest. The triceps and front shoulders help through the whole press, and they do more when the grip is closer. No muscle switches off.',
    movementPattern: 'horizontal_push',
    joints: ['Shoulder', 'Elbow', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder', 'elbow'],
    commonMistakes: [
      'Flaring the elbows straight out to the sides.',
      'Bouncing the bar off the chest.',
      'Lifting the hips off the bench to finish a rep.',
      'Letting the shoulder blades slide apart so the shoulders roll forward.',
      'Letting the wrists bend far back so the bar sits in the fingers.',
    ],
    goodFormFeels:
      'Your upper back feels pinned to the bench, the bar moves in a smooth slight arc, and the effort sits across the chest and the back of the arms rather than in the front of the shoulder joint.',
    stopRules: [
      'Stop the set when the bar slows sharply, drifts off its path, or your technique changes.',
      EFFORT_RULE.never,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Always use safety arms set just below chest height, or a spotter who knows how to help.',
      'Learn this lift with a qualified coach first. Never test a one rep maximum.',
      'Your shoulders also work hard in spiking and swimming this week. Keep the pressing smooth and stop the set if the front of the shoulder pinches.',
    ],
    easierSubstitution: {
      exerciseId: 'machine-bench-press',
      name: 'Machine Bench Press',
      reason: 'The machine guides the path and needs no spotter, so you can focus on control.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Dumbbell bench press',
      reason: 'Use when the rack is busy. Start lighter, because each arm has to steady its own dumbbell.',
    },
    otherSubstitutions: [
      { exerciseId: null, name: 'Push up', reason: 'No equipment needed. Put your hands on a bench to make it easier.' },
    ],
    loadIncrement: 'upper',
    failure: 'never',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Lie with the eyes under the bar, feet flat, and arms straight over the shoulders.',
          ...LYING,
          armNear: [180, 180],
          props: [FLAT_BENCH, { type: 'barbell', at: 'hands' }],
        },
        {
          label: 'Bottom',
          caption: 'Lower the bar to the lower chest. The elbows dip just below the bench line.',
          ...LYING,
          armNear: [50, 180],
          props: [FLAT_BENCH, { type: 'barbell', at: 'hands' }, { type: 'arrow', from: [128, 62], to: [128, 94] }],
        },
        {
          label: 'Finish',
          caption: 'Press back up over the shoulders with the hips and upper back still on the bench.',
          ...LYING,
          armNear: [180, 180],
          props: [FLAT_BENCH, { type: 'barbell', at: 'hands' }, { type: 'arrow', from: [128, 94], to: [128, 62] }],
        },
      ],
    },
  },
  {
    id: 'incline-barbell-bench-press',
    name: 'Incline Barbell Bench Press',
    aliases: ['Incline bench press'],
    kind: 'strength',
    purpose:
      'Trains pressing on an upward angle, which biases the upper chest and front shoulders. It sits between a flat press and an overhead press.',
    equipment: ['Barbell', 'Incline bench with a rack', 'Safety arms or a spotter'],
    setup: [
      'Set the bench to a low incline of about 30 to 40 degrees. Steeper angles hand more work to the shoulders.',
      'Set the safety arms just below the height of your upper chest.',
      'Sit back with your eyes just in front of the bar and your feet flat on the floor.',
      'Grip the bar a little wider than shoulder width and pull your shoulder blades back and down.',
    ],
    steps: [
      'Unrack the bar and hold it with straight arms over your shoulders.',
      'Lower the bar with control to your upper chest, just below the collarbones.',
      'Keep your elbows angled partway between your sides and straight out.',
      'Touch the chest lightly without bouncing.',
      'Press the bar straight up until it is back over your shoulders.',
    ],
    breathing:
      'Breathe in and brace before you lower the bar. Hold it through the bottom, then breathe out as the bar passes the hardest part of the press.',
    tempo: '2 1 1 0 means two seconds down, a one second pause on the upper chest, one second up, no rest at the top.',
    rangeOfMotion:
      'Lower until the bar lightly touches the upper chest, then press to straight arms. Keep your hips on the seat and your upper back on the pad.',
    muscles: {
      primary: ['pec_clavicular', 'delt_anterior'],
      secondary: ['triceps', 'pec_sternal'],
    },
    emphasisNote:
      'The incline angle biases the upper chest and the front of the shoulder. The middle chest and the triceps still do a large share of the work. The steeper the bench, the more the front shoulder takes over, which is why a low incline is used here.',
    movementPattern: 'horizontal_push',
    joints: ['Shoulder', 'Elbow', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder', 'elbow'],
    commonMistakes: [
      'Setting the bench so steep that it turns into a shoulder press.',
      'Lowering the bar to the neck or the middle of the chest instead of the upper chest.',
      'Arching so hard that the hips lift off the seat.',
      'Flaring the elbows straight out to the sides.',
    ],
    goodFormFeels:
      'Your upper back stays tight on the pad, the bar travels in a short straight line, and you feel the work in the upper chest and the front of the shoulders without any pinching.',
    stopRules: [
      'Stop the set when the bar slows sharply, drifts off its path, or your technique changes.',
      EFFORT_RULE.never,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Always use safety arms set just below upper chest height, or a spotter who knows how to help.',
      'Learn this lift with a qualified coach first. Never test a one rep maximum.',
      'This angle loads the front shoulder more than flat pressing, and your shoulders also work in spiking and swimming this week. Keep the incline low and stop the set at any pinch.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Incline machine press',
      reason: 'The machine guides the path and needs no spotter.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Incline dumbbell press',
      reason: 'Use when no incline rack is free. Start lighter, because each arm has to steady its own dumbbell.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'barbell-bench-press',
        name: 'Barbell Bench Press',
        reason: 'Use when no incline bench is free. The flat angle shifts the bias toward the middle chest.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'never',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Sit back on a low incline, feet flat, bar held straight over the shoulders.',
          ...INCLINE,
          armNear: [180, 180],
          props: [...INCLINE_PROPS, { type: 'barbell', at: 'hands' }],
        },
        {
          label: 'Bottom',
          caption: 'Lower the bar to the upper chest, just below the collarbones.',
          ...INCLINE,
          armNear: [25, 180],
          props: [...INCLINE_PROPS, { type: 'barbell', at: 'hands' }, { type: 'arrow', from: [118, 46], to: [118, 80] }],
        },
        {
          label: 'Finish',
          caption: 'Press straight up until the bar is back over the shoulders.',
          ...INCLINE,
          armNear: [180, 180],
          props: [...INCLINE_PROPS, { type: 'barbell', at: 'hands' }, { type: 'arrow', from: [118, 80], to: [118, 46] }],
        },
      ],
    },
  },
  {
    id: 'machine-bench-press',
    name: 'Machine Bench Press',
    aliases: ['Machine chest press', 'Seated chest press'],
    kind: 'strength',
    purpose:
      'Trains the chest, triceps, and front shoulders on a guided path. You can work close to your target effort safely without a spotter.',
    equipment: ['Chest press machine'],
    setup: [
      'Set the seat so the handles line up with the middle of your chest.',
      'Sit with your back and head against the pad and your feet flat on the floor.',
      'Grip the handles with straight wrists, knuckles in line with your forearms.',
      'Set your shoulder blades back and down before the first rep.',
      'If the handles have a start position setting, choose one where they begin level with your chest, not far behind it.',
    ],
    steps: [
      'Press the handles forward until your arms are straight but not locked hard.',
      'Keep your back on the pad and your shoulders down away from your ears.',
      'Let the handles come back slowly until your hands are level with your chest.',
      'Pause briefly in that stretch without letting the weight stack rest.',
      'Press again along the same path.',
    ],
    breathing: 'Breathe in as the handles come back. Breathe out as you press.',
    tempo: '2 1 1 0 means two seconds as the handles come back, a one second pause at the chest, one second to press, no rest at the front.',
    rangeOfMotion:
      'Bring the handles back until they are level with your chest, or a little behind if your shoulders stay comfortable. Press to nearly straight arms.',
    muscles: {
      primary: ['pec_sternal'],
      secondary: ['triceps', 'delt_anterior', 'pec_clavicular'],
    },
    emphasisNote:
      'Like the barbell press, this biases the middle chest with help from the triceps and front shoulders. Seat height changes the angle a little. A lower seat, so you press slightly upward, tends to bias the upper chest. No part of the chest switches off.',
    movementPattern: 'horizontal_push',
    joints: ['Shoulder', 'Elbow', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder', 'elbow'],
    commonMistakes: [
      'Setting the seat so the handles start at the neck or the belly.',
      'Letting the handles pull the shoulders forward off the pad.',
      'Shrugging the shoulders up toward the ears as you press.',
      'Letting the weight stack crash between reps.',
    ],
    goodFormFeels:
      'Your back stays on the pad, the press feels smooth, and the work sits in the chest and the back of the arms.',
    stopRules: [
      'Stop the set when the press slows sharply, your back leaves the pad, or your technique changes.',
      EFFORT_RULE.last,
      PAIN_RULE,
    ],
    safetyNotes: [
      'The machine removes the need for a spotter, but keep the same control you would use with a barbell.',
      'Your shoulders also work in spiking and swimming this week. Stop the set if the front of the shoulder pinches.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Incline push up',
      reason: 'Hands on a bench make the push up lighter, and you can do it anywhere.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Dumbbell bench press',
      reason: 'Use when the machine is taken. Start lighter, because each arm has to steady its own dumbbell.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'barbell-bench-press',
        name: 'Barbell Bench Press',
        reason: 'A free weight option once a coach has taught you the lift and safety arms or a spotter are ready.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'last',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Sit tall against the pad with the handles level with the middle of the chest.',
          ...CHEST_PRESS,
          armNear: [-30, 100],
          props: [...CHEST_PRESS_PROPS, { type: 'handle', at: 'hands' }],
        },
        {
          label: 'Press',
          caption: 'Press forward to nearly straight arms, back and head still on the pad.',
          ...CHEST_PRESS,
          armNear: [76, 84],
          props: [...CHEST_PRESS_PROPS, { type: 'handle', at: 'hands' }, { type: 'arrow', from: [98, 70], to: [130, 70] }],
        },
        {
          label: 'Finish',
          caption: 'Let the handles come back slowly until they are level with the chest.',
          ...CHEST_PRESS,
          armNear: [-30, 100],
          props: [...CHEST_PRESS_PROPS, { type: 'handle', at: 'hands' }, { type: 'arrow', from: [130, 70], to: [98, 70] }],
        },
      ],
    },
  },
  {
    id: 'flat-cable-fly',
    name: 'Flat Cable Fly',
    aliases: ['Lying cable fly', 'Flat bench cable fly'],
    kind: 'strength',
    purpose:
      'Trains the chest through a long, controlled stretch with steady cable tension. It adds chest work with very little triceps or elbow stress.',
    equipment: ['Two low cable pulleys', 'Flat bench', 'Two D handles'],
    setup: [
      'Place a flat bench between two low pulleys so the pulleys line up with your chest.',
      'Take one handle in each hand, then lie back with your feet flat and your head on the bench.',
      'Start with the handles together over your chest and a soft bend in your elbows.',
      'Pull your shoulder blades back and down so your chest feels high.',
    ],
    steps: [
      'Keeping the same soft elbow bend, open your arms out to the sides in a wide arc.',
      'Lower until your hands are about level with the bench or you feel a clear stretch across the chest.',
      'Pause briefly without letting the shoulders roll forward.',
      'Bring the handles back up and together over your chest, as if hugging a wide tree.',
      'Keep your hips and upper back on the bench the whole time.',
    ],
    breathing: 'Breathe in as your arms open. Breathe out as you bring the handles together.',
    tempo:
      '2 1 1 1 means two seconds opening the arms, a one second pause in the stretch, one second to bring the handles together, and a one second squeeze at the top.',
    rangeOfMotion:
      'Open until your hands are about level with the bench. Stop sooner if you feel strain in the front of the shoulder rather than a stretch across the chest.',
    muscles: {
      primary: ['pec_sternal'],
      secondary: ['pec_clavicular', 'delt_anterior'],
    },
    emphasisNote:
      'A flat fly with the handles meeting over the middle of the chest biases the middle and lower chest. Bringing the handles together higher, over the face, tilts more work toward the upper chest and front shoulders. The whole chest works in every rep.',
    movementPattern: 'shoulder_horizontal_adduction',
    joints: ['Shoulder', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder'],
    commonMistakes: [
      'Bending and straightening the elbows so the fly turns into a press.',
      'Dropping the hands too low and straining the front of the shoulder.',
      'Letting the shoulders roll forward off the bench at the top.',
      'Using a weight so heavy that you jerk out of the stretch.',
    ],
    goodFormFeels:
      'A long stretch across the chest at the bottom, a firm squeeze in the middle of the chest at the top, and elbows that keep the same bend.',
    stopRules: [
      'Stop the set when the elbows start bending and straightening, or your technique changes in any other way.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Keep the load light to moderate. The stretch at the bottom is where the shoulder is most exposed.',
      'Your shoulders also work in spiking and swimming this week. Shorten the range if the front of the shoulder aches.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Pec deck machine fly',
      reason: 'You sit upright on a fixed path, with no need to set up two cables.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Dumbbell fly on a flat bench',
      reason: 'Use when no cables are free. Keep the dumbbells light, because they feel heaviest in the stretch and light at the top.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'machine-bench-press',
        name: 'Machine Bench Press',
        reason: 'A chest option with a shorter stretch if the wide arm position bothers your shoulder.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Lie on the bench with the handles together over the chest and a soft elbow bend.',
          ...LYING,
          armNear: [165, 180],
          props: [
            FLAT_BENCH,
            { type: 'cable', from: 'hands', to: [36, 168] },
            { type: 'cable', from: 'hands', to: [128, 168] },
            { type: 'handle', at: 'hands' },
          ],
        },
        {
          label: 'Stretch',
          caption: 'Open both arms out wide in an arc, elbows softly bent, until the chest stretches.',
          ...LYING,
          armNear: [50, 75],
          armFar: [-50, -75],
          props: [
            FLAT_BENCH,
            { type: 'cable', from: 'farHand', to: [36, 168] },
            { type: 'cable', from: 'nearHand', to: [128, 168] },
            { type: 'handle', at: 'nearHand' },
            { type: 'handle', at: 'farHand' },
          ],
        },
        {
          label: 'Finish',
          caption: 'Bring the handles back up and together over the chest.',
          ...LYING,
          armNear: [165, 180],
          props: [
            FLAT_BENCH,
            { type: 'cable', from: 'hands', to: [36, 168] },
            { type: 'cable', from: 'hands', to: [128, 168] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [125, 95], to: [106, 70] },
          ],
        },
      ],
    },
  },

  // ---------- Back ----------
  {
    id: 'wide-grip-lat-pulldown',
    name: 'Wide Grip Lat Pulldown',
    aliases: ['Lat pulldown'],
    kind: 'strength',
    purpose:
      'Builds the lats and upper back, the muscles that drive the arm down in a spike and pull you through the water when you swim.',
    equipment: ['Lat pulldown station', 'Long straight bar'],
    setup: [
      'Set the thigh pad so your thighs are held firmly and your feet are flat.',
      'Grip the bar with palms facing away, hands a little wider than shoulder width.',
      'Sit down with straight arms and lean back only slightly from the hips.',
      'Lift your chest and set your shoulders down away from your ears.',
    ],
    steps: [
      'Start the pull by drawing your shoulder blades down.',
      'Drive your elbows down toward your sides as the bar moves toward your upper chest.',
      'Pull until the bar is between your chin and upper chest, chest still lifted.',
      'Pause briefly without leaning further back.',
      'Let the bar rise slowly until your arms are straight and you feel the lats stretch.',
    ],
    breathing: 'Breathe out as you pull down. Breathe in as the bar rises.',
    tempo: '2 0 1 1 means two seconds to let the bar rise, no pause at the top, one second to pull down, and a one second hold at the bottom.',
    rangeOfMotion:
      'Go from straight arms with the shoulders reaching up to the bar at your upper chest. Keep the bar in front of your head and never pull it behind the neck.',
    muscles: {
      primary: ['lats'],
      secondary: ['teres_major', 'biceps', 'brachialis', 'traps_lower', 'traps_middle', 'rhomboids'],
    },
    emphasisNote:
      'A wide grip with palms facing away biases the lats and the muscles that pull the shoulder blades down. The biceps and brachialis help, a little less than with a close grip. A slight lean back adds some middle back work. The lats lead in every grip.',
    movementPattern: 'vertical_pull',
    joints: ['Shoulder', 'Elbow', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder', 'elbow', 'wrist_grip'],
    commonMistakes: [
      'Leaning far back so the pulldown turns into a row.',
      'Pulling the bar behind the neck.',
      'Shrugging the shoulders up at the top instead of setting them down.',
      'Swinging the body to move the weight.',
      'Stopping halfway up so the lats never lengthen.',
    ],
    goodFormFeels:
      'Your elbows drive down to your sides, you feel the pull along the sides of your back under the armpits, and your chest stays tall.',
    stopRules: [
      'Stop the set when you start leaning back or swinging, or your technique changes in any other way.',
      EFFORT_RULE.last,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Keep the bar in front of your face. Pulling behind the neck strains the shoulder.',
      'Your lats and shoulders also work hard in spiking and swimming this week, so keep every rep smooth and controlled.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Close neutral grip lat pulldown',
      reason: 'Palms facing each other let the elbows follow a more natural path, which most people find easier on the shoulders.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Assisted pull up',
      reason: 'Use when there is no pulldown station. Pick enough assistance to keep every rep smooth.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'one-arm-lat-pulldown',
        name: 'One Arm Lat Pulldown',
        reason: 'Trains one side at a time to even out the left and right.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'last',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Sit with the thighs under the pad and the arms reaching up to the bar.',
          ...PULLDOWN,
          armNear: [165, 175],
          props: [...PULLDOWN_PROPS, { type: 'cable', from: 'hands', to: [96, 4] }, { type: 'handle', at: 'hands' }],
        },
        {
          label: 'Pull',
          caption: 'Drive the elbows down and back until the bar reaches the upper chest.',
          ...PULLDOWN,
          armNear: [-35, 140],
          props: [
            ...PULLDOWN_PROPS,
            { type: 'cable', from: 'hands', to: [96, 4] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [130, 36], to: [130, 72] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Let the bar rise slowly until the arms are straight and the lats stretch.',
          ...PULLDOWN,
          armNear: [165, 175],
          props: [
            ...PULLDOWN_PROPS,
            { type: 'cable', from: 'hands', to: [96, 4] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [130, 72], to: [130, 36] },
          ],
        },
      ],
    },
  },
  {
    id: 'one-arm-lat-pulldown',
    name: 'One Arm Lat Pulldown',
    aliases: ['Single arm lat pulldown'],
    kind: 'strength',
    purpose:
      'Trains each lat on its own, so a stronger side cannot cover for a weaker one. Useful for a hitter whose hitting arm gets most of the work in practice.',
    equipment: ['Pulldown station or high cable pulley', 'Single D handle'],
    setup: [
      'Attach a single handle to the high pulley.',
      'Sit with your thighs under the pad and your feet flat.',
      'Reach up and take the handle with the palm facing forward or facing in, whichever feels better.',
      'Rest your free hand on the thigh pad and sit tall.',
    ],
    steps: [
      'Let the working arm reach up until you feel a stretch along the side of your back.',
      'Start the pull by drawing that shoulder blade down.',
      'Drive the elbow down toward your hip, close to your side.',
      'Finish with the hand near your shoulder and the elbow by your ribs.',
      'Let the handle rise slowly back to the full stretch.',
      'Finish all reps on one side, then switch.',
    ],
    breathing: 'Breathe out as you pull the elbow down. Breathe in as the arm rises.',
    tempo: '2 1 1 1 means two seconds to let the arm rise, a one second pause in the stretch, one second to pull, and a one second hold at the bottom.',
    rangeOfMotion:
      'Go from a long reach overhead to the elbow at your side. Keep your trunk facing forward instead of twisting to finish the rep.',
    muscles: {
      primary: ['lats', 'teres_major'],
      secondary: ['biceps', 'brachialis', 'traps_lower', 'forearm_flexors'],
    },
    emphasisNote:
      'Pulling the elbow down close to your side, toward the hip, biases the lats and teres major. Letting the elbow drift out wide shares more of the work with the upper back. The biceps and grip help in every rep.',
    movementPattern: 'vertical_pull',
    joints: ['Shoulder', 'Elbow', 'Shoulder blade'],
    laterality: 'unilateral',
    logSides: true,
    fatigueOverlap: ['shoulder', 'elbow', 'wrist_grip'],
    commonMistakes: [
      'Twisting the trunk to finish the pull.',
      'Leaning far away from the working side.',
      'Shrugging the shoulder up at the top of each rep.',
      'Pulling with the hand and biceps instead of driving the elbow down.',
    ],
    goodFormFeels:
      'A long stretch along the side of your back at the top, then a strong squeeze under the armpit as the elbow reaches your ribs.',
    stopRules: [
      'Stop the set when your trunk starts twisting, or your technique changes in any other way.',
      EFFORT_RULE.last,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Start with your weaker side, then do the same reps on the stronger side.',
      'Your lats and shoulders also work in spiking and swimming this week, so keep the reps smooth.',
    ],
    easierSubstitution: {
      exerciseId: 'wide-grip-lat-pulldown',
      name: 'Wide Grip Lat Pulldown',
      reason: 'Both arms share the load, and the trunk is easier to keep still.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'One arm dumbbell row',
      reason: 'Use when no cable is free. It trains the lats from a rowing angle, with your other hand on a bench.',
    },
    otherSubstitutions: [
      {
        exerciseId: null,
        name: 'Half kneeling one arm cable pulldown',
        reason: 'Kneel beside a high pulley when there is no pulldown seat.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'last',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Reach the working arm up to the handle. The free hand rests on the thigh pad.',
          ...PULLDOWN,
          armNear: [170, 178],
          armFar: [40, 80],
          props: [...PULLDOWN_PROPS, { type: 'cable', from: 'nearHand', to: [92, 4] }, { type: 'handle', at: 'nearHand' }],
        },
        {
          label: 'Pull',
          caption: 'Drive the elbow down to the side of the ribs, hand finishing near the shoulder.',
          ...PULLDOWN,
          armNear: [-32, 145],
          armFar: [40, 80],
          props: [
            ...PULLDOWN_PROPS,
            { type: 'cable', from: 'nearHand', to: [92, 4] },
            { type: 'handle', at: 'nearHand' },
            { type: 'arrow', from: [130, 36], to: [130, 72] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Let the arm rise slowly back to a full stretch before the next rep.',
          ...PULLDOWN,
          armNear: [170, 178],
          armFar: [40, 80],
          props: [
            ...PULLDOWN_PROPS,
            { type: 'cable', from: 'nearHand', to: [92, 4] },
            { type: 'handle', at: 'nearHand' },
            { type: 'arrow', from: [130, 72], to: [130, 36] },
          ],
        },
      ],
    },
  },
  {
    id: 'leverage-high-row',
    name: 'Leverage High Row',
    aliases: ['Machine high row', 'Plate loaded high row'],
    kind: 'strength',
    purpose:
      'Trains the middle back, lats, and rear shoulders with a pull from above and in front of you. It balances all the reaching and hitting you do overhead in volleyball.',
    equipment: ['High row machine, plate loaded or with a weight stack'],
    setup: [
      'Set the seat so the handles are a little above head height when your arms reach up.',
      'Sit tall with your thighs under the pad and your feet flat.',
      'Grip the handles and let your shoulders reach up and forward to start.',
      'Keep your chest lifted and your lower back in its natural curve.',
    ],
    steps: [
      'Start by drawing your shoulder blades down and together.',
      'Pull the handles down and back, driving your elbows toward your hips.',
      'Finish with the handles near your upper chest and your elbows just behind your body.',
      'Pause and squeeze between the shoulder blades.',
      'Return slowly until your arms are long and the shoulder blades have moved apart.',
    ],
    breathing: 'Breathe out as you pull. Breathe in as the handles return.',
    tempo: '2 0 1 1 means two seconds to let the handles return, no pause at the top, one second to pull, and a one second squeeze at the chest.',
    rangeOfMotion:
      'Go from a long reach with the shoulder blades apart to the elbows just behind your trunk. Do not force the elbows far back.',
    muscles: {
      primary: ['lats', 'traps_middle', 'rhomboids'],
      secondary: ['delt_posterior', 'teres_major', 'traps_lower', 'biceps', 'brachialis', 'brachioradialis'],
    },
    emphasisNote:
      'Keeping the elbows closer to your body biases the lats. Letting the elbows travel out wider biases the middle traps, rhomboids, and rear shoulders. The elbow flexors help in every rep.',
    movementPattern: 'high_pull',
    joints: ['Shoulder', 'Elbow', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder', 'elbow', 'wrist_grip'],
    commonMistakes: [
      'Leaning back to move the weight.',
      'Shrugging the shoulders up toward the ears.',
      'Pulling with the hands only, so the shoulder blades never move.',
      'Letting the handles yank the arms up at the top.',
    ],
    goodFormFeels:
      'The shoulder blades slide down and together, the effort sits across the middle back and under the armpits, and your trunk stays still.',
    stopRules: [
      'Stop the set when you start leaning back or shrugging, or your technique changes in any other way.',
      EFFORT_RULE.last,
      PAIN_RULE,
    ],
    safetyNotes: [
      'If the machine has separate arms, load them evenly and move them together unless your plan says to work one side.',
      'Your shoulders also work in spiking and swimming this week, so keep the return slow and controlled.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Resistance band high row',
      reason: 'A light band anchored high is simple to set up and good for learning the shoulder blade movement.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Kneeling high cable row',
      reason: 'Kneel facing a high pulley with two handles or a rope, and pull down and back toward your chest.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'seated-cable-row',
        name: 'Seated Cable Row',
        reason: 'A horizontal pull that trains the same middle back muscles.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'last',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Sit tall, thighs under the pad, arms reaching up and forward to the handles.',
          ...HIGH_ROW,
          armNear: [135, 140],
          props: [...HIGH_ROW_PROPS, { type: 'handle', at: 'hands' }],
        },
        {
          label: 'Pull',
          caption: 'Pull down and back until the handles reach the upper chest and the elbows pass the body.',
          ...HIGH_ROW,
          armNear: [-25, 115],
          props: [...HIGH_ROW_PROPS, { type: 'handle', at: 'hands' }, { type: 'arrow', from: [134, 48], to: [116, 82] }],
        },
        {
          label: 'Finish',
          caption: 'Return slowly until the arms are long and the shoulder blades spread.',
          ...HIGH_ROW,
          armNear: [135, 140],
          props: [...HIGH_ROW_PROPS, { type: 'handle', at: 'hands' }, { type: 'arrow', from: [116, 82], to: [134, 48] }],
        },
      ],
    },
  },
  {
    id: 'seated-cable-row',
    name: 'Seated Cable Row',
    aliases: ['Low cable row'],
    kind: 'strength',
    purpose:
      'Builds the middle back, lats, and rear shoulders. It keeps the shoulders balanced against all the pressing, hitting, and reaching in your week.',
    equipment: ['Seated cable row station', 'Close grip V handle'],
    setup: [
      'Sit on the seat with your feet on the platform and your knees slightly bent.',
      'Hold the V handle with your palms facing each other.',
      'Sit tall with your trunk upright and your arms straight in front of you.',
      'Brace your trunk lightly so it does not rock.',
    ],
    steps: [
      'Start the pull by drawing your shoulder blades back.',
      'Pull the handle to your lower ribs, keeping your elbows close to your sides.',
      'Pause and squeeze your shoulder blades together with your chest tall.',
      'Let the handle travel forward slowly until your arms are straight and your shoulder blades spread apart.',
      'Keep your trunk nearly still. A small lean forward at the stretch is fine, but do not swing.',
    ],
    breathing: 'Breathe out as you pull. Breathe in as the handle moves forward.',
    tempo: '2 0 1 1 means two seconds to let the handle return, no pause at the stretch, one second to pull, and a one second squeeze at the body.',
    rangeOfMotion:
      'Go from straight arms with the shoulder blades spread to the handle touching your lower ribs, chest tall at the finish.',
    muscles: {
      primary: ['lats', 'traps_middle', 'rhomboids'],
      secondary: ['delt_posterior', 'teres_major', 'biceps', 'brachialis', 'brachioradialis', 'forearm_flexors', 'erectors'],
    },
    emphasisNote:
      'A close grip with the elbows tucked biases the lats. A wide bar with the elbows out shifts more work to the middle traps, rhomboids, and rear shoulders. The biceps, forearms, and grip help in every rep, and the lower back muscles hold your trunk upright.',
    movementPattern: 'horizontal_pull',
    joints: ['Shoulder', 'Elbow', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['elbow', 'wrist_grip', 'low_back'],
    commonMistakes: [
      'Rocking the trunk back and forth to move the weight.',
      'Rounding the lower back at the stretch.',
      'Shrugging the shoulders toward the ears.',
      'Cutting the range short so the shoulder blades never move.',
    ],
    goodFormFeels:
      'Your trunk stays quiet, the shoulder blades glide back and forward, and the squeeze sits between the shoulder blades and along the sides of your back.',
    stopRules: [
      'Stop the set when your trunk starts rocking or your lower back rounds, or your technique changes in any other way.',
      EFFORT_RULE.last,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Keep your lower back in its natural curve. If it rounds at the stretch, shorten the reach or lower the weight.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Chest supported machine row',
      reason: 'The chest pad holds your trunk still, so you can focus on the shoulder blades.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'One arm dumbbell row',
      reason: 'Use when the cable station is busy. Support yourself with one hand and one knee on a bench.',
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
          caption: 'Sit tall, feet on the platform, knees slightly bent, arms straight toward the pulley.',
          ...CABLE_ROW,
          armNear: [72, 76],
          props: [...CABLE_ROW_PROPS, { type: 'cable', from: 'hands', to: [188, 116] }, { type: 'handle', at: 'hands' }],
        },
        {
          label: 'Pull',
          caption: 'Pull the handle to the lower ribs, elbows close to the sides, chest tall.',
          ...CABLE_ROW,
          armNear: [-25, 95],
          props: [
            ...CABLE_ROW_PROPS,
            { type: 'cable', from: 'hands', to: [188, 116] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [150, 90], to: [118, 90] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Let the handle travel forward slowly until the arms are straight again.',
          ...CABLE_ROW,
          armNear: [72, 76],
          props: [
            ...CABLE_ROW_PROPS,
            { type: 'cable', from: 'hands', to: [188, 116] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [118, 90], to: [150, 90] },
          ],
        },
      ],
    },
  },

  // ---------- Rear shoulder and rotator cuff ----------
  {
    id: 'reverse-machine-fly',
    name: 'Reverse Machine Fly',
    aliases: ['Rear delt machine fly', 'Reverse pec deck'],
    kind: 'strength',
    purpose:
      'Strengthens the rear shoulders and the muscles between the shoulder blades. They balance the front of the shoulder after lots of pressing and hitting.',
    equipment: ['Pec deck or rear delt fly machine'],
    setup: [
      'Set the seat so the handles are at shoulder height.',
      'Set the handles to the most forward position so your arms start in front of you.',
      'Sit facing the machine with your chest against the pad and your feet flat.',
      'Hold the handles with palms facing down or facing each other, elbows softly bent.',
    ],
    steps: [
      'Keeping the soft elbow bend, sweep the handles out and back in a wide arc.',
      'Lead with the backs of your hands and keep your arms at shoulder height.',
      'Stop when your arms are in line with your shoulders.',
      'Pause briefly and feel the backs of the shoulders working.',
      'Return slowly to the front.',
    ],
    breathing: 'Breathe out as your arms open. Breathe in as they return.',
    tempo: '2 0 1 1 means two seconds to return to the front, no pause there, one second to open the arms, and a one second hold with the arms out wide.',
    rangeOfMotion:
      'Go from arms in front of your chest to arms in line with your body. Going further back mostly squeezes the shoulder blades and can pinch the shoulder.',
    muscles: {
      primary: ['delt_posterior'],
      secondary: ['traps_middle', 'rhomboids', 'rotator_cuff'],
    },
    emphasisNote:
      'Keeping the shoulder blades fairly still biases the rear shoulders. Squeezing the shoulder blades together at the end adds more middle trap and rhomboid work. The rotator cuff helps turn the arm and keep the shoulder centred throughout.',
    movementPattern: 'shoulder_horizontal_abduction',
    joints: ['Shoulder', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder'],
    commonMistakes: [
      'Swinging the weight with body movement.',
      'Bending the elbows more as you pull, so it turns into a row.',
      'Shrugging the shoulders up toward the ears.',
      'Taking the arms far behind the body.',
    ],
    goodFormFeels:
      'A steady burn at the back of the shoulders, your chest stays on the pad, and your arms move like wide wings.',
    stopRules: [
      'Stop the set when the elbows bend more or the shoulders shrug, or your technique changes in any other way.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Use a light weight you control. The rear shoulders are small muscles that respond well to smooth reps.',
      'This counts toward your shoulder load for the week alongside spiking and swimming.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Band pull apart',
      reason: 'A light band is easy to set up and good for learning the movement.',
    },
    equipmentSubstitution: {
      exerciseId: 'face-pull',
      name: 'Face Pull',
      reason: 'Uses a cable and rope to train the rear shoulders and upper back.',
    },
    otherSubstitutions: [
      {
        exerciseId: null,
        name: 'Chest supported dumbbell reverse fly',
        reason: 'Lie face down on an incline bench with light dumbbells when no machine is free.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Sit with the chest on the pad and the arms straight ahead at shoulder height.',
          ...REAR_FLY,
          armNear: [88, 92],
          props: [...REAR_FLY_PROPS, { type: 'handle', at: 'hands' }],
        },
        {
          label: 'Open',
          caption: 'Sweep the handles out and back in a wide arc until the arms line up with the shoulders.',
          ...REAR_FLY,
          armNear: [-88, -91],
          props: [...REAR_FLY_PROPS, { type: 'handle', at: 'hands' }, { type: 'arrow', from: [128, 52], to: [96, 52] }],
        },
        {
          label: 'Finish',
          caption: 'Return slowly to the front with the chest still on the pad.',
          ...REAR_FLY,
          armNear: [88, 92],
          props: [...REAR_FLY_PROPS, { type: 'handle', at: 'hands' }, { type: 'arrow', from: [96, 52], to: [128, 52] }],
        },
      ],
    },
  },
  {
    id: 'face-pull',
    name: 'Face Pull',
    aliases: ['Rope face pull', 'Cable face pull'],
    kind: 'strength',
    purpose:
      'Trains the rear shoulders, the middle and lower traps, and the rotator cuff muscles that turn the arm outward. This is shoulder care for a hitter who also swims.',
    equipment: ['Cable pulley', 'Rope attachment'],
    setup: [
      'Set the pulley at about face height and attach a rope.',
      'Hold the rope ends with palms facing each other and thumbs pointing back toward you.',
      'Step back until your arms are straight and the cable has tension.',
      'Stand tall with a small stagger in your feet and brace your trunk.',
    ],
    steps: [
      'Pull the rope toward your face, leading with your elbows high and wide.',
      'Separate the rope ends as they come toward you.',
      'Finish with your hands beside your ears and your knuckles turned up and back.',
      'Pause and squeeze between the shoulder blades.',
      'Let the rope return slowly until your arms are straight.',
    ],
    breathing: 'Breathe out as you pull. Breathe in as the rope returns.',
    tempo: '2 0 1 2 means two seconds to return, no pause with the arms straight, one second to pull, and a two second hold at the face.',
    rangeOfMotion:
      'Go from straight arms to your hands beside your ears with the elbows about level with your shoulders. Stop the pull before your lower back arches.',
    muscles: {
      primary: ['delt_posterior', 'rotator_cuff', 'traps_middle'],
      secondary: ['traps_lower', 'rhomboids'],
    },
    emphasisNote:
      'Keeping the elbows high biases the rear shoulders and middle traps. Finishing with the hands turned up and back makes the rotator cuff muscles that turn the arm outward work harder. The lower traps help keep the shoulder blades down.',
    movementPattern: 'shoulder_horizontal_abduction',
    joints: ['Shoulder', 'Elbow', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder'],
    commonMistakes: [
      'Leaning back and using body weight to pull.',
      'Letting the elbows drop so it becomes a row to the chest.',
      'Shrugging the shoulders toward the ears.',
      'Using a weight too heavy to hold the finish.',
    ],
    goodFormFeels:
      'The backs of the shoulders and the area between the shoulder blades work hard, the finish looks like a double biceps pose, and your neck stays relaxed.',
    stopRules: [
      'Stop the set when the elbows drop or you lean back, or your technique changes in any other way.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Choose a light to moderate weight. A smooth, controlled finish matters more than a heavy pull.',
      'This counts as shoulder work for the week alongside spiking and swimming, even though it protects the shoulder.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Band face pull',
      reason: 'A light band anchored at face height is simple to control and easy to do at home.',
    },
    equipmentSubstitution: {
      exerciseId: 'reverse-machine-fly',
      name: 'Reverse Machine Fly',
      reason: 'Trains the rear shoulders and upper back when no cable is free.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'cable-external-rotation',
        name: 'Cable External Rotation',
        reason: 'Works the outward rotators more directly with a lighter load.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Stand tall with a small stagger, arms straight toward a pulley at face height.',
          ...STAGGER,
          armNear: [98, 95],
          props: [
            { type: 'line', x1: 192, y1: 12, x2: 192, y2: 172 },
            { type: 'cable', from: 'hands', to: [192, 30] },
            { type: 'handle', at: 'hands' },
          ],
        },
        {
          label: 'Pull',
          caption: 'Pull the rope to the face with the elbows high, hands finishing beside the ears.',
          ...STAGGER,
          armNear: [-92, 150],
          props: [
            { type: 'line', x1: 192, y1: 12, x2: 192, y2: 172 },
            { type: 'cable', from: 'hands', to: [192, 30] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [150, 64], to: [116, 64] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Let the rope return slowly until the arms are straight.',
          ...STAGGER,
          armNear: [98, 95],
          props: [
            { type: 'line', x1: 192, y1: 12, x2: 192, y2: 172 },
            { type: 'cable', from: 'hands', to: [192, 30] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [116, 64], to: [150, 64] },
          ],
        },
      ],
    },
  },
  {
    id: 'lateral-raise',
    name: 'Lateral Raise',
    aliases: ['Dumbbell lateral raise', 'Side raise'],
    kind: 'strength',
    purpose:
      'Builds the side of the shoulder, which helps you lift and hold the arm up for hitting and blocking.',
    equipment: ['A pair of light dumbbells'],
    setup: [
      'Stand tall with your feet hip width apart and a dumbbell in each hand.',
      'Hold the dumbbells at your sides with palms facing in and a soft bend in the elbows.',
      'Angle your arms slightly forward so they will rise a little in front of your body.',
      'Set your shoulders down away from your ears.',
    ],
    steps: [
      'Raise your arms out to the sides, slightly in front of your body.',
      'Lead with your elbows and keep your hands no higher than your elbows.',
      'Stop at about shoulder height.',
      'Pause briefly without shrugging.',
      'Lower slowly until the dumbbells are just beside your thighs.',
    ],
    breathing: 'Breathe out as you raise. Breathe in as you lower.',
    tempo: '2 0 1 1 means two seconds down, no pause at the bottom, one second up, and a one second hold near shoulder height.',
    rangeOfMotion:
      'Raise from your sides to about shoulder height. Going higher mostly brings in the upper traps and can pinch the shoulder.',
    muscles: {
      primary: ['delt_lateral'],
      secondary: ['rotator_cuff', 'traps_upper'],
    },
    emphasisNote:
      'Raising the arms slightly in front of the body, in line with the shoulder blades, biases the side of the shoulder and tends to feel smoother on the joint. The supraspinatus helps start the lift and the upper traps help near the top. Shrugging shifts more work to the traps.',
    movementPattern: 'shoulder_abduction',
    joints: ['Shoulder', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder'],
    commonMistakes: [
      'Swinging the dumbbells up with the hips or knees.',
      'Shrugging the shoulders toward the ears.',
      'Raising the arms well above shoulder height.',
      'Using dumbbells so heavy that the reps turn into jerks.',
    ],
    goodFormFeels:
      'A growing burn on the sides of the shoulders, a relaxed neck, and a smooth path with no swing.',
    stopRules: [
      'Stop the set when you start swinging or shrugging, or your technique changes in any other way.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Light weights work well here. Choose a weight you can lift smoothly for every rep.',
      'Your shoulders also work in spiking and swimming this week. Stop the set if you feel a pinch at the top of the shoulder.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Seated lateral raise',
      reason: 'Sitting on a bench removes body swing, so strict reps are easier.',
    },
    equipmentSubstitution: {
      exerciseId: 'single-arm-cable-lateral-raise',
      name: 'Single Arm Cable Lateral Raise',
      reason: 'Use a cable when the dumbbells are busy. The cable keeps tension on at the bottom of the lift.',
    },
    otherSubstitutions: [
      { exerciseId: null, name: 'Machine lateral raise', reason: 'A guided path, if your gym has one.' },
    ],
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Front view. Stand tall with the dumbbells at your sides and the elbows softly bent.',
          ...FRONT,
          armNear: [22, 12],
          armFar: [-22, -12],
          props: [
            { type: 'dumbbell', at: 'nearHand' },
            { type: 'dumbbell', at: 'farHand' },
          ],
        },
        {
          label: 'Top',
          caption: 'Front view. Raise the arms out to the sides to about shoulder height, elbows leading.',
          ...FRONT,
          armNear: [84, 88],
          armFar: [-84, -88],
          props: [
            { type: 'dumbbell', at: 'nearHand' },
            { type: 'dumbbell', at: 'farHand' },
            { type: 'arrow', from: [172, 96], to: [172, 62] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Front view. Lower slowly until the dumbbells are just beside the thighs.',
          ...FRONT,
          armNear: [22, 12],
          armFar: [-22, -12],
          props: [
            { type: 'dumbbell', at: 'nearHand' },
            { type: 'dumbbell', at: 'farHand' },
            { type: 'arrow', from: [172, 62], to: [172, 96] },
          ],
        },
      ],
    },
  },
  {
    id: 'single-arm-cable-lateral-raise',
    name: 'Single Arm Cable Lateral Raise',
    aliases: ['One arm cable lateral raise'],
    kind: 'strength',
    purpose:
      'Trains the side of each shoulder on its own, with cable tension that stays on even when your arm is low.',
    equipment: ['Low cable pulley', 'Single D handle'],
    setup: [
      'Set the pulley at the lowest position and attach a single handle.',
      'Stand side on to the machine and hold the handle in the hand farther from it, so the cable runs in front of your body.',
      'Hold the machine with your free hand and stand tall.',
      'Start with the working hand in front of your hip and a soft bend in the elbow.',
    ],
    steps: [
      'Raise the arm out to the side, slightly in front of your body.',
      'Lead with the elbow and keep the hand no higher than the elbow.',
      'Stop at about shoulder height and pause briefly.',
      'Lower slowly back to the front of your hip.',
      'Finish all reps on one side, then switch.',
    ],
    breathing: 'Breathe out as you raise. Breathe in as you lower.',
    tempo: '2 0 1 1 means two seconds down, no pause at the bottom, one second up, and a one second hold near shoulder height.',
    rangeOfMotion: 'Raise from in front of your hip to about shoulder height. Keep your trunk upright the whole way.',
    muscles: {
      primary: ['delt_lateral'],
      secondary: ['rotator_cuff', 'traps_upper'],
    },
    emphasisNote:
      'The cable pulls across your body, so the side of the shoulder works from the very bottom of the lift, where dumbbells feel light. The supraspinatus and upper traps still help.',
    movementPattern: 'shoulder_abduction',
    joints: ['Shoulder', 'Shoulder blade'],
    laterality: 'unilateral',
    logSides: true,
    fatigueOverlap: ['shoulder'],
    commonMistakes: [
      'Leaning away from the machine to swing the handle up.',
      'Shrugging the working shoulder.',
      'Raising the arm above shoulder height.',
      'Rushing the lowering half of the rep.',
    ],
    goodFormFeels: 'Steady tension on the side of the shoulder the whole way, an upright trunk, and a relaxed neck.',
    stopRules: [
      'Stop the set when you lean away or shrug, or your technique changes in any other way.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Start with your weaker side, then match the reps on the other side.',
      'Your shoulders also work in spiking and swimming this week, so keep the weight light and the reps smooth.',
    ],
    easierSubstitution: {
      exerciseId: 'lateral-raise',
      name: 'Lateral Raise',
      reason: 'Light dumbbells need no setup and are simpler to learn.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Band lateral raise',
      reason: 'Stand on a light band and raise one arm at a time when there is no cable.',
    },
    otherSubstitutions: [
      {
        exerciseId: null,
        name: 'Leaning one arm dumbbell lateral raise',
        reason: 'Hold a post and lean away slightly to keep more tension at the bottom.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Front view. Stand side on to a low pulley, working hand in front of the hip.',
          ...FRONT,
          armNear: [6, -14],
          armFar: [-45, -75],
          props: [
            { type: 'line', x1: 53, y1: 20, x2: 53, y2: 172 },
            { type: 'cable', from: 'nearHand', to: [53, 164] },
            { type: 'handle', at: 'nearHand' },
          ],
        },
        {
          label: 'Top',
          caption: 'Front view. Raise the arm out to the side to about shoulder height, trunk upright.',
          ...FRONT,
          armNear: [82, 86],
          armFar: [-45, -75],
          props: [
            { type: 'line', x1: 53, y1: 20, x2: 53, y2: 172 },
            { type: 'cable', from: 'nearHand', to: [53, 164] },
            { type: 'handle', at: 'nearHand' },
            { type: 'arrow', from: [172, 96], to: [172, 62] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Front view. Lower slowly back to the front of the hip.',
          ...FRONT,
          armNear: [6, -14],
          armFar: [-45, -75],
          props: [
            { type: 'line', x1: 53, y1: 20, x2: 53, y2: 172 },
            { type: 'cable', from: 'nearHand', to: [53, 164] },
            { type: 'handle', at: 'nearHand' },
            { type: 'arrow', from: [150, 62], to: [150, 96] },
          ],
        },
      ],
    },
  },
  {
    id: 'cable-external-rotation',
    name: 'Cable External Rotation',
    aliases: ['Standing cable external rotation'],
    kind: 'strength',
    purpose:
      'Strengthens the small muscles at the back of the shoulder that turn the arm outward and help slow the arm down after every spike and serve. This is shoulder care, so the load stays light.',
    equipment: ['Cable pulley', 'Single D handle', 'Small rolled towel'],
    setup: [
      'Set the pulley at elbow height with a single handle.',
      'Stand side on to the machine and hold the handle in the hand farther from it.',
      'Place a small rolled towel between that elbow and your side.',
      'Bend the elbow to 90 degrees with your forearm across your belly and your wrist straight.',
      'Stand tall with your shoulder blades gently set back and down.',
    ],
    steps: [
      'Keeping the elbow on the towel, rotate your forearm outward, away from your belly.',
      'Move only at the shoulder. Your forearm swings like a door on a hinge.',
      'Rotate as far as you can without the elbow leaving the towel or your trunk turning.',
      'Pause for a moment at the end.',
      'Return slowly to your belly.',
      'Finish all reps on one side, then switch.',
    ],
    breathing: 'Breathe normally and steadily. Do not hold your breath.',
    tempo: '2 0 2 1 means two seconds back in, no pause at the belly, two seconds out, and a one second hold at the end.',
    rangeOfMotion:
      'Rotate from your belly outward as far as you control, usually until your forearm points out at an angle to the side. The elbow stays pinned on the towel the whole time.',
    muscles: {
      primary: ['rotator_cuff'],
      secondary: ['delt_posterior', 'traps_middle', 'traps_lower'],
    },
    emphasisNote:
      'With the elbow at your side, this biases the infraspinatus and teres minor, the rotator cuff muscles that turn the arm outward. The rear shoulder and the muscles that steady the shoulder blade help. Heavier loads let bigger muscles take over, so keep it light.',
    movementPattern: 'shoulder_external_rotation',
    joints: ['Shoulder'],
    laterality: 'unilateral',
    logSides: true,
    fatigueOverlap: ['shoulder'],
    commonMistakes: [
      'Letting the elbow drift away from the towel.',
      'Turning the trunk to swing the handle out.',
      'Bending the wrist instead of turning the forearm.',
      'Using a weight so heavy that the movement becomes jerky.',
    ],
    goodFormFeels:
      'A mild, deep effort at the back of the shoulder, the towel stays in place, and the movement is smooth in both directions.',
    stopRules: [
      'Stop the set when the elbow leaves the towel or the trunk turns, or your technique changes in any other way.',
      EFFORT_RULE.never,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Keep the load light. This is shoulder care for a hitter, and smooth, controlled reps matter more than weight.',
      'Your shoulders also work in spiking and swimming this week. If the shoulder already feels tired, do fewer sets rather than adding weight.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Band external rotation',
      reason: 'A light band anchored at elbow height is simple to set up at home.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Side lying dumbbell external rotation',
      reason: 'Lie on your side with a very light dumbbell and the towel under the top elbow.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'face-pull',
        name: 'Face Pull',
        reason: 'Combines outward rotation with upper back work.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'never',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Front view. Elbow bent to 90 degrees on a towel at your side, hand at the belly.',
          ...FRONT,
          armNear: [28, -88],
          armFar: [-16, -8],
          props: [
            { type: 'line', x1: 24, y1: 30, x2: 24, y2: 172 },
            { type: 'cable', from: 'nearHand', to: [24, 70] },
            { type: 'handle', at: 'nearHand' },
          ],
        },
        {
          label: 'Out',
          caption: 'Front view. Turn the forearm outward like a door on a hinge, elbow still on the towel.',
          ...FRONT,
          armNear: [28, 92],
          armFar: [-16, -8],
          props: [
            { type: 'line', x1: 24, y1: 30, x2: 24, y2: 172 },
            { type: 'cable', from: 'nearHand', to: [24, 70] },
            { type: 'handle', at: 'nearHand' },
            { type: 'arrow', from: [118, 94], to: [146, 94] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Front view. Return slowly to the belly with the elbow pinned.',
          ...FRONT,
          armNear: [28, -88],
          armFar: [-16, -8],
          props: [
            { type: 'line', x1: 24, y1: 30, x2: 24, y2: 172 },
            { type: 'cable', from: 'nearHand', to: [24, 70] },
            { type: 'handle', at: 'nearHand' },
            { type: 'arrow', from: [146, 94], to: [118, 94] },
          ],
        },
      ],
    },
  },

  // ---------- Arms ----------
  {
    id: 'hammer-curl',
    name: 'Hammer Curl',
    aliases: ['Dumbbell hammer curl', 'Neutral grip curl'],
    kind: 'strength',
    purpose:
      'Builds the brachialis, brachioradialis, and biceps for elbow and forearm strength that supports pulling, gripping, and a steady platform when passing.',
    equipment: ['A pair of dumbbells'],
    setup: [
      'Stand tall with a dumbbell in each hand at your sides.',
      'Turn your palms to face your thighs, as if holding two hammers.',
      'Keep your elbows close to your sides and your shoulders relaxed.',
    ],
    steps: [
      'Curl both dumbbells up by bending at the elbows, palms still facing in.',
      'Keep your upper arms close to your sides. A little forward drift at the top is fine.',
      'Stop when your forearms are close to vertical and squeeze briefly.',
      'Lower slowly until your arms are straight again.',
    ],
    breathing: 'Breathe out as you curl. Breathe in as you lower.',
    tempo: '2 0 1 1 means two seconds down, no pause at the bottom, one second up, and a one second squeeze at the top.',
    rangeOfMotion:
      'Go from straight arms at your sides to the dumbbells near your shoulders, without the elbows swinging forward.',
    muscles: {
      primary: ['brachialis', 'brachioradialis'],
      secondary: ['biceps'],
    },
    emphasisNote:
      'The palms in grip biases the brachialis and brachioradialis. The biceps still helps bend the elbow, just a little less than in a palms up curl.',
    movementPattern: 'elbow_flexion',
    joints: ['Elbow'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['elbow', 'wrist_grip'],
    commonMistakes: [
      'Swinging the trunk to start each rep.',
      'Letting the elbows travel forward so the shoulders do the work.',
      'Dropping the dumbbells quickly on the way down.',
      'Turning the palms up during the curl.',
    ],
    goodFormFeels:
      'Work along the top of the forearm and the outside of the upper arm, with elbows that stay by your sides.',
    stopRules: [
      'Stop the set when you start swinging or the elbows drift forward, or your technique changes in any other way.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'If your elbow already feels sore from hitting or blocking, lower the weight and keep the reps smooth.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Seated hammer curl',
      reason: 'Sitting against a bench back removes body swing.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Cable rope hammer curl',
      reason: 'Use a rope on a low pulley when the dumbbells are busy.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'machine-preacher-curl',
        name: 'Machine Preacher Curl',
        reason: 'Shifts the bias toward the biceps.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Stand tall, dumbbells at the sides, palms facing the thighs.',
          ...STAND,
          armNear: [14, 18],
          props: [{ type: 'dumbbell', at: 'hands' }],
        },
        {
          label: 'Top',
          caption: 'Curl up with the palms still facing in until the forearms are close to vertical.',
          ...STAND,
          armNear: [16, 155],
          props: [{ type: 'dumbbell', at: 'hands' }, { type: 'arrow', from: [140, 96], to: [140, 60] }],
        },
        {
          label: 'Finish',
          caption: 'Lower slowly until the arms are straight again.',
          ...STAND,
          armNear: [14, 18],
          props: [{ type: 'dumbbell', at: 'hands' }, { type: 'arrow', from: [140, 60], to: [140, 96] }],
        },
      ],
    },
  },
  {
    id: 'machine-preacher-curl',
    name: 'Machine Preacher Curl',
    aliases: ['Preacher curl machine'],
    kind: 'strength',
    purpose:
      'Trains the biceps and brachialis with the upper arms supported, so the body cannot swing and the elbows do the work.',
    equipment: ['Preacher curl machine'],
    setup: [
      'Set the seat so your armpits sit snugly at the top edge of the pad.',
      'Rest the backs of your upper arms flat on the pad.',
      'Line up your elbows with the machine pivot, if it has one.',
      'Grip the handles with palms facing up.',
    ],
    steps: [
      'Curl the handles up until your forearms are close to vertical.',
      'Squeeze briefly at the top without lifting your elbows off the pad.',
      'Lower slowly until your arms are nearly straight.',
      'Stop just short of a full lockout and start the next rep.',
    ],
    breathing: 'Breathe out as you curl. Breathe in as you lower.',
    tempo: '3 0 1 1 means three seconds down, no pause at the bottom, one second up, and a one second squeeze at the top.',
    rangeOfMotion:
      'Go from nearly straight arms to forearms close to vertical. Control the bottom, where the elbow is most exposed.',
    muscles: {
      primary: ['biceps', 'brachialis'],
      secondary: ['brachioradialis'],
    },
    emphasisNote:
      'With the upper arms in front of your body, the preacher position tends to bias the short head of the biceps and the brachialis, especially near the bottom. The long head still works in every rep. Grip and pad angle shift emphasis a little, but no head switches off.',
    movementPattern: 'elbow_flexion',
    joints: ['Elbow'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['elbow'],
    commonMistakes: [
      'Lifting the elbows off the pad to finish the rep.',
      'Dropping into the bottom and bouncing out of it.',
      'Setting the seat too low so the shoulders shrug up.',
      'Curling the wrists in to help the lift.',
    ],
    goodFormFeels:
      'A strong squeeze in the front of the upper arm, upper arms quiet on the pad, and a smooth, slow lowering.',
    stopRules: [
      'Stop the set when the elbows lift off the pad or the range shrinks, or your technique changes in any other way.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Take the bottom of each rep slowly, and never relax into a locked elbow with the weight on.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Standing cable curl',
      reason: 'A light cable curl is simple to control and gentler at the bottom.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Dumbbell preacher curl',
      reason: 'Use a preacher bench, or the back of an incline bench, with one light dumbbell at a time.',
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
          caption: 'Upper arms flat on the pad, arms nearly straight, palms up on the handles.',
          ...PREACHER,
          armNear: [50, 65],
          props: [...PREACHER_PROPS, { type: 'handle', at: 'hands' }],
        },
        {
          label: 'Top',
          caption: 'Curl until the forearms are close to vertical, elbows still on the pad.',
          ...PREACHER,
          armNear: [50, 170],
          props: [...PREACHER_PROPS, { type: 'handle', at: 'hands' }, { type: 'arrow', from: [142, 112], to: [142, 80] }],
        },
        {
          label: 'Finish',
          caption: 'Lower slowly to nearly straight arms without locking out.',
          ...PREACHER,
          armNear: [50, 65],
          props: [...PREACHER_PROPS, { type: 'handle', at: 'hands' }, { type: 'arrow', from: [142, 80], to: [142, 112] }],
        },
      ],
    },
  },
  {
    id: 'triceps-pushdown',
    name: 'Triceps Pushdown',
    aliases: ['Cable pushdown', 'Triceps pressdown'],
    kind: 'strength',
    purpose:
      'Builds the triceps, which straighten the elbow when you press, block, and swing the arm through a spike.',
    equipment: ['High cable pulley', 'Straight bar or rope attachment'],
    setup: [
      'Set the pulley at the top and attach a bar or rope.',
      'Stand close to the machine with feet hip width apart and a slight forward lean from the hips.',
      'Grip the attachment and bring your elbows to your sides.',
      'Start with your forearms about level with the floor.',
    ],
    steps: [
      'Push the attachment down by straightening your elbows.',
      'Keep your upper arms still at your sides.',
      'Finish with straight arms and the attachment near your thighs. With a rope, spread the ends slightly.',
      'Pause briefly and squeeze the backs of your arms.',
      'Let the attachment rise slowly until your forearms are level with the floor again.',
    ],
    breathing: 'Breathe out as you push down. Breathe in as the attachment rises.',
    tempo: '2 0 1 1 means two seconds up, no pause at the top, one second down, and a one second squeeze with straight arms.',
    rangeOfMotion:
      'Go from forearms about level with the floor to straight arms. Letting the hands rise a little higher is fine if the elbows stay still.',
    muscles: {
      primary: ['triceps'],
      secondary: [],
    },
    emphasisNote:
      'With the arms at your sides, the lateral and medial heads of the triceps tend to do a bit more than the long head. All three heads straighten the elbow in every rep.',
    movementPattern: 'elbow_extension',
    joints: ['Elbow'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['elbow'],
    commonMistakes: [
      'Letting the elbows drift forward and back so the shoulders help.',
      'Leaning over the attachment and pushing with body weight.',
      'Letting the attachment fly up fast after each rep.',
      'Flaring the elbows out wide.',
    ],
    goodFormFeels:
      'The work stays in the backs of the upper arms, the elbows feel pinned to your sides, and the wrists stay straight.',
    stopRules: [
      'Stop the set when the elbows start moving or you lean over the attachment, or your technique changes in any other way.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'If the elbow aches after hitting practice, lower the weight or use the rope, which lets the wrists turn more freely.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Band triceps pushdown',
      reason: 'A light band over a door anchor is easy to control at home.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Dumbbell kickback',
      reason: 'No cable needed. Brace one hand on a bench and keep the upper arm still.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'rope-overhead-triceps-extension',
        name: 'Rope Overhead Triceps Extension',
        reason: 'Trains the triceps with more stretch on the long head.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Elbows at the sides, slight forward lean, forearms about level with the floor.',
          ...PUSHDOWN,
          armNear: [10, 105],
          props: [{ type: 'cable', from: 'hands', to: [122, 4] }, { type: 'handle', at: 'hands' }],
        },
        {
          label: 'Bottom',
          caption: 'Push down to straight arms while the upper arms stay still.',
          ...PUSHDOWN,
          armNear: [10, 8],
          props: [
            { type: 'cable', from: 'hands', to: [122, 4] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [152, 62], to: [152, 96] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Let the attachment rise slowly until the forearms are level again.',
          ...PUSHDOWN,
          armNear: [10, 105],
          props: [
            { type: 'cable', from: 'hands', to: [122, 4] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [152, 96], to: [152, 62] },
          ],
        },
      ],
    },
  },
  {
    id: 'rope-overhead-triceps-extension',
    name: 'Rope Overhead Triceps Extension',
    aliases: ['Overhead cable triceps extension'],
    kind: 'strength',
    purpose:
      'Trains the triceps with the arms overhead, which puts the long head on a stretch. It pairs well with pushdowns for full triceps development.',
    equipment: ['Cable pulley', 'Rope attachment'],
    setup: [
      'Set the pulley at about head height and attach a rope.',
      'Hold the rope ends and turn so you face away from the machine.',
      'Step forward into a split stance with the rope behind your head and your elbows pointing forward.',
      'Lean your trunk forward slightly and brace so your lower back does not arch.',
    ],
    steps: [
      'Start with your elbows bent and your hands behind your head.',
      'Straighten your elbows to push the rope forward and up.',
      'Keep your upper arms close to your head and still.',
      'Finish with straight arms and squeeze briefly.',
      'Bend your elbows slowly to let the rope return behind your head.',
    ],
    breathing: 'Breathe out as you straighten your arms. Breathe in as the rope returns.',
    tempo: '2 1 1 0 means two seconds to bend the elbows, a one second pause in the stretch, one second to straighten, no rest at the finish.',
    rangeOfMotion:
      'Go from a deep elbow bend with your hands behind your head to straight arms. Stop the stretch where your shoulder still feels comfortable.',
    muscles: {
      primary: ['triceps'],
      secondary: [],
    },
    emphasisNote:
      'The long head of the triceps crosses the shoulder joint, so raising your arms overhead lengthens it and gives it a larger share of the work, especially in the stretch. The lateral and medial heads still straighten the elbow in every rep.',
    movementPattern: 'elbow_extension',
    joints: ['Elbow', 'Shoulder'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['elbow', 'shoulder'],
    commonMistakes: [
      'Letting the elbows flare out wide.',
      'Arching the lower back instead of bracing.',
      'Moving the upper arms so the shoulders do the work.',
      'Rushing through the stretch at the bottom.',
    ],
    goodFormFeels:
      'A strong stretch along the back of the upper arm at the bottom, then a firm squeeze at straight arms, with your ribs down and trunk steady.',
    stopRules: [
      'Stop the set when the elbows flare or your lower back arches, or your technique changes in any other way.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Holding the arms overhead also loads the shoulder, which already works in spiking and swimming. If the shoulder pinches, stop and do pushdowns instead that day.',
    ],
    easierSubstitution: {
      exerciseId: 'triceps-pushdown',
      name: 'Triceps Pushdown',
      reason: 'Arms at your sides are easier on the shoulder and simpler to learn.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Seated overhead dumbbell triceps extension',
      reason: 'Hold one dumbbell with both hands behind your head when no cable is free.',
    },
    otherSubstitutions: [
      {
        exerciseId: null,
        name: 'Band overhead triceps extension',
        reason: 'A light band anchored low behind you works at home.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Split stance facing away from the pulley, elbows by the head, hands behind the head.',
          ...OVERHEAD,
          armNear: [140, -75],
          props: [
            { type: 'line', x1: 18, y1: 10, x2: 18, y2: 172 },
            { type: 'cable', from: 'hands', to: [18, 40] },
            { type: 'handle', at: 'hands' },
          ],
        },
        {
          label: 'Extend',
          caption: 'Straighten the elbows to push the rope forward and up. Upper arms stay still.',
          ...OVERHEAD,
          armNear: [140, 140],
          props: [
            { type: 'line', x1: 18, y1: 10, x2: 18, y2: 172 },
            { type: 'cable', from: 'hands', to: [18, 40] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [166, 52], to: [182, 26] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Bend the elbows slowly to let the rope return behind the head.',
          ...OVERHEAD,
          armNear: [140, -75],
          props: [
            { type: 'line', x1: 18, y1: 10, x2: 18, y2: 172 },
            { type: 'cable', from: 'hands', to: [18, 40] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [182, 26], to: [166, 52] },
          ],
        },
      ],
    },
  },

  // ---------- Forearms ----------
  {
    id: 'palm-down-wrist-curl',
    name: 'Seated Palm Down Wrist Curl',
    aliases: ['Reverse wrist curl', 'Barbell wrist extension'],
    kind: 'strength',
    purpose:
      'Strengthens the muscles on the back of the forearm that lift the back of the hand. It balances grip work and helps the wrists and elbows handle passing, setting, and hitting.',
    equipment: ['Two light dumbbells, or a light EZ bar', 'Flat bench'],
    setup: [
      'Sit on the end of a bench with your feet flat and your knees bent to about 90 degrees.',
      'Hold a light bar with palms facing down and hands about shoulder width apart.',
      'Rest your forearms on your thighs so your wrists sit just past your knees.',
      'Lean forward a little so your forearms stay flat on your thighs.',
    ],
    steps: [
      'Let the backs of your hands lower slowly toward the floor.',
      'Lift the backs of your hands up as high as you can, moving only at the wrists.',
      'Pause briefly at the top.',
      'Lower slowly back to the start.',
      'Keep your forearms still on your thighs the whole time.',
    ],
    breathing: 'Breathe steadily throughout. Do not hold your breath.',
    tempo: '2 0 1 1 means two seconds down, no pause at the bottom, one second up, and a one second hold at the top.',
    rangeOfMotion:
      'Move through the full comfortable range of the wrist, from hands pointing down to knuckles lifted up.',
    muscles: {
      primary: ['forearm_extensors'],
      secondary: ['forearm_flexors'],
    },
    emphasisNote:
      'Palms down with the forearms supported biases the wrist extensors on the back of the forearm. The forearm flexors still work to hold the bar in your fingers.',
    movementPattern: 'wrist_extension',
    joints: ['Wrist'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['wrist_grip', 'elbow'],
    commonMistakes: [
      'Lifting the forearms off the thighs to move the bar.',
      'Using a bar so heavy that the range becomes tiny.',
      'Bouncing at the bottom.',
    ],
    goodFormFeels:
      'A burn on the top of the forearm near the elbow, forearms still on the thighs, and a smooth hinge at the wrist.',
    stopRules: [
      'Stop the set when the forearms lift off the thighs or the range shrinks, or your technique changes in any other way.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'This lift needs very little weight. An empty EZ bar is often enough to start.',
      'These muscles attach at the outside of the elbow, so they also load the elbow. Keep the reps smooth and light.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Dumbbell palm down wrist curl',
      reason: 'One light dumbbell at a time lets each wrist move through its own range.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Band wrist extension',
      reason: 'Stand on a light band and lift the back of the hand when no bar is free.',
    },
    otherSubstitutions: [
      { exerciseId: null, name: 'Wrist roller', reason: 'Rolling a light weight up with palms down trains the same muscles.' },
    ],
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Forearms on the thighs, palms down, hands relaxed toward the floor.',
          ...WRIST,
          armNear: [0, 90],
          props: [WRIST_SEAT, { type: 'barbell', at: [125, 128] }],
        },
        {
          label: 'Lift',
          caption: 'Lift the backs of the hands up, moving only at the wrists.',
          ...WRIST,
          armNear: [0, 90],
          props: [WRIST_SEAT, { type: 'barbell', at: [124, 111] }, { type: 'arrow', from: [144, 128], to: [144, 110] }],
        },
        {
          label: 'Finish',
          caption: 'Lower slowly back down with the forearms still on the thighs.',
          ...WRIST,
          armNear: [0, 90],
          props: [WRIST_SEAT, { type: 'barbell', at: [125, 128] }, { type: 'arrow', from: [144, 110], to: [144, 128] }],
        },
      ],
    },
  },
  {
    id: 'palm-up-wrist-curl',
    name: 'Seated Palm Up Wrist Curl',
    aliases: ['Barbell wrist curl', 'Wrist flexion curl'],
    kind: 'strength',
    purpose:
      'Strengthens the forearm flexors that curl the wrist and close the hand. They support grip, setting, and the wrist snap at the end of a spike.',
    equipment: ['Two light dumbbells, or a light EZ bar', 'Flat bench'],
    setup: [
      'Sit on the end of a bench with your feet flat and your knees bent to about 90 degrees.',
      'Hold a light bar with palms facing up and hands about shoulder width apart.',
      'Rest your forearms on your thighs so your wrists sit just past your knees.',
      'Lean forward a little so your forearms stay flat on your thighs.',
    ],
    steps: [
      'Let the bar lower slowly, bending your wrists back toward the floor.',
      'Curl the bar up by bending your wrists toward you as far as you can.',
      'Pause briefly at the top.',
      'Lower slowly back to the start.',
      'Keep your forearms still on your thighs the whole time.',
    ],
    breathing: 'Breathe steadily throughout. Do not hold your breath.',
    tempo: '2 0 1 1 means two seconds down, no pause at the bottom, one second up, and a one second hold at the top.',
    rangeOfMotion:
      'Move from the wrists bent back toward the floor to the wrists curled up, within a comfortable range.',
    muscles: {
      primary: ['forearm_flexors'],
      secondary: [],
    },
    emphasisNote:
      'Palms up with the forearms supported biases the wrist and finger flexors on the palm side of the forearm. Letting the bar roll slightly toward the fingers at the bottom adds more finger flexor work.',
    movementPattern: 'wrist_flexion',
    joints: ['Wrist'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['wrist_grip', 'elbow'],
    commonMistakes: [
      'Lifting the forearms off the thighs.',
      'Using a bar so heavy that the reps get short and jerky.',
      'Bouncing out of the bottom.',
    ],
    goodFormFeels: 'A burn on the inner forearm, steady forearms, and smooth movement at the wrist.',
    stopRules: [
      'Stop the set when the forearms lift off the thighs or the range shrinks, or your technique changes in any other way.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Start with an empty bar or a very light weight.',
      'These muscles attach at the inside of the elbow, which hitters already load heavily. Keep the reps smooth and light.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Dumbbell palm up wrist curl',
      reason: 'One light dumbbell at a time lets each wrist move through its own range.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Cable wrist curl',
      reason: 'Sit by a low pulley with a short straight bar when no barbell is free.',
    },
    otherSubstitutions: [
      { exerciseId: null, name: 'Farmer carry', reason: 'Walking while holding dumbbells trains grip strength in a more whole body way.' },
    ],
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Forearms on the thighs, palms up, wrists bent back so the bar sits low.',
          ...WRIST,
          armNear: [0, 90],
          props: [WRIST_SEAT, { type: 'barbell', at: [125, 128] }],
        },
        {
          label: 'Curl',
          caption: 'Curl the bar up by bending the wrists toward you.',
          ...WRIST,
          armNear: [0, 90],
          props: [WRIST_SEAT, { type: 'barbell', at: [124, 111] }, { type: 'arrow', from: [144, 128], to: [144, 110] }],
        },
        {
          label: 'Finish',
          caption: 'Lower slowly with the forearms still on the thighs.',
          ...WRIST,
          armNear: [0, 90],
          props: [WRIST_SEAT, { type: 'barbell', at: [125, 128] }, { type: 'arrow', from: [144, 110], to: [144, 128] }],
        },
      ],
    },
  },
];
