# Two letters to send before any money moves

Both of the open questions that block a funded-account plan are answered by
other people, not by analysis. Leaving them as headings ("ask the firm", "see an
accountant") is how they stay open for months. Here they are as text to send.

Neither is advice. The firm's answer and the accountant's answer are the facts;
these letters only make sure the right questions get asked once, in writing.

---

## 1. To the prop firm — automated order copying

**Why this one first.** Every other risk in the plan is bounded by evaluation
fees. This one is not: if the order path is not permitted, accounts are closed
and payouts already earned can be voided. Get the answer in writing, keep the
email, and do not rely on a forum post or a support chat that disappears.

> **Subject:** Rule confirmation before purchase — automated order routing and multiple accounts
>
> Hello,
>
> I am preparing to purchase evaluations and I want to confirm several rules in
> writing before I do, so that I can build my setup to comply from the start
> rather than correct it later.
>
> 1. **Automated order routing.** I intend to run a program that generates
>    signals and submits orders automatically, without manual confirmation of
>    each trade. Is this permitted? If so, which routing methods or third-party
>    platforms are approved, and are there any that are explicitly prohibited?
>
> 2. **Copying across my own accounts.** If I hold multiple accounts under my own
>    name, may the same orders be placed across all of them simultaneously, and
>    up to how many accounts? Please confirm whether any approved copy-trading
>    tool is required, or whether direct API submission to each account is
>    acceptable.
>
> 3. **Payout ladder.** Please confirm the exact per-payout caps for the plan
>    sizes I am considering, stated separately for the EOD and Intraday variants:
>    the six caps in order, and the lifetime total for one account.
>
> 4. **Drawdown figures.** Please confirm the trailing drawdown amount and the
>    safety-net threshold for each of those sizes, and the balance at which the
>    trailing floor locks.
>
> 5. **Consistency rule.** Please confirm the current percentage, and whether it
>    is evaluated against profit at the time of the payout request or over the
>    account's life.
>
> 6. **After the final payout.** When an account reaches its last permitted
>    payout, is the account closed, or can it be re-qualified?
>
> Thank you — a written confirmation of these six points is all I need.

**What to do with the answer.** Item 1 is a stop/go. If automated routing is not
permitted, or is permitted only through a tool the bot cannot use, the plan needs
rebuilding before anything is purchased, not after. Items 3–5 replace the values
in `apex-rules.md` that public sources disagree on — update that file and re-run
the model, because the payout ladder is the single biggest input to it.

---

## 2. To the accountant — how this income is classified

**Why it matters.** The difference between the two plausible classifications is
larger than most of the trading decisions in the plan. Modelled over eight years
at the same performance, it is **$507,154** — 24.6% a year against 17.4%, or 7.2
percentage points of return for one hour of a professional's time. It is worth
that hour before the first account is bought, not after the first payout arrives.

(An earlier draft of this file said $643,000. That paired a 47% figure from one
model configuration against a 25% figure from another and overstated the gap by
about $136,000. `scripts/claims.py` recomputes it.)

**And read the facts below before assuming the good number.** Every one of them
argues *against* the 25% treatment: nothing is owned, nothing is sold, the
account is simulated, the payment is contractual consideration for a result, and
the activity is daily and automated. The model's 25% base case is therefore the
optimistic branch, not the neutral one. Until an accountant says otherwise in
writing, plan on 17.4% and treat 24.6% as the upside.

Bring these facts, and ask these questions.

**The facts they need:**

- The payments come from a **US company**, to a private individual resident in
  Israel.
- The money is **not** proceeds from selling securities. No securities are owned
  at any point. The trading happens in a **simulated account** on the firm's own
  platform, using the firm's simulated capital.
- The payment is made under a contract for **performance in that simulated
  account** — economically closer to a fee for a result than to a capital gain.
- The activity is **frequent, systematic and automated** — a program trading
  daily, not occasional discretionary decisions.
- There are recurring **costs**: evaluation fees, account activation fees,
  broker commissions, data and infrastructure.
- The plan is to scale to **10–20 accounts** and to continue for years.

**The questions:**

1. Is this income from a business (`הכנסה מעסק`, marginal rates) or a capital
   gain (`רווח הון`, 25%)? Which facts above drive the answer?
2. If it is business income, does National Insurance apply, and at what rate?
3. Should this be run through a company, and at what income level does that stop
   being premature?
4. Are the evaluation and activation fees deductible against this income —
   including the fees for accounts that fail and produce nothing?
5. What US withholding applies, is a W-8BEN required, and does a foreign tax
   credit apply against Israeli tax?
6. What is the reporting obligation and its timing — advance payments, annual
   return, anything triggered by the first payment received?
7. What records should be kept from day one so that the classification can be
   supported later?

**What to do with the answer.** Set aside the stated percentage from every
payout on the day it arrives, into a separate account. Until an accountant says
otherwise, reserve at the higher rate. Over-reserving is an inconvenience;
under-reserving for two years while the plan compounds is not.
