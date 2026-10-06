# פרק 19: תהליכי הפקה למודעות, עריכה ואפקטים, ודקדוק פרומפט

> **מה בפרק:** חמישה תהליכי עבודה מלאים למודעות של 15/30/60 שניות עם עלויות · מה למדנו מ-24 רילסים ויראליים (הוקים, קצב, סיומים) · תפריט אפקטים (מה המשתמש אומר בעברית ← מה Claude עושה) · חיתוך על הביט · כתוביות בעברית · סאונד ורישוי מוזיקה · דקדוק פרומפט לכל פורמט, עם כ-15 פרומפטים אמיתיים מילה במילה.
> **מקורות:** הערות סבב 2: [T5 תהליכי הפקה](../round2/notes/T5.md) · [T6 עריכה ב-ffmpeg](../round2/notes/T6.md) (כל מתכון הורץ בפועל; סקריפטים ב-[T6-scripts](../round2/notes/T6-scripts/)) · [V1 ניתוח 24 רילסים ויראליים](../round2/notes/V1.md) · [V2 פרומפטים אמיתיים של יוצרים](../round2/notes/V2.md) (46 פרומפטים). מנוע העריכה: [skills/reel-studio/SKILL.md](../../../skills/reel-studio/SKILL.md).
> **מספרים:** Higgsfield ‏20 קרדיט = $1. עלויות "$ למודעה" הן **[הערכה]** וכוללות ניסיונות חוזרים. כשיש סתירה, [פרק 10](10-numbers-capacity-pricing.md) גובר. שער ‏1$ = ₪3.04.

---

## תקציר

1. **מודעה טובה היא בערך 5% ג'נרציה ו-95% תכנון ובחירה.** "The finished ad is just the best few seconds out of 100 tries cut together. Iteration is the skill" (`3rDs6FhFoUQ` 35:00). כל התהליכים כאן נועדו להפוך את 100 הניסיונות לזולים.
2. **נועלים קודם, מייצרים אחר כך.** כל דמות, לוקיישן, מוצר ותלבושת נבדקים בתנועה עם פרומפט פשוט אחד לפני שנכנסים לסצנה. "Images are cheap, videos aren't."
3. **ברירת המחדל ללקוח אמריקאי היא "Silent plate":** וידאו בלי טקסט, בלי לוגו ובלי קריינות. VO, כתוביות, מחיר ו-CTA נוספים בעריכה (Claude עם ffmpeg). כשהלקוח משנה הצעה או רוצה ספרדית, לא מייצרים וידאו מחדש.
4. **שני מוצרים שונים, לא לערבב:** רילס ל**לייקים** (רגע אחד, מוזיקה בלבד, בלי טקסט, עד 30 שניות, לופ) ורילס ל**לידים** (הוכחה ב-split screen ו-"Comment X"). ה-CTA מכפיל תגובות פי 10–100, אבל שובר את הלופ.
5. **עברית רק ב-ASS** עם `Encoding=-1` ו-RLM בתחילת כל שורה. `drawtext` שובר עברית מעורבת. נבדק אוטומטית.
6. **הפרומפט הוא מסמך הפקה, לא תיאור.** מצלמה כעובדות פיזיות (מטרים, גובה, עדשה, תנועה אחת), רגש כהתנהגות, פיזיקה לפי סדר הכשל, שורת "End with…", ולכל רפרנס תפקיד אחד וגם "do not use".

---

## 1. הצינור האוניברסלי

### 1.1 שישה שלבים (המודל של Higgsfield, 17.09.2026)
| שלב | מי | כלי |
|---|---|---|
| 1. מחקר קריאייטיב | Claude + Meta Ad Library | Meta MCP |
| 2. קונספט ותסריט | Claude | [פרק 17](17-creative-director-system.md) |
| 3. הפקת נכסים | Claude + Higgsfield MCP (`https://mcp.higgsfield.ai/mcp`) | Soul 2 / Soul Cinema, ‏GPT Image 2.5, ‏Nano Banana 2, ‏Seedance 2.5 |
| 4. וריאציות | Ad Multiplier, ‏Genjutsu, ‏Lipsync, ‏Reframe | Higgsfield |
| 5. פרסום | TikTok ישירות מה-MCP. ‏Meta: קמפיין **paused** + העלאת וידאו ידנית | Meta MCP |
| 6. לולאת ביצועים | Claude קורא דוחות | [פרק 16](16-product-fidelity-and-ad-strategy.md) |

**רמת אוטונומיה ללקוחות בהתחלה: "Operator"** (Claude מייצר, אתה מפרסם). אף פעם לא מפעילים תקציב בלי אישור.

### 1.2 מבנה זמן לפי אורך (אנגלית, כ-2 מילים לשנייה)
| אורך | ביטים | מילים ב-VO | הערה |
|---|---|---|---|
| **15s** | ‏0–2 הוק (מקומי + כאב) · 2–6 הקשר · 6–11 מנגנון/הצעה · 11–15 הוכחה + CTA | 25–30 | ג'נרציה אחת. ב-UGC מדבר: **+2 שניות באפר** (להגדיר 17) |
| **30s** | הוק · בעיה · מוצר בפעולה (2–3 שוטים) · הוכחה (מספר אמיתי) · התנגדות · CTA | 55–65 | Seedance 2.5 נותן 30 שניות בג'נרציה אחת |
| **60s** | שני חצאים של 30 עם **match cut**, או 4 בלוקים של 15 | 110–130 | אין מודל שנותן 60 שניות Hero בטייק אחד |

**טריק החיבור (match cut):**
```
Rework 2A. Kill the warm-up. Match the opening tap to the closing tap of 1C exactly. Same hand, same motion. So it match cuts clean.
```
**מסגרות מסר (Higgsfield, 10,000 מודעות):** למוצר **PROOF** (Promise, Receipts, Offer, Objection, First step). לשירות **QUEST** (Qualify, Understand, Educate, Stimulate, Transition), בשלושה פורמטים: quiz, ‏case story, ‏direct offer (`MESSAGE US "AUDIT"`).

---

## 2. חמישה תהליכי עבודה

