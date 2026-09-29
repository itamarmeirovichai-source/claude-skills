// Progressive enhancements. Every function fails quietly when the API is missing.

let audioCtx: AudioContext | null = null;
let wakeLock: WakeLockSentinel | null = null;

/** Create the audio context during a user gesture so iOS allows sound later. */
export function unlockAudio(): void {
  try {
    const Ctx = window.AudioContext ?? (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
    if (!Ctx) return;
    if (!audioCtx) audioCtx = new Ctx();
    if (audioCtx.state === 'suspended') void audioCtx.resume();
  } catch {
    audioCtx = null;
  }
}

function tone(freq: number, start: number, dur: number) {
  if (!audioCtx) return;
  const o = audioCtx.createOscillator();
  const g = audioCtx.createGain();
  o.type = 'sine';
  o.frequency.value = freq;
  g.gain.setValueAtTime(0.0001, audioCtx.currentTime + start);
  g.gain.exponentialRampToValueAtTime(0.25, audioCtx.currentTime + start + 0.02);
  g.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + start + dur);
  o.connect(g).connect(audioCtx.destination);
  o.start(audioCtx.currentTime + start);
  o.stop(audioCtx.currentTime + start + dur + 0.05);
}

export function cue(sound: 'off' | 'beep' | 'chime', vibrate: boolean): void {
  try {
    if (sound === 'beep') {
      tone(880, 0, 0.15);
      tone(880, 0.25, 0.15);
    } else if (sound === 'chime') {
      tone(660, 0, 0.25);
      tone(990, 0.18, 0.35);
    }
  } catch {
    /* no audio */
  }
  if (vibrate) haptic([120, 60, 120]);
}

export function haptic(pattern: number | number[] = 12): void {
  try {
    if (typeof navigator.vibrate === 'function') navigator.vibrate(pattern);
  } catch {
    /* not supported, for example on iPhone */
  }
}

export function supportsWakeLock(): boolean {
  return typeof navigator !== 'undefined' && 'wakeLock' in navigator;
}

export async function keepAwake(): Promise<boolean> {
  try {
    if (!supportsWakeLock()) return false;
    if (wakeLock && !wakeLock.released) return true;
    wakeLock = await navigator.wakeLock.request('screen');
    return true;
  } catch {
    return false;
  }
}

export async function releaseAwake(): Promise<void> {
  try {
    await wakeLock?.release();
  } catch {
    /* ignore */
  }
  wakeLock = null;
}

// ---------- Files and sharing ----------

export function canShareFiles(files: File[]): boolean {
  try {
    return typeof navigator.canShare === 'function' && navigator.canShare({ files });
  } catch {
    return false;
  }
}

export function downloadBlob(name: string, blob: Blob): void {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = name;
  a.rel = 'noopener';
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 4000);
}

/** Share files when the device supports it, otherwise download them. Returns what happened. */
export async function shareOrDownload(files: File[], title: string): Promise<'shared' | 'downloaded' | 'cancelled'> {
  if (canShareFiles(files)) {
    try {
      await navigator.share({ files, title });
      return 'shared';
    } catch (e) {
      if ((e as DOMException)?.name === 'AbortError') return 'cancelled';
    }
  }
  for (const f of files) downloadBlob(f.name, f);
  return 'downloaded';
}

export async function requestPersistence(): Promise<boolean | null> {
  try {
    if (!navigator.storage?.persist) return null;
    if (await navigator.storage.persisted()) return true;
    return await navigator.storage.persist();
  } catch {
    return null;
  }
}

export async function storageEstimate(): Promise<{ usage: number; quota: number; persisted: boolean | null } | null> {
  try {
    const est = await navigator.storage?.estimate?.();
    const persisted = navigator.storage?.persisted ? await navigator.storage.persisted() : null;
    if (!est) return null;
    return { usage: est.usage ?? 0, quota: est.quota ?? 0, persisted };
  } catch {
    return null;
  }
}

export function isStandalone(): boolean {
  return window.matchMedia?.('(display-mode: standalone)').matches || (navigator as unknown as { standalone?: boolean }).standalone === true;
}

/** Compress a photo to a small JPEG data URL for local storage. */
export async function compressImage(file: File, maxSide = 1024, quality = 0.72): Promise<{ dataUrl: string; bytes: number }> {
  const bitmap = await createImageBitmap(file);
  const scale = Math.min(1, maxSide / Math.max(bitmap.width, bitmap.height));
  const canvas = document.createElement('canvas');
  canvas.width = Math.round(bitmap.width * scale);
  canvas.height = Math.round(bitmap.height * scale);
  canvas.getContext('2d')?.drawImage(bitmap, 0, 0, canvas.width, canvas.height);
  const dataUrl = canvas.toDataURL('image/jpeg', quality);
  return { dataUrl, bytes: Math.round((dataUrl.length * 3) / 4) };
}
