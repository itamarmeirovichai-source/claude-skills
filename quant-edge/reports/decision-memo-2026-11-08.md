# מזכר הכרעה — תוכנית quant-edge, 8.11.2026 (גרסה סופית, 22:50 שעון ישראל)

## ההכרעה: N1 — לא נמצא קצה, וההמלצה היא לעצור.

התוכנית נסגרת היום לפי הוראתך ("היום צריך לסיים הכול"; תנאי סיום (c) בפרומפט). בערב היא נפתחה מחדש לבקשתך לבדוק את כל המועמדים שנשארו: כל 130 הפריטים מוינו, והאחרון שאפשר היה לבדוק בחינם (Q-0011) נבדק ונכשל. ארבעת המועמדים החזקים שדרשו נתונים בתשלום נקנו מ־Databento ‏($9.25 מתוך הקרדיט) ונבדקו (Q-0012 עד Q-0015), וכולם נכשלו. לבסוף נבדקה "דרך 1" — הון עצמי, תיק Risk Parity רב־נכסי עם מסנן מגמה (Q-0016). היא הרוויחה מעל מזומן (t = 2.02), אבל זה רחוק מהרף 3.68, והיא הייתה **גרועה** מ־60/40 פשוט באותה תנודתיות. שום השערה לא עברה את השער. **הסייג:** זו לא הוכחה שאין קצה בשום מקום; זו הוכחה שבכל מה שנבדק כאן, עם הנתונים והתקציב שהיו, אין.

## 1. מה נבדק (כל שורה שנספרה)

| id | מה נבדק | מבנה | OOS | תוצאה נטו | t | פסק דין |
|---|---|---|---|---|---|---|
| CAL-D | כיול הצינור: מגמת 12 חודשים על 54 חוזים | — | 1990–2016 | Sharpe 1.43 ברוטו | 6.78 | כיול עבר (לא קצה) |
| Q-0001 | תיקון לונדון בסוף חודש, EURUSD/GBPUSD/AUDUSD | FTMO תוך־יומי | 2015–2024 | ‎−7.4 bp לאירוע | ‎−2.04 | נכשל |
| Q-0003 | לונג AUDUSD בימי FOMC | FTMO תוך־יומי | 2014–2024 | ‎+9.7 bp לאירוע | 0.95 | נכשל |
| Q-0005 | קנייה אחרי נפילת יומיים באנרגיה | FTMO Swing | 1990–2007 | ‎−0.17 bp ליום | ‎−1.37 | נכשל |
| Q-0006 | אותו כלל על זהב | FTMO Swing | 1990–2007 | ‎−0.44 bp ליום | ‎−2.48 | נכשל |
| Q-0007 | היפוך לילה מול יום ב־7 מדדי CFD | FTMO תוך־יומי | 2015–2024 | ‎−4.5 bp ליום (ברוטו ≈ 0) | ‎−4.81 | נכשל |
| Q-0008 | נגד תנועות HSI אחרי שעות המסחר | FTMO תוך־יומי | 2016–2024 | ‎+3.6 bp לעסקה | 1.09 | נכשל |
| Q-0009 | ORB של 30 דקות על ה־S&P (3 גרסאות) | FTMO תוך־יומי | — | נכשל בתוך המדגם, OOS לא נקרא | — | נכשל, משפחה נסגרה |
| Q-0011 | נגד התנועה בפתיחה מחדש ב־18:00 ET, ‏US500/US100/זהב | FTMO תוך־יומי | 2013–2024 | Sharpe נטו ‎−0.14 | ‎−0.52 | נכשל |
| Q-0012 | היפוך לילה מול יום על חוזי CME (ES/NQ/YM/EMD/NKD) — המועמד היחיד בדירוג medium | חוזים תוך־יומי | 2015–2024 | ‎−4.7 bp ליום (ברוטו ‎+1.0, t 1.24) | ‎−5.74 | נכשל |
| Q-0013 | סוף חודש באג"ח האוצר (ZN/UB) | חוזים | 2015–2024 | ‎+7.9 bp לאירוע | 1.31 | נכשל |
| Q-0014 | תגובה לדוח היבולים של USDA (ZC/ZS) | חוזים | 2015–2024 | ‎−10.7 bp לאירוע | ‎−1.58 | נכשל |
| Q-0015 | פרמיית יום דוח האחסון של גז טבעי (NG) | חוזים | 2019–2024 | ‎−9.8 bp לאירוע | ‎−2.53 | נכשל |
| Q-0016 | דרך 1 — הון עצמי: Risk Parity על 7 סוגי נכסים + מסנן מגמה של 10 חודשים | הון עצמי ב־IBKR | 2010–2024 | Sharpe נטו 0.52 (60/40 באותה תנודתיות: 0.87) | 2.02 | נכשל, וגם נחות מ־60/40 |
| Q-0017 | היפוך אחרי סגירת המסחר ב־S&P (16:01–16:07) | חוזים תוך־יומי | 2015–2024 | ‎−4.7 bp לאירוע (ברוטו ‎−1.1) | ‎−8.84 | נכשל |
| Q-0018 | היפוך אחרי הסגירה הכפויה של חשבונות פרופ (16:10–16:14) | חוזים תוך־יומי | 2022–2024 | ‎−1.1 bp לאירוע (ברוטו ‎+1.35) | ‎−2.05 | נכשל |
| Q-0019 | קנייה אחרי "פרץ" ירידה חד עם נפח גבוה, ES וזהב | חוזים תוך־יומי | 2015–2024 | ‎−2.7 bp לעסקה (ברוטו ‎+0.2), ‏3,515 עסקאות | ‎−7.31 | נכשל |
| Q-0020 | נגד חמש הדקות הראשונות כשחלק המיקרו גבוה | חוזים תוך־יומי | 2022–2024 | ‎−4.0 bp לאירוע (בתוך המדגם היה ‎+4.3) | ‎−1.78 | נכשל |
| Q-0021 | היפוך אחרי חצי השעה האחרונה (מחקר JFE 2021), ES וזהב | חוזים מהערב עד הסגירה למחרת | 2015–2024 | ‎+7.9 bp לאירוע, 70% מהשנים חיוביות | 1.14 | נכשל (חיובי אבל רחוק מהרף) |

