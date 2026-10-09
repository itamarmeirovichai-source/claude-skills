import { PAIN_RULE, QUALITY_RULE } from './effort';
import type { ExerciseContent } from '../types';

// Home drills added in 3.0.0. Home sessions hold the jump, landing, footwork, and volleyball skill
// work, so they must also work in a small room, under a normal ceiling, and without noise or a ball.
// Order matches HOME_IDS in ids.ts.

export const HOME_EXERCISES: ExerciseContent[] = [
  // ---------------------------------------------------------------- Home Movement Prep
  {
    id: 'home-movement-prep',
    name: 'Home Movement Prep',
    aliases: ['Small space warm up', 'Home warm up'],
    kind: 'warmup',
    purpose:
      'Warms up the legs, hips, ankles, and trunk in a space of about two by two metres, before landings, hops, footwork, or arm swing practice at home. It also lets you notice any knee, heel, back, or wrist pain before harder work.',
    equipment: ['About 2 by 2 metres of clear floor', 'Supportive trainers', 'Optional mat'],
    setup: [
      'Clear the floor of bags, cables, and furniture edges, and check nobody is standing close by.',
      'Wear the trainers you will jump in, laces tied.',
      'Plan about 10 minutes, starting easy. The landing, balance, and trunk parts are the injury prevention part: keep them even on a short day.',
    ],
    steps: [
      'March in place, 1 minute, lifting the knees to hip height and swinging the arms.',
      'Jog in place on the balls of the feet, 1 minute, staying quiet.',
      'Leg swings, 1 minute. Hold a wall or a chair and swing each leg 10 times front to back and 10 times side to side.',
      'Walking or stationary lunges with an overhead reach, 5 on each leg.',
      'Ankle rocks, 10 on each side. Put one foot forward, push the knee over the toes and back without lifting the heel.',
      'Glute bridges, 10 slow reps lying on your back, squeezing the glutes at the top.',
      'Side plank, 20 seconds on each side, with the body in a straight line from head to feet.',
      'Single leg balance, 20 seconds on each leg, with a soft knee kept over the middle of the foot.',
      'Drop and freeze, 5 reps: from standing tall, drop quickly into a quarter squat as if landing, both feet flat, knees over the toes, and hold for 2 seconds.',
      'Small calf bounces in place, 2 sets of 10, getting a little quicker, only if hops are in today\'s plan.',
    ],
    breathing: 'Breathe easily the whole time. You should be able to talk. Breathing picks up a little by the end.',
    tempo: 'Easy at first and brisk by the end, about 10 minutes in total. Nothing should feel hard.',
    rangeOfMotion:
      'Start with small, comfortable ranges and let each swing, lunge, and ankle rock grow a little until you reach your normal full range. Never force a stretch.',
    muscles: {
      primary: ['glute_max', 'quads'],
      secondary: ['hamstrings', 'glute_med', 'hip_flexors', 'gastrocnemius', 'soleus', 'tibialis_anterior', 'obliques_core'],
    },
    emphasisNote:
      'Preparation, not training volume. The hips, thighs, and calves warm up the most. It is counted as activity time, not as muscle building sets.',
    movementPattern: 'general_preparation',
    joints: ['Ankle', 'Knee', 'Hip', 'Spine'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['systemic'],
    commonMistakes: [
      'Skipping it because the jump session is short.',
      'Rushing straight into hops while the calves are still cold.',
      'Turning the warm up into a workout that leaves you tired.',
      'Holding long static stretches instead of moving.',
    ],
    goodFormFeels: 'Warm, loose, and a little out of breath, with springy ankles and no pain anywhere.',
    stopRules: [
      'Stop and skip today\'s jumps if a knee, heel, shin, back, or wrist hurts during the warm up.',
      PAIN_RULE,
    ],
    safetyNotes: [
      'Two metres of clear floor is enough for this warm up. Bigger drills need more room, and PeakForm only plans the ones your home space allows.',
      'Use a wall or a sturdy chair for balance, never a door or anything that can roll.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Five minutes of easy walking and marching',
      reason: 'Enough to warm up for footwork practice without hops.',
    },
    equipmentSubstitution: {
      exerciseId: 'dynamic-volleyball-warm-up',
      name: 'Dynamic Volleyball Warm Up',
      reason: 'The fuller version, when you have half a court or a yard.',
    },
    loadIncrement: 'none',
    visual: {
      poses: [
        {
          label: 'March',
          caption: 'March in place: knee to hip height, opposite arm forward.',
          trunk: 180,
          armNear: [-30, -10],
          armFar: [40, 80],
          legNear: [90, 0, 80],
          legFar: [0, 0, 90],
        },
        {
          label: 'Lunge reach',
          caption: 'Step into a lunge and reach both arms overhead. Front knee over the toes.',
          trunk: 178,
          armNear: [175, 178],
          armFar: [172, 176],
          legNear: [70, -5, 80],
          legFar: [-25, -95, -60],
        },
        {
          label: 'Ankle rock',
          caption: 'Push the front knee over the toes and back, heel down.',
          trunk: 172,
          armNear: [20, 60],
          legNear: [40, 20, 90],
          legFar: [-10, -20, 75],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Lateral Line Hop
  {
    id: 'lateral-line-hop',
    name: 'Lateral Line Hop',
    aliases: ['Side to side line hop', 'Low lateral hop'],
    kind: 'jump',
    purpose:
      'Low, quick hops side to side over a line on the floor. They train quick, controlled ankles and steady knees when you move sideways, as you do when you block or cover in volleyball, with small landings that fit under a normal ceiling.',
    equipment: ['A line of tape on the floor, or a rope laid flat', 'About 1.5 by 1.5 metres of clear floor', 'Supportive trainers'],
    setup: [
      'Lay a strip of tape or a rope flat on a floor that is not slippery.',
      'Stand beside the line with your feet about hip width apart.',
      'Bend the knees slightly and keep your weight on the balls of the feet.',
    ],
    steps: [
      'Hop sideways over the line with both feet, only a few centimetres off the floor.',
      'Land quietly on the balls of the feet with the knees over the toes, not caving in.',
      'Hop straight back over the line.',
      'Keep the trunk upright and the eyes forward while the feet do the work.',
      'Each landing counts as one contact. Stop at the planned number or earlier if the landings get loud.',
    ],
    breathing: 'Breathe in a short, relaxed rhythm. Do not hold your breath.',
    tempo: 'Quick but controlled, about two hops per second. Rest 60 seconds between sets.',
    rangeOfMotion: 'Small: about 30 centimetres sideways and a few centimetres up. Knees and hips bend only a little.',
    muscles: {
      primary: ['gastrocnemius', 'soleus'],
      secondary: ['glute_med', 'quads', 'tibialis_anterior', 'adductors'],
    },
    emphasisNote:
      'The calves and ankles absorb and return each small landing, while the side of the hip keeps the knee in line. It is counted as jump contacts, not as muscle building sets.',
    movementPattern: 'jump',
    joints: ['Ankle', 'Knee', 'Hip'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['achilles_calf', 'shin'],
    commonMistakes: [
      'Hopping high instead of quick and low.',
      'Knees falling inward on the landing.',
      'Landing flat footed or loudly.',
      'Leaning the trunk from side to side.',
    ],
    goodFormFeels: 'Light and quick, with quiet landings and knees that point the same way as the toes.',
    stopRules: [
      'End the set when the landings get louder or the knees start to cave in.',
      'Stop for pain at the heel, the Achilles tendon, the shin, or below the kneecap.',
      QUALITY_RULE,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Never on tile, wet floors, or socks. A mat or a firm floor with trainers is right.',
      'Count every landing toward the day\'s jumps, together with any jumping at school or club practice.',
      'Heel or knee soreness that lasts into the next morning means fewer hops and telling a parent or coach.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Side to side step overs',
      reason: 'Step over the line instead of hopping. Same pattern, no impact, and silent.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Hops over a crack in the pavement',
      reason: 'Any flat, dry outdoor line works when there is no tape.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'pogo-hop',
        name: 'Pogo Hop',
        reason: 'The same quick ankle contacts in place, without the sideways move.',
      },
    ],
    loadIncrement: 'none',
    visual: {
      diagram: {
        kind: 'lane',
        caption: 'From above: hop over the line and back. Each landing is one contact. Keep the hops low and quiet.',
        steps: [
          { x: 2, y: 0.4, label: '1' },
          { x: 2, y: -0.4, label: '2' },
          { x: 2, y: 0.4, label: '3' },
          { x: 2, y: -0.4, label: '4' },
        ],
        markers: [
          { x: 1, y: 0, label: 'Line' },
          { x: 3, y: 0, label: 'Line' },
        ],
      },
    },
  },

  // ---------------------------------------------------------------- Spike Arm Swing Shadow
  {
    id: 'spike-arm-swing-shadow',
    name: 'Spike Arm Swing, No Ball',
    aliases: ['Shadow arm swing', 'Bow and arrow drill'],
    kind: 'skill',
    purpose:
      'Practises the order of the spike arm swing slowly, with no ball and no jump: both arms back on the last steps, both up, the bow and arrow draw, and a relaxed reach to a high contact point. It builds timing and technique without any impact on the wrist or shoulder.',
    equipment: ['Space to swing both arms fully, about 2 by 2 metres', 'A ceiling high enough to reach up without touching, or outdoors'],
    setup: [
      'Stand with your feet in the approach plant position: right foot slightly behind the left for right handers. Left handers mirror this.',
      'Check that nothing is within reach of your arms in any direction.',
      'Start slowly. Speed is not the goal.',
    ],
    steps: [
      'Swing both arms back behind the hips as if you were taking the last two approach steps.',
      'Bring both arms forward and up together until they are above the shoulders.',
      'Pull the hitting elbow back and up to about ear height, like drawing a bow, while the other hand points up at an imaginary ball.',
      'Bring the non hitting arm down to the chest as the hitting shoulder turns forward.',
      'Reach up with the hitting arm, nearly straight, to a contact point in front of the hitting shoulder, with a loose hand.',
      'Let the arm finish across the body, relaxed. Reset and repeat.',
    ],
    breathing: 'Breathe out softly as the arm reaches up. Breathe normally between reps.',
    tempo: 'Slow walk throughs first, then about three quarter speed. Rest about 30 seconds between sets.',
    rangeOfMotion: 'Full, comfortable range at the shoulder. Never force the arm behind you or snap the elbow straight.',
    muscles: {
      primary: ['delt_anterior', 'pec_clavicular'],
      secondary: ['lats', 'triceps', 'obliques_core', 'rotator_cuff', 'serratus_anterior'],
    },
    emphasisNote:
      'This is technique practice. The shoulder and trunk muscles work lightly in the right order. It is counted as skill practice, not as muscle building sets.',
    movementPattern: 'overhead_strike',
    joints: ['Shoulder', 'Elbow', 'Spine'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder'],
    commonMistakes: [
      'Leaving the arms in front of the body instead of swinging them back.',
      'Dropping the hitting elbow below the shoulder.',
      'Swinging with only the arm instead of turning the trunk.',
      'Rushing. Fast swings with poor order teach the wrong pattern.',
    ],
    goodFormFeels: 'Smooth and relaxed, arms back, both up, a high elbow, then a long reach. The shoulder feels loose, never pinched.',
    stopRules: [
      'Stop if the shoulder pinches, clicks with pain, or feels unstable.',
      'Stop when the order gets sloppy, rest, then restart slowly.',
      PAIN_RULE,
    ],
    safetyNotes: [
      'No ball, no jump, no impact, so it is suitable while a wrist injury is still being checked. Stop if the wrist hurts anyway.',
      'Check the ceiling, lights, and fans before reaching up indoors.',
      'A coach can check your arm swing from a short phone video. Film it only with permission from anyone else in view.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Arm swing only, no bow and arrow',
      reason: 'Practise just the back and up arm swing of the approach first.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Arm swing outdoors',
      reason: 'Outdoors there is no ceiling to worry about.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'volleyball-approach-footwork',
        name: 'Volleyball Approach Footwork',
        reason: 'Combine the arm swing with the approach steps once both are smooth on their own.',
      },
    ],
    loadIncrement: 'none',
    visual: {
      poses: [
        {
          label: 'Arms back',
          caption: 'Both arms swing back behind the hips, as on the last approach steps.',
          trunk: 160,
          armNear: [-50, -40],
          armFar: [-45, -35],
          legNear: [30, -10, 80],
          legFar: [10, -30, 70],
        },
        {
          label: 'Draw',
          caption: 'Both arms up, then the hitting elbow pulls back to ear height like drawing a bow.',
          trunk: 178,
          armNear: [-160, 120],
          armFar: [160, 170],
          legNear: [5, -5, 85],
          legFar: [5, -5, 85],
        },
        {
          label: 'Reach',
          caption: 'Turn the trunk and reach up with a nearly straight arm to a high contact point in front.',
          trunk: 182,
          armNear: [165, 170],
          armFar: [40, 100],
          legNear: [5, -5, 85],
          legFar: [5, -5, 85],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Wall Spike Control
  {
    id: 'wall-spike-control',
    name: 'Wall Spike Control',
    aliases: ['Wall hits', 'Controlled down balls against a wall'],
    kind: 'skill',
    purpose:
      'Light, controlled hits of a volleyball down at the floor so it bounces up off a wall and back to you. It trains contact on the heel of the hand, wrist snap, arm swing timing, and accuracy at a target, at a fraction of spike effort. It is planned only after a clinician has cleared the wrist.',
    equipment: ['A volleyball', 'A solid outside wall or a court wall with no windows nearby', 'About 4 by 3 metres of clear space'],
    setup: [
      'Stand about 3 metres from a solid wall, never one with windows, pictures, or anything breakable.',
      'Make sure nobody is between you and the wall, and that the ball cannot roll into a road.',
      'Mark a target spot on the floor about 1 metre in front of the wall with tape or chalk.',
      'Start with soft hits at about half effort.',
    ],
    steps: [
      'Toss the ball a little in front of your hitting shoulder.',
      'Draw the hitting arm back with a high elbow, as in the arm swing drill.',
      'Hit the top back of the ball with an open hand, heel of the hand first, fingers spread and relaxed.',
      'Aim at the floor target so the ball bounces into the wall and back to you.',
      'Catch the ball, reset, and repeat. Count the hits that land on target.',
    ],
    breathing: 'Breathe out as you hit. Breathe normally while you reset.',
    tempo: 'One controlled hit, then catch and reset. About half effort. Rest 30 to 60 seconds between sets.',
    rangeOfMotion: 'A full but relaxed arm swing with a short wrist snap at contact. Never swing hard enough to lose control.',
    muscles: {
      primary: ['delt_anterior', 'pec_clavicular'],
      secondary: ['lats', 'triceps', 'forearm_flexors', 'rotator_cuff', 'obliques_core'],
    },
    emphasisNote:
      'This is skill practice for contact and accuracy. The shoulder, chest, and forearm work lightly. It is counted as skill practice, not as muscle building sets.',
    movementPattern: 'overhead_strike',
    joints: ['Shoulder', 'Elbow', 'Wrist'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder', 'wrist_grip'],
    commonMistakes: [
      'Hitting hard. Control and accuracy are the point.',
      'Contacting the ball with a stiff, flat hand or the fingertips instead of the heel of the hand.',
      'Letting the elbow drop below the shoulder.',
      'Standing so close to the wall that the ball comes back too fast to control.',
    ],
    goodFormFeels: 'A clean slap sound, topspin on the ball, and a relaxed arm. Most hits land on or near the target.',
    stopRules: [
      'Stop at once for any wrist pain, or if the wrist feels weak or unstable.',
      'Stop if the shoulder pinches or aches, or when control drops.',
      PAIN_RULE,
    ],
    safetyNotes: [
      'Only after a clinician has confirmed that the wrist is cleared for ball contact. Until then PeakForm plans the no ball arm swing instead.',
      'Never indoors near windows, lights, screens, or people. Outdoors against a solid wall, or on a court, is right.',
      'Keep it at half effort. Hard spikes are for court practice with a coach.',
    ],
    easierSubstitution: {
      exerciseId: 'spike-arm-swing-shadow',
      name: 'Spike Arm Swing, No Ball',
      reason: 'The same arm swing with no ball and no impact on the wrist.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Self toss and catch',
      reason: 'Toss and catch at the contact point with both hands to practise timing without hitting.',
    },
    loadIncrement: 'none',
    visual: {
      poses: [
        {
          label: 'Toss and draw',
          caption: 'Toss slightly in front of the hitting shoulder and draw the elbow back high.',
          trunk: 178,
          armNear: [-160, 120],
          armFar: [165, 175],
          legNear: [10, -5, 85],
          legFar: [-5, -10, 80],
          props: [{ type: 'ball', at: [128, 22], r: 7 }],
        },
        {
          label: 'Contact',
          caption: 'Heel of the hand on the top back of the ball, then a short wrist snap toward the floor target.',
          trunk: 182,
          armNear: [160, 140],
          armFar: [40, 100],
          legNear: [10, -5, 85],
          legFar: [-5, -10, 80],
          props: [
            { type: 'ball', at: 'nearHand', r: 7 },
            { type: 'arrow', from: [150, 40], to: [178, 150] },
          ],
        },
      ],
    },
  },
];
