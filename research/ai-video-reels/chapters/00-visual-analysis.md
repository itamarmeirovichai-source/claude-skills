# פרק 0: ניתוח ויזואלי של 10 הרילס, פריים אחרי פריים (המפקח הראשי)

> זה המקור הראשוני והאמין ביותר במחקר. כל 10 הסרטונים הורדו במלואם (yt-dlp, 720p/1080p), חולצו מהם פריימים עם חותמות זמן ונבדקו בעין, פריים אחרי פריים. כאן מתועד **מה באמת רואים על המסך**: הרמה, הזרימה והפרומפטים שנחשפים בתוך הסרטונים עצמם.
> רשתות הפריימים: `assets/frames/<ID>.jpg`. בכל פריים מוטבעת חותמת זמן.

## הרמה: שורה תחתונה
- **הרמה היא קולנועית ולא "AI מגומגם"**: עור, השתקפויות, צללים, אבק ותנועת רכב מציאותיים. גם ברזולוציית אינסטגרם (720p) רוב הצופים לא יזהו שזה AI.
- **עקביות דמות לאורך 30 שניות ו-8 עד 10 שוטים** מתמונה אחת בלבד (רילס דובאי: תמונת פספורט אחת → אותו פרצוף בכל השוטים).
- **סינכרון שפתיים בעברית נשמר** בהפקה היברידית (מאור חני מדבר בעברית בתוך הרולס, והפה תואם).
- **סרט של 20 דקות** (ANERNEQ) עם דמויות עקביות, אש, שלג, דיאלוג וכתוביות: רמת סטרימינג.
- איפה עדיין רואים AI: טקסט ולוגואים קטנים, ידיים במגע עם חפצים, ותנועות מהירות מאוד שמעט "נמרחות" (בעיקר בשוטי פעולה בפסטיבל).

**המסקנה החשובה:** היתרון כבר לא נמצא ב"להשיג איכות", כי הכלים נותנים אותה. היתרון נמצא ב**רעיון, בבימוי (רשימת שוטים מתוזמנת), בצילום הקלט ובהוק**.

---

## שלוש שיטות עבודה שרואים בסרטונים
| שיטה | מה נכנס | מה יוצא | דוגמאות |
|---|---|---|---|
| **1. Image→Video, פרומפט רב-שוטי מתוזמן** | תמונת פנים אחת + פרומפט עם timecodes | 30 שניות של "פרסומת" שלמה עם 9 שוטים | דובאי / למבורגיני (edbert_yienson) |
| **2. Video→Video "Genjutsu", הפקה היברידית** | צילום אמיתי בטלפון (חניון, סטודיו ריק, גרין-סקרין, סלון) + תמונות רפרנס + שורת טקסט | אותה תנועה ואותו משחק בעולם אחר | מאור חני (רולס), Higgsfield רכבת תחתית, האסטרונאוט, החתול |
| **3. "אינסוף זוויות" מקליפ אחד** | טייק אחד מזווית אחת + רשימת זוויות עם timecodes ("Claude מרחיב לפרומפט") | אותו טייק עם קאברג' של צוות צילום: קלוז-אפ, רחפן, low angle, בתוך הכוס | rourke (Lovart × Seedance 2.5), sidequestpat_ (Genjutsu + Seedance) |

---

## ניתוח כל רילס

### 1. DcDrXjXsLcU: @edbert_yienson, "Dubai Lamborghini" (30 שניות, 9:16) ★ הכי מלמד
**המבנה על המסך:** בחלק העליון הווידאו, באמצע הכותרת "STEAL MY PROMPT · COMMENT 'DUBAI'", ובתחתית **INPUT** (תמונת פספורט אחת על רקע אפור) ליד **PROMPT** שגולל יחד עם הווידאו.
**השוטים:** צלילה מראש הבורג' ח'ליפה, צד הרכב, מראה אחורית, חזית, תא הנהג, סטירינג, עקיפה ושוט נעול לסיום. **אין דיבור**, רק סאונד מנוע ומוזיקה.
**הפרומפט שנחשף בסרטון (מתומלל מהפריימים):**
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
(ככל הנראה קודמת לזה פסקת פתיחה שמתארת את הדמות, החליפה השחורה והלמבורגיני הצהובה בדובאי.)
**לקחים:**
- **הפורמט "Input + Prompt על המסך" הוא בעצמו ההוק:** הצופה רואה שמספיקה תמונת פספורט, ורוצה את הפרומפט. התוצאה: 24 אלף תגובות מול 19 אלף לייקים.
- כל שוט מוגדר בשלושה דברים: **זווית ומיקום מצלמה**, **מה הרכב או הדמות עושים** ו**איך השוט נגמר** (exiting frame, pulling away).
- שוטים קצרים של 1 עד 3 שניות = קצב של פרסומת רכב.

