# Store build (live objects on the Shopify store, written by the program through the Admin API)

Store: rmynwr-k1.myshopify.com (Basic plan, USD, US). Opened 2026-11-12 by the operator; ownership to be transferred to the mother before payments go live (Shopify ToS 18+, S-01). Storefront is password-protected until launch (M0 step 6 gate).

Access: custom app "store-builder" (Dev Dashboard, client-credentials grant, 24-hour tokens; scopes limited to themes, products, content, pages, navigation, read orders, locales). The token lives in the session environment's network secrets, never in this repo. The client secret was rotated once after an accidental paste.

## What exists on the store (2026-11-12)
| object | id | state |
|---|---|---|
| Theme "Pawnook v1 (Dawn base)" | gid://shopify/OnlineStoreTheme/189982408995 | **published (MAIN)**; Dawn + the custom files in `theme/` |
| Theme "Horizon" (Shopify default) | gid://shopify/OnlineStoreTheme/189980934435 | unpublished, kept as fallback |
| Product "Raised Ceramic Cat Bowl Stand — Slow-Feed Bowl" (P-0002, ceramic variant) | gid://shopify/Product/10442912104739, variant 56046220640547 | **DRAFT**, $49.90, copy with [brackets]; not published until the brackets are filled from the Eprolo spec and the sample |
| Page "Shipping & Returns" | gid://shopify/Page/165163401507 | published; text = `runbooks/store-policies.md` |
| Page "About" | gid://shopify/Page/165163434275 | published; new-store honesty text |
| Page "Contact" (Shopify default) | gid://shopify/Page/165161959715 | published |
| Main menu | gid://shopify/Menu/317957013795 | Home · Shop · Shipping & Returns · About · Contact |
| Footer menu | gid://shopify/Menu/317957046563 | Shipping & Returns · About · Contact · Your Privacy Choices |

## Theme files in `theme/` (uploaded with themeFilesUpsert; everything else is stock Dawn)
- `assets/pawnook.css`: styles for the custom sections only.
- `sections/pn-proof-rows.liquid`: "What we fixed": complaint (customer's words) → fix (proven on the sample) → where the proof is. The page's core block (rules LP5, LP6).
- `sections/pn-delivery-bar.liquid`: shipping included · US warehouse · returns · payment line (LP1).
- `sections/pn-note.liquid`: the large-breed caution (S-205) and any honesty line.
- `sections/pn-specs.liquid`: spec list; values only from the spec or the sample.
- `sections/pn-steps.liquid`: how ordering works (three steps).
- `sections/pn-honest-line.liquid`: new-store line (no fake trust, S-36).
- `sections/header-group.json`, `sections/footer-group.json`: announcement line, no country/language selectors, newsletter off, legal footer placeholders.
- `templates/product.json`: delivery bar → product → proof rows → specs → large-breed note → steps → honest line.
- `templates/index.json`: hero → delivery bar → featured collection → "how we choose what to sell" → steps → honest line.
- `config/settings_data.json`: palette (paper #FBF8F3, ink #1F1A17, sage #2F4F3A, sand #EFE8DC), fonts Lora / Work Sans, animations off, cart as page, no vendor display.

## Not done by the program (needs the operator, the mother, or data)
- Store name is provisional ("Pawnook": no trademark hit on 2026-11-12 search; "Hearthpaw" rejected, pending TM). The mother approves the name; USPTO check in a browser before buying the domain.
- Logo, hero image, product photos: from the sample (no stock or AI images on product pages; D1).
- Brackets in the product, product template and footer: filled from the Eprolo product page and the sample.
- Legal policies (refund/privacy/terms in Settings → Policies): the app scope does not cover them; the mother pastes `runbooks/store-policies.md` and Shopify's generated privacy/terms there.
- Shopify Payments, Shopify Tax (Florida), Meta app + CAPI, reviews app: owner-level steps (M0).
- Storefront password stays on until the launch gate in `runbooks/store-build.md` §9 passes.

## How to update
Edit files in `theme/`, then upload with the GraphQL `themeFilesUpsert` mutation to the theme id above (the session helper is `gql.sh` in the scratchpad; a fresh 24-hour token is needed each day: the operator runs the PowerShell command in the work log and pastes the `shpat_` value into the secure credential form).
