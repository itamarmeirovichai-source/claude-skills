# 52 — Niche deep-dive: pet products, baby/kids products, outdoor and travel gear

Research brief, 2026-10-09. No generation money was spent. Nobody was contacted.

**What this adds.** Doc `02-niches.md` gives these three niches one line each (pets: "the pet's real reaction", AI 3; baby: AI 1, avoid; outdoor: "stress tests", AI 4 for mood and 2 for proof). This doc replaces those lines with evidence:
- teardowns of 16 public TikToks we downloaded and measured, plus metadata for 12 more;
- Meta creative benchmarks for each sub-niche (Benly Q1 2026), which split cleanly: **pets reward product shots, baby rewards UGC, outdoor rewards studio work**;
- AI-realism pitfalls specific to fur, gait, babies, fire, smoke, ice, steel and fabric, mapped to doc 43's model rules;
- the policy and legal landmines (pet-food claims and NAD, safe-sleep imagery, baby monitors as medical devices, CARU, "smokeless", "leakproof", "ice for days");
- the buyer, 20 brand types and 8 ready concepts with shot lists, physics checks, audio maps and costs.

**Tags.**
- `[measured]`: we downloaded the file and measured it with ffmpeg (scene cuts at threshold 0.30, audio RMS in 0.5 s windows, frame tiles that we looked at).
- `[unverified]`: no primary source found.
- `[inf]`: our own inference.
- `[vendor]`: the number comes from a company that sells the thing being measured.

**Method and limits.**
- **TikTok** downloads worked: 16 reels pulled to `scratchpad/niche/pets/` (outside the repo, never committed). Three Frida posts returned "IP address is blocked". Profile listing still fails (yt-dlp JSON error), so every URL came from a web search.
- **YouTube** search worked (`ytsearch`), but metadata and downloads hit "Sign in to confirm you're not a bot" after a few calls. YouTube rows are therefore search-listing metadata only (title, view count, duration).
- **View counts** are the yt-dlp snapshot of 2026-10-09. **Like rate** = likes ÷ views. As in doc 49, a very high view count with a like rate near or under 1 % is read as a **paid-distribution signal**, not a fact `[inf]`.
- **Motion Creative Analytics MCP:** skipped (no workspace, doc 45 §0). Motion's public brand page for BarkBox was read instead.
- **Purchase data:** no measured post publishes CPA or ROAS. Purchase-side evidence comes from Benly's longevity index, Ad Meter/Samba rankings and brand statements.

---

## 0. The 8 findings that matter most

1. **Proof by ordeal is the format this whole niche runs on.** The biggest measured post is a one-take, zero-cut phone video of a Stanley tumbler that survived a car fire with ice still rattling inside: **98.6M views, 9.4 % like rate** `[measured]`. The same shape repeats at every budget level:
   - Béis at a real airline counter, scale reading 40.0 lb (344K, the paid signature);
   - a YETI partner on his 65th attempt at a snow-tube jib, tumbler in hand (1.8M, 6.2 %);
   - Frida's gas reliever that "whistles when it works", demonstrated on an apple (3.8M, 1.5 %).

   The product survives something, or proves itself in public. **VXO can stage the ordeal; the proof moment must be real or claim-safe.**
2. **The three sub-niches want different assets on Meta (Benly Q1 2026, effectiveness index 0–100)** `[vendor]`:

   | Sub-niche | Best asset | Worst asset |
   |---|---|---|
   | Pets & Animals (6.1K creatives) | **Product Shot 72** (median life 74 d, 78 % alive at 30 d) | Graphic Design 44, UGC 45 |
   | Family & Parenting (3.4K) | **UGC/Organic 77** | Motion Design 54, Lifestyle 60, Graphic 60 |
   | Sports & Recreation (2.9K) | **Branded/Studio 67**, Lifestyle 65 | **UGC 18** |
   | Travel & Hospitality (9.8K) | Motion Design 50, Studio 41 | Lifestyle 31, Graphic 30 |

   **VXO's cinematic product film fits pets and outdoor gear. In baby and kids, it has to arrive inside a UGC frame.**
3. **Pet creatives live longest; outdoor creatives die fastest.** Pets & Animals: 30 d median, 40 d average, **Pet Supplies 60 d average**. Family & Parenting: 26 d median. Sports & Recreation: **20 d median, 0 % alive at 60 d**, and 53 % of its creatives are "New Launch" `[vendor]`. A pet film can be a Premiere ($2,500) one-off. Outdoor gear needs the Season plan ($3,500/mo), because it ships new colours and launches monthly.
4. **Do not generate babies.** Five independent reasons:
   - model safety filters scrutinise youth words (doc 43 §5);
   - New York's synthetic-performer disclosure law covers AI people in ads (doc 45 §5.3);
   - the 4A's safe-sleep guidance bars loose bedding, pillows and soft toys in any sleeping-baby image, and the CPSC infant-sleep rule targets "marketing ploys showing a baby sleeping";
   - the Toys"R"Us Sora film (2024) was attacked for a child whose face "changes each time you see them";
   - parents punish tone: Frida, the niche's organic leader, faced a 2026 boycott over packaging innuendo (a 7.8M-view creator video).

   **House rule: the baby is heard, not seen.** Parents' hands, the product, the room and the sound carry the film. Real babies only from client footage with consent.
