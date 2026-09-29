import type { MediaReference, ClaimReview } from './types';

/**
 * External demonstration videos, matched 2026-09-29 from web search results only.
 *
 * None of these videos were watched. youtube.com was not reachable from the build environment,
 * so each record rests on the title, channel and description shown in search results. Exercises
 * with no record had no search result that showed a credible channel and an exact title match
 * (for example the Romanian deadlift, where two uploads share one title and the original channel
 * could not be told apart from a reupload). The user can confirm a video in the app, which
 * upgrades it to 'user-confirmed' at runtime.
 *
 * Channel attribution for the Renaissance Periodization technique library rests on search
 * results that describe those uploads as RP videos "Filmed at Exile Gym in Baltimore, MD"
 * (mostly October 2019). The channel name itself was not always printed next to each video.
 */

const NOT_WATCHED =
  'Matched by title and channel from search results; not watched frame by frame.';

function yt(
  id: string,
  targetId: string,
  targetType: 'exercise' | 'recipe',
  videoId: string,
  title: string,
  channel: string,
  note: string,
): MediaReference {
  return {
    id,
    targetId,
    targetType,
    platform: 'youtube',
    title,
    channel,
    url: `https://www.youtube.com/watch?v=${videoId}`,
    videoId,
    verifiedOn: '2026-09-29',
    language: 'en',
    captions: 'unknown',
    reviewStatus: 'metadata-match',
    reviewerNote: `${NOT_WATCHED} ${note}`,
  };
}

const RP_NOTE =
  'Short Renaissance Periodization technique library clip, described in search results as filmed at Exile Gym in Baltimore, MD (about October 2019). RP channel attribution comes from the search result summary. Likely demonstration only with little spoken coaching.';

