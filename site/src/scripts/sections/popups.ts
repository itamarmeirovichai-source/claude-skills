// The one-off pop-up on /frames/thanks: a short silent clip with a fixed caption, once, then gone.
// Off under reduced motion; "Hide" removes it (remembered).
import '../alpha-video';
import type { AlphaVideo } from '../alpha-video';
import { media, resolveClip } from '../../lib/media';
import { alphaSrc, pickAlphaCodec } from '../core/codec';
import { prefs, reducedMotion, saveData } from '../core/prefs';
import { track } from '../core/analytics';

const hidden = (): boolean => prefs.get().hosts === 'hidden' || reducedMotion();

async function show(pop: HTMLElement): Promise<void> {
  const who = pop.dataset['char'] === 'vee' ? media.vee : media.otto;
  const clip = resolveClip(who, pop.dataset['clip'] ?? '');
  const av = pop.querySelector<AlphaVideo>('alpha-video');
  pop.classList.add('on');
  track('pop_seen', { id: pop.dataset['pop'] ?? '' });
  const codec = await pickAlphaCodec();
  const playing =
    clip && av && codec && !saveData() && prefs.get().motion !== 'paused'
      ? av.play(alphaSrc(clip, codec), { duration: clip.duration, startTimeoutMs: 2500 })
      : new Promise((r) => setTimeout(r, 2500));
  await Promise.race([playing, new Promise((r) => setTimeout(r, 3000))]);
  await new Promise((r) => setTimeout(r, 2200));
  av?.pause();
  pop.classList.remove('on');
}

/** One-off pop (form success). */
export function popNow(pop: HTMLElement | null): void {
  if (!pop || hidden()) return;
  pop.querySelector<HTMLButtonElement>('[data-hide-hosts]')?.addEventListener('click', () => {
    prefs.set({ hosts: 'hidden' });
    pop.classList.remove('on');
    track('character_hide');
  });
  void show(pop);
}
