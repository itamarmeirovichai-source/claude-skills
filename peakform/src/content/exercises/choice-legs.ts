import { EFFORT_RULE, PAIN_RULE } from './effort';
import type { ExerciseContent, Pose, PoseProp } from '../types';

// Leg and core alternatives for the exercise questionnaire. Order matches LEGS_CHOICE_IDS in ids.ts.
// Machines, cables, the Smith machine, and dumbbells only, so hard sets are safe without a spotter.
// He is a jumping athlete, so the knees and lower back get extra care: deep squats with a pause
// instead of a bounce, a flat back in every hinge, and ribs down at the top of the hip thrust.
// Poses are side views unless the caption says front view.

type Base = Pick<Pose, 'trunk' | 'hip' | 'legNear' | 'legFar' | 'footX' | 'head'>;

// ---------- Shared pose pieces ----------

/** Smith squat: the bar rides on a vertical rail, feet a little in front of it. */
const SMITH_SQUAT_TOP: Base = { trunk: 178, legNear: [0, 0], legFar: [2, -2], footX: 100 };
const SMITH_SQUAT_BOTTOM: Base = { trunk: 150, legNear: [98, -30], legFar: [96, -29], footX: 100 };
const SMITH_SQUAT_PROPS: PoseProp[] = [
  { type: 'line', x1: 97, y1: 8, x2: 97, y2: 172 },
  { type: 'line', x1: 86, y1: 113, x2: 108, y2: 113 },
];

/** Standing hinge, feet hip width, soft knees. */
const HINGE_TOP: Base = { trunk: 180, legNear: [3, -3] };
const HINGE_BOTTOM: Base = { trunk: 114, legNear: [32, -2] };

/** Smith Romanian deadlift: rail through the bar, safety stop just below the lowest point. */
const SMITH_RDL_PROPS: PoseProp[] = [
  { type: 'line', x1: 99.5, y1: 8, x2: 99.5, y2: 172 },
  { type: 'line', x1: 89, y1: 145, x2: 110, y2: 145 },
];

/** Hip thrust on the floor, upper back on the bench edge. Matches the barbell hip thrust. */
const THRUST_LOW: Base = { trunk: -120, head: -150, hip: [107.3, 151.6], legNear: [117.3, 7.7, 90] };
const THRUST_HIGH: Base = { trunk: -90, head: -125, hip: [108, 132], legNear: [90, 0, 90] };
const THRUST_PROPS: PoseProp[] = [
  { type: 'line', x1: 107.6, y1: 14, x2: 107.6, y2: 172 },
  { type: 'bench', x: 18, y: 140.5, w: 53, h: 8 },
];

/** Front view: seated in a hip abduction or adduction machine, hands on the seat handles. */
const SEATED_FRONT = { trunk: 180, hip: [100, 80] } satisfies Partial<Base>;
const SEATED_FRONT_PROPS: PoseProp[] = [
  { type: 'box', x: 84, y: 30, w: 32, h: 52 },
  { type: 'line', x1: 100, y1: 90, x2: 100, y2: 172 },
  { type: 'line', x1: 84, y1: 171, x2: 116, y2: 171 },
  { type: 'pad', x: 76, y: 83, w: 48, h: 8 },
];

/** Reclined in a 45 degree leg press, legs almost straight, hands on the side handles. */
const LEG_PRESS = { trunk: 230, head: 215, hip: [72, 128] } satisfies Partial<Base>;
const LEG_PRESS_PROPS: PoseProp[] = [
  { type: 'bench', x: 65.6, y: 131.7, w: 58, h: 8, angle: -140 },
  { type: 'bench', x: 56, y: 138, w: 30 },
  { type: 'line', x1: 96, y1: 150, x2: 176, y2: 70 },
  { type: 'line', x1: 176, y1: 70, x2: 176, y2: 172 },
];

/** Kneeling facing a high pulley, hips a little back of the knees. */
const KNEEL: Base = { hip: [70, 126], legNear: [5, -92, -90], legFar: [3, -92, -90] } as Base;
const CRUNCH_PROPS: PoseProp[] = [{ type: 'line', x1: 176, y1: 4, x2: 176, y2: 172 }];

/** Front view: standing side on to a high pulley, feet wider than the shoulders. */
const CHOP: Base = { trunk: 180, legNear: [15, 0, 90], legFar: [-15, 0, -90], footX: 118 };
const CHOP_POST: PoseProp = { type: 'line', x1: 12, y1: 4, x2: 12, y2: 172 };