5. **AI animals fail on fur that doesn't move, gait, limb count and multi-animal contact.** Kapwing's Feb 2026 test scored **Kling 2.6 20/20**, Seedance 2 14, Sora 2 and Veo 3 13: Seedance's fur was "under-textured", Veo's dog-and-cat play was "loose, abstract". **Fix:** a real photo of the client's (or a licensed) dog as the Kling 3.0 i2v start frame, one animal per frame, tight shots of 5 s or less, and **never a generated close-up of eating or chewing** (the mouth–object contact breaks). Doc 43's i2v-insert rule extends from labels to animals.
6. **In pets, a real owner with a real dog beats brand polish by 5–6× on engagement.** A Farmer's Dog partner creator (one take, 35 s talking head before any cut): 668K views at **10.1 %**. WeRateDogs' BarkBox toy ranking: 8.7 %. The Farmer's Dog's own polished film, a fresh-vs-kibble comparison: **4.8K views at 1.8 %** `[measured]`. The dog's reaction *is* the proof, so **an AI dog must never be used as evidence** ("dogs love it", "picky eater converted"). That is a fake testimonial in all but name `[inf]`. Use AI for the world and the joke; keep the evidence real.
7. **Outdoor/drinkware sells through drops and sound.** Owala's 8 s "Boo-Ya" glow-in-the-dark reveal: **4.1M views at 8.5 %**. Lights off, the ghost print glows, the logo, done. Owala's colour drops "sell out pretty much within less than an hour" (Salt Lake Tribune 2025). Stanley's fire video sells through **one sound: ice rattling in a burnt car**. Both are ideal AI territory: a **rigid object, a light change, a single diegetic sound**. No faces need carry the proof.
8. **The claims are where these films get pulled.**
   - **Pet food:** comparative claims draw NAD challenges (The Farmer's Dog v. Sundays for Dogs, closed April 2026; v. Freshpet earlier). "Human grade" has an AAFCO handling definition. Disease claims turn food into a drug (FDA CVM).
   - **Baby monitors** with alarms are medical devices: FDA's 2021 warning letter halted Owlet's Smart Sock until a 2023 De Novo clearance.
   - **Drinkware:** Stanley spent 2024–2026 defending "safe" in lead class actions (dismissed April 2026).

   Rule: **every on-screen claim maps to a client test sheet** ("ice after 72 h at 21 °C, lid closed"), never an adjective ("indestructible", "smokeless", "leakproof forever").

---

## 1. Teardowns: 16 measured reels (2023–2026) plus 12 metadata-only

`[measured]` = downloaded. Cut rate = (cuts + 1) ÷ duration. Hook = what is on screen and in the audio during second 1. TikTok's 4 s end card is included in some durations (noted).

### 1.1 Measured (TikTok)

| # | Ad | Date · views · like rate | Length · cuts · shots/s | Second 1 (hook) | Turn / punchline | Sound | CTA | Why it sold |
|---|---|---|---|---|---|---|---|---|
| O1 | **Stanley car fire**, @danimarielettering ([link](https://www.tiktok.com/@danimarielettering/video/7301724587488759070)) | 2023-11-15 (older anchor) · **98.6M** · **9.4 %**, 49.7K comments | 14.8 s · **0 cuts** · one handheld take | A burnt-out car interior, melted dash, red door sill: disaster already on screen | The camera finds the tumbler upright in the cupholder, she lifts it and **shakes it: ice rattles** | Her voice −28 to −32 dB; the rattle peaks at −23 dB around 7.5–12 s | None (organic); Stanley's president replied with a stitched video offering her a new car | **Proof by ordeal, filmed by a customer.** One take = undeniable. The proof is a sound. It sold so well that the brand bought the story (car replacement) |
| O2 | **Stanley × Messi "Quencher ProTour"** ([link](https://www.tiktok.com/@stanleybrand/video/7440150786262207787)) | 2024-11-22 · 1.5M · **7.6 %** | 30.0 s · 16 · 0.57 | A hand pushes the pink tumbler into a bag; Messi's face in shot 2 | The tumbler in a duffel is thrown, dropped from a golf cart, hurled across a hangar; Messi drinks from it: "Action proof. Leakproof." | Near-silent 1.5 s open (−51 dB), then a flat music bed at −22 dB | Launch date | **Abuse montage = leakproof proof** (the bag never gets wet). Celebrity licence is not reproducible; the **"throw the bag" coverage** is |
| O3 | **Owala "Boo-Ya" FreeSip** ([link](https://www.tiktok.com/@owala/video/7416476002915847467)) | 2024-09-22 · **4.1M** · **8.5 %** | 12.1 s (≈8 s content + end card) · 9 · ≈1.1 | A hand pulls the white bottle out of a bowl of Halloween candy | Lights go out: **the ghost print glows green**; macro on the logo; date super | Bed −17 to −20 dB, stinger peak −6 dB at 8 s | "Available 9/24 10am MT" | **A light-change reveal of a limited drop.** Rigid object, one trick, eight seconds. Exactly what AI does well |
| O4 | **BÉIS "Testing the weight indicator"** ([link](https://www.tiktok.com/@beis/video/7493972519230197038)) | 2025-04-16 · 344K · **0.95 %** (paid signature) | 15.8 s · 1 detected (handheld whips) | A woman at a real airline counter heaving a red check-in case | She lifts it by the handle (where the built-in indicator sits); the airline scale reads **40.0 lb**; the agent smiles and tags it | Room tone and voice, −25 to −35 dB | New colour drop on the app | **The test happens where the fear happens** (the check-in scale). Real agent, real scale, no claim adjectives |
| O5 | **@teresalauracaruso × BÉIS small carry-on** ([link](https://www.tiktok.com/@teresalauracaruso/video/7383715370680683822)) | 2024-06-23 · 1.9M · 5.1 % | 29.6 s · **40** · **1.39** | Hands unzipping a pink carry-on on a white bed | Everything fits; "even fits on Frontier & Spirit" | Packing ASMR, very quiet (−40 to −60 dB), no VO | #beispartner, link in bio | **Pack-with-me ASMR at 1.4 cuts/s.** Hands only, no face. The fastest cut rate in the set, and it works because each cut is one object going in |
| O6 | **@mattslyon × Solo Stove "Smokeless Steve"** ([link](https://www.tiktok.com/@mattslyon/video/7301760492765236523)) | 2023-11-15 · 2.2M · 5.7 % | 52.5 s · 4 · 0.10 | Super "Every Person with a Smokeless Fire Pit: Part 2"; he walks in carrying the bag | A one-man character sketch: the obsessive owner who unpacks, explains and sits *inside* the routine | Single voice, −30 to −40 dB | #ad | **Character comedy about the owner, not the product.** The fire pit is the prop that defines the character (doc 44 §8) |
| O7 | **@ryannpurvis × YETI "The Z challenge"** ([link](https://www.tiktok.com/@ryannpurvis/video/7444587803788299538)) | 2024-12-04 · 1.8M · 6.2 % | 53.9 s · 21 · 0.41 | Helmet-cam POV on a snowboard, tumbler in the gloved hand, a black tube jib below | "Attempt #18… attempt #65… got it!": the tumbler rides along every attempt and he sips between tries | Voice + wind, loud (−14 to −25 dB) | #YETI_Partner | **Persistence story, product as companion.** POV makes the camera diegetic (doc 42 rule 5). The tumbler surviving 65 falls is the unspoken proof |
| P1 | **@simonsits × The Farmer's Dog** ([link](https://www.tiktok.com/@simonsits/video/7505899204942826782)) | 2025-05-18 · 668K · **10.1 %** | 75.9 s · 9 (all after 35 s) · 0.13 | Woman in a cream cardigan, warm kitchen, holding the pouch: "Okay so ever since Tiki got his dental…" | Two dogs race to the bowls; close-ups of them eating; back to her with the code | Voice −30 to −35 dB, no music | "Free shipping, link in bio" | **Owner confession + the dog's real reaction.** 35 s of uncut talking before any b-roll. #tfdpartner |
| P2 | **The Farmer's Dog "Our fresh food looks like real food"** ([link](https://www.tiktok.com/@thefarmersdog/video/7546703680335039757)) | 2025-09-05 · 4.8K · 1.8 % | 34.1 s (incl. end card) · 14 · 0.44 | A scruffy terrier staring into the lens | Bowl of "The Farmer's Dog. Turkey" vs a bowl of kibble: "Apparently, this is also turkey." Fork, steam, a woman smiling | Music bed −13 to −18 dB with VO | Logo | **Control: a well-made brand film with a comparative claim and no story.** 1/140 the reach of P1 on the same account's category |
| P3 | **BARK "Something spicy is coming"** ([link](https://www.tiktok.com/@bark/video/7535571440104443166)) | 2025-08-06 · 304K · 0.99 %, 435 comments | 13.1 s · 4 · 0.38 | A red curtain, neon peach and eggplant signs | "Bark After Dark": pixelated toys, dogs with "CENSORED" bars | Loud music −11 to −15 dB | "Link in bio to sign up" | **Innuendo teaser for adults.** It works for BARK's dog-owner audience; the same tone sank Frida in baby (§4) |
| P4 | **@weratedogs "Top 5 wildest BarkBox toys"** ([link](https://www.tiktok.com/@weratedogs/video/7485796233026538783)) | 2025-03-25 · 245K · **8.7 %** | 84.6 s · 21 · 0.26 | Host to camera, holding two plush toys | Ranked list: Tampawns, a cassette tape, a "Blunt Hound"; real dogs with each | Voice −24 to −28 dB | "BARK will give $10 to [shelter] for every…" | **Toy-as-joke.** BARK's product is the punchline (pun toys). A rescue donation as CTA |
| K1 | **Frida Baby Windi "whistles when it works"** ([link](https://www.tiktok.com/@fridababy/video/7484310762932981022)) | 2025-03-21 · **3.8M** · 1.5 %, 1,744 comments | 17.9 s · 7 · 0.45 | Hand holds the Snow White-painted Windi over an apple: "Imagine this is your baby's butt" | Lube, insert into the apple, "what'll happen next is either a super long fart or a ton of poop" | One VO line, steady −27 dB, cut on each phrase | "Baby will feel so much better" | **A prop stands in for the baby.** The apple carries the demo; no infant on screen. The whistle is the proof device (sound again) |
| K2 | **Frida "Breast milk ice cream truck"** ([link](https://www.tiktok.com/@fridababy/video/7534085339267321119)) | 2025-08-02 · 236K · 2.8 % | 29.1 s · 19 · 0.69 | A silver tanker truck reading "BREAST MILK" rolls through Manhattan | Street vox-pops: "What breast?", "Can I ask why?", free samples | Street sound + voices −21 to −30 dB | "See you in Brooklyn", Aug 5–10 | **Stunt + vox-pop.** A real truck in a real street. The brand's organic engine (110M+ organic views, Marketing Brew 2024) |
| K3 | **Lovevery Play Gym on TikTok Shop** ([link](https://www.tiktok.com/@lovevery/video/7322255462299143467)) | 2024-01-10 · 531K · **0.33 %** (paid signature) | 13.7 s · **0** | A baby doing tummy time on the gym, "Have you heard?" + "SOUND ON" badge | Super: "The Lovevery Play Gym is now available on TikTok Shop!" | Quiet, −35 to −40 dB | TikTok Shop | **Real baby, real UGC, one take.** Benly's Family & Parenting UGC index of 77 in one clip. The baby is customer footage (credited @imoneeniyah) |
| K4 | **@_brookehoppe × Coterie "Diaper review"** ([link](https://www.tiktok.com/@_brookehoppe/video/7418969310833560875)) | 2024-09-26 · **996K** · 2.5 %, 699 comments | 28.3 s · 4 · 0.18 | Mom wearing her baby in a carrier, five diapers taped to a white wall like evidence | She walks the wall: Pampers, Kirkland, Honest, Huggies… pros/cons supers; Coterie last, with hearts | Voice −22 to −28 dB | Code for 20 % off | **Us-vs-them on a wall.** Comparative claims made by a creator, as opinion. The baby is held, back to camera, face barely visible |
| A1 | **@longliveai "Seedance 2.0 mutant dog vs cat"** ([link](https://www.tiktok.com/@longliveai/video/7610794090732522774)) | 2026-02-25 · 16.8K · 1.3 % | 10.1 s · 0 · one take, letterboxed 16:9 | Giant collie and ginger cat boxing over a town | They grapple; the cat falls; smoke | Music −14 to −21 dB | Follow | **AI animal spectacle without a product or joke.** Doc 42 rule 11 again: spectacle doesn't travel |

### 1.2 Metadata only (YouTube search listing, not downloaded)

YouTube view counts on brand channels largely reflect paid TrueView/Shorts distribution `[inf]`.

| Ad | Views · length | Note |
|---|---|---|
| Chewy "Dash, the recent rescue" ([link](https://youtu.be/-k6www7PtkY)) | 35.4M · 31 s | Chewy's 30 s "pet portrait" series: "Gouda, the cheesiest boy" 29.3M, "Junior, the forever friend" 16.4M, "Rex, the wrecking dog" 3.5M. **One named pet, one trait, 30 s.** Dates blocked by YouTube `[unverified]` |
| The Farmer's Dog "Forever" (Super Bowl 2023) ([link](https://youtu.be/IAIo-pUDl0s)) | 36.4M · 61 s | #1 on USA Today Ad Meter (6.56) and Samba TV's top-reach brand ad of the game ([Ad Age](https://adage.com/article/special-report-super-bowl/farmers-dog-wins-usa-todays-super-bowl-2023-ad-meter/2472121)). A dog's whole life, no product until the end. Older, but the niche's emotional reference |
| The Farmer's Dog "More Good Years" ([link](https://youtu.be/L0Nmxq1VW00)) | 106K · 40 s | The 30–40 s DR follow-up to "Forever" |
| Yoto Mini "Meet Yoto Mini" ([link](https://youtu.be/HLi9_ZVoxaw)) | 40.6M · 30 s | Now "not available"; the kids-audio category's paid workhorse |
| Lovevery "Look at Me Ladybug: visual tracking 1–2 months" ([link](https://youtu.be/TXpdx725OGM)) | 4.7M · 71 s | **A developmental how-to as an ad.** Parents watch education |
| Lovevery Play Kits ([link](https://youtu.be/Xsd3ioWbjVo)) | 555K · 31 s | Brand 30 s |
| Owala "What makes the FreeSip so different?" ([link](https://youtu.be/wCuE6sIPTG4)) | 2.6M · 41 s | Lid demo: sip vs swig. Plus "20,000+ five star reviews" 1.78M (35 s) and "Girls Night In" 1.4M (12 s) |
| Solo Stove Bonfire ([link](https://youtu.be/6v8uAtSg_FQ)) | 2.55M · 30 s (2021) | "America's favorite smokeless fire pit". Mesa tabletop 1.16M (36 s, 2022) |
| YETI "Don't Get Them a YETI (Unless You Really Love Them)" ([link](https://youtu.be/1mpZZZkrgAU)) | 956K · 61 s | Gift-season reverse psychology |
| Stanley "Quencher H2.0 FlowState" ([link](https://youtu.be/dJxt7IQRoq0)) | 864K · 31 s | Product 30 s |
| Fi "All-new Series 3+ AI-powered GPS collar" ([link](https://youtu.be/BHRiPrvQBA4)) | 1.16M · 61 s | Pet tech explainer; Fi Mini 279K (43 s) |
| Coterie "The Long-Haul Flight Diaper" ([link](https://youtu.be/Z2aptryxYiI)) | 26.8K · 15 s (2026-06-16) | Occasion-named diaper series ("Pass the Baby", "Super Special Outfit", "IYKYK"): **occasion hooks** |

### 1.3 What the measured set says `[measured]`

- **The winners make the camera part of the story.** Phone in a burnt car (O1), helmet-cam on a board (O7), creator at a counter (O4), creator at a wall of diapers (K4). The polished brand films (P2, O2) either borrow a superstar or sit at 1.8 %.
- **Cut rate follows the format, not the niche.** Proof one-takes: 0 cuts (O1, K3). Talking-head creators: 0.1–0.2 shots/s (O6, P1, K4). Skits and lists: 0.26–0.45 (P4, K1, O7). Montage/drop: 0.57–1.1 (O2, O3). Packing ASMR: 1.4 (O5). The 30 s brand film (O2) cuts every 1.8 s, the same rhythm doc 42 found for action.
- **The proof is often a sound.** Ice rattling (O1), the Windi's whistle (K1), packing zips (O5), the airline scale's beep (O4). This matches doc 49's "product sound is a beat inside a story" and doc 38's "visual + audio hook = 1.5×".
- **A prop stands in for whatever must not be shown.** An apple for a baby's bottom (K1), diapers taped to a wall for a diaper test (K4), a bag thrown across a hangar for "leakproof" (O2). **That is the VXO workaround for babies and claims.**
- **Babies on screen are real and incidental.** In both baby posts that show one (K3, K4), the baby is customer footage, never the performer of a claim. No winning post in the set relies on a baby's face.
- **In pets, the owner talks and the dog proves.** P1 and P4 are 80 % human to camera; the dog appears for the reaction. No measured winner uses a dog as a talking character. (Chewy's TV series shows that pet "portraits" work at 30 s with VO; the dog never speaks.)
- **AI spectacle fails here exactly as in doc 42.** The only AI post (A1) has no product, no joke and a 1.3 % like rate.

---

## 2. What actually converts in this niche (data)

| # | Finding | Number | Source | Status |
|---|---|---|---|---|
| N1 | Pets & Animals: effectiveness by asset | **Product Shot 72**, Lifestyle 48, Studio 48, UGC 45, Graphic 44; Product Shot median life **74 d**, 78 % survive 30 d | [Benly pets](https://benly.ai/benchmarks/q1-2026/pets-animals), 6,108 creatives, 23 brands, Q1 2026 | `[vendor]` |
| N2 | Pets: hooks and sub-industries | Bold Statement 23.8 % of video hooks (34 d), Visual Intrigue 22.1 % (41 d), Pain Point 18.7 %, Pattern Interrupt 16.2 %. Pet Food 44 d avg life; **Pet Supplies 60 d**; Pet Healthcare 23 d. **Discount intent 73 %** (66 % → 78 % Jan–Mar) | same | `[vendor]` |
| N3 | Pets: image vs video | Images live longer (43 d avg vs 37 d); 50/50 split | same | `[vendor]` |
| N4 | Family & Parenting: effectiveness by asset | **UGC 77**, Studio 65, Lifestyle 60, Graphic 60, Motion 54. Top hook Visual Intrigue 32 %. Baby Food 41 d, Baby Products 36 d, Toys 23 d. **Only 14.5 % survive 60 d** | [Benly family](https://benly.ai/benchmarks/q1-2026/family-parenting), 3,367 creatives, 19 brands | `[vendor]` |
| N5 | Sports & Recreation: effectiveness by asset | **Studio 67**, Lifestyle 65, Product Shot 59, Graphic 55, **UGC 18**. Median life **20 d**; **0 % survive 60 d**; New Launch intent 53 % | [Benly sports](https://benly.ai/benchmarks/q1-2026/sports-recreation), 2,902 creatives | `[vendor]` |
| N6 | Travel & Hospitality | Motion Design 50, Studio 41, UGC 34, Lifestyle 31. **Travel Gear** sub-industry: 34 d avg, 36 % video, Visual Intrigue hook 61 % of video | [Benly travel](https://benly.ai/benchmarks/q1-2026/travel-hospitality), 9.8K creatives | `[vendor]` |
| N7 | BarkBox on Meta | 19 active ads, ~9 new creatives/week; **17 of the 20 latest are statics**; formats Offer-First 29 %, Collage 14 %, Humor 7 %; offers "free toys for a year", "free $90 bed" | [Motion library: BarkBox](https://motionapp.com/library/barkbox) | Ad-library read |
| N8 | The Farmer's Dog "Forever" | Ad Meter #1 (6.56), Samba TV top reach, Emmy nomination; strategy shift from product detail to "owners want their dogs to live as long as possible" | [Ad Age](https://adage.com/article/special-report-super-bowl/farmers-dog-wins-usa-todays-super-bowl-2023-ad-meter/2472121), [Campaign CMO 50](https://www.campaignlive.com/article/cmo-50-2023-katie-iles/1835615) | Press |
| N9 | Stanley car fire | 84–98M views in weeks; president's reply video 32M+; Stanley revenue cited at ~$750M for 2023 (from ~$70M in 2019) | [designrush](https://news.designrush.com/stanley-finds-marketing-breakthrough-in-viral-video), [hardware connection](https://thehardwareconnection.com/?p=11396) | Revenue figure `[unverified]` (reported both as actual and projection) |
| N10 | Owala drops | Hundreds of limited colour drops; "sells out pretty much within less than an hour" | [Salt Lake Tribune 2025](https://www.sltrib.com/news/business/2025/03/22/how-utah-family-made-owala-water) | Press, quotes a subreddit moderator |
| N11 | Frida organic | 110M+ organic TikTok views; an anatomical-model fertility tutorial got 11M | [Marketing Brew 2024](https://marketingbrew.com/stories/2024/04/30/how-frida-found-organic-success-through-unfiltered-content) | Press |
| N12 | US pet market | $152B in 2024; **$158B in 2025**, $165B projected 2026; 95M pet households; Gen Z ownership 11 % (2018) → 20 % (2024), 70 % of Gen Z owners multi-pet | [APPA 2026](https://americanpetproducts.org/news/the-american-pet-products-association-appa-releases-2025-state-of-the-industry-report), [Petfood Industry](https://www.petfoodindustry.com/pet-food-market/market-trends-and-reports/news/15825309/us-pet-industry-hits-158-billion-in-2025) | Trade association |
| N13 | Pet ROAS case claims | Agency claims: whitelisted creator ads 2.4–4.1× brand ads on ROAS; a pet supplement at 4.8× | [Redefine Web](https://redefineweb.com/blog/proven-ppc-for-pet-brands-grow-subscription-revenue/), [Top Growth](https://topgrowthmarketing.com/services/pet-marketing-agency/) | `[vendor]` `[unverified]`, no n |
| N14 | Ollie on TV | iSpot: the :30 "Marco" was the campaign's strongest performer among dog owners | via [iSpot hub](https://www.ispot.tv/hub/?p=36597) | Survey-based |
| N15 | Format hit rates (all niches) | Unboxing 9.83 %, founder 8.57 %, demo 8.11 %, cinematic b-roll 6.85 % | doc 45 D3 (Motion, 550K ads) | `[vendor]` |

### 2.1 What this means, by sub-niche `[inf]`

- **Pets (toys, beds, collars, bowls, grooming, carriers):** product shots win and live 74 days. Sell VXO's **hero product film + 4–6 product stills cut from it** (Benly's image lifespan beats video). The comedic film is the hook layer; the product shot is the long runner. Put the offer on the end card: 73 % of pet creatives carry a discount.
- **Pet food and supplements:** creator confession + the dog's real reaction (P1) is the converter; the brand film is weak (P2). VXO's role is the **world and the joke around real footage** (hybrid, doc 42 rule 8), or the long-running emotional brand film (Farmer's Dog "Forever" shape) for brands that can afford reach.
- **Baby and kids:** UGC 77, Studio 65. A VXO film must **look like a parent's phone video** (POV, one take, a hand, a caption) or be a **prop demo** (Frida's apple). Highest-value VXO deliverable here: **product-only and hands-only films and stills**, plus a UGC-style wrapper the brand's creators can stitch.
- **Outdoor gear and drinkware:** Branded/Studio 67, UGC 18, life 20 days. **This is VXO's best fit**: studio-made films win, and the 20-day lifespan means a constant need for new launch films. Sell Season.
- **Travel gear (luggage, packing):** lifestyle editorial is weakest (31); motion design and studio work lead. Use **test-at-the-pain-point films** (scale, sizer, overhead bin) and packing ASMR (hands only).

---

## 3. AI realism pitfalls for this niche, and the fixes

Builds on doc 43 §1 (model table), §5 (failure → fix) and doc 41. Only the niche-specific traps are listed.

| Subject | What goes wrong | Fix (prompt + reference + model) |
|---|---|---|
| **Fur** | Static, flat or "plush-toy" fur that does not shift with motion; over-symmetrical face, oversized eyes, underdefined muzzle ([Kapwing 2026](https://www.kapwing.com/resources/best-ai-video-models-for-realistic-animals/)) | Start every dog/cat close-up from a **real photo** (client's own pet, or a licensed stock photo) via **Kling 3.0 Pro i2v** (Kling led the Kapwing test). Prompt: "fur moves with each step and lifts in the breeze, individual guard hairs catch the rim light, natural asymmetry". Add grain in post |
| **Gait, legs, paws** | Wrong gait cycle, a leg vanishing for a frame, extra paw; floaty steps | One animal per shot; **≤5 s**; describe start and end poses, not "running" (doc 43 rule 11). Prefer sitting, lying, head turns, tail sweeps. Walking only in medium-wide, cut before 3 s. Write "exactly four legs, each paw plants and bears weight, pads splay on landing" |
| **Eating, chewing, licking** | Food dissolves into the mouth, the toy passes through teeth, the tongue morphs | **Never generate the mouth–object contact.** Cut on action: the bowl before, the empty bowl after; or a **real insert** of the client's product being chewed. Doc 43 rule 12: script the object's fate ("the toy stays whole; tooth marks rebound") |
| **Two animals, or animal + person touch** | "Loose, abstract interactions" and hallucinations in multi-animal shots ([Kapwing](https://www.kapwing.com/resources/best-ai-video-models-for-realistic-animals/)) | One animal per frame; a person's hand touches the animal only in a locked close-up from a real photo; no pets playing together |
| **Wet dog, shake, mud** | Water spray from a shake is liquid physics (doc 11); mud slides like paint | No generated shake. Mud as **static clumps** ("dried mud in clumps on the legs, no dripping"). Wet fur as slicked texture, not moving water |
| **Babies and toddlers** | Safety filters; uncanny faces that change between shots (Toys"R"Us 2024); unsafe-sleep imagery | **Baby heard, not seen.** Hands, back of head at distance, an empty high chair, a crib only as a dark doorway. Real baby only from client footage with consent (§4) |
| **Kids' toys (wood, felt, silicone)** | Wood grain swims; felt pills grow; silicone looks like glass | i2v from the client's product photo; "matte food-grade silicone, soft diffuse highlight, flexes 2–3 mm when pressed then recovers"; rigid wooden toys "never bend" |
| **Car seats, strollers, carriers** | Buckles merge, straps pass through each other, a harness on the wrong side, a stroller folding into an impossible shape | Show folding only from **first/last frames of the real product** (Kling `last_image_url`) or a real insert. Any child-restraint shot must show **correct use** (chest clip at armpit level; harness snug) or the brand will get corrected by parents and CPSTs `[inf]` |
| **Fire and flames** | AI fire is good (doc 02: candles AI 5) but flames ignore wind; embers float like snow | Name the wind ("light breeze from frame-left; flames lean right"); embers "rise, flicker out within a second". Night shots hide artifacts (doc 42 rule 12) |
| **Smoke** | Smoke ignores the wind direction from shot to shot; dry-ice fog | A FIXED GEOGRAPHY line for wind (doc 43 §7.1 pattern): "wind always from the lake side, frame-left in the wide". **Do not show "zero smoke"** unless the client's test says so (§4) |
| **Stainless steel drinkware** | Reflections that don't match the set; **condensation on a vacuum-insulated tumbler** (impossible: a working double wall does not sweat) | Clean, simple set so the reflection is plausible; write "no condensation on the outer wall, it is vacuum-insulated"; brushed steel = "soft streaked highlight, no mirror" |
| **Ice** | Ice that melts and regrows; cubes merging; the rattle without visible motion | Ice only heard in a closed tumbler (Stanley O1 logic); if shown, "4 cubes, they only shrink" (doc 43 rule 12). Rattle placed on the measured shake frame in post |
| **Technical fabrics (shells, down, tents)** | Rain that soaks a "waterproof" shell; down jackets with no baffle structure; tent poles bending like rubber; guy-lines floating | Beading water = **real insert** (a spray bottle on the client's fabric is a 2-minute phone shot). Prompt: "aluminium tent poles are rigid between joints and flex only in a smooth arc under tension; guy-lines are taut straight lines". Show a pitched tent static, never pitching |
| **Luggage** | Wheels that slide instead of roll; shell that dents like foil; zippers that heal | "Four spinner wheels rotate and swivel; the case rolls, never slides"; "polycarbonate flexes 1 cm under a knee and springs back"; zipper teeth only from the product photo, no zipping close-up generated |
| **Labels and printed patterns** | Logo on a curved bottle warps; all-over print (Owala ghosts) swims | Doc 43 §1 product-macro rule: **Kling i2v from the product photo, one move, sound off**. All-over prints as i2v only, never r2v |
| **Phone UI (GPS collars, baby monitors, apps)** | Generated screens are garbage text | Shoot the screen green or black; comp the client's real UI in post. Never generate a health reading (§4) |
| **Water bodies (lake, river, pool)** | Water moves the wrong way past a canoe; reflection mismatch | Still water at dawn (mist hides it); no paddling close-ups; boats static or locked-off wide |

---

## 4. Ad policy and legal constraints

Rules change; re-check before each campaign. Doc 45 §5 (weapons, police, AI labels, FTC fake reviews, NY synthetic performers) applies in full. This section adds only what is niche-specific.

### 4.1 Pets

| Topic | Rule | Source | VXO rule |
|---|---|---|---|
| Pet food disease claims | A product that claims to treat or prevent disease is an **animal drug**, not food (CPG 690.150). Specific health claims (urinary tract, hairball) need FDA CVM review | [FDA: animal food labeling and pet food claims](https://www.fda.gov/animal-veterinary/animal-foods-feeds/animal-food-labeling-and-pet-food-claims) | On screen: ingredients, process, nutrient facts. Never "cures itching", "prevents kidney disease", "adds years" |
| "Human grade" | An AAFCO **handling** specification: every ingredient and the product handled under human-food cGMPs (21 CFR 117); must be paired with intended use ("human grade dog food") | [AAFCO Human Grade guidelines](https://www.aafco.org/wp-content/uploads/2023/01/Appendix_A_Human_Grade_Guidelines.pdf) | Only if the client holds the documentation; always "human-grade dog food" |
| Comparative and price claims | NAD (BBB National Programs) hears competitor challenges. **The Farmer's Dog v. Sundays for Dogs** (Case 7523, closed 8 Apr 2026): air-drying superiority claims and implied price comparisons had to change; NAD found consumers would read the price comparison as including The Farmer's Dog **even though it wasn't named**. Earlier, Freshpet changed ads that implied "human-grade" | [Faegre Drinker](https://www.faegredrinker.com/en/insights/publications/2026/5/advertising-alert-sit-stay-substantiate-nad-review-of-pet-food-claims-provide-important-reminders-when-comparing-products), [Kilpatrick](https://ktslaw.com/blog/kilpatrick-ad-vantage/2026/5/barking-up-the-right-tree) | No "vs kibble" or "vs [leader]" visual comparison unless the client has head-to-head data. A kibble bowl next to the product (P2) is a comparative claim |
| "Vet recommended" | Needs survey evidence that a meaningful share of vets recommend it; "vet approved" is not a usable term | Only a brand blog found ([Freshpet](https://www.freshpet.com/blog/what-does-vet-recommended-dog-food-mean)) `[unverified]` | Never a white coat or "vet" character in the film. No AI vet |
| Live animals | Meta bars peer-to-peer live-animal sales; allows shelters, retail, breeders | [Meta: live animals](https://transparency.meta.com/policies/ad-standards/restricted-goods-services/live-endangered-nonendangered-animals) | Not our product category; keep "adoption" CTAs to real shelters the client names (P4 pattern) |
| Pet meds, flea/tick | Meta prohibits direct sale of prescription drugs; flea/tick parasiticides are EPA-registered pesticides or FDA drugs | [Meta drugs](https://transparency.meta.com/policies/ad-standards/restricted-goods-services/drugs-pharmaceuticals/) | Out of scope for VXO films. Specific ad rules for vet products `[unverified]` |
| Animal welfare on screen | No platform rule found that bans fictional animal peril, but audiences report "animal in distress" fast `[inf]`. TikTok bars "dangerous, harmful, or violent acts" (doc 45 §5.1) | — | Dogs never in danger, never in a moving car's front seat or unrestrained in a cargo area, never eating human junk food on camera. Show a car tether in any car shot |
| "Indestructible" | Classic complaint and NAD bait for chew toys `[inf]` | — | Use the client's guarantee wording ("replace it free if…"), never "indestructible" |

### 4.2 Baby and kids

| Topic | Rule | Source | VXO rule |
|---|---|---|---|
| Safe-sleep imagery | 4A's guidance: depict babies (≤18 months) **only in safe-sleep positions and environments**: on the back, flat, firm surface, **no blankets, quilts, bumpers, pillows or stuffed animals** in the sleep space. Studies found 35–40 % of crib ads showed unsafe sleep | [4A's](https://www.aaaa.org/guidance-safe-sleep-advertising/), [Pediatrics via Children's Mercy](https://news.childrensmercy.org/reuters-crib-ads-often-show-babies-in-unsafe-sleep-settings/) | No sleeping baby in any VXO film. Nursery shots: empty crib, fitted sheet only |
| Infant sleep products | Safe Sleep for Babies Act (2022) bans inclined sleepers and padded bumpers; the CPSC rule covers anything **"marketed or intended to provide a sleeping accommodation"**, and staff called out "showing a baby sleeping but then saying the product is not for sleep in small print" | [Morgan Lewis](https://www.morganlewis.com/pubs/2022/12/safe-sleep-for-babies-what-you-need-to-know-if-you-offer-infant-sleep-products) | Loungers, nests, pods, swaddles: never imply sleep unless the product is certified for it. The film's picture is the claim |
| Baby monitors and wearables | FDA's warning letter (Oct 2021) said Owlet's oxygen and heart-rate **notifications** made the Smart Sock an uncleared medical device; US sales stopped; the Dream Sock got De Novo clearance in Nov 2023 for healthy infants 1–18 months | [FDA warning letter](https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/warning-letters/owlet-baby-care-inc-616354-10052021), [Business Wire](https://www.businesswire.com/news/home/20231109884987/en/) | Never show or imply a health alarm, SIDS prevention or "peace of mind that your baby is breathing" unless the client's clearance covers that exact claim. No generated vitals on screen |
| Sound machines | A Pediatrics study (2014) measured some infant sleep machines above recommended noise limits at crib distance `[unverified exact figures]` | Hugh et al., *Pediatrics* 2014;133(4) | Show machines across the room, not in the crib; no "louder = better" |
| Advertising to children | CARU guidelines (in force 1 Jan 2022) cover child-directed ads to **under-13s**: truthful, clearly ads, no unsafe behaviour, clear influencer disclosures in language kids understand; CARU's generative-AI guidance asks for disclosure when kids could think a virtual character is real | [BBB National Programs](https://bbbprograms.org/media-center/prd/CARU-revised-guidelines-for-advertising-to-children), [MediaPost](https://www.mediapost.com/publications/article/410029/caru-issues-guidance-for-ai-aimed-at-kids.html) | Toy films are aimed at **parents**, not kids: no "ask your parents", no kid-speak urgency. Toy capability shown at true scale and speed |
| TikTok baby/minors | Ads may not involve minors in inappropriate content; baby food and infant formula are restricted or banned in several regions; TikTok updated its Baby Food Products policy in June 2026 | [TikTok NA handbook](https://ads.tiktok.com/help/article/ad-policy-handbook-north-america?lang=en), [2026 change log](https://ads.tiktok.com/help/article/tiktok-ad-policy-change-log-2026) | Infant formula: decline. Baby food: check the June 2026 text first `[unverified content]` |
| AI children | NY synthetic-performer disclosure applies to AI people of any age (doc 45 §5.3); model filters flag youth words (doc 43 §5) | — | No AI child faces. Hands-only shots of a child are a grey zone `[inf]`; prefer an adult's hands or none |
| Tone | Frida's packaging innuendo ("How about a quickie?") drew a 2026 boycott call and a 7.8M-view creator video | [Modern Retail](https://www.modernretail.co/marketing/frida-baby-faces-backlash-over-the-use-of-sexual-innuendos-in-marketing/) | Gross-out humour (the Windi fart) is the niche's proven register; **sexual innuendo near infant products is not**. BARK's "Bark After Dark" tone works only because the audience is adults with dogs |

### 4.3 Outdoor, drinkware and travel

| Topic | Rule | Source | VXO rule |
|---|---|---|---|
| "Safe" and material claims | Stanley's lead class actions (2024) argued "safe for ordinary use" was misleading; dismissed (Jan 2025, then April 2026) for no plausible risk, after two years of litigation | [Arnold & Porter](https://www.arnoldporter.com/en/perspectives/news/2026/04/arnold-porter-wins-dismissal-of-consumer-class-action-against-stanley-drinkware), [Bloomberg Law](https://news.bloomberglaw.com/litigation/stanley-tumbler-maker-sued-again-over-alleged-lead-advertising) | No "safe", "non-toxic", "lead-free", "BPA-free" unless the client gives the test report |
| Performance claims | Insulation hours, waterproof ratings, "leakproof", "smokeless", "fits all airlines" are objective claims that need substantiation (FTC Act §5) `[inf from doc 45]` | — | On-screen claims carry conditions: "ice after 72 h*" with "*21 °C, lid closed, 2/3 full" on the end card. Prefer "low-smoke" or the client's measured wording over "smokeless" |
| Environmental claims | "Recycled", "sustainable", "PFAS-free" fall under the FTC Green Guides; several states now restrict PFAS in outdoor apparel `[unverified state dates]` | FTC Green Guides (16 CFR 260) | Only exact, client-documented percentages ("made with 60 % recycled polyester") |
| Stunts and dangerous activities | TikTok: professional stunts allowed with "Do not try this at home" if imitable; extreme parkour prohibited; "inappropriate use of dangerous tools, vehicles" prohibited (doc 45 §5.1) | doc 45 | Outdoor action stays within sane recreation: hiking, camping, paddling at rest. No cliff jumps, no fire tricks, no axe throwing in the paid cut |
| Blades, axes, bear spray | Meta prohibits promotion of non-culinary blades and weapons; TikTok bars pepper spray (doc 45 §5.1) | doc 45 | Camp knives, hatchets, bear spray: decline paid work, or keep them out of frame |
| Airline and park branding | Real airline liveries and NPS logos are third-party marks; FTC Impersonation Rule (doc 45 §5.2) | doc 45 | Invented airline counters, unbranded sizers, generic trailheads |

### 4.4 Pre-flight checklist additions (with doc 45 §5.4)

- [ ] No AI baby or child face; no sleeping baby; any nursery shot follows 4A's safe sleep.
- [ ] No health reading, alarm or disease claim (pets or babies).
- [ ] No comparison bowl, competitor product or price comparison without client data (NAD).
- [ ] No AI animal used as evidence of preference, palatability or health.
- [ ] Dogs restrained in cars, never in danger, never eating junk food.
- [ ] Every performance number on screen has a footnoted test condition from the client.
- [ ] AIGC label on; C2PA kept (doc 45).

---

## 5. The buyer

### 5.1 Who signs a $1,200–3,500 film

| Brand stage | Who signs | Where they come from `[inf]` |
|---|---|---|
| Under ~$5M revenue (most pet accessory and baby-gear DTC) | **The founder**, often a couple or a parent-founder who built the product for their own dog or child | They make the TikToks themselves; they buy a film when the product's "hero shot" is missing or a launch is coming |
| $5–30M | **Head of Growth / Performance** (owns Meta spend) with the founder approving taste | Buys on hook rate and cost per test; needs variants, not one film |
| $30M+ (Farmer's Dog, Lovevery, YETI-tier) | **Brand / Creative Director**, with legal and (in baby) a safety or regulatory reviewer | Has agencies; VXO enters through a launch, a colour drop, or a spec film they can't make fast |

### 5.2 What they fear (ranked) `[inf]`, with evidence

1. **Pets: a fake-looking animal.** Owners know how their dog moves; fur and gait are "immediate giveaways" ([Kapwing](https://www.kapwing.com/resources/best-ai-video-models-for-realistic-animals/)). One uncanny dog in the comments ends the campaign.
2. **Baby: a safety or tone backlash.** Parent communities correct unsafe sleep and car-seat use in public (§4.2), and Frida's 2026 boycott shows how fast a beloved brand can be turned on.
3. **Baby: anything AI near a child.** The Toys"R"Us reaction ("ghoulish", "changes each time you see them") is the reference every baby-brand founder has seen ([NBC](https://www.nbcnews.com/tech/internet/toys-r-us-ai-video-ad-controversy-explained-commercial-rcna159030)).
4. **Outdoor: inauthenticity.** Core users spot a wrong knot, a tent pitched in a gully, a down jacket in summer, or a "hiker" in jeans. Studio work wins in Benly's sports data (N5), but only if it is technically right.
5. **Claims trouble.** NAD challenges (pet food), FDA letters (monitors), class actions (drinkware).
6. **Wasted spend.** Outdoor creatives die in 20 days (N5); a film that can't be cut into 10 variants is money gone.

### 5.3 What proof they need

- **A frame of *their* product and, in pets, a breed like theirs**, made from their own product photo (the "5 free frames" lead magnet does this). In pets, offer to use a photo of the founder's own dog.
- **A realism sample in motion:** one 5 s Kling i2v of a dog from a real photo (fur, blink, head turn). This is the single most persuasive asset for a pet founder `[inf]`.
- **A claims sheet:** VXO's list of every on-screen claim, waiting for their test data (§4.4). It shows we know their landmines.
- **The variant plan:** hero + 6 s cut + 4–6 stills + a UGC-style wrapper (baby) or offer end cards (pets, 73 % discount intent).
- **Baby only:** a written "no AI baby" promise and a storyboard that shows how the baby stays off-screen.

### 5.4 Twenty example brand types (no outreach)

Pets:
1. Design-led walk kits: harness, leash, poop-bag carrier (the Wild One type).
2. Heavy-chewer toys with a replacement guarantee.
3. Pun/novelty plush subscription boxes (the BARK type).
4. GPS / activity smart collars (the Fi, Halo, Tractive type).
5. Treat-tossing pet cameras (the Furbo type).
6. Fresh or air-dried dog food subscriptions (the Farmer's Dog, Ollie, Sundays type). Claims-heavy.
7. Cat litter and odour systems (crystal, plant-based, self-cleaning boxes).
8. Orthopedic and outdoor dog beds.
9. Car seat hammocks, crash-tested car harnesses, ramps.
10. Grooming tools and waterless shampoos.

Baby and kids:
11. Parent-problem gadgets (gas, nose, nails, bath; the Frida type). Prop demos.
12. Montessori/developmental play kits and gyms (the Lovevery type).
13. Screen-free kids' audio players and story cards (the Yoto type).
14. Spill-proof cups, suction plates, toddler feeding gear.
15. Travel strollers and car-seat/stroller hybrids (the Doona type). Correct-use scrutiny.
16. Premium diapers and wipes (the Coterie type). Creator comparisons.

Outdoor and travel:
17. Insulated tumblers and bottles with colour drops (the Stanley, Owala, YETI type).
18. Low-smoke fire pits and camp stoves (the Solo Stove, BioLite type).
19. Carry-on luggage and packing systems (the Béis, Away, Calpak type).
20. Packable technical apparel and bags (the Cotopaxi type). Green-claims scrutiny.

---

## 6. Eight ready film concepts (invented brands)

Conventions:
- **Formats:** 9:16 master; 4:5 reframe; a 6 s cutdown; **4–6 stills pulled from the film** (pets: product-shot stills are the long runners, N1); for baby, a UGC-style wrapper.
- **Physics:** each concept passes doc 41 §2 and doc 44's "could a crew rig this?" read. Every camera position below is a tripod, slider, dolly, Steadicam, car mount, helmet cam or locked-off floor camera.
- **Costs** are list prices from doc 43 §6 `[EST]`:
  - Seedance 2.5 r2v: $2.06 / $4.62 per 10 s at 480p / 720p. 15 s scene: $3.09 proof + 3 × $6.93 takes = **$23.88**. 20 s scene: $4.12 + 3 × $9.24 = **$31.84**;
  - Kling 3.0 Pro i2v, sound off: **$0.48 per 5 s insert**, budgeted ×2 = $0.95;
  - stills (Flare / Soul Cinema): ~$0.30 each (doc 11).
- **Animals:** every close-up of an animal is **Kling 3.0 Pro i2v from a real photo** (client's own dog, or licensed). Seedance r2v gets animals only in medium-wide.
- **Babies:** never generated (§4.2).
- **Brand names** are invented and differ from earlier docs. Clear them on USPTO before use.
- **Mascots:** Otto and Vee appear only in VXO's own spec films, so they are absent here. Concepts C4 and C8 convert to VXO spec films most easily: Otto as the deadpan dad or the camper (his mouth is never visible, which removes lip-sync risk).

### C1 · ROAMLY (GPS dog collar) — "The Regular" (20 s)

- **Idea:** 7:02 a.m. The side gate is open and the beagle is gone. The owner, in a robe, follows the app's dot down the block, and finds the dog sitting in the queue at the corner bakery. The baker leans over the counter: "The usual?" The app's history shows the same line to the bakery every morning for a month.
- **Hook (0–1 s):** the gate swings open on its own with a long creak; a dog-shaped gap in the hedge behind it. Visual intrigue + sound.
- **Punchline (product-caused):** the tracking history exposes the dog's secret daily routine. The product didn't just find him; it outed him.
- **Built on:** Chewy's one-dog-one-trait portraits (§1.2), O1's proof-by-reveal, N2 Bold Statement.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Low locked-off camera on the grass: the side gate swings open, latch clacks | Seedance. Gate swings on its hinge arc and decelerates |
| 2 | 1.5–3 | Bedroom, over-shoulder, tripod: a phone on the nightstand buzzes | Screen shot black; client's real UI comped in post |
| 3 | 3–5.5 | Steadicam follow behind the owner in robe and slippers, jogging along a sidewalk | Seedance. Real-time; no traffic in frame |
| 4 | 5.5–7 | Insert, hand-held phone close-up: the moving dot | Post comp on a black screen |
| 5 | 7–9.5 | Wide from across the street, tripod: bakery front, two adults and a beagle sitting in the queue | Seedance. Dog small in frame, sitting still |
| 6 | 9.5–12 | Medium at dog height, locked-off: the beagle sits, tail sweeps the pavement twice; ROAMLY collar visible | **Kling i2v** from a real beagle photo + collar photo |
| 7 | 12–14.5 | Over-the-counter medium: the baker leans out with a paper bag: {The usual?}; the owner arrives breathless behind | Seedance, ≤3 people, line in `{ }` |
| 8 | 14.5–17 | Insert: the history map, 30 identical morning lines to the bakery | Post comp |
| 9 | 17–20 | End card: collar packshot on the bakery bench, "ROAMLY. Know where they go." + first-month offer | Real product photo |

- **Physics check:** the dog never crosses a street on camera and never eats (the bag stays closed). The gate's latch and swing are rigid-body motion. The phone screen is never generated.
- **Audio map:**
  - 0.0 s: long gate creak; latch clack at 0.8 s.
  - 1.5 s: phone buzz ×2.
  - 3 s: slippers slapping pavement, breathing.
  - 7 s: street room tone; bakery door bell at 7.5 s.
  - 12 s: baker's line. 14.5 s: soft map "pop".
  - 17 s: 0.5 s silence → sonic logo.
- **Models and cost:**

  | Item | Cost |
  |---|---|
  | Seedance 2.5 r2v, 20 s scene for shots 1, 3, 5, 7 (template 7.5 adapted; refs: owner, baker, beagle photo, bakery plate) | $31.84 |
  | Kling i2v, shot 6 ×2 | $0.95 |
  | Stills, 9 | $2.70 |
  | **Total** | **≈ $35.50** |
- **Claim check:** "real-time" and "safe-zone alerts" only as the client specifies; never "never lose your dog again".

### C2 · GRITTO (power-chewer toy) — "Round 12" (15 s)

- **Idea:** a boxing-match parody in a living room. The ring bell rings; the toy drops onto the rug. A pit-bull mix bows to it. The owner, a towel over his shoulder like a corner man, reads on the couch. The basket in the corner holds eleven shredded plush toys ("Rounds 1–11"). By the end the dog is asleep with his chin on the toy, and it squeaks once.
- **Hook (0–1 s):** product shot first (N1: product shot index 72): the toy drops into frame onto the rug, bounces once, on a boxing bell.
- **Punchline (product-caused):** the fighter loses to the toy. Final bell rings as the dog snores.
- **Built on:** P4 (toy as joke), BarkBox's "ENTERING HYPER-CHEW" humour statics (N7).

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Top-down, locked-off over the rug: the toy drops in, bounces once, settles | **Kling i2v** from the product photo; rigid rubber, one bounce |
| 2 | 1.5–3 | Low wide, tripod at couch height: the dog lowers into a play bow facing the toy | Kling i2v from a real dog photo |
| 3 | 3–5 | Insert, slider: the "graveyard" basket of shredded plush, stuffing spilling; super "ROUNDS 1–11" | Kling i2v from a still |
| 4 | 5–7 | Product macro, locked: the toy on the rug, deep tooth marks that slowly rebound flat | Kling i2v; "rubber recovers in 1 s" |
| 5 | 7–9 | Medium, tripod: the owner on the couch with a towel over his shoulder, turns a page, glances over | Kling i2v from a still |
| 6 | 9–11.5 | Low wide, same position as shot 2: the dog lying down, chin on the toy, eyes closing | Kling i2v; breathing rise |
| 7 | 11.5–13 | Close, locked: the toy under the sleeping dog's paw; it squeaks once as he shifts | Kling i2v |
| 8 | 13–15 | End card: toy on a white sweep, "Round 12. Still standing." + guarantee line | Real product photo |

- **Physics check:** no generated chewing. The fight happens off-screen in sound only (gnaws over shot 3–4); shot 4 shows the result. The toy's fate is scripted: it stays whole, dents rebound. A real 2 s insert of the client's toy in a real dog's mouth can replace shot 4 if the client has one.
- **Audio map:**
  - 0.0 s: boxing bell "ding"; rubber thud at 0.4 s.
  - 1.5 s: a low play-growl.
  - 3–7 s: off-screen gnawing (library), a crowd murmur from a boxing broadcast on a radio, very low.
  - 7.5 s: page turn.
  - 10 s: a long dog sigh. 12 s: one squeak.
  - 13 s: bell ×3 ("end of fight") → sonic logo.
- **Models and cost:** all Kling 3.0 Pro i2v, 7 shots × 2 takes = **$6.66**; stills 10 = $3.00; **total ≈ $9.70**. The cheapest concept; the right first film for a pet-toy founder.
- **Claim check:** no "indestructible". The guarantee wording comes from the client.

### C3 · TRAILHOUND (waterproof back-seat dog hammock) — "Mud Season" (15 s)

- **Idea:** after a rainy hike, the car's back door opens: a dog caked in mud sits on the hammock, perfectly at home. The owner shuts the door, turns, and we see his back: he is muddier than the dog (he fell). He looks at the clean driver's seat. Cut: he rides in the back on the hammock, next to the dog, while his clean friend drives.
- **Hook (0–1 s):** inside the car, looking out through the open rear door: a mud-caked dog's head pops up into frame, ears up.
- **Punchline (product-caused):** the hammock is the only place the owner is allowed to sit.
- **Built on:** proof by ordeal (O1, O4), outdoor studio work (N5).

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Locked-off camera on the back seat facing the open door: the muddy dog's head pops into frame | Seedance; dried mud clumps, no drips |
| 2 | 1.5–3.5 | Exterior medium, tripod in a gravel trailhead lot: the dog hops onto the hammock; it dips and holds | Seedance; weight lands, hammock dips 3 cm |
| 3 | 3.5–5 | Product macro, slider: muddy paw prints on the quilted fabric, water beads standing still | **Kling i2v** from the product photo; static beads only |
| 4 | 5–7 | Exterior, side, tripod: the owner closes the door with a thunk, turns: mud from shoulder to boots | Seedance |
| 5 | 7–9 | His POV, handheld: the clean, light-grey driver's seat | Seedance |
| 6 | 9–11 | Medium, tripod from the passenger side: the friend, spotless, holds the keys, shakes his head once | Seedance |
| 7 | 11–13 | Dash-mounted, locked-off, facing the back seat: owner and dog side by side on the hammock, both muddy, both staring forward. The dog wears a seat-belt tether | Seedance; deadpan hold |
| 8 | 13–15 | End card: hammock packshot, "Mud goes in the back." | Real product photo |

- **Physics check:** the car is parked for every shot (no driving physics); the engine only starts in sound. Mud is clumped and dry-edged. The dog is tethered (§4.1). No shake, no splash.
- **Audio map:** 0.0 s door latch + dog panting; 2 s fabric creak and a soft thump; 5 s door thunk; 7 s boot squelch; 11 s friend's sigh; 12 s dog snort; 13 s engine start → sonic logo.
- **Models and cost:** Seedance 2.5 r2v 15 s (refs: dog photo, owner, friend, car-interior plate, hammock) $23.88; Kling insert ×2 $0.95; stills 8 $2.40; **total ≈ $27.20**.
- **Claim check:** "waterproof" only with the client's rating; "fits most cars" with the dimensions.

### C4 · HUSHLING (white-noise machine) — "Floorboard" (20 s)

- **Idea:** 2:47 a.m. A dad performs a heist down the hallway past the nursery door (doc 44 §3 heist grammar): masking-tape Xs mark the boards that don't creak. He nails it, until his foot lands on the dog's squeaky toy. Squeak. Freeze. From the nursery: nothing but the HUSHLING's soft hiss. He exhales, turns, and finds his wife asleep in the hallway armchair with a second HUSHLING beside her head.
- **Hook (0–1 s):** a socked foot lowering onto a floorboard that starts to creak; the foot freezes mid-step. Super "02:47".
- **Punchline (product-caused):** the machine covers the squeak, and mom has quietly claimed one for herself.
- **Baby rule:** **the baby is never on screen**, not even as a shape. The nursery is a dark doorway with a warm glow.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Low macro on the hallway floor, locked-off: a socked foot lowers; the board starts to creak; the foot freezes | Seedance |
| 2 | 1.5–3.5 | Medium from the hallway's end, tripod: dad balancing with a mug and a phone torch; the nursery door ajar, dark | Seedance; torch pool consistent |
| 3 | 3.5–5 | Through the door gap, long lens from the hallway: the HUSHLING on a dresser across the room, amber glow | **Kling i2v** from the product photo |
| 4 | 5–8 | Top-down, camera rigged to the ceiling: three masking-tape Xs on the boards; he steps X to X | Seedance |
| 5 | 8–10 | Low close, locked-off: his foot lands on a squeaky dog toy | Seedance; the toy compresses |
| 6 | 10–12 | Close on the door gap, locked: nothing. Only the hiss | Kling i2v; held silence is the joke |
| 7 | 12–15 | Medium, tripod: he exhales, a tiny fist pump, turns | Seedance |
| 8 | 15–17.5 | Reverse wide, tripod: mom asleep sideways in the hallway armchair, a second HUSHLING glowing on the side table | Seedance; adult sleeping, no baby |
| 9 | 17.5–20 | End card: "HUSHLING. For whoever needs it." | Real product photo |

- **Physics check:** the creak is timed to weight transfer onto the board; the squeak toy deforms and recovers. The nursery shows only a dresser (no crib, no bedding, §4.2). The machine sits across the room from where a crib would be.
- **Audio map:**
  - 0.0 s: a slow board creak that cuts off as the foot freezes.
  - 1.5 s: the house's room tone, a fridge hum far away.
  - 3.5 s: the HUSHLING's soft pink-noise hiss enters and stays under everything.
  - 5–8 s: three careful socked steps.
  - 8.6 s: **SQUEAK**. 8.7–12 s: nothing but the hiss.
  - 12.5 s: a long exhale. 15 s: mom's light snore.
  - 17.5 s: sonic logo, quiet.
- **Models and cost:** Seedance 2.5 r2v 20 s (refs: dad, mom, hallway plate, product) $31.84; Kling ×2 $0.95; stills 9 $2.70; **total ≈ $35.50**.
- **Claim check:** no "longer sleep", no medical or SIDS language; volume and distance per the client's manual.

### C5 · CLAMPY (spill-proof snack cup) — "Unemployed" (15 s)

- **Idea:** the family dog's job was catching whatever falls off the high chair. Then the CLAMPY cup arrived. Day 1: the cup falls, bounces, nothing spills; the dog lunges for nothing. Day 4, Day 9: the dog waits under the high chair, chin on paws. Final beat: he has moved under Dad's chair, where the chips are.
- **Hook (0–1 s):** the cup is already mid-fall into a low floor frame; it hits tile and bounces.
- **Punchline (product-caused):** the cup put the dog out of work; he found a new employer.
- **Baby rule:** no child on screen. The high chair is seen from the floor, tray edge only.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Low locked-off floor camera: the cup falls in, hits tile, bounces twice, rolls, lid shut | **Kling i2v** from the product photo; rigid, light (≈60 g) |
| 2 | 1.5–3 | Same position: a golden retriever lunges into frame, mouth open, stops: nothing to eat | Kling i2v from a real dog photo; mouth opens, no contact |
| 3 | 3–4.5 | Product macro, slider: the soft valve flaps hold a cereal ring inside | Kling i2v |
| 4 | 4.5–6 | Floor, locked: the dog nudges the cup with his nose; it rolls away, sealed | Kling i2v; nose–cup contact brief |
| 5 | 6–10 | Same floor frame, three short shots with supers "DAY 1 / DAY 4 / DAY 9": the dog lying under the high chair, light changing from morning to dusk | Kling i2v ×3 from one still with relit variants |
| 6 | 10–12.5 | Wide, tripod: the dog now lies under Dad's chair; Dad, eating chips, drops one; cut on the drop | Kling i2v |
| 7 | 12.5–13.5 | Close: the dog chewing with closed mouth, satisfied | Kling i2v; no object visible |
| 8 | 13.5–15 | End card: "CLAMPY. Snacks stay in. (Sorry, Murphy.)" | Real product photo |

- **Physics check:** the cup is rigid and stays sealed; it bounces twice and rolls in an arc. The chip catch is cut on action (doc 42 rule 4). Dad's chips: adult food for the adult; the dog is never shown eating junk food on camera (§4.1).
- **Audio map:** 0.0 s plastic-silicone clack on tile ×2, a roll; 1.5 s claws scrambling on tile; 2.4 s a confused "huff"; 6 s a clock tick under the day cards; 10 s chip-bag crinkle; 11 s a chip's tiny crunch; 13.5 s sonic logo.
- **Models and cost:** all Kling 3.0 Pro i2v, 6 shots × 2 takes = $5.71; stills 8 = $2.40; **total ≈ $8.10**.
- **Claim check:** "spill-proof" as the client's test defines it (upside-down shake?), shown exactly that way and no further.

### C6 · EMBERLY (low-smoke fire pit) — "Musical Chairs" (20 s)

- **Idea:** around an old open fire ring, smoke follows one man every time he moves his chair: three moves, three faces full of smoke, and he ends up sitting in the hedge. Next weekend: the EMBERLY. He sits, braces, eyes shut... nothing. Opens one eye. Then he starts his favourite long story ("So in 2009…"), and his friends, who used to escape it by "moving out of the smoke", have nowhere to go. One fans the fire hopefully.
- **Hook (0–1 s):** mid-sentence, a wall of smoke rolls into his face; he coughs.
- **Punchline (product-caused):** no smoke means no escape from his story.
- **Built on:** O6 (character comedy about the owner), N5 (studio wins in outdoor).

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Medium across the fire, tripod: smoke rolls into his face | Seedance; wind from frame-left |
| 2 | 1.5–3.5 | Wide, locked-off: he picks up the chair, moves a quarter turn round the ring; the smoke swings after him | Seedance; same wind logic |
| 3 | 3.5–5 | Same wide, jump cut: second move, smoke follows | Seedance |
| 4 | 5–6.5 | Same wide: third move; he is in the hedge, smoke still on him | Seedance |
| 5 | 6.5–9 | Next weekend, slider push-in: the EMBERLY, clean flame, the secondary-burn ring at the top | **Kling i2v** from the product photo at night |
| 6 | 9–12 | Medium, tripod: he sits, braces, eyes shut; nothing; one eye opens | Seedance |
| 7 | 12–15 | Wide, locked-off: {So in 2009…}; the friends exchange a look; one fans the fire hopefully | Seedance, ≤3 visible faces |
| 8 | 15–17.5 | Macro, locked: a marshmallow toasting golden over the flame (it is still a real fire) | Kling i2v; slow browning only |
| 9 | 17.5–20 | End card: "EMBERLY. Nobody moves seats." | Real product photo |

- **Physics check:** smoke follows the draft, which is real; the wind is written once and kept in every shot (FIXED GEOGRAPHY). The EMBERLY shot shows a calmer flame and the secondary-burn jets the real product has. Night and firelight hide artifacts (doc 42 rule 12). No fire tricks.
- **Audio map:** crackle and pops throughout the first half; 0.5 s a cough; 2, 4, 5.5 s chair scrapes; laughs under shot 4; 6.5 s a cleaner, quieter crackle with no pops; 12 s the story line; 13 s a long collective silence; 15 s marshmallow sizzle; 17.5 s sonic logo.
- **Models and cost:** Seedance 2.5 r2v 20 s (refs: three friends, backyard plate at night, old fire ring) $31.84; Kling ×2 $0.95; stills 9 $2.70; **total ≈ $35.50**.
- **Claim check:** "low-smoke" or the client's measured wording; the "before" fire ring is a generic open fire, never a competitor's product.

### C7 · STOWAWAY (compression carry-on) — "The Sizer" (15 s)

- **Idea:** at a boarding gate, an agent slaps the metal bag sizer: "In the box." The traveller's soft carry-on looks overstuffed. She pulls two compression straps; the bag slims; it slides into the sizer with a finger of space. The agent, suspicious, pulls a tape measure. It fits. Behind her, a man with a hard shell starts unpacking shoes onto the carpet.
- **Hook (0–1 s):** a palm slapping the metal sizer, a clang.
- **Punchline (product-caused):** the test happens where the fear happens (O4's logic); the competitor's shell becomes the "before".
- **Built on:** O4 (Béis at the counter), O5 (packing ASMR), N6 (studio beats lifestyle in travel).

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Low, locked over the sizer: the agent's palm slaps the frame | Seedance; unbranded gate, invented airline |
| 2 | 1.5–3 | Medium, tripod: the traveller, calm; her bag bulging; the queue sighs | Seedance |
| 3 | 3–5 | Insert, slider: two compression straps pulled; the bag slims 3–4 cm | **Real insert preferred**; else Kling i2v with first/last frames of the real product |
| 4 | 5–7 | Side wide, tripod: the bag slides into the sizer and settles flat | Seedance; rolls on wheels, never slides through metal |
| 5 | 7–9 | Close on the agent: eyes narrow; she pulls out a tape measure | Seedance |
| 6 | 9–11 | Insert: the tape against the bag | Real insert or comp (numbers are text) |
| 7 | 11–13 | Medium: the agent waves her on; behind her, the man kneels and unpacks shoes from a hard shell | Seedance, ≤3 people |
| 8 | 13–15 | End card: "STOWAWAY. Fits the box." + dimensions | Real product photo |

- **Physics check:** fabric compression shown only from real-product first/last frames; wheels roll; the sizer is rigid. No airline names or liveries (§4.3).
- **Audio map:** 0.0 s metal slap and clang; 1.5 s gate PA murmur (unintelligible); 3 s strap zip-zip; 5 s wheels on carpet, a soft thump; 7.5 s tape-measure zip; 11 s a gruff sigh; 13 s sonic logo.
- **Models and cost:** Seedance 2.5 r2v 15 s $23.88; Kling ×2 shots × 2 takes $1.90; stills 8 $2.40; **total ≈ $28.20**.
- **Claim check:** "fits the sizer on most US carriers" with exact dimensions, never "fits every airline".

### C8 · NORTHBOUND (insulated tumbler) — "Day Three" (15 s)

- **Idea:** 5 a.m. on day three of a lake camping trip. Everyone's cooler ice died yesterday. Inside a dark tent, a hand shakes a NORTHBOUND tumbler: **ice rattles**. Outside, four tent zippers open one after another; four heads emerge and turn toward the sound. He sips. The cooler beside him holds floating cans in warm water. He shakes it again; four heads turn in sync.
- **Hook (0–1 s):** sound first: the ice rattle in near-darkness, a blue dawn glow on the tent wall.
- **Punchline (product-caused):** the rattle (proof the ice survived) wakes the whole camp, rule of three, then the synced head-turn.
- **Built on:** O1 (ice rattle as proof), O3 (rigid object, one trick), N5 (studio work wins outdoor).

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Inside the tent, locked-off at sleeping-bag height: a hand shakes the tumbler; dawn blue on nylon | Seedance; rattle on the shake frame |
| 2 | 1.5–3 | Exterior wide, tripod on the lakeshore: four tents in mist, still water | Seedance; mist hides the water |
| 3 | 3–4.5 | Close, locked: tent zipper #1 opens, a head pops out | Seedance |
| 4 | 4.5–6 | Same framing, quick: zippers #2 and #3, heads out | Seedance (rule of three) |
| 5 | 6–8 | Medium, slider: the communal cooler, lid open, floating cans in warm water, "DAY 3" super | Seedance; still water surface |
| 6 | 8–10.5 | Medium, tripod: he steps out, sips from the tumbler; brushed steel, no condensation | **Kling i2v** insert for the tumbler in hand |
| 7 | 10.5–13 | Wide: he shakes it once more; all four heads turn in sync toward him | Seedance; deadpan hold |
| 8 | 13–15 | End card: tumbler on a log, "NORTHBOUND. Ice on day three.*" with the test-condition footnote | Real product photo |

- **Physics check:** the tumbler never sweats (vacuum-insulated, §3); the ice is only heard, never seen melting or regrowing; no liquid level change on camera (doc 41); tent zippers move in one direction and the fabric drapes under gravity. All camera positions are tripods, a slider and a locked-off camera inside a tent.
- **Audio map:**
  - 0.0 s: **ice rattle** ×3 shakes (the hook), very dry and close.
  - 1.5 s: lake dawn room tone, one loon call.
  - 3 s, 4.5 s, 5.2 s: zipper ×3, rising in pitch.
  - 6 s: a can bumps another in the cooler water.
  - 8.5 s: one sip.
  - 10.5 s: rattle again; 11 s four sleeping-bag rustles in sync.
  - 13 s: silence 0.5 s → sonic logo.
- **Models and cost:** Seedance 2.5 r2v 15 s (refs: camper, four friends as two group refs, lakeshore plate, tents) $23.88; Kling insert ×2 $0.95; stills 8 $2.40; **total ≈ $27.20**.
- **Claim check:** "*Ice after 72 h at 21 °C ambient, lid closed" from the client's own test; without it, the end card becomes "Still rattling."

### 6.1 Ranking

| Rank | Concept | Why |
|---|---|---|
| 1 | **C8 NORTHBOUND "Day Three"** | Outdoor is where studio work wins (N5) and where creatives refresh every 20 days (Season plan). The proof is one diegetic sound, the format of the 98.6M-view Stanley post. No animal, no baby, no face carries a claim. Rule-of-three + synced head turn is a clean deadpan punchline. $27 |
| 2 | C2 GRITTO "Round 12" | Pets reward product shots (index 72, 74 d life). All Kling i2v from real photos: the safest way to put a dog on screen. $10 |
| 3 | C6 EMBERLY "Musical Chairs" | Night and fire hide artifacts; owner-character comedy (O6). Needs claim discipline on "smokeless" |
| 4 | C1 ROAMLY "The Regular" | Strongest story; more moving parts (street, three people, UI comps) |
| 5 | C4 HUSHLING "Floorboard" | The best baby concept because the baby is never shown; heist grammar |
| 6 | C7 STOWAWAY "The Sizer" | Proof at the pain point; needs a real compression insert |
| 7 | C3 TRAILHOUND "Mud Season" | Good reveal; mud and dog-in-car need care |
| 8 | C5 CLAMPY "Unemployed" | Cheapest ($8) and charming; the joke leans on the dog's acting |

---

## 7. QA gate additions for this niche

Add to doc 44 §10 and doc 49 §7:

- [ ] Every animal close-up started from a real photo (Kling i2v); one animal per frame; no generated eating, chewing, licking or shaking.
- [ ] Fur moves with motion; exactly four legs, each paw plants; frame-by-frame check at 2 fps for vanishing limbs.
- [ ] No baby or child face anywhere; nursery imagery follows safe sleep; car-seat and carrier use is correct.
- [ ] Steel drinkware shows no condensation; ice only shrinks or is only heard.
- [ ] Waterproof, compression and folding proofs are real inserts or real-product first/last frames.
- [ ] Wind direction (smoke, flames, hair, fur) is written once and holds across cuts.
- [ ] Every on-screen claim has a footnote from the client's test sheet (§4.4).
- [ ] Product shot of the hero product within 2 s; 4–6 stills exported for the pet product-shot long-runners.

---

## Sources

**Measured TikToks** (links in §1.1): @danimarielettering 7301724587488759070; @stanleybrand 7440150786262207787; @owala 7416476002915847467; @beis 7493972519230197038; @teresalauracaruso 7383715370680683822; @mattslyon 7301760492765236523; @ryannpurvis 7444587803788299538; @simonsits 7505899204942826782; @thefarmersdog 7546703680335039757; @bark 7535571440104443166; @weratedogs 7485796233026538783; @fridababy 7484310762932981022 and 7534085339267321119; @lovevery 7322255462299143467; @_brookehoppe 7418969310833560875; @longliveai 7610794090732522774.

**Metadata-only TikToks checked** (not in the table): @fridababy 7489125511591972126 (197K); @myboyrudder × BarkBox 7301463223289597230 (176K); @owalalife 7221286918594546986 (263K); @thefarmersdog 7475858752982322474, 7432770902372224298, 7118048222018358574 (1–18K); @bradystauffer15 × Solo Stove 7554157676545051918 (1.0M, 15.7 %); @beis 7257568703473093934 (207K); @lovevery 7482926094832733483 (4K); @fi.dogs 7325856233154432287, 7314155609618697515 (0.5–26K); @yotoplay 7473459437001297185 (450K, 0.8 %); @stanleybrand 7322145117194767646 (417K), 7410821056115510570 (64K), @stanley1913 7476552311888760110 (135K); @life.with.kora × Wild One 7369037843861130513 (161K); @wildonepets 7268420964176661806 (2.5K).

**YouTube** (search listing, §1.2): IDs -k6www7PtkY, RCOjrIh34FQ, fw62oxIMk9E, qJ8r1wY8LNY, IAIo-pUDl0s, L0Nmxq1VW00, HLi9_ZVoxaw, TXpdx725OGM, Xsd3ioWbjVo, wCuE6sIPTG4, 5qfxm4eMXY4, -hFSlOtgvx0, 6v8uAtSg_FQ, ur71TAjHjP0, 1mpZZZkrgAU, dJxt7IQRoq0, BHRiPrvQBA4, Le5oVm0lth0, Z2aptryxYiI, a47L1wlP_-E. URL form `https://youtu.be/<id>`.

**Benchmarks and data:**
- Benly Q1 2026: [overview](https://benly.ai/benchmarks/q1-2026), [pets & animals](https://benly.ai/benchmarks/q1-2026/pets-animals), [family & parenting](https://benly.ai/benchmarks/q1-2026/family-parenting), [sports & recreation](https://benly.ai/benchmarks/q1-2026/sports-recreation), [travel & hospitality](https://benly.ai/benchmarks/q1-2026/travel-hospitality)
- [Motion library: BarkBox](https://motionapp.com/library/barkbox); [Motion library: pets index](https://motionapp.com/library/pets)
- [APPA 2026 report](https://americanpetproducts.org/news/the-american-pet-products-association-appa-releases-2025-state-of-the-industry-report); [Petfood Industry $158B](https://www.petfoodindustry.com/pet-food-market/market-trends-and-reports/news/15825309/us-pet-industry-hits-158-billion-in-2025); [Gen Z ownership](https://www.petfoodindustry.com/pet-food-market/market-trends-and-reports/news/15741428)
- [Ad Age: Farmer's Dog Ad Meter](https://adage.com/article/special-report-super-bowl/farmers-dog-wins-usa-todays-super-bowl-2023-ad-meter/2472121); [Campaign CMO 50: Katie Iles](https://www.campaignlive.com/article/cmo-50-2023-katie-iles/1835615); [Vimeo debrief](https://vimeo.com/blog/post/farmers-dog-debrief)
- Stanley: [designrush](https://news.designrush.com/stanley-finds-marketing-breakthrough-in-viral-video), [WXYZ](https://www.wxyz.com/stanley-offers-woman-a-new-car-after-viral-video-of-cup-surviving-fire), [Hardware Connection](https://thehardwareconnection.com/?p=11396), [Bigblue](https://www.bigblue.co/blog/unveiling-stanleys-hype-quenchers-impact-tiktok-viral)
- Owala: [Salt Lake Tribune](https://www.sltrib.com/news/business/2025/03/22/how-utah-family-made-owala-water)
- Frida: [Marketing Brew](https://marketingbrew.com/stories/2024/04/30/how-frida-found-organic-success-through-unfiltered-content), [Modern Retail 2026](https://www.modernretail.co/marketing/frida-baby-faces-backlash-over-the-use-of-sexual-innuendos-in-marketing/), [The Mary Sue](https://www.themarysue.com/mom-discovers-frida-baby-products-at-walmart-with-disturbing-packaging-we-are-not-mad-enough/)
- Agency claims: [Redefine Web](https://redefineweb.com/blog/proven-ppc-for-pet-brands-grow-subscription-revenue/), [Top Growth Marketing](https://topgrowthmarketing.com/services/pet-marketing-agency/), [The Good Marketer: Zoomadog](https://thegoodmarketer.co.uk/case-study/zoomadog/)

**AI realism:** [Kapwing, best AI video models for realistic animals (Feb 2026)](https://www.kapwing.com/resources/best-ai-video-models-for-realistic-animals/); [NBC: Toys"R"Us Sora ad](https://www.nbcnews.com/tech/internet/toys-r-us-ai-video-ad-controversy-explained-commercial-rcna159030); [Decrypt](https://decrypt.co/237017/ai-film-toys-r-us-sora-controversy); doc 43 (model rules), doc 41, doc 42.

**Policy and law:**
- Pets: [FDA animal food labeling and claims](https://www.fda.gov/animal-veterinary/animal-foods-feeds/animal-food-labeling-and-pet-food-claims); [AAFCO human grade guidelines](https://www.aafco.org/wp-content/uploads/2023/01/Appendix_A_Human_Grade_Guidelines.pdf); [Faegre Drinker on NAD 7523](https://www.faegredrinker.com/en/insights/publications/2026/5/advertising-alert-sit-stay-substantiate-nad-review-of-pet-food-claims-provide-important-reminders-when-comparing-products); [Kilpatrick](https://ktslaw.com/blog/kilpatrick-ad-vantage/2026/5/barking-up-the-right-tree); [Petfood Industry on Sundays](https://www.petfoodindustry.com/pet-food-marketing-and-branding/news/15822732/nad-rules-on-sundays-for-dogs-advertising-claims); [Meta live animals](https://transparency.meta.com/policies/ad-standards/restricted-goods-services/live-endangered-nonendangered-animals); [Meta drugs](https://transparency.meta.com/policies/ad-standards/restricted-goods-services/drugs-pharmaceuticals/)
- Baby/kids: [4A's safe sleep](https://www.aaaa.org/guidance-safe-sleep-advertising/); [Morgan Lewis on the Safe Sleep for Babies Act](https://www.morganlewis.com/pubs/2022/12/safe-sleep-for-babies-what-you-need-to-know-if-you-offer-infant-sleep-products); [crib ads study](https://news.childrensmercy.org/reuters-crib-ads-often-show-babies-in-unsafe-sleep-settings/); [FDA Owlet warning letter](https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/warning-letters/owlet-baby-care-inc-616354-10052021); [Owlet Dream Sock De Novo](https://www.businesswire.com/news/home/20231109884987/en/); [CARU revised guidelines](https://bbbprograms.org/media-center/prd/CARU-revised-guidelines-for-advertising-to-children); [CARU AI guidance](https://www.mediapost.com/publications/article/410029/caru-issues-guidance-for-ai-aimed-at-kids.html); [TikTok NA handbook](https://ads.tiktok.com/help/article/ad-policy-handbook-north-america?lang=en); [TikTok 2026 change log](https://ads.tiktok.com/help/article/tiktok-ad-policy-change-log-2026)
- Outdoor: [Arnold & Porter: Stanley dismissal](https://www.arnoldporter.com/en/perspectives/news/2026/04/arnold-porter-wins-dismissal-of-consumer-class-action-against-stanley-drinkware); [Bloomberg Law](https://news.bloomberglaw.com/litigation/stanley-tumbler-maker-sued-again-over-alleged-lead-advertising); doc 45 §5 (weapons, stunts, impersonation, AI labels, FTC reviews, NY synthetic performers)
