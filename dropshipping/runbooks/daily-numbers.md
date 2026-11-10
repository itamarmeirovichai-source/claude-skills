# Runbook: daily numbers into the ledger (manual first, then `phase3/reconcile.py`)

מי מבצע: המפעיל, 10 דקות ביום, מיום ההזמנה האמיתית הראשונה. אחרי 3 ריצות ידניות יציבות, הסקריפט מריץ את אותו הצ'קליסט.

## מה אוספים (ייצוא CSV)
1. Shopify → Orders → Export (היום הקודם): `shopify_orders.csv` בעמודות `order_id, created_at, gross_usd, status, tags`.
2. שער הסליקה / PayPal → Activity/Payouts export: `payouts.csv` בעמודות `order_id, payout_date, net_usd, currency_rate, fee_usd`.
3. החזרים וצ'ארג'בקים: `refunds.csv` בעמודות `order_id, refund_date, amount_usd, kind`.
4. Meta Ads Manager → Export (יום): `meta_purchases.csv` בעמודות `date, purchases, spend_usd`.

## שמונה השאלות (הסקריפט שואל אותן בדיוק כך)
1. יש מזהה הזמנה כפול? 2. הזמנות בדיקה/צוות הוצאו? 3. יש הזמנה "שולמה" בלי תשלום מהמעבד אחרי 45 יום? (זו הזמנה מזויפת או בעיה) 4. יש תשלום בלי הזמנה? 5. תשלום שתאריכו לפני ההזמנה? 6. החזרים נרשמו לחודש של ההחזר, לא של ההזמנה? 7. ההכנסה היא הנטו של המעבד, בשער שלו? 8. מספר הרכישות של Meta מוצג ליד מספר ההזמנות של Shopify, ולא במקומן?

## הרצה
```bash
python3 -I dropshipping/phase3/reconcile.py --dir exports/2026-12 --period 2026-12
```
יציאה 2 = יש ממצא SUSPECT/LEAK/DUPLICATE; המספרים לא נכנסים לספר עד שהממצא מוסבר בשורת הערה.

## מה נכנס לספר
`ledger.md` שורת שבוע: הזמנות משוחזרות, הכנסה משוחזרת, הוצאת Meta, ROAS משוחזר, החזרים, צ'ארג'בקים, תאריך שחזור. תזכורת: מה שמופיע בלוח של Meta הוא לא רווח.

## בדיקה עצמית של הכלי (פעם בשבוע)
```bash
python3 -I dropshipping/phase3/reconcile.py --selftest
```
חייב להדפיס `planted problems caught: True` ו-`placebo clean: True`. אם לא, הכלי שבור ושום מספר ממנו לא נספר (חוק 5.2).
