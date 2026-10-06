import { PAIN_RULE, QUALITY_RULE } from './effort';
import type { ExerciseContent, PoseProp } from '../types';

// Jump drills, part B (added in 2.1.0; since 3.0.0 done at home where the space allows). Order matches JUMP_B_IDS in ids.ts.
// Written for a young, heavy, still growing jumper who trains alone: quality first, never to failure,
// soft landings that protect the knees and heels, and no jumps beyond the plan.

const GROUND = 172;

/** A low plyo box of about 25 to 30 cm, drawn at the same scale as the box in part A (about 0.9 px per cm). */
const DEPTH_BOX_H = 24;
const DEPTH_BOX_TOP = GROUND - DEPTH_BOX_H;
const DEPTH_BOX: PoseProp = { type: 'box', x: 8, y: DEPTH_BOX_TOP, w: 56, h: DEPTH_BOX_H };

/** A basketball rim seen from the side, near the top right: the backboard, the rim, and the net. Not to scale. */
const RIM_Y = 16;
const RIM: PoseProp[] = [
  { type: 'line', x1: 193, y1: 2, x2: 193, y2: 32 },
  { type: 'line', x1: 164, y1: RIM_Y, x2: 193, y2: RIM_Y },
  { type: 'line', x1: 166, y1: RIM_Y, x2: 171, y2: RIM_Y + 15 },
  { type: 'line', x1: 191, y1: RIM_Y, x2: 186, y2: RIM_Y + 15 },
];

