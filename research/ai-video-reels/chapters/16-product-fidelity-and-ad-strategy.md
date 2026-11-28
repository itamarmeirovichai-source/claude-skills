# פרק 16: נאמנות מוצר ואסטרטגיית מודעות ביצועים

> **מה בפרק:** חלק א': איך שומרים על המוצר המדויק (תווית, לוגו, צורה, צבע) בכל פריים, כולל pipeline, פרומפטים, QA ופקודות ffmpeg שנבדקו. חלק ב': איך מודעות מנצחות ב-Meta, TikTok ו-YouTube Shorts ב-2026, בנצ'מרקים, שיטות בדיקה, safe zones, חבילות למכירה וכללי AI/FTC.
> **מקורות:** [X1 נאמנות מוצר](../round3/notes/X1.md) (14 מדריכים מתומללים, דף Genjutsu, ה-changelog של Higgsfield) ו-[X2 אסטרטגיית ביצועים](../round3/notes/X2.md) (18 תמלולים של מדיה-באיירים, Motion, ‏WordStream, דפי מדיניות). מזהי YouTube מופיעים בסוגריים, למשל (`l8laTEDB29M` 1:30).
> **מספרים:** עלויות ייצור לפי [פרק 10](10-numbers-capacity-pricing.md). שער ‏1$ = ₪3.04. **[מאומת]** = מקור רשמי או דאטה ראשוני. **[משני]** = בלוג או סוכנות. **[הערכה]** = שיקול דעת של הסוכן.

---

## תקציר

1. **"מוצר לא נכון = פרסומת מתה."** הלקוח סולח על הכול חוץ ממילה שגויה על האריזה. נאמנות היא שער QA ראשון, לפני היופי.
2. **שני גיליונות ולא אחד.** גיליון A לצורה בלבד, וגיליון B רק למה שנשבר בטסט (תווית פרושה, לוגו). גיליון אחד עמוס גורם למודל "לנחש" והטקסט נשבר (`l8laTEDB29M`, `kGku3TTiYO8`).
3. **שלוש שכבות הגנה:** מניעה (רפרנסים ופרומפט), תיקון מקומי (רק הקטע הפגום), וקומפוזיט של הלוגו האמיתי בעריכה. בשוט hero שכבה 3 היא ביטוח חובה.
4. **ב-2026 הקריאייטיב הוא הטרגוט.** Andromeda של Meta "קוראת" את המודעה ומחליטה למי להציג אותה. מודעות דומות מקובצות כמודעה אחת. **מה שמוכרים הוא גיוון קונספטים, לא כמות של אותו דבר.**
5. **רק כ-5% מהמודעות מנצחות, וחצי לא מקבלות הוצאה בכלל** (Motion, ‏550K מודעות) **[מאומת]**. לכן המוצר הוא נפח ומהירות של ניסויים, ו-AI הוא היתרון: וריאציה עולה כמעט $0.
6. **AI UGC בגוף ראשון הוא סיכון FTC אמיתי.** אווטאר כמגיש עם תווית AI: כן. אווטאר כ"לקוח מרוצה": לא.

---

# חלק א': נאמנות מוצר

## 1. מפת החלטות: איזה מסלול לכל שוט

| סוג שוט | סיכון | מסלול |
|---|---|---|
| **Hero packshot**, סטטי או push-in איטי | נמוך | start frame מושלם (תמונה) ← I2V עם תנועה מינימלית ← הדבקת הלוגו או התווית האמיתיים |
| **סיבוב / orbit** סביב המוצר | גבוה (הגב "מומצא") | first + last frame (חזית וגב אמיתיים), ‏90°–180° לכל היותר |
| **מוצר ביד** שמזיזים או פותחים | גבוה מאוד | צילום אמיתי של המוצר ← Genjutsu Motion Transfer, או צילום עם דמה ← Object Swap |
| **שוט רחב / lifestyle** | בינוני | multi-reference (גיליון A + B). התווית קטנה או מסובבת, לא מנסים שתהיה קריאה |
| **מאקרו:** טיפות, נוזל, קצף | נמוך | חופשי. לא שמים את התווית בפריים |
| **End card** | אפס | ה-packshot האמיתי של הלקוח (PNG) עם אנימציה בעריכה. **אף פעם לא AI** |
| **FOOH** (פחית ענקית ברחוב) | גבוה | Blender blockout (צהוב = מוצר) ← Seedance ← tracking של התווית האמיתית ([פרק 14](14-blender-blockout-and-voices.md)) |

**שלושה חוקי תנועה:**
- **מרחק הוא האויב של הטקסט.** טקסט קטן מחזיק בקלוז-אפ ונשבר בשוט רחב (`kGku3TTiYO8` 13:00). בשוט רחב התווית מסובבת הצידה או מטושטשת. רק בשוט ה-hero (קרוב, חזיתי, סטטי) היא קריאה.
- **סיבוב של יותר מ-180°** ממציא את הצד האחורי ("It has completely invented the back of the clock", `esAfAQV7p9I` 11:00). מותר רק עם last frame של הגב.
- **תנועה מהירה מסתירה עיוות, תנועה איטית חושפת אותו.** טקסט מעוות בשוט איטי הוא הכי בולט.

## 2. ה-Pipeline בתשעה שלבים

### שלב 1: קליטת נכסים מהלקוח
מבקשים תמיד:
1. **קבצי מקור של העיצוב:** AI/PDF/PSD של התווית, ולוגו SVG או PNG שקוף. לקוחות שולחים אותם בשמחה (`l8laTEDB29M` 4:00). זה הכלי הכי חזק לגיליון B ולקומפוזיט.
2. **קודי צבע:** HEX או Pantone של המותג, המכסה והנוזל. בלי זה אי אפשר להגיד "צבע לא נכון" באופן אובייקטיבי.
3. **מידות פיזיות** (גובה וקוטר), ואם אפשר, 3 יחידות של המוצר עצמו.
4. **הטקסט המדויק שעל התווית**, מוקלד אות באות.
5. **"מה אסור":** חלקים שלא מראים (ברקוד, רכיבים), צבעים שלא משנים, טענות שלא מציגים.

### שלב 2: צילום רפרנסים
- **6 זוויות:** חזית, 3/4 שמאל, 3/4 ימין, צד, גב, מלמעלה. רקע אפור או לבן, 2K–4K, **תאורה רכה מלמעלה** (מתאימה כמעט לכל מוצר).
- **צילום קנה מידה:** יד מחזיקה את המוצר. למוצר גדול: אדם לידו.
- **תווית שטוחה:** לפחית או לבקבוק, צילום של התווית פרושה, או export מקובץ העיצוב.
- **אם יש רק תמונה גרועה אחת:** Nano Banana Pro או GPT Image משחזרים זוויות, **אבל כל זווית "מושלמת" ב-AI צריכה אישור של הלקוח**, כי המודל ממציא את הגב.

