"""Does the regime chain actually produce clustering? Tail, not mean."""
import numpy as np

def streaks(persistence, spread, avg_R=0.30, rr=2.0, n=2_000_000, seed=4):
    rng = np.random.default_rng(seed)
    p = (avg_R + 1) / (rr + 1)
    pg, pb = p + spread, p - spread
    assert 0 < pb and pg < 1, (pg, pb)
    flips = rng.random(n) > persistence
    good = np.empty(n, bool); g = True
    # vectorised regime walk via cumulative parity of flips
    good = (np.cumsum(flips) % 2 == 0)
    win = rng.random(n) < np.where(good, pg, pb)
    loss = ~win
    # run lengths of consecutive losses
    d = np.diff(np.concatenate(([0], loss.view(np.int8), [0])))
    starts = np.where(d == 1)[0]; ends = np.where(d == -1)[0]
    runs = ends - starts
    return dict(loss_rate=loss.mean(), mean=runs.mean(),
                p99=np.percentile(runs, 99), p999=np.percentile(runs, 99.9),
                mx=runs.max(), ge8=100*(runs >= 8).mean(), ge12=100*(runs >= 12).mean())

print(f"{'scenario':<26} {'loss%':>6} {'mean':>5} {'p99':>4} {'p99.9':>6} {'max':>4} {'>=8':>6} {'>=12':>6}")
print("-" * 68)
for name, pers, spr in [("i.i.d.", 0.50, 0.00),
                        ("mild", 0.90, 0.08),
                        ("strong", 0.97, 0.12),
                        ("severe", 0.99, 0.15),
                        ("extreme", 0.995, 0.20),
                        ("regime-flip", 0.998, 0.28)]:
    s = streaks(pers, spr)
    print(f"{name:<26} {100*s['loss_rate']:>5.1f}% {s['mean']:>5.2f} {s['p99']:>4.0f} "
          f"{s['p999']:>6.0f} {s['mx']:>4.0f} {s['ge8']:>5.2f}% {s['ge12']:>5.2f}%")