N סופי: 301 מתוך 430 (280 בירושה + 21 בתוכנית). הוצאה ב־Databento: ‏$9.25 מהקרדיט, על נתוני שעה של 10 חוזים. הרף נשאר z = 3.6807 לאורך כל התוכנית. כל שורה נרשמה ונדחפה לפני שנכתב הקוד שלה; כל קריאה של נתוני OOS מתועדת ביומן; ה־hold-out לא נפתח.

## 2. מה לא נבדק

**מיון כל 130 הפריטים שנותרו (`research/triage-2026-11-08.md`):** 1 אפשר היה לבדוק בחינם (Q-0011, נבדק ונכשל); 0 דרשו רק הורדה חינמית בכוח בדיקה שווה; 10 דורשים Databento; 119 לא שווים ספירה (דומים למשפחות סגורות, דליפת עתיד מובנית, עלויות, או כוח בדיקה מתחת ל־5%).

**Databento נפתח הערב:** אחרי החלפת המפתח והגדרתו כמשתנה סביבה, סשן נפרד רשם מראש ובדק את ארבעת המועמדים החזקים ביותר שדרשו נתונים בתשלום (Q-0012..Q-0015), ב־$9.25 מהקרדיט. כולם נכשלו. 6 המועמדים הנותרים בקבוצת Databento הם בדירוג low ויקרים יותר (≈ $68).

### מה לא נבדק כי הנתונים לא נקנו

