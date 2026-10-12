"""F2 (wave 3) stress extension of the D1 prop-economics model.

D1's model lives in agents/daily/w1-prop/prop_model.py and is NOT modified.
This file re-implements its daily simulators (eval_sim, funded_sim,
economics, slot_years) with one extra argument, `stress`, a dict of
switches pre-registered in agents/prereg/F2.csv. With `stress=None` (or {})
every function consumes the random stream in exactly the same order as D1
and returns identical numbers (test_stress_model.py checks this).

Stress switches (all optional):

  df          Student-t degrees of freedom of every shock (D1: 5). The shock is
              scaled to unit variance, so annual vol stays sigma.
  sub         intraday sub-steps per day, i.e. how often equity is checked
              against the limits (D1: 4).
  gap_frac    share of each trading day's variance that arrives as ONE jump
              at the open, before any sub-step (overnight gap). The bot
              cannot react to it.
  weekend_var extra variance, in units of one day's variance, added to the
              opening jump of every 5th trading day (Monday).
              With gaps on, all variances are scaled by 5/(5+weekend_var)
              so the ANNUAL variance is still sigma**2.
  garch       (alpha, beta, hmax): daily variance multiplier
              h' = (1-alpha-beta) + alpha*z**2 + beta*h, z = the day's market
              move in unconditional daily s.d., clipped at hmax. E[h] = 1.
  kill        bot kill switch: when today's loss reaches kill * (daily loss
              limit) the bot closes everything and stays flat until the next
              day. A jump can still carry it through the firm's limit.
  dll_ref     reference for the daily loss limit:
                "equity"  start-of-day equity, floating P&L included (D1);
                "balance" start-of-day closed balance;
                "max"     the higher of the two (strictest).
              Equity is checked against (reference - limit) at every sub-step.
  real_rate   share of open P&L realised into the closed balance at the end
              of each day by daily rebalancing (closed balance lags equity).
              None: balance == equity at all times (D1).
  (firm key) day_cap  $ cap on one day's profit, measured from the day
              reference; the excess is removed at the end of the day (CFT).
  shield      dict(level, cut_split, breach_on): open-P&L shield on the
              funded account (Blue Guardian "Guardian Shield"). When
              equity - closed balance <= -level * start, every position is
              closed (balance = equity) and the bot is flat for the day; the
              first trigger sets the split to cut_split for the rest of that
              account's life, trigger number `breach_on` breaches.

Added after the model red team (post-hoc rows F2-12.., all off by default):

  daily_t     the DAY's move is exactly Student-t(df) (a per-day variance
              mixture v = (df-2)/chi2(df)) and the intraday path is Brownian
              given v. Without it each day is a sum of `sub` t shocks, which
              is close to Gaussian when sub is large (red-team finding 4).
  payout_ref_fix  after a payout, the day's loss reference is recomputed from
              the post-payout balance/equity under dll_ref (finding 6).
  open_stop   bot stop on the funded account: when equity - closed balance
              <= -open_stop * start, the bot closes everything for the day
              (set below a shield so the shield is not reached by diffusion).
  cost_S      Sharpe lost to trading costs of a variant (e.g. realising all
              open P&L every day): the drift uses S - cost_S.

All money is in $, time in trading days (252 a year).
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "w1-prop"))
from prop_model import HORIZON, SIGMAS, SUB, TAX, TD, _Account  # noqa: E402

BASE_STRESS = dict(df=5, sub=SUB, gap_frac=0.0, weekend_var=0.0, garch=None,
                   kill=None, dll_ref="equity", real_rate=None, shield=None,
                   daily_t=False, payout_ref_fix=False, open_stop=None, cost_S=0.0)


def cfg(stress=None):
    c = dict(BASE_STRESS)
    c.update(stress or {})
    return c


def _t(rng, shape, df, tdist=True):
    """Unit-variance shocks. Same call as D1's _noise for the same df."""
    if not tdist:
        return rng.standard_normal(shape, dtype=np.float32)
    z = rng.standard_t(df, size=shape).astype(np.float32)
    return z * np.float32(np.sqrt((df - 2) / df))


