import { z } from 'zod';
import { SCHEMA_VERSION, TABLE_NAMES, TABLE_SCHEMAS, type TableName } from '../db/records';

// Backup, restore, and migration. A backup is canonical JSON with a SHA-256 checksum
// over the table data. Optional encryption uses AES-GCM with a PBKDF2 derived key.
// A lost passphrase cannot be recovered.

export const BACKUP_FORMAT = 'peakform-backup';
export const ENCRYPTED_FORMAT = 'peakform-backup-encrypted';
export const PBKDF2_ITERATIONS = 310000;

export type TableData = Partial<Record<TableName, Array<Record<string, unknown>>>>;

export interface BackupFile {
  format: typeof BACKUP_FORMAT;
  schemaVersion: number;
  appVersion: string;
  exportedAt: string;
  checksum: string;
  tables: TableData;
}

export interface EncryptedBackupFile {
  format: typeof ENCRYPTED_FORMAT;
  schemaVersion: number;
  appVersion: string;
  exportedAt: string;
  kdf: { name: 'PBKDF2'; hash: 'SHA-256'; iterations: number; salt: string };
  cipher: { name: 'AES-GCM'; iv: string };
  data: string;
}

/** JSON with sorted object keys so the same data always produces the same checksum. */
export function canonicalJson(value: unknown): string {
  if (value === null || typeof value !== 'object') return JSON.stringify(value) ?? 'null';
  if (Array.isArray(value)) return `[${value.map((v) => canonicalJson(v === undefined ? null : v)).join(',')}]`;
  const obj = value as Record<string, unknown>;
  const keys = Object.keys(obj)
    .filter((k) => obj[k] !== undefined)
    .sort();
  return `{${keys.map((k) => `${JSON.stringify(k)}:${canonicalJson(obj[k])}`).join(',')}}`;
}

export async function sha256Hex(text: string): Promise<string> {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

export async function checksumTables(tables: TableData): Promise<string> {
  return sha256Hex(canonicalJson(tables));
}

export async function makeBackup(tables: TableData, appVersion: string, now: Date = new Date()): Promise<BackupFile> {
  return {
    format: BACKUP_FORMAT,
    schemaVersion: SCHEMA_VERSION,
    appVersion,
    exportedAt: now.toISOString(),
    checksum: await checksumTables(tables),
    tables,
  };
}

// ---------- Encryption ----------

const b64 = (bytes: Uint8Array): string => {
  let s = '';
  bytes.forEach((b) => (s += String.fromCharCode(b)));
  return btoa(s);
};
const unb64 = (s: string): Uint8Array<ArrayBuffer> => {
  const bin = atob(s);
  const out = new Uint8Array(new ArrayBuffer(bin.length));
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
};

async function deriveKey(passphrase: string, salt: Uint8Array<ArrayBuffer>, iterations: number): Promise<CryptoKey> {
  const material = await crypto.subtle.importKey('raw', new TextEncoder().encode(passphrase), 'PBKDF2', false, ['deriveKey']);
  return crypto.subtle.deriveKey({ name: 'PBKDF2', hash: 'SHA-256', salt, iterations }, material, { name: 'AES-GCM', length: 256 }, false, ['encrypt', 'decrypt']);
}

export async function encryptBackup(backup: BackupFile, passphrase: string, iterations = PBKDF2_ITERATIONS): Promise<EncryptedBackupFile> {
  if (passphrase.length < 8) throw new Error('Use a passphrase of at least 8 characters.');
  const salt = crypto.getRandomValues(new Uint8Array(new ArrayBuffer(16)));
  const iv = crypto.getRandomValues(new Uint8Array(new ArrayBuffer(12)));
  const key = await deriveKey(passphrase, salt, iterations);
  const plain = new TextEncoder().encode(JSON.stringify(backup));
  const cipher = new Uint8Array(await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, plain));
  return {
    format: ENCRYPTED_FORMAT,
    schemaVersion: backup.schemaVersion,
    appVersion: backup.appVersion,
    exportedAt: backup.exportedAt,
    kdf: { name: 'PBKDF2', hash: 'SHA-256', iterations, salt: b64(salt) },
    cipher: { name: 'AES-GCM', iv: b64(iv) },
    data: b64(cipher),
  };
}

