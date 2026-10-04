# MeiroX Prop Fleet — the agent organization

Built 4 Oct 2026 at Itamar's request: an organization of agents that researches
every day on its own, with heads and workers, each in a different domain, each
knowing what the others do, all with one shared goal.

## The goal (shared by everyone)

**More than 20% a year, net of every cost and tax, from many funded prop
accounts.**

## The two things that cannot change (Itamar's words)

1. **Fully automatic.** The bot trades with no human in the loop.
2. **Many funded accounts can be bought on it.**

Everything else may change: the strategy, the instrument, the timeframe, the
firm, the sizing, the code.

## What these two rules already imply (found 4 Oct)

- **Apex is out as the main firm.** Third-party summaries of its User Agreement
  say automated order submission is forbidden on funded (PA) accounts. Rule 1
  rules it out unless Apex answers otherwise in writing (asked 20 + 29 Sep).
- **Firms that reportedly allow full automation:** MyFundedFutures, Bulenox,
  Tradeify, Lucid; Topstep on Express Funded accounts, via its ProjectX API, with
  the code running on the trader's own computer (not a VPS). Most cap accounts
  at about 5 per firm, so "many accounts" means about 20 spread over four
  firms, not 20 at one. Every one of these is a claim to verify, not a fact.

## The organization

| Level | Role | Domain |
|---|---|---|
| Director | ראש ההנהלה | Reads every division, decides the day, writes the board and the report to Itamar |
| Head | ראש חטיבת מחקר קצה | Finding an edge the structure can use |
| Worker | חוקר ספרות | New papers, replications and public results on intraday futures edges |
| Worker | צייד נתונים | Free intraday and daily data reachable from here (GitHub raw, PyPI) |
| Worker | בונה השערות | Writes one pre-registered hypothesis a day and backtests it |
| Head | ראש חטיבת מבנה פרופ | Which firms, which rules, what it pays |
| Worker | שומר כללים | Automation, drawdown, account caps, payouts per firm |
| Worker | כלכלן | Runs apex_model-style economics per firm at the measured edge |
| Head | ראש חטיבת סטטיסטיקה וסיכון — has a veto | Nothing is called an edge without passing the gate |
| Worker | סטטיסטיקאי | Checks every claimed result against the gate and the ledger |
| Worker | צוות אדום | Tries to refute every claim; default is refuted |
| Head | ראש חטיבת הנדסה ותפעול | The repository and the road into the bot |
| Worker | מהנדס | Runs the test suites, fixes what breaks, plans the automation route per allowed firm |

Everyone reads `board.md` (yesterday's state) and `ledger.csv` (every
hypothesis ever tested) before doing anything. Heads see every division's
worker output, not only their own. The director sees everything.

## The gate — the one rule the referee enforces

A strategy may be called an edge, and may be proposed for the bot, only if all
of these hold:

1. Its rules were written in `ledger.csv` **before** its first backtest.
2. Out-of-sample, after realistic costs, the bootstrap 5th percentile of the
   mean R per trade is above zero.
3. The result survives the multiple-testing correction for **N = the sum of
   the `count` column in `ledger.csv`** (every hypothesis and variant ever
   tested, by anyone, any day). Today N = 110.
4. Translated to annual Sharpe at its trade frequency, it reaches about **3**,
   the level at which a 21-day evaluation stops being a lottery
   (`references/stack.md`, section 3).

The ledger is what stops an organization that tests something new every day
from finding "edges" by chance: every day adds to N, and N raises the bar.

## What the organization does not do

- Buy anything, move money, or sign up for anything.
- Touch Itamar's Mac, the bot's live configuration, IBKR or Telegram. It cannot
  reach them. Changes to the bot are proposals until a bot repository is
  attached to this session, and then pull requests, never direct pushes.
- Call a result an edge without the gate.

## Where its output goes

The daily run writes `board.md`, appends to `ledger.csv`, saves the day's full
record under `daily/`, commits, and reports to Itamar in Hebrew in this
conversation.
