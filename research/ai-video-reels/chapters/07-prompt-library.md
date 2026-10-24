# פרק 7: ספריית הפרומפטים. העתק, מלא את הסוגריים, הדבק

> **העורך הראשי · 05.10.2026 · תוצר 1 מתוך 3.** הפרק מאחד ומנקה כפילויות מנספח א' של פרק 03, מהדוחות C1, ‏C2, ‏C3, ‏E4 ו-D3, ומפרק 11. כל הפרומפטים **שוכתבו כך שאין בהם שמות של מותגים אמיתיים** (רכבים, מלונות, שעונים, ציוד), לפי מדיניות ספק-אדים בפרק 10 §4 וטבלת ההחלפות בפרק 06 §4.
> **מספרים:** כל עלות כאן לקוחה מפרק 10 (מקור האמת) או נגזרת ממנו בנוסחה שבסעיף 0.2. שער: **1$ = ₪3.04**. שווי קרדיט Higgsfield לתכנון: **‏$0.049 ≈ ₪0.149** (Plus חודשי).
> **סטטוס בדיקה:** **אף פרומפט בפרק לא הורץ על ידינו.** כולם בנויים לפי הכללים בפרק 03 ולפי מה שנראה ברילס. כל פרומפט מסומן **[לא נבדק בפועל]**. הפרומפטים שתומללו מתוך הרילס עצמם מסומנים **[נראה ברילס; לא נבדק על ידינו]**. חוק העבודה: טיוטה ב-480p, ורק אחריה 1080p.

## תקציר

1. **איך עובדים עם הספרייה:** בוחרים פורמט (סעיף 3), מעתיקים את הפרומפט, ממלאים את מה שבסוגריים המרובעים, מריצים טיוטה ב-480p (כ-₪4.5 ל-10 שניות), משנים **משתנה אחד** בכל ריצה, ורק אז מרנדרים ב-1080p. מי שרוצה פרומפט חדש לגמרי ממלא את **תבנית המאסטר** (סעיף 1), או שולח רשימת שוטים קצרה ל-**meta-prompt** ב-Claude/ChatGPT (סעיף 2).
2. **מה יש בפנים:** 5 תבניות מאסטר (Multi-shot מתמונה, ‏V2V עם CHANGE/PRESERVE, ‏Infinite Angles, קליפ קצר, ‏Object Swap). ‏6 meta-prompts. **‏72 פרומפטי וידאו** ב-15 פורמטים, ולכל אחד שימוש, מודל והגדרות, רפרנסים, עלות משוערת והערה. **‏25 פרומפטי תמונה ו-keyframe**. צ'קליסט רפרנסים וספריית שורות negative ונעילה.
3. **שלושה כללים שחוזרים בכל הספרייה:** (א) **תנועת מצלמה אחת לכל שוט**, עם מצב סיום ("exits frame", "holds"). (ב) **לכל רפרנס תפקיד אחד**, וכתוב גם מה הוא לא קובע. (ג) **בלי טקסט ובלי לוגו בתוך הג'נרציה.** כתוביות, לוגו אמיתי ו-end card מוסיפים בעריכה.
4. **עלויות לתכנון (עם טיוטות וניסיונות):** קליפ של 10 שניות ב-Seedance 2.5 ב-1080p ≈ **₪42**. ‏Genjutsu של 15 שניות ≈ **₪71**. ‏Infinite Angles של 20 שניות ≈ **₪54**. ‏Kling 3.0 של 10 שניות ≈ **₪11**. רילס Hero של 30 שניות ≈ **₪127** (בתמחור ללקוח ₪167).
5. **עברית:** דיבור עברי מצלמים באמת ומעבירים ב-V2V עם פסקול המקור. שורת דיאלוג בעברית בתוך פרומפט אנגלי היא ניסוי בלבד (פרק 11 §8).

---

## 0. איך להשתמש בספרייה

### 0.1 זרימה בשישה צעדים

| # | צעד | זמן | איפה בפרק |
|---|---|---|---|
| 1 | בוחרים פורמט לפי המטרה: צפיות, לקוח או מוצר שלך | 2 דק' | סעיף 3 + אינדקס בסעיף 7 |
| 2 | אוספים רפרנסים לפי הצ'קליסט. אם חסרה תמונה טובה, מייצרים keyframe | 10–20 דק' | סעיפים 4 ו-5 |
| 3 | מעתיקים את הפרומפט וממלאים `[סוגריים]`. בפורמט חדש: תבנית מאסטר או meta-prompt | 5–15 דק' | סעיפים 1 ו-2 |
| 4 | טיוטה ב-480p (ב-Higgsfield: ‏Draft Mode), ‏8–10 שניות | 3–10 דק' | — |
| 5 | בודקים פנים, ידיים, טקסט, ספירת אובייקטים ו-2 השניות הראשונות. משנים **משתנה אחד** ומריצים שוב (עד 3 פעמים) | 10–30 דק' | סעיף 6 (negatives) |
| 6 | ‏1080p לקליפ שעבר. בעריכה: כתוביות, לוגו אמיתי, אודיו מקורי, תווית AI | — | פרק 03 §7–10 |

**שלושה דברים שאסור לשכוח:**
- **מחליפים טוקנים לפי הממשק.** ב-Higgsfield הטוקן הוא `@Image 1` (עם רווח). ב-Lovart הוא `@Video1`. ב-Kling ‏`@Element1`. ב-Veo ובכלים בלי טוקנים כותבים "the man from the reference image". משתמשים בדיוק בטוקן שהממשק מכניס כשלוחצים על הנכס (פרק 03 §4.4).
- **לא מפנים למשבצת ריקה.** אם אין `@Image4`, מוחקים כל שורה שמזכירה אותו.
- **ארוך = מפוצל.** רילס של 40–60 שניות הוא 2–6 ג'נרציות שמחברים בעריכה. ב-V2V וב-Infinite Angles עובדים תמיד בקטעים של 3–8 שניות (הטיפ של rourke, פרק 00).

### 0.2 מפתח עלויות (לפי פרק 10)

"תכנון" = עלות צפויה כולל טיוטות 480p וניסיונות חוזרים. "תמחור" = המספר שמכניסים להצעת מחיר. כשרשום **[נגזר]**, המספר חושב כאן לפי מחיר ה-API ויחס הניסיונות של פרק 10 §1.1, ולא הופיע בפרק 10 עצמו.

| מנוע | יחידה לתכנון | יחידה לתמחור | דוגמאות (תכנון / תמחור) | מקור |
|---|---|---|---|---|
| **Seedance 2.5, ‏Image→Video, ‏1080p** | **‏₪4.2 לשנייה סופית** | ‏₪5.6 לשנייה | ‏8 ש': ₪34/45 · ‏10 ש': ₪42/56 · ‏15 ש': ₪63/83 · ‏30 ש': ₪127/167 | פרק 10 §1.2 (850/1,120 קרדיט ל-30 ש') |
| **Genjutsu V2V, ‏1080p** | **‏₪4.6 לשנייה** | ‏₪6.8 לשנייה | ‏10 ש': ₪46/68 · ‏15 ש': ₪71/104 · ‏30 ש': ₪138/205 | פרק 10 §1.2 |
| Genjutsu V2V, ‏720p (לחשבון שלך) | ‏₪2.3 לשנייה | — | ‏15 ש': ₪34 | פרק 10 §1.2 |
| **Seedance 2.5 Edit (Infinite Angles), ‏1080p** | **‏₪2.7 לשנייה** | ‏₪3.8 לשנייה | ‏10 ש': ₪27/38 · ‏20 ש': ₪54/75 · ‏30 ש': ₪80/113 | פרק 10 §1.2 (×0.6 [לא מאומת ב-Higgsfield]) |
| **Kling 3.0, ‏1080p** (אפליקציית Kling Pro) | **‏₪1.1 לשנייה** (עם אודיו ₪1.6) | אותו דבר | ‏8 ש': ₪9 · ‏10 ש': ₪11 · ‏15 ש': ₪16 | פרק 10 §1.2 |
| Kling 3.0 ב-4K | ‏≈₪3.9 לשנייה | אותו דבר | ‏6 ש': ≈₪22 | **[נגזר]**: ‏$0.33–0.37 לשנייה (פרק 02 §1) ×3.5 ניסיונות |
| Kling 3.0 Turbo (דיבור באנגלית, ליפ-סינק) | ‏≈₪1.5 לשנייה | אותו דבר | ‏10 ש': ≈₪15 | **[נגזר]**: ‏$0.11–0.14 לשנייה ×3.5 |
| Kling Motion Control (ריקוד, טרנד) | ‏≈₪1.2 לשנייה | אותו דבר | ‏10 ש': ≈₪12 | **[נגזר]**: ‏$0.112 לשנייה (פרק 03 §6.1) ×3.5 |
| Veo 3.1 Fast / Standard | ‏≈₪1.1 / ₪3.6 לשנייה | אותו דבר | קליפ של 8 ש': ≈₪9 / ₪29 | פרק 10 §1.2 (מסלול D: ‏₪33/₪109 ל-30 ש') |
| Runway Aleph 2.0 (עריכה מקומית) | ‏≈₪3.3–5.1 לשנייה | אותו דבר | ‏10 ש': ≈₪33–51 | **[נגזר]**: ‏$0.44–0.67 לשנייה ×2.5 |
| **טיוטה בודדת, Seedance 2.5 ב-480p** | ‏₪0.45 לשנייה | — | ‏10 ש': ₪4.5 | פרק 10 §1.2 |
| **תמונה / keyframe** (Nano Banana Pro) | ‏≈₪0.3 לתמונה (~2 קרדיט) | — | ‏4 וריאציות: ≈₪1.2 | פרק 02 §3.4, §5.1 |

**כלל אצבע לתמחור (פרק 10 §1.2):** עלות הכלים היא 5%–20% מהמחיר ללקוח. העלות האמיתית היא זמן. לכן **לא נותנים הנחה של 50% על רילס קצר.**

### 0.3 איזה מנוע לאיזה פרומפט (תקציר מפרק 02 ופרק 03 §4.8)

| צריך | מנוע ברירת מחדל | מגבלות שחשוב לזכור |
|---|---|---|
| פרסומת רב-שוטית מתמונה אחת, עד 30 ש' | **Seedance 2.5** (Higgsfield / invideo) | ‏4–30 ש', ‏24fps קבוע, עד 50 רפרנסים (בפועל 1–8) |
| צילום אמיתי ← עולם אחר, עם עברית | **Higgsfield Genjutsu** (Motion Transfer / Object Swap / Restyle) | קלט 4–30 ש', קובץ בלבד; בפועל 3–6 רפרנסים |
| זוויות חדשות מטייק אחד | **Seedance 2.5 Edit** (Lovart / Higgsfield / fal) | ‏1.8–30.2 ש', ≤200MB. ב-Lovart ייתכן איסור על פנים אמיתיות [לא מאומת] |
| שוט מוצר חד, B-roll זול | **Kling 3.0** (4K native) | עד 15 ש', עד 6 קאטים |
| דמות מדברת באנגלית | **Kling 3.0 Turbo** / ‏Veo 3.1 Fast | ‏Veo: ‏4/6/8 ש' לקליפ |
| טיוטה מהירה | Seedance 2.5 ב-480p / ‏Gemini Omni ב-360p | — |
| ריקוד או טרנד על דמות AI | **Higgsfield AI Influencer** / ‏Kling Motion Control | ידיים רחוק מהפנים |
| Sora | **לא.** נסגר ב-24.09.2026 | — |

### 0.4 בטיחות מותג: מה כותבים במקום שמות אמיתיים

לפי פרק 10 §4: מותג אמיתי מותר **רק בפיץ' פרטי**. בפרסום פומבי משתמשים במותג פיקטיבי או בעסק שנתן אישור בכתב, ו**אף פעם** לא במגנט לידים ("comment KEYWORD"). כל הפרומפטים בפרק כבר כתובים כך. כשמתאימים פרומפט מהרשת, מחליפים לפי הטבלה:

| במקום (לא לכתוב) | כותבים |
|---|---|
| דגם ספציפי של סופרקאר איטלקי | `a sleek yellow Italian-style supercar, no visible badges or logos` |
| מכונית ספורט גרמנית מוכרת | `a matte-black German-style sports coupe, no badges` |
| לימוזינה בריטית אולטרה-יוקרתית | `a stately black ultra-luxury British-style sedan, no grille emblem, no hood ornament` |
| מלון יוקרה מפורסם במונקו | `a grand Belle Époque luxury hotel facade on the Riviera, no signage` |
| שעון יוקרה ממותג | `a gold dress watch with no visible brand` |
| המגדל הגבוה בעולם | `a needle-thin supertall glass skyscraper` |
| "Apple-style" / "NASA suit" / "GoPro" | `minimal white tech-studio look` / `classic white astronaut suit, no patches` / `chest-mounted action camera` |
| מותג נעליים, משקה או קוסמטיקה | מותג פיקטיבי (למשל `"NOIR roasters"`, `"Sela Skin"`), או המוצר האמיתי של לקוח שאישר |

ובכל פרומפט: `no logos, no badges, no readable signage`. לוגו אמיתי של לקוח מוסיפים **בעריכה** (tracking ב-CapCut / After Effects) ולא בג'נרציה.

### 0.5 מוסכמות בפרק

- `[CAPS IN BRACKETS]` = ממלאים. `[A / B]` = בוחרים אחד.
- כל פרומפט וידאו מופיע עם כרטיס של חמש שורות: **שימוש · מודל והגדרות · רפרנסים · עלות (תכנון / תמחור) · הערה**.
- ‏9:16 הוא ברירת המחדל בכל מקום. "Draft→1080p" פירושו טיוטה ב-480p ואז אותו פרומפט ב-1080p.
- המספור (V01–V72, ‏K01–K25) קבוע, כדי שיהיה אפשר להפנות אליו מלקוח, מקורס או מ-DM.

---

## 1. תבניות מאסטר (ממלאים את החסר)

### 1.1 MASTER-A: פרסומת רב-שוטית מתוזמנת, Seedance 2.5 (Image→Video)

**מתי:** כל פרסומת של 8–30 שניות מתמונה אחת או כמה תמונות (בסגנון edbert_yienson). **הגדרות:** ‏Seedance 2.5 · ‏Image→Video (או Reference) · ‏9:16 · ‏480p→1080p · ‏8–30 ש'. **עלות:** ‏₪4.2 לשנייה בתכנון. **[לא נבדק בפועל]**

**כללי מילוי:** ציר רציף בלי חורים ובלי חפיפות. שוט של 1.5–3 ש' לפרסומת, 4–8 ש' לדרמה. מיקום אחד לכל שוט. תנועת מצלמה אחת לכל שוט. ‏60–100 מילים לקליפ בודד, ‏250–600 מילים ל-15–30 ש'. כמה שפחות זמן מסך לפנים, כך פחות דריפט.

```
ASSET BINDING:
@Image1 = [MAIN CHARACTER]'s face and identity only — keep facial features identical in every shot; ignore its background, lighting and clothing.
@Image2 = [same person, left 3/4 profile / full body] — identity support only.
@Image3 = [PRODUCT / VEHICLE / HERO PROP] — exact shape, color and proportions; no logos added.
@Image4 = [LOCATION or STYLE reference] — [color palette and atmosphere only]; do not copy any people from it.

GLOBAL STYLE: [premium automotive commercial / luxury lifestyle ad / product film / documentary], 9:16 vertical, photoreal, [teal-and-orange / warm golden / cool clean] grade, [crisp digital / 35mm film grain], 24fps, no on-screen text, no logos, no watermark.

SCENE: [The man from @Image1, black tailored suit,] [does what] [where], [time of day], [mood in 3 words].

TIMELINE:
0:00-0:0[X]  Shot 1: [subject + action with strong verbs]. [shot size + angle], [lens mm], [light source + direction]. Camera: [ONE move] ending [end state]. [How the shot ends: exits frame / pulls away / holds]. Hard cut.
0:0[X]-0:[Y]  Shot 2: [...]. Hard cut.
0:[Y]-0:[Z]  Shot 3: [...]. [Match cut on / whip-pan to] Shot 4.
0:[Z]-0:[END]  Final shot: locked-off [hero framing]; [subject] [drives / walks] through and out of frame. Hold 1s on [the empty frame / the product].

PHYSICS: [fabric lags behind motion / wheels rotate correctly / liquid has real weight / feet plant firmly].

AUDIO: [SFX: ...], [Ambience: ...], [Music: "no music" OR genre + tempo]. [Dialogue (character): "..." OR "no dialogue"].

CONSISTENCY LOCKS: Face identical to @Image1 in every shot, zero drift. Same [car color and shape / outfit / product] throughout. Exactly [N] people. Same screen direction, never flip.

NEGATIVE: no [extra cars in lane / extra fingers / warped text / duplicate products / license plate text], no on-screen text.
```

### 1.2 MASTER-B: ‏Video→Video עם CHANGE/PRESERVE (Genjutsu / Seedance Edit)

**מתי:** "Reality-Swap" (חניון ← מלון), סטודיו ריק ← עולם מלא, סלון ← פנטהאוז, החלפת תלבושת. **הגדרות:** ‏Higgsfield Genjutsu ← Motion Transfer · קליפ מקור 8–15 ש' (עד 30) · ‏9:16 כמו המקור · ‏480p→1080p. **אודיו:** תמיד משתיקים את ה-AI ומניחים את ה-WAV המקורי. **עלות:** ‏₪4.6 לשנייה בתכנון (‏15 ש' ≈ ₪71). **[לא נבדק בפועל]**

```
Use @Video1 (the uploaded video) as reference for motion, timing, cuts, camera trajectory, framing, perspective and performance.

REFERENCES:
@Image1 = [my face, front, same day] — identity only.
@Image2 = [my full body in the target wardrobe] — wardrobe only.
@Image3 = [second actor: face + costume, e.g. chauffeur suit and cap].
@Image4 = [vehicle / product — generic, no badges].
@Image5 = [location look — generic, no signage].
@Image6 = [hero prop: gold watch with no visible brand / banknotes / leather suitcase].

CHANGE:
- Location: [original place] → [new place, time of day, 2–3 concrete details].
- Object: [original object] → [new object from @Image4], same position and scale.
- Wardrobe/character: [who] → [new look, see @Image2 / @Image3].

PRESERVE:
Keep every face identical to its reference, the original [Hebrew] dialogue and lip movement, every gesture, body movement, shot duration, camera motion, composition and interaction timing. [Keep the {prop} exactly as filmed.]

STYLE: photorealistic, lighting direction and intensity matched to the original footage, [warm luxury / cool night] grade.

NEGATIVE: no added text, logos, signs or watermarks; no extra people; no face drift.
```

