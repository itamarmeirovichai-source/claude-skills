// PIN hashing for the optional app lock. The lock is a privacy convenience, not encryption.

export function newSalt(): string {
  const b = crypto.getRandomValues(new Uint8Array(16));
  return btoa(String.fromCharCode(...b));
}

export async function hashPin(pin: string, salt: string): Promise<string> {
  const saltBytes = Uint8Array.from(atob(salt), (c) => c.charCodeAt(0));
  const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(pin), 'PBKDF2', false, ['deriveBits']);
  const bits = await crypto.subtle.deriveBits({ name: 'PBKDF2', hash: 'SHA-256', salt: saltBytes, iterations: 150000 }, key, 256);
  return btoa(String.fromCharCode(...new Uint8Array(bits)));
}

export async function verifyPin(pin: string, salt: string, hash: string): Promise<boolean> {
  return (await hashPin(pin, salt)) === hash;
}
