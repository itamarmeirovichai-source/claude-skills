#!/bin/bash
# usage: dix_times.sh repo_dir owner/repo path N
d=$1; r=$2; p=$3; n=$4
git -C $d log -n $n --format='%H %cI %aI' -- "$p" | while read sha ci ai; do
  last=$(curl -s -m 20 "https://raw.githubusercontent.com/$r/$sha/$p" | tail -1 | cut -d, -f1)
  echo "$ci $ai $last $sha"
done