### שלב 3: שיטת שני הגיליונות
- **גיליון A, צורה:** חזית, גב, צדדים, מלמעלה ומלמטה, ויד שמחזיקה. **בלי** כיתובים, חיצים או קלוז-אפים של טקסט. כל טקסט בגיליון נקרא כתוכן.
- **טסט:** שוט דינמי וקשה, לא packshot. מסתכלים **מה** נשבר. בפחית זה כמעט תמיד הטקסט הקטן מתחת ללוגו. בשפתון: המכסה המתכתי. בנעל: הטקסטורה בצד.
- **גיליון B, רק מה שנשבר:** תווית פרושה, קלוז-אפ של לוגו עם סימון מיקום, או קלוז-אפ של דוגמה. ללקוח אמיתי בונים אותו **ב-Photoshop מקבצי המקור**, לא ב-AI.
- **רפרנס C (אופציונלי):** hero packshot אחד מושלם, שהמודל מתייחס אליו כמקור האמת.
- **שמות לרפרנסים:** `@product_shape`, ‏`@product_label` ולא Image1..9. כשיש 5–10 רפרנסים זה מונע בלבול (`MzIGw-W_kTQ` 6:00).
- **פחות זה יותר:** 2–4 רפרנסי מוצר ממוקדים עדיפים על 9 מבולגנים. (מגבלות: Seedance 2.5 עד 50 רפרנסים, Genjutsu עד 30.)

### שלב 4: Keyframes בתמונה (זול, ושם מנצחים)
- **כל שוט שבו התווית קריאה מתחיל מ-start frame שנבדק אות באות.** תמונה עולה סנטים. וידאו עולה דולרים.
- Nano Banana Pro לפרטים קטנים וטיפוגרפיה. GPT Image 2.5 לעריכת מוצר וגיליונות. בפועל מריצים את שניהם ובוחרים.
- **כשהמודל נתקע על אותה טעות:** פותחים צ'אט חדש עם הרפרנסים המקוריים. ההקשר הישן מזהם (`12pQ0W2bCDE` 11:00).
- **upscale גנרטיבי יכול להמציא אותיות.** בודקים שוב אחרי upscale.
- **סבב אישור סטילס עם הלקוח לפני הווידאו** חוסך את רוב סבבי התיקונים.

### שלב 5: איזה מצב וידאו לאיזה שוט
| מצב | מתי | הערה |
|---|---|---|
| **I2V מ-start frame** | hero, ‏push-in | הכי בטוח. "Locked-off", ‏"slow push-in 5–8%" |
| **First + Last frame** | סיבוב חזית↔גב, נחיתה על packshot | שתי התמונות מאותו סט ובאותה תאורה. End frame חזיתי "נועל" את התווית בסוף |
| **Multi-reference** | דמות + מוצר | Seedance: `@` עם תפקיד מוגדר. Kling 3.0 Omni: הרפרנסים "remain active during generation" |
| **V2V / Object Swap** | תיקון קטע, החלפת SKU | Genjutsu: "change exactly what you describe; the rest stays untouched" |
| **Motion Transfer על מוצר אמיתי מצולם** | ידיים, פתיחה, מזיגה | הלוגו חד כי הוא צולם. **הדרך היחידה ל-100% נאמנות כשיש ידיים** |
| **Blender blockout → V2V** | קנה מידה בלתי אפשרי | בלוק צהוב = מוצר, פאה מגנטה = מיקום התווית ([פרק 14](14-blender-blockout-and-voices.md)) |

### שלב 6: QA (סעיף 4)

### שלב 7: תיקון, מהזול ליקר
1. **Trim:** משתמשים רק בחלק הטוב. "The finished ad is just the best few seconds out of 100 tries" (`3rDs6FhFoUQ` 35:00).
2. **Re-roll** עם seed אחר, 2–3 פעמים.
3. **Regenerate מקומי:** חותכים רק את הקטע הפגום, מעלים כ-`@Video1` ומבקשים החלפה. לא מייצרים מחדש את כל 20 השניות.
4. **Inpaint ל-start frame:** Nano Banana Pro Inpaint, ‏Photoshop Generative Fill. לטקסט: Photoshop ידני מקובץ המקור.
5. **קומפוזיט** (שלב 8).
6. **הסתרה:** מסובבים, מטשטשים (DOF), יד או אדים, ומשאירים את האמת ל-end card.

### שלב 8: קומפוזיט של הלוגו או ה-packshot האמיתי
**כלים:** After Effects (Mocha ל-planar tracking + corner pin), ‏DaVinci Resolve (Fusion Planar Tracker, ‏Magic Mask), ‏CapCut (tracking בסיסי), ו-Higgsfield AI Motion Designer שבונה logo reveals ב-AE.

**ffmpeg, נבדק בסביבה שלנו ב-06.10.2026** (קליפ 720×1280):
```bash
# A) Logo bug: real logo PNG fades in 1s→5s, top-centre (safe zone)
ffmpeg -i ai_clip.mp4 -loop 1 -t 6 -i logo.png -filter_complex \
"[1:v]scale=240:-1,format=rgba,fade=t=in:st=1:d=0.4:alpha=1,fade=t=out:st=4.6:d=0.4:alpha=1[lg]; \
 [0:v][lg]overlay=x=(W-w)/2:y=H*0.08:enable='between(t,1,5)'[v]" \
-map "[v]" -map 0:a? -c:v libx264 -pix_fmt yuv420p -c:a copy out_logo.mp4

# B) Corner-pin the REAL flat label onto the product face (4 corners measured in the frame)
ffmpeg -i ai_clip.mp4 -loop 1 -t 6 -i label_flat.png -filter_complex \
"[1:v]format=rgba,pad=iw+4:ih+4:2:2:color=black@0,scale=720:1280, \
 perspective=x0=260:y0=500:x1=520:y1=540:x2=250:y2=640:x3=510:y3=700:sense=destination[w]; \
 [0:v][w]overlay=0:0:shortest=1[v]" -map "[v]" -c:v libx264 -pix_fmt yuv420p out_pin.mp4

# C) Moving product: animate the corners, e.g. x0='260+on*1.5' ... :eval=frame

# E) Real packshot end card (2s) appended after the AI clip
ffmpeg -i ai_clip.mp4 -i end_bg.mp4 -loop 1 -t 2 -i packshot.png -filter_complex \
"[1:v][2:v]overlay=(W-w)/2:(H-h)/2:shortest=1,fade=t=in:st=0:d=0.3[ec];[0:v][ec]concat=n=2:v=1:a=0[v]" \
-map "[v]" -c:v libx264 -pix_fmt yuv420p out_endcard.mp4

# F) QA: frames for label inspection + a contact sheet
ffmpeg -i ai_clip.mp4 -vf "fps=1,scale=480:-1" qa_%02d.png
ffmpeg -i ai_clip.mp4 -vf "fps=2,scale=240:-1,tile=6x4" -frames:v 1 qa_grid.jpg
```
פקודה D (מסכת הסתרה, כשיד עוברת מעל התווית) נמצאת בהערות X1 §2.8.

