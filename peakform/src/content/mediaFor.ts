import { MEDIA } from './media';
import type { MediaReference } from './types';

export function mediaFor(targetId: string): MediaReference[] {
  return MEDIA.filter((m) => m.targetId === targetId);
}
