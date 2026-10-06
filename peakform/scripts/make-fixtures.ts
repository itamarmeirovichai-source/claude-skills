// Example backups with synthetic demo history. No real person's data.
// Passphrase for the encrypted example: example passphrase 2026
import { writeFileSync } from 'node:fs';
import { BASELINE_PLAN } from '../src/content/plan';
import { LIBRARY } from '../src/content/library';
import { generateDemo } from '../src/domain/demo';
import { baselinePlanRecord, defaultProfile, defaultSettings } from '../src/domain/defaults';
import { encryptBackup, makeBackup } from '../src/domain/backup';

const now = Date.parse('2026-09-28T20:00:00Z');
const byId = Object.fromEntries(LIBRARY.map((e) => [e.id, e]));
const demo = generateDemo(BASELINE_PLAN.days, '2026-09-27', 2, { kind: (id) => byId[id]?.kind ?? 'strength', logSides: (id) => byId[id]?.logSides ?? false });
const settings = { ...defaultSettings(now), onboarded: true, demoData: true };
const profile = { ...defaultProfile(now), name: 'Demo athlete', heightCm: 175 };
const tables = {
  settings: [settings],
  profile: [profile],
  plans: [baselinePlanRecord(now)],
  ...demo,
} as unknown as Parameters<typeof makeBackup>[0];
const plain = await makeBackup(tables, '1.0.0', new Date(now));
writeFileSync('fixtures/example-backup-plain.json', JSON.stringify(plain));
const enc = await encryptBackup(plain, 'example passphrase 2026');
writeFileSync('fixtures/example-backup-encrypted.json', JSON.stringify(enc, null, 2));
writeFileSync(
  'fixtures/example-recommendation.json',
  JSON.stringify(
    {
      format: 'peakform-recommendation',
      version: 1,
      source: 'Example coach',
      createdAt: '2026-10-04',
      changes: [
        { type: 'plan-item', planItemId: 'wed-7-machine-lateral-raise', sets: 3, reason: 'Side delts are recovering well. Add one set for four weeks.' },
        { type: 'plan-item', planItemId: 'mon-2-dumbbell-romanian-deadlift', repMin: 8, repMax: 12, reason: 'Keep the hinge a little lighter for now.' },
      ],
    },
    null,
    2,
  ),
);
console.log('Fixtures written.', Object.entries(tables).map(([k, v]) => `${k}:${(v as unknown[]).length}`).join(' '));
