# מערכת הפנייה: תבניות, פולואפים, תסריטי תגובה, שיחה, הצעה וחוזה

> **מה במסמך:** כל הטקסטים שצריך כדי להריץ את 30 הימים של [V3 §3](../validation/V3-demand-and-alternatives.md). הסברים בעברית, כל מה שהלקוח רואה באנגלית (חוץ מגרסת המייסדים הישראלים).
> **איך משתמשים:** כל תבנית מסומנת בקוד (למשל `DTC-A`, `DTC-FU1`). את הקוד רושמים בעמודה `message_variant` ב-[tracker.csv](tracker.csv), כדי שביום 14 נדע איזו גרסה עובדת.
> **משתנים:** `{first_name}`, `{brand}`, `{product}`, `{N}` (מספר מודעות פעילות ב-Meta Ad Library), `{format}` (למשל "static testimonial cards"), `{link}` (לינק לספק או לתיק עבודות), `{your_name}`, `{studio}`.

---

## 0. כללי ברזל לכל פנייה

1. **לפני כל מייל: 5 דקות מחקר.** פותחים את [Meta Ad Library](https://www.facebook.com/ads/library/) של המותג, סופרים מודעות פעילות, ורושמים פורמט אחד חוזר. זה ה-`{N}` וה-`{format}`. בלי זה המייל גנרי ושיעור התגובה יורד ל-1–3% (V3 §3.3).
2. **10 המובילים מקבלים ספק על המוצר שלהם** (12 שניות, PRODUCT LOCK לפי פרק 16). השאר מקבלים לינק לתיק העבודות + פריים מותאם אחד (ספק קל, V2 §6.2 #2).
3. **ספק עם מותג אמיתי נשלח רק בפרטיות.** לא מפרסמים, לא מעלים ל-YouTube ציבורי (Unlisted/Loom בלבד), ומוחקים אם ביקשו (פרק 10 §4).
4. **מחיר כבר במייל הראשון** ב-DTC (V3 §3.5): זה מסנן ומקצר את המשפך. בסוכנויות: "first 3 free".
5. **CTA קל.** אם ביום 14 יש תגובות בלי שיחות, מחליפים את ה-CTA ל-"Want 3 free hooks for your best-selling SKU?" (V3 §3.4).
6. **CAN-SPAM:** כתובת פיזית (או PO Box) בחתימה, שורת opt-out, נושא לא מטעה. שולחים מדומיין משני מחומם (למשל `try{studio}.com`), לא יותר מ-30–40 מיילים ביום לתיבה.
7. **אין "AI" בשורת הנושא.** AI מופיע בגוף, בכנות, כחלק מהתהליך.

**חתימה סטנדרטית (באנגלית):**
```
{your_name}
{studio} · Performance ad creative for DTC brands
Boca Raton, FL · {studio}.com
{mailing address}
Not relevant? Reply "no" and I won't follow up.
```

---

## 1. DTC: מייל קר, 3 גרסאות

**מתי משתמשים במה:** שבוע 1 מחלקים 50/50 בין A ל-B (על אותו סוג רשימה). C נשמרת לשבוע 3 אם A ו-B מתחת ל-3% (V3 §3.2), או למותגים שה-Ad Library שלהם כמעט ריק.

### `DTC-A`: Andromeda + ספק (הגרסה הבסיסית מ-V3 §3.5, מהודקת)
```
Subject: 3 new hooks for {product}

Hi {first_name},

{brand} has {N} ads live on Meta right now, mostly {format}. Since Andromeda,
Meta groups look-alike ads and rewards 8–15 distinct concepts per ad set.
Most brands ship 2–4 a month.

I made a 12-second concept for {product} using your real packaging:
{link}

I run a 5-day Creative Test Sprint: 12 ads (4 angles × 3 hooks), $750.
If none beats your control within 14 days of spend, the next sprint is half off.

Worth a look?

{signature}
```

### `DTC-B`: "הפער" (מבוסס סקירה של המודעות שלהם, בלי מילה על Andromeda)
```
Subject: {brand}'s ads — one gap I noticed

Hi {first_name},

I went through {brand}'s live Meta ads. Your "{one ad hook/line you saw}" ad is strong,
but almost every variation uses the same angle: {angle they overuse, e.g. "ingredient list"}.

Angles I'd test next, pulled from your own reviews:
1. {angle 1 — e.g. "the 3pm slump at work"}
2. {angle 2 — e.g. "gym bag essential"}
3. {angle 3 — e.g. "hot-car test"}

Here's angle 1 as a 12s ad with your real {product}: {link}

I build these in batches of 12 (4 angles × 3 hooks) in 5 days, $750,
with a beat-your-control guarantee. Want the other two?

{signature}
```

### `DTC-C`: CTA קל, בלי מחיר (לשבוע 3, או אם יש תגובות בלי שיחות)
```
Subject: free hooks for {product}?

Hi {first_name},

Quick one: I make ad creative for DTC brands and I'm building a few case studies
in {category}.

If you send me your best-selling SKU, I'll make 3 hook variations for it
(9:16, ready for Meta), free, no call needed. If one of them beats what you're running,
we can talk about a sprint. If not, you keep them.

Interested?

{signature}
```
**הערה:** C נותן עבודה חינמית. **מקסימום 3 הוקים** (V3 §3.4, "לא עושים עבודה חינמית גדולה מ-3 מודעות"), ורק למותג עם 3–20 מודעות פעילות (סימן שיש תקציב).

### פולואפים (לכל הגרסאות)

**`DTC-FU1` (יום 4, באותו thread):**
```
Hi {first_name}, bumping this in case it got buried.

One thing I didn't mention: the sprint includes the angle brief (pulled from your reviews
and current ads), so even if you only keep 2 of the 12 ads, your team gets 4 tested angles
to brief against.

Here's the {product} concept again: {link}

{your_name}
```

**`DTC-FU2` (יום 9, breakup קצר, באותו thread):**
```
Hi {first_name}, I'll stop here so I'm not cluttering your inbox.

If creative volume becomes a priority (Q4, a launch, a new SKU), just reply "sprint"
and I'll send a slot. Happy to keep the {product} concept either way: {link}

{your_name}
```

### DM (אינסטגרם / לינקדאין) למייסד

**`DTC-DM-IG` (אחרי שהמייל נשלח; קצר, בלי לינק בהודעה הראשונה אם החשבון חדש):**
```
Hey {first_name}! Big fan of what you're doing with {brand}. I made a quick 12s ad
concept for {product} with your real packaging. Mind if I send it here?
```
אחרי "sure": שולחים את הלינק + משפט אחד: `"It's one of 4 angles I'd test. I run 12-ad sprints for $750 if it's useful."`

**`DTC-DM-LI` (בקשת חיבור, עד 300 תווים):**
```
Hi {first_name}, I make performance ad creative for DTC brands (12 new concepts in 5 days).
Made a short concept for {product} I think you'd like. Happy to connect and share.
```
אחרי שאישר:
```
Thanks for connecting! Here's the {product} concept: {link}
It's built around {angle}. If it's interesting, I run a 5-day, 12-ad sprint ($750)
with a beat-your-control guarantee. No pressure either way.
```

### `DTC-HE`: מייסד ישראלי (עברית)
**מייל/DM ראשון:**
```
נושא: 3 הוקים חדשים ל-{מוצר}

היי {שם},
ראיתי ש-{מותג} רץ עכשיו עם {N} מודעות ב-Meta בארה"ב, רובן {פורמט}.
מאז העדכון של Andromeda, מטא מקבצת מודעות דומות ומתגמלת 8–15 קונספטים שונים לכל ad set.

אני ישראלי שגר בבוקה רטון ובונה קריאייטיב למודעות למותגי DTC, עם המוצר האמיתי שלכם, לא "בערך".
הכנתי לכם קונספט של 12 שניות: {לינק}

יש לי ספרינט של 5 ימים: 12 מודעות (4 זוויות × 3 הוקים), ב-$750.
אם אף אחת לא מנצחת את ה-control שלכם תוך 14 יום, הספרינט הבא בחצי מחיר.

שווה הצצה?
{שם} · {סטודיו}
```
**פולואפ יום 4 (עברית):**
```
היי {שם}, מקפיץ למקרה שזה נקבר. הספרינט כולל גם בריף זוויות (מתוך הביקורות והמודעות שלכם),
כך שגם אם תשאירו רק 2 מתוך 12, יש לכם 4 זוויות בדוקות. הקונספט שוב: {לינק}
```
**פולואפ יום 9 (עברית):**
```
אני עוצר כאן כדי לא להעמיס. אם בהמשך תצטרכו נפח קריאייטיב (Q4, השקה, מוצר חדש), תכתבו "ספרינט" ואשלח מועד. בהצלחה!
```
**טון:** דוגרי, בלי "מקווה שהמייל מוצא אותך בטוב". שורה אחת של חיבור ("גם אני ישראלי בפלורידה") מספיקה. את הספק והקבצים שולחים באנגלית (הקהל אמריקאי).

---

## 2. סוכנויות: white-label

**רשימה:** ‏15 סוכנויות קטנות בדרום פלורידה (ניהול מודעות, סושיאל, שיווק למד-ספא/מסעדות) + 25 ארציות (כולל מ-[us-dtc §4](../prospects/us-dtc.md), אבל בעדיפות נמוכה לסטודיו הגדולים, V2 §6.2 #3). איש קשר: Founder / Head of Creative / Account Director.

### `AG-1`: מייל ראשון
```
Subject: white-label ad creative for your clients (first 3 free)

Hi {first_name},

I produce white-label performance video ads for agencies: product-accurate,
9:16 + 4:5, captions and safe zones done, 72-hour turnaround. No branding from me,
your client relationship stays yours, and I'll sign your NDA.

$150 per ad (min. 5), or $1,200/month for 10.

Send me one real client brief and I'll deliver 3 ads free, so you can judge
the quality on a live account before paying anything.

Samples: {portfolio link}

{signature}
```

### `AG-FU1` (יום 4)
```
Hi {first_name}, quick follow-up. Agencies usually use this in one of two ways:
1) add a "creative refresh" line item to existing ad-management retainers, or
2) say yes to clients asking for more video without adding headcount.

The 3 free ads offer stands. One brief is enough: {portfolio link}

{your_name}
```

### `AG-FU2` (יום 9)
```
Hi {first_name}, last note from me. If a client ever asks for "more creative" and your
team is at capacity, reply "brief" and I'll turn 3 ads around in 72 hours, on the house.

{your_name}
```

### `AG-LI`: לינקדאין
```
Hi {first_name}, I'm a white-label ad creative producer in Boca (video ads for agencies'
DTC and local clients, 72h turnaround). Would love to connect. First 3 ads are free if you
ever want to test a partner.
```

### סוכנות מקומית בדרום פלורידה (תוספת לגוף המייל)
```
I'm based in Boca Raton, so I'm happy to meet for coffee and walk through a client brief in person.
```

---

## 3. מקומי בבוקה (אופורטוניסטי בלבד)

**מתי:** רק לידים חמים (הכרות, אירוע, הפניה) ועסקים מנישות "מוצר ונוף": יאכטות, רכבי יוקרה, השקות מסעדות, פרויקטים חדשים בנדל"ן (V1 §8.3 #7). **לא** מד-ספא בלי היברידי עם הבעלים מול המצלמה.

### `LOCAL-DM` (אינסטגרם, אחרי שהגבת בכנות על 2 פוסטים שלהם)
```
Hi! I'm a neighbor in Boca, I make short video ads for local businesses.
I had an idea for {business} — {one-line concept, e.g. "your boat at golden hour,
cut like a movie trailer"}. Can I send you a 10-second sketch? Free, no strings.
```
**פולואפ (יום 5):**
```
Here it is: {link}. If you like it, I do a local pilot: 6 short ads for your
Reels/Meta, $750. If not, no worries, keep the sketch.
```
**מפגש פנים אל פנים (YP Mixer, Expo):** "I make scroll-stopping video ads for local businesses. Can I show you a 10-second example on my phone?" ואז להראות את "Real vs AI" (ראה [public-posts.md](public-posts.md)).

---

## 4. תסריטי טיפול בתגובות

### 4.1 "Too expensive" / "No budget right now"
```
Totally fair. Two options:
1) The first three founding-client sprints are $500 instead of $750. I have {X} left.
2) If even that's not the right time, send me your best-selling SKU and I'll make 3 hooks free.
   If one beats your control, we talk. If not, you keep them.
For context: one UGC creator video usually runs $150–300 with shipping and wait time.
The sprint is 12 ads in 5 days, about $62 per ad, plus the angle brief.
```
**בראש:** לא יורדים מתחת ל-$500 ולא נותנים יותר מ-3 מודעות חינם (V3 §3.4).

### 4.2 "We do creative in-house"
```
Makes sense, most brands at your stage do. Where we usually help in-house teams:
volume spikes (launches, Q4, new SKUs) and new angles your team hasn't had time to test.
Think of the sprint as 12 extra shots on goal your team doesn't have to produce.
Your designers keep the brand; we feed them tested angles.
Would a one-off sprint before {next launch / BFCM} be useful?
```

### 4.3 "Is this AI?" / "We don't want AI ads"
```
Good question, and yes: we use AI in production, the way a post house uses CGI,
to build scenes and variations around your product fast. A few things that matter:
- Your product is locked from your own photos and label files and checked frame by frame.
- No fake testimonials or AI "customers," ever. That's an FTC issue and a trust issue.
- AI content is labeled per Meta/TikTok rules. Studies suggest disclosure doesn't hurt
  trust; hiding it does.
- If you'd rather keep people real, we do hybrids: your real footage or UGC, with AI only
  for the openings, worlds and transitions.
The metric we care about is the same as yours: does it beat the control.
```

### 4.4 "Send examples" / "Send more info"
```
Here are 3 that fit {brand}'s category: {link1}, {link2}, {link3}
(Demo brands are fictional; client work is shared privately with permission.)
Even better: tell me your best-selling SKU and I'll make a 10-second concept with your
actual packaging this week. That's the most honest example I can give you.
```
**בראש:** "Send examples" הוא לעיתים קרובות דחייה מנומסת. התשובה הכי חזקה היא ספק על המוצר שלהם.

### 4.5 "Not right now" / "Maybe next quarter"
```
Understood. Want me to check back in {month}? I'll send one concept for whatever
you're launching then. No follow-ups before that.
```
→ ב-tracker: `notes = recontact {date}`.

### 4.6 "Who else have you worked with?"
```
I'm early: the studio launched this fall, which is exactly why the guarantee and the
founding-client price exist. I won't show you made-up logos. What I can show you is
work on your own product before you pay: {link}.
```

---

## 5. תסריט שיחה של 15 דקות

**מטרה אחת:** ספרינט בתשלום או "שלח הצעה". לא להציג את כל השירותים.

| דקה | שלב | מה אומרים / שואלים |
|---|---|---|
| 0–1 | פתיחה | "Thanks for the time. I'd like to understand how you're testing creative right now, and then tell you if a sprint makes sense. If it doesn't, I'll say so. Sound good?" |
| 1–6 | אבחון (הם מדברים 70%) | 1. "Roughly what are you spending on Meta/TikTok a month?" · 2. "How many new ads do you launch in a typical month? Who makes them?" · 3. "What's your current control, and how long has it been the winner?" · 4. "Which angles have you tested? Which flopped?" · 5. "What's coming up: launch, BFCM, new SKU?" · 6. "What would a good result from a test look like for you?" |
| 6–9 | שיקוף + הצעה | "So you're shipping ~{X}/month, your control is {Y} weeks old, and {launch} is coming. Here's what I'd do: a sprint with 4 angles: {angle 1 from their words}, {angle 2}, {angle 3}, {angle 4}. 3 hooks each, 12 ads, 5 days." |
| 9–11 | מחיר + הבטחה | "$750, or $500 as a founding client. If none of the 12 beats your control on CTR or thumb-stop within 14 days of spend, the next sprint is half off. You'd share a screenshot at day 14 and we review together." |
| 11–13 | התנגדויות | לפי §4. שאלה חשובה: "Is there anything that would stop you from running these ads next to your control?" |
| 13–15 | סגירה | "If it sounds right, I'll send a one-page proposal and invoice today. You send product files and reviews, and I deliver by {date}. Want to do that?" → אם "צריך לחשוב": "What's the one thing you'd need to know to decide?" ולקבוע תאריך מעקב. |

**מיד אחרי השיחה:** הצעה (§6) תוך שעתיים, עדכון tracker (`call_booked=Y`, `proposal_sent=Y`).
**אל תעשה:** לא לתת פריסה של מחירי Growth/Scale אם לא שאלו. לא להבטיח ROAS. לא להגיד "AI" כמילת מכירה.

---

## 6. תבנית הצעה בעמוד אחד (באנגלית)

```
STUDIO NAME — Creative Test Sprint Proposal
Prepared for: {brand} · {first_name} {last_name} · {date}
Valid until: {date + 7 days}

THE GOAL
Find 1–2 new winning ads for {product} that beat your current control ({control ad name})
on CTR or thumb-stop rate, and learn which angles to scale.

WHAT YOU GET
• 12 video ads: 4 angles × 3 hooks, 6–15s each
• Formats: 9:16 (Reels/TikTok/Stories) + 4:5 (Feed) = 24 files
• Burned-in captions, safe-zone checked, licensed music
• Angle brief (1 page): the 4 angles, why each, and what to test next
• One revision round (within 3 business days of delivery)
• File naming ready for your media buyer: {BRAND}_{ANGLE}_{HOOK}_{FORMAT}_v1

THE ANGLES (from our call)
1. {angle 1} — hook ideas: …
2. {angle 2} — …
3. {angle 3} — …
4. {angle 4} — …

TIMELINE
Day 0: payment + assets received → Day 1: angle & hook sign-off →
Day 4–5: delivery → Day 5–19: you run the test → Day 19: results review call

WHAT WE NEED FROM YOU
Product photos (front/back/45°), label/packaging files, logo, approved claims list,
10–20 customer reviews, current top 3 ads (or screenshots).

INVESTMENT
Creative Test Sprint: $750 (founding client: $500), 100% upfront.
Guarantee: if none of the 12 ads beats your control on CTR or thumb-stop rate within
14 days of spend (fair test: each ad gets meaningful spend next to the control),
your next sprint is 50% off. You share an Ads Manager screenshot at day 14.

AFTER THE SPRINT (optional)
Growth: $1,800/mo — 20 ads/month · Scale: $3,500/mo — 40–50 ads + 2 hero films/month.

AI & COMPLIANCE
We use AI tools in production. Your product is reproduced from your own references and
QA'd frame by frame. No synthetic testimonials. AI content labeled per platform rules.

To accept: reply "approved" and pay the invoice: {payment link}
```

---

## 7. מתווה הסכם שירות (Service Agreement Outline)

> ⚠️ **זה מתווה, לא חוזה.** חובה שעורך דין אמריקאי (פלורידה) יעבור עליו לפני השימוש הראשון. עלות סבירה לבדיקה חד-פעמית של תבנית: $300–800. הסעיפים בעברית מסבירים, הנוסח לדוגמה באנגלית.

| # | סעיף | מה הוא אומר | נוסח לדוגמה (EN) |
|---|---|---|---|
| 1 | **Parties & Scope** | מי, מה, איזו חבילה. ה-SOW (ההצעה מ-§6) מצורף ומהווה חלק מההסכם | "Studio will deliver the Deliverables described in the attached Statement of Work (SOW)." |
| 2 | **Fees & Payment** | ספרינט: 100% מראש. חודשי: מראש בתחילת כל חודש. איחור: עצירת עבודה | "Fees are due before work begins. Monthly plans renew automatically unless cancelled with 30 days' written notice." |
| 3 | **Revisions** | סבב תיקונים אחד תוך 3 ימי עסקים. שינוי בריף אחרי אישור הזוויות = עבודה חדשה | "One round of revisions is included if requested within 3 business days of delivery. Changes to approved angles are billed as new work." |
| 4 | **Client Materials & Warranties** | הלקוח מתחייב שיש לו זכויות על כל מה שהוא שולח (לוגו, תמונות, מוזיקה, ביקורות) ושהטענות מבוססות | "Client warrants that all testimonials, reviews, statistics, before/after results and claims supplied for use in ads are truthful, substantiated, and from real customers with consent." (פרק 16 §10) |
| 5 | **AI Disclosure** ⭐ | גילוי מלא שמשתמשים ב-AI, ושהתוכן יסומן לפי מדיניות הפלטפורמות. הלקוח מתחייב לא להסיר תוויות/מטא-דאטה C2PA | "Client acknowledges that Studio uses generative AI tools in producing the Deliverables. AI-generated or AI-altered people, voices or realistic scenes will be disclosed per applicable platform policies (e.g., Meta 'AI info', TikTok AIGC label). Client will not remove such labels or embedded content credentials. Studio will not create synthetic testimonials or present AI-generated people as real customers." |
| 6 | **Likeness & Voice Consent** ⭐ | אין שימוש בפנים/קול של אדם אמיתי בלי הסכמה בכתב (release). אין שיבוט של אנשי ציבור. אין קטינים סינתטיים. אווטאר רק מורשה | "Studio will use the likeness or voice of a real, identifiable person only with that person's prior written consent and release, supplied by Client or obtained by Studio. Studio will not create digital replicas of public figures or minors. Client is responsible for consents for any people appearing in materials Client supplies." |
| 7 | **Ownership & License** | אחרי תשלום מלא: הלקוח מקבל בעלות/רישיון מלא על התוצרים הסופיים. קבצי פרויקט ופרומפטים נשארים של הסטודיו אלא אם נקנו. הערה: זכויות יוצרים על תוכן AI טהור לא תמיד מוגנות בארה"ב (US Copyright Office), ולכן מנסחים "assigns whatever rights it holds" | "Upon full payment, Studio assigns to Client all rights Studio holds in the final Deliverables. Client acknowledges that purely AI-generated elements may not be eligible for copyright protection. Working files, prompts and templates remain Studio's property unless purchased." |
| 8 | **Portfolio Use** | הסטודיו לא מציג עבודה של הלקוח בפומבי בלי אישור בכתב | "Studio may show Deliverables publicly only with Client's written approval." |
| 9 | **Guarantee** | ההבטחה מנוסחת בדיוק: מה נמדד, תוך כמה זמן, מה התנאי (תקציב בדיקה הוגן, צילום מסך), ומה התרופה (50% הנחה על הספרינט הבא, לא החזר כספי) | "If no Sprint ad outperforms Client's designated control ad on CTR or thumb-stop rate within 14 days of spend, Client may purchase one additional Sprint at 50% off within 60 days, upon providing Ads Manager screenshots. This is Client's sole remedy." |
| 10 | **No Performance Promise** | אין התחייבות ל-ROAS/מכירות. הפלטפורמה יכולה לדחות מודעות | "Studio does not guarantee sales, ROAS or ad approval by any platform." |
| 11 | **Compliance Responsibility** | הלקוח אחראי לאישור סופי של טענות (בעיקר תוספי תזונה/קוסמטיקה, FDA/FTC) ולתוויות אלכוהול/גיל | "Client is responsible for final review and approval of all claims and regulatory statements before publishing." |
| 12 | **Confidentiality** | NDA הדדי, כולל נתוני Ads Manager | |
| 13 | **Limitation of Liability** | תקרה = הסכום ששולם ב-3 החודשים האחרונים | "Studio's total liability is limited to fees paid in the 3 months before the claim." |
| 14 | **Indemnity** | הדדי: הלקוח על חומרים שסיפק ועל טענות; הסטודיו על הפרה ידועה של זכויות צד ג' בעבודה שלו | |
| 15 | **Term & Termination** | חודשי: 30 יום הודעה. ספרינט: מסתיים במסירה | |
| 16 | **Governing Law** | פלורידה, מחוז Palm Beach | |
| 17 | **White-label addendum (לסוכנויות)** | אין מיתוג של הסטודיו, אין פנייה ישירה ללקוחות של הסוכנות (non-solicit, 12 חודשים), הסוכנות אחראית להסכמות וגילוי מול הלקוח שלה, וסעיפים 5–6 עוברים הלאה ללקוח הסופי | "Agency will pass through Sections 5–6 to its clients." |

**טיפ:** לחתימה, PandaDoc/Dropbox Sign/Bonsai בחינם או זול. לתשלום: Stripe Payment Link (פרק 13).
