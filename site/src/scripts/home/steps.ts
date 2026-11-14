// How it works: three steps, one panel each (Photo / Frame / Film). Panels hard-cut: exactly one is shown,
// the others are `hidden`, so there is never a cross-fade, ghost or double exposure. While the demo is in view
// it advances on its own until the visitor picks a step; under reduced motion it waits for a tap.
import { motionPaused, reducedMotion, saveData } from '../core/prefs';

const HOLD_MS = [3200, 3600, 6200];

export function mountSteps(): void {
  const root = document.querySelector<HTMLElement>('[data-steps]');
  if (!root) return;
  const tabs = [...root.querySelectorAll<HTMLButtonElement>('[role="tab"]')];
  const panels = [...root.querySelectorAll<HTMLElement>('[role="tabpanel"]')];
  const film = root.querySelector<HTMLVideoElement>('video[data-step-film]');
  let cur = 0;
  let auto = !reducedMotion();
  let timer = 0;
  let inView = false;

  const show = (i: number, focus = false): void => {
    cur = (i + tabs.length) % tabs.length;
    tabs.forEach((t, j) => {
      t.setAttribute('aria-selected', String(j === cur));
      t.tabIndex = j === cur ? 0 : -1;
    });
    panels.forEach((p, j) => (p.hidden = j !== cur));
    root.dataset['step'] = String(cur);
    if (focus) tabs[cur]?.focus();
    if (film) {
      const filmOn = !!panels[cur]?.contains(film);
      if (filmOn && !saveData() && !motionPaused()) {
        if (!film.src) film.src = (film.canPlayType('video/mp4; codecs="av01.0.05M.08"') && film.dataset['av1']) || film.dataset['h264'] || '';
        film.currentTime = 0;
        void film.play().catch(() => undefined);
      } else film.pause();
    }
    schedule();
  };
  const schedule = (): void => {
    window.clearTimeout(timer);
    if (auto && inView && !motionPaused()) timer = window.setTimeout(() => show(cur + 1), HOLD_MS[cur] ?? 3500);
  };

  tabs.forEach((t, i) => {
    t.addEventListener('click', () => {
      auto = false;
      show(i);
    });
    t.addEventListener('keydown', (e) => {
      const d = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1 : e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? -1 : 0;
      if (!d) return;
      e.preventDefault();
      auto = false;
      show(cur + d, true);
    });
  });
  new IntersectionObserver(
    ([e]) => {
      inView = !!e?.isIntersecting;
      if (!inView) film?.pause();
      else if (film && panels[cur]?.contains(film) && !motionPaused()) void film.play().catch(() => undefined);
      schedule();
    },
    { threshold: 0.5 },
  ).observe(root.querySelector('[data-monitor]') ?? root);
  show(0);
}
