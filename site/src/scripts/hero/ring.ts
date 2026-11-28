// The orbit: 3–6 film cards on a flat 2D ellipse around Otto. Slow continuous rotation, cards stay upright,
// hover/focus holds it still. Same on phones (a smaller circle); loops only decode on desktop.
// Otto gets the largest size whose box never meets a card anywhere on the orbit (no overlap, ever).
import { isMobile, motionPaused, reducedMotion, saveData } from '../core/prefs';

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
    new ResizeObserver(() => this.layout()).observe(scene);
    this.layout();
    requestAnimationFrame(this.tick);
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

  private tick = (ms: number): void => {
    requestAnimationFrame(this.tick);
    const time = ms / 1000;
    const dt = this.last ? Math.min(0.1, time - this.last) : 0;
    this.last = time;
    if (document.hidden) return;
    const still = motionPaused() || reducedMotion();
    const moving = this.running && !this.hold && !still;
    // Ease the angular speed (≈0.8 s) so a hover settles the ring instead of freezing it.
    this.ease += ((moving ? 1 : 0) - this.ease) * Math.min(1, dt * 3.2);
    if (!moving && this.ease < 0.02) this.ease = 0; // settled: fully still
    if (this.ease > 0.001 && !still) {
      this.angle += this.speed * this.ease * dt;
      this.place();
    }
  };

  /**
   * Measure the scene: card centres ride the largest ellipse that keeps every card inside the scene, and Otto
   * (9:16, centred) gets the largest height whose box, grown by half a card plus a margin, stays inside that
   * ellipse. A convex box inside the ellipse of card centres means no card can ever touch him.
   */
  layout(): void {
    const w = this.scene.clientWidth;
    const h = this.scene.clientHeight;
    const card = this.cards[0];
    const cw = card?.offsetWidth || 64;
    const ch = card?.offsetHeight || 114;
    const pad = 6;
    const rx = Math.max(40, w / 2 - cw / 2 - 1);
    const ry = Math.max(40, h / 2 - ch / 2 - 1);
    const fits = (oh: number): boolean => {
      const x = (oh * 9) / 16 / 2 + cw / 2 + pad;
      const y = oh / 2 + ch / 2 + pad;
      return x < rx && y < ry && (x / rx) ** 2 + (y / ry) ** 2 <= 1;
    };
    let lo = 0;
    let hi = h;
    for (let i = 0; i < 24; i++) {
      const mid = (lo + hi) / 2;
      if (fits(mid)) lo = mid;
      else hi = mid;
    }
    this.scene.style.setProperty('--otto-h', `${Math.floor(lo)}px`);
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
