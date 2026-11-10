# Sweep 4 (2026-11-10): creative science, statistics for ad tests, AI tooling

## תקציר בעברית
1. **סטטיסטיקה של בדיקה ב-$120.** להציץ כל יום ולהכריז "עובד" ברכישה הראשונה הוא הדרך הבטוחה לטעות: מוצר גרוע (CPA כפול מנקודת האיזון) מראה לפחות רכישה אחת תוך 6 ימים ב-93% מהמקרים. הכלל שחושב ב-`phase1/test_stop_rule.py` (פואסון, קריאה אחת בסוף כל מנה): מנה 1 $120, ממשיכים רק עם ≥ 5 רכישות; מנה 2 $120, מועמד ל-M1 רק עם ≥ 3 רכישות. מוצר טוב באמת (CPA ≤ 80% מנקודת האיזון) עובר ב-77%, מוצר גרוע ב-7%, הוצאה צפויה על מוצר גרוע $136, מקסימום $240. הציצה מותרת רק כדי **להרוג** (אין הוספה לסל עד $60), לא כדי לאשר.
2. **קריאייטיב.** המדד הראשון: hook rate = צפיות 3 שניות ÷ חשיפות; חציון Meta ≈ 28% (12,347 מודעות, ינואר–מרץ 2026, ספק); מתחת ל-25% מחליפים את הפתיח. UGC-סגנון מול מלוטש: +33% CTR באותו מאגר, אבל מבקר רציני מראה שרוב הסטטיסטיקות של UGC הן של ספקים, ושסוג ה-Hook חשוב יותר מהפורמט. אווטאר AI איכותי מגיע ל-26–36% hook מול 28–38% לאדם; הפער הוא בהמרה, במיוחד מעל $75. במחיר $5–20 לסרטון, AI מנצח בכמות הווריאציות, לא באיכות.
3. **זכויות וגילוי.** Higgsfield: לא תובע בעלות על הפלט ולא מגביל שימוש מסחרי; הפלט שלך עשוי להיות זהה לשל אחרים; אתה אחראי לאישורי זכויות ולדמויות אמיתיות. Canva: פלט מותר לשימוש מסחרי לפי תנאי ה-AI; תבניות/מלאי עם רישיון נפרד. FTC: המלצה חייבת לשקף ניסיון אמיתי; "אי אפשר לדבר על חוויה עם מוצר שלא ניסית"; תוצאות חריגות דורשות גילוי של התוצאה הטיפוסית. לכן: אווטאר AI מותר כ**מציג** (demo, הסבר), אסור כ**לקוח מרוצה**. כל סרטון AI נושא תווית/כתובית "AI-generated".
4. **כלים ב-$0.** הכלים הגנרטיביים של Meta בתוך Ads Manager (רקעים, הרחבת תמונה, וריאציות טקסט, ומ-2026 גם טקסט על מדיה וקריינות) חינמיים ומסומנים אוטומטית. Canva ו-Adobe Express כבר מחוברים לסשן (MCP) וניתן לייצר בהם סטטיקה וסרטונים קצרים. Higgsfield ($19/חודש, 270 קרדיטים ≈ 10–30 קליפים של 5 שניות) נכנס רק אחרי שמוצר עבר את מנה 1.

## Searched
Peeking and sequential testing (Evan Miller; Johari, Pekelis, Walsh); sample-size rules of thumb; hook-rate benchmarks; UGC vs produced; AI avatars vs human; Higgsfield, Canva, Adobe terms (Adobe page 404, Canva terms 403: Canva quoted from its product page via search); FTC Endorsement Guides FAQ; Meta's generative-AI ad tools (press coverage; no primary page); Schwartz awareness stages.

## Sources in this area (19; primary 4; dissenting 3)
Carried: S-07, S-08, S-29, S-30, S-36, S-82. New S-90..S-102. Primary: S-91 (peer-reviewed), S-92 (Higgsfield terms), S-94 (FTC), S-36 (FTC rule). Dissenting: S-90/S-91 (against daily reads), S-96 (UGC claims are vendor-sourced), S-82 (carried).

## Findings and rules

### A. Statistics: the stop rule for a $120 product test
- "Repeated significance testing always increases the rate of false positives"; stopping at the first significant look yields ~26% false positives at a nominal 5% (S-90). Sequential inference needs always-valid p-values or a pre-fixed sample (S-91).
- Rules of thumb "50 conversions per variant" (S-101) cost $1,000–2,000 per variant at a $20 CPA and are out of reach. The program therefore accepts a coarse test that finds only clearly good products.
- Computed (phase1/test_stop_rule.py, inputs: price $40, contribution 0.556, breakeven CPA $22.2; "good" = CPA ≤ 0.8×breakeven, "bad" = 2×breakeven):

