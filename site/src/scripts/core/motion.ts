// One ticker: GSAP drives Lenis; ScrollTrigger listens to Lenis. Reduced motion → no smoothing.
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Flip } from 'gsap/Flip';
import Lenis from 'lenis';
import { reducedMotion } from './prefs';

gsap.registerPlugin(ScrollTrigger, Flip);

let lenis: Lenis | null = null;

export function initMotion(): void {
  if (lenis || reducedMotion()) return;
  lenis = new Lenis({ lerp: 0.12, smoothWheel: true, syncTouch: false, anchors: false });
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
  else window.scrollTo({ top: y, behavior: opts.immediate || reducedMotion() ? 'auto' : 'smooth' });
}

export function stopSmooth(on: boolean): void {
  if (!lenis) return;
  if (on) lenis.stop();
  else lenis.start();
}

export { gsap, ScrollTrigger, Flip };
