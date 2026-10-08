// One ticker: GSAP drives Lenis; ScrollTrigger listens to Lenis. Reduced motion → no smoothing.
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Flip } from 'gsap/Flip';
import Lenis from 'lenis';
import { reducedMotion } from './prefs';

export const isTouch = (): boolean => window.matchMedia('(hover: none) and (pointer: coarse)').matches;

gsap.registerPlugin(ScrollTrigger, Flip);

let lenis: Lenis | null = null;

export function initMotion(): void {
  // Lenis on desktop only: touch devices keep native scroll (ref 39 §1.4).
  if (lenis || reducedMotion() || isTouch()) return;
  lenis = new Lenis({ lerp: 0.1, smoothWheel: true, syncTouch: false, anchors: { offset: -64 } });
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((t) => lenis?.raf(t * 1000));
  gsap.ticker.lagSmoothing(0);
  window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', (e) => {
    if (e.matches) {
      lenis?.destroy();
      lenis = null;
    }
  });
}

export function scrollToY(y: number, opts: { immediate?: boolean; duration?: number } = {}): void {
  if (lenis) lenis.scrollTo(y, { immediate: opts.immediate ?? false, force: true, lock: false, ...(opts.duration ? { duration: opts.duration } : {}) });
  else window.scrollTo({ top: y, behavior: opts.immediate || reducedMotion() ? 'instant' : 'smooth' });
}

export function stopSmooth(on: boolean): void {
  if (!lenis) return;
  if (on) lenis.stop();
  else lenis.start();
}

export { gsap, ScrollTrigger, Flip };
