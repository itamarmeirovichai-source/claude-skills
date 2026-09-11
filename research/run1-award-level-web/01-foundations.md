CHATGPT MESSAGE 1 of 7 — RESEARCH RESULTS. These are the results of deep research into how award-level interactive websites (Awwwards / FWA level) are built. Study them carefully — this is your knowledge base from now on. Don't build anything yet. Reply only: "Got it — send the next part."

# A. FOUNDATIONS CATALOG
Format: feature | best way to do it | must-have for a restaurant site?

## F1 — IMAGES
| Feature | Best way | Restaurant must-have |
|---|---|---|
| Responsive images | `<img srcset>` with w-descriptors at 400/800/1200/1600/2400 + accurate `sizes`; `<picture>` only for true art direction | Y |
| Modern formats | AVIF first → WebP → JPEG inside `<picture>`; AVIF is ~30–50% smaller than WebP at equal perceived quality | Y |
| Compression targets | Hero ≤200KB, content ≤120KB, thumbnail ≤40KB. sharp/Squoosh, AVIF q55–65, WebP q75 | Y |
| Lazy loading | `loading="lazy"` on everything below the fold; NEVER on the LCP image | Y |
| Hero priority | `fetchpriority="high"` + `<link rel="preload" as="image" imagesrcset imagesizes>`; no lazy, no JS gate | Y |
| LQIP / blur-up | 20–32px base64 or ThumbHash/BlurHash, CSS `filter: blur(20px)`, cross-fade on `img.decode()` | Y |
| Zero layout shift | `width`+`height` attributes or `aspect-ratio` on every image box; reserve space before load | Y |
| Art direction | `<picture><source media="(max-width:640px)" srcset="crop-portrait.avif">` — different crop, not just smaller | Y |
| Image CDN | Cloudflare Images, imgix or Cloudinary with `f_auto,q_auto`; origin stays one master file | Y |
| Alt text | Describe function/dish; `alt=""` for decorative; never "image1" | Y |
| SVG | Inline critical icons (styleable + animatable), sprite for the rest, SVGO in build | Y |
| Gallery / lightbox | GSAP Flip FLIP-expand from the thumbnail, not a generic modal; keyboard + swipe + Esc | Y |
| Pinch/zoom detail | `object-fit: cover` + transform scale on a 2× source, pointer-driven, capped at 3× | N |
| CSS background images | `image-set()` with AVIF/WebP variants; never a raw 4MB JPEG in CSS | Y |
| Favicon / app icons | SVG favicon + 180px apple-touch-icon + manifest 192/512 maskable PNG | Y |
| OG / share images | 1200×630 generated per page (`@vercel/og` / satori), real dish photo + logo | Y |

## F2 — CREATING ASSETS (catalog; full toolkit in section C)
| Asset | Best source |
|---|---|
| Food photography | Real shoot: phone in RAW/ProRAW, 1 big soft key at 45–90° back-side, black+white bounce, 50–85mm equivalent, f/2.8–5.6, tripod, focus stack |
| Photogrammetry / scan | Polycam, Scaniverse (free unlimited Classic mode), KIRI Engine, RealityScan — LiDAR or photo mode, 80–150 photos, matte spray or polarizer for shine |
| AI stills | Nano Banana Pro (top photoreal + in-image text), FLUX.2 Pro (physically plausible product light), Midjourney v7 (taste/mood), Adobe Firefly (cleanest commercial indemnity) |
| Style/character consistency | Lock one reference image + a written "style contract" (lens, light, palette hex, surface, grain) reused verbatim in every prompt |
| Upscale | Topaz Gigapixel / Magnific for print-grade; ESRGAN via Real-ESRGAN for batch |
| Background removal | `image_remove_background`-class tools, Photoroom, or `rembg` locally; always re-check edge halos on dark backgrounds |
| AI video | Veo 3.x (realism + native audio, commercial rights on paid tiers), Kling 3.0 (motion, 4K), Runway (ownership on paid) — OpenAI's Sora consumer app was retired in 2026 |
| AI 3D | Meshy, Hunyuan3D, Rodin — fallback only; topology and UVs are unusable for hero close-ups |
| Music / SFX | Real recording first; then licensed libraries; AI (Suno/ElevenLabs SFX) only with a commercial tier |
| Voice | ElevenLabs with a paid commercial tier, or a real VO artist |
| Stock | Unsplash/Pexels (free, but generic — never for hero), Freesound (check per-file CC terms) |
| Rights rule | Log per asset: source, tool, plan tier, date, license text. No entry = don't ship it |

