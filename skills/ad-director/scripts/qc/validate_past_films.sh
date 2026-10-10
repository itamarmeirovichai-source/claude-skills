#!/bin/bash
# Re-run the QC validation on our past films (local media only; zero generation spend).
# usage: bash validate_past_films.sh OUT_DIR [PYTHON]
# Writes reports under OUT_DIR. Never commit OUT_DIR (it holds frame strips).
set -u
OUT=${1:?usage: validate_past_films.sh OUT_DIR [PYTHON]}
PY=${2:-python3}
Q=$(cd "$(dirname "$0")" && pwd)
E=$(cd "$Q/../../../.." && pwd)/research/ai-video-reels/lab/experiments
W=$E/W06_lipsync
mkdir -p "$OUT"

echo "### AURUM v1 picture (rebuilt from the v1 clips in the 215e8d2 assemble.sh order)"
F=$E/F04_aurum_topshelf/clips
ffmpeg -v error -y -i $F/A_push_t01.mp4 -i $F/B_open_t01.mp4 -i $F/C_sip_t01.mp4 -i $F/E_float_k_t01.mp4 \
  -i $F/F_land_t01.mp4 -i $F/G_pack_t01.mp4 -filter_complex "\
[0:v]setpts=PTS/1.25,trim=0:4,setpts=PTS-STARTPTS,fps=24,scale=540:960,setsar=1[a];\
[1:v]trim=start=0.0417:duration=5,setpts=PTS-STARTPTS,scale=540:960,setsar=1[b];\
[2:v]trim=start=0.0417:duration=5,setpts=PTS-STARTPTS,scale=540:960,setsar=1[c];\
[3:v]trim=start=0.0417,setpts=1.2*(PTS-STARTPTS),trim=0:6,setpts=PTS-STARTPTS,fps=24,scale=540:960,setsar=1[e];\
[4:v]trim=start=0.0417:duration=5,setpts=PTS-STARTPTS,scale=540:960,setsar=1[f];\
[5:v]trim=start=0.0417:duration=5,setpts=PTS-STARTPTS,scale=540:960,setsar=1[g];\
[a][b][c][e][f][g]concat=n=6:v=1,format=yuv420p[v]" -map "[v]" -c:v libx264 -crf 20 -preset veryfast -t 30 "$OUT/aurum_v1_video.mp4"
$PY $Q/continuity_check.py "$OUT/aurum_v1_video.mp4" --out "$OUT/cont_aurum_v1" --cast 2 --seams 4,9,14,20,25 \
  --object glass=9.5:195,545,95,200 --object glass=13.0:155,255,95,190 \
  --object glass=23.5:55,370,55,120 --object glass=29.0:262,333,135,327

echo "### AURUM v3 final"
V3=$E/F04_aurum_topshelf/final/aurum_topshelf_30.mp4
$PY $Q/qc_report.py "$V3" --out "$OUT/qc_aurum_v3"
$PY $Q/continuity_check.py "$V3" --out "$OUT/cont_aurum_v3" --cast 2 --seams 4,9,13,17.35,22,26 \
  --object glass=9.5:390,1095,180,390 --object glass=12.0:330,615,225,460 \
  --object glass=23.5:90,620,110,335 --object glass=29.0:504,730,230,600

echo "### F09 heist"
$PY $Q/qc_report.py $E/F09_heist/clips/HEIST15_t01.mp4 --stage take --out "$OUT/qc_heist_raw"
$PY $Q/qc_report.py $E/F09_heist/final/aurum_heist_14s.mp4 --out "$OUT/qc_heist_final"
$PY $Q/continuity_check.py $E/F09_heist/clips/HEIST15_t01.mp4 --out "$OUT/cont_heist" --fps 4 --cast 2 \
  --ref-face otto=$E/F09_heist/ref/otto.png --ref-face vee=$E/F09_heist/ref/vee.png

echo "### F07 native-audio test (good)"
$PY $Q/qc_report.py $E/F07_native_audio/clips/T1_t01.mp4 --stage take --out "$OUT/qc_f07"

echo "### W06 lip-sync"
for c in v1_wan_t01:v1 v2_t01:v2 v3_t01:v3 v4c_t01:v4 v4b_t01:v4 v4_old:v4 o1_wan_t01:o1 o3_t01:o3; do
  v=${c%%:*}; a=${c##*:}
  $PY $Q/lipsync_check.py $W/clips/$v.mp4 --audio $W/audio/$a.wav --windows --out "$OUT/lip_raw_$v"
done
for k in v1 v2 v3 v4; do $PY $Q/lipsync_check.py $W/keyed/$k.mp4 --out "$OUT/lip_keyed_$k"; done
$PY $Q/lipsync_check.py $W/clips/v2_t01.mp4 --audio $W/audio/v3.wav --out "$OUT/lip_control_wrong_line"
$PY $Q/lipsync_check.py $W/clips/v4c_t01.mp4 --audio $W/audio/v4.wav --audio-delay 0.2 --out "$OUT/lip_control_plus200"
