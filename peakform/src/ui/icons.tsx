import type { SVGProps } from 'react';

// Original line icons drawn for PeakForm. 24 x 24 grid, 1.8 stroke.

type P = SVGProps<SVGSVGElement> & { size?: number };

function Base({ size = 24, children, ...rest }: P & { children: React.ReactNode }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false" {...rest}>
      {children}
    </svg>
  );
}

export const IconToday = (p: P) => (
  <Base {...p}>
    <circle cx="12" cy="12" r="8.5" />
    <path d="M12 7v5l3 2" />
  </Base>
);
export const IconTrain = (p: P) => (
  <Base {...p}>
    <path d="M3 12h2M19 12h2M7 8v8M17 8v8M5 10v4M19 10v4M7 12h10" />
  </Base>
);
export const IconEat = (p: P) => (
  <Base {...p}>
    <circle cx="13.5" cy="12" r="7" />
    <circle cx="13.5" cy="12" r="3.5" />
    <path d="M3.5 4v5.5a1.5 1.5 0 0 0 3 0V4M5 11v9" />
  </Base>
);
export const IconProgress = (p: P) => (
  <Base {...p}>
    <path d="M4 19V5M4 19h16" />
    <path d="M7 15l4-4 3 3 5-6" />
  </Base>
);
export const IconMore = (p: P) => (
  <Base {...p}>
    <circle cx="6" cy="12" r="1.3" fill="currentColor" />
    <circle cx="12" cy="12" r="1.3" fill="currentColor" />
    <circle cx="18" cy="12" r="1.3" fill="currentColor" />
  </Base>
);
export const IconChevron = (p: P) => (
  <Base size={18} {...p}>
    <path d="M9 6l6 6-6 6" />
  </Base>
);
export const IconBack = (p: P) => (
  <Base {...p}>
    <path d="M15 5l-7 7 7 7" />
  </Base>
);
export const IconClose = (p: P) => (
  <Base {...p}>
    <path d="M6 6l12 12M18 6L6 18" />
  </Base>
);
export const IconPlus = (p: P) => (
  <Base {...p}>
    <path d="M12 5v14M5 12h14" />
  </Base>
);
export const IconCheck = (p: P) => (
  <Base {...p}>
    <path d="M5 12.5l4.5 4.5L19 7" />
  </Base>
);
export const IconTimer = (p: P) => (
  <Base {...p}>
    <circle cx="12" cy="13" r="7.5" />
    <path d="M12 9v4l2.5 1.5M10 2.5h4" />
  </Base>
);
export const IconScale = (p: P) => (
  <Base {...p}>
    <rect x="4" y="4" width="16" height="16" rx="4" />
    <path d="M8 11a4 4 0 0 1 8 0" />
    <path d="M12 11l1.8-2.2" />
  </Base>
);
export const IconWater = (p: P) => (
  <Base {...p}>
    <path d="M12 3.5c3 4 5.5 7 5.5 10a5.5 5.5 0 0 1-11 0c0-3 2.5-6 5.5-10z" />
  </Base>
);
export const IconMoon = (p: P) => (
  <Base {...p}>
    <path d="M19 14.5A7.5 7.5 0 0 1 9.5 5a7.5 7.5 0 1 0 9.5 9.5z" />
  </Base>
);
export const IconShare = (p: P) => (
  <Base {...p}>
    <path d="M12 15V4M8 8l4-4 4 4" />
    <path d="M6 12v6.5A1.5 1.5 0 0 0 7.5 20h9a1.5 1.5 0 0 0 1.5-1.5V12" />
  </Base>
);
export const IconAlert = (p: P) => (
  <Base {...p}>
    <path d="M12 4l9 16H3z" />
    <path d="M12 10v4M12 17h.01" />
  </Base>
);
export const IconPlay = (p: P) => (
  <Base {...p}>
    <path d="M8 5.5v13l10.5-6.5z" />
  </Base>
);
export const IconCamera = (p: P) => (
  <Base {...p}>
    <path d="M4 8.5h3l1.5-2h7l1.5 2h3v10H4z" />
    <circle cx="12" cy="13.5" r="3.3" />
  </Base>
);
export const IconSearch = (p: P) => (
  <Base {...p}>
    <circle cx="11" cy="11" r="6.5" />
    <path d="M16 16l4 4" />
  </Base>
);
export const IconUndo = (p: P) => (
  <Base {...p}>
    <path d="M9 7L4.5 11.5 9 16" />
    <path d="M5 11.5h9a5 5 0 0 1 0 10h-2" />
  </Base>
);
export const IconLock = (p: P) => (
  <Base {...p}>
    <rect x="5" y="10.5" width="14" height="9.5" rx="2" />
    <path d="M8 10.5V8a4 4 0 0 1 8 0v2.5" />
  </Base>
);
