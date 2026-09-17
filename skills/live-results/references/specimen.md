# Specimen & Variants

Read this when you need the format concretely: the gold-standard example with each move marked, the same update written badly, and variants for other kinds of live results.

---

## The gold standard

A forward-test ledger for a trading strategy, reported to its owner. Hebrew, because that's the reader's language.

> אנחנו ב−2.15% אחרי 14 ימים שנספרו, כלומר −$2,154 לחשבון של $100K. לא השתנה מאז הבדיקה הקודמת.
>
> - אתמול (9 בספטמבר): −0.69%.
> - היום הכי טוב עד עכשיו: +1.08%. הכי גרוע: −1.81%.
> - ה-10 בספטמבר: עדיין מחכה למחירים מאסיה. הבוט יחשב אותו הלילה ב-18:30, בעוד בערך 45 דקות.
>
> אחרי 14 ימים זה עדיין רעש. גם כשהאסטרטגיה עובדת כמו בבקטסט, בערך חלון אחד מכל 12 נראה ככה.

English rendering of the same update:

> We're at −2.15% after 14 days counted, so −$2,154 on a $100K account. No change since the last check.
>
> - Yesterday (Sept 9): −0.69%.
> - Best day so far: +1.08%. Worst: −1.81%.
> - Sept 10: still waiting on Asian prices. The bot computes it tonight at 18:30, about 45 minutes out.
>
> After 14 days this is still noise. Even when the strategy performs exactly like the backtest, roughly 1 window in 12 looks like this.

### Why it works, move by move

| Line | Move | What it does |
|---|---|---|
| `−2.15% ... −$2,154 on a $100K account` | 1 — two units | The percent is comparable, the dollar figure is felt. Neither alone is enough. |
| `after 14 days counted` | 4 — partial count, stated up front | The denominator is in the headline, not a footnote. The reader can never mistake this for a full month. |
| `No change since the last check` | 2 — movement | Answers "do I need to do anything?" before the reader has to ask. |
| `Yesterday: −0.69%` / `Best: +1.08%. Worst: −1.81%` | 3 — three anchors | The −2.15% didn't come from one blowup. Daily swings run ±1–2%. That reframes the headline without arguing about it. |
| `Sept 10: still waiting on Asian prices ... 18:30, about 45 minutes out` | 4 — what's missing | Names the gap, the cause, the mechanism, and the wait. Nothing for the reader to chase. |
| `roughly 1 window in 12 looks like this` | 5 — base rate | The load-bearing line. A frequency, derived from the backtest's own distribution, that tells the reader exactly how much to care. |
| *(nothing after it)* | 6 — no action | Fourteen days of noise doesn't support a decision, so none is offered. |

Note what's absent: no bold, no headers, no emoji, no "unfortunately," no "on the bright side," no closing question.

---

## Before / after

Same facts. First, an ordinary status update:

> **Performance Update** 📊
>
> Great question! Here's where things stand. The forward test is currently showing a **drawdown of -2.15%**, which, while not ideal, is well within expected parameters for this stage. It's important to note that short-term fluctuations are a normal part of any trading strategy, and we shouldn't read too much into early results.
>
> **Key highlights:**
> - Yesterday saw a modest decline
> - We've had some strong days as well
> - One day is still pending
>
> Overall, the strategy is performing as expected and we should continue to monitor closely. Let me know if you'd like me to dig deeper into any of these numbers!

What's wrong with it:

- **No second unit.** −2.15% of what? The reader has to do the multiplication.
- **"Within expected parameters" is the fake version of move 5.** It asserts normality without a frequency. Nothing to check, nothing to disagree with.
- **The anchors are adjectives.** "A modest decline," "some strong days" — the real numbers (−0.69%, +1.08%, −1.81%) were available and got replaced with mood.
- **The pending day has no time and no cause.** "One day is still pending" leaves the reader to chase it.
- **"Performing as expected" is a claim about the strategy** made on a sample that can't support it. This is exactly the sentence the format exists to stop.
- **"Continue to monitor closely" is an invented action item**, and the closing offer undoes the last line's job.

The good version is shorter and says more, which is the usual result.

---

## Variants

### A/B test, midway

> Variant B is up 4.1% on signup rate — 312 signups vs 300 on the same traffic, 9 days in. Unchanged since Tuesday.
>
> Daily lift has run between −6% and +11%. Neither arm has led for more than three days running.
>
> That 4.1% is inside the noise band: with this traffic, two identical variants finish 9 days more than 4% apart about a third of the time. The test separates at roughly 2,400 signups per arm, which is late next week at current volume.

### Ad campaign, first week

> Week one: $3,180 spent, 41 leads, $77.56 a lead. Target was $60.
>
> Best day was Thursday at $52 a lead, worst was Sunday at $140. Monday's numbers land in the dashboard around noon.
>
> I don't have enough history on this account to say how unusual $77 is for a first week — there's no prior campaign at this budget to compare against. Forty-one leads is a small enough count that one good day moves the average by $10. Ask again at 150 leads, roughly three weeks out.

That last variant is the honest handling of the no-base-rate case: name the gap, show the sensitivity instead (one good day = $10), and give a date. What it never does is guess a frequency.

### A good number, same treatment

> Up 6.4% after 21 days, so +$6,400 on the $100K. Best stretch since the forward test started.
>
> Best day +2.2%, worst −1.4%, twelve up days out of twenty-one.
>
> Still noise, same as the drawdown three weeks ago was: about one window in seven beats +6% even with the backtest's own numbers. Nothing here says the strategy is working better than it was. Sixty days is where this starts to mean something.

If the format only shows up when the number is bad, it isn't a format — it's an excuse. This is the test of whether you've actually adopted it.
