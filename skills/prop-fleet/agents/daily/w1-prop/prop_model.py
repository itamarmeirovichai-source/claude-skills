"""COPY of scripts/apex_model.py (D1, wave 1, 2026-10-11), extended with a
Sharpe/volatility daily-return model that covers any prop firm's rules:
static, trailing-intraday and trailing-EOD drawdowns (with lock), hard or soft
daily loss limits, one- or two-phase evaluations with or without a clock,
monthly subscriptions, fee refunds, payout cycles, caps, splits and closure
after N payouts. The original Apex trade-level model below is untouched.

Pre-registered in agents/prereg/D1.csv (D1-01..03) before the first run.

Original docstring: Eight-year fleet model: N Apex slots, copy-traded (perfectly correlated),
staggered onboarding, full Apex payout mechanics, costs, tax and the
post-year-4 withdrawal plan.
"""
import numpy as np

DAYS_YEAR, DAYS_MONTH, TRADES_DAY = 250, 21, 3
COMM_RT, SLIP_PTS, MES_PT, STOP_PTS = 1.30, 0.25, 5.0, 8.5
MIN_PAYOUT, QUAL_DAYS, CONSIST = 500.0, 5, 0.50

PLANS = {
    # $2,500 is the LEGACY drawdown (plans bought before 1 Mar 2026). Kept
    # so the documented numbers stay reproducible; new purchases are 50K-2026.
    "50K": dict(start=50_000., dd=2_500., target=3_000., qmin=200.,
                ladder=[1500., 1500., 2000., 2500., 2500., 3000.],
                evalfee=40., activation=85.),
    # Post-March-2026 50K: $2,000 trailing drawdown (see references/apex-rules.md,
    # correction of 29 Sep 2026). Same ladder and target.
    "50K-2026": dict(start=50_000., dd=2_000., target=3_000., qmin=200.,
                     ladder=[1500., 1500., 2000., 2500., 2500., 3000.],
                     evalfee=40., activation=85.),
    # 150K ladder is the conservative reading of conflicting public sources
    "150K": dict(start=150_000., dd=5_000., target=9_000., qmin=350.,
                 ladder=[2500., 2500., 3000., 3000., 3500., 3500.],
                 evalfee=90., activation=125.),
}


EVAL_TRADING_DAYS = 21          # 30 calendar days, hard expiry, no extension


