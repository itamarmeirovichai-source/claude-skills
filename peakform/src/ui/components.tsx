import { createContext, useCallback, useContext, useEffect, useId, useRef, useState, type ReactNode, type RefObject } from 'react';
import { IconBack, IconChevron, IconClose } from './icons';
import { back, Link } from './router';

// Shared building blocks. Large tap targets, clear labels, no colour only signals.

export function PageHead({ title, eyebrow, end, backTo }: { title: string; eyebrow?: string; end?: ReactNode; backTo?: string }) {
  return (
    <>
      {backTo !== undefined && (
        <div className="back-row">
          <button type="button" className="btn btn-ghost" onClick={() => back(backTo)} aria-label="Back">
            <IconBack /> Back
          </button>
        </div>
      )}
      <header className="page-head">
        <div className="grow">
          {eyebrow && <div className="eyebrow">{eyebrow}</div>}
          <h1>{title}</h1>
        </div>
        {end}
      </header>
    </>
  );
}

export function Section({ title, end, children, id }: { title?: string; end?: ReactNode; children: ReactNode; id?: string }) {
  return (
    <section className="section" id={id} aria-label={title}>
      {title && (
        <h2 className="section-title">
          <span>{title}</span>
          {end}
        </h2>
      )}
      {children}
    </section>
  );
}

export function Item({ title, sub, end, to, onClick, icon, chevron, testId }: { title: ReactNode; sub?: ReactNode; end?: ReactNode; to?: string; onClick?: () => void; icon?: ReactNode; chevron?: boolean; testId?: string }) {
  const inner = (
    <>
      {icon}
      <span className="item-main">
        <span className="item-title" style={{ display: 'block' }}>
          {title}
        </span>
        {sub && (
          <span className="item-sub" style={{ display: 'block' }}>
            {sub}
          </span>
        )}
      </span>
      {end && <span className="item-end">{end}</span>}
      {(chevron ?? (to !== undefined || onClick !== undefined)) && <IconChevron className="chev" />}
    </>
  );
  if (to !== undefined)
    return (
      <Link to={to} className="item" data-testid={testId}>
        {inner}
      </Link>
    );
  if (onClick)
    return (
      <button type="button" className="item" onClick={onClick} data-testid={testId}>
        {inner}
      </button>
    );
  return (
    <div className="item" data-testid={testId}>
      {inner}
    </div>
  );
}

export function Note({ tone = 'info', title, children }: { tone?: 'info' | 'warn' | 'danger' | 'accent'; title?: string; children?: ReactNode }) {
  return (
    <div className={`note ${tone === 'info' ? '' : `note-${tone}`}`} role={tone === 'danger' ? 'alert' : undefined}>
      {title && <strong>{title}</strong>}
      {children}
    </div>
  );
}

export function Seg<T extends string | number>({ value, options, onChange, label, tone }: { value: T | null; options: Array<{ value: T; label: string; tone?: 'good' | 'warn' | 'danger' }>; onChange: (v: T) => void; label: string; tone?: boolean }) {
  return (
    <div className={`seg ${tone ? 'seg-good' : ''}`} role="group" aria-label={label}>
      {options.map((o) => (
        <button key={String(o.value)} type="button" aria-pressed={value === o.value} data-tone={o.tone} onClick={() => onChange(o.value)}>
          {o.label}
        </button>
      ))}
    </div>
  );
}

export function Toggle({ checked, onChange, label, sub, testId }: { checked: boolean; onChange: (v: boolean) => void; label: string; sub?: string; testId?: string }) {
  const id = useId();
  return (
    <div className="switch-row">
      <label htmlFor={id} className="grow">
        <span style={{ display: 'block', fontWeight: 560 }}>{label}</span>
        {sub && (
          <span className="small muted" style={{ display: 'block' }}>
            {sub}
          </span>
        )}
      </label>
      <span className="toggle">
        <input id={id} type="checkbox" role="switch" checked={checked} onChange={(e) => onChange(e.target.checked)} data-testid={testId} />
      </span>
    </div>
  );
}

export function Stepper({ label, value, onChange, step = 1, min = 0, max = 9999, decimals = 0, prev, unit, testId, base, placeholder }: { label: string; value: number | null; onChange: (v: number | null) => void; step?: number; min?: number; max?: number; decimals?: number; prev?: string; unit?: string; testId?: string; base?: number | null; placeholder?: string }) {
  const id = useId();
  const [text, setText] = useState(value === null ? '' : String(value));
  useEffect(() => {
    setText(value === null ? '' : String(value));
  }, [value]);
  const clamp = (n: number) => Math.min(max, Math.max(min, Math.round(n * 10 ** decimals) / 10 ** decimals));
  return (
    <div>
      <label className="stepper-label" htmlFor={id}>
        <span>
          {label}
          {unit ? ` (${unit})` : ''}
        </span>
        {prev && <span className="prev">Last {prev}</span>}
      </label>
      <div className="stepper">
        <button type="button" aria-label={`Decrease ${label}`} onClick={() => onChange(clamp(value === null && base != null ? base : (value ?? 0) - step))}>
          −
        </button>
        <input
          id={id}
          data-testid={testId}
          inputMode={decimals > 0 ? 'decimal' : 'numeric'}
          pattern={decimals > 0 ? '[0-9]*[.,]?[0-9]*' : '[0-9]*'}
          value={text}
          onChange={(e) => {
            const t = e.target.value.replace(',', '.');
            setText(t);
            if (t === '') onChange(null);
            else if (!Number.isNaN(Number(t))) onChange(clamp(Number(t)));
          }}
          onFocus={(e) => e.target.select()}
          placeholder={placeholder}
          autoComplete="off"
        />
        <button type="button" aria-label={`Increase ${label}`} onClick={() => onChange(clamp(value === null && base != null ? base : (value ?? 0) + step))}>
          +
        </button>
      </div>
    </div>
  );
}

