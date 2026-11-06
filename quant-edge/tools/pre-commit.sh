#!/usr/bin/env bash
# quant-edge pre-commit hook: secrets, oversized files, data patterns, manifest paths.
# HexHighEntropyString is disabled: sha256 pins of data files are hex by design; the Databento key rule above stays.
# Install: cp quant-edge/tools/pre-commit.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
set -uo pipefail
ROOT=$(git rev-parse --show-toplevel)
fail=0
files=$(git diff --cached --name-only --diff-filter=ACMR)
for f in $files; do
  [ -f "$ROOT/$f" ] || continue
  size=$(stat -c%s "$ROOT/$f")
  if [ "$size" -gt 1048576 ]; then echo "BLOCKED: $f is $size bytes (> 1 MB)"; fail=1; fi
  case "$f" in
    *.dbn|*.dbn.zst|*.zst|*.parquet|*.h5|*.hdf5|*.csv.gz|*.feather|.env|*/.env|*.env|*.key)
      echo "BLOCKED: $f matches a market-data or secret file pattern"; fail=1;;
  esac
  content=$(git show ":$f" 2>/dev/null || true)
  if printf '%s' "$content" | grep -qE 'db-[A-Za-z0-9]{32}'; then
    echo "BLOCKED: $f contains a Databento key pattern (db- + 32 alphanumerics)"; fail=1; fi
  if printf '%s' "$content" | grep -qE 'AKIA[0-9A-Z]{16}|-----BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY-----|(ALPACA_SECRET_KEY|APCA_API_SECRET_KEY|DATABENTO_API_KEY|TELEGRAM_BOT_TOKEN|IB_PASSWORD)[[:space:]]*[=:][[:space:]]*[A-Za-z0-9_./+-]{16,}'; then
    echo "BLOCKED: $f contains a credential pattern"; fail=1; fi
  if [ -f "$ROOT/quant-edge/data/MANIFEST.md" ] && [ "$f" != "quant-edge/data/MANIFEST.md" ]; then
    if grep -qF -- "| $f |" "$ROOT/quant-edge/data/MANIFEST.md" 2>/dev/null; then
      echo "BLOCKED: $f is a path listed in quant-edge/data/MANIFEST.md (market data)"; fail=1; fi
  fi
done
if command -v detect-secrets-hook >/dev/null 2>&1 && [ -n "$files" ]; then
  if ! detect-secrets-hook --disable-plugin HexHighEntropyString --baseline "$ROOT/quant-edge/.secrets.baseline" $files; then
    echo "BLOCKED: detect-secrets flagged a staged file"; fail=1; fi
elif command -v gitleaks >/dev/null 2>&1; then
  gitleaks protect --staged --redact >/dev/null 2>&1 || { echo "BLOCKED: gitleaks flagged a staged change"; fail=1; }
else
  echo "notice: neither detect-secrets-hook nor gitleaks is installed; pattern rules only"
fi
if [ "$fail" -ne 0 ]; then echo "pre-commit: commit refused"; exit 1; fi
exit 0