def simulate(plan="50K", slots=20, avg_R=0.30, risk_pct=0.04, years=8,
             n=1500, rr=2.0, seed=11, onboard_per_month=1, tax=0.25,
             correlated=True, risk_pct_eval=None, risk_pct_locked=None,
             persistence=0.5, spread=0.0):
    P = PLANS[plan]
    START, DD = P["start"], P["dd"]
    SAFETY, LOCK = START + DD + 100., START + 100.
    LAD = np.array(P["ladder"]); NP_ = len(LAD)
    risk = risk_pct * DD
    risk_e = (risk_pct_eval or risk_pct) * DD
    # סיכון אחרי נעילת הרצפה. לפני הנעילה כל הפסד גורר את הרצפה
    # איתו, ואחריה היא מקובעת ב-START+100 לנצח — כלומר רק
    # 2,600 הדולרים הראשונים מסוכנים באמת. שני המצבים האלה אינם
    # אותו הימור, ולסכן בהם אותו דבר זה לוותר על הבדל חוזי ודאי.
    risk_l = (risk_pct_locked or risk_pct) * DD
    k = max(1, round(risk / (STOP_PTS * MES_PT)))
    ke = max(1, round(risk_e / (STOP_PTS * MES_PT)))
    kl = max(1, round(risk_l / (STOP_PTS * MES_PT)))
    comm, slip = k * COMM_RT, k * SLIP_PTS * MES_PT
    comm_e, slip_e = ke * COMM_RT, ke * SLIP_PTS * MES_PT
    comm_l, slip_l = kl * COMM_RT, kl * SLIP_PTS * MES_PT
    p = (avg_R + 1.0) / (rr + 1.0)
    # Two market regimes whose stationary mixture gives exactly avg_R, so a
    # clustered run and an i.i.d. run carry the same edge and differ only in
    # the SHAPE of the sequence. persistence=0.5, spread=0 is i.i.d.
    p_good, p_bad = p + spread, p - spread
    # Strict bounds would reject p=0 and p=1, which are legitimate: avg_R=-1
    # is always-lose and avg_R=rr is always-win. Only reject a spread that
    # actually pushes a probability outside [0, 1].
    if not (0.0 <= p_bad and p_good <= 1.0):
        raise ValueError(f"spread {spread} impossible at avg_R {avg_R}")
    rng = np.random.default_rng(seed)
    shape = (n, slots)
    good = rng.random(n) < 0.5          # the regime is the market's, shared

    bal   = np.full(shape, START); peak = np.full(shape, START)
    floor = np.full(shape, START - DD)
    lock  = np.zeros(shape, bool); ispa = np.zeros(shape, bool)
    npay  = np.zeros(shape, int);  qual = np.zeros(shape, int)
    dpnl  = np.zeros(shape);       mday = np.zeros(shape)
    edays = np.zeros(shape, int)                  # trading days used in evaluation
    active= np.zeros(shape, bool)                 # slot has a running account
    opened= np.zeros(shape, bool)                 # slot has been onboarded
    cash  = np.zeros(n)                           # gross withdrawn, cumulative
    spend = np.zeros(n)                           # fees paid, cumulative
    attempts = np.zeros(shape, int)
    yearly_gross = np.zeros((n, years))
    yearly_fees  = np.zeros((n, years))
    burned = np.zeros(n)

    def fresh(mask):
        nonlocal bal, peak, floor, lock, ispa, npay, qual, mday, active, spend, attempts, edays
        bal = np.where(mask, START, bal); peak = np.where(mask, START, peak)
        floor = np.where(mask, START - DD, floor)
        lock &= ~mask; ispa &= ~mask
        npay = np.where(mask, 0, npay); qual = np.where(mask, 0, qual)
        mday = np.where(mask, 0.0, mday)
        edays = np.where(mask, 0, edays)
        attempts = attempts + mask
        active |= mask

    total_days = years * DAYS_YEAR
    for d in range(total_days):
        yr = d // DAYS_YEAR
        # onboarding: open new slots on a monthly cadence
        if d % DAYS_MONTH == 0:
            want = min(slots, (d // DAYS_MONTH + 1) * onboard_per_month)
            col = np.arange(slots)[None, :] < want
            new = col & ~opened
            if new.any():
                m = np.broadcast_to(new, shape) & ~opened
                opened |= m
                fresh(m)
                fee = m.sum(axis=1) * P["evalfee"]
                spend += fee; yearly_fees[:, yr] += fee

        for _ in range(TRADES_DAY):
            good = np.where(rng.random(n) > persistence, ~good, good)
            pr = np.where(good, p_good, p_bad)
            if correlated:
                r = np.where(rng.random(n) < pr, rr, -1.0)[:, None]
            else:
                r = np.where(rng.random(shape) < pr[:, None], rr, -1.0)
            # שלושה מצבים, לא שניים: הערכה, ממומן לפני נעילה,
            # וממומן אחרי נעילה.
            fund = np.where(lock, risk_l, risk)
            fcm = np.where(lock, comm_l, comm)
            fsl = np.where(lock, slip_l, slip)
            sz  = np.where(ispa, fund, risk_e)
            cm  = np.where(ispa, fcm, comm_e)
            sl  = np.where(ispa, fsl, slip_e)
            net = r * sz - cm - np.where(r < 0, sl, 0.0)
            bal = np.where(active, bal + net, bal)
            dpnl = np.where(active, dpnl + net, dpnl)
            up = active & (bal > peak)
            peak = np.where(up, bal, peak)
            hit = up & ~lock & (peak >= SAFETY)
            floor = np.where(hit, LOCK, np.where(up & ~lock, peak - DD, floor))
            lock |= hit
            dead = active & (bal <= floor)
            if dead.any():
                active &= ~dead
                burned += dead.sum(axis=1)

        edays += (active & ~ispa)
        qual += (active & (dpnl >= P["qmin"]))
        mday = np.where(active & (dpnl > mday), dpnl, mday)
        dpnl = np.zeros(shape)

        pass_ = active & ~ispa & (bal >= START + P["target"])
        if pass_.any():
            bal = np.where(pass_, START, bal); peak = np.where(pass_, START, peak)
            floor = np.where(pass_, START - DD, floor)
            lock &= ~pass_
            qual = np.where(pass_, 0, qual); mday = np.where(pass_, 0.0, mday)
            ispa |= pass_
            fee = pass_.sum(axis=1) * P["activation"]
            spend += fee; yearly_fees[:, yr] += fee

        expired = active & ~ispa & (edays >= EVAL_TRADING_DAYS)
        if expired.any():
            active &= ~expired

        el = active & ispa & (qual >= QUAL_DAYS) & (npay < NP_)
        if el.any():
            cap = LAD[np.clip(npay, 0, NP_ - 1)]
            last = npay == NP_ - 1
            keep = np.where(last, LOCK, SAFETY)
            amt = np.minimum(cap, bal - keep)
            profit = bal - START
            enough = (amt >= cap) | (last & (amt >= MIN_PAYOUT))
            ok = el & enough & ~((profit > 0) & (mday > CONSIST * profit))
            if ok.any():
                bal = np.where(ok, bal - amt, bal)
                got = np.where(ok, amt, 0.0).sum(axis=1)
                cash += got; yearly_gross[:, yr] += got
                npay = np.where(ok, npay + 1, npay)
                qual = np.where(ok, 0, qual); mday = np.where(ok, 0.0, mday)
                active &= ~(ok & (npay >= NP_))

        # any opened slot without a live account restarts a fresh evaluation
        restart = opened & ~active
        if restart.any():
            fresh(restart)
            fee = restart.sum(axis=1) * P["evalfee"]
            spend += fee; yearly_fees[:, yr] += fee

    net_year = (yearly_gross - yearly_fees)
    net_year = np.where(net_year > 0, net_year * (1 - tax), net_year)
    return dict(plan=plan, slots=slots, avg_R=avg_R, risk_pct=risk_pct,
                risk=risk, k=k, risk_e=risk_e, ke=ke,
                risk_l=risk_l, kl=kl, net_year=net_year,
                gross=yearly_gross, fees=yearly_fees,
                burned=burned, attempts=attempts.sum(axis=1))


def allocate(net_year, port_r=0.07, biz_r=0.12, start_extract=4):
    """From year 5 on: 25% to a private portfolio, 25% to business/real
    estate, the rest stays in the reserve. Everything compounds."""
    n, years = net_year.shape
    port = np.zeros(n); biz = np.zeros(n); res = np.zeros(n)
    hist = []
    for y in range(years):
        port *= (1 + port_r); biz *= (1 + biz_r)
        cash = net_year[:, y]
        if y >= start_extract:
            a = np.maximum(cash, 0) * 0.25
            port += a; biz += a; res += cash - 2 * a
        else:
            res += cash
        hist.append((res.copy(), port.copy(), biz.copy()))
    return hist


def report(d, label=""):
    ny = d["net_year"]
    tot = ny.sum(axis=1)
    hist = allocate(ny)
    res, port, biz = hist[-1]
    wealth = res + port + biz
    print(f"\n{label}  [{d['plan']} x{d['slots']}, {d['avg_R']:+.2f}R, "
          f"{100*d['risk_pct']:.0f}% of DD = ${d['risk']:.0f}/trade, {d['k']} MES]")
    print(f"  {'year':>5} {'gross':>11} {'fees':>8} {'net after tax':>15}")
    for y in range(ny.shape[1]):
        print(f"  {y+1:>5} {d['gross'][:, y].mean():>11,.0f} "
              f"{d['fees'][:, y].mean():>8,.0f} {ny[:, y].mean():>15,.0f}")
    yrs = ny.shape[1]
    print(f"  accounts burned over {yrs}y (median): {np.median(d['burned']):,.0f}"
          f"   evals bought: {np.median(d['attempts']):,.0f}")
    print(f"  {yrs}-year net after tax:  mean ${tot.mean():>12,.0f}   "
          f"median ${np.median(tot):>12,.0f}   p10 ${np.percentile(tot,10):>11,.0f}")
    print(f"  wealth at year {yrs} (reserve+portfolio+business): "
          f"median ${np.median(wealth):,.0f}   p10 ${np.percentile(wealth,10):,.0f}")
    return tot


# ---------------------------------------------------------------------------
# D1 extension: firm-generic daily model at Sharpe S and annual vol sigma.
# ---------------------------------------------------------------------------
TD = 252                      # trading days per year
SUB = 4                       # intraday sub-steps per day (D1-01)
HORIZON = 3 * TD              # cap on an evaluation attempt and on a funded life
SIGMAS = np.array([1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30, 40]) / 100.0
TAX = 0.25


def _noise(rng, shape, tdist=True, df=5):
    """Unit-variance i.i.d. shocks: Student-t(df) scaled, or Gaussian."""
    if not tdist:
        return rng.standard_normal(shape, dtype=np.float32)
    z = rng.standard_t(df, size=shape).astype(np.float32)
    return z * np.float32(np.sqrt((df - 2) / df))


class _Account:
    """Drawdown / daily-loss state for a batch of accounts (all in $)."""

    def __init__(self, F, shape, start):
        self.F, self.start = F, start
        self.dd = F["dd"] * start
        self.dll = (F.get("dll") or 0) * start
        self.lock = None if F.get("dd_lock") is None else start + F["dd_lock"] * start
        self.bal = np.full(shape, start, np.float32)
        self.peak = np.full(shape, start, np.float32)      # trailing anchor
        self.day0 = np.full(shape, start, np.float32)      # day-start equity
        self.halted = np.zeros(shape, bool)                # soft DLL hit today
        # floor jumps to start + lock_on_payout*start after the first payout
        self.paylock = np.zeros(shape, bool)
        lp = F.get("lock_on_payout")
        self.paylock_at = None if lp is None else start + lp * start

    def reset(self, mask):
        for a in (self.bal, self.peak, self.day0):
            a[mask] = self.start
        self.halted[mask] = False
        self.paylock[mask] = False

    def floor(self):
        if self.F["dd_type"] == "static":
            f = np.float32(self.start - self.dd)
        else:
            f = self.peak - self.dd
            f = f if self.lock is None else np.minimum(f, self.lock)
        if self.paylock_at is not None:
            f = np.where(self.paylock, np.maximum(f, self.paylock_at), f)
        return f

    def step(self, inc, live):
        """One intraday sub-step. Returns mask of accounts breached now."""
        inc = np.where(live & ~self.halted, inc, 0).astype(np.float32)
        self.bal += inc
        if self.F["dd_type"] == "trail_intraday":
            np.maximum(self.peak, self.bal, out=self.peak)
        dead = live & (self.bal <= self.floor())
        if self.dll:
            hit = live & (self.bal <= self.day0 - self.dll)
            if self.F.get("dll_hard", True):
                dead |= hit
            else:                                   # soft: flat for the day
                self.bal = np.where(hit & ~self.halted,
                                    self.day0 - self.dll, self.bal).astype(np.float32)
                self.halted |= hit
        return dead

    def end_day(self):
        if self.F["dd_type"] == "trail_eod":
            np.maximum(self.peak, self.bal, out=self.peak)
        self.day0[:] = self.bal
        self.halted[:] = False


def eval_sim(F, S, sigmas=SIGMAS, n=3000, seed=11, tdist=True, sub=SUB):
    """Evaluation attempts for each sigma. Returns dict of arrays over sigma:
    p_pass, t_pass (mean days | pass), t_fail (mean days | fail),
    fee_pass / fee_fail (mean fees paid inside one attempt)."""
    st = F["start"]; phases = F["targets"]
    if not phases:                                 # instant funding
        z = np.zeros(len(sigmas))
        return dict(p_pass=z + 1, t_pass=z, t_fail=z, fee_pass=z + F["fee"],
                    fee_fail=z + F["fee"])
    k = len(sigmas); shape = (k, n)
    rng = np.random.default_rng(seed)
    sd = (sigmas / np.sqrt(TD)).astype(np.float32)[:, None] * st
    mu = (S * sigmas / TD).astype(np.float32)[:, None] * st
    acc = _Account(F, shape, st)
    live = np.ones(shape, bool); passed = np.zeros(shape, bool)
    phase = np.zeros(shape, int); pdays = np.zeros(shape, int)
    days = np.zeros(shape, int); hit = np.zeros(shape, bool)
    lim = F.get("time_limit")           # list per phase (trading days) or None
    mind = F.get("min_days", [0] * len(phases))
    for d in range(HORIZON):
        if not live.any():
            break
        trade = live & ~hit                # after the target, the bot idles
        for _ in range(sub):
            inc = mu / sub + sd / np.sqrt(sub) * _noise(rng, shape, tdist)
            dead = acc.step(inc, trade)
            live &= ~dead
        acc.end_day()
        days += live; pdays += live
        tgt = np.array(phases)[phase] * st
        hit |= live & (acc.bal >= st + tgt)
        done = live & hit & (pdays >= np.array(mind)[phase])
        last = done & (phase == len(phases) - 1)
        passed |= last; live &= ~last
        nxt = done & ~last
        if nxt.any():
            phase[nxt] += 1; pdays[nxt] = 0; hit[nxt] = False; acc.reset(nxt)
        if lim is not None:
            exp = live & (pdays >= np.array(lim)[phase])
            live &= ~exp
    # a still-live attempt at the horizon counts as a failure (conservative)
    sub_fee = F.get("monthly", 0.0)
    months = np.ceil(np.maximum(days, 1) / 21.0) if sub_fee else 0
    fee = F["fee"] + (months - 1) * sub_fee if sub_fee else np.full(shape, F["fee"])
    out = dict(paths=dict(passed=passed, days=days, fee=np.broadcast_to(fee, shape)))
    pp = passed.mean(1)
    out["p_pass"] = pp
    with np.errstate(invalid="ignore"):
        out["t_pass"] = np.where(pp > 0, (days * passed).sum(1) / np.maximum(passed.sum(1), 1), 0)
        out["t_fail"] = np.where(pp < 1, (days * ~passed).sum(1) / np.maximum((~passed).sum(1), 1), 0)
        out["fee_pass"] = np.where(pp > 0, (fee * passed).sum(1) / np.maximum(passed.sum(1), 1), F["fee"])
        out["fee_fail"] = np.where(pp < 1, (fee * ~passed).sum(1) / np.maximum((~passed).sum(1), 1), F["fee"])
    return out


def funded_sim(F, S, sigmas=SIGMAS, n=3000, seed=12, tdist=True, sub=SUB,
               horizon=HORIZON, keep_paths=False):
    """Funded account until breach, closure after max payouts, or horizon.
    Returns per sigma: life (mean days), pay (mean trader $), n_pay,
    p_any (share with >=1 payout), breach share."""
    G = dict(F, **F.get("funded", {}))
    st = G["start"]; k = len(sigmas); shape = (k, n)
    rng = np.random.default_rng(seed)
    sd = (sigmas / np.sqrt(TD)).astype(np.float32)[:, None] * st
    mu = (S * sigmas / TD).astype(np.float32)[:, None] * st
    acc = _Account(G, shape, st)
    if G.get("start_floor_locked"):      # e.g. instant-funding style accounts
        pass
    live = np.ones(shape, bool); life = np.zeros(shape, int)
    paid = np.zeros(shape, np.float32); gross = np.zeros(shape, np.float32)
    npay = np.zeros(shape, int); since = np.zeros(shape, int)
    qual = np.zeros(shape, int); breach = np.zeros(shape, bool)
    first = G.get("first_wait", 0); cyc = G.get("cycle", 10)
    base = st + G.get("payout_base", 0.0) * st     # balance kept after payout
    frac = G.get("payout_frac", 1.0); cap = G.get("payout_cap")
    caps = G.get("payout_caps")                    # ladder of caps per payout
    mn = G.get("payout_min", 0.0); maxp = G.get("max_payouts")
    split = G["split"]; qd, qmin = G.get("qual_days", 0), G.get("qual_min", 0.0) * st
    full_until = G.get("split_full_until", 0.0)    # first $X at 100%
    yearly = np.zeros((k, n, horizon), np.float32) if keep_paths else None
    for d in range(horizon):
        if not live.any():
            break
        dstart = acc.bal.copy()
        for _ in range(sub):
            inc = mu / sub + sd / np.sqrt(sub) * _noise(rng, shape, tdist)
            dead = acc.step(inc, live)
            breach |= dead; live &= ~dead
        acc.end_day()
        life += live; since += live
        qual += live & ((acc.bal - dstart) >= max(qmin, 1e-9))
        el = live & (life >= first) & (since >= cyc) & (qual >= qd)
        if el.any():
            avail = np.maximum(acc.bal - base, 0) * frac
            if caps is not None:
                c = np.array(caps + [caps[-1]])[np.minimum(npay, len(caps))]
                avail = np.minimum(avail, c)
            elif cap is not None:
                avail = np.minimum(avail, cap * st)
            ok = el & (avail >= max(mn, 1.0))
            if ok.any():
                w = np.where(ok, avail, 0).astype(np.float32)
                acc.bal -= w
                full = np.clip(full_until - gross, 0, None)
                trader = np.minimum(w, full) + split * np.maximum(w - full, 0)
                gross += w; paid += trader
                if keep_paths:
                    yearly[:, :, d] += trader
                npay += ok; since[ok] = 0; qual[ok] = 0
                acc.paylock |= ok
                if maxp:
                    closed = ok & (npay >= maxp)
                    live &= ~closed
    r = dict(life=life.mean(1), pay=paid.mean(1), n_pay=npay.mean(1),
             p_any=(npay > 0).mean(1),
             p_refund=(npay >= G.get("refund_after", 1)).mean(1), breach=breach.mean(1),
             survive=live.mean(1))
    if keep_paths:
        r["paths"] = dict(life=life, paid=paid, yearly=yearly)
    return r


def economics(F, S, n=3000, tdist=True, sub=SUB, sigmas=SIGMAS, seed=11):
    """Renewal-reward per slot-year for every (sigma_e, sigma_f) pair; returns
    the pair that maximizes mean pre-tax net $ per slot-year."""
    E = eval_sim(F, S, sigmas, n, seed, tdist, sub)
    Fd = funded_sim(F, S, sigmas, n, seed + 1, tdist, sub)
    p = np.clip(E["p_pass"], 1e-6, 1)[:, None]
    # expected eval time / fees until the first pass (geometric attempts)
    t_eval = (E["t_fail"] * (1 - E["p_pass"]) / np.clip(E["p_pass"], 1e-6, 1)
              + E["t_pass"])[:, None]
    f_eval = (E["fee_fail"] * (1 - E["p_pass"]) / np.clip(E["p_pass"], 1e-6, 1)
              + E["fee_pass"])[:, None]
    act = F.get("activation", 0.0) + F.get("funded_fixed", 0.0)
    refund = F.get("refund", 0.0) * Fd["p_refund"][None, :]
    fixed_yr = F.get("fixed_year", 0.0)            # per-slot data/API fees
    L = t_eval + Fd["life"][None, :]
    fees = f_eval + act + fixed_yr * L / TD
    reward = Fd["pay"][None, :] + refund - fees
    rate = reward / L * TD                         # $ per slot-year, pre-tax
    fee_rate = fees / L * TD
    rate = np.where(E["p_pass"][:, None] < 1e-4, -fee_rate, rate)
    i, j = np.unravel_index(np.nanargmax(rate), rate.shape)
    net = rate[i, j]
    after = net * (1 - TAX) if net > 0 else net
    return dict(S=S, sig_e=sigmas[i], sig_f=sigmas[j], p_pass=E["p_pass"][i],
                t_eval=float(t_eval[i, 0]), attempts=1 / max(E["p_pass"][i], 1e-6),
                life=Fd["life"][j], pay=Fd["pay"][j], n_pay=Fd["n_pay"][j],
                p_any=Fd["p_any"][j], survive=Fd["survive"][j],
                net_yr=net, fees_yr=fee_rate[i, j],
                ros_pre=net / fee_rate[i, j], ros_after=after / fee_rate[i, j],
                grid=rate)


def min_sharpe(F, target=0.20, lo=0.3, hi=3.0, iters=9, **kw):
    """Smallest S with after-tax ROS >= target (bisection; common random
    numbers make ROS monotone in S in practice)."""
    if economics(F, hi, **kw)["ros_after"] < target:
        return float("nan")
    if economics(F, lo, **kw)["ros_after"] >= target:
        return lo
    for _ in range(iters):
        mid = (lo + hi) / 2
        if economics(F, mid, **kw)["ros_after"] >= target:
            hi = mid
        else:
            lo = mid
    return hi


def slot_years(F, S, sig_e, sig_f, years=3, n=2000, seed=21, tdist=True, sub=SUB):
    """Per-slot yearly pre-tax net $ by chaining simulated attempts and funded
    lives in calendar order (resampled with replacement). Returns (n, years)."""
    E = eval_sim(F, S, np.array([sig_e]), n, seed, tdist, sub)["paths"]
    Fd = funded_sim(F, S, np.array([sig_f]), n, seed + 1, tdist, sub,
                    keep_paths=True)["paths"]
    ep, ed, ef = E["passed"][0], E["days"][0], E["fee"][0]
    fl, fy = Fd["life"][0], Fd["yearly"][0]
    act = F.get("activation", 0.0) + F.get("funded_fixed", 0.0)
    fixed_day = F.get("fixed_year", 0.0) / TD
    refund = F.get("refund", 0.0)
    rng = np.random.default_rng(seed + 2)
    T = years * TD; out = np.zeros((n, years))
    for p in range(n):
        t = 0
        while t < T:
            i = rng.integers(n)
            out[p, min(t, T - 1) // TD] -= ef[i]
            t += max(int(ed[i]), 1)
            if not ep[i] or t >= T:
                continue
            out[p, t // TD] -= act
            j = rng.integers(n)
            ev = np.nonzero(fy[j])[0]
            for k_, day in enumerate(ev):
                if t + day < T:
                    rf = refund if k_ == F.get("refund_after", 1) - 1 else 0
                    out[p, (t + day) // TD] += fy[j, day] + rf
            t += max(int(fl[j]), 1)
        out[p] -= fixed_day * TD
    return out
