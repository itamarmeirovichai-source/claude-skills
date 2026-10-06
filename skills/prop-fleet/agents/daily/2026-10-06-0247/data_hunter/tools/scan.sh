#!/bin/bash
# usage: scan.sh owner/repo ...   -> lists data-like files with raw sizes
S=/tmp/claude-0/-home-user-claude-skills/83e06ccf-6299-5e6f-ac94-4ff79d8a5049/scratchpad/d6/scan
for r in "$@"; do
  d=$S/${r//\//_}
  if [ ! -d $d ]; then GIT_LFS_SKIP_SMUDGE=1 timeout 90 git clone -q --filter=blob:none --no-checkout https://github.com/$r.git $d >/dev/null 2>&1 || { echo "## $r CLONE_FAIL"; continue; }; fi
  sha=$(git -C $d rev-parse HEAD 2>/dev/null); date=$(git -C $d log -1 --format=%cs 2>/dev/null)
  files=$(git -C $d ls-tree -r --name-only HEAD 2>/dev/null | grep -iE '\.(csv|parquet|txt|gz|zip|feather|h5|hdf5|pkl|dbn|zst|arrow|db|sqlite|7z|xz|bz2)$' | grep -viE 'requirements|license|readme|cmake|\.lock' )
  n=$(echo "$files" | grep -c .)
  echo "## $r $sha $date datafiles=$n"
  echo "$files" | grep -iE 'nq|es|qqq|spy|mnq|mes|ndx|spx|nas|1m|1min|minute|5m|ohlc|bars|intraday' | head -40 | while read f; do
     [ -z "$f" ] && continue
     u="https://raw.githubusercontent.com/$r/$sha/$(python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$f")"
     sz=$(curl -sI -m 15 "$u" | awk 'tolower($1)=="content-length:"{print $2}' | tr -d '\r')
     echo "   $sz $f"
  done
done
