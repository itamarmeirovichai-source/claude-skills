// Before/after: a native range input drives clip-path (keyboard support for free).
import { track } from '../core/analytics';
export function mountBeforeAfter(): void {
  document.querySelectorAll<HTMLElement>('[data-ba]').forEach((el) => {
    const input = el.querySelector<HTMLInputElement>('input[type="range"]');
    if (!input) return;
    let used = false;
    const set = (): void => {
      el.style.setProperty('--pos', `${input.value}%`);
      if (!used) {
        used = true;
        track('ba_slider_used');
      }
    };
    input.addEventListener('input', set);
    el.style.setProperty('--pos', `${input.value}%`);
  });
}