**כדי שהקומפוזיט לא ייראה "מודבק":**
- להתאים תאורה (Curves, ו-highlight באותו כיוון אור).
- להוסיף את אותו grain ו-blur של הקליפ (`noise=alls=6:allf=t`, ‏`gblur=sigma=0.6`).
- על פחית או בקבוק מעוקל, corner-pin שטוח עובד עד כ-20° סיבוב. מעבר לזה: CC Cylinder או Mocha mesh warp, או להסתיר.
- לוגו בפינת המסך (bug) לא צריך tracking. לוגו **על** המוצר צריך.
- **הכי חכם: לייצר את השוט מראש "label-friendly":** תנועה איטית, תווית חזיתית ושטוחה, בלי ידיים מעליה.

### שלב 9: Blender blockout למוצר
בלוק במידות אמיתיות (פחית 330 מ"ל ≈ ‏6.6 × 11.5 ס"מ) בצהוב, ופאה חזיתית במגנטה כמיקום התווית. מרנדרים שני passes: ה-beauty לגנרציה, ו-pass של מסכת התווית (לבן על שחור). **ה-pass השני הוא matte מוכן לקומפוזיט, בלי רוטו.** ‏**[לא מאומת]:** ה-AI "זז" כמה פיקסלים מהבלוק, ולכן ייתכן שתידרש הזזה קטנה.

## 3. פרומפטים להעתקה

### 3.1 גיליון A: צורה וקנה מידה (GPT Image 2.5 / Nano Banana Pro)
```
Using ONLY the product in the uploaded photos, create a clean product SHAPE reference sheet.
Same exact product: identical proportions, silhouette, cap/lid, materials and colors — do not redesign.
Layout on a seamless light-grey background, identical soft overhead studio lighting in every panel:
top row — front view, back view, left side view, right side view;
bottom row — top-down view, bottom view, and one photo of an adult hand holding the product to show real-world scale.
Orthographic-looking camera, no perspective distortion, product centered and the same size in every panel.
Label artwork may be visible but small; do NOT add any captions, arrows, measurements, panel titles or extra text.
Photorealistic, 4K, no watermark.
```

### 3.2 גיליון B: תווית פרושה (ללקוח אמיתי: export מקובץ המקור)
```
From the uploaded product photos, create a flat LABEL reference: the full wrap-around label of the can
unrolled into one flat rectangle, front panel on the left, back panel on the right, perfectly flat,
evenly lit, no curvature, no reflections, no shadows.
Reproduce the existing artwork and typography EXACTLY — same words, spelling, fonts, weights,
colors, line breaks and positions. Do not translate, re-letter, simplify or invent any text.
Plain white background, nothing else in the frame.
```

### 3.3 Start frame במבנה של 7 שכבות (Magnific, `XLHTLJhzDyQ`)
**סדר הפרומפט חשוב יותר מהאורך שלו:** קומפוזיציה ← זהות ← בלוק טיפוגרפיה ← צבע ← אור ← אופטיקה ← איסורים.
```
[1 COMPOSITION] Vertical 9:16 editorial still life: the product stands on a wet black stone plinth,
slight 15° diagonal placement, centered in the middle third, headroom at top, clear space at bottom.
[2 EXACT IDENTITY] The product must match @product_shape and @product_label exactly — same proportions,
silhouette, cap, materials, label layout and logo placement. Do not redesign.
[3 TYPOGRAPHY BLOCK] The front label reads exactly: "ZESTA" (large, white, bold condensed sans-serif,
centered), below it "LIME & CHILI" (small caps, lime green), and "330 ml" (bottom right, white).
All text horizontal, centered on the label, sharp and fully legible. No misspellings, no extra letters,
no warped or melted glyphs, no additional words.
[4 TRUE COLOR] Matte deep forest-green can (#0F3D2E), brushed silver lid, neon-lime accent stripe.
[5 LIGHT] Large soft overhead light, thin hard rim light from behind left, subtle reflection on the stone.
[6 OPTICS] 100mm macro look, f/5.6, tack-sharp focus on the label, no oversaturation, no glow.
[7 NEGATIVES] No extra logos, no duplicated text, no invented branding, no second product, no props touching the label.
```

### 3.4 PRODUCT LOCK v2 + שורת "Label authority" (לכל פרומפט וידאו)
```
@product_label is the close-up of the front label. Use it as the AUTHORITY for the exact wording,
typeface, weight, color, line breaks and layout of the label. The label reads: "[EXACT TEXT]".

PRODUCT LOCK: @product_shape = shape and proportions; @product_label = label artwork and text (authority);
@product_hero = overall look. The product must match them exactly in every frame — same silhouette,
proportions, cap, materials, colors (#HEX), label layout and logo size/position. Rigid object: it never
bends, melts, stretches or changes size. Do not redesign, rename, translate or add text.
Keep the label sharp and readable when it faces camera; when the product turns, let the label rotate
away naturally rather than distort. Exactly one product unless stated.
```
**שורה אחרונה (negative):**
```
Rigid product, constant size, no melting, no bending, no extra products, no duplicated or mirrored text,
no gibberish letters, no logo drift, no color shift, fingers never cover the label.
```

### 3.5 וידאו: hero I2V (הכי בטוח לטקסט)
```
@Image1 is the first frame. Locked-off tripod, 100mm. The camera slowly pushes in about 6% over 5 seconds.
Only the environment moves: light condensation droplets slide down the can, faint mist drifts at the base,
a soft light sweep passes across the background. The can itself stays perfectly still, label facing camera,
text sharp and unchanged for the whole shot. Ends on a held frame. No cuts, no text, no music.
PRODUCT LOCK: ...
```

### 3.6 First + Last frame: סיבוב גב→חזית
```
Start frame @Image1 (back of the product), end frame @Image2 (front, label facing camera).
The product rotates 180° smoothly on a turntable at constant speed while the camera pushes in slightly.
Rigid object, constant size, no wobble. The front label becomes fully readable only in the final second
and settles exactly as in @Image2. Premium CGI product film, studio gradient background.
```