| Rule | P(pass both | good) | P(pass both | bad) | E[spend | bad] | Max spend |
|---|---|---|---|---|---|
| T1 $120 ≥ 5 purchases → T2 $120 ≥ 3 purchases (chosen) | 0.77 | 0.07 | $136 | $240 |
| T1 $120 ≥ 3 → T2 $180 ≥ 5 | ≈0.8 | ≈0.1 | higher | $300 |
| naive "kill only at zero purchases in $120" | 1.00 | 0.93 keep | — | — |
| daily peeking, "confirmed" at first purchase | — | 0.93 | — | — |

- Rule ST1: one read per tranche, at its end, logged in reads.log. Rule ST2: an early kill is allowed on a pre-stated rule only (no add-to-cart by $60; CTR < 0.5% at 2,000 impressions), never an early pass. Rule ST3: the thresholds are recomputed per product from its price and contribution before registration, with the script output pasted into the registry entry. Rule ST4: a product that passes both tranches is "M1 candidate", not "passing": M1 needs ≥ 30 orders and ≥ 14 days reconciled (frame §2.6).

### B. Creative metrics and benchmarks
- Hook rate (3-s plays ÷ impressions): median 28% on Meta across 12,347 ads, Jan–Mar 2026 (S-95, vendor); other vendors 23–30% median, < 25% "kill the hook", 40%+ elite (S-98). Rule CR1: a creative under 20% hook rate at 1,000 impressions is replaced by a new hook, not a new product (early-kill class, allowed by ST2).
- UGC-style vs polished: CTR 1.88% vs 1.41% on Meta in the same dataset (S-95); Opascope: "Almost every stat traces back to a vendor publishing its own case studies"; hook type > creator relationship > placement > format; storytelling visual hooks beat talking heads 86–14 in its accounts (S-96, dissenting, self-caveated). Rule CR2: the two creatives in a test differ by hook type first (demo-problem vs storytelling), not by polish.
- AI avatars: hook 26–36% (high quality) vs 28–38% human; robotic avatars 14–20%; conversion gap grows above $75 price; AI video $5–20 vs $150–400 creator (S-97, S-99, all vendor-adjacent). Rule CR3: AI video is used for product demos, text-on-screen and voiceover; an AI "person" never speaks as a customer.

### C. Rights and disclosure
- Higgsfield: "Company does not claim ownership of any of your Inputs or Outputs, nor does it restrict your commercial use of Outputs"; "Other users may receive an Output that is similar or possibly identical to yours"; you must hold rights to any "name, likeness, voice" used; updated Oct 23, 2026 (S-92).
- Canva: AI outputs usable "for any purpose, including personal or commercial projects" under its AI Product Terms; templates and stock carry their own licence (S-93, via product page; terms page refused).
- FTC: "You can't talk about your experience with a product if you haven't tried it"; exceptional results require stating "the generally expected results"; disclosures best "included in the video itself" (S-94). FTC rule bans testimonials by people who do not exist (S-36).
- Meta labels AI-made ad media automatically where it detects it; no evasion (S-30, S-08).
- Rule D1: every AI-generated video or image used in an ad carries an on-screen "AI-generated visuals" line and is not stripped of C2PA metadata. Rule D2: no testimonials, reviews or "customer" voices unless from a real, verified buyer with written consent. Rule D3: no "was $X" prices unless the product sold at $X for a documented period (FTC, Meta S-77).

### D. Tooling for creatives at $0 first
| Tool | Cost | Rights | Use | Evidence |
|---|---|---|---|---|
| Meta gen-AI tools in Ads Manager (backgrounds, image expansion, text variations; 2026: text-on-media, voiceover) | $0 | Meta's; auto "AI info" label | first static variants and copy | S-100 (press), S-30 |
| Canva (MCP in session) | plan-dependent; AI clips limited per month on Pro | commercial OK per AI terms | statics, short clips, captions | S-93 |
| Adobe Express (MCP in session) | plan-dependent | Adobe page refused; Unknown | statics | — |
| Higgsfield Starter | $19/mo, 270 credits ≈ 10–30 five-second clips by model | commercial OK; outputs non-exclusive | demo b-roll after a product passes T1 | S-07, S-92 |
Rule TL1: no paid creative tool before a product passes tranche 1. Rule TL2: each tool's rights line is re-read within 30 days of use (expiry rule).

### E. Copy frameworks (curriculum, not rules)
Schwartz's five awareness stages and market sophistication (S-102, secondary summaries of the 1966 book): a cold Meta audience is "problem aware" at best; the hook names the problem, the page proves the solution; in a sophisticated market (saturated product) the claim must be a mechanism, not a bigger promise. Applied: the ad brief template in the registry asks "which awareness stage, which sophistication stage" before any hook is written.