export function Sheet({ open, onClose, title, children, testId }: { open: boolean; onClose: () => void; title: string; children: ReactNode; testId?: string }) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!open) return;
    const prev = document.activeElement as HTMLElement | null;
    ref.current?.focus();
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', onKey);
    // A toast from the previous step would sit on top of the sheet header.
    window.dispatchEvent(new Event('pf-sheet-open'));
    document.body.style.overflow = 'hidden';
    return () => {
      window.removeEventListener('keydown', onKey);
      document.body.style.overflow = '';
      prev?.focus?.();
    };
  }, [open, onClose]);
  if (!open) return null;
  return (
    <div className="sheet-backdrop" onClick={onClose}>
      <div className="sheet" role="dialog" aria-modal="true" aria-label={title} ref={ref} tabIndex={-1} onClick={(e) => e.stopPropagation()} data-testid={testId}>
        <div className="sheet-grip" aria-hidden="true" />
        <div className="sheet-head">
          <h2>{title}</h2>
          <button type="button" className="btn btn-icon btn-outline" onClick={onClose} aria-label="Close">
            <IconClose />
          </button>
        </div>
        {children}
      </div>
    </div>
  );
}

/** A file chooser styled as a normal button. The native control is visually hidden but stays focusable. */
export function FilePick({ label, accept, onFile, testId, inputRef }: { label: string; accept: string; onFile: (f: File) => void; testId?: string; inputRef?: RefObject<HTMLInputElement | null> }) {
  return (
    <label className="btn btn-outline file-pick">
      <input
        ref={inputRef}
        className="sr-only"
        type="file"
        accept={accept}
        data-testid={testId}
        onChange={(e) => {
          const f = e.target.files?.[0];
          if (f) onFile(f);
        }}
      />
      {label}
    </label>
  );
}

// ---------- Toasts with undo ----------

interface ToastState {
  id: number;
  text: string;
  action?: { label: string; run: () => void };
}
const ToastCtx = createContext<(text: string, action?: ToastState['action']) => void>(() => {});

export function ToastProvider({ children }: { children: ReactNode }) {
  const [t, setT] = useState<ToastState | null>(null);
  const timer = useRef<number | null>(null);
  useEffect(() => {
    const clear = () => setT(null);
    window.addEventListener('hashchange', clear);
    window.addEventListener('pf-sheet-open', clear);
    return () => {
      window.removeEventListener('hashchange', clear);
      window.removeEventListener('pf-sheet-open', clear);
    };
  }, []);
  const show = useCallback((text: string, action?: ToastState['action']) => {
    if (timer.current) window.clearTimeout(timer.current);
    setT({ id: Date.now(), text, action });
    timer.current = window.setTimeout(() => setT(null), action ? 5000 : 2500);
  }, []);
  return (
    <ToastCtx.Provider value={show}>
      {children}
      {t && (
        <div className="toast" role="status" aria-live="polite">
          <span>{t.text}</span>
          {t.action && (
            <button
              type="button"
              className="btn"
              onClick={() => {
                t.action!.run();
                setT(null);
              }}
            >
              {t.action.label}
            </button>
          )}
        </div>
      )}
    </ToastCtx.Provider>
  );
}

export const useToast = () => useContext(ToastCtx);

// ---------- Small helpers ----------

export function Metric({ label, value, sub, testId }: { label: string; value: ReactNode; sub?: ReactNode; testId?: string }) {
  return (
    <div className="metric" data-testid={testId}>
      <div className="m-label">{label}</div>
      <div className="m-value">{value}</div>
      {sub && <div className="m-sub">{sub}</div>}
    </div>
  );
}

/** A bar with the target band and the logged estimate range, readable without colour. */
export function RangeBar({ low, mid, high, band, max, label }: { low: number; mid: number; high: number; band: [number, number]; max: number; label: string }) {
  const pct = (n: number) => `${Math.max(0, Math.min(100, (n / max) * 100))}%`;
  return (
    <div className="bar" role="img" aria-label={label}>
      <div className="bar-range" style={{ left: pct(band[0]), width: `calc(${pct(band[1])} - ${pct(band[0])})` }} />
      <div className="bar-fill" style={{ width: pct(mid) }} />
      {high > low && <div className="bar-est" style={{ left: pct(low), width: `calc(${pct(high)} - ${pct(low)})` }} />}
    </div>
  );
}

export function useOnline(): boolean {
  const [on, setOn] = useState(typeof navigator === 'undefined' ? true : navigator.onLine);
  useEffect(() => {
    const up = () => setOn(true);
    const down = () => setOn(false);
    window.addEventListener('online', up);
    window.addEventListener('offline', down);
    return () => {
      window.removeEventListener('online', up);
      window.removeEventListener('offline', down);
    };
  }, []);
  return on;
}

export function Empty({ title, children }: { title: string; children?: ReactNode }) {
  return (
    <div className="panel" style={{ textAlign: 'center', padding: '20px 16px' }}>
      <h3>{title}</h3>
      {children && <div className="muted small" style={{ marginTop: 6 }}>{children}</div>}
    </div>
  );
}
