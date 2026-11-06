# Inherited closed families (Scribe, 2026-11-03)

Paths: PF=`~/quant-edge-inherited/pr4/skills/prop-fleet`, R=`PF/references`, D=`PF/agents/daily`, PR26=`~/quant-edge-inherited/pr26/prompts/research`. Ledger `PF/agents/ledger.csv`: 105 rows, count sum 280, nothing passed; units differ per row ("result fields =" in notes; `PR26/digest-hypotheses-ledger.md`). Fields: ids; data, period; best gross/net; why dead; new row needs; source.

- Bot SMC/ICT/TJR (H0001–04, H0010, H0016); ES 5m setups, SPXUSD 1m 2010–18; replay +0.101R [-0.197,+0.398], TJR gross +0.007R net -0.203R/trade; no gross edge, 0/100 survive; never (retune forbidden, `PF/scripts/hypotheses.py` Z01); `R/tjr.md`.
- Beat-the-Market noise-area momentum (H0005/H0011); SPY 1m 2020–26, ES 2024–26; Sharpe 1.11 to 2024, 2025 -4.9%, 2026 -12.9%, ES -0.07; gone since 2025; only with 2007–19 1m data; `R/second-opinion-audit.md` §4.
- Last-half-hour momentum incl. GEX (H0006/H0019); SPXUSD 2010–18, SPY 2019–25; H0006 net -0.142R/trade, H0019 GEX<0 net +7.69 bp/trade t 1.47; gross ≈ 0.02R vs 0.6 pt RT; none; `R/gamma-H0019.md`, `D/2026-10-04/run.txt`.
- Intraday IBS reversal (H0013/H0014); SPXUSD 2010–18; ex-ante net -0.089R/trade; trade-day filter leaked 0.22R, unregistered run; none, no short-only split; `D/2026-10-05/statistician/audit.txt` §4.
- Overnight-gap fade (H0012/H0017); SPXUSD IS, SPY 2019–25, NQ 2020–25; SPY gross -0.095R net -0.122R/trade t -3.35; negative gross OOS; none (no other k, stop, target); `R/gapfade-H0012.md`.
- 5-min ORB (H0020); NQ 1m 2020-09..2025-11, SPY, SPXUSD; NQ gross +0.110R net -0.005R/trade; R is 13–27 bp of price, cost 0.12–0.23R; 30-min version pre-registered, unrun; `R/orb-H0020.md`.
- 1m/30m VWAP trend (H0021/H0022); NQ 1m 2020–25; H0021 net +4.4 bp/day t 1.38 (gross +12.4); H0022 net +5.04 t 1.68, flat since 2023-11; turnover × cost; new data class only; `R/vwap-H0021.md`, `R/vwap30-H0022.md`.
- Macro events intraday ES/NQ (E2-01..12); SPXUSD IS, SPY+NQ 2019–25; best E2-04 FOMC fade +16.0 bp/event-day t 1.09, opposite sign IS; gross ≈ 0; other instruments or releases only; `R/w2-events.md`, `D/w2-events/redteam/findings.md`.
- Intraday rules across 19 CFDs (D4-01..05); Oanda M1 + HistData, OOS 2013–2020; best gross t +3.53, every net t ≤ -4.6 (% basket/day at 1% vol); turnover, effective N ≈ 8; post-2020 data only; `R/w1-breadth.md`.
- Daily FX/CFD trend + carry (D2-01..09); 32 instruments, OOS 2013–26; best OOS Sharpe 0.16 t 0.54, gross ≤ 0.58 vs 0.96 needed; swap markup 3–4%/yr; curve carry or real value, paid data; `R/w1-fxtrend.md`.
- Crypto (D3-01..11); Binance, OOS 2023–26; long/flat TSMOM +5.61 bp/day t 2.26 Sharpe 1.17 = BTC 1.16; beta (20 best days → 0), other variants dead; funding per 8h or hard-DD overlay; `R/w1-crypto.md`.
- FTMO stock CFDs (E1-01..11); S&P 500 + 46 FTMO names, OOS 2015–26; all 11 net negative, best zero-cost t 2.66; 1:1 leverage, swap both sides ≈7.5%/yr; none at FTMO; `R/w2-stocks.md`.
- Near-miss ensemble (F1-01..03); D3-11 FTMO coins + H0022 US100, 2023–26; +1.65 bp/day t 0.74 Sharpe 0.41, worst day -6.74% breaches 5% DLL; bar ≈ Sharpe 1.95; none; `R/w3-ensemble.md`.
- Turn-of-month S&P (H0023); spx_open_close.csv, OOS 2010–26; net +1.10 bp/day t 1.56, Sharpe 0.38 vs B&H 0.76 at equal exposure; beta; none; ledger row H0023, `R/w1-synthesis.md`.
- Buy-the-dip on 10 index CFDs (G2-01..07); Yahoo daily, OOS 2013–26; G2-06 Sharpe 0.24 t 0.90, alpha t -0.63 vs basket 0.72; swap -7.9% of +17.4% gross; US-only slice only post-2026; `R/w4-meanrev.md`.
- VRP/VIX carry (G1, 0 rows); no safe-list firm lists VIX/VX/VXX, CFE not CME, daily flat kills roll yield; only if FTMO adds a VIX CFD (`D/w4-vrp/symbol_gate.py`); `R/w4-vrp.md`.
- Insider purchases (H0018); SEC Form 4 + Yahoo; OOS 2017-02..2026-04 -0.50%/mo vs SPY t -1.66; sign flipped, 55% of tickers lack history; none; `R/insider-H0018.md`.
- Multi-day futures trend as the goal (H0007; H0008 ETF; H0009/H0015 stacks); 54 futures 1984–2016, ETFs; TSMOM Sharpe 1.17 but 0.46 in 2010–16, ETF OOS 2016–26 0.61 vs 60/40 0.92; daily-flat firms, Sharpe ≈1 vs ≥1.5 needed; FTMO Swing sleeve with hard-DD overlay and bonds; `R/trend-following.md`, `R/stack.md`.

Negative evidence without rows: `briefs/00-common.md`; numbers in `PR26/lit-practitioner.md` "Closed-family cross-references".