export const LEGS_CHOICES: ExerciseContent[] = [
  // ---------------------------------------------------------------- Smith Machine Squat
  {
    id: 'smith-squat',
    name: 'Smith Machine Squat',
    aliases: ['Smith squat'],
    kind: 'strength',
    purpose:
      'Builds the quads and glutes with a guided bar and safety stops, so you can squat deep and train hard alone. Depth is what matters most here: deep squats train the glutes and adductors more than shallow ones.',
    equipment: ['Smith machine', 'Weight plates'],
    setup: [
      'Set the safety stops just below the lowest point of your squat. Check the height with an empty bar first.',
      'Set the bar on the hooks at about shoulder height.',
      'Step under the bar and rest it on the muscle of your upper back, below the bony top of the spine.',
      'Place your feet slightly in front of the bar, about shoulder width apart, toes turned out a little.',
      'Grip the bar just outside your shoulders and brace your trunk.',
    ],
    steps: [
      'Stand up to lift the bar, then twist it off the hooks.',
      'Sit down between your hips, letting your knees travel forward in line with your toes.',
      'Keep your whole foot on the floor, heels down, and your chest facing forward.',
      'Lower until your thighs are below parallel, or as deep as your back stays neutral and your heels stay down.',
      'Pause for a moment at the bottom without bouncing, then drive the floor away to stand up.',
      'After the last rep, twist the bar back onto the hooks before you step out.',
    ],
    breathing:
      'Breathe in and brace before each rep. Hold the brace on the way down and through the pause. Breathe out near the top.',
    tempo: '3 1 1 0 means three seconds down, a one second pause at the bottom, one second up, and no rest at the top.',
    rangeOfMotion:
      'Go deep. Thighs below parallel is the target, as long as your back stays neutral and your heels stay down. The safety stops sit just below that point, so a missed rep lands on them.',
    muscles: {
      primary: ['quads', 'glute_max'],
      secondary: ['adductors', 'hamstrings', 'erectors', 'obliques_core'],
    },
    emphasisNote:
      'The quads and glutes do most of the work. The glutes and adductors are stretched most at the bottom, so deep reps load them more. A ten week study (Kubo and colleagues, 2019) found that full squats grew the glutes and adductors more than half squats, while the quads grew about the same. How deep you go seems to matter more than which squat you pick. None of these muscles switch off in any version.',
    movementPattern: 'squat',
    joints: ['Hip', 'Knee', 'Ankle'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['knee', 'hip', 'low_back', 'systemic'],
    commonMistakes: [
      'Setting the safety stops so low that they would not catch the bar, or so high that they cut your depth.',
      'Standing with the feet right under the bar, which pushes the knees far forward and lifts the heels.',
      'Bouncing out of the bottom instead of pausing.',
      'Knees caving inward on the way up.',
      'Cutting depth as the weight goes up.',
    ],
    goodFormFeels:
      'Pressure through the whole foot, a tight trunk, and deep work in the thighs and glutes. The bar feels settled on your upper back and the machine takes care of balance.',
    stopRules: [
      'End the set when your depth gets shallower, your heels lift, your knees cave, or your lower back starts to round at the bottom.',
      EFFORT_RULE.last,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Set the safety stops before every set. If a rep stalls, sit down under control until the bar rests on them, then slide out.',
      'Practise twisting the bar on and off the hooks with an empty bar first.',
      'You jump a lot in volleyball. The pause at the bottom, instead of a bounce, spares your knees.',
    ],
    easierSubstitution: {
      exerciseId: 'leg-press',
      name: 'Leg Press',
      reason: 'Your back rests on a pad and there is no bar on your shoulders, so deep knee bending is simpler to learn.',
    },
    equipmentSubstitution: {
      exerciseId: 'hack-squat',
      name: 'Hack Squat',
      reason: 'Use it when the Smith machine is busy. It also guides the path and has safety catches.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'bulgarian-split-squat',
        name: 'Bulgarian Split Squat',
        reason: 'Dumbbells and one leg at a time, when both machines are taken.',
      },
    ],
    loadIncrement: 'lower',
    failure: 'last',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Bar on your upper back, feet a little in front of the bar, safety stops set low.',
          ...SMITH_SQUAT_TOP,
          armNear: [-30, 160],
          props: [...SMITH_SQUAT_PROPS, { type: 'barbell', at: 'hands' }],
        },
        {
          label: 'Bottom',
          caption: 'Sit deep with your heels down and your back neutral. Pause here, no bounce.',
          ...SMITH_SQUAT_BOTTOM,
          armNear: [-72, 116],
          props: [...SMITH_SQUAT_PROPS, { type: 'barbell', at: 'hands' }, { type: 'arrow', from: [150, 55], to: [150, 95] }],
        },
        {
          label: 'Finish',
          caption: 'Drive the floor away and stand tall. The bar moves straight up the rail.',
          ...SMITH_SQUAT_TOP,
          armNear: [-30, 160],
          props: [...SMITH_SQUAT_PROPS, { type: 'barbell', at: 'hands' }, { type: 'arrow', from: [150, 95], to: [150, 55] }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Dumbbell Romanian Deadlift
  {
    id: 'dumbbell-romanian-deadlift',
    name: 'Dumbbell Romanian Deadlift',
    aliases: ['Dumbbell RDL'],
    kind: 'strength',
    purpose:
      'Trains the hamstrings and glutes in a long stretch with weights that are easy to handle and put down. Strong hamstrings support sprinting and jumping, and a flat back on every rep protects the lower back, which already works hard when you jump and land.',
    equipment: ['A pair of dumbbells'],
    setup: [
      'Pick the dumbbells up from the rack and stand tall with your feet about hip width apart.',
      'Hold the dumbbells in front of your thighs, palms facing you.',
      'Unlock your knees into a soft bend and keep that same bend for the whole set.',
      'Brace your trunk and draw your shoulders slightly back and down.',
    ],
    steps: [
      'Push your hips straight back, as if closing a car door behind you with your backside.',
      'Let the dumbbells slide down the front of your thighs, staying very close to your legs.',
      'Keep your back flat and your neck in line with your spine, eyes on the floor a couple of metres ahead.',
      'Stop when you feel a strong stretch in the back of your thighs, or just before your back starts to round.',
      'Pause for a moment in the stretch, then drive your hips forward to stand tall without leaning back.',
    ],
    breathing:
      'Breathe in and brace at the top. Hold the brace as you lower and as you start to stand. Breathe out near the top.',
    tempo: '3 1 1 0 means three seconds down, a one second pause in the stretch, one second up, and no rest at the top.',
    rangeOfMotion:
      'Lower until you feel a strong hamstring stretch while your back stays flat. For most people the dumbbells end between just below the knees and mid shin. Your back position sets the depth, not how low the dumbbells go.',
    muscles: {
      primary: ['hamstrings', 'glute_max'],
      secondary: ['adductors', 'erectors', 'forearm_flexors', 'obliques_core'],
    },
    emphasisNote:
      'The hamstrings and glutes share the load, and the adductor magnus helps extend the hip. The hamstrings work hardest near the bottom, where they are longest, which makes this a strong choice for hamstring growth. A small, fixed knee bend keeps the stretch on the hamstrings. The back muscles and your grip hold position rather than move the weight.',
    movementPattern: 'hinge',
    joints: ['Hip'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['low_back', 'hamstring'],
    commonMistakes: [
      'Rounding the lower back to reach the dumbbells lower.',
      'Bending the knees more and more until the lift turns into a squat.',
      'Letting the dumbbells drift forward, away from the legs.',
      'Leaning back or pushing the hips too far forward at the top.',
      'Looking up at a mirror, which strains the neck.',
    ],
    goodFormFeels:
      'A strong, even stretch in the back of both thighs, your weight over the middle of the foot, and a flat, braced back. Standing up feels like your hips pull you upright.',
    stopRules: [
      'End the set when your back starts to round, the dumbbells drift away from your legs, or your grip starts to slip.',
      'Stop at once for a sharp pull in the back of the thigh.',
      EFFORT_RULE.never,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Learn the hip hinge with light dumbbells before you add load.',
      'Take the dumbbells from the rack or a bench at thigh height rather than lifting them off the floor with a rounded back.',
      'Keep your lower back flat on every rep. It already works hard in jumping and landing.',
    ],
    easierSubstitution: {
      exerciseId: 'back-extension',
      name: '45 Degree Back Extension',
      reason: 'Body weight only at first, with your legs held in place, so the hip hinge is easier to learn.',
    },
    equipmentSubstitution: {
      exerciseId: 'smith-romanian-deadlift',
      name: 'Smith Machine Romanian Deadlift',
      reason: 'Use it when the heavy dumbbells are taken. The bar path is guided and it rests on the hooks between sets.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'seated-leg-curl',
        name: 'Seated Leg Curl',
        reason: 'Trains the hamstrings at a long length without loading the lower back.',
      },
    ],
    loadIncrement: 'lower',
    failure: 'never',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Stand tall with the dumbbells in front of your thighs, knees soft, trunk braced.',
          ...HINGE_TOP,
          armNear: [0, 0],
          props: [{ type: 'dumbbell', at: 'hands' }],
        },
        {
          label: 'Stretch',
          caption: 'Push the hips back with a flat back until the hamstrings are stretched. Dumbbells stay close to the legs.',
          ...HINGE_BOTTOM,
          armNear: [-15, -15],
          props: [{ type: 'dumbbell', at: 'hands' }, { type: 'arrow', from: [66, 76], to: [44, 76] }],
        },
        {
          label: 'Finish',
          caption: 'Drive the hips forward and stand tall without leaning back.',
          ...HINGE_TOP,
          armNear: [0, 0],
          props: [{ type: 'dumbbell', at: 'hands' }, { type: 'arrow', from: [60, 90], to: [80, 90] }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Smith Machine Romanian Deadlift
  {
    id: 'smith-romanian-deadlift',
    name: 'Smith Machine Romanian Deadlift',
    aliases: ['Smith RDL'],
    kind: 'strength',
    purpose:
      'Trains the hamstrings and glutes in a long stretch with a guided bar that you can load heavier than dumbbells and hook back on when you are done. The fixed path lets you focus on the hips, and a flat back on every rep protects the lower back, which already works hard when you jump and land.',
    equipment: ['Smith machine', 'Weight plates'],
    setup: [
      'Set the bar on the hooks at about mid thigh height, so you can take it while standing tall.',
      'Set the safety stops just below the lowest point of your range, around mid shin.',
      'Stand close to the bar with your feet about hip width apart and grip it overhand, just outside your thighs.',
      'Stand tall to lift the bar, twist it off the hooks, and unlock your knees into a soft bend.',
    ],
    steps: [
      'Push your hips straight back while the bar slides down the front of your thighs.',
      'Keep your back flat and your neck long, eyes on the floor a little ahead.',
      'Stop when you feel a strong stretch in the back of your thighs, or just before your back starts to round.',
      'Pause for a moment, then drive your hips forward to stand tall without leaning back.',
      'After the last rep, stand tall and twist the bar back onto the hooks.',
    ],
    breathing:
      'Breathe in and brace at the top. Hold the brace as you lower and as you start to stand. Breathe out near the top.',
    tempo: '3 1 1 0 means three seconds down, a one second pause in the stretch, one second up, and no rest at the top.',
    rangeOfMotion:
      'Lower until you feel a strong hamstring stretch while your back stays flat, usually with the bar between just below the knees and mid shin. The bar moves straight up and down, so stand close enough that it brushes your thighs.',
    muscles: {
      primary: ['hamstrings', 'glute_max'],
      secondary: ['adductors', 'erectors', 'forearm_flexors', 'obliques_core'],
    },
    emphasisNote:
      'The hamstrings and glutes share the work, and the adductor magnus helps. Because you do not have to balance the bar, you can put your effort into pushing the hips back into a long hamstring stretch, the position that matters most for growth. A small, fixed knee bend keeps more of the stretch on the hamstrings. The back muscles hold your spine still.',
    movementPattern: 'hinge',
    joints: ['Hip'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['low_back', 'hamstring'],
    commonMistakes: [
      'Standing too far from the bar, so it pulls you forward onto your toes.',
      'Rounding the lower back to reach a lower bar position.',
      'Bending the knees more and more until the lift turns into a squat.',
      'Leaning back at the top.',
    ],
    goodFormFeels:
      'A strong stretch in the back of both thighs, the bar brushing your legs, and a flat, braced back. The machine holds the path steady, so all your effort goes into the hips.',
    stopRules: [
      'End the set when your back starts to round or your knees start to bend more to reach the depth.',
      'Stop at once for a sharp pull in the back of the thigh.',
      EFFORT_RULE.never,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Set the safety stops before every set, so the bar can never travel below your lowest point.',
      'Practise twisting the bar on and off the hooks with an empty bar first.',
      'Keep your lower back flat on every rep. It already works hard in jumping and landing.',
    ],
    easierSubstitution: {
      exerciseId: 'back-extension',
      name: '45 Degree Back Extension',
      reason: 'Body weight only at first, with your legs held in place, so the hip hinge is easier to learn.',
    },
    equipmentSubstitution: {
      exerciseId: 'dumbbell-romanian-deadlift',
      name: 'Dumbbell Romanian Deadlift',
      reason: 'The same hinge with dumbbells when the Smith machine is busy.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'seated-leg-curl',
        name: 'Seated Leg Curl',
        reason: 'Trains the hamstrings at a long length without loading the lower back.',
      },
    ],
    loadIncrement: 'lower',
    failure: 'never',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Stand tall close to the bar, knees soft. The safety stops sit just below your lowest point.',
          ...HINGE_TOP,
          armNear: [5, 4],
          props: [...SMITH_RDL_PROPS, { type: 'barbell', at: 'hands' }],
        },
        {
          label: 'Stretch',
          caption: 'Push the hips back with a flat back. The bar slides straight down close to your legs.',
          ...HINGE_BOTTOM,
          armNear: [-18, -18],
          props: [...SMITH_RDL_PROPS, { type: 'barbell', at: 'hands' }, { type: 'arrow', from: [66, 76], to: [44, 76] }],
        },
        {
          label: 'Finish',
          caption: 'Drive the hips forward and stand tall without leaning back.',
          ...HINGE_TOP,
          armNear: [5, 4],
          props: [...SMITH_RDL_PROPS, { type: 'barbell', at: 'hands' }, { type: 'arrow', from: [60, 90], to: [80, 90] }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Dumbbell Walking Lunge
  {
    id: 'walking-lunge',
    name: 'Dumbbell Walking Lunge',
    aliases: ['Walking lunge'],
    kind: 'strength',
    purpose:
      'Builds the quads and glutes one leg at a time while you move forward, which also trains the balance and control you need for take offs and landings. A long step puts the glute of the front leg in a deep stretch at the bottom.',
    equipment: ['A pair of dumbbells', 'A clear walkway of about 10 metres'],
    setup: [
      'Find a clear, flat path where you can take 10 to 20 steps without anyone in the way.',
      'Stand tall with a dumbbell in each hand and your arms hanging by your sides.',
      'Brace your trunk and look straight ahead.',
    ],
    steps: [
      'Take a long step forward and place your whole front foot on the floor.',
      'Lower your back knee under control until it is just above the floor.',
      'Keep your front heel down and your front knee in line with your middle toes, torso tall or leaning slightly forward.',
      'Push through your whole front foot to stand up and bring your back foot forward.',
      'Step straight into the next lunge with the other leg, and keep alternating.',
    ],
    breathing: 'Breathe in as you step and lower. Breathe out as you push up.',
    tempo:
      '2 1 1 0 means two seconds to lower, a one second pause just above the floor, one second to stand up, and no rest before the next step.',
    rangeOfMotion:
      'Lower until your back knee is just above the floor, with your front heel down and your trunk steady. A longer step gives the front glute more stretch, and a shorter step with more forward knee travel gives the quads more.',
    muscles: {
      primary: ['quads', 'glute_max'],
      secondary: ['adductors', 'glute_med', 'hamstrings', 'gastrocnemius', 'soleus', 'obliques_core'],
    },
    emphasisNote:
      'The front leg does most of the work. A long step and a slight forward lean from the hips stretch the glute and adductors of the front leg more at the bottom, which suits growth. A shorter step and an upright torso bias the quads. The side of the hip works on every step to keep your pelvis level.',
    movementPattern: 'lunge',
    joints: ['Hip', 'Knee', 'Ankle'],
    laterality: 'alternating',
    logSides: false,
    fatigueOverlap: ['knee', 'hip', 'systemic'],
    commonMistakes: [
      'Dropping the back knee hard onto the floor.',
      'Taking short, choppy steps so the front heel lifts.',
      'Letting the front knee cave inward.',
      'Pushing off the back foot instead of the front leg.',
      'Walking the feet in one narrow line, which makes balance hard.',
    ],
    goodFormFeels:
      'Most of the effort in the front thigh and glute, a stretch deep in the front hip at the bottom, and a steady trunk. Each step flows smoothly into the next.',
    stopRules: [
      'End the set when your balance wobbles, your back knee starts to drop hard, or your front knee caves.',
      EFFORT_RULE.never,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Clear the path first, and choose dumbbells light enough that you can set them down safely at any point.',
      'Keep your feet about hip width apart side to side for balance.',
      'Lunges can leave your legs sore at first. Start with fewer steps than you think you can do.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Dumbbell reverse lunge',
      reason: 'Stepping backward is easier to balance and gentler on the front knee, and it needs less space.',
    },
    equipmentSubstitution: {
      exerciseId: 'bulgarian-split-squat',
      name: 'Bulgarian Split Squat',
      reason: 'Trains the same front leg pattern in one spot when there is no space to walk.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'smith-squat',
        name: 'Smith Machine Squat',
        reason: 'A two leg option with a guided bar if balance is the limit today.',
      },
    ],
    loadIncrement: 'lower',
    failure: 'never',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Stand tall with a dumbbell in each hand, arms hanging by your sides.',
          trunk: 180,
          armNear: [0, 0],
          legNear: [2, -2],
          legFar: [-2, 2],
          footX: 58,
          props: [{ type: 'dumbbell', at: 'hands' }],
        },
        {
          label: 'Bottom',
          caption: 'Take a long step and lower the back knee under control until it is just above the floor.',
          trunk: 172,
          hip: [88, 125],
          armNear: [-4, -4],
          legNear: [80, -8, 90],
          legFar: [-10, -99, 20],
          props: [{ type: 'dumbbell', at: 'hands' }, { type: 'arrow', from: [165, 70], to: [165, 105] }],
        },
        {
          label: 'Finish',
          caption: 'Push through the whole front foot to stand up, and bring the back leg through into the next step.',
          trunk: 178,
          armNear: [0, 0],
          legNear: [0, 0],
          legFar: [35, -45, 80],
          footX: 124,
          props: [{ type: 'dumbbell', at: 'hands' }, { type: 'arrow', from: [150, 110], to: [175, 80] }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Smith Machine Hip Thrust
  {
    id: 'smith-hip-thrust',
    name: 'Smith Machine Hip Thrust',
    aliases: ['Smith hip thrust', 'Machine hip thrust'],
    kind: 'strength',
    purpose:
      'Builds the glutes hard at full hip extension, the position you drive through when you jump and sprint. The Smith machine guides the bar and its safety stops catch it, so you can train it alone. A hip thrust machine works the same way.',
    equipment: ['Smith machine', 'Flat bench', 'Thick bar pad', 'Weight plates'],
    setup: [
      'Place a flat bench side on behind the Smith bar, against something solid so it cannot slide.',
      'Set the safety stops so the bar rests on them just above your hips when you sit on the floor.',
      'Sit with your upper back against the bench edge, just below your shoulder blades.',
      'Put a thick pad on the bar and slide under it until it sits over the crease of your hips.',
      'Place your feet flat, about hip width apart, so your shins will be close to vertical at the top.',
    ],
    steps: [
      'Tuck your chin, brace your trunk, and push through your heels and midfoot.',
      'Drive your hips up until your body is straight from shoulders to knees.',
      'Keep your chin tucked and your ribs down at the top, so your lower back does not arch.',
      'Squeeze your glutes and pause for one second.',
      'Lower your hips under control until the bar is just above the safety stops.',
    ],
    breathing: 'Breathe in and brace before each rep. Breathe out at the top once your hips are fully up.',
    tempo:
      '2 0 1 1 means two seconds to lower the hips, no pause at the bottom, one second to drive up, and a one second squeeze at the top.',
    rangeOfMotion:
      'Move from hips just above the floor to a straight line from shoulders to knees. Stop at full hip extension. Going higher only arches the lower back, which adds stress there and no extra glute work.',
    muscles: {
      primary: ['glute_max'],
      secondary: ['hamstrings', 'adductors'],
    },
    emphasisNote:
      'The glutes are under the most tension near the top, where the hips are straight, so the pause there counts. Finishing with the chin tucked and the ribs down keeps the work in the glutes and the spine neutral. That matters for you, because repeated arching of the lower back is a known strain for young athletes who jump a lot. Feet a little further out bring in more hamstring, and feet closer in bring in more quad.',
    movementPattern: 'hip_extension',
    joints: ['Hip'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['hip', 'low_back'],
    commonMistakes: [
      'Arching the lower back at the top instead of finishing with the glutes.',
      'Letting the head fall back, which usually pulls the lower back into an arch.',
      'Placing the bar on the belly or thighs instead of the hip crease.',
      'Pushing through the toes so the heels lift.',
      'Rushing the top and skipping the pause.',
    ],
    goodFormFeels:
      'A strong squeeze in your glutes at the top, pressure through your heels, and ribs staying down. The bench works as a pivot under your shoulder blades and the bar moves straight up and down.',
    stopRules: [
      'End the set when you can no longer reach full hip extension with a one second pause, or your lower back starts to arch to finish the rep.',
      EFFORT_RULE.last,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Set the safety stops before you load the bar, so the bar can never come down onto your hips.',
      'Use a thick bar pad so the bar does not press into your hip bones.',
      'If your gym has a hip thrust machine, it works the same way and is quicker to set up.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Glute bridge',
      reason: 'Lying on the floor shortens the range and needs no bench. Start with body weight or a light plate.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Hip thrust machine',
      reason: 'The same movement with a padded belt or lever instead of a bar. Use the same chin tucked, ribs down finish.',
    },
    otherSubstitutions: [
      {
        exerciseId: null,
        name: 'Dumbbell hip thrust',
        reason: 'Rest one heavy dumbbell in the crease of your hips when the Smith machine is busy.',
      },
      {
        exerciseId: 'back-extension',
        name: '45 Degree Back Extension',
        reason: 'Another hip extension exercise for the glutes and hamstrings, with your legs held in place.',
      },
    ],
    loadIncrement: 'lower',
    failure: 'last',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Upper back on the bench edge, bar in the hip crease, hips just above the floor.',
          ...THRUST_LOW,
          armNear: [37, 116.6],
          props: [...THRUST_PROPS, { type: 'barbell', at: [107.3, 139.6] }],
        },
        {
          label: 'Top',
          caption: 'Drive the hips up until shoulders, hips, and knees line up. Chin tucked, ribs down, pause one second.',
          ...THRUST_HIGH,
          armNear: [77.8, 134.2],
          props: [...THRUST_PROPS, { type: 'barbell', at: [107.6, 120] }, { type: 'arrow', from: [132, 110], to: [132, 88] }],
        },
        {
          label: 'Finish',
          caption: 'Lower the hips under control until the bar is just above the safety stops.',
          ...THRUST_LOW,
          armNear: [37, 116.6],
          props: [...THRUST_PROPS, { type: 'barbell', at: [107.3, 139.6] }, { type: 'arrow', from: [132, 100], to: [132, 122] }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Seated Hip Abduction Machine
  {
    id: 'hip-abduction-machine',
    name: 'Seated Hip Abduction Machine',
    aliases: ['Hip abductor machine', 'Outer thigh machine'],
    kind: 'strength',
    purpose:
      'Strengthens the side of the hip, which keeps your pelvis level and your knees lined up in single leg take offs and landings. Leaning slightly forward also brings more of the glute max into the work.',
    equipment: ['Seated hip abduction machine'],
    setup: [
      'Set the start position so your knees begin close together.',
      'Sit with your hips all the way back in the seat and your feet on the foot rests.',
      'Place the pads on the outside of your knees.',
      'Lean your trunk slightly forward from the hips, keeping your back straight, and hold the handles.',
    ],
    steps: [
      'Push your knees out against the pads as far as you can control.',
      'Pause for one second with the knees wide.',
      'Let the pads bring your knees back in slowly, into the stretch on the outside of the hips.',
      'Stop just before the weight stack touches down, then start the next rep.',
    ],
    breathing: 'Breathe out as you push the knees out. Breathe in as they come back in.',
    tempo:
      '2 0 1 1 means two seconds to let the knees come back in, no pause there, one second to push them out, and a one second hold with the knees wide.',
    rangeOfMotion:
      'From knees close together, where the outside of the hip is stretched, out as wide as you can push with your hips still on the seat. Use the full range at both ends.',
    muscles: {
      primary: ['glute_med'],
      secondary: ['glute_max'],
    },
    emphasisNote:
      'The gluteus medius and minimus do most of the work, with help from the upper glute max and the tensor fasciae latae at the front of the hip. With the hips bent in a slight forward lean, more of the glute max joins in. Sitting tall shifts a larger share to the gluteus medius. Both work in every position, and the slow return into the stretch is part of the work.',
    movementPattern: 'hip_abduction',
    joints: ['Hip'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['hip'],
    commonMistakes: [
      'Letting the weight snap the knees back together.',
      'Rocking the trunk to swing the pads out.',
      'Lifting the hips off the seat.',
      'Cutting the range short at the inside, where the stretch is.',
    ],
    goodFormFeels:
      'A strong burn high on the outside of your hips and in the upper glutes, while your trunk stays still.',
    stopRules: [
      'End the set when the range gets shorter or you start rocking the trunk to move the pads.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Keep your fingers clear of the pads and levers while they move.',
      'Choose a weight you can lower back into the stretch under control. The weight stack should never slam.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Side lying hip abduction',
      reason: 'Body weight only, lying on your side and lifting the top leg. Easy to learn and control.',
    },
    equipmentSubstitution: {
      exerciseId: 'cable-hip-abduction',
      name: 'Cable Hip Abduction',
      reason: 'Trains one side at a time with a low pulley when the machine is busy.',
    },
    otherSubstitutions: [
      {
        exerciseId: null,
        name: 'Banded lateral walk',
        reason: 'Needs only a mini band above the knees. Useful in a warm up.',
      },
    ],
    loadIncrement: 'lower',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Front view. Seated with the pads on the outside of your knees, knees close together.',
          ...SEATED_FRONT,
          armNear: [25, 8],
          armFar: [-25, -8],
          legNear: [10, 0, 90],
          legFar: [-10, 0, -90],
          props: [
            ...SEATED_FRONT_PROPS,
            { type: 'pad', x: 113.3, y: 112.4, w: 6, h: 18 },
            { type: 'pad', x: 80.7, y: 112.4, w: 6, h: 18 },
            { type: 'handle', at: 'nearHand' },
            { type: 'handle', at: 'farHand' },
          ],
        },
        {
          label: 'Out',
          caption: 'Front view. Push the knees out against the pads and pause for one second.',
          ...SEATED_FRONT,
          armNear: [25, 8],
          armFar: [-25, -8],
          legNear: [32, 0, 90],
          legFar: [-32, 0, -90],
          props: [
            ...SEATED_FRONT_PROPS,
            { type: 'pad', x: 128.3, y: 106.6, w: 6, h: 18 },
            { type: 'pad', x: 65.7, y: 106.6, w: 6, h: 18 },
            { type: 'handle', at: 'nearHand' },
            { type: 'handle', at: 'farHand' },
            { type: 'arrow', from: [140, 150], to: [168, 150] },
            { type: 'arrow', from: [60, 150], to: [32, 150] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Front view. Let the knees come back in slowly, into the stretch on the outside of the hips.',
          ...SEATED_FRONT,
          armNear: [25, 8],
          armFar: [-25, -8],
          legNear: [10, 0, 90],
          legFar: [-10, 0, -90],
          props: [
            ...SEATED_FRONT_PROPS,
            { type: 'pad', x: 113.3, y: 112.4, w: 6, h: 18 },
            { type: 'pad', x: 80.7, y: 112.4, w: 6, h: 18 },
            { type: 'handle', at: 'nearHand' },
            { type: 'handle', at: 'farHand' },
            { type: 'arrow', from: [168, 150], to: [140, 150] },
            { type: 'arrow', from: [32, 150], to: [60, 150] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Seated Hip Adduction Machine
  {
    id: 'adductor-machine',
    name: 'Seated Hip Adduction Machine',
    aliases: ['Hip adductor machine', 'Inner thigh machine'],
    kind: 'strength',
    purpose:
      'Strengthens the inner thigh muscles that pull the legs together. They steady the hip and knee in every side step and landing, and strong adductors are linked to fewer groin strains in court sports. Starting from a wide stretch trains them at a long length.',
    equipment: ['Seated hip adduction machine'],
    setup: [
      'Set the start position so your legs begin in a wide stretch that feels comfortable, not forced.',
      'Sit with your hips all the way back in the seat and your feet on the foot rests.',
      'Place the pads on the inside of your knees and hold the handles.',
      'Sit tall with your back against the pad.',
    ],
    steps: [
      'Squeeze your knees in against the pads until they almost meet.',
      'Pause for one second with the knees together.',
      'Let the pads open slowly back to the wide start position.',
      'Stop just before the weight stack touches down, then start the next rep.',
    ],
    breathing: 'Breathe out as you squeeze in. Breathe in as the legs open.',
    tempo:
      '2 1 1 1 means two seconds to let the legs open, a one second pause in the wide stretch, one second to squeeze in, and a one second hold with the knees together.',
    rangeOfMotion:
      'From a comfortable wide stretch to the knees almost together. Widen the start position only a little at a time, over weeks.',
    muscles: {
      primary: ['adductors'],
      secondary: [],
    },
    emphasisNote:
      'The adductors, including the large adductor magnus, do most of the pulling. They are longest in the wide start position, so the slow opening and the pause there are an important part of the work. The trunk and glutes help hold the hips steady on the seat.',
    movementPattern: 'hip_adduction',
    joints: ['Hip'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['hip'],
    commonMistakes: [
      'Setting the start so wide that the groin is strained before the first rep.',
      'Letting the pads snap the legs open.',
      'Rocking the trunk forward to squeeze harder.',
      'Cutting the range short at the wide end.',
    ],
    goodFormFeels:
      'A strong squeeze along the inside of your thighs and a controlled stretch as the legs open, with no sharp feeling in the groin.',
    stopRules: [
      'Stop at once for groin pain. It is a stop signal, not something to push through.',
      'End the set when the range gets shorter or you start rocking the trunk.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Start light. The inner thigh muscles are small compared with the thighs.',
      'Groin pain is common in players who move sideways a lot. Report it early rather than training through it.',
      'Keep your fingers clear of the pads and levers while they move.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Adductor ball squeeze',
      reason: 'Lie on your back with the knees bent and squeeze a ball between them. Gentle inner thigh work with no machine.',
    },
    equipmentSubstitution: {
      exerciseId: 'cable-hip-adduction',
      name: 'Cable Hip Adduction',
      reason: 'One leg at a time with a low pulley when the machine is busy.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'copenhagen-plank',
        name: 'Copenhagen Plank',
        reason: 'A held body weight version for the same muscles, harder than it looks.',
      },
    ],
    loadIncrement: 'lower',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Front view. Seated with the pads on the inside of your knees, legs open in a comfortable stretch.',
          ...SEATED_FRONT,
          armNear: [25, 8],
          armFar: [-25, -8],
          legNear: [32, 0, 90],
          legFar: [-32, 0, -90],
          props: [
            ...SEATED_FRONT_PROPS,
            { type: 'pad', x: 110.3, y: 106.6, w: 6, h: 18 },
            { type: 'pad', x: 83.7, y: 106.6, w: 6, h: 18 },
            { type: 'handle', at: 'nearHand' },
            { type: 'handle', at: 'farHand' },
          ],
        },
        {
          label: 'In',
          caption: 'Front view. Squeeze the knees in until they almost meet, and pause for one second.',
          ...SEATED_FRONT,
          armNear: [25, 8],
          armFar: [-25, -8],
          legNear: [14, 0, 90],
          legFar: [-14, 0, -90],
          props: [
            ...SEATED_FRONT_PROPS,
            { type: 'pad', x: 99.2, y: 112, w: 5, h: 18 },
            { type: 'pad', x: 95.3, y: 112, w: 5, h: 18 },
            { type: 'handle', at: 'nearHand' },
            { type: 'handle', at: 'farHand' },
            { type: 'arrow', from: [168, 150], to: [140, 150] },
            { type: 'arrow', from: [32, 150], to: [60, 150] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Front view. Let the legs open slowly back into the wide stretch.',
          ...SEATED_FRONT,
          armNear: [25, 8],
          armFar: [-25, -8],
          legNear: [32, 0, 90],
          legFar: [-32, 0, -90],
          props: [
            ...SEATED_FRONT_PROPS,
            { type: 'pad', x: 110.3, y: 106.6, w: 6, h: 18 },
            { type: 'pad', x: 83.7, y: 106.6, w: 6, h: 18 },
            { type: 'handle', at: 'nearHand' },
            { type: 'handle', at: 'farHand' },
            { type: 'arrow', from: [140, 150], to: [168, 150] },
            { type: 'arrow', from: [60, 150], to: [32, 150] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Leg Press Calf Raise
  {
    id: 'leg-press-calf-raise',
    name: 'Leg Press Calf Raise',
    aliases: ['Calf press on the leg press'],
    kind: 'strength',
    purpose:
      'Builds the calves, mostly the gastrocnemius, with straight knees and heavy load but no weight on your spine. Stronger calves help with jumping, landing, and repeated take offs. The deep stretch at the bottom is the most valuable part of each rep.',
    equipment: ['45 degree leg press machine'],
    setup: [
      'Sit in the leg press with your lower back and hips pressed into the seat.',
      'Place the balls of your feet on the bottom edge of the platform, about hip width apart, with your heels hanging off.',
      'Press the platform up until your knees are straight but not locked.',
      'Leave the safety locks on, so the platform is caught if a foot slips.',
    ],
    steps: [
      'Let your heels drop slowly toward you until you feel a deep stretch in your calves.',
      'Pause for two seconds in the stretch without bouncing.',
      'Push the platform away through the balls of your feet, mostly the big toe side, as far as you can.',
      'Hold the top briefly, then lower slowly back into the stretch.',
      'Keep your knees straight and your hips on the seat the whole time.',
    ],
    breathing: 'Breathe steadily. Breathe out as you push and in as you lower. Do not hold your breath.',
    tempo:
      '2 2 1 1 means two seconds to lower into the stretch, a two second pause at the bottom, one second to push, and a one second hold at the top.',
    rangeOfMotion:
      'Use the full range, from a deep stretch with your heels past the platform edge to a full rise onto the balls of your feet. The stretched bottom of the range matters most, so never cut it short.',
    muscles: {
      primary: ['gastrocnemius'],
      secondary: ['soleus'],
    },
    emphasisNote:
      'Straight knees keep the gastrocnemius long, so it takes a larger share of the work, and the soleus helps on every rep. In one study (Kassiano and colleagues, 2023), training in the stretched bottom part of the range grew the gastrocnemius the most of the ranges tested. That is why the two second pause in the stretch matters.',
    movementPattern: 'plantar_flexion',
    joints: ['Ankle'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['achilles_calf'],
    commonMistakes: [
      'Bouncing out of the bottom instead of pausing.',
      'Bending the knees to push, which turns it into a small leg press.',
      'Placing the feet so high on the platform that the heels cannot drop.',
      'Using a short range at the top or the bottom.',
    ],
    goodFormFeels:
      'A deep stretch in your calves at the bottom, a strong squeeze at the top, and pressure through the balls of your feet. Your knees and hips stay still.',
    stopRules: [
      'End the set when the range gets shorter, you start to bounce, or your feet start to slide on the platform.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Keep the safety locks on for the whole set, so the platform is caught if a foot slips off the edge.',
      'Never lock your knees hard under the load.',
      'Heel and Achilles pain is common in growing athletes who jump a lot. Report it early rather than training through it.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Calf raise on a step',
      reason: 'Body weight only on both feet, holding a rail. Easy to learn the deep stretch and the pause.',
    },
    equipmentSubstitution: {
      exerciseId: 'standing-calf-raise',
      name: 'Standing Calf Raise',
      reason: 'The same straight knee calf work when the leg press is busy.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'single-leg-calf-raise',
        name: 'Single Leg Dumbbell Calf Raise',
        reason: 'One leg at a time on a step, with only a dumbbell.',
      },
    ],
    loadIncrement: 'lower',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Balls of the feet on the bottom edge of the platform, heels free, knees straight but not locked.',
          ...LEG_PRESS,
          armNear: [12, 62],
          legNear: [136, 133, 225],
          props: [...LEG_PRESS_PROPS, { type: 'bench', x: 101.8, y: 29.7, w: 38, h: 6, angle: 45 }, { type: 'handle', at: 'hands' }],
        },
        {
          label: 'Stretch',
          caption: 'Let the heels drop toward you into a deep calf stretch and pause for two seconds.',
          ...LEG_PRESS,
          armNear: [12, 62],
          legNear: [136, 133, 252],
          props: [
            ...LEG_PRESS_PROPS,
            { type: 'bench', x: 99.6, y: 33.3, w: 38, h: 6, angle: 45 },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [160, 26], to: [146, 40] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Push the platform away through the balls of your feet to a full rise. Knees stay straight.',
          ...LEG_PRESS,
          armNear: [12, 62],
          legNear: [136, 133, 197],
          props: [
            ...LEG_PRESS_PROPS,
            { type: 'bench', x: 105.5, y: 27.5, w: 38, h: 6, angle: 45 },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [150, 36], to: [164, 22] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Single Leg Dumbbell Calf Raise
  {
    id: 'single-leg-calf-raise',
    name: 'Single Leg Dumbbell Calf Raise',
    aliases: ['Single leg calf raise on a step'],
    kind: 'strength',
    purpose:
      'Builds the calf of one leg at a time with only a step and a dumbbell. Working each side alone helps you spot and even out differences between the legs you jump off. The deep stretch below the step is the most valuable part of each rep.',
    equipment: ['A step or sturdy block', 'One dumbbell', 'A rail or post to hold'],
    setup: [
      'Stand on a step next to a rail or post, with the ball of one foot on the edge and the heel hanging off.',
      'Hold a dumbbell in the hand on the same side as the working leg.',
      'Hold the rail lightly with the other hand, only for balance.',
      'Bend the other knee and hook that foot behind the working ankle, or hold it off the step.',
    ],
    steps: [
      'Keep your working knee straight but not locked.',
      'Lower your heel slowly below the step until you feel a deep stretch in your calf.',
      'Pause for two seconds in the stretch without bouncing.',
      'Push through the ball of your foot, mostly the big toe side, and rise as high as you can.',
      'Hold the top briefly, then lower slowly again.',
      'Finish all reps on one leg, then switch the dumbbell and your legs and match the reps.',
    ],
    breathing: 'Breathe steadily. Breathe out as you rise and in as you lower.',
    tempo:
      '2 2 1 1 means two seconds to lower the heel, a two second pause in the stretch, one second to rise, and a one second hold at the top.',
    rangeOfMotion:
      'From a deep stretch with the heel well below the step to as high on the ball of the foot as you can go. The stretch at the bottom matters most.',
    muscles: {
      primary: ['gastrocnemius'],
      secondary: ['soleus'],
    },
    emphasisNote:
      'A straight knee keeps the gastrocnemius long, so it takes a larger share of the work, and the soleus helps on every rep. The step lets the heel drop well below the toes, which loads the calf in its most stretched position. Training the calf at long lengths like this appears to be especially good for growth.',
    movementPattern: 'plantar_flexion',
    joints: ['Ankle'],
    laterality: 'unilateral',
    logSides: true,
    fatigueOverlap: ['achilles_calf'],
    commonMistakes: [
      'Bouncing at the bottom.',
      'Bending the knee to push up.',
      'Pulling yourself up with the rail hand.',
      'Rolling onto the little toe side.',
      'Rushing the reps so the stretch is skipped.',
    ],
    goodFormFeels: 'A deep stretch in the calf at the bottom, a strong squeeze at the top, and your body staying tall and still.',
    stopRules: [
      'End the set when the range gets shorter, you start to bounce, or you need the rail to pull yourself up.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Use a step that cannot slide or tip, and keep one hand on the rail for the whole set.',
      'Heel and Achilles pain is common in growing athletes who jump a lot. Report it early rather than training through it.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Two leg calf raise on a step',
      reason: 'Both feet share the load, and balance is easier.',
    },
    equipmentSubstitution: {
      exerciseId: 'leg-press-calf-raise',
      name: 'Leg Press Calf Raise',
      reason: 'Trains both calves with heavier load when no step or dumbbell is free.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'seated-calf-raise',
        name: 'Seated Calf Raise',
        reason: 'Bent knees shift the emphasis toward the soleus.',
      },
    ],
    loadIncrement: 'lower',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Ball of one foot on the step edge, dumbbell in the same side hand, other hand on the rail.',
          trunk: 172,
          head: 160,
          hip: [96.9, 80.6],
          armNear: [-3, -3],
          armFar: [60, 90],
          legNear: [3, -3, 90],
          legFar: [8, -60, 20],
          props: [
            { type: 'line', x1: 155, y1: 30, x2: 155, y2: 172 },
            { type: 'box', x: 104, y: 166, w: 44, h: 6 },
            { type: 'dumbbell', at: 'nearHand' },
          ],
        },
        {
          label: 'Stretch',
          caption: 'Lower the heel below the step into a deep calf stretch and pause for two seconds. Knee stays straight.',
          trunk: 172,
          head: 160,
          hip: [98.1, 85.3],
          armNear: [-3, -3],
          armFar: [60, 90],
          legNear: [3, -3, 118],
          legFar: [8, -60, 20],
          props: [
            { type: 'line', x1: 155, y1: 30, x2: 155, y2: 172 },
            { type: 'box', x: 104, y: 166, w: 44, h: 6 },
            { type: 'dumbbell', at: 'nearHand' },
            { type: 'arrow', from: [180, 110], to: [180, 130] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Push through the ball of the foot and rise as high as you can.',
          trunk: 172,
          head: 160,
          hip: [97.9, 76.2],
          armNear: [-3, -3],
          armFar: [60, 90],
          legNear: [3, -3, 64],
          legFar: [8, -60, 20],
          props: [
            { type: 'line', x1: 155, y1: 30, x2: 155, y2: 172 },
            { type: 'box', x: 104, y: 166, w: 44, h: 6 },
            { type: 'dumbbell', at: 'nearHand' },
            { type: 'arrow', from: [180, 130], to: [180, 110] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Kneeling Cable Crunch
  {
    id: 'cable-crunch',
    name: 'Kneeling Cable Crunch',
    aliases: ['Cable crunch', 'Rope crunch'],
    kind: 'strength',
    purpose:
      'Builds the front abs with a load you can add to in small steps, like any other muscle. Curling the spine against the cable trains the rectus abdominis through its full range, from a stretch when you are tall to a strong squeeze at the bottom.',
    equipment: ['Cable machine with a high pulley', 'Rope attachment', 'A mat for the knees'],
    setup: [
      'Set the pulley at the top and attach a rope.',
      'Kneel on a mat about one step back from the machine, facing it.',
      'Hold the rope ends beside your head, hands near your ears or forehead.',
      'Sit your hips slightly back, and keep them at that height for the whole set.',
    ],
    steps: [
      'Start tall, with the cable lifting your chest and a gentle stretch in your abs.',
      'Curl your ribs down toward your hips, rounding your back one part at a time.',
      'Keep your hips still. The movement comes from your spine, not from folding at the hips.',
      'Squeeze your abs for a moment at the bottom, with your elbows near your thighs.',
      'Uncurl slowly back up to tall, letting the abs stretch.',
    ],
    breathing: 'Breathe out fully as you curl down. Breathe in as you return to tall.',
    tempo:
      '2 0 1 1 means two seconds to uncurl, no pause at the top, one second to curl down, and a one second squeeze at the bottom.',
    rangeOfMotion:
      'From tall with a light stretch in the abs to a full curl with the ribs close to the hips. The hips stay at the same height the whole time.',
    muscles: {
      primary: ['rectus_abdominis'],
      secondary: ['obliques_core'],
    },
    emphasisNote:
      'Curling the spine is the main job of the rectus abdominis, so this loads it directly, with the obliques helping. Keeping the hips still stops the hip flexors from taking over. The stretch as you return to tall is part of the work, so do not rush it.',
    movementPattern: 'trunk_flexion',
    joints: ['Spine'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: [],
    commonMistakes: [
      'Folding at the hips and sitting back onto the heels instead of curling the spine.',
      'Pulling the rope down with the arms.',
      'Using so much weight that the cable jerks you back up.',
      'Nodding the head down without moving the ribs.',
    ],
    goodFormFeels:
      'A strong squeeze down the front of your belly at the bottom and a controlled stretch as you rise. Your hips and arms feel still.',
    stopRules: [
      'End the set when your hips start to move or you need your arms to pull the rope down.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Use a mat under your knees.',
      'Start light. A jerky rep strains the neck or back more than it trains the abs.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Crunch on the floor',
      reason: 'Body weight only, with the same ribs to hips curl and a shorter range.',
    },
    equipmentSubstitution: {
      exerciseId: 'hanging-leg-raise',
      name: 'Hanging Leg Raise',
      reason: 'Trains the abs from the other end, curling the pelvis up, when no cable is free.',
    },
    otherSubstitutions: [
      {
        exerciseId: null,
        name: 'Machine crunch',
        reason: 'A seated ab machine loads the same curl, if your gym has one.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Kneel facing the high pulley, rope beside your head, hips slightly back. Tall, with a stretch in the abs.',
          ...KNEEL,
          trunk: 168,
          head: 172,
          armNear: [93, -127],
          props: [...CRUNCH_PROPS, { type: 'cable', from: 'hands', to: [170, 8] }, { type: 'handle', at: 'hands' }],
        },
        {
          label: 'Curl',
          caption: 'Curl your ribs down toward your hips. The hips stay still while the spine rounds.',
          ...KNEEL,
          trunk: 115,
          head: 55,
          armNear: [40, 180],
          props: [
            ...CRUNCH_PROPS,
            { type: 'cable', from: 'hands', to: [170, 8] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [150, 60], to: [155, 95] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Uncurl slowly back to tall and let the abs stretch.',
          ...KNEEL,
          trunk: 168,
          head: 172,
          armNear: [93, -127],
          props: [
            ...CRUNCH_PROPS,
            { type: 'cable', from: 'hands', to: [170, 8] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [155, 95], to: [150, 60] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Ab Wheel Rollout
  {
    id: 'ab-wheel-rollout',
    name: 'Ab Wheel Rollout',
    aliases: ['Kneeling ab wheel rollout', 'Ab roller'],
    kind: 'bodyweight',
    purpose:
      'Trains the abs to stop your lower back from arching while your body lengthens. That stiffness through the trunk helps you pass force from the legs to the arm when you spike and block, and it loads the abs while they are long.',
    equipment: ['Ab wheel', 'A mat for the knees'],
    setup: [
      'Kneel on a mat with the ab wheel on the floor in front of your knees.',
      'Hold both handles with your shoulders over the wheel and your arms straight.',
      'Tuck your pelvis slightly under and brace your abs, so your back is flat.',
    ],
    steps: [
      'Roll the wheel forward slowly, letting your hips and shoulders move forward together.',
      'Stop as soon as you feel your lower back start to sag or arch, or just before.',
      'Hold for a moment with your abs tight and your back flat.',
      'Pull the wheel back toward your knees with your abs, without piking the hips up first.',
      'Start with short rolls, and add a little distance only when every rep stays flat.',
    ],
    breathing: 'Breathe in before you roll out. Hold the brace on the way out, and breathe out as you pull back.',
    tempo:
      '3 1 2 0 means three seconds to roll out, a one second hold at the far point, two seconds to roll back, and no rest at the start.',
    rangeOfMotion:
      'Only as far as your lower back stays neutral. For most people that starts as a short roll of about 30 centimetres. Go further over the weeks, never by letting the back arch.',
    muscles: {
      primary: ['rectus_abdominis', 'obliques_core'],
      secondary: ['lats', 'hip_flexors'],
    },
    emphasisNote:
      'The abs and obliques work hard to stop your lower back from arching as the wheel rolls away, and the lats help control the arms. The further you roll, the longer the lever and the harder it gets. Keeping the spine neutral is the whole point: repeated arching of the lower back is a known strain for young athletes who jump a lot.',
    movementPattern: 'anti_extension',
    joints: ['Spine', 'Shoulder', 'Hip'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['low_back', 'shoulder'],
    commonMistakes: [
      'Rolling out so far that the lower back sags.',
      'Piking the hips up high instead of moving the hips and shoulders together.',
      'Bending the arms to pull the wheel back.',
      'Holding your breath through the whole set.',
      'Dropping the head between the arms.',
    ],
    goodFormFeels:
      'A strong, deep effort through the whole front of your trunk, a back that stays flat like a table, and shoulders working to hold the arms.',
    stopRules: [
      'End the set at the planned reps in reserve, or as soon as your lower back starts to sag or arch.',
      EFFORT_RULE.never,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Use a mat under your knees.',
      'Start with short rolls. Rolling out too far too soon is the most common way to strain the lower back here.',
      'Roll toward a wall, so the wall stops the wheel at the distance you choose.',
    ],
    easierSubstitution: {
      exerciseId: 'dead-bug',
      name: 'Dead Bug',
      reason: 'Teaches the same flat back control lying on the floor, with no load on the arms.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Stability ball rollout',
      reason: 'Roll a large ball forward on your forearms when there is no ab wheel. The range is shorter and easier.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'cable-crunch',
        name: 'Kneeling Cable Crunch',
        reason: 'Loads the front abs with a cable when you want to add weight in small steps.',
      },
    ],
    loadIncrement: 'none',
    failure: 'never',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Kneel with the wheel under your shoulders, arms straight, back flat.',
          trunk: 118,
          hip: [42.7, 125.6],
          armNear: [0, 0],
          legNear: [10, -120, -150],
          props: [{ type: 'barbell', at: 'hands' }],
        },
        {
          label: 'Out',
          caption: 'Roll forward only as far as your lower back stays flat. Hips and shoulders move together.',
          trunk: 115,
          hip: [88.1, 149.3],
          armNear: [56.8, 56.8],
          legNear: [-65, -120, -150],
          props: [{ type: 'barbell', at: 'hands' }, { type: 'arrow', from: [120, 100], to: [160, 100] }],
        },
        {
          label: 'Finish',
          caption: 'Pull the wheel back toward your knees with your abs, back still flat.',
          trunk: 118,
          hip: [42.7, 125.6],
          armNear: [0, 0],
          legNear: [10, -120, -150],
          props: [{ type: 'barbell', at: 'hands' }, { type: 'arrow', from: [140, 100], to: [100, 100] }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Cable Woodchop
  {
    id: 'cable-woodchop',
    name: 'Cable Woodchop',
    aliases: ['High to low cable chop', 'Cable wood chop'],
    kind: 'strength',
    purpose:
      'Trains the obliques to turn the trunk with control, like the rotation you use when you swing at the ball. Turning through the upper back and hips together keeps the lower back from twisting on its own.',
    equipment: ['Cable machine with an adjustable pulley', 'Single handle or rope'],
    setup: [
      'Set the pulley at its highest point and attach a single handle.',
      'Stand side on to the machine, about one arm length away, feet a little wider than your shoulders.',
      'Hold the handle with both hands up by the pulley, arms straight.',
      'Brace your trunk and soften your knees.',
    ],
    steps: [
      'Pull the handle down and across your body toward the outside of your far hip, arms straight.',
      'Turn your chest and hips together, and let your back foot pivot on the ball of the foot.',
      'Stop when the handle is outside your far hip and your chest faces that way.',
      'Let the handle travel back up the same path slowly, turning back toward the pulley.',
      'Finish all reps on one side, then turn around and match them on the other.',
    ],
    breathing: 'Breathe out as you chop down. Breathe in as the handle returns.',
    tempo:
      '2 0 1 1 means two seconds to return, no pause at the top, one second to chop down, and a one second hold at the bottom.',
    rangeOfMotion:
      'From hands up toward the pulley to hands outside the far hip. The turn comes from the upper back and hips together, with no twisting strain in the lower back.',
    muscles: {
      primary: ['obliques_core'],
      secondary: ['rectus_abdominis'],
    },
    emphasisNote:
      'The obliques on both sides share the work of turning and then braking the trunk, with the front abs helping. Straight arms make a long lever, so the trunk does the work instead of the arms. Turning the hips with the chest spreads the rotation over several joints instead of twisting the lower back.',
    movementPattern: 'trunk_rotation',
    joints: ['Spine', 'Hip', 'Shoulder'],
    laterality: 'unilateral',
    logSides: true,
    fatigueOverlap: [],
    commonMistakes: [
      'Pulling with the arms and bending the elbows.',
      'Twisting only at the lower back while the hips stay fixed.',
      'Letting the cable yank you back to the start.',
      'Rounding forward at the bottom instead of turning.',
    ],
    goodFormFeels:
      'A strong effort along the sides of your waist, arms that feel like straight levers, and a smooth turn from the hips up.',
    stopRules: [
      'End the set at the planned reps in reserve, or when your arms start to bend or the turn gets jerky.',
      EFFORT_RULE.never,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Keep the cable path clear of other people.',
      'Start light. The goal is a controlled turn, not a heavy pull.',
    ],
    easierSubstitution: {
      exerciseId: 'pallof-press',
      name: 'Pallof Press',
      reason: 'Resists turning instead of producing it, which is easier to control while you learn to brace.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Dumbbell woodchop',
      reason: 'Hold one light dumbbell with both hands and chop from high to low when no cable is free.',
    },
    otherSubstitutions: [
      {
        exerciseId: null,
        name: 'Low to high cable woodchop',
        reason: 'The same turn in the other direction, with the pulley set low.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'never',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Front view. Stand side on to the high pulley, both hands on the handle, arms straight toward it.',
          ...CHOP,
          armNear: [-120, -122],
          armFar: [-122, -120],
          props: [CHOP_POST, { type: 'cable', from: 'hands', to: [16, 10] }, { type: 'handle', at: 'hands' }],
        },
        {
          label: 'Low',
          caption: 'Front view. Chop down and across to the outside of the far hip, turning chest and hips together.',
          ...CHOP,
          armNear: [40, 40],
          armFar: [38, 40],
          props: [
            CHOP_POST,
            { type: 'cable', from: 'hands', to: [16, 10] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [150, 40], to: [172, 78] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Front view. Let the handle travel back up the same path slowly, arms still straight.',
          ...CHOP,
          armNear: [-120, -122],
          armFar: [-122, -120],
          props: [
            CHOP_POST,
            { type: 'cable', from: 'hands', to: [16, 10] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [172, 78], to: [150, 40] },
          ],
        },
      ],
    },
  },
];
