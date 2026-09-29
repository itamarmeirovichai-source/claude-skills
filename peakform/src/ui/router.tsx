import { useEffect, useState, type AnchorHTMLAttributes, type ReactNode } from 'react';

// Hash routing works on any static host and inside the offline service worker.

function current(): string {
  const h = window.location.hash.replace(/^#/, '');
  return h.startsWith('/') ? h : '/today';
}

export function useRoute(): { path: string; parts: string[]; query: URLSearchParams } {
  const [path, setPath] = useState(current);
  useEffect(() => {
    const on = () => setPath(current());
    window.addEventListener('hashchange', on);
    return () => window.removeEventListener('hashchange', on);
  }, []);
  const [p, q] = path.split('?');
  return { path: p ?? '/today', parts: (p ?? '').split('/').filter(Boolean).map(decodeURIComponent), query: new URLSearchParams(q ?? '') };
}

export function navigate(to: string, opts: { replace?: boolean } = {}): void {
  const url = `#${to}`;
  if (opts.replace) window.location.replace(url);
  else window.location.hash = to;
  window.scrollTo({ top: 0 });
}

export function back(fallback = '/today'): void {
  if (window.history.length > 1) window.history.back();
  else navigate(fallback);
}

export function Link({ to, children, ...rest }: { to: string; children: ReactNode } & AnchorHTMLAttributes<HTMLAnchorElement>) {
  return (
    <a href={`#${to}`} {...rest}>
      {children}
    </a>
  );
}
