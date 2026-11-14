// One schema, shared by the browser form (inline errors) and the Pages Functions (server checks).
import { z } from 'zod';

export const MAX_FILES = 3;
export const MAX_CLIENT_FILE_BYTES = 20 * 1024 * 1024; // what the picker accepts before resizing
export const MAX_UPLOAD_BYTES = 4 * 1024 * 1024; // what the server stores after client-side resize
export const UPLOAD_TYPES = ['image/jpeg', 'image/png', 'image/webp'] as const;
export const MIN_FILL_MS = 3000;

export const MESSAGES = {
  email: "That email doesn't look right. Check for a typo?",
  website: 'Add your site, e.g. yourbrand.com',
  product: 'Tell us which product.',
  fileSize: 'That file is too big (20 MB max). Try a smaller copy?',
  upload: "Upload failed. Try again, or skip it and we'll use your site.",
  consent: 'Tick the box so we can use your photo for your frames.',
} as const;

export function normaliseUrl(raw: string): string {
  const v = raw.trim();
  if (!v) return v;
  return /^https?:\/\//i.test(v) ? v : `https://${v}`;
}

const website = z
  .string()
  .trim()
  .min(1, MESSAGES.website)
  .max(300, MESSAGES.website)
  .transform(normaliseUrl)
  .refine((v) => {
    try {
      const u = new URL(v);
      return (u.protocol === 'https:' || u.protocol === 'http:') && u.hostname.includes('.');
    } catch {
      return false;
    }
  }, MESSAGES.website);

export const fileMetaSchema = z.object({
  type: z.enum(UPLOAD_TYPES),
  size: z.number().int().positive().max(MAX_UPLOAD_BYTES, MESSAGES.fileSize),
});

export const leadSchema = z
  .object({
    email: z.string().trim().max(254, MESSAGES.email).pipe(z.email(MESSAGES.email)),
    website,
    product: z.string().trim().min(1, MESSAGES.product).max(160, MESSAGES.product),
    look: z.enum(['studio', 'world']).default('studio'),
    firstName: z.string().trim().max(80).optional().default(''),
    intent: z.enum(['bestseller', 'launch', 'general']).default('general'),
    consent: z.boolean().default(false),
    files: z.array(fileMetaSchema).max(MAX_FILES).default([]),
    utm: z.record(z.string().max(40), z.string().max(120)).optional().default({}),
  })
  .refine((d) => d.files.length === 0 || d.consent, { message: MESSAGES.consent, path: ['consent'] });

export type LeadInput = z.input<typeof leadSchema>;
export type Lead = z.output<typeof leadSchema>;

export const qualifySchema = z.object({
  runs: z.array(z.enum(['meta', 'tiktok', 'youtube', 'website', 'not-sure'])).max(5).default([]),
  win: z.enum(['launch', 'tired-winner', 'new-look', 'exploring', '']).default(''),
  hardest: z.string().trim().max(400).default(''),
  spend: z.enum(['<5k', '5-20k', '20-50k', '50k+', 'n/a', '']).default(''),
  next: z.enum(['email', 'call', '']).default(''),
});
export type Qualify = z.output<typeof qualifySchema>;

/** Flatten zod issues to { field: firstMessage }. */
export function fieldErrors(error: z.ZodError): Record<string, string> {
  const out: Record<string, string> = {};
  for (const issue of error.issues) {
    const key = String(issue.path[0] ?? 'form');
    if (!(key in out)) out[key] = issue.message;
  }
  return out;
}
