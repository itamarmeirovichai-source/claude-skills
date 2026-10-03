import Dexie, { type EntityTable } from 'dexie';
import type {
  AppSettings,
  BackupManifest,
  BodyCheckIn,
  CalendarExport,
  CustomExercise,
  DayNote,
  ExerciseSession,
  FoodLog,
  FourExposureReviewRecord,
  Kv,
  MediaStatus,
  PainLog,
  Photo,
  PlanRecord,
  ProgressionSuggestionRecord,
  SchemaMigration,
  SetLog,
  SleepLog,
  Snapshot,
  SupplementLog,
  TableName,
  TimerHistory,
  UserProfile,
  WaistMeasurement,
  WaterLog,
  WeeklyReviewRecord,
  WorkoutSession,
} from './records';

// IndexedDB through Dexie. All data stays on this device.

export class PeakFormDB extends Dexie {
  settings!: EntityTable<AppSettings, 'id'>;
  profile!: EntityTable<UserProfile, 'id'>;
  plans!: EntityTable<PlanRecord, 'id'>;
  sessions!: EntityTable<WorkoutSession, 'id'>;
  exerciseSessions!: EntityTable<ExerciseSession, 'id'>;
  setLogs!: EntityTable<SetLog, 'id'>;
  suggestions!: EntityTable<ProgressionSuggestionRecord, 'id'>;
  fourReviews!: EntityTable<FourExposureReviewRecord, 'id'>;
  foodLogs!: EntityTable<FoodLog, 'id'>;
  waterLogs!: EntityTable<WaterLog, 'id'>;
  dayNotes!: EntityTable<DayNote, 'id'>;
  checkins!: EntityTable<BodyCheckIn, 'id'>;
  waist!: EntityTable<WaistMeasurement, 'id'>;
  sleep!: EntityTable<SleepLog, 'id'>;
  pain!: EntityTable<PainLog, 'id'>;
  supplementLogs!: EntityTable<SupplementLog, 'id'>;
  weeklyReviews!: EntityTable<WeeklyReviewRecord, 'id'>;
  calendarExports!: EntityTable<CalendarExport, 'id'>;
  backups!: EntityTable<BackupManifest, 'id'>;
  mediaStatus!: EntityTable<MediaStatus, 'id'>;
  photos!: EntityTable<Photo, 'id'>;
  timerHistory!: EntityTable<TimerHistory, 'id'>;
  customExercises!: EntityTable<CustomExercise, 'id'>;
  migrations!: EntityTable<SchemaMigration, 'id'>;
  kv!: EntityTable<Kv, 'id'>;
  snapshots!: EntityTable<Snapshot, 'id'>;

  constructor(name = 'peakform') {
    super(name);
    this.version(1).stores({
      settings: 'id',
      profile: 'id',
      plans: 'id, planKey, version',
      sessions: 'id, date, status, [date+session], startedAt',
      exerciseSessions: 'id, sessionId, exerciseId',
      setLogs: 'id, sessionId, exerciseSessionId, exerciseId, planItemId, completedAt',
      suggestions: 'id, exerciseId, planItemId, status, createdAt',
      fourReviews: 'id, exerciseId, status, createdAt',
      foodLogs: 'id, date, slot, [date+slot]',
      waterLogs: 'id, date',
      dayNotes: 'id, date',
      checkins: 'id, date, at',
      waist: 'id, date',
      sleep: 'id, date',
      pain: 'id, date, region, at',
      supplementLogs: 'id, date, supplementId',
      weeklyReviews: 'id, weekStart',
      calendarExports: 'id, createdAt',
      backups: 'id, createdAt, kind',
      mediaStatus: 'id, mediaId',
      photos: 'id, createdAt',
      timerHistory: 'id, startedAt',
      customExercises: 'id, name',
      migrations: 'id, appliedAt',
      kv: 'id',
      snapshots: 'id, createdAt',
    });
  }

  table_(name: TableName) {
    return this.table(name);
  }
}

export let db = new PeakFormDB();

/** Used by tests to get a fresh database. */
export function resetDbForTests(name: string): PeakFormDB {
  db = new PeakFormDB(name);
  return db;
}
