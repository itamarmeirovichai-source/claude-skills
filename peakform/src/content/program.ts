import type { LibraryExerciseId } from './exercises/ids';
import { exercise } from './library';
import type { PlanDay, PlanItem, SetTarget, Weekday } from './plan';
import { wristAllows, type WristStatus } from './traits';

// The training program, built from the athlete's own exercise choices.
//
// Each slot is one muscle or muscle head. Its options are exercises that train that head in a
// similar way, with a similar stretch, so any choice builds about the same muscle (machines and
// free weights grow muscle similarly: Haugen 2023; Schwanbeck 2020). The weekly template decides
// where each slot goes, how many sets, and the rest. Since 3.0.0 work sets stop about two reps short
// of failure (three for shoulder care and while learning), because sets close to failure build about
// as much muscle with less fatigue, and youth guidance does not prescribe routine failure. Only
// machines, cables, the Smith machine, and dumbbells are offered, because the athlete trains alone.

export type SlotId =
  | 'shoulder-care'
  | 'chest-upper'
  | 'chest-press'
  | 'chest-fly'
  | 'lats'
  | 'lats-stretch'
  | 'row'
  | 'side-delt'
  | 'rear-delt'
  | 'biceps-long'
  | 'biceps-short'
  | 'brachialis'
  | 'triceps-long'
  | 'triceps-short'
  | 'traps'
  | 'forearm-flexors'
  | 'forearm-extensors'
  | 'quads'
  | 'rectus-femoris'
  | 'hamstring-curl'
  | 'hinge'
  | 'glutes'
  | 'glute-med'
  | 'adductors'
  | 'calves'
  | 'abs'
  | 'obliques';

export type SlotGroup = 'Warm up' | 'Chest' | 'Back' | 'Shoulders' | 'Arms' | 'Legs' | 'Core';

export interface ProgramSlot {
  id: SlotId;
  group: SlotGroup;
  /** Short name shown in the questionnaire, for example "Upper chest". */
  title: string;
  /** The muscle or head, in plain words. */
  head: string;
  /** Why this slot exists and what the options share. */
  why: string;
  /** Equivalent choices. The first is the default. */
  options: LibraryExerciseId[];
  sets: number;
  reps: [number, number];
  restSec: number;
  /** Reps in reserve for work sets. */
  rirShort: number;
  /** Seconds, when an option is a hold. */
  holdSeconds?: number;
}

const BIG = { sets: 3, restSec: 150, rirShort: 2 } as const;
const SMALL = { sets: 3, restSec: 90, rirShort: 2 } as const;

