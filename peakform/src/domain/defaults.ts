import { BASELINE_PLAN } from '../content/plan';
import { DEFAULT_INCREMENTS } from './progression';
import { SCHEMA_VERSION, type AppSettings, type PlanRecord, type Reminder, type UserProfile } from '../db/records';

// Generic defaults. No personal data is stored here. The private profile is entered
// on the device during first run, or imported from a private seed file.

const ALL: number[] = [0, 1, 2, 3, 4, 5, 6];
const SCHOOL_DAYS: number[] = [0, 1, 2, 3, 4, 5];

export const DEFAULT_REMINDERS: Reminder[] = [
  { id: 'checkin', label: 'Morning check in', time: '05:15', weekdays: ALL, enabled: true, kind: 'checkin' },
  { id: 'morning', label: 'Morning volleyball and rope', time: '05:25', weekdays: SCHOOL_DAYS, enabled: true, kind: 'training' },
  { id: 'breakfast', label: 'Breakfast', time: '07:10', weekdays: SCHOOL_DAYS, enabled: true, kind: 'meal' },
  { id: 'lunch', label: 'School lunch', time: '12:00', weekdays: SCHOOL_DAYS, enabled: true, kind: 'meal' },
  { id: 'preworkout', label: 'Pre workout meal', time: '15:20', weekdays: SCHOOL_DAYS, enabled: true, kind: 'meal' },
  { id: 'training', label: 'Get ready for training', time: '16:15', weekdays: SCHOOL_DAYS, enabled: true, kind: 'training' },
  { id: 'dinner', label: 'Dinner after training', time: '18:45', weekdays: SCHOOL_DAYS, enabled: true, kind: 'meal' },
  { id: 'milk', label: 'Evening milk', time: '20:30', weekdays: SCHOOL_DAYS, enabled: true, kind: 'meal' },
  { id: 'winddown', label: 'Wind down for sleep', time: '20:45', weekdays: ALL, enabled: true, kind: 'sleep' },
  { id: 'review', label: 'Weekly review', time: '20:30', weekdays: [0], enabled: true, kind: 'review' },
];

export function defaultSettings(now: number): AppSettings {
  return {
    id: 'app',
    createdAt: now,
    updatedAt: now,
    schemaVersion: SCHEMA_VERSION,
    appName: 'PeakForm',
    theme: 'system',
    reducedMotion: 'system',
    units: { weight: 'kg', length: 'cm', clock: '24h' },
    autoStartRest: true,
    restSound: 'beep',
    vibration: true,
    keepScreenOn: true,
    poolLengthM: null,
    sessionTimes: {
      morning: '05:30',
      main: { '0': '16:30', '1': '16:30', '2': '16:30', '3': '16:30', '4': '16:30', '5': '13:00' },
      swim: { '0': '20:00', '5': '16:30' },
    },
    equipment: { ...DEFAULT_INCREMENTS },
    sabbath: { enabled: true, mode: 'manual', fridayStart: '17:30', saturdayEnd: '18:45', cityId: null, candleOffsetMin: 20, endOffsetMin: 40 },
    reminders: DEFAULT_REMINDERS.map((r) => ({ ...r, weekdays: [...r.weekdays] })),
    supplements: [
      { id: 'creatine', name: 'Creatine monohydrate', kind: 'creatine', product: '', dose: 0, unit: 'g', reviewedWithGuardian: false, active: true },
      { id: 'calcium', name: 'Calcium', kind: 'calcium', product: '', dose: 0, unit: 'tablet', calciumMg: 0, reviewedWithGuardian: false, active: true },
      { id: 'omega3', name: 'Omega 3', kind: 'omega3', product: '', dose: 0, unit: 'capsule', epaDhaMg: 0, reviewedWithGuardian: false, active: true },
    ],
    lock: { enabled: false, pinHash: null, salt: null, idleMinutes: 5 },
    coachShare: { includePhotos: false, includeNotes: false },
    activePlanId: 'baseline-v1',
    onboarded: false,
    demoData: false,
    eventDate: null,
    eventLabel: '',
    planStartDate: null,
    guardianReviewAck: false,
    deploymentUrl: '',
  };
}

export function defaultProfile(now: number): UserProfile {
  return { id: 'me', createdAt: now, updatedAt: now, name: '', birthYear: null, heightCm: null, startWeightKg: null, startBodyFatPct: null, goals: [], medicalNotes: '', allergies: '' };
}

export function baselinePlanRecord(now: number): PlanRecord {
  return {
    id: 'baseline-v1',
    createdAt: now,
    updatedAt: now,
    planKey: BASELINE_PLAN.id,
    version: BASELINE_PLAN.version,
    name: BASELINE_PLAN.name,
    days: BASELINE_PLAN.days.map((d) => ({ ...d, items: d.items.map((i) => ({ ...i, notes: [...i.notes] })) })),
    globalRules: [...BASELINE_PLAN.globalRules],
    changeNote: 'Baseline plan.',
  };
}
