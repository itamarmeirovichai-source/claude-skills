CHATGPT MESSAGE 1 of 8 — THE EXAMPLE SITE. Apply the research and the capabilities I sent you. You are building an award-level PROPOSAL website for Smash House Burgers (Boca Raton) to win them as a client. Use their brand kit exactly — colors, fonts, logo, Kong. Follow this spec exactly. Do not simplify effects, swap libraries, skip fallbacks, or leave placeholder assets. Smoothness is a hard requirement: 60fps on a mid-range phone. The 8-beat burger sequence plays image-sequence frames rendered in Blender, per the asset contract — until they exist, use the real-time fallback. Build in the order given. Generate the missing images from the asset plan yourself where you can, photoreal, matched to their brand, respecting the kosher rules. Add a small "Concept proposal for Smash House Burgers" footer tag and noindex. Wait until you have all 8 parts, then start. After each step, state what you built and what's next.

# 1. THE CLIENT — VERIFIED FACTS ONLY

**Rule that overrides everything else in this spec: never invent a price, a review, an award, a promotion or a quote.** Anything below marked `[TO CONFIRM]` must be verified against the live site (smashhouseburgers.com) before anything is shown to the owner. If you cannot verify it, leave the `[TO CONFIRM]` tag visible in the build so it cannot ship by accident.

## Business
| Field | Value |
|---|---|
| Name | Smash House Burgers |
| Positioning | "The First Glatt Kosher Smashed Burger Restaurant in America" |
| Founded | 2022, North Miami Beach, FL |
| Footprint | ~10 locations across NY, NJ, FL, CA `[TO CONFIRM exact count and list]` |
| Mascot | "Kong" — a gorilla in sunglasses |
| Voice | Casual, loud, playful. Example line from their material: "EVERYBODY'S A WINNER!" |
| Kashrut | Glatt kosher. **All cheese is plant-based — no dairy at any location.** |
| Current stack | WordPress + Elementor |

## The Boca Raton location
| Field | Value |
|---|---|
| Address | 21065 Powerline Rd, Suite C15, Boca Raton, FL 33433 (The Shops at Boca Grove) |
| Phone | 561-367-3401 |
| Location page | https://www.smashhouseburgers.com/locations/florida/boca-raton/ |
| Sun–Thu | 11:00 AM – 11:00 PM |
| Friday | **CLOSED** |
| Saturday | Opens **one hour after Shabbat ends**, until 12:00 AM |
| Online ordering | Toast — https://order.toasttab.com/online/smashhouseboca |
| App | iOS + Android, with loyalty `[TO CONFIRM store URLs]` |
| Also offered | Gift cards, catering / events |
| Kosher certification | `[TO CONFIRM the certifying agency and its logo usage permission]` |

## Menu items confirmed by name
Loaded Smashed (double smashed burger, plant-based cheese, caramelized onion, beef bacon) · Double Smashed · Dirty Fries (pulled brisket + chef sauce) · Blooming Onion · Popcorn Chicken · Philly Cheese Sando · The Crispity Crunch · kids menu · desserts.
`[TO CONFIRM]` every price, every full description, allergen data, the complete item list, and the exact Loaded Smashed build order.

## Kosher content rules — enforce on every image, render and copy line
1. Never show meat and dairy together. All cheese rendered or generated must read as **plant-based**: a matte melt, slightly less stringy than dairy, no glossy dairy sheen.
2. No pork. "Beef bacon" is deep red and thick-cut, with **no white marbled fat strips** — that silhouette reads as pork and must never appear.
3. No butter sheen, no cream sauces, no milkshake-with-meat compositions.
4. Do not depict the restaurant open on Friday or during Shabbat.

---

# 3. PAGES
| Page | Route | Purpose |
|---|---|---|
| Home | `/` | The full show. The signature sequence, every show-stopper, ends on Order. |
| Menu | `/menu` | The complete menu with photos, tags and filters. The ticket rail. |
| Catering | `/catering` | The party planner, the inquiry form, event proof. |
| Boca Raton | `/locations/florida/boca-raton` | Hours, live open status, map, directions, call, order. Local SEO target. |
| 404 | `/404` | "Kong ate this page." |

