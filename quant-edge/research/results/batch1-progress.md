# Batch 1 progress (Dept D Backtest Engineers) — Q-0001, Q-0003, Q-0005, Q-0006

Registration commit 93cb97a (stamped 2a4b581). Notes appended as work proceeds (UTC).

- 2026-11-06 start: read 00-common, PARAMETERS, method lessons, CONVENTIONS, CAL-D, the four prereg JSONs, Gate v2 (master prompt).
- Infrastructure findings BEFORE any data read for batch 1 (no batch-1 read in registry_reads.log yet):
  1. `qe.registry` splits the `data` field on "," but the batch-1 rows use ";" -> Q-0001/Q-0003 dataset names unparseable. Fix: split on "," or ";".
  2. `qe.gateway._read_file` treats a suffix-less path as CSV; the HistData datasets are partitioned parquet directories. Fix: read a directory with read_parquet.
  Both fixes change no rule, parameter, cost or window; tests added.
