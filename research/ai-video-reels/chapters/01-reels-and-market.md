# פרק 1: הסרטונים והשוק – למה הרילס עובדים, אילו פורמטים אפשר לשכפל, ומה קורה בישראל

> ⚠️ **הערת המפקח:** מחירים, עלויות לרילס, קיבולת חודשית ומחירון לקוחות — **[פרק 10](10-numbers-capacity-pricing.md) הוא מקור האמת** וגובר על כל מספר סותר בפרק זה (ראו טבלת ה-Errata בפרק 10 §5). מדיניות Spec Ads — פרק 10 §4.


> ראש חטיבה A (Reel Forensics & Market) · 05.10.2026
> מבוסס על: `chapters/00-visual-analysis.md` (ניתוח פריים-אחר-פריים של המפקח, **מקור האמת**), ועל דוחות העובדים `workers/A1.md` (ניתוח 10 הרילס), `workers/A2.md` (קטלוג 48 סרטונים ו-30 יוצרים, טקסונומיה) ו-`workers/A3.md` (השוק הישראלי).
> שער המרה: **$1 = ₪3.04** (open.er-api.com, 05.10.2026). כל המחירים בש"ח בפרק חושבו מחדש לפי השער הזה. A3 השתמש ב-3.05, ולכן יש הבדלים קטנים מהדוח שלו.
> מה שלא אומת מסומן **[לא מאומת]**. כשהעובדים סתרו את הניתוח הוויזואלי, הניתוח הוויזואלי קובע (ראו סעיף 1.8).

---

## תקציר

1. **האיכות כבר לא היתרון.** Seedance 2.5 ו-Higgsfield Genjutsu מייצרים וידאו קולנועי שרוב הצופים לא יזהו כ-AI ברזולוציית אינסטגרם: פנים עקביות לאורך 30 שניות ו-8 עד 10 שוטים מתמונה אחת, ודיבור עברי מסונכרן בהפקה היברידית. היתרון עבר ל**רעיון, לבימוי (רשימת שוטים מתוזמנת), לצילום הקלט ולהוק**.
2. **ה"מנוע" של הרילס הוא משפך "תגיבו מילה ← קבלו DM".** הוא מופיע בכל 10 הרילס. אצל יוצרים קטנים יש **יותר תגובות מלייקים**: edbert_yienson 24K תגובות מול 19K לייקים (יחס 1.26), maorhani1 יחס 1.68, sidequestpat_ יחס 0.97. הרילס האלה הם מכונות לידים, לא בידור.
3. **ההוק הוא ההשוואה.** ב-7 מתוך 10 הרילס רואים קלט מול תוצאה: מסך מפוצל (מקור למטה, AI למעלה) או "Input + Prompt" על המסך. אף רילס לא נפתח בלוגו או ב"היי חברים".
4. **תזמון הוא חצי מהסוד.** edbert פרסם יום אחרי ש-Seedance 2.5 1080p עלה ל-Higgsfield, ו-sidequestpat_ פרסם ביום ההשקה של Genjutsu Restyle. החלון הוא 24 עד 72 שעות מהשקת פיצ'ר.
5. **מצאנו 20 פורמטים חוזרים** (סעיף 2). הפורמטים של הרילס שהמשתמש שלח (Reality-Swap, Hybrid, Luxury Self-Insert, Infinite Angles) בנויים ללידים ולמכירה. הפורמטים שמביאים את מספרי הצפיות הגדולים (100M ומעלה) הם דמויות וסדרות: ארנבות במצלמת אבטחה (203M), Mini Republic (120M+), Fruit Love Island (35M לפרק).
6. **הכסף האמיתי מגיע מלקוחות, ממוצר משלך וממשפך DM, לא מ-CPM.** TikTok משלמת $0.40 עד $1.00 לאלף צפיות (₪1.2-3.0). Yang Mun, פרסונה של ישראלי, הכניס כ-$213K (כ-₪648K) ב-90 יום ממוצרים דיגיטליים. Genre.ai הפיקה פרסומת ל-Kalshi ב-$2,000 (כ-₪6,080).
7. **השוק הישראלי נמצא שלב אחד מאחור, וזה החלון.** מותגים (H&O, תדיראן, FreeTV, Lusha, Enso, תמנון) כבר מפרסמים ב-AI, אבל **אין כמעט יוצר עברי שעושה "steal my prompt"** בפורמט של edbert/rourke. maorhani1 הוא כמעט היחיד: 3,729 עוקבים ו-19 פוסטים.
8. **מחירי שוק בישראל:** סרטון תדמית רגיל ₪3,000-4,000 + מע"מ; רילס AI בסטודיו קטן ₪1,200-1,290; קורסי וידאו AI ₪1,000-6,000. אין "tripwire" עברי זול (₪99-490) שנמכר מתוך משפך DM.
9. **היתרון של יוצר עברי:** הפקה היברידית. מצלמים דיאלוג אמיתי בעברית, ו-Genjutsu מחליף רק את הוויז'ואל. כך עוקפים את כל בעיות ה-TTS וה-lip-sync בעברית.
10. **ההזדמנות מס' 1:** "פרסומת מונקו" לבעלי עסקים ישראליים (₪2,500-5,000 לסרטון), שנמכרת דרך חשבון אינסטגרם עברי שמפרסם הדגמות בתוך 72 שעות מכל השקה.

---

## 1. למה הרילס האלה עובדים: הדפוסים המנצחים

### 1.1 שני סוגי רילס בערימה
מתוך 10 הרילס, **4 הם רילס של יוצרים** (אנכיים 9:16, 29 עד 60 שניות) ו-**6 הם פרסומות רשמיות של Higgsfield** (רובם אופקיים 16:9, 22 עד 74 שניות, ועוד סרט מלא של 20 דקות). שני הסוגים משתמשים באותו משפך, אבל ביצועים יחסיים שונים לגמרי: יוצר עם 43K עוקבים משיג יותר תגובות מהחשבון הרשמי עם 2M.

### 1.2 טבלת המעורבות של 10 הרילס
(עוקבים נמשכו מ-og:description של אינסטגרם ב-05.10.2026. "חיתוכים" נספרו אוטומטית ב-ffmpeg `scene>0.3`, וזו הערכת חסר.)

