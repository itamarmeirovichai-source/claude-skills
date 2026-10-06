import { z } from 'zod';
import type { WristStatus } from '../content/traits';

// The athlete profile added in 3.0.0: facts that decide what the plan may contain, kept on the
// phone in the key value table so backups carry them. Every value can be "unknown", and unknown
// is always treated cautiously. None of this is a diagnosis or a clearance.

const dateKey = z.string().regex(/^\d{4}-\d{2}-\d{2}$/);

export const WristInfoSchema = z.object({
  status: z.enum(['unknown', 'not-cleared', 'cleared', 'symptoms']),
  /** Who confirmed the clearance, for example "orthopaedic surgeon". */
  clearedBy: z.string().max(80),
  date: dateKey.nullable(),
  /** Any limits the clinician gave, in their words. */
  limits: z.string().max(300),
});
export type WristInfo = z.infer<typeof WristInfoSchema>;
export const DEFAULT_WRIST: WristInfo = { status: 'unknown', clearedBy: '', date: null, limits: '' };

export const HomeSetupSchema = z.object({
  space: z.enum(['unknown', 'small', 'medium', 'large']),
  ceiling: z.enum(['unknown', 'low', 'standard', 'high']),
  surface: z.enum(['unknown', 'slippery', 'hard', 'mat', 'carpet']),
  noiseLimits: z.enum(['unknown', 'yes', 'no']),
  /** People, pets, or breakable things close to where you train. */
  breakables: z.enum(['unknown', 'yes', 'no']),
  outdoor: z.enum(['unknown', 'none', 'small', 'large']),
  outdoorSurface: z.enum(['unknown', 'grass', 'court', 'concrete']),
  equipment: z.array(z.enum(['mat', 'box', 'cones', 'ball', 'wall', 'rope', 'tape', 'light-dumbbells'])),
});
export type HomeSetup = z.infer<typeof HomeSetupSchema>;
export const DEFAULT_HOME: HomeSetup = { space: 'unknown', ceiling: 'unknown', surface: 'unknown', noiseLimits: 'unknown', breakables: 'unknown', outdoor: 'unknown', outdoorSurface: 'unknown', equipment: [] };

const sportWeek = z.object({ sessions: z.number().int().min(0).max(14).nullable(), minutes: z.number().int().min(0).max(1500).nullable() });
export const SportLoadSchema = z.object({
  basketball: sportWeek,
  volleyball: sportWeek,
  other: sportWeek.extend({ name: z.string().max(60) }),
  /** Whether jumping in school sport is light, some, or a lot in a usual week. */
  jumping: z.enum(['unknown', 'little', 'some', 'lots']),
  confirmed: z.boolean(),
});
export type SportLoad = z.infer<typeof SportLoadSchema>;
export const DEFAULT_SPORT: SportLoad = {
  basketball: { sessions: null, minutes: null },
  volleyball: { sessions: null, minutes: null },
  other: { sessions: null, minutes: null, name: '' },
  jumping: 'unknown',
  confirmed: false,
};

export const WeightPrefsSchema = z.object({
  /** frequent: several mornings a week. weekly: one morning a week. off: no weighing. */
  mode: z.enum(['frequent', 'weekly', 'off']),
  hideNumbers: z.boolean(),
});
export type WeightPrefs = z.infer<typeof WeightPrefsSchema>;
export const DEFAULT_WEIGHT_PREFS: WeightPrefs = { mode: 'weekly', hideNumbers: false };

export const KosherPrefsSchema = z.object({
  enabled: z.boolean(),
  /** Hours waited after meat before dairy, as the family's custom. */
  meatToDairyHours: z.number().min(0).max(8),
});
export type KosherPrefs = z.infer<typeof KosherPrefsSchema>;
/** Six hours is the most widespread custom and the cautious default; each family sets its own. */
export const DEFAULT_KOSHER_HOURS = 6;
export const DEFAULT_KOSHER: KosherPrefs = { enabled: true, meatToDairyHours: DEFAULT_KOSHER_HOURS };

/** A goal in the athlete's own words, kept apart from any professionally reviewed target. */
export const AspirationSchema = z.object({
  id: z.string().min(1).max(40),
  text: z.string().min(1).max(300),
  recordedOn: dateKey,
});
export type Aspiration = z.infer<typeof AspirationSchema>;

/**
 * A target that a professional set or reviewed. PeakForm never invents one. Recording who, when,
 * and the units keeps it honest, and "discussed with a parent" is kept apart from a professional review.
 */