## Candidates extracted
| Candidate | Family | Mechanism | Cost | Prior | Negative |
|---|---|---|---|---|---|
| A-c3: storytelling visual hook beats product-demo hook on cost per purchase for the same product | creative | pattern-break + narrative holds attention past 3 s | 2 arms inside a tranche-2 budget | 50% (S-96 says 86/14 in its accounts; vendor) | demo wins by more than noise |
| A-c4: AI-generated demo b-roll with text-on-screen matches a phone-shot demo on hook rate | creative/AI | attention is driven by motion and claim, not by production | $19 Higgsfield + 1 arm | 50% | hook rate < 20% vs ≥ 25% for phone-shot |

## Research synthesis block
```
Searched: peeking/sequential testing; sample sizes; hook-rate benchmarks; UGC vs produced; AI avatars; AI tool rights; FTC endorsement rules; Meta gen-AI tools.
Strongest sources: Johari et al. (S-91, peer-reviewed); Evan Miller (S-90, classic with numbers); Higgsfield terms (S-92, primary); FTC Endorsement Guides FAQ (S-94, primary); Benly dataset (S-95, largest sample found, vendor).
Candidates found: 2 (A-family); 0 previously failed.
Patterns: every creative "benchmark" is a vendor's; the only robust rule is to fix the read in advance; hook type matters more than production value; AI wins on volume and cost, loses on trust; rights are fine, disclosure is the gate.
Failure modes: daily peeking (93% false keep on bad products); AI "customers"; stripped AI labels; fake "was" prices; buying tools before a product exists.
Cumulative P(any passes): n/a.
Assumptions and gaps: stop-rule inputs are placeholders until per-product numbers exist; Adobe terms unread; Canva terms page refused; Meta gen-AI tool list unverified on a primary page.
```

## Top-up (2026-11-10, later): statistics and AI tooling to minimum depth

### Statistics (area total 15 sources; primary 3: S-91, S-146, S-155; dissenting 2: S-82, S-147)
- Multiple creatives in one tranche are a multiple-comparison family. Spotify's analysis of 1,296 experiments: Holm and Hommel gain "roughly 4–5 percentage points in ship rate" over Bonferroni when the family holds only success metrics, and collapse to Bonferroni when guardrails are wrongly included (S-146, arXiv Apr 2026). Platform docs recommend Bonferroni for families of three or fewer, Benjamini-Hochberg beyond (S-148, S-149). Rule ST5: a tranche with 2–3 creatives uses Bonferroni on the creative comparison (if one is ever made); the product-level decision uses the pooled count, so no correction is needed there.
- Sequential methods are not free: always-valid inference needs "nearly 85% larger sample size" for the same power; SPRT about 22% more (S-147). Rule ST6: the program keeps fixed reads at the end of each tranche (ST1); no sequential engine at this budget.
- Small counts: Wald intervals "unreliable when event counts are below 10 to 15"; the Garwood exact interval "has guaranteed coverage and is the standard choice" (S-150, S-155). Rule ST7: every result file reports purchases with a Garwood 95% interval; a CPA is reported as spend ÷ [interval], never as a point.

### AI tooling (area total 19 sources; primary 4: S-92, S-156, S-158, S-159; dissenting 2: S-160, S-163)
- Consumers: only 45% of US Gen Z/Millennials feel positive about AI-generated ads vs 82% of executives who think they do (n=505 / 104, Oct 2025–Jan 2026, S-156); 73% say disclosure would raise or not change purchase likelihood; over half want disclosure for AI video or images. Animoto: 83% suspect they have seen AI video, 36% say it lowers brand perception; cues: robotic gestures 67%, unnatural voices 55% (S-157, press release; page refused). NielsenIQ: AI ads rated "annoying," "boring," "confusing"; a "negative halo effect" on the brand (S-160, secondary).
- Platform: Meta labels AI images via C2PA/IPTC and requires disclosure of realistic AI video or audio in organic posts, and "may apply penalties if they fail to do so" (S-158, Meta newsroom, updated Apr 2025). Metadata can be stripped by tools and even by platforms (S-163), which is why the program's on-screen line (D1) does not depend on metadata.
- Rights: ElevenLabs free users "may only use the Services for non-commercial purposes"; paid users may; output non-unique; voice cloning only with rights (S-159, Oct 9, 2026). Kling's free tier blocks commercial use per roundups; Runway/Luma pricing conflicts across sources (S-162, vendor). AI product images that misrepresent the product fall under ordinary deception rules; a disclosure duty for enhanced images is disputed among vendors (S-164, S-165).
- Rules: TL3: no free-tier AI output in an ad (non-commercial licences). TL4: on-screen AI line regardless of metadata; never strip C2PA. TL5: first tests use AI for b-roll, backgrounds and captions, not synthetic faces or voices; a human-voice or no-voice variant is the control. TL6: product images on the page are photos of the real sample; AI only for backgrounds and never for the product itself.
