import { PAIN_RULE, QUALITY_RULE } from './effort';
import type { ExerciseContent, PoseProp } from '../types';

// Jump drills for the dunk program, part A. Order matches JUMP_A_IDS in ids.ts.
// Written for a young, heavy, still growing jumper who trains alone: quality first, never to failure,
// soft landings that protect the knees and heels, and no jumps beyond the plan.

const GROUND = 172;

/** A plyo box of about 37 cm, drawn to the figure's scale (about 1.15 cm per pixel). */
const BOX_H = 32;
const BOX_TOP = GROUND - BOX_H;

/** A low hurdle of about 30 cm seen from the side: an upright plus a short top bar. */
const HURDLE_H = 26;
function hurdle(x: number): PoseProp[] {
  return [
    { type: 'line', x1: x, y1: GROUND, x2: x, y2: GROUND - HURDLE_H },
    { type: 'line', x1: x - 7, y1: GROUND - HURDLE_H, x2: x + 7, y2: GROUND - HURDLE_H },
  ];
}

export const JUMPS_A: ExerciseContent[] = [
  // ---------------------------------------------------------------- Pogo Hop
  {
    id: 'pogo-hop',
    name: 'Pogo Hop',
    aliases: ['Pogo jump', 'Ankle hop'],
    kind: 'jump',
    purpose:
      'Trains stiff, springy ankles. Small, fast hops teach the calves and Achilles tendon to store energy as you land and give it straight back as you leave the floor. That rebound finishes every jump you take. It also makes a good warm up before bigger jumps.',
    equipment: ['No equipment', 'Firm, flat floor with some give, such as a gym or court floor', 'Supportive trainers'],
    setup: [
      'Stand in a clear space with at least 2 metres free around you.',
      'Place your feet about hip width apart with your weight on the balls of your feet.',
      'Lift your heels just off the floor and keep your knees almost straight, soft but not locked.',
      'Bend your elbows to about 90 degrees with your hands by your hips.',
      'Wear supportive trainers with the laces tied firmly. Avoid concrete if you can.',
    ],
    steps: [
      'Hop a few centimetres off the floor, using mostly your ankles. The knees bend only a little.',
      'Point your toes slightly in the air so you meet the floor on the balls of your feet.',
      'Touch down softly and quietly with the heels still off the floor and the knees over your toes.',
      'Bounce straight back up at once, as if the floor were hot.',
      'Keep a steady rhythm with small forearm swings for the planned number of hops.',
      'After the last hop, land softly with the hips going back and the knees bending, then stand still.',
    ],
    breathing: 'Breathe in a short, relaxed rhythm. Do not hold your breath through the set. Breathe normally between sets.',
    tempo:
      'Very short ground contacts, about 2 to 3 hops per second. Each touch should be over almost before you feel it. Sets are short, often 10 to 20 hops. Stand still and reset after each set, and rest 60 to 120 seconds between sets.',
    rangeOfMotion:
      'Small. Your feet leave the floor only 3 to 8 centimetres, the knees bend a little, and the heels never sink to the floor. Most of the movement comes from the ankles.',
    muscles: {
      primary: ['gastrocnemius', 'soleus'],
      secondary: ['tibialis_anterior', 'quads'],
    },
    emphasisNote:
      'The calves and Achilles tendon carry most of the work. They act like a stiff spring: they stretch a little as you land and recoil as you leave the floor. This is the stretch shortening cycle. The shin muscles help hold the foot position and the quads keep the knees firm. It trains ankle stiffness and timing, counted as jump contacts, not as calf building sets.',
    movementPattern: 'jump',
    joints: ['Ankle', 'Knee', 'Hip'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['achilles_calf', 'shin'],
    commonMistakes: [
      'Letting the heels sink to the floor on each landing, which makes the contact long and slow.',
      'Bending the knees a lot, which turns the hop into a small squat jump.',
      'Hopping as high as you can. Quick, springy contacts matter more than height.',
      'Landing loudly or flat footed.',
      'Knees drifting inward or the feet creeping apart.',
    ],
    goodFormFeels:
      'Light and springy, like a bouncing ball. The floor contact is so short you barely feel it, your calves feel warm, and each hop is quiet.',
    stopRules: [
      'End the set when your heels start to touch down, the hops get louder, or the contacts get longer and slower.',
      'Stop for pain at the back of the heel, in the Achilles tendon, or along the shin.',
      QUALITY_RULE,
      PAIN_RULE,
    ],
    safetyNotes: [
      'You train alone, so clear a space of about 2 metres around you and keep weights and benches out of the way.',
      'Count every landing as one foot contact. A set of 20 pogo hops is 20 contacts.',
      'Volleyball practice and games add their jumps to the same weekly count. Do only the planned hops, and do not add sets or reps on your own, even on a good day.',
      'Hop on a floor with some give, in supportive trainers.',
      'While you are growing, the back of the heel is sensitive. Heel soreness that lasts into the next day means tell a parent or coach before you hop again.',
    ],
    easierSubstitution: {
      exerciseId: 'easy-jump-rope',
      name: 'Easy Jump Rope',
      reason: 'Lower, gentler bounces with the same quick foot contacts. Easier on the calves and Achilles.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Pogo hops on flat grass',
      reason: 'Use any flat surface with some give when the gym floor is busy. Avoid concrete and tile.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'standing-calf-raise',
        name: 'Standing Calf Raise',
        reason: 'Builds calf strength without impact on days when the Achilles needs a break from hopping.',
      },
    ],
    loadIncrement: 'none',
    visual: {
      poses: [
        {
          label: 'Ready',
          caption: 'Stand tall on the balls of your feet, heels just up, knees almost straight, elbows bent.',
          trunk: 179,
          armNear: [10, 95],
          armFar: [6, 90],
          legNear: [2, -2, 65],
          legFar: [3, -1, 65],
        },
        {
          label: 'Hop',
          caption: 'Spring a few centimetres up from the ankles. Toes point slightly, knees stay nearly straight.',
          trunk: 180,
          armNear: [14, 100],
          armFar: [10, 95],
          legNear: [2, -1, 55],
          legFar: [3, 0, 55],
          lift: 4,
          props: [{ type: 'arrow', from: [150, 150], to: [150, 120] }],
        },
        {
          label: 'Contact',
          caption: 'Touch down quietly on the balls of your feet, heels up, and bounce straight back up.',
          trunk: 178,
          armNear: [8, 90],
          armFar: [4, 85],
          legNear: [6, -6, 70],
          legFar: [7, -5, 70],
          props: [
            { type: 'arrow', from: [142, 120], to: [142, 150] },
            { type: 'arrow', from: [156, 150], to: [156, 120] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Snap Down and Stick
  {
    id: 'snap-down-stick',
    name: 'Snap Down and Stick',
    aliases: ['Snap down', 'Drop and stick'],
    kind: 'jump',
    purpose:
      'Teaches you to land fast, quiet, and in control. You drop from tall on your toes into a strong athletic landing and freeze. Learning to brake well protects your knees, and it lets you jump harder later, because your body only uses the power it knows it can stop.',
    equipment: ['Firm, flat floor with some give, such as a gym or court floor', 'Optional mirror at your side to check the landing position'],
    setup: [
      'Warm up first, for example with easy jump rope and a few pogo hops.',
      'Stand in a clear space with your feet about hip width apart.',
      'Rise onto the balls of your feet and reach both arms straight overhead.',
      'If you can, stand side on to a mirror so you can check your landing.',
      'Wear supportive trainers with the laces tied firmly.',
    ],
    steps: [
      'Stand tall on the balls of your feet with both arms reaching overhead.',
      'Snap both arms down and back hard, and at the same moment drop your hips fast.',
      'Land on both feet, balls of the feet first and then the whole foot, softly and quietly.',
      'Stop in an athletic position: hips back, knees bent about 45 to 60 degrees, knees over your toes, chest over your knees.',
      'Freeze there for 2 seconds without wobbling, then stand up and reset.',
    ],
    breathing: 'Breathe in as you reach tall. Breathe out sharply as you snap down, then breathe normally while you hold the landing.',
    tempo:
      'The drop is as fast as you can make it, then a sudden stop. Hold the landing for 2 seconds, stand up, and take a full reset of 10 to 20 seconds before the next rep. Rest 60 to 120 seconds between sets.',
    rangeOfMotion:
      'From fully tall on the toes down to a landing with the knees bent about 45 to 60 degrees and the hips back. Do not sink into a deep squat. Stop at the depth you can reach fast and hold still.',
    muscles: {
      primary: ['quads', 'glute_max'],
      secondary: ['hamstrings', 'obliques_core'],
    },
    emphasisNote:
      'The quads and glutes do the braking. They work while lengthening to stop your body quickly, which is the eccentric part of every jump and landing. The hamstrings help hold the hips back and the core keeps the trunk stiff. This trains landing skill and braking strength, counted as landings, not as muscle building sets.',
    movementPattern: 'jump',
    joints: ['Hip', 'Knee', 'Ankle', 'Shoulder'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['knee', 'achilles_calf'],
    commonMistakes: [
      'Landing with the hips under the shoulders and the knees far past the toes, which loads the front of the knee.',
      'Knees caving inward on the landing.',
      'Sinking slowly instead of dropping fast and stopping suddenly.',
      'Landing on the heels or with a loud slap.',
      'Rounding the back or letting the chest fall to the thighs.',
    ],
    goodFormFeels:
      'A fast drop and a sudden, quiet stop. You feel the front of the thighs and the glutes catch you, your weight sits over the middle of your feet, and you can hold still without wobbling.',
    stopRules: [
      'End the set when the landing gets loud, you wobble or step to catch your balance, or your knees start to cave in.',
      'Stop for pain just below the kneecap or at the top of the shin.',
      QUALITY_RULE,
      PAIN_RULE,
    ],
    safetyNotes: [
      'You train alone, so clear a space of about 2 metres around you and keep weights and benches out of the way.',
      'Count every landing as one foot contact, even though this drill is small.',
      'Volleyball practice and games add their jumps to the same weekly count. Do only the planned reps, and do not add sets on your own.',
      'Land on a floor with some give, in supportive trainers.',
      'Master this landing before box jumps or hurdle hops. If your landing is not quiet and still, stay with this drill.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Slow drop to athletic stance',
      reason: 'Start flat footed and lower into the same landing position at a slow, steady speed. Learn the position before adding speed.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Snap down and stick on flat grass',
      reason: 'Use any flat surface with some give when no gym floor is free.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'countermovement-jump',
        name: 'Countermovement Jump',
        reason: 'The next step once your landing is quiet and still: add a jump before the landing.',
      },
    ],
    loadIncrement: 'none',
    visual: {
      poses: [
        {
          label: 'Tall',
          caption: 'Rise onto the balls of your feet and raise both arms high.',
          trunk: 180,
          armNear: [122, 128],
          armFar: [116, 124],
          legNear: [0, 0, 60],
          legFar: [2, -2, 60],
        },
        {
          label: 'Snap',
          caption: 'Snap the arms down and back hard as the hips drop fast.',
          trunk: 160,
          head: 172,
          armNear: [30, 40],
          armFar: [25, 35],
          legNear: [22, -10, 60],
          legFar: [24, -8, 60],
          props: [{ type: 'arrow', from: [150, 40], to: [150, 85] }],
        },
        {
          label: 'Stick',
          caption: 'Freeze for 2 seconds: hips back, knees over toes, chest over knees, landing quiet.',
          trunk: 140,
          head: 158,
          armNear: [-60, -50],
          armFar: [-56, -46],
          legNear: [35, -25, 90],
          legFar: [33, -27, 90],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Box Jump
  {
    id: 'box-jump',
    name: 'Box Jump',
    aliases: ['Box jump with step down'],
    kind: 'jump',
    purpose:
      'Lets you practise a full effort takeoff with a big arm swing while the box takes away most of the landing. You land higher than you took off, so your legs absorb far less force than on a floor landing. That makes it a good way to train jump intent for the dunk while protecting the knees.',
    equipment: [
      'Stable plyo box 30 to 50 cm high that cannot slide or tip',
      'Firm, flat floor with some give, with clear space around the box',
    ],
    setup: [
      'Warm up fully first, including pogo hops and a few snap downs.',
      'Check the box sits flat on the floor and does not rock or slide when you push it with your foot.',
      'Pick a box low enough that you land in a quarter squat. If you land in a deep squat, the box is too high.',
      'Stand facing the box about half a step away, roughly 30 cm from the front edge, feet hip width apart.',
      'Wear supportive trainers with the laces tied firmly.',
    ],
    steps: [
      'Dip quickly by pushing the hips back and bending the knees to a quarter or half squat, swinging both arms back.',
      'Without pausing, swing the arms forward and up hard and drive through the floor, fully extending the hips, knees, and ankles.',
      'Bring the knees up and land on the middle of the box with your whole foot, softly and quietly, knees over toes and hips back.',
      'Stand up tall on the box to finish the rep.',
      'Step down one foot at a time, never jump down, then reset before the next rep.',
    ],
    breathing: 'Breathe in and brace before the dip. Breathe out as you jump or as you land. Breathe normally as you step down and reset.',
    tempo:
      'Fast dip, no pause at the bottom, full effort takeoff, soft landing on the box. Step down calmly and take a full reset of 15 to 30 seconds between reps. Rest 60 to 120 seconds between sets.',
    rangeOfMotion:
      'Dip to a quarter or half squat, the depth you can reverse quickly. Finish the takeoff fully extended with the arms high. Land on the box in a quarter squat, no deeper.',
    muscles: {
      primary: ['glute_max', 'quads'],
      secondary: ['gastrocnemius', 'soleus', 'hamstrings'],
    },
    emphasisNote:
      'The glutes and quads produce most of the force at takeoff, the calves add the last push through the ankles, and the hamstrings help extend the hips. The arm swing adds height by helping the legs push harder. Because you land on the box, the landing load stays small. This is power practice counted as jump contacts, not as muscle building sets.',
    movementPattern: 'jump',
    joints: ['Hip', 'Knee', 'Ankle', 'Shoulder'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['knee', 'achilles_calf', 'systemic'],
    commonMistakes: [
      'Using a box so high that you land in a deep squat. That tests how high you can tuck your knees, not how high you jump.',
      'Jumping down off the box, which adds a hard landing to every rep.',
      'Pausing at the bottom of the dip, which loses the spring.',
      'A small or late arm swing.',
      'Landing on the toes near the edge, or with the knees caving inward.',
    ],
    goodFormFeels:
      'A fast dip and a strong push where the arms and legs finish together. You land quietly on the box with your whole foot, already balanced, and the landing feels easy.',
    stopRules: [
      'End the set when the box landing gets loud, you land near the edge, or your knees start to cave in.',
      'If you clip the box edge or feel unsure about clearing it, stop and use a lower box next time.',
      QUALITY_RULE,
      PAIN_RULE,
    ],
    safetyNotes: [
      'You train alone, so use a stable box that cannot slide or tip, on a flat floor, with about 2 metres of clear space around and behind it.',
      'Always step down from the box, one foot at a time. Never jump down.',
      'Count every landing on the box as one foot contact.',
      'Volleyball practice and games add their jumps to the same weekly count. Do only the planned jumps, and do not add sets or raise the box on your own.',
      'Keep your bag, bottle, and phone well away from the box.',
    ],
    easierSubstitution: {
      exerciseId: 'snap-down-stick',
      name: 'Snap Down and Stick',
      reason: 'Practise the landing position on its own if your box landings are loud or deep.',
    },
    equipmentSubstitution: {
      exerciseId: 'countermovement-jump',
      name: 'Countermovement Jump',
      reason: 'The same dip and arm swing when no box is free. The floor landing is harder, so land softly and keep to the planned reps.',
    },
    otherSubstitutions: [
      {
        exerciseId: null,
        name: 'Low box jump',
        reason: 'Use a 20 to 30 cm box while you learn the takeoff, the landing, and the step down.',
      },
    ],
    loadIncrement: 'none',
    visual: {
      poses: [
        {
          label: 'Dip',
          caption: 'Half a step from the box, push the hips back, bend the knees, and swing both arms back.',
          trunk: 145,
          armNear: [-60, -50],
          armFar: [-55, -45],
          legNear: [55, -30],
          legFar: [52, -32],
          footX: 60,
          props: [
            { type: 'box', x: 100, y: BOX_TOP, w: 60, h: BOX_H },
            { type: 'arrow', from: [18, 50], to: [18, 85] },
          ],
        },
        {
          label: 'Takeoff',
          caption: 'Swing the arms up hard and drive the hips, knees, and ankles to full extension.',
          trunk: 160,
          head: 170,
          armNear: [118, 128],
          armFar: [110, 122],
          legNear: [-10, -12, 25],
          legFar: [-8, -10, 28],
          footX: 62,
          props: [
            { type: 'box', x: 100, y: BOX_TOP, w: 60, h: BOX_H },
            { type: 'arrow', from: [112, 112], to: [140, 86] },
          ],
        },
        {
          label: 'Land',
          caption: 'Land softly on the box in a quarter squat and stand tall. Then step down, never jump down.',
          trunk: 140,
          head: 160,
          armNear: [40, 55],
          armFar: [36, 50],
          legNear: [35, -22, 90],
          legFar: [33, -24, 90],
          hip: [116, 68.5],
          props: [{ type: 'box', x: 100, y: BOX_TOP, w: 60, h: BOX_H }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Hurdle Hop
  {
    id: 'hurdle-hop',
    name: 'Hurdle Hop',
    aliases: ['Two foot hurdle hop', 'Mini hurdle hop'],
    kind: 'jump',
    purpose:
      'Builds reactive strength, the ability to land and leave the floor again quickly. Short, springy contacts between low hurdles train the same fast stretch and rebound your legs use on the plant step of a spike or dunk approach.',
    equipment: [
      '3 to 5 low hurdles or cones, 15 to 45 cm high, that tip over if you clip them',
      'Firm, flat floor with some give and a clear lane of about 6 metres',
    ],
    setup: [
      'Warm up fully first, including pogo hops and a few snap downs.',
      'Set 3 to 5 hurdles in a straight line, about 1 metre apart.',
      'Start with the lowest height. Raise the hurdles only when the plan says.',
      'Stand about half a metre behind the first hurdle, feet hip width apart, weight on the balls of your feet.',
      'Wear supportive trainers with the laces tied firmly.',
    ],
    steps: [
      'Dip slightly with the arms back, then hop over the first hurdle with both feet together.',
      'Drive both knees up and swing the arms forward and up to clear the hurdle.',
      'Land on the balls of your feet, softly and quietly, knees over your toes and hips slightly back.',
      'Rebound straight away into the next hurdle, keeping each contact short and quick.',
      'After the last hurdle, land softly with the hips back and knees bent, and hold it for a second.',
      'Walk back to the start and reset before the next row.',
    ],
    breathing: 'Breathe in before the first hop. Short, natural breaths through the row are fine. Breathe normally on the walk back.',
    tempo:
      'Short, quick ground contacts between hurdles, as if the floor were hot, with one even rhythm from the first hurdle to the last. Walk back and fully reset after each row, and rest 60 to 120 seconds between sets.',
    rangeOfMotion:
      'The knees drive up just enough to clear each hurdle with a little room. On each contact the hips and knees bend only a little, a shallow quarter squat at most, so you can rebound fast. Finish with a deeper, controlled landing.',
    muscles: {
      primary: ['gastrocnemius', 'soleus', 'quads'],
      secondary: ['glute_max', 'hip_flexors'],
    },
    emphasisNote:
      'The calves, Achilles tendon, and quads act like springs on each contact. They stretch as you land and recoil as you leave, which is the stretch shortening cycle, the same one your legs use in the plant step. The glutes help extend the hips and the hip flexors lift the knees over each hurdle. This trains quick contacts and timing, counted as jump contacts, not as muscle building sets.',
    movementPattern: 'jump',
    joints: ['Ankle', 'Knee', 'Hip', 'Shoulder'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['knee', 'achilles_calf', 'systemic'],
    commonMistakes: [
      'Long, heavy contacts with a deep knee bend between hurdles. Use lower hurdles until the contacts are quick.',
      'Hurdles set so high that you stop and gather before each one.',
      'Landing on the heels or flat footed.',
      'Knees caving inward on landing.',
      'Kicking the feet back under you instead of driving the knees up.',
    ],
    goodFormFeels:
      'Bouncy and rhythmic, as if the floor pushes you up. Each contact is quick and quiet, and you clear every hurdle with the same easy height.',
    stopRules: [
      'End the set when contacts get long or loud, you have to pause between hurdles, or your knees start to cave in.',
      'Stop for pain just below the kneecap or at the back of the heel.',
      QUALITY_RULE,
      PAIN_RULE,
    ],
    safetyNotes: [
      'You train alone, so use hurdles or cones that tip over if you clip them, never a fixed bar, and keep the lane and 2 metres past the last hurdle clear.',
      'Count every landing as one foot contact. A row of 5 hurdles is 5 contacts.',
      'Volleyball practice and games add their jumps to the same weekly count. Do only the planned rows, and do not add rows or raise the hurdles on your own.',
      'Hop on a floor with some give, in supportive trainers.',
      'While you are growing, the spot just below the kneecap and the back of the heel are sensitive. Soreness there that lasts into the next day means tell a parent or coach before you hop again.',
    ],
    easierSubstitution: {
      exerciseId: 'pogo-hop',
      name: 'Pogo Hop',
      reason: 'The same quick, springy contacts in place, without hurdles to clear.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Hops over floor lines',
      reason: 'With no hurdles or cones, hop over court lines or flat markers about 1 metre apart, with the same quick contacts and knee drive.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'snap-down-stick',
        name: 'Snap Down and Stick',
        reason: 'Practise a quiet, controlled landing first if your contacts between hurdles are loud.',
      },
    ],
    loadIncrement: 'none',
    visual: {
      poses: [
        {
          label: 'Push',
          caption: 'Push off the balls of your feet and swing the arms forward and up toward the hurdle.',
          trunk: 162,
          head: 170,
          armNear: [118, 128],
          armFar: [110, 122],
          legNear: [-10, -12, 25],
          legFar: [-8, -10, 28],
          footX: 75,
          props: [...hurdle(118), { type: 'arrow', from: [110, 125], to: [140, 100] }],
        },
        {
          label: 'Clear',
          caption: 'Drive both knees up to clear the hurdle, arms forward, trunk tall.',
          trunk: 170,
          armNear: [112, 125],
          armFar: [105, 118],
          legNear: [75, -15, 70],
          legFar: [72, -18, 70],
          lift: 32,
          footX: 105,
          props: [...hurdle(108), { type: 'arrow', from: [150, 60], to: [180, 60] }],
        },
        {
          label: 'Rebound',
          caption: 'Land quietly on the balls of your feet, knees over toes, and spring straight into the next hurdle.',
          trunk: 168,
          armNear: [-50, -40],
          armFar: [-45, -35],
          legNear: [22, -14, 70],
          legFar: [24, -12, 70],
          footX: 95,
          props: [...hurdle(46), ...hurdle(140), { type: 'arrow', from: [118, 120], to: [138, 100] }],
        },
      ],
    },
  },
];