| עדיפות | מועמד | נתונים נדרשים | עלות משוערת ב־Databento |
|---|---|---|---|
| 1 | היפוך לילה מול יום על חוזי ES/NQ/YM/EMD/NKD (הגרסה החינמית שלו, Q-0007, נכשלה עם רווח גולמי ≈ 0) | ‎1h, 2010–2024 | ≈ $5 |
| 2 | פרמיית ימי דוח האחסון של גז טבעי | NG 1m RTH | ≈ $7 |
| 3 | פירוק אחרי העלאת מרווחים ב־CME | GC/SI/CL/NG 1m | ≈ $28 |
| 4 | עסקת ה־index extension של האוצר בסוף חודש | ZN + UB 1h | ≈ $2 |
| 5 | היפוך אחרי חצי שעה אחרונה חריגה | ES/NQ/ZN/GC/SI/NG 1m | ≈ $40 |
| 6 | Carry של עקום האנרגיה | CL/BZ/NG/HO 1d | ≈ $0.20 |

עדיפויות 1–6 יחד ≈ $82, מתחת לתקרה של $94 מתוך הקרדיט. לא הוצא סנט.

## 3. "כמעט"

אין אף אחד. הקרוב ביותר: Q-0016 (דרך 1, הון עצמי) עם t = 2.02, ואחריו Q-0013 עם t = 1.31. שניהם מתחת ל־2.68 (הרף פחות 1.0). וגם Q-0016 לא באמת "כמעט": t שלו מודד רווח מעל מזומן, ומול 60/40 באותה תנודתיות ה־alpha שלו לא מובהק (t = 0.79) והוא הניב פחות. התוצאה תואמת "אין כלום".

## 4. הסיבות המבניות, עם מספרים

- **הרף הכלכלי גבוה מאוד.** $20,000 לשנה לחשבון FTMO Swing של $100k דורשים Sharpe נטו 2.44 / 1.95 / 1.45 בתנודתיות 12% / 15% / 20%, לפני מס; אחרי מס 1.89–2.61 ב־20% (הרצה מחדש, `economics/required-sharpe-2026-11.md`).
- **עלויות.** כדי לעבור את מבחן כפל העלויות, הרווח הגולמי צריך להיות לפחות פי 3 מעלות הלוך־חזור. ב־Q-0007 הרווח הגולמי היה כמעט אפס; ב־Q-0008 הרווח הגולמי (t 2.14) נמחק כמעט כולו בעלויות.
- **דעיכה אחרי פרסום.** מנגנונים מפורסמים מאבדים בערך חצי מהביצועים אחרי שהם מתפרסמים; גם אלה שנבדקו כאן עברו את הסינון רק בדרגת "low".
- **כללי החברות מחמירים.** מאז 11.10: The5ers חוסמת את ישראל, Topstep הוסיפה חלון חדשות של ±5 דקות ודמי API של $29 לחודש, TradeDay בודקת החזקות קצרות מכ־10 שניות, וסעיף 7.8 של FTMO חל עכשיו על כל סוגי החשבונות (`economics/firms-matrix-2026-11.md`).

## 5. הסטנדרט החלש יותר

שום תוחלת חיובית לא נמצאה, גם לא בסטנדרט חלש יותר: כל שבע ההשערות היו שליליות או סביב אפס נטו. לכן אין מה לתמחר לחשבון או להון עצמי ב־IBKR. נקודת הייחוס שהתוכנית הקודמת נתנה לכסף הפרטי נשארת בתוקף: 60/40 SPY/IEF, קנייה והחזקה, Sharpe 0.92 ב־2016–2026 (`references/trend-following-etf.md`). ההחלטה על ההון הפרטי היא שלך ומחוץ למנדט התוכנית.

## 6. מה נמסר בכל מקרה (הכול ב־PR #27)