export const JUMPS_B: ExerciseContent[] = [
  // ---------------------------------------------------------------- Standing Broad Jump
  {
    id: 'broad-jump',
    name: 'Standing Broad Jump',
    aliases: ['Broad jump', 'Standing long jump'],
    kind: 'jump',
    purpose:
      'Jump forward from both feet as far as you can and stick the landing. It builds hip extension power from the glutes and hamstrings and teaches you to time a full arm swing with the legs. Jumping forward does not take away from jumping up. The same hip drive lifts you off the floor in a vertical jump and in the spike approach.',
    equipment: ['A clear, flat, non slip floor with about 3 metres of free space in front', 'A line or a strip of tape to start from', 'Optional cone and tape measure to mark and measure your landing'],
    setup: [
      'Warm up fully first, including a few easy standing jumps.',
      'Stand with your toes just behind the line, feet about hip width apart.',
      'Check that the 3 metres in front of you are clear of people, weights, and benches.',
      'Wear supportive trainers with a grippy sole. Never jump in socks or on a slippery floor.',
    ],
    steps: [
      'Swing both arms back as you push the hips back and bend the knees into a quick dip.',
      'Without pausing, swing the arms forward and up hard and drive the hips forward.',
      'Push off both feet and stretch out long, forward and a little up, at about a 45 degree angle.',
      'In the air, bring the knees forward so your feet land ahead of your hips.',
      'Land softly on both feet with the hips back and the knees over the toes. Stick it and hold for two seconds.',
      'Walk back to the line and reset before the next rep.',
    ],
    breathing: 'Breathe in and brace before the dip. Breathe out as you jump or as you land. Breathe normally between reps.',
    tempo:
      'Fast dip, no pause at the bottom, explosive takeoff, then a quiet landing held for two seconds. Walk back and reset for 15 to 30 seconds between reps, and rest 60 to 120 seconds between sets.',
    rangeOfMotion:
      'Dip to about a quarter or half squat with the arms swung fully back. At takeoff, fully extend the hips, knees, and ankles. On landing, bend the hips and knees until the force is absorbed, no deeper than you can control.',
    muscles: {
      primary: ['glute_max', 'quads'],
      secondary: ['hamstrings', 'gastrocnemius', 'soleus'],
    },
    emphasisNote:
      'Driving the hips forward puts more of the work on the glutes and hamstrings than a straight up jump does, while the quads still extend the knees and the calves add the last push. The quick dip uses the stretch shortening cycle: muscles and tendons stretch, then recoil like a spring. The arm swing adds distance when it is timed with the legs. This is power work counted as jump contacts, not muscle building sets.',
    movementPattern: 'jump',
    joints: ['Hip', 'Knee', 'Ankle', 'Shoulder'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['knee', 'achilles_calf', 'systemic'],
    commonMistakes: [
      'Landing with straight legs or on the heels, which sends the force into the knees and back.',
      'Jumping so far that you fall forward or take a step. Only count the jumps you stick.',
      'Swinging the arms late or only halfway.',
      'Knees caving inward on takeoff or landing.',
      'Jumping low and flat instead of forward and a little up.',
    ],
    goodFormFeels:
      'One fast swing down and forward, a long stretch through the whole body in the air, then a quiet landing that you hold without wobbling.',
    stopRules: [
      'End the set if you cannot stick a landing, you step or fall forward, or the landings get loud.',
      'Stop if your knees cave in on takeoff or landing.',
      QUALITY_RULE,
      PAIN_RULE,
    ],
    safetyNotes: [
      'You train alone, so keep the landing area clear and jump away from walls, racks, and other people.',
      'Jump on a firm floor with some give, never on concrete or a wet or slippery surface.',
      'Count every landing as one foot contact. Volleyball practice and games add their jumps to the same weekly count, so do only the planned jumps and never add more on your own.',
      'Stick each landing before you think about distance. Distance comes from power, not from falling forward.',
    ],
    easierSubstitution: {
      exerciseId: 'snap-down-stick',
      name: 'Snap Down and Stick',
      reason: 'Teaches the fast, quiet landing on its own before you add the forward jump.',
    },
    equipmentSubstitution: {
      exerciseId: 'countermovement-jump',
      name: 'Countermovement Jump',
      reason: 'Needs almost no floor space when there is no clear 3 metre lane.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'box-jump',
        name: 'Box Jump',
        reason: 'Trains the same hip drive, and landing on the box top cuts the landing force on days your knees need a lighter session.',
      },
    ],
    loadIncrement: 'none',
    visual: {
      poses: [
        {
          label: 'Load',
          caption: 'Toes behind the line, push the hips back, bend the knees, and swing both arms back.',
          trunk: 140,
          armNear: [-65, -55],
          armFar: [-60, -50],
          legNear: [58, -30],
          legFar: [55, -32],
          footX: 42,
          props: [
            { type: 'line', x1: 62, y1: 165, x2: 62, y2: 172 },
            { type: 'arrow', from: [120, 70], to: [120, 100] },
          ],
        },
        {
          label: 'Takeoff',
          caption: 'Swing the arms forward and up and drive the hips forward. Stretch out long at about 45 degrees.',
          trunk: 140,
          head: 145,
          armNear: [118, 128],
          armFar: [112, 122],
          legNear: [-36, -38, -5],
          legFar: [-34, -36, -2],
          footX: 58,
          props: [
            { type: 'line', x1: 62, y1: 165, x2: 62, y2: 172 },
            { type: 'arrow', from: [130, 150], to: [175, 120] },
          ],
        },
        {
          label: 'Stick',
          caption: 'Land on both feet with the hips back and the knees over the toes. Hold still for two seconds.',
          trunk: 138,
          armNear: [75, 85],
          armFar: [70, 80],
          legNear: [62, -28, 90],
          legFar: [60, -30, 90],
          footX: 120,
          props: [
            { type: 'line', x1: 62, y1: 165, x2: 62, y2: 172 },
            { type: 'arrow', from: [60, 95], to: [60, 125] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Depth Jump
  {
    id: 'depth-jump',
    name: 'Depth Jump',
    aliases: ['Drop jump', 'Box rebound jump'],
    kind: 'jump',
    purpose:
      'Step off a low box, land, and rebound straight up as fast and as high as you can. It trains reactive strength, which is how well your legs catch a landing and turn it into a quick, high jump. That is the fast plant at the end of a spike approach. Coaches measure it with the reactive strength index: jump height divided by ground contact time. In plain words, jump high while touching the floor as briefly as you can.',
    equipment: ['A stable plyo box, 20 to 30 cm to start and never above 40 cm', 'A firm floor with some give in front of the box', 'Optional phone filming in slow motion to check your ground contact'],
    setup: [
      'Warm up fully first, including a few countermovement jumps and pogo hops.',
      'Set the box on a non slip floor where it cannot slide or tip, with about 2 metres of clear space in front.',
      'Pick the height by the rebound. It is right when the rebound is quick and higher than your standing jump. If contact gets long or your heels crash down, the box is too high, so go lower.',
      'Stand tall at the front edge of the box with your toes near the edge, in supportive trainers.',
    ],
    steps: [
      'Step forward off the box with one foot. Do not jump up or out, just drop.',
      'Land on both feet at once, on the front of the feet, close to the box. The heels may brush the floor but never crash down.',
      'The moment you touch, swing the arms up and jump straight up as high as you can, with as little time on the floor as possible.',
      'Land softly and quietly on both feet with the hips back and the knees over the toes.',
      'Step back up onto the box, stand tall, and reset before the next rep.',
    ],
    breathing: 'Breathe in and brace on the box. Breathe out as you rebound or as you land. Breathe normally while you reset.',
    tempo:
      'The floor contact is the key: as short as you can make it while still jumping high, about a quarter of a second or less. It should feel like the floor is hot. Reset fully for 20 to 30 seconds between reps, and rest 60 to 120 seconds between sets.',
    rangeOfMotion:
      'Only a small, quick dip at contact, with the knees bending a little and the heels light. Finish the rebound fully extended with the arms high. On the final landing, bend the hips and knees until the force is absorbed.',
    muscles: {
      primary: ['quads', 'glute_max', 'gastrocnemius', 'soleus'],
      secondary: ['hamstrings'],
    },
    emphasisNote:
      'The drop stretches the calves, quads, and glutes along with the Achilles and patellar tendons, and a fast rebound uses that stored energy like a spring. This is the stretch shortening cycle, and it works best when the contact is short and stiff. The hamstrings help hold the hips steady. This is power work counted as jump contacts, not muscle building sets.',
    movementPattern: 'jump',
    joints: ['Hip', 'Knee', 'Ankle', 'Shoulder'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['knee', 'achilles_calf', 'systemic'],
    commonMistakes: [
      'Jumping up or out off the box, which makes the drop higher than planned.',
      'Sinking into a deep squat at contact, which turns it into a slow jump.',
      'Heels crashing into the floor, a sign the box is too high.',
      'Landing with one foot before the other.',
      'Knees caving inward at contact or on landing.',
      'Choosing a higher box to feel tougher. Higher is not better here.',
    ],
    goodFormFeels: 'A short, springy bounce, as if the floor is hot. You pop up higher than your standing jump and land quietly.',
    stopRules: [
      'End the set if the ground contact gets long, your heels crash down, or the rebound is lower than your standing jump.',
      'Stop if the landings get loud or your knees cave in.',
      QUALITY_RULE,
      PAIN_RULE,
    ],
    safetyNotes: [
      'Use a solid plyo box that cannot slide or tip, on a non slip floor. Never stack plates, steps, or benches to make a box.',
      'Step off the box with control. This is the one drill where you step off on purpose. Climb back up by stepping, never by jumping.',
      'You train alone, so clear the space in front of and around the box before every set.',
      'Your knees and heels are still growing, and depth jumps load them hard. Keep the box low and never above 40 cm.',
      'Count every landing as a foot contact. Volleyball practice and games add their jumps to the same weekly count, so do only the planned reps and never add more on your own.',
    ],
    easierSubstitution: {
      exerciseId: 'snap-down-stick',
      name: 'Snap Down and Stick',
      reason: 'The same fast, quiet landing from the floor, with much less force than a drop from a box.',
    },
    equipmentSubstitution: {
      exerciseId: 'pogo-hop',
      name: 'Pogo Hop',
      reason: 'Trains short, stiff ground contacts when no stable box is free.',
    },
    otherSubstitutions: [
      {
        exerciseId: null,
        name: 'Depth drop and stick',
        reason: 'Step off the same low box and stick the landing with no rebound. A good first step before full depth jumps.',
      },
    ],
    loadIncrement: 'none',
    visual: {
      poses: [
        {
          label: 'Step off',
          caption: 'Stand at the edge of a low box and step off with one foot. Do not jump up or out.',
          trunk: 166,
          head: 172,
          armNear: [10, 25],
          armFar: [-10, 0],
          legNear: [48, 15, 60],
          legFar: [42, -22, 90],
          hip: [36, DEPTH_BOX_TOP - 68],
          props: [DEPTH_BOX, { type: 'arrow', from: [92, 130], to: [92, 162] }],
        },
        {
          label: 'Contact',
          caption: 'Land on both feet and spring up at once. Keep the contact short and stiff, heels light.',
          trunk: 155,
          armNear: [-50, -38],
          armFar: [-45, -32],
          legNear: [38, -22, 92],
          legFar: [35, -25, 92],
          footX: 98,
          props: [DEPTH_BOX, { type: 'arrow', from: [148, 130], to: [148, 95] }],
        },
        {
          label: 'Rebound',
          caption: 'Jump straight up as high as you can with the arms swinging up hard. Then land softly, hips back.',
          trunk: 178,
          head: 182,
          armNear: [118, 130],
          armFar: [112, 124],
          legNear: [22, -52, -12],
          legFar: [26, -55, -16],
          lift: 14,
          footX: 100,
          props: [DEPTH_BOX, { type: 'arrow', from: [148, 120], to: [148, 70] }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Single Leg Hop
  {
    id: 'single-leg-hop',
    name: 'Single Leg Hop',
    aliases: ['One leg hop', 'Single leg pogo'],
    kind: 'jump',
    purpose:
      'Low, quick, stiff hops on one leg, in place or moving forward, then the same on the other leg. They build the ankle stiffness and the single leg spring for a one foot takeoff, and they show if one leg is weaker. Later in the program they progress to short single leg bounds.',
    equipment: ['A firm floor with some give, such as a court or gym floor', 'Optional line or tape to hop along'],
    setup: [
      'Warm up fully first, including easy jump rope or two leg pogo hops.',
      'Stand on one leg with the knee soft and the other foot lifted just off the floor.',
      'Keep 2 to 3 metres of clear floor around you, or a clear lane if you hop forward.',
      'Wear supportive trainers. Start with your weaker leg, then match the reps on the stronger leg.',
    ],
    steps: [
      'Rise onto the ball of the foot and keep the ankle firm, like a stiff spring.',
      'Hop a few centimetres up, in place or a short way forward, with a quick push from the ankle.',
      'Land on the ball of the same foot with the knee over the toes and go straight into the next hop.',
      'Keep the hips level and the knee in line with the toes on every contact.',
      'After the last hop, land softly with the hips back and the knee bent, and hold for two seconds.',
      'Switch legs and do the same number of hops.',
    ],
    breathing: 'Breathe in short, easy breaths in rhythm with the hops. Do not hold your breath through the set.',
    tempo:
      'Short, springy contacts, about as quick as a jump rope bounce. Small hops, fast off the floor. Do the set on one leg, then the other, and rest 60 to 120 seconds between sets.',
    rangeOfMotion:
      'Small. The ankle and knee bend only a little on each contact, and the heel stays off the floor or barely touches it. On the last landing, bend the hip and knee to absorb the force.',
    muscles: {
      primary: ['gastrocnemius', 'soleus', 'quads'],
      secondary: ['glute_med', 'glute_max'],
    },
    emphasisNote:
      'The calves and the Achilles tendon do most of the spring work. A stiff ankle stores energy on each short contact and gives it straight back, which is the stretch shortening cycle. The quads keep the knee firm, and the side hip muscles hold the pelvis level and stop the knee from caving in. This is how a one foot takeoff works, so it trains the leg you plant. This is power work counted as foot contacts, not muscle building sets.',
    movementPattern: 'jump',
    joints: ['Ankle', 'Knee', 'Hip'],
    laterality: 'unilateral',
    logSides: true,
    fatigueOverlap: ['achilles_calf', 'knee', 'shin'],
    commonMistakes: [
      'Hopping too high, which makes the contacts long and heavy.',
      'Landing flat footed or on the heel.',
      'The knee caving inward or the hip dropping on the side of the lifted leg.',
      'Looking down and leaning forward.',
      'Doing more hops on the stronger leg than on the weaker one.',
    ],
    goodFormFeels: 'Light, quick, and quiet, like bouncing on a stiff spring. The ankle stays firm, the hips stay level, and both legs feel about the same.',
    stopRules: [
      'End the set on that leg if the landings get loud, the heel starts to sink, or the knee caves in.',
      'End the set if the back of the heel, the Achilles, or the shin starts to ache.',
      QUALITY_RULE,
      PAIN_RULE,
    ],
    safetyNotes: [
      'You train alone, so hop in a clear space away from racks, benches, and other people.',
      'Hop on a floor with some give, never on concrete or a slippery surface.',
      'Count every landing as one foot contact, on each leg. One leg takes the whole load, so the sets stay short.',
      'Volleyball practice and games add their jumps to the same weekly count. Do only the planned hops and never add more on your own.',
      'Move on to single leg bounds only when the plan says so and your hops are quiet on both legs.',
    ],
    easierSubstitution: {
      exerciseId: 'pogo-hop',
      name: 'Pogo Hop',
      reason: 'The same quick, stiff ankle on two feet, so each leg takes about half the load.',
    },
    equipmentSubstitution: {
      exerciseId: 'single-leg-calf-raise',
      name: 'Single Leg Dumbbell Calf Raise',
      reason: 'Trains the same calf and ankle on one leg with no impact when there is no space or the floor is too hard.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'bulgarian-split-squat',
        name: 'Bulgarian Split Squat',
        reason: 'Builds single leg strength for the one foot takeoff on days without jumps.',
      },
    ],
    loadIncrement: 'none',
    visual: {
      poses: [
        {
          label: 'Ready',
          caption: 'Stand on the ball of one foot, knee soft, the other foot lifted behind you.',
          trunk: 177,
          armNear: [25, 100],
          armFar: [-15, 70],
          legNear: [8, -4, 70],
          legFar: [30, -60, 30],
        },
        {
          label: 'Hop',
          caption: 'Push off with a stiff ankle and hop just a few centimetres. Toes point a little in the air.',
          trunk: 173,
          head: 177,
          armNear: [30, 105],
          armFar: [-12, 72],
          legNear: [10, -5, 58],
          legFar: [30, -60, 30],
          lift: 6,
          props: [{ type: 'arrow', from: [140, 150], to: [140, 120] }],
        },
        {
          label: 'Land',
          caption: 'Land quietly on the ball of the same foot, knee over the toes, and hop again at once.',
          trunk: 175,
          armNear: [22, 96],
          armFar: [-18, 66],
          legNear: [20, -12, 70],
          legFar: [30, -60, 30],
          props: [
            { type: 'arrow', from: [134, 120], to: [134, 150] },
            { type: 'arrow', from: [148, 150], to: [148, 120] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Approach Jump and Reach
  {
    id: 'approach-touch-jump',
    name: 'Approach Jump and Reach',
    aliases: ['Approach touch', 'Rim touch jump'],
    kind: 'jump',
    purpose:
      'A short run up and a maximal jump to touch as high as you can on a wall mark or a backboard. It turns running speed into height. Done only on a court or outdoors where the run up and the landing are safe. A touch on a hoop is a training note, not a measurement: the jump tests on Progress use a marked wall and the same conditions every time.',
    equipment: [
      'A basketball hoop on a court, or a high wall you are allowed to mark',
      'Chalk, or water to wet your fingertips, to leave a touch mark',
      'A tape measure to read the touch height',
      'A court floor with a clear run up of 4 to 6 metres',
    ],
    setup: [
      'Warm up fully first, including a few countermovement jumps and easy run ups.',
      'Mark a start spot 3 to 5 steps from the point under the rim or below your wall mark.',
      'Check that the run up and the area under the hoop are dry and clear of balls and people. Wear court shoes.',
      'Test both takeoffs, two foot and one foot, with a few attempts each on a fresh day. Keep the one that touches higher.',
      'To read the touch height, chalk or wet your fingertips, touch the wall, and measure the mark from the floor. On a hoop, use known heights: the rim is 305 cm. Log the height of every touch in the Reach field.',
    ],
    steps: [
      'Run into the approach for 3 to 5 steps, each step a little quicker than the last.',
      'Make the penultimate step, the second to last one, longer and lower. Drop the hips and swing both arms back.',
      'Plant quickly. For a two foot takeoff, plant both feet close together. For a one foot takeoff, plant the inside leg and drive the other knee up.',
      'Swing both arms up hard and jump straight up, reaching with one hand to touch as high as you can on the net, the rim, the backboard, or the wall mark.',
      'Land softly and quietly on both feet with the hips back and the knees over the toes, then walk back.',
    ],
    breathing: 'Breathe naturally on the run up. Many players breathe out sharply at takeoff. Take easy breaths while you rest.',
    tempo:
      'Build speed through the run up, with the last two steps the quickest. Explosive takeoff, soft controlled landing. Rest fully, 60 to 120 seconds, between attempts. Full rest keeps every jump maximal, and maximal jumps are what build jump height.',
    rangeOfMotion:
      'A long, low second to last step, a quick dip to about a quarter squat at the plant, then full extension of the hips, knees, and ankles with the reaching arm fully stretched. On landing, bend the hips and knees until the force is absorbed.',
    muscles: {
      primary: ['glute_max', 'quads', 'gastrocnemius'],
      secondary: ['soleus', 'hamstrings', 'obliques_core', 'delt_anterior'],
    },
    emphasisNote:
      'The long, low second to last step lets the glutes and quads load up, and the quick plant stretches the legs and tendons so they recoil like a spring. That is the stretch shortening cycle. The calves add the final push, the core keeps the trunk stiff so the arm swing adds height, and the front of the shoulders drives the arms up. This is power work counted as jump contacts, not muscle building sets.',
    movementPattern: 'jump',
    joints: ['Hip', 'Knee', 'Ankle', 'Shoulder'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['knee', 'achilles_calf', 'systemic'],
    commonMistakes: [
      'Running in faster than you can control at the plant. Use only the speed you can turn into height.',
      'A short, high second to last step that does not drop the hips.',
      'A slow plant or a pause before the jump.',
      'Jumping forward into the post or the wall instead of up.',
      'Landing on one stiff leg after a one foot takeoff.',
      'Cutting the rest short, so the jumps are no longer maximal.',
    ],
    goodFormFeels:
      'A run up that speeds up into a long, low step, then a quick plant and a snap upward where the arms and legs finish together. You stretch tall at the top with the reaching arm, then land quiet and balanced.',
    stopRules: [
      'Stop the drill for the day if your touch drops clearly below your best of the day or your landings get loud.',
      'Stop if your knees cave in at the plant or on landing.',
      QUALITY_RULE,
      PAIN_RULE,
    ],
    safetyNotes: [
      'You train alone, so check that nobody is shooting, rebounding, or walking under the hoop before every attempt.',
      'Touch the rim and let go. Never hang on it, and land on your feet below it.',
      'Leave room to land in front of the wall or post, and jump up, not into it.',
      'Count every landing as one foot contact. Volleyball practice and games add their jumps to the same weekly count, so do only the planned attempts and never add more on your own.',
    ],
    easierSubstitution: {
      exerciseId: 'countermovement-jump',
      name: 'Countermovement Jump',
      reason: 'Removes the run up so you can practise the dip, the arm swing, and the reach first.',
    },
    equipmentSubstitution: {
      exerciseId: 'volleyball-approach-jump',
      name: 'Volleyball Approach Jump',
      reason: 'Uses the same run up on any open court when no hoop or high wall is free. Reach for a spot in the air.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'volleyball-approach-footwork',
        name: 'Volleyball Approach Footwork',
        reason: 'Practise the run up and the long, low second to last step without jumping on days with a jump limit.',
      },
    ],
    loadIncrement: 'none',
    visual: {
      poses: [
        {
          label: 'Penultimate',
          caption: 'Take a long, low second to last step. Drop the hips and swing both arms back.',
          trunk: 160,
          armNear: [-75, -65],
          armFar: [-68, -58],
          legNear: [50, 0, 105],
          legFar: [-30, -60, 0],
          footX: 100,
          props: [...RIM, { type: 'arrow', from: [130, 100], to: [170, 100] }],
        },
        {
          label: 'Takeoff',
          caption: 'Plant quickly and swing both arms up hard as the hips, knees, and ankles extend.',
          trunk: 162,
          armNear: [105, 120],
          armFar: [96, 112],
          legNear: [25, -10, 75],
          legFar: [28, -8, 78],
          footX: 85,
          props: [...RIM, { type: 'arrow', from: [150, 130], to: [150, 85] }],
        },
        {
          label: 'Reach',
          caption: 'Reach up with one hand and touch as high as you can, on the rim or a wall mark.',
          trunk: 178,
          head: 184,
          armNear: [155, 162],
          armFar: [15, 35],
          legNear: [45, -80, -45],
          legFar: [52, -75, -40],
          lift: 12,
          footX: 132,
          props: [...RIM, { type: 'arrow', from: [118, 75], to: [118, 40] }],
        },
      ],
    },
  },
];
