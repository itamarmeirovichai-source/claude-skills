// One film player for the whole home page (ring cards, "Watch a film", the work grid). A native <dialog>:
// focus trap, Esc and focus return for free. Sound only after "Sound on"; the controls can unmute.
// When a film opened from the hero finishes, the player closes and Otto asks "Another? Or shall we make yours?".
import { filmBySlug, mediaUrl, SPEC_LABEL, VIDEO_TYPES } from '../../lib/media';
import { soundOn } from '../core/prefs';
import { track } from '../core/analytics';
import { hush, request } from './characters';

type From = 'hero' | 'grid';
let from: From = 'grid';

export function mountPlayer(): (slug: string, src: From) => boolean {
  const dialog = document.querySelector<HTMLDialogElement>('[data-film-dialog]');
  const video = document.querySelector<HTMLVideoElement>('[data-fd-video]');
  const label = document.querySelector<HTMLElement>('[data-fd-label]');
  const more = document.querySelector<HTMLAnchorElement>('[data-fd-more]');
  if (!dialog || !video || typeof dialog.showModal !== 'function') return () => false;

  const open = (slug: string, src: From): boolean => {
    const f = filmBySlug(slug);
    if (!f) return false;
    from = src;
    hush();
    const av1 = video.canPlayType(VIDEO_TYPES.av1Audio) || video.canPlayType(VIDEO_TYPES.av1);
    video.src = mediaUrl(av1 ? f.full.av1 : f.full.h264);
    video.poster = mediaUrl(f.poster);
    video.muted = !soundOn();
    video.setAttribute('aria-label', `${f.brand}: ${f.title}. ${SPEC_LABEL(f)}`);
    if (label) label.textContent = SPEC_LABEL(f);
    if (more) more.href = `/work/${f.slug}`;
    dialog.showModal();
    void video.play().catch(() => {
      video.muted = true;
      void video.play().catch(() => undefined);
    });
    track('ad_play', { film: f.slug, from: src });
    return true;
  };

  video.addEventListener('ended', () => {
    track('ad_complete', { from });
    if (from !== 'hero') return;
    dialog.close();
    request('hero', 'o2', 5000);
  });
  dialog.addEventListener('close', () => {
    video.pause();
    video.removeAttribute('src');
    video.load();
  });
  // A tap on the backdrop closes it.
  dialog.addEventListener('click', (e) => e.target === dialog && dialog.close());
  dialog.querySelectorAll<HTMLAnchorElement>('[data-fd-cta]').forEach((a) => a.addEventListener('click', () => dialog.close()));

  // Work grid tiles open here (a modified click still opens the film page).
  document.querySelectorAll<HTMLAnchorElement>('#work .tile').forEach((tile) =>
    tile.addEventListener('click', (e) => {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
      const slug = tile.getAttribute('href')?.split('/').pop() ?? '';
      if (open(slug, 'grid')) e.preventDefault();
    }),
  );
  return open;
}
