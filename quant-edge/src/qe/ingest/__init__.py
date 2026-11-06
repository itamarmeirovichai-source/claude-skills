"""qe.ingest — outcome-free loaders that turn raw downloads into manifest-listed parquet/CSV under DATA_ROOT.

This package and qe.qa are the only places allowed to read raw market-data files (tests/test_no_direct_reads.py).
Every loader has a `--dry-run` flag, pins each raw file by sha256, is idempotent on re-run and writes the manifest row
the moment a file lands (qe.ingest.common.manifest_upsert).
"""
