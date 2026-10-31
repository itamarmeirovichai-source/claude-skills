// The line director. Eight fixed lines, each ONE clip with its audio baked in, so lips, sound and captions
// run on the same clock (the clip's own currentTime). Rules:
//   · a line starts only when its character's slot is at least 60 % in view, and stops if the slot leaves;
//   · one line at a time, each line at most once per visit (sessionStorage);
//   · idle loop before and after; audio only after "Sound on", otherwise the clip plays muted with captions;
//   · a line whose clip isn't delivered yet: the character keeps idling and the line shows as a plain caption.
import '../alpha-video';
import type { AlphaVideo } from '../alpha-video';
import { media, mediaUrl, resolveClip, lineReady, type LineId } from '../../lib/media';
import { alphaSrc, pickAlphaCodec, pickLineCodec, type AlphaCodec } from '../core/codec';
import { prefs, session, soundOn, reducedMotion, motionPaused, saveData } from '../core/prefs';
import { track } from '../core/analytics';

const VIEW_START = 0.6;
const VIEW_LOST = 0.25;
const GAP_MS = 700;
const KEY = 'vxo:lines-played';

interface Word {
  text: string;
  start: number;
  end: number;
}
interface Request {
  id: LineId;
  until: number;
}

class Slot {
  readonly id: string;
  readonly who: 'otto' | 'vee';
  readonly av: AlphaVideo | null;
  readonly say: HTMLElement | null;
  /** The element that carries data-talking / data-said (the hero section for Otto in the hero). */
  readonly host: HTMLElement;
  ratio = 0;
  queue: Request[] = [];
  idling = false;

  constructor(readonly el: HTMLElement) {
    this.id = el.dataset['slot'] ?? '';
    this.who = el.dataset['who'] === 'vee' ? 'vee' : 'otto';
    this.av = el.querySelector<AlphaVideo>('alpha-video');
    this.host = this.id === 'hero' ? (el.closest<HTMLElement>('#hero') ?? el) : el;
    this.say = this.host.querySelector<HTMLElement>('[data-say]');
  }
}

let codec: AlphaCodec | null = null;
let lineCodec: AlphaCodec | null = null;
const slots = new Map<string, Slot>();
let current: { slot: Slot; id: LineId; audible: boolean; cut: () => void } | null = null;
let pumpTimer = 0;

const played = new Set<string>(
  (() => {
    try {
      return JSON.parse(sessionStorage.getItem(KEY) ?? '[]') as string[];
    } catch {
      return [];
    }
  })(),
);
const markPlayed = (id: string): void => {
  played.add(id);
  try {
    sessionStorage.setItem(KEY, JSON.stringify([...played]));
  } catch {
    /* private mode: this page view only */
  }
};

const wordsCache = new Map<string, Promise<Word[]>>();
function words(rel: string | null | undefined): Promise<Word[]> {
  if (!rel) return Promise.resolve([]);
  let p = wordsCache.get(rel);
  if (!p) {
    p = fetch(mediaUrl(rel))
      .then((r) => (r.ok ? (r.json() as Promise<{ words?: Word[] }>) : { words: [] }))
      .then((j) => (Array.isArray(j.words) ? j.words : []))
      .catch(() => []);
    wordsCache.set(rel, p);
  }
  return p;
}

/** Characters animate only with video available, data allowed and motion welcome. */
const animated = (): boolean => !!codec && !saveData() && !reducedMotion() && !motionPaused();

function idle(s: Slot): void {
  if (!s.av?.ok || !codec || current?.slot === s || !animated() || s.ratio === 0) return;
  const clip = resolveClip(s.who === 'vee' ? media.vee : media.otto, s.who === 'vee' ? 'vee_idle' : 'char_idle');
  if (!clip) return;
  const src = alphaSrc(clip, codec);
  const fv = s.av.frontVideo;
  if (s.idling && fv.dataset['src'] === src && !fv.paused) return;
  s.idling = true;
  void s.av.play(src, { loop: true, duration: clip.duration, fadeMs: 260, startTimeoutMs: 5000 }).then((r) => {
    if (r === 'error' || r === 'timeout') s.idling = false;
  });
}
function rest(s: Slot): void {
  s.idling = false;
  s.av?.pause();
}

function renderWords(el: HTMLElement, text: string, ws: Word[]): HTMLElement[] {
  el.textContent = '';
  if (!ws.length) {
    el.textContent = text;
    return [];
  }
  return ws.map((w, i) => {
    const span = document.createElement('span');
    span.className = 'w';
    span.textContent = w.text;
    el.append(span);
    if (i < ws.length - 1) el.append(' ');
    return span;
  });
}

const announce = (s: Slot, text: string): void => {
  const live = document.querySelector('[data-crew-live]');
  if (live) live.textContent = `${s.who === 'vee' ? 'Vee' : 'Otto'}: ${text}`;
};

