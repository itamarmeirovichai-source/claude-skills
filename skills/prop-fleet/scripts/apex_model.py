"""Eight-year fleet model: N Apex slots, copy-traded (perfectly correlated),
staggered onboarding, full Apex payout mechanics, costs, tax and the
post-year-4 withdrawal plan.
"""
import numpy as np

DAYS_YEAR, DAYS_MONTH, TRADES_DAY = 250, 21, 3
COMM_RT, SLIP_PTS, MES_PT, STOP_PTS = 1.30, 0.25, 5.0, 8.5
MIN_PAYOUT, QUAL_DAYS, CONSIST = 500.0, 5, 0.50

PLANS = {
    "50K": dict(start=50_000., dd=2_500., target=3_000., qmin=200.,
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
