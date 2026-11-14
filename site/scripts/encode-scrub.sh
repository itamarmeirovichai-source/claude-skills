#!/usr/bin/env bash
# All-intra scroll-scrub clip for a pinned scene (every frame a keyframe, no audio), per ref 39 §1.4.
# Usage: bash scripts/encode-scrub.sh <master.mp4> <slug> <start_s> <length_s> [reverse]
#   → public/media/films/<slug>/scrub.h264.mp4 (≤720 wide, 24 fps). Keep it 4–6 s; it is several MB.
set -euo pipefail
SRC="$1"; SLUG="$2"; SS="$3"; LEN="$4"; REV="${5:-}"
OUT="$(cd "$(dirname "$0")/.." && pwd)/public/media/films/$SLUG"
mkdir -p "$OUT"
VF="scale='min(720,iw)':-2:flags=lanczos,fps=24"
[ "$REV" = "reverse" ] && VF="reverse,$VF"
ffmpeg -hide_banner -loglevel error -y -ss "$SS" -t "$LEN" -i "$SRC" -vf "$VF" -an -c:v libx264 -preset slow -crf 23 -g 1 -pix_fmt yuv420p -movflags +faststart "$OUT/scrub.h264.mp4"
ls -la "$OUT/scrub.h264.mp4"
