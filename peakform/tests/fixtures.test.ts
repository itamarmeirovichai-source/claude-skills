import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { buildPreview, decryptBackup, detectFile, type BackupFile, type EncryptedBackupFile } from '../src/domain/backup';
import { checkRecommendation } from '../src/domain/report';

describe('example fixtures', () => {
  it('the plain example backup validates with a matching checksum', async () => {
    const parsed = detectFile(readFileSync('fixtures/example-backup-plain.json', 'utf8'));
    expect(parsed.kind).toBe('plain');
    const p = await buildPreview(parsed.file as BackupFile, {}, 'plain');
    expect(p.checksumOk).toBe(true);
    expect(p.issues).toEqual([]);
    expect(p.tables.find((t) => t.table === 'setLogs')!.incoming).toBeGreaterThan(100);
  });

  it('the encrypted example opens only with its passphrase', async () => {
    const parsed = detectFile(readFileSync('fixtures/example-backup-encrypted.json', 'utf8'));
    expect(parsed.kind).toBe('encrypted');
    await expect(decryptBackup(parsed.file as EncryptedBackupFile, 'wrong')).rejects.toThrow();
    const inner = await decryptBackup(parsed.file as EncryptedBackupFile, 'example passphrase 2026');
    expect((inner as BackupFile).format).toBe('peakform-backup');
  });

  it('the example recommendation is valid and not blocked', () => {
    const r = checkRecommendation(readFileSync('fixtures/example-recommendation.json', 'utf8'));
    expect(r.ok).toBe(true);
    expect(r.blocked).toEqual([]);
  });

  it('fixtures only carry the synthetic demo profile', () => {
    const b = JSON.parse(readFileSync('fixtures/example-backup-plain.json', 'utf8')) as BackupFile;
    const profile = b.tables.profile![0]!;
    expect(profile.name).toBe('Demo athlete');
    expect(profile.startWeightKg).toBeNull();
    expect(profile.startBodyFatPct).toBeNull();
    expect(profile.birthYear).toBeNull();
    expect((b.tables.settings![0] as { eventLabel: string }).eventLabel).toBe('');
  });
});