### 3.7 מוצר ביד (Seedance 2.5 / Kling 3.0 Omni)
```
@model = woman (face, hair, outfit). @product_shape, @product_label = the product.
9:16, 6s. A woman in a sunlit kitchen picks up the can from the counter with her right hand,
grips it from the BOTTOM half so her fingers never cover the label, lifts it to chest height
and turns the label to camera, holding it still for the last 2 seconds.
Medium close-up, 50mm, natural window light from the left.
[append Label authority line + PRODUCT LOCK]
```
"grips from the bottom half" מוריד את רוב עיוותי היד-על-התווית **[המלצה הגיונית, לא נבדקה מבוקר]**.

### 3.8 תיקון מקומי
```
Replace the can in @Video1 with the product in @product_hero, using @product_label for the label.
Match the original lighting, reflections, hand grip, motion and timing exactly.
Change nothing else in the shot: same person, background, camera move and duration.
```
```
Object Swap (Genjutsu): Replace only the plain white dummy bottle in the actor's hand with the product
from the references. Keep the actor's grip, motion, timing and camera identical; match the scene lighting.
Label faces camera when the bottle is raised.
```

### 3.9 מטא-פרומפט ל-Claude: Product Bible
```
Look at these product photos and the client's label file. Produce a PRODUCT BIBLE for AI video:
(1) exact label text, line by line, with font style, weight, color and position;
(2) brand colors as HEX (sample them from the images; mark guesses);
(3) physical size and proportions (height:width ratio);
(4) the 3 details most likely to break in AI video (small text, metallic parts, textures) and how to protect each;
(5) a 'Typography block' and a 'PRODUCT LOCK' paragraph ready to paste into Seedance/Kling prompts.
Never invent text that is not visible; write [UNREADABLE] instead.
```

## 4. צ'קליסט QA לפני מסירה

**א. רפרנסים**
- [ ] גיליון A (זוויות + יד) **בלי** טקסט מסביב.
- [ ] גיליון B נבנה **אחרי** טסט, ורק עם מה שנשבר.
- [ ] טקסט התווית מוקלד בפרומפט ומאושר ע"י הלקוח. HEX כתובים. לכל רפרנס יש שם ותפקיד.

**ב. Start frames**
- [ ] זום 200% על כל מילה וכל ספרה (נפח, אחוזים).
- [ ] יחס גובה-רוחב זהה בכל ה-keyframes (מניחים זה לצד זה).
- [ ] לוגו באותו גודל ומיקום. צבע הגוף נדגם ב-eyedropper ומושווה ל-HEX.
- [ ] בדיקה חוזרת אחרי upscale. טסטים ב-480p/720p, ו-1080p (או 4K) רק לטייק שעבר QA.

**ג. וידאו**
- [ ] grid של 2fps (ffmpeg F), ומעבר על כל פריים שבו התווית נראית.
- [ ] **"מבחן הפריים הגרוע":** בפריים עם הכי הרבה תנועה, המוצר לא משנה גודל או צורה.
- [ ] אין מוצר כפול, מכסה משתנה או נוזל בצבע לא נכון. אצבעות לא "נבלעות" במוצר.
- [ ] בשוטים רחבים התווית לא קריאה, **אבל גם לא ג'יבריש בולט**.
- [ ] End card = packshot אמיתי. כל טקסט שיווקי נוסף בעריכה.

**ד. לפני שליחה**
- [ ] הלקוח אישר סטיל של ה-hero לפני הרנדר הסופי.
- [ ] בהצעה יש "נספח אישור מוצר": "הלקוח מאשר את מראה המוצר בפריימים X, Y, Z".
- [ ] סימון AI לפי הפלטפורמה (סעיף 10).
- [ ] נשמר "Fidelity log": ‏seed, פרומפט ורפרנסים לכל שוט מאושר, כדי לשחזר וריאציות.

## 5. טבלת כשלים ותיקונים

| כשל | למה | מניעה | תיקון |
|---|---|---|---|
| **טקסט מעוות / ג'יבריש** | טקסט קטן, מרחק, גיליון עמוס | גיליון B, ‏Typography block, ‏Label authority, שוט קרוב | re-roll; תיקון מקומי; **corner-pin של התווית האמיתית**; DOF |
| **לוגו "נודד"** | המודל לא יודע שהוא "קדוש" | קלוז-אפ לוגו עם סימון מיקום; "logo size/position" ב-LOCK | tracking + overlay (ffmpeg B/C או Mocha) |
| **צבע לא נכון** | "blue" כללי, ‏grade של הסצנה | HEX ושם ספציפי ("deep cobalt blue"), ‏"no oversaturation" | Hue/Sat ממוסך (Resolve Qualifier) |
| **שינוי גודל או פרופורציה** | אין רפרנס קנה מידה | יד בגיליון A, ‏"rigid object, constant size" | טייק אחר, שוט קצר יותר, first+last |
| **גב מומצא בסיבוב** | המודל לא ראה את הגב | גב בגיליון A, סיבוב ≤180° | לחתוך לפני שהגב נראה |
| **ידיים מעוותות את התווית** | אצבעות מעל טקסט בתנועה | "grips from the bottom half", הפקה היברידית | Motion Transfer על צילום אמיתי; מסכת הסתרה |
| **מוצר כפול** | "products" ברבים, רפרנס עם כמה יחידות | "Exactly one product" | inpaint; ‏Object Swap |
| **אריזה מומצאת בסוף** | concept של ChatGPT | האריזה האמיתית בסט | end card אמיתי |
| **הקשר מזוהם** (אותה טעות שוב) | צ'אט ארוך | צ'אט חדש לכל keyframe | צ'אט חדש + רפרנסים מקוריים |
| **upscale שינה אותיות** | upscaler גנרטיבי | upscaler שמרני | upscale לרקע בלבד, התווית מעל |
| **קפיצה בתחילת קליפ** | ארטיפקט התחלה | — | trim של 0.3–0.5 שניות |
| **"מראה מודבק"** אחרי קומפוזיט | אין grain, ‏blur ואור תואם | — | noise + gblur + Curves |

**נאמנות כמוצר למכירה:** רוב המתחרים "מעלים 7 תמונות ומתפללים". בהצעה כותבים: "המוצר בפרסומת זהה למוצר שלך: התווית והלוגו מקבצי המקור שלך, נבדקים פריים-פריים". את שלב ה-Product Bible ושני הגיליונות אפשר למכור כ-**setup fee לכל SKU** (‏$100–200, כ-₪300–600) **[הערכה]**. אחריו כל וריאציה זולה יותר.

---

# חלק ב': אסטרטגיית מודעות ביצועים

## 6. איך האלגוריתם עובד ב-2026

