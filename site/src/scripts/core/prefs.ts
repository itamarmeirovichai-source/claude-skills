// Visitor preferences (per browser) + session flags. localStorage access is always guarded.
export interface Prefs {
  sound?: 'on' | 'off';
  motion?: 'paused' | 'running';
  hosts?: 'hidden' | 'shown';
}
const KEY = 'vxo:prefs';
type Listener = (p: Prefs) => void;
const listeners = new Set<Listener>();

function read(): Prefs {
  try {
    return JSON.parse(localStorage.getItem(KEY) ?? '{}') as Prefs;
  } catch {
    return {};
  }
}
let current: Prefs = read();

export const prefs = {
  get: (): Prefs => current,
  set(patch: Prefs): void {
    current = { ...current, ...patch };
    try {
      localStorage.setItem(KEY, JSON.stringify(current));
    } catch {
      /* private mode: keep in memory */
    }
    const root = document.documentElement;
    root.classList.toggle('motion-paused', current.motion === 'paused');
    root.classList.toggle('hosts-hidden', current.hosts === 'hidden');
    listeners.forEach((l) => l(current));
  },
  on(l: Listener): () => void {
    listeners.add(l);
    return () => listeners.delete(l);
  },
};

/** True after the first click/tap/key on the page: audio may play from now on. */
export const session = { gesture: false };
const markGesture = (): void => {
  session.gesture = true;
};
if (typeof window !== 'undefined') {
  for (const ev of ['pointerdown', 'keydown'] as const) window.addEventListener(ev, markGesture, { capture: true, passive: true });
}

/** Crew voices and film sound only after the visitor chose "Sound on" (and tapped this visit). */
export const soundOn = (): boolean => session.gesture && current.sound === 'on';

export const reducedMotion = (): boolean => window.matchMedia('(prefers-reduced-motion: reduce)').matches;
export const motionPaused = (): boolean => current.motion === 'paused' || reducedMotion();
export const saveData = (): boolean =>
  Boolean((navigator as Navigator & { connection?: { saveData?: boolean } }).connection?.saveData);
export const isMobile = (): boolean => window.matchMedia('(max-width: 767px)').matches;