export const PROGRAM_SLOTS: ProgramSlot[] = [
  {
    id: 'shoulder-care',
    group: 'Warm up',
    title: 'Shoulder warm up',
    head: 'Rotator cuff',
    why: 'Short, light work for the small muscles that turn the arm outward and slow it down after every spike. A warm up like this three times a week cut shoulder problems in overhead athletes (Andersson 2017). It is care, not a muscle builder, so it stays light.',
    options: ['cable-external-rotation', 'side-lying-external-rotation'],
    sets: 2,
    reps: [15, 20],
    restSec: 45,
    rirShort: 3,
  },
  {
    id: 'chest-upper',
    group: 'Chest',
    title: 'Upper chest',
    head: 'Upper, clavicular head of the chest, with the front shoulder',
    why: 'Pressing on a 30 to 45 degree incline grows the upper chest more than flat pressing (Chaves 2020). All three options press on that angle and give a deep stretch at the bottom.',
    options: ['incline-dumbbell-press', 'incline-machine-press', 'incline-smith-press'],
    ...BIG,
    reps: [8, 12],
  },
  {
    id: 'chest-press',
    group: 'Chest',
    title: 'Middle chest press',
    head: 'Middle and lower, sternal head of the chest',
    why: 'A flat press trains the biggest part of the chest, with the triceps and front shoulder helping. Machine, Smith, and dumbbell presses built chest muscle about equally in studies.',
    options: ['machine-bench-press', 'dumbbell-bench-press', 'smith-bench-press'],
    ...BIG,
    reps: [8, 12],
  },
  {
    id: 'chest-fly',
    group: 'Chest',
    title: 'Chest fly',
    head: 'Sternal head of the chest, in the long, stretched position',
    why: 'A fly loads the chest when it is most stretched, with little help from the triceps. All three keep tension from the open stretch to the squeeze.',
    options: ['flat-cable-fly', 'pec-deck-fly', 'standing-cable-crossover'],
    ...SMALL,
    reps: [10, 15],
  },
  {
    id: 'lats',
    group: 'Back',
    title: 'Lats, vertical pull',
    head: 'Latissimus dorsi and teres major, the width of the back',
    why: 'Pulling from overhead with a full stretch at the top builds back width. Wide, neutral, and single arm grips worked about the same, so pick the one that feels strongest.',
    options: ['wide-grip-lat-pulldown', 'neutral-grip-pulldown', 'one-arm-lat-pulldown', 'assisted-pull-up'],
    ...BIG,
    reps: [8, 12],
  },
  {
    id: 'lats-stretch',
    group: 'Back',
    title: 'Lats, long stretch',
    head: 'Lats trained with straight arms, from the stretch overhead',
    why: 'With straight arms the biceps cannot help, and the lats work from their most stretched position overhead down to the hips.',
    options: ['straight-arm-cable-pulldown', 'dumbbell-pullover'],
    ...SMALL,
    reps: [10, 15],
  },
  {
    id: 'row',
    group: 'Back',
    title: 'Upper back row',
    head: 'Middle trapezius, rhomboids, lats, and rear shoulder',
    why: 'Rowing builds the thickness of the upper back and balances all the pressing and spiking. Supported rows let the lower back rest, so you can push the back itself hard.',
    options: ['chest-supported-dumbbell-row', 'seated-cable-row', 'chest-supported-machine-row', 'leverage-high-row'],
    ...BIG,
    reps: [8, 12],
  },
  {
    id: 'side-delt',
    group: 'Shoulders',
    title: 'Side shoulder',
    head: 'Lateral head of the deltoid, the width of the shoulders',
    why: 'Presses barely train the side of the shoulder, so it needs its own exercise. Cable and dumbbell raises grew it equally (Larsen 2025). It recovers fast, so it is trained three times a week.',
    options: ['single-arm-cable-lateral-raise', 'lateral-raise', 'machine-lateral-raise'],
    ...SMALL,
    reps: [12, 20],
  },
  {
    id: 'rear-delt',
    group: 'Shoulders',
    title: 'Rear shoulder',
    head: 'Posterior head of the deltoid',
    why: 'The back of the shoulder gets some work from rows, but a direct exercise fills it out and protects the shoulder of a hitter.',
    options: ['reverse-machine-fly', 'cable-reverse-fly', 'face-pull'],
    ...SMALL,
    reps: [12, 20],
  },
  {
    id: 'biceps-long',
    group: 'Arms',
    title: 'Biceps, long head',
    head: 'Long head of the biceps, trained with the arm behind the body',
    why: 'With the arm behind the body the biceps starts in a long stretch. Incline curls grew the upper biceps more than preacher curls (Kassiano 2025).',
    options: ['incline-dumbbell-curl', 'bayesian-cable-curl'],
    ...SMALL,
    reps: [10, 15],
  },
  {
    id: 'biceps-short',
    group: 'Arms',
    title: 'Biceps, short head',
    head: 'Short head of the biceps and the brachialis, arm in front of the body',
    why: 'On a preacher pad the arm sits in front of the body and the curl is hardest near the stretched bottom. It complements the curl with the arm behind the body.',
    options: ['machine-preacher-curl', 'dumbbell-preacher-curl'],
    ...SMALL,
    reps: [10, 15],
  },
  {
    id: 'brachialis',
    group: 'Arms',
    title: 'Brachialis and forearm',
    head: 'Brachialis and brachioradialis, under and beside the biceps',
    why: 'A neutral or palms down grip shifts work to the brachialis, which pushes the biceps up and makes the whole arm thicker, and to the top of the forearm.',
    options: ['hammer-curl', 'rope-hammer-curl', 'cable-reverse-curl'],
    ...SMALL,
    reps: [10, 15],
  },
  {
    id: 'triceps-long',
    group: 'Arms',
    title: 'Triceps, long head',
    head: 'Long head of the triceps, the biggest part of the back of the arm',
    why: 'Overhead extensions stretch the long head. They grew the triceps about 1.4 times more than pushdowns (Maeo 2023), so the long head is trained twice a week.',
    options: ['rope-overhead-triceps-extension', 'single-arm-cable-overhead-extension', 'dumbbell-overhead-triceps-extension'],
    ...SMALL,
    reps: [10, 15],
  },
  {
    id: 'triceps-short',
    group: 'Arms',
    title: 'Triceps, outer heads',
    head: 'Lateral and medial heads of the triceps, arm at the side',
    why: 'With the arm at the side the outer heads do more of the work and you can go heavy with little stress on the shoulder.',
    options: ['triceps-pushdown', 'single-arm-cable-pushdown'],
    ...SMALL,
    reps: [10, 15],
  },
  {
    id: 'traps',
    group: 'Back',
    title: 'Upper traps',
    head: 'Upper trapezius, between the neck and shoulders',
    why: 'Rows train the middle traps, but the upper traps need a shrug to grow. Once a week is enough.',
    options: ['dumbbell-shrug', 'smith-shrug'],
    ...SMALL,
    reps: [10, 15],
  },
  {
    id: 'forearm-flexors',
    group: 'Arms',
    title: 'Forearm, inside',
    head: 'Wrist flexors, the inside of the forearm',
    why: 'Strong forearm flexors help the grip on every pull and protect the wrist when you block and dig.',
    options: ['palm-up-wrist-curl'],
    ...SMALL,
    reps: [12, 20],
    restSec: 75,
  },
  {
    id: 'forearm-extensors',
    group: 'Arms',
    title: 'Forearm, outside',
    head: 'Wrist extensors, the outside of the forearm',
    why: 'The outside of the forearm gets little from curls and rows, so it gets one short exercise a week.',
    options: ['palm-down-wrist-curl'],
    ...SMALL,
    reps: [12, 20],
    restSec: 75,
  },
  {
    id: 'quads',
    group: 'Legs',
    title: 'Quads and glutes, squat',
    head: 'The three vasti of the quads, with the glutes and adductors',
    why: 'A deep squat pattern builds the front of the thigh and, with depth, the glutes and inner thigh too (Kubo 2019). Depth matters more than the machine, and all three let you go deep with the back supported or guided.',
    options: ['hack-squat', 'leg-press', 'smith-squat'],
    ...BIG,
    reps: [8, 12],
    restSec: 180,
  },
  {
    id: 'rectus-femoris',
    group: 'Legs',
    title: 'Quads, rectus femoris',
    head: 'Rectus femoris, the quad head that also crosses the hip',
    why: 'Squats and leg presses barely grow this head, but leg extensions do (Kinoshita 2026). Leaning back in the seat stretches it more and grew it more (Larsen 2024).',
    options: ['leg-extension'],
    ...SMALL,
    reps: [10, 15],
  },
  {
    id: 'hamstring-curl',
    group: 'Legs',
    title: 'Hamstrings, knee bend',
    head: 'Hamstrings, trained by bending the knee',
    why: 'The seated leg curl trains the hamstrings in a long stretch and grew them more than the lying curl (Maeo 2021: about 14 against 9 percent).',
    options: ['seated-leg-curl'],
    ...SMALL,
    reps: [10, 15],
  },
  {
    id: 'hinge',
    group: 'Legs',
    title: 'Hamstrings and glutes, hinge',
    head: 'Long hamstrings, glutes, and the back muscles along the spine, trained from the hip',
    why: 'Bending at the hips with a flat back stretches the hamstrings from the top end. Together with the leg curl, that trains the hamstrings at both joints.',
    options: ['dumbbell-romanian-deadlift', 'smith-romanian-deadlift', 'back-extension'],
    ...BIG,
    reps: [8, 12],
  },
  {
    id: 'glutes',
    group: 'Legs',
    title: 'Glutes',
    head: 'Gluteus maximus, the biggest muscle in the body',
    why: 'Split squats and lunges train the glutes deep in the stretch, and hip thrusts load them hard at the top. Squats and hip thrusts grew the glutes about equally (Plotkin 2023).',
    options: ['bulgarian-split-squat', 'walking-lunge', 'smith-hip-thrust'],
    ...BIG,
    reps: [8, 12],
  },
  {
    id: 'glute-med',
    group: 'Legs',
    title: 'Side of the hip',
    head: 'Gluteus medius and minimus',
    why: 'Squats and hip thrusts barely grow the side of the hip (Plotkin 2023). It steadies the knee in every landing and side step.',
    options: ['cable-hip-abduction', 'hip-abduction-machine'],
    ...SMALL,
    reps: [12, 20],
    restSec: 75,
  },
  {
    id: 'adductors',
    group: 'Legs',
    title: 'Inner thigh',
    head: 'Adductors',
    why: 'The adductors are a big part of the thigh and strong ones are linked to fewer groin strains in court sports (Harøy 2019).',
    options: ['adductor-machine', 'cable-hip-adduction', 'copenhagen-plank'],
    ...SMALL,
    reps: [12, 15],
    restSec: 75,
    holdSeconds: 25,
  },
  {
    id: 'calves',
    group: 'Legs',
    title: 'Calves',
    head: 'Gastrocnemius and soleus',
    why: 'Straight knee raises train both calf muscles, and seated raises add little for the gastrocnemius (Kinoshita 2023). A pause in the deep stretch grew the calves most (Kassiano 2023).',
    options: ['standing-calf-raise', 'leg-press-calf-raise', 'single-leg-calf-raise'],
    ...SMALL,
    reps: [10, 15],
  },
  {
    id: 'abs',
    group: 'Core',
    title: 'Abs',
    head: 'Rectus abdominis',
    why: 'The six pack muscle grows like any other muscle, with load and a stretch. Each option bends or braces the trunk against real resistance.',
    options: ['cable-crunch', 'hanging-leg-raise', 'ab-wheel-rollout'],
    ...SMALL,
    reps: [10, 15],
    restSec: 75,
  },
  {
    id: 'obliques',
    group: 'Core',
    title: 'Obliques',
    head: 'Obliques and deep core',
    why: 'Resisting and producing rotation trains the side of the trunk that links hips and shoulders in every spike and serve.',
    options: ['pallof-press', 'cable-woodchop'],
    ...SMALL,
    reps: [10, 15],
    restSec: 60,
    rirShort: 2,
  },
];

