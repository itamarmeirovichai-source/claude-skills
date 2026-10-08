// Spoken lines + captions. Captions always show; audio only when sound is on (after a gesture).
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

let audio: HTMLAudioElement | null = null;
let gen = 0;

export interface SayOptions {
  /** Where to write the caption text. */
  caption: (text: string) => void;
  /** Force caption-only (e.g. before the first click). */
  silent?: boolean;
  /** How long a caption-only line stays (ms). */
  holdMs?: number;
}

/** Say a line. Resolves when the audio ends (or after the hold time for caption-only lines). */
export function say(key: string, opts: SayOptions): Promise<void> {
  const line = media.voice[key];
  const my = ++gen;
  if (!line) return Promise.resolve();
  const hold = opts.holdMs ?? Math.max(1600, line.text.length * 60);
  opts.caption(line.text);
  if (opts.silent || !soundOn() || !line.audio) {
    return new Promise((r) => setTimeout(r, hold));
  }
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
        if (c) opts.caption(c.text);
      });
    };
    a.addEventListener('ended', finish);
    a.addEventListener('error', finish);
    a.addEventListener('timeupdate', onTime);
    setTimeout(finish, 8000); // never wait forever on a stalled line
    a.play().catch(() => setTimeout(finish, hold));
  });
}

export function hush(): void {
  gen++;
  audio?.pause();
}
