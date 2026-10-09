# PART F — יומן בנייה והעברה (Run 4, חלקי)

## מה זה כן ומה זה לא
בניתי את הסצנה **headless** דרך מודול `bpy` 5.0.1 בקונטיינר הענן הזה — **לא** דרך Blender MCP על המק שלך, ו**לא** מהסריקות שלך (עוד אין). לכן זה לא Run 4 כפי שהוגדר, אלא **סצנה בנויה מראש לפי החוזה** שאתה פותח על המק וממשיך ממנה. כל שלב שדרש את החומרה שלך — הסריקות והרנדר הסופי — נשאר אצלך.

## מה נבנה
- **תשע שכבות** בשמות החוזה המדויקים: `bun_bottom`, `patty_lower`, `cheese_lower`, `patty_upper`, `cheese_upper`, `bacon_beef`, `onion_caramelized`, `sauce_chef`, `bun_top`. אורז'ין של כל שכבה במרכז שלה, ציר הערימה +Z, גובה כולל 11 ס"מ. `sesame_scatter` עם 53 שומשומים על הכיפה, כולל כתם קירח מכוון, ועוד 30 `seed_loose_01..30`.
- **חומרים** עם subsurface בלחמנייה, שונות ברוגנס ובאלבדו מרעש ב-Object space, coat על הרוטב, גבינה טבעונית מאט.
- **החיתוך**: שני חצאים חתוכים מראש (`burger_half_left/right`) עם **1,038 פאות פנים אמיתיות** — bisect + holes_fill + poke, לא בוליאן שטוח. `cut_face_left/right`. **חומר פנים נפרד לכל שכבה** מ-`INTERIOR_COLORS`, כדי שהחתך ייקרא כבורגר ולא כמשטח ורוד אחיד.
- **סכין** `knife_blade` + `knife_handle` עם להב מחודד אמיתי, ו-`knife_glint` (תאורת שטח צרה שמטאטאת את הלהב, רנדר בלבד).
- **חמישה בורגרים** `burger_toss_a..e`, `burger_toss_c` הוא הגיבור.
- **248 פריימים מוקפאים** לכל שמונת הביטים לפי טבלת האחוזים בחוזה. הכל פונקציה טהורה של ה-progress, כך שגלילה אחורה מדויקת.
- **מצלמה: צילום אחד רצוף**, עדשה אחת 85mm לכל הרצף — המרחק עושה את המסגור, לא הזום. פוקוס על אובייקט `focus_target` מונפש (rack focus בביט 7), f-stop מונפש 11→5, רעד מצלמה דועך על הפגיעה. גם `cam_main_portrait` למובייל.
- **תאורה** בשפה של פרסומת אוכל: KEY גדול מאחור-משמאל, FILL חלש מקדימה, RIM צהוב מותגי, KICK אדום מותגי, עולם כמעט-שחור, פלנצ'ה מאט.
- **הגדרות רנדר**: Cycles, device GPU (Metal), 512 samples אדפטיבי, **OpenImageDenoise** (OptiX הוא NVIDIA בלבד), motion blur, DOF, AgX.
- **`labels.desktop.json` + `labels.mobile.json`** — 70 פריימים (78–147), מיקומי עוגן מוקרנים לכל שכבה בקואורדינטות 0–1 עם ראשית שמאל-עליון. 92% מהעוגנים בתוך הפריים. **בלי הקובץ הזה התוויות באתר לא יכולות לעקוב אחרי השכבות.**
- **glTF**: `hero.glb` (0.04MB) ו-`halves.glb` (0.07MB), Draco. אימתתי בתוך ה-GLB עצמו שכל 15 שמות החוזה קיימים כ-meshes.

## איפה הקבצים
`research/run4-blender-handoff/` — `scripts/` (חמישה סקריפטים שמייצרים הכל מאפס), `out/smash_v04.blend`, `out/models/*.glb`, `out/frames/labels.*.json`, `out/tests/*.png`.
העתק ל-`~/Desktop/smash-blender/` ותמשיך משם.

## פסק דין כן על הריאליזם
**זה לא נראה כמו אוכל אמיתי, וזה צפוי.** הסתכלתי על כל פריים בדיקה — שישה סבבי תיקון — והנה מה שיצא: הסצנה **עובדת מבנית** — הזריקה קופאת בשיא, הפיצוץ קריא ומעל הפלנצ'ה, החצאים נפתחים כמו ספר ומראים חתך בשכבות. אבל הגיאומטריה היא **גלילים פרוצדורליים זמניים**, ובלי סריקות וטקסטורות אמיתיות זה נקרא כתרשים CG של בורגר, לא כבורגר. חסרים: קראסט אמיתי, קצוות תחרה של פטי סמאש, גבינה שנוזלת בפועל, אדים, טפטוף רוטב. **אל תראה את זה ללקוח.** הערך כאן הוא הריג: שמות, אורז'ינים, 8 ביטים, הצילום הרצוף, מסלול התוויות והגדרות הרנדר.

שלושה באגים אמיתיים שתפסתי ותיקנתי בדרך, כדי שלא תיתקל בהם: פסים אנכיים מהבוול ומרעש ב-Generated coords; פאות הצד שנצבעו בחומר הפנים כי זיהיתי לפי נורמל במקום לתייג בזמן החיתוך; וסימן סיבוב הפוך שהפנה חצי אחד עם הגב למצלמה.

## הפקודות