export const SLOT_BY_ID: Record<SlotId, ProgramSlot> = Object.fromEntries(PROGRAM_SLOTS.map((s) => [s.id, s])) as Record<SlotId, ProgramSlot>;

/** A place in a session: which slot, whether it uses the first or second choice, and its dose. */
export interface SlotEntry {
  slot: SlotId;
  choice: 0 | 1;
  sets?: number;
  reps?: [number, number];
  restSec?: number;
}

/** Items that are not chosen. */
export type FixedEntry = { fixed: Omit<PlanItem, 'id' | 'session'> };

export interface ProgramDay {
  weekday: Weekday;
  key: PlanDay['key'];
  title: string;
  short: string;
  main: Array<SlotEntry | FixedEntry>;
}

const s = (slot: SlotId, choice: 0 | 1 = 0, dose: Omit<SlotEntry, 'slot' | 'choice'> = {}): SlotEntry => ({ slot, choice, ...dose });
const r = (min: number, max: number): SetTarget => ({ type: 'reps', min, max });

// Four gym days since 3.0.0, upper and lower body in turn, so every muscle is trained twice a week
// with about 8 to 12 direct sets. With weekly sets the same, training a muscle two or three times a
// week builds about as much as more frequent training (Schoenfeld 2016, 2019), and the days off
// leave room for school sport, the home jump sessions, and recovery. Jumps never happen in the gym:
// on Monday and Thursday they are done at home first, on fresh legs, and the leg work follows.
export const PROGRAM_DAYS: ProgramDay[] = [
  {
    weekday: 0,
    key: 'sun',
    title: 'Upper A',
    short: 'Upper A',
    main: [s('shoulder-care', 0, { sets: 2 }), s('chest-press'), s('lats'), s('chest-upper', 0, { sets: 2 }), s('row'), s('side-delt'), s('biceps-long', 0, { sets: 2 }), s('triceps-long', 0, { sets: 2 })],
  },
  {
    weekday: 1,
    key: 'mon',
    title: 'Lower A',
    short: 'Lower A',
    main: [s('quads', 0, { reps: [6, 10], restSec: 180 }), s('hinge', 0, { reps: [8, 10] }), s('hamstring-curl', 0, { sets: 2 }), s('calves', 0, { sets: 2 }), s('abs', 0, { sets: 2 })],
  },
  {
    weekday: 3,
    key: 'wed',
    title: 'Upper B',
    short: 'Upper B',
    main: [s('shoulder-care', 1, { sets: 2 }), s('chest-upper', 1), s('row', 1), s('lats', 1), s('chest-fly', 0, { sets: 2 }), s('rear-delt'), s('side-delt', 1, { sets: 2 }), s('biceps-short', 0, { sets: 2 }), s('triceps-short', 0, { sets: 2 })],
  },
  {
    weekday: 4,
    key: 'thu',
    title: 'Lower B',
    short: 'Lower B',
    main: [s('glutes', 0, { reps: [8, 10] }), s('rectus-femoris', 0, { sets: 2 }), s('hamstring-curl', 0, { sets: 2 }), s('glute-med', 0, { sets: 2 }), s('adductors', 0, { sets: 2 }), s('calves', 1, { sets: 2 }), s('obliques', 0, { sets: 2 })],
  },
];

