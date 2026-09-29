import { describe, expect, it } from 'vitest';
import {
  buildPreview,
  canonicalJson,
  checksumTables,
  decryptBackup,
  detectFile,
  encryptBackup,
  makeBackup,
  mergeTables,
  migrateTables,
  toCsv,
  validateTables,
  type TableData,
} from '../src/domain/backup';
import { checkRecommendation } from '../src/domain/report';
import { defaultSettings, baselinePlanRecord } from '../src/domain/defaults';

const now = Date.UTC(2026, 8, 29);
const water = (id: string, ml: number, updatedAt = now) => ({ id, createdAt: now, updatedAt, date: '2026-09-29', at: now, ml, drink: 'water' });

function sample(): TableData {
  return {
    settings: [defaultSettings(now) as unknown as Record<string, unknown>],
    plans: [baselinePlanRecord(now) as unknown as Record<string, unknown>],
    waterLogs: [water('w1', 250), water('w2', 500)],
  };
}

describe('backup checksum', () => {
  it('is stable regardless of key order', async () => {
    const a = { waterLogs: [{ b: 1, a: 2 }] } as unknown as TableData;
    const b = { waterLogs: [{ a: 2, b: 1 }] } as unknown as TableData;
    expect(canonicalJson(a)).toBe(canonicalJson(b));
    expect(await checksumTables(a)).toBe(await checksumTables(b));
  });

  it('detects tampering', async () => {
    const file = await makeBackup(sample(), '1.0.0', new Date(now));
    const tampered = JSON.parse(JSON.stringify(file));
    tampered.tables.waterLogs[0].ml = 9999;
    const parsed = detectFile(JSON.stringify(tampered));
    expect(parsed.kind).toBe('plain');
    const preview = await buildPreview(parsed.file as never, {}, 'plain');
    expect(preview.checksumOk).toBe(false);
    const good = await buildPreview(detectFile(JSON.stringify(file)).file as never, {}, 'plain');
    expect(good.checksumOk).toBe(true);
  });
});

describe('encrypted backup', () => {
  it('round trips with the right passphrase and fails with the wrong one', async () => {
    const file = await makeBackup(sample(), '1.0.0', new Date(now));
    const enc = await encryptBackup(file, 'correct horse battery', 100000);
    expect(JSON.stringify(enc)).not.toContain('"ml"');
    const parsed = detectFile(JSON.stringify(enc));
    expect(parsed.kind).toBe('encrypted');
    const back = await decryptBackup(enc, 'correct horse battery');
    expect(back).toEqual(file);
    await expect(decryptBackup(enc, 'wrong passphrase')).rejects.toThrow(/passphrase/);
  });

  it('rejects short passphrases', async () => {
    const file = await makeBackup(sample(), '1.0.0');
    await expect(encryptBackup(file, 'short')).rejects.toThrow();
  });
});

describe('import validation', () => {
  it('rejects files that are not backups', () => {
    expect(() => detectFile('not json')).toThrow(/valid JSON/);
    expect(() => detectFile('{"hello":1}')).toThrow(/not a PeakForm backup/);
  });

  it('keeps valid rows and reports invalid ones', () => {
    const { valid, issues, unknownTables } = validateTables({
      waterLogs: [water('ok', 250), { ...water('bad', 250), ml: -5 }],
      mystery: [{ id: 'x' }],
    } as unknown as TableData);
    expect(valid.waterLogs).toHaveLength(1);
    expect(issues).toHaveLength(1);
    expect(issues[0]!.table).toBe('waterLogs');
    expect(unknownTables).toEqual(['mystery']);
  });

  it('builds a preview with added, identical, and conflicting rows', async () => {
    const file = await makeBackup({ waterLogs: [water('w1', 250), water('w2', 750, now + 10), water('w3', 100)] }, '1.0.0');
    const existing: TableData = { waterLogs: [water('w1', 250), water('w2', 500)] };
    const p = await buildPreview(file, existing, 'plain');
    const t = p.tables.find((x) => x.table === 'waterLogs')!;
    expect(t).toMatchObject({ incoming: 3, existing: 2, added: 1, identical: 1, conflicts: 1 });
    expect(p.dateRange).toEqual({ from: '2026-09-29', to: '2026-09-29' });
  });

  it('merges according to the conflict choice', () => {
    const existing: TableData = { waterLogs: [water('w1', 250, now + 50)] };
    const incoming: TableData = { waterLogs: [water('w1', 999, now), water('w2', 100)] };
    const keep = mergeTables(existing, incoming, 'keep-existing').waterLogs!;
    expect(keep.find((r) => r.id === 'w1')!.ml).toBe(250);
    expect(keep).toHaveLength(2);
    expect(mergeTables(existing, incoming, 'use-incoming').waterLogs!.find((r) => r.id === 'w1')!.ml).toBe(999);
    expect(mergeTables(existing, incoming, 'newer-wins').waterLogs!.find((r) => r.id === 'w1')!.ml).toBe(250);
  });
});

describe('schema migration', () => {
  it('migrates a version 0 backup', async () => {
    const v0 = {
      setLogs: [{ id: 's1', weight: 50 }],
      checkins: [{ id: 'c1', createdAt: now, updatedAt: now, date: '2026-09-20', waistCm: 91.5, standardConditions: true }],
    } as unknown as TableData;
    const { tables, applied } = migrateTables(v0, 0);
    expect(applied).toEqual([0]);
    expect(tables.setLogs![0]).toMatchObject({ weightKg: 50 });
    expect(tables.setLogs![0]).not.toHaveProperty('weight');
    expect(tables.checkins![0]).not.toHaveProperty('waistCm');
    expect(tables.waist![0]).toMatchObject({ cm: 91.5, date: '2026-09-20' });
  });

  it('refuses unknown future migrations', () => {
    expect(() => migrateTables({}, -1)).toThrow(/No migration/);
  });
});

describe('CSV export', () => {
  it('escapes quotes, commas, newlines, and formula injection', () => {
    const csv = toCsv([{ a: 'x,y', b: 'say "hi"', c: '=HYPERLINK("x")', d: 'line\nbreak' }], ['a', 'b', 'c', 'd']);
    expect(csv).toContain('"x,y"');
    expect(csv).toContain('"say ""hi"""');
    expect(csv).toContain(`"'=HYPERLINK(""x"")"`);
    expect(csv).toContain('"line\nbreak"');
  });
});

describe('recommendation import', () => {
  it('validates and blocks changes below the safety floors', () => {
    const rec = {
      format: 'peakform-recommendation',
      version: 1,
      source: 'Coach',
      createdAt: '2026-10-04',
      changes: [
        { type: 'nutrition-target', weekday: 1, kcal: 1800, reason: 'cut' },
        { type: 'nutrition-target', weekday: 2, carbs: 100, reason: 'low carb' },
        { type: 'plan-item', planItemId: 'mon-5-barbell-squat', repMin: 6, repMax: 10, reason: 'same' },
      ],
    };
    const r = checkRecommendation(JSON.stringify(rec));
    expect(r.ok).toBe(true);
    expect(r.blocked).toHaveLength(2);
  });

  it('rejects malformed recommendations and RIR of zero', () => {
    expect(checkRecommendation('{').ok).toBe(false);
    const r = checkRecommendation(JSON.stringify({ format: 'peakform-recommendation', version: 1, source: 'x', createdAt: 'x', changes: [{ type: 'plan-item', planItemId: 'a', rir: 0, reason: 'failure' }] }));
    expect(r.ok).toBe(false);
  });
});
