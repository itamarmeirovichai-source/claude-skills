"""Render research/results/Q-0013/14/15.md from the events.py JSONs."""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import kit
from write_result import manifest_lines, reads, years_md, gate_rows, bp

META = {
 "Q-0013": dict(title="month-end Treasury index-extension strike, overnight-session holds on UB + ZN (1h)",
   sign="LONG UB and ZN at equal risk on the sessions T-2, T-1, T of each month", ds=["dbn_glbx_1h_UB", "dbn_glbx_1h_ZN"],
   job="GLBX-20261108-MBU7744PRH ($1.90 estimate)", unit="session", windows="IS 2010-06-07..2014-12-31; OOS 2015-01-01..2024-12-31",
   costs="UB 1 tick (1/32 = $31.25) + $2.50, ZN 1 tick (1/64 = $15.625) + $2.50 per side on notional ($1,000 x price); 2x doubled",
   seeds="stationary bootstrap 0 (430,000 draws, mean block 5 sessions) and month-cluster bootstrap 0 (430,000); random-date null 0 (10,000)",
   n2="OOS 10.0 years; {legs} leg round trips on {n} sessions (need >= 300 on >= 150): met.",
   null_txt=lambda n: (f"- Event vs non-event sessions (same 18:00->16:00 hold, UB + ZN log returns summed, unweighted, before costs): event mean {n['event_mean_raw_bp']:.2f} bp, "
                       f"non-event {n['nonevent_mean_raw_bp']:.2f} bp, difference {n['event_minus_nonevent_raw_bp']:.2f} bp, Welch t {n['welch_t']:.2f}.\n"
                       f"- Random-date null (10,000 draws of the same number of OOS sessions): the event mean sits at percentile {n['random_dates_percentile']:.4f} (need >= 0.95 for criterion 6): "
                       f"{'passed' if n['random_dates_percentile'] >= 0.95 else 'failed'}. Criterion 6 is reached only after criterion 4, which failed."),
   disc=["The month-end sessions are distinguishable from ordinary sessions before costs (Welch t 3.10, random-date percentile 0.997), in the direction the cash evidence describes; "
         "the vol-scaled net mean (+7.9 bp per session of account) is t 1.31, far from the bar 3.68, and the 2x-cost mean is negative. Nothing here is called an edge; "
         "as a stack-sleeve candidate it would need a materially new construction (fewer cost round trips, e.g. one hold T-3 evening -> T 16:00, which is overnight across "
         "firm days and not registered), i.e. a new row and a new count.",
         "Early-close month-ends (e.g. Dec 31, Nov day-after-Thanksgiving if last) use the fallback exit (last bar 11:00..14:00 ET).",
         "Databento's .v.0 mapping changes at the UTC day boundary (00:00 UTC = 19:00/20:00 ET), so on a roll evening the 18:00 ET entry bar can carry the old contract and the exit the new one; the row's roll rule then skips that hold (348 sessions traded vs 354 in the 19:00-entry variant)."]),
 "Q-0014": dict(title="USDA Crop Progress condition change -> ZC/ZS from the 20:00 ET reopen to 13:00 ET (1h)",
   sign="side = -sign(week-on-week change in national good+excellent %), per crop", ds=["dbn_glbx_1h_ZC", "dbn_glbx_1h_ZS", "cal_nass_crop_progress"],
   job="GLBX-20261108-L7G4FFMCNL ($1.55 estimate); event file from 527 archived NASS report texts (ESMIS), outcome-free", unit="report week",
   windows="IS 2010-06-07..2014-12-31; OOS 2015-01-01..2024-12-31",
   costs="ZC and ZS 2 ticks (0.50 cent = $25) + $2.50 per side on notional ($50 per cent x price); 2x doubled",
   seeds="stationary bootstrap 0 (430,000 draws, mean block 5 weeks); sign-flip null 0 (10,000)",
   n2="OOS 10.0 years; {legs} leg round trips on {n} report weeks (need >= 300 on >= 150): **not met** (about 20 rated weeks a year per crop).",
   null_txt=lambda n: f"- Sign-flip null on the gross week series (10,000): p = {n['sign_flip_p']:.4f} (need < 0.05): failed.",
   disc=["Release dates come from each report's own 'Released <date>' line (521 of 527; the 6 others from the archive index, all equal where both exist); time 16:00 ET by NASS practice. "
         "Holiday-Monday reports are dated Tuesday, so the entry is the Tuesday 20:00 reopen.",
         "The national row is the '18 States' total for corn and soybeans, as printed; 'Previous week' from the same report."]),
 "Q-0015": dict(title="NG EIA storage announcement-day premium, Wednesday 18:00 ET -> Thursday 15:00 ET (1h)",
   sign="LONG NG over the report day", ds=["dbn_glbx_1h_NG", "cal_eia_ngsr"],
   job="GLBX-20261108-LENW633LRD ($0.97 estimate); calendar rebuilt by rule, sha256 equal to the 2026-11-04 pin", unit="event",
   windows="IS 2010-06-07..2018-12-31; OOS 2019-01-01..2024-12-31 (D-009: the paper's sample probably ends 2018)",
   costs="NG 1 tick ($0.001 = $10) + $2.50 per side on notional ($10,000 x price); 2x doubled",
   seeds="stationary bootstrap 0 (430,000 draws, mean block 5 events); random-date null 0 (10,000)",
   n2="OOS 6.0 years; {legs} trades on {n} days (need >= 300 on >= 150): **not met** (holiday weeks before 2025 are skipped by the row).",
   null_txt=lambda n: (f"- Event vs non-event sessions (same hold, unweighted log return, before costs): event mean {n['event_mean_raw_bp']:.2f} bp, non-event "
                       f"{n['nonevent_mean_raw_bp']:.2f} bp, difference {n['event_minus_nonevent_raw_bp']:.2f} bp, Welch t {n['welch_t']:.2f}.\n"
                       f"- Random-date null (10,000): event mean at percentile {n['random_dates_percentile']:.4f} (need >= 0.95): failed."),
   disc=["DATA DEPARTURE (in the row): 1h bars instead of NG 1m RTH windows (1m full session $17.29 > the $8 limit). SPLIT DEPARTURE (in the row): OOS 2019-2024.",
         "Holiday weeks before 2025 (real release date unverified) are skipped ex ante, as registered."]),
}