class Market:
    """Generates the book's $ P&L increments for one day, per sub-step."""

    def __init__(self, C, mu, sd, shape, rng, tdist=True):
        self.C, self.mu, self.sd, self.shape, self.rng = C, mu, sd, shape, rng
        self.tdist = tdist
        self.h = np.ones(shape, np.float32) if C["garch"] else None
        g, w = C["gap_frac"], C["weekend_var"]
        self.gaps = g > 0 or w > 0
        self.k = 5.0 / (5.0 + w) if self.gaps else 1.0

    def _z(self):
        if self.C["daily_t"]:
            return self.rng.standard_normal(self.shape, dtype=np.float32)
        return _t(self.rng, self.shape, self.C["df"], self.tdist)

    def day(self, d):
        C, sub = self.C, self.C["sub"]
        vol = self.sd if self.h is None else self.sd * np.sqrt(self.h)
        mix = None
        if C["daily_t"]:
            df = C["df"]
            mix = np.sqrt((df - 2) / self.rng.chisquare(df, self.shape)).astype(np.float32)
            vol = vol * mix
        incs = []
        if self.gaps:
            jv = self.k * (C["gap_frac"] + (C["weekend_var"] if d % 5 == 0 else 0.0))
            jump = vol * np.float32(np.sqrt(jv)) * self._z() \
                if jv > 0 else np.zeros(self.shape, np.float32)
            dv = self.k * (1.0 - C["gap_frac"])
        else:
            jump, dv = None, 1.0
        # written exactly as D1 (same dtype promotion) so stress=None matches it
        dsd = vol / np.sqrt(sub) if dv == 1.0 else vol * np.sqrt(dv) / np.sqrt(sub)
        for _ in range(sub):
            incs.append(self.mu / sub + dsd * (self._z() if mix is not None else
                                               _t(self.rng, self.shape, C["df"], self.tdist)))
        if jump is not None:
            incs[0] = incs[0] + jump        # the open: gap lands before any check
        if self.h is not None:
            a, b, hmax = C["garch"]
            z2 = ((sum(incs) - self.mu) / self.sd) ** 2
            self.h = np.minimum((1 - a - b) + a * z2 + b * self.h, hmax).astype(np.float32)
        return incs


class Account(_Account):
    """D1's account plus closed balance, kill switch, DLL reference and shield."""

    def __init__(self, F, shape, start, C):
        super().__init__(F, shape, start)
        self.C = C
        self.closed = np.full(shape, start, np.float32)
        self.shield_hits = np.zeros(shape, int)
        sh = C["shield"]
        self.shield = sh if (sh and F.get("_funded")) else None
        self.open_stop = C["open_stop"] if F.get("_funded") else None

    def reset(self, mask):
        super().reset(mask)
        self.closed[mask] = self.start
        self.shield_hits[mask] = 0

    def _flatten(self, mask):
        self.closed = np.where(mask, self.bal, self.closed)
        self.halted |= mask

    def step(self, inc, live):
        C = self.C
        inc = np.where(live & ~self.halted, inc, 0).astype(np.float32)
        self.bal += inc
        if C["real_rate"] is None:
            self.closed[:] = self.bal
        if self.F["dd_type"] == "trail_intraday":
            np.maximum(self.peak, self.bal, out=self.peak)
        dead = live & (self.bal <= self.floor())
        if self.dll:
            hit = live & (self.bal <= self.day0 - self.dll)
            if self.F.get("dll_hard", True):
                dead |= hit
            else:
                self.halted |= hit
            if C["kill"] is not None:
                ks = live & ~dead & ~self.halted & (self.bal <= self.day0 - C["kill"] * self.dll)
                self._flatten(ks)
        if self.shield is not None:
            trig = live & ~dead & ~self.halted & \
                (self.bal - self.closed <= -self.shield["level"] * self.start)
            self.shield_hits += trig
            dead |= trig & (self.shield_hits >= self.shield["breach_on"])
            self._flatten(trig)
        if self.open_stop is not None:          # after the shield: a jump past both
            os_ = live & ~dead & ~self.halted & \
                (self.bal - self.closed <= -self.open_stop * self.start)
            self._flatten(os_)
        return dead

    def end_day(self):
        C = self.C
        cap = self.F.get("day_cap")              # firm cap on one day's profit, $
        if cap:                                  # (CFT: excess is cut, trades closed)
            over = self.bal > self.day0 + cap
            self.bal = np.where(over, self.day0 + np.float32(cap), self.bal).astype(np.float32)
            self.closed = np.where(over, self.bal, self.closed).astype(np.float32)
        if self.F["dd_type"] == "trail_eod":
            np.maximum(self.peak, self.bal, out=self.peak)
        if C["real_rate"] is None:
            self.closed[:] = self.bal
        else:
            self.closed += np.float32(C["real_rate"]) * (self.bal - self.closed)
        self.day0[:] = self.ref()
        self.halted[:] = False

    def ref(self):
        """Daily-loss reference under dll_ref from the current bal/closed."""
        ref = self.C["dll_ref"]
        if ref == "equity":
            return self.bal
        if ref == "balance":
            return self.closed
        if ref == "max":
            return np.maximum(self.bal, self.closed)
        raise ValueError(ref)