export const ReviewedTargetSchema = z.object({
  id: z.string().min(1).max(40),
  kind: z.enum(['energy', 'protein', 'body-composition', 'weight', 'supplement', 'training', 'other']),
  /** The target in the professional's words, for example "about 3,000 kcal on training days". */
  value: z.string().min(1).max(200),
  units: z.string().max(40),
  source: z.string().min(1).max(120),
  role: z.enum(['pediatrician', 'pediatric sports dietitian', 'dietitian', 'physiotherapist', 'orthopaedic clinician', 'qualified coach', 'other']),
  date: dateKey,
  status: z.enum(['professionally reviewed', 'discussed with a parent only']),
  /** Daily energy range in kcal, only when the professional gave numbers. Used for display, never as a limit. */
  kcalRange: z.tuple([z.number().min(500).max(8000), z.number().min(500).max(8000)]).nullable(),
  notes: z.string().max(500),
});
export type ReviewedTarget = z.infer<typeof ReviewedTargetSchema>;

/** Supplement details that matter for a review. Creatine is never started or increased by PeakForm. */
export const SupplementReviewSchema = z.object({
  creatineProduct: z.string().max(120),
  creatineDoseG: z.number().min(0).max(30).nullable(),
  startedOn: dateKey.nullable(),
  thirdPartyTested: z.enum(['unknown', 'yes', 'no']),
  kosherCertified: z.enum(['unknown', 'yes', 'no']),
  reviewedBy: z.string().max(120),
});
export type SupplementReview = z.infer<typeof SupplementReviewSchema>;
export const DEFAULT_SUPPLEMENT_REVIEW: SupplementReview = { creatineProduct: '', creatineDoseG: null, startedOn: null, thirdPartyTested: 'unknown', kosherCertified: 'unknown', reviewedBy: '' };

/** A vegetable eaten in large amounts most days, such as green beans, described well enough to calculate it honestly. */
export const UsualVegSchema = z.object({
  grams: z.number().min(0).max(3000).nullable(),
  state: z.enum(['unknown', 'raw', 'frozen-cooked', 'boiled-drained', 'canned-drained']),
  /** Whether the beans were added on top of the usual food or replaced something. */
  role: z.enum(['unknown', 'added', 'replaced']),
  oilG: z.number().min(0).max(100).nullable(),
  sauce: z.string().max(120),
  stomach: z.enum(['unknown', 'fine', 'bloating', 'discomfort']),
  weighed: z.enum(['unknown', 'weighed', 'estimated']),
});
export type UsualVeg = z.infer<typeof UsualVegSchema>;
export const DEFAULT_USUAL_VEG: UsualVeg = { grams: null, state: 'unknown', role: 'unknown', oilG: null, sauce: '', stomach: 'unknown', weighed: 'unknown' };

/** Basic facts that need a yes before they are used in any calculation. */
export const BasicsSchema = z.object({
  heightConfirmed: z.boolean(),
  heightMeasuredOn: dateKey.nullable(),
  /** Who supervises gym sessions, if anyone. */
  supervision: z.enum(['unknown', 'none', 'gym staff', 'qualified coach', 'parent']),
  typicalSleepH: z.number().min(0).max(14).nullable(),
  wakeTime: z.string().regex(/^\d{2}:\d{2}$/).nullable(),
  schoolEnds: z.string().regex(/^\d{2}:\d{2}$/).nullable(),
});
export type Basics = z.infer<typeof BasicsSchema>;
export const DEFAULT_BASICS: Basics = { heightConfirmed: false, heightMeasuredOn: null, supervision: 'unknown', typicalSleepH: null, wakeTime: null, schoolEnds: null };

export interface AthleteProfile {
  basics: Basics;
  wrist: WristInfo;
  home: HomeSetup;
  sport: SportLoad;
  weight: WeightPrefs;
  kosher: KosherPrefs;
  supplements: SupplementReview;
  veg: UsualVeg;
  aspirations: Aspiration[];
  reviewed: ReviewedTarget[];
}

export const DEFAULT_ATHLETE: AthleteProfile = {
  basics: DEFAULT_BASICS,
  wrist: DEFAULT_WRIST,
  home: DEFAULT_HOME,
  sport: DEFAULT_SPORT,
  weight: DEFAULT_WEIGHT_PREFS,
  kosher: DEFAULT_KOSHER,
  supplements: DEFAULT_SUPPLEMENT_REVIEW,
  veg: DEFAULT_USUAL_VEG,
  aspirations: [],
  reviewed: [],
};