def render(rid):
    m = META[rid]
    r = json.load(open(HERE / f"{rid}_oos.json")); isr = json.load(open(HERE / f"{rid}_is.json"))
    yt, pos, ny = years_md(r)
    g1, g2, gg = r["g1"], r["g2"], r["gross"]
    terc = r["terc"]
    tt = "\n".join(f"| {k} | {terc['count'][k]} | {100*terc['sum'][k]:.3f}% | {1e4*terc['mean'][k]:.2f} |" for k in terc["sum"])
    nb = "\n".join(f"| {k} | {v[0]} | {100*v[1]:.3f}% | {v[2]:.2f} | {v[3]:.2f} |" for k, v in r["neigh"].items())
    sub = "\n".join(f"| {k} | {v[0]} | {v[1]:.2f} | {v[2]:.2f} |" for k, v in r["sub"].items())
    yrs = 6.0 if rid == "Q-0015" else 10.0
    joint = "about 0.53 / 0.78 / 0.87 (interpolated 5-8 y)" if rid == "Q-0015" else "about 0.72 / 0.85 / 0.91"
    near = g1["t_min"] >= kit.BAR - 1.0 and g1["boot_p5_min"] > 0
    md = f"""# {rid} — {m['title']}: Gate-v2 OOS result

Registry row {rid} (registered commit 4588d6c, count 1, sign fixed: {m['sign']}). Script `research/dbn1h/events.py` (plumbing `kit.py`; renderer `render_events.py`). A pre-registered hypothesis under test; nothing here is called an edge.

- Commands: `python3 quant-edge/research/dbn1h/events.py {rid} --stage is`, `--stage oos --dry` (IS data as a pretend window), then `--stage oos` once.
- Seeds: {m['seeds']}; harness 0.
{manifest_lines(m['ds'])}
- Data: Databento GLBX.MDP3 ohlcv-1h continuous `.v.0`, job {m['job']}. QA `data/qa/dbn1h_qa.md` (outcome-free): the rows' hours exist on >= 98% of OOS sessions.
- Windows: {m['windows']}; hold-out not read.
- Costs 1x: {m['costs']}.
- Units: P&L per {m['unit']} as a fraction of account; w = (0.10/sqrt 252)/sigma, sigma = EWMA(com 60) s.d. of the same hold over all prior sessions (as-of strictly before the event).

## registry_reads.log lines for this id

```
{reads(rid)}
```

Reads: IS stage, dry run (IS only), then the OOS stage: one IS read (warm-up) and exactly one OOS read per dataset. No crash after the OOS read; no change after the result.

## Leak checks (IS only, before the OOS read)

| rule | truncation passed | events | violations | perturbation passed | violations |
|---|---|---|---|---|---|
| as registered | {isr['harness']['truncation_passed']} | 30 | {isr['harness']['truncation']} | {isr['harness']['perturbation_passed']} | {isr['harness']['perturbation']} |
| planted look-ahead (side from the hold's own return; must FAIL) | {isr['planted']['truncation_passed']} | 30 | {isr['planted']['truncation']} | {isr['planted']['perturbation_passed']} | {isr['planted']['perturbation']} |

Decisions compared: side and weight per instrument. IS (information only): {isr['is_obs']} traded {m['unit']}s, net 1x {isr['is_net_bp']:.2f} bp, t {isr['is_t']:.2f}; tercile bounds {isr['terciles'][0]:.5f} / {isr['terciles'][1]:.5f}.

## Headline (OOS)

{r['n_obs']} traded {m['unit']}s, {r['legs']} legs.

{gate_rows(r, [("gross", "gross"), ("net 1x", "g1"), ("net 2x", "g2")])}

- Deciding t = {g1['t_min']:.2f} vs bar 3.6807; bootstrap lower bound {bp(g1['boot_lower_min'])} bp <= 0.
- {kit.power_line(yrs)}; joint (criteria 3+4+7) {joint}.

## Criterion 3 (2x cost)

Net 2x {bp(g2['mean'])} bp per {m['unit']}, t {g2['t_min']:.2f}: **{'passed' if g2['mean'] > 0 else 'failed'}**.

## Criterion 6 (nulls)

{m['null_txt'](r['nulls'])}

## Criterion 7 (stability)

{yt}

Years positive {pos} of {ny} (need {int(-(-0.7*ny//1))}).

| vol tercile (IS bounds; -1 = no value) | obs | net1x sum | mean bp |
|---|---|---|---|
{tt}

Neighbours and one-bar delay (fixed in the row; run once on the OOS):

| variant | obs | net1x total | bp per obs | t |
|---|---|---|---|---|
{nb}

Extra concentration figures: {json.dumps(r['extra'], default=str)}

Criterion 7 overall: **{'passed' if r['crit7'] else 'failed'}**.

Sub-periods (information only):

| period | obs | net bp | t |
|---|---|---|---|
{sub}

## Criterion 2

{m['n2'].format(legs=r['legs'], n=r['n_obs'])}

## Verdict (the row's decision rule, applied mechanically)

- (1) criterion 4: t {g1['t_min']:.2f} {'>=' if g1['t_min'] >= kit.BAR else '<'} 3.6807, bootstrap lower bound {bp(g1['boot_lower_min'])} bp: **{'passed' if (g1['t_min'] >= kit.BAR and g1['boot_lower_min'] > 0) else 'failed'}**; (2) criterion 3 **{'passed' if g2['mean'] > 0 else 'failed'}**; (3) criterion 7 **{'passed' if r['crit7'] else 'failed'}**.
- Near-miss (t within 1.0 of the bar, i.e. >= 2.6807, with bootstrap p5 > 0): {'yes' if near else 'no'} (p5 {bp(g1['boot_p5_min'])} bp).
- **Verdict: {r['verdict']}{' (refuted under the row' + chr(39) + 's rule)' if r['verdict'] == 'FAIL' else ''}.** Read against the power above; a failure is not evidence of absence.

## Disclosures

""" + "\n".join("- " + d for d in m["disc"]) + "\n- Hold-out not read.\n"
    (HERE.parents[0] / "results" / f"{rid}.md").write_text(md)
    print(rid, r["verdict"], len(md))


if __name__ == "__main__":
    for rid in sys.argv[1:]:
        render(rid)
