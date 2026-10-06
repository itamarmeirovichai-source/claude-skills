import { z } from 'zod';

// Typed, versioned record schemas. Every stored record has a stable ID, created and
// updated times (epoch ms), and explicit units in field names or comments.
// Plan data (plans table) is separate from logged data (everything else).

export const SCHEMA_VERSION = 1;

const id = z.string().min(1).max(80);
const ms = z.number().int().nonnegative();
const dateKey = z.string().regex(/^\d{4}-\d{2}-\d{2}$/);
const hhmm = z.string().regex(/^\d{2}:\d{2}$/);
const shortText = z.string().max(2000);

const base = { id, createdAt: ms, updatedAt: ms };

// ---------- Settings and profile ----------

export const ReminderSchema = z.object({
  id,
  label: z.string().max(80),
  time: hhmm,
  /** 0 = Sunday. */
  weekdays: z.array(z.number().int().min(0).max(6)),
  enabled: z.boolean(),
  kind: z.enum(['checkin', 'meal', 'training', 'sleep', 'review', 'supplement', 'custom']),
});
export type Reminder = z.infer<typeof ReminderSchema>;

export const SupplementSchema = z.object({
  id,
  name: z.string().max(80),
  kind: z.enum(['creatine', 'calcium', 'omega3', 'protein', 'other']),
  product: z.string().max(120),
  dose: z.number().nonnegative(),
  unit: z.string().max(20),
  /** Calcium supplement mg per dose, for calcium totals. */
  calciumMg: z.number().nonnegative().optional(),
  /** EPA plus DHA mg per dose, from the label. */
  epaDhaMg: z.number().nonnegative().optional(),
  reviewedWithGuardian: z.boolean(),
  active: z.boolean(),
});
export type Supplement = z.infer<typeof SupplementSchema>;

export const AppSettingsSchema = z.object({
  ...base,
  schemaVersion: z.number().int(),
  appName: z.string().min(1).max(40),
  theme: z.enum(['system', 'light', 'dark']),
  reducedMotion: z.enum(['system', 'on', 'off']),
  units: z.object({ weight: z.enum(['kg', 'lb']), length: z.enum(['cm', 'in']), clock: z.enum(['24h', '12h']) }),
  autoStartRest: z.boolean(),
  restSound: z.enum(['off', 'beep', 'chime']),
  vibration: z.boolean(),
  keepScreenOn: z.boolean(),
  poolLengthM: z.number().positive().nullable(),
  sessionTimes: z.object({ morning: hhmm, main: z.record(z.string(), hhmm), swim: z.record(z.string(), hhmm), home: z.record(z.string(), hhmm).optional() }),
  equipment: z.object({
    barbellKg: z.number().positive(),
    machineKg: z.number().positive(),
    cableKg: z.number().positive(),
    dumbbellKg: z.number().positive(),
    upperPct: z.number().min(0).max(0.1),
    lowerPct: z.number().min(0).max(0.1),
  }),
  sabbath: z.object({
    enabled: z.boolean(),
    mode: z.enum(['manual', 'city']),
    fridayStart: hhmm,
    saturdayEnd: hhmm,
    cityId: z.string().max(40).nullable(),
    candleOffsetMin: z.number().int().min(0).max(90),
    endOffsetMin: z.number().int().min(0).max(120),
  }),
  reminders: z.array(ReminderSchema),
  supplements: z.array(SupplementSchema),
  lock: z.object({
    enabled: z.boolean(),
    pinHash: z.string().max(200).nullable(),
    salt: z.string().max(100).nullable(),
    idleMinutes: z.number().int().min(1).max(120),
  }),
  coachShare: z.object({ includePhotos: z.boolean(), includeNotes: z.boolean() }),
  activePlanId: id,
  onboarded: z.boolean(),
  demoData: z.boolean(),
  eventDate: dateKey.nullable(),
  eventLabel: z.string().max(80),
  planStartDate: dateKey.nullable(),
  guardianReviewAck: z.boolean(),
  deploymentUrl: z.string().max(300),
});
export type AppSettings = z.infer<typeof AppSettingsSchema>;

export const UserProfileSchema = z.object({
  ...base,
  name: z.string().max(60),
  birthYear: z.number().int().min(1900).max(2100).nullable(),
  heightCm: z.number().positive().max(250).nullable(),
  startWeightKg: z.number().positive().max(300).nullable(),
  startBodyFatPct: z.number().min(2).max(70).nullable(),
  goals: z.array(z.string().max(200)),
  medicalNotes: z.string().max(1000),
  allergies: z.string().max(500),
});
export type UserProfile = z.infer<typeof UserProfileSchema>;