/** Reads a stored value, falling back to the default when it is missing or no longer valid. */
export function parseOr<T>(schema: z.ZodType<T>, value: unknown, fallback: T): T {
  const r = schema.safeParse(value);
  return r.success ? r.data : fallback;
}

export function parseAthlete(raw: Partial<Record<keyof AthleteProfile, unknown>>): AthleteProfile {
  return {
    basics: parseOr(BasicsSchema, raw.basics, DEFAULT_BASICS),
    wrist: parseOr(WristInfoSchema, raw.wrist, DEFAULT_WRIST),
    home: parseOr(HomeSetupSchema, raw.home, DEFAULT_HOME),
    sport: parseOr(SportLoadSchema, raw.sport, DEFAULT_SPORT),
    weight: parseOr(WeightPrefsSchema, raw.weight, DEFAULT_WEIGHT_PREFS),
    kosher: parseOr(KosherPrefsSchema, raw.kosher, DEFAULT_KOSHER),
    supplements: parseOr(SupplementReviewSchema, raw.supplements, DEFAULT_SUPPLEMENT_REVIEW),
    veg: parseOr(UsualVegSchema, raw.veg, DEFAULT_USUAL_VEG),
    aspirations: parseOr(z.array(AspirationSchema), raw.aspirations, []),
    reviewed: parseOr(z.array(ReviewedTargetSchema), raw.reviewed, []),
  };
}

export function wristStatusOf(a: Pick<AthleteProfile, 'wrist'>): WristStatus {
  return a.wrist.status;
}

/** The reviewed energy target, if a professional gave one. Never a limit: it is shown for reference. */
export function reviewedEnergy(a: Pick<AthleteProfile, 'reviewed'>): ReviewedTarget | null {
  const list = a.reviewed.filter((r) => r.kind === 'energy' && r.status === 'professionally reviewed').sort((x, y) => y.date.localeCompare(x.date));
  return list[0] ?? null;
}

// ---------- Things to confirm ----------

export interface OpenQuestion {
  id: 'height' | 'wrist' | 'sport' | 'home' | 'creatine' | 'veg' | 'supervision' | 'sleep';
  title: string;
  why: string;
  /** Blocks or limits part of the plan until answered. */
  gates: boolean;
}

/** The facts PeakForm still needs, most important first. Answers stay on the phone. */
export function openQuestions(a: AthleteProfile, opts: { creatineActive: boolean }): OpenQuestion[] {
  const out: OpenQuestion[] = [];
  if (a.wrist.status === 'unknown') out.push({ id: 'wrist', title: 'Wrist after an injury', why: 'If a wrist or forearm injury is still healing, PeakForm keeps loads on gripping and pressing exercises the same and plans no ball contact or falls onto the hands until a clinician confirms it is cleared. If there was no injury, say so once.', gates: true });
  if (a.home.space === 'unknown' || a.home.ceiling === 'unknown' || a.home.surface === 'unknown' || a.home.outdoor === 'unknown') out.push({ id: 'home', title: 'Your space at home', why: 'Jumps need room, a safe floor, and a high enough ceiling. Until this is answered, home sessions use quiet drills without jumps.', gates: true });
  if (!a.sport.confirmed) out.push({ id: 'sport', title: 'School and club sport', why: 'Basketball and volleyball add jumps and training hours. They count toward the same weekly load as the plan.', gates: false });
  if (!a.basics.heightConfirmed) out.push({ id: 'height', title: 'Height', why: 'Measure it again before it is used in any calculation. You are still growing.', gates: false });
  if (opts.creatineActive && (!a.supplements.creatineProduct || a.supplements.creatineDoseG === null)) out.push({ id: 'creatine', title: 'Creatine product and dose', why: 'A parent and a clinician can only review it with the product name and the daily dose.', gates: false });
  if (a.veg.grams !== null && a.veg.grams > 0 && (a.veg.state === 'unknown' || a.veg.role === 'unknown')) out.push({ id: 'veg', title: 'Your large vegetable portion', why: 'Raw, frozen, and cooked weights give different numbers, and oil or sauce adds more. PeakForm only calculates what it knows.', gates: false });
  if (a.basics.supervision === 'unknown') out.push({ id: 'supervision', title: 'Supervision at the gym', why: 'Youth strength guidance asks for qualified supervision, especially for new exercises.', gates: false });
  return out;
}