/** The athlete's choices: the first and, for variety, an optional second exercise per slot. */
export type ProgramPicks = Partial<Record<SlotId, LibraryExerciseId[]>>;

/** How many times a week each slot appears. */
export function slotExposures(slot: SlotId): number {
  return PROGRAM_DAYS.reduce((n, d) => n + d.main.filter((e) => 'slot' in e && e.slot === slot).length, 0);
}

/** Slots used in the current week. Slots outside it keep their saved choices for later. */
export const ACTIVE_SLOTS: ProgramSlot[] = PROGRAM_SLOTS.filter((sl) => slotExposures(sl.id) > 0);

/** The first option, and the second option for the second weekly exposure. */
export function firstOptionPicks(): ProgramPicks {
  const out: ProgramPicks = {};
  for (const slot of PROGRAM_SLOTS) out[slot.id] = slot.options.length > 1 && slotExposures(slot.id) > 1 ? [slot.options[0]!, slot.options[1]!] : [slot.options[0]!];
  return out;
}

/**
 * The athlete's answers to the exercise questionnaire, 30 September 2026. A second exercise is
 * used for the second time that muscle is trained in the week.
 */
export const CHOSEN_PICKS: ProgramPicks = {
  'shoulder-care': ['cable-external-rotation'],
  'chest-upper': ['incline-machine-press'],
  'chest-press': ['machine-bench-press'],
  'chest-fly': ['pec-deck-fly'],
  'lats': ['wide-grip-lat-pulldown', 'one-arm-lat-pulldown'],
  'lats-stretch': ['straight-arm-cable-pulldown'],
  'row': ['chest-supported-dumbbell-row', 'seated-cable-row'],
  'side-delt': ['single-arm-cable-lateral-raise', 'machine-lateral-raise'],
  'rear-delt': ['reverse-machine-fly', 'face-pull'],
  'biceps-long': ['incline-dumbbell-curl'],
  'biceps-short': ['machine-preacher-curl'],
  'brachialis': ['rope-hammer-curl'],
  'triceps-long': ['dumbbell-overhead-triceps-extension', 'rope-overhead-triceps-extension'],
  'triceps-short': ['triceps-pushdown'],
  'traps': ['dumbbell-shrug'],
  'forearm-flexors': ['palm-up-wrist-curl'],
  'forearm-extensors': ['palm-down-wrist-curl'],
  'quads': ['leg-press'],
  'rectus-femoris': ['leg-extension'],
  'hamstring-curl': ['seated-leg-curl'],
  'hinge': ['dumbbell-romanian-deadlift'],
  'glutes': ['bulgarian-split-squat'],
  'glute-med': ['hip-abduction-machine'],
  'adductors': ['copenhagen-plank'],
  'calves': ['leg-press-calf-raise'],
  'abs': ['cable-crunch'],
  'obliques': ['cable-woodchop'],
};

