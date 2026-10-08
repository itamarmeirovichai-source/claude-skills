import type { AlphaClip } from '../../lib/media';
import { VIDEO_TYPES, mediaUrl } from '../../lib/media';

export type AlphaCodec = 'av1' | 'hevc';
let picked: Promise<AlphaCodec | null> | null = null;

async function decodes(contentType: string, w: number, h: number): Promise<{ supported: boolean; smooth: boolean; powerEfficient: boolean }> {
  try {
    if ('mediaCapabilities' in navigator) {
      const r = await navigator.mediaCapabilities.decodingInfo({
        type: 'file',
        video: { contentType, width: w, height: h, bitrate: 1_500_000, framerate: 24 },
      });
      return { supported: r.supported, smooth: r.smooth, powerEfficient: r.powerEfficient };
    }
  } catch {
    /* fall through */
  }
  const ok = document.createElement('video').canPlayType(contentType) !== '';
  return { supported: ok, smooth: ok, powerEfficient: ok };
}

/** AV1 when hardware-smooth, else HEVC (Apple), else software AV1, else nothing (poster only). */
export function pickAlphaCodec(): Promise<AlphaCodec | null> {
  picked ??= (async () => {
    const [av1, hevc] = await Promise.all([decodes(VIDEO_TYPES.av1, 540, 1920), decodes(VIDEO_TYPES.hevc, 540, 1920)]);
    if (av1.supported && av1.smooth && av1.powerEfficient) return 'av1';
    if (hevc.supported) return 'hevc';
    if (av1.supported) return 'av1';
    return null;
  })();
  return picked;
}

export function alphaSrc(clip: AlphaClip & { av1: string; hevc: string }, codec: AlphaCodec): string {
  const hd = window.matchMedia('(min-width: 1024px)').matches && window.devicePixelRatio >= 1;
  const rel = codec === 'av1' ? (hd && clip.av1_hd) || clip.av1 : (hd && clip.hevc_hd) || clip.hevc;
  return mediaUrl(rel);
}
