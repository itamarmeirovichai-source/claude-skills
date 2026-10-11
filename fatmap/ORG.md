# FatMap — מבנה הארגון (v1.0, 2026-09-29)

```
                               מייסד (אתה)
                                   │
                         fatmap-director  (L0 — מפקח על הכול)
   ┌──────────┬───────────┬────────┴──────┬────────────┬───────────┬───────────┐
 פיזיקה     המצאה      סימולציה        ראיות        חומרה       תוכנה      קניין/רגולציה
 head-      head-      head-           head-        head-       head-      head-
 physics    invention  simulation      evidence     hardware    software   ip-reg
   │           │          │               │            │           │          │
 lead-mr    ideation   sim-electrical  literature   phantoms    algorithms prior-art
 electrical fusion     sim-mr          open-data    electronics app        regulatory
 acoustic   first-     sim-wave        redteam      safety      imaging    venture
 optical    principles body-models     validation-
 biochem               testbench       stats
 novel
   │
 L3: עובדים זמניים — נוצרים לכל משימה צרה (מאמר אחד, חישוב אחד, סימולציה אחת) ונעלמים בסוף
```

| רמה | כמות | קבוע? | תפקיד |
|---|---|---|---|
| L0 מנהל | 1 | כן | בוחר מה הכי חשוב, מאחד תוצאות, מחליט, מדווח לך |
| L1 ראשי חטיבות | 7 | כן | מפרקים את התחום למשימות ומאחדים את התוצאות |
| L2 ראשי צוותים | 27 | כן | מומחים בנושא אחד |
| L3 עובדים | כמה שצריך | לא | משימה צרה אחת כל אחד, עשרות במקביל כשצריך |

## למה לא 100,000 סוכנים
- כל תוצאה של סוכן צריך לבדוק. 100,000 תוצאות אי אפשר לבדוק, ובלי בדיקה הן לא שוות כלום.
- סוכנים רבים שקוראים את אותם מאמרים הם לא ראיות נפרדות: הם חוזרים על אותה טעות.
- זה עולה המון כסף וזמן, והמגבלה האמיתית היא פיזיקה ונתונים, לא ידיים.
- במקום זה, מספר העובדים (L3) גדל לפי הצורך: משימת סקירה של 40 מאמרים = 40 עובדים במקביל.

## איך מפעילים
בשיחה עם Claude Code בתוך המאגר: "תפעיל את fatmap-director ותתחיל את חודש 1", או ישירות סוכן מסוים:
"תפעיל את fatmap-lead-biochem ותבדוק את השערת flux + anchor".
הגדרות הסוכנים: `.claude/agents/fatmap-*.md` בשורש המאגר. החוקים המשותפים: `CHARTER.md`.
