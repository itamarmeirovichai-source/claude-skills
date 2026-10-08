import raw from '../data/site.json';
import pricingRaw from '../data/pricing.json';

export const site = raw;
export type Tier = (typeof pricingRaw.tiers)[number] & { ribbon?: string; credit?: string; cta?: { label: string; href: string } };
export const pricing = pricingRaw as typeof pricingRaw & { tiers: Tier[] };

/** Replace {{TOKENS}} with site.json values; an empty token renders nothing. */
export function t(text: string): string {
  const map: Record<string, string> = {
    STUDIO: site.studio,
    MASCOT: site.mascot,
    PRODUCER: site.producer,
    ADDRESS: site.address,
    EMAIL: site.email,
    DOMAIN: site.domain,
    FOUNDER: site.founder,
  };
  return text.replace(/\{\{(\w+)\}\}/g, (_, k: string) => map[k] ?? '');
}

export const money = (n: number): string => `$${n.toLocaleString('en-US')}`;

/** "Book a 15-min call" goes to the booking link when one exists, else to the form with the preference set. */
export const callHref = (): string => site.bookingUrl || '/frames?next=call';

export type Bfcm = typeof raw.bfcm;
export const bfcm: Bfcm = raw.bfcm;
/** The BFCM offer is live until the end of its booking day (UTC-12, so no time zone closes it early). */
export const bfcmOpen = (now: Date = new Date()): boolean => bfcm.show && now.getTime() < Date.parse(`${bfcm.bookBy}T23:59:59-12:00`);

/** Tier CTA href: "call" means the booking link (or the form with the call preference). */
export const tierHref = (href: string): string => (href === 'call' ? callHref() : href);
