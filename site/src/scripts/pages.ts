// Inner pages: tile loops, /work filter, lazy forms, the form-success pop on /frames/thanks.
import { mountTiles } from './sections/tiles';
import { mountLazyForms } from './form/lazy';

mountTiles();
mountLazyForms();

const filter = document.querySelector<HTMLElement>('[data-filter]');
if (filter) {
  const tiles = [...document.querySelectorAll<HTMLElement>('[data-category]')];
  filter.hidden = false;
  filter.addEventListener('click', (e) => {
    const b = (e.target as HTMLElement).closest<HTMLButtonElement>('button[data-cat]');
    if (!b) return;
    const cat = b.dataset['cat'] ?? 'All';
    filter.querySelectorAll('button').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
    tiles.forEach((t) => (t.closest('li')!.hidden = cat !== 'All' && t.dataset['category'] !== cat));
  });
}

const thumb = document.querySelector<HTMLElement>('[data-pop="success"]');
if (thumb) {
  void import('./core/motion').then(() => import('./sections/popups')).then((m) => m.popNow(thumb));
}
