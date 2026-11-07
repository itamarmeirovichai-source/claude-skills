// Runs on every page: reveal-on-scroll, menu close, small helpers. Kept tiny (no GSAP).
export function initGlobal(): void {
  const els = document.querySelectorAll<HTMLElement>('[data-reveal]');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (es) => {
        for (const e of es) {
          if (e.isIntersecting) {
            e.target.classList.add('is-in');
            io.unobserve(e.target);
          }
        }
      },
      { rootMargin: '0px 0px -8% 0px' },
    );
    els.forEach((el) => io.observe(el));
  } else els.forEach((el) => el.classList.add('is-in'));

  document.addEventListener('click', (e) => {
    const menu = document.querySelector<HTMLDetailsElement>('.menu[open]');
    if (menu && !menu.contains(e.target as Node)) menu.open = false;
  });
}

export function toast(msg: string): void {
  const t = document.getElementById('toast');
  if (!t) return;
  t.textContent = msg;
}
