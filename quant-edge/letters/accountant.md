# Accountant — classification of prop-firm payouts for an Israeli resident (send before the first funded account)

**Paste into:** an email to your own accountant (רואה חשבון) — no address fetched; this is Itamar's own contact. Timing per the inherited plan: when a variant first reaches Gate 5, and in any case before the first purchase.

**Subject:** Classification of "funded trading" payouts from US and Czech firms — written opinion requested before the first payment

Dear [Accountant],

I am about to start receiving payments from so-called proprietary-trading ("funded account") firms and would like your written opinion on how this income is classified, taxed and reported in Israel before the first payment arrives.

**The facts**

- Payers: US companies (Topstep LLC, TradeDay LLC, MyFunded Futures LLC, Bulenox LLC, Lucid Trading) and a Czech company (FTMO s.r.o.); payee: me, a private individual resident in Israel.
- I buy and sell no securities. Trading takes place in a simulated account on the firm's platform with the firm's simulated capital. The payment is contractual consideration (a "reward" or "payout") for performance in that account, typically 80–90% of the simulated profit.
- The activity is frequent, systematic and automated: a program I wrote trades daily on several accounts in parallel, and I intend to continue for years and to scale to 10–20 accounts.
- Recurring costs: evaluation fees, activation and reset fees, platform and market-data fees, commissions passed through by the firm, hosting.
- Payment rails: international bank wire, Wise / Rise (Riseworks), Visa Direct, crypto. US firms issue Form 1099 to US persons; I expect to be asked for a W-8BEN.

**The questions**

1. Is this business income (הכנסה מעסק, marginal rates plus National Insurance) or a capital gain (רווח הון, 25%)? Which of the facts above decide it?
2. If business income: the National Insurance rate and advance-payment (מקדמות) obligations.
3. Should it run through a company, and from what income level does that stop being premature?
4. Are evaluation, activation and reset fees deductible, including for accounts that fail and pay nothing?
5. US withholding, W-8BEN, and foreign tax credit against Israeli tax.
6. Reporting and timing: opening a file at the Tax Authority, VAT status (עוסק פטור / מורשה — is this a VAT-able export of services?), the annual return, anything triggered by the first payment.
7. Records to keep from day one, and the treatment of payouts received in crypto.

Please answer in writing; from the first payout I will set aside the percentage you name into a separate account.

Kind regards,
[Name], ID [number]

---

**תשובה שימושית חייבת לכלול:** סיווג חד-משמעי (עסק / הון) עם הנימוק לפי העובדות; שיעורי מס וביטוח לאומי ומקדמות; מעמד מע"מ; ניכוי דמי אבלואציה גם על חשבונות שנכשלו; W-8BEN וזיכוי מס זר; אילו רישומים לשמור מהיום הראשון; טיפול בתשלומים בקריפטו.
**תשובה שמשנה את התוכנית (אין "הורג" כאן):** סיווג כהכנסה מעסק בשיעור שולי + ביטוח לאומי מעלה את הסף הנדרש לאדג' בכשליש לעומת 25% (מורשת F2/D1) — המספרים ב-economics חייבים לרוץ מחדש עם השיעור שרואה החשבון נוקב; חובת מע"מ או חברה משנה את מבנה העלויות.

---

**Sources:**
- Inherited draft: `~/quant-edge-inherited/pr4/skills/prop-fleet/references/verification-letters.md`, section 2 (facts and the seven questions; the "about a third" sensitivity is the inherited claim there, not recomputed here).
- `~/quant-edge-inherited/pr26/prompts/research/firms-2026-10-11.md` ("Israeli tax classification of payouts (business income vs capital gains changes the required edge by about a third); the accountant letter goes out when a variant first reaches Gate 5, before any purchase").
- Payment rails and entities as fetched 2026-11-03 for the firm letters in this folder (FTMO reward methods; Topstep Wire/SWIFT; TradeDay Riseworks; MFFU privacy policy naming Riseworks, Wise, Confirmo; Topstep/MFFU 1099 articles exist for US persons).