### 2. DdyIfcjSm3P: @maorhani1 (ישראלי), "רולס מול חניון" (40 שניות, 9:16) ★ הנוסחה לשוק הישראלי
**המבנה:** מסך מפוצל. **למעלה** התוצאה (מלון Hotel de Paris במונטה קרלו, Rolls-Royce שחורה, נהג בחליפה). **למטה** המקור: חניון תת-קרקעי, רכב כחול קטן, חבר בטי-שירט. אותה תנועה בדיוק: יציאה מהלובי, פתיחת דלת, "נותן טיפ" (שטרות על הרצפה), "hello mr hani" / "thank you mr hani".
**החלק השני:** מאור יושב ברכב ומדבר למצלמה בעברית ("בדיוק סגרנו עסקה עכשיו של מאה מיליון דולר...", "אנחנו הולכים להיות המפיצים הגדולים ביותר בעולם של מכונות מזל לקזינו"). למטה רואים את הצילום המקורי בתוך רכב רגיל. בסיום: "תגיבו רולס תעקבו אחריי ואשלח לכם את המדריך", ומסך "המלא!".
**לקחים:** כלי ההפקה הוא **Higgsfield Genjutsu**, והלוגו "Higgsfield + ChatGPT" מופיע כל הזמן. כלומר שיתוף פעולה או שותפות עם Higgsfield. **הומור "פייק עשיר"**, מה שהכי עובד בעברית. כל מה שצריך: חבר, רכב רגיל, חניון וטלפון.

### 3. DclqVvdqvZw: @rourke, "Infinite Camera Angles" (60 שניות) ★ מראה את כל זרימת העבודה
**חלק א' (0 עד 22 שניות):** לפני ואחרי. למטה טייק אחד, רחב ונעול, של דוכן לימונדה ("Original"). למעלה "AI Video": קלוז-אפ סלואו-מושן על לימון באוויר, low angle, טופ-דאון, extreme close-up, **מצלמה בתוך הכוס**, דולי-זום, POV מבעד לחלון.
**חלק ב': ההדרכה (22 עד 45 שניות):**
1. רושמים את ה-timecodes שבהם רוצים "לחתוך" לזווית חדשה.
2. ב-**Claude** מדביקים את הווידאו ורשימה קצרה:
   `00:00 Tracking shot to Rourke / 03:07 Close up slow motion / 05:03 Low angle / 06:14 Top down shot / 08:14 Extreme close up / 14:00 Camera inside the cup / 15:22 tracking shot of the lemonade jug / 20:06 Dolly zoom` + `Keep the location, dialogue, and actions identical to the original video`
3. Claude מרחיב אותה לפרומפט מקצועי ומתוזמן, למשל:
   `[00:00-02.37] Shot 1: Rourke from @Video1 speaks to camera behind the lemonade stand, same performance and dialogue. Straight-on eye level, slow zoom in. Standard prime. Harsh midday sun. Handheld micro-drift easing forward. Hard cut to Shot 2. [02.37-05.57] Shot 2: The lemon wedge from @Video1 tosses up from Rourke's hand, ramping into deep slow motion as it spins midair...`
4. מדביקים ב-**Lovart** עם המודל **Seedance 2.5**, מצרפים את הסרטון כ-`@Video1`, ומייצרים.
**לקחים:** "**LLM ככותב פרומפטים**" היא שיטת עבודה מוכחת. לכל שוט: עדשה, תאורה, סוג תנועת מצלמה, מעבר (Hard cut) ושמירה על הביצוע המקורי. הפנייה לנכסים נעשית בתחביר `@Video1`.

