#!/bin/bash
# bake.sh ID : green-key clips/<ID>*_t01.mp4 -> keyed/<ID>.mp4 (stacked alpha) + the line's audio baked in
# (audio delayed 0.125 s to match the measured mouth lag) + keyed/<ID>.words.json (times shifted the same way).
set -e
cd "$(dirname "$0")"; id=$1; src=$(ls clips/${id}_t01.mp4 clips/${id}_wan_t01.mp4 2>/dev/null | head -1)
python3 ../W02_otto_ui/tools/greenkey.py "$src" keyed/_${id}_v.mp4 >/dev/null
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$src")
ffmpeg -v error -y -i keyed/_${id}_v.mp4 -i audio/${id}.wav -filter_complex "[1:a]adelay=125:all=1,apad[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 128k -t "$D" -movflags +faststart keyed/${id}.mp4
rm -f keyed/_${id}_v.mp4
python3 - "$id" <<'PY'
import json,sys
i=sys.argv[1]; w=json.load(open(f'audio/{i}.words.json'))['words']
json.dump({"id":i,"text":" ".join(x['text'] for x in w),"words":[{"text":x['text'],"start":round(x['start']+0.525,3),"end":round(x['end']+0.525,3)} for x in w]},open(f'keyed/{i}.words.json','w'),indent=1)
PY
echo "keyed/${id}.mp4 $(ffprobe -v error -show_entries stream=codec_type,width,height -of csv=p=0 keyed/${id}.mp4 | tr '\n' ' ')"
