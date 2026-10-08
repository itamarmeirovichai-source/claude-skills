// The crew on the story page: each <div data-actor> enters its act in three scroll-driven beats
// (ref 39 §2.3): peek ("Down here ↓") → hold → arrive, then says one line with its talking clip.
// Rules: captions always; audio only after "Sound on"; a line is spoken once per session; fast scrolling
// gets the caption only; reduced motion = still frame + caption, no rise.
import '../alpha-video';
import type { AlphaVideo } from '../alpha-video';
import { media, resolveClip, hasRealClip, type CharacterSet } from '../../lib/media';
import { alphaSrc, pickAlphaCodec, type AlphaCodec } from '../core/codec';
import { prefs, reducedMotion, saveData, soundOn } from '../core/prefs';
import { say, heard, draw } from '../core/voice';
import { gsap, ScrollTrigger } from '../core/motion';
import { track } from '../core/analytics';

type Phase = 'off' | 'peek' | 'arrived';
const FAST_PX_S = 1500;

let codec: AlphaCodec | null | undefined;
const live = (): HTMLElement | null => document.querySelector('[data-crew-live]');

export class Actor {
  readonly who: 'otto' | 'vee';
  readonly id: string;
  private set: CharacterSet;
  private av: AlphaVideo;
  private bubble: HTMLElement;
  phase: Phase = 'off';
  private talkGen = 0;
  private capTimer = 0;
  busy = false;

  constructor(readonly el: HTMLElement) {
    this.who = el.dataset['who'] === 'vee' ? 'vee' : 'otto';
    this.id = el.dataset['actor'] ?? '';
    this.set = this.who === 'vee' ? media.vee : media.otto;
    this.av = el.querySelector('alpha-video') as AlphaVideo;
    this.bubble = el.querySelector('[data-bubble]') as HTMLElement;
  }

  private get videoOk(): boolean {
    return !!codec && this.av.ok && !saveData() && !reducedMotion() && prefs.get().motion !== 'paused';
  }
  srcOf(key: string): string {
    const c = codec ? resolveClip(this.set, key) : undefined;
    return c && codec ? alphaSrc(c, codec) : '';
  }
  real(key: string): boolean {
    return hasRealClip(this.set, key);
  }
  usePoster(): void {
    this.el.classList.add('poster-mode');
  }

  /** Play a clip; loops resolve once started, one-shots when they end (or fail fast). */
  async clip(key: string, loop = false, from = 0): Promise<void> {
    if (!this.videoOk) return this.usePoster();
    const src = this.srcOf(key);
    if (!src) return this.usePoster();
    const c = resolveClip(this.set, key);
    const r = await this.av.play(src, { loop, duration: c?.duration ?? 5, startTimeoutMs: 4000, from });
    if (r === 'error' || r === 'timeout') this.usePoster();
  }

  idle(): void {
    if (this.who === 'otto') void this.clip('char_idle', true);
    else if (this.real('vee_idle')) void this.clip('vee_idle', true);
    // Without an idle loop Vee holds the last frame of her walk-in / talk clip (they end on her idle pose).
  }

  caption(text: string, ms = 0): void {
    this.bubble.textContent = text;
    this.el.classList.add('captioned');
    window.clearTimeout(this.capTimer);
    if (ms) this.capTimer = window.setTimeout(() => this.el.classList.remove('captioned'), ms);
  }
  hideCaption(): void {
    this.el.classList.remove('captioned');
  }

