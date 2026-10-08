// Spoken lines + captions. Captions always show; audio only when sound is on (after a gesture).
// A line is either a voice key ("act_o1") or a group ("otto.pick"); groups draw from a per-session
// shuffle bag, so the crew never repeats itself until a group runs out (and never twice in a row).
import { media, mediaUrl } from '../../lib/media';
import { soundOn } from './prefs';

interface Cue { start: number; end: number; text: string }
const cueCache = new Map<string, Promise<Cue[]>>();

const ts = (s: string): number => {
  const parts = s.trim().split(':').map(Number);
  return parts.reduce((acc, n) => acc * 60 + (Number.isFinite(n) ? n : 0), 0);
};
export function parseVtt(src: string): Cue[] {
  const cues: Cue[] = [];
  for (const block of src.replace(/\r/g, '').split(/\n\n+/)) {
    const lines = block.split('\n');
    const i = lines.findIndex((l) => l.includes('-->'));
    if (i < 0) continue;
    const [a = '', b = ''] = (lines[i] ?? '').split('-->');
    cues.push({ start: ts(a), end: ts(b.trim().split(/\s/)[0] ?? ''), text: lines.slice(i + 1).join('\n').trim() });
  }
  return cues;
}
function cues(rel: string): Promise<Cue[]> {
  let p = cueCache.get(rel);
  if (!p) {
    p = fetch(mediaUrl(rel))
      .then((r) => (r.ok ? r.text() : ''))
      .then(parseVtt)
      .catch(() => []);
    cueCache.set(rel, p);
  }
  return p;
}

// ---------- shuffle bags (sessionStorage, guarded) ----------
const BAG_KEY = 'vxo:bags';
interface Bags { left: Record<string, string[]>; last: Record<string, string>; heard: string[] }
const loadBags = (): Bags => {
  try {
    const b = JSON.parse(sessionStorage.getItem(BAG_KEY) ?? '') as Bags;
    if (b && b.left && b.last && Array.isArray(b.heard)) return b;
  } catch {
    /* empty or blocked */
  }
  return { left: {}, last: {}, heard: [] };
};
let bags: Bags | null = null;
const saveBags = (): void => {
  try {
    sessionStorage.setItem(BAG_KEY, JSON.stringify(bags));
  } catch {
    /* private mode: memory only */
  }
};
const shuffle = <T>(a: T[]): T[] => {
  const r = [...a];
  for (let i = r.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [r[i], r[j]] = [r[j] as T, r[i] as T];
  }
  return r;
};

/** Resolve a key or group to one voice key (groups advance their bag). */
export function draw(keyOrGroup: string): string {
  const group = media.voiceGroups?.[keyOrGroup];
  if (!group?.length) return keyOrGroup;
  bags ??= loadBags();
  let left = (bags.left[keyOrGroup] ?? []).filter((k) => group.includes(k));
  if (!left.length) {
    const last = bags.last[keyOrGroup];
    left = shuffle(group);
    // A fresh bag never starts with the line that ended the last one.
    if (left.length > 1 && left[0] === last) left.push(left.shift() as string);
  }
  const key = left.shift() as string;
  bags.left[keyOrGroup] = left;
  bags.last[keyOrGroup] = key;
  saveBags();
  return key;
}

/** Has this exact line already been heard with sound this session? */
export function heard(key: string): boolean {
  bags ??= loadBags();
  return bags.heard.includes(key);
}
function markHeard(key: string): void {
  bags ??= loadBags();
  if (!bags.heard.includes(key)) bags.heard.push(key);
  saveBags();
}

let audio: HTMLAudioElement | null = null;
let gen = 0;
const listeners = new Set<(text: string, key: string) => void>();
/** Subscribe to every line that starts (for the polite live region). */
export const onLine = (fn: (text: string, key: string) => void): void => void listeners.add(fn);

export interface SayOptions {
  /** Where to write the caption text. */
  caption: (text: string) => void;
  /** Force caption-only (e.g. before the first click). */
  silent?: boolean;
  /** How long a caption-only line stays (ms). */
  holdMs?: number;
  /** Called once the line is chosen: key, text and whether it will be audible. */
  onStart?: (key: string, text: string, audible: boolean) => void;
}

/** Say a line (key or group). Resolves when the audio ends (or after the hold time for caption-only lines). */
export function say(keyOrGroup: string, opts: SayOptions): Promise<void> {
  const key = draw(keyOrGroup);
  const line = media.voice[key];
  if (!line) return Promise.resolve();
  const hold = opts.holdMs ?? Math.max(1600, line.text.length * 60);
  opts.caption(line.text);
  listeners.forEach((l) => l(line.text, key));
  const audible = !opts.silent && soundOn() && !!line.audio;
  opts.onStart?.(key, line.text, audible);
  // Caption-only lines never interrupt a line that is being heard.
  if (!audible || !line.audio) return new Promise((r) => setTimeout(r, hold));
  const my = ++gen;
  markHeard(key);
  audio ??= new Audio();
  const a = audio;
  a.pause();
  a.src = mediaUrl(line.audio);
  a.currentTime = 0;
  const cuePromise = line.vtt ? cues(line.vtt) : Promise.resolve<Cue[]>([]);
  return new Promise<void>((resolve) => {
    let done = false;
    const finish = (): void => {
      if (done) return;
      done = true;
      a.removeEventListener('ended', finish);
      a.removeEventListener('error', finish);
      a.removeEventListener('timeupdate', onTime);
      resolve();
    };
    const onTime = (): void => {
      if (my !== gen) return finish();
      void cuePromise.then((cs) => {
        const c = cs.find((q) => a.currentTime >= q.start && a.currentTime < q.end);
        if (c && my === gen) opts.caption(c.text);
      });
    };
    a.addEventListener('ended', finish);
    a.addEventListener('error', finish);
    a.addEventListener('timeupdate', onTime);
    setTimeout(finish, 8000); // never wait forever on a stalled line
    // play() runs synchronously inside a click handler when the caller is one (autoplay unlock).
    a.play().catch(() => setTimeout(finish, hold));
  });
}

export function hush(): void {
  gen++;
  audio?.pause();
}