| # | תהליך | למי | אורך | עלות כלים [הערכה] |
|---|---|---|---|---|
| **W1** | **Local Service Ad Machine** (UGC או faceless, לוח 8 משבצות) | HVAC, גגות, ניקיון, ציפוי קרמי, בריכות, מד-ספא, נדל"ן | 15–20s | **~$16–27** לווידאו + 2 סטטיים |
| **W2** | **Spec Commercial** קולנועי (4–5 סצנות) | מותג DTC, מסעדה, אלקטרוניקה. תיק עבודות ופיץ' | 30s | **$90–145** (עם Draft ~$85; גרסה פשוטה ~$42) |
| **W3** | **Silent Plate / One-Take** (ג'נרציה אחת, VO בעריכה) | עסקי שירות, מסעדה, השקת מותג | 30s | **~$29–35** (ב-Lovart ~$5–15 + מנוי) |
| **W4** | **מכונת וריאציות** (Genjutsu, ‏Ad Multiplier, לוקליזציה) | לקוח עם מודעה מנצחת שהתעייפה | 10–15s לווריאציה | **~$3–7 לווריאציה**; ‏20 מודעות EN+ES ב-~$110 |
| **W5** | **המסלול הזול** (Storyboard-grid → ג'נרציה אחת) | בדיקת קונספט, לקוח קטן ($300–500), תוכן לחשבון שלך | 15s | **~$10** |

**אמת מידה:** יוצר UGC אנושי גובה "$100 to $200 for a single ad". בניסוי של Higgsfield יצאו כ-$8–12 לנכס. עלות הכלים ב-W1, ‏W3 ו-W5 היא **פחות מ-10% מהמחיר ללקוח**, ולכן מתמחרים לפי זמן ותבנית (פרק 10), לא לפי קרדיטים.

### W1. ‏Local Service Ad Machine (15–20 שניות)
**צעד 0, intake (הלקוח עונה תוך 2 דקות):**
```
1. Business name + city?
2. What's your Google review count and star rating?
3. Years in business / jobs completed (any real number we can brag about)?
4. Current offer or discount you're willing to run? (If none, I'll use the industry's proven default)
5. Any photos/videos of you, your team, or recent jobs? (Send 2-3 if yes)
6. English, Spanish, or both?
```
**שאלה 6 קריטית בדרום פלורידה:** "bilingual" = שתי גרסאות קופי, "written natively… never a literal translation".
**צעד 1, פקודה אחת ל-Claude:** `Generate me [X] video ads and [Y] static ads for a [NICHE] client. Business name: [NAME]. Location: [CITY, STATE].`
**צעד 2, פורמט מתוך 10** (Talking-head, ‏POV באתר העבודה, תהליך "מספק" faceless, לפני/אחרי, עדות, VO + B-roll, הסבר, אווטאר, ראיון רחוב, רחפן). לא חוזרים על פורמט ב-3 סרטונים. **מד-ספא: בלי לפני/אחרי.**
**צעד 3, סקריפט:** חובה בכל מודעה: אסימון גיאוגרפי, מספר הוכחה **אמיתי**, דולר או ימים בהצעה, CTA עם דדליין.
**צעד 4, הלוח של 8 משבצות (הלב של השיטה)**, ב-`gpt_image_2`, ‏21:9, ‏2k, עם רפרנס דמות:
```
One horizontal 21:9 storyboard image containing EXACTLY 8 vertical 9:16 panels in ONE row.
Same person as @Image1 (identity, outfit, setting identical in all 8 panels).
Alternate SELFIE / STATIC POV panel by panel; alternate distance bands (tight / macro / medium / wide) so no two adjacent panels share both POV and band.
Name hand placement in every panel (max 2 hands; in selfie panels one hand holds the phone, out of frame).
Panels map to 8 beats: 1 hook, 2 context, 3 detail, 4 turn, 5 mechanism, 6 reaction, 7 result, 8 close.
[Panel 1: ...] ... [Panel 8: ...]
No on-image text, no logos, no fisheye, no deformed hands.
```
**צעד 5, קליפ:** Seedance 2.5 עם 8 חיתוכים מתוזמנים (משך ÷ 8) ושדה אודיו עם הסקריפט מילה במילה. **Draft ב-480p קודם.**
**צעד 6, שער ציות:** לא ממציאים מספר ביקורות, שנים או אחריות (`[X]+ 5-star Google reviews`). נדל"ן: Special Ad Category. מד-ספא: "neuromodulator" ולא Botox, בלי הבטחת תוצאה. גגות: "we document damage and provide a report", אף פעם לא "we file your claim". מימון: "0% APR, subject to credit approval".

### W2. ‏Spec Commercial (30 שניות)
**נכסים (נועלים כל אחד):**
- **Product sheet** ב-GPT Image 2.5 + **תווית כ-"authority"** (הפרומפט ב-V2-21, סעיף 9).
- **Character sheet** ב-Soul Cinema (8 תמונות בקרדיט אחד), **רקע אפור**, ובוחרים **2 מועמדים** ("a face that looks great as a still might fall apart the moment it moves").
- **פנים אחת בלבד בגיליון:** `Erase the face from the full body shot on the right panel.` אחרת הפנים "נודדות".
- **לוקיישן בזווית 3/4** (עומק, "way better win rate").
- **מבחן תנועה:** אותו פרומפט בדיוק, ומחליפים כל פעם רק דמות או רק לוקיישן.
- **מצב חדש = גיליון חדש** (רטוב מזיעה, תלבושת אחרת), לא תיאור במילים.
**Shot list מחובר:** Claude מקבל סקריפט + נכסים נעולים עם שמות, ומחזיר **Style prefix** אחד ופרומפטים עם שמות (1A, ‏1B). תיקון גלובלי:
```
Change the style prefix for the whole shot list. Kill the contre-jour and shadow-side framing. Let's go soft even daylight from the camera side, bright and clean. Apply to every prompt.
```
**שלושה טריקים מהמדריך הכי נצפה (657K):**
- **ריקוד = שמות של תנועות:** "You don't just write 'dances'… That means nothing to Seedance" ← `two head nods, shoulder rolling one at a time, a knee dip, a finger snap, quarter spin at the door`. ולריקוד על הביט: מצרפים את השיר כרפרנס אודיו.
- **מפה סכמטית לגיאוגרפיה** ("the number one hack to steal"): `Make a schematic. Mark the fire hydrant and lock the sky dancer to its right. It should be two times a person's height, located on the same line.`
- **Snorricam לשוט מוצר:** `Swap the middle for a single body-rig snorricam locked on the right ear cup. Camera bolted to his body. The headphones rock solid dead center. Everything behind him whipping past in motion blur.`

### W3. ‏Silent Plate (30 שניות, ג'נרציה אחת)
**שלד הפרומפט** (Higgsfield, מקוצר; הכותרות בדיוק כך):
```
ACTIVE REFERENCES
<<<image_1>>> = JOHN — defines face, build, dark navy polo and light khaki work trousers only. 100% match at every distance; the sheet's background, lighting and pose are not inherited.
Zero video references, zero audio references.

[LOOK] Photoreal 9:16 commercial documentary, 24 fps, natural 180° shutter. Everything is a clean silent plate for an edit: no titles, no on-screen text, no logos, no screens facing camera. ...
[LIGHT] ...  [COLOR] ...
[STRUCTURE] 30 seconds of source footage, ten hard-cut stages, one location per stage. ... No zooms; when the camera gets closer it walks.
[PHYSICS] ...
[RULES] 1. Characters match references at every distance; no stand-ins. 2. One primary action per stage, one reaction. Hands do one thing at a time. 3. ... no brand marks anywhere. 4. No readable text is generated anywhere.
ACTING TASKS ...
ACTION TIMING
0-2s INSERT, 85 mm, ... END STATE: ...
[Sound design] Silent plates: no dialogue, no narration, no music; all visible characters keep their mouths naturally closed. Voice-over is added in the edit. Faint natural room tone and contact sounds at low level for the editor to keep or mute.
HOLD FOR THE FULL TIMELINE
```
**כשדמות UGC מדברת: "Acting Task" מלא** (MOTIVE, ‏GOAL, ‏OBSTACLE, ‏TACTIC), למשל: "keep this a friends' show-and-tell across a kitchen table, never a sales pitch; the moment it sounds like an ad, the friends are gone." ועוד שורה: `HARD RULE FOR EVERY OBJECT IN FRAME: every item is a plain, generic, unbranded version of itself`.
**החוזה של Claude כעורך** (שכבת הטקסט וה-motion graphics; מקוצר):
```
Work as my motion designer and video editor. Add finished motion graphics to the attached video and render the result. Execute the edit, not just a written plan.
Start by inspecting the entire video: cuts, speech, existing graphics, faces, hands, product movement and available space for text.
Preserve the original footage, duration, cuts, playback speed and audio unless I explicitly request changes.
Use the exact screen copy from my brief. Do not invent discounts, prices, results, product claims or brand names.
Keep graphics clear of faces, hands and the product throughout their entire appearance.
Give each graphic a deliberate entrance, readable hold and coordinated exit. Synchronize graphics with the relevant action or spoken phrase.
First create and inspect representative frames from the opening, the busiest scene and the ending, plus one complete animated transition.
Review the finished video at normal speed, text readability at phone size, audio sync and the final frame.
Briefly state what you changed and what you actually checked.
```
**גרסת Lovart:** פרומפט אחד שמבקש **4 תמונות נפרדות** (לוגו, אריזה, מדי עובדים, פנים המקום), מעלים ל-Assets Library (Seedance לא מושך תמונות עם אנשים ישר מה-canvas), ואז 30 שניות "one continuous shot" ב-16:9. מתאים לפיץ' למסעדה לפני שיש תקציב.

### W4. מכונת וריאציות (מודעה אחת ← 20–100)
- **מסלול A, ‏Genjutsu Motion Transfer (שחקן חדש, אותה הופעה):** מפרקים את המודעה לסצנות ו**מייצאים raw** (בלי כתוביות ו-SFX). מכל סצנה צילום מסך, ובונים דמות חדשה **באותה תנוחה** ב-Nano Banana Pro: `make me a man 50 years old wearing suit white beard. Make him in the same position as in image one.` ב-Genjutsu מדליקים את ה-prompt: `Use the man from image one.` ‏**Change voice** עולה קרדיט אחד. "In 1 hour you could make like 20 variations."
- **מסלול B, ‏Object Swap / Ad Multiplier (מוצר או טעם אחר):**
```
Take this approved ad and create versions where the product is replaced with the second product from my references. Preserve the presenter, the timing, and the camera movement from the source.
```
  **תנאי:** מוצר בגודל ובאחיזה דומים. אחרת ההחלפה נכשלת.
- **מסלול C, לוקליזציה:** Translate ← Lipsync Studio ← Reframe ל-9:16, ‏1:1 ו-16:9. ספרדית ארוכה מאנגלית בכ-15–25%, אז מקצרים. **בדיקה של דובר שפת אם חובה.**
- **המטריצה:** מאסטר ← 5 הוקים × 5 מוצרים × 4 שפות = 100. אין כפתור batch; סקייל עובר דרך לולאת MCP ב-Claude.
- **עלות לווריאציה (10 שניות, 720p):** Marketing Studio $3.00 · ‏Genjutsu $3.58 · ‏Seedance Edit $3.30 · ‏Relight $4.50 · ‏Lipsync $2.90 · ‏Change voice $0.05.
- **מבצעים:** כשיש "70% OFF + unlimited Genjutsu for 7 days", מרכזים את עבודת הווריאציות של כל הלקוחות לשבוע הזה.

### W5. המסלול הזול (~$10 ל-15 שניות)
1. Character sheet ב-GPT Image 2.5 (חזית, גב, פורטרט חזיתי וצדדי). למוצר גם תמונת "פירוק": `Using that image one, disassemble it and lay out each individual part separately, set against a clean pure gray background.`
2. **Storyboard בתמונה אחת** (עד 4K), כי "the storyboard is the blueprint".
3. ג'נרציה אחת עם פרומפט קצר:
```
Use the reference storyboard as a complete animation film preserving character consistency and visual style. Smooth camera movement and natural storytelling. No text or subtitles. Audio: diegetic sound only. Natural ambience, environmental foley, and subject-driven sound.
```
4. Draft ב-480p (‏~$2.25). **מתקנים את ה-board, לא את הווידאו.** אחר כך 720p (~$4.9).
5. תיקון נקודתי בלי ג'נרציה מחדש: `[At 0:06–0:09] Replace the background with a futuristic neon technology environment while keeping the earbuds, person, camera movement, and overall composition consistent.`

**Kling:** Kling 3.0 ב-Unlimited (שנתי) ל-B-roll בעלות שולית $0. ‏**Kling 4.0** (אוקטובר): 30 שניות native, עד 10 keyframes. בהשוואה של 11 פרומפטים Seedance 2.5 "looks more realistic. Kling 4.0 had a bit of plastic look" ← **Seedance לשוט ה-Hero, Kling ל-B-roll.**
**"חינם" לגיטימי בלבד:** 66 קרדיט הרשמה ב-Kling, ‏Firefly חינמי. **לא** פותחים חשבונות עם מיילים זמניים (הפרת תנאי שימוש, ובלי זכויות מסחריות ברורות).

### 2.6 ספר חיסכון בקרדיטים (10 הראשונים לפי השפעה)
1. **מבחני תנועה קצרים לכל נכס** לפני סצנות מלאות: 30%–50% פחות ג'נרציות לפח.
2. **Draft ב-480p ← 1080p:** כ-60% מעלות האיטרציה.
3. **מפה סכמטית או Blender** במקום "20 generations just to fish out a few good seconds".
4. **Storyboard grid אחד** וג'נרציה רב-שוטית אחת: כ-50%.
5. **Silent plate:** שינוי מסר = $0.
6. **Edit במקום regenerate** (Seedance Edit עם חותמת זמן): כ-40% לכל תיקון.
7. **משתנה אחד בכל ריצה.**
8. **+2 שניות באפר לדיאלוג** (חוסך קליפ שנחתך באמצע משפט).
9. **720p וייצוא ב-1080p** לפיד: 30%–50%. ‏Meta ו-TikTok דוחסים בכל מקרה.
10. **שגיאה גנרית פעמיים = נגמרו הקרדיטים.** לא מנסים בפעם השלישית.

---

## 3. מה למדנו מ-24 רילסים ויראליים (V1, ספטמבר–אוקטובר 2026)

**השיטה:** כל רילס נמדד ב-ffprobe ו-scdet, עם רשתות פריימים שנצפו בעין ותמלול ב-faster-whisper. אינסטגרם בלבד (YouTube חסם).

### 3.1 המספרים
- **6 הרילסים עם הכי הרבה לייקים (100K–2M):** ‏15.6–37.8 שניות (חציון ~26). **באף אחד אין קריינות ואין טקסט על המסך.** מוזיקה בלבד.
- **שני קטבים של קצב:** (א) **טייק אחד רציף** שנראה כמו צילום טלפון: 0 חיתוכים ב-26–29 שניות (jean_philanthrope, ‏195K ו-219K) או שוט אחד של 15 שניות (Sapphire Princess, ‏2M). (ב) **מונטאז' מוזיקלי** עם שוט חציוני של 1.1–1.7 שניות.
- **4 מתוך 6 המובילים לא אנכיים** (16:9 או 4:3). "לוק של סרט" לא חייב להיות 9:16.
- **עוצמה:** כל 28 הקבצים ב-‎-14.1 עד ‎-14.8 LUFS. היעד ביצוא: ‎-14 LUFS.
- **יחס תגובות ללייקים:** רילס עם "Comment X": ‏0.07–1.74 (מאור חני: 2,060 תגובות מול 1,183 לייקים). רילס בידור: 0.002–0.02.
- **צפיות של מותגים ב-YouTube מנופחות בקידום** (43M צפיות ו-181 לייקים). ויראליות מודדים בלייקים ובתגובות.

### 3.2 הוקים (0–1.5 שניות)
**ב-6 המובילים ההוק תמיד ויזואלי בלבד:**
- **H1 פנים בעדשה:** פנים רוכנות לטלפון, מבט ישיר.
- **H2 מאש-אפ אבסורדי בפריים אחד:** אבירים במסוק Huey, חתלתול-אביר מול ברברי.
- **H3 in medias res:** הפעולה כבר באמצע.

**הוקים ללידים:** ‏H5 הוכחה בפיצול מסך (CCTV→Cinema, מאור חני) ו-H9 מספר הוכחה ("4.3M views"). **עוד:** cold open עם שורה מהסוף, blockout ואז reveal, טייק חם ("Who even listens to K-pop?"), וידוי ("I'm an AI addict"), כרטיס ז'אנר (לוגו של סיטקום משנות ה-90), שורת דיאלוג מזלזלת ("Thank you, Nicholas. You can go now.").

### 3.3 קצב לפי ז'אנר
| ז'אנר | משך | חציון שוט | חיתוך ראשון |
|---|---|---|---|
| מיקרו-סיפור רגשי | 20s | 1.7s | 0.8s |
| מונטאז' גאגים | 27s | 1.7s | 1.5s |
| אקשן / מרדף קולנועי | 30–140s | 1.65s | 0.9s |
| הדמו ב-split (לפני/אחרי) | 16s | 1.2s | 1.3s |
| blocks→reality | 13s | 1.0s (על הביט) | 4.5s (ה-reveal) |
| "photo dump" אופנה AI | 11s | 1.16s | 1.7s |
| רגע יפה בשוט אחד | 15.6s | 15s | — |
| סקיצה עם דיאלוג | 64–73s | 4.5s | 3.5–4.9s |

**כלל אצבע:** במונטאז' מוזיקלי חותכים כל 1.5–1.7 שניות (בערך 2 ביטים ב-75–80 BPM). אחרי reveal, בפריסת פרטים, חותכים על כל ביט. **שוט של יותר מ-4 שניות מחזיק רק אם יש בו reveal או דיאלוג.**

### 3.4 סיומים, טקסט ותובנות
- **סיומים:** לופ מושלם (פריים אחרון ≈ ראשון) · bookend (אותה קומפוזיציה עם שינוי רגשי) · פאנץ' דיאלוג · end card של מותג · CTA בתגובות · cut to black של חצי שנייה. **בגרסת ויראליות:** לופ, וה-CTA רק בכיתוב. **בגרסת לידים:** "Comment X" בקול ובטקסט בשנייה האחרונה.
- **טקסט על המסך, 7 סגנונות:** בלי טקסט (המובילים) · מילה אחת במרכז · 1–2 מילים ב-CAPS עם צל · משפט בשתי שורות עם קו מתאר (TikTok) · כתוביות קטנות · כותרת קבועה בראש ("Cinema from CCTV") · תוויות על פאנלים ("AI" / "אמיתי").
- **הכי מצליח לא נראה כמו AI ולא כמו קולנוע:** טלפון על שולחן וטייק אחד (219K), או אנימציה בסגנון דיסני הישן (2M). המשותף: **סגנון מוכר**, לא "וואו טכנולוגי".
- **סדרתיות:** כל החשבונות המצליחים מריצים **תבנית אחת עם וריאציות** ("If X had Instagram", ‏"Oui Madame", ‏"Cinema from CCTV"). **ללקוח בונים "תבנית סדרה", לא רילס.**
- **שלושה חוקי V2V חדשים (rourke):** ACTION LOCK, ‏FORBIDDEN ANGLE ו-PATH MARKER (קווים אדומים שמסמנים מסלול ולא מרונדרים), ומשך היצירה = משך המקור + שנייה. ובצילום הקלט ל-Genjutsu: **מיפוי צורות** (מדרגות חירום ← מדרגות מטוס).

---

## 4. תפריט אפקטים: "המשתמש אומר X" ← "Claude עושה Y"

**המנוע:** `skills/reel-studio/scripts/reelstudio.py` מרנדר spec של JSON. **הטבלה המלאה של ביטוי בעברית ← שדה ב-spec נמצאת ב-[SKILL.md, "Hebrew phrase → spec mapping"](../../../skills/reel-studio/SKILL.md)** (חיתוך, פייד, וויפ, זום פאנץ', קן ברנס, שייק, גליץ', גרעין, טיל-אורנג', letterbox, סלואו, ספיד ראמפ, מסך מפוצל, לפני-אחרי, blocks→reality, PiP, "פרומפט על המסך", כותרות, כתוביות, לוגו, פאקשוט, ducking, SFX, ‏-14 LUFS ופריסטים).

**מה T6 מוסיף מעבר למנוע** (נבדק ב-ffmpeg 6.1; מתכונים ב-`round2/notes/T6-scripts/recipes.sh <name>`):

| המשתמש אומר | Claude עושה | ברירת מחדל |
|---|---|---|
| "תוסיף אפקטים" (בלי פירוט) | חבילת בסיס: beat-cut, ‏zoom_punch על downbeats, ‏whip בין שוטים, impact shake + hit על הדרופ, grain 0.25, ‏SFX על כל חיתוך, ‏-14 LUFS | **שואלים שאלה אחת:** "אנרגטי (מוזיקה, רכבים) או נקי (יוקרה, נדל"ן)?" |
| "ויפ" / "שהמצלמה תיזרק" | whip אמיתי עם blur כיווני | ‏0.25 שניות + whoosh |
| "מעבר זום" / "שיצלול פנימה" | zoom-through | scale 1→3 ב-5 פריימים |
| "ספיד ראמפ" / "וולוסיטי" / "שיאיץ ואז יאט" | `velocity.py` (עקומת ease כמו CapCut) | `"0:1,T-0.3:1,T:3,...,0.4"` |
| "סלואו מושן" | optical flow (`minterpolate=mci`) על הקטע בלבד | ×3 |
| "רעידה כשהוא נוחת" | impact shake דועך על ה-hit | 28px, דעיכה 9 |
| **"שייראה מצולם ולא AI"** | handheld עדין + grain אמיתי 0.3 + halation 0.4 + SFX אווירה | תנועה של 2%–4% |
| "לוק קולנועי" | LUT ‏teal&orange ב-60% + halation + letterbox 9% + grain 0.25 | — |
| "VHS" / "שנות ה-90" | vhs | — |
| "בצבעי המותג" | duotone בצבעי המותג | — |
| "דליפות אור" / "פילם ברן" | light leak בין שוטים | ‏0.6 שניות screen |
| "תקפיא ותכתוב מי זה" | freeze intro + ASS | ‏1.5 שניות, punch 12% |
| "בומרנג" / "טריילים" | boomerang / echo trails | — |
| "תדגיש את המילה החשובה" | stack: מילה ב-170px צהובה במרכז, השאר 70px | — |
| "תוסיף אימוג'י" | PNG מ-Noto Color Emoji ← overlay (סעיף 6) | — |

**כלל:** אחרי בקשה מעורפלת, Claude מרנדר **גרסה אחת** + contact sheet (`reelstudio grid`) ושואל "יותר / פחות / אחר". לא מציג 5 אופציות.
**טעם ("מתי לא"):**
- יוקרה, נדל"ן, אוכל: **בלי** glitch, ‏VHS, ‏spin או RGB. כן: חיתוך על ביט, whip עדין, light leak, halation, ‏grain 0.2.
- טק, גיימינג, AI-reveal: כן glitch, ‏RGB ו-flash.
- רכבים, ספורט, אופנה: velocity, ‏impact shake, ‏zoom-through, ‏flash.
- **לא יותר מ-2 סוגי מעברים בסרטון.** חיתוך נקי על הביט הוא ברירת המחדל.

---

## 5. חיתוך על הביט

```bash
pip install librosa        # first run ~30s (numba JIT)
python3 beats.py music.mp3 --band low --every 2 --min-gap 0.35
# -> {"engine":"librosa","bpm":117.45,"beats":[...],"downbeats":[...],"cuts":[...],"onsets":[...],"drop":4.0}
python3 beats.py music.mp3 --engine numpy --band low     # no librosa: ffmpeg decode + spectral flux
python3 beatcut.py music.mp3 out.mp4 clip1.mp4 clip2.mp4 clip3.mp4 --every 2 --max 15 --punch --flash-downbeats
```
- **`--band low` (מתחת ל-160Hz) ננעל על הקיק.** בלי זה librosa ננעל על ה-hi-hat (חצי ביט). ברירת המחדל לפופ, EDM, טראפ ופונק. `full` רק למוזיקה אקוסטית.
- **drop** = הקפיצה הגדולה באנרגיה מתחת ל-150Hz. שם נכנס ה-reveal, ושם ה-riser נגמר.
- `downbeats` = כל ביט רביעי (קירוב). אם הפלאש נופל באמצע תיבה, מזיזים 1–3 ביטים.
- **beatcut.py** מקביל ל-Auto Beat Sync של CapCut. נבדק ב-scdet: החיתוכים בדיוק על הנקודות. **התיקון החשוב:** מעגלים כל חיתוך לגריד של 1/30 שנייה (אחרת יש drift של 20–40ms).
- **אורך חלון ב-120 BPM:** `--every 1` = ‏0.5 שניות (הוק) · `--every 2` = שנייה (מונטאז' אנרגטי) · `--every 4` = ‏2 שניות.
- **חותמות הזמן של מודל הווידאו לא מדויקות לפריים.** חיתוך על קראק או על ביט נעשה תמיד בעריכה.

---

## 6. כתוביות וטקסט בעברית

**ממצא קריטי (נבדק אוטומטית ב-`bidi_test.py`, שצובע כל מילה ומחזיר את סדר המילים לפי פיקסלים):**

| הגדרה | עברית + אנגלית + מספרים ("יצרתי את זה ב-Seedance 2.5 תוך 10 דקות!") | "AI זה העתיד" |
|---|---|---|
| ASS ‏`Encoding=1` (ברירת המחדל של רוב הכלים) | ❌ | ❌ |
| ASS ‏`Encoding=-1` | ✅ | ❌ ("AI" זז שמאלה) |
| **ASS ‏`Encoding=-1` + RLM ‏(U+200F) בתחילת השורה** | ✅ | ✅ |
| `drawtext` | ❌ (עברית מעורבת יוצאת בסדר שגוי) | ❌ |

**כללי ברזל:**
1. **כל טקסט עברי רק ב-ASS**, עם `Encoding=-1` בסטייל ו-RLM בתחילת כל שורה, **אחרי** בלוק ה-override (`{\pos(..)}‏טקסט`). זה מה ש-`rtl_fix()` במנוע עושה. **`drawtext` אסור לעברית מעורבת.**
2. **אסור לסמוך על "קריאה" של צילום מסך.** מריצים את `bidi_test.py` על כל שורה מעורבת בפרויקט אמיתי.
3. **אף פעם לא עברית בתוך ג'נרציה של וידאו.** היא יוצאת משובשת. הכול בעריכה.
4. כותבים בסדר לוגי, כמו שמקלידים. לא הופכים מראש.
5. **אימוג'י:** libass מרנדר אותם כקו מתאר בלבד. פתרון שנבדק: PNG מ-PIL ואז overlay:
```python
from PIL import Image, ImageDraw, ImageFont
f=ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf',109)   # CBDT font: size must be 109
im=Image.new('RGBA',(136,128),(0,0,0,0)); ImageDraw.Draw(im).text((0,0),'🔥',font=f,embedded_color=True); im.save('fire.png')
```
6. **פונטים:** Heebo (ברירת המחדל במנוע), ‏Rubik, ‏Assistant, ‏Secular One. ליוקרה: Frank Ruhl Libre.
7. **תזמון:** כתוביות בעברית קצרות יותר בתווים אבל צריכות אותו זמן על המסך. מתזמנים מחדש לכל שפה, לא משתמשים בגרסה האנגלית כמו שהיא.
8. **קריינות בעברית:** כ-2 מילים לשנייה. ‏TTS בעברית: בודקים הגייה של שמות מותג והטעמה, ותמיד בדיקה של דובר עברית. **לעברית מדוברת משתמשים באודיו אמיתי מהטלפון**, לא בדיבור עברי שנוצר ב-AI.
9. **כתוביות קופצות:** whisper ← ASS בסגנון Pop או Karaoke, ‏2–3 מילים, 84–110px. תבניות ב-`kin.ass` ו-`stack.ass`.

---

## 7. סאונד

**שכבות:** (1) דיאלוג או VO, (2) מוזיקה, (3) SFX: **ambience** (כמה שכבות), ‏**foley** (דלת, שאטר), ‏**transitional** (whoosh, ‏riser).
- מוזיקה ב-‎-5 עד ‎-6 dB מתחת לווליום המקורי, עם fade in ו-out.
- **מיישרים את השיא של ה-whoosh לחיתוך**, לא את תחילת הקובץ: ה-whoosh מתחיל 0.35 שניות לפני. ‏hit על החיתוך. ה-riser **נגמר** על הדרופ.
- תנועה דרמטית: שכבות לפי תדרים (whoosh עמוק + sub + swish גבוה).
- **"כיס" EQ:** במקום רק להנמיך, חותכים את המוזיקה ב-2–4kHz כדי שהדיבור "יישב". נמדד: ducking של ‎-10.8 dB.
```bash
[voice]aformat=channel_layouts=stereo,asplit[v1][sc];
[music]aformat=channel_layouts=stereo,equalizer=f=3000:t=q:w=1:g=-4[m];
[m][sc]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=400:makeup=1[md];
[v1][md]amix=inputs=2:normalize=0[a]
```
- **`amix ... normalize=0` חובה**, אחרת כל המיקס נחלש.
- **כניסה ויציאה משיר:** כניסה = הביט הראשון של השיר הפוך (reverse) כ-riser. יציאה = reverb על הביט האחרון.
- **Seedance 2.5 מייצר אודיו גם כשלא ביקשו.** תמיד כותבים בלוק סאונד, ו-`No music` **בראש הפרומפט וגם בבלוק Sound**. במודעות עם SFX מדויק מייצרים בלי אודיו ומוסיפים SFX מספרייה.

**Loudness, ‏‎-14 LUFS בשני מעברים** (נמדד: ‎-18.2 לפני, ‎-14.1 / peak ‎-1.5 אחרי):
```bash
J=$(ffmpeg -hide_banner -nostats -i in.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p')
MI=$(echo "$J" | python3 -c "import json,sys;d=json.load(sys.stdin);print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
ffmpeg -i in.mp4 -af "loudnorm=I=-14:TP=-1.5:LRA=11:$MI:linear=true,aresample=48000" -c:v copy -c:a aac -b:a 256k out.mp4
```
**מלכודת:** אם מריצים את המעבר הראשון עם `-loglevel error`, ה-JSON לא מודפס והמעבר השני נכשל. משתמשים ב-`-nostats` בלבד.
**ייצוא סופי ל-Reels / TikTok / Shorts:**
```bash
ffmpeg -i master.mp4 -c:v libx264 -preset slow -crf 18 -profile:v high -level 4.2 -pix_fmt yuv420p -r 30 -g 60 -bf 2 \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 256k -ar 48000 -movflags +faststart final.mp4
```

---

## 8. רישוי מוזיקה ו-SFX: אזהרות

> **הכלל:** במודעה ממומנת אסור להשתמש בשיר טרנדי מוכר. רק ספרייה מסחרית, Meta Sound Collection או TikTok Commercial Music Library. לכל פרויקט שומרים `LICENSES.txt` עם מקור ורישיון לכל קובץ.

| מקור | רישיון (לפי הדף, 10/2026) | ללקוח / למודעה? |
|---|---|---|
| **Pixabay** | חינם, בלי ייחוס | כן, חוץ מתוכן עם סימני מסחר. ⚠️ טראקים פופולריים מקבלים לפעמים Content ID claim **[לא מאומת]** |
| **Sonniss GameAudioGDC** | "royalty free and commercially usable", גם לפרויקטים של לקוחות | **כן. המקור הכי טוב ל-whoosh, impact ו-riser אמיתיים.** אסור לאימון AI |
| **Freesound** | לכל צליל CC0, ‏CC-BY או CC-BY-NC | רק CC0 ו-CC-BY (עם קרדיט). **לסנן לפי רישיון** |
| **ZapSplat** (חינם) | מסחרי, אבל **חובה קרדיט** | כן, עם קרדיט בתיאור |
| **Uppbeat** (חינם) | רק לערוץ שלך | **ללקוח צריך תוכנית בתשלום** |
| **BBC Sound Effects** | אישי ולא מסחרי. "no uploading to social media sites" | **לא** |
| **YouTube Audio Library / Meta Sound Collection** | רק בתוך הפלטפורמה שלהם **[לא מאומת]** | רק שם |
| **Epidemic / Artlist** (מנוי) | לפי התוכנית | כן |
| **Suno / Udio** | רק עם תוכנית שנותנת רישיון מסחרי | עם רישיון בלבד. עדיף ספרייה |
| **SFX סינתטיים של reelstudio** | נוצרים ב-ffmpeg, בלי זכויות | כן. טובים לטיוטה |

**ספריית מינימום** (מ-Sonniss ו-Pixabay): 5 whooshes (קצר, ארוך, עמוק, swish, reverse), 3 impacts (sub, ‏boom, ‏punch), 2 risers (‏1.5 ו-3 שניות), 3 glitch, שאטר, ‏record scratch, ‏3 pop/click (לכתוביות), 3 ambience (עיר, טבע, חדר).

---

## 9. דקדוק פרומפט לכל פורמט, ו-15 פרומפטים אמיתיים

### 9.1 שש החלטות לפני כל פרומפט
1. **מצב תמונה:** `exact first frame` (I2V) או `identity reference only` (Element)? זו ההחלטה הראשונה בכל פרומפט עם תמונה.
2. **חותמות זמן או שוטים בשם?** אקשן ופרסומת: חלונות זמן של 2–5 שניות. דיאלוג או שוט רציף: Shot 1 / Shot 2 בשמם ("When you name per second details, the model starts adding its own cuts in random places").
3. **תפקיד לכל רפרנס, וגם "do not use".** רפרנס שהועלה בלי תפקיד נכנס לשורת Unused.
4. **מצלמה כעובדות פיזיות:** מרחק במטרים, גובה, צד, עדשה, **תנועה אחת**, ושלילות של תנועות אחרות ("No orbit, no crane, no sudden push-in").
5. **רגש כהתנהגות, פיזיקה לפי סדר:** המילה "scared" לא מופיעה. "Give it the order and the order is the physics."
6. **סוף מוגדר:** `End with…` או `Last frame:`.

### 9.2 התבניות (מזוקק מ-V2 §9)
**סרטון multi-shot (Seedance 2.5, ‏10–15 שניות):**
```
[REF ROLES]   @Image1 is <product/person/place>; preserve <exact features>. @Image2 is <...>. All references are ingredients, never displayed as cards.
[PREMISE]     <one sentence: genre + core event>. [already in motion from the first frame.]
<t0>s to <t1>s: <shot size>, <camera rig + height + move + speed/distance>, <~NN-degree view>. <subject action, physical>. <motivated cut cue>.
Hard cut.
... (2–5s per window; one camera move per window)
Continuity: <count of people/objects>, <wardrobe/product lock>, <light direction>, <the only intentional transformation is ...>; no <shape morphing, duplicate, text overlays, logos>.
Sound: <music style or "no music">, <SFX per beat>, <dialogue rule: "the single quoted sentence is the only speech" / "No dialogue, narrator, voiceover, subtitles">.
Last frame: <exact final composition>, <still moving / camera easing out>.
```
**שוט בודד מבוים (8–12 שניות):**
```
<Scene + subject + situation in 1–2 sentences>.
[<0:00, 0:03> beat ... (only for action beats)]
CAMERA, <start distance m>, <height>, <side>, <lens mm character>. <ONE move> <speed>. No <orbit, crane, push-in, shake...>. <subject never turns to camera>. End with <camera distance + framing>.
LIGHT, <one motivated source> + <secondary>. <falloff>. No beauty fill.
PERFORMANCE, <emotion written as physical behavior: eyes before head, breath, one step>.
ENVIRONMENT, <moving elements>. Never reveal <threat>.
SOUND, Native sound only: <closest → farthest>. No dialogue. No music.
<Photoreal style line>. Photographed rather than rendered.
End with <final state>.
```
**Keyframe / תמונה:** SUBJECT / SETTING / CAMERA (גוף, עדשה, f/, גובה ומרחק) / LIGHT (מקור, K, כיוון) / SURFACE / DELIBERATE IMPERFECTIONS / PALETTE (HEX) / COMPOSITION, ובסוף: `A single normal full-frame cinematic photograph, not a contact sheet, grid, diptych…; no written text anywhere in frame.`
**גיליון דמות בווידאו, שורת binding חובה:** `@ImageN is a three-panel character sheet of one person: … Render one normal complete human …; never reproduce panels, gray backdrop or headless anatomy.`
**Kling 4.0 / Elements:** "assign each character and location reference a clear role", ושוטים של כ-10 שניות.

**Negative בארבע שכבות:**
1. כשלי AI כלליים בשורה אחת: `warped faces, extra limbs, fused fingers, watermarks, subtitles, plastic CGI sheen, uncanny plastic skin, teleporting bodies, frozen background extras`.
2. כשלי ז'אנר, 2–3 פריטים בלבד: `no daylight outside the windows`, ‏`don't duplicate the labels on the instrument panel`.
3. נעילת זהות כשלילה: `different hoodie color, missing backpack, hair color shift`.
4. **ביטול הסיבה ולא רק הסימפטום:** `The woman is NOT holding the smartphone… tripod` במקום "no third hand". ועוד **ספירה חיובית**: "exactly TWO hands", ‏"only ONE woman".

### 9.3 הפרומפטים (מילה במילה, מתוך המקורות)
**V2-01 · מבוים מול מעורפל (מרדף בסמטה).** המעורפל, להשוואה בלבד: `A woman runs through a rainy alley at night while something chases her. Make it cinematic, realistic, tense, and dramatic.` המבוים:
```
A tense nighttime chase through a narrow rain-soaked city alley. A woman in her late 20s wearing a dark charcoal jacket runs away from camera toward the far end of the alley, repeatedly glancing over her left shoulder at an unseen pursuer behind her.
CAMERA, Camera starts roughly 4 meters behind her at waist height, slightly offset camera-right. Natural 35mm documentary lens character. Handheld tracking forward at her running pace, with restrained operator shake caused by footsteps, never smooth or floating. She remains slightly left of center so the alley depth stays visible beside her.
LIGHT, Cold overhead street lamps mixed with a single red neon sign halfway down the alley. Wet brick, metal pipes and puddles catch broken reflections. Light falls off quickly between fixtures, leaving sections of the alley close to black. No soft studio fill.
PERFORMANCE, She runs with real effort rather than a perfect sprint: shoulders rising with hard breathing, jacket fabric pulling and bouncing, wet hair sticking unevenly to her face, shoes splashing through shallow puddles. She looks back once, almost loses her footing, catches herself against the wall with one hand, then keeps moving.
ENVIRONMENT, Heavy rain, overflowing gutter water, steam leaking from a vent, scattered trash shifting in the wind. The unseen pursuer is suggested only by fast approaching footsteps and a moving shadow briefly crossing the wall behind her. Never reveal the pursuer.
SOUND, Native sound only. Her breathing closest in the mix, shoes striking wet pavement and splashing water beneath it, rain on metal fire escapes, distant traffic, then the pursuer's footsteps growing louder behind her. No dialogue. No music.
Photoreal documentary thriller. Visible skin texture, wet fabric weave, imperfect hair movement, realistic water weight and splash behavior, natural motion blur, subtle film grain. Photographed, not rendered.
End with her reaching the brighter red-neon section of the alley while the shadow behind her grows larger.
```

**V2-02 · חלונות זמן** (מקצים זמן מסך לביטים שכבר קיימים):
```
[0:00, 0:03] A thief dressed in dark clothing moves quietly through a closed museum gallery at night. The camera tracks behind and slightly to his right as he approaches a glass display case containing a small ancient gold statue. The gallery is mostly dark, lit only by faint emergency lighting.
[0:03, 0:06] He reaches the display case and slowly raises one gloved hand toward the glass.
[0:06, 0:09] Suddenly the museum security system activates. Bright white ceiling lights snap on one section at a time toward him, rapidly exposing the gallery. He freezes and turns his head toward the approaching light.
[0:09, 0:12] He abandons the display and runs toward a dark doorway at the end of the room. Security alarm tones begin as he runs.
Handheld documentary-style camera movement, realistic body mechanics, natural motion blur, hard practical lighting, deep blacks, polished stone floor reflections, photorealistic and photographed rather than rendered.
```

**V2-05 · רגש כהתנהגות** (אין את המילה "scared"):
```
A woman stands alone in a dim kitchen at night, checking her phone beside the counter. Her phone vibrates once.
She looks down and reads the message. Her expression does not instantly become exaggerated. Instead, her hand stops halfway toward the counter, her shoulders become slightly rigid, and her breathing becomes shallow.
Her eyes move toward the dark kitchen window first. A moment later, her head slowly follows.
She tightens her grip around the phone with one hand and takes one quiet step backward from the window.
Outside, the curtain shifts slightly.
A faint crunch of gravel is heard from somewhere beyond the window.
She freezes and keeps staring toward the sound. Never reveal another person or creature.
CAMERA, Single continuous medium shot from slightly behind and camera-left, roughly 4 meters away at chest height. Natural 50mm lens character. Very slow push forward throughout the shot. No orbit, no sudden zoom and no angle change.
LIGHT, One warm kitchen light above the counter provides the main motivated source. The window side of her face falls into deeper shadow. No beauty fill.
SOUND, Native sound only: phone vibration, refrigerator hum, subtle room tone, faint wind outside, one gravel crunch, and her increasingly audible breathing. No dialogue. No music.
Photoreal documentary suspense, natural skin texture, realistic hand movement, restrained facial performance, subtle fabric movement and natural motion blur. Photographed rather than rendered.
```

**V2-13 · First + Last frame, "רק מה שביניהם"** (לניסויים ולהוקים, לא לעבודת לקוח):
```
Show me what happens in between. Use multiple camera angles.
```

**V2-14 · התבנית הרשמית של ByteDance לרפרנסים:**
```
【Generation Goal】
Generate <video type or core event>. The core subject is <subject>, and the principal event is <summary>.

【Reference Asset Roles】
@Image1 is used for <subject>'s <appearance, clothing, structure, or material>.
@Video1 is used for <action, camera movement, or pacing>; do not use <identity, clothing, or scene that could be unintentionally carried over>.
@Audio1 is used for <character or sound type>'s <voice quality, dialogue, ambient sound, or music>.

【Unused Assets】
@Image2, @Video2, and @Audio2 are not used in this task or for people, scenes, props, actions, camera, or sound.

【Subjects and Relationships】
<Subject A> maps to @Image1 and always retains <fixed features>.
The spatial, prop, or identity relationship between <Subject A> and <Subject B> is <relationship>.

【Event Script】
At the start: <state of people, props, and scene>.
Principal event: <continuous action or event>.
At the end: <character positions, prop ownership, or final visual state>.

【Maintain Consistency】
Keep <character identities and count, clothing, prop ownership, spatial directions, and sound relationships> stable.
```

**V2-15 · הדוגמה הרשמית (נגר מתקן כיסא):**
```
【Generation Goal】
Generate a video of an old wooden chair being repaired. A carpenter first inspects the loose backrest, then applies wood glue and secures the joint. At the end, the chair is stable again.

【Reference Asset Roles】
@Image1 is used for the carpenter's facial features, short hair, and dark blue work apron; do not use the image background.
@Image2 is used for the old chair's curved backrest, dark wood grain, and worn areas; do not use the person in the image.
@Video1 is used for the hand movements when applying glue and pressing the joint together; do not use the character identity, clothing, or workbench from the video.

【Subjects and Relationships】
The carpenter always wears the dark blue apron defined by @Image1. There is only one old wooden chair, defined by @Image2, throughout the video. The tools remain on the right side of the wooden table.

【Event Script】
At the start, the chair is centered on the wooden table and the backrest joint is loose. The carpenter inspects the joint, applies wood glue, and uses both hands to press the backrest into place and secure it. At the end, the carpenter releases the chair, the backrest remains stable, and the chair's count and appearance remain unchanged.

【Maintain Consistency】
Keep the carpenter's identity and clothing, the chair's structure and count, the tool positions, and the studio's spatial orientation stable.
```

**V2-21 · שתי תוויות למוצר אחד** (צורה מגיליון, טקסט מקלוז-אפ):
```
image 2 corresponds with the close-ups of the front label. Use this as the authority for the exact wording, typeface, weight, color, line breaks, and the layout of the front label.
```
(ואחריו הטקסט המילולי של התווית. "On close-ups it works a lot better than shots from far away.")

**V2-25 · ‏I2V: התמונה היא פריים 1:**
```
Use the supplied image as the exact first frame. Preserve Conor's identity, face, hairstyle, burgundy leather jacket, white T-shirt, diner booth, table, coffee cup, window, lighting, camera side and framing.
Conor stays seated. He slowly lifts the coffee cup, takes one small sip, lowers it back onto the table, then looks through the rain-streaked window.
Passing car headlights briefly sweep across the diner interior from outside. His movement stays subtle and natural: breathing, slight hand movement, small fabric shifts.
Camera performs one extremely slow push forward from the exact starting composition. Do not change camera side, rebuild the environment or introduce a new angle.
Native sound only: quiet diner room tone, refrigerator hum, ceramic cup touching the saucer, rain against the window and distant wet-road traffic. No dialogue. No music.
Photoreal, natural skin texture, realistic leather and glass reflections, restrained film grain. Photographed rather than rendered.
```

**V2-26 · ‏Element-to-Video: אותה תמונה, רק כזהות:**
```
Use the supplied image as the identity and wardrobe reference for Conor only. Preserve his face, short curly brown hair, facial proportions, burgundy leather jacket and white T-shirt.
Create a completely new shot on a rainy downtown street at night. Conor walks toward camera through light rain while traffic and pedestrians remain softly out of focus behind him.
Camera starts roughly 5 meters in front of him at chest height and tracks backward at his walking pace. Natural 50mm lens character. Conor stays slightly left of center and looks past camera-right toward passing traffic, never directly into lens.
Wet asphalt reflects red traffic lights and storefront glow. One overhead streetlamp provides the main motivated light with natural falloff into the darker street.
Conor walks naturally with small shoulder movement, realistic jacket motion, breathing and wet hair movement. No posing.
Native sound only: rain, footsteps on wet pavement, passing traffic, distant horn and crosswalk signal. No dialogue. No music.
Photoreal documentary street photography, natural skin texture, wet leather, realistic reflections and restrained grain. Photographed rather than rendered.
```

**V2-27 · ניסוח רשמי ל-First + Last frame** (את שני המשפטים הראשונים כותבים מילה במילה, כל אחד משפט עצמאי; שתי התמונות באותו יחס):
```
Use @Image1 as the first frame.
This first frame defines the baking station, the cake decorator's position, the undecorated cake, tool placement, and a frontal medium-shot camera position.
Use @Image2 as the last frame.
This last frame defines the decorated cake centered on the turntable, the cake decorator's hands away from the cake, and the same frontal medium-shot camera position.
Use @Image3 for the cake decorator's facial features, updo, and white uniform without changing the first-frame composition in @Image1 or the last-frame composition in @Image2.

The shot begins naturally from the first frame defined by @Image1. The cake decorator rotates the cake turntable, continuously pipes even cream patterns along the edges of both tiers, and then places the blueberries one by one. Finally, the decorator moves both hands away from the cake and naturally arrives at the last frame defined by @Image2.
Maintain continuity from first to last in the cake decorator's identity and clothing, the number and two-tier structure of the cake, tool positions, the baking-station layout, and camera direction.
```

**V2-28 · ‏Storyboard grid כרפרנס** (עד 15 פאנלים, מעט טקסט על הגריד):
```
@Image1 provides the shot order and approximate compositions for an <N-panel storyboard grid>. Read it <from left to right and from top to bottom>; do not adopt <the sketch style, text annotations, or placeholder characters> shown in the image.
@Image2 defines <Subject A>'s <appearance and clothing>.
@Image3 defines <the structure, material, or lighting> of <a key prop or scene>.

Shot 1: <shot size, subject action, and scene state>.
Shot 2: <shot size, subject action, and camera movement or transition>.
...
Shot N: <ending action and final visual state>.

The final visuals use <visual style>. The audio includes <dialogue, ambience, action sound effects, or music>.
```

**V2-37 · תבנית העריכה הרשמית (V2V, וגם Genjutsu):**
```
【Editing Goal】
Edit @Video1, changing only <original object or region> to <target content>.

【Role of the Source Video】
@Video1 is the sole editing master and governs the original scene, camera position, camera movement, action trajectories, occlusion relationships, and event order.

【Role of the Target Material】
@Image1 is used for the <appearance, structure, or material> of <the target subject, background, or product>; do not use <irrelevant background, characters, or composition>.

【Edit Objects and Scope】
Modify only <explicit objects and regions>. The number of target objects throughout the video is <count>. Do not modify <content that must be preserved>.
Except for the objects explicitly modified above, all other visible characters, props, and background elements in @Video1 remain unchanged and are not to be replaced or removed.

【Timeline Inheritance】
<Target object> inherits the timing, duration, path, and speed changes of every appearance, movement, occlusion, and exit of <original object>.
All other character actions, camera movement, shot changes, and event order remain as in @Video1.
```
**חובה רשמית:** כל פרומפט עריכה כולל משפט "סגירת היקף" מילה במילה. עריכה מקומית: `Except for the objects explicitly modified above, all other visible characters, props, and background elements in @Video1 remain unchanged and are not to be replaced or removed.` השארת יעד בלבד: `Except for the objects explicitly retained above, remove all other visible subjects from @Video1; do not add any unspecified objects.`

**V2-38 · החלפת סובייקט נע ("motion slot"):**
```
【Editing Goal】
Edit @Video1, replacing only the red bicycle and its rider passing in front of the bench with the dark-gray electric patrol vehicle from @Image1.

【Role of the Source Video】
@Video1 is the sole editing master and governs the park road, the two people on the bench, the camera position, camera movement, the original rider's motion slot, occlusion relationships, and event order.

【Role of the Target Material】
@Image1 is used only for the body structure, color, and transparent windshield of the dark-gray electric patrol vehicle; do not use the image background or driver.

【Edit Objects and Scope】
Remove the red bicycle and its rider from the source video. There must be exactly one electric patrol vehicle throughout the video. The two people on the bench, the trees, the road, and the background remain as in @Video1.

【Timeline Inheritance】
The electric patrol vehicle fills the original rider's motion slot with exactly the same appearance timing, movement path, speed, and occlusion positions. The red bicycle and rider must no longer appear in the final video. All other character actions, camera movement, shot changes, and event order remain as in @Video1.
```
(רשימת ה-Preserve קצרה, רק מה שגובל ביעד.)

**V2-42 · ‏UGC עם חצובה: לבטל את הסיבה לכשל** (מקוצר; המקור משתמש במותג אמיתי, אצלנו מוצר של הלקוח):
```
The woman is NOT holding the smartphone.
The smartphone is placed vertically in a small, simple phone tripod/stand positioned in front of her, exactly like a casual home UGC recording setup.
The woman has exactly TWO arms and exactly TWO hands. Both hands must always be connected naturally to her two arms. Never generate a third hand, third arm, extra fingers, duplicated hands, floating hands, detached limbs, or anatomically impossible hand positions.
Do not create a mirror-selfie setup.
Do not create a reflection of the woman on the phone screen, phone glass, camera lens, or any other reflective surface.
There is only ONE woman in the entire video.
No handheld camera movement. No camera shake. No framing drift.
Use hard jump cuts between moments, like genuine social-media UGC.
*0–2s:* She has just started recording. The smartphone is already standing vertically in its small tripod directly in front of her. She is not touching the phone. [...] She says casually: "Okay… brown gloss? Hear me out."
```
("um" שכתוב **בתוך** השורה נותן דיבור טבעי.)

### 9.4 תובנות רוחביות מהיוצרים
- **מוזיקה זולגת:** `No music` בראש הפרומפט. "the things that are at the top of a prompt… it's going to hold true to that".
- **ספרו את הדיאלוג פעמיים:** כל שורה בתוך השוט שלה, ובלוק בסוף עם כל השורות לפי הסדר.
- **ההגשה חשובה יותר מהכוריאוגרפיה:** בדיאלוג מביימים "the emotion and how the line is delivered".
- **שיעור הצלחה אמיתי:** פרומפט ויראלי מורכב רץ 6–8 פעמים עד שיצא. מתכננים ×5–8 ([פרק 17](17-creative-director-system.md): ×20–25 לשוטי Hero).
- **שפת דיבור:** כותבים את השורה ישר בשפת היעד, אחרת יוצא "an accent doing an impression". לעברית: לנסות שורה בכתב עברי בתוך הפרומפט האנגלי **[לא נבדק]**.
- **Claude כ-prompt compiler:** מדביקים פרומפט שעבד ומבקשים "use this prompting structure… change into X". ו-**style block מתמונות:** מעלים 5–10 תמונות השראה ומבקשים לנתח תאורה וצבע לבלוק סגנון קבוע.
- **אורך הפרומפט לפי השליטה שצריך:** 300–700 מילים לשוט מבוים, משפט אחד כשיש start + end frame.

---

**איפה עוד:** פרומפטים לפי נישה: [פרק 15](15-product-ads-by-niche.md). נאמנות מוצר, QA ו-ffmpeg לתווית: [פרק 16](16-product-fidelity-and-ad-strategy.md). מבריף לרעיון ולפרומפט: [פרק 17](17-creative-director-system.md). ספריית הפרומפטים המקורית: [פרק 7](07-prompt-library.md).