export async function decryptBackup(file: EncryptedBackupFile, passphrase: string): Promise<unknown> {
  const key = await deriveKey(passphrase, unb64(file.kdf.salt), file.kdf.iterations);
  try {
    const plain = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: unb64(file.cipher.iv) }, key, unb64(file.data));
    return JSON.parse(new TextDecoder().decode(plain));
  } catch {
    throw new Error('The passphrase is wrong or the file is damaged.');
  }
}

// ---------- Parsing, migration, validation ----------

const EncryptedSchema = z.object({
  format: z.literal(ENCRYPTED_FORMAT),
  schemaVersion: z.number().int(),
  appVersion: z.string(),
  exportedAt: z.string(),
  kdf: z.object({ name: z.literal('PBKDF2'), hash: z.literal('SHA-256'), iterations: z.number().int().min(100000).max(5000000), salt: z.string() }),
  cipher: z.object({ name: z.literal('AES-GCM'), iv: z.string() }),
  data: z.string(),
});

const EnvelopeSchema = z.object({
  format: z.literal(BACKUP_FORMAT),
  schemaVersion: z.number().int().min(0),
  appVersion: z.string(),
  exportedAt: z.string(),
  checksum: z.string().regex(/^[0-9a-f]{64}$/),
  tables: z.record(z.string(), z.array(z.record(z.string(), z.unknown()))),
});

export type ParsedFile = { kind: 'encrypted'; file: EncryptedBackupFile } | { kind: 'plain'; file: BackupFile };

export function detectFile(text: string): ParsedFile {
  let json: unknown;
  try {
    json = JSON.parse(text);
  } catch {
    throw new Error('This file is not valid JSON.');
  }
  const enc = EncryptedSchema.safeParse(json);
  if (enc.success) return { kind: 'encrypted', file: enc.data as EncryptedBackupFile };
  const env = EnvelopeSchema.safeParse(json);
  if (env.success) return { kind: 'plain', file: env.data as BackupFile };
  throw new Error('This is not a PeakForm backup file.');
}

/**
 * Migrations from older backup schema versions. Version 0 was the pre release format
 * where body check ins stored waist inline and sets used "weight" instead of "weightKg".
 */
export const MIGRATIONS: Record<number, (t: TableData) => TableData> = {
  0: (t) => {
    const out: TableData = { ...t };
    out.setLogs = (t.setLogs ?? []).map((s) => {
      const { weight, ...rest } = s as Record<string, unknown> & { weight?: number };
      return { ...rest, weightKg: (rest.weightKg as number | undefined) ?? weight ?? null };
    });
    const waist = [...(t.waist ?? [])];
    out.checkins = (t.checkins ?? []).map((c) => {
      const { waistCm, ...rest } = c as Record<string, unknown> & { waistCm?: number };
      if (typeof waistCm === 'number') {
        waist.push({ id: `waist-${rest.id as string}`, createdAt: rest.createdAt, updatedAt: rest.updatedAt, date: rest.date, cm: waistCm, standardConditions: Boolean(rest.standardConditions) });
      }
      return rest;
    });
    out.waist = waist;
    out.sessions = (t.sessions ?? []).map((s) => ({ ...s, planWeekday: (s as { planWeekday?: number }).planWeekday ?? (s as { weekday?: number }).weekday }));
    return out;
  },
};

export function migrateTables(tables: TableData, fromVersion: number): { tables: TableData; applied: number[] } {
  let t = tables;
  const applied: number[] = [];
  for (let v = fromVersion; v < SCHEMA_VERSION; v++) {
    const m = MIGRATIONS[v];
    if (!m) throw new Error(`No migration from schema version ${v}.`);
    t = m(t);
    applied.push(v);
  }
  return { tables: t, applied };
}

export interface ValidationIssue {
  table: string;
  index: number;
  message: string;
}

