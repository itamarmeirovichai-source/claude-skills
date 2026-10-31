# 6 מודעות דמו לתיק העבודות

> **מה במסמך:** 6 קונספטים מוכנים להפקה: 3 למותגי DTC **פיקטיביים** ו-3 "ספק" של פרודיה על קטגוריה, **בלי שום מותג אמיתי**. לכל אחד: זווית, הוק, משפט התפנית (פרק 17 §6.1), רשימת שוטים עם timecodes, פרומפטים מדויקים (תמונה, Seedance 2.5, Kling 4.0), רפרנסים נדרשים, ו-spec עריכה ל-reel-studio.
> **כללים שחלים על כולם (פרקים 16–17):**
> 1. **PRODUCT LOCK** בכל פרומפט וידאו שיש בו מוצר. המוצר מגיע מרפרנס, לא מתיאור.
> 2. **Silent plate:** אין טקסט, כתוביות, לוגואים או סימני מים בג'נרציה. **כל הטקסט נוסף בעריכה** (ב-spec). התווית של המוצר היא הטקסט היחיד בפריים, והיא מגיעה מגיליון B.
> 3. **"ידיים בחוץ, טקסט בעריכה, מגע בחיתוך"** (פרק 17 תקציר #5). אף שוט לא דורש יד שאוחזת במוצר.
> 4. **אין עדויות, אין לפני/אחרי, אין טענות תוצאה.** הטענות על התוויות הפיקטיביות הן "עובדות תווית" בלבד.
> 5. **כרטיס סיום = packshot אמיתי** (קומפוזיט, פרק 16 שלב 8E), לא פריים AI.
> 6. כל דמו פומבי נושא בעריכה את השורה "AI-generated demo · fictional brand" (או "category parody · not a real brand").
>
> **שמות המותגים הפיקטיביים לא נבדקו מול סימני מסחר.** לפני פרסום: חיפוש ב-[USPTO](https://tmsearch.uspto.gov/) ובגוגל. אם יש מותג אמיתי בשם זה בקטגוריה, משנים שם.

---

## 0. איך מייצרים מוצר פיקטיבי (פעם אחת לכל מותג, ~45 דקות)

1. **עיצוב התווית בכלי עיצוב** (Figma/Canva), לא במודל: הטקסט המדויק מהטבלה בכל דמו, PNG שטוח 2000px. זה **גיליון B** (תווית פרושה) והמקור של הלוגו לכרטיס הסיום.
2. **גיליון A (צורה)** במודל תמונה (Nano Banana Pro / GPT Image 2.5), ב**לי טקסט**:
```
Product reference sheet on a plain white background, 3 views side by side: front, 45-degree, back.
[OBJECT DESCRIPTION]. Blank label area (no text, no logo, no graphics), even studio light,
no shadows on the background, orthographic product photography, 1:1 scale between views.
No text anywhere in the image.
```
3. **החלת התווית:** בכלי התמונה (edit mode), עם גיליון A + גיליון B כרפרנסים:
```
Apply the flat label artwork from @label exactly onto the blank label area of the product in @shape.
Wrap it naturally around the curvature. Do not change, translate, re-letter or simplify any text.
Keep the product shape, proportions and materials exactly as in @shape. Plain white background.
```
   בודקים זום 200% על כל אות. אם משהו נשבר: מקמפזים את ה-PNG ב-Photoshop/Photopea במקום לנסות שוב (פרק 16 שלב 7).
4. **3 רפרנסים לשמור:** `product_shape.png` (גיליון A), `product_label.png` (גיליון B), `product_hero.png` (המוצר עם התווית, חזית). + `logo.png` שקוף, + `packshot_real.png` 1080×1920 (המוצר על רקע המותג, לכרטיס הסיום).

**שורת PRODUCT LOCK (מוסיפים לסוף כל פרומפט וידאו עם מוצר, פרק 16 §3.4):**
```
@product_label is the close-up of the front label. Use it as the AUTHORITY for the exact wording,
typeface, weight, color, line breaks and layout of the label. The label reads: "[EXACT TEXT]".
PRODUCT LOCK: @product_shape = shape and proportions; @product_label = label artwork and text (authority);
@product_hero = overall look. The product must match them exactly in every frame — same silhouette,
proportions, cap, materials, colors, label layout and logo size/position. Rigid object: it never
bends, melts, stretches or changes size. Do not redesign, rename, translate or add text.
Exactly one product unless stated.
NEGATIVE: rigid product, constant size, no melting, no bending, no extra products, no duplicated or
mirrored text, no gibberish letters, no logo drift, no color shift, no hands touching the label,
no on-screen text, no captions, no watermark.
```
בהמשך המסמך זה מופיע כ-`[PRODUCT LOCK]`.

**שמות קבצים:** כל קליפ נשמר בשם שמופיע ב-spec, למשל `launch/specs/media/demo1/s1_hook_glass.mp4`. התיקייה `media/` ו-`out/` לא נכנסות ל-git (`specs/.gitignore`).
**רינדור:** `cd launch/specs && python3 ../../../../skills/reel-studio/scripts/reelstudio.py render demo1.json --preset draft`, אחר כך `grid`, ואז final. ל-4:5: `--preset feed`.
**בדיקה שבוצעה:** כל 6 ה-specs עברו `plan` (exit 0) עם קבצי placeholder מ-`demo-media`, ו-demo1 רונדר כ-draft ונבדק ב-grid.

---

## DEMO 1: DRIFTLINE Electrolyte (פיקטיבי) · `specs/demo1.json` · 15s

| | |
|---|---|
| **מוצר** | אבקת אלקטרוליטים בסטיקים. קופסה מט בצבע חול (#E9DFC9) עם פס ליים (#A8D84E), סטיק כסוף-מט עם אותו פס |
| **תווית (טקסט מדויק)** | `DRIFTLINE` / `ELECTROLYTE DRINK MIX` / `KEY LIME SALT` / `1,000 mg ELECTROLYTES · 0 g SUGAR` / `12 STICKS` |
| **לוגו** | wordmark ‏DRIFTLINE בגרוטסק דחוס, מעליו קו גל דק אחד |
| **זווית** | Florida heat: הבעיה מורגשת (חום), המוצר הוא "המתג" |
| **הוק** | "92° OUTSIDE." → "38° IN THIS GLASS." (פרק 17 §6.3, הוק מספרים) |
| **משפט התפנית** | "We think we're watching a heatwave, but actually it's frost spreading from one glass, because of DRIFTLINE." |
| **חוק** | משקה, לא תוסף רפואי. רק עובדות תווית. בלי "cures dehydration" |

**רשימת שוטים**
| TC | ביט | שוט | שיטה | סיכון |
|---|---|---|---|---|
| 0:00–0:02 | Hook | מאקרו של כוס מים קרים עם קרח, טיפות עיבוי זולגות, רקע של חוף מסנוור באוור חם, heat haze | I2V מ-keyframe | A |
| 0:02–0:04 | Setup | טיילת לאורך החוף בצהריים, אוויר רוטט, דמות מגב בפוקוס רך מנגבת מצח (בלי פנים) | T2V | B: דמות מרחוק |
| 0:04–0:06 | Turn | אבקה בצבע ליים נשפכת מלמעלה לתוך הכוס (מקור מחוץ לפריים, **בלי ידיים**), המים הופכים לליים חיוור | I2V | B |
| 0:06–0:09 | Escalation | כפור מתפשט מבסיס הכוס על שולחן העץ ועל הזכוכית, ה-heat haze ברקע נעלם | I2V | A: שבירת פיזיקה |
| 0:09–0:12 | Product hero | הקופסה וסטיק אחד על אבן מכוסה כפור, עיבוי, push-in איטי | I2V hero (פרק 16 §3.5) | B→A עם קומפוזיט |
| 0:12–0:15 | CTA | packshot אמיתי + לוגו + CTA | POST | A |

**Keyframe (תמונה), שוט 1:**
```
SHOT 1 KEYFRAME — 9:16 vertical, photoreal commercial still.
Subject: a tall clear glass of ice water on a weathered white wooden table, heavy condensation
droplets on the glass, two ice cubes. Action frozen at: a single droplet halfway down the glass.
Setting: Florida beachfront at noon, bright white sand and turquoise water far behind, visible heat
haze shimmer. Composition: glass centered at x 50%, lower-middle third, headroom for captions in
the top 15% and bottom 20%.
Light: hard midday sun from top-left, bright specular highlights on the glass. Lens: 100mm macro,
shallow depth of field, background blown out warm. Grade: bleached warm highlights, cyan accents.
No text, no logos, no watermark.
```

**Seedance 2.5 (MASTER-A, כל השוטים 1–5 בג'נרציה אחת; אפשר גם שוט-שוט):**
```
ASSET BINDING:
@Image1 = Shot 1 keyframe (glass on the beach table) — composition and light reference.
@product_shape, @product_label, @product_hero = the DRIFTLINE box and stick pack — exact shape,
sand-colored matte box with a lime stripe; never redesign or re-letter.

GLOBAL STYLE: premium beverage commercial, 9:16, photoreal, bleached warm Florida light turning cool
and frosty after the turn, crisp digital, 24fps, no on-screen text, no logos other than the
product's own label, no watermark.

SCENE: On a scorching Florida beach day, a glass of water turns lime as electrolyte powder falls in,
and frost spreads out from it until the heat itself seems to stop.

TIMELINE:
0:00-0:02 Shot 1: macro of the glass from @Image1, a droplet slides down, heat haze ripples behind.
100mm, locked-off, slow 4% push-in. Hard cut.
0:02-0:04 Shot 2: wide shot of a beach boardwalk at noon, air shimmering, a person seen from behind
in soft focus wipes their forehead with a forearm. 35mm, slight handheld drift. Hard cut.
0:04-0:06 Shot 3: top-down macro: fine pale-lime powder streams into the glass from above the frame,
swirling and dissolving, the water turning pale lime. No hands, no packet visible. 100mm, locked-off.
Cut on the swirl.
0:06-0:09 Shot 4: low angle on the glass; white frost crystals spread from its base across the wooden
table and climb the glass; behind it the heat haze stops and the sky turns crisp. 50mm. Camera:
slow pull back, ending on a wide of the frosted table. Hard cut.
0:09-0:12 Shot 5: the DRIFTLINE box with one stick pack leaning on it, on a frost-covered stone,
label facing camera, cool condensation, soft mist at the base. 85mm. Camera: slow 6% push-in,
product perfectly still, ends on a held frame.

PHYSICS: powder falls in a smooth stream; frost grows like time-lapse ice, never cracking the glass;
the glass never moves.
AUDIO: none (music and SFX added in edit).
CONSISTENCY LOCKS: same glass in shots 1, 3, 4; exactly one box and one stick in shot 5.
[PRODUCT LOCK] — label reads: "DRIFTLINE / ELECTROLYTE DRINK MIX / KEY LIME SALT /
1,000 mg ELECTROLYTES · 0 g SUGAR / 12 STICKS"
```

**Kling 4.0 (שוט 5, hero, הכי בטוח לתווית):**
```
@Image1 (product_hero composited on frosted stone) is the first frame. Locked-off tripod, 85mm.
The camera slowly pushes in about 6% over 5 seconds. Only the environment moves: frost crystals
creep slowly across the stone, a faint cold mist drifts at the base, condensation beads on the box.
The box and stick stay perfectly still, label facing camera, text sharp and unchanged for the whole
shot. Ends on a held frame. No cuts, no text, no music.
[PRODUCT LOCK]
```
**רפרנסים נדרשים:** product_shape, product_label, product_hero, keyframe שוט 1, keyframe שוט 5 (המוצר מקומפז על אבן כפור), logo.png, packshot_real.png.
**קבצים ל-spec:** `media/demo1/s1_hook_glass.mp4`, `s2_setup_heat.mp4`, `s3_turn_pour.mp4`, `s4_frost_spread.mp4`, `s5_hero_pack.mp4`, `logo.png`, `packshot_real.png`, ‏`media/music.wav`.

---

## DEMO 2: VELLUM Barrier Serum (פיקטיבי) · `specs/demo2.json` · 14s

| | |
|---|---|
| **מוצר** | בקבוק זכוכית חלבית 30ml עם טפטפת, פקק אלומיניום מוברש זהב-שמפניה, תווית שמנת (#F3EEE6) עם טקסט פחם |
| **תווית** | `VELLUM` / `BARRIER SERUM` / `CERAMIDES + SQUALANE` / `30 ml · 1 fl oz` |
| **זווית** | Texture proof: מראים "קלילות" במטאפורה, **בלי עור ובלי פנים** |
| **הוק** | "This is what “lightweight” actually looks like." |
| **משפט התפנית** | "We think a drop will crush a feather, but it doesn't even bend it, because VELLUM is that light." |
| **חוק** | קוסמטיקה: אין טענות תוצאה, אין לפני/אחרי. "Sinks in" היא תיאור טקסטורה. ללקוח אמיתי: רק טענות מאושרות |

**רשימת שוטים**
| TC | ביט | שוט | שיטה | סיכון |
|---|---|---|---|---|
| 0:00–0:03 | Hook | טפטפת זכוכית תלויה בפריים (בלי יד), טיפה אחת שקופה-זהובה מתארכת ונופלת בסלואו (velocity "hero") | I2V | B |
| 0:03–0:06 | Setup/Turn | הטיפה נוחתת על נוצה לבנה מאוזנת על קצה, הנוצה **לא מתכופפת** | I2V | A: שבירת פיזיקה מכוונת |
| 0:06–0:09 | Proof | הטיפה מתפשטת לשכבה זגוגית דקה על משי ונבלעת בלי להשאיר כתם | I2V | A |
| 0:09–0:12 | Hero | הבקבוק על אבן רטובה עם השתקפות, אור בוקר רך, push-in | I2V hero | B→A |
| 0:12–0:14 | CTA | packshot אמיתי + לוגו + CTA | POST | A |

**Keyframe, שוט 2:**
```
SHOT 2 KEYFRAME — 9:16 vertical, photoreal macro still.
Subject: a single white feather balanced upright on its tip on a pale silk surface, a perfectly round
clear golden droplet resting on its outer vane. Action frozen at: the droplet just landed, the vane
not bent at all. Setting: minimal studio, cream backdrop. Composition: feather centered x 50%,
middle third, headroom top 15% and bottom 20%.
Light: large soft window light from the left, thin warm rim from behind. Lens: 100mm macro, f/4.
Grade: cream, champagne and soft white, gentle contrast.
No text, no logos, no watermark.
```

**Seedance 2.5:**
```
ASSET BINDING:
@Image1 = Shot 2 keyframe (feather and droplet) — composition and light.
@product_shape, @product_label, @product_hero = the VELLUM bottle — frosted glass, champagne-gold
dropper cap, cream label; never redesign or re-letter.

GLOBAL STYLE: luxury skincare commercial, 9:16, photoreal macro, cream and champagne palette,
soft morning light, slow and calm, 24fps, no on-screen text, no logos except the bottle's own label,
no watermark, no people, no skin.

SCENE: A single drop of serum is so light that a feather doesn't bend under it, then it melts into
silk without a trace.

TIMELINE:
0:00-0:03 Shot 1: a glass dropper pipette hangs vertically in frame (held by nothing visible); a single
clear golden drop slowly stretches from its tip and falls. 100mm macro, locked-off. Slow motion. Hard cut.
0:03-0:06 Shot 2: as in @Image1: the drop lands on the vane of a white feather balanced on its tip;
the feather does not bend or wobble. 100mm, locked-off, very slow push-in. Soft dissolve.
0:06-0:09 Shot 3: extreme macro: the drop spreads into a thin glassy film across pale silk and
disappears into the weave, leaving the silk dry and unmarked. Top-down, 100mm. Camera: slow drift
right. Soft dissolve.
0:09-0:12 Shot 4: the VELLUM bottle stands on wet pale stone, soft reflection below, dropper cap on,
label facing camera, morning light sweeping slowly across the background. 85mm. Camera: slow 5%
push-in, bottle perfectly still, ends on a held frame.

PHYSICS: the drop is viscous but light; the feather never moves; silk ripples only slightly.
AUDIO: none (added in edit).
[PRODUCT LOCK] — label reads: "VELLUM / BARRIER SERUM / CERAMIDES + SQUALANE / 30 ml · 1 fl oz"
```

**Kling 4.0 (שוט 1–2 ב-keyframes):**
```
Keyframe 1 (0s): glass dropper tip, a golden drop forming, cream background, macro.
Keyframe 4 (1.5s): the drop has detached, falling, elongated.
Keyframe 7 (3s): the drop lands on a white feather balanced on its tip [@Image1], vane not bent.
Keyframe 10 (5s): same frame, drop still resting, faint light shimmer across it.
Motion: very slow, weightless. Camera locked-off with a faint push-in. No hands. No text.
```
**רפרנסים:** product_shape, product_label, product_hero, keyframes שוטים 2 ו-4, logo.png, packshot_real.png.
**קבצים:** `media/demo2/s1_hook_drop.mp4`, `s2_feather.mp4`, `s3_absorb_silk.mp4`, `s4_hero_bottle.mp4`, `logo.png`, `packshot_real.png`.

---

## DEMO 3: PAWSTEAD Hip & Joint Chews (פיקטיבי) · `specs/demo3.json` · 14s

| | |
|---|---|
| **מוצר** | צנצנת פלסטיק עבה בצבע ירוק-יער (#2F4A3A), מכסה עץ בהיר, תווית קרם עם איור קו של כלב |
| **תווית** | `PAWSTEAD` / `HIP & JOINT CHEWS` / `GLUCOSAMINE + CHONDROITIN` / `FOR DOGS` / `90 SOFT CHEWS` |
| **זווית** | טקס יומי: "הטיפול שהוא לא נותן לך לשכוח" (טעם ו-compliance יומי, לא תוצאה) |
| **הוק** | "He waits by the cabinet at 7:02. Every day." |
| **משפט התפנית** | "We think he's waiting for breakfast, but actually he's waiting for his PAWSTEAD chew." |
| **חוק** | תוסף לחיות: **אין טענות יעילות** ("fixes hips", "pain-free"), אין "לפני: צולע / אחרי: רץ". הכלב שמח כי זה טקס, לא כי "נרפא" |

**רשימת שוטים**
| TC | ביט | שוט | שיטה | סיכון |
|---|---|---|---|---|
| 0:00–0:02.5 | Hook | גולדן רטריבר מבוגר (פנים אפורות) יושב ובוהה בארון מטבח סגור, אור בוקר, זווית נמוכה. השעה רק בכיתוב | I2V | B: עקביות כלב |
| 0:02.5–0:04.5 | Setup | קלוז-אפ: האוזניים מזדקפות (על צליל מכסה, בסאונד) | I2V | B |
| 0:04.5–0:07 | Turn | הצנצנת על השיש, מכסה פתוח לידה, חטיפים נראים, push-in | I2V hero | B→A |
| 0:07–0:09.5 | Proof | חטיף אחד על רצפת עץ, האף של הכלב נכנס לפריים ומרחרח (בלי ידיים) | I2V | B |
| 0:09.5–0:11.5 | Payoff | הכלב פוסע בשמחה במסדרון מואר, זנב מכשכש, גב למצלמה | I2V | B |
| 0:11.5–0:14 | CTA | packshot אמיתי + לוגו + CTA | POST | A |

**Keyframe "כלב" (רפרנס זהות, משתמשים בו בכל השוטים):**
```
Character reference sheet: a senior golden retriever, about 10 years old, grey-white muzzle and
eyebrows, warm golden coat, slightly wavy ears, kind dark eyes, green fabric collar with no tag text.
Three views on plain white: front, side, three-quarter. Photoreal, even studio light. No text.
```
**Keyframe, שוט 1:**
```
SHOT 1 KEYFRAME — 9:16 vertical, photoreal lifestyle still.
Subject: the senior golden retriever from @dog sits upright, staring intently up at a closed
white kitchen cabinet. Action frozen at: head tilted slightly, ears relaxed.
Setting: bright modern kitchen, white oak floor, morning sun through a window. Composition: dog in
lower half at x 40%, cabinet upper right, headroom top 15% and bottom 20%.
Light: low warm sun from camera left, soft fill. Lens: 35mm from dog's eye level. Grade: warm, airy.
No text, no clocks, no logos, no watermark.
```

**Seedance 2.5:**
```
ASSET BINDING:
@dog = the senior golden retriever (identity, coat, muzzle, collar) — identical in every shot.
@Image1 = Shot 1 keyframe (dog at the cabinet) — composition and light.
@product_shape, @product_label, @product_hero = the PAWSTEAD jar — forest-green jar, light wood lid,
cream label; never redesign or re-letter.

GLOBAL STYLE: warm pet-brand commercial, 9:16, photoreal, morning sunlight, gentle and funny,
24fps, no on-screen text, no clocks with numerals, no logos except the jar's own label, no watermark,
no human hands or faces.

SCENE: Every morning an old golden retriever waits by the same cabinet for the treat he never forgets.

TIMELINE:
0:00-0:02 Shot 1: as in @Image1, the dog sits perfectly still staring up at the closed cabinet, only his
eyebrows twitch. 35mm, eye level, locked-off. Hard cut.
0:02-0:04 Shot 2: close-up of the dog's head, his ears lift and he turns his head toward the sound.
50mm, shallow focus. Locked-off. Hard cut.
0:04-0:06 Shot 3: the PAWSTEAD jar on a white counter, wooden lid resting beside it, soft chews visible
inside, label facing camera, morning sun. 85mm. Camera: slow 5% push-in, jar perfectly still. Hard cut.
0:06-0:08 Shot 4: low angle on a wooden floor: a single soft chew lies there; the dog's nose enters
from the top of frame and sniffs it. 50mm, floor level, locked-off. No hands. Hard cut.
0:08-0:10 Shot 5: the dog trots happily away down a sunlit hallway, tail wagging, seen from behind.
35mm. Camera: slow follow, ends as he turns the corner.

PHYSICS: natural dog motion, relaxed gait, no jumping or running fast.
AUDIO: none (added in edit).
CONSISTENCY LOCKS: same dog in all shots; exactly one jar.
[PRODUCT LOCK] — label reads: "PAWSTEAD / HIP & JOINT CHEWS / GLUCOSAMINE + CHONDROITIN /
FOR DOGS / 90 SOFT CHEWS"
```
**Kling 4.0 (שוט 3, hero של הצנצנת):** כמו ה-hero ב-DEMO 1, עם: `"Only the environment moves: morning sunlight shifts slowly across the counter, a few dust motes float. The jar stays perfectly still..."` + `[PRODUCT LOCK]`.
**רפרנסים:** dog sheet, product_shape, product_label, product_hero, keyframes שוטים 1 ו-3, logo.png, packshot_real.png.
**קבצים:** `media/demo3/s1_hook_dog_cabinet.mp4`, `s2_ears_perk.mp4`, `s3_jar_hero.mp4`, `s4_chew_floor.mp4`, `s5_dog_hallway.mp4`, `logo.png`, `packshot_real.png`.

---

## DEMO 4 (פרודיה): "The Mattress: A Trailer" · `specs/demo4.json` · 14.7s

| | |
|---|---|
| **קטגוריה** | מזרן בקופסה. **מוצר גנרי:** קופסת קרטון חומה בלי שום הדפס, מזרן לבן עם פס תפר אפור |
| **זווית** | "If a bed-in-a-box ad were a summer blockbuster" (V2 §6.2 #8: פרודיה על קטגוריה) |
| **הוק** | מסך שחור + "THIS SUMMER" + תוף עמוק |
| **משפט התפנית** | "We think we're watching a monster movie, but actually it's a mattress unboxing." |
| **חוק** | אין שום לוגו/שם של מותג מזרנים אמיתי, אין חיקוי של טריילר מסוים או של קול קריין מוכר. כרטיסי טקסט בלבד |

**רשימת שוטים**
| TC | ביט | שוט | שיטה |
|---|---|---|---|
| 0:00–0:01.5 | Hook | שחור + "THIS SUMMER" | POST |
| 0:01.5–0:04 | Setup | קופסה על מפתן דלת בלילה, גשם כבד, ברק, זווית נמוכה אפית | T2V |
| 0:04–0:07 | Turn | דשי הקופסה מתפרצים לבד, אוויר ואבק, סלואו | I2V |
| 0:07–0:10 | Escalation | המזרן נפרש כמו יצור, ממלא חדר שינה, וילונות עפים | I2V |
| 0:10–0:12 | Payoff | גבר (פוקוס רך, גב למצלמה) נופל לאחור על המזרן בסלואו, כריות מרחפות | T2V |
| 0:12–0:14.7 | Title | "THE MATTRESS / Sleep is coming." | POST |

**Seedance 2.5:**
```
GLOBAL STYLE: epic summer blockbuster trailer, 9:16, photoreal, teal-and-orange grade, heavy
atmosphere, anamorphic lens flares, 24fps, no on-screen text, no logos or brand names anywhere,
plain unprinted cardboard box, no watermark.

SCENE: A plain cardboard box delivered on a stormy night unleashes a giant white mattress, filmed
like a monster movie.

TIMELINE:
0:00-0:02 Shot 1: low angle, a plain brown cardboard box sits on a front doorstep at night in pouring
rain, lightning flashes behind the house. 24mm, locked-off. Hard cut.
0:02-0:04 Shot 2: the box flaps burst open on their own, a blast of air and dust, slow motion.
35mm. Camera: slight push-in. Hard cut.
0:04-0:07 Shot 3: inside a dark bedroom, a white mattress with a grey seam unrolls and inflates
dramatically, filling the room, curtains blowing, lamp shades rocking. 24mm wide. Camera: slow
low-angle orbit. Hard cut.
0:07-0:09 Shot 4: a man in a grey t-shirt, seen from behind in soft focus, falls backwards onto the
mattress in extreme slow motion, pillows float up around him. 35mm. Locked-off.

PHYSICS: rain heavy and cinematic; the mattress moves like a living thing but stays a soft mattress.
AUDIO: none (added in edit).
NEGATIVE: no text, no logos, no printed box, no recognizable brand, no faces in focus.
```
**Kling 4.0 (שוט 3, keyframes):**
```
Keyframe 1 (0s): rolled white mattress on a dark bedroom floor, plastic wrap torn, moody blue light.
Keyframe 4 (1.5s): mattress half unrolled, rising, air blast lifting curtains.
Keyframe 7 (3s): mattress fully inflated, filling the frame, pillows bouncing.
Keyframe 10 (5s): wide low angle, mattress dominating the room like a monster, lightning through the window.
Motion: dramatic but soft; camera orbits slowly left. No text, no logos.
```
**רפרנסים:** keyframe לשוט 2 ולשוט 3 בלבד (אין מוצר אמיתי לנעול). **קבצים:** `media/demo4/s2_box_doorstep_storm.mp4`, `s3_box_bursts.mp4`, `s4_mattress_unfurls.mp4`, `s5_falls_back.mp4`.

---

## DEMO 5 (פרודיה): "Pans in the Wild" · `specs/demo5.json` · 14.6s

| | |
|---|---|
| **קטגוריה** | כלי בישול נון-סטיק. **מוצר גנרי:** מחבת קרמית ירוקת-מרווה בלי לוגו, ידית עץ |
| **זווית** | "If cookware ads were nature documentaries" |
| **הוק** | "THE KITCHEN. 6:14 AM." על שיש ערפילי כמו סוואנה עם עלות השחר |
| **משפט התפנית** | "We think we're watching a predator hunt, but actually it's an egg sliding off a nonstick pan." |
| **חוק** | **לא לחקות קול של קריין אמיתי** (אין voice clone של אנשי ציבור). הכיתובים בסגנון דוקו, בלי קריינות או עם TTS מקורי. אין לוגו של מותג כלי בישול |

**רשימת שוטים:** 0:00–0:02.5 שיש מטבח עם ערפל בוקר, אור זהוב, נוף "סוואנה" (T2V) · 0:02.5–0:05 ביצה מתגלגלת לאט לעבר המחבת, כמו טרף (I2V) · 0:05–0:08 מאקרו: ביצת עין מחליקה על פני המחבת בלי להידבק, רחש (I2V) · 0:08–0:10.5 "העדר": 4 מחבתות תלויות על מסילה מתנדנדות, אחת שונה בצבע (I2V) + chip בלטינית "Sartago antiadhaerens" · 0:10.5–0:12.5 hero של המחבת על אבן (I2V) · 0:12.5–0:14.6 "Wild. Nonstick. Yours." (POST).

**Seedance 2.5:**
```
ASSET BINDING:
@pan = the sage-green ceramic frying pan with a wooden handle, no logo — same pan in every shot.

GLOBAL STYLE: wildlife documentary cinematography, 9:16, photoreal, golden dawn light, long-lens
compression, subtle film grain, 24fps, no on-screen text, no logos, no watermark, no people.

SCENE: A kitchen at dawn filmed like the African savanna, where an egg meets the pan.

TIMELINE:
0:00-0:02 Shot 1: low wide shot across a marble kitchen counter at dawn, morning mist drifting over it
like grassland, the @pan silhouetted in the distance against the golden window. 200mm long lens.
Camera: very slow push-in. Hard cut.
0:02-0:04 Shot 2: an egg rolls slowly across the counter toward the @pan, stops, wobbles nervously.
Counter-level, 135mm. Locked-off. Soft dissolve.
0:04-0:07 Shot 3: macro on the @pan: a sunny-side-up egg glides effortlessly across the pan's surface
in one smooth slide, butter sizzling, nothing sticks. 100mm. Camera: slow track following the egg.
Hard cut.
0:07-0:09 Shot 4: four identical frying pans hang from a rail and sway gently in unison like grazing
animals; one sage-green @pan among dull grey ones. 85mm, locked-off.

PHYSICS: the egg slides smoothly without tearing; pans sway slowly.
AUDIO: none (added in edit).
NEGATIVE: no text, no brand logos, no hands, no people.
```
**Kling 4.0 (שוט 5, hero):** `@pan on a mossy wet stone at dawn, mist drifting, locked-off 85mm, slow 5% push-in, the pan perfectly still, dew drops on the rim, no text, no logos.`
**רפרנסים:** תמונת `pan` (גיליון A בשיטה של §0, בלי תווית). **קבצים:** `media/demo5/s1_kitchen_dawn.mp4`, `s2_egg_rolls.mp4`, `s3_egg_glides.mp4`, `s4_herd_rail.mp4`, `s5_pan_hero.mp4`.

---

## DEMO 6 (פרודיה): "Eau de Parking Lot" (HUMIDITÉ) · `specs/demo6.json` · 14s

| | |
|---|---|
| **קטגוריה** | פרפיום יוקרתי. **מוצר פיקטיבי:** בקבוק זכוכית מלוטש עם נוזל ענבר, פקק שחור, בלי תווית (השם רק בכרטיס הסיום) |
| **זווית** | "If perfume ads were shot in South Florida in August" (הומור מקומי, V2 §6.2 #8) |
| **הוק** | שחור-לבן בסלואו, אישה בשמלת משי בחניון של סופרמרקט, "AUGUST." |
| **משפט התפנית** | "We think we're watching a perfume ad, but actually it's a Florida parking lot at 94% humidity." |
| **חוק** | חניון ומכוניות **בלי לוגואים** (לא "Publix", לא דגם רכב מזוהה). הדמות AI, לא אדם אמיתי, ומסומנת. אין סלב |

**רשימת שוטים:** 0:00–0:03 אישה בשמלת משי לבנה הולכת בסלואו בחניון ענק, heat haze, שחור-לבן (T2V) · 0:03–0:05 העקב שלה נתקע באספלט רך ונמתח (I2V, קומדיה) · 0:05–0:07.5 עגלת קניות מתגלגלת לבד בסלואו כמו סוס פרא, "Freedom." (I2V) · 0:07.5–0:10 סופת 4 אחה"צ פוגעת, גשם בסלואו, היא לא מתרגשת (I2V) · 0:10–0:12 הבקבוק על מכסה מנוע לוהט, אדים עולים, צבע (I2V hero) · 0:12–0:14 "HUMIDITÉ / For 94% humidity." (POST).

**Seedance 2.5:**
```
ASSET BINDING:
@woman = AI-generated model (not a real person): late 30s, short dark bob, white silk slip dress,
gold hoop earrings — identical in every shot.
@bottle = faceted glass perfume bottle with amber liquid and a black cap, no label, no text.

GLOBAL STYLE: high-fashion black-and-white perfume commercial, 9:16, slow motion, dramatic contrast,
wind machine elegance, 24fps, no on-screen text, no store signs, no car logos, no brand names,
no watermark.

SCENE: A glamorous perfume film that happens to be shot in a Florida supermarket parking lot in August.

TIMELINE:
0:00-0:03 Shot 1: @woman walks toward camera across a vast sunny parking lot in slow motion, silk dress
flowing, heat haze rising off the asphalt, unbranded cars and a distant blank storefront. 85mm.
Camera: slow dolly back. Soft dissolve.
0:03-0:05 Shot 2: close-up of her heel sinking slightly into soft hot asphalt and stretching a thin
strand of tar as she lifts it; she pauses, unbothered. 100mm, ground level. Locked-off. Soft dissolve.
0:05-0:07 Shot 3: an empty shopping cart rolls alone across the lot in slow motion, majestic, like a
wild horse, palm trees behind. 135mm. Camera: slow pan following it. Hard cut.
0:07-0:09 Shot 4: a sudden tropical downpour hits; rain falls in slow motion around @woman who stands
still, eyes closed, chin up. 50mm. Locked-off.

PHYSICS: slow-motion fabric and rain; everything heavy with heat until the rain.
AUDIO: none (added in edit).
NEGATIVE: no logos, no readable signs, no license plates, no text.
```
**Kling 4.0 (שוט 5, hero):**
```
@bottle stands on the glossy hood of an unbranded dark car in harsh sunlight; heat shimmer and faint
steam rise around it after rain; droplets on the glass. Locked-off 85mm, slow 5% push-in. The bottle
stays perfectly still and rigid, amber liquid catching the light. No text, no logos, no label.
```
**רפרנסים:** woman sheet (3 זוויות, AI, לא אדם אמיתי), bottle sheet. **קבצים:** `media/demo6/s1_gown_parking_lot.mp4`, `s2_heel_sticks.mp4`, `s3_cart_slowmo.mp4`, `s4_storm_hits.mp4`, `s5_bottle_hood.mp4`.

---

## QA לפני שמעלים לתיק העבודות (מקוצר מפרק 16 §4)

- [ ] כל אות בתווית נכונה בפריים ה-hero (זום 200%). אם לא: קומפוזיט של `product_label.png` ב-corner-pin.
- [ ] אין טקסט שנוצר ב-AI בשום מקום חוץ מהתווית (שלטים, שעונים, לוחיות).
- [ ] אין ידיים מעוותות (התכנון כבר מוציא אותן מהפריים).
- [ ] שורת הגילוי ("AI-generated demo · fictional brand") מופיעה.
- [ ] מבחן השתקה: (1) מה קרה? (2) מי המותג עד אמצע? (3) מה ה-CTA? (פרק 17 §6.4)
- [ ] `grid` על ה-draft: כיתובים בתוך ה-safe zone, אין פריימים שחורים.
- [ ] ייצוא: `instagram` (9:16) + `feed` (4:5). poster JPG לכל דמו לדף הנחיתה (`landing/media/demoN.jpg`).

**זמן ועלות משוערים:** ‏2–4 שעות לדמו, $15–40 קרדיטים לדמו [הערכה, לפי פרק 10]. סה"כ ~$150–250 ל-6.