| עובדה | מה זה אומר לך | מקור |
|---|---|---|
| **Andromeda** בוחרת מעשרות מיליוני מודעות כמה אלפי מועמדות לכל משתמש. המודל גדל פי 10,000 | המערכת בנויה לבלוע הרבה וריאציות | Meta Engineering **[מאומת]** |
| Andromeda **מתמללת** כל מודעה. ‏Persona call-out בהוק דוחף את המודעה לקהל דומה | **ההוק הוא הוראת טרגוט.** הוק שלא תואם לגוף מבזבז את המודעה | Blue Sense (`vUbLw80KTpo` 24:30) **[משני]** |
| **Creative Similarity:** מודעות דומות מקובצות לישות אחת ומוצגות לאותו קהל | **10 צבעי רקע לאותו סרטון = מודעה אחת** | (`vUbLw80KTpo` 12:00) |
| Meta עושה **sequencing:** מודעת TOF פותחת, BOF סוגרת. הייחוס last-click | **לא מכבים מודעה בגלל ROAS נמוך ברמת המודעה** כשה-ad set עומד ביעד | (`vUbLw80KTpo` 17:00) |
| החלפת הוק יוצרת creative ID חדש | בדיקת הוקים היא הדרך הכי זולה להחיות מודעה עייפה | (`vUbLw80KTpo` 63:00) |

### "קונספט" = יחידת המכירה שלך
**Concept = Persona × Angle × Offer (+ Format).** כדי ש-Andromeda תראה מודעה "חדשה", משנים לפחות אחד משלושת הראשונים. שינוי פורמט לבד נותן רק חשיפה חדשה חלקית.
- **סדר הבדיקה:** Angle ← Offer ← Persona ← Format. רוב המפרסמים הופכים: "בוא ננסה UGC". אבל "UGC as a concept doesn't work. It is the script, the persona, the angle, the offer".
- **Persona ספציפית עד כאב:** לא "health-conscious parent", אלא "mom who's tried six supplements because her toddler won't eat vegetables".
- **Angle מול Hook:** ה-angle הוא האסטרטגיה (איזה רצון מופעל, איזה כאב מוגבר). ה-hook הוא המילים הראשונות שמציגות אותו. לכל angle יש אינסוף הוקים.

### מבנה חשבון אחרי Andromeda
| אסכולה | מבנה | למי |
|---|---|---|
| **Packs + minimum spend** (Moonlighters) | כל סבב חדש = ad set חדש עם 4–8 מודעות. מינימום יומי = ‏1× CPA (עד 20% מהתקציב) ל-7 ימים | e-com ב-$5K–100K לחודש. **ברירת המחדל ללקוחות** |
| **25–30 ads unique** (Jeremy Haynes, מיאמי) | 3 ad sets (Broad / Interest / Lookalike), כל אחד עם אותן 25–30 מודעות שונות לגמרי | high-ticket ולידים |
| **Concept per ad set** (Blue Sense) | ad set לכל קונספט, מינימום 3 מודעות. **לא מוסיפים מודעות ל-ad set שעומד ב-KPI** | מי שרוצה למידה נקייה לכל קונספט |

**לעסק קטן** (מתחת ל-$1M בשנה): אווטאר אחד, 10–50 pain points. מוצאים angle מנצח ואז "משכפלים" אותו לפורמטים: static ← talking-head ← סלפי ← B-roll.

## 7. בנצ'מרקים (לשימוש מול לקוח)

> **כלל-על: "Your data is your benchmark."** מספר כללי מועיל רק כשאין היסטוריה. אחרי 5 מודעות דומות משווים לחציון של החשבון. Hook ו-hold הם כלי אבחון, לא KPI. ה-KPI הוא CPA, ‏ROAS ו-CAC מול LTV.

### 7.1 Meta: מטריקות וידאו
| מטריקה | נוסחה | בסדר | טוב | חזק |
|---|---|---|---|---|
| **Hook rate** | צפיות 3 שניות ÷ חשיפות | 20–25% | 25–30% | 35%+ |
| **Hold rate** | ThruPlays ÷ חשיפות | 5–8% | 8–12% | 15%+ |
| CTR (link) | קליקים ÷ חשיפות | 1% | 1.5–2% | 2–3%+ |
| LPV ÷ קליקים | | 70% | 80%+ | 90% |
| Frequency (קר, ברמת מודעה) | | | ≤2 | |
| CPM ‏US | | $10–25 | | |

**מלכודת ThruPlay:** ‏ThruPlay = ‏15 שניות **או** צפייה מלאה בסרטון קצר. סרטון של 6 שניות יציג hold מנופח, ולכן תמיד מוסיפים Avg. watch time.

**אבחון לפי דפוס:**
| Hook | Hold | CTR | CPA | אבחנה | פעולה |
|---|---|---|---|---|---|
| נמוך | – | – | – | הפתיחה לא רלוונטית | 5–10 הוקים חדשים על אותו גוף |
| גבוה | נמוך | – | – | Clickbait, או "גשר" שבור | לכתוב מחדש את שניות 3–8 |
| גבוה | גבוה | נמוך | – | אין CTA או הצעה חלשה | CTA ויזואלי, הצעה ברורה |
| גבוה | גבוה | גבוה | גבוה | דף הנחיתה | message match, מחיר מעל הקפל |
| בינוני | בינוני | בינוני | **טוב** | "הבלסט" של החשבון | **לא נוגעים** |

### 7.2 Meta לפי ענף בארה"ב (WordStream 2026, ‏1,000+ קמפיינים) **[מאומת]**
כללי: traffic ‏CTR ‏1.93%, ‏CPC ‏$0.60. leads ‏CTR ‏2.70%, ‏**CPL ‏$27.39**.

| ענף (רלוונטי לבוקה) | CTR leads | **CPL** |
|---|---|---|
| Real Estate | 4.17% | $13.74 |
| Health & Fitness | 3.09% | $27.11 |
| Physicians & Surgeons | 4.18% | $32.14 |
| Personal Services | 2.24% | $38.09 |
| Home Improvement (HVAC, בריכות) | 2.14% | $42.95 |
| Beauty & Personal Care (מד-ספא) | 1.35% | $50.91 |
| Dentists | 1.62% | **$61.56** (הכי יקר) |

**שימוש במכירה:** "Your dental CPL benchmark is ~$62. If our creative takes you to $45, that's 27% more patients for the same budget." אומרים "benchmark", לא "guarantee".

