#!/usr/bin/env bash
# Remaster the sound of site films to the spec we sell: -14 LUFS integrated, true peak <= -1.0 dBTP,
# MEASURED ON THE ENCODED FILE (LESSONS: AAC/Opus encoding adds peak). Video is stream-copied (no re-encode).
# Two-pass loudnorm (I=-14, TP=-2, linear), then ebur128 on the output. If the encoded true peak is still
# above -1.0 dBTP, it retries with a lower TP ceiling, then in loudnorm's dynamic mode,
# then (last resort) static gain + an oversampled limiter. Files without audio are skipped.
# Usage: bash scripts/remaster-audio.sh public/media/films/<slug>/full.h264.mp4 [more files...]
#        bash scripts/remaster-audio.sh --measure <file>   (print "LUFS TP" only)
set -euo pipefail

measure() { # prints "<I> <TP>" of the file's audio
  ffmpeg -hide_banner -nostats -i "$1" -map 0:a:0 -filter_complex ebur128=peak=true -f null - 2>&1 |
    awk '/Integrated loudness:/{f=1} f&&/ I:/{i=$2} /True peak:/{p=1} p&&/Peak:/{tp=$2} END{print i, tp}'
}

if [ "${1:-}" = "--measure" ]; then shift; for f in "$@"; do echo "$(measure "$f") $f"; done; exit 0; fi

for SRC in "$@"; do
  if [ -z "$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$SRC" | head -1)" ]; then
    echo "skip (no audio) $SRC"; continue
  fi
  VC=$(ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of csv=p=0 "$SRC")
  if [ "$VC" = "av1" ]; then AC=(-c:a libopus -b:a 160k -ar 48000); else AC=(-c:a aac -b:a 192k -ar 48000); fi
  J=$(ffmpeg -hide_banner -nostats -i "$SRC" -map 0:a:0 -af loudnorm=I=-14:TP=-2:LRA=20:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
  g() { echo "$J" | sed -n "s/.*\"$1\" : \"\(.*\)\".*/\1/p"; }
  MI=$(g input_i); MTP=$(g input_tp); MLRA=$(g input_lra); MT=$(g input_thresh); OFF=$(g target_offset)
  TMP="${SRC%.mp4}.remaster.tmp.mp4"
  ok=0
  # Linear first (pure gain, keeps the mix); dynamic mode only when linear can't reach -14 under the peak ceiling.
  for MODE in "linear=true:TP=-2" "linear=true:TP=-2.5" "linear=true:TP=-3" "linear=false:TP=-2" "linear=false:TP=-2.5" "linear=false:TP=-3" "limiter:TP=0" "limiter:TP=0.5" "limiter:TP=1" "limiter:TP=1.5"; do
    LIN=${MODE%%:*}; TP=${MODE##*TP=}
    if [ "$LIN" = "limiter" ]; then
      # Last resort for very peaky mixes: static gain to target (+TP dB extra to offset the limiting), then a 4x-oversampled -3 dBFS limiter.
      G=$(awk -v m="$MI" -v x="$TP" 'BEGIN{printf "%.2f", -14 - m + x}')
      AF="volume=${G}dB,aresample=192000,alimiter=limit=0.70:attack=1:release=60:level=false,aresample=48000"
    else
      AF="loudnorm=I=-14:TP=$TP:LRA=20:measured_I=$MI:measured_TP=$MTP:measured_LRA=$MLRA:measured_thresh=$MT:offset=$OFF:$LIN"
    fi
    ffmpeg -hide_banner -loglevel error -y -i "$SRC" -map 0:v:0 -map 0:a:0 -c:v copy -af "$AF" \
      "${AC[@]}" -movflags +faststart "$TMP"
    read -r OI OTP < <(measure "$TMP")
    if awk -v i="$OI" -v p="$OTP" 'BEGIN{exit !(i>=-15 && i<=-13 && p<=-1.0)}'; then ok=1; break; fi
  done
  if [ "$ok" = 1 ]; then
    mv "$TMP" "$SRC"
    echo "PASS  in ${MI} LUFS / ${MTP} dBTP  ->  out ${OI} LUFS / ${OTP} dBTP ($LIN, TP ceiling $TP)  $SRC"
  else
    rm -f "$TMP"
    echo "FAIL  in ${MI} / ${MTP}  ->  best ${OI} / ${OTP}  $SRC (left unchanged; take this film off the site)"
  fi
done