- **אבחון ניתוקי ה־IBKR של הבוט שלך:** מדריך צעד־צעד בעברית, סקריפט ניטור לקריאה בלבד (selftest 26/26), ותוכנית תיקון לבוט (`engineering/`). זה הדבר השימושי ביותר שאפשר להפעיל כבר השבוע.
- **אגם נתונים:** יותר מ־30 מערכי נתונים חינמיים עם מניפסט sha256 (דקות FX ו־CFD מ־2010 עם שעון מתוקן, חוזים יומיים, VIX, COT, GEX, לוחות שנה של אירועים); הנתונים עצמם מחוץ לריפו.
- **רתמת שער מלאה עם 61 בדיקות:** שער נתונים יחיד, יומן קריאות, נעילת hold-out, סטטיסטיקת Gate v2, בקרות כסף ל־Databento, מנוע בקטסט.
- **רישום מלא:** 115 שורות, N = 290, כל תוצאה עם הקוד והקומיט שלה.
- **שבעה מכתבי חברות מוכנים לשליחה** ומטריצת כללים מעודכנת מהמקור.
- **רשימת 114 מנגנונים מדורגים** (`research/candidates.md`), כך שאם תחליט לחזור לזה עם נתונים, אפשר להתחיל מהאצווה הבאה.

## 7. ההמלצה

**לעצור.** לא לקנות חשבונות ממומנים על בסיס שום דבר שנבדק כאן. אם בעתיד תרצה ניסיון אחרון וזול, הוא היפוך הלילה מול היום על חוזי CME (כ־$5 מהקרדיט), אבל הגרסה החינמית שלו נכשלה עם רווח גולמי אפסי, כך שהסיכוי נמוך. הפעולה המועילה הבאה היא להריץ את סקריפט הניטור של IBKR חמישה ימי מסחר ולתקן את הניתוקים בבוט.

---

## English appendix

**Verdict: N1 (honest negative), program closed on 2026-11-08 at Itamar's instruction (end condition c); reopened the same evening to triage all 130 remaining items (1 free-testable → Q-0011, FAIL; 10 Databento-only, of which the 4 strongest were bought ($9.25) and tested in a child session (Q-0012..Q-0015, all FAIL) and 6 low-rated ones remain; 119 not worth a count).** Path 1 (own capital, Q-0016) was then tested at Itamar's request and also failed. Nothing passed Gate v2; no near-miss (best t = 2.02 for Q-0016 vs bar 3.6807, and its alpha vs 60/40 at equal vol is t 0.79). Final N = 301 of N_total 430. Databento spend $60.60 of $99.37 credit (2026-11-09: $51.35 for ES/GC/MES 1m). Reopened 2026-11-09 (D-028/D-029): the five remaining Databento rows Q-0017..Q-0021 all FAIL (best Q-0021 t 1.14); C-12-04 not testable (CME archive blocked); literature sweep2 found 14 new ideas, none with power >= 0.05 (summed power x prior ~0.006). Hold-out never read.

