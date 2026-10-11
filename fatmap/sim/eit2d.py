"""
FatMap BOT-SIM / EXP-002 — 2D abdominal-slice EIT forward model (complete electrode model).

Version: 0.1.0  (2026-09-29)

What this is
------------
A deterministic finite-element forward model of ONE axial abdominal slice (roughly the
L4-L5 level where single-slice VAT area is conventionally reported). It maps a small
parameter vector theta (body shape, SAT thickness, muscle thickness, VAT extent,
hydration, electrode contact impedance, electrode-belt rotation) to the boundary
voltages a 16-electrode belt would record at two frequencies.

The mesh is *morphed*, not regenerated, when theta changes: every tissue interface lies
exactly on a mesh ring, so the forward map is smooth in theta and finite-difference
Jacobians are meaningful.

What this is NOT
----------------
* Not 3D. In a real body, current leaves the electrode plane; 2D OVERSTATES how much a
  belt "sees" deep tissue in its own slice and ignores tissue above/below it.
* Conductivity values are assumed order-of-magnitude numbers (see CONDUCTIVITY below),
  not measured values. They must be checked against the IT'IS tissue-property database
  or Gabriel et al. (1996) before any conclusion is treated as more than qualitative.
* The anatomy is a cartoon: ellipse, uniform SAT, uniform muscle, VAT as a peripheral
  band plus a central (mesenteric-like) core, plus a spine block.
"""
from __future__ import annotations

import dataclasses
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

# ----------------------------------------------------------------------------------------
# Assumed conductivities (S/m) at two frequencies.  ASSUMPTION, order of magnitude only.
# Tag: A-COND-001 in data_dictionary.md
# ----------------------------------------------------------------------------------------
FREQS_HZ = (5e3, 200e3)
CONDUCTIVITY = {           # (low f, high f)
    "fat":    (0.025, 0.045),
    "muscle": (0.25, 0.40),   # transverse-ish; anisotropy ignored
    "lean":   (0.25, 0.45),   # visceral organs/bowel/blood mixture
    "bone":   (0.02, 0.03),
}
# Hydration model (ASSUMPTION A-HYD-001): an extracellular-fluid expansion h scales
# lean conductivity by (1+h) at low f and (1+0.6h) at high f; fat by (1+0.5h).
HYD_GAIN = {"fat": (0.5, 0.5), "muscle": (1.0, 0.6), "lean": (1.0, 0.6), "bone": (0.0, 0.0)}

TISSUE_ID = {"sat": 0, "muscle": 1, "vat_rim": 2, "lean": 3, "vat_core": 4, "spine": 5}
TISSUE_MATERIAL = {0: "fat", 1: "muscle", 2: "fat", 3: "lean", 4: "fat", 5: "bone"}

PARAM_NAMES = ["a", "b", "t_sat", "t_mus", "s_rim", "s_core", "hyd", "log10_z", "rot"]
PARAM_UNITS = ["m", "m", "m", "m", "1", "1", "1", "log10(Ohm*m)", "fraction of perimeter"]

DEFAULT = dict(
    a=0.16,        # half-width (lateral), m
    b=0.11,        # half-depth (antero-posterior), m
    t_sat=0.020,   # subcutaneous fat thickness, m
    t_mus=0.012,   # abdominal wall muscle thickness, m
    s_rim=0.80,    # inner edge of peripheral VAT band, as fraction of intra-muscular radius
    s_core=0.30,   # radius of central VAT core, fraction of intra-muscular radius
    hyd=0.0,       # extracellular-fluid expansion (fraction)
    log10_z=-2.0,  # 2D contact impedance, log10(Ohm*m)
    rot=0.0,       # rotation of the electrode belt relative to anatomy, fraction of perimeter
)

BOUNDS = dict(
    a=(0.12, 0.22), b=(0.08, 0.17), t_sat=(0.004, 0.06), t_mus=(0.006, 0.02),
    s_rim=(0.55, 0.97), s_core=(0.05, 0.50), hyd=(-0.08, 0.08), log10_z=(-3.0, -1.0),
    rot=(-0.03, 0.03),
)


def theta_from(d: dict) -> np.ndarray:
    return np.array([d[k] for k in PARAM_NAMES], float)


def dict_from(theta) -> dict:
    return {k: float(v) for k, v in zip(PARAM_NAMES, theta)}


# ----------------------------------------------------------------------------------------
# Mesh
# ----------------------------------------------------------------------------------------
@dataclasses.dataclass
class Mesh:
    nodes: np.ndarray       # (n,2)
    tris: np.ndarray        # (m,3)
    tissue: np.ndarray      # (m,)
    area: np.ndarray        # (m,)
    elec_edges: list        # per electrode: array of (i,j) boundary node pairs


