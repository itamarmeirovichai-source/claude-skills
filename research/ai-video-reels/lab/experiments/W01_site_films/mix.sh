#!/bin/bash
# mix.sh NAME VIDEO : music bed (trim 30 s, fade out) + sfx under the first 12 s -> final/NAME_30.mp4
set -e
n=$1; v=$2
ffmpeg -v error -y -i "$v" -i audio/${n}_music.mp3 -i audio/${n}_sfx.mp3 -filter_complex \
"[1:a]atrim=0:30,asetpts=N/SR/TB,afade=t=in:d=0.8,afade=t=out:st=27.5:d=2.5,volume=0.85[m];\
[2:a]atrim=0:12,asetpts=N/SR/TB,afade=t=out:st=9:d=3,volume=0.6[s];\
[m][s]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.9[a]" \
-map 0:v -map "[a]" -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 160k -t 30 final/${n}_30.mp4
