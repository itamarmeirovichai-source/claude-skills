"""Gate v2 statistics: t-statistics, bootstraps, Sharpe standard errors, DSR, CSCV, the fixed bar.

All functions take plain numpy arrays. Daily mark-to-market P&L is the default unit; trade-level
series are only for strategies flat by day end, with day clusters.
"""
import math
from itertools import combinations
from statistics import NormalDist
from typing import Optional, Tuple

import numpy as np

try:
    from numba import njit
except Exception:  # pragma: no cover
    def njit(*a, **k):
        def deco(f):
            return f
        return deco if not (a and callable(a[0])) else a[0]

_ND = NormalDist()
N_TOTAL = 430
ALPHA = 0.05 / N_TOTAL
Z_BAR = _ND.inv_cdf(1 - ALPHA)                 # 3.6807
Z_BAR_TWO_COUNT = _ND.inv_cdf(1 - 0.025 / N_TOTAL)  # 3.8538
MIN_DRAWS = int(math.ceil(50 / ALPHA))         # 430,000


def bar_sharpe_units(years: float, z: float = Z_BAR) -> float:
    return z / math.sqrt(years)


def power(true_sharpe: float, years: float, z: float = Z_BAR) -> float:
    return 1 - _ND.cdf(z - true_sharpe * math.sqrt(years))


# ---------------------------------------------------------------- t-statistics
def iid_t(x: np.ndarray) -> float:
    x = np.asarray(x, float)
    n = x.size
    if n < 2:
        return float("nan")
    s = x.std(ddof=1)
    return float(x.mean() / (s / math.sqrt(n))) if s > 0 else float("inf") if x.mean() > 0 else float("nan")


def newey_west_t(x: np.ndarray, lag: int) -> float:
    """t-stat of the mean with Bartlett-kernel HAC variance (Newey-West 1987)."""
    x = np.asarray(x, float)
    n = x.size
    if n < 2:
        return float("nan")
    e = x - x.mean()
    s = float(e @ e)
    for k in range(1, lag + 1):
        w = 1 - k / (lag + 1)
        s += 2 * w * float(e[k:] @ e[:-k])
    var_mean = s / n / n
    return float(x.mean() / math.sqrt(var_mean)) if var_mean > 0 else float("nan")


def gate_t(x: np.ndarray, longest_hold_days: int = 1) -> Tuple[float, float, float]:
    """Returns (min(iid, NW), iid, NW) with NW lag = max(10, longest holding period in days)."""
    a, b = iid_t(x), newey_west_t(x, max(10, int(longest_hold_days)))
    return (min(a, b), a, b)


def clustered_t(values: np.ndarray, clusters: np.ndarray) -> float:
    """Cluster-robust t of the mean of trade-level values clustered by trading day."""
    values = np.asarray(values, float)
    clusters = np.asarray(clusters)
    n = values.size
    m = values.mean()
    e = values - m
    _, inv = np.unique(clusters, return_inverse=True)
    g = inv.max() + 1
    sums = np.bincount(inv, weights=e, minlength=g)
    var = float((sums ** 2).sum()) / n / n * (g / (g - 1)) if g > 1 else float("nan")
    return float(m / math.sqrt(var)) if var and var > 0 else float("nan")


# ------------------------------------------------------------------ bootstraps
@njit(cache=True)
def _stationary_boot_means(x, n_draws, p, seed):
    np.random.seed(seed)
    n = x.size
    out = np.empty(n_draws)
    for d in range(n_draws):
        s = 0.0
        i = np.random.randint(0, n)
        for t in range(n):
            if t > 0 and np.random.random() < p:
                i = np.random.randint(0, n)
            s += x[i]
            i += 1
            if i >= n:
                i = 0
        out[d] = s / n
    return out


def stationary_bootstrap_mean(x: np.ndarray, n_draws: int = MIN_DRAWS, mean_block: float = 20.0,
                              alpha: float = ALPHA, seed: int = 0, chunk: int = 50_000) -> dict:
    """Politis-Romano stationary bootstrap of the mean (geometric blocks, mean length `mean_block`).

    Returns the alpha-quantile (the gate's lower bound), the 5th percentile, the mean and the draw count.
    Draws are generated in chunks so 430,000 draws on 4,000 days fit in memory.
    """
    x = np.ascontiguousarray(np.asarray(x, float))
    p = 1.0 / mean_block
    parts = []
    done = 0
    k = 0
    while done < n_draws:
        m = min(chunk, n_draws - done)
        parts.append(_stationary_boot_means(x, m, p, seed * 1_000_003 + k))
        done += m
        k += 1
    means = np.concatenate(parts)
    return {"lower_alpha": float(np.quantile(means, alpha)), "p5": float(np.quantile(means, 0.05)),
            "p50": float(np.quantile(means, 0.5)), "n_draws": int(means.size), "alpha": alpha, "mean_block": mean_block}


def day_cluster_bootstrap_mean(values: np.ndarray, clusters: np.ndarray, n_draws: int = MIN_DRAWS,
                               alpha: float = ALPHA, seed: int = 0, chunk: int = 50_000) -> dict:
    """Resample whole trading days (clusters) with replacement; statistic = mean R per trade."""
    values = np.asarray(values, float)
    _, inv = np.unique(np.asarray(clusters), return_inverse=True)
    g = inv.max() + 1
    day_sum = np.bincount(inv, weights=values, minlength=g)
    day_cnt = np.bincount(inv, minlength=g).astype(float)
    rng = np.random.default_rng(seed)
    means = np.empty(n_draws)
    done = 0
    while done < n_draws:
        m = min(chunk, n_draws - done)
        idx = rng.integers(0, g, size=(m, g))
        means[done:done + m] = day_sum[idx].sum(axis=1) / day_cnt[idx].sum(axis=1)
        done += m
    return {"lower_alpha": float(np.quantile(means, alpha)), "p5": float(np.quantile(means, 0.05)),
            "p50": float(np.quantile(means, 0.5)), "n_draws": int(n_draws), "alpha": alpha, "n_days": int(g)}