N_ANG = 128            # nodes per ring
N_ELEC = 16
ELEC_HALF = 1          # electrode spans 2*ELEC_HALF boundary edges (~2 cm on typical body)
RINGS_SAT = 5
RINGS_MUS = 3
RINGS_RIM = 4
RINGS_MID = 8
RINGS_CORE = 5
SPINE_ANG = (-0.5 * np.pi - 0.18, -0.5 * np.pi + 0.18)   # posterior sector (anatomical angle)
SPINE_S = (0.40, 0.72)                                    # radial extent (fraction)


def _ellipse_arclength_angles(a, b, n, offset_frac):
    t = np.linspace(0.0, 2 * np.pi, 8193)
    ds = np.hypot(-a * np.sin(t), b * np.cos(t))
    s = np.concatenate([[0.0], np.cumsum(0.5 * (ds[1:] + ds[:-1]) * np.diff(t))])
    targets = (np.arange(n) / n + offset_frac) % 1.0 * s[-1]
    return np.interp(targets, s, t)


def build_mesh(p: dict) -> Mesh:
    a, b = p["a"], p["b"]
    # angular positions: uniform in arclength, shifted by belt rotation.  The ANATOMY is
    # fixed; rotating the belt = shifting which nodes carry electrodes.  To keep the mesh
    # topology fixed we shift node angles (anatomy sampled at shifted angles) and keep
    # electrodes at fixed node indices.
    t = _ellipse_arclength_angles(a, b, N_ANG, p["rot"])
    surf = np.stack([a * np.cos(t), b * np.sin(t)], 1)
    nrm = np.stack([b * np.cos(t), a * np.sin(t)], 1)
    nrm /= np.linalg.norm(nrm, axis=1, keepdims=True)
    anat_ang = np.arctan2(surf[:, 1] / b, surf[:, 0] / a)

    depths = np.concatenate([
        np.linspace(0, p["t_sat"], RINGS_SAT + 1)[:-1],
        np.linspace(p["t_sat"], p["t_sat"] + p["t_mus"], RINGS_MUS + 1)[:-1],
    ])
    rings = [surf - d * nrm[:, :] for d in depths]
    inner = surf - (p["t_sat"] + p["t_mus"]) * nrm
    s_vals = np.concatenate([
        np.linspace(1.0, p["s_rim"], RINGS_RIM + 1)[:-1],
        np.linspace(p["s_rim"], p["s_core"], RINGS_MID + 1)[:-1],
        np.linspace(p["s_core"], 0.0, RINGS_CORE + 1)[:-1],
    ])
    rings += [s * inner for s in s_vals]
    n_r = len(rings)
    nodes = np.concatenate(rings + [np.zeros((1, 2))], 0)
    center = n_r * N_ANG

    # ring "kind" for each band between ring r and r+1
    band_kind = (["sat"] * RINGS_SAT + ["muscle"] * RINGS_MUS + ["vat_rim"] * RINGS_RIM
                 + ["lean"] * RINGS_MID + ["vat_core"] * RINGS_CORE)
    band_s = np.concatenate([np.ones(RINGS_SAT + RINGS_MUS), s_vals])  # s at outer ring of band

    tris, tissue = [], []
    k = np.arange(N_ANG)
    k1 = (k + 1) % N_ANG
    for r in range(n_r - 1):
        o, i = r * N_ANG, (r + 1) * N_ANG
        kind = band_kind[r]
        s_mid = 0.5 * (band_s[r] + band_s[r + 1]) if r + 1 < len(band_s) else band_s[r]
        ang_mid = np.angle(np.exp(1j * anat_ang[k]) + np.exp(1j * anat_ang[k1]))
        tid = np.full(N_ANG, TISSUE_ID[kind])
        if kind in ("vat_rim", "lean"):
            in_spine = (ang_mid > SPINE_ANG[0]) & (ang_mid < SPINE_ANG[1]) & \
                       (s_mid > SPINE_S[0]) & (s_mid < SPINE_S[1])
            tid = np.where(in_spine, TISSUE_ID["spine"], tid)
        tris.append(np.stack([o + k, o + k1, i + k1], 1)); tissue.append(tid)
        tris.append(np.stack([o + k, i + k1, i + k], 1)); tissue.append(tid)
    last = (n_r - 1) * N_ANG
    tris.append(np.stack([last + k, last + k1, np.full(N_ANG, center)], 1))
    tissue.append(np.full(N_ANG, TISSUE_ID["vat_core"]))
    tris = np.concatenate(tris)
    tissue = np.concatenate(tissue)

    x, y = nodes[tris, 0], nodes[tris, 1]
    area = 0.5 * np.abs((x[:, 1] - x[:, 0]) * (y[:, 2] - y[:, 0]) - (x[:, 2] - x[:, 0]) * (y[:, 1] - y[:, 0]))

    step = N_ANG // N_ELEC
    elec_edges = []
    for e in range(N_ELEC):
        c = e * step
        idx = [(c + j) % N_ANG for j in range(-ELEC_HALF, ELEC_HALF + 1)]
        elec_edges.append(np.array([(idx[j], idx[j + 1]) for j in range(len(idx) - 1)]))
    return Mesh(nodes, tris, tissue, area, elec_edges)