export const MEDIA: MediaReference[] = [
  // ---------- Lower body ----------
  yt(
    'yt-barbell-squat-squatu',
    'barbell-squat',
    'exercise',
    'SbgHegC6lEs',
    'How to Back Squat |#AskSquatU Show Ep. 10|',
    'Squat University',
    'Dr. Aaron Horschig (physical therapist) with weightlifting coach Anna Martin demonstrating a high bar back squat; published August 2017. Episode format with discussion, not a short demo.',
  ),
  yt(
    'yt-bulgarian-split-squat-squatu',
    'bulgarian-split-squat',
    'exercise',
    '-4LVK1crLSw',
    'The ULTIMATE Bulgarian Split Squat Tutorial',
    'Squat University',
    'Dr. Aaron Horschig covers stance length and bench height; published September 2019.',
  ),
  yt(
    'yt-standing-calf-raise-childrens-colorado',
    'standing-calf-raise',
    'exercise',
    'k8ipHzKeAkQ',
    'Exercises with an Athletic Trainer: Standing Calf Raises',
    "Children's Hospital Colorado",
    'Athletic trainer demonstrating for patients and student athletes; published June 2021. Likely a bodyweight version rather than a loaded machine calf raise.',
  ),
  yt('yt-hack-squat-rp', 'hack-squat', 'exercise', 'rYgNArpwE7E', 'Hack Squat', 'Renaissance Periodization', RP_NOTE),
  yt(
    'yt-barbell-hip-thrust-contreras',
    'barbell-hip-thrust',
    'exercise',
    'hCm-70-9_XE',
    'Hip Thrust Instructional Video',
    'Bret Contreras Glute Guy',
    'Ten minute instructional by Bret Contreras, who popularised the barbell hip thrust; posted March 2010 and linked from his own blog post of the same name. Older video, so setup details (pad, bench height) may differ from current coaching.',
  ),
  yt('yt-seated-leg-curl-rp', 'seated-leg-curl', 'exercise', 'Orxowest56U', 'Seated Leg Curl', 'Renaissance Periodization', RP_NOTE),
  yt(
    'yt-leg-extension-rp',
    'leg-extension',
    'exercise',
    'm0FOpMEgero',
    'Leg Extension',
    'Renaissance Periodization',
    `${RP_NOTE} This one was linked to the RP series by search context rather than an explicit channel line, so it is the least certain RP match.`,
  ),
  yt(
    'yt-nordic-hamstring-curl-e3',
    'nordic-hamstring-curl',
    'exercise',
    '_e9vFU9-tkc',
    'How to Set Up, Perform, & Program Nordic Hamstring Curls (Progressions | Regressions | Alternatives)',
    'E3 Rehab',
    'Doctors of physical therapy; includes regressions, which suits a first Nordic block for a teen.',
  ),

  // ---------- Upper body ----------
  yt(
    'yt-barbell-bench-press-rp-2012',
    'barbell-bench-press',
    'exercise',
    'hSHZvAp1VvA',
    'RP Medium Grip Bench Press',
    'Renaissance Periodization',
    'Older upload (July 2012). Channel attributed from the RP title prefix and search summary. Title does not say barbell, although a medium grip bench press is normally a barbell lift; check that the video shows a barbell.',
  ),
  yt(
    'yt-incline-barbell-bench-press-rp-2012',
    'incline-barbell-bench-press',
    'exercise',
    'wqByyWZjHgY',
    'RP Incline Medium Grip Barbell Bench Press',
    'Renaissance Periodization',
    'Older upload (July 2012). Channel attributed from the RP title prefix and search summary.',
  ),
  yt(
    'yt-machine-bench-press-rp',
    'machine-bench-press',
    'exercise',
    'NwzUje3z0qY',
    'Machine Chest Press',
    'Renaissance Periodization',
    `${RP_NOTE} Titled machine chest press; the specific machine may differ from the one at the user gym.`,
  ),
  yt('yt-wide-grip-lat-pulldown-rp', 'wide-grip-lat-pulldown', 'exercise', 'YCKPD4BSD2E', 'Wide Grip Pulldown', 'Renaissance Periodization', RP_NOTE),
  yt(
    'yt-one-arm-lat-pulldown-meadows',
    'one-arm-lat-pulldown',
    'exercise',
    'r68DrqhNSis',
    'Exercise Index - Single Arm Pulldown',
    'Mountain Dog Diet (John Meadows)',
    'Established bodybuilding coach explaining his preferred single arm pulldown with a soft handle; published June 2019.',
  ),
  yt(
    'yt-leverage-high-row-rp',
    'leverage-high-row',
    'exercise',
    'gg5hwJuv6KI',
    'Hammer High Row',
    'Renaissance Periodization',
    `${RP_NOTE} Shows a plate loaded Hammer Strength style high row, which is the leverage machine this exercise refers to; other brands differ in handle path.`,
  ),
  yt('yt-seated-cable-row-rp', 'seated-cable-row', 'exercise', 'UCXxvVItLoM', 'Seated Cable Row', 'Renaissance Periodization', RP_NOTE),
  yt('yt-reverse-machine-fly-rp', 'reverse-machine-fly', 'exercise', '5YK4bgzXDp0', 'Machine Reverse Flye', 'Renaissance Periodization', RP_NOTE),
  yt(
    'yt-face-pull-rp',
    'face-pull',
    'exercise',
    '-MODnZdnmAQ',
    'Cable Rope Facepull',
    'Renaissance Periodization',
    `${RP_NOTE} Standing cable rope version; RP also has kneeling, dumbbell and barbell face pull clips, which were not used.`,
  ),
  yt('yt-lateral-raise-rp', 'lateral-raise', 'exercise', 'OuG1smZTsQQ', 'Lateral Raise', 'Renaissance Periodization', RP_NOTE),
  yt(
    'yt-single-arm-cable-lateral-raise-rp',
    'single-arm-cable-lateral-raise',
    'exercise',
    'lq7eLC30b9w',
    'Leaning Cable Lateral Raise',
    'Renaissance Periodization',
    `${RP_NOTE} This is the leaning variant of a single arm cable lateral raise; if PeakForm cues an upright torso, the video differs in body position.`,
  ),
  yt(
    'yt-cable-external-rotation-e3',
    'cable-external-rotation',
    'exercise',
    'X-JP6sJTZAI',
    'Cable Shoulder External Rotation',
    'E3 Rehab',
    'Doctors of physical therapy; published February 2020. Arm at the side version.',
  ),
  yt('yt-hammer-curl-rp', 'hammer-curl', 'exercise', 'XOEL4MgekYE', 'Hammer Curl', 'Renaissance Periodization', RP_NOTE),
  yt('yt-machine-preacher-curl-rp', 'machine-preacher-curl', 'exercise', 'Ja6ZlIDONac', 'Machine Preacher Curl', 'Renaissance Periodization', RP_NOTE),
  yt('yt-triceps-pushdown-rp', 'triceps-pushdown', 'exercise', '6Fzep104f0s', 'Cable Triceps Pushdown', 'Renaissance Periodization', RP_NOTE),
  yt(
    'yt-rope-overhead-triceps-extension-rp',
    'rope-overhead-triceps-extension',
    'exercise',
    'kqidUIf1eJE',
    'Rope Overhead Triceps Extension',
    'Renaissance Periodization',
    RP_NOTE,
  ),
  yt(
    'yt-palm-up-wrist-curl-rp',
    'palm-up-wrist-curl',
    'exercise',
    '2wPpcJBe03o',
    'Dumbbell Bench Wrist Curl',
    'Renaissance Periodization',
    `${RP_NOTE} Title does not say palm up; a standard wrist curl is palm up (wrist flexion), but this should be confirmed on first view.`,
  ),

  // ---------- Athletic and core ----------
  yt(
    'yt-dynamic-volleyball-warm-up-usav',
    'dynamic-volleyball-warm-up',
    'exercise',
    'OQyGncNgNIk',
    '15-Minute Volleyball WARM-UP Routine ft. Aaron Brock & Olympian Jeff Jendryk',
    'USA Volleyball',
    'Presented by USA Volleyball director of sports medicine and performance Aaron Brock. Fifteen minutes, so it may be longer than the PeakForm warm up block; 5 and 3 minute versions also exist on the same channel.',
  ),
  yt(
    'yt-volleyball-approach-footwork-aoc',
    'volleyball-approach-footwork',
    'exercise',
    'BXBTBBngrwA',
    'Art of Coaching Volleyball - Hitting Approach (Portland Clinic)',
    'The Art of Coaching Volleyball',
    'Clinic footage (June 2011) of high level coaches explaining what they look for in the hitting approach and how to teach it. Aimed at coaches, so it is more discussion than a step by step player drill.',
  ),
  yt(
    'yt-volleyball-spike-olympics',
    'volleyball-spike',
    'exercise',
    'jx7z8bkIj4Y',
    "How to improve your Attack in Volleyball feat. Jordan Larson | Olympians' Tips",
    'Olympics',
    'Four time Olympian Jordan Larson on attacking. Official Olympics channel series. Covers attack technique broadly rather than one isolated drill.',
  ),
  yt(
    'yt-pallof-press-hinge-health',
    'pallof-press',
    'exercise',
    'n8ZZG9gElhs',
    'How to Do a Pallof Press: A Guide from Physical Therapists',
    'Hinge Health',
    'Physical therapist led guide from a digital physical therapy company; published April 2025. Whether it uses a band or a cable was not visible in the snippet.',
  ),
  yt(
    'yt-copenhagen-plank-e3',
    'copenhagen-plank',
    'exercise',
    'YRRnnZsRs9U',
    'How to Set Up, Perform, & Program Copenhagen Planks (Progressions | Regressions | Alternatives)',
    'E3 Rehab',
    'Doctors of physical therapy; regressions (short lever, knee supported) matter for a teen starting adductor work.',
  ),
  yt(
    'yt-hanging-leg-raise-rp',
    'hanging-leg-raise',
    'exercise',
    '7FwGZ8qY5OU',
    'Hanging Straight Leg Raise',
    'Renaissance Periodization',
    `${RP_NOTE} Straight leg version; RP also has a Hanging Knee Raise clip (RD_A-Z15ER4) that suits the easier substitution.`,
  ),

  // ---------- Recipes ----------
  yt(
    'yt-overnight-oats-bbc-good-food',
    'yogurt-oat-breakfast',
    'recipe',
    'JE7BOBMtP58',
    'How to make overnight oats',
    'BBC Good Food',
    'Published June 2022. Per the linked recipe snippet: oats soaked overnight in water or milk with cinnamon and a pinch of salt, then topped with yogurt, berries, honey and nut butter. Honey and nut butter add sugar and fat beyond the PeakForm base; exact amounts were not checked.',
  ),
  yt(
    'yt-sheet-pan-salmon-atk',
    'sheet-pan-salmon',
    'recipe',
    'PdqgZz5qnJc',
    'How to Make One-Pan Roasted Salmon with Broccoli and Red Potatoes',
    "America's Test Kitchen",
    'Bridget Lancaster and Julia Collin Davison; published December 2019. Vegetable is broccoli. Oil amount and any butter or sauce could not be checked. Cook salmon to 145 F / 63 C.',
  ),
  yt(
    'yt-lentil-soup-atk',
    'lentil-soup',
    'recipe',
    'uH8Fq7CwfR8',
    'How to Make Easy Red Lentil Soup with North African Spices',
    "America's Test Kitchen",
    'Test cook Erin McMurrer. Search snippets say the onions are cooked in butter, so it is not a low oil recipe as filmed; PeakForm can suggest a smaller amount of oil instead. Red lentils blended smooth, which differs from a chunky soup. ATK also has a chorizo and lentil soup (Julia at Home) that was not used because chorizo adds fat and salt.',
  ),
  yt(
    'yt-chicken-rice-downshiftology',
    'chicken-rice-boxes',
    'recipe',
    'oNXigmY_dIM',
    'CHICKEN & RICE | easy & healthy one-pan recipe',
    'Downshiftology',
    'Published October 2020. One pan chicken thighs in a lemon dijon marinade with rice. Uses thighs (more fat than breast) and olive oil, and is not shown as boxed meal prep; if boxed, cool within 2 hours, refrigerate at 40 F / 4 C or below, eat within 3 to 4 days, and cook chicken to 165 F / 74 C.',
  ),
];