// ---------- Plans ----------

export const SetTargetSchema = z.discriminatedUnion('type', [
  z.object({ type: z.literal('reps'), min: z.number().int().min(0), max: z.number().int().min(0) }),
  z.object({ type: z.literal('duration'), totalMin: z.number().positive(), workSec: z.number().optional(), restSec: z.number().optional() }),
  z.object({ type: z.literal('hold'), seconds: z.number().positive() }),
  z.object({ type: z.literal('roundTrips'), count: z.number().int().positive() }),
]);

export const PlanItemSchema = z.object({
  id,
  exerciseId: id,
  session: z.enum(['morning', 'home', 'main', 'swim']),
  sets: z.number().int().min(1).max(20),
  target: SetTargetSchema,
  restSec: z.number().int().min(0).max(1800),
  rir: z.number().min(0).max(6).optional(),
  lastSetRir: z.number().min(0).max(6).optional(),
  rpe: z.tuple([z.number(), z.number()]).optional(),
  tempo: z.string().max(8).optional(),
  per: z.enum(['side', 'direction']).optional(),
  notes: z.array(z.string().max(300)),
});

const weekday = z.union([z.literal(0), z.literal(1), z.literal(2), z.literal(3), z.literal(4), z.literal(5), z.literal(6)]);

export const PlanDaySchema = z.object({
  weekday,
  key: z.enum(['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']),
  title: z.string().max(80),
  short: z.string().max(40),
  isRest: z.boolean(),
  items: z.array(PlanItemSchema),
  restNotes: z.array(z.string()).optional(),
});

export const PlanRecordSchema = z.object({
  ...base,
  planKey: z.string().max(40),
  version: z.number().int().positive(),
  name: z.string().max(80),
  days: z.array(PlanDaySchema).length(7),
  globalRules: z.array(z.string()),
  changeNote: z.string().max(300),
});
export type PlanRecord = z.infer<typeof PlanRecordSchema>;

// ---------- Training logs ----------

export const WorkoutSessionSchema = z.object({
  ...base,
  date: dateKey,
  weekday: z.number().int().min(0).max(6),
  /** Weekday of the plan day that was performed. Differs from weekday when a session was moved. */
  planWeekday: z.number().int().min(0).max(6),
  planId: id,
  planVersion: z.number().int(),
  session: z.enum(['morning', 'home', 'main', 'swim']),
  title: z.string().max(100),
  status: z.enum(['active', 'done', 'abandoned']),
  startedAt: ms,
  finishedAt: ms.nullable(),
  /** Snapshot of the prescription the session was performed against. */
  planSnapshot: z.array(PlanItemSchema),
  sessionRpe: z.number().min(0).max(10).nullable(),
  recovery: z.object({ energy: z.number().min(1).max(5).nullable(), soreness: z.number().min(0).max(3).nullable() }).nullable(),
  poolLengthM: z.number().positive().nullable(),
  note: shortText,
  /** Planned date if this session was moved from another day. */
  rescheduledFrom: dateKey.nullable(),
});
export type WorkoutSession = z.infer<typeof WorkoutSessionSchema>;

export const ExerciseSessionSchema = z.object({
  ...base,
  sessionId: id,
  planItemId: id,
  order: z.number().int(),
  exerciseId: id,
  /** Original prescribed exercise when a substitution was made. */
  originalExerciseId: id.nullable(),
  substitutionReason: z.string().max(300).nullable(),
  skipped: z.boolean(),
  skipReason: z.string().max(300).nullable(),
  note: shortText,
});
export type ExerciseSession = z.infer<typeof ExerciseSessionSchema>;

export const SetLogSchema = z.object({
  ...base,
  sessionId: id,
  exerciseSessionId: id,
  exerciseId: id,
  planItemId: id,
  setIndex: z.number().int().min(0),
  side: z.enum(['left', 'right']).nullable(),
  warmup: z.boolean(),
  weightKg: z.number().min(0).max(1000).nullable(),
  reps: z.number().int().min(0).max(500).nullable(),
  rir: z.number().min(0).max(10).nullable(),
  seconds: z.number().min(0).max(36000).nullable(),
  form: z.enum(['good', 'acceptable', 'poor']).nullable(),
  pain: z.enum(['none', 'mild', 'stop']),
  painScore: z.number().int().min(0).max(10).nullable(),
  /** Quality 1 to 5 for jumps, sprints, throws, and skills. */
  quality: z.number().int().min(1).max(5).nullable(),
  landing: z.enum(['good', 'ok', 'poor']).nullable(),
  reachCm: z.number().min(0).max(400).nullable(),
  timeSec: z.number().min(0).max(36000).nullable(),
  roundTrips: z.number().int().min(0).max(200).nullable(),
  stroke: z.string().max(40).nullable(),
  rpe: z.number().min(0).max(10).nullable(),
  symptoms: z.string().max(300).nullable(),
  note: shortText,
  completedAt: ms,
});
export type SetLog = z.infer<typeof SetLogSchema>;

