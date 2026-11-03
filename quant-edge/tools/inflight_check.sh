#!/usr/bin/env bash
# Prints the last-modified time of every output path in WORK-LOG's "Agents in flight" table (mode-5 warning sign:
# an in-flight entry whose output has not changed for 60 minutes is presumed dead; apply the Resume rule).
cd "$(git rev-parse --show-toplevel)/quant-edge" || exit 1
awk '/^## Agents in flight/{p=1} /^## Session log/{p=0} p && /^\|/ && !/^\| name/ && !/^\|---/' WORK-LOG.md | while IFS='|' read -r _ name brief out start status _; do
  out=$(echo "$out" | xargs); latest=""
  for g in ${out//,/ }; do for f in $(ls -d $g 2>/dev/null); do m=$(stat -c %y "$f" 2>/dev/null | cut -c1-16); [ "$m" \> "$latest" ] && latest=$m; done; done
  printf '%-70s last write: %s  status:%s\n' "$(echo "$name" | xargs | cut -c1-70)" "${latest:-NONE}" "$(echo "$status" | xargs)"
done