### 7.3 TikTok ו-YouTube Shorts **[משני]**
- **TikTok:** CTR ל-DTC ‏1.0–1.5% (מזון ומשקאות: חציון 1.5%). מתחת ל-0.5% = ההוק נכשל. ‏CPM ‏$5–12 לביוטי וצריכה. 50–70% מההוצאה עוברת דרך Spark Ads. בדיקה: 3–5 Spark ב-$20 ליום כל אחד.
- **YouTube Shorts (Demand Gen):** CPM לרוב מתחת ל-$10. ‏view rate של 6–12%. ‏CTR מעל 1%. Channels: רק Shorts. תקציב יומי לפחות 3× CPA, סבלנות של 2–3 שבועות.

### 7.4 מספרי "מערכת"
| מספר | ערך |
|---|---|
| Hit rate (מודעה שמוציאה פי 10 מהחציון) | **~5%** **[מאומת, Motion]** |
| מודעות שלא מקבלות כמעט הוצאה | ~50% |
| מודעות חדשות בחודש | **≈ הוצאה חודשית ÷ $1,000** |
| מודעות לכל קונספט נבדק | 10+ (ב-5% hit rate: כ-20) |
| תקציב הפקה | $30–100K מדיה: ‏25%. מעל $100K: ‏~10% |
| חלוקת מאמץ | 50–60% שכפול מנצחות, 20–30% איטרציות, 20–30% קונספטים חדשים |
| קונספטים פעילים | $4–30K: ‏3. ‏$30–100K: ‏5–6. ‏$100K+: ‏8–10 |

**ה-USP שלך:** AI מוריד את עלות ההפקה למודעה מ-$150–500 ל-$20–60, ולכן כמעט כל מודעה הופכת לרווחית. "We don't sell you a $10K commercial. We sell you 40 shots on goal."

## 8. איך בודקים: מסגרות עבודה

### 8.1 Creative Flywheel (הכי קל להסביר ללקוח)
```
 SOURCE  ->  BUILD  ->  LAUNCH  ->  WAIT 7d  ->  ANALYZE  ->  ITERATE  -> (back to BUILD)
 (competitors, reviews,   (concepts   (new pack +    (don't touch)  (spend-sorted,      (variants of
  Reddit, own winners)     x formats)  min spend)                   incremental ROAS)   top spenders)
```
השראה ממותגים שגדולים פי 10 (לא מ-Nike). ב-Ad Library מחפשים מודעות שרצות הכי הרבה זמן. **אבל:** אם כולם מעתיקים מה-Ad Library, כל הנישה נראית אותו דבר. הרעיונות המפתיעים באים מסרטים, ספרים ודוקו ([פרק 17](17-creative-director-system.md)).

### 8.2 3-2-2 ללקוח מקומי קטן
‏3 קונספטים (באמת שונים: UGC-style, דמו, static עם טקסט) × 2 angles בקופי × 2 קהלים. שופטים אחרי 7 ימים בלי לגעת. בתקציב קטן: 2-1-1. מעל $10K לחודש עוברים ל-packs.

### 8.3 Hooks × Bodies (מבנה מודולרי, מושלם ל-AI)
> "שעה עבודה: 2 הוקים × 5 גופים, **או** 15 הוקים × 2 גופים. השני תמיד מנצח, אם הגוף טוב."
```
HOOK (0-3s)   x 5-10 variants    <- visual + audio + text overlay (3 layers)
BRIDGE (3-8s) x 1-2              <- continues the hook's promise, product NOT yet named
BODY (8-25s)  x 2                <- problem agitate x2 -> mechanism -> proof
CTA (last 3-5s) x 2              <- offer + visual CTA + "before/after" recap
```
- **הגשר הוא המקום שבו רוב המודעות מתות.** לא קופצים מ"Training for a marathon?" ישר ל"Creatine X is your solution". מכניסים את המוצר כמה שיותר מאוחר.
- **להעלות hold:** קאט כל פחות מ-2 שניות, שתי זוויות לאותה פעולה, להמשיך את סיפור ההוק.
- **Pre-test ב-TikTok:** 20 גרסאות הוק כ-Trial Reels אורגניים, ורק 5 הטובות נכנסות לממומן.

### 8.4 סולם איטרציות
| דרגה | מה משנים | עלות ב-AI | מתי |
|---|---|---|---|
| L1 Variation | טקסט הוק, צבע כתוביות, יחס, CTA | ~$0 | מנצחת שמתעייפת |
| L2 Hook swap | 3–10 הוקים חדשים על אותו גוף | נמוכה | hook rate מתחת לחציון |
| L3 Iteration | אותו angle, ‏persona/שחקן/setting/פורמט אחר | בינונית | angle שעובד, להרחבת קהל |
| L4 New concept | angle, ‏offer או persona חדשים | מלאה | 20–30% מהמאמץ |

### 8.5 SOP של kill / keep / scale
```
DAY 0   Launch new pack (4-8 ads, 1 concept or 1 angle family). Min spend = 1x CPA (<=20% budget).
DAY 1-6 Don't touch. Only kill ads with policy issues or broken links.
DAY 7   Remove ad-set minimum. Read at AD SET level (7-day click, new customers).
        - Pack beats CPA target           -> keep, raise budget 20-30% steps, brief iterations L1-L3.
        - Pack at target +-15%            -> keep running (mid-range ballast), brief L2 hook swaps.
        - Pack >30% over target, low spend-> pause pack, log learnings, move on.
DAY 14  Winner check: ad spending >=10x account median OR >=3x CPA at/below target = "WINNER".
        -> 5-10 hook swaps + 2 format translations within 72h.
NEVER   Turn off a top-of-funnel ad inside an ad set that's hitting KPI because its ad-level ROAS looks low.
NEVER   Add new ads into a performing ad set (breaks sequencing) - launch a new pack instead.
```
הספים (±15%, ‏30%) הם **[הערכה]**. **אזהרה:** לפני scale שואלים את הלקוח על מלאי ותזרים. "לסחוט" מנצחת בשביל case study פוגע בחשבון.

### 8.6 מכונת angles (30 בשעה)
אוספים 10–12 angles מביקורות Amazon, ‏Reddit, תגובות TikTok ופניות תמיכה. מחפשים ניסוחים כמו "I was skeptical, but…", ‏"finally something that doesn't…", ‏"I tried everything". מכפילים ×3 (benefit / problem / story) ומדרגים.
```
You are a direct-response creative strategist. Product: [PRODUCT + URL]. Price: [$]. 
Here are 40 real customer reviews / Reddit comments / support tickets: [PASTE].
1) Extract 12 distinct ANGLES (the strategic argument, not the hook). For each: desire activated,
   pain/benefit amplified, motivation the product attaches to, awareness stage (Schwartz).
2) For each angle write 3 hooks: benefit-driven, problem-driven, story-driven (<= 12 words, spoken).
3) Score each angle 1-5 on Relevance, Differentiation (would Meta see a new audience?), Ease of
   AI production this week. Return a table sorted by total. No medical/financial guarantees,
   no fake testimonials, no "you" + personal-attribute callouts that violate Meta policy.
```
**אזהרה:** LLM "נותן ממוצעים". קודם כותבים ידנית כמה פרסונות טובות, ורק אז נותנים לו להרחיב.