Every page: shared header with a sticky Order button, the live open/closed status, and the footer concept tag.

---

# 4. FOUNDATIONS — each with its exact tool

| Requirement | How to build it |
|---|---|
| Full menu with photos + tags | Sanity CMS: `Category → Item → Modifier` documents with `name`, `description`, `price`, `photo`, `tags[]` (`beef`, `chicken`, `plant-cheese`, `spicy`, `kids`, `dessert`), `available` boolean. Never a PDF, never an image of text. |
| Giant sticky "Order Now" | Fixed bottom bar on mobile, header pill on desktop, `#E51144` on `#13110C`. Links to `https://order.toasttab.com/online/smashhouseboca`, `target="_blank" rel="noopener"`. Navigation fires first, animation second — always. |
| App download + loyalty | Platform-detected buttons + a QR for desktop, with UTM params. `[TO CONFIRM store URLs]` |
| Gift cards | Designed card component linking to their gift card page `[TO CONFIRM URL]`. |
| Catering / events | Dedicated page + a form posting to a Next.js route handler → Resend email, Turnstile + honeypot + a 2-second time trap. |
| Location + map + directions | Mapbox **Static Images API** rendered as an `<img>` that swaps to interactive Mapbox GL JS on click. Directions button uses `https://www.google.com/maps/dir/?api=1&destination=21065+Powerline+Rd+Suite+C15+Boca+Raton+FL+33433`. |
| Click-to-call | `<a href="tel:+15613673401">561-367-3401</a>` — the number is the visible text. |
| Kosher certification badge | Header + footer + every menu page. `[TO CONFIRM agency + permission to reproduce the mark]` — until confirmed, render the text "Glatt Kosher" in the brand lockup, never a fabricated agency logo. |
| **Live "open now" status** | Computed **server-side** in a Next.js Server Component. Base hours: Sun–Thu 11:00–23:00, Fri closed, Sat opens (Shabbat end + 60 min) until 00:00. Shabbat end and Jewish holidays come from the **Hebcal REST API** using Boca Raton's coordinates (lat 26.3683, lon -80.1289, tzid `America/New_York`) — request Shabbat times and the holiday calendar, cache for 6 hours with `revalidate`, and derive: `isOpen`, `opensAt`, `closesAt`, `isShabbat`, `isHoliday`, `holidayName`. Render the resulting sentence into the HTML so it is correct with JavaScript disabled, and pass the booleans to the neon sign and to Kong's Rive state machine. Never compute this in the browser — a visitor in another timezone would see the wrong answer. |
| Schema | `Restaurant` with `servesCuisine`, `priceRange` `[TO CONFIRM]`, `hasMenu`, `openingHoursSpecification` (including the Friday closure and the Saturday variable open), `acceptsReservations`, `geo`, `telephone`. Plus `Menu` / `MenuSection` / `MenuItem` per item, `LocalBusiness`, `FAQPage`. `AggregateRating` **only** if real ratings are sourced. |
| Google Business Profile | Deliverable in the pitch, not in the code: hours, photos, menu link, order link, attributes. |
| Mobile-first | Design and build the 390px view first. Every layout decision is made there and then expanded. |
| Accessibility (ADA / WCAG 2.2 AA) | 4.5:1 contrast on body text, `:focus-visible` rings at 2px offset, a complete keyboard path, skip link, 24×24px minimum targets, captions on video, `prefers-reduced-motion` branches on every animation, an accessibility statement page. |
| Images | AVIF + WebP via `<picture>`, `srcset` at 400/800/1200/1600/2400, `sizes` set accurately, `aspect-ratio` on every container, `fetchpriority="high"` + preload on the LCP image, everything else `loading="lazy"`. |
| SEO | Unique titles/descriptions, per-page OG images generated with `@vercel/og`, sitemap, clean URLs. **This build ships `noindex, nofollow` + `robots.txt` disallow** until the client approves. |
| Analytics | GA4 + Microsoft Clarity. Events: `order_click`, `call_click`, `directions_click`, `app_download`, `catering_submit`, `giftcard_click`, `menu_item_open`. |
| Legal | Privacy, terms, accessibility statement. Cookie consent that actually gates the analytics scripts. |
| Infra | Vercel, Cloudflare DNS, Resend for transactional mail with SPF/DKIM/DMARC, Sentry with source maps, a `noindex` staging branch. |

