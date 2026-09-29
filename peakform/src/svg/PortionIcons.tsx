import type { PortionKey } from '../domain/portions';

// Original visual portion icons for Estimate by Eye.

const S = { fill: 'none', stroke: 'currentColor', strokeWidth: 1.6, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const };

export function PortionIcon({ k, size = 40 }: { k: PortionKey; size?: number }) {
  const common = { width: size, height: size, viewBox: '0 0 40 40', 'aria-hidden': true as const };
  switch (k) {
    case 'palm':
      return (
        <svg {...common}>
          <path {...S} d="M12 34c-2-4-3-9-3-14 0-5 4-8 11-8s11 3 11 8c0 5-1 10-3 14z" />
          <path {...S} d="M13 20h14" opacity=".5" />
        </svg>
      );
    case 'fist':
      return (
        <svg {...common}>
          <rect {...S} x="9" y="11" width="22" height="20" rx="7" />
          <path {...S} d="M15 11v7M20.5 11v7M26 11v7M9 22h8" />
        </svg>
      );
    case 'cupped-hand':
      return (
        <svg {...common}>
          <path {...S} d="M6 18c2 9 7 14 14 14s12-5 14-14" />
          <path {...S} d="M9 18h22" />
          <circle cx="16" cy="15" r="2" fill="currentColor" opacity=".45" />
          <circle cx="21" cy="14" r="2" fill="currentColor" opacity=".45" />
          <circle cx="25" cy="16" r="2" fill="currentColor" opacity=".45" />
        </svg>
      );
    case 'thumb':
      return (
        <svg {...common}>
          <rect {...S} x="15" y="6" width="10" height="28" rx="5" />
          <path {...S} d="M17 12h6" />
        </svg>
      );
    case 'serving-spoon':
      return (
        <svg {...common}>
          <ellipse {...S} cx="14" cy="14" rx="8" ry="6" transform="rotate(-35 14 14)" />
          <path {...S} d="M19 19l14 14" />
        </svg>
      );
    case 'cup':
      return (
        <svg {...common}>
          <path {...S} d="M9 11h19l-2 22H11z" />
          <path {...S} d="M28 15h3a3 3 0 0 1 0 6h-4" />
        </svg>
      );
    case 'restaurant-small':
    case 'restaurant-medium':
    case 'restaurant-large': {
      const r = k === 'restaurant-small' ? 9 : k === 'restaurant-medium' ? 12.5 : 16;
      return (
        <svg {...common}>
          <circle {...S} cx="20" cy="20" r="17" opacity=".35" />
          <circle cx="20" cy="20" r={r} fill="currentColor" opacity=".22" />
          <circle {...S} cx="20" cy="20" r={r} />
        </svg>
      );
    }
  }
}
