# פרק 3: אומנות ההפקה. פרומפטים, תמונות, הפקה היברידית ועריכה

> ראש חטיבה C (Craft) · 2026-10-05 · מאחד את דוחות העובדים C1 (הנדסת פרומפטים וספריית 37 פרומפטים), C2 (תמונות רפרנס), C3 (הפקה היברידית Video-to-Video) ו-C4 (פוסט-פרודקשן), עם הצלבה מול B1 (מפרטי מודלים) ומול פרק 00 (ניתוח הפריימים של הרילס, שהוא האמת על המקור).
> **שער:** כל הסכומים בשקלים חושבו מחדש לפי **1$ = 3.04 ₪** (open.er-api.com, 05.10.2026). חלק מהעובדים השתמשו ב-3.6 עד 3.7, ולכן המספרים כאן נמוכים בכ-18% מהמספרים בדוחות שלהם. מחירים שנקובים במקור בשקלים (חצובה, מיקרופון, מחיר ללקוח) נשארו כפי שהם.
> **Sora נסגר** (אפליקציה ב-26.04.2026, API ב-24.09.2026). הפניות ל-Sora בדוחות העובדים הוסרו או סומנו כלא רלוונטיות.
> מה שלא אומת מסומן **[לא מאומת]**. הפרומפטים בספרייה לא נבדקו בייצור בפועל, והם בנויים לפי הכללים שבפרק.

---

## תקציר

1. **האיכות כבר לא היתרון. הבימוי הוא היתרון.** הכלים (Seedance 2.5, Genjutsu) מוציאים תמונה קולנועית. מה שמבדיל רילס ויראלי מרילס בינוני הוא הרעיון (ניגוד חד), רשימת שוטים מתוזמנת, צילום קלט נכון, ופריסה של "קלט מול תוצאה" ב-0.5 השניות הראשונות. הפריסה הזו מופיעה ב-7 מתוך 10 רילסי המקור.
2. **הפייפליין בעשרה שלבים:** רעיון והוק ← רשימת שוטים מתוזמנת ← רפרנסים וצילום ← פרומפט (Claude מרחיב רשימה קצרה) ← ג'נרציה בטסטים של 480p ובקליפים קצרים ← Video-to-Video (אם יש צילום אמיתי) ← עריכה ופריסה ← כתוביות בעברית ← ייצוא ← QA. רילס של 30 עד 40 שניות לוקח 1 עד 4 שעות ועולה **כ-40 עד 300 ₪** ב-AI, כולל ניסיונות חוזרים.
3. **פרומפט הוא הוראת עבודה ולא תיאור.** Subject → Action → Scene/Light → Camera → Style → Audio → Constraints. פעלים ולא שמות תואר. **תנועת מצלמה אחת לכל שוט**. ציר timecodes רציף בלי חורים. **לכל רפרנס תפקיד אחד מפורש** (`@Image1 controls the face only`). ב-Seedance 2.5 כותבים בריף מובנה בסעיפים (GLOBAL STYLE, SCENE, CHARACTERS, TIMELINE, AUDIO, LOCKS).
4. **תמונה אחת מספיקה, אם היא "פספורט" טוב.** פנים קדמיות, רקע אפור חלק, אור רך, בלי פילטרים, לפחות 1024px (עדיף 2K+). כשהדמות מדברת בקלוז-אפ זמן רב, מוסיפים 3/4 ופרופיל, או עוברים ל-Video-to-Video עם צילום אמיתי. בפועל 3 עד 6 רפרנסים נקיים עדיפים על 20 בינוניים.
5. **הכלל החשוב ביותר (rourke):** לא מייצרים 30 שניות בבת אחת. חותכים לקטעים של 3 עד 8 שניות, מריצים טסט ב-480p (כ-4.6 ₪ ל-10 שניות ב-Higgsfield), משנים משתנה אחד בכל פעם, ורק את מה שעבד מרנדרים ב-1080p (כ-18 ₪ ל-10 שניות). מתקצבים פי 3 עד 5 ניסיונות.
6. **הפקה היברידית (V2V) היא הנישה הישראלית:** מצלמים בטלפון בחניון עם חבר, Genjutsu Motion Transfer בונה מחדש את העולם ושומר על התנועה ועל העברית. **את האודיו לוקחים תמיד מהטלפון** ולא מה-AI. ל"אינסוף זוויות" משתמשים ב-Seedance 2.5 Edit על טייק נעול ורחב. הקומבו: Genjutsu ואחר כך Seedance.
7. **עריכה:** תוצאה למעלה, מקור למטה (1080×960 כל חצי). Pattern interrupt כל 2 עד 4 שניות. 20 עד 35 שניות. כתוביות עבריות צרובות (Heebo Black / Rubik Bold) עם בדיקת bidi. גריין 15 עד 20% ו-LUT ב-50 עד 70%. ייצוא: 1080×1920, H.264 High, 12 עד 15 Mbps, AAC 192k/48kHz, ‏‎-14 LUFS. כל טקסט ולוגו מוסיפים בעריכה, אף פעם לא דרך המודל.

---

## 0. מפת הפייפליין (עמוד אחד)

| # | שלב | תוצר | כלי | זמן טיפוסי | עלות טיפוסית |
|---|---|---|---|---|---|
| 1 | רעיון והוק | משפט ניגוד אחד ("חניון ← מונטה קרלו") ופורמט | ראש, A2 | 10 דק' | 0 |
| 2 | רשימת שוטים | רשימה מתוזמנת, מחולקת לביטים של ≤30 שניות | פתק / Claude | 10 עד 20 דק' | 0 |
| 3 | רפרנסים וצילום | פספורט + 2 עד 5 זוויות, packshot, וידאו מקור 9:16 | טלפון, חצובה, Nano Banana Pro / Seedream | 15 עד 60 דק' | 0 עד 30 ₪ (תמונות AI) |
| 4 | פרומפט | בריף מובנה באנגלית | Claude עם meta-prompt | 5 עד 15 דק' | 0 |
| 5 | ג'נרציה | קליפים מאושרים ב-1080p | Seedance 2.5 (Higgsfield / Lovart / fal) | 30 עד 90 דק' | 40 עד 230 ₪ |
| 6 | V2V (אם יש צילום) | עולם חדש / זוויות חדשות | Genjutsu, Seedance Edit, Aleph 2.0 | 30 עד 90 דק' | 40 עד 300 ₪ |
| 7 | עריכה ופריסה | Split / Prompt Reveal / Wipe | CapCut, Premiere, ffmpeg | 30 עד 45 דק' | 0 עד 61 ₪ לחודש |
| 8 | כתוביות ועברית | כתוביות צרובות, bidi תקין | Whisper / Submagic / DaVinci | 10 עד 20 דק' | 0 |
| 9 | ייצוא | מאסטר אחד ל-IG, TikTok ו-Shorts | הגדרות בפרק 9 | 5 דק' | 0 |
| 10 | QA ופרסום | רשימת בדיקה מסומנת, תיוג AI, CTA + DM | פרק 10 | 10 דק' | 0 |

סדר הפייפליין הטכני בתוך שלבים 5 עד 9 (C4):
`ג'נרציה ← בחירת טייקים וחיתוך ראש/זנב ← תיקון ארטיפקטים (inpaint/regen) ← אפסקייל (אם צריך) ← אינטרפולציה לסלואו (אם צריך) ← עריכה וקצב ← צבע ← טקסט וכתוביות ← סאונד ← ייצוא ← QA`

---

## 1. רעיון והוק: בוחרים פורמט לפני שבוחרים כלי

### 1.1 שלוש שיטות העבודה שרואים ברילס (פרק 00)
| שיטה | מה נכנס | מה יוצא | דוגמה |
|---|---|---|---|
| **Image→Video, פרומפט רב-שוטי מתוזמן** | תמונת פנים אחת + פרומפט עם timecodes | פרסומת של 30 שניות עם 8 עד 9 שוטים | דובאי / למבורגיני (edbert_yienson) |
| **Video→Video "Genjutsu"** | צילום טלפון + עד כ-6 רפרנסים + שורת טקסט | אותה תנועה ואותו משחק בעולם אחר | מאור חני (רולס), Higgsfield רכבת תחתית |
| **"אינסוף זוויות" מטייק אחד** | טייק נעול + רשימת זוויות מתוזמנת שClaude מרחיב | קאברג' של צוות צילום מטלפון אחד | rourke (Lovart × Seedance 2.5), sidequestpat_ |

### 1.2 חמשת הפורמטים המרכזיים: מה לבחור
| פורמט | הוק | שיטה | זמן | עלות AI עם ניסיונות | קהל |
|---|---|---|---|---|---|
| **1. Reality-Swap בעברית** (מאור חני) | מסך מפוצל זול מול יוקרה + משפט "פייק עשיר" | Genjutsu Motion Transfer | כ-3 שעות | $40–100 (‏122–304 ₪) | קהל ישראלי, לקוחות |
| **2. מסטודיו ריק לעולם מלא** (Higgsfield רכבת/אסטרונאוט) | split רציף: חדר לבן מול רכבת מלאה דמויות | Genjutsu + 6 רפרנסים, 3 עולמות | 2 עד 3 שעות | כ-$50 (‏152 ₪) | B2B, מותגים |
| **3. Infinite Angles מטייק אחד** (rourke) | "This was shot on ONE camera" | Seedance 2.5 Edit | 2 עד 3 שעות | $30–60 (‏91–182 ₪) | יוצרים, עסקים |
| **4. קומבו Genjutsu ← Seedance** (sidequestpat_) | wipe סלון ← פנטהאוז ← "סט צילום" | שרשור שני כלים | 3 עד 4 שעות | $45–65 (‏137–198 ₪) | אנשי וידאו, דמו מכירה |
| **5. משפיען AI אבסורדי + Motion Transfer** | ראש חתול ספינקס בחליפה מבצע טרנד | AI Influencer / Kling Motion Control | שעה | $3–7 לסרטון (‏9–21 ₪) | ערוצים ללא פנים |
| **בונוס: Prompt Reveal** (דובאי) | INPUT (פספורט) + PROMPT גולל + תוצאה | Seedance 2.5 Image→Video | 1 עד 2 שעות | כ-$18 ב-Higgsfield ל-30 שניות 1080p, יותר עם ניסיונות | יוצרים שרוצים את הפרומפט |

