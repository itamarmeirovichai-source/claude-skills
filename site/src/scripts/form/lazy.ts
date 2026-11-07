// Loads the form code (and zod) only when a form nears the viewport or gets focus.
export function mountLazyForms(): void {
  const forms = [...document.querySelectorAll<HTMLFormElement>('form[data-lead-form], form[data-qualify-form]')];
  if (!forms.length) return;
  let loaded = false;
  const load = (): void => {
    if (loaded) return;
    loaded = true;
    void import('./lead-form').then((m) => forms.forEach((f) => m.mountForm(f)));
  };
  const io = new IntersectionObserver((es) => es.some((e) => e.isIntersecting) && load(), { rootMargin: '600px 0px' });
  forms.forEach((f) => {
    io.observe(f);
    f.addEventListener('focusin', load, { once: true });
    f.addEventListener('submit', (e) => {
      if (!loaded) {
        e.preventDefault();
        load();
      }
    }, { once: true });
  });
}