def eval_sim(F, S, sigmas=SIGMAS, n=3000, seed=11, tdist=True, stress=None):
    """As D1's eval_sim, under `stress`."""
    C = cfg(stress)
    st = F["start"]; phases = F["targets"]
    if not phases:
        z = np.zeros(len(sigmas))
        return dict(p_pass=z + 1, t_pass=z, t_fail=z, fee_pass=z + F["fee"],
                    fee_fail=z + F["fee"])
    k = len(sigmas); shape = (k, n)
    rng = np.random.default_rng(seed)
    sd = (sigmas / np.sqrt(TD)).astype(np.float32)[:, None] * st
    mu = ((S - C["cost_S"]) * sigmas / TD).astype(np.float32)[:, None] * st
    mkt = Market(C, mu, sd, shape, rng, tdist)
    acc = Account(F, shape, st, C)
    live = np.ones(shape, bool); passed = np.zeros(shape, bool)
    phase = np.zeros(shape, int); pdays = np.zeros(shape, int)
    days = np.zeros(shape, int); hit = np.zeros(shape, bool)
    lim = F.get("time_limit")
    mind = F.get("min_days", [0] * len(phases))
    for d in range(HORIZON):
        if not live.any():
            break
        trade = live & ~hit
        for inc in mkt.day(d):
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
    sub_fee = F.get("monthly", 0.0)
    months = np.ceil(np.maximum(days, 1) / 21.0) if sub_fee else 0
    fee = F["fee"] + (months - 1) * sub_fee if sub_fee else np.full(shape, F["fee"])
    out = dict(paths=dict(passed=passed, days=days, fee=np.broadcast_to(fee, shape)))
    pp = passed.mean(1)
    out["p_pass"] = pp
    out["t_pass"] = np.where(pp > 0, (days * passed).sum(1) / np.maximum(passed.sum(1), 1), 0)
    out["t_fail"] = np.where(pp < 1, (days * ~passed).sum(1) / np.maximum((~passed).sum(1), 1), 0)
    out["fee_pass"] = np.where(pp > 0, (fee * passed).sum(1) / np.maximum(passed.sum(1), 1), F["fee"])
    out["fee_fail"] = np.where(pp < 1, (fee * ~passed).sum(1) / np.maximum((~passed).sum(1), 1), F["fee"])
    return out


def funded_sim(F, S, sigmas=SIGMAS, n=3000, seed=12, tdist=True, horizon=HORIZON,
               keep_paths=False, stress=None):
    """As D1's funded_sim, under `stress`. Extra outputs: breach_pre1 (share
    breached before the first payout), shield (mean shield triggers)."""
    C = cfg(stress)
    G = dict(F, **F.get("funded", {}), _funded=True)
    st = G["start"]; k = len(sigmas); shape = (k, n)
    rng = np.random.default_rng(seed)
    sd = (sigmas / np.sqrt(TD)).astype(np.float32)[:, None] * st
    mu = ((S - C["cost_S"]) * sigmas / TD).astype(np.float32)[:, None] * st
    mkt = Market(C, mu, sd, shape, rng, tdist)
    acc = Account(G, shape, st, C)
    live = np.ones(shape, bool); life = np.zeros(shape, int)
    paid = np.zeros(shape, np.float32); gross = np.zeros(shape, np.float32)
    npay = np.zeros(shape, int); since = np.zeros(shape, int)
    qual = np.zeros(shape, int); breach = np.zeros(shape, bool)
    first = G.get("first_wait", 0); cyc = G.get("cycle", 10)
    base = st + G.get("payout_base", 0.0) * st
    frac = G.get("payout_frac", 1.0); cap = G.get("payout_cap")
    caps = G.get("payout_caps")
    mn = G.get("payout_min", 0.0); maxp = G.get("max_payouts")
    split = G["split"]; qd, qmin = G.get("qual_days", 0), G.get("qual_min", 0.0) * st
    full_until = G.get("split_full_until", 0.0)
    cut = acc.shield["cut_split"] if acc.shield else None
    yearly = np.zeros((k, n, horizon), np.float32) if keep_paths else None
    for d in range(horizon):
        if not live.any():
            break
        dstart = acc.bal.copy()
        for inc in mkt.day(d):
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
                if C["real_rate"] is not None:     # positions closed for the payout
                    acc.closed = np.where(ok, acc.bal, acc.closed)
                acc.bal -= w
                acc.closed -= w
                acc.day0 -= w
                if C["payout_ref_fix"]:
                    acc.day0 = np.where(ok, acc.ref(), acc.day0).astype(np.float32)
                sp = split if cut is None else np.where(acc.shield_hits > 0, cut, split)
                full = np.clip(full_until - gross, 0, None)
                trader = np.minimum(w, full) + sp * np.maximum(w - full, 0)
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
             survive=live.mean(1), breach_pre1=(breach & (npay == 0)).mean(1),
             shield=acc.shield_hits.mean(1))
    if keep_paths:
        r["paths"] = dict(life=life, paid=paid, yearly=yearly)
    return r


