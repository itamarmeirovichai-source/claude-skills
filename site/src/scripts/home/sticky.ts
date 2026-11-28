// Phones: the "5 free frames →" bar shows only once the whole hero (its CTA, the ring, Otto) has scrolled away, and hides whenever another CTA or
// the form is on screen, so it never doubles up or sits on top of them. The page reserves its height at the end.
import { track } from '../core/analytics';

export function mountSticky(): void {
  const bar = document.querySelector<HTMLElement>('[data-sticky]');
  if (!bar || !('IntersectionObserver' in window)) return;
  const visible = new Set<Element>();
  let pastHero = false;
  const sync = (): void => {
    const on = pastHero && visible.size === 0;
    bar.classList.toggle('on', on);
    bar.toggleAttribute('inert', !on);
  };
  const hero = document.getElementById('hero');
  if (hero) {
    new IntersectionObserver(([e]) => {
      if (!e) return;
      // Past = the hero is above the viewport.
      pastHero = !e.isIntersecting && e.boundingClientRect.top < 0;
      sync();
    }).observe(hero);
  }
  const io = new IntersectionObserver(
    (es) => {
      es.forEach((e) => (e.isIntersecting ? visible.add(e.target) : visible.delete(e.target)));
      sync();
    },
    { threshold: 0 },
  );
  document.querySelectorAll('[data-inflow-cta]:not([data-hero-cta]), .site-footer').forEach((el) => io.observe(el));
  bar.querySelector('a')?.addEventListener('click', () => track('sticky_cta_click'));
  sync();
}