/** The starting choices: the questionnaire answers, and the first option for any slot left empty. */
export function defaultPicks(): ProgramPicks {
  const base = firstOptionPicks();
  const out: ProgramPicks = {};
  for (const slot of PROGRAM_SLOTS) {
    const mine = (CHOSEN_PICKS[slot.id] ?? []).filter((id) => slot.options.includes(id)).slice(0, 2);
    out[slot.id] = mine.length ? mine : base[slot.id]!;
  }
  return out;
}

/** Keeps only valid picks, falling back to the defaults. */
export function normalizePicks(picks: ProgramPicks | undefined | null): Record<SlotId, LibraryExerciseId[]> {
  const base = defaultPicks();
  const out = {} as Record<SlotId, LibraryExerciseId[]>;
  for (const slot of PROGRAM_SLOTS) {
    const mine = (picks?.[slot.id] ?? []).filter((id) => slot.options.includes(id)).slice(0, 2);
    out[slot.id] = mine.length ? mine : base[slot.id]!;
  }
  return out;
}

/** Tapping cycles an option through first choice, second choice, and not chosen. */
export function togglePick(current: LibraryExerciseId[], id: LibraryExerciseId, allowSecond: boolean): LibraryExerciseId[] {
  if (current.includes(id)) return current.filter((x) => x !== id);
  if (!allowSecond || current.length === 0) return [id];
  return [current[0]!, id];
}