### 1.3 כללי הוק (0 עד 2 שניות)
1. **לא פותחים בלוגו, אינטרו או "היי חברים".** הפריים הראשון הוא כבר השוט הכי מטורף, או רגע ה-wipe.
2. **ניגוד ויזואלי שמובן תוך 0.5 שניות:** זול מול יקר, ריק מול מלא, צעצוע מול עתידני (Higgsfield: נדנדת קפיץ ומאוורר ← אופנוע מעופף במדבר).
3. **טקסט הוק של 3 עד 7 מילים**, בתוך האזור הבטוח, **מהפריים הראשון** (לא מונפש פנימה לאט).
4. **תנועה בפריים הראשון.** אם השוט מתחיל סטטי, חותכים ממנו 5 עד 10 פריימים. Seedance נוטה "להתחמם" בתחילת קליפ.
5. **מילת ה-CTA כבר בהוק** ("STEAL MY PROMPT · COMMENT 'DUBAI'"), קבועה לאורך כל הסרטון ולא רק בסוף.
6. **אדם אמיתי בפריים.** Mosseri הודיע (31.12.2025) שב-2026 אינסטגרם תעדיף תוכן "raw, real, human" ([SocialPilot](https://www.socialpilot.co/de/blog/instagram-reels-algorithm)). פורמט היברידי עם צילום אמיתי במסך מפוצל עונה על זה.

---

## 2. רשימת שוטים מתוזמנת

### 2.1 מבנה כל שוט
לפי פרומפט דובאי ופרומפט rourke (פרק 00), כל שוט מוגדר בשבעה דברים:
`[time] Shot N: <subject+action> + <camera position/angle> + <lens> + <light> + <ONE camera move> + <how it ends> + <transition>`

**מצב סיום הוא הטריק של דובאי:** `exiting frame`, `pulling away down the straightaway`, `passes the camera a second time`. Kapwing ממליץ גם לקשור תנועה לפעולה ולא לטיימר: `pans only after the door opens` ([Kapwing](https://www.kapwing.com/resources/how-to-prompt-seedance-2-5-a-guide-for-ai-video-creators/)).

### 2.2 כללי תזמון
1. **ציר רציף:** 0–3, 3–7, 7–12. בלי חורים ובלי חפיפות. זמן שלא מוגדר, המודל ממלא כרצונו ([Runway](https://runway.com/resources/seedance-2-5-prompt-guide)). (בפרומפט דובאי יש חפיפה, `0:01-0:13` ואחריו `0:12-0:15`, וזה עבד, אבל עדיף להימנע.)
2. **אורך שוט:** 1.5 עד 3 שניות = קצב פרסומת. 4 עד 8 שניות = דרמה. Mindstudio: 2 עד 3 נקודות זמן לקליפ של 5 שניות, ו-3 עד 4 לקליפ של 10 שניות ([Mindstudio](https://www.mindstudio.ai/blog/timeline-prompting-seedance-2-cinematic-ai-video)).
3. **2 עד 3 משפטים לכל ביט.** "Precision matters more than length".
4. **מיקום אחד לכל שוט.** שלושה מיקומים בקליפ של 5 שניות = מריחה ומורפינג.
5. **ביטים של ≤30 שניות.** זו מגבלת הקלט של Genjutsu ומגבלת הפלט של Seedance 2.5. רילס של 40 עד 60 שניות = 2 עד 6 ג'נרציות שמחברים בעריכה.
6. **טריק בימוי מדובאי:** פחות זמן מסך לפנים = פחות דריפט. בדובאי הפנים ברורות רק ב-2 עד 3 שוטים (cockpit, דרך שמשה). השאר רכב ומצלמה.
7. **אזהרה:** Seedance מצהיר ש-"timestamps allocate time to events. They are not frame-accurate" ([Morphic](https://morphic.com/resources/how-to/seedance-2-5-guide)). את הסנכרון המדויק עושים בעריכה.

### 2.3 שלושה פורמטים של timecode (כולם עובדים ב-Seedance)
```
A) Dubai style:         0:01-0:13  Descent from the spire tip ...
B) Rourke/Claude style: [00:00-02.37] Shot 1: ... Hard cut to Shot 2.
C) Plain seconds:       0s to 8s: steadicam follow ... 8s to 18s: whip pan ...
```
- Veo 3.1: `[00:00-00:02] ...` ([Google Cloud](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)).
- Kling 3.0: `Shot 1 (0-5 seconds): ...`, עד **6 שוטים** ו-15 שניות ([Atlabs](https://www.atlabs.ai/blog/kling-3-0-prompting-guide-master-ai-video-generation)).

### 2.4 תבנית תכנון לפורמט V2V (דוגמת מאור חני)
| ביט | אורך | פעולה | מקור | יעד |
|---|---|---|---|---|
| A: ההגעה | ~15 שניות | יציאה מהכניסה, החבר פותח דלת אחורית, "זורק טיפ", "thank you mr hani" | כניסה לחניון + רכב קטן | לובי Hotel de Paris + Rolls-Royce Phantom + שוער במדים |
| B: הווידוי | ~20 שניות | מדבר למצלמה בעברית מהמושב האחורי | רכב רגיל, טלפון על המושב הקדמי | פנים רולס: עור לבן, Starlight Headliner |

---

## 3. רפרנסים: מה לצלם ומה להביא

### 3.1 שלושה סוגי קלט, שלוש משימות
רוב הכישלונות נובעים מבלבול ביניהם (C2):

| קלט | מה נשמר | מה המודל ממציא | מתי |
|---|---|---|---|
| **Start frame** (`image_url` / `frameImages`) | הפריים הראשון כמעט פיקסל-לפיקסל, כולל טקסט | את התנועה ומה שנכנס לפריים | שוט hero של מוצר, פתיחה שחייבת להיראות בדיוק כך |
| **End frame** (`end_image_url`) | הפריים האחרון | את הדרך מ-A ל-B | טרנספורמציה, "נחיתה" על packshot |
| **Identity ref** (`@Image1`) | פנים, שיער, מבנה גוף | קומפוזיציה, זווית, רקע, תאורה | כל סרטון עם "אני" או דמות |
| **Wardrobe ref** | בגד או אביזר | איך הבגד יושב בתנועה | כשהבגד בתמונת הפנים לא נכון |
| **Product ref** | צורה, חומר, תווית | תאורה וזווית | פרסומת מוצר, placement |
| **Location ref** | אדריכלות ואווירה | מיקום המצלמה | מקום שחייב להיות מזוהה |
| **Style ref** | פלטה, ניגודיות, גריין | תוכן | מראה עקבי לסדרה |
| **Original video** (Genjutsu / `@Video1`) | תנועה, תזמון, מצלמה, משחק, תנועת שפתיים | עולם, לבוש, דמויות | הפקה היברידית |

מקורות: [fal](https://fal.ai/models/bytedance/seedance-2.5/image-to-video), [Runware](https://runware.ai/docs/models/bytedance-seedance-2-5/guides/multi-reference-production), [MindStudio](https://www.mindstudio.ai/blog/seedance-2-5-multimodal-reference-system-explained).
**הבחנת Runware:** `frameImages` מצמיד את הסטיל כפריים הפתיחה, ואילו `referenceImages` מאפשר "אותו אדם בשוט אחר".

### 3.2 מגבלות טכניות
| פרמטר | Seedance 2.5 | Genjutsu | מקור |
|---|---|---|---|
| רפרנסים מקסימום | 30 תמונות + 10 וידאו + 10 אודיו (50) | **סתירה:** 6 משבצות בממשק שברילס, "עד 30" בדף הרשמי, "עד 40" בצד שלישי | [Runware](https://runware.ai/docs/models/bytedance-seedance-2-5/guides/multi-reference-production), [Higgsfield](https://higgsfield.ai/genjutsu), [CreativeAINews](https://www.creativeainews.com/blog/higgsfield-genjutsu-ai-video-motion-transfer-2026/) |
| מספר יציב בפועל | 1 עד 8 תמונות; 9 עד 12 "עובד, פחות יציב" | 3 עד 6 | Runware, C2/C3 |
| פורמט ומידות תמונה | jpeg/png/webp/bmp/tiff/gif; ‏300–6000px לצלע; יחס 0.4–2.5; עד 30MB | — | [Evolink](https://docs.evolink.ai/cn/api-manual/video-series/seedance2.5/seedance-2.5-image-to-video.md) |
| וידאו קלט | MP4/MOV, ‏1.8–30.2 שניות לרפרנס, 30 שניות במצטבר, ≤200MB, ‏24–60fps | 4 עד 30 שניות (צד שלישי: 3–30), קובץ בלבד (לא קישור) | [fal](https://fal.ai/learn/tools/how-to-create-multi-angle-video-seedance-2-5), [riffkit](https://riffkit.ai/blog/how-to-use-higgsfield-genjutsu) |
| פלט | 4–30 שניות, 24fps קבוע, ‏480/720/1080p (1080p אומת ב-Higgsfield וב-fal; חלק מהספקים מציעים רק 480/720p; "early access" ב-Higgsfield [לא מאומת: דף Higgsfield לא מציין זאת]) | עד 1080p | B1, [fal](https://fal.ai/models/bytedance/seedance-2.5/image-to-video), [Higgsfield](https://higgsfield.ai/blog/higgsfield-genjutsu) |
| יחסי מסך | 21:9, 16:9, 4:3, 1:1, 3:4, 9:16 | כמו המקור | fal |
| Seedance 2.0 להשוואה | 12 רפרנסים (9/3/3), עד 15 שניות, עד 4K | — | Dreamina FAQ, B1 |

**יישוב 6 מול 30 ב-Genjutsu:** כנראה הממשק מציג 6 משבצות בתצוגה הראשונית, או שהמגבלה הורחבה אחרי הדמו [לא מאומת]. ההמלצה לא משתנה: **3 עד 6 רפרנסים, כל אחד עם תפקיד**. "Three excellent character angles are more useful than twelve mediocre ones" ([MindStudio](https://www.mindstudio.ai/blog/seedance-2-5-multimodal-reference-system-explained)).

### 3.3 מה היה ב-INPUT של דובאי
תמונה אחת: ראש וכתפיים, פנים כמעט קדמיות, **רקע אפור סטודיו חלק**, **ז'קט שחור**, אור רך ואחיד, בלי משקפיים וכובע. היתרונות: אין רקע שמתחרה, הבגד כבר מתאים לסצנה, ואור ניטרלי שמאפשר להאיר מחדש לשמש מדברית. הפרומפט לא מתאר את הפנים בכלל. **הזהות מגיעה 100% מהתמונה.**
**לקח:** אל תיבנו על תמונה אחת כשהדמות מדברת 30 שניות בקלוז-אפ. שם מוסיפים פרופיל ו-3/4, או עוברים ל-Genjutsu עם וידאו שלכם.

### 3.4 "Self Reference Kit": מפרט צילום (לעצמכם או ללקוח)
| פרמטר | מה לעשות | למה |
|---|---|---|
| מצלמה | אחורית (לא סלפי), 1x או 2x (שקול ל-50–85 מ"מ) | עדשת סלפי מעוותת אף ופנים, והמודל משכפל |
| מרחק | 1.5 עד 2 מטר עם 2x | פרופורציות טבעיות |
| רזולוציה | לפחות 1024px בצלע הקצרה ([Runway](https://runway.com/resources/ai-character-references-tips)), מומלץ 2K–4K. JPEG מקורי, לא צילום מסך מ-WhatsApp | דחיסה מוחקת פרטי עור |
| תאורה | אור חלון רך מקדימה או יום מעונן. בלי שמש ישירה, אור תקרה או פלאש | צללים "נצרבים" בזהות |
| רקע | קיר חלק אפור/לבן/בז', מטר מהקיר | רקע עמוס דולף לסצנה |
| הבעה | ניטרלית, פה סגור או חיוך קל (+ תמונה עם חיוך אם הסרטון "שמח") | הבעה קיצונית הופכת לברירת מחדל |
| פנים ושיער | שיער מחוץ לפנים, בלי משקפי שמש וכובע | כל הסתרה = דריפט |
| בגדים | בגד היעד, או חלק כהה בלי לוגו והדפס | הדפסים "רוקדים" |
| פילטרים | אפס: בלי Beauty, Portrait blur או פילטר | המודל לומד עור "פלסטיק" |
| אנשים נוספים | רק אתם | מונע ערבוב זהויות |

**סט הזוויות (8 תמונות, 5 דקות):**
| # | תמונה | שימוש | חובה? |
|---|---|---|---|
| 1 | פנים קדמי ("פספורט") | הזהות הקנונית, תמיד `@Image1` | ✅ חובה |
| 2 | 3/4 שמאל (45°) | שוטים מהצד, נהיגה | ✅ מומלץ מאוד |
| 3 | 3/4 ימין | כנ"ל | אופציונלי |
| 4 | פרופיל מלא (90°) | cockpit, הליכה מהצד | מומלץ |
| 5 | גוף מלא קדמי, ידיים לצדדים | פרופורציות, בגדים | ✅ מומלץ מאוד |
| 6 | גוף מלא מאחור | הליכה מהמצלמה | אופציונלי |
| 7 | חצי גוף, חיוך עם שיניים | סצנות שמחות ודיבור | אופציונלי |
| 8 | קלוז-אפ ידיים / אביזר | אם האביזר חשוב | לפי הצורך |

**כלל זהב:** הכל באותו יום, באותה תאורה, באותם בגדים ובאותה תספורת ([CapCut](https://capcut.com/create/character-consistency-ai-video-clips-reference-images), [MagicHour](https://magichour.ai/blog/how-to-keep-characters-consistent-in-ai-video)).

**טוב מול רע:**
| ✅ טוב | ❌ רע | מה יקרה |
|---|---|---|
| פספורט על קיר אפור, אור חלון, 3000px | סלפי ברכב, עדשה רחבה, שמש מהצד | אף מוגדל; חצי פנים בצל = "פנים אחרות" |
| אתם לבד | תמונה קבוצתית חתוכה | ערבוב תווי פנים, רזולוציה נמוכה |
| טישרט חלקה כהה | לוגו ענק או משבצות | ההדפס משתנה בכל פריים |
| הבעה ניטרלית | צחוק פרוע, עיניים עצומות | ההבעה נדבקת לכל השוטים |
| 3 תמונות מאותו יום | תמונה מלפני 5 שנים + תמונה עם זקן | "cousin effect", ממוצע של שני אנשים |
| JPEG מקורי | צילום מסך מסטורי | ארטיפקטים, עור "שעווה" |
| בלי משקפיים (או עם, אם תמיד) | משקפי שמש | עיניים מומצאות |
| גובה עיניים | מלמטה/מלמעלה | Runway: "Extreme angles" = חוסר עקביות |

### 3.5 טקסט מוכן ללקוח (לשלוח ב-WhatsApp)
> "כדי להכין את הסרטון אני צריך: (1) 3 תמונות שלך מהיום, באור יום מול חלון, על קיר חלק: פנים מקדימה, פנים בזווית חצי צד, וגוף מלא. בגדים כמו שתרצה להופיע בסרטון. בלי פילטרים, לשלוח כ'קובץ' ולא כ'תמונה' ב-WhatsApp. (2) קובץ לוגו מקורי (PNG/SVG). (3) 3 עד 5 תמונות מוצר על רקע לבן/אחיד, כולל צילום חזיתי שהתווית קריאה בו."

**משפטית:** אישור כתוב לשימוש בדמות (likeness) ובמוצר. Higgsfield ו-media.io: "footage and references you own or have permission to edit" ([media.io](https://www.media.io/video-effects/higgsfield-ai-genjutsu-tutorial.html)). חלק מהפלטפורמות חוסמות פנים מזוהות כרפרנס; edbert עבד עם פספורט, אז זה אפשרי לפחות בחלקן. אם יש חסימה, character sheet שנוצר ב-AI [לא מאומת: המדיניות משתנה].

### 3.6 Packshot של מוצר
- רקע לבן/אפור חלק (בריסטול, או light-box ב-60 עד 100 ₪ מ-AliExpress [מחיר משוער]).
- 2K–4K, חדות מלאה על התווית (לפחות 1024×1024, [Opus](https://www.opus.pro/blog/product-photo-to-commercial-seedance)).
- 3 עד 5 זוויות: חזית (תווית ישרה) · **3/4 (הכי חשוב לסיבוב מצלמה)** · צד · למעלה · גב.
- בלי השתקפויות שורפות. מפזר על זכוכית/מתכת. אפשר להסיר רקע (Photoroom / Adobe / Canva).
- **רפרנס אחד = נושא אחד.** לא לשים רכב ונהג באותה תמונה. רקע ניטרלי לאובייקטים ודמויות; רפרנס לוקיישן הוא היוצא מן הכלל.
- **זווית ותאורה ברפרנס ≈ זווית ותאורה בסצנה** ("from a similar angle and lighting condition", Higgsfield/[Stork](https://www.stork.ai/en/higgsfield-genjutsu)).

### 3.7 כשאין צילום טוב: keyframes במודל תמונה (זול ומהיר)
Runway: "Generate a clean AI reference image first". Runware: "Iterate hero stills in image models first, then animate". סטילס = סנטים ושניות; וידאו = דולרים ודקות. כלים: Nano Banana Pro / Seedream / Soul (ב-Higgsfield וב-Lovart) [זמינות לפי חבילה: לא מאומת]. **מבחן חבר:** אם חבר לא אומר מיד "זה אתה", לא ממשיכים.

**שלב א': Anchor portrait (ניקוי תמונה קיימת)**
```
Using the person in the uploaded photo, create a clean studio identity reference.
Keep the exact face, facial proportions, skin texture, moles, hairline and hairstyle
— do not beautify or change age. Head-and-shoulders, facing the camera, neutral
expression, mouth closed. Plain medium-gray seamless studio background. Soft, even
front lighting from a large softbox, no harsh shadows. 85mm lens look, eye level,
sharp focus on eyes, natural skin pores visible. Wearing a plain black crew-neck
t-shirt. Photorealistic, 4K, no text, no watermark.
```

**שלב ב': Character sheet / Turnaround** ([invideo](https://invideo.io/faq/how-do-you-create-a-character-reference-sheet-using-nano/), [SelfieLab](https://selfielabstudio.com/blog/nano-banana-pro-master-character-consistency-prompts-20260302)). 4 וריאציות, בוחרים אחת:
```
Create a professional character reference sheet based strictly on the uploaded
reference photo. Same person, same face, same hairstyle, same outfit: black tailored
suit, white shirt, no tie, gold watch on left wrist.
Layout on a clean light-gray background, consistent soft studio lighting across all panels:
Top row — four full-body standing views side by side: front view, left profile,
right profile, back view. Neutral standing pose, arms relaxed.
Bottom row — three detailed close-up portraits: front, left 3/4, right profile.
No props in hands. Photorealistic, 4K, no text labels, no captions, no watermark.
```
- **"no text labels"**: טקסט כמו "FRONT" "נקרא כתוכן" ועלול להופיע בסרטון (Runware). שם הדמות רק בפרומפט.
- בכלים מרובי רפרנסים עדיף **לחתוך את הגיליון ל-2 עד 3 תמונות** (פנים, 3/4, גוף מלא), כל אחת עם תפקיד [המלצה מבוססת היגיון, לא בדיקה מבוקרת].
- החלפת בגדים באמצע סיפור: גיליון חדש באותה פריסה ("beat-specific sheets"). נעילת דמות שלמה: כ-$10 (‏30 ₪), לפי invideo.

**שלב ג': Start frame לכל שוט חשוב, ישר ב-9:16**
```
[Image 1 = identity reference] Vertical 9:16 frame. The man from Image 1 — same face,
same black suit — stands beside a yellow Lamborghini Revuelto on Sheikh Zayed Road
at golden hour, Burj Khalifa in the background top of frame. Low angle, 24mm lens,
car fills the lower third, man in the right third, looking at camera with a slight
smile. Warm backlight, light haze, cinematic color grade, photorealistic. Leave
headroom at the top and clear space at the bottom for captions. No text, no logos added.
```
```
[Image 1 = product packshot] Vertical 9:16 hero frame. The exact bottle from Image 1 —
same shape, cap, label layout and colors, label facing camera and fully legible — on a
wet black stone surface, single hard rim light from behind, soft fill from front,
water droplets on the glass, dark moody background, 100mm macro look. Product centered
in the middle third. Do not alter or re-letter the label.
```
```
[Image 1 = me, Image 2 = location photo] Vertical 9:16. The person from Image 1 sits
at an outdoor café table in the exact location from Image 2 (keep the architecture,
signage shapes and street layout), morning light, espresso cup on table, medium shot
from eye level, 35mm, natural candid moment, photorealistic, shallow depth of field.
```
**Start + End frame לטרנספורמציה:**
- Start: `Vertical 9:16, my empty white living room from the uploaded photo, flat daylight, phone-camera realism.`
- End: `Same room, same camera position and lens, transformed into a sea-view penthouse: beige linen sofa, marble floor, floor-to-ceiling windows with Mediterranean view, warm sunset light.`
- Kapwing: "change too much at once and the model has to invent the middle". מקבעים מצלמה ומשנים רק את העולם.

### 3.8 9:16 ואזורים בטוחים בשלב הרפרנס
- Start frames ווידאו מקור **חייבים** להיות 9:16. רפרנסי זהות ומוצר לא חייבים (הם לזהות, לא לקומפוזיציה).
- נושא בשליש האמצעי. כ-15% עליונים ו-20% עד 25% תחתונים מכוסים בממשק ובכתוביות. בפרומפט: `leave headroom at top and clear space at bottom for captions`.
- במסך מפוצל כל חצי הוא בערך 9:8. מייצרים ב-9:16 וחותכים בעריכה, או מבקשים קומפוזיציה ממורכזת [טכניקה מעשית, לא מאומתת מול היוצרים].

### 3.9 צילום וידאו מקור ל-V2V: צ'קליסט שטח
המודל **מעתיק את מה שהוא רואה**: רעידות, צל קשה ויד על הפנים יעברו לתוצאה, ולפעמים יוגדלו.

| ✅ | כלל | איך בפועל |
|---|---|---|
| ☐ | **9:16 אנכי מראש**, 4K/30 או 1080p/30. הפלט שומר את יחס הקלט | לפני העלאה מכווצים ל-1080p (HandBrake/CapCut) כדי לעמוד ב-200MB |
| ☐ | **חצובה, או תנועה איטית וחלקה** (ג'ימבל), בלי זום דיגיטלי | חצובה עם תפסנית: 50–100 ₪ |
| ☐ | **ל"אינסוף זוויות": שוט רחב ונעול**, הכל בפריים, אביזרים "within arm's reach" | fal: "single, locked-off tripod shot" |
| ☐ | **טייקים של 8 עד 15 שניות** לכל ביט, 3 עד 5 טייקים | הגבלה של 30 שניות, איכות יורדת בארוך |
| ☐ | **אור רך ואחיד**; כיוון האור תואם ליעד; בלי backlight שהופך לצללית | חניון תת-קרקעי = אור עילי אחיד, נוח להחלפה |
| ☐ | **בלי פליקר:** Pro mode, shutter 1/50 (רשת 50Hz בישראל) | פלורסנט בחניונים מהבהב |
| ☐ | **HDR כבוי** | HLG עולה לאינסטגרם "שרוף" |
| ☐ | **תנועות גדולות וברורות:** פתיחת דלת, הושטת שטרות, הליכה לעבר המצלמה | מזוהות גם מרחוק |
| ☐ | **פרוקסי בגודל ובמיקום דומים ליעד**: רכב קטן ← רולס עובד; אופניים ← רולס פחות; בקבוק ריק במקום בושם | בלי אובייקט, ידיים "פותחות דלת באוויר" ונשברות |
| ☐ | **מגע פשוט:** חפץ אחד, בלי העברה בין ידיים, ידיים רחוק מהפנים | ידיים במגע = נקודת התורפה |
| ☐ | **פנים גלויות ופה גלוי בזמן דיבור**, בלי מיקרופון מול השפתיים | שימור הסינכרון |
| ☐ | **אודיו נקי:** מיקרופון דש אלחוטי (100–250 ₪) | **הפסקול המקורי הוא מה שישמור על העברית** |
| ☐ | **בלי טקסט, לוגואים ושלטים בולטים** בפריים | יידלפו או יתעוותו |
| ☐ | **"שחקן נגדי"** (חבר כנהג/שוער) וגם לו רפרנס | גם הוא מוחלף |
| ☐ | **רקע פשוט** (קיר, חניון, חדר ריק). **לא צריך גרין-סקרין** | Higgsfield: "doesn't require a green screen, heavy CGI, or weeks in post-production" |
| ☐ | אופציונלי: **Clean plate**, 5 שניות של המקום ריק מאותה זווית | ל-VACE ולקומפוזיטינג ידני; לא נדרש ב-Genjutsu |
| ☐ | ל-60fps אם יש תנועה מהירה (ואז מבקשים slow motion במקום מהירות) | תנועה מהירה "נמרחת" |

---

## 4. כתיבת הפרומפט

### 4.1 אנטומיה: 9 רכיבים + מגבלות
| # | רכיב | מה לכתוב | טוב | גרוע |
|---|---|---|---|---|
| 1 | **Subject** | מי/מה + 1–2 מאפיינים מוחשיים | `a man in his 30s, black tailored suit, silver watch` | `a handsome man` |
| 2 | **Action** | שרשרת פעלים עם השלכות פיזיות | `pushes the door open, pauses, adjusts his cufflinks` | `walking cinematically` |
| 3 | **Setting** | מקום + פרט סביבתי אחד | `rain-wet Tel Aviv boulevard, neon reflections on asphalt` | `a beautiful city` |
| 4 | **Camera** | גודל, זווית, **תנועה אחת** + מצב סיום | `low angle, slow push-in ending in medium close-up` | `epic camera movement` |
| 5 | **Lens** | אורך מוקד ועומק שדה | `85mm, shallow depth of field, creamy bokeh` | `cinematic lens` |
| 6 | **Lighting** | **מקור** וכיוון | `hard late-afternoon sun from camera left, warm rim light` | `dramatic lighting` |
| 7 | **Style** | גריד, פילם/דיגיטל, ז'אנר | `teal-and-orange grade, 35mm film grain, commercial look` | `cinematic, 8K, masterpiece` |
| 8 | **Motion/Physics** | קצב, סלואו, משקל, בד ושיער | `real-time 24fps, hair and fabric lag behind motion` | (חסר) |
| 9 | **Audio** | דיאלוג, SFX, אווירה, מוזיקה, **או "no music"** | `Audio: V12 engine roar, tire hiss, no music` | (חסר ← מוזיקה תזמורתית אקראית) |
| + | **Constraints** | שורת "לא" קצרה + נעילות | `No text on screen. Face identical across all shots.` | 40 מילות "no" |

- **סדר בתוך שוט** (מדריך Seedance): תנועת מצלמה/מעבר ← פעולת הנושא והבעה ← שינוי מיקום ← אודיו ([heyuan110](https://www.heyuan110.com/posts/ai/2026-07-11-seedance-2-prompt-guide/)).
- **אורך:** קליפ בודד של 5–10 שניות = 60–100 מילים, החשוב בהתחלה (ההיענות יורדת לקראת הסוף). Veo: ‏100–150 ([Frameo](https://frameo.ai/blog/google-veo-3-prompt-guide-best-practices/)). Seedance 2.5 רב-שוטי של 15–30 שניות = 250–600 מילים בסעיפים.
- **Verbs > Adjectives:** "The model understands physics, not adjectives" ([Runway](https://runway.com/resources/seedance-2-0-prompt-guide)).
  - ❌ `A beautiful woman walking down a city street at night, cinematic, stunning, epic camera movement, high quality, 8K`
  - ✅ `A woman in her 30s, dark hair, charcoal wool coat, walks past rain-wet storefronts, stops, and exhales visibly in the cold air. Night street after rain, neon reflections on the asphalt. Camera: slow push-in from 45° angle, ending in medium close-up. Audio: light rain, distant traffic, muffled jazz from inside a shop, no music.`

### 4.2 שלוש רמות של מבנה

**רמה 1: חמישה חריצים (קליפ קצר, כל מודל)**
```
[SUBJECT]     who/what + 1-2 concrete attributes
[ACTION]      one verb chain with physical consequences
[SCENE]       place + light (one sentence)
[CAMERA]      exactly ONE primary move, optionally with end state
[STYLE/AUDIO] visual treatment + named sounds ("no music" if unwanted)
```

**רמה 2: הבריף המובנה של Higgsfield ל-Seedance 2.5 (עד 30 שניות)**. בלוק טקסט רציף בסעיפים עם כותרות. כל סעיף שמדלגים עליו = כשל צפוי ([Higgsfield](https://higgsfield.ai/blog/seedance-2-5-prompting-guide)):
| סעיף | תוכן | אם מדלגים |
|---|---|---|
| `GLOBAL STYLE` | ז'אנר, גריד, פילם/דיגיטל, יחס, shutter, מה **אסור** | הסגנון נודד |
| `SCENE` | לוגליין ומצב רוח | אין עוגן |
| `CHARACTERS` | תיאור פיזי + @Image | פנים משתנות |
| `LOCATION` | מרחב ואביזרים, בנפרד מאנשים | המיקום זוחל |
| `FIRST FRAME AND BLOCKING` | עמדות פתיחה, כולל קואורדינטות (`x 42%, y 44%`) | דמויות מתחלפות |
| `SHOT-BY-SHOT BREAKDOWN` | Shot 1, Shot 2... | המודל ממציא קצב |
| `OPTICS` | אורך מוקד לשוט, גובה מצלמה, תנועה | העדשה נודדת |
| `PHYSICS` | בד, עשן, שיער, נוזלים, משקל, מגע קרקע | תנועה מרחפת |
| `LIGHTING` | מקור, כיוון, נפילה | שטוח/לא עקבי |
| `AUDIO` | אווירה, SFX, ומה לא (`no music, no dialogue`) | מוזיקה אקראית |

נעילות שחוזרות אצל Higgsfield: `Face lock: photoreal natural skin, identical features, zero drift` · `MEMBER COUNT LOCK: exactly four, no duplicates` · `same screen direction, never flip` · `accumulating dirt that never resets`.

**רמה 3: בריף Runway עם רפרנסים** ([Runway](https://runway.com/resources/seedance-2-5-prompt-guide)): (1) Asset-binding list (`@Image 1: the woman (subject). @Image 2: the car (subject). @Video 1: camera movement reference (motion).`) ← (2) סיכום במשפט ← (3) Timeline בשניות שלמות, רציף ← (4) Consistency notes. Kapwing: `Format → Subject + Action → Reference Roles → Timeline → Camera → Continuity → Audio → Constraints`, וסוגרים בשורת negative קצרה ([Kapwing](https://www.kapwing.com/resources/how-to-prompt-seedance-2-5-a-guide-for-ai-video-creators/)).

### 4.3 אוצר מילים של מצלמה (להעתקה)
**גודל שוט:** `extreme wide / establishing` (פתיחה, נדל"ן) · `wide shot` (גוף מלא) · `medium shot` (דיבור) · `medium close-up` (וולוג, UGC) · `close-up` (פנים/מוצר) · `extreme close-up / macro` (עין, טיפה, שעון) · `insert shot` (כפתור, לוגו) · `two-shot / over-the-shoulder` (דיאלוג).
**זווית:** `eye level` · `low angle / hero angle` (כוח, יוקרה) · `high angle` · `top-down / bird's-eye` (אוכל, מוצר) · `dutch angle` · `worm's-eye` · `POV` · `3/4 angle` (רכבים) · `profile / lateral` · `nose-on / front-on`.

**תנועה (אחת לכל שוט):**
| מונח | שימוש |
|---|---|
| `locked-off / static` | סיום, מוצר |
| `slow push-in / dolly in` | רגש, חשיפה |
| `pull-out / dolly out` | חשיפת הקשר |
| `tracking shot / follow` | הליכה, רכב |
| `lateral tracking / trucking` | רכב בפרופיל |
| `orbit / arc shot (180°/360°)` | מוצר, אופנה |
| `crane up / crane down / jib` | פתיחה וסיום |
| `aerial / drone flyover / FPV drone dive` | נדל"ן, דובאי |
| `whip pan` | מעבר אנרגטי |
| `crash zoom / snap zoom` | קומדיה, הוק |
| `dolly zoom (Vertigo)` | "וואו" |
| `handheld / shoulder-cam drift` | UGC, דוקו |
| `gimbal / steadicam` | ליווי |
| `rack focus` | חשיפה, מוצר |
| `parallax` | נדל"ן, טבע |
| `bullet time / speed ramp` | ספורט, "לימון באוויר" |

**עדשות:** `14–24mm wide` · `35mm` · `50mm standard prime` · `85mm portrait` · `100mm macro` · `anamorphic 2.39:1, oval bokeh, horizontal flare` · `shallow depth of field f/1.8` · `deep focus` · `tilt-shift` · `fisheye`.
**תאורה (תמיד מקור וכיוון):** `golden hour` · `blue hour` · `harsh midday sun` · `overcast soft light` · `practical lights (lamps, neon)` · `window light from camera left` · `rim light / backlight` · `Rembrandt lighting` · `softbox key + negative fill` · `volumetric light through haze` · `candlelight / firelight` · `flickering fluorescent`.
**מעברים בתוך פרומפט:** `Hard cut to Shot 2` · `match cut on the spinning wheel` · `whip-pan transition` · `cut on the beat` · `smash cut` · `J-cut (audio leads)` · `continuous one-take, no cuts`.

### 4.4 תחביר רפרנסים ו-binding
| מודל | רפרנסים | תחביר |
|---|---|---|
| Seedance 2.0 | עד 12: ‏9/3/3 | `@image1`, `@video1`, `@audio1` |
| **Seedance 2.5** | עד 50: ‏30 תמונות (4K), 10 וידאו (30 שניות במצטבר), 10 אודיו | `@Image 1` / `@Video1` (לפי הממשק) |
| Kling 3.0 | Elements (דמות/אובייקט כולל קול) | `@Element1` |
| Veo 3.1 | Ingredients (עד 3 תמונות, לפי [Google AI docs](https://ai.google.dev/gemini-api/docs/veo); עם רפרנסים רק קליפ של 8 שניות), First & Last frame | תיאור טקסטואלי |
| Gemini Omni Flash 1.1 | 1–10 תמונות, first+last frame; video ref: **סתירה** (Segmind: הוסר ב-1.1; Runware/aicybr: עד 3 קליפים) [לא מאומת] | תיוג בפרומפט |
| Higgsfield Genjutsu | וידאו מקור + 3–6 (מקס' 30, ראו 3.2) + שורת טקסט | משפט אחד או CHANGE/PRESERVE |

> משתמשים בדיוק בטוקן שהממשק מכניס בלחיצה על הנכס. Higgsfield כותב `@Image 1` עם רווח, Lovart כותב `@Video1`. ייתכן ששתיהן עובדות [לא מאומת].

**כללי הזהב (C1 + C2):**
1. **תפקיד אחד לכל רפרנס, ומה הוא לא משפיע:** `@Image1 controls the face only — do not take its lighting, background or clothing`. רפרנס "עירום" מדליף תאורה, מסגור וקצב.
2. **לא לתאר מחדש מה שהרפרנס מראה.** `Refer to the camera movement and motion in @Video 1`. טקסט = סמנטיקה, רפרנס = מראה ותנועה. (חריג: תיאור קצר כעוגן לדריפט, `the yellow Lamborghini Revuelto in @Image3`.)
3. **שמות תפקידים:** `The driver references @Image1.` ובהמשך רק `the driver`. בלי זה רפרנסים דומים "מתמצעים".
4. **הפנים הראשיות תמיד ב-`@Image1`**; אינדקסים נמוכים מחזיקים זהות טוב יותר.
5. **לא להפנות למשבצת ריקה.** `@Image4` בלי תמונה נזרק בשקט. משנים סדר ← מעדכנים כל הפניה.
6. **מתחילים בקטן:** מוצר/דמות אחד, רמז סגנון אחד, כיוון תנועה אחד. מוסיפים רק אם טסט מוכיח שיפור.
7. **עוצמת רפרנס (אם יש סליידר): 70–80%.** ב-90–100% "קרטון גזור", מתחת ל-60% הזהות נודדת.
8. **סעיף שימור בסוף:** `Preserve the exact face, hair, and wardrobe of each subject from their reference.`

**תבניות binding להעתקה:**
```
@Image1 = character identity (face, hair, skin tone) — hold across all shots.
@Image2 = wardrobe only (black suit, white shirt).
@Image3 = product (bottle shape, label, cap) — must match exactly, label legible.
@Video1 = camera movement and pacing only — do not copy its location or people.
@Audio1 = background rhythm; cut on the beat.
```
```
Preserve the composition, camera position, lighting, and performance rhythm of @Video 1. Only modify the subject's expression.
```
```
Keep the location, dialogue, and actions identical to @Video1. Only change camera position, lens and framing per shot.
```
**נאמנות מוצר בפרומפט:**
```
The hero product is the glass serum bottle with gold cap in @Image1 (front label) and
@Image2 (3/4 view). Preserve the bottle's exact proportions, cap, label layout, colors
and position. Keep the label facing camera in the final 2 seconds. Do not invent,
translate or re-letter any text.
```

### 4.5 אודיו, דיאלוג ועברית
| מודל | תחביר |
|---|---|
| Veo 3.1 | דיאלוג במירכאות אחרי שם הדובר; `SFX: thunder cracks in the distance`; `Ambient noise: ...`; כל רכיב במשפט נפרד |
| Seedance 2.5 | `Dialogue (character): "text"`; שכבות Dialogue → SFX → Ambience → Music |
| Kling 3.0 | `[Character A, tone]: "words"`; `Immediately`, `Then`; `SFX: ...` |

- שקט = לכתוב `no music`. אחרת ניקוד תזמורתי אקראי.
- כ-2.5 מילים לשנייה: קליפ של 8 שניות ≈ 20 מילים לכל היותר.
- **עברית (הכרעת החטיבה):** אין עדות שמודל כלשהו מייצר דיבור עברי טבעי ברמת פרסומת (B1) [לא מאומת לכל מודל]. לכן **דיבור עברי = מצלמים דיבור אמיתי ומעבירים ב-V2V**, ומשתמשים בפסקול המקורי. אפשר לנסות שורת דיאלוג בעברית במירכאות בתוך פרומפט אנגלי (כמו פרומפט 7 בנספח), אבל זה ניסוי, לא שיטת עבודה. מדריך Seedance ממליץ **לא לערבב שפות כשרוצים טקסט על המסך**, ולכן כל כתובית עברית נוספת בעריכה.
- טקסט על המסך (אם בכל זאת): `text 'SALE 50%' appears center of frame`, מילים נפוצות, בלי סימנים מיוחדים. ברירת המחדל שלנו: `no on-screen text`.

### 4.6 Negative cues
- ל-Seedance ול-Veo אין שדה negative בכל ממשק: שורה אחרונה, 3–6 פריטים, ממוקדת בכשלים שבאמת רואים.
- Google: ניסוח חיובי וספציפי (`a desolate landscape with no buildings or roads` עדיף על `no man-made structures`).
- Kling (יש שדה): 3–5 פריטים, למשל `no sliding feet, no distorted hands, stabilized camera, no text glitches on signs`.
- **Positive locks עדיף על "no":** `Face identical in every shot. Exactly two people. Same screen direction. Wardrobe unchanged.`
```
Cars:     no extra cars in lane, wheels rotate correctly, no warped badges, no license plate text.
Product:  label must stay legible and unchanged, no extra products, no floating, no melting.
People:   no extra fingers, hands hold objects firmly, no face drift, no duplicate people.
Food:     no plastic look, steam rises naturally, no morphing ingredients.
General:  no on-screen text, no watermark, no subtitles, no music.
```

### 4.7 דוגמת ייחוס: פרסומת דובאי בסגנון edbert_yienson (30 שניות, תמונה אחת)
הפרומפט המקורי מתומלל בפרק 00. זו הגרסה המשוכתבת לפי כל הכללים:
```
@Image1 is the driver's face and identity only — keep facial features identical in every shot; ignore its background and lighting.
GLOBAL STYLE: premium automotive commercial, 9:16, photoreal, teal-and-orange grade, anamorphic flares, crisp 1080p, no on-screen text, no logos.
SCENE: The man from @Image1, black tailored suit, drives a yellow Lamborghini Revuelto through Dubai at golden hour.
0:00-0:06  Continuous FPV aerial dive from the tip of the Burj Khalifa down toward street level; the yellow supercar is picked out on the right side of frame as it comes into view.
0:06-0:09  Lateral tracking shot at wheel height; camera holds the side profile, then the car accelerates and overtakes the camera, exiting frame left. Hard cut.
0:09-0:11  Inside the cabin, center rear-view mirror shot: his eyes in the mirror, skyline receding behind.
0:11-0:13  Nose-on low angle, grille and headlights filling frame, heat shimmer off the asphalt.
0:13-0:16  Cockpit view from the passenger side, 35mm: his face in 3/4, calm half-smile, one hand on the wheel.
0:16-0:19  Rear-bumper 3/4 tracking shot, the car pulling away down an empty straightaway.
0:19-0:23  Macro insert: carbon-fiber wheel spinning, brake caliper glowing, speed ramp into slow motion.
0:23-0:27  Lateral profile hold again, the car accelerates and passes the camera a second time.
0:27-0:30  Locked-off 3/4 wide shot at sunset; the car drives through and out of frame. Hold on empty road.
AUDIO: V12 engine roar rising on each pass, tire hiss, wind, deep cinematic bass hits on cuts, no dialogue.
CONSTRAINTS: same car color and model in every shot, no extra cars in lane, no warped text, no face drift.
```
גרסה מרובת רפרנסים (C2) נמצאת בנספח, פרומפט A1b.

### 4.8 בחירת מודל לפי משימה (מעודכן מול B1, בלי Sora)
| | **Seedance 2.5** | **Kling 3.0** | **Veo 3.1** | **Gemini Omni Flash 1.1** |
|---|---|---|---|---|
| אורך מקס' | **30 שניות** | 15 שניות | 4/6/8 שניות לקליפ (‏1080p/4K רק ב-8 ש'); Extend של 7 ש' עד 148 ש' ב-720p | 3–10 שניות (שרשור עד ~40) |
| רב-שוטי | נייטיב, timecodes | עד 6 שוטים | `[00:00-00:02]` | לא נייטיב |
| רזולוציה | 720p ברוב הספקים, 1080p ב-Higgsfield/fal | **4K native** (ב-API מ-23.04.2026), 60fps ב-Ultra [לא מאומת] | עד 4K | 4K/1080p ב-upscale מ-720p |
| רפרנסים | 50 | Elements | Ingredients, first/last | 1–10 תמונות |
| חוזקות | פרסומות, רכבים, multi-shot, V2V, Region Edit, הארכה | תנועה, ריקוד, מוצר חד, ליפ-סינק זול (Turbo) | אודיו ודיאלוג אנגלי, ריאליזם, Lite זול | מקום 1 ב-Arena, אווירה, draft זול ב-360p |
| חולשות | יקר לשנייה, 24fps קבוע | 15 שניות | קצר, ירד ל-~מקום 12 | "Action descriptions are followed loosely", טקסט קטן מתפרק |

**איך לבחור:** פרסומת רב-שוטית או "אינסוף זוויות" ← Seedance 2.5. שוט hero חד של מוצר ← Kling 3.0 / Omni ב-4K. דיאלוג באנגלית ← Veo 3.1 Fast / Kling 3.0 Turbo. טיוטות זולות ← Gemini Omni ב-360p או Seedance ב-480p. **דיבור בעברית ← צילום אמיתי ← V2V.**
**המרת פרומפט בין מודלים:** קודם מקצרים לאורך הנתמך, אחר כך מחליפים תחביר רפרנס (`@Image1` ↔ `@Element1` ↔ "the woman from the reference image"), ואז תחביר אודיו. (מדריכי "Sora 2 prompts" ברשת כבר לא רלוונטיים.)
**הערת B1:** בזירה העיוורת Seedance 2.0 (מקום 5) מעט מעל 2.5 (מקום 7). ‏2.5 מנצח באורך, ברפרנסים ובעריכה, לא באיכות פריים גולמית. לשוט קצר מ-15 שניות שצריך 4K, ‏Seedance 2.0 זול יותר וטוב באותה מידה.

### 4.9 Claude כמחולל פרומפטים: meta-prompt כללי (C1, מעודכן)
זרימת rourke (פרק 00): **רשימת timecodes קצרה ← LLM ← פרומפט מקצועי ← Lovart/Higgsfield**. מדביקים פעם אחת כ-system prompt או כ-Claude Project, ואז שולחים רק בריף קצר. (שינוי מ-C1: Sora הוחלף ב-Gemini Omni Flash.)
```
You are a senior commercial director and AI-video prompt engineer. You write production prompts for Seedance 2.5 (default), and can convert to Kling 3.0, Veo 3.1 or Gemini Omni Flash on request.

INPUT I will give you (any language, often Hebrew):
- Format & goal (ad / vlog / drama / product), platform & aspect ratio (default 9:16), total duration (max 30s for Seedance 2.5, 15s Kling, 8s Veo per clip, 10s Gemini Omni per clip).
- My assets: list of @Image/@Video/@Audio and what each is.
- A rough shot list, optionally with timecodes (e.g. "00:00 tracking shot / 03:07 close up slow motion / 06:14 top down").
- Must-keep rules (e.g. "keep location, dialogue and actions identical to @Video1").

OUTPUT exactly this structure, in English (keep any dialogue lines in their original language inside quotes):
1. ASSET BINDING — one line per asset: "@Image1 = <one job only>; do not take its <X>."
2. GLOBAL STYLE — genre, grade, film/digital look, aspect ratio, frame rate/shutter, what must NOT appear.
3. SCENE — one-sentence logline (who, where, what happens, genre, overall camera feel).
4. CHARACTERS / PRODUCT — concrete physical attributes; reference tags.
5. TIMELINE — continuous, gap-free timecodes covering the full duration. For each shot:
   [mm:ss-mm:ss] Shot N: subject + action (strong verbs, physical consequences) · shot size & angle · lens (mm) · light source & direction · EXACTLY ONE camera move with end state · how the shot ends · transition ("Hard cut to Shot N+1" / match cut / whip pan).
   Rules: 1.5–3s shots for ads, 4–8s for drama; max one location per shot; never two camera moves in one shot.
6. PHYSICS — weight, fabric, hair, liquids, speed ramps (only where specified).
7. AUDIO — Dialogue (character): "..." / SFX / Ambience / Music — or explicitly "no music".
8. CONSISTENCY LOCKS — face, wardrobe, product, member count, screen direction.
9. NEGATIVE LINE — 3–6 targeted items, phrased specifically.

Then add:
- "SPLIT PLAN": how to split this into 2–4 shorter generations if the full one fails (Seedance works better in incremental clips).
- "WEAK SPOTS": 2–3 shots most likely to fail (hands, text, fast motion) and a fallback for each.
- "SHORT VERSION": a 60–100 word single-clip version.

Never use empty adjectives (stunning, epic, 8K, masterpiece). Prefer verbs, named light sources, lens numbers. No on-screen text unless I ask. Ask me at most 2 questions only if a critical input is missing; otherwise make smart assumptions and state them in one line.
```
**בריף קצר לדוגמה (נשלח אחרי ה-meta-prompt):**
```
פורמט: פרסומת לבית קפה בתל אביב, 9:16, 20 שניות, Seedance 2.5.
נכסים: @Video1 = צילום טלפון של הבריסטה מכין קפה (טייק אחד רחב). @Image1 = לוגו (רק לשלט על הכוס בסוף).
שוטים: 00:00 tracking to barista / 03:00 macro espresso pour slow motion / 07:00 top down latte art / 11:00 camera inside the cup looking up / 15:00 customer first sip close up / 18:00 wide locked-off hero.
Keep location, actions and timing identical to @Video1.
```
**טיפים:** ב-Claude מדביקים את הסרטון או פריימים ממנו (כמו rourke), והמודל מתאר כל timecode. מבקשים "3 variations of Shot 4 only" לשוט בעייתי. שומרים את ה-meta-prompt כ-Project או Custom GPT. זה גם נכס שאפשר **למכור** (חבילת פרומפטים, קורס).

ה-meta-prompt הייעודי ל"אינסוף זוויות" (MOUTH MAP וכו') נמצא בסעיף 6.4.

### 4.10 רשימת בדיקה לפני Generate
- [ ] בכל שוט תנועת מצלמה אחת, עם מצב סיום
- [ ] ציר זמן רציף שמכסה את כל המשך
- [ ] לכל @רפרנס תפקיד אחד, וכתוב מה הוא **לא** קובע; אין הפניה למשבצת ריקה; `@Image1` = הפנים הראשיות
- [ ] בחרתי במודע: start frame / reference / original video
- [ ] מקור אור מוגדר עם כיוון
- [ ] אודיו מוגדר, כולל `no music` אם צריך
- [ ] שורת negative קצרה + נעילות + סעיף PRESERVE
- [ ] אין stunning / epic / 8K; אין טקסט על המסך (נוסף בעריכה)
- [ ] 9:16 מוגדר
- [ ] ניסיון ראשון קצר (4–8 שניות) וב-480p לפני 30 שניות וב-1080p
- [ ] שיניתי **משתנה אחד בלבד** מהריצה הקודמת

---

## 5. אסטרטגיית ג'נרציה: טסטים זולים, קליפים קצרים

### 5.1 חמשת חוקי הברזל
1. **"Small clips incrementally" (rourke):** "It's not going to give you the perfect generation all in one go. Instead, take small clips and give those to Seedance and adjust the camera angle in incremental clips." מקטעים של **3 עד 8 שניות** (C1 המליץ 5–8, C3 ‏3–8; המינימום הטכני ב-Seedance: רפרנס וידאו 1.8 שניות, פלט 4 שניות).
2. **480p קודם.** Draft Mode נוסף ב-Higgsfield ב-22.9 ([Changelog](https://higgsfield.ai/creator-hub/changelog)). בודקים פנים, ידיים, ספירת אובייקטים ותנועה. רק אז 1080p.
3. **משתנה אחד בכל ריצה.** אחרת לא יודעים מה תיקן.
4. **תקציב ×3 עד ×5.** ביקורת על Higgsfield: "3-5 generation attempts per usable clip" ([Luma](https://lumalabs.ai/news/higgsfield-pricing)); זה מקור מתחרה, אבל תואם לניסיון שטח.
5. **עריכה קודם, ג'נרציה אחר כך.** חיתוך של 6 פריימים או punch-in של 115% מעלימים רוב הבעיות. מייצרים מחדש רק כשהארטיפקט בשוט הגיבור או בשניות 0–2.

**מתי בכל זאת 30 שניות בטייק אחד?** C2 ממליץ להעדיף ג'נרציה אחת רב-שוטית של Seedance 2.5 על פני 8 ג'נרציות נפרדות, כי העקביות פנימית. **הכרעה:** ב-Image→Video מסוג דובאי (שוטי רכב, פנים מעט) מנסים קודם 30 שניות ב-480p; אם 2–3 שוטים נכשלים, עוברים ל-SPLIT PLAN שה-meta-prompt מייצר. ב-V2V ובאינסוף זוויות תמיד עובדים בקליפים קצרים.

### 5.2 מחירון Seedance 2.5 (לפי ספק; המחירים משתנים פי 2 ויותר)
| ספק | 480p | 720p | 1080p | הערה |
|---|---|---|---|---|
| **Higgsfield** (קרדיט ≈ $0.05) | 10 שניות = $1.50 (‏4.6 ₪) | 10 שניות = $3.50 (‏10.6 ₪) | 10 שניות = 120 קרדיטים = **$6 (‏18 ₪)** | [Higgsfield](https://higgsfield.ai/blog/seedance-2-5-on-higgsfield-2026) (אומת); "early access" ו"לא ב-Unlimited" [לא מאומת]. מדריך מחירים אחר של Higgsfield מציג 52 קרדיטים ל-8 ש' ב-720p ([Higgsfield](https://higgsfield.ai/blog/seedance-2-5-pricing-2026)), קרוב אך לא זהה |
| **fal** | $0.22/ש' (‏0.67 ₪) | $0.47/ש' (‏1.43 ₪) | ~$1.16/ש' (‏3.54 ₪) | [fal](https://fal.ai/models/bytedance/seedance-2.5/image-to-video) (תוקן מ-$1.36) |
| **OpenRouter** | — | $0.231/ש' | — | B1 |
| **Segmind** (V2V) | $0.06/ש' | $0.14/ש' | — | C3 |
| מצב Edit (V2V) | ×0.6 ממחיר יצירה (~$0.28/ש' ב-720p ב-fal) [לא מאומת; בדוגמת fal עריכה של 20 ש' עלתה $5.18 ב-480p ו-$27.40 ב-1080p, כלומר כ-$0.26/ש' וכ-$1.36/ש'] | | | B1, [fal](https://fal.ai/learn/tools/how-to-create-multi-angle-video-seedance-2-5) |

**דוגמאות פרויקט (30 שניות):**
| תרחיש | הרכב | $ | ₪ |
|---|---|---|---|
| Higgsfield, רשמי | 2 טסטים 480p ($9) + 1080p אחד ($18) | ~$27 | ~82 |
| fal, B1 (מתוקן) | 3 טיוטות 480p ($20) + 720p ($14) + 1080p ($35) | ~$69 | ~210 |
| A1 (הערכה) | 30 שניות 1080p ב-Higgsfield | $11–14 | 33–43 [לא מאומת; נמוך מהמחירון הרשמי של $18, אולי לפי מנוי] |
| זול (B1) | 6 טיוטות Gemini Omni 360p + ‏4 קליפים Veo 3.1 Fast 1080p | $8–12 | 24–36 |
| סטנדרט (B1) | 3 טיוטות Seedance 480p + רינדור 720p | $25–35 | 76–106 |
| פרימיום (B1) | הנ"ל + 1080p סופי + 2 שוטי Kling 4K | $70–90 | 213–274 |

**המשמעות העסקית:** עלות המודל זניחה מול המחיר ללקוח. העלות האמיתית היא זמן איטרציות. לכן שווה מנוי "Unlimited" (Higgsfield All Unlimited מ-20.07) או cashback ב-API (‏$15 בונוס אחרי $100, עד 20% cashback, 02.10.2026) ([Higgsfield](https://higgsfield.ai/changelog)).

### 5.3 עקביות בין שוטים וג'נרציות
| בעיה | תיקון |
|---|---|
| פנים זזות לאורך קליפ | `@Image1` קבוע ותיאור זהות זהה מילה במילה בכל פרומפט; לקצר קליפ; להאט תנועה |
| דמות שונה בין קליפים | אותו סט רפרנסים באותו סדר; תיקייה "LOCKED" |
| איפוס אחרי חיתוך | הפריים האחרון של קליפ N = start frame של קליפ N+1 ([MagicHour](https://magichour.ai/blog/how-to-keep-characters-consistent-in-ai-video)) |
| זהות משתנה עם תאורה | רפרנסים בתאורה ניטרלית; בסצנה תאורה "מתונה" |
| "בן דוד" | ערבבתם תקופות; סט מאותו יום |
| בגד משתנה | רפרנס בגדים + `same outfit throughout, no wardrobe change` |
| ידיים/מגע | לקצר את רגע המגע; ידיים חלקית מחוץ לפריים |
| סדרה (אותה דמות בסרטונים רבים) | שיטת Anchor Shot (למטה) |

**שיטת Anchor Shot** ([heyuan110](https://www.heyuan110.com/posts/ai/2026-07-11-seedance-2-prompt-guide/)): (1) Storyboard עם שוטים של עד 15 שניות ← (2) חבילת רפרנסים: character sheet רב-זוויתי וקליפים ← (3) שוט עוגן שנועל דמות, לוק ופלטה ← (4) העוגן כ-`@Video` בכל השוטים הבאים ← (5) השלמת פערים בהארכה ← (6) הרכבה בעריכה.

### 5.4 כשלים נפוצים ותיקונים
| כשל | סימפטום | תיקון |
|---|---|---|
| עומס הוראות | מתוך 8 דרישות בוצעו 4–5 | 60–100 מילים לקליפ, החובה בהתחלה |
| שתי תנועות מצלמה | רעידות, סחף | תנועה אחת, השאר `Cut to` |
| רפרנס עירום | תאורה ומסגור זולגים | תפקיד + "only" + "not" |
| רפרנס חזק מדי | "קרטון", בלי הבעה | 70–80% |
| דחיסת סצנות | 3 מיקומים ב-5 שניות = מורפינג | לפצל או להאריך |
| חורים בציר | קטעים מתים או ממוצאים | ציר רציף |
| טקסט משובש | שלטים ולוגואים מעוותים | לא לבקש טקסט; `no text on signs`; להוסיף בעריכה |
| ידיים ומגע | אצבעות נמסות סביב כוס | שוט רחב, `hands grip firmly`, Region Edit |
| תנועה מהירה נמרחת | אקשן מרוח | `speed ramp into slow motion`, שוטים קצרים |
| מוזיקה לא רצויה | תזמורת אקראית | `no music` |
| פנים נודדות | השחקן משתנה | `Face lock: identical features, zero drift` + קליפ עוגן כ-@Video |
| החלפת מיקום דמויות | מתחלפות בצדדים | `FIRST FRAME AND BLOCKING` עם קואורדינטות (`woman frame-left x 30%`) |
| מספר דמויות משתנה | פתאום חמישה | `MEMBER COUNT LOCK: exactly four` |
| "מרחף" | רגליים מחליקות | `PHYSICS: feet plant firmly, weight transfer` |
| ייצור ארוך שנכשל | 30 שניות, 5 טובות | קליפים קצרים, Region Edit, הארכה |
| V2V משנה יותר מדי | הכל השתנה | `Preserve ... Only modify X` |

---

## 6. הפקה היברידית (Video-to-Video)

### 6.1 מפת הכלים (אוקטובר 2026)
| כלי | מה עושה | קלט וידאו | פלט | רפרנסים | אודיו | מחיר | מקור |
|---|---|---|---|---|---|---|---|
| **Genjutsu: Motion Transfer** | שומר תנועה, מצלמה, חיתוכים ותזמון; בונה מחדש דמות ועולם | 4–30 שניות | 480/720/1080p | עד 30 (צד ג': 40); בפועל 3–6 | לא מתועד | 15 שניות: 40 / 104 / 144 קרדיטים = $2 / $5.2 / $7.2 (‏6 / 16 / 22 ₪) | [Higgsfield](https://higgsfield.ai/blog/higgsfield-genjutsu) |
| **Genjutsu: Object Swap** | מחליף אלמנט אחד, השאר נשאר | כנ"ל | כנ"ל | כנ"ל | לא מתועד | כנ"ל | [Higgsfield](https://higgsfield.ai/genjutsu) |
| **Genjutsu: Restyle** (30.9) | מצייר מחדש בסגנון (20+ או מרפרנס), כולל אנימה | כנ"ל | כנ"ל | עד 30 | — | כנ"ל [לא מאומת] | [Changelog](https://higgsfield.ai/creator-hub/changelog) |
| **Seedance 2.5 Edit/Reference** | זוויות מצלמה חדשות מאותו טייק, Region Edit, Extend | עד 10 סרטונים, 1.8–30.2 שניות, ≤200MB | 4–30 שניות | 30/10/10 | מסנכרן לאודיו המקור ("the performance and its soundtrack stay fixed") | ראו 5.2 | [fal](https://fal.ai/learn/tools/how-to-create-multi-angle-video-seedance-2-5) |
| **Runway Aleph 2.0** | עריכה מקומית לפי פריים ערוך, רב-שוטית; הוספה/הסרה/החלפה, תאורה | **עד 30 שניות ב-1080p** (B1, הודעת Runway) | 1080p | פריים ערוך + פרומפט | שומר מקור | 28 קרדיטים/ש' (‏140 קרדיטים ל-5 ש', [runway.com/pricing](https://runway.com/pricing)) ≈ $0.44–0.67/ש' באפליקציה, $0.28/ש' ב-API ($0.01 לקרדיט); 10 שניות ≈ $4.4–6.7 (‏13–20 ₪) | [Runway](https://runway.com/news/introducing-aleph-2-and-edit-studio) |
| **Luma Ray 3.2 V2V** | שינוי עולם עם Structure / Bodies / Poses / Face | עד 20 שניות, פלט באורך זהה | עד 1080p | — | לא מתועד | לפי רזולוציה | [Luma](https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video) |
| **Kling O1 Edit** | החלפת דמות/סביבה/סגנון בשפה טבעית | **3–10 שניות** | 720–2160px | עד 4 | `keep_audio` (ברירת מחדל false) | $0.168/ש' (‏0.51 ₪) | [fal](https://fal.ai/models/fal-ai/kling-video/o1/video-to-video/edit) |
| **Kling Omni (O3)** | עריכה עם עקביות למקור, Elements | 3–15 שניות | 4K | Elements | — | $0.044–0.168/ש' | B1 |
| **Kling Motion Control** (2.6/3.0) | תנועה מווידאו לתמונת דמות (ריקודים) | וידאו + תמונה | — | 1 | — | $0.112/ש' | [fal](https://fal.ai/models/fal-ai/kling-video/v2.6/pro/motion-control) |
| **MiniMax H3** | עריכה בהוראות, העברת תנועה | 5–15 שניות | 2K | 9/3/3 | — | $0.08–0.13/ש' | B1 |
| **Wan VACE** (קוד פתוח) | Move/Swap/Reference/Expand עם מסכות | ~81 פריימים (~5 שניות ב-16fps) | 720×1280 | כן | — | חינם + GPU (ComfyUI) | [GitHub](https://github.com/ali-vilab/VACE) |

**הערה:** C3 כתב ש-Aleph מוגבל ל-~5 שניות לקטע, לפי Aleph 1 [לא מאומת]. B1 מצטט את הודעת Runway על Aleph 2.0: עד 30 שניות ב-1080p. אנחנו הולכים לפי B1. גם Kling O1 Edit (‏3–10 שניות) ו-Kling Omni O3 (‏3–15 שניות) הם שני מוצרים שונים, לא סתירה.

**שורה תחתונה:**
- החלפת עולם שלמה עם דיבור ← **Genjutsu Motion Transfer**.
- רק מוצר, רכב או שלט ("Fix it in post") ← **Genjutsu Object Swap**, ‏Kling O1 Edit, או Aleph 2.0.
- זוויות חדשות מטייק אחד ← **Seedance 2.5 Edit** (Lovart / fal / Higgsfield).
- ריקוד או טרנד על דמות AI ← Higgsfield AI Influencer / Kling Motion Control.
- שליטה מלאה וחינם עם GPU ← Wan VACE (עקומת לימוד גבוהה, איכות נמוכה יותר).

### 6.2 שלוש טכניקות ליבה

**Motion Transfer (העולם חדש, התנועה נשארת).** פרומפט "שמור + החלף":
```
PRESERVE: original motion, camera path, cuts, timing, body poses, facial expressions, lip movements.
CHANGE: [location] → [new location]; [character] → [new character, see @Image1-3]; [wardrobe] → [...].
STYLE: photorealistic, lighting matched to original, no text overlays.
```
תבנית CHANGE/PRESERVE המלאה ([media.io](https://www.media.io/video-effects/higgsfield-ai-genjutsu-tutorial.html)):
```
Use the uploaded video as reference for motion, timing, cuts, camera trajectory,
framing, perspective and performance.
CHANGE: Move the scene to the entrance of a Monte Carlo grand hotel at night (Reference
Image 2). Replace the blue hatchback with the black Rolls-Royce Phantom from Reference
Image 3. Dress the driver in the black chauffeur suit and cap from Reference Image 4.
PRESERVE: Keep both men's faces, the Hebrew dialogue and lip movement, the original
action, body movement, shot duration, camera motion, composition and interaction timing.
No added text, logos or watermarks.
```
ב-Luma Ray 3.2: Bodies + Poses = "the full performance"; **מכבים Face כשמחליפים דמות**, אחרת "pull the old face back". ב-Genjutsu אין כפתורים, אז כותבים את זה בפרומפט.

**Object Swap ("Fix it in post", שוק ה-B2B).** מצלמים פעם אחת ומחליפים מוצר לכל שוק, צבע או SKU (Higgsfield: שלט SALE, כוס קפה על הירח, "Space Food").
1. מצלמים את השחקן עם **פרוקסי** באותו גודל וצורה.
2. מעלים packshot אמיתי (2–3 זוויות).
3. פרומפט:
```
Replace only the bottle in his right hand with the product in @Image1 (exact shape, color, label). Keep everything else in the shot unchanged: person, hands, background, lighting, camera.
```
4. לוגו שנשבר ← tracking ב-CapCut/After Effects ולוגו אמיתי. **אסור למסור ללקוח לוגו מעוות.**
- חלופה: Seedance 2.5 Edit עם טווח זמן: `From 00:04–00:08, replace ... Preserve the subject's identity, movement, and camera trajectory` ([Kapwing](https://www.kapwing.com/resources/how-to-use-seedance-2-5-a-guide-for-ai-video-creators/)).

**החלפת דמות (משפיען AI, חיה, דמות מצוירת).** Higgsfield AI Influencer (2.10.2026): בונים דמות (סוג, מגדר, גיל, גוף) ומכניסים עם Motion Transfer או Object Swap; 5 ג'נרציות חינם. **שחקן מקור בגוף דומה לדמות** משפר מעקב ([Curious Refuge](https://curiousrefuge.com/blog/how-to-change-camera-angles-with-ai-video)). ראש חתול ענק עובד, אבל ידיים רחוק מהפנים.

### 6.3 Reality-Swap של מאור חני, צעד אחר צעד
**שלב 0: תסריט** (טבלת הביטים בסעיף 2.4).
**שלב 1: צילום (30–60 דק', חבר + טלפון + חצובה).** ביט A: חצובה בגובה עיניים, 9:16, 4K/30, שוט אחד רציף בלי זום, 3–5 טייקים. ביט B: טלפון בתפסנית על משענת הראש הקדמית, מיקרופון דש, פנים למצלמה. רפרנסים: 4 תמונות של מאור (חזית, 3/4 ימין, 3/4 שמאל, גוף מלא), רולס (צד, 3/4 קדמי, פנים), חזית המלון. אופציונלי: clean plate.
**שלב 2: הכנה (10 דק').** חיתוך ב-CapCut: ביט A ל-12–15 שניות, ביט B ל-≤20 שניות. **מייצאים WAV נפרד של ביט B** (ביטוח העברית).
**שלב 3: Genjutsu, ביט A.** Higgsfield ← Genjutsu ← Motion Transfer (או מ-ChatGPT עם `/genjutsu`, הרחבה מ-30.9). מעלים קליפ + 4 פנים + 2 רולס + מלון + מדי שוער:
```
Keep the original motion, camera position, framing and timing exactly.
Replace the parking garage with the front entrance of Hôtel de Paris, Monte-Carlo, late afternoon golden light, marble steps, potted palms.
Replace the small blue car with a black Rolls-Royce Phantom (see references), same position and scale.
The man opening the door becomes a uniformed chauffeur: black suit, white gloves, cap.
Keep the main character's face, hairstyle and gestures identical to the references; dress him in a navy double-breasted suit and sunglasses.
Banknotes falling to the ground stay as in the original.
Photorealistic, natural lighting matched to the original footage, no text, no logos.
```
קודם 480p (‏40 קרדיטים ל-15 שניות, ‏$2, ‏6 ₪). בודקים פנים, ידיות דלת, שטרות, ושהרולס לא "מתנפחת". תיקון: משתנה אחד; פנים זזות ← עוד רפרנסים או קליפ קצר יותר. אחר כך 1080p (‏144 קרדיטים, ‏$7.2, ‏22 ₪; עד ~10 דק' רינדור בעומס ([Cachephoto](https://www.cachephoto.com/en/cineblog/higgsfield-genjutsu-video-a-video/))).
**שלב 4: ביט B (עברית):**
```
Keep the original motion, head movements, lip movements, eye line and timing exactly — the man is speaking, preserve his mouth shapes frame by frame.
Replace the car interior with the rear cabin of a Rolls-Royce Phantom: white leather seats, starlight headliner, wood veneer, champagne flute in the armrest.
Outside the windows: Monte-Carlo harbor with yachts, daylight.
Keep the man's face identical to the references, navy suit, white shirt.
Photorealistic, same lighting direction as the original.
```
**סינכרון שפתיים:** ברילס המקורי הפה תואם לעברית (פרק 00), אבל Higgsfield לא מתעדת טיפול באודיו או ב-lip-sync ([riffkit](https://riffkit.ai/blog/how-to-use-higgsfield-genjutsu)). **תמיד משתיקים את אודיו ה-AI ומניחים את ה-WAV המקורי.** פספוס של כמה פריימים ← מזיזים 1–3 פריימים או חותכים ל-B-roll. במקרה קיצון: lip-sync נפרד (Sync Labs / HeyGen) [לא נבדק].
**שלב 5: עריכה (30–45 דק')** לפי פרק 7: תוצאה למעלה, מקור למטה באותו timecode (50/50 או 60/40), אודיו מקורי + מוזיקת luxury חלשה + סאונד דלת, כתוביות עבריות צרובות, כותרת "HIGGSFIELD GENJUTSU", סיום "תגיבו **רולס** ואשלח לכם את המדריך" + ManyChat.

**עלות (35 שניות):**
| פריט | קרדיטים | $ | ₪ |
|---|---|---|---|
| 480p, 3 ניסיונות × 2 ביטים | ~270 | ~13.5 | ~41 |
| 1080p, 1–2 ניסיונות × 2 ביטים | ~510 | ~25.5 | ~78 |
| **סה"כ AI** | **~780** | **~39** | **~119** |
| חצובה + מיקרופון (חד-פעמי) | — | ~82 | ~250 |

**מחשבון Genjutsu (1 קרדיט ≈ $0.05):**
| רזולוציה | קרדיטים/ש' | $/ש' | 30 שניות |
|---|---|---|---|
| 480p | ~2.7 | ~0.13 | ~$4 (‏12 ₪) |
| 720p | ~6.9 | ~0.35 | ~$10.4 (‏32 ₪) |
| 1080p | ~9.6 | ~0.48 | ~$14.4 (‏44 ₪) |

### 6.4 Infinite Angles (rourke): זרימה מלאה
**העיקרון:** Seedance 2.5 Edit/Reference מקבל את הטייק כ-`@Video1` ו"מצלם מחדש" לפי רשימה מתוזמנת. Curious Refuge: שימור של כ-90–95% מהביצוע. fal הוציאו **13 זוויות מטייק של 20 שניות**.
1. **צילום:** שוט רחב ונעול, הכל בפריים, 10–25 שניות, אביזרים קרובים לגוף, אביזרים שמייצרים נקודות קאט טבעיות.
2. **מיפוי timecodes** על הטייק: פריימים לפעולות (1fps, או 4fps לזריקה), תמלול ברמת מילה לדיבור (ElevenLabs Scribe v2, פחות מ-$0.01).
3. **רשימה קצרה ל-Claude** (הפורמט של rourke):
```
00:00 Tracking shot to Rourke
03:07 Close up slow motion
05:03 Low angle
06:14 Top down shot
08:14 Extreme close up
14:00 Camera inside the cup
15:22 Tracking shot of the lemonade jug
20:06 Dolly zoom
Keep the location, dialogue, and actions identical to the original video.
```
4. **Claude מרחיב** עם ה-meta-prompt הייעודי (מבוסס על המבנה של [fal](https://fal.ai/learn/tools/how-to-create-multi-angle-video-seedance-2-5) ועל פורמט השוט של rourke):
```
You are a cinematographer writing a Seedance 2.5 video-edit prompt.
Source: @Video1, a single locked-off wide take, [DURATION]s, 9:16. Setup: [describe set, person, props].
Shot list (my cut points): [paste timecoded list].
Write one timecoded prompt in this structure:
THE TAKE: what @Video1 shows.
LOCKED ELEMENTS: nothing about the event changes — same location, actions, dialogue, wardrobe, props, timing; only camera position and lens change.
MOUTH MAP: talking windows [paste from transcript] — whenever the mouth is in frame during a talking window, lips follow the original audio; never invent dialogue in quiet windows.
WHERE HE LOOKS: eyes stay on the original A-camera position unless stated.
CLOCK: real-time playback, no retiming, except where slow motion is requested.
COVERAGE: for each shot — [start-end] Shot N: subject, camera placement, lens feel (wide/standard prime/macro), depth of field, movement (dolly, handheld micro-drift, crane), lighting, and transition ("Hard cut to Shot N+1").
CONTINUITY BIBLE: performer, wardrobe, props count (exactly one lemon), set.
CONSTRAINTS: no crew, no extra props, no text, no duplicated objects.
```
דוגמת פלט (מהרילס):
```
[00:00-02.37] Shot 1: Rourke from @Video1 speaks to camera behind the lemonade stand, same performance and dialogue. Straight-on eye level, slow zoom in. Standard prime. Harsh midday sun. Handheld micro-drift easing forward. Hard cut to Shot 2.
[02.37-05.57] Shot 2: The lemon wedge from @Video1 tosses up from Rourke's hand, ramping into deep slow motion as it spins midair...
```
5. **Lovart:** Seedance 2.5, מעלים וידאו (`@Video1`), מדביקים.
6. **קליפים קטנים בפועל:**
| שלב | פעולה | למה |
|---|---|---|
| 1 | חותכים את המקור בנקודות החיתוך ל-3–8 שניות | פחות זוויות לג'נרציה = פחות דליפה |
| 2 | 1–2 זוויות בכל קטע | המודל מקפיד יותר |
| 3 | 480p קודם | טסט של ~$5 (‏15 ₪) במקום ~$27 (‏83 ₪) ל-20 שניות ב-1080p (fal) |
| 4 | בדיקה לפי רשימת הכשלים, תיקון רק הקטע הבעייתי | לא שורפים קרדיטים |
| 5 | 1080p לקטעים מאושרים, חיבור עם **הפסקול המקורי הרציף** | האודיו מדביק חיתוכים |
| 6 | קטע שנכשל שוב ושוב ← השוט המקורי | גם זווית רחבה אמיתית היא זווית |

**רשימת כשלים** ([fal](https://fal.ai/learn/tools/how-to-create-multi-angle-video-seedance-2-5)): פה סגור בזמן דיבור · עיניים שמסתכלות לזווית החדשה במקום ל-A-camera · חפצים כפולים (שני לימונים) · תנועה צפה או איטית מדי · ציוד או צוות ברקע · פריים אחרון חסר או אורך לא תואם · יחס מסך או רזולוציה לא עקביים.
**אזהרה:** "an edit cannot guarantee frame-by-frame overlap with the source" ([Morphic](https://morphic.com/resources/how-to/seedance-2-5-guide)). מסנכרנים בעריכה. ו**AI על AI מוריד איכות** ([Curious Refuge](https://curiousrefuge.com/blog/how-to-change-camera-angles-with-ai-video)): מקור הזוויות עדיף צילום אמיתי, או תוצאת Genjutsu אחת נקייה ב-1080p.

### 6.5 מתכונים לשאר הפורמטים
**פורמט 2: מסטודיו ריק לעולם מלא.** צילום: חדר ריק עם קיר לבן, שחקן אחד ב**פנטומימה ברורה** (מקל מטאטא במקום מוט). Genjutsu: וידאו + 6 רפרנסים (דמויות/תחפושות) + שורה:
```
Same video, but inside a crowded New York subway car. Passengers from the references: a clown, a medieval knight, a person in a dinosaur costume, a spaniel dog. Keep the actor's motion, face and timing exactly.
```
מאותו מקור עוד 2 עולמות (`Same video, but on a medieval battlefield` / `...in a busy street with balloons and bicycles`), ובעריכה מחליפים עולם כל 5–8 שניות. **3 ג'נרציות = 3 "וואו".** גרסת B2B: מצלמים בחור עם הכוס **של הלקוח**, ומבקשים `astronaut suit, on the Moon surface, Earth in the sky, keep the cup in @Image1 exact`; לוגו מתוקן בעריכה. עלות: 3 × 15 שניות 1080p ≈ $22 (‏67 ₪), עם ניסיונות ≈ $50 (‏152 ₪).

**פורמט 4: קומבו Genjutsu ← Seedance (sidequestpat_).** שלב 1, Restyle או Motion Transfer:
```
Keep motion, framing and timing. Replace the plain white living room with a luxury penthouse with floor-to-ceiling windows overlooking the sea at sunset. Change his black t-shirt to a beige knit polo and add a gold watch on the left wrist. Keep his face identical.
```
שלב 2: Seedance 2.5 על **התוצאה**, בקליפים קטנים: קלוז-אפ על השעון, רחפן מחוץ לחלון, פרופיל מול הים, ושוט רחב שחושף "film set with lighting rigs and cinema cameras". שלב 1 ב-1080p; זוויות של 2–4 שניות בקאט (דור שני = ירידת איכות). עלות: ~$15 + ‏$30–50 = **$45–65 (‏137–198 ₪)**. מצוין כ**דמו מכירה** לשירות "פרסומת יוקרה מצילום ביתי".

**פורמט 5: משפיען AI אבסורדי.** צילום: אתם מבצעים טרנד ברחוב תל-אביבי, גוף מלא, 9:16, 8–15 שניות, תנועות חדות, בלי עוברים ושבים בין המצלמה לרקדן. כלי: AI Influencer ← Character Type ← Motion Transfer, או Kling Motion Control (~$1.1 ל-10 שניות, ‏3.3 ₪). מוניטיזציה: מוצר ביד הדמות ב-Object Swap (product placement). עקביות: אותם 3–5 רפרנסים בכל סרטון = "ערוץ ללא פנים".

**וריאציות ישראליות לפורמט 1:** קורקינט ← למבורגיני בדובאי; מטבח בדירה שכורה ← פנטהאוז בהרצליה פיתוח; קופסת שימורים ← ארוחת מישלן. ללקוחות: "צילמנו בטלפון בחניון, והנה הפרסומת שלכם". **Fix it in post לסוכנויות:** "SALE" ← "BLACK FRIDAY" ← "חג שמח", מוצר אדום ← כחול, נוף ישראלי ← אירופאי, מצילום אחד.

⚠️ **מותגים:** לוגו של מלון או רכב אמיתי בפרסומת **מסחרית** ללקוח בלי אישור = סיכון סימני מסחר. בתוכן ממומן עדיף רכב "גנרי-יוקרתי" ומלון בסגנון (`grand Belle Époque hotel entrance at night, Monaco style`) בלי לוגו [המלצה זהירה, לא ייעוץ משפטי].

### 6.6 מגבלות V2V (10/2026)
| נושא | המצב | מה עושים |
|---|---|---|
| אורך | Genjutsu 4–30 ש'; Seedance 4–30 ש'; Luma 20 ש'; Kling O1 ‏3–10 ש'; VACE ~5 ש' | ביטים, חיתוך בנקודה טבעית (מבט, יציאה מפריים) |
| רזולוציה | עד 1080p (Kling עד 2160px); חלק מספקי Seedance רק 480/720p | 1080p מספיק לרילס; ללקוח upscale (פרק 7.7) |
| סינכרון שפתיים | טוב בפועל, **לא מובטח** ב-Genjutsu | אודיו מקורי תמיד, MOUTH MAP ב-Seedance, בדיקה פריים-פריים |
| ידיים, מגע, חסימות | חולשה | חפץ אחד, אחיזה פשוטה |
| טקסט ולוגואים | נשברים | tracking בעריכה |
| זהות | "Faces described without reference images may shift" | 3–6 רפרנסים, קליפים קצרים |
| תנועה מהירה | נמרחת | 60fps וסלואו |
| AI על AI | ירידת איכות בכל מעבר | מקסימום שני מעברים, 1080p בכל שלב |
| קלט | קובץ בלבד; Seedance ≤200MB | מכווצים מראש |
| סימן מים | בתוכנית החינמית של Higgsfield | מנוי בתשלום לכל דבר מסחרי |

### 6.7 עלות מול מחיר ללקוח (הערכה)
| פורמט | עלות AI עם ניסיונות | זמן | מחיר ללקוח ישראלי [לא מאומת, הערכת שוק של C3] |
|---|---|---|---|
| Reality-Swap של 30–40 שניות | 122–304 ₪ | 3–4 שעות | 1,500–3,500 ₪ |
| Infinite Angles (מוצר/פודקאסט) | 90–181 ₪ | 2–3 שעות | 1,200–2,500 ₪ |
| Object Swap: 5 גרסאות מצילום אחד | 82–164 ₪ | 2 שעות | 2,000–4,000 ₪ |
| הפקה היברידית מלאה (3 עולמות) | 152–329 ₪ | 4–6 שעות | 3,000–6,000 ₪ |

**מנויים (בדקו באתר; המקורות סותרים):** Higgsfield לפי Creatify: Starter ~$19 (‏58 ₪, 270 קרדיטים), Plus ‏$47–59 (‏143–179 ₪, 1,200), Ultra ‏$99–129 (‏301–392 ₪, 3,000); הטווחים הם חיוב שנתי מול חודשי (Creatify, 08.2026) [לא מאומת מול higgsfield.ai/pricing, שלא נטען בבדיקה]; קרדיטים לא עוברים לחודש הבא. Runway (אומת ב-[runway.com/pricing](https://runway.com/pricing)): Standard $12 / Pro $28 / Max $76 בחיוב שנתי, ו-$15 / $35 / $95 בחיוב חודשי; 625 / 2,250 / 9,500 קרדיטים בחודש. ב-Pro מקבלים כ-80 שניות Aleph בחודש (2,250 ÷ 28). Kling: Standard $6.99 (‏21 ₪). Lovart: Seedance 2.5 זמין (עד 30 שניות, עד 50 רפרנסים, [Lovart](https://www.lovart.ai/landing/seedance_2_5)); תמחור בקרדיטים לא מפורט בדף [לא מאומת].

---

## 7. עריכה ופריסות

### 7.1 מה האלגוריתם מודד (2026)
- Mosseri: שלושת האותות המרכזיים באינסטגרם הם **watch time**, **sends per reach** ו-**likes per reach**. נמדדים גם מעבר סימן 3 השניות ו-replay: רילס של 15 שניות שנצפה 3 פעמים עוקף רילס של 60 שניות שנצפה פעם אחת ([SocialPilot](https://www.socialpilot.co/de/blog/instagram-reels-algorithm), [eClincher](https://www.eclincher.com/articles/how-the-instagram-algorithm-works-in-2026)). שליחה ב-DM שוקלת פי 3 עד 5 מלייק בהגעה לזרים [לא מאומת: מקור משני].
- **Hook rate של 60–70% בשנייה 3** נחשב בריא; משווים ל-baseline שלכם ([CapCut](https://www.capcut.com/create/short-video-discovery-2026-ai-editing)).
- במחקר על 9.2 מיליון המלצות, 55% מהסרטונים לא נצפו עד הסוף. קליפים מתחת ל-30 שניות מגיעים ל-retention גבוה יותר ([ClipSpeed](https://www.clipspeed.ai/blog/short-form-video-statistics-data-2026.html)) [לא מאומת: נתון משני].

### 7.2 שלוש תבניות שנייה-שנייה
**A. "Before/After Split" (30 שניות, מאור חני + Genjutsu)**
| זמן | מסך | סאונד | מטרה |
|---|---|---|---|
| 0.0–0.5 | שני החצאים כבר מלאים: למעלה יוקרה, למטה חניון. תגיות "AI" / "מקור" | Impact/boom + תחילת מוזיקה | עצירת גלילה |
| 0.5–2.0 | כותרת גדולה: "צילמתי את זה בחניון 👇" / "THIS WAS FILMED IN A PARKING LOT" | דיאלוג מקורי | פער סקרנות |
| 2–12 | 3–5 שוטים של 2–3 שניות, מסונכרנים בין החצאים | SFX על כל חיתוך (דלת, שטרות, מנוע) | הוכחה ש"זו אותה תנועה" |
| 12–14 | **Pattern interrupt:** החצי התחתון נבלע, wipe למעלה, תוצאה במסך מלא | Riser ← drop | איפוס קשב |
| 14–25 | תוצאה במסך מלא + כתוביות מילה-מילה | דיבור + מוזיקה ב-ducking | הנאה |
| 25–28 | חזרה קצרה למפוצל ("ככה זה התחיל") | Whoosh | חיזוק |
| 28–30 | CTA: "תגיבו **רולס** ואשלח לכם את המדריך" | סוף מוזיקלי | תגובות = DM funnel |
| לופ | הפריים האחרון דומה לראשון | חיתוך על downbeat | replay |

**B. "Prompt Reveal" (30 שניות, דובאי).** 0–1 שנ': השוט הכי חזק כבר רץ למעלה, ולמטה פספורט עם התווית INPUT. 1–30 שנ': הפרומפט גולל **בסינכרון**, שורת ה-timecode הנוכחית מודגשת. אי אפשר לקרוא הכל בצפייה אחת, ולכן replay, ולכן 24K תגובות מול 19K לייקים. CTA קבוע באמצע ("STEAL MY PROMPT · COMMENT 'DUBAI'"). בלי דיבור: עובד בכל שפה.

**C. "Infinite Angles".** 0–1 שנ': wipe אנכי **באמצע משפט** (sidequestpat_: "believe it or not… **but this video**"). 1–20: למטה Original נעול, למעלה זוויות שמתחלפות כל 1.5–3 שניות על אותו פסקול. 20–45: הדרכה, צילומי מסך של Claude ו-Lovart עם זום על הפרומפט, ~2 שניות למסך. סוף: CTA ("תגיבו ANGLE").

### 7.3 קצב וחיתוכים
| סוג | אורך שוט | חיתוכים/שנייה | הערה |
|---|---|---|---|
| פרסומת רכב/יוקרה | 1–3 ש' | 0.3–0.5 | פתיחה ארוכה ואז פרגמנטים (דובאי: 9 שוטים ב-30 ש') |
| מפוצל לפני/אחרי | 2–4 ש' | 0.25–0.4 | צריך זמן לסרוק שני חצאים |
| Infinite angles | 1.5–3 ש' | 0.4–0.6 | הדיאלוג רציף, רק הזווית משתנה |
| קטע הדרכה (UI) | 1.5–2.5 ש' | 0.4–0.6 | זום על המקום הרלוונטי |
| סרט נרטיבי (ANERNEQ) | 3–8 ש' | 0.15–0.3 | לטיזר חותכים מחדש לקצב רילס |
(המלצת עבודה על בסיס ספירת שוטים ב-A1 ובפרק 00, לא נתון מחקרי.)

- **Pattern interrupt כל 2–4 שניות:** שינוי פריסה, punch-in של 110–120%, כותרת, SFX או speed ramp.
- **Cut on action ועל ה-beat.** CapCut: Auto Beat. Premiere: M על ה-beats ואז Automate to Sequence.
- **J-cut / L-cut:** סאונד השוט הבא נכנס 4–8 פריימים לפני התמונה. מסתיר תפרים בין ג'נרציות.
- **חותכים תמיד "ראש וזנב"**: 0.2–0.3 (עד 0.5) השניות הראשונות והאחרונות של כל קליפ AI (האטה, מורפינג, קפיאה).
- **אורך:** 20–35 שניות; 45–60 רק עם קטע הדרכה שמחזיק (rourke: 60).
- **fps:** Seedance 2.5 מוציא 24fps קבוע (B1). רילס שכולו Seedance ← טיימליין 24 (או 30). מפוצל עם צילום טלפון ב-30 ← טיימליין 30. לא "מחליקים" ל-60 (ראו 7.7).

### 7.4 מידות הפריסות (קנבס 1080×1920)
**Prompt Reveal:**
| אזור | Y | תוכן |
|---|---|---|
| שוליים עליונים (UI) | 0–220 | רקע/המשך וידאו, בלי טקסט חשוב |
| RESULT | 220–1100 (~880) | הווידאו, crop ל-1080×880 או 4:5 במסגרת |
| כותרת / CTA | 1100–1220 | "STEAL MY PROMPT · COMMENT 'DUBAI'", ‏54–64px |
| INPUT + PROMPT | 1220–1600 | שמאל: INPUT 320×320 + תווית. ימין: PROMPT גולל ~640 רוחב |
| שוליים תחתונים | 1600–1920 | רקע בלבד |

**Split Before/After:** למעלה RESULT 1080×960, למטה ORIGINAL 1080×960 (זה הסדר בכל רילסי המקור; העין נוחתת למעלה). תווית בפינה **שמאלית** עליונה של כל חצי (הימנית התחתונה מוסתרת ע"י פס האייקונים). קו מפריד 4–6px ב-Y=960. **אזהרה:** החצי התחתון נכנס ל-35% שבהם ממשק IG מכסה ([HopperHQ](https://www.hopperhq.com/blog/instagram-reel-size/)); ממקמים את הפעולה החשובה של המקור ב-Y=960–1400, ושום טקסט מתחת ל-1600.

**אזור בטוח אוניברסלי:** 900×1400 במרכז (X≈90–990, Y≈260–1660) ל-IG, TikTok ו-Shorts ([AdaptlyPost](https://adaptlypost.com/blog/social-media-safe-zones-2026-complete-guide)). ב-IG הטופ ~250–270px תפוס (handle, אודיו), והפינה הימנית התחתונה (~40%) תפוסה ע"י האייקונים.

### 7.5 בנייה בכלים
**מסך מפוצל ב-CapCut:**
1. פרויקט 9:16; המקור ברצועה הראשית.
2. Overlay ← Add overlay ← קליפ ה-AI ([CapCut](https://www.capcut.com/create/split-screen-effects-multi-frame-videos)).
3. Basic ← Position/Scale: מקור Y שלילי (תחתון), AI ‏Y חיובי (עליון), Scale ~100%.
4. Mask ← Split (או Linear) לכל קליפ; מזיזים את מרכז המסכה כך שהפנים/הרכב גלויים.
5. סנכרון לפי גל הקול (Genjutsu שומר משך ותזמון, ולרוב מספיק ליישר את הפריים הראשון). סטייה ← Speed 0.97×–1.03× על קליפ ה-AI.
6. קו מפריד: מלבן 1080×6 ב-Y=0 של הקנבס.
7. תוויות "AI" / "ORIGINAL" עם רקע חצי שקוף.
8. אודיו: **רק של המקור**; מה-AI לכל היותר אווירה.

**Wipe ב-CapCut:** AI ב-Overlay מיושר בדיוק (100%) ← Mask Linear, Rotation 90° (אנכי) או 0°, Feather 0–5 ← keyframe על מיקום המסכה: מחוץ למסך בצד אחד ← מחוץ למסך בצד השני תוך 0.4–0.8 שניות ← קו ניאון 8px עם Glow באותם keyframes (ה-wipes של Higgsfield) ← whoosh שמתחיל 2 פריימים לפני ← **wipe על מילה, לא בין משפטים**.

**Premiere Pro:** Sequence ← Custom 1080×1920, Square Pixels, 30fps (או 25/24 לפי המקור); workspace "Vertical" ב-2026.
- מפוצל: V1 מקור, V2 AI. ל-V2 ‏Crop Bottom 50% + Position Y מעלה ~480px; ל-V1 ‏Crop Top 50% + Position Y מטה. Rectangle 1080×6. Nest ("Split_Master"). סנכרון: קליק ימני ← Synchronize ← Audio.
- Wipe: Linear Wipe על V2, keyframe ל-Transition Completion 100%←0% ב-12–20 פריימים, Wipe Angle 90°/0°, Feather 0.
- **PROMPT גולל:** Essential Graphics עם הפרומפט (פונט מונו JetBrains Mono / Roboto Mono, 26–30px, ריווח 1.3) ← מסכת מלבן בגודל החלון ← keyframes על Position Y, keyframe לכל שוט (Hold או Ease) כך שכל שורת timecode מגיעה לראש החלון בתחילת השוט ← מלבן הדגשה קבוע (Opacity 30%). ב-CapCut: keyframe בהתחלה ובסוף + מסכה; אם אין מסכה על טקסט, מייצאים את הפרומפט כ-PNG ארוך.
- **INPUT:** התמונה כ-PNG עם מסגרת ותווית "INPUT", ותיבות "REF 1–6" כמו בממשק Genjutsu.

**ffmpeg (ייצור סדרתי), מסך מפוצל:**
```bash
ffmpeg -i ai.mp4 -i original.mp4 -filter_complex \
"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:960,setsar=1[top]; \
 [1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:960,setsar=1[bot]; \
 [top][bot]vstack=inputs=2,drawbox=x=0:y=957:w=1080:h=6:color=white@0.9:t=fill,format=yuv420p[v]" \
-map "[v]" -map 1:a? -c:v libx264 -profile:v high -preset slow -crf 18 -maxrate 15M -bufsize 30M \
-r 30 -c:a aac -b:a 192k -ar 48000 -movflags +faststart split.mp4
```
(האודיו מהמקור, `1:a`. crop לא מרכזי: `crop=1080:960:0:Y`.)

### 7.6 מעברים
| מעבר | מתי | איך | אורך |
|---|---|---|---|
| Hard cut על beat | ברירת מחדל | חיתוך | 0 |
| Linear wipe אנכי + קו ניאון | חשיפת לפני/אחרי | Mask Linear + keyframe / Linear Wipe | 10–20 פריימים |
| Split ← Full | interrupt באמצע | Scale+Position של חצי ה-AI מ-50% ל-100% | 8–12 |
| Whip pan / blur | בין זוויות (Infinite Angles) | Blur/Swipe / Transform עם Shutter angle | 6–8 |
| Match cut | אותה תנועה בשני עולמות (דלת בחניון ← דלת ברולס) | חיתוך בשיא הפעולה | 0 |
| Speed ramp | אקשן, לימון באוויר | Speed Curve "Montage" / Time Remapping | — |
| Punch-in | הדגשה בדיבור | Scale 100→115% בקפיצה | 0 |
| Flash/white dip | מעבר ל-CTA | Dip to White | 4 |
**להימנע:** "3D cube", מעברים מוכנים מגוחכים, ו-crossfade ארוך בין ג'נרציות (חושף הבדלי צבע ופנים).

### 7.7 סאונד
**שכבות (מלמטה למעלה):**
1. אווירה/room tone. האודיו הנייטיב של Seedance נשאר כשכבת אווירה ב-‎-20 עד ‎-25 dB.
2. מוזיקה: ‎-18 עד ‎-14 LUFS לבד; ducking של ‎-8 עד ‎-12 dB מתחת לדיבור (CapCut Auto ducking; Premiere Essential Sound; Instagram Edits).
3. דיאלוג: ‎-16 עד ‎-14 LUFS, high-pass ב-80Hz, קומפרסור קל. הד בחניון ← Enhance Speech (Adobe Podcast/Premiere) או Voice enhance ב-CapCut.
4. **SFX על כל מעבר:** whoosh ל-wipe, impact לפריים הראשון, riser לפני חשיפה, pop לכותרת, קולות תוכן (דלת, שטרות, מנוע). **SFX הוא הדרך הזולה ביותר לגרום ל-AI להרגיש אמיתי.**
5. Master: **‎-14 LUFS integrated, true peak ‎-1 dBTP**. רילסים "צועקים" יושבים על ‎-10 עד ‎-12 LUFS [לא מאומת].

**זכויות:** חשבון אישי/Creator ← סאונד טרנדי **רק מתוך האפליקציה** (שיר מסחרי צרוב בקובץ = השתקה או חסימה). חשבון Business, לקוח או פרסומת ← ספרייה מסחרית (Meta Sound Collection / TikTok Commercial Music Library), Artlist, Epidemic, ספריית CapCut Pro, או מוזיקה מקורית. "royalty-free" ≠ "copyright-free" ([Soundverse](https://www.soundverse.ai/blog/article/ai-music-for-instagram-reels-that-wont-get-muted-0153)). מוזיקת AI (Suno / Udio / ElevenLabs Music) רק עם זכויות מסחריות בתוכנית [לא מאומת לכל כלי]. טריק נפוץ: עורכים על מוזיקה מורשית ומוסיפים באפליקציה סאונד טרנדי ב-0–5% כדי להיכנס לעמוד הסאונד [לא מאומת שזה עוזר].

### 7.8 צבע
סדר: (1) **אפסקייל לפני צבע** ← (2) נרמול WB וחשיפה מול scopes, עור על ה-skin line ← (3) **Match לקליפ "גיבור" אחד** (CapCut Color Match, DaVinci Shot Match, Lumetri Color Match) ← (4) Look: **LUT ב-50–70%**, split-tone (טיל בצללים, כתום בהיילייטים), **Film grain 15–20%, גודל 0.4**, ‏Gaussian 0.3–0.5 או Halation לשבירת החדות ([InVideo](https://invideo.io/faq/how-do-you-color-grade-ai-generated-video-clips-to-look/), [Genra](https://genra.ai/blog/why-ai-videos-look-fake-how-to-fix)).
- **במפוצל לא מבצעים grade למקור** (או רק תיקון בסיסי); אפשר לקרר/לשטח אותו ב-5–10% כדי לחדד את הניגוד.
- גריין חזק נאכל בדחיסת IG והופך לבלוקים. בודקים בייצוא בדיקה.

### 7.9 טריאז' ארטיפקטים
| ארטיפקט | זיהוי | תיקון בעריכה (זול) | תיקון בג'נרציה (יקר) |
|---|---|---|---|
| ידיים | פריים-פריים על כל מגע | חיתוך לפני המגע, קרופ/punch-in, motion blur, שוט רחב | Inpainting, 2–3 ניסיונות; ידיים פשוטות (אגרוף, כף פתוחה) ([HackerNoon](https://hackernoon.com/how-to-fix-warped-hands-and-faces-in-ai-generated-video)) |
| מורפינג בתנועה מהירה | צורה "זורמת" | speed ramp שמאיץ (6–8 פריימים), חיתוך, motion blur | קליפ קצר (2–4 ש') עם תנועה איטית יותר |
| face drift | השוואת פריימים | שוטים עם פנים קטנות/בפרופיל + הקלוז-אפ הטוב | SOUL ID / @character, Enhancer נגד flicker ([Higgsfield](https://geo.higgsfield.ai/task/blog/which-tool-avoids-flickering-face-ai-video)) |
| Flicker | צפייה ב-100% | Deflicker (DaVinci Studio), Temporal NR, גריין | Topaz Astra |
| טקסט/לוגו מעוות | שלטים, לוחיות, מסכים | טשטוש/כיסוי, טקסט אמיתי עם tracking | Inpainting / Genjutsu Fix it in post |
| אובייקט "רוח רפאים" | עצמים שמופיעים ונעלמים | קרופ, חיתוך | Video inpainting, למשל VOID (Netflix, קוד פתוח, אפריל 2026) [לא מאומת ישירות] |
| ראש/זנב | 0.2–0.5 ש' בקצוות | חיתוך תמיד | — |
| אודיו נייטיב מוזר | מילים לא קיימות | השתקה ו-SFX ספרייתי | — |

**כל טקסט שהצופה אמור לקרוא** (שלט, מחיר, מותג) נוסף בעריכה כשכבה אמיתית, עם tracking אם המצלמה זזה (CapCut Tracking; Premiere Mask Tracking; Corner Pin ב-After Effects). **אמינות מנצחת שלמות:** גריין, motion blur, Camera Shake של 2–5% ו-SFX מסתירים ארטיפקטים טוב יותר מתיקון "מושלם".

### 7.10 אפסקייל ואינטרפולציה
| מצב | המלצה |
|---|---|
| Seedance 2.5 ב-1080p ← רילס | **לא צריך** (IG דוחסת בכל מקרה) |
| ג'נרציה ב-720p ← רילס | ×1.5 ל-1080p (Topaz Proteus/Rhea או Astra) |
| לקוח / מסך גדול / YouTube 4K | 4K. ב-Shorts, ‏4K מקבל 20–30 Mbps ([ShortSync](https://shortsync.app/resources/youtube-shorts-upload-requirements-2026)) |

**כלים:** Topaz Video (desktop, GPU) ~$299 לשנה (‏909 ₪); **Topaz Astra / Astra 2** (ענן, upscaler דיפוזיוני עם פרומפט, Creativity 1–5, אפריל 2026) $39 לחודש (‏119 ₪), במבצע $19 (‏58 ₪), או $328 לשנה (‏997 ₪) ([MyArchitectAI](https://www.myarchitectai.com/blog/topaz-ai-pricing)); Topaz Seedance Upscaler (4K + אינטרפולציה עד 60fps); fal upscalers, Upsampler, Enhancer של Higgsfield. **Creativity גבוה ב-Astra משנה פנים וטקסט:** ללקוח עם פנים מוכרות, 1–2.
**אינטרפולציה:** כן לסלואו-מושן מכוון (לימון, שטרות, דלת) ×2–×4 ב-Apollo/Chronos או **RIFE** חינמי (Flowframes). לא ל"החלקה" של 24←60 (יחס 2.5 = judder). Apollo: פחות ארטיפקטים, פנים קופצניות; Chronos: הפוך. אינטרפולציה **מגבירה** מורפינג קיים, אז מתקנים קודם. ×2 RIFE לפני עריכה מחליק drift אבל נותן "מראה טלנובלה": רק למוצר נקי.

---

## 8. כתוביות ועברית

### 8.1 סגנונות
| סגנון | מתי | מפרט |
|---|---|---|
| **מילה-מילה (karaoke)** | דיבור למצלמה | 1–3 מילים, 70–90px, פונט עבה, stroke שחור 6–8px, המילה הפעילה בצהוב/ירוק |
| **מילה אחת גדולה** | בלי דיבור, מעברים | 120–160px, מרכז, pop של 3 פריימים |
| **כותרת קבועה** | כל הסרטון | שם הכלי ("HIGGSFIELD SEEDANCE 2.5 1080P") או CTA, 48–60px, Y≈280–400 |
| **תוויות טכניות** | INPUT / PROMPT / RESULT / ORIGINAL / AI | 28–36px, caps, מלבן מעוגל |
| **דיאלוג קולנועי** | טיזר לסרט | 40–48px, לבן דק, תחתית האזור הבטוח |
טקסט על המסך **בכל רגע** (פרק 00, דפוס 5). כתוביות **צרובות**, לא SRT. לבן עם stroke שחור. מקסימום 2 שורות.

### 8.2 איפה כל כלי עומד בעברית (10/2026)
| כלי | תמלול עברי | הערה |
|---|---|---|
| Premiere Pro | **אין** (בקשות פתוחות בקהילת Adobe, עדיין ללא מענה באפריל 2026; פתרון עוקף: תוסף צד ג' או SRT מ-Whisper) | SRT עברי מתהפך ← Track Settings ← Styling ← Text Engine = **"South Asian and Middle Eastern"**; גם ב-Preferences ← Graphics ← Text Engine ([Adobe Community](https://community.adobe.com/t5/premiere-pro-discussions/srt-import-with-right-to-left-language-e-g-hebrew-arabic-text-is-reversed/m-p/13592853/highlight/true)) |
| DaVinci Resolve | כן, לפי דיווחי קהילה | [לא מאומת בגרסה הנוכחית] |
| CapCut | בחירת שפה ב-Auto captions; בחירה שגויה = ריק/שגוי | [לא מאומת: איכות עברית]; לבדוק פיסוק |
| Submagic | מצהירה על עברית עם אנימציה ואמוג'י, מסמנת מילים מפוקפקות בכתום | "99.5%" לפי היצרן [לא מאומת] |
| Instagram Edits | "מספר שפות" | עברית [לא מאומת] |
| Whisper large-v3 / ivrit.ai | כן, לוקלי וחינמי | ivrit.ai [לא מאומת: מצב עדכני] |

### 8.3 תהליך עבודה (כל עורך)
1. מייצאים WAV ← Whisper large-v3 ← SRT ברמת מילה (`--word_timestamps True`).
2. מעבר ידני: שמות, סלנג, מספרים.
3. ייבוא: Premiere עם Text Engine מזרח-תיכוני; CapCut: Import captions.
4. **בדיקת bidi לכל שורה מעורבת** ("ייצרתי את זה ב-Seedance 2.5 תוך 10 דקות"): (א) פיסוק שקופץ שמאלה, (ב) "2.5" שמתפצל, (ג) סוגריים הפוכים. **תיקון:** תו **RLM** (U+200F) אחרי המילה האנגלית או בסוף השורה, או המילה האנגלית בשורה נפרדת. במקרים קשים: Photoshop/Canva ← PNG.
5. **פונטים (Google Fonts, חינם גם מסחרית):** Heebo Black/ExtraBold, Rubik Bold/Black, Assistant ExtraBold, Secular One, Suez One (פרימיום), Varela Round. מתקינים לוקלית, כדי לא לקבל "ריבועים".
6. יישור למרכז. תווית אנגלית בשורה נפרדת ("AI" מעל "מה שיצא").
7. אימוג'י ב-PNG; בתוך כתובית RTL הם עלולים להחליף צד.
8. **אף פעם לא טקסט עברי דרך המודל** (גם לא על מוצרים): מודלים שוברים טקסט, ועברית עוד יותר [לא מאומת בבדיקה, מבוסס על הלקח הכללי].

---

## 9. ייצוא

### 9.1 לפי פלטפורמה
| פרמטר | Instagram Reels | TikTok | YouTube Shorts |
|---|---|---|---|
| רזולוציה | 1080×1920 | 1080×1920 | 1080×1920 (אפשר 2160×3840) |
| Codec | H.264 MP4 (HEVC נכשל במכשירים ישנים) | H.264 MP4, **לא HEVC** (קידוד מחדש פוגע) | H.264 (או H.265) |
| FPS | 30 (60 לתנועה מהירה; 23–60 נתמך) | 30 או 60 | 24–60 |
| Bitrate | 8–15 Mbps | 10–15 (1080p30), 15–25 (1080p60) | ~12 (1080p), 20–30 (4K) |
| אודיו | AAC 128–320 kbps | AAC 192 kbps (מקור אחד: 44.1kHz) | AAC-LC 384 kbps, 48kHz |
| צבע | Rec.709 SDR | Rec.709 SDR | Rec.709 (HDR ב-Rec.2020 PQ) |
מקורות: [Argil](https://argil.ai/blog/instagram-reel-size-e350f), [ShortSync TikTok](https://www.shortsync.app/guides/tiktok-video-quality-settings), [ShortSync Shorts](https://shortsync.app/resources/youtube-shorts-upload-requirements-2026).

**מאסטר אחד לכולן:** 1080×1920, H.264 High, 30fps (או fps המקור אם 24/25), VBR 2-pass יעד 12 / מקס' 15 Mbps, AAC 192 kbps ב-48kHz [44.1 ב-TikTok: 48kHz מתקבל בפועל, לא מאומת], yuv420p, Rec.709, **לא HDR**.

### 9.2 הגדרות בכלים
- **CapCut:** 1080p ← 30fps ← Bitrate "Higher" (Desktop: Custom 12–15 Mbps) ← H.264 ← MP4. ‏4K60 ו-HDR דורשים Pro: $19.99 לחודש (‏61 ₪) או $179.99 לשנה (‏547 ₪). ב-Free יש watermark על חלק מהתבניות.
- **Premiere:** H.264 ← "Match Source – Adaptive High Bitrate" ← VBR 2-pass, Target 12, Max 15 ← AAC 192/48kHz ← "Use Maximum Render Quality" אם יש scaling.
- **Instagram Edits:** עד 4K60 בלי watermark, כולל safe zones.
- **ffmpeg (מאסטר):**
```bash
ffmpeg -i master.mov -vf "scale=1080:1920:flags=lanczos,format=yuv420p" -r 30 \
-c:v libx264 -profile:v high -level 4.2 -preset slow -b:v 12M -maxrate 15M -bufsize 24M \
-color_primaries bt709 -color_trc bt709 -colorspace bt709 \
-c:a aac -b:a 192k -ar 48000 -movflags +faststart reel_1080x1920.mp4
```

### 9.3 העלאה בלי לאבד איכות
- TikTok: Settings ← Content preferences ← **Allow high-quality uploads**.
- Instagram: Settings ← Data usage and media quality ← **Upload at highest quality**; העלאה ב-WiFi.
- העברה לטלפון ב-AirDrop או כבל, **לא WhatsApp**. לא מוסיפים פילטרים באפליקציה (קידוד נוסף).
- Cover: פריים "וואו" עם טקסט בתוך ה-1:1 המרכזי (1080×1080, Y≈420–1500).

---

## 10. QA, תיוג AI ופרסום

### 10.1 תיוג AI
- **Meta:** חובה לסמן תוכן AI ריאליסטי; תווית "AI info" גם אוטומטית לפי C2PA ([MakeInfluence](https://www.makeinfluence.com/en/academy/content-credentials-c2pa-how-platforms-label-ai-assisted-content)).
- **TikTok:** הכי מחמירה. תווית חובה על כל תוכן שמייצר או משנה משמעותית תיאור ריאליסטי של אנשים; C2PA ו-watermark בלתי נראה; strikes, ולפי מקור משני הרחקה ממונטיזציה אחרי 4 עבירות ([Storrito](https://storrito.com/resources/tiktoks-2026-ai-labeling-rules-and-what-they-signal-for-platform-governance)) [לא מאומת: פרטי הענישה].
- **בפועל:** מסמנים בעצמכם (ה-AI ממילא נקודת המכירה). לא "מנקים" מטא-דאטה. בתוכן ללקוח: גם Paid partnership.

### 10.2 רשימת QA לפני פרסום (מאוחדת, C2 + C4)
**טכני**
- [ ] 1080×1920, 9:16, בלי letterbox בשום פריים
- [ ] H.264, MP4, yuv420p, Rec.709 SDR, 30fps (או fps המקור)
- [ ] 8–15 Mbps; AAC 192k/48kHz; `+faststart`
- [ ] ≈‎-14 LUFS, true peak ≤‎-1 dBTP, בלי clipping
- [ ] נבדק על **טלפון אמיתי**, בבהירות מלאה ונמוכה, באוזניות וברמקול

**זהות ומוצר (C2)**
- [ ] "מבחן חבר": מזהים אותי/את הלקוח מיד?
- [ ] הפנים זהות בשוט הראשון ובאחרון
- [ ] תווית/לוגו קריאים בשוט ה-hero
- [ ] בגדים לא השתנו; אין טקסט, סימני מים או ניצבים שנוספו

**הוק וקצב**
- [ ] הפריים הראשון "וואו" (לא לוגו, שחור או סטטי)
- [ ] לפני **וגם** אחרי נראים בשנייה הראשונה (split/wipe)
- [ ] טקסט הוק מפריים 0, עד 7 מילים, נקרא תוך 1.5 שניות
- [ ] אין קטע של יותר מ-4 שניות בלי שינוי ויזואלי
- [ ] נחתכו ראש/זנב של כל ג'נרציה
- [ ] הסוף מתחבר לפתיחה (לופ); 20–35 שניות (אלא אם יש סיבה)

**פריסה וטקסט**
- [ ] כל טקסט קריטי בתוך 900×1400; כלום מעל Y=250 או מתחת ל-Y=1600; כלום מתחת לפס האייקונים
- [ ] תוויות AI / ORIGINAL / INPUT / PROMPT קריאות במסך 6 אינץ'
- [ ] Prompt Reveal: הגלילה מסונכרנת לשוטים, אין שגיאות כתיב בפרומפט
- [ ] **עברית:** כל שורה עם אנגלית/מספרים נבדקה (פיסוק, סוגריים, "2.5"); אין "ריבועים"; הכתוביות תואמות לדיבור

**ארטיפקטים (פריים-פריים בשוטים קריטיים)**
- [ ] ידיים: בלי אצבעות מיותרות או התמזגות
- [ ] פנים: אותו אדם בכל השוטים
- [ ] טקסט ולוגואים בווידאו: הוחלפו, טושטשו או נכונים
- [ ] בלי מורפינג בתנועות מהירות בשוט הגיבור
- [ ] Color match: בלי קפיצת צבע/WB בין שוטים צמודים
- [ ] גריין/soften הוחלו, אין מראה "פלסטי"

**סאונד וזכויות**
- [ ] מוזיקה מורשית / ספרייה מסחרית / AI עם זכויות; בלי שיר מסחרי צרוב בחשבון Business או ללקוח
- [ ] SFX על כל wipe ועל הפריים הראשון
- [ ] הדיבור מעל המוזיקה (ducking)

**הפצה ומשפט**
- [ ] מילת ה-CTA ("רולס", "DUBAI") גם בווידאו וגם בכיתוב; אוטומציית DM (ManyChat) נבדקה עם חשבון בדיקה
- [ ] כיתוב: שורה ראשונה עם הוק, מילות מפתח (שם הכלי, "AI video"), 3–5 האשטגים
- [ ] סימון AI הופעל
- [ ] אישור כתוב לכל אדם אמיתי שמופיע או שפניו שימשו רפרנס
- [ ] אין לוגו של צד שלישי שמשתמע ממנו חסות בתוכן **ממומן**; Paid partnership סומן
- [ ] Cover נבחר
- [ ] גרסת בדיקה הועלתה ל-Close Friends/טיוטה ונצפתה אחרי הדחיסה
- [ ] **ארכיון:** הפרומפטים והרפרנסים שעבדו נשמרו (זה המוצר הבא: מדריך, חבילת פרומפטים, קורס)

---

## 11. סתירות בין העובדים ואיך הוכרעו
| נושא | הגרסאות | ההכרעה |
|---|---|---|
| מספר רפרנסים ב-Genjutsu | 6 (ממשק ברילס, פרק 00/C1) · עד 30 (דף רשמי, C2/C3) · עד 40 (CreativeAINews) | מקסימום רשמי 30; עבודה מעשית עם 3–6 |
| אורך קטע ב-Aleph 2.0 | ~5 ש' (C3, לפי Aleph 1, לא מאומת) · 30 ש' ב-1080p (B1, הודעת Runway) | 30 שניות (מקור רשמי) |
| מחיר 30 שניות 1080p ב-Higgsfield | $11–14 (A1, דרך C2/C4) · 360 קרדיטים = $18 (מחירון 120 קרדיטים ל-10 ש') | מתקצבים לפי $18 (‏55 ₪); $11–14 [לא מאומת] |
| מחיר 1080p ב-Seedance 2.5 | $0.60/ש' (Higgsfield) · ~$1.16/ש' (fal; תוקן מ-$1.36, שהוא בערך מחיר העריכה ב-1080p) | שני המחירים נכונים לספקים שונים; משווים ספקים לפני פרויקט |
| מחירי Runway | $12/$28/$76 (C3) · $15/$35/$95 (B1) | אומת: שנתי ($12/$28/$76) מול חודשי ($15/$35/$95), runway.com/pricing |
| Sora 2 | מופיע בטבלאות וב-meta-prompt של C1 | הוסר; הוחלף ב-Gemini Omni Flash (B1) |
| אורך קליפים קטנים | 5–8 ש' (C1) · 3–8 ש' (C3) | 3–8 שניות; מינימום פלט 4 ש' |
| 30 שניות בטייק אחד או פיצול | C2: עדיף טייק רב-שוטי לעקביות · C1/C3: קליפים קטנים | Image→Video: לנסות 30 ש' ב-480p, לפצל אם נכשל. V2V ואינסוף זוויות: תמיד קטן |
| דיבור עברי מהמודל | C1: אפשר שורת דיאלוג עברית בפרומפט · B1: אין עדות לעברית טבעית | עברית = צילום אמיתי + V2V + אודיו מקורי; עברית בפרומפט = ניסוי |
| דחיסת IG | C4: ~1080p · C3: 720p | לא משנה את ההחלטה: 1080p מספיק, אין צורך באפסקייל |
| שער המרה | 3.6–3.7 אצל העובדים | 3.04 בכל הפרק |
| מספר הפרומפטים בספרייה של C1 | הכותרת: 34 · בפועל: 37 | 37, כולם בנספח, עם תוספות מ-C2/C3 |

---

## נספח א': ספריית הפרומפטים, לפי פורמט

> ברירת מחדל: Seedance 2.5, ‏9:16. מחליפים את מה שבסוגריים מרובעים. המספור המקורי של C1 (1–37) נשמר לצורך מעקב; תוספות מ-C2/C3 מסומנות באות. הפרומפטים לא נבדקו בייצור [לא מאומת כתוצאה]. עבור כל אחד: טסט 480p קודם, ואז 1080p.

### A. רכב ויוקרה (Image→Video)
**1. Dubai supercar, תמונה אחת (30 שניות):** ראו סעיף 4.7.

**1b. Dubai, גרסה מרובת רפרנסים (C2):**
```
References: The driver is @Image1 (front face) and @Image2 (left 3/4 profile) — a man
in a black suit. The car is @Image3, a yellow Lamborghini. The style reference is @Image4
(warm desert golden-hour grade, light haze).
Vertical 9:16, 30 seconds, cinematic luxury car commercial, no dialogue, engine sound and music.
0:00-0:06 Aerial dive from the Burj Khalifa spire down to street level, the yellow car
picked out on the right side of frame.
0:06-0:09 Side profile of the car, camera holds, the car accelerates past camera, exiting frame.
0:09-0:12 Cockpit view from the passenger side: the driver's face clearly visible, calm
confident expression, city lights reflecting on the glass.
...
0:27-0:30 Locked-off 3/4 static shot, the car drives through and past frame.
Preserve the exact face and hairstyle of the driver from @Image1 and @Image2, and the
exact body shape, color and badge of the car from @Image3 in every shot.
```

**3. Night-drive cinematic (10 שניות):**
```
A matte-black Porsche 911 GT3 cruises through rain-soaked Tel Aviv at night. 0-3s: low tracking shot at wheel height, neon reflections streaking across the wet bodywork. 3-6s: hard cut, interior over-the-shoulder of the driver, dashboard glow on his face, 35mm. 6-10s: drone pulls up and back from the car at a traffic light, city lights spreading out, ends locked-off. Audio: flat-six exhaust burble, rain on glass, no music. No text on signs, no extra cars in lane.
```

**4. Car reveal מתחת לכיסוי:**
```
A silk cover slides off a red Ferrari in a dark concrete studio. Single overhead softbox, everything else black. Camera: slow 90° orbit at headlight height, 50mm, ending on the front three-quarter. The silk ripples and pools on the floor with real weight. Dust particles glow in the light beam. Audio: fabric whoosh, one deep bass hit as the headlights flick on, then silence. No logos, no text.
```

### B. הפקה היברידית (Video→Video, Genjutsu / Seedance Edit)
**2. Rolls-Royce "פייק עשיר", גרסת @-binding (C1):**
```
@Video1 = original performance, blocking, timing and Hebrew dialogue — keep identical, including lip movement. @Image1 = Hotel de Paris Monte-Carlo facade (location look only). @Image2 = black Rolls-Royce Phantom (vehicle only).
Same video, but the underground parking garage becomes the grand entrance of @Image1 at golden hour, the small blue car becomes the Rolls-Royce from @Image2, and the friend in a T-shirt becomes a uniformed chauffeur in a black suit and white gloves. Keep every gesture, the door opening and the cash falling to the ground. Warm luxury grade, 35mm. Audio: keep original voices; add soft fountain ambience and distant traffic. No on-screen text.
```
**2b–2c. ביט A וביט B (C3):** ראו סעיף 6.3. **2d. CHANGE/PRESERVE (C2):** ראו סעיף 6.2.

**2e. הקצאת 6 המשבצות של Genjutsu לפי תרחיש (C2):**
| משבצת | A: "פייק עשיר" (חניון ← מונטה קרלו) | B: פרסומת מוצר עם שחקן (Object Swap) | C: "עולם חדש" (רכבת תחתית) |
|---|---|---|---|
| Ref 1 | אתה, פנים קדמי (מאותו יום) | packshot קדמי, תווית קריאה | אתה, פנים |
| Ref 2 | אתה, גוף מלא בלבוש היעד (צילום או Nano Banana) | מוצר 3/4 | אתה, גוף מלא בבגד היעד |
| Ref 3 | השחקן השני (נהג): פנים + חליפת נהג | מוצר מלמעלה/אחורי | ניצב/דמות (ליצן) |
| Ref 4 | Rolls-Royce Phantom שחורה 3/4 קדמי, packshot שנוצר במודל תמונה | פני השחקן | ניצב/דמות (אביר) |
| Ref 5 | כניסת מלון יוקרה בלילה (`grand Belle Époque hotel entrance at night, Monaco style`), בלי לוגו אמיתי | הסביבה | ניצב/דמות (כלב) |
| Ref 6 | אביזר hero: שעון זהב, שטרות, מזוודת עור | style ref (צבעי המותג) | לוקיישן (קרון רכבת) |

פרומפט לתרחיש B:
```
Object Swap: replace the plain bottle in my hand with the product from Ref 1–3, keep my hand grip, motion and timing; keep label facing camera when held up.
```

**2f. מסטודיו ריק לרכבת תחתית / 2g. סלון ← פנטהאוז:** ראו סעיף 6.5.

**17. Apartment virtual staging (V2V):**
```
@Video1 = original walkthrough (camera path and timing — keep identical). @Image1 = interior style reference (Scandinavian minimal, oak and linen) — style only.
Same walkthrough, but the empty apartment is fully furnished in the style of @Image1: linen sofa, oak dining table, plants, warm lamps. Keep walls, windows, floor plan and camera path exactly as in @Video1. Bright daylight from windows. Audio: quiet room tone. No people, no text.
```

**33. Superhero reveal (V2V, בסגנון Genjutsu):**
```
@Video1 = original performance in an empty living room (keep motion, timing and face identical).
Same video, but at 3s, as he clenches his fist, a liquid-metal armor ripples outward from his chest and covers his whole body in 1.5 seconds; the living room becomes a rooftop at night over a neon city. Camera move identical to @Video1. Audio: metallic flowing SFX, deep bass impact, wind on the rooftop.
```

### C. Infinite Angles (Seedance 2.5 Edit)
**37. בריף קצר ל-Claude + פורמט הפלט:** ראו סעיף 6.4 (רשימת rourke, ה-meta-prompt הייעודי ודוגמת הפלט). מייצרים בקטעים של 3–8 שניות.

### D. מוצר (Product hero)
**8. Perfume hero:**
```
@Image1 = perfume bottle (shape, glass color, cap) — must match exactly; label legible and unchanged.
A crystal perfume bottle stands on wet black obsidian. Camera: slow 180° orbit at bottle height, 100mm macro, ending front-on. A single drop runs down the glass; at 4s a burst of golden mist sprays in slow motion, backlit so every droplet sparkles. Hard rim light from behind, soft fill from the left, deep black background. Audio: soft glass chime, mist hiss, low ambient pad. No extra bottles, no text.
```
**9. Sneaker splash:**
```
A white running sneaker drops into a shallow pool of water in extreme slow motion, 1000fps look. Crown-shaped splash rises around the sole, droplets frozen mid-air. Camera locked-off at ground level, 85mm, shallow depth of field. Bright studio key from above, clean gradient grey backdrop. Audio: deep whoosh, single splash impact, silence. Shoe shape identical to @Image1, no logo distortion.
```
**10. Skincare UGC-style hero:**
```
Close-up of a woman's hand pumping a white serum bottle (@Image1, label legible) onto her fingertips in a bright bathroom, soft window light. 0-3s: macro of the golden serum drop. 3-6s: medium close-up, she pats it onto her cheek, dewy skin texture, natural pores visible. 6-8s: rack focus from her face to the bottle on the marble sink. Audio: gentle pump click, soft bathroom ambience, no music.
```
**11. Tech product levitation:**
```
Wireless earbuds case (@Image1) floats and slowly rotates above a matte white plinth. Lid opens by itself, the earbuds rise out and hover, soft blue LED pulse. Camera: slow push-in, 85mm, ending on the open case. Clean Apple-style studio, high-key light, soft shadow under the plinth. Audio: subtle magnetic click, airy whoosh, minimal electronic tone. No text, no extra devices.
```
**12. Beverage pour:**
```
Ice cubes tumble in slow motion into a tall glass, then amber cold brew pours in, swirling with cream. Condensation beads run down the glass. Camera: locked-off side view, 100mm macro, backlight through the liquid creating a warm glow. Speed ramp: real-time pour, slow motion on the cream swirl. Audio: ice clinks, liquid pour, fizz. No logos.
```
(ל-start frame של מוצר: פרומפט ה-packshot בסעיף 3.7. לנאמנות תווית: התבנית בסעיף 4.4.)

### E. אוכל
**13. Burger build:**
```
Top-down overhead shot of a gourmet burger assembling itself layer by layer on a wooden board: brioche bottom, lettuce, smash patty with dripping cheddar, tomato, pickles, top bun pressed down. Each layer drops in with real weight and a small bounce. Warm practical light, steam rising from the patty. Audio: sizzle, soft thuds on each layer. Ingredients do not morph, no plastic look.
```
**14. Israeli street food (שווארמה):**
```
Handheld street-food documentary style. 0-3s: macro of a shawarma spit turning, fat glistening, knife shaving thin slices. 3-6s: hard cut, the cook's hands stuff a fluffy pita with meat, tahini drizzle, pickles and amba. 6-9s: medium shot, he hands it across the counter toward camera with a grin. Warm evening light, neon sign glow. Audio: sizzling, knife scraping, street chatter in Hebrew, no music.
```
**15. Cheese pull ASMR:**
```
Extreme close-up, 100mm macro: a slice of pizza is lifted from the pan, stretchy mozzarella pulling in long glossy strands, steam rising. Camera slow pull-up following the slice, ending on the cheese strands snapping. Warm side light from a window, shallow depth of field. Audio: ASMR crisp crust crackle, cheese stretch, no music.
```

### F. נדל"ן
**16. Villa drone reveal:**
```
Luxury villa with infinity pool overlooking the Mediterranean at golden hour. 0-5s: FPV drone glides low over the pool surface toward the glass facade, reflections rippling. 5-9s: the drone flies through the open sliding doors into a double-height living room. 9-14s: crane up inside to reveal the mezzanine and ocean view behind. 14-18s: pull-out back over the terrace, sun on the horizon, locked-off. Wide 16mm, warm natural light, interior practicals on. Audio: soft waves, gentle piano. No people, no text.
```
**18. Penthouse day-to-night:**
```
Locked-off wide shot, 16mm, from the corner of a penthouse living room facing floor-to-ceiling windows over a city skyline. Time-lapse from late afternoon to blue hour to night over 10 seconds: sunlight shadows sweep across the floor, then interior lamps switch on and city lights twinkle outside. Camera completely still. Audio: soft city hum, no music.
```
(17, ‏virtual staging מצילום, נמצא בקטגוריה B.)

### G. אופנה
**19. Runway walk:**
```
@Image1 = model identity. @Image2 = outfit (oversized cream wool coat, wide trousers) — exact.
The model walks toward camera down a concrete runway, coat flowing with real weight behind her. Camera: low-angle backward tracking, 50mm, ending in a medium close-up as she stops and turns her head. Hard top light, black background, light haze. Audio: heels echoing, deep pulsing beat. Fabric lags behind motion, no face drift.
```
**20. Outfit transition (snap/spin):**
```
A young woman in a plain grey hoodie spins once in front of a white wall; on the spin at 2s a match cut reveals her in a sequined black evening dress, then on the second spin at 5s in a red tailored suit. Camera locked-off, medium-wide, 35mm. Bright ring-light key. Audio: whoosh on each spin, upbeat pop beat, cut on the beat. Same face and hair in every look.
```
**21. Editorial street fashion:**
```
Paris street at golden hour, 35mm film look, Portra 400 grain. A man in a camel overcoat and sunglasses crosses a cobblestone street toward camera. Camera: slow lateral tracking from left to right, ending on his profile as he lights a cigarette-free silver lighter. Warm low sun from behind, long shadows, gentle flare. Audio: street ambience, distant accordion. No text.
```

### H. לפני ואחרי
**22. Room makeover:**
```
Locked-off wide shot of a messy, dim student bedroom. At 3s a smooth left-to-right wipe transforms it into a clean, modern bedroom with warm LED strips, plants and a made bed; the camera position never changes. Then slow push-in toward the new desk setup. Audio: whoosh on the wipe, cozy lo-fi beat. Same room geometry, same window.
```
**23. Fitness transformation** (בזהירות, בלי הבטחות בריאותיות):
```
@Image1 = man's face identity. Split screen, top and bottom, 9:16. Top: the man from @Image1 in a gym, confident, lifting a dumbbell, hard side light. Bottom: the same man months earlier on a couch, dim TV light. Both halves move in sync: he turns his head toward camera at 3s. Audio: motivational beat building. Face identical in both halves.
```
**24. Car detailing:**
```
Macro close-up on a dusty, swirled black car hood. A gloved hand sweeps a microfiber cloth from left to right; everything behind the cloth becomes a deep mirror-gloss finish reflecting the sky. Camera slow tracking alongside the hand, 85mm. Overcast soft light. Audio: cloth swish, satisfying squeak. Same car panel shape.
```
(Start/End frame לטרנספורמציה של חדר: סעיף 3.7.)

### I. דרמה קולנועית
**25. Thriller one-take** (מצוטט מ-[Atlabs](https://www.atlabs.ai/blog/ultimate-seedance-2.5-prompting-guide-2026)):
```
A man in a charcoal three-piece suit walks the length of a hotel lobby at night, marble floor, brass fittings, moody amber tungsten light. 0s to 8s: steadicam follow from behind as he crosses the floor, staff turning to watch him pass. 8s to 18s: he pushes through the brass doors into the street, whip pan to reveal a crowd of photographers, flashbulbs strobing. 18s to 30s: slow push in on his face, half smile, rack focus to the marquee behind him. Sound is crowd murmur, camera shutters, distant traffic, no music.
```
**26. Emotional two-hander (בסגנון Veo):**
```
[00:00-00:03] Medium two-shot, 35mm: an elderly man and his adult daughter sit on a park bench at golden hour, not looking at each other.
[00:03-00:06] Close-up on the daughter, 85mm: she says, "I should have called more." Her voice cracks.
[00:06-00:08] Close-up on the father, he exhales, takes her hand without looking.
Ambient noise: wind in leaves, distant children playing. SFX: a single bird call. Warm backlight, soft lens flare, gentle film grain.
```
**27. Arctic epic (בסגנון ANERNEQ):**
```
GLOBAL STYLE: photochemical epic, IMAX 65mm look, fine grain, halation, 2.39:1, no music, no subtitles.
SCENE: An Inuit hunter returns to a tent village during a blizzard at night.
0-6s: extreme wide, the hunter is a tiny silhouette against aurora borealis, snow streaking horizontally.
6-12s: hard cut, medium tracking shot alongside him, fur hood frosted, breath freezing, firelight from the village ahead on his face.
12-18s: close-up, he kneels by the fire, ice cracks off his gloves, eyes wet.
PHYSICS: snow accumulates on his shoulders and never resets; fur lags with wind.
AUDIO: howling wind, crackling fire, footsteps crunching. Face identical across shots.
```

### J. וולוג POV
**5. POV historical vlog:**
```
Handheld selfie-vlog POV, smartphone wide lens, 9:16. A young Roman legionary in dusty armor holds the camera at arm's length and walks through a bustling Roman market in 50 AD, grinning. Dialogue (legionary, casual, out of breath): "Okay guys, day three of the campaign, and the bread here is honestly overrated." Background: merchants shouting, a goat crosses behind him, sunlight bouncing off white stone. Natural handheld shake, slight motion blur. Audio: crowd chatter, sandals on stone, no music.
```
**6. POV first-person action (GoPro):**
```
First-person POV from a chest-mounted GoPro, fisheye. Hands grip the handlebars of a mountain bike racing down a narrow forest trail at speed, roots and rocks flashing past, sunlight strobing through the trees. Real vibration, mud spatter hits the lens at 4s. Audio: heavy breathing, tires on dirt, wind, no music.
```
**7. "A day in the life" (רב-שוטי, 15 שניות; שורת העברית ניסיונית, ראו 4.5):**
```
@Image1 = the creator's face only.
0-3s: POV hand turns off a phone alarm at 5:00 AM, dim blue room light.
3-6s: hard cut, mirror selfie MCU, the man from @Image1 ties his tie, window light from camera left.
6-10s: handheld walk-and-talk on a Tel Aviv street at sunrise, phone held at arm's length, he says: "בוקר טוב, יום ראשון של הסטארטאפ."
10-15s: over-the-shoulder at a laptop in a café, steam rising from coffee, slow push-in to the screen.
Audio: street ambience, coffee machine hiss, light lo-fi beat. Face identical in every shot.
```

### K. UGC
**31. UGC testimonial (Veo / Seedance):**
```
Vertical selfie video, front phone camera, slightly handheld, natural window light, a woman in her late 20s sits in her car in a parking lot. She holds up a small lip-oil tube (@Image1, label legible) toward the lens and says, excited but casual: "Okay, I didn't expect this to last through a whole day of meetings — but look." She tilts her head to show glossy lips. Audio: car interior ambience, no music. Authentic, unpolished, no on-screen text.
```
**32. UGC unboxing:**
```
Top-down POV of hands opening a matte black box on a wooden desk; tissue paper rustles, revealing a smartwatch (@Image1, exact design). Hands lift it toward camera, screen lights up. 0-3s unbox, 3-6s lift, 6-8s rack focus to the watch face. Soft daylight. Audio: ASMR paper rustle, click of the box, soft "wow" from off-screen. Hands hold the product firmly.
```

### L. חיות
**28. Talking-cat podcast:**
```
A grumpy orange tabby cat sits in a tiny podcast studio, headphones on, in front of a professional microphone. Medium close-up, 50mm, warm practical lights and an "ON AIR" glow behind. The cat leans in and says, in a deep tired voice, "Let's be honest. Monday was a mistake." Mouth moves in sync, whiskers twitch. Audio: room tone, slight mic pop, no music.
```
**29. Wildlife documentary:**
```
Telephoto 600mm, nature documentary look. A snow leopard stalks along a rocky Himalayan ridge at dawn, muscles shifting under thick fur, breath visible. Camera: slow lateral tracking, ending as the leopard stops and looks directly into the lens. Soft pink dawn backlight, mist in the valley. Audio: wind, distant raven, soft paw steps on stone. No humans, realistic anatomy.
```
**30. Absurd animal influencer:**
```
A sphynx cat with a human body in a tailored navy suit walks confidently through a busy Milan street at noon, holding an iced coffee, pedestrians do a double take. Camera: backward tracking at chest height, 35mm, handheld gimbal float. Bright midday sun. Audio: street chatter, footsteps, trending upbeat track. Realistic street, photoreal fur texture.
```

### M. משפיען AI ו-VFX
**35. AI influencer, נעילת דמות לסדרה:**
```
@Image1 = character sheet of "Noa" (front, 3/4, profile) — identity only. Reference strength ~75%.
Noa, 24, wavy auburn hair, freckles, oversized beige knit, sits cross-legged on a sunlit balcony in Jaffa with a coffee. Medium close-up, 50mm, handheld micro-drift. She looks at camera and says: "Today I'm testing every bakery on this street. Ranking at the end." Golden morning light from camera right. Audio: street below, birds, no music. Face identical to @Image1, no makeup change.
```
**36. Dance trend motion-transfer (Kling / Genjutsu):**
```
@Video1 = dance choreography and timing only — do not copy the dancer's appearance or room. @Element1 = AI influencer character (identity and outfit).
@Element1 performs the exact choreography from @Video1 on a Tel Aviv beach promenade at sunset, full body wide shot, camera locked-off at chest height. Hair and clothes follow the motion with real weight. Audio: keep the trend's beat from @Video1. Negative: no sliding feet, no distorted hands, no face drift.
```
**34. Element morph:**
```
Locked-off medium shot: a woman stands still in a desert at sunset, then from her feet upward her body dissolves into swirling golden sand that blows away in the wind, revealing the empty landscape behind. Particles have real weight and drift. 85mm, warm backlight, heavy haze. Audio: wind rising, sand hiss, single low drone note.
```
(33, ‏Superhero reveal, נמצא בקטגוריה B.)

---

## מה עושים עם זה – צעדים מעשיים

**שבוע 1: לבנות את התשתית (3–4 שעות, כ-60 ₪)**
1. צלמו את ה-**Self Reference Kit** שלכם (סעיף 3.4): 8 תמונות, אותו יום, קיר אפור, אור חלון. הריצו Anchor portrait ו-Character sheet (סעיף 3.7) ושמרו בתיקייה "LOCKED".
2. קנו חצובה עם תפסנית (50–100 ₪) ומיקרופון דש (100–250 ₪).
3. פתחו Claude Project עם ה-**meta-prompt הכללי** (סעיף 4.9) ו-Project שני עם ה-**meta-prompt של Infinite Angles** (סעיף 6.4).
4. התקינו Heebo/Rubik, Whisper ו-CapCut. בנו פעם אחת תבנית Split ותבנית Prompt Reveal (סעיף 7.4–7.5) ושמרו כ-template. מי שמייצר בכמות: סקריפט ה-ffmpeg.

**שבוע 2: שלושה רילסים ראשונים (תקציב AI של כ-300 ₪)**
5. **Prompt Reveal "אני בדובאי"** מתמונה אחת: רשימת שוטים ← Claude ← Seedance 2.5 ב-480p (~4.6 ₪ ל-10 ש') ← 1080p (~18 ₪ ל-10 ש') ← פריסת INPUT + PROMPT ← CTA "תגיבו דובאי".
6. **Reality-Swap בעברית** עם חבר בחניון (סעיף 6.3): 2 ביטים, Genjutsu, אודיו מקורי, כתוביות צרובות. תקציב: ~119 ₪ ב-AI.
7. **Infinite Angles** על עסק של חבר (בית קפה, מספרה): טייק נעול אחד, קליפים של 3–8 שניות, ‏480p ואז 1080p.
8. לפני כל פרסום: **רשימת ה-QA** (סעיף 10.2), כולל בדיקת bidi, תיוג AI, ובדיקת אוטומציית ה-DM בחשבון בדיקה.

**שבוע 3 ואילך: להפוך לשירות ולמוצר**
9. את 3 הרילסים הופכים ל**דמו מכירה**. תמחור התחלתי לפי טבלה 6.7 (1,200–6,000 ₪ לפרויקט) מול עלות AI של 82–329 ₪. הפיץ' הכי חזק לעסקים: Object Swap, "5 גרסאות מוצר מצילום אחד".
10. שלחו ללקוחות את **טקסט הבקשה המוכן** (סעיף 3.5) וקבלו אישור כתוב לשימוש בדמות. בתוכן ממומן: בלי לוגואים של מותגי צד שלישי.
11. **ארכבו כל פרומפט ורפרנס שעבד** (עם עלות ומספר ניסיונות). אחרי 10–15 פרויקטים זו חבילת פרומפטים בעברית או פרק בקורס, ו-meta-prompt שמור הוא נכס למכירה.
12. **אל תבנו על מודל אחד.** השוק מתחלף כל 4–8 שבועות (B1). בנו על ה-workflow: רפרנסים עם תפקיד ← timeline מתוזמן ← 480p ← 1080p ← V2V ← עריכה. עקבו אחרי ה-changelog של Higgsfield, Kling ו-Runway ופרסמו מדריך בתוך 24–72 שעות מכל השקה.
13. **פתוח לבדיקה בשטח** (לא אומת במחקר): האם Genjutsu שומר את האודיו המקורי בפלט; איכות תמלול עברי ב-CapCut וב-DaVinci; מחירי Lovart ו-Higgsfield העדכניים; איך נראית שורת דיאלוג עברית ב-Seedance 2.5. כל אחד מאלה הוא גם רילס ("בדקתי בשבילכם").

---

## בדיקת עובדות (Fact-check)

> נבדק ב-05.10.2026 מול מקורות רשת עדכניים (עדיפות לתיעוד רשמי). עובדות שמקורן בפרק 00 (ניתוח הרילס) לא נבדקו מחדש.

| טענה | פסק דין (אומת / תוקן / לא מאומת) | מקור |
|---|---|---|
| Seedance 2.5: עד 30 שניות לג'נרציה, פלט 4–30 ש' | אומת | [fal](https://fal.ai/models/bytedance/seedance-2.5/image-to-video), [Higgsfield changelog](https://higgsfield.ai/creator-hub/changelog) |
| Seedance 2.5: רפרנסים 30 תמונות / 10 וידאו / 10 אודיו (50) | אומת | [Kapwing](https://www.kapwing.com/resources/how-to-use-seedance-2-5-a-guide-for-ai-video-creators/), [OpenRouter](https://openrouter.ai/blog/insights/seedance-2-5-review) |
| Seedance 2.5: ‏24fps קבוע; יחסי מסך 21:9 עד 9:16 | אומת | [fal](https://fal.ai/models/bytedance/seedance-2.5/image-to-video) |
| Seedance 2.5: 480/720/1080p; חלק מהספקים רק עד 720p | אומת | fal, Higgsfield, [seedance.tv](https://www.seedance.tv/blog/seedance-2-5-1080p-not-available) |
| 1080p ב-Higgsfield הוא "early access" ולא ב-Unlimited | לא מאומת | דף Higgsfield לא מציין זאת |
| וידאו קלט ב-Seedance: ‏1.8–30.2 ש', ≤200MB, ‏24–60fps, MP4/MOV | אומת | [fal multi-angle](https://fal.ai/learn/tools/how-to-create-multi-angle-video-seedance-2-5) |
| Higgsfield Seedance 2.5: ‏10 ש' = 30/70/120 קרדיטים ($1.5/$3.5/$6), קרדיט $0.05 | אומת | [Higgsfield](https://higgsfield.ai/blog/seedance-2-5-on-higgsfield-2026) |
| fal Seedance 2.5 ‏1080p ≈ $1.36/ש' | תוקן ל-~$1.16/ש' (480p $0.22, 720p $0.47 אומתו) | [fal](https://fal.ai/models/bytedance/seedance-2.5/image-to-video) |
| מצב Edit = ×0.6 ממחיר יצירה | לא מאומת (בדוגמת fal עריכה ב-1080p ≈ $1.36/ש') | [fal multi-angle](https://fal.ai/learn/tools/how-to-create-multi-angle-video-seedance-2-5) |
| fal: ‏13 זוויות מטייק של 20 ש'; טסט 480p ≈ $5, ‏1080p ≈ $27 | אומת ($5.18 / $27.40) | [fal multi-angle](https://fal.ai/learn/tools/how-to-create-multi-angle-video-seedance-2-5) |
| Draft Mode ‏480p ב-Higgsfield מ-22.09 | אומת | [Higgsfield changelog](https://higgsfield.ai/creator-hub/changelog) |
| Genjutsu: קלט 4–30 ש', פלט עד 1080p | אומת | [Higgsfield](https://higgsfield.ai/blog/higgsfield-genjutsu) |
| Genjutsu: עד 30 תמונות רפרנס | אומת (6 משבצות בממשק שברילס, ההסבר לפער לא מאומת) | [Higgsfield](https://higgsfield.ai/blog/higgsfield-genjutsu) |
| Genjutsu: ‏15 ש' = 40 / 104 / 144 קרדיטים ($2 / $5.2 / $7.2) | אומת | [Higgsfield](https://higgsfield.ai/blog/higgsfield-genjutsu) |
| Genjutsu מצבים: Motion Transfer, Object Swap (01.09), Restyle (30.09), ‏`/genjutsu` ב-ChatGPT (30.09) | אומת | [Higgsfield changelog](https://higgsfield.ai/creator-hub/changelog) |
| Genjutsu: טיפול באודיו / lip-sync | לא מאומת (לא מתועד בדף הרשמי) | [Higgsfield](https://higgsfield.ai/blog/higgsfield-genjutsu) |
| AI Influencer ‏(02.10), cashback ב-API ‏($15 אחרי $100, עד 20%), All Unlimited ‏(20.07) | אומת | [Higgsfield changelog](https://higgsfield.ai/creator-hub/changelog) |
| Runway Aleph 2.0: עד 30 ש' ב-1080p, כל התוכניות בתשלום | אומת | [Runway](https://runway.com/news/introducing-aleph-2-and-edit-studio) |
| Aleph 2.0: ‏28 קרדיטים/ש' | אומת (140 קרדיטים ל-5 ש'; API ‏$0.01 לקרדיט) | [runway.com/pricing](https://runway.com/pricing) |
| מחירי Runway ‏$12/$28/$76 מול $15/$35/$95 | אומת: שנתי מול חודשי | [runway.com/pricing](https://runway.com/pricing) |
| Kling 3.0: עד 6 שוטים, 15 ש', ‏4K native | אומת (4K ב-API מ-23.04.2026); ‏60fps לא מאומת | [Atlabs](https://www.atlabs.ai/blog/kling-3-0-prompting-guide-master-ai-video-generation), [CineD](https://www.cined.com/kling-3-0-ai-video-model-introduced-native-4k-) |
| Kling O1 Edit: קלט 3–10 ש', ‏720–2160px, עד 4 רפרנסים, `keep_audio` כבוי, $0.168/ש' | אומת | [fal](https://fal.ai/models/fal-ai/kling-video/o1/video-to-video/edit) |
| Veo 3.1: קליפ 4–8 ש'; Ingredients עד 3 | אומת (4/6/8; ‏1080p/4K ורפרנסים רק 8 ש'; Extend של 7 ש' עד 148 ש' ב-720p) | [Google AI docs](https://ai.google.dev/gemini-api/docs/veo) |
| Gemini Omni Flash 1.1: ‏3–10 ש', שרשור עד 40, ‏1–10 תמונות, ‏1080p/4K הם upscale מ-720p, draft ב-360p | אומת | [Segmind](https://blog.segmind.com/gemini-omni-1-1-flash-features-examples-and-1-0-compared/), [aicybr](https://aicybr.com/blog/gemini-omni-1-1-flash-video-api-guide) |
| Gemini Omni 1.1: הוסר video ref | לא מאומת (מקורות סותרים: Runware ו-aicybr מתעדים עד 3 קליפי רפרנס) | [Runware](https://runware.ai/docs/models/google-gemini-omni-flash-1-1/guides/reference-driven-video) |
| Lovart: Seedance 2.5 זמין, עד 30 ש' | אומת; תמחור לא מאומת | [Lovart](https://www.lovart.ai/landing/seedance_2_5) |
| Premiere Pro: אין תמלול עברי | אומת (בקשות פתוחות, אפריל 2026) | [Adobe Community](https://community.adobe.com/feature-requests-730/hebrew-voice-transcription-support-in-premiere-pro-1328496) |
| מנויי Higgsfield: Starter ~$19 / Plus $47–59 / Ultra $99–129 | לא מאומת מול האתר הרשמי (תואם Creatify, 08.2026) | [Creatify](https://creatify.ai/blog/higgsfield-pricing-(2026)-plans-and-what-you-ll-actually-pay) |
| Instagram: ‏1080×1920, H.264, ‏23–60fps, ‏8–15 Mbps, AAC ‏48kHz ≥128k | אומת (מקורות משניים) | [Argil](https://argil.ai/blog/instagram-reel-size-e350f) |
| CapCut Pro: ‏$19.99 לחודש / $179.99 לשנה | אומת | [nemovideo](https://www.nemovideo.com/blog/capcut-pro-pricing-2026) |
| Topaz Video ~$299 לשנה; Astra ‏$39 לחודש ($19 במבצע) / $328 לשנה | אומת | [MyArchitectAI](https://www.myarchitectai.com/blog/topaz-ai-pricing), [Renderahouse](https://www.renderahouse.com/blog/topaz-ai-pricing) |

---

## מקורות

**פנימיים:** `chapters/00-visual-analysis.md` (ניתוח פריימים ותמלולים); `workers/C1.md`, `C2.md`, `C3.md`, `C4.md`, `B1.md`, ובאמצעותם `A1.md`, `A2.md`; `assets/frames/dubai_prompt.png`, `assets/frames/DdwEiL4KzVS.jpg`.

**פרומפטים ומודלים**
- Higgsfield: https://higgsfield.ai/blog/seedance-2-5-prompting-guide · https://higgsfield.ai/blog/seedance-2-5-on-higgsfield-2026 · https://higgsfield.ai/changelog · https://higgsfield.ai/creator-hub/changelog · https://higgsfield.ai/genjutsu · https://higgsfield.ai/blog/higgsfield-genjutsu
- Runway: https://runway.com/resources/seedance-2-5-prompt-guide · https://runway.com/resources/seedance-2-0-prompt-guide · https://runway.com/resources/ai-character-references-tips · https://runway.com/news/introducing-aleph-2-and-edit-studio · https://runway.com/research/introducing-runway-aleph · https://runway.com/pricing
- Kapwing: https://www.kapwing.com/resources/how-to-prompt-seedance-2-5-a-guide-for-ai-video-creators/ · https://www.kapwing.com/resources/how-to-use-seedance-2-5-a-guide-for-ai-video-creators/
- Atlabs: https://www.atlabs.ai/blog/ultimate-seedance-2.5-prompting-guide-2026 · https://www.atlabs.ai/blog/kling-3-0-prompting-guide-master-ai-video-generation
- https://www.heyuan110.com/posts/ai/2026-07-11-seedance-2-prompt-guide/
- https://www.mindstudio.ai/blog/timeline-prompting-seedance-2-cinematic-ai-video · https://www.mindstudio.ai/blog/seedance-2-5-multimodal-reference-system-explained
- https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1 · https://frameo.ai/blog/google-veo-3-prompt-guide-best-practices/ · https://ai.google.dev/gemini-api/docs/pricing
- fal: https://fal.ai/learn/tools/how-to-create-multi-angle-video-seedance-2-5 · https://fal.ai/learn/devs/seedance-2-5-vs-seedance-2-0 · https://fal.ai/learn/devs/seedance-2-5-prompting-guide · https://fal.ai/models/bytedance/seedance-2.5/image-to-video · https://fal.ai/models/fal-ai/kling-video/o1/video-to-video/edit · https://fal.ai/models/fal-ai/kling-video/v2.6/pro/motion-control
- https://openrouter.ai/blog/insights/seedance-2-5-review · https://www.segmind.com/models/seedance-2.5/pricing · https://blog.segmind.com/gemini-omni-1-1-flash-features-examples-and-1-0-compared/ · https://arena.ai/leaderboard/text-to-video/overall
- https://morphic.com/resources/how-to/seedance-2-5-guide · https://curiousrefuge.com/blog/how-to-change-camera-angles-with-ai-video · https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video · https://lumalabs.ai/news/higgsfield-pricing · https://github.com/ali-vilab/VACE
- https://www.atlascloud.ai/blog/guides/kling-3.0-turbo-vs-kling-3.0 · https://kling.ai/blog/kling-video-3-0-credit-cost-guide · https://creatify.ai/blog/higgsfield-pricing-(2026)-plans-and-what-you-ll-actually-pay · https://creatify.ai/blog/runway-pricing-(2026)-plans-credits-and-what-you-ll-actually-pay
- Sora shutdown: https://engadget.com/ai/openai-is-shutting-down-its-sora-video-generation-app-211023358.html · https://zilliz.com/ai-faq/what-is-the-sora-shutdown-timeline

**רפרנסים ו-V2V**
- https://runware.ai/docs/models/bytedance-seedance-2-5/guides/multi-reference-production · https://docs.evolink.ai/cn/api-manual/video-series/seedance2.5/seedance-2.5-image-to-video.md · https://dreamina.capcut.com/de-de/ai-video/ai-video-reference-inputs-faq
- https://www.creativeainews.com/blog/higgsfield-genjutsu-ai-video-motion-transfer-2026/ · https://www.stork.ai/en/higgsfield-genjutsu · https://www.media.io/video-effects/higgsfield-ai-genjutsu-tutorial.html · https://riffkit.ai/blog/how-to-use-higgsfield-genjutsu · https://www.cachephoto.com/en/cineblog/higgsfield-genjutsu-video-a-video/
- https://magichour.ai/blog/how-to-keep-characters-consistent-in-ai-video · https://capcut.com/create/character-consistency-ai-video-clips-reference-images · https://invideo.io/faq/how-do-you-create-a-character-reference-sheet-using-nano/ · https://selfielabstudio.com/blog/nano-banana-pro-master-character-consistency-prompts-20260302
- https://www.opus.pro/blog/product-photo-to-commercial-seedance · https://www.krea.ai/blog/top-6-ai-video-models-for-ecommerce-ads-in-2026

**עריכה, כתוביות וייצוא**
- אלגוריתם: https://www.socialpilot.co/de/blog/instagram-reels-algorithm · https://www.eclincher.com/articles/how-the-instagram-algorithm-works-in-2026 · https://www.capcut.com/create/short-video-discovery-2026-ai-editing · https://www.clipspeed.ai/blog/short-form-video-statistics-data-2026.html
- פריסות ואזורים בטוחים: https://www.hopperhq.com/blog/instagram-reel-size/ · https://adaptlypost.com/blog/social-media-safe-zones-2026-complete-guide · https://argil.ai/blog/instagram-reel-size-e350f · https://www.capcut.com/create/split-screen-effects-multi-frame-videos · https://thinglabs.io/how-to-put-two-videos-in-one-screen-on-capcut · https://www.capeditcut.com/how-to-use-the-masking-tool-in-capcut-for-creative-video-editing/ · https://www.storyblocks.com/resources/tutorials/make-horizontal-videos-verticle-premiere · https://pixflow.net/blog/edit-youtube-shorts-premiere-pro/
- עברית: https://community.adobe.com/feature-requests-730/hebrew-voice-transcription-support-in-premiere-pro-1328496 · https://community.adobe.com/t5/premiere-pro-discussions/srt-import-with-right-to-left-language-e-g-hebrew-arabic-text-is-reversed/m-p/13592853/highlight/true · https://www.capcut.com/help/auto-captions · https://submagic.co/auto-subtitle-generator/hebrew-subtitles · https://napoleoncat.com/blog/instagram-edits/
- צבע וארטיפקטים: https://invideo.io/faq/what-is-the-best-color-grading-workflow-for-ai-generated/ · https://invideo.io/faq/how-do-you-color-grade-ai-generated-video-clips-to-look/ · https://www.capcut.com/ideas/seedance-2-0-for-color-grading · https://genra.ai/blog/why-ai-videos-look-fake-how-to-fix · https://hackernoon.com/how-to-fix-warped-hands-and-faces-in-ai-generated-video · https://geo.higgsfield.ai/task/blog/which-tool-avoids-flickering-face-ai-video
- אפסקייל ואינטרפולציה: https://www.topazlabs.com/tools/seedance-video-upscaler · https://www.myarchitectai.com/blog/topaz-ai-pricing · https://www.renderahouse.com/blog/topaz-ai-pricing · https://www.buildfastwithai.com/blogs/topaz-astra-2-ai-video-upscaler-prompt-controls · https://community.topazlabs.com/t/optimized-apollo-variant-for-3x-interpolation-9-step-internal-model-and-24-to-60-fps/100359 · https://unifab.ai/resource/topaz-video-ai-frame-interpolation.htm · https://longstories.ai/blog/ai-frame-interpolation-for-youtube-creators
- ייצוא: https://www.shortsync.app/guides/tiktok-video-quality-settings · https://cococonvert.com/blog/video-for-tiktok-format · https://shortsync.app/resources/youtube-shorts-upload-requirements-2026 · https://vidpros.com/capcut-pro-vs-free/ · https://www.eesel.ai/en/blog/capcut-pricing
- סאונד ותיוג: https://www.soundverse.ai/blog/article/ai-music-for-instagram-reels-that-wont-get-muted-0153 · https://www.valueyournetwork.com/en/declare-ia-content/ · https://storrito.com/resources/tiktoks-2026-ai-labeling-rules-and-what-they-signal-for-platform-governance · https://www.makeinfluence.com/en/academy/content-credentials-c2pa-how-platforms-label-ai-assisted-content
- שער: open.er-api.com (USD/ILS = 3.04, 05.10.2026)