רנדר לילה מלא (דסקטופ):
```bash
/Applications/Blender.app/Contents/MacOS/Blender -b ~/Desktop/smash-blender/smash_v04.blend \
  -o //render/desktop/smash_#### -F PNG -s 1 -e 248 -a -- --cycles-device METAL
```

רנדר מובייל (מצלמה ורזולוציה אחרות — לא דחיסה של הדסקטופ):
```bash
/Applications/Blender.app/Contents/MacOS/Blender -b ~/Desktop/smash-blender/smash_v04.blend \
  --python-expr "import bpy; s=bpy.context.scene; s.camera=bpy.data.objects['cam_main_portrait']; s.render.resolution_x=1080; s.render.resolution_y=1440" \
  -o //render/mobile/smash_#### -F PNG -s 1 -e 248 -a -- --cycles-device METAL
```
במובייל החוזה מבקש 124 פריימים — קח כל פריים שני: `mv smash_0001 → 0001, 0003 → 0002 …` (הסקריפט בהמרה למטה עושה את זה).

הערכת זמן, כנה: מדדתי כאן **CPU בלבד** — 4 שניות לפריים ב-1280×720 ו-96 samples על הגיאומטריה הפרוצדורלית. על M-series ב-1920×1080 ו-512 samples עם denoise, הסצנה **הנוכחית** תיקח בערך **20–40 שניות לפריים → 1.5–3 שעות**. אחרי שתכניס סריקות, טקסטורות 4K, אדים וולומטריים וטפטוף — צפה ל**1–4 דקות לפריים → 4–16 שעות**. לקצר: לאפות את האדים ל-`.vdb` מראש, `adaptive_threshold` ל-0.02, לכבות motion blur בביטים סטטיים, ולרנדר ב-1600px ולהגדיל.

המרה לפורמט ולשמות של החוזה:
```bash
mkdir -p frames/desktop frames/mobile
i=0
for f in render/desktop/smash_*.png; do
  i=$((i+1)); n=$(printf "%04d" $i)
  ffmpeg -y -loglevel error -i "$f" -c:v libaom-av1 -still-picture 1 -crf 32 -cpu-used 6 \
    "frames/desktop/smash_${n}.avif"
done
# מובייל: כל פריים שני, 124 סה"כ
i=0; k=0
for f in render/mobile/smash_*.png; do
  k=$((k+1)); [ $((k % 2)) -eq 1 ] || continue
  i=$((i+1)); n=$(printf "%04d" $i)
  ffmpeg -y -loglevel error -i "$f" -c:v libaom-av1 -still-picture 1 -crf 34 -cpu-used 6 \
    "frames/mobile/smash_${n}.avif"
done
# גיבוי WebP לספארי ישן
for f in frames/desktop/*.avif; do
  ffmpeg -y -loglevel error -i "render/desktop/$(basename ${f%.avif}).png" -q:v 80 \
    "frames/desktop/webp/$(basename ${f%.avif}).webp"
done
```
`avifenc` (מ-libavif) נותן קבצים קטנים יותר — בדוק `avifenc --help` לגרסה שלך, הדגלים השתנו בין גרסאות.

glTF לאינטראקציות:
```bash
npx @gltf-transform/cli optimize out/models/hero.glb hero.opt.glb \
  --compress meshopt --texture-compress ktx2 --texture-size 2048
npx @gltf-transform/cli inspect hero.opt.glb   # ודא ששמות ה-meshes שרדו
```

## מה אתה עושה
1. **קנה שלושה Loaded Smashed בבוקה.** אחד שלם, אחד לפירוק, אחד לחיתוך לשניים.
2. **סרוק כל שכבה בנפרד** על משטח מאט אפור או שחור, בתאורה שטוחה בלי צללים. **מצב צילום/פוטוגרמטריה, לא LiDAR** — LiDAR לא פותר שומשום. פטיפון + טלפון על חצובה: שלושה סבבים ב-15°, 45° ו-70°, 40–60 תמונות לסבב, 120–180 לשכבה. נעל חשיפה, פוקוס ואיזון לבן. חכה שהאדים ייעלמו, והקהה ברק רק על הבורגר המוקרב. אפליקציות: Polycam, Scaniverse (מצב Classic חינמי), KIRI Engine, RealityScan.
3. **זרוק ל-`~/Desktop/smash-scans/`** בשמות `scan_bun_top`, `scan_patty_lower`, `scan_half_left` וכו'.
4. **פתח `smash_v04.blend`** והחלף את ה-mesh של כל שכבה בסריקה — **בלי לשנות שם אובייקט אחד**. כל האנימציה, המצלמה ומסלול התוויות ימשיכו לעבוד.
5. **רשימת צילומים לשאר האתר** (טלפון, ProRAW, חצובה, טיימר 2 שניות, איזון לבן נעול לאורך כל הצילום, 50–85mm, f/4–5.6, תאורה גדולה ורכה מאחור ב-45–135° עם פוליסטרן לבן מנגד): חזית החנות בין הערביים · פנים והדלפק · כל פריט בתפריט ב-1:1 · Dirty Fries · Blooming Onion · פריסת קייטרינג אמיתית · הצוות על הפלנצ'ה · הפלנצ'ה עצמה אחרי שירות.
6. **הרץ את רנדר הלילה**, המר, ושלח את התיקיות `frames/` ואת ה-glTF לבונה האתר עם המשפט: *"The rendered frames and the glTF are ready, named exactly per the asset contract — switch the signature section from the fallback to the frames."*
