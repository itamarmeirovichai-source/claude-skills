import raw from '../data/media.json';

export interface AlphaClip {
  /** Reuse another clip of the same character until a dedicated one exists. */
  alias?: string;
  av1?: string;
  hevc?: string;
  av1_hd?: string;
  hevc_hd?: string;
  duration: number;
  loop?: boolean;
  small?: boolean;
  markers?: Record<string, number>;
}
export interface CharacterSet {
  poster: string;
  width: number;
  height: number;
  premultiplied?: boolean;
  status?: string;
  pointMap?: Record<'L' | 'R' | 'C', string>;
  clips: Record<string, AlphaClip>;
}
export interface FilmMedia {
  slug: string;
  title: string;
  brand: string;
  category: string;
  duration: number;
  poster: string;
  loop: { av1: string; h264: string };
  full: { av1: string; h264: string };
  captions: string | null;
  /** Overrides the default spec label (e.g. the studio's own film). */
  label?: string;
}
export interface VoiceLine {
  text: string;
  audio: string | null;
  vtt: string | null;
}
export interface MediaManifest {
  base: string;
  otto: CharacterSet;
  vee: CharacterSet;
  films: FilmMedia[];
  voice: Record<string, VoiceLine>;
  stills: Record<string, string>;
}

export const media = raw as unknown as MediaManifest;

export const mediaUrl = (rel: string | null | undefined): string => (rel ? media.base + rel : '');

/** The ring holds 3–6 films (whatever media.json lists, capped at 6); extra entries stay on /work only. */
export const ringFilms = (): FilmMedia[] => media.films.slice(0, 6);

export const filmBySlug = (slug: string): FilmMedia | undefined => media.films.find((f) => f.slug === slug);

export const SPEC_LABEL = (f: Pick<FilmMedia, 'duration' | 'label'>): string =>
  f.label ?? `Spec film · invented brand · 100% AI · ${f.duration} s · one take`;

/** Resolve a clip key, following `alias` (max 3 hops). Markers/duration on the alias entry win. */
export function resolveClip(set: CharacterSet, key: string): (AlphaClip & { av1: string; hevc: string }) | undefined {
  let c = set.clips[key];
  const own = c;
  for (let i = 0; c?.alias && i < 3; i++) c = set.clips[c.alias];
  if (!c?.av1 || !c.hevc) return undefined;
  return { ...c, ...(own?.markers ? { markers: own.markers } : {}), duration: own?.duration ?? c.duration, av1: c.av1, hevc: c.hevc };
}

export const VIDEO_TYPES = {
  av1: 'video/mp4; codecs="av01.0.05M.08"',
  av1Audio: 'video/mp4; codecs="av01.0.05M.08, opus"',
  h264: 'video/mp4; codecs="avc1.640028"',
  h264Audio: 'video/mp4; codecs="avc1.640028, mp4a.40.2"',
  hevc: 'video/mp4; codecs="hvc1.1.6.L93.B0"',
} as const;