## 9. מה מנצח לפי הדאטה (Motion, ‏550K מודעות) **[מאומת]**

| פורמט | Hit rate | הערה ל-AI |
|---|---|---|
| Unboxing | **9.83%** | ידיים, מאקרו של אריזה, ‏ASMR. קל מאוד |
| Offer-first banner | 8.68% | static או motion עם מחיר בשנייה הראשונה |
| Behind the scenes | 8.64% | B-roll של מטבח/סטודיו, מסומן AI |
| Founder | 8.57% | **רק המייסד האמיתי** |
| POV | 8.28% | AI מצוין בזה |
| Demo | 8.11% | רק אם משקף ביצועים אמיתיים (FTC) |
| Cinematic b-roll | 6.85% | ה-sweet spot של Seedance ו-Kling |
| Testimonial | 6.57% | **רק לקוח אמיתי** |
| Before & after | 6.07% | מוגבל בבריאות ויופי |

- **סוג נכס:** **Text only ‏11.6%**, תמונת מוצר + טקסט 8.75%, ‏UGC ‏7.56%, הפקה גבוהה 6.97%. טקסט פשוט וברור מנצח לעיתים קרובות יותר מהפקה יקרה.
- **טקטיקות הוק:** Newness ‏11.4%, הכרזת מבצע 11.4%, Price anchor ‏10.9%, Urgency ‏9.7%. (הדאטה כולל את עונת המבצעים, ולכן הצעה ודחיפות מנופחות.)

**האסטרטגיה שכדאי למכור: "Hybrid".** ה-AI עושה את מה שיקר לצלם: B-roll קולנועי, packshot, סצנות, וריאציות, יחסי מסך והחלפות הוק. האמת האנושית מגיעה מאדם אמיתי: מייסד, לקוח, עובד. כך מקבלים גם את ה-hit rate של founder ו-UGC וגם את הנפח של AI, בלי סיכון FTC.

**מבחר הוקים (באנגלית):** "I tested 3 [hacks]. Only one worked." · "This costs $[X]. Yes, it's expensive. Here's why it sells out." · "I'm the owner, and I'm going to tell you what most [industry] won't." · "POV: you finally found a [X] that actually [Y]." · "Boca, your AC shouldn't sound like that in October." · "If you live east of I-95, read this before hurricane season." עוד 20 בהערות X2 §5.3, ו-bank מלא ב[פרק 17](17-creative-director-system.md).

## 10. AI, ‏FTC ופלטפורמות (חובה לפני שמוכרים בארה"ב)

| פלטפורמה | הכלל ב-2026 | מה עושים |
|---|---|---|
| **Meta** | תווית "AI info". אדם פוטוריאליסטי שנוצר ב-AI מקבל תווית ליד "Sponsored". מ-1.6.2026: זיהוי אוטומטי של כלים חיצוניים לפי C2PA | לא מוחקים מטא-דאטה. סוגרים בחוזה שהתווית תופיע |
| **TikTok** | AIGC חובה לתוכן ריאליסטי. במודעות: מתג "This ad contains AI-generated content" **שמתאפס בכל שכפול קמפיין** | לבדוק את המתג בכל שכפול (ב-QA) |
| **TikTok, אסור לגמרי** | דמות סינתטית של קטין, של אדם פרטי בלי הסכמה, או איש ציבור "שממליץ" | אווטאר stock או מורשה בלבד |
| **YouTube** | לסמן ("AI use" ב-Studio) תוכן ריאליסטי שלא קרה. לא צריך: סצנה לא ריאליסטית, פילטרים, שיבוט הקול שלך | לסמן לפני שמקשרים כמודעה |

**FTC 16 CFR 465** (בתוקף מאוקטובר 2024) **[מאומת]** אוסר ביקורות ועדויות "by someone who does not exist, such as AI-generated fake reviews", או של מי שלא השתמש במוצר. יש קנסות אזרחיים (כ-$50K+ להפרה **[לא מאומת לסכום 2026]**).

| מותר (עם תווית AI) | אפור, להימנע | אסור |
|---|---|---|
| אווטאר AI כ-**spokesperson** ("Here's how it works") | אווטאר שמקריא ביקורת אמיתית, עם "AI dramatization of a verified customer review" | אווטאר: "I've used this for 3 months and…" |
| B-roll, ‏packshots וסצנות שמייצגים נכון את המוצר | דמו AI של תוצאה (ניקוי, הרזיה, עור) | before/after שנוצר ב-AI ומוצג כאמיתי |
| POV או המחזה מסומנת | | שיבוט פנים או קול בלי הסכמה בכתב |

**סעיף חוזה (להעתקה):**
```
Client warrants that all testimonials, reviews, statistics, before/after results and claims supplied for use in ads are truthful, substantiated, and from real customers with consent. Agency will not create synthetic testimonials presented as real customers. AI-generated people or voices will be disclosed per platform policy.
```
כללי פלורידה לרפואה, נדל"ן ועורכי דין: [פרק 18](18-us-clients-boca.md).

## 11. מפרטים ו-safe zones

| פורמט | גודל | Safe zone |
|---|---|---|
| **9:16 Reels + Stories** (אוחדו במרץ 2026) | 1080×1920 | **14% עליון (270px), ‏35% תחתון (670px), ‏6% בצדדים** ⇒ אזור בטוח של ~950×980 במרכז **[משני]** |
| **4:5 Feed** (ה-sweet spot) | 1080×1350 | ~250px למעלה ולמטה, 100px בצדדים |
| 1:1 Feed | 1080×1080 | ריפוד ~100px |
| **TikTok** | 1080×1920 | להימנע מעמודת הכפתורים בימין (~140px) ומ-20% התחתונים |
| YouTube Shorts | 1080×1920 | כמו Reels. הוק שעובד בלי קול בחצי השנייה הראשונה |

```
MASTER: 9:16 1080x1920, text inside 950x980 center box, no text in bottom 35%.
DERIVE: 4:5 1080x1350 (re-frame, move captions up), 1:1 1080x1080 (statics/feed), 16:9 (YouTube in-stream only if needed).
KEEP:   1 textless master per concept (cheap re-hooks/translations).
AUDIO:  captions burned-in (most watch muted) + licensed/commercial music only (no trending sounds in Meta ads unless from Meta Sound Collection / TikTok Commercial Music Library).
QA:     AI label toggle (Meta self-disclosure where applicable; TikTok AIGC ad toggle re-checked after every duplication).
```

