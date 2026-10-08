// Section pop-ups: Otto (P1, P2, P5, P6) and Vee (S4, S5). One at a time, once each, ≤2.5 s clip,
// aria-hidden, never over a headline/CTA/form, voice only if sound is on, off under reduced motion,
// and "Hide" removes them all (remembered).
import '../alpha-video';
import type { AlphaVideo } from '../alpha-video';
import { media, resolveClip } from '../../lib/media';
import { alphaSrc, pickAlphaCodec } from '../core/codec';
import { prefs, reducedMotion, saveData } from '../core/prefs';
import { say } from '../core/voice';
import { ScrollTrigger } from '../core/motion';
import { track } from '../core/analytics';

let busy = false;
const queue: HTMLElement[] = [];

const hidden = (): boolean => prefs.get().hosts === 'hidden' || reducedMotion();

async function show(pop: HTMLElement): Promise<void> {
  if (hidden()) return;
  busy = true;
  const who = pop.dataset['char'] === 'vee' ? media.vee : media.otto;
  const clip = resolveClip(who, pop.dataset['clip'] ?? '');
  const av = pop.querySelector<AlphaVideo>('alpha-video');
  const bubble = pop.querySelector<HTMLElement>('[data-bubble]');
  pop.classList.add('on');
  track('pop_seen', { id: pop.dataset['pop'] ?? '' });
  const codec = await pickAlphaCodec();
  const playing =
    clip && av && codec && !saveData() && prefs.get().motion !== 'paused'
      ? av.play(alphaSrc(clip, codec), { duration: clip.duration, startTimeoutMs: 2500 })
      : new Promise((r) => setTimeout(r, 2500));
  const line = pop.dataset['line'] ?? '';
  const spoken = say(line, { caption: (t) => bubble && (bubble.textContent = t), holdMs: 2500 });
  await Promise.all([playing, spoken]);
  await new Promise((r) => setTimeout(r, 1400));
  pop.classList.remove('on');
  pop.classList.add('done');
  busy = false;
  const next = queue.shift();
  if (next) void show(next);
}

export function mountPopups(): void {
  const pops = [...document.querySelectorAll<HTMLElement>('[data-pop]')];
  for (const pop of pops) {
    const trigger = pop.closest('section') ?? pop;
    ScrollTrigger.create({
      trigger,
      start: 'top 62%',
      once: true,
      onEnter: () => {
        if (hidden()) return;
        if (busy) queue.push(pop);
        else void show(pop);
      },
    });
  }
  document.querySelectorAll<HTMLButtonElement>('[data-hide-hosts]').forEach((b) =>
    b.addEventListener('click', () => {
      prefs.set({ hosts: 'hidden' });
      queue.length = 0;
      document.querySelectorAll('[data-pop].on').forEach((p) => p.classList.remove('on'));
      track('character_hide');
    }),
  );
}

/** One-off pop (form success). */
export function popNow(pop: HTMLElement | null): void {
  if (pop && !hidden()) void show(pop);
}
