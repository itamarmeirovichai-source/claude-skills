import type { ExerciseContent } from '../types';

// Athletic, volleyball, and trunk exercises. Order matches ATHLETIC_IDS in ids.ts.
// Written for a young volleyball player: quality first, never to failure,
// and no volume increases without a coach or the plan.

export const ATHLETIC_EXERCISES: ExerciseContent[] = [
  // ---------------------------------------------------------------- Easy Jump Rope
  {
    id: 'easy-jump-rope',
    name: 'Easy Jump Rope',
    aliases: ['Skipping rope', 'Easy rope intervals'],
    kind: 'conditioning',
    purpose:
      'Easy morning conditioning that trains quick, quiet foot contacts and builds calf and Achilles tolerance for jumping, without adding much fatigue.',
    equipment: ['Jump rope that fits your height', 'Supportive trainers', 'Firm, flat floor with a little give, such as a gym or court floor'],
    setup: [
      'Stand on the middle of the rope. The handles should reach about armpit height. Adjust the length if not.',
      'Pick a firm, flat surface with a little give. Avoid concrete if you can.',
      'Stand tall with your feet close together and your weight on the balls of your feet.',
      'Keep your elbows close to your sides with the handles just in front of your hips.',
      'Set a timer for 1 minute of skipping and 30 seconds of rest.',
    ],
    steps: [
      'Swing the rope over your head from behind and let it drop in front of your feet.',
      'Turn the rope with small circles of the wrists, not big arm swings.',
      'Hop only 2 to 3 centimetres off the floor as the rope passes under your feet.',
      'Land softly on the balls of your feet with slightly bent knees. Your heels touch the floor lightly or not at all.',
      'Keep a steady, relaxed rhythm for the full minute. Single bounces only, no double unders.',
      'Rest for 30 seconds and shake out your calves, then repeat for the planned rounds.',
    ],
    breathing: 'Breathe steadily. You should be able to say a short sentence. If you are gasping, slow the rope down.',
    tempo:
      'An even, relaxed rhythm you could keep for several minutes. Effort about 3 to 4 out of 10. Work for 1 minute, rest for 30 seconds.',
    rangeOfMotion:
      'Small. Your feet leave the floor only 2 to 3 centimetres and the knees bend just enough to soften each landing. The ankles do most of the work.',
    muscles: {
      primary: ['gastrocnemius', 'soleus'],
      secondary: ['tibialis_anterior', 'quads', 'glute_max', 'obliques_core'],
    },
    emphasisNote:
      'Bouncing off the balls of the feet puts most of the load on the calves. The shins, thighs, glutes, and trunk work to keep each contact stiff and quiet. Treat it as easy conditioning and tendon exposure, not as calf building sets.',
    movementPattern: 'jump',
    joints: ['Ankle', 'Knee', 'Hip', 'Wrist'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['achilles_calf', 'shin', 'systemic'],
    commonMistakes: [
      'Jumping too high, which turns an easy session into hard jumping.',
      'Swinging the whole arm instead of turning the rope from the wrists.',
      'Landing flat footed or on locked knees, so each contact is loud.',
      'Adding double unders or tricks. Keep to single, easy bounces.',
      'Looking down at your feet so the upper back rounds.',
    ],
    goodFormFeels:
      'Light, quiet, and rhythmic. Your calves feel warm and springy, your shoulders stay relaxed, and you could keep talking in short sentences.',
    stopRules: [
      'Stop if you feel pain in the Achilles tendon, the front of the shin, or the arch of the foot. Pain of 4 out of 10 or more, or pain that worsens or changes how you land, pauses jump rope. Tell a parent, coach, or clinician.',
      'End the round early if your landings get loud or heavy, or you keep catching the rope because you are tired.',
      'Stop if you feel dizzy, unusually breathless, or have chest pain.',
    ],
    safetyNotes: [
      'This is an easy session. You should finish warm, not tired.',
      'Keep to the planned rounds. Do not add rounds on your own. Achilles or shin soreness the next morning means cut back and tell a parent or coach.',
      'Skip on a surface with some give, in supportive shoes.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Marching or easy jogging on the spot',
      reason: 'Keeps the heart rate up with much less impact on the calves and Achilles.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Rope free skipping',
      reason: 'Same rhythm and foot contacts when you have no rope. Turn your wrists as if you were holding the handles.',
    },
    otherSubstitutions: [
      { exerciseId: null, name: 'Easy cycling', reason: 'Low impact conditioning for days when the calves or shins need a break from jumping.' },
    ],
    loadIncrement: 'none',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Stand tall with elbows by your sides and the handles just in front of your hips.',
          trunk: 178,
          armNear: [12, 75],
          armFar: [8, 70],
          legNear: [6, -4, 80],
          legFar: [8, -2, 80],
          props: [{ type: 'rope' }],
        },
        {
          label: 'Hop',
          caption: 'Turn the rope from the wrists and hop just high enough for it to pass under.',
          trunk: 177,
          armNear: [14, 80],
          armFar: [10, 75],
          legNear: [14, -10, 45],
          legFar: [16, -8, 45],
          lift: 4,
          props: [{ type: 'rope' }],
        },
        {
          label: 'Land',
          caption: 'Land quietly on the balls of your feet with soft knees, ready for the next turn.',
          trunk: 177,
          armNear: [12, 75],
          armFar: [8, 70],
          legNear: [14, -12, 70],
          legFar: [16, -10, 70],
          props: [{ type: 'rope' }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Dynamic Volleyball Warm Up
  {
    id: 'dynamic-volleyball-warm-up',
    name: 'Dynamic Volleyball Warm Up',
    aliases: ['Movement preparation', 'Pre training warm up'],
    kind: 'warmup',
    purpose:
      'Raises body temperature and moves every joint you use in volleyball, so the jumps, sprints, and spikes that follow feel smooth and controlled. It is also your chance to notice anything that feels off before hard work.',
    equipment: ['Light resistance band', 'Open floor or half a court', 'The shoes you will train in'],
    setup: [
      'Clear a space about the size of half a court.',
      'Have a light band ready for the arm station.',
      'Plan 8 to 10 minutes. Start easy and build up gradually.',
      'Wear the shoes you will train in.',
    ],
    steps: [
      'Easy movement, 2 minutes. Jog lightly around the court, then mix in side shuffles and backward jogging.',
      'Leg swings, 1 minute. Hold a wall and swing each leg 10 times front to back, then 10 times side to side.',
      'Lunges with reach, 1 minute. Take 5 walking lunges on each leg and reach both arms overhead as you step.',
      'Arm circles and band pull aparts, 1 minute. Make 10 arm circles each way, small to big, then 12 to 15 band pull aparts at chest height.',
      'Skips, 1 minute. Skip about 10 metres with a light knee lift and arm swing, then skip back a little higher.',
      'Shuffles, 1 minute. Shuffle along the net and back in a low stance without letting your feet cross.',
      'Approach steps, 1 minute. Walk through your approach, then jog it, then do it at about three quarter speed without jumping.',
      'Easy jumps, 1 minute. Finish with 3 to 5 approach or standing jumps at about 70 percent effort, landing softly.',
    ],
    breathing: 'Breathe easily throughout. You should be able to talk. Breathing picks up a little near the end as the movements get quicker.',
    tempo:
      'Builds from easy to brisk. Start slow and controlled and finish at about 70 to 80 percent of game speed. No station should feel hard.',
    rangeOfMotion:
      'Start with comfortable ranges and let each swing, lunge, and circle get a little bigger each rep until you reach your normal full range. Never force a stretch.',
    muscles: {
      primary: ['glute_max', 'quads'],
      secondary: [
        'hamstrings',
        'glute_med',
        'adductors',
        'hip_flexors',
        'gastrocnemius',
        'soleus',
        'obliques_core',
        'delt_posterior',
        'traps_middle',
        'rhomboids',
        'rotator_cuff',
        'serratus_anterior',
      ],
    },
    emphasisNote:
      'This is preparation for training. It is counted as activity exposure, not as hypertrophy sets, even though almost every muscle works lightly. The legs and hips do the most, and the band and arm work prepare the upper back and shoulders for hitting.',
    movementPattern: 'general_preparation',
    joints: ['Ankle', 'Knee', 'Hip', 'Spine', 'Shoulder'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['systemic'],
    commonMistakes: [
      'Rushing into fast jumps before you are warm.',
      'Turning the warm up into a workout that leaves you tired.',
      'Holding long static stretches instead of moving.',
      'Skipping the arm and band station before hitting.',
      'Doing the approach steps carelessly instead of practising good footwork.',
    ],
    goodFormFeels:
      'Warm, loose, and ready. Your breathing is up a little, your legs feel springy, and your shoulders move freely overhead.',
    stopRules: [
      'Stop and tell a parent, coach, or clinician if any movement causes pain of 4 out of 10 or more, or pain that gets worse as you warm up.',
      'Skip the jumps if landings feel heavy or you feel Achilles or shin pain.',
      'Stop if you feel dizzy, unusually breathless, or have chest pain.',
    ],
    safetyNotes: [
      'A warm up should feel easier as it goes. If a joint feels worse as you warm up, leave the hard work for another day and report it.',
      'Keep the final jumps easy. Save full effort jumps for the main session.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Short 5 minute warm up',
      reason: 'Easy jog, leg swings, arm circles, and a few approach walk throughs when time is short.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Warm up without a band',
      reason: 'Replace band pull aparts with arm circles and wall slides when no band is available.',
    },
    otherSubstitutions: [
      { exerciseId: 'easy-jump-rope', name: 'Easy Jump Rope', reason: 'Two easy minutes of skipping can replace the opening jog.' },
    ],
    loadIncrement: 'none',
    visual: {
      diagram: {
        kind: 'court',
        caption:
          'Stations in order: 1 easy jog, 2 leg swings, 3 lunges with reach, 4 arm circles and band pull aparts, 5 skips, 6 shuffles, 7 approach steps, 8 easy jumps at the net.',
        steps: [
          { x: 1.2, y: 8.0 },
          { x: 4.5, y: 8.0 },
          { x: 7.8, y: 8.0 },
          { x: 7.8, y: 5.6 },
          { x: 4.5, y: 5.6 },
          { x: 1.2, y: 5.6 },
          { x: 2.6, y: 3.3 },
          { x: 4.5, y: 1.2 },
        ],
      },
    },
  },

  // ---------------------------------------------------------------- Volleyball Approach Jump
  {
    id: 'volleyball-approach-jump',
    name: 'Volleyball Approach Jump',
    aliases: ['Spike approach jump', 'Approach jump'],
    kind: 'jump',
    purpose:
      'Trains the full spike approach and takeoff so you turn running speed into height. This is the jump you use to attack.',
    equipment: ['Court or open floor with a firm surface', 'Optional net or a high target to reach for'],
    setup: [
      'Warm up fully first, including a few easy approaches.',
      'Mark a start spot about 4 to 5 metres from the net for a four step approach.',
      'Stand relaxed with your weight slightly forward and arms loose by your sides.',
      'Right handers start with the right foot. Left handers mirror every step.',
    ],
    steps: [
      'Take your first two steps to set your direction and build speed. Each step is a little longer and quicker.',
      'Take a long, low third step with the right foot and swing both arms back behind you.',
      'Plant the left foot quickly beside the right, heels first, feet about shoulder width apart.',
      'Swing both arms forward and up hard as you drive through the floor with both legs.',
      'Reach tall at the top with the hitting arm high.',
      'Land softly on both feet with the hips and knees bending, close to where you took off.',
    ],
    breathing: 'Breathe naturally on the approach. Many players breathe out sharply at takeoff. Take a few easy breaths between reps.',
    tempo:
      'Build speed through the approach, with the last two steps the quickest. Explosive takeoff, soft controlled landing, then walk back and rest 45 to 90 seconds before the next rep.',
    rangeOfMotion:
      'A quick dip to about a quarter or half squat at the plant, then full extension of the hips, knees, and ankles at takeoff. On landing, bend the hips and knees until the force is absorbed.',
    muscles: {
      primary: ['glute_max', 'quads'],
      secondary: ['gastrocnemius', 'soleus', 'hamstrings', 'obliques_core'],
    },
    emphasisNote:
      'The hips and knees drive the takeoff, so the glutes and quads carry most of the work, with the calves adding the final push. The core keeps the trunk stiff so force passes from the legs into the arm swing. This is power work counted as quality jump contacts, not muscle building sets.',
    movementPattern: 'jump',
    joints: ['Hip', 'Knee', 'Ankle', 'Shoulder'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['knee', 'achilles_calf', 'systemic'],
    commonMistakes: [
      'Slowing down before the last two steps. They should be the quickest.',
      'A late or small arm swing. The arms go back on the long step and forward as you plant.',
      'Jumping forward into the net instead of up.',
      'Knees caving inward at the plant or on landing.',
      'Landing on straight legs or on one foot.',
    ],
    goodFormFeels:
      'A rhythm that speeds up into a quick, low plant, then a snap upward where the arms and legs finish together. You land balanced and quiet.',
    stopRules: [
      'Quality first, never to failure. End the set as soon as jump height, approach speed, or landing control visibly drops.',
      'Stop for Achilles, shin, knee, or low back pain. Pain of 4 out of 10 or more, or pain that worsens or changes your technique, pauses this exercise. Tell a parent, coach, or clinician.',
      'Stop if your landings become loud or one sided, or your knees start to cave in.',
    ],
    safetyNotes: [
      'Learn the approach, jump, and landing with a qualified coach.',
      'Do the planned number of jumps. Do not add reps or sets on your own, even on a good day.',
      'Jump on a court or other surface with some give, in supportive shoes.',
    ],
    easierSubstitution: {
      exerciseId: 'countermovement-jump',
      name: 'Countermovement Jump',
      reason: 'Removes the run up so you can practise the dip, arm swing, and landing first.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Open floor approach jump',
      reason: 'Use any open gym floor with a clear run up when no net is available. Reach for an imaginary ball.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'volleyball-approach-footwork',
        name: 'Volleyball Approach Footwork',
        reason: 'Practise the step pattern without the jump on days with a jump limit.',
      },
    ],
    loadIncrement: 'none',
    visual: {
      poses: [
        {
          label: 'Plant',
          caption: 'Plant the last two steps quickly, heels first, with hips low and both arms swung back.',
          trunk: 138,
          armNear: [-72, -62],
          armFar: [-66, -56],
          legNear: [58, 5, 100],
          legFar: [46, -22, 95],
          footX: 118,
        },
        {
          label: 'Takeoff',
          caption: 'Swing the arms forward and up as the hips, knees, and ankles extend.',
          trunk: 168,
          armNear: [110, 125],
          armFar: [100, 118],
          legNear: [-8, -12, 25],
          legFar: [-4, -8, 30],
        },
        {
          label: 'Reach',
          caption: 'In the air, reach high with the hitting arm and keep the trunk tall.',
          trunk: 182,
          head: 195,
          armNear: [155, 165],
          armFar: [130, 145],
          legNear: [35, -75, -35],
          legFar: [42, -80, -40],
          lift: 10,
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Countermovement Jump
  {
    id: 'countermovement-jump',
    name: 'Countermovement Jump',
    aliases: ['CMJ', 'Standing vertical jump'],
    kind: 'jump',
    purpose:
      'Builds vertical jump power from a standing start. It teaches the quick dip, arm swing, and soft landing that every volleyball jump uses.',
    equipment: ['Firm, flat floor or court', 'Optional wall mark or target to reach for'],
    setup: [
      'Warm up fully first.',
      'Stand with your feet about hip width apart, toes forward or turned out slightly.',
      'Stand tall with your arms relaxed by your sides.',
      'Look straight ahead and brace your trunk lightly.',
    ],
    steps: [
      'Dip quickly by pushing the hips back and bending the knees to about a quarter or half squat.',
      'Swing both arms back behind you as you dip.',
      'Without pausing at the bottom, drive through the whole foot and jump straight up.',
      'Swing the arms forward and up hard and fully extend your hips, knees, and ankles.',
      'Land softly on the balls of your feet, then let the heels come down as the hips and knees bend.',
      'Stand up, reset your feet, and take a few breaths before the next rep.',
    ],
    breathing: 'Breathe in and brace before the dip. Breathe out as you jump or as you land. Breathe normally between reps.',
    tempo:
      'Fast dip, no pause at the bottom, explosive up, soft controlled landing. Full reset of 15 to 30 seconds between reps and about 2 minutes between sets.',
    rangeOfMotion:
      'Dip to a quarter or half squat, the depth you can reverse quickly. Finish fully extended with the arms high. On landing, bend the hips and knees until the landing feels controlled.',
    muscles: {
      primary: ['glute_max', 'quads'],
      secondary: ['gastrocnemius', 'soleus', 'hamstrings', 'obliques_core'],
    },
    emphasisNote:
      'The glutes and quads produce most of the force, and the calves add the last push through the ankles. The hamstrings help extend the hips and the core keeps the trunk stiff. This is power practice counted as jump contacts, not muscle building sets.',
    movementPattern: 'jump',
    joints: ['Hip', 'Knee', 'Ankle', 'Shoulder'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['knee', 'achilles_calf', 'systemic'],
    commonMistakes: [
      'Pausing at the bottom of the dip, which loses the spring.',
      'Dipping too deep and too slowly.',
      'Arms staying still or swinging out of time with the legs.',
      'Knees caving inward on takeoff or landing.',
      'Landing on straight legs or on the heels.',
    ],
    goodFormFeels:
      'One smooth, fast down and up. The arms and legs feel linked, you leave the floor tall and straight, and the landing is quiet.',
    stopRules: [
      'Quality first, never to failure. End the set as soon as jump height or landing control visibly drops.',
      'Stop for Achilles, shin, knee, or low back pain. Pain of 4 out of 10 or more, or pain that worsens or changes your technique, pauses this exercise. Tell a parent, coach, or clinician.',
      'Stop if landings get loud, you land off balance, or your knees start to cave in.',
    ],
    safetyNotes: [
      'Learn the jump and landing with a qualified coach.',
      'Do the planned number of jumps. Do not add reps or sets on your own.',
      'Jump on a surface with some give, in supportive shoes.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Snap down and stick',
      reason: 'Drop quickly into the landing position and hold it. Teaches a controlled landing before you jump for height.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Countermovement jump on flat grass',
      reason: 'Use a flat grass area when no gym floor is free.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'volleyball-approach-jump',
        name: 'Volleyball Approach Jump',
        reason: 'Adds the run up once the standing jump and landing are solid.',
      },
    ],
    loadIncrement: 'none',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Stand tall, feet about hip width apart, arms relaxed by your sides.',
          trunk: 178,
          armNear: [6, 4],
          armFar: [3, 2],
          legNear: [0, 0],
          legFar: [2, -2],
        },
        {
          label: 'Dip',
          caption: 'Push the hips back, bend the knees, and swing both arms back.',
          trunk: 145,
          armNear: [-60, -50],
          armFar: [-55, -45],
          legNear: [55, -30],
          legFar: [52, -32],
          props: [{ type: 'arrow', from: [160, 70], to: [160, 105] }],
        },
        {
          label: 'Jump',
          caption: 'Drive straight up with the arms swinging forward and up, toes pointed.',
          trunk: 177,
          armNear: [118, 132],
          armFar: [112, 126],
          legNear: [18, -48, -10],
          legFar: [24, -52, -14],
          lift: 10,
          props: [{ type: 'arrow', from: [160, 110], to: [160, 70] }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Volleyball Approach Footwork
  {
    id: 'volleyball-approach-footwork',
    name: 'Volleyball Approach Footwork',
    aliases: ['Approach steps', 'Spike approach footwork'],
    kind: 'skill',
    purpose:
      'Grooves the step pattern and rhythm of the spike approach without a full jump, so the footwork becomes automatic and your takeoff spot is consistent.',
    equipment: ['Court or open floor', 'Optional tape or cones to mark the start'],
    setup: [
      'Start about 4 to 5 metres from the net for a four step approach, or about 3 to 4 metres for three steps.',
      'Right handers use right, left, right, left for four steps, or left, right, left for three steps. Left handers mirror this.',
      'Stand relaxed with your weight slightly forward and arms loose.',
      'Mark your start spot so every rep begins in the same place.',
    ],
    steps: [
      'Walk the pattern slowly first and say the steps out loud.',
      'Take a short first step to set your direction, then a slightly longer second step.',
      'Make the third step long and low, a big right step for right handers, with both arms swinging back.',
      'Close quickly with the left foot so it lands just ahead of the right, heels first, feet about shoulder width apart.',
      'Stop in the loaded position with the arms back, or finish with a small hop, then walk back.',
      'Move from walking to jogging to about three quarter speed only while the pattern stays clean.',
    ],
    breathing: 'Breathe naturally and stay relaxed between reps.',
    tempo: 'Slow to fast rhythm. The first steps are calm and the last two are the quickest. Walk back to the start to reset between reps.',
    rangeOfMotion:
      'Steps grow longer toward the net. The third step is the longest, with the hips low, and the plant finishes in about a quarter squat.',
    muscles: {
      primary: ['quads', 'glute_max'],
      secondary: ['gastrocnemius', 'soleus', 'hamstrings'],
    },
    emphasisNote:
      'This is coordination practice. The legs work lightly, with the quads and glutes loading at the plant and the calves driving each step. Count it as skill practice, not muscle building work.',
    movementPattern: 'locomotion',
    joints: ['Ankle', 'Knee', 'Hip'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['knee', 'achilles_calf'],
    commonMistakes: [
      'Starting on the wrong foot, which leaves you planting on the wrong side.',
      'Taking steps all the same length instead of building longer and quicker.',
      'Slowing down or stuttering before the last two steps.',
      'Planting with the feet too close together or one directly behind the other.',
      'Arms swinging late or staying in front of the body.',
    ],
    goodFormFeels:
      'A rhythm that builds, slow, quicker, then a fast right left plant. You arrive balanced in a low, loaded position with the arms back and ready to swing.',
    stopRules: [
      'Stop when the pattern gets sloppy or you start mixing up the feet. Rest, then restart slowly.',
      'Stop for pain of 4 out of 10 or more, or pain that worsens or changes your steps, and tell a parent, coach, or clinician.',
    ],
    safetyNotes: [
      'Learn the approach with a qualified coach so the pattern you repeat is correct.',
      'Keep reps crisp and stop before you get tired. This is practice, not conditioning.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Two step approach',
      reason: 'Only the last two steps, right then left for right handers, so you can learn the plant first.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Approach footwork on any open floor',
      reason: 'Tape a start mark and a plant mark on any floor when no court is free.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'volleyball-approach-jump',
        name: 'Volleyball Approach Jump',
        reason: 'Adds the jump once the footwork is automatic.',
      },
    ],
    loadIncrement: 'none',
    visual: {
      diagram: {
        kind: 'court',
        caption:
          'Right handed four step approach from above: 1 short right, 2 left, 3 long right, 4 quick left plant. For three steps, drop step 1. Left handers mirror it.',
        steps: [
          { x: 5.8, y: 5.5, label: '1R' },
          { x: 5.0, y: 4.5, label: '2L' },
          { x: 5.5, y: 3.1, label: '3R' },
          { x: 4.5, y: 2.2, label: '4L' },
        ],
        ball: { x: 4.7, y: 0.8 },
        markers: [{ x: 6.4, y: 6.5, label: 'Start' }],
      },
    },
  },

  // ---------------------------------------------------------------- Shuffle to Sprint
  {
    id: 'shuffle-to-sprint',
    name: 'Shuffle to Sprint',
    aliases: ['Shuffle and go', 'Lateral shuffle to sprint'],
    kind: 'sprint',
    purpose:
      'Trains the quick change from moving sideways to sprinting, like covering the court after a block or chasing a ball that has been deflected.',
    equipment: ['Court or open floor with about 12 metres of space', 'Two or three cones or tape marks'],
    setup: [
      'Warm up fully before the first rep.',
      'Mark a start line, a cone about 3 metres along, and a finish line 10 metres from the start.',
      'Stand side on at the start line in a low athletic stance, feet a little wider than your shoulders.',
      'Face across the lane so the finish line is to your side.',
    ],
    steps: [
      'Shuffle sideways for three quick steps toward the cone without crossing or clicking your feet together.',
      'Stay low with the chest up and the hips level.',
      'At the cone, push hard off the trailing leg, turn your hips toward the finish, and drive through with a crossover step.',
      'Sprint through the finish line, leaning forward for the first few steps.',
      'Slow down gradually after the line, then walk back.',
      'Rest fully, then repeat facing the other way so you shuffle in the other direction.',
    ],
    breathing: 'Breathe in before you start and breathe freely as you sprint. Let your breathing settle fully before the next rep.',
    tempo: 'Quick, low shuffle, sharp turn, explosive sprint. Full recovery of 60 to 90 seconds between reps.',
    rangeOfMotion:
      'Short, quick shuffle steps with the feet about shoulder width apart. The turn is a full hip turn to face the finish, and the sprint builds to a full stride.',
    muscles: {
      primary: ['glute_max', 'glute_med', 'quads'],
      secondary: ['adductors', 'hamstrings', 'gastrocnemius', 'soleus', 'obliques_core'],
    },
    emphasisNote:
      'The glutes and quads drive the push off and the sprint. The side hip muscles and inner thighs work hard to push and control the shuffle and the turn. This is speed work counted as quality sprint reps, not muscle building sets.',
    movementPattern: 'change_of_direction',
    joints: ['Hip', 'Knee', 'Ankle'],
    laterality: 'alternating',
    logSides: true,
    fatigueOverlap: ['hamstring', 'hip', 'achilles_calf', 'knee', 'systemic'],
    commonMistakes: [
      'Standing up tall during the shuffle.',
      'Crossing or clicking the feet together while shuffling.',
      'Rounding the turn with several small stutter steps instead of one sharp push.',
      'Popping up tall in the first sprint steps instead of staying low and driving.',
      'Starting the next rep before you have recovered.',
    ],
    goodFormFeels: 'Low and quick in the shuffle, then a sharp, powerful push into the sprint. You feel fast, not tired.',
    stopRules: [
      'Quality first, never to failure. End the set as soon as your speed, turn, or footwork visibly declines.',
      'Stop at once for a sharp or pulling feeling in the hamstring, groin, or calf. Pain of 4 out of 10 or more, or pain that worsens or changes how you move, pauses this exercise. Tell a parent, coach, or clinician.',
      'Stop if you slip or cannot keep your footing on the surface.',
    ],
    safetyNotes: [
      'Warm up fully and use a floor that is not slippery, in good shoes.',
      'Rest fully between reps. This is speed training, not conditioning. Do not add reps on your own.',
      'Learn the turn and sprint start with a qualified coach.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Shuffle to jog',
      reason: 'The same pattern at lower speed while you learn the turn.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Shuffle to sprint on grass or a track',
      reason: 'Any flat surface with grip and about 12 metres of space works. Use shoes or lines as markers.',
    },
    otherSubstitutions: [
      { exerciseId: 'ten-metre-sprint', name: 'Ten Metre Sprint', reason: 'Straight line speed without the change of direction.' },
    ],
    loadIncrement: 'none',
    visual: {
      diagram: {
        kind: 'lane',
        caption:
          'Start side on at 1. Shuffle through 2 to the cone at 3, turn your hips, and sprint through the 10 m line to F. Repeat facing the other way.',
        steps: [
          { x: 0.5, y: 0, label: '1' },
          { x: 2.0, y: 0, label: '2' },
          { x: 3.5, y: 0, label: '3' },
          { x: 10.4, y: 0, label: 'F' },
        ],
        markers: [{ x: 3.5, y: 1.4, label: 'Cone' }],
      },
    },
  },

  // ---------------------------------------------------------------- Medicine Ball Spike Throw
  {
    id: 'medicine-ball-spike-throw',
    name: 'Medicine Ball Spike Throw',
    aliases: ['Overhead medicine ball slam', 'Medicine ball slam'],
    kind: 'throw',
    purpose:
      'Trains fast, coordinated force from the legs through the trunk into the arms, the same chain you use to spike. A light ball keeps the focus on speed.',
    equipment: ['Light medicine ball or slam ball, about 2 to 3 kg', 'Open floor, or a solid wall for the wall version'],
    setup: [
      'Use a light ball of about 2 to 3 kg. For floor throws, choose one that does not bounce high.',
      'Clear the space around you and check nobody is in front of you.',
      'Stand with your feet about shoulder width apart and knees soft.',
      'Hold the ball with both hands at your chest.',
    ],
    steps: [
      'Lift the ball overhead and slightly behind your head, rising tall without arching your lower back.',
      'Snap your trunk forward and pull the ball down with long, nearly straight arms, like the swing of a spike.',
      'Throw the ball hard into the floor just in front of your feet, bending your hips and knees as you release.',
      'For the wall version, stand 1 to 2 metres from a solid wall and throw down and forward at a spot low on the wall.',
      'Let the ball settle, pick it up with a flat back, and reset before the next throw.',
    ],
    breathing: 'Breathe in as you lift the ball. Breathe out forcefully as you throw.',
    tempo: 'Controlled lift, fast and explosive throw, then a full reset of 15 to 30 seconds before the next rep. Quality, not fatigue.',
    rangeOfMotion:
      'From the ball overhead to release at about knee height as the hips and knees bend. The trunk moves from tall to a strong forward bend.',
    muscles: {
      primary: ['lats', 'rectus_abdominis', 'obliques_core'],
      secondary: ['pec_sternal', 'triceps', 'teres_major', 'rotator_cuff', 'serratus_anterior'],
    },
    emphasisNote:
      'The lats and the trunk flexors do most of the work, pulling the ball from overhead down and forward. The chest, triceps, serratus, and shoulder rotators help, much as they do in a spike. Treat it as power practice counted in throws, not as muscle building sets.',
    movementPattern: 'throw',
    joints: ['Shoulder', 'Elbow', 'Spine', 'Hip', 'Knee'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder', 'low_back'],
    commonMistakes: [
      'Using a ball so heavy that the throw becomes slow.',
      'Arching the lower back hard at the top.',
      'Throwing only with the arms, without the trunk snapping forward.',
      'Picking the ball up with a rounded back. Squat down to lift it.',
      'Throwing at an angle that sends the ball back toward your face.',
    ],
    goodFormFeels:
      'A fast, whole body snap. The power starts at the hips and trunk and finishes through the arms, and the ball hits the floor with a crisp sound.',
    stopRules: [
      'Quality first, never to failure. End the set as soon as throw speed or coordination visibly drops.',
      'Stop for shoulder, elbow, or low back pain. Pain of 4 out of 10 or more, or pain that worsens or changes your throw, pauses this exercise. Tell a parent, coach, or clinician.',
    ],
    safetyNotes: [
      'Use a light ball, about 2 to 3 kg. Do not move to a heavier ball on your own or add throws beyond the plan.',
      'Use a ball made for floor throws and keep your face clear of the bounce.',
      'Learn the throw with a qualified coach.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Tall kneeling medicine ball throw',
      reason: 'Kneeling takes the legs out so you can learn the trunk and arm snap.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Volleyball slam into the floor',
      reason: 'Use a volleyball when no medicine ball is available and focus on the same fast trunk and arm snap.',
    },
    otherSubstitutions: [
      {
        exerciseId: null,
        name: 'Medicine ball wall throw',
        reason: 'Throw down and forward at a low spot on a solid wall when floor throws are not allowed.',
      },
    ],
    loadIncrement: 'none',
    visual: {
      poses: [
        {
          label: 'Overhead',
          caption: 'Lift the ball overhead and slightly behind your head without arching the lower back.',
          trunk: 186,
          head: 182,
          armNear: [150, 235],
          armFar: [146, 230],
          legNear: [28, -28],
          legFar: [30, -26],
          props: [{ type: 'ball', at: 'hands', r: 8 }],
        },
        {
          label: 'Snap',
          caption: 'Snap the trunk forward and pull the ball down with long arms.',
          trunk: 158,
          armNear: [135, 128],
          armFar: [131, 124],
          legNear: [30, -22],
          legFar: [32, -20],
          props: [
            { type: 'ball', at: 'hands', r: 8 },
            { type: 'arrow', from: [170, 26], to: [176, 66] },
          ],
        },
        {
          label: 'Release',
          caption: 'Release the ball hard into the floor just in front of your feet as the hips and knees bend.',
          trunk: 118,
          armNear: [40, 25],
          armFar: [36, 20],
          legNear: [55, -30],
          legFar: [52, -32],
          props: [
            { type: 'ball', at: 'hands', r: 8 },
            { type: 'arrow', from: [160, 146], to: [166, 167] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Volleyball Spike
  {
    id: 'volleyball-spike',
    name: 'Volleyball Spike',
    aliases: ['Attack hit', 'Spike'],
    kind: 'skill',
    purpose:
      'Practises the full attack, from approach and jump to arm swing and contact, so you hit hard and consistently.',
    equipment: ['Court and net at the height for your age group', 'Volleyballs', 'A setter, coach, or tosser'],
    setup: [
      'Warm up fully, including arm circles, band work, and easy approach jumps.',
      'Set the net at the height used in your age group.',
      'Start your approach about 4 to 5 metres from the net, or closer for a three step approach.',
      'Agree with the setter or tosser where the ball will go.',
    ],
    steps: [
      'Read the set and start your approach, with the last two steps the quickest.',
      'Swing both arms back on the long step, then forward and up as you plant and jump.',
      'In the air, lift the non hitting arm toward the ball and draw the hitting elbow back and high, like pulling a bow.',
      'Swing the hitting arm forward and up, leading with the elbow, and contact the ball high and in front of your hitting shoulder.',
      'Snap the wrist over the ball, then let the arm follow through down and across your body.',
      'Land on both feet with the hips and knees bent, without touching the net.',
    ],
    breathing: 'Breathe naturally on the approach. Breathe out sharply as you swing. Take a few breaths between reps.',
    tempo: 'Accelerating approach, explosive jump and swing, soft controlled landing, then a full reset of 30 to 60 seconds between reps.',
    rangeOfMotion:
      'A full arm swing from the elbow high behind you, to reaching as high as you can at contact, then a relaxed follow through past the hip. Full hip, knee, and ankle extension on takeoff.',
    muscles: {
      primary: ['lats', 'pec_sternal', 'glute_max', 'quads'],
      secondary: ['serratus_anterior', 'triceps', 'rotator_cuff', 'delt_anterior', 'obliques_core', 'gastrocnemius', 'hamstrings'],
    },
    emphasisNote:
      'The legs produce the jump, the trunk links the jump to the swing, and the lats and chest drive the arm through contact with help from the triceps, serratus, and shoulder muscles. The rotator cuff works hard to slow the arm after contact. This is skill practice counted as spike reps, not muscle building sets.',
    movementPattern: 'overhead_strike',
    joints: ['Shoulder', 'Elbow', 'Wrist', 'Spine', 'Hip', 'Knee', 'Ankle'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder', 'elbow', 'knee', 'achilles_calf', 'low_back', 'systemic'],
    commonMistakes: [
      'Dropping the hitting elbow below shoulder height during the swing.',
      'Contacting the ball behind your head or too far out to the side.',
      'Jumping forward into the net instead of up.',
      'Swinging only with the arm, without the trunk turning and bending first.',
      'Landing on one foot or on straight legs.',
    ],
    goodFormFeels:
      'A whip that starts in the trunk and finishes at the hand. Contact feels high, in front, and clean, and you land balanced on two feet.',
    stopRules: [
      'Quality first, never to failure. End the set as soon as jump height, arm speed, or contact quality visibly drops.',
      'Stop for shoulder, elbow, knee, Achilles, shin, or back pain. Pain of 4 out of 10 or more, or pain that worsens or changes your technique, pauses spiking. Tell a parent, coach, or clinician.',
      'Stop if your hitting shoulder feels tired, heavy, or loose.',
    ],
    safetyNotes: [
      'Learn spiking and landing with a qualified coach.',
      'Hit only the planned number of balls. Add reps only when your coach or plan says so.',
      'Land on your own side of the net and watch for players underneath it.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Standing wall spike',
      reason: 'Hit a ball into the floor so it bounces off a wall, from standing, to groove the arm swing without jumping.',
    },
    equipmentSubstitution: {
      exerciseId: 'medicine-ball-spike-throw',
      name: 'Medicine Ball Spike Throw',
      reason: 'Trains the same trunk and arm chain when no net or setter is available.',
    },
    otherSubstitutions: [
      {
        exerciseId: 'volleyball-approach-jump',
        name: 'Volleyball Approach Jump',
        reason: 'Keeps the approach and jump when the shoulder needs a rest from hitting.',
      },
    ],
    loadIncrement: 'none',
    visual: {
      poses: [
        {
          label: 'Arm back',
          caption: 'In the air, point the non hitting arm at the ball and draw the hitting elbow back and high.',
          trunk: 192,
          head: 185,
          armNear: [250, 175],
          armFar: [135, 150],
          legNear: [20, -70, -35],
          legFar: [30, -75, -40],
          lift: 12,
          footX: 88,
          props: [
            { type: 'net', x: 178 },
            { type: 'ball', at: [156, 14], r: 7 },
          ],
        },
        {
          label: 'Contact',
          caption: 'Swing up and contact the ball high and in front of the hitting shoulder.',
          trunk: 174,
          armNear: [160, 165],
          armFar: [35, 15],
          legNear: [35, -82, -42],
          legFar: [42, -76, -36],
          lift: 6,
          footX: 108,
          props: [
            { type: 'net', x: 178 },
            { type: 'ball', at: 'nearHand', r: 7 },
          ],
        },
        {
          label: 'Land',
          caption: 'Follow through down past the hip and land on both feet with bent knees.',
          trunk: 148,
          armNear: [40, 15],
          armFar: [30, 10],
          legNear: [48, -28],
          legFar: [44, -30],
          footX: 110,
          props: [{ type: 'net', x: 178 }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Lateral Block Jump
  {
    id: 'lateral-block-jump',
    name: 'Lateral Block Jump',
    aliases: ['Block move and jump', 'Step close block jump'],
    kind: 'jump',
    purpose:
      'Trains the quick sideways move along the net and a controlled jump to block, then a balanced landing ready for the next play.',
    equipment: ['Court and net at the height for your age group', 'Optional tape marks along the net'],
    setup: [
      'Stand facing the net, close enough to reach over it without touching, about half an arm length away.',
      'Place your feet about shoulder width apart with knees bent and weight on the balls of your feet.',
      'Hold your hands up at shoulder height in front of you, palms facing the net.',
      'Mark a spot 1 to 2 metres to the side where you will jump.',
    ],
    steps: [
      'Step sideways toward the mark with the lead foot, keeping your hips and shoulders square to the net.',
      'Close the trailing foot so your feet are square to the net and shoulder width apart.',
      'Stop your sideways movement, dip quickly, and jump straight up.',
      'Press both hands up and over the net with fingers spread and thumbs up.',
      'Pull your hands back and land softly on both feet on the same spot, without drifting sideways.',
      'Reset and repeat to the other side.',
    ],
    breathing: 'Breathe naturally. Breathe out as you jump.',
    tempo: 'Quick side step, sharp stop, explosive jump, soft controlled landing, then a full reset of 20 to 40 seconds between reps.',
    rangeOfMotion:
      'A side step of 1 to 2 metres, a quick dip to about a quarter squat, full extension on takeoff, and arms reaching fully up and over the net.',
    muscles: {
      primary: ['quads', 'glute_max'],
      secondary: ['glute_med', 'adductors', 'gastrocnemius', 'soleus', 'obliques_core'],
    },
    emphasisNote:
      'The quads and glutes drive the jump and absorb the landing. The side hip muscles and inner thighs start and stop the sideways step, and the calves finish the takeoff. This is power practice counted as jump contacts, not muscle building sets.',
    movementPattern: 'jump',
    joints: ['Hip', 'Knee', 'Ankle', 'Shoulder'],
    laterality: 'alternating',
    logSides: true,
    fatigueOverlap: ['knee', 'achilles_calf', 'hip', 'systemic'],
    commonMistakes: [
      'Drifting sideways during the jump instead of stopping first and going straight up.',
      'Crossing the feet or letting them click together on the step.',
      'Swinging the arms wide instead of pressing them straight up and over.',
      'Touching the net with your hands or body.',
      'Knees caving inward on landing.',
    ],
    goodFormFeels:
      'A quick step and a sharp stop, then a jump straight up with your hands already high. You land on the same spot, balanced and ready to move again.',
    stopRules: [
      'Quality first, never to failure. End the set as soon as jump height, footwork, or landing control visibly drops.',
      'Stop for Achilles, shin, knee, or shoulder pain. Pain of 4 out of 10 or more, or pain that worsens or changes your technique, pauses this exercise. Tell a parent, coach, or clinician.',
      'Stop if you land off balance or drift into the net.',
    ],
    safetyNotes: [
      'Learn blocking footwork and landing with a qualified coach.',
      'Do the planned number of jumps. Do not add reps or sets on your own.',
      'Watch for players under the net and land on your own side.',
    ],
    easierSubstitution: {
      exerciseId: 'countermovement-jump',
      name: 'Countermovement Jump',
      reason: 'Practise the vertical jump and landing without the side step first.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Lateral block jump along a line',
      reason: 'Use a floor line as the net when no court is free. Reach straight up with the hands.',
    },
    otherSubstitutions: [
      {
        exerciseId: null,
        name: 'Side step and stick',
        reason: 'Step, close, and stop in the blocking stance without jumping to learn the stop.',
      },
    ],
    loadIncrement: 'none',
    visual: {
      diagram: {
        kind: 'court',
        caption:
          'From above, along the net. Start square to the net at S, step and close to the right, jump at J, and land on the same spot. Repeat to the left.',
        steps: [
          { x: 3.4, y: 0.9, label: 'S' },
          { x: 5.4, y: 0.9, label: 'J' },
        ],
      },
    },
  },

  // ---------------------------------------------------------------- Block to Spike Transition
  {
    id: 'block-to-spike-transition',
    name: 'Block to Spike Transition',
    aliases: ['Transition attack', 'Block and transition'],
    kind: 'skill',
    purpose:
      'Links a block at the net with getting off the net and attacking, the sequence front row players repeat all match.',
    equipment: ['Court and net at the height for your age group', 'Volleyballs', 'A coach or setter to set the ball'],
    setup: [
      'Warm up fully, including easy blocks and approach jumps.',
      'Start in your blocking stance at the net in your usual front row spot.',
      'Have the setter ready near the net to set you after you land.',
      'Know your transition spot, about 3 to 4 metres off the net, where your approach will start.',
    ],
    steps: [
      'Jump and block, pressing your hands over the net.',
      'Land softly on both feet and find the ball.',
      'Turn to face the court and move quickly off the net with a few running steps to your transition spot.',
      'Stop balanced and face the setter, then start your approach as the ball is set.',
      'Approach, jump, and hit, then land on both feet.',
      'Walk back to the net and rest fully before the next rep.',
    ],
    breathing: 'Breathe naturally. Breathe out on each jump and on the swing. Let your breathing settle before the next rep.',
    tempo:
      'Explosive block, quick move off the net, controlled stop, accelerating approach and spike, soft landings. Full reset of 60 to 90 seconds between reps.',
    rangeOfMotion:
      'Two full jumps per rep: a block jump with the arms reaching over the net, and an approach jump with a full arm swing. The move off the net covers about 3 to 4 metres.',
    muscles: {
      primary: ['glute_max', 'quads'],
      secondary: [
        'hamstrings',
        'glute_med',
        'gastrocnemius',
        'soleus',
        'obliques_core',
        'lats',
        'pec_sternal',
        'delt_anterior',
        'rotator_cuff',
        'serratus_anterior',
      ],
    },
    emphasisNote:
      'The legs do most of the work across two jumps and the quick move off the net. The trunk and shoulder muscles work in both the block and the spike. This is skill practice counted as jump contacts and spike reps, not muscle building sets.',
    movementPattern: 'jump',
    joints: ['Hip', 'Knee', 'Ankle', 'Shoulder', 'Elbow', 'Spine'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['knee', 'achilles_calf', 'shoulder', 'systemic'],
    commonMistakes: [
      'Turning away from the ball when you leave the net, so you lose sight of the play.',
      'Backpedalling slowly instead of turning and running off the net.',
      'Not getting far enough off the net, so the approach is cramped.',
      'Starting the approach before you have stopped and set your feet.',
      'Landing from the block off balance, which delays everything after it.',
    ],
    goodFormFeels:
      'Land, turn, go. You arrive at your spot early and balanced, with time to read the set and a full approach ahead of you.',
    stopRules: [
      'Quality first, never to failure. End the set as soon as jump height, speed off the net, or landing control visibly drops.',
      'Stop for shoulder, knee, Achilles, shin, or back pain. Pain of 4 out of 10 or more, or pain that worsens or changes your technique, pauses this drill. Tell a parent, coach, or clinician.',
      'Stop if your approach becomes cramped or rushed because you are tired.',
    ],
    safetyNotes: [
      'Learn transition footwork, blocking, and landing with a qualified coach.',
      'Do only the planned reps. Each rep has two jumps, so it counts twice toward your jump total.',
      'Watch for players under the net and land on your own side.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Walk through transition',
      reason: 'Walk the block, turn, and approach route without jumping to learn the path.',
    },
    equipmentSubstitution: {
      exerciseId: 'volleyball-approach-footwork',
      name: 'Volleyball Approach Footwork',
      reason: 'Practise moving off a floor line into your approach when no net or setter is available.',
    },
    otherSubstitutions: [
      { exerciseId: 'lateral-block-jump', name: 'Lateral Block Jump', reason: 'Trains the blocking half on its own.' },
    ],
    loadIncrement: 'none',
    visual: {
      diagram: {
        kind: 'court',
        caption:
          'Block at B, turn and move off the net through 1 to your spot at 2, about 3.5 to 4 m back, then take a left, right, left approach and hit the set.',
        steps: [
          { x: 3.0, y: 0.5, label: 'B' },
          { x: 2.0, y: 2.1, label: '1' },
          { x: 1.2, y: 3.9, label: '2' },
          { x: 2.4, y: 3.2, label: 'L' },
          { x: 3.6, y: 2.1, label: 'R' },
          { x: 4.4, y: 1.0, label: 'L' },
        ],
        ball: { x: 5.1, y: 0.5 },
        markers: [{ x: 6.9, y: 1.0, label: 'Setter' }],
      },
    },
  },

  // ---------------------------------------------------------------- Ten Metre Sprint
  {
    id: 'ten-metre-sprint',
    name: 'Ten Metre Sprint',
    aliases: ['10 m sprint', 'Acceleration sprint'],
    kind: 'sprint',
    purpose: 'Builds acceleration, the first few fast steps you use to chase a ball or get to your spot on the court.',
    equipment: ['Flat floor or track with grip and about 20 metres of space', 'Two cones or tape lines 10 metres apart'],
    setup: [
      'Warm up fully, including a few gradual build up runs.',
      'Mark a start line and a finish line 10 metres apart, with room to slow down after it.',
      'Take a split stance with the front foot just behind the line and the back foot about a foot length behind.',
      'Lean forward slightly with your weight on the front foot and the opposite arm forward.',
    ],
    steps: [
      'Push hard through the front foot and drive the back knee forward to start.',
      'Stay leaning forward for the first few steps and push the ground back behind you.',
      'Drive the arms strongly forward and back from the shoulders with the elbows bent.',
      'Rise gradually to an upright running position by about 8 to 10 metres.',
      'Sprint through the finish line, not to it, then slow down gradually.',
      'Walk back and rest fully before the next rep.',
    ],
    breathing: 'Take a breath before you start. Breathe freely during the sprint and let your breathing settle fully before the next rep.',
    tempo: 'Maximal intent from the first step. Each rep lasts about 2 seconds. Full recovery of 1 to 2 minutes between reps.',
    rangeOfMotion:
      'Short, powerful steps that lengthen gradually. The back leg fully extends on each push and the front knee drives forward strongly.',
    muscles: {
      primary: ['glute_max', 'quads', 'hamstrings'],
      secondary: ['gastrocnemius', 'soleus', 'hip_flexors', 'obliques_core'],
    },
    emphasisNote:
      'Acceleration leans heavily on the glutes and quads to push the ground back, with the hamstrings and calves helping every step and the hip flexors driving the knee forward. This is speed work counted as quality sprint reps, not muscle building sets.',
    movementPattern: 'sprint',
    joints: ['Hip', 'Knee', 'Ankle', 'Shoulder'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['hamstring', 'achilles_calf', 'hip', 'systemic'],
    commonMistakes: [
      'Standing up tall on the first step.',
      'Reaching forward with the feet so they land in front of your hips.',
      'Arms swinging across the body instead of forward and back.',
      'Tensing the face, neck, and shoulders.',
      'Starting the next rep before you have recovered.',
    ],
    goodFormFeels:
      'Powerful pushes into the ground, a forward lean that rises smoothly, and speed that builds with every step.',
    stopRules: [
      'Quality first, never to failure. End the set as soon as your speed or form visibly drops.',
      'Stop at once for a sharp, pulling, or cramping feeling in the hamstring, calf, or groin. Pain of 4 out of 10 or more, or pain that worsens or changes how you run, pauses sprinting. Tell a parent, coach, or clinician.',
      'Stop if you slip or the surface feels unsafe.',
    ],
    safetyNotes: [
      'Warm up fully. Never sprint cold.',
      'Keep the planned reps and full rest. Do not add reps on your own.',
      'Learn the start position and acceleration with a qualified coach.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Build up run',
      reason: 'Accelerate smoothly to about 80 percent speed over 20 metres to learn the lean and arm action.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Ten metre sprint on grass',
      reason: 'Use a flat grass area if the gym floor is busy or slippery.',
    },
    otherSubstitutions: [
      { exerciseId: 'shuffle-to-sprint', name: 'Shuffle to Sprint', reason: 'Adds a sideways start that matches court movement.' },
    ],
    loadIncrement: 'none',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Split stance, front foot at the line, slight forward lean, opposite arm forward.',
          trunk: 140,
          head: 125,
          armNear: [-45, 10],
          armFar: [40, 110],
          legNear: [30, -12, 90],
          legFar: [-30, -35, 60],
        },
        {
          label: 'Drive',
          caption: 'Push the ground back with the rear leg fully extended and drive the front knee forward.',
          trunk: 135,
          head: 125,
          armNear: [-55, -5],
          armFar: [65, 150],
          legNear: [80, 15, 100],
          legFar: [-38, -38, 40],
          footX: 128,
        },
        {
          label: 'Upright',
          caption: 'By about 8 to 10 metres, run tall with high knees and strong arms.',
          trunk: 176,
          armNear: [45, 135],
          armFar: [-45, 40],
          legNear: [-4, -6, 90],
          legFar: [82, 5, 100],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Easy Moderate Pool Round Trip
  {
    id: 'easy-pool-round-trip',
    name: 'Easy Moderate Pool Round Trip',
    aliases: ['Easy swim', 'Pool recovery swim'],
    kind: 'swim',
    purpose:
      'Easy aerobic exercise in the water that adds activity with almost no impact on the legs. One round trip means swimming to the far wall and back.',
    equipment: ['Swimming pool with a lane you can use', 'Swimsuit and goggles', 'A lifeguard or supervising adult present'],
    setup: [
      'Swim only where a lifeguard or supervising adult is present.',
      'Plan at least 3 hours between swimming and your main workout.',
      'Pool lengths vary, so count round trips, not metres.',
      'Start in the water at the start wall of your lane.',
    ],
    steps: [
      'Push off the start wall gently and settle into a stroke you know well.',
      'Swim at a relaxed, conversational pace, about 4 to 5 out of 10 effort.',
      'At the far wall, touch or turn and swim back to the start wall. That is one round trip.',
      'Rest at the wall as long as you need before the next round trip.',
      'Change strokes if you like, keeping the same easy effort.',
    ],
    breathing:
      'Breathe rhythmically. In freestyle, breathe out steadily underwater and turn to breathe in every 2 or 3 strokes. You should never feel out of breath.',
    tempo: 'Easy, steady pace at 4 to 5 out of 10 effort. You could say a short sentence at each wall.',
    rangeOfMotion: 'Long, relaxed strokes through a comfortable shoulder range with a gentle, steady kick. Do not force the reach.',
    muscles: {
      primary: ['lats', 'pec_sternal', 'delt_anterior'],
      secondary: ['delt_lateral', 'rotator_cuff', 'triceps', 'obliques_core', 'hip_flexors', 'glute_max', 'quads'],
    },
    emphasisNote:
      'Freestyle biases the lats, chest, and shoulders, with the triceps finishing each pull and the trunk, hips, and legs keeping you long in the water. At this easy effort it is aerobic exposure, not muscle building work.',
    movementPattern: 'swim',
    joints: ['Shoulder', 'Elbow', 'Spine', 'Hip', 'Knee', 'Ankle'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['shoulder', 'systemic'],
    commonMistakes: [
      'Swimming too hard because you feel fresh.',
      'Holding your breath instead of breathing out underwater.',
      'Lifting the head high to breathe, which drops the hips.',
      'Counting lengths instead of round trips.',
    ],
    goodFormFeels:
      'Relaxed and smooth. Your breathing is steady, your shoulders move freely, and you finish feeling better than when you started.',
    stopRules: [
      'Stop and get out of the water for chest pain, unusual breathlessness, or dizziness. Tell the lifeguard and a parent right away.',
      'Stop for shoulder pain. Pain of 4 out of 10 or more, or pain that worsens or changes your stroke, pauses swimming. Tell a parent, coach, or clinician.',
      'Stop if you feel cold, shivery, or very tired.',
    ],
    safetyNotes: [
      'Never swim alone. Swim only with a lifeguard or supervising adult present.',
      'Keep at least 3 hours between swimming and your main workout.',
      'Pool length varies. Never assume a distance, count round trips.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Pool walking or easy kicking with a board',
      reason: 'Keeps you moving in the water with less work for the shoulders.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Easy cycling or a brisk walk',
      reason: 'Low impact aerobic work when no pool is available. Keep the same easy effort.',
    },
    otherSubstitutions: [
      { exerciseId: 'easy-jump-rope', name: 'Easy Jump Rope', reason: 'Short easy conditioning at home, only on days the calves and shins feel fresh.' },
    ],
    loadIncrement: 'none',
    visual: {
      diagram: {
        kind: 'pool',
        caption:
          'One round trip: push off the start wall (S), swim to the far wall and turn (T), and swim back to the start wall (F). Pool length varies.',
        steps: [
          { x: 1, y: 3, label: 'S' },
          { x: 24, y: 3, label: 'T' },
          { x: 1, y: 5.2, label: 'F' },
        ],
        markers: [{ x: 1.4, y: 9.2, label: 'Start' }],
      },
    },
  },

  // ---------------------------------------------------------------- Pallof Press
  {
    id: 'pallof-press',
    name: 'Pallof Press',
    aliases: ['Cable anti rotation press', 'Pallof hold'],
    kind: 'strength',
    purpose:
      'Trains your trunk to resist twisting, which helps you stay stable when you land, block, or swing at the ball.',
    equipment: ['Cable machine with a single handle', 'Or a resistance band anchored at chest height'],
    setup: [
      'Set the pulley at chest height and attach a single handle.',
      'Stand side on to the machine and step away until the cable has light tension.',
      'Hold the handle with both hands at the middle of your chest.',
      'Place your feet about shoulder width apart with soft knees, ribs down, and glutes lightly squeezed.',
    ],
    steps: [
      'Brace your trunk as if someone were about to push you from the side.',
      'Press the handle straight out in front of your chest until your arms are straight.',
      'Hold for 2 seconds without letting the handle drift toward the machine or your hips turn.',
      'Bring the handle back to your chest slowly with the same control.',
      'Finish all reps on one side, then turn around and repeat facing the other way.',
    ],
    breathing: 'Breathe out as you press. Keep breathing slowly during the hold without losing your brace.',
    tempo: 'Press out over 2 seconds, hold for 2 seconds, and return over 2 seconds. Smooth, with no jerking.',
    rangeOfMotion:
      'From hands at the chest to arms fully straight in front of the breastbone. The trunk and hips stay still through the whole range.',
    muscles: {
      primary: ['obliques_core'],
      secondary: ['rectus_abdominis'],
    },
    emphasisNote:
      'The obliques and deep core do most of the work by resisting the cable pulling you sideways, with the front abs helping to hold your position. Straight arms make the lever longer, so the hold at arm length is the hardest part.',
    movementPattern: 'anti_rotation',
    joints: ['Spine', 'Hip', 'Shoulder'],
    laterality: 'unilateral',
    logSides: true,
    fatigueOverlap: [],
    commonMistakes: [
      'Letting the handle drift toward the machine as you press.',
      'Twisting the hips or shoulders toward the cable.',
      'Leaning away from the machine to fight the pull.',
      'Using so much weight that you cannot hold still.',
      'Arching the lower back or shrugging the shoulders.',
    ],
    goodFormFeels:
      'A firm, steady tension around your waist while your arms, chest, and hips stay still. Nothing twists.',
    stopRules: [
      'Stop the set when you can no longer keep the handle centred or your hips start to turn.',
      'Stop when you reach the planned reps in reserve.',
      'Stop for back pain. Pain of 4 out of 10 or more pauses this exercise. Tell a parent, coach, or clinician.',
    ],
    safetyNotes: [
      'Choose a weight you can hold perfectly still for every rep. Make it harder with a longer hold or a narrower stance before adding weight.',
      'Keep the cable path clear of other people.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Pallof hold at the chest',
      reason: 'Holding the handle at the chest shortens the lever and makes it easier to stay still.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Band Pallof press',
      reason: 'Anchor a resistance band at chest height to a sturdy post when no cable machine is free.',
    },
    otherSubstitutions: [
      { exerciseId: null, name: 'Side plank', reason: 'Trains the side of the trunk with no equipment.' },
    ],
    loadIncrement: 'none',
    failure: 'never',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Stand side on to the cable with the handle at the middle of your chest.',
          trunk: 180,
          armNear: [-8, 128],
          armFar: [-12, 124],
          legNear: [8, -6],
          legFar: [10, -4],
          props: [
            { type: 'cable', from: 'hands', to: [16, 57] },
            { type: 'handle', at: 'hands' },
          ],
        },
        {
          label: 'Press',
          caption: 'Press straight out and hold. The cable pulls sideways, and you stay square.',
          trunk: 180,
          armNear: [92, 90],
          armFar: [90, 88],
          legNear: [8, -6],
          legFar: [10, -4],
          props: [
            { type: 'cable', from: 'hands', to: [16, 57] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [150, 40], to: [180, 40] },
          ],
        },
        {
          label: 'Return',
          caption: 'Bring the handle back to your chest slowly, still square to the front.',
          trunk: 180,
          armNear: [-8, 128],
          armFar: [-12, 124],
          legNear: [8, -6],
          legFar: [10, -4],
          props: [
            { type: 'cable', from: 'hands', to: [16, 57] },
            { type: 'handle', at: 'hands' },
            { type: 'arrow', from: [160, 40], to: [130, 40] },
          ],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Copenhagen Plank
  {
    id: 'copenhagen-plank',
    name: 'Copenhagen Plank',
    aliases: ['Copenhagen adduction hold', 'Copenhagen side plank'],
    kind: 'hold',
    purpose:
      'Strengthens the inner thigh and the side of the trunk. Strong adductors help protect the groin during lateral moves, lunges, and landings.',
    equipment: ['Flat bench or sturdy box about knee height', 'Exercise mat', 'Optional towel or pad for the bench'],
    setup: [
      'Lie on your side next to the bench with your forearm on the mat and the elbow under your shoulder.',
      'To learn it, use the short lever: rest the inside of your top knee on the bench.',
      'For the long lever, rest the inside of your top ankle and foot on the bench instead.',
      'Keep the bottom leg under the bench, slightly bent or straight.',
      'Line up your head, trunk, and hips.',
    ],
    steps: [
      'Press the top leg down into the bench and lift your hips off the floor.',
      'Hold a straight line from your head to your top foot, or to your top knee on the short lever.',
      'Let the bottom leg hang under the bench, or lift it toward the bench if you can do so with control.',
      'Hold for the planned time, breathing steadily.',
      'Lower your hips gently to the floor, rest, then switch sides.',
    ],
    breathing: 'Breathe slowly and steadily throughout the hold. Do not hold your breath.',
    tempo: 'A steady hold for the planned time, often 10 to 30 seconds per side. Lift into position over 1 to 2 seconds and lower slowly.',
    rangeOfMotion:
      'No movement during the hold. Keep the hips level with the shoulders and top leg, not sagging toward the floor or piking up.',
    muscles: {
      primary: ['adductors', 'obliques_core'],
      secondary: ['glute_med'],
    },
    emphasisNote:
      'The adductors of the top leg hold much of your body weight while the obliques and deep core keep the trunk from sagging. The long lever, with the foot on the bench, biases the adductors more than the short lever.',
    movementPattern: 'hip_adduction',
    joints: ['Hip', 'Spine', 'Shoulder'],
    laterality: 'unilateral',
    logSides: true,
    fatigueOverlap: ['hip'],
    commonMistakes: [
      'Letting the hips sag toward the floor.',
      'Piking the hips up or rolling the chest toward the floor.',
      'Starting with the long lever before the short lever feels easy.',
      'Holding your breath.',
    ],
    goodFormFeels:
      'A strong, steady effort in the inner thigh of the top leg and along the side of your waist, with the shoulder stable over the elbow.',
    stopRules: [
      'End the hold when your hips start to sag or rotate.',
      'Stop at once for sharp groin pain or pain on the inside of the knee. Pain of 4 out of 10 or more, or pain that worsens, pauses this exercise. Tell a parent, coach, or clinician.',
      'Stop if the supporting shoulder hurts.',
    ],
    safetyNotes: [
      'Learn the short lever with the knee on the bench first. Move to the long lever only when the short lever feels easy and a coach agrees.',
      'Pad the bench under your leg for comfort.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Short lever Copenhagen plank',
      reason: 'The knee on the bench shortens the lever and makes the hold easier to control.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Partner assisted Copenhagen plank',
      reason: 'A partner holds your top leg at hip height when no bench is available.',
    },
    otherSubstitutions: [
      {
        exerciseId: null,
        name: 'Adductor ball squeeze',
        reason: 'Lie on your back with knees bent and squeeze a ball between the knees. Gentler inner thigh work with no equipment beyond a ball.',
      },
    ],
    loadIncrement: 'none',
    failure: 'never',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Forearm under the shoulder, inside of the top ankle on the bench, hips on the floor.',
          trunk: 248,
          head: 250,
          armNear: [0, -90],
          armFar: [70, 60],
          legNear: [115, 115, 180],
          legFar: [87, 88, 180],
          hip: [86, 161],
          props: [{ type: 'bench', x: 146, y: 131, w: 46 }],
        },
        {
          label: 'Hold',
          caption: 'Lift the hips so the body forms a straight line. Hold still and breathe.',
          trunk: -83,
          head: -85,
          armNear: [0, -90],
          armFar: [180, 180],
          legNear: [97, 97, 170],
          legFar: [78, 70],
          hip: [80, 136],
          props: [{ type: 'bench', x: 146, y: 131, w: 46 }],
        },
        {
          label: 'Short lever',
          caption: 'Learning version: rest the top knee on the bench instead of the ankle.',
          trunk: -81,
          head: -83,
          armNear: [0, -90],
          armFar: [180, 180],
          legNear: [101, 90, 180],
          legFar: [80, 60],
          hip: [95, 136],
          props: [{ type: 'bench', x: 128, y: 133, w: 62 }],
        },
      ],
    },
  },

  // ---------------------------------------------------------------- Hanging Leg Raise
  {
    id: 'hanging-leg-raise',
    name: 'Hanging Leg Raise',
    aliases: ['Hanging knee raise, bent knee version'],
    kind: 'bodyweight',
    purpose: 'Strengthens the abs and hip flexors through a big range and builds grip strength from hanging.',
    equipment: ['Pull up bar', "Or a captain's chair with forearm pads"],
    setup: [
      'Grip the bar with your hands about shoulder width apart, palms facing forward.',
      'Hang with straight arms and your shoulders gently pulled down away from your ears.',
      'Let your body hang still before the first rep so you are not swinging.',
      'Start with bent knees if straight legs are too hard to control.',
    ],
    steps: [
      'Brace your abs and tuck your pelvis slightly under.',
      'Raise your legs, bent or straight, until your thighs are at least level with your hips.',
      'At the top, curl your pelvis up toward your ribs so the abs finish the movement.',
      'Lower your legs slowly over 2 to 3 seconds without swinging.',
      'Pause briefly at the bottom to settle any swing before the next rep.',
    ],
    breathing: 'Breathe out as you raise your legs. Breathe in as you lower them.',
    tempo: '1 1 3 1 means about one second up, a one second squeeze at the top, three seconds down, and one second still at the bottom.',
    rangeOfMotion:
      'From a still hang to thighs at hip height or higher. Bent knees toward the chest is the learning version. Straight legs to hip height is the full version.',
    muscles: {
      primary: ['rectus_abdominis', 'hip_flexors'],
      secondary: ['obliques_core', 'forearm_flexors'],
    },
    emphasisNote:
      'The hip flexors lift the legs, and curling the pelvis up at the top shifts more of the work to the abs. Hanging also trains grip, so the forearms work throughout. The hip flexors do a large share of the work in every version.',
    movementPattern: 'trunk_flexion',
    joints: ['Hip', 'Spine', 'Shoulder'],
    laterality: 'bilateral',
    logSides: false,
    fatigueOverlap: ['wrist_grip', 'shoulder'],
    commonMistakes: [
      'Swinging to get the legs up.',
      'Lifting the thighs without curling the pelvis, which leaves most of the work to the hip flexors.',
      'Dropping the legs quickly instead of lowering them.',
      'Shrugging the shoulders up toward the ears.',
      'Holding your breath.',
    ],
    goodFormFeels: 'A strong squeeze low in the abs at the top, a slow and controlled lowering, and a body that stays still under the bar.',
    stopRules: [
      'Stop the set at the planned reps in reserve, or as soon as you need to swing to finish a rep.',
      'Stop before your grip gives out and step down with control rather than dropping.',
      'Stop for low back, hip, or shoulder pain. Pain of 4 out of 10 or more pauses this exercise. Tell a parent, coach, or clinician.',
    ],
    safetyNotes: [
      'Use a bar you can reach and step down from safely.',
      'Learn the bent knee version first and move to straight legs only when you can do it without swinging.',
    ],
    easierSubstitution: {
      exerciseId: null,
      name: 'Hanging knee raise',
      reason: 'Bending the knees shortens the lever so you can control the movement and curl the pelvis.',
    },
    equipmentSubstitution: {
      exerciseId: null,
      name: 'Reverse crunch',
      reason: 'Trains the same pelvis curl lying on the floor when no bar is available, with no grip limit.',
    },
    otherSubstitutions: [
      { exerciseId: null, name: "Captain's chair knee raise", reason: 'Forearm pads take grip out of the exercise.' },
    ],
    loadIncrement: 'none',
    failure: 'all',
    visual: {
      poses: [
        {
          label: 'Start',
          caption: 'Hang still from the bar with straight arms. Bend the knees if your feet would touch the floor.',
          trunk: 180,
          head: 155,
          armNear: [192, 186],
          armFar: [190, 184],
          legNear: [0, -80, -50],
          legFar: [4, -76, -46],
          hip: [77, 108],
          props: [{ type: 'line', x1: 40, y1: 6, x2: 104, y2: 6 }],
        },
        {
          label: 'Knee raise',
          caption: 'Learning version: raise the knees above hip height and curl the pelvis up.',
          trunk: 190,
          head: 150,
          armNear: [182, 180],
          armFar: [180, 178],
          legNear: [95, 10, 60],
          legFar: [92, 8, 60],
          hip: [79, 107],
          props: [{ type: 'line', x1: 40, y1: 6, x2: 104, y2: 6 }],
        },
        {
          label: 'Straight legs',
          caption: 'Full version: straight legs to hip height, then lower slowly without swinging.',
          trunk: 192,
          head: 150,
          armNear: [180, 178],
          armFar: [178, 176],
          legNear: [90, 90, 175],
          legFar: [88, 88, 175],
          hip: [79, 107],
          props: [{ type: 'line', x1: 40, y1: 6, x2: 104, y2: 6 }],
        },
      ],
    },
  },
];
