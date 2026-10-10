// Hero: the ring of films around Otto. Tap a card (or "Watch a film") and the film opens in the player.
// Otto himself (idle loop, his lines) belongs to the line director in scripts/home/characters.ts.
import { Ring } from './ring';
import { prefs } from '../core/prefs';
import { track } from '../core/analytics';

export function mountHero(open: (slug: string, from: 'hero' | 'grid') => boolean): void {
  const hero = document.getElementById('hero');
  const ringEl = hero?.querySelector<HTMLElement>('[data-ring]');
  const scene = hero?.querySelector<HTMLElement>('[data-scene]');
  if (!hero || !ringEl || !scene) return;
  const ring = new Ring(ringEl, scene);

  hero.querySelectorAll<HTMLAnchorElement>('[data-card]').forEach((card) =>
    card.addEventListener('click', (e) => {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
      if (open(card.dataset['slug'] ?? '', 'hero')) e.preventDefault();
    }),
  );
  hero.querySelector<HTMLAnchorElement>('[data-watch-film]')?.addEventListener('click', (e) => {
    if (open(e.currentTarget instanceof HTMLElement ? (e.currentTarget.dataset['watchFilm'] ?? '') : '', 'hero')) e.preventDefault();
  });

  const motionBtn = hero.querySelector<HTMLButtonElement>('[data-motion]');
  const syncMotion = (): void => {
    const paused = prefs.get().motion === 'paused';
    motionBtn?.setAttribute('aria-pressed', String(paused));
    if (motionBtn) motionBtn.textContent = paused ? 'Play motion' : 'Pause motion';
    ring.setLoops(!paused);
  };
  motionBtn?.addEventListener('click', () => {
    prefs.set({ motion: prefs.get().motion === 'paused' ? 'running' : 'paused' });
    track('motion_pause', { on: prefs.get().motion === 'paused' ? 1 : 0 });
    syncMotion();
  });
  syncMotion();

  // Off screen: no orbit, no card loops.
  new IntersectionObserver(([e]) => {
    const on = !!e?.isIntersecting;
    ring.run(on);
    ring.setLoops(on && prefs.get().motion !== 'paused');
  }).observe(scene);
  hero.dataset['state'] = 'idle';
}