**Spark Ads ו-Partnership Ads:** תוכן AI שעלה **אורגנית** לחשבון של הלקוח (עם תווית) והוכיח את עצמו ← מקדמים כ-Spark. מוכרים "Organic-first testing": 10 גרסאות אורגניות, ומממנים רק את 2 שהחזיקו watch time ותגובות "where can I buy". ללקוח מקומי: partnership עם משפיען מקומי (בוקה/דלריי) + B-roll AI שלך.

## 12. החבילה למכירה: "Creative-as-a-Service"

**איך השוק מתמחר** **[משני]**: פרילנס $150–500 לסטטי ו-$500–2,000 לווידאו. ריטיינר של סוכנות ביצועים $5–15K לחודש. Superside מ-$15K לחודש **[מאומת]**. יוצר UGC אנושי ~$198 לסרטון. כלי AI UGC בעשה-זאת-בעצמך $29–149 לחודש.
**המיקום שלך:** מתחת לסוכנויות ומעל כלי DIY. "Agency-level volume and strategy at freelancer price, because AI makes every extra variation nearly free." המרווח ב-Growth מעל 85% **[הערכה]**.

```markdown
# [Your Studio] — AI Performance Creative, Monthly
Built for Meta (FB/IG), TikTok and YouTube Shorts. Made in Boca Raton, FL.

Why: After Meta's Andromeda update, your creative IS your targeting. Accounts that test more
distinct concepts find more winners (only ~5% of ads become winners - Motion 2026, 550K ads).
We give you agency-level testing volume at a fraction of agency cost, using AI production
plus real human proof from your business.

## Plans
### LOCAL LAUNCH — $1,500/mo  (for local businesses spending $1.5K-$8K/mo on ads)
- 3 concepts/month (persona x angle x offer), 12 ad assets total
  (e.g., 4 videos 15-30s + 8 statics/hook swaps), delivered in 2 drops
- 9:16 + 4:5 + 1:1 exports, safe-zone checked, captions burned in
- Monthly 30-min results call + 1-page Creative Report
- 1 revision round per asset | 5 business-day turnaround

### GROWTH ENGINE — $3,500/mo  (DTC & multi-location, $8K-$40K/mo spend)   <- most popular
- 6 concepts/month, 30 ad assets (60% iterations of winners / 40% new concepts)
- Weekly drops (Mon), angle library + research from your reviews/Reddit/competitors
- Hook-swap kit: up to 10 new hooks on any winner within 72h
- Testing roadmap + Creative Report (weekly snapshot, monthly deep-dive)
- TikTok/Reels organic test versions for Spark/Partnership ads

### SCALE PARTNER — $7,500/mo  ($40K+/mo spend)
- 10 concepts/month, 60+ assets, dedicated strategist hours, 48h hook-swap SLA
- Static + video + YouTube Shorts (Demand Gen) cuts, multilingual (EN/ES) versions
- Creative unit economics: cost per asset vs contribution per ad

## Performance bonus (optional, chosen by client)
Option A — Winner bonus: $250 per "Winning Ad" (an ad we produced that spends >=10x the account's
median ad spend in a 30-day window AND is at/below target CPA). Cap: $2,000/mo.
Option B — Spend share: 3% of media spend on ads we produced, on top of a reduced base
(Local $1,000 / Growth $2,500).

## Add-ons
- Media buying: +$750/mo (Local) or 10% of spend, min $1,000 (Growth+)
- Real-person shoot day in Palm Beach County: $650 half-day
- Rush (48h): +50% | Extra concept: $400 | Extra static: $40 | Extra hook swap: $35

## Terms
3-month initial term (creative testing needs 60-90 days), then month-to-month, 30-day notice.
Client owns all final assets on payment. AI-generated people/voices are disclosed per platform policy.
We never create fake customer testimonials (FTC 16 CFR 465). Claims supplied by client must be true.
```
**הערות:**
- **Pilot:** "Creative Sprint" ב-$750: קונספט אחד, 6 נכסים, דוח אחרי 14 יום. אם הלקוח עובר לחודשי, מקזזים 50%.
- **למה "קונספטים" ולא "סרטונים":** זה מחייב גיוון אמיתי ומונע ויכוח על "עוד גרסה אחת".
- **קיבולת:** לא יותר מ-12 קונספטים חדשים בשבוע לאדם. ליוצר יחיד, בערך 4 לקוחות Growth ו-4 Local הם המקסימום **[הערכה]**.
- **התאמה לפרק 10:** המחירים כאן לשוק האמריקאי. המחירון בשקלים של פרק 10 נשאר בתוקף לישראל.

**בריף, דוח חודשי ו-snapshot שבועי** (תבניות באנגלית, מוכנות להעתקה): הערות X2 §10 ו-§12. עמודות מותאמות ל-Meta שמגדירים פעם אחת:
```
Hook rate        = Video plays at 3 seconds / Impressions
Hold rate        = ThruPlays / Impressions          (+ show Avg. watch time!)
Hold-of-hooked   = ThruPlays / 3-second plays
Link CTR         = Link clicks / Impressions
LPV rate         = Landing page views / Link clicks
Spend vs median  = Ad spend / median ad spend (export -> sheet)
Attribution: 7-day click (+ Compare: Incremental attribution). Exclude existing customers where possible.
```

## 13. פנייה מבוססת דאטה (Andromeda audit)
```
Subject: 3 new ads for [Business] (made them already)

Hi [Name] — I'm [You], a creative strategist in Boca. 

I looked at your Meta Ad Library: you're running [N] ads, and they're all [same format/same message].
Since Meta's Andromeda update, ads that look alike get grouped and shown to the same people —
so the platform effectively sees 1 ad, not [N].

I made 3 different concepts for you (spec, free, yours to keep if you like them):
1) [Angle 1]
2) [Angle 2]
3) [Angle 3 — offer-first static]
Preview: [link]

For reference, the average [dental/home-services] cost per lead on Meta in 2026 is ~$[62/43]
(WordStream). Want me to show you how we'd test these against your current ads in a 14-day sprint?

[You] · [phone] · [site]
```
**למה זה עובד:** הוכחה שעשית שיעורי בית (Ad Library), מושג אחד של 2026 שמבדל אותך, עבודה מוכנה, מספר שמתרגם לכסף, וצעד קטן (Sprint ב-$750). **בלי "AI" כמילה ראשונה.** כללי ספק ([פרק 10](10-numbers-capacity-pricing.md)): מותג אמיתי רק בפיץ' פרטי.
