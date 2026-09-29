// Builds the private setup file for one user from a private input file.
// Both the input (private/profile-input.json) and the output live in private/, which is
// gitignored. Personal values must never be committed to this public repository.
// Copy scripts/profile-input.example.json to private/profile-input.json and fill it in.
// Usage: npx tsx scripts/make-private-seed.ts [input] [output]
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { defaultProfile, defaultSettings, baselinePlanRecord } from '../src/domain/defaults';
import { makeBackup } from '../src/domain/backup';

interface ProfileInput {
  name?: string;
  heightCm?: number | null;
  birthYear?: number | null;
  startWeightKg?: number | null;
  startBodyFatPct?: number | null;
  goals?: string[];
  medicalNotes?: string;
  allergies?: string;
  planStartDate?: string | null;
  eventDate?: string | null;
  eventLabel?: string;
  sabbath?: boolean;
}

const input = resolve(process.argv[2] ?? 'private/profile-input.json');
const out = resolve(process.argv[3] ?? 'private/peakform-private-setup.json');
if (!existsSync(input)) {
  console.error(`Missing ${input}. Copy scripts/profile-input.example.json there and fill it in.`);
  process.exit(1);
}
const p = JSON.parse(readFileSync(input, 'utf8')) as ProfileInput;
const now = Date.now();
const settings = defaultSettings(now);
settings.onboarded = true;
settings.guardianReviewAck = false;
settings.planStartDate = p.planStartDate ?? null;
settings.eventDate = p.eventDate ?? null;
settings.eventLabel = p.eventLabel ?? '';
settings.sabbath = { ...settings.sabbath, enabled: p.sabbath ?? true };

const profile = {
  ...defaultProfile(now),
  name: p.name ?? '',
  heightCm: p.heightCm ?? null,
  birthYear: p.birthYear ?? null,
  startWeightKg: p.startWeightKg ?? null,
  startBodyFatPct: p.startBodyFatPct ?? null,
  goals: p.goals ?? [],
  medicalNotes: p.medicalNotes ?? '',
  allergies: p.allergies ?? '',
};

const backup = await makeBackup(
  { settings: [settings as unknown as Record<string, unknown>], profile: [profile as unknown as Record<string, unknown>], plans: [baselinePlanRecord(now) as unknown as Record<string, unknown>] },
  'private-seed',
);
mkdirSync(dirname(out), { recursive: true });
writeFileSync(out, JSON.stringify(backup, null, 2));
console.log(`Private setup file written to ${out}. Keep it private.`);