export function pickFor(picks: Record<SlotId, LibraryExerciseId[]>, entry: SlotEntry): LibraryExerciseId {
  const list = picks[entry.slot];
  return list[entry.choice] ?? list[0]!;
}

/**
 * The exercise for a slot that the wrist allows: the athlete's pick when it fits, otherwise their
 * other pick, otherwise the first equivalent option that fits. Null when no option fits.
 */
export function wristSafePick(picks: Record<SlotId, LibraryExerciseId[]>, entry: SlotEntry, wrist: WristStatus): LibraryExerciseId | null {
  const first = pickFor(picks, entry);
  const order = [first, ...picks[entry.slot], ...SLOT_BY_ID[entry.slot].options];
  return order.find((id) => wristAllows(id, wrist)) ?? null;
}

// ---------- Building plan items ----------

/** Reps in reserve for work sets. Holds have none. Nothing is prescribed to failure. */
export function effortFor(exerciseId: string, slot: ProgramSlot): Pick<PlanItem, 'rir'> {
  const ex = exercise(exerciseId);
  if (!ex || ex.kind === 'hold') return {};
  return { rir: slot.rirShort };
}

/** The gym session of one program day, with the athlete's choices, fitted to the wrist. */
export function buildMainItems(day: ProgramDay, picks: Record<SlotId, LibraryExerciseId[]>, wrist: WristStatus = 'cleared'): PlanItem[] {
  const out: PlanItem[] = [];
  for (const entry of day.main) {
    const n = out.length + 1;
    if ('fixed' in entry) {
      out.push({ ...entry.fixed, id: `${day.key}-${n}-${entry.fixed.exerciseId}`, session: 'main', notes: [...entry.fixed.notes] });
      continue;
    }
    const slot = SLOT_BY_ID[entry.slot];
    const exerciseId = wristSafePick(picks, entry, wrist);
    if (!exerciseId) continue;
    const ex = exercise(exerciseId);
    const hold = ex?.kind === 'hold';
    const reps = entry.reps ?? slot.reps;
    const item: PlanItem = {
      id: `${day.key}-${n}-${exerciseId}`,
      exerciseId,
      session: 'main',
      sets: entry.sets ?? slot.sets,
      target: hold ? { type: 'hold', seconds: slot.holdSeconds ?? 20 } : r(reps[0], reps[1]),
      restSec: entry.restSec ?? slot.restSec,
      notes: [],
      ...effortFor(exerciseId, slot),
    };
    if (exerciseId !== pickFor(picks, entry)) item.notes.push(`Planned instead of ${exercise(pickFor(picks, entry))?.name ?? 'your pick'} while the wrist is not cleared.`);
    if (ex?.logSides) item.per = 'side';
    if (ex?.laterality === 'alternating') item.notes.push('Count the reps for each leg.');
    out.push(item);
  }
  return out;
}