export const SuggestionTargetSchema = z.object({
  setIndex: z.number().int(),
  side: z.enum(['left', 'right']).nullable(),
  reps: z.number().nullable(),
  weightKg: z.number().nullable(),
  seconds: z.number().nullable(),
});

export const ProgressionSuggestionSchema = z.object({
  ...base,
  exerciseId: id,
  planItemId: id,
  basedOnSessionId: id,
  kind: z.enum(['add_reps', 'add_load', 'hold', 'reduce', 'pain_hold', 'quality_hold', 'coach_review', 'complete_sets']),
  title: z.string().max(200),
  reason: z.string().max(1000),
  targets: z.array(SuggestionTargetSchema),
  status: z.enum(['pending', 'accepted', 'dismissed']),
  decidedAt: ms.nullable(),
});
export type ProgressionSuggestionRecord = z.infer<typeof ProgressionSuggestionSchema>;

export const FourExposureReviewSchema = z.object({
  ...base,
  exerciseId: id,
  exposureNumber: z.number().int(),
  sessionIds: z.array(id),
  recommendation: z.enum(['progress', 'hold', 'reduce', 'change_technique', 'coach_review']),
  summary: z.string().max(1000),
  details: z.array(z.string().max(400)),
  status: z.enum(['pending', 'seen']),
});
export type FourExposureReviewRecord = z.infer<typeof FourExposureReviewSchema>;

// ---------- Nutrition logs ----------

export const NutrientsSchema = z.object({
  kcal: z.number(),
  protein: z.number(),
  carbs: z.number(),
  fat: z.number(),
  fibre: z.number(),
  calcium: z.number(),
  caffeine: z.number().optional(),
});

export const PortionEstimateSchema = z.object({
  method: z.enum(['weighed', 'label', 'template', 'household', 'hand', 'restaurant', 'plate-guide']),
  portion: z.string().max(40).nullable(),
  count: z.number().nonnegative().nullable(),
  gramsMid: z.number().nonnegative(),
  gramsLow: z.number().nonnegative(),
  gramsHigh: z.number().nonnegative(),
  confidence: z.enum(['high', 'medium', 'low']),
});
export type PortionEstimate = z.infer<typeof PortionEstimateSchema>;

export const FoodLogItemSchema = z.object({
  foodId: z.string().max(80).nullable(),
  name: z.string().max(120),
  estimate: PortionEstimateSchema,
  mid: NutrientsSchema,
  low: NutrientsSchema,
  high: NutrientsSchema,
  /** When the user swapped a default food, the original food ID. */
  substitutedFrom: z.string().max(80).nullable(),
});
export type FoodLogItem = z.infer<typeof FoodLogItemSchema>;

export const FoodLogSchema = z.object({
  ...base,
  date: dateKey,
  slot: z.enum(['breakfast', 'lunch', 'preworkout', 'dinner', 'evening', 'sabbath', 'snack', 'other']),
  time: hhmm,
  source: z.enum(['template', 'manual', 'estimate', 'restaurant', 'sabbath', 'barcode']),
  templateId: z.string().max(80).nullable(),
  /** True when the default template was logged unchanged. */
  asPlanned: z.boolean(),
  items: z.array(FoodLogItemSchema),
  photoId: z.string().max(80).nullable(),
  note: shortText,
  /** Hidden oil allowance applied, grams of oil [low, mid, high]. */
  hiddenOil: z.tuple([z.number(), z.number(), z.number()]).nullable(),
});
export type FoodLog = z.infer<typeof FoodLogSchema>;

export const WaterLogSchema = z.object({
  ...base,
  date: dateKey,
  at: ms,
  ml: z.number().int().min(0).max(5000),
  drink: z.enum(['water', 'coke-zero', 'zero-drink']),
});
export type WaterLog = z.infer<typeof WaterLogSchema>;