def element_sigma(mesh: Mesh, p: dict, f_idx: int) -> np.ndarray:
    sig = np.empty(len(mesh.tissue))
    for tid, mat in TISSUE_MATERIAL.items():
        base = CONDUCTIVITY[mat][f_idx]
        gain = HYD_GAIN[mat][f_idx]
        sig[mesh.tissue == tid] = base * (1.0 + gain * p["hyd"])
    return sig


# ----------------------------------------------------------------------------------------
# FEM with complete electrode model
# ----------------------------------------------------------------------------------------
def _stiffness(mesh: Mesh, sig: np.ndarray) -> sp.csr_matrix:
    P = mesh.nodes[mesh.tris]                     # (m,3,2)
    bx = np.stack([P[:, 1, 1] - P[:, 2, 1], P[:, 2, 1] - P[:, 0, 1], P[:, 0, 1] - P[:, 1, 1]], 1)
    cy = np.stack([P[:, 2, 0] - P[:, 1, 0], P[:, 0, 0] - P[:, 2, 0], P[:, 1, 0] - P[:, 0, 0]], 1)
    ke = (bx[:, :, None] * bx[:, None, :] + cy[:, :, None] * cy[:, None, :]) \
        * (sig / (4 * mesh.area))[:, None, None]
    rows = np.repeat(mesh.tris, 3, axis=1).ravel()
    cols = np.tile(mesh.tris, (1, 3)).ravel()
    n = len(mesh.nodes)
    return sp.csr_matrix((ke.ravel(), (rows, cols)), shape=(n, n))


def adjacent_patterns():
    L = N_ELEC
    I = np.zeros((L, L))
    for d in range(L):
        I[d, d] = 1.0
        I[d, (d + 1) % L] = -1.0
    meas = []
    for d in range(L):
        for m in range(L):
            m2 = (m + 1) % L
            if len({d, (d + 1) % L} & {m, m2}) == 0:
                meas.append((d, m, m2))
    return I, meas


PATTERNS, MEAS = adjacent_patterns()


def forward(p: dict, f_idx: int, mesh: Mesh | None = None) -> np.ndarray:
    """Return the 16x13 = 208 adjacent-drive/adjacent-measure voltages (V per A/m)."""
    if mesh is None:
        mesh = build_mesh(p)
    n, L = len(mesh.nodes), N_ELEC
    z = 10.0 ** p["log10_z"]
    K = _stiffness(mesh, element_sigma(mesh, p, f_idx)).tolil()
    rows, cols, vals = [], [], []
    D = np.zeros(L)
    for l, edges in enumerate(mesh.elec_edges):
        for (i, j) in edges:
            le = np.linalg.norm(mesh.nodes[i] - mesh.nodes[j])
            for (r, c, v) in ((i, i, le / 3), (j, j, le / 3), (i, j, le / 6), (j, i, le / 6)):
                K[r, c] += v / z
            for node in (i, j):
                rows.append(node); cols.append(n + l); vals.append(-le / 2 / z)
            D[l] += le / z
    C = sp.csr_matrix((vals, (rows, cols)), shape=(n, n + L))[:, n:]
    # Lagrange multiplier enforcing sum(U) = 0 (ground)
    ones = sp.csr_matrix(np.ones((1, L)))
    A = sp.bmat([[K.tocsr(), C, None],
                 [C.T, sp.diags(D), ones.T],
                 [None, ones, None]], format="csc")
    lu = spla.splu(A)
    rhs = np.zeros((n + L + 1, L))
    rhs[n:n + L, :] = PATTERNS.T
    sol = lu.solve(rhs)
    U = sol[n:n + L, :]           # electrode potentials, column = drive pattern
    return np.array([U[m, d] - U[m2, d] for (d, m, m2) in MEAS])


def forward_multi(p: dict) -> np.ndarray:
    mesh = build_mesh(p)
    return np.concatenate([forward(p, f, mesh) for f in range(len(FREQS_HZ))])


# ----------------------------------------------------------------------------------------
# Reported quantities (the things a user would actually want)
# ----------------------------------------------------------------------------------------
def areas_cm2(p: dict) -> dict:
    mesh = build_mesh(p)
    out = {}
    for name, tid in TISSUE_ID.items():
        out[name] = float(mesh.area[mesh.tissue == tid].sum() * 1e4)
    out["VAT"] = out["vat_rim"] + out["vat_core"]
    out["SAT"] = out["sat"]
    out["total"] = float(mesh.area.sum() * 1e4)
    return out


if __name__ == "__main__":
    import time
    t0 = time.time()
    v = forward_multi(DEFAULT)
    print("n meas", v.shape, "time %.2fs" % (time.time() - t0))
    print("areas", {k: round(x, 1) for k, x in areas_cm2(DEFAULT).items()})
