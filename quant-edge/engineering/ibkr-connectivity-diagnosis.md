# IBKR connectivity diagnosis (Department G, week 1) — DRAFT, being written 2026-11-06

Status: skeleton. Sections follow: (1) Hebrew one-page for Itamar; (2) English technical appendix.

## Evidence found so far (inherited files)
- Bot reads signal prices through `data.feed.MarketDataFeed` (yfinance continuous series), orders through IBKR
  (`~/quant-edge-inherited/pr4/skills/prop-fleet/scripts/futures_bars.py` lines 15, 32-35, 118-130).
- Bot fires 9:20 ET each trading day; "IBC brings the Gateway back after its nightly restart"
  (`references/schedule.md` line 343). Paper Gateway port 4002 (`futures_bars.py` line 70).
- IBKR order ids restart after a gateway restart (`references/schedule.md` line 450).