### 4. Dd6gkuVR7jS: @sidequestpat_, "Genjutsu + Seedance" (29 שניות)
**שלב 1:** Genjutsu הופך סלון לבן ופשוט (חולצה שחורה) לפנטהאוז עם נוף לים (פולו בז', שעון זהב), עם wipe של לפני ואחרי.
**שלב 2:** Seedance 2.5 "Infinite Angles": קלוז-אפ על השעון, שוט רחפן, שוט רחב שחושף "סט צילום" עם תאורה ומצלמות שלא קיימים במציאות.
**הטקסט שנאמר:** "believe it or not, was recorded on one camera, one angle... what this means if you work in video production, your clients, personal brand... you need insane skills... because video AI has come to this".
**לקח:** **שרשור כלים** (סביבה, ואז זוויות) מאפשר להפיק "פרסומת יוקרה" מצילום של סלון רגיל. קהל היעד המוצהר: **אנשי וידאו ובעלי עסקים**.

### 5. DdwEiL4KzVS: Higgsfield, "Genjutsu AI Production" (59 שניות)
מסך מפוצל: **למטה סטודיו לבן ריק עם גרין-סקרין קטן**, ולמעלה אותו שחקן ברכבת תחתית מלאה בדמויות (ליצן, אביר, דינוזאור, כלב), ברחוב עם בלונים ואופניים, ובשדה קרב עם שריון. בהמשך מוצג הממשק: **Original video + References (6 תמונות: דמויות, כלב, תחפושות) + שורת טקסט** "Same video, but inside a subway."
**לקח:** זה ה-UI בפועל: וידאו מקורי, עד כ-6 תמונות רפרנס ומשפט אחד. **אפשר לצלם בכל חדר ריק.**

### 6. Ddjk5fCq1VK: Higgsfield, "Hybrid Production" (41 שניות, 16:9)
גרין-סקרין עם מאוורר ונדנדת קפיץ כחולה, שהופכים לאופנוע מעופף במדבר; הליכה על קורה הופכת להליכה על חבל בין גורדי שחקים; אסטרונאוט עם כוס קפה (פרסומת מוצר) על הירח; בחורה בבריכה עם מוצר "Space Food"; "Fix it in post": שלט SALE מוחלף.
**לקח:** זה **שוק ה-B2B**. פרסומות מוצר בהפקה היברידית, עם placement של מוצר ותיקון בדיעבד. המילים "FOR LARGE STUDIOS & PRODUCTION TEAMS" ו-"NOW IN API".

### 7. DeHZl65CI2G: Higgsfield, "AI Influencer" (49 שניות, 16:9)
דמויות אבסורדיות (שיער מוגזם, ראש חתול ספינקס בחליפה, ראש צפרדע, שרימפס במדי כדורסל) בתוך סצנות רחוב מציאותיות. הממשק מראה "Character Type" (Human/Animal/...). כותרות: "CREATE YOUR INFLUENCER", "GO VIRAL", "TRANSFER ANY MOTION WITH GENJUTSU". מוצגות דוגמאות של חשבונות עם **6.4M** ו-**6.3M** צפיות.
**לקח:** **משפיען AI אבסורדי + טרנד ריקוד או תנועה (motion transfer)** = נוסחת צפיות לערוצים ללא פנים.

### 8. Ddwky9yq-Jt: Higgsfield, "Seedance 2.5 API / 100% cashback" (22 שניות)
פתיחה מהירה וקולנועית (low angle, בחורה עם ציוד), כותרת "SEEDANCE 2.5 1080P · NOW IN Higgsfield {API}", בילבורד "BEST AI VIDEO MODEL FOR ENTERPRISE", מונה כסף "$20,000,000 CASHBACK POOL / $17,998,344 LEFT", ודוגמנית עם בקבוק ובושם (פרסומת מוצר).
**לקח:** הטכניקה של **מונה FOMO**, והמחשה לכך ש-Seedance 2.5 מתאים לפרסומות מוצר.

### 9. Dd1xCWei0CF: Higgsfield Originals, "ANERNEQ" (20 דקות, 16:9)
דרמה ארקטית: אש, כפר אוהלים, דמויות עקביות בפרוות, כתוביות דיאלוג ("Take him to the sacred Bones", "Stop this!", "[Sings a lullaby]"), זוהר צפוני, ותאורת לילה כחולה וחמה. החותמת: "HIGGSFIELD CINEMA STUDIO".
**לקח:** כבר אפשר לייצר **סרט קצר וארוך עם עלילה**. הפרומפטים והנכסים פתוחים ("open source"), ולכן זה חומר לימוד מצוין.

### 10. DdmkVEgKLE4: Higgsfield, "Global Film Festival $1M" (74 שניות, 16:9)
פתיחה בסגנון MGM עם ילד במקום האריה, מנחה בטוקסידו, "145 COUNTRIES", "OVER 3,000,000 VIEWS ON HIGGSFIELD", קטעים מסרטים שהוגשו (רכבת, מערב פרוע, פיצוצים) ושופטים מוכרים: **Edwin Catmull** ו-**Phedon Papamichael (2× Oscar nominee)**.
**לקח:** **תחרויות עם פרסים** הן ערוץ הכנסה ומיצוב. השופטים הם אנשי הוליווד, כלומר התעשייה מתייחסת לזה ברצינות.

---

## דפוסים חוצי-רילס (מה לשכפל)
1. **"תראה את הקלט מול התוצאה":** מסך מפוצל (למעלה AI, למטה מקור) או Input+Prompt על המסך. **מופיע ב-7 מתוך 10 הרילס.** ההשוואה היא ההוק.
2. **"הגב מילה ואשלח לך..."** (DUBAI / רולס / AI / ANGLE / JUTSU / GENJUTSU / VIRAL / API / FESTIVAL / UNLOCK): מופיע **בכל 10**.
3. **כותרת קבועה למעלה** עם שם הכלי ("HIGGSFIELD SEEDANCE 2.5 1080P"). זה גם מוסיף אמינות וגם מכניס לחיפוש של מי שמחפש את הכלי.
4. **אורך:** רילס של יוצרים נמשכים 29 עד 60 שניות; טיזרים מסחריים 22 עד 74 שניות.
5. **טקסט על המסך בכל רגע** (כתוביות מילה-מילה, או מילה אחת גדולה בכל פעם).
6. **פנטזיית עושר וסטטוס** (למבורגיני, רולס, פנטהאוז, שעון זהב) = הנושא הוויראלי ביותר ליוצרים.
7. **אפקט ה"וואו" הוא הטכנולוגיה עצמה.** הקהל הראשי הוא יוצרים ועסקים שרוצים ללמוד, ולכן הפרומפט והמדריך הם מגנט לידים מושלם.

## מה זה אומר עלינו: כללי עבודה
- **הסגנון הנכון:** פורמט "Input + Prompt + Result" או "מקור למטה, תוצאה למעלה". זה עובד, וזה גם מוכיח לקוחות פוטנציאליים שאתה יודע את העבודה.
- **כתיבת פרומפט:** קודם רשימת שוטים קצרה עם timecodes, ואז LLM (Claude/ChatGPT) מרחיב לפרומפט מקצועי ומתוזמן. לכל שוט: מצלמה, עדשה, תאורה, תנועה, איך השוט נגמר ומעבר.
- **מה לצלם או להביא:** תמונת פנים ברורה (פספורט, אור אחיד ורקע נקי) ל-Image→Video. לווידאו→וידאו: טייק יציב עם תנועה ברורה, תאורה טובה, וחבר שמשחק את "הצד השני".
- **הנישה הישראלית:** "פייק עשיר" עם הומור, ודיבור בעברית שנשמר ב-Genjutsu. אף אחד עוד לא מציף את השוק הזה.

## תמלולים: מה נאמר בקול (Whisper)
- **rourke:** "First, make a note of all the timecodes where the camera is going to cut to a new angle. Then inside Claude, paste your video, note the timecodes and write the new camera angles... Also add: keep the same location, dialogue and actions. Claude will give you a prompt; give it to Lovart. Make sure Seedance 2.5 is selected and upload the original video. **It's not going to give you the perfect generation all in one go. Instead, take small clips and give those to Seedance and adjust the camera angle in incremental clips.**"
  → **הטיפ הכי חשוב:** מחלקים את הסרטון לקליפים קצרים ומייצרים כל קטע לחוד, ולא את כל הסרטון בבת אחת.
- **sidequestpat_:** התסריט בנוי כפנייה ישירה לקהל המשלם: "If you work in video production, what can you offer your clients? If you have a personal brand, what does your next ad look like? You don't need insane skills... neither a massive budget".
- **Higgsfield (רכבת תחתית):** "Go to Genjutsu, upload the original footage, describe the result you want in one simple prompt, and let AI rebuild the shot. Replacing a single element or transforming the entire scene... **doesn't require a green screen, heavy CGI, or weeks in post-production**".
- **maorhani1:** הקטע המבוים כמעט ללא מלל ("מיסטר חני... תודה"). הדיבור בעברית שבתוך הרכב לא נקלט בתמלול האוטומטי, אבל הוא מופיע ככתוביות על המסך. כלומר **כתוביות צרובות** הן חלק מהפורמט.
- רילס דובאי, Hybrid Production ו-API: ללא דיבור, רק מוזיקה, סאונד ותמלול על המסך. **רילס בלי דיבור עובדים בכל שפה** ומתאימים לקהל עולמי.
