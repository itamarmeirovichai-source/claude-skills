# Putting the VXO site live: owner steps

Written 2026-10-09. You do every step below yourself. No agent logs in, buys, deploys or sends anything for you. The whole job takes about 45 minutes, and the domain is the only cost (about $25–35 a year).

**Order:** 1. Set your email. 2. Register the domain. 3. Create the Cloudflare Pages project. 4. Get the films onto the site. 5. Attach the domain. 6. Connect the form. 7. Test. Do not send any lead a link until step 7 passes.

---

## 1. Set your reply email (2 minutes, before anything else)

The site shows "Rather email? Write to me directly: …" under every form. It stays hidden until there is a real address, and the agent was told not to invent one.

1. Open `site/src/data/site.json` in the repo.
2. Set `"email": "you@yourdomain"` to the inbox you will actually read every day. Once step 6 is done, an address on the new domain works best (for example `itamar@vxo.studio`).
3. Commit it (or ask an agent to make the one-line change).

While `email` is empty, `npm run build` prints `WARN site.json email is empty`.

## 2. Register the domain

**Availability, checked 2026-10-09 (public RDAP, no login):**

| Domain | Result |
|---|---|
| `vxo.studio` | **Not registered.** The `.studio` registry's RDAP says "Object not found", and DNS says it doesn't exist (NXDOMAIN). Three-letter names are often sold at a premium price, so check the price before you buy. |
| `vxostudio.com` | Not registered (Verisign RDAP 404). This is the fallback if `vxo.studio` is premium-priced or gets taken. |
| `vxo.com` | Taken since 1999. |

Steps (Cloudflare Registrar sells at cost and puts the DNS in the right place automatically):
1. Log in at **dash.cloudflare.com**. Use the same account that will host the site.
2. In the left menu, open **Domain Registration → Register Domains**.
3. Search for `vxo.studio`. If it's listed at the normal price (about $25–35 a year), click **Purchase**, fill in the contact form (WHOIS privacy is on by default) and pay.
   - If Cloudflare doesn't offer `.studio`, or shows a premium price you don't want to pay, register `vxostudio.com` there instead. Or buy `vxo.studio` at another registrar (Porkbun, Namecheap), then in Cloudflare go to **Add a domain**, enter it, choose the **Free** plan, and change the nameservers at that registrar to the two that Cloudflare shows you. Wait until Cloudflare says **Active**.
4. If you end up with a domain other than `vxo.studio`, update `domain` and `url` in `site/src/data/site.json`.

## 3. Create the Cloudflare Pages project `studio-site`

The site is Astro (static pages plus a few Pages Functions in `site/functions/`). There are two ways to deploy it. **Choose one. A Pages project can't switch between them later.**

### Option A (recommended): connect the repo, so every push rebuilds the site
1. dash.cloudflare.com → **Workers & Pages** → **Create** → **Pages** tab → **Connect to Git**. If the screen only offers Workers, look for the link "Looking to deploy Pages? Get started".
2. Connect GitHub and pick **this repository**. Grant access to this one repo only.
3. On **Set up builds and deployments**:
   - **Project name:** `studio-site` (your preview URL becomes `studio-site.pages.dev`)
   - **Production branch:** `research/ai-video-reels`. Switch it to `main` later if the site is merged there.
   - **Framework preset:** `Astro`
   - **Build command:** `npm run build`
   - **Build output directory:** `dist`
   - **Root directory (advanced):** `site`
   - **Environment variables (advanced) → Add:** `NODE_VERSION` = `22` (the site needs Node 22.12 or newer)
4. Click **Save and Deploy**. The first build takes 2–3 minutes and must end in **Success**.

**Important: the films are not in git.** `site/public/media/` is git-ignored (102 MB of video), so this build has **no films, posters or Otto/Vee clips** until you finish step 4. The pages still load, but the tiles are empty.

### Option B: direct upload from the machine that has the media
Use this if you'd rather not deal with R2 for media. The repo already has a one-command deploy, `site/scripts/deploy-pages.sh`. It builds the site and uploads it **with** `public/media`. It needs `CLOUDFLARE_API_TOKEN` (permission "Cloudflare Pages: Edit") and `CLOUDFLARE_ACCOUNT_ID` set as **environment secrets in the Claude Code environment settings**. Never paste them into chat or into a file. After that, an agent can run `bash scripts/deploy-pages.sh`, but only when you ask it to. Re-run it after every change. If you choose B, skip step 4.

## 4. Get the films onto the site (Option A only)

The remastered films (all −14 LUFS ±1, true peak ≤ −1 dBTP, measured on the encoded files), the Red Light making-of stills and the character clips currently exist **only in the agent's working copy** (`site/public/media/`). They have to be uploaded once to a private R2 bucket. The site then serves them from its own domain through `site/functions/media/[[path]].ts`, so the security policy (CSP) needs no change.