# ------------------------------------------------------------------ Sharpe SE
def sharpe(x: np.ndarray, periods_per_year: int = 252) -> float:
    x = np.asarray(x, float)
    s = x.std(ddof=1)
    return float(x.mean() / s * math.sqrt(periods_per_year)) if s > 0 else float("nan")


def sharpe_se(x: np.ndarray, periods_per_year: int = 252) -> dict:
    """Mertens (2002) / Opdyke (2007) standard error of the per-period Sharpe with skew and kurtosis,
    plus Lo's (2002) first-order autocorrelation adjustment of the annualisation factor."""
    x = np.asarray(x, float)
    n = x.size
    mu, sd = x.mean(), x.std(ddof=1)
    sr = mu / sd
    z = (x - mu) / sd
    g3 = float((z ** 3).mean())
    g4 = float((z ** 4).mean())
    var = (1 + 0.5 * sr ** 2 - g3 * sr + (g4 - 3) / 4 * sr ** 2) / n
    se = math.sqrt(max(var, 0.0))
    rho1 = float(np.corrcoef(x[:-1], x[1:])[0, 1]) if n > 2 else 0.0
    q = periods_per_year
    lo_factor = q / math.sqrt(q + 2 * sum((q - k) * rho1 ** k for k in range(1, q))) if abs(rho1) < 1 else 1.0
    ann = math.sqrt(q)
    return {"sharpe_period": float(sr), "se_period": float(se), "skew": g3, "kurtosis": g4, "n": n,
            "sharpe_annual": float(sr * ann), "se_annual": float(se * ann),
            "ci90_annual": (float((sr - 1.645 * se) * ann), float((sr + 1.645 * se) * ann)),
            "lower90_one_sided_annual": float((sr - 1.2816 * se) * ann),
            "rho1": rho1, "sharpe_annual_lo": float(sr * lo_factor), "lo_factor": float(lo_factor)}


def deflated_sharpe(sr_hat: float, n_trials: int, var_trials: float, skew: float, kurt: float, T: int) -> dict:
    """Bailey & Lopez de Prado (2014). Inputs in per-period units: sr_hat, var_trials (variance of trial Sharpes),
    skew, kurtosis (non-excess), T observations. Returns the expected max Sharpe under the null and the DSR."""
    gamma = 0.5772156649
    sr0 = math.sqrt(max(var_trials, 1e-12)) * ((1 - gamma) * _ND.inv_cdf(1 - 1 / n_trials) + gamma * _ND.inv_cdf(1 - 1 / (n_trials * math.e)))
    denom = math.sqrt(max(1 - skew * sr_hat + (kurt - 1) / 4 * sr_hat ** 2, 1e-12))
    z = (sr_hat - sr0) * math.sqrt(T - 1) / denom
    return {"sr0_period": sr0, "dsr": float(_ND.cdf(z)), "z": float(z), "n_trials": n_trials,
            "var_trials": var_trials, "skew": skew, "kurt": kurt, "T": T}


# ------------------------------------------------------------------------ CSCV
def cscv(returns_matrix: np.ndarray, n_splits: int = 16, periods_per_year: int = 252) -> dict:
    """Combinatorially symmetric cross-validation (Bailey, Borwein, Lopez de Prado, Zhu 2017).

    returns_matrix: T x N (periods x configurations). Returns PBO, the degradation slope (OOS SR on IS SR of the
    IS-selected configuration), and the probability that the IS-selected configuration loses OOS.

    Reading note (measured on Day 0, tests/test_stats.py): because IS and OOS are complementary halves of ONE finite
    sample, a configuration picked for a high IS Sharpe has a mechanically lower OOS Sharpe, so on pure noise with a
    small N the PBO sits well above 0.5 (0.91 at N = 12, T = 1600). PBO is therefore conservative; the Referee reads
    it beside `p_oos_loss` and the slope, and a true skill column still produces PBO near 0."""
    M = np.asarray(returns_matrix, float)
    T, N = M.shape
    if N < 2:
        return {"pbo": float("nan"), "slope": float("nan"), "p_oos_loss": float("nan"), "n_combos": 0, "note": "n/a (single configuration)"}
    blocks = np.array_split(np.arange(T), n_splits)
    half = n_splits // 2
    logits, is_sr, oos_sr = [], [], []
    for comb in combinations(range(n_splits), half):
        is_idx = np.concatenate([blocks[i] for i in comb])
        oos_idx = np.concatenate([blocks[i] for i in range(n_splits) if i not in comb])
        A, B = M[is_idx], M[oos_idx]
        sa = A.mean(0) / (A.std(0, ddof=1) + 1e-12) * math.sqrt(periods_per_year)
        sb = B.mean(0) / (B.std(0, ddof=1) + 1e-12) * math.sqrt(periods_per_year)
        best = int(np.argmax(sa))
        rank = (sb < sb[best]).sum() / N
        w = min(max(rank, 1 / (N + 1)), N / (N + 1))
        logits.append(math.log(w / (1 - w)))
        is_sr.append(sa[best]); oos_sr.append(sb[best])
    logits = np.array(logits); is_sr = np.array(is_sr); oos_sr = np.array(oos_sr)
    slope = float(np.polyfit(is_sr, oos_sr, 1)[0]) if is_sr.std() > 0 else float("nan")
    return {"pbo": float((logits <= 0).mean()), "slope": slope, "p_oos_loss": float((oos_sr < 0).mean()),
            "n_combos": int(logits.size), "n_configs": N}