async function play(s: Slot, id: LineId): Promise<void> {
  const line = media.lines[id];
  markPlayed(id);
  const audible = soundOn() && !!line.audio;
  let stopped = false;
  current = { slot: s, id, audible, cut: () => void (stopped = true) };
  s.host.dataset['talking'] = id;
  announce(s, line.text);
  const say = s.say;
  const ready = lineReady(line) && !!lineCodec && !!s.av?.ok && !saveData() && (animated() || soundOn());
  track('line_play', { id, audible: audible ? 1 : 0, clip: ready ? 1 : 0 });

  if (ready && s.av && lineCodec && lineReady(line)) {
    const av = s.av;
    const ws = await words(line.words);
    if (stopped) return finish(s);
    const spans = say ? renderWords(say, line.text, ws) : [];
    let raf = 0;
    const sync = (): void => {
      const t = av.time;
      spans.forEach((sp, i) => sp.classList.toggle('on', (ws[i]?.start ?? Infinity) <= t + 0.04));
      raf = requestAnimationFrame(sync);
    };
    const src = alphaSrc(line, lineCodec);
    const opts = { duration: line.duration ?? 7, fadeMs: 220, startTimeoutMs: 5000, onStart: () => (raf = requestAnimationFrame(sync)) };
    current.cut = () => {
      stopped = true;
      av.stop();
    };
    s.idling = false;
    let r = await av.play(src, { ...opts, audible });
    // Sound refused (no gesture this visit on this element): the same clip, muted. Lips still match the words.
    if (r === 'error' && audible && !stopped) r = await av.play(src, { ...opts, audible: false });
    cancelAnimationFrame(raf);
    spans.forEach((sp) => sp.classList.add('on'));
    if (say && !spans.length) say.textContent = line.text;
    return finish(s);
  }

  // No clip (pending, no codec, Save-Data): idle on, the line as a plain caption for a reading-length beat.
  if (say) say.textContent = line.text;
  idle(s);
  await new Promise<void>((r) => {
    const t = window.setTimeout(r, Math.max(2600, line.text.split(' ').length * 330));
    current && (current.cut = () => (window.clearTimeout(t), (stopped = true), r()));
  });
  return finish(s);
}

function finish(s: Slot): void {
  delete s.host.dataset['talking'];
  s.host.dataset['said'] = '';
  current = null;
  idle(s);
  window.clearTimeout(pumpTimer);
  pumpTimer = window.setTimeout(pump, GAP_MS);
}

function pump(): void {
  if (current || document.hidden) return;
  const now = Date.now();
  let best: Slot | null = null;
  for (const s of slots.values()) {
    s.queue = s.queue.filter((q) => q.until > now && !played.has(q.id));
    if (s.queue.length && s.ratio >= VIEW_START && (!best || s.ratio > best.ratio)) best = s;
  }
  const next = best?.queue.shift();
  if (best && next) void play(best, next.id);
}

/** Ask a slot to say a line (once per visit). `ttlMs`: give up if the slot isn't in view by then. */
export function request(slotId: string, id: LineId, ttlMs = Infinity): void {
  const s = slots.get(slotId);
  if (!s || played.has(id) || s.queue.some((q) => q.id === id)) return;
  s.queue.push({ id, until: Date.now() + ttlMs });
  pump();
  if (Number.isFinite(ttlMs)) window.setTimeout(pump, ttlMs + 20);
}

/** Stop the line that is playing (a film opened, the tab was hidden). It still counts as heard. */
export function hush(): void {
  current?.cut();
}

/** The "Sound on / off" choice. Call inside the tap: that is what lets audio play on iOS. */
export function setSound(on: boolean): void {
  session.gesture = true;
  prefs.set({ sound: on ? 'on' : 'off' });
  syncSoundUi();
  if (on) {
    slots.forEach((s) => s.av?.unlock());
    if (current && media.lines[current.id].audio) current.slot.av?.setMuted(false);
    request('hero', 'o1');
    track('crew_sound_on');
  } else {
    current?.slot.av?.setMuted(true);
    track('crew_sound_off');
  }
  document.dispatchEvent(new CustomEvent('vxo:sound'));
}

function syncSoundUi(): void {
  const on = soundOn();
  document.documentElement.classList.toggle('sound-on', on);
  document.querySelectorAll<HTMLButtonElement>('[data-sound-toggle]').forEach((b) => {
    if (b.hasAttribute('data-sound-hint')) return;
    b.setAttribute('aria-pressed', String(on));
  });
}

export async function mountCharacters(): Promise<void> {
  const els = [...document.querySelectorAll<HTMLElement>('[data-slot]')];
  els.forEach((el) => slots.set(el.dataset['slot'] ?? '', new Slot(el)));
  document.querySelectorAll<HTMLButtonElement>('[data-sound-toggle]').forEach((b) =>
    b.addEventListener('click', () => setSound(b.hasAttribute('data-sound-hint') ? true : !soundOn())),
  );
  // A remembered "on" still needs this visit's first tap before audio may play.
  window.addEventListener('pointerdown', () => queueMicrotask(syncSoundUi), { once: true, capture: true });
  syncSoundUi();

  [codec, lineCodec] = await Promise.all([pickAlphaCodec(), pickLineCodec()]);
  const still = !animated();
  slots.forEach((s) => {
    if (still || !s.av?.ok) s.el.classList.add('poster-mode');
    (s.el.dataset['lines'] ?? '').split(/\s+/).filter(Boolean).forEach((id) => request(s.id, id as LineId));
  });

  const io = new IntersectionObserver(
    (es) => {
      for (const e of es) {
        const s = slots.get((e.target as HTMLElement).dataset['slot'] ?? '');
        if (!s) continue;
        s.ratio = e.isIntersecting ? e.intersectionRatio : 0;
        if (s.ratio === 0) {
          if (current?.slot !== s) rest(s);
        } else idle(s);
        if (current?.slot === s && s.ratio < VIEW_LOST) current.cut();
      }
      pump();
    },
    { threshold: [0, 0.1, VIEW_LOST, 0.4, VIEW_START, 0.8, 1] },
  );
  slots.forEach((s) => io.observe(s.el));

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      hush();
      slots.forEach(rest);
    } else {
      slots.forEach((s) => s.ratio > 0 && idle(s));
      pump();
    }
  });
  prefs.on(() => {
    if (motionPaused()) slots.forEach((s) => current?.slot !== s && rest(s));
    else slots.forEach((s) => s.ratio > 0 && idle(s));
  });
}