export const DayNoteSchema = z.object({
  ...base,
  date: dateKey,
  kind: z.enum(['not-hungry', 'schedule-changed', 'ate-out', 'other']),
  note: shortText,
});
export type DayNote = z.infer<typeof DayNoteSchema>;

// ---------- Body, sleep, pain ----------

export const PAIN_REGIONS = ['achilles', 'heel', 'shin', 'knee', 'lowBack', 'shoulder', 'wrist', 'elbowWrist'] as const;
export type PainRegion = (typeof PAIN_REGIONS)[number];
export const PAIN_REGION_LABELS: Record<PainRegion, string> = {
  achilles: 'Achilles',
  heel: 'Heel',
  shin: 'Shin',
  knee: 'Knee',
  lowBack: 'Low back',
  shoulder: 'Shoulder',
  wrist: 'Wrist',
  elbowWrist: 'Elbow',
};

export const SORENESS_REGIONS = ['legs', 'glutes', 'back', 'chest', 'shoulders', 'arms', 'calves'] as const;

export const RED_FLAGS = [
  'fainting',
  'chest-pain',
  'breathless',
  'severe-dizziness',
  'dark-urine',
  'worsening-injury',
  'repeated-illness',
  'severe-restriction',
] as const;
export type RedFlag = (typeof RED_FLAGS)[number];
export const RED_FLAG_LABELS: Record<RedFlag, string> = {
  fainting: 'Fainting or nearly fainting',
  'chest-pain': 'Chest pain',
  breathless: 'Shortness of breath outside normal exercise',
  'severe-dizziness': 'Severe dizziness',
  'dark-urine': 'Dark urine',
  'worsening-injury': 'An injury that is getting worse',
  'repeated-illness': 'Getting ill again and again',
  'severe-restriction': 'Eating far less than planned or skipping many meals',
};

export const BodyCheckInSchema = z.object({
  ...base,
  date: dateKey,
  at: ms,
  weightKg: z.number().min(20).max(300).nullable(),
  bodyFatPct: z.number().min(2).max(70).nullable(),
  /** Morning standard conditions: after the toilet, before food or drink. */
  standardConditions: z.boolean(),
  energy: z.number().int().min(1).max(5).nullable(),
  mood: z.number().int().min(1).max(5).nullable(),
  concentration: z.number().int().min(1).max(5).nullable(),
  hunger: z.number().int().min(1).max(5).nullable(),
  soreness: z.record(z.string(), z.number().int().min(0).max(3)),
  illness: z.boolean(),
  illnessNote: z.string().max(300),
  hydrationNote: z.string().max(300),
  redFlags: z.array(z.enum(RED_FLAGS)),
  note: shortText,
});
export type BodyCheckIn = z.infer<typeof BodyCheckInSchema>;

export const WaistMeasurementSchema = z.object({
  ...base,
  date: dateKey,
  cm: z.number().min(30).max(200),
  standardConditions: z.boolean(),
});
export type WaistMeasurement = z.infer<typeof WaistMeasurementSchema>;

export const SleepLogSchema = z.object({
  ...base,
  /** The morning the sleep ended. */
  date: dateKey,
  bedtime: hhmm,
  wakeTime: hhmm,
  durationMin: z.number().int().min(0).max(1440),
  quality: z.number().int().min(1).max(5).nullable(),
});
export type SleepLog = z.infer<typeof SleepLogSchema>;

export const PainLogSchema = z.object({
  ...base,
  date: dateKey,
  at: ms,
  region: z.string().max(40),
  score: z.number().int().min(0).max(10),
  source: z.enum(['checkin', 'workout']),
  exerciseId: z.string().max(80).nullable(),
  note: z.string().max(300),
});
export type PainLog = z.infer<typeof PainLogSchema>;

export const SupplementLogSchema = z.object({
  ...base,
  date: dateKey,
  at: ms,
  supplementId: id,
  amount: z.number().nonnegative(),
  unit: z.string().max(20),
});
export type SupplementLog = z.infer<typeof SupplementLogSchema>;

/** School and club sport, logged so it counts toward the same weekly load as the plan (3.0.0). */
export const SportLogSchema = z.object({
  ...base,
  date: dateKey,
  sport: z.enum(['volleyball', 'basketball', 'other']),
  name: z.string().max(60),
  minutes: z.number().int().min(0).max(600),
  intensity: z.enum(['light', 'moderate', 'hard']),
  jumping: z.enum(['little', 'some', 'lots']),
  note: z.string().max(300),
});
export type SportLog = z.infer<typeof SportLogSchema>;