/**
 * Social media claim reviews. A claim is a lead, not evidence.
 * Context from the user: an app they tried seemed to miss upper back, calves and forearms, so these
 * videos may be about muscle coverage or exercise selection. That is context only; the content was
 * not seen and is not guessed here.
 */
export const CLAIM_REVIEWS: ClaimReview[] = [
  {
    id: 'claim-tiktok-zsbhyxd9r',
    url: 'https://vt.tiktok.com/ZSbhYxd9R/',
    platform: 'tiktok',
    accessible: false,
    claimed: 'Not visible: the video could not be opened from the build environment.',
    evidence:
      'WebFetch on the short link was blocked by the egress proxy, and web searches for the short code and full link returned no page about this video. To evaluate it, someone needs the creator name, caption and the specific claim (for example which muscles a program misses, or which exercise is said to be best), then compare it with the exercise library muscle map and with studies such as those in SOURCES.',
    verdict:
      'Not reviewed. No change to PeakForm. If the user shares the caption or a short summary, the claim can be checked. Separately, the current library already includes upper back (face pull, reverse machine fly, high row, seated cable row), calves (standing and seated calf raise, tibialis raise) and forearms (palm up and palm down wrist curls, hammer curl).',
    changesApp: false,
    reviewedOn: '2026-09-29',
  },
  {
    id: 'claim-tiktok-zsbh2l6fg',
    url: 'https://vt.tiktok.com/ZSbh2L6Fg/',
    platform: 'tiktok',
    accessible: false,
    claimed: 'Not visible: the video could not be opened from the build environment.',
    evidence:
      'WebFetch on the short link was blocked by the egress proxy, and web searches for the short code and full link returned no page about this video. Needed: the creator, the caption, the exact claim, and any study or guideline it cites, checked against peer reviewed evidence and pediatric guidance.',
    verdict:
      'Not reviewed. No change to PeakForm. The user can describe the claim or paste the caption for a follow up review.',
    changesApp: false,
    reviewedOn: '2026-09-29',
  },
];
