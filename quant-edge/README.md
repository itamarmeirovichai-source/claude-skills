# quant-edge program

Autonomous quantitative research and engineering organization for one client (Itamar). Master prompt:
`prompts/quant-edge-master-prompt.md` on branch `claude/sweet-dijkstra-kshdva` (PR #26).

Start here: `WORK-LOG.md` (decisions, steps, checkpoint), `board.md` (shared state), `registry.csv` (every
hypothesis ever counted, 105 inherited rows + program rows), `PARAMETERS.md` (the fixed parameters and the bar).

Layout: `briefs/` (one-page briefs for agents), `letters/` (firm letters Itamar sends himself), `research/candidates.md`,
`research/prereg/`, `research/results/<id>.md`, `data/` (manifest, spend ledger, licences; no market data),
`economics/`, `engineering/`, `reports/<date>.md` (Hebrew), `daily/<date>/`, `src/qe/` (code), `tests/`, `tools/`.

Market data lives under `~/quant-edge-data/`, never here. Secrets come from environment variables only.