  /** Say a line (key or group) with the talking clip; back to idle on the talk clip's own end pose. */
  async talk(keyOrGroup: string, opts: { silent?: boolean } = {}): Promise<void> {
    const my = ++this.talkGen;
    this.busy = true;
    const talkKey = this.who === 'otto' ? 'otto_talk_a' : /pricing|cta|act_v4|act_v5/.test(keyOrGroup) ? 'vee_talk_b' : 'vee_talk_a';
    this.el.classList.add('talking');
    void this.clip(talkKey, true);
    await say(keyOrGroup, {
      caption: (t) => this.caption(t),
      silent: opts.silent ?? false,
      onStart: (key, text, audible) => {
        const l = live();
        if (l) l.textContent = `${this.who === 'vee' ? 'Vee' : 'Otto'}: ${text}`;
        if (audible) track('crew_line_played', { id: key });
      },
    });
    if (my !== this.talkGen) return;
    this.el.classList.remove('talking');
    window.setTimeout(() => my === this.talkGen && this.hideCaption(), 1400);
    if (this.videoOk) await this.av.finishLoop();
    if (my !== this.talkGen) return;
    this.busy = false;
    this.idle();
  }

  pause(): void {
    this.av.pause();
  }
}

// Scroll speed (px/s), smoothed: arrivals during a fast fling stay caption-only.
let vel = 0;
let lastY = 0;
let lastT = 0;
if (typeof window !== 'undefined') {
  window.addEventListener(
    'scroll',
    () => {
      const t = performance.now();
      const dt = t - lastT;
      if (dt > 0 && lastT) vel = vel * 0.6 + ((Math.abs(window.scrollY - lastY) / dt) * 1000) * 0.4;
      lastY = window.scrollY;
      lastT = t;
    },
    { passive: true },
  );
}
const velocity = (): number => (performance.now() - lastT > 250 ? 0 : vel);

/** Speak only when the visitor is reading, not skimming; never replay a line with sound. */
function shouldSpeak(key: string): boolean {
  const v = velocity();
  return v < FAST_PX_S && !heard(key);
}

export interface Entrance {
  actor: Actor;
  /** Fire the arrival line now (used by scenes that time it themselves). */
  speak: (keyOrGroup: string) => Promise<void>;
}

