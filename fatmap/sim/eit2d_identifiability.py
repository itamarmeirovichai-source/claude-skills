"""
EXP-002 — Identifiability of VAT area from a 16-electrode abdominal EIT belt (2D model).

Version 0.1.0 (2026-09-29).  Run:  python3 eit2d_identifiability.py
Outputs: ../results/eit2d_identifiability.json, ../results/figures/eit2d_*.png

Three analyses (all on SIMULATED data from eit2d.py):
 1. Local (Cramer-Rao) analysis: best-case achievable 1-sigma error for VAT area and SAT
    area under different noise levels and different amounts of prior knowledge about the
    nuisance parameters (shape, hydration, contact impedance, belt rotation).
 2. Global counterexample search: for a reference body, find a DIFFERENT body whose VAT
    area differs by a fixed amount but whose voltages are as close as possible.  If the
    RMS difference is below 1 noise-sigma the two bodies are practically indistinguishable.
 3. Blinded test-set generation (sealed; see EXP-002.md) for later inverse methods.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, os.path.dirname(__file__))
import eit2d as E  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")
FIG = os.path.join(RES, "figures")
BLIND = os.path.join(HERE, "..", "data", "blinded")
os.makedirs(FIG, exist_ok=True)
os.makedirs(BLIND, exist_ok=True)

NAMES = E.PARAM_NAMES
RANGE = np.array([E.BOUNDS[k][1] - E.BOUNDS[k][0] for k in NAMES])


def noise_sigma(v, rel):
    """ASSUMPTION A-NOISE-001: per-channel sigma = rel*|V| + floor, floor = 5% of rel*max|V|
    per frequency block. rel=0.001 ~ good lab EIT system on a phantom; rel=0.01 ~ plausible
    absolute-calibration error of a wearable belt on skin (contact, motion)."""
    s = np.empty_like(v)
    half = len(v) // len(E.FREQS_HZ)
    for f in range(len(E.FREQS_HZ)):
        blk = slice(f * half, (f + 1) * half)
        s[blk] = rel * np.abs(v[blk]) + 0.05 * rel * np.abs(v[blk]).max()
    return s


def fwd(theta, freqs=(0, 1)):
    p = E.dict_from(theta)
    mesh = E.build_mesh(p)
    return np.concatenate([E.forward(p, f, mesh) for f in freqs])


def vat_sat(theta):
    a = E.areas_cm2(E.dict_from(theta))
    return np.array([a["VAT"], a["SAT"]])


def jac(fun, theta, h_frac=2e-3):
    base = fun(theta)
    J = np.zeros((len(base), len(theta)))
    for k in range(len(theta)):
        h = h_frac * RANGE[k]
        tp, tm = theta.copy(), theta.copy()
        tp[k] += h; tm[k] -= h
        J[:, k] = (fun(tp) - fun(tm)) / (2 * h)
    return base, J


# Prior scenarios: 1-sigma prior on each parameter (np.inf = unknown)
INF = np.inf
SCENARIOS = {
    "S0_all_unknown": dict(),
    "S1_shape_measured": dict(a=0.005, b=0.005, rot=0.003),
    "S2_S1_plus_contact_known": dict(a=0.005, b=0.005, rot=0.003, log10_z=0.05),
    "S3_S2_plus_hydration_known_1pct": dict(a=0.005, b=0.005, rot=0.003, log10_z=0.05, hyd=0.01),
    "S4_S3_plus_SAT_by_ultrasound_2mm": dict(a=0.005, b=0.005, rot=0.003, log10_z=0.05, hyd=0.01, t_sat=0.002),
}


def crb(J_norm, prior: dict):
    F = J_norm.T @ J_norm
    for k, s in prior.items():
        F[NAMES.index(k), NAMES.index(k)] += 1.0 / s ** 2
    # pseudo-inverse guarded; report condition number too
    w, V = np.linalg.eigh(F)
    w = np.maximum(w, 1e-30)
    cov = (V / w) @ V.T
    return cov, float(w.max() / w.min())


def local_analysis(theta0):
    out = {}
    for freqs, label in (((0, 1), "dual_freq"), ((1,), "single_freq_200k")):
        v0, J = jac(lambda t: fwd(t, freqs), theta0)
        _, Ja = jac(vat_sat, theta0)
        for rel in (0.001, 0.01):
            sig = noise_sigma(v0, rel) if len(freqs) == 2 else rel * np.abs(v0) + 0.05 * rel * np.abs(v0).max()
            Jn = J / sig[:, None]
            for sname, prior in SCENARIOS.items():
                cov, cond = crb(Jn, prior)
                ca = Ja @ cov @ Ja.T
                sd = np.sqrt(np.diag(cov))
                corr = cov / np.outer(sd, sd)
                out[f"{label}|rel={rel}|{sname}"] = dict(
                    vat_sd_cm2=float(np.sqrt(ca[0, 0])), sat_sd_cm2=float(np.sqrt(ca[1, 1])),
                    fisher_condition=cond,
                    param_sd={k: float(s) for k, s in zip(NAMES, sd)},
                    corr_vatrim_hyd=float(corr[NAMES.index("s_rim"), NAMES.index("hyd")]),
                    corr_vatrim_tmus=float(corr[NAMES.index("s_rim"), NAMES.index("t_mus")]),
                    corr_vatrim_score=float(corr[NAMES.index("s_rim"), NAMES.index("s_core")]),
                )
        if label == "dual_freq":
            # singular values of noise-normalised Jacobian with column scaling by range
            sv = np.linalg.svd(J / noise_sigma(v0, 0.01)[:, None] * RANGE[None, :], compute_uv=False)
            out["singular_values_rel1pct_range_scaled"] = sv.tolist()
    return out


def counterexample(theta0, d_vat, rel, prior: dict, free=None, seed_jitter=0.0, rng=None):
    """Find theta1 with VAT(theta1) = VAT(theta0)+d_vat minimising the noise-normalised
    voltage difference (plus prior penalties for parameters that could be measured)."""
    v0 = fwd(theta0)
    sig = noise_sigma(v0, rel)
    target = vat_sat(theta0)[0] + d_vat
    free = list(range(len(NAMES))) if free is None else [NAMES.index(k) for k in free]
    lo = np.array([E.BOUNDS[k][0] for k in NAMES])
    hi = np.array([E.BOUNDS[k][1] for k in NAMES])

    def unpack(x):
        t = theta0.copy(); t[free] = x; return t

    def resid(x):
        t = unpack(x)
        r = [(fwd(t) - v0) / sig]
        r.append([30.0 * (vat_sat(t)[0] - target)])          # hard-ish constraint (per cm2)
        for k, s in prior.items():
            i = NAMES.index(k)
            r.append([(t[i] - theta0[i]) / s])
        return np.concatenate(r)

    x0 = theta0[free].copy()
    # start by moving s_rim to hit the target VAT roughly
    i_rim = NAMES.index("s_rim")
    if i_rim in free:
        j = free.index(i_rim)
        dA = np.gradient  # noqa
        eps = 1e-3
        tp = theta0.copy(); tp[i_rim] += eps
        dvat = (vat_sat(tp)[0] - vat_sat(theta0)[0]) / eps
        x0[j] = np.clip(theta0[i_rim] + d_vat / dvat, lo[i_rim] + 1e-3, hi[i_rim] - 1e-3)
    if rng is not None and seed_jitter > 0:
        x0 = x0 + seed_jitter * RANGE[free] * rng.standard_normal(len(free))
    x0 = np.clip(x0, lo[free] + 1e-6, hi[free] - 1e-6)
    sol = least_squares(resid, x0, bounds=(lo[free], hi[free]), x_scale=RANGE[free], max_nfev=400)
    t1 = unpack(sol.x)
    dv = (fwd(t1) - v0) / sig
    return dict(
        rel_noise=rel, d_vat_target_cm2=d_vat, prior=prior, free=[NAMES[i] for i in free],
        rms_noise_units=float(np.sqrt(np.mean(dv ** 2))),
        max_noise_units=float(np.abs(dv).max()),
        chi2=float(np.sum(dv ** 2)), n_meas=int(len(dv)),
        theta0=E.dict_from(theta0), theta1=E.dict_from(t1),
        areas0=E.areas_cm2(E.dict_from(theta0)), areas1=E.areas_cm2(E.dict_from(t1)),
    )


def make_blinded_set(n=40, seed=20260929):
    """Sealed test set.  Truth stored separately; its SHA-256 is recorded in EXP-002.md.
    RULE: no calibration/training code may read test_truth.npz until the inverse method
    and pass thresholds are frozen in the decision log."""
    rng = np.random.default_rng(seed)
    lo = np.array([E.BOUNDS[k][0] for k in NAMES]); hi = np.array([E.BOUNDS[k][1] for k in NAMES])
    thetas = lo + (hi - lo) * rng.uniform(0.1, 0.9, size=(n, len(NAMES)))
    V, T, A = [], [], []
    for t in thetas:
        v = fwd(t)
        V.append(v + noise_sigma(v, 0.01) * rng.standard_normal(len(v)))
        T.append(t); A.append(vat_sat(t))
    np.savez(os.path.join(BLIND, "test_measurements.npz"), V=np.array(V),
             freqs=np.array(E.FREQS_HZ), noise_rel=0.01, model_version="eit2d 0.1.0")
    truth = os.path.join(BLIND, "test_truth.npz")
    np.savez(truth, theta=np.array(T), vat_sat_cm2=np.array(A), names=np.array(NAMES))
    return hashlib.sha256(open(truth, "rb").read()).hexdigest()


def figures(theta0, ce_list):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection

    cols = {0: "#e8c547", 1: "#b5523b", 2: "#f2a541", 3: "#7aa6c2", 4: "#f2a541", 5: "#dddddd"}
    worst = min(ce_list, key=lambda c: c["rms_noise_units"])
    fig, axs = plt.subplots(1, 3, figsize=(15, 4.6))
    for ax, th, title in ((axs[0], worst["theta0"], "Body A"), (axs[1], worst["theta1"], "Body B")):
        m = E.build_mesh(th)
        pc = PolyCollection(m.nodes[m.tris], facecolors=[cols[t] for t in m.tissue], edgecolors="none")
        ax.add_collection(pc); ax.set_aspect("equal"); ax.autoscale(); ax.axis("off")
        ar = E.areas_cm2(th)
        ax.set_title(f"{title}: VAT {ar['VAT']:.0f} cm², SAT {ar['SAT']:.0f} cm²\n"
                     f"hyd {th['hyd']*100:+.1f}%, t_mus {th['t_mus']*1000:.1f} mm")
        for e in range(E.N_ELEC):
            nd = m.nodes[e * (E.N_ANG // E.N_ELEC)]
            ax.plot(*nd, "ks", ms=4)
    v0 = fwd(E.theta_from(worst["theta0"])); v1 = fwd(E.theta_from(worst["theta1"]))
    sig = noise_sigma(v0, worst["rel_noise"])
    axs[2].plot((v1 - v0) / sig, lw=0.8)
    axs[2].axhline(1, color="k", ls=":"); axs[2].axhline(-1, color="k", ls=":")
    axs[2].set_title(f"B − A voltages in noise-σ units (rel noise {worst['rel_noise']*100:.1f}%)\n"
                     f"RMS {worst['rms_noise_units']:.2f} σ")
    axs[2].set_xlabel("channel (0-207: 5 kHz, 208-415: 200 kHz)")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "eit2d_counterexample.png"), dpi=130)
    plt.close(fig)


def main():
    theta0 = E.theta_from(E.DEFAULT)
    res = {"model": "eit2d 0.1.0", "theta0": E.DEFAULT, "areas0_cm2": E.areas_cm2(E.DEFAULT)}
    res["local"] = local_analysis(theta0)

    rng = np.random.default_rng(1)
    ces = []
    S1 = SCENARIOS["S1_shape_measured"]
    S3 = SCENARIOS["S3_S2_plus_hydration_known_1pct"]
    for rel in (0.001, 0.01):
        for d in (+30.0, -30.0):
            for pname, prior in (("S1", S1), ("S3", S3)):
                best = None
                for trial in range(3):
                    c = counterexample(theta0, d, rel, prior, seed_jitter=0.0 if trial == 0 else 0.08, rng=rng)
                    if best is None or c["rms_noise_units"] < best["rms_noise_units"]:
                        best = c
                best["prior_name"] = pname
                ces.append(best)
                print(f"rel={rel} dVAT={d:+.0f} prior={pname}: RMS {best['rms_noise_units']:.3f} sigma, "
                      f"max {best['max_noise_units']:.2f}")
    # Pure two-parameter confound: VAT vs hydration only
    for rel in (0.001, 0.01):
        c = counterexample(theta0, +30.0, rel, {}, free=["s_rim", "hyd"])
        c["prior_name"] = "only_s_rim_and_hyd_free"; ces.append(c)
        print(f"rel={rel} VAT-vs-hydration only: RMS {c['rms_noise_units']:.3f} sigma")
    res["counterexamples"] = ces
    res["blinded_truth_sha256"] = make_blinded_set()
    with open(os.path.join(RES, "eit2d_identifiability.json"), "w") as f:
        json.dump(res, f, indent=1)
    figures(theta0, [c for c in ces if c["prior_name"] in ("S1", "S3")])

    print("\nLocal CRB summary (VAT sd / SAT sd, cm2):")
    for k, v in res["local"].items():
        if isinstance(v, dict):
            print(f"  {k:70s} VAT {v['vat_sd_cm2']:8.2f}  SAT {v['sat_sd_cm2']:7.2f}  cond {v['fisher_condition']:.1e}")
    print("blinded truth sha256:", res["blinded_truth_sha256"])


if __name__ == "__main__":
    main()