def economics(F, S, n=3000, tdist=True, sigmas=SIGMAS, seed=11, stress=None, E=None, Fd=None):
    """As D1's economics (renewal reward, best (sigma_e, sigma_f) pair).
    E / Fd may be passed in to reuse simulations (they do not depend on fees)."""
    E = E if E is not None else eval_sim(F, S, sigmas, n, seed, tdist, stress)
    Fd = Fd if Fd is not None else funded_sim(F, S, sigmas, n, seed + 1, tdist, stress=stress)
    t_eval = (E["t_fail"] * (1 - E["p_pass"]) / np.clip(E["p_pass"], 1e-6, 1)
              + E["t_pass"])[:, None]
    f_eval = (E["fee_fail"] * (1 - E["p_pass"]) / np.clip(E["p_pass"], 1e-6, 1)
              + E["fee_pass"])[:, None]
    act = F.get("activation", 0.0) + F.get("funded_fixed", 0.0)
    refund = F.get("refund", 0.0) * Fd["p_refund"][None, :]
    fixed_yr = F.get("fixed_year", 0.0)
    L = t_eval + Fd["life"][None, :]
    fees = f_eval + act + fixed_yr * L / TD
    reward = Fd["pay"][None, :] + refund - fees
    rate = reward / L * TD
    fee_rate = fees / L * TD
    rate = np.where(E["p_pass"][:, None] < 1e-4, -fee_rate, rate)
    i, j = np.unravel_index(np.nanargmax(rate), rate.shape)
    net = rate[i, j]
    after = net * (1 - TAX) if net > 0 else net
    return dict(S=S, sig_e=sigmas[i], sig_f=sigmas[j], p_pass=E["p_pass"][i],
                t_eval=float(t_eval[i, 0]), attempts=1 / max(E["p_pass"][i], 1e-6),
                life=Fd["life"][j], pay=Fd["pay"][j], n_pay=Fd["n_pay"][j],
                p_any=Fd["p_any"][j], survive=Fd["survive"][j],
                breach_pre1=Fd.get("breach_pre1", np.full(len(sigmas), np.nan))[j],
                shield=Fd.get("shield", np.zeros(len(sigmas)))[j],
                net_yr=net, fees_yr=fee_rate[i, j],
                ros_pre=net / fee_rate[i, j], ros_after=after / fee_rate[i, j],
                grid=rate)


def capped(grid_out, sigmas, cap):
    """Best (sigma_e, sigma_f) with both <= cap, from a full-grid rate matrix."""
    m = sigmas <= cap + 1e-9
    sub = np.where(m[:, None] & m[None, :], grid_out, -np.inf)
    i, j = np.unravel_index(np.argmax(sub), sub.shape)
    return float(sub[i, j]), float(sigmas[i]), float(sigmas[j])


def slot_years(F, S, sig_e, sig_f, years=3, n=2000, seed=21, tdist=True, stress=None):
    """As D1's slot_years (calendar-order chain of attempts and funded lives);
    fees are paid when an attempt starts and the refund on the date of the
    refund payout. Returns (n, years) pre-tax net $."""
    E = eval_sim(F, S, np.array([sig_e]), n, seed, tdist, stress)["paths"]
    Fd = funded_sim(F, S, np.array([sig_f]), n, seed + 1, tdist,
                    keep_paths=True, stress=stress)["paths"]
    ep, ed, ef = E["passed"][0], E["days"][0], E["fee"][0]
    fl, fy = Fd["life"][0], Fd["yearly"][0]
    act = F.get("activation", 0.0) + F.get("funded_fixed", 0.0)
    fixed_day = F.get("fixed_year", 0.0) / TD
    refund = F.get("refund", 0.0)
    ra = F.get("refund_after", 1)
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
                    rf = refund if k_ == ra - 1 else 0
                    out[p, (t + day) // TD] += fy[j, day] + rf
            t += max(int(fl[j]), 1)
        out[p] -= fixed_day * TD
    return out