export function validateTables(tables: TableData): { valid: TableData; issues: ValidationIssue[]; unknownTables: string[] } {
  const valid: TableData = {};
  const issues: ValidationIssue[] = [];
  const unknownTables = Object.keys(tables).filter((k) => !(TABLE_NAMES as string[]).includes(k));
  for (const name of TABLE_NAMES) {
    const rows = tables[name];
    if (!rows) continue;
    const schema = TABLE_SCHEMAS[name] as z.ZodType;
    const ok: Array<Record<string, unknown>> = [];
    rows.forEach((row, index) => {
      const r = schema.safeParse(row);
      if (r.success) ok.push(r.data as Record<string, unknown>);
      else issues.push({ table: name, index, message: r.error.issues.map((i) => `${i.path.join('.')}: ${i.message}`).join('; ').slice(0, 300) });
    });
    valid[name] = ok;
  }
  return { valid, issues, unknownTables };
}

// ---------- Preview and conflicts ----------

export interface TablePreview {
  table: TableName;
  incoming: number;
  existing: number;
  added: number;
  identical: number;
  conflicts: number;
}

export interface ImportPreview {
  fileKind: 'plain' | 'encrypted';
  schemaVersion: number;
  migratedFrom: number[];
  exportedAt: string;
  checksumOk: boolean;
  tables: TablePreview[];
  issues: ValidationIssue[];
  unknownTables: string[];
  dateRange: { from: string; to: string } | null;
  data: TableData;
}

export async function buildPreview(parsed: BackupFile, existing: TableData, fileKind: 'plain' | 'encrypted'): Promise<ImportPreview> {
  const checksumOk = (await checksumTables(parsed.tables)) === parsed.checksum;
  const { tables: migrated, applied } = migrateTables(parsed.tables, parsed.schemaVersion);
  const { valid, issues, unknownTables } = validateTables(migrated);
  const previews: TablePreview[] = [];
  const dates: string[] = [];
  for (const name of TABLE_NAMES) {
    const rows = valid[name];
    if (!rows || rows.length === 0) continue;
    const ex = new Map((existing[name] ?? []).map((r) => [String(r.id), r]));
    let added = 0;
    let identical = 0;
    let conflicts = 0;
    for (const r of rows) {
      if (typeof r.date === 'string') dates.push(r.date);
      const cur = ex.get(String(r.id));
      if (!cur) added++;
      else if (canonicalJson(cur) === canonicalJson(r)) identical++;
      else conflicts++;
    }
    previews.push({ table: name, incoming: rows.length, existing: ex.size, added, identical, conflicts });
  }
  dates.sort();
  return {
    fileKind,
    schemaVersion: parsed.schemaVersion,
    migratedFrom: applied,
    exportedAt: parsed.exportedAt,
    checksumOk,
    tables: previews,
    issues,
    unknownTables,
    dateRange: dates.length ? { from: dates[0]!, to: dates[dates.length - 1]! } : null,
    data: valid,
  };
}

export type ConflictChoice = 'keep-existing' | 'use-incoming' | 'newer-wins';

/** Merge incoming rows into existing ones according to the user's conflict choice. */
export function mergeTables(existing: TableData, incoming: TableData, choice: ConflictChoice): TableData {
  const out: TableData = {};
  for (const name of TABLE_NAMES) {
    const ex = existing[name] ?? [];
    const inc = incoming[name];
    if (!inc) {
      out[name] = ex;
      continue;
    }
    const map = new Map(ex.map((r) => [String(r.id), r]));
    for (const r of inc) {
      const cur = map.get(String(r.id));
      if (!cur || choice === 'use-incoming') map.set(String(r.id), r);
      else if (choice === 'newer-wins' && Number(r.updatedAt ?? 0) > Number(cur.updatedAt ?? 0)) map.set(String(r.id), r);
    }
    out[name] = [...map.values()];
  }
  return out;
}

// ---------- CSV ----------

export function toCsv(rows: Array<Record<string, unknown>>, columns: string[]): string {
  const esc = (v: unknown) => {
    if (v === null || v === undefined) return '';
    const s = typeof v === 'object' ? JSON.stringify(v) : String(v);
    // Neutralise spreadsheet formula injection.
    const safe = /^[=+\-@\t\r]/.test(s) ? `'${s}` : s;
    return /[",\n\r]/.test(safe) ? `"${safe.replace(/"/g, '""')}"` : safe;
  };
  return [columns.join(','), ...rows.map((r) => columns.map((c) => esc(r[c])).join(','))].join('\r\n') + '\r\n';
}
