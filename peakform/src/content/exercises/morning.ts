import type { ExerciseContent } from '../types';

// Morning volleyball work for home: no ball, no net, and only light dumbbells and a rope.
// Order matches MORNING_IDS in ids.ts. These build movement patterns and resilient
// shoulders, trunk, and ankles. Muscle growth still comes from the main sessions.

export const MORNING_EXERCISES: ExerciseContent[] = [
  // ---------------------------------------------------------------- Shadow Passing Footwork
  {
    id: 'shadow-pass-footwork',
    name: 'Shadow Passing Footwork',
    aliases: ['Passing footwork without a ball', 'Serve receive shadow drill'],
    kind: 'skill',
    purpose:
      'Practises the ready position and the quick shuffle to get your body behind a ball before you pass it, so on court you arrive early, balanced, and square to the target.',
    equipment: ['About 3 by 3 metres of floor', 'Optional tape or two socks as markers'],
    setup: [
      'Mark a centre spot and pick a "target" on a wall, where the setter would stand.',
      'Stand on the centre spot in the ready position: feet a bit wider than the shoulders, knees bent, weight on the balls of the feet, arms relaxed in front.',
      'Decide the order of directions before each set, for example left, right, forward, back.',
    ],
    steps: [
      'From the ready position, take one or two quick shuffle steps in the chosen direction. Do not cross the feet.',
      'Stop with the feet wide and the hips low, facing the target.',
      'Form the passing platform: hands together, thumbs side by side, elbows straight, forearms flat and angled toward the target.',
      'Hold the platform for one second with a still trunk, as if the ball is arriving.',
      'Shuffle back to the centre spot and reset the ready position before the next direction.',
      'Keep going for the whole work interval, calm and exact rather than fast.',
    ],
    breathing: 'Breathe out as you stop and form the platform, breathe in as you shuffle back.',
    tempo: 'Quick feet, then a clear stop. About one direction every 2 to 3 seconds.',
    rangeOfMotion:
      'Short steps, one to two metres. The hips stay low the whole time, about a quarter squat, and the head stays level.',
    muscles: {
      primary: ['quads', 'glute_med'],
      secondary: ['adductors', 'glute_max', 'gastrocnemius', 'obliques_core'],
    },
    emphasisNote:
      'Coordination practice. The thighs and the side of the hips hold the low stance, and the calves drive the quick steps. It is light work, not muscle building.',
    movementPattern: 'change_of_direction',
    joints: ['Ankle', 'Knee', 'Hip'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['knee', 'achilles_calf'],
    commonMistakes: [
      'Reaching with the arms instead of moving the feet.',
      'Standing up tall between directions, which makes you late on court.',
      'Crossing the feet during the shuffle.',
      'Swinging the platform instead of holding it still and angled at the target.',
      'Going fast and sloppy instead of exact.',
    ],
    goodFormFeels:
      'Light, quiet feet, a low steady head, and a platform that stops still and points at the target every time.',
    stopRules: [
      'Stop when the stops become sloppy or you start standing up between reps. Rest, then restart slower.',
      'Stop for pain of 4 out of 10 or more, or pain that worsens or changes how you move, and tell a parent, coach, or clinician.',
    ],
    safetyNotes: [
      'Clear the floor of anything you could step on, and use shoes or a floor that does not slip.',
      'Early in the morning, start slowly for the first minute until the body feels warm.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Ready position holds',
      reason: 'Hold the low ready stance for 20 seconds, then form the platform, with no steps.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Partner pointing drill',
      reason: 'A parent or sibling points a direction and you react, still without a ball.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'volleyball-approach-footwork',
        name: 'Volleyball Approach Footwork',
        reason: 'Another footwork pattern for the same session when you have more space.',
      },
    ],
    loadIncrement: 'none',
    visual: {
      diagram: {
        kind: 'court',
        caption: 'C is the centre spot. Shuffle to L, stop low and form the platform facing the target, shuffle back to C, then R, then F.',
        steps: [
          { x: 2.2, y: 6.2, label: 'L' },
          { x: 4.5, y: 6.2, label: 'C' },
          { x: 6.8, y: 6.2, label: 'R' },
          { x: 4.5, y: 4.4, label: 'F' },
        ],
        markers: [{ x: 6.5, y: 1.2, label: 'Target' }],
      },
    },
  },

  // ---------------------------------------------------------------- Blocking Footwork, No Jump
  {
    id: 'block-footwork',
    name: 'Blocking Footwork, No Jump',
    aliases: ['Block slide and crossover steps', 'Shadow block footwork'],
    kind: 'skill',
    purpose:
      'Grooves the slide step and crossover step a blocker uses to move along the net, and ends each rep in a balanced, square block position, without the landing load of repeated jumps.',
    equipment: ['About 4 metres of clear floor along a wall', 'Optional tape to mark the "antennas"'],
    setup: [
      'Stand facing a wall about half a metre away, as if the wall is the net.',
      'Hands up at forehead height, palms toward the wall, elbows in front of the body.',
      'Mark a spot about 2 metres to each side for the short and long moves.',
    ],
    steps: [
      'Slide step, short move: step sideways with the lead foot, bring the other foot next to it, and stop square to the wall with the hands up.',
      'Crossover, long move: turn the hips, run a crossover step with the back foot, then plant both feet square to the wall.',
      'At each stop, press the hands up and slightly forward over the "net" and hold for one second. No jump.',
      'Return with the same footwork to the middle, then go to the other side.',
      'After a few clean reps, you may add a small hop of a few centimetres at the stop, landing softly.',
    ],
    breathing: 'Breathe out as you press the hands up at the stop.',
    tempo: 'Quick feet, then a still stop of one second. Walk back if you need to reset.',
    rangeOfMotion:
      'Moves of one to three metres. The shoulders stay square to the wall at every stop, and the hands never drop below the forehead.',
    muscles: {
      primary: ['glute_med', 'adductors'],
      secondary: ['quads', 'gastrocnemius', 'soleus', 'delt_anterior', 'obliques_core'],
    },
    emphasisNote:
      'Coordination practice. The side of the hips and the inner thighs control the side steps, and the shoulders hold the hands up. Light work that saves your legs for the main session.',
    movementPattern: 'change_of_direction',
    joints: ['Ankle', 'Knee', 'Hip', 'Shoulder'],
    laterality: 'alternating',
    logSides: false,
    fatigueOverlap: ['knee', 'achilles_calf'],
    commonMistakes: [
      'Letting the hands drop while moving, so they arrive late at the net.',
      'Stopping with the shoulders turned instead of square to the net.',
      'Crossing the feet on a short move, or shuffling on a long move.',
      'Drifting toward the wall, which would mean touching the net on court.',
    ],
    goodFormFeels: 'Quiet feet, hands that stay high, and a square, balanced stop you could jump from.',
    stopRules: [
      'Stop when the stops drift or the hands start to drop. Rest, then restart slowly.',
      'Stop for pain of 4 out of 10 or more, or pain that worsens or changes how you move, and tell a parent, coach, or clinician.',
    ],
    safetyNotes: [
      'Keep the optional hops tiny and soft. The big block jumps belong in the main session.',
      'Clear the floor and use a surface that does not slip.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Slide steps only',
      reason: 'Practise only the short slide step until the stop is square and still.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Doorway net',
      reason: 'Use a doorway or a line on the floor when there is no free wall.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'lateral-block-jump',
        name: 'Lateral Block Jump',
        reason: 'The jumping version, for the main session on the court.',
      },
    ],
    loadIncrement: 'none',
    visual: {
      diagram: {
        kind: 'court',
        caption: 'M is the middle. Slide step to S and stop square with the hands up, return to M, then crossover to C at the far side. No jump.',
        steps: [
          { x: 2.6, y: 1.0, label: 'S' },
          { x: 4.5, y: 1.0, label: 'M' },
          { x: 7.4, y: 1.0, label: 'C' },
        ],
        markers: [
          { x: 0.6, y: 4.6, label: 'Antenna' },
          { x: 8.4, y: 4.6, label: 'Antenna' },
        ],
      },
    },
  },

  // ---------------------------------------------------------------- Bent Over Dumbbell Y Raise
  {
    id: 'dumbbell-y-raise',
    name: 'Bent Over Dumbbell Y Raise',
    aliases: ['Y raise', 'Prone Y with dumbbells'],
    kind: 'strength',
    purpose:
      'Strengthens the lower trapezius and the back of the shoulder, which keep the shoulder blade moving well when you spike and serve many times a week.',
    equipment: ['Two light dumbbells, usually 1 to 3 kg each'],
    setup: [
      'Hold a light dumbbell in each hand with the thumbs pointing up.',
      'Soft knees, then hinge at the hips until the trunk is about 45 degrees to the floor, back flat.',
      'Let the arms hang straight down under the shoulders.',
    ],
    steps: [
      'Set the shoulder blades slightly down and back.',
      'Raise both arms forward and up at an angle, in the shape of a Y, thumbs up, elbows almost straight.',
      'Stop when the arms are in line with your ears or just below, without shrugging.',
      'Pause for one second at the top.',
      'Lower slowly for about three seconds and repeat.',
    ],
    breathing: 'Breathe out as the arms rise, breathe in as they lower.',
    tempo: 'One second up, one second pause, three seconds down.',
    rangeOfMotion:
      'From hanging under the shoulders to in line with the trunk in a Y. Stop earlier if the lower back arches or the shoulders shrug.',
    muscles: {
      primary: ['traps_lower', 'delt_posterior'],
      secondary: ['traps_middle', 'rhomboids', 'rotator_cuff', 'erectors'],
    },
    emphasisNote:
      'The lower trapezius and rear shoulder do most of the work, with the rotator cuff and mid back helping. The back muscles hold the hinge. Light weights are normal here.',
    movementPattern: 'shoulder_abduction',
    joints: ['Shoulder', 'Shoulder blade'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder', 'low_back'],
    commonMistakes: [
      'Using weights that are too heavy, so the shoulders shrug up to the ears.',
      'Swinging the trunk up to lift the arms.',
      'Rounding the back in the hinge.',
      'Bending the elbows into a row.',
    ],
    goodFormFeels:
      'A warm, working feeling low between the shoulder blades and at the back of the shoulders, with the neck relaxed.',
    stopRules: [
      'Stop the set when you cannot keep the shoulders down or the trunk still, or you reach the prescribed reps in reserve. This exercise is never taken to failure.',
      'Stop for pain of 4 out of 10 or more, pinching at the front of the shoulder, or pain that changes your form, and tell a parent, coach, or clinician.',
    ],
    safetyNotes: [
      'Start with the lightest dumbbells you have. Water bottles also work.',
      'If the lower back feels tired, rest the forehead on a table edge or do the chest supported version.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Chest supported Y raise on a bench or bed edge',
      reason: 'Support takes the lower back out of it, so the shoulders get all the attention.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Band Y raise',
      reason: 'A light resistance band gives the same shape when there are no dumbbells.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'face-pull',
        name: 'Face Pull',
        reason: 'Trains the rear shoulder and mid back with a cable in the gym.',
      },
    ],
    loadIncrement: 'upper',
    failure: 'never',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Hinge to about 45 degrees with a flat back. Arms hang under the shoulders, thumbs up.',
          trunk: 128,
          head: 118,
          armNear: [2, 2],
          legNear: [18, -4],
          props: [{ type: 'dumbbell', at: 'hands' }],
        },
        {
          label: 'Top',
          caption: 'Raise the arms up and forward in a Y, in line with the trunk, without shrugging. Pause for one second.',
          trunk: 128,
          head: 118,
          armNear: [125, 125],
          legNear: [18, -4],
          props: [
            { type: 'dumbbell', at: 'hands' },
            { type: 'arrow', from: [140, 110], to: [150, 60] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Side Lying Dumbbell External Rotation
  {
    id: 'side-lying-external-rotation',
    name: 'Side Lying Dumbbell External Rotation',
    aliases: ['Side lying ER', 'Rotator cuff external rotation'],
    kind: 'strength',
    purpose:
      'Strengthens the rotator cuff muscles that slow the arm down after a spike or serve, one of the most useful habits for healthy volleyball shoulders.',
    equipment: ['One light dumbbell, usually 1 to 2 kg', 'A folded towel', 'Floor or bed'],
    setup: [
      'Lie on your side with the working arm on top. Rest your head on the lower arm or a pillow.',
      'Put a folded towel between the top elbow and your side.',
      'Bend the top elbow to 90 degrees with the dumbbell resting in front of your belly.',
    ],
    steps: [
      'Keep the elbow pressed lightly into the towel.',
      'Rotate the forearm up toward the ceiling, like a door opening, as far as you can without the elbow lifting.',
      'Pause for one second at the top.',
      'Lower slowly for about three seconds back to the belly.',
      'Finish all reps, then roll over and do the other side.',
    ],
    breathing: 'Breathe out as the dumbbell rises, breathe in as it lowers.',
    tempo: 'One second up, one second pause, three seconds down.',
    rangeOfMotion:
      'From the forearm resting across the belly to pointing up or slightly back, while the elbow stays on the towel.',
    muscles: {
      primary: ['rotator_cuff'],
      secondary: ['delt_posterior'],
    },
    emphasisNote:
      'The rotator cuff at the back of the shoulder does the work, with the rear shoulder helping. Heavy weights make other muscles take over, so keep it light.',
    movementPattern: 'shoulder_external_rotation',
    joints: ['Shoulder'],
    laterality: 'unilateral',
    logSides: true,
    fatigueOverlap: ['shoulder'],
    commonMistakes: [
      'Lifting the elbow away from the towel to get more range.',
      'Rolling the body backward to help the arm.',
      'Dropping the weight quickly instead of lowering it slowly.',
      'Using a dumbbell that is too heavy.',
    ],
    goodFormFeels: 'A focused, warm feeling at the back of the shoulder, with the elbow still and the neck relaxed.',
    stopRules: [
      'Stop the set when the elbow starts to lift or the body rolls, or you reach the prescribed reps in reserve. This exercise is never taken to failure.',
      'Stop for pain of 4 out of 10 or more, clicking with pain, or pain that changes your form, and tell a parent, coach, or clinician.',
    ],
    safetyNotes: ['Light is right. A full water bottle is often enough at the start.'],
    easierSubstitution: {
      exerciseId: null,
      name: 'No weight external rotation',
      reason: 'The same movement with an empty hand until the elbow stays still.',
    },
    equipmentSubstitution: {
      exerciseId: 'cable-external-rotation',
      name: 'Cable External Rotation',
      reason: 'The standing cable version, for the gym.',
    },
    loadIncrement: 'upper',
    failure: 'never',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Lie on your side, elbow bent to 90 degrees on a towel, dumbbell in front of the belly.',
          trunk: 90,
          head: 90,
          armNear: [-90, 55],
          legNear: [-92, -88],
          hip: [62, 150],
          props: [{ type: 'dumbbell', at: 'hands' }],
        },
        {
          label: 'Top',
          caption: 'Rotate the forearm up toward the ceiling while the elbow stays on the towel. Lower slowly.',
          trunk: 90,
          head: 90,
          armNear: [-90, 180],
          legNear: [-92, -88],
          hip: [62, 150],
          props: [
            { type: 'dumbbell', at: 'hands' },
            { type: 'arrow', from: [118, 146], to: [118, 112] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Dead Bug
  {
    id: 'dead-bug',
    name: 'Dead Bug',
    aliases: ['Dead bug core drill'],
    kind: 'bodyweight',
    purpose:
      'Teaches the trunk to stay still while the arms and legs move, the same control you need to transfer force from the legs to the arm when you spike and block.',
    equipment: ['Floor or mat'],
    setup: [
      'Lie on your back with the arms pointing straight up to the ceiling.',
      'Lift the legs so the hips and knees are both bent to 90 degrees, shins parallel to the floor.',
      'Press the lower back gently into the floor and breathe out fully to set the ribs down.',
    ],
    steps: [
      'Slowly reach one arm back overhead and straighten the opposite leg out, keeping both a little above the floor.',
      'Keep the lower back pressed down. Only go as far as you can without it lifting.',
      'Pause for one second, then bring the arm and leg back to the start.',
      'Switch sides. One arm and leg on each side counts as one rep per side.',
    ],
    breathing: 'Breathe out slowly as the arm and leg reach away, breathe in as they return.',
    tempo: 'About three seconds out, one second pause, two seconds back.',
    rangeOfMotion:
      'The arm reaches beside the head and the leg straightens just above the floor. Shorten the reach if the lower back lifts.',
    muscles: {
      primary: ['rectus_abdominis', 'obliques_core'],
      secondary: ['hip_flexors'],
    },
    emphasisNote:
      'The front abdominal wall and the deep side of the trunk hold the lower back still. The hip flexors hold the legs up. It is about control, not burning.',
    movementPattern: 'anti_extension',
    joints: ['Spine', 'Hip', 'Shoulder'],
    laterality: 'alternating',
    logSides: false,
    fatigueOverlap: [],
    commonMistakes: [
      'The lower back arching off the floor as the leg straightens.',
      'Moving fast and bouncing between sides.',
      'Holding the breath.',
      'Lowering the leg all the way to the floor.',
    ],
    goodFormFeels: 'A steady, working trunk, lower back quietly on the floor, and slow controlled limbs.',
    stopRules: [
      'Stop the set when the lower back lifts or the movement speeds up, or you reach the prescribed reps in reserve. This exercise is never taken to failure.',
      'Stop for pain of 4 out of 10 or more, or back pain that changes your form, and tell a parent, coach, or clinician.',
    ],
    safetyNotes: ['Keep it slow. More reps with a lifting back teach the wrong habit.'],
    easierSubstitution: {
      exerciseId: null,
      name: 'Dead bug, legs only',
      reason: 'Keep the arms up and move only the legs, with the knees bent, until the back stays down.',
    },
    equipmentSubstitution: {
      exerciseId: 'pallof-press',
      name: 'Pallof Press',
      reason: 'Another trunk control drill, with a cable or band in the gym.',
    },
    loadIncrement: 'none',
    failure: 'never',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'On your back, arms up, hips and knees at 90 degrees, lower back gently on the floor.',
          trunk: 90,
          head: 90,
          armNear: [180, 180],
          legNear: [180, -90],
          hip: [80, 150],
        },
        {
          label: 'Reach',
          caption: 'Reach one arm back overhead and straighten the opposite leg just above the floor. The back stays down.',
          trunk: 90,
          head: 90,
          armNear: [95, 95],
          armFar: [180, 180],
          legNear: [180, -90],
          legFar: [-80, -85],
          hip: [80, 150],
        },
      ],
    },
  },
];
