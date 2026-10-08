#!/usr/bin/env bash
# Encode stacked-alpha masters (colour top, alpha-as-luma bottom) into the site's AV1 + HEVC targets.
# Usage: bash scripts/encode-otto.sh <keyed_dir> [otto|vee]
#   mobile 540x1920 (AV1 + HEVC), desktop *_hd 720x2560 (AV1 + HEVC); pop_* / vee_* clips 360x1280 only.
set -euo pipefail
SRC="$1"; WHO="${2:-otto}"
OUT="$(cd "$(dirname "$0")/.." && pwd)/public/media/$WHO"
mkdir -p "$OUT"
q() { ffmpeg -hide_banner -loglevel error -y "$@"; }
enc() { # in, w, h, base
  q -i "$1" -vf "scale=$2:$3:flags=lanczos,format=yuv420p" -an -c:v libsvtav1 -preset 6 -crf 42 -g 48 -svtav1-params tune=0 -movflags +faststart "$4.av1.mp4"
  q -i "$1" -vf "scale=$2:$3:flags=lanczos,format=yuv420p" -an -c:v libx265 -preset medium -crf 28 -tag:v hvc1 -x265-params log-level=error -movflags +faststart "$4.hevc.mp4"
}
for f in "$SRC"/*.mp4; do
  k=$(basename "$f" .mp4)
  case "$k" in
    pop_*|vee_*) enc "$f" 360 1280 "$OUT/$k" ;;
    *) enc "$f" 540 1920 "$OUT/$k"; enc "$f" 720 2560 "$OUT/${k}_hd" ;;
  esac
  echo "encoded $k"
done