// ---------- Reviews, exports, media, misc ----------

export const WeeklyReviewSchema = z.object({
  ...base,
  weekStart: dateKey,
  generatedAt: ms,
  data: z.unknown(),
});
export type WeeklyReviewRecord = z.infer<typeof WeeklyReviewSchema>;

export const CalendarExportSchema = z.object({
  ...base,
  eventCount: z.number().int(),
  reminderHash: z.string().max(80),
  untilDate: dateKey,
});
export type CalendarExport = z.infer<typeof CalendarExportSchema>;

export const BackupManifestSchema = z.object({
  ...base,
  kind: z.enum(['plain', 'encrypted', 'snapshot', 'coach-report', 'csv']),
  checksum: z.string().max(100),
  counts: z.record(z.string(), z.number().int()),
  note: z.string().max(200),
});
export type BackupManifest = z.infer<typeof BackupManifestSchema>;

export const SnapshotSchema = z.object({
  ...base,
  reason: z.string().max(200),
  payload: z.string(),
});
export type Snapshot = z.infer<typeof SnapshotSchema>;

export const MediaStatusSchema = z.object({
  ...base,
  mediaId: id,
  status: z.enum(['user-confirmed', 'user-rejected']),
  note: z.string().max(300),
});
export type MediaStatus = z.infer<typeof MediaStatusSchema>;

export const PhotoSchema = z.object({
  ...base,
  mime: z.string().max(40),
  bytes: z.number().int(),
  /** Stored as a data URL string so it round trips through JSON backups. */
  dataUrl: z.string(),
});
export type Photo = z.infer<typeof PhotoSchema>;

export const TimerHistorySchema = z.object({
  ...base,
  label: z.string().max(120),
  durationSec: z.number().int(),
  startedAt: ms,
  endedAt: ms,
  completed: z.boolean(),
});
export type TimerHistory = z.infer<typeof TimerHistorySchema>;

export const CustomExerciseSchema = z.object({
  ...base,
  name: z.string().min(1).max(80),
  kind: z.enum(['strength', 'bodyweight', 'hold', 'jump', 'sprint', 'skill', 'throw', 'conditioning', 'warmup', 'swim']),
  primary: z.array(z.string().max(40)),
  secondary: z.array(z.string().max(40)),
  logSides: z.boolean(),
  loadIncrement: z.enum(['upper', 'lower', 'none']),
  equipment: z.string().max(200),
  notes: z.string().max(1000),
});
export type CustomExercise = z.infer<typeof CustomExerciseSchema>;

export const SchemaMigrationSchema = z.object({
  ...base,
  fromVersion: z.number().int(),
  toVersion: z.number().int(),
  appliedAt: ms,
  note: z.string().max(300),
});
export type SchemaMigration = z.infer<typeof SchemaMigrationSchema>;

export const KvSchema = z.object({ id, value: z.unknown(), updatedAt: ms });
export type Kv = z.infer<typeof KvSchema>;

/** Table name to schema. Order matters for import. */
export const TABLE_SCHEMAS = {
  settings: AppSettingsSchema,
  profile: UserProfileSchema,
  plans: PlanRecordSchema,
  sessions: WorkoutSessionSchema,
  exerciseSessions: ExerciseSessionSchema,
  setLogs: SetLogSchema,
  suggestions: ProgressionSuggestionSchema,
  fourReviews: FourExposureReviewSchema,
  foodLogs: FoodLogSchema,
  waterLogs: WaterLogSchema,
  dayNotes: DayNoteSchema,
  checkins: BodyCheckInSchema,
  waist: WaistMeasurementSchema,
  sleep: SleepLogSchema,
  pain: PainLogSchema,
  supplementLogs: SupplementLogSchema,
  sportLogs: SportLogSchema,
  weeklyReviews: WeeklyReviewSchema,
  calendarExports: CalendarExportSchema,
  backups: BackupManifestSchema,
  mediaStatus: MediaStatusSchema,
  photos: PhotoSchema,
  timerHistory: TimerHistorySchema,
  customExercises: CustomExerciseSchema,
  migrations: SchemaMigrationSchema,
  kv: KvSchema,
} as const;

export type TableName = keyof typeof TABLE_SCHEMAS;
export const TABLE_NAMES = Object.keys(TABLE_SCHEMAS) as TableName[];

/** Tables excluded from backups. Snapshots are local safety copies only. */
export const NON_BACKUP_TABLES: TableName[] = [];
