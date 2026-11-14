// Muted loops on film tiles: play only while on screen, ≤3 decoding at once, posters under Save-Data/paused motion.
import { motionPaused, saveData } from '../core/prefs';

const MAX = 3;
export function mountTiles(root: ParentNode = document): void {
  const vids = [...root.querySelectorAll<HTMLVideoElement>('video[data-tile-loop]')];
  if (!vids.length || !('IntersectionObserver' in window)) return;
  const playing = new Set<HTMLVideoElement>();
  const src = (v: HTMLVideoElement): string => {
    const av1 = v.dataset['av1'] ?? '';
    const h264 = v.dataset['h264'] ?? '';
    return v.canPlayType('video/mp4; codecs="av01.0.05M.08"') && av1 ? av1 : h264 || av1;
  };
  const stop = (v: HTMLVideoElement): void => {
    playing.delete(v);
    v.classList.remove('on');
    v.pause();
  };
  const io = new IntersectionObserver(
    (es) => {
      for (const e of es) {
        const v = e.target as HTMLVideoElement;
        if (e.isIntersecting && !motionPaused() && !saveData() && playing.size < MAX) {
          if (!v.src) v.src = src(v);
          playing.add(v);
          v.play()
            .then(() => v.classList.add('on'))
            .catch(() => stop(v));
        } else if (!e.isIntersecting && playing.has(v)) stop(v);
      }
    },
    { threshold: 0.5 },
  );
  vids.forEach((v) => io.observe(v));
}