---

# 5. BRAND & CONCEPT

## Brand kit — use exactly. No new hues; tints and shades are fine.
| Token | Hex | Use |
|---|---|---|
| Smash Red | `#E51144` | Primary. CTAs, the neon sign, the impact flash. |
| Deep Red | `#C20F3A` | Pressed states, gradients. |
| Deeper Red | `#BA0C36` | Shadow side of red surfaces. |
| Near-Black | `#13110C` | Page ground. Everything sits on this. |
| Yellow | `#FEEB13` | Accents, badges, "PERFECT CRUST", highlight type on dark. |
| Blue | `#0083B0` | Secondary accent. |
| Deep Blue | `#007198` | Blue text on light backgrounds. |
| White | `#FFFFFF` | Body text on dark. |
| Brown | `#401C10` | Griddle, wood, ticket paper shadow. |

**Verified contrast — obey these or the site fails ADA:**
- Smash Red `#E51144` on white = **4.67:1** ✓ body text allowed.
- Smash Red on Near-Black = **4.04:1** ✗ body text. Large text only (≥24px, or ≥18.66px bold). For body copy on the dark ground use white or yellow.
- Yellow `#FEEB13` on Near-Black = **15.4:1** ✓ excellent.
- Yellow on white = **1.23:1** ✗ never. Yellow text never touches a white background.
- Blue `#0083B0` on white = **4.31:1** ✗ body text — use Deep Blue `#007198` on white = **5.50:1** ✓.

## Fonts
- **Display:** "Smash Dollars" (their custom face). If you cannot license or embed it, substitute **Londrina Solid** (Google Fonts, free, uppercase display) and **state the substitution visibly in the handover notes** — never silently swap a brand face.
- **Display secondary / uppercase:** Londrina Solid.
- **Body / UI:** Poppins (400, 500, 600, 700).
- Load with `font-display: swap`, `<link rel="preload" as="font" crossorigin>`, and a `size-adjust` fallback stack so there is no layout shift.

## Assets they already own — use these first, always
- Logo: `https://cdn.smashhouseburgers.com/wp-content/uploads/2024/07/29163847/Logo_new2.webp`
- "Kong Arm" cut-out: `https://cdn.smashhouseburgers.com/wp-content/uploads/2026/07/07175624/kong_part.webp`
- Food photos and illustrations live on `cdn.smashhouseburgers.com` and are **lazy-loaded on their current site** — read the rendered page or the `data-lazy-src` attributes to collect them, not the raw HTML.

## Three concept directions
| # | Direction | One line |
|---|---|---|
| A | **THE SMASH** | Every moment on the site is an impact — things are flung, flattened, slammed and recoil; force is the site's grammar. |
| B | **THE GRIDDLE** | The whole page is a hot flat-top: heat haze, grease, sizzle and grill marks follow the cursor everywhere. |
| C | **KONG'S HOUSE** | Kong personally walks you through his restaurant, room by room, reacting to everything. |

## Chosen: **A — THE SMASH**
**Why.** It is the brand's name, the product's cooking method, and the only one of the three that becomes a *motion grammar* rather than a texture. B is one effect stretched across a site — it would run out by the second section and it fights legibility. C makes the mascot the product; the burger is the product, and it would force a slow linear tour that kills the order flow. A gives every component the same physical vocabulary: **anticipation → impact → squash → recoil → settle.** A button press, a page transition, a menu card, a stamp, a patty on a griddle and the hero sequence all obey the same three-beat rhythm. That is what makes a site feel like one world instead of a collection of effects — and it is a rhythm a visitor can feel without ever being told about it.

**The one-sentence idea to repeat in every review:** *Everything on this site gets smashed — and comes back better.*
