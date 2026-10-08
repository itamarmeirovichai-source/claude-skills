// The orbit: N (3–6) film cards on a CSS-3D ellipse around Otto (desktop), or a swipeable row (mobile).
// Cards are billboards (always face the viewer) placed with translate3d, so they pass behind Otto.
import { gsap } from 'gsap';
import type { Dir } from './machine';
import { isMobile, motionPaused, saveData } from '../core/prefs';

const MAX_DECODERS_DESKTOP = 3;
const MAX_DECODERS_MOBILE = 3;

export class Ring {
  private items: HTMLElement[];
  private cards: HTMLAnchorElement[];
  private videos: HTMLVideoElement[];
  private angle = 0; // radians; card i sits at angle + i*step
  private running = false;
  private hold = false; // hover/focus stops rotation
  private speed = 0.12; // rad/s
  private step: number;
  private last = 0;
  private tween: gsap.core.Tween | null = null;
  private loopsOn = new Set<number>();
  private io: IntersectionObserver | null = null;
  private visibleMobile = new Set<number>();
  private loopsEnabled = true;

  constructor(root: HTMLElement, private hero: HTMLElement, private ottoFrame: HTMLElement) {
    this.items = [...root.querySelectorAll<HTMLElement>('.ring-item')];
    this.cards = [...root.querySelectorAll<HTMLAnchorElement>('[data-card]')];
    this.videos = this.cards.map((c) => c.querySelector('video') as HTMLVideoElement);
    this.step = (Math.PI * 2) / Math.max(1, this.items.length);
    root.addEventListener('pointerenter', () => (this.hold = true));
    root.addEventListener('pointerleave', () => (this.hold = false));
    root.addEventListener('focusin', () => (this.hold = true));
    root.addEventListener('focusout', () => (this.hold = false));
    root.addEventListener('keydown', (e) => {
      if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      e.preventDefault();
      const i = this.frontIndex() + (e.key === 'ArrowRight' ? 1 : -1);
      const n = this.items.length;
      const next = ((i % n) + n) % n;
      this.rotateTo(next);
      this.cards[next]?.focus({ preventScroll: true });
    });
    this.io = new IntersectionObserver(
      (es) => {
        for (const e of es) {
          const i = Number((e.target as HTMLElement).dataset['i']);
          if (e.isIntersecting) this.visibleMobile.add(i);
          else this.visibleMobile.delete(i);
        }
        if (isMobile()) this.assignLoops();
      },
      { root: root.querySelector('.ring-track'), threshold: 0.6 },
    );
    this.items.forEach((it) => this.io?.observe(it));
    gsap.ticker.add(this.tick);
    window.addEventListener('resize', () => this.layout());
    this.layout();
  }

  get count(): number {
    return this.items.length;
  }

  run(on: boolean): void {
    this.running = on;
    this.loopsEnabled = on || !isMobile();
    this.assignLoops();
  }

  setLoops(on: boolean): void {
    this.loopsEnabled = on;
    this.assignLoops();
  }

  private tick = (time: number): void => {
    const dt = this.last ? Math.min(0.1, time - this.last) : 0;
    this.last = time;
    if (isMobile()) return;
    if (this.running && !this.hold && !this.tween && !motionPaused()) {
      this.angle -= this.speed * dt;
      this.layout();
    }
  };

  /** Place every card on the ellipse; also refresh which cards may decode a loop. */
  layout(): void {
    if (isMobile()) {
      this.items.forEach((it) => (it.style.transform = ''));
      return;
    }
    const w = this.hero.clientWidth;
    const frame = this.ottoFrame.getBoundingClientRect();
    const rx = Math.min(Math.max(frame.width * 0.95, 220), w * 0.34);
    const rz = rx * 0.75;
    const ry = frame.height * 0.06;
    this.items.forEach((it, i) => {
      const a = this.angle + i * this.step;
      const x = Math.sin(a) * rx;
      const z = Math.cos(a) * rz;
      const y = -Math.cos(a) * ry; // the far side rides a little higher: an orbit, not a flat circle
      const depth = (Math.cos(a) + 1) / 2; // 0 back … 1 front
      it.style.transform = `translate3d(${x.toFixed(1)}px, ${y.toFixed(1)}px, ${z.toFixed(1)}px)`;
      it.style.opacity = (0.45 + depth * 0.55).toFixed(2);
      it.style.filter = depth < 0.35 ? `brightness(${(0.5 + depth).toFixed(2)})` : '';
      it.style.zIndex = String(Math.round(depth * 10));
    });
    this.assignLoops();
  }

  frontIndex(): number {
    let best = 0;
    let bestZ = -Infinity;
    this.items.forEach((_, i) => {
      const z = Math.cos(this.angle + i * this.step);
      if (z > bestZ) {
        bestZ = z;
        best = i;
      }
    });
    return best;
  }

  /** Ease card i to the front (desktop) or scroll it into view (mobile). */
  rotateTo(i: number, duration = 0.6): Promise<void> {
    if (isMobile()) {
      this.items[i]?.scrollIntoView({ behavior: motionPaused() ? 'auto' : 'smooth', inline: 'center', block: 'nearest' });
      return Promise.resolve();
    }
    const target = -i * this.step;
    let delta = (target - this.angle) % (Math.PI * 2);
    if (delta > Math.PI) delta -= Math.PI * 2;
    if (delta < -Math.PI) delta += Math.PI * 2;
    this.tween?.kill();
    const state = { a: this.angle };
    return new Promise((resolve) => {
      this.tween = gsap.to(state, {
        a: this.angle + delta,
        duration: motionPaused() ? 0 : duration,
        ease: 'power3.inOut',
        onUpdate: () => {
          this.angle = state.a;
          this.layout();
        },
        onComplete: () => {
          this.tween = null;
          resolve();
        },
      });
    });
  }

  /** Where is card i relative to Otto? Left third / right third / centre of the hero. */
  dirOf(i: number): Dir {
    const card = this.cards[i];
    if (!card) return 'C';
    const r = card.getBoundingClientRect();
    const o = this.ottoFrame.getBoundingClientRect();
    const cx = r.left + r.width / 2;
    const ox = o.left + o.width / 2;
    const third = Math.max(o.width * 0.5, this.hero.clientWidth / 6);
    if (cx < ox - third) return 'L';
    if (cx > ox + third) return 'R';
    return 'C';
  }

  card(i: number): HTMLAnchorElement | undefined {
    return this.cards[i];
  }

  /** Decoder budget: only the front-most (desktop) or visible (mobile) cards play loops. */
  private assignLoops(): void {
    const allow = new Set<number>();
    if (this.loopsEnabled && !motionPaused() && !saveData()) {
      if (isMobile()) {
        [...this.visibleMobile].slice(0, MAX_DECODERS_MOBILE).forEach((i) => allow.add(i));
      } else {
        this.items
          .map((_, i) => ({ i, z: Math.cos(this.angle + i * this.step) }))
          .sort((a, b) => b.z - a.z)
          .slice(0, MAX_DECODERS_DESKTOP)
          .forEach(({ i }) => allow.add(i));
      }
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
        v.removeAttribute('src');
        v.load();
      }
    });
  }
}

function pickLoop(v: HTMLVideoElement): string {
  const av1 = v.dataset['loopAv1'] ?? '';
  const h264 = v.dataset['loopH264'] ?? '';
  return v.canPlayType('video/mp4; codecs="av01.0.05M.08"') && av1 ? av1 : h264 || av1;
}