1. dash.cloudflare.com → **R2 Object Storage** → **Create bucket** → name it `studio-media`, location Automatic → **Create**. Leave public access **off**.
2. Create an API token: **My Profile → API Tokens → Create Token → Custom token**. Permissions: *Account · Workers R2 Storage · Edit* and *Account · Cloudflare Pages · Edit*. Restrict it to your account, then copy it.
3. Add `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` as **secrets in the Claude Code environment settings** (not in chat). The account ID is on the right side of the Cloudflare dashboard home page.
4. Ask the agent: "run `bash site/scripts/upload-media-r2.sh studio-media`". It uploads every file under `media/...`.
5. Pages project `studio-site` → **Settings → Bindings → Add → R2 bucket**. Variable name: `MEDIA`. Bucket: `studio-media`. Save.
6. **Deployments → … → Retry deployment.** Bindings only take effect on a new deployment.
7. Open `https://studio-site.pages.dev/work/red-light`. The film must play, with sound, and you must be able to drag the playhead.

Note: every `/media/*` request runs the small media Function. That fits easily in the free plan (100,000 requests a day).

## 5. Attach the domain

1. Pages project `studio-site` → **Custom domains** → **Set up a custom domain** → `vxo.studio` → **Continue** → **Activate domain**. Cloudflare adds the DNS record for you, because the domain is on the same account.
2. Repeat for `www.vxo.studio`. Then, under the domain's **Rules → Redirect Rules**, choose **Create rule → "Redirect from WWW to root"** (template) → Deploy.
3. Wait for **Active** and an SSL certificate (usually under 15 minutes). Then open `https://vxo.studio`.

## 6. Connect the form (so no lead is lost)

Right now the form tells a visitor "done" but keeps nothing. With no `UPLOADS` bucket and no Resend key, the API answers `stored:false, alerted:false`. The site now detects this and shows a red notice on the thanks page ("Our form isn't connected to the studio inbox yet…"), plus your email once step 1 is done. Do both parts below. R2 keeps the lead, and Resend tells you it arrived.

### 6a. Store every lead in R2 (binding `UPLOADS`)
1. **R2 → Create bucket** → `studio-uploads` (private).
2. Open the bucket → **Settings → Object lifecycle rules → Add rule**: delete objects after **90 days**. The privacy page promises this.
3. Pages project → **Settings → Bindings → Add → R2 bucket**. Variable name: `UPLOADS`. Bucket: `studio-uploads`.

### 6b. Get an email for every lead (Resend)
1. Sign up at **resend.com** → **Domains → Add domain** → `vxo.studio`. Resend shows 3–4 DNS records (SPF/DKIM). In Cloudflare go to **DNS → Records → Add record** and copy each one exactly, leaving the proxy **off** (grey cloud). Back in Resend, click **Verify**.
2. In Resend: **API Keys → Create** (permission: Sending access, domain vxo.studio). Copy the key.
3. Pages project → **Settings → Variables and Secrets → Add** (Production):
   - `RESEND_API_KEY`: the key (type **Secret**)
   - `MAIL_FROM`: `VXO <frames@vxo.studio>`
   - `NOTIFY_TO`: your inbox (the same address as in step 1)
   - `LEAD_SIGNING_SECRET`: any random string of 32 or more characters (type **Secret**). Without it, photo uploads can fail between servers.
4. **Deployments → Retry deployment.**

Optional (spam protection): create a Turnstile widget for `vxo.studio`. Put its *site key* in `site.json → turnstileSiteKey` and its *secret* in the Pages secret `TURNSTILE_SECRET`.

## 7. Test before you send anyone the link
1. Open `https://vxo.studio/?utm_content=product`. The headline should read "Your product, as the punchline of an ad people watch to the end." Red Light is the gold-bordered card in the ring.
2. Fill in the home form with **your own** email and a product page URL, and submit.
3. Pass means all four of these:
   - the thanks page shows **no** red "isn't connected" notice;
   - an email "Frames request: …" reaches `NOTIFY_TO`;
   - the auto-reply reaches your test address;
   - R2 `studio-uploads` contains `leads/<id>/lead.json`.
4. Play Red Light on a phone, with sound.
5. Only then: links can go into the approved messages, which you send yourself.

## Still open (owner decisions, from doc 65 §7)
- A real photo, your full name, one true line of background, and the postal address for CAN-SPAM (`site.json → founderLine`, `address`; the About page). The site still has no face.
- The new founding-five trade (an extra hook variant + a QC sheet, in exchange for 30-day Ads Manager numbers). Not applied; the current line is unchanged.
- The two optional promises (the test take matches the frames or we redo it; the hook re-cut). Not applied.
- Red Light's known limits are stated on its page (a second stopwatch on Vee's lapel, the cruiser stopping beside the car rather than behind it, 480p chase detail). Fixing them needs paid renders: your call.
