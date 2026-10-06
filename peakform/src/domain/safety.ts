import { RED_FLAG_LABELS, type BodyCheckIn, type PainLog, type SleepLog } from '../db/records';
import type { DateKey } from './dates';
import { addDays } from './dates';

// Safety checks that override progression advice. Pain tracking is not a diagnosis.

export const PAIN_PAUSE_SCORE = 4;

export interface SafetyState {
  stopProgression: boolean;
  urgent: boolean;
  messages: string[];
  pausedRegions: string[];
}

export function safetyState(today: DateKey, checkins: BodyCheckIn[], pain: PainLog[], windowDays = 7): SafetyState {
  const from = addDays(today, -(windowDays - 1));
  const recent = checkins.filter((c) => c.date >= from && c.date <= today);
  const flags = new Set(recent.flatMap((c) => c.redFlags));
  const messages: string[] = [];
  const urgent = flags.size > 0;
  if (urgent) {
    const list = [...flags].map((f) => RED_FLAG_LABELS[f].toLowerCase()).join(', ');
    messages.push(`You recorded ${list}. Progression advice is paused. Tell a parent today and get appropriate medical care. If it is severe or sudden, get help now.`);
  }
  const recentPain = pain.filter((p) => p.date >= from && p.date <= today);
  const byRegion = new Map<string, PainLog[]>();
  for (const p of recentPain) byRegion.set(p.region, [...(byRegion.get(p.region) ?? []), p]);
  const pausedRegions: string[] = [];
  for (const [region, logs] of byRegion) {
    const sorted = [...logs].sort((a, b) => a.at - b.at);
    const max = Math.max(...sorted.map((l) => l.score));
    const worsening = sorted.length >= 2 && sorted[sorted.length - 1]!.score > sorted[0]!.score && sorted[sorted.length - 1]!.score >= 2;
    if (max >= PAIN_PAUSE_SCORE || worsening) {
      pausedRegions.push(region);
      messages.push(
        worsening && max < PAIN_PAUSE_SCORE
          ? `${label(region)} pain is getting worse. Pause exercises that load it and tell a parent or coach.`
          : `${label(region)} pain reached ${max} out of 10. Pause exercises that load it and talk with a parent, coach, or clinician.`,
      );
    }
  }
  const illnessDays = recent.filter((c) => c.illness).length;
  if (illnessDays >= 3) messages.push('You felt ill on several days this week. Rest, and tell a parent if it keeps coming back.');
  return { stopProgression: urgent || pausedRegions.length > 0, urgent, messages, pausedRegions };
}

function label(region: string): string {
  const map: Record<string, string> = { achilles: 'Achilles', heel: 'Heel', shin: 'Shin', knee: 'Knee', lowBack: 'Low back', shoulder: 'Shoulder', wrist: 'Wrist', elbowWrist: 'Elbow', exercise: 'Exercise' };
  return map[region] ?? region;
}

// ---------- Readiness ----------

export type Readiness = 'ready' | 'easier' | 'rest';

export interface ReadinessResult {
  level: Readiness;
  label: string;
  reasons: string[];
}

export function readiness(today: DateKey, checkin: BodyCheckIn | null, sleep: SleepLog | null, pain: PainLog[], safety: SafetyState): ReadinessResult {
  const reasons: string[] = [];
  if (safety.urgent) return { level: 'rest', label: 'Rest and tell a parent', reasons: safety.messages };
  let score = 0;
  if (sleep) {
    const h = sleep.durationMin / 60;
    if (h < 7) {
      score += 2;
      reasons.push(`${h.toFixed(1)} hours of sleep`);
    } else if (h < 8) {
      score += 1;
      reasons.push(`${h.toFixed(1)} hours of sleep, a little under target`);
    }
  }
  if (checkin?.illness) {
    score += 3;
    reasons.push('Feeling ill');
  }
  const todayPain = pain.filter((p) => p.date === today);
  const maxPain = Math.max(0, ...todayPain.map((p) => p.score));
  if (maxPain >= PAIN_PAUSE_SCORE) {
    score += 3;
    reasons.push(`Pain ${maxPain} out of 10`);
  } else if (maxPain >= 2) {
    score += 1;
    reasons.push(`Some pain, ${maxPain} out of 10`);
  }
  const sore = checkin ? Math.max(0, ...Object.values(checkin.soreness)) : 0;
  if (sore >= 3) {
    score += 2;
    reasons.push('Very sore');
  } else if (sore === 2) {
    score += 1;
    reasons.push('Quite sore');
  }
  if (checkin?.energy !== null && checkin?.energy !== undefined && checkin.energy <= 2) {
    score += 1;
    reasons.push('Low energy');
  }
  if (!checkin && !sleep) return { level: 'ready', label: 'No check in yet', reasons: ['Do the morning check in for a readiness read.'] };
  if (score >= 3) return { level: 'rest', label: 'Take it easy today', reasons };
  if (score >= 1) return { level: 'easier', label: 'Train, but keep it comfortable', reasons };
  return { level: 'ready', label: 'No warning signs logged', reasons: reasons.length ? reasons : ['No pain, illness, or short sleep was logged. Your own feel counts too: stop if something hurts.'] };
}
