// The orbit: 3–6 film cards on a flat 2D ellipse around Otto. Slow continuous rotation, cards stay upright,
// hover/focus holds it still. Same on phones (a smaller circle); loops only decode on desktop.
import { gsap } from 'gsap';
import type { Dir } from './machine';
import { isMobile, motionPaused, saveData } from '../core/prefs';

const LOOP_PERIOD_S = 84; // one full orbit: slow enough to read, fast enough to notice
const MAX_LOOPS_DESKTOP = 4; // + Otto = 5 decoders (ref 39 §1.4)

export class Ring {
  private items: HTMLElement[];
  private cards: HTMLAnchorElement[];
  private videos: HTMLVideoElement[];
  private angle = 0; // radians; card i sits at angle + i*step, 0 = top
  private running = false;
  private hold = false;
  private speed = (Math.PI * 2) / LOOP_PERIOD_S;
  private ease = 1; // 0..1: the orbit eases in/out of a hold instead of stopping dead
  private step: number;
  private last = 0;
  private tween: gsap.core.Tween | null = null;
  private loopsOn = new Set<number>();
  private loopsEnabled = true;
  private geo = { rx: 0, ry: 0 };

  constructor(private root: HTMLElement, private scene: HTMLElement) {
    this.items = [...root.querySelectorAll<HTMLElement>('.ring-item')];
    this.cards = [...root.querySelectorAll<HTMLAnchorElement>('[data-card]')];
    this.videos = this.cards.map((c) => c.querySelector('video') as HTMLVideoElement);
    this.step = (Math.PI * 2) / Math.max(1, this.items.length);
    this.angle = -this.step / 2; // start with no card dead-centre over Otto's hat
    const on = (): void => void (this.hold = true);
    const off = (): void => void (this.hold = this.root.contains(document.activeElement));
    root.addEventListener('pointerover', (e) => (e.target as HTMLElement).closest('.card') && on());
    root.addEventListener('pointerout', (e) => (e.target as HTMLElement).closest('.card') && (this.hold = false));
    root.addEventListener('focusin', on);
    root.addEventListener('focusout', () => queueMicrotask(off));
    root.addEventListener('keydown', (e) => {
      if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      e.preventDefault();
      const n = this.items.length;
      const cur = this.cards.findIndex((c) => c === document.activeElement);
      const next = ((((cur < 0 ? 0 : cur) + (e.key === 'ArrowRight' ? 1 : -1)) % n) + n) % n;
      this.cards[next]?.focus({ preventScroll: true });
    });
    gsap.ticker.add(this.tick);
    new ResizeObserver(() => this.layout()).observe(scene);
    this.layout();
  }

  get count(): number {
    return this.items.length;
  }

  run(on: boolean): void {
    this.running = on;
    this.assignLoops();
  }

  setLoops(on: boolean): void {
    this.loopsEnabled = on;
    this.assignLoops();
  }

  private tick = (time: number): void => {
    const dt = this.last ? Math.min(0.1, time - this.last) : 0;
    this.last = time;
    const moving = this.running && !this.hold && !this.tween && !motionPaused();
    // Ease the angular speed (≈0.8 s) so a hover settles the ring instead of freezing it.
    this.ease += ((moving ? 1 : 0) - this.ease) * Math.min(1, dt * 3.2);
    if (!moving && this.ease < 0.02) this.ease = 0; // settled: fully still
    if (this.ease > 0.001 && !this.tween && !motionPaused()) {
      this.angle += this.speed * this.ease * dt;
      this.place();
    }
  };

  /** Measure the scene and size the ellipse so cards clear Otto's face. */
  layout(): void {
    const w = this.scene.clientWidth;
    const h = this.scene.clientHeight;
    const card = this.cards[0]?.getBoundingClientRect();
    const cw = card?.width || 80;
    const ch = card?.height || 142;
    const ry = Math.max(40, h / 2 - ch / 2 - 6);
    const rx = Math.max(40, Math.min(w / 2 - cw / 2 - 6, ry * 1.35));
    this.geo = { rx, ry };
    this.place();
  }

  private place(): void {
    const { rx, ry } = this.geo;
    this.items.forEach((it, i) => {
      const a = this.angle + i * this.step;
      const x = Math.sin(a) * rx;
      const y = -Math.cos(a) * ry;
      it.style.transform = `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px)`;
    });
  }

  /** The card nearest the bottom of the ring (closest to the visitor's hand). */
  frontIndex(): number {
    let best = 0;
    let bestY = -Infinity;
    this.items.forEach((_, i) => {
      const y = -Math.cos(this.angle + i * this.step);
      if (y > bestY) {
        bestY = y;
        best = i;
      }
    });
    return best;
  }

  /** Where is card i relative to Otto? */
  dirOf(i: number): Dir {
    const a = this.angle + i * this.step;
    const x = Math.sin(a);
    if (x < -0.35) return 'L';
    if (x > 0.35) return 'R';
    return 'C';
  }

  card(i: number): HTMLAnchorElement | undefined {
    return this.cards[i];
  }

  /** Decoder budget: desktop plays every card loop (≤4); phones show posters (Otto is the one decoder). */
  private assignLoops(): void {
    const allow = new Set<number>();
    if (this.loopsEnabled && !motionPaused() && !saveData() && !isMobile()) {
      this.items.slice(0, MAX_LOOPS_DESKTOP).forEach((_, i) => allow.add(i));
    }
    this.videos.forEach((v, i) => {
      if (allow.has(i) && !this.loopsOn.has(i)) {
        this.loopsOn.add(i);
        if (!v.src) v.src = pickLoop(v);
        v.play()
          .then(() => v.classList.add('on'))
          .catch(() => undefined);
      } else if (!allow.has(i) && this.loopsOn.has(i)) {
        this.loopsOn.delete(i);
        v.classList.remove('on');
        v.pause();
      }
    });
  }
}

function pickLoop(v: HTMLVideoElement): string {
  const av1 = v.dataset['loopAv1'] ?? '';
  const h264 = v.dataset['loopH264'] ?? '';
  return v.canPlayType('video/mp4; codecs="av01.0.05M.08"') && av1 ? av1 : h264 || av1;
}