/** Wire one actor's entrance to its act. */
function enter(actor: Actor, touch: boolean): Entrance {
  const el = actor.el;
  const act = el.closest<HTMLElement>('[data-act]') ?? el;
  const peekKey = el.dataset['peek'] ?? '';
  const lineKey = el.dataset['line'] ?? '';
  const arriveAt = Number(el.dataset['arrive'] ?? 0.45);
  const peekOnly = el.hasAttribute('data-peek-only');
  const fromRight = actor.who === 'vee';
  const body = el.querySelector<HTMLElement>('.actor-body') as HTMLElement;
  const rm = reducedMotion();
  let arrivedOnce = false;
  let peekText = '';

  // Real entrance clips do the travelling inside the frame; stand-ins travel by transform.
  const realPeek = actor.who === 'otto' && actor.real('otto_peek');
  const realRise = actor.who === 'otto' && actor.real('otto_rise');
  const realWalk = actor.who === 'vee' && actor.real('vee_walk_in');
  const prop = fromRight ? 'xPercent' : 'yPercent';
  const hidden = 110;
  const peekPos = fromRight ? (realWalk ? 0 : 72) : realPeek ? 0 : 80;
  const move = gsap.quickTo(body, prop, { duration: touch ? 0.9 : 0.7, ease: 'power3.out' });
  gsap.set(body, { [prop]: rm ? 0 : hidden });
  if (rm) {
    el.dataset['state'] = 'arrived';
    actor.usePoster();
  }

  const speak = async (keyOrGroup: string): Promise<void> => {
    if (!keyOrGroup) return;
    const key = draw(keyOrGroup);
    await actor.talk(key, { silent: !soundOn() || !shouldSpeak(key) });
  };

  const toPeek = (): void => {
    actor.phase = 'peek';
    el.dataset['state'] = 'peek';
    if (rm) return;
    move(peekPos);
    if (realPeek) void actor.clip('otto_peek', true);
    else if (realWalk) void (async () => {
      // Vee's first beat: the edge of her walk-in (stopwatch hand), held still.
      const src = actor.srcOf('vee_walk_in');
      if (src && codec) await (el.querySelector('alpha-video') as AlphaVideo).showFrame(src, 0.55).catch(() => false);
    })();
    else if (actor.who === 'otto') actor.idle();
    if (peekKey) {
      peekText = peekText || draw(peekKey);
      const k = peekText;
      const text = media.voice[k]?.text ?? '';
      const arrow = actor.who === 'otto' ? ' ↓' : ' →';
      // "Tells you it's here": caption always, voice only with sound on and only once. No talk clip:
      // he is still only peeking over the edge.
      actor.caption(text + arrow);
      void say(k, {
        caption: (t) => actor.phase === 'peek' && actor.caption(t + arrow),
        silent: !(soundOn() && shouldSpeak(k)),
        holdMs: 400,
        onStart: (_k, t) => {
          const l = live();
          if (l) l.textContent = `${actor.who === 'vee' ? 'Vee' : 'Otto'}: ${t}`;
        },
      });
      track('crew_peek', { id: actor.id });
    }
  };
  const toArrive = (): void => {
    actor.phase = 'arrived';
    el.dataset['state'] = 'arrived';
    actor.hideCaption();
    if (rm) return;
    move(0);
    if (realRise) void actor.clip('otto_rise').then(() => actor.phase === 'arrived' && !actor.busy && actor.idle());
    else if (realWalk) void actor.clip('vee_walk_in', false, 0.55).then(() => actor.phase === 'arrived' && !actor.busy && actor.idle());
    else actor.idle();
    if (!arrivedOnce) {
      arrivedOnce = true;
      if (lineKey) window.setTimeout(() => actor.phase === 'arrived' && void speak(lineKey), realRise || realWalk ? 1600 : 700);
    }
  };
  const toOff = (): void => {
    actor.phase = 'off';
    el.dataset['state'] = 'off';
    actor.hideCaption();
    if (rm) return;
    move(hidden);
    window.setTimeout(() => actor.phase === 'off' && actor.pause(), 900);
  };

  // Phones may pin a different element than desktop (Act III pins only the monitor): optional mobile trigger.
  const narrow = window.matchMedia('(max-width: 899px)').matches;
  const mTrigger = narrow && el.dataset['mtrigger'] ? act.querySelector<HTMLElement>(el.dataset['mtrigger']) : null;
  ScrollTrigger.create({
    trigger: mTrigger ?? act,
    start: el.dataset['start'] || 'top 70%',
    end: el.dataset['end'] || 'bottom bottom',
    onUpdate: (st) => {
      if (rm) return;
      const p = st.progress;
      const want: Phase = p <= 0.001 ? 'off' : peekOnly || p < arriveAt ? 'peek' : 'arrived';
      if (want === actor.phase) return;
      if (want === 'off') toOff();
      else if (want === 'peek' && actor.phase !== 'arrived') toPeek();
      else if (want === 'peek' && actor.phase === 'arrived' && p < arriveAt * 0.5) toPeek();
      else if (want === 'arrived') toArrive();
    },
    onLeaveBack: () => toOff(),
    onLeave: () => window.setTimeout(() => actor.pause(), 1200),
    onEnterBack: () => actor.phase === 'arrived' && !actor.busy && actor.idle(),
  });
  if (rm && lineKey) {
    // Same story in stills: the line shows as a caption when the act comes into view.
    ScrollTrigger.create({ trigger: act, start: 'top 60%', once: true, onEnter: () => actor.caption(media.voice[draw(lineKey)]?.text ?? '', 5000) });
  }
  return { actor, speak };
}

/** Mount every actor on the page. Returns them by id. */
export async function mountCrew(touch: boolean): Promise<Map<string, Entrance>> {
  codec = await pickAlphaCodec();
  const out = new Map<string, Entrance>();
  document.querySelectorAll<HTMLElement>('[data-actor]').forEach((el) => {
    const a = new Actor(el);
    if (!codec || saveData()) a.usePoster();
    out.set(a.id, enter(a, touch));
  });
  return out;
}