## F3 — VIDEO
| Feature | Best way | Must-have |
|---|---|---|
| Hero/background video | `muted autoplay loop playsinline preload="metadata"` + `poster`; ≤6s, ≤2MB, no audio track at all | Y |
| Formats | AV1/WebM first + H.264 MP4 fallback; HEVC only as an extra source for Safari | Y |
| Poster frame | A real frame exported as AVIF, preloaded — the video must never show black | Y |
| Adaptive streaming | Mux, Cloudflare Stream or Bunny (HLS) for anything >20s; hls.js where native HLS is absent | N |
| YouTube/Vimeo | Facade (`lite-youtube-embed`): static thumb + play button, iframe injected on click; saves ~1MB+ | Y |
| Custom controls | Vidstack or a plain `<video>` + your own UI; never ship default chrome on a designed site | N |
| Captions | WebVTT `<track kind="captions">` on every spoken-word video — legal + silent autoplay | Y |
| Vertical / Reels | 9:16 sources, `object-fit: cover`, IntersectionObserver play/pause | Y |
| Lazy video | Don't put `<video>` in the DOM until it's within ~1 viewport; swap `poster`→`src` | Y |
| Data saving | Respect `navigator.connection.saveData` and `prefers-reduced-motion` → serve the poster only | Y |

## F4 — OTHER MEDIA & EMBEDS
| Feature | Best way | Must-have |
|---|---|---|
| Audio player | Howler.js (sprite-based, unlocks iOS on first gesture); never autoplay | N |
| PDFs / downloads | Direct link with size+format in the label ("Catering menu · PDF · 1.2MB") | Y |
| Instagram / TikTok | Server-fetch the feed via an API/scraper into your own image grid; official embeds are heavy and break design | Y |
| Maps | Static map image (Mapbox Static API) that swaps to interactive on click; never a blocking iframe | Y |
| 3D / AR files | `<model-viewer>` with GLB + USDZ pair for AR Quick Look on iOS | N |
| Calendars | Generated `.ics` links + Google Calendar template URL | N |

## F5 — CONTENT & PAGES
Home · About/story · Menu (or services/products) · Pricing · Portfolio/case studies · Testimonials & reviews · FAQ (with FAQPage schema) · Blog/news · Team · Contact · Privacy · Terms · Accessibility statement · Designed 404 · Thank-you pages (one per conversion, for pixel firing). For a restaurant: Home, Menu, Locations (one page per location — local SEO), Catering, Order, About, 404 are non-negotiable.

## F6 — CONVERSION & CONTACT
| Feature | Best way | Must-have |
|---|---|---|
| Primary CTA | One verb, sticky on mobile, visible within the first viewport, contrast ≥4.5:1 | Y |
| Forms | Native `<form>` + progressive enhancement; inline validation on blur not on keystroke; `autocomplete` + `inputmode` on every field | Y |
| Spam protection | Cloudflare Turnstile (invisible) + a honeypot field + a 2s time-trap. Never reCAPTCHA v2 checkboxes | Y |
| Click-to-call | `<a href="tel:+15613673401">` with the number as visible text | Y |
| WhatsApp | `https://wa.me/<number>?text=<prefilled>` | N (US) |
| Booking | Cal.com (self-hostable, themeable) > Calendly | N |
| Chat / AI assistant | Only if staffed; otherwise a menu-aware FAQ bot. Lazy-load after idle | N |
| Newsletter | Double opt-in, one field, Resend/Klaviyo; success state inline, no page reload | Y |
| Lead magnet | Catering pricing sheet, party-planning guide | Y |
| Popups | Exit-intent on desktop only, after 2 pageviews, never on mobile, never over a CTA | N |
| Calculators | Guest-count → platters estimator; no invented prices, output = "we'll quote X" | Y |

## F7 — COMMERCE
| Feature | Best way | Must-have |
|---|---|---|
| Product/dish page | Real photo, allergens, tags (spicy/vegan-cheese/kids), price from CMS, Product+Offer schema | Y |
| Cart & checkout | Don't rebuild it for a restaurant — hand off to the existing ordering platform | Y |
| Payments | Stripe (Payment Element, Apple/Google Pay) for anything custom; Israel: Tranzila, Cardcom, Grow, PayPlus | N |
| Restaurant ordering | Toast, Olo, ChowNow — deep-link to the live menu; open in a new tab instantly, never behind an animation | Y |
| Gift cards | Platform-hosted link; render as a designed card, link out | Y |
| Loyalty | App deep link + QR; `itms-apps://` / Play Store URLs with UTM | Y |
| Coupons / promos | CMS-driven banner with start/end datetimes, auto-hides | Y |
| Order emails | Transactional via Resend/Postmark with SPF+DKIM+DMARC | Y |

