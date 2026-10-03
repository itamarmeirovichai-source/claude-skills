import { EFFORT_RULE } from './effort';
import type { ExerciseContent } from '../types';

// Lower body library entries. Order matches LOWER_IDS in ids.ts.
// Pose angles follow the conventions in types.ts. Seated, lying, and machine poses
// set an explicit hip so props can be drawn at matching coordinates.

const painRule = (extra?: string) =>
  `Pain of 4 out of 10 or higher, or pain that worsens or changes your technique, pauses this exercise.${extra ? ` ${extra}` : ''} Report it to a parent, coach, or clinician.`;
const PAIN_RULE = painRule();

export const LOWER_EXERCISES: ExerciseContent[] = [
  // ---------------------------------------------------------------- Barbell Squat
  {
    id: 'barbell-squat',
    name: 'Barbell Squat',
    aliases: ['Back squat', 'High bar squat'],
    kind: 'strength',
    purpose:
      'Builds strength in the thighs and hips that carries over to jumping higher, landing softly, and sprinting.',
    equipment: ['Barbell', 'Squat rack with safety bars', 'Weight plates and collars'],
    setup: [
      'Set the bar in the rack at about armpit height and the safety bars just below the lowest point of your squat.',
      'Step under the bar and rest it on the muscle of your upper back, below the bony top of the spine.',
      'Grip the bar a little wider than your shoulders and keep your wrists straight.',
      'Stand with your feet about shoulder width apart and your toes turned out slightly.',
      'Breathe into your belly and brace your trunk as if someone were about to push on your stomach.',
    ],
    steps: [
      'Lift the bar out of the rack and take two or three small steps back.',
      'Sit down between your hips, letting your knees travel forward over your toes.',
      'Keep your whole foot on the floor and your chest facing forward.',
      'Pause briefly at the deepest point you can hold with a flat lower back.',
      'Drive the floor away and stand up, moving your hips and shoulders together.',
      'After the last rep, walk forward until the bar touches the uprights, then lower it onto the hooks.',
    ],
    breathing:
      'Breathe in and brace before each rep. Hold the brace on the way down and through the bottom. Breathe out near the top, then breathe in again before the next rep.',
    tempo: '3 1 1 0 means three seconds down, a one second pause at the bottom, one second up, and no rest at the top.',
    rangeOfMotion:
      'Go as deep as you can while your back stays neutral and your heels stay down. Thighs at parallel or a little lower is a good target. Set the safety bars to match that depth.',
    muscles: {
      primary: ['quads', 'glute_max'],
      secondary: ['adductors', 'erectors', 'hamstrings', 'obliques_core'],
    },
    emphasisNote:
      'The quads and glutes do most of the work. Squatting deeper asks more of the glutes and adductors, a more upright torso shifts a little more work to the quads, and a wider stance brings in more adductor. None of these muscles switch off in any version.',
    movementPattern: 'squat',
    joints: ['Hip', 'Knee', 'Ankle'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['knee', 'low_back', 'hip', 'systemic'],
    commonMistakes: [
      'Heels lifting at the bottom.',
      'Knees caving inward on the way up.',
      'Hips rising first so the squat turns into a forward lean.',
      'Losing the brace and rounding the lower back at the bottom.',
      'Cutting depth as the weight goes up.',
    ],
    goodFormFeels:
      'Pressure spread over the whole foot, a tight trunk, and effort shared by the front of the thighs and the glutes. The bar feels settled on your back and moves in a straight line over the middle of your foot.',
    stopRules: [
      'End the set when bar speed slows sharply or your technique changes, such as heels lifting, knees caving, or your back rounding.',
      EFFORT_RULE.never,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Always squat inside the rack with the safety bars set.',
      'Learn this lift with a qualified coach before you add load.',
      'Do not test a one rep max.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Goblet squat',
      reason: 'Holding one dumbbell at your chest makes depth and bracing easier to learn with a lighter load.',
    },
    equipmentSubstitution: {
      exerciseId: 'hack-squat',
      name: 'Hack Squat',
      reason: 'Use it when the rack is busy. The machine guides the path and keeps your torso more upright.',
    },
    otherSubstitutions: [
      { exerciseId: null, name: 'Leg press', reason: 'Trains the same muscles with much less load on the lower back.' },
      {
        exerciseId: 'bulgarian-split-squat',
        name: 'Bulgarian Split Squat',
        reason: 'Works one leg at a time with far lighter weights, which suits days when your back feels tired.',
      },
    ],
    loadIncrement: 'lower',
    failure: 'never',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Stand tall with the bar on your upper back and your trunk braced.',
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
  },

  // ---------------------------------------------------------------- Romanian Deadlift
  {
    id: 'romanian-deadlift',
    name: 'Romanian Deadlift',
    aliases: ['RDL', 'Barbell Romanian deadlift'],
    kind: 'strength',
    purpose:
      'Strengthens the hamstrings and glutes through a long range. This supports sprinting and jumping and helps the hamstrings cope with fast stretching.',
    equipment: ['Barbell', 'Weight plates and collars', 'Squat rack to start the bar at mid thigh height'],
    setup: [
      'Set the bar in the rack at mid thigh height so you can lift it out while standing tall.',
      'Hold the bar with an overhand grip just outside your thighs and step back with your feet about hip width apart.',
      'Unlock your knees into a soft bend and keep that same bend for the whole set.',
      'Brace your trunk and draw your shoulders slightly back and down.',
    ],
    steps: [
      'Push your hips straight back, as if closing a car door behind you with your backside.',
      'Let the bar slide down the front of your thighs, touching them or staying very close.',
      'Keep your back flat and your neck in line with your spine, with your eyes on the floor a couple of metres ahead.',
      'Stop when you feel a strong stretch in the back of your thighs, or just before your back starts to round.',
      'Drive your hips forward to stand tall, and squeeze your glutes at the top without leaning back.',
    ],
    breathing:
      'Breathe in and brace at the top. Hold the brace as you lower and as you start to stand. Breathe out near the top.',
    tempo: '3 1 1 0 means three seconds down, a one second pause at the bottom, one second up, and no rest at the top.',
    rangeOfMotion:
      'Lower until you feel a strong hamstring stretch while your back stays flat. For most people the bar ends between just below the knees and mid shin. Your back position sets the depth, not how low the bar goes.',
    muscles: {
      primary: ['hamstrings', 'glute_max'],
      secondary: ['adductors', 'erectors', 'obliques_core', 'forearm_flexors'],
    },
    emphasisNote:
      'The hamstrings and glutes share the load, and the adductor magnus helps extend the hip. Keeping the knee bend small increases the stretch on the hamstrings. More knee bend shares more of the work with the glutes and adductors. The back muscles and your grip hold position rather than move the weight.',
    movementPattern: 'hinge',
    joints: ['Hip'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['hamstring', 'low_back', 'hip', 'wrist_grip', 'systemic'],
    commonMistakes: [
      'Rounding the lower back to reach a lower bar position.',
      'Bending the knees more and more until the lift turns into a squat.',
      'Letting the bar drift away from your legs.',
      'Leaning back or pushing the hips too far forward at the top.',
      'Looking up at a mirror, which strains the neck.',
    ],
    goodFormFeels:
      'A strong, even stretch in the back of both thighs, your weight balanced over the middle of the foot, and a flat, braced back. Standing up feels like your hips pull you upright.',
    stopRules: [
      'End the set when your back starts to round, the bar drifts away from your legs, or your technique changes in any other way.',
      EFFORT_RULE.never,
      'Stop if your grip gives out before your hips and hamstrings do. Use a lighter weight next set rather than pushing through.',
      painRule('A sharp pull in the back of the thigh counts.'),
    ],
    safetyNotes: [
      'Learn the hip hinge and this lift with a qualified coach before you add load.',
      'Start each set from the rack at mid thigh height rather than lifting the bar from the floor.',
      'Do not test a one rep max.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Dumbbell Romanian deadlift',
      reason: 'Lighter dumbbells held at your sides make the hinge easier to learn, and you can stop the moment your back position changes.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Cable pull through',
      reason: 'Uses a low cable and a rope when no barbell is free. It trains the same hip hinge with less load on the lower back.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'seated-leg-curl',
        name: 'Seated Leg Curl',
        reason: 'Trains the hamstrings without a hinge if your lower back is tired.',
      },
    ],
    loadIncrement: 'lower',
    failure: 'never',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Stand tall holding the bar against your thighs, knees soft, trunk braced.',
          trunk: 180,
          armNear: [0, 0],
          legNear: [3, -3],
          props: [{ type: 'barbell', at: 'hands' }],
        },
        {
          label: 'Bottom',
          caption: 'Push the hips back with a flat back until the hamstrings are stretched. The bar stays close to the legs.',
          trunk: 115,
          armNear: [-15, -15],
          legNear: [32, -2],
          props: [
            { type: 'barbell', at: 'hands' },
            { type: 'arrow', from: [66, 76], to: [44, 76] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Drive the hips forward and stand tall without leaning back.',
          trunk: 180,
          armNear: [0, 0],
          legNear: [3, -3],
          props: [
            { type: 'barbell', at: 'hands' },
            { type: 'arrow', from: [60, 90], to: [80, 90] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Bulgarian Split Squat
  {
    id: 'bulgarian-split-squat',
    name: 'Bulgarian Split Squat',
    aliases: ['Rear foot elevated split squat'],
    kind: 'strength',
    purpose:
      'Builds single leg strength and control in the thigh and hip. Training one leg at a time helps you notice and reduce differences between sides that matter for take offs and landings.',
    equipment: ['Flat bench or box about knee height', 'Two dumbbells'],
    setup: [
      'Stand about two steps in front of a bench, facing away from it.',
      'Reach one foot back and rest the top of that foot on the bench, laces down.',
      'Place your front foot far enough forward that your front heel stays down at the bottom.',
      'Keep your feet about hip width apart side to side, not in one narrow line.',
      'Hold a dumbbell in each hand with your arms hanging by your sides.',
    ],
    steps: [
      'Brace your trunk and keep most of your weight on the front foot.',
      'Lower straight down by bending your front knee and letting your back knee drop toward the floor.',
      'Keep your front heel down and your front knee in line with your middle toes.',
      'Stop when your back knee is just above the floor or your front thigh is about parallel.',
      'Push through your whole front foot to stand back up.',
      'Finish all reps on one leg, then switch legs and match the reps.',
    ],
    breathing: 'Breathe in and brace at the top. Hold it on the way down and breathe out as you stand up.',
    tempo:
      '3 1 1 0 means three seconds down, a one second pause at the bottom, one second up, and no rest at the top. Use this steady pace unless the plan says otherwise.',
    rangeOfMotion:
      'Lower until your back knee is just above the floor or your front thigh is about parallel, whichever comes first with a steady trunk and your front heel down.',
    muscles: {
      primary: ['quads', 'glute_max'],
      secondary: ['glute_med', 'adductors', 'hamstrings', 'gastrocnemius', 'soleus', 'obliques_core'],
    },
    emphasisNote:
      'The front leg does most of the work. A longer stride and a slight forward lean from the hips bias the glutes and adductors, while a shorter stride and a more upright trunk bias the quads. The side of the hip works to keep your pelvis level. Every one of these muscles works in both setups.',
    movementPattern: 'lunge',
    joints: ['Hip', 'Knee', 'Ankle'],
    laterality: 'unilateral',
    logSides: true,
    fatigueOverlap: ['knee', 'hip', 'systemic'],
    commonMistakes: [
      'Standing too close to the bench so the front heel lifts.',
      'Pushing off the back foot instead of the front leg.',
      'Letting the front knee cave inward.',
      'Bouncing out of the bottom.',
      'Placing the feet in one narrow line, which makes balance hard.',
    ],
    goodFormFeels:
      'Most of the effort in your front thigh and glute, a light stretch at the front of your back hip, and a steady trunk. The back leg only helps with balance.',
    stopRules: [
      'End the set when your balance, knee position, or depth changes, or your front heel starts to lift.',
      EFFORT_RULE.never,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Learn the position with bodyweight first, then add dumbbells.',
      'Use a stable bench that cannot slide, with space around you in case you need to step out.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Split squat with the back foot on the floor',
      reason: 'Keeping both feet on the floor makes balance easier and shortens the range while you learn the position.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Goblet reverse lunge',
      reason: 'Needs only one dumbbell and no bench, and trains the same front leg pattern.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'hack-squat',
        name: 'Hack Squat',
        reason: 'A two leg option if balance or the back foot position bothers you.',
      },
    ],
    loadIncrement: 'lower',
    failure: 'never',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Back foot laces down on the bench, front foot well forward, dumbbells hanging.',
          trunk: 176,
          armNear: [0, 0],
          legNear: [34.7, 10.2],
          legFar: [-3.5, -101.3, -95],
          hip: [88, 98],
          props: [
            { type: 'bench', x: 14, y: 136, w: 34, h: 8 },
            { type: 'dumbbell', at: 'hands' },
          ],
        },
        {
          label: 'Bottom',
          caption: 'Lower straight down until the back knee is just above the floor. Front heel stays down.',
          trunk: 172,
          armNear: [0, 0],
          legNear: [80, -15],
          legFar: [-25, -143, -95],
          hip: [88, 126],
          props: [
            { type: 'bench', x: 14, y: 136, w: 34, h: 8 },
            { type: 'dumbbell', at: 'hands' },
            { type: 'arrow', from: [160, 70], to: [160, 105] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Push through the whole front foot to stand back up.',
          trunk: 176,
          armNear: [0, 0],
          legNear: [34.7, 10.2],
          legFar: [-3.5, -101.3, -95],
          hip: [88, 98],
          props: [
            { type: 'bench', x: 14, y: 136, w: 34, h: 8 },
            { type: 'dumbbell', at: 'hands' },
            { type: 'arrow', from: [160, 105], to: [160, 70] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Standing Calf Raise
  {
    id: 'standing-calf-raise',
    name: 'Standing Calf Raise',
    aliases: ['Machine standing calf raise'],
    kind: 'strength',
    purpose:
      'Strengthens the calves and the Achilles tendon for jumping, landing, and sprinting. Stronger calves also handle the repeated take offs of volleyball better.',
    equipment: ['Standing calf raise machine with a foot block'],
    setup: [
      'Set the shoulder pads so you have to bend your knees slightly to get under them.',
      'Place the balls of your feet on the edge of the foot block, about hip width apart, with your heels free.',
      'Stand up under the pads so your knees are straight but not locked.',
      'Point your toes straight ahead or turned out slightly, and hold the handles.',
    ],
    steps: [
      'Lower your heels slowly until you feel a strong stretch in your calves.',
      'Pause for two full seconds in the stretch without bouncing. Training this stretched part grew the calves most in a study.',
      'Push through the balls of your feet, mostly the big toe side, to rise as high as you can.',
      'Hold the top for a moment with your ankles steady, not rolling outward.',
      'Lower slowly and repeat, keeping your knees straight the whole time.',
    ],
    breathing: 'Breathe steadily. Breathe out as you rise and in as you lower. Do not hold your breath.',
    tempo:
      '2 2 1 1 means two seconds to lower the heels, a two second pause in the stretch, one second to rise, and a one second hold at the top.',
    rangeOfMotion:
      'Use the full range, from a deep stretch with your heels below the block to as high on your toes as you can go. The stretched part of the range matters most, so do not cut it short.',
    muscles: {
      primary: ['gastrocnemius'],
      secondary: ['soleus'],
    },
    emphasisNote:
      'Straight knees keep the gastrocnemius long, so it takes a larger share of the work. The soleus still works on every rep. Bending the knees shifts the emphasis toward the soleus, which is what the seated calf raise does.',
    movementPattern: 'plantar_flexion',
    joints: ['Ankle'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['achilles_calf'],
    commonMistakes: [
      'Bouncing at the bottom instead of pausing in the stretch.',
      'Bending the knees to push the weight up.',
      'Cutting the range short at the bottom or the top.',
      'Rolling onto the little toes at the top.',
    ],
    goodFormFeels:
      'A deep stretch in your calves at the bottom and a strong squeeze at the top, with the pressure through the balls of your feet.',
    stopRules: [
      'End the set when your range gets shorter, you start to bounce, or your knees bend to help.',
      EFFORT_RULE.all,
      'Pain of 4 out of 10 or higher in the Achilles tendon, heel, or calf, or pain that worsens or changes your technique, pauses this exercise. Report it to a parent, coach, or clinician.',
    ],
    safetyNotes: [
      'Heel pain is common in growing athletes who jump a lot. Report it early rather than training through it.',
      'Keep the balls of your feet firmly on the block so they cannot slip off.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Bodyweight calf raise on a step',
      reason: 'No added load. Hold a rail for balance and learn the full range first.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Smith machine calf raise',
      reason: 'Stand with your forefeet on a step or plate and the bar across your upper back when there is no calf machine.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'seated-calf-raise',
        name: 'Seated Calf Raise',
        reason: 'Shifts the emphasis toward the soleus. Use it when the standing machine is not available.',
      },
    ],
    loadIncrement: 'lower',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Stand tall under the shoulder pads with your knees straight but not locked and heels down.',
          trunk: 180,
          armNear: [30, 170],
          legNear: [0, 0, 90],
          footX: 95,
          props: [
            { type: 'line', x1: 68, y1: 20, x2: 68, y2: 172 },
            { type: 'line', x1: 68, y1: 34, x2: 86, y2: 34 },
            { type: 'pad', x: 84, y: 30, w: 22, h: 8 },
            { type: 'handle', at: 'hands' },
          ],
        },
        {
          label: 'Top',
          caption: 'Push through the balls of the feet and lift the heels as high as you can. Knees stay straight.',
          trunk: 180,
          armNear: [30, 170],
          legNear: [0, 0, 58],
          footX: 97,
          props: [
            { type: 'line', x1: 68, y1: 20, x2: 68, y2: 172 },
            { type: 'line', x1: 68, y1: 27, x2: 88, y2: 27 },
            { type: 'pad', x: 86, y: 23, w: 22, h: 8 },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [150, 110], to: [150, 90] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Lower the heels slowly all the way down. On the foot block they drop below it into a stretch.',
          trunk: 180,
          armNear: [30, 170],
          legNear: [0, 0, 90],
          footX: 95,
          props: [
            { type: 'line', x1: 68, y1: 20, x2: 68, y2: 172 },
            { type: 'line', x1: 68, y1: 34, x2: 86, y2: 34 },
            { type: 'pad', x: 84, y: 30, w: 22, h: 8 },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [150, 90], to: [150, 110] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Tibialis Raise
  {
    id: 'tibialis-raise',
    name: 'Tibialis Raise',
    aliases: ['Wall tibialis raise', 'Toe raise'],
    kind: 'bodyweight',
    purpose:
      'Strengthens the muscle on the front of the shin, which lifts the foot and helps control landings and sudden stops. It balances the heavy calf work that jumping demands.',
    equipment: ['A clear wall'],
    setup: [
      'Stand with your back and hips against a wall.',
      'Walk your heels out about one and a half foot lengths from the wall, feet hip width apart.',
      'Keep your legs straight but not locked, and let your arms hang by your sides.',
      'Let the wall and your heels take your weight.',
    ],
    steps: [
      'Pull your toes up toward your shins as high as you can, keeping your heels on the floor.',
      'Hold the top for a moment.',
      'Lower your toes slowly until they almost touch the floor.',
      'Repeat without letting your toes slap down.',
      'To make it harder, move your heels a little further from the wall. To make it easier, move them closer.',
    ],
    breathing: 'Breathe steadily throughout. There is no need to brace hard.',
    tempo:
      '2 1 1 1 means two seconds to lower the toes, a one second pause just above the floor, one second to lift them, and a one second hold at the top.',
    rangeOfMotion:
      'Lift your toes as high as your ankles allow and lower until they nearly touch the floor. Keep your heels down the whole time.',
    muscles: {
      primary: ['tibialis_anterior'],
      secondary: [],
    },
    emphasisNote:
      'The tibialis anterior does most of the lifting, helped by the smaller muscles that raise the toes. Moving your feet further from the wall puts more of your body weight through the shins without adding any equipment.',
    movementPattern: 'dorsiflexion',
    joints: ['Ankle'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shin'],
    commonMistakes: [
      'Letting the toes slap down instead of lowering them slowly.',
      'Bending the knees or pushing the hips off the wall to help.',
      'Stopping halfway up instead of lifting the toes fully.',
      'Rushing the reps so the pauses disappear.',
    ],
    goodFormFeels:
      'A strong burn along the front of your shins by the end of the set, with your heels planted and the rest of your body still.',
    stopRules: [
      'End the set when your range shrinks, your toes start to slap down, or your knees bend to help.',
      EFFORT_RULE.never,
      PAIN_RULE,
    ],
    safetyNotes: [
      'A muscle burn in the front of the shin is normal. Sharp pain or pain on the bone of the shin is not, so stop and report it, especially if it also shows up after jumping.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Seated toe raise',
      reason: 'Sit on a bench with your heels on the floor and lift your toes. The load is lower and easy to control.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Resistance band toe raise',
      reason: 'Sit with a band looped over the top of your foot and anchored in front, then pull your toes up against it when there is no free wall.',
    },
    otherSubstitutions: [
      {
        exerciseId: null,
        name: 'Tib bar raise',
        reason: 'Sit on a box with a tib bar over your feet. It adds a small load once the wall version with your heels far out feels easy.',
      },
    ],
    loadIncrement: 'none',
    failure: 'never',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Lean back on the wall with your heels out in front and your legs straight.',
          trunk: 181,
          head: 176,
          armNear: [0, 0],
          legNear: [14, 14, 90],
          hip: [95.2, 92.4],
          props: [{ type: 'line', x1: 84.5, y1: 12, x2: 84.5, y2: 172 }],
        },
        {
          label: 'Top',
          caption: 'Pull your toes up as high as you can. Heels stay on the floor.',
          trunk: 181,
          head: 176,
          armNear: [0, 0],
          legNear: [14, 14, 125],
          hip: [94.7, 90.7],
          props: [
            { type: 'line', x1: 84.5, y1: 12, x2: 84.5, y2: 172 },
            { type: 'arrow', from: [150, 168], to: [150, 146] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Lower your toes slowly until they almost touch the floor.',
          trunk: 181,
          head: 176,
          armNear: [0, 0],
          legNear: [14, 14, 90],
          hip: [95.2, 92.4],
          props: [
            { type: 'line', x1: 84.5, y1: 12, x2: 84.5, y2: 172 },
            { type: 'arrow', from: [150, 146], to: [150, 168] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Hack Squat
  {
    id: 'hack-squat',
    name: 'Hack Squat',
    aliases: ['Machine hack squat'],
    kind: 'strength',
    purpose:
      'Builds quad strength with your back supported, so your legs can work hard with less demand on balance and the lower back.',
    equipment: ['Hack squat machine'],
    setup: [
      'Stand on the platform with your back flat against the pad and your shoulders under the shoulder pads.',
      'Place your feet about shoulder width apart in the middle of the platform, toes turned out slightly.',
      'Hold the handles, stand up to take the weight, and release the safety catches.',
      'Brace your trunk and keep your head resting against the pad.',
    ],
    steps: [
      'Lower yourself by bending your knees and hips together, letting your knees travel forward over your toes.',
      'Keep your hips and upper back against the pad and your heels flat.',
      'Pause at the lowest point you can hold without your hips curling off the pad.',
      'Push through your whole foot to straighten your legs.',
      'Stop just short of locking your knees, then start the next rep.',
      'After the last rep, lock the safety catches back into place before you step off.',
    ],
    breathing:
      'Breathe in and brace before each rep, hold it on the way down, and breathe out as you pass the hardest part of the way up.',
    tempo: '3 1 1 0 means three seconds down, a one second pause at the bottom, one second up, and no rest at the top.',
    rangeOfMotion:
      'Go as deep as you can while your lower back stays on the pad and your heels stay flat. Thighs parallel to the platform or a little lower is a good target.',
    muscles: {
      primary: ['quads'],
      secondary: ['glute_max', 'adductors'],
    },
    emphasisNote:
      'The supported, upright back and the forward knee travel bias the quads. Placing your feet higher on the platform shifts more work to the glutes and adductors, and a lower foot position biases the quads further. The glutes and adductors work in every foot position.',
    movementPattern: 'squat',
    joints: ['Hip', 'Knee', 'Ankle'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['knee', 'hip', 'systemic'],
    commonMistakes: [
      'Hips curling off the pad at the bottom.',
      'Heels lifting as the knees travel forward.',
      'Knees caving inward on the way up.',
      'Locking the knees hard at the top.',
      'Cutting depth to move more weight.',
    ],
    goodFormFeels:
      'A deep bend in the knees, pressure through the whole foot, and strong effort in the front of the thighs. Your back feels supported and still.',
    stopRules: [
      'End the set when your hips lift off the pad, your heels rise, your knees cave, or your depth gets shallower.',
      EFFORT_RULE.last,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Ask a coach to show you how the safety catches work, and always lock them before you step off.',
      'Keep your hands on the handles and away from the rails while the sled moves.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Leg press',
      reason: 'Fully seated with your back supported and simple to stop at any depth. Good while you learn to control deep knee bending.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Goblet squat',
      reason: 'Needs only one dumbbell. Holding it at your chest keeps your torso upright, so the quads still do most of the work.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'barbell-squat',
        name: 'Barbell Squat',
        reason: 'A free weight option when a coach and a rack are available. It needs more balance and bracing.',
      },
    ],
    loadIncrement: 'lower',
    failure: 'last',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Back flat on the pad, shoulders under the pads, feet in the middle of the platform.',
          trunk: 205,
          armNear: [40, 175],
          legNear: [30, 26, 100],
          hip: [70, 84],
          props: [
            { type: 'line', x1: 26.9, y1: 37.8, x2: 75.5, y2: 142 },
            { type: 'line', x1: 75.5, y1: 142, x2: 75.5, y2: 172 },
            { type: 'bench', x: 62.1, y: 92.5, w: 64, h: 8, angle: -115 },
            { type: 'line', x1: 100.5, y1: 162.9, x2: 128.1, y2: 158 },
            { type: 'line', x1: 114, y1: 161, x2: 114, y2: 172 },
            { type: 'handle', at: 'hands' },
          ],
        },
        {
          label: 'Bottom',
          caption: 'Bend the knees and hips together. Knees travel forward, hips and back stay on the pad.',
          trunk: 205,
          armNear: [40, 175],
          legNear: [82.3, -26, 100],
          hip: [84.4, 114.8],
          props: [
            { type: 'line', x1: 26.9, y1: 37.8, x2: 75.5, y2: 142 },
            { type: 'line', x1: 75.5, y1: 142, x2: 75.5, y2: 172 },
            { type: 'bench', x: 76.5, y: 123.3, w: 64, h: 8, angle: -115 },
            { type: 'line', x1: 100.5, y1: 162.9, x2: 128.1, y2: 158 },
            { type: 'line', x1: 114, y1: 161, x2: 114, y2: 172 },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [160, 60], to: [172, 86] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Push through the whole foot and stop just short of locking the knees.',
          trunk: 205,
          armNear: [40, 175],
          legNear: [30, 26, 100],
          hip: [70, 84],
          props: [
            { type: 'line', x1: 26.9, y1: 37.8, x2: 75.5, y2: 142 },
            { type: 'line', x1: 75.5, y1: 142, x2: 75.5, y2: 172 },
            { type: 'bench', x: 62.1, y: 92.5, w: 64, h: 8, angle: -115 },
            { type: 'line', x1: 100.5, y1: 162.9, x2: 128.1, y2: 158 },
            { type: 'line', x1: 114, y1: 161, x2: 114, y2: 172 },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [172, 86], to: [160, 60] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Barbell Hip Thrust
  {
    id: 'barbell-hip-thrust',
    name: 'Barbell Hip Thrust',
    aliases: ['Hip thrust'],
    kind: 'strength',
    purpose:
      'Builds glute strength at full hip extension, the position you drive through when you jump and sprint.',
    equipment: ['Barbell', 'Flat bench', 'Thick bar pad', 'Weight plates and collars'],
    setup: [
      'Sit on the floor with your upper back against the long side of a bench, the edge just below your shoulder blades.',
      'Roll the padded bar over your legs until it sits in the crease of your hips.',
      'Place your feet flat and about hip width apart, so your shins will be close to vertical at the top.',
      'Hold the bar with both hands just outside your hips to keep it steady.',
    ],
    steps: [
      'Tuck your chin slightly, brace your trunk, and push through your heels and midfoot.',
      'Drive your hips up until your body is straight from shoulders to knees.',
      'Squeeze your glutes at the top and keep your ribs down so your lower back does not arch.',
      'Pause for a moment at the top.',
      'Lower your hips under control until they are just above the floor.',
    ],
    breathing: 'Breathe in and brace before each rep. Breathe out at the top once your hips are fully up.',
    tempo:
      '2 1 1 1 means two seconds to lower the hips, a one second pause at the bottom, one second to drive up, and a one second squeeze at the top.',
    rangeOfMotion:
      'Move from hips just above the floor to a straight line from shoulders to knees. Stop at full hip extension. Going higher only arches the lower back.',
    muscles: {
      primary: ['glute_max'],
      secondary: ['hamstrings', 'adductors'],
    },
    emphasisNote:
      'The glutes are under the most tension near the top, where the hips are fully straight. Feet a little further out bring in more hamstring, and feet closer in bring in more quad. The glutes lead in every foot position.',
    movementPattern: 'hip_extension',
    joints: ['Hip'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['hip', 'low_back'],
    commonMistakes: [
      'Arching the lower back at the top instead of finishing with the glutes.',
      'Pushing through the toes so the heels lift.',
      'Letting the knees fall in or out.',
      'Sliding the upper back up the bench during the set.',
      'Rushing the top and skipping the pause.',
    ],
    goodFormFeels:
      'A strong squeeze in your glutes at the top, pressure through your heels, and ribs staying down. The bench works as a pivot under your shoulder blades.',
    stopRules: [
      'End the set when you can no longer reach full hip extension with a pause, or your lower back starts to arch to finish the rep.',
      EFFORT_RULE.never,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Use a thick bar pad so the bar does not press into your hip bones.',
      'Set the bench against a wall or rack so it cannot slide.',
      'Learn the setup with a qualified coach before you add heavy plates.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Glute bridge',
      reason: 'Lying on the floor shortens the range and needs no bench. Start with bodyweight or a light plate.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Dumbbell hip thrust',
      reason: 'Rest one dumbbell in the crease of your hips when no barbell is free.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'romanian-deadlift',
        name: 'Romanian Deadlift',
        reason: 'Another hip extension exercise that also loads the hamstrings in a long stretch.',
      },
    ],
    loadIncrement: 'lower',
    failure: 'never',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Upper back on the bench edge, bar in the hip crease, hips just above the floor.',
          trunk: -120,
          head: -150,
          armNear: [37, 116.6],
          legNear: [117.3, 7.7, 90],
          hip: [107.3, 151.6],
          props: [
            { type: 'bench', x: 18, y: 140.5, w: 53, h: 8 },
            { type: 'barbell', at: [107.3, 139.6] },
          ],
        },
        {
          label: 'Top',
          caption: 'Drive the hips up until shoulders, hips, and knees line up. Chin tucked, ribs down.',
          trunk: -90,
          head: -125,
          armNear: [77.8, 134.2],
          legNear: [90, 0, 90],
          hip: [108, 132],
          props: [
            { type: 'bench', x: 18, y: 140.5, w: 53, h: 8 },
            { type: 'barbell', at: [108, 120] },
            { type: 'arrow', from: [128, 110], to: [128, 88] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Lower the hips under control until they are just above the floor.',
          trunk: -120,
          head: -150,
          armNear: [37, 116.6],
          legNear: [117.3, 7.7, 90],
          hip: [107.3, 151.6],
          props: [
            { type: 'bench', x: 18, y: 140.5, w: 53, h: 8 },
            { type: 'barbell', at: [107.3, 139.6] },
            { type: 'arrow', from: [128, 100], to: [128, 122] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Seated Leg Curl
  {
    id: 'seated-leg-curl',
    name: 'Seated Leg Curl',
    aliases: ['Seated hamstring curl'],
    kind: 'strength',
    purpose:
      'Strengthens the hamstrings through knee bending while the hips are bent, so the muscles train at a long length. Strong hamstrings support sprinting and help protect against strains.',
    equipment: ['Seated leg curl machine'],
    setup: [
      'Adjust the back pad so the machine pivot lines up with the side of your knee.',
      'Set the lower pad on the back of your lower legs, just above your heels.',
      'Lower the thigh pad until it presses firmly on your thighs just above the knees.',
      'Sit tall, or lean forward slightly from the hips, and hold the handles.',
    ],
    steps: [
      'Start with your knees almost straight and your feet relaxed.',
      'Curl your heels down and back under the seat as far as you can.',
      'Pause briefly with your knees fully bent.',
      'Let the pad rise slowly until your knees are almost straight again.',
      'Keep your thighs pinned under the pad and your hips on the seat the whole time.',
    ],
    breathing: 'Breathe out as you curl and breathe in as you return. Keep your breathing steady.',
    tempo:
      '2 1 1 1 means two seconds to let the knees straighten, a one second pause with the legs almost straight, one second to curl, and a one second squeeze with the knees bent.',
    rangeOfMotion:
      'Move from almost straight knees to as much knee bend as you can control, usually a little past a right angle. Do not let the weight stack rest between reps.',
    muscles: {
      primary: ['hamstrings'],
      secondary: [],
    },
    emphasisNote:
      'Sitting with the hips bent keeps the hamstrings long, which makes this a strong choice for hamstring growth. Leaning slightly forward increases that stretch. The gastrocnemius also helps bend the knee, a little more when you pull your toes toward your shins.',
    movementPattern: 'knee_flexion',
    joints: ['Knee'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['hamstring', 'knee'],
    commonMistakes: [
      'Lifting the hips off the seat to swing the weight.',
      'Leaving the thigh pad loose so your legs slide.',
      'Stopping short of a full curl.',
      'Letting the weight drop fast on the way back.',
    ],
    goodFormFeels:
      'A strong squeeze in the back of your thighs at the end of each curl and a controlled stretch as your knees straighten. Your hips and thighs stay still.',
    stopRules: [
      'End the set when you can no longer curl through the full range or your hips start to lift.',
      EFFORT_RULE.all,
      'Stop the set if a hamstring cramps. Rest and stretch gently before you try again.',
      PAIN_RULE,
    ],
    safetyNotes: [
      'Check that the pivot lines up with your knee before every session. A poor setup strains the knee.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Lying band leg curl',
      reason: 'Lie face down with a light band anchored low in front of your feet. The resistance is light and easy to control.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Lying leg curl',
      reason: 'Trains the same knee bending action when the seated machine is busy. Your hips are straighter, so the hamstring stretch is a little smaller.',
    },
    otherSubstitutions: [
      {
        exerciseId: null,
        name: 'Stability ball hamstring curl',
        reason: 'A bodyweight option that needs only a stability ball.',
      },
    ],
    loadIncrement: 'lower',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Seated with the thigh pad above the knees and the lower pad behind the ankles. Knees almost straight.',
          trunk: 184,
          armNear: [18.3, 75.8],
          legNear: [90, 72, 160],
          hip: [62, 116],
          props: [
            { type: 'bench', x: 40, y: 122, w: 46, h: 8 },
            { type: 'bench', x: 50, y: 118.9, w: 56, h: 8, angle: -94 },
            { type: 'pad', x: 86, y: 101, w: 16, h: 9 },
            { type: 'line', x1: 104, y1: 116, x2: 133.8, y2: 137.3 },
            { type: 'pad', x: 127.8, y: 131.3, w: 12, h: 12 },
            { type: 'handle', at: 'hands' },
          ],
        },
        {
          label: 'Curl',
          caption: 'Curl the heels down and back under the seat. Hips stay on the seat.',
          trunk: 184,
          armNear: [18.3, 75.8],
          legNear: [90, -12, 78],
          hip: [62, 116],
          props: [
            { type: 'bench', x: 40, y: 122, w: 46, h: 8 },
            { type: 'bench', x: 50, y: 118.9, w: 56, h: 8, angle: -94 },
            { type: 'pad', x: 86, y: 101, w: 16, h: 9 },
            { type: 'line', x1: 104, y1: 116, x2: 86, y2: 147.9 },
            { type: 'pad', x: 80, y: 141.9, w: 12, h: 12 },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [150, 140], to: [124, 164] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Let the pad rise slowly until the knees are almost straight.',
          trunk: 184,
          armNear: [18.3, 75.8],
          legNear: [90, 72, 160],
          hip: [62, 116],
          props: [
            { type: 'bench', x: 40, y: 122, w: 46, h: 8 },
            { type: 'bench', x: 50, y: 118.9, w: 56, h: 8, angle: -94 },
            { type: 'pad', x: 86, y: 101, w: 16, h: 9 },
            { type: 'line', x1: 104, y1: 116, x2: 133.8, y2: 137.3 },
            { type: 'pad', x: 127.8, y: 131.3, w: 12, h: 12 },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [128, 164], to: [156, 146] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Leg Extension
  {
    id: 'leg-extension',
    name: 'Leg Extension',
    aliases: ['Machine leg extension', 'Knee extension'],
    kind: 'strength',
    purpose:
      'Trains the quads through the full knee straightening range, above all the rectus femoris, the quad head that also crosses the hip. Squats and leg presses barely grow that head, but leg extensions do. Strong quads help you absorb landings.',
    equipment: ['Leg extension machine'],
    setup: [
      'Adjust the back pad so the machine pivot lines up with the side of your knee.',
      'Set the shin pad on the front of your lower legs, just above the ankles.',
      'Recline the back pad as far as it goes, or lean back against it, so your hips are more open. This stretches the rectus femoris, and leaning back grew it more in a study.',
      'Sit all the way back with your thighs flat on the seat, and hold the handles by your hips to keep yourself from sliding.',
    ],
    steps: [
      'Start with your knees bent at about a right angle.',
      'Straighten your knees until your legs are almost fully straight.',
      'Pause briefly at the top with the front of your thighs tight.',
      'Lower the pad slowly back to the start.',
      'Keep your hips on the seat and your back against the pad throughout.',
    ],
    breathing: 'Breathe out as you straighten your legs and breathe in as you lower them.',
    tempo:
      '2 1 1 1 means two seconds to lower the pad, a one second pause with the knees bent, one second to straighten, and a one second hold at the top.',
    rangeOfMotion:
      'Move from about a right angle at the knee to almost straight. Stop just short of snapping the knee into a hard lock.',
    muscles: {
      primary: ['quads'],
      secondary: [],
    },
    emphasisNote:
      'All four quad muscles straighten the knee here. Leaning back a little lengthens the rectus femoris, the quad muscle that also crosses the hip, so it takes a larger share of the work. Turning the toes in or out makes little real difference.',
    movementPattern: 'knee_extension',
    joints: ['Knee'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['knee'],
    commonMistakes: [
      'Swinging the weight up and letting it drop.',
      'Lifting the hips off the seat at the top.',
      'Snapping the knees into a hard lock.',
      'Setting the pivot too far from the knee.',
    ],
    goodFormFeels:
      'A strong squeeze in the front of your thighs at the top, smooth movement at the knee, and no sharp pressure around the kneecap.',
    stopRules: [
      'End the set when you can no longer reach almost straight knees with a pause, or you start to swing.',
      EFFORT_RULE.all,
      painRule('Pain just below the kneecap counts.'),
    ],
    safetyNotes: [
      'Pain just below the kneecap is common in growing jumpers. Report it early instead of training through it.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Seated band knee extension',
      reason: 'Sit on a bench with a light band anchored behind you and around your ankle. The load is light and easy to control.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Heels elevated goblet squat',
      reason: 'Raising your heels on a small plate lets the knees travel forward, which biases the quads when there is no machine.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'hack-squat',
        name: 'Hack Squat',
        reason: 'Another quad biased option that also trains the hips.',
      },
    ],
    loadIncrement: 'lower',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Seated with the shin pad just above the ankles and the knees bent at about a right angle.',
          trunk: 188,
          armNear: [2.6, 41.3],
          legNear: [90, -3, 90],
          hip: [62, 116],
          props: [
            { type: 'bench', x: 40, y: 122, w: 58, h: 8 },
            { type: 'bench', x: 50.4, y: 119.7, w: 56, h: 8, angle: -98 },
            { type: 'line', x1: 104, y1: 116, x2: 113.4, y2: 146.5 },
            { type: 'pad', x: 107.4, y: 140.5, w: 12, h: 12 },
            { type: 'handle', at: 'hands' },
          ],
        },
        {
          label: 'Top',
          caption: 'Straighten the knees until the legs are almost straight, then pause.',
          trunk: 188,
          armNear: [2.6, 41.3],
          legNear: [90, 84, 170],
          hip: [62, 116],
          props: [
            { type: 'bench', x: 40, y: 122, w: 58, h: 8 },
            { type: 'bench', x: 50.4, y: 119.7, w: 56, h: 8, angle: -98 },
            { type: 'line', x1: 104, y1: 116, x2: 135, y2: 108.2 },
            { type: 'pad', x: 129, y: 102.2, w: 12, h: 12 },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [150, 160], to: [172, 132] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Lower the pad slowly back to the start. Hips stay on the seat.',
          trunk: 188,
          armNear: [2.6, 41.3],
          legNear: [90, -3, 90],
          hip: [62, 116],
          props: [
            { type: 'bench', x: 40, y: 122, w: 58, h: 8 },
            { type: 'bench', x: 50.4, y: 119.7, w: 56, h: 8, angle: -98 },
            { type: 'line', x1: 104, y1: 116, x2: 113.4, y2: 146.5 },
            { type: 'pad', x: 107.4, y: 140.5, w: 12, h: 12 },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [160, 112], to: [150, 142] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Cable Hip Abduction
  {
    id: 'cable-hip-abduction',
    name: 'Cable Hip Abduction',
    aliases: ['Standing cable hip abduction'],
    kind: 'strength',
    purpose:
      'Strengthens the side of the hip, which keeps your pelvis level and your knee lined up during single leg landings, take offs, and changes of direction.',
    equipment: ['Cable machine with a low pulley', 'Ankle cuff'],
    setup: [
      'Set the pulley at its lowest point and attach an ankle cuff.',
      'Stand side on to the machine and strap the cuff to the ankle furthest from it.',
      'Hold the machine with your near hand and stand tall on the leg closest to it, knee soft.',
      'Step away until the cable is tight with your working foot just off the floor.',
    ],
    steps: [
      'Start with your working foot beside or just in front of your standing foot, toes pointing forward.',
      'Lift the working leg out to the side, keeping it straight and leading with the heel.',
      'Stop before your trunk starts to lean or your hip hikes up.',
      'Pause briefly at the top.',
      'Return slowly to the start without letting the weight stack touch down.',
      'Finish all reps on one side, then switch sides and match the reps.',
    ],
    breathing: 'Breathe steadily. Breathe out as you lift the leg and in as you return it.',
    tempo:
      '2 1 1 1 means two seconds to bring the leg back in, a one second pause at the start, one second to lift it out, and a one second hold at the top.',
    rangeOfMotion:
      'Lift the leg out to about 30 to 40 degrees, or as far as you can with your trunk upright and toes pointing forward. The side of the hip should do the work, not a lean of the body.',
    muscles: {
      primary: ['glute_med'],
      secondary: [],
    },
    emphasisNote:
      'The gluteus medius and minimus do most of the work, helped by the tensor fasciae latae at the front of the hip and the upper fibres of the glute max. Keeping your toes forward and the leg slightly behind your body biases the gluteus medius. Turning the toes out or swinging the leg forward lets the tensor fasciae latae and hip flexors take a larger share.',
    movementPattern: 'hip_abduction',
    joints: ['Hip'],
    laterality: 'unilateral',
    logSides: true,
    fatigueOverlap: ['hip'],
    commonMistakes: [
      'Leaning the trunk away from the machine to swing the leg higher.',
      'Turning the toes out so the front of the hip takes over.',
      'Hiking the hip up instead of moving the leg out.',
      'Letting the cable snap the leg back in.',
    ],
    goodFormFeels:
      'A burning effort high on the side of your working hip, just below the top of the pelvis, while your trunk stays still. Your standing hip also works to keep you level.',
    stopRules: [
      'End the set when your trunk starts to lean, your toes turn out, or the range gets shorter.',
      EFFORT_RULE.all,
      PAIN_RULE,
    ],
    safetyNotes: ['Hold the machine for balance and check that the cuff is fastened securely before each set.'],
    easierSubstitution: {
      exerciseId: null,
      name: 'Side lying hip abduction',
      reason: 'Bodyweight only, lying on your side and lifting the top leg. Easy to learn and control.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Seated hip abduction machine',
      reason: 'Trains both sides at once when the cable is busy. Leaning slightly forward brings in more of the glutes.',
    },
    otherSubstitutions: [
      {
        exerciseId: null,
        name: 'Banded lateral walk',
        reason: 'Needs only a mini band above the knees. Useful at home or in a warm up.',
      },
    ],
    loadIncrement: 'lower',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Front view. Stand tall beside the low pulley, cuff on the outside ankle, hand on the machine.',
          trunk: 180,
          armNear: [41.3, 96.1],
          armFar: [-35, 45],
          legNear: [0, 0, 90],
          legFar: [-5, -5, -95],
          footX: 130,
          props: [
            { type: 'line', x1: 178, y1: 20, x2: 178, y2: 172 },
            { type: 'cable', from: [122.9, 170], to: [174, 166] },
          ],
        },
        {
          label: 'Out',
          caption: 'Lift the working leg out to the side with toes forward. Trunk stays upright.',
          trunk: 180,
          armNear: [41.3, 96.1],
          armFar: [-35, 45],
          legNear: [0, 0, 90],
          legFar: [-32, -32, -80],
          footX: 130,
          props: [
            { type: 'line', x1: 178, y1: 20, x2: 178, y2: 172 },
            { type: 'cable', from: [86.5, 159.5], to: [174, 166] },
            { type: 'arrow', from: [118, 150], to: [92, 136] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Bring the leg back in slowly without letting the weight touch down.',
          trunk: 180,
          armNear: [41.3, 96.1],
          armFar: [-35, 45],
          legNear: [0, 0, 90],
          legFar: [-5, -5, -95],
          footX: 130,
          props: [
            { type: 'line', x1: 178, y1: 20, x2: 178, y2: 172 },
            { type: 'cable', from: [122.9, 170], to: [174, 166] },
            { type: 'arrow', from: [92, 136], to: [118, 150] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Seated Calf Raise
  {
    id: 'seated-calf-raise',
    name: 'Seated Calf Raise',
    aliases: ['Seated calf raise machine'],
    kind: 'strength',
    purpose:
      'Strengthens the soleus, the deep calf muscle that handles large forces in running and jumping and supports the Achilles tendon.',
    equipment: ['Seated calf raise machine'],
    setup: [
      'Sit on the seat and place the balls of your feet on the edge of the foot plate, about hip width apart.',
      'Adjust the knee pad so it presses firmly on your thighs just above the knees.',
      'Lift your heels slightly and release the safety lever.',
      'Keep your toes pointing forward and your knees bent at about a right angle.',
    ],
    steps: [
      'Lower your heels slowly until you feel a deep stretch low in your calves.',
      'Pause in the stretch without bouncing.',
      'Push through the balls of your feet to raise your heels as high as you can.',
      'Hold the top briefly with your ankles steady.',
      'After the last rep, raise your heels and put the safety lever back before you get up.',
    ],
    breathing: 'Breathe steadily. Breathe out as you rise and in as you lower.',
    tempo:
      '2 1 1 1 means two seconds to lower the heels, a one second pause in the stretch, one second to rise, and a one second hold at the top.',
    rangeOfMotion: 'Use the full range, from a deep stretch at the bottom to as high on your toes as you can go.',
    muscles: {
      primary: ['soleus'],
      secondary: ['gastrocnemius'],
    },
    emphasisNote:
      'Bending the knees slackens the gastrocnemius, so the soleus takes a larger share of the load. The gastrocnemius still contributes. Pair this with the standing calf raise to train both parts of the calf well.',
    movementPattern: 'plantar_flexion',
    joints: ['Ankle'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['achilles_calf'],
    commonMistakes: [
      'Bouncing at the bottom.',
      'Using a short range at the top or the bottom.',
      'Pushing the pad up with your hands or by rocking your body.',
      'Rolling onto the little toes.',
    ],
    goodFormFeels:
      'A deep stretch low in your calves at the bottom and a strong squeeze at the top, with the pressure through the balls of your feet.',
    stopRules: [
      'End the set when your range gets shorter or you start to bounce.',
      EFFORT_RULE.all,
      'Pain of 4 out of 10 or higher in the Achilles tendon, heel, or calf, or pain that worsens or changes your technique, pauses this exercise. Report it to a parent, coach, or clinician.',
    ],
    safetyNotes: [
      'Always put the safety lever back on before you take your feet off the plate.',
      'Heel pain is common in growing athletes who jump a lot. Report it early rather than training through it.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Bent knee calf raise on a step',
      reason: 'Bodyweight only. Stand on a step holding a rail, keep your knees slightly bent, and raise your heels.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Seated dumbbell calf raise',
      reason: 'Sit on a bench with a dumbbell resting on your thighs above the knees and your forefeet on a plate when there is no machine.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'standing-calf-raise',
        name: 'Standing Calf Raise',
        reason: 'Straight knees shift the emphasis toward the gastrocnemius.',
      },
    ],
    loadIncrement: 'lower',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Seated with the pad on your thighs and the balls of your feet on the step. Heels low in a stretch.',
          trunk: 176,
          armNear: [2, 81.3],
          legNear: [89.2, 5.5, 110],
          hip: [58, 110],
          props: [
            { type: 'bench', x: 30, y: 116, w: 52, h: 8 },
            { type: 'box', x: 108, y: 150, w: 39, h: 22 },
            { type: 'pad', x: 83.2, y: 95, w: 16, h: 9 },
            { type: 'handle', at: 'hands' },
          ],
        },
        {
          label: 'Top',
          caption: 'Push through the balls of your feet and raise your heels as high as you can.',
          trunk: 176,
          armNear: [-5.9, 98.7],
          legNear: [103.9, 8.5, 60],
          hip: [58, 110],
          props: [
            { type: 'bench', x: 30, y: 116, w: 52, h: 8 },
            { type: 'box', x: 108, y: 150, w: 39, h: 22 },
            { type: 'pad', x: 79.4, y: 86.9, w: 16, h: 9 },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [165, 120], to: [165, 98] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Lower your heels slowly back into the stretch before the next rep.',
          trunk: 176,
          armNear: [2, 81.3],
          legNear: [89.2, 5.5, 110],
          hip: [58, 110],
          props: [
            { type: 'bench', x: 30, y: 116, w: 52, h: 8 },
            { type: 'box', x: 108, y: 150, w: 39, h: 22 },
            { type: 'pad', x: 83.2, y: 95, w: 16, h: 9 },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [165, 98], to: [165, 120] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Nordic Hamstring Curl
  {
    id: 'nordic-hamstring-curl',
    name: 'Nordic Hamstring Curl',
    aliases: ['Nordic curl', 'Nordic hamstring exercise'],
    kind: 'bodyweight',
    purpose:
      'An eccentric exercise, which means your hamstrings work while they lengthen under control. This kind of strength is linked to fewer hamstring strains in sports that involve sprinting and jumping.',
    equipment: [
      'Soft mat or pad for the knees',
      'A partner to hold your ankles, or a secure anchor such as a Nordic bench or padded bar',
      'Resistance band for assisted reps while learning',
    ],
    setup: [
      'Kneel on a soft pad with your body upright from knees to head.',
      'Have a partner kneel behind you and press your ankles firmly down, or hook your heels under a secure padded anchor.',
      'Squeeze your glutes and brace your trunk so your hips stay straight.',
      'Hold your hands in front of your chest, ready to catch yourself.',
      'While you are learning, loop a band around your chest anchored high behind you, or keep your hands on a box in front of you for help.',
    ],
    steps: [
      'Lean forward slowly from the knees, keeping a straight line from knees to shoulders.',
      'Resist the fall with the back of your thighs for as long as you can control it.',
      'When you can no longer slow down, catch yourself with your hands like the bottom of a push up.',
      'Push off the floor with your hands to return upright, using your hamstrings only lightly.',
      'Reset your position and brace before the next rep.',
    ],
    breathing:
      'Breathe in and brace before you lean. Breathe out slowly as you lower. Take a full breath at the top between reps.',
    tempo:
      '4 0 1 0 means about four seconds of controlled lowering, no pause at the bottom, a one second push back up with your hands, and no rest before you reset. The slow lowering is the part that trains the hamstrings.',
    rangeOfMotion:
      'Lower only as far as you can control with a straight body, then catch yourself. As you get stronger the controlled part of the range gets longer. You do not need to reach the floor under control.',
    muscles: {
      primary: ['hamstrings'],
      secondary: [],
    },
    emphasisNote:
      'The hamstrings do the braking as they lengthen. Your glutes and trunk work to keep the hips straight, and the calves help a little at the knee. Bending at the hips shortens the lever and takes load off the hamstrings, so keep the hips straight.',
    movementPattern: 'knee_flexion',
    joints: ['Knee'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['hamstring', 'knee'],
    commonMistakes: [
      'Bending at the hips so your backside sticks out.',
      'Dropping fast in the first part of the lowering.',
      'Trying to pull back up with the hamstrings from the bottom.',
      'Kneeling on a hard floor without padding.',
      'Moving to a harder version before the current one is smooth.',
    ],
    goodFormFeels:
      'A steady, strong effort along the back of both thighs as you lean, with your body in one straight line from knees to head.',
    stopRules: [
      'End the set when you can no longer lower slowly with straight hips, or your lowering speed changes sharply.',
      EFFORT_RULE.never,
      painRule('A sharp pull or cramp in the back of the thigh counts.'),
    ],
    safetyNotes: [
      'Difficulty never increases automatically. Move to a harder version, such as less band help, only when a coach agrees and every rep of the current version is controlled.',
      'Always use a partner or a secure anchor. Never hook your feet under furniture that could tip.',
      'Expect sore hamstrings for a few days after the first sessions. Keep to the low volume in the plan.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Band assisted Nordic hamstring curl',
      reason: 'A band around your chest, anchored high behind you, takes part of your weight so you can control a longer range.',
    },
    equipmentSubstitution: {
      exerciseId: 'seated-leg-curl',
      name: 'Seated Leg Curl',
      reason: 'Use it when you have no partner or anchor. Lower the weight slowly to keep an eccentric focus.',
    },
    otherSubstitutions: [
      {
        exerciseId: null,
        name: 'Hand assisted Nordic hamstring curl',
        reason: 'Push lightly against a box or the floor with your hands through the whole lowering to reduce the load.',
      },
    ],
    loadIncrement: 'none',
    failure: 'never',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Kneel tall on a pad with your ankles held down. Straight line from knees to head.',
          trunk: 180,
          armNear: [20, 150],
          legNear: [0, -90, -95],
          hip: [68, 118],
          props: [
            { type: 'box', x: 8, y: 165, w: 74, h: 7 },
            { type: 'pad', x: 20, y: 146, w: 15, h: 9 },
          ],
        },
        {
          label: 'Lowering',
          caption: 'Lean forward slowly from the knees. Hips stay straight while the hamstrings brake.',
          trunk: 145,
          armNear: [20, 110],
          legNear: [-35, -90, -95],
          hip: [92.1, 125.6],
          props: [
            { type: 'box', x: 8, y: 165, w: 74, h: 7 },
            { type: 'pad', x: 20, y: 146, w: 15, h: 9 },
            { type: 'arrow', from: [128, 50], to: [158, 72] },
          ],
        },
        {
          label: 'Finish',
          caption: 'Catch yourself with your hands, then push back up to the start.',
          trunk: 108,
          armNear: [-33.5, 64.2],
          legNear: [-72, -90, -95],
          hip: [107.9, 147],
          props: [
            { type: 'box', x: 8, y: 165, w: 74, h: 7 },
            { type: 'pad', x: 20, y: 146, w: 15, h: 9 },
            { type: 'arrow', from: [150, 100], to: [120, 78] },
          ],
        },
      ],
    },
  },
];