| id | hypothesis | firm structure | OOS | net (1x) | t_min | 2x-cost t | verdict |
|---|---|---|---|---|---|---|---|
| CAL-D | MOP 12m TSMOM, 54 futures (pipeline calibration) | — | 1990–2016 | Sharpe 1.432 gross | 6.78 | — | calibration pass (a); (b) not verifiable |
| Q-0001 | month-end London-fix legs signed by foreign-vs-US equity MTD | FTMO intraday CFD | 2015-03..2024 | −7.39 bp/event | −2.04 | −2.85 | FAIL |
| Q-0003 | long AUDUSD on FOMC statement days | FTMO intraday CFD | 2014..2024 | +9.74 bp/event | 0.95 | 0.63 | FAIL |
| Q-0005 | energy two-day-fall dip buy | FTMO Swing | 1990..2007 | −0.17 bp/day | −1.37 | −1.14 | FAIL |
| Q-0006 | gold two-day-fall dip buy | FTMO Swing | 1990..2007 | −0.44 bp/day | −2.48 | −2.47 | FAIL |
| Q-0007 | cross-index CO-OC reversal, 7 index CFDs | FTMO intraday CFD | 2015..2024 | −4.52 bp/day (gross +0.01) | −4.81 | −9.61 | FAIL |
| Q-0008 | HSI after-hours fade on HK50 | FTMO intraday CFD | 2016-11..2024 | +3.64 bp/trade (431) | 1.09 | 0.05 | FAIL |
| Q-0009 | prereg_orb30 A/B/C | FTMO intraday CFD | not read | IS A: −0.120 R, p5 −0.167 R | — | — | FAIL at stage 1; family closed |
| Q-0011 | 18:00 ET reopen fade, US500/US100/XAUUSD | FTMO intraday CFD | 2013..2024 | daily net Sharpe −0.136 | −0.52 | −1.55 | FAIL |
| Q-0012 | C-4-01 cross-sectional CO-OC reversal, CME ES/NQ/YM/EMD/NKD 1h | intraday futures | 2015..2024 | −4.72 bp/day (gross +1.0, t 1.24) | −5.74 | −12.61 | FAIL |
| Q-0013 | C-1-01 month-end Treasury index extension, ZN/UB 1h | futures | 2015..2024 | +7.92 bp/event | 1.31 | −0.30 | FAIL |
| Q-0014 | C-2-05 USDA Crop Progress reaction, ZC/ZS 1h | futures | 2015..2024 | −10.73 bp/event | −1.58 | −3.64 | FAIL |
| Q-0015 | C-2-01 NG storage-day premium, NG 1h | futures | 2019..2024 | −9.84 bp/event | −2.53 | −2.99 | FAIL |
| Q-0016 | path 1, own capital: risk parity of 7 asset classes + 10-month trend filter, 10% vol target | own capital | 2010..2024 | excess Sharpe 0.52 (60/40 equal vol 0.87; alpha t 0.79) | 2.02 | 1.94 | FAIL; also worse than 60/40 |
| Q-0017 | C-1-08 ES post-cash-close fade 16:01-16:07, ES 1m | intraday futures | 2015..2024 | -4.74 bp/event (gross -1.12) | -8.84 | -8.36 bp | FAIL |
| Q-0018 | C-12-01 prop-flatten extension fade 16:10-16:14, ES 1m (+MES footprint) | intraday futures | 2022..2024 | -1.09 bp/event (gross +1.35) | -2.05 | -3.53 bp | FAIL |
| Q-0019 | C-4-04 drift-burst fade, long after negative high-volume bursts, ES+GC 1m | intraday futures | 2015..2024 | -2.67 bp/trade (gross +0.18; n 3515) | -7.31 | -5.52 bp | FAIL |
| Q-0020 | C-12-21 micro-share open-thrust fade 09:35-10:00, ES+MES 1m | intraday futures | 2022..2024 | -3.97 bp/event (IS +4.27) | -1.78 | -5.51 bp | FAIL |
| Q-0021 | C-4-07 hedging-overshoot reversal 18:00 -> next close, ES+GC 1m | overnight-session futures | 2015..2024 | +7.93 bp of account/event-date; 70% years positive; all neighbours positive | 1.14 | +5.67 bp | FAIL (positive, far below bar) |

Disclosures: CAL-D double OOS read after a pre-P&L crash; HistData DST defect affecting ≤ 6 events in each of Q-0001/Q-0003 (bound shows verdicts cannot flip; no re-read); Q-0001/Q-0003/Q-0007 registered eligibility filters failed the truncation harness by construction, ex-ante versions printed and no better; gateway parsing fixes made before any batch-1 read. Null-expected near-misses across the 7 tests ≈ 0.03; observed 0.

Not tested for lack of paid data: priorities 1–6 in section 2 (≈ $82). Structural reasons, required-Sharpe table, firm-rule changes, deliverables: sections 4–6 above with file paths. Reference for private capital: 60/40 SPY/IEF buy-and-hold Sharpe 0.92 (2016–2026, inherited `references/trend-following-etf.md`).