**גרסת שורה אחת** (כמו בממשק שנראה ברילס של Higgsfield, פרק 00):
```
Same video, but [inside a crowded subway car / on a medieval battlefield / in a sea-view penthouse]. Keep the actor's motion, face and timing exactly.
```

**תוספת חירום** (כשהמודל משנה גם את התנועה, פרק 11 §5.2):
```
Preserve the original performance exactly. Only modify the environment and wardrobe.
```

### 1.3 MASTER-C: ‏Infinite Angles, ‏Seedance 2.5 Edit (שיטת rourke)

**מתי:** טייק אחד רחב ונעול ← "קאברג' של צוות 3 מצלמות". **הגדרות:** ‏Seedance 2.5 Edit/Reference · ‏`@Video1` = הטייק · ‏9:16 · קטעים של 3–8 ש', ‏1–2 זוויות לכל קטע · ‏480p→1080p · פסקול המקור הרציף בעריכה. **עלות:** ‏₪2.7 לשנייה בתכנון. **[לא נבדק בפועל]**

**שלב 1, הרשימה הקצרה** (זה מה ש-rourke הדביק ב-Claude; [נראה ברילס]):
```
00:00 Tracking shot to [NAME]
[mm:ss] Close up slow motion
[mm:ss] Low angle
[mm:ss] Top down shot
[mm:ss] Extreme close up
[mm:ss] Camera inside the [cup / pot / box]
[mm:ss] Tracking shot of the [prop]
[mm:ss] Dolly zoom
Keep the location, dialogue, and actions identical to the original video.
```

**שלב 2, הפורמט של כל שוט בפרומפט המורחב:**
```
[mm:ss-mm:ss] Shot N: [NAME] from @Video1 [action], same performance and dialogue. [Angle + height], [move]. [Lens feel: wide / standard prime / macro]. [Light as in source]. [Handheld micro-drift / locked-off / slow dolly]. Hard cut to Shot N+1.
```
(את ההרחבה המלאה עושה ה-meta-prompt בסעיף 2.2.)

### 1.4 MASTER-D: קליפ קצר בחמישה חריצים (Kling 3.0 / Veo 3.1 / כל מודל)

**מתי:** B-roll, שוט מוצר, אוכל, שוט בודד של 5–10 ש'. ‏60–100 מילים. **עלות:** ‏Kling 3.0: ‏≈₪11 ל-10 ש'. **[לא נבדק בפועל]**
```
[SUBJECT: who/what + 1–2 concrete attributes] [ACTION: one verb chain with a physical consequence] in [SCENE: place + one environmental detail], [LIGHT: source + direction]. Camera: [shot size, angle, lens mm], [EXACTLY ONE move] ending [end state]. [STYLE: grade / film look]. Audio: [named sounds], [no music / music genre]. [NEGATIVE: 3–5 targeted items].
```
**Kling (שדה negative נפרד):** `no sliding feet, no distorted hands, stabilized camera, no text glitches on signs`.
**Veo (דיאלוג):** `[Character], [tone]: "line in quotes."` ‏+ `SFX: ...` ‏+ `Ambient noise: ...`, כל רכיב במשפט נפרד.

### 1.5 MASTER-E: ‏Object Swap ("Fix it in post")

