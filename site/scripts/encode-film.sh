#!/usr/bin/env bash
# Encode one finished 30 s film into the site's media set (names match src/data/media.json).
# Usage: bash scripts/encode-film.sh <master.mp4> <slug> [poster_time_s=12] [loop_start_s=10]
set -euo pipefail
SRC="$1"; SLUG="$2"; PT="${3:-12}"; LS="${4:-10}"
OUT="$(cd "$(dirname "$0")/.." && pwd)/public/media/films/$SLUG"
mkdir -p "$OUT"
q() { ffmpeg -hide_banner -loglevel error -y "$@"; }
HAS_AUDIO=$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$SRC" | head -1)
# Poster 540 px tall-ish (9:16), WebP
q -ss "$PT" -i "$SRC" -frames:v 1 -vf "scale=-2:960" -c:v libwebp -quality 78 "$OUT/poster.webp"
# 6 s muted ring/tile loop, 640 px tall, no audio track
q -ss "$LS" -t 6 -i "$SRC" -vf "scale=-2:640,fps=24" -an -c:v libsvtav1 -preset 6 -crf 40 -g 48 -pix_fmt yuv420p -movflags +faststart "$OUT/loop.av1.mp4"
q -ss "$LS" -t 6 -i "$SRC" -vf "scale=-2:640,fps=24" -an -c:v libx264 -preset slow -crf 25 -profile:v high -pix_fmt yuv420p -g 48 -movflags +faststart "$OUT/loop.h264.mp4"
# Full film (keeps source resolution up to 1080 tall)
if [ -n "$HAS_AUDIO" ]; then A1=(-c:a libopus -b:a 128k); A2=(-c:a aac -b:a 160k); else A1=(-an); A2=(-an); fi
q -i "$SRC" -vf "scale=-2:'min(1080,ih)'" -c:v libsvtav1 -preset 6 -crf 34 -g 96 -pix_fmt yuv420p "${A1[@]}" -movflags +faststart "$OUT/full.av1.mp4"
q -i "$SRC" -vf "scale=-2:'min(1080,ih)'" -c:v libx264 -preset slow -crf 21 -profile:v high -pix_fmt yuv420p "${A2[@]}" -movflags +faststart "$OUT/full.h264.mp4"
ls -la "$OUT"
