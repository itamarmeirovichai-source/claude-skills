"""Model parameters per firm, taken from rules/*.csv (2026-10-11).

Units: start in $; dd, dll, targets, payout_base, payout_cap, qual_min,
lock fractions are FRACTIONS of start; fee, activation, monthly, refund,
payout_min, caps (ladder) and fixed_year are $. Time in trading days
(30 calendar days = 21, 14 calendar days = 10).

`slots` = accounts per person at the firm's cap for this program.
`auto` = is fully automatic trading on FUNDED accounts allowed?
  yes / conditional / unknown / no  (see rules/*.csv and verifier.csv).
`hold` = may positions be held overnight and over the weekend?
Rules NOT modeled are listed in `unmodeled`.
"""

FUT = 50_000.
FX = 100_000.


def _f(x):          # $ on a 50K futures account -> fraction
    return x / FUT


FIRMS = {
    # ------------------------------------------------------------ futures
    "Topstep XFA 50K": dict(
        start=FUT, fee=49., monthly=49., activation=149., targets=[0.06],
        min_days=[2], time_limit=None, dd_type="trail_eod", dd=_f(2000),
        dd_lock=0.0, dll=None,
        funded=dict(split=0.9, first_wait=5, cycle=1, qual_days=5,
                    qual_min=_f(150), payout_frac=0.5, payout_cap=_f(2000),
                    payout_min=125., lock_on_payout=0.0),
        fixed_year=29 * 12 / 5, slots=5, auto="conditional", hold=False,
        unmodeled="ProjectX API only, no VPS (own computer); Live Funded move ends API use; "
                  "eval best-day 50-55% consistency; optional $1,000 DLL not chosen"),
    "Bulenox Master 50K": dict(
        start=FUT, fee=175., activation=148., targets=[0.06], min_days=[1],
        time_limit=[21], dd_type="trail_eod", dd=_f(2500), dd_lock=_f(100),
        dll=_f(1100), dll_hard=False,
        funded=dict(split=0.9, split_full_until=10_000., cycle=10,
                    payout_base=_f(2600), payout_min=1000.,
                    payout_caps=[1500., 1500., 1500., 1e9]),
        fixed_year=100 * 12 / 5, slots=5, auto="yes", hold=False,
        unmodeled="40% payout consistency; Rithmic only, +$100/month third-party API; "
                  "DLL removed once drawdown locks (kept here, conservative)"),
    "Lucid Flex 50K": dict(
        start=FUT, fee=146., targets=[0.06], min_days=[2], time_limit=None,
        dd_type="trail_eod", dd=_f(2000), dd_lock=_f(100), dll=None,
        funded=dict(split=0.9, cycle=1, qual_days=5, qual_min=_f(150),
                    payout_frac=0.5, payout_cap=_f(2000), payout_min=500.,
                    max_payouts=5, lock_on_payout=_f(100)),
        slots=5, auto="yes", hold=False,
        unmodeled="eval 50% consistency; after 5 payouts live review (treated as closure); "
                  "no hedging across accounts"),
    "Tradeify Select 50K": dict(
        start=FUT, fee=165., targets=[0.06], min_days=[3], time_limit=None,
        dd_type="trail_eod", dd=_f(2000), dd_lock=_f(100), dll=None,
        funded=dict(split=0.9, cycle=1, qual_days=5, qual_min=_f(150),
                    payout_frac=0.5, payout_cap=_f(2500), payout_min=250.),
        slots=5, auto="conditional", hold=False,
        unmodeled="bot must be used at Tradeify only; eval 40% consistency; >50% of profit "
                  "from trades held >10 s"),
    "MFFU Rapid EOD 50K": dict(
        start=FUT, fee=135., targets=[0.06], min_days=[4], time_limit=None,
        dd_type="trail_eod", dd=_f(2000), dd_lock=_f(100), dll=None,
        funded=dict(split=0.9, cycle=1, payout_base=_f(2100), payout_min=500.),
        slots=3, auto="conditional", hold=False,
        unmodeled="eval 30% consistency; flat around tier-1 news; auto Live at $10k/day; "
                  "unattended-bot wording conflicts (third party)"),
    "Apex EOD PA 50K": dict(
        start=FUT, fee=119., activation=140., targets=[0.06], min_days=[1],
        time_limit=[21], dd_type="trail_eod", dd=_f(2000), dd_lock=_f(100),
        dll=_f(1000), dll_hard=False,
        funded=dict(split=1.0, cycle=1, qual_days=5, qual_min=_f(250),
                    payout_base=_f(2100), payout_min=500., max_payouts=6,
                    payout_caps=[1500., 1500., 2000., 2500., 2500., 3000.]),
        slots=20, auto="no", hold=False,
        unmodeled="automation BANNED on PA; 50% payout consistency; tiered DLL"),
    # ------------------------------------------------------------- crypto
    "HyroTrader 2-Step 100K": dict(
        start=FX, fee=599., refund=599., targets=[0.10, 0.05], min_days=[5, 5],
        time_limit=None, dd_type="static", dd=0.10, dll=0.05,
        funded=dict(split=0.8, cycle=5, payout_min=125.),
        slots=2, auto="yes", hold=True,
        unmodeled="eval best day <=40% of target; 3% max loss per trade; margin <=25%, "
                  "notional <=2x; own strategy only"),
    "Breakout 1-Step 100K": dict(
        start=FX, fee=800., targets=[0.10], min_days=[0], time_limit=None,
        dd_type="static", dd=0.06, dll=0.03,
        funded=dict(split=0.8, cycle=5, payout_min=63.),
        slots=2, auto="unknown", hold=True,
        unmodeled="bots not addressed by firm; bans off-the-shelf strategies; leverage caps"),
    "CFT 2-Phase 100K": dict(
        start=FX, fee=660., targets=[0.08, 0.05], min_days=[0, 0],
        time_limit=None, dd_type="static", dd=0.10, dll=0.05,
        funded=dict(split=0.8, first_wait=5, cycle=15),
        slots=3, auto="yes", hold=True,
        unmodeled="$10k max profit per day/trade; fee unverified"),
    # -------------------------------------------------------------- forex
    "Alpha Swing 2-Step 100K": dict(
        start=FX, fee=577., targets=[0.10, 0.05], min_days=[3, 3],
        time_limit=None, dd_type="static", dd=0.10, dll=0.05,
        funded=dict(split=0.8, cycle=5, payout_min=2000.),
        slots=4, auto="no", hold=True,
        unmodeled="autonomous EAs BANNED; 2% floating loss per asset; 40% best-day rule; "
                  "one asset per funded account"),
    "E8 Pro Forex 100K": dict(
        start=FX, fee=568., targets=[0.08], min_days=[0], time_limit=None,
        dd_type="static", dd=0.08, dll=0.025, lock_on_payout=0.0,
        funded=dict(split=0.8, cycle=5, payout_frac=0.5, payout_min=1000.),
        slots=5, auto="yes", hold=True,
        unmodeled="only 2%/day of profit counts; E8 Pro Crypto is a second $500K market "
                  "(another 5 slots, rules partly unverified); refund policy unknown"),
    "Blue Guardian 2-Step 100K": dict(
        start=FX, fee=347., refund=347., refund_after=4,
        targets=[0.08, 0.04], min_days=[3, 3], time_limit=None,
        dd_type="static", dd=0.08, dll=0.04,
        funded=dict(split=0.85 * 0.97, first_wait=10, cycle=10, payout_min=100.,
                    dll=0.02),
        slots=4, auto="yes", hold=True,
        unmodeled="Guardian Shield -2% open P&L modeled as a hard 2% daily loss on funded "
                  "(first trigger really cuts split to 50%, second breaches); min days need "
                  ">=0.5% profit each; no trades +-5 min of high-impact news"),
    "FTMO Swing 2-Step 100K": dict(
        start=FX, fee=510., refund=510., targets=[0.10, 0.05], min_days=[4, 4],
        time_limit=None, dd_type="static", dd=0.10, dll=0.05,
        funded=dict(split=0.8, first_wait=10, cycle=10, payout_min=50.),
        slots=4, auto="yes", hold=True,
        unmodeled="fee EUR 439 promo ~ $510; scaling (+25% per 4 months) ignored; "
                  "gambling clause; server limits 200 orders/2000 positions a day"),
    "The5ers High Stakes 100K": dict(
        start=FX, fee=455., refund=0.7 * 455., targets=[0.08, 0.05], min_days=[3, 3],
        time_limit=None, dd_type="static", dd=0.08, dll=0.04,
        funded=dict(split=0.8, first_wait=10, cycle=10, payout_cap=0.04,
                    payout_min=500.),
        slots=1, auto="yes", hold=True,
        unmodeled="one High Stakes account per person; scaling to $500K and split to 100% "
                  "ignored (conservative); 8% vs 10% drawdown conflict (8% used); min days "
                  "must be profitable >=0.5%; no orders +-2 min of high-impact news"),
    "FundedNext Stellar 2-Step 25K": dict(
        start=25_000., fee=250., targets=[0.08, 0.05], min_days=[4, 4],
        time_limit=None, dd_type="static", dd=0.10, dll=0.05,
        funded=dict(split=0.8, first_wait=15, cycle=10),
        slots=1, auto="conditional", hold=True,
        unmodeled="EAs banned on >=$50K; EA add-on price unknown (+25% assumed); "
                  "no identical trades across accounts, no copying -> 1 slot per strategy; "
                  "3% max open risk; news-window profits count 40%"),
    "FTUK Flex 100K": dict(
        start=FX, fee=9., activation=672., targets=[0.04], min_days=[1],
        time_limit=None, dd_type="trail_eod", dd=0.06, dd_lock=0.0, dll=0.02,
        funded=dict(split=0.6, cycle=5),
        slots=1, auto="unknown", hold=True,
        unmodeled="'risk-management EAs' wording vs 'EAs/Bots allowed' (unverified); "
                  "-2% Account Protector modeled as hard 2% daily loss; each account a different "
                  "strategy, no copying -> 1 slot; consistency score on payouts; split 60% at L1"),
}

SHARPES = [0.0, 0.8, 1.0, 1.17, 1.2, 1.5, 2.0]
