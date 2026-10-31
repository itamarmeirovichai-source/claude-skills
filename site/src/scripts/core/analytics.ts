// Cookieless events → /api/e (Analytics Engine when bound). No IDs, no PII.
export function track(name: string, props: Record<string, string | number | boolean> = {}): void {
  if (!import.meta.env.PROD) return;
  try {
    const body = JSON.stringify({ n: name, p: props, path: location.pathname });
    navigator.sendBeacon?.('/api/e', new Blob([body], { type: 'application/json' }));
  } catch {
    /* never break the page for analytics */
  }
}