| # | ID | יוצר | עוקבים | תאריך | לייקים | תגובות | תגובות/לייקים | לייקים/עוקבים | אורך | יחס מסך | CTA |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [DcDrXjXsLcU](https://www.instagram.com/edbert_yienson/reel/DcDrXjXsLcU/) | @edbert_yienson | 43K | 15.08 | 19K | **24K** | **1.26** | **44%** | 30s | 9:16 | DUBAI |
| 2 | [DclqVvdqvZw](https://www.instagram.com/rourke/reel/DclqVvdqvZw/) | @rourke | 975K | 28.08 | **72K** | 8,635 | 0.12 | 7.4% | 60s | 9:16 | AI |
| 3 | [Dd6gkuVR7jS](https://www.instagram.com/sidequestpat_/reel/Dd6gkuVR7jS/) | @sidequestpat_ | 22K | 30.09 | 3,216 | 3,131 | 0.97 | 14.6% | 29s | 9:16 | ANGLE |
| 4 | [DdyIfcjSm3P](https://www.instagram.com/maorhani1/reel/DdyIfcjSm3P/) | @maorhani1 🇮🇱 | 3,729 | 27.09 | 144 | 242 | **1.68** | 3.9% | 40s | 9:16 | רולס |
| 5 | [DdwEiL4KzVS](https://www.instagram.com/higgsfield.ai/reel/DdwEiL4KzVS/) | Higgsfield (רכבת תחתית) | 2M | 26.09 | 11K | 4,226 | 0.38 | 0.55% | 59s | 9:16 | JUTSU / GENJUTSU |
| 6 | [Ddjk5fCq1VK](https://www.instagram.com/higgsfield.ai/reel/Ddjk5fCq1VK/) | Higgsfield (Hybrid Production) | 2M | 21.09 | 8,746 | 1,467 | 0.17 | 0.44% | 41s | 16:9 | JUTSU |
| 7 | [DeHZl65CI2G](https://www.instagram.com/higgsfield.ai/reel/DeHZl65CI2G/) | Higgsfield (AI Influencer) | 2M | 05.10 | 7,912 | 1,669 | 0.21 | 0.40% | 49s | 16:9 | VIRAL |
| 8 | [DdmkVEgKLE4](https://www.instagram.com/higgsfield.ai/reel/DdmkVEgKLE4/) | Higgsfield (Film Festival) | 2M | 22.09 | 9,688 | 1,321 | 0.14 | 0.48% | 74s | 16:9 | FESTIVAL |
| 9 | [Ddwky9yq-Jt](https://www.instagram.com/higgsfield.ai/reel/Ddwky9yq-Jt/) | Higgsfield (API cashback) | 2M | 26.09 | 3,983 | 1,220 | 0.31 | 0.20% | 22s | 16:9 | API |
| 10 | [Dd1xCWei0CF](https://www.instagram.com/higgsfield.ai/reel/Dd1xCWei0CF/) | Higgsfield (ANERNEQ) | 2M | 28.09 | 4,648 | 2,863 | 0.62 | 0.23% | **20 דק'** | 16:9 | UNLOCK |

**בנצ'מרק:** שיעור המעורבות הממוצע לרילס באינסטגרם ירד ל-0.48% ברבעון 2 של 2026 ([Socialinsider](https://www.socialinsider.io/blog/instagram-reels-engagement/)). אצל edbert **הלייקים לבדם הם 44% מבסיס העוקבים**, בערך פי 90 מהממוצע. כלומר הרילס יצא הרחק מחוץ לבסיס העוקבים, והתגובות ההמוניות דחפו אותו.

**איך לקרוא את יחס התגובות/לייקים:**

| טווח | פירוש | דוגמאות |
|---|---|---|
| מתחת ל-0.15 | צפייה בידורית אורגנית; ה-CTA משני | rourke 0.12, Festival 0.14 |
| 0.15-0.4 | ה-CTA עובד, אבל המוצר עצמו הוא הסיבה לצפייה | 4 רילסים של Higgsfield |
| 0.6-1.0 | ה-CTA הוא חצי מהסיבה לצפייה | ANERNEQ 0.62 ("UNLOCK" לפרומפטים), sidequestpat_ 0.97 |
| מעל 1.0 | **מגנט לידים טהור**: אנשים באים לקבל את הפרומפט/המדריך | edbert 1.26, maorhani1 1.68 |

לפי הדיווחים, ב-2026 האות החזק ביותר באלגוריתם של אינסטגרם הוא "sends per reach" (שיתופים ו-DM), אחריו saves ואחריו תגובות ([Zorcha](https://zorcha.com/blogs/instagram-comment-to-dm-automation/), [Unilink](https://www.unilink.us/blog/instagram-auto-reply)). משפך Comment→DM מייצר **גם תגובה וגם שיחת DM**, כלומר שני אותות בבת אחת, ובנוסף עוקף את הענישה על פוסטים עם קישור חיצוני.

### 1.3 שלוש שיטות העבודה שרואים על המסך
(מתוך הניתוח הוויזואלי, ובתוספת נתונים טכניים מ-A1.)

| שיטה | מה נכנס | מה יוצא | דוגמאות | כלי |
|---|---|---|---|---|
| **1. Image→Video עם פרומפט רב-שוטי מתוזמן** | תמונת פנים אחת + פרומפט עם timecodes | 30 שניות של "פרסומת" שלמה עם 8 עד 9 שוטים | edbert (דובאי/למבורגיני) | Seedance 2.5 1080p ב-Higgsfield. מודל שמייצר עד 30 שניות בטייק אחד ([APIYI](https://docs.apiyi.com/en/live/2026-08/seedance-2-5-launch)) |
| **2. Video→Video "Genjutsu", הפקה היברידית** | צילום טלפון אמיתי (חניון, סטודיו ריק, גרין-סקרין, סלון) + תמונות רפרנס + שורת טקסט | אותה תנועה ואותו משחק בעולם אחר | maorhani1 (רולס), Higgsfield רכבת תחתית, האסטרונאוט, האופנוע | Higgsfield Genjutsu (הושק 01.09.2026): Motion Transfer ו-Object Swap, קלט וידאו של 4 עד 30 שניות (בעמוד AI Influencer כתוב 3-30), עד 30 תמונות רפרנס; רזולוציות 480p-1080p לא מופיעות בעמוד המוצר [לא מאומת] ([higgsfield.ai/genjutsu](https://higgsfield.ai/genjutsu)) |
| **3. "אינסוף זוויות" מקליפ אחד** | טייק אחד מזווית אחת + רשימת זוויות עם timecodes, ש-Claude מרחיב לפרומפט | אותו טייק, כאילו צילם אותו צוות שלם: קלוז-אפ, רחפן, low angle, "בתוך הכוס" | rourke (Lovart × Seedance 2.5), sidequestpat_ (Genjutsu ואז Seedance) | Claude → Lovart/Higgsfield → Seedance 2.5 במצב editing |

### 1.4 שלושה מקרי בוחן מפורטים

**א. edbert_yienson, "Dubai Lamborghini": המודל לשכפול.**
- **הפריסה על המסך לאורך כל 30 השניות:** למעלה הווידאו עם באדג' "HIGGSFIELD SEEDANCE 2.5 1080P"; באמצע "STEAL MY PROMPT · COMMENT 'DUBAI'"; למטה **INPUT** (תמונת פספורט אחת על רקע אפור) ולידה **PROMPT** שגולל יחד עם הווידאו.
- **אין דיבור**, רק סאונד מנוע ומוזיקה. לכן הרילס עובד בכל שפה.
- **למה זה התפוצץ:** (1) תזמון: Higgsfield פתחה את Seedance 2.5 ב-1080p ב-14.08.2026 ([Changelog](https://higgsfield.ai/creator-hub/changelog)), והרילס עלה ב-15.08. (2) פנטזיית עושר אוניברסלית. (3) "אפשר מסלפי": הקלט משעמם והפער לתוצאה עצום. (4) הפרומפט גלוי **חלקית**: מספיק כדי להוכיח שזה אמיתי, לא מספיק כדי לוותר על התגובה.
- היוצר כתב "Inspired by @menezes.ai" (Felipe Menezes, 12K עוקבים). הפורמט עובר מיוצר ליוצר.
- **הפרומפט שנחשף על המסך** (מתומלל מהפריימים; ככל הנראה קודמת לו פסקה שמתארת את הדמות, החליפה השחורה והלמבורגיני הצהובה):
```
0:01-0:13  Descent from the spire tip down toward street level, continuous aerial dive, the yellow supercar picked out and spotlighted on the right side of the frame as it comes into view below.
0:12-0:15  Side view of the car, camera holds a lateral profile position, then the car accelerates and overtakes past the camera, exiting frame.
0:15-0:17  Center rear-view mirror shot, view from inside the cabin looking back through the rear-view mirror, road and skyline receding behind.
0:18-0:19  Front-on view of the car, nose-on framing, grille and headlights facing the camera.
0:20-0:21  Cockpit view of the driver, seen from the right-hand side of the car, face and posture visible through the window/windshield from a right-side angle.
0:22-0:24  Driving on a straight road, camera angled from the rear bumper, 3/4 perspective, car pulling away down the straightaway.
0:25-0:28  Side view of the car again, lateral profile hold, then the car accelerates and passes the camera a second time.
0:29-0:30  Static camera, 3/4 angle, locked-off shot, the car drives through and past frame to close the sequence.
```
- **מה לומדים מהפרומפט:** כל שורה היא שוט אחד שמוגדר בשלושה דברים: **מיקום ותנועת מצלמה**, **מה הרכב או הדמות עושים**, ו**איך השוט נגמר** (exiting frame, pulling away). אין מילים ריקות כמו "epic" או "cinematic". הפתיחה הארוכה (12 שניות של צלילה) "קונה" את ההוק, ושאר השוטים קצרים (1 עד 3 שניות) בקצב של פרסומת רכב. זה תואם להנחיות הרשמיות של Seedance 2.5: "number your shots, one camera setup per beat" ([Kapwing](https://www.kapwing.com/resources/how-to-prompt-seedance-2-5-a-guide-for-ai-video-creators/), [OpenArt](https://openart.ai/de/blog/seedance-2-5-prompt-guide/)).
- **עלות ייצור משוערת:** כ-72 קרדיטים ל-8 שניות 1080p ב-Higgsfield, כלומר כ-270 קרדיט ל-30 שניות, כ-$11-14 (₪33-43) **[לא מאומת ישירות]** ([Krea](https://www.krea.ai/blog/higgsfield-pricing-explained-2026-unlimited-credits-and-real-monthly-costs)).

**ב. rourke, "One clip. Infinite camera angles": מראה את כל זרימת העבודה.**
- **חלק א' (0-22 שניות):** מסך מפוצל. למטה "Original", טייק רחב ונעול של דוכן לימונדה. למעלה "AI Video": לימון באוויר בסלואו-מושן, low angle, טופ-דאון, extreme close-up, **מצלמה בתוך הכוס**, דולי-זום, POV דרך חלון.
- **חלק ב' (22-45 שניות):** ההדרכה. רושמים את ה-timecodes של כל "חיתוך"; מדביקים ב-Claude את הווידאו ורשימה קצרה:
```
00:00 Tracking shot to Rourke / 03:07 Close up slow motion / 05:03 Low angle / 06:14 Top down shot / 08:14 Extreme close up / 14:00 Camera inside the cup / 15:22 tracking shot of the lemonade jug / 20:06 Dolly zoom
Keep the location, dialogue, and actions identical to the original video
```
- **מה ש-Claude החזיר** (נקרא מצילום המסך, A1):
```
Arricam LT, Cooke S4/i primes, 35mm Kodak Vision3 500T, 1.85:1 spherical, T2.8, shallow depth of field, halation on highlights, fine organic grain, lifted milky blacks, low contrast, no sharpening, no HDR.

Golden Driveway grade: sun-bleached lemon yellow as the hero tone, warm cream stucco and red brick house field, sunbaked pale concrete driveway and warm timber board base, soft transparent daylight shadows that never reach true black, dry midday heat shimmer. Handheld with micro-drift, never locked off. Naturalistic performance, real dialogue sync, no music.

[00:00-02.37] Shot 1: Rourke from @Video1 speaks to camera behind the lemonade stand, same performance and dialogue. Straight-on eye level, slow zoom in. Standard prime. Harsh midday sun. Handheld micro-drift easing forward. Hard cut to Shot 2.
[02.37-05.57] Shot 2: The lemon wedge from @Video1 tosses up from Rourke's hand, ramping into deep slow motion as it spins midair. Tight close-up on the tumbling lemon. Close prime, shallow depth of field. Handheld micro-drift, frame effectively still. Hard cut to Shot 3.
```
- **המבנה התלת-שכבתי:** (1) גוף מצלמה + עדשה + פילם, שנותנים ריאליזם קולנועי; (2) "Grade" עם שם, פלטת צבע ואיכות צללים; (3) שוטים ממוספרים עם timecodes מדויקים, ולכל שוט עדשה, תנועת מצלמה ומעבר ("Hard cut to Shot N"). הפנייה לנכסים בתחביר `@Video1`.
- **הטיפ הכי חשוב (מהתמלול):** *"It's not going to give you the perfect generation all in one go. Instead, take small clips and give those to Seedance and adjust the camera angle in incremental clips."* מחלקים את הסרטון לקליפים קצרים ומייצרים כל קטע לחוד.
- **עלות לפי fal.ai** לאותו use-case: כ-$0.26 לשנייה ב-480p לבדיקה (₪0.79), כ-$1.36 לשנייה ב-1080p (₪4.13); עריכה של 20 שניות ב-1080p עולה כ-$27.40 (₪83) ([fal.ai](https://fal.ai/learn/tools/how-to-create-multi-angle-video-seedance-2-5)).
- rourke הוא יוצר לייפסטייל עם 975K עוקבים, לא "יוצר AI". התיוג `@lovart.ai` וה-CTA מרמזים על שיתוף פעולה ממומן **[לא מאומת; אין #ad בכיתוב]**.

**ג. maorhani1, "רולס מול חניון": הנוסחה לשוק הישראלי.**
- **מסך מפוצל לכל האורך:** למעלה Hotel de Paris במונטה קרלו, Rolls-Royce שחורה ונהג בחליפה. למטה המקור: חניון תת-קרקעי, רכב כחול קטן וחבר בטי-שירט. אותה תנועה בדיוק: יציאה מהלובי, פתיחת דלת, "טיפ" (שטרות על הרצפה), "hello mr hani" / "thank you mr hani".
- **החלק השני:** מאור יושב ברכב ומדבר בעברית: "בדיוק סגרנו עסקה עכשיו של מאה מיליון דולר...", "אנחנו הולכים להיות המפיצים הגדולים ביותר בעולם של מכונות מזל לקזינו". **סינכרון השפתיים בעברית נשמר.** הכתוביות צרובות.
- **CTA:** "תגיבו רולס, תעקבו אחריי ואשלח לכם את המדריך" (follow-gate), ומסך "המלא!".
- **כלי:** Higgsfield Genjutsu. הלוגו "Higgsfield + ChatGPT" מופיע כל הזמן. הרילס עלה ב-27.09, לפני ההשקה הכללית של אינטגרציית ChatGPT ב-30.09, ולכן כנראה מדובר בגישה מוקדמת או בשותפות **[לא מאומת]**. Genjutsu מגביל קליפ ל-30 שניות, כך שרילס של 40 שניות הוא לפחות 2 ג'נרציות מחוברות.
- **מה עובד:** עברית, סקיט עם פאנץ' ("פייק עשיר"), פער ויזואלי, הפקה בטלפון עם חבר ורכב רגיל. **מה חסר:** הפצה. 19 פוסטים לא מספיקים כדי שהאלגוריתם ילמד את החשבון.

### 1.5 שאר הרילס בקצרה (מה כל אחד מלמד)
- **sidequestpat_ (Genjutsu + Seedance, 29 שניות, 11 חיתוכים):** הוק של "believe it or not", ובאמצע המשפט wipe הופך סלון לבן ופשוט (חולצה שחורה) לפנטהאוז עם נוף לים (פולו בז', שעון זהב). אחר כך Seedance 2.5 נותן קלוז-אפ על השעון, שוט רחפן, ושוט רחב שחושף "סט צילום" שלא קיים. **שרשור כלים** (סביבה, ואז זוויות). הקהל המוצהר: "If you work in video production... If you have a personal brand... You don't need insane skills... neither a massive budget". תג `#higgsfieldpartner`, ופורסם ביום ההשקה של Genjutsu Restyle (30.09).
- **Higgsfield רכבת תחתית (59 שניות, בלי חיתוכים):** למטה סטודיו לבן עם גרין-סקרין קטן; למעלה אותו שחקן ברכבת מלאה דמויות (ליצן, אביר, דינוזאור, כלב), ברחוב ובשדה קרב. בסוף מוצג הממשק: **Original video + References (6 תמונות) + שורה אחת**: "Same video, but inside a subway." הרילס הרשמי היחיד עם אדם מדבר בפורמט של יוצר, והוא קיבל הכי הרבה לייקים ותגובות מכל הרשמיים. **הלקח: "נראה כמו UGC של יוצר" עדיף על "נראה כמו פרסומת".**
- **Higgsfield Hybrid Production (41 שניות, 16:9):** גרין-סקרין עם מאוורר ונדנדת קפיץ כחולה שהופכים לאופנוע מעופף במדבר; הליכה על קורה שהופכת להליכה על חבל בין גורדי שחקים; אסטרונאוט עם כוס קפה על הירח (product placement); "Space Food"; שלט SALE שמוחלף ("Fix it in post"). הכותרות "FOR LARGE STUDIOS & PRODUCTION TEAMS" ו-"NOW IN API". **זה הפיץ' ל-B2B**: כל זוג לפני/אחרי הוא תבנית לשירות.
- **Higgsfield AI Influencer (49 שניות):** דמויות אבסורדיות (שיער מוגזם, ראש חתול ספינקס בחליפה, ראש צפרדע, שרימפס במדי כדורסל) בסצנות רחוב מציאותיות. ממשק "Character Type" ו-"TRANSFER ANY MOTION WITH GENJUTSU". על המסך מוצגים חשבונות עם **6.4M ו-6.3M** צפיות. הדמות הבולטת דומה ל-@jean_philanthrope (ראו סעיף 3). הכלי הושק ב-02.10.2026 (Changelog): קרדיטים חינם בהרשמה ("5 ג'נרציות" [לא מאומת]), Motion Transfer מתבניות טרנדיות, עד 40 תמונות לסרטון, פלט 1080p ([higgsfield.ai/ai-influencer](https://higgsfield.ai/ai-influencer)).
- **Higgsfield API Cashback (22 שניות):** פתיחה בזווית נמוכה עם בחורה עם ציוד, בילבורד "BEST AI VIDEO MODEL FOR ENTERPRISE", מונה "$20,000,000 CASHBACK POOL / $17,998,344 LEFT", ודוגמנית עם בקבוק ובושם. לפי הכיתוב: עד $200K לעסק / $1,000 ליחיד, בתוקף עד 30.09. **טכניקת FOMO**, וגם רמז שכדאי לספק שירות לעקוב אחרי מבצעי cashback שמורידים את עלות הייצור.
- **ANERNEQ (20 דקות):** דרמה ארקטית עם אש, שלג, דמויות עקביות, כתוביות וזוהר צפוני, בחותמת "HIGGSFIELD CINEMA STUDIO". CTA "UNLOCK" לקבלת הפרומפטים. הסדרה "Higgsfield Originals" כוללת גם את Hell Grind (95 דקות, כ-$500K, מתוכם כ-$400K מחשוב; הוקרן בקאן במקביל לפסטיבל 2026, לא במסגרתו הרשמית ([Wikipedia](https://en.wikipedia.org/wiki/Hell_Grind)); [Variety](https://variety.com/2026/film/features/i-saw-hell-grind-ai-generated-film-cannes-shocking-realistic-1236770720/)) ואת The Cully Hill Boys (110 דקות, כ-$2M; [Crypto Briefing](https://cryptobriefing.com/higgsfield-ai-movie-2m-budget/)). **פרומפטים פתוחים של סרט שלם הם משאב הלימוד הטוב ביותר לפרומפטים ארוכים.**
- **Global Film Festival $1M (74 שניות):** פרודיית MGM עם ילד במקום האריה, "145 COUNTRIES", "OVER 3,000,000 VIEWS ON HIGGSFIELD", שופטים Edwin Catmull ו-Phedon Papamichael. לפי הכיתוב: 67,223 הגשות מ-176 מדינות. פרסים: $500K / $200K / $100K + $100K פרס הקהל + 10 × $10K ([Official Rules](https://higgsfield.ai/contests/higgsfield-global-film-festival?tab=rules)). שימו לב: Higgsfield מקבלת רישיון שיווקי "perpetual, irrevocable" לכל ההגשות, וכל הפרויקטים ציבוריים עם הפרומפטים ([ContentGrip](https://www.contentgrip.com/higgsfield-film-festival-growth/)). כלומר יש ספרייה של עשרות אלפי סרטים עם פרומפטים פתוחים.

### 1.6 עשרת הדפוסים המנצחים (מה לשכפל)
1. **"תראה את הקלט מול התוצאה".** מסך מפוצל או Input+Prompt על המסך, ב-7 מתוך 10 הרילס. ההשוואה היא ההוק, וגם ההוכחה.
2. **"הגב מילה ואשלח לך..."** בכל 10 הרילס. מילה אחת שקשורה לנושא (DUBAI, ANGLE, רולס, JUTSU), לא "LINK" גנרי. היא נשארת בזיכרון ומאפשרת להפריד אוטומציות לפי רילס. ה-CTA מופיע **על המסך לאורך כל הסרטון**, לא רק בכיתוב. ההבטחה קונקרטית ("the full prompt + workflow"). אצל maorhani1 יש גם follow-gate.
3. **הוק ויזואלי בשנייה 0 עד 1.** אף רילס לא נפתח בלוגו או בהקדמה. סוגי ההוקים שעבדו:

| סוג הוק | דוגמה | עיקרון |
|---|---|---|
| תנועת מצלמה קיצונית | צלילה מצריח בורג' ח'ליפה | תנועה אנכית מהירה עוצרת גלילה |
| טרנספורמציה באמצע פריים | wipe בסלון, גרין-סקרין | "רגע, מה קרה?" |
| פער סטטוס | רולס מול חניון | השוואה חברתית |
| דמות מוזרה | פאה ושפם | Pattern interrupt |
| פרודיה מוכרת | לוגו MGM | זיהוי מיידי |
| אובייקט בהילוך איטי | לימון באוויר | יופי ו"איך?" |

4. **כותרת קבועה למעלה עם שם הכלי** ("HIGGSFIELD SEEDANCE 2.5 1080P"). מוסיפה אמינות ומכניסה את הרילס לחיפושים של מי שמחפש את הכלי.
5. **טקסט על המסך בכל רגע**: כתוביות מילה-מילה, או מילה אחת גדולה בכל פעם. רילס בלי דיבור (דובאי, Hybrid, API) עובדים בכל שפה.
6. **פנטזיית עושר וסטטוס** (למבורגיני, רולס, פנטהאוז, שעון זהב): הנושא הוויראלי ביותר אצל יוצרים.
7. **אפקט ה"וואו" הוא הטכנולוגיה עצמה.** הקהל הוא יוצרים ובעלי עסקים שרוצים ללמוד, ולכן הפרומפט והמדריך הם מגנט לידים מושלם.
8. **תזמון השקות:**

| רילס | השקת הכלי | פרסום | פער |
|---|---|---|---|
| edbert (Seedance 2.5 1080p) | 14.08 | 15.08 | +1 יום |
| sidequestpat_ (Genjutsu Restyle) | 30.09 | 30.09 | 0 ימים |
| maorhani1 (ChatGPT ext.) | 30.09 | 27.09 | לפני ההשקה הכללית, כנראה גישה מוקדמת [לא מאומת] |
| AI Influencer (Higgsfield) | 02.10 | 05.10 | +3 ימים |

9. **9:16 ופנים אנושיות בפריים הראשון.** 4 מתוך 6 הרילסים הרשמיים הועלו ב-16:9 עם פסים שחורים בפיד, והם הפסידו לרילס הרשמי האנכי עם אדם מדבר.
10. **אורך:** רילס יוצרים 29 עד 60 שניות; טיזרים מסחריים 22 עד 74 שניות.

### 1.7 מי משלם למי (הכלכלה שמאחורי הרילס)
הרילס האלה הם במידה רבה **פרסומות ממומנות למחצה**. היוצר מרוויח משלושה כיוונים: תשלום מהפלטפורמה, עמלת אפילייט מה-DM וצמיחת עוקבים.

| שחקן | איך מרוויח | מספרים |
|---|---|---|
| Higgsfield | הרשמות ומנויים | ARR של $230M בינואר ו-$500M ביוני 2026, שווי כ-$5B ([36Kr](https://eu.36kr.com/en/p/3933070123089287)); גיוס $400M בשווי $5.4B ([ContentGrip](https://www.contentgrip.com/higgsfield-film-festival-growth/)) |
| יוצר בתוכנית Earn | תשלום לכל וידאו מאושר + בונוס 24 שעות + בונוס יום 7 | עד $1,000 (₪3,040) ביום הראשון ועד $2,500 (₪7,600) לסרטון ([higgsfield.ai/earn](https://higgsfield.ai/earn)); כ-$492K שולמו עד ינואר 2026 ([Joe Youngblood](https://www.joeyoungblood.com/creator-marketing/higgsfield-launched-earn-a-way-for-creators-to-earn-money-with-generative-ai-videos/)); לפי A2 יותר מ-$1M ל-10K+ יוצרים (מקור שיווקי), ובונוסים שבועיים עד $100K ([36kr](https://eu.36kr.com/en/p/3650517574312323)) |
| יוצר אפילייט | עמלה חוזרת | עד 25% ל-12 חודשים; המופנה מקבל עד 50% הנחה ל-3 שעות ([Higgsfield Affiliate](https://higgsfield.ai/blog/higgsfield-affiliate-program-2026)) |
| יוצר גדול (rourke) | דיל חסות ישיר עם Lovart | סכום [לא מאומת] |
| יוצר קטן (maorhani1) | בניית קהל ומכירת מדריך או קורס | — |

**מה נשלח כנראה ב-DM** (הערכה, לא נבדק בפועל): קישור אפילייט לכלי, PDF או Notion עם הפרומפט, או הפניה לקורס/קהילה. כלי האוטומציה: ManyChat, Zorcha או LinkDM, שעובדים דרך ה-API הרשמי של Meta ([Zorcha](https://zorcha.com/blogs/7-best-instagram-comment-to-dm-automation-tools-for-businesses-in-2026/)).

### 1.8 סתירות בין המקורות, ואיך הוכרעו
| נושא | מה נאמר | הכרעה |
|---|---|---|
| מספר תמונות רפרנס ב-Genjutsu | בממשק שברילס רואים **6**; עמוד המוצר מדבר על **עד 30** | שני הנתונים נכונים: הממשק בהדגמה השתמש ב-6, והמגבלה הטכנית היא 30. לעבודה מעשית: 3 עד 6 רפרנסים ממוקדים |
| מונה ה-cashback | A1: "$18,000,000 LEFT" | על המסך (ניתוח ויזואלי): **$17,998,344 LEFT**. A1 עיגל. הסכומים לא אומתו מחוץ לרילס [לא מאומת] |
| הפסטיבל: מדינות | על המסך "145 COUNTRIES"; בכיתוב "67,223 entries from 176 countries" | שני מספרים ממקורות שונים של Higgsfield עצמה. מצטטים את שניהם עם המקור. A1 קרא גם "544 hours of video generated" [לא מאומת] |
| צפיות בחשבונות ברילס AI Influencer | ניתוח ויזואלי: 6.4M ו-6.3M; A1: 8.1M / 7.6M / 3.2M | הניתוח הוויזואלי קובע (6.4M ו-6.3M). המספרים של A1 נקראו כנראה מפריימים אחרים [לא מאומת] |
| השוט האחרון אצל edbert | A1: 0:28-0:30, "חלקי" | ניתוח ויזואלי: **0:29-0:30** |
| מספר השוטים אצל edbert | "9 שוטים" מול 8 שורות timecode | 8 שורות timecode בפרומפט שנחשף. הצלילה הארוכה בתחילתה כוללת למעשה שני "שוטים" (מגדל ואז רחוב) |
| עוקבים של sidequestpat_ | A2: "לא נשלף"; A1: 22K | **22K** (A1 משך בהצלחה) |
| תאריך Seedance 2.5 | A2: יצא 31.07 וב-Higgsfield מ-06.08; A1: 1080p ב-Higgsfield 14.08 | אין סתירה: המודל 31.07, ב-Higgsfield 06.08, גרסת 1080p 14.08 |
| שער המרה | A3: 3.05; עובדים אחרים: 3.6 | **3.04** בכל הפרק |
| Sora 2 | A2 מונה את Sora 2 Cameos בין הכלים | **Sora נסגרה** (אפליקציה 26.04.2026, API 24.09.2026). הדוגמה של Jake Paul היא היסטורית. לא להמליץ |
| שם המשפחה של Yang Mun | A2: "שלו חני (Shalev Hani)"; HeyGen: "Shalev Chani" | אותו אדם בתעתיק שונה. הקשר ל-maorhani1 **[לא מאומת]** |

---

## 2. טקסונומיה: 20 פורמטים שאפשר לשכפל

**מקרא:** **ויראליות** ★ עד ★★★★★ (פוטנציאל צפיות). **קושי** 1 עד 5. **התאמה למונטיזציה** לפי ארבעת המסלולים של המשתמש: (a) לקוחות/מותגים, (b) מוצר משלך, (c) צפיות/תשלומי יוצרים/אפילייט, (d) קורסים/מדריכים. "ישראל" = עד כמה הפורמט פתוח בעברית (הערכה של החטיבה).

| # | פורמט | דוגמאות ומספרים | כלים עיקריים | ויראליות | קושי | מונטיזציה | ישראל |
|---|---|---|---|---|---|---|---|
| F1 | **Reality-Swap לפני/אחרי** (זול מול יוקרה, split-screen או wipe) | [maorhani1](https://www.instagram.com/maorhani1/reel/DdyIfcjSm3P/) (יחס 1.68); [Higgsfield Hybrid](https://www.instagram.com/higgsfield.ai/reel/Ddjk5fCq1VK/) | Genjutsu (Motion Transfer / Object Swap), CapCut למסך מפוצל | ★★★ | 2 | (a) נדל"ן, רכב, מסעדות; (d) מדריך ב-DM | **פתוח לגמרי**; דיבור עברי נשמר |
| F2 | **Hybrid Production** (צילום אמיתי, ו-AI מחליף לוקיישן, דמויות, VFX) | [Higgsfield subway](https://www.instagram.com/higgsfield.ai/reel/DdwEiL4KzVS/) (11K / 4,226); [sidequestpat_](https://www.instagram.com/sidequestpat_/reel/Dd6gkuVR7jS/) | Genjutsu, Seedance 2.5 editing | ★★★ | 3 | **(a) שירות פרסומות** | פתוח; אין ספק ישראלי עם תיק עבודות כזה |
| F3 | **Luxury Self-Insert "I filmed myself"** (דובאי, למבו, יאכטה) | [edbert](https://www.instagram.com/edbert_yienson/reel/DcDrXjXsLcU/) (24K תגובות ב-43K עוקבים); @menezes.ai | Seedance 2.5 1080p (Image→Video), תמונת פנים אחת | ★★★★ | 3 | (c) Earn, אפילייט; (d) | פתוח; עובד גם בלי דיבור |
| F4 | **Infinite Angles / Coverage** | [rourke](https://www.instagram.com/rourke/reel/DclqVvdqvZw/) (72K לייקים) | Claude → Lovart/Higgsfield → Seedance 2.5 | ★★★★ | 2 | (a) B2B לעורכים ולעסקים; (c) שותפויות עם כלים | פתוח |
| F5 | **Tool-Launch Demo + Comment-for-Link** | כל 6 הרילסים של Higgsfield | הכלי שהושק השבוע | ★★ | 1 | (c) אפילייט ו-partner; (d) | **הפער הגדול ביותר בעברית** |
| F6 | **AI Influencer / Persona ריאליסטית** | [@fit_aitana](https://www.instagram.com/fit_aitana/) 404K, עד כ-$11K לחודש (Entrepreneur); [@miazelu](https://www.instagram.com/miazelu/) 283K; [@lilmiquela](https://www.instagram.com/lilmiquela/) 2M | Higgsfield Soul ID / AI Influencer, Nano Banana, Kling | ★★★ | 3 | חסויות, Fanvue/Passes, UGC | בינוני (סיכון אתי); המשביר ניסה "דני" [לא מאומת] |
| F7 | **Absurd Meme Character** | [@jean_philanthrope](https://www.instagram.com/jean_philanthrope/) קליפ של 35.9M, 239K עוקבים מ-10 פוסטים; Italian Brainrot 35M-50M+ | Higgsfield AI Influencer + Genjutsu Motion Transfer | ★★★★★ | 2 | מרצ'נדייז, IP, חסויות (לא meme coin) | פתוח; דמות ישראלית אבסורדית |
| F8 | **Guru / Wisdom Persona** (נזיר, סבא, מאמן) | Yang Mun (@yangmunus), כ-2.5M עוקבים, כ-$213K ב-90 יום | HeyGen, ElevenLabs, LLM לתסריט | ★★★★ | 2 | **(b) ספר, קורס, מנוי** | הוכח על ידי ישראלי (באנגלית). **חובה לגלות שזה AI** |
| F9 | **Cryptid / Character Fake Vlog** (Bigfoot, Yeti, סטורמטרופר) | Big Yowie 35M מ-20 פוסטים; Yeti-Boo 8.6M בשבוע | Veo 3/3.1, Seedance 2.5 עם אודיו | ★★★★ | 2 | (c) creator funds; מכירת פרומפטים ב-Gumroad | אפשרי באנגלית; בעברית הדיבור המסונתז חלש |
| F10 | **POV היסטורי / תנ"כי** ("If Moses had an iPhone") | @holyvlogsz: משה 30M, דניאל 6.1M ב-3 ימים; @timetravellerpov צ'רנוביל 21.8M | Veo 3.1, Seedance 2.5 | ★★★★★ | 2 | (c) creator funds, חסויות | **נישה כמעט ריקה בעברית** (התרשמות, לא נבדק) |
| F11 | **AI Soap Opera / סדרה** (פירות, חתולים) | Fruit Love Island ‏(@ai.cinema021): 35M לפרק 1, 3.1M עוקבים ב-9 ימים, 300M+ לערוץ | Seedance 2.5, Kling 3.0, Nano Banana ל-keyframes | ★★★★★ | 3 | (c) creator funds, חסויות; הצבעות קהל | פתוח; סדרה עברית סאטירית |
| F12 | **Impossible ASMR** | @asmraiworks 11.3M בשבוע; @crackleai 11M ביום | Veo 3, Seedance 2.5 (אודיו מובנה) | ★★★★ | 1 | (c) creator funds | בלי שפה, ולכן גלובלי. הטרנד מתחיל להישחק |
| F13 | **Fake CCTV / מצלמת אבטחה עם חיות** | ארנבות על טרמפולינה (@rachelthecatlovers): 148.8M צפיות ו-18M לייקים ב-2 ימים ([KYM](https://knowyourmeme.com/memes/ai-bunnies-jumping-on-a-trampoline-video)); 203M+ מצטבר [לא מאומת] | Veo / Kling, פילטר "Ring cam" | ★★★★★ | 1 | (c) | גלובלי. **גבול ההטעיה**: לסמן AI |
| F14 | **Miniature World** (אנשים זעירים בעולם שלנו) | Hanlab "Mini Republic" (@haniverse_00): 120M+, לקוחות Nongshim, CJ ENM | Seedance 2.5, Nano Banana | ★★★★★ | 3 | **(a) IP ופרסומות למותגים** | פתוח; פורמט בטוח למותגי מזון ישראליים |
| F15 | **Dialogue Gag** (ראיון רחוב, פודקאסט תינוקות) | ראיון רחוב Veo 14M+; פודקאסט תינוקות 13M [לא מאומת] | Veo 3.1, Seedance 2.5 | ★★★★ | 2 | (c) חסויות | בעברית צריך קול אמיתי או Hybrid |
| F16 | **IP / Celebrity Mashup** | Ruairi Robinson "Tom Cruise vs Brad Pitt" 1.8M; C&D מ-Disney, Netflix ואחרות תוך 72 שעות | — | ★★★★★ | 1 | **אין. סיכון משפטי** | ❌ לא לעשות |
| F17 | **Spec Ad / פרסומת AI** | PJ Accetturo (Genre.ai) ל-Kalshi: פחות מ-$2,000, יומיים, 300-400 ג'נרציות, 3M+ צפיות ב-X בשבוע | Seedance 2.5, Veo 3.1, Kling, ElevenLabs | ★★★★ | 4 | **(a) לקוחות B2B** | Lusha/Enso הוכיחו ביקוש. ספק-אד למותג ישראלי מוכר = תיק עבודות |
| F18 | **AI Short Film / סדרה** | ANERNEQ, Hell Grind (קאן), Santiago | Higgsfield Cinema Studio, Seedance 2.5 | ★★ | 5 | פסטיבלים (פרס ראשון $500K), סטודיו | ויראליות נמוכה ויוקרה גבוהה |
| F19 | **Effect Template** (Earth Zoom Out, ריקוד Motion Control) | #EarthZoomOut 1B+ בהאשטג (מקור שיווקי) | Higgsfield presets, Kling 3.0 Motion Control | ★★★★ | 1 | (c) Earn, לידים | גל של 1-3 שבועות; מהירות היא הכול |
| F20 | **AI Product UGC / TikTok Shop** | Jade roller: 1.2M צפיות, 487 הזמנות, כ-$3 עלות (מקור שיווקי, [לא מאומת]); Daria Simhony | HeyGen, Seedance 2.5, Nano Banana | ★★★ | 2 | (a) רטיינר; (c) עמלות | פתוח לחנויות אונליין ישראליות |

**הפורמטים שמביאים הכי הרבה צפיות לאורך זמן:** F11 (סדרות), F10 (POV היסטורי), F13 (CCTV), F14 (מיניאטורות), F7 (דמות-מם).
**הפורמטים שמביאים הכי הרבה כסף ישיר:** F8 (פרסונת גורו עם מוצר דיגיטלי), F17 ו-F2 (שירות פרסומות), F6 (מנויים).
**הפורמטים של סט המקור (F1-F5)** בנויים ללידים: פחות צפיות, הרבה יותר תגובות ושיחות DM, והם גם תיק העבודות שמוכר ללקוחות.

**דפוסים משותפים לכל הפורמטים:**
1. **פריים ראשון "בלתי אפשרי"** שעוצר גלילה בתוך 0.5 שניות ([Picsart](https://picsart.com/blog/seedance-2-ai-video-trend/)).
2. **ויכוח "האם זה אמיתי?"** מייצר תגובות (ארנבות, Jean Phil, Yang Mun). אבל בשקלול הסיכון עדיף "Real vs AI" גלוי (F1, F2).
3. **דמות חוזרת עדיפה על סרטון בודד** לבניית עוקבים (Fruit Love Island, Big Yowie, Jean Phil). Tool-demo בונה לידים.
4. **מצלמה "לא קולנועית"** (selfie-stick, handheld, Ring-cam) נראית אמינה יותר. גם ANERNEQ מדגיש "natural handheld camera movement".
5. **אודיו כחלק מהסיפור.** Seedance 2.5 ו-Veo מייצרים אודיו באותו pass, וזה הבסיס ל-F9 עד F15.
6. **מהירות על כלים חדשים** (ראו 1.6, דפוס 8).

### 2.1 פרומפטים לדוגמה לשלושת הפורמטים הראשונים לשכפול

**F3, Luxury Self-Insert (מבוסס edbert + rourke; לבדיקה ב-Seedance 2.5, עם תמונת פנים כ-@Image1):**
```
STYLE: Shot on ARRI Alexa 35, Cooke S4/i primes, Kodak Vision3 500T look, 2.39:1, shallow depth of field, natural halation, fine grain, no HDR, no sharpening.
SUBJECT: The man from @Image1 (face and hairstyle only), wearing a tailored black suit.
0:00-0:08 Continuous aerial descent from the top of a skyscraper down to street level, the black supercar picked out on the right side of frame as it comes into view.
0:08-0:12 Side view of the car, camera holds a lateral profile position, the car accelerates and overtakes the camera, exiting frame.
0:12-0:15 Cockpit view of the driver from the passenger side, face and posture visible, city lights sliding across the windshield.
0:15-0:20 Rear bumper 3/4 perspective, car pulling away down a straight coastal road at golden hour.
AUDIO: engine roar, tire hiss, light wind. No music. No dialogue.
CONSTRAINTS: realistic vehicle physics, no morphing, no extra people in the car, consistent face throughout.
```

**F1, Reality-Swap (Genjutsu, Hybrid לעסק ישראלי):**
```
Transform the scene into a luxury Monaco evening: the man exits the Hotel de Paris lobby in a tailored navy suit, a chauffeur opens the rear door of a black Rolls-Royce Phantom. Keep the exact body motion, timing, facial expressions and lip movement of @Video1. Warm golden-hour light, cinematic 35mm, shallow depth of field. Do not add any text or signage in the frame.
```

**F10, POV היסטורי:**
```
Handheld selfie-style vlog, 9:16. A young Israelite man in 1250 BCE, dusty linen robe, holding a smartphone at arm's length, walking between two towering walls of water as the Red Sea parts behind him. He talks excitedly to camera: "Guys, the sea literally just opened up. I'm not joking." Crowd of families with sheep in the background, wind noise, rushing water sound, natural daylight, slight camera shake, realistic skin texture, no text on screen.
```

**פרומפט עזר ל-Claude (הופך תסריט עברי ל-shot list להפקה היברידית):**
```
I have a Hebrew dialogue script for a 30-second vertical ad (below). Produce a timecoded shot list in English (0:00-0:30, 4-6 shots) for a hybrid video-to-video workflow: for each shot describe (1) what I film on my phone in a cheap real location, (2) the target luxury transformation, (3) one-line Genjutsu prompt referencing @Video1. Keep the Hebrew lines untouched; never request on-screen text from the model. Script: <paste Hebrew>
```

---

## 3. נוף היוצרים: מי עושה את זה, ובאילו מספרים

### 3.1 30 יוצרים וחשבונות מרכזיים
(עוקבים עם הסימון "og" נמשכו מאינסטגרם ב-05.10.2026. השאר לפי דיווחי מדיה.)

| # | Handle | פלטפורמה | עוקבים | נישה / פורמט | המספר הבולט | למה ללמוד ממנו |
|---|---|---|---|---|---|---|
| 1 | [@higgsfield.ai](https://www.instagram.com/higgsfield.ai/) | IG | **2M** (og), 496 פוסטים | פלטפורמה | 11K לייקים לרילס הטוב בסט | ספר החוקים של "Comment X for link" |
| 2 | [@higgsfield.creators](https://www.instagram.com/higgsfield.creators/) | IG | **324K** (og), 1,677 פוסטים | רה-פוסט של יוצרים | — | הדרך המהירה לחשיפה: להיות מוצג שם |
| 3 | [@rourke](https://www.instagram.com/rourke/) | IG | **975K** (og), 706 פוסטים | Tool-demo, שותפויות (Lovart) | 72K לייקים | קהל גדול שגובה בשיתופי פעולה עם כלים |
| 4 | [@edbert_yienson](https://www.instagram.com/edbert_yienson/) | IG | **43K** (og), 53 פוסטים | Luxury self-insert | 24K תגובות | הכי מצליח ביחס לגודל |
| 5 | [@menezes.ai](https://www.instagram.com/menezes.ai/) | IG | **12K** (og), 400 פוסטים | Cinematic self-insert | — | המקור של הפורמט של edbert |
| 6 | [@sidequestpat_](https://www.instagram.com/sidequestpat_/) | IG | **22K**, 44 פוסטים | Genjutsu tutorials (טורונטו) | 3,131 תגובות | #higgsfieldpartner רשמי |
| 7 | [@maorhani1](https://www.instagram.com/maorhani1/) 🇮🇱 | IG | **3,729** (og), 19 פוסטים | Before/After בעברית | יחס 1.68 | המתחרה הישיר בשוק העברי |
| 8 | @yangmunus (Yang Mun) / שלו חני 🇮🇱 | IG | כ-2.5M | פרסונת גורו (HeyGen) | כ-$213K ב-90 יום | המשפך המוכח ביותר למוצר דיגיטלי |
| 9 | [@jean_philanthrope](https://www.instagram.com/jean_philanthrope/) | IG | **239K** (og), 10 פוסטים | דמות-מם | קליפ של 35.9M | ויראליות מקסימלית לכל פוסט |
| 10 | Ruairi Robinson | X | — | במאי | 1.8M מפרומפט של 2 שורות | (אבל סיכון IP) |
| 11 | PJ Accetturo / Genre.ai | X/IG | — | סוכנות פרסומות AI | 300M+ צפיות מצטברות | מודל B2B: Nike, LVMH, Qatar Airways, Popeyes, Kalshi |
| 12 | @ai.cinema021 | TT | 3M+ | סדרת פירות | 10M+ לפרק | סדרתיות והצבעת קהל |
| 13 | @trombonechef | TT | — | דרמת אוכל | 26M | יצר את הטרנד שהועתק |
| 14 | @holyvlogsz | TT | 435K | Bible vlogs | 30M | "If X had an iPhone" |
| 15 | @timetravellerpov | TT | 329K | POV היסטורי | 21.8M | כ-20M לסרטון |
| 16 | Big Yowie (Seiji) | TT/IG | כ-490K (IG 278K, TT 151K) | Cryptid vlog | 35M מ-20 פוסטים | שקיפות מלאה בעלויות |
| 17 | @stormtrooper.vlogz | TT | — | IP vlog | 1.2M לייקים ב-13 ימים | (סיכון IP) |
| 18 | Yeti-Boo / @YetiVlogLife | TT | — | ASMR vlog | 28.6M-30M מ-16 פוסטים | — |
| 19 | @asmraiworks / @crackleai | TT | — | AI ASMR | 11M ביום | — |
| 20 | Hanlab / @haniverse_00 | IG | 200K | Miniature IP | 120M+ | IP שהפך לחוזים עם מותגים |
| 21 | @rachelthecatlovers | TT | — | Fake CCTV | 148.8M ב-2 ימים (203M מצטבר [לא מאומת]) | — |
| 22 | [@lilmiquela](https://www.instagram.com/lilmiquela/) | IG/TT | 2M (og) / 3.4M | Virtual influencer | "$10M בשנה" [לא מאומת] | Prada, Calvin Klein |
| 23 | [@fit_aitana](https://www.instagram.com/fit_aitana/) | IG | **404K** (og) | Fitness AI model | עד כ-$11K לחודש ([Entrepreneur](https://entrepreneur.com/business-news/this-ai-fitness-model-makes-11000-a-month/465975)) | מקורות שמדברים על 4.3M שגויים |
| 24 | [@miazelu](https://www.instagram.com/miazelu/) | IG | 283K (og) | Fashion AI | — | עיתוי לאירוע אמיתי (ווימבלדון) |
| 25 | @naina_avtr | IG | כ-376K | AI influencer הודית | €28K לפוסט [לא מאומת] | — |
| 26 | Aze Alter | IG/YT | — | Sci-fi דיסטופי | — | מרצ'נדייז |
| 27 | @Godsaresai | IG/TT | — | נרטיבים של כדורגלנים | — | קהילת Skool ב-$19 לחודש (₪58) |
| 28 | @mrdata_visuals | IG | — | היסטוריה היפותטית | — | קורס Gumroad ב-$79.99 (₪243) |
| 29 | @lucamaxiim | IG | — | Meme narratives | — | קורס $197 (₪599) וביגוד |
| 30 | Hashem Al-Ghaili | FB/IG/YT | 40M+ בסה"כ | מדע ו-AI films | — | קונספטים מדעיים ויראליים |

מקורות ליוצרים 26-29: [Pixflow](https://pixflow.net/blog/how-faceless-channel-creators-earn-without-adsense/). שאר המקורות בטבלת הפורמטים ובסעיף המקורות.

### 3.2 מקרי בוחן בולטים
- **Jean Phil (@jean_philanthrope):** מתאגרף צללים בפריז עם פאה בלונדינית ושפם מסולסל. הופיע ב-17.09.2026, צבר 228K+ עוקבים תוך ימים, וקליפ אחד הגיע ל-35.9M צפיות. הביו קישר למטבע מם JEANPHIL שהגיע לשווי של כ-$8.8M וקרס ב-99% באותו יום ([EarlyGame](https://earlygame.com/news/entertainment/this-influencer-doesnt-exist-jean-phil-leaves-the-internet-fooled)). היום יש לו 239K עוקבים מ-10 פוסטים בלבד. Higgsfield מציגה אותו כהוכחה ש-"every viral AI influencer was made on Higgsfield". **הלקח:** דמות מוזרה ועקבית + Motion Transfer של טרנד = ויראליות. את ה-meme coin לא לחקות.
- **Yang Mun (שלו חני):** נזיר AI שנבנה כולו ב-HeyGen, עם כ-2.5M עוקבים, לקהל בני 25-50. סרטון לוקח כ-20 דקות הפקה, ובזכות ייצור באצוות הקצב עלה לסרטון ביום (פי 7) ([HeyGen case study](https://www.heygen.com/he-il/customer-stories/yangmun)). מוצרים: ספר דיגיטלי $23.99 (₪73; כ-470 בחודש, כ-$11K), קורס $49.99 (₪152), מנטורינג $799 לשעה (₪2,429). כ-$213K (₪648K) ב-90 יום לפי dashboard, והיוצר טוען ל-$300K+ ([instantdm](https://instantdm.com/blog/yang-mun-ai-influencer-digital-product-funnel)). ספג ביקורת חריפה על חוסר גילוי ([Columbia News Service](https://columbianewsservice.com/2026/03/24/millions-found-comfort-in-a-buddhist-monk-but-he-was-never-real/), [EBU Spotlight](https://spotlight.ebu.ch/p/yang-mun-ai-influencer-scam)). **הלקח:** ישראלי בנה מותג גלובלי באנגלית. המשפך עובד, אבל חובה לגלות שמדובר ב-AI.
- **Fruit Love Island (@ai.cinema021):** ריאליטי של פירות (Strawberina, Bananito). פרק 1: 35M צפיות ו-2.7M לייקים; 3.1M עוקבים ב-9 ימים; פרק 15: 39M בשבועיים; 300M+ לערוץ; הצופים מצביעים על העלילה ([The Decoder](https://the-decoder.com/ai-generated-dating-show-pulls-10-million-views-per-episode-on-tiktok/), [The Triangle](https://thetriangle.org/article/the-rise-and-fall-of-fruit-love-island)). הרעיון המקורי של @trombonechef (26M), שהועתק.
- **Big Yowie (Seiji):** 35M צפיות מ-20 פוסטים וכ-490K עוקבים בכל הפלטפורמות, אבל עם Veo 3 Ultra ב-$250 לחודש (₪760) ו-$50-150 לסרטון (₪152-456) **הוא עדיין פועל בהפסד** ("still operating at a loss") מ-creator funds ([Kapwing](https://www.kapwing.com/resources/what-it-takes-to-make-viral-ai-video-content-we-asked-bigfoot/)). זו ההוכחה שצפיות לבד לא מספיקות.
- **Genre.ai / PJ Accetturo:** פרסומת Kalshi ל-NBA Finals: פחות מ-$2,000 (₪6,080) בעלויות פרומפטים, יומיים, 300-400 ג'נרציות ל-15 קליפים, 3M+ צפיות ב-X בשבוע; "95% חיסכון" לא מופיע במקור [לא מאומת] ([OPB/NPR](https://www.opb.org/article/2025/06/23/an-ai-video-ad-is-making-a-splash-is-it-the-future-of-advertising/)). היום הסוכנות עובדת עם Nike, LVMH, Qatar Airways, Oracle, Popeyes, Google ו-Disney ([Wrapbook](https://www.wrapbook.com/on-production-podcast/the-real-economics-of-ai-native-production-featuring-pj-accetturo)).
- **Mini Republic (Hanlab):** פועלים זעירים קוטפים פרי מעולם בני האדם; 120M+ צפיות ו-200K עוקבים, ומזה חוזים עם Nongshim, CJ ENM ו-GS E&C ([KOCCA](https://welcon.kocca.kr/en/directory/content/mini-republic--10139)). דמות או עולם חזותי שהופך ל-IP שמותגים קונים.
- **מקרה אנונימי של AI influencer ב-Passes:** Higgsfield Soul ID + Gemini + ChatGPT + Claude ב-$77 לחודש (₪234); 50K עוקבים ב-30 יום; $12.5K לחודש (₪38K) ביום 90 (מנויים $7.5K, DM בתשלום $3K, PPV $1.5K, חסויות $2K) **(מקור שיווקי, [לא מאומת])** ([AI Journal](https://aijourn.com/?p=533249)).
- **דוגמה שאסור לחקות: "Rabbi Goldman".** "רב" AI עם תוכן אנטישמי, 1.4M+ עוקבים, מכר מדריך "get rich" ב-$9 (מספר הקונים "4,000+" [לא מאומת]). Meta הורידה את החשבון בסוף מרץ 2026 ([Jewish Insider](https://jewishinsider.com/2026/03/a-i-rabbi-goldman-account-removed-instagram-backlash/)).

### 3.3 מפת מונטיזציה: מי מרוויח וכמה
| מודל | דוגמה מוכחת | מספרים (USD / ₪) | פורמטים |
|---|---|---|---|
| **מוצר דיגיטלי דרך משפך DM** | Yang Mun | $213K / ₪648K ב-90 יום | F8, F3, F1, F5 |
| **סוכנות / לקוחות B2B** | Genre.ai, Hanlab | Kalshi: $2,000 / ₪6,080 להפקה; לקוחות Fortune 500 | F2, F14, F17, F20 |
| **מנויים / תוכן בלעדי** | AI influencer ב-Passes | $12.5K / ₪38K לחודש [לא מאומת] | F6 |
| **תוכניות של כלים** | Higgsfield Earn | עד $1K (₪3,040) ביום 1, עד $2.5K (₪7,600) לסרטון | F3, F5, F19 |
| **שותפות / אפילייט עם כלים** | rourke × Lovart, #higgsfieldpartner | עד 25% ל-12 חודשים; סכומי חסות לא פורסמו | F4, F5 |
| **Creator funds** | Big Yowie, Bigfoot | TikTok $0.40-1.00 (₪1.2-3.0) לאלף צפיות | F9-F13 |
| **פסטיבלים ותחרויות** | Higgsfield GFF | $500K (₪1.52M) למקום ראשון | F18 |
| **IP, מרצ'נדייז וקורסים** | lucamaxiim, Godsaresai, mrdata_visuals | $197 / $19 לחודש / $79.99 | F7, F10 |
| **מכירת פרומפטים** | Bigfoot vlog packs ב-Gumroad, גיגים ב-Fiverr | $10-50 (₪30-152) למוצר | F9 |

**אזהרות פלטפורמה ל-2026:**
- **YouTube:** מדיניות "inauthentic content" מ-15.07.2025, גל אכיפה בינואר 2026, וחובת גילוי ל-AI פוטוריאליסטי ([AIR Media-Tech](https://air.io/en/monetization/youtube-monetization-policy-changes-2026-a-complete-dated-timeline)).
- **TikTok:** חובת תווית AI. לפי דיווח, תוכן AI מלא לא כשיר ל-Creator Rewards **[לא מאומת, מקור יחיד]** ([Storrito](https://storrito.com/resources/what-tiktoks-ai-monetization-restrictions-signal-for-creator-income/)). התמיכה של הקהל ב-AI UGC ירדה מ-60% ב-2023 ל-26% ב-2026 (לפי A2).
- **Instagram/Meta:** הורידה את "Rabbi Goldman". חשבונות שמתחזים לאנשים אמיתיים בסיכון. ייתכן שה-CTA של "comment X" ייענש אם התגובות לא "משמעותיות" **[לא מאומת, אין מקור רשמי ל-2026]**.
- **Higgsfield עצמה:** בפברואר 2026 החשבון שלה ב-X הושעה אחרי קמפיין יוצרים אגרסיבי, טענות על deepfakes של סלבריטאים, תוכן גזעני ותלונות על תשלומים חסרים ליוצרים ([The Register](https://www.theregister.com/2026/02/06/higgsfield_ai_job_loss/), [Forbes](https://www.forbes.com/sites/rashishrivastava/2026/02/11/racist-videos-and-payment-problems-the-dark-side-of-this-ai-startups-super-fast-growth/), [Times of Central Asia](https://timesca.com/kazakh-startup-higgsfield-ai-from-unicorn-to-racism-and-sexism-scandal/)). **לא לבנות עסק על פלטפורמה אחת, ולקרוא את תנאי Earn לפני התחייבות.**

---

## 4. השוק הישראלי

### 4.1 התמונה הכללית
השוק הישראלי נמצא **שלב אחד מאחורי השוק העולמי**. מותגים כבר מפרסמים קמפיינים "100% AI", אבל אלה פרסומות טלוויזיה או דיגיטל שהפיקו סוכנויות. **בצד היוצרים כמעט אין מי שעושה בעברית את מה ש-edbert ו-rourke עושים באנגלית.** זה החלון.

### 4.2 המתחרים: יוצרים, סטודיואים, קורסים
**יוצרים ומותגים אישיים:**

| שם | מה עושה | נתונים | איום / לקח |
|---|---|---|---|
| **@maorhani1** (מאור חני) | Reality-Swap בעברית, Genjutsu, משפך "רולס" | 3,729 עוקבים, 669 נעקבים, 19 פוסטים; יחס תגובות 1.68 | המתחרה הישיר היחיד שמצאנו. הפורמט מוכח, ההפצה חלשה. ייתכן שיש לו קשר ל-Higgsfield [לא מאומת] |
| **שלו חני / Yang Mun** | פרסונת AI גלובלית באנגלית, ומלמד את השיטה בקורס | 2.5M+ עוקבים | לא מתחרה על הקהל העברי; מוכיח שישראלי יכול לבנות קהל גלובלי |
| **Too Short for Modeling** (טל רוזנטל ונועם שרון) | סטודיו AI ישראלי שמוכר למותגים אמריקאיים | קמפיין ויראלי ל-Liquid Death ([Globes](https://www.globes.co.il/news/article.aspx?did=1001529974)) | המקבילה הישראלית ל-Genre.ai; מסלול (a) בגרסה הגדולה |
| **LetsAI** (אבי סתר אדרי ומאור אדרי) | מגזין AI עברי, קורסים, WhatsApp, YouTube, TikTok, Telegram | קורס וידאו AI ב-₪2,990, 1,000+ בוגרים לפי האתר; כתבו על Seedance 2 (29.06.2026) ועל Seedance 2.5 Omni-Reference (09.08.2026) | המתחרה החזק ביותר במסלול (d), אבל עובד במאמרים ובקורסים, לא ברילס ויראליים |
| **"המעצבים ב-AI"** (נטלי סדובניק שפיר, סטודיו PNG) | קהילת WhatsApp + זום שבועי | 500+ פעילים; תערוכה "כמעט אמיתי" בת"א (02-03.2026) | בעיקר תמונה, פחות וידאו |
| **Artlist** (חברה ישראלית) | פלטפורמת סטוק + AI | סרט חג מולד: 3 אנשים, 3 שבועות, $3,000 (₪9,120), לעומת $1M, 30 אנשים וחצי שנה; קיצוץ של 85% בתקציב ההפקה ל-2026 [לא מאומת; לא מופיע בכתבה] ([mako](https://www.mako.co.il/nexter-news/Article-16249e6d4955b91027.htm)) | הוכחה שהתעשייה עוברת ל-AI, וגם שיש תגובת נגד |

**סטודיואים וסוכנויות שמוכרים וידאו AI לעסקים:**

| ספק | סוג | מחיר | מקור |
|---|---|---|---|
| **SmartPush** | סטודיו קטן; "סרטון פרסומי AI", רילס, קריינות בעברית/רוסית/אנגלית | **₪1,200-1,290** (באתר: סרטוני תדמית/אנימציה; מחיר נפרד ל"רילס AI" לא נמצא), אנימציה ₪1,200, סרטון מוצר ₪1,200, וידאו לפייסבוק מ-₪1,000 | [smartpush.co.il](https://smartpush.co.il), [ערוץ 7 (ממומן)](https://www.inn.co.il/news/677784) |
| **אקסטרה דיגיטל** | סוכנות דיגיטל (18 שנה; רמי לוי, Lastprice) | לא פורסם. טוענים לחיסכון של 60-80%, "מאות עד אלפי שקלים בודדים" לסרטון סושיאל | [ice, ממומן, 27.05.2026](https://www.ice.co.il/contentpoint-sponsored/news/article/1114491) |
| **KNBL / Kanibal Media** | משרד פרסום | קמפיין H&O | — |
| **Arlo Digital + FLOW** | משרד + פוסט | קמפיין תדיראן | — |
| **Alison.ai** | SaaS לניתוח קריאייטיב ויצירת פרסומות וידאו | גייסו $13.3M (11.2024) | [ice](https://www.ice.co.il/digital-140/news/article/1037737) |

**חברות טכנולוגיה ישראליות** (כלים ושותפים, לא מתחרים): D-ID (אווטארים ו-Video Translate ל-30 שפות), Deepdub (דיבוב AI, 30 שפות ויעד של 60, גיוס $26M, דיבבו את "חטופים" לאנגלית; [Calcalist](https://www.calcalistech.com/ctechnews/article/bl93aqoik)), Canny AI (lip-sync), Lightricks (LTX Studio/LTX Video בקוד פתוח, מחיר עדכני [לא מאומת]), Artlist.

**קורסים בעברית (מתחרים למסלול d):**

| ספק | קורס | מחיר | היקף | כלים |
|---|---|---|---|---|
| LetsAI | יצירת סרטים עם AI | **₪2,990** (עד 10 תשלומים) | כ-50 שעות אקדמיות, כ-100 שיעורים מוקלטים, 30 מפגשי זום (חצי שנה) | ChatGPT, Midjourney, **Higgsfield**, Kling, Veo, HeyGen, **Seedance**, Suno, CapCut ועוד ([letsai](https://letsai.co.il/product/videoai-workshop/)) |
| LetsAI | AI Content Creators (דרך דרושים) | לא פורסם | היברידי | HeyGen, Suno, Kling, Veo, AI influencers ([drushim](https://www.drushim.co.il/academy/4/)) |
| בצלאל, לימודי חוץ | מחוללים סרטים | לא פורסם | 8 מפגשי זום | Claude, Midjourney, Runway ועוד ([study.co.il](https://www.study.co.il/P47514/)) |
| חשיפה, האוניברסיטה הפתוחה | מחולל תמונות ווידאו AI | לא פורסם | 11 מפגשים, 33 שעות | כללי ([study.co.il](https://www.study.co.il/P47207/)) |
| טווח השוק | קורסי AI לסרטונים | **₪1,000-6,000** + ₪200-300 לחודש לכלים | כ-3 חודשים | [study.co.il](https://www.study.co.il/P47148/) |

**מה חסר בנוף:** לא מצאנו יוצר עברי עם קהל משמעותי שמפרסם "steal my prompt" ב-24-72 השעות שאחרי השקת כלי. לא מצאנו מוצר עברי ב-₪99-490. לא מצאנו קורס שמלמד "איך להרוויח": תמחור בש"ח, הצעת מחיר לעסק, משפך comment→DM בעברית ואפילייט. **הסתייגות:** בגלל מכסת החיפוש, טיקטוק העברי לא נסרק לעומק, וייתכן שיש שם יוצרים שלא עלו **[לא מאומת]**.

### 4.3 מותגים ישראליים שכבר משתמשים בפרסומות AI
| מותג | תאריך | מה | מי הפיק | עלות / נתונים | מקור |
|---|---|---|---|---|---|
| **H&O** | 11.2024 | "קמפיין הקמעונאות הראשון בישראל שמבוסס כולו על AI" לשבוע הילדים: דמויות, מנגינה, מילים ודוגמניות AI שלובשות את הקולקציה האמיתית | KNBL (ארט: ולדימיר יודשקין) | לא פורסם | [Ads of the World](https://www.adsoftheworld.com/campaigns/kids-week-campaign-a-first-of-its-kind-ai-initiative) |
| **תדיראן** | 09.03.2025 | קמפיין ה-AI הראשון בענף המזגנים (אפקטים ומושן) | Arlo Digital + FLOW | לא פורסם | [ice](https://www.ice.co.il/advertising-marketing/news/article/1054523) |
| **FreeTV** | 03.10.2025 | פרסומת מוזיקלית בסגנון שיר מחאה עם דמויות AI; ₪44.90 לחודש מול ₪69.90. **ויתרו על משרד הפרסום** | In-house + Green + צוות AI/VFX של 4 | לא פורסם | [ice](https://www.ice.co.il/advertising-marketing/news/article/1085904) |
| **Artlist** | 25.12.2025 | סרט חג מולד (Kling + Nano Banana Pro) | In-house | $3,000 (₪9,120); כ-60K צפיות, פחות מ-400 לייקים, 120+ תגובות, רובן שליליות | [mako](https://www.mako.co.il/nexter-news/Article-16249e6d4955b91027.htm) |
| **Lusha** | 2025 | 2 ספוטים (נציגי מכירות על במה; מהדורת חדשות) | In-house (VP Marketing יעל אבוגסיס) | **$500 (₪1,520)** במקום "מאות אלפי דולרים" | [Globes](https://www.globes.co.il/news/article.aspx?did=1001529974) |
| **Enso** | 2025 | הדמות "נתן", עובד הייטק שהאינבוקס שלו מתרוקן | מיקי חסלבסקי (מנכ"ל) | **$150 (₪456), 6 שעות**; מאות אלפי צפיות ב-LinkedIn וב-YouTube | [Globes](https://www.globes.co.il/news/article.aspx?did=1001529974) |
| **Fiverr** | 2025 | "Nobody Cares"; זהב בגרנות (קטגוריית סרט) | — | — | [Globes](https://www.globes.co.il/news/article.aspx?did=1001530088) |
| **בזק** | 2025 | זהב ב"שימוש הטוב ביותר ב-AI" בגרנות | אדלר חומסקי | — | [Globes](https://www.globes.co.il/news/article.aspx?did=1001530088) |
| **תמנון** | 19.04.2026 | קמפיין פיג'מות (₪50 למבוגר, ₪30 לילד) שנוצר כולו ב-AI, בלי דוגמנים, ושודר בטלוויזיה. "פיילוט; בשנה הקרובה נרחיב משמעותית" | לא צוין | לא פורסם | [ice](https://www.ice.co.il/consumerism/news/article/1110077) |
| **Samsung ישראל** | 03.2026 | "Glitch in Reality" ל-Galaxy S26 Ultra. AI כ**נושא**, לא כשיטת הפקה | אברהם ADV | — | [Ads of the World](https://www.adsoftheworld.com/campaigns/glitch-in-reality) |
| **המשביר / Adidas** | — | משפיען AI בשם "דני" | — | **[לא מאומת]** (המקור מחזיר 410) | [jpost](https://jpost.com/brandblend/article-807616) |

**מה רואים מהטבלה:**
1. **שלושה גלים:** (א) 2024-2025: "הראשונים בענף" (H&O, תדיראן), כשה-AI הוא גימיק יחצ"ני. (ב) סוף 2025: חברות הייטק מפיקות AI בתוך הבית ב-$150-500 (Lusha, Enso). (ג) 2026: קמעונאות המונית בטלוויזיה (תמנון) עם הצהרה על הרחבה. **הגל הבא הוא עסקים קטנים ובינוניים שרוצים "מה שתמנון עשתה" בתקציב של ₪2,000-10,000. זה הלקוח של המשתמש.**
2. **חברות הייטק ישראליות ב-B2B** (Lusha, Enso, Fiverr) הן הלקוח המוכן ביותר: מבינות AI, פונות לקהל אמריקאי באנגלית, משלמות בדולרים ורוצות פורמט ויראלי ל-LinkedIn.
3. **FreeTV ויתרה על משרד הפרסום.** זה איום על הסוכנויות והזדמנות לפרילנסר שמגיע ישר למנהל השיווק.
4. **מחקר BCG** (251 מנהלי שיווק, 03.05.2026): 92% אופטימיים, אבל רק כשליש משתמשים ב-GenAI באופן עקבי מקצה לקצה. 51% רוצים "דוגמאות ROI ברורות". החסמים: חוסר ריאליזם, חוסר אותנטיות, תלות במיומנות הפרומפט ותוצרים גנריים ([Globes](https://www.globes.co.il/news/article.aspx?did=1001541589)). **לכן הפיץ' צריך case study עם מספרים, לא רק "תראה איזה יפה".**

### 4.4 מחירים בש"ח
**נקודות ייחוס מהשוק:**

| פריט | מחיר | מקור |
|---|---|---|
| סרטון תדמית בסיסי (הפקה רגילה) | ₪3,000-4,000 + מע"מ | [מידרג](https://www.midrag.co.il/Content/Tip/11772) |
| הפקה ברמת טלוויזיה | ₪10,000+ | מידרג |
| יום צילום | ₪1,000 (מתחיל) עד ₪2,500 (מנוסה) | מידרג |
| משמרת עריכה (8 שעות) | ₪1,400 | מידרג |
| משמרת גרפיקה / אנימציה | ₪1,000-1,600 | מידרג |
| רילס פרסומי AI (סטודיו קטן) | ₪1,200-1,290 | SmartPush |
| ספוט AI של Lusha (עלות פנימית) | $500 = ₪1,520 | Globes |
| ספוט AI של Enso | $150 = ₪456, 6 שעות | Globes |
| סרט AI של Artlist | $3,000 = ₪9,120 | mako |
| פרסומת Kalshi (Genre.ai, ארה"ב) | $2,000 = ₪6,080 | OPB |
| מנוי צ'טבוט AI לעסק קטן (להשוואה) | ₪700-1,500 לחודש | [Bizportal](https://www.bizportal.co.il/BizTech/news/article/20017062) |
| מנויי כלים לסטודנט וידאו AI | ₪200-300 לחודש | study.co.il |

**עלויות ייצור (כלים):** סרטון של 30 שניות ב-Seedance 2.5 1080p ב-Higgsfield: כ-$11-14 (₪33-43) **[לא מאומת ישירות]**. עריכת זוויות של 20 שניות ב-1080p ב-fal.ai: $27.40 (₪83). בדיקות ב-480p: $0.26 לשנייה (₪0.79). HeyGen Creator: מ-$24 לחודש (₪73).

**מחירון מוצע למשתמש** (הערכת החטיבה על סמך נקודות הייחוס; לפני מע"מ):

| מוצר | מה כולל | מחיר מומלץ | עלות כלים משוערת | הערה |
|---|---|---|---|---|
| **רילס AI בודד** (מוצר בלוקיישן, לפני/אחרי) | רילס אחד של 15-30 שניות, 9:16, כתוביות עבריות, סבב תיקונים אחד | **₪900-1,800** | ₪15-60 (כ-$5-20) | מתחרה ב-₪1,200 של SmartPush, אבל ברמה קולנועית |
| **חבילה חודשית לעסק קטן** | 4-8 רילסים + 3 וריאציות hook לכל אחד, ל-A/B | **₪3,500-7,000 לחודש** | ₪150-400 | המכירה היא על "וריאציות לבדיקה", יתרון של AI שמנהלי שיווק מבינים |
| **"פרסומת מונקו" Hybrid עם בעל העסק** | מצלמים את בעל העסק בטלפון; Genjutsu מעביר אותו לסט יוקרתי, בעברית המקורית שלו | **₪2,500-5,000** לסרטון | ₪50-150 | פורמט maorhani1 לעסקים |
| **ספוט Hero למותג** | 30-60 שניות, תסריט, shot list, מוזיקה, 2-3 גרסאות יחס מסך | **₪8,000-20,000** | ₪300-1,000 | מתחת ל-₪10K+ של הפקה רגילה, וזמן אספקה של ימים |
| **קמפיין מלא** (כמו תמנון/H&O) | ספוט + 10-20 נכסים | **₪25,000-60,000** **[הערכה, אין נתון ציבורי]** | ₪1,000-3,000 | כנראה דרך משרד פרסום; אפשר להציע את עצמך כקבלן משנה |
| **ספוט LinkedIn לחברות הייטק** (באנגלית) | פורמט Enso/Lusha | **$1,000-3,500 (₪3,040-10,640)** | — | משלמות בדולרים, ואין בעיית עברית |
| **קבלן משנה למשרד פרסום** | יום עבודה | ₪1,500-3,000 ליום **[הערכה]** | — | — |
| **שירות "עברית ל-AI"** (כתוביות RTL, קריינות, lip-sync) | לפי דקה | ₪150-400 לדקה **[הערכה]** | — | — |

**כלל אצבע לתמחור:** לתמחר לפי **ערך ומהירות**, לא לפי שעות. לקוח שקרא ש-AI חוסך "60-80%" ישאל "למה זה עולה כמו צילום?". התשובה: "צילום ייקח 3 שבועות ויום צילום. אני נותן לך 5 גרסאות בתוך 72 שעות, ואתה בוחר לפי ביצועים."

### 4.5 פערי העברית (והיתרון שהם יוצרים)
| תחום | המצב | מה לעשות |
|---|---|---|
| **קול עברי (TTS)** | ElevenLabs טוב **רק עם v3 ו-`language_code: "he"`**; multilingual v2 מייצר עברית "unintelligible" ([Hebrew-TTS-Providers](https://github.com/danielrosehill/Hebrew-TTS-Providers)). העמוד מזכיר עכשיו Eleven v4 **[איכות בעברית לא נבדקה]**. MiniMax (דרך Replicate) הכי טוב בשיבוט. Edge TTS (Avri, Hila) חינמי וטוב. Resemble צריך ניקוד; Chatterbox ג'יבריש. ההשוואה ממרץ 2025, ולכן **לבדוק מחדש לפני עבודה ללקוח** | לכתוב מספרים במילים ("ארבעים ותשע תשעים"), לנקד חלקית מילים דו-משמעיות, לבדוק שמות מותגים לועזיים |
| **Lip-sync** | HeyGen תומכת בתרגום לעברית עם lip-sync ([HeyGen Help](https://help.heygen.com/en/articles/11391941-video-translation-languages-we-support)). D-ID: עברית לא אומתה. דיבור עברי שנוצר ישירות ב-Veo / Seedance **[לא מאומת]**; ההערכה היא שהוא פחות טבעי מאנגלית | לייצר קול ב-ElevenLabs/MiniMax ולהכניס אותו כ-audio reference (Seedance 2.5 מקבל עד 10 קבצי אודיו) |
| **כתוביות RTL** | CapCut שובר עברית (סמן קופץ, פיסוק); Descript לא תומכת (399 הצבעות בלי מענה); ב-Premiere דווחו כתוביות הפוכות | לתמלל בכלי חיצוני (CaptionX חינם, Whisper large-v3 או ivrit.ai **[לא נבדקו]**), לתקן SRT ידנית, לצרוב בפונט עבה (Heebo, Assistant, Rubik) בגודל 60-80px על 1080×1920, ולבדוק כל שורה עם מספר או אנגלית |
| **טקסט עברי בתוך הפריים** | המודלים משבשים אותיות עבריות על שלטים ואריזות **[לא נבדק ישירות]**; גם הניתוח הוויזואלי מראה שטקסט ולוגואים קטנים הם נקודת חולשה כללית | לא לבקש מהמודל לכתוב עברית. מוסיפים טקסט בעריכה, או משתמשים במוצר האמיתי כ-reference image |
| **הפתרון: Hybrid בעברית** | מה ש-maorhani1 עשה: דיאלוג אמיתי בעברית, ו-Genjutsu מחליף רק את הוויז'ואל | (1) מצלמים בטלפון סצנה עם דיאלוג עברי; (2) מעלים ל-Genjutsu עם 3-6 רפרנסים (מלון, רכב, חליפה) ושורת פרומפט; (3) התנועה ותנועות הפה נשמרות; (4) צורבים כתוביות; (5) מסך מפוצל מקור/תוצאה |

**למה זה יתרון:** זה עוקף את כל פערי ה-TTS וה-lip-sync, כי ה-AI עושה רק את הוויז'ואל, ושם הוא מצוין. וזה גם המוצר הכי קל למכור: "אתה מדבר בעברית שלך, אבל נמצא בסט של מיליון דולר."

### 4.6 הזדמנויות בשוק הישראלי, מדורגות
הדירוג משקלל ארבעה דברים: גודל הפער (אין מתחרה), זמן להכנסה ראשונה, קושי ביצוע, והתאמה לנכסים של המשתמש (עברית, אינסטגרם).

| דירוג | הזדמנות | למה עכשיו | מודל הכנסה | קושי | זמן להכנסה ראשונה |
|---|---|---|---|---|---|
| **1** | **"פרסומת מונקו" Hybrid לבעלי עסקים** (סוכני נדל"ן, יבואני רכב, מסעדות, מאמני כושר) | maorhani1 הוכיח מעורבות; אין ספק ישראלי עם תיק עבודות כזה; העסקים הקטנים הם הגל הבא אחרי תמנון | ₪2,500-5,000 לסרטון | נמוך-בינוני | 2-4 שבועות |
| **2** | **חשבון "steal my prompt" בעברית** שמפרסם תוך 24-72 שעות מכל השקה (Higgsfield, Lovart, Kling) | אין מתחרה עברי בפורמט; LetsAI כותבים מאמרים, לא רילס. החשבון הוא גם תיק העבודות של הזדמנות 1 | אפילייט Higgsfield (עד 25% ל-12 חודשים) + Earn + מדריכים | בינוני (דורש עקביות יומית) | 1-3 חודשים |
| **3** | **מדריך tripwire ב-₪99-490 + קהילה ב-₪49-149 לחודש** | קורסים קיימים עולים ₪1,000-6,000 ונמשכים 30-50 שעות; אין מוצר כניסה זול שנמכר מתוך DM; קורס מוקלט מתיישן בתוך שבועות | מכירה מתוך DM | נמוך | 1-2 חודשים (צריך קהל) |
| **4** | **ספוטי LinkedIn לסטארט-אפים ישראליים** (באנגלית) | Lusha ו-Enso הוכיחו ROI; ההייטק משלם בדולרים | $1,000-3,500 (₪3,040-10,640) לספוט | בינוני | 1-2 חודשים |
| **5** | **קבלן משנה AI למשרדי פרסום** (KNBL, Arlo, אדלר חומסקי, אברהם) | תמנון "תרחיב משמעותית"; למשרדים חסרים אנשי AI | ₪1,500-3,000 ליום [הערכה] | בינוני-גבוה (צריך תיק עבודות) | 2-3 חודשים |
| **6** | **אסטרטגיה דו-לשונית:** רילס בלי דיבור לקהל גלובלי (פורמט דובאי) + שירותים בעברית מקומית | Yang Mun הוכיח שישראלי יכול לבנות קהל גלובלי; רילס בלי דיבור עובדים בכל שפה | כל המסלולים | בינוני | מקביל ל-2 |
| **7** | **POV היסטורי / תנ"כי בעברית** (F10) | 20M-30M לסרטון בחו"ל; בעברית הנישה כמעט ריקה (התרשמות) | חסויות, creator funds, קהל | בינוני (דיבור עברי מסונתז חלש; עדיף קריינות אמיתית) | 2-3 חודשים |
| **8** | **שירות "עברית ל-AI"** (כתוביות RTL, קריינות מתוקנת, lip-sync) לסוכנויות ויוצרים זרים | פער טכני אמיתי | ₪150-400 לדקה [הערכה] | נמוך | שבועות |
| **9** | **AI influencer עברי** | מותגים כבר ניסו ("דני", לא מאומת) | חסויות | גבוה (אתיקה, תדירות) | 3-6 חודשים |

### 4.7 סיכונים מקומיים
1. **תגובת נגד לפרסומות AI.** הסרטון של Artlist זכה לביקורת קשה. **הפתרון:** להציג את ה-AI כ"קסם" שקוף. המסך המפוצל מראה את האדם האמיתי, ולא מעמידים פנים שזה צילום.
2. **דיפ-פייק של אנשים אמיתיים.** סיון רהב-מאיר "פרסמה" את WhatsApp Business בסרטון מזויף ב-YouTube (14.11.2024) ([סרוגים](https://www.srugim.co.il/1059969-סיון-רהב-מאיר-מבהירה-זה-פייק-זו-בכלל-לא)). **לעולם לא** משתמשים בפנים או בקול של אדם בלי הסכמה בכתב. בעבודת Hybrid לעסק, כל מי שמופיע חותם על אישור שימוש.
3. **סימני מסחר בפריים** (Hotel de Paris, Rolls-Royce, Lamborghini). בתוכן לקוח ממומן זה עלול להיחשב שימוש מסחרי בסימן מסחר **[לא נבדק משפטית; להתייעץ עם עו"ד]**. בתוכן אישי או סאטירי הסיכון נמוך יותר. בפרסומות ללקוחות: רכב "generic luxury" בלי לוגו.
4. **שקיפות ופרסום ממומן.** תוכן ממומן חייב סימון (#ad / Paid partnership), גם בישראל. Higgsfield Earn דורשת גילוי. אין לנו מקור מאומת לחובת סימון "נוצר ב-AI" בישראל נכון לאוקטובר 2026 **[לא מאומת]**, ולכן מומלץ לסמן מרצון.
5. **"עושר מזויף" מול הטעיה.** בתוכן אישי זה הומור. בפרסומת מסחרית אסור להציג מוצרים או נכסים שלא קיימים כאילו הם של העסק.
6. **מחסור בנתוני ROI ישראליים.** לבנות 1-2 case studies עם מספרים (צפיות, לידים, עלות לליד), גם אם זה על העסק של חבר בחינם.

---

## 5. מה עושים עם זה – צעדים מעשיים

**שבוע 1: תשתית ושלושה רילסים ראשונים**
1. **לפתוח מנוי Higgsfield** (Seedance 2.5 + Genjutsu), ולהירשם ל-**Affiliate**, ל-**Earn** ול-**Creator Partnership**. לקרוא את התנאים, ולסמן כל רילס ממומן.
2. **להקים ManyChat** עם מילת מפתח ייעודית לכל רילס. ה-DM כולל: (א) הפרומפט, (ב) קישור אפילייט, (ג) הצעה לשירות או למדריך. לבדוק תצוגת RTL בתוך ה-DM.
3. **רילס 1 – F1 Reality-Swap בעברית:** לצלם עם חבר בטלפון סקיט "פייק עשיר" בחניון, במטבח או במשרד, עם פאנץ' בעברית. להעביר ב-Genjutsu (3-6 רפרנסים + שורה אחת; פרומפט בסעיף 2.1). מסך מפוצל (מקור למטה, AI למעלה), כתוביות צרובות, ו-CTA קבוע על המסך: "תגיבו [מילה] ואשלח לכם את הפרומפט".
4. **רילס 2 – F3 Luxury Self-Insert בלי דיבור:** תמונת פספורט (אור אחיד, רקע נקי) + פרומפט מתוזמן בסגנון edbert. פריסה של INPUT + PROMPT + "STEAL MY PROMPT" על המסך. בלי דיבור, ולכן מתאים גם לקהל גלובלי.
5. **רילס 3 – F4 Infinite Angles:** טייק אחד מחצובה ← רשימת timecodes ← Claude מרחיב (עם "Keep the location, dialogue, and actions identical") ← Seedance 2.5. **לייצר בקטעים קצרים**, לא את כל הסרטון בבת אחת. לבדוק ב-480p לפני 1080p.

**כללי ייצור קבועים**
- 9:16 תמיד, פנים או דמות בפריים הראשון, הוק ויזואלי בשנייה 0-1, בלי לוגו ובלי הקדמה.
- כותרת קבועה עם שם הכלי למעלה, וטקסט על המסך בכל רגע.
- פרומפט: רשימת שוטים קצרה עם timecodes ← LLM מרחיב. לכל שוט: מצלמה, עדשה, תאורה, תנועה, איך השוט נגמר, ומעבר. בלוק "film stock + lens + grade" בראש.
- אף פעם לא לבקש מהמודל טקסט עברי בפריים.

**שבועות 2-3: לקוחות ראשונים**
6. **להציע "פרסומת מונקו" ל-3 עסקים מקומיים** (נדל"ן, רכב, כושר) בחינם או ב-₪500, תמורת זכות פרסום ונתוני ביצועים. להחתים כל מי שמופיע על אישור שימוש. בלי לוגואים של מותגי צד ג'.
7. **לבנות spec ad אחד לסטארט-אפ ישראלי באנגלית** בפורמט Enso/Lusha, לשלוח ל-VP Marketing עם המספרים של Enso (₪456, 6 שעות) ושל Lusha (₪1,520) כעוגן.
8. **לפרסם case study עם מספרים** (צפיות, לידים, עלות לליד) ודף שירות עם המחירון מסעיף 4.4.

**שבוע 4 והלאה: מוצר וסקייל**
9. **מדריך PDF/Notion ב-₪99** לפורמט אחד (למשל "רולס מול חניון ב-Genjutsu"), עם פרומפטים באנגלית והסבר בעברית, שנשלח מתוך ה-DM עם קישור אפילייט. אחר כך קהילה ב-₪49-149 לחודש עם פרומפטים חדשים כל שבוע.
10. **מעקב יומי אחרי ה-changelog** של Higgsfield, Lovart ו-Kling ([Higgsfield changelog](https://higgsfield.ai/creator-hub/changelog)), ופרסום הדגמה בעברית **בתוך 24-72 שעות מכל השקה**.
11. **קצב:** לפחות 3-4 רילסים בשבוע. זו הבעיה של maorhani1, ולא לחזור עליה. לשקול קולאב עם חשבונות גדולים ולשלוח עבודות ל-@higgsfield.creators (324K).
12. **ללמוד מהספריות הפתוחות:** הפרומפטים של ANERNEQ ("UNLOCK"), Hell Grind ועשרות אלפי ההגשות הציבוריות לפסטיבל של Higgsfield.
13. **לגוון פלטפורמות.** לא לבנות עסק רק על Higgsfield, בגלל ההיסטוריה של שערוריות ובעיות תשלום. לשמור גרסה של כל workflow גם ב-Lovart, ב-fal.ai או ב-Kling. לא להשתמש ב-Sora (נסגרה).

**מדדי הצלחה ל-30 הימים הראשונים:** יחס תגובות/לייקים מעל 0.6 ברילסים עם CTA; 3 לקוחות ניסיון עם case study; מכירה ראשונה של מדריך; לפחות רילס אחד שפורסם בתוך 72 שעות מהשקה.

---

## בדיקת עובדות (Fact-check)

> נבדק ב-05.10.2026 מול מקורות ראשוניים ככל האפשר. עובדות שמקורן בניתוח הוויזואלי (`00-visual-analysis.md`) לא נבדקו מחדש (למשל לייקים/תגובות ברילס, המונה $17,998,344, השופטים שמופיעים על המסך). פרופילי אינסטגרם: רק edbert_yienson, sidequestpat_, menezes.ai ו-lilmiquela החזירו og:description; השאר נחסמו (תגובה ריקה) ונשארו כפי שנשלפו קודם.

| טענה | פסק דין | מקור |
|---|---|---|
| @edbert_yienson: 43K עוקבים, 53 פוסטים | אומת | og:description, 05.10.2026 |
| @sidequestpat_: 22K עוקבים, 44 פוסטים | אומת | og:description, 05.10.2026 |
| @menezes.ai: 12K עוקבים, 400 פוסטים | אומת | og:description, 05.10.2026 |
| @lilmiquela: 2M עוקבים | אומת | og:description, 05.10.2026 |
| Seedance 2.5 ב-Higgsfield 06.08; 1080p ב-14.08; Genjutsu 01.09; Genjutsu Restyle ו-ChatGPT 30.09; AI Influencer 02.10 | אומת | [Higgsfield Changelog](https://higgsfield.ai/creator-hub/changelog) |
| Genjutsu: קלט וידאו "3/4 עד 30 שניות", 480p-1080p | תוקן: 4-30 שניות, עד 30 רפרנסים; רזולוציה לא מופיעה בעמוד | [higgsfield.ai/genjutsu](https://higgsfield.ai/genjutsu) |
| AI Influencer: 5 ג'נרציות חינם, עד 40 תמונות | תוקן חלקית: "קרדיטים חינם" ועד 40 תמונות לסרטון; "5" לא מאומת | [higgsfield.ai/ai-influencer](https://higgsfield.ai/ai-influencer) |
| Earn: עד $1,000 ביום הראשון, עד $2,500 לסרטון, בונוסים ב-24 שעות וביום 7 | אומת | [higgsfield.ai/earn](https://higgsfield.ai/earn) |
| Earn: כ-$492K שולמו עד ינואר 2026 | אומת ($491,909, 25.01.2026) | [Joe Youngblood](https://www.joeyoungblood.com/creator-marketing/higgsfield-launched-earn-a-way-for-creators-to-earn-money-with-generative-ai-videos/) |
| אפילייט: עד 25% ל-12 חודשים; המופנה עד 50% הנחה ל-3 שעות | אומת | [Higgsfield Affiliate](https://higgsfield.ai/blog/higgsfield-affiliate-program-2026) |
| Higgsfield ARR $230M (01.2026) ו-$500M+ (06.2026); שווי טרום-כסף $5B | אומת | [36Kr](https://eu.36kr.com/en/p/3933070123089287) |
| גיוס $400M בשווי $5.4B | אומת | [ContentGrip](https://www.contentgrip.com/higgsfield-film-festival-growth/) |
| פסטיבל: $500K/$200K/$100K + $100K קהל + 10×$10K; רישיון perpetual, irrevocable | אומת | [Official Rules](https://higgsfield.ai/contests/higgsfield-global-film-festival?tab=rules) |
| Hell Grind: 95 דק', כ-$500K, "הוקרן בקאן 2026" | תוקן: הוקרן בקאן במקביל לפסטיבל, לא במסגרתו | [Wikipedia](https://en.wikipedia.org/wiki/Hell_Grind), [TechNode](https://technode.com/2026/05/22/bytedances-seedance-2-0-hits-cannes-with-95-minute-ai-film-hell-grind/) |
| The Cully Hill Boys: 110 דק', $2M | אומת | [Crypto Briefing](https://cryptobriefing.com/higgsfield-ai-movie-2m-budget/) |
| חשבון Higgsfield ב-X הושעה בפברואר 2026 | אומת | [tech.az](https://tech.az/en/posts/higgsfield-ai-039-s-x-account-has-been-closed-6558), [Qazinform](https://qazinform.com/amp/scam-claims-and-backlash-hit-kazakhstans-ai-unicorn-higgsfield-b311a7/) |
| Sora: אפליקציה נסגרה 26.04.2026, API 24.09.2026 | אומת | [The Decoder](https://the-decoder.com/openai-sets-two-stage-sora-shutdown-with-app-closing-april-2026-and-api-following-in-september/) |
| מעורבות ממוצעת לרילס 0.48% ברבעון 2 של 2026 | אומת | [Socialinsider](https://www.socialinsider.io/blog/instagram-reels-engagement/) |
| Yang Mun: כ-2.5M עוקבים, $213K ב-90 יום (dashboard), טענה ל-$300K; ספר $23.99, קורס $49.99, מנטורינג $799 | אומת (נתוני הכנסה מדווחים על ידי היוצר) | [instantdm](https://instantdm.com/blog/yang-mun-ai-influencer-digital-product-funnel), [virtualhumans.org](https://virtualhumans.org/article/who-is-yang-mun-the-ai-generated-wellness-guru-with-2-6m-followers) |
| Yang Mun: כ-20 דקות לסרטון, קהל 25-50, היוצר Shalev Hani | אומת | [HeyGen](https://www.heygen.com/he-il/customer-stories/yangmun) |
| Jean Phil: הופיע 17.09, 228K+ עוקבים, קליפ 35.9M, מטבע $8.8M וקריסה של 99% | אומת | [EarlyGame](https://earlygame.com/news/entertainment/this-influencer-doesnt-exist-jean-phil-leaves-the-internet-fooled) |
| Fruit Love Island: פרק 1 35M ו-2.7M לייקים, 3M+ עוקבים, 300M+ לערוץ | אומת (המספר "9 ימים" ו-"פרק 15: 39M" לא נמצאו במקור שנבדק) | [The Triangle](https://thetriangle.org/article/the-rise-and-fall-of-fruit-love-island) |
| ארנבות על טרמפולינה: 203M+ | תוקן: 148.8M ו-18M לייקים ב-2 ימים; 203M מצטבר לא מאומת | [Know Your Meme](https://knowyourmeme.com/memes/ai-bunnies-jumping-on-a-trampoline-video) |
| Big Yowie: כ-450K עוקבים, "הפסיד כסף" | תוקן: כ-490K בכל הפלטפורמות; "still operating at a loss" | [Kapwing](https://www.kapwing.com/resources/what-it-takes-to-make-viral-ai-video-content-we-asked-bigfoot/) |
| Mini Republic: 120M+ צפיות, 200K+ עוקבים, Nongshim, CJ ENM, GS E&C | אומת | [KOCCA](https://welcon.kocca.kr/en/directory/content/mini-republic--10139) |
| Ruairi Robinson: 1.8M צפיות מפרומפט של 2 שורות; C&D מאולפנים תוך 72 שעות | אומת (Disney 13.02, Netflix 17-19.02) | [Let's Data Science](https://letsdatascience.com/blog/bytedances-seedance-2.0-spooked-all-of-hollywood-in-72-hours) |
| Kalshi (Genre.ai): $2,000, יומיים, 300-400 ג'נרציות, 3M+ צפיות; 95% חיסכון | תוקן: "פחות מ-$2,000"; 95% לא מופיע במקור | [OPB/NPR](https://www.opb.org/article/2025/06/23/an-ai-video-ad-is-making-a-splash-is-it-the-future-of-advertising/) |
| fit_aitana: עד $11.5K לחודש | תוקן: עד כ-$11K לחודש | [Entrepreneur](https://entrepreneur.com/business-news/this-ai-fitness-model-makes-11000-a-month/465975) |
| Rabbi Goldman: 1.5M עוקבים, מדריך $9 ל-4,000+, הורד במרץ 2026 | תוקן: 1.4M+; מספר הקונים לא מאומת | [Jewish Insider](https://jewishinsider.com/2026/03/a-i-rabbi-goldman-account-removed-instagram-backlash/) |
| Lusha $500; Enso $150 ו-6 שעות; Too Short for Modeling × Liquid Death | אומת | [Globes](https://www.globes.co.il/news/article.aspx?did=1001529974) |
| H&O 11.2024, KNBL/Kanibal, "קמפיין הקמעונאות הראשון ב-AI" | אומת | [Ads of the World](https://www.adsoftheworld.com/campaigns/kids-week-campaign-a-first-of-its-kind-ai-initiative) |
| תדיראן 09.03.2025, Arlo Digital + FLOW | אומת | [ice](https://www.ice.co.il/advertising-marketing/news/article/1054523) |
| FreeTV: ₪44.90 מול ₪69.90, ויתור על משרד הפרסום, Green + צוות AI של 4 | אומת | [ice](https://www.ice.co.il/advertising-marketing/news/article/1085904) |
| תמנון 19.04.2026, ₪50/₪30, "נרחיב משמעותית" | אומת | [ice](https://www.ice.co.il/consumerism/news/article/1110077) |
| Artlist: $3,000, 3 אנשים, 3 שבועות, כ-60K צפיות; קיצוץ 85% | אומת חלקית: 85% לא מופיע בכתבה | [mako](https://www.mako.co.il/nexter-news/Article-16249e6d4955b91027.htm) |
| BCG: 251 מנהלים, 92% אופטימיים, כשליש עקביים, 51% רוצים ROI | אומת | [Globes](https://www.globes.co.il/news/article.aspx?did=1001541589) |
| LetsAI: ₪2,990, עד 10 תשלומים, כ-50 שעות, כ-100 שיעורים, 30 זומים, 1,000+ בוגרים | אומת | [letsai](https://letsai.co.il/product/videoai-workshop/) |
| קורסי AI לסרטונים ₪1,000-6,000 + ₪200-300 לחודש, כ-3 חודשים | אומת | [study.co.il](https://www.study.co.il/P47148/) |
| מידרג: תדמית ₪3,000-4,000 + מע"מ; יום צילום ₪1,000-2,500; עריכה ₪1,400; גרפיקה ₪1,000-1,600; טלוויזיה ₪10,000+ | אומת | [מידרג](https://www.midrag.co.il/Content/Tip/11772) |
| SmartPush: "רילס פרסומי AI ₪1,200-1,290" | תוקן: המחיר מופיע לסרטוני תדמית/אנימציה; אין מחיר נפרד לרילס AI | [smartpush.co.il](https://smartpush.co.il) |
| Alison.ai גייסה $13.3M ב-11.2024 | אומת | [ice](https://www.ice.co.il/digital-140/news/article/1037737) |
| Deepdub: 30+ שפות, $26M, דיבוב "חטופים" | תוקן: 30 שפות (יעד 60); השאר אומת | [Calcalist](https://www.calcalistech.com/ctechnews/article/bl93aqoik) |

---

## מקורות

**מקורות ראשוניים (המחקר הזה):** `chapters/00-visual-analysis.md` · `00-source-reels.md` · `workers/A1.md` · `workers/A2.md` · `workers/A3.md`

**רילס המקור:** https://www.instagram.com/edbert_yienson/reel/DcDrXjXsLcU/ · https://www.instagram.com/rourke/reel/DclqVvdqvZw/ · https://www.instagram.com/sidequestpat_/reel/Dd6gkuVR7jS/ · https://www.instagram.com/maorhani1/reel/DdyIfcjSm3P/ · https://www.instagram.com/higgsfield.ai/reel/DdwEiL4KzVS/ · https://www.instagram.com/higgsfield.ai/reel/Ddjk5fCq1VK/ · https://www.instagram.com/higgsfield.ai/reel/DeHZl65CI2G/ · https://www.instagram.com/higgsfield.ai/reel/DdmkVEgKLE4/ · https://www.instagram.com/higgsfield.ai/reel/Ddwky9yq-Jt/ · https://www.instagram.com/higgsfield.ai/reel/Dd1xCWei0CF/

**פרופילים (og meta, 05.10.2026):** https://www.instagram.com/higgsfield.ai/ · https://www.instagram.com/higgsfield.creators/ · https://www.instagram.com/rourke/ · https://www.instagram.com/edbert_yienson/ · https://www.instagram.com/sidequestpat_/ · https://www.instagram.com/maorhani1/ · https://www.instagram.com/menezes.ai/ · https://www.instagram.com/jean_philanthrope/ · https://www.instagram.com/lilmiquela/ · https://www.instagram.com/fit_aitana/ · https://www.instagram.com/miazelu/

**Higgsfield, כלים ותמחור:**
- https://higgsfield.ai/creator-hub/changelog
- https://higgsfield.ai/genjutsu
- https://higgsfield.ai/ai-influencer · https://x.com/higgsfield/status/2106119916479037742
- https://higgsfield.ai/earn · https://higgsfield.ai/blog/higgsfield-affiliate-program-2026 · https://higgsfield.ai/creator-partnership-program
- https://higgsfield.ai/blog/higgsfield-api
- https://higgsfield.ai/contests/higgsfield-global-film-festival?tab=rules · https://aifilmcontests.com/guide/how-to-win-higgsfield-global-film-festival-2026
- https://higgsfield.ai/blog/Santiago-breakdown
- https://www.cachephoto.com/en/cineblog/higgsfield-genjutsu-video-a-video/
- https://docs.apiyi.com/en/live/2026-08/seedance-2-5-launch
- https://fal.ai/learn/tools/how-to-create-multi-angle-video-seedance-2-5
- https://www.kapwing.com/resources/how-to-prompt-seedance-2-5-a-guide-for-ai-video-creators/
- https://openart.ai/de/blog/seedance-2-5-prompt-guide/
- https://www.krea.ai/blog/higgsfield-pricing-explained-2026-unlimited-credits-and-real-monthly-costs

**Higgsfield, עסקים ומוניטין:**
- https://eu.36kr.com/en/p/3933070123089287 · https://eu.36kr.com/en/p/3650517574312323
- https://www.contentgrip.com/higgsfield-film-festival-growth/
- https://cryptobriefing.com/higgsfield-ai-movie-2m-budget/
- https://variety.com/2026/film/features/i-saw-hell-grind-ai-generated-film-cannes-shocking-realistic-1236770720/ · https://en.wikipedia.org/wiki/Hell_Grind
- https://www.joeyoungblood.com/creator-marketing/higgsfield-launched-earn-a-way-for-creators-to-earn-money-with-generative-ai-videos/
- https://www.theregister.com/2026/02/06/higgsfield_ai_job_loss/
- https://www.forbes.com/sites/rashishrivastava/2026/02/11/racist-videos-and-payment-problems-the-dark-side-of-this-ai-startups-super-fast-growth/
- https://timesca.com/kazakh-startup-higgsfield-ai-from-unicorn-to-racism-and-sexism-scandal/

**אלגוריתם ומשפכי DM:**
- https://www.socialinsider.io/blog/instagram-reels-engagement/
- https://zorcha.com/blogs/instagram-comment-to-dm-automation/ · https://zorcha.com/blogs/7-best-instagram-comment-to-dm-automation-tools-for-businesses-in-2026/
- https://www.unilink.us/blog/instagram-auto-reply

**יוצרים ופורמטים (A2):**
- https://earlygame.com/news/entertainment/this-influencer-doesnt-exist-jean-phil-leaves-the-internet-fooled
- https://instantdm.com/blog/yang-mun-ai-influencer-digital-product-funnel · https://columbianewsservice.com/2026/03/24/millions-found-comfort-in-a-buddhist-monk-but-he-was-never-real/ · https://www.heygen.com/he-il/customer-stories/yangmun · https://spotlight.ebu.ch/p/yang-mun-ai-influencer-scam
- https://jewishinsider.com/2026/03/a-i-rabbi-goldman-account-removed-instagram-backlash/ · https://www.algemeiner.com/2026/03/29/ai-generated-antisemitic-rabbi-racks-up-millions-of-followers-with-questionable-financial-advice/
- https://success.com/how-ai-influencers-generate-millions-per-year · https://entrepreneur.com/business-news/this-ai-fitness-model-makes-11000-a-month/465975 · https://www.khaleejtimes.com/business/tech/mia-zelu-wimbledon-ai-influencer?amp=1 · https://aijourn.com/?p=533249
- https://tech.yahoo.com/ai/articles/tom-cruise-brad-pitt-fight-181013137.html · https://picsart.com/blog/seedance-2-ai-video-trend/ · https://letsdatascience.com/blog/bytedances-seedance-2.0-spooked-all-of-hollywood-in-72-hours
- https://www.kapwing.com/resources/how-to-make-an-ai-earth-zoom-out-video-higgsfield-ai/ · https://www.kapwing.com/resources/what-it-takes-to-make-viral-ai-video-content-we-asked-bigfoot/
- https://www.complex.com/pop-culture/a/maggie-ekberg/jake-paul-ai-cameo-sora-tiktok-october-2025
- https://knowyourmeme.com/memes/ai-vlogs · https://knowyourmeme.com/memes/ai-asmr · https://knowyourmeme.com/memes/ai-bible-influencer-videos-ai-bible-stories · https://knowyourmeme.com/memes/ai-bunnies-jumping-on-a-trampoline-video
- https://petapixel.com/2025/07/31/people-are-falling-for-an-ai-video-of-bunnies-bouncing-on-a-trampoline · https://petapixel.com/2025/06/03/viral-ai-videos-bring-bible-figures-to-life-as-influencers
- https://argil.ai/blog/ai-videos-that-went-viral-58d69 · https://www.goodreads.com/author_blog_posts/25842167-this-whispering-ai-yeti-is-blowing-up-on-tiktok · https://www.4over4.com/content-hub/stories/bigfoot-ai-goes-viral-your-business-guide-to-this-social-media-gold-mine
- https://jasondeegan.com/two-women-terrify-the-internet-in-a-street-interview-viewers-shocked-by-the-chilling-reason/ · https://www.submagic.co/nl/blog/talking-baby-podcast
- https://thetriangle.org/article/the-rise-and-fall-of-fruit-love-island · https://the-decoder.com/ai-generated-dating-show-pulls-10-million-views-per-episode-on-tiktok/ · https://says.com/my/tech/ai-fruit-dating-tiktok · https://lede-v2.dailydot.com/ai-slop-videos-of-cheating-fruit-are-taking-over-tiktok
- https://highxtar.com/en/the-viral-phenomenon-of-ai-kung-fu-cats-taking-tiktok-by-storm/ · https://welcon.kocca.kr/en/directory/content/mini-republic--10139 · https://www.freemalaysiatoday.com/category/leisure/2025/08/16/italian-brainrot-the-ai-memes-most-adults-dont-know
- https://www.opb.org/article/2025/06/23/an-ai-video-ad-is-making-a-splash-is-it-the-future-of-advertising/ · https://www.wrapbook.com/on-production-podcast/the-real-economics-of-ai-native-production-featuring-pj-accetturo · https://fearlessmediapodcast.buzzsprout.com/1364653/episodes/18604620-advertising-s-top-ai-disruptor-pj-ace-rewriting-the-rules-turning-down-super-bowl-ads
- https://www.weshop.ai/blog/how-ai-video-is-replacing-traditional-ecommerce-content-production-in-2026/ · https://aiweekly.co/alerts/tiktok-shop-sellers-turn-to-ai-avatars-sidelining-creators · https://www.artshub.com.au/?p=2809450
- https://pixflow.net/blog/how-faceless-channel-creators-earn-without-adsense/ · https://www.deutschland.de/en/topic/culture/communication-media/science-explainer-with-seven-million-fans
- https://www.youtube.com/watch?v=aAg9iDh9_BQ
- https://air.io/en/monetization/youtube-monetization-policy-changes-2026-a-complete-dated-timeline · https://storrito.com/resources/what-tiktoks-ai-monetization-restrictions-signal-for-creator-income/

**השוק הישראלי (A3):**
- Globes: https://www.globes.co.il/news/article.aspx?did=1001529974 · https://www.globes.co.il/news/article.aspx?did=1001530088 · https://www.globes.co.il/news/article.aspx?did=1001541589
- ice: https://www.ice.co.il/consumerism/news/article/1110077 · https://www.ice.co.il/advertising-marketing/news/article/1085904 · https://www.ice.co.il/advertising-marketing/news/article/1054523 · https://www.ice.co.il/digital-140/news/article/1037737 · https://www.ice.co.il/contentpoint-sponsored/news/article/1114491
- mako: https://www.mako.co.il/nexter-news/Article-16249e6d4955b91027.htm · https://www.mako.co.il/nexter-news/Article-801df96afe15c91026.htm
- Ads of the World: https://www.adsoftheworld.com/campaigns/kids-week-campaign-a-first-of-its-kind-ai-initiative · https://www.adsoftheworld.com/campaigns/glitch-in-reality
- https://jpost.com/brandblend/article-807616 (410)
- מידרג: https://www.midrag.co.il/Content/Tip/11772 · SmartPush: https://smartpush.co.il · https://www.inn.co.il/news/677784 · https://extra.co.il · Bizportal: https://www.bizportal.co.il/BizTech/news/article/20017062
- קורסים: https://letsai.co.il/product/videoai-workshop/ · https://letsai.co.il/seedance-2-video-model/ · https://letsai.co.il/omni-reference-video-consistency/ · https://www.study.co.il/P47148/ · https://www.study.co.il/P47514/ · https://www.study.co.il/P47207/ · https://www.drushim.co.il/academy/4/
- עברית: https://github.com/danielrosehill/Hebrew-TTS-Providers · https://elevenlabs.io/text-to-speech/hebrew · https://www.heygen.com/text-to-speech/hebrew · https://help.heygen.com/en/articles/11391941-video-translation-languages-we-support · https://caption-x.com/capcut-captions/hebrew · https://feedback.descript.com/feature-requests/p/hebrew-and-rtl-languages-support · https://community.adobe.com/questions-734/hebrew-captions-are-reverse-now-312304
- https://www.calcalistech.com/ctechnews/article/bl93aqoik · https://www.srugim.co.il/1059969-סיון-רהב-מאיר-מבהירה-זה-פייק-זו-בכלל-לא
- שער חליפין: https://open.er-api.com/v6/latest/USD (05.10.2026, ‏3.04)