**מתי:** אותו צילום, מוצר אחר לכל SKU, צבע, שוק או חג. **הגדרות:** ‏Genjutsu Object Swap / ‏Kling O1 Edit (3–10 ש') / ‏Runway Aleph 2.0 / ‏Seedance 2.5 Edit עם טווח זמן. **עלות:** ‏Genjutsu ‏10 ש' ≈ ₪46. **[לא נבדק בפועל]**
```
Replace only the [bottle / can / sign / cup] in [the actor's right hand / the shop window] with the [product] from @Image1 — exact shape, color and label layout; label facing camera when held up. Match lighting, reflections and hand grip. Keep everything else in the shot unchanged: person, hands, background, lighting, camera.
```
**גרסה עם טווח זמן (Seedance 2.5 Edit):**
```
From [00:04]–[00:08], replace [the object] with [the product in @Image1]. Preserve the subject's identity, movement and camera trajectory. Change nothing else.
```
**חובה:** לוגו שנשבר מתקנים ב-tracking בעריכה. **אסור למסור ללקוח לוגו מעוות.** שינוי מחיר, תנאי מבצע או תוצאת מוצר הוא הטעיה (פרק 06).

---

## 2. Meta-prompts: ‏Claude / ChatGPT כותבים את הפרומפט בשבילכם

הזרימה של rourke (פרק 00): **רשימת שוטים קצרה ← LLM ← פרומפט מקצועי ← מחולל הווידאו.** מדביקים את ה-meta-prompt פעם אחת כ-system prompt, כ-Claude Project או כ-Custom GPT, ומשם שולחים רק בריף קצר, גם בעברית. **[לא נבדק בפועל]** כנכס: ה-meta-prompts האלה הם גם מוצר שאפשר למכור (חבילת פרומפטים, קורס).

### 2.1 M1: ‏"הבמאי" — מרשימת שוטים לפרומפט מלא (כללי)

עדכון של פרק 03 §4.9: נוספו שורת בטיחות מותג, הערכת עלות ופלט של בריף צילום.
```
You are a senior commercial director and AI-video prompt engineer. You write production prompts for Seedance 2.5 (default) and can convert them to Kling 3.0, Veo 3.1 or Gemini Omni Flash on request. Never mention or target Sora (discontinued).

INPUT I will give you (any language, often Hebrew):
- Format & goal (ad / vlog / drama / product / V2V reality-swap / infinite angles), platform & aspect ratio (default 9:16), total duration (max 30s Seedance 2.5, 15s Kling 3.0, 8s per Veo clip, 10s per Gemini Omni clip).
- My assets: list of @Image / @Video / @Audio and what each one is.
- A rough shot list, optionally with timecodes (e.g. "00:00 tracking shot / 03:07 close up slow motion / 06:14 top down").
- Must-keep rules (e.g. "keep location, dialogue and actions identical to @Video1").

OUTPUT exactly this structure, in English (keep any dialogue in its original language inside quotes):
1. ASSET BINDING — one line per asset: "@Image1 = <one job only>; do not take its <X>." Never reference an asset I did not list.
2. GLOBAL STYLE — genre, grade, film/digital look, aspect ratio, frame rate, what must NOT appear.
3. SCENE — one-sentence logline.
4. CHARACTERS / PRODUCT — concrete physical attributes + reference tags.
5. TIMELINE — continuous, gap-free timecodes covering the full duration. For each shot:
   [mm:ss-mm:ss] Shot N: subject + action (strong verbs, physical consequences) · shot size & angle · lens (mm) · light source & direction · EXACTLY ONE camera move with end state · how the shot ends · transition.
   Rules: 1.5–3s shots for ads, 4–8s for drama; one location per shot; never two camera moves in one shot; keep the main face on screen only where needed.
6. PHYSICS — weight, fabric, hair, liquids, speed ramps (only where relevant).
7. AUDIO — Dialogue (character): "..." / SFX / Ambience / Music — or explicitly "no music".
8. CONSISTENCY LOCKS — face, wardrobe, product, member count, screen direction.
9. NEGATIVE LINE — 3–6 targeted items, phrased specifically.

Then add:
- SPLIT PLAN: how to split into 2–4 shorter generations if the full one fails.
- WEAK SPOTS: the 2–3 shots most likely to fail (hands, text, fast motion) and one fallback for each.
- SHORT VERSION: a 60–100 word single-clip version.
- SHOOT BRIEF (only if a source video is needed): 5 bullet points on how to film it on a phone (9:16, tripod, light, take length, proxy props).
- COST CHECK: total generated seconds at final resolution, so I can estimate credits.

Hard rules: no real brand names, logos, car models, hotel names or celebrity likeness — replace them with generic descriptions ("Italian-style supercar, no badges"). No on-screen text unless I ask. Never use empty adjectives (stunning, epic, 8K, masterpiece); prefer verbs, named light sources and lens numbers. Ask at most 2 questions, only if a critical input is missing; otherwise state your assumptions in one line.
```

**בריף לדוגמה (נשלח אחרי ה-meta-prompt):**
```
פורמט: פרסומת לבית קפה שכונתי בתל אביב, 9:16, 20 שניות, Seedance 2.5 Edit.
נכסים: @Video1 = צילום טלפון של הבריסטה מכין קפה (טייק אחד רחב ונעול). @Image1 = לוגו (רק לכוס בסוף; אם יישבר, אוסיף בעריכה).
שוטים: 00:00 tracking to barista / 03:00 macro espresso pour slow motion / 07:00 top down latte art / 11:00 camera inside the cup looking up / 15:00 customer first sip close up / 18:00 wide locked-off hero.
Keep location, actions and timing identical to @Video1.
```

### 2.2 M2: ‏Infinite Angles — הרחבת רשימת timecodes (Seedance 2.5 Edit)

מבוסס על המבנה של [fal](https://fal.ai/learn/tools/how-to-create-multi-angle-video-seedance-2-5) ועל פורמט השוט של rourke.
```
You are a cinematographer writing a Seedance 2.5 video-edit prompt.
Source: @Video1, a single locked-off wide take, [DURATION]s, 9:16. Setup: [describe set, person, props].
Shot list (my cut points): [paste timecoded list].
Talking windows from the transcript: [00:00-00:04, 00:09-00:15 ...].
Write one timecoded prompt in this structure:
THE TAKE: what @Video1 shows.
LOCKED ELEMENTS: nothing about the event changes — same location, actions, dialogue, wardrobe, props, timing; only camera position and lens change.
MOUTH MAP: whenever the mouth is in frame during a talking window, lips follow the original audio; never invent dialogue in quiet windows.
WHERE HE LOOKS: eyes stay on the original A-camera position unless stated.
CLOCK: real-time playback, no retiming, except where slow motion is requested.
COVERAGE: for each shot — [start-end] Shot N: subject, camera placement, lens feel (wide / standard prime / macro), depth of field, ONE movement (dolly, handheld micro-drift, crane), lighting as in the source, transition ("Hard cut to Shot N+1").
CONTINUITY BIBLE: performer, wardrobe, prop count (exactly one [lemon / cup]), set.
CONSTRAINTS: no crew, no lighting rigs, no extra props, no text, no duplicated objects.
Finally, split the result into chunks of 3–8 seconds with 1–2 angles each, so I can generate them one by one.
```

### 2.3 M3: ‏"עשר מודעות ממוצר אחד" (e-commerce, לפי E4 §7.4)
```
You are a performance creative director for Meta & TikTok ads.
Product: [name, what it is, price in ILS, audience, 3 TRUE benefits, forbidden claims].
Reference: @Image1 = product photo (front, label legible). @Image2 = 3/4 view (optional).
Create 10 ad concepts that are RADICALLY different (format, setting, persona, emotion) so the ad system treats them as separate ads: hero packshot, UGC selfie, ASMR unboxing, impossible scale, timecoded multi-angle, retro era, problem→solution (no medical claims), Israeli lifestyle, luxury/fake-rich humor, absurd AI character meme.
For each: (1) one-line concept, (2) a Seedance 2.5 prompt, 9:16, 8–15s, timecoded shots with camera / lens / light / movement / how each shot ends, (3) append the PRODUCT LOCK paragraph below, (4) 3 Hebrew on-screen hooks of ≤8 words, (5) a Hebrew CTA.
PRODUCT LOCK: The product must match @Image1 exactly — same shape, proportions, colors, cap, label layout and logo. Do not redesign, rename, add text or change the label. Keep the logo sharp and readable; if unsure, keep the label partially turned away rather than distorted.
Never write fake testimonials, fake numbers, fake discounts or before/after results. Never use real third-party brands.
```

### 2.4 M4: ‏"תקן רק את שוט N" (איטרציה בלי לשרוף קרדיטים)
```
Here is my Seedance 2.5 prompt and what went wrong in the 480p draft.
Prompt: [paste]
Problem: [e.g. "Shot 4: fingers melt into the steering wheel; Shot 6: the car turns red"].
Change ONE variable only. Give me 3 alternative versions of the failing shot(s), each with a one-line reason, keeping every other line of the prompt byte-for-byte identical. If the shot is likely to keep failing, propose a fallback (wider shot, hands partly out of frame, cut it and redistribute its seconds).
```

### 2.5 M5: ‏"מנקה מותגים" (לפני פרסום פומבי)
```
Rewrite the following video prompt so it contains no real brand names, car models, hotel names, landmarks that are registered trademarks, celebrity names or logos. Replace each with a vivid generic description that keeps the same look (e.g. "a stately black ultra-luxury British-style sedan, no grille emblem"). Add "no logos, no badges, no readable signage" to the negative line. Return the rewritten prompt and a 2-column table: original term → replacement.
[paste prompt]
```

### 2.6 M6: ‏מבריף עברי של לקוח לתוכנית צילום + פרומפט
```
You are my production assistant. Below is a client brief in Hebrew (a WhatsApp voice-note transcript).
1. Summarize it in 5 Hebrew bullet points (goal, product, audience, tone, must-have shot).
2. Pick the best format from: Image→Video multi-shot (Seedance 2.5), V2V reality-swap (Genjutsu), Infinite Angles (Seedance 2.5 Edit), product hero (Kling 3.0), UGC (Kling 3.0 Turbo + Hebrew voice-over). Justify in one line.
3. Write the Hebrew WhatsApp message I send the client listing exactly what to film or photograph (phone, 9:16, light, files as "document", no filters).
4. Write the full English prompt (timecoded, 9:16, ≤30s) following the rules of my director prompt.
5. List generated seconds per resolution (480p drafts + final) so I can price it.
Brief: [paste]
```

---

## 3. ספריית הווידאו: 72 פרומפטים לפי פורמט

> כל הפרומפטים בסעיף **[לא נבדק בפועל]**. העלויות לפי המפתח בסעיף 0.2 (תכנון / תמחור).

### A. יוקרה ו"פייק עשיר" (Image→Video)

**V01 · "תמונת פספורט אחת ← פרסומת סופרקאר" (30 ש', גרסת הייחוס)** [לא נבדק בפועל]
- **שימוש:** הרילס של edbert_yienson (24K תגובות), בגרסה בלי מותגים. פורמט "INPUT + PROMPT + RESULT" על המסך, ומשפך "STEAL MY PROMPT".
- **מודל והגדרות:** ‏Seedance 2.5 · Image→Video · ‏30 ש' · ‏9:16 · ‏480p→1080p · מצלמה: FPV dive, ‏lateral tracking, ‏macro, ‏locked-off.
- **רפרנסים:** תמונת פספורט אחת (רקע אפור, ז'קט שחור, אור רך). רצוי גם 3/4 שמאל (K01, ‏K03).
- **עלות:** ‏₪127 / ₪167.
- **הערה:** הפרומפט המקורי מתומלל בפרק 00. כאן הגרסה המתוקנת: ציר רציף, בלי חפיפות, ובלי מגדל או רכב מזוהים. אם 2–3 שוטים נכשלים, מפצלים ל-3 ג'נרציות של 10 ש'.
```
@Image1 is the driver's face and identity only — keep facial features identical in every shot; ignore its background and lighting.
GLOBAL STYLE: premium automotive commercial, 9:16, photoreal, teal-and-orange grade, anamorphic flares, crisp 1080p, no on-screen text, no logos, no badges.
SCENE: The man from @Image1, black tailored suit, drives a sleek yellow Italian-style supercar with no visible badges through a desert skyline city at golden hour.
0:00-0:06  Continuous FPV aerial dive from the tip of a needle-thin supertall glass skyscraper down toward street level; the yellow supercar is picked out on the right side of frame as it comes into view.
0:06-0:09  Lateral tracking shot at wheel height; camera holds the side profile, then the car accelerates and overtakes the camera, exiting frame left. Hard cut.
0:09-0:11  Inside the cabin, center rear-view mirror shot: his eyes in the mirror, skyline receding behind.
0:11-0:13  Nose-on low angle, headlights filling frame, heat shimmer off the asphalt.
0:13-0:16  Cockpit view from the passenger side, 35mm: his face in 3/4, calm half-smile, one hand on the wheel.
0:16-0:19  Rear-bumper 3/4 tracking shot, the car pulling away down an empty straightaway.
0:19-0:23  Macro insert: wheel spinning, brake caliper glowing, speed ramp into slow motion.
0:23-0:27  Lateral profile hold again; the car accelerates and passes the camera a second time.
0:27-0:30  Locked-off 3/4 wide shot at sunset; the car drives through and out of frame. Hold on the empty road.
AUDIO: engine roar rising on each pass, tire hiss, wind, deep cinematic bass hits on cuts, no dialogue.
CONSTRAINTS: same car color and shape in every shot, no extra cars in lane, no license plate text, no warped text, no face drift.
```

**V02 · אותו רעיון ב-10 שניות (הרילס הראשון שלך)** [לא נבדק בפועל]
- **שימוש:** הניסיון הראשון בפרק 11. ‏4 שוטים במקום 9, כי 9 שוטים ב-10 ש' יוצרים מורפינג.
- **מודל והגדרות:** ‏Seedance 2.5 · I2V · ‏10 ש' (או 8) · ‏9:16 · ‏480p (Draft) ואז 1080p.
- **רפרנסים:** תמונת פנים אחת.
- **עלות:** טיוטה ₪4.5. גמור ₪42 / ₪56.
- **הערה:** בגרסת 8 ש' מוחקים את השוט השלישי ומשנים את האחרון ל-`0:05-0:08`.
```
@Image1 is the driver's face and identity only — keep facial features identical in every shot; ignore its background and lighting.
STYLE: premium automotive commercial, 9:16 vertical, photoreal, golden hour, teal-and-orange grade, no on-screen text, no logos, no badges.
SCENE: The man from @Image1, black tailored suit, drives a sleek yellow Italian-style supercar with no visible badges through a modern coastal skyline city.
0:00-0:03  Continuous aerial drone dive from above the glass towers down toward the street; the yellow supercar comes into view on the right side of frame.
0:03-0:05  Lateral tracking shot at wheel height; the car accelerates and overtakes the camera, exiting frame left. Hard cut.
0:05-0:08  Cockpit view from the passenger side, 35mm: his face in 3/4, calm half-smile, one hand on the wheel, city lights sliding past the window.
0:08-0:10  Locked-off low 3/4 wide shot; the car drives through and out of frame. Hold on the empty road.
AUDIO: engine roar rising on the pass, tire hiss, wind, one deep bass hit on each cut, no dialogue, no music.
CONSTRAINTS: same car color and shape in every shot, no extra cars in lane, no license plate text, no face drift.
```

**V03 · בוקר בפנטהאוז (פייק עשיר, 15 ש')** [לא נבדק בפועל]
- **שימוש:** סדרת "מיליונר מזויף" לחשבון שלך, או ספק-אד לנדל"ן יוקרה.
- **מודל והגדרות:** ‏Seedance 2.5 · I2V · ‏15 ש' · ‏9:16 · ‏1080p · מצלמה: push-in, ‏insert, ‏crane.
- **רפרנסים:** ‏K01 (anchor), ‏K02 (גיליון דמות), ‏K18 (פנטהאוז).
- **עלות:** ‏₪63 / ₪83.
- **הערה:** השעון וה"עושר" הם אביזרים גנריים. בטקסט על המסך מוסיפים הומור עצמי ("בפועל: דירת 3 חדרים בבת ים").
```
@Image1 = the man's face and identity only. @Image2 = full-body reference, same person — proportions only. @Image3 = penthouse interior look only; do not copy people.
GLOBAL STYLE: luxury lifestyle commercial, 9:16, photoreal, warm golden morning grade, 35mm film grain, no on-screen text, no logos.
SCENE: The man from @Image1 starts his morning in a sea-view penthouse, unhurried, confident.
0:00-0:03  Wide, 16mm, locked-off: floor-to-ceiling curtains open by themselves, sunlight floods across a marble floor; he stands silhouetted at the window.
0:03-0:06  Insert, 100mm macro: his hand fastens a gold dress watch with no visible brand; shallow depth of field. Hard cut.
0:06-0:09  Medium shot, 50mm, eye level: he pours espresso from a steel machine, steam rising, window light from camera left; slow push-in.
0:09-0:12  Over-the-shoulder on the terrace, 35mm: he sips, the sea below; handheld micro-drift.
0:12-0:15  Crane up and back from the terrace to reveal the coastline; he raises the cup toward camera. Ends locked-off.
AUDIO: soft waves, espresso machine hiss, distant gulls, light piano, no dialogue.
CONSISTENCY LOCKS: face identical to @Image1 in every shot, same white linen shirt throughout.
NEGATIVE: no extra people, no warped watch dial text, no logos.
```

**V04 · עלייה למטוס פרטי (12 ש')** [לא נבדק בפועל]
- **שימוש:** "פייק עשיר", או סיום של רילס נסיעות.
- **מודל והגדרות:** ‏Seedance 2.5 · I2V · ‏12 ש' · ‏9:16 · ‏1080p · מצלמה: tracking, ‏low angle, ‏locked-off.
- **רפרנסים:** ‏K01, ‏K02. אופציונלי: מזוודה (K12).
- **עלות:** ‏₪50 / ₪67.
- **הערה:** מטוס בלי לוגו ובלי מספר זנב. ידיים על המעקה הן נקודת סיכון, ולכן הן חלקית מחוץ לפריים.
```
@Image1 = the man's face and identity only; ignore its background.
GLOBAL STYLE: luxury travel commercial, 9:16, photoreal, warm sunset grade, no on-screen text, no logos, no tail numbers.
0:00-0:03  Low angle, 24mm: a white private jet with no markings on a tarmac at sunset, a red carpet runs to the airstairs; heat haze.
0:03-0:06  Backward tracking shot at chest height, 35mm: the man from @Image1, navy suit and sunglasses, walks toward camera pulling a cognac leather suitcase; jacket lifts in the wind.
0:06-0:09  Profile medium shot: he climbs the airstairs, hand partly out of frame on the rail; flight attendant nods at the door.
0:09-0:12  Locked-off wide from the runway: the door closes, engines spool, the sun touches the horizon. Hold.
AUDIO: jet engine whine building, wind, suitcase wheels on asphalt, no music, no dialogue.
CONSISTENCY LOCKS: face identical to @Image1, same suit throughout. NEGATIVE: no extra aircraft, no text on the fuselage.
```

**V05 · סיפון יאכטה בריביירה (10 ש')** [לא נבדק בפועל]
- **שימוש:** הוק "איפה צילמתי את זה?" לפני חשיפת המקור (סלון).
- **מודל והגדרות:** ‏Seedance 2.5 · I2V · ‏10 ש' · ‏9:16 · ‏1080p · מצלמה: drone pull-back, ‏medium.
- **רפרנסים:** ‏K01, ‏K02.
- **עלות:** ‏₪42 / ₪56.
- **הערה:** מים ושיער ברוח הם מבחן פיזיקה טוב. אם השיער "מתנפח", מוסיפים `hair moves gently, no exaggerated motion`.
```
@Image1 = the man's face and identity only.
GLOBAL STYLE: Riviera lifestyle ad, 9:16, photoreal, bright Mediterranean noon, crisp digital look, no on-screen text, no logos.
0:00-0:04  Medium shot, 50mm: the man from @Image1, white linen shirt, leans on the teak rail of a sleek white motor yacht, turquoise water behind; he turns to camera and lifts his sunglasses.
0:04-0:07  Insert, 85mm: a glass of sparkling water on the rail, condensation, sea glitter in bokeh.
0:07-0:10  Drone pulls up and back from the bow, revealing the cliffside coastline and the wake; ends locked-off high.
AUDIO: water slapping the hull, wind, distant gulls, soft house beat, no dialogue.
CONSISTENCY LOCKS: face identical to @Image1. NEGATIVE: no extra boats crossing the frame, no text on the hull.
```

### B. רכבים

**V06 · נסיעת לילה גשומה בתל אביב (10 ש')** [לא נבדק בפועל]
- **שימוש:** B-roll לחשבון רכב, ספק-אד לסוחר רכב, הוק אווירה.
- **מודל והגדרות:** ‏Kling 3.0 (או Seedance 2.5) · Text→Video · ‏10 ש' · ‏9:16 · ‏1080p · מצלמה: low tracking, ‏OTS, ‏drone pull-up.
- **רפרנסים:** אין. אופציונלי: תמונת הרכב של הלקוח.
- **עלות:** ‏Kling ‏₪11 (עם אודיו ₪16). ב-Seedance ‏₪42.
- **הערה:** ב-Kling מעבירים את שורת ה-negative לשדה הייעודי.
```
A matte-black German-style sports coupe with no badges cruises through rain-soaked Tel Aviv at night. 0-3s: low tracking shot at wheel height, neon reflections streaking across the wet bodywork. 3-6s: hard cut, interior over-the-shoulder of the driver, dashboard glow on his face, 35mm. 6-10s: drone pulls up and back from the car at a traffic light, city lights spreading out, ends locked-off. Audio: flat-six exhaust burble, rain on glass, no music. No text on signs, no extra cars in lane, no license plate text.
```

**V07 · חשיפת רכב מתחת לבד משי (8 ש')** [לא נבדק בפועל]
- **שימוש:** השקת דגם אצל סוחר, "reveal" לליסינג.
- **מודל והגדרות:** ‏Kling 3.0 ב-4K (או Seedance 2.5) · ‏8 ש' · ‏9:16 · מצלמה: orbit של 90°.
- **רפרנסים:** אופציונלי: תמונת הרכב (3/4 קדמי) כ-`@Image1`.
- **עלות:** ‏Kling 1080p ‏₪9. ב-4K ≈ ₪31 [נגזר].
- **הערה:** הבד שמחליק הוא מבחן פיזיקה. אם הוא "נמס", מקצרים ל-6 ש'.
```
A silk cover slides off a red Italian-style supercar with no badges in a dark concrete studio. Single overhead softbox, everything else black. Camera: slow 90° orbit at headlight height, 50mm, ending on the front three-quarter. The silk ripples and pools on the floor with real weight. Dust particles glow in the light beam. Audio: fabric whoosh, one deep bass hit as the headlights flick on, then silence. No logos, no text.
```

**V08 · רכב יד שנייה ← פרסומת קולנועית (שרשור Genjutsu ← Seedance, ‏15 ש')** [לא נבדק בפועל]
- **שימוש:** שירות לסוחרי רכב: "צילמנו במגרש בחולון, יצאה פרסומת" (D3 R9).
- **מודל והגדרות:** שלב 1: Genjutsu Motion Transfer על 3 קליפים של סיבוב סביב הרכב (5 ש' כל אחד), ‏1080p. שלב 2 (אופציונלי): Seedance 2.5 Edit לזוויות.
- **רפרנסים:** הווידאו מהמגרש, ‏3 תמונות של הרכב (חזית, 3/4, צד), ‏K17 (כביש הרים).
- **עלות:** שלב 1: ‏₪71 / ₪104. עם זוויות: עוד כ-₪40.
- **הערה:** **צבע, צורה ומצב הרכב חייבים להישאר אמיתיים.** שינוי של מצב הרכב בפרסומת מכירה הוא הטעיה. לוחיות מטשטשים בעריכה.
```
Use @Video1 as reference for motion, timing and camera path.
CHANGE: the used-car lot becomes a wet mountain road at blue hour with hairpin turns and low mist; add soft streetlight reflections on the paint.
PRESERVE: the exact car from @Video1 and @Image1–3 — same model shape, paint color, wheels, dents and trim; same camera path and timing.
STYLE: cinematic car commercial, cool blue grade, photorealistic. Headlights switch on at the end of the clip.
NEGATIVE: no badges or logos added, no readable plates, no extra cars, no body-shape change.
```

**V09 · Detailing: לפני ואחרי במשיכת מטלית (8 ש')** [לא נבדק בפועל]
- **שימוש:** לקוח שטיפה/ליטוש/ציפוי קרמי. "Satisfying" עם replay גבוה.
- **מודל והגדרות:** ‏Kling 3.0 · ‏8 ש' · ‏9:16 · ‏1080p · מצלמה: tracking צמוד ליד.
- **רפרנסים:** אופציונלי: תמונת מכסה המנוע של הלקוח.
- **עלות:** ‏₪9.
- **הערה:** בפרסומת אמיתית ללקוח עדיף לצלם את התוצאה האמיתית ולהשתמש ב-AI רק לאווירה, כדי לא להבטיח תוצאה שלא קיימת.
```
Macro close-up on a dusty, swirled black car hood. A gloved hand sweeps a microfiber cloth from left to right; everything behind the cloth becomes a deep mirror-gloss finish reflecting the sky. Camera: slow tracking alongside the hand, 85mm. Overcast soft light. Audio: cloth swish, satisfying squeak, no music. Same car panel shape, no logos.
```

**V10 · ג'יפ בדיונות (10 ש')** [לא נבדק בפועל]
- **שימוש:** טיולי ג'יפים בערבה או במדבר יהודה, השכרת רכבי שטח.
- **מודל והגדרות:** ‏Seedance 2.5 · ‏10 ש' · ‏9:16 · ‏1080p · מצלמה: drone follow, ‏low angle.
- **רפרנסים:** אופציונלי: תמונת הרכב של הלקוח (`@Image1`).
- **עלות:** ‏₪42 / ₪56.
- **הערה:** חול שעף הוא חוזקה של Seedance. ביקשנו `wheels rotate correctly`, כי גלגלים "מחליקים" הם כשל נפוץ.
```
@Image1 = the off-road vehicle (body shape and color only, no badges).
GLOBAL STYLE: adventure commercial, 9:16, photoreal, warm late-afternoon desert grade, no on-screen text, no logos.
0:00-0:04  Drone follow shot from behind and above: the 4x4 from @Image1 crests a tall sand dune, sand plume trailing; camera keeps pace.
0:04-0:07  Low angle at sand level, 24mm: the vehicle drops over the ridge toward camera, sand sprays over the lens. Hard cut.
0:07-0:10  Locked-off wide: the vehicle stops on the ridge, silhouetted against the setting sun, dust drifting. Hold.
PHYSICS: wheels rotate correctly, suspension compresses on landing, sand has weight.
AUDIO: engine roar, sand hiss, wind, no music. NEGATIVE: no extra vehicles, no plate text.
```

### C. ‏POV ו-Vlog

**V11 · ‏Vlog היסטורי: לגיונר רומי (10 ש')** [לא נבדק בפועל]
- **שימוש:** ערוץ faceless של "vlog מהעבר" (פורמט ויראלי באנגלית).
- **מודל והגדרות:** ‏Veo 3.1 Fast (דיאלוג באנגלית) או Seedance 2.5 · ‏8–10 ש' · ‏9:16 · מצלמה: selfie handheld.
- **רפרנסים:** אין, או K21 (דמות קבועה לסדרה).
- **עלות:** ‏Veo Fast ‏≈₪9. ‏Seedance ‏₪42.
- **הערה:** ב-Veo מקצרים ל-8 ש'. הדיאלוג: כ-2.5 מילים לשנייה, כלומר עד 20 מילים.
```
Handheld selfie-vlog POV, smartphone wide lens, 9:16. A young Roman legionary in dusty armor holds the camera at arm's length and walks through a bustling Roman market in 50 AD, grinning. Dialogue (legionary, casual, out of breath): "Okay guys, day three of the campaign, and the bread here is honestly overrated." Background: merchants shouting, a goat crosses behind him, sunlight bouncing off white stone. Natural handheld shake, slight motion blur. Audio: crowd chatter, sandals on stone, no music.
```

**V12 · ‏POV גוף ראשון: אופני הרים (8 ש')** [לא נבדק בפועל]
- **שימוש:** B-roll לחנות אופניים, פארק אתגרי, ערוץ אקסטרים.
- **מודל והגדרות:** ‏Kling 3.0 · ‏8 ש' · ‏9:16 · ‏1080p · מצלמה: chest-mount, ‏fisheye.
- **רפרנסים:** אין.
- **עלות:** ‏₪9.
- **הערה:** תנועה מהירה "נמרחת". אם זה קורה, מוסיפים `slight speed ramp to slow motion at 4s`.
```
First-person POV from a chest-mounted action camera, fisheye. Hands grip the handlebars of a mountain bike racing down a narrow forest trail at speed, roots and rocks flashing past, sunlight strobing through the trees. Real vibration, mud spatter hits the lens at 4s. Audio: heavy breathing, tires on dirt, wind, no music. No logos on the bike.
```

**V13 · "יום בחיים" של יזם (רב-שוטי, 15 ש', שורה עברית ניסיונית)** [לא נבדק בפועל]
- **שימוש:** פרסונל ברנדינג, "AI me" לסדרה.
- **מודל והגדרות:** ‏Seedance 2.5 · I2V · ‏15 ש' · ‏9:16 · ‏1080p.
- **רפרנסים:** ‏K01 + ‏K03 (חיוך).
- **עלות:** ‏₪63 / ₪83.
- **הערה:** **השורה בעברית היא ניסוי** (פרק 11 §8). אם הדיבור יוצא ג'יבריש, משתיקים ומוסיפים voice-over אמיתי, או מוחקים את השורה.
```
@Image1 = the creator's face only.
0-3s: POV hand turns off a phone alarm at 5:00 AM, dim blue room light.
3-6s: hard cut, mirror selfie medium close-up, the man from @Image1 ties his tie, window light from camera left.
6-10s: handheld walk-and-talk on a Tel Aviv street at sunrise, phone held at arm's length, he says: "בוקר טוב, יום ראשון של הסטארטאפ."
10-15s: over-the-shoulder at a laptop in a café, steam rising from coffee, slow push-in to the screen.
Audio: street ambience, coffee machine hiss, light lo-fi beat. Face identical in every shot. No readable text on the laptop screen.
```

**V14 · ‏Vlog תנ"כי בעברית (8 ש')** [לא נבדק בפועל]
- **שימוש:** סדרת "אם היה להם טלפון" (D3 R6), תוכן עונתי לחגים.
- **מודל והגדרות:** ‏Seedance 2.5 או Veo 3.1 · ‏8 ש' · ‏9:16 · מצלמה: selfie-stick.
- **רפרנסים:** אופציונלי: דמות קבועה מ-K21.
- **עלות:** ‏Seedance ‏₪34. ‏Veo Fast ‏≈₪9.
- **הערה:** **רגישות דתית.** טון חיובי, בלי לעג. גם כאן העברית היא ניסוי.
```
Selfie-stick vlog, handheld, phone-camera look, 9:16. A bearded man in simple ancient robes stands on the shore of a parted sea, towering walls of water on both sides, a crowd walking behind him. He speaks to camera, amazed: "חברים, אתם לא מאמינים מה קרה עכשיו". Natural daylight, wind noise on the mic, slight lens shake. No on-screen text, no music.
```

**V15 · נוסע בזמן: נמל יפו, 1920 (10 ש')** [לא נבדק בפועל]
- **שימוש:** תוכן היסטורי מקומי, שיתוף פעולה עם מוזיאון או סיורים.
- **מודל והגדרות:** ‏Seedance 2.5 · ‏10 ש' · ‏9:16 · מצלמה: selfie handheld ‏+ hard cut.
- **רפרנסים:** ‏K01 (אתם כמגישים).
- **עלות:** ‏₪42 / ₪56.
- **הערה:** הבגדים המודרניים של המגיש יוצרים את הניגוד. כדאי לנעול אותם בפרומפט.
```
@Image1 = the host's face only; he wears a modern grey hoodie throughout.
GLOBAL STYLE: smartphone vlog look, 9:16, slightly warm, natural handheld, no on-screen text.
0:00-0:05  Selfie POV: the man from @Image1 walks through a crowded 1920s Jaffa port market, wooden boats behind him, porters carrying crates of oranges; he grins at the lens, eyebrows raised.
0:05-0:08  Hard cut, his POV: a fisherman in a flat cap hands him an orange; hands partly out of frame.
0:08-0:10  Selfie again, he bites the orange and nods to camera. Hold.
AUDIO: harbor bells, crowd chatter, waves on stone, gulls, no music, no dialogue.
CONSISTENCY LOCKS: same hoodie, face identical to @Image1. NEGATIVE: no modern cars, no readable signs.
```

### D. מוצר (Product hero)

> לכל פרומפט מוצר מצרפים את **PRODUCT LOCK** (סעיף 6.3). את התווית והלוגו האמיתיים מוסיפים בעריכה כ-end card.

**V16 · בושם: ‏orbit על אובסידיאן רטוב (10 ש')** [לא נבדק בפועל]
- **שימוש:** קוסמטיקה, בשמים, מוצר פרימיום.
- **מודל והגדרות:** ‏Seedance 2.5 (או Kling 3.0 ב-4K) · ‏10 ש' · ‏9:16 · מצלמה: orbit של 180°, ‏100mm macro.
- **רפרנסים:** ‏packshot חזית + 3/4 (K09, ‏K10).
- **עלות:** ‏Seedance ‏₪42 / ₪56. ‏Kling 1080p ‏₪11.
- **הערה:** אם התווית מתעוותת, מסובבים אותה חלקית מהמצלמה עד הפריים האחרון.
```
@Image1 = perfume bottle (shape, glass color, cap) — must match exactly; label legible and unchanged.
A crystal perfume bottle stands on wet black obsidian. Camera: slow 180° orbit at bottle height, 100mm macro, ending front-on. A single drop runs down the glass; at 4s a burst of golden mist sprays in slow motion, backlit so every droplet sparkles. Hard rim light from behind, soft fill from the left, deep black background. Audio: soft glass chime, mist hiss, low ambient pad. No extra bottles, no text.
```

**V17 · נעל ספורט: ‏splash בסלואו-מושן (6 ש')** [לא נבדק בפועל]
- **שימוש:** חנות נעליים, מותג פיקטיבי לתיק עבודות.
- **מודל והגדרות:** ‏Kling 3.0 ב-4K · ‏6 ש' · ‏9:16 · מצלמה: locked-off בגובה הקרקע.
- **רפרנסים:** נעל (צד + 3/4).
- **עלות:** ≈₪22 [נגזר].
- **הערה:** לא לבקש לוגו. מוסיפים אותו בעריכה.
```
A white running sneaker drops into a shallow pool of water in extreme slow motion, 1000fps look. A crown-shaped splash rises around the sole, droplets frozen mid-air. Camera locked-off at ground level, 85mm, shallow depth of field. Bright studio key from above, clean gradient grey backdrop. Audio: deep whoosh, single splash impact, silence. Shoe shape identical to @Image1, no logo distortion, no text.
```

**V18 · סרום: סרט מוצר רב-זוויתי (15 ש')** [לא נבדק בפועל]
- **שימוש:** "Infinite angles" למוצר בלי צילום מקור (E4 V5).
- **מודל והגדרות:** ‏Seedance 2.5 · I2V (reference) · ‏15 ש' · ‏9:16 · ‏1080p · 6 שוטים.
- **רפרנסים:** ‏K09 + ‏K10.
- **עלות:** ‏₪63 / ₪83.
- **הערה:** השוט "inside the bottle" הוא ההוק. אם הוא נכשל, מעבירים אותו לשנייה 0.
```
9:16, 15s, timecoded multi-shot product film; the bottle from @Image1 is the hero in every shot.
0:00-0:02 Extreme close-up of the dropper squeezing, golden drop forming, slow motion.
0:02-0:04 Camera inside the glass bottle looking out through the serum at a blurred face.
0:04-0:07 Top-down shot: the bottle on a vanity among fresh citrus slices, soft window light.
0:07-0:10 Low angle: the bottle on a wet rock, water splash in slow motion around it.
0:10-0:13 Dolly zoom on the bottle on a bathroom shelf.
0:13-0:15 Locked-off frontal packshot, label sharp. Hard cuts between shots.
PRODUCT LOCK: The product must match @Image1 exactly — same shape, proportions, colors, cap and label layout. Do not redesign, rename, add text or change the label; if unsure, keep the label partially turned away rather than distorted.
```

**V19 · אוזניות מרחפות (8 ש')** [לא נבדק בפועל]
- **שימוש:** גאדג'טים, חנויות סלולר.
- **מודל והגדרות:** ‏Kling 3.0 · ‏8 ש' · ‏9:16 · מצלמה: push-in איטי.
- **רפרנסים:** ‏packshot של המארז (סגור + פתוח).
- **עלות:** ‏₪9 (עם אודיו ₪13).
- **הערה:** "נפתח מעצמו" עובד טוב יותר כשיש תמונה של המארז הפתוח כרפרנס שני.
```
A wireless earbuds case (@Image1) floats and slowly rotates above a matte white plinth. The lid opens by itself, the earbuds rise out and hover, soft blue LED pulse. Camera: slow push-in, 85mm, ending on the open case. Minimal white tech-studio look, high-key light, soft shadow under the plinth. Audio: subtle magnetic click, airy whoosh, minimal electronic tone. No text, no extra devices, no logos.
```

**V20 · מזיגת משקה קר (8 ש')** [לא נבדק בפועל]
- **שימוש:** בתי קפה, מותגי משקאות, תפריט דיגיטלי.
- **מודל והגדרות:** ‏Kling 3.0 · ‏8 ש' · ‏9:16 · מצלמה: locked-off ‏100mm.
- **רפרנסים:** אופציונלי: הכוס הממותגת של הלקוח.
- **עלות:** ‏₪9.
- **הערה:** ‏speed ramp אחד בלבד. שניים יוצרים "קפיצות".
```
Ice cubes tumble in slow motion into a tall glass, then amber cold brew pours in, swirling with cream. Condensation beads run down the glass. Camera: locked-off side view, 100mm macro, backlight through the liquid creating a warm glow. Speed ramp: real-time pour, slow motion on the cream swirl. Audio: ice clinks, liquid pour, fizz, no music. No logos, no text.
```

**V21 · קנה מידה בלתי אפשרי (8 ש')** [לא נבדק בפועל]
- **שימוש:** ‏pattern interrupt למודעה (E4 V4).
- **מודל והגדרות:** ‏Seedance 2.5 · I2V · ‏8 ש' · ‏9:16 · מצלמה: drone push-in ← hard cut.
- **רפרנסים:** ‏packshot.
- **עלות:** ‏₪34 / ₪45.
- **הערה:** השוט השני (מוצר בגודל רגיל) מחזיר את הצופה למציאות, ושם מניחים את ה-CTA.
```
9:16, 8s. 0:00-0:05 The product from @Image1, scaled to the size of a building, stands in the middle of a calm desert at golden hour; a tiny person walks toward it, long shadows. Slow drone push-in from wide to medium. 0:05-0:08 Hard cut to the normal-size product on a bathroom shelf in the same warm light, locked-off. Photorealistic, commercial grade, no text.
PRODUCT LOCK: same shape, proportions, colors and label layout as @Image1; do not redesign or re-letter.
```

**V22 · פרסומת רטרו משנות ה-70 (10 ש')** [לא נבדק בפועל]
- **שימוש:** וריאציה שונה מאוד לבדיקת מודעות (E4 V6).
- **מודל והגדרות:** ‏Seedance 2.5 · ‏10 ש' · ‏9:16 עם מסגור בטוח של 4:3 · מצלמה: zoom-in בסגנון התקופה.
- **רפרנסים:** ‏packshot.
- **עלות:** ‏₪42 / ₪56.
- **הערה:** המוצר עצמו נשאר מודרני. רק העולם רטרו.
```
1970s TV commercial look, 9:16 with 4:3-safe framing, heavy film grain, warm faded colors, soft halation. A glamorous woman in a 70s bathroom with orange tiles picks up the product from @Image1 and admires it in a round mirror; slow optical zoom-in typical of 70s ads, ending on the product in her hand. Audio: vintage jingle-style instrumental, tape hiss, no dialogue. The product itself remains modern and exactly as in @Image1. No text.
```

**V23 · בעיה ← פתרון (12 ש', בזהירות)** [לא נבדק בפועל]
- **שימוש:** הדגמת מוצר (E4 V7).
- **מודל והגדרות:** ‏Seedance 2.5 · ‏12 ש' · ‏9:16 · ‏3 שוטים.
- **רפרנסים:** ‏packshot.
- **עלות:** ‏₪50 / ₪67.
- **הערה:** **"לפני ואחרי" של תוצאת מוצר ב-AI הוא הטעיה אם התוצאה לא מייצגת** (פרק 06). מציגים כאווירה ("light warms up"), בלי טענות רפואיות ובלי "תוצאות".
```
9:16, 12s. [0:00-0:04] Close-up of a cheek under harsh bathroom light, desaturated, the person sighs. [0:04-0:08] A hand applies a drop from the bottle in @Image1; the room light warms up. [0:08-0:12] Same framing in soft natural light, she smiles; the bottle enters frame bottom-right with the label visible. Natural, non-exaggerated skin, natural pores, no medical-style claims, no text.
PRODUCT LOCK: same shape, colors and label layout as @Image1.
```

### E. אוכל

**V24 · המבורגר שנבנה בשכבות (8 ש')** [לא נבדק בפועל]
- **שימוש:** המבורגריות, תפריט דיגיטלי, אפליקציות משלוחים.
- **מודל והגדרות:** ‏Kling 3.0 · ‏8 ש' · ‏9:16 · מצלמה: top-down נעול.
- **רפרנסים:** אופציונלי: צילום של המנה האמיתית.
- **עלות:** ‏₪9.
- **הערה:** במנה של לקוח, המנה ב-AI צריכה להיות דומה למנה שמגישים בפועל.
```
Top-down overhead shot of a gourmet burger assembling itself layer by layer on a wooden board: brioche bottom, lettuce, smash patty with dripping cheddar, tomato, pickles, top bun pressed down. Each layer drops in with real weight and a small bounce. Warm practical light, steam rising from the patty. Audio: sizzle, soft thuds on each layer, no music. Ingredients do not morph, no plastic look, no text.
```

**V25 · שווארמה, סגנון דוקו רחוב (9 ש')** [לא נבדק בפועל]
- **שימוש:** דוכן או מסעדה ישראלית.
- **מודל והגדרות:** ‏Seedance 2.5 · ‏9 ש' · ‏9:16 · מצלמה: handheld דוקומנטרי.
- **רפרנסים:** אופציונלי: פני המוכר (באישור), תמונת הדוכן.
- **עלות:** ‏₪38 / ₪50.
- **הערה:** "street chatter in Hebrew" יוצא לרוב מלמול לא מובן. זה בסדר כרקע.
```
Handheld street-food documentary style, 9:16. 0-3s: macro of a shawarma spit turning, fat glistening, a knife shaving thin slices. 3-6s: hard cut, the cook's hands stuff a fluffy pita with meat, tahini drizzle, pickles and amba. 6-9s: medium shot, he hands it across the counter toward camera with a grin. Warm evening light, neon sign glow with no readable letters. Audio: sizzling, knife scraping, street chatter in Hebrew, no music.
```

**V26 · ‏Cheese pull ‏ASMR (6 ש')** [לא נבדק בפועל]
- **שימוש:** פיצריות, הוק של 2 שניות.
- **מודל והגדרות:** ‏Kling 3.0 · ‏6 ש' · ‏9:16 · ‏100mm macro.
- **רפרנסים:** אין.
- **עלות:** ‏₪6.
- **הערה:** מצוין כשוט פתיחה ללולאה (loop).
```
Extreme close-up, 100mm macro: a slice of pizza is lifted from the pan, stretchy mozzarella pulling in long glossy strands, steam rising. Camera: slow pull-up following the slice, ending on the cheese strands snapping. Warm side light from a window, shallow depth of field. Audio: ASMR crisp crust crackle, cheese stretch, no music. No plastic look.
```

**V27 · שקשוקה במחבת ברזל (8 ש')** [לא נבדק בפועל]
- **שימוש:** בתי קפה, ארוחות בוקר, מסעדות שכונתיות.
- **מודל והגדרות:** ‏Kling 3.0 · ‏8 ש' · ‏9:16 · מצלמה: push-in מלמעלה ב-45°.
- **רפרנסים:** אופציונלי: המחבת והשולחן האמיתיים.
- **עלות:** ‏₪9.
- **הערה:** בקשו `yolks stay intact`, אחרת המודל "שובר" ביצים.
```
45-degree overhead, 50mm: a black cast-iron pan of shakshuka bubbles on a rustic table, tomato sauce simmering, two eggs set with glossy intact yolks. A hand sprinkles chopped parsley and crumbled feta; a piece of challah dips into the sauce. Camera: slow push-in ending on the yolk. Morning window light from camera left, steam rising. Audio: gentle bubbling, café ambience, no music. Yolks stay intact, ingredients do not morph, no text.
```

**V28 · ארוחת בוקר ישראלית מלמעלה (10 ש')** [לא נבדק בפועל]
- **שימוש:** בתי מלון, צימרים, קפה.
- **מודל והגדרות:** ‏Seedance 2.5 · ‏10 ש' · ‏9:16 · ‏top-down ‏+ ‏stop-motion.
- **רפרנסים:** אופציונלי: צילום השולחן הריק.
- **עלות:** ‏₪42 / ₪56.
- **הערה:** אם הצלחות "נמסות" זו לתוך זו, מקצרים לחצי מהמנות.
```
Top-down locked-off shot of a wooden table, 9:16. In quick stop-motion rhythm, dishes slide into frame one by one on the beat: chopped salad, labneh with olive oil, hummus, olives, a basket of fresh bread, two coffees. At 8s two hands clink the coffee cups in the center. Bright morning light from top left, soft shadows. Audio: dish clinks on each beat, upbeat acoustic guitar. Dishes do not merge, no plastic look, no text.
```

### F. נדל"ן

**V29 · וילה: ‏drone reveal ‏(18 ש')** [לא נבדק בפועל]
- **שימוש:** הדמיה לפרויקט, מתווכי יוקרה, צימרים.
- **מודל והגדרות:** ‏Seedance 2.5 · ‏18 ש' · ‏9:16 · מצלמה: FPV, ‏fly-through, ‏crane.
- **רפרנסים:** לנכס אמיתי: 3–5 תמונות חוץ ופנים (K19).
- **עלות:** ‏₪76 / ₪101.
- **הערה:** **בנכס אמיתי כותבים "הדמיה" על המסך.** אסור להוסיף נוף, בריכה או חדר שלא קיימים.
```
Luxury villa with an infinity pool overlooking the Mediterranean at golden hour, 9:16. 0-5s: FPV drone glides low over the pool surface toward the glass facade, reflections rippling. 5-9s: the drone flies through the open sliding doors into a double-height living room. 9-14s: crane up inside to reveal the mezzanine and the sea view behind. 14-18s: pull-out back over the terrace, sun on the horizon, locked-off. Wide 16mm, warm natural light, interior practicals on. Audio: soft waves, gentle piano. No people, no text.
```

**V30 · ‏Virtual staging: דירה ריקה ← מרוהטת (V2V, ‏15 ש')** [לא נבדק בפועל]
- **שימוש:** מתווכים, יזמים, Airbnb (D3 R14).
- **מודל והגדרות:** ‏Genjutsu Motion Transfer (או Seedance 2.5 Edit) · סיור של 15 ש' בטלפון על ג'ימבל · ‏9:16 · ‏1080p.
- **רפרנסים:** הווידאו + תמונת סגנון (K20).
- **עלות:** ‏₪71 / ₪104.
- **הערה:** **מסמנים "הדמיה"** כדי לא להטעות קונים. קירות, חלונות ותוכנית הדירה לא משתנים.
```
@Video1 = original walkthrough (camera path and timing — keep identical). @Image1 = interior style reference (Scandinavian minimal, oak and linen) — style only.
Same walkthrough, but the empty apartment is fully furnished in the style of @Image1: linen sofa, oak dining table, plants, warm lamps. Keep walls, windows, floor plan and camera path exactly as in @Video1. Bright daylight from windows. Audio: quiet room tone. No people, no text.
```

**V31 · פנטהאוז: מיום ללילה (10 ש')** [לא נבדק בפועל]
- **שימוש:** נדל"ן, לולאה (loop) לאתר או לסטורי.
- **מודל והגדרות:** ‏Kling 3.0 או Seedance 2.5 · ‏10 ש' · ‏9:16 · מצלמה נעולה לגמרי.
- **רפרנסים:** אופציונלי: start frame מ-K18.
- **עלות:** ‏Kling ‏₪11. ‏Seedance ‏₪42.
- **הערה:** ‏time-lapse עובד טוב רק כשהמצלמה נעולה.
```
Locked-off wide shot, 16mm, from the corner of a penthouse living room facing floor-to-ceiling windows over a city skyline. Time-lapse from late afternoon to blue hour to night over 10 seconds: sunlight shadows sweep across the floor, then interior lamps switch on and city lights twinkle outside. Camera completely still. Audio: soft city hum, no music. No text.
```

**V32 · מגרש ריק ← הבניין העתידי (start/end frame, ‏8 ש')** [לא נבדק בפועל]
- **שימוש:** שיווק פרויקט "על הנייר" ליזמים.
- **מודל והגדרות:** ‏Seedance 2.5 (או Veo 3.1) עם first + last frame · ‏8 ש' · ‏9:16.
- **רפרנסים:** ‏start = צילום המגרש. ‏end = הדמיית האדריכל (או K18, אבל רק באישור היזם).
- **עלות:** ‏Seedance ‏₪34. ‏Veo Fast ‏≈₪9.
- **הערה:** המצלמה זהה בשני הפריימים. רק העולם משתנה ("change too much at once and the model has to invent the middle", Kapwing). כותבים "הדמיה".
```
Start frame = @Image1 (empty lot, today). End frame = @Image2 (architect's rendering, same camera position).
Locked-off camera, identical lens and position in both frames. Over 8 seconds the building rises floor by floor from the empty lot in a smooth construction time-lapse, scaffolding appearing and dissolving, ending exactly on @Image2 at golden hour. Clouds move fast. Audio: soft construction ambience fading into calm wind, no music. No text, no people close to camera.
```

### G. אופנה

**V33 · הליכה על מסלול (8 ש')** [לא נבדק בפועל]
- **שימוש:** בוטיק, מעצבת, lookbook.
- **מודל והגדרות:** ‏Seedance 2.5 · I2V · ‏8 ש' · ‏9:16 · מצלמה: low-angle backward tracking.
- **רפרנסים:** דוגמנית (K01 או K21) + הבגד על קולב או flat lay (K11).
- **עלות:** ‏₪34 / ₪45.
- **הערה:** בגד אמיתי של לקוח: מעלים 2 תמונות (חזית + גב). הדפסים מסובכים "רוקדים".
```
@Image1 = model identity. @Image2 = outfit (oversized cream wool coat, wide trousers) — exact.
The model walks toward camera down a concrete runway, coat flowing with real weight behind her. Camera: low-angle backward tracking, 50mm, ending in a medium close-up as she stops and turns her head. Hard top light, black background, light haze. Audio: heels echoing, deep pulsing beat. Fabric lags behind motion, no face drift, no text.
```

**V34 · מעברי תלבושת בסיבוב (8 ש')** [לא נבדק בפועל]
- **שימוש:** חנויות בגדים, "3 לוקים לאירוע".
- **מודל והגדרות:** ‏Seedance 2.5 · ‏8 ש' · ‏9:16 · מצלמה נעולה, ‏match cut.
- **רפרנסים:** פנים (K01) + 3 תמונות בגדים (K11).
- **עלות:** ‏₪34 / ₪45.
- **הערה:** אם המודל מערבב בגדים, מייצרים כל לוק כקליפ נפרד ומחברים על הסיבוב בעריכה.
```
A young woman in a plain grey hoodie spins once in front of a white wall; on the spin at 2s a match cut reveals her in a sequined black evening dress, then on the second spin at 5s in a red tailored suit. Camera locked-off, medium-wide, 35mm. Bright ring-light key. Audio: whoosh on each spin, upbeat pop beat, cut on the beat. Same face and hair in every look, no text.
```

**V35 · אופנת רחוב אדיטוריאלית (8 ש')** [לא נבדק בפועל]
- **שימוש:** מותג גברים, משקפיים, מעילים.
- **מודל והגדרות:** ‏Seedance 2.5 או Kling 3.0 · ‏8 ש' · ‏9:16 · מצלמה: lateral tracking.
- **רפרנסים:** אופציונלי: פנים + פריט.
- **עלות:** ‏Seedance ‏₪34. ‏Kling ‏₪9.
- **הערה:** שם של סרט צילום (film stock) מוחלף בתיאור גנרי.
```
A Paris street at golden hour, 35mm film look, fine color-negative film grain. A man in a camel overcoat and sunglasses crosses a cobblestone street toward camera. Camera: slow lateral tracking from left to right, ending on his profile as he flips open a plain silver lighter. Warm low sun from behind, long shadows, gentle flare. Audio: street ambience, distant accordion. No text, no logos.
```

**V36 · תכשיט במאקרו (6 ש')** [לא נבדק בפועל]
- **שימוש:** צורפים, חנויות תכשיטים.
- **מודל והגדרות:** ‏Kling 3.0 ב-4K · ‏6 ש' · ‏9:16 · ‏100mm macro, ‏rack focus.
- **רפרנסים:** התכשיט (חזית + צד), על רקע ניטרלי.
- **עלות:** ≈₪22 [נגזר].
- **הערה:** מתכת משקפת "ממציאה" פרטים. בודקים שמספר האבנים זהה למקור.
```
@Image1 = the ring (exact design, stone count and metal color — must match).
Extreme macro, 100mm: the ring from @Image1 rests on dark velvet; a slow rotation of 45° catches a single moving spotlight, the stone throws sparkles. Rack focus from the band to the stone, ending sharp on the stone. Deep black background. Audio: soft shimmer, low ambient tone. Exactly one ring, same number of stones, no text.
```

### H. לפני/אחרי ו-Reality-Swap ‏(Genjutsu)

> המבנה ברילס: **תוצאה למעלה, מקור למטה, באותו timecode**, ‏50/50 או 60/40 (פרק 03 §7.4). אודיו: רק המקור.

**V37 · ‏"חניון ← כניסה למלון יוקרה", ביט A (15 ש')** [לא נבדק בפועל]
- **שימוש:** הנוסחה של maorhani1 לשוק הישראלי: "פייק עשיר" עם חבר שמשחק נהג.
- **מודל והגדרות:** ‏Genjutsu Motion Transfer · ‏12–15 ש' · ‏9:16 · חצובה בגובה עיניים · ‏480p (≈₪6) ← ‏1080p.
- **רפרנסים (6 משבצות):** פנים שלך · גוף מלא בלבוש היעד · החבר עם חליפת נהג · לימוזינה גנרית (K14) · כניסת מלון גנרית (K15) · אביזר (שטרות / מזוודה).
- **עלות:** ‏₪71 / ₪104.
- **הערה:** תנועות גדולות (פתיחת דלת, הושטת שטרות). פרוקסי בגודל דומה: רכב קטן ← לימוזינה עובד, אופניים ← לא.
```
Keep the original motion, camera position, framing and timing exactly.
Replace the parking garage with the front entrance of a grand Belle Époque luxury hotel on the Riviera at golden hour: marble steps, brass revolving door, potted palms, warm lobby light spilling out, no signage.
Replace the small car with a stately black ultra-luxury British-style sedan with no grille emblem and no hood ornament, same position and scale.
The man opening the door becomes a uniformed chauffeur: black suit, white gloves, cap.
Keep the main character's face, hairstyle and gestures identical to the references; dress him in a navy double-breasted suit and sunglasses.
Banknotes falling to the ground stay as in the original.
Photorealistic, natural lighting matched to the original footage, no text, no logos.
```

**V38 · ביט B: הווידוי בעברית מהמושב האחורי (20 ש')** [לא נבדק בפועל]
- **שימוש:** החלק המצחיק של הרילס ("בדיוק סגרנו עסקה של מאה מיליון...").
- **מודל והגדרות:** ‏Genjutsu Motion Transfer · ‏≤20 ש' · ‏9:16 · טלפון בתפסנית על משענת הראש, מיקרופון דש.
- **רפרנסים:** 4 תמונות פנים שלך + פנים של רכב יוקרה (K16).
- **עלות:** ‏₪92 / ₪137.
- **הערה:** **מייצאים WAV של המקור לפני הכל.** משתיקים את אודיו ה-AI. אם השפתיים "זזות" ב-1–3 פריימים, מזיזים את האודיו או חותכים ל-B-roll.
```
Keep the original motion, head movements, lip movements, eye line and timing exactly — the man is speaking; preserve his mouth shapes frame by frame.
Replace the car interior with the rear cabin of an ultra-luxury sedan: white leather seats, starlight headliner, wood veneer, a champagne flute in the armrest. No emblems anywhere.
Outside the windows: a Riviera harbor with yachts, daylight.
Keep the man's face identical to the references; navy suit, white shirt.
Photorealistic, same lighting direction as the original, no text, no logos.
```

**V39 · גרסת ה-binding המלאה של "פייק עשיר" (Seedance 2.5 Edit, ‏15 ש')** [לא נבדק בפועל]
- **שימוש:** כשעובדים ב-Seedance Edit (Lovart/fal) במקום Genjutsu.
- **מודל והגדרות:** ‏Seedance 2.5 Edit · ‏`@Video1` ‏≤15 ש' · ‏9:16 · ‏720p/1080p.
- **רפרנסים:** הווידאו + K15 + K14.
- **עלות:** ‏≈₪40–63 (Edit עד I2V מלא).
- **הערה:** ב-Lovart ייתכן חסימה של פנים אמיתיות [לא מאומת]. לפנים שלך, Higgsfield בטוח יותר.
```
@Video1 = original performance, blocking, timing and Hebrew dialogue — keep identical, including lip movement. @Image1 = grand Belle Époque hotel facade (location look only, no signage). @Image2 = black ultra-luxury British-style sedan (vehicle only, no emblems).
Same video, but the underground parking garage becomes the grand entrance of @Image1 at golden hour, the small car becomes the sedan from @Image2, and the friend in a T-shirt becomes a uniformed chauffeur in a black suit and white gloves. Keep every gesture, the door opening and the cash falling to the ground. Warm luxury grade, 35mm. Audio: keep original voices; add soft fountain ambience and distant traffic. No on-screen text, no logos.
```

**V40 · סטודיו ריק ← קרון רכבת תחתית מלא (15 ש')** [לא נבדק בפועל]
- **שימוש:** הדמו של Higgsfield (פרק 00 רילס 5), ופיץ' "Hybrid Production" לסוכנויות.
- **מודל והגדרות:** ‏Genjutsu · ‏15 ש' · ‏9:16 · חדר ריק עם קיר לבן, שחקן בפנטומימה ברורה (מקל מטאטא במקום מוט).
- **רפרנסים:** 6: פנים, ליצן, אביר, תחפושת דינוזאור, כלב, קרון רכבת (K22).
- **עלות:** ‏₪71 / ₪104. לשלושה עולמות (V40 + 2 וריאציות) כ-₪213.
- **הערה:** מאותו מקור מייצרים עוד 2 עולמות, ובעריכה מחליפים עולם כל 5–8 ש'. **3 ג'נרציות = 3 "וואו".**
```
Same video, but inside a crowded subway car at rush hour. Passengers from the references: a clown, a medieval knight, a person in a dinosaur costume, a spaniel dog. Keep the actor's motion, face and timing exactly. Photorealistic, flickering fluorescent light, no readable signs, no logos.
```
וריאציות: `Same video, but on a medieval battlefield.` · `Same video, but in a busy street with balloons and bicycles.`

**V41 · סלון ← פנטהאוז מול הים (שלב 1 בשיטת sidequestpat_, ‏15 ש')** [לא נבדק בפועל]
- **שימוש:** דמו מכירה ל"פרסומת יוקרה מצילום ביתי", או הוק "לא זזתי מהספה" (D3 R5).
- **מודל והגדרות:** ‏Genjutsu Motion Transfer או Restyle · ‏15 ש' · ‏9:16 · ‏1080p (כי אחריו מגיע שלב זוויות, V50).
- **רפרנסים:** פנים + K18 + K13 (שעון).
- **עלות:** ‏₪71 / ₪104.
- **הערה:** ‏wipe באמצע משפט בעריכה הוא רגע ה"וואו".
```
Keep motion, framing, lip-sync and timing. Replace the plain white living room with a luxury penthouse with floor-to-ceiling windows overlooking the sea at sunset. Change his black t-shirt to a beige knit polo and add a gold dress watch with no visible brand on the left wrist. Keep his face identical. Photorealistic, warm sunset light from the windows matched to the original light direction, no text, no logos.
```

**V42 · סופר שכונתי ← מעדנייה גורמה ("מיליונר מזויף", פרק 2, ‏15 ש')** [לא נבדק בפועל]
- **שימוש:** סדרה עם פרקים (D3 R12). כל פרק = מקום יומיומי אחר.
- **מודל והגדרות:** ‏Genjutsu · ‏15 ש' · ‏9:16 · ‏720p לחשבון שלך.
- **רפרנסים:** פנים + גוף מלא + בטלר (K21 גנרי).
- **עלות:** ‏720p: ‏₪34. ‏1080p: ‏₪71.
- **הערה:** **לא לצלם בתוך רשת אמיתית בלי אישור**, ולא להשאיר שילוט או מותגים בפריים. על המסך לא כותבים שם של רשת.
```
Same video, now a luxury gourmet market: marble floors, gold-trimmed wooden shelves, crystal chandeliers; a uniformed butler in white gloves pushes the cart behind the man. Keep the actions, faces, cart movement and timing exactly. Photorealistic, warm chandelier light, no readable labels, no brand packaging, no logos.
```

**V43 · ‏"Guess which half is real": רחוב ← סמטת ניאון גשומה (10 ש')** [לא נבדק בפועל]
- **שימוש:** חשבון שני באנגלית (D3 R11). עובד בלי דיבור.
- **מודל והגדרות:** ‏Genjutsu · ‏10 ש' · ‏9:16 · הליכה לעבר המצלמה.
- **רפרנסים:** פנים + K22 (סמטה).
- **עלות:** ‏720p: ≈₪23. ‏1080p: ‏₪46.
- **הערה:** שלטים ביפנית יוצאים "דמויי כתב". זה בסדר באווירה, אבל לא בפרסומת ללקוח.
```
Same video, but the street becomes a neon-lit alley in Tokyo at night in light rain, glowing paper lanterns, steam from food stalls, reflections on wet asphalt. Keep the walk, face and camera motion identical. Photorealistic, no readable text, no logos.
```

**V44 · חדר מבולגן ← חדר מסודר (I2V, ‏wipe, ‏8 ש')** [לא נבדק בפועל]
- **שימוש:** מעצבי פנים, מארגנות בית, ניקיון.
- **מודל והגדרות:** ‏Seedance 2.5 · I2V (start frame = החדר האמיתי) · ‏8 ש' · ‏9:16 · מצלמה נעולה ← push-in.
- **רפרנסים:** ‏start frame (K06).
- **עלות:** ‏₪34 / ₪45.
- **הערה:** לעסק אמיתי: "הדמיה" על המסך. גאומטריית החדר והחלון נשארות.
```
Start frame = @Image1 (the real room). Locked-off wide shot of a messy, dim student bedroom. At 3s a smooth left-to-right wipe transforms it into a clean, modern bedroom with warm LED strips, plants and a made bed; the camera position never changes. Then a slow push-in toward the new desk setup. Audio: whoosh on the wipe, cozy lo-fi beat. Same room geometry, same window, no text.
```

**V45 · תחפושת פורים ב-₪0 (10 ש')** [לא נבדק בפועל]
- **שימוש:** טרנד עונתי (D3 R7), ומשפך "שלחו לי סרטון ב-DM".
- **מודל והגדרות:** ‏Genjutsu (Motion Transfer / Object Swap) · ‏10 ש' · ‏9:16 · סיבוב של 360° בחולצה חלקה.
- **רפרנסים:** פנים + תמונת התחפושת (נוצרה ב-K11).
- **עלות:** ‏720p: ≈₪23. ‏1080p: ‏₪46.
- **הערה:** "visor up" שומר על הפנים גלויות. בלי זה, הקסדה מכסה את הזהות.
```
Same video and motion: the person now wears full medieval knight armor with a red cape, inside a castle hall lit by torches. Keep the face visible, visor up, and the 360° turn and timing identical. Photorealistic metal reflections, cape follows the spin with real weight, no text.
```

### I. ‏Infinite Angles ‏(Seedance 2.5 Edit)

> צילום: שוט רחב ונעול, הכל בפריים, אביזרים קרובים לגוף, 10–25 ש'. ייצור בקטעים של 3–8 ש'. הפסקול המקורי הרציף מדביק את הקאטים. מקור הזוויות עדיף צילום אמיתי (AI על AI מוריד איכות).

**V46 · דוכן לימונדה: רשימת rourke (20 ש')** [נראה ברילס; לא נבדק על ידינו]
- **שימוש:** הרילס של rourke. הוק: "צילמתי במצלמה אחת".
- **מודל והגדרות:** ‏Seedance 2.5 Edit (Lovart / Higgsfield / fal) · ‏`@Video1` של 20 ש' · ‏9:16 · ‏480p ← ‏1080p בקטעים.
- **רפרנסים:** הטייק בלבד.
- **עלות:** ‏₪54 / ₪75.
- **הערה:** מדביקים את הרשימה ב-M2 (סעיף 2.2). הדוגמה למטה מראה את 2 השוטים הראשונים שנחשפו ברילס, עם [NAME] במקום שם היוצר.
```
00:00 Tracking shot to [NAME] / 03:07 Close up slow motion / 05:03 Low angle / 06:14 Top down shot / 08:14 Extreme close up / 14:00 Camera inside the cup / 15:22 Tracking shot of the lemonade jug / 20:06 Dolly zoom
Keep the location, dialogue, and actions identical to the original video.
```
```
[00:00-02.37] Shot 1: [NAME] from @Video1 speaks to camera behind the lemonade stand, same performance and dialogue. Straight-on eye level, slow zoom in. Standard prime. Harsh midday sun. Handheld micro-drift easing forward. Hard cut to Shot 2.
[02.37-05.57] Shot 2: The lemon wedge from @Video1 tosses up from [NAME]'s hand, ramping into deep slow motion as it spins midair, macro lens, background melting into bokeh. Hard cut to Shot 3.
```

**V47 · קפה בבית: "צילמתי פעם אחת, AI צילם עוד 7" (10 ש')** [לא נבדק בפועל]
- **שימוש:** הרילס החינוכי הראשון בפורמט (D3 R4). ‏CTA: "תגיבו זוויות".
- **מודל והגדרות:** ‏Seedance 2.5 Edit · ‏`@Video1` של 10 ש' · ‏9:16 · ‏2 קטעים של 5 ש'.
- **רפרנסים:** הטייק.
- **עלות:** ‏₪27 / ₪38.
- **הערה:** "exactly one cup" חשוב. כפילות אובייקטים היא הכשל הנפוץ ביותר (fal).
```
@Video1 = a single locked-off wide take of me pouring coffee at my kitchen counter, 10s. Keep location, actions and timing identical; only camera position and lens change.
[00:00-02:00] Shot 1: same action, medium shot at eye level, slow push-in, standard prime, window light as in the source. Hard cut.
[02:00-04:00] Shot 2: extreme close-up of the coffee stream hitting the cup, slow motion, macro lens. Hard cut.
[04:00-06:00] Shot 3: overhead top-down shot of the cup filling, crema swirling. Hard cut.
[06:00-08:00] Shot 4: camera inside the cup looking up at the pouring stream and my face beyond. Hard cut.
[08:00-10:00] Shot 5: drone-style pull-out through the kitchen window, ending wide and locked-off.
CONTINUITY: exactly one cup, same mug color, same shirt. CONSTRAINTS: no crew, no lighting rigs, no text, no duplicated objects.
```

**V48 · פודקאסט: כיסוי של 3 מצלמות מטלפון אחד (30 ש')** [לא נבדק בפועל]
- **שימוש:** שירות לפודקאסטרים ולמאמנים (פרק 10: ‏Infinite Angles ₪1,200 / ₪1,800 / ₪2,500 ללקוח).
- **מודל והגדרות:** ‏Seedance 2.5 Edit · ‏`@Video1` של 30 ש' (שני דוברים, שוט רחב נעול) · ‏6 קטעים של 5 ש'.
- **רפרנסים:** הטייק + תמלול ברמת מילה לחלונות הדיבור (MOUTH MAP).
- **עלות:** ‏₪80 / ₪113.
- **הערה:** הכשל העיקרי: פה סגור בזמן דיבור, או עיניים שמסתכלות למצלמה החדשה. אם קטע נכשל פעמיים, משתמשים בשוט הרחב המקורי.
```
@Video1 = a single locked-off wide take of two people talking at a podcast table, 30s, 9:16. LOCKED ELEMENTS: same room, dialogue, gestures, wardrobe, microphones and timing; only camera position and lens change.
MOUTH MAP: Host speaks [00:00-00:09], [00:18-00:24]; Guest speaks [00:09-00:18], [00:24-00:30]. Whenever a mouth is in frame during its talking window, lips follow the original audio; never invent speech in quiet windows.
WHERE THEY LOOK: eyes stay on each other or on the original camera position.
[00:00-00:05] Shot 1: two-shot, eye level, slow push-in, 35mm. Hard cut.
[00:05-00:09] Shot 2: Host medium close-up from the Guest's side, 85mm, shallow depth of field. Hard cut.
[00:09-00:14] Shot 3: Guest close-up over the Host's shoulder, 85mm. Hard cut.
[00:14-00:18] Shot 4: insert of the Guest's hands gesturing near the mic, 100mm. Hard cut.
[00:18-00:24] Shot 5: Host profile, 50mm, handheld micro-drift. Hard cut.
[00:24-00:30] Shot 6: high wide angle from the corner, locked-off.
CONSTRAINTS: exactly two people, two microphones, no crew, no extra cameras, no text.
```

**V49 · שף במסעדה: מקרו על המחבת (20 ש')** [לא נבדק בפועל]
- **שימוש:** מסעדות, שפים פרטיים, קייטרינג.
- **מודל והגדרות:** ‏Seedance 2.5 Edit · ‏`@Video1` של 20 ש', שוט רחב של עמדת הבישול · ‏4 קטעים.
- **רפרנסים:** הטייק (באישור המסעדה).
- **עלות:** ‏₪54 / ₪75.
- **הערה:** אש ושמן הם "תנועה מהירה". מבקשים slow motion במקום מהירות אמיתית.
```
@Video1 = a single locked-off wide take of a chef cooking at a stove, 20s. Keep the kitchen, actions, timing and wardrobe identical; only camera position and lens change.
[00:00-00:04] Shot 1: medium shot from across the pass, slow push-in, 35mm. Hard cut.
[00:04-00:08] Shot 2: macro of oil sizzling as the vegetables hit the pan, slow motion. Hard cut.
[00:08-00:12] Shot 3: low angle from counter height as the chef flips the pan, flames rising, slow motion. Hard cut.
[00:12-00:16] Shot 4: top-down on the plating, tweezers placing herbs. Hard cut.
[00:16-00:20] Shot 5: wide hero, locked-off, chef slides the plate toward camera.
CONTINUITY: exactly one pan, same plate, same apron. CONSTRAINTS: no extra cooks, no crew, no text.
```

**V50 · שלב 2 של sidequestpat_: זוויות על תוצאת הפנטהאוז (12 ש')** [לא נבדק בפועל]
- **שימוש:** ממשיך את V41. החשיפה בסוף: "סט צילום" שלא היה קיים.
- **מודל והגדרות:** ‏Seedance 2.5 Edit על **תוצאת V41 ב-1080p** · זוויות של 2–4 ש' בקאט.
- **רפרנסים:** תוצאת V41 כ-`@Video1`.
- **עלות:** ‏≈₪32 / ₪46.
- **הערה:** דור שני של AI מוריד איכות. מקסימום שני מעברים, ‏1080p בכל שלב.
```
@Video1 = the penthouse clip (already generated). Keep his performance, wardrobe, location and timing identical; only camera position and lens change.
[00:00-00:03] Shot 1: macro of the gold watch on his wrist as he gestures, shallow depth of field. Hard cut.
[00:03-00:06] Shot 2: exterior drone shot through the window, slowly pushing toward him. Hard cut.
[00:06-00:09] Shot 3: profile medium shot against the sea, 85mm. Hard cut.
[00:09-00:12] Shot 4: wide pull-back revealing the room is a film set with lighting rigs and cinema cameras around him; locked-off at the end.
CONSTRAINTS: exactly one watch, no text, no logos.
```

### J. דרמה קולנועית

**V51 · ‏One-take במלון: מותחן (30 ש')** [לא נבדק בפועל]
- **שימוש:** טיזר קולנועי, תחרויות (פסטיבל Higgsfield), תיק עבודות.
- **מודל והגדרות:** ‏Seedance 2.5 · ‏30 ש' · ‏9:16 (או 16:9 לפסטיבל) · ‏steadicam ← ‏whip pan ← ‏push-in.
- **רפרנסים:** אופציונלי: K01 לשחקן.
- **עלות:** ‏₪127 / ₪167.
- **הערה:** מצוטט כמעט כלשונו מ-[Atlabs](https://www.atlabs.ai/blog/ultimate-seedance-2.5-prompting-guide-2026), בפורמט "plain seconds".
```
A man in a charcoal three-piece suit walks the length of a hotel lobby at night, marble floor, brass fittings, moody amber tungsten light. 0s to 8s: steadicam follow from behind as he crosses the floor, staff turning to watch him pass. 8s to 18s: he pushes through the brass doors into the street, whip pan to reveal a crowd of photographers, flashbulbs strobing. 18s to 30s: slow push in on his face, half smile, rack focus to the marquee behind him. Sound is crowd murmur, camera shutters, distant traffic, no music. No readable text on the marquee.
```

**V52 · שני אנשים על ספסל (8 ש', סגנון Veo)** [לא נבדק בפועל]
- **שימוש:** סרט קצר, קמפיין רגשי (ביטוח, בנק, עמותה).
- **מודל והגדרות:** ‏Veo 3.1 (דיאלוג באנגלית) · ‏8 ש' · ‏9:16 · ‏3 שוטים.
- **רפרנסים:** אופציונלי: 2 דמויות.
- **עלות:** ‏Veo Fast ‏≈₪9. ‏Standard ‏≈₪29.
- **הערה:** לעברית: מצלמים שחקנים אמיתיים ומעבירים ב-V2V.
```
[00:00-00:03] Medium two-shot, 35mm: an elderly man and his adult daughter sit on a park bench at golden hour, not looking at each other.
[00:03-00:06] Close-up on the daughter, 85mm: she says, "I should have called more." Her voice cracks.
[00:06-00:08] Close-up on the father; he exhales and takes her hand without looking.
Ambient noise: wind in leaves, distant children playing. SFX: a single bird call. Warm backlight, soft lens flare, gentle film grain.
```

**V53 · אפוס ארקטי (18 ש', בסגנון ANERNEQ)** [לא נבדק בפועל]
- **שימוש:** סרט קצר, פסטיבל, תרגול של עקביות דמות לאורך קאטים.
- **מודל והגדרות:** ‏Seedance 2.5 · ‏18 ש' · ‏16:9 או 9:16 · ‏3 שוטים.
- **רפרנסים:** אופציונלי: גיליון דמות (K02).
- **עלות:** ‏₪76 / ₪101.
- **הערה:** "snow accumulates and never resets" הוא נעילת מצב בסגנון של Higgsfield.
```
GLOBAL STYLE: photochemical epic, large-format 65mm film look, fine grain, halation, 2.39:1 framing inside the frame, no music, no subtitles.
SCENE: An Arctic hunter returns to a tent village during a blizzard at night.
0-6s: extreme wide, the hunter is a tiny silhouette against the aurora borealis, snow streaking horizontally.
6-12s: hard cut, medium tracking shot alongside him, fur hood frosted, breath freezing, firelight from the village ahead on his face.
12-18s: close-up, he kneels by the fire, ice cracks off his gloves, eyes wet.
PHYSICS: snow accumulates on his shoulders and never resets; fur lags with the wind.
AUDIO: howling wind, crackling fire, footsteps crunching. Face identical across shots.
```

**V54 · ‏"סבתא בפריז" (10 ש', רגש)** [לא נבדק בפועל]
- **שימוש:** תוכן רגשי עם הרבה שליחות (D3 R8). גם שירות למתנות ולאירועים.
- **מודל והגדרות:** ‏Seedance 2.5 · I2V · ‏10 ש' · ‏9:16 · ‏follow shot.
- **רפרנסים:** תמונה ישנה (סרוקה ברזולוציה גבוהה). אם צריך, ניקוי ב-K01.
- **עלות:** ‏₪42 / ₪56.
- **הערה:** **רק בהסכמת המשפחה**, ובלי להציג את זה כתיעוד אמיתי.
```
@Image1 = the elderly woman's face and clothing style — identity only; ignore the photo's background and damage.
She walks slowly along the river Seine at dawn in a light wool coat, turns to the camera and laughs warmly. Gentle handheld follow shot at shoulder height, 35mm look, warm film grain, soft pink morning light from behind. Audio: river ambience, distant church bells, soft accordion. Face identical to @Image1, natural aging, no beautification, no text.
```

### K. חיות

**V55 · חתול מגיש פודקאסט (8 ש')** [לא נבדק בפועל]
- **שימוש:** ערוץ faceless הומוריסטי.
- **מודל והגדרות:** ‏Kling 3.0 Turbo או Veo 3.1 (ליפ-סינק באנגלית) · ‏8 ש' · ‏9:16.
- **רפרנסים:** אין, או תמונת החתול שלכם.
- **עלות:** ‏Turbo ≈₪12. ‏Veo Fast ≈₪9.
- **הערה:** לגרסה עברית: מייצרים בלי דיבור, ומוסיפים קריינות ב-ElevenLabs ‏+ ‏Kling Lip Sync (פרק 02 §1).
```
A grumpy orange tabby cat sits in a tiny podcast studio, headphones on, in front of a professional microphone. Medium close-up, 50mm, warm practical lights and an "ON AIR" glow behind. The cat leans in and says, in a deep tired voice, "Let's be honest. Monday was a mistake." Mouth moves in sync, whiskers twitch. Audio: room tone, slight mic pop, no music. No logos.
```

**V56 · נמר שלג: דוקו טבע (10 ש')** [לא נבדק בפועל]
- **שימוש:** ערוץ טבע, B-roll, רקע לקריינות.
- **מודל והגדרות:** ‏Kling 3.0 או Gemini Omni (אווירה) · ‏10 ש' · ‏9:16 · ‏600mm טלה.
- **רפרנסים:** אין.
- **עלות:** ‏Kling ‏₪11.
- **הערה:** "realistic anatomy" מפחית רגליים מיותרות.
```
Telephoto 600mm, nature documentary look. A snow leopard stalks along a rocky Himalayan ridge at dawn, muscles shifting under thick fur, breath visible. Camera: slow lateral tracking, ending as the leopard stops and looks directly into the lens. Soft pink dawn backlight, mist in the valley. Audio: wind, distant raven, soft paw steps on stone. No humans, realistic anatomy.
```

**V57 · חתול ספינקס בחליפה: משפיען אבסורדי (10 ש')** [לא נבדק בפועל]
- **שימוש:** הפורמט של רילס 7 (AI Influencer, ‏6M+ צפיות בדוגמאות של Higgsfield).
- **מודל והגדרות:** ‏Seedance 2.5 (Text→Video) או Genjutsu (ראו V67) · ‏10 ש' · ‏9:16 · ‏backward tracking.
- **רפרנסים:** אופציונלי: דמות קבועה (K21).
- **עלות:** ‏₪42 / ₪56.
- **הערה:** אותה דמות בכל סרטון = "ערוץ ללא פנים". ‏product placement מכניסים ב-Object Swap.
```
A sphynx cat with a human body in a tailored navy suit walks confidently through a busy Milan street at noon, holding an iced coffee in a plain cup, pedestrians do a double take. Camera: backward tracking at chest height, 35mm, handheld gimbal float. Bright midday sun. Audio: street chatter, footsteps, trending upbeat track. Realistic street, photoreal fur texture, no readable signs, no logos.
```

**V58 · כלב "מנכ"ל" בפגישת בוקר (8 ש')** [לא נבדק בפועל]
- **שימוש:** תוכן ויראלי למשרדים, חנות חיות, מספרת כלבים.
- **מודל והגדרות:** ‏Seedance 2.5 · I2V · ‏8 ש' · ‏9:16 · ‏2 שוטים.
- **רפרנסים:** תמונה של הכלב שלכם (פנים + גוף).
- **עלות:** ‏₪34 / ₪45.
- **הערה:** הכלב "לא מדבר". זה מפחית כשל ליפ-סינק, וההומור בא מכתוביות.
```
@Image1 = the dog's identity (breed, fur color and markings) — exact.
0:00-0:04  Medium shot, 50mm: the dog from @Image1 sits at the head of a glass conference table in a small office, a tiny tie around its neck, three people in business clothes nodding at it. Soft window light from camera left. Slow push-in.
0:04-0:08  Close-up: the dog tilts its head, then pushes a paper with its paw toward camera. Locked-off. Hold.
Audio: office room tone, a paper slide, a stifled laugh, no music, no dialogue. Same dog markings in both shots, no readable text on paper.
```

### L. ‏UGC ומודעות

**V59 · ‏UGC "בדיוק גיליתי את זה" (8 ש', אנגלית)** [לא נבדק בפועל]
- **שימוש:** מודעת UGC לשוק בינלאומי (Meta/TikTok).
- **מודל והגדרות:** ‏Veo 3.1 / ‏Kling 3.0 Turbo / ‏Seedance 2.5 · ‏8 ש' · ‏9:16 · ‏selfie handheld.
- **רפרנסים:** ‏packshot של המוצר (K09).
- **עלות:** ‏Veo Fast ≈₪9. ‏Turbo ≈₪12.
- **הערה:** **אין להציג דמות AI כ"לקוחה אמיתית" עם "תוצאות".** מסמנים AI. משפטים פשוטים, בלי טענות.
```
Vertical selfie video, front phone camera, slightly handheld, natural window light; a woman in her late 20s sits in her car in a parking lot. She holds up a small lip-oil tube (@Image1, label legible) toward the lens and says, excited but casual: "Okay, I didn't expect this to last through a whole day of meetings — but look." She tilts her head to show glossy lips. Audio: car interior ambience, no music. Authentic, unpolished, no on-screen text.
```

**V60 · ‏Unboxing ‏ASMR (8 ש', בלי דיבור)** [לא נבדק בפועל]
- **שימוש:** כל מוצר עם אריזה. עובד בכל שפה.
- **מודל והגדרות:** ‏Kling 3.0 או Seedance 2.5 · ‏8 ש' · ‏9:16 · ‏top-down ← ‏rack focus.
- **רפרנסים:** המוצר + האריזה.
- **עלות:** ‏Kling ‏₪9. ‏Seedance ‏₪34.
- **הערה:** ידיים במגע הן נקודת החולשה. ‏`hands hold the product firmly` חובה.
```
Top-down POV of hands opening a matte black box on a wooden desk; tissue paper rustles, revealing a smartwatch (@Image1, exact design). Hands lift it toward camera and the screen lights up. 0-3s unbox, 3-6s lift, 6-8s rack focus to the watch face. Soft daylight. Audio: ASMR paper rustle, click of the box, a soft "wow" from off-screen. Hands hold the product firmly, no readable text on the screen, no logos.
```

**V61 · ‏UGC "חברה ממליצה" ב-I2V עם קריינות עברית (12 ש')** [לא נבדק בפועל]
- **שימוש:** מודעה לשוק הישראלי בלי שחקנית (E4 V2). הדיבור מגיע מ-voice-over.
- **מודל והגדרות:** ‏Seedance 2.5 · I2V · ‏12 ש' · ‏9:16 · מראה טלפון (לא קולנועי).
- **רפרנסים:** ‏packshot. אופציונלי: דמות קבועה (K21).
- **עלות:** ‏₪50 / ₪67. קריינות ב-ElevenLabs: סנטים.
- **הערה:** "no cinematic grading" חשוב. UGC שנראה מלוטש מדי מאבד אמינות.
```
9:16, 12s, authentic UGC smartphone selfie video. A woman in her late 20s in a sunlit Tel Aviv apartment bathroom holds the bottle from @Image1 close to the camera, label facing the lens, then applies two drops to her cheek and smiles naturally. Handheld micro-shake, natural window light, slight phone lens distortion, no cinematic grading. She blinks naturally every 2–4 seconds; hand grip on the bottle is realistic, fingers do not merge with the glass. A hard cut at 0:06 is hidden in a head turn. No dialogue, no text.
PRODUCT LOCK: same shape, colors and label layout as @Image1.
```

### M. טרנספורמציה ו-VFX

**V62 · שריון מתכת נוזלית בסלון (V2V, ‏10 ש')** [לא נבדק בפועל]
- **שימוש:** "וואו" לחשבון שלך, הוק לשירות VFX.
- **מודל והגדרות:** ‏Genjutsu (או Seedance 2.5 Edit) · ‏10 ש' · ‏9:16 · אגרוף ברור בשנייה 3.
- **רפרנסים:** פנים + תמונת סגנון לשריון (K11).
- **עלות:** ‏₪46 / ₪68.
- **הערה:** ‏Seedance לא מדויק לפריים ("timestamps allocate time to events"). מסנכרנים את רגע האגרוף בעריכה.
```
@Video1 = original performance in an empty living room (keep motion, timing and face identical).
Same video, but at 3s, as he clenches his fist, a liquid-metal armor ripples outward from his chest and covers his whole body in 1.5 seconds; the living room becomes a rooftop at night over a neon city. Camera move identical to @Video1. Audio: metallic flowing SFX, deep bass impact, wind on the rooftop. No text, no logos.
```

**V63 · גוף שמתפורר לחול (8 ש')** [לא נבדק בפועל]
- **שימוש:** קליפ מוזיקה, טיזר, מעבר בין סצנות.
- **מודל והגדרות:** ‏Seedance 2.5 או Kling 3.0 · ‏8 ש' · ‏9:16 · מצלמה נעולה.
- **רפרנסים:** אופציונלי: פנים (K01).
- **עלות:** ‏Seedance ‏₪34. ‏Kling ‏₪9.
- **הערה:** חלקיקים הם חוזקה של המודלים, אבל אם יש פנים מוכרות, משאירים אותן לשלב האחרון.
```
Locked-off medium shot: a woman stands still in a desert at sunset; then, from her feet upward, her body dissolves into swirling golden sand that blows away in the wind, revealing the empty landscape behind. Particles have real weight and drift. 85mm, warm backlight, heavy haze. Audio: wind rising, sand hiss, a single low drone note. No text.
```

**V64 · אסטרונאוט על הירח עם המוצר האמיתי (Hybrid placement, ‏12 ש')** [לא נבדק בפועל]
- **שימוש:** שחזור פרסומת האסטרונאוט וכוס הקפה (פרק 00 רילס 6, ‏E4 §8). זה שירות B2B.
- **מודל והגדרות:** ‏Genjutsu Motion Transfer · ‏12 ש' · ‏9:16 · צילום בחדר ריק, טלפון על חצובה, אוברול לבן, **המוצר האמיתי בפריים** עם לוגו למצלמה לפחות 1.5 ש'.
- **רפרנסים:** פני השחקן · ירח (K22) · חליפת חלל גנרית · המוצר (K09).
- **עלות:** ‏₪55 / ₪82.
- **הערה:** כשהמוצר **מצולם** ולא מיוצר, הלוגו נשאר חד. זה היתרון של השיטה. ‏Object Swap לכל SKU: ‏MASTER-E (סעיף 1.5).
```
Transform the scene into the lunar surface with Earth rising on the horizon; the actor becomes an astronaut in a classic white astronaut suit with no patches or flags. Keep the [coffee cup / can] from the original footage exactly as filmed — same logo, size and position. Keep the actor's motion, timing and camera identical. Low-gravity dust puffs at each step. Photorealistic, hard sunlight from the left, black sky, no added text.
```

### N. משפיען AI ו-Motion Transfer

**V65 · ‏"נועה": נעילת דמות לסדרה (8 ש')** [לא נבדק בפועל]
- **שימוש:** משפיענית AI קבועה (ערוץ faceless, פרזנטורית ללקוח).
- **מודל והגדרות:** ‏Seedance 2.5 · I2V · ‏8 ש' · ‏9:16 · ‏handheld micro-drift. בסדרה: Higgsfield Soul ID / AI Influencer.
- **רפרנסים:** גיליון דמות (K21), חתוך ל-2–3 תמונות. עוצמת רפרנס ≈75% אם יש סליידר.
- **עלות:** ‏₪34 / ₪45.
- **הערה:** **דמות מקורית בלבד.** בודקים שהיא לא דומה לאדם אמיתי (פרק 06 §3). את משפט הדיבור באנגלית אפשר להחליף בקריינות עברית בעריכה.
```
@Image1 = character sheet of "Noa" (front, 3/4, profile) — identity only.
Noa, 24, wavy auburn hair, freckles, oversized beige knit, sits cross-legged on a sunlit balcony in Jaffa with a coffee. Medium close-up, 50mm, handheld micro-drift. She looks at camera and says: "Today I'm testing every bakery on this street. Ranking at the end." Golden morning light from camera right. Audio: street below, birds, no music. Face identical to @Image1, no makeup change, no text.
```

**V66 · טרנד ריקוד על דמות AI (10 ש')** [לא נבדק בפועל]
- **שימוש:** "TRANSFER ANY MOTION" (פרק 00 רילס 7).
- **מודל והגדרות:** ‏Kling Motion Control או Higgsfield AI Influencer + Genjutsu · ‏10 ש' · ‏9:16 · גוף מלא, מצלמה נעולה בגובה החזה.
- **רפרנסים:** הווידאו שלך מבצע את הטרנד (תנועות חדות, בלי עוברים ושבים) + דמות (K21 / K23).
- **עלות:** ‏Kling Motion Control ≈₪12. ‏Genjutsu ‏₪46.
- **הערה:** שחקן מקור בגוף דומה לדמות משפר את המעקב. ידיים רחוק מהפנים.
```
@Video1 = dance choreography and timing only — do not copy the dancer's appearance or room. @Element1 = AI influencer character (identity and outfit).
@Element1 performs the exact choreography from @Video1 on a Tel Aviv beach promenade at sunset, full-body wide shot, camera locked-off at chest height. Hair and clothes follow the motion with real weight. Audio: keep the trend's beat from @Video1. Negative: no sliding feet, no distorted hands, no face drift.
```

**V67 · דמות אבסורדית ברחוב עם מוצר ביד (Genjutsu, ‏10 ש')** [לא נבדק בפועל]
- **שימוש:** ‏product placement למותגים בתוך ערוץ ויראלי.
- **מודל והגדרות:** ‏Genjutsu Motion Transfer · ‏10 ש' · ‏9:16 · אתם הולכים ברחוב עם המוצר האמיתי ביד.
- **רפרנסים:** דמות (K23) + המוצר.
- **עלות:** ‏₪46 / ₪68.
- **הערה:** אם המותג משלם, מסמנים גם "Paid partnership" וגם AI.
```
Keep the original walk, camera motion and timing exactly. Replace the person with the character from @Image1: a frog-headed man in a tailored white tuxedo, photoreal skin texture. Keep the [product] in his right hand exactly as filmed — same label, size and position, label toward camera. Same street, same light direction. Passersby do a double take. No added text, no logos.
```

### O. רעיונות לעסקים מקומיים בישראל

> **חובה:** אישור בכתב מהעסק לפני פרסום פומבי (וואטסאפ מספיק, שומרים צילום מסך). בכיתוב: "קונספט שנוצר ב-AI בשיתוף ובאישור [שם העסק]. הדמיה בלבד" (פרק 10 §4.2).

**V68 · דוכן הפלאפל ← פרסומת בסגנון מותג ספורט (Infinite Angles, ‏15 ש')** [לא נבדק בפועל]
- **שימוש:** "₪0 תקציב, פרסומת של ₪50K" (D3 R3). קולאב שהוא גם ליד.
- **מודל והגדרות:** ‏Seedance 2.5 Edit · ‏3 קליפים של 5 ש' (פיתה נפתחת, כדורים בשמן, הבעלים מחייך) · ‏9:16.
- **רפרנסים:** הקליפים כ-`@Video1–3`.
- **עלות:** ‏₪40 / ₪57.
- **הערה:** "sports-brand style" הוא סגנון, לא מותג. לא כותבים שם של מותג ספורט, לא בפרומפט ולא על המסך.
```
Using @Video1 as performance reference, re-shoot as a high-end sports-brand-style commercial: extreme macro of a falafel ball dropping into bubbling oil in deep slow motion; low-angle hero shot of the owner from @Video1 with dramatic rim light against a black background; whip-pan to steam rising off a fresh pita. Keep the owner's face and actions identical. Hard cuts on the beat. Audio: oil crackle, bass hits on each cut, no music bed under the sizzle. No text, no logos.
```

**V69 · מספרה: "גזירה של 20 דקות ב-12 שניות" (Infinite Angles)** [לא נבדק בפועל]
- **שימוש:** ספרים וספריות. רילס לפני/אחרי שהלקוח מעלה בעצמו.
- **מודל והגדרות:** ‏Seedance 2.5 Edit · טייק רחב נעול של הגזירה, חתוך ל-12 ש' · ‏9:16 · ‏3 קטעים.
- **רפרנסים:** הטייק (באישור הלקוח שבכיסא).
- **עלות:** ‏≈₪32 / ₪46.
- **הערה:** המספריים קרובים לפנים, וזו "ידיים במגע". עדיף זווית מאחור ומהמראה.
```
@Video1 = a single locked-off wide take of a barber finishing a fade haircut, 12s. Keep the shop, actions and timing identical; only camera position and lens change.
[00:00-00:04] Shot 1: macro of the clipper blade gliding up the neckline, hair falling in slow motion. Hard cut.
[00:04-00:08] Shot 2: over-the-shoulder into the mirror, 50mm, the barber shapes the top with scissors; hands partly out of frame. Hard cut.
[00:08-00:12] Shot 3: low angle as the cape is whipped off and the client turns to camera; locked-off.
CONSTRAINTS: exactly one client and one barber, no extra mirrors, no readable text, no logos.
```

**V70 · מאפייה: חלה יוצאת מהתנור (10 ש')** [לא נבדק בפועל]
- **שימוש:** מאפיות לקראת שישי וחגים.
- **מודל והגדרות:** ‏Kling 3.0 (או Seedance 2.5) · ‏10 ש' · ‏9:16 · ‏push-in ← ‏macro.
- **רפרנסים:** אופציונלי: צילום החלה האמיתית.
- **עלות:** ‏Kling ‏₪11.
- **הערה:** קלעים "מתמזגים" זה בזה. אם זה קורה, מבקשים `six-strand braid, strands stay separate`.
```
A baker in a flour-dusted apron slides a wooden peel into a stone oven and pulls out a glossy golden braided challah, steam rising. 0-4s: medium shot, 35mm, warm firelight from the oven on his face, slow push-in. 4-7s: macro of the crust cracking as he taps it, sesame seeds catching the light. 7-10s: the challah placed on a cooling rack next to five others, locked-off. Audio: oven crackle, hollow tap on crust, soft morning radio murmur, no music. Strands stay separate, no plastic look, no text.
```

**V71 · חדר כושר שכונתי ← גג בשקיעה (Genjutsu, ‏12 ש')** [לא נבדק בפועל]
- **שימוש:** סטודיו פילאטיס, אימון פונקציונלי, מאמן אישי.
- **מודל והגדרות:** ‏Genjutsu Motion Transfer · ‏12 ש' · ‏9:16 · מצלמה נעולה, תנועות ברורות.
- **רפרנסים:** פני המתאמן/ת + גג (K22).
- **עלות:** ‏₪55 / ₪82.
- **הערה:** **בלי הבטחות לתוצאות גוף.** זה "אווירה", לא "לפני/אחרי".
```
Keep the original exercise motion, rep timing, camera position and face exactly. Replace the small neighborhood gym with a rooftop training deck at sunset over the Tel Aviv skyline: wooden floor, potted olive trees, warm low sun from camera right, light breeze. Keep the same mat, weights and clothing. Photorealistic, no text, no logos.
```

**V72 · אולם אירועים / גן אירועים: ‏fly-through ‏(15 ש')** [לא נבדק בפועל]
- **שימוש:** שיווק אולמות, מתכנני חתונות.
- **מודל והגדרות:** ‏Seedance 2.5 (I2V מתמונת האולם המעוצב) · ‏15 ש' · ‏9:16 · ‏FPV.
- **רפרנסים:** 2–3 תמונות אמיתיות של האולם המעוצב.
- **עלות:** ‏₪63 / ₪83.
- **הערה:** **רק עיצוב שהאולם באמת מציע.** כותבים "הדמיה".
```
@Image1 = the real venue, decorated (architecture, chandeliers and table layout must match).
GLOBAL STYLE: wedding venue showcase, 9:16, photoreal, warm candlelight grade, no text, no people close to camera.
0:00-0:05  FPV drone enters through the open garden gate at blue hour, string lights overhead, gliding low over the aisle.
0:05-0:10  It flies into the hall of @Image1, between round tables with white flowers and candles, chandeliers glowing.
0:10-0:15  Crane up to reveal the full hall from above, ending locked-off on the dance floor.
Audio: soft string quartet, distant chatter, glasses clinking. NEGATIVE: no added rooms, no layout change, no logos.
```

---

## 4. פרומפטי תמונה ו-keyframe (25)

> **מודל ברירת מחדל:** ‏Nano Banana Pro (‏~2 קרדיט ב-Higgsfield, כ-₪0.3; ‏$0.134 ב-API). חלופות: Seedream (זול), ‏GPT Image 2 (כשצריך טקסט), ‏Soul (Higgsfield). **מבחן חבר:** אם חבר לא אומר מיד "זה אתה", לא ממשיכים לווידאו. כל הפרומפטים בסעיף **[לא נבדק בפועל]**, מלבד ההשראה הישירה מ-C2.

### 4.1 זהות ודמות

**K01 · ‏Anchor portrait (ניקוי תמונה קיימת)** [לא נבדק בפועל]
שימוש: הפיכת תמונה "בסדר" לרפרנס זהות נקי (`@Image1`). ‏4 וריאציות, בוחרים אחת. עלות: ≈₪1.2.
```
Using the person in the uploaded photo, create a clean studio identity reference. Keep the exact face, facial proportions, skin texture, moles, hairline and hairstyle — do not beautify or change age. Head-and-shoulders, facing the camera, neutral expression, mouth closed. Plain medium-gray seamless studio background. Soft, even front lighting from a large softbox, no harsh shadows. 85mm lens look, eye level, sharp focus on the eyes, natural skin pores visible. Wearing a plain black crew-neck t-shirt. Photorealistic, 4K, no text, no watermark.
```

**K02 · גיליון דמות / ‏Turnaround** [לא נבדק בפועל]
שימוש: עקביות לאורך שוטים וסרטונים. אחר כך חותכים ל-2–3 תמונות (פנים, 3/4, גוף מלא). עלות: ≈₪1.2. נעילת דמות מלאה כ-$10 (₪30) לפי invideo.
```
Create a professional character reference sheet based strictly on the uploaded reference photo. Same person, same face, same hairstyle, same outfit: [black tailored suit, white shirt, no tie, gold dress watch with no visible brand on the left wrist].
Layout on a clean light-gray background, consistent soft studio lighting across all panels:
Top row — four full-body standing views side by side: front view, left profile, right profile, back view. Neutral standing pose, arms relaxed.
Bottom row — three detailed close-up portraits: front, left 3/4, right profile.
No props in hands. Photorealistic, 4K, no text labels, no captions, no watermark.
```
(**"no text labels" חובה:** תוויות כמו "FRONT" נקראות כתוכן ועלולות להופיע בסרטון.)

**K03 · הבעת חיוך (לסצנות שמחות)** [לא נבדק בפועל]
```
Same person as the uploaded reference, same face, hair and t-shirt, same gray background and soft front light. Half-body, natural open smile showing teeth, eyes relaxed, looking into the lens. 85mm look, photorealistic, no beautification, no text.
```

**K04 · ‏3/4 ופרופיל מתמונה אחת (כשאין זמן לצלם)** [לא נבדק בפועל]
שימוש: שוטים מהצד (נהיגה, cockpit). אם התוצאה "בן דוד", מצלמים באמת.
```
Same person as the uploaded reference — identical facial structure, nose, jawline, ears, hairline and skin texture. Generate two images side by side: left 3/4 view (45°) and full left profile (90°). Same gray seamless background, same soft front-left light, same black t-shirt, neutral expression. Photorealistic, no text.
```

### 4.2 ‏Start / End frames (ישר ב-9:16)

**K05 · ‏Start frame: אני ליד סופרקאר (גנרי)** [לא נבדק בפועל]
```
[Image 1 = identity reference] Vertical 9:16 frame. The man from Image 1 — same face, same black suit — stands beside a sleek yellow Italian-style supercar with no visible badges on a wide desert-city boulevard at golden hour, glass towers in the background top of frame. Low angle, 24mm lens, car fills the lower third, man in the right third, looking at camera with a slight smile. Warm backlight, light haze, cinematic color grade, photorealistic. Leave headroom at the top and clear space at the bottom for captions. No text, no logos, no plates.
```

**K06 · ‏Start frame: החדר האמיתי שלי (לטרנספורמציה)** [לא נבדק בפועל]
```
Vertical 9:16, my [empty white living room / messy bedroom] from the uploaded photo, flat daylight, phone-camera realism. Keep every wall, window, door and the exact camera position; only straighten verticals and correct exposure. No added objects, no text.
```

**K07 · ‏End frame: אותו חדר, פנטהאוז מול הים** [לא נבדק בפועל]
```
Same room as the uploaded start frame, same camera position and lens, transformed into a sea-view penthouse: beige linen sofa, marble floor, floor-to-ceiling windows with a Mediterranean view, warm sunset light. Keep the room's geometry and window positions. Photorealistic, vertical 9:16, no text, no logos.
```

**K08 · ‏Start frame: אני בבית קפה במקום אמיתי** [לא נבדק בפועל]
```
[Image 1 = me, Image 2 = location photo] Vertical 9:16. The person from Image 1 sits at an outdoor café table in the exact location from Image 2 (keep the architecture, signage shapes and street layout), morning light, espresso cup on the table, medium shot from eye level, 35mm, natural candid moment, photorealistic, shallow depth of field. No readable text.
```

### 4.3 מוצר

**K09 · ‏Packshot חזית נקי (מצילום טלפון)** [לא נבדק בפועל]
שימוש: רפרנס מוצר (`@Image1`) ו-end card. **עדיף צילום אמיתי**; זה רק ניקוי.
```
Using the product in the uploaded photo, create a clean e-commerce packshot. Keep the exact shape, proportions, cap, colors and label layout — do not redesign, translate or re-letter any text. Front view, label straight and fully legible, centered. Pure white seamless background, soft even light from two softboxes, subtle contact shadow. 100mm macro look, edge-to-edge sharpness, 2K or higher, no added text, no watermark.
```

**K10 · ‏Packshot ב-3/4 (הכי חשוב לסיבוב מצלמה)** [לא נבדק בפועל]
```
Same product as the uploaded packshot, identical design and label, rotated to a 3/4 view (about 35° to the right), same white background and lighting, same scale. Do not invent the hidden side: keep it simple and consistent with the visible design. Photorealistic, no added text.
```

**K11 · ‏Flat lay של בגד / תחפושת / רפרנס סגנון** [לא נבדק בפועל]
```
Flat lay, top-down, of [an oversized cream wool coat and wide trousers / a medieval knight armor set with a red cape] on a light-gray seamless surface, soft even daylight, every seam and texture visible, garment laid fully open. Photorealistic, 4K, no person, no hanger, no text, no logos.
```

**K12 · ‏Hero frame של מוצר על אבן רטובה (9:16)** [לא נבדק בפועל]
```
[Image 1 = product packshot] Vertical 9:16 hero frame. The exact bottle from Image 1 — same shape, cap, label layout and colors, label facing camera and fully legible — on a wet black stone surface, single hard rim light from behind, soft fill from the front, water droplets on the glass, dark moody background, 100mm macro look. Product centered in the middle third. Do not alter or re-letter the label.
```

**K13 · אביזר hero גנרי (שעון / מזוודה / שטרות)** [לא נבדק בפועל]
```
Studio product photo of [a gold dress watch with a white dial and no visible brand or text / a cognac leather suitcase with brass corners and no logo / a neat stack of plain banknote-like props with no real currency markings], on a neutral gray seamless background, soft key light from top left, 3/4 angle, photorealistic, 4K, no text, no logos.
```

**K14 · כלי רכב גנרי לרפרנס (Genjutsu Ref 4)** [לא נבדק בפועל]
```
Studio photo of a stately black ultra-luxury British-style sedan, long wheelbase, no grille emblem, no hood ornament, no badges, no plates, front 3/4 view at headlight height, dark gray seamless studio, soft overhead light with long reflections on the paint. Photorealistic, 4K, no text.
```

### 4.4 לוקיישנים

**K15 · כניסת מלון יוקרה גנרית (Genjutsu Ref 5)** [לא נבדק בפועל]
```
Vertical 9:16 photo of a grand Belle Époque luxury hotel entrance on the Riviera at golden hour: marble steps, brass revolving door, potted palms, a red carpet, warm lobby light spilling out. No signage, no logos, no people. Eye-level, 24mm, photorealistic, matching the camera height of a phone on a tripod.
```

**K16 · פנים רכב יוקרה (לביט B)** [לא נבדק בפועל]
```
Rear cabin of an ultra-luxury sedan, seen from the front seat looking back: white leather seats, starlight headliner with tiny fiber-optic stars, wood veneer, a champagne flute in the armrest, a Riviera harbor with yachts visible through the windows in daylight. No emblems anywhere, no people, no text. Vertical 9:16, 24mm, photorealistic.
```

**K17 · כביש הרים רטוב בשעה הכחולה** [לא נבדק בפועל]
```
Vertical 9:16 photo of an empty wet mountain road with hairpin turns at blue hour, low mist in the valley, soft streetlights reflecting on the asphalt, pine trees, no vehicles, no road signs with text. Low angle at bumper height, 24mm, photorealistic.
```

**K18 · פנטהאוז מול הים** [לא נבדק בפועל]
```
Vertical 9:16 photo of a sea-view penthouse living room at sunset: floor-to-ceiling windows, beige linen sofa, marble floor, a small terrace with glass railing, the Mediterranean on the horizon, warm golden light, no people, no text, no logos. Eye-level, 24mm, photorealistic, interior design magazine look.
```

**K19 · וילה עם בריכת אינפיניטי (לנדל"ן)** [לא נבדק בפועל]
```
Vertical 9:16 aerial photo at 30 meters of a modern white villa with an infinity pool overlooking the Mediterranean at golden hour, glass facade, wooden deck, olive trees, no people, no text. Photorealistic, warm natural light, high detail.
```
(בנכס אמיתי: משתמשים בתמונות האמיתיות של הנכס ולא בזה.)

**K20 · רפרנס סגנון פנים (Virtual staging)** [לא נבדק בפועל]
```
Interior style reference: Scandinavian minimal living room — oak floors, linen sofa in oatmeal, round oak dining table, a fiddle-leaf fig, a paper pendant lamp, warm afternoon sun through sheer curtains. Wide 16mm, eye level, photorealistic, no people, no text, no logos.
```

**K22 · עולמות לסטודיו ריק (רכבת, ירח, גג, סמטה)** [לא נבדק בפועל]
שימוש: משבצת לוקיישן ב-Genjutsu. מייצרים אחד לכל עולם.
```
Vertical 9:16 environment plate, eye-level at about 1.6 m, 24mm, photorealistic, no people, no text, no logos:
[A: the interior of a crowded-looking but empty subway car at rush hour, fluorescent light, handrails, ads frames left blank]
[B: the lunar surface with Earth rising on the horizon, hard sunlight from the left, black sky, footprints in gray dust]
[C: a rooftop training deck at sunset over a Mediterranean city skyline, wooden floor, potted olive trees]
[D: a neon-lit alley at night in light rain, paper lanterns, steam from food stalls, reflections on wet asphalt]
```

### 4.5 דמויות AI ומיתוג

**K21 · יצירת משפיען/ית AI מקורי/ת** [לא נבדק בפועל]
שימוש: ערוץ faceless, פרזנטור קבוע, בטלר/נהג גנרי. **חובה:** לוודא שאין דמיון לאדם אמיתי.
```
Create an original fictional person (not resembling any real or famous person): [Noa, 24, Israeli, wavy auburn hair, light freckles, warm brown eyes, natural makeup, oversized beige knit sweater]. Front-facing portrait on a light-gray seamless background, soft even light, neutral expression, 85mm look. Photorealistic, natural skin texture with pores, no beautification filter, no text, no watermark.
```
(אחרי שבוחרים פנים: K02 לגיליון הדמות, ואז Soul ID או AI Influencer לסדרה.)

**K23 · דמות אבסורדית (ראש חיה, גוף אדם)** [לא נבדק בפועל]
```
Full-body photoreal character on a light-gray seamless background: [a sphynx cat head / a frog head / a shrimp head] on a human body wearing [a tailored navy suit / a white tuxedo / a basketball uniform with no team logos], standing relaxed, arms at the sides, front view. Realistic fur/skin texture, soft studio light, 4K, no text, no logos.
```

**K24 · לוגו ותווית של מותג פיקטיבי (לספק-אד פומבי)** [לא נבדק בפועל]
שימוש: פרסום פומבי בלי מותג אמיתי (פרק 10 §4.1). **בודקים בגוגל ובמאגר סימני המסחר שהשם לא תפוס.** כאן עדיף GPT Image 2, כי הוא טוב בטקסט.
```
Design a minimal logo and product label for a fictional brand called "[NOIR roasters]" — [specialty coffee]. Clean sans-serif wordmark, one simple geometric symbol, two-color palette [matte black and warm copper]. Show: (1) the logo alone on white, (2) the label applied to a [matte black coffee bag] in a front-view packshot on a white background. Crisp, legible text spelled exactly "[NOIR roasters]", no other text, no real brand references.
```

**K25 (בונוס) · ‏Cover / thumbnail למסך מפוצל** [לא נבדק בפועל]
שימוש: פריים "וואו" ל-cover אם אין פריים טוב בתוך הקליפ. הטקסט נוסף ב-CapCut.
```
Vertical 9:16 split image, top and bottom halves of equal size, same person (Image 1) in the same pose: TOP — in front of a grand Riviera hotel entrance at golden hour next to a black ultra-luxury sedan with no emblems, wearing a navy double-breasted suit; BOTTOM — in an underground parking garage next to a small blue hatchback, wearing a plain t-shirt, flat fluorescent light. Photorealistic, identical face in both halves, leave the center band clear for a title, no text, no logos.
```

---

## 5. צ'קליסט רפרנסים: מה לצלם ומה להביא

### 5.1 לפי פורמט

| פורמט | חובה | מומלץ | אסור |
|---|---|---|---|
| **Image→Video "אני ב..."** (V01–V05) | תמונת פספורט: מצלמה אחורית 1x–2x, ‏1.5–2 מ', קיר חלק, אור חלון, בלי פילטר, JPEG מקורי ≥1024px (עדיף 2K–4K) | ‏3/4 שמאל, גוף מלא בבגד היעד, חיוך (K03) | סלפי, משקפי שמש, תמונה קבוצתית, צילום מסך מ-WhatsApp |
| **V2V / Genjutsu** (V37–V45, ‏V62–V64) | קליפ 9:16 של 8–15 ש', חצובה, ‏HDR כבוי, shutter ‏1/50 (פליקר 50Hz), תנועות גדולות וברורות, פרוקסי בגודל דומה ליעד | מיקרופון דש (₪100–250), ‏3–5 טייקים, ‏clean plate של 5 ש', רפרנסים לשחקן השני | טקסט, לוגואים ושלטים בפריים, ידיים על הפנים, זום דיגיטלי, backlight |
| **Infinite Angles** (V46–V50, ‏V68–V69) | שוט **רחב ונעול**, הכל בפריים, 10–25 ש', אביזרים "within arm's reach" | תמלול ברמת מילה (MOUTH MAP), אביזר אחד שיוצר נקודת קאט | תנועת מצלמה במקור, אביזרים כפולים |
| **מוצר** (V16–V23) | ‏packshot חזית (תווית ישרה) + **3/4**, רקע לבן, ≥1024px, בלי השתקפות שורפת | צד, למעלה, גב, פתוח; לוגו מקורי PNG/SVG ל-end card | רכב ונהג באותה תמונה; רפרנס עם רקע עמוס |
| **אוכל / עסק מקומי** (V24–V28, ‏V68–V72) | אישור בכתב, צילום של המנה או המקום האמיתיים | ‏3 קליפים קצרים של "רגעים" (חיתוך, מזיגה, חיוך) | שילוט של רשתות, מותגים של ספקים |
| **נדל"ן** (V29–V32) | תמונות/סיור אמיתי של הנכס, אישור הבעלים | ג'ימבל, תמונת סגנון | נוף, חדר או בריכה שלא קיימים |
| **משפיען AI** (V65–V67) | גיליון דמות מקורי (K21 + K02), אותם 3–5 רפרנסים בכל סרטון | וידאו טרנד עם גוף דומה לדמות | דמיון לאדם אמיתי או לסלבריטאי |

### 5.2 שמונה התמונות של "Self Reference Kit" (5 דקות, באותו יום, אותו אור, אותם בגדים)

| # | תמונה | שימוש | חובה? |
|---|---|---|---|
| 1 | פנים קדמי ("פספורט") | תמיד `@Image1` | ✅ |
| 2 | ‏3/4 שמאל (45°) | נהיגה, שוטים מהצד | ✅ מומלץ מאוד |
| 3 | ‏3/4 ימין | כנ"ל | אופציונלי |
| 4 | פרופיל (90°) | ‏cockpit, הליכה מהצד | מומלץ |
| 5 | גוף מלא קדמי, ידיים לצדדים | פרופורציות ובגדים | ✅ מומלץ מאוד |
| 6 | גוף מלא מאחור | הליכה מהמצלמה | אופציונלי |
| 7 | חצי גוף, חיוך עם שיניים | סצנות שמחות ודיבור | אופציונלי |
| 8 | קלוז-אפ ידיים / אביזר | אם האביזר חשוב | לפי הצורך |

### 5.3 הודעת WhatsApp ללקוח (להעתקה, מפרק 03 §3.5)
> "כדי להכין את הסרטון אני צריך: (1) 3 תמונות שלך מהיום, באור יום מול חלון, על קיר חלק: פנים מקדימה, פנים בזווית חצי צד, וגוף מלא. בגדים כמו שתרצה להופיע בסרטון. בלי פילטרים. לשלוח כ'קובץ' ולא כ'תמונה' ב-WhatsApp. (2) קובץ לוגו מקורי (PNG/SVG). (3) 3 עד 5 תמונות מוצר על רקע לבן או אחיד, כולל צילום חזיתי שהתווית קריאה בו. (4) אישור בכתב שמותר להשתמש בתמונות ובמוצר לסרטון ולפרסום."

### 5.4 הקצאת 6 המשבצות של Genjutsu (לפי C2)

| משבצת | A: ‏"פייק עשיר" | B: מוצר עם שחקן (Object Swap) | C: "עולם חדש" (סטודיו ריק) |
|---|---|---|---|
| 1 | אתה, פנים קדמי | ‏packshot קדמי, תווית קריאה | אתה, פנים |
| 2 | אתה, גוף מלא בלבוש היעד | מוצר 3/4 | אתה, גוף מלא בבגד היעד |
| 3 | השחקן השני: פנים + חליפת נהג | מוצר מלמעלה / מאחור | ניצב או דמות 1 |
| 4 | לימוזינה גנרית (K14) | פני השחקן | ניצב או דמות 2 |
| 5 | כניסת מלון גנרית (K15) | הסביבה | ניצב או דמות 3 / חיה |
| 6 | אביזר hero (K13) | ‏style ref (צבעי המותג) | לוקיישן (K22) |

**כלל:** רפרנס אחד = נושא אחד. זווית ותאורה ברפרנס ≈ זווית ותאורה בסצנה. "Three excellent character angles are more useful than twelve mediocre ones" ([MindStudio](https://www.mindstudio.ai/blog/seedance-2-5-multimodal-reference-system-explained)).

---

## 6. ספריית שורות negative ונעילה

**איך משתמשים:** שורה אחרונה בפרומפט, ‏3–6 פריטים, רק על כשלים שבאמת רואים בטיוטה. **נעילה חיובית עדיפה על "no".** ב-Kling יש שדה negative ייעודי (3–5 פריטים). [לא נבדק בפועל, מבוסס על פרק 03 §4.6 ו-§5.4]

### 6.1 לפי קטגוריה (להעתקה)
```
Cars:      no extra cars in lane, wheels rotate correctly, no warped badges, no license plate text.
Product:   label must stay legible and unchanged, no extra products, no floating, no melting.
People:    no extra fingers, hands hold objects firmly, no face drift, no duplicate people.
Food:      no plastic look, steam rises naturally, ingredients do not morph.
Real estate: no added rooms, walls and windows unchanged, no people close to camera.
Fashion:   fabric lags behind motion, prints stay stable, no wardrobe change.
Animals:   realistic anatomy, correct number of legs, no human hands on animals.
V2V:       no added text, logos, signs or watermarks; no extra people; motion and timing unchanged.
Angles:    no crew, no lighting rigs, no extra props, no duplicated objects.
General:   no on-screen text, no watermark, no subtitles, no music.
Brand-safe: no logos, no badges, no readable signage, no brand names.
```

### 6.2 נעילות חיוביות
```
Face lock: photoreal natural skin, features identical to @Image1, zero drift.
MEMBER COUNT LOCK: exactly [two] people in every shot, no duplicates.
Same screen direction, never flip.
Same outfit throughout, no wardrobe change.
Same car color and body shape in every shot.
Exactly one [lemon / cup / ring]; prop count never changes.
State continuity: [snow / dirt / water] accumulates and never resets.
Preserve the exact face, hair and wardrobe of each subject from their reference.
```

### 6.3 ‏PRODUCT LOCK (מצרפים לכל פרומפט מוצר, E4)
```
PRODUCT LOCK: The product must match @Image1 exactly — same shape, proportions, colors, cap, label layout and logo. Do not redesign, rename, add text or change the label. Keep the logo sharp and readable; if unsure, keep the label partially turned away rather than distorted.
```

### 6.4 ‏PRESERVE ל-V2V (בחירה לפי מה שחשוב)
```
Preserve the composition, camera position, lighting and performance rhythm of @Video1. Only modify [the subject's expression / the environment / the wardrobe].
Keep the location, dialogue and actions identical to @Video1. Only change camera position, lens and framing per shot.
Keep the original motion, head movements, lip movements, eye line and timing exactly — preserve mouth shapes frame by frame.
```

### 6.5 תיקון לפי סימפטום (משנים שורה אחת בלבד)

| סימפטום בטיוטה | השורה שמוסיפים או משנים |
|---|---|
| הפנים נודדות | בתחילת הפרומפט: `Face lock: identical features to @Image1, zero drift.` ‏+ קליפ קצר יותר |
| מוזיקה תזמורתית אקראית | `Audio: ..., no music.` |
| שלטים ולוחיות משובשים | `no text on signs, no license plate text.` |
| שתי תנועות מצלמה / "שחייה" | מוחקים תנועה אחת: `Camera: [one move] only.` ‏+ ‏`Cut to` |
| רגליים מחליקות, ריחוף | `PHYSICS: feet plant firmly, weight transfer on each step.` |
| דמויות מחליפות צד | `FIRST FRAME AND BLOCKING: woman frame-left x 30%, man frame-right x 70%.` |
| פתאום יש חמישה אנשים | `MEMBER COUNT LOCK: exactly four.` |
| ב-V2V הכל השתנה, גם התנועה | בתחילת הפרומפט: `Preserve the original performance exactly. Only modify the environment and wardrobe.` |
| ב-Genjutsu הרכב "מתנפח" | מקצרים ל-6–8 ש', או מוחקים את שורת הרכב |
| תנועה מהירה נמרחת | `speed ramp into slow motion` + שוטים קצרים |
| אצבעות נמסות סביב כוס | שוט רחב יותר, `hands grip firmly`, ידיים חלקית מחוץ לפריים |
| בקשה נחסמה במודרציה | מורידים "rich", "money", שמות מותגים. בודקים שהתמונה שלכם בלבד |

---

## 7. אינדקס מהיר: פורמט ← פרומפט ← עלות

| פורמט | פרומפט מומלץ להתחלה | מנוע | עלות לתכנון | ללקוח (פרק 10 §3.2, רשמי) |
|---|---|---|---|---|
| הרילס הראשון שלך | **V02** | Seedance 2.5 | ‏₪4.5 טיוטה / ₪42 | — |
| ‏"STEAL MY PROMPT" (אני בפרסומת) | V01, ‏V03 | Seedance 2.5 | ‏₪63–127 | פרסומת קולנועית ₪2,500 |
| ‏Reality-Swap בעברית | **V37 + V38** | Genjutsu | ‏₪163 (35 ש') | רילס היברידי ₪1,800 |
| עולם חדש מסטודיו ריק | V40 | Genjutsu | ‏₪71 לעולם | Premium ₪3,000 (3 עולמות) |
| ‏Infinite Angles | **V47** (חשבון), ‏V48 (לקוח) | Seedance 2.5 Edit | ‏₪27–80 | ‏₪1,800 |
| מוצר / e-commerce | V16, ‏V18 + ‏M3 | Seedance / Kling | ‏₪11–63 לקליפ | ‏Pilot-10 ₪3,500 |
| ‏UGC | V59, ‏V61 | Veo / Kling Turbo / Seedance | ‏₪9–50 | אצוות UGC ₪2,500 (5 מודעות) |
| ‏Hybrid placement | V64 + ‏MASTER-E | Genjutsu | ‏₪55 + ₪46 לכל SKU | לפי פרק 10 §3.2 |
| עסק שכונתי (קולאב) | **V68** | Seedance 2.5 Edit | ‏₪40 | פיילוט ₪1,000–1,200 |
| נדל"ן | V30, ‏V29 | Genjutsu / Seedance | ‏₪71–76 | רילס היברידי ₪1,800 |
| משפיען AI | V65, ‏V66 | Seedance / Kling MC | ‏₪12–34 | — (ערוץ שלך) |
| B-roll זול למלאי | V06, ‏V12, ‏V20, ‏V26 | Kling 3.0 | ‏₪6–11 | — |

---

## מקורות

**פנימיים (מקור האמת לכל מספר ולכל פרומפט):**
- `chapters/00-visual-analysis.md`: פרומפט דובאי המתומלל, רשימת השוטים והפלט של rourke, ממשק Genjutsu ("Same video, but inside a subway"), רילס האסטרונאוט ו-AI Influencer.
- `chapters/03-craft.md`: §2 (רשימת שוטים ו-timecodes), §3 (רפרנסים, Self Reference Kit, keyframes), §4 (אנטומיה, אוצר מילים, binding, אודיו, negatives, meta-prompt), §5 (טיוטות וכשלים), §6 (V2V, ‏Reality-Swap, ‏Infinite Angles), נספח א' (37 הפרומפטים של C1 ותוספות C2/C3).
- `chapters/02-tools-stack.md` §1–2: טבלת ההחלטה, מפרטי מודלים, מחירי API לשנייה.
- `chapters/10-numbers-capacity-pricing.md` §1.1–1.2 (עלויות לרילס ויחסי ניסיונות), §3.2 (מחירון ללקוח), §4 (מדיניות ספק-אדים ונוסחי disclaimer).
- `chapters/11-first-video-60-minutes.md` §4.4–4.5 (הפרומפטים הגנריים לרילס הראשון), §5.2 (טבלת "השינוי האחד"), §8 (ניסוי העברית).
- `chapters/06-legal-ops.md` §4 (טבלת החלפת מותגים).
- `workers/C1.md` (34 פרומפטים ו-meta-prompt), ‏`workers/C2.md` (keyframes, ‏binding, ‏6 משבצות), ‏`workers/C3.md` (Reality-Swap, meta-prompt ל-Infinite Angles, מתכונים), ‏`workers/E4.md` §7–8 (10 וריאציות מוצר, ‏PRODUCT LOCK, ‏hybrid placement), ‏`workers/D3.md` §11 (15 רעיונות לרילס).

**חיצוניים (כפי שצוטטו בפרקים המקוריים):**
- Higgsfield, Seedance 2.5 Prompting Guide: https://higgsfield.ai/blog/seedance-2-5-prompting-guide
- Higgsfield, Genjutsu: https://higgsfield.ai/genjutsu · https://higgsfield.ai/blog/higgsfield-genjutsu
- Runway, Seedance 2.5 Prompt Guide: https://runway.com/resources/seedance-2-5-prompt-guide
- Kapwing, How to prompt Seedance 2.5: https://www.kapwing.com/resources/how-to-prompt-seedance-2-5-a-guide-for-ai-video-creators/
- fal, Multi-angle video with Seedance 2.5: https://fal.ai/learn/tools/how-to-create-multi-angle-video-seedance-2-5
- fal, Seedance 2.5 image-to-video: https://fal.ai/models/bytedance/seedance-2.5/image-to-video
- media.io, Genjutsu tutorial (CHANGE/PRESERVE): https://www.media.io/video-effects/higgsfield-ai-genjutsu-tutorial.html
- Atlabs, Ultimate Seedance 2.5 prompting guide: https://www.atlabs.ai/blog/ultimate-seedance-2.5-prompting-guide-2026
- MindStudio, Seedance 2.5 multimodal reference system: https://www.mindstudio.ai/blog/seedance-2-5-multimodal-reference-system-explained
- Runware, Seedance 2.5 multi-reference production: https://runware.ai/docs/models/bytedance-seedance-2-5/guides/multi-reference-production
- Morphic, Seedance 2.5 guide: https://morphic.com/resources/how-to/seedance-2-5-guide
- invideo, character reference sheet: https://invideo.io/faq/how-do-you-create-a-character-reference-sheet-using-nano/
- Curious Refuge, changing camera angles with AI: https://curiousrefuge.com/blog/how-to-change-camera-angles-with-ai-video
- Google Cloud, Veo 3.1 prompting guide: https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
- Atlabs, Kling 3.0 prompting guide: https://www.atlabs.ai/blog/kling-3-0-prompting-guide-master-ai-video-generation