## F8 — CMS & ADMIN
| Feature | Best way | Must-have |
|---|---|---|
| Editable content | Sanity (best real-time + structured content), Payload (self-host, Postgres), Webflow CMS (client-friendly), headless WordPress only if they already live there | Y |
| Menu modelling | `Category → Item → Modifier` documents with price, photo, tags, availability window — never a rich-text blob | Y |
| Media library | CMS-native with on-the-fly transforms (Sanity's image pipeline, Cloudinary) | Y |
| Roles | Owner / editor / viewer; a manager can toggle "86'd" on an item without touching layout | Y |
| Drafts & preview | Draft mode with a live preview URL; scheduled publish for promos | Y |

## F9 — USER FEATURES
Accounts via magic link (Resend + Auth.js) or Google; profile; file upload with client-side crop (`react-easy-crop`) + direct-to-storage signed URLs; favorites (localStorage first, account second); reviews pulled from Google rather than self-hosted; site search (client-side Fuse.js under ~2k items, Algolia/Typesense above); filters/sorting with FLIP animation and URL state; notifications via Web Push only after a value-first prompt; on-site AI only where it answers a real question ("what's dairy-free?").

## F10 — LANGUAGE & ACCESSIBILITY
| Feature | Best way | Must-have |
|---|---|---|
| Multilingual | Route-based `/en/`, `/he/` with `hreflang` + `lang` attributes; content per locale in the CMS, not machine-translated at runtime | N |
| RTL | `dir="rtl"` + CSS logical properties (`margin-inline-start`, `inset-inline`) everywhere — never `left/right` | N (US) |
| WCAG 2.2 AA | 4.5:1 text contrast (3:1 for ≥24px), visible focus ring (`:focus-visible`, 2px offset), full keyboard path, skip link, ARIA only where semantics fail, 24×24px minimum target | Y |
| Motion | `prefers-reduced-motion: reduce` honoured by every animation, including scroll scrub | Y |
| Legal | US: ADA/Section 508 exposure — WCAG 2.2 AA is the defensible standard. Israel: IS 5568 + a published accessibility statement and a named coordinator | Y |
| Testing | axe DevTools + real keyboard pass + VoiceOver pass on the 3 key flows | Y |

## F11 — SEO & SHARING
| Feature | Best way | Must-have |
|---|---|---|
| Titles / meta | Unique per page, ≤60 / ≤155 chars, primary keyword + city | Y |
| OG / Twitter | `og:title/description/image/url`, `twitter:card=summary_large_image` | Y |
| Sitemap / robots | Auto-generated `sitemap.xml`, `robots.txt`; a concept/demo site must be `noindex, nofollow` + robots disallow | Y |
| Schema.org | `Restaurant` (with `servesCuisine`, `hasMenu`, `openingHoursSpecification`, `acceptsReservations`), `Menu`/`MenuSection`/`MenuItem`, `LocalBusiness`, `FAQPage`, `AggregateRating` only if real | Y |
| URLs | `/locations/florida/boca-raton/` — readable, stable, lowercase, no params | Y |
| Headings | One `<h1>`, no skipped levels, real DOM text behind every WebGL scene | Y |
| Google Business Profile | Hours, photos, menu link, order link, attributes; the single biggest local lever | Y |
| Local SEO | NAP consistency, one page per location, embedded map, local schema, reviews | Y |
| AI answer engines | Clean semantic HTML + schema + an FAQ block phrased as real questions; ensure content is in the server-rendered HTML, not client-only | Y |

## F12 — ANALYTICS & TRACKING
GA4 (or Plausible for privacy-first) · Meta Pixel + Conversions API (server-side, dedupe with `event_id`) · Microsoft Clarity (free heatmaps + session recordings) · custom conversion events: `order_click`, `call_click`, `directions_click`, `app_download`, `catering_submit` · A/B testing only with real traffic volume · UTM discipline on every outbound and ad link.

## F13 — TRUST, LEGAL & SECURITY
HTTPS + HSTS · cookie consent that actually gates scripts (GDPR/CCPA) · privacy policy + terms · CSP, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy` · Turnstile on forms · daily backups of CMS + media · uptime monitoring (Better Stack / Cronitor) with SMS alert.

## F14 — HOSTING & INFRA
Domain + DNS on Cloudflare · hosting on Vercel / Netlify / Cloudflare Pages · CDN with long `Cache-Control` + immutable hashed filenames · Google Workspace for business email · Resend for transactional mail · a staging branch with its own URL and `noindex` · auto-deploy on merge · Sentry for errors with source maps.

## F15 — UX BASICS
Mobile-first (design the 390px view first) · sticky header that hides on scroll-down and returns on scroll-up · breadcrumbs on deep pages · back-to-top after 2 viewports · dark mode only if it's designed, not auto-inverted · skeletons that match final layout exactly (no spinners) · designed empty + error states · PWA (installable, offline menu page) · print stylesheet for the menu · a **live open/closed status** computed from real data — for a kosher business this must respect Friday closure, Saturday reopening one hour after Shabbat ends, and Jewish holidays, using real sunset times (Hebcal's Shabbat/holiday JSON API with the venue's lat/long, computed server-side and revalidated hourly so it also works with JS off).

### Foundations gaps most sites miss (add these to every build)
1. The LCP image is lazy-loaded or JS-gated — instant 3s LCP penalty.
2. No `aspect-ratio` → CLS on every image.
3. Forms have no server-side validation or no success state.
4. No `Restaurant`/`Menu` schema → no rich results, no AI-answer visibility.
5. Hours are hard-coded text that goes stale the first holiday.
6. Menu lives in an image or PDF — invisible to search and screen readers.
7. No transactional email auth (SPF/DKIM/DMARC) → contact forms land in spam.
8. Fonts load without `font-display: swap` + preload → invisible text then a shift.
9. No analytics events on the money clicks, so nobody can prove ROI.
10. Staging is indexed, duplicating the live site.
